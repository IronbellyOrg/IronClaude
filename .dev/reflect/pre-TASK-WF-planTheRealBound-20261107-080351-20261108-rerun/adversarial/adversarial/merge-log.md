# Merge Log

## Metadata

- Base: variant 2 (reviewer 2, qa persona, opus class), `variant-2-original.md`
- Executor: merge-executor (Step 5 of /sc:adversarial)
- Plan executed: `refactor-plan.md` (8 planned changes); content source of truth: `.work/merged-findings-spec.md`
- Output: `../merged-verdict.yaml` (merge_method: adversarial; findings M2-01..M2-14)
- Changes applied: 8 of 8
- Status: COMPLETE (one provenance discrepancy flagged for the orchestrator, see Change #7)
- Timestamp: 2026-11-08T02:20Z

## Changes Applied

### Change #1: severity scale HIGH/MEDIUM/LOW/INFO only

- Status: applied
- What changed in the output: every finding carries exactly one of MEDIUM, LOW or INFO (no HIGH remains). Variant 2's hedged labels (Q-5 and Q-6 "Low-Medium", N-2 "Medium-Low", N-13 "Info/Low") and variant 1's "Drift" category column were dropped. The spec's qualifiers that are not severities ("value risk" on M2-07, "opportunity" on M2-09, "list of small items" on M2-13) were moved out of the severity field into a parenthesised prefix of the claim, so the severity field holds only a scale value.
- Provenance tag: `<!-- Source: Variant 2 and Variant 1 severity labels, normalised per brief reviewer-briefs/reviewer-1.md:3 and S-002 - merged per Change #1 -->`

### Change #2: documentary basis for the budget finding

- Status: applied
- What changed in the output: M2-02 replaces base N-4's [INFERRED] budget claim with the archived help evidence (help:131-132, "only works with --print") and the owner choice (record the pty /clear case unavailable, or authorize a separately bounded interactive run with no --disable-slash-commands).
- Provenance tag: `<!-- Source: Variant 1 A-02, replacing Variant 2 N-4 - merged per Change #2 -->`

### Change #3: timeout self-check and runner-caused stop label

- Status: applied
- What changed in the output: M2-01 combines base N-3 and Q-6 (recorded-pid teardown, cwd escape) with A-01's self-check (time out a dependent run while the survivor lives) and the distinct label for a runner-caused stop.
- Provenance tag: `<!-- Source: Variant 1 A-01 appended to Variant 2 N-3 / Q-6 - merged per Change #3 -->`

### Change #4: narrowed A-03 with Q-1 and Q-7

- Status: applied
- What changed in the output: M2-03 states that the originating controller is not reused, and requires the controller identity before and after /clear together with Q-1's ordered calls and expected statuses and Q-7's expected fork status.
- Provenance tag: `<!-- Source: Variant 1 A-03 (narrowed) merged into Variant 2 Q-1 / Q-7 - merged per Change #4 -->`

### Change #5: redacted process-tree snapshot fields

- Status: applied
- What changed in the output: M2-04 adds the snapshot fields (pid, ppid, start identity, role) next to Q-3's "not run (budget)" label and Q-5's real governed Git push; N-8 and M-12 recorded as sources.
- Provenance tag: `<!-- Source: Variant 1 A-04 merged into Variant 2 Q-3 / Q-5 - merged per Change #5 -->`

### Change #6: reparenting assertion

- Status: applied
- What changed in the output: new finding M2-11 (LOW) requires the intermediate parent to exit, the PPID of the same live descendant to change, and the selector to be sampled afterwards while the supervisor lives.
- Provenance tag: `<!-- Source: Variant 1 A-05 (unique), new row - merged per Change #6 -->`

### Change #7: restated N-1

- Status: applied
- What changed in the output: M2-06 states that thirteen starts are not forced (plan:22) and recommends claude_run_id and claude_started; it records that this corrects the Tier 1 claim.
- Provenance tag: `<!-- Source: Variant 1 refutation of N-1, replacing Variant 2 N-1 - merged per Change #7 -->`
- Flag for the orchestrator (not changed): the spec lists the variant 1 source as "reviewer 1 A-02 refutation", and the YAML keeps `A-02` in source_findings as the spec says. In `variant-1-original.md` the N-1 refutation sits in the "Independent assessment of Tier 1" section (line 26), not in A-02's row (line 12). The fact is unaffected; only the pointer is loose.

### Change #8: restated coverage verdicts

- Status: applied
- What changed in the output: the `coverage` map gives INF-003 Partial (M2-03, M2-11); INF-001, INF-002, INF-008 covered with defects tracked as M2-01, M2-02, M2-04, M2-05; INF-005 controlled only (M2-09); INF-006 covered (lexical miss, with its citations); coverage_pct null, coverage_pct_union 1.0, coverage_degraded parsed-sparse.
- Provenance tag: `<!-- Source: Variant 2 coverage table, restated per X-002 / C-006 - merged per Change #8 -->`

Findings kept from the base without a planned change other than #1: M2-05 (Q-2, C-005), M2-07 (N-12), M2-08 (N-2), M2-09 (Q-4), M2-10 (N-5), M2-12 (N-7), M2-13 (N-6, N-9, N-10, N-11, N-13, Q-8), M2-14 (N-14). The four rejected alternatives in "Changes NOT Being Made" (S-001, S-003, C-005, X-002) were not applied.

## Post-Merge Validation

### Structural integrity

- YAML parses: PASS. `uv run python -I -c "import yaml,sys; ..."` printed `adversarial 14`.
- Top-level key order matches the requested order: merge_method, base_variant, convergence_status, convergence_score, convergence_note, calibrated_confidence, plan_verdict, findings, earlier_findings_disposition, coverage, limits: PASS.
- Finding ids M2-01..M2-14 contiguous: PASS. Duplicate ids: 0.
- Severities used: INFO, LOW, MEDIUM only: PASS.
- Disposition keys M-01..M-17 complete: PASS.

### Internal references

- Every `provenance.source_findings` entry matches a variant finding id (A-0N, Q-N, N-N or M-NN): PASS (0 unresolved). A-01..A-05 resolve to variant 1; Q-1..Q-8 and N-1..N-14 resolve to variant 2's findings table and Tier 1 disposition; M-07, M-12, M-15 resolve to the earlier run's merged verdict.
- Every M2- pointer in `earlier_findings_disposition` and `coverage` (M2-01, M2-02, M2-03, M2-04, M2-05, M2-06, M2-09, M2-11) resolves to a finding in the file: PASS.
- One loose pointer noted, not a broken reference: M2-06's `A-02` (see Change #7).

### Contradiction rescan

- No new contradiction found. Checked pairs: M2-01 (survivors exempt from timeout sweeps) with M2-08 (one run group per task) and M2-10 (minimum child lifetime) are consistent; M2-09 (release step before teardown) is consistent with M2-01's teardown; M2-02 (no --disable-slash-commands) and M2-13(b) (default tool set) point the same way; M2-06 does not contradict the earlier M-07, which it records as partly resolved.
- The M-02 / M-16 conflict is pre-existing and recorded as M2-01, not introduced by the merge.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 8 | 8 | 0 | 0 |
