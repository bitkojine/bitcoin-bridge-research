from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

SHA256 = re.compile(r"^[0-9a-f]{64}$")
REVIEW_STATUSES = {"accepted", "rejected", "contested"}


def _time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone is required")
    return parsed


def validate_case(case: dict) -> list[str]:
    errors: list[str] = []
    meta = case.get("case")
    if not isinstance(meta, dict):
        return ["case metadata is required; raw Boolean fact maps are no longer accepted"]
    for field in ("schema_version", "id", "title", "assessed_at", "jurisdiction", "subject_id"):
        if not meta.get(field):
            errors.append(f"case.{field} is required")
    if meta.get("schema_version") != "1.0.0":
        errors.append("case.schema_version must be 1.0.0")
    try:
        assessed_at = _time(meta.get("assessed_at", ""))
    except (TypeError, ValueError):
        errors.append("case.assessed_at must be an ISO 8601 date-time")
        assessed_at = None

    evidence = case.get("evidence")
    if not isinstance(evidence, list):
        return errors + ["evidence must be a list"]
    seen: set[str] = set()
    for index, record in enumerate(evidence):
        prefix = f"evidence[{index}]"
        record_id = record.get("id")
        if not record_id:
            errors.append(f"{prefix}.id is required")
        elif record_id in seen:
            errors.append(f"duplicate evidence id: {record_id}")
        seen.add(record_id)

        assertion = record.get("assertion", {})
        if not assertion.get("fact"):
            errors.append(f"{prefix}.assertion.fact is required")
        if not isinstance(assertion.get("value"), bool):
            errors.append(f"{prefix}.assertion.value must be Boolean")
        if assertion.get("subject_id") != meta.get("subject_id"):
            errors.append(f"{prefix}.assertion.subject_id must match case.subject_id")

        artifact = record.get("artifact", {})
        for field in ("type", "title"):
            if not artifact.get(field):
                errors.append(f"{prefix}.artifact.{field} is required")
        digest = artifact.get("sha256")
        if digest and not SHA256.fullmatch(digest):
            errors.append(f"{prefix}.artifact.sha256 must be 64 lowercase hexadecimal characters")
        if not digest and not artifact.get("integrity_not_recorded_reason"):
            errors.append(f"{prefix}.artifact requires sha256 or integrity_not_recorded_reason")

        issuer = record.get("issuer", {})
        for field in ("id", "name", "type"):
            if not issuer.get(field):
                errors.append(f"{prefix}.issuer.{field} is required")
        if issuer.get("type") not in {"person", "organization", "software"}:
            errors.append(f"{prefix}.issuer.type must be person, organization, or software")

        provenance = record.get("provenance", {})
        for field in ("obtained_at", "method"):
            if not provenance.get(field):
                errors.append(f"{prefix}.provenance.{field} is required")

        scope = record.get("scope", {})
        if not scope.get("jurisdictions"):
            errors.append(f"{prefix}.scope.jurisdictions is required")
        if not scope.get("description"):
            errors.append(f"{prefix}.scope.description is required")
        for field in ("valid_from", "valid_until"):
            if scope.get(field):
                try:
                    _time(scope[field])
                except (TypeError, ValueError):
                    errors.append(f"{prefix}.scope.{field} must be an ISO 8601 date-time")
        if scope.get("valid_from") and scope.get("valid_until"):
            if _time(scope["valid_from"]) > _time(scope["valid_until"]):
                errors.append(f"{prefix} validity period is inverted")

        review = record.get("review", {})
        if review.get("status") not in REVIEW_STATUSES:
            errors.append(f"{prefix}.review.status must be accepted, rejected, or contested")
        for field in ("reviewed_at", "method"):
            if not review.get(field):
                errors.append(f"{prefix}.review.{field} is required")
        reviewer = review.get("reviewer", {})
        for field in ("id", "name", "role"):
            if not reviewer.get(field):
                errors.append(f"{prefix}.review.reviewer.{field} is required")

        if assessed_at and scope.get("valid_from") and scope.get("valid_until"):
            pass  # validity is evaluated, not rejected, during assessment
    return errors


