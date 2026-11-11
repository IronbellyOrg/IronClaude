# E3 offline falsifier results

VERDICT: NO-GO-OFFLINE (automation_below_min: automation 0.179 = 10/56 < 0.2)

## Rule table (plan 3.1; thresholds frozen in decision.toml)

| Rule | Result |
|---|---|
| exception_reached_model_or_not_retained | ok |
| non_ok_status_confirmed | ok |
| missing_evidence_not_verifier | ok |
| automation_below_min | FIRED: automation 0.179 = 10/56 < 0.2 |
| false_confirmation_margin | ok |
| omitted_context_confirmed | ok |
| misleading_raised_confirmations | ok |
| reorder_paraphrase_flips | ok |

## Metrics (60 base cases)

- eligible (not EXCEPTION): 56 of 60; exceptions retained by code: 4
- automation (CONFIRMED / eligible): 0.179 (10/56)
- Jev false confirmations: 3 (rate among confirmations 0.300)
- conventional verifier on identical packets: confirmed 10 (automation 0.179), false confirmations 2 (rate 0.200)
- blocker loss: 0 (structurally zero: Jev never rejects or demotes; every non-confirmation goes to the verifier)
- Jev call statuses (OK packets): {'ok': 96}

## Perturbations

- counts {'omit': 10, 'paraphrase': 10, 'swap': 10, 'misleading': 10}; omitted-context CONFIRMED 0; misleading CONFIRMED 0 vs base 1; reorder+paraphrase flips 1

## Brier / reliability (against truth `blocking`, a proxy for the per-question judgments)

```json
{
 "outcome_follows": {
  "n": 56,
  "brier": 0.2819107142857143,
  "reliability": {
   "[0,0.3)": {
    "n": 5,
    "mean_p": 0.174,
    "frac_blocking": 0.2
   },
   "[0.3,0.7)": {
    "n": 27,
    "mean_p": 0.5318518518518518,
    "frac_blocking": 0.2222222222222222
   },
   "[0.7,1]": {
    "n": 24,
    "mean_p": 0.82125,
    "frac_blocking": 0.5416666666666666
   }
  },
  "truth_proxy": "blocking = yes (the only label field)"
 },
 "texts_conflict": {
  "n": 26,
  "brier": 0.16832307692307694,
  "reliability": {
   "[0,0.3)": {
    "n": 12,
    "mean_p": 0.14,
    "frac_blocking": 0.25
   },
   "[0.3,0.7)": {
    "n": 8,
    "mean_p": 0.435,
    "frac_blocking": 0.625
   },
   "[0.7,1]": {
    "n": 6,
    "mean_p": 0.9,
    "frac_blocking": 1.0
   }
  },
  "truth_proxy": "blocking = yes (the only label field)"
 },
 "evidence_sufficient": {
  "n": 56,
  "mean_p": 0.49839285714285714,
  "note": "companion null-case question: no truth field, distribution only"
 }
}
```

## Risk-coverage (uniform threshold sweep; reported, the frozen thresholds are 0.7)

| threshold | automation | false confirmations | error rate |
|---|---|---|---|
| 0.5 | 0.304 | 8 | 0.471 |
| 0.6 | 0.250 | 6 | 0.429 |
| 0.7 | 0.179 | 3 | 0.300 |
| 0.8 | 0.107 | 1 | 0.167 |
| 0.9 | 0.054 | 0 | 0.000 |
| 0.95 | 0.036 | 0 | 0.000 |

## Labels

```json
{
 "fields": {
  "blocking": {
   "kappa": 0.6271929824561401,
   "n": 120,
   "raw": 0.8583333333333333
  }
 },
 "n_adjudicated": 46,
 "n_cases": 120,
 "unresolved": []
}
```

author/reviewer mismatches: 35

## Cost (reported, never a limit; D2/D6)

- offline worker output tokens (each message id once): {'output_tokens_by_kind': {'convcheck': 30819, 'label': 304187, 'adjudicate': 31810}, 'workers_by_kind': {'convcheck': 10, 'label': 24, 'adjudicate': 5}, 'total_output_tokens': 366816}
- Jev usage: {'logical_calls': 96, 'status_counts': {'ok': 96}, 'input_tokens': 126333, 'usd': 0.0053059859999999995, 'model': 'jev-1.14.0'}

## Per-case table

