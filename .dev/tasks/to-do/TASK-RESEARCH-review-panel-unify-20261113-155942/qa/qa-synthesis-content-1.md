# QA Report - Synthesis Gate, content-quality lens (Partition 1 of 2)

**Topic:** Unified Review Panel (E1 reflect Tier 2 panel, E2 tasklist review-panel study at 4a22d74, E3 #346 review loop)
**Date:** 2026-11-14
**Phase:** synthesis-gate (content-quality lens, items 7-12)
**Fix cycle:** 0 (first review)
**Assigned files:** synth-01-problem-current-state.md, synth-02-target-gaps.md, synth-03-external-findings.md, synth-04-options-conflicts.md
**Fix authorization:** false (report only)

[PARTITION NOTE: Cross-file checks limited to assigned subset plus read-only consultation of synth-05..07 for consistency.]

---

## Overall Verdict: FAIL

Two blocking findings (B-1, B-2). Every other finding is MINOR and recorded as a note. The four debates (C03, C05, C13, C14) were read and each is stated as `partial` with its unaddressed HIGH invariants and unresolved diff points listed in both the conflict index and the body; per the executor note these are legitimate open items and are not findings.

## Items Reviewed (content-quality lens, items 7-12)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 7 | Cross-section consistency | FAIL | B-1 (Tier 2 / parsed-sparse claim) and B-2 (shadow calibration count). Counts that agree across synth-01/02/04: 49 lost blocking findings (24+14+10+1), 3 flips, 195/1398/83 chaining, 65 vs 38, Stage 2 exit 13 of 20 and 8/13 = 0.615 vs 3/39 = 0.077, 0/689 legacy and 142/142 shadow (in 01, 02, 04 only), 651/131/520 and 1182 tests, 43 call sites in 11 skill files, 23 of 45 briefs. synth-02 internal counts re-derived by script: 144 rows, Critical 15 / Important 65 / Minor 64, Track M1 56 / M2 20 / M3 18 / M4 16 / none 34, 11 rows with the C8 note, section 4.3 M1 Important list = 33 rows. All 80 Critical+Important gap ids appear in synth-04..07 (script check, 0 unreferenced). |
| 8 | No doc-only claims in Sections 2 or 6 | PASS (note N-6) | Doc-sourced material in synth-01 (S04 reports, E2 COMBO-REPORT, FINAL-REPORT) and synth-04 (MR, CR, PR) is labelled `doc-sourced` or `[DOC-SOURCED]`; the 3 unverified experiment variants are tagged `[UNVERIFIED beyond the description]`. Architecture descriptions (2.1, 2.3 master components, 2.4, 2.5, 6.D) trace to code lines; 16 sampled line citations match the code (findings_v2.py:107-108,161-162; ledger.py:150-157,254-258; panel.py:485-486,536-543; telemetry.py:23,112-115; runner.py:538-545; ensemble.py:773,789; contract.py:295-296,380-381; review/__init__.py:24-25; cluster.py:407-408; card_convert.py:199-201). |
| 9 | Stale docs surfaced in Section 4 | PASS | gaps-and-questions.md rows D-01 to D-77 all exist; synth-02 has DOC-01 to DOC-70 plus one combined row for D-71 to D-77 (144 rows total, matches the 4.2 self-check). Row text for D-11, D-20, D-27, D-44, D-59, D-63, D-66, D-70 matches the log. Sampled research Stale Documentation sections (R06 lines 272-278, R11 lines 469-480) all map to DOC rows (DOC-32, 33, 36, 37, 38, 59, 60, 61, 11, 25, 44). DOC-59 content is wrong, see B-1. |
| 10 | Content rules | PASS (notes N-1 to N-5) | Tables carry multi-item data; ASCII diagrams present for data flow (synth-01 three, synth-02 one, synth-04 one); no full source reproductions; inline `file:line` evidence throughout; uncertainty tags used. Notes only. |
| 11 | Completeness, no placeholders | PASS | Grep for TODO, TBD, PLACEHOLDER, FIXME, XXX, lorem in synth-01..04: only "placeholder" hits, all about brief placeholders (`{{SOURCE}}` etc.); grep for empty table cells found none (only a regex-in-code `v2\|role\|path\|\|refs` and an ASCII diagram). Sections 1, 2.1-2.6, 3, 3.1, 4, 4.1-4.3, 5.1-5.5, 6.0, C-01 to C-20, 6.D, 6.X and Options Comparison all have content. |
| 12 | No hallucinated file paths | PASS | Batch check of 120+ repo, `~/.claude` and `.dev` paths: 0 missing (see path list). 17 of 17 sampled E2 paths resolve with `git cat-file -e 4a22d74213f93837d00c2c314075dd967b9a98e3:<path>`; E2 line cites `run-reviewer.sh:13-17, :48, :57, :58, :76, :87` and `COMBO-REPORT.md:292, :373, :501` match the content at that commit. File line counts quoted in synth-01 (304, 517, 487, 197, 184, 534, 240, 707, 129, 457, 494, 118, 137, 447, 98, 420, 366, 410, 2033, 116, 490, 74, 2668, 2050, 475, 481, 193) match `wc -l` exactly. All 8 cited commit hashes resolve. |

## Issues Found

| # | Severity | Synth file | Section | Finding | Required fix |
|---|---|---|---|---|---|
| B-1 | IMPORTANT (blocking) | synth-01, synth-02, synth-04 | synth-01 sec 2.1 measurements table row "Tier 2 is the typical path" (line 73); synth-02 DOC-59 (line 245); synth-04 C-14 lines 691, 897, 917, 926, 941, 944 | The superseded claim "Tier 2 was driven by the parsed-sparse flag" is presented as measured fact. Line 926: "Acts on the measured driver of Tier 2 spend (35 of 39 parsed-sparse)". Line 941: "Pays Tier 2 on 38 of 39 plans for an input-format reason, not plan risk". Line 944: "Tier 2 cost is almost always paid and mostly for an input-format reason ... 35 by the parsed-sparse pre-filter ... same conclusion [CODE-VERIFIED in data]". Line 917: "pre-filter from forcing Tier 2". Line 691: "Parsed-sparse escalation sends nearly every workflow plan to Tier 2". synth-01:73 says "38 of 39 ... selected tier 2; 35 of them through the parsed-sparse pre-filter" and DOC-59 says "38 of 39, 35 (same conclusion)". The C-14 debate in the same file (line 956) and `reviews/adversarial/panel-size-cost/adversarial/base-selection.md:150-153` state the opposite: flag set in 35 of 39 non-shadow files (34 of the 38 Tier 2 runs), decisive in 0 for certain and at most 1, "the flag is not the cost driver", with a warning to recount every document that repeats "34 of 38". So C-14 contradicts itself, and synth-01 also gets the numerator wrong (the recount says 34 of the 38 Tier 2 runs; 35 is of all 39 files). synth-05:284 and synth-06 (V-316, V-366, V-399, V-518, V-673) already carry the correction. R11 line 412 itself reports only "parsed-sparse in 35" of 39 files, not a causal share. | Rewrite every listed sentence to the corrected form: "38 of 39 non-shadow pre runs selected Tier 2; the parsed-sparse flag was set in 35 of 39 files (34 of the 38 Tier 2 runs) and was decisive in 0 for certain, at most 1; the cost driver is not established". synth-04 line 926 pros: drop "measured driver"; say the flag is set in most runs but its causal share is unmeasured and at most 1. Line 941 cons: delete "for an input-format reason, not plan risk". Line 944: state the corrected figures and cite the C14 debate recount. Line 917: "making a flag that is set in 35 of 39 files advisory". Line 691: replace "sends nearly every workflow plan to Tier 2" with the measured 38 of 39. synth-02 DOC-59: finding = "recount: 38 of 39 selected Tier 2; flag set in 35 of 39 (34 of 38); the older 'driven by the flag' conclusion is NOT preserved (debate recount: decisive in at most 1)". synth-01:73: same rewrite, and Strength cell "measured census of selection; cause not established". |
| B-2 | IMPORTANT (blocking) | synth-03 | 5.3 intro (line 168), 5.3.3 Xiong row (line 205), 5.3.4 Platt row (line 215) | False codebase statements that contradict synth-01 (lines 69-70), synth-02 MS-16 and synth-04 C-06/C-05. Line 168: "shadow runs recorded 0 numeric per-finding calibrations of 689 findings". Line 205: "zero numeric calibrations in shadow runs is a small loss of evidence". Line 215: "With 689 findings and the E2 ground-truth packages, Platt is feasible". R05 section 5 (`research/05-blocking-calibration.md:155-159, 193`) says legacy runs hold 0 of 689 numeric per-finding values and shadow runs hold 142 of 142. The 689 findings carry no numbers and no ground truth, so they cannot be the Platt calibration set; the 142 shadow numbers have no ground truth. The error is inherited from `research/web-03-judge-calibration.md:11`, but synth-03 line 6 says code facts are quoted as recorded, so it is stated as fact. | Line 168: "legacy runs recorded 0 numeric per-finding calibrations of 689 findings; shadow runs recorded 142 of 142 (no ground truth)". Line 205: "zero numeric calibrations in the legacy census (shadow runs added 142 numbers) is a small loss of evidence". Line 215: restate feasibility against the real data: 142 shadow numbers with no ground truth, plus E2 labelled packages that carry no calibrator numbers, so a fit is not currently possible; keep the staleness argument. |
| N-1 | MINOR | synth-04 | C-05 evidence (line 375) | "`cluster_agreement` 1.0 in 10 of 11" is quoted from R07 without the correction logged as GQ C-05 and carried at synth-01 line 72 and synth-02 DOC-19 (11 of 14 runs are 1.0 only because they have no blocking cluster; shadow09 = 0.9328). The populations (10 of 11 vs 11 of 14) are not reconciled. | Add the GQ C-05 caveat and state the population, or cite the same 11 of 14 figure. |
| N-2 | MINOR | synth-04 | 6.X Assessment summary (line 1439) | The status list "C01, C02, C04, C07-C12, C15, C16, C18-C20 decided; C03, C05, C13, C14 open" omits C06 and C17, both DECIDED-BY-EVIDENCE in the index (18 of 20 conflicts listed). | Add C06 and C17 to the decided list. |
| N-3 | MINOR | synth-01 vs synth-02 | synth-01 line 290 vs synth-02 DOC-43 and 4.1 row 6 | synth-01 states `tests/cli/reflect` "has 37 files" flatly; synth-02 records the 37 vs 38 file count as unresolved (353 tests agree). | State "37 or 38 files (unresolved), 353 tests" in synth-01. |
| N-4 | MINOR | synth-01 vs synth-02 | synth-01 line 33 vs synth-02 4.1 row 15 | synth-01 says "94 open rows, none Critical, 30 Important" without saying this is the gaps log's scale; synth-02 rates 15 rows Critical on a different scale (explained only at 4.1 row 15). | Add "on the gaps log's own scale (Section 4 rates 15 rows Critical, see 4.1 row 15)" to synth-01. |
| N-5 | MINOR | synth-01 to synth-04 | id and citation namespaces | `C5`, `C11`, `C12` mean reflect-contract constraints in synth-04 C-17 (lines 1117, 1124) and synth-02 K-2, but `C05`, `C11`, `C12` are conflict ids in the same file (C11 merge path, C12 clustering); synth-03 uses `C1`-`C5` for a third set. synth-02 uses `CR:`, `HO:`, `AD/`, `MR:` without a key (defined only in synth-04 line 5 and synth-01 line 17). DOC-16 title reads as if the hand-off line `:23` is stale although the finding says it was right. SARIF `level` is "three buckets" in synth-02 3.1 and "four values" (with `none`) in synth-03 5.2.1. | Cite the constraints as `K-2` etc. in synth-04; add a citation key to synth-02; reword DOC-16; say "three non-`none` values" in synth-02. |
| N-6 | MINOR | synth-01 | 2.3 "Experiment outcomes and the caveat" (line 182) | Outcome numbers (13, 9, 3 new labels; 22.16% growth; 10.31%, 22.03%, 57.72%, 69.34%) come from FINAL-REPORT.md and are not tagged `[DOC-SOURCED]`, although the section preamble promises doc-only statements are marked. They are outcomes, not architecture, so item 8 still passes. | Add `[DOC-SOURCED]` to that paragraph. |

## Open items stated as open (not findings)

| Debate | Index row | Body status text | Open items named |
|---|---|---|---|
| C03 model-tier-config | line 17 | line 226 | INV-013, INV-009 HIGH unaddressed; diff points S-007, C-001, C-006, X-003; O-2 open |
| C05 who-judges-blocking | line 19 | lines 378-382 | 11 HIGH invariants listed by id (count matches); diff points C-005, C-012, X-002; grader accuracy unmeasured |
| C13 ledger-model | line 27 | lines 887-891 | 10 HIGH invariants (INV-001..010); diff points S-006, C-013, A-002, A-004; gate choice open |
| C14 panel-size-cost | line 28 | lines 952-956 | 3 HIGH invariants (INV-009, 012, 013) plus 7 MEDIUM; diff points S-002, S-006, C-003, C-010, C-013, C-016; Decision D-1 owner-gated. Its recount text is correct; the body around it is not (B-1). |

Explicit flags allowed by the executor: synth-05 raises one `[CONTRADICTION]` (PENDING / exit 12; synth-05 lines 158 and 290). Partition-1 text agrees with the code: `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py:63` is `{"PASS": 0, "CONTINUE": 10, "ESCALATE": 11, "PENDING": 12}`, and synth-04 C-19 and synth-02 BL-13 describe that vocabulary correctly. No silent inconsistency found in this subset. E2 is cited only at `4a22d74213f93837d00c2c314075dd967b9a98e3` (short form `4a22d742` in synth-01 is the same commit).

## Paths checked

- `src/superclaude/cli/review/`: findings_v2, card_convert, cluster, cluster_cmd, verify_cmd, manifest, manifest_cmd, panel, panel_cmd, findings, ledger, merge_cmd, ledger_cmd, telemetry, telemetry_cmd, `__init__` (.py); `data/review-panel.default.json`, `review-panel.live7.json`, `review-tiers.default.json`, `review-panel.reflect-lite.json`.
- `src/superclaude/cli/reflect/`: panel_lint, contract, ensemble, runner, commands, config, models (.py).
- `scripts/`: reflect_cluster_pairs, reflect_consumer_inventory, reflect_stage0a_replay, reflect_verdict_replay, reflect_shadow_exit (.py).
- `src/superclaude/skills/`: sc-reflect-protocol (SKILL.md, refs/reviewer-spec.md, refs/reflection-rubric.md, refs/deviation-taxonomy.md), sc-workflow-protocol, sc-tasklist-protocol, sc-brainstorm-protocol, sc-pr-submit-protocol (SKILL.md, refs/severity-routing.md, refs/finding-verify.md).
- `src/superclaude/agents/`: reflect-reviewer, confidence-calibrator, evidence-validator, rf-qa, rf-qa-qualitative, rf-analyst; `commands/spec-panel.md`, `commands/design.md`; `rules/prompts/document_review_loop_prompts.md`; `src/superclaude/pr_submit/` reviewers, fsm, severity_router, models, classifier (.py).
- 24 test files located by basename in the tracked tree (test_review_ledger, test_review_findings, test_review_findings_v2, test_review_cluster, test_review_panel_exclusion, test_review_cli, test_review_telemetry, test_review_rules_text, test_review_loop_extension, test_spec_panel_review_loop, test_review_brief_placement, test_review_severity_mapping, test_review_card_convert, test_reflect_cluster_pairs, test_review_panel_reflect_profile, test_review_panel_live7, test_review_panel, test_review_prompt_overrides, test_review_severity_rule, test_shadow_skill_contract, test_shadow_exit_script, test_ensemble_stub_integration, test_reviewer_readonly_tools, test_panel_contract_lint) plus phase-template.md, severity-rubric.md, auggie-prompts.md, return-contract.md, ccsession-models.json.
- `~/.claude/`: skills/sc-review-ledger/scripts/review_ledger.py, skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py and refs/rubric.md, agents/finding-grader.md, commands/sc/spec-panel-{ledger,stoprule,diffgate,ponytail,armb}.md, skills/sc-diffgate/SKILL.md, skills/sc-fix-audit/SKILL.md.
- `.dev/experiments/346-validation/phase5/final-bundle/` SNAPSHOT-STATE.txt and reports/phase5/FINAL-REPORT.md; `.dev/eval-workspaces/shadow-model-combos/` PLAN.md, FINDINGS.md, results.md, combos.json, analysis/extract.py.
- Task dir: `reviews/adversarial/{model-tier-config,who-judges-blocking,ledger-model,panel-size-cost}/proposal-merged.md` and `adversarial/return-contract.yaml` (8 files), gaps-and-questions.md, BUILD-REQUEST.md, research/scope/04-this-session-artifacts.md.
- E2 at `4a22d74213f93837d00c2c314075dd967b9a98e3` under `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` (17 of 17 resolve): tools/run-reviewer.sh, tools/tmp-scripts/{judge-one.sh, anon-combos.sh, README.md}, analysis/final-table.py, analysis/three-way.py, analysis/audits/audit-A/{audit.py, summary.md}, analysis/audits/audit-D/{audit.py, audit2.py, summary.md, anch.py, flags.tsv}, COMBO-REPORT.md, PILOT-REPORT.md, combos/SPEC.md, manifest.md.
- Commits resolved with `git cat-file -t`: 4a22d742, 9163bd1c7, 5d9a0ae70, 77e0a7029, d2d8a2d16, 9874d63fb, c2e3347d3, 792cf8c52.

## Summary

- Checks passed: 5 / 6 (items 8, 9, 10, 11, 12); failed: 1 (item 7)
- Blocking issues: 2 (B-1 IMPORTANT, B-2 IMPORTANT); CRITICAL: 0; minor notes: 6 (N-1 to N-6)
- Issues fixed in place: 0 (fix_authorization false)
- Items 1-6 of the 12-item checklist belong to the other lens and were not graded here.
- [PARTITION NOTE: Cross-file checks limited to assigned subset (synth-01 to synth-04) plus read-only consultation of synth-05 to synth-07 for consistency (synth-05 lines 158, 284, 290; synth-06 V-316, V-366, V-399, V-518, V-673; downstream references of all 80 Critical and Important gap ids). Full cross-file verification requires merging all partition reports.]

## Recommendations

1. Fix B-1 in synth-01, synth-02 and synth-04 using the corrected wording that synth-05 line 284 and synth-06 already use, then grep the four files for `parsed-sparse`, `input-format`, `driver of Tier` and `same conclusion` to confirm none presents the old claim.
2. Fix B-2 in synth-03 (three sentences).
3. Notes N-1 to N-6 need no re-review.

## Confidence

- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (the six items of this lens; items 1-6 are the other lens)
- **Tool engagement:** Read: 32 | Grep: 26 | Glob: 0 | Bash: 12 (counts approximate; Bash calls were batched, e.g. one script covering 120+ path checks and one covering 17 E2 paths). Read + Grep + Glob (58) exceeds the 6 checklist items of this lens.
- Web research: none needed (external URLs in synth-02 and synth-03 are quoted as external context and were not re-fetched; that is the other lens). tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.
- UNCHECKED: none for this lens. UNVERIFIABLE: none.

## QA Complete
