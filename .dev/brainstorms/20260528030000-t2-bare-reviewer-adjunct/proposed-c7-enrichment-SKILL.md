---
name: c7-enrichment
description: Caller-agnostic documentation enrichment skill — detects libraries from a target file, resolves them via context7, fetches lens-derived doc queries, optionally indexes the result via auggie, and writes a SYNTHESIS.md artifact + structured return contract for the caller to inject into downstream prompts.
allowed-tools: Read, Glob, Grep, Bash, Write, mcp__context7__resolve-library-id, mcp__context7__query-docs, mcp__auggie__codebase-retrieval
model: sonnet
---

# c7-enrichment — Documentation Enrichment Skill

<!-- Extended metadata (for documentation, not parsed):
category: infrastructure
complexity: standard
mcp-servers: [context7, auggie]
personas: [analyzer, scribe]
model-escalation: opus when challenge_label="custom" with complex --custom-queries
delegate-only: true (no /sc:c7-enrichment user command)
-->

## Purpose & Identity

`c7-enrichment` is a **callable infrastructure skill** that turns a target file into a small bundle of documentation context. It runs the seven-step enrichment pipeline that was originally inlined in `sc-bare-review` Wave B.5 (v1.1) and was extracted into a standalone skill in v1.2 per the adversarial debate at `adversarial/c7-agent-debate.md` (Variant B selected).

**What this skill IS:**

- A pure delegation target invoked by other commands/skills (e.g., `sc-bare-review`, `/sc:auggie-review`, `/sc:troubleshoot`, `/sc:reflect`, `/sc:code-review`, `/sc:tech-research`).
- A self-contained owner of: library detection, context7 resolution, lens-driven query derivation, doc fetching, auggie-indexing decision, synthesis artifact generation, and a structured return contract.
- Caller-agnostic. The caller picks the lens (`--challenge-label`) and the output dir; the skill does the rest.

**What this skill IS NOT:**

- Not a reviewer, not a debater, not a fixer — it produces context, never opinions on the target.
- Not user-invoked. There is no `/sc:c7-enrichment` slash command. The skill exists only as a delegate.
- Not a substitute for the `c7-context-analyst` agent. If the lens taxonomy grows past 8 labels or `--custom-queries` usage exceeds 30% over a 4-week window, the skill is promoted to a Task agent per §18.6 of the merged requirements. The promotion is mechanical because skill and agent share the same API + return contract.

**Compliance tier:** STANDARD — multi-MCP integration, network-bound, fail-soft on every external dependency.

## Required Input

```
Skill c7-enrichment
  --target <path>                    # File to enrich (REQUIRED)
  --challenge-label <str>            # Lens label (REQUIRED) — one of: troubleshooting,
                                     #   completeness-audit, feasibility-study, code-review,
                                     #   spec-review, custom
  --output <dir>                     # Output directory (REQUIRED) — skill writes <dir>/c7-context/
  --custom-queries <comma-list>      # REQUIRED only when --challenge-label=custom
  --libs <comma-list>                # Optional explicit library names; overrides auto-detection
  --query-cap <N>                    # Max docs queries (default 6)
  --timeout-sec <N>                  # Total wall-clock budget (default 45)
  --auggie-threshold-tokens <N>      # Token threshold for auggie indexing (default 8000)
  --auggie-threshold-libs <N>        # Lib-count threshold for auggie indexing (default 3)
```

## Triggers

- **Delegate-only.** Invoked as `Skill c7-enrichment ...` from caller commands or other skills.
- **Not user-invoked.** Never appears as a slash command. No keyword trigger surface — the only entry point is explicit `Skill` invocation by an upstream pipeline.
- Active in caller pipelines when the caller's `--c7` flag is set OR the corresponding env (e.g., `T2C7Enable=true`) is true.

## Prerequisites (before Step 1)

**Purpose**: Validate environment and inputs before any network or filesystem work. Fail fast on contract violations.

