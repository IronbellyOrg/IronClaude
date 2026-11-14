# Scoring Re-evaluation: slot C-10 pr-review-wire-format-and-slot

Scorer: re-evaluation (third, neutral). Variant A = `variant-1-original.md` (adapter now, separate pre-step). Variant B = `variant-2-original.md` (one wire format, panel as third reviewer).
Inputs read: `scoring-pass1.md`, `scoring-pass2.md`, `variant-1-original.md`, `variant-2-original.md`, `diff-analysis.md`, `scoring-protocol.md` (A.1 to A.5). Nothing in the repository was modified and no test was run. Checks made this session were Grep passes over the two variant files only (hedge-word list, label first uses, GQ-179, GQ-182, the research/13 lean, reply and resolve, run-1 mentions).

## Disagreement log

### Position-by-position comparison of the verdict strings

Criterion order is the protocol's (A.2). Both passes' tables follow it, so the string positions line up with the tables. Clarity: 1 Unambiguous language, 2 Concrete rather than abstract, 3 Clear section purpose, 4 Terms defined on first use, 5 Actionable next steps.

| Dimension | Variant | Pass 1 string | Pass 2 string | Differing positions |
|---|---|---|---|---|
| Completeness | A | 01111 | 01111 | none |
| Completeness | B | 01111 | 01111 | none |
| Correctness | A | 00101 | 00101 | none |
| Correctness | B | 01001 | 01001 | none |
| Structure | A | 11111 | 11111 | none |
| Structure | B | 11111 | 11111 | none |
| Clarity | A | 11111 | 01101 | 1 and 4 |
| Clarity | B | 11111 | 01101 | 1 and 4 |
| Risk Coverage | A | 00001 | 00111 | 3 and 4 |
| Risk Coverage | B | 00111 | 00111 | none |
| Invariant & Edge Case | A | 10111 | 11111 | 2 |
| Invariant & Edge Case | B | 11111 | 11111 | none |

Correction to the task caution: the Clarity positions that differ are 1 (Unambiguous language) and 4 (Terms defined on first use), not 2 and 5. Position 2 (Concrete rather than abstract) and position 5 (Actionable next steps) are MET in both passes for both variants. Both passes' Clarity tables agree with their own strings, so no criterion text mix-up exists in the strings.

### Disagreement table

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Clarity 1 Unambiguous language | A | MET | NOT MET | disagree | MET |
| Clarity 4 Terms defined on first use | A | MET | NOT MET | disagree | NOT MET |
| Risk 3 Failure modes and recovery | A | NOT MET | MET | disagree | MET |
| Risk 4 External dependencies and their failure | A | NOT MET | MET | disagree | MET |
| Invariant 2 State interactions across components | A | NOT MET | MET | disagree | MET |
| Clarity 1 Unambiguous language | B | MET | NOT MET | disagree | MET |
| Clarity 4 Terms defined on first use | B | MET | NOT MET | disagree | MET |

disagreements_found=7 verdicts_changed=7 of 60 pairs

Reading of the count line: 30 criteria times 2 variants is 60 pairs. 53 pairs agree and keep their verdict. Each of the 7 disagreeing pairs necessarily departs from one of the two passes, so verdicts_changed is 7 (counted as: final differs from at least one pass). Split: 4 finals depart from Pass 1 (A Clarity 4, A Risk 3, A Risk 4, A Invariant 2) and 3 finals depart from Pass 2 (A Clarity 1, B Clarity 1, B Clarity 4).

### Re-evaluation of each pair (protocol A.5 comparison; the verdict here is final)

Prompt applied to each pair: two independent evaluations disagree on this criterion for this variant; Pass 1 evidence and verdict, Pass 2 evidence and verdict, re-evaluate with both. One standard is stated per criterion and applied to both variants.

#### Clarity 1, Unambiguous language (Variant A and Variant B, decided together)

