---
needs_human_decision: true
status: RESOLVED
---

# Report layout source

## Question

> "#409 version pinning (`495eb96d`, unmerged) (AMBIGUITY 9)"

Question OQ-4/GQ-35. Three sub-questions quoted from `research/research-notes.md:311` in the research package:

> "copy the layout into this repo or cite commit 495eb96d (unmerged)"

> "which sort tie-break to use"

> "what approval label the reused design carries"

The task's 2026-11-08 check records that the commit was not an ancestor of origin/master and issue #409 was open then. This pending decision makes no claim about their present merge/issue status. The proposed source is the fixed snapshot, not moving issue content.

## Options

> "copy the layout into this repo or cite commit 495eb96d (unmerged); which sort tie-break to use; what approval label the reused design carries."

The design's proposed choice is to pin and cite `495eb96d` while implementing the local report layout in DESIGN section 7.5, rather than depending on a moving external layout. The owner can instead choose copying without this citation or another layout, but a choice changing section 7.5 requires a design revision before implementation.

DESIGN section 7.5 fixes section order through twelve pure render functions. Waiting-on-person rows sort oldest first then unknown ages; its second group lists frozen-plan rows before Ready Tasks. Sessions retain the ten source dimensions plus Class, Rule, Evidence, Safe to close, Notes and Next inspection. Labels and ordering remain exactly those specified by section 7.5. The decision does not assert upstream runtime approval or authorize importing/changing dashboard code.

## Recommendation

Pin `495eb96d` and cite it, using the sort and labels DESIGN section 7.5 states. This recommendation does NOT authorize adoption.

## Blocked work

Item 8.12 (step 1.5), report-renderer skeleton. Item 7.6 halts while this record is PENDING or Chosen is empty. The choice must name the pin/copy strategy and settle the sort/label sub-questions. If it changes DESIGN section 7.5's layout, that design section must be revised through the task-builder route required by item 7.6 before proceeding.

## Operator decision

OPERATOR DECISION: Approve reuse of the pinned layout with DESIGN section 7.5 unchanged.
Chosen: Pin and cite commit `495eb96d` from issue #409 for the local report. Use DESIGN section 7.5's ordering (oldest waiting items first, unknown ages last) and its specified labels/session columns. Approval label: owner-approved reuse of this fixed layout, not a claim that dashboard runtime code or upstream issue work is approved or imported.
Decided by: Ryan Wiancko, owner, 2026-11-09.
Decision source: In this session's report-layout question, the owner selected "Pin and cite snapshot (Recommended)". The selected option explicitly approves this pin, unchanged section-7.5 ordering/labels, and continuation. This settles all three sub-questions for OQ-4/GQ-35 only; it grants no unrelated change.
