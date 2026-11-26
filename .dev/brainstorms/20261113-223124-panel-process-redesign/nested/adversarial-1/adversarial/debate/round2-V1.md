# Round 2 rebuttal: Variant 1 (sonnet:architect)

## Responses to criticisms

- **Auto-promotion (V2, V3).** Partly conceded. The harness must not author a claim, and a substring match proves only that a quote exists. But the reviewer already wrote PROBLEM or DEFECT in its own ledger row, and the merge reads only the findings block, so without promotion the reviewer's own verdict is silently lost. Fix: append a MINOR non-blocking finding built from the reviewer's row, tag it `src=ledger`, never let it count toward blocking, and report it separately (V3's boundary). V3's blind verifier is not the alternative because it breaks +35%.
- **CB2 (V2, V3).** Conceded. The grading rule stays unchanged; CB2 runs only as its own arm. A1 contains CB1, CB3 and the blocker sentence, so redesign versus A1 stays clean.
- **Registry and adapter weight (V2).** Conceded. Ship data cards with flat extractors and a block-kind checklist; no adapter code before a second target.
- **Extractor caps and crowd-out (V2, V3).** Conceded the lack of ranking. My cap is per reviewer, but the final sheet needs a class quota, ranked selection and a dropped-item log.
- **E4 grep scope (V2).** Conceded. E4 is limited to tests, root documents and named paths; skip rather than grep `.dev/`.
- **Worst case relying on a kill (V2).** Conceded (X-005/X-008).

## Open design questions

- Q1: No; the blind verifier stays off the critical path, and may run only in the off-path audit.
- Q2: Yes.
- Q3: Yes: at most 12 items, each to exactly 2 reviewers; at least 1 and at most 2 items per triggered class, the remaining slots filled by ranked trigger strength, with a dropped-item log.
- Q4: Yes.
- Q5: V1: a second fresh ember session, launched only if the first ended before 0.45 x b, with at most 4 recipes per session.
- Q6: Yes.
- Q7: Yes.
- Q8: Yes.
- Q9: Yes.
- Q10: Yes.

## Contested points

| point | choice | moved? |
|---|---|---|
| C-003 | COMBINE V1+V2 (route as card data; replicas = 2 blind) | yes |
| C-005 | COMBINE V1+V3 (substring check; ledger promotion tagged and reported separately) | yes |
| C-012 | COMBINE V1+V2 (verified sums; measured values replace them) | no |
| C-013 | COMBINE V1+V2 (issue-id matrices, planning values) | no |
| C-018 | COMBINE V1+V2 (grading sentence plus two quotes; clean-twin gate) | no |
| C-020 | COMBINE V1+V2 (V1 data cards; V2 line counts) | yes |
| C-023 | COMBINE V1+V2+V3 (union of failure rows) | yes |
| X-003 | V2 (2 s per item up to 12 items) | yes |
| A-001 | V2 (act-rate readout replaces probabilities) | yes |
| A-002 | V2 (sums are planning bounds only) | yes |
| A-004 | COMBINE V2+V3 (H3 precondition, snapshot hash, 15 s kill, fallback) | yes |