def derive_facts(case: dict) -> dict:
    errors = validate_case(case)
    if errors:
        return {"facts": {}, "traces": {}, "excluded": [], "errors": errors, "conflicts": []}

    meta = case["case"]
    at = _time(meta["assessed_at"])
    jurisdiction = meta["jurisdiction"]
    values: dict[str, list[tuple[bool, dict]]] = {}
    excluded = []
    for record in case["evidence"]:
        reasons = []
        review = record["review"]
        scope = record["scope"]
        if review["status"] != "accepted":
            reasons.append(f"review status is {review['status']}")
        if jurisdiction not in scope["jurisdictions"] and "*" not in scope["jurisdictions"]:
            reasons.append(f"not scoped to jurisdiction {jurisdiction}")
        if scope.get("valid_from") and at < _time(scope["valid_from"]):
            reasons.append("not yet valid at assessment time")
        if scope.get("valid_until") and at > _time(scope["valid_until"]):
            reasons.append("expired before assessment time")
        if reasons:
            excluded.append({"evidence_id": record["id"], "reasons": reasons})
            continue
        assertion = record["assertion"]
        values.setdefault(assertion["fact"], []).append((assertion["value"], record))

    facts, traces, conflicts = {}, {}, []
    for fact, assertions in sorted(values.items()):
        distinct = {value for value, _ in assertions}
        if len(distinct) > 1:
            conflicts.append({
                "fact": fact,
                "values": sorted(distinct),
                "evidence_ids": [record["id"] for _, record in assertions],
            })
            continue
        facts[fact] = assertions[0][0]
        traces[fact] = [record["id"] for _, record in assertions]
    return {"facts": facts, "traces": traces, "excluded": excluded, "errors": [], "conflicts": conflicts}


def assess(profile: dict, case: dict[str, Any], rules: list[dict] | None = None) -> dict:
    derivation = derive_facts(case)
    facts = derivation["facts"]
    satisfied, failed, unknown = [], [], []
    for requirement in profile["requirements"]:
        applies_when = requirement.get("applies_when")
        if applies_when:
            controlling_fact = applies_when["fact"]
            if controlling_fact not in facts:
                unknown.append({
                    **requirement,
                    "value": "unknown",
                    "evidence_ids": [],
                    "reason": f"Applicability is unknown until accepted evidence establishes {controlling_fact}.",
                })
                continue
            if facts[controlling_fact] != applies_when["equals"]:
                continue
        fact = requirement["fact"]
        item = {
            **requirement,
            "value": facts.get(fact, "unknown"),
            "evidence_ids": derivation["traces"].get(fact, []),
        }
        if fact not in facts:
            unknown.append(item)
        elif facts[fact] is True:
            satisfied.append(item)
        else:
            failed.append(item)

    if derivation["errors"] or derivation["conflicts"]:
        outcome = "conflict"
    elif failed:
        outcome = "not_ready"
    elif unknown:
        outcome = "insufficient_information"
    else:
        outcome = "ready_for_expert_review"

    derived: dict[str, Any] = {}
    if rules:
        from src.expert import ExpertSystem

        rule_input = {item["fact"]: True for item in satisfied}
        rule_input.update({item["fact"]: False for item in failed})
        inference = ExpertSystem(rules).infer(rule_input)
        conclusions = {
            name: [entry["value"] for entry in assertions if entry["source"] == "derived"]
            for name, assertions in inference["facts"].items()
        }
        derived = {
            "input_facts": dict(sorted(rule_input.items())),
            "conclusions": {k: v for k, v in conclusions.items() if v},
            "status": inference["status"],
            "trace": inference["trace"],
            "conflicts": inference["conflicts"],
        }
    return {
        "assessment": profile["id"],
        "version": profile["version"],
        "case_id": case.get("case", {}).get("id"),
        "scope": profile["scope"],
        "outcome": outcome,
        "summary": {
            "satisfied": len(satisfied), "failed": len(failed), "unknown": len(unknown),
            "invalid": len(derivation["errors"]), "conflicts": len(derivation["conflicts"]),
            "excluded_evidence": len(derivation["excluded"]),
        },
        "satisfied": satisfied,
        "failed": failed,
        "unknown": unknown,
        "invalid": derivation["errors"],
        "conflicts": derivation["conflicts"],
        "excluded_evidence": derivation["excluded"],
        "derived": derived,
        "disclaimer": "Research pre-screen only. A qualified professional must validate the evidence, applicability, and conclusion.",
    }


