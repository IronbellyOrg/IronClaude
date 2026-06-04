---
proposal: 3
author: "devops / haiku"
lens: "all-in cost + operational reality"
date: 2026-06-04
order: "sem → inspect → weave (honored)"
integration: "hybrid — MCP servers + skill wiring"
eval_scope: "framework-native first"
cost_lens: "all-in — tokens + latency + install + maintenance + rollback"
---

# Proposal Variant 3: DevOps/Cost Lens — TCO-Gated Incorporation

## Core Thesis

**Adopting three Rust/tree-sitter binaries into a UV-only Python framework is a toolchain-level
infrastructure change, not a feature addition.** Every gate in the incorporation plan must
answer one question: *does the measured all-in cost (tokens + latency + install + maintenance
+ rollback risk) justify the value?* If the eval cannot produce a positive delta within the
shadow phase, the tool is killed — no sentiment, no sunk-cost fallacy, no "maybe later when
the ecosystem matures." The plan is a **kill-first release pipeline** with hard cost
thresholds.

---

## Cost Taxonomy

Five cost domains, each measurable and attributable per tool:

| Domain | Metric | Unit | Measured When |
|--------|--------|------|---------------|
| C1 — Toolchain/Install | Binary fetch or build wall-clock | seconds | First install + CI cold start |
| C2 — Latency | Wall-clock delta per review/merge loop | seconds/operation | Shadow eval runs |
| C3 — Token Cost | LLM token delta vs status-quo baseline | tokens/prompt | Shadow eval runs |
| C4 — Maintenance/Drift | Quarterly upkeep effort | hours/quarter | Ongoing |
| C5 — Rollback/Operability | Mean time to deregister + clean up | minutes | Documented + tested |

**Total Cost of Ownership (TCO)** per tool = `C1 + (C2 × ops_per_quarter) + (C3 × token_rate) + C4 + C5_weight`

---

## C1: Toolchain & Install Cost

### New Dependency Surface

The framework currently has **zero Rust/cargo dependency**. This is a step-function change.

| Install Path | sem | inspect | weave | Notes |
|---|---|---|---|---|
| `brew install sem-cli` | ~30s | N/A | `brew install weave` ~30s | Requires Homebrew; fails on headless Linux CI |
| `npm i -D @ataraxy-labs/sem` | ~15s | N/A | N/A | Requires Node.js; adds node_modules to CI |
| `cargo install --git ...` | ~120-300s (compile) | ~120-300s | ~120-300s + weave-driver | Dominant cost; Rust toolchain install ~30-60s extra |
| Docker image | ~5s pull | N/A | N/A | sem only; adds container runtime |

### CI Implications

**Current CI**: `uv run` + `ruff` + `pytest`. Zero Rust.

**Post-sem CI options** (ranked by operational cost):

1. **Prebuilt binary install (preferred)**: `pip install` equivalent — fetch prebuilt sem-cli from PyPI/npm/Homebrew. Add ~15-30s to CI per job. No Rust toolchain in CI image.
2. **Cargo install from source**: Add `rustup` + `cargo` to CI image (+~60s). Each `cargo install` compiles from source (+~120-300s per binary). Multiplied by 3 tools = **6-15 minutes added per CI run**.
3. **Cached prebuilt binaries**: Build once, store in CI cache or GitHub Releases. Requires maintaining a build pipeline for the Rust tools themselves.

**Recommendation**: For the shadow eval, use `cargo install` to test the real worst-case. For production, mandate prebuilt binary paths (brew/npm) and **exclude cargo-from-source from CI entirely**. If upstream does not ship prebuilt binaries for the target platform, the tool fails the install gate.

### Headless Environment Install

The framework runs in Docker containers, GitHub Actions, and potentially headless dev machines.
Each install path must be verified on:
- Ubuntu 22.04 / 24.04 (headless, no Homebrew)
- macOS (Homebrew available)
- Docker (scratch/alpine — glibc vs musl implications for prebuilt binaries)

**Install matrix** — each cell must pass within timeout:

| Environment | sem | inspect | weave |
|---|---|---|---|
| Ubuntu headless (cargo) | PASS if `cargo install` < 5min | Same | Same |
| macOS (brew) | `brew install sem-cli` < 60s | `cargo install` only | `brew install weave` < 60s |
| Docker (apt) | npm or cargo path | cargo only | cargo or prebuilt |
| GitHub Actions (ubuntu-latest) | Prebuilt or cached cargo | Same | Same |

