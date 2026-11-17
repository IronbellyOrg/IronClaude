# Merge Execution Log

## Metadata
- Base: Variant A (Proposal A, Sweep-Sheet-shaped; `variant-1-original.md`)
- Executor: merge-executor agent (Step 5, merge execution, of the adversarial pipeline)
- Plan: `refactor-plan.md` (15 planned changes, auto-approved 2026-11-14)
- Output: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/reviews/adversarial/process-redesign-modules/merged-output.md`
- Changes applied: 15 of 15 planned
- Status: success
- Timestamp: 2026-11-14

Notes on method. The merged file is the resolution of slot X-13 as the debate produced it. Every changed or added statement was taken from the plan, `round2-advocate-A.md` (R2A), `round2-advocate-B.md` (R2B), the scoring matrix in `debate-transcript.md` (DT), `invariant-probe.md` (IP) or, where the plan names them, `variant-2-original.md` (VB). The executor re-read no repository code: each code citation is carried with the tag its source file gave it, and the advocate who read or measured it is named. Round 2 tags were kept ([VERIFIED], [MY-MEASUREMENT], [MY-ARITHMETIC]) and not relabelled. The two paths the task forbids were not read, listed, searched or cited; a search of the merged file for them returned no match.

## Changes Applied

### Change 1: Position becomes the converged hybrid
- **Status**: Applied
- **Source**: R2A section 0 and section 5; R2B section 0 and section 6; DT "Points on which the two advocates agree after Round 2" and scoring matrix (13 Hybrid points)
- **Target**: Base section 1 (replaced); merged section 1. The title, status block, code-state line, sources line and tag legend at the top of the file were adjusted at the same time so the file reads as the resolution and not as Proposal A alone.
- **Before**: One paragraph: "script-first and advisory-only"; scripts build typed pre-pass items; sidecar and `coverage_rows` as the only container and link; cards as module data; CB-2 not adopted; extractors decided class by class; "degrades, by construction" to "the core absorbs only the reusable pieces".
- **After**: Opening claim kept (cards are module data; extractors decided per class behind an offline gate with no model tokens). Replaced by five bullets: record-only row block as built-now carrier, entry point, card loader, binding and lint; extractors reserved; advisory-only checks with demotion and promotion not built (reserved behind G-4); sidecar stays the only container, `observed` computed from parsed rows, writer split open; tool wall by lint. CB-2 outside the core kept. The "degrades by construction" wording is replaced by "the leftover is the carrier plus rowcheck, which can be measured" (A withdrew the loader-plus-card-text value claim, R2A section 2 weakness 4). Open points listed.
- **Provenance tag**: `<!-- Source: Base (original, modified) — section 1 replaced per Change 1 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK (no remaining "script-first" claim; the only match is inside the provenance comment)

