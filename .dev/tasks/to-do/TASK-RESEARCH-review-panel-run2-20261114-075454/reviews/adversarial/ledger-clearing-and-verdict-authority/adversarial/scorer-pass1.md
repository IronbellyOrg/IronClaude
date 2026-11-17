# Qualitative scoring, position-bias PASS 1 (order: Variant A, then Variant B)

Slot C-02 (ledger-clearing-and-verdict-authority). Rubric: scoring-protocol.md A.2, 30 additive binary criteria, CEV protocol. Scored text: the ORIGINAL variants (variant-1-original.md = A, variant-2-original.md = B), not the converged hybrid.

Source input for the Completeness criteria: the C-02 row (undecidable-conflicts.md line 19: LG-1 clearing, VM-2 blocking authority, VM-4 defer policy, C-S9 semantics) plus the six sections implied by both papers (design consequence for core and named modules, evidence, invariants, test or measurement, effect on PR review and rf-qa, strongest objection).

Correctness rule applied: a criterion is NOT MET where the debate (debate-transcript.md) established a factual or design error that bears on it. Evidence cells contain no pipe characters; where the papers write open-or-regressed, this file writes "open or regressed".

Debate-established defects used for Correctness (original text):
- A: (a) the claim that `--resolution` already carries the requested reviewer ids for counting was overstated, counting is new code (round2-A evidence 7); (b) A's "recorded completion state is complete" has no counterpart in the merge path, only `block_ok` (round1-A concession 6); (c) A holds a dissented row at `resolved_check`, and `apply_revision` skips non-open rows (`ledger.py:328`), so the next fix is silently ignored (conceded); (d) `expires_round` is inert because held-only gives ESCALATE and VM-6 refuses later rounds, so it contradicts A's own adoption of VM-6 (conceded); (e) reopen-on-refind overrides a human park (conceded); (f) quorum Q above the one-reviewer re-review panel deadlocks (round2-A evidence 8).
- B: (a) the B6 category predicate misgrades the shipped grading check (`document_review_loop_prompts.md:31`, "needs a guess" is not category-expressible) and `findings-v1` has no `rule` or `wrong_outcome` (conceded); (b) the quote gate cannot work for the deletion fix the revise brief prefers (`prompts.md:53`) and the mapped span is lossy for replacements (conceded); (c) B1 says a prior of open or regressed sets the row for any row, which contradicts B7's terminal deferred row (conceded in round2-B); (d) B says "adds fields only" while deriving the verdict on read and never storing it (VM-3), and B5 can yield REVISE with an empty Reviser brief (conceded).

---

