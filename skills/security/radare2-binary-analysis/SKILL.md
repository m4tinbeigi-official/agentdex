---
name: radare2-binary-analysis
description: CLI-first reverse engineering framework, ELF/PE disassembly, hex editing, and binary diffing.
version: 1.0.0
category: security
author: AgentDex Community
source: https://github.com/radareorg/radare2
---

# Radare2 Reverse Engineering

Use when agents need rapid CLI-based binary inspection, string extraction, function analysis, or patching without heavy GUI overhead.

## Quick CLI Commands
```bash
# Analyze all functions and print summary
r2 -A -q -c "afl" /path/to/binary

# Decompile main function or print assembly
r2 -A -q -c "pdf @main" /path/to/binary
```
