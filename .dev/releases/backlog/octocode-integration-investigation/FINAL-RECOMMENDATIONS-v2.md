# Octocode Integration — Final Recommendations v2 (Target-by-Target)

**Date:** 2026-05-30
**Project:** IronClaude / SuperClaude Framework
**Investigation:** TASK-RESEARCH-20260530-044428
**Stage:** 3 v2 — synthesis of 5 per-target brainstorms

**Difference from v1:** v1 ran 6 lenses on ONE target (deep-research). v2 runs 1 brainstorm per each of the **top 5 targets**, asking each "what is the most beneficial way to integrate octocode HERE?"

---

## Executive Summary

Five parallel `/sc:brainstorm`-style ideations produced **5 concrete per-target recommendations**, each with diff sketches, tool whitelists, anti-trigger rules, and effort estimates. The dependency graph reveals:

- **Foundational prerequisite (must land first):** MCP server registration in `install_mcp.py` (~1h)
- **Hub of the dependency graph:** Target #1 (`deep-research` agent) — Targets #2, #3 inherit through it
- **Standalone-shippable:** Targets #2, #4, #5 (can ship without #1, though some benefit from it)
- **Total scope if all 5 adopted:** ~25-30 engineering hours across ~6 PRs (1 foundation + 5 targets)

**Recommended adoption order (updated to include T6):**

1. **Phase 0** (~1h) — MCP registration with restrictive defaults
2. **Phase 1** (~3-4h) — Target #1 (deep-research agent), Candidate B (behavioral router)
3. **Phase 2** (parallel, can ship together or independently) — Targets #2, #4, #5
4. **Phase 2.5** (~1 day) — Target #6 (`/tdd` skill) — best landed after T2 settles (shares Phase 4 routing pattern)
5. **Phase 3** (~4h) — Target #3 (`/sc:research` command) — best landed last because it depends on #1

---

## Cross-Target Comparison Matrix

