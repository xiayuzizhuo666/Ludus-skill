#!/usr/bin/env python3
"""Run the vendored WeChat publisher scripts with a writable config path."""
from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VENDOR_ROOT = SKILL_ROOT / "references" / "_vendor" / "wechat"
PUBLISHER_SCRIPTS = VENDOR_ROOT / "skills" / "wechat-publisher" / "scripts"
SCRIPTS = {
    "upload-draft": PUBLISHER_SCRIPTS / "upload-draft.js",
    "md-to-wechat-html": PUBLISHER_SCRIPTS / "md-to-wechat-html.js",
}


def default_config_path() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "ludus-wechat" / "wechat-config.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a vendored WeChat script with WECHAT_CONFIG pointing to a writable path.",
        epilog=(
            "Examples:\n"
            "  python scripts/run_wechat.py --html article.html --title \"标题\"\n"
            "  python scripts/run_wechat.py --script md-to-wechat-html --input article.md --output article.html\n"
            "  python scripts/run_wechat.py --dry-run --html article.html --title \"标题\""
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--script", choices=sorted(SCRIPTS), default="upload-draft")
    parser.add_argument("--config", type=Path, default=None, help="Writable wechat-config.json path")
    parser.add_argument("--node", default="node", help="Node.js executable")
    parser.add_argument("--dry-run", action="store_true", help="Print the command without running it")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = build_parser()
    args, passthrough = parser.parse_known_args(argv)
    script = SCRIPTS[args.script]
    if not script.is_file():
        print(f"Vendored script not found: {script}", file=sys.stderr)
        return 1

    node = shutil.which(args.node)
    if node is None:
        print(f"Node.js not found: {args.node}", file=sys.stderr)
        return 1

    env = os.environ.copy()
    command = [node, str(script)]

    if args.script == "upload-draft":
        has_inline_credentials = "--appid" in passthrough or "--secret" in passthrough
        config = args.config or Path(env.get("WECHAT_CONFIG", default_config_path()))
        env["WECHAT_CONFIG"] = str(config)
        if "--config" not in passthrough:
            command.extend(["--config", str(config)])
        if not config.is_file() and not has_inline_credentials:
            print(
                f"Warning: config not found: {config}\n"
                "Pass --appid/--secret, or create the file from templates/wechat-config.example.json.",
                file=sys.stderr,
            )

    command.extend(passthrough)

    if args.dry_run:
        print(shlex.join(command))
        if args.script == "upload-draft":
            print(f"WECHAT_CONFIG={env['WECHAT_CONFIG']}")
        return 0

    return subprocess.run(command, env=env).returncode


if __name__ == "__main__":
    raise SystemExit(main())
