# Merge Execution Log: merged reviewer verdict (sc:adversarial step 5, Mode A, depth standard, sc:reflect UC-1 run 4)

## Metadata

- Base: Variant 2 (reviewer 2, qa; recorded model gpt-6.1-sol in the haiku-class slot; calibrated C 0.86), `variant-2-original.md`.
- Executor: merge-executor (steps 3 to 5 in one agent). It applied `refactor-plan.md` and made no change of severity or scope relative to `debate/consensus.md`.
- Plan: `refactor-plan.md`, 11 changes, auto-approved.
- Output: `merged-verdict.yaml` (schema `sc-reflect-merged-verdict/v1`, 664 lines).
- Changes applied: 11 of 11. Failed: 0. Skipped: 0.
- Status: success for the merge itself; the pipeline result is partial because convergence is BLOCKED_BY_INVARIANTS (see `return-contract.yaml`).
- Timestamp: 2026-11-10 (date only).
- Files written by this agent: `base-selection.md`, `scores.json`, `refactor-plan.md`, `merged-verdict.yaml`, `merge-log.md`, `return-contract.yaml`, all in this folder. Two throw-away scripts lived in `/tmp/adv-r4-score/` (scoring and quote check), outside the repository. No other file was changed: not the task file, DESIGN, the addendum, either revision request, the ledger or any source.
- Aliases: as in the `path_aliases` block of the YAML (TL, BASE, DESIGN, ADD, DM, BR, STYLE, OQ6, CM, SK, MV3).

## Changes Applied

| Change | Status | Before (base or source) | After (merged) | Provenance tag |
|---|---|---|---|---|
| 1 | applied | V2 R2-F1: claim "cannot satisfy its literal completion checks", fix "Split 7.17 Verification ... needs a bounded authorization extension" | M-01, HIGH-conditional, outside the 85; claim rewritten from CONS 4.2 (resume trace via TL:195 and SK:535), O-001 folded; fix adds skip-if-exists (INV-R4-005), both outcomes (INV-R4-004), one line (INV-R4-006) and the missing follow-up items (INV-R4-003); 19 evidence refs | Source: Base (original, modified) R2-F1; CONS M-01; diff-analysis O-001; PROBE |
| 2 | applied | V2 R2-F2: fix "Make 7.24 check the approved post-7.17 allowlist ... Apply the same qualification to the reused R5 review inputs" | M-02, HIGH-conditional, inside the 85, owner acceptance by name; fix names all three TL:1321 checks (INV-R4-011), approval from the RESOLVED OQ record (INV-R4-009), R5 sub-fix dropped (INV-R4-012); 17 refs | Source: Base (original, modified) R2-F2; CONS M-02 and 4.1; PROBE |
| 3 | applied | not in base | M-03, MEDIUM, inside the 85; fix from V1 plus no re-record on resume (INV-R4-015), Then spawn order and FAIL branch (T1 L1), 14.x parity for owner acceptance (INV-R4-019, T1 L5); 14 refs | Source: Variant 1 R1-F3 per Change 3 |
| 4 | applied | not in base | M-04, LOW, inside; section-hash idea replaced by the 7.20 read-and-match re-run (INV-R4-020); 4 refs | Source: Variant 1 R1-F4 per Change 4 |
| 5 | applied | not in base | M-05, LOW, inside; qualifier only where absent (INV-R4-021), before excerpts from the original start (INV-R4-022); 7 refs | Source: Variant 1 R1-F2 per Change 5 |
| 6 | applied | not in base | M-06, LOW, inside, owner acceptance by name for the two clauses; INV-R4-025 settled by reading BR:27, ADD:19 and MV3:180; 9 refs | Source: Variant 1 R1-F5 per Change 6 |
| 7 | applied | not in base | M-07, LOW, 7.20 inside, root cause BR:9 outside; V1 owner-file fix not carried (INV-R4-027); optional re-supply clause (INV-R4-026); 11 refs | Source: Variant 1 R1-F1 per Change 7 |
| 8 | applied | not in base | M-08, LOW, inside, owner acceptance by name; separate baseline file (INV-R4-028); frozen-hash option not carried; 7 refs | Source: Variant 3 R3-F3 per Change 8 |
| 9 | applied | not in base | M-09, LOW, outside; cite by quoted sentence (INV-R4-030); executor observation on the DESIGN 971/973 shorthand added as a note; 10 refs | Source: diff-analysis O-002 per Change 9 |
| 10 | applied | none | header comments; `convergence_score` 0.935 with the strict 0.774 and cross-check 0.941 in `convergence_detail`; `convergence_status: BLOCKED_BY_INVARIANTS`; invariant blocks: high 2 (INV-R4-003, 011), medium 4 (009, 012, 015, 026), low 7 (006, 019, 020, 021, 022, 025, 030), addressed 19; 32 in all, matching the probe | Source: CONS section 5; PROBE sections 2 to 4 |
| 11 | applied | none | `f_closure` (8 fixed, 2 partial: F-01, F-07; 13 refs), `tier1_verdicts` (L1, L2, L3, L5, L6, L8 carried; L4, L7, L9 dropped to residual notes), `not_carried` (14), `departures_from_consensus` (none on severity or scope; 6 fix-wording refinements from the probe), `row_coverage` (127 of 127; union 0.99; unmapped INF-017, INF-A29; INF-A06 and INF-A08 covered; 10 refs), `consequence_note` (2 refs), `residual_notes` (5 items, 9 refs), `best_practice_grade` 4, `confidence_calibrated` 0.80, `verdict_recommendation` | Source: cards, CONS, PROBE, T1, coverage matrix |

