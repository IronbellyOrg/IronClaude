# QA Report — Research Gate (Partition C, gap-detection lens)

**Topic:** which ONE unified central Review Panel (shared core plus thin modules) captures all the value of E1, E2 and E3
**Files reviewed:** research/17-*.md through research/24-*.md (defect register, repository constraints, six value ledgers)
**Lens:** gap detection (gap severity, contradictions, depth, integration points, patterns, incremental writing)
**Date:** 2026-11-14
**Phase:** research-gate
**Fix cycle:** N/A
**fix_authorization:** false (report only)
**Overall Verdict: PASS** (0 blocking, 6 minor notes; details at the end)

Status: Complete

[PARTITION NOTE: This is partition C. Cross-file checks are limited to files 17-24. Full cross-file verification requires merging all Gate 1 partition reports.]

---

## Scope actually read

| File | Lines | Read how |
|---|---|---|
| research/research-notes.md | 269 | in full (open items per file, AMBIGUITIES_FOR_USER) |
| 17-defect-register.md | 560 | in full |
| 18-repo-constraints-and-branching.md | 230 | in full |
| 19..24 value ledgers | 986 / 935 / 1797 / 1046 / 894 / 671 | machine-checked in full (row structure, destination cell, ids, DROP targets, slice-line coverage, file:line cites); the Summary, verification and Gaps and Questions sections of all six read in full; about 60 individual rows read in full |

Read-only discipline: no research file or task file was edited; scratch scripts lived in /tmp and were deleted at the end; git was used only through `show`, `ls-tree`, `grep`, `diff --stat`, `for-each-ref`, `check-ignore`, `worktree list`, `remote -v`; Python only through `uv run`.

---

