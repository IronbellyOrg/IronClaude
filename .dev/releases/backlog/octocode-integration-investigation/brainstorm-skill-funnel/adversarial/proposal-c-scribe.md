# Proposal C — Scribe Lens

**Persona:** scribe
**Model:** haiku
**Status:** Complete
---

## Design Thesis

**The skill lives or dies by its contract.**

Every funnel pattern that ever rotted in this codebase rotted because the seam between caller and callee was loose. When the contract is loose, every caller writes a small adapter to massage their inputs to fit. Those adapters drift. Within six months, no two callers invoke the funnel the same way, the funnel's internal logic forks to accommodate the drift, and the original "single source of truth" becomes a fork-pile masquerading as centralization.

The v2 plan distributes octocode logic across six surfaces *because nobody trusted a shared contract would hold*. T1 through T6 each define their own tool whitelist, anti-trigger rules, rate-limit handling, output schema, and failure semantics — not because the logic genuinely differs, but because the caller couldn't articulate what they needed from a shared service in a way the service could honor.

A skill funnel only delivers the promised consolidation if:

1. **The input contract is specific enough** that callers can't smuggle their assumptions through "freeform context" fields. Free-form text in a contract is where reusability goes to die.
2. **The output contract is structured enough** that every caller parses results the same way. Markdown-only output forces every caller to write a brittle regex parser, which forces every caller's parser to silently diverge.
3. **The contract is versioned**. Skills evolve. Callers pin. Breaking changes are announced. Without this, the first "let's tweak the schema" lands silently and breaks three downstream skills no one remembered to update.
4. **Anti-pattern invocations are rejected loudly** at the contract boundary, not deep in the skill's internals where the caller can't see the rejection and learns nothing.

This proposal treats the skill as an *API*, not a workflow. Workflows accrue ad-hoc behavior; APIs constrain it. The constraint is what makes the funnel honest.

The architect lens (sibling Proposal A) will defend the directory layout. The analyzer lens (sibling Proposal B) will defend the measurability. **Scribe defends the contract** — without it, both of their proposals collapse within two quarters as drift accumulates.

---

## Skill Name + Purpose

**Skill name:** `octocode-deep-dive`

**One-line description (for SKILL.md `description:` frontmatter — the trigger surface):**

> Targeted cross-repo investigation of GitHub/GitLab/Bitbucket repositories identified upstream by tech-research, /sc:troubleshoot, /tdd, or /sc:brainstorm. Wraps octocode-mcp's cross-repo tool whitelist with a stable input/output contract, rate-limit budget tracking, evidence-tagged findings (`[PRECEDENT: owner/repo@path]`), and fail-open semantics. Use this skill when you have specific external repositories or packages to investigate, NOT when you need broad web research (use tech-research) or local codebase work (use auggie/serena).

**Why this naming wins on contract grounds:**

- `octocode-deep-dive` names the **mechanism** (octocode) AND the **shape** (deep-dive, not survey) — callers know what they're getting before reading the docs
- `external-codebase-research` was rejected because "research" overloads with `/sc:research` and `tech-research` — naming collisions are contract leaks
- `cross-repo-investigation` was rejected because "investigation" implies an open-ended scope; this skill is explicitly *narrow* — it dives into pre-identified targets, it does not discover them

**Scope (explicit non-goals):**

| In scope | Out of scope |
|---|---|
| Investigating named external repos (owner/repo specified by caller) | Discovering which repos to investigate (that's tech-research's job) |
| Reading specific files/PRs/packages | Open-ended "find me something about X" queries |
| Cross-repo PR archaeology with provenance tags | Local codebase symbol nav (use serena) |
| Package metadata lookup (npm/PyPI → repo URL) | Library docs lookup (use context7) |
| Returning structured findings with quality tiers | Generating implementation plans (caller does that) |

---

## Input Contract (the most important section)

The input contract is a **YAML envelope** the caller passes to the skill, either as a structured invocation argument (when called from a skill/agent) or as the first markdown block in a /sc command invocation. The skill SHALL reject any invocation that fails schema validation.

### Schema (v1.0)

