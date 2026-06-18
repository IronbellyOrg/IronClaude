# SprintReRun stale handoff

## Current state

Target lane: `/config/workspace/IronClaude/.claude/worktrees/SprintReRun`.

Git state observed on 2026-06-17:

- Branch: `feat/sprint-auto-resume-v435`.
- Upstream tracking ref: `origin/feat/sprint-auto-resume-v435` is gone.
- Source tree: no tracked source modifications in `git status --short`; dirty state is three untracked artifact roots only.
- Recent local commits are from 2026-06-03, ending at `aedd0104 style(sprint): ruff format src/ tests/ to clear CI format check (PR #124)`. The same five local branch commits are ahead of both `master` and `origin/master` in this worktree.
- Remote safety: `origin` is `https://github.com/IronbellyOrg/IronClaude.git`.

Dirty artifact roots:

- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/releases/current/`
- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/tasks/done/TASK-SIDECAR-GAP-20260602/`
- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/reflect/post-sprint-rerun-v430-20260602/`

No source modifications were made during this handoff. No artifacts were deleted.

## Artifact inventory

### `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/releases/current/`

Observed contents are limited to three checkpoint reports under `cliEval/checkpoints/`:

- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/releases/current/cliEval/checkpoints/CP-P04-T07-T11.md` — 17,925 bytes, mtime 2026-06-02 06:39. Phase 4 mid-checkpoint for T04.07-T04.11, `status: FAIL`. It reports three blockers: missing `tests/cli/eval/test_eval_run.py`, Click 8.3.2 `CliRunner(mix_stderr=False)` failure, and missing evidence/artifact triplets for T04.08-T04.10.
- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/releases/current/cliEval/checkpoints/CP-P04-T13-T17.md` — 18,192 bytes, mtime 2026-06-02 06:39. Phase 4 mid-checkpoint for T04.13-T04.17, `status: PASS`, with non-blocking T04.16 documentation gaps rolled forward.
- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/releases/current/cliEval/checkpoints/CP-P04-END.md` — 31,320 bytes, mtime 2026-06-02 06:39. Phase 4 / M4 exit gate for T04.01-T04.21, `status: FAIL`. It says M4 is mostly landed but blocked by `uv run pytest tests/cli/eval/ -v` failing, `src/superclaude/cli/eval/commands.py` ruff/F821 undefined-symbol errors, one Click test idiom failure, missing `tests/cli/eval/test_eval_run.py`, and missing D-0070/D-0071/D-0072/D-0077 plus evidence directories.

Important quality note: this `current/cliEval` tree is incomplete. The only files present under the untracked root are the three checkpoint markdown files. Referenced phase tasklists, `evidence/`, `artifacts/`, `decisions.md`, and logs are not present in this untracked root. Treat these as copied/stale checkpoint snapshots, not a restorable full cliEval release workspace.

### `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/tasks/done/TASK-SIDECAR-GAP-20260602/`

Observed files:

- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/tasks/done/TASK-SIDECAR-GAP-20260602/SPEC.md` — 3,208 bytes, mtime 2026-06-02 17:48. Driving spec for the rerun-tasks sidecar gap. It defines AC-1 through AC-5 for writing `<bundle>/results/task-results.json` before `merge_recovery_bundle` so canonical per-task status refreshes after successful rerun.
- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/tasks/done/TASK-SIDECAR-GAP-20260602/reflect-pre-report.md` — 3,752 bytes, mtime 2026-06-02 17:51. Pre-execution reflect report, PASS, 5/5 AC mapping, two low hardening findings folded into the tasklist.
- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/tasks/done/TASK-SIDECAR-GAP-20260602/reflect-post-report.md` — 3,771 bytes, mtime 2026-06-02 18:06. Post-execution reflect report, PASS/status success, AC-1 through AC-5 satisfied, 0 Drift, 0 Regression, promotion suppressed.
- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/tasks/done/TASK-SIDECAR-GAP-20260602/TASK-SIDECAR-GAP-20260602.md` — 8,289 bytes, mtime 2026-06-02 18:08. MDTM task marked Done. Execution log says the sidecar writer was added in `run_rerun_tasks`, tests were added/strengthened, 39 affected sprint tests passed, and `/sc:reflect --post` passed.

This task folder is coherent and self-contained. It records a completed corrective task with spec, pre/post reflection, and test evidence summaries.

### `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/reflect/post-sprint-rerun-v430-20260602/`

Observed file:

- `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/reflect/post-sprint-rerun-v430-20260602/REPORT.md` — 5,251 bytes, mtime 2026-06-02 06:08. Post-execution deviation audit for v4.3.0 `sprint rerun-tasks`, Phases 1-3. Verdict is PASS/status success with 0 regressions and 0 drift. It explicitly says this was a partial task: Phases 1-3 complete, Phases 4-6 still remained at the time. It recommended no refactor, clear to commit/push, with pre-existing test failures tracked separately.

This reflect report is useful historical evidence for the earlier v4.3.0 granular rerun work, but it is older than the branch’s v4.3.5 auto-resume commits from 2026-06-03.

### Session logs and checkpoint reports

- Checkpoint reports found in the target dirty roots are the three `CP-P04-*.md` files listed above.
- No `execution-log.md`, `execution-log.jsonl`, `.sprint-exitcode`, or `*.log` files were found inside the three target untracked roots.
- A broader shallow worktree search found many `.dev/sprint-state/**/.sprint-exitcode` files with mtimes on 2026-06-02 and 2026-06-03, mostly test fixture state. They are outside the dirty roots reported by git status and were not inspected as preservation candidates for this stale-lane handoff.