## Items Reviewed (gap-detection lens, items 1-6, then gate focus a-e)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Gap severity: every gap rated correctly, no hidden gap | PASS (with minor notes) | Open items of research-notes.md for file 17 (reproduce read-only; mark test pins; map numbering schemes) are all resolved in 17 (REPRODUCED 64 / TRACED 46 / UNVERIFIED 59 / mixed 2; crosswalk table; pin table). Open items for 18 (ref rule, constraints, naive-layout failures, package/test layout) are all resolved. Slice-line coverage script: of 4,408 content lines (table data rows, bullets, numbered items) in scope slices 01-12, 160 had no ledger row citing their line number (slice 03: 3, 06: 41, 07: 1, 08: 6, 09: 1, 11: 102, 12: 6; slices 01, 02, 04, 05, 10: 0). I probed every one of those groups by id and by content in the owning ledger (about 60 grep probes); every one is carried by a row that cites the item by id or restates it (for example slice 11 Q-1..Q-7 are carried by VL-24-188, 189, 148, 167, 158, 162, 183, which I read and confirmed; slice 08 D-X-2..D-X-4 by VL-22-900 which names the carrying rows; slice 07:290 design-review loop outcomes by VL-22-334). The line-number misses are citation-granularity only (the carrying rows cite a neighbouring line or an id). Items logged but unresolved by design are listed in the ledgers' own Gaps sections (for example ledger 23 G-6 and G-7: twelve reflect refs files and SKILL.md sections 6.1-6.5, 10, 12-14.5 were read by neither slice; research item 06 owns reading those ranges, outside this partition). No hidden gap rated blocking. |
| 2 | Contradiction resolution inside the assigned files | PASS (with minor notes) | The register counts reconcile: 171 unique DR ids (awk over lines 15-403), owner buckets 75/29/2/2/14/36/2/11 sum to 171, and Repro counts 64/46/59/2 equal the Summary and Gaps text. Ledger destination totals recomputed by script equal each ledger's own Summary in all six ledgers (19: 886; 20: 868; 21: 1,685; 22: 955; 23: 796; 24: 589). Contradicted source claims are corrected in rows (VL-19-027 #518, VL-19-088 combos 96, VL-19-494 T2bModel01, VL-19-645 "159", VL-21-091, 644, 712, VL-20-407, 739). Two cross-file status mismatches and one untagged stale row are listed as notes 1-3. |
| 3 | Depth appropriateness (Deep) | PASS | 17 reproduces defects by running read-only snippets (four repro scripts named, 64 rows REPRODUCED) and follows merge -> ledger -> verdict -> CLI end to end (DR-002, 003, 107, 114, 012). 18 observed the git ref collision in two scratch repositories in both creation orders and cites Makefile, CI, pre-commit and test pins; I re-read about 40 of its cites at HEAD and all match. The ledgers hold 5,779 rows for 12 slices. |
| 4 | Integration-point coverage (defect fix owners, repository constraints) | PASS | 17 gives every one of the 171 rows a fix owner (CORE, MODULE-reflect, MODULE-tasklist, MODULE-spec, HARNESS, EVAL, OPS, DROP) and a pin column, and orders the core families at lines 510-511. 18 section 8 lists 18 naive-layout failures F1-F18 with the rejecting gate and file:line (F1 skill directory without SKILL.md, F6 contract constant names under cli/, F8 reflect SKILL.md pins, F10 severity wording, F18 ref collision); section 9 names the package and test homes. |
| 5 | Pattern documentation | PASS | 18 sections 1, 2, 5, 6, 7, 9 capture the sync/verify/lint architecture checks, CI order, the optional-module registration pattern in `cli/review/__init__.py`, test naming and placement, and the partial plugin-mirror pinning. 17 records the test-pin pattern ("pinned as intended behaviour") per row and the four numbering schemes. |
| 6 | Incremental writing compliance | PASS | File mtimes 10:45 (18), 10:53 (17), 11:06-11:26 (24, 23, 20, 19, 22, 21), consistent with staged writing. 17 has per-slice evidence sections with provisional ids, then a "Corrections to earlier rows" table that overrides earlier cells; ledger 21 rows carry inline "CORRECTED by verification" text (VL-21-644, VL-21-091); ledger 19 has an appended "Tag convention and verification addendum"; ledger 20 has an appended code-verification table. Not one-shot dumps. |
| a | Every kept claim has file:line or an explicit [UNVERIFIED] tag | PASS (with minor notes 4, 5) | 716 file:line cites in 17-24 that resolve to one tracked file were checked mechanically against file length: 0 beyond end of file (6 hits were false resolutions of the bare name "CLAUDE.md" to a core copy). I also re-read more than 90 cites at HEAD and about 15 at the E2 tip with sed or git show (listed under Evidence Log); all matched except the minor items in note 3. UNVERIFIED rows are tagged (17: 59 rows; ledgers: per-row tags plus the convention text in 19 "Tag convention", 20 last row of the verification table, 21 last paragraph of the verification section, 24 G-L1). Ledger rows with no bracket tag and no file:line (19: 46%, 20: 79%, 21: 84%, 22: 62%, 23: 75%, 24: 83%, measured by script) are slice-sourced statements whose evidence is the Source column (slice:line) under that stated convention. |
| b | Open items and slice gaps resolved, logged or carried as rows | PASS | See item 1. 17 Gaps 1-9 and its "Questions for the owner" log what it could not do. The ledgers log slice gaps as rows (VL-20-605 for slice 03 gap 10, VL-24-206..209 for slice 11 G-6..G-9) and in their own Gaps sections (19 G1-G10, 20 items 1-8, 21 items 1-7, 22 items 1-9, 23 G-1..G-12, 24 G-L1..G-L8). |
| c | No run-1 contamination | PASS | grep of 17-24 for `review-panel-unify-20261113`, `REVIEW-PANEL-UNIFY-RUN2-QUEUED`, `TASK-RESEARCH-review-panel-unify`, `unify-2026`, `panel-unify`, `queued`: one hit file, 17-defect-register.md:534, a sentence that states the independence rule (allowed). Ledgers 19, 20, 22, 23 carry independence statements without the path; VL-20-605 rows the known slice-03 slip without a path or content. |
| d | Every value-ledger row has exactly one destination | PASS | Script over all 5,779 rows: each row has exactly one `\| DEST \|` cell from the ten-name vocabulary (0 rows with none, 0 with two); 0 empty cells; ids sequential with no duplicate in all six ledgers. 1,795 DROP rows: 1,573 "Duplicate of ..." (0 name a nonexistent VL id; 20 point to a primary that is itself DROP for an obsolete or out-of-scope reason, which is coherent; about 25 name the carriers inside the Statement cell instead, which I read for VL-22-312, 597, 749, 881, 896, 900) and 222 with another reason (a few terse: "Size inventory", "Cosmetic note"). |
| e | No claim builds on a [CODE-CONTRADICTED] or [UNVERIFIED] AMBIGUITIES row as fact | PASS (with minor note 1) | Of the 13 [CODE-CONTRADICTED] claims in research-notes.md, rows restating them carry the correction inline or link to it for #518, run-1 D14, reflect-has-no-panel, alias GT3, T2bModel01, "159 functions", unpassable-ac, theory.py HARD set, missing-task/severity, the fenced-yaml memory lesson, and the 106/107 combos count. Two claims have a kept row without an inline flag: "16 empty terra reviews" (VL-19-204 CORE; VL-20-109, VL-20-472 EVAL) and "discarded with no error" / "four flips" (VL-20-102, VL-20-104); for the ledger-20 rows the ledger's own Gaps items 1-2 list them as [CODE-CONTRADICTED] with the correcting row, for VL-19-204 nothing does (note 1). |

