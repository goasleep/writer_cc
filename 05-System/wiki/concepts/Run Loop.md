---
type: concept
name: "Run Loop"
---

# Run Loop

The execution engine of an AI agent that runs until a goal is reached or a stop condition fires.

## Structure

```
while not done and steps < limit:
    observe → reason → act → check
```

## Components

- **observe**: Get current state
- **reason**: LLM decides what to do
- **act**: Execute tools/APIs
- **check**: Determine if done

## Related Concepts

- [[AI Agent]]
- [[LLM]]
- [[Memory]]
- [[Tools]]

## Sources

- [[Everyone Is Talking About AI Agents. Most People Have No Idea How to Build One.]]
