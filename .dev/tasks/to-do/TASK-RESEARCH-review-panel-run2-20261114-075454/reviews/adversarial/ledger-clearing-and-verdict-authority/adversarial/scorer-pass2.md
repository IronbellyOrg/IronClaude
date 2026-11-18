# Qualitative scoring, position-bias PASS 2 (Variant B evaluated first, then Variant A)

Slot C-02, ledger-clearing-and-verdict-authority. Rubric: scoring-protocol.md A.2 (30 binary criteria, CEV). Scored text: variant-2-original.md (Variant B) and variant-1-original.md (Variant A), not the converged hybrid. Source input for completeness: C-02 row (undecidable-conflicts.md line 19) plus the six required sections (design consequence, evidence, invariants, test or measurement, effect on PR review and rf-qa, strongest objection).

Correctness rule applied: a criterion is NOT MET when debate-transcript.md established a factual error or a conceded defect that bears on it. Debate facts used: A conceded (round 1, concession 6) that its "complete reviewer" is only `block_ok` and that the `complete` completion state is not in the merge path; A corrected its own claim that `--resolution` already supports counting requested reviewers (merge_cmd.py:73-83 builds only a model map); A's dissent-hold at `resolved_check` is skipped by `apply_revision` (ledger.py:328); A's `expires_round` is inert under the 3-review cap; A's `count >= Q` guard deadlocks when Q exceeds the one-reviewer re-review. B conceded: the quote check cannot be satisfied by a correct deletion (revise brief prefers deleting, prompts.md:53); the B6 category predicate misgrades the shipped grading check (prompts.md:31) and `spec-panel.md:259`; B1 let a `prior` of open or regressed set any row, which would reopen a human-deferred row, against its own B7; B5 can yield REVISE with an empty Reviser brief; B's pin list omitted `test_prior_lines_never_change_a_status`.

---

## EVALUATION 1 OF 2: VARIANT B (variant-2-original.md), evaluated first

### Completeness

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Completeness | 1 | Covers all explicit requirements of source input | MET (1) | Header lists LG-1, VM-2, VM-4, C-S9; sections 2 to 7 are the six required sections; B covers clearing (B1-B4), blocking authority (B6), defer (B7), semantics (E8-E11). |
| Completeness | 2 | Edge cases and failure scenarios | MET (1) | T2 negative set: quote absent, invalid-block reviewer, answer plus re-find, hash mismatch, round after ESCALATE; section 7 discusses a reviewer skipping prior lines. |
| Completeness | 3 | Dependencies and prerequisites | MET (1) | B4 states "A quote check against doc_text means nothing unless doc_text is the revision output"; section 6 names C-01 locator dependency; quorum left to C-03. |
| Completeness | 4 | Success/completion criteria | MET (1) | T1 expected outcomes (L1 stays resolved_check, verify_ids equals L1) and "B is shown wrong if M1 shows the quote check adds no power over silence". |
| Completeness | 5 | Explicit out of scope | MET (1) | "Not addressed by B and left to other slots: the quorum count (C-03; D-2) ... anchors and spans (DR-006, DR-108)"; section 7 "What B leaves open". |

### Correctness

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Correctness | 1 | No factual errors or hallucinated claims | MET (1) | Debate re-read and confirmed B's cited lines (ledger.py:254-258, :112, :279, panel.py:596-605, 8 of 8 templates apply_to first); unverified items are tagged "[UNVERIFIED here]"; no factual error was established against B. |
| Correctness | 2 | Technical approaches feasible with stated constraints | NOT MET (0) | Debate: B3 quote must occur in doc_text yet the revise brief prefers deletion so a correct fix leaves nothing to quote; B6 category predicate misgrades prompts.md:31; B5 can give REVISE with empty brief (all conceded). |
| Correctness | 3 | Terminology consistent and accurate | MET (1) | Section 2.1: "Status names stay those of review-ledger/1 (open, resolved_check, resolved, regressed, deferred)"; verify_ids, held_ids, brief_ids used consistently; minor slip calling unverified and held "row states" in INV-J is not established by debate. |
| Correctness | 4 | No internal contradictions | NOT MET (0) | B1 says "A prior of open or regressed sets the row to open or regressed" with no status guard, against B7 "the row is terminal for the machine"; B conceded in Round 2 it would reopen a human-deferred row. |
| Correctness | 5 | Claims supported by evidence or rationale | MET (1) | Evidence E1-E16 each carry a file:line and a tag; section 7 gives the asymmetry rationale "bounded by cap_reviews (ledger.py:93-96), visible". |

