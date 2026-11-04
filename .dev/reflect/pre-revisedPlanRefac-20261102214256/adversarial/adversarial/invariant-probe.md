# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis
<!-- Fault-finder: read-only general-purpose agent (opus), independent of all advocates. Returned at ~22:39Z; persisted by the orchestrator. No branch-trace.md exists; category 6 uses inline source enumeration. -->
<!-- Orchestrator verification 22:40Z: INV-009 confirmed (`git worktree list` has no /.dev/worktrees/ line; /home/coder/workspaces/IronClaude/.dev/worktrees/* does not exist; plan:27 still lists both). INV-001 confirmed (eval_runner.py:35-43 RESULTS_DIR fixed at import; :307-309 mkdir + write; `git check-ignore` exit 1 for .dev/releases/current/x and eval-results/x). INV-013 confirmed (eval_1.py:456-459 default output `eval-results/...` relative to cwd; eval_runner.py:300 runs E2E with the checkout as cwd). -->

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | Patching `REPO_ROOT` keeps the `main()` test out of the real checkout | UNADDRESSED | MEDIUM | eval_runner.py:35-43 fixes `RESULTS_DIR` at import from the real repo; :307-309 mkdir and write `eval-report.json`; not ignored (check-ignore exit 1); plan:20 forbids edits under `.dev/` outside the package; plan:178 `git diff --stat` misses untracked files |
| INV-002 | state_variables | `master_checkout()` reads `REPO_ROOT` at call time | ADDRESSED | LOW | plan:62 `cwd=REPO_ROOT`; no-master test (plan:70) fails loudly if bound early; plan should say `git worktree list` runs in the throwaway repo |
| INV-003 | guard_conditions | The mkdtemp dir still exists after every failed `git worktree add` | UNADDRESSED | LOW | t1-shell-evidence.txt:29-30 tested remove on an unregistered dir, not post-add state; plain `os.rmdir` could raise `FileNotFoundError` past a narrow catch [INFERRED] |
| INV-004 | guard_conditions | Teardown `git worktree remove --force` cannot hide the body's exception | UNADDRESSED | MEDIUM | plan:62 silent on teardown failure; tests/troubleshoot/backtest/git_replay.py:199-205 wraps each teardown call separately; consensus dropped V1's non-masking point |
| INV-005 | guard_conditions | A test can call `main()` and inspect the result directly | UNADDRESSED | LOW | eval_runner.py:267-269 parses `sys.argv` (pytest args -> exit 2 unless patched); `main()` returns nothing (:266-314) |
| INV-006 | count_divergence | plan:74 "the same tests fail against the pre-change script" holds for added tests | UNADDRESSED | MEDIUM | An exit-code characterization test (eval_runner.py:313) passes before the change too; pre-change `run_global` ignores the add failure (:142-147) |
| INV-007 | count_divergence | Every file left in the Task 8 residual searches was classified in Task 1 | UNADDRESSED | LOW | New test file created in Task 2; plan:46 reclassifies only in Task 1; plan:177 requires a class (= R3-F6) |
| INV-008 | count_divergence | Search A/B baselines still valid | ADDRESSED | LOW | Live rerun 22:36Z: Search A 108/17, Search B 9/7; all files listed at plan:40-42 |
| INV-009 | collection_boundaries | The two retired-location checkouts still exist (plan:27) | UNADDRESSED | LOW | Orchestrator-confirmed 22:40Z: no `/.dev/worktrees/` line in `git worktree list`, directory absent; plan:44 section will be empty, plan:51 passes vacuously, plan:90 describes checkouts that no longer exist |
| INV-010 | collection_boundaries | The throwaway-repo tests run the body of `with master_checkout()` | UNADDRESSED | MEDIUM | Fixture (plan:67) has none of EVAL_FILES (eval_runner.py:21-27) or E2E_SCRIPTS (:29-33); `run_global` returns early (:150-156); E2E loop skips every script (:297-298); all 8 files exist on real `master` |
| INV-011 | collection_boundaries | "No SKIPPED line" (plan:176) is not satisfied by deselection | ADDRESSED | LOW | pyproject.toml:112-116 addopts has no `-m`; skip guards at test_git_replay_integration.py:56-68 and test_implement_retry_revert.py:357 inactive on this host |
| INV-012 | interaction_effects | Task 3's Orca-only rule fits Task 4's absolute ban | UNADDRESSED | MEDIUM | plan:86 requires `orca worktree create`; plan:105 bans any tool call (Orca included) "that resolves to" upstream; plan:111 records Orca's project id `github:superclaude-org/superclaude_framework`; read literally Task 4 forbids Task 3's path |
| INV-013 | interaction_effects | `--force` removal loses nothing the old checkout kept | UNADDRESSED | MEDIUM | E2E scripts run with the checkout as cwd (eval_runner.py:300) and write `eval-results/...` relative to it (eval_1.py:456-459; eval_2.py, eval_3.py on master per probe); not ignored; `RunResult` keeps only `stderr[-500:]` (eval_runner.py:118); removal deletes the outputs |
| INV-014 | sufficiency_challenge | Fixes (a)-(e) make the `main()` global-setup assertion runnable and side-effect free | UNADDRESSED | MEDIUM | Gate chain: patch REPO_ROOT (plan:67) -> argv parse (eval_runner.py:267-269, INV-005) -> MasterCheckoutError -> `global-setup` counted as global by name (:175, :204-206, :219-223) -> print (:234-240) -> JSON to import-time RESULTS_DIR (:36-43, :307-309, INV-001) -> exit (:313). No step exercises teardown after real work (INV-010, INV-013) |
| INV-015 | sufficiency_challenge | `git init -b master` plus identity isolates the tests' git calls | UNADDRESSED | LOW | Repo convention strips `GIT_*` and sets `GIT_CONFIG_GLOBAL=/dev/null` (tests/skills/test_implement_retry_revert.py:31-36, :173-180) |

## Summary

- **Total findings**: 15
- **ADDRESSED**: 3 (INV-002, INV-008, INV-011)
- **UNADDRESSED**: 12
  - HIGH: 0
  - MEDIUM: 7 (INV-001, INV-004, INV-006, INV-010, INV-012, INV-013, INV-014)
  - LOW: 5 (INV-003, INV-005, INV-007, INV-009, INV-015)

Gate: no HIGH UNADDRESSED items, so the invariant gate does not block convergence. WARNING: 7 MEDIUM UNADDRESSED invariant(s): INV-001, INV-004, INV-006, INV-010, INV-012, INV-013, INV-014. These are carried into the merged findings.
