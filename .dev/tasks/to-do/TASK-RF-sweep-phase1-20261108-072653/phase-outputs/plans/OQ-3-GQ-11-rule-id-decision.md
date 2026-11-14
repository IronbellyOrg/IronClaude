---
needs_human_decision: true
status: RESOLVED
---

# Coordinator rule decision

## Question

> "Rule ID: new WC-14 versus amending WC-1 (AMBIGUITY 4)"

This is the historical question GQ-11 (OQ-3), quoted from research GAPS row 34. The design re-anchor found WC-14 and WC-15 already occupied on master `5dc29d23`; the proposed new identifier is therefore WC-16. The current choice is WC-16 versus amending WC-1, not reusing occupied WC-14.

DESIGN section 8 also reserves the proposed coordinator-loop text for owner approval with this decision. The proposed rule keeps watching until all created Tasks are settled and results inspected/recorded, re-arms expired waits, and adds `/sc:sweep` as a read alongside the existing coordinator sweep at its bounded cadence. Its reads are not coordinator L1 probes; it does not replace the existing sweep or update heartbeats. The report is local and never posted; person-started sessions are observed but never messaged; `/sc:sweep` recommends no actions. The complete proposed text is in `docs/designs/orchestrator-mode.md:674-680`; this summary does not replace it.

## Options

> "(a) a new rule WC-16, the next free id on master `5dc29d23`;"

> "(b) amend the unused WC-1."

Option (a) uses the new identifier and proposed text in DESIGN section 8 without changing existing WC-14/WC-15 worker duties. Option (b) changes the chosen identifier and requires the design revision specified by task item 7.4 before implementation continues.

## Recommendation

(a) WC-16, which DESIGN section 8 uses after design fix R4. This recommendation does NOT authorize adoption.

## Blocked work

Items 12.1-12.3 (steps 1.17-1.19), the coordinator rule, never-as-worker addition and contract pins.

Hard gate: GQ-11 must be answered by the owner before steps 1.17-1.19. "Working default accepted" counts only when the owner says it. Silence or an answer that merely says "use the default" without naming an option does not resolve the decision. Item 7.4 halts while this record is PENDING or Chosen is empty. Choosing WC-1 requires revisions to DESIGN sections 8, 9, 10, 12, 15 and 16 before proceeding.

## Operator decision

OPERATOR DECISION: Approve option (a), new WC-16 and the proposed coordinator-loop text in DESIGN section 8, preserving existing worker duties.
Chosen: New WC-16 rule, not amending WC-1.
Decided by: Ryan Wiancko, owner, 2026-11-09.
Decision source: The owner selected "New WC-16 rule (Recommended)" in this session's coordinator-loop question. That option explicitly approved the section-8 text and its new identifier while keeping existing worker rules unchanged. This direct answer resolves OQ-3/GQ-11 only. A separate peer relay from ORCH-IronClaude reports "Approved, proceed" at 12:15 UTC; that relay corroborates but is not the authority used here, which is the owner's direct answer in this session. No later decisions, retry reset, additional workers, commit, push, PR or merge are authorized by this selection.
