# QA Report - Gate 1 Fix Verification, Content (Phase 3, cycle 1)

Task: TASK-RESEARCH-review-panel-run2-20261114-075454, Item 3.19
Phase: report-qualitative (fix-cycle verification), fix_authorization: false
Date: 2026-11-14
Inputs: qa/qa-consolidated-findings-phase3.md (table 1a, 11 blocking findings: P3-001 to P3-010 and P3-013; tables 1b and 1c not in scope), qa/qa-fix-log-phase3-c1.md (not trusted; every fix re-derived from the research files and the code at HEAD 50d4d2b9d), research/ files 01-24 and research-notes.md.
Status: In Progress

## Findings Verification

| Finding ID | FIXED or STILL-OPEN | reason |
|------------|---------------------|--------|
| P3-001 | FIXED | research/10 L27, Gaps item 2 (L215) and Stale Documentation bullet 1 (L234) now quote the full docstring sentence and say it matches the code. Re-read findings_v2.py:1-7 and :96-97 at HEAD: the sentence ends "a line that carries calibrated_confidence is rejected" and check_finding rejects exactly that key (no key iteration in lines 84-187, so class/probe/src/origin pass). The stale-doc item and the "narrow the docstring" question are retracted; the K6 resolution (extra keys accepted) is kept. No new unsupported claim: the file says it did not run a parse and relies on reading the whole function. |
| P3-002 | FIXED | research/13 row P4 (L179) now says "at least six uses" with the pointer to research/12 s3 and :218. research/12 L82 and L218 hold the six-use re-derivation. card_convert.py:81-82 MINOR_WORDS includes "medium", "low", "nit" (read); spec-panel.md:123 has the High/Medium/Low priority label (grep). research-notes L89 and L176 carry the correction and the "definition-dependent" caveat. Remaining "four meanings" hits are research/12:218 (the correct stale-doc entry), 24 VL-24-486 (now tagged) and read-only scope/ inputs. |
| P3-003 | FIXED | research/01 L87 (grid row 7) and L150 (E1 ledger row) no longer say "reflect has no fix loop"; they say the cli/review kernel has no ledger/rounds/reviser and the reflect wrapper `--fix` loop exists but is dormant. Read runner.py:748-793 (`while True`, `if not config.fix: break`, `classify_fix(...) != "auto-fixable"`, `_apply_remediation`, `iteration > max_iters`) and runner.py:474-478 (`--remediate` under config.fix): the cites are exact. The "dormant because engine A emits no remediation pointer" part is carried from research/06 s4.2 (L149, ensemble.py L787-832 read there) and is tagged to it, not asserted fresh. "absent" is kept only for the finding ledger and rounds. |
| P3-004 | FIXED | research/16 Part 2.3 (L56), Part 2 Key Takeaway (L79), Gaps item 6 (L272), Q6 (L284) and Summary (L301) now say j1 is the sonnet + 2x luna challenger family, not evidence for the ember family, and cite research/08 s6 as the stronger side. Checked: E2 three-way.py FAM lists `j1-sonnet-luna2-r1..r5` under "sonnet + 2x luna" (git show at 6c09843); 08 s6 L91-107 has the 45-of-45 identity checks, the six-scenario table (S0 2.33 to S3 2.83 when the two refusals are excluded) and the decision "unaudited does NOT invalidate not confirmed". The two refusals named in 16 (j1-r2, j1-r4, designSpec t4-1) match 08 L92. The "formal audit still open, only completeness remains" wording is proportionate. |
| P3-005 | FIXED | research/13 Stale Documentation bullet 1 (L270), s8 row M1 (L214), Summary (L278) and Key Takeaways now say v2 location is parser-level only and the ledger/merge/annotate path still needs `anchor`. Verified in code: findings.py:346-349 `locate(text, finding["anchor"])` with no `.get`; ledger.py:127-138 merge_round calls fnd.annotate for every parsed finding. I also reproduced it: `uv run python` calling `findings.annotate` on a citations-only finding raises `KeyError 'anchor'`. research/01 P-a (L53) and 17 DR-113 (L276) agree. The earlier "NOT a core blocker" sentence is kept only as the contradicted original. |
| P3-006 | FIXED | research/24 VL-24-444, VL-24-464, the verification note and Summary item 4, and research-notes L72 now use 175 prose spawn lines over 7 skills (44 structured over 8) and mark the slice's 185 as not reproducible. I re-ran both patterns over src/superclaude/skills/*/SKILL.md: U2 = 175 lines (task-builder 45, tech-research 41, roadmap 32, readme 16, task 14, tech-reference 14, operational-guide 13); U1 = 44 lines in 8 files (23, 12, 4, 1 each in five); per-line-and-agent count = 247 (awk). All equal research/13. No other research file 03-24 states 185 as the spawn-line quantity (the 12:179 hit is the slice's own unverified list; 13 L254/271/278 already mark it unreproducible). |
| P3-007 | FIXED | research/24 VL-24-211, -497, -486, -487, -488, -396, -570, the verification note and research/14 Gaps item 10 are corrected. At HEAD: wc -l src 490 / plugin 476; `diff | grep -c '^[<>]'` = 18; hunks are only the usage line (src 23), the --target-release sentence (37), Native reasoning vs Sequential (221), the hard-gate sentence (268 vs 266) and the Unattended-mode section (454-465). The Review Loop section (src L256-264, heading at 256) has no diff line; the hard gate is its own section (heading at 266). Plugin L266 really adds the `${CLAUDE_PLUGIN_ROOT}` fallback, so "softens" is false and the new "extended" wording is right. The Medium/seven-vocabulary/cap counts are now tagged against research/12 (L82, :217-:220) instead of repeated as plain counts. The log honestly says "test-pinned" was not re-verified and the new text says only "identical". |
| P3-008 | FIXED | research/09 s4.2 item (i) (L126) and the s4 Key Takeaways first bullet (L129) now say F1 is the only family that needs neither a hook nor a model-side write, so it is expressible in every runtime HEAD has, but has no clean measured success (both r3 A3 rows `phase2_timeout` 1, L76) and its `--resume` dependency for gateway ids is [UNVERIFIED] (research-notes L262 lists exactly that). "works in every runtime" is gone and the recommendation to leave exchange optional is kept. The swarm half is supported by openai_compat.py:384-388 (read: one user message, no session). See note N-4 for a small wording tension with 09 L107. |
| P3-009 | FIXED | research/07 E1-F8 (L48), G-9 (L102) and a stale-doc bullet (L119); research/06 L132, s6.1 (L236), s6.2 row 1 (L243), gap 14 (L359) and a stale-doc row (L372); research/24 VL-24-047/049; research/23 VL-23-510/513/733 (and 617) now say the contract file exists but is not parseable YAML. Re-derived: `ls -l` shows return-contract.yaml present in shadow04 (5,648 bytes), shadow09 (5,707) and shadow08 (5,637); line 103 of each is `reviewer_models: [claude-gw-tier1b[1m], ...]`; `uv run python yaml.safe_load` on each raises "expected ',' or ']', but got '['". Code: reflect_shadow_exit.py:74-79 `_yaml_map` returns None on YAMLError, :224 `or {}`, :242-243 `["no contract"]` and `ev1_fail ... else True`; contract.py:65-82 parse_contract returns None on YAMLError and :173-174 sets reason "contract-missing". The arithmetic is now consistent: 06 L132 = 5 layout/naming (4 merged-verdict absent + 1 empty reviewer-cards) + 3 unparseable = 8. The serializer recommendation is kept and sharpened (quote or escape aliases with `[`/`]`). Residual wording note N-3. |
| P3-010 | FIXED | research/13 Key Takeaways (tests) (L163) and R9 (L203), research/24 VL-24-244, -469, -495, research/19 VL-19-415 no longer claim spec-panel must migrate with rf-qa. spec-panel.md:262 (read in full) ends "the rules in this section apply on top of it and stand alone when that file is unread", and research/12 L18 and L221 mark B10/I10/G2.9 [CODE-CONTRADICTED] as a hard dependency. Destinations (CORE, MODULE-rfqa, DROP, MODULE-rfqa) are unchanged. The sc-reflect Wave-3B coupling is kept as [UNVERIFIED line numbers]; I read sc-reflect-protocol SKILL.md:632-633 and it does list rf-qa and rf-qa-qualitative as Wave 3B reviewers, so that coupling claim is true (the tag is merely conservative). |
| P3-013 | FIXED | research/19 VL-19-204 (CORE), VL-19-209, VL-19-734, VL-19-740 (and extra VL-19-579); research/20 VL-20-104, -109, -472, -377, -542, -438, -625 and the Summary "Still open" paragraph; research/21 VL-21-643 now carry the corrected figure or a [CODE-CONTRADICTED] tag with a pointer. Checked against the stronger sources: 08 L82 (3 flips; total-loss merges did not flip) and VL-20-739 support the new VL-20-104 clause; 08 L84 / VL-20-718 support "14 terra + 2 luna"; VL-19-091 supports "alias GT1 once, GT3 in 2 runs"; `git ls-tree -d --name-only 6c09843:.../combos | wc -l` = 96 (97 without -d); findings.py:20 has "missing-requirement". grep for "16 empty terra" across research 03-24 now returns only tagged rows or the corrections themselves. Destination columns unchanged. Residual rows are notes N-1 and N-2 (same defect class but DROP duplicates or a trivial miscount; none changes a conclusion). |

