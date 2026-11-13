# Hand-off: the tasklist Review Panel study, for merging with the reflect Tier 2 panel

**Date:** 2026-11-13. **Branch:** `ironbelly/eval-tasklist-review-panel` (remote `origin` = IronbellyOrg/IronClaude). **Last study commits:** `b4db265a8` (study), `2d06a4382` (batch 11 and issue tables). The hand-off commit is added on top of these; read it with `git show <final SHA>:.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification.md`.
**Reader assumption:** you have none of this session's context and cannot ask questions.
**Abbreviations:** `EVAL` = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`; `CR` = `EVAL/COMBO-REPORT.md`; `PR` = `EVAL/PILOT-REPORT.md`; `SPEC` = `EVAL/combos/SPEC.md`; `RV` = `src/superclaude/cli/review`. Product-code lines were read this session (2026-11-13); "UNVERIFIED" marks anything not re-read.
**Method note (honest scope):** the brief said "write only the report" and the standing rule is "change nothing under `.dev/tasks/`". So this report was NOT produced through the full tech-research task-file machinery (no task folder, no multi-gate QA fleet). It was produced by direct reading plus three read-only investigation agents (merge/ledger code, panel/telemetry/brief code, tests/tools). Findings below cite what was read; nothing was cross-checked by a separate QA pass.

---

## 0. One-paragraph summary

We built an evaluation harness and ran about 106 scored reviewer runs (62 distinct reviewer-model sets) to find which model panel best reviews a `/sc:workflow` tasklist plan. Result: every panel finds only about 2 to 2.5 of 14 known defects in defect-rich plans, no panel is statistically better than another except on cost, and four of the 16 known issues were never found by any run. The biggest levers are not model choice but harness and product defects: the merge step drops over-length findings (anchor over 200 characters, claim over 300), and the reviewer brief never names the driving source document, so reviewers cannot check the plan against its source. This branch changes **no product code** (`git diff origin/master...HEAD -- src tests` is empty); it adds only the study under `.dev/eval-workspaces/tasklist-review-panel/`. The product code under `RV` (generic, no tasklist-specific logic) is the thing to merge with reflect Tier 2.

---

## 1. Inventory

All study files are under `EVAL` unless noted. Status as of this report: **C-P** = committed and pushed; **UNCOM** = uncommitted (becomes C-P with the hand-off commit); **LOCAL-ONLY** = never committed by owner order. Reusable? **G** = generic to any review target, **T** = tasklist-study specific.

### 1.1 Product code (no changes on this branch; existing on master, read-only here)

| Artifact | What it is | Status | G/T |
|---|---|---|---|
| `RV/findings.py` (457 lines) | findings-v1 parser, anchor locate, clustering | on master | G |
| `RV/merge_cmd.py` (118), `RV/ledger.py` (494), `RV/ledger_cmd.py` (137) | `superclaude review merge`, review ledger state machine, `ledger revise/defer/verdict/capture` | on master | G |
| `RV/panel.py` (525), `RV/panel_cmd.py` (87) | panel template + tier file resolution into reviewers (`superclaude review panel resolve`) | on master | G |
| `RV/telemetry.py` (447), `RV/telemetry_cmd.py` (98) | JSONL telemetry records, SQLite loader, `model_scores` view | on master | G |
| `RV/data/review-panel.default.json`, `review-panel.live7.json`, `review-tiers.default.json` | packaged panels and tier-to-model table | on master | G (model ids are time-bound) |
| `src/superclaude/rules/prompts/document_review_loop_prompts.md` (74 lines) | the only reviewer brief in `src` | on master | G (spec-oriented) |
| Tests: `tests/review/*` (111 test functions) + 5 `tests/skills/test_*review*` files | see section 8 | on master | G |

### 1.2 Study documents (C-P)

| File | Purpose |
|---|---|
| `PILOT-REPORT.md` (83 lines) | arms A/B/C on 3 pilot packages, fixed decision rule |
| `COMBO-REPORT.md` (506 lines) | master report; **only lines 289-373 (final results), 375-383 (decision update, later rejected), 385-419 (top-10 issue table), 421-428 (batch 11), 430+ (all 62 sets) are current**; earlier tables are superseded (CR:297) |
| `combos/SPEC.md` (152 lines) | procedure, hard limits and an operations log for batches 2-11 (outages, contamination, quarantines, ladder fixes) |
| `manifest.md` | eval setup, ground-truth hashes, sandbox description |
| `analysis/audits/audit-A..F/` | six read-only integrity audits (identity, report validity, inputs/timing, merges, scoring, aggregation) |
| `analysis/issue-table/`, `analysis/allsets/` | per-issue-by-panel tables (top-10 panels; all 62 sets) with agent outputs and direct-script cross-checks |
| `analysis/*.py`, `merge-b7..b11.sh`, `b7..b11-launch.sh`, judge tsv/logs | aggregation, tables, permutation tests (`final-table.py`, `three-way.py`, `doubles.py`, `untried.py`) |
| `analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md` | explains what was left out |
| per-package `reviews/`, `combos/<row>/` (RESULT.md, `merged-1.md`, `ledger.json`, `resolution.json`), `arms/scoring/**/score.json` | the run data (reviewer reports, merges, blind scores) |
| `<pkg>/ground-truth.json`, `candidate.md`, `resolution-*.json` | per-package ground truth and plan under review (3 packages) |

### 1.3 Harness scripts

| Script | Purpose | Status | G/T |
|---|---|---|---|
| `tools/run-reviewer.sh` (current; `.bad-launch` and `.unpassable-ac` are old copies) | runs ONE reviewer in a fresh `claude -p --model <raw id>` session in a sandbox repo; 2 attempts; model-identity check; fallback ladder; writes `<id>.md`, `meta.json`, `cost.json` | C-P | **T** (hard-coded `/tmp/evalsb`, `/sc:spec-panel` brief, `source.md` path, packages) but the pattern is reusable |
| `tools/tmp-scripts/` (54 scripts plus a README, 220 KB, added by this hand-off at the owner's request) | the helper scripts that previously lived only in `/tmp`, copied verbatim: `b4-job-one.sh` (job runner with cancel files), `judge-one.sh` (blind judge prompt), `anon-*.sh`, `merge-b6.sh`, `arm-merges.sh`, `gen-judge-list.sh`, `merge-src-rows.sh`, `b5-jobs-gen.sh`, per-row runners (`n2*`, `n3`, `n4`, `n5*`, `r2*`...). Only files that reference this eval were copied; unrelated scratch from other sessions in `/tmp` was left out (a secret scan of what was copied was clean) | UNCOM at time of writing | T (patterns G) |
| `analysis/*.py` aggregation scripts | tables, permutation tests | C-P | mostly T (package ids, GT labels) |

`/tmp` held 70 `.sh` files; 12 were already in `analysis/` and the rest were copied if they reference this eval. A few `/tmp` files that did not match the eval-path filter were NOT copied (e.g. `checks-gate8.sh`, `r2terra-hb.sh`, `r3-hb.sh`, `snap-b3.py`, `mkcards-b3.py`, `r2cmp.py`); the investigation agent named `checks-gate8` as part of the study, so it is UNVERIFIED whether any of these is needed to reproduce a number. They remain in `/tmp` on the author's machine only.

### 1.4 Left out by owner order (LOCAL-ONLY)

3,041 untracked files under `EVAL` (about 1.48 GB of raw data): 1,380 `*.attemptN.json` (raw `claude -p` transcripts), 1,352 `*.attemptN.meta.json`, 309 other json including every `judge.json` (git status, 2026-11-13). Owner ordered these left out of both commits (`analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md`). The final per-run `meta.json` and `cost.json` ARE committed, so no reported number depends on the excluded files; the transcripts are only needed to re-audit what a model said. The tech-research brief says "commit every artifact": that conflicts with the earlier standing order, so the hand-off commit keeps them out and flags it in section 4 (open decision 6).

---

## 2. Findings

### 2.1 Study design (so the evidence can be judged)

- **Packages (3):** `TASK-WF-designSpec-20261107-075614` (10 known defects, 5 that blocked implementation), `TASK-WF-makeTheAliasOnly-20261105-051649` (4 known, 3 blocking), both "defect-rich" (14 known any, 8 blocking); `TASK-WF-design-20261108-041415` is the control (2 known, 0 blocking). Known defects ("ground truth") were observed in past `/sc:implement` runs of those plans, not invented (PR:7; ground-truth hashes in `manifest.md`).
- **Unit of run:** one reviewer model, one package, fresh `claude -p` session (`tools/run-reviewer.sh:48`), brief at `tools/run-reviewer.sh:13-17` (a copy of the repo brief, section 5). Reviewer outputs merged by `superclaude review merge` (generic code). Merged report anonymized (reviewer ids to R1..Rn, paths redacted), scored by one blind Opus judge per (row, package), prompt in `tools/tmp-scripts/judge-one.sh` (judge writes `score.json`: `gt_covered_any`, `gt_covered_blocking`, `wrong_blockers`).
- **Metrics:** "found /14" = defects caught at any severity on the two defect-rich packages (mean per run). "Real blocking /8" = judge-blocking AND the defect has `blocking_in_implement=true` (CR:291). "Wrong blockers" = blocking ledger rows with no ground-truth match (inflated by novel real finds, a structural bias, CR:75).
- **Eras:** `source.md` (the plan's source document) was first shipped to reviewers 2026-11-12 12:59:34. Only later runs are "valid era" (CR:373). Pre-`source.md` luna, terra and sol data is invalid and partly quarantined (`quarantine-pre-src-luna/`).
- **Scale:** 71 valid-era rows (213 row-packages), 62 reviewer-model sets over 106 scored runs including the 3 pilot arms (CR:431). Replicated panels have 4-6 runs.

### 2.2 Results, with sample size and strength of evidence

| # | Result | n | What it does / does not show | Checked by |
|---|---|---|---|---|
| R1 | Every replicated panel finds about 1.6-2.5 of 14 known defects; no panel is significantly better on found, real blocking, wrong blockers or control (permutation p 0.28-1.0). Only cost and time differ (tokens p 0.002-0.009). | 4-6 per panel | Shows model mix is not the lever at this sample size. Does not show panels are equal (underpowered). | audit F, CR:381, CR:425 |
| R2 | Four of 16 issues never found by any run (designSpec GT1, GT2, GT10; alias GT4) and alias GT3 found once. B3 (designSpec GT3), I2 (GT7), I8 (control GT2) carry nearly all catches. | 106 runs | The ceiling is not reachable by model mix; points at the brief, the packages or the ground truth. | CR:287, CR:419 |
| R3 | **Default recommendation:** ember + 2x luna (64k tokens, ~6 min elapsed, 1.83/14, real blocking 0.17, control 0.83). Optional quality tier: sonnet + 2x luna (n=6: 2.33/14, 139k tokens, ~14 min, control 1.33; reaches control issue I7 in 3 of 6 runs versus 0 of 6 for ember + 2x luna, Fisher p about 0.012, post-hoc and exploratory). Best measured real blocking: haiku + 2x luna (1.2/8, 191k tokens, but 3.0 wrong blockers). | 4-6 | Decision is a cost/reach trade-off, not a quality difference. The "sonnet + 2x luna is the standard" claim from n=1 was REJECTED by batch 11 (the 4/14 run was an outlier). | CR:363-371, 421-428 |
| R4 | Second luna in a panel raises control found by +0.83 (Welch p 0.004, permutation 0.048, baseline all zeros). 2x luna + 2x ember has 2.75-3.25 more wrong blockers than every comparator (p 0.005-0.03). ember + terra is worse by -1.75 found (p 0.029). These three are the only statistics that survived audit. | 4-6 | The earlier "second run of the same model adds nothing" claim was RETRACTED (CR:195) after the owner showed haiku + ember + luna 0/0 on control versus ember + 2x luna 1/1. | CR:298, CR:195 |
| R5 | The pilot (arms A sonnet alone, B, C) found 2/16, 3/16, 4/16 known defects, 0/8 real blocking recall for all three; sonnet alone PASSED both defect-rich plans. Arm C passes the pilot decision rule only by one defect. | 3 packages | Anecdotal. Pilot predates `source.md`, so it is the pre-source era. | PR:44-71 |
| R6 | Single-run high scores (grok + haiku x2 + sonnet 4/14, 3 real blocking, 594k tokens; haiku + sonnet + wonder 4/14, 311k) never replicated; the one near-replica scored 2/14. | 1 each | Treat as unconfirmed. | CR:370 |

### 2.3 Model-by-role findings (valid era unless noted)

| Model | Observed role | Evidence | Caveat |
|---|---|---|---|
| claude-sonnet-5-5 | The only model that never had findings dropped at merge and read `source.md` in every run (0 of 15 dropped, 1 of 63 runs missed `source.md`). Sonnet-bearing panels found 2.43 vs 1.92 found, 1.19 vs 0.68 control, 1.95 vs 2.68 wrong blockers over 21 sonnet rows. Its added reach is mostly the control issue I7. | CR:382-383, 427, 373 | Pre-source era: "sonnet is the only addition that contributes findings" (CR:101); the effect is smaller once luna/ember have `source.md`. |
| gpt-6-luna | Fast, cheap (30-295 s), thin; weakest anchor fidelity (91.4% of anchors verbatim); 30 of its blocking findings lost at merge; 49 of 222 runs never opened `source.md`. The second luna is what helps control. | CR:292-294, 373 | Pre-`source.md` luna data invalid and quarantined (CR:107). |
| muse-ember-1.0 | Cheap; 81 of 209 runs (39%) never opened `source.md`; 33 blocking findings lost at merge. Low catch is partly harness, not ability. | CR:292-293, 373 | Added to the fallback ladder as Tier 4 model 2. |
| claude-haiku-5-5 | Workhorse; best real blocking among replicated panels when paired with 2x luna (1.2/8); 7 findings lost; 15 of 75 runs missed `source.md`. | CR:292, 367, 373 | One early haiku run had no `## Findings block` heading at all (15 findings ignored) (CR:11). |
| grok-4.7 | Slow (600-980 s), 41-63k tokens, second opinion; reports gateway id `grok-4.7-build` (benign). | CR:61-62, 295 | |
| gpt-6.1-terra / sol | Return "incomplete" or empty reviews even with `source.md` (16 empty terra reviews in valid era); 0 findings in most rows; pure cost. ember + terra = 0.5/14. | CR:86-89, 294 | |
| glm-5.3 | Slow (800-1800 s per review), costly, no extra catches in any combo; excluded by owner after batch 4. | CR:54, 110 | Gateway outages 2026-11-12 ~08:25 UTC (SPEC:87). |
| Qwen3.8-max | Timed out 3000 s on 3 of 3 slots (0 output tokens, 9000 s wasted); disqualified by owner. | PR:12 | Still the first or second pick of the packaged `tier2b`/`tier3` lists (section 5). |
| muse-wonder-1.0 | Fast (149-186 s), cheap, mid-table. | CR:62 | Gateway misrouted muse as terra under load (SPEC:116). |
| muse-spark-1.3, muse-wonder-full-1.0, opus | Never run in valid era (spark/wonder-full) or never auto-run (opus guard in runner ladder). | CR:286 | |

### 2.4 Defects found in the product code (open; none fixed on this branch)

Status of all: **OPEN** (no product change was made or proposed in code). Citations are `RV/<file>:<line>`, read 2026-11-13.

| # | Defect | Where | Severity | Effect observed in the study |
|---|---|---|---|---|
| D1 | **Over-length findings are dropped.** `anchor` >200 characters, `anchor2` >200, `claim` >300 (also anchor under 12, 9+ refs, MINOR + blocking) fail validation; the finding is skipped and the reviewer's `block ok` becomes false. The only surfacing is ONE warning per reviewer with ONLY the first error message and a "block ok false" line in the merged report; the dropped ids/count are not stored in the ledger. | `findings.py:104,108,118` (checks); `ledger.py:130-134` (single warning), `ledger.py:147` (stores only `block_ok`) | High | 80 reviewer-level cases, **49 blocking findings lost** (luna 30, ember 33 findings in total, wonder 14, glm 7, haiku 7, grok 1, sonnet 0, terra 0, sol 0; CR:292). 4 verdicts flipped FAIL to PASS (CR:292). It penalises luna, ember and wonder systematically. 56 anchors >200, 18 anchor2 >200, 14 claims >300. |
| D2 | **A dropped re-report can clear a blocking row.** A `resolved_check` row becomes `resolved` whenever no cluster re-reports it, even if the reviewer's block was invalid. | `ledger.py:254-258` | High | Not observed in the eval (first reviews only); latent in the review loop. |
| D3 | **Merge passes with one valid reviewer.** The merge fails only if no reviewer has a valid block; a round can PASS on one reviewer while six others were truncated. | `ledger.py:150-157`, `ledger.py:274` | Medium | Same cause as D1 (verdict flips). |
| D4 | **One reviewer's `blocking` flag decides the row and the verdict** (no quorum, no calibration; `confidence` "single"/"overlap" is computed but never used). | `ledger.py:187,213-218`, `ledger.py:86-90,274` | Medium | Judge counts 65 "blocking" catches, only 38 real blocking over 71 rows (CR:291). |
| D5 | **Missing anchors are kept silently** (`anchor_status "missing"`, no warning), so a hallucinated anchor can still create a blocking row. | `findings.py:350-358` | Medium | UNVERIFIED in data. |
| D6 | **Clustering over-merges and under-merges.** Same section + shared refs, or refs plus spans within 3 lines, union-find is transitive; row keeps only the first member's claim/category. | `findings.py:367-407`, `ledger.py:190-199` | Medium | 83 merged rows lumped unrelated findings (chaining), which can distort matching to ground truth (CR:292). |
| D7 | **Reference-id regex needs letters-hyphen-digits** (`AC-0.4`, `P1`); ids like `T01.02` do not match, so tasklist findings cluster by span proximity only. | `findings.py:29`; same regex idea in `telemetry.py:23` | Medium | INFERENCE, UNVERIFIED on a real tasklist. |
| D8 | **Reviewer brief never names the source document**, so a reviewer cannot check plan against source. | `document_review_loop_prompts.md:32` (no source placeholder, only `{{CANDIDATE}}`) and the eval copy `tools/run-reviewer.sh:15` | High (for tasklist review) | 156 of 665 valid-era runs never referenced `source.md` even though it sat next to the candidate. The causal link (brief does not name it) is an INFERENCE, UNVERIFIED (CR:373). |
| D9 | **Brief makes `missing-requirement` findings Medium by instruction**, while the findings schema lets them be `blocking:true`. | `document_review_loop_prompts.md:31`; schema `findings.py:15-22` | Low-Medium | Possible over/under-blocking depending on reviewer reading. |
| D10 | **Category label** `unpassable-ac` (in the first eval brief) is rejected by the validator, which only knows `unpassable-check`. Fixed in the eval brief; `unpassable-ac` appears nowhere in `src`. | `findings.py:17,102-103`; fix in `tools/run-reviewer.sh` (old copy `.unpassable-ac`); `SPEC:38-39` | Fixed (eval) | 9 pilot files needed `.catfix.md` copies; 15+ findings lost on one haiku and one other run. |
| D11 | `distinct_across_slots` silently allows duplicates when the pool is exhausted (gateway `@live7` run-id `run1` gives Qwen3.8-max to both `t2b-1` and `t3-2`; anthropic-only `@live7` gives 6 identical haiku). | `panel.py:402-408` | Medium | Not observed in the eval (the eval picked models by hand). |
| D12 | Environment select keys on `$T3Model01` only; `T2bModel01` is never read by `cli/review`, so nothing checks that the `tier2b` alias exists. | `panel.py:372`; `T2bModel01` only in ccsession config (UNVERIFIED grep of config) | Medium | Eval found "tier aliases serve only the first model of a tier" (`manifest.md`), so aliases were NOT used; raw model ids were. |
| D13 | `lint_cmd` and `estimate_cmd` are registered but the files do not exist; `ModuleNotFoundError` is swallowed so `superclaude review lint|estimate` silently does not exist. | `__init__.py:19-32` | Medium | |
| D14 | No tasklist review step exists in `sc-tasklist-protocol` or `sc-workflow-protocol` in `src` (grep for `superclaude review`, `review panel`, `review_ledger`, `review loop` returned nothing). The review loop lives only in `commands/spec-panel.md:256-268` plus the prompts file. The "review ledger" skill, `spec-panel-ledger/-stoprule` commands and `finding-grader` agent exist only as experiment copies under `.dev/experiments/346-validation/phase5/final-bundle/builds/`. | grep result; investigation notes | High (for the unification plan) | The eval therefore drove the generic `/sc:spec-panel --mode critique` command against a tasklist file. |
| D15 | Telemetry strata allow only `sonnet` or `haiku`, so other models cannot be tagged; `merge` and `panel resolve` write no telemetry (the caller must append). | `telemetry.py:112-115,267-268`; `merge_cmd.py:71-118` | Low | The eval did NOT use `review telemetry`; it used its own `cost.json`/`meta.json`/`score.json` files. |
| D16 | Round 4 is accepted; `--cap` is ignored on an existing ledger; "verify-only" rounds are not a code mode (prompt-only). | `ledger.py:93-96,114`; `merge_cmd.py:104` | Low | |

Notes on D1 (precision): an earlier eval sentence said the merge drops findings "with no error". More exactly: it returns a one-line warning containing only the first error, and exits successfully if any other reviewer is valid. The practical effect (lost findings, not recorded) stands.

### 2.5 Defects and incidents in the study harness (all FIXED or DISCLOSED, none product code)

| Incident | Effect | Status |
|---|---|---|
| Blocking-count parser grepped `"blocking":true` without space; several models emit `"blocking": true` | per-model blocking numbers wrong in early sections | corrected CR:104-106 |
| Cyclic fallback ladder spun on exit-127 (claude binary self-update) and ran a review on Qwen3.8-max / haiku | 42-minute run, wrong-model data | runner patched (never revisit, `EXCLUDE_MODELS`, `NOFALLBACK=1`), rows quarantined and rerun (`tools/run-reviewer.sh:66-80`, SPEC batch 9) |
| 12 concurrent workers caused gateway model-identity bleed (muse served as terra) | batch 3 contaminated | quarantined as `*-contaminated-20261111`, re-run serially after a 60-min cooldown (CR:86; SPEC:77-87) |
| `claude` binary replaced at 22:17, 23:05, 00:35, 13:48-13:50 | exit-127 failures | rerun/quarantined |
| Batch 10 (grok+sonnet, haiku+sonnet) dropped by owner; an interrupted quarantine had moved 8 runs' files | excluded from all tables | disclosed in SPEC |
| `attrib.py` per-reviewer attribution credited every member of a merged row | doubling claim wrongly concluded "adds nothing" | RETRACTED CR:195 |
| Judge "blocking" mixes definitions | 65 vs 38 blocking | both columns now shown |
| Merge silently drops over-length findings (D1) and stale merges (n2-terra, r2-sol merged before re-runs; n5-sol, n5-terra merged from a report no longer in the row; r2-sonnet scored before a re-merge) | scores slightly off | flagged by audits; r2-sonnet excluded (CR:292, 296) |

### 2.6 Audits that checked these findings

Six independent read-only audits, outputs in `EVAL/analysis/audits/audit-A..F` (summaries in `summary.md`): A identity (2 b4-muse-luna2 "wonder" runs served terra, already quarantined; grok id benign), B report validity (51 incomplete reports), C inputs and timing (source.md first shipped 12:59:34, no run read ground truth or other reviewers' reports), D merges (D1 numbers), E scoring (294 judge outputs clean; blind re-judge of 12 rows: 12/12 exact agreement, 19 of 19 recorded catches confirmed, one borderline GT8 would add one), F aggregation (blocking definition; Welch and permutation tests). Result: no fabricated scores or wrong-document runs (CR:290). Limits: audits were read-only by the same orchestrating session (not independent humans); one judge per (row, package), judge variance only measured on the 12-row re-judge.

### 2.7 What the evidence does NOT show

- No panel is shown to be worse or better on quality; only cost and elapsed time differ (R1).
- Nothing about re-review rounds 2 and 3 (verify-only), the reviser, or the loop verdict: the eval ran **first reviews only**, one round.
- Nothing about tasklists from other repositories, or plans other than these 3 packages (16 known defects).
- Ground truth counts only defects that blocked implementation in the original runs; a genuine novel defect counts as a wrong blocker (CR:75).
- The merge limits (D1) and the missing source (D8) distort every number; the true model ranking under fixed harness is unknown.

---

## 3. Lessons and strategies

**Worked:**
1. **Blind scoring with anonymised merged reports and an Opus judge**, plus an independent re-judge of 12 rows (12/12 agreement). Cheap and credible (audit E).
2. **Ground truth from real implementation failures**, not imagined defects (`blocking_in_implement` flag gave the useful "real blocking" cut that exposed judge-blocking inflation).
3. **Six read-only integrity audits after the data was in** (identity, validity, inputs, merges, scoring, aggregation). They found real problems (D1, blocking definition, stale merges) that tables had hidden.
4. **Replicates (4-6) before any claim**, and permutation tests on run-level values. Every single-run "winner" regressed (sonnet + 2x luna 4/14 became 2.33 over 6; r2 family 4/14 never repeated).
5. **Model-identity check on every run** (`observed_model` from the assistant message vs requested) and quarantine-not-delete: contamination was recoverable because nothing was removed.
6. **`NOFALLBACK=1` for evaluation runs and per-replicate runner streams**; use cancel-files (`/tmp/cancel-<row>`) to stop rows cleanly.
7. **Counting by parallel agents AND a direct script, comparing cell by cell** (0 mismatches over 320 and over 62 x 16 x 2 cells).

**Failed or misled:**
1. Judging a panel's value from a single run (n=1 rows are anecdotes).
2. Attribution of a merged row to every member (flawed, retracted); reading "the second run adds nothing" from it.
3. Treating the judge's `gt_covered_blocking` as real blocking.
4. Running many workers at once on the gateway (model-identity bleed, 429s); long sleep chains in a hooked shell (blocked, use background until-loops).
5. Grepping JSON with fixed spacing; `claude` binary self-updating mid-run; a cyclic fallback ladder that hid wrong-model runs.
6. Not shipping `source.md` at the start (first 48 hours of data pre-source and partly invalid); not noticing the brief never names it.

**Do differently:**
- Fix D1 and D8 first, then re-run ONE replicated 2-panel comparison (ember + 2x luna vs sonnet + 2x luna, 6 runs each), since every table so far is depressed by those two defects.
- Add a dropped-findings counter to the merge output and record it in the ledger before any further eval, so harness loss is visible without a 6-audit pass.
- Keep one canonical scoring script in the repo, not in `/tmp` (58 helper scripts were only in `/tmp`; this hand-off copies them).
- Pre-register the decision rule (the pilot had one, `PR:56-61`; later batches did not).

---

## 4. Decisions

### 4.1 Made (by the owner unless noted) and why

| Decision | Why | Source |
|---|---|---|
| Qwen3.8-max excluded everywhere | 3 of 3 slots timed out at 3000 s | PR:12 |
| Use raw gateway model ids via `claude -p --model`, not tier aliases | aliases only serve the first model of a tier | `manifest.md` |
| Valid era starts when `source.md` shipped (2026-11-12 12:59:34); pre-source luna/terra/sol data quarantined | reviewers lacked a required input | CR:107, 373 |
| Batch 10 dropped; testing closed 2026-11-13 | owner: "we're going to decide and run with it" | CR:290 |
| Default panel = ember + 2x luna; optional quality tier = sonnet + 2x luna; best real-blocking = haiku + 2x luna; do not use ember + terra, 2x ember + 2x luna, terra/sol alone, 5-reviewer panels | cost, reach, wrong blockers; replicated evidence | CR:363-371, 421-428 |
| The "decision update" making sonnet + 2x luna the standard was rejected | batch 11 (5 replicates) showed regression to the mean | CR:428 |
| No PR; push the research branch only to origin for other agents to read | owner order | session |
| Raw transcripts left out of commits | size (1.48 GB) | owner order |
| Never stage `.claude/`; change nothing under `.dev/tasks/` | standing constraints | CLAUDE.md |

### 4.2 Still open, and who decides

| # | Open decision | Who |
|---|---|---|
| 1 | Fix D1: raise or remove the 200/300-character limits, or truncate rather than reject, and add a dropped-findings counter. Product code change under `RV/findings.py`, `ledger.py`. | owner / unified-panel session |
| 2 | Fix D8: add a source/driving-spec input to the reviewer brief and a `{{SOURCE}}` value (shared with reflect, which already takes `spec_path`). | owner / unified-panel session |
| 3 | Which model set the unified panel ships as default, given the replicated numbers, and whether tier ids are time-bound config or code. | owner |
| 4 | Whether tasklist review is a step inside `/sc:workflow` (not present in `src` today) or a separate command; which code path triggers it. | owner |
| 5 | Whether verdicts use one reviewer's `blocking` flag (D4) or a quorum/calibrated rule (reflect has a calibrator; this panel has none). | owner |
| 6 | Whether the 1.48 GB raw transcripts are ever committed (this brief says "commit every artifact"; the prior order says leave them out). Kept out here. | owner |
| 7 | Whether to re-run the comparison after D1 and D8 are fixed. | owner |

---

## 5. The Review Panel as understood now

### 5.1 Roles

| Role | Who does it in code | Notes |
|---|---|---|
| **Reviewer** | A fresh session of a model resolved from the panel template; instructed by the brief; no agent definition in `src` for this panel (reflect has `reflect-reviewer`). Prompt only says "Do not edit the candidate" (`document_review_loop_prompts.md:32`). | The eval used `claude -p` with Edit/Write disallowed (`tools/run-reviewer.sh:48`). |
| **Merge / "judge" (in product)** | `superclaude review merge` is deterministic: cluster by fingerprint (section + refs) or span proximity (+-3 lines), any reviewer's `blocking` => row blocking, verdict FAIL if any open or regressed blocking row. No LLM judge, no calibrator. | `ledger.py:93-104,187,213-218,274`; `findings.py:367-407` |
| **Calibrator** | None in `cli/review`. Reflect Tier 2 has blind `confidence-calibrator` (SKILL.md reflect §11.3, UNVERIFIED line). The stoprule experiment variant has `finding-grader` (blind, decides only blocking). | Both outside this panel code. |
| **Orchestrator** | The main session following `commands/spec-panel.md:256-268` and the prompts file: resolves panel, spawns reviewers, merges, computes review count, runs reviser, calls `ledger revise`. | |
| **Reviser** | An agent given the merged report's reviser brief; returns `fixmap-v1`. `ledger revise --old --new --fixmap` sets touched rows to `resolved_check`. | `ledger_cmd.py:36-71`, `ledger.py:301-347` |
| **Human** | `ledger defer --lid --reason` (deferred rows drop from the brief). | `ledger.py:350-360` |
| **Eval judge (study only, not product)** | Opus, one per (row, package), blind. | `tools/tmp-scripts/judge-one.sh` |

### 5.2 Data contracts

| Contract | Format | Key points (with lines) |
|---|---|---|
| Reviewer to merge: **findings-v1** | `## Findings block` heading followed by a closed fenced block with info `findings-v1`, one JSON object per line | heading regex `findings.py:31`; id `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` (:26, :92); severity CRITICAL\|MAJOR\|MINOR (:14); `blocking` real boolean, MINOR cannot be blocking (:98-101); category: contradiction, unpassable-check, data-loss, safety, missing-requirement, other (:15-22); `anchor` 12-200 chars copied exactly (:104); optional `anchor2` 12-200 (:107-110); `refs` list of up to 8 strings (:111-117); `claim` at most 300 chars (:118). Prior lines: `{"prior":"L3","status":...}` (:175-187). **No confidence field in the reviewer format**; ledger confidence is derived (`overlap` if 2+ reviewers) (`ledger.py:86-90`). Anchors are matched by whitespace-flattened exact substring (`findings.py:276-304`). |
| Reviser to ledger: **fixmap-v1** | JSON lines `{id, action applied\|rejected, reason}` | `findings.py:199-223` |
| Ledger: **review-ledger/1** | JSON: schema, doc, cap_reviews, rounds[], rows[] (lid `L<N>`, fp, blocking, severity_max, category, confidence, status, anchors, spans, refs, claim, members[], history[]) | atomic write, no locking (`ledger.py:52-67`); statuses open/resolved_check/resolved/regressed/deferred (:19) |
| Panel resolution: **review-panel-resolution/1** | per reviewer: reviewer_id (`t1b-1`, `t2-1`, `t2b-1`, `t3-1`, `t3-2`, `t4-1`, `t4-2`), slot, tier, alias, strategy, seed, model, fallback_depth, stand_in, fallbacks, launch; plus template/tiers sha256 | `panel.py:498-520`; merge reads only reviewer_id and model (`merge_cmd.py:76-79`) |
| Capture matrix: **review-capture/1** | defects x reviewers per round | `ledger.py:375-401` |
| Telemetry: **review-telemetry/1** | JSONL `reviewer_run` and `outcome` records, SQLite `model_scores` view (precision, TP, cost per confirmed TP) | `telemetry.py:17,82-109,362-379`; unused in the eval |
| Merged report | text; ends `verdict: PASS\|FAIL`; ESCALATE omits the reviser brief | `ledger.py:408-494` |

Severity semantics: the brief defines "blocking" by a grading sentence (two stated texts contradict, stated text causes data loss or breaks a safety boundary, an acceptance criterion cannot pass); Medium for a guess or an unstated requirement; no CRITICAL/MAJOR/MINOR definitions in the prompt (`document_review_loop_prompts.md:31`). `spec-panel.md:259` says CRITICAL is blocking and MAJOR only with a concrete wrong outcome (UNVERIFIED re-read).

### 5.3 Model and tier configuration

Tier table (`RV/data/review-tiers.default.json:4-11`): tier1a (claude-opus-5-5, claude-sonnet-5-5); tier1b (claude-sonnet-5-5, gpt-6.1-sol, muse-wonder-full-1.0); tier2 (gpt-6.1-sol, glm-5.3, grok-4.7, Qwen3.8-max, muse-wonder-1.0, muse-spark-1.3); tier2b (gpt-6.1-terra, glm-5.3, Qwen3.8-max, muse-wonder-1.0); tier3 (glm-5.3, Qwen3.8-max); tier4 (gpt-6-luna, claude-haiku-5-5, grok-4.7). A tier alias is an ordered model list, first = default. Environments: `gateway` (all models) and `anthropic-only` (opus, sonnet, haiku, fable; stand-ins for tiers 2, 2b, 3, 4 = haiku) (`:18-31`). Packaged panels: `@default` = t1b x1 fixed + t2 x1 random + t3 x2 random (4 reviewers); `@live7` = t1b + t2 + t2b + 2x t3 + 2x t4 (7 reviewers) (`review-panel.*.json`). Re-review uses only the fixed anchor `t1b-1` (`panel.py:452-454`). Verified by running `superclaude review panel resolve` (e.g. anthropic-only `@live7` = 1 sonnet + 6 haiku).

**What the study found about this configuration:** the tier lists pick models the study found unusable (Qwen3.8-max in tier2b, tier3; glm-5.3 as the only tier3 model; terra/sol as tier2 and tier2b first picks, which returned empty reviews), and ignore models the study found useful (haiku and luna only in tier4, ember not listed, sonnet only in tier1). The study did not use `panel resolve`; it hand-picked models per row, so **no result validates the packaged `@default` or `@live7` as shipped** (the pilot arms B and C approximated them minus Qwen slots).

### 5.4 How results are recorded and compared (study, not product)

Per run: `<pkg>/reviews/combos/<row>/<id>.{md,meta.json,cost.json}` (`meta.json`: expected/observed model, model_ok, findings_block, attempts, wall, output tokens). Per row and package: `combos/<row>/<pkg>/{ledger.json,merged-1.md,resolution.json}`. Per blind judgement: `arms/scoring/combos/<row>/<pkg>/<label>/{merged-anon.md,score.json,judge.json}`, with label keys. Tables: `analysis/final-table.py` (AS-SCORED and AUDIT-CLEAN, real vs judge blocking, per-100k-token efficiency), `three-way.py` (permutation tests), `allsets-table.py`, `issue-table.py`.

### 5.5 Tasklist-specific vs target-agnostic

Target-agnostic (generic markdown candidate): all of `RV/*`, both packaged panels, tier file, the brief. Spec-oriented assumptions inside them: category list, reviser rules text, requirement-id regex (D7), numbered-heading section naming. Tasklist-specific: nothing in `src`. The study layer is tasklist-specific: the 3 packages, ground truth (`<pkg>/ground-truth.json`), `tools/run-reviewer.sh` paths, the judge prompt, and the issue labels (B1-B8, I1-I8 map to designSpec GT1-5, alias GT1-3, designSpec GT6-10, alias GT4, control GT1-2).

### 5.6 Contrast with reflect Tier 2 (from the investigation, SKILL.md citations UNVERIFIED by re-read)

| Aspect | Review panel (this study) | Reflect Tier 2 |
|---|---|---|
| Reviewers | N from a panel template, resolved to model ids by tier/slot/strategy/seed | 2-3 fixed `reflect-reviewer` agents; heterogeneity by model class via `ANTHROPIC_DEFAULT_*_MODEL` aliases |
| Input | candidate document only (brief names only `{{CANDIDATE}}`) | spec_path / tasklist_path / diff_scope / persona lens |
| Output | JSON `findings-v1` with anchors, blocking flag | markdown deviations table with file:line, HIGH/MEDIUM/LOW; no blocking flag |
| Calibration | none | blind `confidence-calibrator` per card (disjoint model class) |
| Merge | deterministic script, any-blocking => FAIL | `sc-adversarial-protocol` Mode A (debate, scoring), then evidence-validator gate |
| Config | tier file + panel template + seeds | model class rotation in the skill file; no tier file |

---

## 6. What the unified panel must meet (so sc:workflow and tasklist review move onto it with no regression)

1. **Accept both finding shapes or define a mapping.** Keep findings-v1 (`findings.py:90-121`) fields (id, severity, blocking, category, anchor, anchor2, refs, claim) and add reflect's evidence (file:line) and calibrated confidence, or map one to the other; do not drop the anchor locate check.
2. **No silent loss.** Parser rejections must be counted and recorded (ids, reasons) in the ledger and merged report; limits either removed (truncate rather than reject) or enforced in the brief and re-validated. Never PASS a round when any reviewer's block is invalid unless the caller opts in (D1, D3).
3. **The reviewer input must include the driving document** (source.md for tasklists, spec for reflect) and a named placeholder in the brief (D8); log whether each reviewer referenced it (the study's audit C method).
4. **A defined "blocking" rule**, with either a quorum or a calibrator, plus a measured "real blocking" metric. The study's judge-blocking overstated real blocking by 1.7x (65 vs 38).
5. **Model resolution must be evidence-based and enforce identity.** Observed-model check on every run (`observed_model` equals requested), no model revisit in the fallback ladder, an exclude list, and duplicates flagged (D11, section 2.5). Tier lists must be updated from this study (Qwen, glm, terra/sol out of default slots; luna, ember, haiku, sonnet in).
6. **Cost/time recording by default** (tokens, wall seconds per reviewer, per model), to the telemetry store; tag strata beyond sonnet/haiku (D15).
7. **Re-review semantics preserved** for the review loop (anchor-only reviewers on re-review, ledger rounds, verify-only prompt, `ledger revise`), and fix D2.
8. **A runnable regression suite from this study:** a fixed set of plans with ground truth (the 3 packages, 16 known defects) so any future panel change can be scored the same blind way; the scripts for that now sit in `tools/tmp-scripts/` and `analysis/`.
9. **Reviewer isolation:** fresh context, no cross-visibility, sandbox that excludes `.dev/tasks/done`, eval workspaces and ground truth (`manifest.md`).
10. **A place for tasklist review in `sc-workflow-protocol`/`sc-tasklist-protocol`** (D14: not there today, so "no regression" means defining the baseline: today's behaviour is no panel step in those skills).

---

## 7. Questions for the other session, and merge risks

**Questions:**
1. Does `/sc:workflow` (or `/sc:tasklist`) invoke any reviewer panel today outside `src`? The grep found none in `src`; is there a runtime or `~/.claude` path that does (UNVERIFIED)?
2. Which finding format does the unified panel use, and what is the mapping from reflect's deviation categories (Authorized expansion, Necessary deviation, Drift, Regression) to findings-v1 categories?
3. Does reflect's calibrator apply to findings-v1 anchors or only to deviation cards, and does its model-class disjointness rule conflict with panel `distinct_across_slots`?
4. What does reflect give reviewers for the driving spec, and can the panel reuse that mechanism (D8)?
5. Is the reflect rotation table (sonnet/haiku/qwen|kimi|deepseek else opus) still valid given Qwen was disqualified here?
6. Who owns the model/tier lists: product data (`review-tiers.default.json`) or ccsession config (`ccsession-models.json`, `T2bModel01`)? The two currently diverge (D12).
7. Where does the stoprule/ledger experiment (`.dev/experiments/346-validation/phase5/final-bundle/`) stand? It holds the only copies of the review-ledger skill and `finding-grader`.

**Merge risks:**
- Findings drops (D1) also exist on the reflect side if it ever adopts findings-v1: adopting the parser as is imports the defect.
- Different notions of "blocking": reflect HIGH/MEDIUM/LOW is not a gate; panel blocking is. Mapping them casually will change verdicts.
- The packaged `@live7` embeds gateway-specific, time-bound model lists that the study contradicts.
- The study's numbers are depressed by D1 and D8; a merge that cites "about 2 of 14" as the panel's ability will be citing the harness, not the models.
- The ground truth reflects 3 packages from one repository; over-fitting a panel to it is a risk.
- Branch contains untracked raw data; anyone cloning gets the processed results only.

---

## 8. Test and verification status

| Area | Status |
|---|---|
| Product tests for `RV/*` | 111 tests in `tests/review` (cli 9, findings 23, ledger 24, panel 26, panel_live7 14, rules_text 5, telemetry 10) plus 5 `tests/skills/test_*review*` files (spec_panel_review_loop 11, severity_mapping 8, prompt_overrides 14, severity_rule 21, loop_extension 9 test functions = 63). The full run reported 299 passed, which is more than 111 + 63 = 174, so parametrised cases account for the difference (UNVERIFIED breakdown). **Run 2026-11-13: 299 passed in 7.1 s; nothing written to the repo.** |
| Covered | length limits: anchor under 12 and over 200 and claim over 300 produce `ok=False` (`tests/review/test_review_findings.py:112-117`); `@live7` resolution (14 tests); ledger rounds 1-3. |
| NOT covered | `unpassable-check` as an accepted category (only invalid "weird" tested); `resolution.json` by name (CLI test passes `--resolution panel.json`); any assertion that a dropped finding is reported with its id (D1 behaviour); D2 (dropped re-report clears a blocking row); duplicate models under `distinct_across_slots` (D11); `T2bModel01`/tier2b alias existence (D12); the missing `lint_cmd`/`estimate_cmd` (D13); a tasklist-format id (D7); the eval harness itself (`run-reviewer.sh`: no tests; model-identity, ladder and `NOFALLBACK` logic verified only by incidents and audits). |
| Study verification | six audits (section 2.6); table cells cross-checked by independent script (0 mismatches of 320 and of 62 x 16 x 2); blind re-judge 12/12 agreement. |
| Not verified here | this hand-off report was not run through a QA fleet (method note, top); the reflect side was not read in detail (section 5.6 contrasts come from the investigation agent's notes). |

---

## 9. Where to start (reading order)

1. This report. 2. `CR:289-373` (final results and decision), `CR:421-428` (batch 11). 3. `EVAL/analysis/audits/audit-D/summary.md` (merge drops) and `audit-C/summary.md` (source.md). 4. `RV/findings.py:90-121`, `RV/ledger.py:107-298`. 5. `tools/run-reviewer.sh:13-17` (the brief used) and `tools/tmp-scripts/judge-one.sh` (the scoring prompt). 6. `SPEC.md` ops log for the incident history.

**Evidence trail (files read this session):** `PILOT-REPORT.md`, `COMBO-REPORT.md` (lines 1-12, 47-116, 286-435), `SPEC.md:1-40` plus heading list, `manifest.md`, `tools/run-reviewer.sh:1-80`, `tools/tmp-scripts/judge-one.sh`, investigation notes `/tmp/handoff-notes/code-merge.md`, `code-panel.md`, `tests-tools.md`.
