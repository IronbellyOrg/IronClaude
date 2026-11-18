# Scope slice 03: E2 original study, reports and tooling

**Status:** Complete
**Date:** 2026-11-14
**Scope:** `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` top-level reports/docs, `tools/`, study inputs layout, at tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` of `origin/ironbelly/eval-tasklist-review-panel` (run-1 commit `4a22d74213f93837d00c2c314075dd967b9a98e3` is its ancestor). Read via `git show` / `git ls-tree` only.
**Citation form:** `E2@6c09843:<path>:<lines>`; HEAD = this worktree (branch ironbelly/shadow-runs). `A1` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`. Line numbers are `git show 6c09843:<path> | cat -n` lines.

---

## 1. Study inputs layout (git ls-tree -r at tip 6c09843; no raw file read)

Total files under A1: **9,312** (`git ls-tree -r --name-only 6c0984326cbb8fb06c4a36065de58b171d3f8175 -- A1/ | wc -l`).
Siblings under `.dev/eval-workspaces/tasklist-review-panel/` (other slices; only listed, not opened): `20261111-a1/` (this slice), `20261113-collab/`, `HANDOFF-review-panel-unification-run2.md`, `HANDOFF-review-panel-unification.md`, `HANDOFF-run1-vs-run2.md`, `handoff-notes/`.

| Dir under A1 | Files | Content (from ls-tree names) |
|---|---|---|
| top-level files | 3 | COMBO-REPORT.md (506 lines), PILOT-REPORT.md (83), manifest.md (16) |
| `TASK-WF-design-20261108-041415/` | 2,020 | 5 top files (`candidate.md`, `ground-truth-draft.json`, `ground-truth.json`, `resolution-default.json`, `resolution-live7.json`) + `reviews/` 1,959 + `reviews-failed-launch-1/` 56 |
| `TASK-WF-designSpec-20261107-075614/` | 2,125 | same 5 top files + `reviews/` 2,071 + `reviews-failed-launch-1/` 49 |
| `TASK-WF-makeTheAliasOnly-20261105-051649/` | 2,090 | same 5 top files + `reviews/` 2,036 + `reviews-failed-launch-1/` 49 |
| `arms/` | 1,297 | `arms/A`, `arms/B`, `arms/C` = 12 files each (ledger.json, merge-stdout.txt, merged-1.md, resolution.json per pkg); `arms/scoring/` = 1,261 (3 pkg dirs x 7 files + `arms/scoring/combos/` 1,240) |
| `combos/` | 1,160 | 95 combo row dirs + `SPEC.md` (152 lines, ops log); typical row = 12 files (4 per pkg x 3); c2-haiku-grok has 10 |
| `analysis/` | 141 | top-level scripts/outputs + `analysis/allsets/` 29, `analysis/audits/` 46, `analysis/issue-table/` 28 |
| `quarantine-pre-src-luna/` | 417 | pre-source.md luna reviewer files and merge sets; COMBO-REPORT:107 says "428 reviewer files, 10 combo-row merge sets": tree has 417 files in total (not directly comparable; reviewer-file vs total-file basis [UNVERIFIED]) |
| `tools/` | 58 | `run-reviewer.sh` (8,089 B), `run-reviewer.sh.bad-launch` (4,302 B), `run-reviewer.sh.unpassable-ac` (4,352 B), `tools/tmp-scripts/` 55 files |
| `probe/` | 1 | `probe/probe.json` (Stage 0 model identity probe) |

Counts by kind over the whole A1 tree (own `ls-tree | grep -c`): `score.json` 318 (2 of them name `invalid`); `meta.json` 1,263; `cost.json` 1,263; `*.err` 1,690; `*.catfix.md` 20; `merged-1.md` 339; `merged-anon.md` 319; `label-key.json` 309; `arm-key.json` 3; `RESULT.md` 29; paths containing `contaminated` 592; `superseded` 378; `quarantine-outage` 91; `stale-r1` 8; `judge.json` 0; `*.attempt<N>.json` 0 (raw transcripts excluded).
Per-package `reviews/` layout: `reviews/combos/` = bulk (1,919 of 1,959 in `design`); pilot-arm reviewer files `t1b-1, t2-1, t2b-1, t3-1, t3-2, t4-1` with `*.md`, `*.attempt<N>.md`, `*.attempt<N>.err`, `*.cost.json`, `*.meta.json`, `*.md.catfix.md`; `live7-t3-1/` (5 files).
Raw transcripts NOT committed: `A1/analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md:2` = "About 1.48 GB of raw `claude -p` JSON transcripts ... every `*.attempt<N>.json` ... and every `judge.json` ..., 2,916 files, still on the original machine". :3 lists what IS committed (reviewer reports, meta/cost, merge outputs, blind scores, harness scripts `tools/`, COMBO-REPORT.md, `combos/SPEC.md`, PILOT-REPORT.md, analysis scripts, "six audit outputs"). :4 "Start with COMBO-REPORT.md, section FINAL RESULTS AND DECISION (2026-11-13) near the end: it supersedes every earlier table".
- Consequence for a central panel: judge sessions and reviewer sessions are NOT re-auditable from the commit; only derived data is. The 6 audits (analysis/audits/) are the only re-check evidence.

## 2. manifest.md (E2@6c09843:A1/manifest.md, 16 lines)

- :3-6 EVAL dir; UTC date 2026-11-11; worktree branch `ironbelly/eval-tasklist-review-panel` "(local, never pushed)" [stale: the branch exists on origin at tip 6c09843 (`git branch -r --contains`)]; HEAD sha == origin/master sha == `ec259f1b718ccdb9f08bba0237bfa47b2b7601a2`.
- :8 Precondition 1 "HEAD == origin/master: YES".
- :9 `superclaude review --help` works; `T2bModel01=gpt-6.1-terra`; `@live7` resolves 7 reviewers (run-id probe).
- :10 Reviewer sandbox `/tmp/evalsb/repo` = `git archive` of HEAD minus `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research` (so reviewers cannot read implement history or ground truth). Own throwaway git repo.
- :11 Dispatch (Stage 0, probe/probe.json): Bash `claude -p --model <raw gateway model id>`; observed model = assistant message.model in JSON output. "Tier aliases serve only the first model of a tier, so they are NOT used."
- :13-16 GT sha256 (exact): designSpec `3e56551dc0046c9ff3f2e3f49fb2ccb82da8c63a8a781dbe13b0631ba8cb47e4`; makeTheAliasOnly `79e3205775deace4a9b02810f16abecca0fe3c11e256e8d79b6893df45f5eb1e`; design `e3585b8e6bf11241cdaafbf2faf5e52fd4c6dfed2176b1e7269b6a54c97d5a3c`.
- Destination note: the whole eval used raw model ids on Bash `claude -p`, not product tier aliases. This is the E2 equivalent of E1's model-combination experiment dispatch; harness (`run-reviewer.sh`) is the reusable part, product code was NOT what ran the panels (see section 8).

## 3. PILOT-REPORT.md (E2@6c09843:A1/PILOT-REPORT.md, 83 lines): arms A/B/C on 3 packages

**Setup (:7-14)**
- Packages: designSpec-20261107-075614 = 10 GT defects, 5 blocking-in-implement; makeTheAliasOnly-20261105-051649 = 4 GT, 3 blocking; design-20261108-041415 = 2 GT, 0 blocking (control). (:7)
- Arm A = Tier 1b reviewer alone (claude-sonnet-5-5); Arm B = @default panel minus Qwen3.8-max slots; Arm C = @live7 panel minus Qwen3.8-max slots. (:8-10)
- Qwen3.8-max disqualified by owner after all 3 slots timed out (attempts=2, 0 output tokens, meta wall 3000 s each; 9000 s wasted). B and C deviate from resolved panels. (:12)
- Category-label defect: reports before fix used `unpassable-ac`; merges used `.catfix.md` copies with label changed to `unpassable-check` (9 files; originals unedited). Affected: designSpec t4-1; alias t1b-1, t2b-1, t3-2, t4-1, t4-2; design t1b-1, t3-1, t3-2. (:13) (9 listed = 1+5+3 ok.)
- Scoring: 9 blind Opus subagents (one per pkg x label); X/Y/Z random labels (`arm-key.json`); reviewer ids and file paths anonymized; score.json = GT coverage, blocking coverage, wrong blockers (blocking ledger rows with no GT correspondence). (:14)

**Per-arm results (:18-40)**
| Pkg | Arm | Verdict | GT any | GT blocking | Ledger rows (blocking) | Wrong blk | Wall s | Out tokens |
|---|---|---|---|---|---|---|---|---|
| designSpec | A | PASS | 1/10 (GT3) | 0 | 4 (0) | 0 | 260 | 34,744 |
| designSpec | B | PASS | 1/10 (GT3) | 0 | 9 (0) | 0 | 1,197 | 90,735 |
| designSpec | C | FAIL | 2/10 (GT3, GT7) | 0 | 13 (1) | 1 | 2,355 | 196,357 |
| alias | A | PASS | 0/4 | 0 | 4 (0) | 0 | 198 | 26,694 |
| alias | B | FAIL | 0/4 | 0 | 7 (1) | 1 | 1,874 | 135,517 |
| alias | C | FAIL | 0/4 | 0 | 6 (2) | 2 | 2,785 | 200,371 |
| design (ctl) | A | FAIL | 1/2 (GT1) | GT1 | 1 (1) | 0 | 244 | 31,660 |
| design (ctl) | B | FAIL | 2/2 | GT1, GT2 | 2 (1) | 0 | 2,547 | 167,953 |
| design (ctl) | C | FAIL | 2/2 | GT1, GT2 | 2 (1) | 0 | 3,367 | 207,368 |

**Totals (:46-50)**: A 2/16 caught, 0/8 blocking recall (defect-rich), 702 s, 93,098 tokens, 2.15 catches/100k, 0 wrong blockers; B 3/16, 0/8, 5,618 s, 394,305 tok, 0.76, 1 wb; C 4/16, 0/8, 8,507 s, 604,096 tok, 0.66, 3 wb. Judge cost 9 Opus subagents, 1,034,575 output tokens, ~139 s summed wall (:52).
**Fixed decision rule (:56)**: "Recommend a panel only if on defect-rich packages it catches >= 2x arm A's defects at any severity AND averages <= 1 wrong blocker per plan on controls." Result: A=1, B=1, C=2 defect-rich catches; only C passes, "exactly" and "marginally" (:58-61). Paired: B vs A sign test p=0.5, C vs A p=0.25 (:64-65). B costs 4.2x A's tokens, C 6.5x (:67).
**Honest read (:71)**: all three arms 0/8 blocking recall; single-reviewer A PASSED both defect-rich packages ("worst observed outcome for a gate whose job is to fail bad plans"). Bigger panels helped only on non-blocking defects (4/4 vs 2/4 on control; GT7 on designSpec).
**Stated limits (:75-79)**: n=3; single Opus judge per (pkg,label), judge variance unmeasured; Qwen removal; `unpassable-ac` bug + c1 designSpec haiku block missing `## Findings block` heading (15 findings ignored; reviewer-side format failure; affected a combo run not the pilot arms); GT structural bias: a true novel defect scores as wrong blocker if blocking (:79).
**Next (:83)**: "6 remaining packages are staged for the same pipeline only after approval"; 15 owner-ordered combo runs (5 batch-1 + 10 batch-2) running in parallel workers.
- [RECOMPUTED by this slice from committed `arms/scoring/<pkg>/<label>/score.json` + `arm-key.json` (jq): all 9 (arm, package) cells match the PILOT table for `gt_covered_any` count, `gt_covered_blocking` count, `ledger_rows_total`, `ledger_rows_blocking`, `wrong_blockers` (e.g. designSpec key A=Y B=X C=Z: A 1/0/4/0/0, B 1/0/9/0/0, C 2/0/13/1/1; alias A 0/0/4/0/0, B 0/0/7/1/1, C 0/0/6/2/2; design A 1/1/1/1/0, B 2/2/2/1/0, C 2/2/2/1/0).] Control package shows `gt_covered_blocking` = GT1/GT2 although neither GT has `blocking_in_implement` (confirms H9: judge-blocking = matched by a blocking-flagged row).
- Later superseded: the pilot arm A-vs-B/C conclusion ran WITHOUT `source.md` in the reviewer sandbox (see COMBO-REPORT:132/373 and section 4); all arm A/B/C numbers are therefore pre-source.md-era, never re-run (UNVERIFIED that no re-run exists; COMBO-REPORT:148 says "arm A numbers came from the separately-run pilot judges, all clean").

## 4. COMBO-REPORT.md (E2@6c09843:A1/COMBO-REPORT.md, 506 lines): chronology of batches, retractions, final decision

Reading rule: the file is an append-only log with retractions; `:289` says the FINAL section "supersedes every earlier table, ranking and recommendation". Treat :1-288 as history. Items below keep each claim with its later status.

### 4.1 Batches 1-2 (:5-82), 15 combos x 3 pkgs, pre-source.md era
- :7 15 owner-ordered Tier 3/4 combos, `tools/run-reviewer.sh`, raw ids, `claude -p`, 3000 s timeout, 1 rerun, merged with `superclaude review merge`. Qwen3.8-max excluded.
- :9 Defect-rich = designSpec (10 GT, 5 blocking) + alias (4 GT, 3 blocking) = 14 GT any / 8 GT blocking; design = control (2 GT, 0 blocking).
- :10 Scoring: 45 merged reports anonymized (R1..Rn, paths redacted), one Opus judge per (combo, pkg).
- :11 Known harness event: `unpassable-ac` label; reviewer-side format failures (c1 haiku designSpec block missing heading, 15 findings dropped; r2 haiku alias block with >300-char claim dropped).
- :17-43 Master table. Anchors: best any-catch 4/14 (n5-muse-glm-luna, :20); best blocking 2/8 (n4-muse-glm-haiku :18, r1-haiku-luna2 :21, and 2 B3 rows); worst r4-haiku-luna2-grok 0/14 (:43). Biggest spend r5-glm-haiku2 782,529 tokens / 8,346 s (:24). Cheapest r1-haiku-luna2 188,952 tok / 1,146 s (:21) (c1 927 s, :42).
- :59 "No combo beats arm A's efficiency" (every combo 0-1.06 catches per 100k vs A 2.15, B 0.76, C 0.66).
- :60 "Blocking recall is bad everywhere": best 2/8; 8 of 14 combos caught 0 or 1; 5 combos PASS designSpec (5 blocking GT items).
- :61 luna: fast and thin (30-295 s, 1.4k-14k tokens); :62 haiku in 11 combos, grok slow (600-980 s, 41-63k tokens), muse-wonder-1.0 149-186 s, ~16-17k tokens.
- :63 Wrong blockers 2-3 per combo on defect-rich; GT penalizes novel-but-real catches.
- :67 Verdict (later superseded): "no configuration, cheap or expensive, reached even 30% blocking recall". Retracted in spirit by :132 then by :148.
- :53/:54 glm-5.3 "added cost without catches in every combo it appeared in" (c5, n4, n5: 408-615k tokens). Owner later excluded glm (:110 "glm excluded per owner (delays)").
- :72-75 Stated limits: n=3; one judge; unpassable-ac dropped findings (catfix restores label but not already-skipped findings).

