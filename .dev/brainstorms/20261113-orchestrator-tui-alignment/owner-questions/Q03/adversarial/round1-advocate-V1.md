# Round 1 advocate statement: Variant 1 (narrow Coder#477 to read-only status and identity)

Persona: architect (structure, dependencies, long-term impact). Mode A, depth quick, Round 1.

## Position summary

Narrowing is the only option that keeps the one structural gap #477 still points at (an observer cannot see another workspace) while deleting the dangerous part (any route that can start a session), and it is the only one that gives the owner's comment of 2026-11-13 ("Ensure this aligns with Orchestrator and TUI Panel") a direct answer. Its price is real: text A is not paste-ready and it designs for a consumer (observer R4, a TUIBBS screen) that does not exist yet, so closing (Variant 3) is the honest fallback when the owner says the observer stays single-host with no remote reader planned.

## Steelman

### Variant 2 (keep, with strict guards)

Strongest version: a single poller per workspace is a deliberate limit, not a law. The watcher design itself lists nine revisit conditions under which a listener returns, including "centralized approval or audit becomes necessary" and "a shared ledger becomes necessary" (`docs/designs/issue-watcher.md:60`). If any occurs, the owner will need exactly the design text B already writes: a fixed request list (`claim` plus one integer, mirroring decision D3), signed, expiring, one-use grants, separate read and request credentials, a rate cap, a joinable audit, and written acceptance of each started session's permission mode (ADJ:651-658). Text B is the most thoroughly guarded send design on record, and it is the only variant that keeps the owner's original feature idea rather than replacing it.

Critique: none of those conditions is shown to have occurred (no source in question.md records one; UNVERIFIED that none has). The watcher design says #477 returns "only on a revisit condition" (`docs/designs/issue-watcher.md:49`), so keeping it now inverts the design's own dependency order. Text B is blocked on a grant format that does not exist (ADJ:606, ADJ:655 "the route stays disabled until it exists"), so the issue would sit open and unbuildable. And it keeps a remote path to a session that starts with permission checks off on the stock image (ADJ:284; ADJ:673 item 9; on this host E-11, ADJ:137). The ADJ calls it "the least defensible" (ADJ:283, ADJ:605).

### Variant 3 (close as superseded, two reopen conditions)

Strongest version: the issue's whole written premise is the watcher. Its Problem Statement opens "The owner describes a sibling IronClaude watcher that needs to reach the intended workspace" and its Proposed Solution routes `/sc:issue --claim <N>` to "the workspace listener" (`gh issue view 477 --repo IronbellyOrg/Coder`, read 2026-11-14). The watcher was designed with no listener, inbound port or address registry (`docs/designs/issue-watcher.md:43`), and that design states verbatim "Option A makes IronbellyOrg/Coder#477 unnecessary unless B or C is revisited" (`docs/designs/issue-watcher.md:49`). Text C is the only text the ADJ marks paste-ready (ADJ:606), needs no Q22 number and no owner-token route, and its two reopen conditions are concrete and checkable (ADJ:661). It matches the present boundary: the observer reads one host's Orca only and no TUIBBS document mentions Coder or Orca (ADJ:306). Closing also costs the Coder repo nothing to maintain, and an open issue invites someone to build it.

Critique: (1) closing overrides the owner's one-day-old comment, which asked for alignment, not removal; Variant 3 admits this (variant-3 "What it costs or risks" bullet 1). (2) Text C is not fully self-contained: it carries the placeholder "[link to the comment holding option A]" (ADJ:661), so the narrowed text must be published somewhere a Coder reader can follow; a ledger entry on an IronClaude branch is not that place, and variant-3 step 2 leaves this as "in the ledger (or in the closing comment's link)". (3) The design facts the narrowed text records (identity from the Coder control plane, key by workspace id, the anonymous collector `collector/app.py:5` cannot be reused, no standing credential in Coder's stores; ADJ:284, ADJ:665-673) live only in IronClaude review files after a close; the Coder repo, where a later listener would be built, would hold only a "superseded" comment.

## Strengths claimed

