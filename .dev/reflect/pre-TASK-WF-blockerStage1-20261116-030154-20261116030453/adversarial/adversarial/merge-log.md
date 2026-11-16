# Merge Log

- Base: Variant 1 (sonnet:analyzer), `variant-1-original.md` (not edited)
- Plan: `refactor-plan.md` (9 changes, 5 removals, 5 changes not made)
- Output: `../merged-review-card.md`
- Merge date: 2026-11-16T03:55:55Z
- Citation rule applied: every citation was Read at its cited line range before it was kept, then all 40 were re-checked by script (quote found in the range, whitespace-insensitive, at most 200 characters): 40 of 40 pass.

## Changes

### Change #1 — MF1 -> card F1
- Status: applied
- Before: Variant 1 F3 (MAJOR, blocking, contradiction) mixed the Task 7 grep line with a refuted `verify-sync` half and hedged "Tasks 12 and 13 likely"; 3 citations.
- After: F1, MAJOR, blocking true, unpassable-check; plan claim text; Task 12 named as a certain second match; end-point rule backed by the plan, source.md and the stage ledger README; 6 citations.
- Provenance: Base modified (Variant 1 F3 first half) + Variant 2 F1 + Variant 3 F2, per Change #1.
- Validation: 6 of 6 citations match (PLAN:115, 148, 171, 24; source.md:17; README.md:33). Ranges written as `N-N`.

### Change #2 — MF2 -> card F2
- Status: applied
- Before: Variant 1 F1 with 3 citations; no OD10 fact, no SPEC:145.
- After: F2, MAJOR, blocking true, unpassable-check; plan claim text (Task 3 + Task 5 + T4, OD10 undecided); 5 citations.
- Provenance: Base modified (Variant 1 F1) + Variant 3 F1 + Variant 2 F2, per Change #2.
- Validation: 5 of 5 match (PLAN:62, 87, 209; SPEC:582, 145). The PLAN:87 quote is the plan's longer form ("no file of the skill folder cites a `.dev/` or `./artifacts/` path"), not the base's shorter form.

