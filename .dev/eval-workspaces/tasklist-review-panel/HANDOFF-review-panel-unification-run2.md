# Hand-off research report (run 2): the Review Panel for tasklist review

| Field | Value |
|---|---|
| Date written | 2026-11-13 (`date -u` 16:16 UTC; the writer agent recorded 2026-11-14 in its checks below, which is wrong: read every "2026-11-14" in this file as 2026-11-13) |
| Repo / branch | /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel, branch `ironbelly/eval-tasklist-review-panel` |
| HEAD | 4a22d7421, equal to `origin/ironbelly/eval-tasklist-review-panel` (`git rev-parse` 2026-11-14) |
| Branch base | ec259f1b7 (= origin/master when the eval started, manifest.md:6-8) |
| EVAL | `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` |
| Reader | a session that will merge this work with the reflect Tier 2 panel work and plan one unified Review Panel; it has none of this session's context |

### Method note (read first)

- This report was produced WITHOUT the full tech-research MDTM task-file machinery: there is no task folder, no checklist and no multi-gate QA fleet. One agent wrote it from three fresh investigation notes (`/tmp/handoff-notes-run2/code-merge.md`, `code-panel.md`, `tests-tools.md`) plus its own Reads, greps, git commands and one test run. Treat it as a single-author draft with spot verification, not as a QA-gated report.
- Independence: this run did not open anything under `/tmp/handoff-notes/` (the earlier run), did not open any `HANDOFF-review-panel-unification*.md`, and did not `git show` that file from commit 4a22d7421. Conclusions here are formed independently and may disagree with that earlier hand-off.
- Every file:line below was Read (or grep-confirmed) on 2026-11-14 in the branch working tree unless marked UNVERIFIED. Statements that come only from the orchestrator are marked "session record".
- Product code is cited at the branch state, which equals the branch base ec259f1b7 for `src/` and `tests/` (`git diff --stat origin/master...HEAD -- src tests` is empty). origin/master has since moved: commits d2d8a2d16 (#519, reflect Tier 2 review panel Stage 0-2) and 167184c6b (#518, tier owner decisions) changed 40 files under `src/superclaude/cli/review/` and `tests/review/` (+8,026 lines). Those changes were only listed and grepped here, not reviewed. Where they matter they are flagged "master (grep only)".

### Conventions

- Paths are relative to the repo root; `EVAL/...` means the eval folder above. `CR:n` = line n of `EVAL/COMBO-REPORT.md`. `SPEC:n` = `EVAL/combos/SPEC.md`. `PILOT:n` = `EVAL/PILOT-REPORT.md`. `audit-X:n` = `EVAL/analysis/audits/audit-X/summary.md`.
- Product code: `findings.py`, `ledger.py`, `merge_cmd.py`, `panel.py`, `telemetry.py` are under `src/superclaude/cli/review/`. `prompts:n` = `src/superclaude/rules/prompts/document_review_loop_prompts.md`. `spec-panel.md:n` = `src/superclaude/commands/spec-panel.md`. `tiers.json:n` = `src/superclaude/cli/review/data/review-tiers.default.json`.

### Terms used throughout

| Term | Meaning | Source |
|---|---|---|
| "Tasklist review" in this study | A first review ("review 1 of 3") of an `sc:workflow` plan package: the reviewer reads `candidate.md` (a plan with header `schema: workflow-plan/1.2`, `source: ./source.md`) | `EVAL/TASK-WF-designSpec-20261107-075614/candidate.md:1-3`; run-reviewer.sh:13-17 |
| Packages | designSpec (10 ground-truth defects, 5 blocking in implement), makeTheAliasOnly or "alias" (4, 3 blocking): together "defect-rich", 14 defects / 8 blocking. design = control (2 defects, 0 blocking) | CR:9; PILOT:7 |
| Ground truth (GT) | Defects that actually hurt the past implement run of each package, with evidence lines and a verified plan quote | `EVAL/TASK-WF-design-20261108-041415/ground-truth.json` (keys items, verification, dropped) |
| Model short names | sonnet = claude-sonnet-5-5, haiku = claude-haiku-5-5, luna = gpt-6-luna, terra = gpt-6.1-terra, sol = gpt-6.1-sol, wonder or muse = muse-wonder-1.0, ember = muse-ember-1.0, grok = grok-4.7, glm = glm-5.3, Qwen = Qwen3.8-max; judge = claude-opus-5-5 | SPEC:8-14, :45-56, :120; judge-one.sh:25 |
| Row, row-package | One panel (a set of reviewer models) run once over all 3 packages; a row-package is that row on one package | CR:301 |
| Valid era / src era | Runs made after source.md was shipped next to the candidate (first valid run 2026-11-12 13:02:27) | CR:373 |
| Found /14 | Ground-truth defects matched at any severity on the two defect-rich packages, summed | CR:300, CR:304 |
| Real blocking /8 | Judge credited the defect through a blocking ledger row AND the defect has `blocking_in_implement=true` | CR:291 |
| Judge-blocking | The judge's raw `gt_covered_blocking` (can include non-blocking defects) | CR:291 |
| Wrong blockers | Blocking ledger rows that match no ground-truth defect | judge-one.sh:20 |
| B1-B8, I1-I8 | The 16 issue labels used in the issue tables (B = blocking in implement) | CR:401-417 |

## 1. Inventory

Status tags: **CP** = committed and pushed (on `origin/ironbelly/eval-tasklist-review-panel`); **CL** = committed, local only; **UC** = uncommitted; **MASTER** = product code already on master, not changed by this branch; **OUT** = outside the repo (only on this machine).

### 1.1 Git state

| Item | Status | Evidence |
|---|---|---|
| b4db265a8 "docs(eval): tasklist review panel model-combination study" (8,814 files: packages, arms, combos, quarantine, analysis, tools) | CP | `git log`; tests-tools.md:118 |
| 2d06a4382 "docs(eval): add batch 11, issue-by-panel tables and all-combinations issue table" (445 files incl. COMBO-REPORT.md) | CP | tests-tools.md:119 |
| 4a22d7421 "docs(eval): add review-panel unification hand-off report and /tmp helper scripts" (tools/tmp-scripts 55 files + the earlier hand-off file, not opened here) | CP | tests-tools.md:120 |
| Commits that are local only | none (CL is empty) | `git status -sb` shows no ahead/behind, 2026-11-14 |
| Tracked edits | none | `git status --porcelain` shows only `??` lines, checked before and after the test run |
| Untracked files | UC: 3,041 files, all under EVAL: 1,380 raw reviewer transcripts `*.attempt<N>.json`, 1,352 per-attempt `*.attempt<N>.meta.json`, 309 `judge.json`; about 1.5 GB | count re-run 2026-11-14 (3041); breakdown tests-tools.md:125-129 |
| Source or test changes on this branch | none | `git diff --stat origin/master...HEAD -- src tests` is empty |
| Branch freshness | branch is 11 commits behind origin/master (not rebased), including d2d8a2d16 (#519) and 167184c6b (#518) that edit `src/superclaude/cli/review/` | `git log HEAD..origin/master` 2026-11-14 (no fetch run; origin/master as of the last fetch) |

Discrepancy: `EVAL/analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md:2` says 2,916 raw files (~1.48 GB) were left out; git shows 1,380 + 309 = 1,689 raw transcripts plus 1,352 per-attempt meta files. The per-attempt meta files are also uncommitted, although that note (line 3) implies `meta.json` is committed (only the final `<rid>.meta.json` is). Exact reconciliation UNVERIFIED.

### 1.2 Evaluation artifacts (all under EVAL)

| Artifact | What it is for | Status | Reusable beyond tasklist review? |
|---|---|---|---|
| `COMBO-REPORT.md` (506 lines) | Master results log. Lines 289-506 ("FINAL RESULTS AND DECISION (2026-11-13)" onward) supersede everything above them; lines 1-288 are history incl. retractions | CP | The method and final tables are reusable as a baseline; numbers are specific to the 3 packages |
| `PILOT-REPORT.md` | 2026-11-11 pilot: arms A (sonnet alone), B (@default minus Qwen), C (@live7 minus Qwen), blind-scored, fixed decision rule | CP | Method reusable; luna numbers superseded (CR:107) |
| `manifest.md` | Eval setup: base sha, sandbox, dispatch method, GT hashes. Line 5 "local, never pushed" is now stale (branch is pushed) | CP | Pattern reusable |
| `combos/SPEC.md` (152 lines) | Worker procedure for one combo (lines 18-36) plus an append-only ops log of every batch, outage, quarantine and owner order | CP | Procedure reusable; log specific |
| 3 package folders `TASK-WF-*` | `candidate.md`, `ground-truth.json`, `ground-truth-draft.json`, `resolution-default.json`, `resolution-live7.json`, `reviews/` (every reviewer report `.md`, final `.meta.json`, `.cost.json`), `reviews-failed-launch-1/` | CP (raw `*.attempt*.json` UC) | GT and candidates are a reusable regression fixture for any plan-review panel |
| `arms/` | Pilot arm merges (A/B/C) and blind scoring: `merged-anon.md`, `score.json`, `label-key.json` (judge transcripts `judge.json` UC) | CP | Scoring layout reusable |
| `combos/` | 106 row folders, each with per-package `ledger.json`, `merged-1.md`, `resolution.json`, `merge-stdout.txt` (45 merges lack it, audit-D:26); only 19 rows have `RESULT.md` (tests-tools.md:50) | CP | Specific |
| `probe/probe.json` | Stage 0 dispatch probe (raw id vs tier alias) | CP | Reusable finding (alias serves first model only, manifest.md:11) |
| `quarantine-pre-src-luna/` | Luna runs made before source.md was shipped, quarantined by owner order 2026-11-12 15:16 | CP | No (audit only) |
| `tools/run-reviewer.sh` (87 lines) | Runs one reviewer: sandbox copy of candidate and source.md, brief, `claude -p --model <raw id>`, identity and block checks, 2 attempts, fallback ladder, cost file | CP | Partly: brief and checks are generic; line 10 hard-codes this worktree's `.dev/tasks/done/$PKG/source.md`; ladder is hand-kept |
| `tools/run-reviewer.sh.bad-launch`, `.unpassable-ac` | Earlier versions kept for audit (brief as argv; wrong category label) | CP | No |
| `tools/tmp-scripts/` (55 files + README) | Verbatim copies of `/tmp` helpers: anonymisation (`anon-*.sh`), merges (`merge-b6.sh`, `merge-src-rows.sh`), batch launchers (`b4-*`, `b5-*`, `b6-*`), judging (`gen-judge-list.sh`, `judge-one.sh`, `run-combo-judges.sh`), Orca worker starters (`startcombo*.sh`) | CP (in 4a22d7421) | `judge-one.sh` and `anon-*.sh` are reusable patterns; the rest hard-code the EVAL path and package ids. `snap.py`, `drift-b3.py`, `rlog-r3.sh` reference a different eval (`brainstorm-reflect-panel` worktree; grep 2026-11-14) and `snap.py` writes into it (tests-tools.md:67) |
| `analysis/*.py`, `analysis/*.out`, `final-table.md`, `final-*.json`, `issue-table/`, `allsets/`, `b7..b11` launch, merge and judge logs | Tables, statistics, issue-by-panel counts | CP | No. Several scripts read or `exec` `/tmp` copies (final-table.py:23 and :80-83, three-way.py:4 and :48-52, b9-table.py:3, doubles.py:3, issue-setup.py:3), so they do not run from the committed tree alone |
| `analysis/audits/audit-A..F/` | Six integrity audits: A model identity, B incomplete or short reports, C inputs and leakage, D merges and ledgers, E scoring, F aggregation | CP | Check designs are reusable. Only A and D have a `summary.md`; B, C, E, F hold scripts and `flags.tsv` only, and their conclusions live in CR:290-298 |
| `analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md` | Says which raw files were left out and where to start reading | CP | n/a |
| Raw transcripts and per-attempt meta | Evidence for identity and token audits | UC | n/a; owner decision pending (section 4) |
| `/tmp/evalsb/repo` sandbox, `/tmp/audit-*/`, `/tmp/final-table.py`, `/tmp/*.log` | Reviewer sandbox (git archive of HEAD without `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research`, manifest.md:10) and the live copies the analysis scripts read | OUT; whether they still exist is UNVERIFIED | n/a |

### 1.3 Product code the study exercised (none of it changed by this branch)

| Code | Lines | What it does | Status | Tasklist-specific? |
|---|---|---|---|---|
| `findings.py` | 457 | findings-v1 and fixmap-v1 parsing, field limits, anchor location, refs, fingerprints, clustering | MASTER (branch base) | No (code-merge.md:155) |
| `ledger.py` | 494 | Ledger state machine, `merge_round`, verdict and decision, revise, defer, capture, merged report | MASTER | No |
| `merge_cmd.py`, `ledger_cmd.py` | 118, 137 | `superclaude review merge`; `review ledger revise/defer/verdict/capture` | MASTER | No |
| `panel.py`, `panel_cmd.py` | 525, 87 | Panel template and tier validation, environment selection, `review panel resolve` | MASTER; heavily extended on newer master by #519 (+206 lines, grep only) | No |
| `telemetry.py`, `telemetry_cmd.py` | 447, 98 | review-telemetry/1 records, JSONL store, SQLite `model_scores` view | MASTER; no product caller (code-panel.md:94) | No |
| `data/review-panel.default.json`, `review-panel.live7.json`, `review-tiers.default.json` | 13, 15, 32 | @default (4 reviewers), @live7 (7 reviewers), tier model lists | MASTER; newer master adds six `review-panel.reflect-*.json` and a `classes` map (grep only) | No |
| `prompts` (document_review_loop_prompts.md) | 74 | FIRST-REVIEW, RE-REVIEW, REVISE briefs, findings and fix-map contracts, panel run instructions | MASTER | Spec-shaped, scoped to `/sc:spec-panel --mode critique` (prompts:3) |
| `spec-panel.md` Review Loop + hard gate | 256-268 | Loop rules (grading, verdict, cap 3, reviser contract) and the gate that forces reading the prompts file | MASTER | No |
| Proposed product changes from this study | n/a | Three harness fixes named in CR:371 (anchor limit, source path in brief, keep identity audit and ladder fix). None were implemented in `src/` | Proposal only | Mixed (section 6) |

## 2. Findings

### 2.1 What was run (sample sizes)

| Phase | Dates (UTC) | What | Sample | Source |
|---|---|---|---|---|
| Pilot | 2026-11-11 | Arms A (sonnet alone), B (@default minus Qwen), C (@live7 minus Qwen); one run per reviewer per package; 9 blind Opus judges | 3 packages x 3 arms | PILOT:5-14 |
| Batches 1-3 | 2026-11-11 to 11-12 | 15 owner-ordered combos, then 12 "plus one reviewer" rows; one run each | single runs | CR:5-11, CR:84-102; SPEC:8-75 |
| Batch 4-5 | 2026-11-12 | source.md shipped; 16 rows, glm dropped | single runs | CR:109-129; SPEC:90-114 |
| Batch 6-7 | 2026-11-12 | ember replaces wonder; ember/luna/haiku/grok rows | single runs | CR:150-193 |
| Batch 8-9 | 2026-11-12 | Replicates: 4 runs per combo (300 then 120 reviewer runs) | 4-6 runs per panel | CR:202-270 |
| Batch 10 | 2026-11-13 | grok+sonnet, haiku+sonnet | dropped and excluded by owner | SPEC:143-148; session record |
| Batch 11 | 2026-11-13 | sonnet + 2x luna, 5 more replicates (45 runs) | n=6 with the original | CR:421-428 |
| Final analysis | 2026-11-13 | 71 valid-era rows, 213 row-packages, 665 valid-era runs; 106 scored panel runs in the all-sets table | see each finding | CR:290, CR:301, CR:373, CR:431 |

### 2.2 Results (final, valid era unless noted)

All "Found" numbers are means per row over the two defect-rich packages. Rows with 1 run are anecdotes (CR:361).

| # | Finding | n | What the evidence shows | What it does NOT show | Confounders | Checked by | Source |
|---|---|---|---|---|---|---|---|
| R1 | Catch ceiling: every panel finds about 2-2.5 of 14 defects; no row exceeded 4/14 | 71 rows | A hard ceiling across all model mixes tried | That the ceiling is a model limit: it may be the brief, the packages or the GT | Brief never names source.md (R13); merge drops (D1) | Audits A-F; F recompute | CR:274, CR:371, CR:428 |
| R2 | Four issues were never found by any of 106 runs: B1, B2 (designSpec Task 1 inventory and scope), I5 (CHANGELOG enum), I6 (alias user-guide caveat); B6 found once | 106 runs | These defects are out of reach of every model mix tried | Why: no causal test of brief or GT wording | Same as R1 | All-sets table cross-checked by 10 agents and a script, 0 mismatching cells | CR:431, CR:497, CR:501 |
| R3 | Three issues carry almost all catches: B3 (95 of 106 runs), I8 (76), I2 (71) | 106 runs | Scores are dominated by easy defects | Ranking power on hard defects | Package-specific | Same | CR:502 |
| R4 | Default panel: ember + 2x luna, 1.83/14, real blocking 0.17/8, wrong blockers 1.83, control 0.83/2, 63,644 tokens, ~6 min elapsed | 6 runs | Cheapest replicated panel with quality statistically indistinguishable from the others | That it is "as good" on hard defects: it reached only B3, B7, I2, I8 (4 distinct issues) | Ember skipped source.md in 9 of 18 runs and had findings dropped in 2 (CR:382) | Audits C, D, F; permutation tests | CR:366, CR:378, CR:428, CR:504 |
| R5 | sonnet + 2x luna is NOT the standard: 2.33/14, real blocking 0.33, control 1.33, 139k tokens, 821 s; the first run's 4/14 was an outlier | 6 runs | Indistinguishable from ember + 2x luna on catch, blocking, wrong blockers and control (p 0.28-1.0) at 2.2x tokens and 2.4x time (p 0.003) | That sonnet adds nothing: it reached control GT1 (I7) in 3 of 6 runs vs 0 of 6 for ember + 2x luna (Fisher p ~0.012, post-hoc, exploratory) | Non-random sets | Batch 11 integrity: all 45 runs model_ok, API-error audit bad=0 | CR:421-428 |
| R6 | Best real-blocking panel: haiku + 2x luna, 1.2/8 real blocking, 2.2/14, 3.0 wrong blockers, 191k tokens | 5 runs | Highest measured real-blocking mean among replicated panels | Significance vs others (not shown as significant) | Judge-blocking is 1.4 (CR:291) | Audit F | CR:291, CR:367 |
| R7 | Best precision: ember + sonnet, 2.5/14, 0.25 wrong blockers, but 0.25 real blocking, 143k tokens | 4 runs | Fewest wrong blockers | Better catch (within noise) | none noted | Audit F | CR:368 |
| R8 | Only three statistical effects survive (Welch and permutation, n=4-6): a second luna raises control found by +0.83; 2x luna + 2x ember has 2.75-3.25 more wrong blockers than every comparator; ember + terra finds 1.75 fewer | 4-6 runs per panel | These three effects | Every other "beyond noise" claim in older sections | Control baseline had zero variance, so the luna effect is fragile (CR:239) | Audit F | CR:298 |
| R9 | Panels of 5 reviewers buy no catch gain for 2-4x the cost | 4 runs each | No gain at this sample size | That more diverse 5-panels never help | n/a | Audit F | CR:286, CR:369 |
| R10 | Sonnet is associated with rare issues: in all 3 sets that reached I4, 3 of 4 sets that reached B5, 13 of 16 runs that reached I7 | 106 runs | Association | Causation (sets are not random) | Panel composition | All-sets cross-check | CR:503-505 |
| R11 | Single-run highs never replicated: grok + 2x haiku + sonnet 4/14 with 3 real blocking (594k tokens); haiku + sonnet + wonder 4/14 | 1 run each | Possible ceiling-breakers | That they replicate; the nearest relative (same four plus ember) scored 2/14 | Run-to-run variance is large (CR:171) | n/a | CR:370 |
| R12 | Pilot: sonnet alone was the most efficient arm (2.15 catches per 100k tokens); all arms caught 0/8 blocking; bigger panels added non-blocking rows | 3 packages | Pre-source.md behaviour | Valid-era behaviour (source.md missing; luna numbers quarantined) | Missing source.md; Qwen removed from B and C | Not re-audited for the valid era | PILOT:44-71; CR:107 |
| R13 | Inputs matter: without source.md, sol and terra returned "incomplete" with 0 findings and luna refused 25 of 25; after shipping it, every model produced blocking findings | all batch 1-3 runs | The harness gap, not model ability, drove early zeros | That shipping source.md raised recall (the "8/14" headline was a corrupted judge, see 2.3) | n/a | Audit C | SPEC:91, SPEC:103; CR:106, CR:148 |
| R14 | Even with source.md present, 156 of 665 valid-era runs never referenced it: ember 81/209 (39%), luna 49/222 (22%), haiku 15/75, grok 4/24, wonder 6/25, sonnet 1/63, terra 0/44, sol 0/3 | 665 runs | Many reviewers reviewed source-blind | Cause; "the brief never names source.md" is an inference, UNVERIFIED | Part of ember and luna's low catch is likely this (CR:293) | Audit C | CR:373 |
| R15 | terra and sol still refuse sometimes: 51 reports say incomplete, incl. 16 empty terra reviews in valid rows; ember + terra's 0.5/14 is largely terra returning nothing | valid rows | Refusals persist | Why | n/a | Audit B | CR:294 |
| R16 | Anchor fidelity: luna quotes verbatim in 91.4% of anchors vs 98-100% for others | valid runs | Luna anchors miss more often | Impact on scores (not measured) | n/a | Audit B or D (CR does not say which) | CR:294 |
| R17 | Model presence effects (with vs without): grok 2.62 vs 2.00 found; wonder 2.75 vs 1.98; sonnet 2.43 vs 1.92 found, fewer wrong blockers 1.95 vs 2.68; haiku more blocking 1.30 vs 0.73; ember 1.88 vs 2.55; terra worse; luna neutral | 71 rows | Directions for future tests | Effects (confounded with panel size and cost) | Strong confounding | Not separately audited | CR:275 |
| R18 | Operational: Qwen timed out (3 x 3000 s in pilot); glm slow (805-1435 s) and misrouted; muse-wonder misrouted to terra under load and hit a weekly limit; muse-spark and muse-wonder-full misroute (to sol and sonnet) | operational log | Which models are usable at all | Model quality | Gateway load | Audit A (identity) | PILOT:12; SPEC:3-5, :78, :82, :87-88, :116, :119-120, :131 |
| R19 | Tier aliases (`claude-gw-tierN[1m]`) serve only the first model of a tier, so the study dispatched by raw model id | Stage 0 probe | The product's alias-based dispatch cannot select a tier's other models | Whether the gateway can be steered by alias plus a slot variable (UNVERIFIED) | n/a | probe/probe.json | manifest.md:11 |
| R20 | Merge silently drops findings: 80 reviewer-level cases, 49 blocking findings lost, 4 verdict flips FAIL to PASS, plus total-loss merges; per model: luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet/terra/sol 0 | 264 merges | Long-anchor models are penalised systematically | Exact effect on rankings (not re-scored with the lost findings) | n/a | Audit D | CR:292; audit-D:15-20 |
| R21 | Judging is reliable: 294 judge outputs clean; independent blind re-judge of 12 rows agreed 12/12; 19 of 19 catches confirmed, one borderline (recall 0.95) | 294 judges, 12 re-judged | Judge noise is small relative to panel differences | Judge bias shared by both judges (both Opus, same GT) | Same model family | Audit E | CR:296 |

### 2.3 Retracted or corrected claims (do not reuse these numbers)

| Claim that was retracted | Why | Where corrected |
|---|---|---|
| "n2-sonnet-src caught 8/14 and 5/8 blocking; source.md fixed the panels" | The designSpec judge died with an API error and left a fabricated-looking score.json; re-judged: 2/14, 0/8 | CR:146-148 |
| Early per-model blocking counts (e.g. "grok 0 blocking in 42 runs") | Counter grepped `"blocking":true` without a space; several models write `"blocking": true` | CR:104-106 |
| "r2-sonnet-src is a muse-wonder row" | meta.json shows r2 never contained muse; batch 6 added ember as a 5th reviewer instead of swapping | CR:169-174 |
| "Ember is weaker than wonder" (unqualified) | Rests on 4 single-run rows within the variance the r2 pair shows | CR:172 |
| "A second run of the same model adds nothing"; "haiku overlap 8 of 8" | `attrib.py` credited every reviewer on a merged ledger row, not the ones the judge cited; and the test had no power | CR:195-200 |
| Judge-blocking printed over a denominator of 8 | Included non-blocking defects: 65 judge-blocking catches, only 38 real | CR:291 |
| "Second luna adds +0.5 blocking" | Reversed under the real-blocking metric (falls to 0.17 from 0.50) | CR:291 |
| Audit C count 161 runs skipped source.md | Pre-skip count; final is 156 of 665 after excluding batch 10 | CR:293 vs CR:373 |
| "sonnet + 2x luna as standard panel" (decision update) | Batch 11 replication: n=6 mean 2.33, indistinguishable; REJECTED | CR:383 vs CR:421-428 |
| "Batch 10 outage runs were not moved" | They had been moved into quarantine and left with empty rerun stubs | SPEC:148 |
| All earlier tables, rankings and luna statements | Superseded by the final section | CR:289, CR:297 |

### 2.4 Defects found in the merge, ledger, panel, telemetry, briefs and harness

Status: **OPEN** = not fixed anywhere seen; **FIXED (harness)** = fixed in `EVAL/tools/run-reviewer.sh` only; **master?** = newer master may address it, grep only, UNVERIFIED.

Merge and ledger (product code)

| ID | Defect | Code evidence | Seen in the study | Status |
|---|---|---|---|---|
| D1 | **200-character anchor drop.** A finding whose `anchor` or `anchor2` is over 200 characters (after whitespace flattening) is dropped whole, with no repair or truncation. Same for claim over 300, more than 8 refs, id over 16 chars, bad severity, MINOR marked blocking | findings.py:104-110 (anchor/anchor2 12..200), :111-117 (refs), :118-120 (claim 300), :26 (id), :96-101 | anchor >200: 56; anchor2 >200: 18; claim >300: 14; bad severity 3; bad refs 1; 49 blocking findings lost; verdict flips g3-sonnet-luna-ember-r3/alias, g5-ember2-luna-r2/alias, n5-sonnet-ember/design plus total-loss merges (audit-D:16-20; CR:292) | OPEN on the branch. master (grep only): `findings_v2.py` keeps anchor and citation quote at 12..200 and claim at 300 (origin/master findings_v2.py:80, :111, :126, :132, :136) |
| D2 | Partial-panel failure is invisible to the verdict. The merge refuses a round only when no reviewer has a valid block; one broken reviewer leaves a stdout warning with the first error only, and the merged report prints only `block ok false` | ledger.py:127-134, :150-157, :421-424; merge_cmd.py:117-118 | 80 reviewer-level `block ok false` cases (audit-D:7) | OPEN |
| D3 | Docstring says an invalid-block reviewer "is skipped for clearing"; the clearing loop ignores `block_ok`, so a row only that reviewer would refind is cleared | ledger.py:112 vs :254-258 | Not exercised (all study ledgers are round 1, audit-D:3) | OPEN |
| D4 | Over-merging: union-find over `same_defect` with a 3-line span tolerance chains distinct nearby defects into one row; same-reviewer findings merge too; the row keeps only the first member's anchor and claim | findings.py:367-407; ledger.py:182-199 | 83 mega-cluster rows; 195 of 1,398 rows with 3+ members are chains; r2-sonnet-ember/designSpec L1 has 19 members across 8 sections (audit-D:29) | OPEN |
| D5 | Ref mismatch splits one defect: span matching requires refs to intersect or both be empty, and refs are scraped from free text (claim, anchor) | findings.py:321-337, :373-378 | Not measured | OPEN |
| D6 | Anchor not found in the document: kept with span None and section "none"; such a row can never be refound by span or move to `resolved_check`; `anchor_status` and `anchor_ambiguous` are computed and never read | findings.py:349-358 | 46 rows with span null, 13 blocking (audit-D:30) | OPEN |
| D7 | Tasklist task ids such as `T01.02` are not recognised as refs (`_REF_TOKEN` needs `[A-Z]{1,4}-[0-9]`) | findings.py:29 | Verified by the note author with a direct call (code-panel.md:168) | OPEN; tasklist-specific |
| D8 | Any single blocking finding from any one reviewer fails the round; `confidence` (single or overlap) is computed and printed but never used | ledger.py:86-90, :99-104, :187, :273-274 | Wrong blockers 1.8-4.75 per row on defect-rich packages (CR:304-337) | Design choice; OPEN question (section 4) |
| D9 | A refound row takes the current round's blocking call, so with the re-review panel collapsed to one reviewer, that one reviewer can downgrade a blocker the full panel raised | ledger.py:210-218; panel apply_to (code-panel.md:30) | Not exercised (round 1 only) | OPEN |
| D10 | A cluster matches only the first existing row (`break`) | ledger.py:165-171 | Not exercised | OPEN |
| D11 | `ledger revise` can run twice for one round and remap spans twice; the new text's hash is not stored, so the next round's `--doc` is not checked against it | code-merge.md:135-136 (ledger.py:301-347, not re-read here) | Not exercised | OPEN, UNVERIFIED by this author beyond the note |
| D12 | `merge` always exits 0; only `ledger verdict` maps decisions to exit codes 0/10/11 | merge_cmd.py:117-118; code-merge.md:123 | n/a | OPEN, LOW |
| D13 | A `--report` id missing from `--resolution` silently gets model None; reviewers in the resolution without a report are not detected | merge_cmd.py:94 | 6 WARN resolution lists a reviewer with no run output (audit-A:31) | OPEN, LOW |

Panel, tiers and telemetry (product code)

| ID | Defect | Evidence | Seen in the study | Status |
|---|---|---|---|---|
| P1 | `distinct_across_slots` silently falls back to duplicates when exclusion empties the pool | panel.py:405, :408 | @default and @live7 gateway resolve t3-1 and t3-2 both to Qwen3.8-max; 26 of 40 @live7 run ids hold a duplicate (code-panel.md:64; tests-tools.md:37) | master?: origin/master panel.py adds `hard_exclude` and `strict_distinct` (lines 506-519, grep only) |
| P2 | Gateway environment has an empty `launch` map ("dispatch mechanism per model not defined yet"), so every gateway reviewer resolves with `launch: null` | tiers.json:19-24 | The study bypassed the panel and dispatched raw ids (run-reviewer.sh:48; manifest.md:11) | OPEN |
| P3 | Tier data lacks muse-ember-1.0, the model in the recommended default panel; SPEC says the owner was adding it as Tier 04 Model 02 | tiers.json:4-11; SPEC:120 | Every ember row was dispatched outside the panel | OPEN; master diff for this file only adds a `classes` map (git diff ec259f1b7..origin/master) |
| P4 | Excluded models (Qwen3.8-max owner-excluded; glm excluded from batch 4 on) still sit in tier2, tier2b and tier3 lists | tiers.json:7-9 | Panel resolution keeps picking Qwen (code-panel.md:63-64) | OPEN in data; master `hard_exclude` may cover it at call time (UNVERIFIED) |
| P5 | Environment is guessed from `$T3Model01`; the TxModelNN slot variables (incl. T2bModel01) are never read to choose models | panel.py:365-374 | Shell had T3Model01=glm-5.3 while resolution picked Qwen (code-panel.md:57) | OPEN |
| P6 | Re-review resolves to the single fixed anchor (sonnet) because both templates set `apply_to: ["first"]` | code-panel.md:30 (panel.py:449-454, review-panel.*.json:7) | Not exercised (first reviews only) | Design choice; OPEN |
| P7 | `round_robin` uses today's date when `--sequence` is absent, so resolution changes by day | code-panel.md:31, :177 | n/a | OPEN, LOW |
| T1 | Telemetry is not wired: no product caller of `append_record`; `model.observed` has no producer, so the `model_scores` view is empty without an external harness | code-panel.md:94-95 | The study recorded identity in its own `meta.json` instead (run-reviewer.sh:58) | OPEN |
| T2 | Telemetry strata hard-code `sonnet` and `haiku` | code-panel.md:89, :181 (telemetry.py:112-115) | Gateway models cannot be stratified | OPEN, LOW |

Briefs and prompt contract

| ID | Defect | Evidence | Seen in the study | Status |
|---|---|---|---|---|
| B-1 | The reviewer brief never names the source or driving document; it reviews the candidate "against the requirements it states" and has no SOURCE placeholder | prompts:17-21, :32; run-reviewer.sh:15 | 156 of 665 runs never referenced source.md (CR:373) | OPEN; fix proposed (CR:371) |
| B-2 | Parser limits are not in the prompt: claim <= 300, refs <= 8, id <= 16 chars, "MINOR cannot be blocking". The anchor 12-200 rule IS stated in both the prompt and the harness brief, and luna, ember and wonder still broke it | prompts:60; run-reviewer.sh:17; findings.py:26, :100-120 | D1 counts | OPEN. Lesson: an instruction alone did not hold |
| B-3 | Severity vs blocking: spec-panel says "CRITICAL is blocking"; the prompt requires the grading sentence for every blocking finding; code accepts CRITICAL non-blocking. "Medium" is not a severity value (it is MAJOR with blocking false) | spec-panel.md:259; prompts:31, :60; findings.py:100-101 | Not measured | OPEN |
| B-4 | Report ending conflict: spec-panel says the last line is `verdict:` with the Reviser brief above it; the prompt says the last section is `## Findings block`. The parser tolerates both | spec-panel.md:260, :263; prompts:58 | The harness brief asks for the findings block then a final verdict line (run-reviewer.sh:17) | OPEN, LOW |
| B-5 | No guidance on what to anchor for a `missing-requirement` finding, on uniqueness, or on whitespace and markdown in anchors | prompts:60; findings.py:349-352 | D6 (46 unanchored rows) | OPEN |
| B-6 | Harness brief listed category `unpassable-ac`; the parser accepts only `unpassable-check` | SPEC:38-39; PILOT:13 | 9 pilot reports normalised via `.catfix.md` copies | FIXED (harness): run-reviewer.sh:17 now says `unpassable-check` |
| B-7 | Reviewers are told the merge contract but not its consequence (one blocking row from any reviewer fails the round; the merge, not their verdict line, decides) | prompts:62 vs ledger.py:273-274 | n/a | OPEN |

Evaluation harness and analysis

| ID | Defect | Evidence | Status |
|---|---|---|---|
| H1 | Cyclic fallback ladder spun 69 steps in 3 s during a `claude` binary outage and ran an ember slot on haiku and another on Qwen (42 min) | SPEC:141; CR:247 | FIXED (harness): no revisit, `EXCLUDE_MODELS`, `NOFALLBACK=1` (run-reviewer.sh:66-83) |
| H2 | On fallback, `expected_model` in meta.json is overwritten with the fallback model, so the per-run identity check cannot catch a ladder swap | run-reviewer.sh:58, :76 | OPEN in script; mitigated by audit A cross-checks (audit-A:11-12) and `NOFALLBACK=1` in batch 11 (CR:422) |
| H3 | Attempt counter resets per fallback model, so a fallback's attempt files overwrite the primary's; cost.json undercounts and the primary's raw output is lost | run-reviewer.sh:76, :85-87 | OPEN |
| H4 | `BLOCK_OK` checks only that a line starts with ```` ```findings-v1 ````; it does not parse the block, so D1 drops are not caught at run time | run-reviewer.sh:57 | OPEN |
| H5 | Stale attempt files from earlier runs inflate cost for 5 runs | audit-A:15-16 | Disclosed |
| H6 | Stale merges: n2-terra and r2-sol merged before reports were re-run; n5-sol and n5-terra merged from a report no longer in the row | audit-D:10, :23, :25; CR:292 | Disclosed; flagged EXCLUDE |
| H7 | A judge that died on an API error left a plausible score.json | CR:146-147 | FIXED by procedure: per-batch API-error audit (e.g. CR:177, CR:203) |
| H8 | Blocking counted by grep without space tolerance | CR:105 | FIXED |
| H9 | `attrib.py` attribution by ledger membership | CR:197 | Retracted; not fixed in the script |
| H10 | Analysis scripts read or `exec` `/tmp` copies | final-table.py:23, three-way.py:4, b9-table.py:3, issue-setup.py:3 | OPEN (reproducibility) |
| H11 | 12 concurrent workers caused gateway model-identity bleed (muse served as terra) | SPEC:77-79 | Mitigated by concurrency caps (SPEC:79, :99) and zero-load probes |
| H12 | `claude` binary replaced mid-run three times (batch 9, 10, 11), exit 127 | SPEC:141, :148, :152 | Mitigated by quarantine and single re-run with `NOFALLBACK=1` |

## 3. Lessons and strategies

### 3.1 Methods that worked

| Method | How it was done | Why it worked | Source |
|---|---|---|---|
| Ground truth from implement history | Each GT item is a defect that actually cost a past implement run (retries, halts, owner checks), with evidence file:line, a plan quote whose grep count is verified, and `blocking_in_implement`; a draft GT is kept beside the final one; GT files are hashed in the manifest | Scores measure "would this panel have prevented real pain", not opinion. Novel real catches score as wrong blockers (a known bias) | ground-truth.json `verification` block; manifest.md:13-16; PILOT:79 |
| Control package | One package whose defects were not blocking measures false alarms on a clean-ish plan | Separated precision from recall; produced the only surviving doubling effect | CR:9; CR:298 |
| Blind scoring | Merged reports anonymised (reviewer ids to R1..Rn, paths redacted) under random labels; one Opus judge per (row, package) reads GT, candidate and the anonymised report only; strict "same defect" rule; schema-fixed score.json | Judges cannot favour models; audit E re-judged 12 rows with 12/12 agreement | PILOT:14; CR:10; judge-one.sh:12-23; CR:296 |
| Reviewer sandbox | Reviewers ran in `/tmp/evalsb/repo`, a git archive of HEAD without `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research`; edit tools disallowed | No reviewer read GT, other reports or implement history (audit C) | manifest.md:10; run-reviewer.sh:48; CR:373 |
| Model identity from the transcript | Observed model = the main-thread assistant `message.model`, compared to the requested id; zero-load probes before resuming a model | Caught gateway misrouting (muse served as terra; glm as qwen) | run-reviewer.sh:51-56; SPEC:82, :88 |
| Quarantine in place, never delete | Contaminated or outage runs renamed with a suffix and re-run once | Full audit trail; audits could re-check everything | SPEC:78, :141, :152 |
| Replicates | 4-6 runs per panel from batch 8 on | Exposed regression to the mean (sonnet + 2x luna 4/14 to 2.0/14) | CR:202-203, CR:424 |
| Six independent integrity audits before the final decision | Identity, report validity, inputs and timing, merges, scoring, aggregation, each read-only with flags.tsv | Found the 200-char drop, source-blind runs, stale merges, the blocking-metric error; no fabricated scores | CR:290-298; audit-A, audit-D |
| Two views of every table | AS-SCORED and AUDIT-CLEAN (drops flagged row-packages) | Robustness check without hiding data | CR:303-361 |
| Dual independent counting | Issue tables built by 10 agents and recomputed by a direct script: 0 mismatches (320 cells; 62 sets x 16 issues) | Removed transcription error | CR:386, CR:431 |
| Permutation tests on run-level values | Welch plus permutation; Fisher exact for rare issues, marked post-hoc | Killed most "beyond noise" claims | CR:298, CR:425-426 |
| Run scheduling | Separate streams with per-model caps (ember -P4, others -P6; muse capped at 4; 10 concurrent total); serial waves after contamination; cooldowns of 60-90 min after misroutes; `NOFALLBACK=1` for replicates so outages show as failures | Kept identity clean after the early bleed | SPEC:79, :85, :99, :151 |
| Append-only ops log | Every owner order, outage, correction and quarantine written into SPEC.md with UTC times | The final audit could reconstruct eras and exclusions | SPEC:77-152 |

### 3.2 Methods that failed

| Method | What went wrong | Source |
|---|---|---|
| Ranking single runs | Batch 1-7 rankings flipped on replication; the r2 pair alone showed 4/14 vs 2/14 for nearly the same panel | CR:171, CR:200, CR:424 |
| Attributing catches by ledger-row membership | Credited every reviewer on a merged row; inflated "doubling adds nothing" and "haiku overlap 8/8" | CR:197 |
| Counting blocking with a literal grep | Missed `"blocking": true` with a space | CR:105 |
| Trusting a judge file without checking the transcript | One API-error judge produced the study's headline (8/14) | CR:147 |
| Starting batches before an end-to-end harness check | source.md not shipped for about 1.5 days (luna, terra, sol refusals); wrong category label in the brief; both found only after batches ran | SPEC:38-39, :91, :103 |
| Cyclic fallback ladder with overwritten `expected_model` | A binary outage silently swapped models; would have passed the identity check | SPEC:141 |
| High concurrency on a shared gateway | 12 workers caused model-identity bleed; whole batch torn down | SPEC:77-79 |
| Tier aliases for dispatch | Serve only the first model of a tier | manifest.md:11 |
| One metric name for two things | "Blocking" mixed judge-blocking with real blocking for most of the study | CR:291 |
| Keeping analysis live in /tmp | Committed scripts do not reproduce without the /tmp copies | final-table.py:23; three-way.py:4 |
| Leaving superseded text in place | The report carried retracted numbers next to new ones until the final section declared supersession | CR:297 |

### 3.3 What to do differently next time

| Change | Why |
|---|---|
| Run a one-package smoke test of the full chain (reviewer, `superclaude review merge`, judge) and inspect the merge warnings before any batch | Would have caught the missing source.md, the category label and the 200-char drops on day 1 |
| Validate each report with the real parser at run time (e.g. call `findings.parse_block` and fail or re-ask when any line is dropped), instead of the presence-only `BLOCK_OK` | D1 and H4 |
| Name every input file in the brief, and check from the transcript that each one was read | R14 |
| Pre-register metrics (found, real blocking, wrong blockers, control) and the decision rule, and keep using them; the pilot had a rule (PILOT:56) that later batches did not apply | Avoid metric drift (CR:291) |
| Plan replicates (4+) and a power estimate from the start; treat n=1 rows as screening only | CR:361 |
| Keep raw identity evidence even when transcripts are not committed: per-turn observed model and token counts in the committed meta | H2, H3; raw files are uncommitted |
| Double-score a random sample of judges from the start, ideally with a second judge model family | Audit E did 12 rows late; both judges were Opus |
| Keep analysis scripts self-contained in the repo, reading committed inputs only | H10 |
| Score the raw union of reviewer findings as well as the merged ledger, to separate model recall from merge loss | D1, D4 |

## 4. Decisions made and decisions still open

### 4.1 Decisions made

| # | Decision | When (UTC) | By | Why | Source |
|---|---|---|---|---|---|
| DM1 | Qwen3.8-max excluded from all panels | 2026-11-11 pilot | Owner | All 3 pilot slots timed out (2 x 3000 s each, 0 tokens) | PILOT:12; SPEC:1-3; session record |
| DM2 | Dispatch reviewers by raw gateway model id with `claude -p`, not by tier alias | 2026-11-11 Stage 0 | Eval coordinator | Aliases serve only the first model of a tier | manifest.md:11 |
| DM3 | Reviewers run in a sandbox without implement history, other evals or research | 2026-11-11 | Eval coordinator | Prevent leakage of ground truth | manifest.md:10 |
| DM4 | Category label fix: normalise `unpassable-ac` to `unpassable-check` with `.catfix.md` copies, originals unedited | 2026-11-11 | Coordinator | Parser accepts only `unpassable-check` | SPEC:38-39; PILOT:13 |
| DM5 | Tear down the 12-worker batch 3, quarantine, cool down, re-run serially with identity stop rule | 2026-11-11 22:43 | Owner | Gateway model-identity bleed | SPEC:77-85 |
| DM6 | Ship source.md next to the candidate | 2026-11-12 | Owner request (batch 4) | sol/terra/luna refused without it | SPEC:90-95 |
| DM7 | glm excluded from batch 4 on | 2026-11-12 14:42 | Owner | "massive delays" | SPEC:97-98; session record |
| DM8 | Quarantine all pre-source.md luna data; only `-src` luna runs may be cited | 2026-11-12 15:16 | Owner | Those runs measured a harness gap | SPEC:102-103; CR:107 |
| DM9 | Replace muse-wonder with muse-ember-1.0 (owner adding it as Tier 04 Model 02) | 2026-11-12 ~17:57 | Owner | wonder hit its weekly limit | SPEC:119-120 |
| DM10 | Fallback ladder v2 (tier-ordered), then v3 guards (no revisit, exclusions, `NOFALLBACK`) | 2026-11-12 18:10 and after 22:19 | Owner, then coordinator | Every model needs a fallback; then the cyclic ladder incident | SPEC:130-131, :141 |
| DM11 | Replicate study (4 runs per combo) | 2026-11-12 20:37 | Owner | Single runs indistinguishable; doubling claim retracted | SPEC:137-138 |
| DM12 | Testing closed; batch 10 dropped and excluded | 2026-11-13 01:09 | Owner | "we're done testing, we're going to decide and run with it" | SPEC:146-147; CR:290; session record |
| DM13 | Real blocking (judge-blocking AND `blocking_in_implement`) is the blocking metric | 2026-11-13 | Coordinator after audit F | Judge-blocking overcounted (65 vs 38) | CR:291 |
| DM14 | Final panel guidance: default = ember + 2x luna; optional quality tier = sonnet + 2x luna only if issues like control GT1 matter; haiku + 2x luna = best real blocking; do not use ember + terra, 2x ember + 2x luna, terra or sol alone, haiku + ember + terra, any 5-reviewer panel, anything relying on muse-wonder | 2026-11-13 after batch 11 | Owner direction, recorded by coordinator | Replicated, cheapest, same measured quality | CR:363-369, CR:428 |
| DM15 | Fix the harness before any further model testing: anchor limit, source path in the brief, keep identity audit and ladder fix | 2026-11-13 | Coordinator recommendation | All panels sit at ~2-2.5/14; these are "the biggest lever" | CR:371, CR:428 |
| DM16 | Raw transcripts left out of commits | 2026-11-13 | Owner | Keep repo small (~1.5 GB) | RAW-TRANSCRIPTS-NOT-COMMITTED.md:2; session record |
| DM17 | Never stage `.claude/`; change nothing under `.dev/tasks/`; read-only repo for workers | whole study | Owner | Standing rules | SPEC:33; session record |
| DM18 | No PR; push the research branch to the fork only | 2026-11-13 | Owner | Research artifact, not a product change | session record; branch equals its origin copy (section 1.1) |

### 4.2 Decisions still open

| # | Open question | Who must decide | Inputs available |
|---|---|---|---|
| DO1 | How to stop D1: raise the anchor limit, truncate long anchors at merge, re-ask the reviewer, or keep the limit and only report drops | Owner, with the maintainer of `superclaude review` (and the reflect panel work, since master's `findings_v2.py` keeps the same limits) | D1 counts by model (audit-D:17) |
| DO2 | Should one broken reviewer make the round invalid, or at least be printed in the merged report with its dropped lines? | Owner / panel maintainer | D2, D3 |
| DO3 | Keep "any single blocking finding fails the round", or require overlap, a quorum, a calibrator or an evidence validator | Owner, after comparing with reflect Tier 2's calibrator and validator | D8; wrong blockers 1.8-4.75 per row (CR:304-337) |
| DO4 | How tasklist review is run in the product: through the spec-panel review loop and `superclaude review` (what this study measured), or through reflect UC-1 `--mode pre` (what sc:workflow Wave 4 and sc-tasklist Stage 10.5 actually call today) | Owner plus the unification session | code-panel.md:191-194; sc-workflow-protocol SKILL.md:60 |
| DO5 | Put the decided panels into product data: add muse-ember to the tier file, add templates for ember + 2x luna and sonnet + 2x luna, remove or hard-exclude Qwen and glm | Owner (tier list is owner-controlled; SPEC:120) | P3, P4; DM14 |
| DO6 | Define gateway dispatch for named models (the empty `launch` map) | Owner / gateway maintainer | P2; R19 |
| DO7 | Re-run the decided panels after the harness fixes, before adopting them as product defaults? | Owner | DM15 |
| DO8 | Raw transcripts: commit (LFS), archive elsewhere, or delete; reconcile the 2,916 vs 1,689 count | Owner | Section 1.1 |
| DO9 | Replicate the muse-wonder rows when quota returns (CR:284)? Testing is closed, so this is a new study | Owner | CR:284 |
| DO10 | Wire telemetry (who writes `reviewer_run` and `outcome` records, and how `model.observed` is captured) | Panel maintainer | T1; run-reviewer.sh:51 shows one way to capture it |
| DO11 | Does the brief grow a source or driving-document placeholder for plan and tasklist review? | Owner / prompt maintainer | B-1; R14 |

## 5. The Review Panel as understood now

Scope: the product panel on the branch base (spec-panel review loop plus `superclaude review`), and how the study used it. Reflect Tier 2 is summarised only for contrast, from code-panel.md section 5; this author did not re-read the reflect sources, and origin/master #519 has changed them since.

### 5.1 Roles

| Role | In the product (branch base) | In the study | Driven by |
|---|---|---|---|
| Orchestrator / coordinator | Keeps the review count, the prior report and the baseline copy; spawns reviewers; runs the scripts | Supervised Orca workers (one per row) and shell launchers | spec-panel.md:256-268; prompts:68-70; SPEC:18-36; `startcombo*.sh` |
| Panel resolver | `superclaude review panel resolve --run-id --kind` turns a template plus tier file plus environment into reviewer ids and models | Used to produce `resolution-live7.json`; per-row resolutions were then rewritten with `jq` to the row's raw models | panel.py:427-525 (code-panel.md:29-33); SPEC:26 |
| Reviewer | One fresh context per reviewer, same brief, none sees another's report; writes a report ending in a findings-v1 block | `claude -p --model <raw id>` in a sandbox, edit tools disallowed, brief begins with `/sc:spec-panel @candidate --mode critique` | prompts:27-33, :70; run-reviewer.sh:13-17, :48 |
| Calibrator | None. `confidence` single/overlap is computed and printed, never used | None | ledger.py:86-90 |
| Merge (the "judge" of the loop) | Deterministic script: parse, annotate, cluster, match to ledger rows, any-blocking verdict | Used once per row-package (round 1 only) | merge_cmd.py:71-118; ledger.py:107-298 |
| Scoring judge (eval only, not a panel role) | n/a | Blind Opus per (row, package) against GT | judge-one.sh |
| Reviser | Repairs only the Reviser-brief ids and returns a fixmap-v1 block | Not exercised | prompts:51-54, :66 |
| Revision recorder | `superclaude review ledger revise` moves applied and touched rows to `resolved_check` and remaps spans | Not exercised | prompts:70; code-merge.md:121 |
| Human | Escalation at review 3; `ledger defer`; follow-up issue question | Owner orders | spec-panel.md:260-261; prompts:13 |
| Auditor (eval only) | n/a | Six read-only audits | analysis/audits/ |
| Telemetry writer | None in the product | The study's own meta/cost files | code-panel.md:94; run-reviewer.sh:58, :87 |

### 5.2 Data contracts

Reviewer to merge: the findings-v1 block

| Field | Prompt says (prompts:58-62) | Code enforces (findings.py) | Gap |
|---|---|---|---|
| Location | Last section `## Findings block`, one fenced block, info string `findings-v1` | Any heading level, case-insensitive; first such heading; info string must be the single token `findings-v1`; more than one block = invalid, last used; unclosed = invalid but parsed (:27, :31, :38-76; code-merge.md:19-25) | Two-token info strings not found (code-merge.md:147) |
| `id` | example `F1` | `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$`, unique (:26, :92-95) | Limit not stated |
| `severity` | CRITICAL, MAJOR or MINOR | Same, case-sensitive (:14, :96-97) | "Medium" is a grade, not a value (prompts:31) |
| `blocking` | true only if the grading check passes | Boolean; MINOR + blocking rejected (:98-101) | MINOR rule not stated |
| `category` | 6 values | Same 6 (:15-22, :102-103) | none |
| `anchor`, `anchor2` | 12-200 chars copied exactly; anchor2 for contradictions | 12..200 after whitespace flattening; else the whole finding is dropped (:104-110) | D1 |
| `refs` | requirement ids and section numbers | list of at most 8 strings (:111-117); only `XX-n(.n)`, `P0-P9` and pure section numbers survive normalisation (:29-30, :321-337) | D7 (task ids lost) |
| `claim` | one sentence | at most 300 chars, may be empty (:118-120) | Limit not stated |
| Prior line | `{"prior": "L3", "status": ...}` on re-reviews | Notes only; reviewers cannot change a status (ledger.py:259-272) | n/a |
| Confidence | not a reviewer field | Ledger-computed `single` or `overlap` (ledger.py:86-90) | Unused in verdict |
| Unknown keys | n/a | Accepted silently (code-merge.md:38) | Room for reflect fields |

Other contracts

| Contract | Shape | Source |
|---|---|---|
| Resolution (resolver to merge) | `review-panel-resolution/1`: reviewers[] with reviewer_id (`<slot>-<i>`), slot_id, tier, alias, strategy, seed, model, fallback_depth, stand_in, fallbacks, launch; plus template and tier versions and sha256, environment, run_id, review_kind. The merge reads only reviewer_id and model | code-panel.md:33; merge_cmd.py:73-83 |
| Ledger | `review-ledger/1`: rounds[] (n, doc_sha256, reviewers[{reviewer_id, model, report, report_sha256, block_ok}], verdict, decision, brief_ids) and rows[] (lid, fp, blocking, severity_max, category, confidence, status, anchor(2), span(2), refs, claim, members, history) | ledger.py:184-202, :276-285 |
| Row statuses | open, resolved_check, resolved, regressed, deferred | code-merge.md:111-120 |
| Verdict and decision | FAIL if any blocking row is open or regressed; decision PASS, REVISE (round < cap) or ESCALATE; `ledger verdict` exit 0/10/11 | ledger.py:93-104, :273-275; code-merge.md:123 |
| Merged report | `review: N of cap` header, reviewer list with `block ok`, full ledger table, blocking findings, other findings, Reviser brief or Escalation, final `verdict:` line | ledger.py:408-437; code-merge.md:99 |
| Reviser output | fixmap-v1 lines `{"id","action","reason"}`, or a `| L3 | applied` table fallback | prompts:66; code-merge.md:121 |
| Capture (study input shape) | `review-capture/1` per round: occasions = reviewers, one defect per row | code-merge.md:124 |
| Study score | score.json: label, combo, package, gt_total, gt_covered_any[], gt_covered_blocking[], ledger_rows_total, ledger_rows_blocking, blocking_rows_gt_matched, wrong_blockers, notes | judge-one.sh:21 |
| Study run record | meta.json: reviewer_id, expected_model, observed_model, model_ok, findings_block, attempt, wall_s, output_tokens_main, output_tokens_all, exit; cost.json: attempts, total_wall_s, total_output_tokens_all | run-reviewer.sh:58, :87 |

Severities and blocking in one sentence: severity is recorded (`severity_max`) and only gates "MINOR cannot be blocking"; the verdict uses only the reviewer's `blocking` boolean, and one blocking finding from one reviewer fails the round (ledger.py:187, :273-274; code-merge.md:102).

Anchors in one sentence: an anchor is an exact quote from the candidate (whitespace-flattened), located at its first occurrence; it sets the span, the section and through them the fingerprint and the clustering; a missing anchor leaves the finding unclusterable by span (findings.py:346-360, :367-379).

### 5.3 Model and tier configuration

| Tier | Gateway alias | Models in order (branch base) | Used in the study as |
|---|---|---|---|
| tier1a | `claude-gw-tier1a[1m]` | opus, sonnet | Opus only as scoring judge |
| tier1b | `claude-gw-tier1b[1m]` | sonnet, sol, muse-wonder-full | Sonnet = fixed anchor reviewer (t1b-1) |
| tier2 | `claude-gw-tier2[1m]` | sol, glm, grok, Qwen, wonder, spark | sol rarely; glm and Qwen later excluded |
| tier2b | `claude-gw-tier2b[1m]` | terra, glm, Qwen, wonder | terra, wonder |
| tier3 | `claude-gw-tier3[1m]` | glm, Qwen | Both excluded in the end; t3 ids reused as labels for luna, ember, haiku |
| tier4 | `claude-gw-tier4[1m]` | luna, haiku, grok | luna, haiku, grok; ember was added by the owner as "Tier 04 Model 02" but is not in this file |

Source: tiers.json:4-11; SPEC:120; SPEC:16 ("reviewer ids are only labels").

Templates: @default = t1b x1 fixed (anchor), t2 x1 random, t3 x2 random, `apply_to: ["first"]`; @live7 = t1b, t2, t2b, t3 x2, t4 x2 (code-panel.md:47-48). Environments: `gateway` (all models, empty launch map) and `anthropic-only` (haiku stands in for tiers 2-4) (tiers.json:18-31). Environment choice: `--env`, then `$SUPERCLAUDE_REVIEW_ENV`, then `gateway` if `$T3Model01` is set, else `anthropic-only` (panel.py:365-374).

How the study diverged from the product configuration: it never used aliases (R19), forced models per reviewer id with `jq` (SPEC:26), used a model not in the tier file (ember), excluded Qwen and glm by hand, and used reviewer ids as labels only (SPEC:16). The decided panels (DM14) therefore cannot be expressed by the packaged templates and tier file today (P3).

Newer master (grep only, not reviewed): adds a `classes` map (model to family) to the tier file, six `review-panel.reflect-*.json` templates, `hard_exclude` and `strict_distinct` in resolution, and `findings_v2.py`, `cluster.py`, `manifest.py`, `card_convert.py`, `verify_cmd.py` (git diff ec259f1b7..origin/master).

### 5.4 How results are recorded and compared

| Layer | Product (branch base) | Study |
|---|---|---|
| Per reviewer | `block_ok`, model and report sha in the ledger round | meta.json identity and token fields; cost.json; fallback.log |
| Per round | verdict, decision, brief_ids | merged-1.md, ledger.json, merge-stdout.txt per row-package |
| Quality | none (telemetry outcome records exist but have no writer) | score.json per (row, package, label) from a blind judge against GT |
| Comparison | `model_scores` SQLite view, empty without a harness (code-panel.md:92-95) | final-table.py (AS-SCORED vs AUDIT-CLEAN), three-way.py, issue tables, all-sets table, permutation tests |
| Metrics | n/a | found /14, real blocking /8, judge-blocking, wrong blockers, control found /2, control wrong blockers, tokens, reviewer-seconds and elapsed seconds, found and real blocking per 100k tokens (CR:300-305) |

### 5.5 What depends on tasklist review and what does not

| Part | Tasklist-specific? | Why | Source |
|---|---|---|---|
| `superclaude review` parse, merge, ledger, panel, telemetry | No | Generic markdown machinery; no "tasklist" string in the module | code-merge.md:155; code-panel.md:189 |
| Ref recognition | Effectively yes: tasklist and plan task ids (`T01.02`) are lost | `_REF_TOKEN` shape | findings.py:29; D7 |
| Reviewer brief | Spec-shaped and scoped to `/sc:spec-panel`; no source-document placeholder, which a plan or tasklist review needs | prompts:3, :17-21, :32 | B-1 |
| Category `unpassable-check` | Fits plan acceptance criteria and spec criteria alike | findings.py:17 | n/a |
| Study packages, GT, candidates | Yes: three `sc:workflow` plan packages | CR:9 | n/a |
| Panel recommendations (DM14) | Measured on plan packages only; transfer to specs, code or other targets is UNVERIFIED | CR:9 | n/a |
| Harness (`run-reviewer.sh`) | Mostly generic; hard-coded `.dev/tasks/done/<pkg>/source.md` and spec-panel brief | run-reviewer.sh:10, :13-17 | n/a |
| Where tasklist review happens in the product today | Not this panel: sc:workflow Wave 4 runs `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` (advisory); sc-tasklist Stage 10.5 runs `/sc:reflect --mode pre --remediate` per phase | sc-workflow-protocol SKILL.md:60, :76; sc-tasklist-protocol SKILL.md:1630; code-panel.md:192-194 | DO4 |

### 5.6 Contrast with reflect Tier 2 (from code-panel.md:143-163; not re-read here)

| Aspect | Reflect Tier 2 | This panel |
|---|---|---|
| Purpose | UC-1 pre-execution coverage of a tasklist vs its spec; UC-2 post-execution deviation audit | Document critique review loop |
| Reviewer agent | `reflect-reviewer` (read-only tools), described as UC-2 (SKILL.md:592, verified) | Unspecified fresh context |
| Finding unit | Markdown deviation table with file:line evidence and HIGH/MEDIUM/LOW | findings-v1 JSON lines with exact-quote anchors and CRITICAL/MAJOR/MINOR |
| Calibration and gates | Blind calibrator per card; evidence-validator re-reads every citation | None |
| Merge | `sc-adversarial` Mode A | Deterministic clustering, any-blocking verdict |
| Loop | No fix loop; Tier 3 remediation opt-in | review, revise, re-review, cap 3 |
| Model selection | `ANTHROPIC_DEFAULT_*_MODEL` aliases (skill) and T2Model0N/T1Model0N (CLI) | tier JSON plus templates (a third registry) |

## 6. What this work needs from the unified panel

Requirements the unified Review Panel must meet so that sc:workflow plan review and tasklist review can move onto it without regression. "Must" items protect something this study measured or the loop already guarantees; "should" items fix a measured weakness.

| # | Requirement | Level | Why (evidence) |
|---|---|---|---|
| U1 | No silent finding loss. Every finding line a reviewer writes is either merged or listed, with its reason, in the merged report; per-reviewer drop counts are recorded | Must | D1, D2: 49 blocking findings lost, 4 verdict flips (CR:292) |
| U2 | Over-long anchors are handled without losing the finding (truncate to a located prefix, accept longer, or re-ask), and the policy is the same in findings-v1 and master's findings_v2 | Must | D1; master findings_v2 keeps 12..200 (grep only) |
| U3 | A reviewer whose output is invalid is visible in the verdict (invalid round, or a degraded-panel flag), and is not counted as having "not refound" a row when clearing | Must | D2, D3 |
| U4 | The brief names every input by role, including the driving document (plan `source.md`, spec, roadmap), and the panel records whether each reviewer read it | Must for plan and tasklist review | B-1; R14 (156 of 665 runs source-blind) |
| U5 | All parser limits appear in the brief, and a test asserts the prompt text and the parser constants agree | Should | B-2; no such test exists (tests-tools.md:34) |
| U6 | Observed model identity per reviewer is captured from the transcript and a mismatch invalidates that reviewer; fallbacks are recorded with the original request, never overwrite it, and can be turned off | Must | R18, H1, H2; muse misroutes (SPEC:82, :116) |
| U7 | A real dispatch path for named gateway models (the study needed raw ids because aliases serve only a tier's first model) | Must for any non-anchor tier | P2; manifest.md:11 |
| U8 | Panel data can express the decided panels: ember + 2x luna (default), sonnet + 2x luna (quality tier), haiku + 2x luna (blocking-focused); the same model twice as two independent runs; ember present in the tier data; Qwen and glm excludable | Must if DM14 is adopted | DM14; P1, P3, P4 |
| U9 | Plan and tasklist ids (`T01.02`, phase ids) count as refs for clustering, or ref syntax is configurable per target | Should | D7 |
| U10 | Keep the review loop guarantees sc:workflow and spec-panel rely on: cap 3 reviews, Reviser brief limited to blocking ids, `resolved_check` only via the revise script, escalation at review 3 | Must | prompts:13, :53, :70; spec-panel.md:261-263 |
| U11 | Keep today's tasklist-review entry points' semantics unless deliberately changed: sc:workflow Wave 4 reflect `--mode pre` is advisory and never edits the plan; sc-tasklist Stage 10.5 runs per phase, in parallel, non-blocking | Must | sc-workflow-protocol SKILL.md:60, :76; code-panel.md:193 |
| U12 | A documented verdict rule, told to reviewers, with a decision on quorum vs any-single-blocking; if a calibrator or validator is added, measure its effect on wrong blockers against this study's baseline | Should | D8, B-7; wrong blockers 1.8-4.75 per row |
| U13 | Clustering does not chain unrelated findings into one row (bounded chain length or direct-match only), and the merged row keeps every member's claim | Should | D4: 83 mega-cluster rows |
| U14 | A missing anchor is reported and handled (warning, fuzzy relocation or citation fallback) instead of producing an unfixable open row | Should | D6: 46 rows, 13 blocking |
| U15 | `merge` (or its successor) returns a verdict-bearing exit code | Should | D12 |
| U16 | Telemetry (or an equivalent record) is written by the product: requested and observed model, block_ok, dropped-finding count, tokens, wall time per reviewer | Should | T1; the study had to build this itself |
| U17 | A per-reviewer model override at resolve time (the study rewrote resolutions with `jq`) so evaluations can pin raw models without editing templates | Should | SPEC:26 |
| U18 | Regression benchmark: the three EVAL packages with their GT, judge prompt and anonymisation become a fixture; a unified panel should match or beat ember + 2x luna (1.83/14 found, 0.17/8 real blocking, 1.83 wrong blockers, 0.83/2 control, ~64k tokens) before replacing it | Should | CR:366, CR:428 |

## 7. Questions for the other session, and merge risks

### 7.1 Questions the other session should answer

| # | Question | Why it matters here |
|---|---|---|
| Q1 | Does master's `findings_v2.py` (citations, `reflect_category`, `deviation_class`, `self_confidence`, `lens`, `channel` fields seen by grep) replace findings-v1 for spec-panel, or run beside it? Does it still drop a whole finding on a length violation? | D1 is the largest measured loss in this study |
| Q2 | Does master's `cluster.py` replace `findings.cluster`, and does it chain (D4) or split on refs (D5)? | 83 mega-cluster rows here |
| Q3 | Do `hard_exclude` and `strict_distinct` (master panel.py) remove silent duplicates (P1) and keep owner-excluded models out (P4)? | Panel resolution currently picks Qwen twice |
| Q4 | How does reflect dispatch non-Claude models when `reflect-reviewer` is a Claude agent pinned to one model (code-panel.md:163, UNVERIFIED there)? Can the same path dispatch luna and ember for this panel? | U7; DM14 panels are mostly non-Claude |
| Q5 | Which finding unit wins: exact-quote anchors (this panel) or file:line citations (reflect)? For plan review, the quote is the useful grounding; for code audits, file:line is | Contract choice drives U2, U9, U14 |
| Q6 | Does reflect's calibrator plus evidence validator reduce wrong blockers on these three packages? Run reflect UC-1 on them with the same blind judge | Gives the first like-for-like comparison of the two designs |
| Q7 | Will tasklist review stay on reflect UC-1 (sc:workflow Wave 4, sc-tasklist Stage 10.5) or move to the unified panel? If it moves, is it still advisory? | DO4, U11 |
| Q8 | Is the review loop (cap 3, revise, `resolved_check`) kept for spec-panel while reflect stays loop-free? | U10 |
| Q9 | Which model registry wins: the tier JSON, `ANTHROPIC_DEFAULT_*_MODEL` aliases, or T2Model0N/T1Model0N slots (code-panel.md:184 counts three)? | P3, P5, U8 |
| Q10 | Is muse-ember now in the gateway tier lists (owner said it was being added, SPEC:120), and should the tier JSON follow ccsession's tier data (#518)? | P3 |
| Q11 | Does the confidence-calibrator agent's 6-dimension troubleshoot rubric match reflect's 5-dimension mean (code-panel.md:161, not re-read here)? | Matters only if a calibrator is adopted (DO3) |

### 7.2 Risks of merging

| # | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| K1 | The branch is 11 commits behind master and master already rewrote parts of `src/superclaude/cli/review/` (40 files, +8,026). Code citations in this report describe the branch base, not master | High / medium: line numbers and some defects may be stale | Re-check D1-D13 and P1-P7 against origin/master before planning; this branch has no src changes, so nothing conflicts in git |
| K2 | Adopting reflect's findings_v2 limits as-is carries D1 into the unified panel | Medium / high: luna, ember and wonder lose findings, and those are the default panel's models | U1, U2 |
| K3 | The panel recommendations rest on 3 plan packages, n=4-6 runs per panel, and a hard ceiling of ~2-2.5/14; they may not transfer to specs or code | High / medium | Treat DM14 as plan-review guidance only; re-benchmark per target (U18) |
| K4 | The study scored round 1 only; ledger revise, re-review and clearing paths (D3, D9, D10, D11) were never exercised with real panels | High / unknown | Add multi-round tests before trusting the loop with a multi-reviewer panel |
| K5 | Dispatch: the product panel cannot today launch the models the decision recommends (empty gateway launch map, no ember in tier data) | Certain / high | U7, U8 |
| K6 | Gateway behaviour (misrouting under load, weekly quotas, binary replacements) can silently change which model reviews | Medium / high | U6; concurrency caps; NOFALLBACK-style failure instead of silent fallback |
| K7 | Committing raw evidence: 1.5 GB of untracked transcripts sit only on this machine; if the workspace is lost, identity and token audits cannot be re-run | Medium / medium | DO8 |
| K8 | Analysis scripts depend on `/tmp` copies; the numbers cannot be regenerated from the commit alone | Certain / low-medium | H10; copy the `/tmp` inputs or rewrite the scripts |
| K9 | The earlier hand-off file in 4a22d7421 and this report were written independently and may disagree | Medium / low | Prefer claims that cite file:line; check both against the source |
| K10 | Blocking semantics differ across files (spec-panel "CRITICAL is blocking", prompt grading check, code rule) and the unified panel may pick one silently | Medium / medium | B-3; decide once and test it |
| K11 | Telemetry schema hard-codes `sonnet`/`haiku` strata; a unified panel with gateway models cannot report per-model scores through it | High / low | T2, U16 |

## 8. Test and verification status

### 8.1 Tests that exist on this branch and their result

Re-run by this author on 2026-11-14: `uv run pytest tests/review tests/skills/test_review_brief_placement.py tests/skills/test_review_loop_extension.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_mapping.py tests/skills/test_review_severity_rule.py tests/skills/test_spec_panel_review_loop.py -q -p no:cacheprovider` gave **304 passed in 4.86 s**, 0 failed, 0 skipped; no tracked file changed. Per-file breakdown from tests-tools.md:14-29:

| File | Collected | Covers |
|---|---|---|
| tests/review/test_review_cli.py | 9 | CLI surface, panel resolve, env, merge to revise to verdict round trip, exit codes 0/10/11, merge refuses a round with no valid block |
| tests/review/test_review_findings.py | 23 | findings-v1 and fixmap-v1 parsing, out-of-range field values, anchors across wraps, fingerprints, clusters, 3-line rule |
| tests/review/test_review_ledger.py | 24 | Statuses and events, revise, sha guard, rounds 1-3 with ESCALATE, defer, capture, refusal paths, "one valid block enough" |
| tests/review/test_review_panel.py | 41 | Panel and tier schema errors, stand-ins, fallbacks, strategies, determinism, env and lookup precedence |
| tests/review/test_review_panel_live7.py | 14 | @live7 resolution in both environments, re-review = anchor only, placeholder tier fails closed |
| tests/review/test_review_rules_text.py | 5 | Prompt file structure and pinned text |
| tests/review/test_review_telemetry.py | 10 | Record schema, append-only store, no document text, loader, model score arithmetic, strata |
| tests/skills/test_review_brief_placement.py | 5 | Prompt text lives only in the rules file; spec-panel gate |
| tests/skills/test_review_loop_extension.py | 18 | spec-panel Review Loop prose pins |
| tests/skills/test_review_prompt_overrides.py | 33 | Brief lint (no quotas, no "apply all findings") |
| tests/skills/test_review_severity_mapping.py | 14 | Consequence-based severity text |
| tests/skills/test_review_severity_rule.py | 62 | Severity rule copied to 10 files; 2-fix-cycle cap |
| tests/skills/test_spec_panel_review_loop.py | 46 | `## Review Loop` section structure |

The evaluation itself has no automated tests; its verification is the six audits (section 2, column "Checked by").

### 8.2 Not covered (gaps checked against the source)

| Gap | Linked defect | Source |
|---|---|---|
| Exact length boundaries (anchor 12 and 200, claim 300, refs 8) and anchor2 limits | D1 | tests-tools.md:33 |
| A test that the prompt's stated limits and categories equal the parser constants | B-2, U5 | tests-tools.md:34 |
| Four of six accepted categories never parsed in a test; case variants untested | n/a | tests-tools.md:35 |
| Malformed resolution, report id absent from the resolution, resolved reviewer with no report, `--report` without `=` | D13 | tests-tools.md:36 |
| All seven @live7 gateway models distinct (only pairwise checks) | P1 | tests-tools.md:37 |
| Duplicate reviewer id in one round | n/a | tests-tools.md:38 |
| Round 4+ after ESCALATE; non-default `--cap` | code-merge.md D12, D13 | tests-tools.md:39 |
| Merged-report text for a broken reviewer; a valid-JSON but over-limit line dropped while the reviewer's block still counts for clearing; warning content (only `assert res["warnings"]`) | D2, D3 | tests-tools.md:40 |
| Partial-panel failure flipping a verdict (the audit-D verdict flips have no regression test) | D1, D2 | audit-D:20 |
| Mega-cluster chaining; ref-mismatch splitting; missing-anchor rows | D4, D5, D6 | code-merge.md D3-D5 |
| Task-id refs (`T01.02`) | D7 | code-panel.md:168 |
| `ledger revise` applied twice; next round's doc not equal to revise `--new` | D11 | code-merge.md D7-D8 |
| Any end-to-end multi-reviewer, multi-round run with real reports | K4 | audit-D:3 (round 1 only) |
| `run-reviewer.sh` (identity check, fallback ladder, overwrite bug) | H2-H4 | no tests exist |

### 8.3 Tests added on newer master (listed only, not run here)

From `git diff --stat ec259f1b7 origin/master -- tests/review`: test_reflect_cluster_pairs.py, test_reflect_consumer_inventory.py, test_reflect_stage0a_replay.py, test_review_card_convert.py, test_review_cluster.py, test_review_cluster_cmd.py, test_review_findings_v2.py, test_review_manifest.py, test_review_panel_exclusion.py, test_review_panel_reflect_profile.py, test_review_reflect_templates.py, test_review_verify_citations.py, plus additions to test_review_cli.py and test_review_panel_live7.py and fixtures (golden panels, frozen tiers 1.0.0, reflect cards). Whether they cover any gap in 8.2 is UNVERIFIED.

### 8.4 What this author did not verify

- Reflect sources (sc-reflect-protocol SKILL.md beyond lines 592 and the grep hits, reflect-reviewer.md, confidence-calibrator.md, ensemble.py): taken from code-panel.md only.
- `ledger.py:301-401` (revise, defer, verdict, capture) and `telemetry.py`: taken from the notes.
- Audit B, C, E and F conclusions: no committed `summary.md`; taken from CR:290-298 and CR:373.
- Whether `/tmp` inputs used by the analysis scripts still exist.
- Anything on origin/master beyond file lists and the greps quoted above.

## Reading order for the other session

1. This report: the method note, then sections 2.2, 2.4 (D1-D8) and 6.
2. `EVAL/COMBO-REPORT.md` lines 289-428 (final results, decision, batch 11), then 430-506 (all-sets issue table). Skim the CORRECTION headings at CR:104, CR:146, CR:169, CR:195 to see what was retracted.
3. `EVAL/analysis/audits/audit-D/summary.md` (merge integrity, the 200-character drop) and `audit-A/summary.md` (identity).
4. `src/superclaude/rules/prompts/document_review_loop_prompts.md` (74 lines) and `src/superclaude/commands/spec-panel.md:256-268`.
5. `src/superclaude/cli/review/findings.py:90-121` and `:346-407`, then `ledger.py:107-298`, at this branch and again at origin/master (#519) to see what changed.
6. `EVAL/tools/run-reviewer.sh` (brief at lines 13-17, identity check at 50-59) and `EVAL/tools/tmp-scripts/judge-one.sh` (judge prompt).
7. `EVAL/combos/SPEC.md` for the operational history (outages, exclusions, owner orders) only if planning a new evaluation.
8. `EVAL/PILOT-REPORT.md` last; its luna figures are superseded.
