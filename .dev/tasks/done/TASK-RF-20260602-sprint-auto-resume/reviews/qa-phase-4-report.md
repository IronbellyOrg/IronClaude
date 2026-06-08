# QA Report — Phase-Gate (Phase 4: CLI wiring in run() + rerun_tasks())

**Topic:** Auto-Resume as Default for sprint run / rerun-tasks (v4.3.5) — Phase 4
**Date:** 2026-06-02
**Phase:** phase-gate
**Fix cycle:** N/A (initial gate, fix_authorization: true)

---

## Overall Verdict: PASS (after 2 in-place fixes)

Two real defects found in Phase 4 outputs and fixed in-place (1 CRITICAL, 1 MINOR).
Both fixes re-verified via executed evidence. No new failures introduced. The single
remaining `pytest` failure is the INTENTIONAL FR-4.1 contract change (test update
correctly deferred to Phase 5); the other 7 failures are PROVEN pre-existing via
`git stash`. All 7 acceptance criteria and the adversarial attack matrix pass.

---

## Confidence

**Verified:** 22/22 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%

**Tool engagement:** Read: 11 | Grep: 7 | Glob: 0 | Bash: 14 (CliRunner fixtures + real-call
dispatch probes + ruff + pytest + git-stash classification) | tavily_search: 0 | tavily_extract: 0 |
web_search_fallback: 0 | web_fetch_fallback: 0 (no external claims — all verification is source-truth
local). Tool-call count (32 Read/Grep/Bash) >> 22 checklist items: not suspect.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | AC-1 (4.1) both subcommands gain `--fresh`/`--restart` (alias same dest) + `--yes`/`-y`; run keeps `--dry-run`; existing flags intact | PASS | `sprint run --help` + `rerun-tasks --help` both exit 0; grep shows `--fresh`,`--restart`,`-y/--yes`,`--dry-run`,`--start`,`--end` (run) and `--fresh`,`--restart`,`-y/--yes`,`--phase`,`--tasks` (rerun). `--restart` shares dest `fresh` (commands.py:197-203,728-734) |
| 2 | AC-7 (4.2) `@click.pass_context` + ParameterSource.COMMANDLINE; `--start 1` AND `--start 4` bypass auto-resume; bare invokes once | PASS | ATTACK 1: monkeypatched `_auto_resume` call-counter. `--start 1`→0 calls (value-comparison trap AVOIDED), `--start 4`→0 calls, bare→1 call. `ctx` is first param of `run` (commands.py:214) |
| 3 | rerun_tasks explicit `--phase`/`--tasks`/`--from-reflect-report` via None-sentinel | PASS | commands.py:783 `explicit = phase is not None or tasks is not None or from_reflect_report is not None`; defaults all None (commands.py:658-674) |
| 4 | AC-6 (4.3) granularity NONE → "nothing to resume" exit 0 | PASS | ATTACK 3: all-complete fixture → exit 0, "Nothing to resume — all discovered phases are complete." |
| 5 | AC-8 (4.3) ambiguous → STOP non-zero | PASS | ATTACK 4: two-candidate release-dir fixture → exit 2, both candidates listed, "refusing to auto-pick" |
| 6 | (4.3) gate `not passed` → STOP | PASS | ATTACK 12: over-claim last-completed (missing artifact) → exit 2, "Resume blocked by the boundary integrity gate" |
| 7 | (4.3) drift `<0.8` → STOP with guidance | PASS | ATTACK 13: completed task T03.01 removed from boundary file → exit 2, "drift confidence 0.30 < 0.80" + material-edit explanation + `--start`/`--fresh` guidance |
| 8 | (4.3) else prompt unless --yes/env/CI/non-tty | PASS | `_auto_resume` (commands.py:436-471): assume_yes folds `SUPERCLAUDE_SPRINT_ASSUME_YES`/`CI`; non-tty without --yes → STOP exit 2 with re-run guidance; tty → `click.confirm` |
| 9 | AC-2 (4.4) TASK → `run_rerun_tasks(phase=interrupted, tasks=rerun_task_ids, merge_back=True)` | **PASS (FIXED)** | **CRITICAL defect found+fixed:** dispatch was missing 9 required kwargs (TypeError). After fix: real-call dispatch → SystemExit(0), kwargs `phase=3 tasks=['T03.02'] merge_back=True` |
| 10 | AC-2 merge_back=True passed | PASS | ATTACK 2 captured kwargs `merge_back=True`; fix passes it explicitly (commands.py:485) |
| 11 | (4.4) PHASE → set start/end window + fall through to executor (NG1) | PASS | ATTACK 6: hard-crash P2 (no result.json, no transcripts) → granularity PHASE → `run_rerun_tasks` 0 calls, `execute_sprint(start=2,end=3)` 1 call |
| 12 | AC-9 (4.5) bare `rerun-tasks <idx>` IDENTICAL to explicit `--phase --tasks` | PASS | ATTACK 5: bare and `--phase 3 --tasks T03.02` both → `phase=3 tasks=['T03.02'] merge_back=True`, byte-identical kwargs |
| 13 | FR-4.5 (4.6) `--dry-run` prints ResumePlan + DriftAssessment + BoundaryReport, no execution | PASS | ATTACK 15: dry-run prints "Auto-resume plan", "drift:", "integrity gate", "re-run tasks:"; exit 0, zero dispatch |
| 14 | FR-4.4 (4.7) explicit-flag paths preserve TODAY's exact semantics | PASS | ATTACK 7: `--start 2 --end 3 --dry-run` → 0 auto_resume calls, takes `_print_dry_run` path ("Dry run:" + "Would execute phases 2"). git-stash: 74 passing tests = explicit-path regression guard |
| 15 | §7 verdict refinement: `passed = accept_suspect or validated_last`; partial non-blocking | PASS | ATTACK 8: validated last + half-written next → passed=True, next_unfinished surfaced in suspects, ZERO results/ mutation, quarantined empty. `_verdict` source = `accept_suspect or report.validated_last` (integrity.py:314) |
| 16 | `_blocking_reasons` no longer takes partial_paths param; no caller passes one | PASS | ATTACK 10: `inspect.signature(_blocking_reasons)` params = `['report']` only; `_verdict` params = `['report','accept_suspect']`. No `partial` token in either signature |
| 17 | Over-claim caught (last PASS but artifact missing) | PASS | ATTACK 9b: real `**Artifacts (Intended Paths):**` block, deliverable missing → validated_last=False, passed=False, blocking_reasons populated |
| 18 | NFR-3 coherence advisory never flips verdict | PASS | ATTACK 11: mocked `invoke_sonnet`→"SUSPECT:..." → coherence_warnings=1 but passed/validated_last UNCHANGED (True). `_advisory_coherence` runs AFTER verdict (integrity.py:81) |
| 19 | Decorator/signature alignment; both `--help` exit 0 | PASS | run signature: ctx first, then all 20 decorator dests in order (commands.py:214-235). Both --help exit 0 |
| 20 | resume/__init__.py exports ResumePlanner/DriftAssessor/BoundaryIntegrityGate/ResumeDecision | PASS | Import smoke `from ...resume import ResumePlanner, DriftAssessor, BoundaryIntegrityGate, ResumeDecision` → OK |
| 21 | ruff clean on commands.py + resume package | **PASS (FIXED)** | **MINOR defect found+fixed:** `resume/__init__.py` I001 import-block unsorted. After fix: "All checks passed!" on commands.py + resume/ + executor.py |
| 22 | Known intentional failure: `test_rerun_tasks_requires_phase_without_reflect_report` is FR-4.1, not a regression to revert | PASS | git-stash proof: base=7 failed (halt/watchdog/e2e family), Phase4=8 failed (+contract). The +1 fails on `assert exit_code != 0` because bare rerun now exit 0 (auto-detect). No-phase-index path gives sensible message (ATTACK 14: "phase-level interruption with no recoverable per-task failures... Use sprint run") |

