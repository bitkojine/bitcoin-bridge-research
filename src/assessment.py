from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def assess(profile: dict, facts: dict[str, Any]) -> dict:
    satisfied, failed, unknown, invalid = [], [], [], []
    for requirement in profile["requirements"]:
        applies_when = requirement.get("applies_when")
        if applies_when:
            controlling_fact = applies_when["fact"]
            if controlling_fact not in facts:
                unknown.append({
                    **requirement,
                    "value": "unknown",
                    "reason": f"Applicability is unknown until {controlling_fact} is supplied.",
                })
                continue
            if not isinstance(facts[controlling_fact], bool):
                invalid.append({"fact": controlling_fact, "value": facts[controlling_fact]})
                continue
            if facts[controlling_fact] != applies_when["equals"]:
                continue
        fact = requirement["fact"]
        item = {**requirement, "value": facts.get(fact, "unknown")}
        if fact not in facts:
            unknown.append(item)
        elif not isinstance(facts[fact], bool):
            invalid.append({"fact": fact, "value": facts[fact]})
        elif facts[fact] is True:
            satisfied.append(item)
        else:
            failed.append(item)

    if invalid:
        outcome = "conflict"
    elif failed:
        outcome = "not_ready"
    elif unknown:
        outcome = "insufficient_information"
    else:
        outcome = "ready_for_expert_review"
    return {
        "assessment": profile["id"],
        "version": profile["version"],
        "scope": profile["scope"],
        "outcome": outcome,
        "summary": {
            "satisfied": len(satisfied), "failed": len(failed), "unknown": len(unknown),
            "invalid": len(invalid)
        },
        "satisfied": satisfied,
        "failed": failed,
        "unknown": unknown,
        "invalid": invalid,
        "disclaimer": "Research pre-screen only. A qualified professional must validate the facts, applicability, and conclusion.",
    }


def render_markdown(result: dict) -> str:
    lines = [
        "# Bitcoin Institutional Custody Readiness Assessment", "",
        f"**Outcome:** `{result['outcome']}`", "",
        result["scope"], "",
        f"Satisfied: {result['summary']['satisfied']} · Failed: {result['summary']['failed']} · Unknown: {result['summary']['unknown']} · Invalid: {result['summary']['invalid']}", "",
    ]
    if result["invalid"]:
        lines += ["## Invalid inputs", ""]
        for item in result["invalid"]:
            lines.append(f"- `{item['fact']}` must be `true` or `false`; received `{item['value']}`.")
        lines.append("")
    for key, title in [("failed", "Blocking gaps"), ("unknown", "Missing evidence"), ("satisfied", "Evidenced requirements")]:
        lines += [f"## {title}", ""]
        items = result[key]
        if not items:
            lines.append("None.")
        for item in items:
            detail = f" Expected evidence: {item['evidence_expected']}" if key != "satisfied" else ""
            reason = f" {item['reason']}" if item.get("reason") else ""
            lines.append(f"- **{item['label']}** (`{item['fact']}`) — sources: {', '.join(item['source_ids'])}.{detail}{reason}")
        lines.append("")
    lines += ["## Important limitation", "", result["disclaimer"], ""]
    return "\n".join(lines)


def load_profile(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_profile(profile: dict, source_ids: set[str]) -> list[str]:
    errors = []
    seen = set()
    for requirement in profile.get("requirements", []):
        fact = requirement.get("fact")
        if not fact or fact in seen:
            errors.append(f"assessment has missing or duplicate requirement fact: {fact}")
        seen.add(fact)
        if not requirement.get("label"):
            errors.append(f"assessment requirement {fact} has no label")
        if not requirement.get("evidence_expected"):
            errors.append(f"assessment requirement {fact} has no expected evidence description")
        if not requirement.get("source_ids"):
            errors.append(f"assessment requirement {fact} has no sources")
        for source_id in requirement.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"assessment requirement {fact} references unknown source {source_id}")
    return errors
