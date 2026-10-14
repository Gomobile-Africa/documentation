# Contributing

Write customer documentation in English using Gomobile terminology: contacts, static/live audiences, flows, campaigns, runs, calls, inbound bindings, and credits.

## Verify content

- Check the target release’s customer UI in `apps/web` and behavior in `apps/backend`. Treat the Gomobile repository as read-only.
- Verify permissions, request/response shapes, errors, prerequisites, and side effects. Test workflows when source inspection alone cannot establish the result.
- Document customer-facing features. Keep internal, private, disabled, and unreleased capabilities out of customer pages.
- Record unknown release, API, or policy decisions in `discovery/publication-review-list.md`. Code presence alone does not establish public support.
- Do not invent limits, pricing, retention, compliance, or compatibility guarantees.

## Write useful pages

Task pages should explain the outcome, prerequisites, numbered steps, expected result, limitations, troubleshooting, and next task. Keep labels aligned with the English UI.

Use synthetic data and test numbers you control. Never expose customer data or credentials. Screenshots need meaningful alt text and written instructions.

API examples must match the documented endpoint, use server-side `X-API-Key` authentication, and identify calls, messages, data changes, or credit use. Use the API host supplied by Gomobile; never infer support from raw Swagger or successful authentication.

## Validate changes

```bash
mint validate
mint broken-links
```

Check changed workflows, headings, examples, mobile layout, keyboard access, and contrast as relevant.
