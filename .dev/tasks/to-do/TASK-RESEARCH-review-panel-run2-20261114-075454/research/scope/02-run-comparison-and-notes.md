# Scope slice 02: run1-vs-run2 comparison and per-run notes

**Status:** Complete
**Date:** 2026-11-14
**Scope:** `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-run1-vs-run2.md` and `.dev/eval-workspaces/tasklist-review-panel/handoff-notes/{run1,run2}/{code-merge,code-panel,tests-tools}.md`
**Read at:** `origin/ironbelly/eval-tasklist-review-panel` tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` (run-1 commit `4a22d74213f93837d00c2c314075dd967b9a98e3` is an ancestor). All paths below are relative to the repo root; the files exist only at that tip, not in this worktree (`ls .dev/eval-workspaces/tasklist-review-panel` fails here).
**Code checks:** made against HEAD of this worktree (branch `ironbelly/shadow-runs`, HEAD `50d4d2b9d`).

---

**Notation.** HO = `HANDOFF-run1-vs-run2.md`; R1CM / R1CP / R1TT = `handoff-notes/run1/{code-merge,code-panel,tests-tools}.md`; R2CM / R2CP / R2TT = same under `run2/`; `file:line` after a note abbreviation is a line of that note file at the tip. Code abbreviations: F = `src/superclaude/cli/review/findings.py`, L = `ledger.py`, LC = `ledger_cmd.py`, M = `merge_cmd.py`, P = `panel.py`, PC = `panel_cmd.py`, T = `telemetry.py`, RP = `src/superclaude/rules/prompts/document_review_loop_prompts.md`, SP = `src/superclaude/commands/spec-panel.md`.
**Status tags.** `[V]` = checked at HEAD `50d4d2b9d` and true; `[V-base]` = true in the code the runs read (`ec259f1b7`) and the content still holds at HEAD, but the line number moved; `[CODE-CONTRADICTED]` = code at HEAD or at the runs' base shows otherwise; `[UNVERIFIED]` = could not check here (other worktree, /tmp, remote state, or outside this slice's material).
**Programs.** E1 = reflect Tier 2 panel kernel (this branch); E2 = tasklist review-panel evaluation and redesign (`origin/ironbelly/eval-tasklist-review-panel`); E3 = #346 review loop on master plus `~/.claude` variants.
**Destination vocabulary (value inventory).** CORE = shared kernel; M-TL = tasklist-review module; M-RF = reflect module; M-SP = spec-review module; M-PR = later PR/code-review and rf-qa module; EVID = evidence archive, not code; HARNESS = benchmark/eval tooling; DROP = no value for the unified design.

## 0. Source map and provenance

| Item | Fact | Source |
|---|---|---|
| Tip read | `6c0984326cbb8fb06c4a36065de58b171d3f8175`, 2026-11-14 04:38:11 UTC, "chore(eval): untrack 96 raw claude transcripts that were committed by mistake" | `git log 4a22d7421..6c0984326` |
| Commits after run-1 commit `4a22d7421` | `c2ddeb1b4` 2026-11-13 16:17:36 "docs(eval): add independent second hand-off run and run 1 vs run 2 comparison" (adds HO, all six notes, the run 2 report); `fd69a006d` 2026-11-13 20:25:07 panel-collaboration brainstorm and five redesign designs; `d561461fa` 2026-11-14 04:37:57 panel-process-redesign brainstorm and five collaboration harnesses; `6c0984326` untrack of 96 raw transcripts | `git log` |
| Material sizes at tip | HO 67 lines; R1CM 66; R1CP 100; R1TT 13; R2CM 160; R2CP 195; R2TT 137 | `git show <tip>:<path> \| wc -l` |
| Run reports (outside this slice) | run 1 `HANDOFF-review-panel-unification.md` = 315 lines (HO:11 says 315, `[V]`); run 2 `HANDOFF-review-panel-unification-run2.md` = 543 by `wc -l` (HO:11 says 544; off by one, trivial) | `git show` |
| Files exist only at the tip | `ls .dev/eval-workspaces/tasklist-review-panel` fails in this worktree; every path in this slice is read through `git show <tip>:<path>` | shell |
| Branch relation | merge-base of HEAD and the E2 tip = `ec259f1b718ccdb9f08bba0237bfa47b2b7601a2`; E2 changes no product code: `git diff --stat ec259f1b7 <tip> -- src tests` is empty `[V]` (HO:63, R2TT:115) | git |
| Master relation | `git rev-list --count ec259f1b7..origin/master` = 11 `[V]`; HEAD of this worktree already contains `d2d8a2d16` (#519) and `167184c6b` (#518) | git |
| Dates inside notes | R1CM/R1CP "Read 2026-11-13"; R2CM "verified by Read on 2026-11-13"; R2CP "Date: 2026-11-13"; R2TT "Date: 2026-11-14"; HO "Date: 2026-11-13" | note headers |
| Independence statements | R2CM:6 and R2CP:5 say neither opened `/tmp/handoff-notes/` or any `HANDOFF-review-panel-unification*.md`; R2TT:120 says run 1's hand-off file was "not opened, per independence rule" | notes |

## 1. HO (`HANDOFF-run1-vs-run2.md`) claim inventory

### 1.1 Header table and verdict (HO:1-16)

| # | Claim | Line | Status | Note |
|---|---|---|---|---|
| H1 | Same brief both times: the `/tech-research` hand-off prompt for unifying the tasklist Review Panel with reflect Tier 2; date 2026-11-13 | HO:3 | `[UNVERIFIED]` | the brief itself is not in this slice |
| H2 | Run 1 = `HANDOFF-review-panel-unification.md` (commit 4a22d7421), Sonnet 5.5 Tier 1b orchestrator; the orchestrator wrote the report with the whole session's context, from 3 read-only investigation agents | HO:7-9 | file and commit `[V]`; process `[UNVERIFIED]` | run 1 notes = R1CM, R1CP, R1TT (3 files, matches) |
| H3 | Run 2 = `...-run2.md`, Opus 5.5 Tier 1a orchestrator, all agents pinned to Opus; 3 new investigation agents plus a new writer agent that could not open run 1's report or notes; the orchestrator wrote none of run 2's text and only corrected one wrong date | HO:7-9 | `[UNVERIFIED]` | independence statements exist in R2CM:6, R2CP:5, R2TT:120 |
| H4 | Neither run used the full tech-research task-file machinery | HO:10 | `[UNVERIFIED]` | |
| H5 | Lengths 315 and 544 lines | HO:11 | 315 `[V]`; 543 by `wc -l` | trivial |
| H6 | "Use run 2 as the main hand-off"; run 2 catches four facts run 1 got wrong or missed, two change the unification plan (rows 1 and 2) | HO:16 | internal inconsistency | section 2 lists eight rows (HO:22-29), not four |
| H7 | "Each claim below was checked against the source" | HO:16 | partly false by HO's own text | rows 5, 6, 7 say "not re-checked" (HO:26-28) |

### 1.2 Section 2 "Where run 1 was wrong or missed something" (HO:18-29), row by row

| Row | What HO says | HO check column | My check at HEAD / tip | Status |
|---|---|---|---|---|
| 1 Master has moved | Branch 11 commits behind origin/master; `d2d8a2d16` (#519 "Stage 0-2 of the Tier 2 review panel") and `167184c6b` (#518 tier decisions) changed 40 files under `src/superclaude/cli/review` and `tests/review`, +8,026 lines; `findings_v2.py` has the same 12-200 anchor limits; `cluster.py`, `hard_exclude`/`strict_distinct`, reflect panel templates | `git diff --stat ec259f1b7 origin/master -- src/superclaude/cli/review tests/review` = 40 files, +8,026 | Same command at HEAD gives `40 files changed, 8026 insertions(+), 15 deletions(-)` `[V]`. Split: #518 touched 1 file there (`tests/review/test_review_panel_live7.py`, +24); #519 touched 39 files (+8,002/-15). `findings_v2.py` anchor/anchor2/citation-quote 12-200 at `findings_v2.py:80,126,132,136`, claim 300 at `:111` `[V]`. `cluster.py` 487 lines, `cluster_v2` at `cluster.py:381`, "chained" at `:33,:324,:370` `[V]`. `hard_exclude`/`strict_distinct` at `P:506-519`, `PC:73,101-102` `[V]`. Reflect templates `data/review-panel.reflect-{pre,pre-x2,post,post-x2,lite,enterprise}.json` `[V]` | `[V]` |
| 1 (impact) | "Run 1's defect list cites line numbers that are stale on master" | | `git diff --numstat ec259f1b7 HEAD` for `findings.py`, `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `telemetry.py`, `telemetry_cmd.py`, `data/review-panel.{default,live7}.json` = empty (byte-identical). Changed: `panel.py` +194/-12 (525 to 707 lines), `panel_cmd.py` +45/-3 (87 to 129), `__init__.py` +3, `data/review-tiers.default.json` +6 (new `classes` map). | partly `[CODE-CONTRADICTED]`: merge/ledger/findings/telemetry line cites remain exact at master; only panel/panel_cmd/init/tiers cites are stale |
| 1 (attribution) | "Run 2 said" the 40 files / +8,026 / findings_v2 / hard_exclude facts | | R2CP:121 says only "#519 ... may overlap the unification topic (UNVERIFIED, not inspected)"; the numbers come from the run 2 report (its K1, Q1-Q3), not from R2 notes | note-vs-report gap |
| 2 Where tasklist review runs today | Run 1 said "No tasklist review step exists in sc-tasklist or sc-workflow" (run 1 D14); run 2: sc:workflow Wave 4 runs `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` (advisory); sc-tasklist Stage 10.5 runs `/sc:reflect --mode pre --remediate` per phase | `sc-workflow-protocol/SKILL.md:60, :76`; `sc-tasklist-protocol/SKILL.md:1630` | At HEAD: workflow Wave 4 heading `SKILL.md:85`, the call at `:89` (flags `--mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md`, "no `--remediate`", defaults for the rest); cited `:60,:76` are base lines, #511 added 31 lines. Tasklist `### Stage 10.5: Pre-Reflect Sign-off` at `:1619`, command at `:1630-1636`, per-phase fan-out, verdict "non-blocking" `[V]`. Narrow grep (`superclaude review`, `review_ledger`, `review loop`) in both skills = no hits at HEAD `[V]` | `[V]`; run 1's literal claim ("no review step") is wrong, its narrower claim (no panel/ledger wiring) is right |
| 3 Audit summaries | Run 1: "summaries in summary.md" for audit-A..F; run 2: only audit-A and audit-D have `summary.md`; B, C, E, F hold scripts and `flags.tsv`; conclusions in COMBO-REPORT lines 290-298 | `ls analysis/audits/*/summary.md` = 2 | tip tree: `audit-A/summary.md`, `audit-D/summary.md` only `[V]`; `COMBO-REPORT.md:290-298` carries audit findings 1-7 plus statistics `[V]` | `[V]` |
| 4 Helper scripts in 4a22d7421 | Run 1: "Only files that reference this eval were copied"; run 2: `snap.py`, `drift-b3.py`, `rlog-r3.sh` belong to `brainstorm-reflect-panel`; `snap.py` writes into that other worktree | `grep -l brainstorm-reflect-panel tools/tmp-scripts/*` = 3 | tip: exactly those 3 files contain the string `[V]`; `snap.py:4` is `open("/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboD-r1/artifacts/input-snapshot.yaml","w")` = a write into THIS worktree's E1 evidence tree `[V]`. `tmp-scripts/README.md` says "only files that reference this eval (path, run-reviewer, combos/, arms/scoring)" `[V]`. Count of such scripts: HO says 3; R2TT:67 names 4 (adds `brief_c1.py`, whose line 3 is the relative path `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614`, so it also belongs to E1's eval but has no absolute worktree path) | `[V]`; count 3 vs 4 differs by `brief_c1.py` |
| 5 Run-reviewer harness bugs | Three open bugs in `run-reviewer.sh:57-87`: `expected_model` overwritten on fallback; attempt files overwrite across fallback models; `BLOCK_OK` checks only the fence line | "not re-checked line by line" | tip `tools/run-reviewer.sh`: `:76` `MODEL="$NEXT"; MODEL_LADDER=...; attempt=0` and `:58` writes `expected_model` from `$MODEL` (= the fallback model) `[V]`; attempt files named `$RID.attempt$attempt` (`:48`) are reused after `attempt=0` (`:76-79`), and `:85` copies the last attempt `[V]`; `:57` `BLOCK_OK=false; grep -q '^```findings-v1' ...md && BLOCK_OK=true` = presence only `[V]`. HO says run 1 "described the ladder as fixed": R1TT:9 describes the ladder, guards and `NOFALLBACK`, never says "fixed" | bugs `[V]`; attribution to run 1 `[UNVERIFIED]` |
| 6 Raw-file count | Both: 3,041 untracked files; `RAW-TRANSCRIPTS-NOT-COMMITTED.md` says 2,916 raw files; counts do not reconcile; per-attempt meta files also uncommitted contrary to that note | "Not re-checked" | R1TT:11 and R2TT:125-128 agree: 1380 `*.attemptN.json`, 1352 `*.attemptN.meta.json`, 309 other/`judge.json` = 3041. RAW note (tip) says "About 1.48 GB ... 2,916 files". 1380+309 = 1689 raw transcripts, not 2,916 `[V arithmetic]`. The untracked set lives in the other worktree: `[UNVERIFIED]`. New at tip: commit `6c0984326` untracks 96 raw transcripts; `git ls-tree -r <tip>` finds 0 files matching `attempt[0-9]+\.json$\|judge\.json$` `[V]` | counts `[UNVERIFIED]`; reconciliation open |
| 7 Reproducibility | Committed analysis scripts read or `exec` `/tmp` copies (`final-table.py`, `three-way.py`, `b9-table.py`, `doubles.py`, `issue-setup.py`) | "From run 2 (H10); not re-checked" | tip: `final-table.py:23` reads `/tmp/audit-{k}/flags.tsv`; `three-way.py:4` `exec(open("/tmp/final-table.py")...)`; `b9-table.py:3` reads `/tmp/b8-table.py`; `issue-setup.py:3` `exec(open("/tmp/final-table.py")...)`; `doubles.py:3` reads `/tmp/attrib.json` `[V]` | `[V]` |
| 8 Test count | Run 1: 299 passed with self-contradicting per-file count; run 2: 304 passed (13 files, 159 functions, 304 collected), per-file table; run 2's command includes `test_review_brief_placement.py` which run 1 left out | | 299 + 5 (`test_review_brief_placement` has 5 test functions, R2TT:23) = 304 `[V arithmetic]`; R1TT:2 lists 5 skills files, not `brief_placement` `[V]`; per-file collected in R2TT:16-28 sum to 126 (tests/review) + 178 (tests/skills) = 304 `[V arithmetic]`. At HEAD def counts moved (see section 5); I did not re-run pytest | `[V]` arithmetic; pass status at HEAD `[UNVERIFIED]` |

### 1.3 Sections 3-6 of HO