### The `sem` ↔ GNU Parallel Collision

GNU Parallel ships a `sem` binary (semaphore). This is a **real collision** on any system with both installed.

**Neutralization strategy** (must be implemented before any `sem setup`):

1. **Invocation alias**: Always invoke as `sem-cli` (brew) or `@ataraxy-labs/sem` (npm full path). Never bare `sem` in scripts, hooks, or docs.
2. **MCP server binary name**: The MCP entry in `install_mcp.py` must use the **non-colliding binary name** (e.g., `sem-cli` or full npm path), never `sem`.
3. **Git hook/merge driver**: `sem setup` writes `.gitconfig` entries referencing `sem`. Must patch to `sem-cli` or provide wrapper script.
4. **Detection guard**: In the install script, probe for both `sem --version` and `sem-cli --version`. If both exist and return different versions, emit a **WARN** and require explicit `--sem-binary=sem-cli` flag.

**Cost impact**: ~2 hours dev time to implement guard + patch all invocation sites. One-time. If upstream renames the binary, this debt goes to zero.

---

## C2: Latency Cost

### What We Are Measuring

Every operation that previously used `git diff` / `git merge` / LLM-only retrieval now
has an extra step: **tree-sitter parse → entity extract → tool output**. The wall-clock
delta is real and measurable.

### Measurement Harness

Create `.dev/eval-workspaces/cost-measurement/latency-harness.sh`:

```bash
#!/usr/bin/env bash
# Latency measurement harness for Ataraxy-Labs tool adoption
# Usage: ./latency-harness.sh <tool> <operation> <repo-path>

set -euo pipefail

TOOL="${1:?tool required: sem|inspect|weave}"
OP="${2:?operation required: diff|triage|merge}"
REPO="${3:-.}"

# Record baseline (status quo)
baseline_start=$(date +%s%N)
case "$OP" in
  diff)     git diff --stat > /dev/null 2>&1 ;;
  triage)   echo "baseline: no-op (LLM-only review)" ;;
  merge)    echo "baseline: git merge --no-commit" ;;
esac
baseline_end=$(date +%s%N)
baseline_ms=$(( (baseline_end - baseline_start) / 1000000 ))

# Record tool-latency
tool_start=$(date +%s%N)
case "$TOOL" in
  sem)
    case "$OP" in
      diff)     sem-cli diff --json > /dev/null 2>&1 ;;
      triage)   sem-cli entities --json > /dev/null 2>&1 ;;
      merge)    echo "sem: no merge op" ;;
    esac
    ;;
  inspect)
    case "$OP" in
      diff)     inspect-cli diff --json > /dev/null 2>&1 ;;
      triage)   inspect-cli triage --json > /dev/null 2>&1 ;;
      merge)    echo "inspect: no merge op" ;;
    esac
    ;;
  weave)
    case "$OP" in
      diff)     echo "weave: no diff op" ;;
      triage)   echo "weave: no triage op" ;;
      merge)    weave-driver preview --all > /dev/null 2>&1 ;;
    esac
    ;;
esac
tool_end=$(date +%s%N)
tool_ms=$(( (tool_end - tool_start) / 1000000 ))

# Report
delta_ms=$(( tool_ms - baseline_ms ))
echo "TOOL=$TOOL OP=$OP baseline=${baseline_ms}ms tool=${tool_ms}ms delta=${delta_ms}ms"
```

### Cold vs Warm Measurements

| Phase | What to Measure | Expected Pattern |
|---|---|---|
| Cold start | First invocation after fresh install / reboot | Dominated by binary load + tree-sitter grammar load |
| Warm (same repo) | Second+ invocation on same repository | Grammar cache hit; should be significantly faster |
| Warm (different repo) | Invocation on a new repository | Grammar reload; between cold and warm |

**Threshold**: Cold start must be < 10s for any single operation on repos ≤ 50k files.
Warm operations must be < 3s. If parsing a 100-file PR takes > 30s, the tool is
unusable in interactive review loops — **kill it**.

### Repository Size Scaling

Measure on three repo tiers:

| Tier | Files | Example |
|---|---|---|
| Small | < 500 | This repo (IronClaude) |
| Medium | 500-5k | Typical Python microservice |
| Large | 5k-50k | Monorepo with multiple services |

Plot latency vs file count. Expect O(n) or O(n log n). If O(n²) or worse,
the tool will break at scale — document the ceiling.

