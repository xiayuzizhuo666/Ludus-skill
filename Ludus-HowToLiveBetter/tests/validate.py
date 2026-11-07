#!/usr/bin/env python3
"""Validate one Ludus skill package before install."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT))

import install  # noqa: E402


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    manifest_path = PACKAGE_ROOT / "manifest.json"
    if not manifest_path.is_file():
        print(f"FAIL: manifest.json missing: {manifest_path}")
        return 1
    manifest = json.loads(install.read_text(manifest_path))
    errors: list[str] = []

    if not manifest.get("licenseSummary"):
        errors.append("manifest.json: licenseSummary missing")
    if manifest.get("commercialUseRequiresPermission") is not True:
        errors.append("manifest.json: commercialUseRequiresPermission must be true")

    for skill in manifest.get("skills", []):
        source = PACKAGE_ROOT / skill["path"]
        errors.extend(install.validate_skill(source, skill["name"], skill.get("vendorFileCounts")))

        visible = [
            path
            for path in source.rglob("SKILL.md")
            if "_vendor" not in path.parts
        ]
        if len(visible) != 1:
            errors.append(f"{source}: expected exactly one visible SKILL.md, found {len(visible)}")

        index = source / "references" / "INDEX.md"
        if index.is_file():
            for link in install.extract_links(install.read_text(index)):
                if not (source / link).exists():
                    errors.append(f"{index}: referenced path does not exist: {link}")

        vendor = skill.get("vendor")
        expected = skill.get("vendorSkillCount")
        if vendor and expected is not None:
            vendor_dir = source / vendor
            count = len(list(vendor_dir.rglob("SKILL.md"))) if vendor_dir.is_dir() else 0
            if count != expected:
                errors.append(f"{vendor_dir}: expected {expected} vendor SKILL.md, found {count}")

    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"PASS: {manifest.get('package')} {manifest.get('version')}")
    for skill in manifest.get("skills", []):
        print(f"  {skill['category']}/{skill['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
