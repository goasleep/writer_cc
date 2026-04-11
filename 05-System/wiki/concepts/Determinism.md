---
type: concept
name: "Determinism"
---

# Determinism

The property of a system where running the same code multiple times with the same inputs produces the same results and execution sequence.

## Importance in AI/ML

- Enables reproducible experiments
- Simplifies debugging
- Ensures reliable deployments
- Critical for Explainable AI (XAI)

## Async Python Determinism

Despite the complexity of asynchronous operations, Python's `asyncio` framework can exhibit surprising determinism within a single event loop. The execution order after `await` points is largely predictable, even when external timing varies.

## Related Concepts

- [[asyncio]]
- [[MLOps]]
- [[Explainable AI]]

## Sources

- [[Async Python's Determinism Builds Reliable AI Futures]]
