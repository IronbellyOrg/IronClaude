## Template-Conformance QA Report

**Report reviewed:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md`
**Lens:** template-conformance
**Instance and range:** instance a, lines 1 to 2114 (MODE: SPLIT, split point K = 2115), plus section-heading checks across the whole report for ordering
**Date:** 2026-11-14
**Status:** In Progress

Grading: under the owner grading override (`qa/grading-override.md`). Severity label kept as information only.

### Findings

| # | Severity | Section | Finding | Evidence | Proposed Fix |
|---|---|---|---|---|---|
| 1 | MINOR (label) | End of Section 5 (line 2112) | A synthesis-file completion marker `Status: Complete` is left inside the assembled report, after "Statement on precedence" and before `## 6.`. It is a leftover sentinel from the synthesis file, not report content. No decision, value-inventory destination, conflict outcome or number depends on it. (minor under grading override) Two more copies exist outside this instance's range (line 3104 `**Status: Complete**`, line 3541 `Status: Complete`); instance b owns those. | Grep `^\**Status\**:` over the report returned lines 2112, 3104 and 3541; Read of lines 2100-2115 shows the line sits at the end of Section 5 between the precedence statement and the `## 6.` heading. | Delete the line at 2112 (and the two copies at 3104 and 3541). |
| 2 | MINOR (label) | 2.1 (lines 210, 212, 213, 215), 2.7 (lines 704-713), 2.9.4 Tables A and B (lines 907, 918) | Empty table cells. Lines 210, 212, 213 and 215 leave the "Note" cell empty. Lines 704-713 leave the "Use case" cell empty on continuation rows under "PR code review" and "rf-qa replacement" (a visual row-span). Lines 907 and 918 leave non-total columns empty on the Total rows. In each case the substance of the row is in the other cells, so no missing content stands behind the empty cell. (minor under grading override) | Grep `\|\s*\|` returned these lines in range; Read of lines 200-216, 690-725 and 893-922 confirmed the other cells carry the data. Hits at 283, 1216, 1248 and 2244 are `\|\| true` or `path\|\|refs` text inside cells, not empty cells. Hits at 495, 499 and 529 are in an ASCII diagram or a long cell. | Optional: put a dash or the use-case name in the empty cells so a later reader of a single row has the context. |

### Checks performed (checklist a to d)

| Check | Result | Evidence |
|---|---|---|
| a. All sections present | PASS | Grep `^#{2,4} ` over the report: `## 1.` (122), `## 2.` (137) with `### 2.1` to `### 2.9` (139, 272, 343, 414, 484, 590, 657, 728, 828), `## 3.` (1110), `## 4.` (1206), `## 5.` (1515), `## 6.` (2115) with `### 6.1` to `### 6.12` (2135 to 3107), `## 7.` (3544) with `### 7.1` (3650), `### 7.2` (3760), `### 7.3` (3935), `## 8.` (4209) with `### 8.1` (4213) and `### 8.2` (4369), `## 9.` (4648), `## 10.` (4806). Appendix A and B follow at 5031 and 5035. Nothing is marked N/A. |
| b. Ordering | PASS | Line numbers rise in section order 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 with no reordering or merged section. Numbered subsections stay in order (2.1 to 2.9; 6.1 to 6.12; 7.1, 7.2, 7.3; 8.1, 8.2). Unnumbered subsections sit between numbered ones in 6 (after 6.11, before 6.12) and in 7 (before 7.1 and between 7.2 and 7.3). They add to the numbered set and do not reorder or merge it. |
| c. Placeholders and markers | PASS with finding 1 | Grep `T[O]DO\|T[B]D\|FIX[M]E\|PLACEHOLDER`: no matches (normal result). Grep `\[PENDING-ADJUDICATION`: no matches, no error. Grep `ADJUDICATION-FOLD-PENDING\|PENDING-ADJUDICATION\|FOLD-PENDING`: no matches. Grep for `<!--`, `[SECTION`, `[PENDING`, `sentinel`, `WIP`, `[ ]`, `Status: In Progress/Draft`: no matches. `{{CANDIDATE}}` style tokens at lines 400, 421, 883, 1248, 1309 are quoted content about the loop prompts, not template placeholders. The one leftover marker is `Status: Complete` (finding 1). Empty cells: finding 2. |
| d. Table of Contents | PASS | Read of lines 10-99 against the heading Grep. Every ToC entry has a heading of the same text and the same level (h2 for sections, h3 under them; `2.9.x`, `6.12.x`, `8.1.x` and the lettered 8.2 blocks are h4 and are left out of the ToC at depth 2, which is a consistent rule). The ToC order matches the heading order, including the unnumbered h3 blocks in 6 and 7 and the Appendix A and B entries. I derived the GitHub anchors for the entries with punctuation (`#611-...--rf-qa-qualitative-replacement`, `#corrected-claims-...`, `#adjudication-register-...`, `#items-marked-unverified-...`, `#appendix-a-...`) and they match the heading text. |

### Summary

- Total findings: 2
- Blocking under the grading override: 0
- CRITICAL: 0, IMPORTANT: 0, MINOR: 2 (both `(minor under grading override)`)
- Verdict: **PASS** (with notes)
- Limits: ToC anchors were checked by deriving the slug rule by hand for the entries with punctuation, not by rendering. Instance a covers lines 1 to 2114 for content checks. Structure checks (a, b, d) and the marker Greps ran over the whole report.
- Tool engagement: Read: 12 | Grep: 11 | Glob: 0 | Bash: 0

Status: Complete
