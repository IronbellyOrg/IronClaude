# Research: TDD Template Structure Analysis

**Investigation type:** Doc Analyst
**Scope:** src/superclaude/examples/tdd_template.md
**Status:** Complete
**Date:** 2026-03-25

---

## Main Capture Map — All 28 TDD Sections

Current `build_extract_prompt()` instructs 8 body sections only: Functional Requirements, Non-Functional Requirements, Complexity Assessment, Architectural Constraints, Risk Inventory, Dependency Inventory, Success Criteria, Open Questions.

| Section # | Section Name | Content Format | Verdict | Required Extraction Instruction for TDD Prompt |
|---|---|---|---|---|
| 1 | Executive Summary | Narrative + key deliverables bullet list | PARTIAL | Extract concise component summary, intended deliverables, and stated purpose even when not phrased as requirements |
| 2 | Problem Statement & Context | Narrative subsections + PRD/business references | PARTIAL | Extract problem context, affected actors/systems, business drivers, upstream PRD references as implementation context |
| 3 | Goals & Non-Goals | Goal table, non-goal table, future considerations table | PARTIAL | Add extraction: "Extract goals, non-goals, and deferred future work from tables; preserve IDs like G1/NG1 if present" |
| 4 | Success Metrics | Technical metrics table + business KPI mapping table | PARTIAL | Extract baseline/target/measurement triples from metric tables; preserve business KPI to technical proxy mappings |
| 5 | Technical Requirements | FR table with IDs + acceptance criteria; NFR criteria tables | CAPTURED | Current prompt should capture FR/NFR content; TDD prompt should explicitly parse markdown tables and preserve all columns |
| 6 | Architecture | ASCII diagram, mermaid diagram, boundary table, decision table, multi-tenancy table/checklist | PARTIAL | Add explicit extraction for system boundaries, design decisions, tenancy model, checklist-style guarantees as architecture artifacts |
| 7 | Data Models | TypeScript interfaces in fenced code blocks + field tables + mermaid flowchart + storage table | MISSED | "Extract entities, fields, types, constraints, relationships, storage/retention/backup strategy, and data-flow steps from code blocks and tables" |
| 8 | API Specifications | Endpoint overview table, request/response examples, param tables, error tables, versioning/governance tables | MISSED | "Extract endpoint inventory, methods, paths, auth, params, request/response schemas, error codes, versioning and deprecation policy from tables/code blocks even without behavioral language" |
| 9 | State Management | State tool/library table + TypeScript state interfaces + transition table | MISSED | "Extract state stores, state shape, transitions, triggers, and side effects from interface blocks and state tables" |
| 10 | Component Inventory | Route table, shared component table, ASCII hierarchy tree | MISSED | "Extract routes, page components, shared components, props interfaces, source locations, and component hierarchy from tables and trees" |
| 11 | User Flows & Interactions | Mermaid sequence diagram + numbered steps + success criteria + error scenario bullets | PARTIAL | Extract interaction flows as ordered sequences, participants, success criteria, and error scenarios; parse diagrams as flow metadata |
| 12 | Error Handling & Edge Cases | Error category table, edge-case table, graceful degradation table, retry strategy table | PARTIAL | "Extract error categories, expected behaviors, retries, fallback mechanisms, and recovery strategies from structured tables" |
| 13 | Security Considerations | Threat model table, controls table, sensitive-data table, compliance table, checklist | PARTIAL | "Extract threats, controls, data classifications, regulatory obligations, and verification methods from all security tables/checklists" |
| 14 | Observability & Monitoring | Logging/metrics/tracing/alerts/dashboard tables + business event instrumentation table | PARTIAL | "Extract logs, metrics, labels, alert thresholds, traces, dashboards, and business instrumentation mappings" |
| 15 | Testing Strategy | Test pyramid table, unit/integration/E2E case tables, environment table | MISSED | "Extract test levels, coverage targets, tools, concrete test cases, and environment matrix from test strategy tables" |
| 16 | Accessibility Requirements | WCAG standard + requirements table + testing tools bullets | PARTIAL | Extract accessibility standard, requirement rows, implementations, and testing methods as NFR/accessibility requirements |
| 17 | Performance Budgets | Frontend/backend performance budget tables + performance testing table | PARTIAL | Extract budget thresholds, measurement methods, and performance test cadence as structured performance requirements |
| 18 | Dependencies | External/internal/infrastructure dependency tables | CAPTURED | Current Dependency Inventory should capture this; TDD prompt should parse dependency tables and preserve risk/fallback/interface columns |
| 19 | Migration & Rollout Plan | Phase table, feature-flag table, ASCII lifecycle pipeline, rollout stage table, rollback steps/bullets | PARTIAL | "Extract migration phases, rollout stages, feature flags, rollback procedures, rollback triggers, and ordering/dependency implications" |
| 20 | Risks & Mitigations | Risk table with probability/impact/mitigation/contingency | CAPTURED | Current Risk Inventory should capture this; preserve probability/impact columns explicitly |
| 21 | Alternatives Considered | Narrative alternatives with pros/cons and "Why Not Chosen" | PARTIAL | "Extract rejected alternatives including mandatory Alternative 0 (Do Nothing) with pros/cons and rejection rationale" |
| 22 | Open Questions | Open question table with owner/date/status/resolution | CAPTURED | Current Open Questions should capture this; preserve ownership, due date, status, resolution fields |
| 23 | Timeline & Milestones | Milestone table + phase subsections + deliverables checklist + exit criteria bullets | PARTIAL | "Extract milestones, target dates, dependencies, implementation phases, deliverables, and exit criteria" |
| 24 | Release Criteria | Definition of Done checklist + release checklist | CAPTURED | Current Success Criteria extraction should capture most of this; preserve checklist items as release gates |
| 25 | Operational Readiness | Runbook scenario table, on-call expectations table, capacity planning table | MISSED | "Extract runbook scenarios, diagnosis/resolution steps, on-call expectations, response SLAs, and capacity/scaling triggers" |
| 26 | Cost & Resource Estimation | Infrastructure cost table, scaling model table, optimization opportunities table | MISSED | "Extract resource cost models, scaling economics, cost drivers, and optimization opportunities" |
| 27 | References & Resources | Related docs table + external references table | PARTIAL | "Extract related documents, ADRs, runbooks, external standards, and links as supporting references" |
| 28 | Glossary | Term/definition table | MISSED | "Extract glossary terms and definitions to preserve domain vocabulary for downstream roadmap/tasklist use" |

