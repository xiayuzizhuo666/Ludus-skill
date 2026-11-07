#!/usr/bin/env python3
"""Smoke-test the LawBox package path mapping and scripts."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = next((ROOT / "skills").glob("*/*"))
VENDOR = SKILL / "references/_vendor/lawbox/skills/legal"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    skills = sorted(VENDOR.glob("*/SKILL.md"))
    assert len(skills) == 58, f"expected 58 vendor skills, found {len(skills)}"
    assert (SKILL / "references/_vendor/cn-law-hub/SKILL.md").is_file()
    assert (SKILL / "references/_vendor/cn-law-hub/LICENSE").is_file()
    assert (SKILL / "references/_vendor/cn-law-hub/NOTICE").is_file()

    result = subprocess.run(
        [sys.executable, str(SKILL / "scripts/show_vendor_paths.py"), "--json"],
        cwd=SKILL,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["skill_count"] == 58, data
    assert data["preflight_check"] and data["html_to_docx"] and data["health_check"], data

    preflight = VENDOR / "法律文书出稿前审查/scripts/preflight_check.py"
    result = subprocess.run(
        [sys.executable, str(preflight), "--help"],
        cwd=SKILL,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr

    print("PASS: lawbox smoke (58 skills, path mapping, preflight)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
