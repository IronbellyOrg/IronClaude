# Score Pass 2 (reverse order: B first, then A) - slot C-06 limits-repair-policy

Scope: qualitative layer only, 30 criteria per variant, CEV format, binary verdicts. Scored: the ORIGINAL variants (F/variant-2-original.md = B, F/variant-1-original.md = A). Debate files (diff-analysis.md, round2.5-fault-finder-raw.md) were used only as evidence of defects; each cited defect is named with its id. Source input for Completeness 1: conflict row C-06 in phase-outputs/discovery/undecidable-conflicts.md line 23 (policy for over-limit lines, per-line errors and re-ask, itemised drop report, fail-closed rule, raise-the-limits option, INV-C, INV-I, INV-G, test or measurement, effect on PR review and rf-qa).

Abbreviations: B = Variant 2 (Proposal B), A = Variant 1 (Proposal A). "B s3.3" = section 3.3 of that variant. DA = diff-analysis.md, FF = round2.5-fault-finder-raw.md.

---

# PART 1: VARIANT B (evaluated first)

## B - Completeness

C1. CLAIM: B covers all explicit requirements of conflict row C-06.
EVIDENCE: policy: s1 and s3 (itemise, re-ask, no edit); per-line errors: s3.1 "Line classifier and drop record ... `{line, id, rule, field, actual, limit, blocking_state}`"; itemised drop report: s3.3 "The merged report gains a per-reviewer 'dropped lines' table"; fail-closed: s3.3 "New refusal reason `dropped-blocking`"; raise-the-limits: s3.5 "B-raise ... 300/450 admit 120 of the 124"; INV-C, INV-I, INV-G: s5 table rows; test or measurement: s6 M1-M3, T-B1..T-B5; PR review and rf-qa: s7.
VERDICT: MET

C2. CLAIM: B addresses edge cases and failure scenarios.
EVIDENCE: s3.2 "A transport without the capability gets itemise-only plus the fail-closed rule of 3.3, never a truncation"; s3.3 "so that it cannot deadlock when a re-ask is impossible or fails: an acknowledgement with owner and reason"; s6 T-B3 matrix (one reviewer with only dropped blocking lines; surviving blocking row; only `blocking: false` drops); s3.2 E1 run A2 "OutOfOrder refused".
VERDICT: MET

C3. CLAIM: B includes dependencies and prerequisites.
EVIDENCE: s2 table with a "Where B is conditional on one: C-03's refusal object ... and C-02's `block_ok` filter on clearing"; s3.2 transport prerequisites (`--resume`, session persistence); s9 list of open facts.
VERDICT: MET

C4. CLAIM: B defines success/completion criteria.
EVIDENCE: s6 table columns "Shows B right" / "Shows B wrong" for M1-M3 and T-B1..T-B5, e.g. M1 "the `dropped-blocking` refusal fires on exactly the 3 merges of 4.2 and on none of the other 261".
VERDICT: MET

C5. CLAIM: B specifies what is explicitly out of scope.
EVIDENCE: s3.6 "What B does not do: No truncation step, no normaliser in front of the parser ... no calibrator or debate"; s2 "C-03 INV-006 and INV-007 ... B does not claim to close them"; s9 "Open facts this proposal does not settle".
VERDICT: MET

Completeness subtotal B: 5/5

## B - Correctness

K1. CLAIM: B has no factual errors or hallucinated claims.
EVIDENCE: Defects found. (a) s4.4 states "all 5 re-asked blocks recorded valid afterwards", while B's own E3 row says reviewer 2 "still had two bad citations" and the result is only "3 of 3 (to be confirmed by `review cluster`)": four confirmed, one unconfirmed (DA X-002). (b) s5 INV-C column says "Four boundary assertions are rewritten" but s3.1 also requires `card_convert.py` to import the shared constants, which breaks the `len(claim) == 300` pin at `test_review_card_convert.py:500`, making five (DA C-011). (c) s4.2 "fires on 3 of 264" is derived from `flags.tsv` wording, honestly labelled as not re-executed, so not counted as an error. (a) and (b) are factual overstatements/miscounts.
VERDICT: NOT MET

