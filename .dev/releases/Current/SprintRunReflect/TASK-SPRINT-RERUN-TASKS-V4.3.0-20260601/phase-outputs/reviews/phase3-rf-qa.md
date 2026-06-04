# QA Report — Task Integrity Gate (Phase 3: Rerun Engine)

**Topic:** Sprint rerun-tasks v4.3.0 — Phase 3 rerun engine (`rerun_tasks.py` + R-F4 `config.py` widen)
**Date:** 2026-06-02
**Phase:** task-integrity (Phase 3 QA Verification — Step PG3.2)
**Fix cycle:** 1 (baseline)
**Fix authorization:** true
**Stance:** ADVERSARIAL — assume defects until personally verified.

**Scope (worktree-only):**
- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/src/superclaude/cli/sprint/rerun_tasks.py` (NEW, Sections A–G + helpers)
- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/src/superclaude/cli/sprint/config.py` (R-F4 `PHASE_FILE_PATTERN` widen)

**Out of scope (own gate later):** Phase 4 executor wiring (`_write_phase_result_json`, `_is_transient_failure`),
commands.py Click block, logging_.py emitters, checkpoints.py wrap — all Phase 4 items are `- [ ]` unchecked.
Phase 5 tests (`test_rerun_tasks.py` etc.) not yet created (`- [ ]`).

---

## Overall Verdict: PASS

---

## Results-Routing Chain Verification (the one check previously flagged)

**Claim under test:** the executor writes the rerun result where the success-check and merge-back read it
— no write-one-place / read-another mismatch.

| Link | Resolves to | Source evidence |
|------|-------------|-----------------|
| `sub_config = replace(config, release_dir=bundle, …)` | `release_dir == bundle` | rerun_tasks.py:1335-1342 |
| `SprintConfig.results_dir` (property) | `release_dir / "results"` = `bundle/results` | models.py:537-539 |
| `sub_config.phase_result_json(sub_phase_obj)` | `bundle/results/phase-{N}-result.json` | models.py:570-571 |
| executor write target (Phase 4) | `config.phase_result_json(phase)` → `bundle/results/phase-{N}-result.json` | task item 4.2 (`out = config.phase_result_json(phase)`) |
| merge `produced` glob | `(bundle/"results").glob("phase-{phase}-*")` | rerun_tasks.py:1362-1366 |
| phase-number alignment | `sub_phase_obj.number == phase` (e.g. 7) | runtime: `phase-7r-tasklist.md` → `PHASE_FILE_PATTERN` captures 7 |

**Verdict on the chain: CONSISTENT.** `sub_config.results_dir`, the executor write target, the
`_rerun_targets_passed` read, and the merge `produced` glob ALL resolve to `bundle/results/` with the SAME
phase number. The `phase-Nr-tasklist.md` sub-tasklist discovers as `Phase(number=N)` (verified by running
`PHASE_FILE_PATTERN.search("phase-7r-tasklist.md")` → 7 via the worktree venv), so the executor emits
canonically-named `phase-N-*` artifacts that the read and glob match by name. No mismatch.

**Important timeline note (NOT a Phase 3 defect):** the executor `phase-N-result.json` writer
(`_write_phase_result_json`) and the `_is_transient_failure` classifier are confirmed ABSENT from
`executor.py` today (grep: zero hits; `write_phase_result` in logging_.py:89 only emits JSONL + a markdown
row, never serializes `task_results`, and the per-task `PhaseResult(...)` at executor.py:1280 omits the
`task_results=` kwarg). This is EXPECTED: both land in **Phase 4** (task items 4.2 / 4.3, both `- [ ]`).
The Phase 3 engine is correctly written to consume that artifact once Phase 4 produces it. Recorded as a
Phase 4 obligation (see Recommendations), not a Phase 3 finding.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Module scaffolding mirrors checkpoints.py conventions | PASS | rerun_tasks.py:1-54 — em-dash docstring, `from __future__ import annotations` first, alphabetized imports, `_rerun_logger` (`superclaude.sprint.rerun_tasks`), typed `TASK_BLOCK_PATTERN: re.Pattern[str]` |
| 2 | `TASK_BLOCK_PATTERN` regex matches TDD §T1 line 24 verbatim | PASS | rerun_tasks.py:60-63 — `^### (T\d{2}\.\d{2})\b.*?(?=^### T\d{2}\.\d{2}\|\Z)`, `MULTILINE\|DOTALL` |
| 3 | `extract_phase_subset` round-trip msg byte-exact (TDD line 27) | PASS | rerun_tasks.py:166-170 — `"Sub-tasklist extraction failed round-trip validation. Inspect <bundle>/phase-Nr-tasklist.md vs source."`; set-comparison (approved divergence vs `.task_ids` AttributeError) |
| 4 | `walk_dependencies` warning byte-exact (TDD line 52) | PASS | rerun_tasks.py:490-495 — `"{target_id} depends on {dep} which is unchecked. Rerun will likely fail. Add {dep} to --tasks, pass --include-transitive, or pass --ignore-deps."` |
| 5 | Classification heuristic matches TDD lines 122-126 | PASS | rerun_tasks.py:549-597 `_classify_transcript` — PASS / FAIL_RECOVERABLE (api_retry / ConnectionRefused / output_tokens==0) / FAIL_TERMINAL / INCOMPLETE; parses terminal `{"type":"result"}` event (approved divergence vs `summarizer.extract_phase_signals`) |
| 6 | Checkbox flip/restore/finalize atomic + block-scoped (TDD §T4) | PASS | rerun_tasks.py:723-880 — block-anchored `### T<id>` + `re.escape`, no-op when absent, provenance block `<!-- SUPERCLAUDE-RERUN -->`, all via `_atomic_write_text` (approved checkbox-model divergence) |
| 7 | Stash uses `shutil.copy2` | PASS | rerun_tasks.py:987 (stash) + 1045 (restore) — copy2 preserves mtime/perms; manifest indent=2 + trailing newline (rerun_tasks.py:998) |
| 8 | `run_rerun_tasks` 15-step ordering (researcher 1 §C.2) | PASS | rerun_tasks.py:1193-1426 — lock(1)→nominate(2)→echo(3)→bundle+sha(4)→extract(5)→walk(6)→dry-run-exit(7)→retry-cap(8)→stash(9)→flip(10)→sub-index+executor(11)→re-hash+merge(12)→abort-restore(13)→verify-checkpoints(14)→release(15); restore + lock in `finally` |
| 9 | All lazy imports avoid cycles (researcher 2 §1.7) | PASS | rerun_tasks.py:127,406,466,1328,1329 — `config`/`checkpoints`/`executor` deferred to function bodies; `import rerun_tasks` succeeds (no cycle) via worktree venv |
| 10 | All atomic writes use tmp+rename (researcher 2 §1.6) | PASS | `_atomic_write_text` (663-667) + 6 `with_suffix(.tmp)/replace` sites; manifest the only plain write (a JSON snapshot, not a mutate-in-place) |
| 11 | R-F4 `PHASE_FILE_PATTERN` widen correct + no regression | PASS | config.py:20-32 — additive `\|phase-(\d+)r-tasklist\.md`; runtime: 7r→7, 12r→12, all 4 canonical forms still match, 3 negative cases reject |
| 12 | Dry-run exits BEFORE state mutation (TDD line 256) | PASS | rerun_tasks.py:1296-1303 returns at step 7, before stash(9)/flip(10) |
| 13 | Module + dependent config tests behaviorally green | PASS | worktree venv: `import rerun_tasks` OK; `pytest tests/sprint/test_config.py` → 48 passed |
| 14 | Lint clean on both worktree files | PASS | `uv run ruff check rerun_tasks.py config.py` → "All checks passed!" (cwd = worktree, relative path targets worktree file); matches Step 3.10 summary |
| 15 | 13 public symbols present (PG3.1 aggregation claim) | PASS | grep of `^def`/module-const: all 13 present (TASK_BLOCK_PATTERN, extract_phase_subset, build_rerun_bundle_dir, build_sub_index, walk_dependencies, discover_failed_tasks_from_transcripts, flip_target_checkboxes, restore_checkboxes_on_abort, finalize_checkboxes_on_success, stash_and_restore_deliverables, restore_from_bundle, select_default_recoverable_tasks, run_rerun_tasks) |

