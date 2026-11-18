# Research Completeness Verification (Partition 2 of 2)

**Topic:** Unified Review Panel (E1 reflect Tier 2 panel, E2 tasklist review-panel study at 4a22d742, E3 #346 review loop)
**Date:** 2026-11-13
**Analyst:** rf-analyst, completeness lens (checklist items 1, 4, 5), fix_authorization: false
**Files analyzed:** 6 (research/07-12)
**Depth tier:** Deep

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports. Files 01-06 were read only where a cross-reference had to be checked.]

---

## Verdict: FAIL — 2 blocking findings (IMPORTANT #4 file 10 census granularity, #6 file 11 exit-script output), 6 MINOR notes

---

## Per-file results

### 07-reflect-merge-contract.md (488 lines, read in full)

**Row 7 coverage (research-notes.md:124).** Key files: SKILL.md §9.1-9.2 (sections 1.6-1.7, lines 58-75), `panel_lint.py` (section 2), `tests/cli/reflect/*` (section 4), `.dev/reflect/pre-*-shadow*/adversarial/` (section 7.2 table, 14 runs), `reflect_shadow_exit.py` (sections 5, 6.1). All covered.
Row topics: debate vs script merge (Q1, :422-426), `merge_method` values and bump rule C3 (Q2, :428), EV-1 (Q3, :430), C1-C16 (section 9, :391-416, all 16 rows), HEAD-relative C1/C6 (Q5, :434), UC-2 `reflect-post` readiness (section 8), Stage 2 exit status (section 5). All answered; no unanswered question.
**Exit-script output:** recorded in full, verbatim, with exit code (`:189-266`, ends `OVERALL: FAIL (shadow runs 13 of 20)` / `EXIT_CODE=1`). I re-counted the derived numbers from the verbatim output and the section 7.2 table: EV-1 failures 8 (04, 08, 09 no contract; 03, 05, 06, 07 absent; 15 zero cards), lint/manifest failures 9, parity failures 6, convergence 1.0 in 9 of 14 rows, `cluster_agreement` 1.0 in 10 of 11, inline judge in 6 runs (04, 09, 10, 11, 12, 13). All match the text at :271-277, :360-361.
**Completeness (item 4).** `Status: Complete` (:5). Key Takeaways after every section 0-10 (:18, :71, :111, :130, :180, :280, :304, :359, :385, :414, :451). `## Gaps and Questions` (:457), `## Stale Documentation Found` (:477), `## Summary` (:486) present. Effort tags: every section heading carries [E1] (or [E1][E2][E3]); cross-effort statements are tagged inline (for example :152, :183, :403, :407-411). Pass.
**Cross-references (item 5).** C1-C16 are taken from slice 03:183-200 and re-verified one by one; telemetry placement (§9.2 nested block) is tied to `panel_lint` L2 and the exit script's `tele()` (:292); test pins are listed per test with line ranges (section 4), which file 12 must agree with (checked under file 12 below). Consistent.
**Known-contradicted claims:** none used. E2 evidence: only the hand-off copy (slice 00 §5.6) is cited; no newer commit or run-2 hand-off is referenced.
**Defects found:** one MINOR. The file's own Stale Doc line :482 says "The task prompt describes `tests/cli/reflect/` as twelve files"; research-notes.md:46 says "`tests/cli/reflect/` (12 files incl. ...)", so the research-notes EXISTING_FILES row itself is wrong (the directory has 38 test files per :139). File 07 flags it correctly; this is recorded so synthesis does not reuse "12 files" (see cross-check under file 12).

### 08-run-recording-telemetry.md (487 lines, read in full)

