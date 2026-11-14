# Q5: how the observer and the sweep relate: one contract note, an observer panel on the sweep JSON, or a merge

## The question, verbatim from the spec row

Source: `merged-requirements.md` section 3, row Q5 (line 532).

> One contract note and keep both programs, an observer panel on the sweep JSON, or a merge

Original wording (ADJ Part 7, line 775): "Do you want one written contract note between the observer and the sweep (keep both programs), an optional observer panel that reads the sweep's JSON, or a merge?"

## Recommended answer in the spec

One note; keep both programs (A-012 provisional, X-017). (`merged-requirements.md:532`; ADJ line 775)

## Default if unanswered

ADJ: "proceed as provisional; ask once" (A-012). (`merged-requirements.md:532`; ADJ line 364)

## What it gates (work items, in words)

- XC-05: draft the contract note `docs/designs/observe-sweep-contract.md` on a master-based branch (registry of contracts, units, versioning rule, mapping table of shared words, verb lists per caller, binary resolution, the "candidate join basis" wording until the real-id comparison is done). (section 2, XC-05 row)
- XC-07: link the note from the sweep design and the observer spec and merge the note, its comparison test and the links in one PR (after PR #539 merges and the real-id comparison XC-04). (XC-07 row)
- Wave needed by: W1. (`merged-requirements.md:532`)

## Facts the question depends on

| Fact | Source |
|---|---|
| The two programs exist separately: the observer (`superclaude observe`, #409, merged in PRs #503 and #514) and the sweep (`superclaude sweep run`, #339 Phase 1, PR #539, open). They were built independently from the same design package, mention each other nowhere, and point in the same direction; "aligned in intent and not yet in practice". | ADJ Part 1.1 (line 111); E-03 (line 129) |
| The observer reads Orca only and no sweep file (X-013, 95 percent). | ADJ E-03; line 325 |
| Two JSON files both called "v1": "observe snapshot v1" (rewritten every live cycle, on disk) and "sweep report JSON v1" (stdout only). | ADJ E-05 (line 131) |
| A sweep run always writes one dated report before printing JSON; "a sweep adds exactly one report file" (NFR-001) is pinned by the design and two tests. Running the sweep from a reader writes a report and runs `git status` in every worktree each time. | ADJ E-07 (line 133); Part 8 row X-004 (line 806) and X-013 (line 808) |
| The debate's verdict: one short written note, no runtime link in version 1; neither program reads the other, neither gains a file or key; "the main product of the debate". | ADJ Part 2.3 (line 222) |
| Keep two readers, not one collector (X-017, 70 percent); keep both programs (A-012, 66 percent, provisional; only one review stated it). | ADJ lines 360, 364 |
| Merging was rejected: the facts differ (git, contracts and transcripts versus fleet-wide Orca rows); one collector would break one design's rules (stdlib-only models, the owner-signed exact allow-list); #539 is in review; the observer's only gain for the sweep is paging. A shared parser is revisited after #539 merges. | ADJ Part 8 (line 807) |
| An observer reader of the sweep JSON was rejected for version 1: the sweep's JSON is stdout-only; the snapshot's row keys carry no command, objective, branch, changed paths or issue or PR; an optional panel stays a later owner choice (Q17). | ADJ Part 8 (line 808) |
| The live #409 body (updated 2026-11-13T16:57:51Z) still proposes "one shared set of facts (proposal, needs an owner decision)": "If the observer built its own collector, two programs would classify the same session and could disagree. Reading the sweep's output keeps one definition of 'waiting on a person' or 'stalled'". | `gh issue view 409 --repo IronbellyOrg/IronClaude` (read-only, 2026-11-14), body line 55 |
| Related later questions: Q9 (store the sweep JSON, capture stdout, or neither; recommended Phase 2 caller-side capture first) and Q17 (show sweep facts on the observer screen; recommended "no, not now; if yes later, Q9 becomes a real requirement"). | `merged-requirements.md:536`, `:544` |
| Risk named by the spec: the note's test compares constants, not behaviour; two programs can keep identical words and still mean different things (for example "stale" 45 seconds against 6 hours). | `merged-requirements.md:1160` |
| The note with its test cannot land on master before PR #539 merges; only the draft can run early. | `merged-requirements.md:508` (weak point W4) |
