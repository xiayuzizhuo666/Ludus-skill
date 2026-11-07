#!/usr/bin/env python3
"""Smoke-test the Life package without network access."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = next((ROOT / "skills").glob("*/*"))


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    required = [
        SKILL / "references/_vendor/hltb/book/01-不要早死.md",
        SKILL / "references/_vendor/hltb/docs/结婚划不划算.md",
        SKILL / "references/_vendor/hltb/index.html",
        SKILL / "references/_vendor/hltb-enhancements/how-to-survive-unemployment/README.md",
    ]
    for path in required:
        check(path.is_file(), f"missing {path}")

    result = subprocess.run(
        [sys.executable, str(SKILL / "scripts/extract_ratio.py")],
        cwd=SKILL,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    check(result.returncode == 0, result.stderr)
    check("COST_W" in result.stdout and "e.ratio" in result.stdout, result.stdout)
    print("PASS: life smoke")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
