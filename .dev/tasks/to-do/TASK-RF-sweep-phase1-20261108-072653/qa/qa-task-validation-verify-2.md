# QA Report: Task integrity, fix verification (cycle 2, final review 3 of 3)

**Task file:** TASK-RF-sweep-phase1-20261108-072653.md (2863 lines, 351 items, no duplicate ids)
**Date:** 2026-11-08
**Phase:** task-integrity, lens fix-verification
**Fix cycle:** 2
**fix_authorization:** false (report only; the task file was not edited)

Status: COMPLETE

## Overall Verdict: FAIL

All 6 input findings (V-01, V-02, I-1 to I-4) are gone. The I-1 fix added one new blocking defect, N-01: items 5.1, 5.3, 5.11 and 5.12 put DESIGN line 835 (row 1.17, "The REPORT's WC-14 draft") in section 14. It is in section 13. Section 14 has no WC-14 or WC-16 text, so the 5.12 pass rule "`WC-16` hits in sections ... 14 ..." cannot pass, and no item from 5.1 to 5.11 can make it pass. Open blocking count `|F_2|` = 1, against `|F_1|` = 6, so the count shrinks strictly. N-01 is a new finding, not a regression of a check that passed earlier. This is review 3 of 3, so the hard cap applies: escalate N-01 to the user and do not run a fourth review.

## Items Reviewed

