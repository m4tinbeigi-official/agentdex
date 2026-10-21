---
name: playwright-browser-crawler
description: Resilient browser control, stealth scraping, DOM evaluation, and PDF rendering using Playwright.
version: 1.0.0
category: devops
author: AgentDex Community
source: https://github.com/microsoft/playwright
---

# Playwright Headless Browser Automation

Use when agents need resilient multi-page web scraping, JavaScript DOM extraction, screenshot generation, or PDF document rendering.

## Core Capabilities
- Headless Chromium, Firefox, and WebKit orchestration.
- Stealth browser execution bypassing basic anti-bot headers.
- Emulation of network conditions, geolocations, and mobile viewports.
- Asynchronous and synchronous execution models.

## Minimal Autonomous Extraction Loop
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent="Mozilla/5.0 AgentDex Crawler")
    page.goto("https://target-url.com", wait_until="networkidle")
    content = page.content()
    browser.close()
```
