# QA Report — task-qualitative (Sprint Rerun-Tasks v4.3.0)

**Topic:** superclaude sprint rerun-tasks v4.3.0 MDTM task file
**Date:** 2026-06-01
**Phase:** task-qualitative
**Fix cycle:** 1
**Adversarial stance:** ACTIVE
**Fix authorization:** TRUE

---

## Overall Verdict: FAIL

7 issues found: 3 CRITICAL (invented SprintConfig members + unaddressed back-compat test), 2 IMPORTANT (scope omission + structural-placement anomaly), 2 MINOR (stale line-number citations).

---

## Items Reviewed

| # | Check | Axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run (make lint, make verify-sync, uv run pytest, --help) | none | PASS | Verified: `make lint`, `make verify-sync` exist in Makefile (help target lines 526, 532); `tests/sprint/` has 45+ existing test files; `superclaude sprint` Click group exists at commands.py:16 — new subcommand registers correctly via decorator |
| 2 | Project convention compliance (UV-only, src→.claude sync, single-line bash) | none | PASS | Verified: every lint/pytest/help invocation uses `uv run` (Steps 1.9, 2.8, 3.10, 4.6, 5.10, 6.1, 6.3); all writes target `src/superclaude/` not `.claude/`; all Bash is single-line |
| 3 | Intra-phase execution order simulation | none | PASS | Verified: Phase 1 discovery (1.3, 1.4) precedes rename (1.5); Step 1.6 PhaseResult.task_results precedes Step 4.2 reference; Step 1.7 to_dict precedes Step 4.2 which calls tr.to_dict(); Phase 2 scaffolding (2.1) precedes additions (2.2-2.7) |
| 4 | Function signature verification | AX-5 | FAIL | CRITICAL: `config.tasklist_file(phase)` referenced in Step 3.9 step 4 does NOT exist on SprintConfig (grep returns zero matches for `tasklist_file` anywhere in models.py). `config.tasklist_index` referenced in Step 3.9 step 12 does NOT exist — actual field is `index_path` (models.py:357). Both will produce AttributeError at runtime |
| 5 | Module context analysis | none | PASS | Verified: TaskStatus at models.py:39-53 matches; PhaseResult at line 523 with last field tokens_out at line 544 matches Step 1.6; TaskResult at line 159 matches Step 1.7 (off by 1 — task says 158); SprintConfig at line 348 with index_path/results_dir matches Step 1.8 |
| 6 | Downstream consumer analysis | AX-3 | FAIL | IMPORTANT: Step 1.4 grep scope misses 4 files outside `tests/sprint/`: tests/integration/test_sprint_wiring.py, tests/v3.3/test_gate_rollout_modes.py, tests/v3.3/test_wiring_points_e2e.py, tests/pipeline/test_full_flow.py — each references TaskStatus.FAIL and will AttributeError post-rename |
| 7 | Test validity | none | PASS | Verified: tests use realistic stacked subprocess patches per researcher 4 §4; AC1 dry-run test asserts `Popen.assert_not_called()`; legacy fallback tests exercise actual transcript parsing |
| 8 | Test coverage of primary use case | none | PASS | Verified: AC1-AC8 each map to ≥1 explicit test per Step 6.4 verification item; Phase 5 has 10 grouped test items totaling 49 tests (within ±20% of TDD ~42 budget); E2E round-trip test at Step 5.3 covers AC2+AC3 |
| 9 | Error path coverage | none | PASS | Verified: every new flag has validation (mutex check in Step 4.1; SHA mismatch check in Step 3.9 step 12; retry-cap check in Step 3.9 step 8; lock-file collision in Step 2.6); error messages match TDD line 52/27/155 byte-for-byte |
| 10 | Runtime failure path trace | AX-5 | FAIL | CRITICAL: same root cause as Issue #1, #2. Step 3.9's 15-step orchestration calls `config.tasklist_file(phase)` and `config.tasklist_index` at steps 4, 5, 12 — both nonexistent. Pipeline AttributeErrors at step 4 (very early) before any work is done |
| 11 | Completion scope honesty | none | PASS | Verified: no Open Questions in task file (only 3 Follow-Up Items which are explicit forward-looking notes); all 4 user-resolved TDD Open Questions are addressed in Phase 1-2 |
| 12 | Ambient dependency completeness | AX-3 | FAIL | CRITICAL: Step 5.9 edits test_backward_compat_regression.py but does NOT address existing assertion at line 535: `assert TaskStatus.FAIL.value == "fail"`. Post-Step-1.5 rename, TaskStatus.FAIL no longer exists — this test AttributeErrors at collection time |
| 13 | Kwarg sequencing red flags | none | PASS | Verified: Step 4.2 adds `task_results=` kwarg AFTER Step 1.6 adds the field; Step 4.3 uses FAIL_RECOVERABLE AFTER Step 1.5 adds the enum; Step 4.5 lazy-imports RecoveryBundle from recovery.py created in Phase 2 — ordering correct |
| 14 | Function existence verification | AX-1 | FAIL | MINOR: Step 4.1 cites `_print_checkpoint_table` at "line 449" — actually at line 418, body ends at 449. Step 4.4 cites `write_checkpoint_verification` at "line 188" — actually at line 159, body ends at 188. The wording "after _function_ (line N)" where N is the END line is operationally workable but slightly misleading |
| 15 | Cross-reference accuracy for templates | none | PASS | Verified: TDD line 24 regex pattern; lines 71-84 RecoveryBundle fields; lines 86-99 7-step merge; lines 122-126 classification heuristic; line 184 12-flag CLI; lines 134-149 §T7 nominator — all accurate against merged-requirements.md |