## VARIANT A (guarded one-pass silence-clear; reviewer types blocking; verdict derived on read; defer with owner and expiry)

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Completeness | 1 | Covers all explicit requirements from source input | MET (1) | Sections 1-7 map to the C-02 row (clearing, blocking authority, verdict on read, defer owner and expiry) and to the six required sections; section 6 covers PR review and rf-qa; section 7 is the strongest objection. |
| Completeness | 2 | Edge cases and failure scenarios | MET (1) | Section 3.1 items 1-4 (empty block from one reviewer, invalid-block reviewer, one-reviewer re-review) and section 5 item 1 (D-11 A, B, C replay cases; "an empty diff leaves every prior blocking finding open"). |
| Completeness | 3 | Dependencies and prerequisites | MET (1) | Section 1 and 4: Q comes from slot C-03; `findings_v2.py:279-281` rejects prior lines so a v2 module needs C-01's carrier (section 6); pins to rewrite per LG-4 (section 4). |
| Completeness | 4 | Success or completion criteria | MET (1) | Section 5: deterministic cases with asserted outcomes (L1 stays `resolved_check`, FAIL, `unverified_ids = [L1]`) and a falsifier "A is wrong if its false-clear rate is not clearly below the control's". |
| Completeness | 5 | Explicit out of scope | MET (1) | Section 4: "Items in the slot's neighbourhood that A neither fixes nor depends on: the new-text hash..., the lock on the ledger file (FX-12)..."; "INV-I, round-1 partial panel ... outside this slot". |
| Correctness | 1 | No factual errors or hallucinated claims | NOT MET (0) | Section 2 says `--resolution` carries requested ids the guard "counts" (`merge_cmd.py:50-56, 74-83`) but the debate showed counting is new code (round2-A evidence 7); "recorded completion state is `complete`" (section 1) has no merge-path source, only `block_ok` (round1-A concession 6). |
| Correctness | 2 | Technical approaches feasible with stated constraints | NOT MET (0) | Section 2 "stays `resolved_check`" on dissent is swallowed by `ledger.py:328`; `expires_round` inert at cap 3 with VM-6; quorum above panel size deadlocks the one-reviewer re-review (all conceded in round 2). |
| Correctness | 3 | Terminology consistent and accurate | NOT MET (0) | Section 1 uses "complete reviewers" (recorded completion state) while the section 2 table counts `block_ok`; "complete" is not a state in this merge path (round1-A concession 6). |
| Correctness | 4 | No internal contradictions | NOT MET (0) | Section 2 `defer` returns a row to `open` at the expiry round, but section 2 adopts VM-6 (no round after ESCALATE) and ESCALATE when every remaining row is deferred, so expiry can never fire (round2-A evidence 5). |
| Correctness | 5 | Claims supported by evidence or rationale | MET (1) | Every claim carries a tag and file:line (section 3 items 1-14; "[CODE-CONTRADICTED] the docstring at `ledger.py:112-113`") and the objection answer in section 7 gives three numbered rationales. |
| Structure | 1 | Logical section ordering | MET (1) | Position (1), core and module consequence (2), evidence (3), invariants (4), test (5), PR and rf-qa effect (6), objection (7); invariants refer back to sections 2 and 3. |
| Structure | 2 | Consistent hierarchy depth | MET (1) | Seven H2 sections; H3 subsections 3.1-3.4 all populated and none orphaned; sections 2 and 4 use tables at one level. |
| Structure | 3 | Separation of concerns | MET (1) | Design (section 2), evidence (3), invariants (4), measurement (5), consumer effect (6) and objection (7) are separate sections with no mixed content. |
| Structure | 4 | Navigation aids | MET (1) | Section cross-references throughout ("section 5", "section 2", INV-A to INV-N rows, evidence item numbers, research/NN pointers); no table of contents, cross-references satisfy the criterion. |
| Structure | 5 | Follows artifact-type conventions | MET (1) | Position paper header (slot, slug, Date, Position, Status: Complete), tag legend, path convention line, and the six implied sections in order. |
| Clarity | 1 | Unambiguous language | MET (1) | Grep for "should consider, might, as appropriate, as needed, properly, adequate, various, etc." finds no match; rules are stated as exact guards (`count(...) >= Q`, `defer(ledger, lid, reason, owner, expires_round)`). |
| Clarity | 2 | Concrete rather than abstract | MET (1) | Section 2 table names the function, line range and new field per change (`ledger.py:254-258`, `unverified_ids`, `held` event with reason `no-examination-record`). |
| Clarity | 3 | Section purpose clear | MET (1) | Section 1 is "the position in one paragraph"; each H2 title states its single purpose (evidence, invariants, test or measurement, effect, strongest objection). |
| Clarity | 4 | Acronyms and domain terms defined on first use | NOT MET (0) | No evidence found - searched sections 1-7: D-1, D-11, FX-12, FX-17, X-14, LG-2, LG-4, VM-3, C-S8, E2, DEGRADED are used without definition (only the tag legend and INV rows are glossed). |
| Clarity | 5 | Actionable next steps or decision points | MET (1) | Section 5 items 3-4 (three-arm replay, rule registered before the first run) and section 7 "the one question the section 5 measurement answers" with the decision on each outcome. |
| Risk | 1 | At least 3 risks with probability and impact | NOT MET (0) | Section 4 "Endangered or open" table has 6 items with severity (MEDIUM, LOW, HIGH) but no probability; the held-round cost says its rate "is unmeasured". |
| Risk | 2 | Mitigation for each identified risk | NOT MET (0) | Mitigations exist for INV-D (tolerant readers) and INV-N (mirror edit), but "Typed blocking residue ... A leaves it" and INV-I round-1 partial panel "outside this slot" have none. |
| Risk | 3 | Failure modes and recovery | MET (1) | Section 4 "Held-round cost": fail-closed, bounded by the cap, ends in ESCALATE; INV-J: "A held row consumes a review, never a fourth one"; ESCALATE goes to the user. |
| Risk | 4 | External dependencies and failure scenarios | MET (1) | Section 3.4 item 13: blind-grader `compute_verdict` exists but its integrity check returns `EXIT_OK` in every branch and the live trial was invalid; section 4: dependence on C-03 is "HIGH if C-03 leaves it open". |
| Risk | 5 | Monitoring or validation mechanism | MET (1) | Section 5 items 3-4: false-clear rate, false-hold rate, compliance fraction, reviews to terminal state per arm; plus runtime `held` events and `unverified_ids` in merge output. |
| Invariant and Edge | 1 | Collection boundaries (empty, single, max) | MET (1) | Section 3.1 item 3 (one empty block clears a row found by 3 of 3), item 4 (single-reviewer re-review, `apply_to` first), section 2 row Requested reviewers (requested reviewer with no report counts as not complete). |
| Invariant and Edge | 2 | State variable interactions across boundaries | MET (1) | Section 3.3 items 8-9: stored verdict stale after `apply_revision` moves rows to `resolved_check`; `defer` overwrites `verdict` and `decision`; section 2 Verdict row derives them on read. |
| Invariant and Edge | 3 | Guard condition gaps | MET (1) | Section 3.1 item 1 (`block_ok` returned at `:295` and read nowhere in the clearing loop); section 3.3 item 9 (`defer` has no status guard); section 4 typed-`blocking` residue (only MINOR plus blocking rejected). |
| Invariant and Edge | 4 | Count divergence (off-by-one, inclusive or exclusive) | MET (1) | Section 2 Verdict row "ESCALATE if `n >= cap`" and the guard `count(reviewers with block_ok true) >= Q` against requested ids; section 4 "never a fourth one" fixes the cap boundary. |
| Invariant and Edge | 5 | Interaction effects when components combine | MET (1) | Section 3.1 item 4 (one-reviewer default makes the examination record, not the quorum count, do the work); section 4 INV-J (empty diff plus `named_not_touched` never reaches `resolved_check`); defer plus re-find (section 3.3 item 9). |

