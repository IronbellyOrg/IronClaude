# Issue 450 review

## Verdict and evidence

**Verdict: close** (as a rollout tracker). The issue asks for four things, and each is either done by a different mechanism or no longer the gate.

1. Live test with captured replies and `docs/designs/issue-watcher-live-test.md` (FU-1): the record was never written and the 20 fixtures under `tests/issue_watch/fixtures/_assumed_shape/` were never replaced. But the watcher has since run for real: `~/.local/state/superclaude/issue-watch/IronClaude/audit.jsonl` shows 284 real (not dry-run) cycles from 2026-11-23T21:56:04Z, including two `launch_unknown` outcomes (2026-11-23T22:12:11Z for issue 597, 2026-11-23T22:13:13Z for issue 751) followed by `claimed` for both (22:28:06Z and 22:19:10Z). The live evidence the test was meant to produce now exists in the audit log.
2. Reviewed 24-hour shadow run, lock test, restart test, then `enabled: true`: superseded by the automatic first-run check. `first_run` (`src/superclaude/cli/issue_watch/first_run.py:125`) runs config, label, state, dry run, a lock test expecting exit 75 (`first_run.py:227-235`) and a restart test (`first_run.py:237-253`), and only then rewrites the config to enabled (`first_run.py:152-153`). `~/.config/superclaude/issue-watch.d/IronClaude.json` has `"enabled": true`.
3. Cron entry (FU-2): installed. `crontab -l` shows `* * * * * /usr/bin/flock -n /home/coder/.aidev/issue-watch.lock /usr/local/bin/superclaude issue-watch run-all ...`, managed and rewritten on every boot. The schedule is one minute, not the six-field `0 */5 * * * *` the issue names (`docs/designs/issue-watcher-setup.md:281`).
4. Doc drift: fixed by PR #485 (`91375feb1`), then made stale again by the zero-setup work. `docs/designs/issue-watcher.md:3` still says "never run live; enabled ships as false; no schedule is installed". The reason table now matches: the runbook states 59 names (`docs/designs/issue-watcher-setup.md:345`).

The remaining gap (assumed fixtures, missing live-test record, the stale status line) is documentation and test-fixture hygiene, not the rollout the issue tracks. Issue #717 already carries the fixture and live-test follow-ups (its items W4, W10, W11, W15).
## Real current state

The watcher is live on this host and polling every minute.

- Three repositories run with `enabled: true`: IronClaude (284 real cycles, 280 exit 0, 2 exit 6 `lock_missing`, 2 exit 7 `launch_unknown`), Coder (314 real cycles, all exit 0) and IronOrca (313 real cycles, all exit 0), counted from each repository's `audit.jsonl` under `~/.local/state/superclaude/issue-watch/`.
- IronClaude's latest cycle (2026-11-24T02:39:09Z) ended `cycle_complete` with exit 0 after 10 GitHub calls, and decided: issue 597 `already_dispatched`, issue 695 `approval_before_trigger`, issue 703 `level_gated`, issue 751 `already_dispatched`.
- The ship gate is closed: `GOVERNED_LEVELS_ALLOWED = False` (`src/superclaude/cli/issue_watch/launch.py:48`), enforced in `_examine` (`src/superclaude/cli/issue_watch/cycle.py:1031-1036`), so only a Pipeline value of None launches. Issue 703 is skipped for exactly this reason on every cycle.
- The Coordinator worktrees exist at `/home/coder/workspaces/worktrees/IronClaude/Coordinator` and `/home/coder/workspaces/worktrees/Coder/Coordinator`.
- Not done: `docs/designs/issue-watcher-live-test.md` does not exist, and no commit has touched `tests/issue_watch/fixtures/_assumed_shape/` (the capture sheet at `docs/designs/issue-watcher-setup.md:588-616` is unfilled).
- Anomaly: `~/.local/state/superclaude/issue-watch/IronClaude/first-run.txt` reads `first-run: failed config: worktree_invalid`, yet the config is enabled and cycles succeed. The order of those events is UNVERIFIED.
## Concrete next steps

The tracker itself needs no build. The leftovers, if kept, are:

1. Rewrite the status line at `docs/designs/issue-watcher.md:3` so it no longer says the watcher has never run live.
2. Reconcile the contradiction inside `docs/designs/issue-watcher-setup.md`: section 14.1 (`:581`) forbids enabling before the live test, while section 17 (`:706`) enables on a passing first-run check.
3. Fill the capture sheet (`docs/designs/issue-watcher-setup.md:588-616`) from the replies the live run already produces, starting with the two `launch_unknown` outcomes, and replace the 20 assumed fixtures. This is the substance of issue #717 items W10 and W11, so it belongs there rather than here.

## Complexity and size

**Simple, S.** What remains is a status-line edit, a runbook reconciliation and a fixture swap from replies that already exist; no new mechanism is needed because `first_run` and `run-all` already perform the rollout.
## Priority

**P3.** The rollout is already in effect, so nothing is blocked on this issue. The one real risk it still names, the guessed reply shapes, is contained: the ship gate limits launches to Pipeline None, and issue #717 tracks the fixture replacement.

## Dependencies

- Needs: nothing. The parent issue #331 is closed and its code is merged (PR #447, commit `4c93b6c73`; fixes in PR #448, commit `ce6608258`).
- Blocks: nothing. The ship gate that holds back governed launches is `GOVERNED_LEVELS_ALLOWED` in `src/superclaude/cli/issue_watch/launch.py:48`, which the design ties to issue #442's checks (`docs/designs/issue-watcher.md`, section 19.6), not to this issue.
## Related issues

- #331 (closed): the watcher itself, which this issue follows up.
- #717 (open): the watcher's uncovered features, including the live-firing tests (W5), the shadow-run check (W6), the launched-session permission record (W10), the unknown-launch retry (W11) and the runbook rewrite after the live test (W15). This is where the leftovers belong.
- #716 and #718 (open): the coordinator and dashboard sisters of the same split.
- #442: the guard checks the design says must pass before a governed claim runs on a real issue.
- #651: the templates proposal in clayphi's comment of 2026-11-18 (https://github.com/IronbellyOrg/IronClaude/issues/450#issuecomment-6985547377).
- IronbellyOrg/PrivateRepoF #515 and #516: the cron entry and the coordinator session the zero-setup handoff names (`docs/designs/issue-watcher-zero-setup-coder-handoff.md:10-13`).

## Related PRs

- #447 (`4c93b6c73`) and #448 (`ce6608258`): built the watcher.
- #451 (`git show` not re-read this turn): recorded the brainstorm and the worker report the pick-up note cites. UNVERIFIED beyond the issue comment.
- #485 (`91375feb1`): the doc-drift fixes and the rollout checklist.
- #548 (`d4d1662a8`): recorded the owner's option 3, the claim level.
- #591 (`6af80d6c0`): the coordinator handoff.
- #707 (`2ea524514`): the zero-setup watcher, per-status launch levels, the Approved field and guard version 2, which is the change that made this issue's rollout steps automatic.
## Verification limits and negative evidence

- The GitHub search for pull requests mentioning 450 returned only #485 and #451 before the shared rate limit was exhausted (`gh api rate_limit` was not retried). PR numbers #548, #591 and #707 come from `git log` on this worktree, which is at `a7ae3dd30`, 0 commits ahead of and 0 behind its upstream at the start of the session. Whether any later pull request mentions the issue is UNVERIFIED.
- #584, cited by the 2026-11-17 status comment as the claim-handoff test on throwaway issue 452, was not re-fetched. The absence of `docs/designs/issue-watcher-live-test.md` was confirmed locally.
- The audit logs, the crontab and the config files are state on this one host (`509de1b51957`, the `host` field of the audit lines). Whether other hosts run the watcher is UNVERIFIED.
- The installed cron schedule is one minute, not the five minutes the design specifies. The handoff document shows a five-minute line (`docs/designs/issue-watcher-zero-setup-coder-handoff.md:23`); the crontab on this host does not match it. Who changed it is UNVERIFIED.
- No test suite was run, so the issue's "2655 tests" figure stays unchecked, as the earlier accuracy comment also left it.
- The timeline events of the issue beyond its four comments were not read separately; the comments are the record used here.
