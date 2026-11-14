# Base Selection Report - Scorer Pass 1 (input order: A then B)

Slot C-09 (`panel-resolution-and-tier-source`). Variant A = `variant-1-original.md` (Proposal A). Variant B = `variant-2-original.md` (Proposal B). Both scored AS WRITTEN. The debate is used only as evidence for correctness verdicts. Code spot-checks were read-only (`panel.py:594-707`, `tests/unit/test_ccsession_tiers.py:216-222`, `tests/review/test_review_cli.py:50-61`).

## Requirement list used for RC (derived from the C-09 row; the source has no formal IDs)

Method: the source row text of C-09 in `phase-outputs/discovery/undecidable-conflicts.md` line 26 gives the A-position claims, the B-position claims and the stated tensions; the task adds the seven common sections each proposal must carry. A requirement counts as matched when the variant contains a passage addressing it (keyword match of 3+ consecutive words or section-level topic match, per the protocol edge case "no formal requirement IDs").

| # | Requirement (source) | Variant A match | Variant B match |
|---|---|---|---|
| R1 | A-claim: one package-owned tier file (classes, launch map, vendor) is the single source | Yes: sec 1 "the package owns the tier data ... the one file" | Yes (rejects it): sec 2 item 1 "Nothing in the packaged file is called the single source of membership" |
| R2 | A-claim: checked against `ccsession-models.json` slot lists | Yes: sec 1, 2.1 row "slot lists of ccsession", 3.1 item 4, 5.2 | Yes: sec 2 item 2 derive-and-compare, E3 |
| R3 | A-claim: the E2 fallback ladder is derived from the tier file | Yes: sec 2.1 last row, 3.4 | NO: no passage on the E2 ladder or `FALLBACK` map (grep: only unrelated "fallback" hits at lines 22 and 102) |
| R4 | A-claim: strict distinctness is the default | Yes: sec 1, 2.3 | Yes (rejects it): sec 1, E4, E5, 7 |
| R5 | A-claim: a shortfall fails loudly | Yes: sec 2.3 items 2-3 | Yes (answers it): E4 mechanism, sec 7 point 2 |
| R6 | A-claim: ember is added by a data edit | Yes: sec 2.4 | Yes (rejects it): sec 2 "muse-ember-1.0", E6, sec 4 cross-repo ordering |
| R7 | B-claim: ccsession slots and Coder env are the source; the package file is derived | Yes (answers it): sec 3.1 items 1-3, 7.1 | Yes: sec 1, 2 item 1, E1-E2 |
| R8 | B-claim: soft distinctness stays the default for availability | Yes (answers it): sec 3.3, 4.2 availability, 7 | Yes: sec 1, 2 item 4, E4-E5 |
| R9 | Tension: ownership across the repo and the Coder env (outside the repo) | Yes: sec 2.1 rows "model id behind a slot", 3.1 | Yes: sec 2 item 1, E1, E9 |
| R10 | Tension: three class vocabularies | Yes: sec 3.2 | Yes: sec 2 item 6 |
| R11 | Tension: tests pin soft distinctness as intended | Yes: sec 3.3 first bullet, 4.2 | Yes: E5 |
| R12 | Tension: availability versus diversity trade-off | Yes: sec 3.3 table, 4.2 last bullet, 7 | Yes: E4, 7 |
| R13 | Tension: ember slot and gateway status open | Yes: sec 2.4, 3.5 first bullet | Yes: E6 (slot 02 versus 04, GQ-046) |
| R14 | Common section: position | Yes: sec 1 | Yes: sec 1 |
| R15 | Common section: design consequence for shared core and named modules | Yes: sec 2, 2.2 | Yes: sec 2 |
| R16 | Common section: evidence | Yes: sec 3 | Yes: sec 3 (E1-E10) |
| R17 | Common section: invariants preserved/endangered | Yes: sec 4.1, 4.2 | Yes: sec 4 |
| R18 | Common section: test or measurement that would show it right or wrong | Yes: sec 5 (M1-M3, tests) | Yes: sec 5 (5 items) |
| R19 | Common section: effect on future PR review and rf-qa replacement | Yes: sec 6 | Yes: sec 6 |
| R20 | Common section: strongest objection and answer | Yes: sec 7 | Yes: sec 7 |

Totals: A matched 20/20; B matched 19/20 (R3 missing).

## Quantitative Scoring (50% weight)

Counting unit for IC and SR: one "claim unit" = one numbered item, bullet, table row, or (for the one-paragraph position sections) one sentence, in the numbered sections. Metadata lines, headings, the citation-form legend and the "[UNVERIFIED] what I could not check" bullets (A sec 3.5) are excluded. Counts are by reading; they can be re-derived with the unit definition.