K2. CLAIM: B's technical approaches are feasible with stated constraints.
EVIDENCE: s3.2 builds the re-ask as a `continue(reviewer, message)` capability per transport and degrades to itemise-only plus refusal where the transport lacks it; the manifest record problem is not claimed solved ("The shape of that record belongs to slot C-08; B only requires that one exists", citing the A2 `OutOfOrder` refusal). The classifier keeps `ok` and `errors` shape so existing pins hold (s5 INV-C, T-B2).
VERDICT: MET

K3. CLAIM: B uses terminology consistently and accurately.
EVIDENCE: "B-core"/"B-raise" defined in s3.5 and used in the same sense in s5, s6, s8; `blocking_state` (`true`/`false`/`unknown`) defined in s3.1 and used identically in s3.2, s3.3, s6; "dropped" always means a line removed by the parser with a record; "Replay" is defined in the header as a read-only execution that wrote no file.
VERDICT: MET

K4. CLAIM: B has no internal contradictions.
EVIDENCE: Checked s3.2 vs s3.3 (re-ask trigger and `complete` rule use the same true/unknown rule), s1 vs s5 (no edit vs no pin changes in B-core), s4.2 vs s8 (3 of 264, 44 vs 80 runs consistently stated). The s4.4 "5 of 5 recorded valid" vs E3 row is an overstatement (K1), but the text says "recorded valid" and marks the E3 value "to be confirmed", so it is reconcilable, not a contradiction. s4.5 last bullet narrows its own corruption argument ("bears on where a repair may live, not on a repair written in code") rather than contradicting it.
VERDICT: MET

K5. CLAIM: B's claims are supported by evidence or rationale in the document.
EVIDENCE: Every row in s4.1 carries a file:line and a [CODE-VERIFIED]/[UNVERIFIED] tag; s4.3 gives a stated replay method and counts; s4.6 re-grades each doc-sourced claim from the conflict row (e.g. "88 of 92 ... [CODE-VERIFIED] as arithmetic on the audit-D reasons (56+18+14 = 88; 24+14+10 = 48)").
VERDICT: MET

Correctness subtotal B: 4/5

## B - Structure

S1. CLAIM: B orders sections logically (prerequisites before dependents).
EVIDENCE: s1 position, s2 relation to adjudicated slots C-01..C-03, s3 design consequence, s4 evidence, s5 invariants, s6 tests, s7 downstream effect, s8 objection, s9 open facts.
VERDICT: MET

S2. CLAIM: B keeps consistent hierarchy depth (no orphaned subsections).
EVIDENCE: s3 has 3.1-3.6, s4 has 4.1-4.6, s2, s5, s6, s8, s9 are flat; no section holds a lone subsection.
VERDICT: MET

S3. CLAIM: B separates concerns between sections.
EVIDENCE: design (s3), evidence (s4), invariants (s5), measurement (s6), consumer effect (s7) and objection (s8) are separate sections; the module-by-module table (s3.4) is apart from the shared-core table (s3.1).
VERDICT: MET

S4. CLAIM: B has navigation aids.
EVIDENCE: numbered section references throughout ("section 4.3", "section 3.3", "section 8"), the header tag legend, and tables that index adjudicated outcomes (s2) and invariants (s5).
VERDICT: MET

S5. CLAIM: B follows the conventions of its artifact type (an adversarial position proposal).
EVIDENCE: "Status: Complete" header and footer, position statement, design consequence, evidence, invariants, test or measurement, effect on PR/rf-qa, strongest objection and answer: all items the slot brief requires.
VERDICT: MET

Structure subtotal B: 5/5

## B - Clarity

L1. CLAIM: B uses unambiguous language.
EVIDENCE: Rules are stated as testable conditions, e.g. s3.3 "the round has no blocking-open row after the union and at least one reviewer has an unresolved `true` or `unknown` dropped line". Uncertainty is tagged [UNVERIFIED] rather than hedged in prose. Residual indeterminacy ("one further B-compatible design ... that is not decided here", s7; "Trigger is a module setting", s3.2) is declared, not blurred.
VERDICT: MET

L2. CLAIM: B is concrete rather than abstract.
EVIDENCE: exact record fields (s3.1), exact limits "anchor and anchor2 12..200, ... claim at most 300, refs at most 8, id at most 16" with file:line, exact test matrix (s6 T-B3).
VERDICT: MET

L3. CLAIM: Each B section has a clear purpose.
EVIDENCE: Section titles state purpose ("How this position relates to the adjudicated slots", "The test or measurement that would show B right or wrong", "Open facts this proposal does not settle"); s1 summarises the whole position in one paragraph.
VERDICT: MET

