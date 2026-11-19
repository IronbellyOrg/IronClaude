---
id: ""
title: ""
description: "Phased roadmap for building something from user input"
version: ""
status: "ud83dudfe1 Draft"
type: "ud83duddfa Roadmap"
priority: "ud83dudd3c High"
created_date: "YYYY-MM-DD"
updated_date: "YYYY-MM-DD"
assigned_to: ""
autogen: false
autogen_method: ""
coordinator: ""
parent_doc: ""
parent_task: ""
depends_on: []
related_docs: []
related_prd: ""
related_tdd: ""
tags:
- roadmap
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
task_type: static
template_name: "Roadmap"
template_version: "1.0.0"
sections: 12
placeholder_prefix: "RF_PLACEHOLDER"
---

# Roadmap: {{RF_PLACEHOLDER:project_name}}

## Metadata
- **Source input:** {{RF_PLACEHOLDER:source_input_description}}
- **Source path(s):** {{RF_PLACEHOLDER:source_input_paths}}
- **Created:** {{RF_PLACEHOLDER:created_date}}
- **Total phases:** {{RF_PLACEHOLDER:total_phases}}
- **Total tasks:** {{RF_PLACEHOLDER:total_task_count}}
- **Estimated scope:** {{RF_PLACEHOLDER:estimated_scope}}
- **Estimated duration:** {{RF_PLACEHOLDER:estimated_duration}}

<!-- GUIDANCE: Metadata field formats:
     - source_input_description: 1-line summary of what was provided (e.g., "TDD document, 2777 lines")
     - source_input_paths: comma-separated repo-relative paths (e.g., "docs/tdd.md, docs/prd.md")
     - created_date: YYYY-MM-DD format
     - total_phases: integer (e.g., 5)
     - total_task_count: integer — count of unique T<phase>.<seq> task IDs across all phases in S4 (e.g., 23). This is independent of REQ/SPEC counts in S2.
     - estimated_scope: S/M/L with optional elaboration (e.g., "M — 3 subsystems, ~40 files")
     - estimated_duration: N-M weeks (e.g., "3-5 weeks")
     S/M/L scale (used for scope, complexity, and effort across S3/S4):
       S = small (1 subsystem, <10 files, <1 week)
       M = medium (2-4 subsystems, 10-40 files, 1-3 weeks)
       L = large (5+ subsystems, 40+ files, 3+ weeks) -->

---

## 1. Executive Summary

{{RF_PLACEHOLDER:executive_summary}}

<!-- GUIDANCE: 1-2 paragraph summary of what's being built and the phased approach.
     Should answer: What is being built? Why? How is the work phased? What's the
     expected outcome? Key architectural decisions? Critical path?
     -->

---

## 2. Input Analysis

{{RF_PLACEHOLDER:input_analysis}}

<!-- GUIDANCE: Summary of the user's input — what was provided (document type, length,
     structure), key requirements/features identified, scope boundaries detected,
     ambiguities noted. This section establishes the "contract" — what the roadmap
     must cover. Every item identified here must appear in the Coverage Traceability
     Matrix (Section 7).

     Requirements should be enumerated with IDs for traceability:
     | ID | Requirement/Feature | Source | Priority |
     |-----|---------------------|--------|----------|
     | REQ-001 | [requirement] | [section/line in input] | [Must/Should/Could] |

     When input includes a TDD, specifications should be enumerated with SPEC-NNN IDs
     in a separate table below the REQ table. Format:
     | ID | Specification | Source (TDD section) | Type |
     |-----|---------------|---------------------|------|
     | SPEC-001 | [specification] | [TDD section ref] | [entity/index/api/state/error/perf/test/deploy] |
     SPEC types include: entity, index, api, state, error, perf, test, deploy, security, observability. -->

---

## 3. Phase Overview

{{RF_PLACEHOLDER:phase_overview_table}}

<!-- GUIDANCE: Summary table of all phases.
     | Phase | Name | Goal | Duration | Dependencies | Key Deliverables | Complexity | Parallelizable |
     |-------|------|------|----------|-------------|------------------|------------|----------------|
     | 1 | [name] | [goal] | [est.] | None | [deliverables] | [S/M/L] | -- |
     | 2 | [name] | [goal] | [est.] | Phase 1 | [deliverables] | [S/M/L] | With Phase 3 |

     Complexity: S (1-2 task files), M (3-5 task files), L (6+ task files)
     Parallelizable: which phases can run concurrently (no mutual dependencies) -->

