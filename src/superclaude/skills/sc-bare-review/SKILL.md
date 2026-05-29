---
name: sc-bare-review
description: Infrastructure skill that dispatches 2-4 bare (unscaffolded) reviews of a target file in parallel to diverse EXTERNAL models via an OpenAI-compatible proxy, normalizes each into a compressed-markdown template carrying suspect:true, and returns a contract handing the files to /sc:adversarial --suspect-source. Delegate-only — no slash command.
allowed-tools: Read, Glob, Grep, Bash, Write
model: sonnet
---

# sc-bare-review — T2 Bare-Reviewer Adjunct

<!-- Extended metadata (for documentation, not parsed):
category: infrastructure
complexity: standard
mcp-servers: []            # Phase 1 = Bash+curl reference transport; MCP transport is Phase 5
personas: [analyzer, qa]
delegate-only: true        # no /sc:bare-review user command
suspect-by-construction: true
spec: .dev/brainstorms/20260528030000-t2-bare-reviewer-adjunct/merged-requirements.md (v1.3.0-draft §3,§4,§7,§8,§9.1)
-->

## Purpose & Identity

`sc-bare-review` turns a target file into 2-4 independent "bare" reviews — each from a
*different external model* (DeepSeek, Qwen, Kimi, GLM), prompted with no protocol
scaffolding so the model reviews with its native instinct. Bare reviews surface edge
cases and latent risks that structured reviewers miss, **but their hallucinations are
predictable enough to gate against** — so every output is tagged `suspect: true` and is
meant to flow into `/sc:adversarial --suspect-source`, never trusted directly.

**What this skill IS:**

- A pure delegation target invoked as `Skill sc-bare-review …` by caller commands
  (`/sc:troubleshoot`, `/sc:reflect`, `/sc:auggie-review`, `/sc:code-review`,
  `/sc:adversarial`) — wired up in Phase 3.
- A thin orchestrator over three bundled scripts (`scripts/t2_preflight.sh`,
  `scripts/t2_dispatch.sh`, `scripts/t2_normalize.py`). The scripts own the deterministic
  work; this SKILL.md owns sequencing and the single-message parallel dispatch.

**What this skill IS NOT:**

- **Not user-invoked.** There is no `/sc:bare-review` slash command. Pure infrastructure.
- **Not a judge.** It never scores or filters reviews — raw forwarding to `/sc:adversarial`.
- **Not Anthropic-routed.** T2 is explicitly external; routing bare reviewers to Anthropic
  models defeats the diversification purpose.

**Compliance tier:** STANDARD — single-file output × N, network-bound, fail-soft.

## Required Input (§3.2)

```text
Skill sc-bare-review
  --target <path>           # File to review (REQUIRED)
  --reviewers <N>           # Count, 2-4 (default 3)
  --output <dir>            # Output directory (REQUIRED)
  --target-line-cap <N>     # Truncate target to first N lines (default 4000)
  --timeout-sec <N>         # Per-reviewer hard timeout (default 180 / T2Timeout)
  --label <string>          # Optional context label baked into the prompt
  # --c7 / --c7-libs / --c7-query-cap are accepted by callers but wired in Phase 1.5 (no-op here)
```

## Triggers

- **Delegate-only.** Entry point is an explicit `Skill sc-bare-review …` invocation from a
  caller pipeline. No keyword/slash trigger surface.

## Prerequisites

Requires `T2ProxyUrl` + `T2ProxyKey` env vars and `curl` + `jq` on the host. The preflight
script enforces these and STOPs with an actionable message (see Failure Modes). See
`docs/t2-proxy-setup.md` (Phase 4) for example shell config.

## Behavioral Protocol

Resolve the skill directory once, then run the three waves in order.

```bash
# Resolve SKILL_DIR — the directory containing this SKILL.md (installed vs dev).
SKILL_DIR="$HOME/.claude/skills/sc-bare-review"
[ -d "$SKILL_DIR" ] || SKILL_DIR="src/superclaude/skills/sc-bare-review"
```

### Wave A+B — Preflight (single Bash call)

Run the preflight. It validates args/env, resolves the N models, reads + truncates the
target, enforces the IMM-4 empty-target guard, computes the provenance checksum, builds
the shared reviewer prompts, and writes `<output>/manifest.json`.

```bash
"$SKILL_DIR/scripts/t2_preflight.sh" \
  --target <target> --reviewers <N> --output <output-dir> \
  [--target-line-cap <N>] [--timeout-sec <N>] [--label "<label>"]
```

- **Non-zero exit → STOP.** Surface the script's stderr message to the caller verbatim.
  For the empty-target case (exit 3) a `failed` return-contract.yaml has already been
  written; relay it. **Do NOT dispatch any reviewer in this branch** (IMM-4).
- On success, `Read` `<output>/manifest.json`. Its `reviewers[]` array gives, per reviewer:
  `index, model_id, model_label, raw_path, meta_path, final_path`. Also read `timeout_sec`,
  `temperature`, `prompts_dir`.

### Wave C — Parallel dispatch (single message, N Bash calls — AC-1.5 / IMM-3)

> **MANDATORY structural assertion (AC-1.5 / IMM-3).** Before dispatching, assert that you
> are about to emit **exactly `reviewers_requested` `Bash` tool calls in ONE single
> assistant message** — true parallel dispatch. If you cannot guarantee a single message
> block (e.g., you are tempted to dispatch them one per turn), STOP and fix the plan. One
> `t2_dispatch.sh` call per reviewer, all in the same message. Proxy-side serialization is
> acceptable and explicitly out of scope; *client-side* serialization is a violation.

For each reviewer entry in `manifest.reviewers`, emit (in the same message) one call:

