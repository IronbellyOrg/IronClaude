# Re-evaluation of position-bias disagreements: slot C-08 (run-record-and-served-model-capture)

Variant 1 = Proposal A (`variant-1-original.md`). Variant 2 = Proposal B (`variant-2-original.md`). Scored as written, not as the debate's hybrid. Rubric: `scoring-protocol.md` A.2 (binary, MET needs a direct quote or section reference) and A.5 (re-evaluation verdict is final). Inputs read: both variants in full, `score-pass1.md`, `score-pass2.md`, `invariant-probe.md` (INV-001, INV-013), `diff-analysis.md` (grep only). Debate-verified code facts are used only as evidence for correctness, and none of the 8 criteria below is a correctness criterion.

Standard applied to every pair, so the two variants are judged alike: a criterion is MET when the paper itself contains a quotable statement that does what the criterion names, even if partial or thin. It is NOT MET when the named element is absent from every section.

## Disagreement 1: V1 invariant_edge_case 1

CLAIM: "Addresses boundary conditions for collections (empty, single-element, maximum size)" is met in Variant 1.

PASS 1 (NOT MET): only the empty case, "incidentally"; no single-reviewer or maximum case; no empty or torn `events.jsonl` treatment.

PASS 2 (MET): section 7 "a consumer that never calls `record add` behaves as today" (empty record); item 21 `last-pass` holds 5 entries against "overwritten whole"; M2 400 lines from eight writers.

