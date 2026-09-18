import contextlib
import io
import sys
import unittest
from unittest import mock

from src import cli


class EvidenceCommandExitStatusTests(unittest.TestCase):
    def test_drift_returns_nonzero(self):
        drift = [{"source_id": "s1", "recorded": "a" * 64, "current": "b" * 64}]
        with mock.patch.object(sys, "argv", ["research", "verify-evidence", "--drift"]), \
                mock.patch("src.evidence.check_drift", return_value=drift), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(), 1)

    def test_partial_archive_returns_nonzero(self):
        manifest = {
            "snapshots": [
                {"source_id": "s1", "status": "frozen"},
                {"source_id": "s2", "status": "unavailable"},
            ]
        }
        with mock.patch.object(sys, "argv", ["research", "archive"]), \
                mock.patch("src.evidence.run_archive", return_value=manifest), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(), 1)


if __name__ == "__main__":
    unittest.main()
