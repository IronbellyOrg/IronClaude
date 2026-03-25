# Research: TDD Template and Spec Template Full Audit

**Investigation type:** Doc Analyst
**Scope:** tdd_template.md, release-spec-template.md
**Status:** Complete
**Date:** 2026-03-24

---

## Part 1: TDD Template Full Audit (`src/superclaude/examples/tdd_template.md`)

**File size:** 1,309 lines
**Template version:** 1.2
**Template created:** 2025-11-27
**Template updated:** 2026-02-11
**Based on:** Google Design Docs, Stripe API Governance, HashiCorp RFCs, Google SRE Production Readiness, Pragmatic Engineer RFCs, IEEE SRS, AWS SaaS Lens, FinOps Foundation, SLODLC

---

### 1.1 YAML Frontmatter Fields

| Field | Type/Format | Default/Placeholder | Purpose |
|-------|-------------|---------------------|---------|
| `id` | string | `"[COMPONENT-ID]-TDD"` | Unique document identifier following naming convention `[COMPONENT-ID]-TDD` |
| `title` | string | `"[Component Name] - Technical Design Document"` | Human-readable document title |
| `description` | string | long string | Short paragraph describing what the TDD covers |
| `version` | string | `"1.2"` | Document version number |
| `status` | string (emoji-prefixed) | `"🟡 Draft"` | Lifecycle status: Draft / In Review / Approved / Implementing / Complete |
| `type` | string (emoji-prefixed) | `"📐 Technical Design Document"` | Document type classification |
| `priority` | string (emoji-prefixed) | `"🔥 Highest"` | Priority level |
| `created_date` | date string | `"YYYY-MM-DD"` | ISO date document was created |
| `updated_date` | date string | `"YYYY-MM-DD"` | ISO date of last update |
| `assigned_to` | string | `"[engineering-team]"` | Team responsible for this TDD |
| `autogen` | boolean | `false` | Whether this was auto-generated |
| `coordinator` | string | `"[tech-lead]"` | Tech lead coordinating this TDD |
| `parent_doc` | string | `"[link to Product PRD...]"` | Link to the product PRD this TDD implements |
| `depends_on` | list of strings | `["[list dependent documents/components]"]` | Documents/components this TDD depends on |
| `related_docs` | list of strings | `["[list related documents]"]` | Related documents |
| `tags` | list of strings | `["technical-design-document", "[component-type]", "architecture", "specifications"]` | Classification tags |
| `template_schema_doc` | string | `""` | Empty — link to schema doc if used |
| `estimation` | string | `""` | Empty — effort estimation |
| `sprint` | string | `""` | Empty — target sprint |
| `due_date` | string | `""` | Empty — due date |
| `start_date` | string | `""` | Empty — start date |
| `completion_date` | string | `""` | Empty — completion date |
| `blocker_reason` | string | `""` | Empty — reason if blocked |
| `review_info.last_reviewed_by` | string | `""` | Empty — last reviewer |
| `review_info.last_review_date` | string | `""` | Empty — date of last review |
| `review_info.next_review_date` | string | `""` | Empty — next scheduled review |
| `approvers.tech_lead` | string | `""` | Empty — tech lead approver name |
| `approvers.engineering_manager` | string | `""` | Empty — EM approver name |
| `approvers.architect` | string | `""` | Empty — architect approver name |
| `approvers.security` | string | `""` | Empty — security approver name |

**Total frontmatter fields:** 27 (including nested sub-fields under `review_info` and `approvers`)

**Notable absences vs. pipeline-oriented fields:** No `feature_id`, no `spec_type`, no `complexity_score`, no `complexity_class`, no `target_release` (has `due_date` which is empty), no `quality_scores` block, no `authors` list.

---

### 1.2 Section Inventory (All 28 Numbered Sections + Preamble)

