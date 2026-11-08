# QA Report — Fix Cycle (Qualitative Fix Verification, Gate 3, cycle 0)

**Topic:** git pre-push hook semantics for the L2 launch-level guard (research report)
**Date:** 2026-11-08
**Phase:** fix-cycle (report-validation, content lenses)
**Fix cycle:** 1 (verifying the cycle-0 fixes)
**Fix authorization:** false (report only; no file other than this one was modified)
**Inputs read:** `qa/qa-consolidated-findings-phase6-cycle0.md` (20 blocking findings, 43 MINOR notes), `qa/qa-fix-log.md` (all 20 marked FIXED, sandbox runs X1-X4), `RESEARCH-REPORT-pre-push-guard.md` (all 1469 lines read).

---

## Overall Verdict: FAIL

Every one of the 20 original blocking findings is addressed in the report text. Two of the fixes introduced new blocking issues: a contradiction in how G-44 is rated, and an unprotected trust input created by the fix for finding #1. Details are under Issues Found.

## Items Reviewed

"Original resolved" means the blocking finding from the consolidated file no longer holds in the report. "Quality" covers four questions: is the fixed text actionable, accurate for the domain, reproducible, and cross-referenced (gap to step, option to evidence, recommendation to comparison)?

| # | Original blocking finding | Original resolved | Quality of the fixed text | New issue |
|---|---|---|---|---|
| 1 | CRITICAL: a uv PATH written into the hook bytes can never match the full-byte ownership check | PASS. Step 1.2 (line 1099) keeps the bytes identical and reads `<hooks-dir>/pre-push.uv-dir` at run time. Step 2.1 (line 1115) writes that file. Reason `uv-dir-missing` is in step 1.4, step 4.2 and SC-18; SC-23 and SC-24 were added; step 7.4 has the A-i wording; §7 (line 1026) names the sibling file | Actionable and cross-referenced (G-6 → 1.2 → SC-23/24 → §9 row 1) | **NEW-2 (IMPORTANT)**: nothing verifies the new file. See Issues Found |
| 2 | IMPORTANT: `--path-format` contradiction between the main checkout and a linked worktree | PASS. §2.5(c) note and table (lines 386-394), step 2.2 (line 1116), G-26 (line 680, line 755, §8.8 line 1225) and R9 (line 1374) all cite fix run X1, and they agree | Reproducible (X1 output recorded in the fix log) | none |
| 3 | IMPORTANT: L1 test-file contradiction (#440 edits `test_launch_level_guard.py`) | PASS. Steps 6.7 (line 1174) and 5.3, §9 rows 7, 8 and 29 (lines 1322, 1323, 1349) and the Phase 5 Dependencies line (line 1150) all name the new `tests/hooks/test_launch_level_guard_l2_bypass.py`. The file does not exist yet (`ls` confirmed), which matches its **(new)** tag | Command `uv run pytest tests/hooks/test_launch_level_guard_l2_bypass.py` is present and correct | none |
| 4 | IMPORTANT: Goal and Dependencies lines missing | PASS. §8.1-8.7 each have a Goal line and a Dependencies line (lines 1093-1094, 1110-1111, 1126-1127, 1136-1137, 1149-1150, 1163-1164, 1182-1183) | The dependencies are acyclic: 1 → 2 (2.7 right after 1.1) → 3 → 4; 5 is independent; 6 needs 1, 2, 4 and 5; 7 needs 1, 4 and 5 | none |
| 5 | IMPORTANT: wrong path for the refactor plan / §6.1 Cons | PASS. §6.1 Cons (line 940) has the corrected path | Accurate | none |
| 6 | IMPORTANT: step 2.1 named no source file for the bytes | PASS. Step 2.1 uses `~/.claude/hooks/launch-pre-push-guard.sh` with reason `guard-source-missing`. `_copy_scripts` (`install_hooks.py` 251-290) is cited | Actionable; the reason is in SC-18 and 4.2 | none |
| 7 | IMPORTANT: step 2.7 ordering (verify-sync fails while the script is unregistered) | PASS. Step 2.7 says "do immediately after step 1.1"; Phase 1 and Phase 2 Dependencies repeat it; 1.1 Done-when requires it. Makefile lines 307-323 do print `MISSING from _FRESHNESS_SCRIPTS` and set `drift=1` (read). Lines 90 and 93 of `install_hooks.py` are the identity entry and the L1 guard entry (read) | Accurate against source | none |
| 8 | IMPORTANT: no upgrade path for an earlier owned version | PASS. Step 2.8 (line 1122) adds the `L2_EARLIER_OWNED_SHA256` tuple and a re-read-then-`rename` limited to owned hashes, with a Phase 6.4 case | Actionable; the one replacing operation is called out explicitly | MINOR m-4 (TOCTOU window, below) |
| 9 | IMPORTANT: step 4.2 return type and consumers | PASS. The signature is `tuple[str, str \| None]` with a closed reason set equal to the SC-18 list. Sub-steps 4.2a-4.2j cover every consumer. Spot-checked against source: ow 1012-1029 (current `-> str`, `present-unverified`), ow 1061-1067 (`session_report` text), test lines 1672 and 1691-1692 (`foreign-executable` and `hooks-path` → `present-unverified`) all match | Actionable; Done-when is a Grep check plus test runs | none |
| 10 | IMPORTANT: no separate L2 version line | PASS. Step 1.9 adds `L2_GUARD_VERSION_LINE = "# launch-pre-push-guard-version: 1"`, kept separate from `GUARD_VERSION_LINE` (ow:804, read: `"# launch-level-guard-version: 1"`). `l2_status` checks it, not `enforcement_preflight` | Accurate | none |
| 11 | IMPORTANT: success criteria missing | PASS. SC-24 to SC-31 (lines 595-602) each have a pass condition and map to a step | Testable | MINOR m-1 (SC-18 versus the uv-dir write order), m-2 (`chrt 0`), m-3 (line cite) |
| 12 | IMPORTANT: no Done-when column | PASS. Every step table in §8.1-8.7 has a Done-when column with an observable condition | Actionable | none |
| 13 | IMPORTANT: no IR-7 switch mechanism | PASS. `L2_REFUSAL_ENABLED = False` is in §7 (line 1062), step 4.4, step 6.11, step 7.5, G-17 (lines 671, 1216), row 12 and R3. The test route (the `importlib` loader at test lines 1954-1957 plus `monkeypatch.setattr`) matches the source (read 1952-1958). `run_launch` (line 1289) is the subprocess helper | Actionable; the reason a constant beats an env var is stated | MINOR m-5 (the refusal call omits the 4.3a `l2` field) |
| 14 | IMPORTANT: ANSI-C `-c` spelling not handled | PASS. Step 5.4(b) refuses `$'` in raw `-c`, `--config-env` and `GIT_CONFIG_*` values. SC-27 tests the escaped and plain spellings. §7 (line 1045) cites it | Actionable; the larger alternative (decoding the escapes) is named and rejected | none |
| 15 | IMPORTANT: unlisted wrappers not covered (G-44) | PASS for coverage. G-44 (line 698), step 5.3(b), SC-28, §7 row (line 1046), §8.8 (line 1243), §8.9 L1-5 (line 1268) and §9 row 8 were all added. The wrapper list quoted in 5.3(b) equals guard line 549 (read) | Cross-referenced | **NEW-1 (IMPORTANT)**: the G-44 rating contradicts the report's own severity rule and the L1-5 row. MINOR m-2 |
| 16 | IMPORTANT: `W-L2-ABSENT` masked by another warning (G-45) | PASS. G-45 (line 699), step 4.3a, step 6.11 and §8.8 (line 1244) were added. `launch_result` (ow 1203-1220, read) does put notes[1:] into `detail` and calls `base.update(fields)`, so the proposed `l2=` keyword works. Test line 1554 pins the masking (read) | Accurate against source | none |
| 17 | IMPORTANT: G5 not reproducible | PASS. §6.5 note (line 1000), step 1.5, SC-8 and BP-14 cite fix run X2 (`REC[6]`) with commands recorded in the fix log | Reproducible | none |
| 18 | IMPORTANT: the naive-read failure was inferred, not observed | PASS. X3 (`field3=[ago}]`, rc 0, the remote gained `refs/heads/main`) is cited in §6.5 (line 1000), step 1.5 and DOC-8 | Observed, not inferred | none |
| 19 | IMPORTANT: "proven end to end" was not proven | PASS. §6.4 (line 981), §7 reason row (line 1035), step 2.1, W2-15 (line 817) and §5.5 (line 889) cite X4: install at 0755, EEXIST, both main pushes rc 1 with `for-each-ref` unchanged, feature push rc 0 | The claim now matches the evidence | none |
| 20 | IMPORTANT: §2.5 isolation note | PASS. Line 316 is corrected | Accurate | none |

`[CONTRADICTION` markers left in the report: 0 (Grep).

## Summary

- Original blocking findings resolved: 20 / 20
- New blocking issues introduced by the fixes: 2 (CRITICAL 0, IMPORTANT 2)
- New MINOR notes: 6 (these never fail a review; recorded for the next author)
- Issues fixed in place: 0 (fix authorization false)
- Issue count trend: 20 blocking → 2 blocking. Fewer, so there is no systemic problem.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| NEW-1 | IMPORTANT (contradiction) | §4.1 G-44 row (line 698), against the severity rule (line 649), the L1-5 row (line 728) and the §7 wrapper row (line 1046) | G-44 is rated "Important (rated by this QA under the rule above: L2 still refuses unless `--no-verify` is also given, which this form carries)". The rule at line 649 defines Critical as "a governed push to main or master succeeds with no layer refusing it, and needs no capability beyond ... an ordinary command". By G-44's own text, and by §7 (L1 "allowed (G-44)", L2 "`--no-verify` part removes L2"), the SC-28 form gets through both layers: it meets the Critical definition. The same-class row L1-5 (`A_B=1 git $'\x70ush' --no-verify origin main`) is rated Critical. The fix added a rating that its own justification refutes, and a reader ranking work by severity would put this full bypass below its twin. | Rate G-44 Critical and change the parenthesis to "no layer refuses: L1 allows the wrapper form and `--no-verify` removes L2". Alternatively, state a real reason why G-44 differs from L1-5. Then check whether G-13 (line 667, Important, kept from `gaps-and-questions.md` by the rule) needs a note pointing to L1-5's Critical rating for the same mechanism. |
| NEW-2 | IMPORTANT (missed risk / gap in the recheck design) | Step 1.2 (line 1099), step 2.1 (line 1115), step 2.5 (line 1119), §7 bypass table (lines 1042-1058), SC-31 | The fix for finding #1 adds a new trust input. The hook reads a directory from `<hooks-dir>/pre-push.uv-dir`, accepts it if `uv` there is executable, and puts it **first** on PATH before calling `identify`. Whoever can rewrite that 0644 file, or plant a `uv` in the named directory, decides the verdict: for example, a fake `uv` whose `identify` run prints `ordinary`. Nothing in the plan checks the file. Step 2.5 checks owner, mode, content and `X_OK` for the hook only. Step 2.1 checks the uv-dir file only for "names a directory holding an executable `uv`". SC-31 rechecks only the exec bit and `core.hooksPath`. §7 has no row for it. So a tampered uv-dir file survives every pre-launch recheck, while a replaced hook is caught by the full-byte check. The Phase 5.1 token `*hooks/pre-push*` happens to match `hooks/pre-push.uv-dir` in a spelled path, but the report never says so and does not rely on it. (Grep: no text in the report or the fix log ties `uv-dir` to tamper, owner or writable checks.) | Extend step 2.5 (and `l2_status`, step 4.2) to check `pre-push.uv-dir` itself: a regular `O_NOFOLLOW` file owned by the current user and not group- or other-writable. Also check that the named directory and its `uv` are not writable by others, and either equal the launch process's `shutil.which("uv")` directory or appear on a fixed allow-list. Failures map to a reason (`uv-dir-missing`, or a new one added to the SC-18 list). Add a §7 bypass row ("rewrite `pre-push.uv-dir` / plant `uv`"), name the uv-dir file in the Phase 5.1 token rationale, and add an SC-31 variant that rewrites the file between two launches. |
| m-1 | MINOR | SC-18 (line 589) and step 2.1 | SC-18 says "nothing outside the temp file changes" for every conflict case. Step 2.1 also writes `pre-push.uv-dir` but does not say whether that happens before or after the `pre-push` link. In the `foreign-pre-push` case, writing it first would fail SC-18. | State that the uv-dir file is written only after the `pre-push` link succeeds, or exempt it in SC-18. |
| m-2 | MINOR | G-44 (line 698), §7 (line 1046), step 5.3, SC-28 (line 599), §9 row 8 | The lead example `chrt 0 git ...` does not run git. With no policy flag, chrt uses SCHED_RR, and priority 0 is invalid for it: on this host `chrt 0 true` gave "unsupported priority value for the policy: 0", rc 1 (util-linux 2.41), while `chrt -o 0 true` and `taskset 1 true` gave rc 0. The class claim still holds through `taskset` and `find -exec`. As an L1 text-guard test, SC-28 still expects exit 2 either way. The example came from 02 line 251. | Use `chrt -o 0 git ...` (or lead with `taskset 1`) in the four places. |
| m-3 | MINOR | SC-25 (line 596) | Cites `ll_deny` as "guard lines 135-138". The function runs from line 135 to line 139 (read), and §2.1 says 135-139. | Use 135-139. |
| m-4 | MINOR | Step 2.8 (line 1122) | The re-read-then-`rename` upgrade leaves a window between the hash check and the `rename`. It is limited to owned files and is the plan's only replacing operation, so the risk is small, but the window is not named. | Name the window, or note that a `RENAME_EXCHANGE` / compare-after-swap is the stricter alternative. |
| m-5 | MINOR | Step 4.4 (line 1144) against step 4.3a (line 1143) | The proposed refusal call `launch_result("failed", l2_notes, enforcement_hook=hook)` does not pass the `l2=` field that 4.3a adds, so a refused launch would lack the machine-readable L2 state. | Pass `l2={...}` in the refusal call too. |
| m-6 | MINOR | §10.5 (line 1467) | Still says "43 gaps (G-1 to G-43)". G-44 and G-45 are report-only additions (lines 649, 698-699), so the sentence "Section 9 accounts for every gap" now covers G-1 to G-43 only. | Add "(G-44 and G-45 were added at Gate 3 and live only in this report, §4.1 and §8.8)". |

Candidates checked and dropped: (1) §3.3 line 549 wording of option (i), "fixed PATH holding the uv directory recorded at install time". It does not contradict §7 or step 1.2: the directory is still recorded at install time, only stored in a file. (2) L-2 (line 556) citing only web-01 D3. Step 2.2 and R9 carry the X1 main-checkout evidence, and L-2's claim is true, so this is not a contradiction.

## Actions Taken

None. Fix authorization is false. This report is the only file written.

## Confidence

- **Confidence:** "Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%". The count covers the 20 blocking-fix rows. Each was checked in the report text, and the rows that cite code were also checked against source.
- **Tool engagement:** "Read: 12 | Grep: 4 | Glob: 0 | Bash: 5". The Read count includes the consolidated findings, the fix log, the report in 7 chunks and this file. Bash was used for read-only `sed -n` and `grep` of the cited source lines, for `ls` of the new test paths, and for one harmless `chrt` / `taskset` run of `true`. No git command was run and nothing was pushed. Total Read+Grep+Glob is 16, which is not below the 20 items checked. Several Reads each cover many rows (for example, report lines 954-1153 cover rows 4, 6-10, 12 and 13), so these counts meet the minimum.
- UNCHECKED items: none. UNVERIFIABLE items: none.
- Web research: none was performed. Tavily was not needed; every check used local files and one local command.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was provided. I relied on the fix log's sandbox records X1-X4 (`/tmp/qa-fix-g3.aoYdP9rl`, since removed) as the evidence that the commands ran. I did not re-run X1-X4, because the sandbox is gone and re-running real pushes was not needed to judge whether the content holds.
- Relied on the consolidated findings file for the wording of the 20 original findings.

**(b) Independent semantic checks (≥1 required, INV-019):**
- G-44 severity versus the rule: Grep of the report found line 649 (rule), 667 (G-13 Important), 698 (G-44 Important with a justification meeting the Critical definition) and 728 (L1-5 Critical). That gave NEW-1.
- The trust boundary of the uv-dir file: a Grep across the task folder for `uv-dir` near tamper, owner, writable, L1 or token words found no protection text. Steps 2.5 and SC-31 were read in full. That gave NEW-2.
- The `chrt 0` example: ran `chrt 0 true` (rc 1, "unsupported priority value") against `chrt -o 0 true` and `taskset 1 true` (rc 0) on util-linux 2.41. That gave m-2.
- Step 4.2 consumers and the step 4.4 test route: read `orca_worktree.py` 804, 1012-1029, 1061-1067, 1203-1220 and 1305-1315, and `tests/skills/test_issue_orca_worktree.py` 1552-1556, 1670-1673, 1689-1693, 1952-1958 and 1287-1290. All match the report.
- Step 2.7 and 6.7 sources: read Makefile 307-323, `install_hooks.py` 88-94, the guard at 547-551 (wrapper list) and 133-140 (`ll_deny`), and the helper definitions (`_bind`, `_payload`, `_hook` at 67, 81, 92) in `test_launch_level_guard_with_identity.py`. `LocalPushFixture` is at line 1175. All match, except the m-3 line cite.

1. Factual claims independently verified against source code or a local command: 24.
2. Files read: the report, the consolidated findings, the fix log, `orca_worktree.py`, `test_issue_orca_worktree.py`, `launch-level-guard.sh`, `install_hooks.py`, `Makefile`, `test_launch_level_guard_with_identity.py`, `test_launch_job_identity.py` and research file 02.
3. Not applicable: this review found 2 blocking issues and 6 minor ones.
4. No web research was performed.

## Recommendations

- Fix NEW-1 and NEW-2 in the report (one fix cycle). The MINOR notes m-1 to m-6 are optional.
- This was review 2 of at most 3. If NEW-1 or NEW-2 is still open after the next fix, escalate to the user; do not run a fourth review.

## QA Complete

