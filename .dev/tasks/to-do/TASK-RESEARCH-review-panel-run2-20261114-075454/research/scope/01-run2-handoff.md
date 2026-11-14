# Scope slice 01: run-2 hand-off

**Status:** Complete
**Date:** 2026-11-14
**Material:** `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md` (run-2, 543 lines) and `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification.md` (run-1), both read at `origin/ironbelly/eval-tasklist-review-panel` tip 6c0984326cbb8fb06c4a36065de58b171d3f8175 (run-1 commit 4a22d74213f93837d00c2c314075dd967b9a98e3 is its ancestor).
**Code checked at:** HEAD of worktree `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel` (branch ironbelly/shadow-runs). HEAD = 50d4d2b9d1f2288afa497830b3049f2fe48f5c75 (contains #519 d2d8a2d16 and #518 167184c6b).
**Independence:** nothing under `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` or `REVIEW-PANEL-UNIFY-RUN2-QUEUED.md` was opened. Only E2-branch files read (all via `git show 6c0984326...:<path>`): the two hand-offs, plus `HANDOFF-run1-vs-run2.md` (67 lines, the other session's own comparison, same commit c2ddeb1b4) and, for spot checks of cited numbers, `COMBO-REPORT.md`, `PILOT-REPORT.md`, `combos/SPEC.md`, `manifest.md`, `RAW-TRANSCRIPTS-NOT-COMMITTED.md`, `tools/run-reviewer.sh:10`, `analysis/audits/audit-D/summary.md`.
**Legend for verdicts:** VERIFIED = checked at HEAD code/tree and matches; CONTRADICTED = checked and does not match; STALE@HEAD = true at branch base ec259f1b7, changed by #519 at HEAD; UNVERIFIED = not checkable here. `RV` = `src/superclaude/cli/review`. `CR` = E2 `EVAL/COMBO-REPORT.md` (EVAL = `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`).
**Destination tags (value inventory):** CORE = shared Review Panel core; TL = tasklist/plan-review module; REF = reflect module; SPEC = spec-review module; EVAL = regression fixture/eval harness; OPS = ops lesson; DROP = retracted/superseded; OPEN = needs owner decision.

---

## 1. Material identification

| Item | Value | Source |
|---|---|---|
| Run-2 hand-off | `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification-run2.md`, 543 lines (`wc -l` at tip 6c0984326; the E2 comparison file says 544), added in commit c2ddeb1b4 (2026-11-13 16:17:36 +0000) | `git log` on tip; `git show` |
| Run-1 hand-off | `.dev/eval-workspaces/tasklist-review-panel/HANDOFF-review-panel-unification.md`, 315 lines, added in commit 4a22d7421 (2026-11-13 15:55:41 +0000); unchanged between 4a22d7421 and tip (`git diff --stat` empty) | `git log`, `git diff --stat 4a22d74..6c09843 -- <file>` |
| Third document at tip | `HANDOFF-run1-vs-run2.md`, 67 lines (8,976 bytes), c2ddeb1b4; verdict "Use run 2 as the main hand-off" (cmp:16); recommends re-checking run-2 D1-D13/P1-P7 against origin/master #519 (cmp:67) | `git show` tip |
| Raw notes behind both | `handoff-notes/run1/{code-merge,code-panel,tests-tools}.md` (13,098 / 25,496 / 2,823 bytes), `handoff-notes/run2/...` (17,702 / 31,874 / 26,220 bytes); run-2 cites them as `code-merge.md:n`, `code-panel.md:n`, `tests-tools.md:n`. NOT read here (outside the assigned material) | `git ls-tree -l` tip |
| Commits after the hand-offs on the E2 branch | tip 6c0984326 "chore(eval): untrack 96 raw claude transcripts that were committed by mistake"; d561461fa "panel-process-redesign brainstorm and the five collaboration harnesses"; fd69a006d "panel-collaboration brainstorm and five redesign designs"; c2ddeb1b4 (run-2 + comparison). Not covered by this slice | `git log 4a22d7421..6c0984326` |
| Authorship/method of run-2 | Single writer agent from three fresh notes + own Reads/greps + one test run; no task folder, no QA fleet (run2:14); did not open run-1 or its notes (run2:15); all agents pinned to Opus 5.5 per cmp:8 | run2:12-17; cmp:5-12 |
| Date quirk | run-2 header says date 2026-11-13 and that its internal "2026-11-14" means 2026-11-13 (run2:5). Today's session date is 2026-11-14, so "2026-11-14" inside run-2 is NOT today | run2:5 |
| Run-2 branch/HEAD at writing | worktree `eval-tasklist-review-panel`, HEAD 4a22d7421 = origin copy; branch base ec259f1b7 (= origin/master at eval start, manifest.md:6-8) | run2:6-8 |
| Branch distance | run-2 says 11 commits behind origin/master (run2:55, :467). Re-checked: `git rev-list --count 4a22d7421..origin/master` = 11 (local origin/master ref = d2d8a2d16, i.e. #519 tip); `rev-list --left-right --count origin/ironbelly/eval-tasklist-review-panel...origin/master` = 7 left / 11 right at tip. VERIFIED | git |
| This worktree vs run-2's "newer master" | `git diff --stat ec259f1b7 HEAD -- src/superclaude/cli/review tests/review` = "40 files changed, 8026 insertions(+), 15 deletions(-)" — exactly run-2's "40 files, +8,026" (run2:17, :467). `git diff --stat ec259f1b7 HEAD -- src tests` = 171 files, +28,145/-124 (broader than run-2 states) | git |

## 2. Structure map of the run-2 hand-off (line ranges, `run2:n`)

| Section | Lines | Content | Slice section that covers it |
|---|---|---|---|
| Header table, method note, conventions, terms | 1-38 | Provenance, independence, abbreviations, 9 defined terms (tasklist review, packages, GT, model short names, row/row-package, valid era, found/14, real blocking/8, judge-blocking, wrong blockers, B1-B8/I1-I8) | 1, 6.1 |
| 1. Inventory (1.1 git state, 1.2 eval artifacts, 1.3 product code exercised) | 40-93 | 7 git-state rows, 18 artifact rows, 9 product-code rows | 5, 6.7 |
| 2. Findings (2.1 sample sizes, 2.2 R1-R21, 2.3 retractions, 2.4 defects) | 95-217 | 8 phases; 21 results; 11 retractions; 13 merge/ledger defects D1-D13, 7 panel/tier P1-P7, 2 telemetry T1-T2, 7 brief B-1..B-7, 12 harness H1-H12 | 6.2-6.4, 4 |
| 3. Lessons (3.1 worked, 3.2 failed, 3.3 next time) | 219-267 | 13 methods that worked, 10 failed, 9 to-do-differently | 6.5 |
| 4. Decisions (4.1 made DM1-DM18, 4.2 open DO1-DO11) | 269-308 | decision log with UTC times and owners; 11 open decisions with deciders | 6.6 |
| 5. Review Panel as understood (roles, contracts, tier config, recording, tasklist-specific?, contrast with reflect Tier 2) | 310-418 | 11-row role table, 11-row findings-v1 field table, 11 other contracts, 6-tier table, 5.4 layers, 5.5 tasklist-specificity, 5.6 reflect contrast | 4, 7, 8 |
| 6. Requirements U1-U18 | 420-443 | 18 requirements with Must/Should + evidence | 8 (target-architecture inputs) |
| 7. Questions Q1-Q11, risks K1-K11 | 445-477 | questions for the other (reflect) session; merge risks | 6.8, 9 |
| 8. Test status (8.1 304 pass, 8.2 gaps, 8.3 tests on newer master, 8.4 not verified) | 479-532 | per-file test table, 14 gap rows | 4.5, 6.9 |
| Reading order | 534-543 | 8-step order for the other session | - |

**Self-declared limits of run-2 (run2:14-17, :312, :526-532):** single-author draft with spot verification, not QA-gated; reflect sources NOT re-read (taken from `code-panel.md`); `ledger.py:301-401` and `telemetry.py` taken from notes; audits B, C, E, F conclusions taken from CR:290-298 and CR:373 (no committed summaries); origin/master (#519) code only listed/grepped, not reviewed; existence of `/tmp` inputs unknown. Every `[UNVERIFIED]` below that repeats one of these is inherited.

## 3. Differences between run-1 (`run1:n`) and run-2 (`run2:n`) and every correction run-2 makes

### 3.1 Form and method (no content judgement)

| # | Difference | Run-1 | Run-2 | Evidence |
|---|---|---|---|---|
| F1 | Length | 315 lines | 543 lines (cmp says 544) | `wc -l` |
| F2 | Who wrote it | Orchestrator (Tier 1b Sonnet 5.5 per cmp:8) with the whole session context + 3 read-only agents | Three new read-only agents + a separate writer agent, none able to open run-1 or its notes; the orchestrator only fixed one date (cmp:9); orchestrator Tier 1a Opus 5.5, agents pinned to Opus (cmp:8). Model/session claims [UNVERIFIED, from cmp only] | run1:6; run2:14-15; cmp:8-9 |
| F3 | Honest-scope note | Method note: no task-file machinery, no QA fleet, "nothing was cross-checked by a separate QA pass" (run1:6, :307) | Same, plus "single-author draft with spot verification" and a list of what was not verified (run2:14, :526-532) | both |
| F4 | One-paragraph summary | Has section 0 (run1:10-12) | None; replaced by a reading order at the end (run2:534-543) | both |
| F5 | Status vocabulary | C-P / UNCOM / LOCAL-ONLY, G/T reusability flag (run1:18) | CP / CL / UC / MASTER / OUT, free-text "reusable beyond tasklist review?" (run2:42, :61) | both |
| F6 | Citation style | `RV/<file>:n`, `CR:n`, `PR:n` (run1:5) | bare `findings.py:n`, `prompts:n`, `spec-panel.md:n`, `tiers.json:n`, `audit-X:n`, plus `code-merge.md:n` / `code-panel.md:n` / `tests-tools.md:n` pointers into the raw notes (run2:21-22) | both |
| F7 | Currency of code | Product lines "read this session (2026-11-13)" at branch base; never mentions master moved | Explicitly pins code to branch base ec259f1b7 and flags origin/master #519 as grep-only (run2:17) | run1:5; run2:17 |
| F8 | Evidence trail | Lists files read, with COMBO-REPORT lines 1-12, 47-116, 286-435 only (run1:315) | No trail list; says every file:line was Read or grep-confirmed (run2:16) | both |
| F9 | Model-by-role table | Yes, 10 rows (run1:84-97) | No single table; spread across R14-R18, R20 (cmp:47) | both |
| F10 | Date | 2026-11-13 | Header 2026-11-13 but the body uses "2026-11-14" 9 times on 8 lines (run2:5, :7, :16, :51, :53, :55, :74, :483; `grep -c`/`grep -o` on the tip file), which run2:5 says to read as 2026-11-13 | run2:5 |
| F11 | Verdict between them | - | E2's own comparison: "Use run 2 as the main hand-off", keep cmp section 4 items from run-1 (cmp:16, :41-49, :67) | cmp |

### 3.2 Corrections and new facts run-2 introduces (with evidence and this slice's check)

| # | Topic | Run-1 said | Run-2 says | Evidence cited | Check at HEAD / tip | Verdict |
|---|---|---|---|---|---|---|
| C1 | Master moved | Treats branch-base code as current; never mentions #519 | Branch 11 commits behind; #519 (d2d8a2d16) + #518 (167184c6b) changed 40 files, +8,026, under `RV` and `tests/review` (run2:17, :55, :467) | `git log HEAD..origin/master`; `git diff --stat` | Stat reproduced exactly at HEAD (40 files, +8026/-15). BUT only d2d8a2d16 touches `RV`: `git log ec259f1b7..HEAD -- src/superclaude/cli/review` lists only d2d8a2d16; 167184c6b touches 1 file in `tests/review` (`test_review_panel_live7.py`) and 0 in `RV`, the rest is ccsession tier docs/skills (`git diff-tree` of 167184c6b: CHANGELOG.md, docs/reference/model-aliases.md, skills/ccsession-tag/*, sc-issue-protocol/*, issue-worker-t3.md ...) | VERIFIED for the numbers; CONTRADICTED for the attribution to #518 (also repeated at cmp:22) |
| C2 | Where tasklist review runs today | D14: "No tasklist review step exists in `sc-tasklist-protocol` or `sc-workflow-protocol` in `src`" (run1:118) | sc:workflow Wave 4 runs `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` (advisory, no `--remediate`); sc-tasklist Stage 10.5 runs `/sc:reflect --mode pre --remediate` per phase (run2:406, :436) | `sc-workflow-protocol SKILL.md:60, :76`; `sc-tasklist-protocol SKILL.md:1630` | HEAD: `sc-workflow-protocol/SKILL.md:89` ("Invoke `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` via Skill, defaults for every other flag, no `--remediate`") and `:105`; base ec259f1b7 has the same text at `:60`/`:76` (so run-2's cites are right for base; +29 line shift at HEAD). `sc-tasklist-protocol/SKILL.md:1621,1630` identical at base and HEAD ("fan out one `/sc:reflect --mode pre --remediate` agent" per phase, Stage 10.5) | run-2 VERIFIED; run-1 D14 first half CONTRADICTED by code (run-1 grepped only `superclaude review` strings, cmp:23) |
| C3 | Audit summaries | "summaries in summary.md" for A-F (run1:139) | Only A and D have `summary.md`; B, C, E, F hold scripts + flags.tsv; conclusions live at CR:290-298 (run2:76) | `ls` | `git ls-tree -r tip .../analysis/audits` -> 2 `summary.md` | VERIFIED |
| C4 | Helper scripts | "Only files that reference this eval were copied" (run1:52) | `snap.py`, `drift-b3.py`, `rlog-r3.sh` reference a different eval (`brainstorm-reflect-panel`) and `snap.py` writes into it (run2:74) | grep | `git grep brainstorm-reflect-panel` at tip over `tools/tmp-scripts` -> exactly those 3 files. `snap.py` write behaviour [UNVERIFIED, not opened] | VERIFIED (3 files); write claim UNVERIFIED |
| C5 | Harness bugs | Ladder "patched" (run1:129) | Three still open: H2 `expected_model` overwritten on fallback, H3 attempt counter reset overwrites primary's attempt files and undercounts cost, H4 `BLOCK_OK` only greps the fence line (run2:207-209) | `run-reviewer.sh:57-87` | tip `run-reviewer.sh`: `:57` `grep -q '^```findings-v1'`; `:76` `MODEL="$NEXT"; ...; attempt=0` (so `:58` meta uses `$MODEL` = fallback model; files named `$RID.attempt$attempt` with no model component); `:87` cost from `$RID.attempt*.meta.json`; ladder guard at `:66-83` (`EXCLUDE_MODELS`, `VISITED`, `NOFALLBACK`) | VERIFIED (read directly) |
| C6 | Raw-file count | 3,041 untracked, 1,380 + 1,352 + 309 (run1:59) | Same count, plus discrepancy with `RAW-TRANSCRIPTS-NOT-COMMITTED.md:2` "2,916 files"; the note implies `meta.json` committed while per-attempt meta are uncommitted (run2:53, :57) | note lines 2-3 | Tip file: line 2 says "2,916 files", ~1.48 GB; line 3 "meta.json/cost.json ... IS committed" | VERIFIED (text); reconciliation UNVERIFIED. Note: tip commit 6c0984326 "untrack 96 raw claude transcripts that were committed by mistake" changes the committed/untracked picture after both hand-offs |
| C7 | Reproducibility | Not raised (only "58 helper scripts only in /tmp", run1:173) | H10: analysis scripts read/exec `/tmp` copies (run2:75, :215) | `final-table.py:23`, `three-way.py:4`, `b9-table.py:3`, `doubles.py:3`, `issue-setup.py:3` | tip: `final-table.py:23` `f"/tmp/audit-{k}/flags.tsv"`; `three-way.py:4` `exec(open("/tmp/final-table.py")...)`; `b9-table.py:3` `open("/tmp/b8-table.py")`; `doubles.py:3` `open("/tmp/attrib.json")`; `issue-setup.py` is at `analysis/issue-table/issue-setup.py:3` `exec(open("/tmp/final-table.py")...)` (run-2 omitted the subfolder) | VERIFIED |
| C8 | Test count | "299 passed in 7.1 s", per-file counts that do not add up, 5 skills files (run1:303) | "304 passed in 4.86 s", 13 files, per-file table (run2:483-499) | pytest | At HEAD the same 13 files collect 309 (cli 9->13, live7 14->15 from #519). Per-file collected counts at HEAD match run-2 for the 11 unchanged files (findings 23, ledger 24, panel 41, rules_text 5, telemetry 10, brief_placement 5, loop_extension 18, prompt_overrides 33, severity_mapping 14, severity_rule 62, spec_panel_review_loop 46). 304 - 299 = 5 = `test_review_brief_placement.py` (5), which run-1 omitted | VERIFIED (arithmetic and counts); run-1's per-file figures were `def test_` counts (panel 26) not collected items (panel 41) |
| C9 | Defect granularity | One D1 "over-length drop" lumps merge drop, partial-panel PASS, clearing | Splits D2 (partial-panel invisible), D3 (docstring vs clearing loop), D4 (chaining) vs D5 (ref mismatch splitting), D9, D10, D11, D12, D13 | `ledger.py`, `findings.py` | All VERIFIED at HEAD in section 4 | see 4.1 |
| C10 | Brief vs parser | D8 only: brief has no source placeholder; D9 missing-requirement conflict | B-1..B-7: adds that claim/refs/id/MINOR limits are not in the prompt, B-3 severity-vs-blocking triple conflict, B-4 report-ending conflict, B-5 anchor guidance, B-7 merge consequence not told to reviewers (run2:192-200) | `prompts:17-21, :31, :32, :58-62` | VERIFIED at HEAD (section 4.3) | VERIFIED |
| C11 | Tier data | "tier lists pick unusable models ... ember not listed" (run1:240) | P3: ember absent from tier data; P4 Qwen/glm still in tier lists; P2 gateway `launch` map empty (run2:181-183) | `tiers.json:4-11, :19-24` | `review-tiers.default.json` at HEAD lines 5-10 (aliases), 25-30 (gateway env, `launch: {}` at :29); no `muse-ember` anywhere in `src tests docs scripts` (`grep -rIl`); `Qwen3.8-max|glm-5.3` 5 hits in that one file | VERIFIED (line numbers shifted +6 at HEAD for environments) |
| C12 | Telemetry | D15: strata only sonnet/haiku; merge/resolve write no telemetry | T1 no product caller of `append_record`, `model.observed` has no producer; T2 strata hard-coded (run2:187-188) | `code-panel.md:89-95`, `telemetry.py:112-115` | HEAD: `append_record` has exactly one caller `telemetry_cmd.py:67` (manual `review telemetry append --record <json>`); no skill/command/script calls it; `STRATA = ("sonnet","haiku")` at `telemetry.py:112-115`, check at `:267`; `"model": ("resolved","launch","observed")` at `:49`, `model_observed` read by the view at `:364` | VERIFIED with nuance: "no product caller" is true for automatic callers only; the CLI append command is a (manual) caller |
| C13 | Ref regex | D7 INFERENCE UNVERIFIED on a real tasklist (run1:111) | Verified by a direct call by the note author (run2:168) | `code-panel.md:168` | Direct call at HEAD: `refs_norm({'anchor':'Task T01.02 does x','claim':'T01.02 bad','refs':['T01.02','AC-0.4','1.2']})` -> `['1.2','AC-0.4']` (T01.02 lost) | VERIFIED |
| C14 | Environment selection | D12: `T2bModel01` never read by `cli/review`, `T2bModel01` only in ccsession config | P5: env guessed from `$T3Model01` only; all TxModelNN slot variables unused to choose models (run2:184) | `panel.py:365-374` | HEAD `panel.py:485-494`: only `SUPERCLAUDE_REVIEW_ENV`, then `T3Model01`; `grep T2bModel01 src` hits only `skills/ccsession-tag/{MODEL-TIERS.md,README.md,ccsession-models.json}` and `sc-implement-protocol/refs/retry.md`, none in `RV` | VERIFIED |
| C15 | Evidence for D1 numbers | Per-model counts labelled as "blocking findings lost" (luna 30, ember 33...) (run1:89-90, :105) | Same numbers placed after "49 blocking findings lost" (run2:135, :162) | `audit-D:8, :16-19` | audit-D:16 total dropped by reason 56+18+14+3+1 = 92; audit-D:17 per-model counts luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1 sum to 92 = ALL dropped findings; the 49 BLOCKING dropped (audit-D:8, :19) is a subset and is not broken down by model. Both hand-offs (and CR:292) present per-model figures as if they were the blocking subset | CONTRADICTED in both hand-offs (mislabel; the numbers themselves match audit-D) |

### 3.3 Run-1 items that run-2 drops or weakens (cmp section 4 lists 5; this slice adds the rest), each checked at HEAD where code-based

| # | Run-1 item (`run1:n`) | Run-2 status | Check at HEAD / tip | Verdict |
|---|---|---|---|---|
| L1 | D13 `lint_cmd` and `estimate_cmd` registered but files missing, `ModuleNotFoundError` swallowed (`__init__.py:19-32`) (run1:117) | Not in the report (in notes only, cmp:45) | HEAD `RV/__init__.py:19-29` lists `lint_cmd`, `estimate_cmd` among 9 names; `ls RV` has neither; `:30-35` swallows `ModuleNotFoundError` only when `exc.name` equals the module. Now also lists `cluster_cmd`, `verify_cmd`, `manifest_cmd` (all present, #519) | VERIFIED still true at HEAD |
| L2 | D14 second half: review-ledger skill, `spec-panel-ledger`/`-stoprule` commands, `finding-grader` agent exist only as experiment copies in `.dev/experiments/346-validation/phase5/final-bundle/builds/` (run1:118); Q7 (run1:287) | Not in report | HEAD: `src/superclaude/skills` has none of review-ledger/stoprule/diffgate/fix-audit (only `sc-bare-review`); `src/superclaude/agents` has no `finding-grader`; they ARE installed in `~/.claude` (skills `sc-diffgate`, `sc-fix-audit`, `sc-review-ledger`, `sc-spec-panel-stoprule-protocol`; agent `finding-grader.md`; commands `spec-panel-{armb,diffgate,ledger,ponytail,stoprule}.md`); source builds at `.dev/experiments/346-validation/phase5/final-bundle/builds/{diffgate,ledger,minfix,ponytail,stoprule}` | VERIFIED (this is E3 material: installed-only variants) |
| L3 | D16 round 4 accepted after ESCALATE; `--cap` ignored on an existing ledger; verify-only rounds are prompt-only (run1:120) | Only as test gaps "Round 4+ after ESCALATE; non-default --cap" (run2:513) | `ledger.py:114` checks only `n == len(rounds)+1`; `merge_cmd.py:101-104` passes `cap` only to `new_ledger`; `_decision` (`ledger.py:93-96`) uses stored `cap_reviews` | VERIFIED |
| L4 | D9 brief makes missing-requirement Medium by instruction, schema allows blocking (run1:113) | Partly folded into B-3 (run2:196) | `prompts:31` "Grade it Medium when ... the finding is a requirement the document never states"; `findings.py:15-22` category list has `missing-requirement`; `findings.py:100-101` only MINOR+blocking is rejected | VERIFIED |
| L5 | Pilot decision-rule outcome: only arm C passes, by one defect (run1:81) | R12 gives efficiency only (run2:127) | PILOT-REPORT.md tip lines 44-71: A 2/16, B 3/16, C 4/16; blocking recall 0/8 for all; "C passes exactly (2 >= 2x1)"; catches/100k tokens A 2.15, B 0.76, C 0.66 | VERIFIED |
| L6 | Requirement 1: accept both finding shapes or define a mapping; keep anchor locate check (run1:265) | Only as question Q5 (run2:455); U-list has no mapping requirement | - | design gap in run-2 (see 8) |
| L7 | Requirement 9: reviewer isolation (fresh context, sandbox excluding `.dev/tasks/done`, eval workspaces, GT) (run1:273) | Kept as a method (run2:228), not as a U requirement | - | design gap in run-2 |
| L8 | Q5: is reflect's rotation table (sonnet/haiku/qwen\|kimi\|deepseek else opus) still valid given Qwen disqualified (run1:285); Q7 stoprule experiment status; Q3 does calibrator disjointness conflict with `distinct_across_slots` | Q5 and Q7 dropped; Q3 reshaped to Q11 | - | UNVERIFIED (reflect side not in my material) |
| L9 | Run-1 5.4 file layout of per-run and per-judge outputs (run1:244) and 1.3 list of `/tmp` scripts NOT copied (`checks-gate8.sh`, `r2terra-hb.sh`, `r3-hb.sh`, `snap-b3.py`, `mkcards-b3.py`, `r2cmp.py`) (run1:55) | Layout partly in 5.4; the not-copied list is dropped | - | UNVERIFIED (files are in `/tmp` on the author's machine only) |
| L10 | Audit one-liners A-F with specific results (A: 2 b4-muse-luna2 "wonder" runs served terra, grok id `grok-4.7-build` benign; C: no run read GT; E: 12/12, 19/19, borderline GT8) (run1:139) | Mostly kept in R18, R21, audit-D references | audit-D:11 confirms `grok-4.7-build` label-only (51 WARN); CR:296 confirms E | VERIFIED |
| L11 | Explicit statement that no result validates the packaged `@default` or `@live7` as shipped (run1:240) | Equivalent in run2:381 ("decided panels cannot be expressed by the packaged templates") | `review-panel.default.json` (4 reviewers t1b/t2/t3x2) and `live7` unchanged at HEAD | VERIFIED |
| L12 | "anthropic-only `@live7` gives 6 identical haiku" (D11 effect) | Dropped | `review-panel.live7.json` description (HEAD): "resolves to 1 Sonnet + 6 Haiku" by design | VERIFIED but by design, not a defect |

### 3.4 What run-2 adds that run-1 lacks (inventory)

| Group | Items | Lines |
|---|---|---|
| Definitions | 9-row terms table (valid era, found/14, real blocking/8, judge-blocking, wrong blockers, B1-B8/I1-I8) | run2:24-38 |
| Results | R7 (ember + sonnet best precision), R9 (5-reviewer panels no gain), R10 (sonnet association with rare issues), R13 (inputs matter), R15 (terra/sol refusals), R16 (anchor fidelity 91.4%), R17 (presence effects), R18 (operational), R19 (aliases first model only), R20 (merge drops), R21 (judging reliable) | run2:122, :124-125, :128, :130-136 |
| Retractions | 11-row table (do-not-reuse numbers) | run2:138-152 |
| Defects | D3, D4/D5 split, D6 numbers, D9, D10, D11, D12, D13, P2, P3, P4, P6, P7, T2, B-2..B-5, B-7, H1-H12 | run2:160-217 |
| Lessons | 13 worked / 10 failed / 9 do-differently tables | run2:221-267 |
| Decisions | DM1-DM18 with UTC time and owner; DO1-DO11 | run2:271-308 |
| Contracts | Field-by-field findings-v1 gap table incl. "unknown keys accepted silently (room for reflect fields)"; resolution/ledger/status/verdict/merged-report/capture/score/meta contracts | run2:332-360 |
| Requirements | U1-U18 (run-1 had 10 unnumbered) | run2:424-443 |
| Questions | Q1-Q4, Q6-Q8, Q9-Q11 aimed at master #519 code | run2:451-461 |
| Risks | K1-K11 (run-1 had 6) | run2:465-477 |
| Tests | Per-file table, 14 gap rows, 12 new test files on master | run2:485-524 |

### 3.5 Crosswalk of defect IDs (run-1 -> run-2)

| Run-1 | Run-2 | Note |
|---|---|---|
| D1 over-length drop | D1 (+ B-2, H4, DO1, U1, U2) | run-2 adds bad severity 3 and bad refs 1 to the 56/18/14 counts (audit-D:16 confirms) and names the verdict-flip rows |
| D2 dropped re-report clears a blocker | D3 | run-2 adds the docstring-vs-loop contradiction `ledger.py:112` vs `:254-258` |
| D3 merge passes with one valid reviewer | D2 | reframed as "partial-panel failure invisible"; `ledger.py:127-134, :150-157, :421-424`, `merge_cmd.py:117-118` |
| D4 one blocking flag decides | D8 (+ B-7, DO3, U12) | same lines |
| D5 missing anchors kept silently | D6 | run-2 adds 46 rows / 13 blocking (audit-D:30) and that `anchor_status`/`anchor_ambiguous` are never read |
| D6 clustering over/under-merge | D4 (chaining) + D5 (ref-mismatch split) | run-2 adds 83 mega-clusters, 195 of 1,398 rows chains (audit-D:29) |
| D7 ref regex | D7 | now directly verified |
| D8 brief has no source | B-1 (+ R14, DO11, U4) | same |
| D9 missing-requirement Medium vs blocking | (B-3 partially) | dropped as separate item |
| D10 unpassable-ac label | B-6 | FIXED (harness) |
| D11 `distinct_across_slots` duplicates | P1 | run-2 adds 26 of 40 `@live7` ids |
| D12 env keys on `$T3Model01` | P5 | same |
| D13 lint/estimate missing | none | dropped (L1) |
| D14 no tasklist review step / experiment copies | none (C2 reverses the first half) | dropped (L2) |
| D15 telemetry strata, no writers | T1, T2 | same |
| D16 round 4 / `--cap` | none (test gap only) | dropped (L3) |
| - | D9 refound row takes current call; D10 first-match `break`; D11 revise twice; D12 merge exits 0; D13 missing `--report` id; P2 empty gateway launch; P3 ember absent; P4 excluded models in tier lists; P6 re-review anchors only; P7 round_robin by date; B-3, B-4, B-5, B-7; H1-H12 | new in run-2 |

### 3.6 Numbers that differ or were corrected between the two hand-offs

| Item | Run-1 | Run-2 | Truth check |
|---|---|---|---|
| Tests | 299 passed in 7.1 s | 304 passed in 4.86 s | 5 = `test_review_brief_placement.py`; HEAD collects 309 for the same 13 files (see C8) |
| `tools/tmp-scripts` | "54 scripts plus a README" (run1:52) | "55 files + README" (run2:74), "55 files" (run2:50) | tip tree: 55 files including 1 README -> run-1 right, run-2 off by one in run2:74 |
| Rows in `combos/` | "62 distinct reviewer-model sets" / "71 valid-era rows" (run1:71) | "106 row folders" (run2:69) and "71 valid-era rows, 213 row-packages, 665 valid-era runs; 106 scored panel runs" (run2:108) | tip: `git ls-tree -d combos/` = 96 directories (2 of them quarantine/outage-named); audit-D:3 examined 89 rows x 3 = 264 merges; "106" is the scored-runs figure (CR:497 "ALL ... 106"), not a folder count -> run2:69 CONTRADICTED by the tree count |
| Verdict flips | "4 verdicts flipped" (run1:105) | "4 verdict flips FAIL to PASS ... plus total-loss merges" (run2:135, :162) | audit-D:20 lists 3 flips (rows tagged V at audit-D:48, :53, :83: g3-sonnet-luna-ember-r3/alias, g5-ember2-luna-r2/alias, n5-sonnet-ember/design) + 5 total-loss merges; CR:292 says "Four ... (3 named, plus total-loss merges)" -> the figure 4 is [UNVERIFIED]; 3 is what audit-D shows |
| Alias issue found once | "alias GT3 found once" (run1:78) | "B6 found once" (run2:117) | CR:497-505 legend: B6 = alias GT1 (found once: luna + terra + wonder), B8 = alias GT3 (found in 2 runs) -> run-1 WRONG, run-2 right (run-2 does not print the GT mapping; the mapping is run1:248 = CR legend) |
| Valid-era start | source.md "first shipped 12:59:34" (run1:70) | "first valid run 13:02:27" (run2:33) | both in CR:373; consistent (ship time vs first run) |
| Current section of CR | lines 289-373 current; 375-383 rejected; 385-419; 421-428; 430+ (run1:37) | lines 289-506 supersede all above (run2:63) | CR:297 says "use only the tables below"; consistent, run-2 wider |
| Audit C skipped-source count | 156 of 665 (run1:112) | 156 of 665, with retraction of earlier 161 (run2:149) | CR:373 VERIFIED (156 = 81+49+6+15+4+1+0+0; 665 = 209+222+25+75+24+63+44+3) |
| Pilot | "2/16, 3/16, 4/16 ... sonnet alone PASSED both defect-rich plans" (run1:81) | "sonnet alone most efficient 2.15 catches per 100k tokens; 0/8 blocking" (run2:127) | PILOT-REPORT.md totals VERIFIED (2.15, 0.76, 0.66); "sonnet alone PASSED" [UNVERIFIED] |

### 3.7 Points where both agree independently (cmp:51-63, re-confirmed against code where possible)

| Point | Code/data check |
|---|---|
| Ceiling ~2-2.5 of 14 | CR:274, :371 (data); unchecked here beyond figures above |
| Default ember + 2x luna; sonnet + 2x luna optional; haiku + 2x luna best real blocking | CR:331, :378, :424-428 VERIFIED numbers |
| Merge drop (49 blocking, 4 flips) | 49 VERIFIED audit-D:8; "4" see 3.6 |
| 156/665 source-blind | VERIFIED CR:373 |
| One reviewer's `blocking` decides; no calibrator in this panel | VERIFIED `ledger.py:187, :273-274`; `_confidence` (`:86-90`) never read in `_decision`/`_brief_ids` |
| `T01.02` lost | VERIFIED direct call |
| `distinct_across_slots` silent duplicates | VERIFIED, see 4.2 P1 |
| Telemetry unwritten | VERIFIED with nuance (C12) |
| Branch changes no product code | `git diff --stat origin/master...HEAD -- src tests` claim at E2: [UNVERIFIED here on the E2 branch]; reproduced only for HEAD-vs-base on this branch |

## 4. Run-2 code claims checked against HEAD (50d4d2b9d)

Unchanged between base ec259f1b7 and HEAD (so run-2's line numbers are exact at HEAD): `RV/findings.py` (457 lines), `ledger.py` (494), `ledger_cmd.py` (137), `merge_cmd.py` (118), `telemetry.py` (447), `telemetry_cmd.py` (98), `data/review-panel.default.json` (13), `review-panel.live7.json` (15), `rules/prompts/document_review_loop_prompts.md` (74), `commands/spec-panel.md` (`## Review Loop` at 256-264, hard gate 266-268). Changed by #519: `__init__.py` (+3), `panel.py` 525 -> 707 (+206 per `git diff --stat`), `panel_cmd.py` 87 -> 129, `review-tiers.default.json` 32 -> 38 (+6, the `classes` map), plus 6 new `review-panel.reflect-*.json` and new modules `findings_v2.py` (304), `cluster.py` (487), `cluster_cmd.py` (197), `manifest.py` (534), `manifest_cmd.py` (240), `card_convert.py` (517), `verify_cmd.py` (184). `git diff --stat ec259f1b7 HEAD` over `panel.py`, `data/`, `ledger.py`, `findings.py`, `merge_cmd.py`, `telemetry.py`, `__init__.py`, `rules/prompts/`, `commands/spec-panel.md` lists 9 changed files (`__init__.py`, 6 new reflect templates, `review-tiers.default.json`, `panel.py`): "279 insertions(+), 12 deletions(-)", of which `panel.py` is +206.

### 4.1 Merge and ledger defects (run2:160-173)

| ID | Claim (run-2 cite) | HEAD evidence (exact) | Verdict |
|---|---|---|---|
| D1 | A finding whose `anchor`/`anchor2` is over 200 chars (after whitespace flattening) is dropped whole; claim >300, >8 refs, id >16, bad severity, MINOR+blocking likewise (`findings.py:104-110, :111-117, :118-120, :26, :96-101`) | `findings.py:79-87` `_check_flat` (lo/hi after `flat()`); `:90-121` `_check_finding`: id regex `:26`, severity `:96`, MINOR+blocking `:100-101`, anchor 12..200 `:104`, anchor2 12..200 `:107-110`, refs <=8 `:111-117`, claim <=300 `:118`; `parse_block` `:188-192` on error sets `ok=False`, appends the error and `continue`s (the line is not appended to `findings`). Direct call: `anchor='x'*201` -> "anchor must have at most 200 characters"; `anchor` 200 chars + `claim` 300 chars + 8 refs -> `None` (valid) | VERIFIED |
| D1 (master) | `findings_v2.py` keeps anchor and citation quote at 12..200 and claim at 300 (`findings_v2.py:80, :111, :126, :132, :136`) | `findings_v2.py:80` citation quote `_check_flat(c["quote"], "citation quote", 12, 200)`; `:111` claim `None, 300`; `:126` anchor 12,200 (no citations); `:132` anchor 12,200 (with citations); `:136` anchor2 12,200; refs <=8 at `:114-120`; `:128` citations 1..8 | VERIFIED line-for-line. D1's limit therefore exists in BOTH parsers at HEAD |
| D2 | Partial-panel failure invisible; merge refuses only when no reviewer has a valid block; warning keeps first error only; merged report prints only `block ok false` (`ledger.py:127-134, :150-157, :421-424`; `merge_cmd.py:117-118`) | `ledger.py:127-134` per-reviewer parse, `warnings.append(... first: {msg})`; `:150-157` `if not any(block_ok.values()): raise LedgerError`; `:421-424` `- {id}: report {path}, block ok {true/false}`; `merge_cmd.py:117-118` prints `printable` dict (warnings in JSON); `entries` (`:141-149`) store only `block_ok`, no dropped count or ids | VERIFIED |
| D3 | Docstring says invalid-block reviewer "is skipped for clearing"; clearing loop ignores `block_ok` (`ledger.py:112` vs `:254-258`) | `:112` "A reviewer with an invalid block is skipped for clearing but its parsable findings are kept."; `:254-258` loop over `ledger["rows"]` clears `resolved_check` rows when `lid not in members_by_lid` — no reference to `block_ok` | VERIFIED |
| D4 | Union-find over `same_defect` with 3-line tolerance chains distinct defects; same-reviewer findings merge; row keeps first member's anchor/claim (`findings.py:367-407`; `ledger.py:182-199`) | `findings.py:367-379` `same_defect` (fp+refs OR span overlap +-3 when refs intersect or both empty); `:382-407` union-find, no reviewer filter; `ledger.py:182-199` `first = group[0]`, `anchor/claim/category` from `first`, `blocking = any(...)` | VERIFIED |
| D5 | Ref mismatch splits one defect; refs scraped from free text (`findings.py:321-337, :373-378`) | `refs_norm` `:321-337` scans anchor, anchor2, claim and refs with `_REF_TOKEN`; `:373-374` `if ra & rb or (not ra and not rb)` | VERIFIED |
| D6 | Missing anchor kept with span None and section "none"; `anchor_status`/`anchor_ambiguous` computed, never read (`findings.py:349-358`) | `:349-358`; `grep anchor_status\|anchor_ambiguous src` -> only the two assignments at `findings.py:350-351` | VERIFIED. Rows with span None never match by span (`_spans` filters falsy at `:364`), only by shared fp+refs |
| D7 | `T01.02` not a ref (`findings.py:29`) | `_REF_TOKEN = \b(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*\|P[0-9])\b`; same idea in `telemetry.py:23` `_ID_TOKEN`; direct call loses `T01.02` | VERIFIED |
| D8 | Any single blocking finding fails the round; `confidence` computed, printed, never used (`ledger.py:86-90, :99-104, :187, :273-274`) | `:86-90` `_confidence`; `:99-104` `_brief_ids` uses only `blocking` + status; `:187` `any(m["blocking"])`; `:273-274` verdict; `confidence` appears in the report table `:435` only | VERIFIED |
| D9 | Refound row takes the current round's blocking call; one-reviewer re-review can downgrade (`ledger.py:210-218`; panel `apply_to`) | `:210-218` `current = any(...)`; `row["blocking"] = (row["blocking"] or current) if row["lid"] in refound else current`; `apply_to: ["first"]` in default and live7 json (line 7) and in `reflect-pre.json` (line 7) | VERIFIED (reflect templates have the same single-fixed-anchor re-review) |
| D10 | Cluster matches only the first existing row (`break`) (`ledger.py:165-171`) | `:165-171` | VERIFIED |
| D11 | `ledger revise` can run twice and remap spans twice; new text hash not stored (`ledger.py:301-347`, note only) | `:301-347`: sha check only of `--old` against `rounds[-1].doc_sha256` (`:308-314`); no new-text hash recorded; spans re-mapped unconditionally `:343-346`; `ledger_cmd.py:61-71` also applies even when `fm["ok"]` is false (reports `fixmap_ok`) | VERIFIED by reading (not executed) |
| D12 | `merge` always exits 0; `ledger verdict` maps 0/10/11 (`merge_cmd.py:117-118`) | `ledger_cmd.py:13` `EXIT_BY_DECISION = {"PASS": 0, "REVISE": 10, "ESCALATE": 11}`, `:109` `sys.exit`; `merge_cmd.py` ends after `click.echo` (no exit call) | VERIFIED |
| D13 | `--report` id missing from `--resolution` gets model None; resolution reviewer with no report not detected (`merge_cmd.py:94`) | `:94` `"model": models.get(rid)`; no cross-check loop | VERIFIED |

### 4.2 Panel, tier and telemetry defects (run2:176-188)

| ID | Claim | HEAD evidence | Verdict |
|---|---|---|---|
| P1 | `distinct_across_slots` silently falls back to duplicates when exclusion empties the pool (`panel.py:405, :408`); `@default`/`@live7` gateway resolve t3-1 and t3-2 both to Qwen; 26 of 40 `@live7` run ids hold a duplicate | Base lines 405/408 confirmed (`pool = [...] or candidates`). HEAD `resolve_slot` `:539-543`: `if not pool: if hard: raise ExclusionExhausted; pool = candidates` — silent fallback remains whenever `hard_exclude`/`strict_distinct` are not given. Executed at HEAD: `review panel resolve --template @live7 --env gateway --run-id run1 --kind first` -> `[(t1b-1 sonnet),(t2-1 muse-spark-1.3),(t2b-1 Qwen3.8-max),(t3-1 glm-5.3),(t3-2 Qwen3.8-max),(t4-1 haiku),(t4-2 luna)]` (duplicate Qwen, same as run1:115); with `--strict-distinct` the t3 slot is skipped (`skipped_slots` = `no model available for tier3 after exclusion`). Count over run ids `run1..run40` (gateway, kind first): `@live7` 30/40 and `@default` 18/40 have a duplicate model. The run ids behind run-2's "26 of 40" are not stated (code-panel.md:64 / tests-tools.md:37) | VERIFIED (defect + mechanism + fix flags); count 26/40 NOT reproduced (my id set gives 30/40; depends on run-id set) [UNVERIFIED] |
| P1 (master) | master adds `hard_exclude` and `strict_distinct` (`panel.py:506-519`) | `panel.py:508-509` params, `:515-519` docstring and `hard = set(hard_exclude) \| (set(exclude) if strict_distinct else set())`; `panel_cmd.py:53-62` options `--hard-exclude-class` (repeatable, expands through tier-file `classes`) and `--strict-distinct`; `resolve()` `:574-575`, `:633-635`, `:700-706` writes `skipped_slots` + `excluded{models,classes}` only when used | VERIFIED. Answers run-2 Q3: flags exist but are opt-in; default path (no flags) still duplicates silently |
| P2 | Gateway environment has empty `launch` map | HEAD `review-tiers.default.json:25-30` gateway env with `"launch": {}` (`:29`), note "dispatch mechanism per model not defined yet" (`:26`); `resolve` `:679` `launch.get(model)` -> null for gateway | VERIFIED (cited `tiers.json:19-24` at base = `:25-30` at HEAD) |
| P3 | muse-ember-1.0 not in tier data | `grep -rIl muse-ember src tests docs scripts` -> no file at HEAD; tier lists unchanged at `review-tiers.default.json:5-10` | VERIFIED |
| P4 | Excluded Qwen/glm still in tier lists; master `hard_exclude` may cover at call time | tier lists `:7-9` still contain `Qwen3.8-max`, `glm-5.3`; exclusion is by class via CLI flag only (`classes` map `:18-23`: `Qwen3.8-max: qwen`, `glm-5.3: glm`) | VERIFIED (data unchanged; call-time exclusion exists but nobody passes `--hard-exclude-class qwen/glm` in the default path) |
| P5 | Environment guessed from `$T3Model01`; TxModelNN slot variables not read (`panel.py:365-374`) | HEAD `:485-494` `select_env`: `--env`, `$SUPERCLAUDE_REVIEW_ENV`, `$T3Model01`, else `anthropic-only`; `T2bModel01` not in `RV` | VERIFIED |
| P6 | Re-review resolves to the single fixed anchor; both templates `apply_to: ["first"]` (`panel.py:449-454`, `review-panel.*.json:7`) | HEAD `panel.py:600-605` `if review_kind in panel["apply_to"]: order = fixed+rest else order = fixed`; all 8 packaged templates have `"apply_to": ["first"]` | VERIFIED |
| P7 | `round_robin` uses today's date when `--sequence` absent | HEAD `panel.py:623-628` `(sequence if sequence is not None else date.today().toordinal()) + i - 1` | VERIFIED |
| T1 | No product caller of `append_record`; `model.observed` has no producer | see C12: one manual CLI caller `telemetry_cmd.py:67`; no skill/command/script caller (`grep append_record\|review telemetry append` over `src scripts tests`); the reflect shadow flow (`sc-reflect-protocol/SKILL.md:340-349`) calls `review panel resolve`, `review manifest ...`, cluster, verify-citations — not telemetry append | VERIFIED with nuance |
| T2 | Telemetry strata hard-code sonnet/haiku (`telemetry.py:112-115`) | `STRATA = ("sonnet","haiku")` `:112-115`; `:267` rejects other strata | VERIFIED |

### 4.3 Briefs and prompt contract (run2:190-200)

| ID | Claim | HEAD evidence | Verdict |
|---|---|---|---|
| B-1 | Brief never names the source/driving document (`prompts:17-21, :32`; `run-reviewer.sh:15`) | `document_review_loop_prompts.md:15-21` values to fill = `{{CANDIDATE}}`, `{{BASELINE}}`, `{{PRIOR}}`, `{{N}}`, `{{IDS}}` (no source); `:32` "against the requirements it states"; tip `run-reviewer.sh:15` same sentence | VERIFIED |
| B-2 | Parser limits (claim<=300, refs<=8, id<=16, MINOR-not-blocking) not in prompt; anchor 12-200 is (`prompts:60`) | `:60` "`anchor` is 12 to 200 characters copied exactly"; claim "one sentence", refs "lists the requirement ids and section numbers" (no counts) | VERIFIED. Tip `run-reviewer.sh:17` brief says `unpassable-check` (B-6 fix) |
| B-3 | spec-panel "CRITICAL is blocking"; prompt grading sentence; code accepts CRITICAL non-blocking (`spec-panel.md:259`; `prompts:31, :60`; `findings.py:100-101`) | `spec-panel.md:259` "CRITICAL is blocking; a MAJOR ... is blocking only if it names a concrete wrong outcome"; `prompts:31` grading check; `findings.py:100-101` only MINOR+blocking rejected | VERIFIED |
| B-4 | Report ending conflict: spec-panel last line `verdict:` with Reviser brief above vs prompt last section `## Findings block` (`spec-panel.md:260, :263`; `prompts:58`) | `spec-panel.md:260` "a critique-mode report's last line is `verdict: PASS`..."; `:263` "Reviser brief just above the final `verdict:` line"; `prompts:58` "The last section of every review report is `## Findings block`" | VERIFIED; parser tolerance: `_HEAD_FINDINGS` any heading level, first match (`findings.py:31, :45`) |
| B-5 | No guidance on what to anchor for `missing-requirement`, uniqueness, whitespace (`prompts:60`; `findings.py:349-352`) | `prompts:60` says only "the text that is wrong"; `locate` first occurrence via `annotate` `:349-352` | VERIFIED |
| B-6 | Harness category `unpassable-ac` vs parser `unpassable-check` | tip `run-reviewer.sh:17` now `unpassable-check`; `findings.py:17` | VERIFIED (fixed in harness only) |
| B-7 | Reviewers are not told one blocking row from any reviewer fails the round (`prompts:62` vs `ledger.py:273-274`) | `prompts:62` "The verdict line stays the reviewer's verdict." | VERIFIED |

### 4.4 Contracts, configuration and counts (run2:81-93, :330-383)

| Claim | HEAD evidence | Verdict |
|---|---|---|
| 1.3 line counts: findings 457, ledger 494, merge_cmd 118, ledger_cmd 137, panel 525, panel_cmd 87, telemetry 447, telemetry_cmd 98, tiers 32, panel json 13/15, prompts 74 | `wc -l` HEAD: 457, 494, 118, 137, **707**, **129**, 447, 98, **38**, 13, 15, 74; base `git show ec259f1b7:... \| wc -l`: panel 525, panel_cmd 87 | VERIFIED for base; STALE@HEAD for panel.py, panel_cmd.py, tiers.json |
| findings-v1 location rules: any heading level, case-insensitive, first heading; single-token info string; >1 block invalid, last used; unclosed invalid but parsed (`findings.py:27, :31, :38-76`) | `:27` `_FENCE` info `([^`\s]*)`; `:31` `_HEAD_FINDINGS = ^#{1,6}\s+Findings block\s*$` with `re.M\|re.I`; `:143-158` multi-block and unclosed set `ok=False`; parsing continues `:159-195` | VERIFIED |
| Unknown keys accepted silently (code-merge.md:38) | `_check_finding` `:90-121` has no unknown-key check | VERIFIED. (At HEAD `findings_v2.py:84-149` adds `calibrated_confidence` rejection at `:96-97` and per-lens fields) |
| Ledger contract `review-ledger/1`; statuses; verdict/decision; merged report | `ledger.py:17` SCHEMA; `:19` STATUSES; `:184-202`, `:276-285`; `:93-104`, `:273-275`; `:408-494` | VERIFIED |
| Resolution contract `review-panel-resolution/1` with fields reviewer_id, slot_id, tier, alias, strategy, seed, model, fallback_depth, stand_in, fallbacks, launch (+ template/tiers versions + sha256, environment, run_id, review_kind) | `panel.py:27` schema id; `:666-681` reviewer entry now ALSO has `model_name` (`:675`); `:688-699`; optional `skipped_slots`, `excluded` (`:700-706`) | STALE@HEAD (one new field, two optional keys). Merge still reads only `reviewer_id` and `model` (`merge_cmd.py:76-79`) |
| Tier table (6 aliases) and environments (gateway, anthropic-only: opus, sonnet, haiku, fable; stand-in haiku for tiers 2, 2b, 3, 4) | `review-tiers.default.json:5-10`, `:24-37` (`:33`, `:34`) | VERIFIED (lines shifted +6 for environments) |
| Templates: `@default` t1b x1 fixed + t2 x1 random + t3 x2 random; `@live7` t1b, t2, t2b, t3 x2, t4 x2 | `review-panel.default.json:9-12`; `live7.json:9-14` | VERIFIED |
| Three harness fixes proposed (anchor limit, source path, keep identity audit/ladder) "none implemented in src" (run2:93) | HEAD `findings.py` unchanged (limits intact), `document_review_loop_prompts.md` unchanged, no E2 change in `src` | VERIFIED at HEAD |
| `git diff --stat origin/master...HEAD -- src tests` is empty on the E2 branch (run2:54) | not checkable from this worktree except via `git diff --stat ec259f1b7 6c0984326 -- src tests` | [UNVERIFIED] (not run; tip adds only `.dev/eval-workspaces` per commit subjects) |

### 4.5 Tests (run2:479-524)

| Claim | HEAD evidence | Verdict |
|---|---|---|
| 304 passed (13 files); per-file counts | HEAD: `uv run pytest tests/review + 6 skills files` = 829 collected, 828 passed, 1 skipped (8.19 s). Same-13-file subset collects 309 (cli 13, live7 15; other 11 files equal run-2's counts) | VERIFIED for base (arithmetic 126 + 178 = 304); STALE@HEAD (309) |
| 8.2 gap: exact length boundaries not tested | `test_review_findings.py:111-122` `test_field_validation` tests only `short` anchor, 201, 301, 9 refs; valid case has anchor2 only | VERIFIED. HEAD direct call confirms 200/300/8 accepted (not covered by a test) |
| 8.2 gap: no test that prompt limits equal parser constants | `test_review_rules_text.py` (5 tests) pins structure and the `## Findings block` sentence (`:67`), not constants | VERIFIED (not exhaustively: grep for `200`/`300` in `tests/review/test_review_rules_text.py` found none) |
| 8.2 gap: task-id refs `T01.02` untested | `grep -rn 'T01\.02\|T0[0-9]\.[0-9]' tests/review` -> no match | VERIFIED |
| 8.3 12 new test files on master | HEAD `tests/review` additionally has exactly: `test_reflect_cluster_pairs`, `test_reflect_consumer_inventory`, `test_reflect_stage0a_replay`, `test_review_card_convert`, `test_review_cluster`, `test_review_cluster_cmd`, `test_review_findings_v2`, `test_review_manifest`, `test_review_panel_exclusion`, `test_review_panel_reflect_profile`, `test_review_reflect_templates`, `test_review_verify_citations` (12) | VERIFIED. Coverage of 8.2 gaps by them [UNVERIFIED, not read] (`test_review_panel_exclusion` plausibly covers P1 flags) |
| run-1 claim: `unpassable-check` accepted category not covered | HEAD: only `test_review_card_convert.py:426` maps to it; no `findings.parse_block` test with it | VERIFIED |

### 4.6 Reflect contrast and reflect-side statements (run2:406-418, :451-461) — STALE@HEAD

| Claim | HEAD evidence | Verdict |
|---|---|---|
| `reflect-reviewer` is UC-2 (`SKILL.md:592`) | base `:592` has the row; HEAD `sc-reflect-protocol/SKILL.md:640` "`reflect-reviewer` \| 3A \| UC-2 \| Read-only Tier-2 heterogeneous deviation-audit reviewer..." | VERIFIED (line shifted +48) |
| Model selection = `ANTHROPIC_DEFAULT_*_MODEL` aliases (skill) and T2Model0N/T1Model0N (CLI): "a third registry" | HEAD `SKILL.md:127` still lists `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL`; `T2Model0|T1Model0` in `src/superclaude/cli/sprint/aienv.py`, `swarm/config.py`, `swarm/lenses/reflect_review.py`. BUT HEAD `SKILL.md:87` adds `--t2-engine legacy \| shadow` (default `legacy`; `panel` rejected "ships in Stage 3") and `:340-349` shadow steps resolve through `superclaude review panel resolve --template @reflect-pre --env anthropic-only --hard-exclude-class <executor class> --strict-distinct` -> tier-JSON registry is now consumed by reflect in shadow mode | STALE@HEAD (reflect side already uses the panel kernel in shadow; legacy path unchanged) |
| Reflect: no loop; finding unit = markdown table + file:line | HEAD adds findings-v2 with citations/`reflect_category`/`deviation_class`/`self_confidence`/`lens`/`channel` (`findings_v2.py:93-149`); shadow step 4 parses `## Findings block` per card (`SKILL.md:343`) | STALE@HEAD |
| Q1 (does `findings_v2` replace findings-v1 or run beside; does it still drop whole finding?) | `findings_v2.py:84-138` `check_finding` returns an error string for the line (same drop-on-violation contract; limits identical) -> beside, not replacing: `findings.py` and `ledger.py` unchanged; `merge_cmd` still imports findings-v1 path | partially answered by code: limits identical (VERIFIED); "replace vs beside" at the CLI level [UNVERIFIED, `cluster_cmd`/`verify_cmd` not read] |
| Q4 (reflect dispatch of non-Claude models; `reflect-reviewer` pinned to one model) | `src/superclaude/agents/reflect-reviewer.md:1-9` frontmatter `model: sonnet`, tools allowlist read-only; shadow step 2 says `model:` is copied from `reviewers[N].model` "never from the model the harness reports" (`SKILL.md:341`) | partly answered (the agent is pinned to `sonnet`; non-Claude dispatch not shown) [UNVERIFIED] |
| calibrator/validator agents exist | `src/superclaude/agents/{confidence-calibrator,evidence-validator,reflect-reviewer}.md` and `~/.claude/agents/` copies | VERIFIED |

## 5. Artifact inventory named by run-2 (run2:44-79), with checks and destination

| Artifact (run2 line) | Claim | Check | Dest. |
|---|---|---|---|
| Commit b4db265a8 "docs(eval): tasklist review panel model-combination study", 8,814 files (:48) | CP | `git log tip` contains b4db265a8 as an ancestor (7 commits on E2 not in master incl. it) [file count UNVERIFIED] | EVAL |
| 2d06a4382 batch 11 + issue tables, 445 files incl. COMBO-REPORT (:49) | CP | listed as ancestor [count UNVERIFIED] | EVAL |
| 4a22d7421 hand-off + tmp-scripts 55 files (:50) | CP | `ls-tree` at 4a22d74 and tip: 55 files under `tools/tmp-scripts` incl. 1 README | EVAL |
| "Untracked 3,041 files, 1,380 + 1,352 + 309, ~1.5 GB" (:53) | UC | Same figures as run-1; tip commit 6c0984326 later untracks 96 transcripts that "were committed by mistake" (changes the picture; not examined) | OPEN (DO8) |
| `COMBO-REPORT.md` 506 lines; lines 289-506 supersede (:63) | CP | tip `wc -l` = 506; CR:297 "use only the tables below"; CR:289 header | EVAL (method + final tables) |
| `PILOT-REPORT.md` (:64) | CP | 83 lines at tip (run-1 says 83) | EVAL (method) / DROP (luna numbers, CR:107) |
| `manifest.md` — "Line 5 'local, never pushed' is now stale" (:65) | CP | tip manifest.md:5 = "Worktree branch: ironbelly/eval-tasklist-review-panel (local, never pushed)" -> stale statement confirmed; 16 lines; GT sha256 lines 13-16 (3 hashes) | EVAL |
| `combos/SPEC.md` 152 lines: procedure 18-36 + append-only ops log (:66) | CP | tip `wc -l` = 152 | EVAL / OPS (ops log) |
| 3 `TASK-WF-*` package folders (:67) | CP; GT + candidates "reusable regression fixture" | ground-truth hashes in manifest.md:13-16 | EVAL (benchmark fixture, U18) |
| `arms/` (:68) | pilot arms + blind scoring layout | not opened | EVAL |
| `combos/` "106 row folders ... only 19 rows have RESULT.md" (:69) | | tip: 96 dirs directly under `combos/` (2 quarantine/outage-named); 19 `RESULT.md` files | folder count CONTRADICTED (96 vs 106); RESULT.md count VERIFIED (19) |
| `probe/probe.json` — alias serves first model only (:70) | Stage 0 probe | manifest.md:11 "Tier aliases serve only the first model of a tier, so they are NOT used" | CORE (R19/DM2) |
| `quarantine-pre-src-luna/` (:71) | audit only | CR:107 | DROP (audit only) |
| `tools/run-reviewer.sh` 87 lines; line 10 hard-codes `.dev/tasks/done/$PKG/source.md` (:72) | CP | tip: 87 lines; `:10` `SRC_EVAL=$(ls /home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/tasks/done/$PKG/source.md ...)` | EVAL / CORE (pattern: sandbox + identity + ladder guards) |
| `run-reviewer.sh.bad-launch`, `.unpassable-ac` (:73) | audit | not opened | DROP |
| `tools/tmp-scripts/` 55 files (:74): `judge-one.sh`, `anon-*.sh` reusable; `snap.py`, `drift-b3.py`, `rlog-r3.sh` point at `brainstorm-reflect-panel` | | VERIFIED 3 files (C4) | EVAL (`judge-one.sh`, `anon-*.sh`); DROP rest |
| `analysis/*.py`, `final-table.md`, `issue-table/`, `allsets/`, b7..b11 logs (:75) | scripts read `/tmp` | VERIFIED (C7) | EVAL (needs rewrite) |
| `analysis/audits/audit-A..F/` (:76) | six audits; only A and D have summary.md | VERIFIED (C3); audit-D read fully (90 lines) | EVAL (audit designs reusable) |
| `analysis/RAW-TRANSCRIPTS-NOT-COMMITTED.md` (:77) | | VERIFIED lines 1-4 (2,916 files) | OPEN |
| `/tmp/evalsb/repo`, `/tmp/audit-*/`, `/tmp/final-table.py`, `/tmp/*.log` (:79) | OUT; existence UNVERIFIED | `/tmp` is on the E2 author's machine, not here | EVAL (loses reproducibility if gone) |
| Branch freshness: 11 commits behind origin/master (:55) | | VERIFIED (11) | - |
| Source/test changes on E2 branch: none (:54) | | [UNVERIFIED] (see 4.4) | - |

## 6. Value inventory of the run-2 content (every finding, lesson, strategy, defect, decision, requirement), with proposed destination

### 6.1 Terms and metrics to standardise (run2:24-38, :393)

| Item | Destination | Note |
|---|---|---|
| "Real blocking /8" = judge credited through a blocking ledger row AND `blocking_in_implement=true`; "judge-blocking"; "wrong blockers"; "found /14"; "control found /2" | EVAL / CORE metric set | Judge-blocking overcounts (65 vs 38 over 71 rows, CR:291 VERIFIED); "wrong blockers" is biased by novel real finds (CR:75 per run-1; "known bias" run2:225) |
| Metric list: found /14, real blocking /8, judge-blocking, wrong blockers, control found /2, control wrong blockers, tokens, reviewer-seconds, elapsed, found and real blocking per 100k tokens (run2:393, CR:300-305) | EVAL | candidate pre-registered metric set (run2:262) |
| Valid era / src era, quarantine rules | EVAL | era boundary 2026-11-12 12:59:34 ship, 13:02:27 first valid run (CR:373) |
| B1-B8, I1-I8 labels | EVAL | mapping to GT ids = CR legend 401-417 (VERIFIED, B6 = alias GT1) |

### 6.2 Results R1-R21 (run2:114-136) — evidence strength, dependencies, destination

| # | Result (exact figures, source) | Strength | Dest. | Check |
|---|---|---|---|---|
| R1 | Every panel ~2-2.5 of 14; no row > 4/14; n=71 rows (CR:274, :371, :428) | hard ceiling, cause unknown (brief, packages, GT) | EVAL baseline | numbers per CR |
| R2 | Never found by any of 106 runs: B1, B2, I5, I6; B6 once (CR:431, :497, :501) | all-sets table, 0 mismatches of 320 cells | EVAL (hard-defect set) | VERIFIED CR:497 |
| R3 | B3 95/106, I8 76, I2 71 (CR:502) | dominates scores | EVAL | VERIFIED CR:503 |
| R4 | ember + 2x luna: 1.83/14, real blocking 0.17/8, wrong blockers 1.83, control 0.83/2, 63,644 tokens, ~6 min, n=6; reached only B3, B7, I2, I8 | replicated, cheapest | EVAL (regression target U18) | VERIFIED CR:331, :378 |
| R5 | sonnet + 2x luna: 2.33/14, real blocking 0.33, control 1.33, 139k tokens, 821 s, n=6; first run 4/14 was outlier; Fisher p ~0.012 post-hoc for I7 3/6 vs 0/6 | exploratory | EVAL | VERIFIED CR:424-426 |
| R6 | haiku + 2x luna: 1.2/8 real blocking, 2.2/14, 3.0 wrong blockers, 191k tokens, n=5 | best real blocking, not significant | EVAL | CR:367 [not opened] |
| R7 | ember + sonnet: 2.5/14, 0.25 wrong blockers, 0.25 real blocking, 143k tokens, n=4 | n=4 | EVAL | CR:368 |
| R8 | Only three effects survive audit F: second luna +0.83 control found (Welch 0.004, permutation 0.048, baseline all zeros); 2x luna + 2x ember 2.75-3.25 more wrong blockers (p 0.005-0.03); ember + terra -1.75 found (p 0.029) | fragile | EVAL | VERIFIED CR:298 |
| R9 | 5-reviewer panels: no catch gain for 2-4x cost | n=4 each | CORE (panel size guidance) | CR:286, :369 |
| R10 | Sonnet associated with rare issues: all 3 sets reaching I4, 3 of 4 reaching B5, 13 of 16 runs reaching I7 | association only | CORE (quality tier) | VERIFIED CR:505 |
| R11 | Single-run highs never replicated (grok + 2x haiku + sonnet 4/14, 594k tokens; haiku + sonnet + wonder 4/14) | n=1 | DROP as claims | CR:370 |
| R12 | Pilot: sonnet alone 2.15 catches/100k tokens, all arms 0/8 blocking | pre-source era | DROP (superseded) | VERIFIED PILOT:44-71 |
| R13 | Without source.md sol/terra "incomplete" with 0 findings and luna refused 25 of 25; after shipping every model produced blocking findings | harness gap | CORE (inputs must be named) | CR:106, :148 |
| R14 | 156 of 665 valid-era runs never referenced source.md: ember 81/209 (39%), luna 49/222 (22%), haiku 15/75, grok 4/24, wonder 6/25, sonnet 1/63, terra 0/44, sol 0/3 | cause UNVERIFIED (inference "brief never names source.md") | CORE (U4) | VERIFIED CR:373, sums reconcile |
| R15 | terra/sol: 51 reports incomplete incl. 16 empty terra reviews in valid rows | | CORE (model eligibility rules) | CR:294 |
| R16 | luna quotes verbatim in 91.4% of anchors vs 98-100% others | impact unmeasured | CORE (anchor repair, U2) | CR:294; run-2 does not say which audit [UNVERIFIED] |
| R17 | Presence effects (grok 2.62 vs 2.00; wonder 2.75 vs 1.98; sonnet 2.43 vs 1.92 and wrong blockers 1.95 vs 2.68; haiku blocking 1.30 vs 0.73; ember 1.88 vs 2.55) | strongly confounded | OPEN (hypotheses only) | CR:275 |
| R18 | Operational: Qwen timeout (3 x 3000 s pilot); glm slow 805-1435 s; muse misroutes under load; muse-spark and wonder-full misroute | model eligibility | OPS | PILOT:12; SPEC lines |
| R19 | Tier aliases serve only first model of a tier -> raw-id dispatch | Stage 0 probe | CORE (dispatch, U7) | VERIFIED manifest.md:11 |
| R20 | Merge drops findings: 80 reviewer-level cases, 49 blocking lost, 4 verdict flips (3 shown), per model luna 30, ember 33, wonder 14, glm 7, haiku 7, grok 1, sonnet/terra/sol 0 over 264 merges | measured by replay of parse rules (audit-D:15) | CORE (U1, U2) | numbers VERIFIED audit-D; mislabel + "4 flips" see 3.2 C15, 3.6 |
| R21 | Judging reliable: 294 clean judge outputs; blind re-judge 12/12; 19/19 confirmed, one borderline (recall 0.95); both judges Opus | | EVAL | VERIFIED CR:296 |

### 6.3 Retractions — every one is a DROP; keep as "do not reuse" list (run2:138-152)

11 rows, each VERIFIED to exist in CR via run-2's citations except where marked: (1) "n2-sonnet-src 8/14 and 5/8" (judge died on API error; re-judge 2/14, 0/8; CR:146-148; CR:132 still shows the headline text at tip -> stale text remains in the file, CR:297 declares supersession); (2) early per-model blocking counts (grep without space; CR:104-106 VERIFIED at CR:105); (3) "r2-sonnet-src is a muse-wonder row"; (4) "ember weaker than wonder"; (5) "second run of same model adds nothing"/"haiku overlap 8 of 8" (attrib.py membership credit; CR:195-200); (6) judge-blocking over denominator 8 (65 vs 38, CR:291 VERIFIED); (7) "second luna adds +0.5 blocking" reversed (0.50 -> 0.17); (8) 161 -> 156 skipped-source (CR:293 vs :373 VERIFIED); (9) "sonnet + 2x luna as standard" rejected (CR:383 vs :421-428); (10) batch-10 outage runs "not moved" (they were; SPEC:148 VERIFIED text); (11) all earlier tables superseded (CR:289, :297 VERIFIED).

### 6.4 Defects D1-D13, P1-P7, T1-T2, B-1..B-7, H1-H12 — destination per defect (checks in section 4)

| ID | One-line | Dest. | Status at HEAD |
|---|---|---|---|
| D1 | whole-finding drop on length limit; same limits in findings_v2 | CORE parser (repair/truncate, count drops) | OPEN in both parsers |
| D2 | partial-panel failure invisible | CORE merge | OPEN |
| D3 | clearing ignores `block_ok` | CORE ledger | OPEN |
| D4 | chained clusters (83 mega rows, 195/1,398) | CORE cluster | OPEN in `findings.cluster` (used by the ledger); `cluster_v2` flags chains but still builds them (`cluster.py:33-34`, docstring-read) |
| D5 | ref-mismatch splits | CORE cluster | OPEN in v1; `same_defect_v2` keeps the refs-intersect-or-both-empty rule (`cluster.py:30-32`, docstring-read) |
| D6 | unanchored finding rows (46, 13 blocking) | CORE anchor | OPEN in v1 |
| D7 | task ids not refs | TL (ref syntax per target) | OPEN; also in `telemetry.py:23` |
| D8 | any single blocking fails | OPEN (quorum/calibrator) | OPEN; relates to reflect calibrator/validator |
| D9 | re-review downgrade by single reviewer | CORE loop | OPEN, unexercised |
| D10 | first-match `break` | CORE ledger | OPEN |
| D11 | revise twice | CORE ledger | OPEN (read-verified) |
| D12 | merge exit 0 | CORE CLI | OPEN, low |
| D13 | missing report/resolution cross-check | CORE CLI | OPEN, low |
| P1 | silent duplicates | CORE panel | OPEN by default; opt-in `--strict-distinct` (HEAD) |
| P2 | empty gateway `launch` | CORE dispatch | OPEN |
| P3 | ember absent from tier data | OPEN (owner-controlled, SPEC:120) | OPEN |
| P4 | excluded models in lists | CORE panel data | OPEN in data; `--hard-exclude-class` exists |
| P5 | env guessed from T3Model01 | CORE panel | OPEN |
| P6 | re-review collapses to one anchor | CORE loop | by design; same in reflect templates |
| P7 | round_robin depends on date | CORE panel | OPEN, low |
| T1, T2 | telemetry unwired; strata hard-coded | CORE telemetry | OPEN |
| B-1 | brief has no source placeholder | CORE brief contract (U4) / TL | OPEN |
| B-2 | limits not in prompt; instruction alone did not hold | CORE | OPEN (lesson: enforce in parser, not only brief) |
| B-3 | blocking semantics triple conflict | CORE (decide once) | OPEN |
| B-4 | report ending conflict | SPEC | OPEN, low |
| B-5 | anchor guidance missing | CORE brief | OPEN |
| B-6 | `unpassable-ac` label | DROP | FIXED in harness |
| B-7 | merge consequence not told to reviewers | CORE brief | OPEN |
| H1 | cyclic ladder | OPS | FIXED harness (VERIFIED `:66-83`) |
| H2, H3, H4 | meta overwrite, attempt overwrite, presence-only BLOCK_OK | EVAL harness / CORE (U6) | OPEN in script (VERIFIED) |
| H5 | stale attempt files inflate 5 runs' cost | EVAL | disclosed |
| H6 | stale merges (n2-terra, r2-sol, n5-sol, n5-terra) | EVAL | disclosed; VERIFIED audit-D:23-25 |
| H7 | API-error judge left plausible score | EVAL | FIXED by procedure |
| H8, H9 | grep without space; `attrib.py` | DROP | FIXED / retracted |
| H10 | `/tmp` analysis scripts | EVAL | OPEN (VERIFIED) |
| H11, H12 | 12-worker identity bleed; claude binary replaced mid-run | OPS | mitigated |

### 6.5 Lessons and strategies (run2:221-267)

| Group | Items (13 worked / 10 failed / 9 next-time) | Dest. |
|---|---|---|
| Worked | GT from implement history; control package; blind scoring; reviewer sandbox; model identity from transcript; quarantine in place; replicates 4-6; six audits; two views AS-SCORED/AUDIT-CLEAN; dual independent counting (10 agents + script, 0 mismatches of 320 cells and 62 x 16); permutation tests; run scheduling with caps and cooldowns; append-only ops log | EVAL method (CORE for sandbox/identity/quarantine) |
| Failed | ranking single runs; ledger-membership attribution; literal grep; trusting a judge file; starting before an end-to-end harness check; cyclic ladder; high concurrency; tier aliases; one metric name for two things; `/tmp` analysis; superseded text left in place | OPS |
| Next time | one-package smoke test of reviewer -> merge -> judge; validate reports with the real parser at run time; name every input in the brief and check from transcript it was read; pre-register metrics and decision rule; plan replicates and power; keep raw identity evidence in committed meta; double-score a sample with a second judge family; self-contained analysis scripts; score raw union of reviewer findings as well as merged ledger | CORE (parser validation, input-read check), EVAL |

### 6.6 Decisions made (DM1-DM18) and open (DO1-DO11) (run2:271-308)

| ID | Decision / question | Who, when (UTC) | Source check | Dest. |
|---|---|---|---|---|
| DM1 | Qwen3.8-max excluded everywhere | Owner, 2026-11-11 | PILOT:12 | CORE panel data (P4) |
| DM2 | Dispatch by raw id with `claude -p`, not tier alias | coordinator, 2026-11-11 Stage 0 | VERIFIED manifest.md:11 | CORE (U7) |
| DM3 | Sandbox without implement history | coordinator | VERIFIED manifest.md:10 | CORE reviewer isolation |
| DM4 | `.catfix.md` normalisation | coordinator | SPEC:38-39 | DROP |
| DM5 | Tear down 12-worker batch 3, quarantine, serial rerun | Owner, 2026-11-11 22:43 | SPEC:77-85 | OPS |
| DM6 | Ship source.md next to candidate | Owner request 2026-11-12 | SPEC:90-95 | CORE (U4) |
| DM7 | glm excluded from batch 4 on | Owner 2026-11-12 14:42 | SPEC:97-98 | CORE panel data |
| DM8 | Quarantine all pre-source luna data | Owner 2026-11-12 15:16 | VERIFIED CR:107 | EVAL |
| DM9 | muse-ember replaces wonder; owner adding as Tier 04 Model 02 | Owner ~2026-11-12 17:57 | VERIFIED SPEC:118-120 text | OPEN (P3) |
| DM10 | Fallback ladder v2 then v3 guards | Owner then coordinator | VERIFIED SPEC:141 and `run-reviewer.sh:66-83` | CORE (U6) |
| DM11 | Replicate study (4 runs/combo) | Owner 2026-11-12 20:37 | SPEC:137-138 | EVAL |
| DM12 | Testing closed; batch 10 dropped | Owner 2026-11-13 01:09 | VERIFIED SPEC:146-147 quote "we're done testing, we're going to decide and run with it" | - |
| DM13 | Real blocking is the metric | Coordinator after audit F | VERIFIED CR:291 | EVAL |
| DM14 | Final panel guidance: default ember + 2x luna; quality tier sonnet + 2x luna only if control-GT1-like issues matter; haiku + 2x luna best real blocking; do NOT use ember + terra, 2x ember + 2x luna, terra or sol alone, haiku + ember + terra, any 5-reviewer panel, anything relying on muse-wonder | Owner direction recorded by coordinator, 2026-11-13 after batch 11 | CR:363-369, :428; measured on plan packages only (K3) | TL (plan-review defaults) |
| DM15 | Fix harness before more model testing (anchor limit, source path in brief, keep identity audit + ladder fix) | Coordinator recommendation | CR:371, :428 | CORE (U1, U2, U4, U6) |
| DM16 | Raw transcripts left out of commits | Owner 2026-11-13 | VERIFIED note line 2; tip commit 6c0984326 later untracks 96 committed transcripts | OPEN (DO8) |
| DM17 | Never stage `.claude/`; change nothing under `.dev/tasks/` | Owner standing | SPEC:33 | - |
| DM18 | No PR; push research branch to fork only | Owner 2026-11-13 | session record [UNVERIFIED] | - |
| DO1 | How to stop D1 (raise, truncate at merge, re-ask, keep and report) | Owner + review maintainer (and reflect, since findings_v2 has same limits) | VERIFIED limits in both parsers | CORE |
| DO2 | One broken reviewer invalidates the round or is printed? | Owner/panel maintainer | D2, D3 | CORE |
| DO3 | Keep any-single-blocking, or quorum/calibrator/validator | Owner after comparing reflect Tier 2 | D8 | CORE / REF |
| DO4 | How tasklist review runs: spec-panel loop + `superclaude review` (measured) or reflect UC-1 `--mode pre` (called today) | Owner + unification session | VERIFIED today's callers (C2) | OPEN (largest architecture fork) |
| DO5 | Put decided panels into product data (add ember, templates for ember+2x luna and sonnet+2x luna, remove/hard-exclude Qwen, glm) | Owner (tier list owner-controlled SPEC:120) | P3, P4 | CORE data |
| DO6 | Define gateway dispatch for named models | Owner/gateway maintainer | P2, R19 | CORE |
| DO7 | Re-run decided panels after harness fixes before adopting as defaults | Owner | DM15 | EVAL |
| DO8 | Raw transcripts: commit (LFS), archive, delete; reconcile 2,916 vs 1,689 | Owner | C6 | OPEN |
| DO9 | Replicate muse-wonder rows when quota returns | Owner (new study) | CR:284 | DROP-ish |
| DO10 | Wire telemetry | Panel maintainer | T1 | CORE |
| DO11 | Source/driving-document placeholder in the brief | Owner/prompt maintainer | B-1, R14 | CORE |

### 6.7 Product code the study exercised and "tasklist-specific?" (run2:81-93, :395-406)

| Component | Run-2 verdict | Check | Dest. |
|---|---|---|---|
| `findings.py`, `ledger.py`, `merge_cmd.py`, `ledger_cmd.py`, `panel.py`, `panel_cmd.py`, `telemetry*.py`, 3 data files, prompts file, spec-panel Review Loop | none tasklist-specific ("no 'tasklist' string in the module", code-merge.md:155; code-panel.md:189) | HEAD: `grep -rn tasklist src/superclaude/cli/review/*.py` not run [UNVERIFIED]; ref regex effectively plan-hostile (D7) | CORE |
| Reviewer brief | spec-shaped, scoped to `/sc:spec-panel --mode critique` (prompts:3) | VERIFIED `prompts:3` | SPEC + TL variants |
| Category `unpassable-check` fits plan ACs | | `findings.py:17` | CORE |
| Harness `run-reviewer.sh` | mostly generic; hard-coded path and spec-panel brief | VERIFIED `:10`, `:13-17` | EVAL |
| Panel recommendations DM14 | plan packages only; transfer to specs/code UNVERIFIED | K3 | TL only |

### 6.8 Questions and risks (run2:445-477)

| ID | Item | Check / answer available at HEAD | Dest. |
|---|---|---|---|
| Q1 | `findings_v2` replace or run beside findings-v1; still drops whole finding? | limits identical (VERIFIED `findings_v2.py:80,111,126,132,136`); `findings.py` untouched, so beside | CORE (answered in part) |
| Q2 | `cluster.py` replace `findings.cluster`; chain or split on refs? | Beside, not replace: `cluster.py:1` "Path-aware clustering of findings-v2 blocks (K4 cluster_v2)", pure function; `findings.cluster` (`findings.py:382-407`) untouched and used by `ledger.merge_round` (`ledger.py:165`). `cluster_v2` is still union-find (`cluster.py:33-34`) but marks a cluster "chained when two of its members do not match pairwise" and drops chained clusters from `cluster_agreement` (`:50-52`) — chaining is flagged, not prevented; `same_defect_v2` (`:30-32`) still needs `refs_norm` sets that intersect or are both empty (D5 persists); `cluster.py:64` imports `refs_norm` from `findings.py` so D7 (task ids lost) is inherited. Read from the docstring only; function bodies not read | CORE (partly answered) |
| Q3 | `hard_exclude`/`strict_distinct` remove silent duplicates and keep owner exclusions out? | Yes when passed (VERIFIED, P1); default path unchanged | CORE |
| Q4 | Dispatch of non-Claude models when `reflect-reviewer` is pinned (`model: sonnet`) | agent pinned to sonnet (VERIFIED frontmatter); non-Claude path not shown | OPEN |
| Q5 | Which finding unit wins: exact-quote anchor vs file:line | findings_v2 allows both (`citations` + optional `anchor`, `:122-138`) — i.e. the HEAD kernel already accommodates both | CORE |
| Q6 | Does reflect calibrator + validator reduce wrong blockers on the 3 packages (like-for-like run with the blind judge)? | no such run in the E1 material I read | EVAL (OPEN, high value) |
| Q7 | Tasklist review stays on reflect UC-1 or moves to the unified panel; advisory? | OPEN | OPEN |
| Q8 | Review loop (cap 3, revise, `resolved_check`) kept for spec-panel while reflect stays loop-free? | OPEN | CORE loop module |
| Q9 | Which model registry wins: tier JSON, `ANTHROPIC_DEFAULT_*_MODEL`, T2Model0N/T1Model0N | reflect shadow uses tier JSON; legacy uses aliases (4.6) | CORE |
| Q10 | muse-ember in gateway lists; tier JSON should follow ccsession (#518)? | `muse-ember` absent in all of `src tests docs scripts` at HEAD (VERIFIED); `ccsession-models.json` has none | OPEN |
| Q11 | calibrator 6-dimension vs reflect 5-dimension | not checked (code-panel.md:161) | OPEN |
| K1 | branch 11 behind; code cites describe base | VERIFIED; this worktree = the newer code | - |
| K2 | adopting findings_v2 limits carries D1 | VERIFIED (limits identical) | CORE |
| K3 | recommendations rest on 3 packages, n=4-6, ceiling | by evidence | TL |
| K4 | round 1 only was scored; D3, D9-D11 untested with real panels | VERIFIED audit-D:3 "all use ledger round 1 only" | EVAL |
| K5 | product panel cannot launch decided models (empty launch, no ember) | VERIFIED (P2, P3) | CORE |
| K6 | gateway behaviour silently changes reviewer | | OPS/CORE (U6) |
| K7 | 1.5 GB raw evidence only on one machine | tip later untracks 96 committed transcripts | OPEN |
| K8 | analysis scripts depend on `/tmp` | VERIFIED | EVAL |
| K9 | two hand-offs may disagree | now compared (section 3) | - |
| K10 | blocking semantics differ across files | VERIFIED (B-3) | CORE |
| K11 | telemetry strata hard-code | VERIFIED | CORE |

### 6.9 Test gaps (run2:503-520)

4 of the 14 gap rows were spot-checked at HEAD and are still gaps: exact length boundaries (`test_review_findings.py:111-122`), prompt-vs-parser constants (no `200`/`300` in `test_review_rules_text.py`), `T01.02` (no match in `tests/review`), `unpassable-check` through `parse_block` (only `test_review_card_convert.py:426`). The other 10 rows (malformed resolution, report id absent from resolution, duplicate reviewer id [code exists: `ledger.py:119-121` raises `LedgerError("duplicate reviewer id in one round")`; only the test is missing per run-2], all seven `@live7` models distinct, round 4+ / non-default `--cap`, broken-reviewer report text, valid-JSON-but-over-limit line vs clearing, partial-panel verdict flip, mega-cluster / ref-split / missing-anchor rows, `ledger revise` twice, any end-to-end multi-round run, `run-reviewer.sh` untested) were not re-checked against HEAD tests [UNVERIFIED]; #519 added 12 test files that may cover some (P1 flags certainly via `test_review_panel_exclusion.py`, not read). Dest.: CORE regression tests + EVAL.

## 7. Overlap-matrix cues (a): E1 / E2 / E3 by capability, from the run-2 hand-off plus HEAD

E2 column = what the hand-off claims/measures (E2 branch tip). E1 column = state at HEAD of this worktree (checked above). E3 column = what the hand-off says or does not say; hand-off run-2 says NOTHING about E3 installed variants (run-1 D14b/Q7 only).

| Capability | E1 (reflect kernel, HEAD) | E2 (tasklist eval + hand-off) | E3 (#346 loop, installed variants) | Overlap / gap |
|---|---|---|---|---|
| Finding wire format | `findings_v2.py` (304 lines): findings-v2 info string, adds `citations` (1..8, roles plan/spec/source/test/diff/artifact), `reflect_category`, `deviation_class`, `self_confidence`, `lens` (spec, reflect-pre, reflect-post), `channel`; reuses v1 `_ID`, `_check_flat`, `CATEGORIES`, `SEVERITIES` (`findings_v2.py:15-22`) | findings-v1 (exact-quote anchors 12..200, claim 300, refs 8) measured; D1 drop 92 findings, 49 blocking | spec-panel review loop emits findings-v1 (`prompts:56-62`); installed `spec-panel-ledger` etc. use the same ledger family [UNVERIFIED] | two parsers, identical drop-on-violation limits; E2 wants no silent loss (U1, U2) |
| Length limits | same as v1 (`:80, :111, :126, :132, :136`) | D1 = biggest measured loss (49 blocking lost) | same v1 | conflict candidate C-1 in section 9 |
| Clustering | `cluster.py` `cluster_v2`: path-aware, chain flag, calibrated support, `cluster_agreement` | `findings.cluster` over-merges (83 mega rows) and splits on refs | v1 ledger clustering | E1 flags chains; E2 measured damage; same union-find core |
| Verdict / blocking rule | cards carry no blocking flag in legacy reflect; v2 lines carry `blocking`; calibrated support, `disputed` (<0.5) in `cluster.py:48-49` | any single reviewer's blocking fails (D8); wrong blockers 1.8-4.75/row | ledger verdict any-blocking (v1) | E2 has no calibrator; E1 has calibration + validator; Q6 (like-for-like run) not done |
| Calibration / validation | `confidence-calibrator`, `evidence-validator` agents; `verify_cmd.py` citations | none in panel; study judge is eval-only | `finding-grader` (stoprule variant, installed only) | three different gate designs |
| Panel template / tier / environment | `panel.py` 707 lines; 6 reflect templates; `classes` map; `--hard-exclude-class`; `--strict-distinct`; `skipped_slots`/`excluded` | P1-P7: duplicates, empty launch, ember absent, Qwen/glm in lists, env guess | n/a | E1 already fixes P1/P4 opt-in; P2/P3/P5 still open |
| Model registry | tier JSON (shadow); `ANTHROPIC_DEFAULT_*_MODEL` aliases (legacy skill); T2Model0N (CLI) | aliases serve only first model; raw ids; `ccsession-models.json` divergence (run1 Q6) | n/a | three registries (Q9) |
| Dispatch of non-Claude models | `reflect-reviewer.md` pinned `model: sonnet`; `launch` null for gateway | raw-id `claude -p --model` harness works for luna/ember/haiku/grok/terra/sol | n/a | U7 unresolved; DM14 panels are mostly non-Claude |
| Model identity capture | shadow card header `model:` copied from `resolution.json` "never from the model the harness reports" (`SKILL.md:341`) — opposite direction | observed model from transcript `message.model` vs requested; mismatch invalidates (`run-reviewer.sh:51-56`); misroutes were real (muse served as terra) | n/a | conflict candidate C-5 |
| Telemetry | `telemetry.py`/`telemetry_cmd.py` unchanged; `manifest.py` (534 lines) adds a run manifest with stage advance | meta.json/cost.json/score.json harness-owned | n/a | telemetry still unwired; manifest is a new E1 record |
| Review loop (revise, re-review, cap 3, `resolved_check`) | not used by reflect (no fix loop) | measured round 1 only; D3, D9-D11 latent | the live loop on master (spec-panel `## Review Loop`, `ledger.py`) + installed ledger/diffgate/stoprule/ponytail/armb variants | loop module must keep U10 |
| Brief contract | reflect shadow adds one findings-block line to legacy briefs (`SKILL.md:342`) | brief never names source (B-1), limits unstated (B-2) | `document_review_loop_prompts.md` (74 lines) | shared brief contract is the E2 -> E1 hand-off point |
| Today's tasklist review entry points | reflect UC-1 `--mode pre` in sc:workflow (advisory) and sc:tasklist Stage 10.5 | measured the spec-panel loop on plan packages instead | n/a | DO4 / C2 |
| Benchmark / regression set | shadow-model-combos eval (`.dev/eval-workspaces/shadow-model-combos`, not in this slice) | 3 packages with GT (16 defects), blind judge, audits | n/a | both sides have an eval; sharing the judge/GT fixture is U18 |

## 8. Target-architecture inputs (d): run-2's U1-U18 mapped to shared core vs thin modules

| Req | Level | Proposed home | Evidence anchor | Note |
|---|---|---|---|---|
| U1 no silent finding loss; per-reviewer drop counts | Must | CORE parser/merge | D1, D2; audit-D:8, :16-19 | HEAD stores only `block_ok` (`ledger.py:141-149`) |
| U2 over-long anchors handled; same policy in v1 and v2 | Must | CORE parser | `findings.py:104-110`; `findings_v2.py:126-136` | single shared `_check_flat` already (`findings_v2.py:15-22`) -> one change point |
| U3 invalid reviewer visible in verdict; not counted as "not refound" | Must | CORE merge/ledger | D2, D3 | |
| U4 brief names every input by role; record whether read | Must (plan/tasklist) | CORE brief contract + TL | B-1, R14 | findings-v2 `citations[].role` already has plan/spec/source |
| U5 limits in brief + test pinning prompt vs parser | Should | CORE | B-2 | |
| U6 observed model identity captured, mismatch invalidates; fallbacks recorded, never overwrite, can be off | Must | CORE dispatch | R18, H1, H2 | see C-5 |
| U7 real dispatch path for named gateway models | Must (non-anchor tiers) | CORE dispatch | P2 | |
| U8 data can express decided panels (ember present; same model twice; Qwen/glm excludable) | Must if DM14 adopted | CORE data | P1, P3, P4 | |
| U9 plan/tasklist ids count as refs, or configurable per target | Should | TL module config | D7 | `refs_norm` shared by `cluster.py:64` |
| U10 keep loop guarantees (cap 3, Reviser brief only blocking ids, `resolved_check` only via revise, escalate at 3) | Must | LOOP module (SPEC; later others) | `prompts:13, :53, :70`; `spec-panel.md:261-263` | |
| U11 keep today's entry points' semantics (reflect `--mode pre` advisory; Stage 10.5 per phase, parallel, non-blocking) | Must | TL module | VERIFIED callers (C2) | |
| U12 documented verdict rule told to reviewers; quorum vs any-single-blocking; measure calibrator/validator against baseline | Should | CORE verdict policy | D8, B-7 | |
| U13 clustering must not chain unrelated findings; keep every member's claim | Should | CORE cluster | D4 | |
| U14 missing anchor reported and handled | Should | CORE anchor | D6 | |
| U15 verdict-bearing exit code for merge | Should | CORE CLI | D12 | |
| U16 telemetry written by product (requested + observed model, block_ok, dropped count, tokens, wall) | Should | CORE telemetry | T1 | |
| U17 per-reviewer model override at resolve time | Should | CORE panel CLI | SPEC:26 (jq rewrite) | |
| U18 regression benchmark: 3 packages + GT + judge + anonymisation as fixture; beat ember + 2x luna (1.83/14, 0.17/8, 1.83 wrong blockers, 0.83/2 control, ~64k tokens) | Should | EVAL | CR:366, :428 | |
| (gap) finding-shape coexistence/mapping | - | CORE | run1:265 requirement 1 dropped (L6); only Q5 | now concrete: v1 and v2 coexist at HEAD |
| (gap) reviewer isolation | - | CORE reviewer contract | run1:273 requirement 9 dropped (L7) | |
| (gap) calibration/validation gate position in the shared pipeline | - | CORE | Q6, Q11 | |
| (gap) target-specific lens/ref/category sets (plan, tasklist, spec, code) | - | modules | `findings_v2.py:36` LENSES = spec, reflect-pre, reflect-post only | no tasklist-review or code-review lens |

## 9. Conflict log candidates (c) and future-use-case exposure (e)

### 9.1 Conflicts surfaced by this slice

| ID | Conflict | Sides | Evidence |
|---|---|---|---|
| C-1 | Length-limit policy: E2 requires no whole-finding drop (U1, U2, DO1); E1's findings-v2 keeps drop-on-violation with identical limits | E2 hand-off vs E1 code | `findings_v2.py:111, :126, :132, :136` vs run2:426-427 |
| C-2 | "Tasklist review does not exist in workflow/tasklist skills" (run-1 D14) vs "it runs through reflect UC-1" (run-2) | run-1 vs run-2 | VERIFIED run-2 (C2) |
| C-3 | Where tasklist review should run: spec-panel loop + `superclaude review` (what E2 measured) vs reflect UC-1 `--mode pre` (what is called) | E2 measurement vs product wiring | DO4; `sc-workflow-protocol/SKILL.md:89`; `sc-tasklist-protocol/SKILL.md:1630` |
| C-4 | Blocking semantics: reviewer-asserted `blocking` (any single) vs calibrated support/disputed vs severity "CRITICAL is blocking" vs grading sentence | v1 ledger; E1 `cluster.py:48-49`; `spec-panel.md:259`; `prompts:31` | B-3, K10 |
| C-5 | Model identity source: E1 shadow copies `model:` from the pin "never from the model the harness reports" vs E2 requires the observed model from the transcript and invalidates mismatches | E1 `SKILL.md:341` vs E2 `run-reviewer.sh:51-56`, U6 | reflect-side consequence unknown; gateway misroutes proven (SPEC:116) |
| C-6 | Model registry: tier JSON vs `ANTHROPIC_DEFAULT_*_MODEL` aliases vs T2Model0N/T1Model0N vs ccsession `ccsession-models.json` (owner-controlled) | E1 / legacy reflect / ccsession | Q9, Q10; run1 Q6; `review-tiers.default.json` has no ember |
| C-7 | Panel defaults: E2 DM14 recommends non-Claude cheap panels (ember + 2x luna); E1 reflect templates use Claude anchors (anthropic-only resolves to sonnet/haiku/opus under strict distinctness, `review-panel.reflect-pre.json` description) and hard-exclude the executor class | E2 vs E1 | `review-panel.reflect-pre.json:5` |
| C-8 | Hand-off claims vs HEAD: run-2 attributes the 40-file change to #519 + #518; only #519 touches `RV` (3.2 C1) | run-2 / cmp:22 vs git | VERIFIED |
| C-9 | Per-model drop counts presented as blocking-finding losses (92 total vs 49 blocking) in run-1, run-2 and CR:292 | hand-offs vs audit-D | 3.2 C15 |
| C-10 | `HANDOFF-run1-vs-run2.md` states run-2 "catches four facts"; this slice finds run-2 itself carries errors (C1 attribution, 106 vs 96 folders, 55+README, flips count) | cmp vs this slice | 3.6 |
| C-11 | Evidence retention: DM16 raw transcripts left out vs tip commit "untrack 96 raw claude transcripts that were committed by mistake" vs run-2 K7 | E2 branch history | 3.2 C6 |
| C-12 | Standing-rule mismatch: E2 workers "change nothing under `.dev/tasks/`" (DM17) vs this repo's rule `.dev/tasks/` always staged | E2 vs this repo CLAUDE.md | run2:291; project CLAUDE.md (not a code conflict; process) |

### 9.2 Future-use-case exposure (e)

| Use case | Exposure found in run-2 + HEAD | Evidence |
|---|---|---|
| Spec review (brainstorm/design) | Brief and loop are spec-native (`prompts:3`, spec-panel Review Loop); `LENSES` includes `spec`; B-4 ending conflict and B-3 semantics already bite here | `findings_v2.py:36`; `spec-panel.md:256-264` |
| Tasklist / plan review | D7 task ids lost; B-1 no source; reflect UC-1 is today's path (advisory); DM14 only measured on plan packages (3, n=4-6) | C2, K3 |
| PR code review | Quote-anchor (exact text) vs file:line is open (Q5); v2 `citations` has `diff`/`test` roles and line ranges but no code-review lens; exact-quote anchors flatten whitespace so code would anchor badly [inference, UNVERIFIED]; reviewer isolation sandbox pattern (manifest.md:10) reusable; no calibrator in v1 loop (wrong blockers 1.8-4.75/row would be noise in PR comments) | `findings_v2.py:36-38, :62-80`; D8 |
| rf-qa replacement | The review loop's re-check already defers to rf-qa Fix Cycle steps 1-5 (`spec-panel.md:262`); loop guarantees U10 and `resolved_check` ledger are the machinery a rf-qa replacement would reuse; re-review collapses to one anchor reviewer (P6) and a single reviewer can downgrade a blocker (D9) — risky for a QA gate | `spec-panel.md:262`; `ledger.py:210-218`; `panel.py:600-605` |
| Any new target | Ref syntax (`_REF_TOKEN`, `telemetry.py:23`), category set (`findings.py:15-22`), brief placeholders and per-target defaults are hard-coded to spec-shaped docs; model recommendations (DM14) do not transfer without re-benchmark (K3, U18); telemetry strata hard-coded sonnet/haiku (T2) | cited |

## Summary

**What the material is.** Run-2 (543 lines) is a single-author, independently written, spot-verified hand-off of E2's tasklist Review Panel study (3 plan packages, 16 GT defects, 106 scored runs / 71 valid-era rows) plus a defect list against the product review code, 18 requirements (U1-U18), 11 questions and 11 risks. Run-1 (315 lines, unchanged since 4a22d7421) is the earlier, context-rich version. E2's own comparison (`HANDOFF-run1-vs-run2.md`, 67 lines) prefers run-2 and lists 5 run-1 items to keep.

**Counts of what this slice lists:** 11 form differences (3.1 F1-F11); 15 corrections or new facts run-2 makes over run-1 (3.2 C1-C15, of which 5 reverse or materially fix run-1: C1 master moved, C2 tasklist review runs through reflect UC-1, C3 only 2 audit summaries exist, C5 three open harness bugs, C13 T01.02 verified); 12 run-1 items dropped or weakened by run-2 (3.3 L1-L12); a defect-ID crosswalk of the 16 run-1 defects plus a row for run-2-only items (3.5); 8 numeric disagreements (3.6); 14 + 10 + 7 claim rows checked in code for merge/ledger, panel/tier/telemetry and brief (4.1-4.3) and 20 more for contracts, tests and reflect (4.4-4.6); 21 results, 11 retractions, 41 defect/harness items (13 D + 7 P + 2 T + 7 B + 12 H), 18 decisions, 11 open decisions, 18 requirements, 11 questions, 11 risks and 14 test gaps inventoried with a destination.

**Code verdict at HEAD (50d4d2b9d):** all 13 merge/ledger defects D1-D13, panel/tier P1-P7, telemetry T1-T2 and brief B-1..B-7 are VERIFIED against `findings.py`, `ledger.py`, `ledger_cmd.py`, `merge_cmd.py`, `panel.py`, `telemetry.py`, the tier/panel JSON, the prompts file and `spec-panel.md` (the first six unchanged since base ec259f1b7, so run-2's line numbers are exact; `panel.py`, `panel_cmd.py` and `review-tiers.default.json` shifted). Run-2's "newer master (grep only)" statements are VERIFIED line-for-line for `findings_v2.py` (`:80, :111, :126, :132, :136`), `hard_exclude`/`strict_distinct`, the `classes` map, 6 reflect templates, 7 new modules and the 12 new test files. The key consequence: **D1 (whole-finding drop on length) exists in both parsers at HEAD** (v2 reuses v1 `_check_flat`), P1 duplicates persist on the default resolve path, ember and the gateway launch map are still missing, and D7 (task ids lost) is inherited by `cluster.py` through `refs_norm`.

**Hand-off errors found by this slice:** (1) run-2 and cmp:22 attribute the `RV` changes to #519 + #518; #518 changes no `RV` file (1 test file only); (2) run-2 "106 row folders" under `combos/` vs 96 directories at tip (106 is the scored-runs figure); (3) run-2 "55 files + README" vs 55 files including the README; (4) "4 verdict flips" is not reproduced by audit-D:20 (3 flips + 5 total-loss merges); (5) run-1, run-2 and CR:292 present per-model drop counts (luna 30, ember 33, ...) next to "49 blocking lost" although they sum to 92 = all dropped findings (audit-D:16-17); (6) run-1 "alias GT3 found once" is wrong (B6 = alias GT1; CR:497, legend CR:401-417); (7) run-1 D14 first half is contradicted by `sc-workflow-protocol/SKILL.md:89` and `sc-tasklist-protocol/SKILL.md:1630`; (8) run-2's reflect contrast (5.6) and Q4/Q9 are STALE at HEAD because reflect already has a shadow engine that resolves its panel through the tier JSON (`sc-reflect-protocol/SKILL.md:87, :340-349`).

**Architecture signal.** Both hand-offs agree the generic merge/ledger/panel code is target-agnostic and that the loss and source-blindness defects (D1, B-1) dominate measured scores. At HEAD one shared change point exists for D1 (`findings.py:_check_flat`, imported by `findings_v2.py:15-22`). The open forks the hand-off hands to the unification design are DO3/D8 (verdict rule), DO4 (tasklist review entry point), Q5 (quote anchors vs file:line citations, now both representable in findings-v2), Q9/Q10 (registry owner) and C-5 (identity from pin vs from transcript).

## Gaps and Questions

### Gaps (not verified or not read)

| # | Gap | Why |
|---|---|---|
| G1 | The raw notes `handoff-notes/run1/*.md` and `run2/*.md` (cited as `code-merge.md:n`, `code-panel.md:n`, `tests-tools.md:n`, 118 KB together) were not read; every claim whose only source is those notes (D11 beyond my read, T1 `code-panel.md:94-95`, P6/P7 `code-panel.md:30-31`, reflect contrast `code-panel.md:143-163`, 8.2 rows citing `tests-tools.md:33-40`) is verified only where I read the code myself | outside assigned material |
| G2 | `ledger revise` double-apply (D11) verified by reading, not executed | read-only constraint on mutating ledgers |
| G3 | `findings_v2.py` function bodies beyond lines 1-149, `cluster.py` bodies, `verify_cmd.py`, `manifest.py`, `card_convert.py` not read; Q1-Q3 answers rest on docstrings and the first 149 lines of `findings_v2.py` | scope |
| G4 | Run-2's "26 of 40 `@live7` run ids hold a duplicate" not reproduced (my `run1..run40` set gives `@live7` 30/40, `@default` 18/40 on the gateway env, kind first); the id set behind 26 is not in the hand-off | id set unknown |
| G5 | E2 data claims only spot-checked (COMBO-REPORT lines 105-107, 132, 146-148, 195-200, 289-298, 331, 373, 378, 401-417, 421-428, 497-505; PILOT 44-71; SPEC 118-121, 141, 146-148; audit-D full). Not re-checked: R6/R7/R11/R17 figures, 8,814 / 445 / 3,041 file counts, the 1,689 raw-transcript sum, `snap.py` writing into the other worktree, SPEC lines 77-85, 97-103, 130-131, 137-138 | cost |
| G6 | "Branch changes no product code" for E2 (`git diff --stat origin/master...HEAD -- src tests` empty) was not re-run on the E2 branch; commits after 4a22d7421 (c2ddeb1b4, fd69a006d, d561461fa, 6c0984326) were not diffed for `src/` changes | outside slice |
| G7 | Run-2 session-record claims (DM1, DM7, DM12 quote, DM16, DM18; "owner direction" for DM14) are unverifiable from files (DM12's quote IS in SPEC:147) | session records |
| G8 | Orchestrator/model claims in cmp:8-9 (Tier 1b Sonnet vs Tier 1a Opus; agents pinned to Opus) | only the comparison file says so |
| G9 | E3 (#346 loop, installed-only variants) is nearly absent from run-2; only run-1 D14b/Q7 mention it. This slice confirmed placement (installed in `~/.claude`, builds under `.dev/experiments/346-validation/phase5/final-bundle/builds/`, absent from `src/`) but did not read the variants | outside material |
| G10 | The "tasklist-specific?" verdicts (run2:395-406: "no 'tasklist' string in the module") not re-grepped | cost |

### Questions for the main agent / owner

| # | Question | Needed for |
|---|---|---|
| Q-A | Treat run-2 as the baseline hand-off with the corrections in 3.2/3.6 applied, and keep the 5 run-1 items (L1, L2, L3, L4, L5) plus L6/L7 (finding-shape mapping, reviewer isolation) as requirements? | value inventory (b) |
| Q-B | Is the E2 tip's post-hand-off material (`panel-process-redesign`, `panel-collaboration` designs, c2ddeb1b4..6c0984326) covered by another slice? Run-2's U-list predates it | completeness |
| Q-C | Should the report assert D1 as already present in E1's findings-v2 (VERIFIED), and make "one shared `_check_flat` policy" the first shared-core item? | (d) |
| Q-D | Is a like-for-like run of reflect UC-1 (calibrator + validator) over the 3 E2 packages with the E2 blind judge in scope as a recommended next step (run-2 Q6; no such run found in the E1 material I read)? | (b), (d) |
| Q-E | Identity policy (C-5): should the shared core record both the pinned model and the observed model, and which one gates? | (c), (d) |
| Q-F | Who owns `muse-ember-1.0` in tier data (owner said "adding as Tier 04 Model 02", SPEC:120; absent from `src tests docs scripts` and from `ccsession-models.json` at HEAD)? | P3, DO5 |
| Q-G | Should the corrections in 3.2 (C1, C15) and 3.6 (8 rows) be sent back to the E2 session, or only recorded here? | (c) |

**Status:** Complete.