1. **Required-arg guard.** If any of `--target`, `--challenge-label`, `--output` are missing → STOP with explicit error naming the missing flag(s).
2. **Lens-label validity.** `--challenge-label` MUST be one of the 6 taxonomy values OR `custom`. Invalid → STOP with the full list of accepted labels.
3. **Custom-queries pairing.** If `--challenge-label=custom`, `--custom-queries` MUST be non-empty → STOP otherwise.
4. **Target existence.** Resolve `--target` to an absolute path; STOP if it does not exist or is not readable.
5. **Output writability.** Create `<output>/c7-context/` if missing. STOP if the parent is not writable.
6. **Forbidden-prefix guard.** Refuse if `--output` resolves under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/`. These prefixes are reserved for distributable components. Redirect to `.dev/` per the `.dev/README.md` rule.

**Exit Criteria:** All prerequisites validated. Emit: `c7-enrichment: prerequisites validated, target=<path>, lens=<label>, output=<dir>`.

## Behavioral Protocol — 7 Steps

Same pipeline that lived inline in `sc-bare-review` Wave B.5 (v1.1), now wholly owned by this skill. All steps fail soft — a failure at any step emits the return contract per §18.5 and proceeds with whatever the caller can use.

### Step 1: Library Detection

```yaml
library_detection:
  if_libs_provided: "Use --libs verbatim (skip auto-detect)"
  else_auto_detect:
    Go:         "grep ^import + import blocks; extract quoted package paths"
    Python:     "grep ^from + ^import lines"
    TS_JS:      "grep ^import ... from + require() calls"
    Rust:       "grep ^use; collect top-level crate names"
    Markdown:   "Extract backticked library mentions + YAML frontmatter library fields"
  cap: 8 candidates (prefer most-frequently-mentioned if over)
  output: candidates_detected list (names only, no IDs yet)
  empty_set: "WARN, emit return contract with status=skipped_no_candidates, EXIT"
```

### Step 2: Library ID Resolution

```yaml
library_id_resolution:
  action: "Parallel mcp__context7__resolve-library-id for each detected candidate"
  parallelism: "Single message block — all resolve calls dispatched simultaneously"
  unresolved_handling: "WARN with the specific name; drop from list; continue"
  output:
    candidates_resolved: [(name, context7_id), ...]
    candidates_dropped: [names that failed to resolve]
  empty_resolved: "WARN, emit return contract with status=skipped_no_candidates, EXIT"
  mcp_unavailable: "WARN, emit return contract with status=failed (failure_stage=resolve), EXIT"
```

### Step 3: Documentation Fetch (lens-driven)

```yaml
documentation_fetch:
  query_derivation:
    source: "Lens → query template map from refs/lens-queries.md (per §18.4)"
    instantiation:
      - "Substitute {lib} with detected library name"
      - "Substitute {target_function}, {target_section}, {detected_concept} from target analysis"
    custom_lens: "Use --custom-queries verbatim, one per query slot"
  per_library:
    action: "mcp__context7__query-docs for each (resolved_lib, lens_query) pair"
    write: "<output>/c7-context/<libname-slug>.md"
  query_cap: "Cumulative across all libraries; honor --query-cap (default 6)"
  budget_overflow: "Cap remaining queries at the limit; flag status=partial"
  empty_per_lib: "Drop that library only; continue others"
  cumulative_token_cap: "30K tokens — truncate excess; flag truncated=true"
  timeout_handling: "If elapsed > --timeout-sec, abort remaining queries; status=partial"
```

### Step 4: Auggie Indexing Decision

```yaml
auggie_indexing_decision:
  thresholds:
    tokens: --auggie-threshold-tokens (default 8000)
    libs:   --auggie-threshold-libs   (default 3)
  rule: |
    IF cumulative_docs_token_count > tokens_threshold
       OR len(candidates_resolved) >= libs_threshold:
      auggie_mode = enabled
    ELSE:
      auggie_mode = direct_inline
  rationale: "Small corpora are cheaper to paste verbatim than to index; large corpora need retrieval."
