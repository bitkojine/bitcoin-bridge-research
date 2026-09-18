from __future__ import annotations

import json
from datetime import date
from pathlib import Path


OFFICIAL_SOURCE_KINDS = {"official_register", "authentic_official_journal"}
RESULTS = {
    "prohibited", "permission_not_established", "applicability_disputed",
    "professional_interpretation_required", "personal_route_subject_to_conditions",
}


def load_eligibility(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_eligibility(model: dict) -> list[str]:
    errors: list[str] = []
    authority_ids = {item.get("id") for item in model.get("authorities", [])}
    route_ids: set[str] = set()
    for authority in model.get("authorities", []):
        for field in ("id", "title", "publisher", "source_kind", "official_uri", "eli_mapping"):
            if not authority.get(field):
                errors.append(f"authority {authority.get('id')} has no {field}")
        if authority.get("source_kind") not in OFFICIAL_SOURCE_KINDS:
            errors.append(f"authority {authority.get('id')} is not an official legal source")
    for provision in model.get("provisions", []):
        if provision.get("authority_id") not in authority_ids:
            errors.append(f"provision {provision.get('id')} references unknown authority")
        for field in ("id", "citation", "text", "effect", "targets", "force", "interpretation_limits"):
            if not provision.get(field):
                errors.append(f"provision {provision.get('id')} has no {field}")
    for route in model.get("routes", []):
        route_id = route.get("id")
        if route_id in route_ids:
            errors.append(f"duplicate route id: {route_id}")
        route_ids.add(route_id)
        for field in ("id", "label", "instrument_class", "classification_basis", "classification_state", "desired_effect"):
            if not route.get(field):
                errors.append(f"route {route_id} has no {field}")
    return errors


def recorded_in_force(provision: dict, on_date: str) -> bool:
    """Evaluate recorded dates; this does not authenticate or legally interpret them."""
    target = date.fromisoformat(on_date)
    force = provision["force"]
    starts = date.fromisoformat(force["first_date_in_force"])
    ends = date.fromisoformat(force["date_no_longer_in_force"]) if force.get("date_no_longer_in_force") else None
    return force.get("recorded_status") == "in_force" and starts <= target and (ends is None or target < ends)


def evaluate_route(model: dict, route_id: str, on_date: str | None = None) -> dict:
    route = next((item for item in model["routes"] if item["id"] == route_id), None)
    if route is None:
        raise KeyError(f"unknown route: {route_id}")
    target_date = on_date or model["meta"]["as_of"]
    if route["classification_state"] == "interpretation_required":
        status = "professional_interpretation_required"
        matched = []
    elif route["classification_state"] == "conditional":
        status = "personal_route_subject_to_conditions"
        matched = []
    else:
        matched = [
            provision for provision in model["provisions"]
            if route["instrument_class"] in provision["targets"] and recorded_in_force(provision, target_date)
        ]
        status = "prohibited" if any(item["effect"] == "prohibits" for item in matched) else "permission_not_established"
    assert status in RESULTS
    return {
        "route_id": route_id,
        "label": route["label"],
        "as_of": target_date,
        "status": status,
        "instrument_class": route["instrument_class"],
        "classification_state": route["classification_state"],
        "classification_basis": route["classification_basis"],
        "matched_provisions": [
            {"id": item["id"], "citation": item["citation"], "text": item["text"]}
            for item in matched
        ],
        "force_claim": "recorded_in_force" if matched else "not_evaluated_or_no_match",
        "warning": model["meta"]["not_advice"],
    }


def evaluate_all(model: dict, on_date: str | None = None) -> list[dict]:
    return [evaluate_route(model, route["id"], on_date) for route in model["routes"]]
