persona: qa
model_class: haiku
model: claude-haiku-5-5

## qa analysis

I audited the 9-row coverage matrix against the whole spec body (source.md, 37 lines, in the grounding hunks), and against the task ACs and recorded evidence in the hunks. I did not open the plan file or the artifact files themselves. Everything below rests on the quoted hunks in the brief.

**Spec spans checked against the matrix.** Every requirement-bearing span maps to a row: four-backtick outer fence opening and closing = INF-001; the six-pair line table = INF-002; confirm-each-pair rule = INF-003; script copy + run before/after with -I = INF-004; none-state + named headings outside + Appendix B/C state = INF-005; diff against saved copy exactly twelve fence lines = INF-006; pytest tests/docs = INF-007; out-of-scope list = INF-008; constraints (no dash, staging) = INF-008/INF-009. The t8-stale-fences context paragraph is motivation, not a requirement. No requirement-bearing span missing from the matrix.

**Weak spots, not worth a finding.** "Save that diff under ./artifacts/" and "use -I" have no row of their own; folded into INF-006/INF-004 and covered by task ACs (t1-diff, guide-diff). The matrix cites source lines (7, 9-18, 24) that don't match the spec body's line numbers; a citation-numbering quirk only.

**ACs mechanically checkable from recorded evidence.** Task 1 AC1-AC3 (baseline byte-identity, fence-before, t1-diff line count, 2.2 heading state) all checkable. Task 2 AC1: fence-after.txt:280-281 shows none; heading excerpt shows 2.2, Example 1-3 outside any fence; Appendix B headings inside the four-backtick fence from 2082; Appendix C outside. Task 2 AC2-AC5 (guide-diff, dash grep, pytest-docs, git-status) all checkable.

## Findings block
```findings-v2
```
