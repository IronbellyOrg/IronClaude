# Refactoring Plan: Merge into Base (Variant 5)

## Overview
- Base: Variant 5 (review 05, "The built `superclaude observe` versus Orchestrator mode (#339)", `variant-5-original.md`). Selection and scores: `base-selection.md` (V5 0.915, V2 0.893, margin 2.2 points, tiebreaker V5 18 of 36 matrix points).
- Incorporating strengths from: V1 (`variant-1-original.md`, `round2-rebuttal-V1.md`), V2 (`variant-2-original.md`, `round2-rebuttal-V2.md`), V3 (`variant-3-original.md`, `round2-rebuttal-V3.md`), V4 (`variant-4-original.md`, `round2-rebuttal-V4.md`); the V5 Round 2 contract (`round2-rebuttal-V5.md` section 5); and the Round 2.5 invariant probe (`invariant-probe.md`).
- Planned changes: 22 (numbered below).
- Risk level (overall): Medium. The merged output is a document, so no code or repository state changes; the risk is that a recommendation is wrong or stale. Two things raise it above Low: the document drives a security decision (INV-008) and it will be used to edit four GitHub issues, whose bodies move (A-010, INV-030).
- **Debate status, carried and not waived: BLOCKED_BY_INVARIANTS.** The invariant probe found one HIGH and UNADDRESSED invariant, INV-008 (the open Codex security thread on PR #539 is not closed by the suggested fix). `debate-transcript.md` "Convergence Assessment" records agreement 100 percent on the 36 X and A points, taxonomy covered, and this one blocking invariant. Accepting a security risk in an open PR is the owner's decision, so the merged output carries INV-008 as the first, blocking action and the return contract carries `status: BLOCKED_BY_INVARIANTS` with INV-008 listed under unresolved items. The merge executor must not rewrite this status to "converged" or "success".
- Output file: the merged output is one adjudicated document titled "Alignment findings, decisions and course of action", written to the path the lead names (default `<D>/merged-output.md`, D = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/`). It is not a copy of V5.
- Audience and language: the owner, and a downstream `/sc:brainstorm`. Plain English; no em dashes; every internal id (WC-16, NFR-001, NFR-014, FU-1, AC-S, Q-1, OB-H gates, TUIBBS, QUESTION-OBSERVATION) is glossed on first use (this repairs V5's L4 miss; see Change 22).
- Source discipline for the merge executor: read-only. It posts nothing to GitHub, edits no issue, no checkout and no PR. Every citation keeps the form used in its source file (path:line, `#N`, sha or `updatedAt`); anything the debate marked UNVERIFIED stays UNVERIFIED. Where this plan adds a point that no debate file states (marked "PLAN INFERENCE"), the merged output must mark it the same way.

## Planned Changes

Source ids: V1..V5 = the five variants; "R2-Vn" = `round2-rebuttal-Vn.md`; "R1-Vn" = `round1-advocate-Vn.md`; X, A, S, C, U ids = `diff-analysis.md`; INV = `invariant-probe.md`; "matrix" = the Scoring Matrix in `debate-transcript.md`.

### Change 1: Rebuild the base as a decision document, keep its evidence (from Variant 5, whole file)
- **Source**: V5, all sections.
- **Target**: Base, whole file (restructure). V5's report order (scope read, what the observer is, overlap, re-test, corrections, decisions, questions, verdict) becomes the Part 1 to Part 8 structure below. V5 "Scope read" moves to a short Appendix A (sources and what was not read); V5 sections 1 to 10 of "What `superclaude observe` is today" are condensed into Part 1 facts and Part 2.1 and kept in full by reference to `variant-5-original.md`.
- **Rationale**: the owner needs decisions and an order of work, not a review narrative; A-011 (92 percent) and A-010 (93 percent) show that reports quoting moving text in parallel produced conflicting edits. V5 holds the only correct premise (X-012, 98 percent).
- **Integration point**: new top-level skeleton (see "Final Structure"); each V5 section is re-homed, not rewritten, where its content survived Round 2.
- **Risk**: Medium. Detail lost in condensing. Mitigation: Appendix A names the V5 section for each condensed block.

### Change 2: Replace the V5 verdict with the adjudicated verdict (from V5 "Verdict", R2-V5 section 2 "Net effect")
- **Source**: V5 Verdict (bullets 1 to 5), R2-V5 section 2 last paragraph, matrix.
- **Target**: Part 1.1 (replace).
- **Rationale**: V5's verdict says "All four earlier reviews and the #409 body were wrong about one fact". X-019 (87 percent, no variant won): that overgeneralises. The accurate wording is "V1 stated that no observer exists; V2 W-10 and V4 F13 and its proposals (a) and (b) assumed it; V3 wrote generically and did not check." It was conceded by R1-V5 (concession 7) and R2-V5 row 1.
- **Integration point**: Part 1.1 uses the draft wording given in the Part 1 specification.
- **Risk**: Low.

### Change 3: Add a list of findings the debate withdrew or disproved (from R2-V1 to R2-V5 section 1, INV-008, INV-017, INV-037, INV-041)
- **Source**: R2-V1 section 1 "Net", R2-V2 section 1 "Net", R2-V3 section 1 "Net", R2-V4 section 1 rows, R2-V5 section 1 and the paragraph after its table; invariant-probe rows named.
- **Target**: new Part 1.3 (insert).
- **Rationale**: so no reader re-raises a dead finding. `step3-quantitative.md` section 2 lists 8 items withdrawn in full for V1, 0 for V2 and V3, 1 for V4, 2 for V5, plus narrowed items.
- **Integration point**: table "Finding | Where it came from | Why it fell | Evidence | What stands instead"; content in Part 1 specification.
- **Risk**: Low. Wrongly listing a surviving finding as dead is the failure mode; the list uses each advocate's own concessions, not the orchestrator's reading.

### Change 4: Part 2.1 observer and #409 (from V5 S1 to S10, O-06, O-09, D5, D6, D8; V1 C-07, C-25, C-34; INV-001 to INV-005, INV-014, INV-017, INV-018, INV-023, INV-024, INV-041, INV-044)
- **Source**: V5 "What `superclaude observe` is today" parts 1 to 10; V5 decisions D5, D6, D7, D8; V1 C-07, C-25, C-34, W-7; invariant-probe rows listed.
- **Target**: Part 2.1 (restructure, with the guard-flip prerequisites as a numbered checklist).
- **Rationale**: X-012 (98), X-013 (95), X-018 (74), A-003 (96), A-015 (83). R2-V5 rows 4, 5, 8 withdrew O-05 and the D5(ii) recommendation; the flip now waits on a seeded consumption test and on the owner's own scope sentence (R2-V5 row 8, D-1).
- **Integration point**: see Part 2.1 specification.
- **Risk**: Medium. The flip rests on facts that live in a sibling worktree (A-015, INV-002).

### Change 5: Part 2.2 sweep, #339 and PR #539, with INV-008 as the first, blocking action (from V1 F-07 and C-18, R2-V1 sections 3 and 5, R2-V5 section 3 A-004 and 5.8, invariant-probe INV-008, INV-009, INV-010, INV-022, INV-033, INV-036, INV-037, INV-039, INV-040)
- **Source**: as listed.
- **Target**: Part 2.2 (insert as the second system section; INV-008 is its first item).
- **Rationale**: INV-008 is the only HIGH and UNADDRESSED invariant; it is a measured result (git 2.47.3, temp repo, the sweep's exact argv): `core.fsmonitor` hook and a `filter.*.clean` command both ran in a linked worktree; `-c core.fsmonitor=false` stopped only the first. The debate only said "resolve or formally accept" the thread (R2-V5 5.9 step 2, R2-V1 A-004). INV-037: "a CI re-run alone does not refresh the merge commit" corrects R2-V1 and R2-V2 A-004.
- **Integration point**: see Part 2.2 specification.
- **Risk**: High as a subject (security), Medium as a text change: the document must state the requirement and the options and not invent the fix design.

### Change 6: Part 2.3 the integration contract (from R2-V5 section 5, with additions from V2 W-10, V4 5.2, INV-006, 013, 017 to 020, 023, 028, 031, 035, 042)
- **Source**: R2-V5 5.1 to 5.9; R2-V2 section 3 X-006 row; R2-V4 section 3 X-006 row; invariant-probe rows listed.
- **Target**: Part 2.3 (insert; V5 O-01 to O-16 and "Facts each program owns" fold into it).
- **Rationale**: R2-V5 section 2 "Net": "the contract in section 5 is now needed by three other variants' proposals ... which makes it the main product of the debate". X-006 (74), A-014 (94), X-008 (91), A-002 (82), A-012 (66).
- **Integration point**: the note's content is specified in Part 2.3; the merged output states the content and where the note will live (`docs/designs/observe-sweep-contract.md`), it does not create the note.
- **Risk**: Medium. The note has no test to keep it true (INV-042); the plan adds that requirement.

### Change 7: Part 2.4 issue watcher #331 and #450 (from V2 W-01 to W-16, "Proposed edits to #450"; R2-V2 sections 3 and 5; INV-007, INV-011, INV-012, INV-016, INV-034)
- **Source**: V2 findings table, R2-V2 5.1 to 5.7.
- **Target**: Part 2.4 (insert).
- **Rationale**: X-001 (91, CONFIRMED: `issue.md:43,88`, `launch.py:33`), X-003 (78), A-008 (83). INV-012 (HIGH, ADDRESSED in R2-V2 5.1, 5.5, 5.6 and R2-V3 5.5) is absent from the one-paragraph consensus; the probe asks that "FU-1 records the real session argv, `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS`, and the owner accepts the mode in writing" be an explicit precondition.
- **Integration point**: FU-1 precondition list in Part 2.4.
- **Risk**: Medium. The facts about permission mode are verified on this host only (INV-011); other hosts UNVERIFIED.

### Change 8: Part 2.5 Coder#477 (from V3 F1, F2, F6, F8, F10 to F14, F17; R2-V3 5.1 to 5.7)
- **Source**: V3 findings and R2-V3 sections 5.1 to 5.7.
- **Target**: Part 2.5 (insert).
- **Rationale**: R2-V3 5.1: for the watcher a listener is not needed (`issue-watcher.md:28,43,47-49`); the premise of #477 contradicts the built watcher (X-001 family). V3 has zero withdrawn findings (strict survival 1.000); its losses were proposals (Edit 5, Edit 8).
- **Integration point**: recommendation "narrow, about 65 percent, after the owner answers D-1 and D-2" with the three rewrites referenced, not copied.
- **Risk**: Medium. Several V3 facts are Coder-repo facts that no other variant re-checked (R2-V3 states which); keep them marked "per V3".

### Change 9: Part 2.6 Orchestrator v2 (#423) and the trust design (from V4 F1, F7, F9, F14; R2-V4 5.1 to 5.7; INV-021)
- **Source**: V4 findings and R2-V4 sections 5.1 to 5.7.
- **Target**: Part 2.6 (insert).
- **Rationale**: R2-V4 5.1: "v1" and "v2" have three meanings (INV-021 adds that at least five numbering namespaces are in play). X-005 (66, owner decision): one grant vocabulary, not one trust design. V4 F14 (determinism boundary) was supported by V5 (U-008).
- **Integration point**: rewrite of #423 and the #339 comment are referenced in Part 6, not repeated.
- **Risk**: Medium. V4 has the lowest weighted survival (0.818); only the items that survived Round 2 enter.

### Change 10: Part 2.7 the "TUI panel" question (from R2-V5 5.7, R2-V3 5.2, R2-V3 D-2, INV-043)
- **Source**: as listed.
- **Target**: Part 2.7 (insert, short).
- **Rationale**: only the owner can settle it (R2-V3 D-2, R2-V5 D-4); the contract holds under all three readings (R2-V5 5.7). INV-043: narrowing or closing Coder#477 does not choose a reading.
- **Integration point**: state the working reading (the observer, about 70 to 75 percent), the weaker reading (TUIBBS, about 15 percent), and the one-line owner answer that settles it.
- **Risk**: Low.

### Change 11: Part 3 point register for every point (from the matrix and all R2 section 3 tables)
- **Source**: matrix (36 X and A points with winner and mean confidence); R2-V1 to R2-V5 section 3 (13 contested points, final verdicts and courses of action); diff-analysis X, A, C, U rows.
- **Target**: Part 3 (insert). Specified in full in "Part 3 Content Specification" below.
- **Rationale**: the lead requires id, verdict, confidence, evidence, owner decision with recommendation, course of action, dependencies and reversibility for every point.
- **Integration point**: one table per system, same eight columns, same order as Part 2.
- **Risk**: Low to Medium. Confidence numbers are the matrix mean; the matrix cell text is truncated in the transcript, so the evidence column uses the diff-analysis and R2 wording.

### Change 12: Part 4 dependency graph and merge or implementation order (from R2-V5 5.9, R2-V4 A-011 row, R2-V1 section 5 item 5, INV-001, 002, 029, 031, 033, 036, 037)
- **Source**: as listed.
- **Target**: Part 4 (insert; replaces V5 "Dependencies for integrating Orchestrator mode with `observe`" table).
- **Rationale**: R2-V5 5.9 lists merge order without the probe corrections; INV-037 (re-run does not refresh the merge commit), INV-029 (the routing row is not one row for the two machine-read tables) and INV-031 (the branch that carries the note) change steps.
- **Integration point**: text graph plus a numbered order across the nine named items.
- **Risk**: Medium. Order depends on owner answers that do not exist yet; each step states what it waits for.

### Change 13: Part 5 invariant probe table (from invariant-probe.md)
- **Source**: all 44 rows; HIGH and MEDIUM UNADDRESSED with actions.
- **Target**: Part 5 (insert).
- **Rationale**: the invariant probe is the debate's last gate; its 28 UNADDRESSED rows are the gaps in the fixes the consensus proposed, not in its direction (probe summary).
- **Integration point**: table "id | severity | what is wrong | action | depends on | reversible", then an "Unresolved" block.
- **Risk**: Low.

### Change 14: Part 6.1 #409 body corrections (from V5 "Corrections to the #409 body (exact wording)", with the debate's changes)
- **Source**: `variant-5-original.md` lines 176 to 206 (23 rows, BC-01 to BC-23); R2-V5 section 1 row 9 (BC-17 replacement) and row 13; R2-V1 section 3 A-011; V1 C-07, C-25, C-34, W-7; V2 W-05(a), W-06; V4 edit 1.
- **Target**: Part 6.1 (insert; the exact BC wording is referenced, not retyped, except where the debate changed it).
- **Rationale**: A-011 (92): one editor, one ordered edit set, citations pinned to sha or `updatedAt`.
- **Integration point**: Part 6 specification lists per-row disposition.
- **Risk**: Medium. The #409 body moved during the debate (30,030 to 30,756 to 30,758 bytes; `updatedAt` 2026-11-13T16:57:51Z at probe) and line numbers go stale.

### Change 15: Part 6.2 proposed edits to #450 (from V2 "Proposed edits to #450" 1 to 5, R2-V2 sections 1, 5.1, 5.4, 5.6)
- **Source**: as listed.
- **Target**: Part 6.2 (insert).
- **Rationale**: X-001 (91), W-03, W-04, W-09, W-12; R2-V2 row 1 rewords edit 5.
- **Integration point**: per-edit disposition and which edits are paste-ready.
- **Risk**: Low to Medium. Edit 1 depends on an owner answer.

### Change 16: Part 6.3 Coder#477 rewrites (from R2-V3 5.6 A, B, C)
- **Source**: R2-V3 lines 126 to 172.
- **Target**: Part 6.3 (insert; reference by section, do not retype).
- **Rationale**: keep-as-written is the least defensible (its premise contradicts the built watcher); narrow about 65 percent.
- **Integration point**: recommendation and the placeholders still open in the text.
- **Risk**: Medium. Text A contains `[N minutes: owner decides]` and an UNVERIFIED route (D-7), so it is not fully paste-ready.

### Change 17: Part 6.4 #423 rewrite and #339 comment (from R2-V4 5.7)
- **Source**: R2-V4 lines 134 to 209.
- **Target**: Part 6.4 (insert; reference).
- **Rationale**: R2-V4 5.7 carries four corrections to R1-V4's text. The #339 body is not edited (comment form is reversible).
- **Integration point**: note the two clauses that depend on other answers (see Part 6).
- **Risk**: Low to Medium.

### Change 18: Part 7 deduplicated owner questions (from V5 questions 1 to 10, V2 Q1 to Q4, R2 D-lists of V1 to V5, INV-003, 004, 014, 023, 030)
- **Source**: as listed.
- **Target**: Part 7 (insert; replaces V5 "Questions only the owner can answer").
- **Rationale**: S-007 (the reports ask duplicate questions); the owner should answer each once.
- **Integration point**: 24 questions, each with a recommended answer and the points it gates.
- **Risk**: Low.

### Change 19: Part 8 changes not being made (from R2 concessions, X-004, X-013, X-017, A-012, X-005)
- **Source**: R2-V1 to R2-V5 section 1; matrix; INV-008 for the rejected Codex remedy.
- **Target**: Part 8 (insert).
- **Rationale**: record each rejected proposal with its debate evidence so it is not reopened.
- **Integration point**: table mirrors this plan's "Changes NOT Being Made" section.
- **Risk**: Low.

### Change 20: Carry the status and unresolved items into the merged output header and return contract (from debate-transcript "Convergence Assessment", invariant-probe summary)
- **Source**: `debate-transcript.md` lines 1843 to 1849; invariant-probe "Summary".
- **Target**: merged output header block and the return contract.
- **Rationale**: BLOCKED_BY_INVARIANTS is carried, not waived. Unresolved by evidence: A-009 (Orca build version divergence), INV-008 (no fix specified, owner ruling pending), X-016 (consumption on a live coordinator Run unproven both ways).
- **Integration point**: header fields `status`, `convergence`, `unresolved`.
- **Risk**: Low.

### Change 21: Provenance tags and citation pins (Section 6 of the artifact templates, A-010, A-011, INV-030)
- **Source**: `artifact-templates.md` Section 6; matrix for ids.
- **Target**: every block in the merged output.
- **Rationale**: base content tagged `<!-- Source: Base (original) -->`, modified base content tagged with the reason, incorporated content tagged with variant, section and change number. Every GitHub citation is pinned to a head sha or the body `updatedAt` at the time it was read.
- **Integration point**: the point register carries one "Source" id per row.
- **Risk**: Low.

### Change 22: Plain-English and gloss pass over the base (repairs V5 L4 NOT MET)
- **Source**: re-evaluation standards table (L4: V5 NOT MET, "TUIBBS, QUESTION-OBSERVATION never defined").
- **Target**: whole merged output (edit pass).
- **Rationale**: the merged output is meant for the owner and a brainstorm; undefined coined names make it unreadable to anyone outside the sessions that produced them.
- **Integration point**: a glossary block after the header (TUIBBS = the owner's separate SSH-host TUI platform that the observer snapshot is shaped for; QUESTION-OBSERVATION = the observer's gate for reading coordinator questions; WC-16 = the worker-contract rule that caps a coordinator's sweep at once per 5 minutes; NFR-001 = the sweep rule "exactly one report file"; NFR-014 = the owner-signed allow-list of Orca commands the sweep may run; FU-1 = the watcher's first live test; AC-S = the owner's dated direction-selection record; Q-1 = the observer gate test that failed on 2026-11-11 (an unbound terminal cannot read another terminal's Run); OB-H gates = the claim's ship gate in `claim.md:131`).
- **Risk**: Low. Each gloss must come from the cited source; where a source does not define a term, the merged output writes "UNVERIFIED meaning".

## Final Structure of the Merged Output

The merged output has this structure, in this order. Titles are fixed so the lead and a downstream `/sc:brainstorm` can link to them.

| Part | Title | Built from | Change # |
|------|-------|-----------|----------|
| 0 | Header: status, convergence, unresolved items, glossary, how to read the point records | debate-transcript Convergence Assessment; plan Overview | 20, 22 |
| 1 | Verdict and the facts the debate established; findings the debate withdrew or disproved | V5 Verdict, S1 to S10; all R2 section 1 | 2, 3 |
| 2 | Adjudicated points by issue or system, in this order: 2.1 observer (`superclaude observe`) and #409; 2.2 sweep, Orchestrator mode (#339) and PR #539; 2.3 the integration contract; 2.4 issue watcher (#331, #450); 2.5 Coder#477; 2.6 Orchestrator v2 (#423) and the trust design; 2.7 the "TUI panel" question | V5 base plus V1 to V4 as specified | 4 to 10 |
| 3 | Point register: every point with id, verdict, confidence, evidence, owner decision with recommended answer, course of action, dependencies, reversibility | matrix; R2 section 3 tables | 11 |
| 4 | Dependency graph (text) and merge or implementation order | R2-V5 5.9; R2-V4 A-011; probe corrections | 12 |
| 5 | Invariant probe: HIGH and MEDIUM UNADDRESSED findings with the action for each; the unresolved items | invariant-probe.md | 13 |
| 6 | Corrections to the #409 body and proposed edits to #450, Coder#477, #423 and #339, with which are paste-ready | V5 "Corrections"; R2-V2, R2-V3, R2-V4 | 14 to 17 |
| 7 | Deduplicated owner questions, each with a recommended answer | all variants | 18 |
| 8 | Changes NOT being made | R2 concessions | 19 |
| A | Appendix A: sources read and not read; pointers into `variant-5-original.md` | V5 Scope read | 1 |

Every point record in Part 3 and every action in Part 2 uses these eight fields, in this order, so the owner can scan any point the same way: **id, verdict, confidence, evidence, decision needed from the owner (with the recommended answer), course of action, dependencies (what must happen first, what it unblocks), reversibility**.

## Part 1 Content Specification: Verdict, Established Facts, Withdrawn Findings

### 1.1 Verdict (draft wording for the merged output; adjust only to keep ids and numbers true)

> The five reviews (of #409, #450, Coder#477, #423, and the built observer) agree on one conclusion once Round 2 is applied: Orchestrator mode (the `superclaude sweep` command on PR #539) and the TUI panel (the `superclaude observe` command, merged in PR #503 and PR #514) already exist as two separate programs, were built independently from the same design package, mention each other nowhere, and point in the same direction. They are aligned in intent and not yet in practice: two readers of the same Orca command, two JSON files that both call themselves "v1", three vocabularies, two lists of allowed Orca commands that disagree on one command (`check`), and no written contract between them. Recommended course: keep both programs; write one short contract note; settle the open security question on PR #539 first; correct the four issue bodies in one ordered edit pass; do not build a reader of the sweep's JSON inside the observer; answer the 24 owner questions in Part 7, starting with Q1 to Q4.
>
> Status: BLOCKED_BY_INVARIANTS. All 36 diff points reached one winner or an agreed "unresolved" (convergence 100 percent on points, 63.9 percent before Round 2). One HIGH invariant is not addressed: INV-008, the git-config hole in the sweep's `git status` calls. It is the first action in Part 2.2 and in Part 4 and is not waived.

Also state: nothing was run against live Orca by the debate except read-only list, help and version calls recorded in the invariant probe; every "verified now" claim names its source.

### 1.2 Facts the debate established (each row: fact, evidence, confidence from the matrix where one exists)

| # | Fact | Evidence | Confidence |
|---|------|----------|------------|
| E-01 | The observer is built and merged: release 1 in PR #503 (2026-11-11T19:54:57Z, `9e2608b03`) and release 2 in PR #514 (2026-11-12T12:36:19Z, `cd8736199`); registered in the shipped CLI | `src/superclaude/cli/main.py:572-574`; `gh pr view` (SC-13) | 98% (X-012) |
| E-02 | The observer's coordinator-questions read is OFF on master: `QUESTION_GATE_PASSED = False` (`observe/commands.py:63-67`). The switch-on exists only as two unpushed local commits (`1ae72e1a1`, `f104ca51a`) in sibling worktree `issue-409-mvp`; remote branch `409-Phase2` is gone; `origin/master` is not an ancestor of the sibling HEAD, so a fresh branch is needed | R2-V5 section 1 rows 5, 11; `git merge-base --is-ancestor` exit 1; INV-001 | verified in R1 and by the probe |
| E-03 | The observer reads Orca only and reads no sweep file; the sweep, its design, command, skill and WORKER-CONTRACT contain no reference to the observer, `cli/observe`, #503 or #514. The two programs never mention each other | X-013 (SC-15, SC-16) | 95% |
| E-04 | Two readers of `worker-list`: observer all Runs, 15 s per process, up to 5 calls of 100 rows, 8 MiB and 10 s per call; sweep one Run per wake, WC-16 cap at most once per 5 minutes, up to 50 `worker-show`, 90 s budget. No shared limit; several observers multiply the load | `adapter.py:29,57`; `collector.py:28-34`; `probes.py:112-118`; X-015 | 87% |
| E-05 | Two JSON files both called "v1": "observe snapshot v1" (`schemaVersion`, camelCase, `"UNKNOWN"` strings, rows keyed `dispatchId`, additionalProperties false, rewritten every live cycle in the user state directory) and "sweep report JSON v1" (`schema_version`, snake_case, `null`, rows keyed `row_id` = `orca:<dispatch>`, printed to stdout only) | A-014; O-08 | 94% |
| E-06 | Three vocabularies (observer, sweep, Orca). The built observer shows none of the ten dimension names; it prints Orca's words and marks report status, acceptance, tests, approval, settled and policy-frozen `unavailable (no source)` | X-008; `view.py:96,412` | 91% |
| E-07 | `superclaude sweep run` always writes a dated report before it prints JSON; the JSON goes to stdout only; the rule "a sweep adds exactly one report file" (NFR-001) is pinned by the design (`docs/designs/orchestrator-mode.md:128`) and two tests (`tests/sweep/test_readonly.py:300`, `tests/sweep/test_cli_contract.py:1474`) | X-004; R2-V5 row 7 | 91% |
| E-08 | PR #539: open, head `873599d59`, six review threads, four resolved, two unresolved (`probes.py:1052` Augment, filtered count under-reads a page; `probes.py:1211` Codex security thread). CI fails on one test (`test_every_worktree_gets_an_agent_and_its_creator_owns_it`), the same test that fails on master. PR #541 re-pins that test, changes one file (`tests/core/test_claude_md_worktree_rule.py`), is OPEN and CLEAN; #539's 1003 files do not include it | INV-022, INV-036, INV-038; A-004 | 88% |
| E-09 | The sweep's reads are not fully confined: `git status` runs in every path `worktree ps` lists with the inherited environment; a shared repo config reaches every linked worktree | `probes.py:305-327,1203-1214`; X-007; INV-008 measurement | 89% |
| E-10 | The watcher prompt `/sc:issue --claim <N>` has no `--pipeline`, so the claim runs at its default `worktree` level: it creates or reuses worktree `issue-<N>` and starts a governed second agent. The watcher design says the claim stops at `next-steps.md` | `issue.md:43,88`; `launch.py:33`; `issue-watcher.md:44`; X-001 | 91% |
| E-11 | On this host launched Claude sessions run with permission checks off: `CCSESSION_PERMISSIONS` is unset and `ps` shows `--dangerously-skip-permissions --allowedTools=Grep`; a non-empty `CC_CLAUDE_FLAGS` replaces the flags whatever `CCSESSION_PERMISSIONS` says | `ccsession:134-141`; INV-011 (probe, `ps`) | verified here only |
| E-12 | Coder#477's premise (a watcher that sends prompts to a listener) contradicts the built watcher (design decision D1 option A: no listener, inbound port or address registry) | `issue-watcher.md:28,43,47-49`; R2-V3 5.1 | per V3 and V2 |
| E-13 | "v1" and "v2" mean different things in the #339 issue summary, in the Phase 1 research report (phases 1 to 6) and in #423; at least five numbering namespaces are in play (adds observer R1 to R4 and "release 2", and the watcher's FU-1 to FU-6) | R2-V4 5.1; INV-021 | 100% for the three; INV-021 for five |
| E-14 | On this host the observer is already past its read cap: an unscoped `worker-list` reports `page.total` 513 while the observer stops after 5 calls of 100; only the 13 oldest rows are hidden (order newest-first is an observation, not documented) | `adapter.py:57`; INV-017 | probe, live read |
| E-15 | Two builds of one Orca release are on record: design lock `1.4.245-aidev02.780594c521aa` and host `1.4.245-aidev02.9cfecdd30b2a`; the sweep compares only the text before the first hyphen, so it cannot tell them apart; the observer records no Orca version | `report.py:160`, `:23`; INV-020 | A-009 unresolved |
| E-16 | Most owner decision records the observer relies on are not on master: only `owner-decisions-20261111.md` is; the 2026-11-08 and 2026-11-12 records, the pass record, `live-test-guide.md` and `tuibbs-review/` are untracked or in unpushed commits in the sibling worktree | `git ls-tree origin/master .dev/issues/409/`; INV-002 | 83% (A-015) |
| E-17 | `observe --once` already prints a plain-text record with no file write unless `--snapshot` is passed; the #339 "static report in chat" ask does not need a new program | `commands.py:215-237`; O-16 | verified in R1 |
| E-18 | Orca's own `orchestration check --help` on this build says `--all` "does not mark read" and that `--peek` and `--all` "do not drain a mailbox on their own"; no debate file cited it; the owner's measurement on the coordinator's own Run is non-diagnostic (0 pending is expected either way) | INV-041(a); R2-V1 section 5 item 2; `release-gates.md` | X-016 stays "unproven both ways" (61%) |

Facts the debate could not establish (carry as UNVERIFIED): whether `agent launch` creates any Run or Dispatch record (D-A); the real launch-reply shape (`OPERATION_ID_PATHS`, `launch.py:39-45`); whether a human can use the observer's questions panel in a terminal that already holds a Claude coordinator session (INV-024); who wrote the pass record (authorship); whether Orca prunes worker rows; `projection.attention` values for live and blocked workers; non-owner non-consumption of `check --all`; real message rate; whether an owner API token can drive the owner-shared Orca app (D-7); the second host's Orca shape.

### 1.3 Findings the debate withdrew or disproved (so nobody re-raises them)

| Finding | From | Why it fell | What stands instead |
|---------|------|-------------|---------------------|
| "No observer code exists; 20 designs await a human choice" (C-03, C-02 second half, #409 body L16) | V1 | PR #503 and #514 are merged (X-012, 98%) | observer built; selection record (AC-S) missing |
| C-21, C-26, A-01 "aligned", A-05 to A-07 as gaps, F-01 "(1) the observer reads the sweep JSON", F-03's observer option, F-04 as an observer gap, F-12, F-14, F-15 as observer gaps, W-3, Q1 | V1 | all rest on the false premise; withdrawn in R2-V1 section 1 "Net" | sweep-side F-02, F-05, F-07, F-08 to F-11, F-13, F-17, F-18, C-07, C-25, C-34 stand |
| "Persist `<stem>.json` beside the report" as the recommended answer (F-03, Q1) | V1, and V5 R1 concession 4 "persist now, it is cheap" | breaks NFR-001 and two pinned tests; needs an owner requirement change in a contested PR (R2-V5 row 7) | persistence is Phase 2, owner choice; or caller-side stdout capture |
| C-08 "#539 needs a rebase after #541" | V1 | no file overlap (INV-036) | a new merge ref is needed, not a rebase (INV-037) |
| Verdict "share the same dimension names" and its tally | V1 | contradicts V1's own C-02 and F-02 (X-008); tally miscount (X-009) | F-02 table plus three vocabularies |
| W-10 "observer reader" as written; "absent by construction" for the Run record (W-04); cites by `/tmp` line numbers | V2 | the built observer has no watcher input; the Run claim is an inference | "no watcher panel in `observe` before FU-1"; W-04 as UNVERIFIED |
| W-05 "will be mislabelled person-started" as a firm claim | V2 | depends on `session_join`, which V2 did not run; `prompt` is empty or not a slash command on all 27 live agent rows | labelling by prompt UNVERIFIED until FU-1 (D-B) |
| Edit 5 "the reply is produced without any write" (a status route from `sweep run`) | V3 | `sweep run` always writes a dated report (X-004); a sidecar breaks `test_readonly.py:400` | first status record = the observer snapshot (R2-V3 D-3) |
| Edit 8 restated launch ("a new top-level session") without the second governed agent; the twelve-edit shape; all `/tmp` line cites | V3 | X-001 | state the claim level explicitly |
| Edit 3 "both read the same sweep facts"; C8 "boundary sentence TRUE" (circular); F17 "confines every path"; F16 cadence count; F18 "Collision Lens" as an existing detector; F19; #423 edits 4 and 7; #339 edit 4 and #409 edit 2 narrowed | V4 | circular proofs; the sweep confines file reads only (X-007); Collision Lens is an unbuilt synthetic design | boundary relabelled "proposed" (X-002); the per-class acceptance criteria stand in narrowed form |
| O-05 "the sweep's 'cannot read without consuming' is stronger than the evidence" and its proposed rewording | V5 | the owner's measurement was on the coordinator's own Run and is non-diagnostic; only a synthetic probe Run is diagnostic | X-016 unproven both ways; replacement wording in Part 2.2 |
| BC-17 "(the sweep's output or the observer's snapshot) as a v2 input", as worded; RT-F16 | V5 | the snapshot's 15 required row keys contain no command, objective, branch, changed paths or issue or PR | R2-V5 row 9 replacement text |
| D5 option (ii) "any Run the terminal holds" as a recommendation | V5 | scope is not the risk (Orca fences, `consumer_fenced`); consumption on a live coordinator Run is | seeded consumption test first; owner writes scope in own sentence |
| "All four earlier reviews were wrong about one fact" (X-019) and "drop W-3 from the #409 body" (X-020) | V5 | overgeneralisation; W-3 is V1's proposed wording, not body text | cite exactly; read as "do not add V1's W-3" |
| F-04 headline "CLOSED" | V5 | holds for the Orca ledger on one host only | say "closed for the Orca ledger on one host; open for per-Run depth and for multi-host" |
| "#539 needs only a CI re-run after #541 merges" | R2-V1 A-004, R2-V2 A-004 | a re-run keeps the same merge commit and fails on the same test (INV-037) | push, update-branch, or close and reopen |
| "Filtering to the selected repository and disabling executable Git config closes the Codex thread" | the thread's suggested remedy | a repo filter leaves a shared `.git/config` exposed and one flag stops only `core.fsmonitor`, not `filter.*.clean` (INV-008) | Part 2.2 S0 |
| "The observer's 5-call cap covers a host's worker ledger" (X-014 "closed" read broadly) | R2-V5 X-014 | this host has 513 rows (INV-017) | PARTIAL is the steady state here |
| "A seeded test on a throwaway Run proves `check --all --types question` does not consume" (as sufficient) | R2-V5 D-1, R2-V1 D-2, R2-V3 D-4 | one build, a Run with no `--wait` listeners, Q-1 FAIL means a pass says nothing about usability (INV-041) | the test is necessary, not sufficient; Part 2.1 checklist |

## Part 2 Content Specification: Adjudicated Points by System

Each system section has: points covered (ids), adjudicated verdict (draft wording), numbered actions in order, "do not", and the open owner questions (Part 7 ids). Part 3 holds the per-point record; Part 2 holds the narrative the owner reads.

### 2.1 Observer (`superclaude observe`) and issue #409

- **Points**: X-012, X-013, X-018, X-011, X-014, X-015, X-016, X-002, A-003, A-010, A-013, A-015, A-016; probe INV-001 to INV-005, INV-014, INV-017, INV-018, INV-023, INV-024, INV-041, INV-044.
- **Verdict (draft)**: the observer is built (E-01), reads Orca only (E-03), implements only Signal Bridge's worker ledger and the Attention Ledger's question panel (V5 section 6: Fleet Quilt, Loop Detector, Mission Pulse and the reviewer's four asks are unbuilt; Decision Desk is release 3, gated). Its questions read is dark on master (E-02). The #409 body is wrong in 23 places (Part 6.1), headed by "No observer code exists" (L16) and "Preferred direction is Bubble Tea" (L54, L124, which the owner replaced with Python + Rich on 2026-11-08). The direction was chosen in staged form (2026-11-08, 2026-11-11); the dated selection record (AC-S) does not exist (X-018, 74%).
- **Actions, in order**:
  1. One editor posts the #409 correction pass (Part 6.1), after the owner answers Q8 and, for decision 6, Q16. Pin to `updatedAt` and re-read it immediately before the write (INV-030).
  2. The owner writes the AC-S record, or amends #409's first acceptance criterion (Q8). Agents cite it; they do not write it (`release-gates.md:22`).
  3. The owner commits or archives the evidence that exists only in the sibling worktree: `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/` (INV-002), before that worktree is cleaned. The guard-flip PR itself must commit the owner's pass record (INV-001).
  4. Guard-flip PR (the switch-on of the questions read). Prerequisites, all of them: (a) the owner's scope sentence, "this Run only" or "any Run my terminal holds" (Q6; INV-003: the record names one Run, `run_93bfa00cae2b`, an old "Claim issue 375" Run; the guard is one boolean and `check_run_id` checks syntax only, so after the flip any `--run <id>` reads); no scope answer means the guard stays off; (b) the seeded consumption test, run by the owner or the 409 session from a plain terminal that holds no Run: `run-create` only, never `run-use`, record `run-current` before and after, put known `question`, `worker_done` and heartbeat messages in the mailbox, run the observer's exact template twice, then one consuming `check`, and confirm every seeded message is still returned (INV-005, INV-041 (c); safe precedent: the Task 17 sample `run_86013b917868`); cite Orca's own help text for `--all` first (INV-041 (a)); record the Orca build string in the gate record and add a build check or a test that fails when the build changes (INV-041 (b)); (c) one recorded live attempt of the panel in the real coordinator layout, because Q-1 FAIL means a passing test says nothing about usability and 28 of 53 Runs have no holder terminal (INV-024); (d) the owner-written pass record committed on master, because the constant cites a path that exists only in the sibling (INV-001; authorship rule INV-014: the owner supplies it); (e) the mapping-table row for `reclaimable` (INV-023); (f) grep `.dev/issues/409/` for "not passed" and fix each hit in the same change, including `release-gates.md` (INV-044). Open from a fresh branch off `origin/master` after #541, with `/sc:pr-submit --monitor 3` (project rule: never a bare `gh pr create`).
  5. Routing row for `superclaude observe` (Part 4 step 6; INV-029).
  6. Contract note (Part 2.3).
- **Do not**: add a watcher panel to `observe` before FU-1 (V2 W-10 reworded); add an observer reader of the sweep's JSON (X-013, X-017); flip the guard before steps 4 (a) and (b); treat the owner's "0 pending after reads" on the coordinator's own Run as proof of non-consumption (X-016).
- **Cap facts to state** (INV-017, INV-018): on this host the observer is partial in steady state (513 rows against 500); "at most 5 calls per read" is for `worker-list`; with `--questions` on a cycle can make 6.
- **Owner questions**: Q6, Q7, Q8, Q16, Q17, Q19, Q22, Q23.

### 2.2 Sweep, Orchestrator mode (#339) and PR #539

- **Points**: A-004, A-006, X-004, X-007, X-010, A-005, plus the surviving V1 findings C-07, C-25, F-02, F-05, F-07, F-08 to F-11, F-13, F-17, F-18; probe INV-008, INV-009, INV-010, INV-015, INV-019, INV-022, INV-033, INV-036, INV-037, INV-038, INV-039, INV-040.
- **Verdict (draft)**: PR #539 (Phase 1, the read-only sweep) is open, mergeable and not ready: two unresolved threads, one of them a security thread whose suggested remedy does not work (INV-008). #541 clears the only red test and does not touch #539's files.
- **Actions, in order**:
  1. **INV-008 first, blocking.** Facts (probe experiment, temp repo, git 2.47.3, the sweep's exact argv `git --no-optional-locks -C <wt> status --porcelain=v1 -z --branch --untracked-files=all`, `GIT_OPTIONAL_LOCKS=0`): with `core.fsmonitor=<hook>` and `filter.probe.clean=<cmd>` (`* filter=probe` in `.gitattributes`) set once in the shared repo config and one linked worktree, both the fsmonitor hook and the clean filter ran; with `-c core.fsmonitor=false` the hook did not run and the clean filter still did. So a filter to the selected repository does not protect the at least 18 of 29 listed worktrees that share one `.git/config`, and the thread's remedy is not one flag. Code: `probes.py:305-327`, `:1203-1214`, `:1255`. The owner chooses (Q1): (F1) a fix that neutralises both keys; or (F2) refusing a worktree that defines them, reported as an `unscanned` source row so no JSON key is added; or (F3) accepting the finding. F1 and F2 are an allow-list and test change, not a one-liner: `ALLOWED_GIT` is an exact one-entry list (`probes.py:64-67`) under the owner-signed allow-list (NFR-014), and `tests/sweep/test_probes_allowlist.py:503`, `tests/sweep/test_readonly.py:85,156,453` pin the argv prefix (INV-009). Filtering `paths` to one repo also changes the contract allow-list and transcript scans, which share the same `paths` (`probes.py:1255-1263`, `:1301`) and turns a contract in another repo's worktree into "outside root", the failure Codex thread 623cm5 describes; so the git-status scope must be separated from the contract allow-list, and the golden tests that change must be named (INV-039). Keep the probe experiment as the regression test. F3: the four statements that say read-only or "changes nothing else" must then carry a caveat in the same PR: `HOW-WE-WORK.md:335` and `:406`, `sc-sweep-protocol/SKILL.md:3` and `:15` (INV-010); the ruling must say which premise it relies on (`SECURITY.md:L166-L170`; counterweight: every session on this image runs permission-free, INV-011, so the "lower-privileged agent" premise may not hold here). Recommended answer: F1 or F2 (about 70 percent; PLAN INFERENCE from the probe's stated action, not a debate verdict). The design of the fix belongs to the #539 author and the owner; the merged output states the requirement, not the code.
  2. Resolve the Augment thread (`probes.py:1052`, filtered count under-reads a page) with no new JSON key: Orca replies already carry `page.hasMore`, `page.total` and `page.limit`, and `probes.py:1046-1056` already ORs `hasMore` with `len(filtered) >= 100` (INV-040).
  3. Merge #541 first (one file, CLEAN, six checks pass). It makes master green for one commit; any later edit of the CLAUDE.md bullet it pins fails the test again (INV-033). That is not a reason to hold #541.
  4. Refresh #539's merge commit with a push (step 1 or 2 is one), an update-branch merge, or a close and reopen. A CI re-run alone keeps the old merge ref (`8c689986 = Merge 873599d59 into d2d8a2d16`) and fails on the same test (INV-037; GitHub docs: a re-run keeps the original `GITHUB_SHA` and `GITHUB_REF`).
  5. Add no JSON keys and no files inside #539: key additions change pinned golden sets (`ROW_KEYS`, `test_report.py:1255`; design `:599`), a sidecar file breaks NFR-001. Log wording and key items in #534 (A-004).
  6. Sweep wording to fix after #539 merges, logged in #534 now: design 7.5 ("copied from #409 ... because #409 is unmerged": false since `9e2608b03`), design section 17 item 5 and line 559 (cursor field "open"; the capture already recorded `nextCursor` and `hasMore`), and `report.py:199,534`. Replacement text for the two lines (R2-V5 5.8): "This command reads no messages. A plain `check` consumes them. Whether `check --all --types question` consumes on a live Run is not established." This replaces V5's withdrawn O-05 rewording.
  7. #339 itself: no body edit; one comment (Part 6.4). Phase 1 follow-ups get one table in #534: item, owner, trigger (A-005).
  8. Smaller items the probe adds: a pinned test that no other worker-written field reaches the report (INV-015; today only `blocked_question` prints, through `cell()`, `report.py:258`); state "first 50 in Orca list order" for the `worker-show` cap (INV-019, `probes.py:115,1114,1171`); the sweep's version check compares only the text before the first hyphen (INV-020).
- **Do not**: edit #539 for wording or alignment; add keys or a sidecar; claim "read-only" without saying "toward Orca" until INV-008 is ruled (A-006, 90%).
- **Owner questions**: Q1, Q9, Q10, Q11.

### 2.3 The integration contract between the sweep and the observer

- **Points**: X-006, X-008, X-009, A-001, A-002, A-009, A-012, A-014; probe INV-006, INV-013, INV-017 to INV-020, INV-023, INV-028, INV-031, INV-035, INV-042.
- **Verdict (draft)**: one short written note, no runtime link in version 1: neither program reads the other, neither gains a file or key (R2-V5 5.1).
- **Content (from R2-V5 5.2 to 5.8, with the probe's additions in italics)**:
  - File `docs/designs/observe-sweep-contract.md`, tracked and shipped (not under `.dev/`). Owner: the Orchestrator mode design (#339), because the sweep JSON is the stricter contract (golden-tested key set). The observer spec (`.dev/issues/409/bmad/spec-orca-observer/release-gates.md`, `adapter-contract.md`) and `docs/designs/orchestrator-mode.md` section 1 link to it and do not restate its tables. *Which branch carries the draft: this checkout `ironbelly/issue-339-orchestrator-mode` IS PR #539's head, so a note committed here joins the PR; draft on a master-based branch (INV-031); links into `orchestrator-mode.md` wait for #539 to merge.*
  - Amendment rule: a change to a shared word, the join key, either schema version, or an Orca verb either program may call edits the note in the same PR. *The rule needs a test: one test that compares the note's Orca verb lists, schema versions, join key and shared words with `ALLOWED_ORCA`, the observer templates, `SCHEMA_VERSION` and the report constants; today no test reads any design document (INV-042).*
  - Registry of contracts so nobody says "the JSON v1" again: observe snapshot v1, sweep report JSON v1, the watcher's `status --json` (no `schema_version`) and `dispatch.json` v1, and any future v2 or #477 status record. The note governs only the first two.
  - Units (R2-V5 5.3): observer = all Runs on one host, up to 5 calls x 100 rows per 15 s cycle, PARTIAL beyond; *PARTIAL is the steady state on this host (513 rows) and newest-first order is an observation, not a contract (INV-017); with `--questions` a cycle can make 6 calls (INV-018)*; sweep = rows for the bound Run, `worktrees[]` and transcript scans host-global; `worker-show` for at most 50 *in Orca list order* (INV-019); Run-less sessions (watcher-launched, person-started) not observable by either program today. Write also "single owner, single OS user, single host" once (A-007).
  - What each publishes for the other: nothing new in version 1. Rules for what exists: the snapshot is last-writer-wins and stays on disk after the process exits (no pid, no liveness flag; `export.py:26`), so a reader applies its own age rule to `generatedAt` and shows an old file as stale (*the age threshold is the owner's number, Q22; INV-004*); the sweep's JSON is stdout-only, so a caller that wants it captures stdout and nobody re-runs the sweep; all strings from either program are untrusted input to a reader (two sanitizers: `sanitize.py` and `report.py:563-598`). *The two programs resolve `XDG_STATE_HOME` differently: the observer accepts it only when absolute (`export.py:241-242`), the sweep uses any non-empty value (`probes.py:1264-1266`); list both paths (INV-006).*
  - Versioning (R2-V5 5.5): always "observe snapshot v1" and "sweep report JSON v1"; adding an optional key stays v1 with a deliberate test change in the owner program's PR; rename, remove or change meaning is v2; consumers ignore unknown keys and never validate against a frozen copy of the producer's schema (INV-035: closes the cross-program case). Join key: `dispatchId` (observer) equals the part of `row_id` after `orca:` (sweep); structural basis verified (`probes.py:435`, `classify.py:891`) but not compared on real ids (D-3), so the note calls it a join key only after one comparison; *join on `runId` plus `dispatchId` and exclude empty or duplicate-flagged rows (sweep `NOTE_DUPLICATE_DISPATCH`, `classify.py:893-896`; only ids matching `ctx_[0-9a-f]{12}` reach `worker-show`; INV-028)*.
  - Mapping table of shared words (R2-V5 5.6): stale, unknown, unavailable, could not determine, historical, frozen, settled, "coordinator question" versus "waiting on a person". *Add a `reclaimable` row: the observer's `HISTORICAL_STATES` is released and retained only (`view.py:35`) while Orca counts reclaimable separately (live first page: reclaimable 27, released 41, retained 32, active 0), so reclaimable rows stay in the observer's default view and the sweep derives "settled" from `outcome` (`classify.py:98,114,781-786`); the note decides which side of "historical" it is (Q23; INV-023).*
  - Verb lists per caller: observer 3 argv shapes (one `check --all --types question --run <id> --json` template behind the guard), sweep 10 exact templates over 7 verbs (owner-signed, NFR-014; `check` forbidden), watcher `skills list --json` plus `agent launch` (a write verb that starts an agent; so "read-only" is per caller, not per program pair; R2-V2 section 2). *The observer is for a person or a coordinator only: WORKER-CONTRACT.md:23 lists slash commands, and `observe` is a plain CLI whose unscoped `worker-list` is not fenced; one line "person only" in the routing row and the note (INV-013).* Binary resolution: observer and watcher use `_find_orca`; the sweep uses `$ORCA_CLI_COMMAND` else `orca-ide`; no host with both names was shown, so a note, not a risk row (INV-016).
  - `projection.attention{categories, requiresAction}`: neither program reads it (verified now: only in observer fixtures). After the shared live capture (D-8), the observer may show it verbatim; the sweep does not read it in Phase 1; neither classifies from it until its values for live and blocked workers are recorded (R2-V5 5.8).
  - *Record the Orca build string next to each capture; the sweep's check cannot tell two builds apart (INV-020; A-009 unresolved).*
- **Do not**: add keys or a file to either program for the note's sake; name anything a "join key" before D-3; call either JSON "the JSON v1".
- **Owner questions**: Q5, Q9, Q17, Q22, Q23, Q24.

### 2.4 Issue watcher (#331, rollout #450)

- **Points**: X-001, X-003, A-008, A-009 (watcher fixtures), plus V2 W-01 to W-16; probe INV-007, INV-011, INV-012, INV-016, INV-034.
- **Verdict (draft)**: partly aligned, and FU-1 (the first live test) is not ready to run as written. Two contradictions: the fixed prompt triggers the claim's default `worktree` pipeline against the design's "claim stops at `next-steps.md`" (W-01, W-02); #409 and Coder#477 picture a coordinator that the watcher design does not use (W-06). A watcher session is Run-less, unowned and unrecorded: the watcher keeps only an Orca operation id (W-03, W-04, W-05). Aligned and safe as built: plain-process launch, WC-13, never-as-worker, claim-marker detection, read-only `status` (W-13 to W-15).
- **Actions, in order**:
  1. Owner decides the claim level (Q2). Recommended `--pipeline none` (claim ends after the comments, no worktree, no second agent: exactly design decision D2). Code touched: `launch.PROMPT_PATTERN` (`launch.py:33`), `build_claim_prompt` (`:84-92`), the 12-element argv pin, `retry_argv`, the NFR-001 property test, runbook strings: one small PR, no overlap with #539. If the owner keeps the default: record it as a deliberate chain and require OB-H1 item 1, OB-H2, OB-H3 (#394) as a precondition (W-02).
  2. **FU-1 preconditions (explicit, from INV-012 and INV-011, which the one-paragraph consensus lacked)**: (a) the claim level recorded; (b) the owner accepts in writing the permission mode of the first session: `--pipeline none` removes only the second agent; the first session still assigns the issue, posts comments and runs the accuracy check over untrusted issue text, and on this host runs with permission checks off; (c) FU-1 records `CCSESSION_PERMISSIONS`, `CC_CLAUDE_FLAGS` and the real argv of the launched session (`ccsession:134-141`: a non-empty `CC_CLAUDE_FLAGS` replaces the flags); (d) before and after `run-list` and `worker-list` around one real `agent launch` (D-A); (e) one `worktree ps --json` agent row after the launch: does `prompt` hold `/sc:issue --claim N`, does `paneKey` equal a tab-map name (D-B); (f) the real launch-reply operation-id path (`OPERATION_ID_PATHS`, `launch.py:39-45`, a guess pinned by four `_assumed_shape` fixtures; a wrong path makes every correct launch `unknown`); (g) Orca build string (A-009); (h) the ccsession tab-map entry and whether the session stalls at the Session Name prompt (W-09); (i) the list of writes the test makes (assignment, two marked comments, ClickUp script if its env is set, `.dev/issues/<N>/` files) and closing or unlabelling the test issue, because the order "claim first, then label" can make the enabled watcher claim it again (R2-V2 5.6).
  3. Runbook: add step 1.3a (create the watcher worktree with `orca worktree create --name issue-watch --agent claude --prompt "<task>"` as a person and name who owns its agent; W-07); add that `reset --forfeit-guarantee` on an `unknown` entry first requires checking Orca for a live session in the configured worktree (R2-V2 5.4; INV-007 handled).
  4. Machine-started sessions get a #534 row after FU-1 (W-05, A-005); the sweep may label them only after D-B (Q21).
  5. Do not add a watcher panel to `observe`, and do not route watcher prompts through a listener, until FU-1 is recorded (W-10 reworded).
- **Owner questions**: Q2, Q3, Q20, Q21.

### 2.5 Coder#477 (workspace listener)

- **Points**: X-001 family, X-004 (V3 Edit 5), X-005, A-002 (workspace unit), A-007; V3 F1, F2, F6, F8, F10 to F14, F17; probe INV-043.
- **Verdict (draft)**: do not build a listener for the watcher (E-12). Recommended: narrow #477 to read-only workspace status and identity with no prompt routing, about 65 percent, after the owner answers Q3 and Q4; close it (with the reopen conditions in R2-V3 5.6 C) if the observer stays single-host and TUIBBS is not near; keep as written is the least defensible. Narrowing or closing does not choose what "TUI Panel" means (INV-043).
- **Facts to carry**: identity and running state come from Coder (workspace id, owner, name, build status, last connected), not from a value the workspace reports about itself; key by workspace id, never by name; the existing heartbeat collector is anonymous (`collector/app.py:5`) and cannot be reused; any route that can start a session starts it with permission checks off on the stock image (`README.md:60-66`, `ccsession:135-141`), which is the strongest reason the narrowed version has no send route; a listener runs inside the workspace and cannot start a stopped one (R2-V3 5.1); "its project's orchestrator" is not an address (#339 accuracy check row 3); expose only the allowed list and never the "never exposed" list (R2-V3 5.3); the nine-item checklist R2-V3 5.7 applies to any version.
- **Rewrites**: R2-V3 section 5.6, texts A (narrow), B (keep, only if the owner revisits option B or C), C (close comment). Part 6.3 states which parts are paste-ready.
- **Owner questions**: Q3, Q4, Q18, Q22.

### 2.6 Orchestrator v2 (#423) and the trust design

- **Points**: X-002, X-005, A-007, A-005; V4 F1, F7, F9, F14; probe INV-021.
- **Verdict (draft)**: "v2" has at least three meanings (E-13): the #339 issue summary's v2 (signed grants plus an orchestrator of orchestrators), the research report's phases 2 to 6, and #423's knowledge layer. #423's gate ("after #339 is complete") has two readings and cannot be applied as written. Recommended gate: PR #539 merged plus the #534 live capture that restores the sweep's `working` class; `/sc:close`, resume and the trust layer are not prerequisites unless the brainstorm decides that v2 relays to agents and not only to a person. v2 is advisory, in a separate command or skill (the sweep "recommends nothing": WC-16, `WORKER-CONTRACT.md:288`), delivers to the person or the coordinator only, and keeps LLM-derived entries marked inferred and apart from sweep facts (V4 F14, supported by V5).
- **Trust (X-005, 66 percent, owner decision)**: promise one grant vocabulary and one audit record format, not one trust design; the three consumers have different threat models and signing does not stop poisoned content (#339 comment 2: "encryption alone is not enough"). Recommended: one vocabulary (Q16).
- **Facts to carry**: a catalogue is at least an eighth data store (R2-V4 5.2: sweep report, observer snapshot, watcher store, PM memory, lessons learned, task ledgers, heartbeat collector, plus the catalogue); it needs a named store, owner, reader set, retention, file mode and a reconciliation with WC-16 ("a dated local file; it is never posted"); first release reads only what the same OS user on the same host can read, no transcript or log content enters the catalogue, no cross-user or cross-workspace read without a written read-permission model (R2-V4 5.3); relayed content is data: fixed typed fields, free text only in one `detail` field, a pinned set tested like the sweep's key set, relay through the coordinator because the contract has no worker-to-worker channel, summarisers read-only (5.4); the sweep sections of #423 must say "on PR #539" until it merges (5.5). *The numbering note in #339 also needs the observer's R1 to R4 releases and the watcher's FU-1 to FU-6 (INV-021; PLAN INFERENCE: R2-V4's comment covers three namespaces).*
- **Rewrite**: R2-V4 section 5.7 (title, body, #339 comment); Part 6.4.
- **Owner questions**: Q14, Q15, Q16.

### 2.7 The "TUI panel" question

- **Question**: in the owner's comment of 2026-11-13T16:20:07Z on Coder#477 ("Ensure this aligns with Orchestrator and TUI Panel"), what is the TUI panel?
- **Answer (draft)**: read it as `superclaude observe` (the #409 dashboard) until the owner says otherwise: about 70 percent (R2-V5 5.7) to 75 percent (R2-V3 5.2: the comment's two nouns mirror the titles of #339 and #409; the phrase appears in no owner-written file); a TUIBBS Go screen is possible about 15 percent (the owner's 2026-11-08 record: "the observer may become a TUIBBS module", "Background, not deciding"). Both are a sequence, not a conflict: a TUIBBS screen would be a second reader of the observer's snapshot, not a second program with its own collector. Before a TUIBBS screen can read anything, four things are missing: a transport (TUIBBS runs on a separate SSH host; "No document in TUIBBS mentions Coder or Orca", sibling `tuibbs-review/notes-3.md:78-84`), an identity envelope (the snapshot `scope` is only `object` or `"UNKNOWN"`; only per-row `hostId` and `hostKind`), an age rule (no liveness field), and re-sanitising. So Coder#477, if kept, is designed for a read-only, identity-tagged, aged copy of the observer snapshot and not around either screen. The contract holds under all three readings; the answer changes the transport, not the contract.
- **Owner decision**: one line on #477 (Q4). Recommended: "TUI Panel = `superclaude observe`; single-host; read-only".
- **Dependencies**: gates Q3 and the Coder#477 rewrite; unblocks nothing in IronClaude.

## Part 3 Content Specification: Point Register (every point)

The merged output carries all 36 X and A points of the debate, grouped by the same systems as Part 2 (12 + 6 + 9 + 3 + 2 + 4 = 36), plus the invariant-probe actions in Part 5. Confidence is the matrix mean (`debate-transcript.md` Scoring Matrix). "Winner" is dropped from the output; the verdict states what holds. "Q" ids are Part 7. Reversible: "yes" means undone by a revert, an edit or an issue-history restore; nothing here is irreversible except a posted comment's notification and a merged PR's squash commit (reversible by a revert PR).

Columns: **id | verdict | conf. | evidence | decision needed (Q, with recommended answer) | course of action | depends on (first) / unblocks | reversible**.

### 3.1 Observer and #409

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| X-012 | The observer is built and merged; V1 C-03 and #409 L16 are wrong | 98% | PR #503, #514; `main.py:572-574` | none | correct #409 (BC-02, BC-04, BC-05) | Q8, Q16 before #409 pass / unblocks #409 pass | yes |
| X-013 | The observer does not read the sweep JSON; neither program mentions the other | 95% | `commands.py:37,393`; grep of both trees | none | no runtime link in version 1; contract note links both | none / unblocks note | yes |
| X-018 | A staged direction was chosen (2026-11-08, 2026-11-11) and releases 1 and 2 shipped; the dated selection record (AC-S) is missing | 74% | owner decisions; PR #503 "Known gaps" | Q8: write the AC-S record | owner writes record or amends #409 AC 1 (BC-18) | owner / unblocks #409 AC 1 text and any release 3 | yes |
| A-003 | Observer built; only the selection record is open (replaces "owner will choose a design") | 96% | as X-018 | Q8 | same as X-018 | as X-018 | yes |
| A-015 | Owner decisions are not where reviewers can read them (master holds only `owner-decisions-20261111.md`) | 83% | `git ls-tree origin/master .dev/issues/409/`; INV-002 | Q7: commit or archive them (yes) | owner commits `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/`; flip PR commits the pass record | before the sibling worktree is cleaned / unblocks flip PR | yes |
| A-010 | The reviewed text moves (#409 body 30,030 to 30,758 bytes; sibling HEAD moved; `409-Phase2` deleted) | 93% | SC-18; INV-030 | none | pin every cite to sha or `updatedAt`; re-read `updatedAt` before each write; abort on change; keep the before-body beside the edit set | none / gates every issue edit | yes |
| X-011 | V1's "observer needs a refresh interval for the file" and V4's "second scheduler" premises are both weakened: the observer polls on its own | 74% | `collector.py` INTERVAL 15.0, MAX_BACKOFF 60.0, STALE 45 s | none | drop both premises; say in the sweep design that an observer polling at 15 s runs beside it (O-10) | none / none | yes |
| X-014 | Fleet scale is closed for the Orca ledger on one host, open for the sweep's per-Run depth and for multi-host; this host is already past the cap | 79% | `adapter.py:57`; INV-017 (513 rows) | none | do not add V1's W-3; state "per-Run depth is the sweep's job; PARTIAL is the steady state" in the note | none / none | yes |
| X-015 | The observer already runs its own 15 s poller beside the sweep; several observers multiply load; simultaneous load never measured | 87% | `collector.py`; `commands.py:84-85`; INV-032 | none | record the load note; `PER_CALL_TIMEOUT` stays UNVERIFIED until the first permitted live read | none / none | yes |
| X-016 | UNPROVEN BOTH WAYS whether `check --all --types question` consumes on a live coordinator Run; Orca's help says `--all` does not mark read | 61% | `owner-decisions-20261111.md:13-15`; `release-gates.md:36-50`; INV-041 | Q6: no scope answer, no flip | seeded test (Part 2.1 step 4), cite help text, pin build; sweep keeps its caution and its wording is corrected (Part 2.2 step 6) | the test / unblocks the flip PR | yes |
| X-002 | The boundary sentence "observer shows the human what happened, v2 shares knowledge between agents" is not stated in the #409 body before decision 8; the weaker "distinct from" holds | 81% | `/tmp/pr339/i409-new-body.md:116,209`; V1 C-34 | none | relabel "proposed boundary (not yet stated in this issue)" (V1 W-7); #423 states the boundary itself | #409 pass / none | yes |
| A-013 | Polling Orca read verbs is the only verified source; event replay unverified; `projection.attention` read by neither program | 65% | `orca-ide orchestration --help` lists 30 verbs, none streams | Q24: who runs the shared read-only capture | add to the shared capture: attention values of one live and one blocked worker, the `worktree ps` agent row of a Run-less session, Orca's event surface in help text only | live Orca / unblocks O-13, O-14, #534 `working` class | yes |

### 3.2 Sweep, #339 and PR #539

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| A-004 | PR #539 will change (two unresolved threads); added keys change pinned golden sets; a sidecar breaks NFR-001 | 88% | GraphQL threads; `ROW_KEYS`; `test_cli_contract.py:1474`; INV-022 | Q1 (INV-008) | resolve both threads; add no keys or files; log items in #534; merge #541 first; refresh the merge ref by push | #541, Q1 / unblocks routing row, note links, #534 edits | yes |
| X-007 | The sweep's reads are not confined: `git status` runs in every `worktree ps` path with the inherited environment; V4's "confines every path" holds for file reads only | 89% | `probes.py:305-327,1203-1214`; INV-008 | Q1: fix (F1 or F2) rather than accept | Part 2.2 step 1 | Q1 / blocks #539 merge | yes before merge |
| A-006 | "Read-only" holds toward Orca only: the sweep writes one report and runs git with inherited env; the observer writes snapshot files and one `check` template | 90% | `probes.py:309`; O-11 | Q1 (via INV-010) | say "no Orca write verb" and list the files each program writes; caveat four texts if the owner accepts | Q1 / none | yes |
| X-004 | `sweep run` always writes a dated report before printing JSON, so a "no write" status criterion cannot be met | 91% | `commands.py:186,277-278` | Q9: persistence is Phase 2 | drop V3 Edit 5; first status record is the observer snapshot | none / unblocks Coder#477 text | yes |
| X-010 | The sweep's rows are per Run but `worktrees[]` and transcripts are host-global | 85% | `probes.py:1203-1214` | none | state the host-global scope in the note and the sweep unit line | none / none | yes |
| A-005 | Nobody defends "Phase 2 and #534 will absorb the deferred items": only a reading list exists; observer R3 and R4 have no package | 85% | `PHASE2-preflight-input.md`; V5 section 10 | none | one table in #534: item, owner, trigger; unowned items labelled "unowned"; rows from R2-V5 A-005 (sweep JSON persistence, machine-started label, guard flip, relationship note, routing row, observer R3 and R4) plus V3's three (identity block, read-only status route, label) | #539 merged / none | yes |

### 3.3 The integration contract

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| A-014 | Two JSON "v1" schemas exist | 94% | `snapshot.schema.json`; design 7.4 | none | always "observe snapshot v1" and "sweep report JSON v1" | none / contract note | yes |
| X-008 | V1's verdict line is wrong; its F-02 table is right; the built observer shows none of the ten dimension names; three vocabularies | 91% | `view.py:96,412`; V1 F-02 | none | drop the verdict sentence; publish the mapping table | none / note | yes |
| X-009 | V1's tally miscounts; nothing depends on it | 95% | by inspection | none | none | none | n/a |
| X-006 | Two decisions: sweep JSON keys (decide in #339 after #539 merges) and snapshot changes (observer spec, additive); the note comes first and names all contracts and the join key; the join key is plausible but not compared on real ids | 74% | `classify.py:891`; `probes.py:435`; D-3 | Q24: run the one comparison | note first; keys decided in #339 after #539; comparison before the word "join key" | #539 merged for keys / unblocks note wording | yes |
| X-017 | Keep two readers (observer, sweep), not one collector; V1's persistence idea survives only for an optional later panel | 70% | O-01; V5 D1 | Q5: yes, keep two | contract note; persistence stays Phase 2 | Q5 / none | yes |
| A-001 | Sweep JSON v1 is a candidate carrier only for v2 and for a #477 status record, not for the observer | 78% | X-013 | Q17: no observer panel for sweep facts now | record in the note; v2 names its field list first | Q17, D-2 / none | yes |
| A-002 | The unit differs by program (sweep: bound Run plus host-global worktrees and transcripts; observer: all Runs on one host; watcher: one workspace; Coder: workspace id); Run-less sessions are in neither ledger | 82% | `probes.py:1203-1214`; `adapter.py` | none | one line per unit in the note; "Run-less sessions: not observable by either program today" | note / none | yes |
| A-009 | UNRESOLVED by evidence: the observer's golden capture records no Orca version; design lock `.780594c521aa` against host `.9cfecdd30b2a`; the sweep compares only the text before the first hyphen; watcher launch shapes assumed until FU-1 | 67% | INV-020; `report.py:160` | none | record `orca --version` in the observer golden capture, the sweep lock line, the FU-1 record and every future v2 fact; treat a second host as UNVERIFIED | live Orca / none | yes |
| A-012 | Keep both programs (provisional); only V5 states it and asks the owner | 66% | V5 D1 | Q5 | proceed as provisional; ask once | Q5 / gates the note | yes |

### 3.4 Issue watcher

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| X-001 | CONFIRMED contradiction: the watcher prompt has no `--pipeline`, so the claim runs at default `worktree` and starts a governed second agent; V3 Edit 8 and V4 C7 and F11 omit it | 91% | `issue.md:43,88`; `launch.py:33`; `issue-watcher.md:44` | Q2: `--pipeline none` plus the owner accepts the session mode in writing | Part 2.4 steps 1 and 2 | Q2 / unblocks #450 edits, FU-1, #423 and #477 text | yes (small PR) |
| X-003 | A watcher-started session is Run-less; today the sweep prints `could not determine`, later possibly "person session (active)"; V4's per-class acceptance criterion cannot be met until #534 gets a row | 78% | `classify.py:302-315,748-767` | Q21: yes, label after FU-1 | reword #409 decision 9 (V2 W-05(a)); #534 row (W-05(b)) | FU-1 D-B / none | yes |
| A-008 | The sweep needs a bound Run and a WC-16 pass; the observer ledger needs neither but sees only orchestration Workers; watcher-launched and person-started sessions are a blind spot in both; "no Run record for `agent launch`" is still inference | 83% | `WORKER-CONTRACT.md:288`; `classify.py:748-767` | none | name the blind spot in both docs; settle at FU-1 (D-A) | FU-1 / none | yes |

### 3.5 Coder#477, #423 and trust

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| X-005 | One grant vocabulary and one audit record format, not one trust design; not decidable from sources | 66% | #339 comment 2; V4 F9; V3 F12 | Q16: one vocabulary | do not promise one design in #409 or #423; #409 decision 6 wording (V4 edit 1) only if Q16 = vocabulary | Q16 / #409 decision 6, #423 | yes |
| A-007 | True today: one owner, one OS user, one host, one enabled watcher per login; the live exposure is untrusted repo and issue content more than other users | 77% | `issue-watcher-setup.md:642`; `probes.py:305-327` | none | state it once in the note and #477; read-permission acceptance criterion before v2 or #477 reads another workspace; treat Orca-listed worktrees as untrusted for git | note / none | yes |

### 3.6 Process points

| id | verdict | conf. | evidence | decision needed (rec.) | course of action | depends on / unblocks | reversible |
|----|---------|-------|----------|------------------------|------------------|----------------------|------------|
| A-011 | Five reports edit the same #409 sentences; edits must be one ordered set | 92% | S-006, X-002 | none | one editor, one ordered edit set per issue; order in Part 4 | none / gates every issue edit | yes |
| A-016 | Reading the issue text and the branch is not enough to find every implementation (the observer sat in the review checkout) | 91% | `main.py`; U-011 | none | before any review says "not built": grep the CLI registration, `git log`, merged PR list | none / none | yes |
| X-019 | V5 overgeneralised: V1 stated no observer exists; V2 W-10 and V4 F13 assumed it; V3 wrote generically and did not check | 87% | R1-V5 concession 7 | none | cite exactly that sentence | none / none | yes |
| X-020 | W-3 is V1's proposed wording, not #409 body text | 94% | SC-19 | none | read V5 RT-F04 as "do not add V1's W-3"; no body edit | none / none | yes |

## Part 4 Content Specification: Dependency Graph and Merge Order

### 4.1 Dependency graph (text)

Nodes: **R** = INV-008 owner ruling and fix specification; **P541** = PR #541; **P539f** = a push to PR #539 that fixes the two threads (new merge ref); **P539m** = PR #539 merged; **GF** = observer guard-flip PR; **RR** = observer routing row; **CN** = contract note (with its test); **E409** = #409 correction pass; **E450** = #450 edits; **FU1** = the watcher's first live test; **C477** = Coder#477 reply (narrow, keep or close); **E339** = #339 comment; **E423** = #423 rewrite; **T534** = the #534 table and wording fixes; **SEED** = the seeded consumption test; **REC** = owner records committed (pass record, decisions, live test guide); **CAP** = the shared read-only Orca capture (attention values, Run-less agent row, event help); **JOIN** = the one real-id comparison (join key); **QA** = owner answers (Part 7).

```
QA(Q1) -> R -> P539f -> P539m
P541 ------> P539f   (P539 CI is clean only after #541; refresh by push, not by re-run)
P539m --> RR, CN(links), T534(edits to design and report.py), E423(start of work), GF(practically)
QA(Q6) + SEED + REC + live-layout attempt + build pin -> GF
P541 --> GF          (fresh branch off master after #541 so CI is not red)
QA(Q8, Q16) -> E409 -> (decision 6 wording needs Q16; AC 1 wording needs Q8)
QA(Q2) -> E450 -> FU1 -> { cron enable (FU-2), D-A, D-B, W-05 label row in T534, W-10 reconsidered }
QA(Q3, Q4) -> C477
E339 -> E423 ; QA(Q14, Q15, Q16) -> E423
CAP -> { O-13, O-14, #534 `working` class, E423 gate }
JOIN -> CN (the word "join key")
REC -> GF ; REC -> E409 (cites owner records)
Independent of #539 (no shared files): GF, E450, FU1, C477, E339, E409, E423 text.
Shares files with #539: RR (HOW-WE-WORK.md, its plugin mirror, routing-table test, `tests/recommend/test_routing_refresh.py`), CN links (`docs/designs/orchestrator-mode.md` exists only on the #539 branch), T534 edits to design lines and `report.py`.
```

Sharing check (INV-036): `gh api pulls/539/files` (1003 files) does not include `tests/core/test_claude_md_worktree_rule.py`; #541 changes only that file; the guard flip touches `observe/` only; the one file every later PR also edits is `CHANGELOG.md`, so each PR rebases its own changelog hunk.

### 4.2 Merge and implementation order across the nine named items

| # | Item | Waits for | Unblocks | Notes and reversibility |
|---|------|-----------|----------|-------------------------|
| 0 | Owner answers and INV-008 ruling (R) | nothing (owner) | everything below | decision only; no code. Q1 to Q4 first. |
| 1 | **PR #541** | nothing | clean CI for #539 and GF | one file, OPEN, CLEAN, six checks SUCCESS (INV-038). Green for one commit: any later reword of the CLAUDE.md bullet fails the test again (INV-033). Reversible by revert. |
| 2 | **PR #539**: fix push, then merge | #541; R | RR, CN links, T534, E423 start, practical GF | the thread fixes (INV-008 fix, Augment thread) are a push and so give a new merge ref (INV-037); a CI re-run alone does not. Add no keys or files. Two unresolved threads are the PR author's. Reversible by revert PR. |
| 3 | **#409 correction pass** (E409), then the other issue edits in the cross-issue order below | Q8; Q16 for decision 6; REC | accurate #409 for every later step | one editor, `updatedAt` re-read immediately before each write (INV-030); can run in parallel with steps 1 and 2 because it touches no code. Reversible by issue history. |
| 4 | **Observer guard-flip PR** (GF) | #541; Q6; SEED; REC; live-layout attempt; build pin; "not passed" text grep | questions panel usable | no file overlap with #539; practically after step 2 because SEED needs live Orca and the owner. `/sc:pr-submit --monitor 3` from a fresh branch off master. Default if Q6 is unanswered: guard stays off. Reversible by flipping the constant back. |
| 5 | **Routing row** (RR) for `superclaude observe` | step 2 (shares four files) | discoverability | not "one row" for the two machine-read tables: `tests/core/test_how_we_work_routing_table.py` needs 8 cells and a resolvable step (`:193-205`), and its other-commands block raises IndexError for a first cell with no backticked slash token and asserts `members == _OTHER_COMMANDS` (`:297-298`); every token needs a command file (`:218,312`). Decide which block carries the row and name the test edits (INV-029); plugin mirror byte-for-byte; add a "person only" line (INV-013). Reversible. |
| 6 | **Contract note** (CN) and its test | step 2 for links; JOIN for the wording "join key"; Q5 | #409 wording, V3 status record, V4 field list | draft on a master-based branch (INV-031); one test comparing its tables with code constants (INV-042). Reversible (remove file and test). |
| 7 | **Coder#477** reply (C477) | Q3, Q4 | none in IronClaude | text A, B or C from R2-V3 5.6 (Part 6.3). Reversible (edit or reopen). |
| 8 | **#450 edits and FU-1** | Q2; edits first | cron enable; D-A; D-B; #534 label row | FU-1 runs `/sc:issue --claim` on a test issue and writes (Part 2.4 step 2 (i)); not read-only. Reversible by hand except ClickUp (unknown). |
| 9 | **#423 rewrite** (E423), then the work it gates | E339; Q14 to Q16; step 2 and CAP for the start of work | v2 brainstorm | the rewrite only states the gate; work starts after #539 merged and the #534 capture. Reversible. |

**Cross-issue edit order (R2-V4 A-011 row, accepted by all five advocates)**: (1) owner answers (claim level, "TUI Panel", #477 keep, narrow or close, v2 gate); (2) #450; (3) #477; (4) #409 pass (V5 facts plus V1 C-07, C-25, C-34; then decisions 1 and 8; then decision 6 only if Q16 = vocabulary; W-05(a) decision 9 and W-06 diagram; banner removal last); (5) one #339 comment; (6) #423 rewrite. The relationship note is a document and can be drafted alongside (2) to (4). Sentences are disjoint across issues (R2-V2 A-011 row; R2-V3 A-011 row), so the order is mainly for cross-links.

## Part 5 Content Specification: Invariant Probe

Source: `invariant-probe.md` (44 findings: 16 ADDRESSED, 28 UNADDRESSED; 2 HIGH, 19 MEDIUM, 23 LOW; HIGH and UNADDRESSED: INV-008). The merged output carries the table below. "Action lands in" names the Part 2 or Part 4 step that carries it.

### 5.1 HIGH and MEDIUM, UNADDRESSED (16 rows: 1 HIGH, 15 MEDIUM)

| id | sev. | what is wrong | action that addresses it | action lands in | depends on / unblocks | reversible |
|----|------|---------------|--------------------------|-----------------|----------------------|------------|
| INV-008 | HIGH | The Codex security thread's remedy does not close the git-config hole: `core.fsmonitor` and `filter.*.clean` both run in linked worktrees; `-c core.fsmonitor=false` stops only the first; a repo filter leaves at least 18 of 29 worktrees exposed | before #539 merges: the owner and the #539 author pick a fix that neutralises both keys or refuses a worktree that defines them (`unscanned` source row, no JSON key); accept it is an allow-list and test change; keep the experiment as a regression test; or accept the finding and caveat four texts | Part 2.2 step 1; Part 4 step 0 | Q1 / blocks #539 merge | fix yes; acceptance reversible only before merge |
| INV-002 | MED | Evidence for "observer first, TUIBBS later" is untracked files in a sibling worktree (`owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/`) | the owner commits or archives them before that worktree is cleaned | Part 2.1 step 3 | Q7 / unblocks citing them | yes |
| INV-003 | MED | The pass record covers one Run (`run_93bfa00cae2b`, an old "Claim issue 375" Run, consumer_generation 3); the guard is one global boolean and `check_run_id` checks syntax only | put "this Run only, or any Run my terminal holds" to the owner and make the code match; no answer means guard off | Part 2.1 step 4 (a) | Q6 / gates GF | yes |
| INV-005 | MED | The seeded test's procedure is unwritten: a tester's terminal must hold no Run; `run-use` on a live coordinator is Q-2, "never tested and forbidden for the observer"; 35 of 53 Runs have consumer_generation 2 or more | write the procedure: plain terminal, `run-create` only, never `run-use`, record `run-current` before and after (precedent: Task 17 sample `run_86013b917868`) | Part 2.1 step 4 (b) | owner or 409 session / gates GF | n/a (a live test that writes seeded messages) |
| INV-009 | MED | The git-config fix is an allow-list change plus three test edits: `test_probes_allowlist.py:503`, `test_readonly.py:85,156,453`, `ALLOWED_GIT` (`probes.py:64-67`), NFR-014 | name them in the fix step; the owner's ruling covers the allow-list edit | Part 2.2 step 1 | Q1 / part of INV-008 | yes |
| INV-010 | MED | If the thread is accepted unchanged, "read-only" or "changes nothing else" still stands in `HOW-WE-WORK.md:335`, `:406`, `sc-sweep-protocol/SKILL.md:3,15`; `/sc:recommend` reads the guide; acceptance is a policy call | the owner ruling states which premise it relies on; if accepted, the four texts get a caveat in the same PR | Part 2.2 step 1 (F3) | Q1 / none | yes |
| INV-011 | MED | Two permission knobs, not one: `CCSESSION_PERMISSIONS=default` and a non-empty `CC_CLAUDE_FLAGS` that replaces the flags whatever it says; on this host both unset and live `claude` runs with `--dangerously-skip-permissions --allowedTools=Grep` | FU-1 records both variables and the real argv of the launched session | Part 2.4 step 2 (c) | Q2 / gates FU-1 | yes |
| INV-017 | MED | The observer is already past its 5-call, 500-row cap on this host (513 rows; only the 13 oldest hidden; order is an observation) | the note says PARTIAL is the steady state and that newest-first order is not a contract | Part 2.3 units | none / none | yes |
| INV-023 | MED | `reclaimable` rows stay in the observer's default view (`HISTORICAL_STATES = ("released", "retained")`, `view.py:35`) while the sweep derives settled from `outcome` and historical from a 6 h window | add a `reclaimable` row to the mapping table and decide which side of "historical" it is | Part 2.3 mapping table | Q23 / none | yes |
| INV-024 | MED | The flipped questions panel may not work for the Runs people point it at: 28 of 53 Runs have no `coordinator_handle`; Q-1 FAIL means only the terminal holding the Run can read; the observer never runs `run-use` | record one live attempt in the real coordinator layout before the flip PR | Part 2.1 step 4 (c) | live Orca / gates GF | n/a |
| INV-029 | MED | The routing row is not one row: the two machine-read tables reject a CLI-only entry (`test_how_we_work_routing_table.py:193-205,297-298,218,312`); #539 edits the same test, `tests/recommend/test_routing_refresh.py:33` and both guide copies | decide which block carries the row; name the test changes in the step | Part 4 step 5 | step 2 / none | yes |
| INV-030 | MED | Issue-body edits have no version check: `gh issue edit` has `--body` and `--body-file` with no etag; #409 `updatedAt` moved after the banner; #423 2026-11-08T10:16:24Z; #339 2026-11-07T11:53:40Z; Coder#477 2026-11-13T16:20:07Z | re-read `updatedAt` immediately before each write; abort on any change; keep the before-body beside the edit set | Part 4 step 3; Part 6 | none / gates all issue edits | yes |
| INV-037 | MED | "#539 needs only a CI re-run after #541" is false: a re-run keeps the old merge ref (`8c689986`) and fails the same test | replace "re-run CI" with "push or update the branch" (or close and reopen) | Part 2.2 step 4 | #541 / unblocks #539 merge | yes |
| INV-039 | MED | A thread fix "without adding JSON keys" is not invisible: `paths` feeds git status, the contract allow-list (`probes.py:1262,1301`) and transcript scans; filtering it forces `could not determine` and changes pinned `worktrees[]` and `sources[]` rows | separate the git-status scope from the contract allow-list; name the golden tests that change | Part 2.2 step 1 | Q1 / part of INV-008 | yes |
| INV-041 | MED | The seeded test is not sufficient alone: (a) Orca's own `check --help` says `--all` "does not mark read" (no debate file cited it); (b) the flip is a bare constant with no build condition; (c) a throwaway Run has no `--wait` listeners or acknowledge cycle ("A bound Run replays the same Delivery until --ack"); (d) Q-1 FAIL means a pass says nothing about usability | cite the help text first; record the Orca build string in the gate record; add a build check or a test that fails when the build changes | Part 2.1 step 4 (b) | owner or 409 session / gates GF | yes |
| INV-042 | MED | One written note has no test; nothing fails when a word, verb list or schema version changes; the note's tables are already incomplete against code (INV-006, 015, 017 to 019, 023) | one test that compares the note's verb lists, schema versions, join key and shared words with `ALLOWED_ORCA`, the observer templates, `SCHEMA_VERSION` and the report constants | Part 2.3 | CN / none | yes |

### 5.2 Carry-forward and addressed items

- **INV-012 (HIGH, ADDRESSED in R2-V2 5.1, 5.5, 5.6 and R2-V3 5.5; carried here because the one-paragraph consensus omits it)**: the watcher's first session reads untrusted issue text with permission checks off; `--pipeline none` removes only the second agent. FU-1 precondition (b) and (c) in Part 2.4 step 2 make it explicit.
- **MEDIUM ADDRESSED with a residual**: INV-001 (record survives until the flip PR commits it: item 5.4 of R2-V1 and 5.9 step 3 of R2-V5; residual: the PR must commit it, Part 2.1 step 4 (d)); INV-004 (snapshot last-writer-wins: handled; residual: no age threshold, Q22); INV-007 (watcher `dispatch.json` at-most-once: handled by the FU-1 gate; residual: `reset --forfeit-guarantee` precondition, Part 2.4 step 3); INV-014 (the owner writes the record, agents cite it; git cannot show authorship, so Q7).
- **LOW, UNADDRESSED (12) with one-line actions**: INV-006 list both `XDG_STATE_HOME` rules in the note; INV-013 one "person only" sentence in the routing row and the note; INV-015 a pinned test that no other worker-written field reaches the report and apply the untrusted-strings rule to the coordinator; INV-018 say a cycle can make 6 calls with `--questions` on; INV-019 "first 50 in Orca list order"; INV-020 the sweep's version check cannot tell two builds apart (A-009); INV-021 widen the #339 numbering comment to five namespaces; INV-028 join on `runId` plus `dispatchId`, exclude empty or duplicate-flagged rows; INV-031 draft the note on a master-based branch; INV-032 simultaneous load never measured (observer 5 to 6 calls per 15 s per process, sweep up to 3 list calls per Run plus up to 50 `worker-show` per wake, the coordinator's own `worktree ps --agent-wait`, the watcher's `skills list --json`; about 0.2 s per call, `PER_CALL_TIMEOUT` UNVERIFIED); INV-033 #541 green for one commit; INV-044 grep `.dev/issues/409/` for "not passed" in the flip PR checklist.
- **LOW or other ADDRESSED, no action**: INV-016, INV-022, INV-025, INV-026, INV-027, INV-034, INV-035, INV-036, INV-038, INV-040, INV-043 (INV-043's narrowed text names both candidates and so does not choose; the choice is Q4).

### 5.3 Unresolved items (state as unresolved in the merged output and the return contract)

1. **INV-008**: the fix is not specified and the owner ruling does not exist. Status BLOCKED_BY_INVARIANTS until it does.
2. **A-009**: the Orca build divergence is unresolved by evidence (matrix confidence 67 percent): the observer records no Orca version, two builds of 1.4.245 are on record, the sweep's check compares only the prefix, a second host was never checked.
3. **X-016**: whether `check --all --types question` consumes on a live coordinator Run is unproven both ways (61 percent); Orca's help text says it does not mark read (INV-041 (a)) but no one ran the seeded test.
4. Also open, each with the single fact that settles it (R2-V5 section 4, R2-V2 section 4): D-A and D-5 (does `agent launch` create a Run or Dispatch; before and after `run-list` and `worker-list` at FU-1); D-B (does the agent row's `prompt` hold the claim); D-3 (is `dispatchId` the sweep's `row_id` minus `orca:`; one comparison on a real Run); D-8 (`projection.attention` values); authorship of the pass record; whether a human can use the questions panel in a terminal that holds a Run (INV-024); whether Orca prunes worker rows (INV-017); the owner API token route to the owner-shared Orca app (D-7).

## Part 6 Content Specification: Issue Body Corrections and Proposed Edits

Nothing in this part is posted by the debate, the plan or the merge executor. "Paste-ready" means the exact replacement text exists in a named debate file and needs only the pins and answers listed. Every body edit is preceded by a fresh read of `updatedAt` (INV-030, A-010).

### 6.1 Corrections to the #409 body

- **Exact wording**: `variant-5-original.md`, section "Corrections to the #409 body (exact wording)", lines 176 to 206: 23 rows BC-01 to BC-23 with columns line, current text, problem, replace with. The "Replace with" cell is the text to post.
- **Pins**: V5 checked the live body (fetched 2026-11-13) only through its first 30 lines against `/tmp/pr339/i409-new-body.md`; all line numbers are the scratch file's. The live body had `updatedAt` 2026-11-13T16:57:51Z when probed and keeps moving. Before posting: re-read the live body, re-map every line number to a quoted sentence, and use the sentence, not the number, as the locator (V2 and V4 conceded the same drift).
- **Disposition by row (debate changes to V5's text)**:

| BC rows | Disposition | Why |
|---------|-------------|-----|
| BC-01 to BC-07, BC-09 to BC-11, BC-13, BC-14, BC-18 to BC-22 | post as written, after re-pinning | unchanged by Round 2; BC-18 (AC 1 "not met as recorded") waits for Q8 if the owner prefers to amend the criterion |
| BC-08 (L52, "observer already has its own collector and classifies nothing") | post as written | supported by V4 F14 and U-008 |
| **BC-12** (L66, "was seen not to consume when the Run's owner read it") | **reword before posting** (PLAN INFERENCE from R2-V5 row 4, not stated in a debate file): say the reads did not consume on a synthetic probe Run read by its owner, that no diagnostic result exists for a live coordinator Run, and that Orca's help says `--all` does not mark read (INV-041 (a)); keep "returns at most 100 rows after the type filter, no read marker, works only from the terminal that holds the Run" | R2-V5 row 4 withdrew O-05; the owner's measurement on the coordinator's own Run is non-diagnostic (X-016, unproven both ways) |
| **BC-15** (L102, plan item 4) | **extend**: "Next: the seeded consumption test and the owner's scope sentence, then the switch-on PR (none exists yet), the owner's AC-S record, then release 3 behind QUESTION-LINK; decide where the reviewer's four asks are built" | R2-V5 row 8; Part 2.1 step 4 |
| **BC-16** (L109, alignment item 1: options (a), (b), (c); proposal (a), with (b) later) | **keep, add**: "(b) needs the sweep's JSON to be stored or captured by the caller; storing it needs an owner decision on the one-report-file rule (NFR-001); both are Phase 2" | R2-V5 row 7; D-2 |
| **BC-17** (L116, decision 8, "v2 reuses ... or the observer's snapshot") | **REPLACE** with R2-V5 row 9: "v2 reads the facts it names in its own field list, each with a named source (sweep JSON for per-Run and disk facts; observe snapshot only for Orca ledger fields)." The decision-8 boundary sentence uses V1 W-7: "Proposed boundary (not yet stated in this issue): this observer shows the human what happened, v2 shares knowledge between agents." | R2-V5 row 13; X-002; the snapshot's 15 row keys carry no command, objective, branch, changed paths, issue or PR |
| BC-23 (banner) | post **last**, after all other rows | R2-V1 section 3 A-011 row |

- **Additions from other variants (not in V5's 23 rows)**:
  - V1 C-07: the body's "five review findings" against 6 threads, 4 resolved, 2 unresolved on PR #539. V1 C-25: `policy` IS a JSON row key, so #409's "not keys in the JSON" is wrong. V1 C-34 and W-7: the boundary sentence (see BC-17). V1 C-18: "read-only" claim (see INV-008).
  - V2 W-05(a), decision 9: "A session the watcher launches has no Run and no coordinator; the sweep cannot tell it from a person's session and may label it person-started." V2 W-06, the diagram: watcher to ordinary top-level session, no coordinator; the "project's orchestrator" box goes. W-11 (item 9): show "disabled or planned stop" from `disabled_since` and `enabled`, not only `healthy` (UNVERIFIED how the observer would learn `enabled`).
  - V5 R2 section 5.6 last row: acceptance criterion 2 still says "human attention items"; owner decision 8 (2026-11-11) says "coordinator questions", never "human".
  - V4 edit 1 (decision 6: "Decide one design, not two." becomes "Decide one grant vocabulary and one audit record.") only if Q16 = vocabulary; V4's #409 edit 2 (append to decision 8) is superseded by W-7 plus BC-17.
  - Do NOT add V1's W-3 (fleet mode wording; X-020).
  - Other carriers of the stale "not passed" wording are fixed in the guard-flip PR, not by the issue edit (INV-044).
- **Order inside the pass** (R2-V1 section 3 A-011 row, accepted by R2-V5 row 13): (1) V5 facts plus V1 C-07, C-25, C-34, C-18; (2) decisions 1 and 8 (W-7, BC-17 replaced); (3) decision 6 (only if Q16 = vocabulary); (4) decision 9 and the diagram (V2); (5) banner removal last.
- **Paste-ready**: yes for the rows marked "post as written" once re-pinned; yes for BC-17 (text above) and the V2 wordings; not yet for BC-12, BC-15, BC-16 (replacement text above is the plan's, to be written by the merge executor into the merged output as proposed text and marked PLAN INFERENCE); no for decision 6 (waits for Q16) and BC-18 (waits for Q8).

### 6.2 Proposed edits to #450 (watcher rollout)

- **Source**: `variant-2-original.md` lines 59 to 67 ("Proposed edits to #450", items 1 to 5), with the changes below from `round2-rebuttal-V2.md` sections 1, 5.1, 5.4, 5.6 and from INV-011 and INV-012.

| # | V2 edit | Disposition | Paste-ready |
|---|---------|-------------|-------------|
| 1 | "Done when 0: decide the claim level ... Recommended `--pipeline none` ..." | keep; wording depends on Q2 (either "changed to `--pipeline none`" or "kept at the default, with OB-H1 item 1, OB-H2, OB-H3 (#394) recorded as passed") | after Q2 |
| 2 | Replace item 4 with "Done in #485"; fix the test count (2655 against 2637 and 2653) | keep | yes |
| 3 | Item 1 (FU-1): record session identity fields, before and after `run-list` and `worker-list`, the Orca Claude command, session name behaviour, tab-map entry, permission mode; unsanitised values in a private note, sanitised fixture only committed | **extend** with: `CCSESSION_PERMISSIONS`, `CC_CLAUDE_FLAGS` and the real argv (INV-011); the owner's written acceptance of the first session's permission mode (INV-012); the writes the live test makes and closing or unlabelling the test issue (R2-V2 5.6); the Orca build string (A-009); the real operation-id path | after those additions are written in |
| 4 | Runbook step 1.3a: create the watcher worktree with an agent, name its owner | keep; add that `reset --forfeit-guarantee` on an `unknown` entry first requires checking Orca for a live session in the configured worktree (R2-V2 5.4) | after Q20 names the person |
| 5 | "Do not build the observer's watcher reader, and do not route watcher prompts through a listener, until FU-1 is recorded" | **reword** (R2-V2 row 1): "Do not add a watcher panel to `observe`, and do not route watcher prompts through a listener, until FU-1 is recorded." | yes |

- Edits 2, 4 and the runbook additions share no sentence with another report (R2-V2 A-011 row): apply independently of the #409 pass and of #539.

### 6.3 Coder#477 rewrites

- **Source**: `round2-rebuttal-V3.md` section 5.6, lines 120 to 172: **A** narrow (title "Read-only workspace status and identity for the Orchestrator observer (no prompt routing)", Feature Summary, Problem Statement, Proposed Solution, eight acceptance criteria, Out of Scope, corrected Components Affected, Related); **B** keep (only if the owner revisits option B or C; replacement Problem Statement and eight criteria including the fixed request list, owner-accepted permission mode, per-request grant and one-use nonce, separate read and send credentials); **C** close (comment text with two reopen conditions).
- **Recommendation**: A (about 65 percent) after Q3 and Q4; C if the observer stays single-host and TUIBBS is not near; B is the least defensible and only if the owner revisits option B or C.
- **Paste-ready**: C yes. A: not fully; it holds the placeholder `[N minutes: owner decides]` (Q22), a "Depends on" line naming Q3 and Q4, an owner-token route to the owner-shared Orca app that is UNVERIFIED (D-7), and it names "observe snapshot v1", which must match the contract note's naming (A-014). B: not until the grant format of #339 exists. The Coder-repo paths in "Components Affected" were checked only by V3 and not re-checked by any other variant; keep "per V3".

### 6.4 #423 rewrite and #339 comment

- **Source**: `round2-rebuttal-V4.md` section 5.7, lines 134 to 209: the #423 title `[FEATURE] Orchestrator v2 (knowledge layer): catalogue of agent work and advisory cross-agent reviews`; a body that replaces Feature Summary, Proposed Solution, Acceptance Criteria (14 boxes), Out of Scope, Components Affected and Related (Problem Statement and User Story stay); and a three-paragraph #339 comment with no body edit.
- **Dependencies inside the text** (the merged output must flag them): (1) the sequencing gate "after PR #539 merges and the #534 live capture" assumes Q14 = Phase 1 only; (2) the Related bullet on #331 says "the claim at its default level also launches a second governed agent (#450)", which is false if Q2 = `--pipeline none` and must change then; (3) the "if #477 is kept" clause follows Q3; (4) the words "on PR #539" must go once it merges; (5) the "Collision Lens" criterion states it is a synthetic image, not built.
- **Addition to the #339 comment** (PLAN INFERENCE from INV-021, which says the comment covers only three of at least five namespaces): add one sentence: "Other numbering in play is not a version of #339: the observer's releases R1 to R4 and the watcher's FU-1 to FU-6."
- **Paste-ready**: the #339 comment yes (with the added sentence); the #423 body after Q14, Q2 and Q3 settle the three clauses above.
- **Not edited**: the #339 body.

## Part 7 Content Specification: Deduplicated Owner Questions

The five reviews, the Round 2 "Who can check" lists and the invariant probe ask the owner overlapping questions (S-007: the first four reports pose 29, many duplicated; V5 adds 10; Round 2 adds more). The merged output presents the 24 below, each once, in the order they gate other work, one decision at a time, each with the plain-English meaning, what each answer would do, and a recommended answer. Where the debate gave no winner the recommendation is the orchestrator's default and is labelled "default (no debate verdict)". The owner is not asked anything that the files can answer.

| Q | Question (plain English) | Recommended answer | Gates | Sources deduplicated |
|---|--------------------------|--------------------|-------|----------------------|
| Q1 | The Codex security thread on PR #539: fix the `git status` hole (neutralise both `core.fsmonitor` and `filter.*.clean`, or refuse any worktree that defines them and show it as `unscanned`) or accept the risk and add a caveat to four "read-only" texts? | Fix, by neutralising both keys or refusing and showing `unscanned` (about 70 percent; PLAN INFERENCE from the probe's stated action) | #539 merge; X-007, A-006, INV-008, INV-009, INV-010, INV-039 | V1 F-07 and C-18; INV-008, INV-009, INV-010 |
| Q2 | Should the watcher's claim run at `--pipeline none` (claim only: assign, comment, no worktree, no second agent) or at the default `worktree` level (claim plus worktree `issue-<N>` plus a governed second agent)? And do you accept in writing that the first session runs with permission checks off on the FU-1 test issue? | `--pipeline none`, and yes, in writing, for the test issue only | #450 edits, FU-1, X-001, INV-011, INV-012, #423 and #477 text | V2 Q1 and D-G; INV-011; INV-012 |
| Q3 | Coder#477: keep as written, narrow to read-only status and identity with no prompt routing, or close? | Narrow (about 65 percent); close if the observer stays single-host and TUIBBS is not near; keep only if you revisit the listener options | #477 rewrite | V2 Q2 and D-H; R2-V3 D-1 and 5.6; V4 D-4 |
| Q4 | What does "TUI Panel" mean in your 2026-11-13 comment on Coder#477: `superclaude observe` (the #409 dashboard), a future TUIBBS screen reading the snapshot, or both? | `superclaude observe`; TUIBBS is a possible later reader; single-host; read-only (about 70 to 75 percent) | Q3, #477 text, Part 2.7 | V5 Q1 and D9; R2-V3 D-2; R2-V5 D-4 |
| Q5 | Do you want one written contract note between the observer and the sweep (keep both programs), an optional observer panel that reads the sweep's JSON, or a merge? | One contract note; keep both programs (A-012 and X-017) | the note, X-006, A-001 | V5 Q2 and D1; V1 Q1; V4 D-3 |
| Q6 | Does your 2026-11-12 pass for the coordinator-questions read cover only `run_93bfa00cae2b` or any Run your terminal holds? Do you want it flipped before the seeded consumption test has run? | Default (no debate verdict): do not flip before the seeded test; after it, the scope sentence is yours; no answer means the guard stays off. The only debate recommendation to widen scope (V5 D5(ii)) was withdrawn | the guard-flip PR; INV-003, INV-024, X-016 | V5 Q3 and D5; INV-003; R2-V1 D-3; R2-V5 row 8 |
| Q7 | Will you write the pass record yourself (git cannot show who typed it) and commit or archive the records that exist only in the sibling worktree (`owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/`)? | Yes, both, before that worktree is cleaned | the guard-flip PR; A-015, INV-002, INV-014 | V5 Q10; INV-002; INV-014 |
| Q8 | Will you write the dated direction-selection record (AC-S) naming the staged direction, your reading of "production integration" and the command name, or amend #409's first acceptance criterion? | Write the record (one paragraph) | #409 AC 1 text; X-018, A-003 | V5 Q4 and D6 |
| Q9 | Should the sweep's JSON ever be stored beside the report (which needs you to relax "a sweep adds exactly one report file", NFR-001), or captured from stdout by the caller, or not at all? | Not now. Phase 2: caller-side stdout capture first; relax NFR-001 only if a stored file is needed | persistence, X-004, A-001 | V1 Q2 and D-1; V5 R1 concession 4 (withdrawn); R2-V2 D-E; R2-V3 D-3; R2-V4 D-1 |
| Q10 | May the sweep ever read Orca messages with `check --all --types question`, or is that the observer's alone? | Observer's alone for now; correct the sweep's two sentences (Part 2.2 step 6) | sweep allow-list (NFR-014), O-04, O-05 | V5 Q6 and D4 |
| Q11 | Is the "static report in chat every 3 to 5 minutes" that #339 asks for the sweep's summary, the `observe --once` text, or both? | The sweep summary only until the contract note exists | #339 D2 | V5 Q7 and D2 |
| Q12 | Should the observer get a routing row in `HOW-WE-WORK.md` (and its plugin mirror and the sc-recommend table)? | Yes, one row, own small PR after #539 merges (the two table tests need edits: INV-029) | RR | V5 Q8 and D8 |
| Q13 | Is bare `orca` acceptable for the observer when the sweep's rule is "never bare `orca`"? | Yes: the observer validates the binary with `skills list --json`; record it in the note. The watcher uses the same rule, so only the sweep differs | note | V5 Q9; R2-V2 section 2 |
| Q14 | What does "#339 is complete" mean for #423's gate: PR #539 merged only, or also `/sc:close`, resume and the trust layer? | PR #539 merged plus the #534 live capture; the other phases only if the brainstorm decides v2 relays to agents | #423 rewrite | V4 Q1 and D-2 |
| Q15 | Must v2 ever deliver a course correction to a session that is not a worker, or does it report to a person or the coordinator only? | Report only (advisory); no delivery to non-worker sessions | #423 acceptance criteria | V4 Q4 and D-8 |
| Q16 | Trust: promise one trust design, or one grant vocabulary and one audit record format? | One vocabulary and one audit format (X-005, 66 percent) | #409 decision 6, #423, #477 text | V3 Q7; V4 D-4; X-005 |
| Q17 | Should the observer ever show the sweep's facts (frozen plans, safe-to-close, contract questions, git state) on the same screen as the Orca ledger? | No, not now; if yes later, persistence (Q9) becomes a real requirement | A-001, D-6 | V5 D-6; V1 Q1 |
| Q18 | Do you want a channel that copies the observer snapshot from the Coder workspace to the separate TUIBBS host? | Not before observer release R4 or an owner statement that a TUIBBS screen is planned | #477 text | R2-V5 D-9; V3 D-1 |
| Q19 | Which of the reviewer's four asks (Fleet Quilt, Decision Desk, Loop Detector or Mission Pulse, summary and links) comes first, and in which program? | Fleet Quilt or Decision Desk first, in the observer, after the contract note and the shared capture | `release-gates.md` rows | V5 Q5 and D7 |
| Q20 | Who owns the agent in the watcher worktree, and may that one worktree hold up to 6 new sessions a day that are never owned by a coordinator? | A named person owns it; watcher sessions stay person-reviewed top-level sessions | runbook step 1.3a | V2 Q2 and Q4; R2-V2 5.2 |
| Q21 | May the sweep label machine-started sessions separately from person-started ones, reading `worktree ps` agent rows (`prompt`, `paneKey`)? | Yes, in Phase 2 and only after FU-1 shows what those rows hold (D-B) | #534 row, X-003 | V2 Q3; V4 D-5 |
| Q22 | What age makes a snapshot or a workspace record "stale" (the observer's own feed uses 45 s; a file on disk has no liveness flag)? | Your number; no debate recommendation. Until set, readers show any file older than the producer's own cycle as stale and print its age | note, #477 AC | INV-004; R2-V3 5.6 A |
| Q23 | Is a `reclaimable` worker live, historical, or its own state? | Its own state, shown with Orca's word, until you decide (default, no debate verdict) | mapping table, INV-023 | INV-023 |
| Q24 | Who runs the shared read-only Orca capture (attention values for a live and a blocked worker, the agent row of a Run-less session, Orca's event help) and the one-time comparison of the observer's dispatch ids with a sweep's `row_id` list? | The 409 session with live Orca, read-only, one sitting | CAP, JOIN, A-013, X-006 | V5 D3 and D-3; R2-V1 D-5; R2-V2 D-A, D-B; R2-V4 D-7 |

A small number of questions are marked "default (no debate verdict)". Q1's 70 percent and Q6's default are the orchestrator's reading of the probe and of the withdrawn D5(ii); the merged output must say so beside them.

## Changes NOT Being Made (with rationale)

The merged output carries this table as Part 8 so rejected proposals are not reopened. "Diff Point" is the debate id; the evidence is the debate's own.

| Diff Point | Non-Base or rejected approach | Rationale for not making it |
|------------|-------------------------------|-----------------------------|
| X-004, A-001, X-017 | Persist the sweep JSON now (V1 F-03 and Q1 "persist; it keeps one collector"; V5 R1 concession 4 "cheap"; V3 Edit 5 status route "produced without any write") | NFR-001 ("a sweep adds exactly one report file") is pinned by the design (`orchestrator-mode.md:128`) and two tests (`test_readonly.py:300,400`, `test_cli_contract.py:1192,1361,1474`); a sidecar needs an owner requirement change inside a contested PR; `sweep run` writes a report on every run. V1, V2, V3, V4 and V5 all converged on Phase 2 (R2-V1 D-1; R2-V5 row 7). Alternative kept open: caller-side stdout capture inside the WC-16 pass (R2-V2, R2-V4). Matrix: X-004 V1 91%, X-017 V5 70%. |
| A-012, X-017 | Merge the two programs, retire one, or have the sweep reuse the observer's adapter (V5 D1 option (c); V1 "one collector") | The facts differ (git, contracts and transcripts versus fleet-wide Orca rows); one collector would break one design's rules (stdlib-only models, exact-token owner-signed allow-list NFR-014); #539 is in review; the observer's only gain for the sweep is paging. A shared parser is revisited after #539 merges (D-7). A-012 is 66 percent and provisional: Q5. |
| X-013, X-011, X-015 | Build an observer reader of the sweep JSON, or let the observer start the sweep itself (V1 F-01 (1), #409 L109 "read the sweep's JSON, not a second collector"; V4 proposal (b); V5 BC-17 as worded) | The observer exists, reads Orca only and has its own 15 s poller; the sweep's JSON is stdout-only; the snapshot's 15 row keys carry no command, objective, branch, changed paths or issue or PR (R2-V5 row 9); running the sweep from a reader writes a report and runs `git status` in every worktree each time (X-004). X-013 95%. An optional panel stays a later owner choice (Q17). |
| X-005 | One trust design instead of one grant vocabulary (V3 F12 and Edit 7; #409 decision 6 "Decide one design, not two") | The three consumers have different threat models and signing does not stop poisoned content (#339 comment 2: "encryption alone is not enough"); under watcher option A the watcher's trust is a local model (V3 itself). Not decidable from sources, so it is Q16; the recommended default is the narrower promise. X-005 66%. |
| X-001 | Keep the watcher's default pipeline unexamined, or restate it as "one ordinary session" (V3 Edit 8; V4 C7 and F11) | `issue.md:43,88` and `launch.py:33` show a second governed agent is created at the default level; the design says the claim stops at `next-steps.md`. X-001 91%. |
| A-004 | Add JSON keys, a sidecar file, wording fixes or observer wording inside PR #539 | two threads are unresolved and the key set is golden-tested (`ROW_KEYS`); log items in #534 and edit after merge. A-004 88%. |
| A-004 | "#539 needs only a CI re-run" (R2-V1, R2-V2) and "needs a rebase" (V1 C-08) | a re-run keeps the old merge ref (INV-037); there is no file overlap with #541 (INV-036). |
| X-016 | Treat the observer's non-consumption as established (V5 O-05 and its sweep rewording) or the sweep's "cannot be read without consuming" as established (the sweep's `report.py:534`) | unproven both ways on a live coordinator Run (61 percent); the owner's measurement is non-diagnostic; Orca's help says `--all` does not mark read (INV-041 (a)). Both programs keep their cautions; the sweep's two lines are reworded to state only what is established. |
| A-003, X-018 | Flip the guard on the owner's "Do it" record alone, or recommend scope "any Run the terminal holds" now (V5 D5(ii)) | the seeded consumption test, the live-layout attempt, the build pin and the owner's own scope sentence are prerequisites (R2-V5 row 8; INV-003, INV-005, INV-024, INV-041). |
| X-002 | State the observer and v2 boundary sentence as already established in #409 (V4 C8, V4 #409 edit 2) | the sentence appears only inside decision 8 (V1 C-34; circular proof withdrawn by V4); it is proposed wording (V1 W-7). X-002 81%. |
| X-007 | Treat "the sweep confines every path" as true (V4 F17) | it holds for file reads only; `git status` runs with the inherited environment in every listed worktree (`probes.py:305-327,1203-1214`). X-007 89%. |
| INV-008 | Accept the Codex-suggested remedy ("restrict `git status` to the selected repository" and "disable executable Git config") as sufficient | measured: `core.fsmonitor` and `filter.*.clean` both ran; one flag stops only the first; a repo filter leaves a shared `.git/config` exposed. |
| X-019, X-020, X-009 | Repeat "all four earlier reviews were wrong about one fact", "drop W-3 from the #409 body" or V1's tally | overgeneralisation, a mislabel and a miscount; none changes a decision. |
| A-013 | A separate research task on an Orca event stream | the shared capture D3 covers a help-text read of Orca's event surface at no extra cost (R2-V1, R2-V2, R2-V3, R2-V4, R2-V5 all agree). A-013 65%. |
| A-011 | Five parallel edit sets to the #409 sentences | one editor, one ordered edit set, pinned cites (A-011 92%). |
| X-001 family | A listener, inbound port or address registry for the watcher (Coder#477 as written) | design decision D1 option A (2026-11-07) and the stopped-workspace case (R2-V3 5.1); the narrowed read-only form is the recommendation. |

## Risk Summary

| Change # | Risk | Impact if failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | detail lost when V5 is condensed; reader cannot find a V5 fact | restore the V5 block from `variant-5-original.md` (Appendix A names each section) |
| 2 | Low | verdict overstates or understates a fact | edit the Part 1.1 block; ids and numbers are traceable to the matrix |
| 3 | Low | a surviving finding listed as dead, or a dead one missing | the list uses each advocate's own concession; re-check against R2 section 1 |
| 4 | Medium | the flip is read as ready when its prerequisites are open | Part 2.1 step 4 lists all prerequisites; remove nothing from it |
| 5 | High (subject), Medium (text) | a wrong fix design is implied, or INV-008 is understated | the text states requirement and options only; any fix design goes back to the #539 author and the owner |
| 6 | Medium | the contract note drifts from code (INV-042) | add the one comparison test; the note is a new file and can be removed |
| 7 | Medium | the permission-mode facts are true only on this host | label "verified on this host (INV-011); other hosts UNVERIFIED" |
| 8 | Medium | Coder-repo facts rest on V3 alone | keep "per V3"; re-check before posting any rewrite |
| 9 | Medium | v2 scope judged on V4 items that were narrowed | include only Round 2 survivors; weighted survival of V4 is 0.818 |
| 10 | Low | the working reading of "TUI Panel" is taken as settled | stated as 70 to 75 percent; Q4 is the owner's |
| 11 | Low to Medium | confidence or evidence mis-copied from the matrix (its cell text is truncated) | evidence column uses diff-analysis and R2 wording; matrix mean confidence is exact |
| 12 | Medium | order assumes answers not yet given | every step names what it waits for; a late answer moves one step |
| 13 | Low | a probe row dropped | Part 5 lists all 16 HIGH and MEDIUM UNADDRESSED, the HIGH carry-forward and all LOW |
| 14 | Medium | stale line numbers, a moved body, a conflicting owner edit (A-010, INV-030) | locate by sentence; re-read `updatedAt` before each write; keep the before-body beside the edit |
| 15 | Low to Medium | an edit waits on Q2 or Q20 | edits 2 and 5 are independent; 1, 3, 4 wait |
| 16 | Medium | text A has a placeholder and an UNVERIFIED route | do not post A until Q22 and D-7 are settled; C is ready |
| 17 | Low to Medium | three clauses depend on Q2, Q3, Q14 | flag each clause; post the #339 comment first |
| 18 | Low | an owner question missing or duplicated | each question names the sources it merges |
| 19 | Low | a rejected proposal quietly reappears | Part 8 mirrors this table; cite it in review |
| 20 | Low | status rewritten to "converged" | the plan forbids it; return contract carries BLOCKED_BY_INVARIANTS and INV-008 |
| 21 | Low | a block without a provenance tag | tag every block; the merge log lists untagged blocks as failures |
| 22 | Low | a gloss that no source supports | write "UNVERIFIED meaning" instead |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-13T18:48:21Z
- **Debate status carried into the merge: BLOCKED_BY_INVARIANTS.** One HIGH and UNADDRESSED invariant (INV-008, the git-config hole behind the open Codex security thread on PR #539). The merged output and the return contract carry it as unaddressed and as the first, blocking action in Part 2.2 and Part 4. Auto-approval of this plan approves the plan's content; it does not waive INV-008, which only the owner can rule on (accepting a security risk in an open PR is the owner's decision), and it does not turn "unresolved" items A-009, INV-008 and X-016 into resolved ones.
- Return contract fields the lead should carry: `status: BLOCKED_BY_INVARIANTS`; `convergence: 100% on 36 of 36 X and A points (63.9% before Round 2); taxonomy covered; invariant gate not passed`; `unresolved: INV-008 (no fix specified, owner ruling pending); A-009 (Orca build divergence); X-016 (consumption on a live coordinator Run unproven both ways)`; `base: Variant 5 (0.915; V2 0.893; tiebreaker V5 18 of 36 matrix points)`.