| # | Heading | Subsections | Content Expected | Conditional? |
|---|---------|-------------|-----------------|--------------|
| — | Document Lifecycle Position | — | Table showing PRD → TDD → Tech Ref phases | No |
| — | Tiered Usage | — | Table: Lightweight / Standard / Heavyweight tiers with required sections | No |
| — | Document Information | — | Key-value table: Component Name, Type, Tech Lead, Team, Maintained By, Target Release, Last Verified, Status | No |
| — | Approvers | — | Table: Role / Name / Status / Date for 4 approvers | No |
| — | Completeness Status | — | 28-item checkbox checklist + contract table | No |
| — | Table of Contents | — | Links to all 28 sections | No |
| 1 | Executive Summary | — | 2-3 paragraphs max + Key Deliverables bullet list | No |
| 2 | Problem Statement & Context | 2.1 Background, 2.2 Problem Statement, 2.3 Business Context | Context narrative, core problem statement, PRD reference, business/user impact | No |
| 3 | Goals & Non-Goals | 3.1 Goals, 3.2 Non-Goals, 3.3 Future Considerations | Tables of Goals (with success criteria), Non-Goals (with rationale), deferred items | No |
| 4 | Success Metrics | 4.1 Technical Metrics, 4.2 Business Metrics* | Metric/baseline/target/measurement tables; business KPI proxy metrics | 4.2 is conditional |
| 5 | Technical Requirements | 5.1 Functional Requirements, 5.2 Non-Functional Requirements | FR table with ID/priority/acceptance criteria; Performance/Scalability/Reliability/SLOs/Security sub-tables | No |
| 6 | Architecture | 6.1 High-Level Architecture, 6.2 Component Diagram, 6.3 System Boundaries, 6.4 Key Design Decisions, 6.5 Multi-Tenancy* | Diagrams (Mermaid/ASCII), boundary table, design decisions table | 6.5 conditional |
| 7 | Data Models | 7.1 Data Entities, 7.2 Data Flow, 7.3 Data Storage | TypeScript interfaces + field tables, Mermaid flowchart, storage retention table | No |
| 8 | API Specifications | 8.1 API Overview, 8.2 Endpoint Details, 8.3 Error Response Format, 8.4 API Governance & Versioning | Endpoint tables, request/response examples, error format, versioning policy, deprecation policy | No |
| 9 | State Management | 9.1 State Architecture, 9.2 State Shape, 9.3 State Transitions | Frontend only — state tool table, TypeScript state interfaces, transition table | Conditional: frontend only |
| 10 | Component Inventory | 10.1 Page/Route Structure, 10.2 Shared Components, 10.3 Component Hierarchy | Frontend only — route table, component table, hierarchy ASCII tree | Conditional: frontend only |
| 11 | User Flows & Interactions | 11.1 Primary User Flow, 11.2 Secondary User Flow | Mermaid sequence diagrams, step lists, success criteria, error scenarios | No |
| 12 | Error Handling & Edge Cases | 12.1 Error Categories, 12.2 Edge Cases, 12.3 Graceful Degradation, 12.4 Retry & Recovery Strategies | Category tables, edge case table, degradation table, retry table | No |
| 13 | Security Considerations | 13.1 Threat Model, 13.2 Security Controls, 13.3 Sensitive Data Handling, 13.4 Data Governance & Compliance* | Threat table, controls table, data classification table, compliance table | 13.4 conditional |
| 14 | Observability & Monitoring | 14.1 Logging, 14.2 Metrics, 14.3 Tracing, 14.4 Alerts, 14.5 Dashboards, 14.6 Business Metric Instrumentation* | Log table, metrics table, trace spans, alert table, dashboard links, event mapping | 14.6 conditional |
| 15 | Testing Strategy | 15.1 Test Pyramid, 15.2 Test Cases, 15.3 Test Environments | Level/coverage/tools table, unit/integration/E2E test case tables, environment table | No |
| 16 | Accessibility Requirements | 16.1 Requirements, 16.2 Testing Tools | WCAG 2.1 AA requirements table, tools list | No |
| 17 | Performance Budgets | 17.1 Frontend Performance, 17.2 Backend Performance, 17.3 Performance Testing | Core Web Vitals / bundle size table, API latency/resource table, load test plan table | No |
| 18 | Dependencies | 18.1 External, 18.2 Internal, 18.3 Infrastructure | Dependency tables with version/purpose/risk/fallback; internal service table; infra resource table | No |
| 19 | Migration & Rollout Plan | 19.1 Migration Strategy, 19.2 Feature Flags & Progressive Delivery, 19.3 Rollout Stages, 19.4 Rollback Procedure | Migration phase table, feature flag table with lifecycle, rollout stage table, numbered rollback steps | No |
| 20 | Risks & Mitigations | — | Risk table: ID/description/probability/impact/mitigation/contingency | No |
| 21 | Alternatives Considered | Alt 0 (Do Nothing, mandatory), Alt 1, Alt 2 | Pros/cons/why-not-chosen for each alternative | No |
| 22 | Open Questions | — | Table: ID/question/owner/target date/status/resolution | No |
| 23 | Timeline & Milestones | 23.1 High-Level Timeline, 23.2 Implementation Phases | Milestone table, phase deliverables checklists | No |
| 24 | Release Criteria | 24.1 Definition of Done, 24.2 Release Checklist | 13-item DoD checklist, 9-item release checklist | No |
| 25 | Operational Readiness | 25.1 Runbook, 25.2 On-Call Expectations, 25.3 Capacity Planning | Runbook scenario table, on-call table, capacity projection table | No |
| 26 | Cost & Resource Estimation | 26.1 Infrastructure Costs, 26.2 Cost Scaling Model, 26.3 Cost Optimization | Cost table, scaling model table, optimization opportunities table | Conditional (if applicable) |
| 27 | References & Resources | 27.1 Related Documents, 27.2 External References | Related doc table, external reference table | No |
| 28 | Glossary | — | Term/definition table | No |
| — | Appendices | A: Detailed API Specs, B: Database Schema, C: Wireframes, D: Performance Test Results | Links to external artifacts | No |
| — | Document History | — | Version/date/author/changes table | No |

**Total sections:** 28 numbered + preamble + appendices + document history
**Conditional sections:** 6 (4.2, 6.5, 9, 10, 13.4, 14.6, 26)

---

## Part 2: Release Spec Template Full Audit (`src/superclaude/examples/release-spec-template.md`)

**File size:** 264 lines
**No versioning metadata at the bottom of the file.**
**Embedded inline as fenced YAML block (not a true frontmatter block)** — the YAML is wrapped in triple-backtick fences, not at the top of the file as a real frontmatter header.

---

### 2.1 YAML Frontmatter Fields

The release-spec-template uses a fenced YAML block (lines 19–39) rather than true Jekyll/Hugo YAML frontmatter. All fields use `{{SC_PLACEHOLDER:*}}` sentinels.