**Row 8 coverage (research-notes.md:125).** Key files: `manifest.py` (section 1), `manifest_cmd.py` (2), `telemetry.py` (3), `telemetry_cmd.py` (4), E2 audits A and D (8, via `git show 4a22d742`), `extract.py` (10), `reflect_shadow_exit.py` (9). All covered. Row topics: stages/attempts/hashes (1.2-1.3), records/strata D15/kinds (3.1-3.2), reflect `telemetry:` block §9.2 (6), E2 meta/cost/fallback (7), audits A and D as built-in checks (8.3 table), cost and time per reviewer (11.2), combo `extract.py` fields (10). All answered.
**Completeness (item 4).** `Status: Complete` (:5). Key Takeaways after sections 1-11. Section 12 (:436-453) is a doc-claim verification table with no Key Takeaways; it is a tag table rather than a findings section, so this is MINOR. `## Gaps and Questions` (:457), `## Stale Documentation Found` (:477), `## Summary` (:485) present. Effort tags on every section heading and on every Key Takeaway and gap bullet. Pass.
**Cross-references (item 5).** D15 telemetry strata: `telemetry.py:112-115` (sonnet/haiku) [CODE-VERIFIED] here; file 10 relies on the same fact. Reflect `telemetry:` block: same §9.2 line range (:940-989) as file 07, and the same `tele()` dual-placement reading of `reflect_shadow_exit.py:90-95` (file 07 :292, file 08 :352). Parity recompute (`:117-177`) agrees with file 07 section 6.1. Consistent.
**Known-contradicted claims:** none used; file 08 states them correctly (only A and D have `summary.md`, :269 and :449; audit D "3 verdict flips named", :316). E2 evidence: every E2 path is `git show 4a22d742...` (:226); no newer commit.
**D7 line-number cross-check (verified by me against code):** `src/superclaude/cli/review/telemetry.py:22` is `_TS`, :23 is `_ID_TOKEN`, :24 is `_ID_RE`. File 08 (:448, :479) is correct that the hand-off's `telemetry.py:23` was right and that scope slice 02:167/:229 "corrected" it to a wrong line. Files 03:187, 10:188 and 12:180/:331 agree with :23. But research-notes.md:169 and the gate prompt list "stale line numbers for D7" as a known contradiction; for the telemetry half of D7 that listing is itself wrong, and `findings.py:29` is also unchanged. Synthesis must not repeat "the hand-off D7 line is stale". (Recorded as finding 3, MINOR: no assigned file builds a wrong claim on it.)
**Defects found:** MINOR only (section 12 lacks Key Takeaways; finding 3 above is a gate-input note).

### 09-consumer-plugpoints.md (294 lines, read in full)

**Row 9 coverage (research-notes.md:126).** Workflow Wave 4 (section 3, `sc-workflow-protocol/SKILL.md:85-93`), tasklist Stage 10.5 (4.1, `:1619-1646`) and phase post gate (4.2, `:1155-1179`), brainstorm and design with artifact and id convention (6.1-6.3), spec-panel loop prose and the single CLI paragraph (2.1-2.2, prompts `:68-70`), prose-only fallback without the CLI (2.3), D13 loader (1.4, with a new finding: `lint_cmd`/`estimate_cmd` are PN2/PN3 experiment branches), D14 (section 7), whether reflect pre escalates to Tier 2 by default (section 5). All covered and answered; Q8 design input in section 8.
**Completeness (item 4).** `Status: Complete` (:5). Key Takeaways after sections 1-8. `## Gaps and Questions` (:267), `## Stale Documentation Found` (:284), `## Summary` (:292) present.
**Effort tags.** Most findings are tagged, but several are not: section 6.2 bullets on `design.md` (:200-202) carry no effort or consumer tag (section 6.1 uses "[future consumer]" for the same kind of item, :191-195); :90, :148 and every Key Takeaways bullet (:54-56, :107-109, :130-132, :158-160, :181-182, :215-217, :241-243, :261-263) are untagged. The attribution is recoverable from the tagged body bullets above each list, so this is MINOR.
**Cross-references (item 5).** The tasklist post-gate rule "`adversarial_convergence_score < 0.80`" (:154) matches file 07's `contract.py:317-326` 0.80 floor. "Seven real subcommands, no in-repo caller of merge/ledger except the prompts file" (:43, :223-243) matches file 12's statement that D13/D14 are uncovered by tests (12:179-183 region, checked under file 12). Spec-panel's dependency on rf-qa's Fix Cycle steps 1-5 (`spec-panel.md:262`, file 09 :68) is an rf-qa coupling outside `src/superclaude/skills/`; file 10's census is scoped to the skills directory (row 10) and does not list it, so the cross-reference is missing on file 10's side (finding 5, MINOR). Otherwise consistent.
**Known-contradicted claims:** handled correctly. :238 and :275 state that the variant commands are installed in `~/.claude/commands/sc/`, not only in the bundle. E2: no E2 file read; the one E2 claim (how E2 drove spec-panel) is tagged [UNVERIFIED] (:127, :272). No newer commit referenced.
**Defects found:** MINOR only (missing effort tags listed above).

