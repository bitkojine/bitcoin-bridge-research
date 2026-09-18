"""Regression tests over shipped artifacts, not just engine mechanics.

These encode the repository's honesty standards as failing tests:
- the web UI must actually boot (every selector in app.js must exist);
- generated snapshots must be freshly derivable from the domain files;
- versions must be consistent across knowledge files;
- rule and assessment facts must come from one shared vocabulary;
- claim statuses must not outrun their sources;
- the research paper's named companies must be declared against the model;
- the C4 architecture document must not drift from the code it describes.
"""

import json
import re
import unittest
from pathlib import Path

from src.assessment import load_profile, validate_profile
from src.build_web import build as build_web
from src.cli import build_markdown, claim_status_matches_treatments, load_facts, load_model, validate
from src.evidence import load_manifest, snapshot_coverage
from src.expert import load_rules, validate_rules

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
GENERATED = ROOT / "generated"


def knowledge_payload() -> dict:
    raw = (DIST / "knowledge.js").read_text(encoding="utf-8")
    assert raw.startswith("window.KNOWLEDGE = ")
    return json.loads(raw[len("window.KNOWLEDGE = "):-len(";\n")])


class WebArtefactTests(unittest.TestCase):
    def test_pages_workflow_deploys_only_static_dist_after_checks(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("pages: write", workflow)
        self.assertIn("id-token: write", workflow)
        self.assertIn("python -m src.cli validate", workflow)
        self.assertIn("python -m unittest discover -s tests", workflow)
        self.assertIn("path: dist", workflow)
        self.assertIn("actions/deploy-pages@v4", workflow)
        self.assertTrue((DIST / ".nojekyll").exists())

    def test_every_selector_in_app_js_exists_in_index_html(self):
        app = (DIST / "app.js").read_text(encoding="utf-8")
        index = (DIST / "index.html").read_text(encoding="utf-8")
        selectors = re.findall(r"querySelector\('#([a-zA-Z0-9_-]+)'\)", app)
        self.assertTrue(selectors, "expected to find id selectors in app.js")
        missing = [id_ for id_ in selectors if f'id="{id_}"' not in index]
        self.assertEqual(missing, [], "app.js references ids missing from index.html")

    def test_knowledge_snapshot_is_fresh(self):
        fresh = build_web().read_text(encoding="utf-8")
        self.assertEqual((DIST / "knowledge.js").read_text(encoding="utf-8"), fresh)

    def test_web_exposes_executable_philosophy_model(self):
        payload = knowledge_payload()
        self.assertEqual(
            [stage["id"] for stage in payload["philosophy"]["stages"]],
            ["ontology", "data", "epistemology", "axiology", "action"],
        )
        app = (DIST / "app.js").read_text(encoding="utf-8")
        self.assertIn("philosophy.gates", app)
        self.assertIn("philosophy.invariants", app)

    def test_market_map_is_fresh(self):
        current = (GENERATED / "market-map.md").read_text(encoding="utf-8")
        self.assertEqual(build_markdown(load_model()), current)

    def test_market_map_header_is_truthful(self):
        market_map = (GENERATED / "market-map.md").read_text(encoding="utf-8")
        self.assertIn("Snapshot generated on:", market_map)
        self.assertNotIn("Verified on:", market_map)

    def test_ui_shows_generated_date_not_verified_claim(self):
        index = (DIST / "index.html").read_text(encoding="utf-8")
        self.assertIn("Snapshot generated", index)
        self.assertNotIn("> Verified <", index)


class VersionTests(unittest.TestCase):
    def test_knowledge_versions_agree(self):
        model = load_model()
        rules_doc = json.loads((ROOT / "domain/rules.json").read_text(encoding="utf-8"))
        profile = load_profile(ROOT / "domain/assessments/custody-readiness.json")
        facts_doc = load_facts()
        versions = {
            model["meta"]["version"],
            rules_doc["meta"]["version"],
            profile["version"],
            facts_doc["meta"]["version"],
        }
        self.assertEqual(len(versions), 1)

    def test_pyproject_version_matches_model(self):
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        match = re.search(r'^version = "(.+)"$', pyproject, re.MULTILINE)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), load_model()["meta"]["version"])

    def test_market_map_version_matches_model(self):
        market_map = (GENERATED / "market-map.md").read_text(encoding="utf-8")
        self.assertIn(f"Version: `{load_model()['meta']['version']}`", market_map)


