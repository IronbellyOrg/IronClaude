# Qualitative scoring, pass 2 of 2 (order: B first, then A), conflict C13 ledger-model

Variant B = `variant-2-original.md` (find once, then verify-only). Variant A = `variant-1-original.md` (re-find every round, D2/D3/D16 fixed). Each row reads as: CLAIM "criterion is met in variant X", EVIDENCE (quote or section), VERDICT. Spot-checks done: `review_ledger.py:60-67` and `:1586-1609` (for B's claims), `ledger.py:90-125` and `:250-342` (for A's claims).

## Completeness

| criterion | variant | verdict | evidence |
|---|---|---|---|
| C1 | B | MET | Core items 3, 3a, 4, 5, 7, 11 cover D2, D3, D16a-c, round-1 merge, `prior` protocol; position paragraph covers C01/C02/C05/C12/C15 seams |
| C1 | A | MET | Changes 1-5 cover D2, D3, D16a/b; D16c "closed as by design"; seams table C01/C02/C05/C12/C15/C16/C19; prior lines kept |
| C2 | B | MET | E-INCOMPLETE, cannot-verify as X item, tamper check, "refused answer set gets one re-ask; second refusal is an X item" |
| C2 | A | MET | Degraded round, missing reviewer "an abstention", refused would-be PASS, rejected blocking line cannot PASS |
| C3 | B | MET | "Order of work, as dependencies"; Risk 4 round 1 "depends on C05 and C12"; multi-path snapshots named as prerequisite |
| C3 | A | MET | Seams table; Sequencing row "do not depend on C01, C02, C05 or C12"; multi-file persistence attributed to C01/C12 |
| C4 | B | MET | Falsifier "stated before the run" with metrics and "larger within-arm spread" screen; decision formula; three owner decisions |
| C4 | A | MET | Gate commands (37 + 178 tests), properties P1-P6, 15 listed tests; weaker than B but present |
| C5 | B | MET | "What B decides and what it leaves alone"; PR module "fit shown, not designed here" |
| C5 | A | MET | "What Option A explicitly does not do"; "Not costed here" row lists C05, C19 B, multi-file rows, C11 |

Subtotal: B 5/5, A 5/5.

## Correctness

| criterion | variant | verdict | evidence |
|---|---|---|---|
| R1 | B | NOT MET | Core 11 cites `review_ledger.py:65` as answer status words; line 65 is `ANSWER_ACTIONS = ("fixed","not-fixed","disputed")`; `:1591` has four words |
| R1 | A | MET | Spot-checked `ledger.py:93-104,114-118,254-258,308-314,328-339` all match claims; no error found (not exhaustively checked) |
| R2 | B | MET | Port of built, tested 2,668-line script; shim for old loop; effort rated XL and not disputed |
| R2 | A | MET | Five local changes around existing calls; one-directional (refuse or withhold); additive keys under same schema string |
| R3 | B | NOT MET | "answer" names two things: `ledger answer` (reviser claims from fix map) and verifier "answers" per plan row |
| R3 | A | MET | round/review, quorum, degraded, abstention, valid/block_ok used consistently; status words match master ledger |
| R4 | B | MET | No contradiction found; sweep "mandatory for blocking" vs `sweep: none` profile is reconciled in item 8 |
| R4 | A | MET | No hard contradiction; "only the script changes a status" sits beside silence-based clearing, but that is disclosed |
| R5 | B | MET | Each property P1-P6 names E-items and line refs; claims tagged CODE-VERIFIED / DOC-SOURCED / inference |
| R5 | A | MET | Evidence sections 1-9 with tags; P4 labelled "[INFERENCE ... proof is by reading merge_round]" |

Subtotal: B 3/5, A 5/5.

## Structure

| criterion | variant | verdict | evidence |
|---|---|---|---|
| S1 | B | MET | Citation key, Design, How it works, Evidence, Correctness, Risks, Tests, Cost |
| S1 | A | MET | Same order; citation key first, seams before data flow |
| S2 | B | MET | Evidence A-E subsections; consistent `###`; "Weakest point" nested under Correctness |
| S2 | A | MET | Evidence items 1-9 as `###`; weakest point as lead paragraph of Risks |
| S3 | B | MET | Design, evidence, correctness, risks, tests, cost separated; comparison table confined to Correctness |
| S3 | A | MET | Sections separated; Evidence 6-7 carry rebuttal of B (mild blending, not disqualifying) |
| S4 | B | MET | "Citation key"; E-1..E-28 labels, P1-P6, Risk numbers cross-referenced in text |
| S4 | A | MET | "Citation key"; "Evidence item 4", "changes 1-5", "see Risks", "see Test coverage" cross-references |
| S5 | B | MET | Design, Evidence, Correctness, Risks, Test coverage, Cost all present |
| S5 | A | MET | Design, Evidence, Correctness, Risks, Test coverage, Cost all present |

Subtotal: B 5/5, A 5/5.

## Clarity

