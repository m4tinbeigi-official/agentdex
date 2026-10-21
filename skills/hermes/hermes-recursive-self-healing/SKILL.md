---
name: hermes-recursive-self-healing
description: Autonomous 4-phase error recovery, root-cause isolation, and self-patching for Hermes tool and code execution failures.
version: 1.0.0
category: hermes
author: AgentDex Community
source: https://github.com/NousResearch/hermes-agent
---

# Hermes Recursive Self-Healing & Error Recovery

Use when a command, script, tool call, or build step in Hermes encounters an unexpected exception, non-zero exit code, or type mismatch.

## The 4-Phase Recovery Protocol
1. **Full Error Intake**: Never retry the same command blindly. Read the full traceback, identifying exact line numbers and exception signatures.
2. **Type & State Verification**: 80% of runtime failures stem from subtle schema mismatches (e.g. dict vs list, string vs int, missing env var). Verify in-memory state before patching.
3. **Smallest Reproducible Unit**: Isolate the failing logic into a 3-line RAM test via `python3 -c` before touching project files.
4. **Root-Cause Patching**: Apply the minimal diff to the actual source file rather than silencing errors with loose `try/except`.

## Rules
- Never fabricate output or substitute fake responses when an execution blocks.
- Report real blockers to user with technical precision.
- Test fixes with run-checks immediately.
