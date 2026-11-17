# Round 1 advocate statement: variant 1 (opus, architect)

Persisted by the main session from the agent's message; unedited.

Variant 1, round 1: final positions and concessions.

(1) STEELMAN
V2: The proposed cuts are the right size, but the real cost is tests and dependency lines, not tasks. Keep a plain list file, word RT1 as "any real blocker in a Medium list", use a quorum that never halts a round on one bad report, and do not reopen stage 4, the only package at 0 blockers.
V3: Cut mechanisms, never coverage. Capture failure, safety routing, installed-path checks, a planted safety-miss check, and every gate a later stage reads must survive or be rewired.

(2) Contested points
C-002/X-003 SHRINK, no new file. The list is the report's follow-up candidates section (pragmatic.md:230), and under /sc:implement it is notes.md, which fails closed (qa.md:203). Concede: if the owner wants one list per run across reviewers, keep one plain file.
C-003 SHRINK. The final step prints the notes.md minors; the print goes in SKILL.md and managed-workspace.md, the files stage 2 T3 already edits (stage2 plan:76), so qa.md stays untouched. Cut the sweep and S3 T10. Concede V2: the planned sweep prints "No follow-up ledger" in every real run (stage2:76).
C-006 CUT. Concede: the regrade grades findings it is given, so it cannot measure discovery. Rewire S3 T6 to the regrade ruling, as V2 says.
C-009 CUT T2, T3 and T5 to T8. Concede: keep T9 as a short errata note, and fold T10.
C-010 SHRINK. Concede: the stage 4 entry check reads stage3-summary-for-owner.md and the README go cell (stage4 plan:42,44). Keep any summary that an entry check reads.
C-011 SHRINK. Move the 8-file copy of S1 to S3 into stage 3; stage 4 keeps the merge-rule lines. Concede: a full merge would reopen stage 4's clean text.
C-012/X-004 Copy the text, do not weaken the test. Stage 3 keeps the 8 legacy files passing only through registry rows that pin them to frozen old text (stage3 plan:218), and C4 cuts that registry. Concede V2: removing any file from the tuple must also fix the [:6] slice (test_review_severity_rule.py:193). Concede V3: the reachability check is still owed (UNVERIFIED).
C-013/X-005 SHRINK to V2's form. merge_round raises an error only when no reviewer produced a valid block, and it keeps parsable findings (ledger.py:107-113). Require two reports only when two or more reviewers were launched.

(3) Shared assumptions
A-001 QUALIFY: plain deletions need no new review; rewired dependencies and new print or copy text need one re-review.
A-002 REJECT "sufficient": it is a lower bound only. Pair it with RT1 plus the owner reading the first five lists.
A-004 QUALIFY: under /sc:implement, notes.md (qa.md:200) is also a writer, and the C3 shrink prints it.
A-005 QUALIFY: S1 itself makes security and data-loss findings blocking (pragmatic.md:225); the scan is a second line of defence.

(4) Strongest unconceded claim
All three variants cut the registry (C4), yet the staged plan passes test_c in the mixed-rule state only through registry rows (stage3 plan:218). Without the registry, keeping the stages apart needs a hand-built frozen-text split of S1_S3_FILES. Copying all ten files in the same change as pragmatic.md needs nothing extra and ends the mixed-rule window.
