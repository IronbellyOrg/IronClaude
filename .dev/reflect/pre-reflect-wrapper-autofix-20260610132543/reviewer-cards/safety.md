# Reviewer card — fail-closed safety (sonnet/qa)

self_confidence: 0.91 → calibrated 0.88

- HIGH: apply rc discarded (Step 4.4 `-> int`, Step 4.5 ignores it) → failed `/task` apply treated as completed cycle. [F2]
- MED: FR-5 ownership contradiction — spec `merged-requirements.md:129-130` "wrapper forces --no-promote" vs U6 `:139` "NO wrapper-side O2 force". [F3]
- SOUND: carve-out ordering (human wins), DEGRADED/BLOCKED-never-autofixed guard before classify_fix, marker exact-"1" + negative controls, needs_human_decision→human-required falsifier (Step 6.4), audit-child marker safe.
