# Qualitative scoring, pass 1 of 2 (order: A first, then B)

Scorer: scorer-pass1. Documents scored as written: Variant A = variant-1-original.md ("Proposal A", re-find every round with D2, D3, D16 fixed). Variant B = variant-2-original.md ("Proposal B", find once then verify-only). Method: 30-criterion additive binary rubric with Claim-Evidence-Verdict. Each verdict row below is the CLAIM that the criterion is met in that variant; the evidence column is the support, and the verdict is MET or NOT MET. Spot-checks done: `src/superclaude/cli/review/ledger.py:93-157` (cap label at 93-96, round-order check at 114-118, docstring at 112, `block_ok` and the no-valid-block refusal at 150-157) and the C-16 recommended resolution in the synthesis file.

## Completeness

| criterion | variant | verdict | evidence (at most 25 words) |
|---|---|---|---|
| C1 | A | MET | Core changes 1-5 cover D16a/b, D3, D2; "D16c is closed as by design"; review-1 panel quorum; priors in seam table; seams table to C01/C02/C05/C12/C15/C16/C19 |
| C1 | B | MET | Core 3 round-1 merge; 3a D16c code mode; D2 positive clearing; D3 quorum; Core 11 one re-review protocol; P6 seams to C01/C02/C15/C16/C19 |
| C2 | A | MET | Degraded round, abstaining reviewer, refused would-be PASS, zero valid blocks, `--cap` mismatch, "Quorum denominator is wrong" risk |
| C2 | B | MET | Refusal codes E-INCOMPLETE/E-FROZEN/E-CAP, cannot-verify as X item, P5 fail-closed re-ask, risks 3, 8 |
| C3 | A | MET | Seams table; "Sequencing: Land changes 1 to 5 first... do not depend on C01, C02, C05 or C12"; C15 `rejected[]` prerequisite for change 5 |
| C3 | B | MET | "Order of work": round-1 fixes first, then port verify path; depends on C05/C12; New work 1-6 table |
| C4 | A | MET | Gate commands `uv run pytest tests/review/...` (37 tests) plus G10 group; P1-P6 properties; 15 listed tests define done |
| C4 | B | MET | Falsifier with named metrics and the experiment's within-arm spread screen; "adoption as the default stays conditional" |
| C5 | A | MET | "What Option A explicitly does not do": no verify-only mode, no positive clearing, no C05 decider; "Not costed here" row |
| C5 | B | MET | "What B decides and what it leaves alone" (C05, C12, C01, C15); PR and rf-qa modules "Later consumer... not designed here" |

Subtotal Completeness: A 5/5, B 5/5.

## Correctness

| criterion | variant | verdict | evidence (at most 25 words) |
|---|---|---|---|
| R1 | A | MET | Cited lines match code: `ledger.py:93-96`, `:114-118`, `:112` docstring, `:150-157` all verified in this pass; inferences are tagged |
| R1 | B | MET | Test counts reconcile (9 replaced + 15 kept = 24); ledger lines cited match; only C16 wording is arguable (see defects) |
| R2 | A | MET | Changes 1-5 are conditions added where inputs already exist (`block_ok`, resolution read, `_decision` cap); backward compatible under same schema string |
| R2 | B | MET | Port of a built 2,668-line script with 77 tests; stated cost XL; shim for `ledger revise` keeps loop prompt working |
| R3 | A | MET | `resolved_check`, `regressed`, "round", "degraded", "quorum", "valid" used consistently; evidence tags defined in citation key |
| R3 | B | NOT MET | `review ledger answer` = "Reviser claims from the fix map" but "Answer (one per plan row)" and "reviewer answers every plan row" mean the verifier's reply |
| R4 | A | MET | Change 4 (clear only if not degraded) matches Evidence item 4 and P3; no conflicting statements found |
| R4 | B | MET | Decision formula, Core 7 and CLI exit codes agree; Core 2 "never taken from a reviewer" is reconciled by Core 3 candidate-filter wording |
| R5 | A | MET | Each claim carries file:line or research section; P4 and sizes are labelled [INFERENCE]; E2 numbers labelled [DOC-SOURCED] |
| R5 | B | MET | Evidence E-1 to E-28 each tagged CODE-VERIFIED / DOC-SOURCED / ext; weakest point states what the evidence cannot show |