## Preserve/delete/archive decision criteria

Recommended handling by artifact group:

| Artifact group | Recommendation | Rationale |
|---|---|---|
| `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/tasks/done/TASK-SIDECAR-GAP-20260602/` | Preserve or archive intact | Completed Done/PASS evidence for a real sprint rerun sidecar fix. It is coherent and self-contained. Do not delete before confirming the corresponding code/test changes are already committed in the intended branch or PR history. |
| `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/reflect/post-sprint-rerun-v430-20260602/` | Preserve or archive with the rerun work history | Useful historical reflect evidence for v4.3.0 rerun-tasks phases 1-3. Because it says the task was partial at that time, do not treat it as current completion evidence for v4.3.5. |
| `/config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/releases/current/cliEval/checkpoints/` | Archive as stale cliEval checkpoint snapshots, or delete after external preservation | These are unrelated to the SprintReRun branch focus and incomplete as a release workspace. Preserve only if the cliEval Phase 4 failure analysis has not been captured elsewhere. If already captured in the cliEval lane’s handoff or committed artifact history, this root is a cleanup candidate. |

Decision criteria before cleanup:

1. Preserve any artifact that is the only local evidence for a completed task, reflect verdict, or checkpoint failure diagnosis.
2. Archive rather than delete if an artifact names unresolved blockers or would help reconstruct a crash/resume state.
3. Delete only after confirming the same evidence exists in a committed branch, a PR, or the crash-recovery handoff set under `/config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/`.
4. Treat incomplete `current/` release roots as suspicious. If the release root lacks tasklists, evidence directories, execution logs, and artifacts, it is not a safe resume target.
5. Never stage `.claude/` generated mirror content. These artifacts are under a `.claude/worktrees/` worktree path but are worktree files; still avoid any forced staging of `.claude/*` paths unless the user explicitly authorizes it.

## Validation commands

Run these from a new session to re-check the handoff without mutating source:

- `git -C /config/workspace/IronClaude/.claude/worktrees/SprintReRun status --short --branch`
- `git -C /config/workspace/IronClaude/.claude/worktrees/SprintReRun log -n 5 --date=short --format='%h %ad %s'`
- `find /config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/releases/current /config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/tasks/done/TASK-SIDECAR-GAP-20260602 /config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/reflect/post-sprint-rerun-v430-20260602 -maxdepth 4 -type f -printf '%TY-%Tm-%Td %TH:%TM %s %p\n' | sort`
- `find /config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/releases/current -maxdepth 8 -type f -printf '%P %s bytes\n' | sort`
- `git -C /config/workspace/IronClaude/.claude/worktrees/SprintReRun ls-files .dev/releases/current .dev/tasks/done/TASK-SIDECAR-GAP-20260602 .dev/reflect/post-sprint-rerun-v430-20260602 --error-unmatch 2>/dev/null || true`

Optional validation if deciding whether the sidecar-gap task evidence is already safe to archive:

- `grep -R "task-results.json\|test_merge_refreshes_canonical_status_from_sidecar\|test_merge_without_sidecar_preserves_prior_and_partials" -n /config/workspace/IronClaude/.claude/worktrees/SprintReRun/src/superclaude/cli/sprint /config/workspace/IronClaude/.claude/worktrees/SprintReRun/tests/sprint`
- `cd /config/workspace/IronClaude/.claude/worktrees/SprintReRun && uv run pytest tests/sprint/e2e_real/ tests/sprint/test_recovery.py tests/sprint/test_rerun_tasks.py tests/sprint/test_rerun_tasks_e2e.py tests/sprint/test_rerun_tasks_failure_modes.py -q`

## Risks

- The local branch tracks a gone remote branch. Before any push/PR work, re-establish the intended remote branch strategy and follow the repository rule to target `IronbellyOrg/IronClaude`, not upstream.
- The `current/cliEval` artifact root is incomplete. Attempting to resume or validate cliEval from this root would be misleading because only checkpoint reports are present.
- The v4.3.0 reflect report predates later v4.3.5 commits. It is historical support, not a current validation of HEAD.
- The Done task folder says promotion was suppressed, so it may intentionally remain untracked even though marked Done. Cleanup should not assume untracked equals disposable.
- Running the optional pytest validation can be non-trivial and may surface unrelated pre-existing failures. Use it only when deciding whether to archive/delete evidence, not as a prerequisite for reading the stale artifacts.

## New-session prompt

Paste this into a new Claude Code session if follow-up cleanup/archive is needed:

`Review stale SprintReRun artifacts in /config/workspace/IronClaude/.claude/worktrees/SprintReRun on branch feat/sprint-auto-resume-v435 using /config/workspace/IronClaude/.dev/research/crash-recovery-handoffs-20260617/10-sprint-rerun-stale.md as the handoff; do not delete anything until you verify git status, confirm whether TASK-SIDECAR-GAP-20260602 and post-sprint-rerun-v430-20260602 are preserved elsewhere, and classify /config/workspace/IronClaude/.claude/worktrees/SprintReRun/.dev/releases/current/cliEval/checkpoints as archive or cleanup based on whether cliEval Phase 4 failure evidence exists in another lane.`
