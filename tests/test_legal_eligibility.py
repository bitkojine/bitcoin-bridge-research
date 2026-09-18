import unittest
from pathlib import Path

from src.legal_eligibility import evaluate_all, evaluate_route, load_eligibility, recorded_in_force, validate_eligibility


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "domain/legal/allianz-y3-eligibility.json"


class LegalEligibilityTests(unittest.TestCase):
    def setUp(self):
        self.model = load_eligibility(MODEL_PATH)

    def test_model_uses_official_authority_and_validates(self):
        self.assertEqual(validate_eligibility(self.model), [])
        self.assertEqual(self.model["authorities"][0]["source_kind"], "official_register")
        self.assertIn("eli:version_date", self.model["authorities"][0]["eli_mapping"])

    def test_force_is_temporal_and_does_not_backdate_prohibition(self):
        provision = self.model["provisions"][0]
        self.assertFalse(recorded_in_force(provision, "2026-05-01"))
        self.assertTrue(recorded_in_force(provision, "2026-05-02"))

    def test_direct_bitcoin_and_bitcoin_right_security_are_prohibited(self):
        for route_id in ("direct-bitcoin", "bitcoin-right-security"):
            result = evaluate_route(self.model, route_id)
            self.assertEqual(result["status"], "prohibited")
            self.assertEqual(result["force_claim"], "recorded_in_force")
            self.assertEqual(result["matched_provisions"][0]["citation"], "Article 45(3)")

    def test_mstr_angle_is_not_converted_into_permission(self):
        result = evaluate_route(self.model, "ordinary-bitcoin-company-share")
        self.assertEqual(result["status"], "professional_interpretation_required")
        self.assertEqual(result["matched_provisions"], [])

    def test_personal_exit_is_not_misreported_as_fund_permission(self):
        result = evaluate_route(self.model, "participant-exit-then-personal-bitcoin")
        self.assertEqual(result["status"], "personal_route_subject_to_conditions")
        self.assertEqual(result["instrument_class"], "personal_purchase_after_lawful_payout")

    def test_every_route_returns_a_closed_status(self):
        self.assertEqual(len(evaluate_all(self.model)), len(self.model["routes"]))


if __name__ == "__main__":
    unittest.main()
