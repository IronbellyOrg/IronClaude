# Speed-weighted reviewer combinations (Qwen3.8-max excluded)

Why: in the pilot, Qwen3.8-max timed out twice (2 x 3000s) on 3 of 4 runs; the other Tier 3/4 models took 1-23 min.
Observed wall time per run (pilot, seconds): gpt-6-luna 61-148 (thin output, 2.4k-6.7k tokens), claude-haiku-5-5 185-610 (real reviews, ~40k tokens),
grok-4.7 610-957, glm-5.3 805-1435. Tier 3 therefore has one usable model (glm-5.3); Tier 4 has luna, haiku, grok.
Speed weighs more than intelligence, so haiku and luna appear in most combinations and glm in only one.

| Combo dir | Reviewer id = model |
|---|---|
| c1-haiku-luna | t4-1=claude-haiku-5-5, t4-2=gpt-6-luna |
| c2-haiku-grok | t4-1=claude-haiku-5-5, t4-2=grok-4.7 |
| c3-luna-grok | t4-1=gpt-6-luna, t4-2=grok-4.7 |
| c4-haiku-luna-grok | t3-1=claude-haiku-5-5, t4-1=gpt-6-luna, t4-2=grok-4.7 |
| c5-glm-haiku | t3-1=glm-5.3, t4-1=claude-haiku-5-5 |

(Reviewer ids are only labels so the merge accepts them; the model per id is exactly the one in the table.)

## Procedure for ONE combo (you run only your own row)
EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/eval-workspaces/tasklist-review-panel/20261111-a1
Packages: TASK-WF-designSpec-20261107-075614, TASK-WF-makeTheAliasOnly-20261105-051649, TASK-WF-design-20261108-041415

1. For each package and each reviewer in your row, run (at most 2 of these at once in total; the gateway is untested above ~10 parallel runs across all 5 sessions):
   `bash $EVAL/tools/run-reviewer.sh $EVAL <package> <reviewer id> <model> combos/<combo dir>`
   Output lands in $EVAL/<package>/reviews/combos/<combo dir>/. The script checks the observed model and the findings-v1 block, retries once, and writes <id>.cost.json (wall seconds, output tokens). A single attempt is limited to 3000s by the script; if both attempts fail, record the reviewer as INVALID (reason) and continue.
   Run with `run_in_background` and wait; do not poll in a loop.
2. Build a resolution file per package: `jq --argjson m '{"t4-1":"<model>",...}' '.reviewers |= [ .[] | select(.reviewer_id as $i | $m|has($i)) | .model = $m[.reviewer_id] ]' $EVAL/<package>/resolution-live7.json > $EVAL/combos/<combo dir>/<package>/resolution.json`
3. Merge once per package (read `superclaude review merge --help` first; UV is not needed for the superclaude CLI):
   `superclaude review merge --ledger $EVAL/combos/<combo dir>/<package>/ledger.json --doc $EVAL/<package>/candidate.md --round 1 --report <id>=<path to reviews/combos/<combo dir>/<id>.md> ... --resolution <that resolution.json> --out $EVAL/combos/<combo dir>/<package>/merged-1.md`
   If the merge refuses the round (no valid findings block), rerun the reviewer once, then merge again; if still refused record INVALID.
4. Write $EVAL/combos/<combo dir>/RESULT.md: a table per package with reviewer, model, observed model, attempts, wall seconds, output tokens, invalid or thin (under 1000 output tokens) flag, number of findings and number marked blocking in the merged report; and the total wall time and output tokens per package. No scoring.

## Hard limits
- Read-only for the repo: edit no source, change nothing under .dev/tasks/, stage/commit/push nothing, never stage .claude/. Write only under $EVAL/combos/<your combo dir>/, $EVAL/<package>/reviews/combos/<your combo dir>/ and /tmp.
- Do NOT open any ground-truth*.json, any other combo's folder, or the other arms' reviews or merged reports. Scoring is done later by someone else, blind.
- Models: only those in your row, via the script. Never Fable or any Tier 0 model.
- Do not create worktrees. Heartbeat as your preamble says; send worker_done once with --outcome succeeded (or failed) and the RESULT.md path.

