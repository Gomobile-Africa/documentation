# Gomobile plugin

One `gomobile` skill for Codex and Claude Code. Understand Gomobile, prepare
contacts and audiences, plan SMS, WhatsApp, Voice, or combined campaigns, prepare
AI agents and knowledge sources, and explain reports you share.

The plugin contains instructions and reference notes. It has no connection to
your Gomobile account, and no Gomobile API key is required. Review drafts before
applying changes separately in Gomobile. Share synthetic data or sanitized reports,
and never include API keys.

## Install

Install Codex or Claude Code, sign in, and check your organization's plugin and
data-sharing policy. Git must be installed so the client can fetch this repository.
Run the commands in your terminal; no manual clone or ZIP extraction is needed.

### Codex

```bash
codex plugin marketplace add Gomobile-Africa/gomobile-plugins
codex plugin add gomobile@gomobile
codex plugin list --marketplace gomobile
```

Start a new session with `codex`, then try:

```text
Use $gomobile:gomobile to explain static versus live audiences with documentation sources.
```

### Claude Code

```bash
claude plugin marketplace add Gomobile-Africa/gomobile-plugins
claude plugin install gomobile@gomobile
claude plugin details gomobile
```

Start a new session with `claude`, then try:

```text
/gomobile:gomobile Explain static versus live audiences with documentation sources.
```

Confirm that the plugin is enabled and the single skill `gomobile:gomobile` is
available. The assistant should explain whether it read public documentation,
bundled reference notes, or text you supplied. The notes may be older than the
published documentation; public-page reading uses your client's permitted tools.

Version **0.2.1**. Installation compatibility is checked with Codex CLI **0.160.0**
and Claude Code **2.1.304**; these are tested versions, not minimum requirements.
This Git marketplace is separate from the official plugin directories. ChatGPT
installation and model behavior on every client surface are not established by
CLI package checks.

## Try a workflow

```text
Use $gomobile:gomobile to plan an appointment-reminder campaign using WhatsApp.
List the required contact attributes, template variables, audience settings,
schedule, and channel prerequisites. Identify missing information.
Prepare a plan only; do not create, test, or launch resources.
```

In Claude Code, replace `Use $gomobile:gomobile` with `/gomobile:gomobile`.
You can continue the conversation with a sanitized report obtained separately in
Gomobile. The plugin does not fetch private reports or execute account operations.
Testing a flow separately in Gomobile can send real messages, place calls, change
data, and consume credits, including when `test: true` is used.

## Update or remove

To replace a previous local/ZIP installation or update this installation, remove
the plugin and marketplace using the commands below, repeat the installation
commands, and start a new session. Update the marketplace source before expecting
new files; restarting a session alone does not download an update.

For Codex:

```bash
codex plugin remove gomobile@gomobile
codex plugin marketplace remove gomobile
```

For Claude Code:

```bash
claude plugin uninstall gomobile@gomobile
claude plugin marketplace remove gomobile
```

Versions 0.2.0 and later use one skill instead of the four skills in 0.1.0.
Use `$gomobile:gomobile` or `/gomobile:gomobile` for all Gomobile workflows.
Removal changes your AI client's installation; it does not change Gomobile resources.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Marketplace download fails | Check Git installation, GitHub connectivity, and organization policy |
| `plugin` command is unavailable | Check your client version and its plugin documentation |
| Plugin is not found | Add the marketplace first, then use `gomobile@gomobile` |
| Old skill names are still shown | Remove the old installation and marketplace, reinstall, and start a new session |
| Assistant cannot read documentation | Allow a documentation-reading tool or provide relevant public page text |

Product documentation: [docs.gomobile.ma](https://docs.gomobile.ma).
Client instructions: [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins)
and [Claude Code plugins](https://code.claude.com/docs/en/discover-plugins).
