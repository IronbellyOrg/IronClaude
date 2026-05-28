---
id: "TASK-RF-20260527055700-spec-fidelity-canonicalizer"
title: "Apply spec-fidelity canonicalization fix to structural_checkers.py + add regression tests"
description: "Implement the adversarially-merged spec-fidelity convergence fix: add the _canonicalize_requirement_id helper, modify the phantom_id block in check_signatures to compare canonical sets and emit MEDIUM id_schema_drift findings (instead of HIGH phantom_id) when surface forms differ but canonical forms match, add the corresponding SEVERITY_RULES + FIX_GUIDANCE_TEMPLATES entries, then add 5 golden-fixture unit tests + 1 property-based unit test (NEW file) + 1 flatline-halt integration test + 1 cross-cutting integration test on the remediate executor. Lands the fix that unblocks the TUIBBS v1-MVP roadmap convergence (54 active HIGHs → 0)."
status: "🟢 Done"
type: "🛠️ Bug Fix"
priority: "🔼 High"
created_date: "2026-05-27"
updated_date: "2026-05-27"
completion_date: "2026-05-27"
assigned_to: "rf-task-executor"
autogen: false
autogen_method: ""
coordinator: orchestrator
parent_task: "TROUBLESHOOT-spec-fidelity-deep-dive-20260527045400"
depends_on: []
related_docs:
- path: ".dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/01-troubleshoot-report.md"
  description: "Full sc:troubleshoot --depth deep REPORT.md with diagnosis, evidence (18 citations), proposed fix, risk + rollback"
- path: ".dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md"
  description: "Adversarial-merged fix specification with 4 Changes + restriction compliance audit"
- path: ".dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/03-refactor-plan-concrete-changes.md"
  description: "Refactoring plan with concrete code snippets for each of the 4 Changes"
- path: ".dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/04-self-review-no-blockers.md"
  description: "Wave 4 self-review: APPROVED, 0 blockers, 4 non-blocking concerns"
- path: ".dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/05-restrictions-doc-context.md"
  description: "Documentation Context Card with 7 binding restrictions + 3 re-frame signals"
- path: ".dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/06-invariant-probe.md"
  description: "Round 2.5 fault-finder analysis (INV-001 through INV-006); INV-003 does NOT apply to the merged fix"
- path: ".dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/07-historical-context.md"
  description: "Phase 0 archaeology: 5 sections + 5 pattern bullets across past releases"
- path: ".dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/08-evidence-validation.md"
  description: "Inline evidence-validator pass: 18/18 file:line citations re-Read and verified verbatim"
tags:
- "bug-fix"
- "spec-fidelity"
- "convergence"
- "structural-checkers"
- "canonicalization"
- "regression-tests"
template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"
estimation: ""
sprint: ""
due_date: ""
start_date: "2026-05-27"
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: static
---

# Apply spec-fidelity canonicalization fix to structural_checkers.py + add regression tests

## Task Overview

The TUIBBS v1-MVP roadmap pipeline halts at the `spec-fidelity` step with `Convergence not reached after 3 runs. Remaining active HIGHs: 54`. All 54 ACTIVE HIGHs are identical-shape `phantom_id` findings driven by an asymmetric ID extraction/comparison pattern: the spec parser's regex at `spec_parser.py:329` (`\bD-?\d+\b`) matches both `D1` and `D01` leniently, but the comparator in `structural_checkers.py:380` compares the resulting sets via raw set difference. Spec has `{D1, D3, D5}`; roadmap has `{D01, …, D54}`. The set difference flags all 54 as phantoms.

This task implements the adversarially-merged minimum-viable fix that addresses the immediate trigger (comparator asymmetry) AND adds the test infrastructure that catches future asymmetric-form drift at construction. The fix has been adversarially debated across 5 variants, evidence-validated (18/18 file:line citations re-Read), and self-reviewed (no blockers). Two production-code changes in `src/superclaude/cli/roadmap/structural_checkers.py` (canonicalization helper + `phantom_id` block modification + `SEVERITY_RULES` entry + `FIX_GUIDANCE_TEMPLATES` entry) plus four test changes (5 golden-fixture tests + property-based test + flatline-halt regression test + cross-cutting integration test) across `tests/roadmap/`. Expected outcome: 54 HIGHs → 0 HIGHs + 54 MEDIUMs in Run 1; convergence passes.

## Key Objectives

The following objectives MUST be achieved by this task:

1. **Add `_canonicalize_requirement_id` helper:** A pure `(family: str, raw: str) -> str` function in `structural_checkers.py` that strips leading zeros within the numeric tail while preserving family prefix and sub-ID structure, mirroring the precedent at `integration_contracts.py:445`.
2. **Modify the `phantom_id` block in `check_signatures`:** Compare canonical sets; emit drift findings as MEDIUM `id_schema_drift`; preserve HIGH `phantom_id` for genuine missing IDs whose canonical form is NOT in the spec. Add the corresponding `SEVERITY_RULES` and `FIX_GUIDANCE_TEMPLATES` entries.
3. **Add 5 golden-fixture asymmetric-ID unit tests:** Cover all 5 requirement families (FR, NFR, SC, G, D) with both zero-pad and sub-ID drift cases; regression-lock genuine-phantom detection.
4. **Add a property-based unit test + flatline-halt integration test + cross-cutting integration test:** Family-agnostic property test (NEW file with `pytest.importorskip("hypothesis")`); flatline-halt regression test for the convergence loop on the TUIBBS shape; cross-cutting integration test for the all-fixes-unfixable scenario.
5. **Validate restrictions:** All 7 restrictions in `research/05-restrictions-doc-context.md` MUST hold post-implementation (module ownership, pure-function contract, ≤30% per-patch diff guard, binary pass predicate at `convergence.py:539` untouched, spec immutable, `max_runs=3` untouched, mirrors `integration_contracts.py:445` pattern).

## Prerequisites & Dependencies

### Parent Task & Dependencies

- **Parent Task:** TROUBLESHOOT-spec-fidelity-deep-dive-20260527045400 - sc:troubleshoot --depth deep --fix pipeline that produced the merged fix specification.
- **Blocking Dependencies:** None — research is complete, evidence is verified, self-review is APPROVED.
- **This task blocks:** TUIBBS v1-MVP roadmap convergence (downstream — not in this repo).

### Previous Stage Outputs (MANDATORY INPUTS)

**INFORMATIONAL ONLY - NO CHECKLIST ITEMS HERE**

The actual checklist items for reading these outputs appear in Phase 2 (embedded in each Change item).

**Required Previous Stage Outputs:**

- **Merged Fix Specification:** `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` - Authoritative description of the 4 Changes including expected outcome and restriction compliance audit.
- **Refactoring Plan:** `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/03-refactor-plan-concrete-changes.md` - Concrete code snippets for each Change (helper definition, phantom_id block replacement, test list, target file paths).
- **Restrictions Doc Context:** `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/05-restrictions-doc-context.md` - The 7 binding restrictions that Phase 6 (Restrictions Audit) must verify.
- **Troubleshoot REPORT.md:** `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/01-troubleshoot-report.md` - Full diagnosis with 18 verified file:line citations; canonical reference for root-cause framing.
- **Evidence Validation:** `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/08-evidence-validation.md` - 18/18 citations re-Read and verified; provides the file:line ground truth used by Change items.

### Handoff File Convention

This task uses intra-task handoff patterns. Items write intermediate outputs to:
**`.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/`**

Subdirectories:

- `discovery/` - Discovery scan results and inventories (Phase 2)
- `test-results/` - Test output and summaries (Phase 4, Phase 5)
- `reviews/` - Quality review verdicts (Phase 6 Restrictions Audit + Phase 7 QA gate)
- `plans/` - Fix plans and conditional action outputs
- `reports/` - Aggregated reports and summaries

These files persist across all batches and session rollovers. Later items read them by path.

### Frontmatter Update Protocol

YOU MUST update the frontmatter at these MANDATORY checkpoints:

- **Upon Task Start:** Update `status` to "🟠 Doing" and `start_date` to current date
- **Upon Completion:** Update `status` to "🟢 Done" and `completion_date` to current date
- **If Blocked:** Update `status` to "⚪ Blocked" and populate `blocker_reason`
- **After Each Work Session:** Update `updated_date` to current date

DO NOT modify any other frontmatter fields unless explicitly directed by the user.

## Execution Context

<!-- Reading aid for the executor. Per-item Context fields below carry the load-bearing file:line citations. -->

- **References:** R-001 merged fix spec (`research/02-merged-fix-spec.md`); R-002 refactor plan (`research/03-refactor-plan-concrete-changes.md`); R-003 troubleshoot REPORT (`research/01-troubleshoot-report.md`); R-004 restrictions context (`research/05-restrictions-doc-context.md`); R-005 evidence validation (`research/08-evidence-validation.md`).
- **Source areas:** the structural_checkers module (canonicalization helper + phantom_id block + severity tables); the integration_contracts precedent module (mirror pattern at `_canonicalize_identifiers`); the convergence loop module (binary pass predicate that must remain untouched); the remediate executor module (30% diff guard that must remain untouched); the roadmap test suite under tests/roadmap/.
- **Key constraints:** binary pass predicate `active_high_count == 0` MUST remain untouched; per-patch diff <30% on `structural_checkers.py`; both `make lint` and `make format` MUST pass; `uv run pytest tests/roadmap/ -v` MUST pass with no regressions; all 7 restrictions in `research/05-restrictions-doc-context.md` MUST hold.

---

## Detailed Task Instructions

### Phase 1: Preparation and Setup

YOU MUST complete EVERY item in this checklist IN ORDER. DO NOT skip ahead. Mark each item as complete before proceeding to the next.

**Step 1.1:** Update task status

- [x] Update status to "🟠 Doing" and start_date to current date in frontmatter of this file, then add a timestamped entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task started: Updated status to "🟠 Doing" and start_date.` Once done, mark this item as complete.

**Step 1.2:** Create handoff directories

- [x] Create the phase-outputs directory structure at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/` with subdirectories `discovery/`, `test-results/`, `reviews/`, `plans/`, and `reports/` to enable intra-task handoff between items, ensuring all five directories are created successfully. Use the Bash tool to run `mkdir -p` for each subdirectory. If the parent directory does not exist, create it first. Once done, mark this item as complete.

**Step 1.3:** Capture pre-implementation git state for restriction audit

- [x] Use the Bash tool to run `git status --short` and `git log -1 --oneline` and capture both outputs to the file `pre-implementation-git-state.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/pre-implementation-git-state.md` formatted as a markdown document with two fenced code blocks (one for `git status --short`, one for `git log -1 --oneline`), so that Phase 6 (Restrictions Audit) has a baseline to diff against when verifying restriction #3 (≤30% per-patch diff on `structural_checkers.py`), restriction #4 (zero changes to `convergence.py`), restriction #5 (no spec edits), restriction #6 (no changes to `max_runs=3` at `convergence.py:440`), and restriction #1 (no edits outside `structural_checkers.py` and `tests/roadmap/`). Ensure the file accurately captures the pre-implementation state at task start with no fabricated content. If unable to complete due to git command failure or file write issues, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.4:** Read structural_checkers.py to ground subsequent changes in current line numbers

- [x] Read the file `structural_checkers.py` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/structural_checkers.py` end-to-end to establish the current actual line numbers for the `SEVERITY_RULES` table (research cites lines 42-67), `FIX_GUIDANCE_TEMPLATES` (research cites lines 155-176), the `_make_finding` helper (research cites around line 260), and the `phantom_id` block in `check_signatures` (research cites lines 372-391, with the comparator at line 380), then write a brief inventory to the file `structural-checkers-line-map.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/structural-checkers-line-map.md` containing the current actual line numbers (which may have drifted from research citations) for each of: `SEVERITY_RULES` start/end, `FIX_GUIDANCE_TEMPLATES` start/end, `_make_finding` location, the `check_signatures` function start, and the `phantom_id` block start/end. This grounds Phase 2 changes in current state rather than possibly-stale research citations. Ensure all line numbers are extracted directly from the file with no fabrication. If unable to read the file or locate the expected sections, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 1.5:** Read integration_contracts.py precedent to ground Change 1's mirror pattern

- [x] Read the file `integration_contracts.py` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/integration_contracts.py` focusing on the `_canonicalize_identifiers` function at or near line 445 (the project-level precedent for collapsing semantically-identical IDs per `KNOWLEDGE.md` 2026-05-25 "Fix B Merged"), then write a brief excerpt to the file `precedent-pattern.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/precedent-pattern.md` containing: the actual current line range of `_canonicalize_identifiers`, the function signature, the docstring (if any), and a 5-10 line excerpt of the function body that demonstrates the canonicalization style. This serves as the visual reference for restriction #7 ("Pattern mirrors `integration_contracts.py:445`") verified in Phase 6. Ensure all content is extracted directly from the source file with no fabrication. If unable to locate the function, log the specific blocker using the templated format in the ### Phase 1 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 2: Production Code Change 1 — Add `_canonicalize_requirement_id` helper

This phase adds the pure-function helper that Change 2 will consume. Helper-before-consumer ordering is mandatory: the helper must exist before the `phantom_id` block calls it.

**Step 2.1:** Add the `_canonicalize_requirement_id` helper to structural_checkers.py

- [x] Read the discovery file `structural-checkers-line-map.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/structural-checkers-line-map.md` to identify the current line number of the `_make_finding` helper (research cites around line 260), then read the merged fix specification at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/03-refactor-plan-concrete-changes.md` section "Change 1" to obtain the verbatim function definition (signature + docstring + body), then read the existing file `/config/workspace/IronClaude/src/superclaude/cli/roadmap/structural_checkers.py` to confirm exact insertion context, then use the Edit tool to add the `_canonicalize_requirement_id(family: str, raw: str) -> str` function definition immediately after the `_make_finding` helper. The function MUST be: (1) a pure `(str, str) -> str` transformation with no shared state, no I/O; (2) strip leading zeros within the numeric tail; (3) preserve the family prefix and any sub-ID structure (e.g., `D01` → `D1`; `D-01` → `D1`; `FR-7.1` → `FR-7.1` idempotent; `NFR-02` → `NFR-2`; `FR-07.1` → `FR-7.1`); (4) include the full docstring from `research/03-refactor-plan-concrete-changes.md` Change 1 verbatim, which references both the `integration_contracts.py:445` precedent and the forward-looking fix-2 fixability framing; (5) mirror the canonicalization style established in `integration_contracts.py:445` (as documented in `phase-outputs/discovery/precedent-pattern.md`). Implementation approach: use a regex like `re.sub(r"^(?P<prefix>[A-Z]+)-?0*(?P<num>\d+)(?P<rest>.*)$", ...)` or equivalent that strips leading zeros from the numeric tail while preserving prefix + sub-ID, ensuring idempotence on already-canonical IDs. Ensure the function is placed near `_make_finding` (not at module top, not at file end), the docstring contains all examples and forward-looking notes verbatim from the refactor plan, no behavior is fabricated beyond what the spec describes, and the addition is ~15 LOC. If unable to complete due to file access issues or unclear placement, log the specific blocker using the templated format in the ### Phase 2 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 3: Production Code Change 2 — Modify the `phantom_id` block + add SEVERITY_RULES + FIX_GUIDANCE_TEMPLATES entries

This phase modifies the comparator in `check_signatures` to use canonical sets, and adds the supporting severity rule + fix-guidance template entries. Each sub-change is its own item per A3 granularity.

**Step 3.1:** Add `("signatures", "id_schema_drift"): "MEDIUM"` entry to SEVERITY_RULES

- [x] Read the discovery file `structural-checkers-line-map.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/structural-checkers-line-map.md` to identify the current line range of `SEVERITY_RULES` in `structural_checkers.py` (research cites lines 42-67), then read the merged fix specification at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` section "Change 2" and the refactor plan at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/03-refactor-plan-concrete-changes.md` section "Change 2 — Also required" to confirm the exact key-value to add, then read the existing file `/config/workspace/IronClaude/src/superclaude/cli/roadmap/structural_checkers.py` SEVERITY_RULES table to confirm the surrounding format and style of existing entries, then use the Edit tool to add the new entry `("signatures", "id_schema_drift"): "MEDIUM"` to the `SEVERITY_RULES` table at a position consistent with the existing alphabetical/grouped ordering (most natural placement: adjacent to the existing `("signatures", "phantom_id"): "HIGH"` entry, if present). Ensure the entry uses the same tuple-key + string-value format as surrounding entries, no other SEVERITY_RULES entries are modified, and the addition is exactly 1 line. If unable to complete due to file access issues or unclear placement, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.2:** Add `id_schema_drift` entry to FIX_GUIDANCE_TEMPLATES

- [x] Read the discovery file `structural-checkers-line-map.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/structural-checkers-line-map.md` to identify the current line range of `FIX_GUIDANCE_TEMPLATES` in `structural_checkers.py` (research cites lines 155-176), then read the merged fix specification at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` section "Change 2" to obtain the verbatim template string (`"Spec uses '{spec_quote}' form; roadmap uses '{roadmap_quote}' form. Either normalize roadmap IDs to the spec form OR rely on the canonicalized comparator — this finding does not block convergence."`), then read the existing file `/config/workspace/IronClaude/src/superclaude/cli/roadmap/structural_checkers.py` FIX_GUIDANCE_TEMPLATES dict to confirm the surrounding format and existing entry style (note: existing entries are likely keyed by `mismatch_type` or `(dimension, mismatch_type)` — match the existing convention), then use the Edit tool to add a new `id_schema_drift` entry to `FIX_GUIDANCE_TEMPLATES` containing the verbatim template string above. The entry's key MUST match the structural convention used by sibling entries in the dict. Ensure no other FIX_GUIDANCE_TEMPLATES entries are modified, the template string is byte-for-byte identical to the merged fix spec including the placeholders `{spec_quote}` and `{roadmap_quote}`, and the addition is 1-3 lines depending on dict formatting style. If unable to complete due to file access issues or unclear key convention, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 3.3:** Replace the `phantom_id` block in `check_signatures` with the canonicalized comparator

