# Adversarial Debate Transcript: Q3 (Coder#477: keep, narrow or close)

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 100% on points (13 of 13 points reached at least a 2-of-3 majority)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned in parallel as sub-agents (general-purpose type): Variant 1 persona architect, Variant 2 backend, Variant 3 analyzer. No failures. Advocates were allowed a read-only `gh issue view` on Coder#477.
- Variant map: Variant 1 = proposal-A (narrow to read-only status and identity); Variant 2 = proposal-B (keep the listener and prompt routing with guards); Variant 3 = proposal-C (close as superseded with reopen conditions).

## Round 1: Advocate Statements

Full statements are kept once in their own files: `round1-advocate-V1.md`, `round1-advocate-V2.md`, `round1-advocate-V3.md`.

### Variant 1 Advocate (architect)
Narrowing keeps the one gap #477 still points at (an observer cannot see another workspace), deletes every route that can start a session, and is the only option that answers the owner's comment of 2026-11-13. Concedes: text A is not paste-ready; it designs for consumers that do not exist yet (it "Depends on ... observer release R4"); if the owner treats Q4's "single-host" as lasting, close is the consistent answer; an open issue can still be built wrongly; "narrow" really replaces the problem statement. Neutral recommendation: **Variant 1, about 60 percent**, Variant 3 if single-host is lasting.

### Variant 2 Advocate (backend)
Variant 2 is the only one that writes guards onto the routing the issue asks for, with the route disabled until #339's grant format exists. Concedes it is the weakest today: it contradicts a binding owner decision with no recorded revisit condition (`docs/designs/issue-watcher.md:39`, `:49`); it has the largest attack surface; a listener cannot start a stopped workspace; text B is preserved in ADJ Part 6.3 anyway. Neutral recommendation: **Variant 1, about 55 percent** (close about 40, keep about 5).

### Variant 3 Advocate (analyzer)
Close: the issue body serves one consumer, the watcher, which was built without a listener; the recommended Q4 and Q18 answers meet the ADJ's close condition. Concedes: closing may go against the owner's comment of one day earlier; the review ranks narrow above close; text C is not fully paste-ready, it holds "[link to the comment holding option A]" (ADJ line 661); once closed the gap is less visible; reopening costs a second round of notifications. Neutral recommendation: **Variant 3, about 55 percent**, conditional on the owner answering Q4 "single-host; read-only" and Q18 "no TUIBBS channel yet"; otherwise Variant 1.

### Shared-assumption responses (omission check: none omitted)

| Point | V1 advocate | V2 advocate | V3 advocate |
|---|---|---|---|
| A-001 (the watcher was #477's main purpose) | QUALIFY | QUALIFY | ACCEPT |
| A-002 (cross-repository posting accepted) | QUALIFY | QUALIFY | QUALIFY |
| A-003 (single-host, no TUIBBS screen soon, holds) | REJECT | REJECT | QUALIFY |

Agreed reading of A-001: the issue's written body is entirely about the watcher, but the owner's 2026-11-13 comment adds an alignment purpose the body lacks; narrowing keeps it, closing drops it. A-002: the owner's own account is the only commenter (author association MEMBER on the Coder repository); each post needs its own grant row, and the V3 advocate notes a close is a state change the grant row should name. A-003: observer release R4 (remote fleet) is planned, so the boundary is expected to move; closing hedges with reopen conditions, narrowing is already in place.

### New facts surfaced in the round
- Text C, called paste-ready by ADJ line 606, holds a placeholder "[link to the comment holding option A]" (ADJ line 661). It must be reworded or text A posted first.
- The `issue-write` grant action may not cover a state change (closing); UNVERIFIED.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L1 | none (identical) | 90% | Identical structure by design; agreed. |
| C-001 | L2 | Variant 1 | 62% | 2 of 3: narrowing keeps the observer-visibility gap and the owner's alignment request while dropping the contradicted premise; V3 advocate preferred close conditionally. |
| C-002 | L3 | Variant 1 (tied with Variant 3) | 88% | 3 of 3: no session-start route; Variant 2's guarded route still starts permission-free sessions (checklist item 9). |
| C-003 | L2 | Variant 3 | 80% | 3 of 3: text C needs one fix (the link placeholder); text A has three open items; text B is blocked on #339. |
| C-004 | L2 | Variant 3 | 80% | 3 of 3: only the Q4 one-liner is needed. |
| C-005 | L2 | Variant 1 | 85% | 3 of 3, and the V3 advocate conceded: only narrowing answers "Ensure this aligns with Orchestrator and TUI Panel" concretely. |
| C-006 | L1 | Variant 1 | 60% | 2 of 3: an open issue keeps the gap visible in the repository that must build it. |
| X-001 | L2 | Variant 3 | 62% | 2 of 3: no present consumer exists; R4 is planned, no TUIBBS task package; ADJ: "Unblocks: nothing in IronClaude". |
| X-002 | L3 | Variant 1 (tied with Variant 3) | 92% | 3 of 3, and the V2 advocate conceded: keeping routing contradicts design decision D1 and is "the least defensible" (ADJ line 605). |
| X-003 | L2 | Variant 3 | 70% | 3 of 3: waiting for a task package avoids a stale open design; V1 accepts it "may sit unbuilt". |
| A-001 | L2 | Variant 1 | 62% | 2 of 3: narrowing preserves the non-watcher purpose the owner's comment introduced. |
| A-002 | L2 | Variant 3 (narrowly) | 55% | 2 of 3: smallest cross-repository write; all share the dependency; close needs the grant row to name the state change. |
| A-003 | L3 | Variant 3 (narrowly) | 58% | 2 of 3: its reopen conditions name the boundary change; Variant 1 is better if the boundary moves soon. |

Points won: Variant 1: 6 (C-001, C-002, C-005, C-006, X-002, A-001; two tied with Variant 3); Variant 3: 6 (C-003, C-004, X-001, X-003, A-002, A-003) plus two ties; Variant 2: 0.

## Convergence Assessment
- Points resolved: 13 of 13 (every point at least 2 of 3)
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 (S-001, C-006), L2 (C-001, C-003, C-004, C-005, X-001, X-003, A-001, A-002), L3 (C-002, X-002, A-003): all covered.
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick).
- Status: CONVERGED on points
- Unresolved points: none
- Overall neutral recommendation by the advocates: Variant 1 (narrow), 2 of 3 (60 and 55 percent); the third advocate recommended Variant 3 (close) at 55 percent, conditional on Q4 and Q18. All three agree Variant 2 (keep) is the weakest (about 5 percent or less) and that close is the right answer if the owner states single-host is lasting and no TUIBBS or remote reader is planned.
