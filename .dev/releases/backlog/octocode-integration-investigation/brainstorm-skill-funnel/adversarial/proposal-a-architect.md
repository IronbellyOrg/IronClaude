# Proposal A — Architect Lens

**Persona:** architect
**Model:** opus
**Status:** Complete
---

## Design Thesis

Octocode is an **external dependency** with three properties that make it a poor candidate for direct embedding in caller skills: (1) a churning tool surface (194 npm versions in <12 months) that makes every direct caller a future break-point; (2) operational hazards (30 req/min rate limit, telemetry, supply-chain risk) that must be enforced at exactly **one** place to be enforced at all; (3) a *funnel discipline* (DISCOVER → SEARCH → LOCATE → READ) that is encoded in prompt text, not the protocol — so every caller that talks to octocode directly either re-implements the discipline or violates it. The architect lens therefore demands an **anti-corruption layer** around octocode: a single skill whose entire purpose is to translate the framework's domain language ("investigate this codebase, this area, for this reason") into octocode's tool language, and translate octocode's response shape back into evidence-tagged findings the framework already knows how to consume. Callers never touch octocode tools, never see octocode error codes, never load octocode schemas. The skill is the contract; the contract is the only coupling point; coupling shrinks from 6 surfaces to 1.

## Skill Name + Purpose

**Name:** `cross-repo-investigation`

**Purpose:** Given a scoped investigation request (target repos/packages + focus areas + question shape), produce an evidence-tagged findings pack using cross-repository GitHub/GitLab/Bitbucket research, while fully encapsulating octocode-mcp as an implementation detail.

**Why this name (not `octocode-deep-dive`):**

- **No vendor name in the public surface.** If octocode is later replaced by GitHub's official MCP, a homegrown `gh` wrapper, or a Sourcegraph integration, only the skill's internals change — the caller-facing skill name and contract stay stable. Naming a skill `octocode-*` would embed a single-vendor dependency in 6 caller files; the name itself becomes coupling.
- **`cross-repo`** is the *capability* the framework needs (cross-repository pattern research), distinct from auggie (local semantic), serena (local symbol), Context7 (canonical docs), and Tavily (open web). The name describes what callers get, not how it's delivered.
- **`investigation`** echoes `tech-research`'s vocabulary and signals it's a downstream specialist, not a peer top-level skill. It is intentionally invoked, not auto-triggered on phrases like "GitHub" or "open source."

## Skill Architecture

### Phase structure

**Hybrid — single-phase by default, lightweight task file only in `deep` mode.** The skill has two execution modes selected by the caller via the input contract:

- **`mode: inline` (default)** — single agent invocation, no MDTM task file, synchronous return. Used by `tech-research` Phase 4 sub-agents, `sc-brainstorm` Wave 2A enrichment, `/sc:troubleshoot` Tier 2 precedent-finder. Budget: ≤ 12 octocode calls per invocation; returns Markdown findings block + JSON sidecar.
- **`mode: task` (opt-in)** — MDTM task file under the caller's task directory, multi-phase pipeline (Scope → Discover → Search → Locate → Read → Synthesize), survives context compression. Used only when the caller is itself a long-running MDTM skill (e.g., `tech-research` calling the skill from its own Phase 4 as a sub-task, or `/tdd` Stage A). Budget: ≤ 20 octocode calls per task, suspendable + resumable.

