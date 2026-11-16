# Merge Log

## Metadata

- Base variant: `adversarial/adversarial/variant-2-original.md` (reviewer-2, qa persona, opus class)
- Refactoring plan: `adversarial/adversarial/refactor-plan.md` (12 change groups, 15 findings)
- Non-base sources incorporated: `variant-1-original.md` (F4, F7, F9), `invariant-probe.md` (F1 narrowing, F2, F3, F5, F6, F7, F8, F10 to F13, F15)
- Output: `adversarial/merged-review-card.md`
- Merge date: 2026-11-15
- Executor: merge-executor (plan fidelity only; no plan file edited)
- Instruction from the orchestrator beyond the plan: add `PLAN:490` and `PLAN:513` to F6 (removal of the six stage 4 files from the Task 13 allow-list)

## Changes Applied

| # | Finding | Planned change | Status | Source | Provenance tag in card |
|---|---|---|---|---|---|
| 1 | F1 | Owner gates cannot be enforced by `/sc:implement`; four go points; "inevitable bypass" and "Tasks 11 to 46 run straight through" dropped | Applied | V2 F1 (base), narrowed by debate C-005, A-001 and probe INV-010, INV-011, INV-020 | `Base (reviewer-2 F1), narrowed by debate C-005 and A-001 and by probe INV-010, INV-011, INV-020` |
| 2 | F2 | Task 31 gates nothing; fix is an acceptance line on Task 33, not a dependency line | Applied | V2 F2 (base) plus probe INV-001, INV-002 | `Base (reviewer-2 F2), corrected by probe INV-001 and INV-002` |
| 3 | F3 | Task 40 allow-list names a plugin mirror that Task 46 creates later | Applied | V1 F1 and V2 F3 second half (C-001), probe INV-008, INV-015 | `Base (reviewer-2 F3 second half) and variant 1 (reviewer-1 F1) ... plus probe INV-008 and INV-015` |
| 4 | F4 | Task 41 gives the analysis template a digest and registry row the registry does not have | Applied | V1 F2 (confirmed by advocates, probe INV-009, INV-012) | `Variant 1 (reviewer-1 F2) ...` |
| 5 | F5 | Task 25 T3 fails on `commands/spec-panel.md:220` and its twins | Applied | V2 F4 (base) plus probe INV-007 | `Base (reviewer-2 F4), widened by probe INV-007` |
| 6 | F6 | Later tasks make earlier acceptance lines false; final review cannot pass; PLAN:490 and PLAN:513 added | Applied | Probe INV-004 | `Probe INV-004 ...; Task 13 allow-list citations PLAN:490 and PLAN:513 added at the orchestrator's instruction` |
| 7 | F7 | Fresh-findings set and held-out split never evaluated | Applied | V1 F3, widened by probe INV-006; grade by judge (C-004) | `Variant 1 (reviewer-1 F3), widened by probe INV-006 ...` |
| 8 | F8 | Phase 3 to 5 entry numbers undefined or without a task | Applied | Probe INV-005 | `Probe INV-005 (no card reported it)` |
| 9 | F9 | Task 46 copies the skill folder before adding the `canonical` row | Applied | V1 F4 and V2 F5 (C-002), probe INV-008 | `Variant 1 (reviewer-1 F4) and base (reviewer-2 F5) ...` |
| 10 | F10 | Seeded-recall pass line can be met on an underpowered set | Applied | Probe INV-003 | `Probe INV-003` |
| 11 | F11 | Task 31 does not alternate order or require fresh spawns | Applied | Probe INV-018 | `Probe INV-018` |
| 12 | F12 | T3 may fail a `pointer-only` row before its pointer exists | Applied | Probe INV-019 | `Probe INV-019` |
| 13 | F13 | Wording-dependent scan trips in `scale-map.md` and `rule.md` | Applied | V2 F3 first half (C-007), probe INV-014 | `Base (reviewer-2 F3 first half) ... plus probe INV-014` |
| 14 | F14 | Coverage-matrix omissions in the review run | Applied | V2 F6 (C-009) | `Base (reviewer-2 F6), debate C-009` |
| 15 | F15 | Installed reference files cite `.dev/` package paths | Applied | Probe INV-016 | `Probe INV-016` |

The plan's 12 change groups map to F1 to F15 as written in the plan's "Planned Changes" (the plan numbers its changes 1 to 15 under 12 sources groupings; all 15 were applied).

Also applied: Checked section merged (base bullets kept; V1's four bullets added, the duplicate "one sweep and one offer" anchor kept once in the base form; V1's "no files changed" bullet reworded to name reviewer-1); header lines `persona`/`model_class`/`model` replaced by `merged_from: reviewer-1, reviewer-2, invariant-probe`; Self-report set to the two required lines; PLAN defined once at the top.

## Notes on citations

- Citation paths and line numbers are those of the refactor plan. Quotes were taken from the cards and the probe, or read from the live line when the plan gave only a line number; each quote is a verbatim substring of its line and under 15 words. Where a card's quote was over 14 words, a shorter verbatim substring was used (PLAN:87, PLAN:203, PLAN:328, PLAN:551, merged-requirements.md:940).
- Plan citations given as `:87`-style continuations were expanded to full paths.
- F10 citation `PLAN:376` was given without a distinct quote; the same clause quoted at PLAN:102 appears at PLAN:376.
- No citation outside the refactor plan was added, except PLAN:490 and PLAN:513 on F6 as instructed. The Checked section keeps the PLAN line references of the two source cards.
- Category labels for F10 to F15 are not in the plan; they were set to the nearest label (F10 sufficiency, F11 other, F12 unpassable-check, F13 unpassable-check, F14 missing-requirement from V2 F6, F15 other). A reviewer may relabel them without changing severity or blocking.

## Post-Merge Validation

- Heading structure: `## Verdict`, `## Findings`, `## Checked`, `## Self-report`, in that order, one each. PASS.
- Findings present: 15 lines matching `^F<n> | severity ... | blocking ...`, F1 to F15 in the plan's order. PASS.
- Blocking flags: F1 to F8 `blocking true`; F9 to F15 `blocking false`. Counts 8 and 7. PASS.
- Severity: F1 to F8 MAJOR, F9 to F15 MINOR (the plan sets blocking only; severity follows the source cards). PASS.
- Citations: every finding has at least 2 citation lines (F8 has 4, F9 has 2). PASS.
- PLAN line numbers: the set of `PLAN:<line>` numbers per finding was compared with the refactor plan's Citations line for the same change. F1 to F5 and F7 to F14 match exactly; F15 matches (its Checked-section references are outside the finding); F6 equals the plan set plus PLAN:490 and PLAN:513 (instructed). No number changed. PASS.
- Internal references: F3 refers to F9 and F13; F9 refers to F3; F1 refers to PLAN:20's four go points; F8 refers to the F1 fix. All exist. PASS.
- Contradiction re-scan: the Verdict names 8 blocking findings, matching the 8 flagged. The F1 claim states four go points while the Checked bullet (carried from the base card) says "Three owner gates"; this is the request's wording that the plan keeps, not a contradiction of F1, and is left as in the base. NOTE only.
- Plan files edited: none.

## Summary

- Planned: 12 change groups / 15 findings
- Applied: 15 findings (all 12 change groups)
- Failed: 0
- Skipped: 0
- Blocking findings: 8; non-blocking findings: 7