### Structure

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Structure | 1 | Logical section ordering | MET (1) | Position (1), design (2), evidence (3), invariants (4), tests (5), effects (6), objection (7); the evidence precedes the invariants that cite it. |
| Structure | 2 | Consistent hierarchy depth | MET (1) | H2 sections 1-7 with H3 only under section 2 (2.1, 2.2); no orphan subsections. |
| Structure | 3 | Separation of concerns | MET (1) | Section 3 splits "Defect side" from "Semantics side" and "Limits of this evidence"; section 4 splits Preserves from Endangers. |
| Structure | 4 | Navigation aids | MET (1) | "Numbering E1.. is local to this file"; labelled rules B1-B7, T1-T5, M1-M3 are cross-referenced (for example "section 5 agreement measurement", "E7"). |
| Structure | 5 | Follows artifact-type conventions | MET (1) | Position paper with the six required sections, a Status line, slot id, date, and a tag rule at the head. |

### Clarity

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Clarity | 1 | Unambiguous language | MET (1) | Operative rules are stated flatly (B1 "needs a prior line resolved ... and the quote occurs in doc_text"; B5 "PASS only when all three are empty"); hedging is confined to declared open questions. |
| Clarity | 2 | Concrete, not abstract | MET (1) | Names functions, lines and exit codes ("exit codes stay 0/10/11 (ledger_cmd.py:13,109)"; T1 replay with L1). |
| Clarity | 3 | Each section has a clear purpose | MET (1) | Section 1 is a one-paragraph summary of the position; section 7 is "The strongest objection and the answer". |
| Clarity | 4 | Acronyms and domain terms defined on first use | NOT MET (0) | INV-C is cited in B3 (section 2.1) before section 4 defines it; D-1, E2, R7, M9, P12, "DEGRADED" are used without definition. |
| Clarity | 5 | Actionable next steps or decision points | MET (1) | M2 "free pre-measurement on existing data"; "B is shown wrong if M1 ... or if M2 shows prior-line compliance too low for the cap". |

### Risk Coverage

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Risk Coverage | 1 | At least 3 risks with probability and impact | NOT MET (0) | Section 4 Endangers lists INV-D, INV-C, INV-J as MEDIUM and INV-N, INV-H as LOW (a severity), but no probability is assessed for any of them. |
| Risk Coverage | 2 | Mitigation for each identified risk | NOT MET (0) | INV-J flip risk gets only "the section 5 agreement measurement is what shows how often"; INV-D meaning-of-verdict change "is not settled by B"; no mitigation for either. |
| Risk Coverage | 3 | Failure modes and recovery | MET (1) | Section 7: "two failure modes are asymmetric ... ESCALATE at the 3-review cap with the unanswered rows listed" versus an invisible wrong PASS; held-only gives ESCALATE at once (B5). |
| Risk Coverage | 4 | External dependencies and their failure | MET (1) | E15 "Machinery that informs but does not gate fails open" (stoprule EXIT_OK); E14 no validated variant; section 6 PR dependency on C-01 locator. |
| Risk Coverage | 5 | Monitoring or validation mechanism | MET (1) | B6 reports disagreement "in the merge output warnings"; B7 surfaces `refound_deferred`; M1-M3 measurements. |

### Invariant and Edge Case Coverage

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Invariant & Edge | 1 | Collection boundaries (empty, single, max) | MET (1) | "the zero-valid-block refusal (ledger.py:150-157) stays"; E2 standard re-review is one reviewer; "when only held_ids remain the decision is ESCALATE at once". |
| Invariant & Edge | 2 | State variables across component boundaries | MET (1) | B4: `apply_revision` records no hash of the new text and `merge_round` hashes whatever it is given; B needs `revise` to store new_sha256 and `merge` to refuse a differing hash. |
| Invariant & Edge | 3 | Guard condition gaps | MET (1) | E1 `block_ok` is "written at :129,147 ... never read by this loop"; E4 defer "no status guard"; E6 only MINOR plus blocking is rejected. |
| Invariant & Edge | 4 | Count divergence (off-by-one, inclusive/exclusive) | MET (1) | B5 "REVISE while n < cap_reviews and ESCALATE at the cap"; "a round after ESCALATE is refused (the only check today is n == len(rounds)+1, ledger.py:114-118)". |
| Invariant & Edge | 5 | Interaction effects | MET (1) | INV-J: on a MAJOR contradiction typed blocking false, B6 returns blocking against spec-panel.md:259; "a re-find of the row's defect wins over any resolved answer". |

### Variant B subtotals

