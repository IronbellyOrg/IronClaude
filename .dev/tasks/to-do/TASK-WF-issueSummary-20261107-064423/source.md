# Summary: #361 [featRel] pr-submit: late conflict re-sync during the CI wait (P3 of #305)

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/361
- Type: feature
- Complexity: complex (rubric: `refs/claim.md`)
- Effort estimate: 24 hours

## What the issue asks for

Today `/sc:pr-submit` checks for merge conflicts once (Wave 8a), just before it starts waiting on CI (Wave 8). If the base branch moves during that wait and the PR becomes conflicting, the run does not notice. A run that saw no earlier conflict can even finish `terminal_clean` while the PR is conflicting. The issue asks for P3 of #305. `poll-ci-checks.sh` appends a `merge_state` field to its JSON line. When that field reads CONFLICTING, or the CI wait is stuck at `polling` with no checks while GitHub reports CONFLICTING, the run goes through Wave 8a once more. This second pass handles Tier 0 and Tier 1 only, and only if no sync push has landed yet in this run (`SYNC_CAP = 1`). A late Tier 2 conflict halts with reason `late_conflict`. Every existing push-safety rule stays as it is. There is also a go/no-go gate: one real run where the base moved during the CI wait, or a maintainer waiver.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-ci-checks.sh` | The CI poller. It must also read `mergeStateStatus`/`mergeable` and append `merge_state` after the existing keys (today it reads `number,url,headRefOid` only, lines 71 and 115-118). |
| `src/superclaude/pr_submit/ci.py` | `classify_checks` (lines 25-55) must keep its current results unchanged. The late trigger decision belongs beside it or in `conflicts.py`. |
| `src/superclaude/pr_submit/conflicts.py` | `SYNC_CAP` (41), `HOOKS` (47), `mergeability_hint` (439), `_route_wave8a` (960-1002: already returns `sync_cap` and `late_conflict`), `conflict_action` (1005), `prior_conflict_cycles` (1247). A late trigger can probably reuse the `wave8a` router as it is. Whether that is enough, or a new hook label is needed, is not known yet. |
| `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md` | The Wave 8 bullet (285) and the Wave 8a bullet (286) need the late trigger. Their text is byte-pinned by tests. |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/ci-poll.md` | The poll payload contract (lines 8-21 and 65) and the `pr_conflicting` skip rule (32). |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md` | The end-of-CI-wait `mergeable` re-read and `late_conflict` (214), and the halt-reason table (289). Both cite #361. |
| `src/superclaude/skills/sc-pr-submit-protocol/refs/state-machine.md` | The `sync_push_count` / `SYNC_CAP` rule (164). |
| `src/superclaude/commands/pr-submit.md`, `docs/user-guide/commands.md`, `docs/user-guide/flags.md` | #418 wording ("at most one conflict cycle per run; late text conflicts halt"). Update it to describe the late Tier 1 sync. |
| `tests/pr_submit/test_ci_classify.py` | Existing `classify_checks` rows must pass unchanged. Add the new payload-shape test here (requirements section 8.2, line 718). |
| `tests/pr_submit/test_conflict_scripts.py` | Today it covers only the `poll-ci-checks.sh --evidence-sha` mode (1678-1716). Add a stubbed-`gh` test for `merge_state` here. |
| `tests/pr_submit/test_conflicts_core.py` | The router tables, including the `late_conflict` rows (1031-1032) and the `SYNC_CAP` rows (1526-1528). |
| `tests/pr_submit/test_conflict_sync_protocol.py`, `tests/pr_submit/test_static_grep.py` | Byte-pinned fragments E9/E10 (303-335) and `test_static_grep.py:796`. They break if the Wave 8 or 8a text changes. |
| `.dev/brainstorms/issue-305-pr-submit-conflict-resolution/merged-requirements.md` | Present in this worktree. Section 5.6 P3 row (433), FR-24 (649), FR-25 (650), section 8.2 row (718), section 9 P3 row (795), K17 open question INV-010 (821). |
| `.dev/designs/issue-305-pr-submit-conflict-resolution/DESIGN.md` | Lists P3 as out of scope (12, 65, 1442). The end-of-wait re-read and INV-027 (169, 279) are the shipped behaviour P3 extends. |
| GitHub `gh pr view --json mergeable,mergeStateStatus` | Live data source. GitHub may report `UNKNOWN` for a while after the base moves. A conflicting PR gets no `pull_request` checks. |

## Analysis

None: the accuracy check found the issue current, so no analysis ran.
