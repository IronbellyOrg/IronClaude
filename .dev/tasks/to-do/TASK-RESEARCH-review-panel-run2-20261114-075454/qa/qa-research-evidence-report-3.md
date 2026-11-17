# QA Report - Research Gate, Evidence-Quality Lens (Partition C, Item 3.09)

**Topic:** which ONE unified central Review Panel (shared core plus thin modules) captures all the value of E1, E2 and E3
**Date:** 2026-11-14
**Phase:** research-gate (evidence-quality lens)
**Files reviewed:** research/17-defect-register.md, 18-repo-constraints-and-branching.md, 19-value-ledger-handoffs.md, 20-value-ledger-e2-study.md, 21-value-ledger-brainstorms.md, 22-value-ledger-collab-designs.md, 23-value-ledger-e1-e3-code.md, 24-value-ledger-evidence-consumers.md
**Fix authorization:** false (report only)
**Verdict:** PASS (0 blocking, 12 minor notes)
**Status:** Complete

---

## Method (what was actually done)

- Read research-notes.md in full and the item prompt (task file line 248). Read files 17 (all 560 lines) and 18 (all 230 lines) in full, and the first 90 lines plus the Summary and Gaps sections of ledger 19. Ledgers 19-24 were NOT read line by line; they were (a) parsed mechanically in full (every `VL-nn-nnn` row split on unescaped pipes, 5,779 rows) and (b) sampled by hand: at least 28 rows per ledger, evenly spaced across the ledger, each compared with the cited slice line, plus duplicate-of targets, plus 45 code citations quoted in the rows of ledgers 19, 23 and 24 checked against HEAD, plus the Gaps and Summary sections of all six ledgers.
- Code and tests were read at HEAD in this worktree with `sed -n` / `grep` batches (read-only). The E2 tip was read only with `git show 6c0984326cbb8fb06c4a36065de58b171d3f8175:<path>` and `git ls-tree`. The git ref rule of file 18 was re-run in two scratch repos under `/tmp` (deleted afterwards). Defect claims of file 17 were re-run read-only with `uv run python` (scripts under `/tmp`, deleted at the end); `git status` is unchanged from the session start.
- Independence: the two forbidden paths were never opened, listed, searched or cited. They were searched for as strings inside files 17-24 only (contamination scan); the only hits are sentences that state the independence rule (17:534, 22:1033, 20:927).

## Check 1. File inventory (PASS)

| File | Status line | Summary section | Gaps and Questions |
|---|---|---|---|
| 17-defect-register.md | Complete | yes (line 557) | yes (522) |
| 18-repo-constraints-and-branching.md | Complete | yes (228) | yes (206) |
| 19-value-ledger-handoffs.md | Complete | yes | yes (960) |
| 20-value-ledger-e2-study.md | Complete | yes | yes (917) |
| 21-value-ledger-brainstorms.md | Complete | yes | yes (1773) |
| 22-value-ledger-collab-designs.md | Complete | yes | yes (1021) |
| 23-value-ledger-e1-e3-code.md | Complete | yes | yes (869) |
| 24-value-ledger-evidence-consumers.md | Complete | yes | yes (650) |

(Evidence: `grep -m1 '^\*\*Status:\*\*'`, `grep -c '^## Summary'` and `grep -n '^## Gaps and Questions'` over the eight files.)

## Check 2a. Evidence density, file 17 (defect register): PASS

Sampled well over the required 15 claims, across all sections (slice 01, 02, 03, 04, 09, 10, 11 sections, final register, stale-doc list). Every one was opened at HEAD, or at the E2 tip through `git show`, and matched.