| Unit count by section | Variant A | Variant B |
|---|---|---|
| position (A sec 0 + 1; B sec 1) | 4 + 5 = 9 | 4 |
| design (A sec 2; B sec 2) | 8 + 4 + 5 + 3 = 20 | 6 + 4 = 10 |
| evidence (A sec 3; B sec 3) | 5 + 3 + 6 + 4 = 18 | 10 |
| invariants (A sec 4; B sec 4) | 6 + 4 = 10 | 6 + 5 = 11 |
| tests/measurements | 3 + 6 = 9 | 5 |
| effect on PR review / rf-qa | 3 | 4 |
| objection and answer | 1 + 5 = 6 | 1 + 4 = 5 |
| adjudicated-slot dependence (B sec 8) | (counted in A sec 0) | 4 |
| **total claim units** | **75** | **53** |

Contradictions found by reading (each is an opposing-claims or requirement-constraint conflict inside one variant; each was also conceded or judged against the variant in the debate):

- A-1 (A sec 2.2 versus 4.2; diff X-007): sec 2.2 says "Under A the loop declares its distinctness on purpose, so its panel does not change by the default flip"; sec 4.2 says the flip "changes the spec loop's anthropic-only panel from 4 reviewers to as few as 2" and the declaring prompt copy can lag. Sec 5.2 lists no edit or test for the prompt change. A conceded this in Round 2 (B-W1).
- A-2 (A sec 1 and 2.1 versus 2.1 row "model id behind a slot", 3.1 item 3 and M3; diff X-006): "the one file" / "single source" versus the Coder env owning the served model and M3 "A is wrong on the single-source claim if the env or the live ccsession file changes ... faster than package releases". A conceded "single source" is an overclaim.
- A-3 (A sec 1 "a shortfall ... fails loudly" and 2.3 item 3 versus 3.3 table and 5.2): the exit rule fires only below `min(2, requested)`, but strict anthropic-only resolves 2 reviewers in every run (3.3 table "Max skipped 5" for `@live7`, 2 resolved), and 2 is not below `min(2, 7)`. The stated loud failure never fires in the environment where the shortfall is largest (diff X-003, debate "Neither" 78%). A withdrew the exit rule.
- B-1 (B sec 7 point 1 and sec 1 "so a shortfall is visible" versus sec 2 item 5 and sec 5 item 2; diff X-001): "The repeat is not silent under B: `distinct_models` and `requested_slots` are written" versus the keys being "written only when a profile or flag asks" and the test "the spec profile resolves soft and records neither key". The one soft consumer still repeats silently (code: `skipped_slots` and `excluded` only under `hard_exclude or strict_distinct`, `panel.py:700-706`, read this session). B conceded the text.
- B-2 (B sec 1 and 2 item 1 versus sec 2 "muse-ember-1.0" and sec 6; diff X-005): the packaged lists are "a snapshot", nothing there is "the single source of membership", yet ember panels "become resolvable once membership and `classes` carry it" through a ccsession slot edit, a `classes` and `names` entry and a golden. The resolver reads the packaged list (`panel.py:615`, read this session), so ember is not picked unless the packaged list names it; B's own check also needs a `MODEL-TIERS.md` row. B conceded the omitted edits.
- B-3 (B sec 7 point 2 versus E4 table): "'fails loudly' requires a new raise rule that makes the default panel unresolvable" in anthropic-only, but B's own E4 table says strict there gives "always 2" reviewers, a resolvable panel. B's "unresolvable" does not follow (diff X-003, debate "Neither").

| Metric | Weight | Variant A | Variant B |
|--------|--------|-----------|-----------|
| requirement_coverage | 0.30 | 1.0000 (20/20 requirements matched) | 0.9500 (19/20; R3 E2 ladder absent) |
| internal_consistency | 0.25 | 0.9600 (1 - 3/75; contradictions A-1, A-2, A-3) | 0.9434 (1 - 3/53; contradictions B-1, B-2, B-3) |
| specificity_ratio | 0.15 | 0.9333 (70 concrete / (70 + 5 vague)) | 0.9057 (48 concrete / (48 + 5 vague)) |
| dependency_completeness | 0.15 | 0.8824 (15 resolved / 17 internal refs) | 1.0000 (12 resolved / 12 internal refs) |
| section_coverage | 0.15 | 1.0000 (8 H2 / max 8) | 1.0000 (8 H2 / max 8) |
| **quant_score** | | **0.9624** | **0.9567** |

Computations (re-derivable):