```

### Step 5: Auggie Query (conditional)

```yaml
auggie_query:
  condition: "auggie_mode == enabled"
  action: "mcp__auggie__codebase-retrieval indexed against <output>/c7-context/"
  query_count: "Up to 3 synthesis queries derived from target (function names, imports, file purpose)"
  unavailable_fallback:
    trigger: "mcp__auggie__codebase-retrieval not reachable"
    action: "Fall back to auggie_mode=bypassed_on_failure; direct_inline behavior; WARN; do NOT abort"
  output: "Retrieval excerpts → consumed by Step 6 synthesis"
```

### Step 6: Synthesis Artifact

```yaml
synthesis_artifact:
  output: "<output>/c7-context/SYNTHESIS.md"
  frontmatter:
    status: <success | partial | skipped_no_candidates | failed>
    target: <absolute path>
    challenge_label: <lens>
    candidates_resolved: <list>
    docs_token_count: <int>
    auggie_mode: <enabled | direct_inline | bypassed_on_failure>
    truncated: <bool>
    generated_at: <ISO-8601>
  body:
    - "Top-N most-relevant excerpts (auggie-mode) or full doc concatenation (direct_inline)"
    - "Per-library section headers with provenance: source library, context7_id, query used"
    - "Cap body at 4000 tokens"