- [x] Read the discovery file `structural-checkers-line-map.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/structural-checkers-line-map.md` to identify the current line range of the `phantom_id` block in `check_signatures` (research cites lines 372-391, comparator at line 380), then read the refactor plan at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/03-refactor-plan-concrete-changes.md` section "Change 2 — Integration approach" to obtain the verbatim replacement code (the canonical-set comparator that builds `spec_canon` and `roadmap_canon` dicts, then iterates `roadmap_canon` partitioning into `drift_findings` (MEDIUM `id_schema_drift`) and `phantom_findings` (HIGH `phantom_id`)), then read the existing file `/config/workspace/IronClaude/src/superclaude/cli/roadmap/structural_checkers.py` around the cited line range to confirm the existing code shape (raw set difference: `phantom_ids = roadmap_ids - spec_ids` or similar), then use the Edit tool to REPLACE the existing raw-set-difference block with the canonical-set-difference + classification block from the refactor plan. The replacement MUST: (1) call `_canonicalize_requirement_id(family, raw)` for each raw ID on both spec and roadmap sides, building `{canonical: raw}` mapping dicts; (2) iterate the roadmap canonical map and partition into three buckets: exact match (skip — no finding), canonical match but surface differs (emit MEDIUM `id_schema_drift` via `_make_finding` with `mismatch_type="id_schema_drift"`, `dimension="signatures"`, `spec_quote=spec_canon[canon]`, `roadmap_quote=raw`, plus the description text from the refactor plan), canonical not in spec (emit HIGH `phantom_id` via `_make_finding` — current behavior preserved); (3) extend `findings` with both `phantom_findings` and `drift_findings`; (4) preserve any existing surrounding behavior unrelated to the phantom_id comparator (e.g., other signature checks before/after this block). Ensure the replacement code is byte-equivalent to the refactor plan's Integration approach snippet (modulo minor adjustments to fit the actual surrounding code style), the addition is ~20 LOC net (~10 LOC modified + ~10 LOC added), no other checkers in the file are modified, and the per-patch diff for `structural_checkers.py` remains under 30% of file LOC. If unable to complete due to file access issues, ambiguous current code shape, or unclear integration with surrounding code, log the specific blocker using the templated format in the ### Phase 3 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 4: Test Change 3 — Add 5 golden-fixture asymmetric-ID unit tests

This phase adds 5 sibling tests to `tests/roadmap/test_structural_checkers.py`. Each test is its own checklist item per A3 granularity. All 5 tests live in the existing test file alongside `test_detects_phantom_id` (or analogous existing fixture).

**Step 4.1:** Discover existing test file conventions for test_structural_checkers.py

- [x] Read the existing test file `test_structural_checkers.py` at `/config/workspace/IronClaude/tests/roadmap/test_structural_checkers.py` end-to-end to identify (a) the fixture-construction pattern used by existing phantom_id tests (likely `test_detects_phantom_id` per research citation `test_structural_checkers.py:152, 258`), (b) the imports already in place (in particular how `SpecData`, `RoadmapData`, `check_signatures` or analogous helpers are imported), (c) the assertion style used to inspect Finding severity and rule_id, and (d) whether the file uses pytest fixtures, dataclass constructors, or factory helpers, then write a brief conventions summary to the file `test-structural-checkers-conventions.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/test-structural-checkers-conventions.md` containing: list of relevant imports, name + signature of any fixture or factory used to construct SpecData/RoadmapData, an example assertion pattern (1-3 lines), the line number of the closest existing phantom_id-related test. This grounds the 5 new test items (Steps 4.2-4.6) in actual file conventions rather than fabricated style. Ensure all content is extracted directly from the test file with no fabrication. If unable to locate the file or its phantom_id tests, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.2:** Add test_phantom_id_canonicalizes_zero_padded_d_ids

- [x] Read the discovery file `test-structural-checkers-conventions.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/test-structural-checkers-conventions.md` to identify the SpecData/RoadmapData construction pattern + assertion style used in existing tests, then read the merged fix spec at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` section "Change 3" to obtain the expected fixture inputs and outputs for `test_phantom_id_canonicalizes_zero_padded_d_ids` (spec={D1,D3,D5} roadmap={D01,D03,D05} → 0 HIGH, 3 MEDIUM `id_schema_drift`), then use the Edit tool to append the new test function `test_phantom_id_canonicalizes_zero_padded_d_ids` to `/config/workspace/IronClaude/tests/roadmap/test_structural_checkers.py` as a sibling to the existing `test_detects_phantom_id` test (per refactor plan Change 3). The test MUST: (1) construct a SpecData fixture with D-family requirement IDs `{D1, D3, D5}`; (2) construct a RoadmapData fixture with D-family requirement IDs `{D01, D03, D05}`; (3) invoke `check_signatures` (or the equivalent checker entrypoint used by existing tests); (4) assert that the resulting Finding list contains zero HIGH-severity `phantom_id` findings AND exactly three MEDIUM-severity `id_schema_drift` findings; (5) match the import / fixture / assertion style from the conventions file. Ensure the test follows the existing file's style conventions, no other tests are modified, the test name is exactly `test_phantom_id_canonicalizes_zero_padded_d_ids`, and the test fails BEFORE Phase 2-3 production changes land (regression-lock behavior) and passes AFTER. If unable to complete due to file access issues or unclear fixture API, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.3:** Add test_phantom_id_genuine_phantom_still_emits_high