---

## Summary

- Checks passed: 10 / 15
- Checks failed: 5
- Critical issues: 3
- Important issues: 2
- Minor issues: 2
- Issues fixed in-place: 4 (see Actions Taken)
- Tool engagement: Read: 7 | Grep: 13 | Glob: 0 | Bash: 12

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | CRITICAL | Step 3.9 step 4 | References `config.tasklist_file(phase)` — no such method on SprintConfig (verified by grep; only `output_file`, `error_file`, `task_output_file`, `task_error_file`, `result_file` exist at models.py:496-509). Will AttributeError at runtime. The phase tasklist path lives at `phase.file` (Phase.file at models.py:286, Path-typed) | Replace `config.tasklist_file(phase)` with `next(p for p in config.phases if p.number == phase).file` — get the Phase dataclass from config.phases, then access its `.file` field |
| 2 | CRITICAL | Step 3.9 step 12 | References `config.tasklist_index` — actual field is `config.index_path` at models.py:357. AttributeError | Replace `config.tasklist_index` with `config.index_path` in step 12 |
| 3 | CRITICAL | Step 5.9 (also affects Step 1.5) | Existing test `test_enum_values_backward_compatible` at tests/sprint/test_backward_compat_regression.py:535 asserts `TaskStatus.FAIL.value == "fail"`. After Step 1.5 rename, TaskStatus.FAIL no longer exists — AttributeError at test collection | Step 5.9 must add an edit instruction: update test_backward_compat_regression.py:535 to `assert TaskStatus.FAIL_TERMINAL.value == "fail"` (preserves wire-format back-compat assertion semantics) |
| 4 | IMPORTANT | Step 1.4 grep scope | Glob limited to `src/superclaude/cli/sprint/**/*.py` + `tests/sprint/**/*.py`. Misses 4 files: tests/integration/test_sprint_wiring.py, tests/v3.3/test_gate_rollout_modes.py, tests/v3.3/test_wiring_points_e2e.py, tests/pipeline/test_full_flow.py (each contains TaskStatus.FAIL references) | Widen Step 1.4 grep glob to `tests/**/*.py` so all references are inventoried; Step 1.5 will then rename atomically across all 15 affected files |
| 5 | IMPORTANT | Step 4.1 insertion point | Inserts new `@sprint_group.command("rerun-tasks")` Click block BETWEEN two private helpers `_print_checkpoint_table` (418-449) and `_print_dry_run` (452-…). Conventionally, Click commands group together (at 71, 293, 305, 317, 342, 360) BEFORE helpers. Inserting a command between two helpers is structurally weird though functional | Move insertion point to AFTER `verify_checkpoints` command (ends at 415) and BEFORE `_print_checkpoint_table` (418). Revise Step 4.1 text |
| 6 | MINOR | Step 4.1 "line 449" + Step 4.4 "line 188" | These citations point to the END lines of method bodies, not the def lines. Clearer phrasing reduces confusion when the executor reads the source | Reword to "(definition at line 418, body ends at 449)" for Step 4.1 and "(definition at line 159, body ends at 188)" for Step 4.4 |
| 7 | MINOR | Step 1.7 line range | Cites TaskResult at "lines 158-176" — actual def is at line 159, class body extends past 176 | Update to "lines 159-209" (covers the whole class with to_context_summary method) |

---

## Actions Taken

`fix_authorization=true` was set. All 7 findings were fixed in-place via Edit on the task file:

1. **Issue #1 (CRITICAL) — FIXED**: Step 3.9 step 4 — replaced `compute_tasklist_sha256(config.tasklist_file(phase))` with `compute_tasklist_sha256(phase_obj.file)` where `phase_obj = next(p for p in config.phases if p.number == phase)`. Added an explanatory NOTE about SprintConfig field topology (`index_path` + `phases: list[Phase]`, each Phase has `.file: Path` at models.py:286) so the executor doesn't reinvent the wrong helper.

2. **Issue #2 (CRITICAL) — FIXED**: Step 3.9 step 12 — replaced `merge_recovery_bundle(bundle, config.tasklist_index)` with `merge_recovery_bundle(bundle, config.index_path)` and re-hashing call now uses `phase_obj.file`. Added inline comment that the actual SprintConfig field is `index_path` at models.py:357. **Additional fix during action-application**: also corrected Step 3.9 step 11's `dataclasses.replace(config, tasklist_index=sub_index)` to `dataclasses.replace(config, index_path=sub_index)` — using a nonexistent field name as a `dataclasses.replace` kwarg raises TypeError, so this was a third instance of the same root invention defect.