| Field | Type/Format | Placeholder | Purpose |
|-------|-------------|-------------|---------|
| `title` | string | `{{SC_PLACEHOLDER:spec_title}}` | Human-readable spec title |
| `version` | string | `"1.0.0"` (literal default) | Spec document version; hardcoded to 1.0.0 |
| `status` | string | `draft` (literal default) | Lifecycle status; hardcoded to `draft` |
| `feature_id` | string/identifier | `{{SC_PLACEHOLDER:fr_id}}` | Feature request ID linking spec to a tracked feature |
| `parent_feature` | string or null | `{{SC_PLACEHOLDER:parent_feature_or_null}}` | Parent feature if this is a sub-feature; null if standalone |
| `spec_type` | enum string | `{{SC_PLACEHOLDER:new_feature_or_refactoring_or_portification_or_infrastructure}}` | One of: `new_feature`, `refactoring`, `portification`, `infrastructure` |
| `complexity_score` | float 0.0–1.0 | `{{SC_PLACEHOLDER:0.0_to_1.0}}` | Numeric complexity score |
| `complexity_class` | enum string | `{{SC_PLACEHOLDER:LOW_or_MEDIUM_or_HIGH}}` | Bucketed complexity class |
| `target_release` | string (version) | `{{SC_PLACEHOLDER:version}}` | Target release version string |
| `authors` | list | `[user, claude]` (literal default) | Document authors; hardcoded to `[user, claude]` |
| `created` | date string | `{{SC_PLACEHOLDER:yyyy_mm_dd}}` | ISO creation date |
| `quality_scores.clarity` | float 0.0–10.0 | `{{SC_PLACEHOLDER:0.0_to_10.0}}` | Clarity quality score |
| `quality_scores.completeness` | float 0.0–10.0 | `{{SC_PLACEHOLDER:0.0_to_10.0}}` | Completeness quality score |
| `quality_scores.testability` | float 0.0–10.0 | `{{SC_PLACEHOLDER:0.0_to_10.0}}` | Testability quality score |
| `quality_scores.consistency` | float 0.0–10.0 | `{{SC_PLACEHOLDER:0.0_to_10.0}}` | Consistency quality score |
| `quality_scores.overall` | float 0.0–10.0 | `{{SC_PLACEHOLDER:0.0_to_10.0}}` | Overall quality score (composite) |

**Total frontmatter fields:** 16 (including 5 nested under `quality_scores`)

**Structural note:** The YAML block is embedded as a code fence inside the markdown body, NOT at the document top as true YAML frontmatter. This is intentional — the release-spec-template begins with a prose usage block, then the YAML. A pipeline tool reading this file would need to extract the fenced YAML block rather than parse a frontmatter header.

---

### 2.2 Section Inventory

| # | Heading | Subsections | Content Expected | Conditional? |
|---|---------|-------------|-----------------|--------------|
| — | Usage block (preamble) | — | Usage instructions, spec types, conditional section guide, quality gate command, sentinel self-check command | No (delete from final) |
| — | YAML block | — | Fenced YAML with all frontmatter fields | No |
| 1 | Problem Statement | 1.1 Evidence, 1.2 Scope Boundary | Problem description narrative; evidence table (source/impact); in-scope/out-of-scope declarations | No |
| 2 | Solution Overview | 2.1 Key Design Decisions, 2.2 Workflow / Data Flow | High-level approach narrative; decision table (alternatives + rationale); ASCII flow diagram | No |
| 3 | Functional Requirements | FR-{id}.1, FR-{id}.2 (repeating) | Numbered FR blocks each with: description, acceptance criteria checklist, dependencies | No |
| 4 | Architecture | 4.1 New Files, 4.2 Modified Files, 4.3 Removed Files, 4.4 Module Dependency Graph, 4.5 Data Models, 4.6 Implementation Order | File tables, ASCII dependency graph, Python data model code block, ordered implementation steps with parallelization notes | 4.3 conditional (refactoring/portification); 4.5 conditional (new_feature/portification) |
| 5 | Interface Contracts | 5.1 CLI Surface, 5.2 Gate Criteria, 5.3 Phase Contracts | CLI usage + option table; gate criteria table (tier/frontmatter/min_lines/semantic_checks); YAML phase contract schema | Whole section conditional (portification/new_feature); 5.2 conditional (portification); 5.3 conditional (portification/infrastructure) |
| 6 | Non-Functional Requirements | — | NFR table: ID / requirement / target / measurement | No |
| 7 | Risk Assessment | — | Risk table: risk / probability / impact / mitigation | No |
| 8 | Test Plan | 8.1 Unit Tests, 8.2 Integration Tests, 8.3 Manual/E2E Tests | Test tables (test name / file / validates); integration tests; manual scenario table | 8.3 conditional (infrastructure/portification) |
| 9 | Migration & Rollout | — | Breaking changes, backwards compatibility, rollback plan (bullet list) | Conditional (refactoring/portification) |
| 10 | Downstream Inputs | For sc:roadmap, For sc:tasklist | Themes/milestones guidance for sc:roadmap; task breakdown guidance for sc:tasklist | No |
| 11 | Open Items | — | Open question table: item / question / impact / resolution target | No |
| 12 | Brainstorm Gap Analysis | — | Gap table: gap_id / description / severity / affected_section / persona; gap analysis summary | No (but note: auto-populated by sc:cli-portify Phase 3c) |
| — | Appendix A: Glossary | — | Term/definition table | Conditional (all types, include if domain terminology used) |
| — | Appendix B: Reference Documents | — | Document/relevance table | Conditional (all types, include if external references needed) |