## New Blocking Issues

| New blocking issue | file | reason |
|--------------------|------|--------|
| None | n/a | Checked for each fix: no file became shallower (every edit replaced a claim with a longer, better-evidenced one and kept the original recommendation); no fix contradicts another research file (each correction points at the stronger file: 12, 13, 08, 01/17, 06); no [CODE-CONTRADICTED] or [UNVERIFIED] claim is used as fact (the carried parts are tagged: --resume for gateway ids, "five never caught", E2 raw counts, line numbers l.632-633). |

## Item Status (research files 01-24)

| Research file | Status | basis |
|---------------|--------|-------|
| 01-overlap-capability-matrix.md | PASS | P3-003 FIXED; no new blocking |
| 02-finding-contract.md | PASS | no open or new blocking finding |
| 03-merge-ledger-verdict.md | PASS | no open or new blocking finding |
| 04-dispatch-identity-tiers.md | PASS | no open or new blocking finding |
| 05-input-delivery-brief.md | PASS | no open or new blocking finding |
| 06-reflect-two-engines.md | PASS | P3-009 FIXED; note N-3 minor |
| 07-e1-evidence-grading.md | PASS | P3-009 FIXED |
| 08-e2-evidence-grading.md | PASS | not edited; used as stronger side, content re-read and consistent |
| 09-collaboration-designs.md | PASS | P3-008 FIXED; note N-4 minor |
| 10-process-redesign.md | PASS | P3-001 FIXED |
| 11-consumers-tasklist-workflow.md | PASS | no open or new blocking finding |
| 12-consumers-spec-review.md | PASS | not edited; stronger side for P3-007 and P3-010, verified against code |
| 13-future-pr-review-and-rfqa.md | PASS | P3-002, P3-005, P3-010 FIXED |
| 14-e3-variants-and-experiments.md | PASS | Gaps item 10 corrected (P3-007) |
| 15-telemetry-manifest-run-record.md | PASS | no open or new blocking finding |
| 16-eval-governance.md | PASS | P3-004 FIXED |
| 17-defect-register.md | PASS | no open or new blocking finding (1b/1c items out of scope) |
| 18-repo-constraints-and-branching.md | PASS | no open or new blocking finding |
| 19-value-ledger-handoffs.md | PASS | P3-010 and P3-013 FIXED; note N-2 minor |
| 20-value-ledger-e2-study.md | PASS | P3-013 FIXED; note N-1 minor |
| 21-value-ledger-brainstorms.md | PASS | P3-013 FIXED |
| 22-value-ledger-collab-designs.md | PASS | no open or new blocking finding |
| 23-value-ledger-e1-e3-code.md | PASS | P3-009 annotations verified (VL-23-510, -513, -733 carry the note) |
| 24-value-ledger-evidence-consumers.md | PASS | P3-006, P3-007, P3-009, P3-010 FIXED |

