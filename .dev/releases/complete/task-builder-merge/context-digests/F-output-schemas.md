# Bucket F — output schemas content digest

## Files read
| Path | Lines | Status |
|------|-------|--------|
| `src/superclaude/examples/release-spec-template.md` | 264 (read fully) | OK |
| `src/superclaude/examples/prd_template.md` | 1389 (read in chunks 1-300, 300-700, 700-1100, 1100-end) | OK |
| `.dev/releases/archive/v2.13b-GPTGen-Compared/release-spec.md` | 655 (frontmatter + section index + AC sample) | OK |
| `.dev/releases/backlog/v4.xx-SprintReportScaffolding/release-spec.md` | 543 (frontmatter + section index + AC sample) | OK |
| `.dev/releases/complete/v2.13-CLIRunner-PipelineUnification/release-spec.md` | 655 (frontmatter + section index + AC sample) | OK |

## Files absent
None.

## release-spec-template.md
### Frontmatter fields
YAML block at lines 19–39 (release-spec-template.md:19-39).

| Field | Type | Required | Example | Source line |
|-------|------|----------|---------|-------------|
| title | string | yes | `"{{SC_PLACEHOLDER:spec_title}}"` | :21 |
| version | string | yes | `"1.0.0"` (hardcoded) | :22 |
| status | enum | yes | `draft` | :23 |
| feature_id | id | yes | `{{SC_PLACEHOLDER:fr_id}}` | :24 |
| parent_feature | id\|null | yes | placeholder | :25 |
| spec_type | enum | yes | `new_feature_or_refactoring_or_portification_or_migration_or_infrastructure_or_security_or_performance_or_docs` | :26 |
| complexity_score | float 0.0-1.0 | yes | placeholder | :27 |
| complexity_class | enum LOW/MEDIUM/HIGH | yes | placeholder | :28 |
| target_release | version | yes | placeholder | :29 |
| authors | list | yes | `[user, claude]` | :30 |
| created | date yyyy_mm_dd | yes | placeholder | :31 |
| quality_scores.clarity | float 0.0-10.0 | yes | placeholder | :33 |
| quality_scores.completeness | float 0.0-10.0 | yes | placeholder | :34 |
| quality_scores.testability | float 0.0-10.0 | yes | placeholder | :35 |
| quality_scores.consistency | float 0.0-10.0 | yes | placeholder | :36 |
| quality_scores.overall | float 0.0-10.0 | yes | placeholder | :37 |

All 16 fields requested in the prompt are present. Header sentinel comment at :15 mandates `grep -c '{{SC_PLACEHOLDER:'` must return 0.

### Section order (file:line)
1. `## 1. Problem Statement` :41
2. `### 1.1 Evidence` :47
3. `### 1.2 Scope Boundary` :55
4. `## 2. Solution Overview` :63
5. `### 2.1 Key Design Decisions` :69
6. `### 2.2 Workflow / Data Flow` :77
7. `## 3. Functional Requirements` :85
8. `## 4. Architecture` :103 (subsections 4.1 New Files :105, 4.2 Modified Files :113, 4.3 Removed Files [CONDITIONAL] :121, 4.4 Module Dependency Graph :129, 4.5 Data Models [CONDITIONAL] :135, 4.6 Implementation Order :143)
9. `## 5. Interface Contracts [CONDITIONAL]` :154 (5.1 CLI Surface :158, 5.2 Gate Criteria :168, 5.3 Phase Contracts :176)
10. `## 6. Non-Functional Requirements` :184
11. `## 7. Risk Assessment` :190
12. `## 8. Test Plan` :196 (8.1 Unit :198, 8.2 Integration :204, 8.3 Manual/E2E [CONDITIONAL] :210)
13. `## 9. Migration & Rollout [CONDITIONAL]` :216
14. `## 10. Downstream Inputs` :224 (sc:roadmap :228, sc:tasklist :231)
15. `## 11. Open Items` :234
16. `## 12. Brainstorm Gap Analysis` :242
17. `## Appendix A: Glossary [CONDITIONAL]` :254
18. `## Appendix B: Reference Documents [CONDITIONAL]` :260

Order matches the expected order in the prompt.

### Per-section requirements
- **Problem Statement** (:41-61): Narrative block, then `### 1.1 Evidence` table (Evidence/Source/Impact :51-53), then `### 1.2 Scope Boundary` with **In scope** / **Out of scope** bullets (:59-61).
- **Constraints**: No dedicated "Constraints" section. Constraints surface implicitly via Risk Assessment (§7) and Scope Boundary (§1.2). Explicit absence.
- **FRs / Acceptance Criteria** (:85-101): Pattern is `### FR-{id}.N: {title}` → `**Description**:` → `**Acceptance Criteria**:` as checkbox list → `**Dependencies**:`. Quote at :93-95:
  > `**Acceptance Criteria**:\n- [ ] {{SC_PLACEHOLDER:criterion_1}}\n- [ ] {{SC_PLACEHOLDER:criterion_2}}`
  
  The template does NOT use the phrases "observable behavior", "verification method", or "negative criterion" — verified by absence in the full 264-line read. Acceptance criteria are unstructured checkbox bullets; no required sub-fields.
