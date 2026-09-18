import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src import evidence
from src.evidence import (
    archive_source,
    by_id,
    extension_for,
    extract_text,
    normalize,
    sha256_bytes,
    sha256_file,
    snapshot_coverage,
    unavailable_entry,
    verify_pin_cites,
    verify_snapshots,
)


class HashingTests(unittest.TestCase):
    def test_sha256_bytes_matches_known_vector(self):
        self.assertEqual(
            sha256_bytes(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        )

    def test_sha256_file_matches_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.bin"
            path.write_bytes(b"hello")
            self.assertEqual(sha256_file(path), sha256_bytes(b"hello"))

    def test_normalize_collapses_whitespace(self):
        self.assertEqual(normalize("a\n  b\t c"), "a b c")


class ExtractionTests(unittest.TestCase):
    def test_html_extraction_drops_script_and_style(self):
        html = b"<html><head><style>x{}</style></head><body><script>bad()</script><p>Hello <b>world</b></p></body></html>"
        text = extract_text("text/html", html)
        self.assertIn("Hello", text)
        self.assertNotIn("bad()", text)
        self.assertNotIn("x{}", text)

    def test_pdf_bytes_without_reader_return_none(self):
        with mock.patch.dict("sys.modules", {"pypdf": None}):
            self.assertIsNone(extract_text("application/pdf", b"%PDF-1.4 junk"))

    def test_extension_prefers_url_suffix(self):
        self.assertEqual(extension_for("https://x/y.pdf", "text/html"), ".pdf")
        self.assertEqual(extension_for("https://x/y", "application/pdf"), ".pdf")
        self.assertEqual(extension_for("https://x/y", "text/html"), ".html")


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def make_entry(self, source_id="s1", data=b"the quick brown fox"):
        artifact = self.root / "evidence" / source_id / "a.bin"
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_bytes(data)
        text = self.root / "evidence" / source_id / "a.txt"
        text.write_text(data.decode(), encoding="utf-8")
        return {
            "source_id": source_id,
            "status": "frozen",
            "url": "https://example.test/s1",
            "sha256": sha256_bytes(data),
            "bytes": len(data),
            "path": str(artifact.relative_to(self.root)),
            "text_path": str(text.relative_to(self.root)),
            "text_sha256": sha256_file(text),
        }

    def model(self, source_id="s1", quote="quick brown", locator="p. 1"):
        return {
            "claims": [{
                "id": "c1",
                "treatments": [{"source_id": source_id, "treatment": "supports", "locator": locator, "quote": quote}],
            }]
        }

    def test_clean_manifest_verifies(self):
        manifest = {"snapshots": [self.make_entry()]}
        with mock.patch.object(evidence, "ROOT", self.root):
            self.assertEqual(verify_snapshots(self.model(), manifest), [])
            self.assertEqual(verify_pin_cites(self.model(locator="the"), manifest), [])

    def test_tampered_artifact_is_detected(self):
        entry = self.make_entry()
        manifest = {"snapshots": [entry]}
        (self.root / entry["path"]).write_bytes(b"tampered")
        with mock.patch.object(evidence, "ROOT", self.root):
            problems = verify_snapshots(self.model(), manifest)
        self.assertTrue(any("hash mismatch" in p for p in problems))

    def test_quote_absent_from_frozen_text_is_detected(self):
        manifest = {"snapshots": [self.make_entry()]}
        with mock.patch.object(evidence, "ROOT", self.root):
            problems = verify_pin_cites(self.model(quote="not in the text"), manifest)
        self.assertTrue(any("not present" in p for p in problems))

    def test_locator_must_appear_before_quote(self):
        manifest = {"snapshots": [self.make_entry()]}
        with mock.patch.object(evidence, "ROOT", self.root):
            missing = verify_pin_cites(self.model(locator="page one"), manifest)
            after = verify_pin_cites(self.model(locator="fox"), manifest)
        self.assertTrue(any("locator is not present before" in p for p in missing))
        self.assertTrue(any("locator is not present before" in p for p in after))

    def test_missing_locator_and_quote_are_detected(self):
        manifest = {"snapshots": [self.make_entry()]}
        model = {"claims": [{"id": "c1", "treatments": [{"source_id": "s1", "treatment": "supports"}]}]}
        with mock.patch.object(evidence, "ROOT", self.root):
            problems = verify_pin_cites(model, manifest)
        self.assertTrue(any("no pin-cite locator" in p for p in problems))
        self.assertTrue(any("no pin-cite quote" in p for p in problems))

    def test_cited_unfrozen_source_is_detected(self):
        entry = unavailable_entry({"id": "occ", "url": "https://occ.test/x"}, "timed out", None)
        manifest = {"snapshots": [entry]}
        with mock.patch.object(evidence, "ROOT", self.root):
            problems = verify_snapshots(self.model(source_id="occ"), manifest)
        self.assertTrue(any("snapshot is unavailable" in p for p in problems))

    def test_cited_source_without_snapshot_is_detected(self):
        with mock.patch.object(evidence, "ROOT", self.root):
            problems = verify_snapshots(self.model(source_id="ghost"), {"snapshots": []})
        self.assertTrue(any("has no evidence snapshot" in p for p in problems))

    def test_unavailable_attempt_preserves_previous_frozen_entry(self):
        frozen = self.make_entry()
        merged = unavailable_entry({"id": "s1", "url": "https://example.test/s1"}, "timeout", frozen)
        self.assertEqual(merged["status"], "frozen")
        self.assertEqual(merged["sha256"], frozen["sha256"])
        self.assertEqual(merged["last_attempt"]["error"], "timeout")

    def test_coverage_counts_frozen_and_unavailable(self):
        manifest = {
            "snapshots": [
                self.make_entry("a"),
                unavailable_entry({"id": "b", "url": "https://b.test"}, "timeout", None),
            ]
        }
        self.assertEqual(snapshot_coverage(manifest), {"total": 2, "frozen": 1, "unavailable": ["b"]})

    def test_archive_source_writes_content_addressed_files(self):
        payload = b"<html><body><p>archived</p></body></html>"

        class FakeResponse:
            headers = {"Content-Type": "text/html"}

            def read(self, size=-1):
                return payload

            def geturl(self):
                return "https://example.test/doc.html"

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

        with mock.patch.object(evidence, "EVIDENCE_DIR", self.root / "evidence" / "sources"), \
                mock.patch.object(evidence.urllib.request, "urlopen", return_value=FakeResponse()):
            entry = archive_source({"id": "doc", "url": "https://example.test/doc.html"})
        self.assertEqual(entry["sha256"], sha256_bytes(payload))
        self.assertEqual(entry["status"], "frozen")
        self.assertTrue((self.root / entry["path"]).exists())
        self.assertTrue((self.root / entry["text_path"]).exists())

    def test_fetch_rejects_non_http_urls(self):
        with self.assertRaisesRegex(ValueError, "unsupported source URL scheme"):
            evidence.fetch("file:///etc/passwd")

    def test_fetch_rejects_oversized_response(self):
        class FakeResponse:
            headers = {"Content-Type": "text/plain"}

            def read(self, size=-1):
                return b"12345"

            def geturl(self):
                return "https://example.test/large"

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

        with mock.patch.object(evidence.urllib.request, "urlopen", return_value=FakeResponse()):
            with self.assertRaisesRegex(ValueError, "download limit"):
                evidence.fetch("https://example.test/large", max_bytes=4)


class RealEvidenceTests(unittest.TestCase):
    """The committed manifest must describe real, hash-stable files."""

    def test_committed_manifest_is_internally_consistent(self):
        manifest = evidence.load_manifest()
        self.assertTrue(manifest.get("snapshots"), "expected archived source snapshots")
        for entry in manifest.get("snapshots", []):
            if entry.get("status") != "frozen":
                continue
            artifact = evidence.ROOT / entry["path"]
            self.assertTrue(artifact.exists(), f"missing artifact for {entry['source_id']}")
            self.assertEqual(sha256_file(artifact), entry["sha256"])

    def test_manifest_metadata_counts_match_entries(self):
        manifest = evidence.load_manifest()
        coverage = snapshot_coverage(manifest)
        self.assertEqual(manifest["meta"]["frozen"], coverage["frozen"])
        self.assertEqual(manifest["meta"]["unavailable"], len(coverage["unavailable"]))


if __name__ == "__main__":
    unittest.main()
