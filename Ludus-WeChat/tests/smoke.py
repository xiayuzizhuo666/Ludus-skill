#!/usr/bin/env python3
"""Smoke-test the WeChat package scripts."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
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
    assert "上游 4 个技能" in (SKILL / "references/PATHS.md").read_text(encoding="utf-8")
    stale = [
        path
        for path in SKILL.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".md", ".js", ".json", ".py", ".txt"}
        and "卡兹克" in path.read_text(encoding="utf-8-sig", errors="ignore")
    ]
    assert not stale, f"stale 卡兹克 references: {stale}"

    run([sys.executable, str(SKILL / "scripts/run_wechat.py"), "--help"])
    run([sys.executable, str(VENDOR / "skills/wechat-article-writer/scripts/generate_images.py"), "--help"])
    run([sys.executable, str(VENDOR / "skills/wechat-topic-selector/topic_selector.py"), "--help"])
    assert (SKILL / "templates/wechat-config.example.json").is_file()
    assert not list(VENDOR.rglob(".wechat-config.json")), "real config must not ship"

    node = shutil.which("node")
    assert node, "Node.js is required for the WeChat smoke test"
    run([node, str(VENDOR / "skills/wechat-publisher/scripts/upload-draft.js"), "--help"])
    run([node, str(VENDOR / "skills/wechat-publisher/scripts/md-to-wechat-html.js"), "--help"])

    with tempfile.TemporaryDirectory() as tmp:
        md = Path(tmp) / "a.md"
        md.write_text("# 标题\n\n正文\n", encoding="utf-8")
        html = Path(tmp) / "a.html"
        md_script = VENDOR / "skills/wechat-publisher/scripts/md-to-wechat-html.js"
        result = subprocess.run(
            [node, str(md_script), "--input", str(md), "--output", str(html), "--style", "7"],
            cwd=SKILL,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert result.returncode != 0, "numeric --style should be rejected"
        result = subprocess.run(
            [node, str(md_script), "--input", str(md), "--output", str(html), "--style", "warm"],
            cwd=SKILL,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert result.returncode == 0, result.stderr
        assert html.is_file() and html.stat().st_size > 0

        env_file = Path(tmp) / "image.env"
        env_file.write_text("ZHIPU_API_KEY=test-key\n", encoding="utf-8")
        prompts = Path(tmp) / "prompts.jsonl"
        prompts.write_text('{"id":"cover","prompt":"test"}\n', encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(VENDOR / "skills/wechat-article-writer/scripts/generate_images.py"),
                "--input",
                str(prompts),
                "--out",
                str(Path(tmp) / "images"),
                "--env-file",
                str(env_file),
                "--dry-run",
            ],
            cwd=SKILL,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert result.returncode == 0, result.stderr
        assert "Loaded env file" in result.stderr

    print("PASS: wechat smoke")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
