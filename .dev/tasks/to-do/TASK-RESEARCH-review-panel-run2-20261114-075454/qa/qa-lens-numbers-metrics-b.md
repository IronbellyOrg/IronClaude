# QA Report: numbers-metrics lens, instance b

**Topic:** one unified central Review Panel (shared core plus thin modules) from E1, E2 and E3 (run 2, report only)
**Phase:** report-qualitative (numbers-metrics lens, instance b)
**Range reviewed:** lines 2115 to 5057 of `RESEARCH-REPORT-review-panel-unification-run2.md` (Sections 6 to 10, Appendix A pointer, Appendix B); lines 1 to 2114 checked by Grep only for shared figures.
**Grading:** grading-override.md applies (BLOCKING only if a decision/recommendation/number it rests on is wrong, a required deliverable is missing, or safety risk).
**Overall Verdict:** PASS (zero blocking findings under the grading override; 8 minor notes)
**Status:** Complete

---

## Progress notes

### Checks completed (sections 6 and 7, read-only)

| # | Quantity | Where | Verified by | Result |
|---|---|---|---|---|
| 1 | file line counts findings_v2 304, cluster 487, verify_cmd 184, manifest 534, panel 707, card_convert 517, findings 457, ledger 494, merge_cmd 118, ledger_cmd 137 | 6.1 Reuse rows | `wc -l` on each file at HEAD | all match |
| 2 | tests/review has 19 modules; cli/review has 25 tracked files | 6.1, 7 F-2 | `ls tests/review/*.py`; `git ls-files src/superclaude/cli/review` | 19 and 25 match |
| 3 | 36 verdict-matrix tests | 6.4, 7 | `grep -c 'def test_'` on `tests/cli/reflect/test_verdict_mapping.py` | 36 |
| 4 | `card_convert.py` MAX_CLAIM=300 at :86, cut to 297+`...` at :199-201 | 6.3 | `sed` on the file | match |
| 5 | line cites findings.py:104-106, ledger.py:150-157, findings.py:346-349, findings_v2.py:122-125, cluster.py:256-257 | 6.1 to 6.4 | `sed -n` | content matches each claim |
| 6 | 92 = 56+18+14+3+1; 49 = 24+14+10+1; 88/92 = 95.7 %; 48/49 = 98.0 %; 264 = 89x3; per-model list 30+33+14+7+7+1 = 92 | 6.3 | arithmetic | correct; units (lines vs reviewer-runs 80 vs blocking 49) kept apart |
| 7 | conflict log totals 189 rows, 134 decided, 55 routed | 6.12.10 | row counts per table over lines 3171-3457 (16/22/36/31/41/15/28 rows; UNDECIDABLE-bearing rows 6/1/22/6/20/0/0) | all match |
| 8 | 15 debate scores, margins, convergence figures | 6.12.9.1, 7 axis table, A-3..A-20 | arithmetic on every pair plus Grep of the 15 `ADJUDICATION-RESULT.md` files | every score, margin and convergence figure matches its source file |
| 9 | tiebreaker points C-01 10+2+7+4 = 23 | 7 axis 1 | source file line 22 | match |
| 10 | 7.3 invariants 60/161/23 = 244; per-slot HIGH/MEDIUM/LOW and addressed totals | 7.3 | awk count over the 244 rows and arithmetic | all match; HIGH counts quoted in 6.12.9.1 and the A-rows agree with 7.3 |
| 11 | A-3..A-20 = 18 rows; 12 differ + 6 confirm = 18 | 7 choices table | count | match |

### Checks completed (section 8, read-only)