| Dimension | Score |
|---|---|
| Completeness | 5/5 |
| Correctness | 3/5 |
| Structure | 5/5 |
| Clarity | 4/5 |
| Risk Coverage | 3/5 |
| Invariant & Edge Case Coverage | 5/5 |
| **Total (B)** | **25/30** |

Edge-case floor (B): Invariant & Edge Case Coverage = 5/5, at or above 1/5, ELIGIBLE.

---

## EVALUATION 2 OF 2: VARIANT A (variant-1-original.md), evaluated second

### Completeness

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Completeness | 1 | Covers all explicit requirements of source input | MET (1) | Sections 2 to 7 are the six required sections; position paragraph covers clearing (a), blocking authority (b), derived verdict (c), defer (d); conflict IDs are covered though not listed in the header. |
| Completeness | 2 | Edge cases and failure scenarios | MET (1) | Section 3.1 item 3 (empty block from one unrelated reviewer clears a 3-of-3 row); section 4 "Held-round cost"; section 2 `defer` guards on non-blocking-open rows; empty-diff clause. |
| Completeness | 3 | Dependencies and prerequisites | MET (1) | "The quorum value Q ... belong to slot C-03; A takes Q as a parameter"; section 6 "`findings_v2` rejects prior lines, so a v2-native module needs a carrier ... C-01's re-review contract". |
| Completeness | 4 | Success/completion criteria | MET (1) | Section 5 item 1 gives expected outcomes per reproduction (L1 stays resolved_check, unverified_ids equals L1); item 4 "A is wrong if its false-clear rate is not clearly below the control's". |
| Completeness | 5 | Explicit out of scope | MET (1) | "Items in the slot's neighbourhood that A neither fixes nor depends on: the new-text hash at revise, the lock on the ledger file (FX-12), and ... annotate"; D-2 left to C-03. |

### Correctness

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Correctness | 1 | No factual errors or hallucinated claims | NOT MET (0) | Position paragraph requires reviewers "whose recorded completion state is complete" but the merge path has only `block_ok` (A conceded); A also overstated that `--resolution` already supports counting requested reviewers (corrected in Round 2). |
| Correctness | 2 | Technical approaches feasible with stated constraints | NOT MET (0) | Debate: dissent held at `resolved_check` is skipped by `apply_revision` (ledger.py:328), so the next fix is ignored; `expires_round` is inert under the 3-review cap; a fixed Q above the one-reviewer re-review deadlocks clearing. |
| Correctness | 3 | Terminology consistent and accurate | NOT MET (0) | "Complete reviewer" and "recorded completion state" name a state the merge path lacks (it is only `block_ok`); the paper uses the term in the guard, the table and section 7. |
| Correctness | 4 | No internal contradictions | MET (1) | No contradiction established: "prior lines ... never a status writer" is kept consistent with the veto-only role; the `defer` expiry reopen and "deferred counts open" are consistent. |
| Correctness | 5 | Claims supported by evidence or rationale | MET (1) | 14 numbered evidence items with file:line and tags such as "[CODE-VERIFIED via research/03]"; section 7 answer 1 to 3 give rationale and name the measurement that would falsify A. |

### Structure

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Structure | 1 | Logical section ordering | MET (1) | Position (1), core and modules (2), evidence (3), invariants (4), test or measurement (5), PR and rf-qa (6), objection (7). |
| Structure | 2 | Consistent hierarchy depth | MET (1) | H2 sections 1-7 with H3 3.1 to 3.4 under evidence only; no orphan subsections. |
| Structure | 3 | Separation of concerns | MET (1) | Section 2 splits "Shared core" table from "Named modules" table; section 4 splits "Preserved" from "Endangered or open, with severity". |
| Structure | 4 | Navigation aids | MET (1) | Opening paragraph defines the path convention and tag set; evidence items numbered 1-14; cross-references such as "section 5 item 1" and "(LG-4 rule)". |
| Structure | 5 | Follows artifact-type conventions | MET (1) | Position paper with required six sections, Position and Status lines, slot id, date. |

### Clarity

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Clarity | 1 | Unambiguous language | MET (1) | Rules stated flatly: "verdict FAIL iff blocking_open is non-empty; decision PASS if none, ESCALATE if n >= cap or if every remaining row is deferred, else REVISE"; hedging is confined to declared open items. |
| Clarity | 2 | Concrete, not abstract | MET (1) | Table row "Clearing rule" names `ledger.py:254-258`, `count(reviewers with block_ok true) >= Q`; `defer(ledger, lid, reason, owner, expires_round)`. |
| Clarity | 3 | Each section has a clear purpose | MET (1) | Section 1 one-paragraph position; section 7 "The strongest objection to A, and the answer". |
| Clarity | 4 | Acronyms and domain terms defined on first use | NOT MET (0) | INV-N, INV-D, D-2, D-11, E2, LG-4, FX-12, C-06 are used without definition; INV-N appears in section 2 before section 4 lists it. |
| Clarity | 5 | Actionable next steps or decision points | MET (1) | Section 5 items 3 and 4: replay with three arms, "The rule that says A wrong, to be committed before the first run"; Q handed to C-03. |

