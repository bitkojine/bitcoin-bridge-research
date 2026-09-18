from __future__ import annotations

import json
from pathlib import Path


BLOCKER_STATES = {"established", "unknown", "contested"}
PATHWAY_STATES = {
    "blocked",
    "prohibited_under_current_law",
    "researchable",
    "legally_available_in_principle",
    "potentially_available_subject_to_conditions",
    "available_subject_to_personal_limits",
}


def load_case(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_case_study(case: dict) -> list[str]:
    errors: list[str] = []
    meta = case.get("meta", {})
    for field in ("id", "title", "as_of", "jurisdiction", "status", "purpose", "not_advice"):
        if not meta.get(field):
            errors.append(f"meta.{field} is required")
    source_ids = {item.get("id") for item in case.get("sources", [])}
    blocker_ids = {item.get("id") for item in case.get("blockers", [])}
    if not case.get("verified_facts"):
        errors.append("verified_facts must not be empty")
    if not case.get("blockers"):
        errors.append("blockers must not be empty")
    if not case.get("pathways"):
        errors.append("pathways must not be empty")
    inquiry = case.get("policy_inquiry", {})
    if inquiry:
        for field in ("question", "current_answer", "limits"):
            if not inquiry.get(field):
                errors.append(f"policy_inquiry.{field} is required")
        if not inquiry.get("observations"):
            errors.append("policy_inquiry.observations must not be empty")
        if not inquiry.get("hypotheses"):
            errors.append("policy_inquiry.hypotheses must not be empty")
        for hypothesis in inquiry.get("hypotheses", []):
            for field in ("claim", "status", "support", "counterevidence", "would_change_assessment"):
                if not hypothesis.get(field):
                    errors.append(f"policy hypothesis {hypothesis.get('id')} has no {field}")
    classification = case.get("classification_analysis", {})
    if classification:
        for field in ("question", "legal_answer", "community_claim", "practical_effect"):
            if not classification.get(field):
                errors.append(f"classification_analysis.{field} is required")
        if not classification.get("distinctions"):
            errors.append("classification_analysis.distinctions must not be empty")
    for fact in case.get("verified_facts", []):
        if fact.get("source_id") not in source_ids:
            errors.append(f"fact {fact.get('id')} references unknown source {fact.get('source_id')}")
        for field in ("statement", "quote", "locator", "implication"):
            if not fact.get(field):
                errors.append(f"fact {fact.get('id')} has no {field}")
    for blocker in case.get("blockers", []):
        if blocker.get("status") not in BLOCKER_STATES:
            errors.append(f"blocker {blocker.get('id')} has invalid status")
        for field in ("question", "finding", "unlock"):
            if not blocker.get(field):
                errors.append(f"blocker {blocker.get('id')} has no {field}")
    for pathway in case.get("pathways", []):
        if pathway.get("state") not in PATHWAY_STATES:
            errors.append(f"pathway {pathway.get('id')} has invalid state")
        if not isinstance(pathway.get("on_chain"), bool):
            errors.append(f"pathway {pathway.get('id')} on_chain must be Boolean")
        for blocker_id in pathway.get("requires", []):
            if blocker_id not in blocker_ids:
                errors.append(f"pathway {pathway.get('id')} references unknown blocker {blocker_id}")
    prohibited = {
        pathway.get("id") for pathway in case.get("pathways", [])
        if pathway.get("state") == "prohibited_under_current_law"
    }
    for pathway_id in prohibited:
        pathway = next(item for item in case["pathways"] if item.get("id") == pathway_id)
        if not pathway.get("legal_basis"):
            errors.append(f"pathway {pathway_id} has no legal_basis")
    return errors


def render_case_study(case: dict) -> str:
    meta, transition = case["meta"], case["transition"]
    lines = [
        f"# {meta['title']}", "", f"As of: `{meta['as_of']}` · Jurisdiction: {meta['jurisdiction']}", "",
        f"> {meta['not_advice']}", "", "## Decision question", "", transition["decision_question"], "",
        "## What is already established", "",
    ]
    for fact in case["verified_facts"]:
        lines.append(f"- **{fact['statement']}** {fact['implication']} [{fact['source_id']}, {fact['locator']}]")
        lines.append(f"  - Source text: “{fact['quote']}”")
    inquiry = case.get("policy_inquiry")
    if inquiry:
        lines += ["", "## Policy-consistency inquiry", "", f"**Question:** {inquiry['question']}", "",
                  f"**Current answer:** {inquiry['current_answer']}", "", "### Observations", ""]
        lines += [f"- {item}" for item in inquiry["observations"]]
        lines += ["", "### Competing explanations", ""]
        for hypothesis in inquiry["hypotheses"]:
            lines += [f"#### {hypothesis['id']} · {hypothesis['claim']}", "",
                      f"Status: **{hypothesis['status']}**", "", f"Support: {hypothesis['support']}", "",
                      f"Counterevidence: {hypothesis['counterevidence']}", "",
                      f"Would change the assessment: {hypothesis['would_change_assessment']}", ""]
        lines += [f"**Limits:** {inquiry['limits']}", ""]
    classification = case.get("classification_analysis")
    if classification:
        lines += ["", "## Is Bitcoin legally 'crypto'?", "", f"**Question:** {classification['question']}", "",
                  f"**Legal answer:** {classification['legal_answer']}", "",
                  f"**Bitcoiner claim:** {classification['community_claim']}", "", "### Distinctions", ""]
        lines += [f"- **{item['level']}:** {item['meaning']}" for item in classification["distinctions"]]
        lines += ["", f"**Practical effect:** {classification['practical_effect']}", ""]
    lines += ["", "## Blockers", ""]
    for blocker in case["blockers"]:
        lines += [f"### {blocker['id']} · {blocker['question']}", "", f"Status: **{blocker['status']}**", "",
                  blocker["finding"], "", f"Unlock: {blocker['unlock']}", ""]
    lines += ["## Pathways", ""]
    for pathway in case["pathways"]:
        chain = "on-chain" if pathway["on_chain"] else "off-chain exposure or pension transfer"
        required = ", ".join(pathway["requires"]) or "no case blockers; personal eligibility still applies"
        lines += [f"### {pathway['id']} · {pathway['name']}", "", f"State: **{pathway['state']}** · Form: {chain}", "",
                  pathway["meaning"], "", f"Requires: {required}", "", f"Warning: {pathway['warning']}", ""]
        if pathway.get("legal_basis"):
            lines += [f"Legal basis: {pathway['legal_basis']}", ""]
    lines += ["## Actions for the participant", ""]
    lines += [f"{index}. {action}" for index, action in enumerate(case["participant_actions"], 1)]
    lines += ["", "## Sources", ""]
    lines += [f"- **{source['title']}** — {source['issuer']}, checked `{source['checked_on']}`. {source['url']}"
              for source in case["sources"]]
    lines.append("")
    return "\n".join(lines)