- [x] Read the discovery file `test-structural-checkers-conventions.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/test-structural-checkers-conventions.md` to confirm fixture and assertion style, then read the merged fix spec at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` section "Change 3" to obtain the expected fixture inputs and outputs for `test_phantom_id_genuine_phantom_still_emits_high` (spec={D1,D3} roadmap={D01,D99} → 1 HIGH (D99) + 1 MEDIUM (D01↔D1)), then use the Edit tool to append the new test function `test_phantom_id_genuine_phantom_still_emits_high` to `/config/workspace/IronClaude/tests/roadmap/test_structural_checkers.py`. The test MUST: (1) construct a SpecData fixture with D-family IDs `{D1, D3}`; (2) construct a RoadmapData fixture with D-family IDs `{D01, D99}`; (3) invoke the checker entrypoint; (4) assert exactly 1 HIGH-severity `phantom_id` finding whose `roadmap_quote` is `D99` AND exactly 1 MEDIUM-severity `id_schema_drift` finding whose `roadmap_quote` is `D01` and `spec_quote` is `D1`. Ensure the test regression-locks genuine-phantom detection (i.e., the fix does NOT eliminate the legitimate phantom_id signal when an ID has no canonical match in spec), follows existing test style, and the test name is exactly `test_phantom_id_genuine_phantom_still_emits_high`. If unable to complete due to file access issues or unclear fixture API, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.4:** Add test_phantom_id_canonicalizes_fr_subids

- [x] Read the discovery file `test-structural-checkers-conventions.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/test-structural-checkers-conventions.md` to confirm fixture and assertion style, then read the merged fix spec at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` section "Change 3" to obtain the expected fixture inputs and outputs for `test_phantom_id_canonicalizes_fr_subids` (FR-7.1 idempotent + FR-07.1↔FR-7.1 drift), then use the Edit tool to append the new test function `test_phantom_id_canonicalizes_fr_subids` to `/config/workspace/IronClaude/tests/roadmap/test_structural_checkers.py`. The test MUST: (1) construct a SpecData fixture with FR-family IDs `{FR-7.1, FR-8}`; (2) construct a RoadmapData fixture with FR-family IDs `{FR-7.1, FR-07.1}` (one exact match + one zero-pad drift on the sub-ID-prefixed form); (3) invoke the checker entrypoint; (4) assert zero HIGH `phantom_id` findings AND exactly 1 MEDIUM `id_schema_drift` finding for `FR-07.1↔FR-7.1`. The test verifies sub-ID preservation through the canonicalization (i.e., `FR-7.1` stays `FR-7.1` and is idempotent; only the leading-zero prefix is stripped). Ensure the test name is exactly `test_phantom_id_canonicalizes_fr_subids` and follows the existing file style. If unable to complete due to file access issues or unclear fixture API, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.5:** Add test_phantom_id_canonicalizes_nfr_padding

- [x] Read the discovery file `test-structural-checkers-conventions.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/test-structural-checkers-conventions.md` to confirm fixture and assertion style, then read the merged fix spec at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` section "Change 3" to obtain the expected fixture inputs and outputs for `test_phantom_id_canonicalizes_nfr_padding` (NFR-02↔NFR-2 drift), then use the Edit tool to append the new test function `test_phantom_id_canonicalizes_nfr_padding` to `/config/workspace/IronClaude/tests/roadmap/test_structural_checkers.py`. The test MUST: (1) construct a SpecData fixture with NFR-family IDs `{NFR-2, NFR-4}`; (2) construct a RoadmapData fixture with NFR-family IDs `{NFR-02, NFR-04}`; (3) invoke the checker entrypoint; (4) assert zero HIGH `phantom_id` findings AND exactly 2 MEDIUM `id_schema_drift` findings. The test verifies that the NFR family (in addition to FR and D, already covered by other golden-fixture tests) participates in canonicalization. Ensure the test name is exactly `test_phantom_id_canonicalizes_nfr_padding` and follows the existing file style. If unable to complete due to file access issues or unclear fixture API, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 4.6:** Add test_phantom_id_idempotent_on_unpadded

- [x] Read the discovery file `test-structural-checkers-conventions.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/test-structural-checkers-conventions.md` to confirm fixture and assertion style, then read the merged fix spec at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` section "Change 3" to obtain the expected fixture inputs and outputs for `test_phantom_id_idempotent_on_unpadded` (D1,D3,D5 everywhere → 0 findings), then use the Edit tool to append the new test function `test_phantom_id_idempotent_on_unpadded` to `/config/workspace/IronClaude/tests/roadmap/test_structural_checkers.py`. The test MUST: (1) construct a SpecData fixture with D-family IDs `{D1, D3, D5}`; (2) construct a RoadmapData fixture with the IDENTICAL D-family IDs `{D1, D3, D5}`; (3) invoke the checker entrypoint; (4) assert zero `phantom_id` findings of any severity AND zero `id_schema_drift` findings (i.e., the canonical comparator is idempotent — when both sides are already canonical, no drift is emitted). This test is also a sanity check that the canonicalization helper itself is idempotent. Ensure the test name is exactly `test_phantom_id_idempotent_on_unpadded` and follows the existing file style. Note: The fifth family coverage commitment (SC and G families) is satisfied jointly by the property-based test in Phase 5 + the fact that the FR/NFR/D-family tests already exercise the family-prefix branch of the canonicalization regex; explicit SC/G golden-fixtures are not required because the per-family logic is identical (no family-specific branching beyond the prefix string). If unable to complete due to file access issues or unclear fixture API, log the specific blocker using the templated format in the ### Phase 4 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 5: Test Change 4 — Property-based + flatline-halt + cross-cutting integration tests

This phase adds 3 distinct tests across 2 NEW or existing test files. Each test is its own checklist item per A3 granularity.

**Step 5.1:** Add property-based test in a NEW test file

- [x] Read the merged fix spec at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` section "Change 4" to obtain the description of `test_canonicalization_property_holds_across_families` (NEW file, `importorskip("hypothesis")` guarded; `@given(id_form_pairs())` strategy generates `(canonical, surface_variants)` pairs across all 5 families; asserts 0 HIGH `phantom_id` whenever canonical form matches on both sides), then read the existing precedent file at `/config/workspace/IronClaude/tests/sprint/test_property_based.py` to learn the `pytest.importorskip("hypothesis")` posture and the `@given` strategy declaration style used in this repo (the refactor plan explicitly cites this as the precedent), then read the discovery file `test-structural-checkers-conventions.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/test-structural-checkers-conventions.md` to identify the SpecData/RoadmapData fixture-construction pattern, then create a NEW test file at `/config/workspace/IronClaude/tests/roadmap/test_structural_checkers_properties.py` (~40 LOC) containing: (1) a module-level `pytest.importorskip("hypothesis")` guard so the test is skipped cleanly when hypothesis is not installed; (2) a `from hypothesis import given, strategies as st` import and any other necessary imports; (3) a strategy function `id_form_pairs()` (using `@st.composite` or a `st.builds(...)`-style construction) that yields `(canonical, surface_variants)` pairs across all 5 families FR, NFR, SC, G, D — for each family, generate a canonical id like `D5` and a list of surface variants like `[D5, D05, D-05, D-5]`; (4) a `@given(id_form_pairs())`-decorated test function `test_canonicalization_property_holds_across_families` that, for each `(canonical, surface_variants)` pair, constructs a SpecData with `{canonical}` and a RoadmapData with `surface_variants`, invokes `check_signatures`, and asserts zero HIGH `phantom_id` findings (drift findings ARE acceptable — the property under test is "canonical match → no HIGH"). Ensure the file uses `importorskip` at module level (not function level — module-level skip is the precedent at `tests/sprint/test_property_based.py`), the strategy explicitly covers all 5 families FR/NFR/SC/G/D, the test only asserts on HIGH-severity phantom_id count, the file path is exactly `/config/workspace/IronClaude/tests/roadmap/test_structural_checkers_properties.py`, and no other test files are created or modified. If unable to complete due to missing hypothesis precedent or unclear strategy API, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.2:** Add flatline-halt regression test in test_convergence.py

- [x] Read the merged fix spec at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` section "Change 4" to obtain the description of `test_flatline_halt_emits_structural_verdict` (driver returns 58 findings on n=1, 54 on n=2, 54 on n=3 — TUIBBS shape; post-fix: same fixture passes on Run 1 with 0 active HIGH and 54 MEDIUM `id_schema_drift`), then read the existing test file `/config/workspace/IronClaude/tests/roadmap/test_convergence.py` end-to-end to identify the existing `test_convergence_loop_three_runs` test (research cites at line 911) and the convergence-loop fixture / driver harness used by sibling tests, then use the Edit tool to append the new test function `test_flatline_halt_emits_structural_verdict` to `/config/workspace/IronClaude/tests/roadmap/test_convergence.py` as a sibling to `test_convergence_loop_three_runs`. The test MUST: (1) construct a SpecData fixture with D-family IDs `{D1, D3, D5}` (or a similarly minimal canonical-form spec); (2) construct a RoadmapData fixture with 54 zero-padded D-family IDs `{D01, D02, …, D54}` (the TUIBBS shape); (3) invoke the convergence loop (or the specific entrypoint used by `test_convergence_loop_three_runs`); (4) assert that the loop passes on Run 1 (not flatlines for 3 runs), with `active_high_count == 0` AND ≥54 MEDIUM-severity `id_schema_drift` findings emitted. The test regression-locks the convergence behavior: post-fix, the TUIBBS shape no longer halts. Ensure the test name is exactly `test_flatline_halt_emits_structural_verdict`, follows the existing test_convergence.py style, references the same driver / fixture used by `test_convergence_loop_three_runs`, and the addition is ~30 LOC. If unable to complete due to file access issues, unclear driver API, or inability to construct the 54-ID fixture, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 5.3:** Add cross-cutting integration test in test_remediate_executor.py

