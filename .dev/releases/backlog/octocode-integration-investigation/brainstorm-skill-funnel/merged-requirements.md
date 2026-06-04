---
brainstorm_id: octocode-skill-funnel
topic: "Having all octocode usage flow through a separate unique skill designed specifically to dive into codebases that tech-research finds and look at the specific areas relevant to the work being done"
domain: architecture
strategy: systematic
convergence_score: 0.82
adversarial_status: PASS
created: 2026-05-30T12:50:00Z
proposal_count: 3
proposal_lenses: [architect, analyzer, scribe]
proposal_models: [opus, sonnet, haiku]
---

# Merged Requirements — `octocode-deep-dive` Skill

A unified specification for a single dedicated skill that centralizes all octocode access across the IronClaude framework, derived from 3 parallel adversarial proposals (architect / analyzer / scribe lenses).

This proposal is an **architectural alternative to the v2 distributed plan** (T1-T6 integration points). Adoption decision goes to the user — both designs are now documented and tradeoffs explicit.

---

## 1. Skill Identity

| Field | Value |
|---|---|
| **Name** | `octocode-deep-dive` |
| **Path** | `src/superclaude/skills/octocode-deep-dive/SKILL.md` |
| **Purpose** | Targeted cross-repo investigation of GitHub/GitLab/Bitbucket repositories identified upstream by tech-research, /sc:troubleshoot, /tdd, /sc:brainstorm, or /sc:research. Wraps octocode-mcp's cross-repo tool whitelist with a stable input/output contract, rate-limit budget tracking, evidence-tagged findings (`[PRECEDENT: owner/repo@path]`), and fail-open semantics. |
| **Vendor neutrality** | Mechanism named in skill (`octocode-deep-dive`), but contract is vendor-neutral. If octocode-mcp is replaced (GitHub MCP, custom `gh` wrapper, Sourcegraph), the skill is renamed/aliased in the registry — zero caller-side changes. |

**Anti-scope (loud rejections):**

- ❌ Local codebase questions → use auggie / serena / Read
- ❌ Canonical library docs → use context7
- ❌ Open-web research → use tech-research / Tavily
- ❌ Open-ended target discovery → use tech-research (the upstream scope discoverer)

---

## 2. Architecture

### Execution Modes (hybrid)

```yaml
mode: inline   # DEFAULT — single agent invocation, no MDTM, synchronous return
               # Used by: tech-research Phase 4 sub-agents, sc-brainstorm Wave 2A,
               #          /sc:troubleshoot Tier 2, /sc:research --source octocode
               # Budget: ≤12 octocode calls per invocation
               # Latency: ~2-8s typical

mode: task     # OPT-IN — MDTM task file under caller's task directory
               # Used by: /tdd Stage A precedent discovery, tech-research Phase 4 as sub-task
               # Budget: ≤20 octocode calls per task, suspendable + resumable
               # Latency: ~15-45s typical
```

Ship `inline` mode in v1. `task` mode deferred to v1.1 after pilot data confirms MDTM-caller demand.

### Phase Structure

**Inline mode (default):**

```
Validate input contract → DISCOVER → SEARCH → LOCATE → READ → Synthesize findings → Return
```

(Single agent, no QA gates. The contract IS the QA gate — invalid inputs rejected up front.)

**Task mode (opt-in v1.1):**

```
Phase 1: Validate + Scope confirmation
Phase 2: Discover (githubViewRepoStructure)
Phase 3: Search (githubSearchCode + githubSearchPullRequests in parallel)
Phase 4: Locate (githubGetFileContent on top matches)
Phase 5: Synthesize findings with evidence tags
Phase 6: Return + write metrics
```