L4. CLAIM: B defines acronyms and domain terms on first use.
EVIDENCE: No evidence found - searched s1-s9. "E1", "E2", "CO-8", "CO-9", "GQ-017", "audit-D", "Spike 5", "findings-v1", "`block_ok`", "INV-C" (only by reference to synth-06) are used without a definition in the document; only "Replay", the three tags, and B-core/B-raise are defined.
VERDICT: NOT MET

L5. CLAIM: B identifies actionable next steps or decision points.
EVIDENCE: s3.5 and s9 name the owner decision ("Whether the owner accepts a widening of the findings-v1 grammar (B-raise)"); s6 gives runnable measurements with pre-written decision rules; s9 lists the facts to settle (M2 re-ask recovery, C-03 refusal object form).
VERDICT: MET

Clarity subtotal B: 4/5

## B - Risk Coverage

R1. CLAIM: B identifies at least 3 risks with probability and impact.
EVIDENCE: s8 objection and answer: (1) stall/refusal exposure with probability "3 of 264 merges (1.1 percent)" and 44 vs 80 re-ask runs, impact "refuses ... over a cosmetic length error"; (2) transport cannot re-ask, impact "degrades to itemise plus refusal-on-PASS-by-loss"; (3) long-anchor models repeat the violation, likelihood evidenced by "luna 27 of 30 drops are anchors, ember 24 of 33", impact "B's cost becomes refusals". Also s5 INV-F/K/N rows name endangered invariants.
VERDICT: MET

R2. CLAIM: B gives a mitigation for each identified risk.
EVIDENCE: s8 point 1 (trigger limited to true/unknown drops), point 2 (brief change CO-8 plus B-raise), point 4 (acknowledgement exit removes deadlock), point 5 (B-raise and brief change carry the weight if long-anchor models repeat); s3.2 (transport without capability gets itemise plus refusal); s5 INV-G (headless `--resume` excluded until isolation exists).
VERDICT: MET

R3. CLAIM: B addresses failure modes and recovery procedures.
EVIDENCE: s3.3 acknowledgement exit; s3.2 "A transport without the capability gets itemise-only plus the fail-closed rule ... never a truncation"; s3.2 attempt-record failure in run A2.
VERDICT: MET

R4. CLAIM: B considers external dependencies and their failure scenarios.
EVIDENCE: s2 "without [C-03's refusal object] B's fail-closed rule has no vehicle and falls back to a warning"; s3.2 `--resume` for gateway ids "[UNVERIFIED]"; s9 C-08 record shape, C-03 object form.
VERDICT: MET

R5. CLAIM: B includes a monitoring or validation mechanism.
EVIDENCE: s6 M1 (conservation and fire-set replay), M2 (re-ask recovery), M3 (incidence levers), T-B1..T-B5; s3.2 first-pass `findings_block_compliance_rate` keeps its E1 definition; per-reviewer "dropped lines" table in the merged report (s3.3).
VERDICT: MET

Risk subtotal B: 5/5

## B - Invariant and Edge Case Coverage

I1. CLAIM: B addresses boundary conditions for collections (empty, single, maximum).
EVIDENCE: s6 T-B3 "one reviewer with only dropped blocking lines (today's refusal at `ledger.py:150-157` stays); two reviewers, one with a dropped blocking line and one with an empty valid block"; s4.2 total-loss merges "6 of 6 and 8 of 8 lines"; s3.1 refs at most 8, citations 1..8; s3.1 conservation "every non-blank line of the last findings block is exactly one of kept finding, prior line, or dropped record".
VERDICT: MET

I2. CLAIM: B handles state variable interactions across component boundaries.
EVIDENCE: s2 C-02 row and s8: an over-limit line makes `block_ok` False so the reviewer's `prior` lines "do not count until the re-ask returns a valid block"; s3.2 first-pass validity "recorded before the re-ask"; s3.3 reviewer not `complete` for C-03's quorum.
VERDICT: MET

I3. CLAIM: B identifies guard condition gaps.
EVIDENCE: s3.1 `blocking_state` `unknown` for "absent or non-boolean `blocking`"; s2 "a `prior` line with a bad status is itemised too (`findings.py:175-186`), not only finding lines"; s3.3 "this cannot deadlock" exit; s5 INV-H "This is still a convention".
VERDICT: MET