## Correction (2026-11-11, after c1 reported)
The brief in tools/run-reviewer.sh listed the category `unpassable-ac`; the merge validator only accepts `unpassable-check`. The script now says `unpassable-check` (old copy: tools/run-reviewer.sh.unpassable-ac). If a merge refuses your round ONLY because of `unpassable-ac`, do not rerun the reviewer: copy the report to <report>.catfix.md with `sed 's/unpassable-ac/unpassable-check/g'`, merge with the copy, keep the original unedited, and say so in RESULT.md (mark the reviewer "category normalised").

## Batch 2 (added 2026-11-11 on the owner's request)
Pool is now glm-5.3, claude-haiku-5-5, gpt-6-luna, grok-4.7 and muse-wonder-1.0 (added by the owner; pilot: 153s, ~17k tokens, valid). Qwen stays out. Same procedure and hard limits as above; the reviewer ids below exist in each package's resolution-live7.json (ids are only labels). Where the same model appears under two ids, run it as two independent reviews (separate runs, separate files).
Cheapest model = gpt-6-luna; in rows without luna the cheapest-to-double is claude-haiku-5-5.

| Combo dir | Reviewer id = model |
|---|---|
| r1-haiku-luna2 | t4-1=claude-haiku-5-5, t4-2=gpt-6-luna, t3-1=gpt-6-luna |
| r2-haiku2-grok | t4-1=claude-haiku-5-5, t3-1=claude-haiku-5-5, t4-2=grok-4.7 |
| r3-luna2-grok | t4-1=gpt-6-luna, t3-1=gpt-6-luna, t4-2=grok-4.7 |
| r4-haiku-luna2-grok | t3-1=claude-haiku-5-5, t4-1=gpt-6-luna, t3-2=gpt-6-luna, t4-2=grok-4.7 |
| r5-glm-haiku2 | t3-1=glm-5.3, t4-1=claude-haiku-5-5, t4-2=claude-haiku-5-5 |
| n1-muse-haiku-luna | t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=gpt-6-luna |
| n2-muse-haiku-grok | t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=grok-4.7 |
| n3-muse-luna-grok | t2b-1=muse-wonder-1.0, t4-1=gpt-6-luna, t4-2=grok-4.7 |
| n4-muse-glm-haiku | t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=claude-haiku-5-5 |
| n5-muse-glm-luna | t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=gpt-6-luna |
Fifteen sessions share the gateway. Keep to at most 2 runs at once; if a run fails with an overload or rate-limit error, wait a few minutes before the single allowed retry.

## Batch 3 (added 2026-11-11 on the owner's request)
Twelve runs: each of the top-4 ROI combos (n2-muse-haiku-grok, n4-muse-glm-haiku, n5-muse-glm-luna, r2-haiku2-grok) re-run exactly as in Batch 2 with ONE added reviewer. Added models: gpt-6.1-terra, gpt-6.1-sol, claude-sonnet-5-5. Sonnet runs under reviewer id t1b-1 (tier1b); terra under t2b-1 ONLY in rows whose base combo has no muse in t2b-1 (else use id t2-1); sol under t2-1 (or t2b-1 if t2-1 is taken by terra in the same row). Same procedure and hard limits as Batch 2. Do not reuse Batch 2 reviewer outputs: every reviewer, including the base combo members, runs fresh.

| Combo dir | Reviewer id = model |
|---|---|
| n2-terra | t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=grok-4.7, t2-1=gpt-6.1-terra |
| n2-sol | t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=grok-4.7, t2-1=gpt-6.1-sol |
| n2-sonnet | t2b-1=muse-wonder-1.0, t4-1=claude-haiku-5-5, t4-2=grok-4.7, t1b-1=claude-sonnet-5-5 |
| n4-terra | t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=claude-haiku-5-5, t2-1=gpt-6.1-terra |
| n4-sol | t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=claude-haiku-5-5, t2-1=gpt-6.1-sol |
| n4-sonnet | t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=claude-haiku-5-5, t1b-1=claude-sonnet-5-5 |
| n5-terra | t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=gpt-6-luna, t2-1=gpt-6.1-terra |
| n5-sol | t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=gpt-6-luna, t2-1=gpt-6.1-sol |
| n5-sonnet | t2b-1=muse-wonder-1.0, t3-1=glm-5.3, t4-1=gpt-6-luna, t1b-1=claude-sonnet-5-5 |
| r2-terra | t4-1=claude-haiku-5-5, t3-1=claude-haiku-5-5, t4-2=grok-4.7, t2b-1=gpt-6.1-terra |
| r2-sol | t4-1=claude-haiku-5-5, t3-1=claude-haiku-5-5, t4-2=grok-4.7, t2-1=gpt-6.1-sol |
| r2-sonnet | t4-1=claude-haiku-5-5, t3-1=claude-haiku-5-5, t4-2=grok-4.7, t1b-1=claude-sonnet-5-5 |