| # | Quantity | Where | Verified by | Result |
|---|---|---|---|---|
| 12 | 8.1.0 destination table: every row sum, every column sum, grand total 5,950; 5,779 ledger + 171 register rows | 8.1.0, 8.1.2 | arithmetic, then an awk recount of `synthesis/synth-08-value-inventory.md` by ledger prefix and by `### <DESTINATION>` heading (all 70 cells) | all 70 cells and all totals match exactly; file is 6,127 lines and 2,024,775 bytes as stated |
| 13 | source ledgers 886/868/1,685/955/796/589 rows; register 171 rows, 216 `\| DR-` lines | 8.1.0 | `grep -c` on research 19 to 24 and 17 | match |
| 14 | DROP by reason 1,753+126+86+4 = 1,969; 161 = 118+43; 162+9 = 171 | 8.1.0 | arithmetic | correct |
| 15 | P3-014 table 214-28-2 = 184; 124-30 = 94; 23-9-3 = 11; 70 moved = 28+30+9+2+1; exchange list 20 + 29 = 49; reasons 49+7+3+3+4+4 = 70 | 8.1.3 | counted the row IDs in each list | all consistent |
| 16 | "59 register rows are UNVERIFIED" | 8.1.4 limit 3 | awk over research 17 (cells beginning UNVERIFIED) | 59 |
| 17 | 110 stable fields, 27 telemetry fields, version 1.8.0, `LEGAL_MERGE_METHODS` 2 values | 8.2 C1, G2 | imported `panel_lint` with `uv run python` | match |
| 18 | `contract.py:138`, `:321`; test file lines `:22`..`:609`, 0.75 test `:432`, 0.80 test `:447` | 8.2 C3 | `sed`, `grep -n` | match |
| 19 | plugins/superclaude: 125 tracked files, 4 skills, 28 commands | 8.2 C8 | `git ls-files`, `ls` | match |
| 20 | 148 `src/superclaude` lines in 56 files; reflect dir 8 + 10 | 8.2 C7, G10 | `grep -rn` and `grep -rln` over the six directories | match |
| 21 | 9 templates under `cli/review/data`; `slot_id` 24 hits over 8 templates; 19 `tests/review` files | 8.2 G8, D11 | `ls`, `grep -c` | match |
| 22 | cli/review 16 Python files, 5,086 lines, 25 tracked files | 8.2 (e) | `git ls-files`, `wc -l` | match |
| 23 | 38 reflect test files + conftest + `__init__` + fixtures | 8.2 G4, (e) | `ls tests/cli/reflect` | match |
| 24 | 25 file line counts (contract 420, panel_lint 366, ensemble 895, runner 834, fsm 1257, conflicts 1659, rf-qa 551, rf-qa-qualitative 1154 and others), pr_submit total 6,511 lines | 8.2 (e) | `wc -l` | all match |
| 25 | 44 `subagent_type: rf-*` lines in 8 SKILL.md (23/12/4/1x5) | 8.2 (e) | grep per file | match |
| 26 | permutation floors 2/C(8,4) = 0.0286, 2/C(10,4) = 0.0095; pair-label TP 21 FP 4 FN 1 TN 24, precision 0.84, recall 0.9545; 0.12 x 14 = 1.68; EV-1 8/13 = 0.615, 3/39 = 0.077 | 8.2 AE-5, AE-10, G25, G7 | arithmetic | correct |
| 27 | 8 swarm lens entries plus `custom` | 8.2 (e) | `sed` of `lenses/__init__.py` | match |

### Checks completed (sections 6.5 to 6.11, 9, 10, Appendix; read-only)

| # | Quantity | Where | Verified by | Result |
|---|---|---|---|---|
| 28 | 92 = 56+18+14+3+1 by reason and 30+33+14+7+7+1 by model; 49 blocking; 3 verdict flips | 6.3, 6.12.9 C-06 | re-read the primary data: `git show 6c09843...:.../audit-D/summary.md`, `flags.tsv` (49 rows with first field `3-dropped-blocking`), `audit2.json` keys; per-model reason split re-added (anchor 27+24+5 = 56, anchor2 2+7+8+1 = 18, claim 1+2+1+7+3 = 14) | all match the primary files |
| 29 | static kit +59 % elapsed (281.567 s vs 176.9175 s) and +55 % tokens (46,018 vs 29,655); 131 of 147 catches = 89 % (63+50+18); 510 of 1,047 citations = 48.7 %, 472 of 510 = 92.5 %; 0.704 over 9 runs / 0.867 over 15; 11 of 15; 7 of 15 | 6.6, 6.2, A-rows | recomputed ratios with `uv run python`; located each figure in research 07, 08, 09, 10, 16 and the debate probe | all match; sources are research files tagged by their authors |
| 30 | 36 conflicts in R09 = 13+4+4+15 | 6.6 | arithmetic | sums to 36 |
| 31 | gaps log 555 rows, tags 243+187+67+58, status 192+363 | 10 Gaps Log | read the file's own Counts section; `grep -c` of `\| GQ-` rows | match |
| 32 | 93 questions Q-01..Q-93 in Section 9; 14 pr-submit refs; 96 `combos/` directories (97 entries) at the E2 tip | 9, 8.2 OQ24, App. B | `grep`, `ls`, `git ls-tree` | match |
| 33 | QA report tables 42 + 25 = 67 files at assembly | 10 | counted both table bodies (42 and 25 rows) | match (the directory holds 94 files now because later gates added files; the report says so) |
| 34 | 15 `ADJUDICATION-RESULT.md` files; 15 debate folders; slot list C-01..X-15 | 6.12.9, 10 | `ls reviews/adversarial/` | 15 |

## Issues Found

Grading is by `qa/grading-override.md`. No finding below changes a decision, a recommendation, a value-inventory destination, a conflict-log outcome or a number the recommendation rests on, and none is a missing deliverable or a safety risk, so every finding is minor under the override. The severity label (CRITICAL / IMPORTANT / MINOR) is an information label only.

