# Merge Execution Log

Slot C-07 (dispatch-and-launch-mechanism). Merged file: `../merged-dispatch-and-launch-mechanism.md` (one level above `adversarial/`). Plan executed: `refactor-plan.md` (12 planned changes, auto-approved).

## Metadata
- Base: Variant 2 (Proposal B; default model, default persona), `variant-2-original.md`
- Executor: merge-executor agent
- Changes applied: 12 of 12 planned
- Status: success
- Timestamp: 2026-11-14T17:04:02Z (the merged file's header carries the merge start time, 2026-11-14T16:54:28Z)

Section numbering of the merged file: the base's nine sections keep their numbers 1 to 9 so the base's internal references still resolve. Change 2 and Change 3 are inserted as section 2A and section 2B (between base sections 2 and 3). Change 10 is section 10 (after base section 9). Base evidence rows E1 to E15 keep their ids; new rows are E16 to E33.

## Changes Applied

### Change 1: Replace the packaged `gateway.launch` class-word fill with "binding as data in an explicit environment"
- **Status**: Applied
- **Source**: Base s1 and s2; Variant 1 s2 (not carried: `adapters` map); `round2-advocate-B.md` section 0 items 1 to 3 and Response row 1; `round2-advocate-A.md` N1, N3, N4, V1' items 1 and 5, residual R1; `round2-advocate-B.md` RB6
- **Target**: Base s1 (position), s2 (`review-tiers.default.json` row, "dispatch contract" row, `panel.py` row clause), s4 closing "Tests" paragraph, s7 answer point 3
- **Before**: s1 said the `gateway` environment gets its missing `launch` entries by a data edit; s2 filled `environments.gateway.launch` with model-to-class-word pairs and rewrote `test_gateway_resolution_prints_launch_null`; the `panel.py` row said "so a three-reviewer gateway panel fits without relaxing it"; s4 said the test is rewritten and "Position A rewrites the same test"; s7 point 3 said "the data edit removes it without relaxing the profile".
- **After**: s1 states the fill was withdrawn and why (three grounds, rows E18, E19, E21), the packaged `gateway.launch` stays `{}`, and a binding is data in an explicit environment (S5 in section 2A). The s2 `review-tiers.default.json` row is replaced: no packaged data change, `tiers_sha256` unchanged, `--env gateway` still refuses (INV-018 stated), and the Advocate A / Advocate B split on whether the packaged `gateway` environment may ever be filled is stated without choosing. The `panel.py` row clause is removed and replaced by "the cap of three was accepted, 'three words suffice' was not (A-004 QUALIFY/QUALIFY)". s4 "Tests" paragraph replaced. s7 point 3 keeps "refusal comes from an empty data map, not from the ceiling (both advocates confirmed it)", drops the remedy clause. S5 is stated in both advocates' forms (B: `--tiers <file> --env <new name>` with `available`, `stand_ins`, one-word-per-model `launch`, `note`; A: project or user tier file via `find_path`), with INV-003 attached. Base s5 item 3 is handled in Change 7.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Change 1: ... -->` before s1 and before the s2 table (row-by-row detail inside the comment); `<!-- Source: Debate resolution, Change 2 ... -->` before section 2A
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (see re-scan; the retained base sentence that the refusal comes from an empty map stays true)

### Change 2: Insert the ship-now set: S1-S5 shared, S6-S7 from advocate B only
- **Status**: Applied
- **Source**: `round2-advocate-A.md` "What ships now" S1-S5; `round2-advocate-B.md` "What ships now" S1-S7; `invariant-probe.md` rows INV-004, INV-005, INV-010, INV-015, INV-017 (and INV-018 per Change 1 risk)
- **Target**: Base, new section 2A after s2, "Resolution reached by the debate: what ships now"
- **Before**: Section did not exist
- **After**: Numbered list S1 to S7. S6 and S7 are labelled "(B)" and are not called agreed. S5 is stated in two forms. The three required statements are in the list: S1 is a prompt rule with no enforcer (Advocate B conceded, Response row 3) and the replay runs after the votes; the A-006 split on whether the omitted-`model` failure is fixable only in Python (Advocate A: only a Python-built `--model`, R4; Advocate B: not established, PreToolUse guard candidate with unverified payload, one spike, RB4); S3 is unbuilt (`SubagentStop` registered only for a freshness counter, `hooks.json:179`; spike unrun; each row judged against the id requested for that attempt). A sub-table "Findings of the invariant probe that apply to this list" shows INV-004 (LOW), INV-005, INV-010, INV-015, INV-018 (MEDIUM) and INV-017 (HIGH, full text) next to the list, all UNADDRESSED.
- **Provenance tag**: `<!-- Source: Debate resolution, Change 2 — r2A "What ships now" S1-S5; r2B "What ships now" S1-S7 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: Insert the gated `claude-p` launcher design (from Variant 1, as corrected in Round 2)
- **Status**: Applied
- **Source**: Variant 1 s1, s2, s6 (M-1 to M-4); `round2-advocate-A.md` V1' items 1 to 5, G1 to G4, N5, N6, N7, R1 to R5; `round2-advocate-B.md` "What is gated", RB1 to RB6
- **Target**: Base, new section 2B after section 2A, "Gated: an id-addressed `claude-p` reviewer"
- **Before**: Section did not exist
- **After**: What both advocates accepted (one `launch` vocabulary, no `adapters` key, no `read_only: unproven` marker, class-word half is a rule plus a reader, `ClaudeProcess` caller, visit-once fallback walk with exclusion list, ceiling widening by one value only after G2, untrusted PR diffs on the Agent path until G2); gate table G1 to G4 with Advocate A and Advocate B columns (G1: A gate, B measurement and admission gate; G2 accepted by both; G3 and G4 are A's and not addressed in `r2B`); a six-row side-by-side table of the two positions on what follows the gates (build commitment, launcher location, packaged `gateway` fill, what to count for the reach trigger, omitted-`model` failure, recorder differentiator); probe findings INV-007 and INV-016 (both MEDIUM, UNADDRESSED); what the design does not decide (location, C-08, C-09, C-06). Nothing in it is stated as agreed where the advocates split.
- **Provenance tag**: `<!-- Source: Variant 1 sections 1, 2 and 6 (M-1 to M-4), as corrected in Round 2 — Change 3; ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Correct base statements the debate showed to be wrong or overstated
- **Status**: Applied
- **Source**: `diff-analysis.md` X-002, X-005, X-006, X-007; `round1-advocate-B.md` Concessions 1, 2, 3; `round2-advocate-B.md` section 0 and Response rows 1 to 7
- **Target**: Base s4 last paragraph; s3.1 E7, E9, E11; s2 `cli/reflect` row; s5 item 4; s4 INV-L row; s9 last bullet
- **Before**: "Position A rewrites the same test"; E7 "silent swap passes `MODEL_OK`"; E9 and the `cli/reflect` row "raw-id substrate already exists" without its single-model scope; E11 "0 of the 12 under the tier-1b orchestrator"; s5 item 4 "I did not find such a test"; INV-L row "changes a resolution printed under `--env gateway` only" and "Which `--env` the shadow runs pass was not read ([UNVERIFIED])"; s9 last bullet naming "which `--env` the shadow runs pass" as open.
- **After**: s4 paragraph replaced (X-002 Variant 1 90%: the pin passes under the additive form; the base's own fill is what rewrote it, now withdrawn). E7 rewritten (X-005 Neither 75%: the ladder step is logged at `run-reviewer.sh:75`, what is lost is the original slot id and the meaning of `MODEL_OK`). E9 and the `cli/reflect` row carry the X-006 scope note (both statements true at scope; callers launch one model per run; Advocate A Variant 2 60%, Advocate B Neither 60%, unresolved). E11 states Advocate B withdrew "0 of the 12" and both agree 1 of 15 is too small to call the failure rare. s5 item 4 replaced by the static-test fact (row E29; X-007 Neither 65%: exists, pins the `tools:` line, does not pin `permissionMode`, defers the dynamic test). INV-L row: shadow-hash dependence added (`reflect_shadow_exit.py:128-132,205-207`) and the `--env` item answered from `SKILL.md:340` (row E28; A-005 ACCEPT/ACCEPT). s9 bullet 4 marked answered. Each corrected row keeps its tag and carries a "corrected in debate" note.
- **Provenance tag**: `<!-- Source: Base (original, modified) for E7 (X-005), E9 (X-006) and E11 ... — Change 4 ... -->` before the evidence table; section 4 and 9 comments name Change 4
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Add the Round 2 evidence rows that the debate verified
- **Status**: Applied
- **Source**: `round2-advocate-A.md` N1 to N8; `round2-advocate-B.md` NB1 to NB8; `round1-advocate-A.md` Strengths 1 and 2, Weaknesses 2 and 5; `diff-analysis.md` A-005
- **Target**: Base s3.1 evidence table (new rows) and s3.2
- **Before**: Rows E1 to E15; s3.2 had four bullets
- **After**: Rows E16 to E33 added, each naming its source file and the tag the advocate gave it, marked [CARRIED] when not re-read: validator rejects unknown environment keys (E16, N1); few Python consumers of `launch` (E17, N2); packaged-template arithmetic and the 400-run result (E18, N3, NB2); documented default binding and the same word served different models (E19, NB1, `r1A` Strength 1); `--tiers` and `find_path` (E20, N4, NB5); shadow-hash dependence and `select_env` default (E21, NB4); restricted flags on 2.1.325 (E22, N5, NB8); `ClaudeProcess` flags (E23, N6); E2 ladder lessons (E24, N7); commit-id citation form (E25, N8); explicit-environment in-memory result (E26, NB3); `Agent` PreToolUse precedent with `model` payload [UNVERIFIED] (E27, NB6); shadow `--env anthropic-only` and D4 (E28, A-005); static read-only test (E29); `SubagentStop` capture unbuilt (E30); A's gated fill seed-dependent refusal [INFERENCE] (E31, NB7); reach bounded by the enum (E32, `r1A` Strength 2); one-to-one map not checked (E33, `r1A` Weakness 2). `r1A` Weakness 5 (`live7`) is placed in section 6 with its attribution. s3.2 gained: no `--restricted` gateway-id run, no dynamic read-only test on any path, no measured cost of either path, `message.model` truthfulness after failover unproven and `SubagentStop` spike unrun, and the E2 sandbox sentence. The base's tag legend is kept and extended with [CARRIED].
- **Provenance tag**: `<!-- Source: Base (original) for rows E1-E6, E8, E10, E12-E15 ... Rows E16-E33: Change 5 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Rewrite the invariants section with the probe results
- **Status**: Applied
- **Source**: Base s4 (invariant table); Variant 1 s4 (Preserved/Endangered ratings); `invariant-probe.md`; `round2-advocate-B.md` section 0 item 2 and NB4
- **Target**: Base s4
- **Before**: Two-column table (invariant, "under position B"); no unaddressed list
- **After**: The base's rows are kept row for row with a Rating column added (INV-G Endangered HIGH; INV-L Preserved for ship-now, endangered by any packaged tier edit, MEDIUM; INV-K, N Endangered MEDIUM; INV-E MEDIUM under Advocate A's launcher location). The INV-G row keeps the base statement that it is preserved for every reviewer launched as a read-only agent file (E1) and adds the third gap (static pin only; S4) and the `claude-p` ceiling point (INV-016). Sub-section "Invariants the debate left unaddressed" lists INV-001 to INV-019 with category, status and severity exactly as in `invariant-probe.md` (verified by a column-by-column diff of IDs, categories, statuses and severities: identical): 19 findings, 3 ADDRESSED, 16 UNADDRESSED (1 HIGH INV-017, 12 MEDIUM, 3 LOW).
- **Provenance tag**: `<!-- Source: Base (original, modified) — Change 6 ... -->` and `<!-- Source: invariant-probe.md ... all 19 rows — Change 6 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 7: Rewrite the measurement section in the right-if / wrong-if format
- **Status**: Applied
- **Source**: Base s5 items 1 to 6; Variant 1 s6 (M-1 to M-4); `round2-advocate-A.md` S4, G1 to G4; `round2-advocate-B.md` S4, S6, G2, RB4; `invariant-probe.md` INV-005, INV-006, INV-007, INV-010, INV-012, INV-019
- **Target**: Base s5
- **Before**: Six items with "B is right if / wrong if" only on item 1; item 3 included an "After the data edit" clause; item 4 said no such test was found
- **After**: Eleven items, each with Right if / Wrong if / Fallback. Base items 1, 2, 3, 5, 6 kept (item 3's data-edit clause replaced, base item 4 replaced by the corrected dynamic read-only test); added the binding-shape tests (S6), PreToolUse payload spike (RB4), G1, G2, G3, G4. The probe's open criteria are carried: INV-005 (item 2), INV-006 (item 5), INV-007 (item 9), INV-010 and INV-012 and INV-002 (item 4), INV-004 and INV-012 (item 3), INV-019 falsifiers (item 6). Where neither advocate stated a fallback the item says "none stated" and does not invent one.
- **Provenance tag**: `<!-- Source: Base (original, modified) — Change 7 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 8: Update the consumer section (PR review, rf-qa, C-12)
- **Status**: Applied
- **Source**: Base s6; Variant 1 s5; `round1-advocate-A.md` Concession 8 and Weakness 5; `round2-advocate-A.md` B-W6; matrix rows C-008 and C-009
- **Target**: Base s6
- **Before**: Four bullets
- **After**: The base's statements are kept (`--revagent` takes four class words; rf-qa lenses differ by lens; the C-12 hook-exchange cost). Appended: up to N `claude -p` children per PR round, each loading host hooks without `--bare`; untrusted PR diffs use the Agent-class path until G2 passes; both costs unmeasured; neither position serves `live7` or a panel needing more than three or four distinct served models today; rf-qa gateway diversity is blocked on G2, not on a design change; a closing bullet with the C-008 (Variant 2 57%) and C-009 (Neither 50%) results. The `w02` line numbers are [CARRIED] from Variant 1.
- **Provenance tag**: `<!-- Source: Base (original) bullets, with Change 8 additions appended ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 9: Add the C-06 and C-08 interface constraints to the consistency section
- **Status**: Applied
- **Source**: Base s8; Variant 1 s4; `diff-analysis.md` U-004; `invariant-probe.md` INV-011
- **Target**: Base s8, new bullets
- **Before**: Bullets for C-01, C-02, C-03 and the disagreement/dependency bullet
- **After**: Three bullets added: C-06 (a bounded re-ask needs a persisted session; `ClaudeProcess` always passes `--no-session-persistence`, `process.py:152`; `--resume` for gateway ids [UNVERIFIED]; a `claude-p` launcher must be able to keep a session id if C-06 needs it; stated as a constraint, not a decision); C-08 (recorder's home; reader key must distinguish reviewer id from attempt id, INV-011); C-09 (owner of the model-to-class-word map). The existing C-03 bullet now labels its "INV-007" as slot C-03's own numbering to avoid confusion with the probe's INV-007.
- **Provenance tag**: `<!-- Source: Base (original) for the three slot bullets ...; Change 9 additions ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 10: Add the debate outcome table and the unresolved points
- **Status**: Applied
- **Source**: `debate-transcript.md` Scoring Matrix and Convergence Assessment; `diff-analysis.md`; `invariant-probe.md`; `base-selection.md`; Round 2 final-position paragraphs of both advocates
- **Target**: Base, new section 10 "Debate outcome (26 points)" near the end
- **Before**: Section did not exist
- **After**: Convergence stated exactly (21 of 26 = 80.77% against 80%, BLOCKED_BY_INVARIANTS because INV-017 HIGH is UNADDRESSED; Round 1 agreement 16 of 26 = 61.54%); the 26-row matrix (verified identical to the transcript by a row diff); the tally (Variant 1 2, Variant 2 9, Hybrid 5, Neither 5, unresolved 5); a table of the five unresolved points (X-001, X-006, A-003, A-004, A-006) with Advocate A and Advocate B positions and confidences; the statement that for A-003, A-004, A-006 equal assumption labels with different superior approaches are unresolved at 50% and are not called converged substance; a table of final positions on A-002 to A-006 (A-001 noted as Round 1 only); the 16 UNADDRESSED invariants listed with IDs and severities; a "Not carried from Variant 1" block.
- **Provenance tag**: `<!-- Source: Debate record, Change 10 ... -->` on the section and on each sub-block
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 11: Fix the base's clarity weakness (terms defined on first use)
- **Status**: Applied
- **Source**: `score-reeval.md` pair 7; plan Change 11 rationale; `invariant-probe.md` INV-018 (C-S6 label); `round2-advocate-A.md` G4 (CO-10 label)
- **Target**: Base header block and s1
- **Before**: Header used INV-G, INV-L, INV-F, C-S6, CO-10, FX-13 and "synth-06 6.12.0" before any gloss; "sidechain" and "shim" undefined
- **After**: Header glosses INV-G, INV-L, INV-F, C-S6 (the `--env gateway` refusal), CO-10 (the unmeasured cost, Advocate A's G4), "shim" (the local gateway alias proxy) and "sidechain" (the subagent's own transcript), using only definitions found in the base or the debate files. FX-13 is kept as a bare citation id with its source locator (the base's "synth-06 6.12.1, 6.12.5, 6.12.2" list) and marked as defined in an external synthesis file that the merged document does not reproduce; no definition was invented for it. The pointer to "synth-06 6.12.0" is marked external. Added in the same block: the meaning of "Advocate A", "Advocate B", "I", "my", "B", "A", and a note on the reused ids "E2" and "S1-S5".
- **Provenance tag**: `<!-- Source: Base (original, modified) — Change 11 (terms glossed on first use) and Change 12 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 12: Add provenance, status line and the return pointers
- **Status**: Applied
- **Source**: SKILL.md `provenance_system`; `artifact-templates.md` Section 6
- **Target**: Whole merged file
- **Before**: No provenance
- **After**: Three header comments (`Provenance: This document was produced by /sc:adversarial`, `Base: Variant 2 (Proposal B; default model, default persona)`, `Merge date: 2026-11-14T16:54:28Z`, taken from `date -u`); 20 `<!-- Source: ... -->` tags, one before each section, sub-section with new or modified content, and significant block; a final status line naming the convergence status. `ADJUDICATION-RESULT.md` is not part of the merged file (the orchestrator writes it); the only mention of that file name is the base's own "Read before writing" list in section 8.
- **Provenance tag**: header comments and per-section `<!-- Source: ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. One H1, then H2 sections 1, 2, 2A, 2B, 3, 4, 5, 6, 7, 8, 9, 10; H3 only under H2 (2A: "Findings of the invariant probe..."; 3: 3.1, 3.2; 4: "Invariants the debate left unaddressed"; 10: "Scoring matrix", "The five unresolved points", "Final positions on the shared assumptions", "Invariants left unaddressed", "Not carried from Variant 1"). No level gaps, no orphaned subsections.
- Section ordering: PASS. The base's nine sections are in the base's order; 2A and 2B follow section 2 (they restate what section 2 names and are cited by sections 3 to 9); section 10 follows section 9.
- Document flow: PASS. Header (status, position, glosses, legend) precedes section 1; the ship-now set (2A) precedes the gated design (2B); the evidence (3) precedes the invariants (4) and the measurements (5); the debate record (10) comes last. The `APPEND-MARKER` used while assembling the file is removed (0 left).

### Internal References
- Total references: 386 (evidence-row ids 89, excluding the 32 row-head cells and the prose use of "E2" for the external evaluation; section references 65; section-5 item references 5; probe invariant ids 126; point ids A-001 to A-006 and X-001 to X-009, 101). Other ids (S1 to S7, G1 to G4, R1 to R5, RB1 to RB6) are defined where used (sections 2A and 2B).
- Resolved: 386
- Broken: 0. Checks run: highest evidence id referenced is E33 and E1 to E33 are all defined (33 rows); every `section 2A|2B|4|5|8|10` and every `section 5 item N` target exists; INV-001 to INV-019 are all defined in the section 4 table; the 26 matrix rows are identical to the transcript's; the 19 invariant rows match `invariant-probe.md` on ID, category, status and severity. References to external files (research files `r04`, `r13` and so on, `r1A`, `r1B`, `r2A`, `r2B`, `W02`, `SKILL.md`) are named in the header or in place and are not counted.
- Notes: (1) The base uses "E2" both for the external evaluation and as an evidence row id; this is kept and disambiguated in the header. (2) Section 4 row INV-C, D, E, J keeps the base's own label "S1-S5", which collides with the ship-now items S1 to S5; the header says so. (3) Slot C-03's own "INV-007" and "INV-013" (cited by the base in sections 4 and 8) are labelled as slot C-03's numbering, distinct from the probe's INV-007 and INV-013.

### Contradiction Re-Scan
- New contradictions introduced: 0
- Details: places where the merged text could be read as contradicting itself, and how each is handled:
  1. Section 4 INV-I ("Preserved for dispatch: a reviewer launched without its class word is a dispatch error") against INV-017 and section 2A (S1 is a prompt rule with no enforcer; the collapse failure is not closed). The row now says "Preserved for dispatch, with the S1 caveat" and points to INV-017.
  2. Section 1 ("no launcher ... is added to the core now") against section 2B (a gated launcher design) and section 7 point 5. Consistent through "now" and "gated, not built"; section 7 point 5 states the Advocate A / Advocate B split.
  3. Section 7 objection (retained from the base: "the product still cannot launch a gateway panel") against section 2A (ship-now set leaves `--env gateway` refused, INV-018). Not a contradiction: the objection is the base's strongest objection, and section 7 point 3 now says the refusal remains in a gateway workspace unless a caller passes an explicit tier file and environment.
  4. Section 8 C-01 bullet (retained: B keeps dispatch "in the module's engine") against Advocate A's shared-layer location for a future launcher. The bullet gained a parenthetical naming the difference; the position is not resolved (section 2B).
  5. Section 8 C-02 bullet (retained: a re-review is one Agent call with the original slot's class word) against INV-012 (a fallback model may have no word). INV-012 is an open finding listed in section 4, not a statement that contradicts the bullet.
  6. Evidence rows E4 and E19: E4 (observed reach of class words, retained) against E19 (the same word served different models by session setup). E4 now carries Advocate A's qualification that it shows reach for a panel chosen before the session.
  7. Section 5 intro ("none needs a launcher") against item 1 arm (b), which runs `claude -p`. Clarified: arm (b) is E2's own command line, not product code.
  8. Section 2A S1 ("agreed") against INV-004 (S1's null-`launch` clause meets D4's legacy-rotation rule). INV-004 is shown next to the list; S1's text is unchanged.
  9. Section 2B states G3 and G4 are Advocate A's and `r2B` does not address them, while `r2B` S2 carries a `tiers_sha256` check; the gate table notes this next to the G3 cell, without equating the two.

## Summary
- Total changes planned: 12
- Successfully applied: 12
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
- Notes for the orchestrator: (a) no change needed escalation; (b) the merged file adds nothing the debate did not conclude, but it adds one disambiguation sentence in the header (ids "E2" and "S1-S5") and one closing bullet in section 6 and one "Not carried from Variant 1" block in section 10, all traceable to the plan or to debate files; (c) tags: 34 `[CARRIED]` tags mark content taken from advocate round files and not re-read by the merge executor; the merge executor read only the debate files, the variants, the plan and the two template files, and ran no repository commands beyond structural checks of the merged file and diffs of the matrix and the invariant table against their sources; (d) convergence status is carried exactly: 21 of 26 (80.77% against 80%), BLOCKED_BY_INVARIANTS because INV-017 (HIGH) is UNADDRESSED, with the five unresolved points and the 16 unaddressed invariants listed.