1. **Removes the largest risk structurally, not by policy.** Text A's acceptance criterion 4 says "This feature has no prompt, command or session-start route. A test shows the route rejects every non-read request" (ADJ:632). Checklist item 9 calls the permission-off launch "the strongest reason the narrowed version has no send route" (ADJ:673). Variant 2 guards that route; Variant 1 deletes it.
2. **Keeps the only real remaining need in the system that would own it.** Text A's Problem Statement: "the observer reads one host's Orca only (remote fleet is its release R4 ...) and cannot see another workspace" (ADJ:623). Workspace identity and running state can only come from the Coder control plane (ADJ:284, ADJ:626), so the Coder repo is the right owner of that record. Closing leaves the dependency undocumented in the repo that must satisfy it.
3. **Records the architectural contract once, in the right place.** ADJ Part 2.7 says "the contract holds under all three readings; the answer changes the transport, not the contract" (ADJ:306). Text A writes that contract as testable criteria: identity from Coder, rejected spoofed ids, no stored address or credential, a named versioned record with an age, owner-only reads, an audit line (ADJ:629-636). CO-03 then binds any build to the nine-item checklist and a written read-permission model (`merged-requirements.md:355`). That prevents the anonymous-collector shortcut (`collector/app.py:5`, per V3) from being reused later.
4. **Answers the owner's explicit instruction.** The owner's only comment asks that #477 "aligns with Orchestrator and TUI Panel" (gh issue view 477, comment 2026-11-13T16:20:07Z). Text A names `superclaude observe` (#409) and "a possible later TUIBBS screen" as its readers (ADJ:620), which is the Q4 working reading (ADJ:306-307). It is the only variant that converts that instruction into a scoped design rather than keeping (V2) or dropping (V3) the original.
5. **Matches the ADJ verdict.** Narrow is the recommended answer at about 65 percent (ADJ:283, ADJ:605; `merged-requirements.md:530`).
6. **Settles downstream clauses cleanly.** The #423 rewrite's "if #477 is kept" clause (V2-01) and Q16's "Coder#477 promise neither" default (`merged-requirements.md:543`) both resolve without a grant format, because a read-only route needs none.
7. **Reversible.** Posting is an edit or reopen away from either other state (`merged-requirements.md:353`, undo column "yes (edit or reopen)").

## Weaknesses identified in other variants

1. **V2 contradicts a built design and its own preconditions.** The watcher design's D1 option A has "No listener, inbound port or address registry" (`docs/designs/issue-watcher.md:43`); #477 returns "only on a revisit condition" (`:49`). V2's step 1 asks the owner to revisit D1 without naming which of the nine conditions (`:60`) has occurred.
2. **V2 is unbuildable on arrival.** Text B is "not paste-ready until the grant format of #339 exists" (ADJ:606), and Q16's recommended answer is one vocabulary and one audit format, not one trust design (`merged-requirements.md:543`); the format does not exist.
3. **V2 has the largest attack surface.** Every accepted request starts a session with permission checks off on the stock image (ADJ:284; ADJ:654 text B criterion 4). A listener also "cannot start a stopped one" (ADJ:284, R2-V3 5.1), so it does not even serve stopped workspaces.
4. **V2's "orchestrator of orchestrators" alignment is speculative.** The orchestrator that manages work is unbuilt; aligning a send route to it now designs against a component that does not exist.
5. **V3 depends on A-003 holding.** Its case rests on "the observer is single-host and no TUIBBS screen is planned" (variant-3 "What it unlocks" bullet 3). R4 (remote fleet) is a planned observer release (question.md fact row 5), so the boundary is expected to move.
6. **V3's text C carries an unresolved link** ("[link to the comment holding option A]", ADJ:661), so "paste-ready" is true only once text A is published somewhere public to the Coder repo; that partly recreates V1's work.
7. **V3 discards the owner's stated intent without the owner saying so** (variant-3 risk 1; the comment is the issue's only one and is one day old).

## Concessions