### 4.2 Batch 3 addendum (:84-102) re-run top-4 combos plus one added reviewer (terra / sol / sonnet), 12 rows
- :86 First attempt (12 concurrent workers) torn down for **gateway model-identity bleed (muse served as terra)**; quarantined as `*-contaminated-20261111` (592 paths carry `contaminated` in tree). After 60-minute cooldown and zero-load muse probe, rows re-run serially. gpt-6.1-terra returned thin "incomplete" reports (407-598 tokens, 0 findings, citing a missing input) though model check passed.
- :88-99 per-row results (r2-terra 3/14 + 2/8 + 3 wb at 487,442 tok; r2-sol 1/14 + 1/8; r2-sonnet 2/14 + 2/8 + 1 wb; n2-terra 2/14 + 2/8; n2-sol 2/14 + 1/8; n2-sonnet 2/14 + 1/8; n4-terra 1/14; n4-sol 2/14 + 0/8 + 4 wb (9,552 s); n4-sonnet 3/14 + 1/8; n5-sonnet 3/14 + 1/8; n5-terra, n5-sol 2/14 each).
- :101 B3 summary: sonnet the only addition that contributed findings; terra and sol "pure cost" (0 findings every package every row); no B3 row beat its batch-2 base. Operational: gateway misrouting hit muse (22:40 UTC Nov 11) and glm (08:25 UTC Nov 12) under load; recovered after ~60-90 min.
- :102 Recommendation (superseded): n5-sonnet 4-reviewer panel.

### 4.3 CORRECTION A (:104-107, 2026-11-12 15:20 UTC): parser bug + luna quarantine
- :105 PARSER BUG: blocking counts used grep `"blocking":true` (no space); several models emit `"blocking": true`. "All per-model blocking numbers stated in earlier sections (including 'grok 0 blocking in 42 runs' and the batch-4 interim table claiming only gpt models block) are WRONG." Corrected source.md-run totals (space-tolerant, 84 valid runs): muse 21 blocking/18 runs, haiku 19/16, grok 19/15, sonnet 2/11, luna 23/21, terra 8/3, sol 6/3.
- :107 LUNA QUARANTINE (owner order): pre-source.md luna data to `EVAL/quarantine-pre-src-luna/` "(428 reviewer files, 10 combo-row merge sets)"; luna statements in PILOT-REPORT and batch 1-3 superseded.
- Lesson: an ad hoc grep over structured model output silently produced wrong headline numbers; the parser is the defect. Destination: parse findings only through one schema validator (reflect: `merged-verdict.yaml`/kernel parse).

### 4.4 Batches 4/5 (:109-148): source.md shipped, 17 rows
- :110 "same reviewer harness (now ships source.md beside candidate.md)". "b4-muse-luna2 pending a muse retry (gateway misroute recurrence; 2 runs quarantined)".
- :114-130 table: n2-sonnet-src 8/14, 5/8 (later RETRACTED :146-148), r2-sonnet-src 4/14, 4/8 (later 3 real, :291), n4-sonnet-src 4/14 + 2/8 311,505 tok, b4-sonnet-luna2 4/14 + 0/8 139,660 tok, b4-terra-luna-muse 3/14 + 2/8 at 68,221 tok / 832 s (4.4 catches/100k, :137), terra-alone-src 1/14 at 7,241 tok / 182 s, sol-alone-src 1/14 at 11,588 tok / 410 s.
- :132 "source.md changed the picture completely ... The earlier '0/8 blocking recall everywhere' conclusion was an artifact of the missing source document". (RETRACTED partly at :148.)
- :146-148 CORRECTION (2026-11-12 16:55 UTC): designSpec judge for n2-sonnet-src "died with an Opus API error but left a fabricated-looking score.json (8 rows/6 blocking/8-of-10 GT)"; re-judged: 2 any (GT3, GT7), 0 blocking. "All 48 -src judge runs audited: this was the only failure". Corrected n2-sonnet-src 2/14, 0/8, 1 wb. "'8-of-10'/'source.md fixed the panels' headline RETRACTED". Score kept as `*.invalid-apierror` (2 `invalid` paths in tree).
- Lesson: a judge that fails mid-run can leave a plausible score file; the scorer must validate completion marker, not just presence of score.json.

### 4.5 Batch 6 (:150-174) muse-ember-1.0 replacement (muse-wonder-1.0 hit weekly limit), 6 rows
- :151 all 60 runs model_ok=true, zero fallback triggers, 0 judge failures.
- :155-160 ember rows: r2-sonnet-ember 2/14, 1/8; n4-sonnet-ember 0/14; terra-muse-haiku-ember 2/14; terra-luna-muse-ember 2/14; n5-sonnet-ember 3/14; b4-muse-ember-luna2 2/14, 1/8 at 63,211 tok.
- :163-167 findings "ember is weaker than wonder" and "ember shifts toward precision on clean plans" (control 2/2 both blocking, 0 wb).
- :170-174 CORRECTION (2026-11-12 19:05 UTC): "r2 never contained muse" (r2 = haiku x2 + grok + sonnet from meta.json); batch 6 added ember as a 5th reviewer by mistake; "r2-sonnet-src (muse-wonder version)" wrong. The comparison is evidence of run-to-run variance (n=1), not ember weakness; ember-weakness claim marked UNVERIFIED (:172).
- Lesson: row naming (c/r/n/b4/e/g/h/j prefixes) hid composition; composition must be read from `meta.json`, never inferred from row name.

### 4.6 Batch 7 (:176-200), ember / luna / haiku / grok, 5 rows (e4 cancelled by owner 19:41)
- :177 45 runs, model_ok, 15 merges rc=0, 15 blind judges, API-error audit bad=0. Ember -P4, others -P6.
- :181-185 e1 2/14 1/8 4 wb 240,961 tok 4,401 s; e2 2/14 1/8 2 wb 68,445 tok 710 s; e3 2/14 1/8 3 wb 76,026 tok; e5 2/14 1/8 2 wb 264,641 tok; e6 2/14 1/8 2 wb 197,084 tok.
- :188 "All five rows tie at 2/14 any, 1/8 blocking". :191 replication e2 vs b4-muse-ember-luna2: totals replicate, "which defects are caught is not" stable.
- :192-193 Doubling analysis ("second run adds nothing"; haiku overlap 8 of 8; per-reviewer yields ember 0.65 defects/run 0.62 wb/run; luna 0.30/0.75; haiku 1.35/0.65; grok 1.19/1.00).
- :195-200 CORRECTION (2026-11-12 20:30 UTC), RETRACTED: attribution flaw (`analysis/attrib.py` credits every reviewer on the merged ledger row, not the judge-cited ones) and no power; independent keyword check (control package GT2, 83 src-era runs): grok 7/8, muse-wonder 8/9, terra 4/6, sonnet 6/9, luna 13/22 (59%), haiku 4/13 (31%), ember 4/13 (31%). "Single runs are coin flips"; "do not rank rows on 1-defect differences".
- Lesson: single-run row ranking is noise; any central panel decision needs replicates, per-reviewer yield measured against judge-cited reviewers.

### 4.7 Batch 8 + FINAL TABLE (:202-244), replicate study 8 combos x 4 reps (+1x baseline)
- :203 300 reviewer runs, 108 merges rc=0, 108 blind judges, API-error audit bad=0; prior matching rows folded in.
- :206-220 means table: ember+luna (1x) 2.2/14, 0.5 blk, 52,398 tok, control 0.00; ember+2luna 1.8/14, 63,644 tok, control 0.83 (n=6); 2ember+luna 1.6/14; 2luna+2ember 1.8/14, **4.8 wrong blockers**; ember+terra 0.5/14, 37,255 tok; sonnet+ember 2.5/14, 0.2 wb, 142,967 tok; sonnet+luna+ember 2.2/14; haiku+ember+terra 2.0/14; haiku+2luna 2.2/14, 1.4 blk, 191,018 tok.
- :222-229 doubling-impact table (each "within noise" except flagged ones; later audited: only "second luna raises control found +0.83" survives, :298).
- :231-235 independent proxy: luna 1x panels 1/4 raise control GT2, 2x panels 5/6; ember 2/4 vs 3/5.
- :243 efficiency: ember+luna 4.2 catches/100k; ember+2luna 2.8; sonnet+ember 1.7.
- :244 "nothing found beats ~2.2/14 except sonnet + ember at 2.5".

### 4.8 Batch 9 (:246-270), haiku/sonnet + 2x luna + 2x ember, 8 rows x 3 pkgs = 120 runs
- :247 24 merges, 24 blind judges, 20 judges first failed rc=127 because the `claude` binary was replaced at 23:05 and re-ran.
- **INCIDENT (:247)**: during the 22:17-22:19 `claude` binary replacement the cyclic fallback ladder "spun 69 steps in 3 s", putting one "ember" slot on claude-haiku-5-5 (h1-r1 alias t2b-1) and one on Qwen3.8-max (h2-r1 design t3-1, ran 42 min until killed). "Both would have passed the model_ok check (expected_model is overwritten on fallback)". Fixed: `run-reviewer.sh` never revisits a model, never uses glm/Qwen3.8-max, honours `NOFALLBACK=1`.
- :251-257 table: g6 1.8/14 4.8 wb; h1 haiku+2luna+2ember 2.2/14, 1.8 blk (judge-blocking), 246,213 tok; h2 sonnet+2luna+2ember 2.2/14, 0.8 blk, 189,325 tok.
- :261-265 add-one-reviewer effect table; :268 adding haiku: blocking 0.5 -> 1.8/8 (later 1.00 real, :291).

### 4.9 Untried-combo analysis (:272-287), 71 scored valid rows, 32 distinct sets
- :274 Ceiling: "2/14 in 43 of 71 rows, 3/14 in 12, 4/14 in 4, never above 4"; designSpec GT3 caught in 63 rows, GT7 in 50; designSpec GT1, GT2, GT10 and alias GT4 never caught by any valid row.
- :275 Model presence effects (confounded): grok 2.62 vs 2.00 found; wonder 2.75 vs 1.98 (n=8); sonnet 2.43 vs 1.92 found, wb 1.95 vs 2.68; haiku 2.26 vs 1.98; ember 1.88 vs 2.55; terra 1.64 vs 2.18.
- :278-284 candidate next tests (batch 10: grok+sonnet, haiku+sonnet) later DROPPED by owner (:290).
- :287 "Non-combo lever: the five defects no valid row has ever caught ... point at the review brief, the packages or the ground truth, which is outside this study."

### 4.10 FINAL RESULTS AND DECISION (:289-373, 2026-11-13) six audits
Audits outputs under `A1/analysis/audits/` (46 files); report summary:
1. **BLOCKING DEFINITION (audit F, :291)**: judge `gt_covered_blocking` = defect matched by a blocking-flagged ledger row, may include defects not `blocking_in_implement`. "Over 71 rows the judge counts 65 'blocking' catches but only 38 are real blocking defects". Tables show "Real blocking /8" and "Judge-blocking". r2-sonnet-src 4/8 -> 3 real; c3-luna-grok-src 3/8 -> 1 real; haiku+2luna 1.4 -> 1.2; h1 1.75 -> 1.00; ember+2luna 1.00 -> 0.17 real ("second luna adds +0.5 blocking" reversed).
2. **MERGE DROPS FINDINGS SILENTLY (audit D, :292)**: merge keeps only well-formed finding lines: anchors > 200 chars (56), anchor2 > 200 (18), claims > 300 (14), bad severity, bad refs discarded with no error. "80 reviewer-level cases, 49 blocking findings lost"; by model luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet 0, terra 0, sol 0. Four verdicts flipped FAIL->PASS (g3-sonnet-luna-ember-r3 alias, g5-ember2-luna-r2 alias, n5-sonnet-ember control, plus total-loss merges). "83 merged rows lump unrelated findings into one row (chaining)". Stale merges: n2-terra, r2-sol merged before reports re-run; n5-sol, n5-terra merged from a report no longer in the row. [PRODUCT-CODE DEFECT CLAIM; checked in section 13]
3. **SOURCE.MD OFTEN NOT OPENED (audit C, :293, corrected :373)**: 161 -> 156 valid-era runs of 665 never referenced source.md (ember 81 of 209 = 39%, luna 49 of 222 = 22%, wonder 6 of 25, haiku 15 of 75, grok 4 of 24, sonnet 1 of 63, terra 0 of 44, sol 0 of 3). Cause "(the brief never names source.md) ... is an inference, UNVERIFIED" (:373). No run read GT, resolution files, other reviewers' reports or this report; old-era runs browsed sibling plan packages in sandbox repo (WARN, old rows only).
4. **TERRA/SOL REFUSALS STILL OCCUR (audit B, :294)**: 51 reports say incomplete (16 empty terra reviews in valid-era rows) even with source.md shipped. luna anchor fidelity 91.4% verbatim vs 98-100% others.
5. **MODEL IDENTITY (audit A, :295)**: 2 b4-muse-luna2 t2b-1 "wonder" runs served terra (row quarantined); no other mismatches; no fallback logs before batch 9/10 incident; grok reports gateway id `grok-4.7-build` (benign).
6. **SCORING (audit E, :296)**: 294 judge outputs clean; blind re-judge of 12 rows: 12/12 exact agreement; 19/19 recorded catches confirmed, one borderline defect (GT8) would add 1 (recall 0.95). Stale scores: r2-sonnet (3 scores predate re-merge) excluded; 10 older rows have merged reports only in quarantine and are not used.
7. **STALE TEXT (audit F, :297)** list of retracted lines still printed earlier in the file.
- :298 Statistics (Welch + permutation, n=4-6): only these survive: second luna raises control found +0.83 (p 0.004 Welch, 0.048 permutation, baseline all zeros); 2x luna + 2x ember has 2.75-3.25 more wrong blockers than every comparator (permutation p 0.005-0.03); ember + terra worse by -1.75 found (permutation p 0.029).
- :301 valid-era rows 71; row-packages scored 213; row-packages with an audit EXCLUDE flag (A,B incomplete/short,D,E,F) 69.
- :303-337 AS SCORED table (36 panels); leaders by found: grok+haiku+haiku+sonnet 4.00/14, 3.00 real blocking (n=1), 594,072 tok (:306); haiku+sonnet+wonder 4.00, 2.00 (n=1) 311,505 tok (:307); replicated: ember+sonnet 2.50 (:315), ember+luna 2.25 52,398 tok (:317), haiku+luna+luna 2.20, real blocking 1.20 (:319), ember+luna+luna 1.83, real blocking 0.17 (:331).
- :339-359 AUDIT-CLEAN table (robustness check only; drops ~1/3 of data).
- :361 Reading guide "rows with 1/1/1 are single runs (anecdotes); only rows with 4+ runs per package support any ranking."
- :363-369 **Decision**: cost champion ember+luna (52k tokens ~5 min, 2.25/14, control 0.00); "Recommended default: ember + 2x luna, 64k tokens, ~6 min elapsed, 1.83/14 found, 0.17 real blocking, control 0.83"; high-assurance haiku+2x luna 191k, 1.2/8 real blocking; best precision ember+sonnet 143k, 0.25 wb; do-not-use: ember+terra, 2x ember + 2x luna (4.75 wb), terra/sol alone, haiku+ember+terra, any 5-reviewer panel.
- :370 Single-run high scores unconfirmed (r2 family 4/14, 3 real blocking, 594k tok; haiku+sonnet+wonder 4/14, 2 real blocking, 311k).
- :371 **Pre-requisite harness fixes**: "(1) raise or truncate the 200-character anchor limit at merge, or instruct reviewers and re-validate, so findings are not silently discarded; (2) name the source.md path explicitly in the reviewer brief (161 runs never opened it); (3) keep the fallback-ladder fix and the model-identity audit in the runner. No panel catches designSpec GT1, GT2, GT10 or alias GT4, so model choice cannot lift the ceiling past ~2.5/14."
- :373 Timeline: candidates fixed 2026-11-11 17:35 and byte-identical to the sandbox copies; source.md first shipped 2026-11-12 12:59:34; first valid-era run 13:02:27; no valid-era row before that; 0 identical report bodies.