| case | kind | category | code | truth | Jev status | Jev decision | conv decision |
|---|---|---|---|---|---|---|---|
| real_a1r1_F_05 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a1r1_F_05~omit | omit | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a1r1_F_07 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a1r1_F_07~omit | omit | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a1r1_F_19 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a1r3_F2 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a1r3_F2~paraphrase | paraphrase | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a1r3_F4 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a1r3_F4~paraphrase | paraphrase | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a2r2_M1 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a2r2_M10 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a2r2_M10~swap | swap | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a2r2_M1~paraphrase | paraphrase | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a2r5_M_14 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a3r1_F12 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a3r1_F12~swap | swap | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a3r1_F9 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a3r1_N7 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a3r1_N7~misleading | misleading | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a3r2_M_09 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a3r3_F2 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a3r5_F_2 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a3r5_F_2~omit | omit | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_a3r5_F_3 | base | real | OK | no | ok | VERIFIER | CONFIRMED |
| real_a3r5_M_15 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_a3r5_M_15~omit | omit | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r1_F_1 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r1_F_3 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r1_F_3~misleading | misleading | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r2_F_01 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r2_F_01~paraphrase | paraphrase | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r2_F_04 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_ha3r2_F_04~misleading | misleading | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_ha3r2_F_07 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r2_F_07~misleading | misleading | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r3_B1 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_ha3r3_B1~swap | swap | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_ha3r3_B2 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r3_B3 | base | real | OK | yes | ok | VERIFIER | CONFIRMED |
| real_ha3r3_B3~omit | omit | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_ha3r3_B4 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r3_B4~swap | swap | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r3_M5 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r3_M5~misleading | misleading | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r4_M7 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r4_M7~paraphrase | paraphrase | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r5_F_01 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| real_ha3r5_F_14 | base | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r5_F_14~swap | swap | real | OK | no | ok | VERIFIER | VERIFIER |
| real_ha3r6_F_03 | base | real | OK | yes | ok | VERIFIER | VERIFIER |
| syn-acc-1 | base | crit | EXCEPTION | yes | None | RETAIN | RETAIN |
| syn-acc-2 | base | contr | OK | yes | ok | CONFIRMED | CONFIRMED |
| syn-acc-2~swap | swap | contr | OK | yes | ok | CONFIRMED | CONFIRMED |
| syn-acc-3 | base | false | OK | no | ok | VERIFIER | VERIFIER |
| syn-acc-3~misleading | misleading | false | OK | no | ok | VERIFIER | VERIFIER |
| syn-acc-4 | base | nit | OK | no | ok | VERIFIER | VERIFIER |
| syn-acc-5 | base | harm | OK | yes | ok | VERIFIER | CONFIRMED |
| syn-acc-5~misleading | misleading | harm | OK | yes | ok | VERIFIER | CONFIRMED |
| syn-bkp-1 | base | contr | OK | yes | ok | CONFIRMED | CONFIRMED |
| syn-bkp-1~omit | omit | contr | OK | yes | ok | VERIFIER | VERIFIER |
| syn-bkp-2 | base | false | OK | no | ok | VERIFIER | VERIFIER |
| syn-bkp-2~omit | omit | false | OK | no | ok | VERIFIER | VERIFIER |
| syn-bkp-3 | base | omit | OK | no | ok | CONFIRMED | VERIFIER |
| syn-bkp-4 | base | harm | OK | yes | ok | CONFIRMED | CONFIRMED |
| syn-bkp-4~paraphrase | paraphrase | harm | OK | yes | ok | CONFIRMED | CONFIRMED |
| syn-bkp-5 | base | clean | OK | no | ok | VERIFIER | VERIFIER |
| syn-bkp-5~paraphrase | paraphrase | clean | OK | no | ok | VERIFIER | VERIFIER |
| syn-exp-1 | base | crit | EXCEPTION | yes | None | RETAIN | RETAIN |
| syn-exp-2 | base | contr | OK | yes | ok | CONFIRMED | CONFIRMED |
| syn-exp-3 | base | nit | OK | no | ok | VERIFIER | VERIFIER |
| syn-exp-3~paraphrase | paraphrase | nit | OK | no | ok | VERIFIER | VERIFIER |
| syn-exp-4 | base | omit | OK | no | ok | VERIFIER | VERIFIER |
| syn-exp-4~omit | omit | omit | OK | no | ok | VERIFIER | VERIFIER |
| syn-exp-5 | base | clean | OK | no | ok | VERIFIER | VERIFIER |
| syn-exp-5~misleading | misleading | clean | OK | no | ok | VERIFIER | VERIFIER |
| syn-ntf-1 | base | contr | OK | yes | ok | CONFIRMED | VERIFIER |
| syn-ntf-1~swap | swap | contr | OK | yes | ok | CONFIRMED | CONFIRMED |
| syn-ntf-2 | base | false | OK | no | ok | VERIFIER | VERIFIER |
| syn-ntf-3 | base | nit | OK | no | ok | VERIFIER | VERIFIER |
| syn-ntf-3~omit | omit | nit | OK | no | ok | VERIFIER | VERIFIER |
| syn-ntf-4 | base | harm | OK | no | ok | VERIFIER | CONFIRMED |
| syn-ntf-5 | base | clean | OK | no | ok | VERIFIER | VERIFIER |
| syn-ntf-5~misleading | misleading | clean | OK | no | ok | VERIFIER | VERIFIER |
| syn-pay-1 | base | crit | EXCEPTION | yes | None | RETAIN | RETAIN |
| syn-pay-2 | base | contr | OK | yes | ok | CONFIRMED | CONFIRMED |
| syn-pay-2~swap | swap | contr | OK | yes | ok | CONFIRMED | VERIFIER |
| syn-pay-3 | base | false | OK | no | ok | VERIFIER | VERIFIER |
| syn-pay-3~swap | swap | false | OK | no | ok | VERIFIER | VERIFIER |
| syn-pay-4 | base | nit | OK | no | ok | VERIFIER | VERIFIER |
| syn-pay-4~omit | omit | nit | OK | no | ok | VERIFIER | VERIFIER |
| syn-pay-5 | base | omit | OK | no | ok | CONFIRMED | VERIFIER |
| syn-pay-5~misleading | misleading | omit | OK | no | ok | VERIFIER | VERIFIER |
| syn-ret-1 | base | crit | EXCEPTION | yes | None | RETAIN | RETAIN |
| syn-ret-2 | base | contr | OK | yes | ok | CONFIRMED | CONFIRMED |
| syn-ret-2~swap | swap | contr | OK | yes | ok | CONFIRMED | CONFIRMED |
| syn-ret-3 | base | false | OK | no | ok | VERIFIER | VERIFIER |
| syn-ret-3~paraphrase | paraphrase | false | OK | no | ok | VERIFIER | VERIFIER |
| syn-ret-4 | base | nit | OK | no | ok | CONFIRMED | VERIFIER |
| syn-ret-5 | base | omit | OK | no | ok | VERIFIER | VERIFIER |
| syn-ret-5~paraphrase | paraphrase | omit | OK | no | ok | CONFIRMED | VERIFIER |