- [x] Read the merged fix spec at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/research/02-merged-fix-spec.md` section "Change 4" to obtain the description of `test_loop_reports_structural_when_all_remediations_exceed_diff_guard` (registry where every active finding's only candidate patch exceeds the 30% guard; asserts terminal verdict identifies the structural ceiling, not budget exhaustion), then read the existing test file `/config/workspace/IronClaude/tests/roadmap/test_remediate_executor.py` end-to-end to identify the existing `test_large_change_rejected` test (research cites at line 708) and the registry / 30%-diff-guard fixture used by sibling tests, then use the Edit tool to append the new test function `test_loop_reports_structural_when_all_remediations_exceed_diff_guard` to `/config/workspace/IronClaude/tests/roadmap/test_remediate_executor.py` as a sibling to `test_large_change_rejected`. The test MUST: (1) construct a registry / fixture where every active finding has at least one candidate patch BUT every candidate patch exceeds the 30% diff guard at `remediate_executor.py:309-362`; (2) invoke the remediate executor loop; (3) assert that the terminal verdict identifies a STRUCTURAL ceiling (e.g., halt-reason text contains a marker like "structural", "diff guard", or "all candidates rejected" — match the exact halt-reason format produced by the executor for this case) rather than budget exhaustion or convergence-not-reached. The test verifies that when no remediation can land within the additive-edit constraint, the verdict surfaces that fact clearly (vs. silently flatlining). Ensure the test name is exactly `test_loop_reports_structural_when_all_remediations_exceed_diff_guard`, follows the existing test_remediate_executor.py style, references the same registry / executor API used by `test_large_change_rejected`, and the addition is ~25 LOC. If unable to complete due to file access issues, unclear executor API, or inability to construct an all-fixes-unfixable registry, log the specific blocker using the templated format in the ### Phase 5 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 6: Validation — lint, format, tests

This phase runs the validation gates specified in the BUILD_REQUEST `VALIDATION_REQUIREMENTS` field. Lint and format MUST pass; the full `tests/roadmap/` suite MUST pass with no regressions and the new tests passing.

**Step 6.1:** Run `make lint` and capture results

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && make lint 2>&1` and capture the complete output, then write the raw output to the file `lint-output.txt` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/test-results/lint-output.txt` preserving the exact output with no modifications, then write a structured summary to `lint-summary.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/test-results/lint-summary.md` containing: overall result (PASSED/FAILED), the exit code, any lint errors or warnings (one row per issue with columns File, Line, Rule, Message), and the total count of issues. IF lint FAILS, read the raw output for the specific issues introduced by Phase 2-5 changes (focus on `structural_checkers.py` and the new test files), then use the Edit tool to fix each issue at its source location (the file the lint output points to — typically `structural_checkers.py` or one of the new test files; do NOT use `# noqa` to bypass), then re-run `make lint` until it passes; record each fix cycle in the summary. Ensure the lint output accurately reflects the post-Phase-5 state of the code, all issues are addressed at the source rather than suppressed, and `make lint` ultimately exits 0. If lint fails for reasons unrelated to this task's changes (e.g., pre-existing failures on files NOT touched by this task), log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 6.2:** Run `make format` and capture results

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && make format 2>&1` and capture the complete output, then write the raw output to the file `format-output.txt` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/test-results/format-output.txt` preserving the exact output with no modifications, then write a structured summary to `format-summary.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/test-results/format-summary.md` containing: overall result (PASSED/FAILED), the exit code, the list of files reformatted (if any). If `make format` reformatted any files touched by this task (Phase 2-5 changes), use the Bash tool to run `git diff <reformatted-file>` and confirm the reformatting is purely cosmetic (whitespace, line breaks) rather than semantic. Ensure `make format` exits 0 and any reformatting that occurred is purely cosmetic. If `make format` fails or produces semantic changes, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 6.3:** Run `uv run pytest tests/roadmap/ -v` and capture results

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && uv run pytest tests/roadmap/ -v 2>&1` and capture the complete output, then write the raw output to the file `pytest-output.txt` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/test-results/pytest-output.txt` preserving the exact output with no modifications, then write a structured summary to `pytest-summary.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/test-results/pytest-summary.md` containing: overall result (PASSED/FAILED), total tests run, tests passed, tests failed, tests skipped, a table of any failed tests with columns Test Name + Error Type + Brief Message, a separate section listing the new tests added in Phase 4-5 (`test_phantom_id_canonicalizes_zero_padded_d_ids`, `test_phantom_id_genuine_phantom_still_emits_high`, `test_phantom_id_canonicalizes_fr_subids`, `test_phantom_id_canonicalizes_nfr_padding`, `test_phantom_id_idempotent_on_unpadded`, `test_canonicalization_property_holds_across_families`, `test_flatline_halt_emits_structural_verdict`, `test_loop_reports_structural_when_all_remediations_exceed_diff_guard`) and confirming each is PRESENT in the output and PASSED, and the relevant pytest summary line. The exit code MUST be 0; all 8 new tests MUST pass; no previously-passing test MAY regress. IF any test fails, read `pytest-output.txt` to identify the specific failure cause, then use the Edit tool to fix the source of the failure (either in the test fixture if the fixture is wrong, or in the Phase 2-3 production code if the production code is wrong), then re-run pytest until it passes; record each fix cycle in the summary. Ensure the pytest output accurately reflects the post-Phase-5 state, all 8 new tests pass, no regressions are introduced. If tests fail in a way that cannot be resolved within ~3 fix cycles, log the specific blocker using the templated format in the ### Phase 6 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

### Phase 7: Restrictions Audit — verify all 7 restrictions hold

This phase verifies that every binding restriction in `research/05-restrictions-doc-context.md` holds post-implementation. Each restriction is its own checklist item per A3 granularity. This satisfies the BUILD_REQUEST `QA_GATE_REQUIREMENTS: FINAL_ONLY` requirement.

**Step 7.1:** Restriction #1 — Module ownership (no edits outside structural_checkers.py and tests/roadmap/)

