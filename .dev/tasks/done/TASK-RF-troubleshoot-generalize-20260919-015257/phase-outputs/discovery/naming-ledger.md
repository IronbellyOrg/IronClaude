# Naming ledger (item 0.7 — G-07 rule 1)

Source: `research/07-gap-fill-reconcile.md` §X-3 (flags), §depth-3 (test modules), §G-07; D9/D10/R-05 (ref paths); `research/03-spec-extraction.md` §0.3 (removed names). No later edit may introduce a name absent from this ledger.

## (a) 19 flag names (reconcile §X-3)

- `deduced_headline` (A1)
- `instrumentation_without_falsifier` (A2)
- `timestamp_invalid` (A3)
- `verdict_not_in_contract` (A4)
- `consensus_on_unobserved` (A5)
- `reference_value_not_literal` (A6)
- `run_site_unresolved` (A7)
- `ci_verdict_unobserved` (A8)
- `probe_suspect` (A9)
- `capability_block_unproven` (A10)
- `headline_definite_low_confidence` (C1)
- `unproven_exclusion:<token>` (C2)
- `control_unproven` (C3)
- `locus_unknown` (C3b)
- `no_prereg_falsifier` (C4)
- `timestamp_invalid` (C5 — same token as A3)
- `bracket_unproven` (C6)
- `uncited` (C7)
- `behaviour-cite: missing` (C8)

## (b) card/field lines

- `runs-in=`
- `environment-property:`
- `behaviour-definition: row N`

## (c) contract/status tokens

- `execution_locus_card_path`
- `status: blocked`
- `blocked-on-authorization`
- `split_pending`
- `cosmetic_overrun`
- `contract_version 1.2.0`

## (d) tasklist header keys

- `discriminator-required`
- `re-run permitted`
- `capability-verdict`
- `indistinguishable`
- `probe-rows-truncated`

## (e) audit keys

- `optional_ref_absent`
- `<branch>:<repro-venue-id>`
- `bracket_trigger`

## (f) gate labels

- `HC0`
- `HC1`
- `HC2`
- `HC3`
- `HC4`
- `HC5`

## (g) four new ref paths

- `refs/agent-assertions.md`
- `refs/primitive-differential.md`
- `refs/environment-deltas.md`
- `refs/probe-packs/read-parse.md`

## (h) test modules (reconcile §depth-3)

- `_assertions.py`
- `_procedures.py`
- `test_validator_assertions.py` (T1)
- `test_calibrator_assertions.py` (T2)
- `test_producers_enumeration.py` (T3)
- `test_primitivegrep_targeting.py` (T4)
- `test_locus_card.py` (T5)
- `test_verdict_source.py` (T5b)
- `test_discriminator_form.py` (T6)
- `test_threshold_bracket.py` (T7)
- `test_cosmetic_counter.py` (T8)
- `test_counter_key.py` (T9)
- `test_hardstop_verdicts.py` (T10)
- `test_headline_threshold.py` (T11)
- `test_timestamp_tolerance.py` (T12)
- `test_inline_fallback_parity.py` (T13)
- `test_calibrator_eval_cases.py` (T14)
- `test_regression_sysbox.py` (T15)
- `test_primitive_differential.py` (T16)
- `test_discriminator_rows.py` (T17)
- `test_behaviour_definition_row.py` (T18)
- `test_menu_equality.py` (T19)
- `test_hc_rename_guard.py` (extra)

## (i) removed names that must NOT appear (v2:183 / 03 §0.3)

- `Wave 1.65`
- `discriminator-plan.md`
- `runtime-probe-pack.md`
- `discriminator-template.md`
- `bisect.md`
- `push-allowed`
- `predicted-passing-arm`
- `runtime=`
- `control_arm_unproven`
- `image-layers=`
- `bracket_uncited`
- `artifact_paths`
