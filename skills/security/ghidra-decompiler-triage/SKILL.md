---
name: ghidra-decompiler-triage
description: Analyze compiled binaries, headless decompilation, and p-code emulation based on NSA Ghidra.
version: 1.0.0
category: security
author: AgentDex Community
source: https://github.com/NationalSecurityAgency/ghidra
---

# Ghidra Reverse Engineering & Binary Triage

Use when analyzing executable binaries (ELF, PE, Mach-O), performing headless decompiler batch runs, or evaluating function flow graphs without starting the heavy GUI.

## Core Capabilities
- Headless binary decompilation via `analyzeHeadless`.
- P-Code level intermediate representation extraction.
- Cross-architecture analysis (x86, x64, ARM, AArch64, MIPS, RISC-V).
- Signature and function recovery with exportable C pseudo-code.

## Quick CLI Headless Workflow
```bash
# Analyze a target binary headlessly and export decompiled C code
ghidra_dir="/opt/ghidra"
project_dir="/tmp/ghidra_proj"
mkdir -p "$project_dir"

"$ghidra_dir/support/analyzeHeadless" \
  "$project_dir" TempProject \
  -import "/path/to/binary" \
  -postScript Decompile.java \
  -overwrite
```

## Agent Integration Rules
1. Never load large binaries directly into context; inspect exported symbol tables first.
2. Focus on entry points, imported crypto APIs, and network functions.
3. Validate architecture before invoking specific disassembly options.
