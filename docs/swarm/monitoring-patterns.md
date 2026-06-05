# Swarm Monitoring Patterns (FR-013 / T07.10)

Three durable monitoring patterns are supported against any running
swarm job. All three read the **caller-agnostic** observability artifacts
written under the job's `--output` directory:

| Artifact | Purpose | Module |
|---|---|---|
| `.swarm-state.json` | Coarse wave phase (DM-014) | `state.py` |
| `execution-log.jsonl` | Append-only event stream (DM-015) | `logging_.py` |
| `execution-log.md` | Human-readable mirror of the JSONL stream | `logging_.py` |
| `done.json` | Atomic terminal sentinel (DM-017) | `reduce.py` |

The three patterns below cover the operational triad: **wait for
terminal** (done sentinel), **stream events** (JSONL tail), and
**watch phase progress** (status). Each is demonstrable against the
deterministic `--transport stub` fixture.

See also: `docs/swarm/runbook.md` for the broader operator runbook,
roadmap row R-128 / FR-027 (done sentinel), and milestone M7 exit
criteria (three monitoring patterns demonstrated).

---

## Pattern 1 — Wait for terminal via `done.json` sentinel

Use when the caller needs to **block until the job finishes** (success,
partial, failed, or killed) but does not need to stream intermediate
events. The sentinel is written atomically (tmp + `os.replace`) once
`SwarmState.state` flips to `terminal`, so a `[ -f done.json ]` test is
sufficient — there is no half-written window.

### Paste-ready commands (pattern 1)

```bash
# Variables a caller would set per job.
export OUT=/tmp/swarm-demo-1
export SPEC=/path/to/target.md

# Launch the job in the background (inline run, stub transport).
uv run superclaude swarm run \
    --lens bare-review \
    --transport stub \
    --target "$SPEC" \
    --output "$OUT" &
JOB_PID=$!

# Poll until done.json appears (~atomic terminal marker).
until [ -f "$OUT/done.json" ]; do sleep 1; done

# Inspect terminal status + contract path.
jq -r '"status=" + .terminal_status + " contract=" + .contract_path' \
    "$OUT/done.json"

# Reap the launcher (the executor already exited at terminal).
wait "$JOB_PID" || true
```

For **detached** runs (tmux-backed, survive caller exit) the same poll
pattern applies — replace `&` with `--detached` and the sentinel still
appears in the same `$OUT` directory.

### When this pattern fits (pattern 1)

- Bash scripts / Make targets that synchronously block on a swarm job.
- CI steps that need a single yes/no terminal signal.
- Any caller that wants to avoid parsing the streaming log.

---

## Pattern 2 — Live-tail the JSONL event stream

Use when the caller needs **per-event visibility** (worker started,
worker complete, normalize complete, wave transitions, errors). The
`execution-log.jsonl` surface is append-only and lock-coordinated; one
record per line means a streaming reader (`tail -F` + `jq`, or the
built-in `swarm logs --tail` shortcut) sees events in emission order.

### Paste-ready commands (pattern 2)

```bash
export OUT=/tmp/swarm-demo-2

# Launch the job in the background.
uv run superclaude swarm run \
    --lens bare-review \
    --transport stub \
    --target /path/to/target.md \
    --output "$OUT" &

# Built-in shortcut: --tail == --jsonl --follow. Exits at terminal.
uv run superclaude swarm logs --output "$OUT" --tail
```

To filter for a specific event type with `jq`, pipe the same stream:

```bash
# Surface only worker_complete events with their slot + elapsed_ms.
uv run superclaude swarm logs --output "$OUT" --tail \
    | jq -c 'select(.event_type == "worker_complete")
             | {slot: .slot_index, elapsed_ms}'
```

### When this pattern fits (pattern 2)

- Long-running jobs where progress visibility matters.
- Debugging unexpected normalize / reduce behavior.
- Streaming events into an external dashboard (one line == one event).

---

## Pattern 3 — Watch phase progress with `swarm status --watch`

Use when the caller wants the **coarse wave-level phase** refreshed on
an interval (preflight / dispatching / normalizing / reducing /
terminal) without parsing the per-event stream. The watch loop polls
`.swarm-state.json` at `--watch-interval` seconds and emits one
grep-friendly summary line per iteration; it exits when the phase
reaches `terminal` (or on Ctrl-C). The final exit code reflects the
IMM-5 terminal status (0 success, 1 partial/failed, 2 usage error).

### Paste-ready commands (pattern 3)

```bash
export OUT=/tmp/swarm-demo-3

# Launch the job in the background.
uv run superclaude swarm run \
    --lens bare-review \
    --transport stub \
    --target /path/to/target.md \
    --output "$OUT" &

# Watch phase transitions every 2 seconds; exits at terminal.
uv run superclaude swarm status --output "$OUT" --watch --watch-interval 2
```

One-shot check (no polling) for a CI gate:

```bash
# Exit code: 0 success / 1 partial-or-failed / 2 usage error.
uv run superclaude swarm status --output "$OUT"
```

### When this pattern fits (pattern 3)

- Operators who want a low-frequency, human-readable phase summary.
- CI gates that check final status without consuming the event stream.
- Quick `--job <id>` mismatch detection (wrong-directory invocation
  fails loudly via EXIT_USAGE).

---

## Pattern selection

| Need | Pattern | Reads |
|---|---|---|
| Block until done, single yes/no | 1 (sentinel poll) | `done.json` |
| Per-event visibility / dashboard | 2 (JSONL tail) | `execution-log.jsonl` |
| Coarse phase progress / CI gate | 3 (`status --watch`) | `.swarm-state.json` |

The three patterns are **composable**: a caller can run pattern 2 in
one shell to stream events while pattern 1 in another shell waits for
the sentinel — the four artifacts are independent and consistent
(NFR-004 three-layer durable monitoring; verified by
`tests/swarm/test_three_layer_artifacts.py`).

## References

- Roadmap row R-126 / FR-013 — three monitoring patterns documented.
- Roadmap row R-128 / FR-027 — `done.json` terminal sentinel.
- Roadmap row R-129 / NFR-004 — three-layer durable monitoring.
- Milestone M7 exit criteria — three monitoring patterns demonstrated.
- `docs/swarm/runbook.md` — operator runbook (UV mandate, T2 env
  contract, tmux-optional behavior).
- `src/superclaude/cli/swarm/commands.py` — `status_cmd`, `logs_cmd`,
  `run_cmd` implementations.
- `src/superclaude/cli/swarm/reduce.py` — `emit_done_sentinel`
  atomic-write implementation.
