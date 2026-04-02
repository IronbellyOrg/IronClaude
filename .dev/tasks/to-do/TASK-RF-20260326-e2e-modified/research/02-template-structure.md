# Research: Template Structure — TDD and Release Spec Templates

**Researcher**: researcher-templates
**Status**: Complete
**Created**: 2026-03-26
**Scope**: `src/superclaude/examples/tdd_template.md`, `src/superclaude/examples/release-spec-template.md`
**Goal**: Document full structure of both templates for E2E pipeline test fixture population

---

## 1. TDD Template Structure (`tdd_template.md`)

**Source**: `/Users/cmerritt/GFxAI/IronClaude/src/superclaude/examples/tdd_template.md`
**Total lines**: ~1274
**Sections**: 28 numbered sections + preamble + appendices

### 1.1 YAML Frontmatter Fields

All fields use `[bracket]` placeholder patterns (not `{{SC_PLACEHOLDER:}}`).

| Field | Expected Type | Placeholder Example | Notes |
|-------|--------------|---------------------|-------|
| `id` | string | `"[COMPONENT-ID]-TDD"` | Sentinel check target |
| `title` | string | `"[Component Name] - Technical Design Document"` | |
| `description` | string | Free text with `[component name]` | |
| `version` | string | `"1.2"` | Template version, not doc version |
| `status` | string (emoji + text) | `"🟡 Draft"` | |
| `type` | string | `"📐 Technical Design Document"` | |
| `priority` | string | `"🔥 Highest"` | |
| `created_date` | string | `"YYYY-MM-DD"` | |
| `updated_date` | string | `"YYYY-MM-DD"` | |
| `assigned_to` | string | `"[engineering-team]"` | |
| `autogen` | boolean | `false` | |
| `coordinator` | string | `"[tech-lead]"` | |
| `parent_doc` | string | `"[link to Product PRD that this TDD implements]"` | |
| `feature_id` | string | `"[FEATURE-ID]"` | **Sentinel check target** — must not remain `[FEATURE-ID]` |
| `spec_type` | string enum | `"new_feature"` | Valid: `new_feature`, `refactoring`, `portification`, `migration`, `infrastructure`, `security`, `performance`, `docs` |
| `complexity_score` | string (empty) | `""` | 0.0-1.0; computed by sc:roadmap |
| `complexity_class` | string (empty) | `""` | LOW, MEDIUM, HIGH; computed by sc:roadmap |
| `target_release` | string | `"[version]"` | **Sentinel check target** — must not remain `[version]` |
| `authors` | list of strings | `["[author1]", "[author2]"]` | |
| `quality_scores` | nested map | Sub-fields: `clarity`, `completeness`, `testability`, `consistency`, `overall` — all empty strings | Populated by sc:spec-panel |
| `depends_on` | list of strings | `["[list dependent documents/components]"]` | |
| `related_docs` | list of strings | `["[list related documents]"]` | |
| `tags` | list of strings | `["technical-design-document", "[component-type]", "architecture"]` | |
| `template_schema_doc` | string (empty) | `""` | |
| `estimation` | string (empty) | `""` | |
| `sprint` | string (empty) | `""` | |
| `due_date` | string (empty) | `""` | |
| `start_date` | string (empty) | `""` | |
| `completion_date` | string (empty) | `""` | |
| `blocker_reason` | string (empty) | `""` | |
| `review_info` | nested map | Sub-fields: `last_reviewed_by`, `last_review_date`, `next_review_date` — all empty | |
| `approvers` | nested map | Sub-fields: `tech_lead`, `engineering_manager`, `architect`, `security` — all empty | |

**Total frontmatter fields**: 30 (including nested sub-fields within `quality_scores`, `review_info`, `approvers`)

### 1.2 Sentinel Self-Check Requirements (TDD)

From lines 60-68, the TDD template explicitly states:

1. `feature_id` must not be `"[FEATURE-ID]"`
2. `spec_type` must be one of the valid enum values
3. `target_release` must not be `"[version]"`
4. `complexity_score` and `complexity_class` may remain empty (computed by sc:roadmap)

**Pipeline field consumption** (lines 66-69):
- `complexity_score`, `complexity_class`: Computed by sc:roadmap during extraction — pre-populated values are advisory only
- `feature_id`, `spec_type`, `target_release`: Consumed by sc:spec-panel `--downstream roadmap` (Step 6b)
- `quality_scores`: Populated by sc:spec-panel review output, NOT consumed by sc:roadmap

