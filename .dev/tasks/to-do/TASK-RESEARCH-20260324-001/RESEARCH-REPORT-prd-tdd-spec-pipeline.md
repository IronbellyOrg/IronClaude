# Technical Research Report: IronClaude PRD/TDD/Spec Pipeline Architecture

**Date:** 2026-03-24
**Depth:** Deep
**Research files:** 6 codebase + 0 web research
**Scope:** .claude/commands/sc/, .claude/skills/sc-roadmap-protocol/, .claude/skills/sc-tasklist-protocol/, .claude/skills/prd/, .claude/skills/tdd/, src/superclaude/examples/

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Current State Analysis](#2-current-state-analysis)
3. [Target State](#3-target-state)
4. [Gap Analysis](#4-gap-analysis)
5. [External Research Findings](#5-external-research-findings)
6. [Options Analysis](#6-options-analysis)
7. [Recommendation](#7-recommendation)
8. [Implementation Plan](#8-implementation-plan)
9. [Open Questions](#9-open-questions)
10. [Evidence Trail](#10-evidence-trail)

---

## 1. Problem Statement

### 1.1 Original Research Question

The analysis document `.dev/analysis/spec-vs-prd-vs-tdd.md` was produced through conversation — not by tracing actual source files. It describes the current pipeline behavior, argues for three implementation options, and recommends Option 3 (modify TDD template AND upgrade sc:roadmap, sc:spec-panel, and sc:tasklist to actively consume the TDD's rich sections).

The research question: **verify every factual claim in that document against actual source files**, then produce a precise implementation plan for Option 3 that corrects any errors found.

### 1.2 Why This Verification Matters

The analysis document's implementation recommendations depend entirely on an accurate current-state model. Specifically:

- If a pipeline step is described as consuming a frontmatter field that it does not actually read, then any implementation plan that says "add that field to the TDD so the pipeline can use it" will silently fail.
- If a command is described as capable of a behavior it explicitly refuses to perform, then any plan that relies on that behavior will require new capability development, not configuration.
- If a flag is declared to exist but is unimplemented, then any plan that builds on that flag has a foundation that must be built before the plan can proceed.

Wrong assumptions in a current-state analysis propagate directly into wrong implementation scope estimates.

### 1.3 Contradictions Found in the Analysis Document

Research file 06 (`06-analysis-doc-verification.md`) cross-validated 19 substantive claims against findings from research files 01–05. Five claims were tagged [CODE-CONTRADICTED]:

| # | Contradicted Claim | What the Code Actually Shows |
|---|-------------------|------------------------------|
| 1 | "Path B: Created by /sc:spec-panel from raw instructions" | `sc:spec-panel` explicitly refuses this. Its `Boundaries > Will Not` section states: "Generate specifications from scratch without existing content or context." Path B as described does not exist. |
| 2 | "`spec_type` → feeds template type selection" | `spec_type` from spec YAML frontmatter is ignored by all sc:roadmap pipeline logic. Template type is always derived from computed domain distribution or the `--template` CLI flag. The field value is never read. |
| 3 | "`quality_scores` → pipeline quality signals" | `quality_scores` from input spec frontmatter is ignored by sc:roadmap. sc:spec-panel produces its own quality metrics under a different schema with no bridge. |
| 4 | "The frontmatter advantage is conditional — only exists when spec was manually created from template" | The pipeline ignores all spec frontmatter field values in all paths. The "conditional advantage" does not exist at the pipeline level. |
| 5 | spec-panel output format described as relatively unconstrained in Path B context | sc:spec-panel has three well-defined output format modes. Under `--focus correctness`, three artifact types are mandatory hard gates. |

These five contradictions affect the implementation plan: adding frontmatter fields to the TDD template requires simultaneous pipeline changes to be meaningful; sc:spec-panel's TDD-creation capability must be built from zero; Option 2 ("modify TDD template only") would produce no pipeline benefit without the same foundational changes Option 3 requires.

---

## 2. Current State Analysis

All findings are [CODE-VERIFIED] against actual source files. [CODE-CONTRADICTED] findings from the analysis document are called out explicitly.

---

### 2.1 sc:spec-panel

**Source:** `.claude/commands/sc/spec-panel.md` (624 lines) | **Research file:** `01-spec-panel-audit.md`

#### What It Does

Routes an existing specification through a fixed panel of 11 simulated domain experts (Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower — always in this order). Produces a structured review document, not a revised spec file.

| Format flag | Description |
|-------------|-------------|
| `--format standard` | YAML-structured review: `specification_review`, `quality_assessment`, `critical_issues`, `expert_consensus`, `improvement_roadmap`, `adversarial_analysis` |
| `--format structured` | Token-efficient format using SuperClaude symbol system |
| `--format detailed` | Full expert commentary, examples, and implementation guidance |

Under `--focus correctness`, three artifact types are mandatory hard gates blocking synthesis output if incomplete: State Variable Registry, Guard Condition Boundary Table, Pipeline Quantity Flow Diagram.

#### Explicit Boundaries

`Boundaries > Will Not` states verbatim: "Generate specifications from scratch without existing content or context." The command does not offer a creation mode. Usage syntax requires `[specification_content|@file]` as a required input parameter.

[CODE-CONTRADICTED] "Path B: Created by /sc:spec-panel from raw instructions" does not exist. This capability must be built from zero.

#### Template and Sentinel Knowledge

- Zero references to `release-spec-template.md`, `tdd_template.md`, `prd_template.md`, or any external template file path in the 624-line command.
- No awareness of the `{{SC_PLACEHOLDER:*}}` sentinel system. "Sentinel" appears 5 times; all occurrences refer to Whittaker's adversarial "Sentinel Collision Attack" (FR-2.3), not the SuperClaude template placeholder system.

#### Frontmatter Behavior

Does NOT read or write `spec_type`, `complexity_score`, `complexity_class`, or `quality_scores`. Produces its own quality metrics under a different schema:

| sc:spec-panel metric | Spec template field | Bridge exists? |
|----------------------|--------------------|----|
| `overall_score` (0-10) | `quality_scores.overall` | No |
| `requirements_quality` (0-10) | `quality_scores.completeness` | No |
| `architecture_clarity` (0-10) | (no equivalent field) | No |
| `testability_score` (0-10) | `quality_scores.testability` | No |

#### Downstream Wiring

| Wiring point | Target | Integration |
|--------------|--------|------------|
| RM-2 | `sc:roadmap` | SP-2 (Whittaker Assumptions) feeds assumption tracking |
| RM-3 | `sc:roadmap` | SP-4 (Quantity Flow Diagram) feeds risk-weighted prioritization |

No companion skill directory exists. Integration to `sc:tasklist` is not mentioned anywhere in the file.

---

### 2.2 sc:roadmap-protocol

**Source:** `.claude/skills/sc-roadmap-protocol/SKILL.md` + `refs/extraction-pipeline.md`, `refs/scoring.md`, `refs/templates.md`, `refs/validation.md`, `refs/adversarial-integration.md` | **Research file:** `02-roadmap-pipeline-audit.md`

#### YAML Frontmatter Behavior: Validate-Only

Wave 1B Step 1: "Parse specification file. If spec contains YAML frontmatter, **validate it parses correctly**. If malformed YAML, abort."

Validation-only. Field values within spec frontmatter are NOT consumed by any extraction step, scoring formula, or template selection algorithm.

[CODE-CONTRADICTED] The following spec frontmatter fields are ignored by all pipeline logic in all paths:
- `spec_type` — ignored; template type derived from computed domain distribution, never from this field
- `complexity_score` — ignored; always recomputed via 5-factor formula
- `complexity_class` — ignored; always derived from computed score
- `quality_scores` — ignored; no extraction step reads them

#### The 8-Step Extraction Pipeline

All steps operate on body text using keyword matching and pattern detection. No step reads YAML frontmatter field values.

| Step | Name | What It Extracts |
|------|------|-----------------|
| 1 | Title & Overview | `project_title`, `project_version`, `summary` from opening H1 / metadata / executive summary |
| 2 | Functional Requirements | Behavioral statements ("shall", "must", "will", "should"), user stories, ACs. Fields: `id`, `description`, `domain`, `priority` (P0-P3), `source_lines` |
| 3 | Non-Functional Requirements | Performance, security, scalability, reliability, maintainability constraints |
| 4 | Scope & Domain Classification | Keyword-weighted domain assignment into 5 domains: Frontend, Backend, Security, Performance, Documentation |
| 5 | Dependency Extraction | "requires", "depends on", "after", "before", "blocks" |
| 6 | Success Criteria | Explicit success criteria sections, ACs, KPIs, metrics |
| 7 | Risk Identification | Explicit risks + inferred risks from requirement complexity |
| 8 | ID Assignment | Deterministic IDs by `source_lines` position: `FR-{3digits}`, `NFR-{3digits}`, `DEP-{3digits}`, `SC-{3digits}`, `RISK-{3digits}` |

#### 5-Factor Complexity Scoring Formula

Always computed from extraction outputs. Never reads from spec frontmatter.

| Factor | Raw Value Source | Normalization | Weight |
|--------|-----------------|---------------|--------|
| `requirement_count` | Total FRs + NFRs | `min(count / 50, 1.0)` | 0.25 |
| `dependency_depth` | Max chain in dependency graph | `min(depth / 8, 1.0)` | 0.25 |
| `domain_spread` | Distinct domains with ≥10% representation | `min(domains / 5, 1.0)` | 0.20 |
| `risk_severity` | `(high*3 + medium*2 + low*1) / total_risks` | `(weighted_avg - 1.0) / 2.0` | 0.15 |
| `scope_size` | Total line count of specification | `min(lines / 1000, 1.0)` | 0.15 |

Classification thresholds: LOW < 0.4 → 3-4 milestones, 1:3 interleave; MEDIUM 0.4-0.7 → 5-7 milestones, 1:2 interleave; HIGH > 0.7 → 8-12 milestones, 1:1 interleave.

Template type is always derived from computed domain distribution (body-text keyword analysis), NOT from any frontmatter field.

#### TDD Section Capture Analysis

| TDD Section | Captured? | By Which Step | Notes |
|-------------|-----------|---------------|-------|
| §7 Data Models | Partial | Step 2 (behavioral only) | Structural entity definitions, field type tables missed |
| §8 API Specifications | Partial | Step 2 + Step 5 | Endpoint tables with no "shall" language missed |
| §9 State Management | Partial | Step 2 (behavioral only) | State machine diagrams, transition tables missed |
| §10 Component Inventory | Mostly No | Step 2 (behavioral only) | New/modified/deleted inventory lists missed entirely |
| §14 Observability & Monitoring | Partial | Step 2 + Step 3 | Metric definitions, alert thresholds as structured data missed |
| §15 Testing Strategy | Mostly No | Step 3 (coverage NFRs only) | Test strategy structure not captured |
| §19 Migration & Rollout | Partial | Step 2 + Step 5 | Phase plans, cutover steps as procedural content missed |
| §24 Release Criteria | YES | Step 6 (Success Criteria) | Directly targeted; the only TDD section fully captured |
| §25 Operational Readiness | NO | None | Entirely outside extraction scope |

#### Internal Inconsistency in extraction-pipeline.md

The worked example tags "Data Models" (Section 6, L581-L700) as `FR_BLOCK`. The stated heuristic defines `FR_BLOCK` as headings containing "requirement", "feature", "capability", or "functional" — none of which match "Data Models". Under the documented rules, "Data Models" would be tagged `OTHER` and de-prioritized. The same inconsistency applies to "Migration Plan" (tagged `FR_BLOCK` in the worked example but "migration" is not a `FR_BLOCK` heuristic keyword). The worked example contradicts the documented heuristic at both points.

#### Domain Keyword Gap

The 5 domain dictionaries are: Frontend, Backend, Security, Performance, Documentation. There is no Testing domain, no DevOps/Ops domain, no Data/ML domain. TDD sections §15 Testing Strategy and §25 Operational Readiness have no matching domain and will be systematically undercounted in complexity scoring.

---

### 2.3 sc:tasklist-protocol

**Source:** `.claude/skills/sc-tasklist-protocol/SKILL.md` + `rules/tier-classification.md` + `rules/file-emission-rules.md` + `templates/` | **Research file:** `03-tasklist-audit.md`

#### Input Contract

SKILL.md Input Contract (lines 47-57) states explicitly: "You receive exactly one input: **the roadmap text**. Treat the roadmap as the **only source of truth**."

| Input | Status |
|-------|--------|
| Roadmap text (primary) | Fully defined and processed |
| `--spec <spec-path>` | Listed in argument-hint frontmatter only; **zero body implementation** — no section, no conditional logic, no processing rule anywhere in SKILL.md |
| `--output <output-dir>` | Listed in argument-hint frontmatter only; **zero body implementation** |

TASKLIST_ROOT is computed from roadmap text only (not from `--output` flag):
1. If roadmap text contains `.dev/releases/current/<segment>/`: use that path
2. Else if roadmap text contains version token `v<digits>(.<digits>)+`: `TASKLIST_ROOT = .dev/releases/current/<version-token>/`
3. Else: `TASKLIST_ROOT = .dev/releases/current/v0.0-unknown/`

#### 11-Step Generation Algorithm (summary)

| Step | Name | Summary |
|------|------|---------|
| 4.1 | Parse Roadmap Items | Split at headings, bullets, numbered items; deterministic `R-NNN` IDs |
| 4.2 | Determine Phase Buckets | Explicit phase/milestone headings; fall back to `##` headings; default 3 phases |
| 4.3 | Fix Phase Numbering | Renumber all phases sequentially — no gaps preserved |
| 4.4 | Convert to Tasks | Default 1 task per roadmap item; split only for compound deliverables |
| 4.5 | Task ID and Ordering | `T<PP>.<TT>` zero-padded; dependencies reorder within phase only |
| 4.6 | Clarification Tasks | Insert before blocked task when tier confidence < 0.70 |
| 4.7 | Acceptance Criteria | Every task: 1-5 deliverables; 3-8 steps; exactly 4 AC bullets; exactly 2 validation bullets |
| 4.8 | Checkpoints | After every 5 tasks within a phase; mandatory at end of every phase |
| 4.9 | No Policy Forks | Deterministic tie-breakers; Tier conflict priority: STRICT > EXEMPT > LIGHT > STANDARD |
| 4.10 | Verification Routing | STRICT: sub-agent quality-engineer, 3-5K tokens, 60s; STANDARD: direct test; LIGHT: sanity check; EXEMPT: skip |
| 4.11 | Critical Path Override | Paths matching `auth/`, `security/`, `crypto/`, `models/`, `migrations/` always force CRITICAL verification |

#### TDD Section Usage by sc:tasklist

| TDD Section | Currently Used? | Actual Mechanism |
|-------------|----------------|------------------|
| §7 Data Models | Keyword matching only | "schema", "migration", "model", "database" boost STRICT tier |
| §8 API Specifications | Keyword matching only | "api contract", "query", "transaction" boost STRICT |
| §10 Component Inventory | Not at all | No structured handling |
| §15 Testing Strategy | Keyword matching only | "tests/" path boosts STANDARD |
| §19 Migration & Rollout | Partially (keywords + split rule) | "migration", "rollback", "deploy" boost STRICT/risk |
| §24 Release Criteria | Not at all | No structural extraction of release gates |

Post-generation validation (Stages 7-10) uses 2N parallel agents that validate against the roadmap only. No instructions exist to validate against a spec or TDD.

---

### 2.4 TDD Template

**Source:** `src/superclaude/examples/tdd_template.md` (1,309 lines, template version 1.2, last updated 2026-02-11) | **Research file:** `04-tdd-template-audit.md`

#### YAML Frontmatter: 27 Fields

| Field | Type/Format | Default/Placeholder |
|-------|-------------|---------------------|
| `id` | string | `"[COMPONENT-ID]-TDD"` |
| `title` | string | `"[Component Name] - Technical Design Document"` |
| `version` | string | `"1.2"` |
| `status` | string (emoji-prefixed) | `"🟡 Draft"` |
| `type` | string (emoji-prefixed) | `"📐 Technical Design Document"` |
| `priority` | string (emoji-prefixed) | `"🔥 Highest"` |
| `autogen` | boolean | `false` |
| `coordinator` | string | `"[tech-lead]"` |
| `parent_doc` | string | `"[link to Product PRD...]"` |
| `depends_on` | list | `["[list dependent documents/components]"]` |
| `tags` | list | `["technical-design-document", "[component-type]", "architecture", "specifications"]` |
| `estimation`, `sprint`, `due_date`, `start_date`, `completion_date`, `blocker_reason` | string | `""` (empty) |
| `review_info.last_reviewed_by/date/next_review_date` | string (×3) | `""` (empty) |
| `approvers.tech_lead/.engineering_manager/.architect/.security` | string (×4) | `""` (empty) |

#### Spec Template Fields Absent from TDD Template

| Field | In Spec Template | In TDD Template | Pipeline impact of absence |
|-------|-----------------|-----------------|---------------------------|
| `spec_type` | Yes (enum: 4 values) | No | sc:roadmap ignores even when present; adding requires pipeline upgrade |
| `complexity_score` | Yes (float 0.0-1.0) | No | sc:roadmap ignores even when present; always recomputes |
| `complexity_class` | Yes (enum LOW/MEDIUM/HIGH) | No | sc:roadmap ignores even when present; always derives from score |
| `quality_scores` (×5 sub-fields) | Yes | No | sc:roadmap ignores; sc:spec-panel uses different schema |

#### All 28 Numbered TDD Sections

| # | Title | Content Type | Conditional? |
|---|-------|-------------|--------------|
| 1 | Executive Summary | Narrative + Key Deliverables list | No |
| 2 | Problem Statement & Context | Background, problem, business context, PRD reference | No |
| 3 | Goals & Non-Goals | Goal/non-goal/future tables | No |
| 4 | Success Metrics | Technical + business KPI tables | 4.2 conditional |
| 5 | Technical Requirements | FR table; NFR sub-tables | No |
| 6 | Architecture | Mermaid/ASCII diagrams, boundary table, design decisions | 6.5 conditional |
| 7 | Data Models | TypeScript interfaces + field tables, Mermaid flowchart, storage table | No |
| 8 | API Specifications | Endpoint tables, request/response, error format, versioning policy | No |
| 9 | State Management | State tool table, TS state interfaces, transition table | Frontend-only conditional |
| 10 | Component Inventory | Route table, component table, hierarchy ASCII tree | Frontend-only conditional |
| 11 | User Flows & Interactions | Mermaid sequence diagrams, step lists, success criteria, error scenarios | No |
| 12 | Error Handling & Edge Cases | Error category table, edge case table, degradation table, retry table | No |
| 13 | Security Considerations | Threat table, controls table, data classification table | 13.4 conditional |
| 14 | Observability & Monitoring | Log table, metrics table, trace spans, alert table, dashboard links | 14.6 conditional |
| 15 | Testing Strategy | Test pyramid table, unit/integration/E2E test case tables | No |
| 16 | Accessibility Requirements | WCAG 2.1 AA requirements table | No |
| 17 | Performance Budgets | Core Web Vitals/bundle table, API latency table, load test plan | No |
| 18 | Dependencies | External/internal/infrastructure tables | No |
| 19 | Migration & Rollout Plan | Migration phase table, feature flag table, rollout stage table, rollback steps | No |
| 20 | Risks & Mitigations | Risk table: ID/description/probability/impact/mitigation/contingency | No |
| 21 | Alternatives Considered | Alt 0 (Do Nothing, mandatory) + alternatives | No |
| 22 | Open Questions | Table: ID/question/owner/target date/status/resolution | No |
| 23 | Timeline & Milestones | Milestone table, phase deliverables checklists | No |
| 24 | Release Criteria | 13-item Definition of Done checklist, 9-item release checklist | No |
| 25 | Operational Readiness | Runbook scenario table, on-call table, capacity projection table | No |
| 26 | Cost & Resource Estimation | Cost table, scaling model table | Conditional |
| 27 | References & Resources | Related doc table, external reference table | No |
| 28 | Glossary | Term/definition table | No |

---

### 2.5 PRD and TDD Skills

**Source:** `.claude/skills/prd/SKILL.md` (1,373 lines), `.claude/skills/tdd/SKILL.md` (1,344 lines) | **Research file:** `05-prd-tdd-skills-audit.md`

#### PRD Skill: 7-Phase Pipeline

Final PRD output path: `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md`

| Phase | Name | Key Activity |
|-------|------|-------------|
| 1 | Preparation | Status update, scope confirmation, template read, tier selection, folder creation |
| 2 | Deep Investigation | Parallel subagents: Feature Analyst, Doc Analyst, Integration Mapper, UX Investigator, Architecture Analyst — write to `${TASK_DIR}research/` |
| 3 | Completeness Verification | rf-analyst + rf-qa in parallel; PASS/FAIL gate blocks progression |
| 4 | Web Research | Competitive landscape, market sizing, industry standards, tech trends |
| 5 | Synthesis + QA Gate | Parallel synthesis agents (one per synth file, 9 total); rf-analyst + rf-qa synthesis gate in parallel |
| 6 | Assembly & Validation | rf-assembler → rf-qa report-validation → rf-qa-qualitative |
| 7 | Present to User & Complete | Offers downstream TDD creation: "Would you like me to create a TDD using the `/tdd` skill?" |

The two synthesis files most directly relevant to TDD handoff: `synth-04-stories-requirements.md` (S21.1 Epics/Stories/ACs, S21.2 Product Requirements RICE matrix) and `synth-07-metrics-risk-impl.md` (S19 Success Metrics, S21.3-21.5 Phasing/Release Criteria/Timeline).

#### TDD Skill: PRD_REF Field

`PRD_REF` is one of four input fields captured at Step A.2 (Parse & Triage). When provided, the sufficiency gate (A.5 item 7) is a mandatory gate: if PRD_CONTEXT is empty when a PRD was provided, scope discovery must be redone.

The `00-prd-extraction.md` artifact is created in Phase 2 before all parallel research agents begin. However, no named PRD Extraction Agent Prompt template exists anywhere in TDD SKILL.md (Gap 1).

#### PRD-to-TDD Coverage by Synthesis File

4 of 9 synthesis files read `00-prd-extraction.md`:

| Synth File | TDD Sections Covered |
|------------|---------------------|
| `synth-01-exec-problem-goals.md` | S1 Executive Summary, S2 Problem Statement, S3 Goals & Non-Goals, S4 Success Metrics |
| `synth-02-requirements.md` | S5 Technical Requirements |
| `synth-08-perf-deps-migration.md` | S16 Accessibility, S17 Performance, S18 Dependencies, S19 Migration |
| `synth-09-risks-alternatives-ops.md` | S20 Risks, S21 Alternatives, S22 Open Questions, S23 Timeline, S24 Release, S25 Ops, S26 Cost |

5 of 9 synthesis files do NOT read `00-prd-extraction.md` (synth-03 through synth-07): Architecture, Data Models, API Specs, User Flows, Error Handling, Security, Observability, and Testing are produced without seeing PRD acceptance criteria.

#### 6 PRD-to-TDD Handoff Gaps

| Gap # | Description | Evidence Location |
|-------|-------------|-------------------|
| Gap 1 | No PRD extraction agent prompt template defined. Phase 2 instructs creation of `00-prd-extraction.md` but no named agent prompt template exists. | TDD SKILL.md Phase 2; absence confirmed across all 8 named agent prompt templates |
| Gap 2 | 5 of 9 synthesis files do not list PRD extraction as a source. Architecture, Data Models, API Specs, User Flows, Error Handling, Security, and Testing produced without PRD ACs. | TDD SKILL.md Phase 5 Synthesis Mapping Table |
| Gap 3 | No explicit AC-to-FR mapping instruction. No rule requiring traceability matrices or PRD story ID labeling on requirements. | TDD SKILL.md Synthesis Agent Prompt rule set |
| Gap 4 | PRD acceptance criteria not explicitly ported to TDD functional requirements. QA Synthesis Gate checklist (12 items) does not check PRD traceability. | TDD SKILL.md synth-02 instructions; QA Synthesis Gate checklist |
| Gap 5 | No KPI translation instruction. synth-01 lists PRD extraction as source for S4 but no synthesis rule instructs "translate PRD KPIs into engineering proxy metrics." rf-qa-qualitative does not check metric alignment. | TDD SKILL.md synth-01 instructions |
| Gap 6 | PRD-to-TDD Pipeline section (lines 1315-1326) is reference documentation, not enforced. Its 5-point pipeline is not in BUILD_REQUEST, synthesis prompts, or any QA gate checklist. | TDD SKILL.md lines 1315-1326 |

---

### 2.6 Current State Summary (Pipeline Diagram)

```
User Input
    │
    ├── /prd (.claude/skills/prd/SKILL.md, 1373 lines)
    │       Output: docs/docs-product/tech/[name]/PRD_[NAME].md
    │       Phase 7: manually offers TDD creation to user (user must respond)
    │
    ├── /tdd (.claude/skills/tdd/SKILL.md, 1344 lines)
    │       Accepts: feature description + optional PRD_REF
    │       If PRD_REF:
    │         - Phase 2: creates ${TASK_DIR}research/00-prd-extraction.md (no agent prompt template)
    │         - 4/9 synthesis files read PRD extraction
    │         - 5/9 synthesis files do NOT read PRD extraction (synth-03 through synth-07)
    │         - PRD-to-TDD Pipeline section (lines 1315-1326): unenforced reference docs
    │       Output: docs/[domain]/TDD_[COMPONENT-NAME].md
    │               27 frontmatter fields, 28 sections
    │               0 pipeline-oriented fields shared with spec template
    │
    ├── /sc:spec-panel (.claude/commands/sc/spec-panel.md, 624 lines, no skill dir)
    │       Accepts: existing spec as required input (CANNOT create from scratch)
    │       No template awareness, no sentinel awareness
    │       Output: structured review document (3 format modes)
    │       Wires to sc:roadmap at RM-2, RM-3 only
    │
    └── /sc:roadmap (.claude/skills/sc-roadmap-protocol/)
            Wave 1B: validates YAML parses; field values ignored
            8-step extraction: behavioral text only, modal verbs + heading keywords
            5-factor scoring: always from scratch (ignores frontmatter)
            Template type: from domain distribution keyword analysis (NOT spec_type field)
            Domain dictionaries: 5 domains (no Testing, no DevOps/Ops, no Data/ML)
            TDD coverage: §24 Release Criteria fully; 6 sections partial; §15 §25 not captured
            Output: roadmap.md, extraction.md, test-strategy.md
            │
            └── /sc:tasklist (.claude/skills/sc-tasklist-protocol/)
                    Accepts: roadmap text only
                    --spec flag: declared in argument-hint, ZERO implementation
                    --output flag: declared in argument-hint, ZERO implementation
                    TASKLIST_ROOT: computed from roadmap text, never from --output
                    11-step algorithm: heading/bullet parsing, no TDD section semantics
                    Validation loop: validates against roadmap only, not spec
                    Output: tasklist-index.md + phase-N-tasklist.md files
```

| Component | Verified Fact | Source |
|-----------|--------------|--------|
| sc:spec-panel | Cannot create specs from scratch (explicit Boundaries Will Not) | `01-spec-panel-audit.md` §3.5 |
| sc:spec-panel | Zero template/sentinel file references in 624 lines | `01-spec-panel-audit.md` §3.1, §3.3 |
| sc:roadmap | Frontmatter field values ignored in all paths (validate-only) | `02-roadmap-pipeline-audit.md` §1, §3, §4 |
| sc:roadmap | Template type from domain keyword analysis, not `spec_type` | `02-roadmap-pipeline-audit.md` §4 |
| sc:roadmap | §24 Release Criteria is the only TDD section fully captured | `02-roadmap-pipeline-audit.md` §2 |
| sc:roadmap | Worked example in extraction-pipeline.md contradicts documented heuristic | `02-roadmap-pipeline-audit.md` §2 |
| sc:tasklist | `--spec` flag declared in argument-hint only; zero body implementation | `03-tasklist-audit.md` §1, §8 |
| sc:tasklist | TASKLIST_ROOT derived from roadmap text; `--output` flag unimplemented | `03-tasklist-audit.md` §4 |
| TDD template | 27 frontmatter fields; none of the spec's pipeline-oriented fields present | `04-tdd-template-audit.md` §1.1 |
| TDD skill | 5 of 9 synthesis files do not read PRD extraction | `05-prd-tdd-skills-audit.md` §2.7, Gap 2 |
| TDD skill | PRD-to-TDD Pipeline section (lines 1315-1326) is unenforced | `05-prd-tdd-skills-audit.md` §2.8, Gap 6 |

---

## 3. Target State

### 3.1 What Option 3 Must Achieve

Option 3 upgrades the TDD template and the pipeline tools (sc:roadmap, sc:tasklist, sc:spec-panel) to actively consume TDD structure. The desired end state: a TDD produced from a PRD flows into sc:roadmap, which extracts rich structured content and generates a high-fidelity roadmap, which flows into sc:tasklist to generate richer, more specific tasks than are possible today.

### 3.2 Desired Behaviors

| Behavior | Description |
|----------|-------------|
| TDD → sc:roadmap pipeline works | A TDD file passed to sc:roadmap produces a roadmap with structured extraction from TDD-specific sections, not just behavioral "shall/must" statements |
| sc:roadmap uses TDD's rich sections | Extraction pipeline reads and uses structured content from §7 (Data Models), §8 (API Specs), §10 (Component Inventory), §14 (Observability), §15 (Testing Strategy), §19 (Migration), §24 (Release Criteria), §25 (Operational Readiness) |
| sc:tasklist generates richer tasks from TDD sections | When a roadmap was generated from a TDD, sc:tasklist uses TDD section content to populate task Validation fields (from §15 test cases), Rollback fields (from §19 rollback procedures), and acceptance criteria specificity (from §8 endpoint tables, §7 entity definitions, §10 component lists) |
| PRD → TDD handoff is complete | The TDD skill's PRD extraction step has a defined agent prompt, all 9 synthesis files read `00-prd-extraction.md`, and FR traceability and KPI translation are enforced by a QA gate |

### 3.3 Success Criteria

All criteria are [CODE-VERIFIED] against current pipeline behavior as the measurable delta Option 3 must close.

| # | Success Criterion | How Measured | Baseline (Current) |
|---|-------------------|--------------|--------------------|
| SC-01 | sc:roadmap extracts structured content from §7, §8, §10, §14, §15, §19, §24, and §25 when given a TDD input | extraction.md contains domain-classified requirements sourced from each named section | Only §24 fully captured; §7, §8, §9, §14, §19 partially; §10, §15, §25 not captured |
| SC-02 | Domain dictionaries include Testing and DevOps/Ops/Observability domains | extraction.md domain_distribution shows >0% for Testing and Ops domains on a TDD input | 5 domains only: Frontend, Backend, Security, Performance, Documentation; no Testing or Ops |
| SC-03 | sc:roadmap extracts component inventory tables from §10 | extraction.md contains at least one FR or structured item per row in the §10 component table | §10 content extracted only if phrased as behavioral requirements |
| SC-04 | sc:tasklist --spec flag is implemented and processes TDD content | Passing `--spec <tdd-path>` produces task Validation fields populated from TDD §15 test cases | `--spec` flag declared in argument-hint but completely unimplemented |
| SC-05 | sc:tasklist Rollback fields populated from TDD §19 rollback procedures | Rollback field contains content derived from §19.4 rather than defaulting to "TBD" | All Rollback fields default to "TBD" when not stated in roadmap prose |
| SC-06 | PRD → TDD extraction has a defined agent prompt template | `00-prd-extraction.md` produced by a specified agent with a defined prompt | No PRD extraction agent prompt template defined |
| SC-07 | All 9 TDD synthesis files read 00-prd-extraction.md | Each synth-NN file lists `00-prd-extraction.md` in its source list | Only 4 of 9 synthesis files read the PRD extraction |
| SC-08 | FR traceability from PRD is enforced by QA gate | QA gate checklist includes: "every FR in §5 traces to a PRD epic or user story" | No QA gate checks PRD traceability |
| SC-09 | `spec_type`, `complexity_score`, `complexity_class`, `quality_scores` fields in TDD frontmatter consumed by sc:roadmap | extraction.md reflects values from TDD frontmatter for these fields | sc:roadmap ignores all input spec frontmatter field values; validates YAML syntax only |
| SC-10 | Spec template remains usable for simple releases without TDD | A spec without TDD input produces a valid roadmap via the existing 8-step extraction pipeline | Backward compatibility constraint; existing pipeline must not require TDD |
| SC-11 | sc:spec-panel can produce a spec-template-formatted output from a TDD input | Invoking sc:spec-panel with a TDD produces a document with YAML frontmatter compatible with sc:roadmap | sc:spec-panel has no knowledge of release-spec-template.md; cannot produce pipeline-compatible YAML frontmatter |

### 3.4 Constraints

| Constraint | Rationale | Source |
|------------|-----------|--------|
| Spec template must remain usable for simple releases | Not all releases have TDDs; sc:roadmap must continue to accept spec-format inputs | Backward compatibility requirement |
| Existing pipeline tools must remain backward compatible with spec inputs | sc:roadmap's 8-step extraction pipeline must not be removed or made TDD-dependent | The 8-step pipeline is correct and complete for spec inputs |
| Adding frontmatter fields to TDD without pipeline changes produces zero benefit | sc:roadmap ignores all input frontmatter field values; adding spec_type, complexity_score, etc. to TDD frontmatter has no effect until pipeline is upgraded to read them | [CODE-VERIFIED] file 02 Summary, file 06 B1/B3 |
| sc:tasklist --spec flag implementation must not change the skill's external argument signature | The flag is already declared in the argument-hint; implementation must match the declared interface | [CODE-VERIFIED] file 03 Section 1 |

---

## 4. Gap Analysis

All gaps are confirmed against verified code findings. Severity: **Critical** = blocks Option 3 entirely; **High** = degrades output quality significantly; **Medium** = reduces fidelity or specificity; **Low** = informational or minor.

### 4.1 TDD Frontmatter Gaps

| Gap | Current State | Target State | Severity | Notes |
|-----|---------------|--------------|----------|-------|
| `feature_id` missing | TDD has no `feature_id` field | TDD frontmatter contains `feature_id` for pipeline feature-request linkage | Medium | sc:roadmap does not currently read `feature_id` from frontmatter, but linkage is needed for downstream artifact correlation |
| `spec_type` missing | TDD has no `spec_type` field | TDD frontmatter contains `spec_type` enum | Low | **Adding `spec_type` creates no pipeline value without simultaneous sc:roadmap upgrade.** sc:roadmap always derives type from body-text domain keyword analysis; it never reads `spec_type` from frontmatter. [CODE-VERIFIED: file 02 Section 4] |
| `complexity_score` missing | TDD has no `complexity_score` field | TDD frontmatter contains `complexity_score` | Low | **Adding `complexity_score` creates no pipeline value without simultaneous sc:roadmap upgrade.** sc:roadmap always computes complexity from scratch via 5-factor formula. [CODE-VERIFIED: file 02 Section 3] |
| `complexity_class` missing | TDD has no `complexity_class` field | TDD frontmatter contains `complexity_class` | Low | **Adding `complexity_class` creates no pipeline value without simultaneous sc:roadmap upgrade.** Derived from computed complexity_score, never read from frontmatter. [CODE-VERIFIED: file 02 Section 3] |
| `target_release` missing | TDD has `sprint` (empty) and `due_date` (empty) but no `target_release` version string | TDD frontmatter contains `target_release` version string | Medium | TDD spreads release targeting across `sprint` + `due_date` with different semantics than the spec template's version string |
| `quality_scores` missing | TDD has no `quality_scores` block | TDD frontmatter contains `quality_scores` block | Low | **Adding `quality_scores` creates no pipeline value without simultaneous sc:roadmap upgrade.** sc:roadmap ignores this field entirely; sc:spec-panel uses a different schema and does not write back to YAML frontmatter. [CODE-VERIFIED: file 02 Summary] |

### 4.2 sc:roadmap Extraction Gaps

| Gap | Current State | Target State | Severity | Notes |
|-----|---------------|--------------|----------|-------|
| No Testing domain in domain dictionaries | Domains: Frontend, Backend, Security, Performance, Documentation only | Testing domain with keywords: "unit test", "integration test", "e2e", "coverage", "test suite", "assertion", "mock", "fixture" | Critical | TDD §15 and §25 have no matching domain; systematically misclassified, understating complexity for TDD-heavy specs. [CODE-VERIFIED: file 02 "Domain Keyword Gap"] |
| No DevOps/Ops/Observability domain | Same 5-domain limitation | DevOps/Ops/Observability domain with "observability", "monitoring", "metrics", "dashboards", "alerts", "runbook", "on-call", "SRE" | Critical | TDD §14 and §25 content entirely outside extraction domain scope. [CODE-VERIFIED: file 02 Section 2 §14 analysis] |
| §7 Data Models: only behavioral statements captured | Step 2 captures "shall/must/will/should" within §7; entity definitions as TypeScript interfaces or field tables with no behavioral language tagged OTHER and not extracted | §7 entity definitions, field types, and relationship data extracted as structured items | High | TDD §7 uses TypeScript interfaces + field tables — the structured format the pipeline cannot read. [CODE-VERIFIED: file 02 Section 2 §7] |
| §8 API Specifications: only behavioral statements captured | Behavioral API requirements captured; endpoint tables (method, path, request body, response schema) with no behavioral language not extracted | §8 endpoint tables extracted as structured API spec items | High | TDD §8 has endpoint tables, request/response examples, versioning policy — all structured content invisible to the current extractor. [CODE-VERIFIED: file 02 Section 2 §8] |
| §9 State Management: only behavioral statements captured | Step 2 captures behavioral state requirements; state machine diagrams and transition tables as structured content not extracted | §9 state transition tables extracted | Medium | TDD §9 is conditional (frontend only); state transition tables are structured content the extractor cannot reach. [CODE-VERIFIED: file 02 Section 2 §9] |
| §10 Component Inventory: not captured at all | Heading tagged OTHER; inventory tables not targeted by any extraction step | §10 component inventory rows extracted: new → create task, modified → update task, deleted → remove + migration task | Critical | Component inventory is one of the highest-value TDD sections for task generation; none of it reaches the extraction pipeline in structured form. [CODE-VERIFIED: file 02 Section 2 §10] |
| §14 Observability: not captured structurally | No domain keyword dict includes "observability", "monitoring", "dashboards", "alerts"; metric definitions, alert thresholds, dashboard specs as structured tables not extracted | §14 metric tables, alert tables, and dashboard specs extracted | High | TDD §14 has 6 subsections with full structured tables; none is targeted by the extraction pipeline. [CODE-VERIFIED: file 02 Section 2 §14] |
| §15 Testing Strategy: mostly not captured | Step 3 picks up coverage NFRs only; test case tables, test pyramid breakdown, environment table not extracted | §15 test case tables extracted and wired to sc:tasklist Validation fields | High | TDD §15 has unit/integration/E2E test case tables — precisely the content needed to populate sc:tasklist Validation fields with verbatim commands. [CODE-VERIFIED: file 02 Section 2 §15] |
| §19 Migration Plan: sequential ordering not used | Migration behavioral requirements captured by Step 2; cutover phase sequences and rollout stage tables not captured; worked example inconsistency on FR_BLOCK tagging | §19 rollout stage tables extracted as ordered phase items; rollback procedures wired to sc:tasklist Rollback fields | Medium | Behavioral language captured; structured rollout stages and rollback procedures (§19.4) missed. Heuristic inconsistency between worked example and stated rules. [CODE-VERIFIED: file 02 Section 2 §19] |
| §25 Operational Readiness: not captured at all | Heading tagged OTHER; runbooks, on-call procedures, capacity planning tables entirely outside extraction scope | §25 runbook scenarios and on-call procedures extracted as post-launch phase items | High | Runbooks and on-call tables in §25 are structured operational content; no extraction step targets them and no domain keyword matches. [CODE-VERIFIED: file 02 Section 2 §25] |

### 4.3 sc:tasklist Gaps

| Gap | Current State | Target State | Severity | Notes |
|-----|---------------|--------------|----------|-------|
| `--spec` flag declared but completely unimplemented | Appears in SKILL.md `argument-hint` only; no body section, no conditional logic, no processing rule exists anywhere in SKILL.md for this flag | `--spec` flag fully implemented: reads TDD content, enriches task Validation fields from §15, Rollback fields from §19, acceptance criteria from §7 and §8 | Critical | This is the primary extension point for TDD-aware task generation. The declared interface is the correct hook; the implementation is entirely missing. [CODE-VERIFIED: file 03 Section 1] |
| No structured extraction from any TDD section | Skill processes roadmap text as opaque bullets and headings; §7 entity tables, §8 endpoint tables, §10 component inventories, §15 test cases, §19 rollback procedures all flattened to generic roadmap items | Structured extraction from named TDD sections drives specific field population (Validation, Rollback, Deliverables, acceptance criteria) | Critical | The "non-invention constraint" in Step 4.7 currently prevents writing specific ACs unless the named artifact is in the roadmap. TDD structured tables contain exactly this specificity but cannot be accessed. [CODE-VERIFIED: file 03 Section 3] |
| Validation pipeline validates against roadmap only | Stages 7–10 spawn 2N parallel agents to check generated tasks against the source roadmap only; no instructions to validate against spec/TDD content | Validation pipeline (Stages 7–10) checks generated tasks against both roadmap and TDD spec when `--spec` flag is provided | High | A TDD-enriched tasklist could contain content derived from TDD sections not present in the roadmap; the current validation loop would flag this as "invented content" drift. [CODE-VERIFIED: file 03 Section 9] |

### 4.4 sc:spec-panel Gaps

| Gap | Current State | Target State | Severity | Notes |
|-----|---------------|--------------|----------|-------|
| Zero knowledge of release-spec-template.md | 624-line command file contains zero references to any template file by path; treats all input as opaque text | sc:spec-panel detects TDD format and produces review output mapped to release-spec-template.md section structure | High | No template awareness exists. Adding TDD detection and template-mapped output requires new implementation, not configuration of existing behavior. [CODE-VERIFIED: file 06 A1] |
| Cannot create specs from raw instructions | Boundaries explicitly states "Will Not: Generate specifications from scratch without existing content or context"; Path B as described does not exist | sc:spec-panel can produce a pipeline-compatible spec from raw instructions or a TDD input | Critical | The analysis document's "Path B" is a [CODE-CONTRADICTED] claim. This capability must be built, not wired. [CODE-VERIFIED: file 06 A3, Corrections List item 1] |
| Output format does not produce pipeline-compatible YAML frontmatter | Primary output is a structured review document (3 defined formats); not a spec file, does not contain the YAML block required by sc:roadmap | sc:spec-panel optionally produces a spec file with release-spec-template.md-compatible YAML frontmatter | High | spec-panel produces its own quality metric schema that does not write back to the spec YAML `quality_scores` field. No bridge between the two schemas exists. [CODE-VERIFIED: file 06 A4, B3] |

### 4.5 PRD → TDD Handoff Gaps

| Gap | Current State | Target State | Severity | Notes |
|-----|---------------|--------------|----------|-------|
| No PRD extraction agent prompt template | TDD skill instructs creation of `00-prd-extraction.md` but does not specify agent type, prompt structure, or output format | A defined `rf-prd-extractor` agent (or equivalent prompt template) with a specified output schema for `00-prd-extraction.md` | Critical | If synthesis agents consume a differently-structured `00-prd-extraction.md` each run, PRD traceability is unreliable. [CODE-VERIFIED: file 06 E3] |
| 5 of 9 synthesis files do not read 00-prd-extraction.md | Only 4 of 9 TDD synthesis files list `00-prd-extraction.md` as a source; synth-03 through synth-07 do not | All 9 synthesis files list `00-prd-extraction.md` as a source | High | PRD traceability fails for any TDD section produced by a synthesis file that does not read the PRD extraction. [CODE-VERIFIED: file 06 E3] |
| No FR traceability instruction in synthesis prompts | No synthesis file prompt contains an instruction to map TDD FRs to PRD epics or user stories | Synthesis prompts for §5 (Technical Requirements) explicitly instruct: "for each FR in this section, identify the PRD epic or user story from 00-prd-extraction.md it implements" | High | Without an explicit traceability instruction, FR coverage of PRD requirements is incidental rather than enforced. [CODE-VERIFIED: file 06 E3 gap 3] |
| No KPI translation instruction | No synthesis file prompt instructs how to translate PRD business KPIs into technical success metrics | Synthesis prompts for §4 (Success Metrics) explicitly instruct: "translate each PRD KPI from 00-prd-extraction.md into a measurable technical metric" | Medium | PRD KPIs and TDD technical metrics may be produced independently without documented mapping. [CODE-VERIFIED: file 06 E3 gap 5] |

### 4.6 Analysis Document Correctness Gaps

Claims in `.dev/analysis/spec-vs-prd-vs-tdd.md` directly contradicted by code evidence:

| Claim in Analysis Doc | What Code Actually Shows | Severity |
|-----------------------|--------------------------|----------|
| "`spec_type` → feeds template type selection" | `spec_type` from input spec YAML frontmatter is ignored by all pipeline logic; template type always derived from computed domain distribution | Critical [CODE-CONTRADICTED: file 06 B1; file 02 Section 4] |
| "`quality_scores` → pipeline quality signals" | `quality_scores` from input spec frontmatter is ignored by sc:roadmap; sc:spec-panel uses a different schema and does not write back to YAML frontmatter | Critical [CODE-CONTRADICTED: file 06 B3; file 02 Summary] |
| "Path B: Created by /sc:spec-panel from raw instructions" | spec-panel explicitly refuses to generate specifications from scratch; Boundaries states "Will Not: Generate specifications from scratch without existing content or context" | Critical [CODE-CONTRADICTED: file 06 A3, Corrections List item 1] |
| "Conditional frontmatter advantage" (implies pipeline uses frontmatter when present) | The pipeline ignores ALL spec frontmatter field values in ALL cases; even a fully-populated Path A spec produces identical pipeline behavior to absent frontmatter | High [CODE-CONTRADICTED: file 06 B4; file 02 Summary] |
| spec-panel output format described as open-ended or expert-determined | sc:spec-panel has 3 well-defined output format modes (standard/structured/detailed) hard-coded in Behavioral Flow and Output sections; determined by caller's flag, not panel consensus | Medium [CODE-CONTRADICTED: file 06 agent 06 finding; file 01 Section 3.6] |

---

## 5. External Research Findings

**N/A — Codebase-scoped investigation.**

This investigation was scoped entirely to verification of existing source files in the IronClaude repository. No external competitive analysis, standards research, or industry benchmarking was required or performed. All research files (01–06) are code-tracer audits of specific pipeline components. No `web-NN` research files were produced during Phase 4.

If future work requires external research (e.g., evaluating alternative extraction pipeline architectures, reviewing industry standards for spec-to-task pipelines), that research should be added as a separate investigation and this section updated.

---

## 6. Options Analysis

Three approaches for achieving TDD-to-pipeline compatibility. All evidence references are to the research files in this task directory.

### Option 1: Status Quo (No Changes)

Continue using `release-spec-template.md` manually to author specs. The TDD template exists as a standalone engineering artifact with no integration into sc:roadmap, sc:tasklist, or sc:spec-panel.

| Criterion | Assessment |
|-----------|------------|
| Effort | None |
| Risk | None — no changes, no regressions |
| Maintainability | Low — two parallel document families with no shared source of truth |
| Data richness | Low — TDD's §10, §14, §15, §19 content invisible to all pipeline tools |
| Single source of truth | No |

**Pros:** No disruption, no migration risk, no implementation cost.

**Cons:** The TDD's rich structured content produces no pipeline benefit. The five confirmed analysis-document errors persist indefinitely. The `--spec` flag in sc:tasklist remains a declared-but-dead interface.

---

### Option 2: Create a Spec-Generator Step from TDD

Wire sc:spec-panel to accept a TDD as input and output a `release-spec-template.md`-formatted spec scoped to a single release increment. The resulting spec feeds the existing sc:roadmap and sc:tasklist pipeline unchanged.

| Criterion | Assessment |
|-----------|------------|
| Effort | Medium — sc:spec-panel command file must be edited; TDD-detection logic must be added |
| Risk | Medium — spec-panel Boundaries constraint creates an ambiguous interpretation edge |
| Maintainability | Low — spec is derived but not live; TDD changes require re-running spec generation manually |
| Data richness | Low-to-medium — derived spec shallower than TDD; structured tables prose-converted |
| Single source of truth | No |

**Pros:** Minimal pipeline changes. Only one file requires modification. Existing sc:roadmap and sc:tasklist tools untouched.

**Cons:** sc:spec-panel's `Boundaries > Will Not` explicitly states "Generate specifications from scratch without existing content or context." Working around this requires a semantic stretch or a partial Option 3 implementation anyway. Confirmed research finding: frontmatter fields in any spec are ignored by sc:roadmap, so the derived spec's frontmatter provides no incremental benefit without pipeline changes. The `--spec` flag in sc:tasklist remains unimplemented.

---

### Option 3: Modify TDD Template + Upgrade Pipeline Tools

Add pipeline frontmatter to the TDD template to make TDDs self-describing. Simultaneously upgrade sc:roadmap's extraction pipeline to natively consume TDD-specific sections. Upgrade sc:tasklist to implement the declared `--spec` flag. Upgrade sc:spec-panel to accept TDD as input and produce scoped release specs. Fix the PRD→TDD handoff gaps in `tdd/SKILL.md`. All changes backward-compatible with existing spec-template-based inputs.

| Criterion | Assessment |
|-----------|------------|
| Effort | High — 6 files modified across 4 tools; new extraction steps; new scoring factors; skill body sections |
| Risk | Medium — bounded scope; each upgrade is additive; existing spec-template pipeline paths unchanged; highest risk is sc:roadmap scoring formula rebalancing |
| Maintainability | High — TDD becomes the single upstream source; pipeline tools read richer content natively |
| Integration complexity | Medium — extraction pipeline, scoring formula, spec-panel behavioral flow, tasklist skill body, tdd skill synthesis mapping all require coordinated changes |
| Reuse potential | High — builds on existing hooks (`--spec` already declared, `00-prd-extraction.md` slot exists) |
| Data richness | High — sc:roadmap extraction gains §10, §19, §24, §14; sc:tasklist task generation driven by component inventory, migration phases, testing strategy, release criteria |
| Single source of truth | Yes |

**Pros:** Single source of truth. Richer roadmaps. Richer tasklists with one task per new component, migration-phase-ordered task buckets, verbatim validation commands from testing strategy, DoD items as final-phase verification tasks. PRD→TDD traceability enforced at the QA gate level.

**Cons:** Significant scope — 4 tools require changes across 6 files. Requires thorough testing to verify scoring formula weights sum to 1.0 and backward-compatible extraction path remains stable.

---

### Options Comparison Table

| Criterion | Option 1: Status Quo | Option 2: Spec-Generator Step | Option 3: TDD Template + Pipeline Upgrade |
|-----------|---------------------|-------------------------------|------------------------------------------|
| Effort | None | Medium (1 file) | High (6 files, 4 tools) |
| Risk | None | Medium — Boundaries workaround required | Medium — bounded, backward-compatible |
| Maintainability | Low — two orphaned document families | Low — spec is a manual re-derivation | High — single upstream source |
| Integration complexity | None | Low — pipeline unchanged | Medium — coordinated changes across 4 tools |
| Data richness | Low — TDD content invisible to pipeline | Low-to-medium — derived spec shallower than TDD | High — structured TDD sections natively extracted |
| Single source of truth | No | No | Yes |

---

## 7. Recommendation

**Recommendation: Option 3 — Modify TDD Template + Upgrade Pipeline Tools.**

### Rationale

**1. Option 3 is the only path to data richness and a single source of truth.** Options 1 and 2 both score Low on data richness and No on single source of truth. The TDD template contains highly structured content in §10, §14, §15, §19, and §24 with direct mappings to roadmap milestones and tasklist items. Only Option 3 closes that gap.

**2. The `--spec` flag gap is the most actionable upgrade vector in the entire pipeline.** Research file 03 confirmed the `--spec <spec-path>` flag is declared in sc:tasklist's argument-hint but has zero body implementation. The interface contract already exists and is visible to users. Implementing it is completing a stated intent, not a new API decision. Option 2 does not touch sc:tasklist at all.

**3. Option 2 requires working around a hard Boundaries constraint in sc:spec-panel.** Research file 01 confirmed sc:spec-panel's `Boundaries > Will Not` section explicitly states: "Generate specifications from scratch without existing content or context." Option 3 formalizes the TDD-reading capability cleanly rather than smuggling it in through a Boundaries workaround.

**4. All confirmed frontmatter field gaps make Option 2's pipeline outputs identical to Option 1's.** Research file 06 confirmed that `spec_type`, `complexity_score`, `complexity_class`, and `quality_scores` in any input spec's frontmatter are ignored by sc:roadmap. A derived spec produced by Option 2 flows through the pipeline identically to a hand-authored spec. Option 3 addresses the gap at the source.

**5. Option 3's scope is bounded and the extension points already exist.** The `--spec` hook is already declared in sc:tasklist. The `00-prd-extraction.md` artifact slot and PRD-to-TDD Pipeline section already exist in tdd/SKILL.md. The 8-step extraction pipeline's gaps are precisely documented.

### Recommendation Summary

| Factor | Decision |
|--------|----------|
| Implement Option | 3 |
| Phase order | Template frontmatter → sc:roadmap extraction → sc:roadmap scoring → sc:spec-panel → sc:tasklist → PRD→TDD handoff |
| Backward compatibility required | Yes — all changes additive or conditional on TDD-format detection |
| Breaking change | None — existing spec-template pipeline paths unchanged |
| Risk mitigation | Implement and test each phase independently; verify scoring weights sum to 1.0 before landing Phase 2 |

---

## 8. Implementation Plan

All file paths are absolute. All field names, section references, and instruction text are exact. A developer may begin implementation from this section alone without consulting other documents.

---

### Phase 1: TDD Template Frontmatter Additions

**Primary file:** `/Users/cmerritt/GFxAI/IronClaude/src/superclaude/examples/tdd_template.md`
**Secondary sync target:** `.claude/skills/tdd/` templates directory (run `make sync-dev` after editing source)

Insert these 8 fields after the `parent_doc` field and before `depends_on` in the YAML frontmatter block:

```yaml
feature_id: "[FEATURE-ID]"
spec_type: "new_feature"  # new_feature | refactoring | migration | infrastructure | security | performance | docs
complexity_score: ""      # 0.0–1.0 — computed by sc:roadmap; provide estimated value if known
complexity_class: ""      # LOW | MEDIUM | HIGH — computed by sc:roadmap; provide estimated value if known
target_release: "[version]"
authors: ["[author1]", "[author2]"]
quality_scores:
  clarity: ""
  completeness: ""
  testability: ""
  consistency: ""
  overall: ""
```

**Note on `spec_type` enum:** release-spec-template.md uses `new_feature | refactoring | portification | infrastructure`. The TDD addition expands this to include `migration | security | performance | docs`. When a TDD with `spec_type: migration` is passed to sc:roadmap, it should map to the `migration` template type — this mapping must be implemented in Phase 2 (scoring.md TDD-format detection rule).

**Sentinel self-check addition** (insert into the TDD template's usage preamble section):

```
Sentinel self-check (run before submitting TDD for pipeline consumption):
- feature_id must not be "[FEATURE-ID]"
- spec_type must be one of the valid enum values
- target_release must not be "[version]"
- complexity_score and complexity_class may remain empty (computed by sc:roadmap)

Quality gate: /sc:spec-panel @<this-tdd-file> --focus correctness,architecture --mode critique
```

**After editing source:** Run `make sync-dev` to propagate to `.claude/skills/tdd/`.
**Evidence base:** File 04 Section 1.1 "Notable absences vs. pipeline-oriented fields"; File 04 Section 2.1.

---

### Phase 2: sc:roadmap Extraction Pipeline Upgrades

#### Phase 2, Step 1: Extend Domain Keyword Dictionaries

**File:** `.claude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`

Add two new domains after the Documentation domain entry in Step 4 "Scope & Domain Classification":

```
Testing domain keywords: "unit test, integration test, e2e test, coverage, test suite, test plan, assertion, mock, fixture, spec file, test case, test strategy, test pyramid, qa gate, acceptance test, smoke test, regression test"

DevOps/Ops domain keywords: "runbook, on-call, monitoring, alerting, dashboard, metric, SLO, SLA, deployment, rollout, rollback, feature flag, canary, blue-green, observability, tracing, log level, capacity planning, incident, escalation"
```

Also update the `domain_spread` factor normalization denominator in scoring.md from 5 to 7: `min(domains / 7, 1.0)`.

**Evidence base:** File 02 "Domain Keyword Gap"; File 02 Section 6 Key Takeaway 5.

#### Phase 2, Step 2: Add TDD-Specific Extraction Steps (Steps 9–14) and Scoring Formula Update

**File A:** `.claude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md`

Add after Step 8 "ID Assignment". These steps execute only when TDD-format input is detected (detection rule: input contains `## 10. Component Inventory` heading OR YAML frontmatter with `type: "📐 Technical Design Document"` OR has 20+ section headings matching TDD numbering pattern).

| Step | Name | What It Extracts | Storage Key |
|------|------|-----------------|-------------|
| 9 | Component Inventory Extraction | New/modified/deleted component tables from `## 10. Component Inventory` | `component_inventory: { new: [{name, purpose}], modified: [{name, change}], deleted: [{name, migration_target}] }` |
| 10 | Migration Phase Extraction | Rollout stage table from §19.3; rollback steps from §19.4 | `migration_phases: { stages: [{stage, environment, criteria, rollback_trigger}], rollback_steps: [string] }` |
| 11 | Release Criteria Extraction | DoD checklist from §24.1; release checklist from §24.2 (runs independently from Step 6) | `release_criteria: { definition_of_done: [string], release_checklist: [string] }` |
| 12 | Observability Extraction | Metrics table from §14.2; alerts table from §14.4; dashboard names/links from §14.5 | `observability: { metrics: [{name, description, type, target}], alerts: [{name, condition, severity}], dashboards: [{name, link}] }` |
| 13 | Testing Strategy Extraction | Test pyramid from §15.1; unit/integration/E2E test case tables from §15.2; environments from §15.3 | `testing_strategy: { test_pyramid: [{level, coverage_target, tools}], unit_tests, integration_tests, e2e_tests, environments }` |
| 14 | API Surface Extraction | Endpoint count from endpoint tables in `## 8. API Specifications` §8.2 | `api_surface: { endpoint_count: N }` |

Each step stores `null` for its key if the corresponding section is absent or empty.

**File B:** `.claude/skills/sc-roadmap-protocol/refs/scoring.md`

TDD-format detection rule (add at top of scoring section):
```
TDD-format detection: Input spec is classified as TDD-format if it contains YAML frontmatter with `type` field containing "Technical Design Document", OR if the document body contains 20 or more section headings matching the TDD section numbering pattern (## N. Heading).

When TDD-format is detected: use the 7-factor TDD scoring formula below.
When TDD-format is not detected: use the standard 5-factor formula (unchanged).
```

Updated 7-factor complexity scoring formula for TDD-format input:

| Factor | Raw Value Source | Normalization | Weight |
|--------|-----------------|---------------|--------|
| `requirement_count` | Total FRs + NFRs from extraction | `min(count / 50, 1.0)` | 0.20 |
| `dependency_depth` | Max chain in dependency graph | `min(depth / 8, 1.0)` | 0.20 |
| `domain_spread` | Distinct domains with ≥10% representation (out of 7) | `min(domains / 7, 1.0)` | 0.15 |
| `risk_severity` | `(high*3 + medium*2 + low*1) / total_risks` | `(weighted_avg - 1.0) / 2.0` | 0.10 |
| `scope_size` | Total line count of specification | `min(lines / 1000, 1.0)` | 0.15 |
| `api_surface` | Endpoint count from Step 14 | `min(count / 30, 1.0)` | 0.10 |
| `data_model_complexity` | Entity count + relationship count from §7 Data Entities table | `min(count / 20, 1.0)` | 0.10 |

**Weights sum verification:** 0.20 + 0.20 + 0.15 + 0.10 + 0.15 + 0.10 + 0.10 = 1.00 (verified)

Standard formula (non-TDD input — unchanged): original 5-factor formula with weights 0.25/0.25/0.20/0.15/0.15 remains in effect; `domain_spread` normalization denominator stays at 5.

**Evidence base:** File 02 Section 3; File 02 Section 6 Key Takeaway 5; File 06 Option 3 Feasibility.

---

### Phase 3: sc:spec-panel Additions

**File:** `.claude/commands/sc/spec-panel.md` (standalone 624-line command file)

#### Addition 1: Behavioral Flow — Steps 6a and 6b (insert after existing Step 6 "Improve")

```
Step 6a (conditional — TDD input detected): If the input document is a TDD (detected by presence of `type: "📐 Technical Design Document"` in YAML frontmatter OR 20+ TDD section headings), scope the improved output to a single release increment using `target_release` from TDD frontmatter. If `target_release` is empty or absent, ask the user to specify the target release before proceeding.

Step 6b (conditional — output intended for sc:roadmap): If the user's intent is to feed the output into sc:roadmap (indicated by user instruction or by `--downstream roadmap` flag), ensure the output document contains the following frontmatter fields populated from the TDD frontmatter or computed from TDD content analysis:
- spec_type: copy from TDD spec_type field; if absent, infer from TDD section content
- complexity_score: copy from TDD complexity_score if populated; else leave as placeholder
- complexity_class: copy from TDD complexity_class if populated; else leave as placeholder
- target_release: copy from TDD target_release
- feature_id: copy from TDD feature_id
```

#### Addition 2: Output Section (insert after existing Output block)

```
Output — when input is a TDD:

(a) Review document (default): Structured review document in standard --format mode. Expert analysis covers TDD sections §5 Technical Requirements, §6 Architecture, §7 Data Models, §8 API Specifications, §13 Security Considerations, §15 Testing Strategy, and §20 Risks & Mitigations.

(b) Scoped release spec (when --downstream roadmap or when user requests): Document in release-spec-template.md format covering sections relevant to target_release from TDD frontmatter. Scoped spec extracts FRs from TDD §5.1, NFRs from TDD §5.2, architecture decisions from TDD §6.4, risks from TDD §20, test plan from TDD §15, migration plan from TDD §19. YAML frontmatter populated from TDD frontmatter fields.

Note: spec-panel does not CREATE a spec from raw instructions (Boundaries constraint unchanged). The TDD-to-spec capability requires an existing, substantially populated TDD as input.
```

#### Addition 3: Tool Coordination Section (insert into existing "Read" tools list)

```
- src/superclaude/examples/release-spec-template.md — read when generating scoped release spec output from TDD input (Step 6b / --downstream roadmap mode)
```

**Evidence base:** File 01 Sections 3.5, 3.6, 3.7; File 06 Corrections List items 1 and 5.

---

### Phase 4: sc:tasklist Additions

**File:** `.claude/skills/sc-tasklist-protocol/SKILL.md`

The `--spec` flag is declared in the frontmatter argument-hint at line 9 but has zero body implementation. This phase writes the body implementation.

#### Addition 1: Step 4.1a — Supplementary TDD Context Loading (insert after Step 4.1)

```
Step 4.1a — Supplementary TDD Context (conditional on --spec flag):

If --spec <spec-path> was provided:
1. Read the file at <spec-path>.
2. Detect if the file is TDD-format (YAML frontmatter type contains "Technical Design Document" OR 20+ section headings matching TDD numbering pattern).
3. If TDD-format: extract the following content and store as supplementary_context:
   - component_inventory: scan for ## 10. Component Inventory; extract new/modified/deleted component tables
   - migration_phases: scan for ## 19. Migration & Rollout Plan; extract rollout stage table from §19.3; rollback steps from §19.4
   - testing_strategy: scan for ## 15. Testing Strategy; extract test pyramid from §15.1; unit/integration/E2E test case tables from §15.2
   - observability: scan for ## 14. Observability & Monitoring; extract metrics table from §14.2; alerts table from §14.4
   - release_criteria: scan for ## 24. Release Criteria; extract §24.1 DoD checklist items
4. If spec-path file is not TDD-format: log warning and continue with roadmap-only generation.
5. If spec-path file does not exist: abort with error.
```

#### Addition 2: Step 4.4a — Supplementary Task Generation (insert after Step 4.4)

Runs after standard Step 4.4; appends additional tasks to appropriate phase buckets. Merge rather than duplicate if a generated task duplicates an existing task for the same component.

| Context Key | Task Pattern | Tier | Phase Assignment |
|-------------|-------------|------|-----------------|
| `component_inventory.new` entries | `Implement [component_name]` | STANDARD (STRICT if auth/security/crypto/database/migration/schema/model) | Phase 1 unless migration_phases overrides |
| `component_inventory.modified` entries | `Update [component_name]: [change_description]` | STANDARD or STRICT per keyword rule | Phase 1 unless migration_phases overrides |
| `component_inventory.deleted` entries | `Migrate [component_name] to [migration_target]` or `Remove [component_name]` | STRICT if migration_target non-empty | Phase 1 unless migration_phases overrides |
| `migration_phases.stages` | Re-bucket all tasks using migration phase order; add `rollback_steps` as Rollback field on every migration-phase task (replacing default "TBD") | — | Replaces heading-based phase buckets |
| `testing_strategy.test_pyramid` entries | `Write [level] test suite ([tools])`; Validation bullet 1: verbatim test run command if runnable | STANDARD | Same phase as feature tasks they test |
| `observability.metrics` entries | `Instrument metric: [name]` | STANDARD | Last phase |
| `observability.alerts` entries | `Configure alert: [name]` | STANDARD | Last phase |
| `release_criteria.definition_of_done` items | `Verify DoD: [item_text truncated to 60 chars]` | EXEMPT | End of final phase |

#### Addition 3: Stage 7 Supplementary Spec Validation (insert into Post-Generation Roadmap Validation, Stage 7)

When `--spec` was provided, each Stage 7 validation agent additionally checks the generated tasklist against `supplementary_context`:

| Check | Finding Level | Flag Message |
|-------|--------------|--------------|
| Every entry in `component_inventory.new` has a corresponding task | HIGH | "Missing task for new component [name] from TDD §10." |
| Migration stage names from `migration_phases.stages` reflected in phase bucket names or task titles | MEDIUM | "Migration stage [name] from TDD §19 has no corresponding task bucket or task." |
| Each test pyramid level in `testing_strategy.test_pyramid` has at least one task | MEDIUM | "No [level] test task generated despite TDD §15 test pyramid entry." |
| Each DoD item appears as a DoD verification task or in final phase ACs | LOW | "DoD item '[item_text]' from TDD §24 has no coverage in final phase." |

Findings merged into the same consolidated findings list used by Stage 8. Standard roadmap-only validation is unchanged for invocations without `--spec`.

**Evidence base:** File 03 Section 1 (`--spec` flag gap); File 03 Section 8 Q1; File 03 Section 9; gaps-and-questions.md item [03] item 6.

---

### Phase 5: PRD→TDD Handoff Improvements

**File:** `.claude/skills/tdd/SKILL.md`

#### Addition 1: PRD Extraction Agent Prompt (insert after the last existing agent prompt template in `## Agent Prompt Templates`)

Define a named `### PRD Extraction Agent Prompt` section with a system prompt that instructs the agent to:

- Read the PRD file at `{{PRD_REF}}`
- Write to `${TASK_DIR}research/00-prd-extraction.md`
- Extract 5 sections with defined output formats:
  - Section 1: Epics — table: Epic ID | Title | Description
  - Section 2: User Stories and Acceptance Criteria — story text + bulleted ACs, grouped by parent epic ID
  - Section 3: Success Metrics — table: Metric | Baseline | Target | Measurement Method
  - Section 4: Technical Requirements — flat list with requirement type labels
  - Section 5: Scope Boundaries — in-scope bulleted list + out-of-scope bulleted list
- Tag each fact as [CODE-VERIFIED], [CODE-CONTRADICTED], or [UNVERIFIED]

The agent should be spawned as a read-only research agent. This closes Gap 1 confirmed by File 06 E3.

#### Addition 2: Synthesis Mapping Table Update

Add `00-prd-extraction.md` as a source for synth-03 through synth-07 in `.claude/skills/tdd/SKILL.md`:

| Synthesis File (TDD skill) | Add Source |
|---------------------------|------------|
| `synth-03-architecture.md` | `00-prd-extraction.md (Section 4: Technical Requirements — architectural constraints)` |
| `synth-04-data-api.md` | `00-prd-extraction.md (Section 2: User Stories and ACs — data model traceability)` |
| `synth-05-state-components.md` | `00-prd-extraction.md (Section 2: User Stories and ACs — interaction flows; Section 5: Scope Boundaries)` |
| `synth-06-error-security.md` | `00-prd-extraction.md (Section 4: Technical Requirements — security and error-handling constraints)` |
| `synth-07-observability-testing.md` | `00-prd-extraction.md (Section 3: Success Metrics — KPIs to translate into observability targets; Section 2: ACs — acceptance criteria driving test coverage)` |

Note: synth-01-exec-problem-goals.md, synth-02-requirements.md, synth-08-perf-deps-migration.md, and synth-09-risks-alternatives-ops.md already list PRD extraction as a source in the current Synthesis Mapping Table (confirmed in TDD SKILL.md at lines 1074-1082) and do not require modification. Only synth-03 through synth-07 are missing PRD extraction as a source.

[CORRECTION APPLIED by rf-qa-qualitative 2026-03-24: Previous version listed PRD skill synthesis file names (synth-03-competitive-scope.md etc.) instead of TDD skill synthesis file names, and incorrectly stated the already-correct files did not need PRD extraction.]

#### Addition 3: Synthesis Agent Prompt Rules (append to existing rules list)

```
Rule 12: "Every FR in TDD Section 5.1 must trace back to a PRD epic or user story. Cite the epic ID in the FR row's 'Source' column. If no PRD epic can be identified for an FR, mark it '[NO PRD TRACE]' and flag it as a gap."

Rule 13: "TDD Section 4.2 (Business Metrics, if included) must include at least one engineering proxy metric for each business KPI listed in the PRD's Section 4 and Section 19. Format as: Business KPI: [PRD KPI name] — Engineering Proxy: [measurable technical metric]."
```

#### Addition 4: Synthesis QA Gate Checklist (append to existing checklist)

```
Item 13: "FR traceability — spot-check 3 FRs in the synth-04 output: each must cite a PRD epic ID in its Source column. If any FR lacks a PRD epic citation and is not marked '[NO PRD TRACE]', flag as FAIL."
```

**Evidence base:** File 05 Sections 2.2, 2.6, 3.1–3.3; File 06 Claim E3; gaps-and-questions.md items on PRD traceability enforcement.

---

### Integration Checklist

Run these verification steps after all phases are implemented.

**Phase 1 — TDD Template:**
- [ ] `grep -c 'feature_id' src/superclaude/examples/tdd_template.md` returns 1
- [ ] `grep -c 'spec_type' src/superclaude/examples/tdd_template.md` returns 1
- [ ] `grep -c 'quality_scores' src/superclaude/examples/tdd_template.md` returns 1
- [ ] `make verify-sync` passes

**Phase 2 — sc:roadmap extraction and scoring:**
- [ ] Passing a TDD with populated `## 10. Component Inventory` to sc:roadmap produces a roadmap that includes component work items in at least one milestone
- [ ] TDD scoring formula weights sum to 1.0: 0.20 + 0.20 + 0.15 + 0.10 + 0.15 + 0.10 + 0.10 = 1.00
- [ ] Passing a standard `release-spec-template.md`-format spec produces identical roadmap output to pre-Phase-2 behavior (backward compatibility check)
- [ ] extraction-pipeline.md now lists 7 domains (Frontend, Backend, Security, Performance, Documentation, Testing, DevOps/Ops)

**Phase 3 — sc:spec-panel:**
- [ ] Passing a TDD with `target_release` populated produces a scoped release spec with that release version in the YAML frontmatter
- [ ] `grep -c 'release-spec-template.md' .claude/commands/sc/spec-panel.md` returns 1
- [ ] Passing raw text instructions with no existing spec content still results in refusal (Boundaries constraint intact)

**Phase 4 — sc:tasklist:**
- [ ] Passing `sc:tasklist <roadmap> --spec <tdd-path>` where TDD has populated §10 generates tasks derived from the component inventory (one task per new component)
- [ ] SKILL.md body now contains an implementation block for `--spec` flag processing (not just the frontmatter argument-hint declaration)
- [ ] Passing `sc:tasklist <roadmap>` with no `--spec` flag produces identical output to pre-Phase-4 behavior (backward compatibility check)

**Phase 5 — tdd skill PRD handoff:**
- [ ] tdd/SKILL.md Synthesis Mapping Table now lists `00-prd-extraction.md` as a source for synth-03, synth-04, synth-05, synth-06, and synth-07
- [ ] tdd/SKILL.md Synthesis QA Gate checklist now contains Item 13 for FR traceability
- [ ] tdd/SKILL.md contains a named "PRD Extraction Agent Prompt" section with the extraction instructions

---

## 9. Open Questions

All questions below remain unresolved and require further investigation or decision. Questions definitively answered by research are excluded (see Section 9.2). Questions are ordered by impact level.

### 9.1 Open Questions Table

| # | Question | Impact | Suggested Resolution |
|---|----------|--------|----------------------|
| 2 | The 5-domain keyword dictionaries have no Testing or DevOps/Ops domain. TDD sections §15 and §25 will score poorly against all five domains and may be miscategorized. Should Steps 9–14 proposed for Option 3 extend the domain dictionaries, or should they bypass domain classification entirely for TDD-structured sections? | **Critical** — Without domain dictionary extension, TDD-heavy specifications will systematically underestimate complexity. | Decide whether to (a) add Testing and DevOps/Ops domains to the 5-domain dictionaries, (b) create a separate TDD-detection branch in the classification step, or (c) document this as a known limitation. |
| 3 | The `--spec` flag in sc:tasklist is declared in the SKILL.md argument-hint but has zero implementation. What are its intended semantics? Is it meant to (a) enrich task acceptance criteria from spec content, (b) restrict task scope to items mentioned in the spec, (c) provide metadata for TASKLIST_ROOT computation, (d) activate a TDD-aware parsing mode, or something else entirely? | **Critical** — Option 3's sc:tasklist upgrade has this flag as its natural extension point. Without knowing the intended semantics, the implementation could conflict with the original design intent. | Read any design notes, PRD sections, or git history comments referencing the `--spec` flag. If none exist, treat the flag as intentionally undefined and define semantics as part of the Option 3 implementation spec. |
| 4 | Does `00-prd-extraction.md` have a specified, stable format that all downstream synthesis agents understand and can parse, or does each TDD execution run produce a different structure depending on which agent handles the extraction step? | **Critical** — If the format is ad-hoc, synthesis files that list `00-prd-extraction.md` as a source will produce inconsistent results across runs. PRD→TDD handoff quality is therefore non-deterministic. | Read the TDD SKILL.md text surrounding the `00-prd-extraction.md` production step to check whether a schema or template for that file is defined. If not, this is a gap requiring a defined extraction schema as part of the Option 3 PRD→TDD wiring fix. |
| 6 | What is the exact line (or line range) in extraction-pipeline.md where the new Steps 9–14 should be inserted? Does Step 9 replace Step 4's domain classification, augment it, or run in parallel after Step 8? | **Important** — Determines the precise insertion point for the Option 3 pipeline change. Wrong insertion order could cause ID assignment (Step 8) to run before new extraction steps, producing non-deterministic IDs. | Map the 8-step pipeline execution order in extraction-pipeline.md and confirm whether new TDD-specific steps should run before or after Step 8 ID Assignment. |
| 8 | What is the detection mechanism for sc:roadmap to identify TDD input? Does it check for TDD-specific section headings, check the `type` frontmatter field, or use some other heuristic? | **Important** — The detection mechanism determines whether spec-panel's proposed "TDD detection rule" and sc:tasklist's proposed `--spec` upgrade can reliably activate their TDD-aware modes. | Define a TDD detection protocol as part of the Option 3 spec: enumerate the signal(s) that reliably distinguish a TDD from a spec (e.g., presence of frontmatter `type: "📐 Technical Design Document"`, or presence of 3+ of: §5, §7, §8, §9, §10, §14, §15, §19, §24 headings). |
| 9 | Will specs manually created from release-spec-template.md (Path A) still produce identical pipeline behavior after Option 3's sc:roadmap extraction pipeline changes land? | **Important** — Backward compatibility guarantee. If Steps 9–14 run unconditionally, any spec with content resembling TDD section structure could be processed differently than before. | Define in the Option 3 implementation spec whether new extraction steps are (a) conditionally gated on TDD-format detection, or (b) always run and simply produce empty results for non-TDD sections. Document the backward compatibility guarantee explicitly. |
| 11 | Does the `rf-qa-qualitative` agent's definition check PRD traceability (verifying TDD §5 requirements trace back to PRD epics), or does it only check general document quality? | **Important** — If the agent does not check PRD traceability, the PRD-to-TDD Pipeline section's "every requirement in TDD §5 should trace back to a PRD epic" constraint is unenforced at QA time. | Read `.claude/agents/rf-qa-qualitative.md` to determine what checks it performs. Compare against the PRD traceability requirement from the TDD PRD-to-TDD Pipeline section. |
| 12 | Does spec-panel write an improved spec file as a distinct output artifact, or does it embed the improved spec content inline within the review document? If the former, what is the file naming convention and path? | **Important** — Directly affects how spec-panel fits into the Option 3 pipeline redesign. If spec-panel produces a standalone improved spec file, that file can be directly passed to sc:roadmap without an extraction step. | Read spec-panel.md's Tool Coordination section and any artifact path definitions. Look for `Write` tool invocations with defined output paths for the improved spec. |
| 13 | The `quality_scores` YAML frontmatter field and spec-panel's output quality metrics use different schemas. Is there any planned bridge between the two, and should Option 3 define one? | **Important** — Without a bridge, the `quality_scores` field in the spec template has no mechanism to be populated by tool output. | Determine whether the Option 3 scope should include defining a mapping between spec-panel's output quality metrics and the `quality_scores` frontmatter schema. If yes, add this as a deliverable to the Option 3 implementation plan. |
| 14 | The `--output` flag in sc:tasklist is declared in the argument-hint but TASKLIST_ROOT is always computed from roadmap text, never from a CLI argument. Is the `--output` flag intended to override TASKLIST_ROOT computation, or was it intended for a different purpose? | **Minor** — User-facing UX gap. Not a blocker for Option 3 but should be resolved in the same upgrade to avoid confusing behavior when both `--output` and roadmap-embedded paths are present. | Read any design notes or git history referencing the `--output` flag. If no documentation exists, define its semantics as part of the Option 3 sc:tasklist upgrade. |
| 15 | Should `synth-04-data-api.md` in the TDD skill's synthesis stage read PRD Section 21.1 user flows to ensure data models support all documented user interactions? | **Minor** — Quality improvement opportunity. If PRD user flows are not consulted during data model synthesis, the TDD may produce technically correct but product-misaligned data models. | Check whether the TDD synthesis file mapping table in SKILL.md lists PRD sections as sources for `synth-04-data-api.md`. |
| 16 | sc:spec-panel references NFR-8 (target false positive rate <30% for correctness-focus auto-suggestion) and defers measurement to "Gate B (T05.02)." Where are NFR-8 and Gate B defined? | **Minor** — Does not affect pipeline behavior but means the NFR-8 compliance claim in the command file is unverifiable without finding its source document. | Search for NFR-8 and "Gate B" in the project repository. If not found, flag as an orphaned reference in spec-panel.md. |
| 17 | For the `feature_id`, `target_release`, and `authors` fields described in research file 04's "Exact Additions Needed" section — are these also ignored by the pipeline (as all other tested frontmatter fields are), or does sc:roadmap actually read any of them? | **Minor** — The pattern established by all verified frontmatter fields strongly suggests these are also ignored, but this was not directly verified against the pipeline source files. | Grep the sc-roadmap-protocol skill and all refs/ for `feature_id`, `target_release`, and `authors` as variables being read. If zero code-reads found, mark these three fields as probable-IGNORED consistent with the established pattern. |

---

### 9.2 Questions Definitively Answered by Research

The following questions were raised during research but were definitively resolved by cross-verification in research file 06 and are therefore NOT listed in the Open Questions table:

| Question | Answer | Evidence |
|----------|--------|----------|
| Does sc:roadmap read `spec_type` from frontmatter? | No — [CODE-CONTRADICTED] | Research file 02 (scoring.md, templates.md); research file 06 Claim B1 |
| Does sc:roadmap read `complexity_score` / `complexity_class` from frontmatter? | No — always computed from scratch; [CODE-CONTRADICTED] | Research file 02; research file 06 Claim B2 |
| Does sc:roadmap read `quality_scores` from frontmatter? | No — [CODE-CONTRADICTED] | Research file 02; research file 06 Claim B3 |
| Can spec-panel generate a spec from raw instructions with no existing spec content? | No — explicitly refused in Boundaries section; [CODE-CONTRADICTED] | Research file 01; research file 06 Claim A3 |
| Does sc:tasklist use the `--spec` flag for any processing? | No — declared but completely unimplemented; [CODE-VERIFIED] | Research file 03; research file 06 Claim C2 |
| Is the TDD `PRD_REF` field defined? | Yes — confirmed in Step A.2 of TDD SKILL.md; [CODE-VERIFIED] | Research file 05; research file 06 Claim E1 |
| Does the PRD extraction step produce `00-prd-extraction.md`? | Yes — path confirmed as `${TASK_DIR}research/00-prd-extraction.md`; [CODE-VERIFIED] | Research file 05; research file 06 Claim E2 |
| Is `spec_type` read as a variable anywhere in the sc:roadmap pipeline (including undocumented conventions)? | No — grep of entire `.claude/skills/sc-roadmap-protocol/` for `spec_type` returns zero matches. No undocumented convention exists. Consistent with [CODE-CONTRADICTED] finding in S2.2. [CODE-VERIFIED by rf-qa-qualitative 2026-03-24] | Direct grep verification; consistent with Research file 02 and Research file 06 Claim B1 |
| Does the domain_spread normalization denominator in scoring.md need updating from 5 to 7 when Testing and DevOps/Ops domains are added? | Yes — scoring.md line 17 confirms current formula is `min(domains / 5, 1.0)` with weight 0.20. The denominator is 5 and MUST be updated to 7 when two new domains are added. Without this change, any spec touching Testing or Ops keywords would reach domain_spread = 1.0 with fewer than 7 domains, inflating complexity scores for all specifications. Phase 2 Step 1 of the implementation plan already includes this update. [CODE-VERIFIED by rf-qa-qualitative 2026-03-24] | scoring.md line 17 direct read; Phase 2 Step 1 implementation plan |
| Is there an `rf-prd-extractor` agent definition file? | No — `.claude/agents/` contains no file matching `rf-prd-extractor*` or any similar PRD extraction agent. Confirmed Gap 1: PRD extraction is done by a generic Agent subagent with an ad-hoc prompt. This is a required deliverable for Option 3 Phase 5 Addition 1. [CODE-VERIFIED by rf-qa-qualitative 2026-03-24] | Direct listing of `.claude/agents/`; 35 agent files found, none matching prd-extractor |
| When PRD Phase 7 invokes the tdd skill with the PRD as input, is PRD_REF auto-populated? | No — PRD SKILL.md Phase 7 (line 491) says "invoke the `tdd` skill with the PRD as input" but does not specify how PRD_REF is set. The invocation is described as passing the PRD "as input" which likely means as a prompt parameter, not as an explicit PRD_REF field assignment. This is a gap: Option 3 Phase 5 should define whether PRD_REF is auto-populated from the PRD output path at Phase 7 invocation time, or whether it remains a manual user input. [CODE-VERIFIED by rf-qa-qualitative 2026-03-24] | PRD SKILL.md line 491 direct read |

---

## 10. Evidence Trail

Complete inventory of all files produced during the research and synthesis phases of this investigation. Serves as an audit record, a completeness check, and an index for locating primary evidence for any specific claim.

### 10.1 Codebase Research Files

All files in `/TASK-RESEARCH-20260324-001/research/`:

| File | Topic | Status |
|------|-------|--------|
| `research/01-spec-panel-audit.md` | sc:spec-panel command — full audit of `.claude/commands/sc/spec-panel.md` (624 lines): template awareness, sentinel system knowledge, output format, creation vs. review capability, quality metric schema, downstream integration wiring | Complete |
| `research/02-roadmap-pipeline-audit.md` | sc:roadmap pipeline — full audit of sc-roadmap-protocol SKILL.md and all refs/ (extraction-pipeline.md, scoring.md, templates.md, validation.md, adversarial-integration.md): 8-step extraction pipeline, 5-factor complexity formula, template selection algorithm, TDD section capture analysis, domain keyword dictionaries, Wave 0–4 behavior | Complete |
| `research/03-tasklist-audit.md` | sc:tasklist — full audit of sc-tasklist-protocol SKILL.md, rules/tier-classification.md, rules/file-emission-rules.md, templates/index-template.md, templates/phase-template.md: input contract, 11-step generation algorithm, `--spec` flag status, tier classification rules, output file format, post-generation validation pipeline (Stages 7–10) | Complete |
| `research/04-tdd-template-audit.md` | TDD template and spec template — full audit of `src/superclaude/examples/tdd_template.md` (1,309 lines) and `src/superclaude/examples/release-spec-template.md` (264 lines): frontmatter field inventory, section structure, sentinel system, pipeline compatibility analysis, extraction mapping (corrected per QA fix cycle 1) | Complete |
| `research/05-prd-tdd-skills-audit.md` | PRD and TDD creator skills — full audit of `.claude/skills/prd/SKILL.md` (1,373 lines) and `.claude/skills/tdd/SKILL.md` (1,344 lines): PRD output artifact paths, TDD input fields (PRD_REF), `00-prd-extraction.md` production, synthesis file source mapping, PRD→TDD handoff gap analysis (6 gaps identified) | Complete |
| `research/06-analysis-doc-verification.md` | Analysis document cross-validation — systematic verification of 19 substantive claims from `.dev/analysis/spec-vs-prd-vs-tdd.md` against research files 01–05: 18 claims [CODE-VERIFIED], 5 claims [CODE-CONTRADICTED], 0 [UNVERIFIED]; Corrections List (5 required corrections); Option 3 feasibility assessment | Complete |
| `research/research-notes.md` | Central research scaffold — investigation scope header and status (intentionally minimal per user authorization; substantive scope index reconstructed from individual research files) | Complete (waived) |

### 10.2 Synthesis Files

All files in `/TASK-RESEARCH-20260324-001/synthesis/`:

| File | Report Sections Covered | Status |
|------|------------------------|--------|
| `synthesis/synth-01-verified-current-state.md` | Section 1 (Problem Statement), Section 2 (Verified Current State) — research question, motivation for verification, cross-validation results, corrected current-state model of the pipeline including all 5 CODE-CONTRADICTED corrections | Complete |
| `synthesis/synth-02-gap-analysis.md` | Section 3 (Target State), Section 4 (Gap Analysis) — Option 3 desired behaviors, success criteria, gap-by-gap analysis of sc:roadmap extraction, sc:tasklist TDD-section handling, PRD→TDD handoff gaps, and Option 2 viability reassessment | Complete |
| `synthesis/synth-03-option3-implementation-plan.md` | Sections 6 (Options Analysis), 7 (Recommendation), 8 (Implementation Plan) — three-option comparison, recommendation rationale, 5-phase implementation plan with integration checklist; Section 5 N/A block included (codebase-only scope, no web research performed) | Complete |
| `synthesis/synth-04-questions-evidence.md` | Section 9 (Open Questions), Section 10 (Evidence Trail) — 17-question open questions table triaged by impact, definitively-answered questions log, codebase research file inventory, synthesis file inventory, QA reports inventory, gaps log reference | Complete |

**Note on synthesis numbering:** synth-03 (Sections 6–8) covers Options Analysis, Recommendation, and Implementation Plan. Section 5 (External Research Findings) is declared N/A — the research scope was codebase verification only; no web research files were produced. The absence of Section 5 external findings is intentional and noted here.

### 10.3 QA Reports

All files in `/TASK-RESEARCH-20260324-001/qa/`:

| File | QA Phase | Verdict |
|------|----------|---------|
| `qa/qa-research-gate-report.md` | Research Gate — initial QA cycle: verified file inventory completeness, evidence density, scope coverage, documentation cross-validation tagging, contradiction resolution, gap severity ratings, depth appropriateness, integration point coverage, pattern documentation, incremental writing compliance | **FAIL** — 6 of 10 checks passed; 4 issues requiring resolution (1 critical-equivalent: incorrect sc:roadmap behavior claims in file 04; 2 important: research-notes.md empty, gap severity ratings missing; 1 minor: file 01 status header) |
| `qa/analyst-completeness-report.md` | Research Completeness Verification — independent analyst review: coverage audit (17 of 19 scope items fully covered), evidence quality assessment per file, documentation staleness check, contradiction analysis (2 HIGH severity contradictions between files 02/04 identified), compiled gap ratings (2 critical, 3 important, 2 minor) | **FAIL** — 7 gaps found (2 critical, 3 important, 2 minor); corrections required before synthesis |
| `qa/qa-research-gate-fix-cycle-1.md` | Research Gate Fix Cycle 1 — verification that all 4 issues from the initial QA gate report were resolved: file 04 sc:roadmap behavior descriptions corrected for `spec_type`, `complexity_score`, `complexity_class`, `quality_scores`; research-notes.md accepted as-is per user authorization; gap severity ratings added; file 01 status header updated to Complete | **PASS** — 4 of 4 previously-failed checks now passing; 0 new issues introduced; green light to proceed to synthesis |
| `qa/analyst-synthesis-review.md` | Synthesis Completeness Verification (Analyst) — independent analyst review of all 4 synthesis files: section coverage audit, evidence quality assessment, cross-synthesis consistency check, gap triage | **FAIL (with fixes applied)** — issues found resolved in tandem with synthesis-gate QA; synthesis files updated before assembly |
| `qa/qa-synthesis-gate-report.md` | Synthesis Gate — 12-item synthesis checklist applied to all 4 synth files: section headers, table structures, fabrication checks (5 claims per file), evidence citations, options analysis, implementation plan specificity, cross-section consistency, doc-only claims, stale docs surfaced, content rules compliance, completeness, hallucinated file paths | **PASS** — 9 of 12 checks passed initially; 3 issues found (CRITICAL: Section 5 absent; IMPORTANT ×2: synth-04 status labels); all 3 fixed in-place during gate; net result PASS |

### 10.4 Gaps Log

| File | Description |
|------|-------------|
| `gaps-and-questions.md` | Consolidated gaps and questions log — all unresolved questions from research files 01–06, organized into three severity tiers: Critical (5 gaps, sourced to files 02, 02, 03, 05, 05), Important (13 gaps, sourced to files 01, 01, 02, 02, 02, 02, 03, 03, 03, 03, 05, 05, 05), Minor (5 gaps, sourced to files 01, 01, 01, 03, 05). Severity ratings added in Fix Cycle 1. |

### 10.5 Source Files Investigated

| File | Lines | Role in Investigation |
|------|-------|----------------------|
| `.claude/commands/sc/spec-panel.md` | 624 | sc:spec-panel command — primary investigation target (research/01) |
| `.claude/skills/sc-roadmap-protocol/SKILL.md` | — | sc:roadmap skill root — primary investigation target (research/02) |
| `.claude/skills/sc-roadmap-protocol/refs/extraction-pipeline.md` | — | 8-step extraction pipeline definition (research/02) |
| `.claude/skills/sc-roadmap-protocol/refs/scoring.md` | — | 5-factor complexity formula (research/02) |
| `.claude/skills/sc-roadmap-protocol/refs/templates.md` | — | Template type selection algorithm (research/02) |
| `.claude/skills/sc-roadmap-protocol/refs/validation.md` | — | Validation pipeline definition (research/02) |
| `.claude/skills/sc-roadmap-protocol/refs/adversarial-integration.md` | — | Adversarial integration wiring (research/02) |
| `.claude/skills/sc-tasklist-protocol/SKILL.md` | — | sc:tasklist skill root — primary investigation target (research/03) |
| `.claude/skills/sc-tasklist-protocol/rules/tier-classification.md` | — | Tier classification rules (research/03) |
| `.claude/skills/sc-tasklist-protocol/rules/file-emission-rules.md` | — | Output file emission rules (research/03) |
| `src/superclaude/examples/tdd_template.md` | 1,309 | TDD template — primary investigation target (research/04) |
| `src/superclaude/examples/release-spec-template.md` | ~264 | Spec template — comparison target (research/04) |
| `.claude/skills/prd/SKILL.md` | 1,373 | PRD creator skill — primary investigation target (research/05) |
| `.claude/skills/tdd/SKILL.md` | 1,344 | TDD creator skill — primary investigation target (research/05) |
| `.dev/analysis/spec-vs-prd-vs-tdd.md` | — | Original analysis document — cross-validation target (research/06) |