**Total sections:** 12 numbered + preamble + YAML block + 2 appendices

---

### 2.3 The `{{SC_PLACEHOLDER:*}}` Sentinel System

**How it works:**

Every unfilled value in the release-spec-template is represented by a `{{SC_PLACEHOLDER:KEY}}` token. The key is a human-readable descriptor of what should go there (e.g., `spec_title`, `fr_id`, `0.0_to_1.0`). This allows:

1. **Automated extraction:** A pipeline tool (e.g., sc:cli-portify) can scan the document for sentinel tokens to identify fields that remain unpopulated.
2. **Validation/quality gate:** The sentinel self-check command `grep -c '{{SC_PLACEHOLDER:' <output-file>` returns the count of remaining unfilled sentinels. A count of 0 means the spec is fully populated — this is the completion criterion.
3. **Template vs. instance disambiguation:** The presence of any sentinel in a produced spec file signals that the spec is incomplete or still a template.

**Quality gate command (from usage block):**
```
/sc:spec-panel --focus correctness,architecture
/sc:spec-panel --mode critique
```

**Sentinel self-check command:**
```bash
grep -c '{{SC_PLACEHOLDER:' <output-file>
# Must return 0 for the spec to be considered complete
```

**Full list of sentinel keys used in the template:**

| Sentinel Key | Location | What it expects |
|--------------|----------|-----------------|
| `spec_title` | YAML, title field | Human-readable spec title string |
| `fr_id` | YAML, feature_id field | Feature request identifier |
| `parent_feature_or_null` | YAML, parent_feature field | Parent feature ID or the word `null` |
| `new_feature_or_refactoring_or_portification_or_infrastructure` | YAML, spec_type field | One of the 4 enum values |
| `0.0_to_1.0` | YAML, complexity_score | Float |
| `LOW_or_MEDIUM_or_HIGH` | YAML, complexity_class | One of 3 enum values |
| `version` | YAML, target_release | Version string |
| `yyyy_mm_dd` | YAML, created | ISO date |
| `0.0_to_10.0` (×5) | YAML, quality_scores.* | Float for each quality dimension |
| `problem_description` | Section 1 | Narrative text |
| `evidence_1`, `source`, `impact` | Section 1.1 | Evidence table cells |
| `in_scope`, `out_of_scope` | Section 1.2 | Scope declarations |
| `solution_overview` | Section 2 | Narrative text |
| `decision_1`, `choice`, `alternatives`, `rationale` | Section 2.1 | Decision table cells |
| `flow_diagram` | Section 2.2 | ASCII diagram |
| `id`, `requirement_title`, `what_it_does`, `criterion_1`, `criterion_2`, `dependencies_or_none` | Section 3 | FR block fields |
| `repeat_pattern` | Section 3 | Signal to repeat FR block structure |
| `file_path`, `purpose`, `deps` | Section 4.1 | New files table |
| `file_path`, `change_description`, `why` | Section 4.2 | Modified files table |
| `target`, `reason`, `migration_notes` | Section 4.3 | Removed files table |
| `dependency_diagram` | Section 4.4 | ASCII module graph |
| `data_model_code` | Section 4.5 | Python code block |
| `first_step`, `second_step`, `parallel_step`, `third_step`, `rationale` (×multiple) | Section 4.6 | Implementation order |
| `cli_usage` | Section 5.1 | CLI usage string |
| `option`, `type`, `default`, `desc` | Section 5.1 | CLI option table |
| `step`, `tier`, `fields`, `n`, `checks` | Section 5.2 | Gate criteria table |
| `contract_schema` | Section 5.3 | YAML schema |
| `id`, `requirement`, `target`, `how_measured` | Section 6 | NFR table |
| `risk_1`, `low_med_high` (×2), `mitigation` | Section 7 | Risk table |
| `test_name`, `file_path`, `what_it_validates` | Section 8.1 | Unit test table |
| `test_name`, `what_it_validates` | Section 8.2 | Integration test table |
| `scenario`, `steps`, `expected` | Section 8.3 | Manual test table |
| `yes_no_details`, `strategy`, `plan` | Section 9 | Migration fields |
| `themes_and_milestones` | Section 10 | sc:roadmap input guidance |
| `task_breakdown_guidance` | Section 10 | sc:tasklist input guidance |
| `item`, `question`, `impact`, `target` | Section 11 | Open item table |
| `gap_id`, `description`, `high_medium_low`, `affected_section`, `persona` | Section 12 | Gap table |
| `gap_analysis_summary` | Section 12 | Summary narrative |
| `term`, `definition` | Appendix A | Glossary |
| `doc_path`, `why_relevant` | Appendix B | Reference docs |

---

## Frontmatter Comparison Table

