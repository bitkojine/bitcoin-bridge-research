from __future__ import annotations

import json
from pathlib import Path


STAGE_ORDER = ["ontology", "data", "epistemology", "axiology", "action"]
RELATION_TREATMENTS = {"supports", "contradicts", "qualifies"}


def load_philosophy(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_philosophy(model: dict) -> list[str]:
    errors: list[str] = []
    stages = model.get("stages", [])
    stage_ids = [item.get("id") for item in stages]
    if stage_ids != STAGE_ORDER:
        errors.append(f"stages must follow {STAGE_ORDER}, got {stage_ids}")
    for stage in stages:
        stage_id = stage.get("id", "<missing>")
        for field in ("question", "accepts", "produces", "failure"):
            if not stage.get(field):
                errors.append(f"stage {stage_id} has no {field}")

    relation_ids: set[str] = set()
    for relation in model.get("relations", []):
        relation_id = relation.get("id", "<missing>")
        if relation_id in relation_ids:
            errors.append(f"duplicate relation id: {relation_id}")
        relation_ids.add(relation_id)
        for field in ("from", "to", "meaning"):
            if not relation.get(field):
                errors.append(f"relation {relation_id} has no {field}")
    if not RELATION_TREATMENTS.issubset(relation_ids):
        errors.append("relations must include supports, contradicts, and qualifies")

    gates = model.get("gates", [])
    gate_stages = [item.get("stage") for item in gates]
    if gate_stages != STAGE_ORDER:
        errors.append("exactly one gate is required for each stage in stage order")
    for gate in gates:
        if not gate.get("passes_when") or not gate.get("on_failure"):
            errors.append(f"gate {gate.get('id')} is incomplete")

    required_action_fields = set(model.get("minimum_action_record", []))
    expected = {
        "id", "actor", "action", "requires_claims", "serves_values", "legal_state",
        "authority_state", "consequences", "reversibility",
    }
    if not expected.issubset(required_action_fields):
        errors.append(f"minimum_action_record missing {sorted(expected - required_action_fields)}")
    if not model.get("invariants"):
        errors.append("invariants must not be empty")
    return errors


def evaluate_action(record: dict, claims: dict[str, str], values: set[str]) -> dict:
    """Evaluate the final philosophy gate without pretending to make the decision."""
    blockers: list[dict] = []
    for field in ("id", "actor", "action", "legal_state", "authority_state", "reversibility"):
        if not record.get(field):
            blockers.append({"type": "missing_field", "field": field})
    if not record.get("consequences"):
        blockers.append({"type": "missing_field", "field": "consequences"})
    if record.get("legal_state") == "prohibited":
        blockers.append({"type": "legal_prohibition"})
    if record.get("authority_state") != "established":
        blockers.append({"type": "authority_not_established", "actual": record.get("authority_state", "unknown")})
    for requirement in record.get("requires_claims", []):
        actual = claims.get(requirement["claim_id"], "unknown")
        if actual not in requirement.get("accepted_states", []):
            blockers.append({
                "type": "claim_threshold_not_met", "claim_id": requirement["claim_id"],
                "actual": actual, "accepted_states": requirement.get("accepted_states", []),
            })
    served = set(record.get("serves_values", []))
    if not served:
        blockers.append({"type": "no_explicit_value"})
    unknown_values = sorted(served - values)
    if unknown_values:
        blockers.append({"type": "unknown_values", "values": unknown_values})
    return {
        "status": "blocked" if blockers else "eligible_for_human_decision",
        "blockers": blockers,
        "note": "Passing the gate means the option is structured for human review; it is not an automatic recommendation.",
    }
