# IronClaude 6.0.0 release readiness

- Plan: IronClaude issue 571 (https://github.com/IronbellyOrg/IronClaude/issues/571)
- Orchestrator: `ic6-orchestrator`, worktree `/home/coder/workspaces/worktrees/IronClaude/ic6-orchestrator`, branch `clayphi/release-6.0.0`
- Started: 2026-11-17T19:48Z
- Decisions: `DECISIONS.md`. Step-by-step log: `PROCESS-LOG.md`.

## 1. Baseline

| Fact | Value | Evidence |
|---|---|---|
| `master` head at start | `e3e9d636a` (PR 605) | `git ls-remote --heads origin master` |
| `integration` head at start | `8c21ac41f` (the PR 570 merge), 0 commits ahead and 15 behind master | `git rev-list --left-right --count origin/master...origin/integration` |
| This branch | created at `8c21ac41f` | `git rev-parse HEAD` |
| Snapshot fork | `ironbelly/IronClaudeV5`, created 2026-11-16T17:34Z | `gh repo view ironbelly/IronClaudeV5` |
| 5.0.0 test baseline | 14610 passed, 0 failed, 136 skipped, 2 xpassed | issue 571, from issue 354 |
| Open PRs at start | none meant for this release | issue 571 (R2) |

## 2. Pull requests

State key: NOT STARTED, RUNNING (agent working), GREEN (agent stopped, checks green, not yet verified by the orchestrator), MERGED, BLOCKED.

| Wave | PR item | Branch | State | PR link | Tests before / after | Merged |
|---|---|---|---|---|---|---|
| 1 | 1: `prd` command-line pipeline (`cli/prd`) | `clayphi/v6-prd-cli` | MERGED | [#616](https://github.com/IronbellyOrg/IronClaude/pull/616) | 27914 passed, 3 failed (agent baseline) / 27687 passed, 1 failed (229 tests removed; the failure was already failing before). CI `Test on Python 3.10`: success | 2026-11-17 20:41Z, `b637fd0d8` |
| 1 | 2: cleanup-audit runner (`cli/cleanup_audit`) | `clayphi/v6-cleanup-audit-runner` | MERGED | [#615](https://github.com/IronbellyOrg/IronClaude/pull/615) | 27912 passed, 5 failed (agent baseline) / 27875 passed, 4 failed (38 tests removed; the failures are pre-existing or concurrent-run collisions, see PROCESS-LOG entry 7). CI `Test on Python 3.10`: success | 2026-11-17 20:25Z, `049dcbbf0` |
| 1 | 5: `/sc:spawn` | `clayphi/v6-spawn` | MERGED | [#617](https://github.com/IronbellyOrg/IronClaude/pull/617) | 27914 passed, 3 failed (agent baseline) / 27905 passed, 1 failed (11 tests removed; the failure was already failing before). CI `Test on Python 3.10`: success on the re-run (first run failed on the timing test `test_debit_constant_time`, unrelated) | 2026-11-17 20:49Z, `5b7d13e73` |
| 2 | 6: `/sc:save` and `/sc:load` | `clayphi/v6-save-load` | MERGED | [#620](https://github.com/IronbellyOrg/IronClaude/pull/620) | 27638 passed, 2 failed (agent baseline) / 27629 passed, 1 failed (10 tests removed; the failure was already failing before). CI `Test on Python 3.10`: success | 2026-11-17 21:38Z, `c106d7165` |
| 2 | 7: `/sc:build` | `clayphi/v6-build` | MERGED | [#622](https://github.com/IronbellyOrg/IronClaude/pull/622) | 27637 passed, 3 failed (agent baseline, machine load 25 to 100) / 27632 passed, 2 failed (6 tests removed; the failures are timing tests that pass alone). Taken before the rebase; CI `Test on Python 3.10` passed on the final head | 2026-11-17 22:16Z, `551d5ad38` |
| 2 | 10: `/sc:review-translation` (move to `ironbelly/IronClaudeV5`, then remove) | `clayphi/v6-review-translation` | MERGED | [#621](https://github.com/IronbellyOrg/IronClaude/pull/621) | 27631 passed, 9 failed (agent baseline, load-sensitive) / 27567 passed, 5 failed (68 tests removed; 4 of the 5 pass alone, the 5th is the known `test_install_keep` failure). Taken before the rebase; CI `Test on Python 3.10` passed on the rebased head. The fork `ironbelly/IronClaudeV5` holds the command and skill (checked) | 2026-11-17 21:50Z, `7dbabd045` |
| 3 | 8: `/sc:improve` (with the improve half of 506) | `clayphi/v6-improve` | MERGED | [#627](https://github.com/IronbellyOrg/IronClaude/pull/627) (`Refs` 571, 506) | 27552 passed, 4 failed (agent baseline) / 27528 passed, 1 failed (27 tests gone net; the failure was already failing before). The rebased run (27596 passed, 2 failed) was also clean. CI `Test on Python 3.10`: success. `improve` stays in the launch-level guard's list until PR 12 (see PROCESS-LOG entry 19) | 2026-11-17 23:52Z, `da12c4d76` |
| 3 | Small-fix PR A: 505, 506 (cleanup half), 510, 536, 545 | `clayphi/v6-help-text-fixes` | MERGED | [#626](https://github.com/IronbellyOrg/IronClaude/pull/626) (`Closes` 505, 506, 510, 536, 545) | 27553 passed, 3 failed (agent baseline) / 27576 passed, 1 failed (21 new tests, none removed; the failure was already failing before; each new test shown failing on the old code). CI `Test on Python 3.10`: success | 2026-11-17 22:57Z, `3e2b5dd45` |
| 3 | Small-fix PR B: 542, 543, 544 | `clayphi/v6-ic-launcher-fixes` | MERGED | [#625](https://github.com/IronbellyOrg/IronClaude/pull/625) (`Closes` 542, 543, 544) | 27553 passed, 3 failed (agent baseline) / 27596 passed, 1 failed (new tests, none removed). CI `Test on Python 3.10`: success | 2026-11-17 22:57Z, `ff52d57ab` |
| 4 | 4: cli-portify | `clayphi/v6-cli-portify` | MERGED | [#629](https://github.com/IronbellyOrg/IronClaude/pull/629) | 27598 passed, 1 failed (agent baseline) / 26702 passed, 1 failed (896 tests removed: 868 in `tests/cli_portify`, 3 `PortifyProcess` tests, 25 worker-contract and routing cases; the failure was already failing before). CI `Test on Python 3.10`: success | 2026-11-18 00:25Z, `956f49642` |
| 5 | 9: `/sc:index` and `/sc:index-repo` | `clayphi/v6-index` | MERGED | [#631](https://github.com/IronbellyOrg/IronClaude/pull/631) | 26703 passed, 0 failed (agent baseline) / 26677 passed, 3 failed (23 tests removed on purpose; the 3 failures are the known `test_install_keep` one and two load-sensitive tests that pass alone). CI `Test on Python 3.10`: success | 2026-11-18 01:22Z, `f7af90156` |
| 5 | 11: roadmap, tasklist, sprint | `clayphi/v6-roadmap-family` | MERGED | [#632](https://github.com/IronbellyOrg/IronClaude/pull/632) | 26702 passed, 1 failed (agent baseline) / 22607 passed, 1 failed (4112 tests removed, 17 added; the failure was already failing before; 605 files changed, +2487 -148187). CI `Test on Python 3.10`: success | 2026-11-18 02:05Z, `af5fb69eb` |
| 6 | 12: the retire step (new code) | `clayphi/v6-retire-step` | MERGED | [#633](https://github.com/IronbellyOrg/IronClaude/pull/633) | 22617 passed, 1 failed (agent baseline at `15d4180b7`) / 22648 passed, 1 failed (31 new tests; the failure was already failing before). CI `Test on Python 3.10`: success | 2026-11-18 03:08Z, `ccd724c6b` |
| Release | Release preparation (version, changelog, release notes) into `integration` | `clayphi/release-6.0.0` | WRITTEN 2026-11-18 03:3xZ (version 6.0.0 in `pyproject.toml`, `src/superclaude/__init__.py` and `CLAUDE.md`; `CHANGELOG.md` section `[6.0.0]`; `docs/releases/v6.0.0.md`); PR not yet open | | | |
| Release | Release PR, `integration` to `master` | `integration` | NOT STARTED | | | |

Dropped: PR 3 (swarm), by Ryan on 2026-11-17 13:06.

## 3. Ordering and dependencies

- At most 3 PRs at a time. A wave starts only when every PR of the previous wave has merged into `integration` (or is reported to Clay as blocked), after master is merged into `integration`.
- PR 11 must come after PRs 1 to 4 (it edits files they delete). PR 12 goes last (its removed-name list is generated against the `v5.0.0` tag, and PRs 4, 10 and 11 edit the same install test file).
- `cli/sprint/aienv.py` imports `swarm.config`; swarm stays, so that import goes away with sprint in PR 11.

## 4. Master merged into `integration`

| Before | Result | Time |
|---|---|---|
| Wave 1 | Merged, GitHub 201, `integration` now `c873befec` (was `8c21ac41f`) | 2026-11-17 19:49Z |
| Wave 2 | Merged, GitHub 201, `integration` now `783832f11` (was `5b7d13e73`; 5 master commits) | 2026-11-17 20:50Z |
| Wave 3 | Already up to date (GitHub 204); `integration` at `551d5ad38` | 2026-11-17 22:17Z |
| Wave 4 | Already up to date (GitHub 204); `integration` at `da12c4d76` | 2026-11-17 23:54Z |
| Wave 5 | Already up to date (GitHub 204); `integration` at `956f49642` | 2026-11-18 00:26Z |
| Wave 6 | Merged, GitHub 201, `integration` now `15d4180b7` (was `af5fb69eb`) | 2026-11-18 02:06Z |
| Release | Merged, GitHub 204 (already up to date); `integration` at `ccd724c6b` | 2026-11-18 03:16Z |

## 5. Waves reported

| Wave | Comment on issue 571 | Message to GeneralIronFlow |
|---|---|---|
| Wave 1 | https://github.com/IronbellyOrg/IronClaude/issues/571#issuecomment-6960631380 | sent 2026-11-17 20:50Z |
| Wave 2 | https://github.com/IronbellyOrg/IronClaude/issues/571#issuecomment-6962595146 | sent 2026-11-17 22:17Z |
| Wave 3 | https://github.com/IronbellyOrg/IronClaude/issues/571#issuecomment-6964532968 | sent 2026-11-17 23:54Z |
| Wave 4 | https://github.com/IronbellyOrg/IronClaude/issues/571#issuecomment-6965128936 | sent 2026-11-18 00:26Z |
| Wave 5 | https://github.com/IronbellyOrg/IronClaude/issues/571#issuecomment-6966824624 | sent 2026-11-18 02:07Z |
| Wave 6 | https://github.com/IronbellyOrg/IronClaude/issues/571#issuecomment-6967825673 | sent 2026-11-18 03:15Z |

## 6. Gate on the release PR's merge commit (G1 to G9)

Filled at the release PR. G8 is set by the plan as: (a) a search finds no file naming a removed item, except an allowlist of intentional leftovers collected from the pull request bodies (the frozen recommend-refresh record `tests/recommend/fixtures/routing_refresh_cases.json` and the lines in `tests/recommend/test_routing_refresh.py` that name removed commands, `cleanup-audit` in the kept skill, command and agents, and the `sprint`, `roadmap` and `tasklist` words in `.gitignore`, the reflect promotion adapter and `sc-crash-recovery/scripts/bootstrap_scan.sh`); (b) 0 test failures, as the plan sets it (not relaxed here). One test is known to fail on fast machines in the agents' runs and in the orchestrator's: `tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files` (it writes a file, changes it and compares again within one filesystem timestamp tick, and `filecmp.cmp` caches by size and modification time; GitHub's runners pass it). If it fails in the gate run, the result is recorded as a failed check and goes to Clay for a decision, not excused here. The test count is checked against a baseline measured on `integration` at `ccd724c6b`, the last pull request of the cleanup. With the command of the CI `test` job (`pytest -n auto --ignore=tests/cli/test_verify_sync_hooks.py`, no `--maxfail`), passed plus failed equals 22649, with 70 skipped as before (22648 passed and 1 failed in the retire-step agent's run; a fully passing run shows 22649 passed). The release preparation adds and removes no test, so the gate run must show the same total plus the tests of any `master` commits merged into `integration` after `ccd724c6b`, which the gate record lists. A plain `make test` also runs the 7 tests of `tests/cli/test_verify_sync_hooks.py`, so its total is higher by those. The plan's 14610 is the 5.0.0 figure and is superseded: the suite had grown to about 27,900 passing tests before the removals (14610 stays recorded here as the 5.0.0 reference; the per-pull-request removal and addition counts are in section 2); (d) upgrading an existing 5.0.0 workspace leaves no removed command, skill or agent installed and `/sc:help` lists only what exists. (c) and (e) are dropped.

| Check | Result | Evidence |
|---|---|---|
| G1 fork target | | |
| G2 CI on the exact commit | | |
| G3 version consistency | | |
| G4 changelog cut | | |
| G5 full local suite and gates | | |
| G6 package builds | | |
| G7 upgrade path | | |
| G8 (a), (b), (d) | | |
| G9 no open PR meant for this release | | |

## 7. Finished worktrees (for Clay to remove later)

The orchestrator deletes no worktree. Finished, for Clay to remove later (`orca worktree rm --worktree name:<name>`):

| Worktree | Path | PR |
|---|---|---|
| `v6-prd-cli` | `/home/coder/workspaces/worktrees/IronClaude/v6-prd-cli` | #616 |
| `v6-cleanup-audit-runner` | `/home/coder/workspaces/worktrees/IronClaude/v6-cleanup-audit-runner` | #615 |
| `v6-spawn` | `/home/coder/workspaces/worktrees/IronClaude/v6-spawn` | #617 |
| `v6-save-load` | `/home/coder/workspaces/worktrees/IronClaude/v6-save-load` | #620 |
| `v6-review-translation` | `/home/coder/workspaces/worktrees/IronClaude/v6-review-translation` | #621 |
| `v6-build` | `/home/coder/workspaces/worktrees/IronClaude/v6-build` | #622 |
| `v6-help-text-fixes` | `/home/coder/workspaces/worktrees/IronClaude/v6-help-text-fixes` | #626 |
| `v6-ic-launcher-fixes` | `/home/coder/workspaces/worktrees/IronClaude/v6-ic-launcher-fixes` | #625 |
| `v6-improve` | `/home/coder/workspaces/worktrees/IronClaude/v6-improve` | #627 |
| `v6-cli-portify` | `/home/coder/workspaces/worktrees/IronClaude/v6-cli-portify` | #629 |
| `v6-index` | `/home/coder/workspaces/worktrees/IronClaude/v6-index` | #631 |
| `v6-roadmap-family` | `/home/coder/workspaces/worktrees/IronClaude/v6-roadmap-family` | #632 |
| `v6-retire-step` | `/home/coder/workspaces/worktrees/IronClaude/v6-retire-step` | #633 |