- A: 0.30 x 1.0000 = 0.3000; 0.25 x 0.9600 = 0.2400; 0.15 x 0.9333 = 0.1400; 0.15 x 0.8824 = 0.1324; 0.15 x 1.0000 = 0.1500. Sum = 0.9624 (0.96235 unrounded).
- B: 0.30 x 0.9500 = 0.2850; 0.25 x 0.9434 = 0.2358; 0.15 x 0.9057 = 0.1359; 0.15 x 1.0000 = 0.1500; 0.15 x 1.0000 = 0.1500. Sum = 0.9567.

Detail for SR (vague units = a unit with no number, named file/function/test, threshold or measurable criterion; the protocol vague words "might", "should consider", "as appropriate", "various", "etc." occur in neither variant, grep returned no hit):

- A vague (5): sec 2.2 Tasklist/workflow/PR/rf-qa bullet ("take the strict default ... a consumer that wants repeats declares them"); sec 4.1 "INV-G, INV-H, INV-J, INV-M, INV-N: not touched"; sec 6 third bullet ("Both futures need a launcher that A does not provide"); sec 7 point 4 (conditional concession); sec 7 point 5 (open owner question).
- B vague (5): sec 2 "Tasklist, PR review, rf-qa replacement" bullet; sec 4 "INV-C, INV-D, INV-E, INV-G, ... untouched by this slot"; sec 6 third bullet ("Ember-based panels become resolvable ... nothing else ... changes"); sec 6 fourth bullet ("Both consumers get a stated owner"); sec 8 "Not addressed here, by design".

Detail for DC (internal references only; external IDs such as C-0N, INV-x, R04, r17, GQ-nnn are excluded):

- A, 17 internal refs: sec 0 "(section 4)", "(section 2.3)"; sec 2.2 "(see 2.3)"; sec 2.3 item 4 "(see 3.4)"; sec 2.4 "(2.1)"; sec 3.5 "(section 7)", "(3.3, scarcest tier first)"; sec 4.1 "(see 5.2)", "(section 3.5)", "(3.3)"; sec 4.2 "(table in 3.3)"; sec 5.1 "(3.3)", "(5.2)"; sec 5.2 "(5.1 above lists why)"; sec 7 "(3.1 item 4)", "M1", "M3". Unresolved (2): sec 2.3 item 4 "(see 3.4)" points to the ladder and tier-copy section, but the scarcest-first order is in sec 3.3 third bullet; sec 5.2 "(5.1 above lists why)" points to sec 5.1, which says nothing on the golden (the reason is in sec 4.2). Resolved 15/17 = 0.8824.
- B, 12 internal refs: sec 2 item 3 "(section 3, E9)"; sec 2 "muse-ember-1.0" "(section 3, E6)"; sec 5 "(E3)", "(E8)", "(E4)"; sec 6 "(E4)" twice; sec 7 "(E4)", "(E8)", "(E9)"; sec 8 "(section 2 item 5)", "(E4)". All resolve. Note: "layer 1" (sec 4, 5) is never labelled where defined (sec 2 item 2) but item 3 names "the second layer", so it resolves by implication. 12/12 = 1.0000.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

CEV layout: CLAIM = the criterion named in the first column, stated for that variant; EVIDENCE = the quoted text or section reference in the Evidence column ("No evidence found" where none); VERDICT = the MET / NOT MET column. Evaluated in input order (Variant A rows first, then Variant B). Section numbers are those of each variant's own H2 headings. Correctness verdicts use the debate (`debate-transcript.md` scoring matrix, rounds 1-2) and `diff-analysis.md` verification notes as evidence, with the code spot-checks named at the top.

### Completeness (5 criteria)

