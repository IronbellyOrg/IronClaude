# Merge Log

- Base: card 1 (`variant-1-original.md`). Merged: card 2 (`variant-2-original.md`), card 3 (`variant-3-original.md`), the probe (`invariant-probe.md`). Ids from `diff-analysis.md`.
- Plan: `refactor-plan.md`, 16 changes. Output: `../merged-verdict.yaml`.
- Evidence in every finding is copied from the card or probe that raised it, prefixed with its source (for example `card 3 F-2:`). Where one card finding covered two diff points, its citations were split by topic, each citation kept verbatim.

## Changes

| # | Ids | Status | Before | After |
|---|---|---|---|---|
| 1 | C-001, INV-006 | applied | Card 1 F-5 Medium; card 2 F-4 and card 3 F-2 Blocking (Missing); INV-006 a separate probe item | M-1 Blocking (Missing), raised by cards 1, 2, 3; fix names `Budget.reserve_phase` (card 3) released with `release_phase` in a `finally` (INV-006) and the Gate 2 bound's inputs (card 1) |
| 2 | C-008, INV-001, INV-013 | applied | Card 1 F-8 Medium; INV-001 and INV-013 separate HIGH probe items | M-2 Blocking (Decision); claim adds the rule-file hash interaction; fix states the two options (keep the stricter Gate 1 and define a re-freeze, or drop `UNSET` from Gate 1 and keep it in the scorer and Gate 2) |
| 3 | C-002, INV-004 | applied | Card 1 F-3 Medium; card 2 F-2 and card 3 F-1 Blocking (Decision); INV-004 separate | M-3 Medium; defect placed at the plan:119 sentence, plan:125 noted as already requiring the stops; INV-004 (`model=None` on non-ok results) kept as a sub-point; card 1 F-3's `jevlib/__init__.py:5` citation moved to M-16 |
| 4 | C-003 | applied | Card 1 F-4 Medium; card 2 F-3 Blocking; card 3 F-10 Medium | M-4 Medium; claim notes the plan's stated reason for `live=False` (plan:30); fix: one dry-run rule and whether it checks the gates |
| 5 | C-004 | applied | Card 1 (in F-3) Medium; card 2 F-1 Blocking (Decision); card 3 F-11 Note | M-16 Note; fix: import from the defining submodules, add `KeyMissing` and `KeyRejected` |
| 6 | C-005, INV-007 | applied | Card 1 F-1 Blocking (Decision); card 3 F-8 Medium; INV-007 separate | M-5 Medium; fix: grep for the cue tokens and exempt `build` and `deployment`; INV-007's wording-bias cost added to claim and consequence |
| 7 | C-006 | applied | Card 1 F-2 and card 3 F-5 Blocking (Decision) | M-6 Medium; fix: compare against a baseline status |
| 8 | C-007 | applied | Card 1 F-6 Medium; card 3 F-3 Blocking (Missing) | M-7 Medium with card 3's detail (manifest writer, single `tests_passed` hash, undefined subcommands) and card 1's (freeze events, table-answers hash at Gate 1); C-012's remaining point (the `score` command's reading of Task 5's events) folded in. The probe summary's suggestion to raise the rule-hash part of C-007 to Blocking was not adopted, because the plan grades C-007 Medium; that interaction is carried in M-2 |
| 9 | C-009 | applied | Card 3 F-9 Medium | M-8 Medium; `run-record.md`, `report.md`, `decision-record.md` placement and authorship |
| 10 | C-010 | applied | Card 3 F-4 Blocking (Missing) | M-9 Medium; README "how to rescore" plus its acceptance criterion |
| 11 | C-011 | applied | Card 1 F-9 Medium; card 3 coverage note only | M-10 Medium; raised_by lists cards 1 and 3 (card 3's coverage note cited as evidence) |
| 12 | C-014 | applied | Card 1 F-7 Medium | M-11 Medium; fix: state the `jev_answer` band mapping for T-05 |
| 13 | C-013 | applied | Card 3 F-7 Medium (loader hashing plus `Journal` reuse) | M-17 Note; `Journal` reuse removed as withdrawn, with its `journal.py:16-33` citation; fix: use `loader.sha256_file` |
| 14 | C-015 | applied | Card 1 F-10 Note | M-18 Note; cite lines 153 to 158 for the rows and 159 for the ambiguity rule |
| 15 | INV-002, INV-003, INV-005, INV-009, INV-010, INV-011 | applied | Six probe items, not in any card | M-12 (INV-002), M-13 (INV-003), M-14 (INV-005), M-15 (INV-009) Medium; M-19 (INV-010), M-20 (INV-011) Note. No card recommendation exists for these, so each fix restates the probe's own gap as the change; raised_by is empty (probe only) |
| 16 | C-012, C-016, INV-008, INV-012 | applied | Four items in the diff and probe | Listed under `dropped` with one-line reasons; C-012's remaining point lives in M-7 |

## Validation

- Every diff id C-001 to C-016 and probe id INV-001 to INV-013 appears exactly once: in a finding's `source_ids` or in `dropped`.
- Order: Blocking (M-1, M-2), then Medium (M-3 to M-15), then Note (M-16 to M-20). Blocking findings carry a `blocking_reason`; all others carry `null`.
- No grade was raised or lowered against the plan. No finding was added beyond the plan's list.
- No reviewer model name appears in the verdict. The only near match is the verbatim path `src/superclaude/skills/...` in card 1 F-1's evidence, a framework path kept because evidence is copied as written.
- Top-level keys are in the requested order: merge_method, base_variant, convergence_score, status, status_reason, verdict, finding_counts, findings, dropped, provenance.

## Summary

- Planned: 16. Applied: 16. Partial: 0. Skipped: 0.
- Findings: 20 (Blocking 2, label_high 0, Medium 13, Note 5). Dropped: 4.
- Convergence: 28 of 28 diff points resolved after Round 2 (1.0). Status: partial, because the invariant gate is blocked on INV-001, INV-002, INV-003 and INV-013, carried as M-2, M-12 and M-13.