```yaml
# REQUIRED FIELDS

contract_version: "1.0"           # MUST match a supported version; rejected otherwise

topic:                            # REQUIRED — what's being investigated
  text: string                    # 1-500 chars; the substantive research question
  domain: enum                    # one of: precedent | pr-archaeology | package-investigation
                                  #         | library-usage | comparative
                                  # (matches octocode-research.md R1-R5 archetypes)

caller:                           # REQUIRED — for telemetry, budget accounting, error attribution
  skill_or_command: string        # e.g., "tech-research", "sc-troubleshoot", "tdd"
  invocation_id: string           # UUID or task-id; threads through cost summary
  task_dir: path                  # caller's MDTM task dir if any; for cache hint persistence

# CONDITIONAL FIELDS — required when scope_mode is "explicit", forbidden when "delegated"

scope_mode: enum                  # REQUIRED — "explicit" | "delegated"
                                  # "explicit"  → caller supplies targets[] below
                                  # "delegated" → caller supplies upstream_handoff below
                                  # NO OTHER MODE. No "freeform" escape hatch.

targets:                          # REQUIRED when scope_mode=="explicit"
  - kind: enum                    # "repo" | "pr" | "package" | "file"
    identifier: string            # owner/repo | owner/repo#prNumber | npm:name | owner/repo@path
    rationale: string             # 1-200 chars; WHY this target? (RDD-style, audited)
    priority: enum                # "primary" | "fallback" — primary investigated first
  # min 1, max 8 targets per invocation

upstream_handoff:                 # REQUIRED when scope_mode=="delegated"
  source_skill: string            # e.g., "tech-research"
  source_artifact: path           # the artifact (file path) producing the handoff
                                  # MUST point at a real file; the skill verifies on entry
  extracted_targets: list         # the same targets[] schema above, lifted from the artifact

# OPTIONAL FIELDS — sensible defaults exist; specifying overrides

token_budget:                     # OPTIONAL — caller's max token allotment for THIS invocation
  cap: integer                    # default: 10000; max: 30000
  graceful_exit_at_pct: integer   # default: 80; skill halts at 80% and returns partial findings

rate_limit_budget:                # OPTIONAL — caller's slice of the 30 req/min Search API budget
  search_calls_cap: integer       # default: 5; max: 12
  content_calls_cap: integer      # default: 10; max: 25

quality_threshold:                # OPTIONAL — minimum confidence per finding to include
  min_tier: enum                  # "primary" | "fallback" | "any" (default: "fallback")
                                  # primary = repo verified, file read, line cited
                                  # fallback = repo verified, file existence asserted, line not cited
                                  # any = anything the skill found, including UNVERIFIED

output_format:                    # OPTIONAL — what the caller wants back
  structured: bool                # default: true; returns YAML output envelope
  markdown_report: bool           # default: true; ALSO writes .md report to caller's task_dir
  markdown_path: path             # default: ${task_dir}/research/octocode-{topic_slug}.md

cache_hints:                      # OPTIONAL — caller-passed reuse hints from previous invocation
  prior_invocation_id: string     # if the caller invoked the skill before on a related topic
  cacheable_findings: list        # finding_ids the caller wants reused if still valid
```

### Validation Rules (the rejection contract)

The skill SHALL reject invocations that violate any of these rules, with specific error messages:

| Rule | Rejection Message |
|---|---|
| `contract_version` missing or not "1.0" | `ERROR: contract_version required, must be "1.0". See docs/skills/octocode-deep-dive.md#versioning` |
| `topic.text` length not in `[1, 500]` | `ERROR: topic.text length=${n} outside [1, 500]` |
| `topic.domain` not in enum | `ERROR: topic.domain=${val} invalid. Allowed: precedent|pr-archaeology|package-investigation|library-usage|comparative` |
| `scope_mode == "explicit"` but `targets[]` empty | `ERROR: scope_mode=explicit requires targets[] with min 1, max 8 entries` |
| `scope_mode == "delegated"` but `upstream_handoff.source_artifact` does not exist on disk | `ERROR: upstream_handoff.source_artifact path does not exist: ${path}. Did tech-research complete? Did you pass the wrong path?` |
| `targets[].identifier` does not match its `kind` schema | `ERROR: targets[${i}].identifier=${val} does not match kind=${kind}. Expected format: ${format}` |
| `token_budget.cap > 30000` | `ERROR: token_budget.cap=${n} exceeds maximum 30000. This skill is for targeted investigation, not unbounded search.` |
| Local-codebase topic detected (heuristic) | `ERROR: Topic appears to reference local codebase (matched: ${matched_phrase}). This skill is for CROSS-REPO investigation only. Use auggie or serena for local work.` |
| Topic phrasing matches anti-trigger list (e.g., "best practices", "tutorial", "explain") | `WARNING: Topic phrasing suggests conceptual research. Consider /sc:research with tavily/context7 instead. Proceed anyway? [requires --confirm-conceptual flag]` |

The rejection contract is **publicly documented** so callers learn the shape of valid invocations by being told why their invalid ones failed.

### Three Example Invocations

#### Example 1 — tech-research Phase 4 (delegated scope)

```yaml
contract_version: "1.0"

topic:
  text: "How do popular OSS PR-review bots handle false-positive suppression for security findings?"
  domain: comparative

caller:
  skill_or_command: "tech-research"
  invocation_id: "TASK-RESEARCH-20260601-091200"
  task_dir: ".dev/tasks/to-do/TASK-RESEARCH-20260601-091200/"

scope_mode: "delegated"
upstream_handoff:
  source_skill: "tech-research"
  source_artifact: ".dev/tasks/to-do/TASK-RESEARCH-20260601-091200/research/research-notes.md"
  extracted_targets:
    - kind: repo
      identifier: "googleapis/code-suggester"
      rationale: "Phase 2 codebase scan identified this as the closest architectural precedent"
      priority: primary
    - kind: repo
      identifier: "github/super-linter"
      rationale: "Tech-research Phase 2 noted false-positive logic similar to our needs"
      priority: primary
    - kind: pr
      identifier: "github/super-linter#3421"
      rationale: "Phase 2 found this PR explicitly addresses our suppression question"
      priority: primary

token_budget:
  cap: 12000
  graceful_exit_at_pct: 80

rate_limit_budget:
  search_calls_cap: 4
  content_calls_cap: 8

quality_threshold:
  min_tier: "fallback"

output_format:
  structured: true
  markdown_report: true
  markdown_path: ".dev/tasks/to-do/TASK-RESEARCH-20260601-091200/research/web-octocode-pr-bot-precedent.md"
```

#### Example 2 — /sc:troubleshoot precedent-finder (explicit scope)

