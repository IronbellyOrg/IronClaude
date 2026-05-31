# Adversarial Debate Transcript

**Brainstorm:** octocode-skill-funnel
**Date:** 2026-05-30
**Mode:** Mode B (parallel proposals + adversarial synthesis)
**Proposals:** 3 (opus:architect, sonnet:analyzer, haiku:scribe)
**Convergence score:** 0.82 (HIGH — PASS threshold ≥0.65)

---

## Agreements (Wave 1 — Strong Convergence)

All 3 proposals independently reached the same conclusions on the foundational architecture:

| Agreement | A (architect) | B (analyzer) | C (scribe) |
|---|---|---|---|
| **Single centralized skill replaces v2 distributed integration** | Anti-corruption layer pattern | Single instrumented choke point | Single API surface |
| **5-tool cross-repo whitelist** (`githubSearchCode`, `githubGetFileContent`, `githubSearchPullRequests`, `githubViewRepoStructure`, `packageSearch`) | Embedded in skill frontmatter | Schema enforced per invocation | Schema validated at contract boundary |
| **Reject local-codebase questions** | `INVALID_REQUEST` if names local paths | Anti-pattern detection (AP1) | Rejection rule `LOCAL_CODEBASE_TOPIC_DETECTED` |
| **Reject canonical-docs questions** | `INVALID_REQUEST` if answerable from Context7 | Anti-pattern detection (AP2) | Rejection rule `CONCEPTUAL_QUERY_REQUIRES_CONFIRMATION` |
| **Evidence tagging required** | `[PRECEDENT: owner/repo@path]` mandatory in findings | Per-finding provenance trail with RDD `researchGoal`/`reasoning` | `precedent_tag` field with format `[PRECEDENT: owner/repo@path:line]` |
| **Fail-open semantics** (caller proceeds even when skill returns nothing) | `status: NO_EVIDENCE` returned, caller decides | Circuit breaker emits + degrades gracefully | `rejection` object returned, not raised |
| **Caller identity tracked** | `caller: <skill:phase>` field | Caller identity in per-invocation metrics | `caller.skill_or_command + invocation_id` required |
| **Downstream of tech-research** | Sits below tech-research's scope discovery | Receives scope from upstream, doesn't discover | `scope_mode: explicit` requires upstream-provided targets |
| **Phase 0 install discipline preserved** | Pinned version, `LOG=false`, `TOOLS_TO_RUN` whitelist, `ENABLE_LOCAL=false` | Same | Same |
| **Skill orchestration overhead acknowledged** | "Latency overhead vs direct tool call" listed as honest concession | Quantified break-even at ~10 invocations/session | Listed in "What This Cannot Do" |

**Net effect:** All three proposals would produce the SAME first PR for the skill's MCP whitelist, anti-trigger rules, fail-open semantics, and downstream positioning. The disagreements are about WHAT MORE the skill should do.

---

## Tensions (Wave 2 — Adversarial)

### Tension 1: Naming

| Proposal | Name | Argument |
|---|---|---|
| A | `cross-repo-investigation` | "No vendor name in the public surface" — if octocode is later replaced (GitHub MCP, custom `gh` wrapper, Sourcegraph), only the skill internals change. Names should describe capability, not vendor. |
| B | `octocode-funnel` | Name should signal the mechanism (octocode) AND the role (funnel choke point). Vendor agnosticism is hypothetical; readability is concrete. |
| C | `octocode-deep-dive` | Name signals mechanism + shape (deep-dive vs survey). Callers know what they're getting before reading docs. Naming collisions (vs `tech-research`, `/sc:research`) are themselves contract leaks. |

**Debate resolution:** The architect's "anti-corruption-layer" argument is logically strongest for long-term maintenance, but the analyzer + scribe agree that vendor neutrality is a hypothetical concern (no plan to swap octocode-mcp in the foreseeable future) and the cost of vendor-neutral naming is real cognitive overhead. **Recommended:** `octocode-deep-dive` — signals mechanism + shape, retains contract-stability properties of A, avoids analyzer's funnel-mixed-metaphor concern. **Migration safety:** if octocode is ever replaced, the skill can be renamed/aliased in one place (the skill registry) without touching any caller — so vendor neutrality is preserved at the *integration boundary*, not the name.

