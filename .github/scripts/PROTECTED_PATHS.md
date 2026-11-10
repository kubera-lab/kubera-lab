# Protected-path check (issues #75, #93)

**What it protects:** the root profile README (any case/extension) and everything in
`kubera-lab/kubera-guide-global-mapping/`. Both old and new names of a rename are checked,
so moving a file out of the frozen folder is also caught. Deletions are caught.

**How:** `.github/workflows/protected-paths.yml` runs on every pull request (no paths filter)
via `pull_request_target`, so the workflow and `check_protected_paths.py` always come from
`main`. A pull request cannot weaken the check by editing them; changes to the checker only
take effect after they are merged. No pull-request code is checked out or run. Permissions:
`contents: read`, `pull-requests: read`. The checkout action is pinned to a commit SHA.

**Fails closed** when the changed-file list cannot be read or is shorter than GitHub's
`changed_files` count (GitHub lists at most 3000 files per PR).

**Run the tests:** `cd .github/scripts && python -m unittest -v test_check_protected_paths.py`

## Limits — read before relying on it

- Until branch protection or a ruleset marks the `protected-paths` job as **required**, a red
  check is only a warning: someone with merge rights can still merge, and direct pushes to
  `main` are not checked at all. Turning that on needs Nikola's separate approval.
- The check appears on a pull request only after this workflow is on `main`.
- Repository admins can always bypass checks unless the ruleset also applies to admins.
- `CODEOWNERS` already lists `/README.md`; it only enforces review if "Require review from
  Code Owners" is enabled.
- The older inline step in `unified-agent-workflow.yml` still exists. It uses
  `git diff --name-only`, which can miss the old name of a rename. It is left unchanged here
  to avoid overlapping PR #74's file; it can be removed once this check is required.