| Area | Claims opened and result |
|---|---|
| Slice 01 rows DR-001..DR-029 | `findings.py:104-106, :118, :100-101, :188-192, :27, :29, :31`; `telemetry.py:23, :49, :112, :267, :287`; `ledger.py:112, :114-115, :165-171, :254-258, :273-274`; `merge_cmd.py:94, :117-118`; `panel.py:485-494, :536-543, :600-605, :623-628`; `__init__.py:24-25, :30-35`; `review-tiers.default.json:29, :33, :35`; all match. Pins `test_review_ledger.py:376-385, :388, :518`, `test_review_cli.py:229, :245`, `test_review_panel.py:204-214, :288-291, :303-308, :331-339`, `test_review_panel_exclusion.py:208`, `test_review_findings.py:111-122` match their test names and bodies. |
| Re-run of the reproductions (read-only `uv run python`) | 201-char anchor drops only that finding (F2 kept); boundary 200/300/8 accepted; CRITICAL non-blocking accepted; empty claim accepted; `refs_norm` returns `['1.2','AC-0.4']` for `T01.02`; token matrix (UTF-8, ISO-8601 match; fr-9, FR-12a, P10, T01.02, AC1 do not); `@live7` 30/40 and `@default` 18/40 duplicate-model resolutions on the gateway; fixed slot `count: 2` validates and resolves to two Sonnet; all three `@reflect-*` templates raise in `gateway`. All identical to the register. |
| Slice 02 rows DR-052..DR-078 | `ledger.py:207-238, :326-330, :348-361, :361-373, :467-468, :50-64`; `findings.py:46-49, :293-297, :307-310, :413-416, :344-350, :197-224`; `ledger_cmd.py:132-137`; `merge_cmd.py:111-117`; `cluster_cmd.py:27, :33-34`; fixed-slot line `panel.py:536-537`; all match. E2 tip: `run-reviewer.sh:7-11, :46-48, :55-58, :64-67, :72-90`, `.bad-launch:19`, `judge-one.sh:7`, `final-table.py:11-18`, `three-way.py:19`, audit-D summary (92 = 30+33+14+7+7+1; 49 blocking; 3 flips; 45 merges without merge-stdout), `COMBO-REPORT.md:292`, `PILOT-REPORT.md:12`, `RAW-TRANSCRIPTS-NOT-COMMITTED.md:2`, `tests-tools.md` (re-summed: 111 + 68 = 179, collected 126 + 178 = 304; stated 159), `git ls-tree` counts (96 combo dirs, 55 tmp-scripts, 0 `checks-gate8`), `git diff-tree 167184c6b` (0 paths under `cli/review`). All match. |
| Slice 09-11 rows DR-107..DR-171 | `findings_v2.py:25, :40, :80, :111, :126, :132, :136, :190`; `manifest.py:176, :402`; `cluster.py:33-39, :119-124`; `cluster_cmd.py:146-152`; `verify_cmd.py:123-130`; `telemetry.py:416-429`; `ensemble.py:74, :773, :788, :806`; `contract.py:284-289, :297-300, :307-327, :401-404`; `_diversity.py:15`; `SKILL.md:87, :146, :338-350, :703, :838-839, :858, :1944`; `refs/reflection-rubric.md:39`; `refs/reviewer-spec.md:51, :78`; `panel_lint.py:188, :271`; `commands.py:239, :538`; `runner.py:457`; `reflect_shadow_exit.py:313-314`; `reflect_stage0a_replay.py:68-69`; `test_shadow_exit_script.py:292-299`; `cli/reflect/__init__.py:1-15`; `.gitignore:13, :79, :114`; `git check-ignore -v` and the `/lib/` count 0 at the tip; memory file line 64; `t2-engine` found only in `manifest_cmd.py`; xfail marker in `test_no_nesting_guard.py`. All match. |
| Bookkeeping | 171 rows = 168 eight-column rows + 3 rows with literal pipes (DR-067, DR-135, DR-170); 263 ids in, 253 mapped, 10 claim checks (arithmetic checks out); owner buckets sum to 171 (75+29+2+2+14+36+2+11); REPRODUCED = 64 matches an awk count of the Repro column. |

No false claim found in file 17. Minor notes are in the findings table (F-1 to F-5).

## Check 2b. Evidence density, file 18 (repository constraints): PASS

Opened about 70 cited locations (all sections 1-9 and the stale-doc list). All matched, including:

- `Makefile:108-163, :115, :114, :117, :126-130, :148-151, :165-353, :171-176, :188-195, :282-294, :307-309, :348-353, :362-476, :479-481, :549, :48, :65-71`; `.github/workflows/test.yml:4-8, :22, :32-38, :47, :102, :127-142, :191-199`; `contract3-generator-constraint-lint.yml:26-29, :43-47`; `boundary-guard.yml:19-33`; `.pre-commit-config.yaml:66-71, :105-126, :134-145`; `scripts/precommit_block_claude_mirrors.sh:4-22`; `pyproject.toml:16, :54, :78-87, :107-117, :176-179, :204-207`.
- `CLAUDE.md:16-18, :31, :35-37, :67, :80-100, :203-205, :292-299, :307-317, :336-338`; `/home/coder/.claude/CLAUDE.md:34-37, :45, :84`; `.gitignore:83-85, :127-135, :225`; `git ls-files .claude` = 2 files (S1 holds); hooks: `launch-level-guard.sh:74-77`, `hooks.json:110`, `install_hooks.py:88`, `block-bare-python.sh:1-14`, `require-orca-worktree-agent.sh` exists; `cli/main.py:559-561, :568-570`.
- Test pins: `test_primitive_dual_surface_lookup.py:16-21, :28-35, :38-40, :50-52`; `test_shadow_skill_contract.py:14, :42-49, :52-56, :78-82`; `test_spec_panel_review_loop.py:156-159`; `test_worker_contract.py:786, :871-879, :925`; `test_codegraph_guide.py:116`; `test_panel_contract_lint.py:67-71, :90-114, :196-200` (110 and 27 field counts); `test_verdict_mapping.py` = 36 `def test_`, 0 parametrize; `test_routing_plugin_parity.py:29-47`; `test_review_severity_rule.py:28, :36-44, :112-114, :288-293`; golden fixtures in `tests/review/fixtures/`.
- Counts: 25 tracked files in `cli/review`, 125 tracked plugin files, 19 `tests/review` modules, 38 `tests/cli/reflect` test files, 148 `src/superclaude` lines in 56 files (ops-integration 10, reflect SKILL 8), 31 command files with `## Unattended mode`, 19 worktrees, 47 local heads (40 `ironbelly/`), no `integration` ref, the only `review-panel` refs are the two `eval-tasklist-review-panel` refs, origin prefix counts (32/18/10/10/6/5/3/3/2/1), 16 files and 5,086 lines in `cli/review`, 9 files in `data/`, `contracts/__init__.py:64, :93, :104, :129, :143, :165, :204`, `arch_lint.py:58`.
- The ref rule (file 18 section 3) was re-run independently in two scratch repos (git 2.47.3): both creation orders fail with `fatal: cannot lock ref ...: ... exists; cannot create ...`, exit 128; the dash sibling `feat/review-panel-x` coexists. Identical to the report.
- Plugin claims: `plugins/superclaude/skills` holds `confidence-check, sc-implement-protocol, sc-recommend, sc-workflow-protocol`; 0 rf-qa agents; `cmp` shows `reflect.md` and `spec-panel.md` differ from `src/`.
- The negative claim that no slice mentions `feat/review-panel|verify-sync|cannot lock ref` holds (0 matches in all 12 slices).

No false claim found in file 18. Minor notes are F-6 and F-7.

## Check 2c. Evidence density and destination rules, value ledgers 19-24: PASS (with minor notes)

### Mechanical pass over every row (script parsed all 5,779 rows)