```yaml
contract_version: "1.0"

topic:
  text: "How have other projects fixed UnicodeDecodeError when reading config files with mixed encodings under Python 3.12?"
  domain: pr-archaeology

caller:
  skill_or_command: "sc-troubleshoot"
  invocation_id: "TROUBLESHOOT-20260601-141800"
  task_dir: ".dev/tasks/to-do/TROUBLESHOOT-20260601-141800/"

scope_mode: "explicit"
targets:
  - kind: package
    identifier: "npm:pyenv-installer"
    rationale: "User reported error inside pyenv-installed Python 3.12 path"
    priority: primary
  - kind: repo
    identifier: "python/cpython"
    rationale: "Upstream issue tracker likely has 3.12 encoding regression PRs"
    priority: primary
  - kind: repo
    identifier: "pypa/pip"
    rationale: "Similar error class affects pip; check their fix patterns"
    priority: fallback

token_budget:
  cap: 8000

quality_threshold:
  min_tier: "primary"  # troubleshoot needs verified evidence, not loose precedent

output_format:
  structured: true
  markdown_report: false  # caller uses structured output directly to build Precedent Card
```

#### Example 3 — /tdd Stage A PRD precedent discovery (explicit scope)

```yaml
contract_version: "1.0"

topic:
  text: "Reference implementations of cursor-based pagination for GraphQL list resolvers with sub-100ms latency"
  domain: library-usage

caller:
  skill_or_command: "tdd"
  invocation_id: "TDD-20260601-103000"
  task_dir: ".dev/tasks/to-do/TDD-20260601-103000/"

scope_mode: "explicit"
targets:
  - kind: package
    identifier: "npm:graphql-relay"
    rationale: "PRD references Relay-style cursor pagination as the goal"
    priority: primary
  - kind: repo
    identifier: "facebook/relay"
    rationale: "Reference implementation"
    priority: primary
  - kind: repo
    identifier: "apollographql/apollo-server"
    rationale: "Major alternative cursor implementation; compare approach"
    priority: fallback

token_budget:
  cap: 15000  # Heavyweight TDD warrants larger budget

quality_threshold:
  min_tier: "primary"  # TDD evidence must be code-verified

output_format:
  structured: true
  markdown_report: true
  markdown_path: ".dev/tasks/to-do/TDD-20260601-103000/research/stage-a-precedent.md"
```

---

## Output Contract

The output is a **structured YAML envelope** returned to the caller (parsed by skill/command consumers) AND optionally a markdown report written to disk (for human review or direct LLM-context drop-in). The YAML envelope is canonical; the markdown is a rendering.

### Schema (v1.0)

```yaml
# ENVELOPE METADATA

contract_version: "1.0"           # matches what caller requested
invocation_id: string             # echoed from input for caller correlation
status: enum                      # "complete" | "partial" | "failed" | "rejected"
status_reason: string             # plain-English reason for status
completed_at: ISO8601

# FINDINGS — the substantive payload

findings:
  - finding_id: string            # stable hash; usable as cache_hint in future invocations
    quality_tier: enum            # "primary" | "fallback" | "skipped"
                                  # primary  = source repo verified + file read + line cited
                                  # fallback = source repo verified + file exists + no line citation
                                  # skipped  = couldn't verify; only in output if min_tier=="any"
    precedent_tag: string         # "[PRECEDENT: owner/repo@path]" — REQUIRED for primary tier
                                  # "[PRECEDENT: owner/repo (no line cite)]" for fallback
    target_kind: enum             # echoes input targets[].kind
    target_identifier: string     # echoes input targets[].identifier
    excerpt: string               # quoted excerpt from the source (max 1000 chars)
    excerpt_url: url              # permalink to the exact commit+line
    relevance_to_topic: string    # 1-3 sentences; why this finding matters to topic.text
    confidence: float             # 0.0 - 1.0; the skill's confidence in this finding's relevance
    produced_by_tool_calls: list  # tool-call ids from provenance_trail below

# COST SUMMARY — for budget accounting

cost_summary:
  tokens_spent: integer
  tokens_remaining: integer
  rate_limit_budget_consumed:
    search_calls_made: integer
    search_calls_cap: integer
    content_calls_made: integer
    content_calls_cap: integer
  wall_clock_seconds: float
  budget_exhausted: bool          # true if skill halted at graceful_exit_at_pct

# PROVENANCE TRAIL — full audit of every tool call

provenance_trail:
  - call_id: string               # e.g., "tc-001"
    tool: string                  # e.g., "githubSearchCode"
    research_goal: string         # the octocode RDD-mandated researchGoal field
    reasoning: string             # the octocode RDD-mandated reasoning field
    parameters: object            # exact parameters sent (sanitized for telemetry)
    result_summary: string        # 1-2 lines on what came back
    finding_ids_produced: list    # finding_ids in this output that trace back to this call

# OPEN QUESTIONS — what the skill could NOT investigate

open_questions:
  - question: string              # 1-2 sentences
    reason: enum                  # "rate_limit_exhausted" | "token_budget_exhausted"
                                  # | "target_not_found" | "out_of_scope" | "tool_error"
    suggested_followup: string    # what the caller could do (re-invoke? use different skill?)

# CACHE HINTS — for caller to pass back next time

cache_hints:
  invocation_id: string           # this invocation's ID; caller can pass as prior_invocation_id
  cacheable_finding_ids: list     # findings the skill thinks are stable for ~24h
  cache_expiry_hint: ISO8601      # when these findings should be re-verified

# REJECTION CASE (status=="rejected") — populated INSTEAD of findings/cost_summary

rejection:
  reason_code: string             # matches validation rule codes from Input Contract
  message: string                 # human-readable
  remediation: string             # what the caller should change
```

### Three Example Outputs

#### Example 1 — Complete success (matches tech-research invocation)

