#!/usr/bin/env python3
"""Install this Ludus skill package into <LUDUS_HOME>/skills/<category>/<name>."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
FORBIDDEN_TOP_LEVEL = {"README.md", "CHANGELOG.md", "install.sh", ".env", ".env.example", ".gitignore"}
LINK_RE = re.compile(r"(?<![\w/])((?:references|templates|assets)/[^\s`'\"，。；)）\]}]+)")
TEXT_SUFFIXES = {".md", ".py", ".js", ".mjs", ".json", ".yaml", ".yml", ".txt", ".ps1", ".bat", ".csv"}
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".git", "node_modules", ".DS_Store")
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"C:\\\\Users\\\\", re.IGNORECASE),
    re.compile(r"-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"appsecret\s*[:=]\s*['\"]?[0-9a-fA-F]{32}"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def split_frontmatter(text: str) -> tuple[str, str] | None:
    if not text.startswith("---"):
        return None
    match = re.search(r"\n---\s*\n", text[3:])
    if not match:
        return None
    return text[3:match.start() + 3], text[match.end() + 3:]


def scalar(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", frontmatter, re.M)
    if not match:
        return ""
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def extract_links(text: str) -> list[str]:
    links = []
    for raw in LINK_RE.findall(text):
        link = raw.rstrip(".,;:!?，。；：！？）)]}»")
        link = link.split("#", 1)[0]
        if not link or any(ch in link for ch in "<>*{}"):
            continue
        links.append(link)
    return links


def iter_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file():
            yield path


def scan_secrets(path: Path) -> list[str]:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    text = read_text(path)
    hits = []
    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            hits.append(f"{path}:{line}: {pattern.pattern}")
    return hits


def validate_skill(skill_dir: Path, expected_name: str) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir}: SKILL.md missing"]
    text = read_text(skill_md)
    parts = split_frontmatter(text)
    if parts is None:
        errors.append(f"{skill_md}: frontmatter must start with --- and close with ---")
        body = text
    else:
        frontmatter, body = parts
        name = scalar(frontmatter, "name")
        description = scalar(frontmatter, "description")
        if name != expected_name:
            errors.append(f"{skill_md}: name '{name}' must equal directory '{expected_name}'")
        if not description:
            errors.append(f"{skill_md}: description missing")
        elif len(description) > 60:
            errors.append(f"{skill_md}: description is {len(description)} chars; limit is 60")
        elif not description.rstrip().endswith("."):
            errors.append(f"{skill_md}: description must end with a period")
        if "## When to Use" not in body:
            errors.append(f"{skill_md}: missing '## When to Use'")
    if len(text) > 100_000:
        errors.append(f"{skill_md}: {len(text)} chars exceeds 100000")
    for forbidden in FORBIDDEN_TOP_LEVEL:
        if (skill_dir / forbidden).exists():
            errors.append(f"{skill_dir}: forbidden top-level file '{forbidden}'")
    for link in extract_links(body):
        target = skill_dir / link
        if not target.exists():
            errors.append(f"{skill_md}: referenced path does not exist: {link}")
    for path in iter_files(skill_dir):
        if path.stat().st_size > 1_048_576:
            errors.append(f"{path}: file exceeds 1 MiB")
        for hit in scan_secrets(path):
            errors.append(f"possible secret: {hit}")
    return errors


def resolve_skills_dir(target: str | None) -> Path:
    if target:
        return Path(target).expanduser().resolve()
    home = os.environ.get("LUDUS_HOME")
    if home:
        return (Path(home).expanduser() / "skills").resolve()
    return (Path.home() / ".ludus" / "skills").resolve()


def load_manifest() -> dict:
    path = PACKAGE_ROOT / "manifest.json"
    if not path.is_file():
        raise SystemExit(f"manifest.json not found next to install.py: {path}")
    return json.loads(read_text(path))


def list_package(manifest: dict) -> None:
    print(f"{manifest.get('package')} {manifest.get('version')}")
    print(f"license: {manifest.get('licenseSummary', '')}")
    print(f"internal use only: {manifest.get('internalUseOnly', False)}")
    for skill in manifest.get("skills", []):
        print(f"  {skill['category']}/{skill['name']} -> {skill['path']}")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List skills in this package")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print the install plan")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing install after backup")
    parser.add_argument("--target", help="Skills directory, e.g. ~/.ludus/skills")
    args = parser.parse_args()

    manifest = load_manifest()
    if args.list:
        list_package(manifest)
        return 0

    skills_dir = resolve_skills_dir(args.target)
    backup_root = skills_dir.parent / "skill-backups"
    all_errors: list[str] = []
    plan: list[tuple[Path, Path]] = []

    for skill in manifest.get("skills", []):
        source = PACKAGE_ROOT / skill["path"]
        destination = skills_dir / skill["category"] / skill["name"]
        errors = validate_skill(source, skill["name"])
        all_errors.extend(errors)
        plan.append((source, destination))
        status = "OK" if not errors else f"{len(errors)} error(s)"
        print(f"{skill['category']}/{skill['name']}: {status}")
        for error in errors:
            print(f"  - {error}")

    if all_errors:
        print(f"\nValidation failed with {len(all_errors)} error(s); nothing was installed.", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"\nDry run: would install {len(plan)} skill(s) into {skills_dir}")
        for source, destination in plan:
            print(f"  {source} -> {destination}")
        return 0

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for source, destination in plan:
        if destination.exists():
            if not args.force:
                print(f"Replacing existing skill after backup: {destination} (pass --force to acknowledge)")
            backup_root.mkdir(parents=True, exist_ok=True)
            backup = backup_root / f"{destination.name}-{timestamp}"
            shutil.move(str(destination), str(backup))
            print(f"Backed up existing skill to {backup}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination, ignore=IGNORE)
        print(f"Installed {destination}")

    print("\nDone. Restart Ludus or open a new session, then use skill_view to load the skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
