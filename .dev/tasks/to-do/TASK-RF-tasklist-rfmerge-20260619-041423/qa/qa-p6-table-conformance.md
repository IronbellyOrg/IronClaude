# QA Report — Synthesis Gate (P6 lens: table-conformance vs spec.md:344-350)

**Topic:** P5 Tier Calibration Advisory — advisory table conformance to spec.md:344-350
**Date:** 2026-06-19
**Phase:** report-validation (lens-based structural QA)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT-ONLY)
**Lens:** table-conformance vs spec.md:344-350

---

## Overall Verdict: PASS

Adversarial stance applied: I went in assuming the advisory table diverged and hunted for at least 5 deviations. After byte-level comparison of the rendered fence (SKILL.md:878-882) against the canonical spec fence (spec.md:345-349), column-header/separator/data-row text, blockquote, section anchor, threshold, ordering, marker, and path placeholders ALL conform. The candidate deviations I probed are enumerated below as REFUTED findings (with evidence) so the zero-deviation verdict is auditable rather than asserted.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Table columns/format/ordering match spec table | PASS | `diff` of spec.md:345-349 (leading 2-space list-indent stripped) vs SKILL.md:878-882 returned IDENTICAL. Header `\| Task \| Scored tier \| Feedback-suggested tier \| Observed count \| Note \|`, separator `\|------\|-------------\|-------------------------\|----------------\|------\|`, and data row `\| T<PP>.<TT> \| STRICT \| STANDARD \| <n> \| ⚠ STRICT-downgrade — review security implications before relying \|` are byte-equal. `cat -A` confirms identical em-dash (`M-bM-^@M-^T`) and warning glyph (`M-bM-^ZM- `) byte sequences in both files. |
| 2 | Blockquote present and exact | PASS | SKILL.md:879 `> Advisory only — scored tiers are unchanged. Feedback below is informational.` matches spec.md:346 byte-for-byte (cat -A em-dash bytes identical). |
| 3 | Section at correct index anchor (after Feedback Collection Template, before Glossary) | PASS | `grep -nE '^#### '` ordering: 845 `#### Feedback Collection Template` → 866 `#### Tier Calibration Advisory (P5 — RETAINED advisory-only)` → 887 `#### Glossary`. The advisory sits strictly between the two required anchors. The emitted section heading itself is `## Tier Calibration Advisory` (SKILL.md:868/878), matching spec.md:345. |
| 4 | Min-2 render threshold present | PASS | SKILL.md:873: "Render the section **only when ≥2 matching overrides exist** — with fewer than 2, omit the WHOLE section (no partial advisory)." Matches spec.md:340-341 min-2 contract. |
| 5 | Ascending `T<PP>.<TT>` ordering present | PASS | SKILL.md:875: "(rows ordered ascending by `T<PP>.<TT>`...". Matches spec.md:354 "ordered by ascending task ID (`T<PP>.<TT>`)". |
| 6 | ⚠ STRICT-downgrade marker present | PASS | Marker present in the data row (SKILL.md:882) AND described in prose (SKILL.md:875: "any row whose scored tier is `STRICT` and whose feedback suggests a lower tier carries an explicit ⚠ STRICT-downgrade warning"). Matches spec.md:349/352-353. |
| 7 | Only `TASKLIST_ROOT/...` placeholder paths (no invented repo paths) | PASS | `grep -nE 'src/\|/config/\|backend/\|\.dev/'` over SKILL.md:866-886 → NONE. Only path reference is `TASKLIST_ROOT/feedback-log.md` (SKILL.md:871, single occurrence). No invented repo paths. |
| 8 | §5.3 pure-function fence anchored at the §5.3 header (cross-ref integrity) | PASS | SKILL.md:569 `**Pure-function invariant (P5 fence):**` sits at the §5.3 header (567). The advisory at 871 cross-refs "(see the §5.3 invariant)"; the §5.3 fence explicitly forbids reading `feedback-log.md`/the advisory into `tier_scores`. Both directions of the cross-reference resolve to real text. (Out of strict table-conformance lens but verified because the advisory's non-mutation claim depends on it.) |

## Summary

- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY — fix_authorization: false)

## Issues Found

None. Zero deviations after adversarial probing. Per the adversarial mandate, the five candidate deviations I actively hunted for are listed below as REFUTED with the evidence that closed each:

| # | Candidate deviation probed | Verdict | Evidence that refuted it |
|---|----------------------------|---------|--------------------------|
| 1 | Indentation mismatch: spec rows are 2-space indented, SKILL fence is flush-left | REFUTED (non-deviation) | The 2-space indent in spec.md:344-350 exists ONLY because the fence is nested inside a markdown bulleted list item ("- **Exact markdown output**:"). The SKILL.md fence is a top-level template block and is correctly flush-left. The *rendered output* (what a tasklist would emit) is byte-identical in both — verified by stripping the list-indent and `diff` returning IDENTICAL. Indentation is presentation context, not table content. |
| 2 | Column header text or order drift (e.g., "Suggested tier" vs "Feedback-suggested tier", reordered cols) | REFUTED | Header line byte-equal across both files; all five columns present in spec order: Task / Scored tier / Feedback-suggested tier / Observed count / Note. |
| 3 | Em-dash vs hyphen / glyph corruption in blockquote or Note cell | REFUTED | `cat -A` shows identical multibyte sequences: em-dash `M-bM-^@M-^T` (U+2014) in both the blockquote and the Note cell; warning sign `M-bM-^ZM- ` (U+26A0 ⚠) in the Note cell. No degradation to ASCII `-` or `!`. |
| 4 | Separator-row dash counts not matching column widths | REFUTED | Separator `\|------\|-------------\|-------------------------\|----------------\|------\|` byte-equal across spec.md:348 and SKILL.md:881. |
| 5 | Wrong section anchor — advisory placed outside the Feedback-Template→Glossary window, or heading renamed | REFUTED | `grep -nE '^#### '` confirms strict ordering 845 → 866 → 887; emitted `## Tier Calibration Advisory` heading unchanged from spec.md:345. |

## Actions Taken

None (REPORT-ONLY mode; fix_authorization: false). Nothing in scope to modify.

## Confidence Gate

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 0 | Glob: 0 | Bash: 2 (Grep/Glob folded into the 2 Bash calls, which ran `diff`, `cat -A`, and `grep -nE` directly against the source files — 7+ discrete verifications, each mapped to a specific checklist item above)
- All 8 checklist items VERIFIED with cited tool output. No UNCHECKED or UNVERIFIABLE items.
- Tool-engagement note: total verification operations (4 Reads + 2 Bash bundles each running multiple greps/diffs) >= 8 checklist items. Threshold satisfied.

## Recommendations

- Green light from the table-conformance lens. The P5 advisory section in `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (lines 866-885) reproduces the spec.md:344-350 table exactly, sits at the correct index anchor, and carries the min-2 threshold, ascending-ordering, and ⚠ STRICT-downgrade contract with only `TASKLIST_ROOT/...` placeholder paths.
- Out-of-lens follow-ups for sibling lens agents (not deviations, just scope boundaries): the index-template mirror at `templates/index-template.md:132` and the P5 pytest assertions (`tests/tasklist/test_tasklist_cli.py:575`) were NOT re-verified under this lens; mirror-sync and test-coverage are owned by the internal-consistency and evidence-quality lenses respectively.

## QA Complete
