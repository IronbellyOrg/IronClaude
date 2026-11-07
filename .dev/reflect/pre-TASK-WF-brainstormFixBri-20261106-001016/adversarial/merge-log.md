# Merge Log

## Metadata

- Status: partial
- Merge method: adversarial (`/sc:adversarial` Mode A, `--depth standard`, Step 5)
- Merge date: 2026-11-06
- Executor: merge-executor
- Subject: `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/TASK-WF-brainstormFixBri-20261106-001016.md`
- Base: Variant 2 (reviewer 2, qa, haiku slot), `variant-2-original.md`
- Plan: `refactor-plan.md` (Changes 1-12, auto-approved 2026-11-06T01:24:00Z)
- Output: `merged-verdict.yaml` (this folder)
- Convergence: 1.0 on the 24 diff points; invariant gate BLOCKED_BY_INVARIANTS (INV-020 HIGH, open)
- ID scheme: merged F-N = plan M-0N. Claim and change texts are the plan's, with M-NN renamed to F-N. The Tier-1 card's own F-1..F-4 appear only as "Tier-1 F-n".

## Changes applied

| # | Status | Target | Before (base V2) | After (merged) | Provenance |
|---|---|---|---|---|---|
| 1 | Applied | F-1 (new, first) | No finding on Task 6's tier wording | P1: plan:81 decides the folder by `quality_tier`; remedy = live-check and companion sentences from "Replacement wording" | V3 R3-1 diagnosis, widened by a3 New evidence 1; remedy from the plan (V3 `source` remedy not taken) |
| 2 | Applied | F-2 (base R2-1) | "doubly unpassable", no remedy | P1 single-clause failure; Task 1 saves `status-before.txt`, Task 7 compares with `status-after.txt`, package path exempt | Base R2-1 + V1 R1-2 remedy + INV-001 capture point |
| 3 | Applied | F-4 (base R2-3) | Section-wide assertion vacuous | Plus: Task 1's paragraph clause unpinned; paragraph-slice remedy | Base R2-3 + V3 R3-3 first half |
| 4 | Applied | F-5 (new) | Not in base | Routing pins scoped per codebase tier, `grep -c` kept as smoke check | V1 R1-3 + V3 R3-3 second half |
| 5 | Applied | F-7 (base R2-4) | Placement "not evaluated", no remedy | Companion sentence in 2.1, live-check sentence in 7.2 step 4, two-line AC, Necessary deviation recorded | Base R2-4 + V1 R1-8 + V3 R3-5; INV-017, INV-021 |
| 6 | Applied | F-3 (base R2-2) | Unpinned conditional, no remedy | P1: both halves pinned via shared phrases; Tasks 1-5 applied text copied verbatim | Base R2-2 + V1 R1-4 shape + V3 R3-6 (C-012) |
| 7 | Applied | F-8 (base R2-7) | Baseline 17, implying 18 | Recorded before-count plus 2; 17 kept as today's value only | Base R2-7 + V1 R1-6 / V3 R3-7; INV-008 |
| 8 | Applied | F-11 (new) | Not in base | Section 3.1, not section 6, for spec line 142 | V3 R3-4 |
| 9 | Applied | F-13 (new) | Not in base | Task 7 "no source file" wording | V1 R1-10 first half |
| 10 | Applied | F-14 (new) | Not in base | Drop "only for a nested command that ran"; keep the contract listed, failed calls included | V3 R3-9 reframed; a2 caveat (`debate-transcript.md:394`) |
| 11 | Applied | F-17 (new) | Not in base | Record plan:21 as the resolution of spec open item 8 | V1 R1-8 last sentence |
| 12 | Applied | F-15, F-16, F-4 extra assertion | Not in base | INV-016 routing bullet names `/sc:analyze`; INV-002 Constraints line; INV-005 absence check | invariant-probe.md |

Carried from the plan without a numbered change: F-6 (base R2-5, P2), F-9 (base R2-6), F-10 (base R2-8), F-12 (C-012, resolved through F-3), F-18 (INV-020, priority OPEN, open conflict).

## Post-merge validation

### Structure

- `yaml.safe_load` succeeds. Top-level keys: adversarial_status, base_variant, changes_not_made, confidence_note, convergence_note, convergence_score, findings, invariant_disposition, merge_method, path_aliases, replacement_wording, subject, unaddressed_invariants, unresolved_conflicts, verdict, withdrawn_or_replaced_claims.
- `merge_method` = `adversarial`. 18 findings in plan order: P1 3 (F-1..F-3), P2 14 (F-4..F-17), OPEN 1 (F-18). Every finding has priority, claim, evidence and recommended_action {file, change, verifier}.
- Deviation to escalate: F-18 carries priority `OPEN`, outside the requested P0|P1|P2 set, because the plan fixes M-18 as OPEN and says the executor does not re-decide priorities. It is also marked `status: open_conflict`.
- No HIGH invariant is marked resolved: INV-020 is `open_conflict` in `invariant_disposition` and listed in `unaddressed_invariants` and `unresolved_conflicts`.
- `invariant_disposition` has the plan's 14 UNADDRESSED rows; `changes_not_made` has the plan's 18 rows.

### References

- Every evidence `file:line` was re-Read in this task (plan, source.md, SKILL 175-204 and 358-379, routing 1-80, spec 58-75, 134-155, 212-225, 278-329, 372-379, 438-445, cmd 148-159, analyze.md 94-99, diagnostics.txt, managed-workspace.md 33-38, and the five test files at the cited ranges). Each one supports its claim.
- Not re-run by the executor: `git ls-files` = 953 and the `E-HALT-QA` path in F-2 (from C-001 and A-002); noted in F-2's `evidence_note`.
- Tags: F-14 and F-15 are INFERRED (they predict how a reader takes the text); the rest are Grounded.
- Mechanical check: all claims and each change's first line occur in `refactor-plan.md` after the M-to-F rename. All six `replacement_wording` entries match the plan line by line after removing the Markdown `> ` markers.

### Contradiction rescan (merged card vs plan)

- Pins vs applied text: every Task 4 and Task 5 pin (`write`/`writes no nested directory and no nested contract`, `` only by a `/sc:analyze` call ``) occurs in the matching Task 1, 2 or 3 applied text. `Quality-tier tracking` does not occur in the Task 1 text, and SKILL:196 is a blank line, so the F-4 paragraph slice excludes SKILL:197.
- The F-7 AC phrases (`only for a nested command that actually ran`, `7.2 step 4`, `lc10`, `` a `source: codebase` entry ``, `` neither `quality_tier` nor `source` records ``) all occur in the companion or live-check sentence.
- F-8's "plus 2" matches the two Task 5 pins under F-3.
- F-13 says Task 7 "writes only the logs under `./artifacts/`", and F-2 adds `status-after.txt` there. That file is also a log, so there is no conflict, but Task 7 now writes four files, not three.
- The Task 2 bullet names `quality_tier` as what is recorded, not as what decides the folder. That is consistent with the Tasks 1-3 rule.
- Result: no NEW contradiction found against the plan.

## Summary

- Planned changes: 12. Applied: 12. Skipped: 0. Failed: 0.
- Plan findings carried: 18 of 18 (none added, none dropped).
- Escalations: 1. F-18's priority is `OPEN` per the plan, not P0-P2.
- Merge status: partial. The diff-point convergence is complete, but INV-020 keeps the invariant gate BLOCKED_BY_INVARIANTS until the owner accepts it as a risk or a P2 plan addresses it.