| Criterion | Variant A | Evidence (A) | Variant B | Evidence (B) |
|-----------|-----------|--------------|-----------|--------------|
| C1 Covers all explicit requirements from source input | MET | All 20 derived requirements matched (table above); every A-claim, B-claim, tension and common section has a passage, e.g. sec 2.1 last row "E2 fallback ladder ... a pure function of the tier lists" | NOT MET | 19 of 20: the A-claim "E2 ladder derived from the tier file" (R3) has no passage; grep for `ladder\|FALLBACK` finds only unrelated "fallback" at lines 22 and 102. Searched sec 1-8 |
| C2 Addresses edge cases and failure scenarios | MET | Sec 3.3 table: `@live7` anthropic-only "40 of 40 ... Max skipped 5"; sec 0 "A hand-edited empty list stays C-02's open item"; sec 2.3 item 3 "A fixed-anchor exhaustion keeps failing (`panel.py:647-649`)" | MET | E4 "strict leaves two reviewers" in anthropic-only; E6 "a missing slot fails loudly (`models.py:669`)"; sec 4 "Cross-repo ordering ... fails every workspace whose env lacks the slot" |
| C3 Includes dependencies and prerequisites | MET | Sec 0 names the C-01, C-02, C-03 outcomes it depends on; sec 2.4 "add the env slot in Coder first, because ccsession stops when a listed slot is not set (`MODEL-TIERS.md:189-193`)" | MET | Sec 8 "Dependence on the adjudicated slots C-01, C-02 and C-03" with two named C-03 dependencies; E6 "after the Coder `defaults.sh` carries the matching slot" |
| C4 Defines success/completion criteria | MET | Sec 5.1 "A is wrong on the default if declared-repeat or soft panels beat strict panels at equal reviewer count with a confidence interval that excludes zero; it is right if strict is not worse"; sec 5.2 tests list | MET | Sec 5 item 1 "It is red when any of the six packaged lists differs ... It is green today"; item 4 "B is wrong if distinct-served panels find materially more blocking items at equal reviewer count" |
| C5 Specifies what is explicitly out of scope | MET | Sec 0 "Position A does not decide clearing ... A does not decide the merge-side half"; sec 6 "Both futures need a launcher that A does not provide"; sec 7.5 "What A does not answer" | MET | Sec 8 last paragraph "Not addressed here, by design: the launch mechanism (C-07), served-model capture (C-08), the choice of E2 panels, and any change to the reflect profile ceiling" |
| **Subtotal** | **5/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence (A) | Variant B | Evidence (B) |
|-----------|-----------|--------------|-----------|--------------|
| K1 No factual errors or hallucinated claims | NOT MET | Claims shown wrong or conceded: sec 2.2 "its panel does not change by the default flip" (contradicted by A sec 4.2; conceded B-W1); sec 2.4 "Adding `muse-ember-1.0` is a data edit ... not a code change" and the ember edit list cites only `test_review_panel_live7.py:94-96`, omitting `tests/unit/test_ccsession_tiers.py:222` which pins tier4 to `T4Model01..03` (read this session; conceded B-W7, "data edit is withdrawn"); sec 1 "the one source" (conceded overclaim, B-W4). Line cite `panel.py:371-373` is off by one (harmless, diff V-5) | NOT MET | Claims shown wrong or conceded: sec 7 point 1 "The repeat is not silent under B" (conceded, X-001); sec 7 point 2 "unresolvable" in anthropic-only (own E4 table says "always 2"; debate X-003 "Neither"); sec 2 ember steps omit the packaged-list edit the resolver needs (`panel.py:615`; conceded X-005); sec 4 "pins pass unmodified" holds only for the keys-written-on-request text (B-W1) |
| K2 Technical approaches are feasible with the stated constraints | NOT MET | Strict default conflicts with its own constraint that the spec loop is unchanged: `tests/review/test_review_cli.py:52-61` pins the default `panel resolve --env anthropic-only` at `t1b-1, t2-1, t3-1, t3-2` (read this session), so the flip moves 3-4 CLI pins and needs a 3-file prompt edit; sec 4.2 itself says "I do not call that 'pins unmodified'". Debate C-003: Variant B wins 83%, A withdrew the strict default. The `vendors` map and marker list need validator edits (sec 3.4 admits the closed key set) that sec 5.2 does not count (A-003) | MET | Core design is feasible with the stated constraints: derive-and-compare for six tiers is "green today (E3)", soft default keeps the byte-identity golden (sec 2 item 5 "written only when a profile or flag asks"), and debate C-002 "Variant B 90%, A adopted it", C-009 "Variant B 88%". Weak parts (profile `distinctness` field needing a validator edit, overlay) are flagged by B as weakest (E9) and dropped in the debate, but are not the core |
| K3 Terminology used consistently and accurately throughout | NOT MET | "single source" / "the one file" / "owns the tier data" (sec 1, 2.1) versus the same text saying the Coder env owns the served model (2.1 row 6) and M3; the term is used in two senses (diff X-006, conceded). "A shortfall fails loudly" (sec 1) versus a command that exits 0 on 2 resolved of 7 (sec 2.3 item 3) | MET | Terms stay in one sense: "owner" for membership and order, "consumer" and "snapshot" for the packaged lists (sec 1, 2 item 1); "requested_slots" versus "distinct_models" versus served identity kept apart (E8). Evidence: sec 2 item 1 "Nothing in the packaged file is called the single source of membership" |
| K4 No internal contradictions (cross-validated with IC) | NOT MET | IC found 3: A-1 (sec 2.2 versus 4.2), A-2 (sec 1/2.1 versus 2.1 row 6/M3), A-3 (sec 2.3 item 3 versus 3.3 table). IC_A = 0.9600 | NOT MET | IC found 3: B-1 (sec 7.1 versus 2 item 5/5 item 2), B-2 (sec 1/2 versus ember steps), B-3 (sec 7.2 versus E4 table). IC_B = 0.9434 |
| K5 Claims supported by evidence or rationale within the document | MET | Tagged evidence throughout; counts reproduced by the diff analyst: sec 3.3 table "30 of 40 ... 18 of 40" and "0 skipped slots in 40 of 40 gateway runs" with scarcest tier first (diff V-1 reproduced both) | MET | E1-E10 with line cites; E4 table "18 of 40 / 30 of 40" reproduced (diff V-1); unsupported items are tagged [UNVERIFIED] (E6, E8, E10) rather than asserted |
| **Subtotal** | **1/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | Variant A | Evidence (A) | Variant B | Evidence (B) |
|-----------|-----------|--------------|-----------|--------------|
| S1 Logical section ordering (prerequisites before dependents) | MET | Sec 0 "Consistency with the three adjudicated slots" comes first, then position (1), design (2), evidence (3), invariants (4), tests (5), effect (6), objection (7); the C-01..C-03 prerequisites precede the design that depends on them | NOT MET | The adjudicated-slot dependence is sec 8, last, although sec 2 items 4-5 already build on C-03's quorum and C-02's INV-001 (diff S-001); the dependents come before the prerequisite statement. Searched sec 1-8 |
| S2 Consistent hierarchy depth (no orphaned subsections) | MET | H2 sec 0-7; H3 only under sec 2 (2.1-2.4), 3 (3.1-3.5), 4 (4.1-4.2), 5 (5.1-5.2), each with 2 or more siblings; sec 1, 6, 7 have none | MET | H2 sec 1-8 only; numbered lists inside; no H3 and no single-child subsection (grep of `^## ` gives 8 headings) |
| S3 Clear separation of concerns between sections | MET | Position (1), design (2), evidence (3), invariants (4, split preserved/endangered), tests (5), consequences (6), objection (7) are separate; evidence and design are not mixed | MET | Same separation; sec 3 is evidence only (E1-E10), sec 4 invariants, sec 5 tests |
| S4 Navigation aids present (TOC, cross-references or index) | MET | Citation-form legend at the top ("`R<NN>` is `research/NN-*.md` ... Tags: [CODE-VERIFIED] ..."), numbered sections and in-text cross-references such as "(see 3.3)", "(section 2.3)" | MET | Legend line 8 ("Tags: [CODE-VERIFIED] ... `r04` = `research/04-...`"), evidence ids E1-E10 cross-referenced from sec 2, 5, 6, 7, 8 |
| S5 Follows conventions of the artifact type | MET | Carries all seven required common sections plus the "Status: Complete" marker at top and bottom | MET | Carries all seven required common sections plus the "Status: Complete" marker at top and bottom |
| **Subtotal** | **5/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence (A) | Variant B | Evidence (B) |
|-----------|-----------|--------------|-----------|--------------|
| L1 Unambiguous language (no "should consider", "might", "as appropriate") | MET | Grep for `might\|should consider\|as appropriate\|as needed\|various\|etc\.\|properly\|adequate\|best practice` returns no hit; design statements carry an explicit "design inference" label (sec 2.3 "Under A (design inference; each piece is small)") | MET | Same grep returns no hit; uncertain items are tagged [UNVERIFIED] with the reason (E2 "that rule is [UNVERIFIED] as a repo rule") |
| L2 Concrete rather than abstract (specific actions) | MET | Sec 2.3 items 1-4 name flags, keys and exit behaviour ("`--allow-repeat`", "`expected`", "`shortfall = expected - len(reviewers)`"); sec 5.2 names six tests | MET | Sec 2 item 2 names the exact check ("ordered id list of `aliases.<tier>.models` must equal the ordered ids of the matching row of the `MODEL-TIERS.md` section 1 table"); sec 5 names five tests |
| L3 Each section has a clear purpose or one-sentence summary | MET | Headings state the purpose ("The test or measurement that would show A right or wrong"); sec 1 is a one-paragraph summary | MET | Headings state the purpose ("The test or measurement that would show B right or wrong"); sec 1 is a one-paragraph summary |
| L4 Acronyms and domain terms defined on first use | NOT MET | "E2" (the evidence base for the ladder, the `ember + 2x luna` panel, the harness) is never defined; "T1" in sec 0 ("all existing pins pass unmodified (T1)"), "GT1-style", "M1" use R08 labels, "OQ-10", "DATA-11" and "GQ-050 / Q-5" are not expanded. Some are glossed ("CO-13: `muse-ember-1.0` is not a product default"). Searched sec 0-7 for a definition of E2: none | NOT MET | "E2" never defined; "CO-14", "CO-18", "GQ-046", "DR-014", "A-r3" are used without expansion (some are glossed, e.g. "CO-18 says no E2 default enters the core"); sec 4 lists INV-C, D, E, G, H, I, J, M, N as "untouched" with no gloss (the header points to synth-06 only). Searched sec 1-8 |
| L5 Actionable next steps or decision points clearly identified | MET | Sec 5.1 M1-M3 each end in an "A is wrong if" rule; sec 7.5 names the open owner question; sec 2.4 gives the ember order of operations | MET | Sec 5 items 1-5 each state red/green conditions; sec 8 names where the `requested_slots` decision belongs ("C-03's open point 4"); sec 7 gives the optional-overlay boundary |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence (A) | Variant B | Evidence (B) |
|-----------|-----------|--------------|-----------|--------------|
| RK1 Identifies at least 3 risks with probability and impact | MET | Sec 4.2 lists four: INV-C/INV-D (impact "from 4 reviewers to as few as 2"), INV-L (impact "reports a run recorded under the old hash as 'not proven'"), golden pins regenerated, availability ("strict in `anthropic-only` cannot give 7 distinct models from four Anthropic ids"); probability as measured rates in the sec 3.3 table (30 of 40, 40 of 40) | MET | Sec 4 "Endangered or conditioned" lists five: INV-K parser fragility, reproducibility with the overlay, cross-repo ordering ("fails every workspace whose env lacks the slot"), DR-014 stays open, plus E4 rates "18 of 40", "30 of 40" |
| RK2 Provides a mitigation strategy for each identified risk | NOT MET | INV-C has one ("A makes the loop declare it") and availability has "a named shortfall", but INV-L is only accepted: "Adding `vendors` or ember therefore degrades the parity evidence of every existing shadow run under the Stage 2 exit script, by design of that script" with no mitigation, and whether a resumed run re-resolves is left [UNVERIFIED] | NOT MET | INV-K fragility ("breaks loudly, which is the intended direction") and reproducibility (`tiers_source` recorded) have mitigations, but the cross-repo ordering hazard is stated with no gate or mitigation ("Ember cannot be added 'by a data edit' in this repo alone") and DR-014 is left "visible-but-allowed"; the probe notes the same gap for both (INV-009) |
| RK3 Addresses failure modes and recovery procedures | MET | Sec 2.4 "add the env slot in Coder first, because ccsession stops when a listed slot is not set"; sec 3.1 item 2 "a listed slot that a workspace env lacks stops ccsession there"; sec 2.3 "fixed-anchor exhaustion keeps failing" | MET | E6 "a missing slot fails loudly (`models.py:669`)"; sec 4 cross-repo ordering names the failing component; sec 2 ember bullet orders the recovery-free path "after the Coder `defaults.sh` carries the matching slot" |
| RK4 Considers external dependencies and their failure scenarios | MET | Sec 3.1 item 1: the Coder env is "outside the repo and absent on a laptop or in CI (`select_env` then picks `anthropic-only`)"; item 2: live-fetched `ccsession-models.json` reaches workspaces before package release; sec 3.5 gateway status of `muse-ember-1.0` [UNVERIFIED] | MET | E2 (live fetch from master, owner rule [UNVERIFIED]); E9 (wheel may not carry `ccsession-models.json`; "the shim skips a model whose window is smaller ... or that is cooling") |
| RK5 Includes a monitoring or validation mechanism for risk detection | MET | Sec 5.1 M3 "Run the extended cross-check against the ccsession file of `master` and against the Coder env of a real workspace on a schedule or at release; count disagreements per month"; sec 5.2 tests | MET | Sec 5 item 1 derive-and-compare with mutation case; item 3 "Resolution-shape measurement (rerunnable): the E4 script"; item 5 overlay check |
| **Subtotal** | **4/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence (A) | Variant B | Evidence (B) |
|-----------|-----------|--------------|-----------|--------------|
| IE1 Boundary conditions for collections (empty, single-element, maximum size) | MET | Sec 0 "A hand-edited empty list stays C-02's open item"; sec 3.3 quotes the pinned test "soft exclusion alone: today's behaviour re-admits the only candidate"; sec 4.2 "four distinct Anthropic ids" for seven slots | MET | Sec 2 item 2 "Tier0 is not packaged and is skipped" (empty list); E4 "only Sonnet and Haiku are reachable ... strict leaves two reviewers"; E5 "the only candidate is re-admitted" |
| IE2 State-variable interactions across component boundaries | MET | Sec 3.1 item 3: env `T3Model01..06` with a duplicate versus the repo's two tier-3 models; sec 4.2 INV-L "any tier-file edit changes `tiers_sha256`; `recompute_parity` then reports ... not proven (`reflect_shadow_exit.py:128-132`)"; random slot pool changes when an id is added to tier4 (`panel.py:544-545`) | MET | Sec 2 item 3 `select_env` reads `$T3Model01` while the same env decides what the shim serves; E9(c) "an env overlay gives a different hash per workspace ... needs frozen tiers in goldens" |
| IE3 Guard-condition gaps (missing validation, unguarded type assumptions) | MET | Sec 3.4 "the key set of an environment entry is closed (`panel.py:371-373`), so `validate_tiers` gains the key"; sec 2.4 "the reflect profile rejects any reachable model without [a class]: `panel.py:124-125`"; sec 3.3 "A fixed-anchor exhaustion is fatal" | MET | E4 "a non-fixed slot with no candidate is skipped, not failed (`panel.py:647-656`) ... 'A shortfall fails loudly' therefore needs a new raise rule"; sec 2 item 3 FX-14 reading `$T3Model01` alone as a portability exposure; E6 "a missing slot fails loudly" |
| IE4 Count divergence (off-by-one, inclusive/exclusive ranges) | MET | Sec 2.3 item 2 `expected` and `shortfall = expected - len(reviewers)` "following the same `expand` rule: `panel.py:600-605`, so a re-review expects 1"; sec 3.1 item 4 list lengths "2, 3, 6, 4, 2, 3 equal `len(models_env)`" | MET | Sec 2 item 5 `requested_slots` "(the count the template declares for this kind)"; sec 5 item 2 "`requested_slots` equals the template-expanded count (4 for `default`, 7 for `live7`) while `len(reviewers)` is 2 in anthropic-only under strict"; item 1 length equals `len(models_env)` |
| IE5 Interaction effects when features or components combine | MET | Sec 4.2 strict flip combined with the spec loop's un-flagged `panel resolve` call and a lagging prompt copy; sec 3.5 scarcest-first order combined with pinned strict reflect results ("I measured nothing for it"); `vendors` lookup versus substring table parity test (sec 5.2) | MET | Sec 2 item 5 additive keys combined with the byte-identity golden ("so the byte-identity golden test keeps passing"); sec 8 strict-by-default combined with C-03's floor `min(2, requested)`; E9 overlay combined with `tiers_sha256` goldens |
| **Subtotal** | **5/5** | | **5/5** | |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|-----------|-----------|-----------|
| Completeness | 5/5 | 4/5 |
| Correctness | 1/5 | 3/5 |
| Structure | 5/5 | 4/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 4/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **24/30 = 0.8000** | **24/30 = 0.8000** |