Subtotal Correctness: A 5/5, B 4/5.

## Structure

| criterion | variant | verdict | evidence (at most 25 words) |
|---|---|---|---|
| S1 | A | MET | Design, How it works, Evidence, Correctness argument, Risks, Test coverage, Cost: dependents follow what they need |
| S1 | B | MET | Same order: Design, How it works, Evidence (A-E), Correctness, Risks, Tests, Cost |
| S2 | A | MET | `##` sections with `###` subsections only; Evidence items 1-9 numbered consistently |
| S2 | B | MET | `##` sections; Evidence uses `###` A-E; Core numbered 1-12 (item "3a" is a small irregularity, not an orphan) |
| S3 | A | MET | Risks, tests, cost kept in own sections; Correctness holds guarantees plus "What A does not guarantee" |
| S3 | B | NOT MET | The Correctness section also holds the A-vs-B table, "The weakest point" and the falsifier run, which duplicate Risks and Test item 15 |
| S4 | A | MET | "Citation key" paragraph; cross-references "see Risks", "see Cost", "see Test coverage" |
| S4 | B | MET | "Citation key" paragraph; cross-references "Risks names it", "(Test coverage)", "see Cost" |
| S5 | A | MET | Design, evidence, risks, test coverage, cost sections present as a design proposal |
| S5 | B | MET | Design, evidence, risks, test coverage, cost sections present as a design proposal |

Subtotal Structure: A 5/5, B 4/5.

## Clarity

| criterion | variant | verdict | evidence (at most 25 words) |
|---|---|---|---|
| L1 | A | MET | Imperative, countable statements ("raises LedgerError when n > cap_reviews"); uncertainty is labelled [UNVERIFIED]/[INFERENCE], not hedged |
| L1 | B | MET | Concrete formula and refusal codes; "proposed" items are labelled as such, though rules 5, 11 stay conditional |
| L2 | A | MET | Three-round worked example; named fields, line numbers and exit codes |
| L2 | B | MET | Data-flow diagram, decision formula, CLI table with exit codes |
| L3 | A | MET | Each section has one stated purpose (one-sentence rule, seams, data flow, evidence, properties, risks) |
| L3 | B | MET | Each section has one stated purpose; "Position in one paragraph" summarizes the whole |
| L4 | A | MET | Key defines Cnn/Dnn/Gnn, E2, evidence tags; D2/D3/D16 glossed in the opening paragraph |
| L4 | B | NOT MET | "closes D1", "D3", "D16c" in Core 3-3a appear with no gloss or key entry for the D-codes; "CONTINUE" glossed only later |
| L5 | A | MET | "Sequencing" row gives order; risk table names the measurement and the trigger for a deferral policy |
| L5 | B | MET | "Decisions this proposal asks of the owner" (1)-(3); order of work; falsifier run stated |

Subtotal Clarity: A 5/5, B 4/5.

## Risk coverage

