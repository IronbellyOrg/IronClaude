# Findings: issue 825 (L1 launch-level guard does not protect integration)

Read on 2026-11-25 against origin/integration at 4e35750e7 (PR 824 merge). Issue 825 has no comments and no linked PR. Analyze run: .dev/issuecleanup/g8/825/analyze/analyze-report.md.

## Verdict

**still-relevant.** The main defect is unfixed on the default branch; two of the issue's four steps are partly or wholly open.

- Core gap, confirmed: `src/superclaude/hooks/scripts/launch-level-guard.sh:736` still reads `case $LL_D in master | main) LL_CLASSES+='PROTECTED ' ;; ...`; lines 59-60 still say "a push to master or main." A push to `integration` gets no PROTECTED class. The class is denied for levels W, WA, F, FS at line 812. The plugins mirror has the same line 736 (`plugins/superclaude/hooks/scripts/launch-level-guard.sh`). No live run was done: the gap is read from code (as the issue itself says).
- The issue's "PR 824 is open" is out of date: PR 824 is MERGED (commit 4e35750e7, mergedAt 2026-11-24T23:05:52Z per the PR list; 23:25:39Z in the PR detail view, the two disagree, UNVERIFIED which is right; either way before the issue was filed at 23:26:19Z). PR 824 changed only the L2 hook: `launch-level-pre-push.sh:2` is now version 2 and `:17` is `L2_PROTECTED=(refs/heads/main refs/heads/master refs/heads/integration)`; `orca_worktree.py:877` is `L2_VERSION_LINE = "# launch-level-pre-push-version: 2"`; `orca_worktree.py:1363` lists the three refs.
- Step 2 (version bump): `orca_worktree.py:876` is still `GUARD_VERSION_LINE = "# launch-level-guard-version: 2"`, so the guard has not been bumped. No sha256 pin was found in `src/superclaude/hooks` (git grep returned nothing) and the reviewer found none for the guard, so "re-pin if pinned" does not apply to the guard. A pin exists only for the L2 hook (`tests/cli/test_install_hooks.py:1101`, `L2_HOOK_SHA256`), which this plan does not change.
- Step 3 (stale L2 hook): partly done. `_l2_conflict` (`orca_worktree.py:1278-1283`) already prints the exact `rm` command and the reason `stale` (`:1306`). It does not say which version was found. The stale verdict itself is already tested in `tests/skills/test_issue_l2_install.py` (lines 194-211: `_version_0` and the `old-version`, `marker-only`, `edited-body` forgeries expecting `stale`; line 716 asserts the reason starts with `stale:` or `foreign:`). `tests/cli/test_install_hooks.py` has no stale-L2 case (its "stale" hits at lines 1228-1245 concern tool registrations). Only the version-named message is missing.
- Step 4 (docs): `docs/designs/sc-issue-launch-level-hook.md:516` still says `# launch-level-pre-push-version: 1`; lines 32, 241, 379 and 522 still name only main and master.
- Tests: `tests/hooks/test_launch_level_guard.py` has 0 mentions of integration; `tests/hooks/test_launch_level_pre_push.py:49` has `BRANCHES = ["main", "master", "integration"]` (L2 only).
- Open PRs: none found touching the guard (open-PR title filter for guard, launch, hook, 825 returned nothing).

## Complexity and size

Complexity simple; size S. One list in one shell file (3 lines) plus a mirror, a version bump in two source places plus the two test files and one architecture doc that pin version 2 (about 8 files in all), 2-3 new tests, a design doc edit, and an optional installer message tweak. The "read the default branch at runtime" idea in step 1 would add risk (the guard must not call the network, and has a 5 s budget per the design doc line 220) and is not needed.

## Priority

P2. The L2 hook already refuses `refs/heads/integration` wherever it is installed and current, so this is a missing first layer plus a stale-hook window, not an open door; but integration is now the default branch, and every governed agent in the repo is affected.

## Concrete next steps

1. In `launch-level-guard.sh` add `integration` to the PROTECTED case at line 736 and the texts at lines 59-60; make the same change in `plugins/superclaude/hooks/scripts/launch-level-guard.sh`. Keep it a literal list (no runtime default-branch lookup).
2. Bump `GUARD_VERSION_LINE` (`orca_worktree.py:876`) and the version comment inside the guard to 3 so installed copies are reported stale and refreshed by `superclaude install --force`. The same commit must update every place that pins version 2 (found by the reviewer): `tests/hooks/test_launch_level_guard.py:265` and `:4725-4726` (`test_the_guard_and_its_mirror_carry_stamp_two_and_agree`), `tests/skills/test_issue_orca_worktree.py:1302` and `:1984-1992`, and `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1070` and `:1443`. Otherwise the suite goes red.
3. Add L1 tests in `tests/hooks/test_launch_level_guard.py`: `git push origin integration` and `HEAD:integration`-style forms refused for governed actors at W/WA/F/FS, a feature branch allowed.
4. Optional: make the stale L2 message name the version found, and extend the existing stale cases in `tests/skills/test_issue_l2_install.py` to assert the version text. Do not add a new stale-L2 test elsewhere; the stale verdict is already covered.
5. Update `docs/designs/sc-issue-launch-level-hook.md` (L2 version 2, three-ref list, guard version 3), including the two-ref wording at lines 32, 241, 379, 516, 522 and 532.
6. Gate: `uv run pytest tests/hooks tests/cli/test_install_hooks.py tests/skills/test_issue_orca_worktree.py -q`, full `uv run pytest`, `make lint`, `make verify-sync`; the PR goes through `/sc:pr-submit --monitor 3` against the fork with base `integration`.

## Dependencies

Needs: none (PR 824, which it follows, is merged). Blocks: nothing found. Related ordering: independent of 702 and 723.

## Related issues

- 702 (open): protect the default branch, no direct push or force push (GitHub side).
- 723 (open, parked): protect master and integration with GitHub rules.
- 394 (closed): built the launch-level hook.
- 442 (open): live observations OB-H1 to OB-H3 for the launch-level guard; a new guard version affects what it observes (UNVERIFIED how).
- 678 (open): bare `claude <prompt>` runs outside the limits; same guard.
- 769 (open): trim startup token costs; follow-up 1 is where this was found.

## Related PRs

- 824 (merged): "make integration the base branch everywhere master was assumed"; changed the L2 hook, installer constants, tests and docs files but not the L1 guard.
- 707 (merged): last change to the guard file, introduced guard version 2 (commit 2ea524514).
