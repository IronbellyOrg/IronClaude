# D-0095 — E11 SubagentStop Hook Coverage Eval (Body)

**Deliverable ID:** D-0095
**Task ID:** T05.16 (Phase 5)
**Roadmap items:** R-094 (E11 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-21
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E11 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E11 — the ninth of the
post-OQ-2 hook-event coverage entries (R-086 … R-098). E11 covers the
**SubagentStop hook** in `src/superclaude/hooks/hooks.json` — whose
command is `freshness-subagent-stop.sh` (timeout=1, `async: true`,
no matcher).

E11 is the **third async hook eval** in the roster — after E9
(D-0093 / PostToolUse Read async) and E10 (D-0094 / SubagentStart
async). Like its async siblings, the matched hook is declared
`async: true`, so the body relies on PTY teardown reaping the async
writer with the binary substring presence as the operationally-
meaningful guarantee that the hook fired and flushed before session
exit.

E11 closes the **sub-agent lifecycle pair** opened by E10. E10
covers SubagentStart firing; E11 covers the matched SubagentStop
firing with `event_count(subagent_start) == event_count(subagent_stop)`
symmetry called out as a secondary assertion in D-0082 §4 (deferred —
see §3 footnote). The two evals are designed as sibling pins on the
sub-agent spawn/return cycle and share the input shape (spawn a
sub-agent via the Task tool) while asserting different hook-event
substrings on opposite edges of the lifecycle.

The body must:

- spawn a fresh claude session via the PTY harness, inject a prompt
  that invokes a sub-agent via the Task tool (`subagent_type='Explore'`
  per D-0082 §4 "e.g., Explore or Plan" and the E10 D-0094 §"Why
  `subagent_type='Explore'`" rationale — read-only, lightweight,
  deterministic on a clean HOME), allow the sub-agent to complete and
  return control to the parent, then exit cleanly so the PTY teardown
  reaps both the sub-agent and the async SubagentStop hook writer;
- assert the hook's observable side-effects (freshness ledger present
  + `subagent_stop` event row);
- exit cleanly so the `exit_code.equals(0)` assertion can pin a clean
  `/quit` — and so the PTY teardown reaps any in-flight async writer
  (sibling pattern to E9 and E10);
- carry no capability tag (`requires: []`) — the Task / Agent tool is
  a built-in Claude Code tool, not an MCP tool, so E11 runs on every
  host and under `--no-mcp`.

## 2. Hook-surface contract (from `hooks.json` + OQ-2 D-0082 §4)

`src/superclaude/hooks/hooks.json` SubagentStop block:

```jsonc
"SubagentStop": [
  {
    "hooks": [
      { "type": "command",
        "command": "~/.claude/hooks/freshness-subagent-stop.sh",
        "timeout": 1,
        "async": true }
    ]
  }
]
```

Note the absence of a `"matcher"` field — SubagentStop has no
matcher-group fan-out, so every sub-agent return fires the same single
hook command. This mirrors the E3 SessionStart-unmatched, E5
UserPromptSubmit-unmatched, and E10 SubagentStart-unmatched shapes
(single-substring assertion, no matcher pin needed).

The OQ-2 resolution (D-0082 §4 row E11 / decisions.md OQ-2) freezes
E11's body shape to assert the hook's side-effects per the matched
branch:

| Observable | Purpose |
|---|---|
| `logs/freshness.jsonl` exists | proves the freshness event ledger was opened by `freshness-subagent-stop.sh` (or by a prior SessionStart / SubagentStart hook on the same spawn) |
| `logs/freshness.jsonl` contains `"type":"subagent_stop"` | proves the `subagent_stop`-typed event row was emitted to the freshness ledger by `freshness-subagent-stop.sh` **after** the async hook flushed |
| Process exits cleanly on `/quit` | sanity-pin that the spawn lifecycle ran end-to-end (and that the PTY teardown reaped the async writer) |

These three observables are independently sufficient and discriminate
three distinct failure modes: (a) the ledger existence pins that the
JSONL file was opened; (b) the `subagent_stop` substring pins that
the SubagentStop hook **emitted its event row** AFTER the async
branch flushed; (c) the exit code pins that the session reached clean
shutdown and the async writer was reaped.

