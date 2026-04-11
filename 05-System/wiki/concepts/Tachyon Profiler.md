---
type: concept
name: "Tachyon Profiler"
---

# Tachyon Profiler

Codename for Python's new `profiling.sampling` module, introduced in Python 3.15 (expected October 2026). It's a sampling profiler that uses periodic stack interrupts to record program state.

## Features

- Very low overhead (programs run at nearly full speed)
- No per-function overhead skew
- Compatible with pstats format
- Supports flame graphs and heat maps

## Advantages over Third-Party Tools

- Built into Python (no external dependencies)
- No sudo permissions required (unlike py-spy)
- Maintained as part of Python core

## Related Concepts

- [[Python Profiling]]
- [[Sampling Profiler]]
- [[pstats]]

## Sources

- [[Python introducing profiling-explorer]]