| Ledger | Rows | Ids sequential, no gap or duplicate | Column count 6 on every row | Destination in allowed set (single token) | DROP rows with a reason cell | Dangling VL references | Source cell `NN:line` in the ledger's own two slices and inside the slice length |
|---|---|---|---|---|---|---|---|
| 19 | 886 | yes | yes | yes | 443 of 443 | 0 | 886 of 886 |
| 20 | 868 | yes | yes | yes | 298 of 298 | 0 | 867 of 868 (VL-20-368 cites "git ls-tree", F-12) |
| 21 | 1,685 | yes | yes | yes | 584 of 584 | 0 | 1,685 of 1,685 |
| 22 | 955 | yes | yes | yes | 237 of 237 (4 terse, F-8) | 0 | 955 of 955 |
| 23 | 796 | yes | yes | yes | 150 of 150 | 0 | 796 of 796 |
| 24 | 589 | yes | yes | yes | 83 of 83 (1 terse, F-8) | 0 | 589 of 589 |

- Destination counts recomputed per ledger equal the counts printed in each ledger's own Summary (19: CORE 179, DROP 443, EVAL 104, HARNESS 38, KNOWLEDGE 58, reflect 23, spec 16, tasklist 13, pr-review 7, rfqa 5; the other five ledgers match the same way). DROP rows starting "Duplicate of" in ledger 19: 411 (stated 411).
- Only 4 non-DROP rows name an alternative destination in the reason cell (VL-19-384, VL-21-565, VL-22-044, VL-22-344). Each still has exactly one destination in the Destination cell, so none is a multi-destination row.
- DROP chains (a duplicate of a row that is itself DROP): every chain ends in a DROP row with a stated reason (retracted figure, [CODE-CONTRADICTED] claim, obsolete, out of scope); none ends in a missing or empty row.
- Pipes inside code spans are escaped in all six ledgers (`\|`), so the tables render as 6 columns.

### Hand sample (source slice line opened and compared with the row)

Sampled row numbers (30 / 28 / 30 / 28 / 28 / 28, evenly spaced):

- 19: 12, 41, 70, 99, 128, 157, 186, 215, 244, 273, 302, 331, 360, 389, 418, 447, 476, 505, 534, 563, 592, 621, 650, 679, 708, 737, 766, 795, 824, 853
- 20: 14, 45, 76, 107, 138, 169, 200, 231, 262, 293, 324, 355, 386, 417, 448, 479, 510, 541, 572, 603, 634, 665, 696, 727, 758, 789, 820, 851
- 21: 30, 86, 142, 198, 254, 310, 366, 422, 478, 534, 590, 646, 702, 758, 814, 870, 926, 982, 1038, 1094, 1150, 1206, 1262, 1318, 1374, 1430, 1486, 1542, 1598, 1654
- 22: 18, 52, 86, 120, 154, 188, 222, 256, 290, 324, 358, 392, 426, 460, 494, 528, 562, 596, 630, 664, 698, 732, 766, 800, 834, 868, 902, 936
- 23: 20, 48, 76, 104, 132, 160, 188, 216, 244, 272, 300, 328, 356, 384, 412, 440, 468, 496, 524, 552, 580, 608, 636, 664, 692, 720, 748, 776
- 24: 14, 35, 56, 77, 98, 119, 140, 161, 182, 203, 224, 245, 266, 287, 308, 329, 350, 371, 392, 413, 434, 455, 476, 497, 518, 539, 560, 581

Result: in all 172 sampled rows the Statement is the same content as the cited slice line (numbers, ids and names match), the Destination is one of the allowed values, and the destination is defensible under the rules. Duplicate-of targets were opened for the 15 sampled DROP rows of ledger 19 (targets VL-19-111, 094, 312, 338, 392, 041, 043, 334, 112, 116, 368, 472, 473, 203, 490, 727-729, 155, 806): each target exists, carries the same content and has a non-DROP destination (except VL-19-203, itself a DROP duplicate of VL-19-094, which is EVAL). Three E2-tip facts behind sampled ledger 20 rows were re-read through git (`b4-terra-alone.sh` exists; `RAW-TRANSCRIPTS-NOT-COMMITTED.md:4` text; the batch-11 per-run figures sit on slice line 03:165).

### Code citations quoted inside ledger rows

