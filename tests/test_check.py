"""Failure-oriented tests for the portable release integrity check."""

import hashlib
from pathlib import Path
import unittest

from check import (CheckError, check_shortcuts_text, validate_dependency_graph,
                   validate_digest, validate_tracked_names, validate_count_rows)


class SourceIntegrityTests(unittest.TestCase):
    def test_audited_hash_rejects_one_byte_change(self):
        source = b"theorem tiny : True := True.intro\n"
        expected = hashlib.sha256(source).hexdigest()
        validate_digest("NivatTrial.Tiny", source, expected)
        with self.assertRaisesRegex(CheckError, "hash mismatch"):
            validate_digest("NivatTrial.Tiny", source + b"\n", expected)

    def test_nested_comments_and_strings_are_not_shortcuts(self):
        source = (
            "/- axiom /- native_decide -/ sorry -/\n"
            "-- admit\n"
            "#eval \"sorry axiom admit native_decide\"\n"
            "theorem safe : True := True.intro\n"
        )
        check_shortcuts_text(source)
        with self.assertRaisesRegex(CheckError, "sorry"):
            check_shortcuts_text("theorem false_proof : True := by sorry\n")

    def test_terminal_must_import_every_audited_module(self):
        graph = {"NivatTrial.TheoremB": set(), "NivatTrial.Auxiliary": set()}
        with self.assertRaisesRegex(CheckError, "closure omits"):
            validate_dependency_graph(graph)
        graph["NivatTrial.TheoremB"].add("NivatTrial.Auxiliary")
        validate_dependency_graph(graph)

    def test_tracked_cache_and_private_key_file_are_rejected(self):
        modules = {"NivatTrial.Tiny": Path("NivatTrial/Tiny.lean")}
        tracked = {"NivatTrial/Tiny.lean", "Audit.lean"}
        validate_tracked_names(tracked, modules)
        for invalid in (".lake/build/lib/Tiny.olean", ".env", "keys/release.pem"):
            with self.subTest(invalid=invalid), self.assertRaises(CheckError):
                validate_tracked_names(tracked | {invalid}, modules)

    def test_count_rows_ignore_order_but_reject_changes_or_duplicates(self):
        actual = [
            {"file": "Alpha.lean", "total_lines": 7, "code_lines": 5},
            {"file": "beta.lean", "total_lines": 13, "code_lines": 9},
        ]
        validate_count_rows(actual, list(reversed(actual)))
        changed = [dict(actual[1], code_lines=8), actual[0]]
        with self.assertRaisesRegex(CheckError, "disagree"):
            validate_count_rows(actual, changed)
        with self.assertRaisesRegex(CheckError, "Duplicate"):
            validate_count_rows(actual, [actual[0], actual[0]])


if __name__ == "__main__":
    unittest.main()
