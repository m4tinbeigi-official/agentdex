#!/usr/bin/env python3
"""
AgentDex Registry Builder.
Scans skills/**/SKILL.md, extracts frontmatter, and updates registry.json.
"""
import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT_DIR / "skills"
REGISTRY_FILE = ROOT_DIR / "registry.json"

KNOWN_LOCALIZATIONS = {
    "ghidra-decompiler-triage": {
        "name": {"en": "Ghidra Reverse Engineering & Binary Triage", "fa": "مهندسی معکوس و تحلیل باینری با گیدرا"},
        "summary": {"en": "Headless decompilation, p-code emulation, and reverse engineering based on NSA Ghidra.", "fa": "دیکامپایل هدلس و تحلیل کد باینری بر پایه گیدرا."},
        "tags": ["ghidra", "reverse-engineering", "binary", "decompiler", "p-code"],
        "compatibility": ["hermes", "claude-code", "cursor", "codex"]
    },
    "turnitout-text-humanizer": {
        "name": {"en": "Turnitout AI Text Humanizer", "fa": "طبیعی‌ساز متن و دور زدن دتکتورهای هوش مصنوعی"},
        "summary": {"en": "Humanize AI text by manipulating perplexity and burstiness to bypass detectors like Turnitin.", "fa": "طبیعی‌سازی متون AI از طریق تغییر پیچیدگی جملات جهت عبور از Turnitin."},
        "tags": ["humanizer", "turnitin", "gptzero", "writing", "burstiness"],
        "compatibility": ["hermes", "claude-code", "chatgpt"]
    },
    "playwright-browser-crawler": {
        "name": {"en": "Playwright Headless Browser Automation & Scraping", "fa": "اتوماسیون مرورگر هدلس و اسکرپینگ با پلی‌رایت"},
        "summary": {"en": "Resilient browser control, stealth scraping, DOM evaluation, and PDF rendering using Playwright.", "fa": "کنترل هوشمند مرورگر، وب‌اسکرپینگ و استخراج DOM با Playwright."},
        "tags": ["playwright", "scraping", "headless-browser", "automation"],
        "compatibility": ["hermes", "claude-code", "cursor", "browser-use"]
    },
    "radare2-binary-analysis": {
        "name": {"en": "Radare2 UNIX-Way Reverse Engineering & Disassembly", "fa": "مهندسی معکوس و دیس‌اسمبل با راداره۲"},
        "summary": {"en": "CLI-first reverse engineering framework, ELF/PE disassembly, hex editing, and binary diffing.", "fa": "فریم‌ورک خط‌فرمانی تحلیل باینری، دیکامپایل و دیس‌اسمبلی."},
        "tags": ["radare2", "reverse-engineering", "disassembler", "binary", "hex"],
        "compatibility": ["hermes", "claude-code", "cursor"]
    },
    "browser-use-web-agent": {
        "name": {"en": "Browser-Use Autonomous Web Agent Framework", "fa": "فریم‌ورک عامل‌محور کنترل مرورگر و وب با هوش مصنوعی"},
        "summary": {"en": "Enable AI models to see, interact, click, and navigate websites autonomously using accessibility trees.", "fa": "هدایت خودکار مرورگر و کلیک و پیمایش وب بر اساس ساختار درختی در دسترس‌پذیری."},
        "tags": ["browser-use", "autonomous-agent", "vision", "web-agent"],
        "compatibility": ["hermes", "claude-code", "langchain"]
    },
    "sqlmap-automated-pentest": {
        "name": {"en": "SQLMap Automated SQL Injection & DB Takeover", "fa": "ارزیابی امنیتی تزریق پایگاه داده با SQLMap"},
        "summary": {"en": "Automatic detection and exploitation of SQL injection flaws and taking over of database servers.", "fa": "کشف و ارزیابی خودکار باگ‌های تزریق به پایگاه داده با ابزار SQLMap."},
        "tags": ["sqlmap", "pentest", "sqli", "security", "database"],
        "compatibility": ["hermes", "claude-code"]
    },
    "crewai-multi-agent-orchestrator": {
        "name": {"en": "CrewAI Autonomous Multi-Agent Orchestrator", "fa": "ارکستراسیون سیستم‌های چندعاملی هوش مصنوعی با CrewAI"},
        "summary": {"en": "Framework for orchestrating role-playing autonomous AI agents that collaborate to solve complex missions.", "fa": "معماری تیم‌های هوشمند ایجنت با نقش‌های تخصصی برای انجام کارهای پیچیده."},
        "tags": ["crewai", "multi-agent", "orchestration", "autonomous"],
        "compatibility": ["hermes", "claude-code", "python"]
    },
    "docker-lean-containerization": {
        "name": {"en": "Minimal Docker Multi-Stage Containerization", "fa": "کانتینرسازی بهینه و چندمرحله‌ای داکر"},
        "summary": {"en": "Production-grade multi-stage Docker build patterns for minimal footprint, rootless security, and caching.", "fa": "الگوهای استاندارد ساخت ایمیج‌های فوق‌سبک و امن با داکر."},
        "tags": ["docker", "devops", "container", "alpine", "multi-stage"],
        "compatibility": ["hermes", "claude-code", "cursor"]
    }
}


def parse_frontmatter(file_path: Path) -> dict:
    content = file_path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        return {}
    raw_yaml, body = match.group(1), match.group(2)
    meta = {}
    for line in raw_yaml.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip().strip('"').strip("'")
    meta["_body"] = body.strip()
    return meta


def build():
    skills = []
    for skill_file in sorted(SKILLS_DIR.rglob("SKILL.md")):
        rel_path = skill_file.relative_to(ROOT_DIR).as_posix()
        meta = parse_frontmatter(skill_file)
        skill_id = meta.get("name", skill_file.parent.name)

        loc = KNOWN_LOCALIZATIONS.get(skill_id, {})
        name = loc.get("name", {
            "en": skill_id.replace("-", " ").title(),
            "fa": skill_id.replace("-", " ")
        })
        summary = loc.get("summary", {
            "en": meta.get("description", ""),
            "fa": meta.get("description", "")
        })
        tags = loc.get("tags", [skill_id, meta.get("category", "general")])
        compat = loc.get("compatibility", ["hermes", "claude-code", "cursor"])

        skills.append({
            "id": skill_id,
            "name": name,
            "category": meta.get("category", skill_file.parent.parent.name),
            "tags": tags,
            "summary": summary,
            "source_repo": meta.get("source", ""),
            "path": rel_path,
            "compatibility": compat,
        })

    registry_data = {
        "$schema": "https://agentdex.dev/schema/v1.json",
        "name": "AgentDex",
        "title": {
            "en": "AgentDex — Universal AI Agent Skills & Knowledge Registry",
            "fa": "ایجنت‌دکس — رجیستری جهانی مهارت‌ها و رفتارهای هوش مصنوعی",
        },
        "description": {
            "en": "Universal index of specialized capabilities, security tools, and workflows for Hermes, Claude Code, Cursor, and custom autonomous agents.",
            "fa": "دایرکتوری جامع ابزارها، روش‌ها و مهارت‌های تخصصی برای هرمس، کلود، کرسر و ایجنت‌های خودمختار.",
        },
        "version": "1.1.0",
        "api_endpoint": "https://m4tinbeigi-official.github.io/agentdex/registry.json",
        "skills": skills,
    }

    REGISTRY_FILE.write_text(json.dumps(registry_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"AgentDex: Successfully indexed {len(skills)} skills into registry.json")


if __name__ == "__main__":
    build()
