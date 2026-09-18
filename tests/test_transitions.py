import unittest
from pathlib import Path

from src.transitions import load_case, render_case_study, validate_case_study


ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "domain/cases/allianz-y3-bitcoin.json"


class InstitutionalTransitionCaseTests(unittest.TestCase):
    def setUp(self):
        self.case = load_case(CASE_PATH)

    def test_allianz_case_is_valid(self):
        self.assertEqual(validate_case_study(self.case), [])

    def test_every_pathway_distinguishes_on_chain_from_exposure(self):
        for pathway in self.case["pathways"]:
            self.assertIsInstance(pathway["on_chain"], bool)
            self.assertTrue(pathway["meaning"])
            self.assertTrue(pathway["warning"])

    def test_participant_is_not_misrepresented_as_portfolio_manager(self):
        self.assertIn("not portfolio manager", self.case["transition"]["participant_role"])

    def test_unknown_legal_questions_are_not_reported_as_facts(self):
        blockers = {item["id"]: item for item in self.case["blockers"]}
        self.assertEqual(blockers["B3"]["status"], "unknown")
        self.assertEqual(blockers["B4"]["status"], "unknown")

    def test_rendered_study_contains_limits_and_sources(self):
        rendered = render_case_study(self.case)
        self.assertIn("not legal, pension, tax or investment advice", rendered)
        self.assertIn("## Sources", rendered)
        self.assertIn("## Pathways", rendered)


if __name__ == "__main__":
    unittest.main()
