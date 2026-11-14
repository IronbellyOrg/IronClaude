# Lens 2 (persona: qa): commands, expected values and the decision-record count (F-01) across all consumers

Read first: the common brief (same folder, common.md). Your slice: every task-file line that mentions `OQ-` decision records, owner-decisions.md, `status: RESOLVED`, `does NOT authorize adoption`, OQ-17 or OQ-18 (find them with Grep over TL), plus items 7.11 to 7.19, 7.20 to 7.36, 8.1, 14.19, and the OQ files under P/phase-outputs/plans/.

Focus on F-01 and F-06 and all shell-style checks:
1. Walk each decision-count command and its expected value for three states of the plans folder: (i) the eight prerequisite records alone (OQ-1..OQ-8), (ii) plus one resolved optional record (OQ-17 or OQ-18), (iii) plus both. Also a state where a required record is missing or unresolved. For each consumer (7.13, 7.17, 7.20, 7.22, 7.25, 7.30, 7.33, 7.34, 7.37, 8.1, 14.19 and the twelve lens-input lines) decide: does it give the right answer, and does the fixer in 7.30/7.34 have a path to repair a finding without tripping the regression halt or monotonicity halt in 7.33 (TL near 1384)? Look at which records 7.17 actually writes (TL:1270-1273) and what status they get.
2. Every changed command: does it carry an expected value; is the glob/quoting right for the shell; would a literal glob with zero matches break it (exit codes); are the `grep -c` multi-file outputs read per file?
3. The F-06 reword (58 Context lines): is the new sentence true after item 7.10, and does any lens or verifier still depend on the old literal?
4. Items 10.5 and 8.19 (F-10): is GQ-35 (report layout) versus GQ-63 (chat reply only) stated correctly against the OQ-4 and OQ-6 records?
5. Items 11.4 (TL:1980-1982): do the pins check presence and not absence; are both repair routes executable?