Standard: the criterion tests wording ("no should consider, might, as appropriate"). A design choice that the text says plainly is open is judged under Clarity 5 (decision points), not here. NOT MET needs a hedge phrase, or an assertion that can be read two ways.

- Pass 1 (A and B, MET): the hedge-list search returns 0 hits; unknowns are stated as unknowns.
- Pass 2 (A and B, NOT MET): choices left open (A: "set from cluster facts (for example `disputed`) or left `None`"; B: "B states both and does not decide the threshold", "a pre-registered fraction").

CLAIM: Clarity 1 is met in Variant A and in Variant B.
EVIDENCE: my Grep of both files for should consider, might, as appropriate, as needed, properly, adequate, various, etc., best practice returned no hit in either file. Open items are worded as open: A line 66 "I did not open it and do not state what it asserts", A line 74 "Endangered or left open by A (stated, not resolved here)"; B line 97 "B has NOT decided what pr-submit does with panel findings", B line 125 "OPEN", B line 50 "B states both and does not decide the threshold". Unquantified degree words exist in both and are symmetric: A "cheap" (line 45), "some" (line 103), "a large share" (line 105), "small" (line 120); B "a pre-registered fraction" (line 103). They are not on the protocol list, each sits in a falsifier whose rule is otherwise clear, and neither document is ambiguous about which rule applies.
VERDICT: MET for A and MET for B. Pass 2's NOT MET is overturned for both. The open choices stay scored under Clarity 5, where both are MET (agreed).

#### Clarity 4, Terms defined on first use (Variant A)

Standard: a project-internal label (INV-x, C-0x, M-n, GQ, OQ, T-x, S-n) counts as defined on first use when the header, or the clause in which it first appears, says what it is. Standard industry acronyms (FSM, SARIF) are excluded for both variants. NOT MET needs one verified label with neither a header definition nor a clause gloss.

- Pass 1 (MET): header line 9 defines the shorthand; first uses carry glosses.
- Pass 2 (NOT MET): lists FX-5, M4, M10, M11, GQ-177, OQ-9, S1-S5, T-a, INV-G, INV-J, SARIF as unglossed.

CLAIM: Clarity 4 is not met in Variant A.
EVIDENCE: I checked each of Pass 2's terms in the file. Glossed at first use: FX-5 (line 13 "module-declared vocabularies per the decided FX-5"), M4 (line 18 "an optional per-slot lens (M4, r13:217)"), M11 (line 111 "normalised output adapter spec"), M10 (line 111 "the panel stays pure (M10, INV-E)"), GQ-177 and OQ-9 (line 78 "cost unmeasured (GQ-177, OQ-9)"), T-a (line 19 quotes the trigger), INV-G (line 75 "mutually blind and mechanically read-only reviewers"), INV-J (explained in its own bullet, line 76). Not glossed: S1-S5, line 76 "it must be written once and reviewed against S1-S5". My Grep finds that single occurrence in the file; header line 9 defines only r13, S05, S06, UC and R-C01 to R-C03. A reader cannot tell what the table is to be reviewed against.
VERDICT: NOT MET for A. Pass 1's MET is overturned; Pass 2's NOT MET stands for the reason above, not for the longer list it gave.

#### Clarity 4, Terms defined on first use (Variant B)

Same standard as above.

- Pass 1 (MET): header tags legend; glosses at first use ("CO-27 (wire format), CO-29 (slot)", "C-06 (repair policy)", "R13 is research/13").
- Pass 2 (NOT MET): INV-E appears in section 1 before its section 5 row; OQ-18, GQ-177, C-01 to C-08, M10, P1, P7, P8, P12, FSM undefined.

