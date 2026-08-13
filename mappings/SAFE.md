# AGER → SAFE Compatibility Mapping (Draft)

## Purpose

AGER is intended to preserve operational context before an AI incident occurs. SAFE-style incident exchange begins when an incident or near miss must be described and shared.

The two concepts are complementary:

```text
AGER operational record
        ↓
configuration / permission changes
        ↓
near miss or incident
        ↓
AGER evidence package
        ↓
SAFE-compatible incident representation
```

## Preliminary mapping

| Incident information need | AGER source |
|---|---|
| Agent/workload identity | `agent.agent_id`, `agent.name` |
| Model/provider context | `agent.provider`, `agent.model`, `agent.model_version` |
| Deployment context | `agent.environment` |
| Available systems/tools | `access.systems`, `access.mcp_servers` |
| Credential/permission context | `access.credential_scopes`, `access.write_access` |
| Human approvals | `human_control.*` |
| Operational boundaries | `actions.*` |
| Monitoring sources | `security.monitoring` |
| Relevant evidence | `evidence_refs` |
| Pre-incident changes | `change_refs` |
| Incident references | `incident_refs` |

## Design rule

AGER SHOULD NOT embed secrets, raw credentials or unrestricted sensitive logs merely to make incident export easier. Evidence references should point to appropriately protected evidence stores.

## Status

This mapping is exploratory and non-normative. It must be updated against published SAFE specifications as they evolve. AGER does not claim endorsement, certification or formal compatibility by the Linux Foundation, OpenSSF, SAFE or any other external organization.