The single-substring shape (`subagent_stop`) differs from the
two-substring shape used by E6 / E7 / E8 (Edit / Write / serena
matcher-coverage trio) because the SubagentStop hook has **no
matcher pattern** in hooks.json — there is no matcher-group fan-out
to discriminate. Asserting `"type":"subagent_stop"` is therefore
sufficient to prove the hook fired; no `"matcher":"..."` pin is
needed (no sibling SubagentStop branches exist).

The D-0082 §4 row E11 specification phrases the secondary assertion as
the start/stop **symmetry** predicate
`jsonl.event_count(logs/freshness.jsonl, type=subagent_start) ==
jsonl.event_count(logs/freshness.jsonl, type=subagent_stop)`. This
predicate requires:

1. Streaming `logs/freshness.jsonl` row-by-row twice (or once with
   two filter accumulators);
2. Filtering rows where `type == "subagent_start"` and rows where
   `type == "subagent_stop"`;
3. Counting each filtered set and asserting equality.

None of these are expressible in the current declarative DSL.
`Expect.jsonl.event_count` requires a Python callable filter
(`expect.py:269-369`); equality comparison across two filtered counts
requires a second-order callable. Following the same precedent as
E3-E10 sibling deferrals (event_count, per-prompt count
discrimination, event_count >= 1), T05.16 lands the OQ-2 body shape
with the binary substring assertion as a proxy: the substring is
present iff at least one row carries `"type":"subagent_stop"`. On a
single Task spawn (the body's input shape), `event_count(subagent_stop)
== event_count(subagent_start) == 1` is the only outcome where
symmetry holds AND substring is present, so the proxy is sufficient
for the operationally-meaningful boundary at this spawn count.

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E11 entry that
previously carried only stale scaffolding metadata (a placeholder
title from the pre-OQ-2 numbering and no body). T05.16 replaces the
scaffolding with the frozen body. Final shape:

| Field | Value |
|---|---|
| **title** | `"SubagentStop hook fires"` (matches D-0082 §4 OQ-2 row E11) |
| **category** | `hook-lifecycle` (sibling to E3-E10) |
| **requires** | `[]` — no capability tags; Task / Agent tool is a built-in Claude Code tool, no MCP needed |
| **timeout_sec** | `60` (raised from defaults' 120s — two-prompt PTY round-trip is bounded by the Task tool round-trip + 1s async flush, typically <30s on a lightweight Explore-glob task; 60s is generous; matches E3/E4/E5/E6/E7/E8/E9/E10 sibling for spawn-lifecycle parity) |
| **inputs[0].prompt** | Task fire: `"Use the Task tool with subagent_type='Explore' to find files matching '*.md' under the current working directory and report the count."` + `expect_tool_call: Task` — the Task invocation that spawns the Explore sub-agent (firing SubagentStart) and triggers SubagentStop when the sub-agent returns control |
| **inputs[1].prompt** | `"/quit"` — clean session exit so `exit_code.equals(0)` can pin the PTY teardown contract AND so the teardown reaps the async writer; the prompt also gives the SubagentStop async writer time to flush between the sub-agent's return and the parent session's teardown |
| **expects[0]** | `file: { path: logs/freshness.jsonl, exists: true }` |
| **expects[1]** | `file: { path: logs/freshness.jsonl, exists: true, contains: '"type":"subagent_stop"' }` |
| **expects[2]** | `exit_code: { equals: 0 }` |

PTY-exclusion tag: `no_pty: skip` (carried forward from the
scaffolding entry — every eval in the `real` suite is PTY-driven
per DOC-OQ3 / R-077).

No additions to `optional_capabilities` — Task / Agent is built into
Claude Code; no MCP server is required.

**Footnote — count-equality deferral.** D-0082 §4 row E11 lists a
secondary assertion `jsonl.event_count(logs/freshness.jsonl,
type=subagent_start) == jsonl.event_count(logs/freshness.jsonl,
type=subagent_stop)`. This predicate requires a Python callable
filter (`expect.py:269-369`) and a second-order equality across two
filtered counts; it is not expressible in declarative YAML. Following
the same precedent as E3-E10 sibling deferrals, T05.16 lands the OQ-2
body shape with the binary substring assertion as the operational
proxy. The substring is present iff at least one row carries
`"type":"subagent_stop"`; on the single-spawn input shape, the
equality predicate's only satisfying outcome (= 1, = 1) is exactly the
substring-present case, so the proxy preserves the boundary for this
body. The strict declarative form remains deferred until either (a)
the YAML callback escape hatch (D-4) is exercised for the start/stop
pair, or (b) a future schema bump adds a declarative
`jsonl: { event_count_equals_event_count: {...} }` shorthand. Neither
is in scope for T05.16.

Note: invoking the Task tool fires the SubagentStart hook before the
sub-agent begins and the SubagentStop hook after the sub-agent
returns. E11 only asserts the `subagent_stop` substring; E10 (T05.15)
independently asserts the paired `subagent_start` substring. Both
substrings coexist in `logs/freshness.jsonl` (post-script-update);
the E11 assertion uses `Expect.file.contains` which only requires the
`subagent_stop` substring to appear somewhere, so the SubagentStart
co-fire is harmless from E11's perspective.

## 4. Eval id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. The literal id `E11` is
trivially accepted — `eval describe --suite real --eval E11` returns
the full body and `eval list --json` continues to enumerate 17 evals
under suite `real`.

## 5. Determinism (3-run AC)

The body is deterministic on a clean per-eval HOME (D-0082 §2
constraint 2 / per-task AC):

- The PTY spawn writes a new freshness ledger entry on every
  SubagentStop fire (FR-ISO2 fresh HOME per eval — no carry-over).
- The Task tool invocation triggers exactly one SubagentStart event
  (on spawn) followed by exactly one SubagentStop event (on return)
  per the single Task prompt; the async SubagentStop hook emits one
  `subagent_stop`-typed counter decrement (post-script-update, one
  JSONL row with `"type":"subagent_stop"`).
- The chosen sub-agent task (glob `*.md` under cwd) is read-only,
  deterministic, and bounded — Explore will enumerate the per-eval
  HOME's markdown files (typically zero on a clean ephemeral HOME)
  and report the count, then return. No external network calls; no
  shared-state dependencies.
- The `/quit` input causes an immediate clean exit (exit code 0)
  after the async writer reaps.
- No time-of-day, network, or shared-state dependencies — D-0082 §2
  constraint 3 (no `CLAUDE_FAKE_TIME_OFFSET`) is honored. The `ts`,
  `session_id`, agent-type / agent-instance fields on the
  (post-update) JSONL row are not asserted against.

Three consecutive `eval run --suite real --eval E11` invocations on
a clean HOME must therefore yield identical EvalOutcome statuses,
which is the per-task acceptance criterion.

## 6. Schema validation

The body uses only manifest-supported constructs:

- `inputs[].prompt: string` (additionalProperties: true under
  `evalEntry.inputs.items` per `suite.schema.json`). The two-element
  `inputs[]` array is accepted by the open-shape array schema. The
  `expect_tool_call` field on `inputs[0]` is accepted by the
  open-shape (mirrors E1 / E2.1-3 / E8 / E9 / E10 usage).
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved at
  load-time by `Expect.from_mapping` (`expect.py:640-669`). All three
  primitives used (2×`file`, 1×`exit_code`) are in `PRIMITIVE_NAMES`
  (`expect.py:56-64`).
- `file` primitive kwargs `path`, `exists`, `contains` are supported
  by `Expect.file._build` (`expect.py:186-265`).
- `exit_code` primitive kwarg `equals` is supported by
  `Expect.exit_code._build`.
- `requires: []` (empty / omitted) is accepted by the schema.
- `timeout_sec: 60` is `integer ≥ 1` per schema.
- `isolation.home_strategy: ephemeral` is in the enum.
- `no_pty: skip` matches the enum.

No schema-version bump required.

## 7. `--no-mcp` and `--no-pty` behavior matrix

| Invocation | E11 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E11` (no flags) | RUNS | no capability tags; PTY harness present on host |
| `eval run --suite real --eval E11 --no-mcp` | RUNS | `requires: []` — no MCP capability to skip; Task tool is built-in |
| `eval run --suite real --eval E11 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077); `--no-pty` short-circuits before any eval body executes |
| `eval run --suite real --eval E11 --no-mcp --no-pty` | SKIPPED (`--no-pty`) | `--no-pty` short-circuits first per `commands.py` |

This posture matches siblings E3-E7 / E9 / E10 (which also carry
`requires: []`) and differs from E1 / E2.1-3 / E8 (which carry MCP
capability tags and soft-skip under `--no-mcp`).

## 8. Verification

Per phase-5-tasklist.md T05.16, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E11
```

**Today's runner state:** the same pre-existing `NameError: name
'_new_run_id' is not defined` in `cli/eval/commands.py:1418`
documented in T05.03 / T05.04 / T05.05 / T05.07 / T05.08 / T05.09 /
T05.10 / T05.11 / T05.13 / T05.14 / T05.15 evidence blocks all block
any direct `eval run` invocation. That blocker is the responsibility
of the runner-completion task (Phase-5 dependency of the CP-P05-T13-T17
checkpoint at T05.18). T05.16 authors the manifest body; observable
verification is therefore via:

- (a) `eval describe --suite real --eval E11` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.16/describe-E11.txt`);
- (b) `eval list --json` continuing to enumerate suite `real`
  with 17 evals (proves schema acceptance; see
  `evidence/T05.16/list-with-E11.txt`);
