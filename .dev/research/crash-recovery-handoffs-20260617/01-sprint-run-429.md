# SprintRun429 handoff

## Current state

- Lane root: `/config/workspace/IronClaude/.dev/worktrees/SprintRun429`.
- Branch: `SprintRun429` at `59b9e2a2 fix(prd): two brittle-gate false-negatives that halt the heavyweight pipeline (verdict regex + assembly content-source) (#169)`.
- Remote checked read-only: `origin` is `https://github.com/IronbellyOrg/IronClaude.git`.
- Active task: `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/TASK-RF-429-recovery-20260615-040144.md`.
- Task frontmatter is still `status: "Doing"`. The checklist is not reconciled with the crash state: Phase 4 Step 4.6 and Step 4.7 remain unchecked in the task file, but the corresponding files/tests already exist on disk.
- Phase 2/P1 detector gate is complete and passed. Evidence is under `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/plans/p1-gate-final.md`.
- Phase 3/P2 taxonomy gate is complete and passed. Evidence is under `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/plans/p2-gate-final.md`.
- Phase 4/P3 policy + per-task executor work is partially implemented and currently failing the provider-exhaustion cap tests. There are no `p3-*` test-result artifacts yet under `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/`.
- Git status is dirty with modified tracked source/tests plus untracked task/spec/test fixtures/new policy file. Nothing was staged or committed by this handoff pass.

Dirty tracked files reported by `git status --short --branch`:

- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/executor.py`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/models.py`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/monitor.py`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/rerun_tasks.py`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_executor.py`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_models.py`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_monitor.py`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_rerun_tasks.py`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_resume.py`

Untracked paths reported by `git status --short --branch`:

- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/brainstorms/sprint-429-recovery-spec.md`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/recovery_policy.py`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/fixtures/`
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_recovery_policy.py`

## Evidence read, with absolute paths

- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/TASK-RF-429-recovery-20260615-040144.md` — task frontmatter, phase plan, Phase 4 Step 4.6/4.7/4.8 requirements, Phase 5+ remaining work, and source-of-truth constraints.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/tfep/provider-exhaustion-cap/context.yaml` — current TFEP failure context. It names the three failing new tests and records the observed cap+1 and parallel spawn-storm behavior.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/research/05-test-verification.md` — authoritative P3/P4 test expectations, including cap semantics, K>1 bound, persistence expectations, and later single-session test plan.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/discovery/executor-wiring-points.md` — P3 insertion-point inventory and intended latch/spawn discipline.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/recovery_policy.py` — current `SessionResetPolicy.decide` implementation: single-account retry while `attempt < max_session_resets`, halt at cap, all-account cooldown halt on any attempt.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/executor.py` — current `_run_one_task` re-spawn loop, latch precheck, unlocked spawn, detector/policy dispatch, sequential and parallel call sites, and policy construction.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_executor.py` — current provider-exhaustion executor tests and helper factories.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_recovery_policy.py` — current policy truth-table test.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/models.py` — current `TaskStatus.FAIL_PROVIDER_EXHAUSTED` taxonomy and failure membership.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/p1-summary.md` — P1 detector tests passed: 39 passed, 0 failed.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/p2-summary.md` — P2 taxonomy/resume tests passed: targeted 193 passed and backward-compat marker 20 passed/1 skipped.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/reports/p1-aggregate.md` — P1 aggregate manifest and invariants.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/reports/p2-aggregate.md` — P2 aggregate manifest and invariants.
- `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-SprintRun429/e0b1538c-06e3-44c7-a8d2-795ced5465e1.jsonl` — latest substantial SprintRun429 task-execution session log found by mtime.
- `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-SprintRun429/17154557-e3ba-480f-9a1e-c57378c20e49.jsonl` — latest SprintRun429 session log found by mtime.
- `/config/.claude/projects/-config-workspace-IronClaude/4e25f96f-1ad2-4e59-835b-4ddf5e5e57cd/tool-results/bt3wcx05s.txt` and `/config/.claude/projects/-config-workspace-IronClaude/4e25f96f-1ad2-4e59-835b-4ddf5e5e57cd/tool-results/batp52p80.txt` — grep outputs from this handoff search, too large to read directly but they confirm matches for the failing tests in session/artifact logs.

## Exact unfinished work and first next action

The active failure is Phase 4/P3 provider-exhaustion cap semantics in the per-task executor loop.

Current failing tests from `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/tfep/provider-exhaustion-cap/context.yaml`:

- `tests/sprint/test_executor.py::TestPerTaskOrchestration::test_provider_exhaustion_single_429_stops_at_cap`
- `tests/sprint/test_executor.py::TestPerTaskOrchestration::test_provider_exhaustion_parallel_latch_bounds_spawn_storm`
- `tests/sprint/test_executor.py::TestPerTaskOrchestration::test_provider_exhaustion_single_worker_stops_exactly_at_small_cap`

