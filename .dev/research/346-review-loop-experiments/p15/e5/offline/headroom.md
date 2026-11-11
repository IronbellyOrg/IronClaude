# E5 zero-call headroom

Generated 2026-11-10T06:25:28+00:00. Verdict: **NO-GO-OFFLINE** (headroom 1/11 (9.1%) < 2 packets or < 0.10).

## Decisive stratum (frozen baseline: p11 + p14)
packets 16; code-determined {'cap': 4, 'open_blocker': 0, 'unchanged_hash': 1, 'mandatory_policy': 0}; eligible 11; needs_assurance yes 10 (rate 0.909); headroom 1; sensitivity headroom 2; single-audit eligible 6

## Other designs (reported, not decisive)
packets 19; code-determined {'cap': 7, 'open_blocker': 0, 'unchanged_hash': 1, 'mandatory_policy': 0}; eligible 11; needs_assurance yes 11 (rate 1.0); headroom 0; sensitivity headroom 5; single-audit eligible 0

Escalated (no provisional PASS): 7; excluded runs: 25.

## Packets

| run | design | stratum | k | slots | reason | audits (verdict/blockers) | label | sens | headroom |
|---|---|---|---|---|---|---|---|---|---|
| a2-r1 | stage2-a2 | p11 | 2 | 1 | eligible | FAIL/2 | yes | yes | no |
| a2-r2 | stage2-a2 | p11 | 3 | 0 | cap | FAIL/2 | yes | yes | no |
| a2-r3 | stage2-a2 | p11 | 1 | 2 | unchanged_hash | FAIL/3 | yes | yes | no |
| a2-r4 | stage2-a2 | p11 | 2 | 1 | eligible | FAIL/3 | yes | yes | no |
| a2-r5 | stage2-a2 | p11 | 2 | 1 | eligible | FAIL/1 | yes | yes | no |
| a2-r6 | stage2-a2 | p11 | 2 | 1 | eligible | PASS/0 | no | no | yes |
| a3-r1 | stage2-a3 | p11 | 2 | 1 | eligible | FAIL/2, FAIL/2 | yes | yes | no |
| a3-r2 | stage2-a3 | p11 | 2 | 1 | eligible | FAIL/2, FAIL/1 | yes | yes | no |
| a3-r3 | stage2-a3 | p11 | 2 | 1 | eligible | FAIL/2, FAIL/2 | yes | yes | no |
| a3-r4 | stage2-a3 | p11 | 2 | 1 | eligible | FAIL/2, FAIL/1 | yes | yes | no |
| a3-r5 | stage2-a3 | p11 | 2 | 1 | eligible | PASS/0, FAIL/1 | yes | no | no |
| a3-r6 | stage2-a3 | p11 | 3 | 0 | cap | FAIL/1, FAIL/2 | yes | yes | no |
| a3-r2 | p14-haiku-a3 | p14 | 3 | 0 | cap | FAIL/3 | yes | yes | no |
| a3-r3 | p14-haiku-a3 | p14 | 2 | 1 | eligible | FAIL/1 | yes | yes | no |
| a3-r4 | p14-haiku-a3 | p14 | 2 | 1 | eligible | FAIL/3 | yes | yes | no |
| a3-r5 | p14-haiku-a3 | p14 | 3 | 0 | cap | FAIL/0 | no | yes | no |
| b2-r1 | p12-ab2 | other | 2 | 1 | eligible | FAIL/3, FAIL/2 | yes | yes | no |
| b2-r2 | p12-ab2 | other | 2 | 1 | eligible | FAIL/1, FAIL/1 | yes | yes | no |
| b2-r3 | p12-ab2 | other | 3 | 0 | cap | PASS/0, FAIL/2 | yes | no | no |
| b2-r4 | p12-ab2 | other | 2 | 1 | eligible | PASS/0, FAIL/2 | yes | no | no |
| b2-r5 | p12-ab2 | other | 2 | 1 | eligible | PASS/0, FAIL/1 | yes | no | no |
| b2-r6 | p12-ab2 | other | 2 | 1 | eligible | FAIL/1, FAIL/3 | yes | yes | no |
| b3-r1 | p12-ab3 | other | 3 | 0 | cap | FAIL/2, FAIL/2 | yes | yes | no |
| b3-r2 | p12-ab3 | other | 4 | 0 | cap | FAIL/1, FAIL/2 | yes | yes | no |
| b3-r3 | p12-ab3 | other | 4 | 0 | cap | FAIL/1, FAIL/1 | yes | yes | no |
| b3-r4 | p12-ab3 | other | 4 | 0 | cap | FAIL/1, FAIL/1 | yes | yes | no |
| b3-r5 | p12-ab3 | other | 4 | 0 | cap | FAIL/0, FAIL/2 | yes | yes | no |
| b3-r6 | p12-ab3 | other | 3 | 0 | cap | PASS/0, FAIL/2 | yes | no | no |
| b1-r3 | p13-pn1 | other | 2 | 1 | unchanged_hash | FAIL/1, FAIL/3 | yes | yes | no |
| l2-r1 | p13-pn2 | other | 2 | 1 | eligible | PASS/0, FAIL/1 | yes | no | no |
| l2-r2 | p13-pn2 | other | 2 | 1 | eligible | PASS/0, FAIL/2 | yes | no | no |
| l2-r3 | p13-pn2 | other | 2 | 1 | eligible | PASS/0, FAIL/2 | yes | no | no |
| l2-r4 | p13-pn2 | other | 2 | 1 | eligible | FAIL/2, FAIL/1 | yes | yes | no |
| l2-r5 | p13-pn2 | other | 2 | 1 | eligible | FAIL/2, FAIL/1 | yes | yes | no |
| l2-r6 | p13-pn2 | other | 2 | 1 | eligible | FAIL/2, FAIL/3 | yes | yes | no |

