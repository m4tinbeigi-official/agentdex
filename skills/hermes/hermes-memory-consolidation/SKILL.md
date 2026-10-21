---
name: hermes-memory-consolidation
description: Advanced persistent memory optimization, atomic batch consolidation, and character budget guardrails for Hermes Agent.
version: 1.0.0
category: hermes
author: AgentDex Community
source: https://github.com/NousResearch/hermes-agent
---

# Hermes Persistent Memory Consolidation

Use when persistent memory approaches maximum capacity, or when high-value durable facts must be recorded atomically across sessions.

## Memory Design Contract
- **High-Signal Facts Only**: Store stable environment details, system identities, core user directives, and standing policies.
- **Never Store**: Temporary task progress, ephemeral outputs, raw JSON dumps, or reusable procedures (procedures belong in skills).
- **Atomic Operations**: Always issue batch replacements via the `operations` parameter instead of serial individual adds.

## Consolidation Pattern
When memory is near 100%:
1. Identify outdated or low-relevance entries.
2. Group related facts into single-line declarative statements.
3. Submit a single atomic batch that removes/replaces stale facts while introducing new ones.