- **NFRs** (:184-188): Table with columns ID / Requirement / Target / Measurement. IDs follow `NFR-{id}.N` (:188).
- **Risks/Assumptions** (:190-194): Table with Risk / Probability / Impact / Mitigation. Probability+Impact use `low_med_high` enum (:194). No separate Assumptions section.
- **Test Plan** (:196-214): Three sub-tables — Unit (Test/File/Validates), Integration (Test/Validates), Manual/E2E [CONDITIONAL] (Scenario/Steps/Expected Outcome).
- **Markers**: Placeholder convention is `{{SC_PLACEHOLDER:<name>}}` (every blank). Conditional sections marked `[CONDITIONAL: <spec_types>]` in headings (e.g. :121, :135, :154, :158, :168, :176, :210, :216, :254, :260). No `<!-- REQUIRED -->` markers exist (verified absent).

## prd_template.md
### Frontmatter fields (prd_template.md:1-40)
YAML between `---` markers at :1 and :40. Fields: `id` :2, `title` :3, `description` :4, `version` :5, `status` :6 (`"🟡 Draft"`), `type` :7, `priority` :8, `created_date` :9, `updated_date` :10, `assigned_to` :11, `autogen` :12, `autogen_method` :13, `coordinator` :14, `parent_task` :15, `depends_on` :16-17, `related_docs` :18-19, `tags` :20-25, `template_schema_doc` :26, `estimation` :27, `sprint` :28, `due_date` :29, `start_date` :30, `completion_date` :31, `blocker_reason` :32, `ai_model` :33, `model_settings` :34, `review_info.{last_reviewed_by,last_review_date,next_review_date}` :35-38, `task_type` :39.

### Section list in order
Table of Contents at prd_template.md:121-150 enumerates 28 sections: 1 Executive Summary :123, 2 Problem Statement :124, 3 Background & Strategic Fit :125, 4 Product Vision :126, 5 Business Context :127, 6 JTBD :128, 7 User Personas :129, 8 Value Proposition Canvas :130, 9 Competitive Analysis :131, 10 Assumptions & Constraints :132, 11 Dependencies :133, 12 Scope Definition :134, 13 Open Questions :135, 14 Technical Requirements :136, 15 Technology Stack :137, 16 UX Requirements :138, 17 Legal & Compliance :139, 18 Business Requirements :140, 19 Success Metrics & Measurement :141, 20 Risk Analysis :142, 21 Implementation Plan :143, 22 Customer Journey Map :144, 23 Error Handling & Edge Cases :145, 24 User Interaction & Design :146, 25 API Contract Examples :147, 26 Contributors & Collaboration :148, 27 Related Resources :149, 28 Maintenance & Ownership :150. Body section anchors confirmed (e.g. §1 :154, §2 :166, §21 :854, §28 :1232). Appendices A-E and Document History at :1263-1300.

### Acceptance section shape
Acceptance criteria appear per User Story (:881-884) and per Feature (:927-930) as `✅ [Criterion]` or plain bullet lists. Quote :881-884:
> `**Acceptance Criteria:**\n- ✅ [Criterion 1]\n- ✅ [Criterion 2]\n- ✅ [Criterion 3]`

Each Feature block also requires `Success Metrics:` :886-888 / :932-933.

### Required inputs / variables
Template uses bracketed placeholders `[…]` (e.g. `[Product Name]`, `[Date]`, `[X]`), not `{{SC_PLACEHOLDER:}}`. Tiered Usage table :57-62 defines Lightweight / Standard / Heavyweight selections.

### WHAT / WHY / HOW input mode
prd_template.md:44-46 declares three required summary lines at the document head:
> `> **WHAT:** [One sentence — what this document contains…]`
> `> **WHY:** [One sentence — why this document exists…]`
> `> **HOW TO USE:** [One sentence — who should use it and when…]`

(Note: prompt asked WHAT/WHY/WHERE/OUTPUT — actual template uses **WHAT/WHY/HOW TO USE**. There is no WHERE or OUTPUT marker in this template.) Content rules block at :1331-1336 codifies "PRD defines WHAT to build and WHY — not HOW (that belongs in the TDD)".

## Sample release-spec deviations