A script extracted every `file.ext:line` citation in ledgers 19, 23 and 24 that resolves to one tracked file (295 citations). Zero point beyond the end of the file. 45 random citations were compared with the claim sentence (e.g. `cluster.py:48-49` disputed rule, `panel.py:600-605`, `ledger.py:210-218`, `merge_cmd.py:76-79`, `findings_v2.py:36`, `MODEL-TIERS.md:44`, `reflect-reviewer.md:5-8`, `sc-tasklist-protocol/SKILL.md:1640`, `review-tiers.default.json:32`, `test_review_cluster.py:233-260`); all 45 match. Ledger 24's "Verification notes" were re-checked too (`reflect_shadow_exit.py:55, :215, :313`, `cluster.py:50-51, :67-69`, `findings_v2.py:35`, `findings.py:14-24`, `pr_submit/loop_guard.py:19-20` and `fsm.py:32-33` duplicate cap constants, `reviewers.py:41`, `classifier.py` 618 / `conflicts.py` 1,659 / `merge_guard.py` 605 lines, 16 files and 5,086 lines in `cli/review`): all true.

### Independent confirmation of ledger statements that research-notes lists as [UNVERIFIED]

- "E2 commits after 4a22d7421 changed no product code": `git diff --stat ec259f1b718c 6c0984326c -- src tests` is empty (0 lines); merge-base of HEAD and the E2 tip is `ec259f1b718c`. True (ledger 19 VL-19-454).
- "muse-ember absent from the tier data at HEAD": `review-tiers.default.json` has no `muse-ember` (read in full). True.
- "92 / 49 unit": audit-D summary shows 92 dropped findings by reason and 49 of them blocking, per-model sum 92. Ledger and register state this correctly.
- "combos has 96 directories": `git ls-tree -d` = 96. True.

## Check 3. Scope coverage: PASS

Every key item of research-notes EXISTING_FILES that belongs to topics 17-24 is examined: section B (review package, reflect package, tests, scripts, memory, shadow-run and combo evidence) in file 17 and ledgers 23-24; section C (E2 hand-offs, study, collaboration packages, brainstorms) in ledgers 19-22 and file 17; section D (E3 loop and variants) in ledgers 23-24; section E (consumers) in ledger 24; section F (repository rules) in file 18 (CLAUDE.md, Makefile, CI, pre-commit, plugins, pyproject, docs). `.dev/research/346-review-loop-experiments/` (6,523 files) stays unread by every slice and is carried as a gap (research-notes D; slice 12 gap 2; ledger 24 G-L1/G-L5), not silently skipped.

## Check 4. Documentation cross-validation: PASS

Doc-sourced claims in file 17 carry REPRODUCED / TRACED / UNVERIFIED in the Repro column and [CODE-CONTRADICTED] / [STALE DOC] in the stale-doc list; in file 18 every constraint row and bullet carries [CODE-VERIFIED], [CODE-CONTRADICTED], [UNVERIFIED] or [DOC-STATES]; ledger rows inherit the slice tags and each ledger's Gaps section states that slice-sourced figures are [UNVERIFIED] unless a row says otherwise. Every [CODE-VERIFIED] and [CODE-CONTRADICTED] claim sampled was confirmed by the code (see 2a, 2b, 2c). The five [CODE-CONTRADICTED] claims I re-ran or re-read hold: 159 vs 179 tests (re-summed), fenced yaml calibration parsed at `cluster_cmd.py:27-34`, `.claude/` has 2 tracked files (S1), no `integration` ref (S3), `#518` touches 0 `cli/review` files.

## Gate focus