### 1.3 Tiered Usage Model

The TDD template defines three tiers (lines 86-89):

| Tier | When | Required Sections |
|------|------|-------------------|
| Lightweight | Bug fixes, config changes, <1 sprint | 1, 2, 3, 6.4, 21, 22 |
| Standard | Most features, 1-3 sprints | All numbered sections; skip conditional sections marked *(if applicable)* |
| Heavyweight | New systems, platform changes, cross-team | All sections fully completed including conditional |

### 1.4 All 28 Sections — Purpose and Content Depth Classification

**Legend**:
- **RICH** = Pipeline-critical; needs substantial, structured content for extraction
- **MODERATE** = Needs real content but can be shorter (3-10 lines)
- **MINIMAL** = 1-3 sentences or a small table suffices
- **CONDITIONAL** = Only required for certain spec_types or component types

| # | Section Title | Depth | Pipeline Role | Sub-sections |
|---|--------------|-------|---------------|-------------|
| 1 | Executive Summary | MINIMAL | Overview extraction | Key Deliverables (bullet list) |
| 2 | Problem Statement & Context | MODERATE | Context extraction | 2.1 Background, 2.2 Problem Statement, 2.3 Business Context |
| 3 | Goals & Non-Goals | MODERATE | Scope extraction | 3.1 Goals (table: ID/Goal/Criteria), 3.2 Non-Goals (table: ID/Non-Goal/Rationale), 3.3 Future Considerations |
| 4 | Success Metrics | MODERATE | Metrics extraction | 4.1 Technical Metrics (table), 4.2 Business Metrics *(if applicable)* |
| **5** | **Technical Requirements** | **RICH** | **FR-ID extraction, NFR extraction** | 5.1 Functional Requirements (table: FR-001 format), 5.2 Non-Functional Requirements (Performance, Scalability, Reliability, SLOs, Security sub-tables) |
| **6** | **Architecture** | **RICH** | **Architecture extraction, dependency graph** | 6.1 High-Level Architecture (diagram), 6.2 Component Diagram (mermaid), 6.3 System Boundaries (table), 6.4 Key Design Decisions (table), 6.5 Multi-Tenancy *(if applicable)* |
| **7** | **Data Models** | **RICH** | **Schema extraction** | 7.1 Data Entities (interface + field table per entity), 7.2 Data Flow (mermaid), 7.3 Data Storage (table) |
| **8** | **API Specifications** | **RICH** | **API contract extraction** | 8.1 API Overview (table), 8.2 Endpoint Details (per-endpoint blocks with request/response/errors), 8.3 Error Response Format (JSON schema), 8.4 API Governance & Versioning |
| 9 | State Management | CONDITIONAL (frontend only) | Frontend state extraction | 9.1 State Architecture (table), 9.2 State Shape (TypeScript interface), 9.3 State Transitions (table) |
| **10** | **Component Inventory** | **CONDITIONAL/RICH** (frontend only) | Component extraction | 10.1 Page/Route Structure (table), 10.2 Shared Components (table), 10.3 Component Hierarchy (ASCII tree) |
| 11 | User Flows & Interactions | MODERATE | Flow extraction | 11.1 Primary User Flow (mermaid sequence diagram + steps), 11.2 Secondary flows |
| 12 | Error Handling & Edge Cases | MODERATE | Error strategy extraction | 12.1 Error Categories (table), 12.2 Edge Cases (table), 12.3 Graceful Degradation (table), 12.4 Retry & Recovery Strategies (table) |
| 13 | Security Considerations | MODERATE | Security extraction | 13.1 Threat Model (table), 13.2 Security Controls (table), 13.3 Sensitive Data Handling (table), 13.4 Data Governance *(if applicable)* |
| 14 | Observability & Monitoring | MODERATE | Ops extraction | 14.1 Logging (table + levels), 14.2 Metrics (table), 14.3 Tracing (table), 14.4 Alerts (table), 14.5 Dashboards (table), 14.6 Business Metric Instrumentation *(if applicable)* |
| **15** | **Testing Strategy** | **RICH** | **Test plan extraction** | 15.1 Test Pyramid (table: level/coverage/tools), 15.2 Test Cases (Unit/Integration/E2E tables), 15.3 Test Environments (table) |
| 16 | Accessibility Requirements | CONDITIONAL (frontend) | A11y extraction | 16.1 Requirements (table), 16.2 Testing Tools (list) |
| 17 | Performance Budgets | MODERATE | Perf budget extraction | 17.1 Frontend Performance (table), 17.2 Backend Performance (table), 17.3 Performance Testing (table) |
| 18 | Dependencies | MODERATE | Dependency extraction | 18.1 External Dependencies (table), 18.2 Internal Dependencies (table), 18.3 Infrastructure Dependencies (table) |
| **19** | **Migration & Rollout Plan** | **RICH** | **Rollout strategy extraction** | 19.1 Migration Strategy (table: phases), 19.2 Feature Flags (table + lifecycle), 19.3 Rollout Stages (table), 19.4 Rollback Procedure (numbered steps + criteria) |
| **20** | **Risks & Mitigations** | **RICH** | **Risk matrix extraction** | Single table: ID/Risk/Probability/Impact/Mitigation/Contingency |
| 21 | Alternatives Considered | MODERATE | Decision extraction | Alt 0: Do Nothing *(mandatory)*, Alt 1+: Pros/Cons/Why Not Chosen |
| 22 | Open Questions | MINIMAL | Tracking | Table: ID/Question/Owner/Target Date/Status/Resolution |
| 23 | Timeline & Milestones | MODERATE | Schedule extraction | 23.1 High-Level Timeline (table), 23.2 Implementation Phases (per-phase deliverables + exit criteria) |
| **24** | **Release Criteria** | **RICH** | **Release gate extraction** | 24.1 Definition of Done (checklist, 13 items), 24.2 Release Checklist (9 items) |
| **25** | **Operational Readiness** | **RICH** | **Ops readiness extraction** | 25.1 Runbook (table: scenario/symptoms/diagnosis/resolution/escalation), 25.2 On-Call Expectations (table), 25.3 Capacity Planning (table) |
| 26 | Cost & Resource Estimation | CONDITIONAL | Cost extraction | 26.1 Infrastructure Costs (table), 26.2 Cost Scaling Model (table), 26.3 Cost Optimization (table) |
| 27 | References & Resources | MINIMAL | Link extraction | 27.1 Related Documents (table), 27.2 External References (table) |
| 28 | Glossary | MINIMAL | Term extraction | Single table: Term/Definition |