I4. CLAIM: B covers count divergence scenarios.
EVIDENCE: s4.1 pins "v2 quote 200 ok / 201 not; v2 claim 300 / 301" and "Length is counted after whitespace flattening"; s4.2 "Four verdicts flipped ... three flips plus five total-loss merges" marked [CODE-CONTRADICTED]; s6 M1 "17-19 lines audit-D could not" explain; s4.3 124 vs 154 denominators.
VERDICT: MET

I5. CLAIM: B considers interaction effects when components combine.
EVIDENCE: s3.5 "together they leave about 4 lines in 124 for the re-ask" (B-core plus B-raise); s6 M3 separates the brief lever from the raise lever; s2 interaction with C-02 `block_ok` filter and C-03 refusal.
VERDICT: MET

Invariant subtotal B: 5/5

B totals: Completeness 5, Correctness 4, Structure 5, Clarity 4, Risk 5, Invariant 5 = 28/30 (qual_score 0.933)

---

# PART 2: VARIANT A (evaluated second)

## A - Completeness

C1. CLAIM: A covers all explicit requirements of conflict row C-06.
EVIDENCE: Covered: policy (s1), per-line errors/re-ask (s2 item 6), itemised record (s2 item 3 `repairs`/`dropped`), INV-C, INV-I, INV-G (s4), measurement (s5), PR and rf-qa (s6). Not covered: the raise-the-limits option is never discussed in s1-s7 (s6 last bullet is a per-module profile limit, not raising the shared constants); the fail-closed rule is explicitly excluded (s4.1 "Silent on: whether a residual dropped blocking line should make the merge fail closed ... it is not part of A"). Two named elements of the conflict row are missing.
VERDICT: NOT MET

C2. CLAIM: A addresses edge cases and failure scenarios.
EVIDENCE: s3.2 "A non-verbatim anchor fails to locate cut or uncut ... kept with `anchor_status: missing`"; s5 "refs_norm(original) == refs_norm(repaired)" with `refs_lost`; s2 item 4 residual dropped lines; s5 M3 "if recovery on the residual set is near zero ... the position reduces to truncation plus itemised drops".
VERDICT: MET

C3. CLAIM: A includes dependencies and prerequisites.
EVIDENCE: s4.1 "C-02 ... consistent and dependent"; "C-03 ... consistent and dependent"; "Dependency: if 'called from inside both parsers' is read as unconditional (no keyword), [four tests] must be rewritten"; s7 point 1 states the SKILL.md:343 reading dependency.
VERDICT: MET

C4. CLAIM: A defines success/completion criteria.
EVIDENCE: s5 M1 "Position A is wrong on its central claim if fewer than 75 percent of the 48 blocking length lines come out located and unambiguous"; M2 and M3 name failure conditions; unit tests with boundary, idempotence, no-op properties.
VERDICT: MET

C5. CLAIM: A specifies what is explicitly out of scope.
EVIDENCE: s4.1 "Disagreement with an outcome: none. Silent on: whether a residual dropped blocking line should make the merge fail closed ... it is not part of A"; s2 item 3 and s1 "It touches no field the limits do not name"; s6 "the repair does not change that" (rf-qa ledger path needs C-01).
VERDICT: MET

Completeness subtotal A: 4/5

## A - Correctness

K1. CLAIM: A has no factual errors or hallucinated claims.
EVIDENCE: Defects found. (a) s2 item 5 says the re-ask is recorded as attempt 2 and "adds no vote" citing `manifest.py:378-383`; code at `manifest.py:371-372` raises `OutOfOrder` once the stage is committed and `:378-381` raises `Conflict` when the earlier attempt `complete`d, and E1 run A2 hit exactly this refusal (DA A-006 CONTRADICTED). (b) s4 INV-I row "Preserved ... the step turns a dropped finding into a kept finding, which adds rows and so moves toward FAIL" is refuted by FF INV-017 [RAN]: a 200-character prefix matching two places is absorbed by a `deferred` row and gives verdict PASS where today the round is refused. (c) s1/s3.2 "exact prefix" is false for the claim, which is cut to 297 characters plus `...` (DA C-009).
VERDICT: NOT MET

