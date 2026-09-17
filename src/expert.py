from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Assertion:
    value: Any
    source: str
    rule_id: str | None = None


class ExpertSystem:
    """Small deterministic forward-chaining engine with proof traces."""

    def __init__(self, rules: list[dict]):
        self.rules = sorted(rules, key=lambda rule: (-rule.get("priority", 0), rule["id"]))

    @staticmethod
    def _matches(condition: dict, known: dict[str, list[Assertion]]) -> bool:
        assertions = known.get(condition["fact"], [])
        if "equals" in condition:
            return any(item.value == condition["equals"] for item in assertions)
        if condition.get("known") is True:
            return bool(assertions)
        raise ValueError(f"Unsupported condition: {condition}")

    def infer(self, supplied_facts: dict[str, Any]) -> dict:
        known: dict[str, list[Assertion]] = {
            name: [Assertion(value, "supplied")]
            for name, value in sorted(supplied_facts.items())
        }
        fired: set[str] = set()
        trace: list[dict] = []

        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule["id"] in fired:
                    continue
                if not all(self._matches(condition, known) for condition in rule["when"]["all"]):
                    continue
                fired.add(rule["id"])
                produced = []
                for conclusion in rule["then"]:
                    assertion = Assertion(conclusion["value"], "derived", rule["id"])
                    bucket = known.setdefault(conclusion["fact"], [])
                    if assertion.value not in {item.value for item in bucket}:
                        bucket.append(assertion)
                        changed = True
                    produced.append({"fact": conclusion["fact"], "value": conclusion["value"]})
                trace.append({
                    "rule_id": rule["id"],
                    "description": rule["description"],
                    "because": rule["when"]["all"],
                    "concluded": produced,
                    "sources": rule.get("source_ids", []),
                })

        conflicts = []
        for name, assertions in sorted(known.items()):
            values = []
            for assertion in assertions:
                if assertion.value not in values:
                    values.append(assertion.value)
            if len(values) > 1:
                conflicts.append({"fact": name, "values": values})

        facts = {
            name: [
                {"value": item.value, "source": item.source, "rule_id": item.rule_id}
                for item in assertions
            ]
            for name, assertions in sorted(known.items())
        }
        return {
            "status": "conflict" if conflicts else "complete",
            "facts": facts,
            "trace": trace,
            "conflicts": conflicts,
            "note": "Missing facts remain unknown; they are never treated as false.",
        }


def load_rules(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["rules"]


def validate_rules(rules: list[dict], source_ids: set[str]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for rule in rules:
        rule_id = rule.get("id", "<missing>")
        if rule_id in seen:
            errors.append(f"duplicate rule id: {rule_id}")
        seen.add(rule_id)
        if not rule.get("description"):
            errors.append(f"rule {rule_id} has no description")
        if not isinstance(rule.get("priority"), int):
            errors.append(f"rule {rule_id} priority must be an integer")
        conditions = rule.get("when", {}).get("all", [])
        conclusions = rule.get("then", [])
        if not conditions:
            errors.append(f"rule {rule_id} has no conditions")
        if not conclusions:
            errors.append(f"rule {rule_id} has no conclusions")
        for item in conditions:
            if not item.get("fact") or not ({"equals", "known"} & item.keys()):
                errors.append(f"rule {rule_id} has a malformed condition")
        for item in conclusions:
            if not item.get("fact") or "value" not in item:
                errors.append(f"rule {rule_id} has a malformed conclusion")
        if not rule.get("source_ids"):
            errors.append(f"rule {rule_id} has no sources")
        for source_id in rule.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"rule {rule_id} references unknown source {source_id}")
    return errors
