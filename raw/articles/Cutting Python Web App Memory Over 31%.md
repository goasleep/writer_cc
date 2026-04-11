**tl;dr;** I cut 3.2 GB of memory usage from our Python web apps using five techniques: async workers, import isolation, the Raw+DC database pattern, local imports for heavy libraries, and disk-based caching. Here are the exact before-and-after numbers for each optimization.

Over the past few weeks, I’ve been ruthlessly focused on reducing memory usage on my web apps, APIs, and daemons. I’ve been following the [one big server pattern](https://talkpython.fm/books/python-in-production/chapter-4-one-big-server-rather-than-many-small-ones) for deploying all the Talk Python web apps, APIs, background services, and supporting infrastructure.

There are a ridiculous number of containers running to make everything go around here at Talk Python (23 apps, APIs, and database servers in total).

Even with that many apps running, the actual server CPU load is quite low. But memory usage is creeping up. The server was running at 65% memory usage on a 16GB server. While that may be fine - [the server’s not that expensive](https://talkpython.fm/blog/posts/we-have-moved-to-hetzner/) - I decided to take some time and see if there were some code level optimizations available.

What I learned was interesting and much of it was a surprise to me. So, I thought I’d share it here with you. I was able to drop the memory usage by 3.2GB basically for free just by changing some settings, changing how I import packages in Python, and proper use of offloading some caching to disk.

## How much memory were the Python apps using before optimization?

For this blog post, I’m going to focus on just two applications. However, I applied this to most of the apps that we own the source code for (as opposed to Umami, etc). Take these as concrete examples more than the entire use case.

Here are the initial stats we’ll be improving on along the way.

| Application | Starting Memory |
|---|---|
|

[Training Search Indexer Daemon](https://training.talkpython.fm/search/all/memory-optimization)**Total****1,988 MB**## How async workers and Quart cut Python web app memory in half

I knew that starting with a core architectural change in how we run our apps and access our database would have huge implications. You see, we’re running our web apps as a web garden, one orchestrator, multiple worker processes via [the lovely Granian](https://github.com/emmett-framework/granian).

I’ve wanted to migrate our remaining web applications to some fully asynchronous application framework. See [Talk Python rewritten in Quart (async Flask)](https://talkpython.fm/blog/posts/talk-python-rewritten-in-quart-async-flask/) for a detailed discussion on this topic. If we have a truly async-capable application server (Granian) and a truly async web framework (Quart), then we can change our deployment style to one worker running fully asynchronous code. Much less blocking code means a single worker is more responsive now. Thus we can work with a single worker instance.

This one change alone would cut the memory usage nearly in half. To facilitate this, we needed two actions:

**Action 1: Rewrite Talk Python Training in Quart**

The first thing I had to do was rewrite Talk Python Training, the app I was mostly focused on at the time, in Quart. This was a lot of work. You might not know it from the outside, but Talk Python Training is a significant application.

![](talk-python-training.png)

178,000 lines of code! Rewriting this from the older framework, Pyramid, to async Flask (aka Quart), was a lot of work, but I pulled it off last week.

**Action 2: Rewrite data access to raw + dc design pattern**

Data access was based on MongoEngine, a barely maintained older database ODM for talking to MongoDB, which does not support async code and never will support async code. Even though we have Quart as a runtime option, we hardly can do anything async without the data access layer.

So I spent some time removing MongoEngine and implementing the Raw + DC design pattern. That saved us a ton of memory, facilitated writing async queries, and almost doubled our requests per second.

I actually wrote this up in isolation here with some nice graphs: [Raw+DC Database Pattern: A Retrospective](https://mkennedy.codes/posts/raw-dc-a-retrospective/). Switching from a formalized ODM to raw database queries along with data classes with slots **saved us 100 MB per worker process**, or in this case, 200 MB of working memory. Given that it also sped up the app significantly, that’s a serious win.

| Change | Memory Saved | Bonus |
|---|---|---|
| Rewrite to Quart (async Flask) | Enabled single-worker mode | Async capable |
| Raw + DC database pattern | 200 MB (100 MB per worker) | Almost 2x requests/sec |

## How switching to a single async Granian worker saved 542 MB

Now that our web app runs asynchronously and our database queries fully support it, we could trim our web garden down to a single, fully asynchronous worker process using Granian. When every request is run in a blocking mode, one worker not ideal. But now the requests all interleave using Python concurrency.

This brought things down to a whopping 536 MB in total (**a savings of 542 MB**!) I could have stopped there, and things would have been excellent compared to where we were before, but I wanted to see what else was a possibility.

| Metric | Value |
|---|---|
Before (multi-worker) |
1,280 MB |
After (single async worker and raw+dc) |
536 MB |
Savings |
542 MB |

## How isolating Python imports in a subprocess cut memory from 708 MB to 22 MB

The next biggest problem was that the Talk Python Training search indexer. It reads literally everything from the many gigabyte database backing Talk Python Training, indexes it, and stores it into a custom data structure that we use for our ultra-fast search. It was running at 708 MB in its own container.

Surely, this could be more efficient.

And boy, was it. There were two main takeaways here. I noticed first that even if no indexing ran, just at startup, this process was using almost 200 megabytes of memory. Why? Import chains.

The short version is it was importing almost all of the files of Talk Python Training and their in third-party dependencies because that was just the easiest way to write the code and because of PEP 8. When the app starts, it imports a few utilities from Talk Python Training. That, in turn, pulls in the entire mega application plus all of the dependencies that the application itself is using, bloating the memory way, way up.

All this little daemon needs to do is every few hours re-index the site. It sits there, does nothing in particular related to our app, loops around, waits for exit commands from Docker, and if enough time has elapsed, then it runs the search process with our code.

We could move all of that search indexing code into a subprocess. And only that subprocess’s code actually imports anything of significance. When the search index has to run, that process kicks off for maybe 30 seconds, builds the index, uses a bunch of memory, but once the indexing is done, it shuts down and even the imports are unloaded.

What was the change? Amazing. **The search indexer went from 708 MB to just 22 MB**! All we had to do was isolate imports into its own separate file and then run that separately using a Python subprocess. That’s it, 32x less memory used.

| Metric | Value |
|---|---|
Before (monolithic process) |
708 MB |
After (subprocess isolation) |
22 MB |
Reduction |
32x |

## How much memory do Python imports like boto3, pandas, and matplotlib use?

When we write simple code such as `import boto3`

it looks like no big deal. You’re just telling Python you need to use this library. But as I hinted at above, what it actually does is load up that library in total, and any static data or singleton-style data is created, as well as transitive dependencies for that library.

Unbeknownst to me, boto3 takes a ton of memory.

| Import Statement | Memory Cost (3.14) |
|---|---|
`import boto3` |
25 MB |
`import matplotlib` |
17 MB |
`import pandas` |
44 MB |

Yet for our application, these are very rarely used. Maybe we need to upload a file to blob storage using boto3, or use matplotlib and pandas to generate some report that we rarely run.

By moving these to be local imports, we are able to save a ton of memory. What do I mean by that? Simply don’t follow PEP 8 here - instead of putting these at the top of your file, put them inside of the functions that use them, and they will only be imported if those functions are called.

```
def generate_usage_report():
import matplotlib
import pandas
# Write code with these libs...
```

Now eventually, this generate_usage_report function probably will get called, but that’s where you go back to DevOps. We can simply set a time-to-live on the worker process. Granian will gracefully shut down the worker process and start a new one every six hours or once a day or whatever you choose.

**PEP 810 – Explicit lazy imports**

This makes me very excited for Python 3.15. That’s where [the lazy imports feature](https://peps.python.org/pep-0810/) will land. That *should* make this behavior entirely automatic without the need to jump through hoops.

## How moving Python caches to diskcache reduced memory usage

Finally I addressed our caches. This was probably the smallest of the improvements, but still relevant. We had quite a few things that were small to medium-sized caches being kept in memory. For example, the site takes a fragment of markdown which is repeatedly used, and instead of regenerating it every time, we would stash the generated markdown and just return that from cache.

We moved most of this caching to diskcache. If you want to hear me and Vincent nerd out on how powerful this little library is, listen to the Talk Python episode [diskcache: Your secret Python perf weapon](https://talkpython.fm/episodes/show/534/diskcache-your-secret-python-perf-weapon).

## Total memory savings: from 1,988 MB to 472 MB

![](memory-graph.webp)

So where are things today after applying these optimizations?

| Application | Before | After | Savings |
|---|---|---|---|
|

**1.8x**[Training Search Indexer Daemon](https://training.talkpython.fm/search/all/memory-optimization)**32x****Total****1,988 MB****472 MB****3.2x**Applying these techniques and more to all of our web apps **reduced our server load by 3.2 GB of memory**. Memory is often the most expensive and scarce resource in production servers. This is a huge win for us.