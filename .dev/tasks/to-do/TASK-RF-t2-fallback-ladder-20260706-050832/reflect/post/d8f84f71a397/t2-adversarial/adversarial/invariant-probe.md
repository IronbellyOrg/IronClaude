# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Probes the emerging consensus (both reviews' "terminal gate incomplete → FAIL") against boundary conditions and the sufficiency challenge.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | Consensus assumes the POST reflect gate did not run, so a completion narrative is illegitimate self-certification | **UNADDRESSED** | **HIGH** | Neither review checks whether the audit *is itself* the POST gate. Path `reflect/post/d8f84f71a397/` + return-contract `recommended_next_command` = this `/sc:adversarial` call → the gate is executing. Consensus premise is false. *(Resolved by adjudicator context; mandates C1/X-002 downgrade.)* |
| INV-002 | state_variables | Consensus treats frontmatter `status: "🟠 Doing"` + unchecked L484/L486 as a defect | ADDRESSED | LOW | This is the correct pre-POST-gate state per Terminal-gate ordering (L476) and checklist order (L482 before L484). Not a defect. |
| INV-003 | sufficiency_challenge | glm C2 claims the verification round was skipped — is that claim ALONE sufficient to prove a process breach? | ADDRESSED | HIGH | Sufficiency demonstrated by enumeration: (a) 6.G9 consolidated = FAIL (L565), (b) 6.G10 applied real fixes (L566), (c) 6.G11 "IF fixes applied → spawn 2 verifiers writing the two named artifacts", (d) those artifacts are **absent** on disk while phases 1–5 all have theirs. The branch condition is met and the output is missing → breach confirmed, not merely asserted. |
| INV-004 | count_divergence | Test-file count: is the 6/7/8 spread a real inconsistency or a counting artifact? | ADDRESSED | MEDIUM | Real: §9=6, task-body/Glob-verify=7 (L123/L410/L436/L478), Task-Summary/Files-created=8 (L500/L501). `test_ensemble_fallback_engage.py` has no authorizing Step — genuine drift. |
| INV-005 | collection_boundaries | Only 1.5 of 3 reviewers usable (kimi 0-byte proxy_error; glm truncated). Does the ensemble that fed this comparison itself hold? | UNADDRESSED | MEDIUM | Neither review flags that its own producing ensemble was degraded (2/3 workers, one truncated-but-marked-success). Surfaced here as a merge caveat; not a task defect. |
| INV-006 | interaction_effects | Does glm's over-reach on C3 ("fabricated") interact with its truncation to inflate the overall FAIL? | ADDRESSED | LOW | Yes — truncated glm front-loads 3 CRITICALs (one over-reaching) with no MINOR ballast, biasing its verdict harder than the evidence supports. Merge re-balances. |

## Summary
- **Total findings:** 6
- **ADDRESSED:** 4
- **UNADDRESSED:** 2
  - HIGH: 1 (INV-001 — resolved by adjudicator runtime-context evidence; converts the headline from FAIL to MINOR reconciliation)
  - MEDIUM: 1 (INV-005 — degraded producing-ensemble caveat)
  - LOW: 0

**Gate effect:** INV-001 (HIGH UNADDRESSED) would normally BLOCK convergence. It is resolved by the adjudicator's filesystem/return-contract evidence rather than a further debate round, so it does not block the merge — but it is the mechanical reason the merged verdict downgrades both reviewers' CRITICAL/FAIL headline.
