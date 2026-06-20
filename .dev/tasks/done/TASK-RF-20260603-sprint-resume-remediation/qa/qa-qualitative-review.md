# QA Report — Task File Qualitative Review

**Topic:** TASK-RF-20260603-sprint-resume-remediation
**Date:** 2026-06-03
**Phase:** task-qualitative
**Fix cycle:** N/A (initial review; fix_authorization=true, fixes applied in-place)

---

## Overall Verdict: PASS (after 3 in-place fixes)

All three defects found were fixed in-place in the task file. The plan, as amended, would now succeed if executed. No unfixable issues remain.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | Baseline `uv run pytest tests/sprint/test_resume.py -q` ⇒ 17 passed (verified). `pyproject.toml:107-111` has no `-m` deselect ⇒ `tests/sprint/` e2e (integration) runs by default — Step 5.1 claim accurate. `make lint`/`make verify-sync` preconditions valid (resume subsystem is pure-Python, not synced). |
| 2 | Project convention compliance | none | PASS | All code edits target `src/superclaude/` (no `.claude/` writes); verify-sync correctly expected clean. Tests use pytest, not inline `python -c`. UV-only commands throughout. |
| 3 | Intra-phase execution order | none | PASS | RED test → fix → GREEN ordering holds per phase; §2/§4(b)/field-add ordered before integrity/printer (3.2→3.3→3.4→3.5); BoundaryTask.phase (4.2) before planner (4.3) before integrity (4.4). |
| 4 | Function signature verification | AX-3 | FAIL→FIXED | drift.py:177-187 fall-through + executor.py:2069-2078 writer + commands.py:520-536 printer + integrity.py:63-67/86-130 + planner.py:120-169 + models all verified against real source. **F-3 signature/data gap found:** the WS-hash gate reads a recorded field the test fixture never writes (see Issue 1). Fixed. |
| 5 | Module context analysis | none | PASS | Read full drift.py, integrity.py, planner.py, models.py. `_annotate_git` confirmed never sets confidence (NFR-3 holds). `_verdict` confirmed pure (partial_paths never a term in passed). |
| 6 | Downstream consumer analysis | AX-3 | FAIL→FIXED | F-2 path: `_detect_partial`→`run()`→`BoundaryReport.partial_paths`→printer chain traced; all consumers covered. **F-4: the negative-companion STOP consumer (artifacts check) was not phase-resolved** (see Issue 2). Fixed. |
| 7 | Test validity | none | PASS | CG-1/CG-2/CG-3 reuse real module builders with realistic input (real transcripts, real deliverable blocks, real result.json). No stubs. RED states are true assertion failures, not collection errors. |
| 8 | Test coverage of primary use case | none | PASS | Each finding has its RED→GREEN coverage-gap test; CG-3 adds a negative companion proving non-vacuity. AC-4/AC-5/quarantine/no-writes non-regression checks present. |
| 9 | Error path coverage | none | PASS | Backward-compat fallbacks specified (missing WS hash ⇒ conservative <0.8; missing phase field ⇒ interrupted-phase behavior; prior=None ⇒ emit nothing). |
| 10 | Runtime failure path trace | AX-3 | FAIL→FIXED | Traced input→drift→gate→print and planner→integrity. Two break points found and fixed (Issues 1, 2). Third (planner threading) clarified (Issue 3). |
| 11 | Completion scope honesty | none | PASS | CG-4 is genuinely surfaced as human-decision with blank RULING line; F-1 held conditional (no unconditional gate change); Open Questions resolved or conditionally handled, not ignored. |
| 12 | Ambient dependency completeness | none | PASS | Imports (`Path`/`field`), spec amendments (§2/§4(a)/§4(b)/§5, FR-2.4), printer wiring, design notes all sequenced. |
| 13 | Kwarg sequencing red flags | AX-3 | FAIL→FIXED | F-4 BoundaryTask.phase (4.2) added before planner passes it (4.3) — order correct. **F-3 had a deferred-action gap:** the WS field is written by the writer but the test fixture that the non-regression gate reads was not updated (Issue 1). Fixed. |
| 14 | Function existence claims | none | PASS | Grep-verified: `_write_phase_result_json` (executor.py:2053), `_content_sha256_excluding_rerun_block` (rerun_tasks.py:688), `parse_tasklist_file` (config.py:501), drift fall-through (drift.py:178-187), integrity `if partial_paths:` (integrity.py:64-67), printer quarantined loop (commands.py:533-534), planner else-branch (planner.py:158-166). All claims accurate. |
| 15 | Cross-reference accuracy for templates | none | PASS | All design.md anchors verified against real source: §2 BoundaryReport (line 86), §4(a) (147-154), §4(b) "always" (173), §4(c) (186), §7 passed=True (293); merged-req FR-2.4 (85-87), AC-3 "phase 2 tail" (141-143). All accurate. |

