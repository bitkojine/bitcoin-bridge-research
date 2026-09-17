import json
import unittest
from pathlib import Path

from src.assessment import assess, derive_facts, load_profile, render_markdown, validate_case
from src.build_example_cases import ALL_FACTS, case as evidence_case, record

ROOT = Path(__file__).resolve().parents[1]


class CustodyReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_profile(ROOT / "domain/assessments/custody-readiness.json")
        cls.cases = json.loads(
            (ROOT / "tests/fixtures/custody-readiness-cases.json").read_text(encoding="utf-8")
        )

    def test_scenario_cases(self):
        for scenario in self.cases:
            with self.subTest(case=scenario["name"]):
                case = evidence_case("TEST-CASE", scenario["name"], scenario["facts"])
                self.assertEqual(assess(self.profile, case)["outcome"], scenario["outcome"])

    def test_every_requirement_has_sources(self):
        for requirement in self.profile["requirements"]:
            self.assertTrue(requirement["source_ids"])

    def test_report_names_blockers_and_unknowns(self):
        result = assess(self.profile, evidence_case(
            "TEST-GAP", "Authority gap", {"legal_authority_evidenced": False}
        ))
        report = render_markdown(result)
        self.assertIn("Blocking gaps", report)
        self.assertIn("Legal authority and mandate", report)
        self.assertIn("Missing evidence", report)

    def test_subcustodian_review_is_not_required_when_unused(self):
        facts = {**ALL_FACTS, "subcustodian_used": False}
        del facts["subcustodian_due_diligence_complete"]
        result = assess(self.profile, evidence_case("TEST-DIRECT", "Direct custody", facts))
        self.assertEqual(result["outcome"], "ready_for_expert_review")

    def test_raw_boolean_map_is_rejected(self):
        result = assess(self.profile, {"legal_authority_evidenced": "probably"})
        self.assertEqual(result["outcome"], "conflict")
        self.assertIn("raw Boolean fact maps", result["invalid"][0])

    def test_rules_derive_conclusions_from_accepted_evidence(self):
        from src.expert import load_rules

        rules = load_rules(ROOT / "domain/rules.json")
        complete = assess(self.profile, evidence_case("TEST-READY", "Complete", ALL_FACTS), rules)
        self.assertEqual(complete["derived"]["conclusions"].get("custody_bridge_ready"), [True])
        gap_facts = {**ALL_FACTS, "legal_authority_evidenced": False}
        gap = assess(self.profile, evidence_case("TEST-GAP", "Authority gap", gap_facts), rules)
        self.assertEqual(gap["derived"]["conclusions"].get("legal_authority_gap"), [True])
        self.assertNotIn("custody_bridge_ready", gap["derived"]["conclusions"])

    def test_expired_evidence_is_excluded(self):
        case = evidence_case("TEST-EXPIRED", "Expired", {"legal_authority_evidenced": True})
        case["evidence"][0]["scope"]["valid_until"] = "2026-01-02T00:00:00Z"
        result = derive_facts(case)
        self.assertNotIn("legal_authority_evidenced", result["facts"])
        self.assertIn("expired", result["excluded"][0]["reasons"][0])

    def test_contested_evidence_is_excluded(self):
        case = evidence_case("TEST-CONTESTED", "Contested", {"legal_authority_evidenced": True})
        case["evidence"][0]["review"]["status"] = "contested"
        result = derive_facts(case)
        self.assertEqual(result["facts"], {})
        self.assertIn("contested", result["excluded"][0]["reasons"][0])

    def test_accepted_opposites_create_conflict(self):
        case = evidence_case("TEST-CONFLICT", "Conflict", {"legal_authority_evidenced": True})
        opposite = record(2, "legal_authority_evidenced", False)
        case["evidence"].append(opposite)
        result = assess(self.profile, case)
        self.assertEqual(result["outcome"], "conflict")
        self.assertEqual(result["conflicts"][0]["evidence_ids"], ["EV-001", "EV-002"])

    def test_artifact_needs_integrity_record(self):
        case = evidence_case("TEST-INTEGRITY", "Integrity", {"legal_authority_evidenced": True})
        del case["evidence"][0]["artifact"]["integrity_not_recorded_reason"]
        self.assertIn("requires sha256", validate_case(case)[0])


if __name__ == "__main__":
    unittest.main()
