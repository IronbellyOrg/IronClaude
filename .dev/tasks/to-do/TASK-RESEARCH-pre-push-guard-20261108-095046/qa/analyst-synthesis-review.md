# Synthesis Quality Review (accuracy lens, adversarial)

**Date:** 2026-11-08
**Analysis type:** synthesis-review
**Files reviewed:** 4 synthesis files (`synthesis/synth-01` to `synth-04`)
**Research files checked against:** `research/01-04`, `research/web-01`, `research/web-02`, `gaps-and-questions.md`
**Fix authorization:** false (report only)

**Also checked:** the seed brief (`.dev/brainstorms/20261108-094705-l2-pre-push-guard/seed-brief.md`, lines 68-78) and whether the test files named in the synthesis exist under `tests/hooks/`.

## Overall Verdict: FAIL — 8 issues (0 CRITICAL, 2 IMPORTANT, 6 MINOR)

Two IMPORTANT cross-file inconsistencies block assembly as written:

- The synthesis files disagree on the order of the pre-push stdin records (F1).
- They disagree on whether the IR-7 switch is decided and must be built (F2).

No fabricated content was found. Every claim checked could be traced to a research file, `gaps-and-questions.md`, the seed brief or an existing repository file.

## Per-File Review

### synth-01-problem-current-state.md

**Sections covered:** S1 Problem Statement, S2 Current State Analysis
**Verdict:** FAIL (it shares F1)

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match the template | PASS (minor note) | S1 and S2 are present. The embedded "Items for Open Questions" table is not a template section (F7). |
| 2 | Table column structure | PASS | The S2 tables are descriptive, and the template prescribes no fixed columns for S1 and S2. |
| 3 | No fabrication | PASS | Spot-checked rows trace to 01 (lines 104-110, 236), 02, 03 and 04. |
| 4 | Findings cite paths and evidence | PASS | It cites ow:/line references, 01 §N and the 04 E-numbers. The "01 §5" citation at line 210 for PID namespace and boot_id is plausible, because §5 holds the validation fields. |
| 5 | Options (n/a for S1-S2) | N/A | |
| 6 | Plan with paths (n/a) | N/A | |
| 7 | Cross-reference consistency | FAIL | Lines 309 and 330 say "Stdin order is not command-line order (E9, E19, E24a/b)". This contradicts synth-03's G-24 mapping (line 316) and synth-04 row 22 (F1). |
| 8 | No [UNVERIFIED] §19 git claims as fact in S2 | PASS | The [UNVERIFIED] items are tagged as such (line 210). |
| 9 | CODE-CONTRADICTED / STALE DOC surfaced | PASS | The LL-UNKNOWN line 80 and LL-TAMPER line 95 contradictions from 02 are carried. |
| 10 | Key takeaways reflected | PASS | 01: session-based selection, the unknown mapping and the no-uv exit 2. 02: the L1 gaps. 03: `l2_status` and W-L2-ABSENT. 04: field 3 and the bypasses. All are present. |

### synth-02-target-gaps-external.md

**Sections covered:** S3 Target State, S4 Gap Analysis, S5 External Research Findings
**Verdict:** FAIL (it shares F1; also part of F6, minor)

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match the template | PASS | S3, S4 and S5 are present. |
| 2 | Table column structure | PASS | The S4 rows use Gap/Current/Target/Severity (plus an evidence column), for example line 202. |
| 3 | No fabrication | PASS | The web rows trace to web-01 and web-02 (65 hits for web-02 terms across synth-02, synth-03 and synth-04; `ignoredHook`, `noexec` and `fsync` are all carried). |
| 4 | Findings cite paths and evidence | PASS | |
| 5 | Options (n/a) | N/A | |
| 6 | Plan (n/a) | N/A | |
| 7 | Cross-reference consistency | FAIL | G-24 (line 194) says "Not command order (E9, E19, E24)". W1-21 (line 304) says "In one dry-run test, records came in command-line order". synth-02 holds both observations without reconciling them, and synth-03 marks G-24 resolved in the opposite direction (F1). |
| 8 | No [UNVERIFIED] claims as fact | PASS | S3 is a target, and the D19 claims carry their tags. |
| 9 | CODE-CONTRADICTED / STALE DOC surfaced | PASS | The DOC rows carry D19-16, D19-18, 19.6 lines 538-543 and IR-7 lines 355/514. |
| 10 | Key takeaways reflected | PASS | web-01 Key External Findings (six fields, `rsplit`, bypassing libraries) and all ten web-02 Key External Findings (lines 362-372: `access(X_OK)` fail-open, `advice.ignoredHook`, `noexec`, `fchmod` versus umask, `link` EEXIST, no `O_TMPFILE` on overlay below 6.10, fsync) are reflected. |

