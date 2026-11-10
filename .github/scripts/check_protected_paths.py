#!/usr/bin/env python3
"""Fail a pull request that touches a protected path (issue #75 / #93).

Protected:
  * the root profile README (any case, any extension: README, README.md, readme.rst ...)
  * everything under kubera-lab/kubera-guide-global-mapping/ (frozen project)

Input: the JSON list returned by GET /repos/{owner}/{repo}/pulls/{n}/files
(one object per file with "filename", "status" and, for renames,
"previous_filename"). Both the old and the new name of a rename are checked,
so moving a file out of a protected folder is caught too.

Exit codes: 0 = no protected path touched, 1 = protected path touched,
2 = input incomplete or unreadable (fail closed).
Standard library only; never executes code from the pull request.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Iterable

FROZEN_DIR = "kubera-lab/kubera-guide-global-mapping/"


def is_protected(path: str) -> bool:
    if not path:
        return False
    p = path.replace("\\", "/").lstrip("/")
    while p.startswith("./"):
        p = p[2:]
    if "/" not in p and p.lower().split(".", 1)[0] == "readme":
        return True
    return p == FROZEN_DIR.rstrip("/") or p.startswith(FROZEN_DIR)


def protected_hits(files: Iterable[dict]) -> list[str]:
    hits: list[str] = []
    for item in files:
        status = item.get("status", "?")
        for key in ("filename", "previous_filename"):
            name = item.get(key)
            if name and is_protected(name):
                hits.append(f"{status}: {name}")
    return hits


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files_json", help="path to the PR files JSON ('-' for stdin)")
    ap.add_argument("--expected", type=int, default=None,
                    help="changed_files count from the PR; fewer listed files means fail closed")
    args = ap.parse_args(argv)

    try:
        raw = sys.stdin.read() if args.files_json == "-" else open(args.files_json, encoding="utf-8").read()
        data = json.loads(raw)
    except (OSError, ValueError) as exc:
        print(f"::error::Could not read the changed-file list: {exc}")
        return 2
    # gh api --paginate --slurp gives a list of pages; flatten it.
    if data and all(isinstance(x, list) for x in data):
        data = [f for page in data for f in page]
    if not isinstance(data, list) or not all(isinstance(x, dict) for x in data):
        print("::error::Changed-file list has an unexpected shape.")
        return 2
    if args.expected is not None and len(data) < args.expected:
        print(f"::error::Only {len(data)} of {args.expected} changed files were listed "
              "(GitHub lists at most 3000). Review this PR by hand.")
        return 2

    hits = protected_hits(data)
    print(f"Checked {len(data)} changed file(s).")
    if hits:
        for h in hits:
            print(f"::error::Protected path changed — {h}")
        print("This PR touches the profile README or the frozen Kubera Guide folder. "
              "Only Nikola can approve that, with an explicit instruction.")
        return 1
    print("No protected path changed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
