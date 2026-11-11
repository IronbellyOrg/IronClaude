# E2 Stage 0 headroom falsifier: GO-REPLAY  [PROVISIONAL (author evidence, no labels; information only)]

Rule fired: GO-REPLAY: H=7 >= 1 of 20 defect cases. Candidate-pool misses 11 > 2: raise pool_cap or extend the prefilter BEFORE Stage 1 and rerun Stage 0.

- defect cases measured: 20; clean cases: 4; dropped/undecidable: 0
- extraction coverage: 20/20
- candidate coverage (pool, pool_cap=300): 9/20; admitted-before-cap misses: 9
- static coverage at 12 pairs / 1200 tokens: 2/20
- H (pooled but not in static top-12): 7
- candidate-pool misses (hurt every router equally, reported separately): 11

## Per defect case

| case | layer | category | passages | exhaustive | admitted | pool | evidence | extract | pool cover | static cover | H |
|---|---|---|---|---|---|---|---|---|---|---|---|
| s0-01 | seeded | seed-impossible-check | 231 | 26565 | 2044 | 300 | P0153,P0142 | True | False | False | False |
| s0-02 | seeded | seed-contradiction | 231 | 26565 | 2041 | 300 | P0043,P0114 | True | False | False | False |
| s0-04 | synthetic | synth-exception | 26 | 325 | 7 | 7 | P0005,P0013 | True | False | False | False |
| s0-05 | real | theme-T1 | 231 | 26565 | 2041 | 300 | P0152,P0086 | True | True | False | True |
| s0-06 | real | theme-T2 | 231 | 26565 | 2041 | 300 | P0044,P0060 | True | False | False | False |
| s0-08 | real | theme-T3 | 231 | 26565 | 2041 | 300 | P0151,P0141,P0123 | True | True | False | True |
| s0-09 | synthetic | synth-novel | 28 | 378 | 7 | 7 | P0005,P0013,P0012 | True | False | False | False |
| s0-11 | synthetic | synth-chain | 26 | 325 | 10 | 10 | P0006,P0010,P0016 | True | True | True | False |
| s0-12 | real | other-D8 | 231 | 26565 | 2041 | 300 | P0049,P0196 | True | True | False | True |
| s0-13 | seeded | seed-path-collision | 232 | 26796 | 2051 | 300 | P0119,P0062 | True | False | False | False |
| s0-14 | synthetic | synth-unit | 26 | 325 | 4 | 4 | P0006,P0010 | True | False | False | False |
| s0-15 | seeded | seed-contradiction | 231 | 26565 | 2035 | 300 | P0045,P0157 | True | False | False | False |
| s0-16 | synthetic | synth-chain | 28 | 378 | 4 | 4 | P0007,P0011,P0015 | True | True | True | False |
| s0-17 | synthetic | synth-novel | 29 | 406 | 4 | 4 | P0006,P0015 | True | False | False | False |
| s0-18 | synthetic | synth-exception | 25 | 300 | 4 | 4 | P0005,P0010 | True | False | False | False |
| s0-20 | real | other-D7 | 231 | 26565 | 2041 | 300 | P0050,P0167 | True | True | False | True |
| s0-21 | seeded | seed-chain | 232 | 26796 | 2054 | 300 | P0165,P0051,P0164 | True | True | False | True |
| s0-22 | real | other-D16 | 231 | 26565 | 2041 | 300 | P0116,P0136 | True | True | False | True |
| s0-23 | seeded | seed-chain | 233 | 27028 | 2058 | 300 | P0169,P0053,P0050 | True | True | False | True |
| s0-24 | synthetic | synth-novel | 30 | 435 | 5 | 5 | P0005,P0013,P0010 | True | False | False | False |

## Static ranks of the evidence pairs that are in the pool

- s0-05 P0086-P0152: static rank 56 (tier 1)
- s0-08 P0123-P0151: static rank 95 (tier 1)
- s0-08 P0141-P0151: static rank 161 (tier 1)
- s0-11 P0006-P0010: static rank 1 (tier 1)
- s0-11 P0010-P0016: static rank 2 (tier 1)
- s0-12 P0049-P0196: static rank 21 (tier 1)
- s0-16 P0011-P0015: static rank 2 (tier 1)
- s0-16 P0007-P0011: static rank 1 (tier 1)
- s0-20 P0050-P0167: static rank 274 (tier 4)
- s0-21 P0164-P0165: static rank 264 (tier 3)
- s0-21 P0051-P0165: static rank 24 (tier 1)
- s0-22 P0116-P0136: static rank 148 (tier 1)
- s0-23 P0050-P0053: static rank 165 (tier 1)
- s0-23 P0053-P0169: static rank 25 (tier 1)

## Clean controls (no defect; pool size only)

- s0-03 control-exception: 28 passages, 3 admitted pairs, pool 3
- s0-07 control-conditions: 24 passages, 11 admitted pairs, pool 11
- s0-10 control-conditions: 27 passages, 3 admitted pairs, pool 3
- s0-19 control-exception: 25 passages, 3 admitted pairs, pool 3

## Passes

