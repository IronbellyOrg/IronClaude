# CENTRAL MATRIX

Generated 2026-11-10T12:09:46+00:00

Conventions: BLK = mean blocking findings per frozen Sonnet audit, two audits per final spec, rescored uniformly; A = loop-only output tokens, each message id once; R_LOOP = A/100,424 decides cost; R_B = (A + one audit)/169,468 reported only; Haiku rows judged on HR vs the shared Haiku baseline, never pooled.

## Sonnet stratum

| design | arm | role | n | BLK | AUD1 | AUD2 | A | R_LOOP | R_B | growth% | pass | rev | HR | verdict | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| stage2-a3 | a3 | baseline | 6/6 | 1.50 | 1.50 | 1.50 | 100,424 | 1.00 | 1.00 | 1.41 | 6/6 | 2.17 | - | BASELINE |  |
| p12-ab1 | b1 | test | 6/6 | 0.75 | 1 | 0.50 | 122,678 | 1.22 | 0.90 | 1.59 | 6/6 | 1.50 | - | INCONCLUSIVE | blk-mismatch(rep 0.83) |
| p12-ab2 | b2 | test | 6/6 | 1.33 | 0.83 | 1.83 | 105,354 | 1.05 | 0.81 | 1.01 | 6/6 | 2.17 | - | INCONCLUSIVE |  |
| p12-ab3 | b3 | test | 6/6 | 1.25 | 0.83 | 1.67 | 167,382 | 1.67 | 1.16 | 2.24 | 6/6 | 2 | - | INCONCLUSIVE |  |
| p13-pn1 | b1 | test | 6/6 | 1.25 | 1 | 1.50 | 66,240 | 0.66 | 0.39 | 5.41 | 1/6 | 2.83 | - | DROP |  |
| p13-pn2 | l2 | test | 6/6 | 1.33 | 1 | 1.67 | 47,033 | 0.47 | 0.45 | 0.84 | 6/6 | 2 | - | INCONCLUSIVE |  |
| p15-E1 | f4b | test | 0/6 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |
| p15-E1 | f4c | control | 0/6 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |
| p15-E2 | h2j | test | 0/6 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |
| p15-E2 | h2r | control | 0/6 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |
| p15-E2 | h2s | control | 0/6 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |
| p15-E3 | g3b | control | 0/6 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |
| p15-E3 | g3c | test | 0/6 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |
| p15-E5 | k5j | test | 0/6 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |
| p15-E5 | k5r | control | 0/6 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |
| p15-E5 | k5s | control | 0/6 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |

- p12-ab1 b1: no DROP and not a clear ADOPT
- p12-ab2 b2: REJ = 0: the gate never acted (no effect observed)
- p12-ab3 b3: no DROP and no ADOPT
- p13-pn1 b1: BLK_T 1.25 > 0.8 * B_BLK (1.20)
- p13-pn2 l2: no DROP condition and not all ADOPT conditions (noise band)
- p15-E1 f4b: E1 smoke: NO-GO-OFFLINE
- p15-E1 f4c: E1 smoke: NO-GO-OFFLINE
- p15-E2 h2j: Stage 0 passed; Stage 1 replay (Session 2) and GO-LIVE gate not yet run
- p15-E2 h2r: Stage 0 passed; Stage 1 replay (Session 2) and GO-LIVE gate not yet run
- p15-E2 h2s: Stage 0 passed; Stage 1 replay (Session 2) and GO-LIVE gate not yet run
- p15-E3 g3b: live not started: offline gate NO-GO-OFFLINE (automation_below_min: automation 0.179 = 10/56 < 0.2)
- p15-E3 g3c: live not started: offline gate NO-GO-OFFLINE (automation_below_min: automation 0.179 = 10/56 < 0.2)
- p15-E5 k5j: zero-call headroom absent
- p15-E5 k5r: zero-call headroom absent
- p15-E5 k5s: zero-call headroom absent

