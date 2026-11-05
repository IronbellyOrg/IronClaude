# Merge Log

<!-- Provenance: produced by /sc:adversarial (Step 5, merge executor) -->
<!-- Base: Variant 3 (reviewer-3 card, refactorer, claude-opus-5-5) -->
<!-- Merge date: 2026-11-05 -->

- Base: `variant-3-original.md`
- Plan: `refactor-plan.md` (6 planned changes, auto-approved)
- Output: `merged-verdict-card.md`
- Repository files touched: none (only `merged-verdict-card.md` and this log were written)

## Applied changes

| # | Status | Provenance tag | Result in merged card | Note |
|---|---|---|---|---|
| 1 | applied | V2 R2-1 | M-3 (blocking) | Task 3 AC grep `models opus,sonnet` (plan:65) vs mandated bullet (plan:62); fix `grep -n -- "--models"`; text and citations copied from V2. |
| 2 | applied | V1 R1-2 | M-4 (blocking) | `D12-reflect.md:235` pin; severity raised from V1's minor to blocking as the plan states (missing spec item (4) deliverable); citations 228, 243, `runner.py:507-508` kept. |
| 3 | applied | V1 R1-1 | M-5 (minor) | Ladder activation kept minor; added the plan's acceptance criterion (record in `./artifacts/t5-notes.md` and Task 6 "Known consequences"). |
| 4 | applied | V1, V2 (+ V3 base items) | M-6, M-8, M-9, M-10, M-12, M-13, M-14, M-15, M-16 | Duplicates merged: R3-3+R1-8 (M-6); R3-5+R2-3+R1-10 plus the calibrator markdown-body gap, text copied from `reviewer-cards/reviewer-3-calibration.yaml:15` (M-8); R3-6+R1-9 (M-9); R3-7+R2-2+R1-12 (M-10); R1-5+R3-8 Task 6 part (M-12); R1-3 (M-13), R1-4 (M-14), R2-4 (M-15), R2-5 (M-16) added singly. |
| 5 | applied | V3 R3-9 | M-17 to M-22 | R3-9 split into six items: forward link, Task 9 dependency, duplicated sentence, test overlap, dead allow-list entry, Task 9 anchor correction. R3-8 also split (Task 8 scope note M-11; Task 6 wording into M-12). |
| 6 | applied | V1 Coverage audit (U-001) | M-23 (minor) | Legacy T1Model01/T1Model02 slots (`defaults.sh:63-65`); fix: state it in retry.md. |

## "Changes NOT Being Made" honoured

| Diff point | How it was honoured |
|---|---|
| X-002 / C-012 (R1-6) | Not a finding; the `tests/swarm/test_coder_tier_env_2026_10.py:18,115-124` location kept as a note inside M-11. |
| X-001 (V1 PASS_WITH_NOTES) | Verdict is FAIL; V1's verdict not carried over. |
| C-008 (R3-8 scope creep) | Kept as a minor note only (M-11), owner agreement stated as the open question. |
| C-013 (R1-3) | Kept minor (M-13); fix is cite or drop; notice recorded as observed in the orchestrator's throwaway-HOME run, not in the repo. |
| R3-7 / R1-11 (commit 70ef6486) | Recorded as resolved for `audit-scanner.md` in M-10 and in Verified correct; R1-11 not added as a finding. |

## Items not listed in the plan (escalation)

- V1 R1-7 (Task 5 grep `T[0-4]_Model0` could be tripped by the Task 1 test file or Task 6 doc) is not named in any planned change, so it was not merged. The orchestrator should decide whether to add it as a minor item.
- V1 R1-11 is covered only through the plan's "resolved" note (see above), not as a separate item.

## Summary

- Planned: 6. Applied: 6. Skipped: 0.
- Merged card: 4 blocking (M-1 to M-4), 19 minor (M-5 to M-23).

## Post-merge checks

| Check | Result |
|---|---|
| Heading hierarchy has no gaps | PASS: one H1, then six H2 sections (Verdict, Blocking findings, Minor findings, Coverage audit, Verified correct, Self-confidence); no H3 or deeper, no skipped level. |
| Every cited id in brackets exists in a variant file | PASS: R1-1, R1-2, R1-3, R1-4, R1-5, R1-8, R1-9, R1-10, R1-12 are in `variant-1-original.md`; R2-1 to R2-5 in `variant-2-original.md`; R3-1 to R3-9 in `variant-3-original.md`. The one non-R bracket, `[V1 coverage note]`, points at V1's Coverage audit section (diff point U-001), which has no R id. |
| No new contradiction versus the variants | PASS with two plan-directed differences: the FAIL verdict contradicts V1's PASS_WITH_NOTES (rejected by the plan, X-001), and M-4 is blocking where V1 graded R1-2 minor (plan change 2). V2's "allow-list is complete for the current tree" agrees with V3's "the 9 files containing the text are all allow-listed" and with M-21 (dead `commands/issue.md` entry). Verified-correct line ranges for the Task 9 anchors (V2 `ccsession:1100-1102`) and V3's `1099-1103` overlap; both kept as written. |
