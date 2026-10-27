# D-0093 — Notes / Design Rationale

## Why a Write seed precedes the Read call

The Read tool requires a pre-existing file at the target path;
without a seed file the Read call would either error or fall back
to a help message and never reach the PostToolUse hook with a
successful `tool_response`. E6 (D-0090) and E8 (D-0092) faced the
same constraint for the Edit / serena branches and resolved it with
a Write seed; E9 follows the same pattern: Write `fixture.txt` with
`'content'`, then Read it.

The seed Write fires the PreToolUse hook on the Write matcher
branch — emitting a row with `"matcher":"Write"`. The Read call
fires the PostToolUse hook on the Read matcher branch — emitting a
row with `"type":"post_read"`. Both rows coexist in
`logs/freshness.jsonl`; the E9 assertion uses `Expect.file.contains`
which only requires the `post_read` substring to appear somewhere,
so the Write co-fire is harmless.

E7 (D-0091) already pins the Write branch independently, so no
coverage is gained by isolating E9's input to a Read-only call (e.g.,
by reading a system file like `/etc/hostname` outside the per-eval
HOME).

## Why `fixture.txt` (not a system file or a project-tree file)

The fixture must live **inside** the per-eval HOME so it gets cleaned
up by FR-ISO2's per-eval HOME teardown. Reading a system file
(`/etc/hostname`) or a project-tree file (`CLAUDE.md`) would work
on most hosts but:

- introduces a host-state dependency (the system file might be
  permission-denied or missing on minimal containers; the project
  file path might shift after a checkout move);
- bypasses the FR-ISO2 isolation contract — the eval would observe
  a path outside `EvalContext.scratch_root`, violating the per-task
  AC ("does not read/write outside `EvalContext.scratch_root`").

Seeding `fixture.txt` under the per-eval HOME (via the Write tool,
which the agent runs against the cwd that defaults to `$HOME` under
PTY harness setup) keeps E9 self-contained and FR-ISO2-compliant.

## Why a single-substring assertion (not the two-substring pattern)

E6 / E7 / E8 use a two-substring assertion (`"type":"pre_edit"` +
`"matcher":"<branch>"`) because they cover three branches of the
same matcher group (`Edit|Write|mcp__serena__*`) and need to
discriminate which branch fired. The PostToolUse hook for Read has
only **one matcher pattern** in hooks.json — `"matcher": "Read"` —
with no fan-out. The `post_read` type label alone is sufficient to
prove the Read branch fired; no additional matcher pin is needed
(and there are no sibling Read-family branches to discriminate
against).

## Why `requires: []` (not `[mcp_server.*]`)

Read is a **built-in Claude Code tool**, not an MCP tool. It is
always available regardless of MCP server connectivity. Per
D-0082 §6 capability-tag rollup, E9's row lists no capability tag.
This matches siblings E3-E7 (no MCP) and differs from E1, E2.1-3,
and E8 (which require specific MCP servers).

The practical implication: E9 runs under `--no-mcp` (the
matcher-coverage gate counts it as a non-MCP eval), and the only
way E9 skips is via `--no-pty` (per-eval `no_pty: skip` tag).

## Async-branch nuance — why `/quit` is necessary

The OQ-2 D-0082 §4 row E9 inputs say "wait for async hook to flush"
without prescribing a specific input pattern for the wait. T05.14
implements the wait via the `/quit` clean-exit prompt:

- The PTY harness blocks on EOF after `/quit`;
- PTY teardown reaps any pending async writer processes — either
  by letting them complete naturally (the expected case for a
  fast flock+jq+append) or by SIGHUP'ing them mid-flight (cleanup
  path on a slow host);
- By the time the harness reads `logs/freshness.jsonl` for the
  Expect.file assertions, the async writer has either:
  - completed → row present → assertion passes (expected);
  - been killed mid-flight → row absent → assertion fails (regression
    surface).

The `/quit` pattern also satisfies the `exit_code.equals(0)`
assertion — without `/quit`, the PTY would timeout-kill the session
and yield a non-zero exit code. This is the sibling pattern of E3-E8
(all use `/quit` as the final input for the same reason).

A `sleep` prompt (e.g., `"wait 2 seconds"`) was considered as an
alternative wait mechanism but rejected:

- Claude Code does not expose a deterministic sleep tool to the
  agent; injecting "wait 2 seconds" would trigger a chat response,
  not a measurable delay;
- The teardown-based wait is already deterministic and matches the
  pattern used by every other hook-lifecycle eval (E3-E8); adding a
  sleep would create a divergent pattern and weaken sibling-trio
  symmetry.

## Telemetry gap inheritance

The `freshness-post-read.sh` script telemetry gap (writes to
`state/reads.jsonl`, not `logs/freshness.jsonl`; no `type` field on
its current envelope) applies only to E9 — no sibling eval shares
this script. The OQ-2-frozen body lands verbatim per the established
T05.07..T05.13 posture: the script update is a single-script change
that unblocks E9 specifically.

Unlike E6/E7/E8 (which share `freshness-pre-edit.sh`), there is no
batching opportunity here — E9's hook-script update is independent.
However, the same template (path migration to `logs/freshness.jsonl`
+ field-name normalization to `type` / `matcher`) applies, so the
follow-up task can reuse the patterns established for the pre-edit
script.

## Sibling-trio comparison (cross-event surface)

The seven post-OQ-2 hook-lifecycle evals share a common structural
template (single-prompt or seeded fire + `/quit` exit; freshness
ledger + type substring + exit code assertions):

| Field | E3 (sess-init) | E4 (sess-start) | E5 (user-prompt) | E6 (Edit) | E7 (Write) | E8 (serena) | E9 (Read) |
|---|---|---|---|---|---|---|---|
| Hook script | `session-init.sh` | `freshness-session-start.sh` | `freshness-user-prompt.sh` | `freshness-pre-edit.sh` | `freshness-pre-edit.sh` | `freshness-pre-edit.sh` | `freshness-post-read.sh` |
| Hook event | SessionStart | SessionStart | UserPromptSubmit | PreToolUse | PreToolUse | PreToolUse | PostToolUse |
| Hook async? | no | no | no | no | no | no | **yes** |
| `requires` | `[]` | `[]` | `[]` | `[]` | `[]` | `[mcp_server.serena]` | `[]` |
| Type substring | `"type":"session_init"` | `"type":"session_start"` | `"type":"user_prompt"` | `"type":"pre_edit"` | `"type":"pre_edit"` | `"type":"pre_edit"` | `"type":"post_read"` |
| Matcher pin | — | — | — | `"matcher":"Edit"` | `"matcher":"Write"` | `"matcher":"mcp__serena__replace_content"` | — |
| Scratch file | — | — | — | `edited.txt` | `written.txt` | `modified.txt` | `fixture.txt` |
| Inputs | `/quit` | `/quit` | `echo test` → `/quit` | Write → Edit → `/quit` | Write → `/quit` | Write → serena → `/quit` | Write → Read → `/quit` |

E9 fits the template with two distinguishing characteristics:

1. **First and only async hook eval** — relies on PTY teardown to
   reap the async writer, with the binary substring presence
   serving as the operational guarantee (timing-window assertion
   deferred per spec §3 footnote).
2. **Single-substring assertion** — no matcher fan-out, so no
   `"matcher":"Read"` pin needed.

The matrix is intentional — it gives a future reviewer a clean
comparison across all seven hook-lifecycle evals to spot regressions
in matcher routing or capability gating.
