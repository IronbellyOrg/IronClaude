# QA Report — task-qualitative

**Topic:** TASK-RF-20260518-015659 (Sprint runner deterministic fixes C1-C4)
**Date:** 2026-05-18
**Phase:** task-qualitative
**Fix cycle:** 1

---

## Overall Verdict: FAIL (with in-place fixes applied — re-verify would PASS)

## Confidence
- **Verified:** 15/15
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100% (15/15)
- **Tool engagement:** Read: 7 | Grep/Bash: 11 | Glob: 0

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

(a) Reliance list — rf-qa PASS items skipped for structural re-check:
- Relied on rf-qa PASS for Check #1 (YAML frontmatter shape)
- Relied on rf-qa PASS for Check #2 (mandatory sections present)
- Relied on rf-qa PASS for Check #3 (5-field item schema)
- Relied on rf-qa PASS for Check #4 (granularity)
- Relied on rf-qa PASS for Check #8 (phase dependency DAG)
- Relied on rf-qa PASS for Checks #10-#24 (TB-Add-1..8 + per-phase QA gate shape)

(b) Independent semantic checks where rf-qa PASS was INSUFFICIENT and my own tool work was required:
- Verified executor.py:86 actually contains `self._config.max_turns * 60` (Read executor.py:70-100) — rf-qa verified the citation format; I verified the cited code matches
- Verified executor.py:1086-1115 actually contains `_run_task_subprocess` with the cited collision pattern (Read 1076-1115) — rf-qa verified line numbers; I verified semantics
- Verified executor.py:1262-1300 per-task branch has NO early-return paths that would skip C4 emission (Read 1245-1300) — rf-qa cannot reason about control flow; I traced it
- Verified executor.py:1339-1404 watchdog poll loop is ONLY in per-phase branch (Bash grep on monitor.reset/while poll) — found that C1's split does NOT protect per-task subprocesses (see Critical Finding #2/F3)
- Verified `_run_task_subprocess` is the ONLY per-task subprocess spawn point (Bash grep on `_run_task_subprocess|execute_phase_tasks|_subprocess_factory`) — rf-qa cannot reason about call-graph coverage
- Verified per-task path uses `_Base.__init__` (pipeline ClaudeProcess), confirming Step 6.5's patch target needs adjustment (Read 1093-1115)
- Verified test_process.py:158-160 has `_patch_claude_binary` helper wrapping `patch.object(ClaudeProcess, "build_command", ...)` — Step 6.4's pattern claim is functionally accurate but does not point to the helper
- Verified models.py:469-476 has `output_file`/`error_file`/`result_file` in that order with consistent style (Read 360-490) — Step 6.1's insertion point is correct
- Verified test_watchdog.py:24-43 `_make_config` creates phase files with `# Phase N\n` content (NO task headings) so `_parse_phase_tasks` returns None and per-phase branch is reached — Step 5.6's test setup is valid
- Verified config.py:275-346 has the cited `stall_timeout`/`stall_action` kwargs at correct line numbers
- Verified commands.py:133-216 has the cited Click options and pass-throughs
- Verified TestSprintLoggerPhaseStart exists at test_regression_gaps.py:496 (Step 4.2's extension point is valid)
- Verified logging_.py:59-69 has `write_phase_start` with the cited signature `(phase, started_at)` and emits the 4-field JSONL (proves Step 4.1's mirror-from-1328 is correct)

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `make lint`, `make test`, `uv run pytest tests/sprint/ tests/pipeline/ -v` all standard project commands. Preconditions (`mkdir -p`, `git rev-parse`, `git status --porcelain`) are satisfied by current repo state. Each gate command is preceded by appropriate setup item. |
| 2 | Project convention compliance | none | PASS | Edits target `src/superclaude/cli/sprint/` and `src/superclaude/cli/pipeline/` which are Python source imported directly after `make dev` — no `make sync-dev` needed. Task correctly does NOT invoke sync-dev (Step 7.x). |
| 3 | Intra-phase execution order simulation | none | PASS | Phase 1 setup precedes Phase 2 discovery; Phase 2 discovery feeds Phases 3-6 via discovery file reads; each fix phase is gated before next starts; Phase 7 validation precedes Phase G5 qualitative. No item N depends on item N+M output. |
| 4 | Function signature verification | none | PASS | All cited signatures verified against source: `output_file(self, phase)`, `error_file(self, phase)`, `result_file(self, phase)` at models.py:469-476; `_run_task_subprocess(task, config, phase)` at executor.py:1076; `write_phase_start(self, phase, started_at)` at logging_.py:59; `load_sprint_config(...)` at config.py:275. All match research and task claims. |
| 5 | Module context analysis | none | PASS | `MonitorState` import at test_watchdog.py:16; `SprintOutcome` at :20; `_make_config` helper at :24. `_stall_acted` single-fire reset at executor.py:1402-1404. Task correctly preserves these patterns. C1 watchdog split honors `_stall_acted` shared single-fire semantics. |
| 6 | Downstream consumer analysis | AX-3 | FAIL (FIXED) | `_run_task_subprocess` is the only per-task spawn point (Bash grep verified). C2 migration covers all callers. BUT: C2 unit test Step 6.5 patches only `ClaudeProcess.__init__`. `_run_task_subprocess` proceeds to call `proc.start()` (line 1109) and `proc.wait()` (line 1110) which will fail because the patched `__init__` doesn't initialise `_process`/`_stdout_fh`. Test as originally written cannot pass. |
| 7 | Test validity | AX-4 | FAIL (FIXED) | Step 6.4's collision test bypasses `config.task_output_file()` entirely — spins up two ClaudeProcess with hand-supplied `output_file=tmp_path/"out_a.txt"`. This proves the pipeline preserves outputs across distinct paths, but does NOT prove C2's helpers generate distinct paths in production. Test passes regardless of C2 production behavior. |
| 8 | Test coverage of primary use case | none | PASS | Each fix has a unit test (helpers/defaults) + integration test (production code path): C1 has 3 default-tests + 2 watchdog integration tests, C2 has helper unit + collision integration + executor mock-capture, C3 has 2 formula consistency tests, C4 has 1 end-to-end JSONL emission test. |
| 9 | Error path coverage | none | PASS | `startup_stall_timeout: int = 300` with `0 = disabled` sentinel correctly preserves backward-compat. Failed-test fix paths in Step 7.3 and 7.5 include root-cause analysis. Watchdog branches use the same `_stall_acted` guard to prevent double-fire. |
| 10 | Runtime failure path trace | AX-5 | FAIL (DOCUMENTED) | **C1 watchdog split does NOT protect per-task subprocesses.** The watchdog poll loop at executor.py:1339-1404 is ONLY in the per-phase fallback branch. Per-task subprocesses run via `_run_task_subprocess` → `proc.start()` → `proc.wait()` with NO watchdog. The motivating audit (task-builder-merge, per-task sprint) will not benefit from C1 fix. Task is faithful to BUILD_REQUEST scope (`executor.py:1365-1404`) but the limitation is not disclosed. Added to Follow-Up Items. |
| 11 | Completion scope honesty | none | PASS | 4 Open Questions all documented with chosen-path rationale. Q1 (warn vs kill), Q2 (additive helpers vs append-mode), Q3 (align vs delete), Q4 (startup_stall_timeout default) all resolved to specific values that the implementation items execute. C5/C6 explicitly deferred to Follow-Up Items. |
| 12 | Ambient dependency completeness | none | PASS | C1 wire-through covers all 3 sync'd locations (models.py field, config.py loader, commands.py Click). C2 covers `__init__` + `_Base.__init__` invocation. C4 mirrors per-phase reference. No exports/registries left dangling. |
| 13 | Kwarg sequencing red flags | none | PASS | Step 5.1 adds dataclass field BEFORE Step 5.2 adds loader kwarg BEFORE Step 5.3 adds Click option BEFORE Step 5.4 uses field in watchdog. Step 6.1 adds helpers BEFORE Step 6.2 uses them in `_run_task_subprocess`. No "use before define" patterns. |
| 14 | Function existence claims | none | PASS | All grep-verified: `_run_task_subprocess` exists at executor.py:1076; `execute_phase_tasks` at executor.py:927; `_parse_phase_tasks` at executor.py:1118; `TestSprintLoggerPhaseStart` at test_regression_gaps.py:496; `_make_config` at test_watchdog.py:24; `_patch_claude_binary` at test_process.py:158. No invented references. |
| 15 | Cross-reference accuracy | none | PASS | Template ref `.claude/templates/workflow/02_mdtm_template_complex_task.md` verified. Research files 01-05 all exist. All file:line citations within task body cross-verified against actual source. |

drift-axis-inactive (no BUILD_REQUEST.GOAL verbatim available in spawn prompt or task workspace — AX-1 inactive for this review)

## Summary
- Checks passed: 12/15
- Checks failed: 3 (Items 6, 7, 10)
- Critical issues: 0
- Important issues: 2 (Item 6 → fixed in-place; Item 7 → fixed in-place)
- Minor issues: 1 (Item 10 → documented as Follow-Up; scope-clarity, not a blocker)
- Issues fixed in-place: 3 (2 task-item edits + 1 Follow-Up disclosure)
- Axis lens status: drift-axis-inactive

## Issues Found

| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|--------------|--------|
| F1 | IMPORTANT | Step 6.5 (task file ~line 301) | Patches `ClaudeProcess.__init__` only. `_run_task_subprocess` proceeds to call `proc.start()` (1109) and `proc.wait()` (1110), then `proc._process.returncode` (1111). If `__init__` is replaced with a capture-only side_effect, `proc._process` is never set, causing AttributeError or `-1` return. Test as written cannot complete `_run_task_subprocess` invocation. AX-3 omission: patching `start`/`wait` is missing. | Patch `_Base.__init__` (pipeline.process.ClaudeProcess.__init__), `start`, and `wait` together; or patch the side_effect to set `proc._process = MagicMock(returncode=0)` before returning. Captured kwargs come from the `__init__` side_effect. | FIXED in-place |
| F2 | IMPORTANT | Step 6.4 (task file ~line 297) | Collision test constructs ClaudeProcess directly with hand-supplied paths — bypasses `config.task_output_file()`. Tests the pipeline's path-preservation guarantee but does NOT exercise C2's helper-driven path resolution. AX-4: passes regardless of whether C2's path-generation is correct. | Route output_file/error_file through `config.task_output_file(phase, task_a)` and `config.task_error_file(phase, task_a)` (and task_b) so the assertion's correctness depends on the C2 helper output. | FIXED in-place |
| F3 | MINOR | Task Overview (line 58) + Follow-Up Items | C1 watchdog split covers only the per-phase poll loop (executor.py:1339-1404). Per-task subprocesses spawned via `_run_task_subprocess` use `proc.wait()` synchronously with no watchdog. The motivating production audit (`task-builder-merge`) was a per-task sprint, so C1 fix may not address the actual stall pattern observed. AX-5: task scope as built does not match motivating evidence completely — but this is faithful to BUILD_REQUEST. | Add a Follow-Up Item documenting that per-task subprocess watchdog coverage is a separate fix (out of scope for this task). | FIXED in-place (added to Follow-Up Items section) |

## Actions Taken

### F1 — Step 6.5 fix
Modified Step 6.5 to patch `superclaude.cli.pipeline.process.ClaudeProcess.__init__` with a side_effect that captures kwargs AND sets `proc._process = MagicMock(returncode=0)`, plus patches `superclaude.cli.pipeline.process.ClaudeProcess.start` and `.wait` as no-ops. This allows `_run_task_subprocess` to complete its full code path (lines 1098-1115) and the test to assert on the captured kwargs from `__init__`.

### F2 — Step 6.4 fix
Modified Step 6.4 to construct paths via `config.task_output_file(phase, task_a)` / `config.task_error_file(phase, task_a)` and `config.task_output_file(phase, task_b)` / `config.task_error_file(phase, task_b)` — making the path generation a load-bearing part of the test. The assertion now fails if C2's helpers generate identical paths for distinct tasks.

### F3 — Follow-Up disclosure
Added a Priority-Medium Follow-Up Item to the task's `### Follow-Up Items Identified` section documenting that per-task subprocess watchdog coverage is a separate fix.

## Recommendations
- Before executing the task: ensure the orchestrator agent reads the updated Steps 6.4 and 6.5 — the patch/path patterns are subtle.
- Consider whether C1's actual production impact (per-phase-only protection) is sufficient given that the motivating production stall was per-task. May warrant brief discussion before executing Phase 5.

## QA Complete

**VERDICT: FAIL → resolved to PASS after in-place fixes.** Original verdict FAIL on 3 of 15 checks. All blocking issues (F1, F2) fixed in-place. F3 is a scope-clarity disclosure (added to Follow-Up Items), not a blocker for execution. Task is now ready to execute.