K2. CLAIM: A's technical approaches are feasible with stated constraints.
EVIDENCE: The stated constraint is the manifest: A's s2 item 5 asserts the second attempt is recordable "as attempt 2" for a reviewer "whose first attempt did not complete". With the repair, a length-only block is `complete`, so the re-ask is not triggered for it, and for residual blocks the E1 A2 record shows the commit has already happened (`OutOfOrder`; DA A-006; FF INV-018 shows the reflect step order makes the pre-commit parse impossible as written). The recording design is not feasible as stated.
VERDICT: NOT MET

K3. CLAIM: A uses terminology consistently and accurately.
EVIDENCE: s1 and s3.2 call the cut an "exact prefix" that "still locates" while s2 item 7 states the claim cut is `card_convert`'s "297 characters plus `...`", so the cut output is not a prefix (DA C-009); "normalise" (position title), "repair" (`repair_line`, `repair=`), "truncate" and "cut" are used for one operation without being tied together.
VERDICT: NOT MET

K4. CLAIM: A has no internal contradictions.
EVIDENCE: s1 "It touches no field the limits do not name" vs s5 "The step therefore copies any reference token found only in the cut text into `refs`" (DA C-008: the copy rule writes the `refs` field, which no limit names in that sense). Also s1/s3.2 "exact prefix" vs s2 item 7 and s7 point 3 "The cut is marked (`...`)". Two internal contradictions.
VERDICT: NOT MET

K5. CLAIM: A's claims are supported by evidence or rationale in the document.
EVIDENCE: s3.1 table with source and tag per figure (e.g. "92: anchor over 200 = 56 ... [RECOMPUTED in two files]"); s3.2 executed check "a 335-character flattened table-row anchor cut to `flat(anchor)[:200].rstrip()` gives `locate == [(2, 3)]`"; s2 items 1-8 each carry `file:line` and a [CODE-VERIFIED] tag; s7 answers each objection with a cited reason.
VERDICT: MET

Correctness subtotal A: 1/5

## A - Structure

S1. CLAIM: A orders sections logically.
EVIDENCE: s1 position, s2 design consequence, s3 evidence, s4 invariants (with s4.1 consistency), s5 tests/measurement, s6 PR and rf-qa effect, s7 objection and answer.
VERDICT: MET

S2. CLAIM: A keeps consistent hierarchy depth (no orphaned subsections).
EVIDENCE: s4 "Invariants" contains a table followed by exactly one subsection, "### 4.1 Consistency with the adjudicated slots": a lone subsection with no sibling. s2 also nests bullets under numbered item 7 while other items are flat, and s3 has 3.1-3.4. The lone 4.1 is an orphaned subsection.
VERDICT: NOT MET

S3. CLAIM: A separates concerns between sections.
EVIDENCE: design (s2), evidence (s3), invariants (s4), measurement (s5), downstream effect (s6) and objection (s7) each occupy a section.
VERDICT: MET

S4. CLAIM: A has navigation aids.
EVIDENCE: header abbreviation legend ("`R02` = `research/02-finding-contract.md`, `S05` ..., `S06` ..."), cross-references "See section 7", "section 3.2", "section 5", "(section 2 item 6)".
VERDICT: MET

S5. CLAIM: A follows the conventions of its artifact type.
EVIDENCE: "Status: Complete", position, design consequence, evidence, invariants, test or measurement, effect on PR and rf-qa, strongest objection and answer, matching the slot brief.
VERDICT: MET

Structure subtotal A: 4/5

## A - Clarity

L1. CLAIM: A uses unambiguous language.
EVIDENCE: Rules are stated precisely, e.g. s2 item 4 "`ok` after repair is the real parser's verdict on the repaired line"; s5 kill line "fewer than 75 percent of the 48 blocking length lines". Conditionals are explicit and labelled (s7 point 1 "That is a reading of the sentence, not a fact").
VERDICT: MET

L2. CLAIM: A is concrete rather than abstract.
EVIDENCE: s2 item 3 gives the record fields `{line, finding_id, blocking, field, reason, original_chars, kept_chars}`; s2 item 2 names the three production call sites with `file:line`; s5 lists named unit tests.
VERDICT: MET

L3. CLAIM: Each A section has a clear purpose.
EVIDENCE: Titles state purpose ("The test or measurement that would show Position A right or wrong", "Effect on future PR code review and rf-qa replacement"); s1 gives a one-paragraph summary.
VERDICT: MET

