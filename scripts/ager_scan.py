#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

WEIGHTS = {
    "financial": 0.20,
    "data": 0.25,
    "communication": 0.20,
    "execution": 0.25,
    "propagation": 0.10,
}


def clamp(v):
    return max(0, min(100, int(v)))


def score_dimension(config, key):
    rules = config.get("blast_radius_inputs", {})
    values = rules.get(key, {})
    score = 0
    if values.get("enabled"):
        score += 20
    if values.get("external"):
        score += 20
    if values.get("write"):
        score += 25
    if values.get("unbounded"):
        score += 25
    if values.get("sensitive"):
        score += 10
    return clamp(score)


def scan(config):
    dimensions = {k: score_dimension(config, k) for k in WEIGHTS}
    overall = round(sum(dimensions[k] * WEIGHTS[k] for k in WEIGHTS))

    findings = []
    access = config.get("access", {})
    human = config.get("human_control", {})
    agent = config.get("agent", {})

    if access.get("write_access") and not human.get("approval_required", False):
        findings.append({"severity": "high", "code": "AGER-F001", "finding": "Write access without per-action human approval."})
    if agent.get("autonomy_level") in {"A3", "A4"} and not human.get("kill_switch", False):
        findings.append({"severity": "high", "code": "AGER-F002", "finding": "Autonomous agent without documented kill switch."})
    if access.get("mcp_servers") and not access.get("credential_scopes"):
        findings.append({"severity": "medium", "code": "AGER-F003", "finding": "MCP connectivity is documented but credential scopes are missing."})
    if not config.get("ownership", {}).get("governance_owner"):
        findings.append({"severity": "medium", "code": "AGER-F004", "finding": "No governance owner is documented."})
    if not config.get("evidence_refs"):
        findings.append({"severity": "medium", "code": "AGER-F005", "finding": "No operational evidence references are attached."})

    return {
        "record_id": config.get("record_id"),
        "agent_id": agent.get("agent_id"),
        "autonomy_level": agent.get("autonomy_level"),
        "blast_radius": {**dimensions, "overall": overall},
        "finding_count": len(findings),
        "findings": findings,
        "disclaimer": "AGER exposure scoring is an operational triage aid, not a legal or security certification."
    }


def main():
    p = argparse.ArgumentParser(description="AGER Exposure Scan v0.1")
    p.add_argument("record", help="AGER JSON record")
    p.add_argument("--out", help="write report to JSON file")
    args = p.parse_args()

    config = json.loads(Path(args.record).read_text(encoding="utf-8"))
    report = scan(config)
    rendered = json.dumps(report, indent=2)
    if args.out:
        Path(args.out).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