## Escalated runs

- a1-r1 (stage2-a1, p11): last review R3 = FAIL
- a1-r2 (stage2-a1, p11): last review R3 = FAIL
- a1-r3 (stage2-a1, p11): last review R3 = FAIL
- a3-r1 (p14-haiku-a3, p14): last review R3 = FAIL
- a3-r6 (p14-haiku-a3, p14): last review R3 = FAIL
- b1-r1 (p13-pn1, other): last review M3 = FAIL
- b1-r2 (p13-pn1, other): last review M3 = FAIL

## Excluded runs

- b1-r1 (p12-ab1): audits available 0 < 2
- b1-r2 (p12-ab1): audits available 0 < 2
- b1-r3 (p12-ab1): audits available 0 < 2
- b1-r4 (p12-ab1): audits available 0 < 2
- b1-r5 (p12-ab1): audits available 0 < 2
- b1-r6 (p12-ab1): audits available 0 < 2
- b1h-r1 (p12-ab1): audits available 0 < 2
- b1h-r2 (p12-ab1): audits available 0 < 2
- b1h-r3 (p12-ab1): audits available 0 < 2
- b1h-r4 (p12-ab1): audits available 0 < 2
- b2h-r1 (p12-ab2): audits available 0 < 2
- b2h-r2 (p12-ab2): audits available 0 < 2
- b2h-r3 (p12-ab2): audits available 0 < 2
- b2h-r4 (p12-ab2): audits available 0 < 2
- b3h-r1 (p12-ab3): audits available 0 < 2
- b3h-r2 (p12-ab3): audits available 0 < 2
- b3h-r3 (p12-ab3): audits available 0 < 2
- b3h-r4 (p12-ab3): audits available 0 < 2
- b1-r4 (p13-ab1): audits available 0 < 2
- b1-r5 (p13-ab1): audits available 0 < 2
- b1-r6 (p13-ab1): audits available 0 < 2
- b1h-r1 (p13-ab1): audits available 0 < 2
- b1h-r2 (p13-ab1): audits available 0 < 2
- b1h-r3 (p13-ab1): audits available 0 < 2
- b1h-r4 (p13-ab1): audits available 0 < 2
