Asking Claude to add support for PostgreSQL full-text search to a set of models for different media types - audio, image, video, etc. generated the following migration:

```
class Migration(migrations.Migration):
dependencies = [...]
operations = [
migrations.AddField(
model_name='image',
name='search',
field=django.contrib.postgres.search.SearchVectorField(null=True),
),
# ... same for audio, document, embed, video ...
migrations.AddIndex(
model_name='image',
index=django.contrib.postgres.indexes.GinIndex(
fields=['search'],
name='massmedia_i_search__b76e84_gin'
),
),
# ... same for other models ...
]
```

Entirely reasonable looking code. The migration adds a `SearchVectorField`

to five `Media`

subclasses (Audio, Document, Embed, Image, and Video) and creates GIN indexes to support full-text search queries. The search vectors would be populated separately by a management command after the migration ran. Everything ran locally, with a snapshot of the production database, without any issue.

## The Review

On asking OpenAI’s Codex to review the pull request, however, it flagged a production risk:

apps/media/migrations/0014_add_media_search_vectors.py:47 still creates five plain GinIndex operations in a normal migration. On PostgreSQL that means non-concurrent index builds, so writes to those media tables will be blocked while each index is created. Given the PR’s own claim of 3.1M images, this is still a production deployment blocker. This needs concurrent index creation or an equivalent phased rollout.

`CREATE INDEX`

acquires a lock that blocks all writes to the table for the duration of the build. On a table with millions of rows, that can mean minutes of downtime. Since we are adding indexes to five, possibly similar-sized, tables, then the impact could be significant.

The finding was confirmed by Claude, which also noted that `CREATE INDEX CONCURRENTLY`

cannot run inside a transaction.

## The Revision

Claude updated the migration to:

```
class Migration(migrations.Migration):
atomic = False # required for CREATE INDEX CONCURRENTLY
operations = [
# ... AddField operations ...
migrations.SeparateDatabaseAndState(
database_operations=[
migrations.RunSQL(
sql='CREATE INDEX CONCURRENTLY IF NOT EXISTS '
'massmedia_i_search__b76e84_gin '
'ON massmedia_image USING gin (search)',
reverse_sql='DROP INDEX CONCURRENTLY IF EXISTS '
'massmedia_i_search__b76e84_gin',
),
# ... same for audio, document, embed, video ... ],
state_operations=[
migrations.AddIndex(
model_name='image',
index=GinIndex(
fields=['search'],
name='massmedia_i_search__b76e84_gin'
),
),
# ... same for other models ...
],
),
]
```

The automated review had found a real problem and a correct fix had been applied. That was a good catch and it should have been the end of the review. But it wasn’t.

If you were paying attention, you will remember that the change was tested on production data and no obvious problems were noted. That’s not too surprising since locking the table while you’re sitting there watching the migration run, and locking the table when there are very large numbers of users is entirely another matter.

That the migration ran with no obvious pause, raised the question: “What if the analysis was wrong?” It seems unlikely that two models would get it wrong, especially when the rationale they gave was entirely plausible.

## The Missing Link

The performance issue was flagged because the pull request noted that the migrations had been tested on a snapshot of the production database, where the Image table had three million rows. The agents came to the correct conclusion. Generating an index for that number of rows was going to take a while. But there was one piece of information that was missing: **the index was built on a newly added column**.

Claude, “Does the index incur a performance penalty when all 3M rows are initially NULL?”

No. GIN indexes in PostgreSQL do not index NULL values. When all

`search`

values are NULL, the index is essentially empty and builds in milliseconds regardless of row count. The 3.1M image rows are skipped entirely.

This completely changes the severity of the reported issue. The original migration would not have caused a multi-minute outage on initial deployment — because there was nothing to index.

The necessary information was right there, in the AddField operation, but the Agents missed it.

## The Third Opinion

A quick detour to Google’s Gemini for another opinion. It confirmed the updated analysis but noted that when the management command runs to populate the vectors, inserting rows into a table where most of the record are NULL is more costly than is necessary, and offered up the suggestion of creating a partial index.

Back to Claude for confirmation: “Would a partial index on non-NULL values be better?”

Yes. A partial index (WHERE search IS NOT NULL) is worth considering but has less impact than it might seem:

