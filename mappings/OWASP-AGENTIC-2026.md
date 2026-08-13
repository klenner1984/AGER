# AGER Mapping to OWASP Top 10 for Agentic Applications 2026

Status: draft, non-normative crosswalk.

AGER does not replace OWASP guidance. This mapping shows which AGER evidence fields can help document controls, exposure or incident context related to OWASP Agentic Security Initiative risks.

## ASI01 — Agent Goal Hijack

Relevant AGER evidence:

- agent purpose and autonomy level
- prompt/configuration evidence
- permitted/prohibited actions
- human approval boundaries
- change events affecting prompts, tools or policies
- incident traces and tool calls

## ASI02 — Tool Misuse & Exploitation

Relevant AGER evidence:

- `access.systems`
- MCP permission records
- tool-level read/write/execute/delete/admin classification
- execution limits
- tool restrictions
- human approval requirements
- incident tool-call timeline

## ASI03 — Identity & Privilege Abuse

Relevant AGER evidence:

- credential scopes
- MCP authentication mode
- delegated permissions
- privileged tool access
- permission snapshots
- ownership and review records
- permission-change events

## ASI04 — Agentic Supply Chain Vulnerabilities

Relevant AGER evidence:

- provider and model metadata
- MCP provider/server records
- trust status of third-party MCP servers
- model/configuration change history
- external system dependencies
- evidence hashes and provenance references

## ASI05 — Unexpected Code Execution

Relevant AGER evidence:

- execute-capable tool inventory
- MCP tool access classification
- execution restrictions
- approval gates
- network restrictions
- incident traces and containment actions

## Remaining ASI risks

AGER v0.1 intentionally avoids claiming complete control coverage for every OWASP Agentic Top 10 category. Future revisions will extend the crosswalk after field-level validation against the full OWASP risk descriptions and mitigation guidance.

## Interpretation rule

An AGER record demonstrates that evidence was captured. It does not demonstrate that a risk is mitigated merely because a field exists or has been populated.