CLAIM: Clarity 4 is met in Variant B.
EVIDENCE: INV-E is glossed in the sentence that first uses it (line 10: "the fork-only checks and the 'no `gh` / `git` in the core' rule stay untouched (INV-E)"). OQ-18 and GQ-177 sit under "Measurement the debate needs and does not have (OQ-18 / GQ-177; never measured)" (line 100). C-01 to C-03 are rows of the line 16 table; C-06 is glossed "(repair policy)" (line 18); C-08 is glossed "until the transport records `model_observed` (C-08)" (line 20). M10 is glossed by its clause (line 29: "The core stays free of `gh`, `git`, network and repository constants (M10)"). P1, P7, P8, P12 are always attached to `research/13` and to the claim they support (for example line 80 "the PR flow ignores the panel verdict (R13 P12)"). R13 is defined on line 54. FSM is a standard acronym, excluded as for A. I found no project-internal label in B with neither a definition nor a clause gloss. The M1 to M3 collision (B section 6 versus section 7) is a consistency defect and is already scored in Correctness 3 (NOT MET, agreed) and in the DC metric; it is not scored twice.
VERDICT: MET for B. Pass 2's NOT MET is overturned.

#### Risk 3, Failure modes and recovery procedures (Variant A)

Standard: MET when the variant names a failure mode of its own design and states a defined non-clean outcome for it plus what happens next (continue, re-run or resume). A missing staleness rule is scored under Invariant 2 and Completeness, not here. B's agreed MET rests on the same two parts: item 6 maps `truncated`, `invalid`, `failed`, `timed_out` to `incomplete`, and a re-run on a new head SHA re-establishes presence (item 3 a2). B states no longer recovery procedure than A does.

- Pass 1 (NOT MET): no recovery or resume path; staleness not addressed.
- Pass 2 (MET): INV-I, "visible, never clean", item 7 three outputs.

CLAIM: Risk 3 is met in Variant A.
EVIDENCE: failure mode and non-clean outcome: A line 25 "'panel did not complete' is a third state that is never read as 'clean' (INV-I ...)"; line 72 "the adapter never maps 'no result' to 'no findings'"; line 107 "a test that a pre-step failure, a quorum shortfall and a clean panel produce three different outputs". What happens next: line 94 "the PR case is 'visible, never clean', because the bots still run" (the PR flow continues on the bots); line 78 "A makes the pre-step optional and outside the round counter; if the owner wants a panel re-run after each fix push, the pre-step needs a cycle id" (the re-run path and its missing key are named).
VERDICT: MET for A. Pass 1's NOT MET is overturned. The thinness of the recovery path is the same in B.

#### Risk 4, External dependencies and their failure scenarios (Variant A)

Standard: MET when the variant names a dependency outside its own control (the bots, a prior-slot outcome, a later slot, the model transport) and says what its design does or loses if that dependency fails or changes. The bots-silent omission is the R-16 gap, already scored in Completeness 1 (NOT MET for both, agreed); it is not scored again here. B's agreed MET rests on O3 (OPEN), the C-01 key closure ("B would need a registered key list"), C-06 and C-08.

- Pass 1 (NOT MET): the bots-silent case with panel findings is absent.
- Pass 2 (MET): convergence trigger firing, INV-007 dependency on C-03, "requested, not served" until C-08.

CLAIM: Risk 4 is met in Variant A.
EVIDENCE: A line 84 "If one of R-C01's convergence triggers fires (T-a, T-b, T-c) ... A's claim that 'PR never needs the ledger' would stop being a benefit"; line 90 "If R-C02's CRITICAL floor were dropped, the adapter's table would still need that row"; line 94 INV-007 (`requested` can collapse to 1; the pre-step must pass the resolution); line 96 "Independence is 'requested, not served' until C-08 records `model_observed`"; line 122 describes the bots as "external actors observed through GitHub (identities, markers, silence timeouts, re-trigger phrases)". Each names a dependency and what A loses or must add if it changes.
VERDICT: MET for A. Pass 1's NOT MET is overturned.

#### Invariant 2, State variable interactions across component boundaries (Variant A)

