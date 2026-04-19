[Back to Blog](https://www.dbpro.app/blog)

# Do You Even Need a Database?

![Jay](/_next/image?url=%2Fheadshot-jay.webp&w=64&q=75)

A database is just files. SQLite is a single file on disk. PostgreSQL is a directory of files with a process sitting in front of them. Every database you have ever used reads and writes to the filesystem, exactly like your code does when it calls `open()`

.

So the question is not whether to use files. You're always using files. The question is whether to use a database's files or your own. And for a lot of applications, especially early-stage ones, the answer might be: your own.

Now, obviously we love databases. We're building [DB Pro](https://dbpro.app), a database client for Mac, Windows, and Linux. But the honest answer to "do you need one?" depends on your scale, and most applications are smaller than people assume. We tested this. We built the same HTTP server in Go, Bun, and Rust, using two storage strategies, and hammered them with wrk. Here's what the numbers look like.

## The setup

Three flat files: `users.jsonl`

, `products.jsonl`

, `orders.jsonl`

. The format is newline-delimited JSON (JSONL): one record per line, appended on write. Each file holds one entity type.

Two HTTP endpoints: `POST /users`

to create, `GET /users/:id`

to fetch by ID. We benchmarked the GET path. Reads are where the strategies diverge.

## Approach 1: Read the file every time

The simplest thing you can do: when a request comes in for user `abc-123`

, open the file, scan every line, parse each one as JSON, check the ID. Return when you find a match.

**Go:**

**TypeScript (Bun):**

**Rust:**

This is O(n). Every request reads the entire file from top to bottom, on average scanning half of it before finding the target. The larger the file, the slower every request gets.

## Approach 2: Load it into memory

On startup, read the entire file once and store every record in a hash map keyed by ID. Writes go to both the map and the file. Reads are a single map lookup.

The file is the durable backing store. The map is the index. If the process restarts, reload from the file.

**Go:**

**TypeScript (Bun):**

**Rust:**

Read path is now O(1) at any scale. The `sync.RWMutex`

in Go and `RwLock`

in Rust let multiple readers proceed in parallel, so concurrent requests don't block each other.

## Approach 3: Binary search on disk

What if you need reads that don't load everything into RAM, but also don't scan the whole file? The middle ground: sort the data file by ID, build a fixed-width index alongside it, and binary search the index using `ReadAt`

. Each lookup does O(log n) seeks (about 20 for 1M records), then reads exactly one record from the data file.

The index format is simple: one line per record, exactly 58 bytes: `<36-char UUID>:<20-digit byte offset in data file>\n`

. Fixed width means you can jump to any entry with a single `ReadAt(buf, entryIndex * 58)`

.

The data file must be sorted by ID before building the index. We sort once at seed time, or as a one-time migration step on an existing JSONL file. Appending new records breaks the sort, so in a real system you'd rebuild the index periodically or keep an unsorted write-ahead buffer and merge it in. That merge pattern is what an LSM-tree does.

## The benchmark

We seeded three datasets (10k, 100k, and 1M records) and used [wrk](https://github.com/wg/wrk) to run 10 seconds of load against each server: 4 threads, 50 concurrent connections, random GET requests picking from a sampled list of real IDs.

All servers ran on the same machine (Apple M1 Mac mini, macOS 15). Go 1.26, Bun 1.3, Rust 1.94 (release build).

We also tested two more approaches in Go: a binary search against a sorted file on disk, and SQLite using `modernc.org/sqlite`

(pure Go, no CGO). The binary search uses a fixed-width index file (58 bytes per entry: `<uuid>:<offset>`

) to do O(log n) `ReadAt`

calls, then seeks directly to the matching record. No data loaded into RAM.

## The results

**Requests per second (higher is better)**

| 10k records | 100k records | 1M records | |
|---|---|---|---|
| 783 | 85 | 23 | |
| 45,742 | 41,661 | 38,866 | |
![]() | 26,000 | 25,507 | 25,085 |
| 97,040 | 98,277 | 97,829 | |
| 469 | 61 | 19 | |
| 106,064 | 107,058 | 105,367 | |
| 2,883 | 251 | 52 | |
| 163,687 | 155,364 | 169,106 |

**Average latency per request (lower is better)**

| 10k records | 100k records | 1M records | |
|---|---|---|---|
| 84ms | 552ms | 1,010ms | |
| 1.2ms | 1.4ms | 1.4ms | |
![]() | 2.0ms | 2.0ms | 2.1ms |
| 497µs | 571µs | 584µs | |
| 101ms | 754ms | 1,060ms | |
| 449µs | 443µs | 463µs | |
| 17ms | 195ms | 753ms | |
| 231µs | 482µs | 221µs |

A few things worth pointing out.

**Linear scan degrades linearly.** At 1M records, Go is serving 23 requests per second and each Bun request takes over a second on average. At that point you're not tuning performance, you're explaining to users why the page won't load.

**Binary search on disk is fast and flat.** 45k req/s at 10k records, 38k req/s at 1M records. That's only a 15% drop as the dataset grows 100x. The OS page cache does a lot of work here: after a warmup period, the 566KB index file for 10k records fits entirely in cache. For 1M records the index is ~55MB, but the top levels of the binary search always hit the same offsets near the middle of the file, so those pages stay hot regardless of which key you're looking up. Each lookup does ~20 `ReadAt`

calls on the index plus one `Seek`

into the data file.

**Binary search beats SQLite.** This was unexpected. Plain sorted files with a hand-rolled index outperform SQLite's B-tree by about 1.7x at every scale. SQLite does more work per lookup than a hand-rolled binary search, even for a simple primary key read. That overhead is worth it when you need the features. For a pure ID lookup, you're paying for machinery you're not using.

**SQLite is fast and consistent.** 25,000 to 26,000 req/s regardless of dataset size, with 2ms average latency. The B-tree index means lookup time barely changes as records grow from 10k to 1M.

**In-memory map is the ceiling.** 97k req/s with sub-millisecond latency at every scale. If your dataset fits in RAM, nothing on disk will match it.

**Bun (JavaScript) beats Go on the map approach.** Bun's HTTP server averages around 106k req/s vs Go's 97k. Bun uses JavaScriptCore as its JS engine and implements its HTTP layer natively in Zig via uWebSockets, bypassing libuv entirely. The language matters less than the runtime.

**Rust wins on linear scan by a wide margin.** At 10k records, Rust does 2,883 req/s vs Go's 783 and Bun's 469. That's 3-6x faster for the naive file scan, likely a combination of lower I/O overhead and faster JSON deserialization via serde. For the map approach, Rust leads but the gap narrows considerably.

**Pick by use case:**

| Use case | Winner |
|---|---|
| Absolute fastest throughput | |
| Fastest without loading everything into RAM | |
| Need SQL queries later | ![]() |
| Quickest to ship |

## What does 25,000 requests per second actually mean?

Before we talk about when you need a database, let's put these numbers in context. Because "25,000 requests per second" sounds like a lot, and it is, but it helps to think about what kind of product generates that kind of load.

Traffic is not uniform. Users are awake during the day and asleep at night. Capacity planning guides for web applications generally assume a peak-to-average ratio of around 1.5 to 2.0 for B2B and B2C products ([ByteByteGo](https://blog.bytebytego.com/p/capacity-planning), [Geek Culture](https://medium.com/geekculture/estimating-peak-web-traffic-for-e-commerce-websites-25b7368c2051)). Let's use 2:1, which means a product averaging 12,500 req/s across the day might spike to 25,000 req/s during its busiest hour.

Now work backwards. Let's assume an active user triggers around 10 database lookups per hour — loading their profile, fetching their data, that kind of thing. That's a rough number; your app might be higher or lower. Let's also assume 10% of your daily active users are online at the same time during peak.

Peak req/s = DAU × 0.10 × (10 lookups/hr ÷ 3600 sec/hr) = **DAU × 0.000278**

Flip it around to find the DAU that saturates each approach:

| Approach | Peak capacity | DAU to saturate it |
|---|---|---|
| 783 req/s | 2.8M users | |
| 40,000 req/s | 144M users | |
![]() | 25,000 req/s | 90M users |
| 97,000 req/s | 349M users | |
| 106,000 req/s | 381M users | |
| 169,000 req/s | 608M users |

The linear scan breaks at a real product scale: around 3 million daily active users with a 10k record file. That's a meaningful number.

Everything else? You would need tens of millions of daily active users to push these approaches hard. Instagram was at 400 million daily active users and still running PostgreSQL as their primary data store ([Instagram Engineering](https://instagram-engineering.com/handling-growth-with-postgres-5-tips-from-instagram-d5d7e7ffdfcb)). Most products never get there.

To give a more grounded example: a SaaS with 10,000 paying customers where each customer uses the app once a day generates around 3 req/s peak under these assumptions. A consumer app with 100,000 DAU generates around 30 req/s at peak under these assumptions. Neither comes close to any of the approaches we tested.

The honest answer to "do you need a database?" is: probably not yet. And when you do, SQLite running from a flat file handles 90 million daily active users on a single server.

## When do you actually need a database?

For lookup by ID: the in-memory map handles ~97k req/s, binary search on disk handles ~40k req/s, and SQLite handles ~25k req/s. All three are well above what most applications will ever see from a single server.

The cases where you'll outgrow flat files:

**Your dataset doesn't fit in RAM.** The in-memory map approach requires loading everything at startup. At a few million small records that's fine. At tens of millions, you're looking at gigabytes of RAM just for the index. You need a way to page data in and out. A database does this for you.

**You need to query by more than one field.** Right now, the only fast operation is "find by ID." If you need "find all orders for user X" or "find all products with price under $50," you'd need to scan the file or maintain additional maps. Once you have three or four of those, you've built a query engine.

**You need joins.** Combining orders with users and products in a single response means loading from three files and assembling the result in application code. SQL does this more efficiently.

**Multiple processes need to write at the same time.** The `RwLock`

in these servers protects concurrent access within one process. As soon as you run two instances of the server, both with their own in-memory map, they diverge. You need an external source of truth. That's what a database is.

**You need atomic writes across entities.** Creating an order while decrementing inventory needs to either both succeed or both fail. With separate files, you'd have to implement a transaction log yourself. Databases solve this with ACID guarantees.

None of these constraints apply to a lot of applications. Plenty of internal tools, side projects, and early-stage products will never have a dataset that doesn't fit in a single server's RAM, never need to join across tables under heavy load, and never run more than one instance. For those applications, this approach works.

The file is still there if you need to migrate later. JSONL is trivially importable into any database. You're not locked in.

![](/_next/image?url=%2Ficon.webp&w=64&q=75)

### Work With Your Databases

### Like A Pro

Query, explore, and manage your databases with a beautiful desktop app, collaborative web platform, and built-in AI.

[Download Now](https://www.dbpro.app/download)

![DB Pro Dashboard](/_next/image?url=%2Fdashboard-hero.webp&w=3840&q=75)

The server code for all three languages is embedded above. The seed script, benchmark runner, and wrk Lua script aren't shown inline — download the full project to run it yourself:

[Download the benchmark code (.zip)](https://www.dbpro.app/do-you-even-need-a-database.zip)

The zip contains `go-server/`

, `bun-server/`

, `rust-server/`

, `seed.ts`

, and `run_bench.sh`

. The benchmark script seeds data at three scales, generates a Lua script with sampled real IDs, starts each server, runs wrk, and tears it down.

Quick start:

## Keep Reading

### DB Pro Now Supports Val Town

DB Pro now connects to Val Town's SQLite databases. Browse tables, run queries, and manage your data with a proper desktop client.

### Best Client Database Software for Small Business in 2026

A practical guide to client database software for small businesses. Covers free and paid options, from simple spreadsheets to full CRMs.

### DB Pro v1.3.0: Database Creation, Multi-Query Editor & PlanetScale Vitess

Create databases directly from the sidebar, execute multiple queries at once, and connect to PlanetScale Vitess.