## Summary
- Checks passed: 15/15 (after in-place fixes; 3 were FAIL→FIXED)
- Checks failed (unfixed): 0
- Critical issues: 1 (fixed)
- Important issues: 1 (fixed)
- Minor issues: 1 (fixed)
- Issues fixed in-place: 3
- Axis lens status: all five axes applied; AX-1 Drift baseline = REPORT remediation §103-117 (F-3/F-2/F-4/CG-4) — captured and active. No drift, no contradictions, no invented content, no weakened criteria detected. The three findings were all AX-3 (omissions).

## Confidence
**Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

Every check was verified by reading the actual target source files (not research summaries alone) and, for items 1/14, by executing the real test suite and inspecting pyproject.toml.

## Tool engagement
**Read: 9 | Grep(Bash grep): 5 | Glob: 0 | Bash(pytest/sed): 4**
(Read targets: task file ×2 pages, drift.py, integrity.py, models.py, planner.py, commands.py slice, executor.py slice, config.py slice, rerun_tasks.py slice, test_resume.py, research 01/03/04. Tool calls exceed 15 checklist items — no padding; each call mapped to a specific verification.)

## Issues Found
| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|--------------|--------|
| 1 | CRITICAL | Step 2.2/2.3 vs `tests/sprint/test_resume.py:205-208` | F-3 principled fix returns `<0.8` when recorded `tasklist_sha256_ws` is MISSING. The AC-4 test (`test_drift_trailing_whitespace_high_conf`) builds its result.json via `_build_task_interrupted`, which persists ONLY `tasklist_sha256`, NEVER `tasklist_sha256_ws`. So AC-4 hits the "WS-missing ⇒ <0.8" branch and FAILS its `confidence >= 0.8` assertion — the task's own Step 2.5/PG.2 non-regression gate would fail. The task claimed "AC-4 preserved" without the fixture co-edit that makes it true. | Add a mandatory co-edit to Step 2.2: update `_build_task_interrupted` so `record_hash=True` also writes `rj["tasklist_sha256_ws"]` of the recorded body via the same normalization helper. Cross-reference in Step 2.3 and Step 2.5. | FIXED in-place |
| 2 | IMPORTANT | Step 4.4 vs `integrity.py:120-124` | F-4 negative companion (`test_resume_hard_crash_prior_tail_overclaim_stops`) expects a STOP on a MISSING P2 deliverable. But the artifacts check `_declared_deliverables(phase_file, lc.task_id)` reads `_boundary_phase_file(plan)` = the INTERRUPTED phase (P3) tasklist, not the prior phase (P2). P3 declares no deliverable for `T02.01` ⇒ `_declared_deliverables` returns `[]` ⇒ `all([])` vacuously True ⇒ `artifacts_ok` stays True ⇒ negative companion can never reach `validated_last is False` (stays RED). Step 4.4 mentioned "artifact lookups resolve under that task's phase" but glossed that `_declared_deliverables` needs the prior phase's *tasklist file*, re-resolved via `discover_phases`. | Strengthen Step 4.4 to explicitly require resolving the prior phase's tasklist file (`discover_phases(plan.index_path)` filtered to `lc.phase`) for the deliverable check, with the consequence (RED-stuck negative companion) spelled out. | FIXED in-place |
| 3 | MINOR | Step 4.3 vs `planner.py:120` | Step 4.3 instructs deriving prior `Phase.file` "from the in-scope `phases` list," but `_build_boundary(self, plan, results_dir)` does NOT receive `phases` (it is local to `plan()`). The threading requirement was listed only as a possible blocker, not a determinate sub-step. Research 03 §2.1 flagged this. | Convert to an explicit required sub-step: thread `phases` into `_build_boundary` OR emit the prior-tail in `plan()` after `_build_boundary` returns; pick one explicitly. | FIXED in-place |

