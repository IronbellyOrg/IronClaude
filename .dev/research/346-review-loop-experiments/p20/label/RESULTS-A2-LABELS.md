# Independent labels for the A2 (acceptance-check observability) Jev flags

Question left open by the ab6 gates (`../../p18/seams/live-gates/LIVE-GATES.md`): are the rows Jev flags `cannot_pass` actually flawed? Jev said `cannot_pass` on 220 of the 242 distinct usable check packets; the Sonnet control said `can_pass` on 99%. No precision had been measured.

## Method
- The 242 distinct usable (row, packet) pairs across the 37 shadow specs were rebuilt with the A2 code (`a2_observability.build_items` + `control_items`), so the labeler sees exactly the packet Jev saw: the check row, its cited rows and the code-stage facts.
- Stratified sample of 46 packets: all 16 Jev `can_pass`, all 6 Jev `cannot_discriminate`, 24 of the 220 Jev `cannot_pass` (random, at most 2 per row id, seed 20261110). Order shuffled, three batches of 15 to 16.
- Three Claude Opus 5.5 labelers (one per batch), blind to Jev's answers, using the same four options as Jev; they could read the full spec and run a check in a scratch directory. Opus was used for these three agents only.
- Files: `packets_b*.json` (what the labelers saw, no Jev answers), `labels_b*.json` (their labels), `sample_key.json` (label id to Jev answer), `score_labels.py`, `build_label_set.py` (paths are the session scratchpad).

## Results

| Jev answer | n sampled (of) | Opus: can_pass | Opus: cannot_pass | Opus: cannot_discriminate |
|---|---|---|---|---|
| cannot_pass | 24 (220) | 18 | 4 | 2 |
| can_pass | 16 (16) | 13 | 2 | 1 |
| cannot_discriminate | 6 (6) | 3 | 3 | 0 |

- **Precision of Jev's `cannot_pass`:** Opus agrees the check is flawed (cannot_pass or cannot_discriminate) on 6 of 24 = 25% (90% CI 14 to 42%); an exact `cannot_pass` match on 4 of 24.
- **No separation:** Opus finds a flaw in 25% of Jev `cannot_pass` rows and 19% (3 of 16) of Jev `can_pass` rows (Fisher exact p = 0.72). Jev's answer carries almost no information about whether the check is flawed.
- **Weighted over the 242 packets:** about 61 are truly flawed (25%); Jev flags 226 (93%), so its estimated precision is about 26%, the base rate, with recall of about 95% only because it flags nearly everything.
- Opus said `can_pass` on 34 of 46 (74%). The Sonnet control's 99% looks too lenient and Jev's 88% `cannot_pass` too strict; the truth is nearer the Sonnet side.

## Caveats
- One labeler family, one pass, no second independent labeler; Opus mean self-reported confidence 0.66. A flawed check Opus misses counts against Jev here.
- Sample is stratified, not proportional; the 242 packets are heavily overlapping variants of 36 row ids.
- Nothing here measures the deterministic code stage (separately 93% precise on its own rows).

## Decision
Drop the Jev stage of A2. Keep the deterministic code stage (lint, D20, D21, EXEC), which flags the same kinds of defect without the model call. If Jev is revisited, it needs a precision gate against labels like these before it influences any gate.