---

## 4. Phase Details

{{RF_PLACEHOLDER:phase_details}}

<!-- GUIDANCE: One subsection per phase. Each phase subsection MUST include ALL of
     these elements:

     ### Phase N: [Name]

     **Objective:** [1-2 sentence phase goal]
     **Duration:** [estimated time]
     **Entry Criteria:** [what must be true before this phase can start]
     **Exit Criteria:** [what must be true to consider this phase complete]
     **Dependencies:** [none, or prior phases with specific outputs needed]

     #### Task Table

     | # | ID | Task | Description | Depends On | Acceptance Criteria | Effort | Parallel |
     |---|-----|------|-------------|-----------|---------------------|--------|----------|
     | 1 | T01.01 | [task title] | [what to build/do] | -- | [pass/fail criteria] | S/M/L | -- |
     | 2 | T01.02 | [task title] | [what to build/do] | T01.01 | [pass/fail criteria] | M | -- |
     | 3 | T01.03 | [task title] | [what to build/do] | -- | [pass/fail criteria] | S | With T01.04 |

     Task IDs: T<phase>.<seq> (e.g., T01.03 = Phase 1, Task 3)
     Depends On: other task IDs, or "--" for none
     Effort: S (hours), M (1-2 days), L (3+ days)
     Parallel: which tasks within this phase can run concurrently

     #### Integration Points

     | Artifact | Type | Created By | Consumed By |
     |----------|------|-----------|-------------|
     | [e.g., "User schema"] | [e.g., "DB migration"] | T01.01 | T02.03, T03.01 |

     (Shows cross-phase wiring — what this phase produces that other phases need)
     If a phase has no cross-phase integration points, include the heading with a
     single line: "No cross-phase integration points for this phase."

     #### Key Deliverables
     - [deliverable 1 — specific file/component/feature]
     - [deliverable 2]

     Phase details must be specific enough that /task-builder can create a complete
     MDTM (Markdown Task Management) task file from each phase's build specification. Vague phases like "implement
     the backend" are not acceptable — specify WHAT in the backend, WHICH files,
     WHAT patterns. -->

---

## 5. Dependency Graph

{{RF_PLACEHOLDER:dependency_graph}}

<!-- GUIDANCE: ASCII diagram or structured table showing phase AND task dependencies.
     Must be acyclic.

     Phase-level:
     Phase 1 (Foundation) ─── Phase 2 (Core Logic) ─── Phase 4 (Integration)
                                    │
                              Phase 3 (API Layer) ─────────┘

     Task-level (cross-phase dependencies):
     | Source Task | Target Task | Dependency Type | Artifact |
     |-----------|-------------|-----------------|----------|
     | T01.01 | T02.03 | blocks | User schema migration |

     Parallelism annotations: identify phase groups that can run concurrently. -->

---

## 6. Task File Tracker

{{RF_PLACEHOLDER:task_file_tracker}}

<!-- GUIDANCE: This section is populated by the /roadmap skill AFTER task files are
     created via /task-builder. It tracks all generated task files, their status,
     and their dependencies.

     | Phase | Task File | BUILD_REQUEST | Status | Depends On | Blocks | Created |
     |-------|-----------|------------|--------|-----------|--------|---------|
     | 1 | [path or pending] | [build spec path] | [pending/created/in-progress/done] | -- | Phase 2, 3 | [date] |
     | 2 | [path or pending] | [build spec path] | [pending/created] | Phase 1 | Phase 4 | [date] |
     | 3 | [path or pending] | [build spec path] | [pending/created] | Phase 1 | Phase 4 | -- |

     Execution order: phases with no pending dependencies can be run. Phases marked
     "Parallelizable" in the Phase Overview can be started simultaneously once their
     shared dependencies are met.

     This table is the user's execution dashboard — it shows what's ready to run,
     what's blocked, and what's done. -->

---

## 7. Coverage Traceability Matrix

{{RF_PLACEHOLDER:coverage_traceability_matrix}}