### Risk Coverage

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Risk Coverage | 1 | At least 3 risks with probability and impact | NOT MET (0) | Section 4 "Endangered or open" table carries a Severity column (MEDIUM, HIGH, LOW) for six rows but no probability for any. |
| Risk Coverage | 2 | Mitigation for each identified risk | NOT MET (0) | Typed `blocking` residue row: "A keeps accepting CRITICAL with blocking false as PASS ... so A leaves it" (no mitigation); round-1 partial-panel HIGH risk is pushed to C-03. |
| Risk Coverage | 3 | Failure modes and recovery | MET (1) | "Held-round cost ... fail-closed and bounded"; INV-I row "a row with no attributable examination record stays counted as open"; INV-J "A held row consumes a review, never a fourth one". |
| Risk Coverage | 4 | External dependencies and their failure | MET (1) | Evidence 13: stoprule transcript check "returns EXIT_OK in every branch" and live trial invalid at transport; evidence 14 no validated variant; a requested reviewer that returned nothing counts for nothing. |
| Risk Coverage | 5 | Monitoring or validation mechanism | MET (1) | `held` events with reason codes, `unverified_ids` in merge output and report; section 5 compliance, false-clear and false-hold rates. |

### Invariant and Edge Case Coverage

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Invariant & Edge | 1 | Collection boundaries (empty, single, max) | MET (1) | Evidence 4: default re-review is a single reviewer; zero-valid-block refusal at ledger.py:150-157 stays; "if every remaining row is deferred" gives ESCALATE. |
| Invariant & Edge | 2 | State variables across component boundaries | MET (1) | Evidence 8: `apply_revision` moves rows to `resolved_check` without touching the stored verdict, which stays FAIL/REVISE; section 2 Verdict row stops storing verdict, decision, brief_ids. |
| Invariant & Edge | 3 | Guard condition gaps | MET (1) | Evidence 1: `block_ok` "read at ledger.py:150 and returned at :295 and nowhere in the clearing loop"; `defer` "no status guard"; CRITICAL with blocking false accepted. |
| Invariant & Edge | 4 | Count divergence (off-by-one, inclusive/exclusive) | MET (1) | "decision ... ESCALATE if n >= cap"; guard "count(...) >= Q" for both block_ok and typed-resolved counts; "never a fourth" review under the cap of 3. |
| Invariant & Edge | 5 | Interaction effects | MET (1) | INV-J: "with no hunk, apply_revision records named_not_touched and the row never reaches resolved_check" interacts with the empty-diff clause; quorum interacts with `apply_to` in the default flow. |

### Variant A subtotals

| Dimension | Score |
|---|---|
| Completeness | 5/5 |
| Correctness | 2/5 |
| Structure | 5/5 |
| Clarity | 4/5 |
| Risk Coverage | 3/5 |
| Invariant & Edge Case Coverage | 5/5 |
| **Total (A)** | **24/30** |

Edge-case floor (A): Invariant & Edge Case Coverage = 5/5, at or above 1/5, ELIGIBLE.

---

## Summary and edge-case-floor check

| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant & Edge | Total | qual_score | Floor (>= 1/5) |
|---|---|---|---|---|---|---|---|---|---|
| B (variant-2-original) | 5 | 3 | 5 | 4 | 3 | 5 | 25/30 | 0.833 | Eligible (5/5) |
| A (variant-1-original) | 5 | 2 | 5 | 4 | 3 | 5 | 24/30 | 0.800 | Eligible (5/5) |

Pass 2 margin: B leads A by 1 criterion (0.033). The whole difference sits in Correctness: A carries a factual and terminology error ("recorded completion state is complete" does not exist in the merge path) that B does not; both have a feasibility defect (A: dissent hold, inert expiry, Q deadlock; B: quote on deletions, B6 category predicate), and B alone has the B1 versus B7 contradiction. Neither variant loses a criterion on Risk Coverage criteria 1 and 2 relative to the other; both lack a probability rating and a mitigation for every risk. Both variants pass the edge-case floor.
