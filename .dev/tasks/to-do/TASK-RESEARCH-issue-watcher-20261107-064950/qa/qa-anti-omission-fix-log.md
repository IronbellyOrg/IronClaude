# Anti-omission fix log (Gate 5, fix cycle 1)

**Date:** 2026-11-07
**Agent:** rf-qa, anti-omission fix agent (`fix_authorization: true`)
**Report edited:** `RESEARCH-REPORT-issue-watcher.md` (targeted Edit calls only; no research, synthesis or research-notes file touched)
**Input:** `qa/qa-anti-omission-consolidated-findings.md` (2 blocking omissions: O-05, O-04, both RECOVER; minor omissions stay notes)

## Resolution summary

| # | Omission | Disposition | Resolution | Where |
|---|---|---|---|---|
| O-05 | `orca agent launch` has no permission-mode or allowed-tools flag; the prompt is one free-text argument | RECOVER | RECOVERED | Section 2.2 argument contract (new row "Permission mode and allowed tools", report line 277); Section 7.9 open decision 5 (the "Why open" cell) |
| O-04 | Research 01 estimates the double-claim race window at seconds to minutes and a collision as possible but not frequent | RECOVER | RECOVERED | Section 2.4 "Open governance decisions" paragraph; Section 6 revisit condition 4 (authoritative table); Section 5.15 condition 4 row; Section 7.9 open decision 6; the later revisit-conditions copy of condition 4; Section 9 gap table Q3 row |

Unresolved blocking omissions: 0.

## Details

### O-05 (RECOVER, recovered)

- **Source re-read:** `research/03-governance-and-security-surface.md` section 3.1, line 84: "`orca agent launch` accepts `--agent <id> [--worktree <selector>] [--prompt <text>] [--model] [--effort] [--surface chat|terminal]` (output of `orca agent launch --help`, run 2026-11-07). The prompt is one free-text argument; there is no flag for a permission mode or an allowed-tool list. [OBSERVED]".
- **Evidence level kept:** the source tags the statement [OBSERVED] (help output). The report row carries [OBSERVED] for that fact only. The consequence (how the permission mode is then decided per host) stays [UNVERIFIED], which matches the existing report text and file 03 section 2.2.
- **Edits (2):**
  1. New row in the `orca agent launch` argument contract table in Section 2.2, placed before the "Mechanism by which Claude receives the prompt" row: states no permission-mode flag, no allowed-tools flag, one free-text prompt; cites the help run of 2026-11-07 and R03 section 3.1; links to open decision 5 in Section 7.9.
  2. Section 7.9 item 5 (permission mode of the launched session), "Why open" cell: added that the launch call cannot set it, with the same citation and [OBSERVED]; added §3.1 to the source cell.
- **Note on numbering:** the consolidated file calls this "Q6". In the report, the permission-mode question is Section 7.9 item 5 and Section 9 gap Q4 (permission mode). The Section 9 "Q6" row is about where the poller runs, not permission mode. The recovery therefore went to the rows that actually hold the permission-mode question.

### O-04 (RECOVER, recovered)

- **Source re-read:** `research/01-claim-flow-and-session-launch.md`, the race paragraph at line 155 (section 9, question 2 of that file): "Reading the code, not running it ... The window is the length of Wave 1 plus the spawn, which is seconds to minutes; a 5-minute poll cycle with unsynchronised workspaces makes a collision possible but not frequent." The same paragraph marks the multi-assignee premise as derived from code and UNVERIFIED here.
- **Evidence level kept:** every added clause says the figure is an estimate from reading the code and not measured. No tag was upgraded; the existing "was not measured" statements stay in place, so there is no contradiction.
- **Edits (6), each adding one clause:**
  1. Section 2.4 "Open governance decisions recorded by the research" paragraph.
  2. Section 6 "Revisit conditions for options B and C", condition 4, source cell (the authoritative table).
  3. Section 5.15 condition 4 row (same nine items, so the clause was added to keep the copies consistent).
  4. Section 7.9 item 6 (at-most-once design), "Why open" cell, plus R01 §9 added to its source cell.
  5. The later revisit-conditions copy of condition 4 (source cell).
  6. Section 9 gap table, Q3 row (race window).
- **Note on numbering:** the consolidated file calls this "Q13". In the report, Q13 is the `issue:<number>` selector question; the race-window gap is Q3 and GQ #15. The recovery went to Q3.

## Verification

- Grep of the report for the inserted phrases: 8 hits (2 for O-05, 6 for O-04), matching the 8 edits.
- Grep for `[CONTRADICTION`: 0 hits.
- Table structure: the new Section 2.2 row sits in the argument contract table between the "How the initial prompt is passed" row and the "Mechanism by which Claude receives the prompt" row (report line 277, with the Mechanism row now at line 278; confirmed by Grep); every other edit is inside an existing table cell or an existing paragraph, with no added rows or columns, so the Table of Contents and cross-references are unchanged.
- Addenda conformance not touched: option A decided by the owner, B and C scored, Coder#477 boundary and the unnecessary-under-A statement, and the integer-only prompt rule were not edited.
- Files edited: `RESEARCH-REPORT-issue-watcher.md` only (plus this log).
- Minor omissions (about 25, per the consolidated file) were not recovered and remain notes.
