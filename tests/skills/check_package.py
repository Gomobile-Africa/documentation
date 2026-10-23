#!/usr/bin/env python3
"""Package checks; optional real-client installs use temporary profiles.

Offline by default; --download-url checks anonymous HTTPS distribution first.
--marketplace-source tests a Git marketplace against the same release files.
No model requests, Gomobile calls, credentials, or third-party Python packages.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import runpy
import shutil
import subprocess
import tempfile
import threading
from urllib.parse import unquote, urlsplit
from urllib.request import urlopen
import zipfile


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "plugins/gomobile"
NAMES = {"gomobile"}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def load(path):
    return json.loads(path.read_text())


def inventory(directory):
    return {
        str(p.relative_to(directory)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in directory.rglob("*") if p.is_file()
    }


def check_references(skill_directory):
    """Every bundled module must be discoverable from the installed entrypoint."""
    owner = skill_directory.resolve()
    pending = [owner / "SKILL.md"]
    visited = set()
    while pending:
        page = pending.pop()
        if page in visited:
            continue
        require(page.is_file() and page.is_relative_to(owner), f"Missing/outside module: {page}")
        visited.add(page)
        for target in re.findall(r"\]\(([^\s)]+)\)", page.read_text()):
            url = urlsplit(target)
            if not url.scheme and url.path:
                relative = (page.parent / unquote(url.path)).resolve()
                require(relative.is_relative_to(owner), f"Module escapes installed skill: {target}")
                if relative.suffix == ".md":
                    pending.append(relative)
    references = {p.resolve() for p in (owner / "references").rglob("*.md")}
    require(references <= visited, f"Undiscoverable references: {references - visited}")


def check_archive():
    builder = runpy.run_path(str(ROOT / "scripts/skills/build_bundle.py"))
    archive_path = builder["output_path"]()
    require(archive_path.is_file(), "Build the customer ZIP with python3 scripts/skills/build_bundle.py")
    content = archive_path.read_bytes()
    require(content == builder["build_bytes"](), "Customer ZIP is stale; rebuild before distribution")
    checksum = f"{hashlib.sha256(content).hexdigest()}  {archive_path.name}\n"
    require(archive_path.with_suffix(".zip.sha256").read_text() == checksum, "ZIP checksum differs")
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)), "Duplicate archive members")
        expected = {f"gomobile-skills/{p}" for p in builder["bundle_files"]()}
        require(set(names) == expected, "Unexpected or missing release files")
        package_files = {f"gomobile-skills/plugins/gomobile/{p}" for p in inventory(PACKAGE)
                         if p != "README.md"}
        require(package_files <= set(names), "Release omitted a package resource")
        for name in names:
            require(name.startswith("gomobile-skills/") and ".." not in Path(name).parts,
                    f"Unsafe archive path: {name}")
            data = archive.read(name)
            require(b"github.com/Gomobile-Africa/documentation" not in data,
                    f"Private repository link in public release: {name}")
            if name.endswith(".md"):
                for target in re.findall(r"\]\(([^\s)]+)\)", data.decode()):
                    url = urlsplit(target)
                    if not url.scheme and url.path:
                        relative = Path(name).parent / unquote(url.path)
                        require(relative.as_posix() in names, f"Download depends on missing file: {target}")
    print("PASS: standalone customer ZIP, checksum, complete resources, and no private repository links")
    return archive_path


def check_static():
    manifests = [load(PACKAGE / p) for p in (
        "plugin.json", ".codex-plugin/plugin.json", ".claude-plugin/plugin.json"
    )]
    for key in ("name", "version", "description"):
        require(len({m[key] for m in manifests}) == 1, f"Manifest {key} differs")
    require(manifests[0]["name"] == "gomobile", "Unexpected plugin identity")
    catalog = load(ROOT / ".claude-plugin/marketplace.json")
    require(catalog["name"] == "gomobile", "Unexpected marketplace identity")
    require(len(catalog["plugins"]) == 1, "Unexpected marketplace contents")
    entry = catalog["plugins"][0]
    require(entry["name"] == "gomobile", "Catalog/manifest identity differs")
    require((ROOT / entry["source"]).resolve() == PACKAGE, "Catalog path is wrong")
    require(manifests[1]["skills"] == "./skills/", "Wrong compatibility skill path")

    # Capability inventory is a release boundary, not a wording check.
    expected_keys = [
        {"$schema", "name", "version", "description", "author", "homepage", "repository"},
        {"name", "version", "description", "skills", "interface"},
        {"name", "version", "description", "author", "homepage", "repository"},
    ]
    for manifest, allowed in zip(manifests, expected_keys):
        require(set(manifest) <= allowed, "Unexpected executable/connection manifest field")
    for path in PACKAGE.rglob("*"):
        require(not path.is_symlink(), f"Package symlink: {path}")
        if path.is_file():
            require(path.suffix in {".md", ".json", ".yaml"}, f"Unexpected package file: {path}")
            require(path.name not in {"mcp.json", ".mcp.json", ".app.json"}, "Unexpected account wiring")
        else:
            require(path.name not in {"scripts", "hooks", "node_modules"}, "Unexpected runtime directory")

    skills = list((PACKAGE / "skills").glob("*/SKILL.md"))
    require({p.parent.name for p in skills} == NAMES, "Missing or extra skills")
    for skill in skills:
        match = re.match(r"\A---\n(.*?)\n---\n", skill.read_text(), re.S)
        require(match is not None, f"Missing frontmatter: {skill}")
        fields = dict(line.split(": ", 1) for line in match[1].splitlines())
        require(fields["name"] == skill.parent.name, f"Wrong skill name: {skill}")
        require(bool(fields["description"].strip()), f"Empty skill description: {skill}")
        check_references(skill.parent)

    # Resolve package links after copying: skills must carry their own references.
    for page in PACKAGE.rglob("*.md"):
        for target in re.findall(r"\]\(([^\s)]+)\)", page.read_text()):
            url = urlsplit(target)
            if url.netloc == "docs.gomobile.ma":
                base = ROOT / (unquote(url.path).strip("/") or "index")
                require(base.with_suffix(".mdx").is_file(), f"Missing customer page: {target}")
            elif not url.scheme and url.path:
                resolved = (page.parent / unquote(url.path)).resolve()
                require(resolved.is_file(), f"Broken package link: {page}: {target}")
                if page.name != "README.md":
                    owner = next(p for p in page.parents if p.parent.name == "skills")
                    require(resolved.is_relative_to(owner), f"Skill depends on outside file: {target}")
    print("PASS: package identities, capability inventory, one skill, and reachable bundled modules")


def check_download(url, expected_archive, destination):
    """Validate the delivered bytes before running client installs from them."""
    def public_https(value):
        parsed = urlsplit(value)
        require(parsed.scheme == "https" and parsed.hostname and not parsed.username and not parsed.password,
                "The customer download must use HTTPS without embedded credentials")
    public_https(url)
    with urlopen(url, timeout=30) as response:
        public_https(response.url)
        require(response.status == 200, "Customer download did not return HTTP 200")
        # The expected bytes are already known; reject an oversized or replaced response.
        expected = expected_archive.read_bytes()
        received = response.read(len(expected) + 1)
    require(received == expected, "Public download differs from the verified versioned ZIP")
    destination.write_bytes(received)
    print("PASS: anonymous HTTPS download matches the verified ZIP and SHA-256")
    return destination


def command(argv, env, cwd):
    result = subprocess.run(argv, cwd=cwd, env=env, text=True, capture_output=True, timeout=45)
    require(result.returncode == 0, f"Command failed: {argv}\n{result.stdout}\n{result.stderr}")
    return result.stdout


def codex_skills(binary, env, cwd, names=NAMES):
    """Use the client's loader, without starting a model turn or using sign-in."""
    with tempfile.TemporaryFile(mode="w+") as errors:
        process = subprocess.Popen(
            [binary, "app-server", "--stdio"], cwd=cwd, env=env,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors, text=True,
        )
        lines = queue.Queue()
        def reader():
            for line in process.stdout:
                lines.put(line)
        worker = threading.Thread(target=reader, daemon=True)
        worker.start()
        def send(payload):
            process.stdin.write(json.dumps(payload) + "\n")
            process.stdin.flush()
        def request(number, method, params):
            send({"id": number, "method": method, "params": params})
            while True:
                try:
                    response = json.loads(lines.get(timeout=20))
                except queue.Empty as exc:
                    raise AssertionError(f"Codex loader timed out at {method}") from exc
                if response.get("id") == number:
                    require("error" not in response, f"Codex loader error: {response}")
                    return response["result"]
        try:
            request(1, "initialize", {
                "clientInfo": {"name": "gomobile-package-check", "version": "0.2.1"},
                "capabilities": {"experimentalApi": True, "requestAttestation": False},
            })
            send({"method": "initialized", "params": {}})
            result = request(2, "skills/list", {"cwds": [str(cwd)], "forceReload": True})
            skills = [s for entry in result["data"] for s in entry["skills"]
                      if s.get("pluginId") == "gomobile@gomobile"]
            require({s["name"] for s in skills} == {f"gomobile:{n}" for n in names},
                    f"Unexpected Codex skill names: {[s['name'] for s in skills]}")
            for skill in skills:
                require(skill["enabled"], f"Disabled skill: {skill['name']}")
                require(Path(skill["path"]).resolve().is_relative_to(Path(env["CODEX_HOME"]).resolve()),
                        "Codex must load the installed cache, not the authoring source")
                check_references(Path(skill["path"]).parent)
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            process.stdin.close()
            process.stdout.close()
            worker.join(timeout=2)