1. **Text A is not paste-ready.** It holds `[N minutes: owner decides]` (Q22), an UNVERIFIED owner-token route, and the name "observe snapshot v1" that must match the contract note (ADJ:606; CO-02, `merged-requirements.md:354`). V3 needs none of this.
2. **It designs for absent consumers.** Text A itself says "Depends on: ... observer release R4" (ADJ:648). R4 and any TUIBBS screen are not scheduled; Q18 recommends no snapshot channel before R4 or an owner statement (`merged-requirements.md:545`). The issue may sit open and unbuilt for a long time.
3. **Tension with the recommended Q4 line.** Q4's recommended answer is "TUI Panel = `superclaude observe`; single-host; read-only" (ADJ:307). The ADJ's own close condition is "if the observer stays single-host and TUIBBS is not near" (ADJ:283). If the owner accepts Q4's line as a lasting statement, not just today's scope, close becomes the consistent answer.
4. **An open, narrowed issue can still be built wrongly.** A later Coder change could add a send route without the checklist (variant-1 risk 3); an open issue invites work that a closed one does not.
5. **Coder-repo paths rest on V3 alone** ("per V3", ADJ:606), so text A's Components Affected list is the least verified part.
6. **The issue's written premise is the watcher.** Its body never mentions an observer; text A replaces the problem statement rather than narrowing it. "Narrow" is closer to "close and reopen with a new problem" than the label suggests.

## Shared assumption responses

| A-NNN | Response | Reason |
|---|---|---|
| A-001 | QUALIFY | The issue body supports it: its Problem Statement and Proposed Solution are entirely about the #331 watcher, and "the monitor" is that watcher (gh issue view 477). But the owner's later comment adds Orchestrator and TUI Panel scope that the body does not contain; that added purpose is not the watcher's, so closing loses it while narrowing keeps it. The assumption holds for the written body, not for the owner's latest intent. |
| A-002 | QUALIFY | The repository is in the same organization and the owner has already engaged on #477 (comment author `ironbelly`, `viewerDidAuthor: true`, so the posting account is the owner's). Every post still needs `GRANT(CO-01,issue-write)` (question.md fact row 10). Whether other Coder-repo maintainers accept IronClaude-driven edits is UNVERIFIED; the grant row is the only acceptance on record. |
| A-003 | REJECT | The boundary is planned to move: R4 (remote fleet) is the observer's planned release (question.md fact row 5; ADJ:623), and the ADJ treats single-host as a condition the owner must state, not a given ("if the observer stays single-host", ADJ:283). V1 does not depend on it; V3 depends on it and only mitigates its failure with reopen conditions. |

## Per-point positions

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | none (identical) | 50 | Same five sections by brief design; no difference to judge. |
| C-001 | V1 | 60 | Keeps the observer-visibility need and the owner's alignment request while removing the listener; V3 is close behind if the owner states single-host as lasting. |
| C-002 | V1 (tie with V3) | 85 | No session-start route; V1 enforces it with a testable criterion (ADJ:632), V3 by closing; V2's guarded route still starts permission-off sessions (ADJ:673). |
| C-003 | V3 | 75 | Text C is the only one the ADJ marks paste-ready (ADJ:606), despite its link placeholder (ADJ:661). |
| C-004 | V3 | 75 | Only the Q4 one-liner; V1 adds Q22 or a kept placeholder; V2 adds a D1 revisit, the grant format and Q16. |
| C-005 | V1 | 70 | Only V1 turns "aligns with Orchestrator and TUI Panel" into a concrete scope; V2 keeps the old intent, V3 admits it may not match. |
| C-006 | V1 | 60 | The contract stays in the repo that must build it; V3's ledger copy is not reachable from the Coder repo unless linked publicly. |
| X-001 | V1 | 60 | A real gap exists (observer cannot see another workspace, ADJ:623) but has no present consumer; V3's "no present consumer" is also true, so the margin is small. |
| X-002 | V1 (tie with V3) | 90 | Keeping prompt routing contradicts D1 (`issue-watcher.md:43,49`) and is "the least defensible" (ADJ:605). |
| X-003 | V3 | 55 | Writing a design for absent consumers risks it going stale; V1's counter is that the contract is reading-independent (ADJ:306). Close call. |
| A-001 | V1 | 60 | Narrowing preserves the non-watcher purpose the owner's comment introduced; closing assumes none exists. |
| A-002 | equal | 50 | All three post to the Coder repo under the same grant row; no variant differs here. |
| A-003 | V1 | 70 | V1 is robust to the boundary moving; V3 is correct only while it holds. |

## Overall

If neutral, I would recommend **Variant 1 (narrow)** at about **60 percent** confidence, with **Variant 3 (close)** as the right answer if the owner, when answering Q4, states that single-host is lasting and no TUIBBS or R4 reader is planned. Variant 2 should not be chosen unless the owner first names which revisit condition in `docs/designs/issue-watcher.md:60` has occurred (confidence about 90 percent that V2 is the weakest).