- (c) `Expect.from_mapping` round-trip over each `expects[]` row
  (proves declarative DSL resolution; see
  `evidence/T05.16/expect-roundtrip.txt`).

Full end-to-end PTY execution + 3-run determinism proof rolls
into the runner-completion task downstream of T05.16.

### 8.1 Risk note — freshness-subagent-stop.sh telemetry gap

`src/superclaude/hooks/scripts/freshness-subagent-stop.sh` (current
revision as of 2026-05-21, lines 6-28) writes a plain integer
counter (decremented, floored at 0) to
`$HOME/.claude/state/bg-agents/<session_id>.txt`:

```bash
cur=0
[ -f "$BG_FILE" ] && cur=$(cat "$BG_FILE" 2>/dev/null || echo 0)
case "$cur" in ''|*[!0-9]*) cur=0 ;; esac
if [ "$cur" -gt 0 ]; then
    echo $((cur - 1)) > "$BG_FILE" 2>/dev/null || true
else
    echo "0" > "$BG_FILE" 2>/dev/null || true
fi
```

The OQ-2 D-0082 §4 body shape — which T05.16 lands verbatim —
asserts **both a different path** (`logs/freshness.jsonl`) **and a
JSONL envelope** (`"type":"subagent_stop"`) rather than a bare
integer counter file. The script does NOT write to
`logs/freshness.jsonl` and does NOT emit a JSONL envelope with a
`type` field.

