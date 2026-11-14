# Group 5 summary (owner questions Q21 to Q25)

Q | winner | confidence | converged or split | suggested handling | fallback_mode
Q21 | proposal B (yes, Phase 2, Orca rows after FU-1, with stop rule) | 78% | converged | SAFE-FOR-AGENT-RECOMMENDATION | false
Q22 | proposal A (rule: older than the larger of 3 producer intervals and the longest normal write gap; observer about 75 s) | 70% | converged | NEEDS-HUMAN | false
Q23 | proposal C (its own state, Orca's word; reopen via one read in the shared capture) | 75% | converged | SAFE-FOR-AGENT-RECOMMENDATION | false
Q24 | proposal A (fresh master-based capture session runs XC-03 then XC-04; owner keeps OB-03) | 65% | converged | NEEDS-HUMAN | false
Q25 | proposal A (worker builds, coordinator-launched PR session publishes; fallback: top-level agent per item) | 55% | split | NEEDS-HUMAN | false
