# Q3: Coder#477 (the workspace listener issue): keep, narrow or close

## The question, verbatim from the spec row

Source: `merged-requirements.md` section 3, row Q3 (line 530).

> Coder#477: keep, narrow to read-only status and identity, or close

Original wording (ADJ Part 7, line 773): "Coder#477: keep as written, narrow to read-only status and identity with no prompt routing, or close?"

## Recommended answer in the spec

Narrow (about 65 percent); close if single-host and TUIBBS not near. ADJ adds: "keep only if you revisit the listener options". (`merged-requirements.md:530`; ADJ line 773, line 605)

## Default if unanswered

PLAN INFERENCE: CO-01 not posted; nothing in IronClaude waits: CO-01 is recorded as `skipped (default Q3, date)` and OB-08 becomes eligible (XC-02 (6)). (`merged-requirements.md:530`)

## What it gates (work items, in words)

- CO-01: post the reply on Coder#477 (text A narrow, B keep or C close), stating Q4's answer in one line, after the #450 edits and before the #409 correction pass, by the single issue editor with a fresh `updatedAt` read. (section 2, CO-01 row)
- CO-03: the deferred Coder-repo implementation of the narrowed feature, only after text A is posted, with every item of the nine-point checklist tested. (CO-03 row)
- V2-01 (one clause): the #423 rewrite's "if #477 is kept" clause is settled by this answer. (V2-01 row)
- Wave needed by: W0 (asked after Q1, Q33, Q26, Q2). (`merged-requirements.md:523`)

## Facts the question depends on

| Fact | Source |
|---|---|
| Coder#477 is an issue in a different repository, `IronbellyOrg/Coder`, titled "[FEATURE] Workspace listener, monitor registration and secure prompt routing for every Coder workspace". It is OPEN; its only comment is the owner's of 2026-11-13T16:20:07Z: "Ensure this aligns with Orchestrator and TUI Panel"; `updatedAt` unchanged since then. | `gh issue view 477 --repo IronbellyOrg/Coder` (read-only, 2026-11-14) |
| Its premise (a watcher that sends prompts to a listener) contradicts the built watcher: the watcher design chose a workspace-side poller with no listener, inbound port or address registry (design decision D1 option A, 2026-11-07). | ADJ E-12 (line 138); `docs/designs/issue-watcher.md:39` |
| ADJ verdict: do not build a listener for the watcher. Narrow to read-only workspace status and identity with no prompt routing (about 65 percent); close if the observer stays single-host and TUIBBS is not near; keep as written is the least defensible. | ADJ Part 2.5 (line 283); Part 6.3 (line 605) |
| Any route that can start a session starts it with permission checks off on the stock image; that is "the strongest reason the narrowed version has no send route". | ADJ line 284 (per V3); checklist item 9 (ADJ Part 6.3) |
| The observer (`superclaude observe`, #409) reads one host's Orca only; remote fleet is its planned release R4. TUIBBS, the owner's separate TUI platform, runs on a different SSH host; no TUIBBS document mentions Coder or Orca. | ADJ glossary (line 91); ADJ Part 2.7 (line 306) |
| Three texts exist: A narrow (not fully paste-ready: holds an "owner decides" age placeholder (Q22), an UNVERIFIED owner-token route, and a name that must match the contract note); B keep (not paste-ready until #339's grant format exists); C close (paste-ready, with two reopen conditions). | ADJ Part 6.3 (lines 605 to 606) |
| A nine-item state, guard and boundary checklist applies to any version (stale registration, name reuse, spoofed identity, credential leakage, read-credential escalation, consumed state, version skew, untrusted content, bypass by default). | ADJ Part 6.3, R2-V3 section 5.7 |
| Coder-repo facts and component paths rest on one review (V3) only and are marked "per V3". | ADJ line 280, line 606 |
| What each answer does: narrow means a rewrite with no send route; close means a comment with two reopen conditions. | `merged-requirements.md:562` |
| Q4 (what "TUI Panel" means) decides the transport, not the contract; CO-01 also waits for Q4. Narrowing or closing does not choose what "TUI Panel" means. | ADJ Part 2.7; ADJ line 283 (INV-043) |
| Every post needs its own grant row (`GRANT(CO-01,issue-write)`); posting is reversible (edit or reopen) but a posted comment's notification is not undone. | XC-02 (4); CO-01 row "undo"; ADJ line 101 |