| criterion | variant | verdict | evidence (at most 25 words) |
|---|---|---|---|
| K1 | A | NOT MET | Eight risks listed but columns are Risk / Why it matters / Mitigation; no probability or impact rating (only "worst case is repeated escalations") |
| K1 | B | NOT MET | Ten risks with a Residual column; no probability rating and no explicit impact scale |
| K2 | A | MET | Every table row has a mitigation, including `--cap` default, seams, decider |
| K2 | B | MET | Every one of 10 rows has a Mitigation entry plus a Residual |
| K3 | A | MET | Refusal writes nothing; "only the missing reviewer is re-run"; degraded FAIL recorded; atomic save |
| K3 | B | MET | Refused answer set writes nothing; one re-ask then ESCALATE (P5); `--dry-run`; shim during migration |
| K4 | A | MET | "Quorum denominator" (failing reviewer), "Seams not ready" (C01/C12), PR bots re-trigger as external reviewers |
| K4 | B | MET | Risk 3 model compliance, Risk 4 C05/C12 dependency, Risk 9 served-model drift, Risk 7 external ledger files |
| K5 | A | MET | `unanswered_priors` telemetry; late-row rate "computable from existing ledgers"; store changed ranges "observation only" |
| K5 | B | MET | Falsifier run with spread screen; `would_block` on outside rows; served-model mismatch flag; sweep outcome |

Subtotal Risk coverage: A 4/5, B 4/5.

## Invariant and edge-case coverage

| criterion | variant | verdict | evidence (at most 25 words) |
|---|---|---|---|
| I1 | A | MET | Quorum `min(2, panel_size)`; single-reviewer quorum 1; zero valid blocks refused; tests 5-7 (k-1 vs k, missing reviewer) |
| I1 | B | MET | Test 6 "k-1 valid blocks cannot write PASS, k can"; one anchor reviewer in rounds 2-3; plan row unanswered refused |
| I2 | A | MET | Stored `cap_reviews` vs CLI `--cap` (D16b); `--resolution` panel size vs `--report` count; seams table across components |
| I2 | B | MET | Ledger phases, snapshot hashes and plan vs answers; `ledger revise` shim; resolution file vs round state |
| I3 | A | MET | `block_ok` "never read after :150"; docstring contradicted; `--round` help vs `IntRange(min=1)`; denominator guard |
| I3 | B | MET | Same `block_ok` gap (E-2); no integrity check on `load` (E-6); frozen-field and anchor-ambiguity refusals |
| I4 | A | MET | `n > cap` vs `n == len+1`; "never prints 4 of 3"; "1, 2 or 3" help text; quorum k-1 vs k |
| I4 | B | MET | E-5 "1, 2 or 3" over `IntRange(min=1)`; `begin` refuses fourth review or third fix cycle; quorum k-1 vs k |
| I5 | A | MET | Degraded + clearing (D2/D3 pinned together at `:376-385`); change 5 with C15 `rejected[]`; prior lines vs status invariant |
| I5 | B | MET | All-or-nothing verify vs C15 keep-valid-lines (P6); scope=outside rows + sweep; sweep exit 12 per profile |

Subtotal Invariant and edge-case coverage: A 5/5, B 5/5.

## Totals

| Dimension | Variant A | Variant B |
|---|---|---|
| Completeness (5) | 5 | 5 |
| Correctness (5) | 5 | 4 |
| Structure (5) | 5 | 4 |
| Clarity (5) | 5 | 4 |
| Risk coverage (5) | 4 | 4 |
| Invariant and edge cases (5) | 5 | 5 |
| **Total (30)** | **29** | **26** |

## Defects that affected a verdict

- B, R3: `ledger answer` is the reviser's claim step while "answer" in the verify step means the verifier's reply; one word, two roles.
- B, S3: Correctness section carries the comparison table, "The weakest point" and the falsifier, duplicating Risks and Test item 15.
- B, L4: D1, D3 and D16c are used in Core 3 and 3a without a gloss or a key entry (A defines them in its opening paragraph).
- A and B, K1: neither risk table gives a probability or an impact rating.
- B, not verdict-changing: Core 2 says `blocking` is "never taken from a reviewer" while synthesis C-16 says "keep the reviewer's flag as an input, record the effective flag"; Core 3 softens it to a "candidate filter".
- A, not verdict-changing: it says all five changes live in `ledger.py` and `merge_cmd.py`, but change 5 depends on C15's `rejected[]` field and two prompt-file copies also change.
- A, not verdict-changing: test-group labels "G10" and "G9" are used without a gloss in the key.