| # | Gate focus | Result | Evidence |
|---|---|---|---|
| a | Every kept claim has file:line (or git path:line) or an explicit [UNVERIFIED] tag | PASS | Files 17 and 18: every row and bullet cites a location or carries a tag (17 lists 59 rows as UNVERIFIED with the reason). Ledgers: every row has a slice:line source (5,778 of 5,779; F-12), and each ledger's Gaps section declares slice-sourced figures [UNVERIFIED] unless the row says otherwise. See F-10 for the note that many ledger statements carry no inline tag. |
| b | Open items of research-notes for each file, and the slice gaps, are resolved, logged or carried as rows | PASS | 17: open items (a)-(e) all answered (reproduction summary, test pins table, one numbering scheme with crosswalk, counts in and out, two contradicted claims). 18: ref rule, constraints with enforcing file, installed-path enforcement, plugin mirror, failing naive layouts, package and test layout all present. Slice Gaps and Questions: a source-line script found every gap or question item of slices 02, 03, 04, 05, 07, 08, 09, 10 cited by a ledger row; the apparent misses were traced by hand: slice 01 gap table G1-G10 (e.g. G6 = VL-19-437, G10 = VL-19-441), slice 06 lines 664 and 666 (= VL-21-1667, VL-21-1668), slice 11 G-1..G-8 and Q-1..Q-7 (rows VL-24-020, 034, 138, 148, 155, 162, 165, 168, 183, 188, 189, 196, 206 and the Q-L list), slice 12 Q5 (= VL-24-543). Residual: F-8 (one DROP) and F-11 (slice 11 G-9). |
| c | No run-1 contamination | PASS | String scan of the eight files for the two forbidden paths: 17:534 (rule statement), 22:1033 and 20:927 (rule statements, no path content); 0 hits in 18, 19, 21, 23, 24. The other `.dev/tasks/` mentions concern the E2 sandbox exclusion list and the `.dev/tasks/done/<pkg>/source.md` harness path, the CLAUDE.md staging rule, a script's default output folder (`TASK-WF-implementStages0-20261111-202912`, VL-23-503) and this plan's own folder (VL-23-630); none is the forbidden folder or the queued note. The recorded slip (slice 03 gap 10) is carried without content (VL-20-605). |
| d | Every ledger row has exactly one destination | PASS | Mechanical check above: 5,779 rows, 1 destination each, all in the allowed set; 0 rows with empty or double destination. Notes F-8 and F-9 concern the reason text, not the count. |
| e | No claim builds on a [CODE-CONTRADICTED] or [UNVERIFIED] row of research-notes AMBIGUITIES as fact | PASS | The [CODE-CONTRADICTED] rows (#518 attribution, run-1 D14, reflect has no panel code, alias GT3, "no error", "four flips", "16 terra", `unpassable-ac`, T2bModel01, "159 functions", `theory.py` HARD set, fenced yaml lesson) appear only as corrections (DR-045, 047-051, 074-075, 087, 153; VL rows with DROP or KNOWLEDGE and an explicit tag). The [UNVERIFIED] items (92/80/49 unit, combos size, E2 post-hand-off commits, muse-ember, collaboration estimates, phase-5 numbers) are either resolved by evidence I re-ran (see 2c) or carried with the tag (all collaboration estimates and test counts in ledger 22 gap 1-2; phase-5 numbers in ledger 24 G-L1). |

## Findings

No blocking finding. All items below are MINOR (citation, wording, formatting, or a disclosed judgement call); they are notes and do not fail the gate.

| # | Severity | Blocking Y/N | File and location | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| F-1 | MINOR | N | 17, DR-001 file:line cell | Lists `findings_v2.py:...126,128,132,136` as limit sites. Line 128 is the `citations` list-type check; the length limits are at 126, 132 and 136 (the prose under slice 03 names 126, 132, 136 correctly). | `sed -n 126,136p findings_v2.py`: 128 is `if not isinstance(citations, list) or not 1 <= len(citations) <= 8` | Drop 128 from the cell. |
| F-2 | MINOR | N | 17, DR-053 statement | Says `defer` "rewrites the stored last-round verdict/decision to PASS" without condition. The code does it only when no brief id remains after removing the deferred row. The reproduction covered exactly that case. | `ledger.py:356-360`: `last["brief_ids"] = [...]`; `if not last["brief_ids"]: ... = "PASS", "PASS"` | Add "when it was the last open blocking row". |
| F-3 | MINOR | N | 17, DR-017 file:line cell | Cites `review-tiers.default.json:7-9,18-23` for "Qwen and glm remain in the tier lists". Lines 18-23 are the `classes` map and the end of `names`; the tier lists are lines 5-10. | `sed -n 1,23p review-tiers.default.json` | Cite `:7-9` (and `:5-10` for the full list). |
| F-4 | MINOR | N | 17, rows DR-067, DR-135, DR-170 | Unescaped `\|` inside code spans (`\|\| $APIERR`, `full \| degraded`, `2073600319\|t4\|1`) splits these three table rows into 11 cells in a Markdown renderer; the six ledgers escape pipes correctly. | `awk -F'\|'` gives NF=12 for exactly these three rows | Escape the pipes. |
| F-5 | MINOR | N | 17, "Stale Documentation Found" (`findings.py:322` item) | The `refs_norm` docstring "Uppercase, unique, sorted requirement ids" is graded [CODE-CONTRADICTED]. The behaviour (lower-case ids are dropped, not upper-cased) is verified, but the docstring can also be read as describing the ids that are returned. | `findings.py:322`; `refs_norm('ac-1')` returns `[]` | Soften to "ambiguous docstring" or keep and add the reading. |
| F-6 | MINOR | N | 18, row a5 | Says the `launch-level-guard.sh:74-77` hook "only requires that `--repo` be present". The guard requires a non-empty operand that does not start with `-` (`:598-603`). It still does not check the repo value, so the conclusion stands. | `launch-level-guard.sh:598-603` | Reword to "requires a non-empty `--repo` operand". |
| F-7 | MINOR | N | 18, "Key Takeaways" bullets in sections 1-3 | The takeaway bullets carry no tag (the claim bullets and rows above them do). | Read of sections 1.1-1.3 and 3 | None needed; optional. |
| F-8 | MINOR | N | 22, VL-22-403, 409, 413 (reason "Size inventory"), VL-22-878 ("Cosmetic note"); 24, VL-24-581 ("Coverage statement") | Five DROP rows give a label instead of a reason. VL-24-581 drops slice 12 gap 10 (rf-qa-qualitative's 8 per-document checklists and rf-analyst output formats were counted by headings only). Ledger 24's own Gaps list (G-L6) names only that the rf-qa tests were not searched, so this gap about the rf-qa replacement is not carried anywhere in the file as an open item. | `uv run` row dump of the five rows; `grep -n 'headings only' 24-*.md` = 1 hit (the row itself) | Give the five rows a real reason; carry the slice 12 gap 10 text into ledger 24 Gaps or into the synthesis open questions for the rf-qa module. |
| F-9 | MINOR | N | 21, VL-21-782 (move catalogue M1-M10) and VL-21-1005 (class card schema, `applies_to` plan/spec/doc) | Destination MODULE-tasklist although the row's own reason says spec, PR review and rf-qa can reuse it. Under the stated rule (two or more modules: CORE) this is a borderline call. It is disclosed (ledger 21 Gaps item 6, which also lists VL-21-160 and VL-21-774 as HARNESS where the slices say CORE) and handed to the synthesis. | `grep -n '^\| VL-21-782 \|^\| VL-21-1005 ' 21-*.md`; Gaps item 6 | Synthesis must settle these destinations (hoist to CORE or keep with a stated reason). |
| F-10 | MINOR | N | Ledgers 20, 21, 22, 23 (statement text) | Many non-DROP claim-type rows state slice-reported numbers with no inline tag or code cite (lower bound, counting any back-ticked token as evidence: 181 of 283 in ledger 20, 349 of 609 in ledger 21, 80 of 289 in ledger 22, 168 of 444 in ledger 23, 46 of 223 in ledger 24, 27 of 301 in ledger 19). The evidence is the Source column (slice:line) plus each ledger's Gaps statement that slice-sourced figures are [UNVERIFIED] unless the row says otherwise. Acceptable as designed, but the synthesis must not quote a ledger figure as verified. | `/tmp` script over all rows; Gaps sections of the six ledgers | Synthesis rule: ledger figure = slice-reported unless the row carries [V] or a code cite. |
| F-11 | MINOR | N | 24, slice 11 G-9 | Slice 11 gap G-9 (the slice's own reruns depend on the current tree of 91 `pre-*` dirs) has no row. Ledger 24 G-L1 mentions the `/tmp/e1-recount-slice11/` scratch only indirectly. | `grep -n 'Drift risk' 24-*.md` = 0 hits | Optional: add one row or a sentence to G-L1. |
| F-12 | MINOR | N | 20, VL-20-368 | The only row of 5,779 whose Source cell is not `NN:line` ("git ls-tree"). It is a DROP row that records the agent's own tree listing (`analysis/attrib.json`). | Mechanical source check | Cite the slice line or tag the row "own listing". |

## Issues Found

Blocking (CRITICAL / IMPORTANT): 0. Minor notes: 12 (F-1 to F-12).

## Confidence Gate

Checklist items: 4 (file inventory, evidence density, scope coverage, documentation cross-validation) + 5 gate-focus items (a-e) = 9.

- [x] VERIFIED 9: check 1 (grep of Status, Summary, Gaps in 8 files); check 2 (file 17 and 18 claims opened at HEAD and the E2 tip; ledger rows parsed in full and 172 hand-sampled against slice lines; 45 code citations; 8 re-run reproductions); check 3 (EXISTING_FILES map against files 17-24); check 4 (tag scan plus confirmation of sampled [CODE-VERIFIED] claims); gate a, b, c, d, e (evidence in the Gate focus table).
- [?] UNVERIFIABLE: 0. [ ] UNCHECKED: 0.
- Scope limit stated honestly: ledgers 19-24 were verified by full mechanical parsing plus the required sample (at least 25 rows each, actually 28-30), not by reading all 5,779 rows. Rows outside the sample, and the 59 register rows and slice-reported figures that the files themselves tag [UNVERIFIED], are not re-derived by this review.

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 8 (task line 248; research-notes.md; 17 in 4 chunks; 18; 19 first 90 lines; this report) | Grep: 0 (dedicated tool not used; greps ran inside Bash) | Glob: 1 | Bash: about 48 read-only batches (`sed -n`, `grep`, `awk`, `git show`/`ls-tree`/`for-each-ref`/`diff --stat`/`check-ignore`, two scratch git repos under `/tmp`, 8 small `uv run python` scripts for row parsing, sampling, citation checks and defect re-runs). Read + Grep + Glob = 9 is not below the 9 checklist items, and every Bash batch maps to a named check above.
No Tavily or web call was needed (every claim is repository- or git-bound).

## Summary

- Checks passed: 9 / 9 (4 checklist items, 5 gate-focus items).
- Checks failed: 0.
- Blocking issues: 0 (CRITICAL 0, IMPORTANT 0). Minor notes: 12.
- Issues fixed in place: 0 (report-only; no research file and no task file was modified; scratch scripts and scratch git repos under `/tmp` were deleted; `git status` unchanged from the session start).

Assessment: files 17 and 18 hold up under re-execution. Every sampled location, count and reproduction matched, including the numbers that look most fragile (30/40 and 18/40 duplicate resolutions, 171 rows, 179 vs 159 tests, 96 combo directories, 5,086 lines, 148 `src/superclaude` lines in 56 files, the git ref collision in both orders). The six ledgers are structurally clean (sequential ids, one destination per row, a reason on every DROP, no dangling references, summary tallies equal recounts) and the 172 sampled rows match their slice lines. The weaknesses are small: five DROP rows with label-only reasons (one of them drops a real coverage gap about rf-qa), two disclosed borderline CORE-vs-module destinations in ledger 21, and slice-sourced figures that the synthesis must keep treating as unverified.

## Verdict: PASS

(Zero blocking findings; 12 minor notes. Green light for synthesis on files 17-24. Recommended before synthesis, not required: fix F-8 so the rf-qa checklist-reading gap reaches the open questions, and settle F-9 in the synthesis.)

Status: Complete

## QA Complete
