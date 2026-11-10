# Source snapshot for /sc:workflow

Two inputs were given: the inline prompt, and the file `.dev/issues/450/issue-summary.md` (named as `Input:` in `.dev/issues/450/next-steps.md`). Both are copied below.

## Inline prompt

Roll out the issue watcher (issue #450, follow-up to #331): replace the _assumed_shape fixtures with captured real gh and Orca output after the owner-run live test (FU-1), fix the stale status line and the 59-name reason table in docs/designs/issue-watcher.md, prepare the shadow-run, lock, restart and cron steps (FU-2) as owner-run checklist items, keep enabled false until the owner flips it. Spec and runbook: docs/designs/issue-watcher.md, docs/designs/issue-watcher-setup.md. Code: src/superclaude/cli/issue_watch/, tests/issue_watch/

Flags: --depth standard --handoff none

## File: .dev/issues/450/issue-summary.md

# Summary: #450 [FEATURE] Roll out the issue watcher: live test, shadow run, cron (follow-up to #331)

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/450
- Type: feature
- Complexity: complex (rubric: `refs/claim.md`)
- Effort estimate: 20 hours

## What the issue asks for

The issue watcher (`superclaude issue-watch`, built in PRs #447 and #448) is merged but has never run live, has no schedule, and ships with `enabled: false`. The issue asks to turn it on safely: first an owner-run live test against real `gh` and Orca that replaces every guessed `_assumed_shape` fixture with captured output and is written up as `docs/designs/issue-watcher-live-test.md` (FU-1); then a reviewed 24-hour shadow run, the two-process lock test and the state-directory restart test, after which `enabled` becomes `true`; then the six-field cron entry `0 */5 * * * *` (FU-2). It also asks to fix two doc drifts: the stale "Design only, nothing implemented" status line in the design, and the reason table, which in code has 59 names (adding `cycle_complete` and `cycle_crashed`) that the design does not list. The accuracy check found every checked claim still true on `origin/master` at 933cf3a4f.

Effort reasoning: the live test, capturing and replacing about 12+ fixtures and re-running the suite, the shadow-run review, the lock and restart tests, the cron install and the doc fixes add up to over 16 hours of hands-on work, plus 24 hours of wall-clock waiting for the shadow run. Several steps need the owner's own `gh` login and Orca, so they cannot be done by an agent alone.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/cli/issue_watch/` (`cli.py`, `cycle.py`, `launch.py`, `github.py`, `audit.py`, `record.py`, `predicates.py`, `runner.py`) | The watcher code; `cycle.py:228` reads `enabled`, `audit.py:26-103` holds the 59-name `REASON_TABLE`, `launch.py:95-117` builds the `orca agent launch` argv |
| `src/superclaude/cli/main.py:565` | Registers the `issue-watch` command group |
| `tests/issue_watch/` | Watcher test suite; must still pass after the fixture swap |
| `tests/issue_watch/fixtures/_assumed_shape/` | Guessed `gh` and Orca replies that FU-1 replaces with real output |
| `docs/designs/issue-watcher.md` | Design: stale status line at line 3, deployment gate at line 33, reason table reference at line 718, follow-ups FU-1 to FU-12 in section 16 (line 849) |
| `docs/designs/issue-watcher-setup.md` | Owner runbook: config with `"enabled": false` (line 74), enable step (line 274), cron schedule (line 282) |
| `docs/designs/issue-watcher-live-test.md` | Does not exist yet; the owner writes it in FU-1 |
| `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/reports/worker-final-report.md` | Review state from the build, including the unrechecked low regression fix |
| Orca CLI (`orca agent launch --surface terminal --retry-launch`) | External system the watcher drives; its reply shapes are unverified until FU-1 |
| GitHub CLI (`gh issue list`, `gh api`, GraphQL) | External system the watcher polls; its reply shapes are unverified until FU-1 |
| `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` (PR #449) | New Claude Bash hook; does not affect the watcher, which uses `agent launch`, not `worktree create` |
| `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (PR #455) | Shim check in the `/sc:issue --claim` session the watcher launches; relevant to what the live test sees |
| Host cron / scheduler | FU-2 installs the six-field entry here; FU-2 also covers a persisted `state_dir` if `$HOME` is not persistent |

## Analysis

None: the accuracy check found the issue current, so no analysis ran.
