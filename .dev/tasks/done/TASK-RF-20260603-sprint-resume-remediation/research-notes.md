# Research Notes: Corrective task for sprint auto-resume reflection findings F-3, F-2, F-4 + CG-4

**Date:** 2026-06-03
**Scenario:** A (Explicit — driven by a precise UC-2 reflection REPORT with file:line grounding)
**Depth Tier:** Standard (5 researchers)
**Track Count:** 1 (single track — all findings live in the `resume/` subsystem and share source context that must be understood holistically)

**Source driver:** `.dev/reflect/post-sprint-auto-resume-20260603003009/REPORT.md`
**Remediated work:** `.dev/tasks/to-do/TASK-RF-20260602-sprint-auto-resume/` (v4.3.5 sprint auto-resume; 31/31 items, 24 tests pass, but `partial` spec satisfaction)
**Driving spec (for CG-4 + F-2 design amendment):** `.dev/brainstorms/20260602-sprint-auto-resume-default/{design.md, merged-requirements.md}`

---

## EXISTING_FILES

Resume subsystem (`src/superclaude/cli/sprint/resume/`):

- `drift.py` (11,780 B) — `DriftAssessor.assess()`. Tier 0 (exact hash), Tier 1 (structural / task-ID diff), Tier 2 (additive git characterization, never changes confidence). **F-3 fix target.** Verified grounding:
  - `_current_task_ids(phase_file)` at L210; `assess` ID-diff logic L88-187.
  - Identical-ID set ⇒ `confidence=0.9, cosmetic_only=True` (L132, L179) — the F-3 bug surface.
  - Completed-task ID removed/renamed ⇒ `confidence=0.3, cosmetic_only=False` (L113, L145) — the only material-completed branch today.
  - Module docstring L4: "Only the 0.8 confidence boundary gates resume (AC-4/AC-5)."
- `integrity.py` (18,379 B) — boundary integrity verdict. **F-2 + F-4 + F-1 context.** Verified:
  - `_validate_last_completed` L86; vacuously True when no last-completed task (PHASE granularity) L94-101 — **F-4 grounding**.
  - `_detect_partial` L134 (returns partial-work paths); `_surface_partial` L198 (appends a `BoundaryTask` only) — **F-2 grounding**.
  - `passed` verdict `return accept_suspect or report.validated_last` (report cites L314) — **F-1 context**.
  - Advisory surface uses `invoke_sonnet` (L363,376) — F-5, no action.
- `models.py` (4,318 B) — `BoundaryTask` (L38), `BoundaryReport` (L85, `validated_last: bool` L94). **F-2 option A (add report-only partial-paths field) requires touching this + a design §2 field-exactness amendment.**
- `planner.py` (14,524 B) — `ResumePlanner`. **F-4 fix target.** PHASE hard-crash ⇒ `boundary_tasks == []` (report cites L158-169); no last-completed ⇒ integrity vacuously validated.
- `__init__.py` (1,079 B) — exports.

Command surface (`src/superclaude/cli/sprint/commands.py`):

- `_print_resume_decision(decision)` at L498 (called L293, L441). **F-2 option B (print `_detect_partial()` paths on the report-only path) lives here.**

Tests (`tests/sprint/`):

- `test_resume.py` (25,627 B, 17 tests). Verified anchors:
  - AC-3 hard-crash PHASE: `test_resume_hard_crash_phase_level` L139 (asserts rerun breadth, NOT prior-tail validation — **CG-3 gap**).
  - AC-4 cosmetic: `test_drift_trailing_whitespace_high_conf` L239.
  - AC-5 material: `test_drift_material_edit_low_conf` L261 (covers **ID removal only** — **CG-2 gap**: no same-ID body/checkpoint/deliverable edit test).
  - `test_boundary_quarantine_nondestructive` (report CG-1: asserts only `passed is True` + suspect presence; no report-only partial **paths** assertion).
- `tests/sprint/e2e_real/` — real-subprocess e2e (resume_drift_stop, resume_fresh, resume_multiphase, resume). Pattern reference for any e2e-level locking.

Design spec (`.dev/brainstorms/20260602-sprint-auto-resume-default/`):