### Change 2: Core inventory replaced
- **Status**: Applied
- **Source**: R2A section 5 items 1 to 7; R2B section 6 components 1 to 7; VB section 3 items 4, 5, 7
- **Target**: Base section 2 "Adds only" and "Does not add" bullets, the "Item answers travel through what exists" bullet and the "Telemetry" bullet; merged section 2 (bullets "Built now", "Reserved", "Not added")
- **Before**: "Adds only (a) loader, (b) one entry point that runs extractors and writes the per-reviewer sheet and sidecar `assigned`, (c) additive advisory flags in `precheck.json`"; "Does not add: a per-row verdict block, demotion, promotion, ..."; item answers via `coverage_rows` or an open key; telemetry counts and ids.
- **After**: Built now, items 1 to 7 (card format with the R2B component 1 field list and no `extractor` field; row block; one entry point; check rules; counts-only telemetry with leak test; uniform per-module binding; tool-wall lint). Reserved, items 8 to 11 (slot-keyed binding; extractors; `ran` cross-check; demotion and promotion with D-3 recorded as closed). Not added: demotion, promotion, overlay, profile value, slot key, precheck flags, CB-2 in core, per-row consequence, lens-to-model binding, class constants, reviewer shell, changes to findings v1 and v2, `review-ledger/1`, `derive_verdict`, reflect 1.8.0 and its 36-test matrix. "A per-row verdict block" is removed from the excluded list with a note. The "Keeps and reuses" bullet is kept, with the three-id-space sentence added.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Section 3 items 1, 4, 5, 7 and Section 5, with R2A section 5 ... — merged per Change 2 -->` and a base-modified tag on "Keeps and reuses"
- **Validation**: Structural integrity OK | References OK | Contradictions OK (no remaining precheck-flag item in the inventory; "a per-row verdict block" appears only in the removal note)

### Change 3: Row block specification
- **Status**: Applied
- **Source**: R2B section 6 component 2, section 4.1 (iii); R2A section 5 item 3, section 3 point 11, section 8 items 1 and 6; DT scoring matrix C-002, C-006, X-007; IP INV-006 to INV-010, INV-014
- **Target**: new subsection 2.1
- **Before**: Section did not exist (base had no per-row carrier).
- **After**: `rows-v1` record-only fence with fields; limits labelled as Variant B's Round 2 proposal (A neither accepted nor rejected; IP INV-009 and INV-010 open); placement before the findings block in v1 (`:33`, `:58`) and after it in v2 (`reviewer-spec.md:39`, `SKILL.md:344`, `findings.py:73`); truncated row block never invalidates a complete findings block; `observed` computed from parsed rows and never orchestrator-declared; hard consequence only for the empty findings block (`findings_v2.py:291-298`), one finding plus zero rows valid, so the row block does not prove examination; D-6 and INV-006, INV-007, INV-010, INV-014 stated as open gaps.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Section 3 item 4; R2B section 6 component 2 ... — merged per Change 3 -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 4: Single writer entry point and id map
- **Status**: Applied
- **Source**: R2B section 6 component 3, section 4.2 row "2"; R2A section 5 item 2, section 3 point 6, section 8 item 7; IP INV-001 to INV-005
- **Target**: new subsection 2.2
- **Before**: Section did not exist.
- **After**: One CLI entry point with two outputs (`panel/coverage.json` with `assigned`, one entry per card including `{}`, and the id map; `panel/rowcheck.json`, `review-rowcheck/1`, advisory only). Both Round 2 lists recorded: A's component 2 "fills `assigned` only" (tagged Agreement) and B's AMEND that also computes `observed` from the parsed rows (comboC-r3, comboA-r3, comboA-r2 numbers, [MY-MEASUREMENT, advocate B]); A did not accept the amendment; no Round 3. Agreed: `observed` is not orchestrator-declared. The writer split is stated as open. INV-001 (HIGH, UNADDRESSED), INV-002, INV-004, INV-005 open; INV-003 addressed.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Section 3 items 4 and 5; R2B section 6 component 3 ... — merged per Change 4. The writer split is recorded as open, not resolved -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 5: Check rules and snapshot boundary
- **Status**: Applied
- **Source**: R2B section 6 component 4; R2A section 5 item 4; DT A-004; R2A section 3 point 8, R2B section 2 item d; R2A section 2 weakness 5
- **Target**: Base section 3.3, bullets 1 and 2 (merged 3.3; heading renamed "Why advisory-only holds, and how the quote check is bounded")
- **Before**: Bullet 1 called `ledger.py:3-4` the code's own rule for "no component edits a reviewer finding". Bullet 2: `_check` reused unchanged; 472 of 510 tagged "not re-run by me"; script evidence must be in the snapshot or `verify-citations` flags it.
- **After**: Bullet 1 states both advocates agree `ledger.py:3-4` is a status rule and `verify_cmd.py:10-12` governs the precheck only; surviving grounds `ledger.py:210-213`, `SKILL.md:343`, C-02, C-03 fail-closed; GQ-130 answer and X-002 and X-003 scores kept. Bullet 2 now says `_check` reaches only findings-v2 citations, row quotes are checked in the separate rowcheck file, A's part (c) is withdrawn, and the 472 of 510 counts are "re-run by both advocates" with A's jq counts; rules for `quote_plan`, `quote_other`, `check_skipped`, snapshot-restricted script evidence, advisory only.
- **Provenance tag**: `<!-- Source: Base (original, modified) — bullet 1 revised ... per Change 5 -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 6: Binding (uniform per module; slot-keyed binding reserved)
- **Status**: Applied
- **Source**: R2A section 5 items 6 and 8; R2B section 4.1 (ii); DT X-005 (Hybrid 63 percent), C-013 (Neither 65 percent)
- **Target**: Base section 3.2 last sentences, section 2 (item 6), and a new short paragraph in 3.2
- **Before**: "Position A needs no lens-to-reviewer binding, because the script assigns items per reviewer and the sidecar already keys by `reviewer-<N>`."
- **After**: Uniform per-module binding (loop same-brief sentence `:70` holds, `_SLOT_KEYS` unchanged); sidecar key is the card stem, `reviewer-<N>` for v2 only, three id spaces (F3); GQ-131 answer kept; reflect already breaks "same brief" by design. New paragraph: slot-keyed binding reserved in this document only, name other than `recipes`, golden resolve-output test, `review-panel/1` hash decision, slot-to-card-stem map, `SKILL.md:340`.
- **Provenance tag**: `<!-- Source: Base (original, modified) — heading and the closing sentences adjusted per Changes 6 and 7 ... -->` and `<!-- Source: Variant A and Variant B Round 2 text ... — merged per Change 6 -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK (no remaining per-reviewer or replica assignment; remaining "replica" matches are in a negation note and provenance comments)

### Change 7: Tool wall and card format
- **Status**: Applied
- **Source**: R2A section 5 item 7; R2B section 6 components 1 and 7; VB section 3 item 1 and E10; DT X-004, C-003
- **Target**: Base section 3.2 (new paragraph "Tool wall"); card fields in section 2 item 1
- **Before**: A's tool-wall bullets only (recipes need a shell, reviewer has none; A ran shell searches in a script).
- **After**: No card may require a tool outside the bound agent's allowlist (`reflect-reviewer.md:5, :8`); a test fails otherwise; a class whose only form needs a shell is not bound to a read-only agent; C4 and C8 script extractors reserved; for a read-only slot C4 keeps only a Grep form, equivalence to the shell dialect [UNVERIFIED] (Grep is ripgrep); `ran` unverified until C-08.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Section 5 INV-G and Section 6 T-B5; R2A section 5 item 7 ... — merged per Change 7 -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 8: Evidence section additions
- **Status**: Applied
- **Source**: VB section 4 rows E7, E8, E9, E12 (table form, S-002 and S-003 won by B); R2A section 3 points 1 to 11; R2B section 2 items a to g; IP "Facts the advocates marked [UNVERIFIED] that this probe verified" (in `round2.5-fault-finder-raw.md`)
- **Target**: Base section 3, new 3.7 "Facts established in the debate"
- **Before**: Section did not exist.
- **After**: Table F1 to F14 with claim, evidence and tag: empty-block-only consequence (E7); v1 loop has no snapshot, sidecar, cluster or precheck step; three id spaces plus a fourth `-card` stem and the missing-entry asymmetry; `_brief_ids` and re-find recompute; quote exactness (A's 31/568 = 5.5 percent [MY-ARITHMETIC]; B's 31/313 = 9.9 percent and 18.8 percent for two quotes, which assumes independence that B says is low; failures in 8 of 29 runs, 2 to 57 percent in those 8; transfer to row quotes stated as an assumption); `ledger.py:3-4` status rule and `ledger.py:467-474`; `recipes` collision; no merge hook; placement and brief constraints; recorded sidecars (E8); blocking-versus-severity by engine; INV-N mirror pins excluding `commands/spec-panel.md`; rf-qa marks (E12); orchestrator-only `observed`. E9 (472 of 510) is carried in 3.3 with the "re-run by both advocates" tag.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Section 4 rows E7, E8, E9 and E12 in table form ... — merged per Change 8 -->`
- **Validation**: Structural integrity OK | References OK (F1 to F14 all defined and all referenced ones resolve) | Contradictions OK
- **Note recorded, not resolved**: the two advocates name different runs for the two all-empty sidecars (A: `shadow07`, `shadow15`; B: the `analyzeCodegraph` and `renameTheScIssue` runs) while agreeing on the counts. F10 states this as unreconciled. Advocate A's 8-file token count and advocate B's 2-markdown-file count for the v1 loop absence differ in scope only; F2 gives both. Advocate A's sentence on where `review panel resolve|review merge` appear lists `commands/spec-panel.md` and says in the same sentence it has no match inside it; F2 records this.