| # | Target | Recommended Design | Effort | Standalone? | Anti-trigger discipline | Failure model |
|---|---|---|---|---|---|---|
| 1 | `deep-research` agent | Behavioral router with question-shape triggers (Candidate B) | 3-4h | Yes (after #0) | 6 positive shapes + 4 explicit anti-triggers | `fallback_reason` annotations, mirrors Tavily-first rule structure |
| 2 | `tech-research` Phase 4 | Routed buckets at build time (W1-B + W1-F): rf-task-builder classifies each web-research topic `github-flavored` vs `open-web`, two prompt templates in SKILL.md | ~1 day (~135 LoC) | Yes (after #0) | Per-agent cap (5 searchCode + 3 searchPullRequests) + per-phase cap (8 github agents Deep tier) | Tavily fallback on HTTP 403, "Octocode Tool Usage Log" footer for Phase 6 QA |
| 3 | `/sc:research` command | New `--source` flag (`tavily`/`octocode`/`context7`/`all`/comma-list), per-backend report sections | ~4h alone, ~7-10h with prereqs | Depends on #1 | User-explicit; no auto-magic routing | Multi-source partial failure → "Sources Unavailable" callout; single-source hard-fail with install hints |
| 4 | `sc-brainstorm` Wave 2A | Strategy-gated (enterprise/deep only) + `--precedent` opt-in / `--no-precedent` opt-out, new `enrichment/precedent.md` artifact | ~5.5h | Yes (after #0) | 6 anti-trigger rules; restrictive 4-tool whitelist | Fail-open per existing Wave 2A semantics; quality-tier degrades on failure |
| 5 | `/sc:troubleshoot` command | Hybrid Tier 1 conditional `packageSearch` + Tier 2 new `precedent-finder` agent (only `bug`/`build`/`test`) | ~9.5h (~500 LoC) | Yes (after #0) | Type-gated: perf/deploy/security skip octocode | Precedent ≠ Evidence; separate report section; `evidence-validator` excluded from precedent validation |
| 6 | `/tdd` skill | **A + H + F-as-rollout-gate** — mirror T2's W1-B build-time routed buckets in Phase 4 + add Stage A PRD→octocode precedent discovery + tier-gated to Heavyweight as Phase 1 rollout | ~1 day (~180 LoC across 4 files) | Yes (soft-prefer T2 ships first) | Per-tier gating + `[PRECEDENT: owner/repo@path]` tagging discipline; classifier widening only after Heavyweight passes pilot | Precedent tagging propagates through synthesis/assembly/QA; rf-qa-qualitative spot-checks precedents via `githubGetFileContent` |

---

## Dependency Graph

```
                    Phase 0: install_mcp.py
                            │
              ┌──────┬──────┼──────┬──────┐
              ▼      ▼      ▼      ▼      ▼
            T1     T2     T4     T5     (T6 prefers T2 ship first)
       deep-rsrch tech-rs brstrm trbsht
        agent     Phase 4 Wave2A   PR-arch
              │      │
              │      └──────► T6 (/tdd Phase 4 mirrors T2 + adds Stage A)
              │
              ▼
            T3 /sc:research --source
```

**Dependency rules:**

- Targets #2, #4, #5 do NOT route through `deep-research`. They can ship independently after #0.
- Target #3 (`/sc:research`) delegates to `deep-research-agent` per its frontmatter `personas:` list. Best landed after #1.
- Target #1 is the highest-leverage single change (cascades to all consumers of `deep-research`).

---

## Per-Target Detail (Synthesized)

### Target #1: `deep-research` Agent → Candidate B (Behavioral Router)

**Why it's chosen:** The deep-research file's distinguishing strength is the rigor of its Tavily-first routing policy (`deep-research.md:30-47`). Candidate B uses that same rigor to defend against octocode's primary failure mode — overuse on conceptual ("best practices", "tutorial", "explain X") questions where Tavily/Context7 are strictly better.

**The diff:**

- 5 octocode tools added to frontmatter (`githubSearchCode`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure`, `packageSearch`)
- New "Backend routing by question shape" subsection with 6 positive shapes + 4 explicit anti-triggers
- New "Octocode failure handling" subsection mirroring Tavily-first rule structure (5 failure modes + `fallback_reason` annotations)
- `backend` enum in output contract grows to include `octocode`

**Single file, ~55 added lines, ~3 modified, 0 deleted.**

**Runner-up:** Candidate E (confidence-driven hybrid) — narrowly lost on operationalization difficulty, but composes naturally as a future v2 layer.

**Read more:** `brainstorm/01-deep-research-agent.md`

---

### Target #2: `tech-research` Phase 4 → W1-B + W1-F (Build-Time Routed Buckets)

**Why it's chosen:** Phase 4 of `tech-research` already names "GitHub issues and discussions, community solutions to similar problems" as research targets (SKILL.md:419), but the current prompt is tool-agnostic and falls back to Tavily by default. W1-B classifies each web-research topic at task-build time, neutralizing the LLM's natural fallback-to-familiar bias.

**The diff:**

- `rf-task-builder` classifies each Phase 4 web-research topic as `github-flavored` (use octocode) or `open-web` (use Tavily)
- Two prompt templates in SKILL.md: existing Web Research Agent Prompt for open-web + NEW GitHub Research Agent Prompt template (inserted after line 720)
- BUILD_REQUEST gains a classification block instructing the builder how to categorize topics
- Capability inheritance: Tavily-bucket agents can still reach `packageSearch` if needed (fallback path)

**~135 LoC across one file (SKILL.md), 1 PR, ~1 working day.**

**Runner-up:** W1-A (soft hint in current prompt) — too weak; LLM ignores hints when Tavily is familiar.

**Read more:** `brainstorm/02-tech-research-phase4.md`

---

### Target #3: `/sc:research` Command → `--source` Flag with Per-Backend Sections

**Why it's chosen:** This is the user-facing front door. Predictability matters more than cleverness. A `--source` flag gives users explicit control without surprising auto-routing, and the per-backend report sections preserve provenance (so users know which tool found what).

**The diff:**

- Add `--source` flag accepting `tavily` (default), `octocode`, `context7`, `all`, or comma-list
- Add `octocode` to `mcp-servers:` frontmatter
- Add "Source Selection" subsection documenting the flag
- Add "Findings by Backend" output convention — each finding tagged with `[octocode]` / `[tavily]` / `[context7]`
- Multi-source partial failure handling: emit report with "Sources Unavailable" callout
- Single-source hard-fail: show install/auth hints
- Anti-trigger callout when `--source octocode` is misused for local-repo questions

**~4h alone, ~7-10h risk-adjusted including prereqs.**

**Cross-target dependency:** Hard prereq on Target #1 — `/sc:research` delegates via `personas: [deep-research-agent]`, so the agent change must land first.

**Runner-up:** Candidate A (`--mode github`) — rejected because flag composes better than modes for future octocode-adjacent backends.

**Read more:** `brainstorm/03-sc-research-command.md`

---

### Target #4: `sc-brainstorm` Wave 2A → Strategy-Gated Routing (Candidate C + small A concession)

**Why it's chosen:** The brainstorm protocol's Wave 2A enrichment matrix is already designed for parallel, fail-open sources. Strategy-gating (only `enterprise` strategy OR `deep` depth) prevents context tax for quick/solo brainstorms while unlocking precedent-finding where it actually adds value.

**The diff:**

- New row in the SKILL.md:179-187 routing matrix for `domain in {code, architecture}` AND `strategy in {enterprise, default}`
- New `--precedent` opt-in flag (force on) and `--no-precedent` opt-out flag (force off)
- New `enrichment/precedent.md` artifact with YAML frontmatter (per Wave 2A artifact conventions)
- New `§Precedent enrichment` subsection in `refs/handoff-routing.md`
- Restrictive 4-tool whitelist: `packageSearch`, `githubSearchCode`, `githubSearchPullRequests`, `githubGetFileContent` — explicitly excludes LSP/local/clone
- 6 anti-trigger rules
- Quality-tier semantics: octocode failure degrades gracefully per existing Wave 2A `fail-open` invariant

**~5.5h, single-PR, declarative-only changes.**

**Cross-target dependency:** Hard prereq is only #0 (MCP registration). Independent of #1, #2, #3, #5. Ships standalone.

**Runner-up:** Candidate A (always-on matrix row) — rejected because quick brainstorms shouldn't pay for cross-repo research.

**Read more:** `brainstorm/04-sc-brainstorm-wave2a.md`

---

### Target #6: `/tdd` Skill → A + H + F-as-rollout-gate (added after validate/refute follow-up)

**Why it's chosen:** The validate/refute follow-up identified `/tdd` as a strong fit missed in the original analysis. The brainstorm winner combines **three candidates**: A (mirror T2's W1-B build-time routed buckets in Phase 4) + H (NEW Stage A PRD→octocode precedent discovery, before codebase Phase 2) + F (tier-gate to Heavyweight only as Phase 1 rollout, classifier widening to Standard after pilot passes).

**Why it diverges from T2 (an explicit justification, not an oversight):**

- **`/tdd` has a unique PRD ingestion path** — Stage A precedent discovery (Candidate H) leverages this; tech-research has no equivalent
- **TDDs are normative engineering specs** (vs tech-research's informative reports), warranting stricter `[PRECEDENT: owner/repo@path]` tagging discipline that propagates through synthesis/assembly/QA
- **`/tdd`'s agent prompts live in `refs/agent-prompts.md`** (not inline like tech-research's SKILL.md) — the diff shape differs from T2 even when the routing pattern is the same

**The diff:**

- Mirror T2's `rf-task-builder` classification block to route Phase 4 web research topics to `github-flavored` (octocode) vs `open-web` (Tavily)
- Add NEW Stage A precedent discovery pass when PRD is present (single octocode `githubSearchCode` + `packageSearch` call) — output feeds Phase 2 codebase research as scoping context
- Add `[PRECEDENT: owner/repo@path]` tagging convention through synthesis files and final TDD
- `rf-qa-qualitative` spot-checks 2-3 precedents per Heavyweight TDD via `githubGetFileContent` (hallucination safeguard)
- Tier-gate Phase 1 to Heavyweight only; Phase 2 widens to Standard after pilot data shows precedent quality holds

**~180 LoC across 4 files (SKILL.md, refs/agent-prompts.md, refs/qa-prompts.md, examples/tdd_template.md), 1 PR, ~1 working day.**

**Cross-target dependency:** No hard dependency on T1. **Soft prefer T2 ships first** so the build-time classifier pattern is proven once before /tdd inherits it.

**Runner-up:** Candidate F alone (tier-gated, no Stage A precedent) — lost because it left the highest-value use case (PRD-driven precedent discovery) on the table.

**Read more:** `brainstorm/06-tdd-skill.md`

---

### Target #5: `/sc:troubleshoot` → Hybrid C+A (Tier 1 packageSearch + Tier 2 precedent-finder agent)

**Why it's chosen:** Troubleshoot reports get acted on, so hallucination safeguards are critical. The hybrid design uses Tier 1 for cheap fast-path package metadata (one `packageSearch` call when symptom names a third-party package), and Tier 2 for deeper PR archaeology only when error type is one of `bug | build | test`. Precedent is explicitly NOT treated as evidence — it's advisory context appended to fix proposals.

**The diff:**

- **Tier 1:** Conditional `packageSearch` call at Wave 1 step 1, gated on third-party-package-name signal in the symptom (or `--package` flag). Metadata flows into `root-cause-analyst` brief in Wave 1.7.
- **Tier 2:** New `precedent-finder` agent added to Wave 3 for `--type ∈ {bug, build, test}`. Uses `githubSearchPullRequests` + `githubSearchCode` + `githubGetFileContent`. Produces a **Precedent Card** that appends to each `fix-<N>.md` in Wave 4 as advisory context.
- Tavily reduced from 2 → 1 queries per invocation (keeps Stack Overflow / Discourse long-tail); octocode takes the freed slot for GitHub-native PR archaeology
- Precedent ≠ Evidence: separate report section; `evidence-validator` excluded from precedent validation
- Precedents carry mandatory permalinks + quoted excerpts + similarity scores + star/age thresholds
- Type-gated: perf / deploy / security skip octocode (precedent rarely transfers)

**~500 LoC, ~9.5h, one focused engineering day.**

**Cross-target dependency:** Troubleshoot does NOT route through `deep-research`, so this is independent of #1. Only shared prereq is #0.

**Runner-up:** Candidate G (always-on precedent feed) — tied with hybrid on score, lost on rationale: Wave 4 debate benefits from structured precedent interpretation, not just link lists.

**Read more:** `brainstorm/05-sc-troubleshoot-command.md`

---

## Recommended Adoption Roadmap

```
Week 0:    Phase 0 — install_mcp.py registration (~1h)
           Pinned octocode-mcp@14.2.0, LOG=false, TOOLS_TO_RUN whitelist
           ENABLE_LOCAL=false, ENABLE_CLONE=false

Week 1:    Phase 1 — Target #1 deep-research agent (~3-4h)
           Highest leverage single change; cascades to all consumers

Week 2:    Phase 2 — Targets #2, #4, #5 in parallel (3 PRs)
           Independent ships; can be split across team members
           T2: ~1 day, T4: ~5.5h, T5: ~9.5h

Week 3-4:  Phase 1 + Phase 2 PILOT (8 weeks accumulated experience)
           Measure: octocode invocation rate, hallucination count,
           context tax, user-visible quality improvement

Week 5:    Phase 3 — Target #3 /sc:research command (~4h)
           Best landed after T1 settles; user-facing surface is highest visibility

Week 6+:   PILOT all 5 targets together; gather data for Phase 4 (#3 brainstorm v1's "behavioral router" upgrade) only if metrics justify
```

**Total scope if all 5 adopted:** ~25-30 engineering hours, 6 PRs, ~5 weeks of calendar time with pilot gates.

**With T6 added:** ~33-38 engineering hours, 7 PRs (Phase 0 + T1 + T2 + T4 + T5 + T6 + T3). T6 ships in Phase 2.5 (after T2 settles).

---

## Common Risk Mitigations (Apply to All 5 Targets)

Independent of which target is being implemented, these mitigations apply uniformly (they're encoded in Phase 0 + carry through):

| Risk | Mitigation |
|---|---|
| Single-maintainer / supply chain | Pin `octocode-mcp@14.2.0` exactly; never `@latest` |
| Telemetry leakage of research goals | Set `LOG=false` in install env |
| 14-tool context bloat | Restrict to 5 cross-repo tools via `TOOLS_TO_RUN` whitelist; disable LSP/local via `ENABLE_LOCAL=false` |
| Local-tool overlap with auggie/serena/Read | `ENABLE_LOCAL=false` + anti-trigger rules in each target's policy |
| GitHub Search API 30 req/min rate limit | Per-agent caps + Tavily fallback + `fallback_reason` annotations |
| Broad GitHub token scope | Document the `repo`+`read:user`+`read:org` requirements; recommend `gh auth login` reuse |
| Octocode unavailability | Each target has fail-open semantics; Targets #2 and #4 explicitly fail to Tavily / quality-tier degrade |

---

## What This Investigation Did NOT Cover

These remain as future work, same as v1:

1. **Live MCP introspection** — no actual `octocode-mcp@14.2.0` install + `tools/list` dump
2. **Empirical context-tax measurement** — pilot phase first
3. **Cross-model determinism** — pilot phase
4. **Long-term breakage probability** — 194 npm versions in <12 months remains a stress point
5. **Skills marketplace overlap** — IronClaude's 24 skills not exhaustively mapped against octocode's 19 skills

Additionally, v2 specific gaps:

6. **Cross-target token-tax interaction** — if all 5 ship, the cumulative context tax across an end-to-end task (e.g., `/sc:research → tech-research → brainstorm`) may double-count octocode schema loads. Need to validate during pilot.
7. **`/sc:troubleshoot` precedent vs evidence boundary** — the "precedent ≠ evidence" contract from T5 is novel for the framework. Needs explicit `evidence-validator` opt-out logic that hasn't been designed.

---

## Evidence Trail

### Stage 1 — Research

| File | Status |
|---|---|
| `research/web-01-octocode-tools-architecture.md` | Complete (341 lines) |
| `research/web-02-octocode-strengths.md` | Complete (193 lines) |
| `research/web-03-octocode-weaknesses.md` | Complete (155 lines) |
| `research/web-04-octocode-skills-marketplace.md` | **FAILED (agent stalled 600s)** |
| `research/01-existing-tooling-overlap.md` | **STUB** — covered by web-03 + code-02 |
| `research/02-integration-points.md` | Complete (236 lines) |

### Stage 2 — Analysis

| File | Status |
|---|---|
| `octocode-research.md` | Complete (250 lines) |
| `octocode-fit-analysis.md` | Complete (229 lines) |
| `top-5-targets.md` | Complete (v2 selection) |

### Stage 3 v2 — Per-Target Brainstorms

| File | Target | Lines | Recommended Design |
|---|---|---|---|
| `brainstorm/01-deep-research-agent.md` | `deep-research` agent | 481 | Behavioral router (Candidate B) |
| `brainstorm/02-tech-research-phase4.md` | `tech-research` Phase 4 | 598 | Routed buckets at build time (W1-B+W1-F) |
| `brainstorm/03-sc-research-command.md` | `/sc:research` command | 666 | `--source` flag + per-backend sections |
| `brainstorm/04-sc-brainstorm-wave2a.md` | `sc-brainstorm` Wave 2A | 715 | Strategy-gated + `--precedent` flag (Candidate C+A) |
| `brainstorm/05-sc-troubleshoot-command.md` | `/sc:troubleshoot` | 585 | Hybrid Tier 1 packageSearch + Tier 2 precedent-finder (C+A) |
| `brainstorm/06-tdd-skill.md` | `/tdd` skill | 510 | A+H+F: T2-mirrored Phase 4 routing + Stage A PRD-precedent + Heavyweight-first rollout |

### Stage 3 v1 — Preserved for Reference

| File | Status |
|---|---|
| `brainstorm-v1-lenses-on-deep-research/01-declarative-purist.md` | v1: declarative lens on deep-research |
| `brainstorm-v1-lenses-on-deep-research/02-behavioral-router.md` | v1: routing lens on deep-research |
| `brainstorm-v1-lenses-on-deep-research/03-persona-aware.md` | v1: persona lens on deep-research |
| `brainstorm-v1-lenses-on-deep-research/04-hook-driven.md` | v1: hook lens on deep-research |
| `brainstorm-v1-lenses-on-deep-research/05-sub-agent-delegate.md` | v1: delegation lens on deep-research |
| `brainstorm-v1-lenses-on-deep-research/06-skill-level.md` | v1: skill-level lens (alternate path) |
| `FINAL-RECOMMENDATIONS.md` | v1: 6-lens synthesis (declarative + sub-agent staged) |

---

## Next Actions

If the recommendation is accepted:

1. Open **Phase 0 PR** — MCP registration in `install_mcp.py`
2. Open **Phase 1 PR** — Target #1 deep-research agent (Candidate B router)
3. After Phase 1 merges, fan out **Phase 2 PRs** (Targets #2, #4, #5) — these can be parallel across team members
4. Configure pilot instrumentation (token counter, transcript reviewer, octocode-invocation logger)
5. After 4-week pilot of Phases 1-2, open **Phase 3 PR** for Target #3 (`/sc:research --source` flag)
6. After 8 weeks of full integration, retrospect on cross-target token-tax interaction (gap #6 above)

If a partial recommendation is preferred:

- **Minimum viable** = Phase 0 + Phase 1 only (~5h total). Gives octocode access to the workhorse agent.
- **Maximum-leverage subset** = Phase 0 + Phase 1 + Target #4 (sc-brainstorm Wave 2A). Adds high-value precedent-finding to the most innovation-heavy workflow.
- **Highest-visibility subset** = Phase 0 + Phase 1 + Target #3 (`/sc:research`). Gives users a direct flag to opt into octocode.

---

**Status:** Complete
**Investigation ID:** TASK-RESEARCH-20260530-044428
**Duration (Stage 3 v2 only):** ~6 minutes setup + ~5-7 min parallel execution + ~3 min synthesis
**v2 agents spawned:** 5 (all successful)
**v1 vs v2:** Both available — v1 explored DEPTH on the single highest-leverage target; v2 explored BREADTH across the top 5. Adoption can draw from both.