---

## C3: Token Cost

### The Multi-Vendor Reality

This framework does not use a single LLM provider. Model routing goes through:

```
ANTHROPIC_DEFAULT_MODEL → gpt-5.5 (OpenAI)
ANTHROPIC_DEFAULT_SONNET_MODEL → qwen3.6-plus (Alibaba)
ANTHROPIC_DEFAULT_OPUS_MODEL → claude (Anthropic)
```

Token cost attribution **must account for the provider of the reviewing model**, not
assume Anthropic pricing.

### Token Accounting Method

For each shadow eval run, capture:

1. **Baseline prompt tokens**: Count tokens in the current `git diff` + retrieval context
   piped to the review model (use `tiktoken` for OpenAI models, `cl100k_base` for Claude).
2. **Tool-augmented prompt tokens**: Count tokens in `sem context --budget N` or
   `inspect triage` output piped to the same model.
3. **Delta**: `(baseline - tool) / baseline` = token reduction percentage.

**Important**: Measure against the **current `sc:auggie-review` Auggie retrieval pass**,
not raw `git diff`. The framework already uses entity-aware retrieval via Auggie;
the question is whether sem/inspect does it *better* than Auggie does today.

### Token Cost Attribution by Provider

| Provider | Model | Input cost ($/1M tok) | Output cost ($/1M tok) |
|---|---|---|---|
| OpenAI | gpt-5.5 | ~$10 | ~$40 |
| Alibaba | qwen3.6-plus | ~$0.40 | ~$1.20 |
| Anthropic | claude (Opus-class) | ~$15 | ~$75 |

A 30% token reduction on Claude is worth ~7.5x more than the same reduction on qwen.
**TCO scorecard must weight token savings by the provider actually used in the workflow.**

### Per-Operation Token Budget

| Operation | Baseline (current) | Target (post-tool) | Delta |
|---|---|---|---|
| `sc:auggie-review` full 5-wave | Measure (estimate: 50-150k input) | ≤ 70% of baseline | ≥ 30% reduction |
| `code-review` single pass | Measure (estimate: 10-40k input) | ≤ 70% of baseline | ≥ 30% reduction |
| `sc:git` merge context | Measure | ≤ 80% of baseline | ≥ 20% reduction |

**Go/no-go**: If `sem context` or `inspect triage` does not reduce prompt tokens by
≥ 30% on the `sc:auggie-review` baseline (at equal or better finding recall), the tool
fails the token gate. The framework already has Auggie doing structural retrieval;
the new tool must do materially better.

---

## C4: Maintenance & Version Drift

### Quarterly Upkeep Matrix

| Cost Item | sem | inspect | weave | Notes |
|---|---|---|---|---|
| Binary updates (brew/npm) | ~30 min/qtr | ~30 min/qtr | ~30 min/qtr | Automated if brew/npm; manual if cargo |
| Cargo rebuild (if source) | ~2 hrs/qtr | ~2 hrs/qtr | ~2 hrs/qtr | Compile time + test validation |
| Rust toolchain updates | \multicolumn{3}{c|}{~1 hr/qtr (shared across all 3)} |
| MCP server compatibility checks | ~30 min/qtr | ~30 min/qtr | ~30 min/qtr | Verify stdio protocol hasn't changed |
| Skill-wiring regression tests | ~1 hr/qtr | ~1 hr/qtr | ~1 hr/qtr | Re-run eval scenarios on new version |
| weave MCP tool enumeration | ~2 hrs (one-time) | N/A | N/A | Must discover undocumented MCP tools before wiring |
| **Total per quarter** | **~3 hrs** | **~3 hrs** | **~4.5 hrs** | **~10.5 hrs total** (first qtr: ~12.5 hrs) |

### Breakage Surface

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Upstream Rust tool changes MCP stdio protocol | Medium | High (total breakage) | Pin version in `install_mcp.py`; test on version bump |
| `sem-core` API changes between sem/inspect/weave versions | Medium | High (version skew) | Pin all three to same `sem-core` commit; test matrix |
| weave undocumented MCP tools change/break | High | Medium (partial breakage) | Enumerate + document in spike; test each tool on version bump |
| Homebrew formula renamed or deprecated | Low | Medium (install breakage) | Fallback to cargo/npm path; monitor brew audit |
| GNU parallel `sem` collision resurfaces after OS update | Low | Low (warn-only with guard) | Detection guard in install script |
| Tree-sitter grammar incompatibility with new language syntax | Medium | Low (graceful fallback to line-based) | Acceptable; tool already has this fallback |

