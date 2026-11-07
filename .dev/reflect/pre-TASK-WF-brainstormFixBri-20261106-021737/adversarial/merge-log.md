# Merge Execution Log

## Metadata
- Base: Variant 1 (sonnet:analyzer, reviewer-1 card), combined score 0.829 (`base-selection.md`)
- Executor: merge-executor agent
- Plan executed: `refactor-plan.md` (14 planned changes, 16 findings M-01..M-16, 5 confirmations OK-1..OK-5)
- Changes applied: 14 of 14 planned
- Status: partial (merge complete; 3 conflicts unresolved in the debate, INV-019 open in the plan)
- Merged output: `merged-verdict.yaml` (one YAML document)
- Convergence: 0.885
- Timestamp: 2026-11-06T04:19Z

The merged artifact is a consolidated verdict card, not a prose document. "Applied" means the change is in `merged-verdict.yaml`. No priority was re-decided; priorities, tags, evidence refs and wording are copied from `refactor-plan.md`. Neither the brief nor the plan was edited.

## Changes Applied

| Change | Finding id(s) | Source variant | What was taken | Status |
|---|---|---|---|---|
| 1 | M-02 | V3 R3-1 into base V1 A-2 | Grounded evidence (`analyze.md:97-98`, `WORKER-CONTRACT.md:32`, `SKILL.md:388`); tag "Grounded conflict, INFERRED failure"; V1's P2 and timeout trigger kept; V3's remedy dropped | Applied |
| 2 | M-01 | Orchestrator, `invariant-probe.md` INV-019 | New P1 at the top of the list, tagged INFERRED, with the P1 rationale and the fix pointing at the wording fix | Applied |
| 3 | `recommended_wording_fix` (parts A-D), referenced by M-01..M-05 | V1 advocate R2, V2 advocate R2 (a), V3 advocate R2, probe INV-011/012/015/019 | Amended Part 4 live-check sentence verbatim, Task 1 tail decision (no change), residual-risk texts, plan-line table, fallback if the owner declines | Applied |
| 4 | M-04 | V3 R3-6 + probe INV-013 | Residual-risk list rewrites (risk 2, risk 3 append, new risk 5) | Applied |
| 5 | M-05 | Probe INV-005 (+ V2, V3 advocate R2 points) | Pin `` invokes `sc:analyze` `` for brief:109 and plan:143 | Applied |
| 6 | M-07 | V2 R2-1 | F-16 Constraints line restored to the brief's literal line, P3; replaces base dispute 4 | Applied |
| 7 | M-08 | V2 R2-2 merged with V1 A-4 | F-13 sentence rewrite recording the `status-after.txt` widening and the `make sync-dev` writes | Applied |
| 8 | M-12 | V3 R3-3 | `--report-dir` contract split as a P3 owner note | Applied |
| 9 | M-13 | V3 R3-4 | Companion sentence vs installed twin, owner note | Applied |
| 10 | M-14 | V3 R3-5 | Routing bullet vs `skipped` on timeout, owner note | Applied |
| 11 | M-15 | V2 R2-5 | Coverage-matrix gap, review-artifact note | Applied |
| 12 | OK-3 | V3 R3-8 merged with V1 A-7 | Part 4 byte-for-byte confirmation (plan:38,54,69,122,128 = brief:229,230,231,221,217) | Applied |
| 13 | M-11, M-16 | Probe INV-002, INV-020 | M-11 AC guard clause for plan:44; M-16 owner note | Applied |
| 14 | M-06, M-09, M-10, OK-1, dispute 4 removal | V1 (own concessions) | A-1 narrowed to M-06; A-3 format-check part only as M-09; A-6 as M-10; A-5 as OK-1 with the explicit `git --no-optional-locks status --porcelain -- .dev/tasks/to-do` command; dispute 4 removed | Applied |

Confirmations OK-2 (C-011) and OK-4 (INV-007), OK-5 (INV-010) are carried from the plan's confirmation list without a numbered change.

## Final finding list by priority

| Priority | Count | Ids |
|---|---|---|
| P1 | 1 | M-01 |
| P2 | 4 | M-02, M-03, M-04, M-05 |
| P3 | 11 | M-06, M-07, M-08, M-09, M-10, M-11, M-12, M-13, M-14, M-15, M-16 |
| Confirmations | 5 | OK-1..OK-5 |

## Changes Not Made

All 14 rows of the plan's "Changes NOT Being Made" table are copied into `changes_not_made` in the merged file: C-001 / R3-1 remedy; C-001 / X-001 severity; C-001 option (b); V1 parenthesis + V3 Edit 2; C-002 / X-003 severity; C-004 / R3-2; C-004 / R2-3 and Tier 1 card R-2; C-011 / R3-7; C-006 exit-code half; C-005 Task 5 half; C-007 qualifier; C-008 twin edit; C-009 routing wording; INV-017, INV-020, INV-021.