---

## Summary

- Checks passed: 22 / 22
- Checks failed: 0
- Critical issues: 1 (fixed in-place)
- Issues fixed in-place: 2 (1 CRITICAL, 1 MINOR)

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | `commands.py` `_dispatch_resume_rerun` (~L480) | `run_rerun_tasks(config, phase=, tasks=, merge_back=True)` omitted 9 required keyword-only args (`from_reflect_report, dry_run, include_transitive, ignore_deps, force_merge, allow_loop, no_verify_checkpoints, bundle_dir, restore`) — all defaultless in the real signature. The AC-2 TASK-granularity resume path (design §7 canonical happy path) raised `TypeError: run_rerun_tasks() missing 9 required keyword-only arguments` at runtime. Phase 4 self-verification masked it with a `**kw`-absorbing fake. | Pass all 9 missing kwargs with their CLI default values (None/False). FIXED commands.py:480-487. |
| 2 | MINOR | `resume/__init__.py:16` | ruff I001: import block unsorted (`.models` group placed before `.drift`/`.integrity`/`.planner`). Item 4.7 checkpoint requires ruff clean across the resume package; Phase 4 log only verified commands.py. | Reorder to alphabetical: `.drift`, `.integrity`, `.models`, `.planner`. FIXED. |

---

## Actions Taken

