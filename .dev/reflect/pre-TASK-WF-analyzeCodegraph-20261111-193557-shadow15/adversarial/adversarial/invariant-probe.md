# Invariant Probe Results — Round 2.5 Fault-Finder Analysis

Probed consensus: the Round 2 merged-finding set (survivors: V1-F1, V1-F3, V2-F2-residue, V2-F3, V2-F4, V3-F1, V3-F3-reduced; refutations: V1-F2, V2-F1-matrix-clause, V2-F2-return-contract-clause, V3-F2). No "fix X greens test Y" claim is in play; category 6 ran in its generic sufficiency form over the findings' own claims.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | The tasklist and spec are frozen artifacts (archived under .dev/tasks/done/, execution commit 7764bb623) — later PRs cannot have changed the evidence for plan-text findings | ADDRESSED | LOW | Both files Read this session; git history shows no commits touching the archived package after 7764bb623 |
| INV-002 | guard_conditions | Dropping V2-F2's return-contract clause is safe because Task 2 AC2's byte-identity check transitively gates it | ADDRESSED | MEDIUM | Tasklist Task 2 AC2 requires `## Unattended mode` byte-identical to HEAD; the return-contract wording (analyze.md:112) sits inside that section — verified by Read |
| INV-003 | count_divergence | The 25-line-cap finding is measured on the right object (section `## Codegraph (optional)` line count, not file line count) | ADDRESSED | LOW | Section spans analyze.md:61-70 (~10 lines) at both HEAD and 7764bb623; spec cap is "under about 25 lines" (source.md:63) |
| INV-004 | collection_boundaries | V2-F3's "the test set is unnamed" — the referent collection for Task 3's pytest AC is actually defined | ADDRESSED | MEDIUM | Task 3 body defines the discovery procedure (`grep -rn 'commands' tests`, naming tests/unit/test_cli_install.py); the escape clause, not the set definition, is the defect — claim re-scoped in merged card |
| INV-005 | interaction_effects | Adding an access:mcp AC (V1-F3) would not be excused by Task 3's escape clauses in practice — the two surviving findings do not undermine each other | ADDRESSED | MEDIUM | Round 2, V2 advocate rebuttal: escape clauses (V2-F3) apply to test outcomes, not to grep-able AC text; noted in merged card as one observation, not a new finding |
| INV-006 | sufficiency_challenge | For each surviving "no AC gates X" finding, the cited tasklist text actually shows absence of a gate (not merely absence of the exact string) | ADDRESSED | HIGH | Spot re-verification of Task 1/2/3 AC blocks against each surviving claim: R7 symbolsOnly ban (absent from AC greps), access:mcp (absent), 25-line (absent), leads-not-citations/subagent-handoff (absent from ACs, present in Task 1 body) — all confirmed; refuted findings each carry git or t1-card evidence as falsifier |

## Summary

- **Total findings**: 6
- **ADDRESSED**: 6
- **UNADDRESSED**: 0
  - HIGH: 0
  - MEDIUM: 0
  - LOW: 0

Invariant probe gate: passes (no HIGH-severity UNADDRESSED items). Convergence is not blocked.