class RegistryTests(unittest.TestCase):
    def test_rules_use_registered_facts_only(self):
        source_ids = {s["id"] for s in load_model()["sources"]}
        fact_names = {f["name"] for f in load_facts()["facts"]}
        errors = validate_rules(load_rules(ROOT / "domain/rules.json"), source_ids, fact_names)
        self.assertEqual(errors, [])

    def test_assessment_uses_registered_facts_only(self):
        source_ids = {s["id"] for s in load_model()["sources"]}
        fact_names = {f["name"] for f in load_facts()["facts"]}
        profile = load_profile(ROOT / "domain/assessments/custody-readiness.json")
        errors = validate_profile(profile, source_ids, fact_names)
        self.assertEqual(errors, [])

    def test_registry_covers_every_requirement(self):
        profile = load_profile(ROOT / "domain/assessments/custody-readiness.json")
        names = {f["name"] for f in load_facts()["facts"]}
        for requirement in profile["requirements"]:
            self.assertIn(requirement["fact"], names)
            applies_when = requirement.get("applies_when")
            if applies_when:
                self.assertIn(applies_when["fact"], names)


class ClaimHonestyTests(unittest.TestCase):
    def setUp(self):
        self.sources = {s["id"]: s for s in load_model().get("sources", [])}

    def test_current_claims_satisfy_semantic_checks(self):
        self.assertEqual(validate(load_model()), [])

    def test_corroborated_requires_two_distinct_current_supporting_sources(self):
        src_a = {"currency": "current"}
        self.assertEqual(claim_status_matches_treatments("corroborated", [
            {"source_id": "a", "treatment": "supports"},
        ], {"a": src_a}), ["status corroborated requires at least two distinct current supporting sources"])
        self.assertEqual(claim_status_matches_treatments("corroborated", [
            {"source_id": "a", "treatment": "supports"},
            {"source_id": "b", "treatment": "supports"},
        ], {"a": src_a, "b": src_a}), [])
        self.assertEqual(claim_status_matches_treatments("supported", [
            {"source_id": "a", "treatment": "supports"},
        ], {"a": src_a}), [])

    def test_contested_requires_contradicting_authority(self):
        treatments = [{"source_id": "a", "treatment": "contradicts"}]
        self.assertIn("status must be contested", claim_status_matches_treatments("supported", treatments, {"a": {"currency": "current"}})[0])
        self.assertEqual(claim_status_matches_treatments("contested", treatments, {"a": {"currency": "current"}}), [])

    def test_retracted_requires_a_withdrawn_source(self):
        treatments = [{"source_id": "a", "treatment": "supports"}]
        self.assertIn("status must be retracted", claim_status_matches_treatments("supported", treatments, {"a": {"currency": "withdrawn"}})[0])
        self.assertEqual(claim_status_matches_treatments("retracted", treatments, {"a": {"currency": "withdrawn"}}), [])

    def test_stale_requires_no_current_support(self):
        treatments = [{"source_id": "a", "treatment": "supports"}]
        self.assertEqual(claim_status_matches_treatments("stale", treatments, {"a": {"currency": "superseded"}}), [])
        self.assertIn("status stale but a current supporting source", claim_status_matches_treatments("stale", treatments, {"a": {"currency": "current"}})[0])

    def test_unverified_has_no_treatments(self):
        self.assertIn("status unverified but treatments", claim_status_matches_treatments("unverified", [{"source_id": "a", "treatment": "supports"}], {"a": {"currency": "current"}})[0])

    def test_superseded_requires_superseded_by(self):
        self.assertIn("status superseded requires superseded_by",
                      claim_status_matches_treatments("superseded", [{"source_id": "a", "treatment": "supports"}], {"a": {"currency": "current"}})[0])
        self.assertEqual(claim_status_matches_treatments("superseded", [], {}, superseded=True), [])

    def test_source_currency_rules_enforced_by_validate(self):
        model = load_model()
        model["sources"].append({"id": "x", "level": 3, "checked_on": "2026-09-17", "currency": "superseded"})
        errors = validate(model)
        self.assertTrue(any("superseded currency requires superseded_by" in e for e in errors))
        model["sources"][-1]["superseded_by"] = ["does-not-exist"]
        errors = validate(model)
        self.assertTrue(any("references unknown source" in e for e in errors))
        model["sources"][-1]["superseded_by"] = ["bip-322"]
        errors = validate(model)
        self.assertTrue(all("source x" not in e for e in errors))

    def test_claim_treatment_rules_enforced_by_validate(self):
        model = load_model()
        model["claims"][0]["status"] = "superseded"
        errors = validate(model)
        self.assertTrue(any("status superseded requires superseded_by" in e for e in errors))
        model["claims"][0]["superseded_by"] = ["custody-needs-law"]
        errors = validate(model)
        self.assertTrue(all("claim signature-not-title" not in e for e in errors))
        model["claims"][0]["superseded_by"] = ["does-not-exist"]
        errors = validate(model)
        self.assertTrue(any("references unknown claim" in e for e in errors))

    def test_every_source_records_checked_date_and_currency(self):
        for source in load_model().get("sources", []):
            self.assertTrue(source.get("checked_on"), f"{source['id']} has no checked_on date")
            self.assertIn(source.get("currency"), {"current", "superseded", "withdrawn"})

    def test_every_claim_cites_only_known_sources_through_treatments(self):
        model = load_model()
        source_ids = {s["id"] for s in model["sources"]}
        for claim in model["claims"]:
            self.assertTrue(claim.get("treatments"), f"{claim['id']} has no treatments")
            for treatment in claim["treatments"]:
                self.assertIn(treatment["source_id"], source_ids)
                self.assertIn(treatment["treatment"], {"supports", "qualifies", "contradicts"})

    def test_every_treatment_has_a_pin_cite_on_a_frozen_source(self):
        from src.evidence import by_id

        model = load_model()
        snapshots = by_id(load_manifest())
        for claim in model["claims"]:
            for treatment in claim["treatments"]:
                label = f"{claim['id']} -> {treatment['source_id']}"
                self.assertTrue(treatment.get("locator"), f"{label} has no locator")
                self.assertTrue(treatment.get("quote"), f"{label} has no quote")
                self.assertEqual(
                    (snapshots.get(treatment["source_id"]) or {}).get("status"), "frozen",
                    f"{label} is not backed by a frozen snapshot",
                )