## Batch 3 contamination and re-run (2026-11-11)
The first batch-3 attempt (12 concurrent workers) hit gateway model-identity bleed at high concurrency: the muse-wonder-1.0 slot (t2b-1) came back observed as gpt-6.1-terra (including in workers that never request terra) and was correctly dropped by the observed-model check. By owner decision the attempt was torn down: all 12 workers stopped, and every contaminated output was quarantined in place (dirs renamed with a `-contaminated-20261111` suffix; nothing deleted).
RE-RUN RULES: waves of at most 4 workers live at once, each worker capped at 1 concurrent reviewer run. Wave order: n2 family (n2-terra, n2-sol, n2-sonnet), then n4 family, then n5 family, then r2 family. Same rows as the Batch 3 table. Before merging, if any reviewer fails the observed-model check twice, STOP that worker and report it in RESULT.md instead of merging a degraded panel; do not silently drop a base reviewer.

## Batch 3 muse outage (2026-11-11 ~22:40 UTC)
 muse-wonder-1.0 is currently misrouted at the gateway: requests return init model and billing as muse-wonder-1.0 but every assistant message is served by gpt-6.1-terra (verified with sequential zero-load probes; sol/terra/sonnet report consistently). This began between 20:14 UTC (batch-1/2 muse runs: assistant turns = muse, clean) and ~22:40 UTC. Low concurrency cannot fix it. Wave-1 workers n2-terra and n2-sol correctly stopped per the stop rule. muse-based rows are SUSPENDED until the gateway routing is fixed and a fresh probe shows assistant=muse-wonder-1.0; r2-family rows (haiku x2 + grok + added model, no muse) are unaffected and may run.

## Cooldown (owner decision 2026-11-11 22:43 UTC)
All workers stopped. Gateway cooling down for 60 minutes (until ~23:45 UTC) because of suspected account/model overload from the 12-worker attempt. At resume: re-probe muse (assistant turns must read muse-wonder-1.0, zero-load), then run the remaining batch-3 rows strictly one worker at a time, 1 concurrent reviewer run, wave order r2-terra, r2-sol, r2-sonnet, then (if muse is clean) n2-terra, n2-sol, n2-sonnet, n4-terra, n4-sol, n4-sonnet, n5-terra, n5-sol, n5-sonnet.

## Batch 3 glm outage (2026-11-12 ~08:25 UTC)
 glm-5.3 hit the same gateway misrouting muse had earlier: zero-load probe returned assistant turns as qwen3.8-max (init/billing say glm-5.3), with unrecognized_model on stderr. n5-terra design glm attempt1 timed out (3000s, 0 tokens) and attempt2 showed the same signature before it was killed. The serial recovery runner (/tmp/n5-finish.sh) is stopped; its 5-run queue (n5-terra design glm; n5-sol designSpec glm, design glm/luna/sol) is SUSPENDED until a fresh zero-load probe shows assistant=glm-5.3. luna and sol runs in that queue are unaffected by the glm outage and may be run separately. Haiku probe clean (assistant=claude-haiku-5-5).

## Batch 4 (2026-11-12, owner request): source.md impact study
Root cause found for sol/terra "incomplete" reports: candidates reference ./source.md but the sandbox only shipped candidate.md. source.md is now shipped next to the candidate (run-reviewer.sh patched; originals kept). Re-runs, all into combos/<name>-src/ so the original rows stay untouched:
- sol-alone: gpt-6.1-sol as sole reviewer x 3 packages (label t2-1) — measures what sol does when it can actually review.
- sonnet rows re-run WITH source.md: n2-sonnet-src, n4-sonnet-src, n5-sonnet-src, r2-sonnet-src (full 4-reviewer rows, all reviewers fresh, same ids/models as Batch 3).
- top-3 cheap combos re-run WITH source.md: r1-haiku-luna2-src (best ROI), n2-muse-haiku-grok-src (best value), n5-muse-glm-luna-src (best raw coverage).
Serial execution, 1 reviewer at a time (worker script /tmp/b4-run.sh, log /tmp/b4-run.log). Model-identity check enforced as before; if a reviewer fails it twice, stop and report that row.

