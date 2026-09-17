import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch
from pathlib import Path

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

    def test_pdf_builds_from_model(self):
        from src import pdf

        with TemporaryDirectory() as folder:
            target = Path(folder) / "domain-map.pdf"
            with patch.object(pdf, "OUTPUT", target):
                result = pdf.build_pdf(self.model)
            self.assertEqual(result, target)
            self.assertTrue(target.exists())
            self.assertGreater(target.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
