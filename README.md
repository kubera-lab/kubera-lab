<div align="center">

**NIKOLA KUBERA**

<sub>Technical Solutions Developer · London, United Kingdom</sub>

<sub>AI · Data · Automation · Digital Products · Research</sub>

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=500&size=18&duration=3500&pause=1300&color=70B7F4&center=true&vCenter=true&width=760&height=44&lines=Exploring+ideas.+Building+systems.;From+real-world+operations+to+digital+innovation.;Human-led+AI.+Practical+products.+Verified+results." alt="Animated introduction to KUBERA's work" />

**A connected portfolio of technology projects, experiments and practical solutions.**

[**Explore projects ↓**](#-the-kubera-portfolio) · [**See engineering results ↓**](#-selected-results--evidence) · [**Hugging Face ↗**](https://huggingface.co/spaces/Dzambala/kubera-geoai)

</div>

---

## 👋 About me

I am **Nikola Kubera**, a **Technical Solutions Developer** building practical systems across AI, data, automation and digital products.

My work focuses on turning real operational problems into clear, testable tools. I use AI as part of the engineering workflow, but keep evidence, limitations and human control visible.

**Current flagship:** [KUBERA GEO SI](https://github.com/kubera-lab/kubera-geoai) — evidence-first property intelligence for UK estate agencies. [Live demo ↗](https://kubera-geoai.pages.dev)

**What I do hands-on:** Python and TypeScript applications · LLM tool-calling with server-side validation · open-data pipelines and geospatial products · automated tests and CI/CD · technical documentation.

**My role and AI-assisted development:** I define the problem, the architecture and the acceptance checks. AI tools help draft code; every change is reviewed, tested in CI and checked on the live system before it counts as done.

### ✅ Verify in one click

| | KUBERA AGENT OS (reference implementation) |
| :--- | :--- |
| **Code** | [Python package, tests and examples](https://github.com/kubera-lab/kubera-lab/tree/main/kubera-lab/innovation-stack/reference-implementation) |
| **CI** | [![Tests](https://github.com/kubera-lab/kubera-lab/actions/workflows/test-innovation-stack-reference.yml/badge.svg)](https://github.com/kubera-lab/kubera-lab/actions/workflows/test-innovation-stack-reference.yml) — Python 3.11 · 3.12 · 3.13 |
| **Architecture** | [Technical dossier](KUBERA_AGENT_OS.md) · [Engineering notes](kubera-lab/agent-os/) |
| **Run it** | `cd kubera-lab/innovation-stack/reference-implementation && pip install -e . && python -m unittest discover -s tests && python -m kubera_innovation demo --json` |


### 💡 How I work

| Principle | What it means in practice |
| :--- | :--- |
| **Evidence first** | Every figure, claim and recommendation carries its source, retrieval date and known limitations. If something has not been verified, it is labelled as such — never presented as fact. |
| **Human authority** | AI prepares, drafts and checks; people approve. Consequential actions — publishing, merging, sending, paying — pass through an explicit human decision. |
| **Practical engineering** | Systems are designed around a real user and a real workflow. Success is measured by whether the work gets done correctly, not by how impressive the AI looks. |
| **Verified delivery** | Every change goes through a branch, automated checks, review and a live verification after release. Problems found later are fixed openly, with the reason recorded. |
| **Lawful, open data** | Data is used only where the licence allows it. Official open datasets are preferred, and restricted sources are kept out of public products. |
| **Plain communication** | Results are explained in clear language for the people who use them — what was done, what is proven and what still needs a decision. |

---

## 🧭 Focus

**AI systems** · **Data quality** · **Automation** · **Geospatial products** · **Evaluation & assurance**

---

## 🚀 The KUBERA portfolio

These projects represent different directions and stages of development. Their individual pages contain the technical details.

| Project | What it does | Stage |
| :--- | :--- | :--- |
| **[KUBERA AGENT OS](kubera-lab/agent-os/)** | A reference architecture for coordinating bounded AI workflows with human oversight and verifiable actions | Reference implementation |
| **[KUBERA GEO SI](https://github.com/kubera-lab/kubera-geoai)** | Evidence-first property intelligence for UK estate agencies · [Live demo ↗](https://kubera-geoai.pages.dev) · [Hugging Face showcase ↗](https://huggingface.co/spaces/Dzambala/kubera-geoai) | Live demo |
| **[KUBERA TAO LAB](kubera-lab/kubera-tao-lab/)** | Machine-learning research focused on disciplined evaluation, reproducibility and model robustness | Research |
| **[KUBERA Real Estate OS](kubera-lab/real-estate-os/)** | A wider concept for connected real-estate operations and information workflows | Product concept |
| **[KUBERA Tender Intelligence](kubera-lab/tender-intelligence/)** | Research and qualification tools for public-procurement opportunities | Reference prototype |

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&height=3&color=0:0b1220,50:2475a8,100:0b1220" width="90%" alt="" />

</div>

## 🧪 Selected results & evidence

A few concrete examples from the portfolio's documented engineering work — **not claims that every project is production-ready**.

| Project | Documented result |
| :--- | :--- |
| **KUBERA AGENT OS** | **173 tests passing** and **89% branch coverage** — re-run on 25 October 2026 (Python 3.13); CI matrix Python 3.11–3.13 · [Code](https://github.com/kubera-lab/kubera-lab/tree/main/kubera-lab/innovation-stack/reference-implementation) · [CI runs](https://github.com/kubera-lab/kubera-lab/actions/workflows/test-innovation-stack-reference.yml) |
| **KUBERA TAO LAB** | **34/34 local project tests passed**, reported 2 October 2026; research and benchmark limitations documented · [Research dossier](kubera-lab/kubera-tao-lab/) |
| **KUBERA GEO SI** | Live product on official open data (HM Land Registry, EPC, Environment Agency, OpenStreetMap); typed React + TypeScript app, unit and assistant tests, licence guard and automatic deployment after review · [Open live product](https://kubera-geoai.pages.dev) |
| **Tender Intelligence** | Documented read-only procurement research prototype with a human decision step · [Project details](kubera-lab/tender-intelligence/) |

*Figures are dated. AGENT OS figures were re-run on the date shown; other figures are project-reported.*

---

## 🏠 Case study: KUBERA GEO SI

| | |
| :--- | :--- |
| **Problem** | Estate agents in the UK spend time collecting the same facts for every home — past sales, energy rating, flood risk, local context — from many separate official sites. |
| **Users** | Estate agency staff preparing valuations, listings and buyer answers. |
| **Solution** | One map and home card that brings the official facts together, each with its source and date, plus an assistant that answers only from those checked sources. |
| **Technology** | React · TypeScript · Leaflet · Cloudflare Pages & Workers · GitHub Actions · UK open data (OGL) |
| **Quality** | Type checking, unit tests, assistant tests, a build-time guard against restricted data, deployment only after review and a live check |
| **Limits** | Pilot area Mitcham (CR4). Not a valuation tool. Homes for sale appear only from the agency's own listings. |

[Open the live product ↗](https://kubera-geoai.pages.dev)

---

## 🛠️ Technology & working toolkit

Tools are chosen per problem and grouped by the job they do.

| Area | Technologies | Used for |
| :--- | :--- | :--- |
| **Application development** | Python · TypeScript · React · Node.js · Vite · Tailwind CSS | Web products, data pipelines, internal tools and reference implementations |
| **Geospatial & open data** | Leaflet · OpenStreetMap · UK official open data (property, energy, flood, planning, transport, crime) | Map-based products where every layer keeps its source and licence |
| **AI engineering** | LLM tool-calling · server-side validation · retrieval over verified sources · evaluation tests | Assistants that answer from checked data and say "not in our data" instead of guessing |
| **Quality & assurance** | Automated unit and integration tests · type checking · data validation · licence guards | Catching wrong figures, broken data and restricted content before release |
| **Delivery & operations** | Git · GitHub Actions (CI/CD) · Cloudflare Pages & Workers · Linux | Repeatable builds, automatic deployment after review, scheduled data refreshes |
| **Research & showcase** | Hugging Face · technical documentation · source logs | Public demonstrations and traceable research notes |

![Python](https://img.shields.io/badge/Python-1f2937?style=flat-square&logo=python)
![TypeScript](https://img.shields.io/badge/TypeScript-1f2937?style=flat-square&logo=typescript)
![React](https://img.shields.io/badge/React-1f2937?style=flat-square&logo=react)
![Node.js](https://img.shields.io/badge/Node.js-1f2937?style=flat-square&logo=nodedotjs)
![Vite](https://img.shields.io/badge/Vite-374151?style=flat-square&logo=vite)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-374151?style=flat-square&logo=tailwindcss)
![Leaflet](https://img.shields.io/badge/Leaflet-374151?style=flat-square&logo=leaflet)
![Cloudflare](https://img.shields.io/badge/Cloudflare-374151?style=flat-square&logo=cloudflare)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-374151?style=flat-square&logo=githubactions)
![Linux](https://img.shields.io/badge/Linux-374151?style=flat-square&logo=linux)
[![Hugging Face](https://img.shields.io/badge/Hugging%20Face-111827?style=flat-square&logo=huggingface)](https://huggingface.co/spaces/Dzambala/kubera-geoai)

**Core practices:** problem framing · source verification · data validation · prototyping · automated testing · AI-assisted development · technical documentation · human review.

*The toolkit reflects technologies used across the portfolio; it is not a claim of equal depth in every tool.*

---

## ⚡ From prototype to product

KUBERA separates **exploration** from **production**.

- **Exploration** — new ideas, interfaces and assistant behaviours are tested quickly in isolated prototypes. Speed matters here; nothing from this stage reaches users directly.
- **Production** — a capability is promoted into a product such as **KUBERA GEO SI** only after its data, behaviour and limits have been checked against real cases.

**Promotion criteria**

- the data source is identified, licensed for the intended use and dated;
- the behaviour is covered by automated tests, including failure and edge cases;
- limitations are written down and shown to the user where they matter;
- a person has reviewed the change before release, and the live result is checked after it.

A working prototype is treated as a hypothesis, not as proof.

---

## 🔄 From an idea to a working system

| Stage | Focus | Output |
| :--- | :--- | :--- |
| **01 · Discover** | Who is the user, what decision do they need to make, what does success look like | Problem statement and success criteria |
| **02 · Investigate** | Available evidence, open data, licences, existing tools and alternatives | Source register and feasibility notes |
| **03 · Design** | Workflow, responsibilities, data model and clear limits of what the system will not do | Product structure and acceptance checks |
| **04 · Build** | Small, reviewable increments of software, data and AI components | Working feature behind automated checks |
| **05 · Verify** | Tests, live checks, review of evidence and honest reporting of weaknesses | Verified release and documented results |
| **06 · Operate & evolve** | Monitoring, scheduled data refreshes, user feedback and careful expansion | Maintained system with a clear change history |

---

<details>
<summary><strong>📚 Technical documentation</strong></summary>

[Portfolio review](PORTFOLIO_REVIEW.md) · [Project status](STATUS.md) · [Repository map](REPO_MAP.md) · [Extended README](EXTENDED_README.md) · [Technical dossier](KUBERA_AGENT_OS.md) · [Product vision](KUBERA_PRODUCT.md)

</details>

<div align="center">

</div>