## Notes (minor, not blocking, not to be rechecked)

- N-1: research/20 VL-20-005 ("combos/ holds 95 combo row directories") and VL-20-561 ("x 95 rows") still state 95 although VL-20-625 now says 96 is right. The log discloses VL-20-561 only. A small count in an artifact inventory row; the conclusion is unaffected. Fix in item 5.08 or the synthesis by quoting 96.
- N-2: research/19 DROP duplicate rows VL-19-483, -491, -736, -789 and research/21 VL-21-726 still repeat "4 verdict flips" untagged (VL-21-726 carries "[INCONSISTENT in source]"). They point at corrected primary rows and are DROP, so they do not reach the synthesis. The synthesis must not quote four flips.
- N-3: research/06 L292 (engine comparison table) still reads "orchestrator layout/copy drift: 8/13 EV-1"; after the fix 3 of the 8 are an unparseable contract. Wording only; L132, L236, L243 and gap 14 carry the correct split.
- N-4: research/09 L107 reports r2 spike S2 (`--resume`) PASS for four models as measured, while the new L126/L129 text calls the `--resume` dependency for gateway ids [UNVERIFIED] (taken from research-notes L262). The more cautious tag wins and the F1 conclusion is proportionate; the synthesis should say which models S2 covered.
- N-5: the new gap items are numbered out of order (06 gap 14 before 13, 07 G-9 before G-8), and 06 L359/L372 are long single lines. Cosmetic.
- N-6: honest limits recorded by the fixer and confirmed as carried, not re-derived: E2 raw-data figures (14 terra + 2 luna, 3 flips, "five never caught"), `--resume` for gateway ids. The sc-reflect Wave-3B line numbers I did check (632-633 are right).