- [x] Read the pre-implementation git state at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/pre-implementation-git-state.md` to confirm the baseline, then use the Bash tool to run `cd /config/workspace/IronClaude && git status --short` and `git diff --stat` and capture both outputs, then verify that every modified, added, or deleted file falls within EXACTLY one of these two paths: (a) `src/superclaude/cli/roadmap/structural_checkers.py` (the only production-code file touched per restriction #1), or (b) any file under `tests/roadmap/` (test additions are exempt from the module-ownership constraint). Write the verification result to `restriction-1-module-ownership.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reviews/restriction-1-module-ownership.md` containing: verdict (PASS/FAIL), the full list of changed files from `git diff --stat`, and a per-file determination of whether each file falls within the allowed scope. IF any file outside the allowed scope is modified, the audit FAILS — use the Bash tool to inspect the unexpected change, determine whether it was intentional (and thus a violation) or accidental (e.g., a formatter side-effect that needs reverting), and either revert the change or escalate as a restriction violation. Ensure the audit is based on actual git output with no fabrication. If unable to complete the audit due to git command failure, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.2:** Restriction #2 — Pure-function contract on `_canonicalize_requirement_id`

- [x] Read the implementation of `_canonicalize_requirement_id` at `/config/workspace/IronClaude/src/superclaude/cli/roadmap/structural_checkers.py` (the function added in Phase 2 Step 2.1), then write the verification result to `restriction-2-pure-function.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reviews/restriction-2-pure-function.md` containing: verdict (PASS/FAIL), the function signature, and a checklist confirming each of these pure-function criteria: (a) signature is exactly `(family: str, raw: str) -> str` (yes/no); (b) function body contains no I/O calls (no `open()`, no `print()`, no `sys.stdout`, no `requests`, no `Path.read_*` etc.) (yes/no); (c) function body modifies no module-level state (no global assignment, no class-attribute mutation) (yes/no); (d) function body has no closures over mutable state from the enclosing scope (yes/no); (e) function is deterministic — for identical `(family, raw)` inputs, returns identical output (yes/no, confirmed by inspection); (f) function is idempotent — `f(family, f(family, raw)) == f(family, raw)` (yes/no, confirmed by inspection and by `test_phantom_id_idempotent_on_unpadded`). Ensure all answers are derived from actual code inspection with no fabrication. If any criterion fails, the audit FAILS — log the specific failure mode and fix via Edit, then re-audit. If unable to complete due to file access issues, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.3:** Restriction #3 — ≤30% per-patch diff on structural_checkers.py

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && git diff --numstat src/superclaude/cli/roadmap/structural_checkers.py` to obtain the additions and deletions count for the file, then run `wc -l src/superclaude/cli/roadmap/structural_checkers.py` to obtain the current total LOC, then compute the per-patch diff percentage as `((additions + deletions) / total_LOC) * 100`. Write the result to `restriction-3-diff-guard.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reviews/restriction-3-diff-guard.md` containing: verdict (PASS if <30%, FAIL if ≥30%), the raw `git diff --numstat` output, the file LOC count, and the computed percentage. The merged fix spec estimates ~20 LOC added + ~10 LOC modified in a 700+ LOC file ≈ ~4-6%, well under 30%. IF the percentage is ≥30%, the audit FAILS — review the Phase 2-3 changes for unintended expansion (e.g., duplicated code, unnecessary refactoring of unrelated code paths) and tighten the diff to fit under the guard. Ensure the computation is based on actual git output with no fabrication. If unable to complete due to git command failure, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.4:** Restriction #4 — Binary pass predicate at convergence.py:539 untouched

- [x] Use the Bash tool to run `cd /config/workspace/IronClaude && git diff src/superclaude/cli/roadmap/convergence.py` to check whether the convergence.py file was modified, then verify the output is empty (zero diff). Write the result to `restriction-4-convergence-untouched.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reviews/restriction-4-convergence-untouched.md` containing: verdict (PASS if zero diff, FAIL otherwise), the raw `git diff` output (which should be empty), and an additional confirmation step: use the Read tool to read `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py` at line 539 and confirm the binary pass predicate text (e.g., `if active_high_count == 0:` or equivalent) is identical to what existed at task start. The binary pass predicate is the linchpin that the fix relies upon — its preservation is restriction #4. IF the diff is non-empty, the audit FAILS — inspect the unexpected change and revert. Ensure the verification is based on actual git output and file Read with no fabrication. If unable to complete due to git command failure, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.5:** Restriction #5 — Spec at TUIBBS-scp v1-MVP/epics.md immutable

- [x] Use the Bash tool to run `ls /config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/epics.md` to confirm the spec path exists (this is in a SIBLING repository, NOT in the IronClaude repo, so it should be untouched by any IronClaude change), then run `cd /config/workspace/TUIBBS-scp 2>/dev/null && git status --short -- .dev/releases/current/v1-MVP/epics.md 2>/dev/null || echo "[outside-repo or not-applicable]"` to confirm no modifications to the spec from this IronClaude task. Note: this restriction is structural — the IronClaude task does not have read/write access to the TUIBBS-scp repository in this context; the audit verifies via `git status` in the IronClaude repo that no IronClaude file modifies or proxies the spec. Write the result to `restriction-5-spec-immutable.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reviews/restriction-5-spec-immutable.md` containing: verdict (PASS if no IronClaude file references or modifies the spec path, FAIL otherwise), the output of the `ls` and `git status` commands, and an inspection of the Phase 2-3 changed files confirming none of them touch the spec or any TUIBBS-scp path. Ensure the verification is based on actual filesystem state and git output with no fabrication. If unable to complete due to filesystem or git command failure, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.6:** Restriction #6 — `max_runs=3` at convergence.py:440 untouched

- [x] This restriction is jointly satisfied by Restriction #4 (whole-file convergence.py untouched) — if `git diff src/superclaude/cli/roadmap/convergence.py` is empty per Step 7.4, then `max_runs=3` at line 440 is by construction untouched. Read the result from `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reviews/restriction-4-convergence-untouched.md` to confirm Restriction #4 passed, then use the Read tool to read `/config/workspace/IronClaude/src/superclaude/cli/roadmap/convergence.py` at line 440 and verify the literal value `max_runs=3` (or equivalent default-argument declaration with value 3) is present. Write the result to `restriction-6-max-runs.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reviews/restriction-6-max-runs.md` containing: verdict (PASS if Restriction #4 passed AND line 440 contains `max_runs=3` or equivalent, FAIL otherwise), the line excerpt from convergence.py:440, and a reference back to the Restriction #4 verdict. Ensure the verification is based on actual file Read with no fabrication. If Restriction #4 failed or line 440 does not contain the expected value, the audit FAILS. If unable to complete due to file access issues, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.7:** Restriction #7 — Pattern mirrors integration_contracts.py:445

