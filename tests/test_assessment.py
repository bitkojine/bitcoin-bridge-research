import json
import unittest
from pathlib import Path

from src.assessment import assess, load_profile, render_markdown

ROOT = Path(__file__).resolve().parents[1]


class CustodyReadinessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_profile(ROOT / "domain/assessments/custody-readiness.json")
        cls.cases = json.loads(
            (ROOT / "tests/fixtures/custody-readiness-cases.json").read_text(encoding="utf-8")
        )

    def test_scenario_cases(self):
        for case in self.cases:
            with self.subTest(case=case["name"]):
                self.assertEqual(assess(self.profile, case["facts"])["outcome"], case["outcome"])

    def test_every_requirement_has_sources(self):
        for requirement in self.profile["requirements"]:
            self.assertTrue(requirement["source_ids"])

    def test_report_names_blockers_and_unknowns(self):
        result = assess(self.profile, {"legal_authority_evidenced": False})
        report = render_markdown(result)
        self.assertIn("Blocking gaps", report)
        self.assertIn("Legal authority and mandate", report)
        self.assertIn("Missing evidence", report)

    def test_subcustodian_review_is_not_required_when_unused(self):
        facts = json.loads(
            (ROOT / "examples/custody-readiness-complete.json").read_text(encoding="utf-8")
        )
        facts["subcustodian_used"] = False
        del facts["subcustodian_due_diligence_complete"]
        result = assess(self.profile, facts)
        self.assertEqual(result["outcome"], "ready_for_expert_review")

    def test_non_boolean_input_is_a_conflict(self):
        result = assess(self.profile, {"legal_authority_evidenced": "probably"})
        self.assertEqual(result["outcome"], "conflict")
        self.assertEqual(result["invalid"][0]["fact"], "legal_authority_evidenced")


if __name__ == "__main__":
    unittest.main()