### 4.11 DECISION UPDATE (:375-383) and Batch 11 (:421-428)
- :377-383 three-way compare (analysis/three-way.py): sonnet+2luna n=1 (b4-sonnet-luna2) 4, 0, 3 wb, control 2/2 0 wb, 139,660 tok, 793 s; ember+2luna n=6 1.83; sonnet+luna+ember n=5 2.20; h2 n=4 2.25. Permutation tests p 0.54-1.0 except h2 vs ember+2luna wrong blockers 3.50 vs 1.83 p 0.073; tokens p 0.002-0.009. Reliability: sonnet 0 findings dropped, read source.md every run; ember skipped source.md in 9 of 18 runs of ember+2luna, 2 dropped; luna skipped 9 of 36, 4 dropped. Revised recommendation (sonnet + 2x luna as standard) later REJECTED.
- :421-428 **Batch 11**: sonnet+2luna replicated 5 times (j1-r1..r5), 45 runs, `NOFALLBACK=1`; 5 runs failed when the `claude` binary was replaced at 13:48:51, quarantined (`quarantine-outage-20261113`) and re-run. Per-run: b4 4,0,3,2 139,660 tok 793 s; j1-r1 2,0,2,1 148,599; j1-r2 1,0,1,2 143,674; j1-r3 3,1,1,1 151,355; j1-r4 2,1,2,1 121,787; j1-r5 2,0,2,1 129,604. Family n=6: found 2.33 (sd 0.94, range 1-4), real blocking 0.33, wrong blockers 1.83, control 1.33, tokens 139,113, elapsed 821 s; "the original 4/14 was an upward outlier (regression to the mean)". Permutations vs ember+2luna: found p=0.51, tokens/elapsed p=0.003. Control GT1 (I7: no task updates the gh-api classification table) reached 3 of 6 sonnet+2luna runs and 2 of 4 h2 runs (5/10) vs 0 of 6 ember+2luna, 0 of 5 sonnet+luna+ember (Fisher exact p ~0.012, post-hoc, exploratory). Reliability: 2 of 30 luna findings blocks dropped at merge, sonnet 0 of 15; 3 of 30 luna runs never opened source.md (all alias pkg), sonnet 0 of 15.
- :428 **Final guidance**: default = ember + 2x luna; optional quality tier sonnet + 2x luna (~+75k tokens, ~+8 min); haiku + 2x luna best measured real-blocking panel (1.2/8). "All panels sit at about 2-2.5 of 14, so the harness fixes (anchor limit, source.md path in the brief) remain the biggest lever."

### 4.12 Issue-by-panel table (:385-419) and all-sets table (:430-506)
- :386 10 parallel agents, outputs `analysis/issue-table/issue-NN.json`; independent computation `issue-table.py`: "0 mismatching cells out of 320". Panels = top-10 replicated.
- :401-417 Issue legend (B = blocking_in_implement; truncated to ~200 chars in file): B1 designSpec GT1 (Task 1 AC3 demands a provably complete inventory with no bounded method / stopping rule; 5 attempts, retry ladder end, 2 operator-review halts); B2 designSpec GT2 (Task 1 names 4 target files, AC3 says only "found for O3", scope widening); B3 designSpec GT3 (Task 9 test of L3/draft condition without defining "condition"; two word-list tests failed review); B4 designSpec GT4 (Task 8 vs Task 4 "unreadable" timeline contradiction); B5 designSpec GT5 (Task 8 exit-report field drops `draft_guard_unavailable` -> `unavailable` rule); I1 designSpec GT6 (guard_status `user_override`); I2 designSpec GT7 (`resume_decision` signature lacks `target_sha`/`applied_edits`); I3 GT8 (cycle id minting place); I4 GT9 (heading `Merge guard` vs case-sensitive grep `merge-guard`); I5 GT10 (43-member enum, no CHANGELOG edit); B6 alias GT1 (aliases-only rule vs slot-variables); B7 alias GT2 (present-tense statement vs defaults file exports real model ids, haiku is glm-5.3); B8 alias GT3 (tiers.md false "all other primitives use aliases"); I6 alias GT4 (omitted half of mapping constraint); I7 control GT1 (no task to update `tests/skills/test_worker_contract.py` gh-api classification table); I8 control GT2 (Complexity read-back match rule: numeric option id vs `single_select_option.name`).
- :419 "B1, B2, B6, I5 and I6 were never found by any top-10 panel; B3, I2 and I8 carry almost all catches."
- :431 scope: 106 runs (3 pilot arms + 103 scored combo rows, batch 10 dropped) in 62 sets; 0 mismatching cells across 62 x 16 x found/blocking.
- :497 ALL row: B3 95, B4 3, B5 4, B6 1, B7 28, B8 2, I1 4, I2 71, I3 2, I4 4, I5 0, I6 0, I7 16, I8 76 over 106 runs (column order in file; B1 and B2 = 0).
- :501 Never found in 106 runs: B1, B2, I5, I6. Found once: B6 (luna+terra+wonder).
- :503-505 Reach: widest sonnet+2luna (7 distinct issues over 6 runs); ember+sonnet and h2 (6 each over 4 runs); single run grok+2haiku+sonnet 6 in one run (never replicated); cheap default ember+2luna 4 distinct (B3, B7, I2, I8). Sonnet in 13 of 16 runs that reached I7: "an association across non-random sets, not a controlled comparison."
- :506 caveats: S18 B5 credit loose; S60 findings block failed to parse so zeros partly reflect panel failure.

### 4.13 What COMBO-REPORT does NOT show (gap list for the central design)
- No result on the product `superclaude review` panel code (T2b tiers, @default/@live7 resolution) beyond arms B/C pilot (which dropped Qwen slots); combos used raw ids via Bash, outside product dispatch. 
- Only 3 packages (2 defect-rich, 1 control); GT 16 defects total; 5 never caught. No held-out package; the 6 staged remaining packages (PILOT-REPORT:83) never run in A1 [UNVERIFIED for the collab study].
- No measurement of PASS/FAIL gate accuracy beyond GT coverage; verdict-vs-implement agreement noted only qualitatively (:60).
- Judge: single Opus pass per (combo,pkg); one 12-row re-judge (audit E) is the only variance check; arms A/B/C judged once (PILOT:76).
- No test of the hypothesis "name source.md in the brief" (inference only, :373); harness fixes proposed but their effect not measured in A1.
- No cost data for Tier 1 reviewer vs Opus judge cost in the same units beyond PILOT:52 (1,034,575 output tokens for 9 judges).
- Wall time and tokens are reviewer output tokens only (:204), not input/cache tokens; dollar cost not computed [UNVERIFIED].

## 5. combos/SPEC.md (E2@6c09843:A1/combos/SPEC.md, 152 lines): ops log and worker procedure

Procedure for a supervised worker (reusable runbook pattern, destination: reflect Tier 2 shadow-run runbook / central panel harness):
- :19-20 EVAL path (an Orca worktree path `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/...`), 3 package names.
- :22-24 Step 1 run `bash $EVAL/tools/run-reviewer.sh $EVAL <package> <reviewer id> <model> combos/<combo dir>`; <=2 at once ("gateway untested above ~10 parallel runs"); script checks observed model and `findings-v1` block, retries once, writes `<id>.cost.json`; 3000 s per attempt; both attempts fail -> INVALID.
- :26 Step 2 per-package resolution via `jq` from `resolution-live7.json` selecting reviewer ids and overwriting `.model`.
- :28 Step 3 `superclaude review merge --ledger ... --doc <pkg>/candidate.md --round 1 --report <id>=<path> ... --resolution ... --out ... merged-1.md`.
- :30 Step 4 RESULT.md table per package: reviewer, model, observed model, attempts, wall s, output tokens, invalid/thin (<1000 output tokens) flag, findings count, blocking count; 29 RESULT.md in tree.
- :33-36 Hard limits: read-only repo; do not open `ground-truth*.json`, other combos' folders or other arms' reviews; never Fable or Tier 0; no worktrees.
- :16 "Reviewer ids are only labels so the merge accepts them; the model per id is exactly the one in the table." (design smell: reviewer id (tier label) decoupled from model, so panel members are identified by label only).
- :38-39 Correction 2026-11-11: brief in `tools/run-reviewer.sh` listed category `unpassable-ac`, merge validator accepts only `unpassable-check`; fixed in script; old copy kept as `tools/run-reviewer.sh.unpassable-ac`; workaround `sed 's/unpassable-ac/unpassable-check/g'` to `.catfix.md`. **A reviewer brief contradicted the product validator.** (check at HEAD in section 13)
- :3-6 Speed-weighted combos rationale: pilot walls gpt-6-luna 61-148 s (thin, 2.4k-6.7k tokens), claude-haiku-5-5 185-610 s (~40k tokens), grok-4.7 610-957 s, glm-5.3 805-1435 s; "Tier 3 therefore has one usable model (glm-5.3); Tier 4 has luna, haiku, grok." (:3 says Qwen3.8-max "timed out twice (2 x 3000s) on 3 of 4 runs"; PILOT:12 says all 3 slots timed out: wording differs [UNVERIFIED which is exact])
- :8-14 Batch 1 combos c1-c5; :45-56 Batch 2 r1-r5, n1-n5 (muse-wonder-1.0 added by owner, pilot 153 s, ~17k tokens); :59-75 Batch 3 12 rows with ids t1b-1 (sonnet), t2b-1 (muse or terra), t2-1 (sol/terra).
- :77-79 contamination; re-run rules: waves <=4 workers, 1 concurrent reviewer each; "if any reviewer fails the observed-model check twice, STOP that worker ... do not silently drop a base reviewer" (kernel-relevant rule: degrade loudly).
- :81-82 Muse outage ~22:40 UTC 2026-11-11: "requests return init model and billing as muse-wonder-1.0 but every assistant message is served by gpt-6.1-terra". Detection = observed `assistant message.model`, not init/billing model.
- :84-85 Cooldown 60 min owner decision 22:43 UTC.
- :87-88 glm outage ~08:25 UTC 2026-11-12: probe returned assistant turns as `qwen3.8-max`, `unrecognized_model` on stderr; n5-terra design glm attempt1 timed out 3000 s 0 tokens.
- :90-95 Batch 4 root cause of terra/sol "incomplete": "candidates reference ./source.md but the sandbox only shipped candidate.md". `run-reviewer.sh` patched to ship source.md (originals kept). (Product/harness defect: plan candidate references an input file the reviewer sandbox did not include.)
- :97-100 Batch 4 amendment 14:42 UTC: all glm removed (owner: massive delays); parallelism 10 concurrent, muse capped at 4 (stream -P4 muse, -P6 other).
- :102-103 Quarantine luna: "luna refused to review without source.md (25/25 empty on affected packages)"; 428 reviewer files + "the 9 luna-bearing combo rows" (COMBO-REPORT:107 says 10 combo-row sets: **9 vs 10 mismatch**). Batch 1-3 blind scores for luna rows retained for audit only.
- :105-114 Batch 5 owner's 7 shortlist combos mapped to rows; 5 new rows = 42 reviewer runs.
- :116-117 Muse misroute recurrence ~15:46 UTC; 2 runs quarantined-in-place model_ok=false.
- :119-128 Batch 6 muse-ember-1.0 (owner adding to model list as "Tier 04 Model 02"); fallback ladder (muse-wonder<->muse-ember, glm->haiku, haiku<->luna, grok->haiku, sonnet->haiku, terra/sol->luna).
- :130-131 Fallback ladder v2: tier-ordered succession (02->03->04, T3->T4, T2->T2b, T1->T2, T4 wraps to T2); "muse-spark-1.3 and muse-wonder-full-1.0 currently misroute on the gateway (spark->sol, wonder-full->sonnet)"; Opus guard T1a never auto-selected (Tier 0/Opus owner-only).
- :133-135 Batch 7 six rows 54 runs, e4-haiku2-ember cancelled (19:41) -> 5 rows; :137-138 Batch 8 "9 combos x 4 replicates x 3 packages" (g1-g8 + worker-added g9 baseline); 36 rows x 3 pkgs; second same-model reviewer uses id t3-1.
- :140-141 Batch 9 incident (see 4.8): cyclic ladder, 69 FALLBACK lines in 3 s; "expected_model is overwritten by the fallback model" so model_ok passed; quarantine dirs `quarantine-haiku-fallback-20261112`, `quarantine-qwen-fallback-20261112`; harness fix: ladder never revisits a model, skips EXCLUDE_MODELS (default glm-5.3 Qwen3.8-max), honours `NOFALLBACK=1`; audit now checks each reviewer's expected_model against intended model.
- :143-148 Batch 10 (i1-grok-sonnet r1-r4, i2-haiku-sonnet r1-r4; 48 runs) dropped by owner 2026-11-13 01:09 ("we're done testing, we're going to decide and run with it"); correction :148: 8 outage-hit runs WERE quarantined into `quarantine-outage-20261113` (5 row dirs) and reruns left zero-byte stubs; excluded either way.
- :150-152 Batch 11 five replicates, one runner each, -P2 each = 10 concurrent, NOFALLBACK=1; "sessions are background processes, not Orca sessions (supervised worker cannot create worktrees/sessions)".
- Concurrency lesson: 12 concurrent workers -> identity bleed; at 10 concurrent with muse capped 4 the study ran clean for batches 4-11 except binary-replacement outages. Gateway behavior (identity bleed under load, cooldown 60-90 min) is the key infra risk for any panel using non-Claude models via the proxy.

## 6. tools/ (E2@6c09843:A1/tools/, 58 files)

