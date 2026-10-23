# Documentation and product concepts

Bundled notes checked against customer documentation on 2026-10-22. The audience concepts Markdown page was also read publicly on that date. These notes are a dated fallback, not a live fetch or verification of a customer's deployed release.

## Read and identify the source

Open the relevant public page with the client's allowed reading tools. If HTML reading fails, try its `.md` form, for example `https://docs.gomobile.ma/learn/concepts/audiences.md`. This is a documentation URL, not a product endpoint. Do not change network permissions or bypass client restrictions. Report the actual error when access is blocked. A public page may remain accessible through another permitted reader even when one tool fails.

If fetching is unavailable, answer from these bundled notes when they cover the question and label that source mode. Otherwise ask for the relevant public page text. Do not claim to have read full pages or a local checkout when only notes or a link map were read. A public URL citation identifies the underlying source, not proof that you fetched it in this session.

## Basic concepts

- A **contact** holds customer details and custom attribute values. Use actual returned attribute names and types when preparing configuration. See [Contacts](https://docs.gomobile.ma/learn/concepts/contacts).
- A **static audience** has contacts explicitly added or removed. A **live audience** has rule-based membership: contacts enter and leave as they match the conditions. The audience type cannot be changed after creation. For example, a static audience can be a reviewed test list; a live audience can match contacts whose city is Casablanca. This describes membership, not automatic campaign enrollment. See [Audiences](https://docs.gomobile.ma/learn/concepts/audiences).
- A **Voice flow** describes an in-call journey. A **Multichannel flow** can combine conditions, contact changes, tags, SMS, approved WhatsApp templates, and a Voice sub-flow. API type values are `call` and `agnostic`. SMS and WhatsApp are not separate flow types. See [Build a flow](https://docs.gomobile.ma/getting-started/build-first-flow).
- An **audience** selects recipients; a **flow** defines their experience; a **campaign** connects them with campaign settings. Creating a campaign draft does not establish activation. See [Campaigns](https://docs.gomobile.ma/learn/concepts/campaigns).
- A **run** describes automation execution, while a **call** describes a voice leg. A completed run is not proof that someone answered or received a message. See [Runs](https://docs.gomobile.ma/learn/concepts/runs) and [Runs and calls API](https://docs.gomobile.ma/developers/reference/runs-and-calls).

## Find the relevant public pages

Read the relevant page before relying on a contract beyond the bundled notes. These are customer documentation links, not API hosts or tool endpoints.

| Need | Sources |
| --- | --- |
| Product model and supported vocabulary | [Overview](https://docs.gomobile.ma/product/overview), [How Gomobile works](https://docs.gomobile.ma/product/how-gomobile-works) |
| Account and API prerequisites | [Access](https://docs.gomobile.ma/learn/concepts/access), [Authentication](https://docs.gomobile.ma/developers/authentication), [API basics](https://docs.gomobile.ma/developers/api-basics), [Support boundary](https://docs.gomobile.ma/developers/support-boundary) |
| Contacts, custom attributes, imports | [Contacts API](https://docs.gomobile.ma/developers/reference/contacts), [Import contacts](https://docs.gomobile.ma/getting-started/import-contacts) |
| Static and live audiences | [Audiences API](https://docs.gomobile.ma/developers/reference/audiences), [Audience concepts](https://docs.gomobile.ma/learn/concepts/audiences) |
| Voice and Multichannel flows | [Build a flow](https://docs.gomobile.ma/getting-started/build-first-flow), [Flows API](https://docs.gomobile.ma/developers/reference/flows) |
| Campaign preparation and lifecycle | [Launch guide](https://docs.gomobile.ma/getting-started/launch-first-campaign), [Lifecycle](https://docs.gomobile.ma/product/campaign-lifecycle), [Campaigns API](https://docs.gomobile.ma/developers/reference/campaigns) |
| Approved WhatsApp templates | [WhatsApp concepts](https://docs.gomobile.ma/learn/concepts/whatsapp), [WhatsApp API](https://docs.gomobile.ma/developers/reference/whatsapp) |
| AI agents and knowledge bases | [Agents API](https://docs.gomobile.ma/developers/reference/agents), [Knowledge bases API](https://docs.gomobile.ma/developers/reference/knowledge-bases), [AI voice quickstart](https://docs.gomobile.ma/quickstarts/ai-voice-agent) |
| Runs, calls, reports, and errors | [Runs and calls API](https://docs.gomobile.ma/developers/reference/runs-and-calls), [Errors](https://docs.gomobile.ma/developers/errors), [Pagination](https://docs.gomobile.ma/developers/pagination) |
| Audio, inbound routing, and credits | [Audio API](https://docs.gomobile.ma/developers/reference/audio-and-dictionaries), [Inbound API](https://docs.gomobile.ma/developers/reference/inbound), [Credits API](https://docs.gomobile.ma/developers/reference/credits) |
| Consent and customer data | [Responsible use](https://docs.gomobile.ma/product/responsible-use) |

Use **Gomobile**, **Voice flow**, **Multichannel flow**, **contact**, **audience**, **campaign**, **run**, and **call**. A run describes automation; a call describes a voice leg. SMS and WhatsApp are actions in supported flows, not standalone SMS- or WhatsApp-typed flows.
