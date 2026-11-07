#!/usr/bin/env python3
"""Print the LawBox vendor-root mapping before running export scripts."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VENDOR_ROOT = SKILL_ROOT / "references" / "_vendor" / "lawbox"
LEGAL_DIR = VENDOR_ROOT / "skills" / "legal"
PREFLIGHT = LEGAL_DIR / "法律文书出稿前审查" / "scripts" / "preflight_check.py"
EXPORT = LEGAL_DIR / "法律文书模板与导出" / "scripts" / "html_to_docx.py"
HEALTH = LEGAL_DIR / "法律文书模板与导出" / "scripts" / "health_check.py"


def payload() -> dict[str, object]:
    workspace = Path(os.environ.get("LEGAL_WORKSPACE", ".")).expanduser().resolve()
    return {
        "skill_root": str(SKILL_ROOT),
        "vendor_root": str(VENDOR_ROOT),
        "legal_dir": str(LEGAL_DIR),
        "legal_workspace": str(workspace),
        "workspace_is_inside_skill": workspace.is_relative_to(SKILL_ROOT.resolve()),
        "skill_count": len(list(LEGAL_DIR.glob("*/SKILL.md"))),
        "preflight_check": PREFLIGHT.is_file(),
        "html_to_docx": EXPORT.is_file(),
        "health_check": HEALTH.is_file(),
    }


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print JSON")
    args = parser.parse_args()
    data = payload()
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        for key, value in data.items():
            print(f"{key}: {value}")
        if data["workspace_is_inside_skill"]:
            print(
                "WARNING: LEGAL_WORKSPACE is inside the skill directory. "
                "Set it to the user's matter directory.",
                file=sys.stderr,
            )
    return 0 if data["skill_count"] == 58 else 1


if __name__ == "__main__":
    raise SystemExit(main())