| Field | In TDD Template | In Spec Template | Notes |
|-------|-----------------|-----------------|-------|
| `id` | Yes — `"[COMPONENT-ID]-TDD"` | No | TDD-specific doc identifier; no equivalent in spec |
| `title` | Yes — string | Yes — `{{SC_PLACEHOLDER:spec_title}}` | Both have title; TDD is human placeholder, spec is sentinel |
| `description` | Yes — long string | No | TDD has a description field; spec has no description in YAML |
| `version` | Yes — `"1.2"` | Yes — `"1.0.0"` (literal) | Both have version; different defaults; TDD tracks doc revision, spec always starts at 1.0.0 |
| `status` | Yes — `"🟡 Draft"` | Yes — `draft` (literal) | Both have status; TDD uses emoji-prefixed values, spec uses plain strings |
| `type` | Yes — `"📐 Technical Design Document"` | No | TDD has type field; spec has no equivalent |
| `priority` | Yes — `"🔥 Highest"` | No | TDD has priority; spec has no equivalent |
| `created_date` | Yes — `"YYYY-MM-DD"` | No (but `created` exists) | TDD uses `created_date`; spec uses `created` — different field names |
| `created` | No | Yes — `{{SC_PLACEHOLDER:yyyy_mm_dd}}` | Spec uses `created`; TDD uses `created_date` |
| `updated_date` | Yes — `"YYYY-MM-DD"` | No | TDD tracks update date; spec has no equivalent |
| `assigned_to` | Yes — `"[engineering-team]"` | No | TDD has assignee; spec has no equivalent |
| `autogen` | Yes — `false` | No | TDD tracks whether auto-generated; spec has no equivalent |
| `coordinator` | Yes — `"[tech-lead]"` | No | TDD has coordinator/tech lead field; spec has no equivalent |
| `parent_doc` | Yes — link to PRD | No | TDD links to parent PRD; spec has `parent_feature` instead |
| `parent_feature` | No | Yes — `{{SC_PLACEHOLDER:parent_feature_or_null}}` | Spec has parent_feature; TDD has parent_doc (different semantics) |
| `depends_on` | Yes — list | No | TDD has depends_on list; spec has no equivalent |
| `related_docs` | Yes — list | No | TDD has related_docs; spec has no equivalent |
| `tags` | Yes — list | No | TDD has tags list; spec has no equivalent |
| `template_schema_doc` | Yes — empty string | No | TDD has schema doc pointer; spec has no equivalent |
| `estimation` | Yes — empty string | No | TDD has estimation field; spec has no equivalent |
| `sprint` | Yes — empty string | No | TDD has sprint field; spec has no equivalent |
| `due_date` | Yes — empty string | No | TDD has due_date; spec has `target_release` (different semantics) |
| `start_date` | Yes — empty string | No | TDD has start_date; spec has no equivalent |
| `completion_date` | Yes — empty string | No | TDD has completion_date; spec has no equivalent |
| `blocker_reason` | Yes — empty string | No | TDD has blocker_reason; spec has no equivalent |
| `review_info.*` | Yes — 3 sub-fields | No | TDD has full review tracking; spec has no equivalent |
| `approvers.*` | Yes — 4 sub-fields | No | TDD has structured approvers block; spec has no equivalent |
| `feature_id` | No | Yes — `{{SC_PLACEHOLDER:fr_id}}` | Spec has feature_id for feature request linkage; TDD has no equivalent |
| `spec_type` | No | Yes — enum (4 values) | Spec has type classification (new_feature/refactoring/portification/infrastructure); TDD has `type` but only one value. **sc:roadmap ignores — would need pipeline upgrade to use** (currently computes type from body-text keyword analysis) |
| `complexity_score` | No | Yes — float 0.0–1.0 | Spec has numeric complexity scoring; TDD has no equivalent. **sc:roadmap ignores — would need pipeline upgrade to use** (currently always computes from scratch via 5-factor formula) |
| `complexity_class` | No | Yes — enum LOW/MEDIUM/HIGH | Spec has complexity bucket; TDD has no equivalent. **sc:roadmap ignores — would need pipeline upgrade to use** (currently always derived from computed complexity_score) |
| `target_release` | No (has `due_date` and `sprint`) | Yes — version string | Spec explicitly names target release version; TDD spreads this across sprint + due_date |
| `authors` | No | Yes — list, default `[user, claude]` | Spec has authors list; TDD has `coordinator` and `assigned_to` but no authors list |
| `quality_scores.clarity` | No | Yes — float 0.0–10.0 | Spec has structured quality scoring; TDD has no equivalent. **sc:roadmap ignores — would need pipeline upgrade to use** (sc:spec-panel produces its own metrics under a different schema) |
| `quality_scores.completeness` | No | Yes — float 0.0–10.0 | Same — sc:roadmap ignores input quality_scores |
| `quality_scores.testability` | No | Yes — float 0.0–10.0 | Same — sc:roadmap ignores input quality_scores |
| `quality_scores.consistency` | No | Yes — float 0.0–10.0 | Same — sc:roadmap ignores input quality_scores |
| `quality_scores.overall` | No | Yes — float 0.0–10.0 | Same — sc:roadmap ignores input quality_scores |

**Summary counts:**
- Fields in TDD template YAML: 27
- Fields in spec template YAML: 16
- Fields in both (with any overlap): 4 (title, version, status, and approximate date analog)
- Fields unique to TDD: 23
- Fields unique to spec: 12

---

## TDD Section to sc:roadmap Extraction Mapping

The `sc:roadmap` command takes a spec or TDD as input and extracts structured information to build a roadmap. Based on the spec template's Section 10 (`Downstream Inputs`) and the overall pipeline, the following extraction mapping applies:

