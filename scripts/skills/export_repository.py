#!/usr/bin/env python3
"""Export the public plugin repository without private sources or Git history.

Uses the same explicit file list as the customer ZIP and a Git-install README.
Does not create a Git repository, commit, push, or contact any external service.
"""

import argparse
import hashlib
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DESTINATION = ROOT / "dist/public/gomobile-plugins"


def export_files():
    builder = runpy.run_path(str(ROOT / "scripts/skills/build_bundle.py"))
    files = builder["bundle_files"]()
    files["README.md"] = ROOT / "scripts/skills/templates/repository-readme.md"
    return files


def export(destination, check=False):
    if destination.is_symlink():
        raise ValueError("Destination must not be a symlink")
    destination = destination.resolve()
    if destination == ROOT or ROOT.is_relative_to(destination):
        raise ValueError("Destination must not be the authoring checkout or its parent")
    expected = export_files()
    if destination.exists():
        if any(p.is_symlink() for p in destination.rglob("*") if ".git" not in p.relative_to(destination).parts):
            raise ValueError("Export directory contains a symlink")
        actual = {str(p.relative_to(destination)) for p in destination.rglob("*")
                  if p.is_file() and ".git" not in p.relative_to(destination).parts}
        if actual - expected.keys():
            raise ValueError(f"Unexpected export files; refusing to overwrite: {sorted(actual - expected.keys())}")
    for relative, source in sorted(expected.items()):
        target = destination / relative
        if not target.resolve().is_relative_to(destination) or target.is_symlink():
            raise ValueError(f"Unsafe export target: {relative}")
        content = source.read_bytes()
        if check:
            if not target.is_file() or target.read_bytes() != content:
                raise ValueError(f"Missing or stale export: {relative}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        print(f"{hashlib.sha256(content).hexdigest()}  {relative}")
    print(f"{'Verified' if check else 'Exported'} {len(expected)} public files: {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", type=Path, default=DEFAULT_DESTINATION)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    export(args.destination, args.check)