### 6.1 `tools/run-reviewer.sh` (8,089 B, 87 lines; current form) = the reviewer harness
Usage line 2: `run-reviewer.sh <EVAL abs> <pkg id> <reviewer_id> <model> [subdir]`; one reviewer, fresh `claude -p` on a RAW gateway model id.
| Lines | What it does | Note for central design |
|---|---|---|
| :6-8 | `OUT=$EVAL/$PKG/reviews[/subdir]`; copies `candidate.md` to `/tmp/evalsb/cand/$PKG/candidate.md` if different | sandbox copy per package; sha256 in brief (:12) |
| :10-11 | ship `source.md` next to candidate if `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md` exists | **hard-coded absolute path of the E2 worktree**; added 2026-11-12 (batch 4); script silently skips source.md when file absent (`|| true`); never fails when input missing |
| :13-17 | BRIEF: `/sc:spec-panel @<cand> --mode critique` + first-review brief (copy of rules file line 32) + "First-review rules" + findings-v1 spec: "anchor = 12 to 200 chars copied exactly", category enum with `unpassable-check`, `verdict: PASS|FAIL` final line | does NOT name `source.md` anywhere [CODE-VERIFIED by reading :13-17]; includes "If an input is missing or unreadable, return incomplete" (terra/sol took this literally) |
| :23-43 | `FALLBACK` map (13 entries): glm-5.3->Qwen3.8-max->gpt-6-luna->muse-ember-1.0->claude-haiku-5-5->grok-4.7->gpt-6.1-sol->glm-5.3 (cycle); muse-wonder-1.0->muse-spark-1.3->gpt-6.1-terra->gpt-6-luna; sonnet/muse-wonder-full/opus -> gpt-6.1-sol | tier-ordered succession (owner order 2026-11-12 18:10 UTC); documents tier lists T3, T2, T2b, T1b/T1a, T4 |
| :45-60 | `run_attempt`: `( cd /tmp/evalsb/repo && timeout 3000 claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit <<<"$BRIEF" )`; extracts result text, OBS = unique `assistant` message.model (parent_tool_use_id null), TOK, TOKALL (modelUsage sum); APIERR = grep 'API Error' in result; MODEL_OK = obs == expected or expected+`-build` (case-insensitive); BLOCK_OK = `^```findings-v1` present; writes `<id>.attemptN.meta.json` | **model identity check is sound only while `$MODEL` is not mutated**: after fallback `$MODEL` is overwritten, so `expected_model` becomes the fallback model and a silent swap passes `model_ok` (batch 9 incident). BLOCK_OK checks only fence presence, not parseability (so a block with all lines invalid still passes the harness and fails later at merge) |
| :61-64 | 2 attempts per model | |
| :66-83 | fallback escalation unless `NOFALLBACK` set; `EXCLUDE_MODELS` default "glm-5.3 Qwen3.8-max"; `VISITED` prevents revisiting; log `<id>.fallback.log` | added after batch-9 incident (2026-11-12) |
| :85-87 | final = last attempt copy to `<id>.md`, `<id>.meta.json`; `<id>.cost.json` = {attempts, total_wall_s, total_output_tokens_all} over all `attempt*.meta.json` | cost.json counts both attempts and all fallback attempts |
- Reviewer isolation: `--permission-mode bypassPermissions` with only Edit/Write/NotebookEdit disallowed: reviewer keeps Bash and can read the whole sandbox repo and write to `/tmp` (probe.json `sandbox_write`: "Bash sessions can write to /tmp"). Study's isolation relies on the sandbox snapshot lacking `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research` (manifest.md:10); audit C found "no run read ground truth ... other reviewers' reports" (COMBO-REPORT:373) but old-era runs browsed sibling plan packages (WARN).
- `source.md` copy path is `.dev/tasks/done/<pkg>/source.md` in the E2 worktree: the input exists only because the implement run archived it there.

### 6.2 `tools/run-reviewer.sh.bad-launch` (4,302 B) and `.unpassable-ac` (4,352 B): superseded versions kept as evidence
- `.bad-launch:19`: `... --disallowedTools Edit Write NotebookEdit "$BRIEF"`: the variadic `--disallowedTools` option consumed the prompt; effect proven by `reviews-failed-launch-1/*/t1b-1.attempt1.err` = `Error: Input must be provided either through stdin or as a prompt argument when using --print` (read from `TASK-WF-design-20261108-041415/reviews-failed-launch-1/`). Fix = `<<<"$BRIEF"` on stdin. Failed-launch dirs: 56 / 49 / 49 files (design / designSpec / alias).
- `.unpassable-ac` differs from `.bad-launch` only by the stdin fix and a `cmp -s` skip-copy (diff on lines 8 and 19); its brief lists category `unpassable-ac` (found by grep of `contradiction|unpassable-ac|`).
- Harness defect list from the three versions: (a) variadic CLI flag swallowed prompt (bad-launch); (b) brief category typo `unpassable-ac` vs validator `unpassable-check`; (c) brief never ships `source.md` (until batch 4, 2026-11-12 ~12:59); (d) fallback ladder cyclic with overwritten expected_model (batch 9); (e) `claude` binary replaced mid-run (exit 127; batches 9, 10, 11) is not handled as an infrastructure outage, only as model failure; (f) the Qwen/glm exclusions implemented as env default not as per-run record.
- [CODE-VERIFIED at HEAD] (b): `src/superclaude/rules/prompts/document_review_loop_prompts.md:60` lists `unpassable-check`, identical to tip (`git show 6c09843:src/superclaude/rules/prompts/document_review_loop_prompts.md | diff` = IDENTICAL); `src/superclaude/cli/review/findings.py:15-22` CATEGORIES contains `unpassable-check` only. So the `unpassable-ac` defect was a transcription error in the E2 harness brief, not a product defect. [CORRECTS] the framing "category bug" (PILOT-REPORT:13,78) as harness-side.

### 6.3 `tools/tmp-scripts/` (55 files; `README.md` 4 lines, 728 B)
README: "Helper scripts that lived only in /tmp during the study. Copied 2026-11-13 ... only files that reference this eval ... verbatim copies: many hard-code /tmp paths and the 20261111-a1 eval directory, so read before re-running. Scripts already stored under analysis/ (merge-b7..b11, b7..b11 launchers, table and test scripts) are not duplicated here." Key ones named: b4-job-one.sh, judge-one.sh, anon-combos.sh, merge-b6.sh, gen-judge-list, checks-gate8 (named in README but NOT in the 55-file list: [UNVERIFIED missing]), merge-src-rows, startcombo*.
Groups by name (from ls-tree): anon (6: anon-arms, anon-b7, anon-b8, anon-b9, anon-b11, anon-combos); merges (arm-merges, merge-b6, merge-src-rows); batch runners (b4-*: job-one, luna-muse, luna-muse-gated, luna-nomuse, par-launch, par, run-noglm, run, terra-alone; b5-jobs-gen; b6-launch; b10-rerun-one; c1-driver, c2-run, c3-run, c5-chain; n2/n3/n4/n5 runners; r2/r3/r5 runners; startcombo, startcombo2, startcombo3); judge (judge-one.sh 2,307 B, gen-judge-list.sh 558 B, run-combo-judges.sh 2,771 B); misc (brief_c1.py 6,373 B, drift-b3.py, snap.py, stats.sh, rlog-r3.sh).

**Judge scripts (judge-one.sh, run-combo-judges.sh, gen-judge-list.sh)**
- judge = `claude -p --model claude-opus-5-5 --output-format json --no-session-persistence --permission-mode bypassPermissions`, 900 s timeout, brief on stdin (judge-one.sh:25-27); reads GT json, candidate, one anonymized merged report; writes `score.json` schema `{label, combo, package, gt_total, gt_covered_any[], gt_covered_blocking[], ledger_rows_total, ledger_rows_blocking, blocking_rows_gt_matched, wrong_blockers, notes}` (:21).
- Judge defects: (1) `[ -f "$D/score.json" ] && SKIP` (judge-one.sh:7, run-combo-judges.sh:11): a stale or corrupted score.json is never re-judged; this is how the n2-sonnet-src corrupted score survived until audited (COMBO-REPORT:146). (2) success test = rc 0 and valid `judge.json` JSON (:28), NOT that `score.json` was written or well-formed. (3) judge `gt_covered_blocking` = defect matched by a blocking-flagged ledger row, ignoring the GT field `blocking_in_implement` (brief :19); audit F found 65 judge-blocking vs 38 real (COMBO-REPORT:291). (4) "wrong blocker" = blocking row with no GT correspondence (:20), structurally penalizes novel real defects (PILOT-REPORT:79). (5) Judge runs on `claude-opus-5-5` with bypassPermissions and is told "Do not read anything outside the files named here" (instruction, not enforcement). (6) `run-combo-judges.sh:2` comment says 39 judges (13 combos x 3), hard-coded; later scripts anon-b7/8/9/11 + merge-b7..b11 + b7..b11-judge.tsv scale it.
**Anonymization (anon-arms.sh, anon-combos.sh)**: label pool X/Y/Z for arms (random per package, key `arm-key.json`), Q..V for combos (`label-key.json`); `sed` replaces `$EVAL` path with `<EVAL>`, reviewer ids matched by regex `\bt[0-9a-z]+-[0-9]+\b` mapped to R1..Rn, candidate path line and report paths redacted. Blindness limits: anonymization is regex-based; combo label pool is only 6 letters (Q..V) so label uniqueness per (combo,pkg) uses a directory-exists loop (anon-combos.sh:14), ids matching is by tier-shaped ids only.
- Leak check at tip: 54 of 319 `merged-anon.md` files contain a model-id string (case-insensitive `claude-haiku|claude-sonnet|gpt-6|grok-4|muse-...|glm-5|qwen`); the sampled hits (alias package X/Y/Z, `b4-muse-ember-luna2/.../Z`) are plan content (the alias-package plan itself discusses haiku=glm-5.3 and T3Model01), not reviewer identity. Not exhaustively classified [UNVERIFIED for the other ~50].
**merge-b6.sh (pattern for later merge-bN.sh)**: builds resolution JSON by hand with keys `reviewer_id, model, alias, tier, strategy:"fixed", stand_in:false, fallback_depth:0, fallbacks:[], launch:null, seed:null, slot_id` from `resolution-live7.json` (:19-27) then runs `superclaude review merge ... --round 1` (:36) and, if the CLI answers `expects round 2` (stale ledger), moves ledger+merged to `stale-r1/` and re-merges (:38-41) [matches `ledger.py:114-118` LedgerError]. Skip rule `[ -f merged-1.md ] && skip` (:18) is why stale merges survived (audit D: n2-terra, r2-sol, n5-sol, n5-terra). Gate `model_ok == true` per reviewer meta (:32).
**b4-job-one.sh**: per-row cancel sentinel `/tmp/cancel-<combo>` (:5), `START/END` log lines with observed model, model_ok, findings_block. **stats.sh**: greps `"blocking" *: *true` (space-tolerant, :14) = the post-correction parser; counts per reviewer.
**snap.py / drift-b3.py (cross-effort hit)**: both reference E1 paths under THIS branch: `snap.py:4` writes `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboD-r1/artifacts/input-snapshot.yaml` with `input_tree_sha256` over file list [`TASK-WF-designSpec-20261107-075614.md` sha256 `044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481`, `source.md` sha256 `a865f397468a076c9c070c031f807b44d9cccd91059b2ad5efb1b926090ba10a`]; `drift-b3.py:2` reads `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/`. These two scripts are E1 (shadow-model-combos) helpers sitting in the E2 tools dir; README says only scripts that reference this eval were copied, but these reference E1's tree (see section 12, overlap).

## 7. Study inputs: three packages, ground truth, resolutions (E2@6c09843, per package dir)

| Package | candidate.md lines | GT items (blocking_in_implement) | GT classes (own vocabulary) | Draft GT items | Role |
|---|---|---|---|---|---|
| `TASK-WF-designSpec-20261107-075614` | 200 | 10 (5 blocking: GT1-GT5) | contradiction 5, ambiguity 3, missing-task 1, unpassable-ac 1 | 10 | defect-rich |
| `TASK-WF-makeTheAliasOnly-20261105-051649` | 134 | 4 (3 blocking: GT1-GT3) | contradiction 3, ambiguity 1 | 6 (GT5, GT6 dropped) | defect-rich |
| `TASK-WF-design-20261108-041415` | 173 | 2 (0 blocking) | ambiguity 1, missing-task 1 | 2 | "control" |
- Source for all numbers: `jq` over `ground-truth.json` at the tip. Totals 16 GT items, 8 blocking, matches PILOT-REPORT:7 and COMBO-REPORT:9.
- GT classes (`unpassable-ac`, `missing-task`, `ambiguity`, `contradiction`) differ from findings-v1 CATEGORIES (`contradiction, unpassable-check, data-loss, safety, missing-requirement, other`, `findings.py:15-22`): two vocabularies; GT1 of designSpec carries `unpassable-ac` as a GT class (not the reviewer label).
- GT provenance (`ground-truth-draft.json` notes): defects observed in past /sc:implement runs ("blocking_in_implement" = the task hit review failure/attempt exhaustion/operator halt). designSpec notes: GT1 and GT2 "describe two plan defects ... behind the same Task 1 failure (5 attempts, ladder end, two operator-review halts); count them together if one item per failure is wanted"; GT6 comes from the advisory plan review in executor-guidance.md, referenced `.dev/reflect/pre-designSpec-20261107075755/REPORT.md` "is not present in this worktree", accepted by owner (human_acceptance). alias: `dropped` GT5 (stale commands.py citations; evidence_ok false) and GT6 (executor's own code-path wording; evidence_ok false); GT6 attribution "lower confidence". design: "Every task T1-T12 finished compliant on its first attempt ... FINAL is pass, so no item was blocking in implement"; GT2 "weaker: ... evidence that the built read-back rule was actually wrong is the later 'clarified' entry plus the observed response shape, not a recorded failing run."
- **The control is not a clean plan**: it has 2 real (non-blocking) GT defects; so "control" = plan with no implement-blocking defect. Verdict FAIL there is not necessarily wrong; the wrong-blocker count on it is the only precision measure.
- Per-package `resolution-default.json` / `resolution-live7.json` (schema `review-panel-resolution/1`, with `template_sha256`, `tiers_sha256`, `environment:"gateway"`, `review_kind:"first"`): resolved ONCE with the product CLI, random draws fixed per package. Verified compositions: designSpec default = t1b sonnet, t2 muse-spark-1.3, t3 glm-5.3, t3 Qwen3.8-max; live7 adds t2b gpt-6.1-terra, t4 haiku, t4 grok. alias default = sonnet, muse-spark, Qwen, glm; live7 adds t2b muse-wonder-1.0, t4 grok, t4 luna. design default = sonnet, Qwen3.8-max (t2-1), glm-5.3 x2 (t3-1, t3-2); live7 = sonnet, Qwen (t2-1), t2b glm, Qwen (t3-1), glm (t3-2), haiku, luna.
- **Product template facts** [CODE-VERIFIED at HEAD `src/superclaude/cli/review/data/`]: `review-panel.live7.json` slots t1b(fixed,1) + t2(random,1) + t2b(random,1) + t3(random,2) + t4(random,2) = 7 reviewers; `review-panel.default.json` = t1b(fixed,1) + t2(random,1) + t3(random,2) = 4. `review-tiers.default.json` tier3 = [glm-5.3, Qwen3.8-max], tier4 = [gpt-6-luna, claude-haiku-5-5, grok-4.7] (no muse-ember-1.0 in the product tiers file at HEAD), tier2b = [gpt-6.1-terra, glm-5.3, Qwen3.8-max, muse-wonder-1.0].
- Consequence (derived): the study excluded glm-5.3 and Qwen3.8-max (owner order, SPEC:98, PILOT:12, `run-reviewer.sh:69`), but BOTH are the only Tier 3 models in the product tiers file and appear in tier2/tier2b: product `@default` and `@live7` templates each draw 2 Tier-3 reviewers, so with those two excluded no valid Tier 3 panel exists. The study's recommended panels (ember/luna/haiku/sonnet) are NOT expressible as `@default`/`@live7` templates [UNVERIFIED whether template customization exists; product has `review-panel.*.json` per template].
- Reviewer-run inventory per package reconciles PILOT:12 ("Qwen3.8-max ... all 3 of its slots (one per package) timed out") with the resolutions: the resolution files hold Qwen3.8-max at designSpec t3-2, alias t3-1, design t2-1 and design live7 t3-1 = 4 Qwen reviewer ids; SPEC.md:3 says "timed out twice (2 x 3000s) on 3 of 4 runs". PILOT says 3 slots/9,000 s. The two counts differ in wording (4 slots with 3 timeouts vs 3 slots) [UNVERIFIED which is exact].
- Same-plan overlap with E1: E1's `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` has sha256 `044809e3a963fad395cfbe0988bece975650a3adf17176893665d92338bd3481` = sha256 of E2 `TASK-WF-designSpec-20261107-075614/candidate.md` at the tip (both computed by sha256sum): **byte-identical plan**. E1's `source.md` sha256 `a865f397468a076c9c070c031f807b44d9cccd91059b2ad5efb1b926090ba10a` = sha256 of `.dev/tasks/done/TASK-WF-designSpec-20261107-075614/source.md` at HEAD, which is the file E2's `run-reviewer.sh:10` ships as `source.md` (path form `.dev/tasks/done/<pkg>/source.md`; E2's own copy of source.md is not committed in A1: 0 `source.md` paths in the tree). Therefore E1 and E2 reviewed the same designSpec plan with the same source: E1's per-run catches can be compared with E2 designSpec GT1-GT10 directly (destination: unified GT).
- `source.md` sha256 prefixes at HEAD for the other packages: alias `9c7df653062887a4...`, design `1e0d8cdca37abe75...` (prefix only).

## 8. analysis/ (E2@6c09843:A1/analysis/, 141 files): scripts, derived tables, audits

### 8.1 Top-level (all sizes bytes)
- Reports/derived: `final-table.md` (6,375; 59 lines; same content as COMBO-REPORT:303-359), `b8-final.md` (2,891; 27 lines), `b9-final.md` (2,149; 17 lines), `final-all.json` (9,540), `final-clean.json` (5,641), `attrib.out` (2,415), `doubles.out` (1,824), `untried.out` (4,052), `gt2-hits.txt` (362).
- Estimates: `combo-est-A.md` (5,612; 51 lines), `combo-est-B.md` (7,918; 66 lines), `combo-est-self.md` (2,062; 25 lines): three independent analyst estimates of the top-5 untried combos (2026-11-12); all "UNVERIFIED as predictions" (combo-est-A.md:3), n=1 based; none was executed (batch 10 dropped).
  - combo-est-self.md:3-12 per-model stats (source.md era, 3 packages): sonnet 27 runs, 29.4k avg tok/run, 0.26 blocking claims/run, 5.7 findings/run; haiku 33 runs 57.5k 1.09 8.3; grok 21 53.6k 1.19 3.8; muse-wonder 27 15.7k 1.30 5.3; muse-ember 18 11.2k 0.61 4.6; luna 51 4.7k 1.37 1.7; terra 18 2.1k 2.06 2.5; sol 3 3.9k 2.00 2.7.
  - combo-est-self.md:23 "2x sonnet ... doubles as the missing sonnet-with-source.md baseline (arm A was run before source.md)": **arm A was never re-run with source.md**, so COMBO-REPORT:59/67 ("no combo beats arm A's efficiency", 2.15 catches/100k) compares a pre-source.md arm A with source.md-era combos [UNVERIFIED for the collab study].
  - combo-est-B.md:3-26 per-model GT-hit tallies: sonnet catches designSpec GT3 in ~7 of 8 sonnet rows, GT9 and GT5 only in sonnet rows, rarely says "blocking" (0.28 claims/run defect-rich); grok is the only source of GT6 (c3, r3) plus GT7; alias GT3 and GT4 never caught by any src row; luna/terra are "the wrong-blocker engine".
  - combo-est-A.md:11 derived per-model total tokens (3 packages): terra ~7k, sol ~12k, luna ~25k, ember ~9k, wonder ~35-50k, sonnet ~65-115k, haiku ~165k, grok ~130-160k (+-30%).
- Scripts: `attrib.py` (78 lines; header "Approximate: parses judge prose ... Wrong blockers credited to members marked blocking"; hard-coded E2 worktree absolute path :3; the attribution method RETRACTED at COMBO-REPORT:197), `doubles.py` (1,374 B; retracted), `untried.py` (46 lines), `three-way.py` (63 lines; line 4 `exec(open("/tmp/final-table.py")...)`: depends on a /tmp file not in the commit), `final-table.py` (83 lines; defines valid-era filter `valid(r)` by row-name pattern: `-src`, `b4-*`, `-ember`, `[egh]<digit>`, sol/terra-alone; excludes contaminated/superseded/quarantine/invalid and `i1-`/`i2-`; GT blocking map; audit EXCLUDE flags BAD_CHECKS A none, B 1-incomplete/1-short, D 2-blockok/3-conserve/3-dropped-blocking/1-path/5-stale, E none, F 3-completeness), `b8-table.py` (88 lines, family definitions FAM), `b9-table.py` (3,241 B).
  - Reproducibility defect: all these scripts hard-code `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/...` and read raw `*.attempt<N>.json` / judge session files that are not committed; they rerun only on the original machine [CODE-CHECKED by reading headers].
  - The valid-era selector is a row-NAME pattern; composition is read from meta.json elsewhere. Rows with the same name pattern but different content (r2 incident, COMBO-REPORT:170) show the risk.
- Launch/merge scripts: `b7-launch.sh`, `b8-launch.sh`, `b9-launch.sh`, `b10-launch.sh`, `b11-launch.sh`, `b11-rerun-one.sh`, `merge-b7.sh` ... `merge-b11.sh`, `b7-judge.tsv` (832 B), `b8-judge.tsv` (6,168 B), `b9-judge.tsv` (1,516 B), `b11-judge.tsv` (850 B), `b10-fix.txt` (578 B), `b11-fix.txt` (358 B).

### 8.2 `analysis/audits/` (46 files; six read-only audits A-F run 2026-11-13, every valid-era run: "71 rows, 213 row-packages", COMBO-REPORT:290)
| Audit | Subject | Files | Headline (source) |
|---|---|---|---|
| A | model identity & attempts | `audit.py` (12,976 B), `flags.tsv`, `stats.json`, `summary.md` (5,458 B, 34 lines), `tbl.py` | 890 reviewer runs in 70 rows (batch 10 excluded); 1 root cause EXCLUDE = 2 runs (`b4-muse-luna2/t2b-1` alias + design: asked muse-wonder-1.0, served gpt-6.1-terra, model_ok=false) (summary.md:7); intended == expected == observed 0 mismatches over 828 runs with resolution (:11); 102 runs without resolution entry derived from row name; `fallback.log` present in 0 runs (:12); caveat: silent fallback would hide (known overwrite flaw) |
| | | | `unrecognized_model` in 744 attempt `.err` files = benign client warning for non-Claude names (:18); 57 of 59 `modelUsage` extra keys = auxiliary call to alias `claude-gw-tier2[1m]` (~512 output tokens, `web_fetch_apply`): reviewers used WebFetch and that call is counted in `output_tokens_all` (:22); 10 retries (glm x7 where attempt1 observed `glm-5.3,qwen3.8-max`); 5 runs have stale `attempt2` leftovers that over-count cost (:15); 8 earlier-attempt model differences (:25); terra short reports under 400 tokens: 2 WARN (:18) |
| B | report validity / incomplete reports | `audit.py` (14,375 B), `flags.tsv` (28,719 B), `stats.json`, `inc.txt`, `vi.txt`, `patch.py`, `patch2.py`, `peek.py`, `sumry.py` | no summary.md; stats: 51 reports say incomplete, 16 empty terra reviews valid-era; luna anchor fidelity 91.4% (COMBO-REPORT:294) |
| C | inputs/timing / source.md references | `audit.py` (14,724 B), `flags.tsv` (45,853 B), `runs.json` (231,656 B), `candwrites.py`, `leakdbg.py` | no summary.md; 156 of 665 valid-era runs never referenced source.md; no GT/other-report reads; timeline (COMBO-REPORT:373) |
| D | merge and ledger integrity | `audit.py`, `audit2.py`, `mk.py`, `anch.py`, `bok.py`, `flags.tsv` (58,833 B; header says 438 lines), `audit2.json`, `extra.json`, `exclude-list.txt`, `run1.txt`, `summary.md` (8,267 B, 90 lines) | 89 rows x 3 pkgs = 264 merged-1.md examined (:3); counts C1-C6 (:5-12); drop reasons anchor>200: 56, anchor2>200: 18, claim>300: 14, bad severity 3, refs-bad 1 (:16) = 92 dropped findings in 80 reviewer-level block-ok-false cases; by model luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet/terra/sol 0 (:17); kept/raw ledger counts: haiku 1085/1108, sonnet 446/446, glm 86/93, luna 356/386, sol 8/8, terra 103/103, grok 205/207, ember 834/867, wonder 275/289 (:18); 49 dropped findings blocking (:8,:19) |
| | | | VERDICT FLIPS listed (:20) = 3 explicit (g3-sonnet-luna-ember-r3 alias t4-1 F1; g5-ember2-luna-r2 alias t4-1 F1; n5-sonnet-ember design t4-1 F1+F2) + total-loss merges (g1-ember-luna2-r4 alias t3-1; g7-haiku-luna2-r4 designSpec t4-1 6/6 dropped; n4-sonnet-ember design t4-1 8/8; h1-..-r2 designSpec t4-2; h1-..-r3 designSpec t4-1); COMBO-REPORT:292 says "Four verdicts flipped FAIL->PASS" (count differs from the 3 enumerated) |
| | | | X1 clustering: `findings.py cluster()` union-find, 195 of 1398 rows with >=3 members are chains, 144 span >60 lines, 83 rows have >=8 members or >=4 sections (e.g. r2-sonnet-ember/designSpec L1: 19 members across 8 sections, 142/171 pairs unrelated) (:29); row anchor/claim = first member only (so a row can match the wrong defect and one mega blocking row counts as ONE blocking row); X2 46 rows have null span (anchor not found in candidate), 13 blocking (:30); X3 reviewer/fid mapping 0 mismatches (:31); X5 0 verdict/row logic violations (:33); stale: n2-terra (3 pkgs t2-1+t4-1), r2-sol design t2-1+t4-2 (16 EXCLUDE) (:10); n5-sol/n5-terra merge used a t4-1 no longer in the row dir (:23); 45 merges lack `merge-stdout.txt` so merge warnings unverifiable (:26) |
| E | scoring integrity | `check.py` (11,228 B), `check2.py`, `by.json`, `rows.json`, `flags.tsv` | no summary.md; 294 judge outputs clean; 12/12 re-judge agreement; 19/19 catches confirmed (COMBO-REPORT:296) |
| F | aggregation / stale text | `recompute.py` (17,857 B), `extra.py`, `extra2.py`, `names.py`, `fam.json`, `fam.tsv`, `presence.txt`, `recomputed.tsv`, `rows.json`, `stats.tsv`, `flags.tsv` | no summary.md; blocking-definition finding (65 vs 38); Welch/permutation statistics (COMBO-REPORT:291,298) |
- Only audits A and D ship a `summary.md`; B, C, E, F results are known only from COMBO-REPORT:290-298 plus raw `flags.tsv`/`stats` (their headline numbers [UNVERIFIED] against their flags files in this slice).

### 8.3 `analysis/issue-table/` (28 files) and `analysis/allsets/` (29 files)
- issue-table: `issue-01..10.json/.tsv` (one per top-10 panel), `issue-legend.json/.tsv`, `issue-setup.py`, `issue-compare.py`, `issue-table.py`, `issue-table-direct.json`, `issue-table-final.md`, `top10.json`; method = 10 parallel agents + independent direct computation; 0 mismatching cells out of 320 (COMBO-REPORT:386).
- allsets: `allsets-chunks/chunk-01..10.json`, `allsets-out/chunk-01..10.json`, `chunk05_notes.json`, `chunk05_script.py`, `build03.py`, `c10.py`, `allsets-direct.json`, `allsets.json`, `allsets-setup.py`, `allsets-table.py`, `allsets-table.md`; method = 10 agents reading judge notes + direct script; 0 mismatching cells across 62 sets x 16 issues x found/blocking (COMBO-REPORT:431).
- Pattern: agent-built tables cross-checked by an independent deterministic script ("agents propose, script confirms"): reusable verification pattern (destination: rf-qa replacement / reflect evidence validator).

## 9. Code cross-check of every code claim in the study (HEAD = 50d4d2b9d1f2288afa497830b3049f2fe48f5c75, worktree branch ironbelly/shadow-runs; tip = 6c09843)

| # | Study claim (source) | Code at HEAD | Mark |
|---|---|---|---|
| C1 | Merge validator accepts only `unpassable-check` (SPEC.md:38-39; PILOT:13) | `src/superclaude/cli/review/findings.py:15-22` CATEGORIES = contradiction, unpassable-check, data-loss, safety, missing-requirement, other; check at `:102-103` | [CODE-VERIFIED] |
| C2 | Reviewer brief had `unpassable-ac` (bug) | product rule `src/superclaude/rules/prompts/document_review_loop_prompts.md:60` lists `unpassable-check`; file identical at tip (diff = IDENTICAL) -> E2 harness brief mis-transcribed it | [CODE-VERIFIED]: harness defect, not product defect |
| C3 | Merge keeps only well-formed lines; anchors >200, anchor2 >200, claims >300, bad severity, bad refs dropped (COMBO-REPORT:292; audit-D summary:16) | `findings.py:90-121` `_check_finding` limits: anchor 12..200 (`:104`), anchor2 12..200 (`:107-108`), claim <=300 (`:118`), severity enum (`:96`), MINOR cannot be blocking (`:100-101`), refs <=8 strings (`:112-117`); `parse_block` appends error and continues per line (`:160-195`); `ledger.py:127-138` keeps parsed findings only ("A reviewer with an invalid block is skipped for clearing but its parsable findings are kept", `:112`) | [CODE-VERIFIED] drop behaviour |
| C4 | ...discarded "with no error" (COMBO-REPORT:292) | NOT silent: `ledger.py:130-134` appends a warning per reviewer ("findings block problem (N error(s)), first: msg"), `ledger.py:295-296` returns `block_ok` and `warnings`, `merge_cmd.py:117-118` prints them as JSON, merged report prints `block ok false` (`ledger.py:423`). But the warning names only the FIRST error and not the dropped finding ids, severity, or the count of blocking findings lost; and 45 merges have no saved `merge-stdout.txt` (audit-D:26) | [CODE-CONTRADICTED] on "no error"; [CODE-VERIFIED] on "under-informative" |
| C5 | Four verdicts flipped FAIL->PASS because dropped blocking findings left no blocking row (COMBO-REPORT:292; audit-D:20 lists 3 + total-loss merges) | verdict = `"FAIL" if brief else "PASS"` where `brief` = open/regressed blocking rows (`ledger.py:100-104`, `:273-274`); the reviewer's own `verdict:` line is never parsed (grep `verdict` in ledger.py: only computed/rendered) | [CODE-VERIFIED] mechanism; count 3 vs 4 differs [UNVERIFIED which] |
| C6 | Merge refuses a round only when no reviewer produced a valid block (COMBO-REPORT:7, c1 case) | `ledger.py:150-157` raises LedgerError "no reviewer produced a valid findings block ... the ledger was not changed" only if `not any(block_ok.values())` | [CODE-VERIFIED] |
| C7 | 83 merged rows lump unrelated findings ("chaining"); one mega blocking row counts as ONE (audit-D:29) | `findings.py:382-407` `cluster()` union-find over `same_defect`; `same_defect` `:367-379`: same fingerprint with refs, or (refs intersect or both empty) and spans within 3 lines (`:374-378`, `s1[0] <= s2[1] + 3`); transitive by union-find; row anchor/claim = `first` member (`ledger.py:182-199`) | [CODE-VERIFIED] mechanism; counts (83, 195/1398) [UNVERIFIED] |
| C8 | Anchor not found in candidate -> span null, kept, not clustered by span (audit-D X2: 46 rows, 13 blocking) | `findings.py:346-360` `annotate`: `anchor_status` "missing", `span` None; `ledger.py:196` row span None; `same_defect` requires spans or fp | [CODE-VERIFIED] mechanism |
| C9 | `superclaude review merge` stale ledger -> "expects round 2" (merge-b6.sh:38) | `ledger.py:114-118` `LedgerError("round {n} cannot be merged: the ledger expects round {expected}")`; `merge_cmd.py:101-109` loads existing ledger or creates at round 1 | [CODE-VERIFIED] |
| C10 | Resolution JSON fields strategy/stand_in/fallback_depth/fallbacks/launch/seed/slot_id (merge-b6.sh:23) | `panel.py:652-679` emits `slot_id`, `strategy`, `fallback_depth`, `stand_in`, `launch` | [CODE-VERIFIED] (hand-built resolution matches product emission keys) |
| C11 | `@live7` resolves 7 reviewers; `T2bModel01=gpt-6.1-terra` (manifest.md:9) | `data/review-panel.live7.json` 5 slots t1b1+t2 1+t2b 1+t3 2+t4 2 = 7; `data/review-tiers.default.json` tier2b models [gpt-6.1-terra, glm-5.3, Qwen3.8-max, muse-wonder-1.0] | [CODE-VERIFIED] |
| C12 | Tier aliases serve only the first model of a tier (manifest.md:11; probe.json alias_findings) | `data/review-tiers.default.json:26,29`: `gateway` environment `"note": "... dispatch mechanism per model not defined yet."`, `"launch": {}`; only `anthropic-only` env has launch map (`:35`) | [CODE-VERIFIED] that the product has NO dispatch for non-first-slot gateway models; alias behaviour itself [UNVERIFIED] (gateway runtime) |
| C13 | Reflect panel profiles cap Claude-launched reviewers | `panel.py:71-73` `_REFLECT_PREFIX = "reflect-"`, `_REFLECT_LAUNCH = ("sonnet", "opus", "haiku")`, `_REFLECT_MAX_REVIEWERS = 3`; `:153-156` rejects other launch values | [CODE-VERIFIED] (conflict with E2 raw-id `claude -p` approach: reflect profile cannot name a gateway model) |
| C14 | findings-v2 is a superset container with CHANNELS/DEVIATION_CLASSES and completion states (E1) | `findings_v2.py:9-43` `V1_FIELDS`, `ROLES`, `LENSES`, `CHANNELS`, `COMPLETION_STATES = (complete, truncated, invalid, failed, timed_out)`; same `_check_flat` limits imported from findings.py (`:14-21`) | [CODE-VERIFIED]: E1 inherits the same 200/300-char limits that dropped 92 findings in E2 |
| C15 | Judge/arm numbers (all score tables) | not code; scripts + raw judge sessions not committed | [UNVERIFIED] by me; only audits E/F evidence |
| C16 | "brief never names source.md; inference UNVERIFIED" (COMBO-REPORT:373) | `run-reviewer.sh:13-17` brief has no `source.md` string; the sandbox ship at `:10-11` places it next to candidate | [CODE-VERIFIED] that brief omits it; causal claim stays [UNVERIFIED] |
| C17 | Brief already instructs "anchor = 12 to 200 chars copied exactly" | `run-reviewer.sh:17` and product rule `document_review_loop_prompts.md:60` both say so; the claim cap (300) is NOT in either brief | [CODE-VERIFIED]: harness fix (1) of COMBO-REPORT:371 "instruct reviewers" is already in place for anchors, absent for claim length; 56 anchors still exceeded 200 |
- Not checked against code: `claude -p` CLI behaviours (`--disallowedTools` variadic), gateway routing, judge behaviour.

## 10. Decisions made and open (E2 original study)

### 10.1 Made (owner or study), with source
| # | Decision | Source | Status |
|---|---|---|---|
| D1 | Raw gateway model ids via Bash `claude -p --model`, not tier aliases | manifest.md:11; probe.json | in force |
| D2 | Reviewer sandbox = `git archive` of HEAD without `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research` | manifest.md:10 | in force |
| D3 | Fixed decision rule (>= 2x arm A defect-rich catches AND <= 1 wrong blocker on controls) set BEFORE scoring | PILOT-REPORT:56 | applied; superseded by batch 4+ ranking principle |
| D4 | Qwen3.8-max disqualified (3000 s timeouts) | PILOT:12 | in force |
| D5 | glm-5.3 excluded (delays/outages) | SPEC.md:98; run-reviewer.sh:69 | in force |
| D6 | Pre-source.md luna data quarantined; only `-src` luna may be cited | COMBO-REPORT:107; SPEC.md:102-103 | in force |
| D7 | muse-wonder replaced by muse-ember-1.0 (Tier 04 Model 02); wonder weekly limit | SPEC.md:119-120 | in force |
| D8 | Fallback ladder v2 -> v3 (tier-ordered, never revisit, EXCLUDE_MODELS, NOFALLBACK=1) | SPEC.md:130-131,141 | in force (tool); NOFALLBACK=1 used for batch 11 |
| D9 | Batch 10 dropped, testing closed ("we're done testing, we're going to decide and run with it") | SPEC.md:146 | final |
| D10 | Six read-only audits A-F of all valid-era runs | COMBO-REPORT:290 | done |
| D11 | Final guidance: default = ember + 2x luna; optional quality tier sonnet + 2x luna; best measured real-blocking haiku + 2x luna; harness fixes first | COMBO-REPORT:363-371, 428 | final recommendation (not implemented in product) |
| D12 | Concurrency caps: 12 workers = identity bleed; 10 concurrent with muse capped 4 clean; later 10 | SPEC.md:78,99,151 | operational rule |
| D13 | Judge = claude-opus-5-5 single pass per (combo, package) on anonymized merged report | judge-one.sh:25 | applied |
### 10.2 Open / not done (as of tip)
- O1 Harness fixes proposed before any further testing: (1) raise or truncate 200-char anchor limit at merge or re-validate reviewers (COMBO-REPORT:371); (2) name `source.md` path in brief; (3) keep fallback-ladder fix and model-identity audit in runner. Whether done: the E2 `run-reviewer.sh` at the tip still has no source.md in the brief and no truncation in `findings.py` [CODE-VERIFIED at HEAD for findings.py; run-reviewer.sh read at tip]. So still open.
- O2 Which of ember+2luna / sonnet+2luna / haiku+2luna to standardize: guidance given but "all panels sit at about 2-2.5 of 14".
- O3 Remaining 6 packages staged (PILOT-REPORT:83): never run in A1 [UNVERIFIED in collab].
- O4 Five GT defects never caught: designSpec GT1, GT2, GT10, alias GT4 (+ alias GT3 caught once): "point at the review brief, the packages or the ground truth" (COMBO-REPORT:287).
- O5 Whether `source.md` explicit path in brief lifts ember/luna (inference only).
- O6 Replicate r2-sonnet-src (haiku x2 + grok + sonnet) 4 reps: was candidate #1 of untried (COMBO-REPORT:279); dropped with batch 10 / testing closed.
- O7 Arm A (sonnet alone) re-baseline with source.md (combo-est-self.md:23): never run.
- O8 Judge variance for pilot arms A/B/C (PILOT:76).

## 11. Defects found

### 11.1 In product code (claimed by the study; checked at HEAD in section 9)
| ID | Defect | Evidence | Mark |
|---|---|---|---|
| P1 | Merge drops invalid finding LINES (anchor >200, anchor2 >200, claim >300, bad severity, bad refs) while keeping the reviewer; block flagged `block_ok:false`; verdict computed from remaining rows, so a reviewer's dropped blocking finding can turn FAIL into PASS | `findings.py:90-121,160-195`; `ledger.py:112,127-138,150-157,273-274`; study: 92 findings dropped in 80 reviewer-level cases, 49 blocking (audit-D:8,16,19) | [CODE-VERIFIED]; "no error" part [CODE-CONTRADICTED] (a warning exists, ledger.py:130-134) |
| P2 | Warning gives only first error per reviewer; dropped ids not listed; no `merge-stdout.txt` kept for 45 merges so even that is lost | `ledger.py:131-134` | [CODE-VERIFIED] |
| P3 | Transitive clustering (union-find over proximity within 3 lines when refs intersect or both empty) chains unrelated findings into one "megacluster" row; row anchor/claim = first member only | `findings.py:367-407`; `ledger.py:182-199`; audit-D:29 (195 of 1398 chain rows; 83 megaclusters) | [CODE-VERIFIED] mechanism |
| P4 | Anchors that do not occur in the candidate are kept with null span (46 rows, 13 blocking) so they never cluster by span and cannot be anchor-verified; "verbatim anchor" is not enforced | `findings.py:346-360` | [CODE-VERIFIED] mechanism |
| P5 | `superclaude review merge` is not re-runnable for a round: existing ledger -> "expects round 2"; operators moved ledgers to `stale-r1/` | `ledger.py:114-118`; `merge_cmd.py:101-109`; merge-b6.sh:38-41 | [CODE-VERIFIED] |
| P6 | Merge refuses only when NO reviewer has a valid block: a panel of 7 with 1 valid block merges and may certify PASS on thin coverage (ledger records `block_ok` per reviewer but no minimum-quorum rule) | `ledger.py:150-157` | [CODE-VERIFIED] mechanism; effect in study: r5 alias glm block ok false, round accepted on haiku runs (COMBO-REPORT:7) |
| P7 | Gateway environment has no dispatch mechanism for any model beyond the tier's first slot | `data/review-tiers.default.json:26,29` ("dispatch mechanism per model not defined yet.", `"launch": {}`) | [CODE-VERIFIED] |
| P8 | Product tier3 = [glm-5.3, Qwen3.8-max] (both excluded in the study by owner order) and `@default`/`@live7` draw 2 tier-3 reviewers | `data/review-tiers.default.json` tiers; `review-panel.default.json`, `review-panel.live7.json` | [CODE-VERIFIED] (exclusion is a study decision) |
| P9 | Two vocabularies: GT class (`unpassable-ac, missing-task, ambiguity, contradiction`) vs findings category (`unpassable-check, missing-requirement, ...`); reflect category map in findings_v2 adds a third (`ordering, acceptance, coverage, contradiction, risk, deviation`) | `ground-truth.json` classes; `findings.py:15-22`; `findings_v2.py:39-46` | [CODE-VERIFIED] |
| P10 | Product `findings.py` limits (200/300) are shared by findings-v2 (E1) through `_check_flat` import: the same silent-drop path applies to reflect Tier 2 reviewers | `findings_v2.py:14-21` (imports `_check_flat`) | [CODE-VERIFIED] import; effect on E1 [UNVERIFIED] |

### 11.2 In the E2 harness/tooling (not product code)
| ID | Defect | Evidence | Found / fixed |
|---|---|---|---|
| H1 | Variadic `--disallowedTools` swallowed positional prompt: every launch failed with "Input must be provided either through stdin or as a prompt argument when using --print" | `run-reviewer.sh.bad-launch:19`; `reviews-failed-launch-1/*/t1b-1.attempt1.err` | fixed (stdin `<<<"$BRIEF"`); dirs kept (56/49/49 files) |
| H2 | Brief category typo `unpassable-ac` | `run-reviewer.sh.unpassable-ac`; PILOT:13 (9 files catfix'd); SPEC.md:38-39 | fixed 2026-11-11 after c1 reported; findings already dropped before fix not restored (COMBO-REPORT:72) |
| H3 | `source.md` not shipped: plan `candidate.md` references `./source.md`; terra/sol returned "incomplete"; luna 25/25 empty on affected packages (SPEC.md:103) | SPEC.md:90-91, 102-103 | found 2026-11-12 (batch 4), fixed 12:59:34; all earlier luna data quarantined; brief still does not name the file (COMBO-REPORT:371) |
| H4 | `expected_model` overwritten by fallback so `model_ok` passes after silent model swap; cyclic ladder spun 69 steps in 3 s | SPEC.md:141; `run-reviewer.sh:76` (`MODEL="$NEXT"`) | batch 9; ladder fixed, audit A checks expected vs intended |
| H5 | `claude` binary replaced/missing mid-run (exit 127 "native binary not installed"): 22:17-22:19 batch 9; 23:05 (20 judges rc=127); 00:35 batch 10; 13:48:51 batch 11 | SPEC.md:141,147,152; COMBO-REPORT:247,422 | treated as model failure; reruns with NOFALLBACK=1; no infra-outage classification |
| H6 | Gateway identity bleed under load (muse-wonder-1.0 served as gpt-6.1-terra at 12 concurrent workers; init/billing say muse but assistant message is terra); glm served as qwen3.8-max (~08:25 UTC Nov 12); muse-wonder/spark/wonder-full misroute | SPEC.md:78,81-82,87-88,116-117,131 | detected by observed `assistant message.model`; cooldown 60-90 min |
| H7 | Blocking-count parser grep `"blocking":true` without space undercounted | COMBO-REPORT:105; `stats.sh:14` now space-tolerant | corrected 2026-11-12 15:20 UTC; all earlier per-model blocking numbers WRONG |
| H8 | Judge API error left a plausible `score.json` (8 rows/6 blocking/8-of-10 GT) that was published as best result | COMBO-REPORT:146-148; `judge-one.sh:7` skip-if-exists; files `score.json.invalid-apierror`, `judge.json.invalid-apierror` | retracted 16:55 UTC; 48 -src judges audited |
| H9 | Judge "blocking" = matched by blocking-flagged row, ignoring `blocking_in_implement` (65 judge vs 38 real over 71 rows) | COMBO-REPORT:291; `judge-one.sh:19` | audit F; tables now show both |
| H10 | `attrib.py` credited every reviewer on a merged row; doubling conclusion retracted | COMBO-REPORT:195-198 | retracted |
| H11 | Stale merges (report re-run after merge; n2-terra x3, r2-sol design, n5-sol/n5-terra) because merge scripts skip when `merged-1.md` exists | merge-b6.sh:18; audit-D:23-25 | audit D; excluded |
| H12 | Row naming hides composition: r2 treated as muse row; "valid-era" chosen by row-name regex | COMBO-REPORT:170-174; final-table.py `valid()` | retracted 19:05 UTC |
| H13 | `cost.json` over-counts 5 runs (stale `attempt2` leftovers) and counts WebFetch aux call (~512 tokens) | audit-A:15,22 | disclosed |
| H14 | `BLOCK_OK` = fence-presence grep only; a block whose lines all fail validation passes the harness | `run-reviewer.sh:57` | not fixed |
| H15 | Hard-coded absolute paths (E2 worktree, `/tmp/evalsb`, `/tmp/*.tsv`); scripts need raw transcripts to rerun | all tools/analysis scripts | not fixed; README warns (tmp-scripts/README.md) |
| H16 | Reviewer brief states anchor limit but not the 300-char claim cap | `run-reviewer.sh:17`; rules file :60 | not fixed |
| H17 | Reviewer isolation relies on snapshot content; `bypassPermissions` + Bash + /tmp writable; WebFetch available (audit-A E2) | probe.json `sandbox_write`; run-reviewer.sh:48 | disclosed; old-era runs browsed sibling plan packages (COMBO-REPORT:293) |
| H18 | Pilot arms use random-drawn composition per package (arm B designSpec = sonnet, muse-spark, glm; design = sonnet, glm, glm): arms differ across packages | resolution-*.json | disclosed in PILOT table only |
| H19 | `README.md` lists `checks-gate8` as key script; file absent from `tmp-scripts/` | tmp-scripts/README.md; ls-tree | [UNVERIFIED missing] |

### 11.3 Reviewer-model behaviour findings (not defects of code)
- terra/sol: returned "incomplete" reports even after source.md shipped: 51 reports incomplete, 16 empty terra valid-era reviews (COMBO-REPORT:294); standalone terra 7,241 tok / 182 s and sol 11,588 tok / 410 s, each 1/14, 1/8, 3-4 wrong blockers.
- luna: thin (30-295 s, 1.4k-14k tokens pre-src; 4.7k avg tok/run src era, combo-est-self:11), anchor fidelity 91.4% vs 98-100%, 30 findings dropped at merge; 49 of 222 runs never referenced source.md.
- ember: 81 of 209 runs (39%) never referenced source.md; 33 findings dropped at merge.
- wonder: 14 findings dropped at merge; exhausted weekly limit.
- haiku: workhorse, 1085/1108 findings kept; noisy (8.3-8.6 findings/run).
- grok: slow (600-980 s; 845 s avg wall), ~54k tokens/run, only source of designSpec GT6; reports gateway id `grok-4.7-build` (benign).
- sonnet: highest coverage per run, rarely marks blocking (0.26-0.28 claims/run), 0 findings dropped, read source.md in all but 1 of 63 runs.
- glm-5.3: slow (805-1435 s), mixed `glm-5.3,qwen3.8-max` observed in 7 attempt1s; excluded.
- Qwen3.8-max: 0 output tokens, 3000 s timeouts in pilot; excluded.

## 12. Overlap with E1 and E3 evidence (for the overlap matrix; only facts verified in this slice)

| Item | E2 (A1 @6c09843) | E1 (this branch HEAD 50d4d2b9d) | E3 / master |
|---|---|---|---|
| Plan reviewed | designSpec `candidate.md` sha256 044809e3... (200 lines) | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` same sha256 (sha256sum on both) | plan archived under `.dev/tasks/done/<pkg>/` at HEAD and tip |
| Spec / source input | `source.md` copied from `.dev/tasks/done/<pkg>/source.md` (batch 4 onward) | `.../input/.../source.md` sha256 a865f397... = `.dev/tasks/done/TASK-WF-designSpec-20261107-075614/source.md` at HEAD | same file |
| Ground truth | `ground-truth.json` (sha256 3e56551d... = manifest.md:14) | `shadow-model-combos/combos.json` input.ground_truth = `git show b4db265a8:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/TASK-WF-designSpec-20261107-075614/ground-truth.json`; file at b4db265a8 is byte-identical to tip (`cmp`); b4db265a8 is an ancestor of the tip, NOT of HEAD | |
| Runs | 890 reviewer runs in 70 rows (audit-A:3) + pilot arms; 3 packages | `results.jsonl` 15 runs (combos A-E x 3 repeats, designSpec only), `results.md` shows cost USD 11.88-50.25 and 93,616-367,381 out tokens per run | |
| Dispatch | raw ids via `claude -p --model` in a sandbox repo (D1) | `/sc:reflect --mode pre ... ` pipeline (combos.json `common.prompt`; truncated in my read) [dispatch internals not read in this slice] | product gateway env: no dispatch defined (P7) |
| Findings schema | findings-v1 via `/sc:spec-panel` brief | findings-v2 container reusing v1 limits (`findings_v2.py:14-21`) | findings-v1 (`findings.py`) |
| Verdict logic | `superclaude review merge` ledger | reflect kernel (other slice) | `ledger.py` |
| Common failure class | brief lacks heading/limits -> reviewer block unparseable (c1 haiku missing `## Findings block` heading, 15 findings dropped; PILOT:78) | `c2e3347d3 fix(reflect): reviewer brief names the exact findings heading` | rules file :58-60 |
- A1 is byte-identical at run-1 commit 4a22d74 and tip 6c09843 (`git diff --stat 4a22d74..6c09843 -- A1` empty; 9,312 files both); later tip commits (d561461fa, fd69a006d, c2ddeb1b4, 6c0984326 "untrack 96 raw claude transcripts that were committed by mistake") do not change A1.
- `git merge-base HEAD 6c09843` = `ec259f1b7` (= `origin/master` sha in manifest.md:6, so both efforts forked from the same master commit).
- b4db265a8 (E1's pointer) is the first E2 push, "docs(eval): tasklist review panel model-combination study (#346 live gateway models)", containing 8,814 A1 files; A1 grew to 9,312 by 4a22d74 (`git diff --stat b4db265a8..4a22d74 -- A1` = "500 files changed, 26801 insertions", e.g. tools/tmp-scripts/stats.sh +18). E1's `combos.json` carries `"status":"designed, not run"` although `results.jsonl` holds 15 published runs [stale status field in E1].

## 13. Lessons (each with source; L = lesson)

| # | Lesson | Source | Applies to |
|---|---|---|---|
| L1 | A panel's result is dominated by input delivery, not model choice: the missing `source.md` made luna/terra/sol "incomplete" and was first read as a model finding; "all panels sit at about 2-2.5 of 14, so the harness fixes ... remain the biggest lever" | COMBO-REPORT:132,371,428; SPEC.md:90-91 | core: input manifest per review (list every file shipped, name it in the brief, verify the reviewer opened it) |
| L2 | Verify "model ran" by the OBSERVED assistant model, not init/billing/alias; identity can bleed at high concurrency; fallback must never overwrite the expected id | SPEC.md:81-82,141; run-reviewer.sh:51,56,76; audit-A:7 | core dispatch + served-model record (E1 already records "distinct served reviewers", results.md) |
| L3 | A fallback ladder needs a visited set, an exclude list, and a no-fallback switch; instant failures can loop it | SPEC.md:141 | core dispatch |
| L4 | Silent normalisation hides data loss: invalid finding lines dropped at merge flipped verdicts; need per-reviewer dropped count by reason, with ids and blocking flags, in the merged report | COMBO-REPORT:292; audit-D:16-20 | core merge/ledger |
| L5 | Treat reviewer `findings` limits as a contract the reviewer is told AND the parser tolerates: anchors told "12 to 200" were still >200 in 74 findings (56 + 18); claims >300 in 14 | audit-D:16; rules file :60 | core finding contract |
| L6 | Single-run rows are noise: same nominal panel varied 4/14 -> 2/14; judge corrupted once; rank only on replicates (4+ runs) | COMBO-REPORT:172,200,361,424 | evaluation method |
| L7 | Never read a metric's definition from a column name: judge "blocking" ≠ `blocking_in_implement` (65 vs 38) | COMBO-REPORT:291 | evaluation method + reviewers' blocking rubric |
| L8 | Mechanical correctness checks (parser, attribution, count regex) needed independent re-derivation; agent-built tables must be cross-checked by script (0 mismatches of 320 / 62x16x2) | COMBO-REPORT:105,195,386,431 | verification pattern |
| L9 | Publish retractions in place and keep a "supersedes" pointer; the file has 4 headed CORRECTION blocks (:104, :146, :169, :195) plus the audit-driven FINAL section (:289-373) and a correction note at :373; stale text remained (audit F item 7, :297) | COMBO-REPORT:104,146,169,195,291-297 | documentation discipline: one results file per decision, regenerate from data |
| L10 | Judge mid-run failure may leave a plausible output: validate completion marker + schema; do not skip on file-exists | judge-one.sh:7,28; COMBO-REPORT:146-148 | core scoring |
| L11 | Quarantine, never delete (`*-contaminated-20261111`, `quarantine-*`, `*.invalid-apierror`, `-superseded-`): 592 + 378 + 91 + 8 + 2 paths in tree | `ls-tree` counts | evidence retention |
| L12 | Read composition from `meta.json`, not row names (r2 mislabelled as muse) | COMBO-REPORT:170-174 | measurement |
| L13 | Concurrency: 8 parallel verified in probe; 12 workers broke identity; 10 with muse cap 4 ran clean | probe.json `max_parallel_tested`; SPEC.md:78,99 | core dispatch scheduling |
| L14 | Cheap reviewers (luna, terra, sol, ember) are noisy blockers: 3-4 wrong blockers each; sonnet quiet (0.17-0.25 wrong blockers/run) but rarely blocks | attrib.out:3-12; combo-est-B.md:19-21 | panel composition: blocker role vs coverage role |
| L15 | Second same-model reviewer: only supported effect is luna x2 raising control GT2 detection (+0.83, p 0.004 Welch / 0.048 permutation); per-reviewer chance to raise control GT2 single run: grok 7/8, wonder 8/9, terra 4/6, sonnet 6/9, luna 13/22, haiku 4/13, ember 4/13 | COMBO-REPORT:199,298 | panel composition |
| L16 | Defects no model reached (B1, B2, I5, I6; B6 once) point at the brief/package/GT, not the model mix | COMBO-REPORT:287,501 | reviewer rubric / GT quality |
| L17 | The strongest pilot signal was negative: single arm A PASSED both defect-rich packages with 0/8 blocking recall (no source.md); decision rule passed only by exactly 2x | PILOT:58-61,71 | gate calibration |
| L18 | Row-name-based filters ("valid-era") are fragile; keep an explicit manifest of valid rows | final-table.py `valid()` | measurement |
| L19 | Owner ordered unusual constraints mid-study (exclude glm, Qwen; no Fable/Tier 0; no worktrees for workers): keep exclusion as data (per-run record), not env defaults | SPEC.md:35-36,98; run-reviewer.sh:69 | core panel policy |
| L20 | Wall time of a panel is the slowest reviewer (grok 600-980 s; glm 805-1435 s), tokens do not predict wall; report "reviewer-s summed" and "elapsed" separately | COMBO-REPORT:204 | measurement/cost model |

## 14. What the study does NOT show (use as limits in the report)

1. Anything about the product `superclaude review` panel as shipped: all panels were hand-assembled raw-id `claude -p` runs merged by the product `review merge` CLI; the pilot arms B/C approximate `@default`/`@live7` minus Qwen.
2. Any result for more than 3 packages, any held-out package, any package type other than /sc:workflow tasklists (candidate.md + source.md) (n = 16 GT defects, 8 blocking). Not spec review, not code review, not reflect UC-2, not PR review.
3. Real gate accuracy: GT = defects observed in past implement runs by one observer (plans where the plan caused a block); false-positive burden on clean plans is measured only through "wrong blockers" against a non-clean control; there is no clean-plan control.
4. Cost in money: only reviewer output tokens and wall; input tokens, cache, judge cost per combo not combined (judge cost only for the pilot, PILOT:52). E1 reports USD per run (results.md), E2 does not [UNVERIFIED in collab].
5. Effect of the harness fixes (source.md named in brief; anchor truncation) on catch: unrun.
6. Sonnet-alone with source.md (arm A re-baseline): unrun, so the "no panel beats arm A" claim is pre-source.md (combo-est-self.md:23).
7. Judge reliability beyond a 12-row blind re-judge (12/12) and 19/19 catches confirmed; no inter-judge agreement; one judge model (claude-opus-5-5) for all rows.
8. Whether panel verdict (PASS/FAIL) agrees with implement outcome beyond qualitative remarks (COMBO-REPORT:60).
9. Statistical power: 4-6 replicates per replicated panel; most rows n=1 (anecdotes, COMBO-REPORT:361); after audits only three statistical effects survive (second luna control +0.83; 2x luna + 2x ember more wrong blockers; ember + terra worse).
10. Re-review rounds (round 2/3), reviser loop, ledger convergence: every ledger has `rounds = [1]` (audit-D:3). The study is first-round only; #346 loop dynamics (E3) are not measured.
11. Adversarial/debate merge vs ledger merge: not compared (E1 uses adversarial Mode A; E2 uses ledger clustering).
12. Reflect-style deviation findings (E1 UC-2 taxonomy) and `findings-v2` channels: not exercised.
13. Whether reviewers could write to disk or use web: audit-A shows WebFetch aux calls in 57 runs; effect on findings not assessed.
14. Order/seed effects of random tier draws in product templates: resolution fixed once per package (D1).

## 15. Value inventory: every item of this slice mapped to a destination

Destination codes: CORE-CONTRACT (finding schema, limits, categories, completion state) | CORE-MERGE (ledger, clustering, verdict, drop reporting) | CORE-DISPATCH (model launch, identity check, fallback, timeouts, concurrency) | CORE-PANEL (tier models, templates, exclusions, composition policy) | CORE-INPUTS (input manifest/sandbox) | CORE-SCORE (GT, judge, metrics, audits) | MOD-TASKLIST / MOD-REFLECT / MOD-SPEC / MOD-PR / MOD-RFQA (thin modules) | EVAL (keep as eval tooling outside runtime) | ARCHIVE (evidence only) | DROP.

### 15.1 Findings and numbers
| # | Item (source) | Destination |
|---|---|---|
| V1 | Source-input omission explains terra/sol/luna "incomplete"; with source.md panels FAIL-heavy (SPEC:90-91; COMBO-REPORT:132,148) | CORE-INPUTS (input manifest + brief names each file + "opened?" check); MOD-TASKLIST |
| V2 | 156 of 665 valid-era runs never referenced source.md (ember 81/209, luna 49/222, wonder 6/25, haiku 15/75, grok 4/24, sonnet 1/63, terra 0/44, sol 0/3) (COMBO-REPORT:373) | CORE-INPUTS (acceptance gate: reference check) |
| V3 | 92 dropped findings (anchor>200 56, anchor2>200 18, claim>300 14, severity 3, refs 1), 49 blocking, 80 reviewer cases, 3+ verdict flips (audit-D:16-20) | CORE-CONTRACT (limits, truncate vs reject) + CORE-MERGE (report dropped ids) |
| V4 | 83 megacluster rows; 195/1398 chain rows (audit-D:29) | CORE-MERGE (clustering rule review) |
| V5 | 46 rows null span, 13 blocking (audit-D:30) | CORE-CONTRACT (anchor verbatim check at parse) |
| V6 | Real blocking 38 of 65 judge-blocking over 71 rows (COMBO-REPORT:291) | CORE-SCORE (metric definition) + CORE-CONTRACT (blocking rubric) |
| V7 | Final panel guidance: default ember+2luna (64k tok, 1.83/14, 0.17 real blk, control 0.83); quality tier sonnet+2luna (139k, 2.33/14); haiku+2luna best real blocking 1.2/8; best precision ember+sonnet (0.25 wb); do not use ember+terra, 2ember+2luna, terra/sol alone, 5-reviewer panels (COMBO-REPORT:363-369,428) | CORE-PANEL (candidate defaults; label PROVISIONAL, 3 packages, same effect size ~2-2.5/14) |
| V8 | Statistics surviving audit: luna x2 control +0.83; 2luna+2ember more wrong blockers; ember+terra worse (COMBO-REPORT:298) | CORE-PANEL (composition rules) |
| V9 | Ceiling/reach: B1, B2, I5, I6 never caught in 106 runs; B3 95, I8 76, I2 71 of 106 (COMBO-REPORT:497,501) | CORE-SCORE (GT quality review; test whether brief/package/GT) ; MOD-TASKLIST reviewer rubric |
| V10 | Pilot: arms A/B/C 2/16, 3/16, 4/16; 0/8 blocking recall; A passed both defect-rich pkgs (PILOT:46-50,71) | ARCHIVE (pre-source.md); CORE-SCORE baseline needing re-run |
| V11 | Efficiency table (catches/100k) and ranking tables batches 1-3, 4/5, 6, 7 | DROP (superseded by :289; contain retracted numbers) except as ARCHIVE |
| V12 | Per-model profile: tokens/run, findings/run, blocking claims/run (combo-est-self:3-12; combo-est-B:7-16) | CORE-PANEL (cost model inputs) |
| V13 | Per-model identity risks: muse served as terra; glm as qwen; wonder/spark/wonder-full misroute (SPEC:78-82,87-88,116-117,131) | CORE-DISPATCH (observed-model gate; stand-in/degrade-loud rule) |
| V14 | Gateway concurrency limits (8 tested; 12 broke; 10 with muse cap 4) | CORE-DISPATCH (scheduler cap per model family) |
| V15 | Qwen3.8-max 3000 s timeouts, 0 tokens; glm 805-1435 s; grok 600-980 s | CORE-DISPATCH (per-model timeout/cost classes) ; CORE-PANEL (exclusion data) |
| V16 | terra/sol "incomplete" even with source: 51 reports, 16 empty terra | CORE-PANEL (role: not a standalone reviewer), CORE-DISPATCH (empty-report retry) |
| V17 | Judge process (blind Opus, anonymized, label key, API-error audit, 12-row re-judge 12/12 exact, 19/19 catches) | CORE-SCORE / EVAL |
| V18 | Fixed decision rule written before scoring (PILOT:56) | CORE-SCORE (pre-registered rule pattern) |
| V19 | Statistical conventions used (permutation, Welch, Fisher; "beyond noise" flagged; ranges) | CORE-SCORE |
| V20 | Control package GT2 per-reviewer hit rates (grok 7/8 ... ember 4/13) | CORE-PANEL (keyword proxy only; ARCHIVE) |

### 15.2 Scripts, tools, artifacts
| # | Item | Destination |
|---|---|---|
| T1 | `tools/run-reviewer.sh` (87 lines): observed-model check, findings-block presence check, 2 attempts, cost.json, fallback ladder v3, NOFALLBACK, EXCLUDE_MODELS, per-run meta | CORE-DISPATCH: re-implement in product code (python), keep contract: expected vs observed, attempts, tokens, wall, fallback log; fix H4/H14/H16; drop hard-coded paths |
| T2 | Brief text in `run-reviewer.sh:13-17` (spec-panel critique + first-review rules + findings-v1 spec) | CORE-CONTRACT/MOD-TASKLIST: single source = rules file (`document_review_loop_prompts.md`); delete the copy |
| T3 | `run-reviewer.sh.bad-launch`, `.unpassable-ac` | ARCHIVE (evidence of H1, H2) |
| T4 | `judge-one.sh`, `run-combo-judges.sh`, `gen-judge-list.sh`, `anon-*.sh` | CORE-SCORE: keep design (blind label, anonymize ids/paths/model names, GT-only judge); fix skip-if-exists, success test, blocking definition; paths parameterized |
| T5 | `merge-b6.sh` + `merge-b7..b11.sh` (hand-built resolution + `review merge` + stale-r1 retry) | EVAL; DROP once CORE-MERGE supports idempotent re-merge |
| T6 | `b4-job-one.sh` (cancel sentinel), launchers `b7..b11-launch.sh`, `startcombo*.sh`, per-batch runners (n*, r*, c*, g*, h* runners) | DROP (one-off); keep concept of cancel sentinel and xargs -P caps in CORE-DISPATCH |
| T7 | `final-table.py`, `b8-table.py`, `b9-table.py`, `three-way.py`, `untried.py`, `attrib.py`, `doubles.py` | EVAL: keep `final-table.py` logic (real vs judge blocking, exclude flags); DROP attrib.py/doubles.py (retracted method) |
| T8 | `analysis/audits/audit-A..F` scripts (identity/attempts, validity, inputs/timing, merge integrity, scoring integrity, aggregation) | CORE-SCORE: make audits A (identity), C (input referenced), D (merge integrity) runtime/CI checks; E/F eval-only |
| T9 | `analysis/issue-table`, `analysis/allsets` agent-built tables + independent script | EVAL (verification pattern) |
| T10 | `combo-est-A/B/self.md` untried-combo estimates | ARCHIVE (unverified predictions; no run) |
| T11 | `probe/probe.json` model probe (alias findings, 8 parallel, `sandbox_write`) | CORE-DISPATCH (probe procedure: zero-load assistant-model probe before panel) ; ARCHIVE data |
| T12 | `tools/tmp-scripts/snap.py`, `drift-b3.py` (E1 helpers hash input tree: `input_tree_sha256`) | CORE-INPUTS (input snapshot hash pattern, shared with E1) |
| T13 | GT files (`ground-truth.json` x3, `-draft.json`, verification block `quote_grep_count`, `evidence_ok`, `dropped` with reasons) | CORE-SCORE (GT schema + evidence verification + dropped reasons) ; the 3 sets are shared with E1 |
| T14 | `resolution-default/live7.json` per package (schema review-panel-resolution/1, template/tiers sha256) | CORE-PANEL (provenance fields) |
| T15 | `combos/<row>/{ledger.json,merged-1.md,resolution.json,merge-stdout.txt}` x 95 rows; `arms/scoring/**/score.json` 318; `label-key.json` 309; `merged-anon.md` 319 | ARCHIVE (replay data for CORE-SCORE regression fixtures) |
| T16 | `reviews/combos/**` reviewer reports (`*.md`), `meta.json`, `cost.json` (1,263 each) | ARCHIVE; sample for reviewer-output fixtures (anchors >200, missing heading, incomplete reports) |
| T17 | `quarantine-pre-src-luna/` (417 files), `*-contaminated-20261111` (592 paths), `*-superseded-*` (378 paths), `quarantine-outage-20261113` (91), `reviews-failed-launch-1` (154 files total = 56+49+49) | ARCHIVE (negative fixtures for dispatch/identity tests) |
| T18 | `RAW-TRANSCRIPTS-NOT-COMMITTED.md` (1.48 GB, 2,916 files off-repo) | ARCHIVE; policy: transcripts stay off-repo, derived data committed |
| T19 | `COMBO-REPORT.md`, `PILOT-REPORT.md`, `manifest.md`, `combos/SPEC.md` | ARCHIVE + extract V1-V20, L1-L20; do not cite pre-:289 tables |

### 15.3 Tests (none in A1; product tests relevant at HEAD)
| # | Test | What it pins | Destination / impact |
|---|---|---|---|
| X1 | `tests/review/test_review_findings.py:113,117` | anchor 201 and claim 301 chars make block invalid | CORE-CONTRACT: changing limits/truncation must update these |
| X2 | `tests/review/test_review_findings_v2.py:199-200,241` | v2 anchor 200/201 and claim 300/301 | same; E1 reflect shares the limit |
| X3 | `tests/review/test_review_ledger.py:364-373` | merge refused when no valid block | CORE-MERGE keep |
| X4 | `tests/review/test_review_ledger.py:376-385` `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` | one valid block suffices; invalid reviewer reported via `block_ok` + `warnings` | pins P6 as DESIGN; a quorum rule would change it |
| X5 | `tests/review/test_review_ledger.py:388-393` | round cannot be merged twice or out of order | pins P5 as design |
| X6 | `tests/review/test_review_panel_live7.py`, `test_review_panel.py`, `test_review_panel_exclusion.py` (K1 hard exclusion, strict distinctness, frozen tiers golden) | live7/default composition, exclusion golden | CORE-PANEL: study's exclusions (glm, Qwen) are not product exclusions [UNVERIFIED what K1 excludes: Fable classes seen in `panel.py:149-152`] |
| X7 | `tests/review/test_review_rules_text.py:67-68` | rules prompt wording of the findings block | CORE-CONTRACT: brief single-source change must update |
| X8 | `tests/review/test_review_card_convert.py:426` | reflect category map `acceptance -> unpassable-check` | MOD-REFLECT |
| Missing | No test pins: dropped-finding report content; model-identity gate; fallback visited set; input-manifest presence; judge completion | CORE-* new tests required |

## 16. Future-use-case exposure list (what this slice implies for each consumer)

| Use case | What E2 evidence exposes | Required in shared core |
|---|---|---|
| sc:reflect (UC-1/UC-2 Tier 2) | findings-v2 reuses 200/300 limits (P10) so silent drops apply; reflect profile launch limited to sonnet/opus/haiku, max 3 reviewers (C13) while E2's best panels use luna/ember/terra/grok; E1 already records served-reviewer count but not model-identity bleed; E1 and E2 share the designSpec plan + GT | one contract + one dispatch with observed-model gate; reflect profile must state its dispatch limits explicitly |
| sc:workflow tasklist review (E2's native use) | source.md must be shipped and named; first-round only; real blocking recall about 0.2-1.2 of 8 per panel; GT B1/B2 never found; sonnet quiet/rarely blocks | brief names inputs; reviewers' blocking rubric; GT-driven acceptance harness |
| Spec review (brainstorm/design; `/sc:spec-panel` is the brief's entry) | E2's brief literally starts `/sc:spec-panel @<cand> --mode critique` so reviewers are spec-panel sessions; only candidate+source roles; no re-review loop measured | findings-v1 inputs role list (`findings_v2.ROLES = plan, spec, source, test, diff, artifact`) as the manifest vocabulary |
| PR code review (later) | diff anchors may exceed 200 chars (luna/ember/wonder lost 30/33/14 findings); code anchors are not whitespace-flat; hunk-based clustering not tested; web/Bash tool access in reviewers (audit-A E2) is a risk for untrusted diffs | anchor policy (truncate vs reject), per-run tool policy, sandbox content policy |
| rf-qa replacement | agent-built tables + independent script cross-check (0 mismatches) is the reusable QA pattern; audits A-F = QA of the QA | audit scripts as runtime checks (identity, input-referenced, merge-integrity) |
| Model-combination experiments (E1 follow-ups) | harness defects H1-H19 will recur; dispatch undefined in gateway env (P7); gateway outages (identity bleed, `claude` binary replacement) need an infrastructure-outage class distinct from model failure | classify exit 127 / "native binary" as outage, not as model failure; cooldown + probe procedure |
| Cost governance | reviewer tokens only; ember+luna 52k tokens vs sonnet+ember 143k vs r2 594k; wall: grok 845 s avg; judges 1.03M output tokens for 9 pilot judges (PILOT:52) | cost/wall record per reviewer and per panel in the ledger |
| Security / isolation | `bypassPermissions` + Bash + WebFetch in reviewers; sandbox = archive snapshot minus history dirs; old-era runs browsed sibling plan packages | sandbox contract: read-only content set, no network unless needed, record tool calls |
| Evaluation governance | pre-registered decision rule, blind labels, replicates ≥4, audits, retraction hygiene | eval protocol document for the central panel |

## Summary

- Scope read: A1 top-level reports (PILOT-REPORT 83 lines, COMBO-REPORT 506 lines, manifest 16 lines), `combos/SPEC.md` (152 lines), `tools/` (3 harness files + 55 tmp-scripts; read run-reviewer.sh in full, both old copies by diff, judge/anon/merge/stats/snap/drift scripts, README), analysis summaries (audit-A, audit-D, combo-est-*, attrib/doubles/final-table headers), GT json (3 packages), resolutions, probe.json. Tree: 9,312 files, identical at run-1 commit 4a22d74 and tip 6c09843; raw transcripts (1.48 GB, 2,916 files) off-repo.
- Study design: 3 packages (designSpec 10 GT/5 blocking, alias 4/3, design control 2/0), 16 GT defects total, 8 blocking; 106 scored runs in 62 sets (+ batch 10 dropped); 890 reviewer runs audited; blind Opus judging.
- Headline result (FINAL, COMBO-REPORT:289-428): all panels sit at about 2-2.5 of 14 defect-rich defects; real blocking recall 0.17-1.2 of 8 for replicated panels; no panel catches designSpec GT1, GT2, GT10, alias GT4 (B1, B2, I5, I6 never found in 106 runs); sonnet+2xluna NOT confirmed as standard (replicated n=6: 2.33/14, 4/14 was an outlier); recommended default ember+2xluna (64k tokens, 1.83/14); harness fixes (anchor limit, source.md in brief) named the biggest lever and not done.
- Biggest finding for a central panel: input delivery and parse contract dominated model choice: missing `source.md` (until 2026-11-12 12:59:34), 92 findings dropped at merge (49 blocking, 3+ verdict flips), 156 of 665 runs never opened source.md.
- Code cross-check (17 items): `unpassable-ac` was a HARNESS brief typo (rules file and CATEGORIES say `unpassable-check`); silent-drop is real but not "no error" (warning + `block_ok` exist, first error only) [CODE-CONTRADICTED on wording]; clustering chains verified; gateway env has no dispatch for non-first-slot models (`launch: {}`, "dispatch mechanism per model not defined yet."); reflect profile launch limited to sonnet/opus/haiku, max 3 reviewers; findings-v2 inherits 200/300 limits; tests pin 201/301 invalid and "one valid block is enough".
- Cross-effort: E1 and E2 reviewed the byte-identical designSpec plan (sha256 044809e3...) with the same `source.md` (a865f397...); E1's combos.json scores against E2's GT at b4db265a8 (identical to tip); E2 tools/tmp-scripts contain two E1 helpers (snap.py, drift-b3.py). Both efforts forked from master `ec259f1b7`.
- Pilot table recomputed from score.json: 9/9 cells match. Not recomputed: COMBO-REPORT master tables, audits B/C/E/F headline numbers.
- Counts: 17 code claims checked (section 9), 13 decisions made (10.1), 8 open (10.2), 10 product-code defects (11.1), 19 harness defects (11.2), 20 lessons (13), 14 not-shown items (14), 20 value findings + 19 artifact rows + 9 test rows with destinations (15), 9 future-use rows (16).

## Gaps and Questions

### Gaps (not checked or not checkable)
1. [UNVERIFIED] Audits B, C, E, F headline numbers (51 incomplete reports, 16 empty terra; 156/665 no source.md; 294 clean judges, 12/12 re-judge; 65 vs 38 blocking): only audit-A and audit-D have a `summary.md`; I read those two and cross-checked D's mechanism against code; B, C, E, F rely on COMBO-REPORT text.
2. [UNVERIFIED] Master tables in COMBO-REPORT (:17-43, :114-130, :303-337, :388-399, :433-498) not recomputed from the 318 `score.json` files; only the 9 pilot cells were recomputed. Raw judge/reviewer transcripts are not in the commit, so scoring cannot be replayed.
3. [UNVERIFIED] Whether `muse-ember-1.0` exists in the product tiers file after HEAD (tier4 = luna, haiku, grok at HEAD); E2 says owner is adding it "as Tier 04 Model 02" (SPEC.md:120; run-reviewer.sh:26-27).
4. [UNVERIFIED] Which Qwen count is right (4 reviewer ids in resolutions vs "3 slots" in PILOT:12 vs "3 of 4 runs" in SPEC.md:3).
5. [UNVERIFIED] Quarantine counts: COMBO-REPORT:107 "428 reviewer files, 10 combo-row merge sets" vs SPEC.md:103 "428 ... + the 9 luna-bearing combo rows" vs tree 417 files total (10 `_combos` RESULT.md found).
6. [UNVERIFIED] Verdict flip count: 3 enumerated (audit-D:20) vs "Four" (COMBO-REPORT:292).
7. [UNVERIFIED] Whether the 54 of 319 `merged-anon.md` files naming model ids leak reviewer identity: sampled hits are alias-package plan content; not classified for all 54.
8. [UNVERIFIED] `tmp-scripts/checks-gate8` named in README but absent from the 55-file list.
9. [UNVERIFIED] E1's dispatch internals (`combos.json` `common.prompt` truncated in my read; E1 slices cover it).
10. Grep scope slip: one repo-wide grep (`unpassable-check|unpassable-ac`) printed file NAMES under the run-1 research directory `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/`; no content of those files was opened and nothing from them is cited here. Reported for the independence record.
11. Not read (per task): raw transcripts; per-combo `RESULT.md` (29 files), per-reviewer reports, `analysis/*.json`/`flags.tsv` bodies; `20261113-collab/` and `handoff-notes/` (other slices).

### Questions for the program owner / other slices
Q1. Should the central core keep the product limits (anchor <=200, anchor2 <=200, claim <=300) and truncate, or reject and re-ask the reviewer? 92 dropped findings (49 blocking) in 890 runs say the current drop-and-warn path loses real blockers; E1's findings-v2 inherits the same limits (C14).
Q2. Is `block_ok:false` + kept findings + "one valid block is enough" (pinned by `test_review_ledger.py:376-385`) the intended quorum rule for a central panel, or should a minimum number of valid reviewers be required?
Q3. Which dispatch mechanism will the gateway environment use for non-first-slot models (`review-tiers.default.json:26` "not defined yet"): raw `claude -p --model <id>` as in E2, the Agent tool (enum sonnet/opus/haiku/fable, probe.json), or the reflect launch list? Reflect profile validation (`panel.py:71-73,153`) currently rejects anything but sonnet/opus/haiku.
Q4. Are glm-5.3 and Qwen3.8-max permanently excluded for panels (study decisions D4/D5), given the product `tier3` contains only these two and `@default`/`@live7` draw 2 tier-3 reviewers?
Q5. Should the arm-A (sonnet alone, with source.md) baseline be re-run before any panel is called better or worse than a single reviewer (combo-est-self.md:23)?
Q6. Is E2's GT (16 defects from past implement runs, one observer) accepted as the shared ground truth for E1/E2/E3, or does the central design need its own held-out set and a clean-plan control?
Q7. Should the brief name every shipped input and the harness verify the reviewer opened it (156 of 665 runs did not)? Is that a core input-manifest feature or a per-module rule?
Q8. Do the E2 harness files (`run-reviewer.sh`, judge/anon scripts, audits A, C, D) become product/CI code, or stay as eval tooling under `.dev/eval-workspaces/`?
Q9. `[CODE-CONTRADICTED]` wording "discarded with no error" (COMBO-REPORT:292): should the study's report be corrected (a warning with first error exists), or is "no per-finding error" the intended meaning?
