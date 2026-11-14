---
needs_human_decision: true
status: RESOLVED
---

# Activity window decision

## Question

> "Default window 6 h versus 72 h (AMBIGUITY 2, F11)"

OQ-5/GQ-61, from the research package's `gaps-and-questions.md:84` and `research/research-notes.md:304`. The owner must choose the default, not the implementation. The window bounds activity only: open Tasks, questions and unread reports are always listed regardless of age. A shorter window must not hide unresolved work.

## Options

> "6 h (issue) vs 72 h (`sc-crash-recovery/SKILL.md:26`)"

- "6 h (issue)": set the CLI default to `6h`, matching DESIGN's working default, bounding recent activity to six hours.
- "72 h (`sc-crash-recovery/SKILL.md:26`)": set the CLI default to `72h`, bounding recent activity to three days. The crash-recovery reference is the research's historical alternative, not a claim about its current installed default.

Both options preserve activity-only filtering. `SweepContext` carries the selected duration; there is no additional window constant outside the CLI default. Choosing 72h must be recorded for all later items and in Phase 7 Findings as required by item 7.8.

## Recommendation

6 h, bounding activity only; open Tasks, questions and unread reports are always listed. This recommendation does NOT authorize adoption.

## Blocked work

Items 8.12, 9.1 and 10.5: steps 1.5 and 1.12 window behavior and step 1.6's `--window` default. Item 7.8 halts while this record is PENDING or Chosen is empty. An existing `6h` design default is not an owner answer.

## Operator decision

OPERATOR DECISION: Approve the six-hour activity-only default.
Chosen: `6h` as the CLI default, bounding activity only. Open Tasks, questions and unread reports remain listed regardless of age.
Decided by: Ryan Wiancko, owner, 2026-11-09.
Decision source: In this session's activity-age question, the owner selected "Six hours (Recommended)". The selected option explicitly approves 6h and preserves unresolved-work visibility. This resolves OQ-5/GQ-61 only; no other decision is inferred.
