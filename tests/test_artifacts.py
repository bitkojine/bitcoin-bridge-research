"""Regression tests over shipped artifacts, not just engine mechanics.

These encode the repository's honesty standards as failing tests:
- the web UI must actually boot (every selector in app.js must exist);
- generated snapshots must be freshly derivable from the domain files;
- versions must be consistent across knowledge files;
- rule and assessment facts must come from one shared vocabulary;
- claim statuses must not outrun their sources;
- the research paper's named companies must be declared against the model.
"""

import json
import re
import unittest
from pathlib import Path

from src.assessment import load_profile, validate_profile
from src.build_web import build as build_web
from src.cli import build_markdown, claim_status_matches_sources, load_facts, load_model, validate
from src.expert import load_rules, validate_rules

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
GENERATED = ROOT / "generated"


def knowledge_payload() -> dict:
    raw = (DIST / "knowledge.js").read_text(encoding="utf-8")
    assert raw.startswith("window.KNOWLEDGE = ")
    return json.loads(raw[len("window.KNOWLEDGE = "):-len(";\n")])


class WebArtefactTests(unittest.TestCase):
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
    def test_current_claims_satisfy_semantic_checks(self):
        self.assertEqual(validate(load_model()), [])

    def test_corroborated_requires_two_distinct_sources(self):
        self.assertEqual(claim_status_matches_sources("corroborated", ["a"]), [
            "status corroborated requires at least two distinct sources",
        ])
        self.assertEqual(claim_status_matches_sources("corroborated", ["a", "b"]), [])
        self.assertEqual(claim_status_matches_sources("supported", ["a"]), [])

    def test_every_source_records_a_checked_date(self):
        for source in load_model().get("sources", []):
            self.assertTrue(source.get("checked_on"), f"{source['id']} has no checked_on date")


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


if __name__ == "__main__":
    unittest.main()