**Appendices** (after Section 28): A (Detailed API Specs), B (Database Schema), C (Wireframes), D (Performance Test Results)

### 1.5 Placeholder Patterns (TDD)

The TDD template uses **square bracket** placeholders exclusively:

| Pattern | Example | Where Used |
|---------|---------|-----------|
| `[Name]` | `[Component Name]`, `[Team Name]` | Throughout — generic names |
| `[X]` | `< [X]ms`, `> [X]%` | Performance/metric targets |
| `[H/M/L]` | Probability/Impact fields | Risk tables |
| `[Status]` | Document Info table | Status fields |
| `[Link]` | References | URL placeholders |
| `[COMPONENT-ID]` | Frontmatter `id` | Sentinel check |
| `[FEATURE-ID]` | Frontmatter `feature_id` | **Sentinel check target** |
| `[version]` | Frontmatter `target_release` | **Sentinel check target** |
| `[Description]` | Various | Generic content placeholders |
| `[How implemented]` / `[How tested]` | Security, A11y sections | Implementation/verification |
| `[Date]` | Timeline tables | Date placeholders |
| `[Tool]` | Testing, monitoring | Tooling choices |

**No `{{SC_PLACEHOLDER:}}` sentinels in the TDD template** — that pattern is exclusive to the release-spec template.

---

## 2. Release Spec Template Structure (`release-spec-template.md`)

**Source**: `/Users/cmerritt/GFxAI/IronClaude/src/superclaude/examples/release-spec-template.md`
**Total lines**: 265
**Sections**: 12 numbered sections + 2 appendices

### 2.1 YAML Frontmatter Fields

All fields use `{{SC_PLACEHOLDER:descriptor}}` sentinel pattern.