Verdict count (MET / NOT MET of 30): Variant A 24 / 6; Variant B 24 / 6.
NOT MET list: A = K1, K2, K3, K4, RK2, L4. B = C1, K1, K4, S1, RK2, L4.

### Edge Case Floor Check

| Variant | Invariant & Edge Case Coverage | Floor (>= 1/5) | Eligible as base |
|---------|-------------------------------|----------------|------------------|
| A | 5/5 | Pass | Yes |
| B | 5/5 | Pass | Yes |

### Position-Bias Mitigation

This is pass 1 only (input order A then B). The reverse-order pass is done independently by the other scorer; no pass-2 output was read. The per-criterion agreement table and any re-evaluation belong to the merge of the two passes, so no Pass 2 / Agreement columns are filled here.

Verdicts that are most sensitive to evaluator judgment (candidates for a pass-2 disagreement): K2 (A and B), K3 (A), S1 (B), RK2 (A and B), L4 (A and B). Reasoning for each is in its Evidence cell.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| A (variant-1-original) | 0.4812 (0.9624 x 0.5) | 0.4000 (0.8000 x 0.5) | **0.8812** | 2 pure wins (C-010, X-005; C-007 contested) |
| B (variant-2-original) | 0.4783 (0.9567 x 0.5) | 0.4000 (0.8000 x 0.5) | **0.8783** | 6 pure wins (C-002, C-003, C-006, C-009, X-006, X-007); 9 hybrid, 8 neither/qualify |

