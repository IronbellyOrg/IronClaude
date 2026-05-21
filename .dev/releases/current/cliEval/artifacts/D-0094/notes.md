# D-0094 — Notes / Design Rationale

## Why a Task-tool invocation (not a /agents prompt or other surface)

The SubagentStart hook fires when Claude Code spawns a sub-agent
process. The canonical user-facing path to spawn a sub-agent is the
**Task tool** (the Agent tool's CLI alias), which accepts a
`subagent_type` parameter naming the agent persona (e.g., `Explore`,
`Plan`, `general-purpose`). Invoking the Task tool is the most
reliable, deterministic way to trigger the SubagentStart event from a
single user prompt without depending on session-context flags or
in-band slash commands.

Alternative surfaces considered and rejected:

- **`/agents <name>` slash command** — exists in some IronClaude
  builds but not in the v1 baseline; would require feature-flag
  gating in the eval body and degrade portability across host
  Claude Code revisions.
- **Implicit sub-agent invocation** (e.g., "delegate this to an
  Explore agent") — depends on the parent agent's persona-routing
  heuristics; not deterministic across runs (the parent might do the
  work inline instead of spawning a sub-agent on hosts with
  different system-prompt sizes).
- **Multi-step orchestration** (`/sc:spawn` / similar) — introduces
  superclaude-specific routing logic into a hook-coverage eval;
  out of scope for the OQ-2 frozen body shape.

The explicit Task-tool invocation with `subagent_type='Explore'`
follows the precedent of E1 / E2.1-3 / E8 / E9 — those evals all
name the tool to be invoked explicitly via the prompt + the
`expect_tool_call` field on the input row.

## Why `subagent_type='Explore'` (not 'Plan' or 'general-purpose')

OQ-2 D-0082 §4 row E10 names `Explore` or `Plan` as the example
sub-agent type. T05.15 picks `Explore` for three reasons:

1. **Read-only by design** — the Explore agent is restricted to
   Glob, Grep, Read; it cannot Edit / Write / call MCP tools. This
   keeps the eval body free of unintended PreToolUse co-fires from
   the sub-agent's own tool calls (Plan can call any tool, which
   could fire Edit / Write / serena matchers under the sub-agent's
   process tree and pollute the parent session's freshness ledger
   accounting).
2. **Lightweight** — Explore's typical work (glob + a few reads) is
   bounded in time and resource footprint; the 60-second timeout
   leaves comfortable headroom on slow hosts.
3. **Deterministic on a clean HOME** — the chosen task ("find files
   matching `*.md`") returns zero results on a freshly-isolated
   per-eval HOME (FR-ISO2). The numeric count of zero is reported
   back to the parent session, but E10 does not assert on the count
   — only on the SubagentStart hook firing.

`Plan` was considered but rejected because Plan can spawn its own
tool calls; this would create additional hook-event noise in the
freshness ledger that the assertion would need to filter past, and
could mask regressions where the SubagentStart hook fails to fire
(the ledger might still contain other events from the Plan's tool
calls, falsely suggesting the hook fired).

## Why `requires: []` (not `[mcp_server.*]`)

The Task / Agent tool is a **built-in Claude Code tool**, not an MCP
tool. It is always available regardless of MCP server connectivity.
Per D-0082 §6 capability-tag rollup, E10's row lists no capability
tag. This matches siblings E3-E7 / E9 (no MCP) and differs from E1,
E2.1-3, and E8 (which require specific MCP servers).

The practical implication: E10 runs under `--no-mcp` (the
matcher-coverage gate counts it as a non-MCP eval), and the only
way E10 skips is via `--no-pty` (per-eval `no_pty: skip` tag).

## Why a single-substring assertion (not the two-substring pattern)

E6 / E7 / E8 use a two-substring assertion (`"type":"pre_edit"` +
`"matcher":"<branch>"`) because they cover three branches of the
same matcher group (`Edit|Write|mcp__serena__*`) and need to
discriminate which branch fired. The SubagentStart hook in
hooks.json has **no matcher field** — every sub-agent spawn fires
the same single hook. The `subagent_start` type label alone is
sufficient to prove the hook fired; no additional matcher pin is
needed (and there are no sibling SubagentStart branches to
discriminate against).

This mirrors E3 (SessionStart-unmatched) and E5
(UserPromptSubmit-unmatched), which also use single-substring
assertions for the same reason.

## Async-branch nuance — why `/quit` is necessary (inherited from E9)

The OQ-2 D-0082 §4 row E10 inputs say "invoke a sub-agent" without
prescribing a wait mechanism for the async hook flush. T05.15
implements the wait via the `/quit` clean-exit prompt — identical
posture to T05.14 (E9):

- The PTY harness blocks on EOF after `/quit`;
- PTY teardown reaps any pending async writer processes — either
  by letting them complete naturally (the expected case for a
  fast flock+increment) or by SIGHUP'ing them mid-flight (cleanup
  path on a slow host);
- By the time the harness reads `logs/freshness.jsonl` for the
  Expect.file assertions, the async writer has either:
  - completed → row present → assertion passes (expected);
  - been killed mid-flight → row absent → assertion fails
    (regression surface).

The `/quit` pattern also satisfies the `exit_code.equals(0)`
assertion — without `/quit`, the PTY would timeout-kill the session
and yield a non-zero exit code. This is the sibling pattern of E3-E9
(all use `/quit` as the final input for the same reason).

A `sleep` prompt was considered as an alternative wait mechanism but
rejected for the same reasons documented in D-0093 §"Async-branch
nuance — why `/quit` is necessary": Claude Code does not expose a
deterministic sleep tool to the agent; the teardown-based wait is
already deterministic and matches the pattern used by every other
hook-lifecycle eval. Adding a sleep would create a divergent pattern
and weaken sibling-trio symmetry.

## Why the Explore sub-agent's own tool calls don't pollute the assertion

The Explore sub-agent runs under its own process tree, but the hooks
configured under `~/.claude/settings.json` (which point to
`~/.claude/hooks/*.sh` deployed by `install_hooks`) apply to all tool
calls under the same Claude Code session — parent and sub-agent
alike. So Explore's Glob / Read calls will fire:

- PreToolUse hooks (none — Glob and Read aren't in the
  `Edit|Write|mcp__serena__*` matcher group);
- PostToolUse hooks (Read fires the PostToolUse Read async hook
  covered by E9, emitting `"type":"post_read"` rows).

The post_read co-fires from Explore's Read calls coexist in
`logs/freshness.jsonl` with the SubagentStart row from E10's surface.
The E10 assertion uses `Expect.file.contains` which only requires
the `subagent_start` substring to appear somewhere in the file — the
post_read rows are harmless.

If a future change introduces a "filter ledger rows by hook event"
predicate (D-4 callback escape hatch), E10's assertion could be
narrowed to "exactly one subagent_start row, regardless of co-fires"
— but the current binary substring presence is sufficient for the
OQ-2 minimum AC.

## Telemetry gap inheritance

The `freshness-subagent-start.sh` script telemetry gap (writes to
`state/bg-agents/<sid>.txt` as a bare integer counter, not
`logs/freshness.jsonl`; no `type` field on its current output)
applies only to E10 — no sibling eval shares this script. The OQ-2
frozen body lands verbatim per the established T05.07..T05.14
posture: the script update is a single-script change that unblocks
E10 specifically.

Unlike E6/E7/E8 (which share `freshness-pre-edit.sh`), there is no
batching opportunity here for E10 — E10's hook-script update is
independent. E11 (T05.16) will have an analogous independent update
for `freshness-subagent-stop.sh`. The same template (path migration
to `logs/freshness.jsonl` + field-name normalization to `type`)
applies to both scripts, so the follow-up tasks can reuse the
patterns established for the other freshness hook scripts.

## Sibling-trio comparison (cross-event surface)

The eight post-OQ-2 hook-lifecycle evals share a common structural
template (single-prompt or seeded fire + `/quit` exit; freshness
ledger + type substring + exit code assertions):

| Field | E3 (sess-init) | E4 (sess-start) | E5 (user-prompt) | E6 (Edit) | E7 (Write) | E8 (serena) | E9 (Read) | E10 (SubagentStart) |
|---|---|---|---|---|---|---|---|---|
| Hook script | `session-init.sh` | `freshness-session-start.sh` | `freshness-user-prompt.sh` | `freshness-pre-edit.sh` | `freshness-pre-edit.sh` | `freshness-pre-edit.sh` | `freshness-post-read.sh` | `freshness-subagent-start.sh` |
| Hook event | SessionStart | SessionStart | UserPromptSubmit | PreToolUse | PreToolUse | PreToolUse | PostToolUse | SubagentStart |
| Hook async? | no | no | no | no | no | no | **yes** | **yes** |
| Matcher? | none | `*` | none | `Edit\|Write\|serena` | `Edit\|Write\|serena` | `Edit\|Write\|serena` | `Read` | none |
| `requires` | `[]` | `[]` | `[]` | `[]` | `[]` | `[mcp_server.serena]` | `[]` | `[]` |
| Type substring | `"type":"session_init"` | `"type":"session_start"` | `"type":"user_prompt"` | `"type":"pre_edit"` | `"type":"pre_edit"` | `"type":"pre_edit"` | `"type":"post_read"` | `"type":"subagent_start"` |
| Matcher pin | — | — | — | `"matcher":"Edit"` | `"matcher":"Write"` | `"matcher":"mcp__serena__replace_content"` | — | — |
| Scratch file | — | — | — | `edited.txt` | `written.txt` | `modified.txt` | `fixture.txt` | — |
| Inputs | `/quit` | `/quit` | `echo test` → `/quit` | Write → Edit → `/quit` | Write → `/quit` | Write → serena → `/quit` | Write → Read → `/quit` | Task(Explore) → `/quit` |

E10 fits the template with three distinguishing characteristics:

1. **Second async hook eval** — inherits the E9 PTY-teardown reap
   posture; relies on the binary substring presence as the
   operational guarantee.
2. **No matcher pin** — like E3 and E5 (also no-matcher hooks),
   uses a single-substring assertion (only the type label
   discriminates the SubagentStart branch).
3. **No scratch file** — unlike E6/E7/E8/E9, E10 does not need a
   seeded file; the Task tool invocation is self-contained.

The matrix is intentional — it gives a future reviewer a clean
comparison across all eight hook-lifecycle evals to spot regressions
in matcher routing or capability gating, and pins the structural
template that E11 (SubagentStop) will follow next.

## E10 ↔ E11 pair design

E10 and E11 are designed as a **lifecycle pair** on the sub-agent
spawn/return cycle. The shared input shape (a Task tool invocation)
fires both SubagentStart (E10's surface) and SubagentStop (E11's
surface) on the same prompt. The two evals could in principle have
been folded into one entry with two type-substring assertions, but
the OQ-2 resolution (D-0082 §4) keeps them separate for two reasons:

1. **Roadmap-row separation** — E10 maps to R-093, E11 to R-094;
   merging them would conflate two roadmap items.
2. **Failure-mode separation** — keeping the two assertions in
   separate evals lets the test report tell the reviewer
   independently whether SubagentStart fired but SubagentStop
   didn't (the dangling-sub-agent case), or vice versa
   (the orphaned-stop case). A merged eval would mask which side
   of the pair regressed.

E11 (T05.16) will additionally assert `event_count(subagent_start)
== event_count(subagent_stop)` symmetry — a Python-callable
predicate that follows the same deferral pattern established here
in §3 footnote.