| Field | Sentinel | Expected Value Type |
|-------|----------|-------------------|
| `title` | `{{SC_PLACEHOLDER:spec_title}}` | Quoted string |
| `version` | (hardcoded `"1.0.0"`) | String |
| `status` | (hardcoded `draft`) | String |
| `feature_id` | `{{SC_PLACEHOLDER:fr_id}}` | String (e.g., FR-001) |
| `parent_feature` | `{{SC_PLACEHOLDER:parent_feature_or_null}}` | String or null |
| `spec_type` | `{{SC_PLACEHOLDER:new_feature_or_refactoring_or_portification_or_migration_or_infrastructure_or_security_or_performance_or_docs}}` | String enum |
| `complexity_score` | `{{SC_PLACEHOLDER:0.0_to_1.0}}` | Float 0.0-1.0 |
| `complexity_class` | `{{SC_PLACEHOLDER:LOW_or_MEDIUM_or_HIGH}}` | String enum |
| `target_release` | `{{SC_PLACEHOLDER:version}}` | String |
| `authors` | (hardcoded `[user, claude]`) | List |
| `created` | `{{SC_PLACEHOLDER:yyyy_mm_dd}}` | Date string |
| `quality_scores.clarity` | `{{SC_PLACEHOLDER:0.0_to_10.0}}` | Float 0.0-10.0 |
| `quality_scores.completeness` | `{{SC_PLACEHOLDER:0.0_to_10.0}}` | Float 0.0-10.0 |
| `quality_scores.testability` | `{{SC_PLACEHOLDER:0.0_to_10.0}}` | Float 0.0-10.0 |
| `quality_scores.consistency` | `{{SC_PLACEHOLDER:0.0_to_10.0}}` | Float 0.0-10.0 |
| `quality_scores.overall` | `{{SC_PLACEHOLDER:0.0_to_10.0}}` | Float 0.0-10.0 |

**Total frontmatter fields**: 16 (including 5 nested quality_scores)

### 2.2 Valid `spec_type` Values

From the frontmatter (line 26): `new_feature`, `refactoring`, `portification`, `migration`, `infrastructure`, `security`, `performance`, `docs`

### 2.3 Sentinel Self-Check (Release Spec)

From line 15: `grep -c '{{SC_PLACEHOLDER:' <output-file>` should return 0 after population.

### 2.4 Conditional Sections by spec_type

From lines 7-11:

| Spec Type | Conditional Sections to Include |
|-----------|---------------------------------|
| **Portification** | Section 9 (Migration & Rollout), Section 5 (Interface Contracts), Section 5.2 (Gate Criteria), Section 5.3 (Phase Contracts), Section 8.3 (Manual/E2E Tests) |
| **Refactoring** | Section 4.3 (Removed Files), Section 9 (Migration & Rollout) |
| **New feature** | Section 4.5 (Data Models), Section 5.1 (CLI Surface), Section 5 (Interface Contracts) |
| **Infrastructure** | Section 5.3 (Phase Contracts), Section 8.3 (Manual/E2E Tests) |

### 2.5 All Sections — Purpose and Content Format

| # | Section Title | Purpose | Content Format | Conditional? |
|---|--------------|---------|---------------|-------------|
| 1 | Problem Statement | What problem, why it matters | 1.1 Evidence (table: Evidence/Source/Impact), 1.2 Scope Boundary (In scope / Out of scope) | No |
| 2 | Solution Overview | High-level approach | 2.1 Key Design Decisions (table: Decision/Choice/Alternatives/Rationale), 2.2 Workflow/Data Flow (ASCII diagram) | No |
| 3 | Functional Requirements | Testable numbered requirements | FR-ID.N format (e.g., `FR-{{id}}.1`), each with Description, Acceptance Criteria (checkboxes), Dependencies | No |
| 4 | Architecture | File changes + module graph | 4.1 New Files (table), 4.2 Modified Files (table), 4.3 Removed Files (table) **[CONDITIONAL: refactoring, portification]**, 4.4 Module Dependency Graph (ASCII), 4.5 Data Models **[CONDITIONAL: new_feature, portification]** (code block), 4.6 Implementation Order (numbered + rationale) | Partial |
| 5 | Interface Contracts | API/CLI/Gate definitions | 5.1 CLI Surface **[CONDITIONAL: new_feature, portification]**, 5.2 Gate Criteria **[CONDITIONAL: portification]** (table: Step/Gate Tier/Frontmatter/Min Lines/Semantic Checks), 5.3 Phase Contracts **[CONDITIONAL: portification, infrastructure]** (YAML) | Yes |
| 6 | Non-Functional Requirements | NFR table | Table: ID (NFR-ID.N format), Requirement, Target, Measurement | No |
| 7 | Risk Assessment | Risk matrix | Table: Risk/Probability/Impact/Mitigation | No |
| 8 | Test Plan | Testing breakdown | 8.1 Unit Tests (table: Test/File/Validates), 8.2 Integration Tests (table), 8.3 Manual/E2E Tests **[CONDITIONAL: infrastructure, portification]** (table: Scenario/Steps/Expected) | Partial |
| 9 | Migration & Rollout | Transition plan | Breaking changes, Backwards compatibility, Rollback plan | Yes (refactoring, portification) |
| 10 | Downstream Inputs | Pipeline integration | Subsections: For sc:roadmap, For sc:tasklist | No |
| 11 | Open Items | Unresolved questions | Table: Item/Question/Impact/Resolution Target | No |
| 12 | Brainstorm Gap Analysis | Auto-populated gaps | Table: Gap ID/Description/Severity/Affected Section/Persona + summary | No |
| App A | Glossary | Domain terms | Table: Term/Definition | Conditional (all types, if terminology used) |
| App B | Reference Documents | External refs | Table: Document/Relevance | Conditional (all types, if refs needed) |

