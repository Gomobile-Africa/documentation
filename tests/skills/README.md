# Gomobile plugin verification

Current v0 review package: **0.2.1**, with one `gomobile` skill and five supporting
references. Installation checks and model-behavior evaluations are separate.

## Run package checks

From the repository root, with Python 3.10 or newer:

```bash
python3 scripts/skills/build_bundle.py
python3 tests/skills/check_package.py
python3 scripts/skills/export_repository.py
python3 scripts/skills/export_repository.py --check
node --test tests/markdown/copy-page.test.cjs
```

The Python tools use only the standard library. Generated ZIPs, checksums,
repository exports, caches, and local review copies are excluded from Git.
Builds from a clean checkout do not depend on any historical archive.

With Codex and Claude Code installed, check both clients using the built ZIP:

```bash
python3 tests/skills/check_package.py --codex codex --claude claude
```

To test the actual public Git marketplace instead:

```bash
python3 tests/skills/check_package.py --marketplace-source Gomobile-Africa/gomobile-plugins --codex codex --claude claude
```

Pass the path to a client binary when it is not on `PATH`. Tests use temporary
profiles without sign-in credentials, Git credential configuration, or access to
the author's client configuration. They start no model turns and perform no
Gomobile account operations. The remote check needs Git and network access.

Optional `--upgrade-from PATH_TO_PREVIOUS_ZIP` checks replacement of an older
package. Optional `--download-url HTTPS_URL` verifies the bytes of a separately
hosted ZIP; no public ZIP download is currently advertised or required.

## Recorded installation results

On 23 October 2026, both local-export and anonymous public Git installation passed:

| Client | Recorded checks |
| --- | --- |
| Codex CLI 0.160.0 | Install, enabled cached skill discovery, reachable references, file equality, removal, reinstall |
| Claude Code 2.1.304 | Strict validation, install, enabled single-skill inventory, reachable references, file equality, update, removal, reinstall |

The 0.2.0 → 0.2.1 replacement check also passed on 22 October. These client
versions are tested versions, not minimum requirements or compatibility guarantees.
Mintlify validation, broken-link checks, and Markdown-copy tests passed.

Cleanup verification also passed from a temporary checkout of the staged files,
starting without `dist/`: build, export, both clients' local installation checks,
and all six Markdown-copy tests. Its ZIP matched the SHA-256 below exactly.

Published Git marketplace: https://github.com/Gomobile-Africa/gomobile-plugins.
Initial commit: `2fc8b2b36c96a7b781b90b45a56d7dff29e4111a`, an independent root
commit containing exactly 12 release files, with no authoring-repository history.
The cleanup in this repository preserves those release bytes.

Reproducible 0.2.1 ZIP: **20,602 bytes**; SHA-256:
`66671e7b477a27a18fca7bfc77f06fed24061962ef53bebda090aac7d16d0782`.

## Product and behavioral review

The [source-review record](../../discovery/gomobile-product-source-review-2026-10-22.md)
documents supplied findings against product `develop` commit
`9679b35bd5cd992747f4b6f26b05754d24eda399`. Existing tests were inspected by that
reviewer, not executed. Source findings do not establish deployment parity or
public approval of conditional fields.

Run the [18 manual scenarios](scenarios.md) in fresh target-client sessions to
evaluate the unified skill. Copy or attach the [partial synthetic report](fixtures/run-report.json)
to the isolated workspace before using the report scenario. Record actual
responses and source/tool evidence; scenario descriptions are not passed tests.

Earlier user-supplied four-skill responses concerned 0.1.0. They do not establish
fresh 0.2.1 model outcomes. Technical review, unified-skill behavioral evaluations,
product-runtime checks, event reliability, and conditional-field approval remain
pending. No official-directory listing or ChatGPT installation is claimed.

## Publication boundary

The plugin repository was published separately with user authorization.
Documentation commits do not by themselves establish a deployed Mintlify result.
On 23 October, GitHub reported the documentation repository as public; its
visibility was not changed by this work. Verify actual visibility before making
privacy claims or publishing further files. No product source, account operation,
or global client configuration was changed.
