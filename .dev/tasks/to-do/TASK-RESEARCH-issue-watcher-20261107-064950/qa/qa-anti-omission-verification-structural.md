# QA Report - Anti-Omission Fix Verification (Structural)

**Topic:** GitHub issue watcher research report
**Date:** 2026-11-07
**Phase:** fix-cycle (anti-omission verification)
**Fix authorization:** false (report only)
**Status:** In Progress

---

## Checks (appended incrementally)

### Check A - O-05 (orca agent launch: no permission-mode / allowed-tools flag, one free-text prompt) - PASS

- Source re-read: `research/03-governance-and-security-surface.md` line 84 (section 3.1): "The prompt is one free-text argument; there is no flag for a permission mode or an allowed-tool list. [OBSERVED]" (basis: `orca agent launch --help`, run 2026-11-07).
- Report: Section 2.2 argument-contract table, line 277, new row "Permission mode and allowed tools": states the prompt is one free-text argument, no permission-mode flag, no allowed-tool list; cites the help run of 2026-11-07 and R03 section 3.1; tag `[OBSERVED]` for the flag fact, `[UNVERIFIED]` for how the mode is then decided per host. Evidence level equals the source ([OBSERVED]); the added consequence is correctly kept UNVERIFIED (file 03 line 183 and section 2.2 treat the permission-mode decision as open).
- Report line 1428 (Section 7.9 item 5): same fact, same citation, `[OBSERVED]`, source cell extended with R03 section 3.1.
- Table integrity: row 277 has 3 cells like its neighbours (lines 276, 278); row 1428 has 3 cells like its header (line 1422).
- Note (minor, no action): the report's Invocation row (line 271) lists `--focus`, `--retry-launch`, `--json` in addition to the flags in the R03 help excerpt. They come from the code spec (`agent-launch.js:9`) and are tagged CODE-VERIFIED, so there is no contradiction.

### Check B - O-04 (double-claim window "seconds to minutes", collision "possible but not frequent") - PASS

- Source re-read: `research/01-claim-flow-and-session-launch.md` line 155: "Reading the code, not running it ... The window is the length of Wave 1 plus the spawn, which is seconds to minutes; a 5-minute poll cycle with unsynchronised workspaces makes a collision possible but not frequent." Derived from code; the multi-assignee premise is marked UNVERIFIED there.
- Report hits (8 total, matching the fix log): line 277 (O-05), 499 (Section 2.4 paragraph), 962 (Section 5 condition 4 row), 1319 (Section 6 revisit condition 4, authoritative copy), 1428 (O-05), 1429 (Section 7.9 item 6), 1806 (later revisit copy), 2047 (Section 9 Q3). All six O-04 sites say the figure is an estimate from reading the code, not measured. Evidence level matches the source (derived estimate, not upgraded to a measurement).
- No contradiction with the existing "was not measured" statements: they sit in the same cells and reconcile ("not measured; R01 section 9 estimates ...").
- Table integrity: lines 962, 1319, 1429, 1806, 2047 keep the column counts of their header rows (957, 1314, 1422, 1801, 2043).

### Check C - Minor omissions - PASS (notes only)

- The consolidated file lists about 25 minor omissions as intentional dedup or out of scope. Under the severity rule they are minor and are not rechecked. The only blocking items (O-05, O-04) are verified in Checks A and B.

### Check D - No new blocking defect - PASS

- Grep of the report for `[CONTRADICTION`, `TBD`, `TODO`, `FIXME` returned 0 hits.
- Heading Grep: sections 1 to 10 appear in order (lines 102, 153, 576, 676, 753, 991, 1332, 1442, 1834, 1910), then Appendix A at 1997. The Table of Contents (lines 10-30 read) lists the same sections; no heading was added or renamed, since every edit was inside a cell, a paragraph, or the one new row in the Section 2.2 table.
- `[OBSERVED]` is already used elsewhere in the report (7 occurrences), so the new uses add no new tag.
- Cross-references in the new text (Section 7.9 item 5, "Launch-session environment facts") point to existing content (item 5 confirmed at line 1428).

---

## Summary

- Blocking omissions recovered: 2 of 2 (O-05, O-04), at the evidence level of their sources.
- New blocking defects introduced: 0.
- Minor notes: 1 (Invocation row lists code-verified extra flags; no action).
- Confidence: Verified: 4/4 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 14 | Grep: 5 | Glob: 0 | Bash: 0

VERDICT: PASS

**Status:** Complete