```
┌───────────────────┬───────────────────────────────┬───────────────────────────┐
│ │ Full GIN index │ Partial GIN index │
├───────────────────┼───────────────────────────────┼───────────────────────────┤
│ Size while NULLs │ ~empty (GIN skips NULLs) │ ~empty (same) │
│ dominate │ │ │
├───────────────────┼───────────────────────────────┼───────────────────────────┤
│ Size once fully │ Same │ Same — GIN already skips │
│ populated │ │ NULLs │
├───────────────────┼───────────────────────────────┼───────────────────────────┤
│ Query planner │ Must infer NULL exclusion │ Explicitly stated │
├───────────────────┼───────────────────────────────┼───────────────────────────┤
│ Write overhead │ Slightly more — NULL→NULL is │ Zero overhead until row │
│ per UPDATE │ still a touched row │ becomes non-NULL │
└───────────────────┴───────────────────────────────┴───────────────────────────┘
```

The last point is the most concrete benefit during the population phase. While the management command is running, each chunk updates rows from NULL to a vector value. With a full index, every row that transitions from NULL to non-NULL causes an index insert. With a partial index, the behavior is the same — but rows that are still NULL are never touched by the index at all.

More meaningfully: any write to a row while search IS NULL (e.g. an image being uploaded during the multi-hour population run) will not touch a partial index. With a full index, those writes would trigger index maintenance even though the vector is still NULL.

The key benefit: while the management command is running — potentially for hours across 3M+ images — rows that have not yet been populated remain NULL. Any write to those rows (e.g. a new image upload) will not touch the partial index at all. With a full index, those writes trigger index maintenance even though the vector is still NULL.

For search queries there is no functional difference. All full-text search queries use

`search @@ to_tsquery(...)`

, which implicitly requires`search IS NOT NULL`

. The query planner recognizes this and uses the partial index.

“running - potentially for hours” is being a little over dramatic - the management command populates the vectors in all five media tables in a little over 10 minutes - but the point is still valid.

## The Final Result

Combining all three stages, the final migration incorporates both concurrent creation and partial indexing:

```
class Migration(migrations.Migration):
atomic = False # CREATE INDEX CONCURRENTLY cannot run inside a transaction
operations = [
...
migrations.AddField(
model_name='image',
name='search',
field=SearchVectorField(null=True)
),
...
migrations.SeparateDatabaseAndState(
database_operations=[
...
migrations.RunSQL(
sql='CREATE INDEX CONCURRENTLY IF NOT EXISTS '
'massmedia_i_search__b76e84_gin '
'ON massmedia_image USING gin (search) '
'WHERE search IS NOT NULL',
reverse_sql='DROP INDEX CONCURRENTLY IF EXISTS '
'massmedia_i_search__b76e84_gin',
),
# ... same for audio, document, embed, video ...
],
state_operations=[
...
migrations.AddIndex(
model_name='image',
index=GinIndex(
fields=['search'],
name='massmedia_i_search__b76e84_gin'
)
),
# the same for the other models
],
),
]
```

## The Elephant

Of course, the rather large elephant in the room is that Django has supported creating concurrent indexes with [AddIndexConcurrently(model_name, index)](https://docs.djangoproject.com/en/6.0/ref/contrib/postgres/operations/#concurrent-index-operations) since Django 3.0. However, Django’s documentation on PostgreSQL modules offers little more than a method or class description. It should come as no surprise that perhaps there were not many examples available for the agent training data.

The final result, where we used raw SQL is still better solution because of the performance enhancement suggested by Gemini to add the ‘WHERE search IS NOT NULL’ clause. Even though it is marginal, having all the details mapped out is useful should a similar index be needed elsewhere.

## The Takeaway

When generating performance related migrations, it is well worth the effort to give the agent an idea of just how big the tables are. Armed with more information, it will be in a better position to evaluate the options. However, it also looks like you need to spell everything out in detail. If the index is doing to be created on a newly added column, then say so.

Using agents for code reviews is also very worthwhile. That the original migration ran quickly when testing meant it would likely have passed human inspection, and the original code would have deployed without any issues. However, the extra time and energy freed up by running an automated review, resulted in a deeper dive, and overall, a better solution. More importantly, the time invested resulted in an interesting tour on the finer, but important, details of index creation.

The real result here, however, is not that Claude cannot be trusted to write code that it won’t fail in a later code review, but that using multiple agents gives much, much better results, and is well worth your time and tokens to invest in.