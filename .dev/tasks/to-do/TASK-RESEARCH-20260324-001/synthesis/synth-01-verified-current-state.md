# Synthesis 01: Verified Current State

**Status:** Complete
**Date:** 2026-03-24
**Task:** TASK-RESEARCH-20260324-001
**Research files:** 01-spec-panel-audit.md, 02-roadmap-pipeline-audit.md, 03-tasklist-audit.md, 04-tdd-template-audit.md, 05-prd-tdd-skills-audit.md, 06-analysis-doc-verification.md, gaps-and-questions.md

---

## Section 1 — Problem Statement

### 1.1 Original Research Question

The analysis document `.dev/analysis/spec-vs-prd-vs-tdd.md` was produced through conversation — not by tracing actual source files. It describes the current pipeline behavior, argues for three implementation options, and recommends Option 3 (modify TDD template AND upgrade sc:roadmap, sc:spec-panel, and sc:tasklist to actively consume the TDD's rich sections).

The research question: **verify every factual claim in that document against actual source files**, then produce a precise implementation plan for Option 3 that corrects any errors found.

### 1.2 Why This Verification Matters

The analysis document's implementation recommendations depend entirely on an accurate current-state model. Specifically:

- If a pipeline step is described as consuming a frontmatter field that it does not actually read, then any implementation plan that says "add that field to the TDD so the pipeline can use it" will silently fail.
- If a command is described as capable of a behavior it explicitly refuses to perform, then any plan that relies on that behavior will require new capability development, not configuration.
- If a flag is declared to exist but is unimplemented, then any plan that builds on that flag has a foundation that must be built before the plan can proceed.

Wrong assumptions in a current-state analysis propagate directly into wrong implementation scope estimates.

### 1.3 What Prompted This Verification

Research file 06 (`06-analysis-doc-verification.md`) cross-validated 19 substantive claims in the analysis document against findings from research files 01–05. Five claims were tagged [CODE-CONTRADICTED]:

| # | Contradicted Claim | What the Code Actually Shows |
|---|-------------------|------------------------------|
| 1 | "Path B: Created by /sc:spec-panel from raw instructions — passing raw instructions causes it to generate a spec through its 11-expert panel" | `sc:spec-panel` explicitly refuses this. Its `Boundaries > Will Not` section states: "Generate specifications from scratch without existing content or context." The command is review-and-improve only. Path B as described does not exist. |
| 2 | "`spec_type` → feeds template type selection (feature/refactoring/migration/infrastructure)" | `spec_type` from spec YAML frontmatter is ignored by all sc:roadmap pipeline logic. Template type is always derived from computed domain distribution (body keyword analysis) or the `--template` CLI flag. The field value is never read. |
| 3 | "`quality_scores` → pipeline quality signals" | `quality_scores` from input spec frontmatter is ignored by sc:roadmap. No extraction step reads it. sc:spec-panel produces its own quality metrics under a different schema and does not write back to this field. There is no bridge between the two schemas. |
| 4 | "The frontmatter advantage is conditional — only exists when spec was manually created from template" (implying the pipeline uses frontmatter values when present) | The pipeline ignores all spec frontmatter field values in all paths. Even a fully-populated frontmatter from the spec template produces identical pipeline behavior to absent frontmatter. The "conditional advantage" does not exist at the pipeline level. |
| 5 | spec-panel output format described as relatively unconstrained in the Path B context | sc:spec-panel has three well-defined output format modes (`--format standard`, `--format structured`, `--format detailed`). Under `--focus correctness`, three artifact types are mandatory hard gates. The primary output is always a structured review document, not a free-form or spec-template-formatted file. |

These five contradictions affect the implementation plan in the following ways: adding frontmatter fields to the TDD template requires simultaneous pipeline changes to be meaningful; sc:spec-panel's TDD-creation capability must be built from zero rather than wired from existing behavior; Option 2 ("modify TDD template only, minimal effort") would produce no pipeline benefit without the same foundational changes Option 3 requires.

---

## Section 2 — Current State Analysis

All findings in this section are [CODE-VERIFIED] against actual source files by the research agents. [CODE-CONTRADICTED] findings from the analysis document are called out explicitly. No architecture is described from documentation alone.

---

### 2.1 sc:spec-panel

**Source file:** `.claude/commands/sc/spec-panel.md` (624 lines)
**Research file:** `01-spec-panel-audit.md`

#### What it does

`sc:spec-panel` routes an existing specification through a fixed panel of 11 simulated domain experts in a fixed review sequence. The 11 experts are: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower — always in this order.

The command produces a structured review document, not a revised spec file. The primary output is always a review document in one of three defined formats:

| Format flag | Description |
|-------------|-------------|
| `--format standard` | YAML-structured review with named blocks: `specification_review`, `quality_assessment`, `critical_issues`, `expert_consensus`, `improvement_roadmap`, `adversarial_analysis` |
| `--format structured` | Token-efficient format using SuperClaude symbol system |
| `--format detailed` | Full expert commentary, examples, and implementation guidance |

Under `--focus correctness`, three artifact types are mandatory hard gates that block synthesis output if incomplete: State Variable Registry, Guard Condition Boundary Table, Pipeline Quantity Flow Diagram.

#### Explicit Boundaries (Will Not)

The `Boundaries > Will Not` section states verbatim: "Generate specifications from scratch without existing content or context." Usage syntax requires `[specification_content|@file]` as a required input parameter. The command does not offer a creation mode.

[CODE-CONTRADICTED from analysis doc] "Path B: Created by /sc:spec-panel from raw instructions" does not exist. This capability must be built from zero; it cannot be wired from existing behavior.

#### Template and sentinel knowledge

- Zero references to `release-spec-template.md`, `tdd_template.md`, `prd_template.md`, or any external template file path in the 624-line command.
- No awareness of the `{{SC_PLACEHOLDER:*}}` sentinel system. "Sentinel" appears 5 times; all occurrences refer to Whittaker's adversarial "Sentinel Collision Attack" (FR-2.3), not the SuperClaude template placeholder system.

#### Frontmatter: what it reads and writes

Does NOT read or write `spec_type`, `complexity_score`, `complexity_class`, or `quality_scores`. Produces its own quality metrics under a different schema with no bridge to the spec template's `quality_scores` block:

| sc:spec-panel metric | Spec template field | Bridge exists? |
|----------------------|--------------------|----|
| `overall_score` (0-10) | `quality_scores.overall` | No |
| `requirements_quality` (0-10) | `quality_scores.completeness` | No |
| `architecture_clarity` (0-10) | (no equivalent field) | No |
| `testability_score` (0-10) | `quality_scores.testability` | No |

#### Companion skill package

No `.claude/skills/sc-spec-panel*/` directory exists. The entire command is a single 624-line `.md` file with no `SKILL.md`, `rules/`, `templates/`, or `refs/` subdirectory.

#### Downstream wiring

| Wiring point | Target | Integration |
|--------------|--------|------------|
| RM-2 | `sc:roadmap` | SP-2 (Whittaker Assumptions) feeds assumption tracking |
| RM-3 | `sc:roadmap` | SP-4 (Quantity Flow Diagram) feeds risk-weighted prioritization |

Integration to `sc:tasklist` is not mentioned anywhere in the file.

---

### 2.2 sc:roadmap-protocol

**Source files:** `.claude/skills/sc-roadmap-protocol/SKILL.md` + `refs/extraction-pipeline.md`, `refs/scoring.md`, `refs/templates.md`, `refs/validation.md`, `refs/adversarial-integration.md`
**Research file:** `02-roadmap-pipeline-audit.md`

#### YAML frontmatter behavior: validate-only

Wave 1B Step 1: "Parse specification file. If spec contains YAML frontmatter, **validate it parses correctly**. If malformed YAML, abort."

This is validation-only. The field values within spec frontmatter are NOT consumed by any extraction step, scoring formula, or template selection algorithm.

[CODE-CONTRADICTED from analysis doc] The following spec frontmatter fields are ignored by all pipeline logic in all paths:
- `spec_type` — ignored; template type derived from computed domain distribution, never from this field
- `complexity_score` — ignored; always recomputed via 5-factor formula
- `complexity_class` — ignored; always derived from computed score
- `quality_scores` — ignored; no extraction step reads them

#### The 8-step extraction pipeline

Executed sequentially in Wave 1B. All steps operate on body text using keyword matching and pattern detection. No step reads YAML frontmatter field values.

| Step | Name | What It Extracts |
|------|------|-----------------|
| 1 | Title & Overview | `project_title`, `project_version`, `summary` from opening H1 / metadata / executive summary |
| 2 | Functional Requirements | Behavioral statements ("shall", "must", "will", "should"), user stories, acceptance criteria. Fields: `id`, `description`, `domain`, `priority` (P0-P3), `source_lines` |
| 3 | Non-Functional Requirements | Performance, security, scalability, reliability, maintainability constraints. Fields: `id`, `description`, `category`, `constraint`, `source_lines` |
| 4 | Scope & Domain Classification | Keyword-weighted domain assignment into 5 domains: Frontend, Backend, Security, Performance, Documentation. Computes domain distribution percentages. |
| 5 | Dependency Extraction | Looks for "requires", "depends on", "after", "before", "blocks". Fields: `id`, `description`, `type` (internal/external), `affected_requirements`, `source_lines` |
| 6 | Success Criteria | Explicit success criteria sections, acceptance criteria, KPIs, metrics. Fields: `id`, `description`, `derived_from`, `measurable`, `source_lines` |
| 7 | Risk Identification | Explicit risks + inferred risks from requirement complexity. Fields: `id`, `description`, `probability`, `impact`, `affected_requirements`, `source_lines` (or "inferred") |
| 8 | ID Assignment | Deterministic IDs by `source_lines` position: `FR-{3digits}`, `NFR-{3digits}`, `DEP-{3digits}`, `SC-{3digits}`, `RISK-{3digits}` |

#### 5-factor complexity scoring formula

Always computed from scratch from extraction outputs. Never reads from spec frontmatter. All factors normalized to [0, 1]:

| Factor | Raw Value Source | Normalization | Weight |
|--------|-----------------|---------------|--------|
| `requirement_count` | Total FRs + NFRs from extraction | `min(count / 50, 1.0)` | 0.25 |
| `dependency_depth` | Max chain in dependency graph | `min(depth / 8, 1.0)` | 0.25 |
| `domain_spread` | Distinct domains with ≥10% representation | `min(domains / 5, 1.0)` | 0.20 |
| `risk_severity` | `(high*3 + medium*2 + low*1) / total_risks` | `(weighted_avg - 1.0) / 2.0` | 0.15 |
| `scope_size` | Total line count of specification | `min(lines / 1000, 1.0)` | 0.15 |

Classification thresholds: LOW < 0.4 → 3-4 milestones, 1:3 interleave; MEDIUM 0.4-0.7 → 5-7 milestones, 1:2 interleave; HIGH > 0.7 → 8-12 milestones, 1:1 interleave.

#### Template type selection

Template type is always derived from computed domain distribution (body-text keyword analysis), NOT from any frontmatter field. The `--template` CLI flag overrides this directly, bypassing scoring entirely. There is no code path where a `spec_type` YAML frontmatter value from the input spec influences template selection.

4-tier template discovery (first match wins):

| Tier | Search Path | Status |
|------|-------------|--------|
| 1 (Local) | `.dev/templates/roadmap/` | Active |
| 2 (User) | `~/.claude/templates/roadmap/` | Active |
| 3 (Plugin) | `~/.claude/plugins/*/templates/roadmap/` | Always no-op (future v5.0) |
| 4 (Inline) | Algorithmic generation from extraction data | Fallback |

#### TDD section capture analysis

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

#### Internal inconsistency in extraction-pipeline.md

In `refs/extraction-pipeline.md`, the worked example tags "Data Models" (Section 6, L581-L700) as `FR_BLOCK`. The stated relevance-tagging heuristic defines `FR_BLOCK` as headings containing "requirement", "feature", "capability", or "functional" — none of which match "Data Models". Under the documented rules, "Data Models" would be tagged `OTHER` and de-prioritized. The same inconsistency applies to "Migration Plan" (tagged `FR_BLOCK` in the worked example, but "migration" is not a `FR_BLOCK` heuristic keyword). The worked example contradicts the documented heuristic at both points.

#### Domain keyword gap

The 5 domain dictionaries are: Frontend, Backend, Security, Performance, Documentation. There is no Testing domain, no DevOps/Ops domain, no Data/ML domain. TDD sections §15 Testing Strategy and §25 Operational Readiness have no matching domain and will be systematically undercounted in complexity scoring.

---

### 2.3 sc:tasklist-protocol

**Source files:** `.claude/skills/sc-tasklist-protocol/SKILL.md` + `rules/tier-classification.md` + `rules/file-emission-rules.md` + `templates/`
**Research file:** `03-tasklist-audit.md`

#### Input contract

SKILL.md Input Contract (lines 47-57) states explicitly: "You receive exactly one input: **the roadmap text**. Treat the roadmap as the **only source of truth**."

| Input | Status |
|-------|--------|
| Roadmap text (primary) | Fully defined and processed |
| `--spec <spec-path>` | Listed in argument-hint frontmatter only; **zero body implementation** — no section, no conditional logic, no processing rule anywhere in SKILL.md |
| `--output <output-dir>` | Listed in argument-hint frontmatter only; **zero body implementation** |

#### TASKLIST_ROOT determination (3-step, roadmap text only)

1. If roadmap text contains `.dev/releases/current/<segment>/` (first match): `TASKLIST_ROOT = .dev/releases/current/<segment>/`
2. Else if roadmap text contains version token `v<digits>(.<digits>)+` (first match): `TASKLIST_ROOT = .dev/releases/current/<version-token>/`
3. Else: `TASKLIST_ROOT = .dev/releases/current/v0.0-unknown/`

The `--output` flag is not wired to TASKLIST_ROOT computation in any case.

#### 11-step generation algorithm

| Step | Name | Summary |
|------|------|---------|
| 4.1 | Parse Roadmap Items | Split at headings, bullets, numbered items; semicolons only when each clause is independently actionable. Each item: deterministic `R-NNN` ID. |
| 4.2 | Determine Phase Buckets | Explicit phase/version/milestone headings; fall back to `##` headings; if none, create 3 defaults. |
| 4.3 | Fix Phase Numbering | Renumber all phases sequentially by appearance order — no gaps preserved ("Missing Phase 8 Rule"). |
| 4.4 | Convert to Tasks | Default 1 task per roadmap item; split only for compound deliverables (new component + migration; feature + test strategy; API + UI; pipeline + application change). |
| 4.5 | Task ID and Ordering | `T<PP>.<TT>` zero-padded. Dependencies may reorder within phase, never across phases. |
| 4.6 | Clarification Tasks | Insert before blocked task when specifics are missing or tier confidence < 0.70. Title formats: `Clarify: <missing detail>` or `Confirm: <task title> tier classification`. |
| 4.7 | Acceptance Criteria | Every task: 1-5 deliverables; 3-8 steps with `[PLANNING]`/`[EXECUTION]`/`[VERIFICATION]`/`[COMPLETION]` markers; exactly 4 AC bullets; exactly 2 validation bullets. |
| 4.8 | Checkpoints | After every 5 tasks within a phase; mandatory at end of every phase. Each: 1 purpose sentence, exactly 3 verification bullets, exactly 3 exit criteria bullets. |
| 4.9 | No Policy Forks | Deterministic tie-breakers for alternatives. Tier conflict priority: STRICT (1) > EXEMPT (2) > LIGHT (3) > STANDARD (4). |
| 4.10 | Verification Routing | STRICT: sub-agent quality-engineer, 3-5K tokens, 60s. STANDARD: direct test, 300-500 tokens, 30s. LIGHT: sanity check, ~100 tokens, 10s. EXEMPT: skip, 0. |
| 4.11 | Critical Path Override | Paths matching `auth/`, `security/`, `crypto/`, `models/`, `migrations/` always force CRITICAL verification regardless of computed tier. |

#### TDD section usage by sc:tasklist

| TDD Section | Currently Used? | Actual Mechanism |
|-------------|----------------|------------------|
| §7 Data Models | Keyword matching only | "schema", "migration", "model", "database" boost STRICT tier. No structural extraction from tables. |
| §8 API Specifications | Keyword matching only | "api contract", "query", "transaction" boost STRICT. No endpoint table parsing. |
| §10 Component Inventory | Not at all | No structured handling; new/modified/deleted categorization unused. |
| §15 Testing Strategy | Keyword matching only | "tests/" path boosts STANDARD. No test suite name or coverage target extraction. |
| §19 Migration & Rollout | Partially (keywords + split rule) | "migration", "rollback", "deploy" boost STRICT/risk. Split rule 4.4 handles pipeline + application changes. Phase sequences not extracted. |
| §24 Release Criteria | Not at all | No structural extraction of release gates or sign-off conditions. |

The post-generation validation pipeline (Stages 7-10) uses 2N parallel agents that validate against the roadmap only. No instructions exist to validate against a spec or TDD.

---

### 2.4 TDD Template

**Source file:** `src/superclaude/examples/tdd_template.md` (1,309 lines, template version 1.2, last updated 2026-02-11)
**Research file:** `04-tdd-template-audit.md`

#### All 27 YAML frontmatter fields

| Field | Type/Format | Default/Placeholder |
|-------|-------------|---------------------|
| `id` | string | `"[COMPONENT-ID]-TDD"` |
| `title` | string | `"[Component Name] - Technical Design Document"` |
| `description` | string | Long placeholder paragraph |
| `version` | string | `"1.2"` |
| `status` | string (emoji-prefixed) | `"🟡 Draft"` |
| `type` | string (emoji-prefixed) | `"📐 Technical Design Document"` |
| `priority` | string (emoji-prefixed) | `"🔥 Highest"` |
| `created_date` | date string | `"YYYY-MM-DD"` |
| `updated_date` | date string | `"YYYY-MM-DD"` |
| `assigned_to` | string | `"[engineering-team]"` |
| `autogen` | boolean | `false` |
| `coordinator` | string | `"[tech-lead]"` |
| `parent_doc` | string | `"[link to Product PRD...]"` |
| `depends_on` | list | `["[list dependent documents/components]"]` |
| `related_docs` | list | `["[list related documents]"]` |
| `tags` | list | `["technical-design-document", "[component-type]", "architecture", "specifications"]` |
| `template_schema_doc` | string | `""` (empty) |
| `estimation` | string | `""` (empty) |
| `sprint` | string | `""` (empty) |
| `due_date` | string | `""` (empty) |
| `start_date` | string | `""` (empty) |
| `completion_date` | string | `""` (empty) |
| `blocker_reason` | string | `""` (empty) |
| `review_info.last_reviewed_by` | string | `""` (empty) |
| `review_info.last_review_date` | string | `""` (empty) |
| `review_info.next_review_date` | string | `""` (empty) |
| `approvers.tech_lead` / `.engineering_manager` / `.architect` / `.security` | string (×4) | `""` (empty) |

#### Spec template frontmatter fields absent from TDD template

| Field | In Spec Template | In TDD Template | Pipeline impact of absence |
|-------|-----------------|-----------------|---------------------------|
| `feature_id` | Yes | No | No equivalent; no pipeline impact (field not read) |
| `spec_type` | Yes (enum: 4 values) | No | sc:roadmap ignores even when present; adding would require pipeline upgrade |
| `complexity_score` | Yes (float 0.0-1.0) | No | sc:roadmap ignores even when present; always recomputes |
| `complexity_class` | Yes (enum LOW/MEDIUM/HIGH) | No | sc:roadmap ignores even when present; always derives from score |
| `target_release` | Yes (version string) | No (has `due_date` + `sprint` instead) | No pipeline impact (field not read) |
| `authors` | Yes (list) | No (has `coordinator` + `assigned_to`) | No pipeline impact |
| `quality_scores.clarity` through `.overall` (×5) | Yes | No | sc:roadmap ignores even when present; sc:spec-panel uses different schema |
| `parent_feature` | Yes | No (has `parent_doc` — different semantics) | No pipeline impact |

#### All 28 numbered TDD sections

| # | Title | Content Type | Conditional? |
|---|-------|-------------|--------------|
| 1 | Executive Summary | Narrative + Key Deliverables list | No |
| 2 | Problem Statement & Context | Background, problem, business context, PRD reference | No |
| 3 | Goals & Non-Goals | Goal/non-goal/future tables with success criteria | No |
| 4 | Success Metrics | Technical + business KPI tables with baseline/target/measurement | 4.2 conditional |
| 5 | Technical Requirements | FR table (ID/priority/ACs); NFR sub-tables | No |
| 6 | Architecture | Mermaid/ASCII diagrams, boundary table, design decisions | 6.5 conditional |
| 7 | Data Models | TypeScript interfaces + field tables, Mermaid flowchart, storage table | No |
| 8 | API Specifications | Endpoint tables, request/response, error format, versioning policy | No |
| 9 | State Management | State tool table, TS state interfaces, transition table | Frontend-only conditional |
| 10 | Component Inventory | Route table, component table, hierarchy ASCII tree | Frontend-only conditional |
| 11 | User Flows & Interactions | Mermaid sequence diagrams, step lists, success criteria, error scenarios | No |
| 12 | Error Handling & Edge Cases | Error category table, edge case table, degradation table, retry table | No |
| 13 | Security Considerations | Threat table, controls table, data classification table | 13.4 conditional |
| 14 | Observability & Monitoring | Log table, metrics table, trace spans, alert table, dashboard links | 14.6 conditional |
| 15 | Testing Strategy | Test pyramid table, unit/integration/E2E test case tables, environment table | No |
| 16 | Accessibility Requirements | WCAG 2.1 AA requirements table, testing tools | No |
| 17 | Performance Budgets | Core Web Vitals/bundle table, API latency table, load test plan | No |
| 18 | Dependencies | External/internal/infrastructure tables with version/purpose/risk/fallback | No |
| 19 | Migration & Rollout Plan | Migration phase table, feature flag table with lifecycle, rollout stage table, rollback steps | No |
| 20 | Risks & Mitigations | Risk table: ID/description/probability/impact/mitigation/contingency | No |
| 21 | Alternatives Considered | Alt 0 (Do Nothing, mandatory) + alternatives with pros/cons/why-not-chosen | No |
| 22 | Open Questions | Table: ID/question/owner/target date/status/resolution | No |
| 23 | Timeline & Milestones | Milestone table, phase deliverables checklists | No |
| 24 | Release Criteria | 13-item Definition of Done checklist, 9-item release checklist | No |
| 25 | Operational Readiness | Runbook scenario table, on-call table, capacity projection table | No |
| 26 | Cost & Resource Estimation | Cost table, scaling model table, optimization opportunities | Conditional |
| 27 | References & Resources | Related doc table, external reference table | No |
| 28 | Glossary | Term/definition table | No |

---

### 2.5 PRD and TDD Skills

**Source files:** `.claude/skills/prd/SKILL.md` (1,373 lines), `.claude/skills/tdd/SKILL.md` (1,344 lines)
**Research file:** `05-prd-tdd-skills-audit.md`

#### PRD skill: output path and 7-phase pipeline

Final PRD output path: `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md`

| Phase | Name | Key Activity |
|-------|------|-------------|
| Phase 1 | Preparation | Status update, scope confirmation, template read, tier selection, folder creation |
| Phase 2 | Deep Investigation | Parallel subagents: Feature Analyst, Doc Analyst, Integration Mapper, UX Investigator, Architecture Analyst — write to `${TASK_DIR}research/` |
| Phase 3 | Completeness Verification | rf-analyst + rf-qa in parallel; PASS/FAIL gate blocks progression |
| Phase 4 | Web Research | Competitive landscape, market sizing, industry standards, tech trends |
| Phase 5 | Synthesis + QA Gate | Parallel synthesis agents (one per synth file, 9 total); rf-analyst + rf-qa synthesis gate in parallel |
| Phase 6 | Assembly & Validation | rf-assembler → rf-qa report-validation → rf-qa-qualitative |
| Phase 7 | Present to User & Complete | Offer downstream TDD creation: "Would you like me to create a TDD using the `/tdd` skill? The research files are already in place." |

The PRD produces 9 synthesis files (synth-01 through synth-09) covering all 28 PRD sections. The two synthesis files most directly relevant to TDD handoff are: `synth-04-stories-requirements.md` (S21.1 Epics/Stories/ACs, S21.2 Product Requirements RICE matrix) and `synth-07-metrics-risk-impl.md` (S19 Success Metrics, S21.3-21.5 Phasing/Release Criteria/Timeline).

#### TDD skill: PRD_REF field

`PRD_REF` is one of the four input fields captured at Step A.2 (Parse & Triage). Definition: "A Product Requirements Document that this TDD implements. When provided, the TDD extracts relevant epics, user stories, acceptance criteria, technical requirements, and success metrics from the PRD as foundational context."

`PRD_REF` is optional but strongly recommended. When provided, the sufficiency gate (A.5 item 7) is a mandatory gate: if PRD_CONTEXT is empty when a PRD was provided, scope discovery must be redone.

#### 00-prd-extraction.md artifact

| Property | Value |
|----------|-------|
| File path | `${TASK_DIR}research/00-prd-extraction.md` |
| When created | Phase 2, first checklist item, before all parallel codebase research agents begin |
| Numbering | Prefix `00` places it before all other research files in the sequence |
| Agent prompt defined? | No — no named `PRD Extraction Agent Prompt` template exists anywhere in TDD SKILL.md (Gap 1) |

#### 4 synthesis files that read 00-prd-extraction.md

| Synth File | TDD Sections Covered |
|------------|---------------------|
| `synth-01-exec-problem-goals.md` | S1 Executive Summary, S2 Problem Statement, S3 Goals & Non-Goals, S4 Success Metrics |
| `synth-02-requirements.md` | S5 Technical Requirements |
| `synth-08-perf-deps-migration.md` | S16 Accessibility, S17 Performance, S18 Dependencies, S19 Migration |
| `synth-09-risks-alternatives-ops.md` | S20 Risks, S21 Alternatives, S22 Open Questions, S23 Timeline, S24 Release, S25 Ops, S26 Cost |

#### 5 synthesis files that do NOT read 00-prd-extraction.md

| Synth File | TDD Sections Not Fed by PRD |
|------------|----------------------------|
| `synth-03-architecture.md` | S6 Architecture |
| `synth-04-data-api.md` | S7 Data Models, S8 API Specifications |
| `synth-05-state-components.md` | S9 State Management, S10 Component Inventory |
| `synth-06-error-security.md` | S11 User Flows, S12 Error Handling, S13 Security |
| `synth-07-observability-testing.md` | S14 Observability, S15 Testing Strategy |

#### 6 PRD-to-TDD handoff gaps

| Gap # | Description | Evidence Location |
|-------|-------------|-------------------|
| Gap 1 | No PRD extraction agent prompt template defined. Phase 2 says "first item extracts PRD context to 00-prd-extraction.md" but no named agent prompt template exists. Task builder must invent format and structure. | TDD SKILL.md Phase 2 encoding; absence confirmed across all 8 named agent prompt templates |
| Gap 2 | 5 of 9 synthesis files (synth-03 through synth-07) do not list PRD extraction as a source. Architecture, Data Models, API Specs, User Flows, Error Handling, Security, and Testing are produced without seeing PRD acceptance criteria. | TDD SKILL.md Phase 5 Synthesis Mapping Table |
| Gap 3 | No explicit AC-to-FR mapping instruction. Synthesis prompt has no rule requiring traceability matrices or PRD story ID labeling on requirements. | TDD SKILL.md Synthesis Agent Prompt rule set |
| Gap 4 | PRD acceptance criteria not explicitly ported to TDD functional requirements. No instruction to read each PRD user story AC and map it to a FR-NNN item. QA Synthesis Gate checklist (12 items) does not check PRD traceability. | TDD SKILL.md synth-02 instructions; QA Synthesis Gate checklist |
| Gap 5 | No KPI translation instruction. synth-01 lists PRD extraction as a source for S4 Success Metrics but no synthesis rule instructs "translate PRD KPIs into engineering proxy metrics." rf-qa-qualitative does not check metric alignment. | TDD SKILL.md synth-01 instructions; rf-qa-qualitative prompt |
| Gap 6 | PRD-to-TDD Pipeline section (lines 1315-1326) is reference documentation, not enforced. Its 5-point pipeline (extraction, traceability, metrics alignment, scope inheritance, cross-referencing) is not in BUILD_REQUEST, synthesis prompts, or any QA gate checklist. | TDD SKILL.md lines 1315-1326 |

---

### 2.6 Current State Summary

The actual pipeline based on verified code findings only. No architecture described from documentation.

```
User Input
    │
    ├── /prd (.claude/skills/prd/SKILL.md, 1373 lines)
    │       Accepts: feature description or PRD request
    │       Output: docs/docs-product/tech/[name]/PRD_[NAME].md
    │       Phase 7: manually offers TDD creation to user (user must respond)
    │
    ├── /tdd (.claude/skills/tdd/SKILL.md, 1344 lines)
    │       Accepts: feature description + optional PRD_REF
    │       If PRD_REF:
    │         - Stage A: reads PRD, writes PRD_CONTEXT to research-notes.md
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
            Accepts: spec file (any format)
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

**Summary of verified pipeline facts:**

| Component | Verified Fact | Source |
|-----------|--------------|--------|
| sc:spec-panel | Cannot create specs from scratch (explicit Boundaries Will Not) | `01-spec-panel-audit.md` §3.5 |
| sc:spec-panel | Zero template/sentinel file references in 624 lines | `01-spec-panel-audit.md` §3.1, §3.3 |
| sc:spec-panel | No companion skill directory exists | `01-spec-panel-audit.md` §1 |
| sc:roadmap | Frontmatter field values ignored in all paths (validate-only) | `02-roadmap-pipeline-audit.md` §1, §3, §4 |
| sc:roadmap | Template type from domain keyword analysis, not `spec_type` | `02-roadmap-pipeline-audit.md` §4 |
| sc:roadmap | 5-factor formula always recomputes; never reads `complexity_score` | `02-roadmap-pipeline-audit.md` §3 |
| sc:roadmap | §24 Release Criteria is the only TDD section fully captured | `02-roadmap-pipeline-audit.md` §2 |
| sc:roadmap | Worked example in extraction-pipeline.md contradicts documented heuristic (Data Models, Migration Plan tagging) | `02-roadmap-pipeline-audit.md` §2 |
| sc:tasklist | `--spec` flag declared in argument-hint only; zero body implementation | `03-tasklist-audit.md` §1, §8 |
| sc:tasklist | TASKLIST_ROOT derived from roadmap text; `--output` flag unimplemented | `03-tasklist-audit.md` §4 |
| TDD template | 27 frontmatter fields; none of the spec's pipeline-oriented fields present | `04-tdd-template-audit.md` §1.1 |
| TDD template | 28 numbered sections; 6 conditional | `04-tdd-template-audit.md` §1.2 |
| TDD skill | 00-prd-extraction.md created in Phase 2 before parallel research | `05-prd-tdd-skills-audit.md` §2.6 |
| TDD skill | 5 of 9 synthesis files do not read PRD extraction | `05-prd-tdd-skills-audit.md` §2.7, Gap 2 |
| TDD skill | PRD-to-TDD Pipeline section (lines 1315-1326) is unenforced | `05-prd-tdd-skills-audit.md` §2.8, Gap 6 |

---

**Status:** Complete
