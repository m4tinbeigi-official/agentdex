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
    existing = {}
    if REGISTRY_FILE.exists():
        try:
            existing = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    skills = []
    for skill_file in sorted(SKILLS_DIR.rglob("SKILL.md")):
        rel_path = skill_file.relative_to(ROOT_DIR).as_posix()
        meta = parse_frontmatter(skill_file)
        skill_id = meta.get("name", skill_file.parent.name)

        # Check existing definitions to preserve translations if available
        matched_existing = next(
            (s for s in existing.get("skills", []) if s.get("id") == skill_id),
            None,
        )

        name = matched_existing.get("name") if matched_existing else {
            "en": meta.get("name", skill_id).replace("-", " ").title(),
            "fa": meta.get("name", skill_id).replace("-", " "),
        }
        summary = matched_existing.get("summary") if matched_existing else {
            "en": meta.get("description", ""),
            "fa": meta.get("description", ""),
        }
        tags = matched_existing.get("tags") if matched_existing else [skill_id, meta.get("category", "general")]
        compat = matched_existing.get("compatibility") if matched_existing else ["hermes", "claude-code", "cursor"]

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
        "version": existing.get("version", "1.0.0"),
        "api_endpoint": "https://m4tinbeigi-official.github.io/agentdex/registry.json",
        "skills": skills,
    }

    REGISTRY_FILE.write_text(json.dumps(registry_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"AgentDex: Successfully indexed {len(skills)} skills into registry.json")


if __name__ == "__main__":
    build()