def check_clients(codex, claude, archive_path, upgrade_from=None, marketplace_source=None):
    with tempfile.TemporaryDirectory(prefix="gomobile package ") as temporary:
        base = Path(temporary)
        # Exercise exactly what a customer receives, with no documentation checkout.
        with zipfile.ZipFile(archive_path) as archive:
            archive.extractall(base)
        checkout = base / "gomobile-skills"
        # Avoid loading the real user's client credentials or configuration.
        env = {k: v for k, v in os.environ.items() if k in {
            "PATH", "SYSTEMROOT", "WINDIR", "TMPDIR", "TEMP", "TMP", "LANG", "LC_ALL"
        }}
        config = base / "codex profile"
        config.mkdir()
        env["CODEX_HOME"] = str(config)
        env["CLAUDE_CONFIG_DIR"] = str(base / "claude profile")
        env["DISABLE_TELEMETRY"] = "1"
        env["DISABLE_ERROR_REPORTING"] = "1"
        # Remote installation must work without the author's GitHub credentials.
        env["GIT_CONFIG_GLOBAL"] = os.devnull
        env["GIT_CONFIG_NOSYSTEM"] = "1"
        env["GIT_TERMINAL_PROMPT"] = "0"
        env["GIT_ASKPASS"] = "/usr/bin/false"
        workspace = base / "empty workspace"
        workspace.mkdir()
        install_cwd = workspace if marketplace_source else checkout
        expected = inventory(checkout / "plugins/gomobile")
        previous = None
        if upgrade_from:
            with zipfile.ZipFile(upgrade_from) as archive:
                archive.extractall(base / "previous release")
            previous = base / "previous release/gomobile-skills"
            previous_package = previous / "plugins/gomobile"
            require(load(previous_package / "plugin.json")["name"] == "gomobile", "Wrong previous plugin")
            previous_names = {p.parent.name for p in (previous_package / "skills").glob("*/SKILL.md")}
            previous_files = inventory(previous_package)

        if codex:
            binary = str(Path(shutil.which(codex) or codex).resolve())
            version = command([binary, "--version"], env, checkout).strip()
            if previous:
                command([binary, "plugin", "marketplace", "add", ".", "--json"], env, previous)
                old = load_json_command([binary, "plugin", "add", "gomobile@gomobile", "--json"], env, previous)
                require(inventory(Path(old["installedPath"])) == previous_files, "Previous Codex install differs")
                codex_skills(binary, env, previous, previous_names)
                command([binary, "plugin", "remove", "gomobile@gomobile", "--json"], env, previous)
                command([binary, "plugin", "marketplace", "remove", "gomobile"], env, previous)
            for attempt in range(2):
                command([binary, "plugin", "marketplace", "add", marketplace_source or ".", "--json"], env, install_cwd)
                added = load_json_command([binary, "plugin", "add", "gomobile@gomobile", "--json"], env, install_cwd)
                require(inventory(Path(added["installedPath"])) == expected, "Codex cache differs from package")
                listed = load_json_command([binary, "plugin", "list", "--marketplace", "gomobile", "--json"], env, install_cwd)
                require(listed["installed"], "Codex did not list the installed plugin")
                codex_skills(binary, env, install_cwd)
                command([binary, "plugin", "remove", "gomobile@gomobile", "--json"], env, install_cwd)
                listed = load_json_command([binary, "plugin", "list", "--marketplace", "gomobile", "--json"], env, install_cwd)
                require(not listed["installed"], "Codex uninstall left plugin installed")
                command([binary, "plugin", "marketplace", "remove", "gomobile"], env, install_cwd)
            print(f"PASS: {version}: install, one enabled cached skill, installed references, file integrity, removal, reinstall"
                  + (", replacement of previous release" if previous else "")
                  + (", anonymous Git marketplace" if marketplace_source else ""))

        if claude:
            binary = str(Path(shutil.which(claude) or claude).resolve())
            version = command([binary, "--version"], env, checkout).strip()
            if previous:
                command([binary, "plugin", "marketplace", "add", "./"], env, previous)
                command([binary, "plugin", "install", "gomobile@gomobile"], env, previous)
                old_details = command([binary, "plugin", "details", "gomobile"], env, previous)
                require(f"Skills ({len(previous_names)})" in old_details, "Wrong previous Claude skill inventory")
                for name in previous_names:
                    require(name in old_details, f"Previous Claude install did not discover {name}")
                command([binary, "plugin", "uninstall", "gomobile@gomobile"], env, previous)
                command([binary, "plugin", "marketplace", "remove", "gomobile"], env, previous)
            command([binary, "plugin", "validate", "--strict", str(checkout)], env, checkout)
            command([binary, "plugin", "validate", "--strict", str(checkout / "plugins/gomobile")], env, checkout)
            for attempt in range(2):
                command([binary, "plugin", "marketplace", "add", marketplace_source or "./"], env, install_cwd)
                command([binary, "plugin", "install", "gomobile@gomobile"], env, install_cwd)
                installed = load_json_command([binary, "plugin", "list", "--json"], env, install_cwd)
                plugin = next(p for p in installed if p["id"] == "gomobile@gomobile")
                require(plugin["enabled"], "Claude plugin is not enabled")
                # Local installs may read source directly; inspect the effective folder.
                folder = Path(plugin.get("readFromFolder") or plugin["installPath"])
                require(folder.resolve().is_relative_to(base.resolve()), "Claude install escaped the temporary profile/checkout")
                require(inventory(folder) == expected, "Claude effective package differs from source")
                for name in NAMES:
                    check_references(folder / "skills" / name)
                details = command([binary, "plugin", "details", "gomobile"], env, install_cwd)
                for name in NAMES:
                    require(name in details, f"Claude did not discover {name}")
                require(f"Skills ({len(NAMES)})" in details and "MCP servers (0)" in details and "Hooks (0)" in details,
                        "Unexpected Claude component inventory")
                command([binary, "plugin", "update", "gomobile@gomobile"], env, install_cwd)
                command([binary, "plugin", "uninstall", "gomobile@gomobile"], env, install_cwd)
                remaining = load_json_command([binary, "plugin", "list", "--json"], env, install_cwd)
                require(not any(p["id"] == "gomobile@gomobile" for p in remaining), "Claude uninstall failed")
                command([binary, "plugin", "marketplace", "remove", "gomobile"], env, install_cwd)
            print(f"PASS: {version}: strict validation, install, one skill, installed references, file integrity, update, removal, reinstall"
                  + (", replacement of previous release" if previous else "")
                  + (", anonymous Git marketplace" if marketplace_source else ""))


