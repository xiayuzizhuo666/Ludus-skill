#!/usr/bin/env python3
"""Smoke-test the WeChat package scripts."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = next((ROOT / "skills").glob("*/*"))
VENDOR = SKILL / "references/_vendor/wechat"


def run(command: list[str]) -> None:
    result = subprocess.run(command, cwd=SKILL, capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, f"{command}\n{result.stdout}\n{result.stderr}"


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    assert (VENDOR / "skills/wechat-article-writer/SKILL.md").is_file()
    assert (VENDOR / "skills/wechat-article-writer/writing_style.md").is_file()
    assert not (VENDOR / "skills/khazix-writer").exists()
    run([sys.executable, str(SKILL / "scripts/run_wechat.py"), "--help"])
    run([sys.executable, str(VENDOR / "skills/wechat-article-writer/scripts/generate_images.py"), "--help"])
    run([sys.executable, str(VENDOR / "skills/wechat-topic-selector/topic_selector.py"), "--help"])
    assert (SKILL / "templates/wechat-config.example.json").is_file()
    assert not list(VENDOR.rglob(".wechat-config.json")), "real config must not ship"

    node = shutil.which("node")
    if node:
        run([node, str(VENDOR / "skills/wechat-publisher/scripts/upload-draft.js"), "--help"])
        run([node, str(VENDOR / "skills/wechat-publisher/scripts/md-to-wechat-html.js"), "--help"])
    else:
        print("SKIP: node not found; skipped Node script help checks")

    print("PASS: wechat smoke")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