### Change #3 — MF3 -> card F3
- Status: applied
- Before: Variant 1 F2, MAJOR, blocking true, contradiction; 4 citations.
- After: F3, MAJOR, blocking false, contradiction; plan claim text (gap shows at stage 3, no stage 1 check fails); 6 citations.
- Provenance: Base modified (grade changed per debate C-003, Removal #5), per Change #3.
- Validation: 6 of 6 match (PLAN:65; stage3-request.md:14; SPEC:845, 920; remediate_parser.py:55; fmea_classifier.py:304). Lines 301 and 323 are named in the claim text only, as in the plan.

### Change #4 — MF4 -> card F4
- Status: applied
- Before: Variant 2 F3 (MAJOR, blocking true) with absolute paths and range PLAN:110-115; Variant 1 F6 first half (MINOR, "ledger adapters").
- After: F4, MAJOR, blocking false, missing-requirement; plan claim text including the dissent sentence; 4 repo-relative citations, each pinned to its single line.
- Provenance: Variant 2 F3 merged per Change #4, with Base F6 first half folded in.
- Validation: 4 of 4 match (SPEC:404, 945; PLAN:110, 113).

### Change #5 — MF5 -> card F5
- Status: applied
- Before: Variant 1 F4 with the wording "Task 12 reaches it only through Task 9"; 2 citations.
- After: F5, MAJOR, blocking false, other; that wording removed; path-root and label-less-row gaps (INV-002, INV-003) added; 6 citations.
- Provenance: Base modified (Removal #3) + invariant probe INV-002, INV-003, per Change #5.
- Validation: 6 of 6 match (PLAN:136, 134, 59, 209, 25; SPEC:748). During writing I first added a parenthetical on Task 12's dependencies (from the plan's instruction note); I removed it so the claim text equals the plan's.

### Change #6 — MF6 -> card F6
- Status: applied
- Before: second half of Variant 1 F6 (combined with "ledger adapters").
- After: F6, MINOR, blocking false, other; standalone; 2 citations.
- Provenance: Base modified (split from Variant 1 F6), per Change #6.
- Validation: 2 of 2 match (PLAN:146, 148).

### Change #7 — MF7 -> card F7
- Status: applied
- Before: invariant probe INV-001 only (not in any variant).
- After: F7, MAJOR, blocking false, other; 4 citations.
- Provenance: invariant probe INV-001, per Change #7.
- Validation: 4 of 4 match (PLAN:157, 165, 171, 159).

### Change #8 — MF8 -> card F8
- Status: applied
- Before: invariant probe INV-004 and INV-005 only.
- After: F8, MINOR, blocking false, other; 4 citations.
- Provenance: invariant probe INV-004, INV-005, per Change #8.
- Validation: 4 of 4 match. Citation fixed: the plan's single `src/superclaude/cli/review/__init__.py:24-25 "lint_cmd" and "estimate_cmd"` was read (line 24 `"lint_cmd",`, line 25 `"estimate_cmd",`) and written as two citations, `:24-24 "lint_cmd"` and `:25-25 "estimate_cmd"`. A `ls` of `cli/review/*_cmd.py` confirms 7 modules (no `lint_cmd.py`, no `estimate_cmd.py`). The PLAN:53 quote keeps its inner double quotes escaped with a backslash, as the variants do.

### Change #9 — MF9 -> card F9
- Status: applied
- Before: T1 card observation O7 only (calibrator confidence 0.60).
- After: F9, MINOR, blocking false, other, labelled "[T1-only, not debated]"; 3 citations.
- Provenance: T1 card O7, per Change #9.
- Validation: 3 of 3 match. PLAN:72 was read and quoted ("State that the final-gate sweep records rows as `sweep-flagged` in stage 2"). SPEC:379-390 was read: the table has eight states (`recorded`, `offered`, `resolving`, `resolved`, `filed`, `declined`, `duplicate`, `superseded`) and no `sweep-flagged`; quoted row from SPEC:383, cited as the range 379-390 so the citation covers the "eight states" claim.

## Removals

1. Variant 1 F3 second half (Task 1 `verify-sync` line): removed. Refuted by PLAN:25 (standing `make sync-dev` order); C-010 NOT-A-DEFECT.
2. Variant 1 F5 (`.dev/pr-monitor/` vs Task 5's grep): removed. C-006 NOT-A-DEFECT, unanimous.
3. Variant 1 F4 wording "Task 12 reaches it only through Task 9": removed (see Change #5).
4. Variant 1 Checked bullet "the 9 `review` subcommands in `cli/review/__init__.py:19-29`, with no name clash for `classify`": removed; Variant 3's bullet (lint and estimate modules absent, import optional) kept instead.
5. Variant 1 F2's "blocking true": replaced by blocking false (Change #3).

Changes NOT made (C-004 blocking grade, C-008, C-009, C-010, S-002 absolute paths): none of them appears in the card; the C-004 dissent is recorded in F4 and in Debate notes.

## Other card sections

- Verdict: rewritten from Variant 1's three blocking defects to the two that remain (F1, F2), per the orchestrator brief.
- Checked: 18 bullets merged from the three variants' Checked lists, de-duplicated (cap sentence, `rf-qa.md`/`card_convert.py`, 11 files with the old sentence, `test_review_cli.py`, base-report status were each stated by two or three variants). Variant 1's "Not verified" list dropped `origin_repo.py`, because Variant 3 verified it. Variant 2's absolute citation path converted to repo-relative.
- Base-report findings status: written as the brief directs (F4, F5, F9, F12, F13, F15 resolved; F3 and F6 partly resolved). All three variants listed F3 as resolved; the brief marks it partly resolved, which the card ties to the allow-list gap of card F3 (the stage ledger README:27 files the merge-rule allow-list under base findings F3, F9, F13). Flagged for the orchestrator: this status line follows the brief, not the variants.
- Debate notes: 5 bullets (convergence, base selection, F4 dissent, F3 regrade, reviewer 2 identity).
- Self-report: the line given in the brief, verbatim.

## Post-merge validation

- Structure: PASS. Three provenance comments head the card; the H2 sections run Verdict, Findings, Checked, Debate notes, Self-report; findings F1 to F9 are numbered in plan order MF1 to MF9, one line each in the variant format, blocking findings (F1, F2) first; each finding has a `<!-- Source: ... -->` comment on the line above it.
- References: PASS. 40 of 40 citations re-checked by script against the files (quote in range, whitespace-insensitive, at most 200 characters); every path is repo-relative and every range is `start-end`. Internal references (F1, F2, F3, F4, F8 named in Verdict, Checked and Debate notes) resolve to existing findings.
- Contradictions: PASS. Exactly two finding lines say `blocking true` (F1, F2), matching the Verdict; F3's non-blocking grade matches the Debate notes regrade; the removed texts (`verify-sync` half, `.dev/pr-monitor/`, "reaches it only through Task 9", "9 `review` subcommands") occur only inside provenance comments, and F8 and the Checked list both say 7 subcommand modules exist. One open item for the orchestrator: the base-report status of F3 (partly resolved) follows the brief and differs from all three variants (resolved).

## Summary

- Planned changes: 9; applied: 9; failed: 0.
- Removals: 5 of 5 applied.
- Findings in the card: 9 (2 blocking, 7 non-blocking; 6 MAJOR, 3 MINOR).
- Citations: 39 planned, 40 kept (one split into two); fixed: 1 (`__init__.py:24-25` split into `:24-24` and `:25-25`); shortened: 0; failed: 0; findings without evidence: 0.
- Files changed: `../merged-review-card.md` (new), this log (new). The base variant and every other file were not edited.
