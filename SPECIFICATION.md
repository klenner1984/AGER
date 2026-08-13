# AGER Specification v0.1-draft

## 1. Purpose

The Agent Governance & Evidence Record (AGER) defines a portable record for describing an AI agent's operational identity, ownership, capabilities, access, controls, changes and evidence.

AGER does not determine whether a deployment is legally compliant. It records facts and evidence that can support governance, security, audit and incident-response processes.

## 2. Conformance language

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT and MAY indicate requirement strength within this draft.

## 3. Record identity

Every AGER record MUST contain:

- `ager_version`
- `record_id`
- `agent`
- `ownership`

A record SHOULD contain creation/update timestamps and an environment identifier.

## 4. Agent identity

`agent` describes the governed AI workload. It SHOULD include:

- stable `agent_id`
- human-readable `name`
- `purpose`
- provider and model information where known
- deployment environment
- autonomy level

AGER v0.1 defines autonomy levels A0 through A4.

## 5. Ownership

Each production agent SHOULD identify:

- business owner
- technical owner
- governance owner where applicable

Owners may be roles rather than personal names to reduce unnecessary personal-data duplication.

## 6. Access

The `access` object records resources available to the agent, including APIs, MCP servers, databases, file stores, communication systems and credentials/scopes.

Write capability SHOULD be explicitly identified.

## 7. Data

The `data` object describes categories of information the agent can receive, retrieve, transform or disclose. Organizations SHOULD identify personal, confidential and otherwise sensitive categories where relevant.

## 8. Actions and boundaries

The `actions` object SHOULD distinguish permitted and prohibited actions and MAY define monetary, publishing, execution or other operational limits.

## 9. Human control

The `human_control` object records approval requirements, escalation paths, override mechanisms and kill-switch availability.

## 10. Transparency evidence

The `transparency` object records whether AI disclosure is required or implemented and references evidence supporting the recorded state. Legal applicability is intentionally not inferred by the schema.

## 11. Security controls

The `security` object records operational controls such as tool restrictions, network restrictions, credential scoping, monitoring and relevant risk-framework references.

## 12. Change events

Material changes SHOULD generate a change event. Examples include:

- model or provider change
- new tool or MCP server
- expanded credential scope
- new write permission
- changed autonomy level
- changed approval requirement
- new data category

## 13. Incidents and near misses

AGER MAY reference incidents and near misses. Incident records SHOULD preserve timelines and relevant evidence references without requiring sensitive evidence to be embedded directly in the portable record.

## 14. External mappings

AGER mappings are non-normative unless explicitly promoted in a future specification. Initial mapping targets include:

- SAFE-style incident exchange
- OWASP agentic security guidance
- NIST AI risk-management guidance
- EU AI governance requirements
- ISO/IEC 42001 management-system concepts

## 15. Evidence references

AGER SHOULD reference evidence by durable identifier, URI, hash or internal evidence ID rather than duplicating secrets, credentials or large logs inside the record.

## 16. Security and privacy

AGER records MUST NOT contain plaintext passwords, API keys, private tokens or equivalent authentication secrets.

Implementations SHOULD minimize personal data and SHOULD apply access controls appropriate to the sensitivity of the record.

## 17. Versioning

Breaking schema changes before v1.0 may occur. After v1.0, semantic-versioning rules will be defined for the specification and schemas.