Standard: MET when the variant identifies a state variable that crosses a component boundary (panel presence, bot reviewer state, round counter, head SHA, gate-block variables) and states a rule for its own design on how the two sides interact. An interaction named but left open is a limit. The same test applies to B: B states rules (item 3 a2 head SHA, item 3 b `no_response` kept on the two bots) and leaves `terminal_clean` untraced (B line 135); A also leaves `terminal_clean` untraced, so that gap cancels.

- Pass 1 (NOT MET): head-SHA binding and staleness unspecified (A-008); `terminal_clean` interaction untraced.
- Pass 2 (MET): gate-block variables, "needs a cycle id".

CLAIM: Invariant 2 is met in Variant A.
EVIDENCE: A line 25 "reported as its own presence state next to the bot `reviewers` object, never inside it" (panel state kept apart from bot state by rule); line 44 per-reviewer variables `watermark`, `codex_watermark`, `review_state` live in the one executable gate block that a test namespace executes, so the pre-step stays outside it; line 78 the panel sits "outside the round counter" and a per-push re-run "needs a cycle id"; line 107 "none of them changes the existing `reviewers` object". The staleness rule after a fix push is named but not specified (A-008): recorded as a limit, not scored again.
VERDICT: MET for A. Pass 1's NOT MET is overturned, with the staleness limit recorded.

## Final qualitative

Basis column: agreed means both passes gave the same verdict and it is kept without reopening; re-evaluated means one of the 7 disagreement pairs above.

| Dimension | Criterion | Variant A | Variant B | Basis |
|---|---|---|---|---|
| Completeness | 1 Covers all explicit requirements | NOT MET | NOT MET | agreed (A misses R-16; B misses R-16 and R-14 under the quantitative rule below) |
| Completeness | 2 Edge cases and failure scenarios | MET | MET | agreed |
| Completeness | 3 Dependencies and prerequisites | MET | MET | agreed |
| Completeness | 4 Success or completion criteria | MET | MET | agreed |
| Completeness | 5 Out of scope stated | MET | MET | agreed |
| Correctness | 1 No factual errors | NOT MET | NOT MET | agreed |
| Correctness | 2 Feasible within stated constraints | NOT MET | MET | agreed |
| Correctness | 3 Terminology consistent | MET | NOT MET | agreed |
| Correctness | 4 No internal contradictions | NOT MET | NOT MET | agreed |
| Correctness | 5 Claims supported | MET | MET | agreed |
| Structure | 1 Logical ordering | MET | MET | agreed |
| Structure | 2 Hierarchy depth | MET | MET | agreed |
| Structure | 3 Separation of concerns | MET | MET | agreed |
| Structure | 4 Navigation aids | MET | MET | agreed |
| Structure | 5 Artifact-type conventions | MET | MET | agreed |
| Clarity | 1 Unambiguous language | MET | MET | re-evaluated (A and B) |
| Clarity | 2 Concrete rather than abstract | MET | MET | agreed |
| Clarity | 3 Clear section purpose | MET | MET | agreed |
| Clarity | 4 Terms defined on first use | NOT MET | MET | re-evaluated (A and B) |
| Clarity | 5 Actionable next steps | MET | MET | agreed |
| Risk Coverage | 1 At least 3 risks with probability and impact | NOT MET | NOT MET | agreed |
| Risk Coverage | 2 Mitigation for each risk | NOT MET | NOT MET | agreed |
| Risk Coverage | 3 Failure modes and recovery | MET | MET | re-evaluated (A); B agreed |
| Risk Coverage | 4 External dependencies and failure | MET | MET | re-evaluated (A); B agreed |
| Risk Coverage | 5 Monitoring or validation mechanism | MET | MET | agreed |
| Invariant & Edge Case | 1 Collection boundaries | MET | MET | agreed |
| Invariant & Edge Case | 2 State interactions across components | MET | MET | re-evaluated (A); B agreed |
| Invariant & Edge Case | 3 Guard condition gaps | MET | MET | agreed |
| Invariant & Edge Case | 4 Count divergence | MET | MET | agreed |
| Invariant & Edge Case | 5 Interaction effects | MET | MET | agreed |

