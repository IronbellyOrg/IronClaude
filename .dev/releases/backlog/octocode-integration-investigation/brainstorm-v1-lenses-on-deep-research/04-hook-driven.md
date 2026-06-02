# Brainstorm 04: Hook-Driven Auto-Activation

**Lens:** Use Claude Code's PreToolUse / PostToolUse / UserPromptSubmit hooks to
auto-fire octocode in parallel with existing research tools, so the LLM doesn't
have to remember to invoke it. The framework decides.

**Target:** `src/superclaude/agents/deep-research.md` (and the `deep-research-agent`
variant) — integration target #1 from the fit analysis (score 45).

---

## Lens — Defending Hook-Driven Activation Against the Rejection

The fit-analysis explicitly downgrades hook-level integration in its "low-value
targets" table:

> Hook-level integration (PostToolUse) — Adds latency on every tool use; high
> noise-to-signal

That rejection is **correct as stated, but incomplete**. It treats hooks as a
blunt instrument fired on every tool call. The actual hooks.json mechanism
supports `matcher` regexes that constrain firing to specific tool surfaces, and
the existing hooks (`freshness-pre-edit.sh`, `auggie-flag-clear.sh`) already
prove the project uses tight matchers — `Edit|Write|mcp__serena__replace_*`,
`mcp__auggie__.*` — not wildcard `*`.

The honest counter-claim for this lens:

1. **Hook firing is gated by matcher regex.** `mcp__auggie__codebase-retrieval`
   fires on auggie calls only — not on every Read. The "every tool use" framing
   collapses if the matcher is precise.
2. **Hooks are async-capable.** The current `freshness-post-read.sh` and
   `freshness-subagent-*` entries already run `async: true`. An octocode hook
   that returns a deferred enrichment artifact does not block the agent's
   next turn.
3. **The `deep-research` agent's bottleneck is "remembering to use the new
   tool."** Adding octocode to the frontmatter `tools:` list (the declarative
   approach) puts it on the menu but does not guarantee invocation. A hook
   guarantees invocation when the trigger conditions hold, with zero cognitive
   load on the agent's planning logic.