Expected vs observed from the TFEP context:

- cap 8 single worker expected 8 spawns, observed 9.
- cap 3 single worker expected 3 spawns, observed 4.
- cap 3 with K=4 expected total spawns in 3..6, observed 9.

Likely cause from the current code read:

- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/executor.py` initializes a loop-local `attempt = 0`, spawns, then calls `reset_policy.decide(signal.kind, attempt)`, and only increments `attempt` after `RETRY_NEW_SESSION`. With `SessionResetPolicy.decide` halting at `attempt == cap`, that encodes cap as retries after the first spawn, producing cap+1 total subprocess spawns in K=1.
- `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/recovery_policy.py` has `_exhaustion_attempts` on the shared policy, but the current executor read shows it is not used. The K>1 expected bound is global-total based (`cap <= total_spawns <= cap + (K - 1)`), so the next fix likely needs a lock-guarded shared exhaustion counter/latch decision, not only a loop-local off-by-one adjustment.

First next action:

1. Re-read `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/executor.py`, `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/recovery_policy.py`, `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_executor.py`, and `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/tfep/provider-exhaustion-cap/context.yaml` immediately before editing.
2. Fix the executor cap semantics so `max_session_resets` caps total provider-exhaustion subprocess spawns as the tests/spec require. For K=1, the policy should see the current total spawn count, not the zero-based retry count. For K>1, use the shared `SessionResetPolicy` state under the existing `guard` so one worker trips the latch at the cap and in-flight overshoot remains bounded by `K - 1`.
3. Preserve the load-bearing discipline from `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/discovery/executor-wiring-points.md`: subprocess spawn remains unlocked; latch check/trip and shared counter mutation happen under the guard; non-provider `CONTINUE` still falls through to the normal status ladder.
4. After the three failing tests pass, reconcile the task checklist carefully. Do not duplicate already-authored Step 4.6/4.7 files; mark completed items only after their current on-disk state has been validated and evidence files have been written.

## Validation/QA/test plan (paste-ready single-line commands)

Use UV only. Run from the lane root with absolute `cd` prefixes. Do not run formatting commands that modify files until after the source fix is intentional; for validation, start with checks.

- Target the three known failing tests: `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && uv run pytest tests/sprint/test_executor.py::TestPerTaskOrchestration::test_provider_exhaustion_single_429_stops_at_cap tests/sprint/test_executor.py::TestPerTaskOrchestration::test_provider_exhaustion_parallel_latch_bounds_spawn_storm tests/sprint/test_executor.py::TestPerTaskOrchestration::test_provider_exhaustion_single_worker_stops_exactly_at_small_cap -v`
- Run all P3 policy/executor tests: `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && uv run pytest tests/sprint/test_recovery_policy.py tests/sprint/test_executor.py -v`
- Preserve Phase 4 raw pytest output after the fix: `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && uv run pytest tests/sprint/test_recovery_policy.py tests/sprint/test_executor.py -v 2>&1 | tee /config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/p3-pytest.txt`
- Run format check: `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && uv run ruff format --check src/ tests/`
- Run focused lint: `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && uv run ruff check src/superclaude/cli/sprint/recovery_policy.py src/superclaude/cli/sprint/executor.py src/superclaude/cli/sprint/models.py tests/sprint/test_recovery_policy.py tests/sprint/test_executor.py`
- Run sync check: `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && make verify-sync`
- Re-run already-green P1/P2 surfaces after the P3 fix if time permits: `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && uv run pytest tests/sprint/test_monitor.py tests/sprint/test_models.py tests/sprint/test_rerun_tasks.py tests/sprint/test_resume.py tests/sprint/test_recovery_policy.py tests/sprint/test_executor.py -v`
- Inspect git status before any staging: `git -C /config/workspace/IronClaude/.dev/worktrees/SprintRun429 status --short --branch`
- Inspect diff summary before commit planning: `git -C /config/workspace/IronClaude/.dev/worktrees/SprintRun429 diff --stat`

After Phase 4 tests are green, continue the task-file gate sequence rather than skipping QA:

- Write `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/p3-summary.md` from the preserved pytest result.
- Preserve lint output to `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/p3-lint.txt` and verify-sync output to `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/p3-verify-sync.txt`.
- Complete the Phase 4 Gate steps in the task file: aggregate to `p3-aggregate.md`, run the six QA lenses, consolidate, apply exactly one serialized fix pass if needed, verify, and only then proceed to Phase 5/P4 single-session work.

## Cleanup plan (what to preserve/discard, no action taken)

No cleanup was performed by this handoff pass.

Preserve:

- All dirty source/test changes in `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/` and `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/`.
- The untracked driving spec at `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/brainstorms/sprint-429-recovery-spec.md`.
- The untracked task workspace at `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/`.
- The untracked fixtures under `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/fixtures/`.
- The untracked policy file `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/recovery_policy.py`.

Discard later only after the lane is fully validated and committed, not now:

- Generated `__pycache__` files if present under `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/`. They did not appear in `git status --short`, so they are not currently tracked work.
- Large transient grep outputs in `/config/.claude/projects/-config-workspace-IronClaude/4e25f96f-1ad2-4e59-835b-4ddf5e5e57cd/tool-results/` are session artifacts, not repo artifacts. Leave them alone unless doing a separate Claude session cleanup.

Never stage or commit `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.claude/` contents. `.claude/` is sync-dev output except `.claude/settings.json`, and this lane has no reason to stage any `.claude/` path.

## Risks/ambiguities

- The task checklist is stale relative to disk. Step 4.6/4.7 are unchecked, but `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/recovery_policy.py`, `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_recovery_policy.py`, and the provider-exhaustion tests in `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_executor.py` already exist. A blind `/task` resume may try to recreate or duplicate work unless the executor reconciles first.
- The cap semantics need careful adjudication. The TFEP context and tests treat `max_session_resets` as a total spawn cap for provider-exhaustion attempts. The current loop treats it as retry count after the first spawn. Fix the implementation to match the task/spec tests unless a fresh read of the spec conclusively says otherwise.
- The K>1 storm bound probably cannot be fixed by a local off-by-one alone. Current shared policy `_exhaustion_attempts` is unused, and the expected bound is global across workers. The fix should use shared state under the existing guard while keeping the subprocess spawn unlocked.
- The Phase 4 persistence test currently manually constructs and writes a `PhaseResult` inside the test after `execute_phase_tasks`; this proves `_write_phase_result_json` keys but may not prove the real phase aggregation path writes those keys. Check whether the task’s Step 4.5 expected real per-task derivation in executor aggregation still needs a stronger assertion or code path validation.
- Phase 5+ is not started. Remaining planned work includes single-session `PhaseStatus.PROVIDER_EXHAUSTED`, no diagnostic bundle, `aienv.py`, halt UX, `--max-session-resets` CLI/config/model chain, docs parity, execution log events, nominator exclusion, and final QA/reflect.
- Pre-PR rules are strict for this fork. If this lane reaches commit/PR closeout, run `git remote -v`, rebase onto `origin/master` if needed, push only to `origin`, and create PR with `gh pr create --repo IronbellyOrg/IronClaude --base master --head SprintRun429 ...`.

## New-session prompt

Paste-ready prompt for a new Claude agent:

Resume the SprintRun429 recovery lane in `/config/workspace/IronClaude/.dev/worktrees/SprintRun429` on branch `SprintRun429`. FIRST invoke the `sc:analyze` skill with args `/config/workspace/IronClaude/.dev/worktrees/SprintRun429 --focus quality --depth deep --format report`. Then read `/config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/01-sprint-run-429.md`, `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/TASK-RF-429-recovery-20260615-040144.md`, `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/tfep/provider-exhaustion-cap/context.yaml`, `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/executor.py`, `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/src/superclaude/cli/sprint/recovery_policy.py`, and `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/tests/sprint/test_executor.py`. Do not modify or stage `.claude/`. Fix Phase 4/P3 provider-exhaustion cap semantics so the three failing tests pass: `test_provider_exhaustion_single_429_stops_at_cap`, `test_provider_exhaustion_parallel_latch_bounds_spawn_storm`, and `test_provider_exhaustion_single_worker_stops_exactly_at_small_cap`. Preserve unlocked subprocess spawn and lock-guarded latch/shared-counter discipline. Validate with `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && uv run pytest tests/sprint/test_recovery_policy.py tests/sprint/test_executor.py -v`, `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && uv run ruff format --check src/ tests/`, `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && uv run ruff check src/superclaude/cli/sprint/recovery_policy.py src/superclaude/cli/sprint/executor.py src/superclaude/cli/sprint/models.py tests/sprint/test_recovery_policy.py tests/sprint/test_executor.py`, and `cd /config/workspace/IronClaude/.dev/worktrees/SprintRun429 && make verify-sync`. Preserve p3 outputs under `/config/workspace/IronClaude/.dev/worktrees/SprintRun429/.dev/tasks/to-do/TASK-RF-429-recovery-20260615-040144/phase-outputs/test-results/`, reconcile the task checklist only after evidence is written, then complete the Phase 4 QA gate before proceeding to Phase 5. If all remaining phases complete and tests/QA pass, perform commit/PR closeout on the fork only: run `git -C /config/workspace/IronClaude/.dev/worktrees/SprintRun429 remote -v`, ensure `origin` is `https://github.com/IronbellyOrg/IronClaude.git`, rebase onto `origin/master` if needed, never stage `.claude/`, push to `origin`, and create the PR with `gh pr create --repo IronbellyOrg/IronClaude --base master --head SprintRun429`.
