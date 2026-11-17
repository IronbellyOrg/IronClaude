# Merge log: stage 4 plan, third review

## Metadata

- Base: V1 (`variant-1-original.md`, analyzer, sonnet class), chosen by tiebreaker level 1 (base-selection.md).
- Executor: merge-executor agent (claude-gw-tier1a), run from the main session's dispatch.
- Plan: `refactor-plan.md`, 12 planned changes.
- Changes applied: 12 of 12; changes skipped: 0; rejected alternatives honoured: 4 of 4 (C-001 blocking grade, V2 blocking grades on C-006, C-007 and C-009, C-011 as a plan finding, V3 verdict NEEDS-REVISION).
- Output: `adversarial/merged-review-card.md`. The plan's Overview also names `adversarial/merged-verdict.yaml`; it was not written, because the dispatch allowed only the card and this log.
- Status: complete; post-merge validation passed (below).
- Timestamp: 2026-11-16 (session date; the environment's context date reads 2026-11-17).
- Result: PASS, 0 blocking, 7 MEDIUM (K1 to K7), 4 minor (K8 to K11).

## Applied changes

1. **Change 1 (Verdict).** Applied. Before: "PASS. No finding blocks execution ... six defects below are minor". After: "PASS: 0 blocking, 7 Medium, 4 minor" with the dissent history (V3 cap-count blocking and V2's blocking grades withdrawn in Round 2, 18 of 18 points converged, not a fix-first gate). Provenance: Base V1 (modified) - change 1; debate S-001.
2. **Change 2 (cap count).** Applied as K1. Before: V1-F1 MINOR, "proves nothing", "natural" reading. After: MEDIUM, both readings open (fold gives 1, keep gives 2), stage 3 precedent, fix: state fold or keep and set the count, or rely on the `v2 begin` count. Provenance: V1-F1, V3-F1, V2 Checked; C-001, X-001.
3. **Change 3 (close-enough wording).** Applied as K2. Before: V1-F2 MINOR. After: MEDIUM (probe INV-003 grade adopted), V3's fix (reword the Constraints clause without the banned words). Provenance: V1-F2, V3-F2, INV-003; C-002.
4. **Change 4 (digest-satisfied greps).** Applied as new K3, MEDIUM. Before: not in V1. After: the digest supplies "stays open for verification" (SPEC:199) and `consumer-unknown` (SPEC:201); principle 8 of three prompts holds no banned phrase; fix greps the "8. **NO LENIENCY**" line. Provenance: V3-F3, V2-F3; C-003, X-003.
5. **Change 5 (Rule 6 heading).** Applied as new K4, MEDIUM. Before: not in V1 (V1 marked H7 fixed). After: S3:183 checks only "that's never minor", `rf-qa-qualitative.md:990` heading may stay, P4:49 then halts; fix makes the absence check conditional or adds a stage 3 heading check. Provenance: V3-F4; C-004.
6. **Change 6 (stale switch premise).** Applied as K8, minor. Before: V1-F3 without the patch point. After: adds that case (b) needs a `strict` parameter or a monkeypatch of `STRICT_T2`. Provenance: V1-F3, V3-F5, INV-005; C-005.
7. **Change 7 ("CRITICAL is blocking" kept).** Applied as K7. Before: V1-F4 MINOR. After: MEDIUM, adds SPEC:739's CRITICAL-to-Blocking mapping, P4:98 re-pin, `spec-panel.md:259` resulting text, over-blocking bounded by the cap. Provenance: V1-F4, PRIOR H8; C-009.
8. **Change 8 (sibling doubt and label lines).** Applied as K6. Before: V1-F5 MINOR with `agent_template_qa.md:268` and `skill_template.md:815`. After: MEDIUM, merged with V3-F7 (line 841 VERBATIM note, possibly deliberate), P4:61 "and the like" coverage, fix: list as deliberate keeps with the reason. The `:268` and `:815` items were not carried, because the settled finding names only the four lines of the dispatch. Provenance: V1-F5, V3-F7; C-008.
9. **Change 9 (pointer exclusion and plugin decision).** Applied as K5 (MEDIUM) and K9 (minor owner-tracking). Before: V1 had both only in Checked. After: two findings, each a recorded decision, with BRIEF:16 and the owner's answers cited. Provenance: V2-F1, V2-F2, PRIOR H2; C-006, C-007, X-002.
10. **Change 10 (wording gaps).** Applied as K10, minor. Before: V1-F6 items (a) to (c). After: adds item (d) from V3-F6 (merge line only in `agent_template_qa.md`, line 85). Provenance: V1-F6, V3-F6, PRIOR H10 and H13; C-010.
11. **Change 11 (Kept mechanical gates section).** Applied as new K11, minor. Before: absent. After: P4:48 accepts a listed keep, S3:162 creates the section only on a first keep; fix: create it if absent. Provenance: probe INV-007.
12. **Change 12 (Checked and earlier findings).** Applied. Before: V1 Checked held "Every test path in the Task 5 run list exists (checked by Glob)" and the H1 to H13 status mixed into Checked. After: the statement is dropped (three test files and the skill folder do not exist yet, re-checked with `test -e`), the H1 to H13 status is its own section with live citations, and the Checked section keeps only re-counted facts. Provenance: V1 Checked, scorer correction in base-selection.md.

## Post-merge validation

- **Structure.** Card order: title, Keys (7 keys, one per line), Verdict, Findings (11 lines K1 to K11, each followed by a `<!-- Source: ... -->` line, no table), Earlier-findings status (H1 to H13), Reviewer disagreement, Dropped, Checked. Each section carries a provenance comment. Heading levels: one H1, all sections H2.
- **Internal references.** K-numbers named in the Earlier-findings and Disagreement sections (K1, K2, K5, K7, K8, K9, K10) all exist; every diff point named (C-001 to C-011, X-001 to X-003) exists in `diff-analysis.md`; every probe id (INV-003, INV-005, INV-007) exists in `invariant-probe.md`.
- **Grade counts.** 7 MEDIUM (K1 to K7) and 4 minor (K8 to K11), 0 blocking, matching the Verdict line. Every grade is the settled grade of the dispatch; none was changed.
- **Contradiction re-scan.** The Verdict says no finding is blocking and every K line says `blocking false`. K1 says both readings of the cap count are open; Checked does not claim the cap check passes. Earlier-findings H8, H9 and H10 point to K7, K1 and K10, and those findings describe the same defects. Dropped removes V1's Glob statement; Checked states the opposite fact. No contradiction found.
- **Citations re-read.** Every quoted citation was re-read during this merge (Read of P4, PRIOR and the ADV files; Grep and read-only `awk` line prints of SPEC, S1, S3, BRIEF, OPEN-QUESTIONS, the ledger and every `src`, `plugins` and `tests` line). A script then matched each of the 168 `path:line "quote"` citations of the card against its live line: 168 matched, 0 failed. The card holds no em dash and no en dash.
- **Line-number corrections against the dispatch.** (a) The dispatch placed the owner's plugin-parity statements at OPEN-QUESTIONS lines 44 and 83 (as the Round 2 notes did); the live file holds them at lines 74 ("This is not a decision to remove plugin parity.") and 113 ("The owner's answer said to reassess plugin parity, not to remove it: confirm."), so the card cites 74 and 113. (b) The dispatch placed the registry counts at S1:110; that line is blank, and the counts are at S1:113 ("19 rows in all"), which the card cites. (c) The dispatch called `test_review_severity_mapping.py:58` the only pin of "follow-up candidates"; line 71 also pins it, so the card says the mapping test is the only test file that pins it. (d) `grep -c "NO LENIENCY"` on `agent_template_qa.md` prints 4 (lines 95, 96, 100, 102), not the 3 V1 listed; the plan's check is "3 or more", so it still holds.

## Summary

All 12 planned changes were applied to the V1 base without improvisation; the four rejected alternatives were not merged. The card holds 11 findings (7 MEDIUM, 4 minor, 0 blocking) with a PASS verdict, the H1 to H13 status, the settled disagreements, 4 dropped items and 14 checked items. Not written: `merged-verdict.yaml`, which the plan lists but the dispatch excluded.
