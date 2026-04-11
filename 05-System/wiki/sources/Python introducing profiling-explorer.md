---
type: source
title: "Python introducing profiling-explorer"
source_url: "https://adamj.eu/tech/2026/04/03/python-introducing-profiling-explorer/"
author: "Adam Johnson"
collected_at: "2026-04-11"
---

# Python introducing profiling-explorer

## Summary

Adam Johnson introduces `profiling-explorer`, a new Python tool for exploring profiling data stored in pstats files. The tool provides a web-based interface with dark mode, sortable columns, search filtering, and clickable caller/callee navigation. The article also covers the history and evolution of Python's built-in profilers: the deprecated `profile` module (1992), the C-based `cProfile` (2006), and the upcoming `profiling.sampling` codenamed "Tachyon" (Python 3.15, expected October 2026).

## Key Points

- **profiling-explorer tool**: Web interface for pstats files with dark mode, sortable columns, search by filename/function, copy buttons for locations, and caller/callee navigation
- **Python profiler history**:
  - `profile` (1992): Pure Python tracing profiler, deprecated for removal in 3.17 due to high overhead
  - `cProfile` (2006): C re-implementation with ~50% overhead but per-function overhead can skew results
  - `profiling.sampling`/"Tachyon" (3.15): Low-overhead sampling profiler using periodic stack interrupts
- **Tachyon advantages**: Near-full-speed execution, no per-function overhead skew, compatible with pstats format, supports flame graphs and heat maps
- **Motivation**: Built to address clunky pstats CLI and lack of immediacy in visualization tools like gprof2dot
- **Sponsored by**: Rippling, where it's already being used on their Django codebase

## Technical Details

- **Usage**: `python -m cProfile -o <name>.pstats <program>` or `uvx profiling-explorer <name>.pstats`
- **Output**: Web interface running on http://127.0.0.1:8099/
- **Compatibility**: Works with all three Python profilers since they use the pstats format

## Related Articles

- [[Python: introducing tprof, a targeting profiler]]
- [[Python: Profile a section of code with cProfile]]
- [[Cutting Python Web App Memory Over 31%]]

## Tags

`python` `profiling` `performance` `tools` `django`
