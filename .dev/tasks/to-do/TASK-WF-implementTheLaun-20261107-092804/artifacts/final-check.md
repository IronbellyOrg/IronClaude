# Final check (Task 22, issue #394)

Run on 2026-11-07 in the worktree `issue-394-launch-level-hook`, after the Task 22 document edits.

## Commands run

| Command | Exit code | Result |
|---|---|---|
| `make sync-dev` | 0 | mirrors regenerated (generated `.claude/` copies stay out of any commit) |
| `make verify-sync` | 0 | "All components in sync." |
| `make lint` | 0 | architecture policy: PASS with 5 warnings (pre-existing); `uv run ruff check .`: "All checks passed!" |
| `uv run pytest tests/hooks/ tests/cli/test_install_hooks.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py tests/skills/test_worker_contract.py -v -rs` | 0 | **5093 passed, 12 skipped** in 398.71 s (log: `/tmp/impl-20261107/t22-full.log`) |
| `uv run pytest tests/commands/test_issue_command.py tests/cli/test_issue_body_templates.py tests/skills/test_issue_worker_agents.py -q` | 0 | 93 passed (other tests that read the edited `issue.md`) |
| `cmp src/superclaude/hooks/scripts/launch-level-guard.sh plugins/superclaude/hooks/scripts/launch-level-guard.sh` | 0 | identical; the src script was not changed in Task 22, so it was not re-copied |
| `grep -c 'does not implement this proposed pipeline interface' docs/designs/sc-issue-launch-level-hook.md` | 1 (no match) | count 0 |

Doc fix pass after the Task 22 review (F1-F4, F6; documents only): re-ran `make sync-dev`, `make verify-sync`, `make lint` (all exit 0), the `enforcement_status` and removed-phrase greps (no match in docs/, src/, tests/), and `uv run pytest` on tests/skills/test_issue_protocol.py, test_worker_contract.py, test_issue_orca_worktree.py, tests/hooks/, tests/pr_submit/test_conflict_sync_protocol.py, test_merge_guard_protocol.py, tests/swarm/test_e2e_user_guide.py, tests/skills/test_workflow_archive.py, tests/audit/test_profiler.py, tests/docs: 5129 passed, 12 skipped, 1 failed (T-SPD-5 `backslash-lines-64KB`, max 1230.6 ms, the timing flake of limit 10); `test_speed_large_commands` re-run alone: 4 passed.

## Skips (12)

Every skip is a pending live observation of `tests/hooks/test_launch_level_observations.py:84`, reason "needs a real governed session and has not been run":

| Skipped test | Reason class |
|---|---|
| OB-H1 item 1 to OB-H1 item 9 (9 tests) | pending observation |
| OB-H2 | pending observation |
| OB-H3 | pending observation |
| OB-CTX | pending observation |

No other skip occurred. The hook-order observation of Task 14 did not skip (its file runs on Linux; the open hook-order question is recorded in `hook-order.md` and belongs to OB-H3). The environment skips (non-Linux, running as root, the opt-in live probe) did not fire on this Linux, non-root host.

## Pending observations (none has been run)

OB-H1 items 1, 2, 3, 4, 5, 6, 7, 8 and 9; OB-H2; OB-H3; OB-CTX. None of them has been run. The L2 pre-push layer is not built (`l2-disposition.md`). Ship gate: no governed claim is used on a real issue until OB-H1 item 1 (parent `session_id` in subagent payloads), OB-H2 and OB-H3 have passed (design section 7, U1: item 1 before `full` or `--submit`, item 5 before any level; OB-H2 and OB-H3: sections 11 and 14).

## Acceptance criteria of Task 22

- The design status line names what is built (L1 guard, registrations, installer entry, claim IR-1, IR-2 and IR-4 to IR-7 detection; changed in the doc fix pass below) and what is pending (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX, L2); the removed phrase has no match; section 19.8 holds the O-15 sentence; section 5.1 NM1a has the `LL_RE_NM1A` note.
- `W-ENFORCEMENT-ABSENT` is described as a refusal (no agent, no launch record) and `W-L2-ABSENT` as a warning (the launch continues; L2 not built) in `SKILL.md`, `refs/claim.md`, `commands/issue.md`, `docs/user-guide/commands.md` and `docs/designs/sc-issue-claim-pipeline-flag.md`; each states the ship-gate rule; the last also states that IR-3 stays documentation only because no code writes `pipeline.json`.
- The full test command passed with only the 12 pending-observation skips; `make verify-sync` and `make lint` exited 0.