```

### Step 7: Return Contract

Emit the structured contract per §18.5 (see Return Contract section below). **Mandatory on every invocation including failures** (write-on-failure pattern, AC-1.29).

### Prompt-Augmentation Note

The skill does NOT inject docs into caller prompts itself. It writes `SYNTHESIS.md` and returns the path in the contract. The caller is responsible for reading the synthesis file and injecting the `<<<DOCS>>>` block into downstream prompts (Wave C in `sc-bare-review`'s case). This keeps the skill caller-agnostic.

## Lens Taxonomy

The `--challenge-label` parameter selects from this taxonomy. Each lens picks 2-4 query templates instantiated with the detected library name and (where applicable) target-derived concepts.

| Lens label | Use case | Representative query templates |
|------------|----------|--------------------------------|
| `troubleshooting` | `/sc:troubleshoot` pipeline | "What are common error modes in {lib}?" / "What breaks {lib} {target_function}?" / "What are recent CVEs or known issues in {lib}?" |
| `completeness-audit` | `/sc:reflect` post-execution audit | "What is the full public API surface of {lib}?" / "What edge cases does {lib} {target_function} handle?" / "What are documented invariants of {lib}?" |
| `feasibility-study` | `/sc:tech-research`, brainstorm | "What does {lib} support out of the box?" / "What are {lib}'s scaling limits?" / "What integration patterns does {lib} recommend?" |
| `code-review` | `sc-bare-review` (default for bare adjunct), `/sc:code-review` | "What are {lib} API contracts that {target} uses?" / "What are common pitfalls or breaking changes in {lib}?" / "How does {lib} handle {detected_concept}?" |
| `spec-review` | `/sc:spec-panel`, design review | "What does {lib} document about {target_section}?" / "Are there ambiguities or open questions in {lib} docs around {detected_concept}?" |
| `custom` | Power-user override | Uses `--custom-queries` list verbatim |

**Lens governance.** The full lens→queries map (with per-template prompt fragments and substitution variables) lives in `src/superclaude/skills/c7-enrichment/refs/lens-queries.md`. **This is the central registry.** Adding a new lens is a refs-file change, not a skill-version bump. PR review is required to add a lens to prevent namespace inflation (mitigation for R-V12-4). When the lens map grows beyond 8 entries, the skill is a promotion candidate per §18.6.

## Return Contract (MANDATORY)

**This is the final pipeline step.** `c7-enrichment` MUST write this return contract on every invocation, including failures. When a field cannot be determined (pipeline aborted before reaching that step), use `null`.

```yaml
contract_version: "1.0"
status: success | partial | skipped_no_candidates | failed
target: <absolute path>
challenge_label: <e.g., code-review>
candidates_detected: [list of names from detection]
candidates_resolved: [list of (name, context7_id) pairs]
candidates_dropped: [list of names that did not resolve]
docs_token_count: <int cumulative>
auggie_mode: enabled | direct_inline | bypassed_on_failure | n_a
synthesis_path: <absolute path to SYNTHESIS.md or null>
c7_context_dir: <absolute path>
elapsed_ms: <int>
truncated: <bool — true if docs_token_count was capped at 30K>
failure_stage: <null | detect | resolve | fetch | auggie | synthesis>
```

**Write-on-failure**: If any step aborts, the skill MUST still write the return contract with `status: failed` (or `partial` if some docs landed), `failure_stage` set to the step that failed, and unreached fields set to `null`. The caller can always consume the contract (AC-1.29).

| Field | Type | Description |
|-------|------|-------------|
| `contract_version` | `string` | Schema version; current `1.0` |
| `status` | `enum` | `success` / `partial` / `skipped_no_candidates` / `failed` |
| `target` | `string` | Absolute path to the enriched target |
| `challenge_label` | `string` | The lens label used |
| `candidates_detected` | `list` | Raw output of Step 1 |
| `candidates_resolved` | `list` | (name, context7_id) pairs from Step 2 |
| `candidates_dropped` | `list` | Names that failed resolution; empty on full success |
| `docs_token_count` | `int` | Cumulative tokens fetched across all libraries |
| `auggie_mode` | `enum` | `enabled` / `direct_inline` / `bypassed_on_failure` / `n_a` |
| `synthesis_path` | `string\|null` | Path to SYNTHESIS.md; null if synthesis not reached |
| `c7_context_dir` | `string` | Always set (created in Prerequisites) |
| `elapsed_ms` | `int` | Wall-clock spent in the skill |
| `truncated` | `bool` | True iff 30K token cap kicked in |
| `failure_stage` | `string\|null` | Null on success; identifies aborting step otherwise |

## Failure Modes

Adapted from `merged-requirements.md §16.6` — now owned skill-side, not caller-side.

| Scenario | Skill behavior |
|----------|----------------|
| `--target` missing or unreadable | STOP in Prerequisites; no return contract written (input contract violation) |
| `--challenge-label` invalid | STOP in Prerequisites with full list of accepted labels |
| `--challenge-label=custom` with no `--custom-queries` | STOP in Prerequisites |
| No candidate libraries detected | WARN, emit contract with `status=skipped_no_candidates`, EXIT (NOT a failure) |
| `mcp__context7__resolve-library-id` unavailable | WARN, emit contract with `status=failed`, `failure_stage=resolve`, EXIT |
| `mcp__context7__query-docs` returns empty for a resolved library | Drop that library; continue with others |
| `--libs` lists unresolvable name | WARN with the specific name, drop, continue (not a STOP) |
| Cumulative docs token count exceeds 30K | Truncate to 30K most-relevant; flag `truncated: true` in synthesis frontmatter + return contract |
| `mcp__auggie__codebase-retrieval` unavailable when `auggie_mode=enabled` | Fall back to `direct_inline`; set `auggie_mode=bypassed_on_failure`; WARN; do NOT abort |
| Wall-clock exceeds `--timeout-sec` | Abort remaining queries; emit `status=partial` with whatever docs landed |
| Same target enriched twice into same `<output>` | `c7-context/` overwritten (deterministic; auto-detect is stable) — acceptable per spec |

## Boundaries

### Will Do

- Detect candidate libraries from a target file across Go / Python / TS-JS / Rust / Markdown
- Resolve names via `mcp__context7__resolve-library-id`
- Fetch lens-derived doc queries via `mcp__context7__query-docs`
- Decide auggie indexing based on token + lib-count thresholds
- Query `mcp__auggie__codebase-retrieval` against the fetched docs when enabled
- Write `SYNTHESIS.md` with frontmatter + body (capped at 4000 tokens)
- Emit a structured return contract on every invocation (success or failure)
- Operate as a delegate of any caller without caller-specific code paths

### Will Not Do

- **Not inject docs into caller prompts.** Skill returns the synthesis path; caller injects.
- **Not run as a user-invoked command.** No `/sc:c7-enrichment`; pure infrastructure.
- **Not reason about the target's content.** It picks queries from the target's libraries and lens, nothing more.
- **Not maintain its own metrics store.** Caller (or a higher-level metrics shim) tracks invocation counts for AC-1.32 / promotion-trigger evaluation.
- **Not perform multi-step reasoning.** If multi-step ("fetch A, decide what B to fetch based on A") is needed, the spec mandates promotion to the `c7-context-analyst` agent per §18.6.
- **Not write outside `<output>/c7-context/`.**
- **Not produce review opinions** about the target — context only.

## MCP Integration

| Server | Tool | Used in | Circuit-breaker behavior |
|--------|------|---------|--------------------------|
| context7 | `mcp__context7__resolve-library-id` | Step 2 | Unavailable → WARN, contract `status=failed`, `failure_stage=resolve`, EXIT |
| context7 | `mcp__context7__query-docs` | Step 3 | Per-library empty → drop lib, continue. All empty → `status=partial` or `failed` per coverage |
| auggie | `mcp__auggie__codebase-retrieval` | Step 5 (conditional) | Unavailable → fall back to `direct_inline`, set `auggie_mode=bypassed_on_failure`, do NOT abort |

**No upstream MCP server is allowed to abort the skill.** Every failure path is fail-soft and emits a contract.

## Model Recommendation

- **Default: sonnet.** The skill is mostly deterministic plumbing (detection, resolution, fetch, synthesis).
- **Escalate to opus** when `--challenge-label=custom` is set AND `--custom-queries` contains 3+ free-text queries that require non-trivial query understanding to derive substitutions or rank relevance. Caller may pass an explicit model hint via Task launch.

## Acceptance Criteria

Direct translation of `merged-requirements.md §18.8`. These are the skill's own ACs.

- **AC-1.24** — Skill exists at `src/superclaude/skills/c7-enrichment/SKILL.md`; `make sync-dev` syncs to `.claude/skills/c7-enrichment/`.
- **AC-1.25** — Skill API per "Required Input" above; `--target`, `--challenge-label`, `--output` are required; all others optional with documented defaults.
- **AC-1.26** — `--challenge-label` accepts the 6 taxonomy values + `custom`; invalid label → STOP with the available labels listed in the error message.
- **AC-1.27** — `--challenge-label=custom` requires non-empty `--custom-queries`; STOP otherwise.
- **AC-1.28** — Lens taxonomy resides in `refs/lens-queries.md`; adding a new lens does NOT require editing this SKILL.md.
- **AC-1.29** — Return contract per §18.5 is emitted on every invocation including failures (write-on-failure pattern).
- **AC-1.30** — `sc-bare-review` Wave B.5 invokes `Skill c7-enrichment` per §18.2; no inline c7 pipeline logic remains in `sc-bare-review`.
- **AC-1.31** — Skill is caller-agnostic: passes integration tests with at least one non-`sc-bare-review` caller fixture (suggest `/sc:auggie-review` as the second-caller acceptance gate). The skill MUST contain zero caller-specific branches.
- **AC-1.32** — Skill metrics tracked (by caller or shim): invocation count by `challenge_label`, `--custom-queries` usage rate, lens-map size over time. Required for promotion-trigger decisions per §18.6.

## Risks (inherited from §18.9)

| ID | Risk | Skill-side mitigation |
|----|------|----------------------|
| R-V12-1 | Lens taxonomy too narrow; users hit `custom` constantly | Skill emits metrics enabling promotion decision (AC-1.32) |
| R-V12-2 | Skill-invocation overhead larger than expected | Skill runs in caller context — no Task spawn cost |
| R-V12-3 | Two-component coordination bugs (caller ↔ skill) | Strict `contract_version`-tagged return schema; write-on-failure ensures the caller always has a contract |
| R-V12-4 | Lens-map governance drift | `refs/lens-queries.md` is the single source of truth; PR review required to add a lens |
| R-V12-5 | Promotion-trigger metrics not collected → promotion-decision blind | AC-1.32 mandates metric collection from day one |

---

*v1.0 — extracted from `sc-bare-review` Wave B.5 (v1.1) per `merged-requirements.md` §18 (v1.2 amendment, 2026-05-28). Caller-agnostic by construction; promotion path to `c7-context-analyst` agent documented in §18.6.*
