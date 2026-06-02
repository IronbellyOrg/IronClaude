# Octocode Integration — Final Recommendations

**Date:** 2026-05-30
**Project:** IronClaude / SuperClaude Framework
**Investigation:** TASK-RESEARCH-20260530-044428
**Stage:** 3 of 3 (synthesis)

---

## Executive Summary

After 3-stage investigation (web + codebase research → fit analysis → 6 parallel brainstorm proposals), the recommendation is a **two-stage adoption** that combines two of the six proposals as a sequenced rollout, with a third as an optional Phase 3 enhancement.

**Recommended path:**

1. **Phase 1 (immediate, 1 PR, ~5h):** Adopt **#1 Declarative Purist** to make octocode usable framework-wide via a single deep-research agent edit.
2. **Phase 2 (after 4-week pilot, 1 PR, ~17-22h):** Adopt **#5 Sub-Agent Delegate** to isolate context tax and unlock reuse across 7 downstream consumers.
3. **Phase 3 (optional, contingent on pilot data):** Layer **#2 Behavioral Router** decision logic into the sub-agent if cross-model determinism falls below 90%.

**Defer (do not adopt now):** #3 Persona-Aware (requires runtime persona state that doesn't exist), #4 Hook-Driven (author explicitly recommended deferring until ≥30% forget-rate evidence), #6 Skill-Level (33h / 9-week cost not justified before validating value at the agent level).

---

## Comparison Matrix — All 6 Proposals

| # | Proposal | Effort | Reversibility | Context Tax | Determinism | Coverage | Risk |
|---|---|---|---|---|---|---|---|
| 1 | Declarative Purist | ~5h, 1 PR, ~50 LoC | ★★★★★ single `git revert` | Medium (5 tools in deep-research) | Medium (LLM choice) | All consumers of deep-research | Low |
| 2 | Behavioral Router | ~8h, 1 PR | ★★★★★ single `git revert` | Medium | High (regex/keyword rules) | All consumers of deep-research | Low |
| 3 | Persona-Aware | ~7-8h, multi-file | ★★★★ multiple reverts | Low (per-persona subset) | Medium | Personas only — gap for personaless | Medium (no runtime persona state) |
| 4 | Hook-Driven | ~40h, worker process | ★★★ infra to roll back | Variable (async out-of-band) | High (deterministic triggers) | Framework-wide auto-activation | High (latency, telemetry, hook loops) |
| 5 | Sub-Agent Delegate | ~17-22h (8-10h MVP), 1-2 PRs | ★★★★ delete agent file | Low (~3K savings/invocation) | High (isolated agent prompt) | 7 consumers via delegation | Low-Medium |
| 6 | Skill-Level Alternate | ~33h, 4 PRs, 9.25 weeks | ★★★ per-skill revert | Low (per-skill scoped) | Medium-High | 3 skills + standalone gap | Medium |

**Scoring caveat:** "Risk" excludes the supply-chain/maintainer risk inherent to octocode itself (covered uniformly in `octocode-research.md` §4) — those mitigations (pinned version, `LOG=false`, `TOOLS_TO_RUN` whitelist) apply to ALL six proposals equally and are encoded in the Phase 0 MCP registration step.

---

## Recommended Top 2 (with Phase 3 contingent option)

### Top Pick #1: Declarative Purist (Phase 1)

**Why this is the right first move:**

- **Lowest cost, highest reversibility.** Single-file diff to `src/superclaude/agents/deep-research.md` — 5 octocode tools added to frontmatter + a 4th axis added to the existing Tool Selection Policy section. ~50 net lines, 5-minute PR review, fully revertible.
- **Mirrors existing patterns.** The deep-research agent already has a 3-axis Tool Selection Policy (Tavily / Context7 / Sequential). Adding a 4th axis ("octocode for cross-repo code patterns") is symmetric and reviewable. No new abstractions.
- **Propagates broadly with one change.** deep-research is invoked by tech-research, tech-reference, troubleshoot, brainstorm, and other downstream skills. One frontmatter change activates octocode across all consumers.
- **Codifies risk mitigations at the agent level.** The proposal explicitly bakes in:
  - Whitelisted tools only (`githubSearchCode`, `githubGetFileContent`, `githubViewRepoStructure`, `githubSearchPullRequests`, `packageSearch`) — the 5 cross-repo tools from `octocode-research.md` §6
  - Rate-limit fallback to Tavily with `site:github.com` when GitHub Search hits 30 req/min
  - 4 explicit "do not use octocode when" anti-trigger clauses pointing at auggie / Context7 / Tavily / Read