### Subtotals

| Dimension | Variant A (of 5) | Variant B (of 5) |
|---|---|---|
| Completeness | 4 | 4 |
| Correctness | 2 | 2 |
| Structure | 5 | 5 |
| Clarity | 4 | 5 |
| Risk Coverage | 3 | 3 |
| Invariant & Edge Case | 5 | 5 |
| Total met | 23 | 24 |
| qual_score (met / 30) | 0.7667 (23/30) | 0.8000 (24/30) |

Edge case floor: A 5 of 5 and B 5 of 5, both at or above 1 of 5, both eligible as base; the floor is not suspended.

Final verdict strings (positions in protocol order):
- A: Completeness:01111;Correctness:00101;Structure:11111;Clarity:11101;Risk:00111;Invariant:11111
- B: Completeness:01111;Correctness:01001;Structure:11111;Clarity:11111;Risk:00111;Invariant:11111

## Final quantitative

Why the passes differed: the metrics are meant to be mechanical, but the passes used different units. Pass 1 counted every independent tagged fact inside a bullet (98 and 110 claims) and judged vagueness per sub-clause by eye; Pass 2 counted one claim per item (58 and 56, with section 7 of A and the Limits section of B left out) and judged vagueness by whether the main assertion was "undecided". Each pass also applied a different standard to R-14 and R-16. Below, one rule per metric is stated and applied to both variants, with raw counts shown.

### RC: requirement coverage

Rule: the 17 requirements R-01 to R-17 are those of `diff-analysis.md` (final table). A variant matches a requirement only when its own text states every element the requirement lists, in its own words (explicit content). An ID or a document name is neither needed nor enough. A requirement that is only partly stated is not matched (binary, as the protocol has no partial credit for RC). This is the same standard I used for R-14 and R-16.

Elements of the two reopened requirements:
- R-14: (1) wire format versus adapter (GQ-179), (2) third reviewer name versus separate pre-step (GQ-182), (3) the research/13 lean "adapter now, extensible v2 later".
- R-16: (1) flow through Wave 2 to Wave 4, (2) reply, (3) resolve, (4) the bots-silent case.

| Req | Variant A | Variant B | Basis |
|---|---|---|---|
| R-01 | match | match | A section 1 and 4 (INV-E); B section 1 and 5 (INV-E row) |
| R-02 | match | match | A section 3.3 (12 lines in 3 files, "not run"); B rows B11 and B12 (47 files, static reading) |
| R-03 | match | match | A sections 4 and 6 item 6; B section 6 M1 |
| R-04 | match | match | A section 4 (INV-E HIGH, INV-F MEDIUM, INV-C); B section 5 rows |
| R-05 | match | match | A sections 2 and 3.1; B sections 3.1 item 1, 3.2 item 2, 3.4 |
| R-06 | match | match | A section 5; B section 2 table |
| R-07 | match | match | A section 2 and INV-I, section 5 C-03 bullet; B section 3.2 item 6 |
| R-08 | match | match | A section 2 (SKILL.md:47-49); B section 3.3 |
| R-09 | match | match | A section 6; B section 6 |
| R-10 | match | match | A section 7; B section 7 |
| R-11 | match | match | A section 8; B section 8 |
| R-12 | match | match | A section 5 C-03 last bullet; B section 2 C-03 row |
| R-13 | match | match | INV-F in both |
| R-14 | match | no match | A has all three elements: (1) sections 1, 3.1, 8; (2) sections 3.3, 8; (3) line 1 "position A (adapter now)" with line 13 "a later move to one wire format stays open" and line 121 "promoted to the core only when a second consumer needs it". B has (1) and (2) (sections 1, 3.2, 8) but never states or answers the lean: Grep for lean, extensible, adapter now, v2 later returns no hit in B. |
| R-15 | match | match | A section 2 (adapter owns the four) and 3.4; B sections 1, 3.2 item 1 and 2, M2 |
| R-16 | no match | no match | A has element (1) only, as one sentence (line 60 "Panel findings enter that same path"). B has (1) (section 3.3) and (4) as an OPEN item (O3, line 125), but not (2) or (3): the only "reply" in B (line 104) is about a later step reading a quote, and its "resolve" (line 19) is PR round thread resolution; A's "resolve" (line 111) is a list mention of outward actions that stay in `pr_submit`. |
| R-17 | match | match | A line 7 states no run-1 file was cited; Grep of both files finds no run-1 citation |
| Total | 16 of 17 | 15 of 17 | |

