# Top-5 untried combos: main-session estimate (2026-11-12)

Per-model stats, source.md era (computed from reviewer cost.json + findings-v1 blocks, all 3 packages):
| model | runs | avg tok/run | blocking claims/run | findings/run |
|---|---|---|---|---|
| sonnet | 27 | 29.4k | 0.26 | 5.7 |
| haiku | 33 | 57.5k | 1.09 | 8.3 |
| grok | 21 | 53.6k | 1.19 | 3.8 |
| muse-wonder | 27 | 15.7k | 1.30 | 5.3 |
| muse-ember | 18 | 11.2k | 0.61 | 4.6 |
| luna | 51 | 4.7k | 1.37 | 1.7 |
| terra | 18 | 2.1k | 2.06 | 2.5 |
| sol | 3 | 3.9k | 2.00 | 2.7 |
Row token estimate = sum(per-run) x 3 packages.

Reading of the data: sonnet is the coverage driver (every 4/14 row has sonnet) but rarely marks blocking; terra/luna are near-free blocking-markers (noisy); haiku and grok are the expensive slots; grok's value is unproven (r2 is the only strong grok row). n=1 per row, and the r2 pair (same 4 reviewers +ember: 4/14 vs 2/14) shows +-2 GT swings are noise.

## Picks
1. sonnet + terra + luna (~110k). Sonnet coverage + the two cheapest blockers. Untried (sonnet+terra and sonnet+2xluna both tried). Expect 3-5/14, 2-3/8, wb 3-4. Answers: does adding cheap GPT blockers to sonnet recover the blocking recall sonnet+2xluna (0/8) lacked?
2. 2x sonnet + luna (~190k). Independent second sonnet run; r2's haiku x2 showed independence adds catches. Expect 4-6/14, 1-3/8, wb 1-3. Answers: is sonnet's coverage additive across runs?
3. sonnet + 2x haiku (r2 minus grok, ~430k). Expect 3-4/14, 2-4/8. Answers: grok's real value in the best row (saves ~160k tokens if grok is dead weight).
4. 2x terra + luna (~26k). Cheapest panel possible. Expect 2-3/14, 1-3/8, wb 4-6. Answers: floor ROI of an all-GPT blocking panel.
5. 2x sonnet (~176k), doubles as the missing sonnet-with-source.md baseline (arm A was run before source.md). Expect 3-5/14, 0-2/8, wb 0-2. Answers: do panels beat sonnet alone at all now?

Not run: anything with glm/Qwen (owner-excluded), sol-heavy panels (n=3, same profile as terra at 2x cost), more muse-wonder rows (exhausted), spark (no data at all).
