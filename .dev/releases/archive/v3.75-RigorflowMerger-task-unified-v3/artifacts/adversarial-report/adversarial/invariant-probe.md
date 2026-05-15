# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder probes the emerging consensus (synthesis merge: A's evidence backbone + B's decision instruments) against the five invariant categories. The consensus is a documentation merge; invariant categories map to documentation-integrity assertions.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The candidate ID space is consistent (TU-### task-side, SE-### sprint-side) and B's B-### IDs map 1:1 to A's TU-/SE- IDs | ADDRESSED | LOW | Cross-walk confirmed: B1↔TU-001, B2↔TU-002, B3↔TU-003+TU-003 anti-sycophancy, B4↔universal anti-sycophancy slice of TU-003, B5↔TU-004, B6↔mandatory completion checklist (A §6.1 unnamed), B7↔SE-005, B12↔SE-002, B13↔SE-003, B14↔SE-004, B15↔SE-001, B16↔A §7 RK-10 (TurnLedger persistence, A out of scope), B17↔SE-006, B18↔SE-005 enum. Merged artifact must preserve both ID schemes for traceability. |
| INV-002 | guard_conditions | The merge preserves A's `[inference]` discipline as a guard against uncited synthesis claims (effort labels, owner assignments, Sev field) | ADDRESSED | MEDIUM | Refactor plan applies `[inference]` to all B-origin synthesis fields (S/M/L labels, Owner column, Sev field). Without this guard, the merged artifact would project unearned certainty. |
| INV-003 | count_divergence | Risk register count after merge: A has 20 rows, B has 12; merge retains 14 rows (B's 12 + A-only RK-19, RK-20). Confirm no off-by-one in row IDs | ADDRESSED | LOW | Refactor plan renumbers merged risks as R-1..R-14. A's RK-13, RK-14, RK-18 move to Appendix (out-of-scope retained for traceability). No row duplication. |
| INV-004 | collection_boundaries | Overlap matrix has empty-row edge case: B's 21-row matrix is subset of A's 47-row matrix. Confirm merge does not drop a row from the union | ADDRESSED | MEDIUM | Refactor plan retains A's full 47-row matrix (§5) and supplements with B's decision-needed column where applicable. Empty case (rows in B that are not in A) checked: 0 such rows — B's matrix is a proper subset of A's by topic. |
| INV-005 | collection_boundaries | Open-question count after merge: A has 14 (Q1-Q14), B has 10. Merge retains all 14 from A and overlays B's Blocking? + Options + Recommendation columns. Confirm no question dropped | ADDRESSED | MEDIUM | Refactor plan: A's Q1+Q2 preserved separately (per debate C-007 resolution); B's Q3 maps to A's Q1+Q2 with shared recommendation. Total in merged: 14 questions retained, 4 flagged Blocking (per B's commitment). |
| INV-006 | interaction_effects | Synthetic shared assumptions A-001..A-005 (promoted from agreement points) must appear in merged artifact, not silently dropped | ADDRESSED | MEDIUM | Refactor plan adds new §10 "Shared assumptions surfaced during adversarial review" capturing A-001..A-005 with classification (UNSTATED) and impact. This is novel content the synthesis surfaces; both source drafts implicit. |
| INV-007 | interaction_effects | Naming-artifact decision X-001 + Q1/Q2/Q3 (sentinel + caller string + skip-compliance interaction with BLOCKED) — three changes that interact. Confirm merged artifact handles all three consistently | ADDRESSED | HIGH→reduced to MEDIUM | Three interactions, all resolved by debate: (a) sentinel rename DEFER to dedicated cleanup release (B11/Q3); (b) caller string DEFER (same release); (c) `--skip-compliance` + BLOCKED → `yes with --reason`, audit-logged (Q6 / R-12 mitigation). Refactor plan documents all three as a coupled set in §8. Originally HIGH because three coupled decisions; reduced to MEDIUM because all three reach a single consistent recommendation. |
| INV-008 | guard_conditions | The merged FINAL-REPORT.md must not itself contain `/sc:task-unified` strings except documented carry-over artifacts (§9.1 + §9.4 of A) | ADDRESSED | HIGH | Refactor plan: merge preserves the documented carry-overs (sentinel `SC:TASK-UNIFIED:CLASSIFICATION`, `--caller task-unified`) and adds a sentence noting these are preserved per v3.7 N1-N12. CI grep `grep -nE "/sc:task-unified" FINAL-REPORT.md` should match only the documented carry-overs. |
| INV-009 | count_divergence | Effort total: B does not aggregate. Merged artifact should sum approximate days for ADOPT'd candidates to give release sizing | ADDRESSED | LOW | Refactor plan §6 adds a one-line "Total effort if all ADOPT'd land: ~5-10 dev-days (sum of S+M effort labels)" inferred summary, tagged `[inference]`. |
| INV-010 | state_variables | The merged artifact's "selected base" provenance — readers must be able to determine why A was chosen as base, not B | ADDRESSED | LOW | base-selection.md documents the choice. Merged artifact's preamble explicitly attributes "Synthesized from Draft A (completeness/traceability base) overlaid with Draft B (decision instruments)". |

## Summary

- **Total findings**: 10
- **ADDRESSED**: 10
- **UNADDRESSED**: 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0

**Convergence gate decision:** 0 HIGH UNADDRESSED → invariant probe DOES NOT BLOCK convergence.
