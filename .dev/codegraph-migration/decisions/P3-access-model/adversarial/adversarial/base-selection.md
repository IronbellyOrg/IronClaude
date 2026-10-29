# Base Selection Report

Variants: A = `option-a.md` (MCP-first), B = `option-b.md` (CLI-first, artifacts), C = `option-c.md` (hybrid). Source requirements: the six criteria in `context.md`.

## Quantitative Scoring (50% weight)

Counting rules, so a rerun gives the same numbers:
- **Claims** are top-level bullets in Proposal, Strengths and Weaknesses: A 13, B 15, C 12.
- **RC (requirement coverage)**: a criterion counts as matched when the variant states a position or behaviour for it.
- **IC (internal consistency)**: contradictions are intra-document only. External factual errors are scored under qualitative Correctness-1.
- **SR (specificity)**: a bullet counts as vague when it contains may, might, rarely, most, various or appropriate. Otherwise it counts as concrete when it names a number, command, tool, file or threshold.
- **DC (dependency completeness)**: internal references only. All three variants refer only to external files, so DC = 1.0 for each (no unresolved internal references).

| Metric | Weight | Variant A | Variant B | Variant C |
|--------|--------|-----------|-----------|-----------|
| requirement_coverage | 0.30 | 0.833 (5/6; no failure behaviour for criterion 6) | 1.000 (6/6) | 1.000 (6/6) |
| internal_consistency | 0.25 | 0.923 (1 contradiction, X-005, in 13 claims) | 1.000 (0 in 15) | 1.000 (0 in 12) |
| specificity_ratio | 0.15 | 0.923 (12 concrete / 1 vague: "may not get MCP tools") | 0.933 (14 / 1: "results may be stale") | 0.833 (10 / 2: "rarely need to call", "removes most of INV-001") |
| dependency_completeness | 0.15 | 1.000 (0 internal refs) | 1.000 | 1.000 |
| section_coverage | 0.15 | 1.000 (3/3 H2) | 1.000 (3/3) | 1.000 (3/3) |
| **quant_score** | | **0.919** | **0.990** | **0.975** |

## Qualitative Scoring (50% weight): Additive Binary Rubric

Two independent evaluators ran the rubric with Claim-Evidence-Verdict: Pass 1 in input order (A, B, C) and Pass 2 in reverse (C, B, A). The tables below give the final verdict per criterion. Where the passes disagreed, the orchestrator re-evaluated the criterion (see Position-Bias Mitigation).

### Completeness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|-----------|---|----------|---|----------|---|----------|
| Covers all source requirements | NOT MET | No behaviour when codegraph or the index is missing | NOT MET | No main-session access path | MET | Covers main/orchestrators, agents, allowlists, fallback "exactly like 'codegraph absent'" |
| Edge cases/failures | MET | "Background subagents may not get MCP tools"; nested-worktree warning | MET | Five-state probe; "stale results are leads only" | MET | "If that is not done, primitives fall back to Grep/Read" |
| Dependencies/prerequisites | MET | "Depends on a Phase 2 change" | MET | "No Phase 2 dependency"; cites BR §2.1 | MET | "depends on the one-line Phase 2 env change"; smoke test |
| Success criteria | NOT MET | none | NOT MET | none | NOT MET | none |
| Out of scope | NOT MET | none | MET | "No `CODEGRAPH_MCP_TOOLS` in v1"; MCP stage deferred | NOT MET | none |
| **Subtotal** | **2/5** | | **3/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|-----------|---|----------|---|----------|---|----------|
| No factual errors | NOT MET | "direct 1:1 replacement": `find_symbol` is Partial (EVAL §6.2) | NOT MET | "No always-loaded schema cost": explore listed with `alwaysLoad` (EVAL §3) | NOT MET | "removes most of INV-001": the daemon is session-owned (BR §2.1, EVAL §5.7) |
| Feasible | MET | One env line plus a name swap | MET | Existing subcommands; `query --json` documented | MET | Env line plus exact subcommands, with a fallback |
| Terminology | MET | Consistent `mcp__codegraph__codegraph_*` | MET | Consistent state vocabulary | MET | MCP vs CLI `status` kept distinct |
| No internal contradictions | NOT MET | "no allowlist patterns" vs `Bash(codegraph affected *)` | MET | Re-evaluated: the conflict needs an external fact and is already scored under factual errors | MET | none found |
| Claims supported | MET | Cites EVAL §3, §4 | MET | Cites BR §2.1, FR-04, FR-11, D-28, INV-001 | NOT MET | Re-evaluated: no EVAL citation for any number; INV-001 claim unsupported |
| **Subtotal** | **3/5** | | **4/5** | | **3/5** | |