## Batch 4 amendment (2026-11-12 14:42 UTC, owner decisions)
1. ALL glm runs removed from batch 4 (owner: massive delays). n4-sonnet-src and n5-sonnet-src become 3-reviewer rows (muse + haiku/luna + sonnet); the n5 top-3 re-run becomes n5-muse-luna-src (glm dropped). No glm data collected in batch 4; merges must use the reduced resolutions.
2. Parallelization raised: 10 concurrent reviewer sessions, muse capped at 4 (muse stream -P4, other stream -P6; verified 10 timeout wrappers, 4 muse). The in-flight glm run was killed mid-flight (n4-sonnet-src designSpec t3-1, attempt1 partial only).
Completion markers: MUSE_STREAM_DONE in /tmp/b4-par-muse.log, OTHER_STREAM_DONE in /tmp/b4-par-other.log, ALLDONE_NOGLM_PAR in /tmp/b4-par-done.log.

## Quarantine: pre-source.md luna data (owner order 2026-11-12 15:16 UTC)
ALL luna reviewer outputs from runs made WITHOUT source.md (batches 1-3 combos, pilot t4/t2 slots where luna ran) are MOVED to EVAL/quarantine-pre-src-luna/ (428 reviewer files + the 9 luna-bearing combo rows' merged/ledger/resolution sets). Rationale: luna refused to review without source.md (25/25 empty on affected packages), so those runs measure a harness gap, not the model. Future reports must use ONLY luna runs from -src rows. PILOT-REPORT.md and the batch 1-3 sections of COMBO-REPORT.md predate this order and still contain luna-affected numbers; treat their luna-related statements as superseded. Note for scoring: batch 1-3 blind scores in arms/scoring/combos/ for luna-bearing rows reflect the contaminated merges and are retained for audit only.

## Batch 5 (owner request 2026-11-12 15:21 UTC): best-ROI shortlist
Owner's 7 target combinations vs coverage:
- terra+muse+haiku  -> NEW row b4-terra-muse-haiku (t2-1 terra, t2b-1 muse, t4-1 haiku)
- terra+luna+muse   -> NEW row b4-terra-luna-muse (t2-1, t2b-1, t4-1 luna)
- muse+2xluna       -> NEW row b4-muse-luna2 (t2b-1 muse, t4-1 + t3-1 luna as two independent runs)
- haiku+2xluna      -> COVERED by r1-haiku-luna2-src (in flight, batch 4)
- sonnet+2xluna     -> NEW row b4-sonnet-luna2 (t1b-1 sonnet, t4-1 + t3-1 luna)
- sonnet+terra      -> NEW row b4-sonnet-terra (t1b-1, t2-1)
- sonnet+luna+muse  -> COVERED by n5-sonnet-src (in flight; glm dropped = exactly sonnet+luna+muse)
5 new rows = 42 reviewer runs, queued to start automatically when batch 4's parallel streams finish (same 10-concurrent/4-muse caps). Logs: /tmp/b5-par-muse.log, /tmp/b5-par-other.log; markers MUSE5_DONE / OTHER5_DONE.

## Muse misroute recurrence (2026-11-12 ~15:46 UTC)
b4-muse-luna2 alias+design muse runs came back served as gpt-6.1-terra (both attempts; zero-load probe confirms misroute active again). The other 12 b5 muse runs were clean. Those 2 runs are quarantined-in-place (marked model_ok=false; do not merge) and scheduled for retry after a ~75-min cooldown (~17:00 UTC): probe muse (assistant must read muse-wonder-1.0), then rerun the 2 runs, then merge b4-muse-luna2.

## Batch 6 (owner request 2026-11-12 ~17:57 UTC): muse-ember-1.0 replacement study
muse-wonder-1.0 is exhausted for the week (gateway serves it as terra/sonnet). muse-ember-1.0 verified clean (probe + full review run via fallback smoke: assistant=muse-ember-1.0, valid findings block). Owner is adding it to the model list as Tier 04 Model 02.
Re-run the TOP-5 muse-wonder rows with muse-ember-1.0 in the muse slot (all other reviewers fresh too, source.md shipped, same ids):
1. r2-sonnet-ember:    t4-1 haiku, t3-1 haiku, t4-2 grok, t1b-1 sonnet + t2b-1 muse-ember-1.0  (orig r2-sonnet-src 4/14, 4/8)
2. n4-sonnet-ember:    t2b-1 muse-ember, t4-1 haiku, t1b-1 sonnet                              (orig n4-sonnet-src 4/14, 2/8)
3. terra-muse-haiku-ember: t2-1 terra, t2b-1 muse-ember, t4-1 haiku                            (orig 3/14, 2/8, 0 wblk)
4. terra-luna-muse-ember:  t2-1 terra, t2b-1 muse-ember, t4-1 luna                             (orig 3/14, 2/8, best ROI)
5. n5-sonnet-ember:    t2b-1 muse-ember, t4-1 luna, t1b-1 sonnet                               (orig n5-sonnet-src 3/14, 1/8)
Plus complete b4-muse-luna2 (muse+2xluna) with muse-ember as its muse slot: b4-muse-ember-luna2 (the pending 7th shortlist slot).
Fallback ladder active in run-reviewer.sh (muse-wonder<->muse-ember, glm->haiku, haiku<->luna, grok->haiku, sonnet->haiku, terra/sol->luna).

## Fallback ladder v2 (owner order 2026-11-12 18:10 UTC)
Replaced the ad-hoc fallback map with tier-ordered succession: each model falls back to the NEXT model in its own tier (02->03->04...), then to the FIRST model of the next tier (T3->T4, T2->T2b, T1->T2; T4 wraps to T2). Full chain in run-reviewer.sh FALLBACK map. Notes: muse-spark-1.3 and muse-wonder-full-1.0 currently misroute on the gateway (spark->sol, wonder-full->sonnet) — they remain in the ladder as ordered, but the identity check will skip them and continue to the next rung if they misroute in a fallback. Opus listed only as a guard (T1a); it is never auto-selected by eval rows (Tier 0/Opus usage is owner-only per the original constraints).

## Batch 7 (2026-11-12 19:38 UTC, owner order): ember/luna/haiku/grok combos
Six rows x 3 packages (54 runs), streams ember -P4 / other -P6, source.md shipped, fallback ladder v2 active. Rows: e1-grok-ember-luna; e2-ember-luna2-rep (same multiset as b4-muse-ember-luna2, fresh replication); e3-ember2-luna; e4-haiku2-ember; e5-haiku-ember-luna; e6-haiku-ember2. Second same-model reviewer uses id t3-1. Launcher /tmp/b7-launch.sh, logs /tmp/b7-ember.log, /tmp/b7-other.log.
Batch 7 amendment (2026-11-12 19:42 UTC, owner order): e4-haiku2-ember CANCELLED. Two in-flight haiku runs on designSpec (t4-1, t3-1) killed at ~19:41; one ember run (alias t2b-1) had already finished. Remaining e4 jobs skip via /tmp/cancel-e4-haiku2-ember. Partial e4 files are kept under reviews/combos/e4-haiku2-ember/ (audit only, no merge/score). Row dropped from batch 7 analysis: 5 rows remain.

## Batch 8 (2026-11-12 20:37 UTC, owner order): replicate study, 9 combos x 4 replicates x 3 packages
Reason: batch-7 rows were single runs and indistinguishable; the doubling claim was retracted (attribution flaw + no power). Owner ordered 4x runs of: ember+2luna (g1), sonnet+ember (g2), sonnet+luna+ember (g3), haiku+ember+terra (g4), 2ember+luna (g5), 2luna+2ember (g6), haiku+2luna (g7), ember+terra (g8). WORKER ADDITION (flagged): g9 ember+luna 1x baseline, needed so the table can show 2x-vs-1x impact of luna and ember. Rows named g?-<combo>-r1..r4. Prior matching rows to fold into the final table: ember+2luna = b4-muse-ember-luna2, e2-ember-luna2-rep; sonnet+luna+ember = n5-sonnet-ember; haiku+ember+terra = terra-muse-haiku-ember; 2ember+luna = e3-ember2-luna; haiku+2luna = r1-haiku-luna2-src. Runs: 36 rows x 3 pkgs; launcher /tmp/b8-launch.sh; logs /tmp/b8-ember.log /tmp/b8-other.log. Ember -P4, other -P6.

## Batch 9 (2026-11-12 22:16 UTC, owner order): h1 haiku+2luna+2ember, h2 sonnet+2luna+2ember, 4 replicates x 3 packages = 120 runs (ember 48, luna 48, haiku 12, sonnet 12). Rows h1-haiku-luna2-ember2-r1..r4, h2-sonnet-luna2-ember2-r1..r4. Reviewer ids: haiku t2-1, sonnet t1b-1, luna t4-1/t4-2, ember t2b-1/t3-1 (ids carry only tier alias metadata; models passed explicitly). Launcher /tmp/b9-launch.sh; logs /tmp/b9-ember.log /tmp/b9-other.log. After scoring: determine untried combinations worth testing.
Batch 9 incident (2026-11-12 22:17-22:19 UTC): the `claude` binary was briefly missing ("native binary not installed", exit 127). Fallback ladder v2 is CYCLIC, so instant failures spun it round the cycle (69 FALLBACK lines in 3 s) and landed two ember reviewer runs on other models: h1-r1 alias t2b-1 ended on claude-haiku-5-5 (a real haiku review labelled as an ember slot), h2-r1 design t3-1 ended on Qwen3.8-max (an excluded model; ran 42 min until killed). Both would have passed model_ok because expected_model is overwritten by the fallback model. Handling: runs quarantined in place (quarantine-haiku-fallback-20261112, quarantine-qwen-fallback-20261112), both ember slots re-run with NOFALLBACK=1 (model_ok true, observed muse-ember-1.0), h1-r1 alias merge redone (old merge kept as TASK-WF-makeTheAliasOnly...quarantine-haiku-fallback-20261112). Harness fix in tools/run-reviewer.sh: ladder now never revisits a model, skips EXCLUDE_MODELS (default glm-5.3 Qwen3.8-max), and honours NOFALLBACK=1. Earlier batches checked: no fallback logs in batches 7 and 8; batch 6 reported 0 fallback triggers. An audit now also checks each reviewer's expected_model against the intended model.

## Batch 10 (2026-11-13 00:28 UTC, owner order): untried-combination tests 2 and 3
i1-grok-sonnet-r1..r4 (grok + sonnet) and i2-haiku-sonnet-r1..r4 (haiku + sonnet), 3 packages each = 48 runs, one xargs stream -P10 (no ember), fallback ladder v3 (no revisit, glm/Qwen excluded). Questions: is grok+sonnet the active core of r2-sonnet-src (4/14, 4/8)? does haiku+sonnet replicate n4-sonnet-src (haiku+sonnet+wonder, 4/14-2/8) without wonder? Launcher /tmp/b10-launch.sh, log /tmp/b10.log, merge /tmp/merge-b10.sh.

## Batch 10 DROPPED (2026-11-13 01:09 UTC, owner order)
Owner: "leave those results out of the equation, we're done testing, we're going to decide and run with it." Batch 10 (i1-grok-sonnet-r1..r4, i2-haiku-sonnet-r1..r4; 48 runs) is excluded from all tables and recommendations. 8 outage-hit runs (claude binary update at 00:35) were identified in /tmp/b10-fix.txt and were NOT re-run, quarantined, merged or scored; raw reviewer outputs are left in place untouched (audit only). Heartbeat cron for batch 10 retired. Testing is closed; remaining work = integrity audit of past runs (6 parallel read-only audit agents, outputs /tmp/audit-A..F), final table, and recommendation.
CORRECTION (2026-11-13 01:14 UTC) to the "Batch 10 DROPPED" entry: it said the 8 outage-hit runs were not moved. That is wrong. The quarantine+re-run command that the owner interrupted at ~01:07 had already started: at 01:02:34 it moved the 8 runs' files into reviews/combos/<row>/quarantine-outage-20261113/ (5 row dirs) and launched NOFALLBACK reruns, which left zero-byte attempt1.json/err files (e.g. i1-grok-sonnet-r3 design t1b-1, t4-2) and were then killed by the interrupt (no run-reviewer process is alive at 01:13). Net state: those 8 slots have quarantined originals plus empty rerun stubs and no final report; the other 40 batch-10 runs are untouched. Batch 10 is excluded from all results either way; the files are left as they are, for audit only.
