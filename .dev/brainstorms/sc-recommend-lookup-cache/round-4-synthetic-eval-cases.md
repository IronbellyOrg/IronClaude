---
artifact: round-4-spec
parent_brainstorm: .dev/brainstorms/sc-recommend-lookup-cache/merged-requirements.md
generated: 2026-06-02T21:30:00Z
generator: orchestrator (single advocate, no panel)
status: draft — awaiting user review
auggie_grounded: true
---

# Round 4: Synthetic Eval-Case Generation for Plugin Adoption

## Problem Statement

The round-3 spec made plugin adoption gated on a with-resource vs without-resource eval delta (pass-rate +≥10pp OR token −≥20% with no regression). It did NOT specify where those eval cases come from. The iteration-1 evals test the `sc-recommend` skill itself ("would `/sc:spec-panel` be surfaced for this prompt?"). Those cases are unrelated to whether a Notion MCP server makes Notion-touching tasks better.

Round 4 fills that gap: **per-plugin synthetic eval cases generated from the plugin's stated capabilities, reviewed by the user, then executed via the existing cliEval harness**.

## Key Auggie Findings (load-bearing precedents)

This spec aggressively reuses existing infrastructure rather than building new. Six precedents surfaced by the round-4 auggie sweep:

1. **`src/superclaude/cli/install_mcp.py:check_mcp_server_installed(server_name)`** — Already parses `claude mcp list` output to verify an MCP server is installed. Direct answer to OQ2 self-check. Also: `check_binary_available()`, `check_docker_available()`, `check_prerequisites()` follow the same pattern.

2. **`src/superclaude/cli/eval/suites/*.yaml`** — cliEval real-eval harness already has a structured YAML suite format with `evals: [{id, title, category, isolation, inputs, ...}]`, `required_binaries:`, and `optional_capabilities:`. Plugin eval suites become new entries in this directory.

3. **`src/superclaude/cli/eval/suites/model_capability_matrix.yaml`** — Already does multi-model comparison ("spawn opus, sonnet, haiku on the same source task and score variants"). Direct template for the `--eval normal`/`deep` model panels.

4. **`src/superclaude/cli/eval/suites/adversarial_merge_consistency.yaml`** — Runs the same invocation 3× varying only the judging model family. Directly analogous to the `--eval deep` 3×3 fan-out.

5. **`.dev/eval-workspaces/sc-reflect/grader.py`** — Has assertion types beyond text matching: `file_exists`, `check_checkpoint_logged` (parses JSONL audit logs post-run). This is the **tool-use log inspection precedent** — grade by reading subagent transcripts, not just final text output.

6. **`isolation: { home_strategy: seeded, seed_state: [{path, content}] }`** — Established cliEval pattern for seeding fixture files into per-eval HOMEs. Plugin evals use this to set up test data (e.g., a fixture Notion workspace state) without polluting the real env.

The rest of this spec is a thin extension on top of these six.

## Pipeline (3 stages, gated by user review)

```
Plugin discovery (existing Phase 3 of sc-recommend)
   │
   ▼
Stage 1: Capability extraction (Haiku, ~3K tokens)
   │       → list of "{verb} {noun}" capability statements from README + metadata
   ▼
Stage 2: Synthetic eval-case generation (Haiku or Sonnet, ~30K tokens)
   │       → emits cliEval-compatible suite YAML draft
   ▼
Stage 3: User review gate (interactive, no LLM cost)
   │       → user approves / edits / rejects via eval-viewer HTML
   ▼
Approved suite committed to .claude/cache/eval-runs/synthetic-cases/<plugin-key>.yaml
   │
   ▼
Plugin eval pipeline runs (existing cliEval harness + --eval mode panels)
   │
   ▼
Adoption decision (existing round-3 threshold logic)
```

## Stage 1: Capability Extraction

**Input**: Plugin row from `.claude/cache/sc-recommend-plugin.yaml` (post-discovery, pre-eval). Specifically: `candidate`, `repo_url`, `source_url`, and any README content fetched by tech-research/Tavily during discovery.

