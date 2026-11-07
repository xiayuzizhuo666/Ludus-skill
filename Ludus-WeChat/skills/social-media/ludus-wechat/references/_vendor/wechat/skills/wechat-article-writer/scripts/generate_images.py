#!/usr/bin/env python3
"""Generate WeChat article images through the Zhipu image API (stdlib only)."""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_ENDPOINT = "https://open.bigmodel.cn/api/paas/v4/images/generations"
DEFAULT_MODEL = "cogview-3"
DEFAULT_SIZE = "1024x1024"
SAFE_ID = re.compile(r"[^A-Za-z0-9._-]+")


def sanitize_id(value: str, index: int) -> str:
    cleaned = SAFE_ID.sub("_", value.strip())
    return cleaned or f"image-{index:02d}"


def read_prompts(path: Path) -> list[dict]:
    prompts = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        if not isinstance(item, dict) or not str(item.get("prompt", "")).strip():
            raise ValueError(f"{path}:{line_number}: missing prompt")
        prompts.append(item)
    return prompts


def post_json(endpoint: str, api_key: str, payload: dict, timeout: int) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def download(url: str, destination: Path, timeout: int) -> None:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        destination.write_bytes(response.read())


def extension_for(url: str, content_type: str = "") -> str:
    suffix = Path(urllib.parse.urlparse(url).path).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return suffix
    if "jpeg" in content_type:
        return ".jpg"
    if "webp" in content_type:
        return ".webp"
    return ".png"


def generate_one(item: dict, index: int, args: argparse.Namespace, api_key: str) -> Path:
    image_id = sanitize_id(str(item.get("id") or f"image-{index:02d}"), index)
    size = str(item.get("size") or args.size)
    payload = {
        "model": args.model,
        "prompt": str(item["prompt"]),
        "size": size,
    }
    if args.dry_run:
        print(json.dumps({"id": image_id, "payload": payload}, ensure_ascii=False))
        return args.out / f"{image_id}.png"

    last_error: Exception | None = None
    for attempt in range(args.retries + 1):
        try:
            response = post_json(args.endpoint, api_key, payload, args.timeout)
            data = response.get("data") or []
            if not data:
                raise RuntimeError(f"API returned no data: {response}")
            first = data[0]
            if first.get("url"):
                url = first["url"]
                destination = args.out / f"{image_id}{extension_for(url)}"
                download(url, destination, args.timeout)
                return destination
            if first.get("b64_json"):
                destination = args.out / f"{image_id}.png"
                destination.write_bytes(base64.b64decode(first["b64_json"]))
                return destination
            raise RuntimeError(f"API response has neither url nor b64_json: {response}")
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, OSError, RuntimeError) as exc:
            last_error = exc
            if attempt < args.retries:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"{image_id}: {last_error}")


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="JSONL with id/prompt/size")
    parser.add_argument("--out", type=Path, default=Path("outputs"), help="Output directory")
    parser.add_argument("--api-key", default=os.environ.get("ZHIPU_API_KEY", ""), help="Zhipu API key")
    parser.add_argument("--model", default=os.environ.get("ZHIPU_IMAGE_MODEL", DEFAULT_MODEL))
    parser.add_argument("--size", default=DEFAULT_SIZE, help="Default image size, e.g. 1024x1024")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--retries", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", help="Print requests without calling the API")
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"Input not found: {args.input}", file=sys.stderr)
        return 1
    try:
        prompts = read_prompts(args.input)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if not prompts:
        print("No prompts found.", file=sys.stderr)
        return 1
    if not args.dry_run and not args.api_key:
        print("ZHIPU_API_KEY is required (or pass --api-key).", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    failures = []
    for index, item in enumerate(prompts, 1):
        try:
            destination = generate_one(item, index, args, args.api_key)
            print(f"OK {destination}")
        except Exception as exc:
            failures.append(str(exc))
            print(f"FAIL {exc}", file=sys.stderr)

    print(f"Summary: {len(prompts) - len(failures)} succeeded, {len(failures)} failed")
    return 0 if args.dry_run or len(failures) < len(prompts) else 1


if __name__ == "__main__":
    raise SystemExit(main())