**Margin**: 0.0028 (0.28 percentage points; A ahead) - below the 5% threshold.
**Tiebreaker applied**: Yes.

Tiebreaker walk (protocol A.4):

1. Debate performance (scoring matrix in `debate-transcript.md`, "Pure wins"): Variant B 6, Variant A 2. B wins this step.
2. Correctness criteria count (only needed if step 1 were tied): B 3/5, A 1/5. Same direction.
3. Input order: not reached (A would win it).

So by the protocol the tiebreaker selects Variant B.

## Selected Base: Variant B (variant-2-original.md)

### Selection Rationale

The 0.28-point score margin is not a real difference. A's lead comes from the quantitative layer only: requirement coverage (A 20/20 versus B 19/20, B missing the E2 ladder) and section-count parity, offset by A's two dangling cross-references (DC 0.8824) and weaker consistency density. The qualitative layer is a 24/30 tie, with A ahead on Completeness and Structure and B ahead on Correctness (3/5 versus 1/5). Correctness is the dimension that matters most for a proposal that will be used as a base, and the debate agrees: the points where one variant clearly beat the other went to B six times (ordered derive-and-compare, soft default, class and vendor treatment, spec-loop prompt untouched, "single source" overclaim, spec-loop exposure) against two for A (no env overlay, the resolver reads the packaged list). The debate also showed that A's headline additions (strict default, `--allow-repeat`, `vendors` map, marker list, stderr line, resolve-time exit rule, prompt edit) were withdrawn by A itself, so the base text as written carries more to remove than B's does.