def load_json_command(argv, env, cwd):
    return json.loads(command(argv, env, cwd))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", metavar="BINARY", help="Also test this Codex CLI in a temporary profile")
    parser.add_argument("--claude", metavar="BINARY", help="Also test this Claude Code CLI in a temporary profile")
    parser.add_argument("--download-url", metavar="HTTPS_URL", help="Download anonymously and test those exact bytes")
    parser.add_argument("--upgrade-from", type=Path, metavar="ZIP", help="Install and remove this previous release before the new one")
    parser.add_argument("--marketplace-source", metavar="OWNER/REPO", help="Install anonymously from this Git marketplace instead of a local folder")
    args = parser.parse_args()
    if args.upgrade_from and not (args.codex or args.claude):
        parser.error("--upgrade-from requires --codex or --claude")
    if args.marketplace_source and not (args.codex or args.claude):
        parser.error("--marketplace-source requires --codex or --claude")
    check_static()
    archive_path = check_archive()
    if args.download_url:
        with tempfile.TemporaryDirectory(prefix="gomobile download ") as temporary:
            downloaded = check_download(args.download_url, archive_path, Path(temporary) / archive_path.name)
            if args.codex or args.claude:
                check_clients(args.codex, args.claude, downloaded, args.upgrade_from, args.marketplace_source)
    elif args.codex or args.claude:
        check_clients(args.codex, args.claude, archive_path, args.upgrade_from, args.marketplace_source)
