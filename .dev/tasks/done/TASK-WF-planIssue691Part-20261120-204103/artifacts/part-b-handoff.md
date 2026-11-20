# Issue 691 Part B: hand-off note

Issue: https://github.com/IronbellyOrg/IronClaude/issues/691 (Part A is merged as PR 693; this is Part B). This note is the text for the pull request body and for the question to the owner. `superclaude install` and the live OB-H2 rerun were NOT run.

## Done-when of Part B, both halves

Quoted from the issue brief: "the observation scripts read the file only, and a live claim leaves it in place".

- First half, "the observation scripts read the file only": MET, shown by `grep -n 'CLAIM_TXT\|CLAIM_LAST\|CLAIM_SCREEN\|claim_has\|terminal list\|claim-T[0-9]\.txt\|inodenumber' .dev/issues/442/scripts/session-gov.sh` printing nothing, by `bash .dev/issues/442/scripts/session-gov-selftest.sh` (135 OK lines, no FAIL, exit 0) and by `bash .dev/issues/442/scripts/selftest.sh` ending in `SELFTEST_OK` (exit 0).
- Second half, "a live claim leaves it in place": OPEN and owner-gated. Only the live OB-H2 rerun after merge can show it.

## The four changed files

- `.dev/issues/442/scripts/session-gov.sh`: `claim_send`, `launch_real`, `release_session`, `inode_record` and `preflight_refusal` now take status, warning, detail, terminal, layers and release from `launch-result.json` with `jq`; the `orca terminal list` lookup and the screen parsing are gone.
- `.dev/issues/442/scripts/session-gov-selftest.sh`: the stub claim now writes the result file and leaves a deliberately wrong claim screen; new cases cover fresh, screen ignored, missing, stale, unreadable (not JSON, array, no status, symlink), failed result, already_launched (earlier file untouched), terminal null or odd, missing layer, and a resume that only has saved text.
- `.dev/issues/442/scripts/runbook-selftest.sh`: four new checks that fail on the old text (file cited at least 7 times, no `terminal list` in the script, `orca terminal list` named only as no longer used, no `CLAIM_LAST` or `CLAIM_TXT`).
- `.dev/issues/442/observation-runbook.md`: the claim steps and the release steps point at `launch-result.json`; three section 6 table rows for the new printed literals; one new UNVERIFIED entry (item 15) in the not-verified list.

## Decisions (from the plan Constraints)

- File location: `$MAIN/.dev/issues/<N>/launch-result.json` in the main checkout (the worktree copy never receives it, `orca_worktree.py` skips it when copying).
- Claim start: the script records `CLAIM_START=$(date +%s)` right before it types the claim (after the `/clear`). A result is fresh only when its integer mtime is at least `CLAIM_START` and, when `launched_at` is a string, its epoch is also at least `CLAIM_START`. No clock-skew allowance.
- Outcomes: file absent after the poll loop is `PENDING reason=claim-result-missing` (exit 0); present but stale is `PENDING reason=claim-result-stale` (exit 0), which is also what an `already_launched` claim produces; a symlink, a non-object or a missing string `status` is `FAIL claim-result` (exit 1); a result whose status is not `launched` in `launch_real` is `FAIL <sub>-claim` (exit 1); a missing or invalid terminal handle is `PENDING reason=terminal-handle-missing` (exit 0).
- The claim screen is still read for two non-result jobs only: the vanished-terminal check and the `Do you want|/login|Not logged in` dialog check.
- JSON is read only through `jq` with `command timeout "$T"`; nothing from the file reaches `eval`, `source`, `bash -c` or an unquoted expansion; the terminal handle is checked against `^[0-9A-Za-z_-]+$` before `driver.sh adopt`.

## Task 6 commands and results

- `bash .dev/issues/442/scripts/selftest.sh`: exit 0, last line `SELFTEST_OK`, 0 FAIL lines (tail in `artifacts/t6-selftest.txt`).
- `bash -n` on `session-gov.sh`, `session-gov-selftest.sh`, `runbook-selftest.sh`: exit 0. `shellcheck` was not run (no binary on the machine; UNVERIFIED locally).
- `make sync-dev`: exit 0. `make verify-sync`: exit 0 (`All components in sync.`). `make lint`: exit 0 (`All checks passed!`) (`artifacts/t6-make.txt`).
- Negative checks: the new session-gov self-test fails 78 cases against the old `session-gov.sh` (`artifacts/t4-negative-check.txt`); the new runbook checks `result-file-cited`, `gov-no-terminal-list` and `gov-no-screen-parse` fail on the old text (`artifacts/t6-negative-check.txt`).

## Owner-gated, not run

1. `superclaude install`. Yes: the installed skill gains the file writer, so a live claim writes the file. No: the live rerun cannot happen.
2. The live OB-H2 rerun on the disposable issues T1 to T4. Yes: a real claim is made, the file's presence, mtime and fields are recorded in a new results entry, and the runbook's UNVERIFIED sentence can then be revised in a follow-up change. No: Part B stays open.

## Still UNVERIFIED

- Which `--source` folder the live claim passes (the plan assumes it resolves to the main checkout's `.dev/issues/<N>`).
- Whether a live claim leaves the file in the main checkout, and whether its `terminal`, `layers` and `release` equal what the session prints.
- `shellcheck --severity=warning` was not run locally (the repository's pre-commit config runs it in CI).
- The same-second edge of the staleness rule: a result written by an earlier claim in the very same second as this claim's start would be accepted; the several-second claim run makes this negligible.

## Differences from the plan

- Four more runbook lines (651, 655, 694, 796) said "release with the claim's rm line"; they now point at the `release` field of `launch-result.json`, so no instruction tells a person to take the release text from printed text.
- The appendix list gained one item, so the runbook grew by 4 lines (3 section 6 rows and 1 list item), all after line 698.
- In this checkout the plan's "master 1a6c8723f" is `HEAD`; the negative checks use `git show HEAD:<path>`.
- An unparseable `launched_at` string is ignored (the file mtime check already applies); the plan names only the below-`CLAIM_START` case.
- `claim_result_state` also sets a `CLAIM_STATE` variable, because the globals it sets would be lost if callers read its printed word through `$(...)`.
