# Research: PRD and TDD Creator Skills Full Audit

**Investigation type:** Code Tracer
**Scope:** .claude/skills/prd/SKILL.md, .claude/skills/tdd/SKILL.md
**Status:** Complete
**Date:** 2026-03-24

---
## Part 1: PRD Skill Audit

### 1.1 Skill Identity and Trigger

**File:** `.claude/skills/prd/SKILL.md` (1373 lines)
**YAML name:** `prd`
**Trigger phrases:** "create a PRD for...", "document the product requirements", "write a PRD", "populate this PRD", "product requirements for...", "define the product"

---

### 1.2 Output Files — Exact Paths and Format

| Artifact | Path Pattern |
|----------|-------------|
| MDTM Task File | `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/TASK-PRD-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Gaps log | `${TASK_DIR}gaps-and-questions.md` |
| Analyst reports | `${TASK_DIR}qa/analyst-completeness-report.md`, `${TASK_DIR}qa/analyst-synthesis-review.md` |
| QA reports (research gate) | `${TASK_DIR}qa/qa-research-gate-report.md` |
| QA reports (synthesis gate) | `${TASK_DIR}qa/qa-synthesis-gate-report.md` |
| QA reports (report validation) | `${TASK_DIR}qa/qa-report-validation.md` |
| QA reports (qualitative review) | `${TASK_DIR}qa/qa-qualitative-review.md` |
| **Final PRD** | `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md` |
| Template schema | `docs/docs-product/templates/prd_template.md` |

**File numbering convention:** Zero-padded sequential: `01-`, `02-`, `03-`, etc.

---

### 1.3 PRD YAML Frontmatter Fields

The template at `docs/docs-product/templates/prd_template.md` defines these frontmatter fields (referenced throughout the skill):
- `id`
- `title`
- `status` (set to `"🟡 Draft"` at assembly, `"🟢 Done"` at Phase 7 completion)
- `created_date`
- `tags`
- `depends_on`

The **Document Information table** (embedded in the PRD body, 9 rows) contains: Product Name, Product Owner, Engineering Lead, Design Lead, Stakeholders, Status, Target Release, Last Updated, Review Cadence.

---

### 1.4 Phase Structure (7 Phases)

**Stage A — Scope Discovery & Task File Creation (before task file):**

| Step | What Happens |
|------|-------------|
| A.1 | Check for existing task file / research directory |
| A.2 | Parse & triage PRD request (Scenario A explicit vs B vague); classify as Product PRD vs Feature/Component PRD |
| A.3 | Perform scope discovery — Glob/Grep/codebase-retrieval; map files, plan research assignments, select depth tier |
| A.4 | Write research notes file to `${TASK_DIR}research-notes.md` (6 mandatory categories: EXISTING_FILES, PATTERNS_AND_CONVENTIONS, FEATURE_ANALYSIS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER) |
| A.5 | Review research sufficiency — mandatory gate (8 criteria) |
| A.6 | Template triage (Template 01 simple vs Template 02 complex — almost always Template 02) |
| A.7 | Spawn `rf-task-builder` subagent with BUILD_REQUEST |
| A.8 | Receive and verify task file |

**Stage B — Task File Execution (delegates to `/task` skill):**

| Phase | Name | Activity |
|-------|------|---------|
| Phase 1 | Preparation | Update status, confirm scope, read template, select tier, create task folder |
| Phase 2 | Deep Investigation | Parallel subagent spawning — codebase research agents (Feature Analyst, Doc Analyst, Integration Mapper, UX Investigator, Architecture Analyst) write to `${TASK_DIR}research/` |
| Phase 3 | Completeness Verification | Spawn `rf-analyst` (completeness-verification) + `rf-qa` (research-gate) in parallel; verdicts PASS/FAIL gate progression |
| Phase 4 | Web Research | Parallel web research agents — competitive landscape, market sizing, industry standards, tech trends |
| Phase 5 | Synthesis + QA Gate | Parallel synthesis agents (one per synth file from Synthesis Mapping Table); then `rf-analyst` (synthesis-review) + `rf-qa` (synthesis-gate) in parallel |
| Phase 6 | Assembly & Validation | Single `rf-assembler`; then `rf-qa` (report-validation); then `rf-qa-qualitative` (prd-qualitative) |
| Phase 7 | Present to User & Complete Task | Summary, offer downstream TDD creation, write task log, update frontmatter to Done |

**Tier thresholds:**
- Lightweight: 2–3 codebase agents, 0–1 web agents, 400–800 line PRD
- Standard: 4–6 codebase agents, 1–2 web agents, 800–1,500 lines
- Heavyweight: 6–10+ codebase agents, 2–4 web agents, 1,500–2,500 lines

---

### 1.5 BUILD_REQUEST to rf-task-builder — Key Instructions

The BUILD_REQUEST explicitly encodes the following for synthesis agents:
- **PRD_SCOPE classification** (Product PRD vs Feature PRD) — determines which sections (S5, S8, S9, S16, S17, S18) are N/A or abbreviated
- **DOCUMENTATION STALENESS WARNINGS** — code-contradicted/unverified claims from scope discovery
- **TEMPLATE 02 PATTERN MAPPING** — per-phase agent types and output paths
- **SKILL PHASES TO ENCODE** — exact per-phase checklist requirements, including parallel spawning instructions
- **Agent count guidance by tier**
- **Anti-orphaning rule** — task-completion items must be within Phase 7

For synthesis agents specifically, the BUILD_REQUEST directs the builder to embed the **Synthesis Agent Prompt** from SKILL.md into each Phase 5 checklist item, which instructs synthesis agents to:
- Read the PRD template first
- Follow template structure exactly
- Source every fact from research files
- Use As a / I want / So that format for user stories
- Use RICE or MoSCoW for requirements prioritization
- Apply [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED] discipline

---

### 1.6 Final PRD — Section by Section (28 numbered sections + appendices)

| Section | Title | Content |
|---------|-------|---------|
| 1 | Executive Summary | 2-3 paragraphs + Key Success Metrics |
| 2 | Problem Statement | Core problem, why solutions fall short, market opportunity |
| 3 | Background & Strategic Fit | Why now, company alignment, strategic bets |
| 4 | Product Vision | One-sentence vision with expansion |
| 5 | Business Context | Market opportunity (TAM/SAM/SOM), business objectives, KPIs |
| 6 | Jobs To Be Done (JTBD) | When/I want/So that format, related jobs table |
| 7 | User Personas | Primary/secondary/tertiary personas with attribute tables; anti-personas |
| 8 | Value Proposition Canvas | Customer profile, value map (pain relievers + gain creators), fit assessment |
| 9 | Competitive Analysis | Landscape table, feature comparison matrix, positioning statement, response plan |
| 10 | Assumptions & Constraints | Technical/business/user assumptions with risk-if-wrong; constraints table |
| 11 | Dependencies | External, internal, cross-team dependency tables |
| 12 | Scope Definition | In scope, out of scope, permanently out of scope |
| 13 | Open Questions | Question tracking table with owner, status, resolution |
| 14 | Technical Requirements | Architecture, performance, security, scalability, data & analytics |
| 15 | Technology Stack | Backend, frontend, infrastructure technology tables |
| 16 | User Experience Requirements | Onboarding metrics, core user flows, accessibility, localization |
| 17 | Legal & Compliance Requirements | Regulatory compliance, data privacy, terms & policies |
| 18 | Business Requirements | Monetization strategy, pricing tiers, go-to-market, support |
| 19 | Success Metrics & Measurement | Product/business/technical metrics with targets and measurement frequency |
| 20 | Risk Analysis | Technical/business/operational risk matrices with mitigations |
| 21 | Implementation Plan | 21.1 Epics, Features & Stories (epic summary + user stories with ACs); 21.2 Product Requirements (core features + RICE matrix); 21.3 Implementation Phasing; 21.4 Release Criteria & DoD; 21.5 Timeline & Milestones |
| 22 | Customer Journey Map | Journey stages table, moments of truth |
| 23 | Error Handling & Edge Cases | Error categories, edge case scenarios, graceful degradation plan |
| 24 | User Interaction & Design | Wireframes/mockups table, design system checklist, prototype links |
| 25 | API Contract Examples | Key endpoint request/response examples |
| 26 | Contributors & Collaboration | Contributor table, how to contribute guidelines |
| 27 | Related Resources | Customer research, technical docs, design assets, business documents |
| 28 | Maintenance & Ownership | Document ownership, review cadence, update process |
| Appendices | — | Glossary, Acronyms, Technical Architecture Diagrams, User Research Data, Financial Projections |
| Document Approval | — | Approval signature table |

**Key section for TDD handoff: Section 21 (Implementation Plan)** contains epics, user stories with acceptance criteria, RICE matrix, implementation phasing, and release criteria. Section 19 contains all success metrics with measurement methods. Section 5 contains KPIs.

---

### 1.7 Synthesis File Mapping (synth-01 through synth-09)

The standard 9 synthesis files and what PRD sections they cover:

| Synth File | Template Sections |
|------------|------------------|
| `synth-01-exec-problem-vision.md` | S1 Executive Summary, S2 Problem Statement, S3 Background & Strategic Fit, S4 Product Vision |
| `synth-02-business-market.md` | S5 Business Context, S6 JTBD, S7 User Personas, S8 Value Proposition Canvas |
| `synth-03-competitive-scope.md` | S9 Competitive Analysis, S10 Assumptions & Constraints, S11 Dependencies, S12 Scope Definition |
| `synth-04-stories-requirements.md` | S13 Open Questions, S21.1 Epics Features & Stories, S21.2 Product Requirements |
| `synth-05-technical-stack.md` | S14 Technical Requirements, S15 Technology Stack |
| `synth-06-ux-legal-business.md` | S16 UX Requirements, S17 Legal & Compliance, S18 Business Requirements |
| `synth-07-metrics-risk-impl.md` | S19 Success Metrics, S20 Risk Analysis, S21.3-21.5 Phasing/Release Criteria/Timeline |
| `synth-08-journey-design-api.md` | S22 Customer Journey, S23 Error Handling, S24 User Interaction, S25 API Contracts |
| `synth-09-resources-maintenance.md` | S26 Contributors, S27 Related Resources, S28 Maintenance & Ownership |

**The most TDD-relevant synth files are `synth-04` (epics/stories/ACs/requirements) and `synth-07` (success metrics/risk/implementation plan).**

---

### 1.8 Phase 7 TDD Handoff Offer

Phase 7 explicitly contains this instruction to the orchestrating agent:

> "Ask about downstream documents: 'This PRD can feed directly into a Technical Design Document. Would you like me to create a TDD using the `/tdd` skill? The research files are already in place.' If yes, invoke the `tdd` skill with the PRD as input."

This is the only cross-skill handoff instruction in the PRD skill. The PRD research files are positioned as reusable TDD inputs.

---

## Part 2: TDD Skill Audit

### 2.1 Skill Identity and Trigger

**File:** `.claude/skills/tdd/SKILL.md` (1344 lines)
**YAML name:** `tdd`
**Trigger phrases:** "create a TDD for...", "design the architecture for...", "write a technical design document", "populate this TDD", "TDD for the agent system", "technical design for the wizard", "design this system", "architect this feature", "turn this PRD into a TDD"

---

### 2.2 Output Files — Exact Paths and Format

| Artifact | Path Pattern |
|----------|-------------|
| MDTM Task File | `${TASK_DIR}${TASK_ID}.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| **PRD extraction file** | `${TASK_DIR}research/00-prd-extraction.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Gaps log | `${TASK_DIR}gaps-and-questions.md` |
| Analyst reports | `${TASK_DIR}qa/analyst-[gate]-report.md` |
| QA reports | `${TASK_DIR}qa/qa-[gate]-report.md` |
| QA qualitative review | `${TASK_DIR}qa/qa-qualitative-review.md` |
| **Final TDD** | `docs/[domain]/TDD_[COMPONENT-NAME].md` |
| Template schema | `docs/docs-product/templates/tdd_template.md` |

**Key difference from PRD:** The TDD has a dedicated `00-prd-extraction.md` file slot — `${TASK_DIR}research/00-prd-extraction.md` — which is explicitly numbered `00` so it comes before all other research files in the sequence.

---

### 2.3 TDD Frontmatter Fields

From the template (referenced throughout the skill):
- `id`
- `title`
- `status` (set to `"🟡 Draft"` at assembly, `"🟢 Done"` at Phase 7)
- `created_date`
- `parent_doc` (link to PRD if applicable — explicit PRD traceability field)
- `depends_on`
- `tags`

The **Document Information table** (7 rows + Approvers table): Component Name, Component Type, Tech Lead, Engineering Team, Target Release, Last Updated, Status.

**Notable:** `parent_doc` is a first-class frontmatter field for the PRD link, creating an explicit document lineage.

---

### 2.4 PRD Input — How It Is Accepted

**PRD_REF** is one of the four input fields (step A.2 Parse & Triage), defined as:
> "A Product Requirements Document that this TDD implements. When provided, the TDD extracts relevant epics, user stories, acceptance criteria, technical requirements, and success metrics from the PRD as foundational context."

**The input section states explicitly:**
> "The PRD feeds the TDD the same way tech-research feeds a tech-reference — it provides verified requirements context that the TDD translates into engineering specifications. If no PRD exists, a sufficiently detailed feature description serves the same purpose."

**PRD_REF is optional but strongly recommended.** The skill does not require it. The clarification template the skill shows when a prompt is incomplete asks: "Is there a PRD or feature spec to work from? (This significantly improves requirements traceability)"

---

### 2.5 Where PRD Content Is Consumed — Stage A Scope Discovery

**Step A.3 (Scope Discovery), item 2 (Map the component's files and directories)** contains this instruction:

> "**If PRD_REF is provided**, read the PRD and extract: relevant epics, user stories, acceptance criteria, technical requirements, technology stack, success metrics/KPIs, scope definition (in/out/deferred), performance/security/scalability requirements."

This is the first explicit PRD read in the skill. It happens **before the task file is created**, during scope discovery in Stage A. The extracted content goes into the `PRD_CONTEXT` section of the research notes file (`${TASK_DIR}research-notes.md`).

**Research notes `PRD_CONTEXT` section:**
> "If PRD provided: extracted epics, user stories, acceptance criteria, technical requirements, success metrics, scope boundaries. If no PRD: 'N/A — no PRD provided, using feature description as requirements source.'"

**Sufficiency gate A.5, item 7:**
> "If a PRD was provided: is PRD_CONTEXT populated with extracted requirements (epics, acceptance criteria, technical requirements, scope boundaries)?"

This is a mandatory gate — if PRD_CONTEXT is empty when a PRD was provided, the research notes are insufficient and scope discovery must be redone.

---

### 2.6 Where PRD Content Is Consumed — Phase 2 (Deep Investigation)

**Phase 2 (Deep Investigation) — BUILD_REQUEST phase encoding:**

> "If PRD provided: first item extracts PRD context to `${TASK_DIR}research/00-prd-extraction.md`"

This is a dedicated first checklist item in Phase 2 that precedes all codebase research agents. The PRD is read by a subagent and its content is written to `00-prd-extraction.md` before any other investigation begins.

**Codebase research agent prompt (all research agents in Phase 2)** includes:
> `PRD context: [path to PRD extraction file, if applicable — cross-reference requirements as you research]`

This means all Phase 2 research agents receive the PRD extraction file path and are instructed to cross-reference requirements as they investigate the codebase.

---

### 2.7 Where PRD Content Is Consumed — Phase 5 Synthesis

**Synthesis Mapping Table — PRD extraction appears as a source research file in:**

| Synth File | Uses PRD extraction? |
|------------|---------------------|
| `synth-01-exec-problem-goals.md` | YES — source: "PRD extraction, architecture overview, existing docs" |
| `synth-02-requirements.md` | YES — source: "PRD extraction, architecture overview, all subsystem research" |
| `synth-08-perf-deps-migration.md` | YES — source: "PRD extraction, architecture overview, all subsystem research, web research (performance benchmarks)" |
| `synth-09-risks-alternatives-ops.md` | YES — source: "PRD extraction, all research files, web research (industry practices), gaps log" |
| `synth-03-architecture.md` | No explicit PRD extraction listed |
| `synth-04-data-api.md` | No explicit PRD extraction listed |
| `synth-05-state-components.md` | No explicit PRD extraction listed |
| `synth-06-error-security.md` | No explicit PRD extraction listed |
| `synth-07-observability-testing.md` | No explicit PRD extraction listed |

**Synthesis agent prompt** instructs synthesis agents to:
- Use FR/NFR ID numbering for requirements (FR-001, NFR-001) with priority and acceptance criteria
- Only use [CODE-VERIFIED] findings in Architecture, Data Models, and API Specs sections
- Place [UNVERIFIED] claims in Open Questions
- Include "Alternative 0: Do Nothing" (mandatory)

The synthesis agent prompt does NOT explicitly say "read the PRD extraction file and trace each requirement." It relies on the `00-prd-extraction.md` being listed as a source research file in the research notes mapping.

---

### 2.8 PRD-to-TDD Pipeline Section (Dedicated Section in SKILL.md)

The TDD skill has an explicit dedicated section titled "**PRD-to-TDD Pipeline**" (lines 1315–1326):

> "When a PRD is provided as input, the TDD creation follows an enhanced flow:
> 1. **PRD Extraction** (Step 1.2) — read the PRD and extract requirements, constraints, success metrics, and scope boundaries into `${TASK_DIR}research/00-prd-extraction.md`
> 2. **Requirements Traceability** — every requirement in the TDD's Section 5 should trace back to a PRD epic or user story where applicable
> 3. **Success Metrics Alignment** — TDD Section 4 (Success Metrics) should include engineering proxy metrics for business KPIs defined in the PRD
> 4. **Scope Inheritance** — TDD Section 3 (Goals & Non-Goals) inherits scope boundaries from PRD Section 12 (Scope Definition)
> 5. **Cross-referencing** — the TDD frontmatter's `parent_doc` field links back to the PRD"

This is the most explicit statement of the intended handoff. However, this section is **reference documentation** — it describes intent but does not encode enforcement into the agent prompts or synthesis checklist items.

---

### 2.9 Phase Structure (7 Phases)

**Stage A — Scope Discovery & Task File Creation:**

| Step | What Happens |
|------|-------------|
| A.1 | Check for existing task file |
| A.2 | Parse & triage request; capture PRD_REF |
| A.3 | Scope discovery — **if PRD provided, read it here** and extract to PRD_CONTEXT |
| A.4 | Write research notes (8 sections: EXISTING_FILES, PATTERNS_AND_CONVENTIONS, **PRD_CONTEXT**, SOLUTION_RESEARCH, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER) |
| A.5 | Review research sufficiency — checks PRD_CONTEXT populated if PRD was provided |
| A.6 | Template triage (Template 02 almost always) |
| A.7 | Spawn rf-task-builder with BUILD_REQUEST |
| A.8 | Verify task file |

**Stage B — Task File Execution:**

| Phase | Name | Activity |
|-------|------|---------|
| Phase 1 | Preparation | Update status, confirm scope, read TDD template, select tier, create folder |
| Phase 2 | Deep Investigation | **If PRD: first item extracts PRD to `00-prd-extraction.md`**; then parallel codebase agents (Architecture Analyst, Code Tracer, Data Model Analyst, API Surface Mapper, Integration Mapper, Doc Analyst) — each receives PRD context path |
| Phase 3 | Completeness Verification | `rf-analyst` (completeness-verification) + `rf-qa` (research-gate) in parallel; PASS/FAIL gate |
| Phase 4 | Web Research | Parallel web agents — design patterns, framework docs, security patterns, API design standards, SLO benchmarks |
| Phase 5 | Synthesis + QA Gate | Parallel synthesis agents (one per synth file); then `rf-analyst` (synthesis-review) + `rf-qa` (synthesis-gate, fix_authorization: true) in parallel |
| Phase 6 | Assembly & Validation | Single `rf-assembler`; then `rf-qa` (report-validation); then `rf-qa-qualitative` (tdd-qualitative) |
| Phase 7 | Present to User & Complete Task | Summary; suggest downstream implementation tasks via `/task` skill |

**Tier thresholds:**
- Lightweight: 2–3 agents, 300–600 line TDD
- Standard: 4–6 agents, 800–1,400 lines
- Heavyweight: 6–10+ agents, 1,400–2,200 lines

---

### 2.10 Final TDD — Section by Section (28 numbered sections + appendices)

| Section | Title | TDD-specific content |
|---------|-------|---------------------|
| 1 | Executive Summary | Key deliverables, high-level scope, 2-3 paragraph overview |
| 2 | Problem Statement & Context | Background, problem statement, business context, **PRD reference** |
| 3 | Goals & Non-Goals | Goals with success criteria, non-goals with rationale, future considerations. **Inherits scope from PRD S12** |
| 4 | Success Metrics | Technical metrics and business KPIs with baselines/targets/measurement. **Engineering proxy metrics for PRD KPIs** |
| 5 | Technical Requirements | FR/NFR with ID numbering (FR-001, NFR-001), priority, acceptance criteria. **Requirements trace to PRD epics/stories** |
| 6 | Architecture | High-level architecture, component diagram, system boundaries, key design decisions |
| 7 | Data Models | Data entities with field tables, data flow diagrams, storage strategy |
| 8 | API Specifications | Endpoint overview, detailed specs, error format, API governance |
| 9 | State Management | (frontend only) State architecture, state shape, state transitions |
| 10 | Component Inventory | (frontend only) Page/route structure, shared components, hierarchy |
| 11 | User Flows & Interactions | Sequence diagrams, step-by-step flows, success criteria, error scenarios |
| 12 | Error Handling & Edge Cases | Error categories, edge cases, graceful degradation, retry strategies |
| 13 | Security Considerations | Threat model, security controls, sensitive data, data governance |
| 14 | Observability & Monitoring | Logging, metrics, tracing, alerts, dashboards |
| 15 | Testing Strategy | Test pyramid, unit/integration/E2E test cases, test environments |
| 16 | Accessibility Requirements | WCAG 2.1 AA requirements and testing tools |
| 17 | Performance Budgets | Frontend/backend performance, measurement methods |
| 18 | Dependencies | External, internal, infrastructure dependencies with risk levels |
| 19 | Migration & Rollout Plan | Migration strategy, feature flags, rollout stages, rollback procedure |
| 20 | Risks & Mitigations | Risk table with probability, impact, mitigation, contingency |
| 21 | Alternatives Considered | Alternative 0: Do Nothing (mandatory) + additional alternatives with pros/cons |
| 22 | Open Questions | Question tracking with owner, target date, status, resolution |
| 23 | Timeline & Milestones | High-level timeline, implementation phases with exit criteria |
| 24 | Release Criteria | Definition of Done checklist, release checklist |
| 25 | Operational Readiness | Runbook, on-call expectations, capacity planning |
| 26 | Cost & Resource Estimation | Infrastructure costs, cost scaling model (if applicable) |
| 27 | References & Resources | Related documents and external references |
| 28 | Glossary | Term definitions |
| Document History | — | Version table |
| Appendices | — | A: Detailed API Specs, B: Database Schema, C: Wireframes, D: Performance Test Results |

---

## Part 3: PRD→TDD Handoff Analysis

### 3.1 What PRD Content the TDD Skill Explicitly Consumes Today

The following consumption points are verified from actual TDD SKILL.md text:

| Touch Point | Location in Skill | What It Does |
|-------------|------------------|--------------|
| PRD read during scope discovery | A.3 step 2 | Skill reads PRD and extracts: "relevant epics, user stories, acceptance criteria, technical requirements, technology stack, success metrics/KPIs, scope definition (in/out/deferred), performance/security/scalability requirements" |
| PRD_CONTEXT in research notes | A.4 | Extracted PRD data written to `${TASK_DIR}research-notes.md` under `PRD_CONTEXT` section |
| Sufficiency gate check | A.5 item 7 | Mandatory gate verifies PRD_CONTEXT is populated before proceeding |
| `00-prd-extraction.md` first checklist item | Phase 2, first item | Dedicated subagent extracts PRD to file before parallel research begins |
| Research agent PRD context field | All Phase 2 codebase agents | Each agent receives: `PRD context: [path to PRD extraction file, if applicable — cross-reference requirements as you research]` |
| synth-01 source files | Phase 5 synthesis | PRD extraction listed as source for S1–S4 (Executive Summary, Problem Statement, Goals & Non-Goals, Success Metrics) |
| synth-02 source files | Phase 5 synthesis | PRD extraction listed as source for S5 Technical Requirements |
| synth-08 source files | Phase 5 synthesis | PRD extraction listed as source for S16–S19 (Accessibility, Performance, Dependencies, Migration) |
| synth-09 source files | Phase 5 synthesis | PRD extraction listed as source for S20–S26 (Risks, Alternatives, Open Questions, Timeline, Release, Ops, Cost) |
| `parent_doc` frontmatter field | Assembly Phase 6 | TDD frontmatter links back to PRD via `parent_doc` |
| PRD-to-TDD Pipeline section | Reference section (not enforced) | States 5-point pipeline including traceability, metrics alignment, scope inheritance |

**Summary of what IS consumed:** The PRD extraction file (`00-prd-extraction.md`) is created and listed as a source for 4 of the 9 synthesis files. The PRD_CONTEXT goes into research notes. The `parent_doc` field links the documents. Research agents are told the PRD context path exists.

---

### 3.2 What PRD Content Is NOT Consumed (Gaps)

#### Gap 1: No PRD extraction agent prompt is defined

The skill says "first item extracts PRD context to `${TASK_DIR}research/00-prd-extraction.md`" but **provides no agent prompt template for this extraction step**. The PRD SKILL.md contains 8 named agent prompt templates (Codebase Research, Web Research, Synthesis, rf-analyst Completeness, rf-qa Research Gate, rf-qa Synthesis Gate, rf-qa Report Validation, rf-assembler). The TDD SKILL.md mirrors all 8. **Neither skill has a "PRD Extraction Agent Prompt."** The task builder must invent this prompt from the brief description in Phase 2 encoding. There is no specification of what `00-prd-extraction.md` should contain, what format it should use, or how deeply the extraction should go.

**Evidence:** The artifact appears in the output locations table, Phase 2 encoding description, Synthesis Mapping Table source columns, and PRD-to-TDD Pipeline section — but never in a named, formatted agent prompt template.

#### Gap 2: 5 of 9 synthesis files do not list PRD extraction as a source

The synthesis mapping table shows that `synth-03-architecture.md`, `synth-04-data-api.md`, `synth-05-state-components.md`, `synth-06-error-security.md`, and `synth-07-observability-testing.md` do NOT list `00-prd-extraction.md` as a source research file. These cover:
- S6 Architecture
- S7 Data Models
- S8 API Specifications
- S9 State Management / S10 Component Inventory
- S11 User Flows & Interactions
- S12 Error Handling & Edge Cases
- S13 Security Considerations
- S14 Observability & Monitoring
- S15 Testing Strategy

This means the synthesis agents producing Architecture (S6), Data Models (S7), API Specs (S8), User Flows (S11), Error Handling (S12), Security (S13), and Testing (S15) are **not instructed to read the PRD extraction file**. They will not see PRD acceptance criteria, PRD technical requirements, or PRD error handling expectations when synthesizing these sections.

**For TDDs built from PRDs, this is the largest structural gap.** A PRD's S14 Technical Requirements, S21.1 Epics/Stories/ACs, S21.2 Product Requirements (RICE matrix), and S19 Success Metrics are exactly what should feed the TDD's S6 Architecture, S11 User Flows, S12 Error Handling, and S15 Testing — but the synthesis mapping does not connect them.

#### Gap 3: PRD epics and user stories are not explicitly mapped to TDD requirements

The PRD-to-TDD Pipeline section says: "every requirement in the TDD's Section 5 should trace back to a PRD epic or user story where applicable." However, the synthesis agent prompt (used for `synth-02-requirements.md`) only says:
- "Every fact must come from the research files"
- "Requirements must use FR/NFR ID numbering with priority and acceptance criteria"
- "Documentation-sourced claims require verification status"

There is **no instruction in the synthesis prompt to create a traceability matrix**, to explicitly label requirements with their source PRD story ID, or to ensure coverage of all PRD epics. The synthesis agent will draw from `00-prd-extraction.md` as a source file, but the level of rigor with which it maps PRD stories to FR/NFR items is undefined and agent-discretionary.

#### Gap 4: PRD acceptance criteria are not explicitly ported to TDD functional requirements

The PRD's S21.1 (Epics, Features & Stories) contains user stories with **testable acceptance criteria**. The TDD's S5 (Technical Requirements) should define FR-001 etc. with acceptance criteria traceable to those PRD ACs. However:
- The synthesis agent for `synth-02-requirements.md` is told to use "PRD extraction, architecture overview, all subsystem research" as sources
- It is not told to: read each PRD user story's acceptance criteria → map each AC to a FR-NNN item → verify the AC is preserved or translated into engineering terms
- The QA Synthesis Gate checklist (12 items) checks that requirements have "priority and acceptance criteria" but does not check that the acceptance criteria trace back to specific PRD story IDs

#### Gap 5: PRD success metrics are not explicitly translated to TDD engineering proxy metrics

The PRD-to-TDD Pipeline section says: "TDD Section 4 (Success Metrics) should include engineering proxy metrics for business KPIs defined in the PRD." However:
- `synth-01-exec-problem-goals.md` covers S4 Success Metrics and lists PRD extraction as a source
- The synthesis agent prompt does not include any instruction about "translate PRD KPIs into engineering proxy metrics"
- The QA Synthesis Gate checklist does not check that TDD S4 metrics derive from PRD S19 KPI table
- The rf-qa-qualitative agent prompt mentions "architecture decisions match PRD requirements" and "no PRD content repeated verbatim" — but does not check metric alignment specifically

#### Gap 6: The PRD-to-TDD Pipeline section is reference documentation, not enforced

The dedicated "PRD-to-TDD Pipeline" section (lines 1315–1326) describes 5 intended behaviors. It is NOT:
- Encoded as BUILD_REQUEST instructions to the task builder
- Encoded as checklist items in the synthesis agent prompts
- Checked by the rf-analyst synthesis review (9 criteria)
- Checked by the rf-qa synthesis gate (12 criteria)
- Checked by the rf-qa-qualitative review

The pipeline steps exist as stated intent, not enforced protocol.

---

### 3.3 Exact Locations in the TDD Skill Where PRD Epics, ACs, and Success Metrics Should Be Consumed More Richly

| Where to Change | Phase / Agent | Current State | What's Missing |
|-----------------|--------------|--------------|---------------|
| PRD extraction first item | Phase 2, item 1 | Brief instruction: "first item extracts PRD context to 00-prd-extraction.md" — no prompt template | A named `### PRD Extraction Agent Prompt` template specifying extracted fields, their IDs, and output format |
| synth-03 source files | Phase 5 synthesis | No PRD extraction listed | Add `00-prd-extraction.md` as source; instruct agent to verify architecture covers all PRD epics |
| synth-04 source files | Phase 5 synthesis | No PRD extraction listed | Add `00-prd-extraction.md`; instruct agent to verify data models support all PRD user flows |
| synth-06 source files | Phase 5 synthesis | No PRD extraction listed | Add `00-prd-extraction.md`; instruct agent to check PRD error handling ACs are covered |
| synth-07 source files | Phase 5 synthesis | No PRD extraction listed | Add `00-prd-extraction.md`; instruct agent to check PRD testing ACs appear in test strategy |
| Synthesis Agent Prompt rule set | Phase 5, all synthesis | Rule 11: "never describe architecture from docs alone" — no PRD traceability rule | Add Rule 12: "If 00-prd-extraction.md exists: for each PRD epic create one or more FR-NNN items; for each user story AC verify it appears as-is or translated as FR acceptance criterion; include traceability table: PRD Story ID → FR-NNN" |
| Synthesis Agent Prompt rule set | Phase 5, synth-01 | No KPI translation instruction | Add Rule 13: "For each KPI in PRD S19: define an engineering proxy metric in TDD S4 with format: Business KPI (PRD source) → Engineering Proxy → Measurement Method → Target" |
| Synthesis QA Gate checklist | Phase 5 QA | 12 items — no PRD traceability check | Add item 13: "If PRD provided: sample 3+ FR-NNN items, verify each cites PRD story ID; verify TDD S4 metrics map to PRD S19 KPIs; report untraceable requirements as scope gaps" |
| BUILD_REQUEST SKILL PHASES section | Stage A.7 | PRD-to-TDD Pipeline not in BUILD_REQUEST | Add Phase 2 note: "If PRD_REF provided, first checklist item must use PRD Extraction Agent Prompt from SKILL.md to create 00-prd-extraction.md with structured story-ID/AC/KPI output" |
| BUILD_REQUEST SKILL PHASES section | Stage A.7 | Phase 5 synthesis instructions do not mention PRD traceability | Add to Phase 5 encoding: "Synthesis agents for requirements (synth-02) must produce traceability tables: PRD Story ID → FR-NNN" |

