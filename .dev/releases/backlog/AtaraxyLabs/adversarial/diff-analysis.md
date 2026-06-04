# Diff Analysis: Eval+Incorporation Release Plan Comparison

## Metadata
- Generated: 2026-06-04
- Variants compared: 3 (V1 opus/architect, V2 sonnet/analyzer, V3 haiku/devops)
- Total differences found: 18 (structural 4, content 6, contradictions 5, unique 12, shared assumptions 4)
- Source: `seed-brief.md` (domain=research, strategy=systematic)

## Structural Differences

| # | Area | V1 architect | V2 analyzer | V3 devops | Severity |
|---|------|-------------|-------------|-----------|----------|
| S-001 | Organizing spine | 5-stage state machine per tool (S0–S4 + S-KILL) | 7-step lifecycle + 7-phase timeline (A–G) | 5 cost domains (C1–C5) + 4 cost-gated phases | Medium — different decompositions of the same flow |
| S-002 | Primary artifact | Integration architecture + rollback runbook | Metric catalog + scorecard templates | Latency harness + TCO scorecard | Low — complementary, not competing |
| S-003 | Gate expression | Lettered gates (G-sem-1..5) tied to states | Per-tool spike/shadow/incorporation gates w/ pass/fail lists | Numeric TCO budgets (≤12 shadow / ≤10 prod) | Medium — qualitative vs quantitative gate language |
| S-004 | Depth | Structure-deep, eval/cost-shallow (self-flagged) | Eval-deep, architecture-shallow (self-flagged) | Cost-deep, eval/architecture-shallow (self-flagged) | Low — weaknesses are mutually covering |

## Content Differences

| # | Topic | V1 approach | V2 approach | V3 approach | Severity |
|---|-------|-------------|-------------|-------------|----------|
| C-001 | sem token threshold | ≥30% vs raw-diff, recall floor | ≥30% vs **Auggie** pass, recall within 5pp | ≥30% vs **Auggie**, 20% floor if latency~0 | Low — converge on 30%/beat-Auggie |
| C-002 | inspect gating | advisory/pre-filter only, never gating | advisory ≥45% / pre-filter ≥55% top-20 precision | advisory-only, FP-budget defined in eval | Low — V2 supplies the numbers V1 demands |
| C-003 | weave conflict-reduction bar | ≥50% native | ≥60% native + 90% synthetic stretch | ≥50% native | Low — take ≥60% (strictest) |
| C-004 | weave scope | per-worktree `setup --local` (resolved) | local-first, global blocked | per-worktree default in eval | None — full agreement |
| C-005 | eval harness form | `.dev/` scripts; promote to `superclaude eval` only if proven | `.dev/` first; promote after 1 full cycle | bash harness; CLI only if regular regression | None — full agreement |
| C-006 | minimum sample | defers to analyzer | 20 PR/10 merge graduation; all-available + synthetic if fewer | 5 PR/3 merge shadow minimum | Medium — reconcile as tiered (see X-003) |

## Contradictions

