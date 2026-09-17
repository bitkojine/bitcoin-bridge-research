from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "domain" / "model.json"
OUTPUT_PATH = ROOT / "generated" / "market-map.md"

VALID_STATUSES = {"unverified", "supported", "corroborated", "contested", "stale", "retracted"}


def load_model() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def duplicates(items: list[dict]) -> set[str]:
    seen: set[str] = set()
    repeated: set[str] = set()
    for item in items:
        item_id = item["id"]
        if item_id in seen:
            repeated.add(item_id)
        seen.add(item_id)
    return repeated


def validate(model: dict) -> list[str]:
    errors: list[str] = []
    collections = [
        "bitcoin_capabilities", "finance_requirements", "legal_requirements",
        "bridges", "companies", "sources", "claims"
    ]
    for name in collections:
        if name not in model or not isinstance(model[name], list):
            errors.append(f"{name} must be a list")
            continue
        for duplicate in sorted(duplicates(model[name])):
            errors.append(f"duplicate {name} id: {duplicate}")

    capability_ids = {x["id"] for x in model.get("bitcoin_capabilities", [])}
    finance_ids = {x["id"] for x in model.get("finance_requirements", [])}
    legal_ids = {x["id"] for x in model.get("legal_requirements", [])}
    bridge_ids = {x["id"] for x in model.get("bridges", [])}
    source_ids = {x["id"] for x in model.get("sources", [])}

    for capability in model.get("bitcoin_capabilities", []):
        if not capability.get("formula"):
            errors.append(f"capability {capability['id']} has no formula")
        if not capability.get("terms"):
            errors.append(f"capability {capability['id']} has no term definitions")

    for bridge in model.get("bridges", []):
        for ref in bridge.get("bitcoin_capabilities", []):
            if ref not in capability_ids:
                errors.append(f"bridge {bridge['id']} references unknown capability {ref}")
        for ref in bridge.get("finance_requirements", []):
            if ref not in finance_ids:
                errors.append(f"bridge {bridge['id']} references unknown finance requirement {ref}")
        for ref in bridge.get("legal_requirements", []):
            if ref not in legal_ids:
                errors.append(f"bridge {bridge['id']} references unknown legal requirement {ref}")

    for company in model.get("companies", []):
        if not company.get("bridges"):
            errors.append(f"company {company['id']} has no bridge classification")
        for ref in company.get("bridges", []):
            if ref not in bridge_ids:
                errors.append(f"company {company['id']} references unknown bridge {ref}")

    for source in model.get("sources", []):
        if source.get("level") not in {1, 2, 3, 4, 5}:
            errors.append(f"source {source['id']} has invalid evidence level")

    for claim in model.get("claims", []):
        if claim.get("status") not in VALID_STATUSES:
            errors.append(f"claim {claim['id']} has invalid status")
        if not claim.get("source_ids"):
            errors.append(f"claim {claim['id']} has no sources")
        for ref in claim.get("source_ids", []):
            if ref not in source_ids:
                errors.append(f"claim {claim['id']} references unknown source {ref}")
    return errors


def build_markdown(model: dict) -> str:
    bridge_by_id = {x["id"]: x for x in model["bridges"]}
    lines = [
        f"# {model['meta']['title']}", "",
        f"Version: `{model['meta']['version']}`  ",
        f"Verified on: `{model['meta']['verified_on']}`", "",
        model["meta"]["thesis"], "", "## Bitcoin capabilities", ""
    ]
    for item in model["bitcoin_capabilities"]:
        lines += [f"### {item['name']}", "", f"`{item['formula']}`", ""]
        for term, definition in item["terms"].items():
            lines.append(f"- **{term}**: {definition}")
        lines += ["", f"Establishes: {item['establishes']}", ""]

    lines += ["## Bridge market", ""]
    for bridge in model["bridges"]:
        companies = sorted(x["name"] for x in model["companies"] if bridge["id"] in x["bridges"])
        lines += [f"### {bridge['name']}", "", "Companies: " + ", ".join(f"**{x}**" for x in companies), ""]

    lines += ["## Claims", ""]
    for claim in model["claims"]:
        lines.append(f"- **{claim['status']}** - {claim['text']} Sources: {', '.join(claim['source_ids'])}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(prog="research")
    parser.add_argument("command", choices=["validate", "build"])
    args = parser.parse_args()
    model = load_model()
    errors = validate(model)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.command == "validate":
        print("Domain model is valid.")
        return 0
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_markdown(model), encoding="utf-8")
    print(f"Built {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

