# Reviewer 3 brief: refactorer lens (model class: opus)

Mode: UC-1 pre-execution. You audit a PROPOSED plan (tasklist) against its driving spec, read-only. Do not run commands. Return findings only.

Spec: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/source.md
Tasklist under review (read in full): /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-revisedPlanRefac-20261102-213941/TASK-WF-revisedPlanRefac-20261102-213941.md

Your lens: structure and execution risk. Check that every path, anchor, command and flag the plan names exists and is correct for this repository; that the scripts/eval_runner.py rewrite (Task 2) is complete (every use of the old checkout path, the E2E global block, the error path) and its test can really fail before and pass after; that task order and dependencies are safe; that mirrors stay consistent; and that no search, count or acceptance criterion can pass while the requirement fails. Classify each divergence under the 4-category taxonomy with a one-line rationale and a file:line citation.

## T1 card excerpt

Verbatim from /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/reflect/pre-revisedPlanRefac-20261102214256/t1-card.md, section "Structural / tech-debt section (refactorer lens)":

- S1: Task 2's design is executable. Verified 2026-11-02 in a throwaway repo under /tmp: `git worktree add --detach <empty mktemp -d dir> master` exits 0, and `git worktree remove --force <dir>` exits 0 and deletes the directory. scripts/eval_runner.py:136-162 (`run_global`) and :287-300 (`main`'s global block, which reuses `REPO_ROOT.parent / "IronClaude-eval-master"` at :294) are the two places Task 2 must change; the plan names both.
- S2: Task 8's zero-skip rule is achievable on this host: the only skip markers in its test files are tests/troubleshoot/backtest/test_git_replay_integration.py:56-68 and tests/skills/test_implement_retry_revert.py:357. All five pinned parents (git_replay.py:52-58) are present locally, `git rev-parse --is-shallow-repository` prints `false`, and `id -u` prints 1000. In CI the module would skip, which the plan handles with the recorded-reason-and-rerun clause.
- S3: Task 4's acceptance check "saved as ./artifacts/t4-gh-lines.txt from `grep -n 'gh ' CLAUDE.md`" matches words such as "through " and "high " across the whole file, so the artifact is noisy and the criterion still needs judgment for the section. Low.
- S4: The superseded plan's package (.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/) is still under to-do; nothing archives or marks it. Low.
- S5: Mirror discipline unchanged and correct: Task 7 copies the three sc-recommend files, runs `make sync-dev` before `make verify-sync`, and adds tests/skills/test_sc_recommend_routing_contract.py (D-011). sc-post-release-protocol has no plugin copy.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-02T21:43Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths projectPath=/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths

### scripts/eval_runner.py:287-300

```python
    if args.mode in ("global", "full"):
        print("Running global eval A...")
        runs.append(run_global("A"))
        print("Running global eval B...")
        runs.append(run_global("B"))

        # E2E pipeline evals (global branch)
        worktree_path = REPO_ROOT.parent / "IronClaude-eval-master"
        if worktree_path.exists():
            for script in E2E_SCRIPTS:
                script_path = worktree_path / script
                if script_path.exists():
                    print(f"Running E2E {script} (global)...")
                    e2e_runs.append(run_e2e_script(script, "global", worktree_path))
```

### tests/swarm/test_bare_review_golden_regen.py:153

```python
    spec = importlib.util.spec_from_file_location(
```

## Coverage slice

| Requirement | Matched task | Status | Grounding |
|---|---|---|---|
| D-001 eval_runner rewrite + regression test | Task 2 | covered | source.md:1; scripts/eval_runner.py:136-147, :287-300 |
| D-003 Search B totals | Task 1 | covered | source.md:1 |
| D-011 contract test | Task 7 | covered | source.md:1 |
| INF-010 never stage .claude mirrors | none lexically | content-level covered | plan Constraints |
