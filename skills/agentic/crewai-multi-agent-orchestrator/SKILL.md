---
name: crewai-multi-agent-orchestrator
description: Framework for orchestrating role-playing autonomous AI agents that collaborate to solve complex missions.
version: 1.0.0
category: agentic
author: AgentDex Community
source: https://github.com/crewAIInc/crewAI
---

# CrewAI Multi-Agent Systems

Use when designing delegated multi-turn tasks requiring role separation (e.g. Researcher agent passing findings to Writer agent).

## Architecture
- Role: Defines specific expertise and prompt constraints.
- Tasks: Discrete deliverables with explicit acceptance criteria.
- Tools: Bound API or terminal capabilities.