- [x] Read the precedent pattern file `precedent-pattern.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/discovery/precedent-pattern.md` to obtain the precedent excerpt from `integration_contracts.py:445`, then use the Read tool to read the newly-added `_canonicalize_requirement_id` function in `/config/workspace/IronClaude/src/superclaude/cli/roadmap/structural_checkers.py`, then write a side-by-side comparison to `restriction-7-pattern-mirror.md` at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reviews/restriction-7-pattern-mirror.md` containing: verdict (PASS/FAIL), the precedent function signature and a short excerpt, the new function signature and a short excerpt, and a visual comparison confirming the same shape: (a) both are module-level pure helpers (yes/no); (b) both strip-or-normalize an identifier-like input (yes/no); (c) both return a string (yes/no); (d) both have docstrings that document the canonicalization style (yes/no); (e) the new helper's docstring explicitly references `integration_contracts.py:445` as the precedent (yes/no — required by the merged fix spec Change 1 docstring). The restriction is satisfied when the visual comparison confirms shape parity (not byte-equivalence — the helpers operate on different ID types). IF any criterion fails, the audit FAILS — log the specific mismatch and consider whether a docstring or signature update is needed. Ensure the comparison is based on actual file content with no fabrication. If unable to complete due to file access issues, log the specific blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

**Step 7.8:** Aggregate restriction audit verdicts

- [x] Use Glob to find all restriction review files matching `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reviews/restriction-*.md` to discover all 7 restriction audit files (one per Step 7.1-7.7), then read each file to extract the verdict (PASS/FAIL) and any noted issues, then create a consolidated audit report at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reports/restrictions-audit-report.md` containing: an executive summary with overall pass/fail count (e.g., "7/7 PASS" or "6/7 PASS, 1 FAIL on Restriction #N"), a table of all 7 restrictions with columns Restriction Number, Description, Verdict, Issues (if any), an overall audit verdict (ALL PASS — proceed to Post-Completion / ANY FAIL — block task completion until resolved), and if any restriction failed, a recommended remediation plan. The overall audit verdict MUST be ALL PASS before this task can transition to Phase 8 (Post-Completion). IF any restriction failed, do NOT proceed to Phase 8 — instead, log the failure in `### Phase 7 Findings` and address the failure cause before retrying. Ensure the report accurately aggregates data from all 7 review files with no fabricated verdicts, all 7 restriction files are present, and the report's pass count matches the per-file verdicts. If fewer than 7 review files are found, log this as a blocker using the templated format in the ### Phase 7 Findings section of the ## Task Log / Notes at the bottom of this task file, then mark this item complete. Once done, mark this item as complete.

## Post-Completion Actions

- [x] Verify all task outputs by using Glob to confirm every output file specified in checklist items exists on disk, ensuring no expected deliverables are missing. The expected deliverables include: (production) the `_canonicalize_requirement_id` function added to `structural_checkers.py`, the modified `phantom_id` block in `check_signatures`, the new `SEVERITY_RULES` entry, the new `FIX_GUIDANCE_TEMPLATES` entry; (tests) 5 new test functions appended to `tests/roadmap/test_structural_checkers.py`, the NEW file `tests/roadmap/test_structural_checkers_properties.py`, the new test function appended to `tests/roadmap/test_convergence.py`, the new test function appended to `tests/roadmap/test_remediate_executor.py`; (phase-outputs) the discovery files (line-map, precedent-pattern, test-conventions, git-state), the test-results files (lint, format, pytest), the reviews files (7 restriction audits), and the reports file (restrictions-audit-report). Use the Bash tool to run `grep -n "_canonicalize_requirement_id\|id_schema_drift" src/superclaude/cli/roadmap/structural_checkers.py | head -20` and `ls -la tests/roadmap/test_structural_checkers_properties.py` to spot-check the key production and test additions. If any expected deliverable is missing, check the Task Log for blockers explaining the absence. If files are missing without documented reason, log the gap in ### Follow-Up Items Identified below, then mark this item complete. Once done, mark this item as complete.

- [x] Confirm the testing items in Phase 6 (Step 6.3) ran and passed by reading `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/test-results/pytest-summary.md` and verifying the overall result is PASSED with all 8 new tests present and passing. Since the test suite was run in Step 6.3 and no subsequent source code changes have been made (Phase 7 is read-only audit), note "Tests verified in Phase 6.3 — pytest exited 0, all 8 new tests PASSED, no regressions" in the ### Execution Log of the ## Task Log / Notes section at the bottom of this task file, then mark this item complete. IF the Step 6.3 pytest summary shows FAILED status or missing new tests, do NOT mark this item complete — return to Phase 6 to resolve the failure before transitioning to Done. Once done, mark this item as complete.

- [x] Create a ### Task Summary section at the top of the ## Task Log / Notes section at the bottom of this task file, using the templated format provided there. The summary should document: work completed (referencing the 4 Changes — helper added, phantom_id block modified + severity rule + fix-guidance template, 5 golden-fixture tests added, property-based + flatline-halt + cross-cutting integration tests added), challenges encountered during execution (e.g., line-number drift between research citations and current code state, fixture-construction style differences between test files), any deviations from the planned process and their rationale (e.g., test names or assertion patterns adjusted to match existing file conventions), blockers logged during execution with their resolution status, and the final overall outcome (whether the TUIBBS v1-MVP failure shape is now fixed as expected: 54 HIGHs → 0 HIGHs + 54 MEDIUMs on Run 1). Reference the restrictions-audit-report at `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reports/restrictions-audit-report.md` for the final 7/7 PASS verdict. Once the summary is complete, mark this item as complete.

- [x] Update `completion_date` and `updated_date` to today's date and update task status to "🟢 Done" in frontmatter, then add an entry to the ### Execution Log in the ## Task Log / Notes section at the bottom of this task file using the format: `**[YYYY-MM-DD HH:MM]** - Task completed: Updated status to "🟢 Done" and completion_date.` Once done, mark this item as complete.

## Task Log / Notes 📋

### Task Summary
<!-- Fill this section in Post-Completion Actions -->

**Completion Date:** 2026-05-27

**Work Completed:**

- Change 1 (helper): Added `_canonicalize_requirement_id(family, raw) -> str` to `src/superclaude/cli/roadmap/structural_checkers.py` near `_make_finding`.
- Change 2 (comparator + tables): Replaced the raw set-difference `phantom_id` block in `check_signatures` with the canonicalized-set comparator that emits MEDIUM `id_schema_drift` for surface-form drift and preserves HIGH `phantom_id` for genuine missing IDs. Added `("signatures", "id_schema_drift"): "MEDIUM"` to `SEVERITY_RULES` and the templated `id_schema_drift` entry to `FIX_GUIDANCE_TEMPLATES`.
- Change 3 (golden-fixture tests): Added 5 unit tests to `tests/roadmap/test_structural_checkers.py`.
- Change 4 (property-based + integration tests): Added NEW file `tests/roadmap/test_structural_checkers_properties.py`; added `test_flatline_halt_emits_structural_verdict` to `tests/roadmap/test_convergence.py`; added `test_loop_reports_structural_when_all_remediations_exceed_diff_guard` to `tests/roadmap/test_remediate_executor.py`.
- Restrictions Audit: 7/7 PASS per `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/reports/restrictions-audit-report.md`.

**Files Created:**

- `tests/roadmap/test_structural_checkers_properties.py`
- All phase-outputs/ artifacts under `.dev/tasks/to-do/TASK-RF-20260527055700-spec-fidelity-canonicalizer/phase-outputs/`

**Files Modified:**

- `src/superclaude/cli/roadmap/structural_checkers.py`
- `tests/roadmap/test_structural_checkers.py`
- `tests/roadmap/test_convergence.py`
- `tests/roadmap/test_remediate_executor.py`

**Handoff files created:**

- discovery/: pre-implementation-git-state.md, structural-checkers-line-map.md, precedent-pattern.md, test-structural-checkers-conventions.md
- test-results/: lint-output.txt, lint-summary.md, format-output.txt, format-summary.md, pytest-output.txt, pytest-summary.md
- reviews/: restriction-1-module-ownership.md, restriction-2-pure-function.md, restriction-3-diff-guard.md, restriction-4-convergence-untouched.md, restriction-5-spec-immutable.md, restriction-6-max-runs.md, restriction-7-pattern-mirror.md
- reports/: restrictions-audit-report.md

**Challenges Encountered:**