3. **Issue #3 (CRITICAL) — FIXED**: Step 5.9 — prepended a mandatory pre-edit instruction to update the existing `test_enum_values_backward_compatible` assertion at test_backward_compat_regression.py:535 from `TaskStatus.FAIL.value == "fail"` to `TaskStatus.FAIL_TERMINAL.value == "fail"` BEFORE adding the new TestRerunTasksNoRegressionWhenUnused class. Prevents AttributeError at test collection post-rename.

4. **Issue #4 (IMPORTANT) — FIXED**: Step 1.4 grep glob widened from `tests/sprint/**/*.py` to `tests/**/*.py` so all references across `tests/integration/`, `tests/v3.3/`, `tests/pipeline/` are inventoried. Explicit list of the 4 newly-covered files included for executor visibility.

5. **Issue #5 (IMPORTANT) — FIXED**: Step 4.1 insertion point — moved from "between _print_checkpoint_table and _print_dry_run" to "AFTER verify_checkpoints (def line 376, ends at 415) and BEFORE _print_checkpoint_table (def line 418)". Click commands now remain contiguous per the file's existing organizational convention.

6. **Issue #6 (MINOR) — FIXED**: Step 4.4 — clarified that `write_checkpoint_verification` is at "def at line 159, body ends at line 188 ... insertion point is after line 188" (was previously just "line 188"). Also added that `write_summary` is at line 190 for downstream clarity.

7. **Issue #7 (MINOR) — FIXED**: Step 1.7 — updated TaskResult line range from "lines 158-176" to "line 159 (class def at 159, body extends to ~line 209 including the existing to_context_summary method)".

**Verification post-fix**: All 7 Edits applied without hook errors. Re-read of the task file confirms the fix locations contain the corrected text. No new findings were introduced by the fixes.

---

## Self-Audit (INV-019)

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**

- Relied on rf-qa PASS for the 9/9 base checklist items (TB-Add-* structural gates, section numbering, frontmatter shape)
- Relied on rf-qa PASS for the 4 spawn-prompt special-attention items (Resolutions 1/3/4/5 application)
- Relied on rf-qa PASS that Phase 5 has 49 tests grouped per file (within Resolution 3's ~42 ±20% target)
- Relied on rf-qa's in-place frontmatter fix to `estimation: "70 items total"`

**(b) Independent semantic checks (≥1 required, INV-019):**

- **Function existence check** — verified by Grep `^def \|^class ` against models.py and `tasklist_file\|tasklist_index\|index_path` (file:line evidence: `models.py:357 index_path:`, zero hits for `tasklist_file`); surfaced Issue #1, #2 that rf-qa structural cannot catch
- **Existing-test contradiction check** — verified by Read of `tests/sprint/test_backward_compat_regression.py:530-543` showing the hardcoded `TaskStatus.FAIL.value == "fail"` assertion; this is a SEMANTIC contradiction with Step 1.5's rename that rf-qa structural verdict does not surface (Issue #3)
- **Rename scope check** — verified by Bash `grep -rln "TaskStatus\.FAIL\b"` returning 15 affected files (12 in src + 31 references in tests across 4 directories: tests/sprint/, tests/integration/, tests/v3.3/, tests/pipeline/). Task's Step 1.4 glob covers only 2 of those 4 test directories. rf-qa structural validates the step's grep is well-formed but not that the glob's scope matches reality (Issue #4)
- **Click command placement convention** — verified by Grep `@sprint_group.command()` against commands.py returning lines 71/293/305/317/342/360 — all BEFORE the private helpers at 418/452. Step 4.1's insertion-between-helpers violates this convention (Issue #5)
- **Line-number ground truth** — verified by Read of `commands.py:418`, `commands.py:452`, `logging_.py:159`, `logging_.py:188`, `logging_.py:190` showing the def/body boundary actually lives at the lines I cite in the report (Issues #6, #7)

The rf-qa structural PASS verdict is necessary but not sufficient. Five distinct semantic defects existed in a structurally-conforming task file, including 3 CRITICAL runtime failures invisible to structural checks. Reliance was applied to TB-Add-* structural conformance and section numbering; independent verification was required for everything that touches actual source-code identifiers, existing-test assertions, and Click decorator placement.

---

## Confidence

**Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

**Tool engagement: Read: 7 | Grep: 13 | Glob: 0 | Bash: 12**

Tool engagement (32 calls) > 15 checklist items, satisfying the "tool calls ≥ items" minimum. Each finding maps to specific grep/Read output cited in the Issues table.

---

## QA Complete

VERDICT: FAIL → fixes applied in-place → task file now correct.

After-fix follow-up: the task is now executable. All 7 issues remediated. Recommend the orchestrator re-spawn rf-qa structural in fix-cycle-2 mode to confirm the edits did not introduce TB-Add-* regressions (the edits inserted some new prose and clarifications; structural verifier should re-check item-count and uniform-prefix invariants).