Decision on the two settled items: R-14 is decided by explicit content with all three elements, so A matches and B does not. R-16 is decided by the same rule, so neither matches. Under this rule B is not credited for naming the bots-silent case as OPEN, because R-16 also lists reply and resolve; that also keeps RC consistent with Completeness 1, where both passes agreed NOT MET for both variants. The 13 other requirements that both passes counted as matches for both variants were spot-checked element by element and no listed element is missing in either variant, so they stay matched (agreed).

RC_A = 16/17 = 0.9412. RC_B = 15/17 = 0.8824.

### IC: internal consistency

Rule: a scorable claim (unit) is one list item, one table body row, or one body paragraph in the numbered sections that asserts a falsifiable fact or a design commitment. Excluded: headings and the A "3.x" subsection title lines, Status lines, header metadata, the Tags and Citation shorthand legends, and lines that only introduce a list or table. A contradiction is a pair of statements inside the same variant that oppose each other or break a stated constraint. Each contradiction is counted once, whatever number of units it touches. IC = 1 - contradictions / units.

| Section | A units | B units |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 7 | 3 |
| 3 (A: 3.1 to 3.7; B: 3.1 to 3.5) | 16 | 13 |
| 4 | 11 | 14 |
| 5 | 10 | 12 |
| 6 | 7 | 7 |
| 7 | 2 | 2 |
| 8 | 5 | 9 |
| 9 | none | 6 |
| Total | 59 | 67 |

Contradictions: the 4 of A and 3 of B that both passes found are used (agreed). I re-read each pair in the texts; no extra one is added.
- A1: line 18 "No change to `findings.py`, `findings_v2.py`, `cluster.py`" and line 20 the adapter reads "the highest member severity", while line 54 lists the cluster keys the adapter reads (no severity or category). A requirement-constraint conflict that the code confirms (diff-analysis X-001).
- A2: line 101 "no edit to any existing test file (only new test files added)" versus line 102 "Add the module to the static no-shell-token check" (an edit to the module list in `tests/pr_submit/test_static_grep.py`, diff-analysis C-003; A conceded it in the debate).
- A3: line 121 "downstream only reads `path`, `line`, `body`, `category` and the route" versus line 49, where A itself cites `fsm.py:902-906` as a reader of `in_diff`.
- A4: line 24 the adapter sets `confidence` "from cluster facts (for example `disputed`)" versus line 50 (a fourth `confidence` meaning needs a type chosen) and line 90 (a CRITICAL is never lowered; router step 3 lowers a tier on low confidence). The weakest of the seven because it is conditional; kept because both passes counted it.
- B1: line 66 "A third name reuses this bookkeeping" versus line 35 (a2), which excludes the panel from the re-trigger path and `reviewer_activity`.
- B2: line 20 "B does not call `merge_round`" versus lines 20 and 38, which derive `incomplete` from "a C-03 quorum refusal" that lives in `merge_round`.
- B3: line 58 "Any converter that builds a `Finding` drops them at the conversion point" (and line 65, B8) versus lines 33 and 34, where B's own reader builds a slot-less `Finding` from `citations[0]` and `claim`.

IC_A = 1 - 4/59 = 0.9322. IC_B = 1 - 3/67 = 0.9552.

### SR: specificity ratio