### 2.6 Content Format Expectations

- **Functional Requirements**: Must use `FR-{{id}}.N` numbering with "shall/must" language implied by acceptance criteria checkboxes
- **Non-Functional Requirements**: Must use `NFR-{{id}}.N` numbering
- **Tables**: All use pipe-delimited markdown tables
- **Diagrams**: ASCII in code blocks or YAML in code blocks (no mermaid in this template)
- **Acceptance Criteria**: Checkbox format `- [ ] criterion`

---

## 3. Pipeline-Critical vs Minimal Sections

### 3.1 TDD Template — Pipeline Extraction Priority

**Must be RICH for pipeline** (task builder needs to populate these fully):

| Section | Why Pipeline-Critical |
|---------|----------------------|
| **5 Technical Requirements** | FR-001 IDs are extracted; acceptance criteria feed task generation |
| **6 Architecture** | Module graph and design decisions feed roadmap extraction |
| **7 Data Models** | Schema definitions feed implementation tasks |
| **8 API Specifications** | Endpoint contracts feed integration test generation |
| **15 Testing Strategy** | Test pyramid and cases feed QA task generation |
| **19 Migration & Rollout** | Rollout stages and rollback feed deployment tasks |
| **20 Risks & Mitigations** | Risk matrix feeds risk-tracking in sprint |
| **24 Release Criteria** | DoD and release checklist feed gate validation |
| **25 Operational Readiness** | Runbook and on-call expectations feed ops readiness gates |

**Can be MINIMAL** (1-3 sentences, small table, or skipped for "User Auth Service" fixture):

| Section | Rationale |
|---------|-----------|
| 1 Executive Summary | Just needs 2-3 sentences |
| 9 State Management | Backend service — skip entirely |
| 10 Component Inventory | Backend service — skip entirely |
| 16 Accessibility | Backend service — skip entirely |
| 22 Open Questions | Can be "No open questions" |
| 26 Cost & Resource Estimation | Optional, short table |
| 27 References & Resources | 1-2 rows |
| 28 Glossary | 3-5 terms |

### 3.2 Release Spec Template — Pipeline Extraction Priority

**Must be RICH**:
- Section 3 (Functional Requirements) — FR-ID numbering is extracted by downstream tools
- Section 4 (Architecture) — File lists feed task generation
- Section 8 (Test Plan) — Test tables feed QA validation

**Can be MINIMAL**:
- Section 1 (Problem Statement) — 2-3 sentences + short evidence table
- Section 6 (Non-Functional Requirements) — 2-3 rows
- Section 11 (Open Items) — can be empty table
- Section 12 (Brainstorm Gap Analysis) — can be empty if auto-populated later

---

## 4. Placeholder & Sentinel Patterns

### 4.1 TDD Template Placeholders

**Pattern**: `[DESCRIPTOR]` — square brackets with ALL-CAPS or Title Case

**Sentinel fields requiring replacement before pipeline consumption**:
1. `feature_id`: Must not be `[FEATURE-ID]`
2. `spec_type`: Must be a valid enum value (not a placeholder)
3. `target_release`: Must not be `[version]`

**Fields allowed to remain empty**: `complexity_score`, `complexity_class` (computed by sc:roadmap), all `quality_scores` sub-fields (populated by sc:spec-panel)