- Fixed CRITICAL dispatch defect in `commands.py` `_dispatch_resume_rerun` by adding the 9 missing
  keyword-only arguments (`from_reflect_report=None, dry_run=False, include_transitive=False,
  ignore_deps=False, force_merge=False, allow_loop=False, no_verify_checkpoints=False,
  bundle_dir=None, restore=False`) to the `run_rerun_tasks` call.
  - Verified: called `_dispatch_resume_rerun` against the REAL `run_rerun_tasks` (not a fake);
    pre-fix → `TypeError` (9 missing kwargs); post-fix → `SystemExit(0)` (rerun engine ran fully).
- Fixed MINOR ruff I001 in `resume/__init__.py` by reordering the import block alphabetically.
  - Verified: `uv run ruff check` → "All checks passed!"; re-imported all 4 public symbols → OK.
- Classification proof: `git stash`-ed Phase 4 changes (commands.py, executor.py, resume/) →
  base = 7 failed (halt/watchdog/e2e family, PRE-EXISTING), Phase 4 = 8 failed (+ the intentional
  FR-4.1 contract test). My fix added ZERO new failures.

---

## Recommendations (for Phase 5, non-blocking for the gate)

- **P5 must add a real regression test for the dispatch signature.** The CRITICAL defect existed
  because verification used a `**kw`-absorbing fake. The Phase-5 AC-2 test
  (`test_resume_task_level_recoverable`) MUST either (a) assert against the real `run_rerun_tasks`
  signature via `inspect.signature`, or (b) use a fake whose signature MIRRORS the real one
  (explicit params, not `**kw`), so a future kwargs drift fails loudly.
- **P5 (deferred): update `test_rerun_tasks_requires_phase_without_reflect_report`** to the new
  FR-4.1 default-auto-detect contract (bare on no-recoverable index → ClickException/guidance;
  bare on interrupted index → AC-9 auto-detect). Do NOT revert auto-detect.
- **Pre-existing (separate triage, affects 5.4 "full suite green"):** the `invoke_haiku` ImportError
  (commit 70ef6486 haiku→sonnet rename) breaks `retrospective.py` + `test_summarizer.py` +
  `test_retrospective.py` collection. Not this task's regression; commands.py does not import
  retrospective. One-line-per-site remediation (`invoke_haiku`→`invoke_sonnet`) noted in the P3 report.

## QA Complete
