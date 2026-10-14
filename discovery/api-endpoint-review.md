# Deferred and excluded API routes

Internal inventory, based on the 1–2 October 2026 source reviews of `develop` at `3d489063`. This is not a public endpoint allowlist. Current implementation, publication support, and runtime behavior must be checked separately.

The customer reference lists documented operations. This file retains only capabilities not intended for that reference. Shared unresolved decisions are tracked in `publication-review-list.md`.

## Resource discovery requiring a contract decision

- `GET /dids/available`, `GET /dids/by-ids`: phone-number selection/query and response contract.
- `GET /sender-ids/available`: sender selection and response contract.
- `GET /flows/voices/tts`: provider catalog and stability policy.

## Deferred capabilities

| Capability | Open question |
| --- | --- |
| Agent conversation and resolution routes | Customer availability, lifecycle, privacy, and provider usage |
| Flow audio/TTS preview routes | Supported input/output contract and usage costs |
| `GET /credits/transactions` | Customer-safe response without internal operator attribution; security and commercial scope |
| `POST /sms/send`, `POST /sms/send-to-contact` | Public messaging scope, consent, sender setup, and usage |
| SMS-program routes | Public availability and terminology; no corresponding customer UI established |
| `POST /otp/send` | Identity/security policy and public integration scope |
| Invitations/team/member routes | Customer administration scope and permission contract |

## Excluded from the customer API reference

- Staff/admin/impersonation, health, infrastructure, and operational routes.
- DID/sender/channel provisioning and provider credentials.
- General inbound-binding CRUD, including `POST /did-bindings`, `GET /did-bindings`, and `DELETE /did-bindings/:didId`.
- Recording download routes and `POST /otp/verify`.
- API-key management through another API key.
- Unfiltered runtime Swagger output.

Machine-access eligibility or code presence does not establish public support. Resolve the endpoint allowlist before publication; verify approved examples with synthetic data and controlled resources.