---

### 3.4 What Would Need to Change in the TDD Skill to Close the Handoff Gaps

**Change 1 (highest impact): Add a `### PRD Extraction Agent Prompt` template**

This is the missing foundation. Without a defined extraction format, all downstream synthesis is working from an ad-hoc document. The template should specify:
1. Extract S5 Business Context KPIs as a table: Category / KPI / Target / Measurement Method
2. Extract S12 Scope tables verbatim (In Scope, Out of Scope, Permanently Out of Scope)
3. Extract S14 Technical Requirements by category (architecture, performance, security, scalability)
4. Extract S19 Success Metrics table verbatim
5. Extract S21.1 as structured: per-epic header, then per-story: ID / As-a/I-want/So-that / Acceptance Criteria (bulleted list)
6. Extract S21.2 RICE matrix rows with feature IDs and priorities

**Change 2: Update the Synthesis Mapping Table**

Add `00-prd-extraction.md` to the source columns of synth-03 through synth-07. This is a one-column table edit — no structural changes to the skill flow.

**Change 3: Add PRD traceability rules to the Synthesis Agent Prompt**

The existing synthesis prompt has 11 rules. Add:
- Rule 12: PRD story → FR-NNN traceability table (for synth-02)
- Rule 13: PRD KPI → engineering proxy metric (for synth-01)
- Rule 14: Architecture covers all PRD epics in scope (for synth-03)

