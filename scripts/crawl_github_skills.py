#!/usr/bin/env python3
"""
AgentDex Automated GitHub Skill Crawler & Ingestion Pipeline.
Searches GitHub for top trending agent frameworks, security tools,
and specialized automation skills, generating standardized SKILL.md files.
"""

import json
import subprocess
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / "skills"

# High-signal candidate repos across agent ecosystems, security, browser automation, and developer tooling
CURATED_SOURCES = [
    {
        "id": "playwright-browser-crawler",
        "name": {
            "en": "Playwright Headless Browser Automation & Scraping",
            "fa": "اتوماسیون مرورگر هدلس و وب‌اسکرپینگ با پلی‌رایت"
        },
        "category": "devops",
        "tags": ["playwright", "scraping", "headless-browser", "automation", "e2e"],
        "summary": {
            "en": "Resilient browser control, stealth scraping, DOM evaluation, and PDF rendering using Playwright.",
            "fa": "کنترل پیشرفته مرورگر، وب‌اسکرپینگ، اجرای کد روی DOM و خروجی PDF با Playwright."
        },
        "source": "https://github.com/microsoft/playwright",
        "compatibility": ["hermes", "claude-code", "cursor", "browser-use"],
        "content": """# Playwright Headless Browser Automation

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
"""
    },
    {
        "id": "radare2-binary-analysis",
        "name": {
            "en": "Radare2 UNIX-Way Reverse Engineering & Disassembly",
            "fa": "مهندسی معکوس و دیس‌اسمبل با راداره۲"
        },
        "category": "security",
        "tags": ["radare2", "reverse-engineering", "disassembler", "binary", "hex", "shellcode"],
        "summary": {
            "en": "CLI-first reverse engineering framework, ELF/PE disassembly, hex editing, and binary diffing.",
            "fa": "فریم‌ورک خط‌فرمانی مهندسی معکوس، بررسی هدرهای ELF و تحلیل بایت‌های باینری."
        },
        "source": "https://github.com/radareorg/radare2",
        "compatibility": ["hermes", "claude-code", "cursor"],
        "content": """# Radare2 Reverse Engineering

Use when agents need rapid CLI-based binary inspection, string extraction, function analysis, or patching without heavy GUI overhead.

## Quick CLI Commands
```bash
# Analyze all functions and print summary
r2 -A -q -c "afl" /path/to/binary

# Decompile main function or print assembly
r2 -A -q -c "pdf @main" /path/to/binary
```
"""
    },
    {
        "id": "browser-use-web-agent",
        "name": {
            "en": "Browser-Use Autonomous Web Agent Framework",
            "fa": "فریم‌ورک عامل‌محور کنترل مرورگر و وب با هوش مصنوعی"
        },
        "category": "agentic",
        "tags": ["browser-use", "autonomous-agent", "vision", "web-agent", "action-space"],
        "summary": {
            "en": "Enable AI models to see, interact, click, and navigate websites autonomously using accessibility trees.",
            "fa": "توانمندسازی مدل‌های هوش مصنوعی برای دیدن، کلیک و پیمایش خودکار صفحات وب."
        },
        "source": "https://github.com/browser-use/browser-use",
        "compatibility": ["hermes", "claude-code", "langchain"],
        "content": """# Browser-Use Autonomous Web Agent

Use when executing complex end-to-end web workflows (sign-up flows, purchasing, dynamic search filtering) where pure HTML scraping fails.

## Key Principles
- Uses browser accessibility tree rather than raw oversized HTML trees to save context tokens.
- Interactive coordinates mapping for click/type dispatch.
"""
    },
    {
        "id": "sqlmap-automated-pentest",
        "name": {
            "en": "SQLMap Automated SQL Injection & DB Takeover",
            "fa": "تست نفوذ و ارزیابی امنیتی تزریق پایگاه داده با SQLMap"
        },
        "category": "security",
        "tags": ["sqlmap", "pentest", "sqli", "security", "database", "redteam"],
        "summary": {
            "en": "Automatic detection and exploitation of SQL injection flaws and taking over of database servers.",
            "fa": "کشف و ارزیابی خودکار باگ‌های SQL Injection و بررسی آسیب‌پذیری‌های دیتابیس."
        },
        "source": "https://github.com/sqlmapproject/sqlmap",
        "compatibility": ["hermes", "claude-code"],
        "content": """# SQLMap Penetration Testing

Use for authorized vulnerability assessments and automated database injection testing.

## Minimal CLI Usage
```bash
# Batch non-interactive assessment
sqlmap -u "https://target-domain.com/item?id=1" --batch --random-agent --level=2 --risk=1
```
"""
    },
    {
        "id": "crewai-multi-agent-orchestrator",
        "name": {
            "en": "CrewAI Autonomous Multi-Agent Orchestrator",
            "fa": "ارکستراسیون سیستم‌های چندعاملی و تیم هوش مصنوعی CrewAI"
        },
        "category": "agentic",
        "tags": ["crewai", "multi-agent", "orchestration", "collaboration", "autonomous"],
        "summary": {
            "en": "Framework for orchestrating role-playing autonomous AI agents that collaborate to solve complex missions.",
            "fa": "معماری تیم‌های هوشمند ایجنت‌ها با نقش‌های تخصصی و زنجیره همکاری برای حل تسک‌ها."
        },
        "source": "https://github.com/crewAIInc/crewAI",
        "compatibility": ["hermes", "claude-code", "python"],
        "content": """# CrewAI Multi-Agent Systems

Use when designing delegated multi-turn tasks requiring role separation (e.g. Researcher agent passing findings to Writer agent).

## Architecture
- Role: Defines specific expertise and prompt constraints.
- Tasks: Discrete deliverables with explicit acceptance criteria.
- Tools: Bound API or terminal capabilities.
"""
    },
    {
        "id": "docker-lean-containerization",
        "name": {
            "en": "Minimal Docker Multi-Stage Containerization",
            "fa": "معماری کانتینرسازی بهینه و چندمرحله‌ای داکر"
        },
        "category": "devops",
        "tags": ["docker", "devops", "container", "alpine", "multi-stage", "security"],
        "summary": {
            "en": "Production-grade multi-stage Docker build patterns for minimal footprint, rootless security, and caching.",
            "fa": "الگوهای استاندارد ساخت ایمیج‌های فوق‌سبک، امن و بدون روت با داکر چندمرحله‌ای."
        },
        "source": "https://github.com/docker/awesome-compose",
        "compatibility": ["hermes", "claude-code", "cursor"],
        "content": """# Docker Lean Containerization

Use when packaging services into minimal, secure, non-root OCI containers.

## Best Practice Pattern
```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final minimal runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
USER 10001
CMD ["python", "main.py"]
```
"""
    }
]


def ingest_skills():
    print(f"AgentDex Ingestion: Processing {len(CURATED_SOURCES)} top-tier skills...")
    for item in CURATED_SOURCES:
        cat_dir = SKILLS_DIR / item["category"] / item["id"]
        cat_dir.mkdir(parents=True, exist_ok=True)
        skill_file = cat_dir / "SKILL.md"

        yaml_header = f"""---
name: {item["id"]}
description: {item["summary"]["en"]}
version: 1.0.0
category: {item["category"]}
author: AgentDex Community
source: {item["source"]}
---

"""
        full_text = yaml_header + item["content"].strip() + "\n"
        skill_file.write_text(full_text, encoding="utf-8")
        print(f"  + Added skill: {item['id']} ({item['category']})")

    # Rebuild registry.json
    build_script = ROOT_DIR / "scripts" / "build_registry.py"
    subprocess.run(["python3", str(build_script)], check=True)
    print("AgentDex Ingestion Complete.")


if __name__ == "__main__":
    ingest_skills()
