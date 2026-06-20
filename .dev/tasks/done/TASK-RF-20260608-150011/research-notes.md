# Research Notes: Fix sprint recovery stranded-deliverables + stale-checkpoint defects

**Date:** 2026-06-08
**Scenario:** A (explicit — fix sites, line numbers, fixtures, design fork all pre-resolved by the troubleshoot diagnosis)
**Depth Tier:** Standard (6 files across 4 modules + 2 test files)
**Track Count:** 1 (both fixes interdependent — "ship together"; shared recovery-flow context)
**Source diagnosis:** `.dev/troubleshoot/sprint-merge-stranding-checkpoint-stale-20260608144847/REPORT.md`

---

## EXISTING_FILES
- `src/superclaude/cli/sprint/recovery.py` — `merge_recovery_bundle(bundle, source_index, *, release_dir=None)` at 381-687; 7-step merge; status flip at 674; audit log at 676-687; atomic tmp+replace at 519-521. **FIX 1 site.**
- `src/superclaude/cli/sprint/rerun_tasks.py` — `run_rerun_tasks` merge site 1436-1534; `_declared_deliverables(source_tasklist, task_id)` at 954-978; sub-index `TASKLIST_ROOT=bundle` at 319; `produced` glob at 1444-1446; merge call at 1484-1485; post-merge `finalize_checkboxes_on_success` at 1487; Step-14 verify-checkpoints auto-invoke at 1508-1532. **FIX 1 caller + FIX 2 primary site.**
- `src/superclaude/cli/sprint/checkpoints.py` — `recover_missing_checkpoints` 213-321 (existence short-circuit 248-264); `_render_recovered_checkpoint` 398-439 (UNKNOWN-not-PASS constraint 436-437); `build_manifest` 138-170; `extract_checkpoint_paths` 40-98 (TASKLIST_ROOT strip 74-79). **FIX 2 fallback site.**
- `src/superclaude/cli/sprint/commands.py` — `verify_checkpoints` CLI 647-702. **FIX 2 CLI wiring site.**
- `tests/sprint/test_recovery.py` — `_seed_release` line 28, `_full_recovery_manifest`, `class TestMergeRecoveryBundle` line 153, `test_merge_is_idempotent` line 179. **TEST A site.**
- `tests/sprint/test_checkpoints.py` — `_seed_sprint` line 293, `class TestRecoverMissingCheckpoints` line 407, `_full_recovery_manifest` line 600. **TEST B site.**

## PATTERNS_AND_CONVENTIONS
- UV only: `uv run pytest tests/sprint/... -v`. `make lint && make format` after edits. CLI .py changes do NOT need `make sync-dev`.
- Atomic writes: `tmp = path.with_suffix(path.suffix + ".tmp"); tmp.write_text(...); tmp.replace(path)` (recovery.py:519-521, 667-669).
- Forensic preservation: rename clobbered canonical to `.failed-<int(mtime)>` (recovery.py:444-449).
- Failures→status: `failures: list[str]`; `status = PARTIAL if failures else SUCCESS` (recovery.py:674).
- Local imports inside functions to avoid cycles (recovery.py:418, 530).

## GAPS_AND_QUESTIONS
1. Exact current signature + full body of the 4 functions to modify (builder needs precise insertion points).
2. Exact fixture code: `_seed_release`, `_full_recovery_manifest` (test_recovery.py); `_seed_sprint`, existing `TestRecoverMissingCheckpoints` tests + `test_does_not_overwrite_pre_existing_file` (test_checkpoints.py) — including imports, RecoveryBundle construction, assertion idioms.
3. `checkpoint_gate_mode` plumbing (SprintConfig) + how `--no-verify-checkpoints` flows; whether the end-of-phase checkpoint is a runnable TASK in generated tasklists (decides Fix 2 primary B vs fallback) — see `_check_checkpoint_pass` executor.py ~2518-2519 and CP-Pxx-END.md verdict reading.
4. Does the installed pipx copy differ from src/ (drift)? (Informational — fix targets src/.)

## RECOMMENDED_OUTPUTS
- `research/01-fix-site-signatures.md` — exact current code of the 4 target functions + insertion points + helpers (write_recovery_audit_log, _declared_deliverables, atomic-write).
- `research/02-test-fixtures.md` — exact fixture + existing-test code for both test files.
- `research/03-checkpoint-gate-plumbing.md` — checkpoint_gate_mode, verify-checkpoints flow, checkpoint-as-task analysis (Fix 2 B vs fallback).
- `research/04-template-and-conventions.md` — template 02 rules + existing task examples + branch/lint conventions.

## SUGGESTED_PHASES
- Researcher 1 (File Inventory / signatures): recovery.py + rerun_tasks.py + checkpoints.py + commands.py target functions. Output 01.
- Researcher 2 (Test & Verification): test_recovery.py + test_checkpoints.py fixtures + existing tests. Output 02.
- Researcher 3 (Integration / Data Flow): checkpoint gate plumbing + checkpoint-as-task question. Output 03. Covers what R1 does not (R1 = the merge/recover functions; R3 = the gate/config plumbing + executor checkpoint verdict read).
- Researcher 4 (Template & Examples): template 02 + task examples + conventions. Output 04.

## TEMPLATE_NOTES
Template 02 (complex). Phases: Branch setup → Fix 1 (recovery.py + rerun_tasks.py caller) → Test A → Fix 2 (checkpoints.py + commands.py + rerun_tasks.py re-verify) → Test B → Full validation (lint/format/pytest) → POST reflect handoff → Done. PER_PHASE QA not required (small focused change); FINAL_ONLY validation. TESTING_REQUIREMENTS: UNIT (the two regression tests are core deliverables).

## AMBIGUITIES_FOR_USER
None — intent, fix design, and the Defect-2 design fork are fully resolved in REPORT.md. One implementation decision (Fix 2 primary-B vs fallback) is conditional on whether the end-of-phase checkpoint is a runnable task; researcher 3 resolves this from the codebase, and the task file will branch accordingly.