```yaml
contract_version: "1.0"
invocation_id: "TASK-RESEARCH-20260601-091200"
status: complete
status_reason: "All 3 targets investigated; 4 findings returned; under budget."
completed_at: "2026-06-01T09:14:32Z"

findings:
  - finding_id: "f-a3c1"
    quality_tier: primary
    precedent_tag: "[PRECEDENT: github/super-linter@lib/functions/suppressions.sh:42-71]"
    target_kind: repo
    target_identifier: "github/super-linter"
    excerpt: |
      # Suppression file format:
      # path/to/file:LINTER:RULE_ID  // reason
      # Empty lines and # comments allowed
      while IFS=':' read -r FILE LINTER RULE; do
        [[ -z "${FILE}" || "${FILE}" =~ ^# ]] && continue
        SUPPRESSIONS+=("${FILE}|${LINTER}|${RULE}")
      done < "${SUPPRESSION_FILE}"
    excerpt_url: "https://github.com/github/super-linter/blob/v5.7.2/lib/functions/suppressions.sh#L42-L71"
    relevance_to_topic: "Direct precedent: line-level suppression keyed on (file, linter, rule). Maps cleanly to our 'how do bots handle false-positive suppression' question."
    confidence: 0.92
    produced_by_tool_calls: ["tc-002", "tc-004"]

  - finding_id: "f-b7d4"
    quality_tier: primary
    precedent_tag: "[PRECEDENT: googleapis/code-suggester@src/github-handler/pull-request-handler.ts:188]"
    # ... (additional fields)

  - finding_id: "f-c2e8"
    quality_tier: fallback
    precedent_tag: "[PRECEDENT: github/super-linter#3421 (no line cite)]"
    target_kind: pr
    target_identifier: "github/super-linter#3421"
    excerpt: "PR title + first 300 chars of body discussing suppression heuristics..."
    excerpt_url: "https://github.com/github/super-linter/pull/3421"
    relevance_to_topic: "PR discusses the design rationale for suppression file format. Body summarized; no line-level code citation extracted (PR body, not source)."
    confidence: 0.78
    produced_by_tool_calls: ["tc-005"]

cost_summary:
  tokens_spent: 9847
  tokens_remaining: 2153
  rate_limit_budget_consumed:
    search_calls_made: 3
    search_calls_cap: 4
    content_calls_made: 6
    content_calls_cap: 8
  wall_clock_seconds: 18.4
  budget_exhausted: false

provenance_trail:
  - call_id: "tc-001"
    tool: "githubSearchRepositories"
    research_goal: "Confirm target repos exist and gather metadata before deep dive"
    reasoning: "RDD requires confirming targets before fetching; cheaper than blind fetches"
    parameters: {query: "super-linter OR code-suggester", per_page: 5}
    result_summary: "Both target repos confirmed; star counts noted; default branches noted"
    finding_ids_produced: []
  - call_id: "tc-002"
    tool: "githubSearchCode"
    research_goal: "Find suppression-handling code in super-linter"
    reasoning: "PR archaeology requires locating the implementation before reading PR rationale"
    parameters: {q: "repo:github/super-linter suppression"}
    result_summary: "Found lib/functions/suppressions.sh:42 as primary suppression handler"
    finding_ids_produced: ["f-a3c1"]
  # ... additional calls

open_questions:
  - question: "How does super-linter handle precedence when a file matches multiple suppression patterns?"
    reason: "out_of_scope"
    suggested_followup: "Re-invoke with explicit target on suppressions.sh#L72-L120 for the merge logic"

cache_hints:
  invocation_id: "TASK-RESEARCH-20260601-091200"
  cacheable_finding_ids: ["f-a3c1", "f-b7d4"]
  cache_expiry_hint: "2026-06-02T09:14:32Z"
```

#### Example 2 — Partial (budget exhausted)

```yaml
contract_version: "1.0"
invocation_id: "TROUBLESHOOT-20260601-141800"
status: partial
status_reason: "Token budget reached 80% (graceful_exit_at_pct) after investigating 2 of 3 targets. Primary target pypa/pip not investigated."
completed_at: "2026-06-01T14:19:11Z"

findings:
  - finding_id: "f-x9a3"
    quality_tier: primary
    precedent_tag: "[PRECEDENT: python/cpython@Lib/encodings/__init__.py:127]"
    # ... (full primary finding for cpython)

  - finding_id: "f-y4b8"
    quality_tier: fallback
    # ... (fallback finding from packageSearch on pyenv-installer)

cost_summary:
  tokens_spent: 6412
  tokens_remaining: 1588
  budget_exhausted: true

open_questions:
  - question: "pypa/pip's encoding-error fix pattern not investigated"
    reason: "token_budget_exhausted"
    suggested_followup: "Re-invoke with explicit single target pypa/pip and higher token_budget.cap"

cache_hints:
  invocation_id: "TROUBLESHOOT-20260601-141800"
  cacheable_finding_ids: ["f-x9a3", "f-y4b8"]
  cache_expiry_hint: "2026-06-02T14:19:11Z"
```

#### Example 3 — Rejection (anti-pattern invocation)

