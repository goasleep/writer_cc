# Python gets a new governance model

Ready to give LWN a try?With a subscription to LWN, you can stay current with what is happening in the Linux and free-software community and take advantage of subscriber-only site features. We are pleased to offer you

, no credit card required, so that you can see for yourself. Please, join us![a free trial subscription]

Back in late October, when we [looked in](https://lwn.net/Articles/769178/) on
the Python
governance question, which came about due to the [resignation of Guido van Rossum](https://lwn.net/Articles/759654/), things seemed
to be mostly set for a vote in late November. There were six Python
Enhancement Proposals (PEPs) under consideration that would be ranked by
voters in a two-week period ending December 1; [instant-runoff
voting](https://en.wikipedia.org/wiki/Instant-runoff_voting) would be used to determine the winner. In the interim, though,
much of that changed; the voting period, winner-determination mechanism,
and number of PEPs under consideration are all different. But the voting
concluded on December 16 and a [winner
has been declared](https://discuss.python.org/t/python-governance-vote-december-2018-results/546); [PEP 8016](https://www.python.org/dev/peps/pep-8016/) ("The
Steering Council Model"), which was added to the mix in early November, came
out on top.

Right around the time of our previous article, a [new
thread](https://discuss.python.org/t/python-governance-electoral-system/290) was started on the [Python committers Discourse instance](https://discuss.python.org/c/committers) to discuss the pros and cons of various voting
systems. Instant-runoff voting fell out of favor; there were concerns that
it didn't truly represent the will of the electorate, as [seen](https://en.wikipedia.org/wiki/Instant-runoff_voting#2009_Burlington_mayoral_election)
in a Burlington, Vermont mayoral election in 2009, for example.
The fact that it was put
in place by fiat under a self-imposed deadline based on in-person
conversations at the core developer sprint,
rather than being hashed out on the [Discourse instance](https://discuss.python.org/) or the [python-committers
mailing list](https://mail.python.org/mailman/listinfo/python-committers) may have also been a factor. As Nathaniel J. Smith [put
it](https://discuss.python.org/t/python-governance-electoral-system/290/21):

*looks*like we can work together, make decisions, and hold a legitimate vote, that they're undermining our ability to

*actually*work together, make decisions, or hold a legitimate vote.

Donald Stufft put together a [lengthy
summary](https://discuss.python.org/t/python-governance-electoral-system/290/40) of many of the different voting systems along with their good
and bad attributes. No one had any interest in using "[plurality voting](https://en.wikipedia.org/wiki/Plurality_voting)"
(also known as "first past the post"), but opinions differed on other
possibilities. Eventually, [PEP 8001](https://www.python.org/dev/peps/pep-8001/) ("Python
Governance Voting Process") was changed to use the [Condorcet method](https://en.wikipedia.org/wiki/Condorcet_method)
to determine the winner. A tie or cycle, which are both possible—though
unlikely—under the Condorcet method, would result in a re-vote among the
tied options. Condorcet has been used by Debian and other projects for
many years, which is part of the reason consensus formed around that method.

#### The winner

In the end, Condorcet led to an election where the results were clear
without any real ambiguity about them. As Tim
Peters, who was one of the more active developers in the voting-methodology
discussion, [noted](https://discuss.python.org/t/python-governance-vote-december-2018-results/546/9):
"Not only was there a flat-out Condorcet ('beats all') winner, but if
we throw that winner out, there's also a flat-out Condorcet winner among
the 7 remaining - and so on, all the way down to 'further
discussion'.

" Given that the pool of voters was fairly small, 94, and
that only 62 people actually voted, there could have been some far messier
outcomes.

It is perhaps not surprising that a late entrant into the election was the clear winner. Smith and Stufft authored the PEP; it likely benefited from the discussion of the other PEPs and the changes that were made to them along the way. It also doesn't hurt that it is explicitly intended to be boring, simple, and flexible.

As with most of the other proposals, PEP 8016 creates a council. Various
sizes were proposed in the other PEPs, but the steering council of PEP
8016 consists
of five people elected by the core team. The [definition](https://www.python.org/dev/peps/pep-8016/#membership)
of the core team is somewhat different than today's core developers or
committers. The PEP explicitly states that roles other than "developer" could
qualify for the core team. Becoming a member of the team simply requires a
two-thirds majority vote of the existing members—and no veto by the
steering council.

The veto is not well specified in the PEP and was the subject of a [question](https://discuss.python.org/t/pep-8016-the-steering-council-model/394/34)
during the discussion process. [According
to Smith](https://discuss.python.org/t/pep-8016-the-steering-council-model/394/35), that idea came from the [Django
governance document](https://docs.djangoproject.com/en/dev/internals/organization/), which was a major influence on the PEP. It is
hoped that it would never have to be used, "but there are situations
when the alternatives are even worse

". There is also an escape hatch if
it turns out that a core team member needs to be removed; a super-majority
of four council members can vote to do so.

#### The steering council

The council is imbued with "broad authority to make decisions about
the project

", but the goal is that it uses that authority rarely; it
is meant to delegate its authority broadly.
The PEP says that the council should seek consensus, rather than
dictate, and that it should define a standard PEP decision-making process
that will (hopefully) rarely need council votes to resolve. It is,
however, the "court of final appeal

" for decisions affecting
the language. But the council cannot change the governance PEP; that can
only happen via a two-thirds vote of the core team.

The mandate for the council is focused on things like the quality and
stability of Python and the CPython implementation, as well as ensuring
that contributing to the project is easy so that contributions will
continue to flow into it. Beyond that, maintaining the relationship
between the core team and the [Python
Software Foundation](https://www.python.org/psf/) (PSF) is another piece of the puzzle.

Steering council members will serve for the length of single Python feature
release; after each release, a new council will be elected. Candidates must
be nominated by a core team member; "[approval voting](https://en.wikipedia.org/wiki/Approval_voting)"
will be used to choose the new council. Each core team member can
anonymously vote for zero to five of the candidates; the five with the
highest total number of votes will serve on the new council, with ties
decided by agreement between the tied candidates or by random choice.

There are some conflict-of-interest rules as well: "While we trust
council members to act in the best interests of Python rather than
themselves or their employers, the mere appearance of any one company
dominating Python development could itself be harmful and erode
trust.

" So no more than two council members can be from the same
company; if a third person from the company is elected, they are
disqualified and the next highest vote-getter moves up. If the situation
arises during the council's term (e.g. a change in employer or an
acquisition), enough council members must resign to ensure this makeup.
Vacancies on the council (for this or any other reason) will be filled
by a vote of the council.

In the event of core team dissatisfaction with the council, a no-confidence vote can be held. A member of the core team can call for such a vote; if any other member seconds the call, a vote is held. The vote can either target a single member of the council or the council as a whole. If two-thirds of the core team votes for no confidence, the councilperson or council is removed. In the latter case, a new council election is immediately triggered.

Some of the other PEPs specified things such as how PEPs would
be decided upon
or placed various restrictions on who could serve on the council. Victor
Stinner's [summary](https://discuss.python.org/t/comparison-of-the-7-governance-peps/392)
of the seven proposals gives a nice overview of the commonalities and
differences between them. Many were fairly similar at a high level, most
obviously
varying on the size of the council, though there are other substantive
differences, of course.
[PEP 8010](https://www.python.org/dev/peps/pep-8010/) ("The
Technical Leader Governance Model"), which more
or less preserved the "benevolent dictator" model, and [PEP 8012](https://www.python.org/dev/peps/pep-8012/) ("The
Community Governance Model"), which
did not have a central authority, were both something of an outlier. It is
interesting to
note that 8012 came in second in the voting, while 8010 was one of the
least favored governance options.

#### Another election

Next up is council elections. There are two phases, each of which will
last two weeks; first is a nomination period, followed by the actual
voting. Van Rossum has not ridden off into the sunset as some might have
thought; he was active in some of the threads leading up to the governance
election and was the first to [start
organizing the council election](https://discuss.python.org/t/organizing-the-council-elections/549). He asked that the process start after
the new year to give folks some time to relax over the holidays. Smith [agreed](https://discuss.python.org/t/organizing-the-council-elections/549/4),
noting that starting on January 6 would lead to the actual vote
starting January 20 and a council elected on February 3.

Overall, the process has gone fairly smoothly since Van Rossum stepped down
and the [first steps toward new governance](https://lwn.net/Articles/759756/)
were taken back in July. There would seem to be plenty of good candidates
for the council, many of whom were active in the governance discussions.
The first incarnation of the council will have lots of things to decide,
including the PEP approval process, but it won't have all that much time to
do so. Instead of the usual 18-month cycle, the council will serve an
abbreviated term until [Python 3.8 is
released](https://www.python.org/dev/peps/pep-0569/), which is currently scheduled for October 2019. The council
elected after that should have a full 18 months, unless, of course, the [release cadence is shortened](https://lwn.net/Articles/755224/). It will all be
interesting to watch play out; once again, stay tuned.

| Index entries for this article | |
|---|---|
|