L4. CLAIM: A defines acronyms and domain terms on first use.
EVIDENCE: A defines `R02`, `S05`, `S06` and the three tags in the header, but "E1", "E2", "CO-8", "GQ-017", "GQ-018", "audit-D", "Spike 5", "INV-003", "T1", "DR-006" and "`block_ok`" are used without a definition (s2 item 2 "T1 literally true", s3.3 "E2 Spike 5"). No definition found in s1-s7.
VERDICT: NOT MET

L5. CLAIM: A identifies actionable next steps or decision points.
EVIDENCE: s5 M1-M4 with fixed-before-run thresholds ("the owner may change it"); s7 point 1 states the owner decision on reading `SKILL.md:343`; s4.1 names what C-02/C-03 must decide.
VERDICT: MET

Clarity subtotal A: 4/5

## A - Risk Coverage

R1. CLAIM: A identifies at least 3 risks with probability and impact.
EVIDENCE: s7 and s5: (1) re-ask recovery risk, quantified "at most 4 of 92 lines (1 of 49 blocking) depend on re-ask recovery", impact "reduces to truncation plus itemised drops"; (2) wrong occurrence, "A shorter prefix is more likely to match twice, and `locate` takes the first match", impact first-match binding, kill line 75 percent; (3) false-blocker rows from repaired lines, impact "a rejected row stays `open` and only `defer` clears it" against a cap of 3 reviews; (4) meaning loss in a cut claim. Probabilities are mostly qualitative but each risk has a stated likelihood and impact.
VERDICT: MET

R2. CLAIM: A gives a mitigation for each identified risk.
EVIDENCE: Mitigations exist for risks (1) (re-ask half can be switched off, s7 point 6), (2) (if M1 shows many ambiguous anchors, mark `anchor_ambiguous` and refuse to let the row clear on `prior resolved` alone), (4) (typed fields untouched; refs copy rule). For risk (3), false-blocker rows, s5 M2 only says "this is a real cost to count, not assume" and gives no mitigation. Not every identified risk has one.
VERDICT: NOT MET

R3. CLAIM: A addresses failure modes and recovery procedures.
EVIDENCE: s5 M3 "if recovery on the residual set is near zero ... then the position reduces to truncation plus itemised drops, and the residual is a fail-closed question for C-03"; s2 item 4 residual blocks stay `invalid` and are re-asked; s7 point 1 fallback to B if the owner reads SKILL.md:343 as covering code.
VERDICT: MET

R4. CLAIM: A considers external dependencies and their failure scenarios.
EVIDENCE: s2 item 6 swarm transport has no session and `--resume` for gateway ids is "[UNVERIFIED]", answered by the stateless re-ask; s4.1 C-02 and C-03 dependencies "if those slots decide otherwise the block stays `block_ok` False"; s6 PR caller "must confirm" a second prompt.
VERDICT: MET

R5. CLAIM: A includes a monitoring or validation mechanism.
EVIDENCE: s5 M4 "Track `repaired_lines_rate` per model next to first-parse compliance. A rising repair rate means the brief is failing to state the limits"; s2 item 8 `repaired_lines_rate` and `reask_recovery_rate`; M1-M3 replays.
VERDICT: MET

Risk subtotal A: 4/5

## A - Invariant and Edge Case Coverage

I1. CLAIM: A addresses boundary conditions for collections (empty, single, maximum).
EVIDENCE: s5 "copies any reference token found only in the cut text into `refs` while it has room (cap 8), and records `refs_lost` otherwise" (maximum size); s5 v2 loss unit test "a v2 block with one over-limit line and one valid line"; s3.1 "at most 4 residual lines". Empty-block and panel-of-1 cases are not treated; maximum and small-collection cases are.
VERDICT: MET

I2. CLAIM: A handles state variable interactions across component boundaries.
EVIDENCE: s4 INV-I row "`block_ok` becomes True for a reviewer whose only fault was length, so that reviewer counts for clearing and quorum"; s2 item 8 first-parse metric computed from a `repair=False` parse; s2 item 5 manifest attempt recording.
VERDICT: MET

I3. CLAIM: A identifies guard condition gaps.
EVIDENCE: s3.2 "`anchor_ambiguous` is read by nothing, DR-006" (an unguarded flag); s5 "a citation-only line gets no `anchor`" (non-invention guard); s5 refs "cut could remove an `AC-0.4` that appeared only in the tail"; s2 item 2 "a pin built another way is [UNVERIFIED]".
VERDICT: MET

