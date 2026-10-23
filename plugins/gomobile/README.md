# Gomobile guidance plugin

The first review version is `0.2.1`. It contains one `gomobile` skill shared by
Codex and Claude Code, with no account connection, MCP server, hooks, or executor.
Keep the released instructions and references unchanged pending technical review.

## Package layout

- `plugin.json`: portable Agent Plugins manifest.
- `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`: client compatibility manifests.
- `skills/gomobile/SKILL.md`: skill entrypoint and reference routing.
- `skills/gomobile/agents/openai.yaml`: skill display metadata.
- `skills/gomobile/references/`: five focused product reference modules.

The repository-root `.claude-plugin/marketplace.json` exposes `gomobile@gomobile`
to both clients. Customers install from the separate
[public marketplace](https://github.com/Gomobile-Africa/gomobile-plugins).
See the [customer installation guide](../../guides/ai-tools/installation.mdx).

## Maintain

Keep the name, version, and description aligned across all three manifests.
Keep supporting references inside the skill and reachable from `SKILL.md`.
Update product claims only from reviewed customer documentation or supplied
source evidence; code presence does not establish public availability or
runtime behavior. The [product-source review](../../discovery/gomobile-product-source-review-2026-10-22.md)
records the corrections applied to 0.2.1 and their limits.

Build and export with the commands in the [repository README](../../README.md).
The builders exclude this maintainer README, documentation sources, tests,
internal reviews, and Git history. Generated outputs belong in ignored `dist/`.
The public export has a customer README from `scripts/skills/templates/`.
Publish the exported files separately from this documentation repository.

Run the [package and client checks](../../tests/skills/README.md) after changes.
Use the [workflow scenarios](../../tests/skills/scenarios.md) for model evaluation;
loading a skill successfully does not establish its behavior. Do not run product
operations, real calls/messages, or credit-consuming work for these checks.