| Item | Claim | Line | Status |
|---|---|---|---|
| H8 | Retractions table (run 2 report section 2.3) lists every number that must not be reused, incl. the corrupted-judge "8/14, 5/8" headline run 1 never named | HO:33 | `[UNVERIFIED]` (report outside slice). COMBO-REPORT supports the retraction: `COMBO-REPORT.md:297` "n2-sonnet-src 8/14-5/8 at its table row" listed as retracted `[V]` |
| H9 | Merge defects split finer: chaining and ref-mismatch splitting separate (D4, D5); missing-anchor rows counted (46, 13 blocking); a clearing defect (D3, docstring contradicts code); one re-review reviewer can downgrade a blocker (D9); `merge` always exits 0 (D12) | HO:34 | code facts `[V]` (section 3). The D-numbers are the run 2 REPORT's numbering, which differs from R2CM's numbering (see 2.4). "46 rows, 13 blocking" `[UNVERIFIED]` here |
| H10 | Gateway resolution picks duplicate models in 26 of 40 `@live7` run ids; gateway `launch` map is empty; muse-ember (default panel's model) missing from tier data; so the product panel cannot launch the recommended panels (P1-P5, K5) | HO:35 | `[V]`: I re-ran `superclaude review panel resolve --template @live7 --env gateway --run-id r1..r40`: 26 of 40 contain a duplicate model; `run-a` gives t2b-1 and t3-2 both `glm-5.3` (R2TT:37 says the same); `data/review-tiers.default.json` gateway `"launch": {}`; `grep muse-ember src/superclaude/cli/review/data` = no hit |
| H11 | Brief vs parser: brief states the 200-char anchor limit yet luna, ember, wonder still broke it; claim, refs, id, MINOR-blocking limits are not in the brief at all (B-2) | HO:36 | `[V]`: `RP:60` (HEAD) states anchor "12 to 200 characters", `refs` meaning, categories; no 300, no 8, no 16-char id, no MINOR rule. Model breakdown of drops `COMBO-REPORT.md:292` (luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet 0, terra 0, sol 0; 80 reviewer-level cases, 49 blocking findings lost, four verdicts flipped) `[V]` |
| H12 | 18 numbered requirements U1-U18 with must/should; regression benchmark target "ember + 2x luna: 1.83/14, 0.17/8, 1.83 wrong blockers, 0.83/2, ~64k tokens" | HO:37 | requirements `[UNVERIFIED]`; numbers `[V]` in `COMBO-REPORT.md:331` (`ember + luna + luna | 6/6/6 | 1.83 | 0.17 | 1.00 | 1.83 | 0.83 | 0.83 | 63,644`) and `:366`, `:378` |
| H13 | Decision log DM1-DM18 with dates; 11 open decisions with owners | HO:38 | `[UNVERIFIED]` (report outside slice) |
| H14 | Questions Q1-Q3 aimed at master's #519 code: does `findings_v2` still drop whole findings; does `cluster.py` chain; do `hard_exclude`/`strict_distinct` fix duplicates | HO:39 | answered at HEAD in section 6 below (Q1 yes drops; Q2 detects chaining but ledger path still uses v1 `cluster`; Q3 only when exclusion flags are passed) |
| H15 | Keep from run 1 (section 4): `lint_cmd`/`estimate_cmd` registered but missing, `ModuleNotFoundError` swallowed (`__init__.py:19-32`) | HO:45 | `[V]`: `__init__.py` lists `lint_cmd`, `estimate_cmd` in the loop; `src/superclaude/cli/review/lint_cmd.py` and `estimate_cmd.py` do not exist; the `except ModuleNotFoundError` re-raises other module names and `continue`s for the missing module. HEAD adds `cluster_cmd`, `verify_cmd`, `manifest_cmd` to the same list (`__init__.py:26-28`) |
| H16 | Keep: review-ledger skill, `spec-panel-ledger`/`-stoprule` commands, `finding-grader` agent exist only as experiment copies under `.dev/experiments/346-validation/phase5/final-bundle/builds/` | HO:46 | `[V]`: HEAD `src/superclaude/skills` has no ledger/stoprule/diffgate dir; `src/superclaude/commands` has only `spec-panel.md`; no `*grader*` in `src/superclaude/agents`; `src/superclaude/scripts` has 3 files, none stoprule; `.dev/experiments/346-validation/phase5/final-bundle/builds/` holds `diffgate ledger minfix ponytail stoprule`. Note the session's skill list names `sc-review-ledger`, `sc-spec-panel-stoprule-protocol`, `finding-grader`: installed under `~/.claude` (E3) only |
| H17 | Keep: one-table model-by-role summary; pilot decision rule (only arm C passes, by one defect); "missing-requirement is Medium by instruction but may be blocking in the schema" conflict | HO:47-49 | role table: R1CP:22-30 (tier table) `[V]` for the tier part; pilot rule outcome `[UNVERIFIED]` (PILOT-REPORT not in slice); missing-requirement conflict `[V]` (RP:31 vs `F:102` + `F:98-101`: only MINOR+blocking is rejected; see 3.3) |
| H18 | Agreement list (9 items): ceiling ~2-2.5/14; default ember + 2x luna, sonnet + 2x luna optional, haiku + 2x luna best real blocking; 200/300 drop biggest loss (49 blocking lost, 4 verdict flips); source-blind 156 of 665 runs, "because the brief names no source document"; one reviewer's `blocking` decides, no calibrator; `T01.02` lost as ref; `distinct_across_slots` silent duplicate fallback; telemetry defined but not written; branch changes no product code | HO:51-63 | ceiling/guidance `[UNVERIFIED]` (study results; `COMBO-REPORT.md:366` supports default); 49/4 `[V]` at `COMBO-REPORT.md:292`; 156 of 665 `[V]` at `COMBO-REPORT.md:373` (the earlier 161 at `:293` is the pre-skip count), BUT `COMBO-REPORT.md:373` also says "The cause (the brief never names source.md) is an inference, UNVERIFIED" while HO:58 states the cause as fact: `[CLAIM-OVERSTATED]`; one-reviewer blocking `[V]` (`L:187,213-218,99-104,273-274`); `T01.02` lost `[V]` (3.2); silent duplicates `[V]` (4.2); telemetry unwritten `[V]` (4.4); no product code change `[V]` |
| H19 | Recommended action: give the other session run 2 plus HO section 4; re-check run 2's D1-D13 and P1-P7 against origin/master (#519) because both runs cite the old base; remove `snap.py`, `drift-b3.py`, `rlog-r3.sh` from the folder (deletion waits for the owner) | HO:67 | `[V]` that the re-check matters; results in sections 3-4 below: most D cites still exact, panel cites (P1-P7) moved; the removal is an E2 owner decision, but `snap.py` is a live write path into E1's evidence tree (see conflict C-S2) |

## 2. Run 1 vs run 2 at the notes level (disagreements, agreements, corrections)

### 2.1 Disagreements between the two sets of notes

| ID | Topic | Run 1 notes | Run 2 notes | Adjudication (code at HEAD or tip) |
|---|---|---|---|---|
| X1 | Does a tasklist review exist today? | R1CP:8 and :81 "NO tasklist review step in either skill in src"; R1CP:99 "sc-tasklist-protocol and sc-workflow-protocol contain no panel step" | R2CP:191-194: reflect UC-1 runs it: sc-tasklist Stage 10.5 per phase (`SKILL.md:1619-1646`) and sc-workflow Wave 4 (`:58-64, :76-78`) | run 2 right on "a review exists" `[V]`; run 1 right that the review panel (`superclaude review ...`) is wired to no tasklist/workflow skill `[V]` |
| X2 | T2bModel01 references | R1CP:15, :36: not referenced in `cli/review`; defined in `ccsession-models.json:105-110` and `README.md:445` | R2CP:56: "NOT referenced anywhere in src/ or tests/ ... only CHANGELOG.md:9" | R2's broad form is `[CODE-CONTRADICTED]`: `git grep T2bModel01 ec259f1b7 -- src tests` = `ccsession-models.json:107`, `README.md:445`, `tests/unit/test_ccsession_tiers.py:72,73,239`. Narrow form (panel code never reads it) holds in both (`P:492` reads only `T3Model01`) `[V]`. HEAD adds refs in `sc-implement-protocol/refs/retry.md:162,172`, `tests/skills/test_model_alias_policy.py:227`, `tests/skills/test_workflow_archive.py:799` |
| X3 | Anchor-not-found severity | R1CM:52 MED (finding kept, "a hallucinated anchor still blocks"); R1CM:58 LOW (rows with span None can never reach `resolved_check`) | R2CM D4 HIGH: span None + no refs = never refound, never `resolved_check` (`F:446-447` `hunks_touch(None)` False), stays open and blocking until human defers, forces ESCALATE at cap | facts agree; R2's chain `[V]` (`hunks_touch` returns False for None; `same_defect` span path needs spans; fp path needs refs) |
| X4 | Docstring vs clearing | R1CM:18 and :50 (HIGH defect 1): clearing at `L:254-257` ignores `block_ok`; does not mention the docstring | R2CM:74 and D2: docstring `L:112` "A reviewer with an invalid block is skipped for clearing" is false | `[V]`: docstring at `L:112`, loop `L:253-257` never reads `block_ok` |
| X5 | Severity of silent drops | R1CM:51 HIGH (defect 2), R1CM:19 "Not silent in code, but easy to miss" | R2CM D1 HIGH (partial-panel failure invisible), D9 MEDIUM (limits the prompt does not state) | facts agree; R2 splits partial-panel refusal rule (single reviewer: refuses; N reviewers: PASS possible) from limit drops |
| X6 | Ref-mismatch split | R1CM:53 MED (dedup heuristics: merges distinct, row keeps first member's claim) | R2CM D3 HIGH (ref mismatch splits same defect; tokens like "UTF-8", "ISO-8601", "CVE-2024" scraped from claims), D5 MEDIUM (over-merge) | `[V]`: `_REF_TOKEN` `F:29` matches `[A-Z]{1,4}-[0-9]+...`; run 1 has only the over-merge direction, run 2 both |
| X7 | Revise integrity | R1CM:46 describes the sha guard at `L:308-314` as safe | R2CM D7: `ledger revise` can run twice (guard compares to last round's `doc_sha256`, still equal) and remap spans twice; D8: new text's sha is never stored so next round's `--doc` is not checked | `[V]`: `apply_revision` (`L:301-347`) records no revision marker and no new-text hash; the final loop remaps spans every call (`L:343-346`). Statuses of already-moved rows are protected by the `status not in (open, regressed)` skip, spans are not |
| X8 | Number of code defects | R1CM 13 defects, R1CP 16 defects, R1TT none | R2CM 23 (D1-D23), R2CP 19 | counts differ; no contradiction, run 2 adds D6, D7, D8, D10, D14, D17-D23 (line-model mismatch, two-token fence, quoted example block, non-atomic writes, empty claim, case-sensitive ref token) |
| X9 | Line cites of `reflect-reviewer.md` | R1CP:73 `:4-7`, R1CP:95 "`:7` maxTurns 50 and permissionMode plan" | R2CP:148 `:5-8`; R2CP:163 `:6` pins `model: sonnet` | `[V]` frontmatter at HEAD (file unchanged vs base): `tools` :5, `model: sonnet` :6, `maxTurns: 50` :7, `permissionMode: plan` :8; run 1 is off by one |
| X10 | Tier 2b doc quote | R1CP:36 quotes `MODEL-TIERS.md:42` "if Terra returns 429 retried on GLM-5.3 (owner 2026-11-11)" | R2CP does not quote | `[CODE-CONTRADICTED]` at HEAD: #518 rewrote the Tier 2b row (now `MODEL-TIERS.md:44`, "owner, 2026-11-12": repeated 429s from Terra move to GLM-5.3; the first two other 429s go back to Claude Code to retry, the third parks Terra) |
| X11 | Reflect SKILL line cites | R1CP:73-76 `SKILL.md:86, 128-131, 231-243, 600-612, 1172-1192, 1198, 666`; R2CP:148-157 `SKILL.md:231-239, 598, 600-610, 604-608, 612, 633, 789, 310-314, 1159-1192` | | `SKILL.md` has +68 lines at HEAD (shadow-mode section 4.3a, D1-D5 rules); `--reviewers` at `:86` unchanged, `ANTHROPIC_DEFAULT_*` at `:127`, alias step `:232`, rotation table `:652-654`, spawn text `:646`; content `[V-base]`, line numbers stale for everything after about line 86 |
| X12 | Panel resolve outputs | R1CP:31-35 (run-id `run1`): gateway `@live7` = t1b sonnet, t2-1 muse-spark (depth 5), t2b-1 Qwen3.8-max, t3-1 glm-5.3, t3-2 Qwen3.8-max, t4-1 haiku, t4-2 luna; `@default` = sonnet, spark, glm, Qwen | R2CP:59-75 (run-id `handoff-run2`, base seed 3430211612): `@default` gateway = sonnet, glm-5.3, Qwen, Qwen; `@live7` t2b-1 muse-wonder-1.0 (depth 3), t3-1/t3-2 Qwen | not a conflict: random slots depend on run-id. Re-ran at HEAD: `run1` outputs reproduce R1CP:34-35 exactly; `handoff-run2` `@default` reproduces R2CP:62-64 exactly `[V]` (resolution deterministic per run-id; HEAD adds no random drift) |
| X13 | `T3Model01` reading | R1CP:84 "gateway keyed on `$T3Model01` only (`P:372`)" | R2CP:26, :56 "In this shell `T3Model01=glm-5.3`; resolution picked Qwen for both t3 reviewers" | `[V]`: HEAD `P:486-492` `select_env` reads `T3Model01`; env here also shows `T3Model01=glm-5.3`, `T3Model02=Qwen3.8-max`, `T3Model03=grok-4.7`, `T3Model05=muse-wonder-1.0`, `T3Model06=muse-spark-1.3` (so slot vars exist for T3 beyond what the tier file lists; tier3 file list is only glm-5.3, Qwen3.8-max) |

### 2.2 Agreements between the notes (independent, so higher confidence)

| ID | Agreed fact | R1 | R2 | HEAD |
|---|---|---|---|---|
| A1 | Parser accepts exactly: `findings-v1` fenced block after a "Findings block" heading; per-line JSON; id regex, severity set, bool `blocking`, MINOR cannot be blocking, 6 categories, anchor 12-200 flat chars, claim <= 300, refs <= 8 | R1CM:5-9 | R2CM:8-41 | `F:14-31, 90-121` `[V]` |
| A2 | Drop rules drop one line and set the reviewer `ok=False`; merge refuses only if NO reviewer is ok; warning carries only the first error | R1CM:17-22 | R2CM:45-74 | `L:127-157` `[V]` |
| A3 | Verdict uses only the reviewer `blocking` flag; no quorum; `confidence` single/overlap is computed and unused | R1CM:33, R1CP:65, :87 | R2CM:102, R2CP:128, :171 | `L:86-90, 99-104, 187, 273-274` `[V]` |
| A4 | `--cap` ignored on an existing ledger; `--round` has no upper bound | R1CM:25, :44, :55 | R2CM D12, D13 | `M:62-69, 100-108`; `M:38-42` help "1, 2 or 3" but `IntRange(min=1)` `[V]` |
| A5 | `unpassable-ac` is not an accepted category; only `unpassable-check`; `grep unpassable-ac src` = empty | R1CM:10, R1TT:6 | R2TT:57-58, R2TT:48 | `[V]` (`grep -rn unpassable-ac src` returns nothing at HEAD) |
| A6 | `T01.02`-style task ids are not extracted as refs | R1CM:57, R1CP:44, :89 (both UNVERIFIED, inference) | R2CP:168 (verified by direct call), R2CM:157 (UNVERIFIED) | `[V]` by my own call (3.2) |
| A7 | Telemetry is written by nothing in the product | R1CP:46 | R2CP:94, :174 | `[V]` (4.4) |
| A8 | Brief has no source/driving-document placeholder; only `{{CANDIDATE}}`, `{{BASELINE}}`, `{{PRIOR}}`, `{{N}}`, `{{IDS}}` | R1CP:51, :80 | R2CP:102, :114, :167 | `RP:17-21, 32` `[V]` |
| A9 | `distinct_across_slots` silently falls back to duplicates | R1CP:83 | R2CP:75, :170 | `[V]` (4.2) |
| A10 | No calibrator in the review panel; reflect has the blind `confidence-calibrator` | R1CP:66, :75 | R2CP:128, :155 | `[V]` (6.3) |
| A11 | Gateway `launch` map is empty; dispatch undefined | R1CP:30, :84 | R2CP:27, :169 | `review-tiers.default.json` gateway `"launch": {}` and note "dispatch mechanism per model not defined yet" `[V]` |
| A12 | Telemetry strata hard-coded `sonnet`/`haiku` | R1CP:85 | R2CP:53, :181 | `T:111-115`, `T:267-268` `[V]` |
| A13 | Re-review resolves to the single fixed anchor (`apply_to ["first"]`) | R1CP:20 | R2CP:30, :172 | `[V]` for `@default`, `@live7` (my re-run: `@default --kind re-review` = `t1b-1` only) |
| A14 | Nothing in `cli/review` is tasklist-specific; `grep tasklist` = no hits | R1CM:65, R1CP:98 | R2CM:155, R2CP:189 | `[V]` (still no tasklist logic in `cli/review`; HEAD adds reflect-specific templates/`card_convert`/`verify_cmd`) |
| A15 | Untracked counts 1380 attempt json, 1352 meta, 309 judge/other = 3041 | R1TT:11 | R2TT:125-129 | `[UNVERIFIED]` (other worktree) |
| A16 | `run-reviewer.sh` ladder map, 2 attempts per model, `EXCLUDE_MODELS` default `glm-5.3 Qwen3.8-max`, `NOFALLBACK`, never-revisit guard | R1TT:9 | R2TT:92 | tip `run-reviewer.sh:19-43, 61-83` `[V]` |

### 2.3 Corrections inside the notes

| ID | Correction | Location | Status |
|---|---|---|---|
| K-1 | R1TT:5 says "no dedicated boundary test found" and "Claim length: no limit found in findings.py grep"; R1TT:13 retracts: `test_review_findings.py:112-117` tests anchor < 12, > 200 and claim > 300 (`parse_block ok False`); still uncovered: `unpassable-check` as an accepted category, `resolution.json` by name | R1TT:5 vs :13 | `[V]` at HEAD: `test_field_validation` (`tests/review/test_review_findings.py:111-120`) has anchor `"short"`, 201 chars, `category="weird"`, severity `HIGH`, 9 refs, claim 301, bad id, duplicate id, non-bool blocking; exact boundaries 12 / 200 / 300 / 8 are NOT tested (R2TT:33 correct) |
| K-2 | R1CP:6 `lint_cmd`/`estimate_cmd` "DO NOT EXIST"; R1CP:82 "docs/branches that expect `review lint\|estimate` fail silently" | R1CP | `[V]` still true at HEAD |
| K-3 | R2TT:47 notes `manifest.md` line "Worktree branch: ... (local, never pushed)" is stale (branch is pushed) | R2TT:47, :131 | `[V]` `manifest.md:5` at tip still says "(local, never pushed)" |
| K-4 | R1CM:57 and R1CP:44, :89 mark the `T01.02` regex gap UNVERIFIED (inference) | | upgraded to `[V]` by R2CP:168 and by my call (3.2) |
| K-5 | R2CP:56 narrows to "Observed live: env `T3Model01=glm-5.3` but `@default` gateway resolved both t3 reviewers to Qwen3.8-max"; whether the gateway alias can be steered to a specific underlying model UNVERIFIED | R2CP:56-57, :169 | `[V]` observation; steering `[UNVERIFIED]` |

### 2.4 Numbering hazard (IDs differ between notes and reports)

HO cites D-, P-, B-, K-, Q-, U-, DM-, DO- numbers. Those are numbers of the run 2 REPORT (`HANDOFF-review-panel-unification-run2.md`), not of R2CM's own D1-D23 or R2CP's defect list 1-19. Confirmed by `grep` of the report table at the tip:

| Defect | R2CM (notes) | Run 2 report (HO cites these) |
|---|---|---|
| partial-panel failure invisible | D1 | D2 |
| docstring says skipped for clearing | D2 | D3 (HO:34 "D3, the docstring contradicts the code") |
| ref mismatch splits one defect | D3 | D5 |
| anchor not found, never refound | D4 | D6 |
| over-merging / chaining | D5 | D4 |
| first-row-only match (`break`) | D6 | D10 |
| revise twice / new-text hash | D7, D8 | D11 |
| drop for limits not in prompt | D9 | folded into report D1 and B-2 |
| `merge` exit code always 0 | D11 | D12 (HO:34 "D12") |
| refound row takes current round's blocking | R2CP defect 6 | D9 (HO:34 "D9") |
| task ids not refs | R2CP defect 2 | D7 |
| any single blocker fails | R2CP defect 5 | D8 |

Consequence for the final report: cite a defect by file:line, or by (document, id) with the document named; never by a bare "D4".

## 3. Code facts recorded about findings / merge / ledger (`src/superclaude/cli/review/`)

Base check: `findings.py` (457 lines), `ledger.py` (494), `ledger_cmd.py` (137), `merge_cmd.py` (118), `telemetry.py` (447), `telemetry_cmd.py` (98) are byte-identical between `ec259f1b7` (the runs' base) and HEAD (`git diff --numstat` empty), so every line cite below that I re-read is exact at HEAD. "Dest" = destination in the unified design (vocabulary at top).

### 3.1 findings-v1 format and parser (`F`)

| ID | Fact | Note cite | Code at HEAD | Status | Dest |
|---|---|---|---|---|---|
| F1 | `SEVERITIES = (CRITICAL, MAJOR, MINOR)`, case-sensitive; no MEDIUM/LOW | R2CM:11 | `F:14` | `[V]` | CORE (enum) |
| F2 | `CATEGORIES` = contradiction, unpassable-check, data-loss, safety, missing-requirement, other | R1CM:9, R2CM:12 | `F:15-22` | `[V]` | CORE; M-TL needs its own categories (coverage, traceability, dependency, AC) |
| F3 | `PRIOR_STATUSES` resolved/open/regressed; `ACTIONS` applied/rejected | R2CM:13 | `F:23-24` | `[V]` | CORE |
| F4 | id regex `^[A-Za-z0-9][A-Za-z0-9._-]{0,15}$` (16 chars max) | R1CM:9, R2CM:14 | `F:26,92` | `[V]` | CORE |
| F5 | `_FENCE` single-token info string; `~~~` and ``` ` accepted; `"```json findings-v1"` does NOT match | R1CM:6, R2CM:15, D19 | `F:27` | `[V]` (regex) | CORE; brief wording |
| F6 | `_HEAD_FINDINGS` `^#{1,6}\s+Findings block\s*$` any level, case-insensitive; first match only; error text names `## Findings block` | R1CM:5, R2CM:17, D20 | `F:31, 45, 131` | `[V]` | CORE |
| F7 | Block scan: from the line after the heading to EOF, every fence collected whose info == `findings-v1`; closing fence = same char, >= length, no info; unclosed => `closed=False` | R1CM:6, R2CM:19 | `F:40-76` | `[V]` | CORE |
| F8 | No heading => ok False; heading but no block => ok False; >1 block => ok False and LAST block used; unclosed => ok False, lines still parsed | R1CM:7, R2CM:22-25 | `F:128-158` (`>1` at `F:143-150`, unclosed at `:151-158`) | `[V]` (>1 and unclosed read) | CORE |
| F9 | One JSON object per line; blank skipped; non-JSON/non-dict => error, line skipped; pretty-printed multi-line JSON fails every line | R1CM:8, :62, R2CM:26 | `F:160-174` | `[V-base]` | CORE |
| F10 | Finding checks in order: id, dup id, severity, bool blocking, MINOR+blocking, category, anchor 12..200 flat, anchor2 12..200 or null, refs list <= 8 of str, claim <= 300 flat (no minimum; empty claim accepted) | R1CM:9, R2CM:28-37, D22 | `F:90-121` | `[V]` | CORE |
| F11 | Unknown extra keys accepted silently; reviewer-supplied `confidence` ignored | R1CM:9, R2CM:38-39 | no whitelist in `_check_finding` | `[V]` | CORE (v2 schema now rejects `calibrated_confidence`, `findings_v2.py:3-4`) |
| F12 | `prior` lines: needs non-empty id and status in `PRIOR_STATUSES`, other keys ignored | R1CM:11, R2CM:27 | `F:175-187` | `[V-base]` | CORE |
| F13 | Length counted after whitespace flattening (`flat()`): a long raw anchor with heavy whitespace passes; markdown differences (`**`, backticks) fail `locate` | R1CM:61 (LOW 12), R2CP:115 | `F:79-87` (`_check_flat` uses `len(flat(value))`) | `[V]` | CORE (anchor policy) |
| F14 | `locate`: whitespace-flattened exact substring, all occurrences, half-open 0-based line range; `annotate` takes FIRST occurrence; `anchor_status` found/missing and `anchor_ambiguous` computed | R1CM:13, R2CM:41 | `F:276-304, 345-360` | `[V]` | CORE |
| F15 | `anchor_status` and `anchor_ambiguous` are read by nothing in `src/` or `tests/` except `findings.py` and `tests/review/test_review_findings.py:219,223,230` | R2CM:66 | grep | `[V]` (HEAD adds no reader) | CORE: wire or drop |
| F16 | Missing anchor => `span None`, `section "none"`, finding kept, no warning | R1CM:13, :52; R2CM:66 | `F:349-358` | `[V]` | CORE (needs a gate, see D-defects) |
| F17 | `refs_norm`: `_REF_TOKEN` matches from anchor, anchor2, claim, refs; uppercased; pure numeric section refs from `refs`; `SHA-*` dropped; `_REF_TOKEN` is case-sensitive so `ac-1` is not recognised | R1CM:14, R2CM:41, D23 | `F:29-30, 321-337` | `[V]` | CORE (id grammar must become configurable per document type) |
| F18 | `fp = sha256("v1|section|refs")[:16]` | R2CM:41 | `F:340-343` | `[V]` | CORE |
| F19 | `same_defect`: same fp AND non-empty refs_norm => same; else refs intersect or both empty, and spans within 3 lines => same; transitive union-find; findings of the same reviewer can merge | R1CM:29, R2CM:88-91 | `F:367-379, 382-407` | `[V]` | CORE (E1 `cluster.py` `same_defect_v2` is the successor; see 6.4) |
| F20 | `fixmap-v1` JSON lines `{id, action, reason}`; fallback table regex `\| id \| applied` yields `applied` only; any table row whose second cell starts "applied" counts | R1CM:46, R2CM:121, D16 | `F:199-223` | `[V]` | CORE (revise contract) |
| F21 | Line-model mismatch: `locate` counts `\n` (`F:295-296`), `_blocks_after` counts `\n` for the heading (`F:48`), while `lines`, `section_of`, `opcodes` use `str.splitlines()` (`F:49, 309, 415`), which also splits on lone `\r`, `\x0b`, `\x0c`, `\x1c-\x1e`, `\x85`, U+2028/9 | R2CM:146 (D18) | `F:48-49, 295-296, 309, 415` | `[V]` (mechanism) | CORE bug |

### 3.2 Reference-id regex versus tasklist ids

| ID | Fact | Source | Status |
|---|---|---|---|
| R-1 | `_REF_TOKEN` needs `LETTERS-DIGITS(.DIGITS)*` or `P<digit>`; tasklist task ids are `T<PP>.<TT>` (no hyphen): `sc-tasklist-protocol/SKILL.md:340` ("Task IDs are zero-padded: `T<PP>.<TT>`"). R2CP:168 cites `:1136` for the format, but `:1136` is the heading `### T<PP>.<final> -- Post-Execution Reflection` | R1CM:57, R1CP:44, :89; R2CP:168, R2CM:157 | `[V]`; R2's line cite is off (should be `:340`) |
| R-2 | My direct call at HEAD: `annotate(...)` with refs `["T01.02","R-012","3.2","AC-1"]` and claim "task T03.04 uses D-0003" gives `refs_norm = ['3.2','AC-1','D-0003','R-012']`; `T01.02` and `T03.04` are dropped; `R-012` and `D-0003` (tasklist Roadmap/Deliverable ids) are kept | R2CP:168 (same result) | `[V]` |
| R-3 | Same regex shape in telemetry (`T:23-24` `_ID_TOKEN = (?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*\|P[0-9])\b`), so `ids_defined` / `cross_refs` undercount tasklists | R1CP:44, R2CP:168 | `[V]` |
| R-4 | Consequence: tasklist findings fall back to span-proximity clustering (false merges within 3 lines, splits for far-apart anchors) | R1CP:89 (inference), R1CM:57 | `[UNVERIFIED]` on data; mechanism `[V]` |
| Dest | CORE must take the id grammar from the document-type profile (spec ids `AC-/FR-`, tasklist `T<PP>.<TT>`, `R-###`, `D-####`, reflect file:line citations) | | |

### 3.3 Drop rules, warnings and partial-panel behaviour (`L:107-160`)

| ID | Fact | Note cite | Code | Status | Dest |
|---|---|---|---|---|---|
| G1 | Each failed rule drops ONLY that line (`continue`) and sets whole reviewer `ok=False` | R1CM:17-18, R2CM:47 | `F:188-192` | `[V-base]` | CORE |
| G2 | Rules that drop: not JSON; not object; bad prior; id > 16 or bad; duplicate id; severity not in set (incl. "MEDIUM", lowercase); `blocking` not bool ("true"); MINOR+blocking (dropped, not downgraded); bad category; anchor/anchor2 < 12 or > 200; refs not list / > 8 / non-str; claim > 300 or non-str | R2CM:49-63 | `F:90-121, 163-187` | `[V]` | CORE (repair or reject loudly) |
| G3 | One warning per reviewer: count of errors and ONLY the first message; warnings go to stdout JSON only; the merged report shows only `block ok false` per reviewer; the ledger stores only `block_ok` | R1CM:19, R2CM:70-73 | `L:130-134, 141-149, 421-424`; `M:117-118` | `[V]` (`L:130-134`, `L:147`) | CORE |
| G4 | Valid findings of a reviewer with a bad block are still merged | R1CM:18, R2CM:71 | `L:135-138` | `[V]` | CORE |
| G5 | Merge refuses only when NO reviewer has `ok=True`; ledger unchanged and `--out` not written | R1CM:20, R2CM:72 | `L:150-157` | `[V]` | CORE |
| G6 | Therefore a reviewer whose only blocking finding is dropped for length can still let the round PASS if another reviewer is ok; with ONE reviewer the same failure refuses the merge (behaviour depends on panel size) | R1CM:22, R2CM D1 | `L:150, 273-274` | `[V]` | CORE (partial-panel rule) |
| G7 | Docstring `L:112` ("skipped for clearing") is false; clearing loop never consults `block_ok` | R2CM:74, D2; R1CM:50 | `L:112` vs `L:253-257` | `[V]` | CORE bug |
| G8 | Drop evidence at study scale: 80 reviewer-level cases, 49 blocking findings lost (anchor > 200: 56; anchor2 > 200: 18; claim > 300: 14), by model: luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet 0, terra 0, sol 0; four verdicts flipped FAIL to PASS | `COMBO-REPORT.md:292` (not in the notes) | | `[V]` (report line) | EVID; drives requirement "repair, do not drop" |
| G9 | `missing-requirement` is Medium (non-blocking) by instruction `RP:31`, but the schema allows `blocking:true` for it: `F:98-103` rejects only MINOR+blocking; so reviewers following the schema literally over-block | R1CM:12 (D9 in HO), R1CP:52, :91 | `RP:31`; `F:98-103` | `[V]` | CORE rubric + brief |

### 3.4 `superclaude review merge` and ledger flow (`M`, `L`)

| ID | Fact | Note cite | Code | Status | Dest |
|---|---|---|---|---|---|
| L1 | Options: `--ledger` (created at round 1), `--doc`, `--round` (`IntRange(min=1)`, help "1, 2 or 3"), `--report ID=PATH` repeatable, `--resolution` (optional; only `reviewers[].reviewer_id` and `.model` read), `--out`, `--cap` (default 3, only used when round 1 creates the ledger) | R1CM:25-26, R2CM:78 | `M:21-70, 100-108` | `[V]` | CORE |
| L2 | Reviewer missing from the resolution gets `model None` silently; resolved reviewers with no `--report` are not detected; reviewer id = split on first `=`, no format validation | R1CM:26, :59, R2CM:81, D14 | `M:84-96` | `[V]` | CORE |
| L3 | Malformed resolution => ClickException (`{resolution} is not a panel resolution`) | R2TT:36 (untested path) | `M:74-83` | `[V]` | CORE |
| L4 | `merge_round`: round must equal `len(rounds)+1`; duplicate reviewer ids refused; no `n <= cap` check, so round 4 merges and gets ESCALATE | R1CM:36, :44, R2CM:85, D12 | `L:114-121`; `_decision` `L:93-96` | `[V]` | CORE |
| L5 | Cluster all findings from all reviewers; each cluster matches the FIRST existing row (pre-round snapshot, creation order; `break`) for which any member is `same_defect` with the row view {fp, span, span2, refs}; no match => new row `L{k}` | R1CM:30-31, R2CM:92-93, D6 | `L:160-200` | `[V]` | CORE |
| L6 | New row: fp/anchor/span/claim/category from FIRST member; refs = union; `blocking = any member`; `severity_max = max` | R1CM:31, R2CM:93 | `L:181-206` | `[V]` | CORE |
| L7 | Refound row: members appended; `blocking` = THIS round's classification (OR'd across several clusters of the round); `severity_max` only grows; re-anchor to first member with a span; fp/refs/claim/category never updated; `resolved_check`/`resolved` => `regressed` | R1CM:32, R2CM:94, D10 | `L:210-240` | `[V]` | CORE |
| L8 | Because refound `blocking` is the current round's call, a reviewer re-reporting as non-blocking un-blocks the row; with `apply_to ["first"]` a re-review is ONE reviewer (the anchor), so one re-reviewer can downgrade a blocker the full panel raised | R1CM:54 (defect 5), R2CP defect 6 | `L:210-218`; panel templates `apply_to` | `[V]` | CORE (re-review quorum rule) |
| L9 | `resolved_check` rows not refound this round => `resolved`, event "cleared" (no check that the reviewer looked at the row or that its block was valid) | R1CM:34, :50, R2CM:95 | `L:253-257` | `[V]` | CORE bug |
| L10 | `prior` lines only append history `prior_note`; unknown prior id => warning; reviewers cannot change a status ("Only these scripts change a finding's status", `RP:70`) | R1CM:35, R2CM:96 | `L:259-272` | `[V-base]` | CORE |
| L11 | `brief_ids` = rows `blocking` AND status in (open, regressed); `verdict = FAIL if brief_ids else PASS`; decision PASS / REVISE if `n < cap` / ESCALATE | R1CM:36, R2CM:97 | `L:93-104, 273-275` (read) | `[V]` | CORE |
| L12 | Severity does not affect the verdict, only MINOR+blocking is rejected; one blocking finding from one reviewer fails the round; `confidence` (overlap/single) is computed (`L:84-90`) and never used | R1CM:33, R2CM:102 | `L:84-91, 187, 213-218` | `[V]` | CORE (quorum, calibration) |
| L13 | Output order: `--out` written (not atomic; `M` does `makedirs` then plain `open`) BEFORE `led.save` (atomic temp+fsync+`os.replace`); crash in between leaves a merged report with no ledger update; no locking: concurrent merges/revises race | R1CM:28, :59, R2CM:100, D21 | `M:109-116`; `L:52-67` | `[V]` | CORE |
| L14 | `merge` always exits 0; only `ledger verdict` maps decisions to exit codes 0/10/11 (`EXIT_BY_DECISION`) | R2CM:100, D11, R1CM:47 | `M` has no `sys.exit`; `LC:13, :109` | `[V]` | CORE (CI integration) |
| L15 | Merged report: header `review: n of cap`, reviewers with `block ok`, ledger table, `## Blocking findings` per brief id, `## Other findings` = rows with `blocking False` only (so a resolved/deferred blocking row appears only in the ledger table), `## Escalation` (no reviser brief) at ESCALATE else `## Reviser brief` + `REVISER_RULES`; last line `verdict: PASS\|FAIL` | R1CM:38, R2CM:99, D17 | `L:408-494` (read `:462-472`); `REVISER_RULES` `L:22-26` | `[V]` | CORE (report renderer); M-SP reviser wording |
| L16 | `ledger revise`: needs a merged round; `--old` sha256 must match last round's `doc_sha256`; difflib opcodes; `applied` AND a hunk touches span/span2 => `resolved_check`; else `named_not_touched`; `rejected` => `rejected_by_reviser`; then every row's span/span2 remapped; `fixmap_ok` reported but not enforced; can be run twice for one round (spans remapped twice); new-text hash not stored | R1CM:46, :58, R2CM:121, D7, D8, D16 | `L:301-347`; `LC:60-71` | `[V]` | CORE |
| L17 | `defer`: any status => `deferred`, removes lid from last round's `brief_ids`; if brief empty rewrites last round verdict/decision to PASS; no undefer; no audit of who deferred | R1CM:47, :60, R2CM:122, D15 | `L:350-360` | `[V]` | CORE |
| L18 | `verdict` returns last round's stored verdict/decision/brief_ids; exit 0/10/11 | R1CM:47, R2CM:123 | `L:363-372`; `LC:94-109` | `[V]` | CORE |
| L19 | `capture` exports `review-capture/1` (defects x reviewers `captured_by`) per round; `--out` write is non-atomic and does not create parent dirs | R1CM:47, R2CM:124, D21 | `L:375-401`; `LC:112-137` (write at `:134-136`) | `[V]` (`LC:128-137`) | HARNESS/CORE (benchmark matrix) |
| L20 | Ledger schema `review-ledger/1` {schema, doc (path as given, may be relative), cap_reviews, rounds[], rows[]}; row keys lid, fp, blocking, severity_max, category, confidence, status, anchor, anchor2, span, span2, refs, claim, members[{round, reviewer_id, fid, blocking}], history[]; statuses open, resolved_check, resolved, regressed, deferred; lids `L<N>` never reused | R1CM:40-45, R2CM:108-111 | `L:17-19, 37-38, 184-202` | `[V]` | CORE (public contract: E1, E2, E3 all depend on it) |
| L21 | Rounds with a missing-anchor blocking row: stays open until human defers; forces ESCALATE at cap | R2CM D4 | `F:352`, `hunks_touch` `F:446-447` | `[V]` | CORE bug |
| L22 | "Verify-only" rounds 2-3 are not a code mode: any report in any round can open new rows; verify-only behaviour must come from the reviewer prompt | R1CM:44 (UNVERIFIED) | `L:181-206` shows no round-based restriction | `[V]` (code) | CORE option: `--verify-only` (E3 `sc-review-ledger` variant implements it outside src) |

### 3.5 Tasklist-specific versus generic (code)

| Fact | Cite | Status |
|---|---|---|
| All of `cli/review` (findings, merge, ledger, ledger_cmd, panel, telemetry) is document-agnostic; `grep tasklist` = no hits | R1CM:65, R1CP:98, R2CM:155, R2CP:189 | `[V]` |
| Spec-shaped assumptions: category names, `REVISER_RULES` text, id regex (AC-/FR-/P1), numbered-heading section naming (`F:307-318`, slug fallback) | R1CM:66 | `[V]` |
| Only coupling is to the findings-v1/fixmap-v1 contract in `RP:58-66` | R2CM:160 | `[V]` |

## 4. Code facts recorded about panel config, resolution and telemetry

HEAD differs from the runs' base here: `panel.py` 525 to 707 lines (+194/-12), `panel_cmd.py` 87 to 129, `data/review-tiers.default.json` +6 (a `classes` map), `__init__.py` +3, six new `data/review-panel.reflect-*.json` templates, new modules `cluster.py`, `cluster_cmd.py`, `card_convert.py`, `findings_v2.py`, `manifest.py`, `manifest_cmd.py`, `verify_cmd.py`. `telemetry.py`, `telemetry_cmd.py`, `data/review-panel.{default,live7}.json` are unchanged. HEAD line numbers below are new; the note cites are base lines.

### 4.1 Schemas, validation, loading (`P`, `PC`)

| ID | Fact | Note cite | HEAD cite | Status | Dest |
|---|---|---|---|---|---|
| P-1 | Three schema ids `review-panel/1`, `review-tiers/1`, `review-panel-resolution/1` | R1CP:11, R2CP:13 | `P:25-27` | `[V]` | CORE (public contracts) |
| P-2 | Panel keys closed set {schema, template_id, version, description, distinct_across_slots, apply_to, slots}; slot keys {slot_id, tier, count, strategy, seed}; slot_id `^[a-z0-9]{1,8}$`, tier `^tier[0-9]{1,2}[a-z]?$`, count 1..4, strategy fixed/random/round_robin, seed only with random, exactly ONE `fixed` slot (the anchor), total reviewers 1..8, template_id `^[a-z0-9][a-z0-9-]{0,31}$`, semver | R1CP:12, R2CP:14-15 | `P:29-46, 160-257` (`validate_panel` now takes more args) | `[V-base]` (regexes `P:29-36` read) | CORE |
| P-3 | Tier file: `aliases.<tierN>` {alias, models[], placeholder?}; placeholder tier must have `models == []`; `names`; `environments.<env>` {available "all"\|[ids], stand_ins, launch, note}; model id regex | R1CP:13, R2CP:16-17 | `P:258-379`, `_MODEL_ID` `P:34` | `[V-base]` | CORE |
| P-4 | HEAD adds `classes` (model id to class: opus/sonnet/haiku/fable/gpt/muse/glm/grok/qwen) in the tiers file | not in notes | `data/review-tiers.default.json` `classes`; `P:76` `_is_fable` | `[V]` | CORE (class-disjointness is a reflect rule: executor class, calibrator class) |
| P-5 | Lookup precedence: explicit path > `$SUPERCLAUDE_REVIEW_PANEL`/`_TIERS` > `<git root>/.superclaude/review-<kind>.json` > `~/.superclaude/...` > packaged default; `@name` loads packaged `data/review-panel.<name>.json` (works through `--template` or the env var); whole-file replacement, no overlay; `load_panel('@x')` validates WITHOUT tiers, `panel_cmd` re-validates with tiers; a project/user file silently overrides the packaged default (no log of which file was used, only `template_sha256`) | R1CP:14, :92; R2CP:20-22 | `P:380-483` (`find_path :397`, `packaged_panel :430`, `load_panel :447`, `load_tiers :470`) | `[V-base]` (names read at HEAD) | CORE |
| P-6 | Hard-coded model ids: none in `panel.py`; only env names `gateway`/`anthropic-only` and `T3Model01`; telemetry hard-codes strata `sonnet`/`haiku` | R1CP:30, R2CP:51-53 | `P:485-492`; `T:111-115` | `[V]` | CORE |

### 4.2 Environment selection and resolution

| ID | Fact | Note cite | HEAD cite | Status | Dest |
|---|---|---|---|---|---|
| E-1 | `select_env`: `--env` > `$SUPERCLAUDE_REVIEW_ENV` > `gateway` iff `$T3Model01` non-empty > `anthropic-only` | R1CP:15, R2CP:25 | `P:485-492` | `[V]` | CORE (env sniffing is fragile: one variable decides) |
| E-2 | `T2bModel01` is never read by panel code; `@live7` needs the `claude-gw-tier2b` alias but nothing checks it | R1CP:15, :36, :84; R2CP:55-57, :169 | no `T2bModel`/`Model0` reference in `cli/review/*.py` | `[V]` | CORE |
| E-3 | Resolution order: fixed slots first, then others in template order; if `review_kind` not in `apply_to` => ONLY the fixed slot, count 1; `reviewer_id = <slot_id>-<i>`; seed `sha256(run_id)[:8]` or `--seed`; random seed string `<slot.seed or base>\|<slot_id>\|<i>`; `round_robin` seed = `--sequence` or `date.today().toordinal()` plus `i-1` (non-reproducible across days) | R1CP:16, R2CP:30-33 | `resolve` `P:565-707`; `apply_to` `P:600`; sha256 seed `P:609`; `date.today()` `P:625` | `[V]` | CORE |
| E-4 | `resolve_slot`: candidates = tier models in `available`; none => environment `stand_ins`; none => `NoModelAvailable`; fixed => first candidate; random => `random.Random(seed).choice(pool)`; round_robin => `pool[seed % len]`; outputs per reviewer: reviewer_id, slot_id, tier, alias, strategy, seed, model, model_name, fallback_depth, stand_in, fallbacks, launch; top-level template/tiers sha256 | R1CP:16, R2CP:32-33 | `resolve_slot` `P:500-555` | `[V]` | CORE |
| E-5 | Silent duplicate fallback: when exclusion empties the pool, `pool = candidates` (`P:539-543`); HEAD adds: if `hard` exclusion is active it raises `ExclusionExhausted` instead; so duplicates are removed only when `--hard-exclude-class`/`--strict-distinct` is passed | R1CP:83, R2CP:75, :170 (cite `P:405,408`) | `P:539-543`, `P:519` (`hard = set(hard_exclude) \| (set(exclude) if strict_distinct else set())`) | `[V]` (default path still duplicates: re-run at HEAD: `@default` gateway `handoff-run2` = t3-1 and t3-2 both Qwen3.8-max) | CORE |
| E-6 | Fixed slot ignores `exclude` (HEAD: still true unless `strict_distinct`/`hard_exclude` filter `candidates` first, `P:519-525`) | R1CP:83 | `P:536-537` | `[V]` | CORE |
| E-7 | `@live7` gateway duplicates in 26 of 40 run ids r1..r40; `r19` has `glm-5.3` three times (R2TT:37) | R2TT:37 | my re-run at HEAD: 26 of 40 `[V]`; `r19` triple `[UNVERIFIED]` (not checked individually) | `[V]` count | EVID + CORE test |
| E-8 | Gateway `launch` map empty (note "dispatch mechanism per model not defined yet"); every gateway reviewer has `launch: null`; tier alias strings like `claude-gw-tier3[1m]` are the only dispatch handle; whether the gateway serves the resolved model `[UNVERIFIED]` in R2CP:57, :169 | R1CP:84, R2CP:27, :57 | `review-tiers.default.json` | `[V]` map empty; serving `[UNVERIFIED]` | CORE: launch adapters (E2 harness `claude -p --model <raw gateway id>` is the working path) |
| E-9 | `anthropic-only`: available opus/sonnet/haiku/fable 5.x; stand_ins tier2/2b/3/4 to haiku; launch map opus/sonnet/haiku/fable. Resolved: `@default` = 1 sonnet + 3 haiku; `@live7` = 1 sonnet + 6 haiku (t4-1/t4-2 `stand_in=false`, `fallback_depth 1`) | R1CP:31-33, R2CP:66-70 | my re-run: `@live7 anthropic-only` Counter = haiku 6, sonnet 1 `[V]`; `@default` 1+3 not re-run `[V-base]` | `[V]` | CORE |
| E-10 | `claude-fable-5-1` is in `names`, `available`, `launch` but in no tier list | R1CP:30, R2CP:44, :182 | tiers JSON | `[V]`; HEAD adds `_is_fable` and the reflect rule "Fable and Tier 0 are never picked" (`sc-reflect-protocol/SKILL.md:344`) | CORE |
| E-11 | Model-by-tier table: tier1a opus-5-5, sonnet-5-5; tier1b sonnet-5-5, gpt-6.1-sol, muse-wonder-full-1.0; tier2 gpt-6.1-sol, glm-5.3, grok-4.7, Qwen3.8-max, muse-wonder-1.0, muse-spark-1.3; tier2b gpt-6.1-terra, glm-5.3, Qwen3.8-max, muse-wonder-1.0; tier3 glm-5.3, Qwen3.8-max; tier4 gpt-6-luna, claude-haiku-5-5, grok-4.7 | R1CP:22-29, R2CP:36-43 | `review-tiers.default.json` aliases (unchanged lists) | `[V]` | CORE data; E2 study adds muse-ember-1.0 (absent here, see 4.5) |
| E-12 | `muse-ember-1.0` (recommended default panel model) is missing from tier data; `run-reviewer.sh` ladder includes it as a hand-kept map not read from the tier file | R2TT:93, HO:35 | `grep muse-ember data/` = none; tip `run-reviewer.sh:33-34` | `[V]` | CORE data + CORE ladder |
| E-13 | Owner-excluded models (Qwen3.8-max, glm from batch 4) still sit in tier2/2b/3 lists, so resolution keeps picking Qwen | run 2 report P4 via HO | `data/review-tiers.default.json` lists; HEAD `hard_exclude` exists in `P:506-519` | `[V]` data; exclusion is opt-in per call | CORE policy |
| E-14 | Reflect has two model-selection mechanisms (skill: `ANTHROPIC_DEFAULT_*_MODEL` aliases; CLI: `T2Model0N`/`T1Model0N` in `cli/reflect/ensemble.py:7, 186-198`) and the panel a third (tier JSON); run 2: "neither reads `review-tiers.default.json`" | R2CP:184 (INFO 18), :150 | At HEAD the reflect SKILL shadow path DOES call `superclaude review panel resolve --template @reflect-pre ... --hard-exclude-class ... --strict-distinct` (`SKILL.md:340`), and `cli/reflect/ensemble.py` still uses `T2Model0N` (`:7,126,186-198`) | `[CODE-CONTRADICTED]` for the skill path at HEAD (shadow mode only, off by default `--t2-engine legacy`); still true for `cli/reflect` and for the default `legacy` path | CORE: one model registry |

### 4.3 Packaged panels and recorded model-by-run outputs

| ID | Fact | Note cite | Status |
|---|---|---|---|
| T-1 | `@default` = 4 reviewers: t1b x1 fixed (tier1b), t2 x1 random (tier2), t3 x2 random (tier3); `distinct_across_slots true`; `apply_to ["first"]` | R1CP:19, R2CP:47 | `[V]` (resolve prints 4 reviewers) |
| T-2 | `@live7` = 7 reviewers: t1b x1 fixed, t2 x1, t2b x1, t3 x2, t4 x2 (all random); description says the `claude-gw-tier2b` alias must exist before it runs live | R1CP:20, R2CP:48 | `[V]` (7 reviewers) |
| T-3 | Gateway `@live7` `run1` and `@default` `run1` outputs | R1CP:34-35 | `[V]` reproduced exactly at HEAD |
| T-4 | `template_sha256` default `fd2ef963...146ba`, live7 `191ea47f...48a848`, `tiers_sha256` `1a2a8ad2...f3a49` (tiers_version 1.0.0) | R2CP:73 | `[UNVERIFIED]` for HEAD: `data/review-tiers.default.json` changed (+6 lines), so the tiers hash at HEAD differs from `1a2a8ad2...` by construction; the two panel files are unchanged so their template hashes should still hold |
| T-5 | HEAD adds `reflect-pre`, `reflect-pre-x2`, `reflect-post`, `reflect-post-x2`, `reflect-lite`, `reflect-enterprise` templates; `reflect-pre` = t1b fixed + t4 random + t1a random, `distinct_across_slots true`, `apply_to ["first"]`; personas by resolution order analyzer, qa, refactorer | not in notes | `[V]` (`review-panel.reflect-pre.json`) |

### 4.4 Telemetry (`T`, `telemetry_cmd.py`)

| ID | Fact | Note cite | Code | Status | Dest |
|---|---|---|---|---|---|
| Y-1 | Schema `review-telemetry/1`; two kinds `reviewer_run` and `outcome`; no document text, quote, anchor or claim; `context` values limited to short labels | R1CP:39, R2CP:80 | `T:17, 204, 240-251, 256-266` (read `T:111-115, 265-269`) | `[V-base]` | CORE |
| Y-2 | `reviewer_run` groups: panel{template_id/version/sha256, tiers_version/sha256, environment, panel_size}, slot{...}, model{resolved, launch, observed}, task{doc_sha256, doc_bytes, doc_lines, language, doc_format, specialization, sections, max_heading_depth, tables, table_rows, ids_defined, cross_refs, rfc2119, review_kind}, output{block_ok, findings, blocking, by_severity, verdict, verdict_mismatch}, cost{tokens_in, tokens_cache_read, tokens_cache_write, tokens_out, wall_s}, plus `context`, optional `supersedes`, `stratum` | R1CP:41, R2CP:81-88 | `T:30-91` | `[V-base]` | CORE |
| Y-3 | `outcome` keys: reviewer_record_id, truth_basis (catalog-v1\|theme-v1\|adjudicated-v1), confirmed_tp, false_pos, unconfirmed, unique_tp, overlap_mean_jaccard, recall_vs_confirmed, precision, cost_per_confirmed_tp, supersedes, stratum | R1CP:42, R2CP:89 | `T:92-110` | `[V-base]` | CORE |
| Y-4 | `stratum` in {sonnet, haiku} only, "never pooled" (owner decision D3); any other model cannot be tagged | R1CP:85, R2CP:89, :181 | `T:111-115, 267-268` (error text "stratum must be 'sonnet' or 'haiku'") | `[V]` | CORE bug/extension (gateway models) |
| Y-5 | SQLite: tables `reviewer_runs`, `outcomes`; view `model_scores` grouped by model_observed, slot_tier, slot_stand_in, stratum, truth_basis with n_runs, sums, mean precision/recall, `cost_per_confirmed_tp = SUM(tokens_out)/SUM(confirmed_tp)`; superseded rows excluded; loader idempotent; `stratum_conflicts` counted | R1CP:43, R2CP:92 | `T:313-447` | `[V-base]` | CORE |
| Y-6 | Files `<dir>/records/YYYY/MM/<run_id>.jsonl` and `.outcomes.jsonl`; default dir `.dev/benchmarks/review-telemetry` or `$SUPERCLAUDE_REVIEW_TELEMETRY_DIR` | R1CP:40, R2CP:91 | `T:287-307`; `telemetry_cmd.py:12, 43-47` | `[V-base]` | CORE |
| Y-7 | Nobody in the product writes telemetry: `merge_cmd` imports only `ledger`; `panel_cmd` only `panel`; callers of `append_record`/`task_variables` are tests and `.dev/research/346-review-loop-experiments` harnesses (`p22/harness/harness_j3.py:587`, `p18/ab5/full.py:219`, `p13/ab1/report.py:135`) | R1CP:46, R2CP:94, :174 | grep at HEAD: callers are `tests/review/test_review_telemetry.py` only (src callers none); the three `.dev/research` harness files exist (line numbers not re-checked) | `[V]` for src; harness line cites `[UNVERIFIED]` | CORE gap |
| Y-8 | `model.observed` has no producer, so `model_scores` is empty without an external harness | R2CP:95, :174 | grep | `[V]` | CORE gap |
| Y-9 | `task_variables`: regex-based; `doc_format` always "markdown" (`T:180`), `language` "en" if stop-word share >= 2% (`T:179`) | R2CP:90 | `T:142-190` | `[V-base]` | CORE (document-type profile needed) |
| Y-10 | HEAD: `cluster.py` computes the `cluster_agreement` telemetry value (`cluster.py:1`), `manifest` and `verify_cmd` are new measurement/shadow pieces; reflect SKILL writes panel fields under `telemetry:` of the contract (`SKILL.md:969-973`) | not in notes | `[V]` | E1 reuses/extends `review-telemetry/1` |

## 5. Tests, tools and the eval workspace (R1TT, R2TT)

### 5.1 Tests covering `cli/review` and the review-loop prompts

| ID | Fact | Note cite | HEAD check | Status | Dest |
|---|---|---|---|---|---|
| TS-1 | Run 1 command: `tests/review` + 5 `tests/skills/test_{spec_panel_review_loop,review_severity_mapping,review_prompt_overrides,review_severity_rule,review_loop_extension}.py` = 299 passed in 7.1 s; per-file: cli 9, findings 23, ledger 24, panel 26, panel_live7 14, rules_text 5, telemetry 10 (111); skills 11, 8, 14, 21, 9 (63) | R1TT:2-4 | sums 111 and 63 `[V arithmetic]` | pass result `[UNVERIFIED]` (not re-run) | HARNESS |
| TS-2 | Run 2: 13 files, "159 def test_", 304 collected, 304 passed, 0 fail/skip; per-file table R2TT:16-28 | R2TT:12-29 | The per-file `def test_` column sums to 179 (9+23+24+26+14+5+10 = 111; 5+9+14+8+21+11 = 68), NOT 159: the "TOTAL 159" cell in R2TT:29 and HO:29 "159 functions" are an arithmetic error. Collected column sums to 304 `[V arithmetic]` (126 + 178) | `[CODE-CONTRADICTED]` for 159; 304 `[V arithmetic]` | EVID |
| TS-3 | 299 (run 1) + 5 (`test_review_brief_placement.py`) = 304 (run 2) | HO:29, R2TT:23 | `[V arithmetic]` | `[V]` | EVID |
| TS-4 | HEAD changes: `tests/review` now has 19 test files (was 7 relevant); def counts for the 7 files: cli 13 (was 9), findings 23, ledger 24, panel 26, panel_live7 15 (was 14), rules_text 5, telemetry 10 = 116; `tests/skills` files unchanged (68). New files: `test_reflect_cluster_pairs.py` 24, `test_reflect_consumer_inventory.py` 14, `test_reflect_stage0a_replay.py` 15, `test_review_card_convert.py` 52, `test_review_cluster.py` 38, `test_review_cluster_cmd.py` 15, `test_review_findings_v2.py` 24, `test_review_manifest.py` 35, `test_review_panel_exclusion.py` 14, `test_review_panel_reflect_profile.py` 14, `test_review_reflect_templates.py` 11, `test_review_verify_citations.py` 8 | not in notes | def counts by grep at HEAD `[V]`; #518 added 24 lines to `test_review_panel_live7.py`: a new test that the `tier2b/3/4` list lengths equal the slot counts in `ccsession-models.json` and `tier2b[0] == gpt-6.1-terra`, `tier3[0] == glm-5.3`; #519 added 74 lines to `test_review_cli.py` | `[V]` | CORE tests (E1) |
| TS-5 | `tests/cli` has no file for `cli/review`; `tests/cli/reflect/*` is the reflect ensemble and is excluded | R2TT:10 | `ls tests/cli | grep -i review` = empty `[V]` | `[V]` | |
| TS-6 | NOT covered: exact boundaries (anchor 12 and 200, claim 300, refs 8); anchor2 over/under-length; the 4 accepted categories `unpassable-check`, `data-loss`, `safety`, `missing-requirement` never parsed in a test (only `contradiction`, `other` pass; only `weird` rejected); case variants | R2TT:33-35, R1TT:13 | `test_field_validation` at `tests/review/test_review_findings.py:111-120` `[V]`; `unpassable-check` appears only in `tests/review/test_review_card_convert.py:426` (a card-category mapping, not the parser) | `[V]` | CORE tests |
| TS-7 | NOT covered: prompt/code drift (no test asserts the prompt's category list and limits equal `findings.CATEGORIES`/`_check_flat`); malformed resolution; `--report` id absent from resolution; resolved reviewer with no report; `--report` without `=`; duplicate reviewer id in one round (`L:120-121`); rounds past the cap; non-default `--cap` | R2TT:34, :36, :38-39 | grep at HEAD: no test for duplicate reviewer id, no `--cap` test `[V]` | `[V]` | CORE tests |
| TS-8 | `@live7` gateway test asserts only pairwise t2 != t2b, t3-1 != t3-2, t4-1 != t4-2, not all seven distinct; a duplicate model is accepted by tests | R2TT:37 | the cited lines `85-101` now hold the #518 ccsession-slot test; the pairwise asserts moved. Behaviour `[V]` by my 40-run-id re-run (26 duplicates) | `[V-base]` | CORE tests |
| TS-9 | Dropped-finding reporting is tested only as `assert res["warnings"]` (`test_review_ledger.py:384`); no test of merged-report text for a broken reviewer, warning content, or a valid-JSON-but-invalid line (claim 301) dropped while the reviewer's block still counts for clearing; the existing test `res = ldg.merge_round(led, new, 2, [rev("t1b-1"), _broken("t2-1")])` ends with `status(led)["L1"] == "resolved"` (`:380-385`): a round with one valid and one broken reviewer clears the `resolved_check` row, so the "clear despite a broken block" behaviour is pinned as expected by an existing test (whether intended is undecided; the `L:112` docstring says otherwise) | R2TT:40 | `[V]` (`:380-385`) | `[V]` | CORE tests (decide: bug or contract) |
| TS-10 | Telemetry tests are the only callers of `append_record`/`task_variables` in `src`+`tests` | R2CP:94 | `[V]` | `[V]` | |
| TS-11 | Prompt/skill tests: `test_review_prompt_overrides.py` lints briefs (no quotas, "assume defects remain", "apply all findings", any-severity FAIL); `test_review_severity_rule.py` pins S1-S5 severity rule across 10 files, 2-fix-cycle cap; `test_review_rules_text.py` pins insertion lines A/B/C and heading order Findings block < Fix map < Review panel < Never, no `src/superclaude` in the file; `test_review_brief_placement.py` pins that prompt text lives only in the rules file and the spec-panel gate is one sentence; `test_spec_panel_review_loop.py` 7 bullets in order | R2TT:20-27 | def counts `[V]`; content `[UNVERIFIED]` (not re-read) | | M-SP |

### 5.2 `tools/run-reviewer.sh` (E2 harness, tip, 88 lines, 8,089 B)

| ID | Fact | Note cite | Tip check | Status | Dest |
|---|---|---|---|---|---|
| RR-1 | Usage `run-reviewer.sh <EVAL abs> <pkg id> <reviewer_id> <model> [subdir]`; runs `claude -p --model $MODEL --output-format json --no-session-persistence --permission-mode bypassPermissions --disallowedTools Edit Write NotebookEdit` in `/tmp/evalsb/repo` under `timeout 3000`, brief on stdin; Bash is not disallowed | R1TT:6-7, R2TT:89 | `:2, 48` `[V]` | `[V]` | HARNESS |
| RR-2 | Hard-coded paths: `/tmp/evalsb/{repo,cand}`; `SRC_EVAL=/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md` (absolute worktree path); copies `source.md` next to the candidate, never removes a stale one; brief does not mention `source.md` | R1TT:6-7, R2TT:56, :88 | `:7-11, 13-17` `[V]` | `[V]` | HARNESS (must be parameterised) |
| RR-3 | Brief text (verbatim R2TT:96-100) = `/sc:spec-panel @CAND --mode critique` + RP first-review brief + "First-review rules (from `~/.claude/rules/prompts/document_review_loop_prompts.md`, read it first)": states anchor 12-200, categories, severities; does not state claim <= 300, refs <= 8, id pattern | R2TT:95-101, R1TT:7 | `:13-17` `[V]` (line 15, 17 text present) | `[V]` | M-SP brief; M-TL brief |
| RR-4 | Per attempt files `.attemptN.{json,md,err,meta.json}`; meta {reviewer_id, expected_model, observed_model, model_ok, findings_block, attempt, wall_s, output_tokens_main, output_tokens_all, exit}; OK = `MODEL_OK && BLOCK_OK && !APIERR`; `MODEL_OK` = observed non-empty, not `<synthetic>`, equals requested or `requested-build` (case-insensitive); `APIERR` = text contains "API Error" | R1TT:8, R2TT:90 | `:48-59` `[V]` | `[V]` | CORE (model-identity check is a real requirement: 2 misrouted runs per COMBO-REPORT audit A, `:295`) |
| RR-5 | `BLOCK_OK` is presence only: `grep -q '^```findings-v1'`, no parse or validation | R2TT:90, HO:26 | `:57` `[V]` | `[V]` | CORE bug (should call `parse_block`) |
| RR-6 | 2 attempts per model, no backoff | R2TT:91 | `:61-64` `[V]` | `[V]` | |
| RR-7 | Ladder `FALLBACK`: glm-5.3 to Qwen3.8-max to gpt-6-luna to muse-ember-1.0 to claude-haiku-5-5 to grok-4.7 to gpt-6.1-sol to glm-5.3 (cycle); muse-wonder-1.0 to muse-spark-1.3 to gpt-6.1-terra to gpt-6-luna; claude-sonnet-5-5, muse-wonder-full-1.0, claude-opus-5-5 to gpt-6.1-sol; `EXCLUDE_MODELS` default `glm-5.3 Qwen3.8-max` (skipped as fallback targets only; a primary in the list still runs); `VISITED` guard; `NOFALLBACK` disables; logs `FALLBACK a -> b` to `$RID.fallback.log` | R1TT:9, R2TT:92 | `:19-43, 65-83` `[V]` | `[V]` | CORE ladder (should come from tier file) |
| RR-8 | The ladder is a hand-kept map, not read from `review-tiers.default.json`; includes `muse-ember-1.0` which the tier file lacks | R2TT:93 | `:33-34` vs tiers JSON `[V]` | `[V]` | CORE: unify |
| RR-9 | Ladder never fires for an APIERR-only failure: entry condition is `! (MODEL_OK && BLOCK_OK) \|\| APIERR` (`:66`) but the loop condition is `! (MODEL_OK && BLOCK_OK)` (`:73`), so a result with right model and block but "API Error" text exits the ladder at once | R2TT:92 ("an APIERR result with model+block ok ends the ladder") | `:66, 73` `[V]` | `[V]` | CORE bug |
| RR-10 | Bugs: attempt counter resets per fallback model (`:76`) so fallback attempt files overwrite the primary's, `cost.json` undercounts and the primary's raw output is lost (only `fallback.log` remains); `expected_model` in meta is overwritten with the fallback model so identity checks cannot see a ladder swap; `$RID.md`/`.meta.json` = LAST attempt of LAST model even if it failed | R2TT:94, HO:26 | `:58, 76-79, 85` `[V]` | `[V]` | CORE bug |
| RR-11 | Variants kept: `.bad-launch` (4,302 B; brief as positional argv; unconditional `cp`; category `unpassable-ac`), `.unpassable-ac` (4,352 B; stdin brief + cmp-guarded copy; still `unpassable-ac`; no ladder, no APIERR, 2 attempts); parser accepts only `unpassable-check` so those lines were dropped; `SPEC.md:38-39` prescribes `*.catfix.md` sed copies | R1TT:6, R2TT:57-58 | sizes `[V]`; 20 `*catfix.md` files in tree `[V]` | `[V]` | EVID (DROP the variants once the parser warns) |
| RR-12 | `SPEC.md` 152 lines is an append-only ops log (procedure, hard limits, correction, batches 2-11, outage/contamination/cooldown/quarantine/ladder-v2), not a spec | R1TT:10, R2TT:84 | `git show` = 152 lines `[V]` | `[V]` | EVID |

### 5.3 Eval workspace `20261111-a1` inventory (tip)

| ID | Fact | Note cite | Tip check | Status | Dest |
|---|---|---|---|---|---|
| W-1 | `COMBO-REPORT.md` 83,296 B, 506 lines; "FINAL RESULTS AND DECISION (2026-11-13) - supersedes every earlier table" at line 289; DECISION UPDATE three-way at 375; Batch 11 decision update REJECTED at 421 | R2TT:45 | size/lines `[V]`; `:289` `[V]`; `:375` is "DECISION UPDATE (2026-11-13): sonnet + 2x luna vs ember + 2x luna vs sonnet + luna (+2x) ember" `[V]`; `:421` not re-read | `[V]` | EVID (master evidence) |
| W-2 | `PILOT-REPORT.md` 6,835 B; `manifest.md` 1,271 B | R2TT:46-47 | sizes `[V]` | `[V]` | EVID |
| W-3 | Three packages `TASK-WF-{design-20261108-041415, designSpec-20261107-075614, makeTheAliasOnly-20261105-051649}` with `candidate.md`, `ground-truth.json`, resolutions, `reviews/`; ground-truth sha256 designSpec `3e56551d...`, makeTheAliasOnly `79e32057...`, design `e3585b8e...` | R2TT:47-48 | tip file counts 2,020 / 2,125 / 2,090 (6,235 total); sha prefixes `[UNVERIFIED]` | partly `[V]` | EVID; benchmark inputs for M-TL |
| W-4 | `combos/` = "107 entries = SPEC.md + 106 row dirs"; "only 19 of 106 rows have a RESULT.md" | R2TT:50 | tip tracked tree: 97 entries (SPEC.md + 96 row dirs); 19 `RESULT.md` files `[V]` | count 107 `[CODE-CONTRADICTED]` for the tracked tree (97); 19 `[V]` | EVID |
| W-5 | Per-row content `<pkg>/{ledger.json, merge-stdout.txt, merged-1.md, resolution.json}` (checked on `g1-ember-luna2-r1`) | R2TT:50 | not re-checked | `[UNVERIFIED]` | EVID |
| W-6 | `quarantine-pre-src-luna/` (pre-source.md luna-era data) quarantined by owner order 2026-11-12 15:16 UTC; `probe/probe.json` (4,206 B); `arms/{A,B,C,scoring}` | R2TT:51-52, :49 | dirs `[V]` (quarantine dir, `probe`, `arms/A B C scoring`) | `[V]` | EVID |
| W-7 | `analysis/` scripts: `attrib.py`, `doubles.py`, `b8-table.py`, `b9-table.py`, `final-table.py`, `three-way.py`, `untried.py`, `allsets/`, `issue-table/`, launch/merge records `b7..b11`, `merge-b7..b11.sh`, audits A..F | R2TT:70-79 | listing matches `[V]` | `[V]` | HARNESS |
| W-8 | Audit purposes: A = model identity (890 runs), B = incomplete/short reports, C = era/input leakage, D = merge and ledger integrity (264 `merged-1.md`, all ledgers round 1 only), E = scoring sources/quarantine, F = aggregation/recompute | R2TT:79 | `summary.md` only in A and D `[V]`; counts `[UNVERIFIED]`. `COMBO-REPORT.md:290` says "Six independent read-only audits ... re-checked every valid-era run (71 rows, 213 row-packages)" `[V]` | partly `[V]` | EVID |
| W-9 | `tools/tmp-scripts/` 55 files (README says verbatim copies from `/tmp` made 2026-11-13; many hard-code `/tmp` and the `20261111-a1` dir); R1TT:11 counted `/tmp/*.sh` = 70 of which 12 exist in repo (analysis/) and 58 do not | R1TT:11, R2TT:59 | 55 `[V]`; "58 not copied" vs 55 committed `[UNVERIFIED]` (3 differ; `/tmp` state gone) | | HARNESS (DROP or archive) |
| W-10 | Blind scoring: `anon-*.sh` anonymise merged ledgers; `judge-one.sh` runs `claude -p --model claude-opus-5-5`, `bypassPermissions`, no tool restriction, reads GT + candidate + `merged-anon.md`, writes `score.json`; `gen-judge-list.sh` (39 judges); `run-combo-judges.sh` (4 at a time) | R2TT:65 | script names present in `tmp-scripts` (55) `[V]`; content `[UNVERIFIED]` | | HARNESS (judge protocol reusable for M-PR rf-qa benchmark) |
| W-11 | `startcombo*.sh` use `orca orchestration worker-start`; `r2-sonnet-driver.sh` and `r2terra-run.sh` send hard-coded Orca heartbeats with fixed terminal/task/dispatch ids | R2TT:64, :63 | `[UNVERIFIED]` content | | DROP |
| W-12 | E1 interplay: `snap.py` (writes `input-snapshot.yaml` into this worktree's `shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboD-r1/artifacts/`), `drift-b3.py`, `rlog-r3.sh`, `brief_c1.py` read E1's `shadow-model-combos` tree | R2TT:67, HO:25 | `[V]` (3.1 above: `snap.py:4`, `brief_c1.py:3`) | `[V]` | DROP (EVID only); flagged for E1 owner: do not run |

### 5.4 Git and tree state recorded by the notes

| ID | Fact | Note cite | Check | Status |
|---|---|---|---|---|
| GS-1 | Branch `ironbelly/eval-tasklist-review-panel` at `4a22d7421`, in sync with remote; no tracked modifications; 3 eval commits `b4db265a8` (2026-11-13 01:38 UTC, 8814 files, +314,276), `2d06a4382` (15:03, 445 files, +25,742), `4a22d7421` (15:55, 56 files, +1,374); whole branch diff 9313 files, +341,392 | R2TT:105-124 | the three commits exist; at tip the branch has 4 more commits (section 0); tree under `tasklist-review-panel/` = 10,226 files, of which 9,312 under `20261111-a1/` | commits `[V]` (not re-counted); counts moved after run 2 |
| GS-2 | `git diff --stat origin/master...HEAD -- src tests` EMPTY | R2TT:115 | `git diff --stat origin/master...<tip> -- src tests` empty `[V]` | `[V]` |
| GS-3 | "origin/master is 11 commits ahead of the branch base (d2d8a2d16 #519 ... 9e2608b03 #503); branch not rebased" | R2TT:121 | `git rev-list --count ec259f1b7..origin/master` = 11; log lists `d2d8a2d16`...`9e2608b03` `[V]` | `[V]` |
| GS-4 | Untracked 3041 files, ~1.5 GB, all under `20261111-a1/`, not gitignored; committed tree has 0 `attempt*.json`/`judge.json` | R2TT:125-129 | tip tree 0 such files `[V]`; untracked state `[UNVERIFIED]` | partly |
| GS-5 | CLAUDE.md rule ".dev/tasks/ is always staged" does not cover `.dev/eval-workspaces`; whether raw files should be committed is an owner decision | R2TT:137 | policy statement | `[V]` (project CLAUDE.md) |
| GS-6 | `manifest.md:5` "(local, never pushed)" is stale | R2TT:131 | `[V]` | `[V]` |
| GS-7 | After run 2: `6c0984326` untracks 96 raw transcripts "committed by mistake" (which earlier commit added them is not checked; the two commits before it, `fd69a006d` and `d561461fa`, are the candidates); the owner-decision question "commit raw transcripts?" (R2TT:137) is partly answered "no" for those 96 | commit log | commit message `[V]`; which commit added them `[UNVERIFIED]` |

## 6. Reviewer brief, roles, reflect-vs-panel (R1CP:48-77, R2CP:97-163, :187-195)

`RP` (74 lines), `SP`, `reflect-reviewer.md`, `confidence-calibrator.md`, `sc-tasklist-protocol/SKILL.md` are unchanged between `ec259f1b7` and HEAD (`git diff --numstat` empty); `sc-workflow-protocol/SKILL.md` (+31/-2, codegraph grounding) and `sc-reflect-protocol/SKILL.md` (+68) changed.

### 6.1 Reviewer brief (`RP`) and its consumers

| ID | Fact | Note cite | HEAD check | Status | Dest |
|---|---|---|---|---|---|
| BR-1 | Only reviewer brief in `src`: `RP` (74 lines), installed to `~/.claude/rules/prompts/`; only consumer is `/sc:spec-panel --mode critique`: `SP:266-268` hard gate ("read ... in full; if it cannot be read, return `incomplete`"); scope self-described at `RP:3` | R1CP:49, R2CP:99 | `SP:266-268` `[V]`; `RP:3` `[V-base]` | `[V]` | M-SP |
| BR-2 | Values to fill `RP:17-21`: `{{CANDIDATE}}`, `{{BASELINE}}`, `{{PRIOR}}`, `{{N}}`, `{{IDS}}`; no SOURCE/SPEC/ROADMAP placeholder | R1CP:51, R2CP:102, :114 | `RP:17-21` `[V]` | `[V]` | CORE brief contract (inputs by role) |
| BR-3 | First-review brief `RP:32`: reviews the candidate "against the requirements it states, review 1 of 3 ... Report concrete wrong outcomes, not a minimum number of findings ... If an input is missing or unreadable, return incomplete" | R1CP:50, R2CP:104 | `RP:32` `[V]` | `[V]` | M-SP; M-TL needs source-aware variant |
| BR-4 | Grading check `RP:31`: "An implementer who follows the stated text as written builds X, and X is wrong because Y."; blocking = two stated texts contradict, data loss / security / safety boundary, or an AC that cannot pass; Medium = needs a guess or "a requirement the document never states"; "A Medium finding goes under follow-up candidates even when its label is MAJOR" | R1CP:52, R2CP:103 | `RP:31` `[V]` | `[V]` | CORE rubric (spec-oriented wording: "implementer", "acceptance criterion") |
| BR-5 | Findings-block contract `RP:58-62`: last section `## Findings block`; fenced `findings-v1`; line `{"id","severity","blocking","category","anchor" 12..200,"anchor2","refs","claim"}`; prior lines for re-reviews; "blocking is true only for a finding that passes the grading check"; "The verdict line stays the reviewer's verdict" (but the merge ignores it) | R1CP:53, R2CP:108, :117 | `RP:58-62` `[V]` | `[V]` | CORE |
| BR-6 | Anchor guidance is only "12 to 200 characters copied exactly from the candidate: the text that is wrong; for a contradiction `anchor2` is the other side"; nothing on what to anchor for `missing-requirement`, uniqueness, whitespace/markdown, or what happens on a miss | R1CP:54, R2CP:115 | `RP:60` tail printed `[V]` | `[V]` | CORE brief |
| BR-7 | No severity definitions: CRITICAL/MAJOR/MINOR are an enum; `RP` defines only blocking vs Medium vs minor note; `SP:259` says "CRITICAL is blocking; a MAJOR or an FR-8/FR-9 finding is blocking only if it names a concrete wrong outcome"; code accepts CRITICAL + `blocking:false` and forbids only MINOR + blocking (`F:100-101`); "Medium" is not a severity value | R1CP:55, R2CP:116, R2CP defect 7 | `SP:259`, `F:100-101` `[V]` | `[V]` | CORE (one blocking rule, decided once; HO K10) |
| BR-8 | Report-ending conflict: `SP:260` ("last line is `verdict: PASS\|FAIL`") and `SP:263` (Reviser brief "just above the final verdict line") vs `RP:58` ("last section ... is `## Findings block`"); parser tolerates trailing text after the fence | R2CP:119, defect 14 | `SP:260, 263`, `RP:58` `[V]` | `[V]` | M-SP wording |
| BR-9 | Reviewers are not told the consequence of `blocking` (one blocking row from any single reviewer fails the round; the merge decides) nor the limits claim <= 300, refs <= 8, id <= 16, MINOR+blocking rejected; "MEDIUM" (the prompt's own grading word) is rejected as a severity | R2CP:117, R2CM:43, D9 | `RP:60` vs `F:90-121` `[V]` | `[V]` | CORE brief generated from the parser limits |
| BR-10 | Not in the brief: panel/tier/model identity; persona/lens; coverage target; output path; named sha256 placeholder; no statement that reviewers get no source; "run `diff`/`grep` only when commands can be run" (`RP:46`); no tasklist-specific rubric (task-ID/traceability/AC/dependency checks) | R1CP:60, R2CP:118 | `[V-base]` | `[V]` | M-TL brief |
| BR-11 | Re-review brief `RP:48` (evidence block `diff -w BASELINE CANDIDATE`, prior status, "Record a severe defect you newly discover even if it is older"); REVISE brief `RP:53`; fixmap contract `RP:66`; "Never" list `RP:72-74` (no "any finding is FAIL", "assume defects remain", quotas, "apply all findings") | R1CP:57-59, R2CP:105-111 | `RP:66, 68-74` `[V]` | `[V]` | CORE/M-SP |
| BR-12 | Review panel paragraph `RP:68-70`: run reviewers printed by `superclaude review panel resolve --run-id <loop id> --kind first\|re-review`, each fresh context, same brief, no cross-visibility; merge with `superclaude review merge` (also for one reviewer); `ledger revise` after each revision; "Only these scripts change a finding's status"; if `superclaude` is not installed run one reviewer and say so | R1CP:61, R2CP:110 | `RP:68-70` `[V]` | `[V]` | CORE |
| BR-13 | `SP:256-268` Review Loop: 7 bullets (mode, grading, verdict, cap, re-review output, reviser contract, precedence); cap "at most 2 fix cycles (3 reviews)"; generic copies of the cap sentence in `rf-qa.md`, `rf-qa-qualitative.md`, `rules/prompts/*_qa_prompt.md` (4 files), `output-styles/pragmatic.md:227` (and MDTM templates per R2CP:195) are text only and call no script | R1CP:100, R1CP:8, R2CP:195 | grep at HEAD: the cap sentence ("at most 2 fix cycles") is in 8 files: `documentation_expert_qa_prompt.md`, `automated_qa_workflow_qa_prompt.md`, `doc_code_analyst_qa_prompt.md`, `recruiting_expert_qa_prompt.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `spec-panel.md`, `pragmatic.md:227` `[V]`; R1CP:8's cite `skill_template.md:830` and R2CP:195's MDTM template cites `01_...:646`, `02_...:657` not re-checked `[UNVERIFIED]` | partly `[V]` | M-PR (rf-qa replacement reuses the cap rule) |
| BR-14 | `sc-cli-eval-protocol/SKILL.md:85` "Do not reimplement a review panel" | R1CP:8 | `[V]` (`:85` "Fold the panel's findings back into the spec. Do not reimplement a review panel.") | `[V]` | CORE (consumer, not owner) |

### 6.2 Roles (R2CP:121-141, R1CP:63-70)

| Role | Driver and data contract | Status |
|---|---|---|
| Orchestrator/coordinator | main session following `SP:256-268` plus `RP:68-70`; keeps review count, prior-findings file, saved copy (`SP:261`) | `[V]` |
| Panel resolver | `superclaude review panel resolve` (`PC` to `P`), output `review-panel-resolution/1` | `[V]` |
| Reviewer | `RP:31-33` (first), `:37-49` (re-review); agent type NOT specified ("fresh context", `RP:70`); no read-only agent for this panel (reviewers are generic sessions; prompt only says "Do not edit the candidate") vs reflect's `reflect-reviewer` with a read-only tool allowlist | `[V]` |
| Calibrator | NONE in this loop; `confidence` single/overlap computed (`L:86-90`), printed in the ledger table (`L:433-437`), unused | `[V]` |
| Merge/judge | deterministic script `superclaude review merge` (no LLM judge); verdict from reviewer `blocking` flags only | `[V]` |
| Reviser | `RP:53` + `REVISER_RULES` (`L:22-26`) restated in the merged report; returns `fixmap-v1` | `[V]` |
| Revision recorder | `superclaude review ledger revise` (`LC:36-71` to `L:301-347`) | `[V]` |
| Human | escalation at review 3 (`RP:13`; merged report `## Escalation`); `ledger defer` (`LC:74-91`, `L:350-360`); follow-up-issue question (`SP:260`) | `[V]` |
| Telemetry writer | NONE in product | `[V]` |
| Data contracts | findings-v1 (reviewer to merge), fixmap-v1 (reviser to revise), `review-ledger/1`, merged report text (ends `verdict: PASS\|FAIL`), `review-panel-resolution/1` (merge reads only reviewer_id/model), `review-capture/1`, `review-telemetry/1` | `[V]` |
| Exit codes | `ledger verdict`: 0 PASS, 10 REVISE, 11 ESCALATE | `[V]` |

### 6.3 Reflect Tier 2 versus the review panel (notes) and what HEAD changes

| ID | Aspect | Notes (base) | HEAD status |
|---|---|---|---|
| RV-1 | Purpose | reflect: UC-1 pre-execution coverage of a tasklist vs its spec, UC-2 post-execution deviation audit (R2CP:147); panel: document critique loop for `/sc:spec-panel` | `[V]` |
| RV-2 | Reviewer agent | all reviewers spawn as fixed read-only `reflect-reviewer` (frontmatter `model: sonnet`, tools allowlist, `maxTurns 50`, `permissionMode plan`) | `[V]`: `SKILL.md:646` "All reviewers are spawned as the fixed read-only `reflect-reviewer` agent-type"; `reflect-reviewer.md:5-8` |
| RV-3 | Count and rotation | `--reviewers N` 2-3, default 3 (`SKILL.md:86`); rotation sonnet / haiku / (qwen\|kimi\|deepseek else opus), personas analyzer/qa/refactorer; executor-class exclusion; alias count from three `ANTHROPIC_DEFAULT_*_MODEL` vars | `[V]` at `SKILL.md:86, 127, 232, 652-657` (moved +44); HEAD adds `D5. N_eff = min(--reviewers, alias count, 3); the anchor ... is never dropped` (`SKILL.md:321`) |
| RV-4 | Model registry | three independent registries: skill (`ANTHROPIC_DEFAULT_*`), CLI (`T2Model0N`/`T1Model0N`, `cli/reflect/ensemble.py:7, 154-198`), panel (tier JSON) | `[CODE-CONTRADICTED]` as to the skill: shadow mode resolves through the panel (`SKILL.md:340`: `superclaude review panel resolve --template @reflect-pre --run-id <id> --kind first --env anthropic-only --hard-exclude-class <executor class> --strict-distinct`), maps model ids to classes through the tier file's `classes`, records `panel_parity`; default `--t2-engine legacy` never calls the panel (`SKILL.md:87, 311`); `panel` is rejected "ships in Stage 3" |
| RV-5 | Finding format | reflect: markdown Deviations table (#, Category, Location, What diverged, Evidence file:line, Severity HIGH/MEDIUM/LOW; `reflect-reviewer.md:71-99`) + advisory Correctness gaps (`:101-115`); panel: findings-v1 JSON lines with text anchors | `[V]` for legacy. HEAD adds `findings_v2.py`: container `findings-v2`, `V1_FIELDS` = id, severity, blocking, category, anchor, anchor2, refs, claim; plus `lens` in (spec, reflect-pre, reflect-post), `channel` in (defect, grounding-gap, advisory), `deviation_class` in (authorized, necessary, drift, regression, none), `reflect_category`, `citations` (role plan/spec/source/test/diff/artifact + repo path + line_start/line_end + optional quote), `coverage_rows`, `self_confidence`; shadow-mode briefs append one instruction line (`reviewer-spec.md:39`) |
| RV-6 | Grounding unit | reflect: `file:line` citation; panel: exact text anchor quote | `[V]`; v2 supports both: citations with optional `quote`, `anchor` (`findings_v2.py:80,126-136`) |
| RV-7 | Brief | reflect: per-reviewer file `<output>/reviewer-briefs/reviewer-<N>.md`, exactly 3 sections (T1 card excerpt, Grounding hunks, Coverage slice; `SKILL.md:303`; `reviewer-spec.md:21-74`); D13 UC-1: spec body injected for the qa persona (`reviewer-spec.md:55`); panel: same text for all reviewers | `[V]`; HEAD: first entry of `## Grounding hunks` carries codegraph run state (`SKILL.md:303`) |
| RV-8 | Calibration | reflect: blind `confidence-calibrator` per card with disjoint-set class rule (`SKILL.md:1172-1192`; `reflection-rubric.md:9-13` 5-dim arithmetic mean); panel: none | `[V-base]` (disjoint rule at `SKILL.md:159, 319`; 5-dim mean `reflection-rubric.md:9-13` read); shadow adds a per-finding `calibration: per_finding` yaml block (`SKILL.md:344`) |
| RV-9 | Merge | reflect: `sc-adversarial-protocol` Mode A, judge class owned by sc-adversarial, `merge_method` in {adversarial, single-reviewer-fallback} (`SKILL.md:356`), evidence-validator gate; panel: deterministic clustering + any-blocking | `[V-base]`; HEAD shadow: panel clustering (`cluster_v2`) runs beside the legacy debate, writes under `<output>/panel/`, changes no verdict or stable contract field (`SKILL.md:338`) |
| RV-10 | Final gate | reflect: evidence-validator re-Reads every citation; panel: none (anchor found/missing recorded, not gated) | `[V]`; HEAD adds `verify_cmd.py` (`tests/review/test_review_verify_citations.py`) |
| RV-11 | Loop | reflect: no fix loop, Tier 3 remediation opt-in (plan route sc:workflow, task-builder with `--depth deep`; `SKILL.md:90, 165, 367`); panel: review, revise, re-review, cap 3 | `[V]` |
| RV-12 | `confidence-calibrator.md` is troubleshoot-shaped: description names `sc:troubleshoot` (`:3`), triggers `:15`, 6-dim rubric `:61`, gated-min formula `:67`, `rubric_path refs/escalation-rubric.md` `:48`; reflect expects the 5-dim mean | R2CP:161, defect 9 | `[V]` |
| RV-13 | `reflect-reviewer` is UC-2-shaped (`:3, :15`; output = UC-2 deviation taxonomy) yet `SKILL.md` spawns it for every Tier-2 mode incl. UC-1; UC-1 (what sc-tasklist Stage 10.5 and sc-workflow Wave 4 use) has no matching finding format | R2CP:162, defect 10 | `[V-base]`; HEAD answer is findings-v2 `lens: reflect-pre` (shadow, UC-1 only) |
| RV-14 | `sc-tasklist-protocol/SKILL.md:1640` says reflect "offers a Tier-3 `task-builder` remediation", but reflect's default Tier-3 route is `sc:workflow` and task-builder only with `--depth deep` | R2CP:183 (defect 17) | `[V]`: tasklist text at `:1640` (in Stage 10.5), reflect `SKILL.md:90, 165, 367` |
| RV-15 | How the non-Claude rotation classes (qwen/kimi/deepseek) run as the `reflect-reviewer` agent (pinned `model: sonnet`) is not shown in the skill text | R2CP:163 | `[UNVERIFIED]` |

### 6.4 Run 2's open questions Q1-Q3 answered against HEAD (for the final report)

| Q | Question (HO:39, run 2 report Q1-Q3) | Answer at HEAD |
|---|---|---|
| Q1 | Does master's `findings_v2.py` still drop whole findings, and replace findings-v1 for spec-panel or run beside it? | It runs beside v1: `findings.py` is unchanged and `ledger.py`/`merge_cmd.py` still import v1 (`LC:10-11`, `merge_cmd.py`); `findings_v2.parse_block` (`findings_v2.py:215-303`) `continue`s past a failing line (`:266,273,278,283,287`), i.e. it still drops whole lines, with the same 12-200 anchor/anchor2 and 300 claim limits (`:111, 126, 132, 136`); the v1-valid subset passes unchanged (`:3`); `calibrated_confidence` in a line is rejected (`:4`). Nothing in v2 repairs or truncates |
| Q2 | Does master's `cluster.py` replace `findings.cluster`, and does it chain or split on refs? | It does not replace it: `ledger.merge_round` still calls `fnd.cluster` (`L:165`). `cluster.py` adds `cluster_v2` (`:381`) over findings-v2 records: union-find, `same_defect_v2` (deviation class compatible; refs intersect or both empty, citations on the same path within 3 lines; or equal fingerprints with non-empty refs), and it FLAGS chained clusters (`chained` when two members do not match pairwise, `cluster.py:33, 324, 370`) and excludes them from the support mean (`:404`) rather than preventing them |
| Q3 | Do `hard_exclude`/`strict_distinct` remove silent duplicates and keep excluded models out? | Only when passed: `resolve_slot` (`P:500-555`) raises `ExclusionExhausted` instead of `pool = candidates` when `hard` is non-empty (`:539-543`); `panel resolve` takes `--hard-exclude-class` / `--strict-distinct` (`PC:73, 101-102`). Without them (default path) duplicates still occur: `@default`/`@live7` gateway re-run at HEAD gives t3-1 and t3-2 both Qwen3.8-max; 26 of 40 `@live7` run ids contain a duplicate. Exclusion is class-based (`classes` map) not a per-model data flag; `Qwen3.8-max` and `glm-5.3` remain in tier2/2b/3 lists |

## 7. Value inventory roll-up (output (b)): every item in this slice mapped to a destination

IDs refer to the tables above. Source column says where the item comes from when it is not one of the six notes or HO.

### 7.1 Study findings and numbers (E2 evidence; reached through HO and `COMBO-REPORT.md`)

| ID | Item | Source | Dest | Caveat |
|---|---|---|---|---|
| V-1 | Ceiling: about 2-2.5 of 14 defects for every panel; five defects no valid row ever caught (designSpec GT1, GT2, GT10, alias GT4, alias GT3 in 1 row) point at the brief, the packages or the ground truth, not the model mix | HO:55; `COMBO-REPORT.md:286-287` | EVID; input to M-TL brief design | 3 plan packages, n=4-6 per panel (run 2 report K3) |
| V-2 | Panel guidance: default ember + 2x luna (1.83/14 found, 0.17/8 real blocking, 1.83 wrong blockers, control 0.83/2, 63,644 tokens, 348 s); sonnet + 2x luna optional quality tier; haiku + 2x luna best real blocking | HO:56; `COMBO-REPORT.md:331, 366, 378` | CORE data (named panel templates for M-TL) + EVID | ember is missing from tier data (E-12); plan-review only (K3) |
| V-3 | 49 blocking findings lost to the 200/300 limits, 4 verdict flips FAIL to PASS (80 reviewer-level cases; by model luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet/terra/sol 0) | `COMBO-REPORT.md:292` | CORE requirement: repair or loudly reject, never silently drop; regression benchmark | the largest measured loss |
| V-4 | Source-blind reviews: 156 of 665 valid-era runs never referenced `source.md` (ember 81/209, luna 49/222, wonder 6/25, haiku 15/75, grok 4/24, sonnet 1/63, terra 0/44, sol 0/3); cause "the brief never names source.md" is an inference, UNVERIFIED | `COMBO-REPORT.md:373` (pre-skip 161 at `:293`) | CORE brief contract (inputs by role) | HO:58 states the cause as fact (see 1.3 H18) |
| V-5 | One reviewer's `blocking` flag decides the verdict; no calibrator; wrong blockers 1.8-4.75 per row (run 2 report D8) | HO:59; `L:187, 273-274` | CORE merge-policy plug point (quorum / calibrated support, E1 `cluster_v2` support value) | |
| V-6 | Judge-counted blocking is not real blocking: over 71 rows the judge counts 65 "blocking" catches but only 38 are real blocking defects; tables must show both | `COMBO-REPORT.md:291` | HARNESS metric definition; CORE telemetry `truth_basis` | |
| V-7 | Terra/sol refusals: 51 reports say incomplete; 16 empty terra reviews in valid-era rows; luna anchor fidelity 91.4% verbatim vs 98-100% others | `COMBO-REPORT.md:294` | CORE: incomplete-report handling, model-health data, anchor repair | |
| V-8 | Model identity: 2 `b4-muse-luna2` t2b-1 "wonder" runs were served terra (quarantined); grok reports `grok-4.7-build` (benign) | `COMBO-REPORT.md:295` | CORE observed-model check (RR-4) | |
| V-9 | Surviving statistics only: second luna +0.83 found (Welch p 0.004, permutation 0.048); 2x luna + 2x ember 2.75-3.25 more wrong blockers (p 0.005-0.03); ember + terra -1.75 found (p 0.029); all else within noise | `COMBO-REPORT.md:298` | EVID | |
| V-10 | Retractions: n2-sonnet-src "8/14, 5/8" (corrupted judge), "second run of same model adds nothing", "haiku overlap 8 of 8", "ember weaker than wonder" unqualified, r2 as a muse row, pre-source luna/terra/sol rows, 4/8 and 3/8 blocking claims | `COMBO-REPORT.md:297`; HO:33 | DROP (never reuse) | |
| V-11 | Pilot decision rule: only arm C passes, by one defect; efficiency figure in run 2 R12 | HO:48 | EVID | PILOT-REPORT not read |
| V-12 | Never-run models (muse-spark, muse-wonder-full): at most a one-run smoke test; ember + terra worst row (0.5/14) | `COMBO-REPORT.md:286` | EVID; data hint | |
| V-13 | Testing closed by owner order 2026-11-13; batch 10 (grok+sonnet, haiku+sonnet) dropped and excluded | `COMBO-REPORT.md:290` | EVID (constraint: no new combos) | |

### 7.2 Code defects and gaps (each needs a decision: fix in CORE, fix in a module, or accept)

| ID | Item | Tables | Dest |
|---|---|---|---|
| V-20 | Silent drop of whole findings for limits (anchor/anchor2 > 200, claim > 300, refs > 8, id > 16, MINOR+blocking, bad category/severity/bool) with one first-error warning, nothing persisted | G1-G3, F10, G8 | CORE |
| V-21 | Partial-panel failure invisible: merge refuses only if NO reviewer ok; N-reviewer panel can PASS on a truncated panel; single-reviewer refuses | G5, G6 | CORE |
| V-22 | Clearing ignores `block_ok`; docstring `L:112` false; test pins the behaviour | G7, L9, TS-9 | CORE |
| V-23 | Missing-anchor rows kept, never refound, never `resolved_check`, forced ESCALATE; `anchor_status`/`anchor_ambiguous` unused | F15, F16, L21 | CORE |
| V-24 | Ref-token scraping: free-text tokens ("UTF-8", "ISO-8601", "CVE-2024") split one defect; case-sensitive token; ids without hyphen (`T01.02`) lost; mismatch blocks span merging | F17, R-1..R-4 | CORE (profile-configurable id grammar) |
| V-25 | Over-merge: 3-line tolerance + transitive union-find chain distinct adjacent defects; same-reviewer findings merge; row keeps first member's claim/anchor; a cluster matches only the first existing row | F19, L5-L7 | CORE (E1 `cluster_v2` flags chaining; v1 path unchanged) |
| V-26 | Refound row takes current round's blocking call; re-review panel = one anchor reviewer, so one re-reviewer can downgrade a blocker the full panel raised | L7, L8 | CORE (re-review quorum) |
| V-27 | `ledger revise` runs twice and remaps spans twice; new-text hash not stored; `fixmap_ok` not enforced; fix-map rows for non-open rows skipped silently; table fallback treats any "applied" cell as applied | L16, F20 | CORE |
| V-28 | `defer` rewrites last verdict to PASS, no precondition, no undefer, no audit of who | L17 | CORE |
| V-29 | `--cap` ignored on existing ledger; `--round` unbounded; rounds past cap keep merging; `doc` path stored as given | L1, L4 | CORE |
| V-30 | `merge` exits 0 always; only `ledger verdict` maps to 0/10/11; non-atomic `--out`/capture writes; no ledger lock; report written before ledger saved | L13, L14, L19 | CORE (CI/PR use) |
| V-31 | Line-model mismatch (`\n` vs `splitlines`); two-token fence not found; quoted example block + real block triggers "more than one block"; heading error names `## Findings block` only | F5, F6, F8, F21 | CORE |
| V-32 | Brief vs parser: limits not in brief; "MEDIUM" rejected; `missing-requirement` Medium by instruction but blockable by schema; CRITICAL non-blocking accepted vs `SP:259`; report-ending conflict; reviewers not told consequence of `blocking` | BR-6..BR-10, G9 | CORE (brief generated from parser constants), M-SP wording |
| V-33 | `distinct_across_slots` silently duplicates (default path); fixed slot ignores exclusion; `round_robin` date-dependent; `@name` precedence silently overridden by project/user files; gateway `launch` empty; `T2bModel01` unread; env keyed on one variable | E-1..E-8, P-5 | CORE |
| V-34 | Tier data gaps: no muse-ember-1.0; excluded models still listed; `claude-fable-5-1` in no tier list; ladder is a second hand-kept map | E-10, E-12, E-13, RR-8 | CORE data |
| V-35 | Telemetry: unwired (no product caller), `model.observed` has no producer, strata hard-coded sonnet/haiku, `doc_format` fixed markdown, id regex spec-shaped | Y-4, Y-7..Y-9 | CORE |
| V-36 | `lint_cmd`/`estimate_cmd` registered but absent; `ModuleNotFoundError` swallowed (HEAD list also registers `cluster_cmd`, `verify_cmd`, `manifest_cmd`, which exist) | H15, K-2 | CORE housekeeping (drop the two names or implement) |
| V-37 | Harness bugs: `expected_model` overwritten on fallback; attempt files overwritten across fallback models; `cost.json` undercounts; `BLOCK_OK` is a fence grep; APIERR-only failure never falls back; no backoff; Bash not disallowed | RR-5, RR-9, RR-10, RR-1 | HARNESS (fix or replace by CORE launch adapters) |
| V-38 | Untested: exact limits, 4 of 6 categories in the parser, malformed/missing resolution, duplicate reviewer id, rounds past cap, `--cap`, merged-report text for a broken reviewer, all-seven-distinct gateway check; multi-round paths never exercised with real panels (run 2 report K4) | TS-6..TS-9 | CORE tests |
| V-39 | Reflect-side mismatches: `confidence-calibrator` is troubleshoot-shaped (6-dim gated-min) vs reflect 5-dim mean; `reflect-reviewer` UC-2-shaped but spawned for all modes; tasklist Stage 10.5 text vs reflect Tier 3 default route; three model registries (partly closed in shadow mode) | RV-4, RV-12..RV-14 | M-RF / CORE calibrator |

### 7.3 Strategies, decisions and constraints recorded (made vs open)

| ID | Decision or constraint | Source | Status |
|---|---|---|---|
| V-50 | Strata never pooled; every telemetry record may carry a stratum tag (owner decision D3) | `T:111-115` | made |
| V-51 | anthropic-only: Haiku 5.5 stands in for tier 2/2b/3 (owner 2026-11-10); tier 1b resolves to Sonnet 5.5 | `review-tiers.default.json` note | made |
| V-52 | Tier 2b = review-panel and fallback tier; 429 policy (owner 2026-11-12, rewritten by #518) | `MODEL-TIERS.md:44` | made; R1CP:36 quote stale |
| V-53 | Fallback ladder = next model in the same tier, then head of the next tier (owner order 2026-11-12 18:10 UTC); ember "being added as Tier 04 Model 02" | tip `run-reviewer.sh:24-30` | made in the harness; not in tier data |
| V-54 | Quarantine pre-source.md luna-era data (owner order 2026-11-12 15:16 UTC) | `COMBO-REPORT`, R2TT:51 | made |
| V-55 | Raw transcripts not committed (1.48 GB, 2,916 files per note); 96 more untracked at tip | RAW note; `6c0984326` | partly decided |
| V-56 | Reflect Tier 2: default `--t2-engine legacy`; `shadow` measures only; `panel` ships in Stage 3; Fable and Tier 0 never picked; executor class excluded | `SKILL.md:87, 311, 338-344` | made (E1) |
| V-57 | Which blocking rule is canonical (`SP:259` vs `RP:31` vs `F:100` vs findings-v2 `reflect_category` rule `findings_v2.py:162`) | run 2 report B-3, K10 | OPEN |
| V-58 | Whether the unified panel replaces reflect UC-1's advisory review or runs beside it (requirement U11, decision DO4 of run 2 report) | HO:23 | OPEN |
| V-59 | Whether to adopt reflect's findings_v2 limits as-is (carries D1 loss: K2) | run 2 report K2 | OPEN |
| V-60 | Commit or delete the 3 foreign scripts; deletion waits for the owner | HO:67 | OPEN |
| V-61 | Panel dispatch: raw gateway model ids via `claude -p --model <id>` (study path) vs tier alias strings (product path; alias serves only the first model of a tier, `manifest.md` per R2TT:47) | R2TT:47, :57 | OPEN |

### 7.4 Scripts, tests, artifacts (what to keep)

| ID | Item | Dest |
|---|---|---|
| V-70 | `tools/run-reviewer.sh` (identity check, attempt metadata, ladder idea, `NOFALLBACK`) | HARNESS; port the ideas (identity check, per-attempt files, cost) into CORE launch adapters; DROP the shell file after |
| V-71 | `.bad-launch`, `.unpassable-ac` variants, `*.catfix.md` copies (20) | EVID / DROP |
| V-72 | `analysis/*.py` (`attrib`, `doubles`, `b8/b9-table`, `final-table`, `three-way`, `untried`, `allsets`, `issue-table`), `analysis/audits/audit-A..F` | HARNESS (benchmark regeneration needs them to stop reading `/tmp`, see 1.2 row 7) |
| V-73 | `tools/tmp-scripts/` 55 files (judge, anonymise, batch launchers, per-row drivers, orca heartbeats) | HARNESS: keep `judge-one.sh` protocol, `anon-*.sh` idea; DROP per-row drivers, `startcombo*`, hard-coded Orca heartbeat scripts |
| V-74 | `snap.py`, `drift-b3.py`, `rlog-r3.sh`, `brief_c1.py` (E1's eval) | DROP from E2 folder; `snap.py` must not run (writes into E1 evidence) |
| V-75 | `combos/SPEC.md` (152-line ops log), `COMBO-REPORT.md` (506 lines), `PILOT-REPORT.md`, `manifest.md`, `probe/probe.json`, `quarantine-pre-src-luna/`, 3 package dirs with ground truth | EVID (ground truth + candidates = regression benchmark inputs for M-TL) |
| V-76 | `tests/review/test_review_{cli,findings,ledger,panel,panel_live7,rules_text,telemetry}.py` (116 tests at HEAD) and `tests/skills/test_review_*` + `test_spec_panel_review_loop.py` (68) | CORE tests (keep, extend per V-38) |
| V-77 | Notes: R1CM, R1CP (code reading) and R2CM, R2CP, R2TT (code reading, defect lists) | EVID; their per-claim line cites remain exact for findings/ledger/merge/telemetry at HEAD, stale for panel/panel_cmd/reflect SKILL |
| V-78 | HO itself: verdict, section 4 "keep from run 1", recommended action | EVID; section 4 items map to V-36, E3 variants (H16), model-by-role table (E-11 plus V-2), pilot rule (V-11), missing-requirement conflict (G9) |

## 8. Overlap-matrix inputs (output (a)): what each program has, as seen from this slice

Cell = evidence; "-" = nothing seen. E2 column comes from the notes (base `ec259f1b7` product code plus the study harness); E1 column from HEAD checks; E3 from the notes' references to experiment copies (relation to `cli/review` UNVERIFIED, R2CP:185).

| Capability | E1 (reflect panel kernel, HEAD) | E2 (tasklist study, notes) | E3 (#346 loop + installed variants) |
|---|---|---|---|
| Finding schema | findings-v2 superset of v1: lens spec/reflect-pre/reflect-post, channel, deviation_class, reflect_category, citations (path + lines + optional quote), self_confidence (`findings_v2.py:25-60, 84-190`) | findings-v1 text anchors; limits 12-200 / 300 / 8 / 16 | findings-v1 (master `cli/review`); variants add `finding-grader` (stoprule) outside src |
| Anchor/limit policy | same 12-200 / 300 limits, drops whole lines (`findings_v2.py:266-287`) | measured loss: 49 blocking, 4 flips | brief states 200 limit only |
| Clustering | `cluster_v2`, flags chained clusters, support values, `cluster_agreement` telemetry | v1 `cluster` (union-find, 3-line tolerance) used by ledger | v1 |
| Ledger and loop (verdict, revise, defer, cap) | unchanged `ledger.py`; reflect uses no ledger (no fix loop) | full state machine; round 1 only in the study (K4) | `sc-review-ledger`/`review_ledger.py` variant, `spec-panel-ledger` command (outside src) |
| Verdict policy | shadow only, no verdict change; legacy debate authoritative | any-blocking | any-blocking; `stoprule` variant computes verdict from a sealed claim ledger |
| Panel templates and resolution | `reflect-pre`, `-pre-x2`, `-post`, `-post-x2`, `-lite`, `-enterprise` + `default`, `live7`; `classes`, `--hard-exclude-class`, `--strict-distinct`, `ExclusionExhausted` | uses `@live7` via resolution files, but dispatches raw model ids outside the product | `@live7`, tier 2b (#498); ccsession slot tests (#518) |
| Model registry | tier JSON with `classes`; reflect skill still has alias rotation (legacy) | hand-kept ladder in `run-reviewer.sh`, ember added | `ccsession-models.json` slots (T2b/T3/T4), MODEL-TIERS.md |
| Launch/dispatch | gateway `launch {}` (null); anthropic-only launch map; reflect spawns agents | `claude -p --model <raw id>` with identity check | - |
| Calibration | blind `confidence-calibrator`, plus per-finding `calibration` block in shadow | none | `finding-grader` (stoprule) |
| Evidence/citation verification | `verify_cmd.py`, evidence-validator gate | judge against ground truth (benchmark, not product) | - |
| Telemetry | `review-telemetry/1` + `manifest` + panel fields under contract `telemetry:` | defined, unwired; study used its own scoring | - |
| Benchmark/ground truth | `.dev/eval-workspaces/shadow-model-combos`: 1 input package (`TASK-WF-designSpec-20261107-075614`, the SAME package as one of E2's three), 5 combos A-E x 3 repeats = 15 run dirs under `runs/` `[V]` (`ls`) | 3 packages, ~71 valid-era rows, blind judge, 6 audits | `.dev/experiments/346-validation` |
| Brief | `refs/reviewer-spec.md` 3 sections + findings-v2 line in shadow | `RP` first-review brief + harness brief | `RP` |
| Integration point | `sc:reflect` Tier 2 (UC-1 shadow, UC-2 later), `sc-tasklist` Stage 10.5, `sc-workflow` Wave 4 | none in src (study only) | `/sc:spec-panel` Review Loop |
| Document types | tasklist/plan (UC-1), code diff (UC-2) | tasklist/plan | spec/markdown |

## 9. Conflict log (output (c)), items raised by this slice

| ID | Conflict | Parties | Evidence | Resolution input |
|---|---|---|---|---|
| C-S1 | Anchor-as-text (findings-v1, E2/E3) vs citation-as-path:lines (findings-v2, E1); v2 keeps the same 12-200/300 limits and still drops whole lines | E1 vs E2/E3 | 6.4 Q1; `findings_v2.py:111,126-136,266-287` | one schema; repair instead of drop (V-3) |
| C-S2 | E2's folder holds a script that writes into E1's evidence tree (`snap.py:4`) and three more that read it; HO:67 treats removal as an E2 owner question | E1 vs E2 | 1.2 row 4, W-12 | do not run `snap.py`; ask E2 owner to remove |
| C-S3 | Blocking rule defined four ways: `SP:259` (CRITICAL is blocking), `RP:31` (grading sentence), `F:100` (only MINOR+blocking rejected), findings-v2 `reflect_category` rule (MAJOR/CRITICAL must be blocking, MINOR must not, `findings_v2.py:162`); reflect legacy uses HIGH/MEDIUM/LOW with no blocking flag | E1, E2, E3 | BR-7, RV-5 | decide once (V-57) |
| C-S4 | Merge policy: deterministic any-blocking (panel) vs adversarial debate + calibration + evidence gate (reflect legacy) vs both side by side (shadow) | E1 vs E2/E3 | L12, RV-9 | pluggable verdict policy |
| C-S5 | Three model registries: reflect skill aliases, reflect CLI `T2Model0N`, panel tier JSON, plus E2's ladder map; shadow mode now resolves through the panel but the CLI still uses `T2Model0N` | E1, E2 | RV-4, RR-8, E-14 | single registry with classes |
| C-S6 | Launch restriction: reflect profile validation allows launch only for `sonnet`/`opus`/`haiku` (`P:72` `_REFLECT_LAUNCH`) and max 3 reviewers (`P:73`), while E2's best panels need gateway models (ember, luna, terra, glm) with no launcher | E1 vs E2 | `P:71-73` (constants read; rules of `validate_reflect_profile` not read) | launch adapters for gateway models |
| C-S7 | Tasklist review today is reflect UC-1: advisory, bundle ships regardless (`sc-tasklist-protocol/SKILL.md:1619-1646`, Wave 4 `sc-workflow-protocol/SKILL.md:85-89`); the panel's verdict is FAIL/ESCALATE and drives a revise loop | E2 vs E1/E3 | X1, 1.2 row 2 | requirement U11 / DO4 (V-58) |
| C-S8 | Input contract: reflect briefs carry the spec/source (qa persona gets the spec body, `reviewer-spec.md:55`); panel brief names only the candidate; harness ships `source.md` beside the candidate but the brief never mentions it | E1 vs E2/E3 | BR-2, RR-2, RV-7 | M-TL brief with named inputs |
| C-S9 | Ledger implementations: `cli/review/ledger.py` vs installed `sc-review-ledger` skill (`review_ledger.py`, E3 variant); relation unverified | E1/E2 vs E3 | H16, R2CP:185 | read the variant before merging designs |
| C-S10 | Strata `sonnet`/`haiku` in `review-telemetry/1` vs gateway-model panels vs reflect telemetry fields under the contract | E1/E2 | Y-4, Y-10 | generalise strata to classes (tier file `classes`) |
| C-S11 | Report ending: `SP:260/263` vs `RP:58` | E3 | BR-8 | one wording |
| C-S12 | `sc-tasklist-protocol/SKILL.md:1640` (Tier-3 task-builder) vs reflect default route (plan route) | E1 | RV-14 | text fix in tasklist skill |
| C-S13 | HO recommends run 2 as the main hand-off but run 2 notes carry errors: "159 functions" (TS-2), "T2bModel01 not referenced in src/tests" (X2), "107 combos entries" (W-4); and HO cites report numbers that differ from the notes' own D-numbers (2.4); HO:16 says "four facts" for eight rows; HO:16 "each claim checked" vs rows 5-7 "not re-checked" | E2 internal | 1.1, 1.2, 2.1, 2.4 | cite file:line, not D-numbers |
| C-S14 | HO row 1 attributes the 40-file / +8,026 findings to run 2, but R2CP:121 says #519 was "not inspected"; and "line numbers stale on master" is false for `findings/ledger/ledger_cmd/merge_cmd/telemetry` (byte-identical) | E2 internal | 1.2 row 1 | re-base citations only for `panel*`, `__init__`, tiers JSON |
| C-S15 | HO:58 states the source-blind cause as fact; `COMBO-REPORT.md:373` calls it an inference, UNVERIFIED | E2 internal | H18 | keep as hypothesis; test with a source-aware brief (U4) |
| C-S16 | Tier 2b policy text (#518: owner 2026-11-12) vs run 1 quote (owner 2026-11-11) vs tier file (static lists), and a test now ties tier-list lengths to `ccsession-models.json` slot counts | E3 vs E1/E2 | X10, TS-4 | tier data derived from, or checked against, ccsession slots |

## 10. Target-architecture inputs (output (d)): shared core versus thin modules, from this slice's facts

| Layer | Component | Evidence for it | Source items |
|---|---|---|---|
| CORE | Finding schema = findings-v2 as superset, with a repair-before-reject parser and a persisted drop report (count, ids, reason) | 49 blocking lost, 4 flips; whole-line drops in v1 and v2 | V-3, V-20, C-S1, Q1 |
| CORE | Anchor/citation locator with explicit policy: unique-anchor guidance, miss gate (warn/reject), `anchor_ambiguous` used, one line model (`splitlines` vs `\n`) | missing-anchor rows never clear; line-model mismatch | F13-F16, F21, V-23, V-31 |
| CORE | Id grammar and document-type profile (ref regex, section naming, `doc_format`, `language`) supplied by the module, not hard-coded | `T01.02` lost; telemetry regex spec-shaped | F17, R-1..R-4, Y-9 |
| CORE | Clustering: v2 same-defect with chain flag and support; v1 compatibility for existing ledgers | over-merge/split defects | F19, V-24, V-25, Q2 |
| CORE | Ledger state machine (`review-ledger/1`): public contract kept; fixes for clearing, double revise, new-text hash, defer audit, cap/round bounds, locking, atomic `--out` | the table L1-L21 | V-22, V-26..V-30 |
| CORE | Verdict policy plug point: any-blocking (current), quorum, calibrated support; re-review quorum rule; partial-panel rule | any-blocking loses to over-flaggers (wrong blockers 1.8-4.75 per row); one re-reviewer downgrades | V-5, V-21, V-26, C-S4 |
| CORE | Panel config + resolution with `classes`, strict distinctness as the default, loud duplicate/none-available, launch adapters for gateway models, one model registry fed by the tier file and checked against `ccsession-models.json` | silent duplicates (26 of 40); `launch {}`; three registries; ember missing | E-1..E-14, V-33, V-34, C-S5, C-S6, C-S16 |
| CORE | Model identity check (observed vs requested model, `-build` suffix, `<synthetic>`), per-attempt metadata and cost accounting, ladder from tier data | misrouting found by audit A; harness bugs | RR-4..RR-10, V-8, V-37 |
| CORE | Brief generator: limits and enums read from the parser constants; inputs named by role (source, spec, roadmap) with a "was it opened" record; one blocking rule | B-2 drift; source-blind 156/665 | BR-2..BR-10, V-4, V-32 |
| CORE | Telemetry wired into merge/resolve, `model.observed` filled, strata generalised from sonnet/haiku to classes; manifest and shadow records from E1 reused | unwired telemetry | Y-1..Y-10, V-35 |
| CORE | Evidence/citation verification and calibration as optional stages (E1 `verify_cmd`, `confidence-calibrator`, per-finding `calibration`) | reflect has them, panel has none | RV-8, RV-10, V-39 |
| CORE | CLI exit codes and report contract usable from CI (merge exit, atomic writes) | PR use | V-30 |
| M-TL | Tasklist profile: ids `T<PP>.<TT>`, `R-###`, `D-####`; categories (coverage vs source/roadmap, dependency, AC, traceability); source-aware brief; panel templates from V-2; ground-truth benchmark from the three packages; integration at sc-tasklist Stage 10.5 and sc-workflow Wave 4 replacing or joining reflect UC-1 | no tasklist logic anywhere in `cli/review`; reflect UC-1 is the baseline (advisory) | 3.5, X1, C-S7, C-S8, V-58 |
| M-RF | Reflect profile: `reflect-*` templates, deviation classes, `channel`, shadow/panel engine flag, calibrator rules, executor-class exclusion, adversarial merge as the verdict plug | E1 code at HEAD | 6.3, 6.4, V-56 |
| M-SP | Spec-review profile: `RP` rubric, `SP` Review Loop bullets, grading check wording, cap 3, escalation text | the only current consumer | BR-1..BR-13 |
| M-PR (later) | PR/code review and rf-qa replacement: diff citations, read-only reviewer agent, cap-2-fix-cycles sentence copied across rf-qa prompts | not in the six notes beyond BR-13, RV-2 | BR-13, 11 below |
| HARNESS | Benchmark kit: blind judge, anonymiser, ground-truth packages, audits, regeneration from committed inputs only | numbers cannot be regenerated from the commit (`/tmp` reads) | 1.2 row 7, V-70..V-75 |

## 11. Future-use-case exposure list (output (e)): what in this slice breaks or limits reuse for PR review, rf-qa replacement, spec review, further tasklist work

| ID | Exposure | Why (evidence) | Use case hit |
|---|---|---|---|
| FX-1 | Text-anchor limit 12-200 chars, whole-line drop | code and diff hunks, long table rows and long lines exceed 200 chars; luna/ember/wonder already break it on prose | PR review, rf-qa, tasklist |
| FX-2 | Exact-substring anchors over whitespace-flattened text | markdown escapes, backticks, rendered diffs do not match; first occurrence used; ambiguity unused | PR review, spec |
| FX-3 | Line-number model (`\n` vs `splitlines`) | files with `\r`, form feeds, U+2028 shift spans | PR review (arbitrary source files) |
| FX-4 | Id grammar fixed to `XX-n.n` / `P<digit>` / numeric sections | `T01.02` lost; PR numbers, issue ids, `file:line` unsupported | tasklist, PR review |
| FX-5 | Category enum is spec-shaped (`unpassable-check`, `missing-requirement`, `data-loss`, `safety`) | a code review needs bug/security/test-gap classes; reflect needs deviation classes (v2 has `reflect_category`/`deviation_class`) | PR review, rf-qa |
| FX-6 | Severity/blocking semantics inconsistent across files | `SP:259`, `RP:31`, `F:100`, v2 rule | all |
| FX-7 | Brief names only the candidate, no source/baseline roles beyond `BASELINE`/`PRIOR` | source-blind reviews; PR review needs diff base, ticket/issue, tests | PR review, tasklist |
| FX-8 | Reviewers are generic sessions with no read-only allowlist | only reflect has a read-only agent (tools allowlist, `permissionMode plan`); harness leaves Bash enabled | PR review (untrusted diffs), rf-qa |
| FX-9 | Single-reviewer re-review; one reviewer can downgrade a blocker | `apply_to ["first"]` | rf-qa (fix loops), spec |
| FX-10 | Any-blocking verdict, no calibrator | weakest model decides; wrong blockers 1.8-4.75 per row | all |
| FX-11 | Multi-round behaviour never exercised with real panels (study scored round 1 only); `revise` double-run, no new-text hash, clearing ignores block validity | run 2 report K4; D-items | rf-qa replacement, spec loop |
| FX-12 | No locking, non-atomic `--out`, `merge` exit 0, relative doc path stored | concurrent CI jobs on one ledger | PR review in CI |
| FX-13 | Launch undefined for gateway models; panel templates cannot reach muse/gpt/glm models today; tier list lacks ember; reflect profile permits only sonnet/opus/haiku launchers | `launch {}`; `P:72` | all non-Claude panels |
| FX-14 | Env detection by `T3Model01` only; `T2bModel01` unread; `claude-gw-tier2b` alias presence unchecked; `ccsession-models.json` coupling only via one test | `P:485-492`; TS-4 | portability to other workspaces |
| FX-15 | Silent duplicate models by default; exclusion only by flag | 26 of 40 run ids | all panels |
| FX-16 | Telemetry unwired, strata `sonnet`/`haiku` only, `doc_format` markdown, language "en" | `T:111-115, 179-180` | PR review (code docs), non-English specs |
| FX-17 | Benchmarks rest on 3 plan packages, n=4-6, ceiling ~2-2.5/14; recommendations may not transfer to specs or code | run 2 report K3 | spec, PR review |
| FX-18 | Benchmark regeneration depends on `/tmp` copies; raw transcripts not in git; ground truth packages are the only reusable asset | 1.2 row 7, GS-4 | every re-benchmark |
| FX-19 | Gateway behaviour (misrouting under load, quotas, binary replacement) silently changes which model reviews; harness falls back silently except `fallback.log` | run 2 report K6; V-8; RR-10 | all |
| FX-20 | rf-qa replacement: cap "at most 2 fix cycles (3 reviews)" text is copied into 8 prompt/agent files that call no script; rf-qa fixes in place while panel reviewers are read-only | BR-13 | rf-qa replacement |
| FX-21 | Panel/ledger wired into no skill other than `/sc:spec-panel` (and reflect shadow); variants live only in `~/.claude` | 3.5, H16, RV-4 | any new consumer must wire its own loop |
| FX-22 | Dead registrations: `lint_cmd`, `estimate_cmd` | H15 | CLI surface |

## Summary

- **Material read in full** at tip `6c0984326`: HO (67 lines) and the six notes (R1CM 66, R1CP 100, R1TT 13, R2CM 160, R2CP 195, R2TT 137). Code facts checked against HEAD `50d4d2b9d` (shell reads, `git diff --numstat` vs `ec259f1b7`, and live re-runs of `superclaude review panel resolve` and `findings.annotate`).
- **What HEAD changed for these notes.** `findings.py`, `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `telemetry.py`, `telemetry_cmd.py`, `RP`, `SP`, `reflect-reviewer.md`, `confidence-calibrator.md`, `sc-tasklist-protocol/SKILL.md` are byte-identical to the runs' base, so almost every merge/ledger/findings/telemetry/brief line cite in the notes is still exact. Stale: `panel.py` (525 to 707 lines), `panel_cmd.py` (87 to 129), `__init__.py`, `review-tiers.default.json` (+`classes`), `sc-reflect-protocol/SKILL.md` (+68 lines, all later cites shifted about +40), `sc-workflow-protocol/SKILL.md` (Wave 4 now `:85-89`), `MODEL-TIERS.md` (Tier 2b row rewritten, now `:44`).
- **HO's own claims.** Rows 1-8 hold in substance. Contradicted or overstated: "line numbers stale on master" (false for merge/ledger/findings/telemetry); "four facts" (it lists eight rows); "each claim checked" (rows 5-7 say not re-checked); source-blind cause stated as fact (`COMBO-REPORT.md:373` says inference); row 1's attribution to run 2 notes (R2CP:121 says #519 not inspected); "159 functions" is an arithmetic error (the table sums to 179); D-numbers cited in HO are report numbers, not the notes' D-numbers.
- **Run 1 vs run 2 notes.** 16 agreements (2.2), 13 disagreements or deltas (2.1), 5 in-note corrections (2.3). Run 2 is deeper (23 vs 13 merge defects, 19 vs 16 panel defects) and correct on the tasklist-review baseline; run 1 is correct on T2bModel01 references (run 2's "not referenced anywhere in src/ or tests/" is contradicted by `ccsession-models.json:107`, `README.md:445`, `tests/unit/test_ccsession_tiers.py:72-73,239` at the base).
- **HEAD answers to run 2's open questions Q1-Q3** (6.4): findings-v2 still drops whole lines with the same limits; `cluster_v2` flags chaining but the ledger path still uses v1 `cluster`; `hard_exclude`/`strict_distinct` remove silent duplicates only when passed, the default path still duplicates (re-run: 26 of 40 `@live7` run ids).
- **New facts not in any note** (found at HEAD): findings-v2 is E1's superset and already carries `lens: spec`; six `reflect-*` panel templates; `classes` map; reflect shadow mode resolves through the panel (`SKILL.md:338-349`) so the notes' "reflect has no panel/tier code" is outdated; a #518 test ties tier-list lengths to `ccsession-models.json` slots; E1's experiment uses the same `designSpec` package as one of E2's three; `snap.py` in E2's folder writes into E1's evidence tree.
- **Inventory size.** About 360 coded entries: HO claims (H1-H19 plus rows 1-8), 13 disagreements, 16 agreements, 5 corrections, 21 findings/parser rows, 9 drop-rule rows, 22 merge/ledger rows, 4 reference-id rows, 77 panel/telemetry/test/tool/workspace/git rows (P 6, E 14, T 5, Y 10, TS 11, RR 12, W 12, GS 7), 14 brief rows, 15 reflect-vs-panel rows, 3 answered questions, 13 study findings, 20 defect groups, 12 decisions, 9 artifact groups, a 15-row overlap matrix, 16 conflicts (C-S1..C-S16), 17 architecture components, 22 exposures (FX-1..FX-22).

## Gaps and Questions

### Not verifiable from this worktree (marked `[UNVERIFIED]` above)
1. The two run reports (`HANDOFF-review-panel-unification.md`, `...-run2.md`) are outside this slice: report-only numbers (46 unanchored rows with 13 blocking, 83 mega-cluster rows, U1-U18, DM1-DM18, 11 open decisions, DO4, K1-K11 beyond those I grepped, R12 efficiency figure) were not re-checked. Slice 01 covers run 2's report.
2. The untracked-file state (3,041 files, ~1.5 GB, 1380/1352/309 split) lives in the other worktree; the "2,916 raw files" vs 1689 transcripts discrepancy (1380+309) stays unreconciled.
3. `/tmp` state (70 `/tmp/*.sh`, 12 repo / 58 not; `/tmp/evalsb/*`) is gone or foreign; the 55-file `tmp-scripts` copy vs "58 not in repo" differs by 3.
4. Which commit added the 96 raw transcripts that `6c0984326` untracked.
5. Pytest was not re-run at HEAD: 304 passed is the base result; HEAD has more tests (116 in the 7 original `tests/review` files vs 111). Counts here are `def test_` greps, not collected counts.
6. `combos/` tracked entries: 97 at the tip vs run 2's "107 entries (SPEC.md + 106 row dirs)"; why 10 rows are missing from the tracked tree (untracked dirs? quarantine moves?) is unexplained. Only 19 `RESULT.md` files exist; which rows lack one was never listed.
7. `r19` having `glm-5.3` three times (R2TT:37) not individually re-run; `template_sha256`/`tiers_sha256` values at HEAD not recomputed (tiers JSON changed).
8. How `validate_reflect_profile` (`panel.py:80-136`) constrains `reflect-*` templates (reviewer cap 3, launch set) was not read; C-S6 rests on the constants only.
9. The relation between E3's installed ledger/stoprule/diffgate variants (`sc-review-ledger`, `finding-grader`) and `cli/review/ledger.py` was not read (R2CP:185 says UNVERIFIED too).
10. Whether `findings_v2`/`cluster_v2` are meant to replace the v1 ledger path (Stage 3+ of E1) is not in this slice.
11. HO row 5's attribution ("run 1 described the ladder as fixed") cannot be matched to R1TT.
12. The brief shared by both runs (H1) and the process claims about orchestrator models and agent pinning (H2-H4) are not checkable.

### Questions for the final report or the owner
- Q-A: Which defect numbering will the final report use? Recommendation: file:line plus the owning document, since HO, R2CM and the run 2 report number the same defects differently (2.4).
- Q-B: Is "clear a `resolved_check` row when its reviewer's block was broken" a bug (docstring `L:112`) or a contract (existing test `tests/review/test_review_ledger.py:380-385`)? The unified design must pick one.
- Q-C: Should the unified findings schema keep a text `anchor` at all, or move to findings-v2 citations with an optional quote? (FX-1, FX-2, C-S1.)
- Q-D: Does the unified verdict replace reflect UC-1's advisory (non-blocking) tasklist review, or sit beside it? (V-58, C-S7.)
- Q-E: Does the E2 owner agree to remove `snap.py`, `drift-b3.py`, `rlog-r3.sh` (and `brief_c1.py`) from the E2 branch, given `snap.py` can write into E1's evidence tree?
- Q-F: Is the "brief never names source.md" hypothesis (HO:58) tested by any run? `COMBO-REPORT.md:373` says it is an inference.
- Q-G: Are gateway models to be launched by raw model id (`claude -p --model`, the study path) or by tier alias (product path where an alias serves only the first tier model)? (V-61, E-8.)
- Q-H: Should the notes' stale line cites be re-based before the final report quotes them (panel, panel_cmd, reflect SKILL, workflow SKILL, MODEL-TIERS)? This slice gives the HEAD lines for the ones I touched.

