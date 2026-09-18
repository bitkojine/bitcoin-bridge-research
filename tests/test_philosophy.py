import unittest
from pathlib import Path

from src.philosophy import evaluate_action, load_philosophy, validate_philosophy


ROOT = Path(__file__).resolve().parents[1]


class PhilosophyArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.model = load_philosophy(ROOT / "domain/philosophy.json")

    def test_model_is_valid_and_ordered(self):
        self.assertEqual(validate_philosophy(self.model), [])

    def test_prohibited_action_never_becomes_recommendation(self):
        result = evaluate_action({
            "id": "direct-bitcoin", "actor": "pension-manager", "action": "buy bitcoin",
            "legal_state": "prohibited", "authority_state": "established",
            "requires_claims": [], "serves_values": ["retirement-security"],
            "consequences": ["market risk"], "reversibility": "market-dependent",
        }, {}, {"retirement-security"})
        self.assertEqual(result["status"], "blocked")
        self.assertIn("legal_prohibition", {item["type"] for item in result["blockers"]})

    def test_unknown_claim_does_not_satisfy_action_gate(self):
        result = evaluate_action({
            "id": "mstr", "actor": "pension-manager", "action": "research MSTR eligibility",
            "legal_state": "unknown", "authority_state": "established",
            "requires_claims": [{"claim_id": "mstr-eligible", "accepted_states": ["supported"]}],
            "serves_values": ["participant-choice"], "consequences": ["research cost"],
            "reversibility": "reversible",
        }, {}, {"participant-choice"})
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["blockers"][0]["actual"], "unknown")

    def test_complete_record_is_only_eligible_for_human_decision(self):
        result = evaluate_action({
            "id": "ask-regulator", "actor": "participant", "action": "request interpretation",
            "legal_state": "permitted", "authority_state": "established",
            "requires_claims": [{"claim_id": "boundary-unclear", "accepted_states": ["supported"]}],
            "serves_values": ["legal-clarity"], "consequences": ["time cost"],
            "reversibility": "reversible",
        }, {"boundary-unclear": "supported"}, {"legal-clarity"})
        self.assertEqual(result["status"], "eligible_for_human_decision")
        self.assertEqual(result["blockers"], [])


if __name__ == "__main__":
    unittest.main()