### synth-03-options-recommendation-plan.md

**Sections covered:** S6 Options Analysis, S7 Recommendation, S8 Implementation Plan, the G-1 to G-43 mapping and OQ-1 to OQ-17
**Verdict:** FAIL (F1, F2; minor F3, F7)

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match the template | PASS (minor note) | S6, S7 and S8 are present. It adds an extra "Open Questions (deferred from Sections 6-8)" table (OQ-1 to OQ-17, columns ID/Question/Gap/Why) that duplicates S9 (F7). |
| 2 | Table column structure | PASS | The comparison table is Criterion/Option A/B/C. The Phase 1-7 tables are Step/Action/Files/Details. |
| 3 | No fabrication | PASS | The one-line refusal at line 248 matches 03 (ow:1309-1310 comment). The test citation 934-1003 matches 01 line 270. |
| 4 | Findings cite paths and evidence | FAIL (minor) | Wrong section citations: "01 §3" for `publish()` and the ownership check (they are in 01 §6); "01 §5" for the entry point and three copies (01 §8); Phase 1.9 attributes `GUARD_VERSION_LINE` ow:804 to "03" (it is 01 line 247) (F3). |
| 5 | At least 2 options with pros/cons | PASS | Options A, B and C, with a comparison table. |
| 6 | Plan with specific file paths | PASS | Phases 1-7 name `orca_worktree.py` lines, `install_hooks.py`, the hook scripts, the tests and the design lines. |
| 7 | Cross-reference consistency | FAIL | (a) The G-24 mapping (line 316) says "Resolved by web research: order followed the command line in tests", which contradicts synth-01 lines 309/330 and synth-02 line 194 (F1). (b) G-17 / IR-7 is treated as undecided and Phase 4.4 as conditional (lines 179, 248, 309, 369), but synth-04 R3 and the seed brief say the default is decided and the refusal path must be built (F2). |
| 8 | No [UNVERIFIED] §19 git claims as fact in S6-S8 | PASS | The Option C actor cases cite the design and carry their tags. The plan steps rest on 04 experiments or on web-01/web-02. |
| 9 | CODE-CONTRADICTED / STALE DOC surfaced | PASS | D19-18 [CODE-CONTRADICTED] (line 179) and OQ-7 [STALE DOC] (line 369). |
| 10 | Key takeaways reflected | PASS | The traceability table (line 389 and nearby) maps every research file's takeaways to plan steps. web-02 Recommendation 1 (temp, `fchmod`, `fsync`, `link`, fsync of the directory) is in the plan. |

### synth-04-questions-evidence.md

