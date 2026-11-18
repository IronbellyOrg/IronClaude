# Research Completeness Verification (Gate 1, Partition A, completeness lens)

**Topic:** which ONE unified central Review Panel (shared core plus thin modules) captures all the value of E1, E2 and E3
**Date:** 2026-11-14
**Files reviewed:** research/01-overlap-capability-matrix, 02-finding-contract, 03-merge-ledger-verdict, 04-dispatch-identity-tiers, 05-input-delivery-brief, 06-reflect-two-engines, 07-e1-evidence-grading, 08-e2-evidence-grading (8 files), plus research-notes.md and qa/phase2-output-inventory.md as references
**Lens:** completeness (coverage, completeness, cross-reference) with gate focus (a)-(e)
**Depth tier:** Deep
**Status:** Complete
**Verdict:** PASS (0 blocking, 7 minor)
**Agent:** rf-analyst, Gate 1 (research completeness gate), Item 3.01, partition A (files 01-08). Report-only (fix_authorization: false); no research file or the task file was modified.

---

## Method

- Read the Phase 2 output inventory and `research/research-notes.md` (EXISTING_FILES, PATTERNS, AMBIGUITIES_FOR_USER, and the SUGGESTED_PHASES row of each assigned file: topic, slices, open items).
- Read every assigned file completely (01: 277 lines, 02: 254, 03: 284, 04: 231, 05: 193, 06: 384, 07: 124, 08: 184; total 1,931 lines, equal to the inventory's partition A total).
- Read the `## Gaps and Questions` section of all 12 scope slices and mapped the items that fall in the topic of the 8 files to (a) a resolution in the file, (b) a Gaps entry in the file, or (c) a ledger row in files 19-24 (grep).
- Independent re-verification (read-only; no checkout, fetch, pull, stash, commit or push; Python only via `uv run --no-sync`; no file written in the repo; `git status --short` at the end shows the same four untracked paths as at session start):
  - About 95 line citations at HEAD `50d4d2b9d` (findings.py, findings_v2.py, ledger.py, contract.py, ensemble.py, panel.py, panel_cmd.py, cluster.py, card_convert.py, telemetry.py, document_review_loop_prompts.md, spec-panel.md, sc-reflect-protocol SKILL.md, tiers JSON, installed variant scripts, reflect agents, runner/config/commands, tests) match what the files state (table in "Independent verification log").
  - E2 tip `6c0984326` through `git show` / `git ls-tree` / `git diff-tree` only.
  - E1 evidence recount with read-only scripts.
- Not re-run by me: `pytest tests/cli/reflect` (352 passed per file 06; not needed for this gate), live gateway calls, raw transcripts (not committed anywhere).

## 1. Completeness (checklist item 2)

| Research file | Status | Summary | Gaps and Questions | Key Takeaways | Stale-doc section | Rating |
|---|---|---|---|---|---|---|
| 01-overlap-capability-matrix.md (277 lines) | Complete | Y (L276-277) | Y (L253-263, 10 items) | Y (sections 1-4; none for 5-6, Summary covers them) | Y | Complete |
| 02-finding-contract.md (254) | Complete | Y (L252-254) | Y (L209-240, 13 gaps + negative evidence) | Y (sections 1-9) | Y | Complete |
| 03-merge-ledger-verdict.md (284) | Complete | Y (L281-283) | Y (L260-271, 10 items) | Y (1.1, 1.2, 1.3-1.4, 2, 3, 4) | Y | Complete |
| 04-dispatch-identity-tiers.md (231) | Complete | Y (L229-231) | Y (L207-217, 9 items) | Y (sections 1-8) | Y | Complete |
| 05-input-delivery-brief.md (193) | Complete | Y (L191-193) | Y (L172-182, 9 items) | Y (Units 1-7; Unit 8 is a table with no takeaway line) | Y | Complete |
| 06-reflect-two-engines.md (384) | Complete | Y (L382-384) | Y (L343-359, 13 items) | Y (sections 1-6, 8) | Y (table) | Complete |
| 07-e1-evidence-grading.md (124) | Complete | Y (L120-122) | Y (L92-109, gaps G-1..G-8 + questions Q-1..Q-5) | Y (section 5) | Y | Complete |
| 08-e2-evidence-grading.md (184) | Complete | Y (L181-183) | Y (L161-172, 10 items) | Y (per section) | Y | Complete |

All 8 files have `Status: Complete`, a Summary, a Gaps and Questions section and Key Takeaways. This matches the inventory (`qa/phase2-output-inventory.md` lines 8-15). No file is `In Progress`.

## 2. Coverage audit (checklist item 1): open items of research-notes.md per file

| File | Open items from SUGGESTED_PHASES | Where resolved | Status |
|---|---|---|---|
| 01 | classify each cell identical / superset / conflicting / unique across 15 capabilities | section 4 (15 capabilities x E1, E2, E3s, E3i; adds the label "absent", disclosed in 4.1 and Gaps 10) | COVERED |
| 01 | E2 commits after the hand-off (c2ddeb1b4, fd69a006d, d561461fa, 6c0984326) change no product code (slice 01 G6) | section 1.1; I re-ran `git diff --stat 4a22d7421 6c0984326 -- src tests` (empty) and `git log` (the same 4 commits) | COVERED, re-verified |
| 01 | E2 `snap.py` writes into E1's evidence tree | section 1.2 (path L4 confirmed by me through `git show`; "who ran it" tagged [UNVERIFIED]) | COVERED |
| 02 | does v2 `check_finding` reject unknown keys such as `origin` (slice 07 Q7, slice 08 gap 5) | section 3 (static read + execution; the v2 function is `check_finding`, there is no `_check_finding`) | COVERED |
| 02 | effect of truncate / reject / re-ask on the 92 / 49 figures | section 5 (units re-derived; truncation addresses 88 of 92 and 48 of 49; I recomputed 92, 49, 44 triples, 3 flips) | COVERED, re-verified |
| 02 | tasklist id grammar `T01.01` | section 4 (legal `_ID`, not matched by `_REF_TOKEN` / `_ID_TOKEN`) | COVERED |
| 03 | which test pins encode defects as behaviour | section 2 | COVERED (see minor finding M-1 on one count) |
| 03 | relation of installed variant scripts to `cli/review/ledger.py` (slice 09 gap 1, slice 02 gap 9) | section 3 (stdlib only, no import, no shared schema string) | COVERED |
| 03 | reproduce D-1, D-2, D-11 read-only | section 1 (scratch under `/tmp`, nothing written in the repo) | COVERED |
| 04 | does `muse-ember-1.0` exist at HEAD (slice 01 Q-F) | section 7 (absent from src, tests, docs, scripts, plugins, README, CHANGELOG and `ccsession-models.json`; present only in E1 PLAN.md, E2 evidence and the live env as `T4Model04`) | COVERED |
| 04 | how `panel.py:80-136` limits `reflect-*` templates (slice 02 gap 8) | section 2 (I re-checked `panel.py:71-73, 130, 143-145, 153-155, 252, 588, 595, 679` and `panel_cmd.py:79, 124`) | COVERED, re-verified |
| 04 | what records the served model | section 4 (nothing in product code; transcript only) | COVERED |
| 04 | `T2bModel01` and `ccsession-models.json` / `test_ccsession_tiers.py` | section 6 (18 in 11 files, re-derived by me) | COVERED, re-verified |
| 05 | what the core must expose per module | Unit 8 | COVERED |
| 05 | the claim that the brief never names `source.md` (slice 02 Q-F) | Unit 3 and Unit 6 (true for families 1, 2; not for the reflect brief; I read `run-reviewer.sh:9-17` through `git show`) | COVERED, re-verified |
| 05 | CB-1..CB-5, B-1..B-7, H1-H4, reflect brief heading, spec-shape coupling | Units 4, 5, 7 | COVERED |
| 06 | what must stay byte-identical; which EV-1 failures are mechanical; 0.75 vs 0.80; which engine to absorb | section 8 (a)-(d) | COVERED |
| 06 | run `reflect_shadow_exit.py` and the reflect tests to re-confirm `OVERALL: FAIL (13 of 20)` and 352 passed | section 0; I re-ran the exit script (identical lines); the pytest figure was not re-run by me | COVERED, partly re-verified |
| 06 | `SKILL.md` ranges not read by slice 10 (L508-L621, L872-L935, L1047-L1203, L1293-L1708, L1740-L1849) | section 5 header lists them as read | COVERED |
| 06 | whole `cli/reflect/` | `runner.py` L120-L440 and L620-L686, `config.py` L1-L235, most of `commands.py` and `fallback.py` L110-L594 were not read; logged in Gaps 6 | PARTIAL, logged (see minor finding M-5) |
| 07 | recount 15/15 published, 4,119,747 tokens, 216 clusters / 7 multi-reviewer, TP 21 FP 4 FN 1 TN 24; grade each finding; what it does not show | sections 1-3 (the "7" is corrected to "7 unchained multi-reviewer of 13"; I reproduced 216 / 13 / 6 chained / 7 unchained) | COVERED, re-verified |
| 07 | thresholds T-1..T-10 and the pilot stop rule approved? | section 4 (no approval found; only the T-9 redefinition) | COVERED |
| 08 | recompute pilot cells and `three-way.py` figures | sections 1, 4 | COVERED |
| 08 | resolve the unit of "92 / 80 / 49" and the 3-vs-4 verdict flips (slice 03 gap 6) | section 5 (92 findings, 80 reviewer runs, 49 blocking findings; 3 flips) | COVERED, re-verified |
| 08 | does batch j1 invalidate "not confirmed" (slice 04 Q5) | section 6 (no; exploratory, S2) | COVERED |
| 08 | counts whose sources disagree (96 / 97 / 106 / 107; 19 / 29; 428 / 417; Qwen 3 vs 4) | section 2 (I re-ran the first three with `git ls-tree`: 96, 29, 417) | COVERED, re-verified |

Coverage of slice gaps outside the files' own open items: every slice gap that falls in the topic of files 01-08 is resolved in a file, logged in a Gaps section, or carried as a ledger row (examples found by grep: slice 03 gap 7 -> VL-20-249 / VL-20-602; slice 04 Q2 "70 rows" -> VL-20-706; slice 02 gap 7 `r19` / hashes -> VL-19-620 / VL-19-632 / VL-19-873). No unrouted slice gap found in the topic of these 8 files.

## 3. Gate focus (a)-(e)

### (a) Every kept claim has file:line / git path:line evidence or an explicit [UNVERIFIED] tag
Each file defines its tag legend at the top (01: [CODE-VERIFIED] / [CV], [UV]; 02, 03, 04, 06: [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED]; 05: adds [SLICE-ONLY] "treated as [UNVERIFIED]", [RUN]; 07, 08: [RECOMPUTED]). Claims taken from slices carry the slice id and a tag; numbers not re-derived are marked. Sampling result (about 95 citations re-read by me, see section 7): zero wrong line numbers, zero wrong counts. Evidence rows with a weak tag are explicit, for example 01 Gaps 1-6, 02 Gaps 1-9, 03 Gaps 1-4 and 8, 04 Gaps 1-5, 05 Gaps 1-6, 06 Gaps 2-10, 07 G-1..G-8, 08 Gaps 1-8. PASS for (a). Cosmetic points are in the minor findings (path-less citations, tag abbreviations).

### (b) Open items of research-notes.md and slice gaps resolved, logged or carried
See section 2. PASS for (b); one partial coverage statement (file 06, `cli/reflect/` not read whole) is logged by the author under Gaps 6 and every claim that depends on the unread ranges is tagged as slice-sourced. Graded minor (M-5).

### (c) No run-1 contamination
- Exact-string search over `research/0[1-8]-*.md` for `review-panel-unify`, `UNIFY-RUN2-QUEUED`, `RUN2-QUEUED` (case-insensitive): one hit, `05-input-delivery-brief.md:189`, a sentence that states the independence rule ("No content or citation from the forbidden run-1 folder or the RUN2-QUEUED note was read or used"). Allowed by the gate definition. The folder name `TASK-RESEARCH-review-panel-unify-20261113-155942` and the path `REVIEW-PANEL-UNIFY-RUN2-QUEUED.md` appear in none of the 8 files.
- Search for phrases that would quote the run-1 report or note (`run-1 research`, `previous research run`, `run-1 report`, `RESEARCH-REPORT-review-panel-unification.md`): no hit in the 8 files.
- Citations in the 8 files point only to HEAD source, `.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/` (E1 Stage 0 package, not forbidden), E1/E2 evidence trees, `.dev/brainstorms/` (E1 and E2), and installed `~/.claude` files. None is under the forbidden folder.
- The recorded slip (scope slice 03 gap 10, slice 03 line 564) is in the scope slice, not in the 8 files; none of the 8 files cites it as evidence.
PASS for (c).

### (d) Every value-ledger row has exactly one destination
Not applicable to partition A: files 01-08 contain no `VL-nn-nnn` rows (value ledgers are files 19-24, partition C). Not assessed here.

### (e) No claim builds on a [CODE-CONTRADICTED] / [UNVERIFIED] row of research-notes.md AMBIGUITIES_FOR_USER as if it were fact
Checked each of the 13 [CODE-CONTRADICTED] rows and the 8 [UNVERIFIED] bullets against the 8 files:
- #519 + #518 attribution: 01 section 1.3 repeats it only to contradict it (I re-ran `git diff-tree`: #518 touches 0 files under `cli/review` and 1 under `tests/review`).
- Reflect contrast: 01 section 2 splits it correctly (true for the code-driven path, false for the product).
- alias GT3 / GT1: 08 section 3 reproduces the legend; correct.
- `COMBO-REPORT.md:292` "no error" / "four flips" / per-model figures as the 49: 02 section 5.1 and 08 section 5 contradict them with evidence (I recomputed all).
- "16 empty terra reviews": 08 section 5 (14 terra + 2 luna).
- `unpassable-ac`: 05 Unit 5 (harness-only typo, never shipped).
- `T2bModel01` "not referenced": 04 section 6 (18 in 11 files).
- `theory.py` HARD set: 05 Unit 5 (I read `theory.py:8` and `gtproxy.py:91-93`; set and groups as stated).
- memory line 64 (fenced yaml calibration not parsed): 02 section 6.1 documents `cluster_cmd._embedded_calibration`; 07 E1-F18 keeps it [UNVERIFIED]. Neither uses it as fact.
- `[UNVERIFIED]` bullets: unit of 92/80/49 (resolved by 02, 08), `combos/` counts (resolved by 08 with commands, re-verified by me), E2 post-hand-off commits (resolved by 01), `muse-ember-1.0` (resolved by 04), collaboration estimates (none of the 8 files relies on them as fact; 01 row 15 states "no measured result in the sampled slices"), phase-5 numeric claims (01 row 14 tags them [UV]), installed variants re-implement or import (resolved by 01 section 6 and 03 section 3, consistently), T-1..T-10 approval (07 section 4: no approval found).
PASS for (e).

## 4. Cross-reference check (checklist item 3) and contradictions

### 4.1 Explicit cross-references between the 8 files
A search of the 8 files for references to a sibling research file (`research/0N-`, `item 2.0N`, `file 0N`, `see 0N`) found only the title of file 03 ("item 2.03"). The files cite scope slices and code, not each other. The cross-cutting concerns below are covered by more than one file; for each I compared the figures and statements across files.

| Cross-cutting concern | Files | Consistent? | Note |
|---|---|---|---|
| Drop-and-warn: 92 findings / 80 reviewer runs / 49 blocking / 3 flips; no "silent" discard in code | 01 (table row 3, E2), 02 section 5, 08 section 5 | Yes on every number (I recomputed 92, 49, 44 triples, 80, 3, 195 from `flags.tsv` and `audit2.json`) | wording point M-2 |
| `T01.01` not a recognised ref; `_ID_TOKEN` duplicates `_REF_TOKEN` | 01 (P-d), 02 section 4, 05 Units 2 and 7 | Yes (02 executed `T01.01`; 05 executed `T03.02`, `FR-RSR.9`, `P12`; both give an empty `refs_norm`) | |
| Convergence 0.75 (skill) vs 0.80 (code) | 01 C-6, 03 section 4.2, 06 sections 1.3, 5.3, 8(c) | Yes (`SKILL.md:703`; `contract.py:321`; test pins `test_verdict_mapping.py:432-458` per 06) | |
| Two ledger status machines (`resolved_check` vs `fixed/verified/reopened`) | 01 C-5, 03 section 4.1 | Yes (I read the `STATUSES` tuple at `ledger.py:17-20`, `EXIT_BY_DECISION` at `ledger_cmd.py:13` and `LIVE_STATUSES` at `review_ledger.py:66`) | |
| Two Tier-2 engines; the kernel wired only to the prompt path | 01 section 2, 04 section 3.2-3.3, 06 sections 2, 4, 7 | Yes (`cli/reflect` has no `cli.review` import; `runner.py:538-545`) | |
| Dispatch collapse and served-vs-requested model | 04 section 4, 07 E1-F4..F7 | Yes (reviewers: A-r3 only, 3 of 3 null class; I reproduced from `results.jsonl`). 07 E1-F5 adds the calibrator without class in 6 of 15 runs (A3 3/3, B3 4/4, C1 1/4, C2 1/4, E1 4/4, E2 4/4: reproduced by me); 04 section 4.3 counts only reviewers | complementary, see M-3 |
| `identity_source` | 04 section 4.2, 07 E1-F7, 06 section 7 | Yes (1 `observed` + 14 `requested-pinned` in combos, 13 `requested-pinned` in pilots: reproduced). 06 section 7 cites slice 11 for "requested-pinned" without the 1-of-15 exception that 04 found | harmless, see M-3 |
| Stage 2 exit failures and key leaks | 06 section 6, 07 E1-F8 / N-2 | Yes on 13 of 20, 8/13 EV-1, 0.704 (reproduced). 07 N-2 tags the combo key leaks [UNVERIFIED]; 06 section 6.2 derived 7 of 28 (2 pilot + 5 combo) | take 06 for that figure |
| `muse-ember-1.0` | 01 (row 8 E2, no ember in tier file), 04 section 7 | Yes | |
| E1 and E2 share the designSpec package (sha `044809e3...`) | 01 row 14, 08 | Yes (`snap.py:2`) | independence is file 16's topic |
| Limits 200/300 whole-finding drop in both parsers; v2 cluster step loses a whole reviewer | 01 P-c, 02 sections 2, 5.3, 05 Unit 2 | Yes | |

### 4.2 Contradictions between the 8 files
None that changes a conclusion. Two statements need a reading note for the synthesis (both graded minor): 02 section 5 Key Takeaways line "The 4 verdict flips are 3 in audit2.json plus 5 total-loss merges in summary.md:20" versus 08 section 5 (3 flips; the total-loss merges kept verdict FAIL with non-empty `brief_ids`, so they did not flip; "four" not reproduced). `audit-D/summary.md:20` (read by me) lists 3 flips and then "Also total-loss merges: g1-..., g7-..., n4-..., h1..." so 08 is right and 02 section 5.1 / Gap 2 ("[UNVERIFIED as 4]") are right; only the Key Takeaways sentence is loosely worded. See M-2.

## 5. Compiled gaps (checklist item 7, for the synthesis)

### Critical (block synthesis)
None. Every Gaps entry in files 01-08 is tagged [UNVERIFIED] or is a design question for the owner; none is an open item that the synthesis needs resolved to proceed.

### Important (affect quality; already tagged by the authors, listed so the synthesis does not use them as facts)
- E3 installed-variant cells (grammars, statuses, rubric, exit codes) rest on scope slice 12 except for file existence, sizes, constants and imports (01 Gap 1; 02 Gap 6; 03 Gaps 1-3).
- E1 code-driven path internals (`ensemble.py:772-832` hard-coded contract values, `contract_version 1.0`, `panel_lint` L1/L2 failure) were re-derived by 06; 01 Gap 2 and 03 Gap 4 still say [UNVERIFIED] and should be read together with 06.
- Pilot dispatch-collapse "6 of 9 tier3-orchestrated runs" is not re-derivable (logs absent; 04 Gap 1, 07 E1-F4 / G-2); only 1 of 3 (A-r3) and 0 of 12 are verified.
- Raw-transcript-dependent E2 claims (judge re-judge 12/12, source-opened detection 156 of 665, anchor fidelity 91.4%) have no committed artifact (08 G6, G15; 05 Gap 6).
- Whether any approval of T-1..T-10 / pilot stop rule exists beyond the T-9 redefinition (07 section 4: negative search only).
- Shadow-failure per-run causes and the jump of EV-1 from 3/39 to 8/13 (06 Gap 9; 07 G-1).

### Minor (notes)
- 06 Gaps 2-8, 10; 04 Gaps 2-5, 9; 05 Gaps 4-6; 02 Gaps 6-10; 01 Gaps 3-6; 07 G-3, G-5..G-8; 08 Gaps 1-8, 10. All tagged, none load-bearing for a decision.

## 6. Depth assessment
**Expected depth:** Deep (data-flow traces, integration points, pattern analysis).
**Achieved:** Deep. Evidence of depth: executed read-only reproductions (02 probes P-a..P-e, 03 D-1/D-2/D-11/X1-X3 with scratch scripts, 04 `panel resolve` runs and stream-log `jq`, 05 `refs_norm` probes, 06 exit script and pytest, 07 recounts from raw stream logs and CSV scoring, 08 `git archive` re-run of `final-table.py` / `three-way.py` with a byte-identical `final-table.md`).
**Missing depth elements:** none that blocks synthesis; the partial `cli/reflect/` read (M-5) and the unrun pytest for `tests/review` (02 Gap 10, 03 Gap 9, 04 Gap 9; not authorised) are the only reductions and are disclosed.

## 7. Findings table

Grading by definition: BLOCKING = wrong behaviour, false claim, missing required deliverable, security or data-loss risk. MINOR = cosmetic, wording, formatting, citation format, count wording, nit, style, moved line number on a true claim. I looked for blocking defects in each of the 8 files and in the gate-focus areas (a)-(e) and found none: every file, line, command output and count I re-derived matched what the file states, with the exceptions below, all of which are wording or scope-statement points that leave the conclusions of the files intact.

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| M-1 | MINOR | N | 03-merge-ledger-verdict.md, "Test-pin summary" after the section 2 table (L151) | The sentence "6 of the 8 test pins I read assert defect behaviour as intended (D-1 x3 including the CLI, D-2, D-11, D-3/D-4, D-6, reviewer re-classification)" does not match its own table or its own enumeration: the table has 9 rows that were read (193-217, CLI 274-292, 376-385, 396-405 + CLI 298-313, 408-417, findings 219-230, 201-212, 518-546, panel 204-214 + exclusion 208-213), and the parenthesis lists 8 items, not 6. The conclusion (fixes to D-1, D-2, D-11 will break named-as-feature tests and must rewrite them) is right. | Re-read of the table (L136-L149) and of `tests/review/test_review_ledger.py:376-385` (matches the quoted assertions). | State the counts that the table supports, for example "8 of the 9 rows read pin defect behaviour (D-5 pins the soft-distinctness behaviour in the panel module)". |
| M-2 | MINOR | N | 02-finding-contract.md, Key Takeaways of section 5 (L124) and Gaps 2 (L220); 01-overlap-capability-matrix.md, row 3 E2 cell (L119) | 02 L124: "The 4 verdict flips are 3 in audit2.json plus 5 total-loss merges in summary.md:20" reads as if 4 = 3 + 5; 08 section 5 shows the total-loss merges kept FAIL/REVISE with non-empty `brief_ids` and fixes the figure at 3 flips. 02 section 5.1 and Gap 2 hedge correctly ("[UNVERIFIED as 4]"); only the takeaway line is garbled. 01 row 3 writes "92 dropped findings, 49 blocking; luna 30, ember 33, ..." in one breath, which invites the mislabel that 02 and 08 warn about (the per-model list sums to 92, not 49). | `audit-D/summary.md` lines 17-20 and `audit2.json` (`drop_model` sums to 92, `verdict_flip` has 3 entries) read by me through `git show`; 08 L82. | When synthesising, take the flip and unit wording from 08 section 5 and 02 section 5.1; optionally reword 02 L124 to "the source's 'four' is not reproduced: 3 flips in `audit2.json`, plus total-loss merges that did not flip" and add "(all 92)" after the per-model list in 01. |
| M-3 | MINOR | N | all 8 files (cross-reference check) | No file points to a sibling research file for a concern covered twice (92/49 drop in 01/02/08; dispatch collapse in 04/07; Stage 2 exit failures in 06/07; two engines in 01/04/06; 0.75/0.80 in 01/03/06; `identity_source` in 04/06/07). All shared figures agree (section 4.1). Two complements are not visible from one file alone: 07 E1-F5 (calibrator dispatched without a class in 6 of 15 combo runs; reproduced by me from `results.jsonl`) is absent from 04 section 4.3, whose "collapse" counts reviewers only; 07 N-2 leaves the combo key leaks [UNVERIFIED] while 06 section 6.2 derived them (7 of 28). | grep for sibling references (one hit, the title of file 03); my recount of `calibrator_requested_served` / `reviewer_requested_served`; 06 L251; 07 L64. | The synthesis should cite the pair of files for each concern above; no change to the research files is required. |
| M-4 | MINOR | N | 04-dispatch-identity-tiers.md, section 3.2 (L56), section 3.4 (L71) and section 5 (L129) | Citations `local-gateway-alias-proxy.py:694-697, 834-839, 698-702, 432-449, 851, 935, 238-240, 363` and `ccsession:896-898` carry no directory. Both files exist at `src/superclaude/skills/ccsession-tag/` (`git ls-files` shows `local-gateway-alias-proxy.py` there; I read `ccsession:896-898` and `local-gateway-alias-proxy.py` near 694-697 and 834-839 and they match the text). | `git ls-files \| grep local-gateway-alias-proxy`; `sed -n 896,898p src/superclaude/skills/ccsession-tag/ccsession`. | Add the directory `src/superclaude/skills/ccsession-tag/` when the synthesis cites these lines (citation format only). |
| M-5 | MINOR | N | 06-reflect-two-engines.md, section 4 header (L138) and Gaps 6 (L352) versus the assignment "whole `cli/reflect/`" | The assignment asked for the whole package; the file read `runner.py` L1-L120, L440-L620, L686-L834 (not L120-L440, L620-L686: write-back, sidecar, preflight, alias count), `config.py` L236-L396 (not L1-L235), `commands.py` only L236-L275 plus a Grep, `fallback.py` L1-L110 plus a symbol Grep. The author logs this in Gaps 6 and every claim that depends on the unread ranges is tagged as slice-10-sourced. No claim I re-checked was wrong (`runner.py:538-545`, `commands.py:255`, `config.py:318-320`, `ensemble.py` 74/773/788/808-809, `contract.py` 310/321/403 all match). | Gaps 6 text; my line checks. | Optionally read the remaining ranges before the synthesis relies on `count_model_aliases`, the write-back loop or the fallback controller; otherwise keep the slice-10 tags. |
| M-6 | MINOR | N | 06-reflect-two-engines.md, section 6.2 table row "EV-1: reviewer-cards/ empty for the lint" (L245) and section 8(a) item 6 (L306) | "Across all 59 recorded `reviewer-cards/` dirs, 51 use the `-card` name and only 2 use `reviewer-N.md`" has no stated scope and, read next to the same row (1 pilot + 3 combos with `reviewer-N.md`), looks inconsistent. I reproduced it: it holds exactly for `.dev/reflect/pre-*` (59 dirs: 51 `-card`, 2 `reviewer-N.md`, 6 other); the 3 combo dirs B1-B3 use `reviewer-N.md` too (combos: 12 `-card`, 3 `reviewer-N.md`), and across both roots there are 84 dirs: 64 `-card`, 5 `reviewer-N.md` (shadow05, shadow15, B1-B3), 15 other. The conclusion (a naming mismatch with the lint, not a review failure) is unchanged. | read-only `uv run --no-sync python` over `.dev/reflect/*/reviewer-cards` and `.dev/eval-workspaces/shadow-model-combos/runs/*/reviewer-cards`. | Name the scope ("59 dirs under `.dev/reflect/pre-*`") when the figure is cited; note that shadow05 also uses `reviewer-N.md`. |
| M-7 | MINOR | N | 01, 05, 07, 08 (tag legends) | Tag vocabulary differs per file ([CV] / [UV] in 01; [SLICE-ONLY] and [RUN] in 05; [RECOMPUTED] in 07 and 08) while the gate and research-notes use [CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED]. Each file defines its own legend at the top and maps it to the standard meaning (01 section 4.1; 05 line 8: [SLICE-ONLY] "treated as [UNVERIFIED]"), so no claim is untagged. | legends at 01 L8 and L76, 05 L8, 07 L8, 08 L8. | Normalise to the standard three tags when the synthesis copies a claim. |

No blocking finding. No CRITICAL or IMPORTANT finding.

## 8. Independent verification log (what I re-read or re-ran; all read-only)

| Area | Re-verified items | Result |
|---|---|---|
| `findings.py` | `_ID` :26, `_REF_TOKEN` :29, `_SECTION_REF` :30, `_HEAD_FINDINGS` :31, MINOR+blocking :100-101, anchor 12..200 :104, anchor2 :108, claim 300 :118, `annotate` :346-360 (`finding["anchor"]` :349), 457 lines | match files 01, 02, 05 |
| `findings_v2.py` | 304 lines; `calibrated_confidence` rejection :96-97; anchor-or-citations :122-125; docstring :3-5 | match 01, 02 |
| `ledger.py` | `_brief_ids` :99-104; docstring :112; `block_ok` :129/:147/:150; refusal :150-157; clearing loop :254-258; `defer` :350-360; `verdict` :363-372; `STATUSES` :19; `new_ledger` cap 3 :37-38; `ledger_cmd.py:13` | match 03 |
| `telemetry.py` | `SCHEMA_VERSION` :17, `KINDS` :19, `_ID_TOKEN` :23 (plain string), `_ID_RE` :24, `_BOLD_DEF` :27, `model.observed` :49, strata :113, stratum error :268 | match 01, 02, 05 |
| `contract.py` / `ensemble.py` / `models.py` | 0.80 at :321 and the "incident 0.75" comment :310; `SKILL.md:754` cite at :403; `_VERIFICATION_SKIP_EXEMPTIONS` :36; `REFLECT_CONTRACT_VERSION = "1.0"` :74, :788; `merge_method` by count :772-773; `verification_ran False` :808-809; exit codes `models.py:46-48` | match 03, 06 |
| `panel.py` / `panel_cmd.py` / tiers JSON / templates | :71-73, :130, :143-145, :153-155, :252, :588, :595, :679, :600; 8 templates each with `"apply_to": ["first"]` at line 7; `panel_cmd.py:79, 124`; JSON 38 lines; 707 / 129 line counts | match 03, 04 |
| `card_convert.py`, `cluster.py`, `verify_cmd.py` | 517 lines; `MAX_CLAIM = 300` :86, truncation :199-201, `MINOR_WORDS` :81-83; `cluster.py` :64, :67-72; role-by-name :15-18, :466-471; `verify_cmd.py` :133-140 loop | match 02, 05 |
| `document_review_loop_prompts.md` (74 lines), `spec-panel.md` | placeholders :15-21; grading :31; briefs :32, :48; findings block :56-62; panel :70; never-clause :74; `spec-panel.md` :259 grading, :260 verdict, :263 reviser | match 03, 05 |
| `SKILL.md` (2033 lines) | :87 `--t2-engine`; shadow steps :340 (1), :342 (3), :343 (4), :345 (6), :346 (7), :349 (10); :703 routing; ANTHROPIC_DEFAULT_* :127, :232; `reviewer_briefs_materialized` only in `refs/reviewer-spec.md` :51, :57, :78; tasklist `SKILL.md` :1133-1165, :1619 (Stage 10.5); workflow `SKILL.md` :85-89 | match 01, 04, 06 |
| Agents | `model: sonnet` in reflect-reviewer, confidence-calibrator, evidence-validator at :6; none in `rf-qa.md` | match 04 |
| `runner.py` / `config.py` / `commands.py` | :538-545 ensemble routing; `Choice(["standard","deep"])` :255; quick floored :318-320; `--promote` default text :239; `spec_path` only at `runner.py:471-472`, never in `ensemble.py` | match 05, 06 |
| Installed variants | `review_ledger.py` `SCHEMA = 1` :34, `CAP_REVIEWS = 3` :35, `VERDICT_EXIT` :63, `ROW_INPUT_KEYS` :64, `LIVE_STATUSES` :66, unknown-key refusal :809-817, `decide` :1903-1907, `verdict_of` :2459-2464; `stoprule.py` `compute_verdict` :1162, "silence never passes" :1189; `diffgate.py` :754-756, :796 | match 02, 03 |
| `T2bModel01` | 18 occurrences in 11 files | match 04 |
| E1 recounts | 15 rows, 4,119,747 output tokens; 216 clusters / 13 multi / 6 chained / 7 unchained; identity_source 14 + 1; 69 `model_observed` card files in 11 combo dirs; exit script output; cluster-pair score TP 21 FP 4 FN 1 TN 24, 0.8400, 0.9545; calibrator null-class per run | match 04, 06, 07 |
| E2 through git | 0 `src`/`tests` diff 4a22d7421..6c09843; 4 commits; 96 combo dirs; 29 `RESULT.md`; 417 quarantine files; `snap.py` L4; `run-reviewer.sh` :9-17, :48, :51, :76; `theory.py` :8, `gtproxy.py` :91-93; 12 files in `pc-patterns`; `final-table.py` :7, :15-18, :23, :80-83, `three-way.py` :4, :19, :48, :52; `flags.tsv` counts; `audit2.json`; `COMBO-REPORT.md` :292, :294; #519 17 + 22 files, #518 0 + 1 | match 01, 02, 05, 08 |
| Independence and tree | exact-string and phrase search of the 8 files; `git status --short` unchanged | PASS |

## Summary

- Files reviewed: 8 (01-08; 1,931 lines), plus `research-notes.md` and the Phase 2 inventory.
- Blocking findings: 0. Minor findings: 7 (M-1 to M-7), all notes only.
- Gate focus: (a) PASS, (b) PASS (one partial-coverage statement logged by the author, graded minor), (c) PASS (one allowed sentence stating the independence rule at `05:189`; no citation or quotation from the forbidden folder or note), (d) not applicable to files 01-08 (no value-ledger rows), (e) PASS.
- What I checked to support "zero blocking": about 95 line citations at HEAD and the E2 tip, the counts in files 01, 02, 04, 06, 07, 08 (recomputed from git, from `flags.tsv` / `audit2.json`, from `results.jsonl` and `clusters_kept.json`, from the exit and cluster-pair scripts), the arithmetic of the figures in files 02, 07 and 08 (92 = 56+18+14+3+1; 49 = 24+14+10+1; 131/147; 194/214; 306 = 214+92; 216 = 203+13), all 12 slices' Gaps and Questions sections, and the 13 [CODE-CONTRADICTED] plus 8 [UNVERIFIED] rows of `AMBIGUITIES_FOR_USER`.
- Not verified by me: pytest results, gateway behaviour, raw transcripts, `~/.claude` behaviour beyond reading the installed scripts, and the value-ledger gate (d).

**Verdict: PASS (0 blocking, 7 minor)**

Status: Complete