4. **Hooks compose with declarative approaches.** Hook-driven activation is not
   exclusive of the Tool Selection Policy edit (target #1 declarative); the
   hook fires the enrichment, and the policy text tells the agent how to read
   the deferred output. They are complementary, not competing.

**Where the rejection still bites:** if a hook fires unconditionally on every
auggie call (including for tasks where cross-repo context is irrelevant — e.g.,
local-only refactors), we burn GitHub API budget for noise. The brainstorm's
core engineering work is in the **selective activation** section below. If we
can't keep the hook silent on local-only work, we should not ship it.

---

## Hook Inventory

Four hooks, each tightly matched:

| # | Hook | Matcher | Purpose | Async? |
|---|---|---|---|---|
| **H1** | `PostToolUse` on auggie | `mcp__auggie__codebase-retrieval\|mcp__auggie-mcp__ask_question\|mcp__airis-mcp-gateway__auggie_.*` | Fire octocode `githubSearchCode` in parallel with auggie's local result, scoped to "how do other repos solve this same pattern" | Yes |
| **H2** | `PostToolUse` on Tavily | `mcp__tavily__tavily-search` | If query string contains a known package name (npm/PyPI heuristic), fire `packageSearch` to resolve package → repo URL → top-level structure | Yes |
| **H3** | `UserPromptSubmit` | (no matcher — runs on every prompt, but body is a tiny script that early-exits unless the prompt contains a GitHub URL) | Pre-fetch repo structure via `githubViewRepoStructure` so the first turn has it in context | Yes |
| **H4** | `SubagentStart` on `deep-research` | (filter by `agent_name=deep-research\|deep-research-agent` inside the hook script) | Seed the subagent with an octocode-availability flag file + the activation policy snippet | Yes |

All four hooks are **deep-research-scoped**, not project-wide — H1 and H2 only
write enrichment artifacts when the calling agent (read from session-context)
is `deep-research` or a downstream consumer (`tech-research`, `troubleshoot`,
`brainstorm`). This is implemented inside the hook script, not the matcher,
because the matcher language doesn't read agent identity.

---

## Activation Logic Per Hook

### H1 — Auggie companion search

**Trigger:** Any auggie tool call completes.

**Filter inside script** (all must hold):

1. Caller agent is in `{deep-research, deep-research-agent, tech-research,
   sc-troubleshoot, sc-brainstorm}` — read from
   `$CLAUDE_PROJECT_DIR/.dev/session-context.json` (already maintained by
   `freshness-session-start.sh`).
2. The auggie `information_request` payload contains at least one of:
   - A package name (regex against `node_modules`-style names, `import X from
     'Y'`, `from y import Z`)
   - A "how does X work / how do they implement Y" pattern (regex on
     `^(how|why|where|when) (does|do|is|are)`)
3. No octocode enrichment artifact already exists for this turn (
   `.dev/octocode-cache/<session>-<turn>.json` not present).
4. Token-budget check: `LOG=false` is set, GitHub search budget for the past
   60s has at least 5 remaining slots (tracked in
   `.dev/octocode-cache/rate-limit.json`).

**Payload sent to octocode:**

```json
{
  "tool": "githubSearchCode",
  "researchGoal": "Find cross-repo callsites of the pattern auggie searched locally",
  "reasoning": "Auggie returned local matches for '${question}'; fetch 3-5 external implementations to enrich the deep-research synthesis",
  "query": "${distilled_question}",
  "limit": 5,
  "verbosity": "compact"
}
```

**Result handling:** Write to
`.dev/octocode-cache/<session>-<turn>-enrichment.md` and append a one-line
notice to the next user-visible turn:
`[octocode-enrichment: 5 external callsites available at <path>]`.

The agent reads the enrichment when its Tool Selection Policy says to —
not because the hook injects it inline. **Zero context pollution.**

### H2 — Tavily package resolution

**Trigger:** Tavily search completes.

**Filter inside script:**

1. Caller is a deep-research consumer (same allowlist as H1).
2. Tavily `query` parameter matches `\b(npm|pypi|cargo|gem|composer)\b` OR
   contains a token shaped like `[a-z][a-z0-9-]+/[a-z][a-z0-9-]+` (org/repo) OR
   contains a known-package heuristic (`@scope/name`, `pip install`, etc.).
3. No `packageSearch` already run for this query hash this turn.

**Payload:**

```json
{
  "tool": "packageSearch",
  "researchGoal": "Resolve package mentioned in Tavily query to authoritative repo",
  "reasoning": "User's research query named '${pkg}'; package-search anchors subsequent reads to the canonical source",
  "name": "${pkg}",
  "ecosystem": "${detected}"
}
```

**Result handling:** Write resolved `{ name, version, repoUrl, deprecation }`
to `.dev/octocode-cache/<session>-<turn>-packages.json`. Useful for the agent's
next turn ("ok, the repo is github.com/X/Y; now fetch structure").

### H3 — GitHub URL pre-fetch

**Trigger:** User submits any prompt.

**Filter inside script:**

1. Prompt body contains a GitHub URL regex
   (`https?://github\.com/[\w.-]+/[\w.-]+`).
2. URL is not already cached for this session.
3. Repo is public OR `GITHUB_TOKEN` is set and the repo is accessible.

**Payload:**

```json
{
  "tool": "githubViewRepoStructure",
  "researchGoal": "Pre-fetch repo structure for URL referenced by user",
  "reasoning": "User-provided URL implies upcoming questions about this repo; cache structure to avoid first-turn round trip",
  "owner": "${owner}",
  "repo": "${repo}",
  "branch": "main",
  "depth": 2
}
```

**Result handling:** Cache to
`.dev/octocode-cache/repo-<owner>-<repo>.json`. Inject a SessionStart-style
breadcrumb into `.dev/session-context.json`:
`octocode_prefetched: [{ owner, repo, path }]`. The agent picks it up via
session-context on its first turn.

### H4 — Deep-research subagent seed

**Trigger:** `deep-research` (or `deep-research-agent`) subagent starts.

**Filter:** matcher restricts to those two agent names.

**Action:** Write a tiny `octocode-availability.json` into the subagent's
working scratch directory, declaring:

- Whitelisted octocode tools (`githubSearchCode`, `githubSearchPullRequests`,
  `packageSearch`, `githubGetFileContent`, `githubViewRepoStructure`)
- Rate-limit budget remaining
- Path to any prefetched repo structures from H3
- Path to any companion enrichments from H1/H2 from earlier in the session

**No external API call** — H4 is a pure local seed. Zero latency tax, zero
risk. Its job is to make the *other three* hooks' outputs discoverable to the
subagent on first turn.

---

## Latency Budget

Be honest: hooks add latency. Here's the breakdown for each hook in the
**worst legitimate case** (filter passes and octocode is invoked):

| Hook | Sync wait imposed on agent | External work (async) | Total perceived |
|---|---|---|---|
| H1 (auggie companion) | 0 ms (async dispatch) | 800–3000 ms octocode + GH API | 0 ms perceived |
| H2 (package resolve) | 0 ms (async dispatch) | 400–1200 ms `packageSearch` | 0 ms perceived |
| H3 (URL prefetch) | ≤ 200 ms script eval + dispatch | 600–1500 ms `githubViewRepoStructure` | ≤ 200 ms perceived |
| H4 (subagent seed) | ≤ 50 ms file writes | 0 ms (local only) | ≤ 50 ms perceived |

The two hooks that touch external services (H1, H2) are **async fire-and-forget**.
They write results to the cache directory and exit; the agent reads cache on
its next turn (or doesn't, if the enrichment didn't beat the next turn's
deadline). The agent never blocks.

H3 has a tiny sync footprint because the URL regex match needs to happen
inline (we need to know whether to dispatch before the prompt is forwarded to
the agent). Estimated 50-200 ms in shell — well under the existing
`freshness-user-prompt.sh` 3000 ms timeout.

**Is the latency justified?**

For H1+H2: yes, because perceived latency is zero (async). The cost is
**rate-limit budget**, not wall-clock — and that cost is bounded by the
filtering rules in §"Selective Activation."

For H3: yes, 200 ms is below user-perception threshold and only fires when a
GitHub URL was actually pasted (the explicit signal of intent).

For H4: yes, 50 ms is negligible and the hook fires only when a deep-research
subagent starts (rare event).

**Honest concession:** if the filtering logic in §"Selective Activation"
degrades (e.g., a future package-name heuristic over-matches), H1+H2 burn
GitHub Search API budget (30 req/min ceiling). This is the single most
important risk and the §"Specific Risk Mitigations" section addresses it
directly.

---

## Selective Activation (the key challenge)

This is the section that determines whether this approach is worth shipping.
The fit-analysis rejection ("noise-to-signal") is correct **unless** the
filtering achieves at least ~80% precision (fire when relevant, stay silent
when not).

### Layered filtering (defense in depth)

1. **Matcher-level (Claude Code hooks.json):** Tightest possible regex on
   `tool_name`. `mcp__auggie__.*` not `*`. `mcp__tavily__tavily-search` not
   `mcp__tavily__.*`.

2. **Agent-identity filter (script-level):** Hook script reads
   `.dev/session-context.json` (already maintained) for `current_agent`. If
   not in `{deep-research, deep-research-agent, tech-research,
   sc-troubleshoot, sc-brainstorm}` → early-exit with `OCTOCODE_SKIP=not-research-agent`.

3. **Query-content filter (regex on payload):** For H1, require the auggie
   query to look like an external-pattern question:
   - Whitelist: `\b(how|why|where) (does|do|is|are)\b`,
     `\b(implement|implementation|pattern|approach|example|callsite|usage)\b`,
     a known package-import shape, an `org/repo` shape.
   - Blacklist: `\b(this|our|here|the local|this repo|our codebase)\b` —
     strong signal the user wants local-only context.

4. **Per-session throttle:** Maximum 8 H1 fires per session, 4 H2 fires per
   session, 6 H3 fires per session. State stored in
   `.dev/octocode-cache/throttle.json`. Throttle resets on `SessionStart`.

5. **Per-turn dedupe:** Each turn gets max one H1 enrichment artifact, one H2
   package resolution, one H3 prefetch per unique URL. Hash the payload, skip
   if hash already seen this turn.

6. **Rate-limit budget tracker:** Hook script reads
   `.dev/octocode-cache/rate-limit.json` — if `gh_search_remaining < 5` for
   the trailing 60 s window, hook short-circuits. The tracker is updated on
   every octocode call's response headers.

7. **Kill-switch env:** `IRONCLAUDE_OCTOCODE_HOOKS=0` disables all four hooks
   instantly. Default to **off** until pilot validates precision; enabled
   per-session by the user.

### Precision target & validation

Pilot acceptance criterion: **on 20 representative deep-research turns, hooks
must fire ≥ 80% of the time when relevant, and ≤ 10% of the time when
irrelevant.** Anything worse than 70%/20% = revert. Measurement via a
classifier-by-hand on the pilot's enrichment-cache contents vs. agent's actual
research need (as scored by output utility).

---

## Concrete hooks.json additions

These append to the existing `src/superclaude/hooks/hooks.json`. No existing
entries are modified. The four new hook scripts live in
`src/superclaude/hooks/scripts/` and are synced to `.claude/hooks/` via
`make sync-dev`.

```jsonc
{
  "hooks": {
    "SessionStart": [
      /* ...existing entries unchanged... */
    ],
    "UserPromptSubmit": [
      /* ...existing freshness-user-prompt entry unchanged... */
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/octocode-prefetch-url.sh",
            "timeout": 2,
            "async": true
          }
        ]
      }
    ],
    "PreToolUse": [
      /* ...existing freshness-pre-edit entry unchanged... */
    ],
    "PostToolUse": [
      /* ...existing Read + auggie entries unchanged... */
      {
        "matcher": "mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/octocode-auggie-companion.sh",
            "timeout": 2,
            "async": true
          }
        ]
      },
      {
        "matcher": "mcp__tavily__tavily-search",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/octocode-tavily-package.sh",
            "timeout": 2,
            "async": true
          }
        ]
      }
    ],
    "SubagentStart": [
      /* ...existing freshness-subagent-start entry unchanged... */
      {
        "matcher": "deep-research|deep-research-agent",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/octocode-subagent-seed.sh",
            "timeout": 1,
            "async": true
          }
        ]
      }
    ],
    "SubagentStop": [
      /* ...existing entries unchanged... */
    ]
  }
}
```

Note: The existing `PostToolUse` matcher on auggie
(`mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*`)
already exists for `auggie-flag-clear.sh`. We **add a second hook block** with
the same matcher pointing to `octocode-auggie-companion.sh`. Multiple hook
blocks with overlapping matchers are supported and run independently.

### Companion script skeleton (`octocode-auggie-companion.sh`)

```bash
#!/usr/bin/env bash
set -euo pipefail

# 1) Kill switch
[ "${IRONCLAUDE_OCTOCODE_HOOKS:-1}" = "0" ] && exit 0

# 2) Agent-identity gate
CTX="$CLAUDE_PROJECT_DIR/.dev/session-context.json"
[ -f "$CTX" ] || exit 0
agent="$(jq -r '.current_agent // empty' "$CTX")"
case "$agent" in
  deep-research|deep-research-agent|tech-research|sc-troubleshoot|sc-brainstorm) ;;
  *) exit 0 ;;
esac

# 3) Per-session throttle
TROTTLE="$CLAUDE_PROJECT_DIR/.dev/octocode-cache/throttle.json"
mkdir -p "$(dirname "$TROTTLE")"
[ -f "$TROTTLE" ] || echo '{"h1":0,"h2":0,"h3":0}' > "$TROTTLE"
h1_count="$(jq -r '.h1' "$TROTTLE")"
[ "$h1_count" -ge 8 ] && exit 0

# 4) Query-content gate (extract auggie's information_request from hook payload)
payload="$(cat)"  # hook stdin = tool call payload
question="$(jq -r '.tool_input.information_request // empty' <<< "$payload")"
[ -z "$question" ] && exit 0

# Blacklist: local-only signals
if grep -qiE '\b(this|our|here|the local|this repo|our codebase)\b' <<< "$question"; then
  exit 0
fi

# Whitelist: external-pattern signals
if ! grep -qiE '\b(how|why|where)\s+(does|do|is|are)\b|\b(implement|pattern|approach|example|callsite|usage)\b|[a-z][a-z0-9-]+/[a-z][a-z0-9-]+' <<< "$question"; then
  exit 0
fi

# 5) Rate-limit gate
RL="$CLAUDE_PROJECT_DIR/.dev/octocode-cache/rate-limit.json"
if [ -f "$RL" ]; then
  remaining="$(jq -r '.search_remaining // 30' "$RL")"
  [ "$remaining" -lt 5 ] && exit 0
fi

# 6) Dispatch — write a job file; a background worker (already running, started by
#    SessionStart) consumes and invokes octocode via MCP client. The hook itself
#    does NOT shell out to npx octocode-mcp — that would block. The worker does.
JOB="$CLAUDE_PROJECT_DIR/.dev/octocode-cache/jobs/$(date +%s%N).json"
mkdir -p "$(dirname "$JOB")"
jq -n \
  --arg q "$question" \
  --arg agent "$agent" \
  '{tool: "githubSearchCode",
    researchGoal: "Find cross-repo callsites parallel to local auggie result",
    reasoning: ("Auggie returned local matches for: " + $q + "; fetch 3-5 external implementations"),
    query: $q, limit: 5, verbosity: "compact",
    caller_agent: $agent}' > "$JOB"

# 7) Increment throttle
jq '.h1 += 1' "$TROTTLE" > "$TROTTLE.tmp" && mv "$TROTTLE.tmp" "$TROTTLE"
```

The worker pattern (out-of-band MCP client process) is what makes this design
non-blocking; the hook never invokes `npx octocode-mcp` directly. The worker
binary is part of the package, started by `session-init.sh` (existing
SessionStart hook), shut down on `SubagentStop`/SessionEnd.

---

## Pros

1. **Zero cognitive load on the agent.** Declarative tool-list integration
   (target #1 in fit analysis) puts octocode on the menu but the agent must
   remember to use it. Hooks guarantee invocation when triggers fire.

2. **Composable with the declarative approach.** This proposal does not replace
   the Tool Selection Policy edit — it complements it. The policy text tells
   the agent how to *read* the enrichment artifacts; the hooks *produce* them.

3. **Zero perceived latency** for the three async hooks. The synchronous H3
   stays under 200 ms.

4. **Tight matchers.** The fit-analysis rejection ("every tool use") does not
   apply because the matchers are scoped to auggie + tavily + GitHub URLs +
   deep-research subagent start.

5. **Pure additive change to hooks.json.** Existing hooks unchanged.
   `make sync-dev` already handles the deployment.

6. **Multi-skill propagation for free.** Because the hooks gate on `current_agent
   ∈ {deep-research, tech-research, sc-troubleshoot, sc-brainstorm}`, the same
   hooks serve all four downstream skills with one implementation.

7. **Telemetry-friendly.** Every job file in `.dev/octocode-cache/jobs/`
   provides a precise audit trail of when hooks fired and on what input.
   Validation is trivial.

8. **Reversible.** Kill-switch env (`IRONCLAUDE_OCTOCODE_HOOKS=0`) disables
   instantly; removing the four hook blocks from hooks.json fully reverts.

---

## Cons

1. **The worker-process design adds operational complexity.** A background
   MCP-client worker is non-trivial — it needs lifecycle management, crash
   recovery, log rotation, and a job queue. This is more infrastructure than
   either the declarative or sub-agent-delegate proposals.

2. **Filter precision is critical and unproven.** The 80%/10% precision target
   in §"Selective Activation" requires real-world tuning. First two weeks of
   pilot will likely see over-firing or under-firing; the regex whitelists +
   blacklists will need iteration.

3. **State files proliferate.** `.dev/octocode-cache/{jobs,throttle.json,
   rate-limit.json,repo-*.json,session-*-enrichment.md}` — non-trivial to
   garbage-collect. Need a `SessionStop` cleanup hook.

4. **Agent must learn to read enrichment artifacts.** Even if the hook fires
   perfectly, the agent's Tool Selection Policy needs explicit "check
   `.dev/octocode-cache/<turn>-enrichment.md` after auggie call" instructions.
   That is itself a non-trivial prompt edit and competes with the declarative
   proposal.

5. **Hook-loop risk.** If a hook fires an octocode tool, and a future hook is
   added that matches `mcp__octocode__.*`, we could recurse. Need explicit
   guard.

6. **The fit-analysis rejection is partly true.** Even with tight matchers,
   adding 4 new hooks increases the SessionStart + PostToolUse evaluation
   surface. Each hook script's startup cost (~10-30 ms shell) is amortized but
   non-zero.

7. **Per-session throttle ceilings are arbitrary.** 8/4/6 is a guess. Real
   workloads will demand tuning.

---

## What This Approach Cannot Do

1. **Cannot replace declarative integration.** The agent still needs to know
   octocode exists in its tool list to read enrichment artifacts intelligently.
   Hooks produce side-effects; they don't teach the agent to think with them.

2. **Cannot fire on patterns the matcher doesn't see.** If the agent invokes
   octocode tools without auggie or tavily first (e.g., goes straight to
   `githubSearchCode` because it remembered to), the hooks add nothing.

3. **Cannot handle the first interactive turn well.** H3 helps if the user
   pastes a URL, but for an open-ended "research how X works" prompt the
   hooks only fire after the agent's first tool call.

4. **Cannot work for offline / air-gapped environments.** Octocode needs
   GitHub API access. The hook scripts gate on network reachability or fail
   silently.

5. **Cannot substitute for a Tool Selection Policy edit** (deep-research.md
   lines 30-36 from fit analysis). Pair this hook design with that policy
   edit; do not ship one without the other.

6. **Cannot prevent the agent from ignoring enrichment artifacts.** If the
   agent's planning loop doesn't check `.dev/octocode-cache/`, the hooks
   waste GitHub API budget. Explicit policy text in the agent prompt is the
   only mitigation.

---

## Specific Risk Mitigations

### Risk: rate-limit cascade (GitHub Search API: 30 req/min)

**Mitigation A — rate-limit tracker file.** Worker writes
`.dev/octocode-cache/rate-limit.json` with `search_remaining` after every
GitHub call (extracted from response headers `X-RateLimit-Remaining-Search`).
All hooks consult this file before dispatching. If `< 5`, hooks short-circuit.

**Mitigation B — per-session caps.** Hard ceilings: 8 H1, 4 H2, 6 H3 per
session. Reset on `SessionStart`.

**Mitigation C — exponential backoff in worker.** When the worker sees a 403
from GitHub, it sets `search_remaining = 0` and `cooldown_until = now + 60s`.
All hooks short-circuit until cooldown expires.

**Mitigation D — burst detection.** If 3+ hooks fire within 5 s, the worker
batches them and emits ≤ 1 actual octocode call (the most recent), discarding
older. Prevents auggie-loops from cascading.

### Risk: hook loops

**Mitigation:** Explicit guard in every hook script:

```bash
# Refuse to fire on octocode's own tool calls
case "${CLAUDE_TOOL_NAME:-}" in
  mcp__octocode__*) exit 0 ;;
esac
```

This ensures even if a future matcher accidentally includes octocode tools,
the script self-exits.

### Risk: telemetry leak (octocode sends repo names + research goals to vendor)

**Mitigation A — environment.** All worker invocations set `LOG=false`.

**Mitigation B — content sanitization.** Worker strips known-sensitive
patterns from `researchGoal` and `query` before dispatching. Whitelist of
allowed characters; rejects strings matching `^(internal|private|confidential|
prod|production|customer|client)` (case-insensitive).

**Mitigation C — outbound-DNS allowlist (project-level).** Document a firewall
rule that blocks octocode's telemetry endpoint while allowing api.github.com.

### Risk: cache file explosion / garbage collection

**Mitigation:** `SessionStop` hook (new) runs `find .dev/octocode-cache/
-mtime +7 -delete`. Plus a per-session counter that auto-prunes once the
cache exceeds 200 files.

### Risk: filter precision drift (over-firing or under-firing)

**Mitigation A — telemetry counter.** Worker logs every job with a precision
classifier output:

```json
{
  "timestamp": "...",
  "hook": "H1",
  "fired": true,
  "useful_to_agent": null,  // backfilled by post-pilot review
  "agent_used_artifact": null  // backfilled by output analysis
}
```

**Mitigation B — weekly review.** First 4 weeks: human review of 20 random
fires per week. Tune whitelist/blacklist regex based on false-positive /
false-negative patterns.

**Mitigation C — kill-switch.** `IRONCLAUDE_OCTOCODE_HOOKS=0` instantly
disables. Default to off until pilot validates.

### Risk: supply-chain (octocode bus factor = 1)

**Mitigation:** Pin to `octocode-mcp@14.2.0` in the worker spawn command.
Never `@latest`. Document upgrade gate (security review + version diff
inspection) in the runbook.

### Risk: worker process orphaning

**Mitigation:** `session-init.sh` checks for a stale worker PID; kills and
respawns. Worker writes PID to `.dev/octocode-cache/worker.pid`. `SubagentStop`
+ session-end hooks send SIGTERM to the worker.

---

## Test Plan

### Unit tests (pytest)

1. `test_octocode_hook_agent_filter` — passes auggie call payload with various
   `current_agent` values; asserts hook exits 0 for non-research agents and
   dispatches for research agents.
2. `test_octocode_hook_query_whitelist` — feeds 20 representative questions;
   asserts ≥ 16 trigger and ≤ 2 false positives.
3. `test_octocode_hook_throttle` — fires 10 H1 events; asserts 8 dispatch and
   2 short-circuit.
4. `test_octocode_hook_rate_limit_gate` — sets `search_remaining=4`; asserts
   no dispatch.
5. `test_octocode_hook_loop_guard` — sets `CLAUDE_TOOL_NAME=mcp__octocode__
   githubSearchCode`; asserts hook exits 0.
6. `test_octocode_worker_dedupe` — submits 3 identical jobs in 1 s; asserts
   worker dispatches once.

### Integration tests (uv run pytest + recorded fixtures)

7. `test_deep_research_with_hooks` — run a deep-research agent on a recorded
   research prompt; assert hook fires once, enrichment file is created, agent
   reads it in its synthesis turn.
8. `test_hook_disabled_via_env` — set `IRONCLAUDE_OCTOCODE_HOOKS=0`; assert
   no octocode call across a 5-turn research session.

### Pilot tests (live)

9. Run 20 representative deep-research tasks with hooks enabled. Manual
   precision review: hook should fire on ≥ 16/20 relevant cases, ≤ 2/20
   irrelevant cases. Below threshold = revert.
10. Compare token usage and final-output quality vs. a control set of 20 tasks
    with hooks disabled. Acceptance: equal or better quality at ≤ 10% higher
    token cost.

### Failure-mode tests

11. Disable network; assert hooks fail silently within timeout (≤ 2 s) and
    agent proceeds.
12. Mock GitHub 403; assert worker writes cooldown state and hooks
    short-circuit for 60 s.

---

## Effort Estimate

| Component | Hours | Notes |
|---|---|---|
| Hook scripts (H1–H4) | 6 | 4 shell scripts ~150 LoC each |
| Worker process (Python MCP client) | 12 | Job queue + dedupe + rate-limit tracker + lifecycle |
| hooks.json additions | 1 | 4 entries appended |
| Tool Selection Policy edit (deep-research.md) | 2 | Document the enrichment-artifact contract |
| Unit tests (6) | 6 | |
| Integration tests (2) | 6 | Recorded fixtures + agent harness |
| Pilot review tooling | 4 | Telemetry CSV → manual review script |
| Runbook + ops docs | 3 | Kill switch, throttle tuning, GC |
| **Total** | **40 h** | ~1 sprint |

**Comparison anchor:** the pure declarative proposal (fit-analysis target #1)
is estimated at ~2 h. This hook-driven approach is **20× the effort** but
provides **guaranteed activation + multi-skill propagation + zero cognitive
load on the agent**.

**Decision recommendation:** Ship the declarative proposal first (2 h). Run
the pilot for 2 weeks. If real-world data shows the agent *forgets* to invoke
octocode in ≥ 30% of relevant turns, then escalate to this hook-driven
approach. If activation rate is ≥ 70% with the declarative-only path, skip
this proposal entirely — it would be over-engineering.

---

**End of Brainstorm 04 — Hook-Driven Auto-Activation**
