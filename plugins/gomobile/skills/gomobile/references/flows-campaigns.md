# Campaign and flow preparation

Bundled guidance updated on 2026-10-22 using customer pages and a product-source review. Source-supported implementation paths do not establish deployed-release parity, event reliability, or public contract approval. Read the customer's released contract for the requested workflow.

## Prepare the workflow

Establish the goal, organization/environment, channel choice, consent/opt-out requirements, audience type, and success measure. Carry forward verified attributes, audience rules, and known IDs from an earlier draft. Choose Voice for an in-call journey or Multichannel for SMS, WhatsApp, conditions, contact updates, and a Voice sub-flow. Do not silently choose a different channel or change the audience; identify recommendations as proposals.

Outline branches, required contact values, and failure paths. List missing sender/caller resources, saved flow/audience IDs, approved template details, and agent/knowledge-base or audio readiness when relevant. Use a UI plan when the node schema is incomplete; do not present an outline as executable graph JSON. Do not assume per-contact appointment scheduling, multiple-appointment storage, automatic opt-out handling, or duplicate prevention exists merely because the business plan needs it. Identify the mechanism that still needs verification.

Prepare message-variable mappings using the actual approved template's order. Keep unknown IDs and approval evidence missing. Review schedule/timezone, hours, retries, recording and consent where applicable, and credit scope. A template test or flow test is real work; prepare a controlled-recipient test plan without performing it.

Deliver a draft plus a launch-review block with the exact organization, resources, targets or selection rules, content, timing, side effects, missing information, and verification steps. A saved draft, confirmation of a plan, and confirmation to launch are distinct. An initial preview count alone does not establish a maximum send count or cost.

## Flows

Sources: [Build a flow](https://docs.gomobile.ma/getting-started/build-first-flow), [Flows API](https://docs.gomobile.ma/developers/reference/flows).

- Voice maps to `call`; Multichannel maps to `agnostic`. Type is immutable. Do not create standalone SMS- or WhatsApp-typed flows.
- Only Multichannel flows invoke Voice sub-flows. Documented `invoke_sub_flow.varMapping` currently has no effect; do not rely on it to isolate sensitive variables.
- A graph needs a valid start node, known nodes, supported configuration, and connected outputs. The public reference does not provide every node's complete configuration schema. Prefer an explicit UI plan to guessed graph JSON.
- Updating a flow should use `expectedHash` from the loaded version. `409` means reconcile the latest graph; do not overwrite blindly.
- `GET /flows/:id/run-inputs?contactId=...` is an advisory read of contact inputs. It is not execution validation or a guarantee against later failure or channel activity.
- `POST /flows/:id/run` can call, message, update data, and consume credits even with `test: true`. That field labels the run `manual_test`; it is not dry-run mode.
- Voice `forward.record` defaults to enabled when omitted, independently of full-call recording. Make recording choices explicit; do not promise variable isolation or recording defaults beyond what is documented.

## Campaigns

Sources: [Campaigns API](https://docs.gomobile.ma/developers/reference/campaigns), [Campaign lifecycle](https://docs.gomobile.ma/product/campaign-lifecycle).

Documented flow and campaign operations accept Admin, Manager, and Agent API keys; organization services and referenced-resource availability still apply. The package needs no key because it does not execute them.

- `POST /campaigns` requires `name`, `flowId`, and `audienceId`; creates a draft without enrollment. Voice requires `dialConfig`; Multichannel may need it for a Voice sub-flow. Use verified organization resource IDs, not invented discovery endpoints.
- Draft updates use `PATCH /campaigns/:id`; flow and audience bindings are immutable. Preparing or saving a draft does not confirm its launch.
- Review caller numbers, explicit recording choice, schedule, calling hours, retries, consent, and credits. Eligible Voice campaigns support fixed-delay or scheduled retry policies. Do not assume Voice retry policies apply to Multichannel campaigns.
- Schedule timestamps need `Z` or an offset. Absent or past `startAt` can produce immediate activation. Use deliberate future dates and review the displayed organization timezone.
- A supplied `callingPolicy` replaces the entire default policy; omitted weekdays are closed. Omitted or `null` policy inherits the organization default at activation, not unrestricted hours. Later organization changes do not alter the stamped policy. Hours govern initiation and do not end a live call or establish legal compliance.
- Actual activation enrolls the audience's current members; a future scheduled campaign has not performed that initial enrollment yet. While a campaign is active, new live-audience entries can admit additional executions, including re-entry after an exit. Paused campaigns ignore entry events; resuming does not automatically catch up missed entries. A preview count is neither a fixed send limit nor proof of enrollment. Verify actual executions rather than promising admission or delivery from an event path.
- Pausing holds pending campaign work, including queued retries, while the campaign remains paused. Work already picked up or running can continue; pause does not undo activity already performed. Resuming allows held work to become eligible again, subject to calling hours, deadlines, and other campaign checks.
- Stop is terminal, cancels pending campaign work, and lets in-progress calls finish. Cancelling an individual run can hang up its live call; these are distinct operations.
- When the released interface provides Auto-pause, record the selected flow step, threshold, and counter-reset behavior. Inspect a paused campaign's pause reason before proposing recovery. Resuming can require resolving a reached threshold, credit condition, or elapsed stop time; do not assume every paused campaign can simply resume. A threshold is not a guaranteed maximum send count: work already running can continue. Do not invent Auto-pause API fields or assume public availability from source presence.

## WhatsApp

Sources: [WhatsApp concepts](https://docs.gomobile.ma/learn/concepts/whatsapp), [WhatsApp API](https://docs.gomobile.ma/developers/reference/whatsapp).

The organization needs an available channel and an approved template for supported sends. Record template ID, name, language, approval evidence, and ordered variables. Approval does not establish recipient consent. Status refresh is asynchronous. Template resubmission replaces revisable content; preserve optional content intentionally. Deletion removes all language variants with the same name.

The template test uses the organization creator's verified number and fallback values; it does not accept an arbitrary recipient or variable overrides. It sends a real message and can incur charges. A returned `messageId` does not prove delivery. This skill does not perform template tests, submissions, refreshes, or uploads.

## Expected result and troubleshooting

A prepared campaign consists of a reviewable draft plus missing prerequisites; it has no campaign ID until the user creates it in Gomobile. Verify actual saved configuration before activation. For missing inputs, inspect contact values and reachable sub-flows; for unapproved templates, review channel/approval state; for `402`, review credits with Gomobile; for `409`, inspect current state. After a timed-out mutation, check state before retrying. See [Errors](https://docs.gomobile.ma/developers/errors).
