import unittest

from src.cli import build_markdown, load_model, validate


class DomainModelTests(unittest.TestCase):
    def setUp(self):
        self.model = load_model()

    def test_model_is_valid(self):
        self.assertEqual(validate(self.model), [])

    def test_every_company_is_rendered(self):
        output = build_markdown(self.model)
        for company in self.model["companies"]:
            self.assertIn(company["name"], output)

    def test_every_equation_defines_terms(self):
        for capability in self.model["bitcoin_capabilities"]:
            self.assertTrue(capability["formula"])
            self.assertTrue(capability["terms"])


if __name__ == "__main__":
    unittest.main()

