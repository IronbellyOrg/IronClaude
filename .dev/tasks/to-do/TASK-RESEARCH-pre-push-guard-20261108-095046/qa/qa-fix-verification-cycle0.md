# QA Report — Gate 3 Fix Verification (cycle 0)

**Topic:** git pre-push hook semantics for the L2 launch-level guard
**Date:** 2026-11-08
**Phase:** report-validation (verification of Gate 3 fixes)
**Fix cycle:** 1 (verification of cycle-0 fixes)
**Fix authorization:** false (no file other than this report was changed)
**Inputs:** `qa/qa-consolidated-findings-phase6-cycle0.md` (20 blocking: #1 CRITICAL, #2-#20 IMPORTANT), `qa/qa-fix-log.md` (claims all 20 FIXED), `RESEARCH-REPORT-pre-push-guard.md` (1469 lines, read in full)

---

## Overall Verdict: FAIL

All 20 blocking findings are fixed against their evidence, but the fixes introduced 2 new IMPORTANT issues (N-A, N-B below). Under the gate rule (PASS only when all blocking findings are fixed and no new CRITICAL or IMPORTANT issue exists), the verdict is FAIL.

## Items Reviewed (blocking findings)

Report line numbers are those of the current `RESEARCH-REPORT-pre-push-guard.md`. "ow" = `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`.

| # | Original finding | Fixed | Evidence | New issue |
|---|---|---|---|---|
| 1 | CRITICAL: uv PATH baked into hook bytes vs full-byte ownership | yes | Step 1.2 (line 1099) keeps hook bytes identical to the packaged source and reads `<hooks-dir>/pre-push.uv-dir` at run time; 2.1 (line 1115) writes it at 0644 and reports `uv-dir-missing`; 2.4 (line 1118) states the bytes hold no machine value; reason added to SC-18 (line 589), SC-23/SC-24 (lines 594-595), 4.2 closed set (line 1142), 6.3 (line 1170), 7.4 (line 1190). Contradiction with full-byte check is gone. | **N-A (IMPORTANT)**: the new uv-dir file is an unprotected trust input (see below). |
| 2 | `[CONTRADICTION]` on `--path-format=absolute` | yes | Grep for `[CONTRADICTION` in the report: 0 matches. §2.5(c) table, R9 (line 1374), G-26 (line 1225) and Phase 2.2 (line 1116) agree: verified on 2.47.3 from a linked worktree (web-01 D3a-e) and main checkout (fix run X1, `qa/qa-fix-log.md` line 18: `main: $S/repo/.git/hooks/pre-push`, `wt: $S/repo/.git/hooks/pre-push`, hooksPath outputs recorded). | MINOR M-3 (L-2 row does not cite X1). |
| 3 | `[CONTRADICTION]` on the L1 test file | yes | Phase 6.7 (line 1174) now targets new `tests/hooks/test_launch_level_guard_l2_bypass.py`; rows 7 (line 1322), 8 (line 1323) and 29 (line 1349) name the same file; Phase 5 and 6 dependency lines (1150, 1164) give the reason. Seed brief line 59 read: "Issue #440 edits `tests/hooks/test_launch_level_guard.py` ... Keep the L2 tests in new files where possible." Harness `_bind` 67, `_payload` 81, `_hook` 92, `_both` 103 confirmed by Grep of `tests/hooks/test_launch_level_guard_with_identity.py`. No marker remains. | none |
| 4 | No Goal/Dependencies lines in 8.1-8.7 | yes | `**Goal:**` and `**Dependencies:**` present at lines 1093-1094, 1110-1111, 1126-1127, 1136-1137, 1149-1150, 1163-1164, 1182-1183. | none |
| 5 | Wrong refactor-plan path | yes | `ls`: `.dev/brainstorms/20261105-170229-launch-level-hook/refactor-plan.md` does not exist; `.../adversarial/adversarial/refactor-plan.md` exists and its line 1158 is the `D4, X-009` git-level hooks row. Report §6.1 Cons cites the existing path. | none |
| 6 | Step 2.1 names no byte source or missing-source reason | yes | Line 1115: source is `~/.claude/hooks/launch-pre-push-guard.sh` written by `_copy_scripts` (install_hooks.py line 251, Grep), reason `guard-source-missing`; SC-18 and 6.4 carry it. | none |
| 7 | Step 2.7 conditional though `make verify-sync` fails | yes | Line 1121: "This step is required, not optional"; ordered right after 1.1 (lines 1094, 1111). Makefile lines 307-323 read: `MISSING from _FRESHNESS_SCRIPTS` echo at 314, `drift=1` at 316, STALE branch 318-323. install_hooks.py: `_FRESHNESS_SCRIPTS` at 42, identity 90, L1 guard 93, verify-sync comment 63. | none |
| 8 | No upgrade path | yes | Step 2.8 (line 1122) adds `L2_EARLIER_OWNED_SHA256`, re-check then replace, with a Done-when for both an owned older copy and a near-copy. | MINOR M-1 (2.8's `rename` vs the "never rename" wording of 2.1 and §8.10 line 1292; check-then-rename window). |
| 9 | Step 4.2 has no return type or consumers | yes | Line 1142: `l2_status(wt: str) -> tuple[str, str \| None]`, closed reason set, consumers 4.2a-4.2j. Spot-checked by Grep: ow `l2_status` 1012-1029 and `l2_line` 1061-1067 (`present-unverified` at 1065); `claim.md` 120, 127, 129; `issue.md` 16; `SKILL.md` 92, 136, 150; `docs/user-guide/commands.md` 381; `test_issue_orca_worktree.py` 1672, 1691-1692; `test_issue_protocol.py` 485 — all hit. | none (see N-A for the `uv-dir-missing` check that 4.2 does not list) |
| 10 | Step 1.9 reuses `GUARD_VERSION_LINE` | yes | Line 1106: separate `L2_GUARD_VERSION_LINE` / `# launch-pre-push-guard-version: 1`. Read ow:804 `GUARD_VERSION_LINE = "# launch-level-guard-version: 1"`; ow:950-951 use it in `enforcement_preflight`. Claim matches code. | none |
| 11 | Missing SC rows | yes | SC-23 to SC-31 at lines 594-602, each with a concrete pass condition and a Phase reference; Done-when cells cite them (1.2, 4.1, 4.4, 5.1-5.4, 2.3). | none |
| 12 | No Done-when column; 6.6 open; 7.4 no text | yes | Every §8.1-8.7 table has a `Done when` column with a checkable condition; 6.6 (line 1173) "**Chosen:**" real guard script; 7.4 (line 1190) gives replacement text for line 493 and an addition after 557. | none |
| 13 | No IR-7 switch mechanism | yes | Step 4.4 (line 1144) and §7 (line 1062): `L2_REFUSAL_ENABLED = False` guarding the comment now at ow:1309-1310 (Read: the commented refusal is at 1309-1310, `l2_status` call 1311, `l2_notes` 1312). Test pattern `importlib.util.spec_from_file_location` at `test_issue_orca_worktree.py` 1954-1957 (Read), `run_launch` def at 1289. Matches seed brief line 77 ("a constant, an environment variable, or a file"). 6.11 and SC-29 test both states. | none |
| 14 | `$'core.hooks\x50ath'` via `-c` | yes | Step 5.4(b) (line 1157) refuses raw `$'` in `-c`/`--config-env`/`GIT_CONFIG_*` values; guard line 431 (Read) is the `T=` sed that deletes the `$` before a quote, as claimed. SC-27 tests escaped and plain forms. | none |
| 15 | Unlisted wrappers at guard line 549 | yes | G-44 (line 698), step 5.3(b) (line 1156), SC-28 (line 599), row 8 (line 1323), §8.8 (line 1243), §7 row (line 1046). Guard line 549 (Read) lists exactly the wrappers quoted, without `chrt`, `taskset`, `find`, `uv`; line 637 is the command-position check. | **N-B (IMPORTANT)**: G-44 severity contradicts the report's own rule (see below). |
| 16 | `W-L2-ABSENT` masked in `detail` | yes | G-45 (line 699), step 4.3a (line 1143), 6.11 (line 1178), §8.8 (line 1244). Read ow:1205-1207 (`warning = notes[0][0]`, later codes as `also <code>`) and ow:1219 (`base.update(fields)`); test line 1554 asserts `"; also W-L2-ABSENT: "` in `detail` with test def at 1546. | none |
| 17 | G5 setup in prose only | yes | Fix run X2 (`qa/qa-fix-log.md` line 19): hook body and push command given verbatim, output `REC[6]: HEAD@{0 days ago} ... refs/heads/main 0000...`, `rc=0`; sandbox `/tmp/qa-fix-g3.aoYdP9rl` created with `mktemp -d`, `CLEANED=yes` (line 14). Cited by Phase 1.5, 6.2, 7.1, BP-14. | MINOR M-4 (abridged command column; `run.sh` not retained). |
| 18 | Naive-read let-through only inferred | yes | Fix run X3 (fix-log line 20): naive hook saw `field3=[ago}]`, `rc=0`, remote before no refs, after `refs/heads/main 0258722...`. Report 1.5 (line 1102) and BP-14 (line 718) now say "executed". | none |
| 19 | "Proven end to end" without remote-ref evidence | yes | Fix run X4 (fix-log line 21): `install ok mode 0o755`, `EEXIST unchanged: True`, both main pushes `rc=1` with no refs before or after, feature push `rc=0` creating `refs/heads/feature`. Test guard uses `$(NF-1)` (right-split field 3), so it is a valid stand-in. Step 2.1 cites X4 for refs and web-02 for exit codes. | none |
| 20 | §2.5 source note lacks isolation and ambient variables | yes | Line 316 names `HOME=$S/home`, `GIT_CONFIG_NOSYSTEM=1`, the ambient `GIT_CONFIG_COUNT=2` credential keys, `GIT_ASKPASS`, `GIT_EDITOR`, `GIT_TERMINAL_PROMPT`, `CLAUDECODE`, `CCSESSION_LAUNCH_ID`; 04 lines 9-13 (Read) state the same; helper scripts at 04 lines 83-147 (Read: `hook-logging.sh` begins at 83, `x.sh` ends by 147). | none |

**Blocking findings confirmed fixed: 20 / 20.**

## New Issues Introduced by the Fixes

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| N-A | IMPORTANT | §8 steps 1.2, 2.1, 2.5, 4.1, 4.2 (lines 1099, 1115, 1119, 1141, 1142); SC-24 (line 595) | The fix for #1 adds `<hooks-dir>/pre-push.uv-dir` as a new trust input, and no step verifies it. The hook accepts the file if it holds "exactly one absolute directory path in which `uv` is an executable file" (1.2), and that directory's `uv` then runs the selector under the fixed PATH. Step 2.5's ownership check (full bytes, owner, mode, `X_OK`, noexec) covers only `pre-push`. Step 4.2 grants `("present-owned", None)` "only after the Phase 2.4-2.5 checks and the L2 version line" pass, which does not include the uv-dir file. Step 2.1 only reports a *stale* file (no executable `uv`). A same-user writer, for example an in-process script that L1 cannot see, can point the file at a directory holding a fake `uv` that answers `ordinary`. The pre-launch recheck (4.1, the G-8 answer) would still report `present-owned`, so the tamper persists across launches undetected, unlike a replaced `pre-push`, which 2.5 catches as `not-owned`. 4.2 also lists `uv-dir-missing` in its closed set but gives `l2_status` no step that checks the file, so SC-24's "`l2_status` returns `absent` with reason `uv-dir-missing`" has no implementing step. | Extend 2.5 and 4.2 (and SC-18/SC-24) to verify `pre-push.uv-dir` on every launch: a regular `O_NOFOLLOW` file owned by the current user, not group- or other-writable, with content equal to the value recorded at install. The named directory and its `uv` must be owned by the user or root and not group- or other-writable. Map each failure to `uv-dir-missing` or `not-owned`. Name the file in the 5.1 token rationale. Or state this as an accepted limit in §7 with the reason. |
| N-B | IMPORTANT | §4.1 G-44 (line 698) vs severity rule (line 649) and L1-5 (line 728) | G-44 is rated "Important (rated by this QA under the rule above: L2 still refuses unless `--no-verify` is also given, which this form carries)". The parenthesis admits that the example form (`chrt 0 git $'\x70ush' --no-verify origin main`) removes L2 and passes L1. That meets the line-649 Critical definition: a governed push to main succeeds with no layer refusing it, using an ordinary command. L1-5, the same bypass class with an underscore prefix, is rated Critical at line 728. The added gap therefore understates a full guard bypass and contradicts the report's own rule. | Rate G-44 Critical and reword the parenthesis, or explain why the line-649 rule does not apply. |

### Minor notes (non-blocking; recorded only)

| # | Location | Note |
|---|---|---|
| M-1 | Step 2.8 (line 1122) vs 2.1 (line 1115) and §8.10 (line 1292) | 2.8 uses `rename` over `pre-push` and calls it "the only replacing operation". 2.1 says "Do not use `rename`" and §8.10 says "never `rename` (Phase 2.1)", with no exception noted. A foreign file written between 2.8's hash re-read and its `rename` would be overwritten. The window is narrow, but name the exception in 2.1 and §8.10 and state the window. |
| M-2 | Tag key (line 27) | `[OBSERVED 2.47.3]` is defined as "file 04 or a web-file sandbox run", but T-4 (line 499) and others now use it for QA fix runs X1-X4 (`qa/qa-fix-log.md`). Extend the key. |
| M-3 | L-2 row (line 556) | Does not cite fix run X1, unlike the other `--path-format` locations. |
| M-4 | `qa/qa-fix-log.md` lines 14-21 | The X1-X4 command column is "abridged" and `run.sh` was deleted with the sandbox. Hook bodies and outputs are verbatim, so the evidence is usable, but it cannot be replayed byte for byte. |
| M-5 | §10.4 (lines 1430-1459), §10.5 (line 1467) | The Evidence Trail lists 24 QA files "at assembly time". The Gate 3 files the report now cites as evidence (`qa/qa-fix-log.md`, `qa/qa-lens-domain-accuracy.md`) appear only via the "see `qa/`" pointer. Line 1467 counts 43 gaps while §4 and §8.8 now run to G-45. |

## Changed-section recheck

| Check | Result | Evidence |
|---|---|---|
| Template conformance (§8 phase tables: Goal, Dependencies, Step/Action/Files/Details/Done when) | PASS | All seven phases read in full (lines 1091-1194) |
| Internal consistency of changed sections | FAIL | N-A (4.2 vs SC-24 vs 2.5), N-B (G-44 vs line 649 / L1-5); M-1 (2.8 vs 2.1 / §8.10) |
| Evidence quality (file:line, official URL or recorded `/tmp` command) | PASS with notes | 24 code citations spot-checked by Read/Grep/Bash, all matched; X1-X4 recorded in `qa/qa-fix-log.md` lines 14-21 (M-4) |
| Leftover markers | PASS | Grep `\[CONTRADICTION` = 0 matches |
| Gap mapping completeness | PASS | §8.8 rows for G-1 to G-45 (lines 1198-1244); G-44 also in row 8 |

## Summary

- Blocking findings checked: 20; fixed: 20; still failing: 0
- New issues: CRITICAL 0, IMPORTANT 2 (N-A, N-B), MINOR 5 (M-1 to M-5)
- Issues fixed in place: 0 (fix authorization false)
- Monotonicity: |F_0| = 20 blocking, |F_1| = 2 blocking (strictly smaller); no item that passed earlier regressed. The 2-cycle cap allows one more fix cycle.

## Confidence

- **Confidence:** Verified: 25/25 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (20 blocking findings + 5 changed-section checks)
- **Tool engagement:** Read: 21 | Grep: 9 | Glob: 0 | Bash: 6 (Read count includes the input reads made before context compaction; approximate by ±2). No web research was performed (no tavily or web fallback calls).
- Unchecked items: none. Unverifiable items: none.

## Recommendations

1. Fix N-A: add the uv-dir file to the 2.5 and 4.2 checks and to SC-18/SC-24, or document it in §7 as an accepted limit with the reason.
2. Fix N-B: re-rate G-44 to Critical, or justify the exception.
3. Optionally fold in M-1 to M-5.
4. Re-verify in cycle 1. This is the last cycle allowed before escalating to the user.

## QA Complete

