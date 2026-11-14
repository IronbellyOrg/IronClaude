# QA Report — Synthesis Gate, structure lens (Partition 2 of 2)

**Topic:** Unified Review Panel investigation (E1 reflect Tier 2 panel, E2 tasklist review-panel evaluation, E3 #346 review loop)
**Date:** 2026-11-14
**Phase:** synthesis-gate (structure lens, items 1-6 plus required-content check)
**Fix cycle:** N/A (first review)
**Assigned files:** synth-05-recommendation-architecture.md, synth-06-value-migration-plan.md, synth-07-questions-evidence.md
[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Overall Verdict: FAIL

One blocking finding (IMPORTANT, synth-06 Section 8.3 gate G9: the stated command, file count and collected count do not agree with the repository). Everything else in the structure lens and the required-content check passes. Minor findings are listed as notes and do not fail the gate. The open items the executor named (four debates each `partial` with unaddressed HIGH invariants; the C14 recount; the PENDING / exit 12 `[CONTRADICTION]`; E2 pinned at commit 4a22d74213f93837d00c2c314075dd967b9a98e3) are stated as open or corrected in all three files and are not defects.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Section headers match the Report Structure template and the synthesis prompts | PASS (notes N1, N2) | Read task-file lines 300, 304, 288 (the three embedded synthesis prompts) and `src/superclaude/skills/tech-research/SKILL.md:1432-1493` (template). synth-05: `## 7. Recommendation` with `**Recommended approach:**`, `**Rationale:**`, `### 7.1`-`### 7.4` (+ 7.1.1-7.1.4, 7.4.1-7.4.3). synth-06: `## 8. Implementation Plan (value-capture and migration plan; not a roadmap)`, `### 8.1`-`### 8.6`, the four exact `#### Track M1..M4` headings, `#### Gap coverage`. synth-07: `## 9. Open Questions`, `## 10. Evidence Trail` with Codebase Research, Web Research, Synthesis Files, Scope Discovery Inputs, Adversarial Debate Outputs, QA Reports, Gaps Log. The Phase-based template of Section 8 is replaced by Tracks by the task's own prompt (owner scope change), so that is not a defect. |
| 2 | Table column structures | PASS | Every table header matches the prompt text: synth-05 7.1.3 `Core component / Responsibility / Built from / Contract / Resolves conflicts`; 7.1.4 seven columns; 7.2 five columns; 7.3 four columns; synth-06 8.1 seven columns, 8.2 `Step / Action / Files / Details / Closes gaps`, Gap coverage, 8.3 `Gate / Suite / Command / What it guards / Must change on purpose?`, 8.4, 8.5; synth-07 `# / Question / Impact / Suggested Resolution`, `File / Topic / Agent Type`, `File / Topic`, `File / Report sections`. An awk pass over synth-06 8.1 found 691 rows V-001..V-691 with no ID gap or duplicate; four rows show a different cell count only because of escaped `\|` inside a cell (I printed all four; they are well formed). |
| 3 | No fabrication (at least 8 claims per file checked against research files, code or debate artifacts) | PASS (notes N3, N4, N5) | synth-05 (40+ checks): three batch scripts of `sed -n` over cited lines at HEAD `792cf8c52` confirmed `findings_v2.py:36` (LENSES), `:107-110`, `:144-146`; `panel.py:36,46,73,600-605`; `ledger.py:128,187,254-258,350-360`; `ledger_cmd.py:13`; `manifest.py:39`; `telemetry.py:112-115`; `findings.py:14,29,349`; `card_convert.py:71-83`; `cluster.py:67-70`; `fsm.py:941`; `reviewers.py:41`; `severity_router.py:191-193`; `runner.py:538-545`; `config.py:335`; `reflect-reviewer.md:5-8`; `document_review_loop_prompts.md:70`; `test_review_cli.py:44-49`; `merge_cmd.py:29-35,101-104`; `panel_cmd.py:40-46,108,124`; `review-panel.default.json:9-11` (4 reviewers) and `live7.json:9-13` (7). Debate figures re-read in the four `return-contract.yaml` files (C03 0.9167 vs 0.8798, margin 3.68 percent, 25 of 29; C05 0.9091 vs 0.8810, points 6 to 2, 30 of 33, 11 HIGH; C13 0.9804 vs 0.9724, points 14 to 10, 10 HIGH; C14 0.9256 vs 0.9194, points 6 to 4, 24 of 30, 3 HIGH): all match. The C14 recount was re-run (`recount_tier_decision.py`, read-only): 39 files, tier 2 in 38, flag set in 35, flag and tier 2 in 34, rules 4/5/6 = 18+2+9 = 29: matches synth-05 line 18 and synth-06 line 11 exactly. Research files: 41 review call sites with 32 needing an in-place fix (`research/10:131`), 48 post run dirs with 0 findings blocks (`research/07:376`), 142/142 vs 0/689 (`research/05:155,180`), 23 of 45 briefs (`research/06:87`), 8/13 = 0.615 vs 3/39 (`research/07:197`), 195 chained / 83 mega-rows / 1398 rows (`research/02:145`), 49 lost blocking findings = 24+14+10+1 (`research/02:126`). Web table URLs and figures all exist in `research/web-01..04` (82.7 and 37.7 percent, arXiv 2602.17875, 2510.11822, 2605.29800, 2611.01829, 2601.22548, PMC4849582, CodeQL `fingerprints.ts`, SARIF 2.1.0). synth-06: gate counts re-collected with `uv run pytest --collect-only` (G1 23, G2 37, G3 126, G4 10, G5 211, G6 160, G7 79, G8 82, G10 178, G11 5, G-all 1182: all match; tests/cli/reflect 353 as a whole); every gate test file and script exists; `uv run superclaude eval run --help` and `uv run python scripts/reflect_shadow_exit.py --help` run; branch facts verified (`git log origin/master..HEAD` = 3 commits; `git diff --stat origin/master HEAD -- src tests` = 4 files; `src/superclaude/cli/review` diff empty). synth-07: gap table has 94 G, 77 D, 25 C rows; every G-01..G-94 appears exactly once in 9.1; every D-01..D-77 appears in 9.4; the 27 `unverified claim` and 9 `code-contradicted doc` G ids in 9.2 equal the ids typed in `gaps-and-questions.md` column 7; Q-38 "13 of 20" matches `research/11:192,216,286`. E2 citations at the pinned commit resolve via `git cat-file -e` / `git show` (COMBO-REPORT.md:291,298,373; run-reviewer.sh:58,76; judge-one.sh:13-16,21). |
| 4 | Evidence citations use real paths; parent directories exist | PASS (note N3) | Installed paths exist: `~/.claude/agents/finding-grader.md`, `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py` (2668 lines), the five `~/.claude/commands/sc/spec-panel-*.md` (472, 481, 475, 483, 481 lines: the "472-483" claim holds), `sc-diffgate`, `sc-fix-audit`, the stoprule skill. Paths absent today are all tagged [proposed] and their parents exist: `cli/review/data/lenses/`, `cli/review/data/rubrics/` (parent `cli/review/data/`), `src/superclaude/agents/finding-grader.md` (parent `src/superclaude/agents/`), `cli/reflect/contract_writer.py` (parent `cli/reflect/`). pr-submit code lives at `src/superclaude/pr_submit/` (synth-05 cites bare `fsm.py`, `reviewers.py`; synth-06 uses `pr_submit/fsm.py`; both resolve). `scripts/eval_runner.py`, `.dev/eval-workspaces/shadow-model-combos/analysis/extract.py`, both golden fixtures and `src/superclaude/cli/eval/` exist. Only one E2 commit hash appears in the three files (grep for 40-hex strings: 4a22d742... only). |
| 5 | Recommendation names one option and references the Options Comparison | PASS (note N6) | synth-05 line 22: "Option B from 6.X Overall design options ... built through Option A's code ... Option C rejected"; Rationale 1 cites the Options Comparison criteria. synth-04 lines 1441-1453 hold the comparison (Effort A=L, B=XL, C=M; Risk Medium-High for B; PR and rf-qa fit Weak / Strong / Weak) and the identical "Recommended design (not a roadmap)". The 16 DECIDED + 4 debated split (C-03, C-05, C-13, C-14) matches `reviews/adversarial/conflict-index.md`. The 20-row resolution table covers C-01..C-20 once each. |
| 6 | Migration steps are specific (Step / Action / Files / Details name files) | PASS | M1 has 19 steps, M2 10, M3 9, M4 7; every row has a non-empty Files cell with repository paths (and [proposed] markers on new ones), contract fields and tests that change. All 88 `MS-/BL-/DOC-/ENS-/OPEN-` ids and every `SC-nn` cited in the Closes-gaps cells exist in synth-02; every `G-nn` is within G-01..G-94. |
| 7 | REQUIRED-CONTENT CHECK ((b), (d), (e), Section 8 contents) | FAIL (finding F1) | See the table below. All required elements are present; the gate list contains one wrong entry (G9). |

### Required-content result (blocking if missing)

| Required element | Where | Result |
|---|---|---|
| (d) shared core table: finding contract, panel resolution, run manifest, clustering and citation checks, calibration, merge and telemetry | synth-05 7.1.3, 16 rows (finding contract; severity scale and per-consumer mapping; panel resolution; identity check; dispatch; brief and grounding injection; run manifest; telemetry; clustering; citation checks; calibration; blocking decider hook; round model; merge and verdict; built-in run audits; rollout and evaluation instrument) | PRESENT, all required rows and four extra |
| (d) thin-module table: sc:reflect, sc:workflow tasklist review, spec review for brainstorm and design, PR code review, rf-qa / rf-qa-qualitative replacement | synth-05 7.1.4, 6 rows (reflect UC-1, reflect UC-2, workflow/tasklist, spec review, PR, rf-qa) with file:line plug points | PRESENT |
| (d) ASCII diagrams | synth-05 7.1.1 (layers) and 7.1.2 (data flow) | PRESENT |
| (e) exposure list: lenses, categories, roles, templates, model-role mapping | synth-05 7.2: rows Lenses (X1), Categories (X2), Roles (X7), Templates and review kinds (X8), Model-role mapping and strata (X12), plus severity, predicate, four location types, multi-artifact, clustering key, brief slots, rubric, fix-agent hand-off, verdict format, provenance, verification gate, finder adapters, run profile, CLI reachability | PRESENT |
| (e) blocker table with file:line | synth-05 7.3, 35 rows, each with file:line | PRESENT |
| (b) value inventory, every row a destination or DROP with a reason | synth-06 8.1, 691 rows; awk found no empty Destination or Reason cell; 94 DROP rows each with a concrete reason; every one of GQ:C-01..C-25 and GQ:D-01..D-77 has its own row | PRESENT |
| Section 8 migration path | synth-06 8.2, tracks M1 to M4, Goal / Dependencies / step table | PRESENT |
| Section 8 gate list with `uv run` commands | synth-06 8.3, 17 gates, all commands start with `uv run` | PRESENT, one entry wrong (F1) |
| Section 8 branch options stating the git ref constraint | synth-06 8.4, five layouts, constraint stated correctly (`feat/review-panel` and `feat/review-panel/<name>` cannot coexist) | PRESENT |
| Section 8 contains no roadmap | grep for sprint / milestone / week / date / ordering words in synth-05/06/07: none beyond inherited design-stage names (Stage 0, decision gate) and one wording slip (N7); step ids are declared order-free; no `/sc:workflow` plan | PRESENT (note N7) |
| Core verdict vocabulary `[CONTRADICTION]` | raised in synth-05 7.1.3 "Merge and verdict" row, repeated in 7.4.3, and carried in synth-06 M1-07, M1-08, M1-16, M3-08, 8.5 and 8.6; its description matches the C05 merge (PENDING and exit 12 under `--decide grader`, `proposal-merged.md:28,48,113-119`) and the C13 merge (ESCALATE with a reason unless OD-8 chooses PENDING, `proposal-merged.md:110,389,621`) | Explicit flag, consistent across files: allowed |
| Old C14 claim presented as measured fact | grep of synth-05/06/07 for "35 of 39", "driven by", "parsed-sparse", "37 of 38", "input-format", "forcing Tier 2", "normal path": every hit states the recount and marks the older wording as not used (synth-05 lines 18, 284, 291; synth-06 lines 11, 346, 396, 399, 548, 587, 703, 767; synth-07 lines 54, 216) | No blocking occurrence |

## Issues Found

### Findings table

| # | Severity | Synth file | Section | Finding | Required fix |
|---|----------|------------|---------|---------|--------------|
| F1 | IMPORTANT (blocking) | synth-06 | 8.3 gate G9 (line 938); contradicts synth-07 D-43 (line 201) and Q-39 G-53 (line 55) | The G9 row says "Reflect legacy, must not move (271)", command `uv run pytest tests/cli/reflect` "(the remaining 33 files)". Verified: `tests/cli/reflect` holds 38 `test_*.py` files; G8 names 4 of them, so the remainder is 34, not 33 (synth-07 itself says "G9 is 34 files" and "34 legacy reflect files, not 33"). The command as written also collects all 353 tests including G8 (`uv run pytest --collect-only -qq -p no:cacheprovider tests/cli/reflect` prints "353 tests collected"), not 271. The 8.3 intro defines a gate as green only when the command "exits 0 with the stated collected count", so the G9 criterion cannot be met as written, and the G8 pins that are designed to change on purpose would make G9 fail by design. | In the G9 row replace "(the remaining 33 files)" with "(the remaining 34 files)" and make the command select exactly them, for example `uv run pytest tests/cli/reflect --ignore=tests/cli/reflect/test_panel_contract_lint.py --ignore=tests/cli/reflect/test_shadow_skill_contract.py --ignore=tests/cli/reflect/test_shadow_exit_script.py --ignore=tests/cli/reflect/test_verdict_replay_script.py` (re-run `--collect-only` to confirm 271), or keep the plain command and state "353, includes G8". Make the file count agree with synth-07 D-43 and Q-39. |

### Minor notes (do not fail the gate; not rechecked)

| # | Severity | Synth file | Location | Note |
|---|----------|------------|----------|------|
| N1 | MINOR | synth-07 | 10 Synthesis Files table (lines 268-269) | The rows for synth-05 and synth-06 still say "(planned, written in Step 5.3 / 5.4 ...)"; both files now exist. The synth-07 prompt required "planned paths" at write time and the assembler (task file line 348) is told to rewrite them, so this is a hand-off item, not a defect. Drop the word "planned" at assembly. |
| N2 | MINOR | synth-07 | 10 Adversarial Debate Outputs (line 288) | Still the prompt-mandated placeholder "filled after Step 5.2". Task file line 348 tells the Phase 6 assembler to replace it with a Glob of `reviews/adversarial/<slug>/` (four folders exist: `ledger-model`, `model-tier-config`, `panel-size-cost`, `who-judges-blocking`, each with `proposal-merged.md` and `adversarial/return-contract.yaml`) and line 356 makes a leftover "filled after Step 5.2" a blocking finding of the template-conformance QA of the assembled report. Not blocking here; it must not survive assembly. |
| N3 | MINOR | synth-05, synth-06 | synth-05 7.1.3 Finding contract row and Clustering row; synth-06 M1-06 | Two symbol-to-line pairings are off. `findings.py:90-121` is `_check_finding`, while `parse_block` is `findings.py:124-196` (synth-06 M1-01 has it right). `cluster_v2` is at `cluster.py:381` (`cluster.py:381-433` in `research/02:213`), while `:302-378` is `_components` and the chain computation; synth-05 and M1-06 write "`cluster_v2` `:302-378`". The behaviour described is true; only the label-to-range pairing is wrong. |
| N4 | MINOR | synth-05 | External-context table, "Panel independence" row | Reliability is attributed to "(web-03)", but the "nine judges, about two effective votes" finding and arXiv 2605.29800 are in `research/web-01-panel-aggregation.md` section 2.2 (lines 59-60, 145). The claim itself is supported. |
| N5 | MINOR | synth-05 | Rationale 6 | "9 of 38 recorded Tier 2 runs already ran two cards" traces to the C14 debate artifact (`reviews/adversarial/panel-size-cost/proposal-merged.md:236`), not to a research file. It is traceable to a binding input; cite it as such at assembly. |
| N6 | MINOR | synth-05 | Rationale 1 | "A is Weak, C Weak to medium" is given for both PR review and rf-qa; synth-04's comparison (line 1450-1451) says C is "Weak to medium" for PR review but "Weak" for rf-qa. |
| N7 | MINOR | synth-06 | V-588 reason | "not built in the first migration steps" implies a sequence; the section declares steps order-free. Reword to "not built by any step of 8.2". |

## Summary

- Checks passed: 6 / 7 (items 1-6 pass; the required-content check fails on F1)
- Checks failed: 1
- Critical issues: 0
- Important (blocking) issues: 1 (F1)
- Minor notes: 7 (N1-N7)
- Issues fixed in-place: 0 (fix_authorization false; no file other than this report was edited)

Open items stated honestly in the files (verified as stated, not counted as defects): C03 (2 HIGH invariants), C05 (11), C13 (10, never debated), C14 (3) all `partial`; owner items O-1 to O-6, Decision D-1, OD-6 and the C03 flip shape; the core verdict vocabulary `[CONTRADICTION]` (PENDING / exit 12 against ESCALATE with a reason); the corrected parsed-sparse figure.

## Actions Taken

None (report only). Scratch scripts were written under `/tmp/ironclaude-batch.*` and removed in the same call; the C14 recount script was run read-only.

## Recommendations

1. Fix F1 in synth-06 (one table row), then re-check only F1 in fix cycle 1.
2. At assembly (Phase 6): remove "planned" from the synth-05 and synth-06 rows of the Synthesis Files table, replace "filled after Step 5.2" with the four debate folders (N1, N2), and correct the two line-range labels of N3.
3. The coherence and accuracy partitions should cover cross-file consistency between synth-05 and synth-06 beyond this lens; this report limited cross-file checks to the three assigned files.

## Confidence Gate

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (all seven checks, items 1-6 and the required-content check, carry tool evidence; the verdict is FAIL because of F1, not because of low confidence)
- **Tool engagement:** Read: 17 | Grep: 18 | Glob: 2 | Bash: 31 (three of them generated batch scripts under `/tmp`; includes `uv run pytest --collect-only` runs and one read-only run of `recount_tier_decision.py`). Total Read + Grep + Glob = 37, above the 7 checklist items.
- Web research: none needed (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0); web claims were checked against the local `research/web-0*.md` files only.
- UNCHECKED items: none.
- UNVERIFIABLE items: none for this lens. Limits worth stating: the inventory (691 rows) was checked mechanically for structure, completeness against the C and D rows, and a sample of source cells; I did not re-derive every row's source cell from the scope slices. E2 raw data was not re-aggregated (the report itself marks it [DOC-SOURCED]).

## QA Complete