**Sections covered:** S9 Open Questions, S10 Evidence Trail
**Verdict:** FAIL (F1, F2; minor F4, F5, F6, F8)

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 1 | Section headers match the template | PASS | S9 and S10 are present. |
| 2 | Table column structure | PASS | The 9.x rows use #/Question/Impact/Suggested Resolution. |
| 3 | No fabrication | PASS (minor note) | The seed-brief claims in rows 12, 15, 18 and 27 and in R2/R3 (lines 74, 75, 77) were verified against the seed brief. The test files `tests/hooks/test_launch_level_guard.py` and `test_launch_level_observations.py` exist in the repository. Neither source comes from the research files (F4, F8). |
| 4 | Findings cite paths and evidence | FAIL (minor) | Row 22 attributes the command-order observation to "one test (04)". That observation is web-01 G3 (line 226); in 04 only E7 (line 549) is a loose match, and E24 (line 1339) shows order independent of the command line (F1). |
| 5 | Options (n/a) | N/A | |
| 6 | Plan (n/a) | N/A | |
| 7 | Cross-reference consistency | FAIL | (a) R3 / row 12 say IR-7 is DECIDED off and the refusal path is built in a separate commit, while synth-03 Phase 4.4 says it is built "only if the owner chooses" (F2). (b) R4 says "Yes, they bypass it", while synth-02 keeps the D19-30 API part open for runtime confirmation (F6). (c) Table 9.4 (lines 83-90, 4 rows) omits the stdin-order contradiction (F1). |
| 8 | No [UNVERIFIED] claims as fact | PASS | |
| 9 | CODE-CONTRADICTED / STALE DOC surfaced | PASS | Rows 8, 9, 12, 13, 16, 20 and 21 carry D19-16, D19-18, LL-UNKNOWN line 80, LL-TAMPER line 95, 19.6 and IR-7. |
| 10 | Key takeaways reflected | FAIL (minor) | The Evidence Trail row for 04 (line 103) says "E1-E31, F1-F3", but 04 runs F0-F4, and F4 (line 2126: pre-push adds no local commit/merge restriction, confirming D19-29) is a Key Takeaway (line 2245 and nearby) (F5). |

## Issues Requiring Fixes

