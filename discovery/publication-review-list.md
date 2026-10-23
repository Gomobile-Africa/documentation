# Open documentation decisions

Internal tracking only. These decisions remain unresolved; wording cleanup and static source checks do not establish release availability, API approval, or runtime verification. Keep this context out of customer pages.

## Release and access

- Confirm deployed release parity and customer availability, including onboarding-generated flows/test calls.
- Confirm support procedures for phone numbers, sender IDs, WhatsApp connection, credits, and recovery.
- Confirm the customer role/permission matrix, member administration, and organization/profile editing.

## API contract

- Confirm the supported endpoint allowlist, including standalone calls, and a customer-only OpenAPI specification.
- Confirm production/staging hosts, resource-ID discovery, calling-policy schemas, and incomplete request/response contracts.
- Confirm endpoint-specific rate budgets, response headers, reset semantics, versioning, compatibility, idempotency, and webhooks.
- Resolve deferred API capabilities in `api-endpoint-review.md`; do not infer support from authentication or Swagger.

## Limits and policy

- Confirm supported import formats, upload/row limits, audio formats/browser support, and provider/model/voice availability.
- Confirm recording defaults and notices, retention, exports, deletion/erasure, processor/data-residency terms, pricing, and service guarantees.
- Confirm customer-configurable schedule/webhook triggers outside the current UI.

## Verification and missing coverage

- Runtime-test onboarding, MFA/recovery, permissions, calls/messages, campaign timing/retries, live enrollment, credits, media/documents, reports/exports, and executable API examples.
- A supplied read-only product review at `develop` commit `9679b35bd5cd992747f4b6f26b05754d24eda399` traced contact/rule reevaluation, live-entry admission while active, re-entry, ignored paused entries, and the absence of a resume catch-up loop. The skill and linked audience/campaign pages now describe those conditions rather than blanket uncertainty. Confirm intended customer-release parity, deployed event/worker configuration, missed-event recovery, and actual runtime outcomes. Do not run real calls, messages, launches, or credit-consuming tests under the skills documentation task.
- Confirm public approval/release availability of Auto-pause/resume settings and conditional knowledge-base attachment/retrieval fields before expanding API schema details. The skill references keep these conditional; source presence is not public contract approval.
- Expand UI guides for contacts/audiences, IVR/DTMF, agents in flows, sub-flows, personalization, transfers/recording, inbound routing, agent/knowledge-base setup, WhatsApp templates, audio/dictionaries, MFA, and report metrics/exports.
- Complete endpoint-specific schemas, asynchronous result states, business errors, and operational recovery instructions.

## Keep unpublished

- Staff/admin/impersonation, provisioning, infrastructure, internal pricing, and credentials.
- Disabled or placeholder Messages, Inbox, Notifications, Help, analytics, contact Insights, and preferred-channel controls.
- Agent Tools & Actions and Policies marked coming soon.
- Knowledge-base archive/groups and embedding/chunk/retrieval tuning.
- Standalone SMS-/WhatsApp-typed flows and actions unavailable in the customer palette.

## Follow-up from the 8 October full-content review

- Source review used `develop` at `3d489063550d618f317ded319b437a55041bbd74`; no remote fetch, deployment verification, or runtime requests were performed.
- Tech lead: decide whether to fix live-audience creation returning zero membership count and import linking counts that do not prove actual additions. Documentation describes the current limitations.
- Confirm standalone calls, agent policy/resolution criteria, model/provider catalogs, recording/export access, and field-level public schemas. The review reported 112 unique operations before catalog normalization; regenerate the candidate inventory for the final review rather than treating that count as approval.
- Verify WhatsApp multilingual deletion, replacement content, creator-phone test routing, async refresh and media readiness with the provider.
- Verify file cleanup/retention separately from successful soft deletion. Keep cleanup failures and contact-window fail-open internals in engineering review.
- Calling-policy API has no separate unrestricted override: null inherits organization hours. Validate the customer UI’s unrestricted option against that behavior. The time validator excludes 24:00 while endpoints are exclusive; verify exact midnight coverage before claiming a continuous overnight example.
- Runtime-test imports/link failures, session expiry, large uploads, live audience changes, each released node, variable propagation, campaigns/timezones/retries/AMD, MFA, agents/inbound, knowledge retrieval, playback/signed URLs, delayed report enrichment, exports, and credit reconciliation.
- Complete flow-node and nested agent schemas, report/export states, import result shapes, and channel-specific recovery. Reserved sub-flow varMapping must not be described as effective; transfer recording defaults need their own customer explanation.
- Expand the task guides with synthetic input, exact settings, paths, expected outcomes, and focused troubleshooting. Do not classify the outlines as end-to-end verified tutorials.
- `.mintignore` now excludes discovery/. Verify exclusions in the deployed build, direct URLs, search, and generated context files before launch; no prior exposure was established.