**Worker**: Haiku subagent (per user's Haiku-only constraint).

**Prompt shape** (~80 lines, including 2-3 few-shot examples):

```text
<ROLE>
You extract the discrete capabilities a plugin/MCP server provides from its
README and metadata. Output a structured list. Be concrete — avoid marketing
phrasing.
</ROLE>
<PLUGIN>
Name: <candidate>
Source: <repo_url>
README excerpt: <first ~2K chars from fetched README>
Capability summary: <one-liner from discovery>
</PLUGIN>
<OUTPUT>
List 5-10 capabilities. Each line is a single capability in "{verb} {noun}
[with {qualifier}]" form. NO marketing phrasing. Example:
- search notion workspace by keyword
- fetch notion page by ID and return content
- create notion database row from structured input
- (negative — should NOT be expected) generate calendar events
</OUTPUT>
```

The "negative" hint asks Haiku to surface 1-2 capabilities the plugin probably does NOT do — important for generating genuine without-resource expectations.

**Output**: capability list + 1-2 negative-control capabilities. Cost: one Haiku call, ~3K tokens.

## Stage 2: Synthetic Case Generation

**Input**: Capability list from Stage 1 + plugin row metadata.

**Worker**: Haiku by default, with explicit user override to Sonnet/Opus when stakes are high. *Decision deferred to user as round-4 OQ4 below.*

**Output schema** — a cliEval-compatible suite YAML written to a draft file:

```yaml
# yaml-language-server: $schema=src/superclaude/cli/eval/suites/suite.schema.json
name: plugin-eval-<plugin-key>
version: "1.0"
description: "Synthetic adoption eval for <plugin candidate>"
generator: sc-recommend/--eval round-4 (Haiku synthesis + user review)
generated: 2026-06-XX
source_plugin_row: .claude/cache/sc-recommend-plugin.yaml#<plugin-key>
source_capabilities:
  - search notion workspace by keyword
  - fetch notion page by ID
  - create notion database row
  - (negative-control) generate calendar events

defaults:
  per_eval_timeout_sec: 300
  capture_tty: true
  keep_home_on_success: false

required_binaries:
  - { name: claude, min_version: "0.5.0", failure_mode: hard }

# NEW (round-4) — preconditions are checked BEFORE any eval runs.
# Resolves OQ2: block on self-check failure with explicit message.
preconditions:
  - kind: mcp_server_installed
    server: <plugin-key>
    failure_mode: hard
    failure_message: |
      Plugin '<plugin-key>' is not installed.
      Run the install command first:
          <install_command from plugin row>
      Complete any auth/OAuth steps, then re-run with --eval <mode>.

evals:
  # ── Positive case ───────────────────────────────────────────────────
  - id: NC1
    title: "Search workspace and extract structured items"
    capability: "search + read"           # which capability this case tests
    configuration: with_resource          # NEW: with_resource | without_resource | both
    timeout_sec: 300
    isolation:
      home_strategy: seeded
      seed_state:
        - path: query.txt
          content: |
            Find the page titled 'Q4 roadmap' in my Notion workspace
            and list its milestones.
    inputs:
      - prompt: "Read query.txt and complete the request using available tools."
    assertions:
      - text: "Plugin tool was actually invoked (not hallucinated)"
        type: tool_use_present
        tool_name_pattern: "^notion_(search|get_page)$"
      - text: "Output references 'milestone' or 'roadmap'"
        type: regex_match
        value: "(?i)(milestone|roadmap)"
      - text: "Output is concrete (cites page ID or specific milestone names)"
        type: regex_match
        value: "(?i)([a-f0-9-]{8}|m[12345]|milestone\\s+\\d)"

  # ── Same prompt, without resource — used to compute delta ─────────────
  - id: NC1_without
    title: "Same as NC1 but without the plugin enabled"
    capability: "search + read"
    configuration: without_resource
    pair_id: NC1                           # links this to NC1 for delta computation
    timeout_sec: 300
    isolation:
      home_strategy: seeded
      seed_state:
        - path: query.txt
          content: |
            Find the page titled 'Q4 roadmap' in my Notion workspace
            and list its milestones.
    inputs:
      - prompt: "Read query.txt and complete the request using available tools."
    assertions:
      - text: "Output explicitly acknowledges lack of Notion access"
        type: regex_match
        value: "(?i)(cannot access|don't have|no notion|no access to)"
      - text: "Output does NOT fabricate a page ID or milestone names"
        type: regex_match_not
        value: "(?i)(milestone\\s+\\d|M[12345].*completed)"

  # ── Negative control: capability the plugin should NOT handle ──────────
  - id: NC_neg_1
    title: "Calendar request — plugin should NOT claim to handle this"
    capability: "(negative-control) generate calendar events"
    configuration: with_resource          # WITH plugin enabled, but expectation = refuse
    timeout_sec: 300
    inputs:
      - prompt: "Create a calendar event for next Tuesday at 2pm titled 'sync'."
    assertions:
      - text: "Output declines or redirects (does NOT invoke notion tools)"
        type: tool_use_absent
        tool_name_pattern: "^notion_.*$"
      - text: "Output acknowledges the limitation"
        type: regex_match
        value: "(?i)(cannot|not able|no.*calendar)"

# Delta-gate (round-3 adoption threshold, enforced after all evals run)
adoption_gate:
  threshold_pass_rate_delta: 0.10        # +10pp with-resource over without-resource
  threshold_token_delta: -0.20            # -20% tokens (negative = improvement)
  must_not_regress: ["pass_rate"]         # without-resource pass rate cannot drop below baseline
  on_negative_verdict: write_evaluated_negative_row_with_30d_ttl
```

**Three new assertion types** the grader must support:

| Type | Mechanism | Source |
|---|---|---|
| `tool_use_present` | Read subagent transcript JSONL, grep for tool_use entries matching `tool_name_pattern` regex | NEW; precedent in `.dev/eval-workspaces/sc-reflect/grader.py:check_checkpoint_logged` |
| `tool_use_absent` | Inverse of above | NEW; same precedent |
| `regex_match_not` | Inverse of `regex_match` | Already implemented in `.dev/eval-workspaces/sc-recommend/grader.py` |

`tool_use_present`/`absent` require cliEval to **persist the subagent's tool-use transcript** to a deterministic path. The harness already captures `.output` files (full JSONL transcripts) — the new code is a thin parse-and-filter step.

**Cost**: one Haiku call per capability × ~5-10 capabilities + 1-2 negative-control cases = roughly 6-12 calls × ~3K tokens each = ~20-35K tokens for case generation.

**Pairing**: every positive case (`configuration: with_resource`) MUST have a paired `configuration: without_resource` case with the same `pair_id` and same isolation/inputs. This is what makes the delta meaningful.

## Stage 3: User Review Gate (interactive, mandatory)

**Why mandatory**: LLM-generated test cases are notoriously plausible-but-wrong. Without human review, every plugin adoption is gated by Haiku's interpretation of the README, which is exactly the kind of unverified premise the round-3 R3 amendments were guarding against.

**Mechanism**: reuse the iteration-1 `generate_review.py` eval-viewer with a new `--mode synthetic-case-review` flag (or call directly with `--static` since we have Cowork-style display constraints):

1. Generated YAML draft written to `.claude/cache/eval-runs/synthetic-cases/drafts/<plugin-key>.yaml`
2. Reviewer HTML written next to it: `<plugin-key>-review.html`
3. User opens HTML, sees each case (prompt + assertions side-by-side with the without-resource pair)
4. User clicks approve / edit / reject per case
5. On submit, downloads `<plugin-key>-feedback.json`
6. Orchestrator reads feedback, applies user edits, writes final suite to `.claude/cache/eval-runs/synthetic-cases/<plugin-key>.yaml` (tracked, committed)

**Approval criteria the user should consider** (surfaced in the review HTML):
- Does the prompt actually test the capability claimed?
- Does the without-resource expectation make sense (is "no Notion access" actually what the model would say, or would it just web-search)?
- Are the assertions falsifiable (vs vague "should be useful")?
- Does the negative-control case actually probe a capability gap?

**No commit without review**: a draft suite that hasn't been user-approved gets `status: draft` in its frontmatter. The plugin-eval pipeline (Stage 4 / round-3) refuses to run against a draft suite. Hard gate.

## Stage 4 (existing round-3): Run the suite + compute adoption verdict

This is unchanged from round-3 — the suite runs via cliEval, `--eval <mode>` controls the model panel, `adoption_gate` thresholds are applied, and `adoption_status` is written back to the plugin lookup-table row. The only round-4 additions feeding into Stage 4 are:

- `preconditions:` block runs `check_mcp_server_installed()` (or equivalent for non-MCP plugins) BEFORE any eval. Failure → abort with the spec'd message. (OQ2 resolution.)
- `tool_use_present`/`tool_use_absent` assertion grading.
- `configuration: with_resource | without_resource` pairing for delta computation.

## Schema Additions to `suite.schema.json`

Concrete cliEval schema delta this round-4 introduces:

```yaml
# Per-eval additions
configuration:
  type: string
  enum: [with_resource, without_resource, both]
  default: both          # backward-compatible; existing suites unaffected

pair_id:
  type: string
  description: "Links a without_resource eval to its with_resource counterpart for delta computation"

capability:
  type: string
  description: "Free-text capability label; used for grouping cases in the eval-viewer"

# Suite-level additions
preconditions:
  type: array
  items:
    type: object
    properties:
      kind: { enum: [mcp_server_installed, binary_available, file_present] }
      server: { type: string }         # for mcp_server_installed
      binary: { type: string }         # for binary_available
      path:   { type: string }         # for file_present
      failure_mode: { enum: [hard, warn, skip] }
      failure_message: { type: string }

adoption_gate:
  type: object
  properties:
    threshold_pass_rate_delta: { type: number, minimum: 0, maximum: 1 }
    threshold_token_delta: { type: number, minimum: -1, maximum: 0 }
    must_not_regress: { type: array, items: { enum: [pass_rate, tokens, duration] } }
    on_negative_verdict: { enum: [write_evaluated_negative_row_with_30d_ttl, write_uninstalled_row, discard] }

# New assertion types (additions to existing enum)
assertion_types:
  - tool_use_present:
      tool_name_pattern: { type: string, format: regex }
  - tool_use_absent:
      tool_name_pattern: { type: string, format: regex }
```

All additions are backward-compatible — existing cliEval suites without these fields continue to run unchanged.

## Cost Summary (per plugin adopted)

| Stage | Worker | Cost (tokens) | Wall time |
|---|---|---|---|
| Discovery (existing) | Tavily / tech-research | ~10-30K | ~30s |
| Stage 1: capability extraction | Haiku | ~3K | ~10s |
| Stage 2: case generation | Haiku (default) | ~20-35K | ~60s |
| Stage 3: user review | human | 0 | varies (~5 min) |
| Stage 4: eval execution | per `--eval` mode | ~90K-1.6M | 70s-15min |
| **Total before adoption decision** | | **~120K-1.7M** | **~6-17 min** |

The cost is real but bounded and user-driven. A user evaluating 5 plugins in a session at `--eval normal` is ~2M tokens. At `--eval deep` it's ~9M. Worth ranging an `--eval-budget` flag in a future round.

## Open Questions (round-4)

### OQ4 (round-4): Generator-worker model choice

The Haiku-only constraint applies to sc-recommend's HOT PATH (the cost-sensitive lookup). Synthetic case generation is opt-in, per-plugin, run-once-per-plugin work that lands in a tracked, committed suite YAML reviewed by a human before use.

**Should Stage 2 (case generation) be allowed to use Sonnet/Opus despite the Haiku-only constraint?** Trade-offs:

- **Haiku (strict adherence)**: matches round-3 hard constraint. Generated cases reflect what Haiku can produce. If Haiku-generated cases are weaker (vague assertions, missed capabilities), the user review gate is the safety net — but more cases get rejected, more iterations needed.
- **Sonnet/Opus (relax for off-hot-path generation)**: higher case quality, fewer review-and-redo cycles. Inconsistent with the "all work on Haiku" framing but consistent with the "Haiku-only on hot path, opt-in evaluation can be heavier" pragmatic reading.

I lean toward Sonnet for Stage 2 (per-plugin, one-time, user-gated, off hot-path) but defer the decision.

### OQ5 (round-4): Cases-per-plugin target

5? 10? 20? Cost scales linearly. 5 cases × 1 model × 2 configurations (with/without) = 10 runs at `quick` mode = ~900K tokens. 20 cases at `deep` = ~9M tokens. The right answer probably depends on plugin scope — narrow plugins (single capability) get fewer; broad plugins (Notion, with search + read + write + database) get more. Round-4 spec says "5-10" as Stage 1's target — finalize?

### OQ6 (round-4): Negative controls — how many?

Round-4 spec says "1-2 negative-control capabilities". Negative controls are load-bearing for catching false-positive adoptions (the plugin claims X, but if X requests succeed identically with and without the plugin, X isn't real). But each negative control doubles its cost. Default 1, allow user to bump?

### OQ7 (round-4): Suite TTL

Synthetic eval suites are tied to a specific plugin version. When the plugin's `source_hash` changes (new version published), do generated cases automatically invalidate? Or do they stay valid until manual re-run? Suggests adding `suite.bound_to_plugin_hash: <hash>` and treating any mismatch as a hard-fail until regenerated.

## What Round 4 Explicitly Does NOT Do

- **Does not auto-generate cases on plugin discovery**. Generation happens only when `--eval <mode>` is passed AND the user has opted into adoption-decision flow.
- **Does not auto-approve cases**. Human review is mandatory; the system refuses to run a draft suite.
- **Does not write to plugin's actual data**. All cases use seeded fixture state or read-only operations against the user's account. Generators MUST NOT propose cases that perform irreversible mutations (deleting pages, sending messages, etc.). Stage 1 prompt to be hardened with explicit "no mutation" instructions.
- **Does not support non-Claude clients**. The `mcp_server_installed` precondition assumes `claude mcp list`. If the plugin ships for ChatGPT/Cursor/VSCode, those need separate precondition kinds — out of scope for round-4.

## Files Touched (round-4 implementation scope)

| File | Change | LoC est. |
|---|---|---|
| `src/superclaude/cli/eval/suites/suite.schema.json` | Add `configuration`, `pair_id`, `capability`, `preconditions`, `adoption_gate`, new assertion types | ~50 |
| Existing grader.py implementations (`.dev/eval-workspaces/sc-recommend/grader.py` and/or `cli/eval/grader.py`) | Add `tool_use_present`, `tool_use_absent`, transcript-log parser | ~80 |
| `src/superclaude/cli/sc_recommend/synthetic_cases.py` (NEW) | Stage 1 + Stage 2 orchestrator: spawn Haiku, parse output, write draft suite | ~150 |
| `src/superclaude/cli/sc_recommend/review_workflow.py` (NEW) | Stage 3: invoke generate_review.py, consume feedback.json, emit final suite | ~100 |
| `.claude/cache/eval-runs/synthetic-cases/` (tracked directory created on first plugin eval) | n/a | 0 |
| `.gitignore` | Add `!.claude/cache/eval-runs/synthetic-cases/**` | 1 line |

Round-4 implementation total: ~380 LoC + the schema delta. About the same size as round-3's eval-pipeline implementation; sits cleanly on top.