| # | Severity | Synth file and section | Finding | Research evidence | Proposed fix |
|---|----------|------------------------|---------|-------------------|--------------|
| F1 | IMPORTANT | synth-03 G-24 mapping (line 316); synth-04 row 22 (line 43) and table 9.4 (lines 83-90); synth-01 lines 309, 330; synth-02 G-24 (line 194) and W1-21 (line 304) | The files contradict each other on stdin record order. synth-01 and synth-02 G-24 say it is not command order. synth-03 says G-24 is "resolved" because order "followed the command line in tests". synth-04 row 22 credits the command-order test to 04. Table 9.4 does not record the contradiction. | 04 E7 (line 549): "in command-line order here". 04 E9 (line 702): neither alphabetical nor local-ref order. 04 E24 (line 1339): "identical in both runs and independent of command-line order". 04 Gaps (line 2249): "E9, E19 and E24 show that order is not command order". web-01 G3 (line 226): one dry-run of all creates, "only one observation". web-01 line 471: "no order is documented". | In every file, state that order is undocumented and varies: simple creates followed the command line (04 E7, web-01 G3), while E9, E19 and E24 did not. Mark G-24 resolved only as "the hook must not depend on order". Fix the attribution in row 22. Add a 9.4 row for 04 versus web-01. |
| F2 | IMPORTANT | synth-03 lines 179, 248 (Phase 4.4), 285 (7.5), 309, 350, 369 (OQ-7) versus synth-04 R3 (line 77) and row 12 | synth-03 treats IR-7 as an open owner choice (refuse or warn) and builds the refusal step "only if the owner chooses". The seed brief has decided the default (off, W-L2-ABSENT stays a warning, separate clearly marked commit), and its success criterion requires that "the IR-7 refusal path exists and is tested, ships switched off". synth-04 R3 records this; synth-03 does not, so the plan lacks a required step. | Seed brief line 68 (success criterion) and line 77 (default DECIDED off; mechanism and turn-on condition after #442 still open). 03 raised IR-7 as an owner question, and the seed-brief decision supersedes it. | Rewrite Phase 4.4 as unconditional: build the refusal path behind a switch that defaults off, in its own clearly marked commit, with a test for each switch state. Leave open only the switch mechanism and the turn-on condition (OQ-7). Align 7.5, the G-17 mapping and the line-350 checklist with that. |
| F3 | MINOR | synth-03 Phase 1.1, 1.3, 1.9, 2.1, 2.4-2.6 (lines 205-276) | Wrong research-section citations. `publish()` and the ownership check are cited as "01 §3" (they are in §6). The entry point and three copies are cited as "01 §5" (they are in §8). `GUARD_VERSION_LINE` ow:804 is attributed to "03". | 01 §6 covers publish() and ownership. 01 §8 covers dependencies. 01 line 247 gives ow:804 and line 269 gives ow:803 `IDENTITY_COMMAND`. | Change the citations to 01 §6, 01 §8 and "01 line 247". |
| F4 | MINOR | synth-04 rows 7, 8, 29 (`tests/hooks/test_launch_level_guard.py`) and row 27 (`tests/hooks/test_launch_level_observations.py`) | These test files exist in the repository, but no research file names them. synth-03 Phase 6.7 puts the L1 tests in `test_launch_level_guard_with_identity.py`, so the two files point to different test homes. | 01 line 270 names `test_launch_job_identity.py`, `test_launch_level_guard_with_identity.py` and `test_install_hooks.py`. 02 names no L1 test file. | Pick one test file for each check and use it in both synth-03 and synth-04, or label the synth-04 names as a proposal not drawn from the research. |
| F5 | MINOR | synth-04 §10 Evidence Trail, row for 04 (line 103) | It says "E1-E31, F1-F3". 04 also has F0 and F4, and F4 (no local commit/merge restriction from pre-push) is a Key Takeaway. | 04 F4 (line 2126); Key Takeaways (lines 2233-2245). | Change the range to "E0-E31, F0-F4" and add the F4 result to the key-finding cell. |
| F6 | MINOR | synth-04 R4 versus synth-02 §4.5 (D19-30) | R4 says the question is resolved ("Yes, they bypass it"). synth-02 keeps the API part of D19-30 open for runtime confirmation. | 04 Step 2.5 routes the D19-30 API part to web-01. web-01 J11 is documentary evidence only, with no runtime test. | In R4, say "documented to bypass (web-01); not observed at runtime", or close the item in synth-02 as well. |
| F7 | MINOR | synth-03 "Open Questions (deferred from Sections 6-8)" (OQ-1 to OQ-17); synth-01 "Items for Open Questions" | These non-template sections duplicate S9 with different columns (ID/Question/Gap/Why), so the assembler may produce two open-question lists. | Template S9 columns: #/Question/Impact/Suggested Resolution. | Move the OQ items into synth-04 S9 (or check that S9 already covers them) and remove or label the in-file tables as working notes that are not for assembly. |
| F8 | MINOR | synth-04 §9 rows that rest on Gate 1 QA reports (F1/F8, N-2, N16, fix-log B1-B4) and seed-brief lines 74, 75, 77 | Some content comes from sources other than the research files. The seed-brief lines were verified as accurate, but the QA-report sources are not marked as such in the rows. | Research cites the seed brief only at lines 22-25, 39, 45, 73, 76, 78. The QA reports are not research files. | Tag those rows with their source (seed brief, or a QA report through `gaps-and-questions.md`) so the assembler can see where each one comes from. |

**Research-side note (not a synthesis defect):** 04 Gaps lines 2255-2256 are stale against 04 line 2262 and against the F-series results. The synthesis files do not repeat that stale text.

## Summary

- Files reviewed: 4
- Files passed: 0
- Files failed: 4 (each shares at least one IMPORTANT finding)
- Total issues: 8
- CRITICAL: 0
- IMPORTANT: 2 (F1 stdin-order contradiction; F2 IR-7 decided versus conditional)
- MINOR: 6 (F3-F8)
- Criteria passing in all files: 5 (options), 6 (plan paths), 8 (no [UNVERIFIED] claims as fact), 9 (CODE-CONTRADICTED / STALE DOC surfaced)
- Critical issues that block assembly: 0. Assembly should wait until F1 and F2 are fixed, because both would put contradictory statements into the final report.