**What it cannot do (honest limits):**

- Cannot mechanically enforce fallback compliance (LLM may forget the policy)
- Cannot prevent telemetry leakage at the session level (that's a Phase 0 install-time concern)
- Cannot A/B test outcomes without instrumentation

**Pilot plan for Phase 1 (mandatory before considering Phase 2):**

| Metric | Target | Method |
|---|---|---|
| Octocode invocation rate when query has GitHub/package signal | ≥60% | Manual transcript review, 20 sessions |
| Hallucinated repo/file references | 0 | Verify all `github.com/...` URLs in deep-research outputs |
| Rate-limit failures unhandled | 0 | Log inspection during high-fanout tech-research runs |
| Net context tax vs baseline | ≤+8K tokens at session start | Token counter at session start |
| User-visible improvement in research quality | Subjective +1 on 5-pt scale | Side-by-side comparison, 10 representative queries |

**Pilot duration:** 4 weeks (minimum 50 invocations across tech-research, troubleshoot, brainstorm).

---

### Top Pick #2: Sub-Agent Delegate (Phase 2)

**Why this is the right second move (after Phase 1 pilot succeeds):**

- **Isolates context tax.** Phase 1's declarative approach loads 5 octocode tools into the deep-research agent's frontmatter — meaning every deep-research invocation pays the ~3K-token octocode schema cost, even on queries that don't need it (~75% per the proposal's analysis). The sub-agent delegate moves octocode tools out of deep-research's frontmatter into a dedicated `github-pattern-researcher` agent. Net savings: ~3K tokens per non-GitHub query.
- **Hardens against octocode failures.** The sub-agent returns structured failure codes (`OUT_OF_SCOPE`, `RATE_LIMITED`, `NO_EVIDENCE`, `PARTIAL`, `OCTOCODE_UNAVAILABLE`) so the parent can fall back deterministically. In Phase 1's declarative model, an octocode failure surfaces as a generic tool error.
- **Unlocks reuse across 7 consumers.** Once `github-pattern-researcher` exists, it can be invoked by deep-research, tech-research, sc-brainstorm, sc-troubleshoot, tech-reference, sc-auggie-review, and sc-roadmap without duplicating octocode tool configuration in each.
- **Enforces the Funnel Method.** The sub-agent's prompt mandates DISCOVER → SEARCH → LOCATE → READ ordering, preventing the common LLM failure mode of jumping straight to `githubGetFileContent` without prior `githubViewRepoStructure`.
- **20-call hard cap.** Bounded blast radius for GitHub Search API rate limits.

**Why this isn't the right FIRST move:**

- ~17-22h effort vs ~5h for Phase 1 — not worth the upfront cost without validating value first
- Adds a delegation hop (~700-token overhead) on queries that DO need octocode — net negative if octocode usage is high
- New agent file = new surface area for SoT discipline (`make sync-dev`, gitignore enforcement)

**Phase 2 trigger criteria** (decide based on Phase 1 pilot data):

| Pilot result | Recommendation |
|---|---|
| Octocode usage rate >40% AND context tax >8K | Ship Phase 2 to reclaim tax |
| Octocode usage rate <20% AND no quality wins | Roll back Phase 1; do not ship Phase 2 |
| Octocode usage rate 20-40% AND positive quality signals | Ship Phase 2 to expand reuse to 7 consumers |
| Phase 1 succeeded but rate-limit failures observed | Ship Phase 2 — structured failure codes solve this |

---

### Phase 3 Contingent Option: Behavioral Router (#2) Layered into Sub-Agent

**When to add this:** If Phase 2 sub-agent shows cross-model determinism <90% (i.e., same query routed differently by Opus vs. Sonnet vs. Haiku in the sub-agent).

**What it adds:** The 11-row trigger matrix from Brainstorm #2 (with explicit signal extraction patterns like `URL`, `PKG`, `GH_REPO`, `PR`, `LIB_NAME`, etc.) embedded INSIDE the `github-pattern-researcher` sub-agent's prompt. Tie-breaking precedence + pre-emptive rate-limit budget tracking (28-call demotion threshold) eliminates non-determinism.