---

## Counts

| Verdict | Count | Sections |
|---|---|---|
| CAPTURED | 5 | §5, §18, §20, §22, §24 |
| PARTIAL | 15 | §1, §2, §3, §4, §6, §11, §12, §13, §14, §16, §17, §19, §21, §23, §27 |
| MISSED | 8 | §7, §8, §9, §10, §15, §25, §26, §28 |

---

## (b) §5 FR Format Analysis

### Does TDD §5 use FR-xxx IDs compatible with `spec_parser.extract_requirement_ids()`?

**YES.** TDD template §5.1 uses: `FR-001`, `FR-002`, `FR-003`, `FR-004`

`spec_parser.py` regex: `r'\bFR-\d+(?:\.\d+)?\b'`

**Compatible.** Supports `FR-001` and `FR-001.1` but not deeper chains like `FR-001.1.2` (not present in template).

---

## (c) TDD Frontmatter `type` Field

**YES.** TDD YAML frontmatter has a `type` field.

**Exact value:** `"📐 Technical Design Document"`

Strong human-readable discriminator. Current CLI does NOT use frontmatter type for detection or branching.

---

## (d) Does TDD Have `spec_type` or Equivalent?

**NO.** The TDD template does not include a `spec_type` field, nor any field that maps to the spec template's `spec_type` enum.

It has: `type: "📐 Technical Design Document"`

Without pipeline changes, the CLI would not reliably detect TDD-ness from schema-driven detection. The `type` field value could serve as an auto-detection basis if the executor reads it.

---

## (e) §7 Data Models — Detailed Analysis

### Format
- TypeScript interfaces in fenced code blocks: `interface EntityName { field: Type; }`
- Field definition tables: `| Field | Type | Required | Description | Constraints |`
- Mermaid data-flow flowchart
- Storage/retention/backup table

### Would current prompt capture as Architectural Constraints?
Mostly NO. The extract prompt's "Architectural Constraints" section targets technology mandates and integration boundaries, not entity definitions and field schemas.

### What spec_parser.py extracts
- `extract_code_blocks()` captures TypeScript fenced blocks as `CodeBlock` objects
- `extract_tables()` captures field tables as `MarkdownTable` objects
- BUT `extract_function_signatures()` only parses Python `def/class` — TypeScript `interface` NOT extracted to `function_signatures`

### Conclusion: MISSED — requires dedicated extraction instruction

---

## (f) §8 API Specifications — Detailed Analysis

