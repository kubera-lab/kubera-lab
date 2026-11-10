"""Synthetic changed-file cases for check_protected_paths.py. Run: python -m unittest -v"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(__file__))
import check_protected_paths as c  # noqa: E402

G = "kubera-lab/kubera-guide-global-mapping/"


def f(name, status="modified", prev=None):
    d = {"filename": name, "status": status}
    if prev:
        d["previous_filename"] = prev
    return d


def run(files, expected=None, raw=None):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as t:
        t.write(raw if raw is not None else json.dumps(files))
    args = [t.name] + ([] if expected is None else ["--expected", str(expected)])
    out = io.StringIO()
    with redirect_stdout(out):
        code = c.main(args)
    os.unlink(t.name)
    return code, out.getvalue()


class Cases(unittest.TestCase):
    def test_protected_only_readme(self):
        self.assertEqual(run([f("README.md")])[0], 1)

    def test_protected_only_frozen_folder(self):
        self.assertEqual(run([f(G + "data/map.json")])[0], 1)

    def test_workflow_only(self):
        self.assertEqual(run([f(".github/workflows/community-compass-ci.yml")])[0], 0)

    def test_unrelated_only(self):
        self.assertEqual(run([f("kubera-lab/dzambala-community-compass/index.html"),
                              f("mcp-lab/tests/test_x.py", "added")])[0], 0)

    def test_mixed_unrelated_and_protected(self):
        code, out = run([f("docs/a.md"), f(G + "x.md", "removed")])
        self.assertEqual(code, 1)
        self.assertIn("removed: " + G + "x.md", out)

    def test_deletion(self):
        self.assertEqual(run([f("README.md", "removed")])[0], 1)

    def test_rename_out_of_frozen_folder(self):
        self.assertEqual(run([f("archive/x.md", "renamed", G + "x.md")])[0], 1)

    def test_rename_into_frozen_folder(self):
        self.assertEqual(run([f(G + "x.md", "renamed", "notes/x.md")])[0], 1)

    def test_rename_of_root_readme(self):
        self.assertEqual(run([f("docs/OLD_README.md", "renamed", "README.md")])[0], 1)

    def test_readme_case_and_extension_variants(self):
        for name in ("readme.md", "README", "Readme.rst", "README.MD"):
            self.assertTrue(c.is_protected(name), name)

    def test_nested_readmes_are_not_protected(self):
        for name in ("kubera-lab/dzambala-community-compass/README.md", "docs/README.md", "READMEFIRST.txt"):
            self.assertFalse(c.is_protected(name), name)

    def test_lookalike_folder_is_not_protected(self):
        self.assertFalse(c.is_protected("kubera-lab/kubera-guide-global-mapping-v2/x.md"))
        self.assertFalse(c.is_protected("other/kubera-lab/kubera-guide-global-mapping/x.md"))

    def test_path_normalisation(self):
        self.assertTrue(c.is_protected("./README.md"))
        self.assertTrue(c.is_protected("/" + G + "a"))
        self.assertTrue(c.is_protected("kubera-lab\\kubera-guide-global-mapping\\a"))

    def test_paginated_slurp_input(self):
        pages = [[f("a.txt")] * 2, [f(G + "b")]]
        self.assertEqual(run(pages)[0], 1)

    def test_empty_pr(self):
        self.assertEqual(run([])[0], 0)

    def test_truncated_list_fails_closed(self):
        self.assertEqual(run([f("a.txt")], expected=3001)[0], 2)

    def test_unreadable_input_fails_closed(self):
        self.assertEqual(run(None, raw="not json")[0], 2)
        self.assertEqual(run(None, raw='{"filename": "README.md"}')[0], 2)


if __name__ == "__main__":
    unittest.main()
