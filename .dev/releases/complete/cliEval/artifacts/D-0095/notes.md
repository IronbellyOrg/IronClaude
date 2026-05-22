# D-0095 — Notes / Design Rationale

## Why a Task-tool invocation (not a /agents prompt or other surface)

The SubagentStop hook fires when a sub-agent process returns control
to the parent Claude Code session. The canonical user-facing path to
spawn (and therefore eventually stop) a sub-agent is the **Task tool**
(the Agent tool's CLI alias), which accepts a `subagent_type`
parameter naming the agent persona (e.g., `Explore`, `Plan`,
`general-purpose`). Invoking the Task tool is the most reliable,
deterministic way to trigger the SubagentStop event from a single
user prompt without depending on session-context flags or in-band
slash commands — the SubagentStop is the natural counterpart to the
SubagentStart that Task triggers.

Alternative surfaces considered and rejected (mirroring the E10
sibling rationale in D-0094, plus E11-specific considerations):

- **`/agents <name>` slash command** — exists in some IronClaude
  builds but not in the v1 baseline; would require feature-flag
  gating in the eval body and degrade portability across host
  Claude Code revisions.
- **Implicit sub-agent invocation** — depends on the parent agent's
  persona-routing heuristics; not deterministic across runs.
- **Multi-step orchestration** — introduces superclaude-specific
  routing logic into a hook-coverage eval; out of scope.
- **Aborting a long-running sub-agent** to force SubagentStop on a
  separate path (e.g., a hung Plan that hits the timeout) — adds
  non-determinism (timeout race) and reframes the assertion from "the
  sub-agent returned cleanly and SubagentStop fired" to "the sub-agent
  was killed and SubagentStop fired in the cleanup path"; the OQ-2
  body shape (D-0082 §4 row E11) is satisfied by the normal-return
  path, so the abort surface is not exercised here.

The explicit Task-tool invocation with `subagent_type='Explore'`
follows the precedent of E10 — and of E1 / E2.1-3 / E8 / E9 more
broadly — those evals all name the tool to be invoked explicitly via
the prompt + the `expect_tool_call` field on the input row.

## Why `subagent_type='Explore'` (not 'Plan' or 'general-purpose')

OQ-2 D-0082 §4 row E11 inherits the row E10 example sub-agent type
(`Explore` or `Plan`). T05.16 picks `Explore` for the same three
reasons documented in D-0094 §"Why `subagent_type='Explore'`":

1. **Read-only by design** — Explore is restricted to Glob, Grep,
   Read; it cannot Edit / Write / call MCP tools. This keeps the
   eval body free of unintended PreToolUse co-fires from the
   sub-agent's own tool calls.
2. **Lightweight** — Explore's typical work (glob + a few reads) is
   bounded in time and resource footprint; the 60-second timeout
   leaves comfortable headroom on slow hosts AND ensures the
   sub-agent returns (firing SubagentStop) well before the parent's
   PTY timeout.
3. **Deterministic on a clean HOME** — the chosen task ("find files
   matching `*.md`") returns zero results on a freshly-isolated
   per-eval HOME (FR-ISO2). The numeric count of zero is reported
   back to the parent session, but E11 does not assert on the count
   — only on the SubagentStop hook firing.

Additionally for E11 specifically: a sub-agent that does **not**
return cleanly (e.g., one that goes into a recovery branch or
exception path) might fire SubagentStop on a different code path —
the OQ-2 D-0082 row E11 frozen body shape asserts on the
normal-return surface, so Explore's clean glob-and-report exit is the
right shape. `Plan` was again rejected because its potential to spawn
its own tool calls could create additional hook-event noise that
masks regressions where the SubagentStop hook fails to fire (the
ledger might still contain other events from Plan's tool calls,
falsely suggesting the assertion's substring is present — except in
E11's case the substring `subagent_stop` is uniquely produced by the
SubagentStop hook, so this masking concern is less acute than E10's;
the read-only/lightweight/deterministic considerations dominate the
choice).

## Why `requires: []` (not `[mcp_server.*]`)

The Task / Agent tool is a **built-in Claude Code tool**, not an MCP
tool. It is always available regardless of MCP server connectivity.
Per D-0082 §6 capability-tag rollup, E11's row lists no capability
tag. This matches sibling E10 (Task / Agent tool) and the broader
E3-E7 / E9 hook-lifecycle group (no MCP) — and differs from E1,
E2.1-3, and E8 (which require specific MCP servers).

The practical implication: E11 runs under `--no-mcp` (the
matcher-coverage gate counts it as a non-MCP eval), and the only
way E11 skips is via `--no-pty` (per-eval `no_pty: skip` tag).

## Why a single-substring assertion (not the two-substring pattern)

E6 / E7 / E8 use a two-substring assertion (`"type":"pre_edit"` +
`"matcher":"<branch>"`) because they cover three branches of the
same matcher group (`Edit|Write|mcp__serena__*`) and need to
discriminate which branch fired. The SubagentStop hook in
hooks.json has **no matcher field** — every sub-agent return fires
the same single hook. The `subagent_stop` type label alone is
sufficient to prove the hook fired; no additional matcher pin is
needed (and there are no sibling SubagentStop branches to
discriminate against).

This mirrors E3 (SessionStart-unmatched), E5 (UserPromptSubmit-
unmatched), and E10 (SubagentStart-unmatched), which all use
single-substring assertions for the same reason.

## Async-branch nuance — why `/quit` is necessary (inherited from E9 / E10)

The OQ-2 D-0082 §4 row E11 inputs say "spawn session, invoke
sub-agent as in E10, allow completion, wait for stop hook flush"
without prescribing a specific wait mechanism for the async hook
flush. T05.16 implements the wait via the `/quit` clean-exit prompt
— identical posture to T05.14 (E9) and T05.15 (E10):

- The PTY harness blocks on EOF after `/quit`;
- PTY teardown reaps any pending async writer processes — either
  by letting them complete naturally (the expected case for a
  fast flock+decrement) or by SIGHUP'ing them mid-flight (cleanup
  path on a slow host);
- By the time the harness reads `logs/freshness.jsonl` for the
  Expect.file assertions, the async writer has either:
  - completed → row present → assertion passes (expected);
  - been killed mid-flight → row absent → assertion fails
    (regression surface).

The `/quit` pattern also satisfies the `exit_code.equals(0)`
assertion — without `/quit`, the PTY would timeout-kill the session
and yield a non-zero exit code. This is the sibling pattern of E3-E10
(all use `/quit` as the final input for the same reason).

For SubagentStop specifically, there is an additional bonus: the
sub-agent returns control to the parent before `/quit` is issued, so
the SubagentStop hook fires earlier in the prompt sequence than the
parent's own teardown. The async writer has the gap between
"sub-agent returned" and "parent processes `/quit`" to flush — which
is typically tens of milliseconds on the lightweight Explore task,
well in excess of the flock+decrement microseconds. This gives E11
slightly more flush headroom than E10 (where SubagentStart fires at
the parent's busiest moment — the Task tool round-trip itself), but
the body does not rely on this margin; the binary substring assertion
remains the same.

A `sleep` prompt was considered as an alternative wait mechanism but
rejected for the same reasons documented in D-0093 / D-0094: Claude
Code does not expose a deterministic sleep tool to the agent; the
teardown-based wait is already deterministic and matches the pattern
used by every other hook-lifecycle eval. Adding a sleep would create
a divergent pattern and weaken sibling-trio symmetry.

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
`logs/freshness.jsonl` with the SubagentStop row from E11's surface.
The E11 assertion uses `Expect.file.contains` which only requires
the `subagent_stop` substring to appear somewhere in the file — the
post_read rows are harmless. Symmetrically, the SubagentStart row
that E10 asserts on also coexists in the ledger; E11's assertion
ignores it.

If a future change introduces a "filter ledger rows by hook event"
predicate (D-4 callback escape hatch), E11's assertion could be
narrowed to "exactly one subagent_stop row, regardless of co-fires"
— and the start/stop symmetry predicate could be expressed natively
— but the current binary substring presence is sufficient for the
OQ-2 minimum AC.

## Telemetry gap inheritance

The `freshness-subagent-stop.sh` script telemetry gap (writes to
`state/bg-agents/<sid>.txt` as a bare integer counter — decremented
and floored at 0; not `logs/freshness.jsonl`; no `type` field on its
current output) applies only to E11 — no sibling eval shares this
script. The OQ-2 frozen body lands verbatim per the established
T05.07..T05.15 posture: the script update is a single-script change
that unblocks E11 specifically.

Unlike E6/E7/E8 (which share `freshness-pre-edit.sh` and so were
unblocked by a single script update), there is no batching opportunity
here for E11 — E11's hook-script update is independent. E10 (T05.15)
had an analogous independent update for `freshness-subagent-start.sh`,
which means the SubagentStart/SubagentStop pair represents two
distinct (but structurally identical) follow-up tasks. The same
template (path migration to `logs/freshness.jsonl` + field-name
normalization to `type`) applies to both scripts, so the follow-up
tasks can reuse the patterns established for the other freshness
hook scripts.

A side-effect of the pair-separated script architecture: a future
script-update change can land both `freshness-subagent-start.sh`
and `freshness-subagent-stop.sh` in a single commit (they share the
same emit-observables template + paired roadmap rows R-093/R-094),
which would be the natural way to ship the SubagentStart/SubagentStop
JSONL contract together. T05.16 does not own that change; it merely
unblocks the manifest body for the SubagentStop side.

## Sibling-trio comparison (cross-event surface)

The nine post-OQ-2 hook-lifecycle evals share a common structural
template (single-prompt or seeded fire + `/quit` exit; freshness
ledger + type substring + exit code assertions):

| Field | E3 (sess-init) | E4 (sess-start) | E5 (user-prompt) | E6 (Edit) | E7 (Write) | E8 (serena) | E9 (Read) | E10 (SubagentStart) | E11 (SubagentStop) |
|---|---|---|---|---|---|---|---|---|---|
| Hook script | `session-init.sh` | `freshness-session-start.sh` | `freshness-user-prompt.sh` | `freshness-pre-edit.sh` | `freshness-pre-edit.sh` | `freshness-pre-edit.sh` | `freshness-post-read.sh` | `freshness-subagent-start.sh` | `freshness-subagent-stop.sh` |
| Hook event | SessionStart | SessionStart | UserPromptSubmit | PreToolUse | PreToolUse | PreToolUse | PostToolUse | SubagentStart | SubagentStop |
| Hook async? | no | no | no | no | no | no | **yes** | **yes** | **yes** |
| Matcher? | none | `*` | none | `Edit\|Write\|serena` | `Edit\|Write\|serena` | `Edit\|Write\|serena` | `Read` | none | none |
| `requires` | `[]` | `[]` | `[]` | `[]` | `[]` | `[mcp_server.serena]` | `[]` | `[]` | `[]` |
| Type substring | `"type":"session_init"` | `"type":"session_start"` | `"type":"user_prompt"` | `"type":"pre_edit"` | `"type":"pre_edit"` | `"type":"pre_edit"` | `"type":"post_read"` | `"type":"subagent_start"` | `"type":"subagent_stop"` |
| Matcher pin | — | — | — | `"matcher":"Edit"` | `"matcher":"Write"` | `"matcher":"mcp__serena__replace_content"` | — | — | — |
| Scratch file | — | — | — | `edited.txt` | `written.txt` | `modified.txt` | `fixture.txt` | — | — |
| Inputs | `/quit` | `/quit` | `echo test` → `/quit` | Write → Edit → `/quit` | Write → `/quit` | Write → serena → `/quit` | Write → Read → `/quit` | Task(Explore) → `/quit` | Task(Explore) → `/quit` |

E11 fits the template with three distinguishing characteristics:

1. **Third async hook eval** — inherits the E9 / E10 PTY-teardown
   reap posture; relies on the binary substring presence as the
   operational guarantee.
2. **No matcher pin** — like E3, E5, and E10 (also no-matcher hooks),
   uses a single-substring assertion (only the type label
   discriminates the SubagentStop branch).
3. **No scratch file** — unlike E6/E7/E8/E9, E11 does not need a
   seeded file; the Task tool invocation is self-contained.
4. **Identical input shape to E10** — the only structural difference
   between E10 and E11 is the asserted substring (`subagent_start`
   vs. `subagent_stop`); the prompt sequence is byte-for-byte
   identical, by lifecycle-pair design.

The matrix is intentional — it gives a future reviewer a clean
comparison across all nine hook-lifecycle evals to spot regressions
in matcher routing or capability gating.

## E10 ↔ E11 pair design (closing the loop)

E10 and E11 are designed as a **lifecycle pair** on the sub-agent
spawn/return cycle, as established in D-0094 §"E10 ↔ E11 pair
design". T05.16 closes the loop opened by T05.15. The shared input
shape (a Task tool invocation) fires both SubagentStart (E10's
surface) and SubagentStop (E11's surface) on the same prompt. The
two evals could in principle have been folded into one entry with two
type-substring assertions, but the OQ-2 resolution (D-0082 §4) keeps
them separate for two reasons restated here for completeness:

1. **Roadmap-row separation** — E10 maps to R-093, E11 to R-094;
   merging them would conflate two roadmap items.
2. **Failure-mode separation** — keeping the two assertions in
   separate evals lets the test report tell the reviewer
   independently whether SubagentStart fired but SubagentStop
   didn't (the dangling-sub-agent case), or vice versa
   (the orphaned-stop case). A merged eval would mask which side
   of the pair regressed.

The start/stop symmetry predicate
(`event_count(subagent_start) == event_count(subagent_stop)`) named
in D-0082 §4 row E11 as a secondary assertion is the cross-pair
invariant that would normally live in a merged eval; it is deferred
per §3 footnote in D-0095 spec.md until either D-4's callback escape
hatch is exercised or a future schema bump adds a declarative
shorthand.

The pair's separation also makes the script-update follow-up natural
to scope: one diff for `freshness-subagent-start.sh` (unblocking E10),
one diff for `freshness-subagent-stop.sh` (unblocking E11) —
shippable independently or jointly (per "Telemetry gap inheritance"
above). E11 closes the manifest-authoring half of the pair; the
script-update half is the next checkpoint.

## What "wait for stop hook flush" means in OQ-2 row E11

D-0082 §4 row E11 prescribes "spawn session, invoke sub-agent as in
E10, allow completion, wait for stop hook flush" as the inputs
shape. The "wait for stop hook flush" phrasing is implementation-
neutral; T05.16 implements it via the `/quit` teardown reap (per
"Async-branch nuance" above), which is the same mechanism used by
T05.14 (E9) and T05.15 (E10). Alternative implementations considered
and rejected:

- **Explicit `sleep N` prompt** — rejected per the same reasoning as
  E9 / E10 (no deterministic sleep tool exposed to the agent).
- **Polling the freshness ledger from a tooled prompt** — would
  require the parent session to be aware of the ledger path, which
  is host-state-dependent; rejected for portability.
- **Adding a `Expect.async_wait` primitive** — out of scope for T05.16
  and not present in the current expect.py.

The `/quit` teardown is therefore the canonical wait mechanism for
async hook evals in the v1 manifest, and E11 inherits this convention
without modification.
