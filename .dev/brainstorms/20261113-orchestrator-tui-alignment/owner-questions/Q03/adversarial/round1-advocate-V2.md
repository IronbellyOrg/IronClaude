# Round 1 advocate statement: Variant 2 (keep Coder#477's listener and prompt routing, rewritten with strict guards)

Persona: backend (data integrity, scalability, fault tolerance). Mode A, depth quick, Round 1.

## Position summary

Variant 2 is the only answer that writes guards onto the routing the issue actually asks for (fixed request list, one-use expiring grants, separate read and request credentials, refuse-not-queue, joinable audit), and it keeps the route disabled until #339's grant format exists. As its advocate I must also report that the sources make it the weakest of the three today: no revisit condition of the watcher design has been recorded, so keeping a send route contradicts a binding owner decision.

## Steelman

**Variant 1 (narrow to read-only status and identity).** Strongest version: the owner's comment of 2026-11-13 ("Ensure this aligns with Orchestrator and TUI Panel", `gh issue view 477 --repo IronbellyOrg/Coder`) adds a purpose the original body never had, a read source for the observer. Narrowing keeps that purpose and the one real gap ("the observer reads one host's Orca only ... and cannot see another workspace", ADJ Part 6.3 text A Problem Statement). It also keeps the sound data-integrity rules: identity from the Coder control plane, not self-reported; keyed by workspace id, never by name; stale records reported as stale (ADJ line 284; checklist items 1 and 2). It removes the most dangerous part outright, with a test that the route rejects every non-read request (text A, fourth acceptance criterion). It is the debate's recommendation at about 65 percent (ADJ line 283, line 605).

**Variant 3 (close as superseded).** Strongest version: the issue's own premise is the watcher. Its Problem Statement reads "a sibling IronClaude watcher that needs to reach the intended workspace", and the watcher was built with "No listener, inbound port or address registry" (`docs/designs/issue-watcher.md:43`). The design states #477 is "unnecessary unless B or C is revisited" (`issue-watcher.md:49`). Today the observer is single-host and no TUIBBS screen is planned (ADJ Part 2.7, line 306), so nothing consumes a narrowed design. Closing needs no new owner decisions (no Q22 age, no UNVERIFIED owner-token route), writes no design against consumers that do not exist, and its two reopen conditions are concrete and tied to recorded triggers (`issue-watcher.md:60`, the nine revisit conditions; observer R4 or a TUIBBS task package).

## Strengths claimed

1. **It is the only variant that puts guards on the feature as the issue states it.** The issue's acceptance criteria call for "An authorized monitor request reaches the intended registered workspace and is handed to its project's orchestrator to start a new session" (Coder#477 body). Text B replaces that with a fixed request list ("For the issue watcher the only type is `claim` plus one integer issue number (IronClaude decision D3)"), no free text to a prompt, and no requester-chosen flag, working directory or permission mode (ADJ Part 6.3 text B, criteria 2 and 3). If a revisit condition ever fires, the routing returns with these guards rather than as the unguarded original.
2. **Strongest replay and fault-tolerance guards of the three.** Text B requires sender identity, a grant naming the workspace, request type, expiry and a one-use nonce; unsigned, expired, wrong-workspace and replayed requests are rejected and logged (text B criterion 5). A request for a stopped, stale or deleted workspace "is refused with a reason; it is never queued", and a per-type rate cap applies, 6 a day for the watcher (criterion 6). Refusing instead of queueing avoids a backlog that replays when a workspace restarts.
3. **Credential separation prevents read-escalation.** "Reading status and sending a request use separate credentials; a read credential is rejected by the request route; a test shows it" (text B criterion 7), matching checklist item 5 ("the observer must never hold a credential that can [start a session]").
4. **Audit joinable across stores.** Each decision is audited "and can be joined to the watcher's `audit.jsonl` by issue number and workspace id" (text B criterion 8). Neither text A nor text C gives a cross-store join key for routing decisions.
5. **Fail-closed by default.** "The route stays disabled until it exists" (text B criterion 5), and the owner must accept every started session's permission mode in writing (criterion 4). Nothing can run before the grant format and a live test exist.
6. **Its revisit path is real, not invented.** The watcher design keeps options B and C alive "only on a revisit condition" (`issue-watcher.md:49`), and three of the nine conditions are the routing case: "stopped workspaces cause excessive waiting", "centralized approval or audit becomes necessary", "a shared ledger becomes necessary" (`issue-watcher.md:60`). FU-1 has not been recorded and the watcher is not enabled (`issue-watcher.md:33`), so "recurring workspace execution proves impossible" is not yet ruled out either way (UNVERIFIED).

