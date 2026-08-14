# AGER Roadmap

Updated: 2026-08-14

## v0.1 — Operational record foundation

- [x] Core AGER record
- [x] Autonomy levels A0–A4
- [x] Blast Radius dimensions
- [x] JSON Schema
- [x] Voice-agent example
- [x] Change-event schema
- [x] Incident / near-miss schema
- [x] Evidence-reference schema
- [x] MCP-specific permission representation
- [x] Schema validation tests
- [x] Exposure Scan
- [x] Consent-first automated-call gate

## v0.2 — Framework interoperability

- [x] Preliminary SAFE mapping/export work
- [x] OWASP Agentic mapping draft
- [ ] NIST agent guidance mapping
- [ ] EU AI Act evidence mapping
- [ ] ISO/IEC 42001 concept mapping
- [ ] Refresh SAFE export profile as public specifications evolve

All mappings remain non-normative unless an external standards body explicitly says otherwise.

## v0.3 — Operational tooling

- [x] CLI-oriented record/scan tooling foundation
- [x] Example validation in CI
- [x] Exposure Scan smoke test in CI
- [x] PrivateEmail selective outreach helpers
- [x] Contact-consent evidence bridge
- [x] Tiered partner lead portfolio validation
- [ ] Diff / change detector
- [ ] Human-readable Evidence Pack renderer
- [ ] Evidence integrity verification workflow
- [ ] Platform import/export adapters
- [ ] Bulk agent inventory/import

## v0.4 — Partner pilot productization

Primary focus: prove that AGER works as a repeatable deployment artifact between AI-agent platforms, implementation partners and customers.

- [x] Define partner-led GTM strategy
- [x] Tier A/B/C partner portfolio
- [x] Founding-pilot message set
- [x] Consent-first call policy
- [ ] Book first technical Founding Pilot
- [ ] Generate first real customer/partner AGER Exposure Baseline
- [ ] Produce first anonymized case study
- [ ] Define recurring Governance & Evidence Office SLA
- [ ] Define base + per-agent/per-deployment commercial packaging
- [ ] Build white-label Evidence Pack
- [ ] Build reusable platform adapter interface

## Commercial implementation track

The open specification remains independent from commercial services.

Commercial implementation: **AGER Governance & Evidence Office**

Services:
- agent inventory maintenance;
- permission/MCP/API review;
- autonomy and human-control evidence;
- deployment-change monitoring;
- evidence integrity and retention support;
- incident/near-miss evidence preparation;
- recurring Evidence Pack refresh;
- white-label delivery for AI agencies, MSPs, BPOs and system integrators.

Primary route to market:

`AI-agent platform -> implementation/technology partner -> customer deployments -> recurring AGER records`

See `docs/GTM-PARTNER-STRATEGY.md` and `outreach/leads-tiered-2026-08-14.json`.

## v1.0 objective

A stable, vendor-neutral operational evidence format that can be implemented without purchasing a proprietary governance platform, plus a repeatable commercial operating model for maintaining those records across production AI-agent fleets.