I4. CLAIM: A covers count divergence scenarios.
EVIDENCE: s5 Boundary "200 and 300 characters pass ... 201 and 301 fail ... A flattened-whitespace case (a 205-character raw anchor that is 190 flattened) is not repaired, because the limit is measured after `flat()`"; s3.1 unit mismatch "264 merges ... 80 reviewer-runs ... (a count of runs, not findings)" and "the '4' of `COMBO-REPORT.md:292` is not reproduced".
VERDICT: MET

I5. CLAIM: A considers interaction effects when components combine.
EVIDENCE: s5 M2 re-merge counts a repaired line that "turns from the reviewer's PASS to FAIL because a repaired line added a blocking row"; s4.1 C-02 and C-03 interaction with repair (more `complete` blocks, quorum floor); s2 item 7 repair plus `card_convert` claim rule.
VERDICT: MET

Invariant subtotal A: 5/5

A totals: Completeness 4, Correctness 1, Structure 4, Clarity 4, Risk 4, Invariant 5 = 22/30 (qual_score 0.733)

---

# Summary and floor check

| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | Total | qual_score |
|---|---|---|---|---|---|---|---|---|
| B | 5 | 4 | 5 | 4 | 5 | 5 | 28/30 | 0.933 |
| A | 4 | 1 | 4 | 4 | 4 | 5 | 22/30 | 0.733 |

Edge Case Floor check (Invariant and Edge Case dimension, floor 1/5): B 5/5 eligible; A 5/5 eligible. Floor not suspended.

Notes for the re-evaluation step (not part of the verdict rows): the largest pass-2 disagreement risk is Correctness 1-4 for A (defects DA A-006, DA C-008, DA C-009, FF INV-017) and Correctness 1 for B (the 5-of-5 and four-versus-five pin overstatements); Completeness 1 for A rests on the absence of the raise-the-limits option and of a fail-closed rule in the original.

# Machine-readable verdicts

PASS2|completeness|1|B|MET
PASS2|completeness|2|B|MET
PASS2|completeness|3|B|MET
PASS2|completeness|4|B|MET
PASS2|completeness|5|B|MET
PASS2|correctness|1|B|NOT MET
PASS2|correctness|2|B|MET
PASS2|correctness|3|B|MET
PASS2|correctness|4|B|MET
PASS2|correctness|5|B|MET
PASS2|structure|1|B|MET
PASS2|structure|2|B|MET
PASS2|structure|3|B|MET
PASS2|structure|4|B|MET
PASS2|structure|5|B|MET
PASS2|clarity|1|B|MET
PASS2|clarity|2|B|MET
PASS2|clarity|3|B|MET
PASS2|clarity|4|B|NOT MET
PASS2|clarity|5|B|MET
PASS2|risk|1|B|MET
PASS2|risk|2|B|MET
PASS2|risk|3|B|MET
PASS2|risk|4|B|MET
PASS2|risk|5|B|MET
PASS2|invariant|1|B|MET
PASS2|invariant|2|B|MET
PASS2|invariant|3|B|MET
PASS2|invariant|4|B|MET
PASS2|invariant|5|B|MET
PASS2|completeness|1|A|NOT MET
PASS2|completeness|2|A|MET
PASS2|completeness|3|A|MET
PASS2|completeness|4|A|MET
PASS2|completeness|5|A|MET
PASS2|correctness|1|A|NOT MET
PASS2|correctness|2|A|NOT MET
PASS2|correctness|3|A|NOT MET
PASS2|correctness|4|A|NOT MET
PASS2|correctness|5|A|MET
PASS2|structure|1|A|MET
PASS2|structure|2|A|NOT MET
PASS2|structure|3|A|MET
PASS2|structure|4|A|MET
PASS2|structure|5|A|MET
PASS2|clarity|1|A|MET
PASS2|clarity|2|A|MET
PASS2|clarity|3|A|MET
PASS2|clarity|4|A|NOT MET
PASS2|clarity|5|A|MET
PASS2|risk|1|A|MET
PASS2|risk|2|A|NOT MET
PASS2|risk|3|A|MET
PASS2|risk|4|A|MET
PASS2|risk|5|A|MET
PASS2|invariant|1|A|MET
PASS2|invariant|2|A|MET
PASS2|invariant|3|A|MET
PASS2|invariant|4|A|MET
PASS2|invariant|5|A|MET

END-OF-SCORE-FILE
