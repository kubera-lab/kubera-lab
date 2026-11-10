# KUBERA workspace status

Updated: **2026-10-02**

## Priority order

### P0 — KUBERA AGENT OS / AI Assurance
Public evidence:
- `KUBERA_AGENT_OS.md`
- `kubera-lab/agent-os/`
- `kubera-lab/innovation-stack/reference-implementation/`
- `kubera-lab/mcp-lab/`

Verified on 2026-10-02: **173 tests passed** on Python 3.11–3.13; coverage job reported **89% source branch coverage** against an 85% floor.

Status: **implemented public reference runtime**, not a production security product.

Core evidence includes source/evidence/action gates, Evidence Ledger mechanics, human approval boundaries, idempotency/replay handling, privacy/tool validation, a safe demo and automated CI.

### P1 — KUBERA TAO LAB
Public evidence:
- `kubera-lab/kubera-tao-lab/`

Implementation: private `saturnom999-lab/kubera-tao-lab`.

Verified on 2026-10-02:
- local project suite: **34 passed, 0 failed**;
- Python source compile check: passed;
- secret-pattern scan of staged source: passed;
- private GitHub Actions CI for commit `df3b739`: **success**.

Status: **active ML research/evaluation track**. It does not claim current Bittensor subnet compatibility or a live miner.

### P1 — KUBERA Real Estate OS
Public evidence:
- `kubera-lab/real-estate-os/`

Implementation: private `kubera-lab/kubera-real-estate-os`.

Verified on 2026-10-02: evidence-first Montenegro land-check core, **3/3 tests passed** on Python 3.11/3.12, private CI successful.

Status: **early verified core / wider product bootstrap**. Production integrations are not claimed until authenticated and tested.

### P2 — Applied proof
- `kubera-lab/tender-intelligence/` — deterministic procurement qualification and DRAFT_ONLY bid support; **16 tests passed** on Python 3.11–3.13.
- `kubera-lab/mcp-lab/` — bounded capability servers and deny-by-default gateway policy.
- `research/council-ai-service-finder/eval/v0.1/` — deterministic retrieval evaluation.
- `kubera-lab/dzambala-community-compass/` — provenance-oriented local intelligence.

## Portfolio controls

The root profile is checked by `tools/portfolio_audit.py` and `.github/workflows/portfolio-audit.yml`.

The audit prevents stale/unverified headline claims from returning and verifies that the priority evidence paths remain present.

## Not priority

Migration/visa templates, learning repositories, small experiments and old utilities remain useful library material but are not the primary professional narrative.

`kubera-learning`, `ssh-check` and `kubera-local-ai2` should not be presented as flagship work.

## Administrative cleanup still separate from code work

Repository rename, repository descriptions/topics and profile pinning are GitHub account-setting operations. They are not considered complete merely because README files were edited.

## Rule

**Evidence before claims. KUBERA prepares and verifies. The human remains the authority.**
