# Contact and audience preparation

Bundled guidance updated on 2026-10-22 using customer documentation and a product-source review. Source-supported implementation paths do not establish deployed-release parity, event reliability, or public contract approval. Recheck the customer's released contract before preparing an executable integration. Paths below are request specifications, not requests to run.

## Prepare the requested change

Establish whether the user needs a column mapping, a request body, or UI steps. Identify the intended organization/environment without requesting credentials. Distinguish contact creation, partial update, bulk upsert, and file import. For updates, show changed fields and fields to clear. Verify attribute definitions, types, enum values, and returned names; missing definitions are missing information, not permission to create them.

For imports, flag duplicates, invalid rows, and existing-contact update candidates. Local sample review is separate from server validation and execution; uploading transfers customer data. Prepare static membership with explicit organization contact IDs, and live membership with the documented rule tree and a proposed preview. Do not invent a preview count or treat it as a permanently fixed audience.

## Contacts and attributes

Source: [Contacts API](https://docs.gomobile.ma/developers/reference/contacts).

- Documented contact and custom-attribute operations accept organization Admin, Manager, and Agent API keys; enabled services still apply. Only owners and administrators manage keys in the customer UI. A UI member role and an API-key role are separate concepts.
- Common standard fields include `primaryPhone`, `firstName`, `lastName`, `fullName`, `primaryEmail`, `address`, `city`, `state`, `zip`, `occupation`, `preferredChannel`, and `gender`. Check the current customer contract for field constraints; a request field does not establish that a corresponding UI control is released.
- `POST /contact` requires `primaryPhone`; a duplicate primary phone returns `409`. Inspect `contact.id` and `attributeErrors`; a contact can be created while some attributes fail.
- `PUT /contact/:id` is partial: omitted fields remain, nullable optional fields can be cleared with `null`, and primary phone cannot be cleared.
- `POST /contact/upsert` takes `{ "data": [...] }` and matches by primary phone. Inspect `successCount`, `failureCount`, and `failures`; prepare corrections only for failed entries rather than replaying the entire batch.
- `GET /custom-attributes` discovers definitions. Supported types are `text`, `number`, `boolean`, `date`, `phone_number`, `email`, `url`, and `enum`. A contact's `customAttributes` request is a map keyed by the definition's returned `name`. Do not infer that name solely from its display label.
- Attribute deletion removes the definition and values. `409 CUSTOM_ATTRIBUTE_IN_USE` can include dependent flows in `meta.flows`; report these dependencies rather than proposing deletion of the flows automatically.

For imports, also read [Import contacts](https://docs.gomobile.ma/getting-started/import-contacts). The documented server workflow is upload, validate mappings, review paged validation results, then execute. Mappings use zero-based column indices. Exactly one column maps to `primaryPhone`; custom fields use `custom.<returnedName>`. Duplicate phones in the file are validation errors; existing contacts are update candidates. Contact writes canonicalize recognized Moroccan phone formats; that is separate from the stricter Moroccan validation used by imports. Acceptance of another phone string does not establish channel reachability or international import support. A successful linking count alone does not establish actual new static-audience membership: verify the members after import.

For synthetic columns `primaryPhone`, `city`, `customer_tier` in that order, the draft mapping array is:

```json
[
  { "column": 0, "field": "primaryPhone" },
  { "column": 1, "field": "city" },
  { "column": 2, "field": "custom.customer_tier" }
]
```

This is not a complete validation request. The actual CSV layout, header-row choice, ingestion session ID, and verified attribute definition are still needed.

## Audiences

Source: [Audiences API](https://docs.gomobile.ma/developers/reference/audiences).

- Admin, Manager, and Agent API keys can use the documented audience endpoints. Audience type is immutable: choose `static` or `live` at creation.
- `POST /audience/:id/add-contacts` and `/remove-contacts` take `{ "contacts": ["<contact-uuid>"] }` for a static audience. Deleted, outside-organization, or already-present contacts can be skipped when adding; inspect returned counts and verify membership. Malformed request values still require schema validation.
- Live rules use `group` nodes with `AND` or `OR` and `children`. Conditions use `attributeName`, `operator`, and a value when the operator takes one. The maximum depth is three, counting groups and conditions.
- Supported operators: `equals`, `not_equals`, `is_empty`, `is_not_empty`, `gt`, `gte`, `lt`, `lte`, `contains`, `not_contains`. Select operators compatible with the attribute type. Empty/nonempty checks omit `value`.
- `POST /audience/preview` takes `{ "rules": <rule-group> }`. It does not create an audience or change membership. The result contains `count` and up to 50 most recently created matching contacts; the restricted no-contact-PII response has `contacts: null`. Preparing the body does not obtain a count. For count-only analysis, ask the customer to share the count without the contact records.
- Live creation can report `contactCount: 0` even when matches exist. Verify with `GET /audience/:id` or `/audience/:id/contacts`.
- Contact changes, imports or bulk upserts, and live-rule edits can cause contacts to enter a live audience. For an active campaign using that audience, entry events can create new campaign executions. A contact that exits and re-enters can be admitted again; do not promise one send per contact. Events received while a campaign is paused are not admitted, and resuming does not by itself replay missed entries. These are implementation paths, not proof that a particular contact was enrolled or reached; verify supplied campaign or run evidence.
- Reevaluating a contact that still matches an already-active membership does not itself create another entry transition. Static membership edits do not emit the inspected live-entry events; do not infer the same post-launch admission behavior for a static audience. Review campaigns using the audience before proposing contact or rule changes.
- Deletion is blocked while non-deleted campaigns reference the audience; check `linkedCampaignsCount`.

Example preview body, **prepared only**, assuming a verified text attribute named `customer_tier`:

```json
{
  "rules": {
    "type": "group",
    "operator": "AND",
    "children": [
      { "type": "condition", "attributeName": "contact.city", "operator": "equals", "value": "Casablanca" },
      { "type": "condition", "attributeName": "custom.customer_tier", "operator": "equals", "value": "test" }
    ]
  }
}
```

## Verification and recovery

Record missing schema/IDs as missing information. After a user performs an operation, inspect the provided result for partial errors, skipped entries, and actual membership before suggesting follow-up work. For `401`/`403`, refer to [authentication](https://docs.gomobile.ma/developers/authentication); for validation or state conflicts, use the returned `code` and [errors](https://docs.gomobile.ma/developers/errors). A timed-out mutation is ambiguous: check its result before retrying to avoid duplicate work.