This gap is **not introduced** by T05.16; it predates the
deliverable and mirrors the identical telemetry gaps discovered
for `session-init.sh` during T05.07 (D-0087 §8.1),
`freshness-session-start.sh` during T05.08 (D-0088 §8.1),
`freshness-user-prompt.sh` during T05.09 (D-0089 §8.1),
`freshness-pre-edit.sh` during T05.10 / T05.11 / T05.13
(D-0090/D-0091/D-0092 §8.1), `freshness-post-read.sh` during
T05.14 (D-0093 §8.1), and `freshness-subagent-start.sh` during
T05.15 (D-0094 §8.1). E11 stands alone in script terms (no sibling
shares `freshness-subagent-stop.sh`); the paired
`freshness-subagent-start.sh` (E10) is structurally analogous but a
distinct script, so the script-update follow-up will land two
updates (one per script) for the SubagentStart/SubagentStop pair.

Acceptance criteria for T05.16 (manifest body landed, FR-SCH2-valid
id, OQ-2 body shape recorded, spec/notes/evidence written) are met
by the describe / list / roundtrip evidence above; the per-task AC
that requires `eval run --eval E11` to exit 0 deterministically
depends transitively on (a) the runner NameError fix, and (b) the
freshness-subagent-stop.sh emit-observables update with the OQ-2
contract path + field name.

### 8.2 Async-branch reaping under PTY teardown

