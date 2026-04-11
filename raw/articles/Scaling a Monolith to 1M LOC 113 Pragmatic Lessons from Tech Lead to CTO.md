Kill Worker Processes Regularly as Insurance Against Memory Leaks.

This one IMO is wrong. As in having resilience to leaks is indeed very important, but restarting processes at regular interval only hides the problem until it become so dire that you need to restart even more often.

The better solution is to restart once a fixed memory threshold has been reached, this way you can instrument how often processes need to restart and know that a leak or bloat has been introduced.

Self plug on that exact subject: [https://byroot.github.io/ruby/performance/2025/02/09/guard-rails-are-not-code-smells.html](https://byroot.github.io/ruby/performance/2025/02/09/guard-rails-are-not-code-smells.html)

This one IMO is wrong. As in having resilience to leaks is indeed very important, but restarting processes at regular interval only hides the problem until it become so dire that you need to restart even more often.

Author here: Thanks for the feedback!

In the article I present my points with confidence for the sake of it, but in reality I am on the fence about this one. Ideally, I would like to *NOT* restart worker processes at all and just get rid of memory leaks as they occur. But OTOH with a growing team, you never know what will get deployed.

I very much like your idea of restarting once a fixed memory threshold has been reached. I wonder if available for Gunicorn in Python.

I wonder if available for Gunicorn in Python.

I haven't used Python in two decades, but a quick googling shows it has a `post_request`

hook: [https://gunicorn.org/reference/settings/?h=post_request#post_request](https://gunicorn.org/reference/settings/?h=post_request#post_request)

So from there you can check `/proc/self/smaps_rollup`

(assuming Linux) and call `sys.exit()`

if PSS is above the defined threshold. If `gunicorn`

is anything like `unicorn`

it will fork a new worker to replace it almost immediately.

Kill Worker Processes Regularly as Insurance Against Memory Leaks.

I'm wondering if they really mean memory fragmentation, which can be fixed by swapping out the memory allocator with jemalloc or similar. They don't mention what they are doing other than the restarts, so suspicious that they might not have considered that at all.

Bonus, if there really is a memory leak, jemalloc's heap profiler is good and can help you find them.

I can only guess. But since the context is multiprocessing web services, there isn’t just malloc fragmentation to consider.

The managed heap fragmentation is also an issue as if the GC isn’t moving, it might prevent releasing memory to the system.

Similarly multiprocessing rely heavily on CoW and that gets invalidated over time.

Hence even with jemalloc it’s quite common to see PSS slowly grow over time, and restarting processes once in a while is a good idea. Especially since it’s relatively cheap (just a fork).

Also, depending on what you do, killing threads and processes (if you make use of lockfiles and shared memory) can leave your system in a really bad state. It is generally a good idea to have a graceful shutdown mechanism instead.

I think you need to design your architecture to avoid turning to mush when a process dies because it didn't get the chance to release a lock. Graceful shutdown is good but it's not great if for whatever reason your shutdown can't complete, or someone really did need to kill your process before it got a chance to.

Not saying that's always possible, but once you get into multi-process territory it helps to start thinking in terms of distributed systems and assuming any non atomic action may fail to complete. It's a different way of thinking but pays off imo.

See [https://en.wikipedia.org/wiki/Crash-only_software](https://en.wikipedia.org/wiki/Crash-only_software):

A crash-only software is a computer program that handle failures by simply restarting, without attempting any sophisticated recovery.

Author here: If it helps to add context, I am using Gunicorn server max-requests parameter ([https://gunicorn.org/reference/settings/#max_requests](https://gunicorn.org/reference/settings/#max_requests))

The idea (I think!) is that it will shut down that worker after it has had a chance to serve the last (e.g. the 10k-th) request. Gunicorn sits in front of Django in typical setups and ideally should not be holding any resources such as DB connections of file openings. In ways, it acts like a proxy server I suppose.

Regrettably a WSGI/Gunicorn nerd here :(. Fair warning I skipped lunch today so sorry if I've misunderstood what you wrote and am responding to something you didn't mean.

I don't know much about Django, but assuming it just sets up a vanilla WSGI app the architecture is:

Max requests applies to the worker processes and not the arbiter process. So the process which contains your Django code is shutting down and being restarted.

Oh indeed you are completely right! I stand corrected.

Also, depending on what you do, killing threads and processes (if you make use of lockfiles and shared memory) can leave your system in a really bad state.

Given that this will happen in production (process panics/throws an exception because of a bug in someone else's code that runs in-process, OOM killer, systemd, someone pulls the wrong cable in the datacentre, hardware failures, etc), I think you generally want to ensure software is "crash safe". Often this can be done by hitching to the database (e.g. SQLite is extremely crash safe).

The reason you would want to periodically restart workers instead of *reactively* is so that the restart behavior becomes predictable and controllable, and all downstream performance/load implications on e.g. DB do too. Like you said, the drawback is that this approach hides memory regressions even more effectively. I think ideally you'd have separate config for your canary vs main deployments.

Lots of good and sensible advice here!

I think the title might be suggest the wrong audience, folks who are expecting to run a 50k loc service for the first time would benefit from reading this. Don't need to be aiming to run such a large application to benefit.

Author here: Thanks! I might take your advice and present it differently if I share it somewhere else in future.

Some minor, unsolicited nits:

Reasonable advice though. The "100 lessons" format isn't usually as on the nose. Any single lesson here would resonate with a senior engineer, but I'd be challenged to make such a comprehensive list if asked; well done. :)

Random commentary while reading below

Page Counts Are a Major (but Surprising) Source of DB Performance Issues at Scale

Surprised to not see probabilistic data structures like HLL mentioned here — but perhaps that's what is meant by "for very large tables, we use an estimated count paginator".

Delete Useless Data

I wish this was easier, sometimes. I've been places with either contracts that prevented us from deleting expensive data or sales teams wanting us to hold churned client data for longer (at their approval) in hopes of winning them back.

Prevent Long PRs

I'm looking forward to stacked PRs in Github soon. This is a skill that's atrophied for me since leaving BigCo.

Observability CLI Tooling Is Your Number One Force Multiplier for AI

I wish I had leaned into using LLMs for investigations sooner, because my mind has been blown by this very thing. They're surprisingly (or maybe not) good at looking for trends of telemetry data.

probabilistic data structures like HLL

Author here. I didn't bring it up because I never considered this as a possibility at the DB level for these problems! Thanks for the pointer - I see there are extensions available in PG too.

I'm looking forward to stacked PRs in Github soon

Do you have a link for this one? I tried searching for relevant announcements or rumours and came up dry. Just a sea of third party attempts to make it work in spite of GitHub

Sure thing: [https://github.com/github/roadmap/issues/1218](https://github.com/github/roadmap/issues/1218)

Tell Your Database What Kind of Process Was Connected: We started sending application_name to PostgreSQL to understand whether it was a web node (and which one), worker, or schedule node that might be holding a lock for a long time. This is useful when working with pg_stat_activity. (And, in general, learning your database introspection tools -- including for redis etc. too -- is high ROI)

This is in general pretty good advice. Although I got burned on it recently. We went further w/ a unique identifier for each worker in the application_name. Made cancelling work during shutdown/release a lot easier. You could just term/cancel with the unique name.

What we didn't realize is that pinned the connection via the proxy (RDS in this case) and it caused a blowup in the number of connections.

FWIW, I like it. It's advice I've given or taken. A couple of comments:

Author here: TBH we haven't solved the page/item count problem well enough for our main public listings endpoint yet. Materialized view for common counts (refreshed daily during the night) could well do it!

Not familiar with the reference to Dekker but it sounds up my alley.

I'm glad I gave you an idea. I got it from a DBA in the early 2000's. They also put me later onto Joe Celko's books on SQL which are full of DB techniques and advice.

Reading links to start one thinking about failure, for anyone who comes across this:

[Comment removed by author]

Maybe it isn't aimed at people who have already lived through this several times? That doesn't make it worthless like you're implying. A lot of people are still in the middle of learning these lessons, and there is value in someone reflecting honestly on what took them years to understand. I don't think posturing like this is particularly useful. "Not new to me" isn't the same as "this isn't worth sharing".

[Comment removed by author]

Get to Inbox Zero (or Close Enough) in Your Exception Reporting Software (e.g., Sentry)

from your lips to $DEITY's ears

It sounds like you've independently rediscovered several principles of [SRE](https://en.wikipedia.org/wiki/Site_reliability_engineering). There are three big gaps: capacity planning, disaster recovery, and the concept of balancing load or having a dedicated load balancer. Playbooks/runbooks are a great idea; let's do more of those!

Note that some of these issues are de facto solved by a modern k8s deployment with a modern centralized observability solution like Grafana. Other issues are more easily solved by not using orms & python. :-)

But, good list. Lots of bits to gnaw on.

All Programmers Should Be (Somewhat) Full-Stack

A rare case when I strongly disagree. Yes, if you are doing web, you'd need a couple of true senior full-stack folks to keep things well integrated and help specialized teams find common ground efficiently.

But asking every Go developer to understand React? Not really. If they do understand a CLI efficiently logging the same data a web page renders, we're good to go.

What should be full-stack and have long retention period is tracing 😋

I think I'm so cynical about the industry now that I'm even questioning why bother when you can just have the LLM do the work and not even bother knowing the full stack.

AI Winter can't come fast enough for me.

Yeah, I feel you, was thinking the same while writing my comment 😅 But still, for now it still is the case. I'm still hoping that LLMs are like Google to my local library, C to my ASM and like Perl/PHP to my C 🙂

`All Programmers Should Be (Somewhat) Full-Stack`

A rare case when I strongly disagree. Yes, if you are doing web, you'd need a couple of true senior full-stack folks to keep things well integrated and help specialized teams find common ground efficiently.

I'll partially disagree with your disagreement ☺️ I never want to hear someone say, "I'm a [X-type] Engineer, I don't do [Y]." You don't need to be good or even more than a beginner, but you should have a idea about what you colleagues actually do and what they want/request.

What should be full-stack and have long retention period is tracing 😋

Strong agree. And I have opinions on message content and enhancement for people who use streams, queues, pub-sub, etc.

I never want to hear someone say, "I'm a [X-type] Engineer, I don't do [Y]."

I feel you. This is a popular maxima I've heard a lot throughout my career.

A counterargument I usually give is engineering. A steam engine engineer should not be expected to hop on fixing electricity. As a DIY, sure, but the old electricians' joke "— when did their home burn down? — How did you know?" still applies 😅

A counterargument I usually give is engineering. A steam engine engineer should not be expected to hop on fixing electricity. As a DIY, sure, but the old electricians' joke "— when did their home burn down? — How did you know?" still applies 😅

Sure, just because you're an expert in one area doesn't make you an expert in another but in the trades the master plumber knows the basics of wiring and the electrician knows a little about plumbing and both know a little about framing (extending this bad analogy, no, the dry-wallers and roofers won't know much of other trades but they'll know where to get beer 😆). You wouldn't put any of them in charge of structural changes.

I probably agree with you, but I would really like to lament that we need two engineers to implement every user-facing feature with all of the coordination and communication overhead that entails. In the year of our lord 2026, we really should have a frontend application framework that backend engineers can use for 99% of cases.

It feels like the Go people need to do for the frontend what they did for the backend--make dead simple tooling that is just a "go build" / "go test" / etc and it does the right thing by default 99% of the time with minimum configuration. People will piss and moan about the lack of expressivity and choice and power and how it does things differently than their favorite system, and after a few years everyone's favorite system will (quietly) either simplify their defaults or languish and we'll all pretend that our favorite systems had been this nice/simple the whole time.

True. HTMX is our friend then. But anything competitive on the market would require a proper UI. Which has never been friendly since Delphi fall out of fashion 🙃