### Structure (5 criteria)

All five are MET for every variant: Proposal → Strengths → Weaknesses order, uniform H1/H2/bullets, clean separation, a pointer to `context.md`, and the decision-option format. **A 5/5, B 5/5, C 5/5.**

### Clarity (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|-----------|---|----------|---|----------|---|----------|
| Unambiguous | MET | Re-evaluated: "may" states a documented unknown | MET | Re-evaluated: "about 300 ms" is quantified; "may be stale" is a measured unknown | NOT MET | "rarely need to call"; "removes most of INV-001" |
| Concrete | MET | Per-agent tool subsets | MET | `Bash(codegraph callers *)` | MET | Exact env string |
| Section purpose | MET | | MET | | MET | |
| Terms defined/delegated | MET | Delegated to `context.md` | MET | Delegated to `context.md` and BR | MET | Delegated to `context.md` |
| Decision points | MET | "roster test changes in the same commit" | MET | Deferral trigger | MET | "one live smoke test needed" |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | A | B | C | Evidence |
|-----------|---|---|---|----------|
| ≥3 risks with probability/impact | NOT MET | NOT MET | NOT MET | No variant rates probability or impact |
| Mitigation per risk | NOT MET | NOT MET | NOT MET | A: none; B: no fix for latency or lost follow-ups; C: no fix for schema overhead |
| Failure modes/recovery | NOT MET | MET | MET | B: labels, leads only; C: Grep/Read fallback |
| External dependencies | MET | MET | MET | A: Phase 2; B: undocumented flags; C: Phase 2, foreground MCP |
| Monitoring/validation | NOT MET | MET | MET | B, C: grep test plus per-run probe; A: none |
| **Subtotal** | **1/5** | **3/5** | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | A | B | C | Evidence |
|-----------|---|---|---|----------|
| Collection boundaries | MET (re-evaluated) | MET | MET | A: "without it only explore is listed"; B: `not_initialized`/`absent`; C: missing env = absent |
| State interactions | MET | MET | MET | Daemon/watcher, `foreign_index`, CLI-only label |
| Guard gaps | MET | MET | MET | A: warning "must be read from tool output"; B: allowlist matching unverified; C: foreground MCP UNVERIFIED |
| Count divergence | MET | MET (re-evaluated) | MET (re-evaluated) | A: 8 schemas, `maxFiles`; B: 30-symbol batches, 100-call trigger; C: "seven small tools plus explore", "2-3 subcommands" |
| Interaction effects | MET (re-evaluated) | MET | MET | A: background subagents × MCP; B: one call serves many agents; C: artifacts plus MCP |
| **Subtotal** | **5/5** | **5/5** | **5/5** | |

### Qualitative Summary

| Dimension | A | B | C |
|-----------|---|---|---|
| Completeness | 2/5 | 3/5 | 3/5 |
| Correctness | 3/5 | 4/5 | 3/5 |
| Structure | 5/5 | 5/5 | 5/5 |
| Clarity | 5/5 | 5/5 | 4/5 |
| Risk Coverage | 1/5 | 3/5 | 3/5 |
| Invariant & Edge Case | 5/5 | 5/5 | 5/5 |
| **qual_score** | **21/30 = 0.700** | **25/30 = 0.833** | **23/30 = 0.767** |

### Edge Case Floor Check

All three variants score 5/5, above the 1/5 floor, so all three are eligible as base.

## Position-Bias Mitigation