---

## C5: Rollback & Operability

### Deregistration Procedures

Each tool must have a documented and **tested** rollback path:

| Tool | Deregistration Steps | Estimated Time |
|---|---|---|
| sem | 1. `sem unsetup` (removes git hooks) 2. `claude mcp remove sem` 3. Remove from `install_mcp.py` MCP_SERVERS 4. Uninstall binary (brew/npm/cargo) | < 5 min |
| inspect | 1. No `unsetup` (stateless) 2. `claude mcp remove inspect` 3. Remove from `install_mcp.py` 4. Uninstall binary | < 3 min |
| weave | 1. `weave unsetup` (removes merge driver) 2. `claude mcp remove weave` 3. Remove from `install_mcp.py` 4. Uninstall binaries (weave + weave-driver) | < 5 min |

### Blast Radius: Global vs Per-Worktree

**weave** is the only tool with global git state impact (`weave setup` modifies `~/.gitconfig`).

**Recommendation**: Default to **per-worktree** (`setup --local` or equivalent) during shadow eval.
Global setup is only authorized after the eval proves value AND the rollback is verified.
This limits blast radius to a single worktree — if weave corrupts a merge, only that worktree
is affected, not every git repo on the machine.

**sem**'s `setup` also writes git config (merge driver / diff driver). Same recommendation:
per-repo or per-worktree during eval, global only after proven safe.

### Usage Monitoring

How do we know if a tool is actually being used?

1. **MCP call logging**: Claude Code logs MCP tool invocations. Query the session logs for
   `sem_`, `inspect_`, `weave_` prefixed tool calls.
2. **Git hook invocation**: For `sem setup` / `weave setup`, check `.git/hooks/` for
   tool-invoking scripts.
3. **Simple metric**: If after 2 weeks of shadow deployment, a tool has zero MCP calls
   and zero git hook invocations, **it is dead weight** — initiate deregistration.

---

## Per-Tool TCO Scorecard

### Scoring System

Each cost domain scored 1-5:

- **1** = negligible cost (seconds, cents, zero maintenance)
- **2** = low cost (minutes, dollars, < 1 hr/qtr maintenance)
- **3** = moderate cost (10s of minutes, $10s, 1-2 hrs/qtr)
- **4** = high cost (hours, $100s, 3-5 hrs/qtr)
- **5** = prohibitive cost (days, $1000s, > 5 hrs/qtr)

**Pass threshold**: Total TCO ≤ 12 for shadow phase; ≤ 10 for production.

### sem TCO Scorecard

| Domain | Score | Justification |
|---|---|---|
| C1 Install | 3 | Multiple install paths; cargo-from-source is slow; sem↔GNU collision adds 2h dev work |
| C2 Latency | TBD | Must measure; tree-sitter parse of 27 languages has unknown cost |
| C3 Token | TBD | Must measure vs Auggie baseline; 30% reduction target |
| C4 Maintenance | 3 | ~3 hrs/qtr; Rust toolchain upkeep; version pinning |
| C5 Rollback | 2 | `sem unsetup` exists; < 5 min; git config changes |
| **Total (excl. TBD)** | **8** | + TBD (must clear ≤ 4 combined to pass) |

**Go/no-go**: sem advances only if measured C2 + C3 ≤ 4 (combined) AND token reduction ≥ 30%.

### inspect TCO Scorecard

| Domain | Score | Justification |
|---|---|---|
| C1 Install | 4 | cargo-only (no brew/npm); always compiles from source; +60s Rust toolchain |
| C2 Latency | TBD | Must measure; entity extraction + danger scoring per PR |
| C3 Token | TBD | Must measure; low precision (33%) means extra tokens on false positives |
| C4 Maintenance | 3 | ~3 hrs/qtr; shared sem-core with sem (version coupling risk) |
| C5 Rollback | 1 | Stateless; MCP deregistration only; < 3 min |
| **Total (excl. TBD)** | **8** | + TBD (must clear ≤ 4 combined to pass) |

**Go/no-go**: inspect advances only if measured C2 + C3 ≤ 4 AND its 33% precision is
acceptable in advisory mode (false-positive budget defined in eval).

### weave TCO Scorecard