### 4.2 Release Spec Template Sentinels

**Pattern**: `{{SC_PLACEHOLDER:descriptor}}` — double-brace with `SC_PLACEHOLDER:` prefix

**Sentinel self-check command**: `grep -c '{{SC_PLACEHOLDER:' <output-file>` must return `0`

**All sentinel instances in the template** (by section):
- Frontmatter: 12 distinct sentinels
- Section 1: `problem_description`, `evidence_1`, `source`, `impact`, `in_scope`, `out_of_scope`
- Section 2: `solution_overview`, `decision_1`, `choice`, `alternatives`, `rationale`, `flow_diagram`
- Section 3: `id` (repeated), `requirement_title`, `what_it_does`, `criterion_1`, `criterion_2`, `dependencies_or_none`, `repeat_pattern`
- Section 4: `file_path`, `purpose`, `deps`, `change_description`, `why`, `target`, `reason`, `migration_notes`, `dependency_diagram`, `data_model_code`, `first_step`, `second_step`, `parallel_step`, `third_step`, `rationale`
- Section 5: `cli_usage`, `option`, `type`, `default`, `desc`, `step`, `tier`, `fields`, `n`, `checks`, `contract_schema`
- Section 6: `id` (NFR), `requirement`, `target`, `how_measured`
- Section 7: `risk_1`, `low_med_high`, `mitigation`
- Section 8: `test_name`, `file_path`, `what_it_validates`, `scenario`, `steps`, `expected`
- Section 9: `yes_no_details`, `strategy`, `plan`
- Section 10: `themes_and_milestones`, `task_breakdown_guidance`
- Section 11: `item`, `question`, `impact`, `target`
- Section 12: `gap_id`, `description`, `high_medium_low`, `affected_section`, `persona`, `gap_analysis_summary`
- Appendices: `term`, `definition`, `doc_path`, `why_relevant`

### 4.3 Key Differences Between Templates

| Aspect | TDD Template | Release Spec Template |
|--------|-------------|----------------------|
| Placeholder format | `[DESCRIPTOR]` (square brackets) | `{{SC_PLACEHOLDER:descriptor}}` (double-brace sentinels) |
| Sentinel self-check | 3 specific field checks (feature_id, spec_type, target_release) | grep for zero remaining `{{SC_PLACEHOLDER:` |
| Size | ~1274 lines, 28 sections | ~265 lines, 12 sections |
| Quality gate | `/sc:spec-panel --focus correctness,architecture --mode critique` | `/sc:spec-panel --focus correctness,architecture` and `--mode critique` |
| Tiered usage | Lightweight / Standard / Heavyweight | Single tier, conditional sections by spec_type |
| Conditional mechanism | `*(if applicable)*` annotations on section titles | `[CONDITIONAL: type1, type2]` annotations |
| Diagram format | Mermaid + ASCII | ASCII only |

---

## 5. Summary

### For Test Fixture Population ("User Authentication Service")

**TDD fixture requirements**:
- Populate all 30 frontmatter fields. Critical sentinels: `feature_id` (e.g., `AUTH-001`), `spec_type` (`new_feature`), `target_release` (e.g., `v4.3.0`)
- Sections 5, 6, 7, 8, 15, 19, 20, 24, 25 need rich content with proper FR-001 numbering, data model definitions, API endpoint specs, test tables, risk matrices
- Sections 9, 10, 16 can be skipped (backend service, not frontend)
- Sections 1, 22, 27, 28 can be minimal (1-3 sentences each)
- All `[bracket]` placeholders must be replaced with auth-domain content

**Release spec fixture requirements**:
- Populate all 16 frontmatter fields by replacing `{{SC_PLACEHOLDER:*}}` sentinels
- Use `spec_type: new_feature` to include Sections 4.5 and 5.1 conditionally
- Section 3 must use `FR-AUTH.1`, `FR-AUTH.2` numbering pattern
- Section 8 must have Unit and Integration test tables populated
- After population, `grep -c '{{SC_PLACEHOLDER:'` must return 0

**Key insight for the task builder**: The TDD template is approximately 5x larger than the release spec template. For E2E pipeline tests, the release spec is likely the more practical fixture to fully populate, while the TDD fixture can use the Lightweight tier (sections 1, 2, 3, 6.4, 21, 22 only) to keep test fixtures manageable.