---

## Evidence Log (what I ran, so each verdict above can be re-checked)

| Area | Check | Result |
|---|---|---|
| 17 | awk over lines 15-403 for `\| DR-nnn` rows: row count, unique ids, 10-column shape, Repro cell, owner cell | 171 rows, 171 unique ids, Repro REPRODUCED 64 / TRACED 46 / UNVERIFIED 59 / "partly" 1 / "prose" 1, owners CORE 75, MODULE-reflect 29, HARNESS 14, EVAL 36, DROP 11, MODULE-tasklist 2, MODULE-spec 2, OPS 2: equal to the register's own counts |
| 17 | sed at HEAD of: findings.py:29, 100-101, 118; telemetry.py:23; cluster_cmd.py:27, 33-34; .gitignore:13, 79, 114; ledger.py:254-258, 273-274, 350-360; panel.py:536-543, 230; reviewer-spec.md:51, 78; review/__init__.py:24-35; reflect/contract.py:286-288, 309-326, 403; ensemble.py:74, 773; reflect_shadow_exit.py:313-314; panel_lint.py:188, 273; test_review_ledger.py:376-385; findings_v2.py:21, 80, 96-97, 111, 126, 132, 136; review-tiers.default.json:29; reflect SKILL.md:87, 146, 703, 727, 839, 858; _diversity.py:15; reflection-rubric.md:39; runner.py:457; commands.py:236-239, 538; reflect/__init__.py:1-15 | all match the register's statements; `git check-ignore -v` names .gitignore:13 for r5/lib/r5/x.py; `git log` of cluster_cmd.py shows one commit d2d8a2d16; memory file line 64 holds the fenced-yaml sentence |
| 17 | `git ls-tree` at 6c09843 (E2 tip): combos directories, tmp-scripts count, RESULT.md count; `git show` of run-reviewer.sh lines 48, 57, 66, 73, 76, audit-D summary lines 8-26, tests-tools.md lines 14-29 | 96 directories (97 entries), 55 tmp-scripts, 0 named gate8, 19 RESULT.md; run-reviewer.sh lines and audit-D text match DR-030..033, 067, 046, 048; per-file `def test_` column sums 111 + 68 = 179 against the stated TOTAL 159 |
| 17 | sampling of UNVERIFIED rows at HEAD (DR-062, 063, 122, 132, 137, 150, 110, 121) | DR-062 (confidence-calibrator.md:48 names 6 dimensions), DR-122 (card_convert.py:71-82 MINOR_WORDS has medium/important/should-fix/low/nit/info), DR-137 (refs/ has 12 files and no model-capability-tiers.md), DR-150 (config.py:334-335 clamp [2,4]), DR-132 (executor_class_resolved occurs only in panel_lint.py:155), DR-110 (output_by_severity only as suffixed names at telemetry.py:323, 340) all hold; DR-121 (manifest lock) partly: `save` is an atomic rename (manifest.py:156-163) and `advance_stage`/`record_attempt` exist at :277, :331, no lock text found by grep |
| 18 | sed or grep at HEAD of Makefile:114-117, 150, 171-176, 294, 453-454, 467-476, 549; .pre-commit-config.yaml:119-141; test.yml:22, 32-38, 47, 127-135; .gitignore:83-85, 127-135, 225; pyproject.toml:16, 54, 78-87, 107-116, 176, 204-207; launch-level-guard.sh:74-77; hooks.json:110; install_hooks.py:88; block-bare-python.sh:1-6; test_worker_contract.py:786, 871-873, 925; test_spec_panel_review_loop.py:156-159; test_codegraph_guide.py:116; test_routing_plugin_parity.py:29-47; test_panel_contract_lint.py:90-114; test_shadow_skill_contract.py:42-98; test_review_severity_rule.py:36-44, 112-125 | all match; `git ls-files .claude` prints 2 files (cache/sc-recommend-lookup.yaml, settings.json) as S1 says; `grep -c '^def test_'` of test_verdict_mapping.py = 36; 38 reflect test files, 19 review test files; 31 commands with `## Unattended mode`; 148 `src/superclaude` lines in 56 files; no ref named `feat/review-panel*` or `integration`; 47 local heads; 19 worktrees; `git remote -v` shows only the fork |
| 19-24 | script over all ledger rows: columns, destination cells, ids, DROP targets | see item d |
| 19-24 | slice-line coverage script (python through uv, scratch in /tmp) | 4,408 content lines, 160 not cited by line, all carried by id or content (item 1) |
| 19-24 | mechanical file:line check of 716 resolvable cites | 0 beyond end of file |
| 19-24 | probes for the 13 research-notes [CODE-CONTRADICTED] claims in all ledgers | item e |
| 19-24 | recomputed destination totals vs each ledger's Summary | equal for all six |

