# ab6 Jev replay gates: live results (13 specs, 1,142 Jev calls, about $0.04; key scan clean)

Run 2026-11-10. Controls: 26 Sonnet workers on identical packets. All ledger statuses from the Sonnet blind scoring.

| seam | gate | result | verdict |
|---|---|---|---|
| A1 obligation-to-criterion support | prefilter recall >= 70% (cap 60) | pair level 28.2%, defect-cell level 67.9% | FAIL (recall curve: 90 pairs 36.9%/73.6%, 400 pairs 57.8%/82.1%) |
| | <= 8 false flags per spec | mean 1.58, max 4 (worst-case bound with unmapped: 12) | pass |
| | >= 1 beyond-control catch | 1 (D26, one spec) | pass (thin) |
| | not tied by conventional judge | Jev 19 false vs judge 10 false; Jev-only catch 1, judge-only 0 | pass |
| A2 acceptance-check observability | >= 3 tail defects caught beyond controls | 11 distinct tail defects (D15-D19, D23, D37-D40, D44); 131 cells | pass, with caveat |
| | precision | NOT measured: 113 flagged rows map to no residual ledger defect (upper bound on false flags); Sonnet judge flagged 0 | open |
| A3 revision novelty | Jev separates resolved from failed V2 cases | no (Fisher p 0.13 / 0.44 / 1.0, n=10 cases, 2 resolved) | FAIL, drop |

Answer distribution (caution): Jev answers `cannot_pass` on 82 of 93 usable A2 rows (88%) while the Sonnet judge says `can_pass` on 349 of 352 (99%). On A1 Jev says `supported` on 9 of 476 usable calls, the Sonnet judge on 207 of 780. Jev is strongly negative-biased, so a high catch count there is expected and says little about precision until the flagged rows are labelled independently.

Decision: A3 dropped. A1 killed by its recall rule unless a larger cap is accepted (cap 90 gives 73.6% defect-cell recall; not chosen). A2 proceeds as a flag-only shadow seam with an independent row-labelling step before it is allowed to influence any gate.
