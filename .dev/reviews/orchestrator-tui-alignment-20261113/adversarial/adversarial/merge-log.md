# Merge Execution Log

## Metadata
- Base: Variant 5 (review 05, "The built `superclaude observe` versus Orchestrator mode (#339)", `variant-5-original.md`; score 0.915)
- Executor: merge-executor agent
- Plan executed: `refactor-plan.md` (22 planned changes, applied in plan order)
- Merged output: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md` (842 lines, 156,078 bytes; Parts 0 to 8 plus Appendix A)
- Changes applied: 22 of 22 planned
- Merge execution status: **success** (no change failed or was skipped; post-merge validation PASS)
- Debate status carried unchanged, not a merge result: **BLOCKED_BY_INVARIANTS** (INV-008 unaddressed; also unresolved: A-009, X-016). The merged output shows it at the top (status block, Part 0.1, 0.2), in Part 1.1, Part 2.2 action 1, Part 4 step 0 and Part 5.3. It was not rewritten to "converged".
- Timestamp: 2026-11-13T18:59:05Z
- Read-only otherwise: no GitHub write, no git change, nothing posted. Only the merged output and this log were written.

## Changes Applied

Validation legend for every entry: Structural integrity (heading levels, order), References (every "Part N", "action N", "step N", Q, E and BC id resolves), Contradictions (no new conflict introduced). All entries passed unless a note says otherwise. Merged-output locations are given as Part numbers.

### Change 1: Rebuild the base as a decision document, keep its evidence
- **Status**: Applied
- **Source**: Variant 5, all sections
- **Target**: Base, whole file (restructure) -> merged output Parts 0 to 8
- **Before**: V5 review order: scope read, what the observer is, overlap, re-test, corrections, decisions, questions, verdict
- **After**: Decision-document skeleton (Parts 0 to 8, Appendix A). V5 "Scope read" moved to Appendix A with a section-pointer table; V5 sections 1 to 10 condensed into facts E-01 to E-18 (Part 1.2) and Part 2.1; V5 sections remain whole in `variant-5-original.md`
- **Provenance tag**: `<!-- Source: Base (original, modified) - restructured into a decision document per Change #1 -->` (status block); equivalent tags on Part 2.0, Part 3.0, Part 7, Appendix A
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 2: Replace the V5 verdict with the adjudicated verdict
- **Status**: Applied
- **Source**: V5 Verdict, R2-V5 section 2 "Net effect", matrix (X-019)
- **Target**: Part 1.1 (replace)
- **Before**: V5 verdict "All four earlier reviews and the #409 body were wrong about one fact"
- **After**: The plan's draft wording carried verbatim as a block quote, plus the exact X-019 sentence and the nothing-run-against-live-Orca statement
- **Provenance tag**: `<!-- Source: Base (original, modified) - V5 "Verdict" replaced by the adjudicated verdict per Change #2 (X-019 ...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: List of findings the debate withdrew or disproved
- **Status**: Applied
- **Source**: R2-V1 to R2-V5 section 1, INV-008, INV-017, INV-037, INV-041
- **Target**: Part 1.3 (insert, 19 rows)
- **Before**: Section did not exist
- **After**: Table "Finding | From | Why it fell | What stands instead", every row from the plan's Part 1 specification
- **Provenance tag**: `<!-- Source: Variants 1 to 5 Round 2 rebuttals ... - merged per Change #3 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Part 2.1 observer and #409
- **Status**: Applied
- **Source**: V5 S1 to S10, O-06, O-09, D5, D6, D8; V1 C-07, C-25, C-34; INV-001 to INV-005, INV-014, INV-017, INV-018, INV-023, INV-024, INV-041, INV-044
- **Target**: Part 2.1 (restructure, guard-flip prerequisites kept as lettered checklist (a) to (f))
- **Before**: V5 sections 1 to 10 and D5 option (ii) "any Run the terminal holds" as the recommendation
- **After**: Verdict, six ordered actions, "Do not", cap facts, owner questions; the D5(ii) recommendation is dropped and recorded in Part 1.3 and Part 8
- **Provenance tag**: `<!-- Source: Base (original, modified) - V5 S1 to S10 ... merged per Change #4 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS
- **Plan text corrected (not a content change)**: the plan's action 5 said "Part 4 step 6" for the routing row, but the plan's own Part 4 table puts the routing row at step 5 (the contract note is step 6); the merged text uses step 5. The plan's owner-question list for 2.1 omitted Q12, which Part 7 says gates the routing row; Q12 was added to the list.

### Change 5: Part 2.2 sweep, #339 and PR #539, INV-008 first and blocking
- **Status**: Applied
- **Source**: V1 F-07, C-18; R2-V1 sections 3 and 5; R2-V5 section 3 A-004 and 5.8; INV-008, INV-009, INV-010, INV-015, INV-019, INV-020, INV-022, INV-033, INV-036 to INV-040
- **Target**: Part 2.2 (insert, INV-008 is action 1)
- **Before**: Section did not exist
- **After**: Eight ordered actions; INV-008 labelled UNRESOLVED; options F1, F2, F3 stated as requirement and options only; "about 70 percent" labelled PLAN INFERENCE and "default, no debate verdict"; no fix code invented
- **Provenance tag**: `<!-- Source: Variant 1 (variant-1-original.md), F-07 and C-18, with Round 2 rebuttals ... - merged per Change #5. INV-008 is the first, blocking action ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Part 2.3 the integration contract
- **Status**: Applied
- **Source**: R2-V5 5.1 to 5.9; R2-V2 section 3 X-006 row; R2-V4 section 3 X-006 row; INV-006, 013, 017 to 020, 023, 028, 031, 035, 042
- **Target**: Part 2.3 (insert)
- **Before**: Section did not exist (V5 O-01 to O-16 and "Facts each program owns" folded in)
- **After**: Note content in ten bullets (probe additions in italics, as the plan marks them); R2-V5 5.3 units table and 5.6 mapping table carried verbatim; one `reclaimable` row added to the mapping table and labelled as the probe's addition (INV-023). The note itself is described, not created
- **Provenance tag**: `<!-- Source: Variant 5 (round2-rebuttal-V5.md), Section 5.1 to 5.8, with additions ... - merged per Change #6 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS
- **Plan text corrected**: the plan's owner-question list for 2.3 omitted Q13 (bare `orca`), which Part 7 says gates the note; Q13 was added.

### Change 7: Part 2.4 issue watcher (#331, #450)
- **Status**: Applied
- **Source**: V2 W-01 to W-16, "Proposed edits to #450"; R2-V2 5.1 to 5.7; INV-007, INV-011, INV-012, INV-016, INV-034
- **Target**: Part 2.4 (insert; FU-1 precondition list (a) to (i) in action 2)
- **Before**: Section did not exist
- **After**: Verdict, five ordered actions, permission-mode facts labelled "verified on this host only"
- **Provenance tag**: `<!-- Source: Variant 2 (variant-2-original.md), findings W-01 to W-16 ... - merged per Change #7 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 8: Part 2.5 Coder#477
- **Status**: Applied
- **Source**: V3 F1, F2, F6, F8, F10 to F14, F17; R2-V3 5.1 to 5.7
- **Target**: Part 2.5 (insert)
- **Before**: Section did not exist
- **After**: Verdict "narrow, about 65 percent, after Q3 and Q4"; Coder-repo facts marked "per V3"; rewrites referenced to Part 6.3
- **Provenance tag**: `<!-- Source: Variant 3 (variant-3-original.md), findings F1, F2, F6, F8, F10 to F14, F17 ... - merged per Change #8 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 9: Part 2.6 Orchestrator v2 (#423) and the trust design
- **Status**: Applied
- **Source**: V4 F1, F7, F9, F14; R2-V4 5.1 to 5.7; INV-021
- **Target**: Part 2.6 (insert)
- **Before**: Section did not exist
- **After**: Verdict (three meanings of "v2", recommended gate), trust position (X-005, one vocabulary), facts to carry; only Round 2 survivors included
- **Provenance tag**: `<!-- Source: Variant 4 (variant-4-original.md), findings F1, F7, F9, F14 ... - merged per Change #9 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Part 2.7 the "TUI panel" question
- **Status**: Applied
- **Source**: R2-V5 5.7, R2-V3 5.2 and D-2, INV-043
- **Target**: Part 2.7 (insert)
- **Before**: Section did not exist
- **After**: Working reading (observer, 70 to 75 percent), weaker reading (TUIBBS, about 15 percent), four missing things, one-line owner answer (Q4)
- **Provenance tag**: `<!-- Source: Variant 5 (round2-rebuttal-V5.md), Section 5.7, with round2-rebuttal-V3.md Section 5.2 and D-2 ... - merged per Change #10 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 11: Part 3 point register
- **Status**: Applied
- **Source**: Scoring Matrix (36 X and A points), R2 section 3 tables, diff-analysis rows
- **Target**: Part 3 (insert; six tables, 12 + 6 + 9 + 3 + 2 + 4 = 36 rows)
- **Before**: Section did not exist
- **After**: Eight columns in plan order. Confidence is the matrix mean: A-009 67%, X-006 74%, A-005 85%, A-011 92% are used where a single Round 2 file shows a different figure (R2-V5: 65%, 75%, 88%, 93%). X-016 and A-009 rows carry "UNRESOLVED"
- **Provenance tag**: `<!-- Source: ... matrix rows ... - merged per Change #11 -->` on each of the six tables
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 12: Part 4 dependency graph and merge order
- **Status**: Applied
- **Source**: R2-V5 5.9, R2-V4 A-011 row, R2-V1 section 5 item 5, INV-001, 002, 029, 031, 033, 036, 037
- **Target**: Part 4 (insert; replaces V5's dependencies table)
- **Before**: V5 "Dependencies for integrating Orchestrator mode with observe" table
- **After**: Node list, text graph (in a code fence), sharing check, ten-row order table (steps 0 to 9), cross-issue edit order
- **Provenance tag**: `<!-- Source: Variant 5 (round2-rebuttal-V5.md, Section 5.9) ... corrected by invariant rows ... - merged per Change #12 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 13: Part 5 invariant probe
- **Status**: Applied
- **Source**: `invariant-probe.md`, all 44 rows
- **Target**: Part 5 (insert)
- **Before**: Section did not exist
- **After**: 5.1 table of 16 HIGH and MEDIUM unaddressed rows (1 HIGH, 15 MEDIUM); 5.2 INV-012 carry-forward, four ADDRESSED-with-residual rows, 12 LOW unaddressed one-liners, 11 no-action rows; 5.3 the unresolved list
- **Provenance tag**: `<!-- Source: invariant-probe.md ... - merged per Change #13 -->` on 5.0, 5.1, 5.2; 5.3 also per Change #20
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 14: Part 6.1 #409 body corrections
- **Status**: Applied
- **Source**: `variant-5-original.md` lines 176 to 204 (BC-01 to BC-23); R2-V5 rows 9 and 13; R2-V1 A-011; V1 C-07, C-25, C-34, W-7; V2 W-05(a), W-06; V4 edit 1
- **Target**: Part 6.1 (insert)
- **Before**: V5 table of 23 rows
- **After**: The 23-row table carried verbatim (copied line for line from the source, lines 180 to 204); disposition table (post as written / reword / extend / keep and add / replace / post last); proposed text for BC-12, BC-15, BC-16 written as the plan directs and marked PLAN INFERENCE; additions from V1, V2, V4; order inside the pass; paste-ready statement
- **Deviation from plan wording, per the lead's instruction**: the plan says the BC wording is "referenced, not retyped". The lead asked for exact wording to be carried verbatim and the merged output to be self-sufficient, so the table is carried verbatim, with a warning that the "Replace with" cells of BC-12, BC-15, BC-16, BC-17 are superseded
- **Provenance tag**: `<!-- Source: Variant 5 (variant-5-original.md, "Corrections to the #409 body (exact wording)", lines 176 to 204), carried verbatim ...; dispositions modified by the debate ... - merged per Change #14 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (two carried-wording tensions neutralised by a MERGE-EXECUTOR NOTE, see Contradiction Re-Scan)

### Change 15: Part 6.2 proposed edits to #450
- **Status**: Applied
- **Source**: V2 "Proposed edits to #450" 1 to 5 (lines 61 to 65); R2-V2 sections 1, 5.1, 5.4, 5.6
- **Target**: Part 6.2 (insert)
- **Before**: V2 list of five edits
- **After**: The five edits carried verbatim; disposition table (keep / extend / reword; paste-ready column); note that edits 2 and 4 are independent. A MERGE-EXECUTOR NOTE says V2's "Owner question Q1" is this document's Q2
- **Provenance tag**: `<!-- Source: Variant 2 (variant-2-original.md, "Proposed edits to #450", lines 59 to 67, carried verbatim) ... - merged per Change #15 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 16: Part 6.3 Coder#477 rewrites
- **Status**: Applied
- **Source**: `round2-rebuttal-V3.md` section 5.6 (lines 122 to 172) and section 5.7 (lines 176 to 184)
- **Target**: Part 6.3 (insert)
- **Before**: Section did not exist
- **After**: Recommendation and paste-ready statement (plan wording), then the full texts A (narrow), B (keep), C (close) and the nine-item checklist carried verbatim. Deviation from the plan's "reference, do not retype", same reason as Change 14. A MERGE-EXECUTOR NOTE maps R2-V3's D-1, D-2 to Q3, Q4 and separates R2-V3 D-7 from R2-V5 D-7
- **Provenance tag**: `<!-- Source: Variant 3 (round2-rebuttal-V3.md, Section 5.6 lines 122 to 172 and Section 5.7 lines 176 to 184, carried verbatim) - merged per Change #16 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 17: Part 6.4 #423 rewrite and #339 comment
- **Status**: Applied
- **Source**: `round2-rebuttal-V4.md` section 5.7 (lines 136 to 209)
- **Target**: Part 6.4 (insert)
- **Before**: Section did not exist
- **After**: The five clause dependencies, the PLAN INFERENCE sentence for the #339 comment (INV-021), paste-ready statement, then the full #423 title, body and #339 comment carried verbatim (inside the source's four-backtick fences, so none of its headings enter the document outline). The source's own `### 5.7` heading line (line 134) was left out to keep the heading hierarchy intact
- **Provenance tag**: `<!-- Source: Variant 4 (round2-rebuttal-V4.md, Section 5.7 lines 136 to 209, carried verbatim), with the clause dependencies and the numbering sentence from invariant row INV-021 - merged per Change #17 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 18: Part 7 deduplicated owner questions
- **Status**: Applied
- **Source**: V5 questions 1 to 10, V2 Q1 to Q4, R2 D-lists, INV-003, 004, 014, 023, 030
- **Target**: Part 7 (insert; replaces V5's question list)
- **Before**: V5 ten questions
- **After**: 24 questions in one table (Q, question, recommended answer, gates, sources deduplicated), "default (no debate verdict)" labels on Q1, Q6 and Q23, and a short note on what the first four answers do
- **Provenance tag**: `<!-- Source: Base (original, modified) - V5 "Questions only the owner can answer" ... replaced by the deduplicated set ... - merged per Change #18 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 19: Part 8 changes not being made
- **Status**: Applied
- **Source**: R2 concessions, X-004, X-013, X-017, A-012, X-005, INV-008
- **Target**: Part 8 (insert, 16 rows)
- **Before**: Section did not exist
- **After**: The plan's "Changes NOT Being Made" table; the bare "(D-7)" was qualified as "R2-V5 D-7" to avoid a clash with R2-V3's D-7
- **Provenance tag**: `<!-- Source: refactor-plan.md "Changes NOT Being Made" table ... - merged per Change #19 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 20: Carry the status and unresolved items into the header and return contract
- **Status**: Applied
- **Source**: `debate-transcript.md` lines 1843 to 1849; invariant-probe Summary
- **Target**: Merged output status block, Part 0.1, Part 0.2, Part 5.3; return-contract fields below
- **Before**: Section did not exist
- **After**: BLOCKED_BY_INVARIANTS at the very top; INV-008, A-009, X-016 each labelled UNRESOLVED in 0.2, 5.3 and their register rows ("UNRESOLVED" appears on 14 lines). Return-contract fields for the lead: `status: BLOCKED_BY_INVARIANTS`; `convergence: 100% on 36 of 36 X and A points (63.9% before Round 2); taxonomy covered; invariant gate not passed`; `unresolved: INV-008 (no fix specified, owner ruling pending); A-009 (Orca build divergence); X-016 (consumption on a live coordinator Run unproven both ways)`; `base: Variant 5 (0.915; V2 0.893; tiebreaker V5 18 of 36 matrix points)`
- **Provenance tag**: `<!-- Source: Base (original, modified) - restructured ...; status block carried per Change #20 -->`; Part 0 and Part 5.3 tags
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 21: Provenance tags and citation pins
- **Status**: Applied
- **Source**: `artifact-templates.md` Section 6; SKILL.md T05.04
- **Target**: Every block of the merged output
- **Before**: n/a
- **After**: Header comments (`Provenance: This document was produced by /sc:adversarial`, `Base: Variant 5 ...`, `Merge date: 2026-11-13T18:50:58Z` from `date -u`); 34 `<!-- Source: ... -->` tags, one per section or significant block, each naming base, variant and section, and the change number; modified base blocks carry the reason. Every section heading from Part 0 to Appendix A has a tag in its first block. Citations keep the form used in their source (path:line, `#N`, sha, `updatedAt`). The plan's "one Source id per row" for the point register is met at table level: each of the six tables carries a tag naming its matrix rows, and every row's id is its matrix id
- **Provenance tag**: the header block itself
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 22: Plain-English and gloss pass over the base
- **Status**: Applied
- **Source**: re-evaluation standards table (V5 L4 NOT MET)
- **Target**: Part 0.3 (glossary) and the whole output
- **Before**: V5 used TUIBBS, QUESTION-OBSERVATION, WC-16 and similar names undefined
- **After**: A glossary (Part 0.3) defines the five reviews, every id family (R1/R2, X, A, S, C, U, SC, INV, the per-review item ids, O, RT-F, S1 to S10, D1 to D9, D-n, BC, E, Q, PLAN INFERENCE, UNVERIFIED) and every coined name (Orca terms, observer, sweep, watcher, WC-16, WC-12, WC-13, NFR-001, NFR-014, FU-1, AC-S, Q-1 to Q-3, QUESTION-OBSERVATION, QUESTION-LINK, guard and flip, OB-H1 to OB-H3, TUIBBS, R1 to R4, the design names, #534, the two "v1" JSON files, join key, consume). Glosses come from the plan, WORKER-CONTRACT.md (WC-12 and WC-13 checked there) and the debate files. A search for em dashes and en dashes in the output found 0. No term was left undefined, so no "UNVERIFIED meaning" entry was needed
- **Provenance tag**: `<!-- Source: Base (original, modified) - header block per Change #20; glossary per Change #22 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## Post-Merge Validation

Method: heading outline extracted with awk (fenced blocks excluded), references extracted with grep and checked against the headings and id ranges, dashes and placeholders searched with grep, counts compared with the plan. The long verbatim blocks (BC table, #450 edits, Coder#477 and #423 rewrites, the two R2-V5 tables) were copied mechanically with `sed -n` line ranges from the source files into the output, and the first and last line of each range were spot-checked against the source.

### Structural Integrity
- Heading hierarchy: PASS. One H1; H2 for Part 0 to Part 8 and Appendix A (10); H3 for 0.1 to 0.4, 1.1 to 1.3, 2.1 to 2.7, 3.1 to 3.6, 4.1 to 4.2, 5.1 to 5.3, 6.1 to 6.4. No level gap, no H3 without an H2 parent, document starts with an H1. The verbatim source blocks that contain their own headings sit inside four-backtick code fences (Part 6.4) or had the heading line left out (Part 6.3 and 6.4), so none adds a heading to the outline.
- Section ordering: PASS. The glossary (Part 0.3) comes before the first use of the ids; the verdict (Part 1) before the systems (Part 2); the point register (Part 3) after the narrative; dependencies (Part 4) after both; paste-ready texts (Part 6) after the questions they depend on are defined in Part 7 (Part 6 refers forward to Part 7, as Part 1.1 and Part 2 do; every such reference resolves).
- Document flow: PASS. Status block, then glossary, then verdict, then per-system actions, then the register, order, probe, texts, questions, rejected proposals, appendix. Status BLOCKED_BY_INVARIANTS is visible in the first screen.
- Placeholders: PASS. No `FILL:` or `<<VERB` marker remains. No em dash or en dash remains (0 found).
- Provenance: PASS. 34 `<!-- Source: ... -->` tags plus the three header comments; every H2 or H3 section from Part 0 to Appendix A has a tag in its first block.

### Internal References
- Total references: 462 (Part and section references 105; "action N" references 25; "Part 4 step N" references 8; owner-question ids Q1 to Q24 253; fact ids E-01 to E-18 28; correction ids BC-01 to BC-23 43)
- Resolved: 462
- Broken: 0
- Also checked: every INV id used is between INV-001 and INV-044; Part 5.1 has 16 rows (1 HIGH, 15 MEDIUM) and Part 5.2 lists the 12 LOW unaddressed, 4 addressed-with-residual and 11 no-action rows (44 findings accounted for with INV-008 and INV-012 counted in Part 5.1 and the carry-forward); the register has 36 rows (12 + 6 + 9 + 3 + 2 + 4); Part 6.1 has 23 BC rows; Part 7 has 24 question rows; Part 1.3 has 19 rows and Part 8 has 16 rows.
- Two plan-internal reference errors were found and corrected while applying the plan (listed under Change 4 and Change 6): the routing row is Part 4 step 5, not step 6; Q12 and Q13 were missing from the owner-question lists of Part 2.1 and Part 2.3.

### Contradiction Re-Scan
- New contradictions introduced: 0 left unresolved. Eight tensions between carried text and the document's own rules were found and neutralised in the output (none is a contradiction in the document's own claims once the note is read):
  1. V5's BC-13 text says "JSON v1" with no name, against the naming rule A-014 and the Part 2.3 "do not call either JSON the JSON v1". A MERGE-EXECUTOR NOTE in Part 6.1 says to write "sweep report JSON v1" and "observe snapshot v1" when re-pinning.
  2. V5's BC-16 text says "joined on dispatch id", against the rule that nothing is a "join key" before the one real-id comparison (D-3). Same note: provisional until the comparison.
  3. The "Replace with" cells of BC-12, BC-15, BC-16 and BC-17 as V5 wrote them differ from the debate's dispositions. A warning sentence before the verbatim table says those four cells are superseded, and the proposed text follows the table.
  4. V2's edit 1 says "Owner question Q1" (V2's own question 1); in this document Q1 is the security thread and the claim-level question is Q2. Note added in Part 6.2.
  5. R2-V3's text uses D-1, D-2, D-7 (its own numbering); R2-V5 also has a D-7 with another meaning. Note added in Part 6.3, glossary rule added in Part 0.3, and the other unqualified D-7 mentions were qualified (Part 1.2, Part 5.3, Part 6.3, Part 8).
  6. R2-V4's #423 body says the claim at its default level also launches a second governed agent, while the recommended Q2 answer is `--pipeline none`. This is a dependency the plan names; Part 6.4 flags it as clause (2) to change if Q2 = `--pipeline none`.
  7. Single Round 2 files give different confidence figures from the matrix for A-009 (65 against 67), X-006 (75 against 74), A-005 (88 against 85) and A-011 (93 against 92). The matrix figure is used everywhere and the figure is the same in every part where the point appears (A-009: Part 0.2, 3.3, 5.3).
  8. The Round 2 files say "merge #541, then #539 after a CI re-run"; INV-037 shows a re-run keeps the old merge ref. The re-run remedy appears only as a rejected finding (Part 1.3, Part 8); Part 2.2 action 4 and Part 4 step 2 say "push or update the branch".
- Cross-part consistency checks that passed: INV-008 is "UNRESOLVED", first, blocking and "at least 18 of 29 worktrees" in Parts 0, 2.2, 4, 5, 8; the recommended answers in Part 2 match Part 3 and Part 7 (Q1 about 70 percent labelled default; Q2 `--pipeline none`; Q3 narrow about 65 percent; Q4 observer 70 to 75 percent; Q5 keep both; Q16 one vocabulary); X-016 is 61% and "unproven both ways" in Parts 0, 3.1, 5.3, 8; the PR #539 head `873599d59`, six threads, two unresolved, and PR #503 and #514 dates agree across Parts 1.2, 2.2 and 4.
- Pre-merge contradiction list: the X-001 to X-020 points of `diff-analysis.md` are each stated once as a verdict in Part 3 and are not restated differently elsewhere.

## Summary

- Total changes planned: 22
- Successfully applied: 22
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (structure, 462 of 462 references resolved, 0 unresolved new contradictions)
- Debate status carried, not changed by the merge: BLOCKED_BY_INVARIANTS (INV-008 unresolved; A-009 and X-016 unresolved)

Items the lead should know (none blocks the merge):
1. Deviation from plan wording, on the lead's instruction: Changes 14, 16 and 17 say "reference, do not retype"; the exact BC table, the Coder#477 texts A, B, C and the #423 rewrite with its #339 comment are carried verbatim so the output is self-sufficient and paste-ready.
2. Plan errors corrected: routing row is Part 4 step 5 (plan text said 6 in Part 2.1); Q12 and Q13 added to the Part 2.1 and Part 2.3 question lists. The plan's Final Structure says every Part 2 action uses the eight point fields; the output gives each action a short bracket (decision, waits for and unblocks, undo) and keeps verdict, confidence and evidence in Part 3, as stated in Part 0.4.
3. Text written by the merge and marked PLAN INFERENCE (10 uses of the label in the output): the Q1 "about 70 percent" default, the proposed wording for BC-12, BC-15 and BC-16, the INV-021 sentence for the #339 comment, and the plan's own additions in Part 2.3 and Part 2.6. The owner confirms them before anything is posted.
4. Not verified by the merge: no source was re-checked against GitHub, Orca or the repository; every "verified now" claim is the debate's, with the source it named (Appendix A).
5. Nothing was posted or changed outside the two output files.