Because the matched hook is `async: true` (same as E9's PostToolUse
Read and E10's SubagentStart), the Claude Code runtime does NOT
block on the hook's exit before returning control to the parent
session. The hook writer is a detached background process whose
flock-protected counter decrement (and, post-script-update, freshness
ledger append) runs out-of-band. The `/quit` teardown reaps the async
writer via standard PTY exit-on-EOF: the shell process tree under the
PTY is sent SIGHUP, which the async writer either completes before
receiving (most common case — flock + decrement is microseconds) or
is killed mid-flight (cleanup path).

E11 inherits the E9 / E10 posture: it does NOT assert a specific
bound on the flush delay (D-4 callback would be needed for that —
deferred per §3 footnote). The binary substring presence is the
operationally-meaningful guarantee: on a host where the async writer
races teardown, the substring assertion fails and the eval surfaces
the regression. On a host where the writer completes pre-teardown
(the expected case), the substring is present and the eval passes.

The SubagentStop async window has slightly more headroom than
SubagentStart's because the sub-agent's return-to-parent and the
parent's wait at the next prompt give the async writer additional
microseconds before the `/quit` teardown — but the eval body does not
rely on this margin; the same flock+decrement timing reasoning
established for the SubagentStart sibling carries through unchanged.

### 8.3 Sub-agent lifecycle co-fire considerations

Invoking the Task tool fires three hook events in sequence:

1. **SubagentStart** — async, fires when the sub-agent process is
   spawned. Covered by E10 (D-0094).
2. **(sub-agent runs its work)** — Explore reads files and reports;
   any internal tool calls fire their own PreToolUse / PostToolUse
   hooks under the sub-agent's process tree (independent of the
   parent session's hooks for accounting purposes).
3. **SubagentStop** (this eval's surface) — async, fires when the
   sub-agent returns control to the parent session.

E11 asserts **only** the SubagentStop substring. The SubagentStart
co-fire is harmless because `Expect.file.contains` requires only that
the asserted substring (`"type":"subagent_stop"`) appear somewhere
in the file — the `subagent_start` row coexisting is benign.

E10 (T05.15) independently asserts the paired `"type":"subagent_start"`
substring. Together, E10 and E11 form a lifecycle pair on the
sub-agent spawn/return cycle. The OQ-2 D-0082 §4 row E11 names a
start/stop symmetry predicate
(`event_count(subagent_start) == event_count(subagent_stop)`) — a
Python-callable predicate that follows the same deferral pattern
established in §3 footnote.

The Explore sub-agent's own internal PostToolUse Read co-fires (one
per Read call inside Explore) emit `"type":"post_read"` rows to the
same `logs/freshness.jsonl` ledger. These coexist with the
`subagent_stop` row and are harmless to the substring assertion (E9
covers the post_read surface independently in D-0093).

## 9. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T05.01 / D-0082 | OQ-2 resolution — frozen body shape |
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts literal `E11` |
| Depends on | T04.02 / T04.03 (Expect.file impl) | satisfied by current `expect.py` |
| Depends on | T04.04 / T04.05 (Expect.exit_code impl) | satisfied by current `expect.py` |
| Depends on | T05.15 / D-0094 (E10 body) | establishes the no-matcher async-hook body template + sub-agent lifecycle pair design that E11 mirrors |
| Sibling | T05.07 (E3 body) | first-position SessionStart hook (no-matcher single-substring template — same shape as E11) |
| Sibling | T05.09 (E5 body) | UserPromptSubmit no-matcher hook (no-matcher single-substring template — same shape as E11) |
| Sibling | T05.14 (E9 body) | PostToolUse Read async hook (first async hook eval; established the PTY-teardown reap pattern that E11 follows) |
| Paired | T05.15 (E10 body) | SubagentStart hook — paired with E11 on sub-agent lifecycle; E10 asserts subagent_start substring; symmetry predicate deferred per §3 footnote |
| Unblocks | T05.18 (CP-P05-T13-T17 checkpoint) | E11 must enumerate + describe; full-run verification follows runner fix |
| Unblocks | Hook-script follow-up | `freshness-subagent-stop.sh` emit-observables update (paired with `freshness-subagent-start.sh` per §8.1) |

## 10. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟢 AUTHORED | Claude (Opus 4.7) | 2026-05-21 |
| 🟢 BODY FROZEN | per D-0082 §4 / decisions.md OQ-2 | 2026-05-21 |
