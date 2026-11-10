## Accuracy check for #450

**Verdict:** current

Checked against `origin/master` at 933cf3a4f, and the pull requests merged since the issue was opened (7, list truncated: no). No commit since #449 (24d79b7fa, the first merge after the issue was opened) changes `src/superclaude/cli/issue_watch/`, `tests/issue_watch/`, `docs/designs/issue-watcher.md` or `docs/designs/issue-watcher-setup.md` (`git log 24d79b7fa^..origin/master` on those paths is empty). Checked with `git grep` / `git show` on `origin/master`; codegraph and auggie were not used (the local checkout is on another branch, so the index would not match `origin/master`).

| # | Claim in the issue (quoted) | Status today (still true / changed / gone) | Evidence (path:line, PR #number or commit) |
|---|---|---|---|
| 1 | "`superclaude issue-watch` (check-config, init-state, once, reset, status)" | still true | `src/superclaude/cli/main.py:565` registers `issue-watch`; commands at `src/superclaude/cli/issue_watch/cli.py:111` (once), `:164` (status), `:185` (check-config), `:201` (init-state), `:282` (reset) |
| 2 | "2655 tests in `tests/issue_watch`" | not checked | Counting needs a pytest collection run, which writes caches; out of scope for a read-only check. `git grep -c "def test_"` shows about 600 test functions before parametrization |
| 3 | "the config ships with `enabled: false`" | still true | `docs/designs/issue-watcher-setup.md:74` (`"enabled": false`); code default `raw.get("enabled", False)` at `src/superclaude/cli/issue_watch/cycle.py:228`; refusal `not_enabled` at `cycle.py:685-686` |
| 4 | "Design: `docs/designs/issue-watcher.md` (follow-up list FU-1 to FU-12 is in section 16)" | still true | `docs/designs/issue-watcher.md:849` `## 16. Follow-up and owner questions`, rows FU-1 to FU-12 |
| 5 | "Owner runbook: `docs/designs/issue-watcher-setup.md`" | still true | File present on `origin/master` |
| 6 | "Code: `src/superclaude/cli/issue_watch/`, tests: `tests/issue_watch/` (fixtures under `fixtures/_assumed_shape/`)" | still true | 9 modules in `src/superclaude/cli/issue_watch/`; `tests/issue_watch/fixtures/_assumed_shape/` holds gh fixtures such as `gh_issue_list.json` |
| 7 | "the live-test record `docs/designs/issue-watcher-live-test.md` is written" (not yet done) | still true (not written) | `git ls-tree origin/master docs/designs/issue-watcher-live-test.md` returns nothing; the design says the owner writes it (`issue-watcher.md:33`) |
| 8 | "the cron entry (`0 */5 * * * *`, six fields)" | still true | `docs/designs/issue-watcher-setup.md:282`, `:637`; `docs/designs/issue-watcher.md:854` |
| 9 | "stale status line ... still says 'Design only, nothing implemented'" | still true (still stale) | `docs/designs/issue-watcher.md:3` |
| 10 | "59 reason names in code ... the new names are `cycle_complete` and `cycle_crashed`" | still true | `REASON_TABLE` in `src/superclaude/cli/issue_watch/audit.py:26-103` has 59 entries, including `cycle_crashed` (`:57`) and `cycle_complete` (`:64`); neither name appears in `docs/designs/issue-watcher.md` |
| 11 | "57 in design and spec" | not checked | The design does not list a count; it says `audit.REASONS` equals "the spec's reason table" (`issue-watcher.md:718`). The spec's own count was not checked: Not known yet |
| 12 | "full record is in `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/worker-final-report.md`" | still true | File present on `origin/master` (added in #451) |
| 13 | Launch path (implied by "starts `/sc:issue --claim <N>` in a new session") | still true; consistent with the new rules | `src/superclaude/cli/issue_watch/launch.py:95-117` builds `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt ... --json` in an existing worktree; it never runs `orca worktree create`, so the #449 hook (Claude Bash calls only) does not apply |

### Merged pull requests that touch this issue

| PR | Title | Relevant files | Effect on the issue |
|---|---|---|---|
| #449 | feat(orca): require an agent on every worktree create | `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh`, `src/superclaude/hooks/hooks.json`, `CLAUDE.md` | No change needed. The hook blocks only Claude Bash calls that run `orca worktree create` without `--agent`; the watcher runs from cron and uses `orca agent launch` in an existing worktree, which matches the new rule |
| #451 | docs(dev): record the issue-watcher brainstorm, task outcome and reflect patterns (#331) | `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/...`, `docs/memory/reflect/deviation-patterns-issue-331-github-issue-watcher.md` | Adds the worker-final-report the pick-up note cites; no code change |
| #455 | fix(issue): accept the ccsession session name in the tab title as the shim check | `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, `tests/skills/test_issue_orca_worktree.py` | Indirect: the claim session the watcher launches runs `/sc:issue --claim`, whose shim check now also accepts the ccsession session name. Worth noting in the FU-1 live test; no watcher change |
| #459 | docs(designs): describe the tab-title shim check in the claim pipeline design | `docs/designs/sc-issue-claim-pipeline-flag.md` | Docs for #455 only; no effect on the watcher |
| #458 | fix(mcp): accept the LiteLLM proxy tool names alongside the direct names (#454) | MCP proxy names and task files | No effect found |
| #457 | test(hooks): assert the launch-level guard speed limit on every run, including xdist workers (#440) | `tests/hooks/...` | No effect found |
| #453 | fix(tests): pick ccsession shim ports clear of the stand-in gateway's shim window (#443) | `tests/unit/...` | No effect found |

<!-- sc:issue:accuracy-check -->
