The knee-jerk guess is that people don’t want a VC-backed tool [...]

This is not a knee jerk reaction; this is roughly half of why I intentionally stayed away from using astral products in load-bearing capabilities at work: this financing model guarantees a tool that will enshittify somehow, and I don't want to be holding the bag when it does and i've already drank the kool-aid. Acquisition by OpenAI was a worse outcome than expected, but I expected something like it.

The other half of why i avoided astral products is that I am broadly unimpressed with tools for language A that are written in language B by people outside A-language's in-group, particularly when they're presented as "One Big Tool That Solves All Your Five-Tool Problems ... But Faster"! Astral's products assuredly were and are presented in this way. As is usually the case, in the event they turn out to be 80/20 ports that are advertised as drop-in replacements but aren't, and that don't cover the hard 20% that I inevitably have to deal with. In the case of `uv`

, that sales pitch backfired hard enough when the tool was new that it lead to the post-hoc creation of [documents like this](https://github.com/astral-sh/uv/blob/e176e17144fb6e4ec010f56a7c8fa098b66ba80b/docs/pip/compatibility.md), which, while better than nothing, is an admission that the marketing bumf and the reality on the ground are farther apart than I'd prefer: I recall trying `uv`

on my existing work project and it blew up immediately, and that certainly did not endear me to the tool.

The `pip`

+`setuptools`

+`venv`

stack is community maintained, battle tested, covers all the weird nonsense i have to handle daily, and is slower than `uv`

. 3 out of 4 ain't bad. `Pipenv`

, `poetry`

, and now `uv`

are and were useful experiments that pushed the packaging ecosystem forward; none of them are, for me, worth moving /to/; they are useful experiments to learn from and potentially adopt features from.

The other half of why i avoided astral products is that I am broadly unimpressed with tools for language A that are written in language B by people outside A-language's in-group, particularly when they're presented as "One Big Tool That Solves All Your Five-Tool Problems ... But Faster"!

Separate from everything else, it's worth noting that this isn't true: multiple maintainers of uv, including myself, have put years of both hobby and professional labor into PyPA tooling. I *still* maintain a signifiant stack of "official" PyPA tooling, including libraries (outside of PyPA) that underpin pip.

The actual relationship between PyPA and alternative tooling is significantly less adversarial than you've presented, and I think framing it as such does a disservice to the community.

(Edit: it should also go without saying that people *outside* of uv's development group are also historically embedded into Python development, PEP writing, etc.)

Thanks for your hard work! I use your work all the time and I'm thankful. Thanks for letting me be lazy around python packaging stuff, and spend my time doing other things!

uv is a great tool and makes my life easier. I'm glad you found a way to get paid writing uv and friends. I hope OpenAI corporate doesn't force breakage into uv, but if/when it does, because of the licensing, we can fork when the time comes.

Thanks again!

Thank you for the kind words. It's impossible to predict the future, but I think the open source nature of the tooling ensures that Astral's contributions to Python packaging/linting/typing/etc. will continue to benefit the community regardless of any outcome.

I agree that enshittification of uv has a pretty high chance of happening now, but I'm not very worried about it. uv is license Apache 2.0 or MIT at our option, so whenever it does occur, someone is basically guaranteed to fork it into `openuv`

or something, and continue on without the junk. If in the off chance someone doesn't do that before I notice and care, I'll do it for myself.

Hopefully OpenAI will restrain themselves from ruining uv anytime soon, but alas, we can't always have nice things.

uv is a way better tool than pip in all cases I've used it.

Moving from `uv`

to `openuv`

(or whatever it ends up being called) is not a big deal.

The other reasons I have no comments on, those things are not my concern.

someone is basically guaranteed to fork it into openuv or something

I really hope it's gonna be called something like `sunscreen`

in that case

How about `spf`

instead?

Thanks for volunteering to name all future projects! :) haha.

This is a way better name than openuv! I love it!

Licensing isn't the only kind of enshittification. Pressure to dogfood seems like the more inevitable risk, given their new owners. Not that the ensloppification hadn't already started before the deal, either...

For sure, I wasn't talking about licensing being the problem, I'm saying because they are licensed the way they are, we can fork without trouble whenever someone gets fed up enough from whatever OpenAI ends up doing with uv.

Perhaps we will get lucky and the people behind uv will manage to keep it like it is. I'm not willing to bet on that outcome, however.

Agreed. Ruff, uv, (and to an extent ty) are already mature. I saw this happening as well, but they are close to done and could survive now with light maintenance for years if not decades.

Unlike others I didn't care about the speed much, pip has been regularly breaking things and introducing obvious bugs. Then refusing to fix them with, "we're volunteers." Well, you had time to break them. e.g. [https://github.com/pypa/packaging/issues/774](https://github.com/pypa/packaging/issues/774)

someone is basically guaranteed to fork it into openuv or something, and continue on without the junk

Mad respect for Someone, but they're gonna burn out one of these days.

[Comment removed by author]

The other half of why i avoided astral products is that I am broadly unimpressed with tools for language A that are written in language B by people outside A-language's in-group

I have spent several years where my primary job was writing python tooling, both in python and in rust. I originally did share your view that language tools were best written in the same language to develop an ecosystem that drew on the same community the language's library ecosystem did, but as an ocaml fan i also had the conflicting notion that ML languages were really good at language tooling in general and that we should be exploring that more. when rust burst on to the scene with both a strong ML heritage and actually mainstream popularity, and particularly when first javascript and later python tooling in rust showed the world how much of a difference pure speed made, I have become a convert to "write your tooling in rust and develop a parallel ecosystem of libraries to do it in". not every language has "write fast code manipulation tools" as one of its strengths, and it doesn't need to.

Acquisition by OpenAI was a worse outcome than expected, but I expected something like it.

Playing the OpenAI advocate: maybe this isn't actually bad news, because that company has costs that are so large that they cannot possibly be expect to be making a relevant amount of money from `uv`

directly. If Oracle had bought `uv`

I would be worried that they would try to tie it to support subscriptions or whatever. OpenAI is bleeding billions so it needs a *much* stronger revenue source from a highly-differentiating product. So they may argue that they are incentivized to keep `uv`

(or whatever developer-tooling products they have) as pleasant and attractive as possible for users, and play well with the rest of their tech stack that actually makes revenue. And their non-personnel costs are so large that they may be more willing than others to hire teams to work on these non-business-central tools, if only for the goodwill and brand recognition.

(This is assuming that "machine-assisted programming" remains a strong market for them. If they decide that they want to focus on disrupting (pun intended) other businesses they could stop caring about developer tools.)

As you say, it's still very unclear how OpenAI will make money. Which makes any statement saying uv will be a loss-leader to be on very unstable grounds. Someone like Google can (and does) burn money on side projects because it's a tiny tiny fraction of their profits. But if OpenAi's profit margins are thin you only need management to look at what uv costs and decide to make "savings" once.

One thing I've learned from my years in tech is that you cannot rely on large companies to consistently act in their best long term self interest all the time. Eventually, for whatever reason, they're going to prioritise their short-term finances.

The other half of why i avoided astral products is that I am broadly unimpressed with tools for language A that are written in language B by people outside A-language's in-group

This doesn't track for me. Python has always been a glue language for bindings on top of C, Fortran, etc. Pretty much anything useful you do in Python nowadays is actually happening in C - but increasingly Rust. I have a feeling this is less about tools for language A written in B and more that some people aren't fans of ~~Rust~~ language B.

what? are you a python user? there are certainly some performance intensive AND popular python libraries built on top of C or Rust, but

Pretty much anything useful you do in Python nowadays is actually happening in C - but increasingly Rust.

seems entirely divorced from reality. most things you do in Python are, as the name implies, in Python, unless you have some perverse understanding that using CPython means you are “actually” using C, or that using uv for your Python project means you are “actually” using Rust—ditto for dependencies with components implemented in other languages (not like other languages don’t use C under the hood for some things…)

people who don’t want to use Rust tooling for Python generally don’t do so out of some Luddite fear of Rust itself, they care about being able to extend their tools in the language they know and use. the Rust and Python communities, as far as i can tell, are very close: PyO3’s widespread success points to that. but that doesn’t mean there aren’t still cases where choosing Python tooling makes sense.

Numpy (C) SciPy (C++) PyTorch (C) are just the basic examples. Heck even packages like ujson (c/++?) So I’m not sure what kind of Python you are writing, but I would hazard a guess that most new Python projects these days are using it as it always meant to be: a glue language. There’s probably exceptions around light scripting and web stuff (uwsgi: C btw) but even there packages like Pydantic (Rust) and cryptography (Rust) are doing some heavy lifting.

I stand by being a language purist in the Python ecosystem is just silly unless you are just unaware of the actual language many of the libraries are implemented in.

I am not arguing for language “purism;” I’m saying that your assertion that Python is “actually” mostly C or Rust is missing the point, and is not an observation unique to Python.

PyTorch is mostly C++/CUDA outside of the Python, but this view misses that there are real features that are Python-only here, like its [autodiff engine](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html). I tried using Rust with libtorch only (via [tch-rs](https://github.com/LaurentMazare/tch-rs)) to avoid said 'glue language', only to be met with this fact which I solved by [having my Rust generate the required Python](https://github.com/phase/astral-dunes/commit/38394eb6b74f8d1a649cf01f43054c80623ec4ff).

This to me makes it very much not a glue language, different authors are using different parts of the Python+C++ space to implement their ideas. Not to mention all of the *usages* of PyTorch which are mostly Python and most certainly not "glue" (everything surrounding those algorithms could be considered the "glue" to get it working on real hardware!).

Regardless of how PyTorch is coded, I'm not using the term "glue language" as derogatory and it's not even my words. This essay called [Glue It All Together With Python](https://www.python.org/doc/essays/omg-darpa-mcc-position/) is written by Guido van Rossum himself, where he describes the at the time very new language as "...an advanced scripting language that is being used successfully to glue together large software components." He also goes on to say that "The best approach is often to write only the performance-critical parts of the application in C++ or Java, and use Python for all higher-level control and customization."

This isn't any less true today than it was in the 90s.

That's why I find OP's argument so strange. GVR himself introduced Python as a language most useful paired with other languages. Having an issue with the tooling being written in Rust is strange. The argument may be more about tooling than libraries, but I fail to see the distinction. UV can be pip-installed just like any library. How many people contribute back to pip or setuptools? Very few, I'd imagine - and I don't think it's the language that is making the difference.

I also really like how uv manages the python version for you. How would you normally tackle that in the pip+setuptools+venv case? Rely on another package manager or something else? (Genuine question)

Astral seems to have absorbed [https://github.com/astral-sh/python-build-standalone](https://github.com/astral-sh/python-build-standalone), which provides the Python binary distributions that are the "important" part of the trick. You really can use those with any other tool. I believe rye (absorbed by Astral // the rye maintainer decided that uv was the way to go) also used the same builds.

(IMHO in general you should support a couple of Python versions; using the standalone builds is convenient and fast, but it's nice to make it easy for people to run stuff using whatever Python they have on their system. You pick which LTS distributions are reasonable to support (e.g. RHEL 9, Debian 13 and Ubuntu 24.04- just a random pick) and test everything on the oldest Python release in those.)

pipenv

The pip+setuptools+venv stack is community maintained, battle tested

I've been using that stack for 10 years until uv came along and it has **never** felt "battle tested". It is hack on top of hack that had to support all the way back to when we just ran arbitrary code to declare packages via `setup.py`

and even older.

very minor but, fwiw, i read the “knee jerk” part that way as well, at first. rereading it, it seems to be saying “my own knee jerk guess as to why…”

financing model guarantees a tool that will enshittify somehow,

I really don't think it's going to be a problem. Not in the financial way anyway. OpenAI is operating at a level where any income from the python tooling wouldn't matter. Realistically they get billions of dollars of funding, and extracting any kind of meaningful value from uv in that case is just extremely unlikely.

so the conclusions presented seem to boil down to:

to the first point: people may be cautious to use VC/OpenAI backed tools because they don’t know if they can trust them any longer—monetization strategies, enshittification, advertising; dev tools are not immune to these things in 2026. i’m not saying there is positive evidence this will happen to `uv`

, but i disagree with the conjecture that speed of development is the main issue people are likely to have with this.

to point two: wild conclusion! golly, i sure HOPE we aren’t at the point where LLM recommendations are the the top of the funnel determinant for what tools are being used in open source… but i guess the prevalence of vibe coded or pure slop projects on code forges and package repos is probably changing the dynamics for this specifically.

i think OP has missed a TON of context here, particularly around the history of python tooling written in python. i don’t have links handy, but i think many words have been spent on lobsters alone debating the merits of Python-tooling-in-Rust vs -in-Python.

author goes on to say this isn’t an issue because the speed of development hasn’t slowed down

Development speed is somewhere near the bottom of the list of things I want in my bedrock project infrastructure.

OP here.

For the first point, it is not about speed of development, but speed of adoption by public repos. uv was/is being adopted faster than poetry for new repos. This indicates either that people don't care that it is venture backed, or that venture backed marketing dollars work, or that uv is superior to poetry. Probably all three, but I used it as an argument for people not caring about vc backing. The second part is that the ratio of new repos using uv did not change between 2025 and 2026. This is not a strong argument unfortunately because OpenAI acquisition is so new; we will see what happens.

For the second point, I looked at top 10 most starred repos created in 2026 that were Python. 8 were slop to my eye. Of non-slop, 1 used uv and 1 used pip. So I do think that LLM recommendations are driving tool usage. Don't have any opinions on what is driving popularity of slop.

You are right on the missing context on history of python tooling in python. I have opinions on this and I didn't want to share them in this blog post because they are out of scope. Will consider writing one in the future.

contradicting anecdata - I've done one greenfields Python project with a coding agent so far (Claude), and in that single case it chose uv, not pip. Just one data point though.

Eh, I don’t think you need to reach for venture/OpenAI to explain the adoption rate. Package management using pip has been around a long time, is distributed as part of the core language, and is referred to as the preferred tool in the [language docs](https://docs.python.org/3/installing/index.html). Approximately every large org using Python has projects using pip and requirements.txt, may have reusable CI scripts built around that pattern, and likely has little appetite for converting all those projects to a new tool.

Add to that that most developers (perhaps especially Python developers) are just… not very online? A lot of the Python ecosystem is in scientific/ML circles where Anaconda is more-or-less fully entrenched, and they’re not spending a lot of time following the rest of the ecosystem. I’m not surprised that uv surpassed poetry, because a lot of the Python ecosystem also didn’t pay much attention to that project either.

The software industry is plagued with religious cargo cult. Sadly, most engineers and people in tech do things as they say someone doing rather than because they understand why it's done in a certain way.

"We have use pip for a long time and we know how it works. Let's not change that". I heard this in a project where built times of 7 minutes. Most of which pip install.

I think there's a much simpler explanation: people use what they already know. Widespread adoption of anything new across an entire industry takes far longer than people intuit. I often run into recently written Python that only makes use of features that were present in Python 2 (and encountered this before AI-assisted development was commonplace). I suspect if we could compare the adoption rate of uv to other Python packaging tooling, it'd be far above average.

traditional shout out: try PDM. it's awesome (and it can use `uv`

as the backend, but can work without it as well) [https://pdm-project.org/](https://pdm-project.org/)

This looks nice. Do you think it's ready as a standard replacement for uv? It doesn't have to be drop-in but either stability or robustness is a minimum.

I used it before uv and it was already good :-) just not as fast as uv

I don't use uv yet ... because I don't know it. I am not in the habit of regularly creating Python projects, pip and venv do the job just fine for me. If people (or LLMs I guess) had strongly recommended uv to me I would have tried it.

That's fair, but I strongly recommend you try uv. Even if you don't want to use it for packaging for some reason, the PEP 723 script dependency resolution itself is fantastic, here's an example from my own repo: [https://forge.eblu.me/eblume/blumeops/src/commit/40556e5a2de7e5f92d5afe2ffddfa4c5b6909cd0/mise-tasks/container-build-and-release#L1-L5](https://forge.eblu.me/eblume/blumeops/src/commit/40556e5a2de7e5f92d5afe2ffddfa4c5b6909cd0/mise-tasks/container-build-and-release#L1-L5)

(Note that the `#MISE`

/`#USAGE`

lines that follow the PEP 723 block are unrelated, they come from a quirk of how mise (mise.jdx.dev) interacts with the click CLI arg parseing.)

I believe you can get this in a couple of other places already. (IIRC, pipx?)

Thank you. I tried it on a throw-away script and it is genuinely pleasant to use, will continue using it.

I used to quote and link [Why Not Tell People to Simply Use](https://www.bitecode.dev/p/why-not-tell-people-to-simply-use) because of workflow complexities, nuance and other things. And then they updated the article to say "just use uv". *sound of piano hitting pavement*

Besides zero trust towards VC-baked softrware, I'm more concerned about it being hype-driven, similarly to Bun (acquired by Anthropic). Learned my lesson from Lunatic (Erlang-style runtime for WASM) on top of which I've created a product, and shortly before the release, it became unmaintained without any prior signals or announcements - forcing me to maintain unfamiliar code that happened to be very complex, and impossible to continue as a single person.

given the recent aquisition by openai, i have to pause my uv adoption.

love the tool but the future of uv is questionable now.

As someone who only recently picked up python at work, dealing with a variety of legacy projects, uv is the only thing that made any damn sense to me, so hearing that the python community itself is not really getting behind it bums me out. Managing python dependencies is a special kind of hell that every new python dev gets hazed into.

Anyway, if it’s owned by an ai company, I reckon its models will prefer it, which is also an f’ed up aspect of ai influence that one company might be able to lend weight to arbitrary solutions. What a mess

Managing python dependencies is a special kind of hell that every new python dev gets hazed into.

I wish it were just Python but it's fundamental. I've had it with Perl and Ruby when you need multiple interpreter versions and the matching project dependencies some of which have deps that link to particular native library versions. So over time across different projects you end up laying your hands on cpan, cpanplus, maybe cpanminus or cpm, rbenv, rvm, direnv, asdf, etc. etc. Let's not forget sdkman for things Java. So you throw your hands up and reach for vms, containers, guix, nix, etc. but like jwz's regex joke, now you have two problems.

About a decade ago for work me and a couple of other seniors agreed on what to use for projects and I wrote a bunch of ansible tasks so that a day one a new hire could have a working environment on their laptop with the same selected subset of tools everyone else was using.

You got me there. I agree, it’s not a single-language problem.

Here, I think I went a bit aggro because I have to wrestle with multiple python projects of varying levels of quality/maturity with different dependency management tool assumptions and uv is the only tool that worked across them all and made sense to me. Here it’s seeming to be discarded as “pip and venv and setuptools etc” is fine, and that was not my experience. This is the perspective of someone not experienced in Python (me), so take that either with a grain of salt or an indication of what is being taken for granted that uv solves.

edit: also a bit aggro as I am writing this during a painful hospital stay. I probably shouldn’t have posted at all

I didn't find it aggro, though maybe that's just scar tissue, we're all living with the same frustrations 😂

I hope you have a smooth recovery. Be well.

hearing that the python community itself is not really getting behind it bums me out.

I'd say it's the opposite. The Python community largely has gotten behind `uv`

and only has hesitation because of the openai acquisition.

Since I found poetry and pipx, I really haven't had many problems managing Python projects.

I like uv because yes, that it's faster has an important user-facing benefit: it's reasonable to check that the virtualenv is *always* up to date, eliminating all the pain from forgetting to update it. (That is not a huge pain, but it's annoying.)

However, it sours me greatly that uv is owned by a company I don't want to associate myself with in any way. An old project of mine just produced a security advisory because it uses Black, and I'm not in a happy place because a) I feel bad to use a vulnerable dependency, even if it's unexploitable b) I'm lazy to deal with updating Black, because in this project IIRC it's not straightforward to update and most importantly c) although I'm already using Astral projects in many places, it feels dirty now to extend that.

I wish someone (I don't feel terrible associating with) forks or clones Astral stuff *as soon as possible*. Because I do not enjoy mustering the energy to downgrade to using something else, even if there are plenty of acceptable alternatives. (Funnily enough, some of those acceptable alternatives are also by groups I'm not a fan of either- but nothing close to my dislike of the new Astral owners.)

I thought this is about libuv

Just started using uv the other day. TIL that it's not an open source tool (silly me for not doing my homework). I won't be using it anymore. Just been the downstream payee of enshitification too many times.

It is open source: [https://github.com/astral-sh/uv/blob/main/LICENSE-MIT](https://github.com/astral-sh/uv/blob/main/LICENSE-MIT)

That’s not true. uv, as any other library they built, is open source with a permissive license.

Nice timing. I took up uv using last week for a personal project because I wanted to see how it is. It seemed good, it's different than having multiple tools but not worse.

I like ‘micromamba’. Single portable executable. Pretty fast and handles multiple environments easily and efficiently.

Using ‘conda forge’ is probably the easiest way to get MKL accelerated NumPy and SciPy. What disadvantages do you find in it?

What disadvantages do you find in it?

Pulling in the world because you're using conda.

[Comment removed by author]

I know this only looks at popular projects but I bet 100% of my python projects have (unchanged) `requirement.txt`

in the repo and I've used them with `uv`

for 1-2 years.

So I guess unless it's a) high-profile and b) frequently/recently released - there might be a huge discrepancy between "documented/recommended use" and "it works".