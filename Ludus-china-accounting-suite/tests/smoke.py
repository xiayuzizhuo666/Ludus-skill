#!/usr/bin/env python3
"""Smoke-test the accounting package (pure Markdown)."""
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = next((ROOT / "skills").glob("*/*"))
VENDOR = SKILL / "references/_vendor/accounting/skills"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    skills = sorted(VENDOR.glob("*/SKILL.md"))
    assert len(skills) == 26, f"expected 26 vendor skills, found {len(skills)}"
    assert (SKILL / "templates/accounting-ledger.md").is_file()
    assert (VENDOR / "china-accounting-framework/SKILL.md").is_file()

    entry = VENDOR / "china-accounting/SKILL.md"
    text = entry.read_text(encoding="utf-8-sig")
    links = set(re.findall(r"\.\./china-[a-z0-9-]+/SKILL\.md", text))
    assert links, "entry skill should reference sibling china-* skills"
    for link in links:
        target = (entry.parent / link).resolve()
        assert target.is_file(), f"dangling sibling link: {link}"

    print(f"PASS: accounting smoke ({len(skills)} skills, {len(links)} sibling links)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
