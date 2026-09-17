from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "domain" / "model.json"
RULES_PATH = ROOT / "domain" / "rules.json"
ASSESSMENT_PATH = ROOT / "domain" / "assessments" / "custody-readiness.json"
FACTS_PATH = ROOT / "domain" / "facts.json"
OUTPUT_PATH = ROOT / "generated" / "market-map.md"

VALID_STATUSES = {"unverified", "supported", "corroborated", "contested", "stale", "retracted"}
COMMANDS = ["validate", "build", "build-pdf", "infer", "assess"]


def load_model() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def claim_status_matches_sources(status: str, source_ids: list[str]) -> list[str]:
    """The recorded status must not be stronger than the sources can support."""
    distinct = len(set(source_ids))
    if status == "corroborated" and distinct < 2:
        return ["status corroborated requires at least two distinct sources"]
    return []


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
    meta = model.get("meta", {})
    for field in ("title", "version", "generated_on"):
        if not meta.get(field):
            errors.append(f"meta.{field} is required")
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
        if not source.get("checked_on"):
            errors.append(f"source {source['id']} has no checked_on date")

    for claim in model.get("claims", []):
        if claim.get("status") not in VALID_STATUSES:
            errors.append(f"claim {claim['id']} has invalid status")
        if not claim.get("source_ids"):
            errors.append(f"claim {claim['id']} has no sources")
        errors.extend(
            f"claim {claim['id']} {problem}" for problem in claim_status_matches_sources(
                claim.get("status", ""), claim.get("source_ids", [])
            )
        )
        for ref in claim.get("source_ids", []):
            if ref not in source_ids:
                errors.append(f"claim {claim['id']} references unknown source {ref}")
    return errors


def build_markdown(model: dict) -> str:
    bridge_by_id = {x["id"]: x for x in model["bridges"]}
    lines = [
        f"# {model['meta']['title']}", "",
        f"Version: `{model['meta']['version']}`  ",
        f"Snapshot generated on: `{model['meta']['generated_on']}`", "",
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
    lines += ["", "## Sources", ""]
    for source in model["sources"]:
        lines.append(
            f"- **{source['title']}** (`{source['id']}`, level {source['level']}). "
            f"Checked on: `{source['checked_on']}`. {source['url']}"
        )
    lines.append("")
    return "\n".join(lines)


def load_facts() -> dict:
    return json.loads(FACTS_PATH.read_text(encoding="utf-8"))


def validate_versions(model: dict, rules_doc: dict, profile: dict) -> list[str]:
    versions = {
        "model": model.get("meta", {}).get("version"),
        "rules": (rules_doc.get("meta") or {}).get("version"),
        "assessment": profile.get("version"),
        "fact registry": (load_facts().get("meta") or {}).get("version"),
    }
    distinct = {value for value in versions.values() if value}
    if len(distinct) > 1:
        return [f"version mismatch across knowledge files: {versions}"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(prog="research")
    parser.add_argument("command", choices=COMMANDS)
    parser.add_argument("input", nargs="?", help="JSON facts file for the infer command")
    args = parser.parse_args()
    model = load_model()
    errors = validate(model)
    from src.expert import validate_rules

    rules_doc = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    rules = rules_doc["rules"]
    source_ids = {item["id"] for item in model.get("sources", [])}
    fact_names = {item["name"] for item in load_facts().get("facts", [])}
    errors += validate_rules(rules, source_ids, fact_names)
    from src.assessment import load_profile, validate_profile

    profile = load_profile(ASSESSMENT_PATH)
    errors += validate_profile(profile, source_ids, fact_names)
    errors += validate_versions(model, rules_doc, profile)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    if args.command == "validate":
        print("Domain model is valid.")
        return 0
    if args.command == "infer":
        if not args.input:
            parser.error("infer requires a JSON facts file")
        from src.expert import ExpertSystem

        facts = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result = ExpertSystem(rules).infer(facts)
        print(json.dumps(result, indent=2))
        return 2 if result["conflicts"] else 0
    if args.command == "assess":
        if not args.input:
            parser.error("assess requires a JSON facts file")
        from src.assessment import assess, render_markdown

        facts = json.loads(Path(args.input).read_text(encoding="utf-8"))
        result = assess(profile, facts, rules)
        print(render_markdown(result))
        return 0
    if args.command == "build-pdf":
        from src.pdf import build_pdf

        output = build_pdf(model)
        print(f"Built {output.relative_to(ROOT)}")
        return 0
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(build_markdown(model), encoding="utf-8")
    print(f"Built {OUTPUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