---

## Issues Found

All findings are graded MINOR (notes). None is a real defect of behaviour, a false claim that the synthesis would be forced to rely on, a missing required deliverable, or a data-loss or security risk.

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|----------|--------------|-------------------|---------|----------|--------------|
| 1 | MINOR | N | 19-value-ledger-handoffs.md VL-19-204 (CORE) and VL-19-740 (DROP); 20-value-ledger-e2-study.md VL-20-109, VL-20-472 | "16 empty terra reviews in valid rows" is restated as a plain fact in kept rows. research-notes.md AMBIGUITIES_FOR_USER lists it as [CODE-CONTRADICTED] (14 terra + 2 luna, slice 04). The correction exists at VL-20-718 and VL-20-771 and in ledger 20 Gaps item 2, so ledger 20's rows are covered by that list; VL-19-204 has no flag and no pointer. The rule the row supports (51 incomplete reports; terra and sol are not standalone reviewers) does not depend on the 16. Graded minor because the figure is attributed to its source (CR:294) and the correcting rows are in the same research set. | `grep` of rows containing "16 empty terra" (19: lines 215, 751; 20: lines 120, 388, 483, 553); VL-20-718 reads "valid-era only terra 14 + luna 2 = 16 row-packages, so COMBO-REPORT L294 mislabels 2 luna refusals" | Append "[CODE-CONTRADICTED: 14 terra + 2 luna, VL-20-718]" to the Reason cell of VL-19-204 (and optionally VL-20-109, VL-20-472); synthesis must not quote "16 empty terra" |
| 2 | MINOR | N | 20-value-ledger-e2-study.md Summary ("Still open: combo row directories 95 vs 96, VL-20-625") | The count is resolved elsewhere: 17 DR-047 and DR-076 and VL-19-088 give 96 directories; I re-ran `git ls-tree -d --name-only 6c09843:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/combos \| wc -l` = 96 (97 entries with SPEC.md). Ledger 20 still lists it as open. | command output above | Mark VL-20-625 resolved (96) with a pointer to VL-19-088 |
| 3 | MINOR | N | 17-defect-register.md DR-075 (line 155) | The parenthetical says the author's own check found `T2bModel01` "only under skills/ccsession-tag/* and sc-implement-protocol/refs/retry.md at HEAD". `git grep -n T2bModel01 HEAD -- src tests README.md` also hits tests/unit/test_ccsession_tiers.py:72, tests/skills/test_model_alias_policy.py:227, tests/skills/test_workflow_archive.py:799. The row's conclusion (the run-2 note "not referenced anywhere in src/ or tests/" is wrong) is therefore correct and stronger; only the stated search outcome is incomplete. | `git grep` output above | Replace the parenthetical with the full hit list; keep the DROP (documentation error) |
| 4 | MINOR | N | 17-defect-register.md Gaps and Questions item 1 | Item 1 says the 59 UNVERIFIED rows rest on evidence "outside what this item may open". At least 14 of them cite HEAD code that was readable under the item's own rules (DR-062, 063, 065, 072, 110, 117, 121, 122, 130, 131, 132, 137, 141, 150). I read eight of these at HEAD and every claim held (Evidence Log). The tags are conservative, not wrong, so nothing misleads; the register is weaker than it could be. | Evidence Log row "sampling of UNVERIFIED rows" | Optional: upgrade the verified rows to [CODE-VERIFIED] with the file:line already in the row, and reword Gap 1 |
| 5 | MINOR | N | 18-repo-constraints-and-branching.md section 4 Key Takeaways (4) and Gap 8 | Takeaway (4) says every branch layout "must also be a valid Orca worktree branch name" with no evidence and no tag; Orca's naming rules were not read. Gap 8 (E2 tip not read for collisions with the constraints) is open in the file, but it is closed by evidence already in the research set: ledger 19 addendum records `git diff --stat ec259f1b7 <tip> -- src tests` empty, and I ran `git diff --stat 4a22d74213f93837d00c2c314075dd967b9a98e3 6c0984326cbb8fb06c4a36065de58b171d3f8175 -- src tests`: no output. | command output above; 19 lines 918 | Tag the Orca sentence [UNVERIFIED] (or cite `orca worktree create --help`); cross-reference the E2 no-product-code check in Gap 8 |
| 6 | MINOR | N | 19-24 (all ledgers), rows that are not tagged | 46% to 84% of ledger rows carry neither a bracket tag nor a file:line inside the row. The evidence for them is the Source cell (slice:line) and the per-ledger convention text. The convention is stated but not uniform: ledger 19 has an explicit "Tag convention"; 20-24 state it inside verification sections or Gaps. A synthesis agent that reads only the table could treat an untagged slice figure as verified. | script measurement in item a | In the synthesis and anti-omission prompts, state once that an untagged ledger row is a slice statement, [UNVERIFIED] unless the ledger's verification section lists it |