## Haiku stratum

| design | arm | role | n | BLK | AUD1 | AUD2 | A | R_LOOP | R_B | growth% | pass | rev | HR | verdict | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p14-haiku-a3 | a3h | baseline | 6/6 | 1.83 | 1.83 | - | 167,382 | 1.67 | 1.34 | 3.27 | 4/6 | 2.67 | 1.00 | BASELINE | provisional |
| p12-ab2 | b2h | test | 4/- | 1.88 | 1.75 | 2 | 235,803 | 2.35 | - | 2.62 | 3/4 | 3 | 1.02 | INCONCLUSIVE | provisional |
| p12-ab3 | b3h | test | 4/- | 1.25 | 1.25 | 1.25 | 319,005 | 3.18 | - | 4.59 | 1/4 | 3 | 0.68 | INCONCLUSIVE | provisional |
| p15-E3 | g3bh | control | 0/4 | - | - | - | - | - | - | - | - | - | - | BLOCKED | provisional |
| p15-E3 | g3ch | test | 0/4 | - | - | - | - | - | - | - | - | - | - | BLOCKED | provisional |

- p12-ab2 b2h: REJ = 0: the gate never acted (no effect observed)
- p12-ab3 b3h: no DROP and no ADOPT
- p15-E3 g3bh: live not started: offline gate NO-GO-OFFLINE (automation_below_min: automation 0.179 = 10/56 < 0.2)
- p15-E3 g3ch: live not started: offline gate NO-GO-OFFLINE (automation_below_min: automation 0.179 = 10/56 < 0.2)

## Offline gates

| design | arm | role | n | BLK | AUD1 | AUD2 | A | R_LOOP | R_B | growth% | pass | rev | HR | verdict | flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| p13-pn3 | c3 | offline-gate | 0/0 | - | - | - | - | - | - | - | - | - | - | NO-GO-OFFLINE |  |
| p15-E1 | e1-smoke | offline-gate | 40/40 | - | - | - | - | - | - | - | - | - | - | NO-GO-OFFLINE |  |
| p15-E2 | E2-stage0 | offline-gate | 24/24 | - | - | - | - | - | - | - | - | - | - | BLOCKED |  |
| p15-E3 | E3-falsifier | offline-gate | 100/100 | - | - | - | - | - | - | - | - | - | - | NO-GO-OFFLINE |  |
| p15-E5 | E5-zero-call | offline-gate | 16/- | - | - | - | - | - | - | - | - | - | - | NO-GO-OFFLINE |  |

- p13-pn3 c3: gate: F1 FALSIFIED
- p15-E1 e1-smoke: smoke STOP: false AUTO_CLOSE on ['sm-19', 'sm-20', 'sm-24'] (truth closure_correct = no)
- p15-E2 E2-stage0: GO-REPLAY: H=3 >= 1 of 16 defect cases. Candidate-pool misses 11 > 2: raise pool_cap or extend the prefilter BEFORE Stage 1 and rerun Stage 0.
- p15-E3 E3-falsifier: automation_below_min: automation 0.179 = 10/56 < 0.2
- p15-E5 E5-zero-call: headroom 1/11 (9.1%) < 2 packets or < 0.10

## Blocked downstream

- E4: E1 smoke: NO-GO-OFFLINE: smoke STOP: false AUTO_CLOSE on ['sm-19', 'sm-20', 'sm-24'] (truth closure_correct = no) (from E1)
- E2 Stage 1: pre-registered pool-miss rule unmet (11 > 2) after one a-priori prefilter extension (from E2)
- E2 live: Stage 1 blocked; no further levers added after seeing outcomes (from E2)
- E3 live: offline gate NO-GO-OFFLINE (from E3)
- E5 probe/replay/live: zero-call headroom absent (headroom 1/11 (9.1%) < 2 packets or < 0.10) (from E5)

## WARN

(none)
