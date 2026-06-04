---
topic: "Create an evaluation release plan to incorporate the three Ataraxy-Labs tools (sem, inspect, weave) one at a time, with a detailed set of evals to determine their real-world value and cost across a broad variety of scenarios"
domain: research
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-06-04T00:05:00Z
sources:
  - https://github.com/Ataraxy-Labs/inspect
  - https://github.com/Ataraxy-Labs/weave
  - https://github.com/Ataraxy-Labs/sem
user_decisions:
  integration_mechanism: "Hybrid — register the 3 MCP servers AND wire into existing skills (sc:auggie-review, sc:git, code-review)"
  eval_scope: "Framework-native first (this repo's PR review, worktree merges, roadmap/cleanup-audit diffs), then optionally generalize"
  cost_lens: "All-in — tokens + latency + integration/maintenance burden"
  incorporation_order: "sem → inspect → weave (dependency order; sem-core is the shared foundation)"
---

# Seed Brief: Ataraxy-Labs Tool Evaluation & Incorporation Release Plan

## Problem Statement

IronClaude/SuperClaude is a Claude Code framework whose highest-leverage workflows
revolve around **diffs, code review, and merges**: `sc:auggie-review` (5-wave
PR/diff review shelling out to `auggie`), the built-in `code-review`/`simplify`
skills, `sc:git`, the roadmap scanner, `cleanup-audit`, and heavy git-**worktree**
parallel development. Today all of these operate on **line-based** git diffs and
LLM-token-heavy retrieval.

Ataraxy-Labs ships a coherent, Rust/tree-sitter toolchain — all built on a shared
`sem-core` entity-extraction engine, all distributing CLI **and** MCP server
surfaces — that operates at the **entity level** (functions, classes, methods)
instead of lines:

| Tool | Role | Core capability | Surfaces |
|------|------|-----------------|----------|
| **sem** | Foundation | Entity-aware `git diff` replacement; cross-file impact graph; entity-blame; **token-budgeted LLM context extraction**; 27 languages | CLI (`diff/impact/blame/log/entities/context/setup`), MCP (6 tools: `sem_entities/sem_diff/sem_blame/sem_impact/sem_log/sem_context`), `sem-core` Rust lib |
| **inspect** | Review | Entity-level PR risk triage; 0.0–1.0 danger score (blast radius + public-API exposure + dependents + change taxonomy); Union-Find untangling; routes riskiest entities to an LLM | CLI (`diff/pr/file/review/bench`), MCP (6 tools: `inspect_triage/inspect_entity/inspect_group/inspect_file/inspect_stats/inspect_risk_map`) |
| **weave** | Merge | Entity-level semantic 3-way merge driver; resolves "false conflicts" Git can't; git merge driver + Jujutsu; semantic conflict markers | CLI (`setup/unsetup/preview`), `weave-driver` binary, MCP (tool names **undocumented**) |

The task is to produce a **phased release plan** that incorporates these tools
**one at a time** (sem → inspect → weave), each gated by a **rigorous, falsifiable
eval** that measures real-world **value AND all-in cost** before the next tool is
admitted. The plan must avoid the failure mode of "install three shiny Rust tools,
wire them everywhere, and discover six months later they cost more tokens/latency/
maintenance than they save."

## Known Context

### Integration mechanism (decided: Hybrid)
- MCP servers register via `superclaude mcp --servers <name>` (the `install_mcp.py`
  `MCP_SERVERS` registry) or `claude mcp add --transport stdio --scope user <name> -- <binary>`,
  exactly as Auggie is registered. The 3 tools ship **stdio** MCP servers (Rust binaries:
  `sem-mcp`, an inspect MCP binary, a weave MCP binary).
- Skill wiring targets: `sc-auggie-review-protocol` (inspect overlaps directly),
  `code-review`/`simplify` (sem/inspect context), `sc:git` (weave merge driver),
  roadmap scanner + `cleanup-audit` (sem entity diffs).

### Verified tool facts (from upstream READMEs, 2026-06-04)
- **sem**: install via `brew install sem-cli` / `npm i -D @ataraxy-labs/sem` / `cargo install --git ... sem-cli` / Docker. 133 tests passing, 2.1k stars. **No upstream speed or token-reduction numbers published** → these are the headline claims the eval must *generate*. ⚠️ Binary-name **collision with GNU parallel's `sem`**. Unrecognized file types → chunk-based fallback. `sem context` omits the target entity if it exceeds the token budget.
- **inspect**: `cargo install --git ... inspect-cli`. Danger formula is fully specified (classification_weight 0.05–0.55 + blast_ratio×0.3 + ln(1+dependents)×0.1 + public_api_boost 0.15 + change_type_weight 0.05–0.2; cosmetic ×0.3). Tiers: Critical ≥0.7 / High ≥0.5 / Medium ≥0.3 / Low <0.3. Claims **95% recall** (Greptile set) but **precision only 33.3%** (high false-positive rate); reviews **only the top-60 riskiest entities** (recall ceiling on large PRs); triage benchmark covers **only 3 Rust repos**; benchmark judge is **heuristic keyword matching** (weak). Providers: anthropic/openai/ollama/openai-compatible.
- **weave**: `brew install weave` / `cargo install --path crates/weave-cli` + `weave-driver`. Claims ~95% conflict reduction, 100% clean on 31 scenarios (Py/TS/Rust/Go/Java/C) vs Git 48%, zero regressions on git/Flask/CPython/Go/TypeScript. Jujutsu supported. Falls back to line merge for unsupported types, files >1MB, binaries. ⚠️ **MCP tool names undocumented**.