<!-- GUIDANCE: Every requirement/feature/component and specification identified in Section 2 (Input
     Analysis) MUST appear here with at least one roadmap task covering it.
     Format:
     | Req/Spec ID | Requirement/Specification | Phase | Task ID(s) | Status |
     |-------------|--------------------------|-------|-----------|--------|
     | REQ-001 | [from Section 2] | 1 | T01.01, T01.02 | Covered |
     | SPEC-001 | [from Section 2 SPEC table] | 1 | T01.03 | Covered |

     Coverage: [X/Y] requirements covered ([percentage]%), [A/B] specifications covered ([percentage]%)

     Coverage Matrix tracks both REQ-NNN and SPEC-NNN. Each row maps one ID to its
     implementing task(s). Coverage target: 100% for both REQ and SPEC.

     100% forward coverage is REQUIRED. If any requirement or specification is uncovered, the roadmap
     is incomplete — add a phase or expand an existing phase to cover it.
     Backward check: every task must trace to at least one input requirement
     or specification (no orphan tasks / scope creep). -->

---

## 8. Risk Register

{{RF_PLACEHOLDER:risk_register}}

<!-- GUIDANCE: Risks identified during roadmap creation.
     | Risk | Severity | Probability | Phase(s) Affected | Mitigation | Contingency |
     |------|----------|------------|-------------------|------------|-------------|
     Severity: Critical (blocks progress), High (degrades quality), Medium (manageable),
     Low (minor inconvenience)
     -->

---

## 9. Resource Requirements

{{RF_PLACEHOLDER:resource_requirements}}

<!-- GUIDANCE: What's needed to execute this roadmap.
     | Resource | Phase(s) | Notes |
     |----------|---------|-------|
     | [external dependency, tool, API key, etc.] | [which phases] | [details] |

     Also note any external dependencies that phases are waiting on. -->

---

## 10. Open Questions

{{RF_PLACEHOLDER:open_questions}}

<!-- GUIDANCE: Questions that emerged during roadmap creation that need user input
     before or during task execution. These are genuine unknowns, not things
     answerable from the input.
     | # | Question | Impact | Blocking Phase(s) | Suggested Resolution |
     |---|----------|--------|-------------------|---------------------|

     Open questions that block a phase MUST be resolved before that phase's task
     file can be executed. The /roadmap skill should flag blocking OQs to the user
     before generating build specifications for blocked phases. -->

---

## 11. Architectural Debt & Post-Completion Items

{{RF_PLACEHOLDER:architectural_debt}}

<!-- GUIDANCE: Known shortcuts, deferred decisions, or technical debt that the roadmap
     intentionally creates. These should be addressed after the roadmap phases complete.
     | Item | Reason Deferred | Impact if Not Addressed | Suggested Timeline |
     |------|----------------|------------------------|-------------------|
     -->

---

<!-- LINE BUDGET: Populated roadmap documents should target 300-800 lines depending
     on project complexity. Phase Details (S4) will be the longest section. -->

<!-- CONTENT RULES:
     - Every requirement and specification from S2 must appear in S7 (Coverage Traceability Matrix)
     - Every task ID in S4 must use T<phase>.<seq> format (e.g., T01.03)
     - Dependency graph in S5 must be acyclic
     - S6 (Task File Tracker) is initially generated with placeholder rows matching S3 phases (1:1), then populated with actual paths/status post-creation (via /task-builder)
     - 100% forward coverage in S7 is mandatory — no uncovered requirements or specifications
     - Phase details in S4 must be specific enough for /task-builder consumption
     - Every phase row in S3 must have a corresponding subsection in S4 and a row in S6 (1:1 match)
     - S8 Risk Register: Critical-severity risks without mitigation must appear in S10 as blocking open questions
     - S10 blocking phase references must match phases defined in S3
     - Every phase-level dependency in S3 must be grounded by at least one task-level dependency in S4 (e.g., if S3 says Phase 2 depends on Phase 1, at least one task in Phase 2's table must have Depends On referencing a Phase 1 task ID)
     - Every task ID cited in S7 (Coverage Traceability Matrix) must reference a valid task ID defined in an S4 Task Table — no phantom task IDs
     - S4 Integration Points cross-phase references ("Consumed By" column) must be consistent with S5 dependency entries — if S4 says task T01.01 is consumed by T02.03, S5 must include a corresponding dependency entry -->

<!-- FILE NAMING CONVENTION:
     Output files: ROADMAP-<project_name>.md (SCREAMING_SNAKE_CASE)
     Example: ROADMAP-TASK_MANAGEMENT_SYSTEM.md -->
