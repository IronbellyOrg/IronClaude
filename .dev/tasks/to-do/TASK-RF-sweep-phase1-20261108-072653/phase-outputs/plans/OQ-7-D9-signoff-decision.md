---
needs_human_decision: true
status: RESOLVED
---

# D9 sign-off decision (OQ-7)

## Question

OQ-7 is the owner's sign-off on deviation D9 of `docs/designs/orchestrator-mode.md`, quoted from section 13 (heading `## 13. Deviations from SPEC`, line 822), table row D9 at line 836. In plain words: D9 narrows what counts as a worker when the sweep decides whether a session was started by a person, and two residual cases of the narrower rule were never signed off by the owner.

> D9, column "SPEC text": "FR-010 and SP-29 (line 104): a transcript that the tab map marks as an Orca worker session (any Run), or whose session id appears in any Orca row of any Run, is never True"

> D9, column "Design": "A worker is a transcript joined to a Dispatch row of a scoped Run (path A or B). A tab-map entry that joins no scoped row gives None with note `Orca pane session, not in scoped Runs`, so person sessions started through `ccsession` in Orca panes are never idle or Historical in Phase 1. Under path A only, a transcript with no tab-map entry and no scoped join may be True when the guard holds, so a worker of an unscoped Run that has no entry can be True. Every True reached this way carries note `origin not proved: no tab-map entry; may be a worker of a Run outside the scope`, in the report row and in the JSON `notes`, so such a session is never shown as person-started without a note. Under path B the guard has four join-incomplete cases; the fourth (an earlier session of a reused pane has no entry) makes every unjoined no-entry transcript None, and a path-B join also needs the Dispatch row's time window, a transcript whose tail is complete and, when several rows match one pane session, exactly one window holding it. D9 as first written covers only True becoming None. Two residual path-B cases are new and need the same owner sign-off, which is still pending: a window with no end (a row still `pending` or `dispatched`) has no upper bound, so a person's later session in that pane, started after the worker died, joins the row as False and is shown as `orca:<dispatch>`, not as a person session; and a live session that serves two Dispatches joins the older row only, while the newer row is could not determine. Reason: the ccsession file cannot tell a worker pane from a person pane and holds no Run id, it has no entry for plain `claude` launches or earlier sessions of a reused pane (section 1), and no allowlisted verb lists the rows of Runs outside the scope (section 7.3). Needs the owner's sign-off at step 1.0b. Pinned by the D9 join fixtures in `sweep/test_classify.py`"

> D9, column "Source": "Review 1 B2; review 2 R2-B1 and R2-B2"; column "Section": "1, 7.2, 11"

The question as DESIGN section 17 open item 22 (line 1012) puts it: "the owner's sign-off on the D9 narrowing of SP-29 (D9 as first written covers only that True becomes None) and on its two residual path-B cases: a window with no end can join a person's later session in the pane as False, and a live session serving two Dispatches joins the older row only". Until it is closed, "the classify step does not start until the owner signs off D9 or names a stricter rule."

## Options

> "(a) sign off D9 as written;"

- "(a) sign off D9 as written;": the owner accepts D9 as quoted above, including its two residual path-B cases, and the classify step (step 1.3) may be built to it.

> "(b) name a stricter rule."

- "(b) name a stricter rule.": the owner names a stricter rule instead. Then DESIGN sections 7.2, 11, 13 and 14 need a revision before the classify step starts (item 7.12 Branch 2, option (b)).

## Recommendation

(a) D9 as written. This recommendation does NOT authorize adoption.

## Blocked work

Blocks: item 8.4 (step 1.3, classify) and every later item. Item 7.12 halts while this record is PENDING or Chosen is empty.

## Operator decision

OPERATOR DECISION: Sign off D9 as written, including its two residual path-B cases.
Chosen: (a) sign off D9 as written, as quoted from `docs/designs/orchestrator-mode.md` section 13, row D9, line 836, including the two residual path-B cases: a window with no end can join a person's later session in the pane as False, and a live session serving two Dispatches joins the older row only.
Decided by: Ryan Wiancko, owner, 2026-11-11.
Decision source: In this session's D9 question, the owner selected "Sign off D9 as written (Recommended)". The selected option's text reads: "Accept D9 and both edge cases as quoted in the design (section 13, row D9, line 836). The classify step is then built to it. I record your words as the decision, mark the record RESOLVED, and continue with item 7.13." This resolves OQ-7/D9 only; no other decision is inferred.