| # | Point of conflict | Position(s) | Impact | Resolution |
|---|-------------------|-------------|--------|------------|
| X-001 | Token threshold floor | V2: "no reduction vs Auggie = no graduation" (hard 30%); V3 Risk-2: "lower to 20% if latency near-zero" | Medium | **Merge:** 30% target; 20% floor permissible ONLY IF latency cost ≈0 AND workflow routes to an expensive provider (Claude/GPT-5.5). Ties to A-002. |
| X-002 | Sample size for verdicts | V2: 20 PR/10 merge for graduate; V3: 5 PR/3 merge minimum | Medium | **Not a true contradiction — different tiers.** 5 PR/3 merge = shadow (directional/low-confidence); 20 PR/10 merge = graduate (high-confidence). Adopt V2's confidence-capping. |
| X-003 | inspect precision bar | V1: no numeric (recall-loss <5% for pre-filter); V2: ≥45% advisory/≥55% pre-filter; V3: "FP budget TBD" | Low | **Merge both axes:** V2's precision floor AND V1's recall-loss ceiling AND V3's FP-per-PR budget — all three gate inspect jointly. |
| X-004 | weave reduction % | 50% / 60% / 50% | Low | **Take ≥60%** (V2, most defensible) on native; 90% stretch on synthetic independent-function cases. |
| X-005 | Token-value relevance | V1/V2 treat token reduction as core value; V3 shows it may be economically negligible on cheap providers | **High** | **V3 wins this point.** Token savings is conditional value, not absolute. Gate must weight token savings by the provider actually used; if reviews route to qwen, tools justify on latency/precision instead. Promote to A-002. |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|-------------|-------|
| U-001 | V1 | 5-stage reversible state machine (identical per tool) | High |
| U-002 | V1 | Between-tool gate (next tool's S0 blocked until prior tool's S4 live+KEEP) | High |
| U-003 | V1 | Plan-level checkpoints CP-1 (substrate-failure halt) / CP-2 (cumulative-toolchain-cost freeze) | High |
| U-004 | V1 | "Seam not weld" surface doctrine; **never link sem-core Rust lib directly**; full-initiative kill switch (3 flags + 3 mcp remove + 1 unsetup) | High |
| U-005 | V1 | weave single-semantic-corruption → automatic KILL; preview-only in shadow | High |
| U-006 | V2 | 30-metric catalog with units + baselines + thresholds (RQ/SA/MC/CP/MCP groups) | High |
| U-007 | V2 | Ground-truth tiering (strong/medium/weak) + blind adjudication + dedup policy; **inspect's keyword judge explicitly rejected** | High |
| U-008 | V2 | Statistical-validity guards: Simpson's paradox (stratum-level pass/fail), effect sizes, confidence labels, repeated-run stability | High |
| U-009 | V2 | Scenario matrix (10 scenarios × tools × baselines) + vendor-claim hypotheses (H-sem/inspect/weave) + stratified data-source plan | High |
| U-010 | V3 | **Multi-vendor token economics** — savings weighted by gpt-5.5/qwen/claude pricing; token-value may be negligible on cheap providers | High |
| U-011 | V3 | Concrete latency harness (bash, cold/warm, O(n) scaling) + install matrix (Ubuntu headless/macOS/Docker/GHA) | High |
| U-012 | V3 | TCO 1-5 scorecard with per-tool budgets + usage monitoring (dead-weight detection after 2wk zero-call) + 4-step sem-collision neutralization + quarterly maintenance matrix | High |

## Shared Assumptions (UNSTATED → promoted to debate)

| A-NNN | Assumption | Source agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | This repo HAS enough PR/merge history for a meaningful native eval | All 3 assume native-first is feasible | **HIGH** — if false, every native gate is theater; first action MUST be a corpus inventory; insufficient history caps verdicts at shadow_only/directional | PROMOTED |
| A-002 | Framework review runs on an expensive provider often enough for token savings to matter | V1/V2 treat tokens as core value | **HIGH** — if reviews route to qwen, the token-value case collapses; tools must justify on latency/precision | PROMOTED (ties X-005) |
| A-003 | Upstream ships prebuilt binaries OR cargo-from-source is acceptable in CI | All 3 assume installability | **HIGH** — no prebuilt + cargo-in-CI = 6-15min/run; install gate may fail before value is measured | PROMOTED (Phase 0 gate) |
| A-004 | sem-core entity model is reliable on THIS repo's Markdown-heavy mix (skills are `.md`) | sem G-sem-2 + all fallback notes | **HIGH** — `.md`/skill files dominate; tree-sitter Markdown support is weakest; threatens all 3 tools' value on framework-native scenarios | PROMOTED (CP-1 substrate gate) |

## Summary
- Total structural differences: 4 (all Low/Medium — complementary decompositions)
- Total content differences: 6 (5 converge, 1 reconciled as tiers)
- Total contradictions: 5 (4 numeric/reconcilable, 1 — X-005 — a genuine value-conditionality insight that reshapes the gate model)
- Total unique contributions: 12 (all High value — each variant owns a distinct, non-overlapping pillar)
- Total shared assumptions surfaced: 4 (UNSTATED: 4, all HIGH) — these become mandatory Phase 0 pre-flight checks
- Highest-severity items: X-005, A-001, A-002, A-003, A-004
- **Convergence indicator: HIGH** — zero directional contradictions; all divergence is numeric-threshold or coverage-depth, resolvable by union.