Rule: this is the protocol's closed, grep-checkable test, applied to the same units as IC. Concrete unit: contains at least one number, file:line citation, named code identifier or named entity or threshold. Vague unit: contains a protocol vague indicator (appropriate, as needed, properly, adequate, should consider, might, various, etc., best practices, industry standard without citation). SR = concrete / (concrete + vague).

Raw counts: A 59 concrete, 0 vague. B 67 concrete, 0 vague. My Grep for the indicator list returned no hit in either file; every unit in both files carries a citation, identifier, label or number.

SR_A = 59/59 = 1.0000. SR_B = 67/67 = 1.0000.

Sensitivity (not used in the score): if unquantified degree words are also counted as vague units (A: lines 45, 66, 103, 105, 120 = 5 units; B: line 103 = 1 unit), SR_A = 54/59 = 0.9153 and SR_B = 66/67 = 0.9851. The ranking does not change (see Combined).

### DC: dependency completeness

Rule: an internal reference is a reference, in a sentence of the document, to a section number, numbered item, table row label or defined label of the same document. A reference to a label of another document (r13 or R13, research/13, S05 and S06, UC, R-C01 to R-C03, other slots) is external and excluded when the sentence names the other document. A bare label that the document does not define, with no named external document in its sentence, is counted as an unresolved internal reference. A reference resolves when its target exists in the document and the label is used in the sense the document defines. A group (a list or a range such as "B1 to B8") is one reference. Section-number references resolve by the existence of the section.

Variant A: 12 references, 10 resolve.
- Resolved (10): INV-I (line 25); "per 3.3" (line 77); "(3.1)" (line 84); INV-E (line 111); "(3.5)", "(3.2)", "(6.2)", "(3.1)", "(3.4)" (line 120); "(3.3)" (line 122).
- Unresolved (2): "S1-S5" (line 76; defined nowhere; no document named in its sentence); "M10" (line 111; bare, defined nowhere in A).

Variant B: 34 references, 30 resolve.
- Resolved (30): INV-E (line 10); "section 3.2 item 3 and 6" (line 20); "(B1)" (lines 65 and 104); "(section 3.2)" (line 70); "section 3.2 item 3b" (lines 88 and 125); "section 6, T3" (line 88); "section 8, objection 3" (line 97, resolves to O3); "B5/B6" (line 98); "(B4)" and "(M1)" (line 108); "B13" and "B2" (line 114); "B2", "B1" and "B14" (line 118); "B13", "B10", "B9" and "M1" (line 119); "B1 to B8" and "B9, B10, B13" (line 120); "M2 measures it" (line 124); "section 3.5" (line 127); "section 3.4" and "option (i)" (line 128); "(B11)" and "(T2 is the run)" (line 132); "B10, second half" (line 135).
- Unresolved (4): "M10" (line 29; bare, defined nowhere in B); "what M2 already requires" and "M2 is a decided requirement" (line 110) and "the decided M2 requirement" (line 118), which use M2 in the research/13 sense while B section 6 defines M2 as the `in_diff` precision measurement (label collision).

Decision on the items the task named: A "S1-S5" counts as unresolved. B "M10" counts as unresolved. The B M1/M2 collision counts as unresolved for M2 (3 references); the one M1 use in the research/13 sense (line 10) names research/13 and is external, and the M1 uses in lines 108 and 119 match B's own definition, so M1 resolves. A's bare "M10" is an extra I found on the same rule and counts, so A is not favoured over B. B's "(M10)" and A's "(M10, INV-E)" are treated the same way.

DC_A = 10/12 = 0.8333. DC_B = 30/34 = 0.8824.

### SC: section coverage

Rule: count the H2 headings of the numbered sections; SC = count / max over both variants. A has 8 H2 (sections 1 to 8). B has 9 H2 (sections 1 to 9). Max = 9.

SC_A = 8/9 = 0.8889. SC_B = 9/9 = 1.0000.