## Known limits and findings to carry into the pull request

1. **Raw bound-id scan (Task 5):** on a broken JSON payload, the failure-path scan for a bound session id can block an ordinary session whose broken JSON contains a bound id nested inside it. The scan cost grows with the number of `session_id` strings (500 ids: 0.37 s).
2. **NM1a design text (Task 6):** the printed design test never matched; the script holds the pattern in `LL_RE_NM1A`, and section 5.1 now carries a note saying so.
3. **Git wrapper gaps (Task 7):** a git subcommand of the UNKNOWN class passes when a wrapper option takes a value (`env -u X git ci`, `timeout -s KILL 30 git ci`) or an assignment holds a space (`A="x y" git ci`). Commit, push and merge are still caught (G1); design G3 does not require more.
4. **gh and curl gaps (Task 8):** a `curl` write passes when any word in the segment has basename `gh`; some `gh api` GET spellings of merge endpoints (trailing slash, `//graphql`, percent-encoding) are allowed. Rule H2 over-blocks reads containing `?`, `{`, `}`, `$` or quotes, and `gh pr create` with `--repo` on a continuation line is LL-REPO at FS.
5. **Escape and tamper gaps (Task 9):** `orca terminal send` can pass when the segment ends in `-h` through a comment, here-string or quotes. Allowed tamper spellings include `cd ~/.claude/. && rm -rf state`, `cat ~/.claude/x/../settings.json` and `uvx superclaude@latest install`; byobu and zellij are not escape words, and `claude --print=x` is not an escape flag.
6. **hooks.json files differ (Task 12):** the plugin `hooks.json` is a subset of the src one, not byte-identical. The test pins only that both hold the same two guard entries.
7. **Installer order (Task 13):** `_merge_settings` now inserts a missing managed entry before the first entry owned by a later `hooks.json` entry, so an upgrade keeps `launch-job-identity` last. Fresh install and re-install behave as before.
8. **Degraded level word (Task 14, decided open point):** the guard treats `degraded` as worktree with an LL-STATE note, but the pre-existing `launch-job-identity.sh` rejects it (exit 2 on every governed Bash call), so a degraded session cannot run Bash. A fix (add `degraded` to that hook's levels) needs a separate change.
9. **Hook composition (Task 14):** if Claude Code gave the guard the identity hook's rewritten command (which names `~/.claude/hooks/launch-job-identity.sh`), the guard would block it as LL-TAMPER at every level. The real hook order and `updatedInput` handling are unobserved; this belongs in OB-H3.
10. **Identity hook cost (Task 15):** `launch-job-identity.sh` costs a 79 ms median on ordinary Bash calls when the store holds only `pending/` (2 ms with no store). The worst T-SPD-5 run took 870 ms of its 1 s limit, so the speed test may flake on slow hosts.
11. **Corpus and design ambiguities (Task 16):** corpus ids are `NATK-n`, not `N-ATK-n`; N-ATK-36 cites R17, not R1/R3/R11. An unknown event under a bound id gives LL-BROKEN; OK-33 expects LL-REPO at FS (design H4 over MR).
12. **Unasserted attacks (Task 17):** T-ATK-54, 57 and 59 have no per-level assertion.
13. **Preflight scope (Task 18):** the IR-4 preflight reads the claim process only (HOME, PATH, environment, user and worktree project settings). It does not check enterprise-managed settings, string forms of `disableAllHooks` or plain-word matcher semantics.
14. **Release line (Task 19):** the release instruction uses a `<session id>` placeholder because the claim cannot know the id; the L2 `absent` line is also shown when git fails; the printed `rm` line breaks for a HOME containing a quote or `$`.
15. **L2 disposition (Task 21):** the section 19.2 bullet of `l2-disposition.md` omits the design condition "publication/self-test succeeds".
16. **IR-7 is a warning (decided open point):** the design asks for a refusal when L2 is absent; the claim only warns with `W-L2-ABSENT` because no L2 layer exists. The owner was asked and has not answered (`ir7-consequence.md`).

Third review round (issue #394, Task 22): five further lines of docs/designs/sc-issue-claim-pipeline-flag.md were corrected (output-contract comment, D11, Observed runs, A7, LA-6); make sync-dev and make verify-sync were re-run (exit 0). The test counts above are unchanged because no code or test changed after them.