class PaperConsistencyTests(unittest.TestCase):
    def setUp(self):
        self.model = load_model()
        model_names = {c["name"] for c in self.model["companies"]}
        self.index = json.loads(
            (ROOT / "publications/v0.1.0/PAPER_COMPANIES.json").read_text(encoding="utf-8")
        )
        self.model_names = model_names

    def test_in_model_entries_exist_in_the_model(self):
        for entry in self.index["companies"]:
            if entry["in_model"]:
                self.assertIn(
                    entry["name"], self.model_names,
                    f"paper index marks {entry['name']} in_model but it is absent from domain/model.json",
                )

    def test_out_of_model_entries_are_flagged_illustrative(self):
        for entry in self.index["companies"]:
            if not entry["in_model"]:
                self.assertTrue(
                    entry.get("illustrative_only"),
                    f"paper index names {entry['name']} without an in_model record or illustrative flag",
                )

    def test_every_model_company_is_inventoried_in_the_paper_index(self):
        indexed = {entry["name"] for entry in self.index["companies"] if entry["in_model"]}
        self.assertEqual(
            indexed, self.model_names,
            "every domain model company must have an in_model entry in PAPER_COMPANIES.json",
        )

    def test_paper_notice_exists(self):
        notice = ROOT / "publications/v0.1.0/NOTICE.md"
        self.assertTrue(notice.exists())
        self.assertIn("not generated", notice.read_text(encoding="utf-8"))