### Framework constraints
- Source-of-truth discipline: edit `src/superclaude/`, then `make sync-dev`; never stage `.claude/` (except `settings.json`).
- UV-only Python; Rust/cargo is a **new toolchain dependency** the framework does not currently require → maintenance-cost factor.
- All artifacts under `.dev/`; this plan lives at `.dev/releases/backlog/AtaraxyLabs/`.

## Constraints

- **One tool at a time**, hard-gated: a tool does not advance to "wire into skills" until its eval clears a defined value/cost bar. sem must clear before inspect; inspect before weave.
- **Framework-native scenarios first** — evals run against THIS repo's real PRs, real worktree merges, real roadmap/cleanup diffs before any broad multi-repo generalization.
- **All-in cost accounting** — every eval reports: (a) LLM token delta vs status quo, (b) wall-clock latency added, (c) integration + maintenance burden (Rust build, MCP upkeep, version drift, binary-name collisions).
- **Falsifiable, baseline-anchored evals** — each metric compares against a concrete status-quo baseline (raw `git diff`, current `sc:auggie-review` Auggie pass, native git merge). No metric without a baseline.
- **Independent verification of vendor claims** — upstream benchmark numbers (95% recall, 95% conflict reduction) are treated as hypotheses to confirm/refute on our own data, not as givens. inspect's keyword-matching judge is explicitly distrusted.
- **Reversibility** — every incorporation step must be cleanly removable (`sem unsetup`, `weave unsetup`, MCP deregistration) with a documented rollback.
- **No production gating on day one** — tools run in shadow/advisory mode (compare, don't replace) until an eval proves the replacement is safe.

## Success Criteria

- A **release plan document** with phases per tool: Spike → Shadow eval → Gated decision → Skill integration → Re-eval, plus a kill/keep gate between tools.
- A **detailed eval harness spec**: scenario matrix (PR review, worktree merge, entity diff, impact analysis, LLM-context extraction), metrics with units and baselines, data sources (which repo PRs/branches), and pass/fail thresholds.
- **Per-tool value/cost scorecards** with explicit go/no-go thresholds (e.g., "sem `context` must cut review-prompt tokens ≥30% at equal or better finding recall, adding <Xs latency, or it does not graduate").
- **Decision-record template** capturing the keep/kill verdict per tool with evidence citations.
- A **broad-scenario generalization appendix** (multi-repo / multi-language) gated behind native-eval success.
- Clear ownership of the **new Rust toolchain maintenance cost** and a stance on the `sem` ↔ GNU-parallel collision.

## Open Questions

- Should the eval harness be a new `superclaude eval` CLI subcommand (reusable, scriptable), or a one-off `.dev/` scenario script set? (Tradeoff: reusability vs build cost.)
- For inspect's low precision (33%), what false-positive budget is acceptable when wired into `sc:auggie-review` — pre-filter only, or full replacement of the Auggie pass?
- weave in worktree-heavy dev: eval as a global git merge driver (`weave setup`) or scoped per-worktree (`setup --local`) to limit blast radius?
- Is Anthropic-provider LLM routing for inspect's `review` acceptable given the framework's multi-vendor model routing (`ANTHROPIC_DEFAULT_*` → gpt-5.5/qwen/claude)? Token-cost attribution must account for this.
- Token-cost baseline: measure against raw `git diff` piped to a model, or against the current `sc:auggie-review` Auggie retrieval pass (which already claims large token savings)?
- How many real PRs / merge events does this repo have available to form a statistically meaningful native eval set, vs needing synthetic/curated scenarios?

## Enrichment Context

(Full artifact: `enrichment/codebase-context.md`, quality_tier=primary)

- **MCP registration** is a solved pattern: add 3 stdio entries to `src/superclaude/cli/install_mcp.py` `MCP_SERVERS` (or `claude mcp add --transport stdio`), mirroring how Auggie is registered. Reversible via `claude mcp remove`.
- **Highest-overlap skill** is `sc-auggie-review-protocol` (5-wave; Wave 2 runs `auggie --print --output-format json`). inspect can slot in as a **pre-filter or second review engine**, not a replacement (its 33% precision argues advisory-only).
- **sem** feeds entity-scoped token-budgeted context to `code-review`/`simplify` and structural signals to the roadmap scanner + `cleanup-audit`.
- **weave**'s killer use case is THIS repo's heavy **git-worktree parallel dev** — merging concurrent worktree branches that edit the same files in independent functions.
- **Dominant cost factor**: Rust/cargo is a brand-new toolchain dependency (framework is UV-only Python). Plus the `sem`↔GNU-parallel binary collision and weave's undocumented MCP tools are concrete pre-integration risks.