**Change 4: Add a 13th item to the Synthesis QA Gate checklist**

The rf-qa synthesis gate checklist checks 12 items. Adding a 13th item for PRD traceability verification (spot-check FR-NNN → PRD story ID, spot-check TDD S4 metrics → PRD S19 KPIs) converts the PRD-to-TDD Pipeline from documentation to enforced quality gate.

**Change 5: Move PRD-to-TDD Pipeline from reference to BUILD_REQUEST encoding**

The 5-point pipeline section should be added to the `SKILL PHASES TO ENCODE IN TASK FILE` block in the BUILD_REQUEST, specifically:
- Under Phase 2: explicit mention of PRD Extraction Agent Prompt
- Under Phase 5: explicit mention of requirements traceability and metrics translation

These 5 changes require no architectural restructuring. They are prompt additions and table edits within the existing SKILL.md structure.

---

## Summary

### PRD Skill — What It Does and Outputs

The PRD skill is a 7-phase document creation pipeline producing a comprehensive product requirements document stored at `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md`. Research artifacts persist in `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/`. The final PRD contains 28 numbered sections plus appendices. The most TDD-relevant content:
- **S21.1** — Epics, Features & Stories (epics + user stories + acceptance criteria)
- **S21.2** — Product Requirements (RICE matrix with feature priorities)
- **S19** — Success Metrics & Measurement (KPI table with targets and measurement methods)
- **S14** — Technical Requirements (architecture, performance, security, scalability)
- **S12** — Scope Definition (in/out/deferred tables)