## Post-Merge Validation

### YAML loads

`uv run --no-project --with pyyaml python -I -c 'import yaml,sys;yaml.safe_load(open(sys.argv[1]))' merged-verdict.yaml` loads without error (run after the last edit).

### Evidence quotes (mechanical)

- Script `/tmp/adv-r4-score/check_quotes.py` loads the YAML, walks every `{ref, quote}` pair anywhere in the document, resolves the alias from `path_aliases` (relative to `worktree_root`, or absolute for SK), slices the cited line or range, and tests that the quote is a verbatim substring.
- Result after the last edit: 132 quotes checked, 132 matched, 0 mismatched. Breakdown: findings 98 (M-01 19, M-02 17, M-03 14, M-04 4, M-05 7, M-06 9, M-07 11, M-08 7, M-09 10), f_closure 13, row_coverage 10, residual_notes 9, consequence_evidence 2.
- Line-identity checks against BASE, run in this step, back the "pre-existing" labels: TL lines 1266, 1267, 1270, 1271, 1272, 1274, 1275, 1321, 2384 and 2412 have the same line hash in BASE and TL.
- Count claims inside verifiers were re-run on TL in this step: `Execution authorization (verbatim)` 3 lines; `DESIGN line 55[02]` 3; `Pre-7.10 source anchor` 58; `not an implemented exception` 1; `fabricated successful summary`, `reconstruct role`, `advice prohibited by the sweep skill`, `re-supply`, `sha256-before` 0 each; `sha256sum` on lines 1363, 1391, 2614, 2642, 2705, 2733; `DESIGN edit item` on 1268 and 1271.

### Structural integrity

- Every finding has the fields id, severity, gap_class, tag, location, claim, affected_items, evidence, recommendation {fix, verifier}, authorization, provenance, notes; the HIGH findings also carry severity_condition.
- `severity_counts` (HIGH 2, MEDIUM 1, LOW 6, total 9) equals a count of the findings (checked by the script). `authorization_counts` (inside 7, outside 2) equals the authorization fields (outside: M-01, M-09).
- Every finding severity, condition and scope equals CONS section 1; the departures block says so and lists only fix-wording refinements.

### Internal references

- Every `carried_in` of the invariant blocks names an existing finding; every `as` of `tier1_verdicts` names an existing finding; every `change` in provenance names a change in `refactor-plan.md`. Broken: 0.

### Contradiction re-scan

None found. Checked pairs:
- M-03 and M-08: both propose a separate orchestrator-owned baseline file; M-08 says so explicitly to avoid copying M-03.
- M-04 and M-05: both touch the authorization section; M-04 adds a re-check in 7.30/7.34, M-05 a resume rule in 7.10; no overlap in lines.
- M-05 and the invariant G5 (no 7.20 command change): the M-05 fix states the occurrence-count option is not proposed for that reason.
- M-01 and M-02: M-02 puts the 7.24 slot on the 7.17 follow-up list only through the M-01 extension, consistent with 7.17 being outside the 85.
- f_closure F-01 partial and M-01/M-02 pre-existing: the F-01 note separates the as-scoped fix from the branch defects.
- `convergence_status` BLOCKED_BY_INVARIANTS and `convergence_score` 0.935: the header comment explains the gate.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 11 | 11 | 0 | 0 |

- Post-merge validation: PASS (YAML loads; 132 of 132 quotes match; counts consistent; no broken internal reference; no new contradiction).
- Not done: no fix was applied to any plan or source file, by design. No independent second judge ran the qualitative rubric (both passes were mine; see `base-selection.md`). The two scripts in `/tmp/adv-r4-score/` are not kept in the repository; their method is described in `base-selection.md` and this log.