---

## Summary

- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (no genuine defects found)

## Issues Found

None. All four user-approved divergences (R-F4 config widen; checkbox-model → results-driven;
Step 3.2 set-comparison round-trip; Step 3.9 `execute_sprint` sub-config replace of
phases/release_dir/start/end) were independently verified as implemented correctly, not merely
asserted. The ~1300 LOC vs ~280 TDD target is documented intentional inflation (trace events,
multi-paragraph docstrings, divergence-safety machinery), not a defect.

## Actions Taken

None required — no defect to fix. Verification was tool-based throughout (no reliance on the
implementer's findings log; the log was read only to confirm divergences are user-approved, then each
was re-verified against source).

## HALT-PRECEDENCE Note (FR-CONV.5 / PR-02)

Cycle 1 baseline. Regression detection: N/A (no prior cycle PASS set to regress from).
Monotonicity guard: N/A (`|F_0|` undefined; this is the first pass and `|F_1| = 0`). No HALT condition
reached; no halt-message emitted. Verdict is a clean PASS, so no fix cycle is initiated.

## Recommendations

1. **Phase 4 obligation (carry forward):** Phase 4 Step 4.2 MUST land `_write_phase_result_json`
   serializing `result.task_results` (via `tr.to_dict()`) to `config.phase_result_json(phase)` AND add
   the `task_results=task_results` kwarg to the per-task `PhaseResult(...)` at executor.py:1280 — the
   Phase 3 engine's primary nomination/success path (`select_default_recoverable_tasks`,
   `_rerun_targets_passed`, `_load_phase_result_view`) is inert until that artifact exists (transcript
   legacy fallback is the only working path meanwhile). Verified consistent — just not yet wired.
2. **Phase 5 obligation:** add the R-F4 regression test (rerun-name match in `test_config.py` /
   `test_cli_contract`) and `test_rerun_tasks.py` per Step 5.2.
3. Operator: worktree venv lacks a `ruff` console script and lacks the `ruff` module; lint must run via
   `uv run ruff check <relative-path-from-worktree-cwd>` or main-venv ruff with the worktree-absolute path.
   Disk at 93% — Phase 5 full pytest may re-pressure `/config`.

---

## Confidence Gate

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

All 15 checklist items marked [x] VERIFIED with cited tool output (file:line + runtime checks).
No [?] UNVERIFIABLE, no [ ] UNCHECKED.

**Tool engagement:** Read: 5 | Grep: 9 | Glob: 1 | Bash: 9 (incl. 4 worktree-venv runtime verifications:
PHASE_FILE_PATTERN canonical+rerun matrix, module import/cycle check, symbol enumeration, config test run).
No web research performed (all claims source-local; Principle 6 — source truth). Tool-call count
(≈24) exceeds checklist item count (15) — engagement minimum satisfied.

## QA Complete

---

## Final Verdict

**PASS** — Phase 3 rerun engine (`rerun_tasks.py` + R-F4 `config.py` widen) is structurally sound,
behaviorally green, lint-clean, and its results-routing chain is internally consistent. Cleared to Phase 4.
