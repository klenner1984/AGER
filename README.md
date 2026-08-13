# AGER — Agent Governance & Evidence Record

AGER is an open operational evidence format for AI agents.

It is designed to answer a simple question:

> Which AI agents exist, what can they access, what are they allowed to do, who is accountable, what changed, and what evidence exists?

AGER sits between AI-agent deployment and downstream governance, security, audit and incident-response processes. It is intended to be lightweight enough for SMEs and AI agencies while remaining structured enough for automation.

## Why AGER

AI agents increasingly connect to email, CRM, files, databases, APIs, MCP servers and other production systems. Traditional policy documents do not provide a sufficiently precise operational record of those permissions, controls and changes.

AGER provides a machine-readable evidence layer for:

- agent inventory
- ownership and accountability
- model/provider metadata
- tool and MCP access
- data categories
- write permissions and action limits
- human approvals
- transparency evidence
- security controls
- deployment changes
- incidents and near misses
- incident-export preparation

## Core concepts

### Autonomy levels

- **A0 — Assistive:** information only; no external action.
- **A1 — Recommend:** proposes actions but cannot execute them.
- **A2 — Act with approval:** prepares or initiates actions that require human approval.
- **A3 — Scoped autonomous:** executes pre-authorized actions within defined boundaries.
- **A4 — High-impact autonomous:** can materially affect money, external communications, production data or systems without per-action approval.

### Blast Radius

AGER models the potential operational impact of an agent across five dimensions:

- financial radius
- data radius
- communication radius
- execution radius
- propagation radius

The scoring model is currently experimental and will be formalized in a later version.

## Repository structure

```text
schemas/        JSON Schemas
examples/       example AGER records
mappings/       mappings to external frameworks and incident formats
SPECIFICATION.md  normative draft specification
ROADMAP.md        development roadmap
```

## Status

**AGER v0.1-draft**

This is an early public draft. Field names, semantics and compatibility mappings may change before v1.0.

## Design principles

1. Evidence first.
2. Machine readable by default.
3. Human readable without specialized tooling.
4. Vendor neutral.
5. Compatible with existing governance and incident-response ecosystems rather than replacing them.
6. Practical for SMEs, AI agencies and managed-service providers.
7. No claim of legal compliance or certification by format adoption alone.

## Minimal record

```json
{
  "ager_version": "0.1",
  "record_id": "ager-demo-001",
  "agent": {
    "agent_id": "sales-assistant-01",
    "name": "Sales Assistant",
    "purpose": "Qualify inbound leads",
    "autonomy_level": "A2"
  },
  "ownership": {
    "business_owner": "Head of Sales",
    "technical_owner": "IT Operations"
  },
  "access": {
    "systems": ["CRM", "email"],
    "write_access": true
  }
}
```

See `SPECIFICATION.md` and `schemas/ager-record.schema.json` for the current draft.

## Scope boundary

AGER is a governance and evidence format. It is not legal advice, a certification, a security guarantee or a substitute for risk assessment appropriate to a specific organization or jurisdiction.

## Contributing

Issues and pull requests are welcome while the v0.x schema is being shaped.