### Variant A subtotals

| Dimension | Score |
|---|---|
| Completeness | 5/5 |
| Correctness | 1/5 |
| Structure | 5/5 |
| Clarity | 4/5 |
| Risk Coverage | 3/5 |
| Invariant and Edge Case Coverage | 5/5 |
| **TOTAL (A)** | **23/30** |

---

## VARIANT B (explicit per-row verification; blocking by script predicate or blind grader; deferred row terminal and counted open)

| Dimension | # | Criterion (short) | Verdict | Evidence (one line, no pipes) |
|---|---|---|---|---|
| Completeness | 1 | Covers all explicit requirements from source input | MET (1) | Header names LG-1, VM-2, VM-4, C-S9; sections 1-7 cover clearing (B1-B4), verdict (B5), blocking authority (B6), defer (B7) and all six implied sections including section 6 (PR review and rf-qa) and section 7 (objection). |
| Completeness | 2 | Edge cases and failure scenarios | MET (1) | Section 5 T2 negative set (quote absent, invalid-block reviewer, prior resolved plus re-find, hash mismatch, round after ESCALATE); E4 (defer at round 3 turns ESCALATE into PASS). |
| Completeness | 3 | Dependencies and prerequisites | MET (1) | B4 needs `revise` to store `new_sha256`; "Not addressed by B ... quorum count (C-03)"; section 6 Location: quote check needs C-01's locator work for PR findings. |
| Completeness | 4 | Success or completion criteria | MET (1) | Section 5 T1-T5 with expected outcomes (L1 stays `resolved_check`, `verify_ids == ["L1"]`) and "B is shown wrong if M1 shows the quote check adds no power over silence". |
| Completeness | 5 | Explicit out of scope | MET (1) | Section 4: "Not addressed by B and left to other slots: the quorum count (C-03...); the rule when one valid reviewer is the only voice...; anchors and spans (DR-006, DR-108)". |
| Correctness | 1 | No factual errors or hallucinated claims | MET (1) | Citations were re-read by both advocates; the category list tagged UNVERIFIED (`prompts.md:31`) was confirmed to exist (round1-A, round1-B); the misgrading is a design flaw scored under Correctness 2, not a false citation. |
| Correctness | 2 | Technical approaches feasible with stated constraints | NOT MET (0) | B6 predicate misgrades the shipped grading check and needs fields `findings-v1` lacks; B3 quote gate cannot clear deletion fixes (`prompts.md:53`) and spans are lossy (`findings.py:431`); all conceded in round 2. |
| Correctness | 3 | Terminology consistent and accurate | MET (1) | Status names kept (`open, resolved_check, resolved, regressed, deferred`) and B1-B7 plus `brief_ids`, `verify_ids`, `held_ids`, `blocking_typed` are used identically in sections 1, 2, 5 and 6. |
| Correctness | 4 | No internal contradictions | NOT MET (0) | B1 "a prior of open or regressed sets the row" for any row contradicts B7 deferred row "terminal for the machine" (conceded in round2-B row on A-R1 W2); INV-D "adds fields only" against section 1 verdict "never stored" (VM-3, conceded). |
| Correctness | 5 | Claims supported by evidence or rationale | MET (1) | Evidence E1-E16 each cite file:line with tags (E1 `ledger.py:254-258`, E8 `review_ledger.py:1829-1853`); section 7 gives six bullets of rationale including the asymmetry argument. |
| Structure | 1 | Logical section ordering | MET (1) | Position (1), design 2.1 core then 2.2 modules, evidence (3), invariants (4), tests and measurement (5), effects (6), objection (7). |
| Structure | 2 | Consistent hierarchy depth | MET (1) | Seven H2 sections; H3 only 2.1 and 2.2, both populated; section 3 uses labelled lists (Defect side, Semantics side) without orphaned subsections. |
| Structure | 3 | Separation of concerns | MET (1) | Rules B1-B7 (design), E1-E16 (evidence), Preserves and Endangers (invariants), T and M items (tests), section 6 (consumers) are kept in separate sections. |
| Structure | 4 | Navigation aids | MET (1) | Local numbering with cross-references ("(E3)", "section 2.2", "B6", "T1 to T4", "section 5 agreement measurement"); no table of contents, cross-references satisfy the criterion. |
| Structure | 5 | Follows artifact-type conventions | MET (1) | Header with slot, conflict IDs, Position, Date, repository and HEAD, Status: Complete, tag rule, and the six implied sections in order. |
| Clarity | 1 | Unambiguous language | NOT MET (0) | Three behaviours are left optional or open: B7 "An expiry may be recorded; it has no machine meaning", B6 grader "optional per-lens stage that may overwrite", B3 "the exact normalisation is module work". |
| Clarity | 2 | Concrete rather than abstract | MET (1) | B6 spells out the spec-lens predicate by severity and category (CRITICAL; MAJOR for contradiction, unpassable-check, data-loss, safety); B5 lists the three derived id sets with exact status membership. |
| Clarity | 3 | Section purpose clear | MET (1) | Section 1 is the one-paragraph position; each H2 title names its single purpose; section 3 opens with "Numbering E1.. is local to this file". |
| Clarity | 4 | Acronyms and domain terms defined on first use | NOT MET (0) | No evidence found - searched sections 1-7: D-1 (section 5 T1), R7, R2, M9, P12, DR-006, DR-108, FX-9, FX-11 are used without definition (only INV rows and the tag rule are glossed). |
| Clarity | 5 | Actionable next steps or decision points | MET (1) | Section 5 M2 "free pre-measurement ... count how many carry one prior line per live blocking row" and the two stated falsifiers; section 7 names M1 as the result that would show B adds no power. |
| Risk | 1 | At least 3 risks with probability and impact | NOT MET (0) | Section 4 Endangers lists INV-D, INV-C, INV-J (MEDIUM) and INV-N, INV-H (LOW) with severity only; no probability; E16 cost is "unmeasured". |
| Risk | 2 | Mitigation for each identified risk | NOT MET (0) | INV-D, INV-H (not copied into telemetry) and INV-N have mitigations, but INV-J (B6 can flip a typed non-blocking MAJOR to blocking) is met only by the M3 measurement, with no mitigation. |
| Risk | 3 | Failure modes and recovery | MET (1) | Section 7 asymmetry bullet: if the cost estimate is wrong the result is rows held and "an ESCALATE at the 3-review cap with the unanswered rows listed: bounded by `cap_reviews`, visible"; E15 on fail-open gates. |
| Risk | 4 | External dependencies and failure scenarios | MET (1) | E15: `stoprule.py` `cmd_verify_transcript` returns `EXIT_OK` in every branch so B requires the check to gate, not warn; B6 makes the blind grader optional so the core does not depend on it; C-01 and C-03 dependencies. |
| Risk | 5 | Monitoring or validation mechanism | MET (1) | Section 5 M1 (wrongly cleared and wrongly held rows per arm), M2 (prior-line compliance) and M3 (predicate flip count against typed blocking). |
| Invariant and Edge | 1 | Collection boundaries (empty, single, max) | MET (1) | T1 (one reviewer returns an empty block), E2 (a standard re-review is one reviewer, `apply_to` first), B2 and the zero-valid-block refusal (`ledger.py:150-157`) kept. |
| Invariant and Edge | 2 | State variable interactions across boundaries | MET (1) | B4 binds `revise` (`new_sha256`) to `merge` (`doc_text` hash, `ledger.py:279`); B5 and E5 stored verdict stale after `apply_revision`; B7 `defer` no longer rewrites `last["verdict"]`. |
| Invariant and Edge | 3 | Guard condition gaps | MET (1) | E1 (`block_ok` returned and never read), E4 (`defer` no status guard), E6 (`CRITICAL` with `blocking: false` accepted, only MINOR plus blocking rejected), B4 (round after ESCALATE: only `n == len(rounds)+1` is checked). |
| Invariant and Edge | 4 | Count divergence (off-by-one, inclusive or exclusive) | MET (1) | B5 "REVISE while `n < cap_reviews` and ESCALATE at the cap (`_decision`, `ledger.py:93-96`)" and "cap_reviews stays 3"; B4 round counter `n == len(rounds)+1`. |
| Invariant and Edge | 5 | Interaction effects when components combine | MET (1) | Section 4 INV-J (B6 predicate against the by-consequence grading at `spec-panel.md:259`); B7 deferred row plus re-find (`refound_deferred`); E2 (one-reviewer default weakens an unquoted resolved). |

