# wolf-systems / AGER Call Channel Policy

Status: operational policy, 2026-08-13. Not legal advice.

## Core rule

AGER uses automated voice calling only on a **consent-first** basis.

Do **not** use CALL-E or another automated voice agent for cold promotional calls merely because a business number is public or because a B2B interest seems plausible.

For Germany, § 7(2) no. 2 UWG treats advertising using an automated calling machine as an unacceptable nuisance without the addressee's prior express consent. Because a conversational AI caller can plausibly fall within the concept of an automated calling system, wolf-systems applies the stricter rule until specific authoritative guidance or case law says otherwise.

Primary legal references checked on 2026-08-13:

- https://www.gesetze-im-internet.de/uwg_2004/__7.html
- https://www.bundesnetzagentur.de/DE/Vportal/TK/Aerger/Faelle/UEW/start.html
- https://juris.bundesgerichtshof.de/cgi-bin/bgh_notp/document.py?Art=en&Blank=1&Datum=2022-1-13&Gericht=bgh&Sort=1&anz=20&nr=80960&pos=15
- https://eur-lex.europa.eu/eli/reg/2024/1689/oj

## Channel classes

### GREEN — CALL-E may be used

At least one of the following must be documented before dialing:

- the recipient explicitly requested a callback;
- the recipient explicitly consented to a telephone call about the AGER pilot;
- a meeting/call was booked by the recipient;
- an existing relationship contains a sufficiently specific, documented call permission for this purpose.

The evidence must be stored in an AGER Contact Consent Record.

### AMBER — written/invited channel only

Examples:

- a company publicly invites partner applications;
- a page explicitly invites collaboration proposals;
- a dedicated partner/contact form exists.

Use only the invited channel for the initial approach. Ask whether a short AI-assisted telephone follow-up is welcome. Do not place the CALL-E call until the answer creates a GREEN record.

### RED — no CALL-E

- cold prospect discovered by web search;
- public business phone number with no call consent;
- private/mobile number without explicit business-call consent;
- any previous objection, opt-out or do-not-contact flag;
- unclear identity or unclear purpose.

## Required opening for an automated call

First interaction should make both AI nature and commercial identity clear, for example:

> Guten Tag, ich bin ein KI-Sprachassistent von wolf-systems und rufe im Auftrag von Andreas an. Sie hatten um einen Rückruf zum AGER-Pilot gebeten.

Article 50 AI Act transparency is treated as a design requirement for direct human interaction. The disclosure must be clear and no later than the first interaction, unless AI interaction is already obvious under the applicable rule.

## Operational safeguards

1. Never hide or falsify caller identity.
2. State the purpose briefly and accurately.
3. No pressure tactics and no fabricated scarcity.
4. One failed call attempt, then wait for a new permission signal unless a specific retry time was agreed.
5. Any objection immediately changes the lead to `opted_out` or `do_not_contact`.
6. Do not enable audio recording by default. Recording and retention require a separately checked lawful basis and, where required, consent.
7. Minimise transcripts and personal data; retain only what is necessary for the pilot/contact history.
8. Do not treat an imprint, directory listing or generic public phone number as consent.
9. Every CALL-E run must reference a consent record before execution.
10. Re-check this policy when German/EU law or authoritative guidance changes.

## Sales workflow

`research -> fit score -> invited partner/collaboration channel -> request callback consent -> consent evidence -> call_gate.py -> CALL-E -> outcome -> follow-up / opt-out`

This turns CALL-E into a high-quality warm-lead and booked-call channel rather than a cold-dialer.
