#!/usr/bin/env python3
"""Show ordered next actions for the AGER partner pipeline.

This is an operational routing helper, not a legal decision engine. Automated
voice calls remain subject to the separate contact-consent record and call_gate.
"""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PORTFOLIO = ROOT / "outreach/leads-tiered-2026-08-14.json"


def action_for(lead: dict) -> str:
    status = lead.get("pipeline_status")
    channel = lead.get("channel")
    if status == "WARM_EXISTING_THREAD":
        return "Reply in the existing thread using the warm follow-up; do not open a new cold thread."
    if status == "PARTNER_ROUTE_READY":
        if "application" in channel or "partner" in channel:
            return "Use the explicit partner/application route. Keep CALL-E AMBER until explicit phone/callback consent."
        return "Use the listed invited contact route; no automated call without explicit consent."
    if status == "REPLIED":
        return "Review the reply. If it explicitly authorizes a callback/phone contact, preserve evidence and run call_gate.py."
    if status == "PILOT_PROPOSED":
        return "Follow up in the same thread and ask for a technical scope/meeting."
    if status == "PILOT_BOOKED":
        return "Prepare the one-agent AGER Exposure Baseline and pilot intake."
    if status == "PILOT_RUNNING":
        return "Complete Exposure Baseline, evidence package and conversion proposal."
    if status == "PAID_OFFICE":
        return "Operate recurring Governance & Evidence Office cadence."
    return "Review pipeline status manually before contact."


def main() -> int:
    parser = argparse.ArgumentParser(description="Show next AGER partner outreach actions")
    parser.add_argument("--portfolio", default=str(DEFAULT_PORTFOLIO))
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    leads = json.loads(Path(args.portfolio).read_text(encoding="utf-8"))
    leads = sorted(leads, key=lambda lead: lead["rank"])

    for lead in leads[: args.top]:
        print(f"#{lead['rank']} {lead['organization']} | {lead['tier']}")
        print(f"  status: {lead['pipeline_status']} | call: {lead['call_status']}")
        print(f"  route:  {lead['contact_route']}")
        print(f"  next:   {action_for(lead)}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