```yaml
contract_version: "1.0"
invocation_id: "AD-HOC-20260601-160000"
status: rejected
status_reason: "Input contract violation"
completed_at: "2026-06-01T16:00:02Z"

rejection:
  reason_code: "LOCAL_CODEBASE_TOPIC_DETECTED"
  message: |
    Topic text "How does our payment processing module handle refund webhooks?" appears to reference
    the local codebase ("our ... module"). This skill is for CROSS-REPO investigation only.
  remediation: |
    For LOCAL codebase questions, use auggie's codebase-retrieval or serena's find_symbol.
    If you genuinely meant to investigate cross-repo precedents for refund webhook handling,
    rephrase the topic to name external targets:
      topic.text: "How do popular OSS payment libraries (Stripe SDK, etc.) handle refund webhook deduplication?"
      scope_mode: "explicit"
      targets:
        - kind: package
          identifier: "npm:stripe"
        - kind: repo
          identifier: "stripe/stripe-node"
```

---

## Markdown vs Structured Output

**Argument: BOTH, and the contract specifies which is canonical.**

The YAML envelope is **canonical**. The markdown is a **rendering** of the envelope. The skill's internals MUST produce the envelope first and derive the markdown from it (never the reverse).

| Consumer type | Format consumed | Why |
|---|---|---|
| Downstream skills (tech-research, /tdd, /sc:troubleshoot) | YAML envelope (structured) | Pipeline consumption requires schema-stable parsing. Markdown parsing is brittle and silently drifts. |
| Human reviewers reviewing a research task folder | Markdown report | Markdown is readable; YAML is auditable. Both have a role. |
| LLM-context drop-in (e.g., synthesis agent reading prior octocode output) | Markdown report | LLMs digest markdown better than nested YAML in context windows. The markdown carries the precedent tags verbatim. |
| Cross-invocation cache layer | YAML envelope + finding_ids | Finding-ID-based caching only works on structured data. |
| Telemetry / audit logs | YAML envelope (provenance_trail subset) | Structured logs aggregate; markdown logs don't. |

**Markdown rendering rules (deterministic, derived from envelope):**

```markdown
# Octocode Deep-Dive: ${topic.text}

**Status:** ${status}
**Invocation:** ${invocation_id}
**Tokens spent:** ${cost_summary.tokens_spent} / ${cost_summary.tokens_spent + tokens_remaining}
**Date:** ${completed_at}

## Findings (${count})

### ${finding[i].precedent_tag}  *(tier: ${quality_tier}, confidence: ${confidence})*

${relevance_to_topic}

```${language_from_excerpt_url}
${excerpt}
```

[View in source](${excerpt_url})

---

## Cost Summary

[Rendered table]

## Provenance Trail

[Rendered table]

## Open Questions

${rendered_questions}
```

**Versioning of the markdown:** the markdown SHALL include the line `<!-- octocode-deep-dive contract_version=1.0 envelope-hash=${sha256(envelope)[:8]} -->` at the top, so a downstream consumer can detect drift between an old markdown and a re-rendered one.

---

## Contract Versioning

**Current version:** 1.0

### Stability Guarantees

| Element | Stability tier | Breaking change policy |
|---|---|---|
| `contract_version` field semantics | Permanent | Never removed; new versions add fields, never repurpose existing ones |
| Top-level envelope keys (`status`, `findings`, `cost_summary`, etc.) | Stable across 1.x | Additions only; renames or removals require 2.0 |
| `findings[].quality_tier` enum values | Stable across 1.x | New tiers may be added at minor versions (1.1, 1.2); existing tiers preserved |
| `rejection.reason_code` enum values | Stable across 1.x | New codes added at minor versions; existing codes preserved with stable semantics |
| `precedent_tag` format string | Stable across 1.x | Format is `[PRECEDENT: owner/repo@path:line]` for primary, `[PRECEDENT: owner/repo (no line cite)]` for fallback; bug-level fixes only |
| `provenance_trail[]` schema | Stable across 1.x | Additions only |
| Token budget defaults | Configurable, not contract | May be tuned without version bump |
| Rate limit budget defaults | Configurable, not contract | May be tuned without version bump |
| Anti-trigger heuristics (rejection rules) | Configurable, not contract | May be tuned with telemetry; document in CHANGELOG.md but not a breaking change |

### Versioning Mechanics

- **Major version bump (2.0):** Required for any of: field rename, field removal, enum value removal, semantic shift in existing fields. Announced 1 release cycle in advance via deprecation warnings in the envelope (`deprecations: [...]` field).
- **Minor version bump (1.1, 1.2):** New optional input fields, new optional output fields, new enum additions. Backward compatible — `contract_version: "1.0"` callers continue to work against a 1.1 skill, ignoring new fields.
- **Patch version (1.0.1):** Bug fixes in skill internals that don't change observable contract. Not announced in `contract_version`.

### How Callers Signal Their Accepted Version

Callers pass `contract_version: "1.0"` (string, not float — `"1.0"` ≠ `"1.00"`). The skill SHALL:

1. If caller passes a version newer than the skill supports: reject with `reason_code: "UNSUPPORTED_CONTRACT_VERSION_FROM_CALLER"` and list supported versions.
2. If caller passes a version older than the skill supports: serve the OLDER contract semantics (the skill carries 2 prior versions for ≥6 months after a major bump).
3. If caller omits `contract_version`: reject with `reason_code: "MISSING_CONTRACT_VERSION"`. There is no implicit default — explicit pinning is the contract.

### Deprecation Policy

When a field or enum value is deprecated:

1. **Release N:** Field still works, but envelope includes `deprecations: [{field, replacement, removal_in_version}]`. Callers see the warning in their cost_summary parsing or via the markdown report's "Notices" section.
2. **Release N+1 to N+3:** Field continues to work; warning continues.
3. **Release N+4 (minimum 6 months later):** Field removed in a major version bump. Callers who haven't migrated are rejected with a clear error.

---

## Caller Invocation Patterns (5 examples — concrete)

