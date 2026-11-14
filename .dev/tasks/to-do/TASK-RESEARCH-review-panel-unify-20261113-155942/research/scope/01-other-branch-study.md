# Research: Other session's tasklist review-panel study (branch origin/ironbelly/eval-tasklist-review-panel)

**Scope:** `.dev/eval-workspaces/tasklist-review-panel/` at commit `4a22d74213f93837d00c2c314075dd967b9a98e3` (read via `git show`, not checked out); hand-off copy at `research/scope/00-handoff-copy.md`
**Status:** Complete
**Date:** 2026-11-13
**Citation form:** `<path>:<line>` means that path at commit 4a22d742, relative to `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` (the hand-off's `EVAL`) unless written in full. `CR` = `COMBO-REPORT.md`, `PR` = `PILOT-REPORT.md`, `SPEC` = `combos/SPEC.md`, `HANDOFF` = `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification.md` at 4a22d742.

Commit 4a22d742 = "docs(eval): add review-panel unification hand-off report and /tmp helper scripts", 2026-11-13 15:55 UTC; earlier study commits on that path: `2d06a4382` (batch 11, issue tables), `b4db265a8` (study). The local copy `research/scope/00-handoff-copy.md` is byte-identical to `HANDOFF` at this commit (`diff` empty), so HANDOFF line numbers below equal the copy's line numbers.

---

## 1. File inventory

Line counts are `git show <commit>:<path> | wc -l`. G = generic to any review target; T = tasklist-study specific; T(G) = specific code, generic pattern.

### 1.1 Reports and setup

| Path | Purpose | Lines | G/T |
|---|---|---|---|
| `../HANDOFF-review-panel-unification.md` | hand-off report for unification (copied here as `00-handoff-copy.md`) | 315 | G (planning doc) |
| `manifest.md` (inside EVAL, not at the study root) | eval setup: base SHA ec259f1b, sandbox `/tmp/evalsb/repo` (git archive minus `.dev/tasks/done`, `.dev/eval-workspaces`, `.dev/research`), dispatch via `claude -p --model <raw id>`, GT sha256 hashes | 16 | T |
| `PILOT-REPORT.md` | arms A/B/C on 3 packages, fixed decision rule, honest read | 83 | T |
| `COMBO-REPORT.md` | master report; only lines 289+ are current (see section 2) | 506 | T |
| `combos/SPEC.md` | combo-run procedure, limits, ops log batches 2-11 | 152 | T |
| `analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md` | 1.48 GB / 2,916 raw `*.attempt<N>.json` and `judge.json` files left out; points to CR "FINAL RESULTS AND DECISION" | 4 | T |

### 1.2 Per-package inputs (3 packages, same file set each)

| Path | Purpose | Lines | G/T |
|---|---|---|---|
| `TASK-WF-designSpec-20261107-075614/{candidate.md, ground-truth.json, ground-truth-draft.json, resolution-default.json, resolution-live7.json}` | defect-rich plan, 10 GT items | candidate 200, GT 207 | T (format G) |
| `TASK-WF-makeTheAliasOnly-20261105-051649/{same}` | defect-rich plan, 4 GT items | GT 104 | T |
| `TASK-WF-design-20261108-041415/{same}` | control plan, 2 GT items | GT 48 | T |
| `<pkg>/reviews*/`, `reviews-failed-launch-1/`, `quarantine*/` | per-run reviewer output (`<id>.md`, `.meta.json`, `.cost.json`, `.attemptN.md/.err`) | not read (raw run data) | T |

Note: `source.md` (the plan's driving document) is NOT in the eval tree; `tools/run-reviewer.sh:10` copies it from `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md` (the other worktree's done-task folder) at run time.

### 1.3 Merge and scoring outputs (data; not read)

| Path | Purpose |
|---|---|
| `arms/{A,B,C}/<pkg>/{ledger.json, merge-stdout.txt, merged-1.md, resolution.json}` | pilot merges by `superclaude review merge` |
| `combos/<row>/<pkg>/{same four files}` | per combo row merges |
| `arms/scoring/**/{merged-anon.md, score.json, label-key.json}` | blind judge inputs/outputs |

### 1.4 Harness scripts

| Path | Purpose | Lines | G/T |
|---|---|---|---|
| `tools/run-reviewer.sh` | runs ONE reviewer: sandbox copy of candidate (+ `source.md` if present), brief, `claude -p` with Edit/Write/NotebookEdit disallowed, 2 attempts, identity + findings-block check, fallback ladder with exclude list and no-revisit, writes `<id>.md/.meta.json/.cost.json` | 87 | T(G) |
| `tools/run-reviewer.sh.bad-launch`, `.unpassable-ac` | older copies (pre-fix) | 34 each | T |
| `tools/tmp-scripts/` | 54 scripts + `README.md` (55 entries by `git ls-tree`): `judge-one.sh` (blind judge), `anon-*.sh` (anonymisation per batch), `arm-merges.sh`, `merge-b6.sh`, `merge-src-rows.sh`, `gen-judge-list.sh`, `run-combo-judges.sh`, `b4-job-one.sh` (cancel-file runner), `startcombo*.sh`, per-row runners `n2*/n3/n4/n5*/r2*/r3/r5`, `snap.py`, `drift-b3.py`, `brief_c1.py`, `stats.sh` | README 7, judge-one 31, b4-job-one 8, anon-combos 28, merge-b6 44 | T(G) |
| `analysis/merge-b7..b11.sh`, `b7..b11-launch.sh`, `b11-rerun-one.sh`, `b*-judge.tsv`, `b*-fix.txt` | batch merges, launchers, judge lists | merge-b11 42 | T |

### 1.5 Analysis scripts and outputs (names and docstrings only; not read in full)

| Script | Docstring purpose (first line) | Lines | G/T |
|---|---|---|---|
| `analysis/final-table.py` | FINAL table: valid-era rows grouped by reviewer-model multiset, two views (AS SCORED, AUDIT-CLEAN) | 83 | T(G) |
| `analysis/three-way.py` | per-run detail + permutation tests for sonnet+2luna, ember+2luna, sonnet+luna+ember | 63 | T(G) |
| `analysis/doubles.py` | panels with 2 reviewers of the same model: run A, run B, union, overlap | 18 | T |
| `analysis/untried.py` | model-presence effects on catch/blocking/wrong blockers; untried model sets | 46 | T |
| `analysis/attrib.py` | per-model GT attribution from judge notes + ledgers (method RETRACTED per CR:195 as cited by HANDOFF:133) | 78 | T |
| `analysis/b8-table.py`, `b9-table.py` | replicate family tables | 88, 36 | T |
| `analysis/allsets/allsets-setup.py`, `allsets-table.py` (+ `allsets-chunks/`, `allsets-out/` agent outputs, `allsets-table.md` 66 lines) | inventory every scored run grouped by (era, model multiset); direct per-set issue counts cross-checking agents | table.py 47 | T(G) |
| `analysis/issue-table/issue-setup.py`, `issue-table.py`, `issue-compare.py` (+ `issue-01..10.{json,tsv}`, `issue-table-final.md` 12 lines) | issue legend (I#/B#), top-10 panel map, direct score.json cross-check of 10 agents | issue-table.py 29 | T(G) |
| `analysis/final-table.md` (59), `b8-final.md`, `b9-final.md`, `combo-est-{A,B,self}.md` | rendered tables and estimates | | T |
| `analysis/audits/audit-{A..F}/` | six audits: scripts (`audit.py`, `check*.py`, `recompute.py`, `anch.py`, `bok.py` ...), `flags.tsv`, stats json | see section 2 | T(G) |

**Audit summary files:** only `audit-A/summary.md` (34 lines) and `audit-D/summary.md` (90 lines) exist at this commit. B, C, E, F hold scripts, `flags.tsv` and json/txt outputs but no `summary.md`.

---

## 2. Verified key facts (checked against files at 4a22d742)

Tags: [CONFIRMED] = the cited file says it; [CONTRADICTED] = the file says otherwise; [PARTLY CONTRADICTED] = right in part; [UNVERIFIED] = not read in this slice. Product-code citations in HANDOFF (`src/superclaude/cli/review/*`) were NOT re-read here; they belong to another slice and stay [UNVERIFIED] in this file.

### 2.1 Hand-off claims checked

| # | HANDOFF claim (line) | Tag | Evidence |
|---|---|---|---|
| H1 | CR current sections start at 289 (final), 375 (decision update), 385 (issue table), 421 (batch 11), 430 (all sets) (HANDOFF:37) | [CONFIRMED] | headings at CR:289, CR:375, CR:385, CR:421, CR:430; CR:289 says it "supersedes every earlier table" |
| H2 | 106 scored runs, 62 sets, 3 pilot arms included (HANDOFF:12, :71) | [CONFIRMED] | CR:431; ALL row CR:497 (106 runs), ALL-src CR:498 (76 runs) |
| H3 | Valid era: 71 rows, 213 row-packages (HANDOFF:71) | [CONFIRMED] | CR:290, CR:301 (69 row-packages carry an EXCLUDE flag) |
| H4 | "Four of 16 issues never found by any run (designSpec GT1, GT2, GT10; alias GT4) and alias GT3 found once" (HANDOFF:78) | [PARTLY CONTRADICTED] | The four never-found are right (CR:501; ALL row CR:497: B1=0, B2=0, I5=0, I6=0). But CR:501 says the issue found exactly once over all 106 runs is **B6 = alias GT1** (luna + terra + wonder, set S28, CR:462), not alias GT3. Alias GT3 (B8) was found in 2 runs overall (CR:503: ember + sonnet; grok + haiku + wonder pre-src), 1 in the valid era (CR:498 B8=1). HANDOFF copies the older CR:287 sentence, which omits alias GT1. |
| H5 | Default ember + 2x luna: 64k tokens, ~6 min, 1.83/14, real blocking 0.17, control 0.83 (HANDOFF:79) | [CONFIRMED] | CR:366 (63,644 tokens, 348 s elapsed per CR:331) |
| H6 | Optional quality tier sonnet + 2x luna n=6: 2.33/14, 139k, ~14 min, control 1.33; I7 3/6 vs 0/6, Fisher p ~0.012 (HANDOFF:79) | [CONFIRMED] | CR:424 (821 s elapsed), CR:426, CR:428 |
| H7 | Best real blocking haiku + 2x luna 1.2/8, 191k, 3.0 wrong blockers (HANDOFF:79) | [CONFIRMED] | CR:319, CR:367 |
| H8 | Decision update "sonnet + 2x luna is standard" rejected by batch 11 (HANDOFF:79, :189) | [CONFIRMED] | CR:383 (update), CR:421 and CR:428 ("NOT CONFIRMED") |
| H9 | Only three statistics survive audit: second luna +0.83 control; 2x luna + 2x ember +2.75-3.25 wrong blockers; ember + terra -1.75 found (HANDOFF:80) | [CONFIRMED] | CR:298 |
| H10 | No replicated panel significantly different except cost/time, "permutation p 0.28-1.0" (HANDOFF:77) | [CONFIRMED] with nuance | CR:381 gives p 0.54-1.0 for the three-way; CR:425 gives p=0.28 for control (sonnet + 2x luna vs ember + 2x luna); tokens p 0.002-0.009 (CR:381) |
| H11 | Pilot arms found 2/16, 3/16, 4/16, 0/8 real blocking; sonnet alone PASSED both defect-rich plans (HANDOFF:81) | [CONFIRMED] | PR:48-50, PR:22, PR:30, PR:71 |
| H12 | Pilot decision rule pre-registered (HANDOFF:174 "PR:56-61") | [CONFIRMED] | PR:56 (rule), PR:58-61 (application) |
| H13 | Qwen3.8-max timed out 3000 s on 3 of 3 slots, 9000 s wasted (HANDOFF:95) | [CONFIRMED] | PR:12 |
| H14 | Merge drops: anchor >200 (56), anchor2 >200 (18), claim >300 (14); 80 reviewer-level cases; 49 blocking findings lost; by model luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet/terra/sol 0 (HANDOFF:105) | [CONFIRMED] | audit-D/summary.md:7-8, :16-19; CR:292. Precision note: the per-model numbers are **all dropped findings** by model (sum 92), not blocking ones; audit-D/summary.md:17 labels them "dropped-finding reasons"; CR:292 places them right after "49 blocking findings lost", which reads as if they were blocking. HANDOFF's "(... findings in total ...)" is the correct reading. Audit D also lists bad severity 3 and refs-bad 1 (summary.md:16). |
| H15 | 4 verdicts flipped FAIL to PASS (HANDOFF:105) | [PARTLY CONTRADICTED] | audit-D/summary.md:20 names **3** verdict flips (g3-...-r3 alias, g5-...-r2 alias, n5-sonnet-ember design) plus 5 "total-loss merges" listed separately; CR:292 says "Four verdicts flipped ... plus total-loss merges" but names three. The count 4 is not supported by the audit text. |
| H16 | 83 merged rows lump unrelated findings (chaining) (HANDOFF:110) | [CONFIRMED] | audit-D/summary.md:29 (195 of 1398 rows with 3+ members are chains; 83 rows have 8+ members or 4+ sections; example r2-sonnet-ember designSpec L1: 19 members over 8 sections) |
| H17 | 156 of 665 valid-era runs never referenced `source.md` (HANDOFF:112) | [CONFIRMED] | CR:373 (corrects CR:293's 161). Per model: ember 81/209, luna 49/222, wonder 6/25, haiku 15/75, grok 4/24, sonnet 1/63, terra 0/44, sol 0/3 |
| H18 | "The reviewer brief never names the source document" (D8, HANDOFF:112) | [CONFIRMED] for the eval brief, nuance added | `tools/run-reviewer.sh:13-17`: brief names only `$CAND_SB`; `source.md` is copied next to it (`:10-11`) but never mentioned. However every candidate itself names it (`candidate.md:3` `source: ./source.md` and `:14` `Source: ./source.md` in all 3 packages; designSpec mentions `source.md` 13 times). So reviewers had a pointer inside the document; the brief just did not tell them to open it. SPEC:91 records the earlier root cause (sandbox shipped only `candidate.md` while candidates reference `./source.md`). CR:373 keeps the causal link as an inference. |
| H19 | Source first shipped 2026-11-12 12:59:34; first valid-era run 13:02:27 (HANDOFF:70) | [CONFIRMED] | CR:373 |
| H20 | Audit E: 294 judge outputs clean; blind re-judge 12/12 exact agreement, 19/19 catches confirmed, GT8 borderline (HANDOFF:139) | [CONFIRMED] (via CR only) | CR:296. No `audit-E/summary.md` exists; the claim is only in CR. |
| H21 | "Six ... audits, outputs in `EVAL/analysis/audits/audit-A..F` (summaries in `summary.md`)" (HANDOFF:139) | [CONTRADICTED] | Only `audit-A/summary.md` and `audit-D/summary.md` exist (`git ls-tree` at 4a22d742). B, C, E, F findings are only in CR:290-298, CR:373 and their scripts/`flags.tsv`. Also audit-A/summary.md:2 and audit-D/summary.md:2 still point to `/tmp/audit-A/...` and `/tmp/audit-D/...` paths, not the committed location. |
| H22 | Audit A: 2 b4-muse-luna2 "wonder" runs served terra; grok id `grok-4.7-build` benign (HANDOFF:139) | [CONFIRMED] | audit-A/summary.md:6-8, CR:295, audit-D/summary.md:11 |
| H23 | Reviewer run: fresh `claude -p` session, Edit/Write disallowed (HANDOFF:68, :214) | [CONFIRMED] | `tools/run-reviewer.sh:48` (`timeout 3000 claude -p --model "$MODEL" --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit`). Note: Bash is NOT disallowed and permission mode is bypass, so a reviewer could write via Bash; audit C reports no candidate was written (CR:373). |
| H24 | Brief is at `tools/run-reviewer.sh:13-17`, a copy of the repo brief (HANDOFF:68) | [CONFIRMED] lines; "copy" [UNVERIFIED] | brief text at :13-17 says "First-review rules (from ~/.claude/rules/prompts/document_review_loop_prompts.md, read it first)" and invokes `/sc:spec-panel @<cand> --mode critique`; the repo prompts file itself was not read in this slice |
| H25 | Judge: one blind Opus per (row, package), writes `gt_covered_any`, `gt_covered_blocking`, `wrong_blockers` (HANDOFF:68) | [CONFIRMED] | `tools/tmp-scripts/judge-one.sh:12-23` (brief, score.json schema at :21), :25 (`claude -p --model claude-opus-5-5`, 900 s timeout). Judge reads GT, candidate and `merged-anon.md` only; it is NOT given `source.md`. |
| H26 | Fallback ladder fix: never revisit, `EXCLUDE_MODELS`, `NOFALLBACK=1` (HANDOFF:129, `tools/run-reviewer.sh:66-80`) | [CONFIRMED] | `tools/run-reviewer.sh:66-83`; incident SPEC:141 |
| H27 | 12 concurrent workers caused identity bleed; re-run serially after 60-min cooldown (HANDOFF:130) | [CONFIRMED] | SPEC:77-85 |
| H28 | `tools/tmp-scripts/` holds 54 scripts plus README (HANDOFF:52) | [CONFIRMED] | 55 entries by `git ls-tree` |
| H29 | `checks-gate8.sh` was NOT copied (HANDOFF:55) | [CONFIRMED], but README disagrees | absent from `tools/tmp-scripts/`; yet `tools/tmp-scripts/README.md:7` lists "checks-gate8" among the "key ones" |
| H30 | Raw transcripts left out: 1.48 GB (HANDOFF:59) | [CONFIRMED] with count nuance | `analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md:2` says 2,916 files; HANDOFF:59 counts 3,041 untracked files (1,380 + 1,352 + 309). Different scopes (HANDOFF includes `attemptN.meta.json`), not necessarily a conflict. |
| H31 | Aliases serve only the first model of a tier, so raw ids were used (HANDOFF:185) | [CONFIRMED] | `manifest.md:11` |
| H32 | Sandbox excludes `.dev/tasks/done`, eval workspaces, `.dev/research` (HANDOFF:273) | [CONFIRMED] | `manifest.md:10` |
| H33 | Pre-source luna data quarantined (HANDOFF:70, :89) | [CONFIRMED] | SPEC:102-103 (luna refused without source.md, 25/25 empty; 428 files moved to `quarantine-pre-src-luna/`) |
| H34 | Terra/sol return incomplete/empty reviews even with source.md; 16 empty terra reviews (HANDOFF:93) | [CONFIRMED] | CR:294 |
| H35 | Luna anchor fidelity 91.4% verbatim (HANDOFF:89) | [CONFIRMED] | CR:294 |
| H36 | Judge blocking 65 vs real blocking 38 over 71 rows (HANDOFF:108, :268) | [CONFIRMED] | CR:291 |
| H37 | `manifest.md` "Worktree branch ... (local, never pushed)" | [STALE] | `manifest.md:5` says never pushed; the branch is now on origin (this commit is reachable as a remote ref). Minor. |
| H38 | Product-code defects D1-D16 with `RV/<file>:<line>` citations (HANDOFF:99-120) | [UNVERIFIED] in this slice | product files were not re-read here; audit-D/summary.md:15 and :29 independently replay `findings.py` `_check_finding` and `cluster()` (union-find over same section+refs or spans within 3 lines), which agrees with D1 and D6 in substance |

### 2.2 Additional facts found in this slice (not in HANDOFF or stated differently)

- **Identity check accepts a `-build` suffix and rejects `<synthetic>`**: `tools/run-reviewer.sh:55-56`. Observed model is the unique set of top-level assistant `message.model` values (`:51`, subagent turns excluded by `parent_tool_use_id==null`).
- **Fallback overwrites `expected_model` in `meta.json`**: `tools/run-reviewer.sh:58` writes `expected_model:$MODEL` after `MODEL="$NEXT"` (`:76`), so a fallback run passes `model_ok` against the fallback model; only `<id>.fallback.log` (`:75`) records the swap. SPEC:141 and audit-A/summary.md:12 and :34 describe this as the flaw that hid wrong-model runs; the audit added an "intended vs expected" check (audit-A/summary.md:11) rather than the runner fixing the field.
- **Auxiliary model calls inside a reviewer run**: 57 runs show a client-side call to alias `claude-gw-tier2[1m]` (~512 output tokens, `web_fetch_apply`) counted in `output_tokens_all` (audit-A/summary.md:22). A generic identity check must separate reviewer turns from auxiliary turns.
- **Stale attempt files** make "highest attemptN" wrong for 5 runs; the audit used `meta.attempt` (audit-A/summary.md:15).
- **Anchor resolution failures are kept**: 46 rows have null span (anchor not found after flattening), 13 of them blocking (audit-D/summary.md:30), consistent with HANDOFF D5.
- **Blocking/verdict logic is internally consistent**: row blocking == any member blocking, verdict FAIL iff a blocking row, 0 violations over 264 merges (audit-D/summary.md:33).
- **Merge outputs missing**: 45 merges have no `merge-stdout.txt`, so their merge warnings are UNVERIFIED (audit-D/summary.md:26).
- **Ground-truth format** (all 3 packages): top keys `package, items, dropped, verification`; item keys `id, class, plan_quote, description, evidence[], cost, blocking_in_implement`; classes seen `ambiguity, contradiction, missing-task, unpassable-ac`; cost values `both, extra_attempt, human_acceptance, neither`; `verification[]` holds `quote_grep_count` and `evidence_ok` per item (`TASK-WF-design-20261108-041415/ground-truth.json:1-48`; designSpec keys via `jq`). Evidence points into `.dev/tasks/done/<pkg>/...` implement artifacts (e.g. control GT1 evidence at `ground-truth.json:9-16`).
- **Resolution files reuse product schema**: `<pkg>/resolution-live7.json` has `schema: review-panel-resolution/1` with `template_sha256`, `tiers_sha256`, and per reviewer `alias` (e.g. `claude-gw-tier1b[1m]`), `fallbacks`, `strategy`, `tier` (jq of design package). Combo rows build their `resolution.json` by filtering `resolution-live7.json` and overriding `.model` (SPEC:26), so reviewer ids like `t4-1` are labels only (SPEC:16).
- **Concurrency limits used**: at most 2 runs at once early (SPEC:22, :57), waves of 4 workers x 1 run after contamination (SPEC:79), later 10 concurrent with muse capped at 4 (SPEC:99), batch 11 five runners x `-P 2` (SPEC:151).
- **Stop rule**: "if any reviewer fails the observed-model check twice, STOP that worker ... do not silently drop a base reviewer" (SPEC:79).
- **Pilot judge cost**: 9 Opus judges = 1,034,575 output tokens (PR:52), more than the reviewer tokens of the largest arm (604,096 for arm C, PR:50; the arms are cut from the same reviewer runs, PR:8). A judge-based regression suite is not cheap.

---

## 3. Reusable methods and harness pieces, and what makes them generic

| Piece | Where | What it does | Tasklist/study-specific parts | To make generic |
|---|---|---|---|---|
| **Single-reviewer runner** | `tools/run-reviewer.sh:1-87` | fresh `claude -p` session per reviewer, sandbox cwd, tool deny list, 3000 s timeout, 2 attempts, `meta.json` (expected/observed model, `model_ok`, `findings_block`, wall, tokens, exit), `cost.json` summed over attempts | hard-coded `/tmp/evalsb` (`:7`, `:48`), source path into another worktree (`:10`), `/sc:spec-panel` brief text (`:13-17`), positional args, `reviews${5}` layout | parameterise candidate, driving document(s), brief template, sandbox root and output dir; take the brief from one shared prompt file with `{{CANDIDATE}}` and a `{{SOURCE}}` value; deny Bash writes too (today only Edit/Write/NotebookEdit are denied, `:48`); keep raw transcript optional. Reflect dispatches reviewers as in-session agents (`reflect-reviewer`, SKILL.md:340 step 3 "Dispatch is the legacy dispatch"), so a generic runner needs two adapters: `claude -p` subprocess and Agent-tool subagent. |
| **Model-identity check** | `tools/run-reviewer.sh:51`, `:55-56`; audit-A/summary.md:11-22 | observed = unique top-level assistant `message.model`; ok if equal to requested (case-insensitive) or `<requested>-build`; rejects empty and `<synthetic>` | the `-build` alias rule is gateway-specific | keep **intended model** separate from **served model** and from the ladder model (the runner overwrites `expected_model`, `:58` vs `:76`); exclude auxiliary turns (audit-A E2: `claude-gw-tier2[1m]` `web_fetch_apply` calls); a configurable alias map. Reflect shadow mode already has `identity_source: observed|requested-pinned` and `identity_mismatch_suspected` (SKILL.md:346), which is the same need with a weaker signal (self-report). |
| **Fallback ladder with guards** | `tools/run-reviewer.sh:19-43` (map), `:66-83` (guards) | on identity failure, API error or no findings block, try next model in tier, then next tier head; no revisit, exclude list, `NOFALLBACK=1` | model ids and tier order are time-bound gateway data; the map is a bash associative array | move to data (the product tier file already has ordered `fallbacks` per reviewer, seen in `resolution-live7.json`), record every hop, and **default to no fallback for evaluation runs** (the study's own lesson, HANDOFF:159). |
| **Findings-block gate** | `tools/run-reviewer.sh:57`; reflect SKILL.md:343 step 4 | runner retries if no ```` ```findings-v1 ```` fence; reflect does one bounded re-ask for the block only and records `findings_block_compliance_rate` | the runner only checks the fence exists, not that lines validate; the merge later drops invalid lines (audit-D/summary.md:15-19) | validate the block with the product parser at collection time and report per-line rejects (ids, reasons) back into the ledger; same gate for every consumer. |
| **Blind judge against ground truth** | `tools/tmp-scripts/judge-one.sh:1-31`; anonymisation `tools/tmp-scripts/anon-*.sh` (not read) | Opus judge reads GT + candidate + anonymised merged report, writes `score.json` (`gt_covered_any`, `gt_covered_blocking`, `ledger_rows_*`, `blocking_rows_gt_matched`, `wrong_blockers`, notes) | absolute EVAL path (`:4`), `arms/scoring/combos/<C>/<P>/<L>` layout (`:6`), merged-report wording ("Ledger rows / Blocking findings / Other findings", `:19`) | take GT, candidate, report as arguments; define "real blocking" in the judge output (the study had to post-correct it, CR:291) by giving the judge `blocking_in_implement`; add a second judge or periodic re-judge (audit E did 12 rows, CR:296); keep reports anonymised. Works for any target with a GT file. |
| **Ground-truth format** | `<pkg>/ground-truth.json` (e.g. `TASK-WF-design-20261108-041415/ground-truth.json:1-48`) | defects observed in real implement runs, each with `plan_quote`, `evidence[]` file:line into implement artifacts, `cost`, `blocking_in_implement`, plus `verification` (`quote_grep_count`, `evidence_ok`) | `class` values (`missing-task`, `unpassable-ac`) are tasklist words; evidence points to `.dev/tasks/done/` | the shape is target-neutral; a spec or PR-diff GT needs its own class list and an "observed failure" source (e.g. merged-PR bug reports). The `verification` block (quote really occurs in candidate) is a reusable integrity check. |
| **Six integrity audits** | `analysis/audits/audit-A..F/` (A and D have summaries) | A identity/attempts; B report validity (incomplete/refusals); C inputs/timing (which files reviewers opened, leakage); D merge/ledger integrity (dropped lines replayed with the product parser, stale reports by sha, chain clusters); E scoring integrity + blind re-judge; F aggregation/statistics | scripts read study layout and row names | A, C, D are directly product-relevant: A and D could become built-in checks of a panel run (identity, dropped-finding counter, report sha vs ledger sha, cluster chain size); C ("did the reviewer open the source?") needs transcript access, so it fits a telemetry field rather than an audit. |
| **Replicates + permutation tests** | `analysis/three-way.py` (63), `analysis/final-table.py` (83) | run-level permutation/Welch tests; AS-SCORED vs AUDIT-CLEAN views | panel names, package ids, GT labels | a generic "compare two panel configs on a GT set" script with n>=4 replicates per config; the study shows every n=1 winner regressed (CR:370, CR:424). |
| **Agents + direct-script cross-check** | `analysis/allsets/`, `analysis/issue-table/` | parallel agents count cells, a direct script recomputes, compare cell by cell (0 mismatches, CR:386, CR:431) | study tables | method only; worth keeping for any future rf-qa-style evaluation. |
| **Quarantine-not-delete, cancel files** | SPEC:78, SPEC:103, SPEC:135, SPEC:141; `tools/tmp-scripts/b4-job-one.sh` | rename suspect dirs with a dated suffix; `/tmp/cancel-<row>` stops queued jobs | `/tmp` paths | an eval-runner convention, not product code. |
| **Sandbox snapshot** | `manifest.md:10` | reviewers run in a git archive of HEAD without `.dev/tasks/done`, eval workspaces, `.dev/research` | paths | generic need: reviewers must not see ground truth or prior implement history. Reflect has a related isolation flag (`--isolate-reviewers` review snapshot is listed in the project CLAUDE.md as an allowed internal checkout); how they compare is [UNVERIFIED]. |

---

## 4. Overlaps and conflicts with a reflect-side panel

Reflect-side statements below come only from `src/superclaude/skills/sc-reflect-protocol/SKILL.md:338-349` (shadow-mode steps, read in this slice) and HANDOFF section 5.6 (whose SKILL.md citations HANDOFF itself marks UNVERIFIED). Everything else about reflect is for another slice.

| Topic | Tasklist study (other branch) | Reflect shadow panel (this branch) | Overlap / conflict |
|---|---|---|---|
| **Finding format** | findings-v1 block in each reviewer report, parsed by `superclaude review merge` (SPEC:28; brief `tools/run-reviewer.sh:17`) | reviewers add the "one findings-block instruction line" (SKILL.md:342) and cards carry a `## Findings block` parsed in step 4 (SKILL.md:343); reflect also has `coverage_rows` and a `coverage.json` (SKILL.md:345) | **Overlap:** both use the `## Findings block`. Whether reflect's block is exactly findings-v1 or an extension (it mentions `coverage_rows`) is [UNVERIFIED] here. **Conflict risk:** the study shows the findings-v1 length limits silently drop 88+ lines (audit-D/summary.md:16); reflect step 4 "never edits, remaps or normalizes" and leaves an invalid block invalid (SKILL.md:343), so reflect inherits the drop behaviour if it uses the same parser. |
| **Invalid-block handling** | runner retries the whole review once if no fence (`:57`, `:61-64`); merge drops bad lines, keeps the rest | one bounded re-ask for the block only; compliance rate recorded (SKILL.md:343) | Different policies for the same failure. A unified panel needs one rule: per-line reject list + one block-only re-ask (reflect's) is cheaper than a full rerun (study's). |
| **Blocking rule** | any reviewer's `blocking:true` makes the row blocking and the verdict FAIL (audit-D/summary.md:33); judge-blocking overstated real blocking 65 vs 38 (CR:291) | legacy debate + blind calibration + evidence validator stay authoritative; shadow steps "change no verdict" (SKILL.md:338) | **Conflict:** the study's gate is a single-reviewer veto; reflect's verdict comes from debate and calibration. The study's numbers argue against a single-reviewer veto (wrong blockers 1.8-4.75 per run on defect-rich plans, CR:304-337). |
| **Calibration** | none in the merge; only the offline Opus judge | blind calibration per card, results copied into `panel/cards/reviewer-<N>.md` `calibration: per_finding:` (SKILL.md:344) | reflect has the per-finding calibrator the tasklist panel lacks; the study's judge is an evaluation tool, not a calibrator. A unified panel could use the calibrator where the study used nothing. |
| **Model tiers / selection** | hand-picked raw ids per row; packaged `@default`/`@live7` never validated (HANDOFF:240); evidence favours luna, ember, haiku, sonnet and disfavours Qwen, glm, terra, sol (CR:363-371) | `superclaude review panel resolve --template @reflect-pre --env anthropic-only --hard-exclude-class <executor class> --strict-distinct` (SKILL.md:339) | **Overlap:** both go through the same `panel resolve` code and tier file. **Conflict:** reflect resolves in `anthropic-only` with strict distinct classes; the study's useful panels use two runs of the same model (2x luna) and non-Anthropic models. The study's only surviving doubling effect (second luna, CR:298) is incompatible with `--strict-distinct`. |
| **Identity** | observed model from transcript, hard check, fallback ladder (`tools/run-reviewer.sh:51-59`) | `identity_source: observed|requested-pinned`, self-report compared to pin, mismatch only flagged (SKILL.md:346); card `model:` copied from the pin, never from the harness (SKILL.md:340) | Same goal, different strength. The study needed the hard check (12-worker identity bleed, SPEC:78; ladder hiding swaps, SPEC:141). A subagent dispatch may not expose the served model; this is a real limit for reflect, not just a design choice ([UNVERIFIED] which adapter exposes what). |
| **Recording** | per-run `meta.json`/`cost.json`, per-row `ledger.json`/`merged-1.md`/`resolution.json`, `score.json`; no product telemetry used (HANDOFF:119) | `superclaude review manifest init/advance` stages, `panel/` artifacts, telemetry fields under `telemetry:` in the contract (SKILL.md:338, :349) | reflect already has a staged manifest the study lacked; the study has cost/time per reviewer that reflect's telemetry should include. `review manifest` and `review cluster` are used by reflect but are not in HANDOFF's list of `RV` files (HANDOFF:24-28); whether they exist on master or only on this branch is [UNVERIFIED]. |
| **Clustering** | `findings.py` cluster: union-find, chains up to 19 members over 8 sections (audit-D/summary.md:29) | `superclaude review cluster ... --kept` after the evidence validator (SKILL.md:347) | If `review cluster` uses the same `same_defect` rule, reflect inherits the chaining defect. [UNVERIFIED] which algorithm `review cluster` uses. |
| **Driving document** | `source.md` shipped next to candidate but not named in brief; 156/665 runs never opened it (CR:373) | reflect takes a spec/tasklist path (HANDOFF:255, UNVERIFIED) | the unified brief needs a named source input for every target; the study gives a ready metric ("opened the source?") to record it. |
| **Re-review / loop** | first reviews only (HANDOFF:144) | single-pass audit with debate | neither side has evidence on rounds 2-3; the #346 ledger loop is the only owner of that behaviour. |

---

## 5. Suggested deep-investigation assignments for Phase 2

| # | Topic | Files | Why |
|---|---|---|---|
| P2-1 | **Product parser and merge drop behaviour on master vs this branch** | `src/superclaude/cli/review/findings.py` (`_check_finding`, cluster), `ledger.py:107-298` on master and on `ironbelly/shadow-runs` | HANDOFF D1-D7 cite lines that this slice did not re-read; audit D replays the parser. Confirm the limits, the single warning, and whether the shadow-runs branch changed anything. |
| P2-2 | **Which `review` subcommands exist where** | `src/superclaude/cli/review/__init__.py` and command modules on master, on 4a22d742, and on this branch | reflect uses `review cluster`, `review manifest`, `--strict-distinct`, `--hard-exclude-class`, `@reflect-pre` (SKILL.md:339, :347); HANDOFF lists none of them and reports missing `lint_cmd`/`estimate_cmd` (D13). The unified panel must start from one command surface. |
| P2-3 | **Reflect findings block vs findings-v1** | `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md`, reflect SKILL.md steps 3-6, `findings.py` schema | decide whether one block format serves both, and whether reflect's `coverage_rows` and calibration fields can be added without breaking the merge. |
| P2-4 | **Generic reviewer runner and identity** | `tools/run-reviewer.sh` (study), reflect dispatch (SKILL.md step 3), any `superclaude` adapter that reads transcripts (S-ID spike, SKILL.md:346) | the study's hard identity check worked only because it ran `claude -p` with JSON output; reflect dispatches subagents. Determine what each dispatch path can observe. |
| P2-5 | **Brief unification and `{{SOURCE}}`** | `src/superclaude/rules/prompts/document_review_loop_prompts.md` (74 lines per HANDOFF:29), `tools/run-reviewer.sh:13-17`, reflect reviewer briefs | D8 is the study's biggest named lever (CR:371); the candidate files already point to `./source.md` (`candidate.md:3`), yet 23% of runs ignored it. |
| P2-6 | **Panel config evidence vs packaged tiers** | `src/superclaude/cli/review/data/review-tiers.default.json`, `review-panel.*.json`, reflect templates `@reflect-pre`, CR:363-371, CR:428 | the packaged tier lists favour models the study rejected (HANDOFF:240); reflect's `anthropic-only` + strict-distinct conflicts with the study's best panels. |
| P2-7 | **Blocking/verdict policy** | `ledger.py` verdict code, reflect calibration (§11.3) and evidence validator, stoprule `finding-grader` agent | choose between single-reviewer veto, quorum, calibrator or grader; the study's 65-vs-38 and wrong-blocker figures are the evidence base. |
| P2-8 | **Regression suite from the study** | 3 `ground-truth.json`, 3 `candidate.md`, `judge-one.sh`, `anon-combos.sh`, `analysis/final-table.py`, `three-way.py`; the `source.md` files in `.dev/tasks/done/<pkg>/` on the other worktree | decide what to move into the repo as a reusable benchmark; note `source.md` is not in the eval tree (`tools/run-reviewer.sh:10`) and the judge costs ~115k output tokens per scoring (PR:52 / 9). |
| P2-9 | **Audit A and D as built-in checks** | `analysis/audits/audit-A/audit.py`, `audit-D/audit.py`, `audit2.py`, `anch.py`, `bok.py` | turn the dropped-finding counter, report-sha-vs-ledger check, chain-size flag and identity re-derivation into product telemetry so the next eval does not need a 6-audit pass. |

---

## 6. Gaps and questions

1. **Audit B, C, E, F have no summaries** at 4a22d742; their results are known only through CR:290-298 and CR:373. Anyone citing "audit C" or "audit E" is citing COMBO-REPORT, not an audit file. [CONTRADICTED HANDOFF:139]
2. **HANDOFF R2 names the wrong once-found issue.** All-sets data (CR:497, CR:501) says alias GT1 (B6) was found once; alias GT3 (B8) was found twice overall. The unification report should cite CR:501, not CR:287.
3. **Verdict flips: 3 or 4?** audit-D/summary.md:20 names 3 flips; CR:292 and HANDOFF:105 say 4. [PARTLY CONTRADICTED]
4. **`source.md` is outside the eval tree.** It lives in the other worktree's `.dev/tasks/done/<pkg>/` (`tools/run-reviewer.sh:10`); the committed study cannot be re-run from the commit alone. Whether those `source.md` files are on master is [UNVERIFIED].
5. **Audit summaries and scripts reference `/tmp/audit-*` paths** (audit-A/summary.md:2, audit-D/summary.md:2) and the tmp-scripts README lists a script that was not copied (`checks-gate8`, README.md:7). Re-running audits needs path fixes.
6. **`expected_model` overwritten by the fallback** (`tools/run-reviewer.sh:58`, `:76`) is still in the current runner; only `fallback.log` and the external audit catch it. A generic runner must store the intended model separately.
7. **Reviewer write access:** Bash is allowed with `bypassPermissions` (`tools/run-reviewer.sh:48`). The study relied on an after-the-fact audit (CR:373: "no candidate was written").
8. **Judge has no `source.md`** (`judge-one.sh:13-16`), so "same defect" matching is against plan text and GT only; acceptable for the study, but a generic judge for spec or PR review needs the target's driving input defined.
9. **Product-code defects D1-D16 not re-read** in this slice ([UNVERIFIED] here); P2-1 and P2-2 cover them.
10. **Reflect-side facts** in section 4 rest on SKILL.md:338-349 only; reflect's block schema, calibrator rubric and cluster algorithm are [UNVERIFIED] in this slice.
11. **Question:** does `review cluster` (used by reflect) share `findings.py`'s union-find? If yes, the study's chaining finding (83 mega-rows) applies to reflect's shadow telemetry too.
12. **Question:** can a reflect panel keep `--strict-distinct` and still use the study's best-supported configuration (two runs of the same cheap model)? The two are in direct conflict.
13. **Question:** the study's "valid era" covers 2026-11-12 13:02 onward on one gateway; model behaviour (muse misroutes SPEC:82, :116; glm misroute SPEC:88) is time-bound. Any default model list taken from it should carry a date.

---

## Summary

- The hand-off is accurate on the main results and decisions: 106 runs, 62 sets, the ember + 2x luna default, the rejected sonnet "standard", the 3 surviving statistics, 49 blocking findings lost at merge, 156/665 source-blind runs, and the runner and judge details. Checked against CR, PR, SPEC, audit A/D, `run-reviewer.sh` and `judge-one.sh`.
- Corrections: (a) only audits A and D have `summary.md`; (b) the once-found issue is alias GT1 (B6), not alias GT3; (c) audit D names 3 verdict flips, not 4; (d) the per-model "dropped" numbers count all dropped findings, not blocking ones; (e) the candidates do name `./source.md`, even though the brief does not.
- Reusable for a central panel: the runner pattern (fresh session, identity check, findings-block gate, guarded fallback), the blind judge plus GT format as a regression benchmark, and audits A and D as built-in run checks. Generic work needed: parameterise paths and brief, keep intended vs served model apart, deny Bash writes, and add a subagent dispatch adapter.
- Main conflicts with the reflect shadow panel: single-reviewer veto vs debate/calibration; `--strict-distinct` + `anthropic-only` vs the study's 2x-same-model, mixed-vendor panels; hard observed identity vs self-report; full rerun vs block-only re-ask for invalid blocks; reflect may inherit the parser's drop and chaining defects.