### Quantitative table

| Metric | Weight | Variant A raw counts | Variant A score | Variant B raw counts | Variant B score |
|---|---|---|---|---|---|
| RC | 0.30 | 16 of 17 requirements matched | 0.9412 | 15 of 17 requirements matched | 0.8824 |
| IC | 0.25 | 4 contradictions in 59 units | 0.9322 | 3 contradictions in 67 units | 0.9552 |
| SR | 0.15 | 59 concrete, 0 vague | 1.0000 | 67 concrete, 0 vague | 1.0000 |
| DC | 0.15 | 10 of 12 references resolve | 0.8333 | 30 of 34 references resolve | 0.8824 |
| SC | 0.15 | 8 H2 of max 9 | 0.8889 | 9 H2 of max 9 | 1.0000 |
| quant_score | 1.00 | 0.2824 + 0.2331 + 0.1500 + 0.1250 + 0.1333 | 0.9237 | 0.2647 + 0.2388 + 0.1500 + 0.1324 + 0.1500 | 0.9359 |

Arithmetic (unrounded): A = 0.30 x 0.941176 + 0.25 x 0.932203 + 0.15 x 1.000000 + 0.15 x 0.833333 + 0.15 x 0.888889 = 0.923737. B = 0.30 x 0.882353 + 0.25 x 0.955224 + 0.15 x 1.000000 + 0.15 x 0.882353 + 0.15 x 1.000000 = 0.935865.

Sensitivity of the quantitative inputs (the Combined section shows each stays below the 0.05 margin): (a) IC_A if A1 is treated as a code error and not an internal contradiction: 1 - 3/59 = 0.9492. (b) IC_B without the Limits section: 1 - 3/61 = 0.9508. (c) RC under the looser "topic and axes" reading that Pass 1 used (B matches R-14 and R-16): RC_B = 17/17 = 1.0000, RC_A = 16/17.

## Combined

Formula (protocol A.3): combined = 0.50 x quant_score + 0.50 x qual_score.

| Variant | quant_score | 0.50 x quant | qual_score | 0.50 x qual | combined |
|---|---|---|---|---|---|
| A (adapter now) | 0.9237 | 0.4619 | 0.7667 (23/30) | 0.3833 | 0.8452 |
| B (one wire format) | 0.9359 | 0.4679 | 0.8000 (24/30) | 0.4000 | 0.8679 |

Margin = |A - B| = |0.8452 - 0.8679| = 0.0227 (unrounded 0.022730). The margin is below 0.05, so the protocol A.4 tiebreaker trigger is met (reported only; this file does not apply the tiebreaker). Data the tiebreaker will need from this file: Correctness criteria met are A 2 and B 2 (tied). Debate performance (diff points won in Step 2) is not computed here.

Margin under each sensitivity named above (each also below 0.05):

| Variant of the rule | combined A | combined B | Margin |
|---|---|---|---|
| Base (this file) | 0.8452 | 0.8679 | 0.0227 |
| IC_A with A1 not counted | 0.8473 | 0.8679 | 0.0206 |
| IC_B without the Limits section | 0.8452 | 0.8674 | 0.0222 |
| RC with Pass 1 reading (B 17 of 17) | 0.8452 | 0.8856 | 0.0404 |
| SR with degree words as vague | 0.8388 | 0.8668 | 0.0280 |

Direction: B leads in every row. The lead comes from qualitative Clarity 4 (A fails on "S1-S5") and from IC, DC and SC; A is ahead on RC only (R-14).

FINAL_SCORES
quant_A=0.9237
quant_B=0.9359
qual_A=23/30
qual_B=24/30
combined_A=0.8452
combined_B=0.8679
dims_A=Completeness 4;Correctness 2;Structure 5;Clarity 4;Risk 3;Invariant 5
dims_B=Completeness 4;Correctness 2;Structure 5;Clarity 5;Risk 3;Invariant 5
disagreements=7 changed=7
END
