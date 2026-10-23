# Prepare agents and knowledge bases

Bundled guidance updated on 2026-10-22 using customer documentation and a product-source review. Sources: [AI voice agent quickstart](https://docs.gomobile.ma/quickstarts/ai-voice-agent), [Agents API](https://docs.gomobile.ma/developers/reference/agents), and [Knowledge Bases API](https://docs.gomobile.ma/developers/reference/knowledge-bases). Source findings do not establish public approval of every field, deployed-release parity, or provider availability.

## Prepare an agent

Establish the intended task, language, organization/environment, answer scope, escalation expectations, and knowledge sources. Draft the agent name and instructions, including what to do when evidence is missing. Separate proposed instructions from saved agent configuration. Do not invent a tool, policy feature, provider/model/voice choice, or phone-number binding.

- Agent endpoints accept Admin, Manager, and Agent API-key roles, subject to organization access. No key is needed for this guidance.
- `POST /agents` requires a name and instructions; description is optional. Omitted pipeline, memory, and operational configuration uses platform defaults. Read supplied returned configuration rather than copying example provider defaults into a new promise.
- Custom pipelines need currently available identifiers from the documented `/agents/options/*` routes. Prepare a request or UI checklist; do not fetch those account catalogs through this skill.
- Creation can produce an active but unpublished agent. Active status and inbound publication are separate. Publishing reconciles an exact set of eligible phone-number IDs and changes live inbound routing; activation or restoration does not establish publication.
- `POST /agents/:id/test` is a text playground operation, not a phone call. It can invoke paid providers and expose submitted text. Prepare synthetic test questions and expected answer criteria; do not perform the test. Voice flow tests can place real calls.

Deliver draft instructions, required knowledge and language/provider facts, known/missing IDs, intended usage context, and separate verification steps for saved configuration, knowledge readiness, testing, and any later publication. A campaign or flow referencing an agent still needs its own review; do not infer that agent publication is required for every usage path.

## Prepare a knowledge base

Identify the intended approved documents and the agent that will use them. Use synthetic examples or minimal sanitized excerpts. Propose a name, description, source inventory, access/retention review, and verification questions. A local document is not an uploaded or indexed document.

- Knowledge-base endpoints accept Admin, Manager, and Agent API-key roles. `POST /knowledge-bases` requires a name; description is optional. Read returned processing configuration instead of promising a fixed embedding provider or model.
- Document upload stores and processes the file. A successful `202` means accepted, not ready. Do not promise retrieval quality from upload success.
- Processing can include `uploading`, `waiting_for_scan`, `processing`, and `ready`; `failed` and `blocked` are terminal problems. A later authorized reader should back off and stop at `ready`, `failed`, or `blocked`, rather than poll indefinitely. This skill does not upload or poll.
- Reprocessing is a separate operation for failed documents. A scan-blocked document cannot be reprocessed. Request only the supplied status and failure facts needed to propose recovery.
- Deletion is destructive; a knowledge base still attached to an agent returns `409`. Identify dependencies without automatically detaching agents or deleting documents. Successful deletion does not prove complete erasure of all stored copies.

Before proposing agent attachment, verify the current documented configuration schema and actual IDs. If unavailable, provide UI preparation steps and keep the binding unresolved rather than inventing JSON. Once a customer supplies results, inspect document status and answer evidence separately from assumptions about agent behavior.

If included in the approved customer contract and the actual knowledge-base ID is supplied, attachment uses `knowledgeBaseConfig.knowledgeBaseId`. This draft agent-update fragment illustrates the field; replace the placeholder only with the supplied real ID after verifying the released schema:

```json
{
  "knowledgeBaseConfig": {
    "knowledgeBaseId": "<supplied-knowledge-base-id>"
  }
}
```

Optional retrieval settings include `topK` and `similarityThreshold` when approved by that contract. Use documented values rather than inventing tuning. A saved attachment does not prove that documents are ready or that answers are grounded correctly. Leave the binding unresolved when the schema or ID is missing.
