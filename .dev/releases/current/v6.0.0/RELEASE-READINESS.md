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
| 2 | 7: `/sc:build` | `clayphi/v6-build` | RUNNING (agent started 2026-11-17 20:51Z) | | | |
| 2 | 10: `/sc:review-translation` (move to `ironbelly/IronClaudeV5`, then remove) | `clayphi/v6-review-translation` | RUNNING (agent started 2026-11-17 20:51Z) | | | |
| 3 | 8: `/sc:improve` (with the improve half of 506) | `clayphi/v6-improve` | NOT STARTED | | | |
| 3 | Small-fix PR A: 505, 506 (cleanup half), 510, 536, 545 | `clayphi/v6-help-text-fixes` | NOT STARTED | | | |
| 3 | Small-fix PR B: 542, 543, 544 | `clayphi/v6-ic-launcher-fixes` | NOT STARTED | | | |
| 4 | 4: cli-portify | `clayphi/v6-cli-portify` | NOT STARTED | | | |
| 5 | 9: `/sc:index` and `/sc:index-repo` | `clayphi/v6-index` | NOT STARTED | | | |
| 5 | 11: roadmap, tasklist, sprint | `clayphi/v6-roadmap-family` | NOT STARTED | | | |
| 6 | 12: the retire step (new code) | `clayphi/v6-retire-step` | NOT STARTED | | | |
| Release | Release preparation (version, changelog, release notes) into `integration` | `clayphi/release-6.0.0` | NOT STARTED | | | |
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

## 5. Waves reported

| Wave | Comment on issue 571 | Message to GeneralIronFlow |
|---|---|---|
| Wave 1 | https://github.com/IronbellyOrg/IronClaude/issues/571#issuecomment-6960631380 | sent 2026-11-17 20:50Z |

## 6. Gate on the release PR's merge commit (G1 to G9)

Filled at the release PR. G8 is set by the plan as: (a) a search finds no file naming a removed item; (b) 0 test failures and the pass count equals 14610 minus the removed tests; (d) upgrading an existing 5.0.0 workspace leaves no removed command, skill or agent installed and `/sc:help` lists only what exists. (c) and (e) are dropped.

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
