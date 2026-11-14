# Q4: what "TUI Panel" means in the owner's comment on Coder#477

## The question, verbatim from the spec row

Source: `merged-requirements.md` section 3, row Q4 (line 531).

> What "TUI Panel" means

Original wording (ADJ Part 7, line 774): "What does "TUI Panel" mean in your 2026-11-13 comment on Coder#477: `superclaude observe` (the #409 dashboard), a future TUIBBS screen reading the snapshot, or both?"

## Recommended answer in the spec

`superclaude observe`; TUIBBS a possible later reader; single-host; read-only (about 70 to 75 percent). The one-line form for the Coder#477 reply: "TUI Panel = `superclaude observe`; single-host; read-only". (`merged-requirements.md:531`; ADJ line 774, line 307)

## Default if unanswered

ADJ working reading: `superclaude observe` "until the owner says otherwise" (ADJ Part 2.7); CO-01 still waits for Q3. (`merged-requirements.md:531`)

## What it gates (work items, in words)

- CO-01: the reply on Coder#477 must state Q4's answer in one line. (section 2, CO-01 row (2))
- Indirectly, Q3: the ADJ's condition for closing Coder#477 is "if the observer stays single-host and TUIBBS is not near" (ADJ line 283); the recommended Q4 line includes "single-host". (ADJ Part 2.5)
- Wave needed by: W0 (asked after Q1, Q33, Q26, Q2, Q3). (`merged-requirements.md:523`)

## Facts the question depends on

| Fact | Source |
|---|---|
| The owner's comment on Coder#477, 2026-11-13T16:20:07Z, reads in full: "Ensure this aligns with Orchestrator and TUI Panel". It is the issue's only comment. | `gh issue view 477 --repo IronbellyOrg/Coder` (read-only, 2026-11-14) |
| Working reading: `superclaude observe` (the #409 dashboard), about 70 percent (R2-V5 5.7) to 75 percent (R2-V3 5.2): the comment's two nouns mirror the titles of #339 (Orchestrator mode) and #409 (the TUI observer dashboard); the phrase "TUI Panel" appears in no owner-written file. A TUIBBS Go screen is the weaker reading, about 15 percent. | ADJ Part 2.7 (line 306) |
| The owner's 2026-11-08 record says "the observer may become a TUIBBS module" and "Background, not deciding". That record exists only in a sibling worktree, not on master. | ADJ line 306; ADJ E-16 (line 142) |
| The ADJ glossary already equates them: "the observer, `superclaude observe`, the 'TUI panel' in the owner's wording". | ADJ glossary (line 77); ADJ line 111 |
| The observer is built and merged (PRs #503, #514), reads Orca on one host only, and is read-only; remote fleet is its planned release R4. | ADJ E-01 (line 127); glossary (line 92) |
| TUIBBS is the owner's separate TUI platform on a different SSH host; "No document in TUIBBS mentions Coder or Orca". Before a TUIBBS screen could read the observer's snapshot, four things are missing: a transport, an identity envelope, an age rule and re-sanitising. | ADJ glossary (line 91); ADJ Part 2.7 (line 306) |
| #409's issue body preferred a Go stack (Bubble Tea v2, Lip Gloss v2, Bubbles v2) "informed by TUIBBS-scp styling and components"; the built observer is a `superclaude` CLI command. | `.dev/issues/409/issue-body.md:25`; ADJ E-01 |
| Both readings are a sequence, not a conflict: a TUIBBS screen would be a second reader of the observer's snapshot, not a second program with its own collector. The answer changes the transport, not the contract. | ADJ Part 2.7 (line 306); `merged-requirements.md:562` |
| Narrowing or closing Coder#477 does not choose what "TUI Panel" means (INV-043). | ADJ line 283 |
| Related later question: Q18 (a channel copying the snapshot to the TUIBBS host): recommended "not before observer release R4 or an owner statement that a TUIBBS screen is planned". | `merged-requirements.md:545` |