| Check | Result | Evidence |
|---|---|---|
| V-01 (14.8 Branch B path) | PASS | 14.8 Action, line 2488: `blocker_reason: "OQ-10 option (B): ... and saves output plus exit code to .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/sweep-help-pipx.txt"`. This is the same path as Branch A and as Output (line 2489). |
| V-02 (impl-cli gate floor) | PASS | Title tally over the whole file: impl-cli has 5 rf-qa (9.5, 9.6, 9.7 domain, 9.8, 9.9) and 3 rf-qa-qualitative (9.10, 9.11, and the new 9.12 at line 1700, "agent 8 of 8: rf-qa-qualitative, failure-path lens"). The 9.12 Action spawns `rf-qa-qualitative` with the full report-only preamble and the lens prompt. 9.13 (line 1707) is "consolidate the eight reports" and expects "the Glob found 8 reports". The 8 Output names (lines 1654-1703) match the 9.13 list one for one. |
| I-1 (WC-14 rename coverage) | PASS for the original finding; the fix adds N-01 | `grep -n WC-14` on DESIGN gives lines 5, 13, 659, 661, 668, 677, 695, 701, 715, 777, 812, 835, 926, 953, 988 and 989. Every line now has an owning item: 5.1 covers section 8, 5.2 covers 695, 701 and 715, and 5.3 (line 780) covers "near 5, 13, 777, 926, 953, 988 and both mentions near 989", with 812 and 835 kept as `historical name (keep)` plus " (WC-16 in this design)". The DESIGN headings put line 835 in `## 13. Deviations from SPEC` (lines 801-836, the "REPORT differences" table). `## 14. Panel notes` starts at line 837. See N-01. |
| I-2 (2.7 per-section rule) | PASS | 2.7 Action, line 286, has the per-section rule: 7.2, 2.2 and 18 hold all four model names; 7.1 holds `first_record_ts`; 11 holds `first_record_ts` and the `dispatch_*` names "in the copied fixture expectations"; 15.1 and 17 hold the three dotted names. I checked this against research/04:87-117. Edits 1, 2 and 4 put all four in 7.2, edit 6 puts all four in 2.2, edit 9 puts all four in 18, edit 5 puts `first_record_ts` in 7.1, the `test_worker_show_dispatch_times_sqlite_form` "Then" cell puts all three `dispatch_*` names in 11, and edits 7 and 8 put the dotted names in 15.1 and 17. Every cell can be met. The dotted-name grep is present and the seven checks are numbered. |
| I-3 (8.3 and 8.4 field names) | PASS | 8.3 Context (line 1431): "`dispatch_started: datetime \| None`, `dispatch_ended: datetime \| None` and `dispatch_status: str \| None`, parsed from the `worker-show` JSON paths `dispatch.dispatchedAt`, `dispatch.completedAt` and `dispatch.status`" and "`first_record_ts: datetime \| None`". The 8.3 Verification (line 1434) runs a `grep -c` for each of the four, expecting 1. The 8.4 Context (line 1438) has the full window rule, including "`dispatch_status` is `pending` or `dispatched`" and the note `Dispatch time window not observable`. |
| I-4 (5.7 against 7.19 and DESIGN 1.16a) | PASS | 5.7 Action (line 808) lists four points: (1) the `gh pr view 422 --repo IronbellyOrg/IronClaude` state line (MERGED, `2327fbd3`); (2) `git merge-base --is-ancestor 2327fbd3 HEAD` succeeding; (3) `git merge-base --is-ancestor 495eb96d origin/master` failing; (4) the re-read note. These match research/09:115 word for word and match the 7.19 Action points (1) to (4) (line 1279). DESIGN step 1.16a (line 925) reads "`gh pr view 422 ... --json state,files` and the #409 diff check; results to `.dev/tasks/<pkg>/artifacts/`", with the gate "none; must finish before 1.17". The 5.7 text keeps that gate ("its gate on step 1.17 stays and is satisfied as soon as the record is written") and turns "the #409 diff check" into point (3). There is no contradiction. Notes M1 and M2 list small wording gaps. |
| Phase 9 renumbering, cross-references | PASS | Every `9.12` to `9.21` token (grep) sits inside Phase 9 (lines 1653-1763). Ranges were checked in context: 9.14 "mark items 9.14 to 9.20 complete", 9.17 (c) "mark items 9.18 to 9.20 complete", 9.15/9.16 "items 9.15 and 9.16", 9.19/9.20 "items 9.19 and 9.20", 9.18/9.19/9.20 "If item 9.17 or 9.14 marked", and 9.13 "return to the missing agent item (9.5 to 9.12)". References into Phase 9 from outside it (lines 1144, 1234, 1812, 1951, 2842, 2861) name only 9.1, 9.2 and 9.3, which kept their numbers. All `item(s) N.M` references across the file resolve to existing ids. The only unresolved tokens are DESIGN step numbers in "steps 1.17 to 1.19" form, not item references. |
| Gate counts vs full-intensity floors | PASS (with M4 note carried) | Title tally: r3-b1, r3-b2, r3-b3, r4 and r5 each 5+4; decisions 4+3+1 analyst; impl-core 4+3; impl-cli 5+3; tests 4+3; cmd-skill 4+3; contract 4+3; docs 5+3; final 6+4. Every code and design gate meets 3 rf-qa + 3 rf-qa-qualitative. Fidelity is 3+1, which verify-1 already accepted as MINOR M4 (research/09 Gap 5 fidelity floor). The other gates still say "of 7" or "seven reports" (lines 1507-1560, 1832-1885, 1985-2038, 2138-2191), which is correct for them. |
| TBD, TODO, FIXME | PASS | Every hit (lines 285-1108) is a quoted DESIGN check such as `grep -nw 'TODO\|TBD'`, or a lens prompt saying "no `TODO` or `TBD`". There is no FIXME, and no hit is a placeholder. |
| Leftover project-root `artifacts/` paths | PASS (note M1) | Bare `artifacts/` hits: line 83 (overview), 1226 (7.13 title), 2537 (14.15 lens prompt, verify-1 M1), 2732, 2846 and 2847 (prose about research/09's names and OQ text). None of these is a write target. The one new hit is line 808 (5.7), the path text 5.7 writes into DESIGN (M1). No command writes to a bare `artifacts/` path. |
| Phase order | PASS | Phases 1 to 14 come in order, each with its `<!-- END PHASE N -->` marker (lines 206-2763). The new 9.12 sits inside the existing impl-cli gate, after 9.4 validation and before 9.13 consolidation. No HALT or code item moved. |
| Commit, push or merge item | PASS | `grep 'git (commit\|push\|merge\|rebase)\|gh pr (create\|merge)'` hits only lines 808 and 1279, both `git merge-base --is-ancestor`, which is read-only. Key Constraints line 157 still says there is no commit or push item. |
| POST reflect runner prompt | PASS | I took the 9 lines of `~/.claude/skills/task-builder/SKILL.md:2223-2231`, filled in `{TASK_FILE}`, `{OUTPUT_DIR}`, `[--spec {SPEC_PATH}]`, `{DEPTH}` and `{BASE}..HEAD` (the OQ-12 diff-file fill), and ran `diff` against task lines 2742-2750: IDENTICAL. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| N-01 | IMPORTANT | Items 5.1 Verification (line 768), 5.3 title, Context, Action and Output (lines 778-781), 5.11 change text (line 836), 5.12 pass rules (line 843) | The I-1 fix calls DESIGN line 835 (row 1.17, "The REPORT's WC-14 draft") "section 14 row 1.17". The DESIGN headings put it in section 13: `## 13. Deviations from SPEC` runs from line 801 to 836, and line 835 is in its "REPORT differences" table. `## 14. Panel notes` (lines 837-863) has no WC-14 text. Item 5.12 requires "`WC-16` hits in sections 1, 8, 9, 10, 12, 13, 14, 15, 16 and 17" and "a `historical name (keep)` hit (sections 13 and 14 ...)". After 5.1 to 5.3, section 14 has no WC-16 hit, so the check fails every time. The 5.12 fix loop sends the executor back to "the owning item (5.1 to 5.11)", and none of those items writes WC-16 into section 14. The executor either loops or adds design text no research supports. The same defect class as I-1 and I-2. Item 5.11 would also write the false statement "marked the SPEC and REPORT draft names in 13 and 14" into the DESIGN revision log. | In 5.1, 5.3, 5.11 and 5.12, change "section 14 row 1.17" to "section 13 REPORT-differences row 1.17". Drop 14 from the 5.3 title and Output section lists, from the 5.11 change text ("in 13") and from the 5.12 WC-16 section list (sections 1, 8, 9, 10, 12, 13, 15, 16 and 17). Make the 5.12 historical-hit rule read "(both in section 13, each followed by "(WC-16 in this design)")". |
| M1 | MINOR | 5.7 Action, line 808 | 5.7 tells the executor to write "`artifacts/pr422-409-check.md`" into DESIGN, while DESIGN line 925 uses `.dev/tasks/<pkg>/artifacts/`. A later builder reading DESIGN could take the bare path as the project root. Item 7.19 writes the full task path, so this task behaves the same either way. | Optional: write `.dev/tasks/<pkg>/artifacts/pr422-409-check.md` in the 5.7 text. |
| M2 | MINOR | 5.7 Action and Verification, lines 808 and 810 | "Remove the 'wait or move 1.17 to 1.19 to a follow-up PR' and rebase branches" targets REPORT:1275 wording (research/09:111). DESIGN has none of it (`grep 'follow-up PR\|rebase\|wait for\|#422 is open'` on DESIGN returns no hit). The removal does nothing and the forbidden-word check passes without any edit. 5.7 point (1) also gives no `--json` fields, while DESIGN line 925 says `--json state,files` and 7.19 runs `--json state,mergedAt,mergeCommit`. | Optional: name the 7.19 `gh` command in 5.7, so the reworded DESIGN row and the artifact use the same command. |

Minor notes from earlier reports (verify-1 M1 to M4, alignment M-1 to M-8) are not rechecked, as the severity rule says.

## Summary

- Input findings checked: 6. Resolved: 6.
- New blocking defects from the cycle 2 edits: 1 (N-01, IMPORTANT).
- Minor notes: 2 (M1, M2). They do not fail the gate.
- Monotonicity: `|F_1|` = 6 (V-01, V-02, I-1 to I-4), `|F_2|` = 1, a strict shrink. No check that passed in an earlier cycle fails now.
- Hard cap: this is review 3 of 3 (2 fix cycles used). Per the review loop rule, escalate N-01 to the user. Do not run a fourth review.

## Recommendations

- Escalate N-01 to the user. If the user approves, the fix is one mechanical relabel in 4 items: section 14 becomes section 13 for row 1.17, and section 14 leaves the 5.12 WC-16 list.

**Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 12 | Grep: 16 | Glob: 1 | Bash: 8

## QA Complete

VERDICT: FAIL