### Format
- Endpoint overview table (Method | Path | Auth | Description | Rate Limit)
- Per-endpoint detail: request examples, query param tables, response schema examples, error response tables
- Versioning/governance compatibility tables
- Deprecation policy tables

### Would current prompt capture as Functional Requirements?
Partially. Behavioral text like "Purpose: [What this endpoint does]" might produce an FR. But the core contract (method, path, auth, params, request/response shape, error codes, versioning rules, deprecation schedule) is entirely structural — not captured.

### Conclusion: MISSED — requires dedicated API contract extraction instruction

---

## (g) §10 Component Inventory — Detailed Analysis

### Format
- Route table (Route | Component | Auth Required | Description)
- Shared component table (Component | Props | Usage | Location)
- ASCII component hierarchy tree (`App → Layout → Header → ...`)

### Conclusion: MISSED — none of this maps to FRs, NFRs, constraints, risks, dependencies, or success criteria

---

## (h) §15 Testing Strategy — Detailed Analysis

### Format
- Test pyramid breakdown table (Level | Tools | Coverage Target | Ownership)
- Unit test case table (Test Case | Input | Expected Output | Mocks)
- Integration test case table (similar structure)
- E2E test case table (similar structure)
- Test environment matrix

### Would current prompt capture as NFRs?
Minimally. Coverage targets might appear as NFR coverage requirements. But the concrete test case tables, tooling specifics, and environment matrix are not captured.

### Conclusion: MISSED — highest value for CLI task generation (test validation steps should come from §15)

---

## (i) §19 Migration & Rollout Plan — Detailed Analysis

### Format
- Migration phase table (Phase | Tasks | Duration | Dependencies | Rollback)
- Feature flag table (Flag | Purpose | Status | Cleanup Date | Owner)
- ASCII feature-flag lifecycle pipeline
- Rollout stage table (Stage | Target | Success Criteria | Monitoring | Rollback Trigger)
- Numbered rollback procedure (ordered steps)
- Rollback decision criteria (bullet list with triggers)

### Implies task dependencies?
YES — staged phases, rollout percentages, rollback triggers, and ordered rollback steps encode sequencing and dependency information.

### Conclusion: PARTIAL — some behavioral content captured; rollout procedure, stage ordering, procedural dependencies missed

---

## (j) §25 Operational Readiness — Detailed Analysis

### Format
- Runbook scenario table (Scenario | Symptoms | Diagnosis | Resolution | Escalation | Prevention)
- On-call expectations table (Scenario | Page Volume | MTTD | MTTR | Knowledge Prerequisites)
- Capacity planning table (Metric | Current | 3-Month | 6-Month | Scaling Trigger | Action)

### Would current prompt capture?
Very little. A few scaling triggers might appear as NFRs. Most of the section concerns operational ownership and production readiness — entirely outside current extraction scope.

### Conclusion: MISSED — operational runbooks are important for sprint task generation (post-launch verification tasks)

---

## Gaps and Questions

1. Auto-detection: TDD has `type: "📐 Technical Design Document"` but no `spec_type` field; pipeline could auto-detect by reading frontmatter `type` before building the extract prompt (Option B)
2. If `build_extract_prompt_tdd()` is added, should it replace the 8-section contract or extend it? Safest: preserve current 8 outputs + add TDD-specific sections
3. §9 State Management and §10 Component Inventory are frontend-conditional in the TDD template — extraction instructions should handle conditional sections gracefully
4. §26 Cost & Resource Estimation is also conditional — low priority for implementation

## Summary

**5 CAPTURED sections** — §5 Technical Requirements (FR/NFR), §18 Dependencies, §20 Risks, §22 Open Questions, §24 Release Criteria

**15 PARTIAL sections** — useful content exists but structured non-behavioral elements (tables, diagrams, checklists) are partially or unreliably captured

**8 MISSED sections** — §7 Data Models (TypeScript interfaces), §8 API Specifications (endpoint tables), §9 State Management (state machine tables), §10 Component Inventory (route/component tables), §15 Testing Strategy (test case tables), §25 Operational Readiness (runbook tables), §26 Cost Estimation, §28 Glossary

The current `build_extract_prompt()` is suitable for requirement-centric spec extraction but not for native TDD extraction. It captures behavioral requirement prose and some tabular NFR/risk/dependency content, but omits the core structural artifacts that make a TDD valuable: interfaces, endpoint contracts, state models, component inventories, test matrices, rollout procedures, and operational runbooks. A TDD-aware `build_extract_prompt_tdd()` must add explicit extraction sections for these 8 missed areas.
