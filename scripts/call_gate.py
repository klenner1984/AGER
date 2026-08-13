#!/usr/bin/env python3
"""Consent-first gate for automated AGER pilot calls.

This is an operational safeguard, not legal advice. It deliberately uses a
conservative rule: an automated promotional call is allowed only after an
explicit consent signal such as a callback request or booked meeting.
"""

import argparse
import json
from pathlib import Path

ALLOWED_AUTOMATED_STATUSES = {"explicit_consent", "callback_requested", "booked"}
BLOCKED_STATUSES = {"opted_out", "do_not_contact"}


def load(path: str) -> dict:
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def evaluate(record: dict) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    status = record.get("status")
    channel = record.get("channel")
    evidence = record.get("evidence") or {}

    if status in BLOCKED_STATUSES:
        reasons.append(f"status={status} blocks contact")

    if not evidence.get("source_ref"):
        reasons.append("missing consent/invitation evidence reference")

    if channel == "automated_voice_call":
        if status not in ALLOWED_AUTOMATED_STATUSES:
            reasons.append(
                "automated voice call requires explicit_consent, callback_requested, or booked"
            )
        if record.get("ai_disclosure_required") is not True:
            reasons.append("AI disclosure must be required for automated voice calls")
        if record.get("identity_disclosure_required") is not True:
            reasons.append("caller identity disclosure must be required")

    return (not reasons, reasons)


def main() -> int:
    parser = argparse.ArgumentParser(description="AGER consent-first call gate")
    parser.add_argument("record", help="Path to an AGER contact-consent JSON record")
    parser.add_argument("--json", action="store_true", help="Emit JSON result")
    args = parser.parse_args()

    record = load(args.record)
    eligible, reasons = evaluate(record)
    result = {
        "eligible": eligible,
        "lead_id": record.get("lead_id"),
        "organization": record.get("organization"),
        "channel": record.get("channel"),
        "status": record.get("status"),
        "reasons": reasons,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("ELIGIBLE" if eligible else "NOT ELIGIBLE")
        for reason in reasons:
            print(f"- {reason}")

    return 0 if eligible else 2


if __name__ == "__main__":
    raise SystemExit(main())
