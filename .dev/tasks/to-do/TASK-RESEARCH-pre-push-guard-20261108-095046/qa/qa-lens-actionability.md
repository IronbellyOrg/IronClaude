## Actionability QA Report

**Report reviewed:** .dev/tasks/to-do/TASK-RESEARCH-pre-push-guard-20261108-095046/RESEARCH-REPORT-pre-push-guard.md
**Lens:** Actionability (report-lens-actionability). Checks: S7 recommendations can be carried out without more research; each S8 step gives an action, target files and expected outcome; success criteria are testable pass/fail; a developer new to the work could start from S8 alone.
**Date:** 2026-11-08
**Fix authorization:** false (report only; the document was not modified)

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|----------|---------|---------|--------------|
| 1 | CRITICAL | S7 (identity variant A-i); S8 1.2 vs 2.4 | Step 1.2 (report line 1075) sets the hook's `PATH` to "the install-time uv directory", so each install writes a value specific to that machine into the hook. Step 2.4 (line 1091) treats an existing hook as owned only if "its full bytes equal the installed guard source". A hook with a per-machine uv path can never match the packaged source byte for byte, so the plan's own installs would be reported as `foreign-pre-push`. No step says where or how the uv directory is recorded. A developer cannot build 1.2 and 2.4 as written. | Pick one approach and write it into 1.2 and 2.4. (a) Keep the hook bytes identical to the packaged source and read the uv directory from a separate owned file. Name the file (for example under `~/.claude/state/`) and the reason to report when it is missing. (b) Or define ownership as "the packaged template with exactly one substituted `PATH=` line", and give that line's format and the comparison rule. |
| 2 | IMPORTANT | S8 2.1 (publisher) | The step says to publish the guard bytes but does not name the file the publisher reads them from at run time. It also does not say what happens, or which `l2_status` reason is reported, when that file is missing. Step 2.7 places the guard source in `~/.claude/hooks/` only as a conditional proposal. | Name the source (for example `~/.claude/hooks/<guard>.sh`, installed by `_copy_scripts`) in 2.1, and add a reason value for "guard source missing". |
| 3 | IMPORTANT | S8 2.7 (line 1094); 3.2 | Step 2.7 (register the new script in `_FRESHNESS_SCRIPTS`, `install_hooks.py` 42-94) is marked "conditional on Section 9 rows 15 and 2". The `Makefile` "=== Installer Registration ===" check (lines 307-319) flags drift for any `src/superclaude/hooks/scripts/*.sh` that is not registered. So once Phase 1 adds the guard `.sh` there, 2.7 is required, and step 3.2 (`make verify-sync`) fails without it. | Make 2.7 unconditional and order it right after step 1.1. Or, if the file goes somewhere else, name that location in 1.1. |
| 4 | IMPORTANT | S7 / S8 Phase 2 (keep, don't replace + full-byte ownership) | The plan has no upgrade path. Once the packaged guard changes, a hook installed from an older version no longer matches byte for byte. It is reported as `foreign-pre-push` and never replaced, so every existing worktree keeps the old guard forever. | Add a step with a version marker and an upgrade rule: an existing hook that matches a known earlier owned version is replaced through the same O_EXCL/link path. Say where the known earlier versions (or their hashes) are kept. |
| 5 | IMPORTANT | S8 6.7 and the [CONTRADICTION] at line 1140; S9 rows 7, 8, 29 | The test file for the L1 regression tests is left as an unresolved [CONTRADICTION]: 6.7 names `tests/hooks/test_launch_level_guard_with_identity.py`, while S9 row 7 (line 1279) says to add the test to `tests/hooks/test_launch_level_guard.py`. Neither text cites the seed brief constraint (`.dev/brainstorms/20261108-094705-l2-pre-push-guard/seed-brief.md` line 59): issue #440 edits `tests/hooks/test_launch_level_guard.py` in another worktree, and L2 tests should go in new files where possible. A new developer cannot tell where to write the tests, and following S9 row 7 would conflict with #440. | Resolve it in S8: put the new L1/L2 cases in a new file (for example `tests/hooks/test_launch_pre_push_guard.py`) or in `test_launch_level_guard_with_identity.py`, cite seed brief line 59, update S9 rows 7, 8, 29 to match, and remove the contradiction note. |
| 6 | IMPORTANT | S8 4.2 (`l2_status`) | The step changes `l2_status` (`orca_worktree.py` def at 1012, which now returns only `"absent"` / `"present-unverified"`) to report reason values. It does not give the new return type, and it does not list the consumers that must change: `session_report` (the text "L2 pre-push: present-unverified" at 1065), `cmd_launch` (`l2_notes` at 1312), `sc-issue-protocol/refs/claim.md` line 120, `commands/issue.md`, `sc-issue-protocol/SKILL.md`, `docs/user-guide/commands.md`, `docs/designs/sc-issue-launch-level-hook.md`, `docs/designs/sc-issue-claim-pipeline-flag.md`, and the assertions in `tests/skills/test_issue_orca_worktree.py` (1672, 1691-1692) and `tests/skills/test_issue_protocol.py`. | Give the signature (for example `l2_status(wt) -> tuple[str, str \| None]`, or a closed set of strings), and add one sub-step for each consumer listed here. |
| 7 | IMPORTANT | S8 1.9 (line 1082) | The step says to emit "the guard version line so `l2_status` can read it", and points to "`GUARD_VERSION_LINE` already exists at ow:804". That constant is `"# launch-level-guard-version: 1"`, the L1 guard's version, and `enforcement_preflight` (950-951) checks it. Reusing it would tie the L1 and L2 versions together: bumping the L1 version would break the L2 check. | Define a separate L2 constant (for example `PRE_PUSH_GUARD_VERSION_LINE`) with its own header text, and name the function that checks it. |
| 8 | IMPORTANT | S3.5 success criteria (SC-1..SC-23) | Several planned behaviours have no pass/fail criterion: the Phase 5 L1 refusal tokens (`.git/hooks` tamper, `--config-env`, `GIT_CONFIG_*`, `GIT_CONFIG_PARAMETERS`, `-c hook.pre-push.*`), both states of the IR-7 switch, the `hookspath-set` reason, and the integrity/exec-bit recheck before each launch. SC-18 asks only for "a reason", not the exact reason string. | Add SC rows, each with the command, its input and the exact expected output or exit code. List the exact reason strings in SC-18. |
| 9 | IMPORTANT | S8 step tables (all phases) | The step tables have no "expected outcome" / "done when" column (checklist item b). Several steps give no concrete change or no pass condition: 6.6 (line 1133) leaves two options open ("point it at the real guard script or make it refuse malformed input"); 7.4 (line 1149) says "state the accepted cases or the chosen remedy" without the text; 3.1, 3.2, 5.3 and 5.5 have no observable done condition. | Add a "Done when" column with an observable result (a named test passes, a grep returns 0 hits, given output appears). Choose the 6.6 option, and give the replacement doc text for 7.4. |
| 10 | IMPORTANT | S8 4.4 (IR-7 refusal switch); G-17, R3 | The owner decided the default (off), but the report leaves the switch mechanism open (G-17 line 653: "Open: the switch mechanism"; R3 line 1325) and proposes none. Without a mechanism, step 4.4 cannot be started without another decision. | Propose a concrete mechanism that keeps the decided default, for example a module constant `IR7_REFUSE_ON_L2 = False` in `orca_worktree.py` that guards the commented refusal at lines 1309-1310, and name the test that turns it on. |
| 11 | IMPORTANT | S7 bypass table (line 1025) vs S8 5.4 (line 1120) and 6.7 | S7 says the `-c` form is refused by the `hookspath` token but that "`\x50` spelling and env forms evade" (02 line 249). Step 5.4 adds `GIT_CONFIG_*` (which covers the env form), but no step fixes the escaped `$'core.hooks\x50ath'` spelling passed through `-c` (the token match runs on the undecoded text). Step 6.7 asks for tests of "the section-9 evasions 02 read statically", so the plan asks for a test that no planned fix makes pass. | Add a sub-step to 5.4: decode `$'...'` ANSI-C quoting before the token match, or refuse `-c` values that contain `$'`. Point the 6.7 test at both spellings. |
| 12 | MINOR | S8 1.3 (line 1076) | "Bound the call with a timeout" gives no value and no mechanism (`timeout(1)` or similar). | Give the value and the mechanism. |
| 13 | MINOR | SC-12 / SC-13 | The criteria require stdin to be read in full but do not say how a test can observe that. | Name the method (for example the writer gets SIGPIPE/EPIPE if stdin is not drained). |
| 14 | MINOR | SC-23 | The criterion is written as conditional on choosing A-i, although S7 already recommends A-i. | Make it unconditional, or tie it to the S9 row that decides A-i. |
| 15 | MINOR | S8 2.6 / 6.1 / 6.3 | The steps do not say how to create the synthetic ordinary and governed actors, although reusable fixtures exist in `tests/hooks/test_launch_job_identity.py` (`LocalPushFixture` at 1175 and the governed session fixtures). | Name these fixtures in the steps. |
| 16 | MINOR | S8 6.4 (line 1131) | It cites `test_ir6_l2_status_follows_the_git_hook_path` at 1686-1729. The def is at `tests/skills/test_issue_orca_worktree.py` line 1696. | Correct the line range. |
| 17 | MINOR | S8 2.3 (line 1090) | `git config --get core.hooksPath` is written without `-C <wt>`, so it reads the repository of the current directory, not the target worktree. | Write it as `git -C <wt> config --get core.hooksPath` (and likewise the `--worktree` form). |

### Summary

- Total findings: 17
- Critical: 1
- Important: 10
- Minor: 6

Verdict: FAIL (1 critical + 10 important; the 6 minor findings are notes only)

Checklist results:
- (a) S7 recommendations can be carried out without more research: FAIL (findings 1, 4, 10, 11).
- (b) Each S8 step gives an action, target files and expected outcome: FAIL (findings 2, 3, 6, 7, 9; minor 12, 15, 17).
- (c) Success criteria are testable pass/fail statements: FAIL (finding 8; minor 13, 14).
- (d) A developer new to the work could start from S8 alone: FAIL (findings 1, 5, 6, 9, 10).

## Self-Audit

**(a) Reliance list (rf-qa PASS items skipped for structural re-check):**
- No `## Inherited Structural Verdict` was supplied, so nothing was relied on. Section numbering and the file existence of cited research files were not re-checked, because this lens covers Actionability only.

**(b) Independent semantic checks (INV-019):**
- Ownership vs fixed PATH (finding 1): read report S8 lines 1075 and 1091; read `launch-job-identity.sh` (uv check at line 25, `exec uv run` at 566) to confirm that `identify` needs uv on `PATH`.
- Installer registration (finding 3): read `Makefile` 307-319 and `install_hooks.py` `_FRESHNESS_SCRIPTS` 42-94 (identity at 90, L1 guard at 93).
- `l2_status` consumers (finding 6): read `orca_worktree.py` (l2_status 1012, session_report 1065, cmd_launch 1309-1312) and grepped `present-unverified` / `W-L2-ABSENT` across skills, commands, docs and tests.
- Version constant (finding 7): read `orca_worktree.py` 804 and `enforcement_preflight` 950-951.
- Test file conflict (finding 5): read seed brief line 59 and report lines 1134, 1140, 1279.
- `\x50` evasion (finding 11): grepped the report (lines 143, 687, 1025, 1120) and research 02 line 249; read L1 guard 525-532 and 661.
- Test citation (finding 16): grepped `def test_ir6` in `tests/skills/test_issue_orca_worktree.py` and got 1696.
- Fixtures (finding 15): read `tests/hooks/test_launch_job_identity.py` around 1175.

**Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: about 20 | Grep: about 15 | Glob: 2 | Bash: 2 (read-only batch scripts in a `mktemp -d` directory under /tmp, both `BATCH_OK failures=0`, both cleaned up). No web research was done, so Tavily was not needed. No git experiment, no push, no gh call, and no file outside the task `qa/` directory was written.

