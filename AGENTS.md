# KUBERA Repository Agent Guide

**KUBERA prepares. The human remains the authority.**

This file is the concise operating guide for coding agents working in this repository. It complements `kubera-lab/innovation-stack/KUBERA_OPERATOR.md`; it does not replace DZAMBALA governance, evidence, approvals or execution controls.

## Repository map

- `kubera-lab/innovation-stack/reference-implementation/` — tested Python reference runtime.
- `kubera-lab/operator-workspace-kit/` — task, evidence, review and approval workspace.
- `kubera-lab/dzambala-community-compass/` — Community Compass project.
- `kubera-lab/kubera-guide-global-mapping/` — frozen Kubera Guide project files.
- `.github/workflows/` — CI and profile protection.
- [WORKFLOW.md](WORKFLOW.md) — unified human-controlled workflow for ChatGPT, Claude, Copilot, Grok and Nikola.

## Commands

Run the reference runtime from:

```bash
cd kubera-lab/innovation-stack/reference-implementation
python -m pip install -e .
python -m unittest discover -s tests -v
python -m kubera_innovation demo --json
```

Coverage check used by CI:

```bash
python -m pip install coverage
coverage run --branch --source=kubera_innovation -m unittest discover -s tests -q
coverage run --append --branch --source=kubera_innovation -m kubera_innovation demo --json
coverage report --show-missing --fail-under=85
```

Supported/tested CI versions: Python 3.11, 3.12 and 3.13.

## Hard invariants

- Do not modify root `README.md` unless Nikola gives a new, explicit command to change the profile page itself.
- Do not modify frozen Kubera Guide project files unless Nikola explicitly reverses that freeze.
- Do not create Innovation Stack modules numbered 19 or higher.
- Do not claim live council, bank, autonomous posting or production integration unless it is actually implemented and verified.
- Do not expose private repositories, credentials, secrets or private-core material.
- Do not perform consequential external actions from agent code without the existing human-approval path.
- Keep provider credentials and raw external clients outside agent/plugin reach.

## Architecture invariants

Consequential tool execution follows the existing path:

`HandoffArtifact → WorkContract → PrivacyGate → ToolValidator → Source/Evidence/Action Gate → exact approval when required → IdempotencyStore → ToolAdapter → ActionLogger → EvidenceLedger`

`SovereignToolExecutor` is the reference choke point. Do not add alternative execution paths around it.

## Correction → improvement loop

Repeated user corrections are evidence, not permission to silently rewrite rules.

1. Record a compact `CorrectionSignal` — fingerprint, short summary, conversation id and pain score; do not store a full transcript by default.
2. Promote only when the configured threshold is met across repeated signals and multiple conversations.
3. Draft one exact rule/skill/gate/doc change.
4. Show the evidence and exact diff.
5. Human approves or dismisses the exact proposal.
6. Only an approved proposal may be handed into the normal Git/PR workflow.
7. Deterministic gates are preferred over repeatedly relying on prose instructions when a rule can be enforced safely.

The reference implementation is `kubera_innovation.improvement_loop.ImprovementRegistry`.

## Before saying work is ready

- Re-read the current files you are about to change.
- Run the relevant targeted tests.
- Run the full reference test suite when the runtime changes.
- Confirm no protected/frozen file changed unexpectedly.
- Report what was actually verified; do not invent coverage, deployment or integration status.
