# D-0093 — E9 PostToolUse Read Async Hook Coverage Eval (Body)

**Deliverable ID:** D-0093
**Task ID:** T05.14 (Phase 5)
**Roadmap items:** R-092 (E9 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E9 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E9 — the seventh of the
post-OQ-2 hook-event coverage entries (R-086 … R-098). E9 covers the
**PostToolUse Read async branch** in `src/superclaude/hooks/hooks.json` —
whose command is `freshness-post-read.sh` (timeout=1, `async: true`).

E9 is the **only PostToolUse eval whose matched hook is declared
`async: true`** — distinct from the synchronous PostToolUse auggie-family
matchers covered by E1 / E2.1-3 (which fire `auggie-flag-clear.sh`
synchronously on the `mcp__auggie__.*|mcp__auggie-mcp__.*|mcp__airis-mcp-gateway__auggie_.*`
matcher). E9's specific value is pinning the **async branch** behaves
correctly: the hook fires after the Read returns, flushes its telemetry
row out-of-band, and the PTY harness sees the row materialised in the
freshness ledger by the time the session exits cleanly.

The body must:

- spawn a fresh claude session via the PTY harness, seed a scratch
  fixture file with a single Write prompt (Read requires a pre-existing
  target), then inject a prompt that triggers a single `Read` against
  the fixture so the PostToolUse hook fires on the Read matcher;
- assert the hook's observable side-effects (freshness ledger present
  + `post_read` event row);
- exit cleanly so the `exit_code.equals(0)` assertion can pin a clean
  `/quit` — and so the PTY teardown reaps the async writer;
- carry no capability tag (`requires: []`) — Read is a built-in Claude
  Code tool, so the eval runs on every host.

## 2. Hook-surface contract (from `hooks.json` + OQ-2 D-0082 §4)

`src/superclaude/hooks/hooks.json` PostToolUse block (Read branch):

```jsonc
"PostToolUse": [
  {
    "matcher": "Read",
    "hooks": [
      { "type": "command",
        "command": "~/.claude/hooks/freshness-post-read.sh",
        "timeout": 1,
        "async": true }
    ]
  }
]
```

The OQ-2 resolution (D-0082 §4 row E9 / decisions.md OQ-2) freezes
E9's body shape to assert the hook's side-effects per the matched
branch:

| Observable | Purpose |
|---|---|
| `logs/freshness.jsonl` exists | proves the freshness event ledger was opened by `freshness-post-read.sh` (or by a prior SessionStart hook on the same spawn) |
| `logs/freshness.jsonl` contains `"type":"post_read"` | proves the `post_read`-typed event row was emitted to the freshness ledger by `freshness-post-read.sh` **after** the async hook flushed |
| Process exits cleanly on `/quit` | sanity-pin that the spawn lifecycle ran end-to-end (and that the PTY teardown reaped the async writer) |

These three observables are independently sufficient and discriminate
three distinct failure modes: (a) the ledger existence pins that the
JSONL file was opened; (b) the `post_read` substring pins that the
PostToolUse hook **emitted its event row** AFTER the async branch
flushed; (c) the exit code pins that the session reached clean
shutdown and the async writer was reaped.

The single-substring shape (`post_read`) differs from the
two-substring shape used by E2.1-3 / E6-E8 because the PostToolUse
Read hook has only **one matcher pattern** (`Read`) — there is no
matcher-group fan-out to discriminate. Asserting `"type":"post_read"`
is therefore sufficient to prove the Read-branch fired; no
`"matcher":"Read"` pin is needed (the type label already
identifies the matched branch uniquely).

The D-0082 §4 row E9 specification phrases the secondary
duration-window assertion as
`duration.less_than(post_read_event_ts - read_complete_ts, 2.0)`
(async hook flushes within 2s). See §3 footnote for the explicit
deferral of that intra-eval timestamp-delta aspect to the YAML
callback escape hatch (D-4); the binary substring presence is a
sufficient proxy for the operationally-meaningful guarantee (the
row materialised before session teardown).

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E9 entry that
previously carried only stale scaffolding metadata (a placeholder
title `"installer copies skills into ~/.claude/skills"` from the
pre-OQ-2 numbering and no body). T05.14 replaces the scaffolding
with the frozen body. Final shape:

| Field | Value |
|---|---|
| **title** | `"PostToolUse Read async hook fires"` (matches D-0082 §4 OQ-2 row E9) |
| **category** | `hook-lifecycle` (sibling to E3-E8; was `installer` in stale stub) |
| **requires** | `[]` — no capability tags; Read is a built-in Claude Code tool, no MCP needed |
| **timeout_sec** | `60` (raised from defaults' 120s — three-prompt PTY round-trip is bounded by the Read round-trip + 1s async flush, typically <30s; 60s is generous; matches E3/E4/E5/E6/E7/E8 sibling for spawn-lifecycle parity) |
| **inputs[0].prompt** | Seed Write: `"Use the Write tool to create a file named fixture.txt under the current working directory with the single line 'content'."` — pre-creates the file because Read requires a pre-existing target |
| **inputs[1].prompt** | Read fire: `"Use the Read tool to read fixture.txt."` + `expect_tool_call: Read` — the Read invocation that fires the PostToolUse hook on the Read matcher branch |
| **inputs[2].prompt** | `"/quit"` — clean session exit so `exit_code.equals(0)` can pin the PTY teardown contract AND so the teardown reaps the async writer |
| **expects[0]** | `file: { path: logs/freshness.jsonl, exists: true }` |
| **expects[1]** | `file: { path: logs/freshness.jsonl, exists: true, contains: '"type":"post_read"' }` |
| **expects[2]** | `exit_code: { equals: 0 }` |

PTY-exclusion tag: `no_pty: skip` (carried forward from the
scaffolding entry — every eval in the `real` suite is PTY-driven
per DOC-OQ3 / R-077).

No additions to `optional_capabilities` — Read is built into Claude
Code; no MCP server is required.

**Footnote — duration-window deferral.** D-0082 §4 row E9 lists a
secondary assertion `duration.less_than(post_read_event_ts -
read_complete_ts, 2.0)` (async hook flushes within 2s of the Read
returning). This predicate requires:

1. Capturing two distinct intra-eval timestamps (the `tool_response`
   `read_complete_ts` and the `freshness.jsonl` row's `ts` field);
2. Subtracting them to compute the flush delta;
3. Asserting the delta is less than 2.0s.

None of these are expressible in the current declarative DSL.
`Expect.duration` measures the **total eval duration** via
`ctx.duration_sec` (`expect.py:590-636`), not arbitrary intra-eval
timestamp deltas. A Python callable filter (`expect.py:269-369`)
could compute the delta from the JSONL row but does not have access
to the tool-response timestamp directly.

Following the same precedent as E3-E8 sibling deferrals
(`event_count`, per-prompt count discrimination), T05.14 lands the
OQ-2 body shape with the binary substring assertion as a proxy for
the timing assertion. If the row is present when the PTY harness
reads the ledger after `/quit`, the async branch flushed before
session teardown — which is the operationally-meaningful guarantee.
The strict <2s window assertion is deferred until either (a) the
YAML callback escape hatch (D-4) is exercised for E9, or (b) a
future schema bump adds a declarative
`jsonl: { contains_event: { type: ..., max_delay_from_input: 2.0 } }`
shorthand. Neither is in scope for T05.14; the current body satisfies
the OQ-2 minimum AC ("body matches the OQ-2 resolution; runs
deterministically on a clean HOME").

Note: the seed Write prompt (`inputs[0]`) will fire the PreToolUse
hook on the Write matcher branch, producing a row with
`"matcher":"Write"` in `logs/freshness.jsonl` (covered independently
by E7). The Write co-fire is harmless; the E9 assertion uses
`Expect.file.contains` which only requires the `post_read` substring
to appear somewhere in the file — the Write-row coexists with the
post_read-row, and the assertion succeeds when the post_read substring
is present.

## 4. Eval id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. The literal id `E9` is
trivially accepted — `eval describe --suite real --eval E9` returns
the full body and `eval list --json` continues to enumerate 17 evals
under suite `real`.

## 5. Determinism (3-run AC)

The body is deterministic on a clean per-eval HOME (D-0082 §2
constraint 2 / per-task AC):

- The PTY spawn writes a new freshness ledger entry on every
  PostToolUse Read fire (FR-ISO2 fresh HOME per eval — no carry-over).
- The Write seed creates `fixture.txt` with content `'content'` —
  deterministic content; deterministic file existence.
- The Read call reads `fixture.txt` — fires PostToolUse on the Read
  matcher exactly once per the single Read prompt; the async hook
  emits one `post_read`-typed row.
- The `/quit` input causes an immediate clean exit (exit code 0) after
  the async writer reaps.
- No time-of-day, network, or shared-state dependencies — D-0082 §2
  constraint 3 (no `CLAUDE_FAKE_TIME_OFFSET`) is honored. The `ts`,
  `ts_unix`, `session_id`, `tool_call_idx`, `path` fields on the JSONL
  row are not asserted against.

Three consecutive `eval run --suite real --eval E9` invocations on a
clean HOME must therefore yield identical EvalOutcome statuses, which
is the per-task acceptance criterion.

## 6. Schema validation

The body uses only manifest-supported constructs:

- `inputs[].prompt: string` (additionalProperties: true under
  `evalEntry.inputs.items` per `suite.schema.json`). The three-element
  `inputs[]` array is accepted by the open-shape array schema. The
  `expect_tool_call` field on `inputs[1]` is accepted by the open-shape
  (mirrors E1 / E2.1-3 / E8 usage).
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved at
  load-time by `Expect.from_mapping` (`expect.py:640-669`). All three
  primitives used (2×`file`, 1×`exit_code`) are in `PRIMITIVE_NAMES`
  (`expect.py:56-64`).
- `file` primitive kwargs `path`, `exists`, `contains` are supported
  by `Expect.file._build` (`expect.py:186-265`).
- `exit_code` primitive kwarg `equals` is supported by
  `Expect.exit_code._build`.
- `requires: []` (empty) is accepted by the schema.
- `timeout_sec: 60` is `integer ≥ 1` per schema.
- `isolation.home_strategy: ephemeral` is in the enum.
- `no_pty: skip` matches the enum.

No schema-version bump required.

## 7. `--no-mcp` and `--no-pty` behavior matrix

| Invocation | E9 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E9` (no flags) | RUNS | no capability tags; PTY harness present on host |
| `eval run --suite real --eval E9 --no-mcp` | RUNS | `requires: []` — no MCP capability to skip |
| `eval run --suite real --eval E9 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077); `--no-pty` short-circuits before any eval body executes |
| `eval run --suite real --eval E9 --no-mcp --no-pty` | SKIPPED (`--no-pty`) | `--no-pty` short-circuits first per `commands.py` |

This posture matches siblings E3-E7 (which also carry `requires: []`)
and differs from E8 (which carries `requires: [mcp_server.serena]`
and soft-skips under `--no-mcp`).

## 8. Verification

Per phase-5-tasklist.md T05.14, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E9
```

**Today's runner state:** the same pre-existing `NameError: name
'_new_run_id' is not defined` in `cli/eval/commands.py:1418`
documented in T05.03 / T05.04 / T05.05 / T05.07 / T05.08 / T05.09 /
T05.10 / T05.11 / T05.13 evidence blocks all block any direct
`eval run` invocation. That blocker is the responsibility of the
runner-completion task (Phase-5 dependency of the CP-P05-T13-T17
checkpoint at T05.18). T05.14 authors the manifest body; observable
verification is therefore via:

- (a) `eval describe --suite real --eval E9` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.14/describe-E9.txt`);
- (b) `eval list --json` continuing to enumerate suite `real`
  with 17 evals (proves schema acceptance; see
  `evidence/T05.14/list-with-E9.txt`);
- (c) `Expect.from_mapping` round-trip over each `expects[]` row
  (proves declarative DSL resolution; see
  `evidence/T05.14/expect-roundtrip.txt`).

Full end-to-end PTY execution + 3-run determinism proof rolls
into the runner-completion task downstream of T05.14.

### 8.1 Risk note — freshness-post-read.sh telemetry gap

`src/superclaude/hooks/scripts/freshness-post-read.sh` (current
revision as of 2026-05-20, lines 42-46) emits a JSONL envelope
to **`$HOME/.claude/state/reads.jsonl`** with the schema:

```json
{"ts":...,"ts_unix":...,"session_id":...,"path":...,"tool_call_idx":...}
```

The OQ-2 D-0082 §4 body shape — which T05.14 lands verbatim —
asserts **both a different path** (`logs/freshness.jsonl`) **and a
different field name** (`type=post_read`, not just the field-less
envelope). The script does NOT write to `logs/freshness.jsonl` and
does NOT use a `type` field on its current telemetry path.

This gap is **not introduced** by T05.14; it predates the
deliverable and mirrors the identical telemetry gaps discovered
for `session-init.sh` during T05.07 (D-0087 §8.1),
`freshness-session-start.sh` during T05.08 (D-0088 §8.1),
`freshness-user-prompt.sh` during T05.09 (D-0089 §8.1), and
`freshness-pre-edit.sh` during T05.10 / T05.11 / T05.13
(D-0090/D-0091/D-0092 §8.1). E9 stands alone in script terms
(no sibling shares `freshness-post-read.sh`), so the single
hook-script update for this script only unblocks E9.

Acceptance criteria for T05.14 (manifest body landed, FR-SCH2-valid
id, OQ-2 body shape recorded, spec/notes/evidence written) are met
by the describe / list / roundtrip evidence above; the per-task AC
that requires `eval run --eval E9` to exit 0 deterministically
depends transitively on (a) the runner NameError fix, and (b) the
freshness-post-read.sh emit-observables update with the OQ-2
contract path + field name.

### 8.2 Async-branch reaping under PTY teardown

Because the matched hook is `async: true`, the Claude Code runtime
does NOT block on the hook's exit before returning the Read's
`tool_response`. The hook writer is a detached background process
whose flock-protected append to `reads.jsonl` (and, post-script-update,
`logs/freshness.jsonl`) runs out-of-band. The `/quit` teardown reaps
the async writer via standard PTY exit-on-EOF: the shell process tree
under the PTY is sent SIGHUP, which the async writer either completes
before receiving (most common case — flock + jq + append is <100ms)
or is killed mid-flight (cleanup path).

T05.14 does NOT assert a specific bound on the flush delay (D-4
callback would be needed for that — deferred per §3 footnote). The
binary substring presence is the operationally-meaningful guarantee:
on a host where the async writer races teardown, the substring
assertion fails and the eval surfaces the regression. On a host
where the writer completes pre-teardown (the expected case), the
substring is present and the eval passes.

## 9. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T05.01 / D-0082 | OQ-2 resolution — frozen body shape |
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts literal `E9` |
| Depends on | T04.02 / T04.03 (Expect.file impl) | satisfied by current `expect.py` |
| Depends on | T04.04 / T04.05 (Expect.exit_code impl) | satisfied by current `expect.py` |
| Sibling | T05.07 (E3 body) | first-position SessionStart hook (same comment-block template, different hook surface) |
| Sibling | T05.08 (E4 body) | second-position SessionStart matcher=* hook (same JSONL ledger, different hook surface) |
| Sibling | T05.09 (E5 body) | UserPromptSubmit no-matcher hook (same freshness JSONL ledger, different hook surface) |
| Sibling | T05.10 (E6 body) | PreToolUse Edit matcher (sibling matcher-coverage trio — distinct hook script) |
| Sibling | T05.11 (E7 body) | PreToolUse Write matcher (sibling matcher-coverage trio — distinct hook script) |
| Sibling | T05.13 (E8 body) | PreToolUse serena matcher (sibling matcher-coverage trio — distinct hook script) |
| Unblocks | T05.15 (E10 body) | follows the no-MCP, single-matcher body template established here |
| Unblocks | T05.18 (CP-P05-T13-T17 checkpoint) | E9 must enumerate + describe; full-run verification follows runner fix |

## 10. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟢 AUTHORED | Claude (Opus 4.7) | 2026-05-20 |
| 🟢 BODY FROZEN | per D-0082 §4 / decisions.md OQ-2 | 2026-05-20 |