## Weaknesses identified in other variants

1. **Variant 1 designs for consumers that do not exist.** Its own costs section says the design's consumers (observer R4 remote fleet, a TUIBBS screen) "do not exist yet; it may sit unbuilt". Before any TUIBBS screen could read anything, four things are missing: transport, identity envelope, age rule and re-sanitising (ADJ line 306). An open issue with acceptance criteria and no consumer becomes a stale spec.
2. **Variant 1 is not paste-ready and rests on one review.** Text A holds `[N minutes: owner decides]` (Q22), an UNVERIFIED owner-token route, and the name "observe snapshot v1" that must match the contract note (ADJ line 606). Its Components Affected paths are "per V3" only (ADJ line 606). It also creates another copy of the observer snapshot and a per-workspace record, which adds to the data-store count ADJ already flags (ADJ line 296, "at least an eighth data store" for the catalogue; whether the narrowed record counts as another is PLAN INFERENCE).
3. **Variant 1 still carries data-integrity risk without a send route.** Records come from workspaces that read untrusted issue and repo text (checklist item 8); a read route that returns "the watcher's status counts" and "the observer snapshot" (text A Proposed Solution) is a channel for untrusted strings to the observer. Text A's criteria require an audit line and authentication but do not state the re-sanitising rule as an acceptance criterion (text A criteria list, ADJ lines 629 to 636).
4. **Variant 3 contradicts the owner's most recent statement.** The owner commented one day ago asking that the issue align with Orchestrator and TUI Panel (Coder#477 comment, 2026-11-13T16:20:07Z). Variant 3 admits "closing it may not match that intent".
5. **Variant 3's text C is not fully paste-ready.** Text C contains the placeholder "[link to the comment holding option A]" (ADJ line 661). Either text A must first be posted somewhere linkable, which is a second write, or the link is removed and the narrowed design survives only in the ledger. ADJ line 606 calls C paste-ready; that holds only if the bracket is resolved.
6. **Variant 3 records the real gap only in a closing comment.** The observer's single-host limit is a known gap; closing leaves it with no open tracker until R4 or a TUIBBS task package appears, and reopening costs a second round of notifications (variant 3 costs section; XC-02 (4): a notification is not undone).

## Concessions

1. **Variant 2 contradicts a binding owner decision with no recorded trigger.** D1 option A is a verbatim owner decision ("D1 option A (workspace-side poller, pull)", `issue-watcher.md:39`), and #477 returns "only on a revisit condition: the workspace cannot run a reliable cron, or one poller per login becomes unworkable" (`issue-watcher.md:49`). No source shows a condition has occurred. Revisiting now is premature.
2. **Largest attack surface.** Any route that can start a session starts it with permission checks off on the stock image (ADJ line 284, checklist item 9). Guards reduce, but do not remove, a remote path into a permission-free session.
3. **A listener cannot start a stopped workspace** (ADJ line 284, R2-V3 5.1). A push design fails exactly when work arrives for a stopped workspace; the poller simply runs when the workspace runs. Refuse-not-queue (strength 2) is a mitigation, not a fix.
4. **Unbuildable and long-lived open.** Text B is "not until the grant format of #339 exists" (ADJ line 606). The issue would stay open with a disabled route, which invites someone to build part of it.
5. **The "orchestrator of orchestrators" alignment is weak.** "v2" has at least three meanings (ADJ line 294, E-13); variant 2 claiming alignment with one of them does not hold up.
6. **The guards are not lost if variant 2 loses.** Text B is preserved verbatim in ADJ Part 6.3 (lines 650 to 658), so strengths 1 to 5 survive as a ready rewrite for a future revisit whichever answer the owner gives. That removes most of the reason to keep the issue open now.

