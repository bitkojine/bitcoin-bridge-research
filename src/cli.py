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

VALID_STATUSES = {"unverified", "supported", "corroborated", "contested", "stale", "retracted", "superseded"}
TREATMENTS = {"supports", "qualifies", "contradicts"}
SOURCE_CURRENCIES = {"current", "superseded", "withdrawn"}
COMMANDS = ["validate", "build", "build-pdf", "infer", "assess", "archive", "verify-evidence"]


def load_model() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def claim_status_matches_treatments(
    status: str, treatments: list[dict], source_by_id: dict, superseded: bool = False
) -> list[str]:
    """The recorded status must match the citator treatment + currency semantics."""
    problems: list[str] = []
    if superseded:
        if status != "superseded":
            problems.append("status must be superseded when superseded_by names a replacement")
        return problems
    if status == "superseded":
        problems.append("status superseded requires superseded_by naming the replacement claims")
        return problems
    treatments = treatments or []
    if treatments and status == "unverified":
        problems.append("status unverified but treatments are recorded")
    contradicts = [t for t in treatments if t.get("treatment") == "contradicts"]
    supports = [t for t in treatments if t.get("treatment") == "supports"]
    withdrawn = [
        t["source_id"] for t in treatments
        if source_by_id.get(t["source_id"], {}).get("currency") == "withdrawn"
    ]
    current_support_ids = {
        t["source_id"] for t in supports
        if source_by_id.get(t["source_id"], {}).get("currency") == "current"
    }
    if contradicts:
        if status != "contested":
            problems.append("status must be contested while contradicting authority is cited")
    elif withdrawn:
        if status != "retracted":
            problems.append("status must be retracted while a withdrawn source is cited")
    elif not current_support_ids:
        if status not in {"stale"}:
            problems.append("status stale requires no current supporting authority")
    else:
        if status == "stale":
            problems.append("status stale but a current supporting source is cited")
        if status == "corroborated" and len(current_support_ids) < 2:
            problems.append("status corroborated requires at least two distinct current supporting sources")
    return problems


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
    source_by_id = {x["id"]: x for x in model.get("sources", [])}
    claim_ids = {x["id"] for x in model.get("claims", [])}

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
        currency = source.get("currency")
        if currency not in SOURCE_CURRENCIES:
            errors.append(f"source {source['id']} has invalid currency")
        replaced_by = source.get("superseded_by") or []
        if replaced_by:
            if currency != "superseded":
                errors.append(f"source {source['id']} superseded_by requires superseded currency")
            for ref in replaced_by:
                if ref not in source_ids:
                    errors.append(f"source {source['id']} superseded_by references unknown source {ref}")
        elif currency == "superseded":
            errors.append(f"source {source['id']} superseded currency requires superseded_by")

    for claim in model.get("claims", []):
        if claim.get("status") not in VALID_STATUSES:
            errors.append(f"claim {claim['id']} has invalid status")
        treatments = claim.get("treatments") or []
        if not treatments:
            errors.append(f"claim {claim['id']} has no treatments")
        for treatment in treatments:
            if treatment.get("treatment") not in TREATMENTS:
                errors.append(f"claim {claim['id']} has invalid treatment {treatment.get('treatment')}")
            if treatment.get("source_id") not in source_ids:
                errors.append(f"claim {claim['id']} references unknown source {treatment.get('source_id')}")
        superseded_by = claim.get("superseded_by") or []
        if superseded_by:
            if claim.get("status") != "superseded":
                errors.append(f"claim {claim['id']} status must be superseded when superseded_by is present")
            for ref in superseded_by:
                if ref not in claim_ids:
                    errors.append(f"claim {claim['id']} superseded_by references unknown claim {ref}")
        elif claim.get("status") == "superseded":
            errors.append(f"claim {claim['id']} status superseded requires superseded_by")
        errors.extend(
            f"claim {claim['id']} {problem}" for problem in claim_status_matches_treatments(
                claim.get("status", ""), treatments, source_by_id, superseded=bool(superseded_by)
            )
        )

    from src.evidence import load_manifest, verify_pin_cites, verify_snapshots

    errors += verify_snapshots(model, load_manifest())
    errors += verify_pin_cites(model, load_manifest())
    return errors


def build_markdown(model: dict) -> str:
    from src.evidence import by_id, load_manifest

    snapshots = by_id(load_manifest())
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
        treatments = ", ".join(
            f"{t['source_id']} ({t['treatment']}, {t.get('locator', 'no locator')})"
            for t in claim["treatments"]
        )
        replaced = f" Superseded by: {', '.join(claim['superseded_by'])}." if claim.get("superseded_by") else ""
        lines.append(f"- **{claim['status']}** - {claim['text']} Treatments: {treatments}.{replaced}")
    lines += ["", "## Sources", ""]
    for source in model["sources"]:
        replaced = ""
        if source.get("superseded_by"):
            replaced = f" Superseded by: {', '.join(source['superseded_by'])}."
        snapshot = snapshots.get(source["id"])
        if snapshot and snapshot.get("status") == "frozen":
            archived = (
                f" Archived: `sha256:{snapshot['sha256'][:16]}…`, "
                f"retrieved `{snapshot['retrieved_at'][:10]}`."
            )
        elif snapshot:
            archived = f" Archived: unavailable (`{snapshot.get('error', 'unknown error')}`)."
        else:
            archived = " Archived: no snapshot."
        lines.append(
            f"- **{source['title']}** (`{source['id']}`, level {source['level']}, currency {source['currency']}). "
            f"Checked on: `{source['checked_on']}`.{archived}{replaced} {source['url']}"
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
    parser.add_argument("--drift", action="store_true", help="re-fetch snapshots and report changed bytes")
    args = parser.parse_args()
    if args.command == "archive":
        from src.evidence import run_archive, snapshot_coverage

        coverage = snapshot_coverage(run_archive(load_model()))
        unavailable = ", ".join(coverage["unavailable"]) or "none"
        print(f"Archived {coverage['frozen']}/{coverage['total']} sources; unavailable: {unavailable}")
        return 1 if coverage["unavailable"] else 0
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
    if args.command == "verify-evidence":
        from src.evidence import check_drift, load_manifest, snapshot_coverage

        manifest = load_manifest()
        coverage = snapshot_coverage(manifest)
        unavailable = ", ".join(coverage["unavailable"]) or "none"
        print(f"Snapshots frozen: {coverage['frozen']}/{coverage['total']} (unavailable: {unavailable})")
        if args.drift:
            drift = check_drift(manifest)
            for item in drift:
                detail = item.get("error") or f"sha256 {item['recorded'][:12]} -> {item['current'][:12]}"
                print(f"DRIFT {item['source_id']}: {detail}")
            if not drift:
                print("No drift: every frozen snapshot still matches its recorded hash.")
            return 1 if drift else 0
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