## Actions Taken
- Fixed Issue 1 in Step 2.2 (renamed step to include the helper co-edit; added a CRITICAL co-edit paragraph mandating `_build_task_interrupted` persist `tasklist_sha256_ws`). Cross-referenced in Step 2.3 (added dependency note) and Step 2.5 (added explicit AC-4-helper validation note). Verified the fix preserves RED-then-GREEN: at Step 2.1 the helper still writes only the old field ⇒ CG-2 RED holds; at Step 2.5 the helper writes WS hash ⇒ AC-4 (matching WS) GREEN, CG-2 (differing WS) GREEN.
- Fixed Issue 2 in Step 4.4 (added a CRITICAL clause requiring the deliverable/artifact lookup to resolve the prior phase's tasklist file, with the vacuous-True failure mode spelled out so the negative companion can actually STOP).
- Fixed Issue 3 in Step 4.3 (added an explicit NOTE that `_build_boundary` does not receive `phases` and the executor must thread it or emit in `plan()`).
- Verification method for each fix: re-read the amended task text against the confirmed source semantics (drift.py Tier-0-miss→Tier-1 fall-through; `_build_task_interrupted` lines 205-208; `integrity._validate_last_completed` artifacts block 120-124; `_build_boundary` signature 120). No new contradictions introduced.

## Self-Audit / Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

This phase received an Inherited Structural Verdict (rf-qa A.10) with all items PASS. Reliance on those PASS items (structural re-check skipped) and the independent semantic check I ran for each:

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on rf-qa PASS for #5 (Evidence-based file paths) — skipped re-counting that paths exist.
- Relied on rf-qa PASS for #8 (Phase dependency ordering) — skipped re-deriving the DAG.
- Relied on rf-qa PASS for items A/B/C (F-3/F-4/F-2 structural shape) — skipped verifying the items are *present and structured*.
- Relied on rf-qa PASS for D (PER_PHASE QA gates) and E (RED-then-GREEN present) — skipped confirming the gate/test items exist.
- Relied on rf-qa PASS for TB-1..TB-8 (placeholder scan, granularity, DAG, context binding).

**(b) Independent semantic checks (≥1 required, INV-019) — where rf-qa PASS was INSUFFICIENT and my own tool work was required:**
- rf-qa PASS item A ("F-3 PRINCIPLED fix … NFR-3 preserved") is structurally present, but only by reading the *actual* drift.py fall-through (lines 178-187) AND the *actual* test fixture `_build_task_interrupted` (lines 205-208) did I find the WS-field-not-persisted-in-fixture gap that makes the principled fix regress AC-4 (Issue 1, CRITICAL). Structural presence ≠ operational success. Tool evidence: `Read drift.py:178-187`, `Read test_resume.py:205-208`, `grep tasklist_sha256_ws tests/sprint/test_resume.py` (zero matches).
- rf-qa PASS item B ("F-4 multi-file co-dependency … _read_transcript keys on interrupted_phase confirmed") covers the *transcript* keying, but reading `integrity.py:120-124` showed the *artifacts/deliverable* check ALSO keys on the interrupted-phase file — an independent break point the structural verdict did not surface (Issue 2, IMPORTANT). Tool evidence: `Read integrity.py:86-130`.
- rf-qa PASS item E ("RED-then-GREEN per test") is structurally satisfied, but executing `uv run pytest tests/sprint/test_resume.py -q` (17 passed) and tracing the Tier-0-miss→Tier-1 path by hand was required to confirm the CG-2 RED state is a true assertion failure (0.9 today) and not a collection error. Tool evidence: Bash pytest run + `Read drift.py:46-60,178-187`.

## Recommendations
- Proceed to execution. The three fixes are sufficient to make the plan operationally correct.
- During execution, watch Step 5.1: the `tests/sprint/e2e_real/` real-subprocess tests run by default and may be slow or require the `claude` CLI; the task already instructs distinguishing pre-existing failures from regressions, which is the correct handling.
- No further QA cycle required for these findings (all fixed in-place, ≤3 fix cycles not reached).

## QA Complete
