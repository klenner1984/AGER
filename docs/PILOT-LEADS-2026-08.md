# AGER Pilot Leads — DACH shortlist

Research date: 2026-08-13

Purpose: identify technically strong, commercially plausible founding-pilot targets for AGER. Scores are internal prioritisation, not external endorsements.

## 1. dalvon / neuromanufaktur GmbH — 9.8/10

Why it fits:
- production-grade European voice-agent platform;
- phone + chat agents sharing workflows and knowledge;
- API and MCP control;
- RBAC, SSO and API keys;
- on-premises and white-label enterprise positioning;
- targets IT system houses and AI agencies, making AGER potentially useful as a governance/evidence layer for both platform and channel partners.

Pilot angle:
- one complex agent with MCP/API access;
- map agent identity, tool permissions, human control, change history and evidence package;
- test whether AGER can become an optional governance hand-off artifact for dalvon partners.

Initial outreach class: **AMBER**.
Use their publicly promoted Partner/Enterprise route first. Ask explicitly for permission for a short AI-assisted follow-up call; CALL-E only after that permission.

Sources:
- https://dalvon.ai/
- https://dalvon.ai/kontakt
- https://dalvon.ai/branchen/it-systemhaeuser

## 2. KMK Partners — 9.8/10

Why it fits:
- builds voice agents that write to CRM/ERP;
- n8n/Make/custom backend integration;
- explicitly uses audit trails and human-in-the-loop;
- runs co-development, revenue-share and productisation models;
- publicly invites people interested in collaboration to contact them.

Pilot angle:
- convert an existing voice-agent deployment into a complete AGER evidence baseline;
- compare their current audit trail/HITL practice against AGER's access, change, evidence and incident records;
- explore co-development/white-label governance layer rather than a simple vendor sale.

Initial outreach class: **AMBER — strongest invited collaboration route**.
Their contact page explicitly welcomes collaboration interest. Use that channel first and request callback consent.

Sources:
- https://kmk-partners.de/
- https://kmk-partners.de/leistungen/ai-automatisierung
- https://kmk-partners.de/kontakt

## 3. VoiceBooker / claiverly GmbH — 9.7/10

Why it fits:
- voice and chat agents;
- REST API and MCP integration;
- n8n, Make, CRM, calendar, ticket and database connectivity;
- SIP/telephony integration;
- dedicated Enterprise & Partner tier for resellers/system integrators;
- white-labelling and advanced webhooks.

Pilot angle:
- AGER as a standard machine-readable governance record supplied alongside an enterprise integration;
- permission map for MCP/REST connections;
- evidence baseline and incident reconstruction package for system integrators.

Initial outreach class: **AMBER**.
Use the explicit Partner/Enterprise route first. Request a named technical partner contact and opt-in for a short CALL-E follow-up.

Sources:
- https://voicebooker.de/de
- https://voicebooker.de/de/features-overview
- https://voicebooker.de/contact-centers

## 4. RSG AI / RSG Recruiting Solutions Group GmbH — 9.6/10

Why it fits:
- 12+ agents described as live in production and a larger voice-agent network;
- LangChain + n8n stack;
- CRM integration, inbound/outbound agents and compliance logging;
- advertises partner participation;
- current operational scale gives AGER a meaningful real-world evidence test.

Pilot angle:
- select one deployed voice agent with CRM/tool access;
- calculate AGER blast radius and capture human-control/evidence baseline;
- test governance hand-off for RSG's customer deployments.

Initial outreach class: **AMBER**.
Use their Partner route first; do not use their normal public phone number for an unsolicited CALL-E pitch.

Sources:
- https://www.rsg-ai.de/
- https://www.rsg-ai.de/ki-telefonassistent
- https://www.rsg-ai.de/impressum

## 5. kapio UG — 9.5/10

Why it fits:
- operates at the intersection of CRM, ERP, AI, automation and databases;
- n8n and MCP are explicitly part of current work;
- reports running its own daily business through AI-connected tooling;
- Pipedrive/CRM access makes permission and action evidence directly relevant;
- homepage explicitly invites visitors to "zusammenarbeiten".

Pilot angle:
- govern a non-voice but highly agentic MCP/n8n deployment;
- prove AGER is broader than voice AI and works on operational business agents;
- map Pipedrive/n8n/tool scopes, autonomy, approvals, change events and blast radius.

Initial outreach class: **AMBER — invited collaboration route**.
Use the collaboration route first and request permission for an AI-assisted follow-up call.

Sources:
- https://kapio.eu/
- https://www.kapio.eu/about
- https://www.kapio.eu/impressum

## Reserve: FullCircleAutomations

Very high technical fit: Fonio/Vapi voice agents, n8n/Make, CRM/API integration and ongoing reporting. It remains a reserve because the currently found public contact route is a general project enquiry rather than a clearly labelled partner/co-development invitation.

Sources:
- https://www.fullcircleautomations.de/ai-voice-agent
- https://www.fullcircleautomations.de/kontakt

## Execution order

1. KMK Partners — explicit collaboration/co-development positioning.
2. VoiceBooker — explicit partner/system-integrator tier.
3. dalvon — strongest MCP/enterprise architecture fit.
4. RSG AI — strongest operational voice-agent volume fit.
5. kapio — strongest non-voice MCP/n8n governance proof.

No automated cold calls. Each lead remains AMBER until a callback/phone permission is captured. Once permission is documented, create a Contact Consent Record, run `python scripts/call_gate.py <record>`, then execute CALL-E only on an ELIGIBLE result.