Not findings (checked, correct): the "(3 shown)" annotation in VL-19-209 and the link in its Reason cell to VL-19-048 and VL-19-090 correctly handle the "four flips" and "49 blocking" label; VL-21-644 and VL-21-091 carry their corrections inline; the 20 DROP rows whose primary is also DROP are coherent (obsolete, retracted or out of scope).

---

## Summary

- Checks passed: 11 / 11 (6 checklist items plus gate focus a-e), 5 of them with minor notes.
- Checks failed: 0
- Blocking findings (CRITICAL or IMPORTANT): 0
- Minor findings (notes): 6
- Issues fixed in place: 0 (fix_authorization: false; no file was modified)

**Confidence:** Verified: 11/11 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Basis for each item is in the Items Reviewed table; for the six ledgers (5,779 rows) the verification is mechanical over all rows for structure, destinations, ids, DROP targets, citation lengths and slice coverage, and by reading for the Summary, verification and Gaps sections; per-row factual accuracy of ledger statements was sampled (about 60 rows read, about 20 re-checked against code), not exhaustive.

**Tool engagement:** Read: 14 | Grep: 0 as a separate tool (about 60 grep/awk/sed invocations ran inside Bash scripts) | Glob: 1 | Bash: about 45 (several were batched read-only scripts in `/tmp`, each cleaned up by its own trap). No web research was needed; no Tavily or web fallback was used.

UNCHECKED items: none. UNVERIFIABLE items: none.

Limits that a reader should know: (1) I did not re-run the experiments or pytest; (2) per-row accuracy of the 5,779 ledger rows was sampled; (3) UNVERIFIED rows of 17 outside my eight-row sample were not re-checked; (4) cross-file contradictions between files 17-24 and files 01-16 or the synthesis are outside this partition.

## Overall Verdict: PASS

No CRITICAL or IMPORTANT gap in files 17-24. Green light for synthesis for this partition, with the six minor notes above recorded and not rechecked in later rounds.

## QA Complete

Status: Complete