EVIDENCE: Variant 1 does name boundaries and attaches a test to two of them. (a) Empty: section 7, "Neither depends on events being present ... a consumer that never calls `record add` behaves as today". (b) Collapse of a collection to one element: item 13 (combo A run 3, `reviewer_requested_served` of `[None, "claude-sonnet-5-5"]` while `calibrator_diversity` is `full`) and M1(b), which requires "mismatch rows between `model_requested` and `model_observed` where the contract printed `calibrator_diversity: full`". (c) Size: M2 "eight processes each run `review record add` 50 times ... all 400 lines are valid JSON with unique `seq`". Pass 1 is right that no maximum-size limit and no torn or empty `events.jsonl` rule is stated (the probe's INV-001 and INV-013 find those unhandled), but the criterion asks whether boundaries are addressed, not whether every one is closed. Pass 2's item 21 citation is a rule-versus-count observation, not a boundary, and is discounted. The remaining three quotes are enough.

FINAL VERDICT: MET (section 7 empty-events sentence; M1(b) one-served-model collapse; M2 400-line contention case).

## Disagreement 2: V1 risk_coverage 1

CLAIM: "Identifies at least 3 risks with probability and impact assessment" is met in Variant 1.

PASS 1 (NOT MET): section 5 names five risks with consequences but no probability; "HIGH" for INV-F is impact only.

PASS 2 (MET): lost update (item 5, 0 in 29 manifests), D-17 fan-out (item 10, 400 versus 200), orchestrator share (item 18, median 0.59), sentence validates in `model.resolved` (item 7). No formal labels in either paper; frequencies and quantified impacts instead.

EVIDENCE: Neither paper has a risk register with probability and impact labels, so a formal-label reading would fail both variants for the same reason. Variant 1 does give a frequency and a quantified consequence for three risks. Lost update: item 5, "two loads, two saves, one attempt lost ... 29 real manifests show no lost attempt", with section 8 answer 2 "a hazard that needs only a parallel batch of Bash calls to trigger". Double counting: item 10, "two live outcomes for one reviewer run double its cost, 400 versus 200 per true positive". Reviewer-only under-reporting: item 18, "0.49 to 0.87 of output tokens ... median 0.59". Section 5 adds "INV-F (HIGH)". Two of the three are tagged [UNVERIFIED], which affects correctness, not whether risk coverage is present.

FINAL VERDICT: MET (item 5, item 10 and item 18 give an observed rate or trigger condition plus a quantified impact for three distinct risks).

## Disagreement 3: V2 clarity 4

CLAIM: "Acronyms and domain terms defined on first use" is met in Variant 2.

PASS 1 (NOT MET): "D-17" and "D-31" undefined, "OQ-3, GQ-215" undefined, "R-23" undefined, INV-F and INV-H glossed only in section 5, after use in section 2.

PASS 2 (MET): section 4 glosses the six decided requirements in one sentence; 5.1 and 5.2 gloss INV-F, INV-H, INV-L; the telemetry row states the D-31 and D-17 rules in the same clause; the header defines the tag set and R-file citations.

EVIDENCE: Variant 2 attaches each ID to its content at first use, unlike Variant 1, whose header line 4 opens with a bare list of 13 IDs (both passes agree V1 is NOT MET). Header: "Research citations use R04, R07, R15, R16, R18 for `research/04-...`" plus the tag rule. Section 2 telemetry row: "Group values are type-checked at append (D-31); one live outcome per `(reviewer_record_id, truth_basis)` is enforced (D-17); strata become a module-registered list (C-S10, already decided)", where each ID follows the rule it names. Section 2 adapter row: "reached only through the `superclaude` CLI (INV-F)", which is INV-F's content. B-21: "R-23: about 25 per-reviewer fields such as hook_calls, msgs_sent, snapshot_missing". "OQ-3, GQ-215" is a citation to open-question records and follows the plain statement "availability across harnesses is open". Pass 1 is right that those two IDs, and "EV-1", are never expanded; that is a residue of record citations, not undefined acronyms in the sense of the criterion, since the sentence carrying each is self-explanatory.

FINAL VERDICT: MET (section 2 telemetry row and adapter row give each ID with its rule at first use; header defines R-citations and tags).

## Disagreement 4: V2 completeness 1

CLAIM: "Covers all explicit requirements from source input" is met in Variant 2.

PASS 1 (NOT MET): OQ-19 (reviewer model actually used, `spec-panel.md:258`) not addressed anywhere; FX-19 only named in the section 4 list; CO-20 (one memory step at publish with a study switch) declined ("Memory keeps its writer").

PASS 2 (MET): section 4 maps every decided requirement to a mechanism; OQ-3 and OQ-23 handled; INV-F/H/A/L covered in section 5.

EVIDENCE: I searched Variant 2 for `OQ-19`, `actually used` and `spec-panel`: no hit in any of sections 1 to 9. The slot's open questions are OQ-19, OQ-21 and OQ-23; Variant 2 answers OQ-21 (section 2 adapter row, INV-F) and OQ-23 (M2, "This also answers OQ-23") and never OQ-19, which Variant 1 answers explicitly at the end of its section 2. Section 2's spec-review loop row ("Has no manifest. Its run record is the telemetry records from `merge`") never ties the producer to the header line that the master reviewer writes. Second, section 4 states the decided requirement "the writer of memory moves to one step at publish with a study switch", and the section 4 bullet then says "Memory: B leaves the writer". That is a reasoned refusal, so it is not a gap in addressing the item, but it means Pass 2's "maps every decided requirement to a mechanism" is wrong for memory. The OQ-19 omission alone is a named explicit requirement with no coverage anywhere. Variant 1 is held NOT MET by both passes for the same kind of omission (the two labelled cost bases), so the same standard gives NOT MET here.

FINAL VERDICT: NOT MET (no evidence found for OQ-19 in sections 1 to 9; section 4 itself records the memory writer requirement as not met by B).

## Disagreement 5: V2 invariant_edge_case 1

CLAIM: "Addresses boundary conditions for collections (empty, single-element, maximum size)" is met in Variant 2.

PASS 1 (NOT MET): only the empty case, only as a measurement (M3 "agents[] is empty").

PASS 2 (MET): M3 measures the share of runs whose `agents[]` is empty; B-18 "9 of 29 real manifests only `collected` attempts exist (no `dispatched` rows)"; B-13 1 of 15 versus 14 of 15.

EVIDENCE: Variant 2 treats the empty collection with a stated failure rule, not only a measurement: section 8 M3 "the share of runs whose `agents[]` is empty because the transcript was unreadable ... Fail for B: ... `agents[]` empty in more than the adapter-unavailable cases"; 7.2.3 "a run killed with no process left to commit `published` or `failed` leaves no `agents[]`"; B-7 "A refused round records nothing today". It also treats a partial collection (B-18, nine manifests with only `collected` attempts) and the collapse to one element (M4: replay A3 so that `calibrator_diversity: full` is flagged, "and a run with all three reviewers served by distinct ids is not flagged"). It states no maximum-size case, which is consistent with Variant 1's thin treatment. Pass 1's "only as a measurement" understates 7.2.3 and B-7, which are behaviours.

FINAL VERDICT: MET (M3 empty `agents[]` with a fail rule; 7.2.3 killed run leaves no `agents[]`; M4 collapsed-versus-distinct served ids).

## Disagreement 6: V2 risk_coverage 1

CLAIM: "Identifies at least 3 risks with probability and impact assessment" is met in Variant 2.

PASS 1 (NOT MET): section 5.2 names three endangered invariants and a residual with guards but no probability; the only frequencies are "0 lost attempts in 29" and "9 of 29" (both [UNVERIFIED]).

PASS 2 (MET): B-16 interleaving (impact) with 0 in 29 (frequency); B-18 9 of 29 call-order loss with impact in 7.1; 5.2 INV-L stale-`rev` refusal.

EVIDENCE: Same standard as Disagreement 2 (no formal labels in either paper; observed frequency plus stated consequence counts). Lost update: B-16, "attempts ends as one reviewer, `reviewers_complete = 1` ... 0 lost attempts in 29 real manifests". Call-order loss: 7.1, "A record that depends on the orchestrator calling the CLI in the right order loses exactly the late, killed and non-reviewer rows where cost leaks", with B-18 "In 9 of 29 real manifests only `collected` attempts exist". Cost mislabelled as estimate: B-19, "orchestrator output-token share is a median 0.59 over 15 runs". This is as good a frequency-plus-impact pairing as Variant 1's, and the 7.1 pair is more explicit than anything in Variant 1.

FINAL VERDICT: MET (B-16, B-18 with 7.1, and B-19 each give a frequency and a consequence).

## Disagreement 7: V2 risk_coverage 2

CLAIM: "Provides mitigation strategy for each identified risk" is met in Variant 2.

PASS 1 (MET): section 5.2 Guard column answers every row; 7.2 mitigates the objection point by point.

PASS 2 (NOT MET): 7.2.3 "Residual B does not close: a run killed with no process left to commit `published` or `failed` leaves no `agents[]`" and 7.2.2 "The orchestrator's tail after `published` is not in the manifest" are identified risks left without mitigation.

EVIDENCE: Each risk Variant 2 names carries a stated step. 5.2: INV-H "closed key sets and typed values ... Extend `test_no_document_text_in_any_record`"; INV-L "re-read, retry once, then record `panel_fallback_reason` and continue as legacy"; `cli/reflect` "If the owner prefers a lint line in `panel_lint.py`, it ... must be treated as a C-01 INV-020 case". The two residuals Pass 2 cites also have one: 7.2.2 "labels the all-agents figure 'through publish'. Where a study needs the tail, it reads the same transcript with the same adapter at analysis time"; 7.2.3 "The adapter can be run later over a manifest left in a non-terminal state, but that is a recovery action". Admitting that a mitigation is partial and out-of-run does not remove it; the rubric asks for a mitigation strategy, not elimination of the risk. 7.2.1 handles the killed attempt ("`failed`, `timed_out` ... `usage_complete: false`"), and 7.3.3 handles memory ("a read-freeze addresses [the read side] without moving the writer"; the script writer stays available "if a lost update ... is ever observed"). Variant 1 is held MET by both passes on comparably partial mitigations (for example "a non-POSIX runner would need a different lock").

FINAL VERDICT: MET (5.2 Guard column; 7.2.2 analysis-time transcript read; 7.2.3 later adapter run as recovery action).

## Disagreement 8: V2 structure 1

CLAIM: "Logical section ordering (prerequisites before dependents)" is met in Variant 2.

PASS 1 (MET): H2 order 1 position, 2 module table, 3 evidence, 4 requirements mapping, 5 invariants, 6 PR/rf-qa, 7 objection, 8 measurements, 9 relation to C-01/C-02/C-03; evidence precedes what relies on it.

PASS 2 (NOT MET): C-01/C-02/C-03 dependencies appear only in section 9 after sections 2, 5.2 and 6 rely on them; measurements (section 8) come after the objection (section 7) "that cites M-results".

EVIDENCE: I searched Variant 2 for `M1` to `M5`: they occur only in section 8 itself (lines 124-128), so section 7 does not cite any measurement result and the "objection cites M-results" premise is false. Section 8's M5 refers back to "objection 3" (a backward reference). Evidence (section 3) precedes the requirements mapping (4), invariants (5) and objection (7) that cite B-n rows. Section 9 is a consistency summary that depends on everything before it; the earlier mentions of C-S10, C-07, C-10, C-12 and "C-01 reading, INV-020" are slot-level context from the source input, glossed at the point of use, not content defined in section 9. The forward pointers ("See section 6", "section 7, objection 3") are navigation, not dependencies. Variant 2 places the adjudication cross-check last where Variant 1 places it third, which is a placement preference; neither order makes a section unreadable without a later one.

FINAL VERDICT: MET (H2 order puts evidence before the sections that cite B-n rows; section 7 cites no section 8 result; section 9 is a terminal summary).

## FINAL

V1|invariant_edge_case|1|MET
V1|risk_coverage|1|MET
V2|clarity|4|MET
V2|completeness|1|NOT MET
V2|invariant_edge_case|1|MET
V2|risk_coverage|1|MET
V2|risk_coverage|2|MET
V2|structure|1|MET

## Summary

| Measure | Count |
|---|---|
| Disagreements found | 8 |
| Verdicts changed from Pass 1 | 5 (1, 2, 3, 5, 6) |
| Verdicts changed from Pass 2 | 3 (4, 7, 8) |

Effect on subtotals if these 8 replace the passes' verdicts: V1 gains one MET over Pass 1 on each of invariant_edge_case and risk_coverage; V2 gains one MET over Pass 1 on each of clarity, invariant_edge_case and risk_coverage (completeness 1 stays NOT MET, risk_coverage 2 and structure 1 stay MET).
