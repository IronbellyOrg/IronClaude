# Round 2 rebuttal: Variant 2 (sonnet:analyzer)

## Responses to criticisms

- **12-item cap crowds out classes (V1, V3).** Conceded. My fixed per-class caps (Q2/U2/M2/R2/S2) are replaced by V1's quota: 1 to 2 items per triggered class, remaining slots filled by ranked trigger strength, and a dropped-item log that records every omission.
- **1.6 x deadline (V1).** Conceded as written. It is a hang guard at 1.5 x (the X-005/X-008 outcome), not an acceptance limit. +35% is judged on medians, and I rely on no kill.
- **3(f) adds H and redesign.** Conceded again. The +0.14 is borrowed, and the two shares are reported separately from Z0, Z0-raw and the redesign arms. No headline sum.
- **254-run cost (V1).** Accepted. I stage the arms: Stage 1 runs Z0, Z0-raw, K, A and B on the real packages. The planted-defect, clean-twin, spec/doc and sonnet/haiku sets run only for arms that pass D1. Merging P into K removes one arm. I have not recounted the total.
- **+22 s luna load unmeasured.** Conceded. A 5-run timing spike on luna comes before any arm runs. If luna's median plus overhead exceeds the +35% cell, luna's share drops to 8 items.
- **V1's auto-promotion fix.** I move. The harness builds no claim; it copies the reviewer's own row, as a MINOR non-blocking finding tagged `src=ledger`, so my objection (script-authored findings) is met. It is reported separately and is never blocking.
- **V1's second ember session.** It adds load and a second variable to an A-versus-B comparison that should isolate prompt-only. I keep one session.

## Open design questions

- Q1: No; the blind verifier stays off the critical path, in the off-path audit only.
- Q2: Yes; data cards, flat extractors and a block-kind checklist, with no adapter code until a second target exists.
- Q3: Yes; at most 12 items, each to exactly 2 blind reviewers, a quota of at least 1 and at most 2 items per triggered class, the rest ranked, with a dropped-item log.
- Q4: Yes; a MINOR non-blocking finding built from the reviewer's row, tagged `src=ledger` and reported separately.
- Q5: V2: one session per reviewer with at most 4 recipes.
- Q6: Yes; one generic-checklist arm K naming the eight checks in plain words, plus Z0-raw.
- Q7: Yes; labels B1..I7 throughout, with I7 (control package, scored /2) outside every "of 14" sum.
- Q8: Yes; the mean of the V1 and V2 matrices, labelled planning values, replaced by the measured act rate.
- Q9: Yes; per-package medians against the slowest-reviewer baseline, a 1.5 x hang guard, and a pre-pass kill at 15 s with fallback to the isolated brief.
- Q10: Yes; D1-D6 plus G5 and G7 plus the package-level bootstrap, with consistent meaning reached in at least 60% of runs.

## Contested points

| point | choice | moved? |
|---|---|---|
| C-003 | COMBINE V1+V2 (route and replicas as card data; 2 blind replicas, slow-model cap) | no |
| C-005 | COMBINE V1+V2 (substring check, demote unsupported rows, ledger promotion tagged `src=ledger`, non-blocking, reported separately) | yes |
| C-012 | V2 (verified sums are planning bounds, replaced by measured values) | no |
| C-013 | V2 (matrices tied to the cause map; planning values only) | no |
| C-018 | COMBINE V2+V1 (CB-3 sentence plus two quotes for blocking; clean-twin gate; +1.0 wrong-blocker limit) | yes |
| C-020 | COMBINE V1+V2 (V1 data cards with flat extractors; V2 line counts) | yes |
| C-023 | COMBINE V1+V2+V3 (union of failure rows, including verifier false negatives and flood in the off-path audit) | yes |
| X-003 | V2 (about 2 s per item, valid up to 12 items) | no |
| A-001 | V2 (act-rate readout replaces probabilities) | no |
| A-002 | V2 (sums are planning bounds only) | no |
| A-004 | COMBINE V2+V3 (H3 precondition, snapshot hash, `.dev/` excluded from sweeps, 15 s kill, fallback to the isolated brief) | yes |
