# PN2 offline results (Phase O)

Truth basis: theme-v1 (C9.3 tags). Catalog: present.
MP sample sizes: pass 1 REF 30 of 430 distinct, PATH 30 of 196, KV 26/26, COUNT 7/7, PHASE 4/4; pass 2 REF 30 of 245, PATH 18/18, PHASE 35/35, KV 3/3 (random.Random(0) samples where a check had more than 60 distinct flags). Distinct = identical quote+message across documents counted once.

### Pass 1 (literal, as written in the plan)

| Check | MP (true/adjudicated) | MP weighted by docs | MP defect-only | flags final/orig/other/hist/ref | CLEAN | positive controls caught | HIT final T1/T2/T3 | HIT orig (R1 reports) T1/T2/T3 | HIT near-only final / orig | MP orig-only | catalog clusters caught on orig |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF | 0.37 (11/30) | 0.38 | 0.03 | 362/20/230/133/80 | 0 | seeded:n,n,n; cand_deletion:n; cand_regression:n | 6/6 / 9/9 / 2/2 | 12/12 / 6/6 / 6/6 | 6/6 / 8/9 / 1/2 ; 11/12 / 4/6 / 6/6 | 0/0 | 2/12 ['D12', 'D19'] |
| COUNT | 0.00 (0/7) | 0.00 | 0.00 | 1/0/2/3/1 | 0 | seeded:n,n,n; cand_deletion:n; cand_regression:n | 0/6 / 0/9 / 0/2 | 0/12 / 0/6 / 0/6 | 0/6 / 0/9 / 0/2 ; 0/12 / 0/6 / 0/6 | 0/0 | 0/12 [] |
| KV | 0.00 (0/26) | 0.00 | 0.00 | 2/0/23/1/0 | 0 | seeded:n,n,n; cand_deletion:n; cand_regression:n | 0/6 / 0/9 / 0/2 | 0/12 / 0/6 / 0/6 | 0/6 / 0/9 / 0/2 ; 0/12 / 0/6 / 0/6 | 0/0 | 0/12 [] |
| PHASE | 0.00 (0/4) | 0.00 | 0.00 | 5/0/0/1/0 | 0 | seeded:n,n,n; cand_deletion:n; cand_regression:n | 0/6 / 1/9 / 0/2 | 0/12 / 0/6 / 0/6 | 0/6 / 1/9 / 0/2 ; 0/12 / 0/6 / 0/6 | 0/0 | 0/12 [] |
| PATH | 0.00 (0/30) | 0.00 | 0.00 | 155/4/0/60/45 | 0 | seeded:n,n,n; cand_deletion:n; cand_regression:n | 6/6 / 7/9 / 1/2 | 12/12 / 5/6 / 6/6 | 6/6 / 7/9 / 1/2 ; 11/12 / 5/6 / 6/6 | 0/0 | 5/12 ['D1', 'D2', 'D10', 'D12', 'D19'] |

Live check set (MP>=0.8 and CLEAN=0): none.
G1 (a live-set check with HIT>=0.5 on T1/T2/T3, literal definition incl. quote-regex matches): FAIL
G1 restricted to line-proximity hits only (no quote-regex matches): FAIL
ADOPT-TOOL (MP>=0.9, CLEAN=0, one positive control caught): none.
RFC census of the original (information only): {'MUST': 0, 'SHALL': 0, 'SHOULD': 0, 'MAY': 0}. Total findings over the corpus: 1128.

### Pass 2 (after one tuning pass; the shipped lint)

| Check | MP (true/adjudicated) | MP weighted by docs | MP defect-only | flags final/orig/other/hist/ref | CLEAN | positive controls caught | HIT final T1/T2/T3 | HIT orig (R1 reports) T1/T2/T3 | HIT near-only final / orig | MP orig-only | catalog clusters caught on orig |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF | 0.97 (29/30) | 0.97 | 0.00 | 52/0/193/25/0 | 0 | seeded:n,n,n; cand_deletion:n; cand_regression:n | 3/6 / 6/9 / 0/2 | 0/12 / 0/6 / 0/6 | 3/6 / 4/9 / 0/2 ; 0/12 / 0/6 / 0/6 | 0/0 | 0/12 [] |
| COUNT | n/a | n/a | n/a | 0/0/0/0/0 | 0 | seeded:n,n,n; cand_deletion:n; cand_regression:n | 0/6 / 0/9 / 0/2 | 0/12 / 0/6 / 0/6 | 0/6 / 0/9 / 0/2 ; 0/12 / 0/6 / 0/6 | 0/0 | 0/12 [] |
| KV | 0.00 (0/3) | 0.00 | 0.00 | 1/0/0/0/2 | 0 | seeded:Y,Y,Y; cand_deletion:n; cand_regression:Y | 0/6 / 0/9 / 0/2 | 0/12 / 0/6 / 0/6 | 0/6 / 0/9 / 0/2 ; 0/12 / 0/6 / 0/6 | 0/0 | 0/12 [] |
| PHASE | 0.03 (1/35) | 0.26 | 0.03 | 30/1/0/9/17 | 0 | seeded:n,n,n; cand_deletion:n; cand_regression:n | 6/6 / 8/9 / 2/2 | 11/12 / 6/6 / 6/6 | 6/6 / 5/9 / 1/2 ; 11/12 / 1/6 / 6/6 | 1/1 | 3/12 ['D12', 'D16', 'D19'] |
| PATH | 0.11 (2/18) | 0.48 | 0.11 | 22/2/0/5/4 | 0 | seeded:n,n,n; cand_deletion:n; cand_regression:n | 4/6 / 8/9 / 0/2 | 12/12 / 6/6 / 4/6 | 0/6 / 7/9 / 0/2 ; 4/12 / 4/6 / 4/6 | 2/2 | 3/12 ['D1', 'D2', 'D10'] |

Live check set (MP>=0.8 and CLEAN=0): ['REF'].
G1 (a live-set check with HIT>=0.5 on T1/T2/T3, literal definition incl. quote-regex matches): PASS {'REF/T1/HIT_final': (3, 6), 'REF/T2/HIT_final': (6, 9)}
G1 restricted to line-proximity hits only (no quote-regex matches): PASS {'REF/T1/HITn_final': (3, 6)}
ADOPT-TOOL (MP>=0.9, CLEAN=0, one positive control caught): none.
RFC census of the original (information only): {'MUST': 0, 'SHALL': 0, 'SHOULD': 0, 'MAY': 0}. Total findings over the corpus: 365.

Supplementary stratum (adjudicated in full, not sampled): the 52 distinct REF flags on the Orca-spec family (finals, history, reference snapshots; 0 on the original) are all true-mechanical, and all are revision-log rows or reviewer finding ids (F-nn, N-nn, B-n, REQ-n, ARCH-n) cited in the spec body: 52/52, none is a defect an audit blocked on. The pass-2 REF sample (30 of 245 distinct) was drawn over all groups and is dominated by the `other` design documents (193 of 270 flags), whose ids are defined in sibling documents.

G1 note: the literal G1 passes only through REF hits on revision-log rows of final documents (3/6 T1, 6/9 T2 documents); REF has 0 flags on the original and 0/12 R1 reports hit. PHASE and PATH reach T3 and T2 on the original (PHASE: AC-0.4 -> 7.2 -> WC-4, catalog D19; PATH: adversarial/workflow report paths vs the WC-4 template, catalog D1/D2/D10) but fail MP (0.03 and 0.11) because the revised finals handle the same dependency in their own text.
