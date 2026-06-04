# Independent Reviewer Card — v4.3.5 Sprint Auto-Resume

## Scope

Read-only adversarial review of `TASK-RF-20260602-sprint-auto-resume` against:

- Driving requirements: `.dev/brainstorms/20260602-sprint-auto-resume-default/merged-requirements.md`
- Driving design: `.dev/brainstorms/20260602-sprint-auto-resume-default/design.md`
- Task log: `.dev/tasks/to-do/TASK-RF-20260602-sprint-auto-resume/TASK-RF-20260602-sprint-auto-resume.md`
- Implemented code/tests named in the prompt.

Taxonomy precedence applied: Regression > Drift > Necessary > Authorized.

## Deviation register

### D-001 — Boundary partial work no longer hard-gates resume

- **Evidence:** `src/superclaude/cli/sprint/resume/integrity.py:57-67` detects partial paths, then only calls `_surface_partial()` unless cleanup is opted in; `src/superclaude/cli/sprint/resume/integrity.py:69-75` sets `report.passed` after explicitly saying boundary partial work does not flip the verdict; `src/superclaude/cli/sprint/resume/integrity.py:306-314` returns `accept_suspect or report.validated_last`.
- **Spec measured against:** `merged-requirements.md:80-87` requires half-written artifacts to be surfaced for cleanup/assessment and says resume MUST NOT proceed until boundary half-finished work is cleaned or explicitly assessed-and-accepted; `design.md:184-187` says `passed = validated_last and (no unresolved suspects) and (partial work quarantined or accepted)`.
- **Task-log classification challenged:** `TASK-RF-20260602-sprint-auto-resume.md:358` documents the P4 refinement as aligned to design §7 and says the plan/CLI prompt is the acceptance point.
- **Classification:** **Regression**.
- **Rationale:** Design §7 does show `passed=True` while reporting half-written outputs (`design.md:292-296`), so the implementer had a real contradictory design cue. But the higher-specificity FR-2.4 hard gate and design §4(c) both require a cleaned or accepted boundary before proceeding. The code also permits `--yes`/CI to skip the interactive prompt entirely (`commands.py:436-470`), so the actual proceed path can be neither cleaned nor operator-assessed. “The plan re-runs it” is not equivalent to “explicitly assessed-and-accepted” unless the operator sees the artifacts and assents to that artifact set.

### D-002 — Partial-work artifact paths are detected but not carried in `BoundaryReport` or printed

- **Evidence:** `_detect_partial()` returns `list[Path]` and adds transcript/deliverable/stray files to `found` (`src/superclaude/cli/sprint/resume/integrity.py:134-173`), but `_surface_partial()` only appends a `BoundaryTask` (`src/superclaude/cli/sprint/resume/integrity.py:197-208`). `BoundaryReport` has `suspects`, `quarantined`, `blocking_reasons`, and `coherence_warnings`, but no report-only field for partial paths (`src/superclaude/cli/sprint/resume/models.py:84-101`). `_print_resume_decision()` prints suspect task IDs and only prints paths if quarantine ran (`src/superclaude/cli/sprint/commands.py:520-536`).
- **Spec measured against:** `merged-requirements.md:80-82` requires surfacing artifacts for cleanup or assessment before re-execution; `design.md:172-180` says “report suspect paths in BoundaryReport (always)” and maps quarantine copies separately.
- **Task mapping:** Task item 3.2 promised “ALWAYS report suspect paths in the `BoundaryReport`” (`TASK-RF-20260602-sprint-auto-resume.md:190-195`).
- **Classification:** **Regression**.
- **Rationale:** The implementation detects the right paths internally, but loses them on the report-only path. This makes FR-2.2’s “assessment” weak and directly compounds D-001: an operator cannot explicitly accept artifacts that are not displayed.

### D-003 — Drift Tier 1 ignores completed-task body/checkpoint/deliverable edits when task IDs are unchanged

- **Evidence:** `DriftAssessor._tier1()` computes only `current_ids`, `recorded_completed`, and `recorded_all` (`src/superclaude/cli/sprint/resume/drift.py:88-99`), then treats identical task-ID sets as cosmetic with confidence 0.9 (`src/superclaude/cli/sprint/resume/drift.py:177-187`). The only material completed-work branch is removed/renamed completed task IDs (`src/superclaude/cli/sprint/resume/drift.py:142-155`). The unit test for AC-5 narrows “material edit” to removal/rename (`tests/sprint/test_resume.py:261-274`).
- **Spec measured against:** `merged-requirements.md:93-104` requires comparing phase/task identifiers, checkpoint declarations, and deliverable paths and explaining score; `merged-requirements.md:146-147` says materially editing a completed phase’s task makes confidence <0.8; `design.md:212-218` says structural diff composes task IDs plus checkpoint paths and deliverables, and checkpoint/deliverable changes score ~0.3.
- **Task-log classification:** `TASK-RF-20260602-sprint-auto-resume.md:351` records Tier 1 as “structural ID-diff,” which honestly describes the implementation but silently drops the checkpoint/deliverable part of DD-4/AC-5.
- **Classification:** **Regression**.
- **Rationale:** A completed task’s prose, artifact path, or checkpoint declaration can materially change while keeping the same `### Txx.yy` ID. The current code will score that as cosmetic/high-confidence, allowing silent resume where AC-5 requires refusal.

### D-004 — AC-3 hard-crash path does not double-validate the previous phase tail

