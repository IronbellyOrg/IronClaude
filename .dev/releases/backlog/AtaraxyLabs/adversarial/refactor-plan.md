# Refactor Plan: Merge into Unified Eval+Incorporation Release Plan

Base = V1 (architect state machine). Below: each graft, its source, target location, rationale, risk.

## Grafts from V2 (analyzer) → eval substance

| # | Source (V2) | Target in base | Integration | Risk |
|---|-------------|----------------|-------------|------|
| R-01 | Scenario matrix (§3, 10 scenarios) | New §"Eval Harness" + each tool's S1 Shadow table | Replace V1's per-tool shadow tables with V2's fuller matrix, keyed to baselines | Low |
| R-02 | 30-metric catalog (§4 RQ/SA/MC/CP/MCP) | New §"Metric Catalog"; gate thresholds (S2) cite metric IDs | V1 gates G-* now reference V2 metric IDs (e.g., G-sem-1 = CP-1 + RQ-1) | Low |
| R-03 | Ground-truth tiering + blind adjudication + dedup (§8) | New §"Judging Protocol" | Inserted before metrics; mandates independent judge, rejects inspect keyword judge | Low |
| R-04 | Statistical-validity (§11): Simpson's, effect sizes, confidence labels, repeated-run | New §"Statistical Validity"; verdicts carry confidence label | Caps verdict strength by sample adequacy | Low |
| R-05 | Vendor-claim hypotheses (H-sem/inspect/weave §6) | Per-tool phase sections | Each tool's S1 explicitly lists hypotheses to confirm/refute | Low |
| R-06 | Scorecard templates (§10) | New §"Scorecard Templates" | Value + Cost + Risk scorecards become the S2 decision artifact | Low |
| R-07 | Data-source stratification (§7) + corpus manifest (§9.3) | New §"Data Sources & Corpus" | Native→curated→synthetic→generalization tiers | Low |

## Grafts from V3 (devops) → cost instrumentation

| # | Source (V3) | Target in base | Integration | Risk |
|---|-------------|----------------|-------------|------|
| R-08 | 5-domain cost taxonomy (C1–C5) | New §"Cost Model"; V1's "all-in cost columns" now = C1–C5 | Every shadow scenario reports C1–C5 | Low |
| R-09 | **Multi-vendor token economics** (C3) | §"Cost Model" + token gate | **Resolves X-005:** token-saving value weighted by provider (gpt-5.5/qwen/claude); 20% floor only if expensive provider + ~0 latency | Med — reshapes the token gate; highest-value graft |
| R-10 | Latency harness (bash) + cold/warm + O(n) scaling | §"Cost Model" → instrumentation; Phase 0 deliverable | Becomes the C2 measurement tool in `.dev/eval-workspaces/cost-measurement/` | Low |
| R-11 | Install matrix (Ubuntu/macOS/Docker/GHA) + prebuilt-binary requirement | New Phase 0 §; promoted from A-003 | **Phase 0 install gate**: no prebuilt + cargo-in-CI failure → install gate fails | Med — new hard gate before value measurement |
| R-12 | TCO 1-5 scorecard + per-tool budgets (sem≤12/inspect≤12/weave≤10) | §"Scorecard Templates" (merged with V2 cost scorecard) | TCO budget + V2 metric thresholds JOINTLY gate S2 | Low |
| R-13 | sem↔GNU-parallel 4-step neutralization | sem S0 (replaces V1's narrative rule) | Concrete detection guard + `sem-cli` invocation rule | Low |
| R-14 | Usage monitoring / dead-weight detection (2wk zero-call → deregister) | S4 Re-eval | Adds "is it even used?" gate to steady-state | Low |
| R-15 | Quarterly maintenance matrix (~10.5 hr/qtr) | §"Cost Model" C4; feeds CP-2 | Quantifies V1's CP-2 cumulative-cost freeze | Low |

## Promoted shared assumptions (A-001..A-004) → mandatory Phase 0 pre-flight

| # | Assumption | Becomes |
|---|-----------|---------|
| R-16 | A-001 corpus exists | **Phase 0 Gate G0-1**: corpus inventory; insufficient history caps all verdicts at shadow_only/Low-confidence |
| R-17 | A-002 expensive-provider routing | **Phase 0 Gate G0-2**: confirm review provider; if qwen-default, token-value gate is advisory only, tools justify on latency/precision |
| R-18 | A-003 prebuilt binaries / CI cost | **Phase 0 Gate G0-3**: install matrix must pass; cargo-only-in-CI >5min/tool = fail |
| R-19 | A-004 sem-core on Markdown-heavy mix | **CP-1 substrate gate** stratified by file type; `.md`/skill-file entity reliability measured explicitly |

## Base weaknesses fixed by grafts

| V1 weakness | Fixed by |
|-------------|----------|
| Gate thresholds are placeholders w/o statistical power | R-02, R-04 (metric catalog + confidence labels) |
| Cost is structural not quantitative | R-08, R-09, R-10, R-12, R-15 (full cost model + harness + TCO) |
| No labeling/judging methodology | R-03 (ground-truth tiering + blind adjudication) |

## Changes NOT made (base approach kept)
- V1's "never link sem-core Rust lib" doctrine — kept verbatim (neither other variant contests; it is the keystone of reversibility).
- V1's weave single-corruption auto-KILL — kept (stricter than V2's "blocks adoption"; safety-dominant).
- V1's between-tool gate + CP-1/CP-2 — kept as the plan spine (V2's 7-phase timeline mapped onto it, not replacing it).
- V2's 20/10 graduation minimums kept over V3's 5/3 (V3's 5/3 retained as the *shadow* directional floor — both, tiered).
