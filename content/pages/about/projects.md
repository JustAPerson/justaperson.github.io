Title: Projects
Slug: about/projects

# Professional

## _Broadway Technology_, Summer 2018

At [Broadway][bway] I helped add support for trading commercial paper on their
core distributed platform by implementing logic to communicate to exchanges via
the [FIX protocol][fix]. This involved modifying one of their C++ libraries that
tracks price information about instruments, adding a new battery of tests, and
debugging many edge cases.

In addition, I helped profile and optimize a key C++ data serialization library.
This library was responsible for parsing FIX messages and embedded XML,
serializing objects from the Broadway distributed platform and application state
stored in hashtables, and finally translating between these many formats. I
wrote both synthetic and representative benchmarks using logs captured from test
files. I also used Linux's `perf` and `valgrind` commands to identify
bottlenecks and to eliminate unnecessary memory allocations.

[bway]: https://www.broadwaytechnology.com/
[cp]: https://www.investopedia.com/terms/c/commercialpaper.asp
[fix]:  https://en.wikipedia.org/wiki/Financial_Information_eXchange

## _Ab Initio_, Summer 2017

At [Ab Initio][ab] I implemented a translation pass between their existing data
flow graph representation and the format employed by their new experimental 
optimization engine. As part of this, I wrote logic to enrich the basic data
graph with additional metadata such as type propagation and liveliness analysis.

[ab]: https://www.abinitio.com/en/

## _Touchplan_, Summer 2016

At [Touchplan][tp] I helped distribute their monolithic Java/SQL backend across
multiple servers using [Apache Mesos][mesos] and [Zookeeper][zk]. I developed
and tested high availability features such as handling failovers and online
rolling upgrades.

I also developed a script to deploy to this server cluster and message
build/deployment updates to Slack as a part of their CI/CD system.

Finally, I performed basic data analytics and helped evaluate several data
warehouse solutions.

[tp]: https://www.touchplan.io/
[mesos]: https://mesos.apache.org/
[zk]: https://zookeeper.apache.org/

# Hobby
