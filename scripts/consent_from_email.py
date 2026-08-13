#!/usr/bin/env python3
"""Create an AGER contact-consent record from a reviewed email reply.

This script does not infer consent. The operator must explicitly choose the
verified status after reading the actual reply.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ALLOWED = {"explicit_consent", "callback_requested", "booked", "opted_out", "do_not_contact"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Create consent evidence from reviewed email")
    parser.add_argument("--lead-id", required=True)
    parser.add_argument("--organization", required=True)
    parser.add_argument("--status", required=True, choices=sorted(ALLOWED))
    parser.add_argument("--message-id", required=True)
    parser.add_argument("--body-sha256", required=True)
    parser.add_argument("--contact-name", default="")
    parser.add_argument("--purpose", default="AGER founding-pilot follow-up")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    record = {
        "ager_version": "0.1",
        "lead_id": args.lead_id,
        "organization": args.organization,
        "channel": "automated_voice_call",
        "status": args.status,
        "captured_at": now,
        "purpose": args.purpose,
        "evidence": {
            "source_type": "written_consent",
            "source_ref": f"privateemail:{args.message_id}",
            "notes": f"Reviewed reply body SHA-256: {args.body_sha256}"
        },
        "ai_disclosure_required": True,
        "identity_disclosure_required": True,
        "audio_recording_allowed": False,
        "notes": "Status selected manually after review of the reply; no automated consent inference."
    }
    if args.contact_name:
        record["contact_name"] = args.contact_name

    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
