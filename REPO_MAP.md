# KUBERA repository map

Last reviewed: **2026-11-10**. Status and test evidence: `STATUS.md`, `EVIDENCE_MATRIX.md`.

## Public entry points

1. **Profile / portfolio hub** — `kubera-lab/kubera-lab`
2. **Reviewer route** — `PORTFOLIO_REVIEW.md`
3. **KUBERA LAB index** — `kubera-lab/README.md`

## Flagship product — KUBERA GEO SI
Public showcase: [`kubera-lab/kubera-geoai`](https://github.com/kubera-lab/kubera-geoai) (live demo; application code is private).

Role: evidence-first property facts for UK estate agents from open government data, with the source shown next to every figure.

## Priority architecture

### 1. Control — KUBERA AGENT OS
Paths:
- `KUBERA_AGENT_OS.md`
- `kubera-lab/agent-os/`
- `kubera-lab/innovation-stack/reference-implementation/`

Role:
- orchestration;
- policy and permissions;
- source/evidence/action gates;
- approval boundaries;
- idempotency/replay control;
- Evidence Ledger;
- safe tool execution.

### 2. Capability layer — KUBERA MCP LAB
Path: `kubera-lab/mcp-lab/`

Role:
```text
surface -> Agent OS -> MCP gateway -> bounded capability -> source/tool
                                     -> evidence/result -> human-controlled action
```

MCP is a capability boundary, not a replacement Agent OS.

### 3. ML research — KUBERA TAO LAB
Public path: `kubera-lab/kubera-tao-lab/`

Private implementation: `saturnom999-lab/kubera-tao-lab`.

Role:
- model evaluation discipline;
- temporal validation;
- strict unseen-property testing;
- leakage control;
- bias/error analysis;
- ONNX/deployment checks.

### 4. Product architecture — KUBERA Real Estate OS
Public path: `kubera-lab/real-estate-os/`

Private implementation: `kubera-lab/kubera-real-estate-os`.

Role:
- property intelligence;
- workflow/CRM architecture;
- governance and multi-tenant design;
- future authenticated integrations.

Current status remains bootstrap; architecture is not labelled as production.

## Applied systems

### Tender Intelligence
Path: `kubera-lab/tender-intelligence/`

Official read-only procurement intake -> normalize/provenance -> deadline/CPV/requirements/buyer checks -> BID/REVIEW/NO-BID -> DRAFT_ONLY bid pack -> human.

### Council AI Service Finder
Path: `research/council-ai-service-finder/eval/v0.1/`

Deterministic resident-language retrieval evaluation with regression tests and explicit fallbacks.

### Community Compass
Path: `kubera-lab/dzambala-community-compass/`

Local/event intelligence with source validation and provenance-oriented data handling. Ended events stay in a past-events archive; upcoming events are shown only when verified.

### Kubera Agent Fabric
Path: `research/kubera-agent-fabric/prototype/`

Research prototype for local agents that answer area questions.

## Repository guardrails
- `tools/portfolio_audit.py` + `.github/workflows/portfolio-audit.yml` — headline-claim and evidence-path audit (path-filtered).
- `.github/workflows/protected-paths.yml` + `.github/scripts/check_protected_paths.py` — flags any pull request that touches the root README or the frozen Kubera Guide folder (`kubera-lab/kubera-guide-global-mapping/`).

## Supporting / library repositories

These remain useful but are not flagship portfolio items:
- migration/visa templates;
- learning repositories;
- prompt libraries;
- small infrastructure experiments;
- legacy web prototypes.

Forks used for upstream/open-source participation remain separate from KUBERA product claims.

## Public/private rule

Private implementation history is not made public merely for appearance. Public dossiers expose architecture, status and verified evidence without publishing credentials, client data, raw private datasets or unsafe history.

## Rule

**KUBERA prepares. Capabilities stay bounded. Evidence is explicit. The human remains the authority.**
