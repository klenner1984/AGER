#!/usr/bin/env python3
"""AGER Exposure Scan v0.1 — experimental operational exposure scoring."""
from __future__ import annotations
import argparse, json
from pathlib import Path

AUTONOMY_BASE = {"A0": 5, "A1": 15, "A2": 35, "A3": 60, "A4": 80}

def clamp(v): return max(0, min(100, int(v)))

def score(record):
    agent = record.get("agent", {})
    access = record.get("access", {})
    data = record.get("data", {})
    actions = record.get("actions", {})
    human = record.get("human_control", {})
    autonomy = AUTONOMY_BASE.get(agent.get("autonomy_level", "A0"), 5)
    systems = len(access.get("systems", [])); mcp = len(access.get("mcp_servers", []))
    scopes = " ".join(str(x).lower() for x in access.get("credential_scopes", []))
    permitted = " ".join(str(x).lower() for x in actions.get("permitted", []))

    financial = 10 + (25 if actions.get("financial_limit", 0) else 0)
    if any(k in permitted for k in ["pay", "invoice", "purchase", "refund", "transfer"]): financial += 35

    data_score = 10 + min(35, systems * 5) + min(20, mcp * 5)
    if data.get("personal_data"): data_score += 20
    if data.get("confidential_data"): data_score += 20
    if data.get("external_transfer"): data_score += 10

    communication = 10 + (15 if access.get("write_access") else 0)
    if any(k in permitted for k in ["email", "sms", "call", "message", "publish", "send"]): communication += 45

    execution = autonomy + min(20, systems * 3) + min(15, mcp * 4)
    if access.get("write_access"): execution += 20
    if any(k in scopes for k in ["write", "admin", "execute"]): execution += 15

    propagation = 5
    joined = f"{permitted} {scopes} " + " ".join(str(x).lower() for x in access.get("systems", []))
    if any(k in joined for k in ["agent", "workflow", "deploy", "admin", "token", "credential"]): propagation += 45
    if agent.get("autonomy_level") in ["A3", "A4"]: propagation += 20

    dims = {"financial": clamp(financial), "data": clamp(data_score), "communication": clamp(communication), "execution": clamp(execution), "propagation": clamp(propagation)}
    credit = (10 if human.get("approval_required") else 0) + (8 if human.get("kill_switch") else 0) + (4 if human.get("approver_role") else 0) + (3 if human.get("escalation") else 0)
    dims["overall"] = clamp(round(sum(dims.values()) / 5) - credit)
    return dims

def findings(record, scores):
    out=[]; access=record.get("access",{}); human=record.get("human_control",{}); data=record.get("data",{}); trans=record.get("transparency",{})
    def add(sev, code, title, detail): out.append({"severity":sev,"code":code,"title":title,"detail":detail})
    if access.get("write_access") and not human.get("approval_required"): add("high","AGER-F001","Write access without human approval","The agent can modify state without documented per-action approval.")
    if access.get("write_access") and not human.get("kill_switch"): add("high","AGER-F002","No documented kill switch","A write-capable agent has no documented containment/disable path.")
    if access.get("mcp_servers") and not access.get("credential_scopes"): add("medium","AGER-F003","MCP access without documented scopes","MCP servers are listed but credential scopes are not documented.")
    if data.get("personal_data") and not record.get("evidence_refs"): add("medium","AGER-F004","Personal-data processing without evidence references","The record indicates personal data but contains no linked evidence artifacts.")
    if trans.get("article_50_relevance") in ["unknown","not_assessed"]: add("low","AGER-F005","Transparency relevance not assessed","Article 50 relevance is not yet assessed in this record.")
    if scores["overall"] >= 70: add("high","AGER-F006","High aggregate exposure","Experimental Blast Radius score is 70 or above; prioritize review of permissions and controls.")
    return out

def main():
    p=argparse.ArgumentParser(); p.add_argument("record"); p.add_argument("--json", action="store_true"); args=p.parse_args()
    record=json.loads(Path(args.record).read_text(encoding="utf-8")); scores=score(record); result={"record_id":record.get("record_id"),"agent_id":record.get("agent",{}).get("agent_id"),"blast_radius":scores,"findings":findings(record,scores),"disclaimer":"Experimental operational heuristic. Not a legal opinion, certification, or quantitative risk guarantee."}
    if args.json: print(json.dumps(result, indent=2))
    else:
        print(f"AGER Exposure Scan — {result['agent_id']}"); print(f"Overall Blast Radius: {scores['overall']}/100")
        for k,v in scores.items():
            if k!="overall": print(f"  {k:14} {v:3}/100")
        print("Findings:")
        for f in result["findings"]: print(f"  [{f['severity'].upper()}] {f['code']} {f['title']}")
if __name__ == "__main__": main()