## Shared assumption responses

- **A-001 (the watcher was #477's main purpose): QUALIFY.** The body supports it: the Problem Statement is the watcher ("a sibling IronClaude watcher that needs to reach the intended workspace") and the User Story ends "so that a new session can be started for an eligible issue" (Coder#477 body); "monitor registration" there means "securely associating workspace reachability information" for routing. But the owner's comment of 2026-11-13 adds a second purpose (alignment with Orchestrator and TUI Panel) that the body lacks. So "no separate purpose" was true of the body and is no longer true of the issue. Narrowing keeps that second purpose; closing drops it.
- **A-002 (cross-repository posting is accepted): QUALIFY.** The comment's author is `ironbelly` with `authorAssociation: MEMBER` on IronbellyOrg/Coder (gh issue view, read 2026-11-14), and every post needs its own grant row (`GRANT(CO-01,issue-write)`, XC-02 (4)), so the owner's consent is the mechanism. Whether the Coder repo has other maintainers or readers who must agree is UNVERIFIED.
- **A-003 (single-host, no TUIBBS screen soon, holds for the life of the decision): REJECT.** Remote fleet is the observer's planned release R4 (ADJ line 91, per question.md), and the owner's 2026-11-08 record says "the observer may become a TUIBBS module" (ADJ line 306). The boundary is expected to move. The assumption only needs to hold until the next revisit, because every answer is reversible by edit or reopen (ADJ line 285, "Undo: yes"); variant 3's reopen conditions are the explicit hedge for this.

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (identical) | 95 | Same five sections by design of the brief; no difference to judge. |
| C-001 | V1 | 60 | Keeps the owner's new observer purpose and the real gap while dropping the contradicted premise; V3 a close second. |
| C-002 | V1 | 85 | No session-start route, and a test that the route rejects every non-read request; V3 equal on safety but drops the read need. |
| C-003 | V3 | 85 | Text C needs only the link placeholder resolved; A has three open items, B is blocked on #339. |
| C-004 | V3 | 80 | Only Q4's one line; V2 needs a revisit of D1, the grant format and Q16. |
| C-005 | V1 | 75 | Answers the comment concretely ("aligned as a read-only source for the observer"); V3 admits the mismatch; V2 ignores the comment's new purpose. |
| C-006 | V3 | 55 | Keeps text A linked without an open issue implying work; depends on the link actually being posted. |
| X-001 | V3 | 60 | Strictly "present need": no consumer exists (R4 planned, no TUIBBS task package); V1 states a real gap but not a present consumer. |
| X-002 | V1 | 90 | Removing prompt routing follows D1 and checklist item 9; ADJ calls keep "the least defensible". V3 equally right on this point. |
| X-003 | V3 | 65 | Waiting for a task package avoids a stale spec; V1 accepts "may sit unbuilt". |
| A-001 | V1 | 65 | If registration has a purpose beyond the watcher, narrowing loses the least of it. |
| A-002 | V3 | 55 | One post and a close is the smallest cross-repo write; all three share the dependency. |
| A-003 | V3 | 65 | Its reopen conditions name the boundary change (R4, TUIBBS task package) explicitly. |

## Overall

If I were neutral I would recommend **Variant 1 (narrow)** at about 55 percent, with **Variant 3 (close)** at about 40 percent and **Variant 2 (keep)** at about 5 percent. Narrow wins narrowly because the owner's comment of one day ago asks for alignment, which a close does not give, and its identity-from-control-plane and key-by-id rules are the right data-integrity base. Close is the better choice if the owner confirms single-host and no TUIBBS screen soon, as ADJ already says. Keep should wait for one of the nine recorded revisit conditions; text B stays available in ADJ Part 6.3 for that day.
