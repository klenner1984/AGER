#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Create a provisional SAFE-oriented incident export from AGER records")
    p.add_argument("incident", help="AGER incident JSON")
    p.add_argument("--record", help="optional AGER agent record JSON")
    p.add_argument("--out", required=True, help="output JSON path")
    args = p.parse_args()

    incident = json.loads(Path(args.incident).read_text(encoding="utf-8"))
    record = json.loads(Path(args.record).read_text(encoding="utf-8")) if args.record else {}

    export = {
        "format": "AGER-SAFE-PROVISIONAL-0.1",
        "status": "non-normative",
        "incident": {
            "incident_id": incident.get("incident_id"),
            "type": incident.get("type"),
            "severity": incident.get("severity"),
            "detected_at": incident.get("detected_at"),
            "summary": incident.get("summary"),
            "timeline": incident.get("timeline", []),
            "containment": incident.get("containment", []),
            "evidence_refs": incident.get("evidence_refs", []),
        },
        "agent_context": {
            "record_id": record.get("record_id"),
            "agent": record.get("agent", {}),
            "ownership": record.get("ownership", {}),
            "access": record.get("access", {}),
            "human_control": record.get("human_control", {}),
            "security": record.get("security", {}),
            "change_refs": record.get("change_refs", []),
        },
        "notice": "This export is intended to preserve incident context for future interoperability. It does not claim conformance with any Linux Foundation or SAFE specification."
    }

    Path(args.out).write_text(json.dumps(export, indent=2) + "\n", encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
