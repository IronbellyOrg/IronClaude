# COMBO REPORT — 15 reviewer-model combinations on the 3 pilot packages

Date: 2026-11-11. EVAL: .dev/eval-workspaces/tasklist-review-panel/20261111-a1. Companion to PILOT-REPORT.md (arms A/B/C). Read-only eval; no source edits; nothing staged or committed.

## What was run

15 owner-ordered combinations of Tier 3/4 reviewer models (Qwen3.8-max excluded by owner decision), each combo run by a supervised worker: every reviewer model in the row reviewed all 3 pilot packages via `tools/run-reviewer.sh` (raw model ids, `claude -p`, 3000 s timeout, 1 rerun), then the worker merged each package with `superclaude review merge`. All 15 combos are complete and scored. r5-glm-haiku2 finished last (782,529 tokens, 8,346 s: the largest spend of any combo); on makeTheAliasOnly its glm findings block was marked block-ok false by the merge validator (round accepted on the haiku runs), which cost it some glm findings.

- Packages: designSpec (10 GT defects, 5 blocking-in-implement), makeTheAliasOnly (4 GT, 3 blocking) = defect-rich (14 GT any / 8 GT blocking); design (2 GT, 0 blocking) = control.
- Scoring: same blind procedure as the pilot arms. Each of the 45 merged reports (15 combos x 3 packages) was anonymized (reviewer ids -> R1..Rn, paths redacted) under a random label; one Opus judge per (combo, package) scored GT coverage and wrong blockers against ground-truth.json. Judge score.json files: arms/scoring/combos/<combo>/<pkg>/<label>/score.json. Cost data: per-reviewer .cost.json under <pkg>/reviews/combos/<combo>/.
- Known harness event: reports produced before the category-label fix used `unpassable-ac`; merges used sed-fixed `.catfix.md` copies (originals unedited). Known reviewer-side format failures (not harness): c1's haiku designSpec block missing its heading (15 findings dropped); r2's haiku makeTheAliasOnly block with a >300-char claim (dropped).

## Master table (15 scored combos, ranked by value; tokens/wall are summed reviewer runs across all 3 packages, from cost.json)

| # | Combo | Models | Tokens | Wall s | GT any (defect-rich) | GT blocking (defect-rich) | Wrong blockers (defect-rich) | GT any (control) | Wrong blockers (control) | Ledger rows (dS/alias/design) | Verdicts dS/alias/design |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | r2-haiku2-grok | haiku x2, grok | 488,057 | 4,181 | 3/14 | 1/8 | 2 | 0/2 | 1 | 8/5/4 | PASS FAIL FAIL |
| 2 | n4-muse-glm-haiku | muse, glm, haiku | 615,048 | 6,990 | 3/14 | 2/8 | 2 | 1/2 | 1 | 8/7/4 | FAIL FAIL FAIL |
| 3 | n2-muse-haiku-grok | muse, haiku, grok | 345,387 | 3,423 | 3/14 | 0/8 | 3 | 1/2 | 1 | 7/7/5 | PASS FAIL FAIL |
| 4 | n5-muse-glm-luna | muse, glm, luna | 507,820 | 7,097 | 4/14 | 1/8 | 3 | 1/2 | 1 | 7/6/4 | FAIL FAIL FAIL |
| 5 | r1-haiku-luna2 | haiku, luna x2 | 188,952 | 1,146 | 2/14 | 2/8 | 3 | 0/2 | 2 | 7/6/5 | FAIL FAIL FAIL |
| 6 | n3-muse-luna-grok | muse, luna, grok | 233,893 | 3,505 | 2/14 | 1/8 | 3 | 1/2 | 0 | 5/5/1 | FAIL FAIL FAIL |
| 7 | r3-luna2-grok | luna x2, grok | 193,662 | 3,190 | 2/14 | 0/8 | 3 | 1/2 | 0 | 4/2/4 | FAIL FAIL PASS |
| 7 | r5-glm-haiku2 | glm, haiku x2 | 782,529 | 8,346 | 2/14 | 1/8 | 1 | 1/2 | 1 | 8/7/4 | FAIL FAIL FAIL |
| 7 | r2-terra (B3) | haiku x2, grok, terra | 487,442 | 4,219 | 3/14 | 2/8 | 3 | 2/2 | 1 | 6/9/3 | FAIL FAIL FAIL |
| 10 | r2-sol (B3) | haiku x2, grok, sol | 527,297 | 4,703 | 1/14 | 1/8 | 1 | 0/2 | 2 | 11/7/5 | FAIL FAIL FAIL |
| 7 | r2-sonnet (B3) | haiku x2, grok, sonnet | 490,887 | 3,919 | 2/14 | 2/8 | 1 | 1/2 | 1 | 9/4/7 | FAIL FAIL FAIL |
| 7 | n2-terra (B3) | muse, haiku, grok, terra | 356,035 | 3,594 | 2/14 | 2/8 | 2 | 1/2 | 0 | 4/3/4 | FAIL FAIL FAIL |
| 9 | n2-sol (B3) | muse, haiku, grok, sol | 374,118 | 4,130 | 2/14 | 1/8 | 2 | 1/2 | 0 | 7/6/3 | FAIL FAIL FAIL |
| 9 | n2-sonnet (B3) | muse, haiku, grok, sonnet | 409,322 | 4,084 | 2/14 | 1/8 | 2 | 1/2 | 3 | 5/3/7 | FAIL FAIL FAIL |
| 12 | n4-terra (B3) | muse, glm, haiku, terra | 396,325 | 5,985 | 1/14 | 1/8 | 1 | 1/2 | 1 | 7/6/3 | FAIL FAIL FAIL |
| 9 | n4-sol (B3) | muse, glm, haiku, sol | 491,576 | 9,552 | 2/14 | 0/8 | 4 | 2/2 | 0 | 10/6/4 | FAIL FAIL FAIL |
| 3 | n4-sonnet (B3) | muse, glm, haiku, sonnet | 435,717 | 4,578 | 3/14 | 1/8 | 1 | 1/2 | 1 | 6/5/4 | FAIL FAIL FAIL |
| 3 | n5-sonnet (B3) | muse, glm, luna, sonnet | 358,726 | 5,941 | 3/14 | 1/8 | 1 | 1/2 | 0 | 11/6/2 | FAIL FAIL FAIL |
| 9 | n5-terra (B3) | muse, glm, luna, terra | 362,590 | 7,091 | 2/14 | 0/8 | 2 | 0/2 | 1 | 6/7/3 | PASS FAIL FAIL |
| 9 | n5-sol (B3) | muse, glm, luna, sol | 273,394 | 8,614 | 2/14 | 1/8 | 2 | 0/2 | 1 | 5/7/3 | FAIL FAIL FAIL |
| 8 | n1-muse-haiku-luna | muse, haiku, luna | 196,507 | 1,255 | 2/14 | 0/8 | 3 | 1/2 | 1 | 7/6/4 | PASS FAIL FAIL |
| 9 | c2-haiku-grok | haiku, grok | 336,062 | 3,364 | 1/14 | 1/8 | 2 | 1/2 | 0 | 6/7/2 | FAIL FAIL FAIL |
| 10 | c3-luna-grok | luna, grok | 165,816 | 2,635 | 1/14 | 1/8 | 2 | 1/2 | 1 | 2/4/2 | FAIL FAIL FAIL |
| 11 | c4-haiku-luna-grok | haiku, luna, grok | 356,716 | 3,630 | 1/14 | 0/8 | 2 | 1/2 | 1 | 6/5/8 | FAIL FAIL FAIL |
| 12 | c5-glm-haiku | glm, haiku | 408,097 | 6,460 | 1/14 | 0/8 | 3 | 0/2 | 1 | 6/6/4 | FAIL FAIL FAIL |
| 13 | c1-haiku-luna | haiku, luna | 170,558 | 927 | 1/14 | 1/8 | 3 | 0/2 | 1 | 0/6/7 | PASS FAIL FAIL |
| 14 | r4-haiku-luna2-grok | haiku, luna x2, grok | 302,375 | 3,136 | 0/14 | 0/8 | 2 | 1/2 | 2 | 7/5/6 | PASS FAIL FAIL |

Efficiency view (defect-rich GT-any caught per 100k reviewer tokens, 15 combos; r5 = 0.26): r1-haiku-luna2 1.06; c1-haiku-luna 0.59; n1-muse-haiku-luna 1.02; r3-luna2-grok 1.03; n3-muse-luna-grok 0.86; c3-luna-grok 0.60; r2-haiku2-grok 0.61; c2-haiku-grok 0.30; n2-muse-haiku-grok 0.87; c4-haiku-luna-grok 0.28; r4-haiku-luna2-grok 0; c5-glm-haiku 0.25; n4-muse-glm-haiku 0.49; n5-muse-glm-luna 0.79. Arm baselines from PILOT-REPORT.md: A (sonnet alone) 2.15, B 0.76, C 0.66.

## Ranking rationale (most to least valuable / ROI)

Ranking principle, stated up front: value = GT defects caught on defect-rich packages (any severity, with blocking recall as tiebreak) minus wrong blockers, then cost. This is a judgment call on n=3 packages per combo; ranks 3-8 and 9-13 are within noise of each other and should be read as tiers, not an ordering.

