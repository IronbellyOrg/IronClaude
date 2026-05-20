---
id: "GFXAI-MASTER-DOC-TEMPLATE"
title: "GFxAI Master Documentation Template"
description: "Comprehensive template for product, platform, engineering, and AI documentation alignment"
version: "1.0"
status: "🟢 Active"
type: "📝 Template"
priority: "🔥 Highest"
created_date: "2025-01-08"
updated_date: "2025-10-04"
assigned_to: "documentation-team"
autogen: false
autogen_method: ""
coordinator: ""
parent_task: ""
depends_on: []
related_docs:
- DOCUMENTATION_CONTENT_SPEC.md
- governance/documentation-standards.md
tags:
- template
- documentation
- master-template
- structure
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: "static"
---

# Ironbelly GameFrame + GFxAI — Master Documentation Template (Revised)

> **What this is:** a single, living template for the **product + platform** docs of GFxAI.
> **Why it exists:** to align business, product, engineering, and AI workstreams in one place, and to scale from concept → launch → iteration.
> **How to use:** keep this file as the top-level README (or landing page in mkdocs/Docusaurus) and link out to deep dives. Every section below explains **what to include** and **why it matters**.

---

## Table of Contents
- [Executive Summary & Vision](#executive-summary--vision)
- [Audience & Doc Modes](#audience--doc-modes)
- [Use Cases, Demos & Case Studies](#use-cases-demos--case-studies)
- [Business Model & Pricing](#business-model--pricing)
- [Support, SLAs & Customer Success](#support-slas--customer-success)
- [Product Overview](#product-overview)
- [Full Feature List → Epics/Features/Stories/Tasks](#full-feature-list--epicsfeaturesstoriestasks)
- [System Architecture](#system-architecture)
- [AI & GFxAI Documentation](#ai--gfxai-documentation)
- [Frontend (GFxAI App & Wizard)](#frontend-gfxai-app--wizard)
- [Backend (GFxAI Services)](#backend-gfxai-services)
- [Development Process & Decision Logs](#development-process--decision-logs)
- [Testing & QA](#testing--qa)
- [Deployment & Ops](#deployment--ops)
- [Security & Compliance](#security--compliance)
- [Documentation Maintenance](#documentation-maintenance)
- [Appendices](#appendices)
- [External: GameFrame (UE) Documentation](#external-gameframe-ue-documentation)

> **Note on GameFrame content**: this master template **does not embed** GameFrame gameplay system docs. Those live in a separate, external GameFrame documentation set and are linked from [External: GameFrame (UE) Documentation](#external-gameframe-ue-documentation).

---

# Executive Summary & Vision
<!--
WHAT: A crisp narrative anyone can grok in 60–90 seconds.
WHY: Aligns investors, partners, and the team on the “why” and “where we’re going.”
-->

## High-level Concept
<!-- 2–3 sentences describing GFxAI at a glance (problem, solution, outcome). -->

## Goals & Success Metrics
- **Primary goals:** <!-- e.g., reduce time-to-first-playable < 1 hr; enable NL→safe changes; ship demo #1 -->
- **KPIs/SLOs:** <!-- business (signups, activation %), product (task success rate), tech (latency, success rate of applied plans) -->

## Differentiators
<!-- Bullet list of unique advantages vs point tools, engines, or generic AI assistants (e.g., UE-integrated changes with diffs/rollback, wizard seeding, verifiable DT edits). -->

## Vision (12–36 months)
- **North Star:** <!-- long-term state -->
- **Milestones:** <!-- YYYY-Q# checkpoints; keep to one line each -->

---

# Audience & Doc Modes
<!--
WHAT: Who this doc is for and how they should consume it.
WHY: Different readers need different paths; prevents “wall of text” syndrome.
-->
- **External (Investors/Partners):** vision, market, roadmap, demos.
- **Users (Designers/Engineers):** quickstarts, guides, API, UE manager usage.
- **Internal (PM/Eng/QA/CS):** ADRs, runbooks, SLOs, evals, process.

> Link entry points (or tags) to filter content for each audience.

---

# Use Cases, Demos & Case Studies
<!--
WHAT: Top 3–5 jobs-to-be-done, with demo scripts and measurable outcomes.
WHY: Focuses the product and supports sales/marketing with repeatable narratives.
-->
## Top Use Cases
- <!-- e.g., “Prototype a shooter loop in 1 hour” → metrics and proof points -->
- <!-- e.g., “Balance sprint/jump/reload across 3 classes” -->

## Demo Scripts
- **Script ID, Time, Assets, Steps, Expected Output, Rollback Plan**  
  <!-- Provide copy-pasteable demo flows with seeded projects for reliability. -->

## Case Studies
- **Problem → Approach → Outcome (metrics) → Quote**  
  <!-- Populate as real results arrive. -->

---

# Business Model & Pricing
<!--
WHAT: Tiers, entitlements, and high-level terms.
WHY: Guides packaging, feature gating, and roadmap trade-offs.
-->
- **Tiers & Entitlements:** <!-- hobbyist/indie/enterprise; source access add-on; on-prem -->
- **Billing/License Summary:** <!-- monthly, annual, rev-share, enterprise buyout -->
- **Upgrade Paths:** <!-- how teams move up tiers; gates tied to features -->

---

# Support, SLAs & Customer Success
<!--
WHAT: Channels, SLAs, onboarding, and ongoing success plans.
WHY: Sets expectations and informs internal ops/readiness.
-->
- **Channels:** <!-- email, portal, Discord -->
- **SLA Targets:** <!-- response/restore by severity -->
- **Onboarding Checklists (30/60/90):** <!-- owners + acceptance criteria -->
- **Customer Success Cadence:** <!-- QBRs, health scores, expansion signals -->

---

# Product Overview
<!--
WHAT: Audience/problem/solution, core features, and concise roadmap.
WHY: The spine for sales decks, landing pages, and internal alignment.
-->
## Target Users & Use Cases
| Persona | Needs | Primary Flows | Success Criteria |
|---|---|---|---|
| <!-- e.g., Solo Indie, Producer, UE Engineer --> |  |  |  |

## Market Positioning
- **Category:** <!-- e.g., AI-assisted game creation platform -->
- **Competitive Set:** <!-- who users compare us with; why we win -->

## Core Features & Benefits
<!-- Map feature → benefit → metric (proof). Keep bullets terse. -->

## Product Roadmap (concise)
| Quarter | Initiative | Owner | Status | Notes |
|---|---|---|---|---|

---

# Full Feature List → Epics/Features/Stories/Tasks
<!--
WHAT: The canonical, structured list of capabilities with metadata to generate work items.
WHY: Turns vision into an executable backlog and keeps PM/Eng in lockstep.
-->
> **How to use:** maintain this table as the **source of truth**. Export/filter to generate epics/features/stories in your PM tool.

### Feature Catalog (Authoritative)
| ID | Epic | Feature | User Value (1-2 lines) | Priority (R/M/C) | MoSCoW | OKR/Metric | Dependencies | Risks/Notes | Status |
|---|---|---|---|:---:|:---:|---|---|---|:---:|
| FEAT-001 | Onboarding | Wizard: genre/camera/art seed | Guided project seeding for non-experts | R | M | Time-to-setup | Backend `/session` | – | Planned |
| … | … | … | … | … | … | … | … | … | … |

**Taxonomy & Export Rules**
- **Epic** → **Feature** → **User Story** → **Task**  
- **User Story template:**  
  ```
  As a <persona>, I want <capability>, so that <value>. 
  Acceptance: Given/When/Then…
  NFRs: perf, security, telemetry.
  ```
- **Export mapping:**  
  - **Epic** = group by `Epic`  
  - **Feature** = rows grouped under epic  
  - **Stories** = 1–3 per Feature (derive from “User Value”)  
  - **Tasks** = technical steps (create DT schema, add endpoint, write E2E)

> Keep IDs stable. Use **Dependencies** to auto-sequence roadmaps.

---

# System Architecture
<!--
WHAT: The big picture (C4 L1–L2) and operational constraints.
WHY: Prevents integration drift; informs security, scale, and staffing.
-->

## High-level Diagrams
```
[Diagram Placeholder: System Context (C4 Level 1): FE ↔ BE ↔ UE Manager ↔ UE Project]
```

## Components & Dependencies
- **GFxAI Agents & Orchestrator:** <!-- coordination (e.g., LangGraph), queues, memory classes -->
- **Data Layer:** <!-- Postgres/Redis/vector/object storage, retention -->
- **UE Manager:** <!-- launch/attach/PIE, DataTable read/write, script exec -->
- **Onboarding Wizard:** <!-- seeding flows and persisted state -->
- **External Services:** <!-- e.g., PlayFab/EOS/Steam; note what’s current vs future -->

## Scalability, Performance, Security
- **Perf Targets:** <!-- p95 plan latency, apply success %, editor uptime -->
- **Scale Plan:** <!-- horizontal workers, shard keys, GPU pools -->
- **Security Model:** <!-- authN/Z boundaries, token flows, secrets handling, PII map -->

> Add a Mermaid sequence for **NL → plan → act → verify → diff/rollback**.

---

# AI & GFxAI Documentation
<!--
WHAT: Everything specific to AI integration: models, prompts, agents, orchestration, and (optionally) retrieval.
WHY: Makes AI behavior inspectable, testable, and safe. Note: If you are not using RAG now, keep the placeholders and mark “N/A” until adopted.
-->

## AI System Overview
- **Current Integration:** <!-- LLM provider(s), invocation patterns, streaming, retries -->
- **Agents & Orchestration:** <!-- roles, tool interfaces, handoffs, decision graph -->
- **Memory Strategy:** <!-- what we remember (per project/session), expiration, scoping -->

## (Optional) Retrieval / RAG
- **Status:** <!-- “Not used currently” OR “Pilot” OR “In production” -->
- **If used:** sources, chunking, embeddings (model/dims), index schema, filter strategy.

## Prompting & Models
- **Prompt Templates (by agent/tool):**
  ```text
  <system>
  Role: Movement Specialist
  Goals: …
  Constraints: …
  Tools available: dt_write, run_script
  Success = verified change + diff + rollback token
  </system>
  ```
- **Model Selection Matrix**
  | Use Case | Model | Context Window | Latency Target | Fallback |
  |---|---|---|---|---|

## Evaluation & Safety
- **Eval Suite:** <!-- pass@k on known tasks, factuality checks, plan/apply success -->
- **Risk Controls:** <!-- dry-run, schema clamps, range guards, human confirm -->
- **Failure Modes & Recovery:** <!-- timeouts, degraded mode, mock provider -->

## Sample NL → Engine Modification Pipeline
1. **User:** “Increase player sprint speed by 20%.”
2. **Parse/Plan:** intent → field mapping → safety bounds.
3. **Act:** DT update or UE script; bounded timeout.
4. **Verify:** PIE or scripted check; produce **diff + rollback token**.
5. **Confirm:** surface to UI with accept/rollback.

---

# Frontend (GFxAI App & Wizard)
<!--
WHAT: UX intent, key screens, and API contracts used by FE.
WHY: Keeps FE/BE contracts explicit and UX reproducible.
-->

## UX Goals & Principles
<!-- performance, progressive disclosure, a11y, error recovery -->

## Onboarding Flows & UI States
```
[Diagram Placeholder: Wizard steps, guards, resume rules, persistence]
```

## Key Screens & Journeys
- Chat/Console • Project Setup Wizard • Agent Activity/Logs • Data Table Editor • Live Preview

## API Contracts with Backend
| Endpoint | Method | Request | Response | Errors | Notes |
|---|---|---|---|---|---|
| /api/session | POST | <!-- JSON --> | <!-- JSON --> | <!-- codes --> | idempotency rules |
| /api/plan | POST |  |  |  |  |
| /api/act  | POST |  |  |  |  |

## Frontend Tech Notes
- **Stack:** <!-- Next.js/SSR, state mgmt, query -->
- **Env Vars:** <!-- NEXT_PUBLIC_* -->
- **Performance:** <!-- budgets, code-split -->
- **Accessibility:** <!-- keyboard nav, ARIA patterns -->

---

# Backend (GFxAI Services)
<!--
WHAT: Service shape, APIs, persistence, and observability.
WHY: Ensures contracts are stable and operable.
-->

## Service Overview
- **Auth/AuthZ**, **Orchestration**, **UE Manager Integration**, **WebSockets/Events**

## API Endpoints & Schemas
```yaml
openapi: 3.0.3
info: { title: GFxAI API, version: 0.1.0 }
paths:
  /api/ping:
    get: { responses: { '200': { description: OK } } }
  # Link full spec at /api/openapi.yaml
```

## Data Persistence
- **Relational:** <!-- schemas, migrations -->
- **Vector (if used):** <!-- index names, dims -->
- **Artifacts:** <!-- diffs, logs, bundles; retention -->

## Logging, Monitoring, Error Handling
- **Logs:** JSON with correlation IDs
- **Metrics:** plan latency, apply success, editor uptime
- **Errors:** taxonomy, retries, DLQs
- **Audit:** every mutation emits a **JSON diff** + **rollback token**

---

# Development Process & Decision Logs
<!--
WHAT: How we make and record decisions; reduces institutional memory risk.
WHY: Future-proofs the project and accelerates onboarding.
-->

## Architecture Decision Records (ADR)
**Template**
```
# ADR: <short title>
Date: YYYY-MM-DD  |  Status: Proposed|Accepted|Deprecated|Rejected  |  Owners: <names>

## Context
## Decision
## Alternatives Considered
## Consequences
- Positive:
- Negative:
- Follow-ups:
```

## Technical Trade-offs
<!-- Summary list linking to ADRs. -->

## Lessons Learned & Future Considerations
<!-- Keep running log; prune quarterly. -->

## Open Questions
| Question | Owner | By When | Notes |
|---|---|---|---|

---

# Testing & QA
<!--
WHAT: Strategy, coverage, and Unreal-specific test hooks.
WHY: Prevents regressions and builds trust in AI-driven changes.
-->

## Test Strategy
| Level | Scope | Tools | Gate |
|---|---|---|---|
| Unit | functions/modules | <!-- pytest, vitest, gtest --> | required |
| Integration | service↔DB/UE-mgr |  | required |
| System/E2E | FE ↔ BE ↔ UE |  | release |
| AI Evals | prompts/tools/safety |  | weekly |

## Coverage Targets
- **Code:** <!-- % per repo -->
- **Prompts/Agents:** <!-- pass@k, accuracy -->

## Unreal-specific Testing
- **PIE Automation:** <!-- scripts + expected outputs -->
- **Data Table Validation:** <!-- schema + range checks -->
- **Determinism:** <!-- seeds; replay plans in CI -->

## QA Scripts & Acceptance Criteria
```
[Checklist Placeholder per feature with Given/When/Then steps]
```

---

# Deployment & Ops
<!--
WHAT: Environments, CI/CD, monitoring, and runbooks.
WHY: Ensures reliability and predictable releases.
-->

## Environments
| Env | Purpose | URLs | Data Sources | Notes |
|---|---|---|---|---|
| Dev |  |  |  |  |
| Staging |  |  |  |  |
| Prod |  |  |  |  |

## Setup Guides
- **UE Projects:** <!-- engine version, paths, plugins -->
- **Orchestration:** <!-- containers/K8s/Helm -->
- **(Optional) Retrieval/Index:** <!-- creation, ingestion jobs -->

## CI/CD Pipelines
- **Build:** lint, test, package
- **Security Gates:** SAST/DAST, SBOM
- **Promotion:** staging → prod; approvals

## Monitoring, Logging, Alerting
- **Dashboards:** <!-- link placeholders -->
- **Runbooks:** <!-- common incidents; step-by-step remediation -->
- **SLOs:** <!-- error budget policy and review cadence -->

---

# Security & Compliance
<!--
WHAT: Data privacy, model safety, and program compliance (SR&ED/CTMM).
WHY: Protects users and unlocks funding/enterprise deals.
-->

## Data Privacy & User Data Handling
- **Data Map:** where PII lives; retention & access controls
- **RBAC/Least Privilege:** roles and boundaries

## Model Safety & Bias Mitigation
- **Safety Filters:** input/output guardrails
- **Red Teaming:** cadence, scenarios, results

## Regulatory/Program Compliance
- **SR&ED / CTMM Artifacts:** how evidence is collected (specs, experiments, failed approaches, learnings), time & cost mapping
- **Licensing:** OSS/3rd-party obligations

---

# Documentation Maintenance
<!--
WHAT: Keeping docs current as the product evolves.
WHY: Prevents rot and maintains trust.
-->

## Versioning & Changelog
```
## [x.y.z] - YYYY-MM-DD
### Added
### Changed
### Fixed
### Removed
```

## Update Guidelines
- **DoD includes docs** (PRs must update relevant sections).
- **Doc Linting in CI:** markdownlint + broken-link checks.

## Ownership & Contribution Model
- **Doc Owners:** by area
- **Change Process:** labels, reviewers, SLAs

---

# Appendices
<!-- Reusable templates that teams copy/paste. -->

## Templates
- **User Story**
  ```
  As a <persona>, I want <capability>, so that <value>.
  Acceptance: Given/When/Then…
  NFRs: perf, security, telemetry.
  ```
- **API Spec (per endpoint)**
  ```
  ## <METHOD> /api/<path>
  Summary, Auth, Idempotency
  Request: headers + example JSON
  Response 200: example JSON
  Errors: 400/401/409/5xx (client actions)
  ```
- **AI Agent Card**
  ```
  # Agent: <Name>
  Role • Inputs • Tools • Outputs • Policies
  Prompt Template (system) …
  Evaluation metrics
  Failure modes & recovery
  ```

## Glossary
| Term | Definition |
|---|---|
| GFxAI | AI control plane for UE projects |
| UE Manager | Service controlling Unreal (launch, PIE, DT edits, scripts) |
| RAG | Retrieval-Augmented Generation (if/when adopted) |
| PIE | Play-In-Editor |
| … |  |

---

# External: GameFrame (UE) Documentation
<!--
WHAT: Pointer to the separate GameFrame docs (plugins, Blueprints, C++ modules, gameplay systems).
WHY: Keeps this product doc focused while giving engineers what they need.
-->
- **Canonical link:** <!-- URL or repo path to GameFrame docs -->
- **Integration points from GFxAI → GameFrame:** <!-- high-level list of DTs, modules, BP hooks referenced by GFxAI -->

---

<!--
Authoring Notes:
- Every section above includes WHAT/WHY instructions to guide authors.
- Keep this page short; push details to linked docs.
- Use stable IDs and headings; include examples for every contract.
- Maintain the Feature Catalog — it drives planning across PM/Eng/QA.
-->