| criterion | variant | verdict | evidence |
|---|---|---|---|
| L1 | B | MET | Mostly firm; one soft line "should reduce tokens per round" is labelled as not counted as evidence |
| L1 | A | MET | Firm refusal rules; conditionals ("if the late-row measurement says so") are explicit triggers |
| L2 | B | MET | File:line refs, exact error codes (E-CAP, E-FROZEN), exit codes, field lists |
| L2 | A | MET | File:line refs, exact flag changes (`default=None`), field names, 15 concrete tests |
| L3 | B | MET | Each section has one stated purpose (Evidence opens with what it can and cannot show) |
| L3 | A | MET | Each section has one stated purpose; "Bottom line" summarises |
| L4 | B | MET | Glosses C05/C12/C01/C15 in position paragraph, E1-E3 in key; U, X, I defined in formula (used once before) |
| L4 | A | MET | D2/D3/D16 defined in opening paragraph; E2 defined; seams table glosses C-numbers |
| L5 | B | MET | "Decisions this proposal asks of the owner (1)(2)(3)"; "Order of work" |
| L5 | A | MET | "Sequencing" row and "Bottom line for the adversarial round"; no explicit owner-decision list |

Subtotal: B 5/5, A 5/5.

## Risk coverage

| criterion | variant | verdict | evidence |
|---|---|---|---|
| K1 | B | MET | 10-row table with "Why it is real" (evidence of likelihood) and "Residual" (impact), e.g. Risk 2 "no fix cycle left" |
| K1 | A | NOT MET | Table has "Why it matters" only; no likelihood per risk; weakest point says chance is unknown. No probability assessment |
| K2 | B | MET | Every row has a Mitigation entry |
| K2 | A | MET | Every row has a Mitigation entry |
| K3 | B | MET | Fail-closed refusal, one re-ask then ESCALATE (P5), `--dry-run`, shim during migration |
| K3 | A | MET | Refused degraded PASS: "only the invalid or missing reviewer is re-run"; nothing written on refusal |
| K4 | B | MET | Risk 4 (C05/C12 dependency), Risk 9 served-model drift, Risk 3 model compliance, external sources graded |
| K4 | A | MET | "Seams not ready", "Decider pre-empted", missing-reviewer abstention, PR bots re-trigger (weaker on provider failure) |
| K5 | B | MET | Falsifier run, `would_block` on outside rows, served-model mismatch flag, characterization test for E-4 |
| K5 | A | MET | `unanswered_priors` telemetry; late-row rate "computable from existing ledgers"; store changed ranges, observation only |

Subtotal: B 5/5, A 4/5.

## Invariant and edge case coverage

| criterion | variant | verdict | evidence |
|---|---|---|---|
| I1 | B | MET | Quorum boundary "k-1 valid blocks cannot write PASS, k can"; one anchor reviewer; cap boundary; no-valid-block test kept |
| I1 | A | MET | Quorum k-1 vs k test, single-reviewer quorum 1, zero valid blocks refused, round 4 and cap-2 tests |
| I2 | B | MET | Frozen fields vs decider hook; round-1 rows into `find`; snapshot hashes; `ledger revise` shim state equivalence test |
| I2 | A | MET | `--cap` vs stored `cap_reviews`; `--resolution` panel size vs `--report`; `degraded` gating clearing |
| I3 | B | MET | Master gaps named: `load` checks only schema string; `block_ok` never read after `:150`; E-4 three-line match |
| I3 | A | MET | D2 (`block_ok` unread), D3 (one valid block passes), D16 (no cap guard); `load` checks only schema |
| I4 | B | MET | `IntRange(min=1)` vs help "1, 2 or 3"; E-CAP on fourth review or third fix cycle; k-1 vs k |
| I4 | A | MET | `n > cap` plus `n == len(rounds)+1`; test "never prints `4 of 3`"; `min(2, panel_size)` |
| I5 | B | MET | Frozen blocking x C05 decider (Risk 4); verify all-or-nothing x C15 keep-valid-lines (P6); scope=outside x sweep |
| I5 | A | MET | Quorum x C15 rejected blocking lines; degraded x clearing; `--cap` default change x callers; decider x D4 |

Subtotal: B 5/5, A 5/5.

## Totals

| dimension | B | A |
|---|---|---|
| Completeness | 5 | 5 |
| Correctness | 3 | 5 |
| Structure | 5 | 5 |
| Clarity | 5 | 5 |
| Risk coverage | 5 | 4 |
| Invariant and edge cases | 5 | 5 |
| **Total of 30** | **28** | **29** |

## Defects that affected a verdict

- B, R1: Core item 11 cites `review_ledger.py:65` for the verifier's status words; line 65 holds the reviser actions fixed/not-fixed/disputed, and `:1591` has four words including cannot-verify. Minor mis-citation, strict reading gives NOT MET.
- B, R3: "answer" is used for the reviser's fix-map step (`ledger answer`) and for the verifier's per-plan-row answers (inherited from the script, not disambiguated).
- A, K1: risk table gives impact-side reasons only; no likelihood or probability per risk.

Noted, no verdict effect: B uses U, X, I in the data flow before the formula defines them. A's D2 fix gates clearing on whole-round `degraded`, so in a quorate round with one invalid reviewer the valid reviewers' silence still clears (A discloses this). B's external sources E-25..E-28 were not re-fetched (B discloses this). A and B read C16 differently (A: reviewer flag kept as input; B: predicate per lens in data); I could not settle which is right and gave no credit or penalty.
