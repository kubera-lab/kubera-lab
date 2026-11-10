# KUBERA Evidence Matrix

Last reviewed: **10 November 2026**, against `main` at commit `8166cc4`.

Every row separates four things: what is **verified now**, what is **historical evidence** (kept with its original date), what is **not verified**, and what is **planned**. Counts come from named test runs; they are not estimates. "Local run" means the suite was run from a clean checkout of `main` on the review date (Python 3.13).

## Public projects in this repository

| Project | Status | Verified on 10 Nov 2026 | Historical evidence (original date) | Boundary / not verified |
|---|---|---|---|---|
| **KUBERA AGENT OS / Innovation Stack reference** | Implemented public reference runtime | Local run: 173 tests OK; 89% branch coverage (85% floor) | 2 Oct 2026: **173 tests passed** on Python 3.11, 3.12, 3.13; **89%** coverage — public run [37061120307](https://github.com/kubera-lab/kubera-lab/actions/runs/37061120307) | No CI run since 2 Oct (no code change since). Not a production security product |
| **Tender Intelligence** | Tested public applied capability | **21 passed** on Python 3.11, 3.12, 3.13 — run [42872402933](https://github.com/kubera-lab/kubera-lab/actions/runs/42872402933) (commit `da62947`); local run 21 passed | 2 Oct 2026: **16 tests passed** on 3.11–3.13 — run [37060909375](https://github.com/kubera-lab/kubera-lab/actions/runs/37060909375). Rose to 21 with PR #91 and #94 (closed tenders, unknown currency, malformed deadlines) | Outputs stay DRAFT_ONLY and human-controlled; no live bidding |
| **MCP LAB** | Tested capability layer | Python **17 passed** + TypeScript gateway typecheck — run [42872402965](https://github.com/kubera-lab/kubera-lab/actions/runs/42872402965); local run 17 passed | — | Bounded capabilities; no arbitrary proxy or uncontrolled write layer |
| **Community Compass** | Public civic/local prototype | Validators OK (5 sources, 8 events), **7** Python + **10** Node date/archive tests — run [42872544097](https://github.com/kubera-lab/kubera-lab/actions/runs/42872544097) (commit `5d2bc24`) | Event seed checked 30 Aug 2026 | All 8 seed events have ended and sit in the archive view. No upcoming event is currently verified. Not an official service |
| **Council AI Service Finder** | Public evaluation harness | Local run: **32 passed** | 29 Aug 2026: CI success on 3.11–3.13 — run [33242579297](https://github.com/kubera-lab/kubera-lab/actions/runs/33242579297) | Evaluation/prototype, not council authority. Test count from CI log not re-read |
| **Kubera Agent Fabric (prototype)** | Research prototype | Local run: **5 tests OK** | 29 Aug 2026: CI success on 3.11–3.13 — run [33242695251](https://github.com/kubera-lab/kubera-lab/actions/runs/33242695251) | Prototype only |
| **Portfolio Evidence Audit** | Public guardrail | Success — run [42872544380](https://github.com/kubera-lab/kubera-lab/actions/runs/42872544380); local `python tools/portfolio_audit.py` OK | 2 Oct 2026 — run [37061120309](https://github.com/kubera-lab/kubera-lab/actions/runs/37061120309) | Path-filtered: does not run on every PR, so it is not a required check |
| **Protected Paths** | Public guardrail | Self-test 17 cases OK — run [42872666490](https://github.com/kubera-lab/kubera-lab/actions/runs/42872666490) (PR #97) | — | Runs on every PR from `main`. Not yet a required check: until branch protection marks it required, a red result is a warning only |

## Projects whose code is private

Summarised here; private run links are not used as reviewer dependencies and could not be re-inspected publicly on the review date.

| Project | Status | Historical evidence (original date) | Not verified on 10 Nov 2026 |
|---|---|---|---|
| **KUBERA TAO LAB** | Active private ML research | 2 Oct 2026: **34/34** local tests passed; compile, diff and secret-pattern checks passed; private CI success for commit `df3b739` | Not re-run. No live miner and no current-subnet compatibility claim |
| **KUBERA Real Estate OS** | Early verified core + bootstrap | 2 Oct 2026: Montenegro land-check core, **3/3** tests passed on Python 3.11 and 3.12; private CI success | Not re-run. Wider SaaS integrations not production-labelled |

## Separate repositories

| Project | Status | What can be checked publicly | Not verified on 10 Nov 2026 |
|---|---|---|---|
| **KUBERA GEO SI** ([kubera-geoai](https://github.com/kubera-lab/kubera-geoai)) | Live demo; application code is private | Public showcase README and screenshots. Data sources named there: HM Land Registry, EPC, OS Open UPRN, Ofcom Connected Nations, Environment Agency flood data, Planning Data (MHCLG), UK House Price Index, OpenStreetMap | The live site could not be opened from the review environment. "Defra noise" was removed from the profile README on 10 Nov 2026 (owner decision) because it could not be confirmed. No air-quality data is claimed |

## Evidence policy

A metric belongs in the public portfolio only when the current repository or a named run supports it. Historical figures keep their original date instead of being re-dated. Marketing-style figures that cannot be independently verified are not used as technical credentials.

## Public/private boundary

The public portfolio exposes architecture, evidence, tests and limitations. It does not expose credentials, client data, private raw datasets, wallet/key material or private repository history merely to make the portfolio look larger.