### 10-future-consumers.md (230 lines, read in full)

**Row 10 coverage (research-notes.md:127).** PR review seam with FSM S2-S3 (1.1-1.2), `finding-verify.md` and `severity-routing.md` (1.1, 2), `severity_router.py` in_diff drop and missing `error-handling` row (2, D-a and D-b), Augment/Codex source agreement mapped to ledger confidence (1.2, `ledger.py:86-90`), rf-* census over the 19 skill files with phase, inputs, fix authorization, verdict format and in-place-fix need (3), core exposure list (5, X1-X13), blockers (6). All row topics answered.
**Census check ("one row per call site").** The file defines a call site as "one gate or step in one file" (:78), but three rows bundle several distinct gates, which I confirmed in the skill files:
- Row 7 (`task/SKILL.md:211-217`) is three gates in one row: research gate (2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative), synthesis gate (same mix, different lenses) and task-integrity gate (2 rf-qa + 2 rf-qa-qualitative + 1 rf-analyst; `task/SKILL.md:213-215`). The row gives "analyst + rf-qa + rf-qa-qualitative mixes" and `fix_authorization` "per gate", so the per-gate composition and fix authorization are not recorded.
- Row 17 (`tech-reference/SKILL.md:537-539`) merges Step 6a lens QA plus 6b fix with Step 6c, a separate source-fidelity gate (≥5 rf-qa fidelity agents, `:539`).
- Row 25 (`readme/SKILL.md:600-604`) merges the Phase 6 lens QA/fix cycle with Step 6.3, a separate source-fidelity gate (`:603-604`).
Consequence: the census undercounts call sites (the "39 call sites" and "28 need an in-place fix" at :127, :132 and :230 are computed over these merged rows), and row 7 leaves `fix_authorization` unresolved. This fails the gate's file-10 coverage check (finding 4, IMPORTANT, blocking). I re-counted the "Yes" rows as written: 28, so the arithmetic is internally consistent; only the row granularity is wrong.
**Completeness (item 4).** `Status: Complete` (:5). Key Takeaways after sections 1-6. `## Gaps and Questions` (:204), `## Stale Documentation Found` (:219), `## Summary` (:228). Effort tags: the file defines `[E3-adjacent: master consumer]` for pr-submit, auggie and rf-* facts (:10) and tags each section heading; core facts carry [E1]/[E3]. Pass.
**Cross-references (item 5).** D7 regex at `telemetry.py:23-24` (:188) agrees with code and with files 08 and 12. Telemetry strata (X12, :169) agree with file 08 section 3.2. Reflect's Wave 3B use of rf-qa as read-only reviewers (row 38) is a reflect-side fact that file 07 does not mention; no contradiction. Missing cross-reference: spec-panel's rf-qa Fix Cycle coupling (`spec-panel.md:262`, found by file 09 :68) is not in the census or in the blocker table (finding 5, MINOR).
**Known-contradicted claims / E2:** none used; E2 not read directly, stated at :217 (hand-off only, no newer commit).

### 11-evaluation-evidence.md (403 lines, read in full)

