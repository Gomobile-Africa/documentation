# Gomobile skill for Codex and Claude Code

Version 0.2.1 contains one `gomobile` skill with focused references for documentation,
contacts and audiences, flows and campaigns, agents and knowledge bases, and supplied
reports. The plugin provides instructions and notes; it does not connect to your
Gomobile account. No Gomobile API key or private repository access is required.

Extract the complete ZIP, including hidden directories. Keep the extracted
`gomobile-skills` folder in a permanent location. Open a terminal in that folder.

For Codex:

```bash
codex plugin marketplace add .
codex plugin add gomobile@gomobile
codex plugin list --marketplace gomobile
```

For Claude Code:

```bash
claude plugin marketplace add ./
claude plugin install gomobile@gomobile
claude plugin details gomobile
```

Start a new client session. Confirm that the Gomobile plugin is enabled and its
single skill is available as `gomobile:gomobile`.

In Codex, try:

```text
Use $gomobile:gomobile to explain static versus live audiences with documentation sources.
```

In Claude Code, try:

```text
/gomobile:gomobile Explain static versus live audiences with documentation sources.
```

Use the same skill to prepare an audience or campaign and later explain a
sanitized report. It loads the relevant references when needed. Public-page
reading uses your client's allowed tools. If access is blocked, the assistant can
use the dated bundled notes or public text you provide and should identify that
source mode. A private Gomobile checkout is not needed.

All configurations are drafts until applied separately in Gomobile. The skill
does not import, preview account matches, create resources, launch, test, send,
fetch reports, or replay activity. A flow test can perform real work even with
`test: true`. Contact or rule changes can affect live-audience membership; review
campaigns using the audience before applying them. Consequential actions elsewhere
require review and explicit confirmation. Never share API keys.

## Update or remove

Since version 0.2.0, the package replaces the four skills in 0.1.0 with the single `gomobile` skill.
The plugin and marketplace identifier remains `gomobile@gomobile`.

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

Version 0.2.1 corrects source-reviewed guidance from 0.2.0 without changing the skill name.
To update, extract the new ZIP, repeat the installation commands from its
`gomobile-skills` folder, and start a new session. Replace earlier skill invocations
with `$gomobile:gomobile` in Codex or `/gomobile:gomobile` in Claude Code. Extracted
packages do not download updates automatically. Removal changes the AI client,
not Gomobile resources.

Installation tested with Codex CLI 0.160.0 and Claude Code 2.1.304. These are tested
versions, not minimum supported versions or a model-behavior guarantee. ChatGPT
installation has not been verified. Organization policy can restrict installation
and data sharing.

Product documentation: https://docs.gomobile.ma
