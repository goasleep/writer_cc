---
type: concept
name: "Sampling Profiler"
---

# Sampling Profiler

A type of profiler that periodically interrupts the profiled program to record the current call stack. This approach has very low overhead, allowing programs to run at nearly full speed without the skew from per-function overhead.

## Examples

- **py-spy**: Third-party sampling profiler (requires sudo)
- **Tachyon (profiling.sampling)**: New built-in Python profiler in Python 3.15

## Advantages

- Low overhead
- No per-function overhead skew
- Can output flame graphs and heat maps

## Related Concepts

- [[Python Profiling]]
- [[Tracing Profiler]]

## Sources

- [[Python introducing profiling-explorer]]
