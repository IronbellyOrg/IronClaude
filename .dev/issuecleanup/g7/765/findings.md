# Findings for issue 765

Issue 765: "[FEATURE] Stop Claude Code from killing the coordinator's message watch under low memory, and research what to stop instead" (open, label `enhancement`, filed and claimed 2026-11-24 by clayphi). Checked against `origin/master` f2894fc44 on 2026-11-24 (the local worktree HEAD a7ae3dd30 is 6 commits behind; the ccsession files are identical in both). Supporting analysis: `.dev/issuecleanup/g7/765/analyze/analyze-report.md`.

## Verdict

**still-relevant.** Nothing is built yet and nothing on master makes the issue stale.

Evidence:
- The switch `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` appears nowhere in the repo outside `.dev/issues/765/` (`git grep DISABLE_BG_SHELL_PRESSURE_REAP origin/master` returns nothing). `.dev/issues/765/` is not in this worktree (UNVERIFIED that it exists elsewhere; the claim comment says it was written by the claim session).
- Part 1 target is intact: `src/superclaude/skills/ccsession-tag/ccsession:1080-1086` sources the user env file; `:2412-2438` exports launch identity; the three `exec "$CLAUDE_BIN"` branches are at `:2447-2451` (untagged), `:2508-2512` (resume) and `:2515-2519` (new session). The file is 2520 lines. One export after `:2438` reaches all three branches.
- The settings alternative still lacks the switch: `src/superclaude/cli/user_settings_defaults.json:10-14` holds only `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` and `PONYTAIL_DEFAULT_MODE`. Whether Claude applies settings `env` before its rule is UNVERIFIED.
- No pull request touches it: `gh pr list --repo IronbellyOrg/IronClaude --state all --search 765` returned only #493 (an unrelated ccsession tier PR, merged); no PR names the switch. The issue has no linked or closing PR (`closedByPullRequestsReferences` is empty).
- Real current state: open, claimed by clayphi per the claim comment (the assignee field was not read), no code written; two comments by clayphi (an accuracy check "current" and a claim summary: complex, 32 hours, first step `/sc:design coordinator-watch-reap-protection ...`).
- Coverage gaps the issue must name: `src/superclaude/scripts/ic:128-130` runs `exec claude` directly, so `ic` launches bypass ccsession; ccsession-orca only applies when Orca's Claude command is set to it (`ccsession-tag/README.md:415`). There is no coordinator role signal (`CCSESSION_ORIGIN` at `ccsession:2428-2438` is human or agent, set by who chose the name), so "protect all ccsession launches" is the only verified scope.
- One claim in the issue is now out of date: the Playwright plugin is turned off by default on master (`user_settings_defaults.json` has `"playwright@claude-plugins-official": false`; commits f2894fc44 / PR #778 and f03ca87e2 / PR #768, issue 764). Part 2's "open Playwright browsers" candidate applies to older installs only.
- UNVERIFIED by me: every Claude Code 2.1.331 runtime behavior and all memory measurements (PSS, RSS, 12 sessions, #648 peaks). I did not read the Claude program or measure memory (shared host, read-only job). The accuracy-check comment on the issue confirmed several program strings; I rely on it only as a pointer.

## Complexity and size

Complexity: **complex**. Size: **L** (Part 1 alone is XS: one exported line, README text and about four launch tests; Part 2 is a measured research program over four candidates under load plus follow-up issues, which is what carries the claim comment's 32 hours).

## Priority

**P1.** The incident was real: a coordinator lost its message watch and stopped receiving messages, which blocks all coordinated work; Part 1 is a very cheap fix. Part 2 (the research) alone would be P2 because it only informs a later policy and blocks nothing.

## Concrete next steps

1. Decide scope as "all ccsession launches" (no role signal exists) and record that and the explicit-override rule in the plan: respect an existing value from `~/.claude/ccsession.env` (sourced at `ccsession:1083-1085`) or force `1`.
2. In `src/superclaude/skills/ccsession-tag/ccsession`, add one `export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=...` after the identity block (`:2438`) and before `:2440`; document it in `src/superclaude/skills/ccsession-tag/README.md` (session-wide effect, new Claude process needed, `ic` and hand-started Claude not covered).
3. Add launch tests to `tests/unit/test_ccsession_tag.py` and `tests/unit/test_ccsession_tiers.py` using the fake-Claude harness (fresh, resumed, tagged, untagged, tier variants). Run those two files plus `tests/unit/test_install_ccsession.py`, then `make sync-dev` and `make verify-sync`.
4. Live proof on a fresh coordinator: exact-name read of that one variable in `/proc/<pid>/environ`, and a message received over at least two five-minute watch cycles. Do not force critical pressure on the shared host.
5. Part 2 after Part 1 is merged: refresh the candidate list for the Playwright default change (PR #778), run the controlled measurements in an isolated workspace, write the ranked recommendation, and file one follow-up issue per implementation recommendation.
6. Consider a small separate issue for `ic:128-130` if coordinators are ever launched that way (coordinator decision).

## Dependencies

Needs: none. Part 1 has no prerequisite issue; Part 2 uses closed issue 648 only as a baseline. Blocks: nothing hard; the follow-up issues Part 2 creates (session reaper, browser cleanup, index scheduler, workspace memory cap) depend on its recommendation.

## Related issues

- 648 (closed, completed): codegraph first-index memory measured with concurrent builds; baseline for Part 2.
- 716 (open): coordinator next-release features; 717 (open): issue watcher features; both are coordinator work this fix protects. Related, not duplicates.
- 354 (open): v5.0.0 impact runbook, cited by the issue.
- 764: Playwright plugin default (the cause of PRs #768 and #778); I did not re-read 764 itself (UNVERIFIED state).

## Related PRs

- #778 (f2894fc44) fix(install): turn the Playwright plugin off by default; changes a Part 2 candidate.
- #768 (f03ca87e2) fix(install): point the Playwright plugin at Playwright's Chromium on Linux.
- #301 feat(ccsession): route Orca's Claude launches through ccsession (merged); the path Part 1 relies on.
- No PR targets issue 765 itself.