Raw totals: Pass 1 gave A 19, B 24, C 24; Pass 2 gave A 20, B 23, C 21.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Comp-2 | A | MET | NOT MET | DISAGREE | MET (names the failure scenarios; handling is scored under Risk-3) |
| Corr-1 | A | NOT MET | MET | DISAGREE | NOT MET (the 1:1 swap claim conflicts with EVAL §6.2 "Partial") |
| Clar-1 | A | NOT MET | MET | DISAGREE | MET ("may" states a documented unknown) |
| Inv-1 | A | NOT MET | MET | DISAGREE | MET (the empty-listing boundary is named) |
| Inv-5 | A | MET | NOT MET | DISAGREE | MET (background subagent × MCP; listing × every session) |
| Corr-4 | B | MET | NOT MET | DISAGREE | MET (needs an external fact; already penalised under Corr-1) |
| Clar-1 | B | NOT MET | MET | DISAGREE | MET (approximations are quantified) |
| Inv-4 | B | MET | NOT MET | DISAGREE | MET (count thresholds stated) |
| Comp-1 | C | MET | NOT MET | DISAGREE | MET ("Allowlists name exact read subcommands" covers the closed-Bash class) |
| Corr-5 | C | MET | NOT MET | DISAGREE | NOT MET (no source cited for any figure; INV-001 claim unsupported) |
| Inv-4 | C | MET | NOT MET | DISAGREE | MET (tool and subcommand counts stated) |

- Disagreements re-evaluated: 11 (by the orchestrator, against both passes' evidence).
- Final verdicts that differ from Pass 1: 4. Final verdicts that differ from Pass 2: 7.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker (diff points won, Step 2) |
|---------|---------------|--------------|-----------------|-------------------|
| A (default:architect) | 0.460 | 0.350 | **0.810** | 2.0 |
| B (default:security+analyzer) | 0.495 | 0.417 | **0.912** | 6.5 |
| C (default:backend+qa) | 0.488 | 0.383 | **0.871** | 10.5 |

**Margin**: B leads C by 0.041 (4.1 points), which is below the 5% threshold.
**Tiebreaker applied**: Yes, level 1 (debate performance). C won 10.5 diff points and B won 6.5; shared wins count as 0.5 each (see the Scoring Matrix in `debate-transcript.md`). The two are not within 5% of each other, so C is selected at level 1.

## Selected Base: Variant C (default:backend+qa)

### Selection Rationale

On score alone, B and C are within the tiebreak band. B's lead comes from wording (Clarity-1) and from citing its sources (Correctness-5). C won the substance of the debate. All three advocates ended Round 2 backing "amended C" as the merge base:
- MCP for lookups (3-15 ms against about 300 ms, EVAL §5.5-5.6);
- telemetry inherited from the MCP entry (EVAL §7 step 5);
- a documented `file` pin (EVAL §3);
- an explicit fallback when the env line or codegraph is missing.

C lost on two points:
- its freshness overclaim (X-004, conceded);
- its silence on explore (X-003, conceded).

Both are fixed by merging in B's contract.

### Strengths to Preserve from Base (C)
1. MCP for symbol, caller, callee, impact and outline lookups in main sessions and orchestrators.
2. Exact codegraph MCP names for read-only agents that carried Serena symbol tools; artifacts kept where a brief already uses them.
3. CLI only for what MCP cannot do (`affected`, `status` where MCP is absent, user-typed `init`), with exact read-subcommand allowlists and the mutation grep test.
4. The degrade rule: a missing env line or missing codegraph means behave as "codegraph absent" (Grep/Read).
5. One readiness check per run (MCP `codegraph_status`, else CLI `status`); stale or foreign answers are leads only.

### Strengths to Incorporate from Non-Base Variants
1. From B: the five-state vocabulary `fresh|stale|not_initialized|foreign_index|absent` and the FR-01..FR-08 contract (C-005, U-004).
2. From B: the explore ban, enforced by leaving explore out of the explicit list (X-003; A-002 rejected by all three).
3. From B: measure the NFR-06 schema overhead before the env line ships; drop the 100-call trigger (C-010, X-002).
4. From B: artifacts as the fallback when the foreground-agent MCP smoke test fails (C-008, X-001); evidence-validator stays byte-identical (D-11).
5. From B (Round 2): exact MCP names in `allowed-tools`, never the wildcard in a primitive; pin `projectPath` to the worktree root realpath; FR-22 telemetry handoff; ban node file mode as a Read substitute.
6. From A: the exact per-agent MCP tool subsets (U-001) and the single `Bash(codegraph affected *)` pattern (U-002).
7. From A (Round 2): approval is not availability (A-003).
8. From C (Round 2): E-1 also captures the MCP form of the worktree warning; closed-Bash orchestrators need no `status` pattern.
