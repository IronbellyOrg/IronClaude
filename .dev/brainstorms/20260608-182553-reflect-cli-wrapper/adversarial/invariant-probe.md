# Invariant Probe (Round 2.5)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|-----------|--------|----------|----------|
| INV-001 | sufficiency_challenge | "top-level launch greens the Tier-2 gate" | ADDRESSED | HIGH | Necessary-not-sufficient: also needs ≥2 aliases (FM-4) + MCP (FM-3) + child actually invoking skill. Merged FR-11 verifies tier_reached==2/t2_model_class_diversity==full/non-null adversarial/verification_ran before pass. |
| INV-002 | guard_conditions | child env actually carries MCP + ANTHROPIC_DEFAULT_* | ADDRESSED | HIGH | FR-10 real-env (NOT HomeIsolation) + FR-11 preflight alias count + degraded_components check |
| INV-003 | state_variables | frontmatter write races with concurrent session | ADDRESSED | MEDIUM | FR-6 compare-before-write; run from own worktree |
| INV-004 | interaction_effects | reflect `--output` collision suffix hides parsed contract | ADDRESSED | MEDIUM | FR-4 wrapper owns run-unique output dir; collision unreachable |
| INV-005 | collection_boundaries | empty/missing return-contract.yaml | ADDRESSED | MEDIUM | FR-5 → blocked/exit 2; never guess sibling |
| INV-006 | count_divergence | exit-code mapping vs verdict states | ADDRESSED | LOW | §6 table: 0=pass,10=halted,11=degraded,2=blocked |

## Summary: 6 findings, 6 ADDRESSED, 0 UNADDRESSED. No HIGH unaddressed → convergence not blocked.
