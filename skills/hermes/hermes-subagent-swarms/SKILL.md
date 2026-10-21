---
name: hermes-subagent-swarms
description: Parallel subagent delegation patterns, isolated context partitioning, and structured schema validation for Hermes Agent.
version: 1.0.0
category: hermes
author: AgentDex Community
source: https://github.com/NousResearch/hermes-agent
---

# Hermes Subagent Swarm Delegation

Use when handling reasoning-heavy tasks, parallel independent research streams, or multi-faceted auditing that would overwhelm parent context.

## Delegation Protocol
1. **Context Isolation**: Subagents inherit zero memory from the parent conversation. Explicitly inject all required file paths, constraints, and credentials into `context`.
2. **Schema Enforcement**: Pass an explicit `output_schema` to guarantee deterministic structured JSON output upon child completion.
3. **Non-Blocking Execution**: Launch parallel subtasks in a single `delegate_task` call. Finish non-dependent operations, provide a single-line status, and await completion between turns.
4. **Verification Boundary**: Treat child summaries as self-reports; always verify on-disk artifacts or verifiable handles directly in the parent context.