- **Tier 1 (best value): r2-haiku2-grok, n4-muse-glm-haiku.** r2: 3/14 any + 1/8 blocking at 488k tokens; the only 2-reviewer-tier combo with top-tier catches (its second haiku was a genuinely independent run). n4: the best blocking recall of any combo (2/8) and 3/14 any, but the second-highest cost (615k, 6990 s). Both also passed the control cleanly enough (r2: 1 wrong blocker; n4: caught 1/2 GT with 1 wrong blocker).
- **Tier 2 (good catch rate, mid cost): n2-muse-haiku-grok, n5-muse-glm-luna.** n2: 3/14 any at 345k tokens, the cheapest of the 3-catch combos, but 0/8 blocking and 3 wrong blockers on defect-rich. n5: the highest raw coverage (4/14) but 3 wrong blockers and glm/luna wall time pushes cost to 508k/7097 s.
- **Tier 3 (best ROI per token, fewer catches): r1-haiku-luna2, r5-glm-haiku2, n1-muse-haiku-luna, r3-luna2-grok, n3-muse-luna-grok.** r1 stands out: 2/14 any AND 2/8 blocking (tied-best blocking recall) for only 189k tokens and 1146 s, the cheapest and fastest scored combo. If a budget panel is wanted, r1 (haiku + luna + luna) is the value pick despite 3 wrong blockers. r5 (rank 7) pairs 2/14 any and 1/8 blocking with the set's lowest defect-rich wrong-blocker count (1), but at 782k tokens it is the wrong way to buy that precision. n3 is the cheapest way to get a muse-model panel (234k, 1 wrong blocker on control, cleanest control behavior in the set).
- **Tier 4 (mediocre): c2-haiku-grok, c3-luna-grok, c4-haiku-luna-grok, c5-glm-haiku.** 1/14 any each, moderate cost. c3 and c5 spent their budget without distinguishing themselves; c5's glm runs were slow (800-1800 s per review) for 0 blocking recall. Notably glm-5.3 added cost without catches in every combo it appeared in (c5, n4, n5: 408-615k tokens, 0-2 blocking).
- **Tier 5 (worst value): c1-haiku-luna, r4-haiku-luna2-grok.** c1's headline cheapness (171k, 927 s) bought near-zero information: its designSpec merge produced 0 ledger rows (haiku's findings block unparseable, luna thin at 991 tokens) and it scored 1/14 with 3 wrong blockers. r4 is the worst scored combo outright: 0/14 any at 302k tokens, 2 wrong blockers on the control.

## Cross-cutting findings

1. **No combo beats arm A's efficiency.** Every combo's catches-per-100k (0-1.06) sits below arm A (sonnet alone, 2.15) and roughly at arm B/C level (0.66-0.76). Cheaper reviewers are cheaper per token, not per catch.
2. **Blocking recall is bad everywhere.** Best combo blocking recall is 2/8 (n4, r1); 8 of 14 combos caught 0 or 1 blocking GT item. Panel verdicts also disagree with implement reality: 5 combos PASS the designSpec package (5 blocking GT items) and r3 PASSes the control-behaving design package while FAILing everywhere else.
3. **gpt-6-luna is the budget slot, with a caveat.** Luna runs are fast and thin (30-295 s, 1.4k-14k tokens) and luna-heavy combos (r1, r3, c1, c3, n3) are the cheapest. But luna contributed 0 findings on 2 of 3 packages in n3, was thin (<1000 tokens) in c1's designSpec, and r4 (luna doubled) scored 0/14: luna lowers cost without reliably adding catches.
4. **Haiku is the workhorse, grok the second opinion.** haiku appears in 11 combos and supplied most merged rows; grok-4.7 runs are slow (600-980 s, 41-63k tokens) but appeared in 6 of the top 8 combos. muse-wonder-1.0 (149-186 s, ~16-17k tokens) was the cheapest way to add a third genuine reviewer (n2, n3, n1 all mid-table or better).
5. **Wrong blockers are common on defect-rich packages** (2-3 per combo). Since GT penalizes novel-but-real catches as wrong blockers (stated limit inherited from the pilot), some of these may be genuine finds; the control package shows the cleaner signal (0-2 per combo there, 0 for c2, r3, n3).

## Verdict and recommendation

No 3/4-tier combination recovers what the panels exist to catch: blocking defects in defect-rich plans. If a budget panel must be chosen from this set, pick **r1-haiku-luna2** (best blocking recall per token: 2/8 blocking at 189k tokens/1146 s) or **n2-muse-haiku-grok** (best any-severity catch rate at mid cost, 3/14 at 345k). If quality matters more than cost, **n4-muse-glm-haiku** has the best blocking recall (2/8) at the highest cost. The honest summary: single-reviewer arm A still caught defects more efficiently than every combination tried, and no configuration, cheap or expensive, reached even 30% blocking recall on the packages whose defects actually blocked implementation.

## Stated limits

