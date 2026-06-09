# Tier 1 Observation — Real-Code Grounding

## Target
- SoT files (corrected): merge-back lives in `src/superclaude/cli/sprint/recovery.py` (`merge_recovery_bundle`), NOT `executor.py` as the request stated. verify-checkpoints lives in `src/superclaude/cli/sprint/commands.py` (CLI) + `src/superclaude/cli/sprint/checkpoints.py` (logic). Orchestration in `src/superclaude/cli/sprint/rerun_tasks.py` (`run_rerun_tasks`).

## SYMPTOM 1 — merge-back strands TASKLIST_ROOT deliverables, logs success

Grounded chain:
1. `rerun_tasks.run_rerun_tasks` runs the rerun in an ISOLATED sub-config with `release_dir=bundle` (rerun_tasks.py:1420) and a sub-index whose `TASKLIST_ROOT` is set to the bundle dir (rerun_tasks.py:319). → rerun agents write deliverables into `<bundle>/tasklists/artifacts/<D-ID>/` and `<bundle>/tasklists/evidence/<TASK>/`.
2. The merge's `artifacts_produced` is built ONLY from `<bundle>/results/phase-N-*` files (rerun_tasks.py:1444-1446). The TASKLIST_ROOT deliverable trees are NOT included.
3. `merge_recovery_bundle` (recovery.py:381-687) copies back ONLY `artifacts_produced` items whose `.name` matches a canonical `phase-N-task-*-output.txt` / `phase-N-cp*.md` / `-errors.txt` filename (steps 1-3, recovery.py:440-500). There is NO step that copies the `tasklists/artifacts/<D-ID>/` or `tasklists/evidence/<TASK>/` trees into canonical, and NO verification they landed.
4. `failures` (recovery.py:431) only accumulates from the steps that DO run; since none touch the deliverable trees, it stays empty → `bundle.status = SUCCESS` (recovery.py:674) and audit log records `status: success, failures: []` (recovery.py:676-687). **Matches the symptom exactly.**

The `stash_and_restore_deliverables` mechanism (rerun_tasks.py:991) is a PRE-rerun backup into `<bundle>/preserved/` for `--restore`; it is not a merge-forward of newly-produced deliverables.

## SYMPTOM 2 — checkpoint recovery no-op on stale verdicts

Grounded chain:
1. `recover_missing_checkpoints` (checkpoints.py:213-321) returns any entry whose `expected_path.is_file()` UNCHANGED (checkpoints.py:248-264). It only regenerates entries whose file is ABSENT.
2. It never reads existing checkpoint frontmatter / verdict; an existing checkpoint with stale `FAIL`/`BLOCKED` is left untouched.
3. `build_manifest` (checkpoints.py:138-170) records only `exists` (file present), no verdict. `verify_checkpoints` command (commands.py:663-702) prints "N declared | N found | 0 missing" and stops.
4. rerun's Step 14 auto-invokes `verify-checkpoints --recover` (rerun_tasks.py:1508-1532) — a no-op for stale-verdict files. → gated checkpoints stay FAIL/BLOCKED after a successful rerun+merge. **Matches the symptom exactly.**

A reusable verdict regex already exists: `summarizer.py:69` (`PASS|FAIL|COMPLETE|DONE|BLOCKED|SKIP`). Checkpoint reports carry YAML frontmatter. → a re-evaluate-stale mode is feasible.

## Documentation context
No formal external contract documents stranding-verification or stale re-eval as intended behavior. Code comments reference an internal "TDD §T5" (7-step merge) and "§T9" (auto-verify-checkpoints) but those steps were never specified to cover TASKLIST_ROOT deliverable trees or stale-verdict re-evaluation. → `behavior_is_documented = false`; this is a genuine code-side gap, not a documented contract.
