#!/usr/bin/env python3
"""Build a standalone customer ZIP without exposing the documentation checkout.

Run from any directory. --check verifies the built artifact without writing.
Only the explicit package inputs below are exported; no Git access or network.
"""

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
import zipfile


ROOT = Path(__file__).resolve().parents[2]
PREFIX = "gomobile-skills"


def bundle_files():
    package = ROOT / "plugins/gomobile"
    files = {
        ".claude-plugin/marketplace.json": ROOT / ".claude-plugin/marketplace.json",
        "README.md": ROOT / "scripts/skills/templates/zip-readme.md",
    }
    for relative in ("plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
        files[f"plugins/gomobile/{relative}"] = package / relative
    for skill in sorted((package / "skills").iterdir()):
        if not skill.is_dir():
            continue
        for path in [skill / "SKILL.md", skill / "agents/openai.yaml", *sorted((skill / "references").glob("*.md"))]:
            files[f"plugins/gomobile/{path.relative_to(package)}"] = path
    for path in files.values():
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(ROOT):
            raise ValueError(f"Missing or unsafe bundle input: {path}")
    return files


def build_bytes():
    output = BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative, path in sorted(bundle_files().items()):
            info = zipfile.ZipInfo(f"{PREFIX}/{relative}", date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compresslevel=9)
    return output.getvalue()


def output_path():
    version = json.loads((ROOT / "plugins/gomobile/plugin.json").read_text())["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?", version):
        raise ValueError("Version cannot form a release filename")
    return ROOT / "dist" / f"gomobile-skills-{version}.zip"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the generated ZIP/checksum needs rebuilding")
    args = parser.parse_args()
    destination = output_path()
    content = build_bytes()
    checksum = f"{hashlib.sha256(content).hexdigest()}  {destination.name}\n"
    checksum_path = destination.with_suffix(".zip.sha256")
    if args.check:
        if not destination.is_file() or destination.read_bytes() != content:
            raise SystemExit("Bundle is missing or stale; run python3 scripts/skills/build_bundle.py")
        if not checksum_path.is_file() or checksum_path.read_text() != checksum:
            raise SystemExit("Bundle checksum is missing or stale; rebuild the bundle")
        print(f"PASS: standalone ZIP and SHA-256 match package inputs ({len(content)} bytes)")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        checksum_path.write_text(checksum)
        print(f"Built {destination.relative_to(ROOT)} ({len(content)} bytes)")
        print(checksum.strip())