class ArchitectureDocTests(unittest.TestCase):
    """The C4 document (docs/architecture-c4.md) must not drift from the code.

    Every backticked file path or glob must resolve, every Level 4 anchor must
    point at the named function, the CLI subcommand list must match argparse
    choices, and the snapshot contract table must equal the live knowledge.
    """

    DOC = ROOT / "docs" / "architecture-c4.md"

    def read_doc(self) -> str:
        return self.DOC.read_text(encoding="utf-8")

    def test_referenced_files_and_globs_exist(self):
        text = self.read_doc()
        tokens = re.findall(r"`([A-Za-z0-9_./*-]+\.(?:py|json|yml|yaml|js|css|html|md|toml))`", text)
        self.assertTrue(tokens, "expected backticked file references in the C4 document")
        for token in tokens:
            if "*" in token:
                self.assertTrue(list(ROOT.glob(token)), f"C4 glob has no matches: {token}")
            else:
                self.assertTrue((ROOT / token).exists(), f"C4 references missing file: {token}")

    def test_level4_anchors_resolve_to_the_named_function(self):
        text = self.read_doc()
        anchors = re.findall(
            r"`(src/[a-zA-Z0-9_]+\.py):(\d+)`[^`]*`([a-zA-Z_][a-zA-Z0-9_]*(?:\(\))?)`", text
        )
        self.assertTrue(anchors, "expected src file:line anchors in the C4 Level 4 section")
        for path, line_str, name in anchors:
            line = int(line_str)
            name = name.rstrip("()")
            source = (ROOT / path).read_text(encoding="utf-8").splitlines()
            message = f"anchor {path}:{line} ({name})"
            self.assertLessEqual(line, len(source), f"{message} is past the end of the file")
            self.assertIn(
                f"def {name}(", source[line - 1],
                f"{message} does not define the named function on that line",
            )

    def test_snapshot_contract_matches_live_knowledge(self):
        text = self.read_doc()
        match = re.search(r"\|\s*metric\s*\|\s*value\s*\|\n((?:\|[^\n]+\|\n)+)", text)
        self.assertIsNotNone(match, "snapshot contract table not found in the C4 document")
        expected = {}
        for row in match.group(1).strip().splitlines():
            cells = [cell.strip() for cell in row.split("|")[1:-1]]
            if all(re.fullmatch(r":?-+:?", cell or "") for cell in cells):
                continue  # markdown table separator row
            self.assertEqual(len(cells), 2, f"malformed snapshot row: {row}")
            expected[cells[0]] = cells[1]

        model = load_model()
        rules_doc = json.loads((ROOT / "domain/rules.json").read_text(encoding="utf-8"))
        profile = load_profile(ROOT / "domain/assessments/custody-readiness.json")
        philosophy = json.loads((ROOT / "domain/philosophy.json").read_text(encoding="utf-8"))
        eligibility = json.loads(
            (ROOT / "domain/legal/allianz-y3-eligibility.json").read_text(encoding="utf-8")
        )
        transition = json.loads(
            (ROOT / "domain/cases/allianz-y3-bitcoin.json").read_text(encoding="utf-8")
        )
        live = {
            "model version": model["meta"]["version"],
            "bitcoin capabilities": len(model["bitcoin_capabilities"]),
            "finance requirements": len(model["finance_requirements"]),
            "legal requirements": len(model["legal_requirements"]),
            "bridges": len(model["bridges"]),
            "companies": len(model["companies"]),
            "sources": len(model["sources"]),
            "archived source snapshots": snapshot_coverage(load_manifest())["frozen"],
            "claims": len(model["claims"]),
            "assessment requirements": len(profile["requirements"]),
            "inference rules": len(rules_doc["rules"]),
            "fact registry facts": len(load_facts()["facts"]),
            "philosophy stages": len(philosophy["stages"]),
            "philosophy gates": len(philosophy["gates"]),
            "legal eligibility authorities": len(eligibility["authorities"]),
            "legal eligibility provisions": len(eligibility["provisions"]),
            "legal eligibility routes": len(eligibility["routes"]),
            "transition verified facts": len(transition["verified_facts"]),
            "transition pathways": len(transition["pathways"]),
        }
        self.assertEqual(set(expected), set(live), "snapshot metric names differ from live knowledge")
        for metric, value in live.items():
            self.assertEqual(expected[metric], str(value), f"snapshot metric is stale: {metric}")

    def test_cli_subcommands_match_argparse_choices(self):
        text = self.read_doc()
        for line in text.splitlines():
            if line.strip().startswith("- CLI subcommands:"):
                break
        else:
            self.fail("CLI subcommands bullet not found in the C4 document")
        from src.cli import COMMANDS

        doc_commands = re.findall(r"`([^`]+)`", line)
        self.assertEqual(doc_commands, COMMANDS)


class RoadmapTests(unittest.TestCase):
    """The roadmap (docs/roadmap.md) must not claim progress reality denies.

    While evidence/claims/ is empty the only honest CURRENT-STAGE marker is
    Seed. When real evidence records land, the marker must move to the next
    stage; the test forces the document to track the repository, not the
    other way around.
    """

    ROADMAP = ROOT / "docs" / "roadmap.md"

    def test_current_stage_marker_matches_reality(self):
        text = self.ROADMAP.read_text(encoding="utf-8")
        marker = re.search(r"CURRENT-STAGE:\s*([A-Za-z]+)", text)
        self.assertIsNotNone(marker, "roadmap must declare a CURRENT-STAGE marker")
        observed = marker.group(1)
        claims_dir = ROOT / "evidence" / "claims"
        has_real_evidence = claims_dir.is_dir() and bool(list(claims_dir.rglob("*.json")))
        expected = "Sprout" if has_real_evidence else "Seed"
        self.assertEqual(observed, expected, "roadmap stage marker disagrees with the repository")

    def test_roadmap_marks_seed_as_current_until_evidence_exists(self):
        text = self.ROADMAP.read_text(encoding="utf-8")
        self.assertIn("Stage 0", text)
        self.assertIn("we are here today", text)
        self.assertIn("None of the later stages exist yet", text)


if __name__ == "__main__":
    unittest.main()