### Pattern 1 — tech-research Phase 4 invokes for github-flavored topics

In `src/superclaude/skills/tech-research/SKILL.md` Phase 4, after rf-task-builder classifies a Phase 4 topic as `github-flavored`, the dispatcher checklist item invokes:

```markdown
- [ ] Phase 4 Topic 3 (github-flavored): Invoke octocode-deep-dive skill
  Pass the following YAML to the skill (see docs/skills/octocode-deep-dive.md):

  ```yaml
  contract_version: "1.0"
  topic:
    text: "${PHASE_4_TOPIC_3.text}"
    domain: "${PHASE_4_TOPIC_3.classified_domain}"
  caller:
    skill_or_command: "tech-research"
    invocation_id: "${TASK_ID}"
    task_dir: "${TASK_DIR}"
  scope_mode: "delegated"
  upstream_handoff:
    source_skill: "tech-research"
    source_artifact: "${TASK_DIR}research/research-notes.md"
    extracted_targets: ${PHASE_4_TOPIC_3.targets_yaml}
  output_format:
    structured: true
    markdown_report: true
    markdown_path: "${TASK_DIR}research/web-octocode-topic-3.md"
  ```

  The skill returns a YAML envelope. Mark this item complete and store the envelope path at ${TASK_DIR}qa/octocode-envelopes/topic-3.yaml for the rf-qa-qualitative agent to spot-check.
```

### Pattern 2 — /sc:troubleshoot Tier 2 precedent-finder invokes

In `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Tier 2 Wave 3, the precedent-finder agent (replacing what T5 in v2 specified as a dedicated agent):

```markdown
When troubleshoot --type is bug | build | test, Wave 3 invokes octocode-deep-dive:

```yaml
contract_version: "1.0"
topic:
  text: "${USER_SYMPTOM_NORMALIZED}"
  domain: pr-archaeology
caller:
  skill_or_command: "sc-troubleshoot"
  invocation_id: "${TROUBLESHOOT_ID}"
  task_dir: "${TROUBLESHOOT_DIR}"
scope_mode: "explicit"
targets: ${TARGETS_EXTRACTED_FROM_SYMPTOM}
quality_threshold:
  min_tier: "primary"     # troubleshoot needs verified evidence
output_format:
  structured: true
  markdown_report: false   # caller uses envelope to build Precedent Card
```

The Precedent Card appends `findings[].precedent_tag` and `findings[].excerpt_url` to each fix-<N>.md as advisory context.
```

### Pattern 3 — /tdd Stage A invokes for PRD precedent discovery

In `src/superclaude/skills/tdd/refs/agent-prompts.md` Stage A:

```markdown
## Stage A: PRD Precedent Discovery (when PRD is present)

After parsing the PRD, extract candidate external targets (libraries, frameworks, reference implementations named in the PRD). Then invoke octocode-deep-dive:

```yaml
contract_version: "1.0"
topic:
  text: "Reference implementations for ${PRD_CORE_CAPABILITY}"
  domain: library-usage
caller:
  skill_or_command: "tdd"
  invocation_id: "${TDD_ID}"
  task_dir: "${TDD_DIR}"
scope_mode: "explicit"
targets: ${TARGETS_FROM_PRD_EXTRACTION}
quality_threshold:
  min_tier: "primary"     # TDDs are normative specs; precedent must be code-verified
output_format:
  structured: true
  markdown_report: true
  markdown_path: "${TDD_DIR}research/stage-a-precedent.md"
```

The findings feed Phase 2 (codebase research) as scoping context. The `[PRECEDENT: owner/repo@path]` tags propagate through synthesis/assembly/QA per T6's discipline.
```

### Pattern 4 — /sc:brainstorm Wave 2A invokes for cross-repo precedent

In `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` Wave 2A enrichment matrix:

```markdown
| Domain | Strategy | Source | Skill |
|---|---|---|---|
| code, architecture | enterprise, default+--precedent | octocode-deep-dive | invoked with delegated scope_mode |

When the matrix row matches, invoke:

```yaml
contract_version: "1.0"
topic:
  text: "Cross-repo precedents for ${BRAINSTORM_TOPIC}"
  domain: comparative
caller:
  skill_or_command: "sc-brainstorm"
  invocation_id: "${BRAINSTORM_ID}"
  task_dir: "${BRAINSTORM_DIR}"
scope_mode: "delegated"
upstream_handoff:
  source_skill: "sc-brainstorm"
  source_artifact: "${BRAINSTORM_DIR}enrichment/precedent-targets.md"
  extracted_targets: ${TARGETS_FROM_SOCRATIC_PHASE}
output_format:
  structured: true
  markdown_report: true
  markdown_path: "${BRAINSTORM_DIR}enrichment/precedent.md"
```

Fail-open: if the skill returns `status: failed`, Wave 2A degrades the quality tier on the enrichment row and proceeds. The brainstorm does not block on octocode.
```

### Pattern 5 — /sc:research --source octocode invokes directly (passthrough)

In `src/superclaude/commands/sc/research.md`, when `--source octocode` is passed:

```markdown
When --source includes "octocode", invoke octocode-deep-dive once per research topic:

```yaml
contract_version: "1.0"
topic:
  text: "${USER_TOPIC_TEXT}"
  domain: "${USER_DOMAIN_OR_INFERRED}"     # default to "comparative" if user didn't specify
caller:
  skill_or_command: "sc-research"
  invocation_id: "${RESEARCH_ID}"
  task_dir: "${RESEARCH_DIR}"
scope_mode: "${EXPLICIT_IF_USER_NAMED_TARGETS_ELSE_DELEGATED}"
targets: ${USER_PROVIDED_TARGETS_OR_NULL}
upstream_handoff: ${NULL_OR_AUTO_GENERATED_FROM_RESEARCH_DISCOVERY}
output_format:
  structured: true
  markdown_report: true
  markdown_path: "${RESEARCH_DIR}reports/octocode-section.md"
```

The /sc:research command stitches the markdown report into its "Findings by Backend" section, tagged [octocode]. The structured envelope is preserved at ${RESEARCH_DIR}envelopes/octocode.yaml for downstream tools.
```

---

## Caller-Facing Documentation

A new file `docs/skills/octocode-deep-dive.md` is required. **This is part of the contract** — the skill's behavior is whatever this document says it is. Outline:

```markdown
# octocode-deep-dive — Caller Guide

## What This Skill Does
[2 paragraphs: targeted cross-repo investigation, downstream of upstream scoping, with provenance and budgets.]

## When to Use It
- ✅ You have specific external repos/packages/PRs to investigate
- ✅ You need [PRECEDENT: owner/repo@path] tags for downstream evidence chains
- ✅ You want a structured envelope you can pipeline-consume

## When NOT to Use It
- ❌ You need to *discover* which repos to investigate → use tech-research
- ❌ You need local-codebase work → use auggie or serena
- ❌ You need library docs → use context7
- ❌ You need general web research → use tavily