def render_markdown(result: dict) -> str:
    s = result["summary"]
    lines = [
        "# Bitcoin Institutional Custody Readiness Assessment", "",
        f"**Case:** `{result['case_id']}`  ", f"**Outcome:** `{result['outcome']}`", "",
        result["scope"], "",
        f"Satisfied: {s['satisfied']} · Failed: {s['failed']} · Unknown: {s['unknown']} · Invalid: {s['invalid']} · Conflicts: {s['conflicts']} · Excluded evidence: {s['excluded_evidence']}", "",
    ]
    if result["invalid"]:
        lines += ["## Invalid case data", ""] + [f"- {error}" for error in result["invalid"]] + [""]
    if result["conflicts"]:
        lines += ["## Conflicting evidence", ""]
        for item in result["conflicts"]:
            lines.append(f"- `{item['fact']}` has accepted evidence for incompatible values: {', '.join(item['evidence_ids'])}.")
        lines.append("")
    if result["excluded_evidence"]:
        lines += ["## Excluded evidence", ""]
        for item in result["excluded_evidence"]:
            lines.append(f"- `{item['evidence_id']}`: {'; '.join(item['reasons'])}.")
        lines.append("")
    for key, title in (("failed", "Blocking gaps"), ("unknown", "Missing evidence"), ("satisfied", "Evidenced requirements")):
        lines += [f"## {title}", ""]
        if not result[key]:
            lines.append("None.")
        for item in result[key]:
            evidence = f" Evidence: {', '.join(item['evidence_ids'])}." if item["evidence_ids"] else ""
            expected = f" Expected: {item['evidence_expected']}" if key != "satisfied" else ""
            reason = f" {item['reason']}" if item.get("reason") else ""
            lines.append(f"- **{item['label']}** (`{item['fact']}`).{evidence}{expected}{reason}")
        lines.append("")
    derived = result.get("derived") or {}
    if derived.get("conclusions"):
        lines += ["## Derived conclusions", ""]
        for fact, values in sorted(derived["conclusions"].items()):
            lines.append(f"- `{fact}` = {', '.join(str(v) for v in values)}. Rules: {', '.join(step['rule_id'] for step in derived['trace'])}.")
        lines.append("")
    lines += ["## Limitation", "", result["disclaimer"], ""]
    return "\n".join(lines)


def load_profile(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_profile(profile: dict, source_ids: set[str], fact_registry: set[str] | None = None) -> list[str]:
    errors = []
    seen = set()
    for requirement in profile.get("requirements", []):
        fact = requirement.get("fact")
        if not fact or fact in seen:
            errors.append(f"assessment has missing or duplicate requirement fact: {fact}")
        seen.add(fact)
        if fact_registry is not None and fact not in fact_registry:
            errors.append(f"assessment requirement {fact} is not registered in the fact registry")
        applies_when = requirement.get("applies_when")
        if applies_when and fact_registry is not None and applies_when.get("fact") not in fact_registry:
            errors.append(f"assessment requirement {fact} control fact {applies_when.get('fact')} is not registered in the fact registry")
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
