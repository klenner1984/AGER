#!/usr/bin/env python3
"""Validate AGER partner-outreach portfolio integrity.

This validator checks repository consistency only. It does not determine whether
an outreach message is legally permissible. Channel/legal review remains a
separate operational step.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "outreach/leads-tiered-2026-08-14.json"

TIERS = {
    "A_FOUNDING_PILOT",
    "B_MULTIPLIER",
    "C_STRATEGIC_TECH_PARTNER",
}
CALL_STATES = {"AMBER", "GREEN", "RED"}
REQUIRED = {
    "rank",
    "lead_id",
    "organization",
    "fit_score",
    "tier",
    "sender_profile",
    "channel",
    "contact_route",
    "body_file",
    "pipeline_status",
    "call_status",
    "pilot_angle",
    "verified_signals",
}


def main() -> int:
    leads = json.loads(PORTFOLIO.read_text(encoding="utf-8"))
    failures: list[str] = []

    if not isinstance(leads, list) or len(leads) != 10:
        failures.append("portfolio must contain exactly 10 leads")

    ids: set[str] = set()
    ranks: set[int] = set()

    for lead in leads:
        missing = sorted(REQUIRED - set(lead))
        if missing:
            failures.append(f"{lead.get('lead_id', '<unknown>')}: missing {missing}")
            continue

        lead_id = lead["lead_id"]
        rank = lead["rank"]

        if lead_id in ids:
            failures.append(f"duplicate lead_id: {lead_id}")
        ids.add(lead_id)

        if rank in ranks:
            failures.append(f"duplicate rank: {rank}")
        ranks.add(rank)

        if lead["tier"] not in TIERS:
            failures.append(f"{lead_id}: invalid tier {lead['tier']}")
        if lead["call_status"] not in CALL_STATES:
            failures.append(f"{lead_id}: invalid call_status {lead['call_status']}")
        if lead["sender_profile"] not in {"partner", "andreas", "kontakt"}:
            failures.append(f"{lead_id}: invalid sender_profile")
        if not isinstance(lead["fit_score"], (int, float)) or not (0 <= lead["fit_score"] <= 10):
            failures.append(f"{lead_id}: fit_score must be between 0 and 10")
        if not lead["verified_signals"]:
            failures.append(f"{lead_id}: verified_signals must not be empty")

        body_path = ROOT / lead["body_file"]
        if not body_path.is_file():
            failures.append(f"{lead_id}: missing body_file {lead['body_file']}")
        elif body_path.stat().st_size < 200:
            failures.append(f"{lead_id}: body_file is unexpectedly short")

    if ranks and ranks != set(range(1, 11)):
        failures.append("ranks must be exactly 1..10")

    if failures:
        print("OUTREACH PORTFOLIO INVALID")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("OUTREACH PORTFOLIO OK")
    for lead in sorted(leads, key=lambda x: x["rank"]):
        print(
            f"#{lead['rank']} {lead['organization']} | {lead['tier']} | "
            f"{lead['pipeline_status']} | call={lead['call_status']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