Phase 7 explicitly offers to invoke the TDD skill with the PRD as input.

### TDD Skill — What It Does and Outputs

The TDD skill is a structurally identical 7-phase pipeline producing a technical design document at `docs/[domain]/TDD_[COMPONENT-NAME].md`. It has a dedicated PRD input field (`PRD_REF`), a dedicated extraction artifact (`00-prd-extraction.md`), a `parent_doc` frontmatter field, and a "PRD-to-TDD Pipeline" reference section. The final TDD contains 28 numbered sections.

### PRD→TDD Handoff — Current State

**What works:** PRD is read in scope discovery, extracted to `00-prd-extraction.md` in Phase 2, listed as source for 4 of 9 synthesis files, and linked via `parent_doc`.

**What is missing:** No PRD extraction agent prompt template. 5 of 9 synthesis files don't read PRD content. No explicit AC→FR mapping instruction. No KPI translation instruction. The PRD-to-TDD Pipeline is reference documentation, not enforced.

---

## Gaps and Questions

1. [Critical] Does `00-prd-extraction.md` have a specified format that synthesis agents understand, or does each run produce a different structure depending on which agent invents the extraction?
2. [Critical] Is there an `rf-prd-extractor` agent definition, or is the extraction done by a generic Agent subagent with an ad-hoc prompt? The skill text says "first item extracts PRD context" without specifying the agent type.
3. [Important] When the PRD-to-TDD Pipeline says "every requirement in TDD S5 should trace back to a PRD epic or user story," who enforces this? Currently no QA gate checks it.
4. [Important] The rf-qa-qualitative agent prompt for the TDD is not provided in SKILL.md — it references "the agent definition." Does the agent definition check PRD traceability, or only general document quality?
5. [Minor] Should `synth-04-data-api.md` read PRD S21.1 user flows to ensure data models support all documented user interactions?
6. [Important] The PRD Phase 7 says "invoke the tdd skill with the PRD as input" — does this automatically set PRD_REF, or does the user need to manually provide the path in the TDD invocation?

