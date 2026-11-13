# Base Selection

## Quantitative (50%)
- R2 (qa): 9 findings, 15 citations, broadest section coverage (covers A0-A6 + s17) -> RC 1.0 (amendments referenced), SC 1.0
- R1 (analyzer): 6 findings, 12 citations -> SC 0.85
- R3 (refactorer): 5 findings, 10 citations + shipped-code line evidence -> SC 0.8, SR highest (file:line in claims)

## Qualitative (50%, CEV)
- R2: completeness 5/5 (only card covering A5 dedup + s17 fail-open); correctness 5/5 (all quotes verified by calibrator); clarity 4/5
- R1: correctness 5/5; completeness 4/5 (no A5/s17); clarity 5/5
- R3: correctness 5/5; completeness 3/5; risk coverage 4/5 (only card with time-relative staleness)

## Combined
R2 0.86 > R1 0.82 > R3 0.78. Base: Variant 2 (qa/haiku). No tiebreaker needed.

## Strengths to incorporate
- From R1: the plan-line anchors (plan:44/61/91/95/102/147) for every cluster.
- From R3: shipped-code evidence citations (classifier.py:321,355-363; reviewers.py:337,375; test_run_log.py:171) proving each amendment landed outside the plan, and the time-relative staleness finding (CL-8).