| TDD Section | Content Type | Maps to sc:roadmap extraction? | Extraction step / target |
|-------------|-------------|-------------------------------|--------------------------|
| 1. Executive Summary | High-level scope narrative | Yes — partial | Roadmap overview/theme extraction |
| 2. Problem Statement & Context | Background + business context | Yes | Context for epic/theme framing; maps to themes in roadmap |
| 3. Goals & Non-Goals | Goal table with success criteria | Yes — strong | Direct input for milestone and epic goal definitions |
| 4. Success Metrics | Technical + business KPIs | Yes — partial | Milestone acceptance criteria; maps to quality gates |
| 5. Technical Requirements | FR table + NFR sub-tables | Yes — strong | FR rows map directly to task-level extraction; NFR rows map to constraints |
| 6. Architecture | Component diagram + design decisions + system boundaries | Yes — partial | Phase structure inference; component names become task groupings |
| 7. Data Models | Entity definitions + data flow | Yes — partial | Implementation ordering dependencies |
| 8. API Specifications | Endpoint table + versioning | Yes — partial | API-specific tasks; endpoint list can become sub-tasks |
| 9. State Management | State architecture + transitions | No / Weak | Frontend-conditional; roadmap does not specifically target state management for extraction |
| 10. Component Inventory | Route/component tables | No / Weak | Frontend-conditional; too granular for roadmap-level extraction |
| 11. User Flows & Interactions | Sequence diagrams + steps | Yes — partial | Flow names can become epic-level user stories in roadmap |
| 12. Error Handling & Edge Cases | Error category + retry tables | No — low | Too implementation-specific for roadmap extraction; may feed into task descriptions |
| 13. Security Considerations | Threat model + controls | Yes — partial | Security tasks appear as roadmap phase items (e.g., "security review complete") |
| 14. Observability & Monitoring | Metrics + alerts + dashboards | Yes — partial | "Monitoring setup" as a distinct roadmap task/milestone |
| 15. Testing Strategy | Test pyramid + test cases | Yes — partial | Testing phases and coverage targets appear as milestone exit criteria |
| 16. Accessibility Requirements | WCAG compliance checklist | No — low | Only relevant for frontend; too granular for roadmap |
| 17. Performance Budgets | FE/BE performance targets | Yes — partial | Performance validation milestone; targets feed into acceptance criteria |
| 18. Dependencies | External/internal/infra dependencies | Yes — strong | Dependency graph shapes roadmap phase sequencing; blocking dependencies affect milestone ordering |
| 19. Migration & Rollout Plan | Migration phases + feature flags + rollout stages | Yes — strong | Maps directly to roadmap phases; rollout stages are milestones |
| 20. Risks & Mitigations | Risk table | Yes — partial | Risk items can appear as contingency tasks or phase gates in roadmap |
| 21. Alternatives Considered | Pros/cons of alternatives | No — metadata only | Not typically extracted into roadmap tasks; informs design decisions but not execution |
| 22. Open Questions | Question/owner/status table | Yes — partial | Unresolved open questions become blocking items or investigation tasks in roadmap |
| 23. Timeline & Milestones | Milestone table + phases | Yes — very strong | Direct source for roadmap milestones; phase deliverables become roadmap tasks |
| 24. Release Criteria | DoD checklist + release checklist | Yes — strong | Maps to milestone exit criteria and release gate tasks |
| 25. Operational Readiness | Runbook + on-call + capacity planning | Yes — partial | Ops readiness tasks appear as post-launch phase items in roadmap |
| 26. Cost & Resource Estimation | Infrastructure cost tables | No — metadata only | Not directly extracted; informs planning but not execution roadmap |
| 27. References & Resources | Related doc table | No — metadata only | Not extracted; used for context only |
| 28. Glossary | Term definitions | No | Not extracted |

**Strong extraction targets (5):** Sections 3, 5, 18, 19, 23 — these directly shape roadmap structure.
**Partial extraction targets (13):** Sections 1, 2, 4, 6, 7, 8, 11, 13, 14, 15, 17, 20, 22, 24, 25 — these contribute to individual tasks or milestone criteria.
**No/weak extraction (10):** Sections 9, 10, 12, 16, 21, 26, 27, 28 — metadata, frontend-specific, or too granular.

---

## Exact Additions Needed for Pipeline Compatibility

These are YAML frontmatter fields present in the spec template but absent from the TDD template. For sc:roadmap to use a TDD as a first-class input (the way it uses a release spec), these fields would need to be added to the TDD's frontmatter:

### 1. `feature_id`
- **Exact field name:** `feature_id`
- **Purpose:** Links the TDD to a tracked feature request in the pipeline. sc:roadmap uses this to associate the TDD with a specific feature in the backlog/project management system.
- **Possible values:** String — e.g., `"FR-042"`, `"AUTH-TDD-001"`, any feature request ID
- **sc:roadmap behavior:** Reads from frontmatter. The pipeline needs this to correlate the TDD with downstream artifacts (tasks, sprints, releases). It cannot be computed.

### 2. `spec_type`
- **Exact field name:** `spec_type`
- **Purpose:** Classifies the type of work being described. This determines which conditional sections are active and how sc:roadmap routes the document through extraction logic (different extraction strategies for new_feature vs. refactoring vs. portification vs. infrastructure).
- **Possible values:** `new_feature` | `refactoring` | `portification` | `infrastructure`
- **sc:roadmap behavior:** sc:roadmap does NOT read `spec_type` from frontmatter. It computes the dominant type from body-text domain keyword analysis. Adding `spec_type` to the TDD frontmatter provides no benefit to the current pipeline — it would only be useful if sc:roadmap were upgraded to read it.

