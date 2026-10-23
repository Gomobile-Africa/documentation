# Product-source review applied to skill 0.2.1

Internal provenance record. The user supplied a read-only review from the Gomobile product repository on 2026-10-22. Reported product branch: `develop`; commit: `9679b35bd5cd992747f4b6f26b05754d24eda399`; working tree: clean. The reviewer inspected source and existing tests without executing them, installing the plugin, evaluating a model, or performing product operations. This documentation agent applied the supplied findings; it did not independently inspect that product checkout or verify deployed/runtime behavior.

The reviewed baseline was skill/plugin **0.2.0**. The reviewer reported all 17 source snapshots and all 12 ZIP members matched, including ZIP SHA-256 `d11e0bd4e3257c284069dd2c4dedfc862e3547c539ceaa09ec23d61807a2e817`. The original ZIP and full source-review snapshots remain local, generated review artifacts under ignored `dist/`; they are not required to build or test the current package. Corrections are packaged separately as **0.2.1**.

## Applied findings and supplied evidence

### 1. Pause holds pending work

Changed the flow/campaign reference, scenario 7, Campaigns API, and campaign lifecycle page. Pending work, including queued retries, is held while paused; work already picked up/running can continue. Resume makes held work eligible subject to hours, deadlines, and campaign checks. Stop and individual-run cancellation remain distinct.

Supplied evidence: `apps/backend/src/platform/campaign/campaign.service.ts:758`; `apps/backend/src/platform/outbound-call-queue/outbound-call-queue.repository.ts:230`; `apps/backend/src/platform/flow/flow-execution.repository.ts:1572` and `:1632`. The review cited outbound queue integration coverage at `apps/backend/src/platform/outbound-call-queue/__tests__/outbound-call-queue.int-spec.ts:435`, inspected rather than executed. Source-supported behavior, not a reproduced dispatch result.

### 2. State-specific live-entry admission

Replaced blanket enrollment uncertainty in the contacts/audiences and flows/campaigns references. Actual activation enrolls current members. Active live-entry events can create executions; already-matching membership is not itself another entry, while exit/re-entry can admit again. Paused entries are ignored and resume has no identified automatic catch-up loop. Static membership methods do not emit the inspected live-entry events. No guarantee of event recovery, one send per contact, particular enrollment, or delivery was added.

Supplied evidence: `apps/backend/src/platform/audience/live-audience/live-audience.listener.ts:39`; `apps/backend/src/platform/audience/audience.service.ts:279`; `apps/backend/src/platform/audience/live-audience/services/live-audience.service.ts:67`; `apps/backend/src/platform/campaign/flow-audience.listener.ts:53`; `apps/backend/src/platform/campaign/campaign.repository.ts:459`; `apps/backend/src/platform/campaign/campaign.service.ts:1162` and `:814`. Inspected listener coverage: `apps/backend/src/platform/campaign/__tests__/flow-audience.listener.spec.ts:247`.

The main skill and linked audience/campaign pages now use the same conditions. The short customer warning to review campaigns using an audience remains.

### 3. Preview data exposure

The contacts reference and Audiences API now describe `count` plus up to 50 most recently created matching contacts, with `contacts: null` in the restricted no-contact-PII branch. The response example illustrates that restricted shape without inventing a full contact DTO. The root skill, usage page, and scenarios request count only when contact records are unnecessary. Preparing a body does not obtain data; preview does not create an audience/change membership.

Supplied evidence: `apps/backend/src/platform/audience/dto/preview-audience.dto.ts:40`; `apps/backend/src/platform/audience/audience.service.ts:44`; inspected unit coverage at `apps/backend/src/platform/audience/audience.service.spec.ts:194`.

### 4. Funnel grain

The runs/reports reference and Campaigns API distinguish run-grain node funnels from the contact-grain funnel in a campaign report. Retries/repeated admission can contribute additional runs. Confirm endpoint, scope, and denominator before comparing; no invented report totals or aggregation guarantees.

Supplied evidence: `apps/backend/src/platform/funnel-report/funnel-report.controller.ts:102`; `apps/backend/src/platform/campaign-report/campaign-contact-outcome.ts:50`; `apps/backend/src/platform/funnel-report/funnel-rows.repository.ts:143`. Tests were inspected, not run.

### 5. Conditional Auto-pause recovery

Added flow/campaign guidance for released UI configurations: selected step, threshold, counter-reset behavior, pause reason, credit condition, and elapsed stop time. Running work can continue, so a threshold is not a maximum-send guarantee. No Auto-pause API schema or unconditional public availability was introduced.

Supplied evidence: `apps/web/messages/en.json:3663`; `apps/web/src/app/dashboard/(shell)/campaigns/_components/wizard/throttle-fields.tsx`; `apps/backend/src/platform/campaign/campaign.service.ts:879`; `apps/backend/src/platform/campaign/campaign-lifecycle.service.ts:101`. Public contract approval remains unresolved.

### 6. Contact fields, phone handling, and mapping

Added compact standard fields, zero-based column mapping, and the distinction between contact-write Moroccan canonicalization, stricter Moroccan import validation, and channel reachability. The three-column mapping is explicitly an array rather than a complete validation request; real layout/header/session/attribute facts remain necessary. A request field does not imply a released UI control.

Supplied evidence: `apps/backend/src/platform/contact/dto/create-contact.dto.ts`; `apps/backend/src/platform/contact/dto/update-contact.dto.ts`; `apps/backend/src/platform/contact/phone-utils.ts`; `apps/backend/src/platform/contact/ingestion/ingestion-validator.service.ts:78`.

### 7. Conditional knowledge attachment

Added the `knowledgeBaseConfig.knowledgeBaseId` fragment only when the field belongs to the approved customer contract and a real ID is supplied. Optional `topK`/`similarityThreshold` values remain dependent on that contract; no tuning defaults or ranges were invented. Attachment, ready documents, and grounded answering remain separate checks. No expanded public Agents API schema was asserted.

Supplied evidence: `apps/backend/src/platform/agent-studio/dto/create-agent.dto.ts:257`; `apps/backend/src/platform/agent-studio/dto/update-agent.dto.ts:99`; `apps/backend/src/platform/agent-studio/services/agent-studio.service.ts:87`. Public approval/release availability remains unresolved.

### 8. Stage the partial synthetic fixture

Scenario 6 now copies/attaches `tests/skills/fixtures/run-report.json` into the isolated test workspace and gives its actual staged path. The JSON remains intentionally partial and synthetic, not a complete API-response example. Tests do not depend on finding the private checkout. Zero costs in this partial excerpt do not prove zero final usage/charges; the report reference and acceptance criteria now make that explicit.

Supplied evidence: the reviewed fixture/ZIP inventory and `apps/backend/src/platform/flow-report/types.ts:99`. The existing settlement caveat remains supported by the review's `apps/backend/src/platform/flow-report/report-assembly.ts:56` reference.

## Scope and remaining evidence

The one-skill structure, source-mode handling, no-account-execution boundary, continuity rules, correct request bodies, and existing examples were preserved. The installation title now says “Install the Gomobile plugin.” Focused changes to three linked public product pages prevent them from repeating the old pause/preview/funnel claims when the skill reads its sources. No product source was changed.

Product runtime, release parity, provider delivery/charges, event recovery, public approval of conditional fields, and fresh 0.2.1 model behavior remain unverified. The expanded manual scenarios are a plan, not passed evaluations. Current package and Git-marketplace installation results are recorded in [the verification record](../tests/skills/README.md). The public Git marketplace is the customer installation route; a hosted ZIP is not required. These source findings do not authorize product operations or establish deployed behavior.