(MDTM task file in caller's task dir; survives context compression.)

### Tool Whitelist (single source of truth)

5 tools, declared exactly once in the skill's frontmatter:

```yaml
mcp-servers: [octocode]
allowed-tools:
  - mcp__octocode__githubSearchCode
  - mcp__octocode__githubGetFileContent
  - mcp__octocode__githubSearchPullRequests
  - mcp__octocode__githubViewRepoStructure
  - mcp__octocode__packageSearch
```

`ENABLE_LOCAL=false`, `ENABLE_CLONE=false`, `LOG=false`, `TOOLS_TO_RUN=` matching the above, all enforced by Phase 0 (install_mcp.py registration).

---

## 3. Contract (v1.0)

### Input Schema (YAML)

```yaml
contract_version: "1.0"   # REQUIRED — rejected if not supported

topic:                    # REQUIRED
  text: string            # 1-500 chars
  domain: enum            # precedent | pr-archaeology | package-investigation |
                          # library-usage | comparative (maps to R1-R5 archetypes)

caller:                   # REQUIRED — for telemetry, budget accounting, error attribution
  skill_or_command: string
  invocation_id: string   # UUID or task-id
  task_dir: path          # caller's MDTM task dir if any (optional)

scope_mode: enum          # REQUIRED — "explicit" | "delegated"

# scope_mode: explicit → caller supplies targets directly
targets:                  # CONDITIONAL (required when scope_mode=explicit)
  repos: ["owner/repo", ...]      # 1-10 max
  packages: ["pkg-name", ...]     # 0-10
  focus_areas: ["topic", ...]     # narrows search queries

# scope_mode: delegated → caller hands off upstream artifact
upstream_handoff:         # CONDITIONAL (required when scope_mode=delegated)
  artifact_path: path     # e.g., tech-research/research/scope.md
  artifact_type: enum     # tech-research-scope | troubleshoot-symptom | tdd-prd

# OPTIONAL (defaults shown)
mode: inline              # inline | task
max_evidence: 5           # 1-10
verbosity: compact        # compact | verbose
token_budget: 8000        # caller's allotment (skill returns RATE_LIMITED if exceeded)
rate_limit_budget: 5      # share of the 30 req/min global ceiling
output_format: both       # yaml | markdown | both
output_path: null         # if set, written to disk and path returned
quality_threshold: medium # low | medium | high (filters findings by confidence)
parent_context: ""        # 2-4 sentence paragraph — what is the caller trying to do
cache_hints: []           # from prior invocations for cache reuse
```

**Contract invariants (rejected with named error codes):**

| Rule | Error Code | Trigger |
|---|---|---|
| Contract version supported | `UNSUPPORTED_CONTRACT_VERSION` | Not in {1.0} |
| Topic non-empty | `EMPTY_TOPIC` | text < 1 char |
| Topic not local-codebase | `LOCAL_CODEBASE_TOPIC_DETECTED` | Names local paths or "this codebase" |
| Topic not canonical-docs | `CONCEPTUAL_QUERY_REQUIRES_CONFIRMATION` | Answerable from Context7 |
| Scope provided | `NO_SCOPE_PROVIDED` | Neither targets nor upstream_handoff |
| Targets bounded | `TARGETS_EXCEEDS_LIMIT` | >10 repos or >10 packages |
| Upstream artifact exists | `HANDOFF_ARTIFACT_MISSING` | File not found |
| Budget reasonable | `BUDGET_OUT_OF_RANGE` | token_budget > 30000 or rate_limit_budget > 10 |
| Caller identity present | `MISSING_CALLER_IDENTITY` | skill_or_command or invocation_id empty |

### Output Schema (YAML — canonical)

```yaml
contract_version: "1.0"
status: enum              # OK | PARTIAL | NO_EVIDENCE | INVALID_REQUEST |
                          # RATE_LIMITED | UNAVAILABLE | CLARIFY_NEEDED
question: string          # verbatim echo of input topic.text
caller: object            # verbatim echo of input caller
calls_used: int
calls_cap: int

repos_investigated:       # with SHA pins for reproducibility
  - "owner/repo@sha"

findings:                 # zero or more
  - precedent_tag: "[PRECEDENT: owner/repo@path:line]"
    quality_tier: enum    # primary | fallback | skipped
    summary: string       # 1-3 sentences
    evidence:
      - tool: string      # which octocode tool produced this
        url: string       # SHA-pinned permalink
        excerpt: string   # quoted code/text (60-200 chars)
    relevance_score: float  # 0.0-1.0
    research_goal: string  # the RDD field — what we were looking for
    reasoning: string      # the RDD field — why we picked this

provenance_trail:         # full tool-call audit log
  - tool: string
    research_goal: string
    reasoning: string
    timestamp: ISO8601
    duration_ms: int
    result_size_bytes: int

cost_summary:
  tokens_spent: int
  rate_limit_consumed: int
  cache_hits: int
  cache_misses: int

open_questions:           # things we noticed but didn't investigate (caller decides next step)
  - string

cache_hints:              # for caller to pass back to future invocations
  - key: string
    expires_at: ISO8601

# If status != OK, the following block is populated:
rejection:
  reason_code: string     # one of the named error codes above
  message: string         # human-readable
  remediation: string     # what the caller should do instead
```

### Markdown Output (deterministic projection)

When `output_format` is `markdown` or `both`, a Markdown projection is rendered from the YAML envelope with a contract-version + envelope-hash header for drift detection:

```markdown
<!-- octocode-deep-dive contract_version=1.0 envelope_sha=abc123def -->

# Cross-Repo Investigation: <topic.text>

**Status:** OK | PARTIAL | ...
**Caller:** <skill>:<invocation_id>
**Calls used:** N / cap

## Findings

### [PRECEDENT: owner/repo@path:line] — Summary
- **Quality tier:** primary
- **Evidence:** [excerpt](url)
- **Reasoning:** ...

## Open Questions
- ...

## Cost Summary
- Tokens: N | Rate-limit consumed: N | Cache hits: N
```

Markdown is a **rendering** of the YAML — not a separate output. Caller scripts parse the YAML; LLM consumers drop the Markdown into context.

---

## 4. Instrumentation (per Analyzer Proposal B)

Every invocation writes a structured metrics record:

```yaml
# .octocode-metrics/invocation-${ULID}.yaml
schema_version: "1.0"
invocation_id: <ULID>
caller: <skill:phase>
timestamp_start: ISO8601
timestamp_end: ISO8601
input:
  scope_size: {repos: N, packages: N, focus_areas: N}
  budget_hint: {tokens: N, rate_limit: N}
  mode: inline | task
tool_calls:
  - tool: githubSearchCode
    research_goal: string
    duration_ms: int
    result_size_bytes: int
    status: OK | RATE_LIMITED | ERROR
output:
  status: OK | PARTIAL | ...
  findings_count: N
  tokens_returned: N
budget_consumed:
  rate_limit_window_seconds: 60
  searches_this_window: N
  searches_remaining: N
cache:
  hits: N
  misses: N
  hint_persistence: bool
```

**Session-aggregate file** (cross-invocation): `~/.octocode-funnel/sessions/${SESSION_ID}.jsonl` (append-only, one record per invocation).

**Daily rollup**: `~/.octocode-funnel/daily/${YYYY-MM-DD}.json` (cumulative budget tracking across sessions).

### Global Rate-Limit Budget (the analyzer's KEY claim)

Distributed v2 plan: per-surface caps allow theoretical max of ~80 searches/min against GitHub's 30/min ceiling. **No global enforcement.**

Centralized skill: ONE sliding-window guard (per Proposal B's `RateLimitBudget` sketch):

- CEILING = 30 searches/min (GitHub's hard limit)
- SOFT = 24 searches/min (warn threshold)
- HARD = 28 searches/min (cap threshold; subsequent invocations return `RATE_LIMITED`)

Each invocation reads the window state, claims its slice, executes, then releases. **Global visibility, central enforcement.**

---

## 5. Anti-Pattern Detection (Programmatic Push-Back)

The skill's contract enforces anti-patterns by rejection. Listed for clarity:

| AP | Anti-pattern | Rejection code | Message to caller |
|---|---|---|---|
| AP1 | Local-codebase question | `LOCAL_CODEBASE_TOPIC_DETECTED` | "octocode-deep-dive does not investigate local files. Use auggie or serena instead." |
| AP2 | Canonical-docs question | `CONCEPTUAL_QUERY_REQUIRES_CONFIRMATION` | "This question is answerable from official documentation. Use context7." |
| AP3 | Open-ended target discovery | `NO_SCOPE_PROVIDED` | "octocode-deep-dive investigates pre-identified targets. Use tech-research to discover targets first." |
| AP4 | Too many targets | `TARGETS_EXCEEDS_LIMIT` | "Max 10 repos + 10 packages per invocation. Split into multiple calls." |
| AP5 | Budget overrun | `BUDGET_OUT_OF_RANGE` | "token_budget cap is 30K; rate_limit_budget cap is 10. Reduce or split." |
| AP6 | Missing handoff artifact | `HANDOFF_ARTIFACT_MISSING` | "scope_mode=delegated requires upstream_handoff.artifact_path to exist." |

These are loud rejections at the contract boundary — caller sees the rejection code + remediation, learns the skill's bounds, doesn't pass through to internals.

---

## 6. Versioning Policy

- **contract_version: 1.0** — initial release
- **Major** (2.0): breaking schema changes — requires caller updates
- **Minor** (1.1): additive fields only — backward-compatible
- **Patch** (1.0.1): bug fixes, no schema change

**Migration policy:**

- 6-month deprecation window before removing a supported version
- 2 prior versions carried simultaneously (e.g., when 1.2 ships, 1.0 and 1.1 still accepted)
- `contract_version` is REQUIRED in input — no implicit default (forces explicit caller awareness)

---

## 7. Caller Migration (How v2's T1-T6 Become This Skill)

| v2 Target | What changes |
|---|---|
| **T1: `deep-research` agent** (behavioral router) | Tool Selection Policy retains the "4th axis" prose, but instead of invoking `octocode-*` tools directly, the policy says: "For cross-repo research, invoke the `octocode-deep-dive` skill with the appropriate input contract." Frontmatter `tools:` no longer lists octocode tools. |
| **T2: `tech-research` Phase 4** (routed buckets) | The github-flavored bucket's agent prompt template instructs the agent to invoke `octocode-deep-dive` with `scope_mode: delegated` and `upstream_handoff.artifact_type: tech-research-scope`. Tavily-bucket agents unchanged. |
| **T3: `/sc:research --source` flag** | When `--source octocode`, command invokes `octocode-deep-dive` directly (passthrough), formats output as Markdown for the user. |
| **T4: `sc-brainstorm` Wave 2A enrichment** | Enrichment matrix gains a row for `domain in {code, architecture}` AND `strategy in {enterprise, default}` → invoke `octocode-deep-dive` with `scope_mode: explicit` and proposal-derived targets. Output written to `enrichment/precedent.md`. |
| **T5: `/sc:troubleshoot`** | Tier 1 `packageSearch` becomes `octocode-deep-dive` invocation with `domain: package-investigation` + single-package scope. Tier 2 `precedent-finder` agent becomes `octocode-deep-dive` invocation with `domain: pr-archaeology` + error-signature focus_areas. |
| **T6: `/tdd` Stage A** (PRD precedent) | Stage A precedent discovery becomes `octocode-deep-dive` invocation with `domain: precedent` + PRD-derived focus_areas. Phase 4 github-flavored bucket invokes same skill in delegated mode. |

**Net result:** All 6 v2 targets become THIN integration points (~10-25 LoC each) that compose the skill's input contract. The skill itself is the integration logic.

---

## 8. Comparison: Centralized Skill vs v2 Distributed Plan

| Dimension | v2 Distributed (T1-T6) | This proposal (centralized skill) |
|---|---|---|
| **Total LoC** | ~510 across 6 files | ~1,100 in one skill + ~150 across 6 thin invocation points = ~1,250 |
| **Net LoC delta** | baseline | **+145% (~+740 LoC)** — but front-loaded; v2 grows linearly per new caller |
| **Per-new-caller cost** | Full whitelist + anti-triggers + fallback per surface (~80-120 LoC) | ~10-25 LoC invocation contract |
| **Coupling cardinality** | `6 × N` (every change touches all 6 surfaces) | `6 × 1 + 1 × N` (skill changes are absorbed; callers only break on contract changes) |
| **Schema tax (per session)** | ~3K × 6 = ~18K tokens loaded at session start | ~3K loaded once in the skill |
| **Rate-limit budget enforcement** | Per-surface caps, NO global view; theoretical max ~80 req/min against 30/min ceiling | Single sliding-window guard, hard global cap |
| **Outage detection** | Per-surface; minutes-to-hours to correlate across artifacts | Single health.log; <1 second |
| **Anti-pattern enforcement** | Documented best-effort across 6 files | Executable code in one place; rejected at contract boundary |
| **Pilot data quality** | Bolt-on instrumentation per surface (deferred to "pilot phase" per v2 plan) | Instrumentation IS the primary output |
| **Time-to-implement first PR** | ~5h (Phase 0 + T1 deep-research) | ~15-20h (skill + first caller) |
| **Time-to-implement Nth PR** | ~5-10h per additional surface | ~1-2h per additional caller |
| **Failure-mode coverage** | Each surface defines its own; gaps possible | Centralized; one place to harden |
| **Vendor coupling** | "octocode" name in 6 caller files (rename = breaking) | "octocode" in skill internals only; caller-facing contract vendor-neutral |
| **Discoverability** | Per-surface; users learn surface-by-surface | One skill, one docs page, three discovery layers |

**Break-even point:** This proposal's higher initial cost pays back when there are ≥4 callers invoking it. v2 plan already has 6 caller targets identified — so break-even is reached on day 1 of the second caller integration.

**Risk-adjusted recommendation:** The centralized skill is the better long-term architecture **IF** the team commits to it before any of T1-T6 ships. If T1 has already shipped under v2, retrofitting to the centralized skill becomes a refactor with churn cost.

---

## 9. Implementation Phasing (Recommended)

```
Phase 0 (1h):  install_mcp.py registration (SAME as v2 Phase 0 — already covered)

Phase 1 (15-20h):  Build octocode-deep-dive skill
  - SKILL.md (frontmatter + behavioral spec)
  - Input/output contract validation logic
  - Tool invocation orchestration (inline mode only in v1)
  - Anti-pattern rejection logic with named error codes
  - Per-invocation metrics writer
  - Rate-limit budget sliding-window guard
  - docs/skills/octocode-deep-dive.md (caller-facing docs)
  - Unit tests for contract validation

Phase 2 (2-3h per caller):  Migrate each v2 target to thin invocation
  - tech-research Phase 4: github-flavored bucket invokes skill
  - sc-brainstorm Wave 2A: new enrichment row invokes skill
  - /sc:troubleshoot: Tier 1 + Tier 2 invoke skill
  - /tdd Stage A + Phase 4: invokes skill
  - deep-research agent: Tool Selection Policy points at skill (no direct tools)
  - /sc:research --source octocode: passthrough invocation

Phase 3 (deferred):  task-mode (v1.1) — opt-in MDTM mode after pilot data shows demand

Total: ~30-35h (vs v2 ~33-38h) — comparable effort, single-skill maintenance afterward.
```

---

## 10. Open Questions (For User Decision)

1. **Adopt this design or stick with v2 distributed plan?** Both are documented; both are valid architectures. This brainstorm's strongest argument is that the v2 plan's pilot-phase observability gaps are addressed natively by the centralized skill.
2. **If adopting: should T1 (deep-research agent) ship first under v2, then refactor to the skill? Or start fresh with the skill?** Fresh-start is cleaner; refactor accepts ~20-30% rework cost on T1.
3. **Skill name final: `octocode-deep-dive` (this proposal's merge) or `cross-repo-investigation` (architect's vendor-neutral preference)?** Trade-off documented in debate transcript.
4. **task-mode in v1 or v1.1?** v1.1 reduces initial scope; v1 lets `/tdd` Stage A use it from day one.
5. **Cache invalidation policy?** Not specified in any of the 3 proposals — defer to v1.1 after pilot data.
6. **Discoverability via slash command (`/octocode-deep-dive`)?** Architect argues NO (intentionally invoked); scribe argues YES (3-layer discoverability). Trade-off documented.

---

## 11. What This Proposal Cannot Do

- **Cannot eliminate octocode's supply-chain risk** — still depends on `npx octocode-mcp@<version>` from bgauryy. Centralized invocation doesn't make this safer; it does make the version pin visible in one place.
- **Cannot help if users invoke octocode-mcp tools directly outside the skill** — the skill assumes all octocode access flows through it. Direct tool calls bypass instrumentation. Solution: don't whitelist octocode tools at the framework level outside the skill's frontmatter.
- **Cannot survive contract drift if callers add free-form context fields** — the strict contract is the discipline. The moment a caller smuggles an unstructured `extras` field, the funnel rots. (See scribe's proposal §"What Happens When the Contract Needs to Change.")
- **Cannot replace tech-research** — tech-research remains the upstream scope discoverer. This skill is the deep-diver, not the surveyor.
- **Cannot serve hook-level integrations** — if PostToolUse hooks want to fire octocode in async fashion (per v1 brainstorm #4), they have to invoke the skill through the same contract; hooks are not exempt.

---

## 12. Return Contract Summary (for downstream pipeline consumption)

```yaml
contract_version: "1.0"
status: success
seed_brief_path: .dev/tasks/to-do/TASK-RESEARCH-20260530-044428/brainstorm-skill-funnel/seed-brief.md
merged_output_path: .dev/tasks/to-do/TASK-RESEARCH-20260530-044428/brainstorm-skill-funnel/merged-requirements.md
convergence_score: 0.82
adversarial_artifacts_dir: .dev/tasks/to-do/TASK-RESEARCH-20260530-044428/brainstorm-skill-funnel/adversarial/
domain: architecture
proposal_count: 3
enrichment_used:
  - source: codebase
    quality_tier: primary
  - source: research-deep
    quality_tier: primary
handoff_action: none
handoff_output_path: null
unresolved_conflicts:
  - "Skill name (3-way: cross-repo-investigation / octocode-funnel / octocode-deep-dive — merged on -deep-dive)"
  - "task-mode timing (v1 vs v1.1)"
  - "Cache invalidation policy (deferred)"
  - "Slash-command discoverability (yes/no — deferred)"
```

---

**Status:** Complete
**Next step (user-driven):** Decide whether to adopt this centralized-skill architecture vs the v2 distributed plan documented in `FINAL-RECOMMENDATIONS-v2.md`. If adopting, the first PR builds `src/superclaude/skills/octocode-deep-dive/SKILL.md` per Phase 1 of §9 above.
