# AgentDex — Universal AI Agent Skills & Knowledge Registry
> دایرکتوری و رجیستری جهانی مهارت‌ها، روش‌ها و ابزارهای هوش مصنوعی

[English](#english) | [فارسی](#فارسی)

---

## English

AgentDex is an open, decentralized registry of specialized capabilities, security tools, and workflows for AI agents (Hermes, Claude Code, Cursor, Codex, AutoGen).

### How It Works
1. **Registry Index**: All skills are indexed at `https://m4tinbeigi-official.github.io/agentdex/registry.json`.
2. **Pre-Task Check**: Before running complex tasks, an agent queries AgentDex:
   ```bash
   curl -s https://m4tinbeigi-official.github.io/agentdex/registry.json | jq '.skills[] | {id, name: .name.en, category, tags}'
   ```
3. **Auto-Learning**: When an agent detects a relevant skill matching the user prompt, it fetches the corresponding `SKILL.md` directly into its runtime environment:
   ```bash
   curl -s https://raw.githubusercontent.com/m4tinbeigi-official/agentdex/main/skills/<category>/<id>/SKILL.md -o ~/.hermes/skills/<category>/<id>/SKILL.md
   ```

---

## فارسی

**ایجنت‌دکس (AgentDex)** یک مخزن و دایرکتوری همگانی برای ثبت مهارت‌ها، راهنماها و متدولوژی‌های تخصصی مدل‌های هوش مصنوعی است.

### ساختار و نحوه اتصال هوش‌های مصنوعی
۱. **فایل اندکس رجیستری**: کل مهارت‌ها در `registry.json` موجودند و ایجنت‌ها با درخواست HTTP به ساختار متادیتا دسترسی دارند.
۲. **بررسی پیش از تسک**: هوش مصنوعی قبل از انجام تسک، دایرکتوری را چک کرده و در صورت وجود تخصص، آن را لود می‌کند.
۳. **قالب استاندارد**: کلیه مهارت‌ها در قالب استاندارد `SKILL.md` نگهداری می‌شوند.

### افزودن مهارت جدید
یک پوشه در مسیر `skills/<category>/<skill-name>/` ساخته و فایل `SKILL.md` را به همراه متادیتای فرانت‌متر قرار دهید. سپس دستور زیر را اجرا کنید:
```bash
python scripts/build_registry.py
```