| # | Severity (label) | Section | Finding | Evidence | Proposed Fix |
|---|---|---|---|---|---|
| 1 | IMPORTANT label, (minor under grading override) | 6.12.9 C-10 row (line 3473), 7.2 text (3710, 3779), 8.2 G14 (4438), 8.2 (e) PR module (4552); also 2.7 (1312, outside my range) | "50 test files" under `tests/pr_submit`. At HEAD there are 47 `test_*.py` files (49 `.py` entries with `conftest.py` and `__init__.py`; `git ls-files tests/pr_submit` gives 91 files with fixtures). Line 3772 of the same report reads "50 files, 47 `test_*.py`", so the report is internally inconsistent about the unit. | `ls tests/pr_submit/test_*.py \| wc -l` = 47; `ls tests/pr_submit/*.py \| wc -l` = 49; research/13 line 34 says "50 `.py` test files plus conftest and `__init__`" | Replace "50 test files" with "47 `test_*.py` files" everywhere, or state the unit. No decision depends on it (the C-10 open point is that the additive Output Contract key was not run against the tests). |
| 2 | IMPORTANT label, (minor under grading override) | 6.4 Option 3 "Reuse of existing code" (line 2406) | "14 degraded triggers at `:263-358`". `_degraded_reason` in `contract.py` has 12 distinct reason slugs (`degraded-components`, `degraded-tier1`, `degraded-model-diversity`, `single-vendor`, `adversarial-unavailable`, `single-reviewer-fallback`, `null-convergence`, `degraded-subrun-partial`, `low-convergence`, `verification-skipped`, `citations-dropped`, `input-drift`). The research file that the figure comes from (research/06 line 33) says "14" and then lists those same 12. | `sed -n 263,358p src/superclaude/cli/reflect/contract.py \| grep -nE 'return '` gives 12 returns plus `return None` | Change "14" to "12". The option's effort and risk cells do not use the count. |
| 3 | MINOR, (minor under grading override) | 8.1.1 "Cross-ledger duplicates (P3-011)" (line 4246) | "a read-only scan of the 3,989 rows that are not DROP". The final inventory has 5,950 - 1,969 = 3,981 non-DROP rows. The 3,989 is the figure before the Gate 2 fix moved 8 rows to DROP (the same section says so for the 114/39 pair counts). | arithmetic on 8.1.0; Appendix A recount (DROP = 1,969) | Write "3,989 rows (before the Gate 2 fix; 3,981 after)" or update the number. |
| 4 | MINOR, (minor under grading override) | 8.2 (c) D24 (line 4482) | "The synthetic-dnsp definition appears in five files (30 lines)" has no scope. The count (5+2+3+11+9 = 30) is exact for `src/superclaude/{agents,skills}` only. A grep over all of `src/superclaude` gives 7 files and 36 lines: `templates/modularization-template-review/INDEX.md` (2) and `synthetic-dnsp-finding.contract` (4) are two more places. | `Grep synthetic-dnsp src/superclaude` count mode: 7 files, 36 occurrences; research/13 line 123 scopes its grep to `{agents,skills}` | Add "(under `src/superclaude/{agents,skills}`)" and mention the template contract file. |
| 5 | MINOR, (minor under grading override) | 8.2 (c) D21 (line 4479) | "`cli/swarm` is imported by 38 files". 38 is the count of `src/superclaude` Python files that import `superclaude.cli.swarm`, and 32 of them are inside the swarm package itself; 6 files outside it import it. The point of the row (reflect imports swarm, review does not) is unchanged. | `grep -rlE 'superclaude\.cli\.swarm\|from \.\.swarm' src/superclaude --include='*.py'` = 38; same excluding `cli/swarm/` = 6 | Say "6 files outside the swarm package (38 counting the package itself)". |
| 6 | MINOR, (minor under grading override) | 6.4 mechanism table, `derive_verdict` row (line 2374) | "BLOCKED 2, DEGRADED 11, HALTED 10, PASS 0" has no unit. They are exit codes (`models.py:44-49`), but sit beside "19 fields" and, in Option 3, "14 degraded triggers", so a reader can take them for trigger counts. | `sed -n 44,49p src/superclaude/cli/reflect/models.py` | Write "exit codes: BLOCKED 2, ...". |
| 7 | MINOR, (minor under grading override) | 6.6 (line 2534) against 6.12.10 Table C | R09's own classification of the 36 collaboration conflicts (13 decided, 4 partly, 4 not decidable, 15 design decisions) and the conflict-log split of the same 36 rows (14 decided, 22 routed) use different taxonomies; the report gives the first without saying the second differs. Both add up (36). | arithmetic; counted Table C rows (36, 22 containing UNDECIDABLE) | Add "(R09's own taxonomy; the conflict log uses 14 / 22)". |
| 8 | MINOR, (minor under grading override) | `qa/report-size-and-partition.md` line 10 (not part of the report) | The partition note gives Appendix A as 6,121 lines; the file has 6,127 lines (`wc -l`), which is the figure the report uses everywhere (lines 4215, 4255, 4892, 5033). | `wc -lc synthesis/synth-08-value-inventory.md` = 6127 lines, 2024775 bytes | Orchestration note only; correct it or ignore. |

