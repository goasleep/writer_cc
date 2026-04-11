---
type: concept
name: "cProfile"
---

# cProfile

Python's built-in profiling module, introduced in 2006 as a C re-implementation of the original `profile` module. It has lower overhead than the pure Python version (~50% slower) but still introduces per-function overhead that can skew results.

## Usage

```bash
python -m cProfile -o output.pstats program.py
```

## Related Concepts

- [[Python Profiling]]
- [[pstats]]
- [[profiling-explorer]]

## Sources

- [[Python introducing profiling-explorer]]