### Variant B subtotals

| Dimension | Score |
|---|---|
| Completeness | 5/5 |
| Correctness | 3/5 |
| Structure | 5/5 |
| Clarity | 3/5 |
| Risk Coverage | 3/5 |
| Invariant and Edge Case Coverage | 5/5 |
| **TOTAL (B)** | **24/30** |

---

## Qualitative summary (pass 1)

| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant and Edge | Total | qual_score |
|---|---|---|---|---|---|---|---|---|
| A | 5 | 1 | 5 | 4 | 3 | 5 | 23/30 | 0.767 |
| B | 5 | 3 | 5 | 3 | 3 | 5 | 24/30 | 0.800 |

Verdict-sensitive criteria (most likely to flip in pass 2): Correctness 1 for A (the `--resolution` overstatement and the "complete" state are real but small), Correctness 3 for A and B, Clarity 1 for B (optional-behaviour wording, no listed hedge phrase present), Risk 1 and 2 for both (severity given, probability absent; mitigation absent for one risk each), Invariant and Edge 4 for both (cap boundary stated, no explicit divergence analysis).

## Edge-case-floor check (Invariant and Edge Case Coverage >= 1/5)

- Variant A: 5/5, eligible as base.
- Variant B: 5/5, eligible as base.
- Floor suspension not needed.