- `design.md` (27,823 B) — §2 (field-exactness), §4(a) interrupted-phase validation, §4(b) L172-180 (report suspect paths in BoundaryReport always), §4(c) L186 (`passed` = validated_last AND no-suspects AND partial quarantined/accepted), §5 L212-218 (structural diff composes task IDs + `extract_checkpoint_paths` + deliverable-path diff), §7 L292-296 (happy path `passed=True` with half-written outputs reported). **CG-4 contradiction: §7 vs §4(c)/FR-2.4.**
- `merged-requirements.md` (13,261 B) — FR-2.1, FR-2.4 (HARD gate), L141-143 (hard crash mid-phase must double-validate the last completed task before re-running — **F-4 spec basis**), AC-3/AC-4/AC-5.

## PATTERNS_AND_CONVENTIONS

- UV only: `uv run pytest`, `uv run pytest tests/sprint/test_resume.py -v`. Never `python -m`.
- Source of truth is `src/superclaude/`. The resume subsystem is pure Python CLI (not a synced `.claude/` component), so edits stay in `src/` and need NO `make sync-dev`. `make verify-sync` only governs skills/agents/commands.
- Deterministic-core invariant (NFR-3): drift confidence is a pure function of deterministic signals; Tier 2 git is additive and NEVER changes confidence. Any F-3 fix MUST preserve this (the safe fix lowers confidence deterministically on a Tier-0 hash miss with unprovable-cosmetic same-ID content — it must not depend on git availability for the gate).
- Non-destructive default (NFR-1): planner performs no writes (`test_planner_performs_no_writes` L158). F-4 fix must not introduce writes in planning.
- Test conventions: pytest classes grouped by component with AC-tagged docstrings; `tmp_path` fixtures; deterministic assertions on `confidence`, `tier`, `cosmetic_only`, `explanation`. e2e_real uses real subprocess + fake_claude harness.
- Field-exactness (design §2, Phase-1 QA-verified): models were deliberately kept to exact spec fields. F-2 Option A (new BoundaryReport field) therefore REQUIRES a design §2 amendment first, or it re-introduces the exact drift Phase-1 QA guarded against. Option B (print paths, no model change) avoids the amendment.

## GAPS_AND_QUESTIONS

1. **F-3 data constraint:** Is there a per-task content/checkpoint baseline in `result.json` (or the resume index) that drift can diff against, or only task IDs + a phase-file content hash? The report says no per-task baseline exists — confirm exactly what signals are available so the fix is "don't assume same-ID ⇒ cosmetic after a Tier-0 hash miss" rather than an impossible per-task diff. Confirm whether `extract_checkpoint_paths` + deliverable-path diff can run from available data, and whether `git --ignore-all-space` is viable when the phase file is tracked.
2. **F-2 decision:** Option A (BoundaryReport field + design §2 amendment) vs Option B (print `_detect_partial()` paths in `_print_resume_decision()` only). Which does the task pick — and does the report-only path actually reach `_print_resume_decision`? Confirm the call sites (L293 vs L441) and which fires on report-only vs quarantine.
3. **F-4 reachability:** On a PHASE hard-crash with `boundary_tasks == []`, where does the "prior completed phase's tail" come from? Does the planner have access to the prior phase's last task, or must it derive it from the tasklist/index? Confirm the minimal data path to double-validate phase N-1's tail before re-running phase N.
4. **CG-4:** Exact quotations of design §7 (L292-296), §4(c) (L186), and FR-2.4 from the spec, so the decision item frames the contradiction precisely and records an authoritative ruling (does bare `sprint run --yes` proceeding past *reported* (not quarantined) partial work satisfy FR-2.4 "assessed-and-accepted"?).
5. **Scope boundary on F-1/F-5/F-6:** Report adjudicates F-1 as Necessary-deviation blocked on CG-4 (no direct code fix until CG-4 decided), F-5/F-6 as no-action. The task must NOT create code-fix items for F-1 beyond what CG-4's ruling authorizes, and must NOT touch F-5/F-6.

## RECOMMENDED_OUTPUTS

Corrective MDTM task file at
`.dev/tasks/to-do/TASK-RF-20260603-sprint-resume-remediation/TASK-RF-20260603-sprint-resume-remediation.md`
(Template 02). Phases (proposed):

- Phase 1 — CG-4 spec decision (resolve §7 vs §4(c)/FR-2.4; record ruling; amend spec; this gates F-1 and informs F-2 Option A).
- Phase 2 — F-3 fix (drift Tier-1 conservative on Tier-0 hash miss with unchanged IDs) + CG-2 test.
- Phase 3 — F-2 fix (surface partial-work paths to operator) + CG-1 test.
- Phase 4 — F-4 fix (PHASE hard-crash prior-phase-tail double-validation) + CG-3 test.
- Phase 5 — Full-suite verification (`uv run pytest tests/sprint/ -v`, lint) + task completion.