## Unresolved conflicts and open invariants

- C-002 (split 50%): V2 right on recording, V1 right on severity. Carried as M-07 (P3).
- C-007 (split 50%): real fragility, note-level because conforming briefs pass `--output`. Carried as M-12 (P3 note).
- X-003 (split 50%): V1 on severity, V2 on recording. Carried with C-002 as M-07.
- INV-019 (HIGH): addressed in the recommendation, OPEN in the plan until the owner amends brief Part 4 and plan:128 mirrors it.
- Accepted-open (owner): INV-017, INV-020, INV-021. Open in the plan until edited: INV-002, INV-005, INV-011, INV-013.

## Post-Merge Validation

### Structural Integrity
- YAML hierarchy: one document; top-level keys are `merge_method`, `base_variant`, `sources`, `convergence_score`, `status`, `failure_stage`, `unresolved_conflicts`, `unaddressed_invariants`, `findings`, `confirmations`, `recommended_wording_fix`, `invariant_disposition`, `changes_not_made`, `provenance`, plus header keys. Parse result is recorded in the final report of this run (`uv run python` check).
- Finding order: P1, then P2, then P3, then confirmations, as in the plan.

### Required-field check
- Every M-id (M-01..M-16) has `priority`, `tag`, `claim`, `evidence`, `source_variants`, `file`, `exact_change`, `verifier` and `provenance`: PASS (16 of 16).
- `replacement_wording` is present where the refactor plan gives one: M-01, M-02, M-03 (pointer to part A), M-04, M-05, M-07, M-08, M-10, M-11. M-06 and M-09 give an exact change and no separate wording block in the plan, so the field is omitted there. M-12..M-16 are notes with no wording.
- Evidence refs were copied only from `refactor-plan.md`, the reviewer cards and `invariant-probe.md`; none were invented. Short names such as `SKILL.md:183` and `analyze.md:97` are kept exactly as the plan writes them.

### Invariants
- `invariant_disposition` has 22 rows: the plan's 8 table rows (INV-002, 005, 011, 013, 017, 019, 020, 021) copied as written, plus 14 rows for the remaining probe invariants (INV-001, 003, 004, 006, 007, 008, 009, 010, 012, 014, 015, 016, 018, 022). The plan's table lists only the 8 that the probe marked UNADDRESSED; the other 14 are marked ADDRESSED in `invariant-probe.md` and get severity, category and status from the probe with no new disposition text. No INV row from the probe is missing.

### Contradiction Re-Scan
No contradiction between findings. Items found that the owner should know:
1. Miscount in the plan overview: "Planned changes: 14 (12 incorporations, 1 orchestrator insertion group, 1 base-internal correction group)". The change list holds 11 incorporations (Changes 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), 2 orchestrator insertions (Changes 2, 13) and 1 base-internal group (Change 14). The total of 14 is right; the breakdown is not. No effect on any finding.
2. Wording tension, not a contradiction: the verdict says the plan is not ready for `/sc:implement`, while M-01 says no AC reads the live-check sentence so the executor cannot stop on it. Resolved in the merged file by `readiness_gate_kind`: the gate is an owner gate on the recommendation.
3. Open tension tied to the unresolved X-003 / C-002: M-07 restores the brief's wording "commits and merges" and calls it true under spec:282, while the debate transcript (Round 1 advocate 1) called the brief's wording the weaker one because spec:282 asks only for a commit to a branch. The plan decides this at P3 and the conflict stays listed as unresolved. No finding depends on which wording is "more correct".
4. M-04 is P2 although its parent Change 4 is rated Low risk. Not a conflict: finding priority (needs fixing with the P1) and merge-change risk (cost of getting the merge wrong) are different scales.

### Internal References
- Verifier strings for M-01..M-05 were checked against the amended sentence in `recommended_wording_fix`: it contains `a `Skill` tool call (not a `Task` or `Agent` call`, `invokes `sc:analyze``, `must then hold its own `return-contract.yaml` with every `artifacts` entry under it existing` and `every `nested/analyze-<n>/return-contract.yaml` that exists is listed in `artifacts``, and does not contain `a `Skill`, `Agent` or `Task` tool call`. `invokes `sc:analyze`` occurs once in it. All resolve.
- Part D plan-line table references M-01..M-05 only, all of which exist.

## Summary
- Total changes planned: 14
- Successfully applied: 14
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS (with the notes above)
