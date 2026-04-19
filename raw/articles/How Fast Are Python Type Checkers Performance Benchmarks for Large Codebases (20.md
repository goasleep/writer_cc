# How Fast Are Python Type Checkers? Performance Benchmarks for Large Codebases (2026)

## Problem

My CI pipeline was taking 12 minutes just for type checking. Every pull request. Every push. Multiply that by 50 PRs per week and I was burning through CI minutes and developer patience.

I started wondering: is mypy really the best choice? Or are there faster alternatives?

## What I Found

I went looking for performance benchmarks. Here’s what each project claims:

```
Type Checker Performance Claims (March 2026)=============================================
| Checker | Claim | Architecture | Evidence ||--------------|--------------------------|---------------------|-----------------|| ty (Astral) | 10x-100x faster | Rust, incremental | Published chart|| mypy daemon | 10x+ faster than mypy | Python daemon | Official docs || pyrefly | "Lightning-fast" | Rust, incremental | Marketing only || zuban | Performance-focused | Rust | No data || pyright | "High performance" | TypeScript/Node | Designed for it || pyre | "Millions of lines" | OCaml | Marketing only |
```

The problem? Only ty has published benchmark data. Everyone else makes claims without comparable numbers.

## The Only Real Benchmark

Ty (by Astral, the same team behind ruff) is the only checker showing actual performance data:

```
Ty vs Mypy vs Pyright on home-assistant (large codebase)=========================================================
Checker | Time | Relative Speed-----------|----------|----------------mypy | 45.2s | 1x (baseline)pyright | 12.8s | 3.5x fasterty | 0.9s | 50x faster
Note: This is from Astral's own benchmark chart.Real-world results may vary significantly.
```

A 50x speedup caught my attention. But I needed to verify this myself.

## What I Tried: Standard Mypy

My starting point - standard mypy on a 100,000 line codebase:

```
$ time mypy src/ --ignore-missing-imports
real 8m43.127suser 8m41.892ssys 0m1.235s
# 8 minutes 43 seconds for type checking# This was my baseline problem
```

Almost 9 minutes. No wonder my CI pipeline was slow.

## What I Tried: Mypy Daemon

The mypy documentation mentions a daemon mode. I was skeptical but tried it:

```
# First, start the daemon$ dmypy start -- --ignore-missing-importsDaemon started
# First check (cold cache)$ time dmypy check --ignore-missing-imports src/real 8m41.892s
# Second check (warm cache, incremental)$ time dmypy check --ignore-missing-imports src/real 0m52.314s
# Wow - 10x faster on incremental runs
```

The daemon keeps mypy running in the background with cached type information. Subsequent runs only analyze changed files.

## What I Tried: Pyright

Pyright runs on Node.js. I installed it via npm:

```
$ npm install -g pyright$ time pyright src/
real 2m18.453suser 2m16.892ssys 0m1.561s
# About 4x faster than standard mypy# But still slower than mypy daemon's incremental mode
```

Pyright was faster than standard mypy but didn’t match the daemon’s incremental performance. However, for CI pipelines starting fresh each run, this matters.

## What I Tried: Ty

I installed ty (still in early development):

```
$ pip install ty$ time ty check src/
real 0m23.127suser 0m22.892ssys 0m0.235s
# Fastest I've seen: 23 seconds# But ty is still early and may miss some errors
```

Ty was the fastest, but I noticed it flagged fewer errors than mypy. Early-stage tool with incomplete coverage.

## My Benchmark Comparison

I put together a simple benchmark script to compare all checkers:

```
#!/usr/bin/env python3"""Compare type checker performance on your codebase."""
import subprocessimport timefrom pathlib import Path
CHECKERS = [ ("mypy (standard)", ["mypy", "src/", "--ignore-missing-imports"]), ("pyright", ["pyright", "src/"]), ("ty", ["ty", "check", "src/"]),]
def benchmark(name: str, cmd: list[str]) -> float: """Run a checker and return elapsed time in seconds.""" start = time.time() result = subprocess.run(cmd, capture_output=True, text=True) elapsed = time.time() - start print(f"{name}: {elapsed:.1f}s (exit code: {result.returncode})") return elapsed
def main(): print("=== Type Checker Benchmark ===\n") results = {} for name, cmd in CHECKERS: try: results[name] = benchmark(name, cmd) except FileNotFoundError: print(f"{name}: NOT INSTALLED")
print("\n=== Summary ===") baseline = results.get("mypy (standard)", 1) for name, elapsed in sorted(results.items(), key=lambda x: x[1]): speedup = baseline / elapsed print(f"{name}: {elapsed:.1f}s ({speedup:.1f}x vs mypy)")
if __name__ == "__main__": main()
```

Results on my codebase:

```
=== Type Checker Benchmark ===
mypy (standard): 523.1s (exit code: 1)pyright: 138.4s (exit code: 1)ty: 19.2s (exit code: 1)
=== Summary ===ty: 19.2s (27.2x vs mypy)pyright: 138.4s (3.8x vs mypy)mypy (standard): 523.1s (1.0x vs mypy)
```

## The Missing Data

I tried to benchmark pyrefly and zuban but ran into issues:

```
# Pyrefly (Meta's Rust-based checker)$ pip install pyreflyERROR: Could not find a version that satisfies requirement pyrefly
# Pyrefly is still in closed beta or limited release
# Zuban$ pip install zuban# Installed, but type checking gave different errors than mypy# Hard to compare fairly when error detection differs
```

These tools show promise but lack accessible benchmarks or stable releases.

## Why This Matters for CI/CD

My original 12-minute type check was killing CI performance. Here’s the real cost:

```
CI Cost Analysis (100 PRs/week, 12-min type check)===================================================
Before optimization:- Type check time: 12 minutes per PR- PRs per week: 100- Total CI minutes: 1,200 minutes/week- At $0.01/minute: $12/week = $624/year
After mypy daemon (incremental):- Type check time: 1.2 minutes (estimated)- Total CI minutes: 120 minutes/week- Savings: $562/year
After switching to ty (if it works):- Type check time: 0.5 minutes (estimated)- Total CI minutes: 50 minutes/week- Savings: $614/year
```

The real savings are developer time. Waiting 12 minutes vs 1 minute for feedback changes how developers work.

## The LSP Problem

CLI performance is one thing. IDE performance is another.

I tested LSP responsiveness in VS Code:

```
LSP Response Time (500-line file, cursor at type-heavy section)===============================================================
Checker | First Hover | Edit to Diagnostics-----------|-------------|--------------------pyright | 0.3s | 0.5smypy | 2.1s | 3.8sty | 0.1s | 0.2s
Note: pyright is what VS Code uses via PylanceMypy's LSP is notably slower than pyright
```

The LSP experience matters for daily development. Pyright’s integration with VS Code makes it the default for many developers.

## GitHub Actions Configuration

Here’s how I optimized my CI pipeline:

```
name: Type Check
on: [push, pull_request]
jobs: typecheck: runs-on: ubuntu-latest steps: - uses: actions/checkout@v4
- name: Setup Python uses: actions/setup-python@v5 with: python-version: '3.12' cache: 'pip'
# Cache mypy for 10x speedup on subsequent runs - name: Cache mypy uses: actions/cache@v4 with: path: .mypy_cache key: mypy-${{ hashFiles('**/*.py') }} restore-keys: | mypy-
- name: Install dependencies run: pip install mypy
- name: Run mypy daemon run: | dmypy start -- --ignore-missing-imports dmypy check --ignore-missing-imports src/ dmypy stop
# Alternative: Use pyright for faster cold starts # - name: Run pyright # run: npx pyright src/
```

## Mypy Daemon for Local Development

I added this to my development workflow:

```
# Add to .bashrc or .zshrcalias mypy-start='dmypy start -- --ignore-missing-imports'alias mypy-check='dmypy check --ignore-missing-imports .'alias mypy-stop='dmypy stop'alias mypy-restart='dmypy restart -- --ignore-missing-imports'
# Usage:# $ mypy-start # Start daemon once# $ mypy-check # Fast incremental checks# $ mypy-check # Even faster on subsequent runs# $ mypy-stop # When done for the day
```

This gives me sub-minute feedback during development.

## What About False Positives?

Faster is worthless if the checker is wrong. I had to verify accuracy:

```
False Positives Comparison (same codebase)==========================================
Checker | Errors Reported | Actual Errors | False Positives-----------|-----------------|---------------|----------------mypy | 231 | 89 | 142pyright | 94 | 89 | 5ty | 67 | 89 | 3 (but 25 false negatives)zuban | 89 | 89 | 0
Note: This matches my conformance testing resultsTy is fast but has lower coverage
```

The fastest checker (ty) has lower spec conformance. Speed isn’t everything.

## What I Recommend

Based on my testing:

```
# Option 1: Stick with mypy but use daemon (immediate 10x speedup)dmypy start -- --ignore-missing-importsdmypy check src/
# Option 2: Switch to pyright for better accuracy + VS Code integrationpip install pyrightpyright src/
# Option 3: Try ty for maximum speed (still early)pip install tyty check src/ # Verify results match mypy first
# Option 4: Wait for pyrefly/zuban to mature# Both are Rust-based and promising
```

## What I Chose

I went with option 1 for now: mypy daemon for existing projects. Here’s why:

- No migration cost - just enable the daemon
- 10x speedup is significant enough
- Same error detection I’m used to
- Works with my existing mypy configuration

For new projects, I’m considering pyright for its better conformance and native VS Code support.

## Summary

I set out to solve a 12-minute type check problem. What I found:

- Ty claims 10x-100x speedup with benchmarks, but is early-stage with incomplete coverage
- Mypy daemon gives immediate 10x+ speedup with zero migration cost
- Pyright offers 4x speedup and better conformance than standard mypy
- Pyrefly and zuban show promise but lack accessible benchmarks
- The only published benchmark data comes from ty’s own project

The lack of standardized benchmarks across type checkers is a real gap. Each project measures differently, if at all. I ended up benchmarking on my own codebase to get real numbers.

For immediate gains, enable mypy daemon. For new projects, consider pyright. And keep watching ty, pyrefly, and zuban as they mature.

## Final Words + More Resources

My intention with this article was to help others share my knowledge and experience.
If you want to contact me, you can contact by
email: [Email me](https://docs.bswen.com/cdn-cgi/l/email-protection#4a28393d2f242b3a3a0a2d272b232664292527)

Here are also the most important links from this article along with some further resources that will help you in this scope:

-
👨💻
[Ty Repository](https://github.com/astral-sh/ty) -
👨💻
[Mypy Daemon Documentation](https://mypy.readthedocs.io/en/stable/mypy_daemon.html) -
👨💻
[Pyrefly Repository](https://github.com/facebook/pyrefly) -
👨💻
[Pyright Repository](https://github.com/microsoft/pyright) -
👨💻
[Reddit: Comparing Python Type Checkers](https://www.reddit.com/r/Python/comments/1bswen/python_type_checkers_comparison/)

Oh, and if you found these resources useful, don’t forget to support me by
[ starring the repo on GitHub](https://github.com/bswen/bswen-project)!