- **Line-number drift between research citations and current state:** research/01-troubleshoot-report.md cited `structural_checkers.py:42-67` for SEVERITY_RULES; actual current range was 31-56 (-11 lines). Addressed by the Phase 1 line-map discovery file (`phase-outputs/discovery/structural-checkers-line-map.md`) — Phases 2-3 used current line numbers, not stale research citations.
- **`make format` reformatted 128 pre-existing files outside scope:** ruff format applied repo-wide and touched many pre-existing-drift files. Addressed by reverting all 132 (128 + 4 in `tests/roadmap/` not intentionally modified) via `git checkout HEAD -- <files>`, then running `ruff check --fix` only on the new property test file. Final `make lint` passes; format restricted to in-scope files (5 already formatted).
- **TUIBBS-shape fixture in `test_flatline_halt_emits_structural_verdict`:** the merged-fix-spec's "spec={D1,D3,D5} vs roadmap={D01..D54} → 0 HIGH + 54 MEDIUM" only holds if the spec enumerates D1..D54 canonically (the literal {D1,D3,D5} would leave 51 genuine phantoms). Addressed by writing the test fixture with `spec=D1..D54, roadmap=D01..D54`, which exercises the post-fix mechanism end-to-end and asserts exact drift counts (9: D01..D09 ↔ D1..D9; D10..D54 byte-identical → no findings).
- **3 pre-existing tests in `TestSeverityRules` needed updating:** `test_exactly_19_rules`, `test_11_medium_rules`, `test_all_canonical_rules_present` encoded the rule count (19) and rule set. The new `("signatures", "id_schema_drift"): "MEDIUM"` (Step 3.1) required these tests to be updated to 20 / 12 and include the new rule. Renamed and updated.

**Deviations from Process:**

- **`make format` not invoked as a final whole-repo command:** Step 6.2 says "ensure `make format` exits 0". Whole-repo `make format` would have touched 126 out-of-scope files (pre-existing drift), violating Restriction #1. Resolution: applied `ruff format` only to the 5 in-scope files (all "already formatted"), reverted inadvertent reformats, and logged the resolution in `phase-outputs/test-results/format-summary.md`. Step 6.2's intent (in-scope files clean) is satisfied; whole-repo cleanup is deferred as separate tech debt.

**Blockers Logged:**

- **Step 6.2 — repo-wide format check fails due to pre-existing drift outside scope:** Documented in `phase-outputs/test-results/format-summary.md`. Resolution: in-scope subset confirmed clean; out-of-scope drift untouched per Restriction #1. **Status:** Resolved (in-scope clean; out-of-scope drift acknowledged as pre-existing tech debt).

**Follow-Up Required:** Yes
- Pre-existing repo-wide format drift (126 files would-be-reformatted by `ruff format`) is unrelated to this task but will block any future `make format` invocation. Recommend a separate cleanup PR.
- The 6 carried-in upstream follow-up items (INV-001, INV-002, A-001, deferred fix-2 fixability scaffolding, deferred fix-4 ADVISORY tier, LLM attention drift) remain open — see Follow-Up Items Identified.

**Overall Outcome:**

The TUIBBS v1-MVP failure shape is structurally fixed. After this task lands:
- Roadmap zero-padded ID variants no longer flag as HIGH `phantom_id`; they emit MEDIUM `id_schema_drift`, which the convergence-loop pass predicate (`active_high_count == 0` at `convergence.py:539`) correctly ignores.
- The convergence loop can PASS on Run 1 when the spec enumerates the canonical forms of the roadmap's surface-different IDs (confirmed by `test_flatline_halt_emits_structural_verdict`).
- Genuine `phantom_id` HIGH findings are preserved for IDs whose canonical form is NOT in spec (confirmed by `test_phantom_id_genuine_phantom_still_emits_high`).
- All 7 binding restrictions hold (7/7 PASS — see `phase-outputs/reports/restrictions-audit-report.md`).
- All 1715 tests in `tests/roadmap/` pass; 7 of 8 new tests run + pass, 1 cleanly skips when `hypothesis` is unavailable (intended posture per Step 5.1).

### Execution Log

<!-- TEMPLATE FOR EXECUTION LOG ENTRIES:
**[YYYY-MM-DD HH:MM]** - [Action taken]: [Brief description of what was done and outcome]
-->

**[2026-05-27 06:25]** - Task started: Updated status to "🟠 Doing" and start_date.

**[2026-05-27 06:30]** - Phase 1 complete: setup, line-map and precedent-pattern discovery files written.
**[2026-05-27 06:34]** - Phase 2 complete: `_canonicalize_requirement_id` helper added at `structural_checkers.py:295` (rf-qa phase-2 PASS).
**[2026-05-27 06:37]** - Phase 3 complete: SEVERITY_RULES + FIX_GUIDANCE_TEMPLATES entries added; `phantom_id` block replaced with canonicalized set-difference comparator (rf-qa phase-3 PASS).
**[2026-05-27 06:43]** - Phase 4 complete: 5 golden-fixture tests added inside `TestSignaturesChecker`; pytest smoke (10/10 pass) confirms behavior.
**[2026-05-27 06:50]** - Phase 5 complete: NEW property-test file, flatline-halt regression, cross-cutting integration test added; each test smoke-passes individually.
**[2026-05-27 06:55]** - Phase 6 complete: lint PASS (0 issues); format on in-scope files clean; pytest tests/roadmap/ exits 0 with 1715 passed, 12 skipped (3 pre-existing TestSeverityRules tests updated to reflect the new rule).
**[2026-05-27 06:55]** - Phase 7 complete: 7/7 restrictions PASS; restrictions-audit-report.md aggregates all per-restriction verdicts.
**[2026-05-27 06:57]** - Tests verified in Phase 6.3 — pytest exited 0, all 8 new tests PRESENT (7 PASSED, 1 SKIPPED via importorskip), no regressions.
**[2026-05-27 06:57]** - Task completed: Updated status to "🟢 Done" and completion_date.

### Phase 1 - Preparation and Setup Findings

<!-- TEMPLATE FOR BLOCKER ENTRIES:
**[YYYY-MM-DD HH:MM]** - Step 1.Y BLOCKED:
- **Blocker Reason:** [Specific reason]
- **Attempted:** [What was tried before determining blocker]
- **Required to Unblock:** [What information or action is needed to proceed]
-->

### Phase 2 - Helper Addition Findings

### Phase 3 - Comparator + Severity + Template Findings

### Phase 4 - Golden-Fixture Test Findings

### Phase 5 - Property-Based + Integration Test Findings

### Phase 6 - Validation Findings

### Phase 7 - Restrictions Audit Findings

### Follow-Up Items Identified

<!-- TEMPLATE FOR FOLLOW-UP ITEMS:
- **[Priority: High/Medium/Low]** [Description of follow-up needed] - Identified in Step [X.Y]
-->

Known follow-ups carried in from the upstream pipeline (do NOT execute as part of this task — surface as separate work after this task lands):

- **[Priority: Medium]** INV-002: collision warning when both `D1` and `D-01` exist in same spec (no proposal currently emits a warning). - Identified upstream by Wave 2.5 fault-finder.
- **[Priority: Medium]** INV-001: test guard for new requirement families (e.g., `TC-NNN`); ensures `_REQUIREMENT_PATTERNS` upgrade path is covered. - Identified upstream by Wave 2.5 fault-finder.
- **[Priority: Low]** A-001: spec-side normalization product decision (alternative to canonicalization: edit the spec to use zero-pad form — requires product/team alignment). - Identified upstream by diff-analysis.
- **[Priority: Low]** Deferred fix-2 fixability scaffolding (`_classify_fixability` + FIXABILITY_GUIDANCE_TEMPLATES) — blocked on INV-003 (CLASS_DRIFT count threshold undefined). Revisit when a 2nd drift class surfaces. - Identified upstream by Wave 4 adversarial debate.
- **[Priority: Low]** Deferred fix-4 ADVISORY severity tier + `--allow-advisory-drift` / `--strict-no-advisory` CLI lane. Defer until 2+ drift classes justify the new tier. - Identified upstream by Wave 4 adversarial debate.
- **[Priority: Medium]** LLM attention drift (Pattern 1 of `historical-context.md` Section 5) — semantic-fluctuation failures remain possible. A complementary 5-vote-consensus or DISPUTED reclassification automation is a separate concern. - Identified upstream by Phase 0 archaeology.

### Deviations from Process

<!-- TEMPLATE FOR DEVIATIONS:
**[YYYY-MM-DD HH:MM]** - Deviation from [Step X.Y]:
- **Expected:** [What the process specified]
- **Actual:** [What was done instead]
- **Rationale:** [Why this deviation was necessary]
-->
