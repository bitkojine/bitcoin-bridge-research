from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALL_FACTS = {
    "customer_identity_evidenced": True,
    "legal_authority_evidenced": True,
    "asset_scope_approved": True,
    "exclusive_control_evidenced": True,
    "customer_assets_segregated": True,
    "books_reconcile_to_chain": True,
    "key_lifecycle_controls_documented": True,
    "recovery_and_compromise_plan_tested": True,
    "cybersecurity_controls_assessed": True,
    "subcustodian_used": True,
    "subcustodian_due_diligence_complete": True,
    "customer_agreement_complete": True,
    "independent_assurance_current": True,
}


def record(number: int, fact: str, value: bool) -> dict:
    return {
        "id": f"EV-{number:03d}",
        "assertion": {"fact": fact, "value": value, "subject_id": "ORG-EXAMPLE"},
        "artifact": {
            "type": "synthetic-example-record",
            "title": f"Example evidence for {fact}",
            "integrity_not_recorded_reason": "Synthetic example; no real artifact exists."
        },
        "issuer": {"id": "ORG-EXAMPLE", "name": "Example Custody Institution", "type": "organization"},
        "provenance": {
            "obtained_at": "2026-09-17T09:00:00Z",
            "method": "Generated as non-production repository example",
            "chain_of_custody": "None; synthetic data"
        },
        "scope": {
            "jurisdictions": ["US-NY"],
            "description": "Synthetic institutional Bitcoin custody example",
            "valid_from": "2026-01-01T00:00:00Z",
            "valid_until": "2026-12-31T23:59:59Z"
        },
        "review": {
            "status": "accepted",
            "reviewed_at": "2026-09-17T10:00:00Z",
            "method": "Synthetic example review; no professional validation",
            "notes": "Demonstrates data shape and engine behavior only.",
            "reviewer": {"id": "PERSON-EXAMPLE", "name": "Example Reviewer", "role": "synthetic test reviewer"}
        }
    }


def case(case_id: str, title: str, facts: dict[str, bool]) -> dict:
    return {
        "case": {
            "schema_version": "1.0.0",
            "id": case_id,
            "title": title,
            "assessed_at": "2026-09-17T12:00:00Z",
            "jurisdiction": "US-NY",
            "subject_id": "ORG-EXAMPLE"
        },
        "evidence": [record(index, fact, value) for index, (fact, value) in enumerate(facts.items(), 1)]
    }


def build() -> None:
    complete = case("CASE-COMPLETE-SYNTHETIC", "Synthetic complete custody case", ALL_FACTS)
    gaps = case("CASE-GAPS-SYNTHETIC", "Synthetic custody case with gaps", {
        "customer_identity_evidenced": True,
        "legal_authority_evidenced": False,
        "asset_scope_approved": True,
        "exclusive_control_evidenced": True,
        "customer_assets_segregated": True,
        "books_reconcile_to_chain": False,
        "key_lifecycle_controls_documented": True,
        "subcustodian_used": False,
        "customer_agreement_complete": True,
    })
    for name, data in (
        ("custody-readiness-complete.json", complete),
        ("custody-readiness-gaps.json", gaps),
    ):
        (ROOT / "examples" / name).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