## Self-Audit

**(a) Reliance list**
- Relied on the consolidated findings table 1a for the exact defect, location and proposed fix of each of the 11 findings. I did not take their evidence as true; each claim was re-derived below.
- Relied on the fix log only to find where the edits were made.

**(b) Independent semantic checks (each with its own tool evidence)**
- P3-001: Read findings_v2.py:1-187 (docstring and the whole check_finding) and research/10 L23-29, L210-239.
- P3-002: Read card_convert.py:76-88; Grep spec-panel.md:123; Grep "four meanings|at least six" over research.
- P3-003: Read runner.py:470-482 and :745-796; Grep remediation_* over src; Read 01 L26/L87/L150 and 06 L149.
- P3-004: Read 16 L54-82, L284, L299-302; Read 08 L89-107; `git show 6c09843:.../three-way.py` (FAM lists).
- P3-005: Read findings.py:338-355 and ledger.py:120-144; ran `uv run python` annotate on a citations-only finding (KeyError 'anchor'); Read 13 L160-165, L196-217, L266-280.
- P3-006: Bash grep census of src/superclaude/skills/*/SKILL.md (175, 44, 247 reproduced); Bash context extraction of every "185" hit in research 24, 13, 12 and research-notes.
- P3-007: Bash wc/diff of src and plugin spec-panel.md (490/476, 18, five hunks); Bash heading listing (Review Loop at 256, hard gate at 266); read of the corrected 24 rows and 14 gap 10.
- P3-008: Read 09 L72-132; Read openai_compat.py:380-391; Grep research-notes for "resume".
- P3-009: Bash `ls -l`, `sed -n 103p` and `uv run python yaml.safe_load` on the three contracts; Read scripts/reflect_shadow_exit.py:60-82 and :224-245 (Bash sed); Read contract.py:62-83 and :168-177; Grep all "no contract" mentions in research 01-24.
- P3-010: Bash print of spec-panel.md:262; Grep sc-reflect SKILL.md:632-633; Grep 12 for B10/I10/G2.9; Bash read of 24 rows 244/482/508 and 19 row 426.
- P3-013: Grep/Bash over research 02-24 for "16 empty terra", "four flips", "alias GT3", "95 rows", "no missing-task"; `git ls-tree` directory count (96/97); Read of findings.py:20; Read 08 L82/L84, VL-20-739.
- Cases where "FIXED per log" was not enough and my own work changed the picture: N-1 (VL-20-005 never mentioned in the log), N-2 (duplicate rows still carrying the old figure), N-3 (06:292 table cell).

Counts: about 45 factual claims independently re-derived (code line cites, counts, byte sizes, YAML parse results, diff hunks, git tree counts, row text). Files read: findings_v2.py, findings.py, ledger.py, card_convert.py, runner.py, contract.py, openai_compat.py, spec-panel.md (src and plugin), sc-reflect-protocol SKILL.md, scripts/reflect_shadow_exit.py, the three shadow return-contract.yaml files, research 01, 06, 07, 08, 09, 10, 12, 13, 14, 16, 19, 20, 21, 23, 24, research-notes, and the E2 three-way.py at git tip 6c09843.

Why 0 open findings is believable: eleven of eleven corrections were checked against code or the stronger research file, and several were reproduced (KeyError, YAML failure, grep census, diff count, git tree count). The review also found six residual notes the fix log did not report, so it is not a rubber stamp.

Web research: none performed (all claims are local). Tavily and the fallback tools were not used.

## Confidence Gate

Checklist items: 11 findings + 1 new-issue sweep (contradiction, shallowness, tagged claim used as fact) + 1 Item Status sweep over files 01-24 = 13.
- Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Carried claims not re-run, and not needed for FIXED: E2 raw-data counts (14 terra + 2 luna, 3 flips), "five never caught", and the engine-A "no remediation pointer" reasoning beyond research/06's own read. They are tagged as carried in the research files.
- Tool engagement: Read: about 26 | Grep: about 24 | Glob: 1 | Bash: 14 (plus one `uv run python` reproduction). Read+Grep+Glob (about 51) exceeds the 13 checklist items.

## Summary

- Blocking findings re-checked: 11. FIXED: 11. STILL-OPEN: 0.
- New blocking issues: 0.
- Minor notes: 6 (N-1 to N-6), not blocking.
- F_1 = 0
- Verdict: PASS

Status: Complete
