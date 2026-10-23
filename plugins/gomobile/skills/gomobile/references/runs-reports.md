# Runs, calls, reports, and recovery

Bundled guidance updated on 2026-10-22 using customer documentation and a product-source review. Source findings are not deployed-release or runtime verification. Recheck the customer's released contract before proposing requests. These paths describe possible reads by the customer, not operations performed by this package.

## Work from supplied evidence

Identify whether the evidence is a run, call leg, campaign aggregate, per-contact result, or error. Ask only for the missing sanitized fields needed to resolve the question, such as status, typed failure, relevant node facts, and polling interval. Do not request keys, complete contact exports, recordings, transcripts, signed URLs, or unrelated private variables. If the user only supplies an ID and asks to get its report, explain that this package cannot fetch account data; propose the narrowest documented report to obtain separately.

Separate observed facts, likely causes, and missing evidence. Reconstruct the last confirmed event without assuming the plan was executed or linking a report to it without matching identifiers. Explain what a useful later result would establish. For a proposed read, give its method, path, scope, permissions, data exposure, and any relevant stopping condition, clearly labeled as not performed. Do not query, poll, replay, cancel, or resume through this skill.

## Choose evidence at the right level

Sources: [Runs and calls API](https://docs.gomobile.ma/developers/reference/runs-and-calls), [Flows API](https://docs.gomobile.ma/developers/reference/flows), [Campaigns API](https://docs.gomobile.ma/developers/reference/campaigns).

| Evidence | Meaning and proposed verification |
| --- | --- |
| Run | Automation execution, node runs, direct children, own call leg, messages, variables subject to access, and cost. Proposed read: `GET /flows/executions/:id`. |
| Call | One voice leg, outcome/reason, technical timeline, recording metadata, and cost. Proposed read: `GET /calls/:id`. A run can involve more than one leg or child. |
| Campaign aggregate | Snapshot of campaign activity. Proposed read: `GET /campaigns/:id/report`; distinguish `not_started`, `computing`, and `ready`. |
| Campaign contacts | Per-contact outcomes collapse retry chains to the latest attempt. Proposed read: `GET /campaigns/:id/report/contacts`. |
| Node funnel | Counts executions reaching flow steps, rather than unique contacts; retries or repeated admissions can contribute additional runs. Distinguish this from the contact-level funnel inside a campaign report. Confirm the endpoint and denominator before comparing figures. Reads can enqueue snapshot computation. |

Documented run/call/campaign reads accept Admin, Manager, and Agent API keys, subject to organization scope, enabled services, and field-level access. This plugin neither receives credentials nor performs the reads. Supplied reports may contain personal data: summarize minimally and omit signed download links and private variables.

## Filters and settlement

- `GET /executions` scopes by `flow`, `contact`, `campaign`, or `binding`. The flow-specific `GET /flows/:id/executions` uses `contactId` instead of `contact`.
- Manual tests are hidden by default in the organization list. Use `includeTests=true` or an explicit `triggeredBy=manual_test` filter when preparing a relevant read.
- Lists generally use `page`/`limit` with `{ data, meta }`; contact interactions instead use `meta.nextCursor`. Use endpoint-specific pagination rather than guessing.
- Run reports return `nextReadInMs`. A later authorized reader should wait at least that duration. Stop automatic reads at `null`; it settles this execution and own leg, not all children or enrichments. Inspect relevant child runs separately when needed.
- Campaign snapshot fields can include `asOf`, `final`, `refreshing`, and `nextReadInMs`. Do not treat `computing` as an empty result or an old `asOf` as current. Follow that endpoint's polling contract and tolerate unfamiliar states.
- A message ID is not delivery proof. A completed automation is not proof of an answered or successful voice interaction. Automated transcripts can be inaccurate.
- Treat costs in a partial report as the supplied snapshot only. A partial synthetic excerpt showing zero cost does not establish zero final usage or charges.

## Error interpretation

Sources: [Errors](https://docs.gomobile.ma/developers/errors), [API basics](https://docs.gomobile.ma/developers/api-basics).

Prefer top-level `code` and structured `fieldErrors`/`fieldDetails` to human-readable wording. `401` suggests credential validity/lifecycle; `403` suggests role or enabled services. Ask for masked diagnostic facts, never the credential. `404` can reflect organization scope as well as absence. `409` requires state/conflict review. `402 INSUFFICIENT_CREDITS` requires reviewing balance and arranging credits through Gomobile, not repeated launch attempts. `429` requires respecting returned `Retry-After` in a later authorized reader.

For a timed-out mutation, do not recommend immediate replay. Determine whether the original resource/run exists and what activity occurred. No general idempotency guarantee is documented. A `POST` can duplicate work; a bulk upsert's HTTP success can contain failures. Stop recovery planning when evidence cannot establish the affected scope, and request only the missing sanitized facts.