### 3. `complexity_score`
- **Exact field name:** `complexity_score`
- **Purpose:** Numeric measure of implementation complexity used by the pipeline to estimate sprint length, allocate resources, and set milestone timescales.
- **Possible values:** Float 0.0 to 1.0 (e.g., `0.3` for low, `0.6` for medium, `0.9` for high)
- **sc:roadmap behavior:** sc:roadmap does NOT read `complexity_score` from frontmatter. It always computes complexity from scratch using a 5-factor formula applied to extracted requirements. Adding `complexity_score` to TDD frontmatter provides no benefit to the current pipeline unless sc:roadmap is upgraded to optionally use it as an override.

### 4. `complexity_class`
- **Exact field name:** `complexity_class`
- **Purpose:** Human-readable complexity bucket derived from complexity_score. Used for display, prioritization, and sprint planning heuristics.
- **Possible values:** `LOW` | `MEDIUM` | `HIGH`
- **sc:roadmap behavior:** sc:roadmap does NOT read `complexity_class` from frontmatter. It always computes complexity from scratch using a 5-factor formula and derives the class from that result. Adding `complexity_class` to TDD frontmatter provides no benefit to the current pipeline unless sc:roadmap is upgraded to optionally use it as an override.

### 5. `target_release`
- **Exact field name:** `target_release`
- **Purpose:** The explicit release version this TDD targets. The TDD template has `sprint` and `due_date` (both empty) but no version-string target. sc:roadmap uses `target_release` to bucket milestones under the correct release.
- **Possible values:** Version string — e.g., `"v4.3.0"`, `"2026-Q2"`, `"Sprint-14"`
- **sc:roadmap behavior:** Reads from frontmatter. If absent, sc:roadmap may fall back to `sprint` or `due_date` but these are different semantics. Having an explicit `target_release` prevents ambiguity.

### 6. `authors`
- **Exact field name:** `authors`
- **Purpose:** Lists document authors (human + AI). Used for attribution, notification routing, and audit trail in the pipeline.
- **Possible values:** YAML list — e.g., `[user, claude]`, `["eng-team-lead"]`
- **sc:roadmap behavior:** Reads from frontmatter. Not computed. The TDD has `coordinator` and `assigned_to` which are partial equivalents but do not map cleanly to the `authors` concept.

### 7. `quality_scores`
- **Exact field name:** `quality_scores` (with sub-fields: `clarity`, `completeness`, `testability`, `consistency`, `overall`)
- **Purpose:** Structured quality assessment used by the pipeline (sc:spec-panel) as a gate before roadmap generation. Scores validate the TDD is ready for extraction.
- **Possible values:** Each sub-field is a float 0.0–10.0
- **sc:roadmap behavior:** sc:roadmap does NOT read `quality_scores` from input frontmatter at all. sc:spec-panel produces its own quality metrics under a different schema as part of its own output. Adding `quality_scores` to TDD frontmatter has no effect on the pipeline.

### 8. `created` (rename of `created_date`)
- **Exact field name:** `created` (spec uses this; TDD uses `created_date`)
- **Purpose:** ISO creation date. The field name inconsistency means a pipeline reading both spec and TDD types would need to handle both `created` and `created_date`. Standardizing to `created` in the TDD would improve compatibility.
- **Possible values:** ISO date string `YYYY-MM-DD`
- **sc:roadmap behavior:** Reads from frontmatter. Currently reads `created` from specs; would need normalization logic for TDDs unless the field is renamed.

---

## Sentinel System Documentation

### Overview

The `{{SC_PLACEHOLDER:KEY}}` system is the release-spec-template's mechanism for marking every unfilled value in a template document. It enables automated pipeline validation of spec completeness.

### How It Works

1. **Template authoring:** Every value that must be filled in by the author or auto-populated by a pipeline tool is replaced with `{{SC_PLACEHOLDER:KEY}}` where KEY is a human-readable descriptor of what belongs there.

2. **Population:** When a spec is created from the template (manually or via sc:cli-portify), each sentinel is replaced with its actual value. After all sentinels are replaced, the document is an instance, not a template.

3. **Completion validation:** The sentinel self-check command counts remaining sentinels:
   ```bash
   grep -c '{{SC_PLACEHOLDER:' <output-file>
   ```
   A return value of `0` means the spec is fully populated and ready for pipeline use. Any non-zero value means the spec is incomplete.

4. **Quality gate integration:** Before sc:roadmap consumes a spec, the pipeline runs:
   - `/sc:spec-panel --focus correctness,architecture` — checks correctness and architectural coherence
   - `/sc:spec-panel --mode critique` — runs a critique pass to surface gaps
   Both gates must pass. Sentinel count of 0 is a precondition for these gate commands.

### Sentinel Coverage by Document Area

| Area | Sentinel count (approx.) | Notes |
|------|--------------------------|-------|
| YAML frontmatter | 11 unique keys (16 total including repeating quality_scores) | All frontmatter values except `version`, `status`, `authors` are sentinels |
| Section 1 Problem | 6 | Problem description, 3 evidence cells, 2 scope declarations |
| Section 2 Solution | 6 | Overview, 4 decision table cells, flow diagram |
| Section 3 FRs | 6 per FR block | Repeating pattern; count scales with number of FRs |
| Section 4 Architecture | 10+ | File tables, dependency graph, data models, implementation order |
| Section 5 Interfaces | 8 | CLI usage, option table, gate criteria, contract schema |
| Sections 6-9 | 4–6 each | NFR, risk, test plan, migration |
| Sections 10-12 | 6–8 | Downstream inputs, open items, gap analysis |
| Appendices | 4 | Glossary and reference doc tables |