---

## Key Takeaways

1. **The TDD skill has the right architecture for PRD consumption** — the `00-prd-extraction.md` file, `parent_doc` field, and PRD_CONTEXT in research notes create correct infrastructure. The gap is in enforcement depth, not structural design.

2. **The biggest single fix is adding a PRD Extraction Agent Prompt Template** — defining exactly what goes into `00-prd-extraction.md` (story IDs, ACs, KPI table, scope tables, RICE matrix) would immediately improve all downstream synthesis quality without restructuring the pipeline.

3. **The synthesis mapping table is the lowest-effort enforcement mechanism** — adding `00-prd-extraction.md` to the source files for synth-03 through synth-07 would route PRD content to the synthesis agents that currently don't see it, with zero structural change to the skill flow.

4. **PRD S21.1 (Epics/Stories/ACs) and S19 (Success Metrics/KPIs) are the most underconsumed sections** — these are the sections that most directly translate to TDD requirements and metrics, but the TDD synthesis mapping only routes them to synth-01 and synth-02.

5. **The PRD-to-TDD Pipeline reference section describes exactly the right behavior** — the 5-point pipeline (traceability, metrics alignment, scope inheritance, cross-referencing, parent_doc) is correct design intent. The work is encoding these 5 points into agent prompts and QA checklists rather than leaving them as documentation.

6. **The qualitative QA step (rf-qa-qualitative, Phase 6) is the last-resort enforcement point** — it currently checks "architecture decisions match PRD requirements" and "no requirements invented that aren't in the PRD." Strengthening this checklist to add explicit traceability checks would catch failures that slip through synthesis without restructuring earlier phases.

7. **Gap 1 (no extraction prompt) compounds all other gaps** — because without a defined extraction format, the quality of `00-prd-extraction.md` is inconsistent across runs, which means the 4 synthesis files that do read it may be working from inconsistently structured content.