- **Evidence:** In the no-result/no-transcript hard-crash case, planner derives no failed tasks and sets PHASE granularity with an empty boundary (`src/superclaude/cli/sprint/resume/planner.py:158-169`). The gate then treats absence of a last-completed task as vacuously validated (`src/superclaude/cli/sprint/resume/integrity.py:97-101`). The unit test locks `plan.boundary_tasks == []` for the hard-crash path (`tests/sprint/test_resume.py:139-156`), and the e2e test only asserts whole-phase rerun after deleting result/transcripts (`tests/sprint/e2e_real/test_e2e_resume.py:113-147`).
- **Spec measured against:** `merged-requirements.md:141-143` requires that a hard crash mid-phase assesses/cleans half-finished phase artifacts and double-validates the last completed task, explicitly “phase 2 tail,” before rerunning phase 3. `merged-requirements.md:83-87` also requires whole-boundary assessment/cleanup first.
- **Classification:** **Regression**.
- **Rationale:** The implementation satisfies “whole boundary phase re-runs,” but not the AC-3 seam validation requirement for the prior completed phase. This is likely why the tests passed: they assert PHASE granularity and rerun breadth, not previous-tail validation.

### D-005 — Advisory surface uses `invoke_sonnet` rather than the design’s “Haiku” name

- **Evidence:** `_coherence_read()` imports and calls `invoke_sonnet` (`src/superclaude/cli/sprint/resume/integrity.py:358-376`). The task log records a pre-existing missing `invoke_haiku` import and says the real surface is `invoke_sonnet` (`TASK-RF-20260602-sprint-auto-resume.md:347`, `TASK-RF-20260602-sprint-auto-resume.md:354`).
- **Spec measured against:** `design.md:155-162` and `design.md:318-322` name the advisory coherence read as Haiku and require it never affect deterministic verdicts.
- **Classification:** **Necessary deviation**.
- **Rationale:** The model-class/name changed, but the load-bearing property is advisory-only isolation. The code computes the advisory read after `passed` is set (`src/superclaude/cli/sprint/resume/integrity.py:78-82`) and catches failures as no-op (`src/superclaude/cli/sprint/resume/integrity.py:351-356`). The task log documents the real constraint: `invoke_haiku` does not exist.

### D-006 — Missing last-completed transcript hard-STOPS validation

- **Evidence:** `_validate_last_completed()` reads the task transcript and classifies it independently (`src/superclaude/cli/sprint/resume/integrity.py:111-126`). `_classify_transcript()` returns `TaskStatus.INCOMPLETE` when no terminal result event is present (`src/superclaude/cli/sprint/rerun_tasks.py:549-597`), so an absent transcript read as `""` fails Signal B.
- **Spec measured against:** `merged-requirements.md:76-79` says a persisted PASS is a claim to be re-checked and not trusted; `merged-requirements.md:85-87` requires last completed task double-validation before resume.
- **Classification:** **No deviation**.
- **Rationale:** This can false-stop if transcripts were rotated or manually cleaned, but the requirements deliberately bias toward distrust. I do not reclassify this as regression; it is a conservative implementation of FR-2.1/FR-2.4. If operators need a transcript-retention exception, that would be a future spec change.

## Coverage gaps / unsatisfied requirements

1. **FR-2.2 / FR-2.4 path assessment gap:** No `BoundaryReport` field or CLI output carries report-only partial artifact paths (D-002), so assessment is not meaningfully possible before proceed. Existing test `test_boundary_quarantine_nondestructive` asserts only next-unfinished suspect presence and `passed is True` (`tests/sprint/test_resume.py:513-521`).
2. **AC-5 material-edit gap:** Existing drift tests cover removed/renamed completed task IDs only (`tests/sprint/test_resume.py:261-274`). There is no coverage for same-ID completed-task body edits, checkpoint edits, or deliverable path edits despite DD-4/FR-3 requiring those.
3. **AC-3 previous-tail validation gap:** Hard-crash tests prove PHASE rerun but not last-completed phase-tail double-validation (`tests/sprint/test_resume.py:139-156`; `tests/sprint/e2e_real/test_e2e_resume.py:113-147`).
4. **Spec/code self-contradiction is unresolved:** `design.md:184-187` and `merged-requirements.md:85-87` require partial cleanup/acceptance before resume; `design.md:292-296` shows a happy-path `passed=True` with half-written outputs merely reported. The implementation chose the latter and logged it (`TASK-RF-20260602-sprint-auto-resume.md:358`), but did not preserve the required artifact reporting, making the choice unsafe.

## Highest-confidence missed finding

**D-003 (AC-5 drift body/checkpoint/deliverable blind spot)** is the highest-confidence “9 gates missed” finding. It is mechanically clear from source: Tier 1 only compares task IDs and returns 0.9 for identical IDs, while the spec explicitly includes checkpoint/deliverable declarations as material drift. This is a silent high-confidence resume against a changed completed-task definition.

## Verdict

The feature is not clean. The planner and dispatch skeleton are broadly aligned, and the advisory-LLM isolation is acceptable, but the safety core has three regressions that matter: partial artifacts are not surfaced as paths, unresolved partial work no longer blocks unless one treats a generic prompt/`--yes` as acceptance, and drift scoring ignores material same-ID edits. A fourth regression leaves AC-3’s previous-phase-tail double validation unimplemented on the PHASE hard-crash path. I would not promote this as fully satisfying FR-2/FR-3/AC-3/AC-5 until these are corrected or explicitly amended in the requirements.

Counts: `{regressions: 4, drift: 0, necessary: 1, authorized: 0, coverage_gaps: 4}`