### Tension 2: Execution Model

| Proposal | Model | Argument |
|---|---|---|
| A | Hybrid `mode: inline` (default) + `mode: task` (opt-in MDTM) | Hot path (90% of callers) shouldn't pay MDTM overhead. Long-running MDTM callers can fold cross-repo work into their existing checklist discipline. |
| B | Metered execution (no MDTM) | Adding MDTM is itself a measurement burden. Keep the skill minimal so the metrics stay legible. Callers that need MDTM compose externally. |
| C | API-first (silent on MDTM) | The contract is what matters; execution mode is a caller-visible parameter only if the contract exposes it. |

**Debate resolution:** A's hybrid model is the right answer. B's concern about "measurement burden" is satisfied if MDTM is opt-in (default path produces simpler metrics; task-mode produces richer metrics + state). C's silence on MDTM is compatible. **Merged:** ship inline-mode in v1, task-mode flagged for v1.1 after pilot data confirms demand from MDTM callers.

### Tension 3: Where Novel Value Lives

| Proposal | Novel value claim |
|---|---|
| A | Decoupling — callers never touch octocode |
| B | Measurement — global rate-limit budget + per-caller hit-rate analysis previously impossible |
| C | Contract — strict YAML envelope rejects misuse loudly, prevents drift |

**Debate resolution:** These are NOT competing — they are stacked. Decoupling (A) is the prerequisite for measurement (B) to be sound (per-caller telemetry requires that callers route through one skill). Contract (C) is the mechanism that makes decoupling (A) hold over time (loose contract = drift = lost decoupling). **All three are merged into the final spec** with explicit phasing: contract first (without it, nothing else works), then decoupling becomes natural, then measurement instrumentation can be added incrementally.

### Tension 4: Output Format

| Proposal | Format |
|---|---|
| A | Markdown findings block + JSON sidecar |
| B | YAML metrics (primary) + Markdown findings (secondary) |
| C | YAML envelope canonical, Markdown derived (deterministic projection) |

**Debate resolution:** C's "canonical YAML, derived Markdown" wins on engineering grounds — single source of truth, deterministic rendering, drift-detectable via envelope hash. A's "Markdown + JSON sidecar" is the same thing under a different framing. B's metrics file is orthogonal (it's the metrics, not the findings). **Merged:** canonical YAML output envelope + deterministic Markdown projection + separate metrics file per B's schema.

---

## Unresolved (Wave 3 — Surfaced for Human Decision)

1. **Caching strategy:** A's hybrid mode mentions cache hints; B mentions cross-session cache sharing via `~/.octocode/repos/` (24h disk cache); C's contract has `cache_hints` field. None of the three propose a complete cache invalidation/eviction policy. Recommendation: defer to v1.1 after pilot data shows hit rate.
2. **Versioning policy specifics:** C proposes major/minor/patch with 6-month deprecation window + 2-prior-version carry. A and B are silent. Recommendation: adopt C's policy as default; revisit if too heavy for actual change cadence.
3. **Discoverability:** C proposes 3-layer (slash command + skill auto-trigger + caller-skill auto-invocation). A and B don't address. Recommendation: ship without slash command (per A's "intentionally invoked, not auto-triggered"); add slash command only if pilot shows direct user demand.

---

## Convergence Score: 0.82 (PASS)

- Agreements span all foundational architecture decisions (>10 strong agreements)
- Tensions are about *emphasis* and *naming*, not *architecture*
- All three proposals would produce the same first PR
- The merged design is genuinely better than any individual proposal — it stacks the three lenses rather than choosing among them

**Routing decision:** PASS → produce `merged-requirements.md`, proceed to Wave 4 (handoff=none, print summary).
