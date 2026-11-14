# QA Report - Gate 1 Fix Verification (structural), cycle 1

**Topic:** review-panel run 2 (Phase 3 research files 01-24)
**Date:** 2026-11-14
**Phase:** fix-cycle (verification 1, structural)
**Fix cycle:** 1
**fix_authorization:** false (report only)

Status: Complete

---

Scope: the 11 blocking findings of table 1a of `qa/qa-consolidated-findings-phase3.md` (P3-001 to P3-010 and P3-013). Tables 1b and 1c are out of scope (owner decision). The fix log `qa/qa-fix-log-phase3-c1.md` was not trusted: every cited location was re-opened in the research file and every code claim was re-derived at HEAD (`/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`). No research file and no task file was modified.

## 1. Finding ID | FIXED or STILL-OPEN | evidence

| Finding ID | FIXED or STILL-OPEN | evidence |
|------------|---------------------|----------|
| P3-001 | FIXED | research/10 L27 now quotes the docstring in full and says it matches the code [CODE-VERIFIED]; Gaps item 2 (L215) retracted as a gap; Stale Documentation bullet 1 (L234) now says "No stale claim found". Re-read `src/superclaude/cli/review/findings_v2.py:3-4` (full sentence ends "a line that carries calibrated_confidence is rejected") and `:96-97` (`if "calibrated_confidence" in obj: return ...`): the docstring is accurate, so the retraction is correct. The K6 resolution (extra keys accepted) is kept. |
| P3-002 | FIXED | research/13 L179 row P4 now reads "Medium has at least six uses, research/12 section 3 and :218, [CODE-CONTRADICTED] against slice 12 I1's four". research-notes.md L89 and L176 carry the same correction. research/12:82 and :218 hold the six-use re-derivation. `card_convert.py:81-82` `MINOR_WORDS = frozenset({"minor", "medium", ...})` confirms the new citation. The only remaining "four meanings" hits are the quoted stale item at 12:218 and the read-only slice inputs under research/scope/. |
| P3-003 | FIXED | research/01 L87 (grid row 7, E1 cell) and L150 (s4.3 row 7) now say the `cli/review` kernel has no ledger, rounds or reviser, and that the reflect code wrapper has a dormant `--fix` loop, with the old text marked [CODE-CONTRADICTED]. Re-read `src/superclaude/cli/reflect/runner.py:748-793` (`while True:`, `if not config.fix: break`, `classify_fix(...) != "auto-fixable"`, `_apply_remediation(...)`, `iteration > max_iters`) and `:474-478` (`--remediate` appended under `config.fix`): citations exact. research/06:149 and :167 support "dormant" (engine A emits no remediation pointer). |
| P3-004 | FIXED | research/16 L56 (Part 2.3), L79 (Part 2 Key Takeaway), L272 (Gaps 6), L284 (Q6) and L301 (Summary) now say j1 is the sonnet + 2x luna challenger family, absent from the six audits but hand-audited in research/08 s6, with 08 as the stronger side. Re-read research/08 L89-107: 45 of 45 `model_ok` and `expected == observed`, no run under 1,000 tokens, no attempt>1, sensitivity table S0 to S4, S3 found mean 2.83 vs S0 2.33, "Decision: j1 being unaudited does NOT invalidate not confirmed", two luna refusals j1-r2 and j1-r4. Every number quoted in 16 matches 08. L136 and L189 ("batch j1 not audited") stay true. |
| P3-005 | FIXED | research/13 L270 (Stale Documentation bullet 1), L214 (row M1) and L278 (Summary) now say the v2 PARSER accepts citations but the ledger/merge/annotate path needs `anchor`, and the old "NOT a core blocker" sentence is marked [CODE-CONTRADICTED]. Re-read `findings.py:346-349` (`spans = locate(text, finding["anchor"])`, no `.get`) and `ledger.py:127-138` (`fnd.parse_block` then `fnd.annotate(f, doc_text)`); research/01:53 probe P-a and :230 conflict C-3 carry the KeyError. The KeyError was read from the code, not re-run (see note N-3). |
| P3-006 | FIXED | Re-ran both patterns over `src/superclaude/skills/*/SKILL.md`: the U2 pattern gives 175 lines in 7 files (task-builder 45, tech-research 41, roadmap 32, readme 16, tech-reference 14, task 14, operational-guide 13); the structured pattern gives 44 lines in 8 files (task-builder 23, roadmap 12, task 4, one each in tech-research, tech-reference, tdd, prd, operational-guide). research/24 VL-24-444 (L457), VL-24-464 (L477), the verification note (L614) and the Summary (L647), and research-notes.md L72, now carry 175 / 44 and mark slice 12's 185 [CODE-CONTRADICTED] or [UNVERIFIED, not reproducible]. The other "185" hits in 24 (L142, L198, L355) are line cites, not the census. |
| P3-007 | FIXED | Re-ran at HEAD: `wc -l` src 490, plugin 476; `diff src plugin \| grep -c '^[<>]'` = 18; diff hunks at src lines 23, 37, 221, 268 and 454-465 only, so none falls in Review Loop bullets 1-7 (src L256-264; the hard gate is the separate heading at L266, the changed sentence at L268); plugin L266 holds the `${CLAUDE_PLUGIN_ROOT}` fallback, so "softens" is false. research/24 VL-24-211 (L224), VL-24-497 (L510), VL-24-486 (L499), VL-24-487 (L500), VL-24-488 (L501), VL-24-396 (L409), VL-24-570 (L583), the verification note (L615) and research/14 Gaps item 10 (L246) now carry 18 / extended / six uses / six label sets. VL-24-499 and VL-24-501 (L512, L514) carry nothing on this contradiction (the finding's L499 and L501 are VL-24-486 and VL-24-488). New row defect in VL-24-211: see section 2. |
| P3-008 | FIXED | research/09 L126 (s4.2 item (i)) and L129 (Key Takeaways first bullet) now say F1 "needs neither a hook nor a model-side write", is expressible in every runtime but has no clean measured success (both r3 A3 smoke rows `phase2_timeout` 1, r3 luna kill-text FAIL [UNVERIFIED-slice], `--resume` for gateway ids [UNVERIFIED]); the unsupported "works for a swarm or any runtime" and "works in every runtime" are gone. research/09 L76 holds the `phase2_timeout` 1 rows; research-notes.md:262 holds the [UNVERIFIED] `--resume` row. |
| P3-009 | FIXED | Re-ran: `return-contract.yaml` exists in shadow04 (5,648 bytes), shadow09 (5,707) and shadow08 (5,637); `yaml.safe_load` (via `uv run python`) raises `YAMLError ... expected ',' or ']', but got '['` at line 103, column 18 in all three; line 103 is `reviewer_models: [claude-gw-tier1b[1m], ...]`. `scripts/reflect_shadow_exit.py:74-79` `_yaml_map` returns None on YAMLError, `:224` `or {}`, `:243` `["no contract"]`; `contract.py:65-82` `parse_contract` returns None on YAMLError; `contract.py:174` `reason = ... "contract-missing"`. research/07 E1-F8 (L48), G-9 (L102) and Stale bullet (L119); research/06 L132, L236, L243, Gaps item 14 (L359) and Stale row (L372); research/24 VL-24-047 (L60) and VL-24-049 (L62); research/23 VL-23-510, -513 and -733 (L523, L526, L630 and L746) now say "present but unparseable YAML", keep the serializer recommendation and add the quote-or-escape requirement. 06 L132 arithmetic (4 absent + 1 empty cards + 3 unparseable = 8 of 13) agrees with 06 L236. |
| P3-010 | FIXED | Re-read `src/superclaude/commands/spec-panel.md:262`: "the rules in this section apply on top of it and stand alone when that file is unread". research/13 L163 (Key Takeaways, tests) and L203 (row R9), research/24 VL-24-244 (L257), VL-24-469 (L482), VL-24-495 (L508) and research/19 VL-19-415 (L426) now say the link is soft and no same-change spec-panel migration is required; the false "breaks the loop" and "migrate in the same change" claims are gone from 13, 19 and 24 (the remaining hits are research/scope/ inputs and research/12, the stronger side). |
| P3-013 | FIXED | Re-ran `git ls-tree -d --name-only 6c0984326cbb8fb06c4a36065de58b171d3f8175:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/combos \| wc -l` = 96 (97 without `-d`) and re-read `findings.py:20` (`"missing-requirement",`). research/19 VL-19-204 (L215), VL-19-209 (L220), VL-19-734 (L745), VL-19-740 (L751), VL-19-579 (L590); research/20 VL-20-104 (L115), VL-20-109 (L120), VL-20-472 (L483), VL-20-377 (L388), VL-20-542 (L553), VL-20-438 (L449, RESOLVED), VL-20-625 (L636, RESOLVED), Summary (L913); research/21 VL-21-643 (L656) now carry the corrected figures or a [CODE-CONTRADICTED] or RESOLVED tag; no destination column changed. The corrected counts (14 terra + 2 luna, 3 flips, alias GT1 once and GT3 in 2 runs) are carried from VL-20-718, VL-20-771, VL-20-739, VL-19-090, VL-19-091 and research/08, not re-derived from E2 raw data (the fix log says so too). New row defect in VL-20-625: see section 2. |

STILL-OPEN count: 0 of 11.

## 2. New blocking issue | file | evidence

Method: (a) `find research -maxdepth 1 -name '*.md' -newer qa/qa-consolidated-findings-phase3.md` lists exactly the 13 files plus research-notes.md that the fix log names (01, 06, 07, 09, 10, 13, 14, 16, 19, 20, 21, 23, 24, research-notes); files 02-05, 08, 11, 12, 15, 17, 18, 22 were not touched. (b) A script (`uv run python`, removed afterwards) counted unescaped `|` per row: every `| VL-` row in ledgers 19-24 should have 7 (six columns) and every row of the other edited tables should match its table header. (c) Grep for `Status:`, `## Summary`, `## Gaps and Questions` in files 01-24. (d) Grep of files 01-24 and research-notes for the forbidden run-1 paths.

| New blocking issue | file | evidence |
|--------------------|------|----------|
| NEW-1 (IMPORTANT). The fix put an unescaped pipe inside a ledger table cell, so row VL-24-211 has 8 pipes (seven columns) instead of 7. A Markdown parser and any column-position read (statement, type, destination, reason) now puts `defect` into the destination slot and shifts every later cell. Ledger 24 is one of the six ledgers synth-08 is built from by destination. | research/24-value-ledger-evidence-consumers.md L224 (VL-24-211) | The cell text contains the command `diff src plugin`, then a bare pipe character, then `grep -c '^[<>]'`, all inside backticks. Script result for file 24: 589 rows, modal pipe count 7, one anomaly: line 224, 8 pipes. All other 588 rows are 7. (The same fix correctly wrote `rf-(qa\|analyst)` with an escaped pipe in VL-24-444, L457, which shows the intended form.) Required fix: write `diff src plugin \| grep -c '^[<>]'` (or "diff piped to grep -c") in the row. |
| NEW-2 (IMPORTANT). Same defect: the fix put an unescaped pipe inside the git command in row VL-20-625, giving 8 pipes instead of 7. The ledger 20 Summary (L900) states "every row has all six columns and exactly one destination", which the fix made false for this row; the Destination reads `question` instead of `EVAL`. | research/20-value-ledger-e2-study.md L636 (VL-20-625) | The cell text contains the command `git ls-tree -d --name-only 6c0984...:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/combos`, then a bare pipe character, then `wc -l`, all inside backticks. Script result for file 20: 868 rows, modal pipe count 7, one anomaly: line 636, 8 pipes. Required fix: write `\| wc -l`. |

Checked and found clean (no new blocking issue):
- Lost Status, Summary or Gaps section: none. Files 01-24 each have `**Status:** Complete` at line 4 (24 of 24); every edited file still has `## Summary` and `## Gaps and Questions` (01: L276, L253; 06: L384, L343; 07: L122, L92; 09: L221, L200; 10: L241, L210; 13: L277, L247; 14: L274, L228; 16: L299, L262; 19: L927, L960; 20: L898, L917; 21: L1723, L1773; 23: L830, L869; 24: L617, L650).
- References to the forbidden run-1 paths: none in files 01-24 introduced by the fix. The only hits are negative independence statements (research/17:534, research-notes.md:100 and :151, which say the paths were NOT read), and research/17 and research-notes.md were not altered by any fix beyond research-notes L72 and L89, which carry no such reference.
- Table structure of the other edited rows: 01 L87 and L150, 06 L243 and L372, 07 L48, 13 L179, L203 and L214 all match their table header (script reported no anomaly on any edited line outside NEW-1 and NEW-2; the anomalies it reported at 01:103, :110, :177, :231, 13:97, :98, 14:121 and 16:97, :172, :174 are on lines no fix touched, so they are not introduced by the fix).
- Mis-citations introduced by the fix: none found. Every new file:line cite was re-opened: `findings_v2.py:3-4, 96-97`, `findings.py:20, 346-349`, `ledger.py:127-138`, `runner.py:474-478, 748-793`, `card_convert.py:81-82`, `contract.py:65-82, 174`, `reflect_shadow_exit.py:74-79, 224, 242-243`, `spec-panel.md:262, 268` and plugin `:266`.
- Regression check (PASS at review 1, FAIL now): none. Files 14 and 23 were PASS at review 1 and were edited; neither has a defect.

## 3. Item Status (research files 01-24)

PASS = no STILL-OPEN finding and no NEW blocking issue names the file.

| Research file | Status | Reason |
|---------------|--------|--------|
| 01-overlap-capability-matrix.md | PASS | P3-003 FIXED |
| 02-finding-contract.md | PASS | not edited, no finding |
| 03-merge-ledger-verdict.md | PASS | not edited, no finding |
| 04-dispatch-identity-tiers.md | PASS | not edited, no finding |
| 05-input-delivery-brief.md | PASS | not edited, no finding |
| 06-reflect-two-engines.md | PASS | P3-009 FIXED |
| 07-e1-evidence-grading.md | PASS | P3-009 FIXED |
| 08-e2-evidence-grading.md | PASS | not edited, no finding |
| 09-collaboration-designs.md | PASS | P3-008 FIXED |
| 10-process-redesign.md | PASS | P3-001 FIXED |
| 11-consumers-tasklist-workflow.md | PASS | not edited, no finding |
| 12-consumers-spec-review.md | PASS | not edited, stronger side of P3-002 and P3-007 |
| 13-future-pr-review-and-rfqa.md | PASS | P3-002, P3-005, P3-010 FIXED |
| 14-e3-variants-and-experiments.md | PASS | P3-007 part FIXED, no new issue |
| 15-telemetry-manifest-run-record.md | PASS | not edited, no finding |
| 16-eval-governance.md | PASS | P3-004 FIXED |
| 17-defect-register.md | PASS | not edited, no finding |
| 18-repo-constraints-and-branching.md | PASS | not edited, no finding |
| 19-value-ledger-handoffs.md | PASS | P3-010, P3-013 FIXED, rows well formed |
| 20-value-ledger-e2-study.md | FAIL | NEW-2 (VL-20-625 broken row); P3-013 itself FIXED |
| 21-value-ledger-brainstorms.md | PASS | P3-013 FIXED, rows well formed |
| 22-value-ledger-collab-designs.md | PASS | not edited, no finding |
| 23-value-ledger-e1-e3-code.md | PASS | P3-009 annotations in place, rows well formed |
| 24-value-ledger-evidence-consumers.md | FAIL | NEW-1 (VL-24-211 broken row); P3-006, P3-007, P3-009, P3-010 FIXED |

PASS 22, FAIL 2 (20, 24).

## 4. Open blocking count and verdict

- STILL-OPEN from table 1a: 0 (all 11 verified FIXED, section 1).
- NEW blocking issues introduced by the fix: 2 (NEW-1, NEW-2, section 2).

F_1 = 2

Monotonicity: F_1 = 2 is strictly below F_0 = 11. Regression: none (no item that was PASS at review 1 now fails; files 14 and 23 stay PASS).

## Overall Verdict: FAIL

All 11 original blocking findings are FIXED, but the fix itself broke two ledger table rows (an unescaped pipe in a cell), so 2 blocking findings are open. Required action for fix cycle 2 (two one-character edits, nothing else): in `research/24-value-ledger-evidence-consumers.md` L224 (VL-24-211) and `research/20-value-ledger-e2-study.md` L636 (VL-20-625), escape the pipe inside the backticked command as `\|` (or reword it without a pipe), then re-run the per-row pipe count: every `| VL-` row in ledgers 19-24 must have exactly 7 unescaped pipes.

## 5. Notes (minor, not rechecked, not blocking)

- N-1. research/21 VL-21-934 (L934) still says "has no missing-task category, no severity definitions" with no tag; the correction lives in VL-21-091, VL-21-825, VL-21-1540 and VL-21-643. Not part of P3-013's row list; DROP-class context.
- N-2. research/20 L350 (the per-model defect profile row) still says "alias GT3 and GT4 never caught by any src row"; VL-20-690 and VL-19-091 correct it. Pre-existing, not in P3-013's row list.
- N-3. P3-005 mechanism: `ledger.merge_round` parses with the v1 `findings.parse_block` (it needs a `findings-v1` fence and the v1 `check_finding` requires `anchor`), so a findings-v2 block never reaches `annotate` through that path; the KeyError arises only when a v2-validated citations-only finding is passed to `annotate` directly (research/01 probe P-a). The conclusion written into research/13 (v2 findings need a locator-agnostic annotate and an adapter before the ledger) is right; the sentence order in 13 L270 compresses the mechanism. Wording only.
- N-4. research/12:179 mentions "the 185-line spawn census" inside a gap statement; it is a description of what was not re-derived, not a live figure.
- N-5. research/06 Gaps item 14 and research/07 G-9 were inserted before items 13 and G-8 (the fix log says so); numbering order is not ascending. Cosmetic.
- N-6. research/16 L56 still says the E2 guidance "is computed on a family whose 5 of 6 runs were never audited". True for the six-audit method and now bracketed by the research/08 s6 correction two sentences earlier; no false statement.
- N-7. Honest limits carried from the fix log and confirmed in the files: the E2 raw-data counts (14 terra + 2 luna, 3 flips, alias GT1/GT3 counts, "five never caught") are copied from earlier corrections in the research files (VL-20-718, VL-20-771, VL-20-739, VL-19-090, VL-19-091, research/08), not re-derived from the E2 raw JSON, which is not in git; the sc-reflect Wave 3B line numbers in research/13 R9 and VL-24-469 stay [UNVERIFIED].

## Self-audit

If this report said "0 new issues" it would be wrong: the per-row pipe count found two. Evidence the checks were real: 5 Bash re-runs (skill spawn census 175 / 44, spec-panel diff 18, `yaml.safe_load` failure at line 103 on three contracts, `git ls-tree` 96, pipe-count scripts), plus re-reads of the code lines named in section 1.

## Summary

- Checks passed: 13 of 15 (11 finding verifications plus 4 new-issue categories; structure of rows fails on 2 rows).
- Checks failed: 1 category (row structure, 2 rows), 0 of the 11 findings.
- Critical issues: 0. Blocking (IMPORTANT) open: 2. Minor notes: 7.
- Issues fixed in-place: 0 (fix_authorization: false).

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (the verdict is FAIL because of the 2 open blocking findings, not because of low confidence; limits are in N-7).
**Tool engagement:** Read: about 50 | Grep: about 32 | Glob: 1 | Bash: 7 (all read-only; two temporary scripts under /tmp, removed in the same call). No web tools used.

## QA Complete

Status: Complete
