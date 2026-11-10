# E2 Stage 0 headroom falsifier: GO-REPLAY  [FINAL (labeled truth)]

Rule fired: GO-REPLAY: H=3 >= 1 of 16 defect cases. Candidate-pool misses 11 > 2: raise pool_cap or extend the prefilter BEFORE Stage 1 and rerun Stage 0.

- defect cases measured: 16; clean cases: 8; dropped/undecidable: 4
- extraction coverage: 16/16
- candidate coverage (pool, pool_cap=150): 5/16; admitted-before-cap misses: 9
- static coverage at 12 pairs / 1200 tokens: 2/16
- H (pooled but not in static top-12): 3
- candidate-pool misses (hurt every router equally, reported separately): 11

## Per defect case

| case | layer | category | passages | exhaustive | admitted | pool | evidence | extract | pool cover | static cover | H |
|---|---|---|---|---|---|---|---|---|---|---|---|
| s0-01 | seeded | seed-impossible-check | 231 | 26565 | 2044 | 150 | P0153,P0142 | True | False | False | False |
| s0-02 | seeded | seed-contradiction | 231 | 26565 | 2041 | 150 | P0043,P0114 | True | False | False | False |
| s0-04 | synthetic | synth-exception | 26 | 325 | 14 | 14 | P0005,P0013 | True | False | False | False |
| s0-08 | real | theme-T3 | 231 | 26565 | 2041 | 150 | P0151,P0141 | True | False | False | False |
| s0-09 | synthetic | synth-novel | 28 | 378 | 17 | 17 | P0005,P0013,P0012 | True | False | False | False |
| s0-11 | synthetic | synth-chain | 26 | 325 | 20 | 20 | P0006,P0010,P0016 | True | True | True | False |
| s0-13 | seeded | seed-path-collision | 232 | 26796 | 2051 | 150 | P0119,P0044 | True | False | False | False |
| s0-14 | synthetic | synth-unit | 26 | 325 | 14 | 14 | P0006,P0010 | True | False | False | False |
| s0-15 | seeded | seed-contradiction | 231 | 26565 | 2035 | 150 | P0045,P0157 | True | False | False | False |
| s0-16 | synthetic | synth-chain | 28 | 378 | 10 | 10 | P0007,P0011,P0015 | True | True | True | False |
| s0-17 | synthetic | synth-novel | 29 | 406 | 13 | 13 | P0006,P0015 | True | False | False | False |
| s0-18 | synthetic | synth-exception | 25 | 300 | 9 | 9 | P0005,P0010 | True | False | False | False |
| s0-21 | seeded | seed-chain | 232 | 26796 | 2054 | 150 | P0165,P0051,P0164 | True | True | False | True |
| s0-22 | real | other-D16 | 231 | 26565 | 2041 | 150 | P0116,P0136 | True | True | False | True |
| s0-23 | seeded | seed-chain | 233 | 27028 | 2058 | 150 | P0169,P0053,P0050 | True | True | False | True |
| s0-24 | synthetic | synth-novel | 30 | 435 | 15 | 15 | P0005,P0013,P0010 | True | False | False | False |

## Static ranks of the evidence pairs that are in the pool

- s0-09 P0005-P0013: static rank 11 (tier 4)
- s0-11 P0006-P0010: static rank 1 (tier 1)
- s0-11 P0010-P0016: static rank 2 (tier 1)
- s0-16 P0011-P0015: static rank 2 (tier 1)
- s0-16 P0007-P0011: static rank 1 (tier 1)
- s0-21 P0164-P0165: static rank 132 (tier 3)
- s0-21 P0051-P0165: static rank 12 (tier 1)
- s0-22 P0116-P0136: static rank 73 (tier 1)
- s0-23 P0050-P0053: static rank 85 (tier 1)
- s0-23 P0053-P0169: static rank 13 (tier 1)

## Clean controls (no defect; pool size only)

- s0-03 control-exception: 28 passages, 9 admitted pairs, pool 9
- s0-05 theme-T1: 231 passages, 2041 admitted pairs, pool 150
- s0-06 theme-T2: 231 passages, 2041 admitted pairs, pool 150
- s0-07 control-conditions: 24 passages, 15 admitted pairs, pool 15
- s0-10 control-conditions: 27 passages, 15 admitted pairs, pool 15
- s0-12 other-D8: 231 passages, 2041 admitted pairs, pool 150
- s0-19 control-exception: 25 passages, 11 admitted pairs, pool 11
- s0-20 other-D7: 231 passages, 2041 admitted pairs, pool 150

## Dropped cases (listed)

- s0-05: labelers judged the proposed defect not blocking/real
- s0-06: labelers judged the proposed defect not blocking/real
- s0-12: labelers judged the proposed defect not blocking/real
- s0-20: labelers judged the proposed defect not blocking/real

## Passes

- pass 1 2026-11-10T07:03:31+00:00 final: GO-REPLAY (H=3, extraction_lost=0)
- pass 2 2026-11-10T07:27:21+00:00 final: GO-REPLAY (H=3, extraction_lost=0)