```bash
"$SKILL_DIR/scripts/t2_dispatch.sh" \
  --model "<model_id>" \
  --prompt-dir "<prompts_dir>" \
  --raw-out "<raw_path>" --meta-out "<meta_path>" \
  --timeout <timeout_sec> --temperature <temperature>
```

Each call is self-contained and always exits 0 after writing its `.meta.json` — a failing
reviewer (timeout / proxy_error / parse_error) never aborts its siblings (AC-1.7).

### Wave D+E — Normalize + return contract (single Bash call)

```bash
"$SKILL_DIR/scripts/t2_normalize.py" --manifest "<output-dir>/manifest.json"
# invoke via: uv run python "$SKILL_DIR/scripts/t2_normalize.py" --manifest ... (or python3)
```

This parses each `.raw` into the §4 template, writes final `bare-review-NN-<model>.md`
files atomically with deterministic names (IMM-6), determines status (IMM-5, success-first),
emits `<output>/return-contract.yaml`, and prints the contract to stdout. Relay that
contract as the skill's result.

## Return Contract (§3.3 Wave E)

```yaml
contract_version: "1.0"
status: success | partial | failed
target: <absolute path>
target_checksum: <sha256-12>
target_truncated: <bool>
reviewers_requested: <N>
reviewers_succeeded: <M>
output_files:
  - path: <absolute path>
    model_id: <e.g., deepseek-v4-pro>
    model_label: <e.g., DeepSeek V4 Pro>
    bytes: <size>
    status: success | timeout | parse_error | proxy_error
    elapsed_ms: <int>
suspect: true                          # always — these are suspect by construction
recommended_next_command: "/sc:adversarial --compare <existing-review>,<bare1>,... --suspect-source <bare1>,..."
```

**Status (IMM-5, success-first):** `M == N` → `success`; `2 ≤ M < N` → `partial`;
`M < 2` → `failed`. The `M == N == 2` case is `success` (the `M==N` rule is evaluated
first), because a user who asked for 2 and got 2 received what they requested.

The contract is written on **every** invocation including failure (write-on-failure).

## Failure Modes (§8 — skill rows)

| Scenario | Behavior |
|----------|----------|
| `T2ProxyUrl`/`T2ProxyKey` unset | STOP at preflight naming the missing var |
| `--reviewers` out of `[2,4]` or > configured models | STOP at preflight |
| Target missing/unreadable | STOP at preflight with the path |
| Target < 50 non-whitespace bytes (IMM-4) | STOP, write `failed`/`target-too-small` contract, **no dispatch** |
| `curl`/`jq` unavailable | STOP at preflight |
| Proxy HTTP 5xx | dispatch retries once after 2s; then `proxy_error`, continue |
| Proxy HTTP 4xx | no retry; `proxy_error`, continue |
| Per-reviewer timeout | `timeout`, continue with others |
| Response parse fails | `parse_error`; `.raw` retained; normalizer attempts §7.4 salvage |
| `M < 2` reviewers succeed | `status=failed`; caller should NOT proceed to adversarial |
| `2 ≤ M < N` | `status=partial`; contract lists only successful files |
| Adversarial fails later (IMM-6) | bare-review artifacts preserved (idempotent filenames); `recommended_next_command` enables manual retry; caller surfaces the failure (no auto-retry) |

## Boundaries (§3.4)

**Will:** read target; dispatch N parallel proxy calls; apply per-reviewer hard timeout;
continue on partial success (≥2); always set `suspect: true`; emit `recommended_next_command`;
write only inside `--output`.

**Will NOT:** make claims about review quality; filter or score reviews; retry beyond a
single 5xx retry; route to Anthropic models; write outside `--output`.

## MCP Integration

None in Phase 1 — the reference transport is Bash + curl + jq against an OpenAI-compatible
proxy (spec §7.3). An optional `mcp__t2-proxy__chat` MCP transport adapter is Phase 5
(AC-5.1/5.2): the skill would auto-detect MCP availability and fall back to Bash+curl when
absent. Not implemented here.

## Model Recommendation

- **Default: sonnet.** The skill is deterministic orchestration over scripts; the
  reviewing intelligence lives in the external T2 models, not in this skill.

## Acceptance Criteria (§9.1)

- **AC-1.1** — Skill at `src/superclaude/skills/sc-bare-review/SKILL.md`; `make sync-dev`
  copies to `.claude/skills/sc-bare-review/`.
- **AC-1.2** — Reads env per §7.1; STOPs cleanly when required vars missing.
- **AC-1.3** — Defaults `deepseek-v4-pro` / `qwen3.6-plus` / `kimi-k2.6` / `glm-5.1`.
- **AC-1.4** — `--reviewers ∈ [2,4]`; out-of-range → STOP.
- **AC-1.5** — All N reviewers dispatched in a single message (structural assertion in
  Wave C); proxy-side serialization out of scope.
- **AC-1.6** — Per-reviewer timeout enforced (default 180s; `--timeout-sec` / `T2Timeout`).
- **AC-1.7** — Per-reviewer failure does not abort other reviewers.
- **AC-1.8** — Output files conform to §4.1; `schema_version` present.
- **AC-1.9** — Output frontmatter always carries `suspect: true`.
- **AC-1.10** — `target_checksum` is SHA-256 first 12 hex chars.
- **AC-1.11** — Return contract includes `recommended_next_command` with literal
  `--suspect-source` flag and paths.
- **AC-1.12** — `failed` when `M < 2`; `partial` when `2 ≤ M < N`; `success` when `M == N`.

---

*v1.0 — Phase 1 of the T2 Bare-Reviewer Adjunct (spec v1.3.0-draft). Bash+curl reference
transport; suspect-by-construction. Source of truth: `src/superclaude/`; run `make sync-dev`
after edits — never edit the `.claude/` mirror directly.*
