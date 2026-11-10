# KUBERA workspace status

Last reviewed: **2026-11-10** (against `main` at `8166cc4`). Figures marked with an earlier date are historical and keep their original date. Full detail and run links: `EVIDENCE_MATRIX.md`.

## Priority order

### P0 — KUBERA AGENT OS / AI Assurance
Public evidence:
- `KUBERA_AGENT_OS.md`
- `kubera-lab/agent-os/`
- `kubera-lab/innovation-stack/reference-implementation/`
- `kubera-lab/mcp-lab/`

Verified on 2026-10-02: **173 tests passed** on Python 3.11–3.13; coverage job reported **89% source branch coverage** against an 85% floor (public run 37061120307).

Re-checked on 2026-11-10: local run of the same suite, 173 tests OK and 89% coverage. No CI run since 2 October because the runtime has not changed.

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

Not re-run on 2026-11-10 (private code).

Status: **active ML research/evaluation track**. It does not claim current Bittensor subnet compatibility or a live miner.

### P1 — KUBERA Real Estate OS
Public evidence:
- `kubera-lab/real-estate-os/`

Implementation: private `kubera-lab/kubera-real-estate-os`.

Verified on 2026-10-02: evidence-first Montenegro land-check core, **3/3 tests passed** on Python 3.11/3.12, private CI successful. Not re-run on 2026-11-10 (private code).

Status: **early verified core / wider product bootstrap**. Production integrations are not claimed until authenticated and tested.

### Flagship product — KUBERA GEO SI
Public showcase: `kubera-lab/kubera-geoai` (live demo; application code private).

Status: **live demo / pilot area Mitcham (CR4)**. Data sources named in the public showcase: HM Land Registry, EPC, OS Open UPRN, Ofcom, Environment Agency flood data, Planning Data, UK HPI, OpenStreetMap. "Defra noise" was removed from the profile README on 2026-11-10 because it could not be confirmed. No air-quality data is claimed.

### P2 — Applied proof
- `kubera-lab/tender-intelligence/` — deterministic procurement qualification and DRAFT_ONLY bid support; **21 tests passed** on Python 3.11–3.13 on 2026-11-10 (was **16 tests passed** on 2026-10-02, before the closed-tender, currency and deadline fixes in PR #91/#94).
- `kubera-lab/mcp-lab/` — bounded capability servers and deny-by-default gateway policy; 17 Python tests + gateway typecheck passed on 2026-11-10.
- `research/council-ai-service-finder/eval/v0.1/` — deterministic retrieval evaluation; 32 tests passed locally on 2026-11-10.
- `kubera-lab/dzambala-community-compass/` — provenance-oriented local intelligence; past-events archive added 2026-11-10. All seed events have ended; no upcoming event is currently verified.

## Portfolio controls

The root profile is checked by `tools/portfolio_audit.py` and `.github/workflows/portfolio-audit.yml`.

The audit prevents stale/unverified headline claims from returning and verifies that the priority evidence paths remain present. It is path-filtered, so it does not run on every pull request.

Since 2026-11-10 `.github/workflows/protected-paths.yml` runs on every pull request and flags changes to the root README or the frozen Kubera Guide folder. It is not yet a required check; that needs the owner's approval in branch protection.

## Not priority

Migration/visa templates, learning repositories, small experiments and old utilities remain useful library material but are not the primary professional narrative.

`kubera-learning`, `ssh-check` and `kubera-local-ai2` should not be presented as flagship work.

## Administrative cleanup still separate from code work

Repository rename, repository descriptions/topics and profile pinning are GitHub account-setting operations. They are not considered complete merely because README files were edited.

## Rule

**Evidence before claims. KUBERA prepares and verifies. The human remains the authority.**