### Strengths to Preserve from Base (Variant B)

1. Ordered derive-and-compare guard for all six tiers against the `MODEL-TIERS.md` section 1 table and `len(models_env)` (sec 2 item 2, sec 5 item 1); the debate's best idea (C-002, 90%, adopted by A).
2. Soft default with strict by declaration, and the evidence that shipped tests pin it (sec 2 item 4, E5), including the reflect `--strict-distinct` call at `SKILL.md:340`.
3. Additive `requested_slots` and `distinct_models` keys written only when asked, which keep the byte-identity golden (sec 2 item 5), serving as the denominator for C-02 INV-001 and C-03 INV-007.
4. No vocabulary merge for class and vendor: one parity test plus the declared-extras subset check (sec 2 item 6), and the observation that `ccsession-models.json` has one `claude` profile so classes cannot be derived from it.
5. Named weakest layer (the env overlay, E9) and the explicit dependence section on C-01..C-03 (sec 8).
6. Served-versus-requested identity caveat (E8) and the lens-per-reviewer cap for rf-qa (sec 6).

### Strengths to Incorporate from Non-Base Variant (Variant A)

1. Scarcest-tier-first slot order, measured: gateway repeats drop to 0 and panels stay full at 4 and 7 (A sec 3.3 third bullet; diff U-001). Use the debate's repaired key (servable-candidate count), not `len(models)`; the sort key stays unresolved (C-007).
2. The E2 fallback ladder as a pure function of (tier, model) over the tier lists, with the reason a model-keyed map cannot say which tier's successor it means (A sec 2.1 last row, 3.4; diff U-002). This fills B's one missing requirement (R3).
3. A's "today versus under A" ownership table (sec 2.1) as the presentation of B's ownership statement, plus the layering note that `find_path` already supports whole-file replacement.
4. Measurements M1 (soft versus strict versus declared repeat on ground truth) and M3 (drift between sources) and the explicit concession that the single-source claim and the strictness default can be judged apart (A sec 5.1, 7.4; diff U-003).
5. The observation that env, ccsession and package already disagree before slot-list filtering (A sec 3.1 item 3), and the union ember edit list (`test_ccsession_tiers.py:222` from B; packaged list edit, `classes`, `names` from A).
6. Candour items: A sec 4.2 "I do not call that 'pins unmodified'" and sec 0's one exact difference from C-01 condition 3.

### Evidence limits of this pass

- Counting units for IC, SR and DC are reading-based; the unit definition is stated so another scorer can re-derive them. A different unit definition moves IC and SR by about 0.01 and cannot change the sign of the margin outcome, because the tiebreaker rather than the score decides.
- Code read this session: `panel.py:594-707` (soft re-admission, `skipped_slots` only under `hard_exclude or strict_distinct`, fixed-anchor raise, resolver reads `tiers["aliases"][slot["tier"]]["models"]` at line 615), `tests/unit/test_ccsession_tiers.py:216-222` (tier4 pinned to three slots), `tests/review/test_review_cli.py:52-61` (default call pinned at four reviewers). Measurement counts (18/40, 30/40, 345/1000, 693/1000) were not re-run by me; they are taken from the diff analyst's reproduction (V-1) and both advocates' runs.
- Not read by me: the E2 branch tip, `COMBO-REPORT.md`, shim internals, research files R04 and r17 (both variants and the debate cite them).

Status: Complete