| Domain | Score | Justification |
|---|---|---|
| C1 Install | 4 | brew or cargo; weave-driver is separate binary; two install surfaces |
| C2 Latency | TBD | Must measure; semantic merge vs line merge delta |
| C3 Token | TBD | Must measure; semantic conflict markers may add or reduce context |
| C4 Maintenance | 4 | ~4.5 hrs/qtr; undocumented MCP tools; weave-driver + weave binary coupling |
| C5 Rollback | 2 | `weave unsetup` exists; but global gitconfig changes need manual verification |
| **Total (excl. TBD)** | **10** | + TBD (must clear ≤ 2 combined to pass — tightest margin) |

**Go/no-go**: weave has the tightest budget. Advances only if measured C2 + C3 ≤ 2
AND conflict reduction ≥ 50% on THIS repo's worktree merge scenarios.

---

## Phased Incorporation Plan (Cost-Gated)

### Phase 0: Infrastructure Prep (1-2 days)

- [ ] Create `.dev/eval-workspaces/cost-measurement/` with latency harness + token counter
- [ ] Implement `sem`↔GNU-parallel collision detection guard in install script
- [ ] Verify install paths on Ubuntu headless, macOS, Docker (install matrix above)
- [ ] Pin Rust toolchain version for CI (if cargo-from-source is the only path)

### Phase 1: sem Shadow Eval (1 week)

- [ ] Install sem via preferred path (brew > npm > cargo)
- [ ] Register MCP server in `install_mcp.py` (non-colliding binary name)
- [ ] Run latency harness on 3 repo tiers (cold + warm)
- [ ] Run token accounting on 5 real PRs (compare `sem context` vs Auggie retrieval)
- [ ] Score C2 + C3; decision: pass (≤ 4) or kill

### Phase 2: inspect Shadow Eval (1 week, only if sem passes)

- [ ] Install inspect (cargo only)
- [ ] Register MCP server
- [ ] Run latency + token harness
- [ ] Validate inspect's 33% precision on THIS repo's PRs (independent judge, not keyword)
- [ ] Score C2 + C3; decision: pass (≤ 4) or kill

### Phase 3: weave Shadow Eval (1 week, only if inspect passes)

- [ ] Install weave + weave-driver
- [ ] Enumerate undocumented MCP tools (spike: 2 hrs)
- [ ] Register MCP server
- [ ] Run latency + token harness on 5 real worktree merges
- [ ] Score C2 + C3; decision: pass (≤ 2) or kill

### Phase 4: Skill Wiring (only for tools that pass)

- Wire passing tools into skills per integration plan
- Re-run eval on wired configuration (wiring may change cost profile)
- If wiring pushes TCO over threshold, **dial back to advisory-only**

---

## Risks

### Risk 1: Cargo-From-Source Makes CI Unusable

If upstream does not ship prebuilt binaries and CI must compile from source, each CI run
adds 6-15 minutes. This alone could exceed the TCO budget for all three tools.

**Mitigation**: Gate on prebuilt binary availability. If not available, escalate to upstream
or fork the build process to publish prebuilt binaries ourselves.

### Risk 2: Token Savings Are Marginal vs Auggie

The framework already uses Auggie for structural code retrieval. sem and inspect may only
achieve 10-15% token reduction, not the 30% target. At that delta, the install + maintenance
cost outweighs the token savings.

**Mitigation**: Lower the threshold to 20% if latency cost is near-zero. But do not
eliminate the threshold — marginal savings are not worth the toolchain debt.

### Risk 3: weave's Global Setup Creates Permanent Git Config Drift

`weave setup` modifies `~/.gitconfig`. If a developer forgets to `unsetup`, every merge
on their machine goes through weave. This is a subtle, hard-to-detect state.

**Mitigation**: Per-worktree default during eval. Post-eval, require explicit opt-in for
global setup with a documented rollback test.

### Risk 4: Multi-Vendor Token Cost Attribution Is Opaque

If the framework routes to qwen3.6-plus for review (cheapest provider), a 30% token
reduction saves ~$0.004 per review. At 100 reviews/quarter, that's $0.40. The maintenance
cost (~10 hrs/qtr × $150/hr = $1,500) swamps the token savings by 3,750x.

**Mitigation**: The token cost gate is only meaningful if reviews run on Claude or GPT-5.5.
If the framework defaults to cheap providers, **the token savings argument collapses** and
the tools must justify themselves on latency or precision alone.

---