### `.dev/releases/archive/v2.13b-GPTGen-Compared/release-spec.md` (655 lines)
- **Frontmatter** (:1-17): Uses fields `title, version, status, decision_source, decision_option, generated_by, generated_date, expert_panel, scope, complexity_class, domain_distribution.{backend,testing}, primary_persona, consulting_personas`. Missing template-mandated fields: `feature_id`, `parent_feature`, `spec_type`, `complexity_score`, `target_release`, `authors`, `created`, `quality_scores.*`. Adds non-template fields: `decision_source`, `decision_option`, `generated_by`, `generated_date`, `expert_panel`, `scope`, `domain_distribution`, `primary_persona`, `consulting_personas`.
- **Section list**: 1 Executive Summary, 2 Background & Decision Record, 3 Deliverables, 4 Milestone Structure, 5 Non-Functional Requirements, 6 Risk Register, 7 Out of Scope (Deferred), 8 Phased Extraction Roadmap (Future), 9 Design Details, 10 Success Metrics. Diverges sharply from template (no Problem Statement §1, no Solution Overview §2, no Architecture §4 numbering, no Interface Contracts §5, no Test Plan §8, no Migration §9, no Downstream Inputs §10, no Open Items §11, no Brainstorm Gap Analysis §12).
- **AC style** (:89-95): Numbered `AC-N` bullets inline under each Deliverable. Quote:
  > `- AC-1: Sprint ClaudeProcess no longer overrides start(), wait(), or terminate()`
  
  Followed by `**Verification**:` block (:97-100) listing test approaches. This is more concrete than template's empty checkboxes.
- **Notable**: Adds Verification + Estimated Reduction sub-blocks per deliverable; uses Risk Register naming; collapses requirements into Deliverable blocks.

### `.dev/releases/backlog/v4.xx-SprintReportScaffolding/release-spec.md` (543 lines)
- **Frontmatter** (:1-19): Same shape as archive sample plus `origin`, `origin_plan`, `dependency`. Same template field gaps.
- **Section list**: 1 Executive Summary, 2 Background, 3 Deliverables, 4 Milestone Structure, 5 Non-Functional Requirements, 6 Status Outcome Matrix, 7 Risk Register, 8 Files Modified, 9 Success Metrics, 10 Out of Scope (Deferred). Plus embedded protocol sections (Per-Task Status, Completion Protocol, Reporting Protocol) at :153-325 used as scaffold prose examples, not spec structure.
- **AC style** (:119-124): Identical `AC-N` numbered bullets pattern. Quote:
  > `- AC-1: parse_phase_tasks() correctly extracts task ID, title, and tier from phase tasklist files matching the format used by /sc:tasklist`
  
  Includes "Primary acceptance scenario (per Adzic review)" framing at :401.
- **Notable additions**: Adds Status Outcome Matrix §6; cites expert panel reviewers (Fowler/Adzic) as rationale anchors.

### `.dev/releases/complete/v2.13-CLIRunner-PipelineUnification/release-spec.md` (655 lines)
- Byte-for-byte equivalent to archive sample on read lines 1-80 and section index. Same frontmatter (:1-17), same section list (10 sections), same AC style (`AC-N` with Verification block at :89-100).

## Reconciliation
The official template (`release-spec-template.md`) is **authoritative for Phase 6**. All three sample specs were emitted by `/sc:spec-panel` and predate (or diverge from) the canonical template — they share a 10-section schema (Executive Summary → Background → Deliverables → Milestone Structure → NFRs → Risk Register → Out of Scope → Roadmap → Design Details → Success Metrics) that does NOT match the template's 12-section schema (Problem Statement → Solution Overview → FRs → Architecture → Interface Contracts → NFRs → Risk Assessment → Test Plan → Migration & Rollout → Downstream Inputs → Open Items → Brainstorm Gap Analysis). The samples also omit the template's full quality_scores frontmatter and 8 other required frontmatter fields.

Per orchestration spec, Phase 6 must "Populate frontmatter exactly as the template defines them — if the template adds or renames fields between now and execution, match the template." Therefore Phase 6 MUST follow `release-spec-template.md` lines 19-39 frontmatter and lines 41-264 section order. Samples are illustrative only for tone, acceptance criterion granularity (AC-N numbered bullets with Verification blocks are a useful pattern to lift), and Deliverable-grouping style — but the canonical section headings and the full frontmatter field set are non-negotiable.

Specifically, useful sample patterns to lift while staying template-compliant:
- AC-N numbered acceptance criteria (more testable than template's empty checkboxes) — can be slotted under `## 3. Functional Requirements` FR blocks.
- `**Verification**:` sub-block per FR (clarifies how AC is tested) — compatible with template.
- Decision-source frontmatter references (`decision_source`, `decision_option`) — may be added as supplementary fields without removing template-mandated ones.

## evidence_status
`complete`. All 5 prompt-named files read; template frontmatter (16 fields) and section list (12 sections + appendices) fully enumerated; three sample specs surveyed for frontmatter, section list, and AC style with one quoted AC per sample.
