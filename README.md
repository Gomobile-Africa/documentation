# Gomobile documentation

Product guides and API reference for Gomobile, built with Mintlify.

## Getting started

Install [Node.js](https://nodejs.org/) **20.17.0 or newer** with npm, and ensure you have Git and access to the repository.

Clone the project:

```bash
git clone https://github.com/Gomobile-Africa/documentation.git
cd documentation
```

## Development

Install the Mintlify CLI:

```bash
npm install -g mint
```

Run the preview from the repository root, where `docs.json` is located:

```bash
mint dev
```

Open **http://localhost:3000**, or the URL printed in your terminal. Keep the terminal running while previewing. Changes to `.mdx` pages update the preview; press **Ctrl+C** to stop it.

No Gomobile backend, database, or API credentials are needed to preview the documentation.

## Check changes

Before opening a pull request, run:

```bash
mint validate
mint broken-links
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for content guidelines.

For the Markdown copying helper, run `node --test tests/markdown/copy-page.test.cjs`. When changing it, also click both Copy page actions in the local browser and check the clipboard after navigating between pages.

## Gomobile AI plugin

The plugin provides one `gomobile` guidance skill for Codex and Claude Code. It
prepares drafts and explains supplied reports; it has no Gomobile account
connection and requires no Gomobile API key.

Customers install from [Gomobile-Africa/gomobile-plugins](https://github.com/Gomobile-Africa/gomobile-plugins).
The [installation guide](guides/ai-tools/installation.mdx) includes the commands,
installation checks, and a first prompt. No manual clone or ZIP download is needed.

| Location | Purpose |
| --- | --- |
| `guides/ai-tools/` | Customer overview, installation, and examples |
| `plugins/gomobile/` | Plugin manifests, skill, and five reference modules |
| `.claude-plugin/marketplace.json` | Shared Codex and Claude Code catalog |
| `scripts/skills/` | Package builders and customer README templates |
| `tests/skills/` | Package checks, workflow scenarios, fixture, and verification record |
| `dist/` | Generated ZIPs, exports, and local review copies; ignored by Git |

Build and check the package from the repository root with Python 3.10 or newer:

```bash
python3 scripts/skills/build_bundle.py
python3 tests/skills/check_package.py
python3 scripts/skills/export_repository.py
python3 scripts/skills/export_repository.py --check
```

The ZIP builder writes a versioned archive and SHA-256 under `dist/`. The repository
exporter writes only the 12 release files to `dist/public/gomobile-plugins/`, using
the same package inputs and a Git-install README. It does not commit or push.
The public plugin repository has independent history; never copy this authoring
repository or its history into it.

See [plugin maintenance](plugins/gomobile/README.md) and
[verification instructions and results](tests/skills/README.md). Package checks
use temporary client profiles and perform no model turns or Gomobile operations.
Changes to this repository and to the public plugin are reviewed and published
separately. Keep the current 0.2.1 package content fixed pending technical review.

## Publishing changes

Submit changes through a pull request for team review. If this repository and branch are connected to Mintlify, merged changes deploy through that connection. Confirm the deployment branch and status in the Mintlify dashboard.

## Troubleshooting

- **`node` or `npm` not found:** install Node.js and reopen your terminal.
- **CLI missing or outdated:** run `npm install -g mint@latest`.
- **Global installation fails:** use `npx mint@latest dev` to preview without a global install.
- **Preview fails to find pages:** run the command from the folder containing `docs.json`.
- **Search asks you to log in:** run `mint login`, sign in to Mintlify, then restart `mint dev` and refresh the browser. CLI login enables search in the local preview.
- **Port occupied:** run `mint dev --port 3333` and open http://localhost:3333.

For more help, see the [Mintlify installation guide](https://www.mintlify.com/docs/cli/install).