### What the Sentinel System Does NOT Cover

- The `version` field (hardcoded to `"1.0.0"`) — pipeline increments this programmatically, not via sentinel
- The `status` field (hardcoded to `draft`) — same pattern
- The `authors` field (hardcoded to `[user, claude]`) — treated as a default, not a sentinel
- The prose content of Appendices (only the placeholder rows are sentineled; if no appendix content exists, the sentinel in the row remains until either removed or filled)

### Sentinel Key Naming Convention

Keys follow a consistent pattern:
- **Snake_case** for field names (`spec_title`, `fr_id`, `problem_description`)
- **Underscore-separated enum hints** for constrained fields (`LOW_or_MEDIUM_or_HIGH`, `new_feature_or_refactoring_or_portification_or_infrastructure`)
- **Range hints** for numeric fields (`0.0_to_1.0`, `0.0_to_10.0`)
- **Format hints** for date fields (`yyyy_mm_dd`)
- **Semantic role hints** for table cells (`evidence_1`, `source`, `impact`, `why_relevant`)

---

## Summary

**Status:** Complete

### Key Findings

1. **The TDD template is a comprehensive engineering specification document** with 28 numbered sections, 1,309 lines at full build-out, and tiered usage guidance (Lightweight/Standard/Heavyweight). It is thorough and self-contained for human engineers.

2. **The release-spec-template is a pipeline-first document** with 12 sections, 264 lines, and a sentinel-based completeness verification system. Every field that needs population is explicitly marked, making automated extraction and validation straightforward.

3. **The two templates have fundamentally different frontmatter philosophies:**
   - The TDD frontmatter is rich with tracking/workflow metadata (sprint, due_date, approvers, review_info, blocker_reason) but lacks pipeline-critical classification fields.
   - The spec frontmatter is sparse on workflow metadata but has all the machine-readable classification fields sc:roadmap needs: `spec_type`, `complexity_score`, `complexity_class`, `feature_id`, `target_release`, `quality_scores`.

4. **For sc:roadmap to use a TDD as input,** at minimum 7 fields need to be added to TDD frontmatter: `feature_id`, `spec_type`, `complexity_score`, `complexity_class`, `target_release`, `authors`, and `quality_scores.*`. The `created_date` vs `created` naming inconsistency also needs resolution.

5. **The sentinel system is elegant and portable.** It could be applied to the TDD template with minimal effort — replacing placeholder text like `"[Component Name]"` with `{{SC_PLACEHOLDER:component_name}}` tokens would make TDD completeness machine-verifiable.

6. **Section 10 of the spec template (`Downstream Inputs`) is the most pipeline-relevant section** and has no equivalent in the TDD template. A TDD intended as pipeline input should include a similar section explicitly documenting what sc:roadmap and sc:tasklist should extract from it.

---

## Gaps and Questions

1. **Does sc:roadmap currently accept TDD files as input, or only spec files?** The pipeline wiring in sc:roadmap may need updating to handle TDD frontmatter field variations.

2. **Should the TDD template adopt the sentinel system for frontmatter fields?** This would make TDD completeness machine-verifiable, but the TDD is human-authored and the sentinel syntax may be unfamiliar to engineers who only work with TDDs.

3. **The `created_date` vs `created` inconsistency** — should TDD standardize to `created` (spec convention) or should the pipeline normalize both?

4. **Quality scores on a TDD:** The spec template computes quality scores via sc:spec-panel. Should TDDs also go through a quality gate before sc:roadmap consumes them? If so, the `quality_scores` block needs to be added to TDD frontmatter.

5. **The `spec_type` enum (new_feature/refactoring/portification/infrastructure) may not fully cover TDD use cases.** A TDD might describe work that spans multiple types. Is `spec_type` a 1:1 classification or can it be a list?

6. **Section 10 (Downstream Inputs) in the spec template** is the bridge to sc:roadmap. The TDD has no equivalent. Should one be added, or should sc:roadmap extract this information from the TDD's existing sections (Goals, Milestones, etc.) without an explicit bridge section?

---

## Key Takeaways

1. **8 fields needed in TDD frontmatter for pipeline compatibility:** `feature_id`, `spec_type`, `complexity_score`, `complexity_class`, `target_release`, `authors`, `quality_scores` (5 sub-fields), and standardizing `created_date` → `created`.

2. **The TDD already contains the content sc:roadmap needs** — it just lacks the machine-readable frontmatter classification that helps the pipeline parse it efficiently. The data is in Sections 3, 5, 18, 19, and 23 specifically.

3. **The sentinel system from the spec template should be evaluated for TDD adoption** — it would provide the same zero-sentinel completeness gate that makes spec validation clean.

4. **The spec template's Section 10 (Downstream Inputs) pattern is valuable** and has no TDD equivalent. Adding a lightweight version of this section to the TDD would make the pipeline handoff explicit rather than implicit.

5. **The two templates serve different audiences** — the TDD is written for engineers and stakeholders who need deep architectural detail; the spec is written for the pipeline that needs clean, machine-parseable input. Making the TDD pipeline-compatible requires adding pipeline-native fields without cluttering the human-readable engineering content.


