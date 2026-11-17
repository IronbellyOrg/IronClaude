## Completeness QA Report (Partition b: Sections 6 to 10)

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/RESEARCH-REPORT-review-panel-unification.md` (4241 lines; Sections 6 to 10 = lines 1146 to 4241)
**Lens:** completeness (instance b, `Assigned sections: 6-10`; the instance a report covers Sections 1 to 5)
**Date:** 2026-11-14
**Fix authorization:** false (report only; the document was not modified)

[PARTITION NOTE: checks that need Sections 1 to 5 (the overlap matrix, Sections 2 to 5 topic coverage) are limited to what Sections 6 to 10 carry; instance a covers the rest. Merge both reports for the full verdict.]

### Checked

Evidence for each lens item. Mechanical checks were run with grep, sed and awk over the report, `gaps-and-questions.md`, `research/research-notes.md`, the 13 research files, the 4 web files, 6 scope slices, 7 synthesis files and the `reviews/adversarial/` tree.

| Lens item | What was checked | Result |
|---|---|---|
| a. Scope-discovery topics | Twelve Phase 2 topics (research-notes `SUGGESTED_PHASES`) plus the gap-fill file 13: each maps to conflict rows C-01 to C-20 (finding contract C-01/C-02/C-16, ledger C-13, clustering C-12, panel and identity C-03/C-04/C-08/C-09, blocking and calibration C-05/C-06, briefs C-10/C-18, reflect merge C-11, run recording C-07, consumers 7.1.4 and 7.2 and M3, future consumers 7.2/7.3 and M4, evaluation C-20, test pins 8.3 and M2-01, ensemble C-17 and ENS-1 to ENS-9). Four web topics: `web-01` to `web-04` are cited in Sections 6 to 10 (7, 9, 15 and 11 hits) and each web recommendation was spot-checked by keyword (abstention, bias battery, standing audit sample, occurrence index, empty-location rule, chaining caps, `match_reason`, five-tier core scale, native severity, vendor diversity); all found. Six solution-research approaches: each has its options in Section 6 (finding contract in 6.X and C-01/C-02; merge and verdict in C-05/C-11/C-13; clustering C-12; resolution and identity C-03/C-04/C-08/C-09; run recording C-07; rollout C-20). Required content (b) to (e): value inventory 8.1 (691 `V-` rows), conflict log Section 6 with D1 to D16 in 6.D, target architecture 7.1, exposure list 7.2, migration path 8.2, no-regression gates 8.3, branch options with the git ref-naming constraint 8.4, risk inputs 8.5. No topic is silently dropped. | PASS |
| b. Every gap resolved in Section 8 or carried in Section 9 | All 94 gap IDs (G-01 to G-94) appear in Section 9.1 exactly once (no duplicate, none missing); the 9.1 mapping was cross-checked against the text of each Q row (no mismatch). All 30 Important gaps are in rows Q-01 to Q-30, and the 64 Minor gaps are in Q-02, Q-05 and Q-31 to Q-44 (62 + 2 = 64). All 77 stale-document rows D-01 to D-77 appear in 9.4; all 25 closed items C-01 to C-25 appear in 9.3; O-1 to O-6 appear as Q-01 to Q-06. The Section 4 gap table (144 rows: 15 Critical, 65 Important, 64 Minor) was walked row by row: every Critical and Important row appears in the 8.2 coverage table, and every Minor row appears by ID in Sections 8 to 10. The four partial adversarial debates are carried as open items (Q-47 to Q-53, Q-57), with their unaddressed HIGH invariants stated as open, not solved (executor note 1). | PASS |
| c. Evidence Trail completeness | Globbed the task folder and compared with Section 10: research files 01 to 13 (13 of 13 listed), web files 01 to 04 (4 of 4), synthesis files 01 to 07 (7 of 7), scope inputs `research-notes.md` plus slices 00 to 05 (7 of 7), the four adversarial folders and `conflict-index.md` (all listed), `BUILD-REQUEST.md`, the task file and `gaps-and-questions.md` (listed). Counts in the Gaps Log line (94, 77, 6, 25) match the file. Notes below (M-1, M-2) are minor. | PASS (2 minor notes) |
| d. Key Takeaways reflected or excluded with rationale | Read the Summary section of research files 01 to 13 and the Recommendations section of `web-01` to `web-04`; checked each distinctive takeaway by keyword in the report (for example: seven finding shapes and the nine-place limits, 49 lost blocking findings split 24/14/10/1, 195 chained rows and 83 mega-rows, `PROFILES`, canary and "silence never passes", 142 of 142 shadow calibrations, 65 versus 38 and +2.75 wrong blockers, 156 of 665 source-blind runs, 23 of 45 briefs, EV-1 0.615 against 0.077, 6 of 14 inline debates, three unparseable `[1m]` contracts, HEAD-relative pins, 43 call sites with 32 needing an in-place fix, the `REVIEWERS` tuple and S2b seam, ensemble defects D1 to D11 of file 13 including the literal `status: "success"` at `ensemble.py:789` carried at V-564 and ENS-1). All found in Sections 1 to 10; where an older figure was superseded it is named and replaced (see next row). | PASS |
| Executor note 3 (parsed-sparse figure) | Listed every line of Sections 6 to 10 that carries 35 of 39, 37 of 38, 34 of 38 or "driven by the parsed-sparse flag" (about 25 lines). Every one states either the recount (flag set in 35 of 39 non-shadow runs, 34 of 38 Tier 2 runs, decisive in 0 for certain and at most 1) or marks the older figure as superseded and not used (lines 1175, 1838, 2044, 2064, 2073, 2088, 2091, 2101, 2103, 2616, 2882, 2888, 2897, 3232, 3282, 3315, 3434, 3589, 4124). No sentence presents the old claim as measured fact. | PASS |
| Executor note 4 (E2 commit) | The only E2 commit hash in Sections 6 to 10 is `4a22d74213f93837d00c2c314075dd967b9a98e3` (8 hits); the other hashes are E1 commits (`9874d63fb`, `c2e3347d3`, `792cf8c52`, `d2d8a2d16`) or the folder name `base-e8db2fe6`. | PASS |
| Executor note 5 (report-only, no roadmap) | Section 8 states it is not a roadmap, step IDs carry no order, date or sprint (lines 2893, 2895, 3611); a search of Sections 7 to 10 for roadmap, sprint, `/sc:workflow` and dates finds only scope statements and inventory rows about existing commands. | PASS |
| Executor note 2 | `[CONTRADICTION]` on the core verdict vocabulary is carried in Section 7 and in M1-07, M1-08, M1-16, M3-08, Q-54 as an allowed open flag. | ALLOWED |

### Findings

| # | Severity | Section | Finding | Proposed Fix |
|---|---|---|---|---|
| M-1 | MINOR | 10 (QA Reports) | The QA table names only the Phase 5 reports (14 files). The `qa/` folder holds about 45 files; the Phase 3 verification and fix files, the analyst and research-gate reports and the task-validation reports are described in one sentence and not listed. The lens checklist item c does not require QA reports, so this is a note only. | Optional: add one row per remaining `qa/` file group, or leave the sentence as the index. Add the Gate 3 to Gate 5 reports when they exist. |
| M-2 | MINOR | 10 (Adversarial Debate Outputs) | The C14 row names `adversarial/recount_tier_decision.py` but not `reviews/adversarial/panel-size-cost/adversarial/quant_score.py`, the other script in that folder. | Optional: add `quant_score.py` to the C14 row. |
| M-3 | MINOR (note) | 5 vs 6 to 10 | `web-01` recommendation 5 (per-reviewer reliability weights learned from agreement, simulation-only evidence) and `web-02` recommendation 8 (SARIF export rank cut points and `security-severity` rule) appear in Section 5 only, not in the option rows of Section 6 to 10. Both are explicitly conditional options in their research files ("only after a calibration set exists", "if SARIF export is a goal"), and the Section 6 options C-05 Option C (calibrator-weighted) and C-01 Option C (five-tier scale with native severity) cover the decision space. | None required. |

Outside this lens (not graded, for the consistency lens): Section 9 line 3906 keeps a `[CONTRADICTION]` between the gap-log rating (no Critical gap) and the Section 4 rating (15 Critical) "for QA resolution", and line 3869 says "32 of 41 review sites" while lines 409, 609 and 2423 say "32 of the 43".

### Summary

- Lens items checked: 4 of 4 (a, b, c, d) plus executor notes 2 to 5.
- Findings: 0 CRITICAL, 0 IMPORTANT, 3 MINOR (notes).
- **Confidence:** Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 13 | Grep: 1 | Glob: 0 | Bash: 30 (batched grep, sed and awk comparisons over the files named above; the line counts and ID sets quoted in the table come from those outputs)

Verdict: PASS (0 critical + 0 important; minor findings listed as notes)

## QA Complete