Items checked and found without defect, by checklist line:

- (a) internal consistency: row/column sums of the 8.1.0 table, the 6.12.10 summary (189 = 134 + 55), the 7.3 invariant register (60 + 161 + 23 = 244, every per-slot split and addressed total), the 18 A-rows (12 + 6), the 15 debate scores and margins (each margin equals the score difference), convergence ratios (C-07 21 of 26 = 80.77 %), P3-014 moves (28 + 30 + 9 + 2 + 1 = 70) and the same quantity across sections (92 / 80 / 49; 110 and 27 fields; 36 tests; 25 tracked files; 5,950 rows; 6,127 lines) all agree.
- (b) units and sources: 6.3 keeps 92 findings, 80 reviewer-package runs, 49 blocking lines and 264 merges apart with a table and an explicit "not the breakdown of the 49" note. E1 recount figures carry status (7 axis 8: "run counts 13 pilot, 15 combo, 28 runs, 8 of 13, 6 of 13 were not re-derived"; 6.3 Option 1 calls the 95.7 % and 98.0 % "an upper bound" and "a derivation, not a measurement").
- (c) 60 or more size and count metrics were checked against code, git data or research files (tables 1 to 34 above).
- (d) collaboration estimates: the +59 % and +55 % are measured (n = 3, one package) and labelled so; the +29 % kit estimate and the reach and act probabilities are named at line 3064 of the report among the planning values that stay unverified (found by grep; I did not read that block in full); the 6.12.9 C-12 row and the A-18 row keep "no arm beat A2" as unmeasured. No unsourced statistic was presented as fact in the range.

## Summary

- Checks passed: 4 / 4 lens checklist items (a to d), with 8 minor notes
- Checks failed: 0
- Blocking findings under the grading override: 0
- Minor findings under the grading override: 8 (findings 1 to 8)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false; nothing but this report was written)

## Self-Audit

**(a) Reliance list:** no Inherited Structural Verdict was supplied in the spawn prompt, so nothing was relied on from rf-qa; every figure was checked from primary files.

**(b) Independent semantic checks:**
- Value-inventory destination table (the 70 cells of 8.1.0): recounted from `synth-08-value-inventory.md` by an awk pass over ledger prefix and `### <DESTINATION>` heading; all match.
- Debate scores, margins and convergence (15 debates): compared with line-level Grep of each `ADJUDICATION-RESULT.md`; all match.
- The 92 / 49 / 3 figures that carry the limits-policy recommendation: recomputed from the E2 primary files through `git show 6c0984326...:.../audit-D/{summary.md,flags.tsv,audit2.json}`; match.
- Code facts: `wc -l`, `sed -n`, `grep -c`, `git ls-files` and one `uv run python` import against HEAD for 40 or more sizes, line cites, counts and constants; found the three count discrepancies (findings 1, 2, 5) and the scope gap (finding 4).

**Confidence:** Verified: 4/4 checklist items (34 numbered check rows plus the arithmetic checks inside them) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0 %. Limits: figures that exist only in E2 data not in HEAD (for example the 71 stored rows, 65 versus 38 judge versus real blocking, E2 test counts 138/358/89/106/108) were checked for consistency with research files and, for the 92/49/3 set, against the E2 tip, but not recomputed from raw data. I did not read lines 2438 to 3106 and 3650 to 3934 line by line; I read the section 6.6 opening, the 6.12 conflict log, the full 7 axis and choices tables, 7.3 headers and summary, and ran numeric greps over the rest of 6.5 to 6.11. Quantitative claims there were checked by pattern (percent, "of N", counts) rather than every sentence.

**Tool engagement:** Read: 17 | Grep: 9 | Glob: 0 | Bash: 21 (read-only: `wc`, `sed -n`, `grep`, `ls`, `git ls-files`, `git ls-tree`, `git show`, one `uv run python` import and arithmetic). Tavily and WebSearch: not used (no external lookup needed). Tool calls (Read + Grep + Glob = 26) are fewer than the 34 numbered check rows because several rows were verified in one batched Bash call; each row cites its own command.

## Recommendations

- Verdict PASS under the grading override. No fix pass is needed for this lens.
- Add findings 1 to 8 to the follow-up list for the owner (all minor under grading override).

## QA Complete

**Overall Verdict: PASS** (zero blocking findings under `qa/grading-override.md`; eight minor notes)
**Status:** Complete