## Open Questions

1. **Eval harness**: CLI subcommand vs `.dev/` scripts? For this cost-focused plan, a simple
   bash harness + manual token counting is sufficient for shadow eval. A reusable CLI
   subcommand is only justified if evals run regularly (monthly/quarterly regression).

2. **Token baseline**: Measure against raw `git diff` or against `sc:auggie-review`?
   **Against `sc:auggie-review`**. The status quo is not raw git diff; it's Auggie-enhanced
   review. The new tool must beat the current best, not the baseline naive approach.

3. **inspect precision eval**: Who judges the findings? Upstream uses keyword matching (weak).
   **Human review of a 20-PR sample** by a senior dev is the only credible judge for the
   shadow eval. Budget 4-6 hours for this.

4. **weave MCP enumeration**: Should this be a prerequisite spike before Phase 3, or part of
   Phase 3? **Prerequisite** — you cannot wire an unknown surface. Budget 2 hours in Phase 0
   to run the weave MCP server and enumerate all tool names.

5. **Provider routing for inspect review**: inspect has its own LLM provider config (anthropic/
   openai/ollama). Should it use the framework's routing (`ANTHROPIC_DEFAULT_*`) or its own?
   **Use framework routing** to keep token cost attribution consistent. Override adds a
   parallel billing stream that complicates the TCO calculation.

6. **Statistical significance**: How many PRs/merges are enough? For shadow eval,
   **5 real PRs + 3 real merges** is the minimum. Below that, a single outlier PR dominates
   the metrics. This repo's PR history should be audited to confirm sufficient volume.

---

## Decision Record Template

```yaml
tool: sem|inspect|weave
eval_date: YYYY-MM-DD
phase: shadow|wired
verdict: PASS|KILL|DIAL_BACK

# Cost metrics
c1_install_seconds: <measured>
c2_latency_delta_ms: <measured>
c3_token_reduction_pct: <measured>
c4_maintenance_hrs_per_qtr: <estimated>
c5_rollback_minutes: <measured>
tco_total: <sum>
tco_threshold: 12|10

# Value metrics
finding_recall_vs_baseline: <pct>
finding_precision_vs_baseline: <pct>
conflict_reduction_pct: <weave only>
false_conflict_resolution_rate: <weave only>

# Evidence
prs_evaluated: [PR-1, PR-2, ...]
merges_evaluated: [merge-1, merge-2, ...]
latency_harness_output: <path>
token_counter_output: <path>

decision_rationale: |
  <2-3 sentences citing specific metric pass/fail>
```

---

## Summary of Distinctive Contributions

**(a) Core thesis**: Three Rust binaries in a UV-only Python framework is a toolchain
infrastructure change, not a feature. Incorporation must be kill-first, with every phase
gated by measured all-in cost (tokens + latency + install + maintenance + rollback) against
hard thresholds. If the eval cannot produce a positive delta, the tool is killed.

**(b) Three strongest contributions**:

1. **Multi-vendor token cost attribution** — accounts for the framework's actual model routing
   (gpt-5.5 / qwen / claude) and shows that token savings on cheap providers may be
   economically irrelevant vs maintenance cost.
2. **TCO scorecard with per-tool budgets** — concrete 1-5 scoring per cost domain with
   explicit go/no-go thresholds (sem ≤ 12, inspect ≤ 12, weave ≤ 10), forcing quantitative
   decisions instead of sentiment.
3. **Install matrix + sem collision neutralization** — comprehensive cross-platform install
   verification (Ubuntu headless, macOS, Docker, GitHub Actions) and a concrete strategy
   for the `sem`↔GNU-parallel binary collision that must be resolved before any integration.

**(c) Two honest weaknesses**:

1. **Thin on eval rigor** — the cost lens specifies what to measure (latency, tokens) but
   delegates *how to judge quality* to "human review of 20 PRs" without a structured rubric,
   inter-rater agreement check, or adversarial validation of the findings. A false-positive
   tool with zero cost still has negative value. The proposal underweights precision/recall
   measurement quality in favor of cost accounting.
2. **Integration architecture is hand-waved** — the proposal says "wire into skills" but does
   not specify the exact wiring points (which waves in sc:auggie-review get replaced vs
   augmented, how sem's entity context flows into code-review's prompt template, how weave's
   merge driver interfaces with git's existing merge machinery). This is a cost plan, not an
   integration plan — the other variants should cover the architecture gap.