### Change 9: Invariants section extended
- **Status**: Applied
- **Source**: VB section 5 (Preserved and Endangered, kept where the debate did not contradict them); IP summary and table
- **Target**: Base section 4 (extended and revised) and new 4.1 table of the 20 probe findings
- **Before**: Preserved list (contract 1.8.0, 36 tests, finding grammar, INV-G, INV-H, repository rules) and Endangered list (precheck byte-identity, snapshot boundary, determinism, second source of false positives, class constants).
- **After**: Preserved kept and revised (no-cards byte identity; INV-013 residual; D-7 and INV-016 cautions; row block separate fence, IP INV-018; INV-G conditional on the lint; INV-H with INV-017 gap; INV-J and INV-L from VB; VB's claim that INV-N holds because "the brief file is untouched" not carried over, because v1 wiring edits a primitive, F12 and INV-015). Endangered revised (precheck flags withdrawn so byte-identity is held by the second file; snapshot boundary; determinism for reserved extractors; row duty and D-1; class constants; v1 weaker check; run-artifact text; the 16 UNADDRESSED findings by ID and severity). 4.1 copies ID, Category, Status, Severity unchanged from IP with a shortened assumption column, totals and the gate result.
- **Provenance tag**: `<!-- Source: Base (original, modified) — section 4 "Preserved" kept and revised ... — per Changes 9 and 11 -->` and `<!-- Source: Invariant probe (IP) table ... — merged per Change 9 -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK (counts re-checked: 20 findings, 4 ADDRESSED, 16 UNADDRESSED = 2 HIGH + 13 MEDIUM + 1 LOW)

### Change 10: Measurement section replaced with ordered gates
- **Status**: Applied
- **Source**: R2A section 5 items 13 to 17; R2B section 6 items 13 to 17 and section 4.2; DT C-007 (Hybrid 75 percent), X-008 (A conditional 55 percent); VB section 6 (M-B1, M-B2, M-B3)
- **Target**: Base section 5 (replaced; merged section 5)
- **Before**: M1 offline per class; M2 shadow mode; M3 against arm K; M4 precision and non-regression; M5 invariants.
- **After**: G-0 code tests (R2A item 13 plus R2B additions: writer duplicate and range rules, `observed` only from parsed rows, id map, normaliser equality, truncated row fence; T-B1 recast as a golden test of the resolution output plus a pin of the loop prompt file because no brief renderer exists). G-1 per class (A's M1 kept; measures selection recall only). G-2 compliance spike. G-3 arms Z0, K, RL, SS (RL must beat K by the pre-registered margin or K wins; SS only for classes that passed G-1). G-4 demotion safety with the three prerequisites (`ledger.py:99-104, 210-218`; `merge_cmd.py:71`; `findings_v2.py:161-162`). Gate order as agreed. A's M2 and M4 (with B's M-B2 limits) kept under G-3, M3 as the K arm of G-3, M5 under G-0; the placement note states this is the merge's placement and not a debate conclusion. The base closing paragraph's equivalence of the leftover to synth-05's "absorb the reusable pieces" option is not carried over (A withdrew the value claim).
- **Provenance tag**: `<!-- Source: Base (original, modified) — section 5 replaced per Change 10 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 11: Consistency with C-01, C-02, C-03 kept and updated
- **Status**: Applied
- **Source**: VA section 6; VB section 2 (content only; table format not adopted because S-004 is unresolved); IP INV-018, INV-011
- **Target**: Base section 6 (merged section 6), plus the conflicting lines elsewhere: the precheck-flag references in base section 2 "Adds only (c)" (Change 2), section 3.3 (Change 5) and the section 4 "Endangered" precheck byte-identity bullet (Change 9); base section 6 lines on item link through `coverage_rows` or an open key (revised to the row block) and on replica assignment (replaced by uniform binding)
- **Before**: Item answers through `coverage_rows`/`probe`; "a sheet is a first-review mechanism"; "no block named ledger ... a per-row carrier later needs a different noun"; replica assignment is a module rule and does not feed the C-03 floor.
- **After**: Labelled prose kept with a statement that S-004 is open. C-01: separate fence in both engines, link key `coverage_rows` (v2) or open key (v1), residual truncation path INV-011; the `class` and `src` example keys of the base are dropped because `class` is now a row field and promotion (`src`) is not built. C-02: first-review only (`apply_to: ["first"]`), `rows-v1` noun, `block_ok` only through the empty-block rule. C-03: union input unchanged; the interaction Proposal B flagged is stated as not engaged, tagged as the merge's inference and not a debate conclusion; uniform binding "a module rule, not a quorum" kept, with the empty-block route to the floor recorded as open (INV-011); INV-007 note kept.
- **Provenance tag**: `<!-- Source: Base (original, modified) — section 6 kept and updated per Change 11 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 12: Modules
- **Status**: Applied
- **Source**: R2A section 5 items 18 to 21; R2B section 6 items 18 to 21 and section 4.2; DT C-005 (Hybrid 60), C-011 (Hybrid 55), C-012 (B 60)
- **Target**: Base section 2 "Modules" (merged 2.3; heading "2.3" added for structure only) and base section 7
- **Before**: Tasklist review with all eight classes and first extractors C4, C8; spec review E1, E2, E5, E7 on v1; reflect reusing Wave 1B for C2; PR review and rf-qa extractors E3 and E4 in the script.
- **After**: Spec loop (v1): uniform cards, row block before the findings block, advisory rowcheck on `quote_plan` against the candidate, `quote_other` check_skipped, no consequence, wired in prose only after G-2 and G-3 per B and as one prose edit per A; D-5 unresolved; mirror pins (F12, INV-015). Tasklist and workflow via reflect UC-1 (v2): items are the Coverage slice rows, class-row ids namespaced, row block after the findings block, verbatim copy into the panel card by a prose edit of reflect step 5, D-7 unresolved, IP INV-002 and INV-016. Reflect default and UC-2: no cards, byte-identical. PR review and rf-qa: reserved; reverse-dependency and whole-tree searches run in a script for untrusted diffs; OK, UNSURE, missing to `[x]`, `[?]`, `[ ]` stated as a design inference, not a tested equivalence. Section 7 revised consistently (extractor cost, "no per-row proof" sentence, Proposal B Section 7 content).
- **Provenance tag**: `<!-- Source: Base (original, modified) — "Modules" group of the base replaced per Change 12 ... -->` and `<!-- Source: Base (original, modified) — section 7 revised per Change 12 ... -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 13: Strongest objection and answer rewritten
- **Status**: Applied
- **Source**: VA section 8; VB section 8; R2A section 2; R2B section 3
- **Target**: Base section 8 (merged section 8)
- **Before**: A's objection with five answers (build size, selection recall, lister-only classes, second source of false positives, unobservable compliance).
- **After**: A's objection kept. A's answers kept where they survived and revised where Round 2 conceded them (no extractor built now; G-1 needs extractors and ground truth that do not exist; `observed` as a declaration conceded hollow). B's objection recorded and answered by the agreement that demotion and promotion are not built, with the three added grounds (`ledger.py:99-104, 210-218`; no merge hook at `merge_cmd.py:71`; 9.9 percent per quote against B's planning figure). The second per-reviewer duty is stated as remaining (D-1). Concessions recorded for A (hollow mechanism, no v1 host, flags withdrawn) and B (no brief renderer, overlay needs a merge hook, `recipes` collision, card-stem key, `ledger.py:468` cite).
- **Provenance tag**: `<!-- Source: Base (original, modified) — Proposal A's objection kept ... — per Change 13 -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 14: Conditions and non-claims
- **Status**: Applied
- **Source**: VB section 9 (S-003, B 60 percent); IP INV-019, INV-020; DT metadata
- **Target**: new section 9, placed before the appendix ("final-but-one")
- **Before**: Section did not exist.
- **After**: No claim that RL beats SS or K; no effect size from planning values; D2 (0.12 x 14 = 1.68 items) exceeds both central estimates and is a pre-registration choice for the owner (3.6; GQ-135 is cited only for the related +35 percent elapsed limit, as the plan-review correction requires); A-001 precondition; built-now set dormant (INV-019, HIGH, UNADDRESSED); hard consequence only for the empty report and `observed` proves a typed id, `ran` unverified until C-08; value of the advisory output depends on a named reader of `rows_missing` and the PROBLEM-without-finding list (INV-020); the agreement is conditional on the open points.
- **Provenance tag**: `<!-- Source: Variant B (Proposal B), Section 9 ...; IP INV-019 and INV-020; DT metadata — merged per Change 14 -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK

### Change 15: Resolution table and open points
- **Status**: Applied
- **Source**: DT scoring matrix and convergence assessment; IP; R2A section 6; R2B section 7
- **Target**: new Appendix A
- **Before**: Section did not exist.
- **After**: A.1 the 29-point table (point, level, winner, confidence) with the DT tally. A.2 open points: S-004 (unresolved; labelled-prose format kept), D-1, D-2, D-5, D-6, D-7 each with the evidence the advocates said would settle it (D-5 with both advocates' readings), the A-versus-B split on who computes `observed`, D-3 and D-4 recorded as closed by agreement. A.3 convergence 96.55 percent (28 of 29), status BLOCKED_BY_INVARIANTS because of INV-001 and INV-019, the 16 UNADDRESSED invariants by ID and severity.
- **Provenance tag**: `<!-- Source: Variant A and Variant B Round 2 text and the DT scoring matrix; IP — new appendix per Change 15 -->`
- **Validation**: Structural integrity OK | References OK | Contradictions OK (point count 29; tally 5 + 4 + 13 + 6 + 1 = 29)

## Changes NOT Being Made (confirmed against the merged file)

All nine rows of the plan's table were respected. The merged file does not contain: demotion, promotion, an overlay or a `rowcheck` profile value as built behaviour (X-002, X-003; reserved in the document only behind G-4); a `recipes` slot key (X-005; `recipes` appears only as the excluded name); a CB-2 route through the row block (C-010, X-006); additive precheck flags (C-004; stated as withdrawn); built extractors (X-001, C-009; reserved); an `extractor` field on the card (C-003); an orchestrator-supplied `observed` or "existing mechanism" for a no-finding item (C-002); T-B1 as golden rendered briefs (C-007); the loader-plus-card-text fallback as having value (C-008).

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: OK. One H1; ten H2 (sections 1 to 9 and Appendix A); fourteen H3 (2.1, 2.2, 2.3, 3.1 to 3.7, 4.1, A.1, A.2, A.3); no H4; no gap and no orphan. The base's plain-line subsection labels 3.1 to 3.6 were converted to H3 headings and "2.3" was added over the base's "Modules" group, so every numbered subsection is a heading.
- Section ordering: OK. Sections 1 to 8 keep Proposal A's order; section 9 (conditions and non-claims) is the final-but-one section; Appendix A is last.
- Document flow: OK. Header comments are the three Section 6 lines (Provenance, Base: Variant A (Proposal A), Merge date 2026-11-14). 25 `<!-- Source: ... -->` tags cover the title block, every section, every subsection group and the two inserted tables. No placeholder or draft sentinel remains (searched for TODO, TBD, placeholder markers and the working sentinel). `Status: Complete` appears at the top and bottom, as in the base.

### Internal References
- Total references: 352 (mechanical counts by pattern: F1 to F14, 38; G-0 to G-4, 73; D-1 to D-7, 36; INV-001 to INV-020, 121, of which 20 are the ID cells of the 4.1 table; subsection references 2.1, 2.2, 2.3, 3.2 to 3.7, 4.1, 56; references to merged sections 1 to 9, 23, counted by hand from a listing of every "section N" occurrence; references to Appendix A and A.2, 5)
- Resolved: 352
- Broken: 0. Searches for undefined targets (F15 and above, G-5 and above, D-0 and D-8 and above, INV-021 and above, 2.4 and above, 3.8 and above, 4.2 and above) returned only false positives (`R2B section 4.2` references to the Round 2 file, numeric values such as 5.5 and 9.9 percent, and "Round 2.5"). "Section N" strings that point at Round 2 files, Proposal B or research files are labelled with their file and were not counted as internal.

### Contradiction Re-Scan
- New contradictions introduced: 0
- Scan list and result: no remaining statement of "no per-row verdict block" (the phrase appears once, in the note that removes it from the excluded list); no precheck item-evidence flags as part of the design (named only as excluded or withdrawn); no replica assignment (named only in a negation note); no `recipes` slot key (named only as the excluded name and the collision); no statement that demotion or promotion is allowed or built (named only as not built and reserved behind G-4); no remaining "script-first" claim; "Sweep Sheet" appears only as the name of the Proposal A design and of arm SS; the one "empty sheet" appears inside a quotation of MR2 REQ-23.
- Items left as stated in the plan's scope, not resolved by the merge: S-004; D-1, D-2, D-5, D-6, D-7; the A-versus-B split on who computes `observed`; INV-001 and INV-019 (HIGH) and the 14 other UNADDRESSED findings; the unreconciled names of the two all-empty sidecars (F10).

### Decisions and differences between Round 2 files and the plan
1. R2A item 1 says the `extractor` field is optional; R2B (section 4.2 AMEND of component 1), the DT scoring matrix (C-003) and the plan say no `extractor` field until an extractor exists. The merged text follows the plan, which matches R2B and DT, and records A's wording in section 2 item 1.
2. The plan says the 12 to 200, 300 and row-cap values are Variant B's Round 2 proposal. Merged section 2.1 labels them as such.
3. The plan asks for both Round 2 writer lists. Merged 2.2 records both and states the split as open.
4. Edits made as consequences of the plan's changes and not listed as separate plan items: the file header and tag legend; the word "sheet" and Proposal A's `class`, `probe`, `src` example keys in the C-01 text (replaced by row-block terms); the CO-24 sentence (row block in place of sheet); the last clause of 3.6 bullet 1 ("any position in this file"); the INV-G sentence in section 4; the extractor-cost sentence in section 7; a parenthetical in 3.4 pointing at the reserved extractors; two parentheticals in 3.1 noting what advocate B did not re-read (R2B "Not re-read" list); the 3.x heading conversion and the "2.3" heading. None adds a mechanism, number, test name, citation or decision.

## Summary
- Total changes planned: 15
- Successfully applied: 15
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS

Status: Complete