**Row 11 coverage (research-notes.md:128).** E2 harness as a regression benchmark: GT format (section 4), blind judge `judge-one.sh` with no `source.md` (2), anonymisation (2), `final-table.py` and `three-way.py` (3), ~115k judge tokens per scoring (5, tagged [UNVERIFIED] against raw data), `source.md` not committed (4). E1 shadow harness generalisation from SSE:100-123 (7). Stage 2 failure classification of shadow runs 08-15 after `9874d63fb`/`c2e3347d3` (8, with a mtime timeline that answers file 07's open gap at 07:466). Combo study leads (9). E2 headline results (6). Experiment-bundle verdicts (11). Tier 2 cost versus worth (12). All row topics answered.
**Exit-script output check.** The gate requires the full output of `uv run python scripts/reflect_shadow_exit.py` in file 11. Section 8 (:209-217) gives "Key output lines, verbatim", but the bullets are a condensed paraphrase: the per-run parity lines are merged into one sentence ("FAILS for shadow04, 05, 07, 08, 09, 15 ..."), the per-run lint lines are summarised, and the 15 `failure:` lines and the `Stage 2 counts:` block layout are not reproduced. The exit code is recorded (:209). The values agree with the verbatim block in file 07 (07:191-266): same 13/20, 8/13 vs 3/39, same failing and holding runs, 0.704 and 1.000. So no number is wrong, but the required artifact is not in this file (finding 6, IMPORTANT, blocking).
**Completeness (item 4).** `Status: Complete` (:5). Key Takeaways after sections 1-12. `## Gaps and Questions` (:354), `## Stale Documentation Found` (:388), `## Summary` (:401). Effort tags on every section heading, Key Takeaways bullet and gap item. Pass.
**Cross-references (item 5).** Stage 2 numbers and per-run causes match file 07 sections 5 and 7. The `[1m]` unquoted-alias YAML break is reported by both (07:315 for shadow04; 11:231-232 for shadow08/09) and agrees. File 11's timeline (08-11 before `9874d63fb`, 12-15 after, none after `c2e3347d3`) resolves file 07's [UNVERIFIED] gap at 07:466; synthesis should take file 11's version. E2 runner defects (`expected_model` overwrite, cost glob, Bash allowed) agree with file 08 sections 7.2-7.4. Served-model drift (haiku slot served by `gpt-6.1-sol`) agrees with file 08:379.
**Known-contradicted claims.** All handled correctly: 3 named verdict flips (:158, :395), once-found = alias GT1 (B6) (:147, :159, :392), 156 not 161 source-blind runs (:160). No finding builds on a contradicted claim.
**E2 commit check.** Every E2 read is `git show 4a22d742...` (:4, :8). The only other commit is `b4db265a8` (:263), quoted from E1's `PLAN.md:171-174` as the planned GT source; I checked that `b4db265a8` (2026-11-13T01:38Z) is an ancestor of `4a22d742` (2026-11-13T15:55Z), so it is older, not newer, and it is not used as evidence. No run-2 hand-off reference (grep over files 07-12 for "run-2", "run2", "second report": no hit).
**Defects found:** finding 6 (IMPORTANT).

### 12-test-pins-regression.md (348 lines, read in full)

**Row 12 coverage (research-notes.md:129).** The 651 `tests/review` tests by file and stack (section 1), defect pins D3 `test_review_ledger.py:376`, D5 `:408`, D11 `test_review_panel_exclusion.py:208` (3.1-3.3, plus new D2, D4 and D15 pins), golden fixtures (5), reflect pins C1/C6/C7/C8 and the `panel_lint` lists (6), `tests/skills/test_review_*` and `test_spec_panel_review_loop.py` pins (7), the no-regression gate list (8), and the tests that must change on purpose (9). All answered.
**Collect-only check.** Section 0 records the command and its result line (`1182 tests collected`). I re-ran the same collection read-only (`uv run pytest --collect-only -qq -p no:cacheprovider`, bytecode writing off; temp list deleted afterwards): 1182 total, 651 / 353 / 178 per area, and every per-file collected count in the section 1 and 2 tables matches my run (for example findings 23, ledger 24, cli 13, panel 41, card_convert 119, cluster 113, panel_contract_lint 38, verdict_mapping 36, spec_panel_review_loop 46, severity_rule 62). Pass.
**Count defect.** File 12 says `tests/cli/reflect/` holds **37** test files and that "the other 33" predate the panel (:19, :23, :72, :277 "remaining 33 files", :327, :348). My collection drew items from **38** files, and `ls tests/cli/reflect/test_*.py` returns 38. File 12's own section 2 table lists 38 files. File 07:139 also says 38. The correct figures are 38 files and 34 legacy files (the 271 legacy items are correct). This is a contradiction between files 07 and 12 (finding 8, MINOR: test counts and gates are right; only the file count is wrong).
**Completeness (item 4).** `Status: Complete` (:5). Key Takeaways after sections 0-9 (section 3.7 sits under section 3's takeaways; acceptable). `## Gaps and Questions` (:322), `## Stale Documentation Found` (:338), `## Summary` (:346). Effort tags on every table row and section heading; the section 0 and 1 Key Takeaways bullets (:26-28, :67-68) are untagged, which is MINOR and covered by finding 7's pattern.
**Cross-references (item 5).** C1/C6/C14 HEAD-relative conclusion matches file 07 section 4.1 and Q5. `panel_lint` 110/27 sizes and `LEGAL_MERGE_METHODS` at `:184` match file 07 section 2.1. D15 strata pin (`test_review_telemetry.py:327`) matches file 08 section 3.2. D13 uncovered matches file 09 section 1.4 (no test pins the registered set). D7 `telemetry.py:23` agrees with file 08 and code. Consistent apart from finding 8.
**Known-contradicted claims.** D2 handled correctly: file 12 states the `ledger.py:112` docstring is contradicted by `:254-258` (:130, :332) and does not build on it. D7 line: correct (:331). No E2 file read; no newer E2 commit.
**Defects found:** finding 8 (MINOR).

---

## Coverage Audit

| Scope item (research-notes row) | Covered by | Status |
|---|---|---|
| Row 7: SKILL.md §9.1-9.2, `panel_lint.py`, `tests/cli/reflect/*`, shadow `adversarial/` dirs, `reflect_shadow_exit.py` (full output) | 07 | COVERED |
| Row 8: manifest, telemetry, E2 meta/cost/fallback, audits A and D, `extract.py`, exit script | 08 | COVERED |
| Row 9: workflow, tasklist, brainstorm, design, spec-panel, prompts file, `__init__.py` loader, D13, D14, default Tier 2 escalation | 09 | COVERED |
| Row 10: PR seam, severity router vs rubric, source agreement, rf-* census, core exposure | 10 | COVERED, census granularity defective (finding 4) |
| Row 11: E2 harness, E1 shadow harness, Stage 2 runs 08-15 with exit-script output, combo leads, E2 headline, bundle verdicts | 11 | COVERED, full exit-script output missing (finding 6) |
| Row 12: test inventory, defect pins, goldens, reflect pins, skill pins, gate list, migration | 12 | COVERED |

## Completeness

| Research file | Status | Summary | Gaps section | Stale Doc section | Key Takeaways | Effort tags | Rating |
|---|---|---|---|---|---|---|---|
| 07 | Complete | Y | Y | Y | Y (all sections) | Y | Complete |
| 08 | Complete | Y | Y | Y | Y except section 12 | Y | Complete (MINOR) |
| 09 | Complete | Y | Y | Y | Y | partial (finding 7) | Complete (MINOR) |
| 10 | Complete | Y | Y | Y | Y | Y | Complete |
| 11 | Complete | Y | Y | Y | Y | Y | Complete |
| 12 | Complete | Y | Y | Y | Y | Y (takeaway bullets untagged) | Complete (MINOR) |

## Contradictions Found

- `tests/cli/reflect/` file count: file 07:139 says 38 test files; file 12:19, :23, :72, :327, :348 say 37. Code: 38 (`ls`, and the collection draws from 38 files). Also research-notes.md:46 says 12.
- Which shadow runs predate the fixes: file 07:466 leaves it [UNVERIFIED]; file 11:223 establishes it by mtime and brief text. Not a contradiction; synthesis should use file 11.
- D7 telemetry line: scope slice 02:167/:229 says `telemetry.py:22` and calls the hand-off's :23 stale; code and files 08, 10 and 12 show :23 is `_ID_TOKEN`. File 03:386 (partition 1) still repeats slice 02's remark that the hand-off's :23 meant `_ID_RE`.

## Compiled Gaps

### Critical Gaps (block synthesis)
- None.

### Important Gaps (affect quality; blocking under this gate)
- File 10 census rows 7, 17 and 25 each bundle several gates; row 7 leaves `fix_authorization` as "per gate" (finding 4).
- File 11 does not contain the full exit-script output that the gate requires (finding 6).

### Minor Gaps (notes; do not block)
- Open [UNVERIFIED] items carried by the files themselves: sprint/promotion-gate routing (07), the audit-D chain-replay script (08), the installed `superclaude` binary's subcommands (09), `classifier.py` root fields and census rows 18/22 (10), raw E2 `score.json` re-aggregation and the ~115k judge tokens (11), bodies of most v2 test files (12). Each is tagged and listed in the file's Gaps section, so synthesis can carry them as open questions.

## Depth Assessment

**Expected depth:** Deep.
**Actual depth achieved:** Deep. Each file traces code paths with file:line evidence, re-runs commands (exit script, `--collect-only`, `--help`, greps, `git ls-tree`), re-counts derived numbers, and adds new code-verified findings beyond the scope slices: the `[1m]` YAML break, EV-1 self-attestation, PN2/PN3 origin of the ghost loader names, the D2 pin, the GLM/Qwen orchestrator in combo A, and the shadow-run timeline.
**Missing depth elements:** only the per-gate split in file 10's census (finding 4).

## Recommendations

- File 10: split census rows 7, 17 and 25 into one row per gate, fill agent counts and `fix_authorization` for each, and recompute the call-site and in-place-fix totals in the table footer, Key Takeaways and Summary.
- File 11: replace the condensed bullets in section 8 with the complete verbatim output of `uv run python scripts/reflect_shadow_exit.py` (or the identical block from file 07:191-266, stating the run date and HEAD).
- Synthesis: use 38 `tests/cli/reflect` test files (34 legacy); do not repeat "hand-off D7 line stale" for `telemetry.py:23`; use file 11's shadow-run timeline.

---

## Findings

| # | Severity | File | Finding | Remediation |
|---|---|---|---|---|
| 1 | MINOR | research-notes.md:46 (flagged by 07:482 and 12:327) | EXISTING_FILES says `tests/cli/reflect/` has 12 files; it has 38 test files | Synthesis uses 38; no research-file change needed |
| 2 | MINOR | 08-run-recording-telemetry.md:436-453 | Section 12 (doc-claim tag table) has no Key Takeaways | Optional: add a one-line takeaway |
| 3 | MINOR | gate input / research-notes.md:169; scope slice 02:167, :229; 03-clustering.md:386 | The "stale hand-off line for D7" contradiction is itself wrong for `telemetry.py`: :23 is `_ID_TOKEN` (verified in code), as the hand-off said; files 08:448/:479 and 12:331 are correct | Synthesis must not state that the hand-off's D7 telemetry line is stale |
| 4 | IMPORTANT | 10-future-consumers.md:92 (row 7), :102 (row 17), :110 (row 25); totals :127, :132, :230 | Census is not one row per call site: row 7 bundles the research, synthesis and task-integrity gates of `task/SKILL.md:211-215` with `fix_authorization` "per gate"; row 17 bundles `tech-reference/SKILL.md` Step 6a/6b with the separate Step 6c fidelity gate (:539); row 25 bundles the readme Phase 6 lens cycle with the separate Step 6.3 fidelity gate (`readme/SKILL.md:603-604`). Call-site totals are undercounted | Split each bundled row into one row per gate with its own agents, inputs, `fix_authorization`, verdict format and in-place-fix flag; recompute "39 call sites" and "28 need in-place fix" wherever stated |
| 5 | MINOR | 10-future-consumers.md section 3 and 6 | Missing cross-reference: `spec-panel.md:262` makes spec-panel's re-check depend on rf-qa's Fix Cycle steps 1-5 (found by 09:68); outside the skills-only census scope, so not listed as an rf-qa coupling | Add a note or a blocker-table row for the spec-panel rf-qa coupling |
| 6 | IMPORTANT | 11-evaluation-evidence.md:209-217 | The gate requires the full output of `uv run python scripts/reflect_shadow_exit.py` in file 11; section 8 gives a condensed paraphrase (merged parity and lint lines, no `failure:` lines). Values agree with file 07's verbatim block | Insert the complete verbatim output with exit code, run date and HEAD into section 8 |
| 7 | MINOR | 09-consumer-plugpoints.md:90, :148, :200-202 and every Key Takeaways list | Some findings carry no effort or consumer tag (design.md bullets in 6.2, all takeaway bullets) | Optional: add [E1]/[E2]/[E3] or "[future consumer]" tags |
| 8 | MINOR | 12-test-pins-regression.md:19, :23, :72, :277, :327, :348 | Says `tests/cli/reflect/` has 37 test files and 33 legacy files; it has 38 and 34 (my collect-only run and `ls`; file 12's own table lists 38; file 07:139 says 38). Collected test counts are all correct | Change 37 to 38 and 33 to 34 |

**What was checked:** all six assigned files read in full; research-notes rows 7-12 and EXISTING_FILES; scope slices 00 and 02 at the D7 rows; code at `telemetry.py:21-24` and `findings.py:25-32`; `task/SKILL.md:209-218`, `tech-reference/SKILL.md:536-540`, `readme/SKILL.md:600-604`, `roadmap/SKILL.md:589` and `:1846`; a read-only `--collect-only` re-run with per-file counts; `ls` of `tests/cli/reflect`; `git merge-base` for `b4db265a8` vs `4a22d742`; greps of files 07-12 for run-2 references, non-4a22d742 E2 commits and each known-contradicted claim. No research file was modified.

## Verdict: FAIL (2 blocking findings: #4, #6; 6 MINOR notes)