**Why it's Phase 3 not Phase 1:** Without the sub-agent isolation, the trigger matrix bloats the deep-research agent definition. With the sub-agent in place, the matrix lives in a focused narrow-scope file where it's reviewable.

**Effort estimate:** ~6h on top of Phase 2.

---

## Deferred Proposals (Explanation for Each)

### #3 Persona-Aware — Defer until runtime persona state exists

**Author's honest acknowledgement** (from proposal): "The framework has no runtime persona state for a hook to read; building it is out of scope." The gating mechanism is prose-policy + audit-tag convention, not runtime enforcement. Until the framework has a persona context that hooks/wrappers can inspect, persona-aware integration is just a documentation convention — which Brainstorm #1's Tool Selection Policy already provides without the persona × tool matrix overhead.

**When this becomes worth revisiting:** If/when a persona context object exists in the framework that can mechanically gate tool availability per persona. Until then, this is "documentation theater" — useful guidance for the LLM but no enforcement.

### #4 Hook-Driven — Defer per the author's own recommendation

The Brainstorm #4 author explicitly closed with: *"Ship the declarative proposal first; only escalate to this hook-driven approach if pilot data shows the agent forgets to invoke octocode ≥30% of the time."* This is the right framing. Hooks add operational complexity (worker process, ~40h) that's only justified if the simpler declarative approach demonstrably fails. Phase 1's pilot directly measures the "forget rate" — if it stays under 30%, hooks are unnecessary; if it exceeds 30%, the hook-driven approach is the natural escalation.

**When this becomes worth revisiting:** If Phase 1 pilot shows octocode invocation rate <60% on queries that should trigger it (i.e., LLM forgets the policy despite the Tool Selection Policy text).

### #6 Skill-Level Alternate — Reject pending value validation

The skill-level proposal's 33h / 9.25-week rollout is structurally sound (3 independent A/B-tested skills) but cost-prohibitive for an integration that hasn't yet proven value. The proposal's strongest critique of the agent-level path — "coarse routing, blast-radius asymmetry, no A/B handle" — is partially addressed by Phase 2 sub-agent delegation, which provides A/B handles at the sub-agent boundary without requiring per-skill duplication.

**When this becomes worth revisiting:** If Phase 2 sub-agent shows per-consumer quality variation >20% (i.e., octocode works great for tech-research but underperforms for troubleshoot) — at that point skill-level fine-tuning becomes justifiable for the underperforming skill specifically.

---

## Mandatory Phase 0: MCP Registration (Foundational)

Independent of which proposal is adopted, Phase 0 is required before any of them:

```python
# src/superclaude/cli/install_mcp.py:29 (append to MCP_SERVERS)
"octocode": {
    "name": "octocode",
    "description": "GitHub/GitLab/Bitbucket semantic code research (5 cross-repo tools, local/LSP disabled)",
    "transport": "stdio",
    "command": "npx -y octocode-mcp@14.2.0",  # PINNED version
    "required": False,
    "api_key_env": "GITHUB_TOKEN",
    "api_key_description": "GitHub PAT (or `gh auth login` for GH_TOKEN reuse). Requires scopes: repo, read:user, read:org",
    "env_overrides": {
        "LOG": "false",  # Opt out of telemetry leaking research goals
        "TOOLS_TO_RUN": "githubSearchCode,githubGetFileContent,githubSearchPullRequests,packageSearch,githubViewRepoStructure",
        "ENABLE_LOCAL": "false",  # Use auggie/serena/Read instead
        "ENABLE_CLONE": "false",  # Reduce blast radius
    },
    "post_install_message": (
        "Octocode installed with restrictive defaults: cross-repo tools only, telemetry disabled, "
        "local tools off (use auggie+serena). To unlock all 14 tools, edit env_overrides. "
        "Pinned to v14.2.0 — review release notes before upgrading."
    ),
},
```

**Phase 0 effort:** ~1h. ~20 LoC.

---

## Rollout Timeline (Recommended)

```
Week 0:          Phase 0 — MCP registration PR (~1h)
Week 1:          Phase 1 — Declarative Purist PR (~5h) → merge
Week 1-5:        Phase 1 PILOT (50+ invocations across tech-research/troubleshoot/brainstorm)
Week 6:          Pilot review → decision gate
                 - Octocode usage 20-40% + positive quality → proceed to Phase 2
                 - Outside that range → halt and reassess
Week 7-9:        Phase 2 — Sub-Agent Delegate PR (~17-22h) → merge
Week 10-12:      Phase 2 pilot (sub-agent in production)
Week 13:         (Optional) Phase 3 — Behavioral Router layer if determinism <90%
```

