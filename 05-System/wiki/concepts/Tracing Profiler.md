---
type: concept
name: "Tracing Profiler"
---

# Tracing Profiler

A type of profiler that records timings for every function call and return. Python's original `profile` module and `cProfile` use this approach.

## Disadvantages

- High overhead (slows down profiling)
- Per-function overhead can make oft-called functions look like bottlenecks
- Can skew results

## Related Concepts

- [[Python Profiling]]
- [[Sampling Profiler]]
- [[cProfile]]

## Sources

- [[Python introducing profiling-explorer]]