The inline mode is the **hot path** (it's what 90% of callers actually need); the task mode exists because skills that already have MDTM machinery should be able to fold cross-repo work into the same checklist discipline rather than spawning a parallel state model.

### Input contract

A single YAML block. Required fields are minimal; optional fields are how callers express scope without forcing the skill to free-form search.

```yaml
CROSS_REPO_INVESTIGATION:
  # --- required ---
  question: "<one sentence — what we want to learn>"
  question_shape: package_internals | api_usage | pattern_discovery | pr_archaeology | comparative
  caller: "<skill or command id — e.g. tech-research:phase-4, sc-troubleshoot:tier-2, tdd:stage-a>"

  # --- scoping (at least one must be non-empty unless question_shape=pattern_discovery) ---
  candidate_repos: ["owner/repo", ...]      # if known from upstream (e.g. tech-research Phase 2)
  candidate_packages: ["pkg-name", ...]     # if starting from a dependency
  focus_areas: ["<topic>", ...]              # e.g. ["retry logic", "exponential backoff"] — narrows search queries

  # --- output shaping (optional, with defaults) ---
  mode: inline | task                        # default: inline
  max_evidence: 5                            # default: 5; cap: 10
  verbosity: compact | verbose               # default: compact
  output_path: "<absolute path>"             # default: returned inline; if set, written to disk and path returned

  # --- caller context (helps the skill stay on-target) ---
  parent_context: |
    <2-4 sentence paragraph — what is the caller trying to accomplish, what
     have they already learned, what are they NOT asking us to do>
```

Two contract invariants the skill enforces (returns `INVALID_REQUEST` if violated):

1. **No local-codebase questions.** `question` must not name local paths, local symbols, or "this codebase." Callers needing local work use auggie/serena/Read directly — the skill rejects to prevent overlap drift.
2. **No canonical-docs questions.** `question` must not be answerable from official maintainer documentation. Callers needing canonical API references use Context7 — the skill rejects to prevent it becoming a slow Context7 proxy.

These rejections are the *anti-corruption layer's* primary value: they teach the framework, by rejection, where octocode actually belongs.

### Output contract

```yaml
CROSS_REPO_INVESTIGATION_RESULT:
  status: OK | PARTIAL | NO_EVIDENCE | INVALID_REQUEST | RATE_LIMITED | UNAVAILABLE | CLARIFY_NEEDED
  question: "<verbatim from input>"
  caller: "<verbatim from input>"
  calls_used: <N>
  calls_cap: <N>
  repos_investigated: ["owner/repo@sha", ...]
  findings: # zero or more
    - claim: "<one-sentence claim>"
      tag: "[PRECEDENT: owner/repo@path]"     # canonical evidence tag (per T6's convention)
      repo: "owner/repo"
      ref: "<sha>"
      path: "<file-path>"
      lines: [A, B]
      permalink: "https://github.com/.../blob/<sha>/.../#LA-LB"
      excerpt: |
        <minimal code excerpt, ≤20 lines>
      why_evidence: "<one sentence>"
  synthesis: "<2-4 sentences, only if findings ≥ 3>"
  gaps: ["<known unknown>", ...]
  fallback_hint: "tavily" | "context7" | "auggie" | null  # set when status ∈ {INVALID_REQUEST, UNAVAILABLE, RATE_LIMITED}
  provenance: # for audit + the RDD discipline
    - tool: "githubSearchCode"
      research_goal: "<verbatim>"
      hits: <N>
```

Two return shapes: the YAML above for programmatic consumers (CLI pipelines, MDTM checklists), and a rendered Markdown block for LLM consumers (deep-research agent, brainstorm Wave 2A) — the Markdown is a deterministic projection of the YAML, generated by the skill, never authored independently. **One contract, two renderings**: this is what keeps the surface stable as callers proliferate.

### Tool whitelist

Only these 5 octocode tools are exposed inside the skill. The skill's `SKILL.md` frontmatter declares them; nothing else in the framework names them.

| Tool | Funnel role | Why included |
|---|---|---|
| `mcp__octocode__githubSearchCode` | SEARCH | Core cross-repo capability |
| `mcp__octocode__githubSearchRepositories` | DISCOVER | When `candidate_repos` empty |
| `mcp__octocode__githubSearchPullRequests` | SEARCH (archaeology) | Only loaded when `question_shape=pr_archaeology` |
| `mcp__octocode__githubGetFileContent` | READ | Targeted partial reads only (charOffset/charLength enforced) |
| `mcp__octocode__githubViewRepoStructure` | LOCATE | Cheap orientation between SEARCH and READ |
| `mcp__octocode__packageSearch` | DISCOVER | When `candidate_packages` non-empty |

**Explicitly excluded:** all `local*` tools (redundant with auggie/serena/Read), all `lsp*` tools (redundant with serena, language-gap risk), `githubCloneRepo` (no need for disk clones — partial reads suffice; also avoids disk-cache cleanup obligation).

This whitelist is the **only place in the framework** that names octocode tools. T1-T6 (v2 distributed plan) named these tools in 6 separate files; this plan names them once.

### State model

- **`mode: inline`** is stateless from the caller's perspective. The skill runs, returns, exits. Octocode's own 24h disk cache at `~/.octocode/repos/` is transparent infrastructure (not skill state).
- **`mode: task`** is stateful via the caller-provided `output_path` and an MDTM task file inside that path. Resumability follows the same convention as `tech-research`: re-read the task file, find the first unchecked `- [ ]`, resume. The skill's task file is conceptually a child of the caller's task file — callers add a single checklist item like `- [ ] Cross-repo investigation: <task-id>` and the skill produces a self-contained sub-task underneath.

### Caller-facing API surface

Callers do exactly one thing: spawn a `Task` subagent of type `cross-repo-investigation` with the input YAML in the prompt. They never:

- Load octocode tools in their own frontmatter
- Reference octocode error codes
- Implement rate-limit handling
- Maintain their own tool whitelists
- Configure telemetry

The skill is invoked. The skill returns. The caller consumes findings and continues. That's the entire surface.

## Coupling Discipline

### How the skill avoids leaking octocode-isms to callers

- **No vendor names in the public contract.** Input/output contracts use framework vocabulary (`question_shape`, `candidate_repos`, `[PRECEDENT: ...]`). Words like "octocode," "researchGoal," "verbosity" appear only in `provenance` (an audit-only field most callers will ignore).
- **No vendor error codes.** Octocode returns HTTP 403 on rate-limit; the skill translates to `status: RATE_LIMITED`. Octocode returns MCP-level errors when the server is unreachable; the skill translates to `status: UNAVAILABLE`. The vendor's error shape is internal.
- **No funnel discipline in caller prompts.** The DISCOVER → SEARCH → LOCATE → READ flow lives in the skill's system prompt only. Callers don't know it exists; they just send a `question` and `question_shape`.
- **No `LOG=false` enforcement in callers.** The skill's `SKILL.md` documents the install-side env var requirement; callers don't (and shouldn't) reference telemetry.

### What changes when octocode adds new tools or breaks API

- **New tool added in octocode 15.x:** evaluate inside the skill's `refs/octocode-tool-eval.md` (a private reference doc). If we adopt it, add to the whitelist in `SKILL.md` frontmatter and update the funnel docs. **Zero changes to any caller skill.**
- **Breaking change in an existing tool's response shape:** update the skill's response-parsing logic (in `refs/response-parsers.md` plus the system prompt rules). The output contract — the YAML the skill emits — stays stable. **Zero changes to any caller skill.**
- **Octocode deprecates a tool we use:** remove it from the whitelist, fall back to other tools (e.g., if `packageSearch` is deprecated, use `githubSearchRepositories` with package-name keyword). The skill may return more `NO_EVIDENCE` results, but the caller contract doesn't change.
- **Octocode disappears entirely (maintainer abandons project):** the skill returns `status: UNAVAILABLE` with `fallback_hint: tavily` on every call. Callers already have fallback logic for `UNAVAILABLE`. The skill itself can be retired or rewritten against a different cross-repo MCP (GitHub's official MCP, Sourcegraph, a homegrown `gh search` wrapper). **The contract is the abstraction — the implementation is replaceable.**

### What happens when callers want capabilities the skill doesn't expose

A caller wanting, e.g., LSP call-hierarchy across a remote repo has three options:

1. **Add it to the skill** if the capability is generally useful (≥3 plausible callers). PR shape: extend `question_shape` enum, add to the whitelist, document in `SKILL.md`. The contract grows, doesn't fragment.
2. **Use the right tool directly** if the capability is local or canonical (serena for symbols, Context7 for docs). The skill's `INVALID_REQUEST` response with `fallback_hint` actively teaches this.
3. **Build a peer skill** if the capability is genuinely a different domain (e.g., GitLab API admin operations). Cross-repo investigation stays focused; new domains get new skills.

The architect lens accepts that some callers will be frustrated by the contract. That frustration is the price of stability. If we let every caller add its own octocode tool list because "the contract doesn't cover my edge case," we end up where v2 was: 6 distributed integration points and no coherent enforcement.

### Extension model

Future callers add new use cases by:

1. Adding a new `question_shape` value if their use case doesn't fit existing shapes. PR touches `SKILL.md` (enum + prompt branch) + caller's invocation site. No new tools, no new files.
2. Subclassing the input contract via `parent_context` for caller-specific framing — the system prompt is designed to read `parent_context` as guidance, not directive, so callers can shape behavior without contract changes.
3. Adding a new `mode` value if their state model genuinely differs (e.g., `mode: streaming` for a future SSE consumer). High bar — most callers fit `inline` or `task`.

## File Structure

```
src/superclaude/skills/cross-repo-investigation/
├── SKILL.md                          # ~300 lines: frontmatter (5 tools), purpose, contract, examples, anti-triggers
├── refs/
│   ├── input-contract.md             # ~120 lines: full YAML schema spec, every field, examples per question_shape
│   ├── output-contract.md            # ~80 lines: YAML output schema + Markdown rendering rules
│   ├── funnel-discipline.md          # ~90 lines: DISCOVER → SEARCH → LOCATE → READ rules, when to skip stages
│   ├── question-shapes.md            # ~110 lines: 5 question_shape values, when each fires, anti-triggers
│   ├── failure-codes.md              # ~70 lines: 7 status codes, what each means, what the caller should do
│   └── octocode-tool-eval.md         # ~60 lines: private — when to add/remove tools from the whitelist
├── rules/
│   ├── caller-rules.md               # ~50 lines: rules CALLERS follow when invoking the skill
│   └── internal-rules.md             # ~80 lines: rules the SKILL follows (rate-limit, RDD, citation, no-hallucination)
├── templates/
│   ├── inline-result.md.j2           # rendered Markdown for inline mode
│   └── task-mode-checklist.md.j2     # MDTM checklist seed for task mode
└── examples/
    ├── tech-research-phase4.yaml     # input + expected output for canonical Phase 4 use
    ├── troubleshoot-tier2.yaml       # input + expected output for PR archaeology
    └── tdd-stage-a.yaml              # input + expected output for PRD-precedent discovery
```

**Total skill footprint: ~960 LoC across 11 files** (one skill package, one contract, one source of truth).

**Versus v2 distributed (~510 LoC across 6 files):** larger absolute LoC, but it's **all in one place**. The v2 LoC was spread across 6 SKILL.md files in 6 different skills — every future octocode-related change touched all 6. This skill's 960 LoC live in one directory; future changes touch one directory.

## Concrete Caller Examples

### Example 1 — `tech-research` Phase 4

**Today's tech-research SKILL.md Phase 4** (the Web Research phase) spawns `rf-web-researcher` subagents that call Tavily directly. With this skill, Phase 4 routes any subagent whose `topic_classification == "github-flavored"` to invoke `cross-repo-investigation` instead.

**What tech-research's SKILL.md changes to:**

Replace the existing Phase 4 agent-prompt template's tool-selection block with:

```markdown
### Phase 4 — Web Research

For each web-research topic in the task file:

1. Read the topic's `classification` field set by rf-task-builder:
   - `github-flavored` → spawn `rf-web-researcher` with `BACKEND: cross-repo-investigation`
   - `open-web` → spawn `rf-web-researcher` with `BACKEND: tavily` (current path)

When BACKEND is `cross-repo-investigation`, the subagent's task is solely to
construct the input YAML and invoke the skill via Task tool. The subagent does
NOT call octocode tools directly — it does not have them in its tool list.

Input YAML construction:

CROSS_REPO_INVESTIGATION:
  question: "<topic.question verbatim>"
  question_shape: <derived from topic.intent: pattern_discovery | api_usage | ...>
  caller: "tech-research:phase-4"
  candidate_repos: <topic.candidate_repos from Phase 2 scope discovery, or []>
  candidate_packages: <topic.candidate_packages, or []>
  focus_areas: <topic.focus_areas from task file>
  mode: inline
  max_evidence: 5
  parent_context: |
    Investigation: <task.investigation_name>
    Phase 2 surfaced these external dependencies: <list>.
    This topic asks <topic.why>. Findings will be merged into the
    cross-repo evidence section of the final research report.

Consume the returned `findings` array; append each to
${RESEARCH}/web-<NN>-<topic-slug>.md with [PRECEDENT: ...] tags intact.
On status ∈ {RATE_LIMITED, UNAVAILABLE}, fall back to Tavily for the topic
per the existing open-web path; note the fallback in the file's frontmatter.
```

**What tech-research's frontmatter changes to:** nothing. tech-research doesn't load octocode tools. tech-research doesn't know about octocode.

**What the new skill receives:** the YAML above.

**What it returns:** the YAML output contract, deserialized by tech-research's Phase 4 consumer into the existing `web-<NN>.md` artifact shape.

**Net change in tech-research SKILL.md:** ~40 LoC modified, 0 LoC added for tool whitelists, 0 LoC added for failure-mode handling.

---

### Example 2 — `/sc:troubleshoot` (PR archaeology Tier 2)

**Today's /sc:troubleshoot:** Tier 2 spawns parallel hypothesis agents. Per v2 plan, a new `precedent-finder` agent would directly load 3 octocode tools and implement its own rate-limit handling, citation discipline, and Precedent Card rendering — ~500 LoC in a new agent file.

**With this skill:** the `precedent-finder` agent doesn't exist. The Tier 2 orchestrator invokes `cross-repo-investigation` directly when `--type ∈ {bug, build, test}`:

```yaml
CROSS_REPO_INVESTIGATION:
  question: "Find merged PRs across public repos that fix this error pattern: '${error_signature}'"
  question_shape: pr_archaeology
  caller: "sc-troubleshoot:tier-2"
  candidate_repos: ["${detected_third_party_repo}"]  # if symptom names a package
  candidate_packages: ["${detected_package}"]
  focus_areas: ["${error_signature_tokens}"]
  mode: inline
  max_evidence: 3
  verbosity: compact
  parent_context: |
    Troubleshooting: ${symptom_summary}
    Error type: ${type}
    Already-investigated local hypotheses: ${tier1_summary}
    These findings will be appended to each fix-<N>.md as a "Precedent Card"
    advisory section — NOT treated as evidence by evidence-validator.
```

**What /sc:troubleshoot's command file changes to:** ~25 LoC — the input YAML construction + a 5-line Tier 2 branch that calls the skill. No agent file. No precedent-finder. No tool list. The "precedent ≠ evidence" boundary (v2 T5's novel contract) is enforced by the **caller's render logic** (it labels the result block "Precedent Card" and excludes it from `evidence-validator`), not by a new agent's prompt.

**What the skill returns:** same YAML output contract; the `findings` array becomes the Precedent Card rows.

**Versus v2 T5's ~500 LoC + new agent + new fallback logic + new tool whitelist:** this is ~25 LoC + reuse the skill.

---

### Example 3 — `/tdd` Phase 4 + Stage A

**Today's /tdd:** Phase 4 generates architecture/integration sections from codebase + Tavily. Per v2 T6, Phase 4 would be modified analogously to tech-research's Phase 4, and a NEW Stage A (PRD → octocode precedent discovery) would be added before Phase 2.

**With this skill:** Both modifications collapse into invocations of `cross-repo-investigation`. Stage A becomes a single Task spawn:

```yaml
CROSS_REPO_INVESTIGATION:
  question: "Find 3-5 production reference implementations of the architecture described in this PRD"
  question_shape: pattern_discovery
  caller: "tdd:stage-a"
  candidate_repos: []                    # discovery mode
  candidate_packages: <from PRD's "Dependencies" section, if present>
  focus_areas: <PRD's "Architecture" section's top-level component names>
  mode: inline
  max_evidence: 4
  verbosity: verbose                     # TDD wants more context
  parent_context: |
    TDD draft for: <prd.title>
    PRD scope: <prd.summary, 2-3 sentences>
    Phase 2 codebase research will use these precedents as scoping context.
    Tag every finding with [PRECEDENT: owner/repo@path] for downstream
    rf-qa-qualitative spot-checks.
```

Phase 4 of /tdd then invokes the same skill for each `github-flavored` web-research topic, exactly as tech-research does — the two skills converge on a single integration pattern instead of independently re-implementing it.

**What /tdd's SKILL.md + refs/agent-prompts.md changes to:** ~60 LoC for Stage A (mostly the YAML construction + Phase 2 hand-off wiring) + ~30 LoC for Phase 4 routing. **No tool whitelist. No failure-mode table. No rate-limit logic.** All of that lives in `cross-repo-investigation`.

**The `[PRECEDENT: ...]` tagging convention** (v2 T6's headline discipline): it's the skill's output contract's `tag` field. Every caller gets tagged precedents *for free* — the tagging is not per-caller code, it's the contract.

## Comparison to v2 Distributed Plan

| Dimension | v2 Distributed | This proposal |
|---|---|---|
| **Files touched per change** | 6 SKILL.md / agent files | 1 skill directory |
| **Total LoC at steady state** | ~510 LoC across 6 files | ~960 LoC in 1 skill |
| **Net caller LoC** | ~510 LoC (all of it is caller LoC) | ~150 LoC across all 6 caller integrations |
| **Tool whitelist locations** | 6 (one per integration) | 1 (skill frontmatter) |
| **Rate-limit handlers** | 6 (each integration implements its own) | 1 (skill's internal rules) |
| **Failure-mode tables** | 6 (with subtle drift over time) | 1 (skill's `refs/failure-codes.md`) |
| **`[PRECEDENT: ...]` tagging discipline** | Defined in T6, must be replicated by T1, T2, T4, T5 | Built into output contract; free for all callers |
| **Telemetry config (`LOG=false`)** | Documented in install + repeated in each integration's risk notes | Single `SKILL.md` block; install enforces |
| **Funnel discipline enforcement** | Either repeated in each caller's prompt or omitted (likely omitted under deadline pressure) | Enforced in skill's system prompt; callers don't know it exists |
| **Octocode version change impact** | Touches 6 files; risk of partial migration | Touches skill internals; contract unchanged |
| **Octocode removal cost** | Revert 6 PRs; clean up 6 places | Deprecate 1 skill; callers see `UNAVAILABLE` and fall back |

### Net LoC delta

- **v2:** ~510 LoC of integration code distributed across 6 caller files. Each future octocode change adds LoC to each file.
- **This proposal:** ~960 LoC for the skill itself + ~150 LoC of caller integrations = **~1,110 LoC total at adoption**.

Larger absolute LoC. But: **the v2 number is the LoC slope, not the intercept.** Every future octocode tool addition or response-shape change increments v2's count by 6×. This proposal's count increments by 1× per change. The break-even point is roughly the first significant octocode upgrade — after which this proposal is permanently cheaper.

### Coupling delta

- **v2:** 6 caller skills are directly coupled to octocode-mcp's tool schemas, response shapes, and failure modes. Coupling cardinality = 6 × N (N = number of octocode surface concerns).
- **This proposal:** 1 skill coupled to octocode; 6 callers coupled to 1 stable skill contract. Coupling cardinality = 6 × 1 + 1 × N.

The skill is an **anti-corruption layer** in the Evans/DDD sense. Callers speak framework language (`question_shape`, `[PRECEDENT: ...]`); the skill translates to vendor language (`searchCode` params, `researchGoal`, `charOffset`).

### Maintenance delta

- **v2:** A bug in rate-limit handling means 6 places to fix, 6 places to test, 6 PRs to ship the fix. Subtle drift between integrations becomes the steady state.
- **This proposal:** One place. One PR. One test suite.

### Failure-mode delta

- **v2:** Distributed graceful degradation — each integration fails independently. **But:** each integration's *quality* of degradation is independent too. T2 might fall back to Tavily; T4 might fail-open silently; T5 might hard-fail. Users see inconsistent behavior across surfaces.
- **This proposal:** Single point of failure — if the skill breaks (bug, octocode incompatibility), every caller sees `UNAVAILABLE`. But: **all callers get the same fallback behavior, the same audit trail, and the same `fallback_hint` field.** Single point of failure for the skill itself is acceptable; the skill's fallback path is the consistent UX across all callers.

The architect lens accepts higher correlation of failures in exchange for guaranteed consistency of failure handling. A single, well-tested skill is more reliable than 6 lightly-tested integrations.

## Trade-offs You Accept

1. **Higher absolute LoC at adoption (~1,110 vs ~510).** Justified by lower marginal LoC for future octocode changes and by the consolidation of operational discipline. The architect lens explicitly trades day-1 LoC for day-180 maintenance LoC.

2. **Per-invocation latency overhead (~3-5s).** Spawning a `Task` subagent has setup cost (per v1 sub-agent-delegate brainstorm §Cons). Some hot paths (e.g., a Tier 2 troubleshoot run already paying for parallel hypothesis agents) absorb this fine; some don't. The architect lens accepts the latency in exchange for context-tax isolation and contract stability. Callers needing <1s GitHub lookups should use `gh` directly (the skill's `INVALID_REQUEST` rejection actively redirects them).

3. **One more skill in the framework (24 → 25).** Marginal cost. The framework already has 24 skills; the marginal cost of a 25th well-scoped skill is low. The benefit is centralization.

4. **Single point of failure for cross-repo work.** A skill bug breaks all cross-repo investigation across the framework simultaneously. Mitigated by: (a) the skill's contract is small and stable, so the bug surface is small; (b) every caller's fallback path (`UNAVAILABLE` → Tavily) is exercised regularly and tested; (c) the skill is the only thing that needs CI coverage for cross-repo behavior, so test budget concentrates instead of dilutes.

5. **The skill must reject "borderline" requests.** Callers will sometimes have a hybrid question ("explain how httpx handles retries AND tell me how our codebase calls it"). The skill rejects with `INVALID_REQUEST: split-into-local-and-remote`. Callers must orchestrate two sub-calls (one to auggie, one to this skill). This is the price of scope discipline. Without it, the skill drifts back into the "everything-MCP" anti-pattern.

6. **Contract evolution requires versioning discipline.** When the input contract grows (new `question_shape`), callers using the old shape must keep working. The skill's `SKILL.md` carries a `contract_version` field and the system prompt accepts older shapes for at least 2 minor versions. Versioning discipline is a real cost; we accept it because the alternative (uncontrolled drift across 6 caller files) is worse.

## What This Cannot Do

- **Cannot serve hook-level integrations.** PostToolUse hooks can't practically spawn `Task` subagents; v1 §Cons #9 made this point and it still holds. The hook-level "fire octocode in parallel with auggie" idea from `octocode-research.md §6` is structurally incompatible with this design. **Mitigation:** if hook-level fan-out becomes important, a separate lightweight hook helper can wrap a single `githubSearchCode` call — but it should still route through a thin shared helper, not duplicate the full skill.

- **Cannot share octocode context across calls within one user turn.** Each `Task` invocation gets a fresh skill context. If a single conversation triggers three cross-repo investigations, each pays the skill's context-load cost. Octocode's 24h disk cache helps amortize *tool-level* state; the skill's *prompt context* is not reused. **Mitigation:** for high-frequency callers (rare), `mode: task` consolidates a sequence of investigations into one MDTM task with a single skill invocation.

- **Cannot do raw passthrough to octocode tools.** Users who explicitly want to run a single `githubSearchCode` query with custom flags have no direct path through the skill. They should use the `gh` CLI or invoke octocode through an MCP debugging path. The skill is a curated abstraction, not a transparent proxy.

- **Cannot eliminate the supply-chain risk.** Octocode is still a single-maintainer npm package; the skill cannot make that risk smaller. The skill can only *bound* the blast radius (one file to change if we abandon octocode) and *contain* the exposure (one place where `LOG=false` is enforced).

- **Cannot prevent callers from misclassifying `question_shape`.** A caller that sends `question_shape: pr_archaeology` for a `pattern_discovery` question gets suboptimal results. The skill's rejection rules catch the worst cases (`INVALID_REQUEST`), but soft misclassification produces lower-quality findings rather than errors. **Mitigation:** the skill's examples directory + the input contract's `parent_context` field nudge callers toward correct framing; over time, the rejection log informs contract refinement.

- **Cannot replace `tech-research`'s scope discovery role.** The skill explicitly assumes the caller has already done scope discovery (which repos? which packages? which focus areas?). It does not free-form search. This is by design — tech-research IS the scoper, and the skill IS the deep-diver. Callers without a scoper upstream need to either invoke tech-research first or hardcode scope in the input contract.

## Status: Complete
