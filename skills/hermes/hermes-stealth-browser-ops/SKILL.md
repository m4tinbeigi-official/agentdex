---
name: hermes-stealth-browser-ops
description: Resilient browser automation using Chrome DevTools Protocol, accessibility trees, and DOM evaluation inside Hermes browser_exec.
version: 1.0.0
category: hermes
author: AgentDex Community
source: https://github.com/NousResearch/hermes-agent
---

# Hermes Stealth Browser Operations

Use when driving live web browsers via Hermes `browser_exec` helper, navigating complex Single-Page Apps (SPAs), or extracting data from JavaScript-heavy DOMs.

## Execution Rules
1. **Accessibility Trees Over Pixels**: Query `cdp('Accessibility.getFullAXTree')` rather than streaming bulky full-page screenshots to preserve context tokens.
2. **Text-First Evaluation**: Use `page_info()` and JavaScript extraction (`js("(() => {...})()")`) for rapid text retrieval.
3. **Batch Operations**: Bundle navigation, wait conditions, and extraction into a single `browser_exec` invocation to prevent roundtrip latency.
4. **Resilient Tab Recovery**: Always invoke `ensure_real_tab()` if the browser session becomes detached or navigates to an internal blank page.
