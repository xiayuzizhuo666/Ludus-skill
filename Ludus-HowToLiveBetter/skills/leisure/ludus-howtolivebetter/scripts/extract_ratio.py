#!/usr/bin/env python3
"""Print the COST_W and e.ratio lines from the vendored book index.html."""
from __future__ import annotations

import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = SKILL_ROOT / "references" / "_vendor" / "hltb" / "index.html"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if not INDEX_HTML.is_file():
        print(f"index.html not found: {INDEX_HTML}", file=sys.stderr)
        return 1
    lines = INDEX_HTML.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    hits = [
        (number, line.strip())
        for number, line in enumerate(lines, 1)
        if "COST_W =" in line or "e.ratio =" in line
    ]
    if not hits:
        print("COST_W = / e.ratio = not found in index.html", file=sys.stderr)
        return 1
    for number, line in hits[:20]:
        print(f"{number}: {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