- n=3 packages per combo; one judge per (combo, package); judge variance unmeasured.
- The `unpassable-ac` harness bug dropped findings from pre-fix reports (catfix restores the label but not findings the merge had already skipped; c1 designSpec and r2 alias lost reviewer blocks to format rules).
- r5-glm-haiku2 confirmed the glm pattern: the largest spend of any combo (782k tokens, 8,346 s) for 2/14 any, 1/8 blocking; its 1 wrong blocker on defect-rich is the lowest in the set, but its efficiency (0.26 catches per 100k) is second-worst.
- Costs include rerun attempts (glm needed 2 attempts on 3 packages across c5/n4/n5; makeTheAliasOnly burned c1's rerun on the category bug).
- Same GT structural bias as the pilot: real novel blocking finds score as wrong blockers.

## Artifacts

- Per-combo worker reports: combos/<combo>/RESULT.md (+ per-package merged-1.md, ledger.json, resolution.json).
- Judge scores: arms/scoring/combos/<combo>/<pkg>/<label>/{merged-anon.md,score.json,judge.json}; label keys in label-key.json and arm-key.json files.
- Reviewer outputs and costs: <pkg>/reviews/combos/<combo>/.
- Pilot arm results: PILOT-REPORT.md.

## Batch 3 addendum (added 2026-11-12, rows marked B3)

Batch 3 = each top-4 combo re-run fresh plus one added reviewer (terra / sol / sonnet). First attempt (12 concurrent workers) was torn down for gateway model-identity bleed (muse served as terra); all outputs quarantined in place as `*-contaminated-20261111`. After a 60-minute cooldown and a clean zero-load muse probe, rows are re-running serially (one worker, one concurrent run). gpt-6.1-terra caveat: in r2-terra it returned thin "incomplete" reports (407-598 tokens, 0 findings, citing a missing input) despite passing the model check; its rows contribute nothing but cost.

- r2-terra (rank 7): 3/14 any, 2/8 blocking (ties best blocking recall), 3 wrong blockers on defect-rich; control 2/2 any with 1 wrong blocker; 487,442 tokens, 4,219 s. Added terra bought the blocking-recall tie at roughly +150k tokens over r2 base (345k) while contributing no findings itself.
- r2-sol (rank 10): 1/14 any, 1/8 blocking, 1 wrong blocker on defect-rich; control 0/2 with 2 wrong blockers; 527,297 tokens, 4,703 s. Its first worker died mid-run (agent exit unconfirmed; 7/12 runs kept) and the relaunch finished it. Like terra, gpt-6.1-sol returned short "incomplete" reports with 0 findings on all 3 packages: both gpt-6.1 tier-2 additions cost tokens without contributing findings. Neither B3 addition to r2 beat the r2 base (3/14, 1/8 at 488k).
- r2-sonnet (rank 7): 2/14 any, 2/8 blocking (ties best blocking recall), only 1 wrong blocker on defect-rich; control 1/2 with 1 wrong blocker; 490,887 tokens, 3,919 s. The sonnet addition is the only B3 reviewer that actually produced findings. Among the r2 B3 variants: terra 3/14-2/8 but 3 wrong blockers, sonnet 2/14-2/8 with the fewest wrong blockers (1), sol 1/14-1/8 with 2 control wrong blockers. None beat r2 base on catches; sonnet matches its blocking recall with less noise.
- n2-terra (rank 7): 2/14 any, 2/8 blocking (ties best blocking recall), 2 wrong blockers on defect-rich; control 1/2 with 0 wrong blockers; 356,035 tokens, 3,594 s. Cheapest B3 row so far. Muse ran clean here (the contamination-era outputs were quarantined; this row was re-run after the outage). Terra again contributed 0 findings (thin incomplete reports) — the blocking-recall tie again comes entirely from the base reviewers.
- n2-sol (rank 9): 2/14 any, 1/8 blocking, 2 wrong blockers on defect-rich; control 1/2 with 0 wrong blockers; 374,118 tokens, 4,130 s. Sol again thin/empty on all 3 packages (0 findings), so the row is effectively the n2 base panel; it dropped from the base's 3/14 to 2/14, which is run-to-run variance of the same nominal panel.
- n2-sonnet (rank 9): 2/14 any, 1/8 blocking, 2 wrong blockers on defect-rich; control 1/2 but 3 wrong blockers (worst control precision in B3); 409,322 tokens, 4,084 s. n2 family B3 summary: none of the three additions beat the n2 base (3/14, 0/8 at 345k); terra 2/14-2/8, sol 2/14-1/8, sonnet 2/14-1/8.
- n4-terra (rank 12): 1/14 any, 1/8 blocking, 1 wrong blocker on defect-rich; control 1/2, 1 wrong blocker; 396,325 tokens, 5,985 s. Below its n4 base (3/14, 2/8 at 615k) at lower cost — again terra contributed 0 findings (thin on all 3).
- n4-sol (rank 9): 2/14 any, 0/8 blocking, 4 wrong blockers on defect-rich (worst defect-rich precision in B3); control 2/2 any with 0 wrong blockers; 491,576 tokens, 9,552 s (glm runs dominate wall). Below its n4 base (3/14, 2/8).
- n4-sonnet (rank 3): 3/14 any, 1/8 blocking, only 1 wrong blocker on defect-rich; control 1/2 with 1 wrong blocker; 435,717 tokens, 4,578 s (glm's wall time dominates). Matches the n4 base's 3/14 any at 180k fewer tokens and with fewer wrong blockers. Best B3 row alongside r2-terra; consistent with sonnet being the only addition that contributes real findings.
- n5-sonnet (rank 3): 3/14 any, 1/8 blocking, only 1 wrong blocker on defect-rich; control 1/2 with 0 wrong blockers; 358,726 tokens, 5,941 s. Cheapest of the three top-coverage B3 rows. Like n4-sonnet, the sonnet addition is what lifts coverage; luna/glm base alone (n5) scored 4/14 any in batch 2 but here sonnet+muse+luna+glm holds 3/14 at similar cost.
- n5-terra (rank 9) and n5-sol (rank 9): each 2/14 any with 2 wrong blockers on defect-rich and 0/2 control coverage (1 wrong blocker each); terra 362,590 tokens, sol 273,394 tokens (cheapest B3 row), both glm-wall-heavy (7,091 s / 8,614 s). These rows were finished by the coordinator after the race + glm outage: the 5 suspended runs were re-run serially, all model_ok=true, merged fresh (stale round-1 ledgers moved to stale-r1/). Both sit below the n5 base (4/14).

## Batch 3 final summary (12/12 rows scored)
Additions ranked by what they brought: sonnet is the only addition that contributed findings and coverage (all three sonnet rows tie rank 3 at 3/14; r2-sonnet and n5-sonnet also post the cleanest controls). terra and sol (gpt-6.1 tier-2 ids) returned thin "incomplete" reports with 0 findings on every package in every row — pure cost. No B3 row beat its own batch-2 base on defect-rich catches (n2 3/14 vs 2/14 for all its B3 rows; n4 3/14-2/8 vs 1-3/14-1/8; n5 4/14 vs 2-3/14; r2 3/14 vs 1-3/14), though sonnet rows matched or bettered their bases' precision (fewest wrong blockers). Operational notes: gateway misrouting hit muse (22:40 UTC Nov 11) and glm (08:25 UTC Nov 12) under load; both recovered after ~60-90 min cooldowns. The contaminated first attempt of all 12 rows is preserved under *-contaminated-20261111.
Recommendation update: if a 4-reviewer panel is wanted, n5-sonnet (muse + glm + luna + sonnet) is the batch-3 pick — 3/14 any, 1/8 blocking, 1 wrong blocker on defect-rich, 0 on control, 358,726 tokens. The cheaper batch-2 r2 and batch-3 r2-sonnet remain better per-token choices; single-reviewer arm A remains unbeaten on efficiency.

## CORRECTION (2026-11-12 15:20 UTC): blocking-count parser bug + luna quarantine
1. PARSER BUG: earlier blocking counts grepped '"blocking":true' (no space); several models emit '"blocking": true'. All per-model blocking numbers stated in earlier sections (including "grok 0 blocking in 42 runs" and the batch-4 interim table claiming only gpt models block) are WRONG. Corrected source.md-run totals (space-tolerant parse, 84 valid runs):
   muse 21 blocking/18 runs, haiku 19/16, grok 19/15, sonnet 2/11, luna 23/21, terra 8/3, sol 6/3. Every model produces blocking findings with source.md present; gpt-6.* have the highest per-run rate but are NOT the only ones.
2. LUNA QUARANTINE (owner order): all pre-source.md luna data is moved to EVAL/quarantine-pre-src-luna/ (428 reviewer files, 10 combo-row merge sets). Luna statements in PILOT-REPORT.md and batch 1-3 sections are superseded; only -src luna runs may be cited going forward.

## Batch 4/5: source.md impact + best-ROI shortlist (2026-11-12, 16 rows, all with source.md shipped)
Method: same 3 pilot packages, same reviewer harness (now ships source.md beside candidate.md), same blind Opus scoring. glm excluded per owner (delays). Pre-fix luna data quarantined. Blocking counts in this section use the corrected (space-tolerant) parser. Rows: 12 from batch 4 + 5 new shortlist rows from batch 5. b4-muse-luna2 pending a muse retry (gateway misroute recurrence; 2 runs quarantined).

| Row | Models | GT any (defect-rich) | GT blocking | Wrong blk (DR) | Control any/blk | Wrong blk (ctl) | Tokens | Wall s |
|---|---|---|---|---|---|---|---|---|
| n2-sonnet-src | muse, haiku, grok, sonnet | **8/14** | **5/8** | 2 | 1/2, 1 | 1 | 471,626 | 4,237 |
| r2-sonnet-src | haiku x2, grok, sonnet | 4/14 | **4/8** | 2 | **2/2, 2** | 1 | 594,072 | 5,624 |
| n4-sonnet-src | muse, haiku, sonnet | 4/14 | 2/8 | 1 | 1/2, 0 | 1 | 311,505 | 2,145 |
| b4-sonnet-luna2 | sonnet, luna x2 | 4/14 | 0/8 | 3 | 2/2, 1 | 0 | 139,660 | 1,438 |
| b4-terra-muse-haiku | terra, muse, haiku | 3/14 | 2/8 | **0** | 1/2, 1 | **0** | 233,549 | 1,417 |
| b4-terra-luna-muse | terra, muse, luna | 3/14 | 2/8 | 3 | 1/2, 1 | 1 | 68,221 | 832 |
| c3-luna-grok-src | luna, grok | 3/14 | 3/8 | 1 | 1/2, 0 | 2 | 180,601 | 2,784 |
| r3-luna2-grok-src | luna x2, grok | 3/14 | 1/8 | 4 | 2/2, 1 | 1 | 169,602 | 2,662 |
| n2-muse-haiku-grok-src | muse, haiku, grok | 3/14 | 2/8 | 3 | 1/2, 0 | 1 | 362,443 | 3,950 |
| n5-sonnet-src | muse, luna, sonnet | 3/14 | 1/8 | 2 | 1/2, 0 | 1 | 134,398 | 1,574 |
| b4-sonnet-terra | sonnet, terra | 2/14 | 0/8 | 3 | 1/2, 0 | 1 | 98,962 | 836 |
| r1-haiku-luna2-src | haiku, luna x2 | 2/14 | 1/8 | 3 | 1/2, 0 | 1 | 205,923 | 1,399 |
| n5-muse-luna-src | muse, luna | 2/14 | 1/8 | 1 | 1/2, 1 | **0** | 64,367 | 733 |
| n3-muse-luna-grok-src | muse, luna, grok | 2/14 | 0/8 | 3 | 1/2, 0 | 1 | 229,684 | 3,275 |
| terra-alone-src | terra | 1/14 | 1/8 | 4 | 0/2, 0 | 1 | 7,241 | 182 |
| sol-alone-src | sol | 1/14 | 1/8 | 3 | 0/2, 0 | 1 | 11,588 | 410 |

### Headline: source.md changed the picture completely
- **n2-sonnet-src (muse+haiku+grok+sonnet, with source.md) caught 8/14 GT defects and 5/8 blocking** — the best result in the entire study, versus 2/14-0/8 for the same-nominal panel in batch 3 without source.md. The earlier "0/8 blocking recall everywhere" conclusion was an artifact of the missing source document: with it, panels find most blocking defects.
- Sonnet-bearing panels dominate: 4 of the top 5 rows. r2-sonnet-src alone matched arm-B-level coverage with 4/8 blocking and a perfect control (2/2, both blocking).
- Terra and sol, freed from the missing-file refusal, are viable cheap blockers (1/8 blocking alone at 7-12k tokens), but noisy (3-4 wrong blockers each).

### Owner's 7-combo ROI ranking (defect-rich catches per 100k tokens, blocking recall as tiebreak)
1. **terra+luna+muse (b4-terra-luna-muse)** — 3/14 any, 2/8 blocking at 68,221 tokens/832 s: 4.4 catches per 100k tokens, best ROI of the shortlist by a wide margin.
2. sonnet+luna+muse (n5-sonnet-src) — 3/14, 1/8 at 134k: 2.2/100k.
3. sonnet+2xluna (b4-sonnet-luna2) — 4/14, 0/8 at 140k: 2.9/100k but zero blocking recall.
4. haiku+2xluna (r1-haiku-luna2-src) — 2/14, 1/8 at 206k: 1.0/100k.
5. terra+muse+haiku (b4-terra-muse-haiku) — 3/14, 2/8 at 234k: 1.3/100k but the cleanest precision of the shortlist (0 wrong blockers anywhere).
6. sonnet+terra (b4-sonnet-terra) — 2/14, 0/8 at 99k: 2.0/100k but no blocking recall.
7. muse+2xluna (b4-muse-luna2) — PENDING muse retry (gateway misroute); scoring to follow.
Best quality regardless of cost: n2-sonnet-src (8/14, 5/8) — 472k tokens. Best value: terra+luna+muse at 1/7th that cost for 2/8 blocking.

### CORRECTION (2026-11-12 16:55 UTC): n2-sonnet-src re-scored; "8/14, 5/8" was a corrupted judge
The designSpec judge for n2-sonnet-src died with an Opus API error but left a fabricated-looking score.json (8 rows/6 blocking/8-of-10 GT — impossible against a 4-row, 0-blocking, PASS merged report). All 48 -src judge runs audited: this was the only failure (35 clean + 12 earlier-batch clean; 1 bad). Score invalidated (kept as *.invalid-apierror), re-judged fresh (label W): designSpec = 2 any (GT3, GT7), 0 blocking — the truth matches the merged report (4 non-blocking rows, PASS).
CORRECTED n2-sonnet-src totals: defect-rich 2/14 any, 0/8 blocking, 1 wrong blocker; control 1/2, 1 blocking, 1 wrong blocker. The "source.md fixed the panels / 8-of-14" headline from the previous section is RETRACTED. Corrected batch-4/5 leaders are: r2-sonnet-src 4/14-4/8 (best blocking recall), n4-sonnet-src and b4-sonnet-luna2 4/14. source.md still clearly changed behavior (luna/terra/sol now review; blocking findings exist across models; every -src row's merged verdicts are FAIL-heavy vs batch 1-3's frequent PASSes), but the dramatic recall jump was one judge's API-error artifact. Sonnet rows still lead; arm A efficiency comparison unaffected (arm A numbers came from the separately-run pilot judges, all clean).

## Batch 6: muse-ember-1.0 replacement study (2026-11-12, 6 rows, source.md shipped)
muse-wonder-1.0 hit its weekly limit; every row below re-runs a batch-4/5 top-5 panel with muse-ember-1.0 in the muse slot (all reviewers fresh; all 60 runs model_ok=true, zero fallback triggers; blind-scored clean, 0 judge failures).

| Row (ember) | vs original (muse-wonder) | GT any DR | GT blk DR | Wrong blk DR | Control | Tokens | Wall s |
|---|---|---|---|---|---|---|---|
| r2-sonnet-ember | r2-sonnet-src 4/14, 4/8 | 2/14 | 1/8 | 1 | 2/2, 2 blk, 0 wb | 682,112 | 5,156 |
| n4-sonnet-ember | n4-sonnet-src 4/14, 2/8 | 0/14 | 0/8 | 3 | 2/2, 2 blk, 0 wb | 265,294 | 1,411 |
| terra-muse-haiku-ember | terra-muse-haiku 3/14, 2/8, 0 wb | 2/14 | 0/8 | 3 | 1/2, 1 blk, 0 wb | 181,474 | 893 |
| terra-luna-muse-ember | terra-luna-muse 3/14, 2/8 | 2/14 | 1/8 | 3 | 1/2, 1 blk, 1 wb | 58,836 | 568 |
| n5-sonnet-ember | n5-sonnet-src 3/14, 1/8 | 3/14 | 1/8 | 1 | 0/2, 0 blk | 134,653 | 1,036 |
| b4-muse-ember-luna2 | (new: the 7th shortlist slot) | 2/14 | 1/8 | 3 | 1/2, 0 blk | 63,211 | 755 |

### Findings
- muse-ember is a WEAKER reviewer than muse-wonder on these panels: every comparable row dropped on defect-rich coverage (r2 4/14->2/14, n4 4/14->0/14, terra-muse-haiku 3/14->2/14 and lost its 0-wrong-blocker precision, terra-luna 3/14->2/14). Only n5-sonnet-ember matched its original (3/14).
- Ember rows are uniformly better on the control package (two perfect 2/2-both-blocking rows with 0 wrong blockers) — ember shifts panels toward precision on clean plans while catching fewer real defects on defect-rich ones.
- The 7th shortlist slot is now complete: muse+2xluna (as b4-muse-ember-luna2, 2/14-1/8 at 63k tokens) ranks mid-pack; it does not displace terra-luna-muse (2/14-1/8 at 59k with the same catches — statistically identical, muse brand irrelevant at this cost point).
- Cost note: muse-ember runs slightly cheaper per review than muse-wonder (~2.5-3.5k tokens vs ~16k), which is why ember rows' totals fell despite equal run counts.
- Verdict: if muse must be replaced, expect a real recall drop on defect-rich packages; pairing ember with sonnet (n5-sonnet-ember, 3/14-1/8, 1 wrong blocker, 135k) best preserves value. The corrected overall leader remains r2-sonnet-src (muse-wonder version, 4/14-4/8) until muse-wonder returns.

### CORRECTION (2026-11-12 19:05 UTC): r2 never contained muse
Verified from meta.json on disk: r2-sonnet-src (and r2-haiku2-grok, r2-sonnet) = haiku x2 + grok + sonnet, NO muse. Batch 6 wrongly treated r2 as a muse-wonder row and ADDED muse-ember as a 5th reviewer (r2-sonnet-ember = haiku x2 + grok + sonnet + ember). Consequences:
- The r2 line in the batch-6 table is not a muse swap: the same 4 reviewers plus ember scored 2/14-1/8 vs 4/14-4/8. This is evidence of large run-to-run variance (n=1 rows), not of ember weakness.
- "Every comparable row dropped" now rests on 4 rows: n4 4->0/14, terra-muse-haiku 3->2/14, terra-luna 3->2/14, n5 3->3/14. Ember still looks weaker on defect-rich, but the effect is within the variance the r2 pair shows; treat it as UNVERIFIED until repeated.
- "r2-sonnet-src (muse-wonder version)" is wrong: r2-sonnet-src has no muse and does not depend on muse-wonder's return. It is available to run now.
- The true 5th muse-wonder row that should have been re-run was a different one (candidates: n2-muse-haiku-grok-src, n5-muse-luna-src, n3-muse-luna-grok-src); not run.

## Batch 7: ember / luna / haiku / grok combinations (2026-11-12, 5 rows, source.md shipped)
Owner order 19:38 UTC; e4-haiku2-ember CANCELLED by owner at 19:41 (partial files kept under reviews/combos/e4-haiku2-ember/, not merged or scored). 45 runs (5 rows x 3 packages): all model_ok=true, findings block present, 0 fallback triggers; 15 merges rc=0; 15 blind Opus judges, API-error audit bad=0. Streams: ember -P4, other -P6. Per-model attribution script and outputs: analysis/attrib.py, attrib.out, doubles.out.

| Row | Models | GT any DR | GT blk DR | Wrong blk DR | Control any/blk | Wrong blk ctl | Tokens | Wall s |
|---|---|---|---|---|---|---|---|---|
| e1-grok-ember-luna | grok, ember, luna | 2/14 | 1/8 | 4 | 1/2, 1 | 0 | 240,961 | 4,401 |
| e2-ember-luna2-rep | ember, luna x2 | 2/14 | 1/8 | 2 | 1/2, 1 | 0 | 68,445 | 710 |
| e3-ember2-luna | ember x2, luna | 2/14 | 1/8 | 3 | 1/2, 0 | 1 | 76,026 | 588 |
| e5-haiku-ember-luna | haiku, ember, luna | 2/14 | 1/8 | 2 | 0/2, 0 | 1 | 264,641 | 1,412 |
| e6-haiku-ember2 | haiku, ember x2 | 2/14 | 1/8 | 2 | 0/2, 0 | 2 | 197,084 | 843 |

### Findings
- All five rows tie at 2/14 any, 1/8 blocking on defect-rich. Defect-rich catch cannot separate them, so cost and control precision decide.
- Cost per identical result: e2 and e3 (68k, 76k tokens, ~10 min wall) vs e5 265k, e1 241k (4,401 s, grok dominates), e6 197k. Adding haiku or grok bought no measurable catches for 130-200k extra tokens.
- Control package: e1 and e2 best (1/2, 1 blocking, 0 wrong blockers). Both haiku-bearing rows (e5, e6) missed the control entirely (0/2) with 1-2 wrong blockers.
- Replication check (e2 = same models as b4-muse-ember-luna2): totals replicate (2/14-1/8 both; wrong blockers 3 vs 2; tokens 63k vs 68k) but the specific catches differ (original: designSpec GT7, alias GT2; replica: designSpec GT3+GT7, alias none). Row totals are stable at this level; which defects are caught is not.
- Same-model doubling (all valid src-era data now): luna doubled in 10 panel-packages, ember in 4, haiku in 4. The second run never caught a defect the first run lacked (gain 0 over the better single run in all 18 cases). haiku's two runs found identical defects (overlap 8 of 8). luna doubles added 16 wrong blockers across the 10 panels; ember doubles 7 across 4. Attribution is parsed from judge notes (53 of 53 judged catches credited in the earlier check; not re-verified for batch 7): treat as approximate. Single-run rows, so +-2 defects is noise.
- Cumulative per-reviewer-run (defect-rich, 36 ember runs now incl. batch 7 included in 26 attributed): ember 0.65 defects/run, 0.62 wrong blockers/run; luna 0.30 / 0.75; haiku 1.35 / 0.65; grok 1.19 / 1.00.

### CORRECTION (2026-11-12 20:30 UTC): "second run of the same model adds nothing" is RETRACTED
Owner challenge: if a doubled model adds nothing, ember+2xluna (1/2 control) should match haiku+ember+luna (0/2). It did not, and the inconsistency exposes two defects in the doubling analysis:
1. ATTRIBUTION FLAW. analysis/attrib.py credits a ground-truth catch to EVERY reviewer listed on the merged ledger row, not to the reviewer(s) the judge actually cited. Example: e2 control GT2 sits on row L1 (members t2b-1, t3-1, t4-1) but the judge cites only R2 and R3 (the two lunas), not R1 (ember). The "haiku twice found identical defects, overlap 8 of 8" result is largely this artifact (merged rows list both haiku reviewers), and the "gain 0 in all 18 cases" result is not trustworthy.
2. NO POWER. The doubling test ran on defect-rich packages where a single luna/ember run catches ~0.25-0.3 defects. At that base rate "no extra catch" is what noise alone produces; it cannot show that a second run is worthless.
Independent per-reviewer check (control package, GT2 keyword in each reviewer's own findings block, 83 src-era runs): chance a single run raises GT2 = grok 7/8, muse-wonder 8/9, terra 4/6, sonnet 6/9, luna 13/22 (59%), haiku 4/13 (31%), ember 4/13 (31%). Single runs are coin flips; the same model on the same package varies run to run. Under independence, two luna runs raise GT2 with p ~ 0.84 (vs 0.59 for one): a second run DOES add. haiku+ember+luna raising it has p ~ 0.80, so its 0/2 was a ~1-in-5 miss, not evidence that haiku subtracts. Keyword matching is a rough proxy (not judge-verified).
Consequence: row-level scores (single runs) are noisy at +-1 control defect; do not rank rows on 1-defect differences. "Haiku and grok bought no catches" in the batch-7 findings rests on the same single-run noise and is UNVERIFIED. The sound conclusion is only that batch-7 rows are statistically indistinguishable on defect-rich (all 2/14-1/8).

## Batch 8 + FINAL TABLE: replicate study with 2x-vs-1x impact (2026-11-12)
Owner order 20:37 UTC: 8 combos x 4 replicates (+ ember+luna 1x baseline added by worker, flagged) x 3 packages = 300 reviewer runs: all model_ok=true, findings block present, 0 fallback triggers; 108 merges rc=0; 108 blind Opus judges, API-error audit bad=0. Prior matching rows folded in: ember+2luna += b4-muse-ember-luna2, e2-ember-luna2-rep; sonnet+luna+ember += n5-sonnet-ember; haiku+ember+terra += terra-muse-haiku-ember; 2ember+luna += e3-ember2-luna; haiku+2luna += r1-haiku-luna2-src. Three single batch-7 rows kept as references. Source: analysis/b8-table.py, analysis/b8-final.md.
Wall columns: "reviewer-s summed" = total reviewer seconds across all reviewers (compute cost); "elapsed" = per package the slowest reviewer, summed over 3 packages (approximate time if reviewers run in parallel). Tokens = reviewer output tokens, all 3 packages. DR = the two defect-rich packages (14 ground-truth defects, 8 blocking); control = the third package (2 defects).

### Final table (mean over runs; range in brackets)
| Combo | Models | 2x model | Runs | Defect-rich found /14 mean (range) | Blocking /8 mean (range) | Wrong blockers (DR) | Control found /2 | Control wrong blk | Tokens (mean) | Wall: reviewer-s summed / elapsed s |
|---|---|---|---|---|---|---|---|---|---|---|
| ember + luna (1x baseline) | ember, luna | - | 4 | 2.2 (2-3) | 0.5 (0-1) | 2.0 | 0.00 | 1.50 | 52,398 | 432 / 300 |
| ember + 2x luna | ember, luna x2 | luna 2x | 6 | 1.8 (1-2) | 1.0 (1-1) | 1.8 | 0.83 | 0.83 | 63,644 | 761 / 348 |
| 2x ember + luna | ember x2, luna | ember 2x | 5 | 1.6 (1-2) | 1.0 (1-1) | 1.8 | 0.60 | 1.20 | 84,527 | 597 / 322 |
| 2x luna + 2x ember | luna x2, ember x2 | luna 2x, ember 2x | 4 | 1.8 (1-3) | 0.5 (0-1) | 4.8 | 0.25 | 1.50 | 91,416 | 855 / 342 |
| ember + terra | ember, terra | - | 4 | 0.5 (0-1) | 0.2 (0-1) | 2.8 | 0.50 | 1.25 | 37,255 | 266 / 162 |
| sonnet + ember | sonnet, ember | - | 4 | 2.5 (2-4) | 0.2 (0-1) | 0.2 | 0.75 | 1.25 | 142,967 | 910 / 766 |
| sonnet + luna + ember | sonnet, luna, ember | - | 5 | 2.2 (2-3) | 0.6 (0-1) | 2.0 | 0.80 | 1.00 | 138,551 | 1,135 / 676 |
| haiku + ember + terra | haiku, ember, terra | - | 5 | 2.0 (2-2) | 0.6 (0-1) | 3.2 | 1.00 | 1.40 | 191,128 | 971 / 684 |
| haiku + 2x luna | haiku, luna x2 | luna 2x (no 1x baseline) | 5 | 2.2 (2-3) | 1.4 (1-2) | 3.0 | 0.80 | 1.60 | 191,018 | 1,355 / 715 |
| (ref, single run) grok + ember + luna | grok, ember, luna | - | 1 | 2.0 (2-2) | 1.0 (1-1) | 4.0 | 1.00 | 0.00 | 240,961 | 4,401 / 3,897 |
| (ref, single run) haiku + ember + luna | haiku, ember, luna | - | 1 | 2.0 (2-2) | 1.0 (1-1) | 2.0 | 0.00 | 1.00 | 264,641 | 1,412 / 910 |
| (ref, single run) haiku + 2x ember | haiku, ember x2 | ember 2x | 1 | 2.0 (2-2) | 1.0 (1-1) | 2.0 | 0.00 | 2.00 | 197,084 | 843 / 609 |

### Impact of running a model twice (vs the ember + luna 1x baseline, 4 runs)
| Doubling vs the 1x baseline (ember + luna) | Runs (2x vs 1x) | Delta defect-rich found | Delta blocking | Delta wrong blockers | Delta control found | Delta tokens | Delta wall (reviewer-s / elapsed) |
|---|---|---|---|---|---|---|---|
| 2nd luna (ember + luna x2 vs ember + luna) | 6 vs 4 | -0.42 (within noise) | +0.50 (within noise) | -0.2 | +0.83 (beyond noise) | +11,246 | +329 / +47 |
| 2nd ember (ember x2 + luna vs ember + luna) | 5 vs 4 | -0.65 (within noise) | +0.50 (within noise) | -0.2 | +0.60 (beyond noise) | +32,129 | +164 / +22 |
| 2nd luna AND 2nd ember | 4 vs 4 | -0.50 (within noise) | +0.00 (within noise) | +2.8 | +0.25 (within noise) | +39,018 | +423 / +42 |
| 2nd ember on top of 2x luna | 4 vs 6 | -0.08 (within noise) | -0.50 (within noise) | +2.9 | -0.58 (within noise) | +27,772 | +94 / -5 |
| 2nd luna on top of 2x ember | 4 vs 5 | +0.15 (within noise) | -0.50 (within noise) | +3.0 | -0.35 (within noise) | +6,889 | +258 / +20 |

Independent check (control package, per-reviewer findings, GT2 keyword proxy; not judge-verified): share of panels where at least one reviewer of that model raises the control defect GT2:
| Model | 1x panels: at least one reviewer raises control GT2 | 2x panels: at least one of the two raises it |
|---|---|---|
| luna | 1/4 | 5/6 |
| ember | 2/4 | 3/5 |

### Reading the table (replicates; rows of 4-6 runs, spread is real)
- Defect-rich catch does not separate the ember/luna family: every panel averages 1.6-2.5 of 14. The only separations that clear the spread: ember + terra is worse (0.5/14, 37k tokens); sonnet + ember is best on defect-rich catch (2.5, range 2-4) with by far the fewest wrong blockers (0.2) but ~143k tokens and 766 s elapsed.
- Second luna (ember + 2x luna vs ember + luna): defect-rich unchanged (-0.4, noise), blocking +0.5 (noise), control found +0.83 (control values are 0/1/2 on 4-6 runs, so the "beyond noise" flag is fragile because the baseline had zero variance), cost +11k tokens and +47 s elapsed. The independent proxy agrees: some luna raised control GT2 in 5 of 6 doubled panels vs 1 of 4 single panels. Best evidence anywhere in this study that a second same-model run helps: on the control package.
- Second ember (2x ember + luna vs ember + luna): defect-rich unchanged (-0.65, noise); control +0.60; +32k tokens (ember runs are cheap but 2x) and +22 s elapsed. Proxy: 3/5 vs 2/4, inconclusive.
- Both doubled (2x luna + 2x ember): no defect-rich gain, 4.8 wrong blockers per row (vs 2.0 for the 1x baseline): the largest false-blocker cost, no catch benefit. Neither marginal second reviewer on top of a doubled pair beats the pair.
- haiku + 2x luna has the best blocking mean (1.4/8) but no 1x baseline, so its doubling effect is not measurable.
- Cost-effectiveness (defect-rich catches per 100k tokens): ember + luna 4.2, ember + 2x luna 2.8, 2x ember + luna 1.9, sonnet + ember 1.7, sonnet + luna + ember 1.6, haiku rows ~1.1, ember + terra 1.3.
- Overall: nothing found beats ~2.2/14 except sonnet + ember at 2.5; ember + luna (52k tokens, 5 min) is the cost-efficiency winner; adding a second luna is the one doubling with supporting evidence (control package). Rows are 4-6 runs; ranges overlap almost everywhere, so rank only differences larger than the shown ranges.

## Batch 9: haiku / sonnet + 2x luna + 2x ember (2026-11-12, 8 rows x 3 packages = 120 runs, 4 replicates each)
Owner order 22:16 UTC. 120 runs all model_ok after reruns; 24 merges; 24 blind Opus judges, API-error audit bad=0 (20 judges first failed with rc=127 because the `claude` binary was replaced at 23:05 and were re-run; none left bad). INCIDENT: during the 22:17-22:19 claude-binary replacement the cyclic fallback ladder spun 69 steps in 3 s and put one "ember" slot on claude-haiku-5-5 (h1-r1 alias t2b-1) and one on Qwen3.8-max (h2-r1 design t3-1, ran 42 min until killed). Both would have passed the model_ok check (expected_model is overwritten on fallback). Both quarantined, re-run on muse-ember-1.0 with NOFALLBACK=1, h1-r1 alias merge redone; run-reviewer.sh now never revisits a model, never uses glm/Qwen3.8-max, honours NOFALLBACK=1; details in combos/SPEC.md. Source: analysis/b9-table.py, b9-final.md.

| Combo | Models | Runs | Defect-rich found /14 mean (range) | Blocking /8 mean (range) | Wrong blockers (DR) | Control found /2 | Control wrong blk | Tokens (mean) | Wall: reviewer-s summed / elapsed s | Found per 100k tokens |
|---|---|---|---|---|---|---|---|---|---|---|
| 2x luna + 2x ember (g6) | luna x2, ember x2 | 4 | 1.8 (1-3) | 0.5 (0-1) | 4.8 | 0.25 | 1.50 | 91,416 | 855 / 342 | 1.9 |
| haiku + 2x luna + 2x ember (h1) | haiku, luna x2, ember x2 | 4 | 2.2 (2-3) | 1.8 (1-3) | 3.0 | 1.00 | 1.75 | 246,213 | 1,537 / 682 | 0.9 |
| sonnet + 2x luna + 2x ember (h2) | sonnet, luna x2, ember x2 | 4 | 2.2 (2-3) | 0.8 (0-1) | 3.5 | 1.50 | 0.25 | 189,325 | 1,636 / 738 | 1.2 |
| (ref) haiku + 2x luna | haiku, luna x2 | 5 | 2.2 (2-3) | 1.4 (1-2) | 3.0 | 0.80 | 1.60 | 191,018 | 1,355 / 715 | 1.2 |
| (ref) sonnet + ember | sonnet, ember | 4 | 2.5 (2-4) | 0.2 (0-1) | 0.2 | 0.75 | 1.25 | 142,967 | 910 / 766 | 1.7 |
| (ref) sonnet + luna + ember | sonnet, luna, ember | 5 | 2.2 (2-3) | 0.6 (0-1) | 2.0 | 0.80 | 1.00 | 138,551 | 1,135 / 676 | 1.6 |
| (ref) ember + luna | ember, luna | 4 | 2.2 (2-3) | 0.5 (0-1) | 2.0 | 0.00 | 1.50 | 52,398 | 432 / 300 | 4.3 |

| Effect of adding one reviewer | Runs | Delta defect-rich found | Delta blocking | Delta wrong blockers | Delta control found | Delta tokens | Delta wall (reviewer-s / elapsed) |
|---|---|---|---|---|---|---|---|
| adding haiku to 2x luna + 2x ember | 4 vs 4 | +0.50 (within noise) | +1.25 (beyond noise) | -1.8 | +0.75 (beyond noise) | +154,797 | +682 / +339 |
| adding sonnet to 2x luna + 2x ember | 4 vs 4 | +0.50 (within noise) | +0.25 (within noise) | -1.2 | +1.25 (beyond noise) | +97,909 | +781 / +396 |
| 2nd luna + 2nd ember on top of sonnet + luna + ember | 4 vs 5 | +0.05 (within noise) | +0.15 (within noise) | +1.5 | +0.70 (within noise) | +50,774 | +501 / +62 |
| 2x luna + 1 more ember on top of sonnet + ember | 4 vs 4 | -0.25 (within noise) | +0.50 (within noise) | +3.2 | +0.75 (within noise) | +46,358 | +726 / -28 |
| 2x ember on top of haiku + 2x luna | 4 vs 5 | +0.05 (within noise) | +0.35 (within noise) | +0.0 | +0.20 (within noise) | +55,194 | +182 / -33 |

Reading (4-5 runs per row; ranges overlap, only flagged-beyond-noise deltas are meaningful):
- Adding haiku to 2x luna + 2x ember: blocking 0.5 -> 1.8/8 (beyond noise), control 0.25 -> 1.0, wrong blockers 4.8 -> 3.0, for +155k tokens and +339 s elapsed. Adding sonnet instead: control 0.25 -> 1.5 (beyond noise) with wrong blockers 4.8 -> 3.5 and blocking only 0.8; +98k tokens and +396 s elapsed. Defect-rich catch is unchanged by either (2.2 vs 1.8, noise).
- Neither new row beats the cheaper references: sonnet + ember (2.5/14, 0.2 wrong blockers, 143k) and ember + luna (2.2/14, 52k) give the same catch for 1/2 to 1/4 of the cost. Found per 100k tokens: h1 0.9, h2 1.2, sonnet + ember 1.7, ember + luna 4.3.
- haiku + 2x luna + 2x ember (h1) is the best blocking mean of any ember/luna row (1.8/8, up to 3) but costs 246k tokens. Row h1-r1 reached 3/14-3/8; the other three reps scored 2/14 any.

## Which untried combinations are worth testing (2026-11-12, based on 71 scored valid rows, 32 distinct model sets)
Evidence base (analysis/untried.py, untried.out):
- Ceiling: defect-rich catch per row is 2/14 in 43 of 71 rows, 3/14 in 12, 4/14 in 4, never above 4. Nearly every row catches the same two defects (designSpec GT3 in 63 rows, GT7 in 50). designSpec GT1, GT2, GT10 and alias GT4 were never caught by any valid row; GT4-GT6, GT8-GT9 and alias GT1/GT3 appear in only 1-3 rows. Blocking recall above 2-3/8 requires catching defects that no model has caught yet.
- Model presence (rows with vs without): grok 2.62 vs 2.00 found, 1.50 vs 0.84 blocking (n=8, confounded); wonder 2.75 vs 1.98 (n=8, exhausted this week); sonnet 2.43 vs 1.92 found but lower blocking (0.71 vs 1.00) and fewer wrong blockers (1.95 vs 2.68); haiku 2.26 vs 1.98 found, 1.30 vs 0.73 blocking; ember 1.88 vs 2.55 found (n=51 vs 20, confounded with cheap small panels); terra 1.64 vs 2.18 (worse). luna is neutral.
- Combos beyond the ember/luna/terra/sol family have the only sub-4% evidence of a higher ceiling, and they are mostly n=1.

Candidates, ranked by expected value of information (all are guesses from n<=8 rows; ranges are judgment, UNVERIFIED):
1. Replicate r2-sonnet-src (haiku x2 + grok + sonnet), 4 runs, ~594k tokens each (~2.4M). Best row ever (4/14, 4/8, control 2/2) but a single run; its only comparison (the same four plus ember) fell to 2/14-1/8. If the mean holds >=3.5/14 and >=3/8 it is the only real improvement found; if not, the study's high-water mark is noise. Tried, not untried, but the highest-value test.
2. grok + sonnet (untried, ~250k, ~15 min elapsed). Expect 2.5-3.5/14, blocking 0.5-2, wrong blockers 1-2. Grok is the only model that ever raised designSpec GT6 and raised the control defect in 7 of 8 runs; sonnet has the best coverage and fewest wrong blockers. Question: are these two the active ingredients of r2-sonnet-src?
3. haiku + sonnet (untried, ~260k). Expect 2.5-3.2/14, blocking 1-2. haiku adds the blocking claims (1.30 vs 0.73 with-vs-without); n4-sonnet-src (haiku + sonnet + wonder) scored 4/14-2/8. Question: does it replicate without wonder?
4. grok + haiku + sonnet (untried, ~420k): r2-sonnet-src minus the duplicate haiku. Expect 3-4/14, blocking 2-4. Question: is the second haiku needed? (Row-level evidence says the second same-model run adds little on defect-rich.)
5. Replicate c3 luna + grok (tried once: 3/14, 3/8, 181k), 4 runs (~720k). Cheapest high blocking result in the study; a luna-heavy sibling (luna x2 + grok) fell to 1/8, so the n=1 may be luck.
When muse-wonder quota returns (next week): replicate n4-sonnet-src (wonder + haiku + sonnet) and try wonder + grok + sonnet; wonder is the only model with a clearly lower wrong-blocker rate (1.75 vs 2.56) and the highest control hit rate (8/9). Availability UNVERIFIED.

NOT worth testing: any further ember/luna/terra/sol variants or doublings (about 40 rows between 1.6 and 2.5/14: no lever there); panels of 5+ reviewers (no catch gain, cost 250k+); muse-spark and muse-wonder-full (never run, so no evidence: at most a one-run smoke test); ember + terra (worst row, 0.5/14).
Non-combo lever: the five defects no valid row has ever caught (designSpec GT1, GT2, GT10, alias GT4, and alias GT3 in 1 row) are not reachable by model mix at this evidence level; they point at the review brief, the packages or the ground truth, which is outside this study.

## FINAL RESULTS AND DECISION (2026-11-13) - supersedes every earlier table, ranking and recommendation in this file
Testing is closed by owner order. Batch 10 (grok+sonnet, haiku+sonnet) is dropped and excluded. Six independent read-only audits (identity, report validity, inputs/timing, merges, scoring, aggregation; outputs in analysis/audits/) re-checked every valid-era run (71 rows, 213 row-packages). The audits did NOT find fabricated scores or wrong-document runs. They found these defects, all now corrected or disclosed:
1. BLOCKING DEFINITION (audit F). The judge's gt_covered_blocking = defect matched by a blocking-flagged ledger row, which can include defects that are not blocking_in_implement. Tables previously printed it over a denominator of 8. Over 71 rows the judge counts 65 "blocking" catches but only 38 are real blocking defects. All tables below show BOTH: "Real blocking /8" (judge-blocking AND the defect has blocking_in_implement=true) and "Judge-blocking". Consequences: r2-sonnet-src 4/8 is 3 real; c3-luna-grok-src 3/8 is 1 real; haiku + 2x luna 1.4 is 1.2; h1 1.75 is 1.00; ember + 2x luna 1.00 judge-blocking is 0.17 real, so the earlier "second luna adds +0.5 blocking" is reversed (real blocking falls to 0.17 from 0.50).
2. MERGE DROPS FINDINGS SILENTLY (audit D). The merge keeps only well-formed finding lines: anchors over 200 characters (56), anchor2 over 200 (18), claims over 300 (14), bad severity, bad refs are discarded with no error. 80 reviewer-level cases, 49 blocking findings lost; by model luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet 0, terra 0, sol 0. Four verdicts flipped FAIL->PASS (g3-sonnet-luna-ember-r3 alias, g5-ember2-luna-r2 alias, n5-sonnet-ember control, plus total-loss merges). This penalises luna, ember and wonder systematically. 83 merged rows lump unrelated findings into one row (chaining), which can distort matching to ground truth. Stale merges: n2-terra, r2-sol merged before their reports were re-run; n5-sol and n5-terra merged from a report no longer in the row.
3. SOURCE.MD OFTEN NOT OPENED (audit C). 161 valid-era runs never referenced source.md (ember 81, luna 49, haiku 16, grok 7, wonder 6, sonnet 2): those reviewers reviewed the plan source-blind even though the file was present. Part of ember's and luna's low catch is likely this, not model ability. No run read ground truth or other reviewers' reports; old-era runs browsed sibling plan packages in the sandbox repo (WARN, old rows only).
4. TERRA/SOL REFUSALS STILL OCCUR (audit B). 51 reports say incomplete (16 empty terra reviews in valid-era rows: g4-haiku-ember-terra, g8-ember-terra, b4-*terra*, terra-*-ember rows) even with source.md shipped; ember+terra's 0.5/14 is largely terra returning nothing. luna has the weakest anchor fidelity (91.4% of quoted anchors verbatim vs 98-100% for the others).
5. MODEL IDENTITY (audit A): 2 b4-muse-luna2 t2b-1 "wonder" runs were served terra (row already quarantined); no other mismatches; no fallback logs before the batch 9/10 incident (and the ladder flaw that hid it is fixed). grok runs report the gateway id grok-4.7-build (benign).
6. SCORING (audit E): 294 judge outputs clean (no API errors, none edited after the judge finished, labels/combos/packages consistent, internal counts match merged ledgers). Independent blind re-judge of 12 rows: 12/12 exact agreement; 19 of 19 recorded catches confirmed, one borderline defect (GT8) would add 1 (recall 0.95). Stale scores: r2-sonnet (3 scores predate a re-merge) excluded; 10 older rows have merged reports only in quarantine and are not used.
7. STALE TEXT (audit F): earlier tables/lines in this file still print retracted numbers (n2-sonnet-src 8/14-5/8 at its table row; "second run of the same model adds nothing"; "haiku overlap 8 of 8"; "ember is weaker than wonder" unqualified; r2 as a muse row; pre-source.md luna/terra/sol rows in batch 1-3 recommendations; 4/8 and 3/8 blocking claims). They are superseded by this section; use only the tables below.
Statistics (audit F, Welch and permutation over run-level values, n=4-6): only these survive: second luna raises control found +0.83 (p 0.004 Welch, 0.048 permutation, baseline all zeros); 2x luna + 2x ember has 2.75-3.25 more wrong blockers than every comparator (permutation p 0.005-0.03); ember + terra is worse than the others by -1.75 found (permutation p 0.029). Everything else "beyond noise" in earlier text does not survive.

### Final tables (valid-era rows only; per-package means summed over the two defect-rich packages; tokens = reviewer output tokens over 3 packages; wall: summed reviewer-seconds / elapsed with reviewers in parallel)
valid-era rows: 71; row-packages scored: 213; row-packages carrying an audit EXCLUDE flag (A,B incomplete/short,D,E,F): 69

### AS SCORED (all valid-era row-packages)
| Panel | Runs DS/AL/ctl | Found /14 | Real blocking /8 | Judge-blocking | Wrong blockers (DR) | Control found /2 | Ctl wrong blk | Tokens | Wall rev-s / elapsed s | Found per 100k tok | Real-blk per 100k tok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| grok + haiku + haiku + sonnet | 1/1/1 | 4.00 | 3.00 | 4.00 | 2.00 | 2.00 | 1.00 | 594,072 | 5,624 / 2,793 | 0.67 | 0.50 |
| haiku + sonnet + wonder | 1/1/1 | 4.00 | 2.00 | 2.00 | 1.00 | 1.00 | 1.00 | 311,505 | 2,145 / 1,154 | 1.28 | 0.64 |
| luna + luna + sonnet | 1/1/1 | 4.00 | 0.00 | 0.00 | 3.00 | 2.00 | 0.00 | 139,660 | 1,438 / 793 | 2.86 | 0.00 |
| luna + terra + wonder | 1/1/1 | 3.00 | 2.00 | 2.00 | 3.00 | 1.00 | 1.00 | 68,221 | 832 / 410 | 4.40 | 2.93 |
| haiku + terra + wonder | 1/1/1 | 3.00 | 1.00 | 2.00 | 0.00 | 1.00 | 0.00 | 233,549 | 1,417 / 845 | 1.28 | 0.43 |
| grok + luna | 1/1/1 | 3.00 | 1.00 | 3.00 | 1.00 | 1.00 | 2.00 | 180,601 | 2,784 / 2,478 | 1.66 | 0.55 |
| grok + haiku + wonder | 1/1/1 | 3.00 | 1.00 | 2.00 | 3.00 | 1.00 | 1.00 | 362,443 | 3,950 / 2,817 | 0.83 | 0.28 |
| luna + sonnet + wonder | 1/1/1 | 3.00 | 1.00 | 1.00 | 2.00 | 1.00 | 1.00 | 134,398 | 1,574 / 886 | 2.23 | 0.74 |
| grok + luna + luna | 1/1/1 | 3.00 | 0.00 | 1.00 | 4.00 | 2.00 | 1.00 | 169,602 | 2,662 / 2,109 | 1.77 | 0.00 |
| ember + sonnet | 4/4/4 | 2.50 | 0.25 | 0.25 | 0.25 | 0.75 | 1.25 | 142,967 | 910 / 766 | 1.75 | 0.17 |
| ember + ember + haiku + luna + luna | 4/4/4 | 2.25 | 1.00 | 1.75 | 3.00 | 1.00 | 1.75 | 246,213 | 1,537 / 682 | 0.91 | 0.41 |
| ember + luna | 4/4/4 | 2.25 | 0.50 | 0.50 | 2.00 | 0.00 | 1.50 | 52,398 | 432 / 300 | 4.29 | 0.95 |
| ember + ember + luna + luna + sonnet | 4/4/4 | 2.25 | 0.25 | 0.75 | 3.50 | 1.50 | 0.25 | 189,325 | 1,636 / 738 | 1.19 | 0.13 |
| haiku + luna + luna | 5/5/5 | 2.20 | 1.20 | 1.40 | 3.00 | 0.80 | 1.60 | 191,018 | 1,355 / 715 | 1.15 | 0.63 |
| ember + luna + sonnet | 5/5/5 | 2.20 | 0.20 | 0.60 | 2.00 | 0.80 | 1.00 | 138,551 | 1,135 / 676 | 1.59 | 0.14 |
| ember + haiku + luna | 1/1/1 | 2.00 | 1.00 | 1.00 | 2.00 | 0.00 | 1.00 | 264,641 | 1,412 / 910 | 0.76 | 0.38 |
| ember + luna + terra | 1/1/1 | 2.00 | 1.00 | 1.00 | 3.00 | 1.00 | 1.00 | 58,836 | 568 / 288 | 3.40 | 1.70 |
| ember + haiku + terra | 5/5/5 | 2.00 | 0.60 | 0.60 | 3.20 | 1.00 | 1.40 | 191,128 | 971 / 684 | 1.05 | 0.31 |
| sonnet + terra | 1/1/1 | 2.00 | 0.00 | 0.00 | 3.00 | 1.00 | 1.00 | 98,962 | 836 / 688 | 2.02 | 0.00 |
| ember + grok + luna | 1/1/1 | 2.00 | 0.00 | 1.00 | 4.00 | 1.00 | 0.00 | 240,961 | 4,401 / 3,897 | 0.83 | 0.00 |
| ember + ember + haiku | 1/1/1 | 2.00 | 0.00 | 1.00 | 2.00 | 0.00 | 2.00 | 197,084 | 843 / 609 | 1.01 | 0.00 |
| grok + haiku + sonnet + wonder | 1/1/1 | 2.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 471,626 | 4,237 / 2,378 | 0.42 | 0.00 |
| grok + luna + wonder | 1/1/1 | 2.00 | 0.00 | 0.00 | 3.00 | 1.00 | 1.00 | 229,684 | 3,275 / 2,507 | 0.87 | 0.00 |
| luna + wonder | 1/1/1 | 2.00 | 0.00 | 1.00 | 1.00 | 1.00 | 0.00 | 64,367 | 733 / 474 | 3.11 | 0.00 |
| ember + grok + haiku + haiku + sonnet | 1/1/1 | 2.00 | 0.00 | 1.00 | 1.00 | 2.00 | 0.00 | 682,112 | 5,156 / 2,653 | 0.29 | 0.00 |
| ember + luna + luna | 6/6/6 | 1.83 | 0.17 | 1.00 | 1.83 | 0.83 | 0.83 | 63,644 | 761 / 348 | 2.88 | 0.26 |
| ember + ember + luna + luna | 4/4/4 | 1.75 | 0.25 | 0.50 | 4.75 | 0.25 | 1.50 | 91,416 | 855 / 342 | 1.91 | 0.27 |
| ember + ember + luna | 5/5/5 | 1.60 | 0.40 | 1.00 | 1.80 | 0.60 | 1.20 | 84,527 | 597 / 322 | 1.89 | 0.47 |
| sol | 1/1/1 | 1.00 | 1.00 | 1.00 | 3.00 | 0.00 | 1.00 | 11,588 | 410 / 410 | 8.63 | 8.63 |
| terra | 1/1/1 | 1.00 | 1.00 | 1.00 | 4.00 | 0.00 | 1.00 | 7,241 | 182 / 182 | 13.81 | 13.81 |
| ember + terra | 4/4/4 | 0.50 | 0.25 | 0.25 | 2.75 | 0.50 | 1.25 | 37,255 | 266 / 162 | 1.34 | 0.67 |
| ember + haiku + sonnet | 1/1/1 | 0.00 | 0.00 | 0.00 | 3.00 | 2.00 | 0.00 | 265,294 | 1,411 / 812 | 0.00 | 0.00 |

### AUDIT-CLEAN (row-packages with no EXCLUDE flag)
| Panel | Runs DS/AL/ctl | Found /14 | Real blocking /8 | Judge-blocking | Wrong blockers (DR) | Control found /2 | Ctl wrong blk | Tokens | Wall rev-s / elapsed s | Found per 100k tok | Real-blk per 100k tok |
|---|---|---|---|---|---|---|---|---|---|---|---|
| grok + haiku + haiku + sonnet | 1/1/1 | 4.00 | 3.00 | 4.00 | 2.00 | 2.00 | 1.00 | 594,072 | 5,624 / 2,793 | 0.67 | 0.50 |
| haiku + sonnet + wonder | 1/1/1 | 4.00 | 2.00 | 2.00 | 1.00 | 1.00 | 1.00 | 311,505 | 2,145 / 1,154 | 1.28 | 0.64 |
| grok + luna | 1/1/1 | 3.00 | 1.00 | 3.00 | 1.00 | 1.00 | 2.00 | 180,601 | 2,784 / 2,478 | 1.66 | 0.55 |
| luna + sonnet + wonder | 1/1/1 | 3.00 | 1.00 | 1.00 | 2.00 | 1.00 | 1.00 | 134,398 | 1,574 / 886 | 2.23 | 0.74 |
| grok + luna + luna | 1/1/1 | 3.00 | 0.00 | 1.00 | 4.00 | 2.00 | 1.00 | 169,602 | 2,662 / 2,109 | 1.77 | 0.00 |
| haiku + luna + luna | 1/4/5 | 2.50 | 1.50 | 1.50 | 2.75 | 0.80 | 1.60 | 204,212 | 1,429 / 783 | 1.22 | 0.73 |
| ember + ember + haiku + luna + luna | 1/2/4 | 2.50 | 0.50 | 1.50 | 2.50 | 1.00 | 1.75 | 251,030 | 1,516 / 681 | 1.00 | 0.20 |
| ember + luna | 3/2/4 | 2.33 | 0.33 | 0.33 | 2.67 | 0.00 | 1.50 | 50,791 | 434 / 307 | 4.59 | 0.66 |
| ember + sonnet | 3/3/4 | 2.33 | 0.00 | 0.00 | 0.33 | 0.75 | 1.25 | 148,721 | 947 / 812 | 1.57 | 0.00 |
| ember + haiku + luna | 1/1/1 | 2.00 | 1.00 | 1.00 | 2.00 | 0.00 | 1.00 | 264,641 | 1,412 / 910 | 0.76 | 0.38 |
| ember + luna + sonnet | 2/2/3 | 2.00 | 0.00 | 0.50 | 2.50 | 1.00 | 1.33 | 136,876 | 1,131 / 642 | 1.46 | 0.00 |
| ember + ember + luna + luna + sonnet | 1/2/4 | 2.00 | 0.00 | 1.00 | 4.50 | 1.50 | 0.25 | 181,212 | 1,574 / 702 | 1.10 | 0.00 |
| grok + haiku + sonnet + wonder | 1/1/1 | 2.00 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 471,626 | 4,237 / 2,378 | 0.42 | 0.00 |
| ember + luna + luna | 3/4/6 | 1.92 | 0.25 | 0.92 | 2.17 | 0.83 | 0.83 | 64,646 | 769 / 350 | 2.96 | 0.39 |
| ember + ember + luna | 2/3/4 | 1.50 | 1.00 | 1.00 | 2.33 | 0.75 | 1.00 | 78,652 | 588 / 325 | 1.91 | 1.27 |
| sol | 1/1/1 | 1.00 | 1.00 | 1.00 | 3.00 | 0.00 | 1.00 | 11,588 | 410 / 410 | 8.63 | 8.63 |
| terra | 1/1/1 | 1.00 | 1.00 | 1.00 | 4.00 | 0.00 | 1.00 | 7,241 | 182 / 182 | 13.81 | 13.81 |
| ember + ember + luna + luna | 1/3/4 | 1.00 | 0.00 | 0.00 | 4.67 | 0.25 | 1.50 | 89,192 | 820 / 326 | 1.12 | 0.00 |

Reading guide: rows with 1/1/1 are single runs (anecdotes); only rows with 4+ runs per package support any ranking. AUDIT-CLEAN drops every row-package carrying a harness-type EXCLUDE flag (incomplete terra/sol refusals, merge-dropped findings, stale merges, stale/quarantined scores); it removes about a third of the data, so most families have too few clean packages to rank; use it as a robustness check on AS-SCORED, not as the main table.

### Decision
Replicated panels (4+ runs), AS-SCORED:
- Cost champion: ember + luna, 52k tokens, ~5 min elapsed, 2.25/14 found, 0.50 real blocking, 4.3 found per 100k tokens, but 0.00 control found in 4 runs.
- Recommended default: ember + 2x luna, 64k tokens, ~6 min elapsed, 1.83/14 found (within noise of the 2.5 best), 0.17 real blocking, control 0.83 (the only doubling effect that survives testing), 1.83 wrong blockers (lowest of the luna panels).
- High-assurance variant when blocking recall matters: haiku + 2x luna, 191k tokens, ~12 min elapsed, 2.2/14 found, 1.2/8 real blocking (best of any replicated panel), 3.0 wrong blockers.
- Best precision: ember + sonnet, 143k tokens, ~13 min elapsed, 2.5/14 found (best replicated), 0.25 wrong blockers, but 0.25 real blocking.
- Do not use: ember + terra (0.5/14), 2x ember + 2x luna (4.75 wrong blockers), terra or sol alone, haiku + ember + terra, any panel of 5 reviewers (no gain for 2-4x the cost), and anything that relies on muse-wonder until it is back.
Single-run high scores (r2 family grok+haiku x2+sonnet 4/14, 3 real blocking, 594k tokens; haiku+sonnet+wonder 4/14, 2 real blocking, 311k) were never replicated; the one comparison available (the same four plus ember) scored 2/14, so treat them as unconfirmed.
Before any further model testing, fix the harness issues that depress catch across the board: (1) raise or truncate the 200-character anchor limit at merge, or instruct reviewers and re-validate, so findings are not silently discarded; (2) name the source.md path explicitly in the reviewer brief (161 runs never opened it); (3) keep the fallback-ladder fix and the model-identity audit in the runner. No panel catches designSpec GT1, GT2, GT10 or alias GT4, so model choice cannot lift the ceiling past ~2.5/14.

Audit C final figures (correction to item 3 above, which used the pre-skip count): after batch 10 is excluded, 156 valid-era runs of 665 never referenced source.md (ember 81 of 209 = 39%, luna 49 of 222 = 22%, wonder 6 of 25, haiku 15 of 75, grok 4 of 24, sonnet 1 of 63, terra 0 of 44, sol 0 of 3). The cause (the brief never names source.md) is an inference, UNVERIFIED. Timeline: candidates fixed 2026-11-11 17:35 and byte-identical to the sandbox copies; source.md first shipped 2026-11-12 12:59:34; first valid-era run 13:02:27; no valid-era row has a run before that; no reviewer read ground truth, resolution files, other reviewers' reports or this report; no candidate was written; 0 identical report bodies. Cross-row statistics (71 rows, presence effects) are computed from valid-era rows only.