## SUGGESTED_PHASES (researcher assignments — 5 researchers, single track)

- **Researcher 1 — Drift / F-3 (File Inventory + Data Flow):** `drift.py` full — Tier 0/1/2 structure, `assess`, `_current_task_ids`, `extract_checkpoint_paths` (does it exist? where?), confidence branches (0.9/0.3/0.85/0.85/1.0), `cosmetic_only`. Trace what data `assess` receives (index, plan) and what per-task/checkpoint/deliverable signals are available vs only task IDs + phase-file hash. Identify the exact minimal code change for "Tier-0 hash miss + unchanged IDs ⇒ cannot prove cosmetic ⇒ <0.8". Output: `research/01-drift-f3.md`.
- **Researcher 2 — Integrity & Boundary models / F-2 + F-1 context (Integration Points):** `integrity.py` (`_detect_partial` L134-173, `_surface_partial` L198, `passed` verdict L314, `_validate_last_completed`) + `models.py` (`BoundaryReport`, `BoundaryTask`). Document exactly what `_detect_partial` returns, how `_surface_partial` drops the paths, the model field set, and both F-2 options (A: new field + §2 amendment; B: print only). Output: `research/02-integrity-boundary-f2.md`.
- **Researcher 3 — Planner & command surface / F-4 + F-2 print path (Data Flow Tracer):** `planner.py` PHASE hard-crash branch (L158-169, `boundary_tasks==[]`), how boundary/last-completed is built, where prior-phase tail could be derived; + `commands.py` `_print_resume_decision` (L498) and call sites (L293, L441) — which fires on report-only vs quarantine, and where partial paths would print. Output: `research/03-planner-commands-f4.md`.
- **Researcher 4 — Tests & Verification / CG-1, CG-2, CG-3 (Test & Verification):** `test_resume.py` (17 tests) + `e2e_real/`. Existing AC-3/AC-4/AC-5 test patterns, fixtures (`tmp_path`, index/plan builders), `test_boundary_quarantine_nondestructive`. Define exactly how to write: (CG-2) same-ID body/checkpoint/deliverable edit ⇒ <0.8; (CG-1) report-only partial paths surfaced; (CG-3) PHASE hard-crash prior-tail double-validation. Capture run commands + assertion style. Output: `research/04-tests-coverage-gaps.md`.
- **Researcher 5 — Spec & CG-4 decision (Doc Cross-Validator):** `design.md` §2/§4(a)/§4(b L172-180)/§4(c L186)/§5 L212-218/§7 L292-296 + `merged-requirements.md` FR-2.1/FR-2.4/L141-143/AC-3-5. Quote the contradicting passages verbatim, tag each [CODE-VERIFIED]/[CODE-CONTRADICTED] against actual implementation, and frame the exact decision CG-4 needs + the minimal design amendment surface for F-2 Option A and the F-4 spec basis. Output: `research/05-spec-cg4.md`.

## TEMPLATE_NOTES

- **Template 02 (Complex):** corrective work with a decision/spec phase + code fixes + new tests + verification. Discovery already largely done by the REPORT, but each fix needs a self-contained implement+test+verify item.
- **Tier Standard** — 5 researchers, bounded single subsystem (~6 source/test files + 2 spec docs), but elevated by a regression-class HIGH finding and a spec contradiction.
- QA_GATE_REQUIREMENTS: PER_PHASE (each fix phase ends with its own test green + the new coverage-gap test). VALIDATION: lint + `uv run pytest tests/sprint/ -v` full pass. TESTING: UNIT (CG-1/2/3) minimum; e2e optional if a fix changes the resume decision surface.
- Granularity: individual items per finding-fix and per new test. CG-4 gets its own decision+amendment items. Do NOT batch "fix F-2/F-3/F-4 together."
- Ordering: CG-4 decision FIRST (it gates F-1's classification and informs whether F-2 takes Option A). F-3 (HIGH regression) is the priority code fix.

## AMBIGUITIES_FOR_USER

- **CG-4 is a human-decision item by design** (REPORT: `needs_human_decision: true`). The task file must encode CG-4 as a DECISION item that surfaces the contradiction and the recommended ruling for operator sign-off — it must NOT silently pick a side and ship a gate change. This is intended, not a defect in the task.
- **F-1 has no standalone code-fix item** unless CG-4's ruling authorizes tightening the `--yes`/CI gate. The task should make F-1's remediation conditional on the CG-4 decision outcome (documented as such), not an unconditional code change.
- Otherwise intent is clear from the REPORT and the codebase.