**Total to fully integrated:** 13 weeks (3 months), gated by quality signals at each step.

---

## What This Investigation Did Not Cover

These are known gaps that downstream work should address:

1. **Live MCP introspection.** We did not actually install octocode-mcp@14.2.0 locally and dump its `tools/list` schema. The 14-tool inventory is from docs; some parameter names/return shapes may differ at runtime.
2. **Empirical context-tax measurement.** The "~3K tokens saved per non-GitHub query" claim from Brainstorm #5 is an estimate, not measured. Phase 1's pilot is the first chance to measure.
3. **Cross-model determinism.** Whether the same Tool Selection Policy text causes Opus, Sonnet, and Haiku to make the same routing decisions is empirically untested.
4. **Long-term breakage probability.** Octocode is at v14.2.0 with 194 versions in <12 months. We cannot predict how often Phase 1's frontmatter will break; the pinned-version strategy buys time but doesn't eliminate maintenance burden.
5. **Skills marketplace overlap.** We did not exhaustively map octocode's 19 bundled skills against IronClaude's 24 skills for semantic overlap. Brainstorm #6's critique of this overlap is the right framing — IronClaude's existing skills are not being replaced.

---

## Evidence Trail

### Research Files (Stage 1)

| File | Purpose | Status |
|---|---|---|
| `research/web-01-octocode-tools-architecture.md` | Comprehensive tool inventory + architecture | Complete |
| `research/web-02-octocode-strengths.md` | Validated use cases + benchmarks | Complete |
| `research/web-03-octocode-weaknesses.md` | Supply chain + maturity + overlap analysis | Complete |
| `research/web-04-octocode-skills-marketplace.md` | Skills marketplace deep dive | **FAILED (agent stalled at 600s)** — partial finding: `npx add-skill` may be third-party `ahmadawais/add-skill` not octocode-native |
| `research/01-existing-tooling-overlap.md` | IronClaude MCP/tool inventory | **STUB ONLY** — agent did 45 tool calls but truncated; coverage filled by web-03 + code-02 |
| `research/02-integration-points.md` | IronClaude integration surface (top 5 targets) | Complete |

### Analysis File (Stage 2)

| File | Purpose | Status |
|---|---|---|
| `octocode-research.md` | Stage 1 synthesis: strengths/weaknesses report | Complete |
| `octocode-fit-analysis.md` | Stage 2 scored fit analysis (40 agents × 24 skills × 41 commands × 10 pipelines) | Complete |

### Brainstorm Files (Stage 3)

| File | Lens | Lines | Status |
|---|---|---|---|
| `brainstorm/01-declarative-purist.md` | Declarative Purist | 294 | Complete |
| `brainstorm/02-behavioral-router.md` | Behavioral Router | 516 | Complete |
| `brainstorm/03-persona-aware.md` | Persona-Aware | 369 | Complete |
| `brainstorm/04-hook-driven.md` | Hook-Driven Auto-Activation | 702 | Complete |
| `brainstorm/05-sub-agent-delegate.md` | Sub-Agent Delegate | 519 | Complete |
| `brainstorm/06-skill-level.md` | Skill-Level Alternate Path | 553 | Complete |

**Total investigation output:** ~7,500 lines of research + analysis + brainstorming across 13 files.

---

## Next Actions

If the recommendation is accepted:

1. Open Phase 0 PR (MCP registration) — single-file change to `install_mcp.py`
2. Open Phase 1 PR (Declarative Purist) — single-file change to `agents/deep-research.md`
3. Configure pilot instrumentation (token counter, transcript reviewer)
4. Schedule 4-week pilot review checkpoint

If the recommendation is rejected:

1. Document the rejection rationale in this folder for future revisits
2. Update `octocode-research.md` Open Questions §6 with the rejection context

---

**Status:** Complete
**Investigation ID:** TASK-RESEARCH-20260530-044428
**Duration:** ~55 minutes (parallel execution)
**Agents spawned:** 12 total (6 research + 6 brainstorm), 2 stalled/stubbed
