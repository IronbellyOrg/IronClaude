# Base Selection

Variants: V1 = option-a (A), V2 = option-b (B), V3 = option-c (C). The scores below rate the original option files as written, not the positions the advocates reached after the debate.

## Quantitative Scoring (50% weight)

Source requirements, used for RC: R1 `update.sh` `set -e` (context c1); R2 exit aggregation (c2); R3 Coder offline run and 60 s bound (c3); R4 doctor exit and `make verify` (c4); R5 removal path after Phase 1 deletes the flag (c5); R6 safety rules (c6); R7 smallest code (c7); R8 daemon holds the old dir for 300 s (c8); R9 installed by default (README line 13); R10 fresh Coder workspace ends with codegraph.

| Metric | Weight | V1 (A) | V2 (B) | V3 (C) | Notes |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 0.90 | 0.90 | 1.00 | A and B never address R8; only C has an old-version-dir rule |
| Internal consistency (IC) | 0.25 | 0.93 | 1.00 | 1.00 | A's "red twice" (option-a.md:20) contradicts its own c1 dependency (`set -e` stops before doctor); 1 of about 14 claims |
| Specificity ratio (SR) | 0.15 | 0.94 | 0.87 | 0.94 | B: "silently", "may run for weeks" |
| Dependency completeness (DC) | 0.15 | 1.00 | 1.00 | 1.00 | All internal refs resolve to context.md or source |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 1.00 | 4 H2 sections each |
| **quant_score** | | **0.944** | **0.951** | **0.991** | |

## Qualitative Scoring (50% weight): Additive Binary Rubric (CEV, summarized)

| Dimension | V1 (A) | V2 (B) | V3 (C) | Key evidence |
|---|---|---|---|---|
| Completeness | 4/5 | 3/5 | 5/5 | Requirement coverage: only C (old-dir rule, R8). Success criterion: A ("green update.sh = working codegraph"), C (exit code proves it); B has none. Edge cases, dependencies, out of scope: all three |
| Correctness | 3/5 | 5/5 | 3/5 | A: "red twice" is factually wrong and inconsistent. C: "breaks every Claude session" is overstated (one server fails), and the `~/.codegraph/daemons/` per-version lookup is unverified and may not be feasible. B: no false claims; its weaknesses are stated honestly |
| Structure | 5/5 | 5/5 | 5/5 | Same template; ordering and cross-references to context.md |
| Clarity | 4/5 | 4/5 | 4/5 | None defines MCP or the receipt on first use; all three are otherwise concrete and actionable |
| Risk coverage | 3/5 | 3/5 | 3/5 | None gives probability or impact, or a mitigation for each risk; all cover failure and recovery, external dependencies (network, Coder) and a validation mechanism (doctor) |
| Invariant and edge-case coverage | 3/5 | 3/5 | 4/5 | C covers multiple version dirs (collection boundary) and daemon versus dir state; all three note interaction with Coder CI and doctor; none covers count divergence |
| **Total** | **22/30 = 0.733** | **23/30 = 0.767** | **24/30 = 0.800** | |

Edge-case floor (at least 1/5): all three are eligible.

## Position-Bias Mitigation
- Pass 1 order V1, V2, V3; pass 2 order V3, V2, V1.
- The passes disagreed on 2 criterion-variant pairs:
  - V2 Correctness-1: pass 2 questioned B's "ordering with the Coder bake is forgiving". Re-evaluation found that B's literal claim, "never breaks `./update.sh` or the Coder slug", is true; the test-57 failure is a Coder-side test, which B listed as a weakness. Result: MET.
  - V3 Correctness-2 (feasibility): pass 2 leaned MET because the baseline "keep previous dir" rule exists. Re-evaluation: the option as written depends on the unverified `daemons/` lookup. Result: NOT MET.
- Verdicts changed by re-evaluation: 0.

## Combined Scoring

| Variant | Quant × 0.5 | Qual × 0.5 | Score |
|---|---|---|---|
| V3 (C) | 0.496 | 0.400 | **0.896** |
| V2 (B) | 0.476 | 0.383 | 0.859 |
| V1 (A) | 0.472 | 0.367 | 0.839 |

The margin between V3 and V2 is 0.037, which is under 0.05, so the tiebreaker applies.
- Level 1, debate performance: V3 won 18 of 18 points (C-001, C-006 and C-009 are shared with V1); V2 won 0 and V1 won 0 outright. **V3 is selected at level 1.**

## Selected Base: Variant 3 (option-c, original)

**Rationale.** C puts the one hard gate on the install exit code, which both `update.sh:2,8` and Coder's exit-0 contract already check. In the debate both other advocates converged on it: V1 conceded the uninstall CLI and the strict doctor, and V2 withdrew the ordering advantage once test-57 had to assert the registration under `--network=none`.

**Strengths to preserve:** required phase; doctor fails only on a dangling registered command; receipt-gated removal with no CLI flag; the `--list` ownership view.

**Strengths to incorporate:**
- From V2: U-004 (stderr names the exact recovery command); a missing entry is reported, not failed; minimal-code pushback (no keep-aside copy, no timing machinery, no separate platform table).
- From V1: prompt-hook leftover reporting (survives the additive hook merge); receipt-based ownership that also scopes the owned-entry test (folded into A-001 and INV-005).
- From the debate and the probe: the A-001 owned-entry test, the A-002 receipt list, the INV-001 reference-based deletion rule, and INV-003, 004, 005, 006, 007, 008, 011, 012 and 014.

**Weaknesses to fix in the base:** the `daemons/` lookup (replace it); the "breaks every session" rationale (downgrade it); the size estimate (raise it); the receipt as a single entry (change it to a list).