## Input Contract (v1.0)
[Full YAML schema, copy-pasted from this proposal's Input Contract section]

## Output Contract (v1.0)
[Full YAML schema, copy-pasted from this proposal's Output Contract section]

## Invoking from a Skill
[Template for each of the 5 caller patterns above]

## Failure Modes
| Status | When | What the caller should do |
|---|---|---|
| complete | Everything investigated | Consume findings |
| partial | Budget hit; some targets not reached | Re-invoke with single-target focus + larger budget |
| failed | Tool-level failure (e.g., rate-limit 403) | Fail open per caller's policy; check `open_questions[].suggested_followup` |
| rejected | Input contract violation | Read `rejection.remediation` and fix the invocation |

## Contract Versioning
[Stability guarantees + breaking change policy, copy-pasted from this proposal]

## Migration Guide (when 2.0 lands)
[Reserved for future]

## Telemetry & Privacy
[LOG=false enforced; what metadata is recorded; how to opt out further]

## Cost Model
[Token budgets, rate limit slice, expected ranges per domain]

## Troubleshooting
[Common rejection reasons + fixes; common partial reasons + fixes]
```

This document is the **caller-facing source of truth**. SKILL.md inside `src/superclaude/skills/octocode-deep-dive/` is the *skill-internal* truth (workflow, prompts, tool whitelists); `docs/skills/octocode-deep-dive.md` is the *caller-facing* truth (schemas, examples, guarantees). Both must stay in sync, enforced by a `make verify-skill-docs` target that fails CI if the schemas drift.

---

## Discoverability

**Three layers of discoverability:**

### Layer 1 — Direct slash-command invocation

`/sc:octocode-deep-dive` is registered in `src/superclaude/commands/sc/octocode-deep-dive.md`. Users typing `/sc:` autocomplete see it. The command dispatches directly into the skill with the input passed as command args.

### Layer 2 — Skill auto-trigger (via SKILL.md description)

The skill's `description:` frontmatter (shown earlier) names the trigger surface: "Use this skill when you have specific external repositories or packages to investigate, NOT when you need broad web research or local codebase work." Phrases like "investigate this OSS repo", "how does X library implement Y", "precedent for X" auto-suggest the skill.

### Layer 3 — Caller-skill auto-invocation

The skill is invoked **by other skills/commands** via the patterns above. Users don't need to know it exists — when they invoke /sc:troubleshoot or /tdd, the upstream skill funnels into octocode-deep-dive automatically. This is the primary intended invocation path.

### Anti-discoverability rules

The skill MUST NOT be:

- Auto-suggested when the user's prompt mentions local-codebase work (anti-trigger heuristic)
- Auto-suggested when the user's prompt is conceptual ("best practices", "how should I", "tutorial")
- Surfaced as a "recommended next step" by /sc:recommend unless the conversational context already contains cross-repo intent

These anti-discoverability rules prevent the funnel from becoming a hammer-looking-for-nails.

---

## Anti-Pattern Pushback

The contract SHALL reject the following invocation classes with **specific, learnable error messages**:

| Anti-pattern | Detection | Rejection message |
|---|---|---|
| Local-codebase question disguised as cross-repo | Topic text contains phrases like "our codebase", "this project", "our X module", or matches paths under the current repo | `LOCAL_CODEBASE_TOPIC_DETECTED` (see Example 3 above for full message) |
| Conceptual question (no specific targets) | Topic matches phrases: "best practices", "tutorial", "explain", "how should I", "what is" + no `targets[]` provided | `CONCEPTUAL_QUERY_REQUIRES_CONFIRMATION` — caller must pass `--confirm-conceptual` flag to proceed; suggests `/sc:research --source tavily` instead |
| Discovery-mode invocation (no targets, no upstream_handoff) | Both `targets[]` and `upstream_handoff` empty | `NO_SCOPE_PROVIDED` — "This skill does not discover targets. Run tech-research first, or specify targets explicitly. See Pattern 1 in docs/skills/octocode-deep-dive.md." |
| Token budget grossly oversized | `token_budget.cap > 30000` | `BUDGET_EXCEEDS_MAXIMUM` — "Budget cap ${n} exceeds 30000. This skill is for targeted investigation. For broader budgets, decompose into multiple invocations." |
| Caller missing identity | `caller.skill_or_command` or `caller.invocation_id` empty | `MISSING_CALLER_IDENTITY` — required for telemetry, budget accounting, error attribution |
| Stale handoff artifact | `upstream_handoff.source_artifact` path does not exist on disk | `HANDOFF_ARTIFACT_MISSING` — see Example 3 logic |
| Too many targets | `targets[].length > 8` | `TARGETS_EXCEEDS_LIMIT` — "Max 8 targets per invocation. Decompose into multiple invocations or filter to the most relevant 8." |
| Library-docs question | Topic matches "what does X API do", "syntax for X" | `CONTEXT7_PREFERRED` — "Library docs queries are better served by context7. Use --confirm-anyway to override." |

**Why explicit rejection beats silent acceptance:**

Silently accepting these invocations and producing low-quality output trains callers to use the skill for the wrong thing. Loud rejection at the contract boundary trains callers — over time — to invoke the skill in the way it was designed for. The rejection messages double as documentation.

---

## What Happens When the Contract Needs to Change

### Migration Strategy

When a breaking change is necessary (e.g., a new finding tier `verified-by-llm-review` requires a 2.0 bump):

1. **Discovery phase (1 release cycle):** Add the new field as OPTIONAL in 1.x. Callers can opt in, but it doesn't break old callers. Telemetry tracks how many callers adopt.
2. **Announcement (1 release):** Cut 2.0-beta. Document the breaking change. Add `deprecations: [...]` entries to 1.x output envelopes.
3. **Deprecation window (minimum 6 months):** Both 1.x and 2.0 work in parallel. Skill internals serve both contract versions based on caller's `contract_version` field.
4. **Removal (after 6 months minimum):** 1.x stops being supported. Callers still passing `contract_version: "1.0"` are rejected with `UNSUPPORTED_CONTRACT_VERSION_FROM_CALLER` and pointed at the migration guide.

### Deprecation Flow Example

Suppose `findings[].confidence` (currently float 0-1) needs to change to a categorical enum (`low|medium|high`) in 2.0:

```yaml
# Release 1.5 (announcement)
findings:
  - confidence: 0.92                   # 1.x field, still present
    confidence_tier: "high"            # 2.0 field, also present
deprecations:
  - field: "findings[].confidence"
    replacement: "findings[].confidence_tier"
    removal_in_version: "2.0"
    removal_after_date: "2026-12-01"
```

Callers reading 1.5 output can use either field. Callers writing inputs don't need to change yet.

### Backward Compat Policy

The skill internals MUST carry the prior 2 minor versions of the contract. So when 1.3 ships, callers passing `contract_version: "1.1"` still work. When 2.0 ships, 1.x is dropped from the carry-window (deprecation already happened).

### How Callers Know a Migration Is Needed

Three signals, in order of subtlety:

1. **Deprecations field** in every envelope they receive (machine-readable)
2. **Notices section** in the markdown report (human-readable)
3. **CHANGELOG.md** in `docs/skills/octocode-deep-dive-changelog.md` (release notes)

---

## What This Cannot Do

Honest limits — what callers MUST handle elsewhere:

| Limit | What this skill does NOT do | What the caller does instead |
|---|---|---|
| Target discovery | Does not figure out which repos to investigate | Caller (tech-research, /tdd Stage A) provides targets |
| Local codebase | Does not read local source files | auggie / serena / Read |
| Library docs | Does not return canonical API documentation | context7 |
| Broad web search | Does not search blogs, Stack Overflow, forums | tavily / WebSearch |
| Persistent storage | Does not maintain cross-invocation findings DB | Caller's MDTM task dir persists artifacts; cache_hints round-trip between calls but the skill is stateless between invocations |
| Implementation plan generation | Does not produce implementation steps | Caller (synthesis agents, /tdd, /sc:roadmap) does this from findings |
| Real-time updates | Does not stream findings as they're produced | Findings are returned as a complete envelope at end-of-invocation; the skill is synchronous |
| GitHub Enterprise auth | Does not handle custom auth flows out-of-box | Octocode-mcp's underlying GitHub Enterprise config applies; caller's responsibility to ensure auth is set up |
| Hallucination prevention beyond evidence tags | Does not LLM-verify that findings are *relevant* (only that they exist) | rf-qa-qualitative agents in caller pipelines spot-check |
| Concurrent invocation limit | Does not coordinate across parallel callers | The 30 req/min global rate limit is shared; budget accounting per-invocation does NOT protect against the system-wide cap; caller orchestrators must serialize when needed |
| Tool churn upstream | Does not abstract away octocode-mcp version churn | Phase 0 pinning + manual migration on each octocode-mcp major version |
| Cross-host federation | Does not federate across multiple GitHub hosts in one invocation | One host per invocation; caller invokes once per host |

---

## Status: Complete

The scribe defense in summary: the contract IS the funnel. Without a stable, schema-enforced, versioned, anti-pattern-rejecting contract, octocode-deep-dive becomes the same fork-pile in skill clothing that distributed v2 already would be. With it, the funnel earns its name — every caller passes the same shape in, every caller parses the same shape out, every breaking change is announced and migratable, and every misuse fails loudly with a teachable error message.

The architect (Proposal A) will argue this directory layout makes the consolidation clean. The analyzer (Proposal B) will argue these metrics make the consolidation measurable. Both proposals presuppose the contract holds. This proposal makes the contract hold.
