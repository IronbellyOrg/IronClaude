# Swarm Observability Procedure (OPS-003 / R-152)

> 📚 Part of the [swarm documentation](./README.md). New here? Start with the
> [User Guide](./user-guide.md). For the three **wait-on-a-job** patterns
> (done-sentinel poll / JSONL tail / `status --watch`), see
> [Monitoring Patterns](./monitoring-patterns.md) — this procedure does **not**
> duplicate them; it documents the underlying artifact layers and how to use
> each one to **diagnose** a run.

This document is the durable-observability procedure for the MultiModelSwarm
orchestrator. It is a superset of [`monitoring-patterns.md`](./monitoring-patterns.md):
where that doc answers *"how do I wait for a job to finish?"*, this doc answers
*"what does each observability artifact contain, and how do I read it to debug a
run that misbehaved?"*

The parent spec mandates **three-layer durable observability**
(`merged-requirements.compressed.md:465`): the state file, the append-only JSONL
event stream, and the human-readable Markdown log. These **three** are
**caller-agnostic**: they are written under the job's `--output` directory
regardless of whether the run was driven by a skill, a human operator, or a CI
subprocess, so the same procedure applies everywhere.

A fourth artifact — the terminal **done sentinel** (`done.json`) — is **not**
universal: it is emitted only on the paths that wire the on-completion sentinel
step (the detached/resume completion path) and by `swarm kill` (which writes a
`terminal_status=killed` sentinel). **A default inline `swarm run` does NOT emit
`done.json`** (`reduce_wave3` does not write it; verified by
`tests/swarm/test_e2e_user_guide.py::test_quickstart_does_not_emit_done_sentinel`).
For an inline run, treat an **absent `done.json` as expected, never as a failure
symptom**: the canonical completion signal is `.swarm-state.json` reaching
`terminal` **AND** `return-contract.yaml` being present — not `done.json`.

OPS-003 / R-152 (`phase-9-tasklist.md:78-111`) requires this doc to map each
artifact to a debugging workflow and to cover the common failure modes
(env-missing, timeout, parse-error).

---

## The artifact layers

Every artifact filename below is a constant in
`src/superclaude/cli/swarm/commands.py`; the procedure cites only artifacts the
swarm CLI actually emits.

| Layer | Filename | Constant (`commands.py`) | What it holds |
|---|---|---|---|
| State file | `.swarm-state.json` | `SWARM_STATE_FILENAME` | Coarse wave-level phase (DM-014), atomically rewritten on each transition. |
| Structured log | `execution-log.jsonl` | `EXECUTION_LOG_JSONL_FILENAME` | Append-only, lock-coordinated event stream (DM-015), one JSON record per line. |
| Human log | `execution-log.md` | `EXECUTION_LOG_MD_FILENAME` | Human-readable Markdown mirror of the JSONL stream. |
| Done sentinel | `done.json` | `DONE_SENTINEL_FILENAME` | Atomic terminal marker (DM-017): `terminal_status` + `contract_path`. **Emitted only on the detached/resume completion path and by `swarm kill`; absent after a default inline `swarm run`.** |

Two supporting artifacts complete the run's on-disk record and are referenced by
the recipes below:

| Supporting | Filename | Source | What it holds |
|---|---|---|---|
| Result contract | `return-contract.yaml` | `RESULT_CONTRACT_FILENAME` (`commands.py`) | The final caller-facing contract; present only once state reaches `terminal`. |
| Manifest | `manifest.json` | written by `preflight.py` (string literal, not a `*_FILENAME` constant) | Preflight-resolved job spec (INV-001 / INV-016); the run is recoverable from it alone. |

### Layer 1 — `.swarm-state.json` (coarse phase)

The state file records exactly one of five wave-level phases in its `state`
field (the `SwarmStateValue` enum, `models.py:71-77`):

```text
preflight_ok → dispatching → normalizing → reducing → terminal
```

It is rewritten **atomically** on every transition (tmp + `os.replace`), so a
`[ -f .swarm-state.json ]` read never sees a half-written record. The
`swarm status` command reads this file; `swarm status --watch` polls it and
exits when `state == "terminal"`. Where the file is *stuck* tells you which wave
a hung job died in.

### Layer 2 — `execution-log.jsonl` (structured event stream)

Append-only, lock-coordinated, one JSON record per line. Each record carries an
`event_type` drawn from the `EventType` enum (`models.py:78-84`):

```text
worker_start | worker_progress | worker_done | wave_transition | terminal
```

Because every event is its own line, `jq`-filtering and `tail -F` streaming both
work without parsing partial records. This is the layer for **per-worker
forensics**: which slot started, which finished, which errored, and in what
order.

### Layer 3 — `execution-log.md` (human-readable mirror)

A Markdown rendering of the same event stream, one bullet per event in the shape
`- [<timestamp>] <event_type> worker=<index|->: <payload_summary>`
(`logging_.py:167,186`). Use it for a fast eyeball pass when you do not want to
pipe JSONL through `jq` — it is the default surface `swarm logs` dumps (JSONL is
opt-in via `--jsonl`).

### Layer 4 — `done.json` (terminal sentinel) — run-mode-dependent

When emitted, it is written atomically once the run reaches a terminal state and
carries `terminal_status` (e.g. `success`, `partial`, `failed`, or `killed`) and
`contract_path` (empty for killed jobs, since an interrupted executor never
emitted a `return-contract.yaml`).

**Crucially, `done.json` is NOT a universal "job finished" signal.** It is
emitted **only** on the paths that wire the on-completion sentinel step — the
**detached/resume completion path** — and by `swarm kill` (which writes a
`terminal_status=killed` sentinel). The **default inline `swarm run` does NOT
emit it** (`reduce_wave3` does not write it; the on-completion step is not wired
on the inline path —
`tests/swarm/test_e2e_user_guide.py::test_quickstart_does_not_emit_done_sentinel`).

Therefore: **only use `[ -f done.json ]` as a completion signal for detached /
resumed / killed jobs.** For an inline run, an absent `done.json` is expected and
is **not** a failure symptom — the completion signal is `.swarm-state.json`
reaching `terminal` **AND** `return-contract.yaml` being present (its
`status` field carries the verdict that `done.json.terminal_status` would carry).

---

## Debugging recipes

Each recipe starts from a symptom and walks down the layers. Set `OUT` to the
job's `--output` directory first:

```bash
export OUT=/path/to/job/output
```

### Recipe 0 — Triage: which layer first?

First, know your run mode — it changes the completion signal:

- **Inline run** (default `swarm run`, no `--resume`): completion = state file at
  `terminal` **AND** `return-contract.yaml` present. **`done.json` is expected to
  be ABSENT — its absence is NOT a failure.**
- **Detached / resumed / killed job**: completion = `done.json` present (with
  `terminal_status`).

```bash
# Snapshot the layers. For an inline run, done.json is expected to be absent.
ls -la "$OUT"/.swarm-state.json "$OUT"/execution-log.jsonl \
       "$OUT"/execution-log.md "$OUT"/return-contract.yaml "$OUT"/done.json 2>&1
jq -r '.state' "$OUT/.swarm-state.json" 2>/dev/null   # coarse phase
# Inline-run verdict: state==terminal + contract present → read the contract.
[ -f "$OUT/return-contract.yaml" ] && grep -E '^status:' "$OUT/return-contract.yaml"
# Detached/resume/kill verdict only: done.json carries terminal_status.
[ -f "$OUT/done.json" ] && jq -r .terminal_status "$OUT/done.json"
```

- **No artifacts at all** → the run never got past launch; jump to Recipe 1
  (env-missing).
- **State stuck at `dispatching`/`normalizing` (not `terminal`) and no
  `return-contract.yaml`** → the run hung mid-wave; Recipe 2 (timeout) or
  Recipe 3 (parse-error). (Do **not** infer a hang from a missing `done.json` on
  an inline run — that file is expected to be absent there.)
- **State `terminal` + `return-contract.yaml` present, `status != success`** (or,
  for detached/killed jobs, `done.json.terminal_status != success`) → it finished
  but degraded; Recipe 4 reads the per-worker stream to find which slots failed.

### Recipe 1 — env-missing (run never started)

A missing T2 proxy env contract is rejected at preflight (INV-007), so the run
fails **before** writing the streaming artifacts. Diagnose from the absence
pattern + the preflight artifact:

```bash
# Symptom: no execution-log.* and no return-contract.yaml; manifest may also be
# absent. (done.json is absent here, but it is also absent on a healthy inline
# run, so its absence is not by itself an env-missing signal.)
ls "$OUT" 2>&1
# If a manifest exists, it captures the preflight-resolved spec; if it is
# missing too, preflight aborted before resolution (the env-missing signature).
[ -f "$OUT/manifest.json" ] && jq -r '.job_id' "$OUT/manifest.json"
```

The fix is environment, not code: see
[`env-readiness.md`](./env-readiness.md) (OPS-002) and the INV-007 env-missing
failure contract. The state file will not reach `preflight_ok` for an
env-missing run.

### Recipe 2 — timeout (a worker hung)

A worker that exceeds its deadline surfaces as a `worker_done` record whose
status is `timeout` (the `WorkerStatus` enum admits
`success | timeout | parse_error | proxy_error`, `models.py:69`). Isolate the
slow slot from the structured stream:

```bash
# Which slots timed out, and in what order did workers report?
jq -c 'select(.event_type=="worker_done")
       | {worker_index, status}' "$OUT/execution-log.jsonl"

# Cross-check the coarse phase: a job stuck at "dispatching" with some
# worker_start events but missing worker_done events is mid-flight / hung.
jq -r '.state' "$OUT/.swarm-state.json"
grep -c worker_start "$OUT/execution-log.md"
grep -c worker_done  "$OUT/execution-log.md"
```

A `worker_start` count exceeding the `worker_done` count, with the state file
parked at `dispatching`, is the live-hang signature. To wait for or stop such a
job, use the patterns in [`monitoring-patterns.md`](./monitoring-patterns.md)
(`status --watch` to observe; `swarm kill` to terminate — kill writes a
`done.json` with `terminal_status=killed`).

### Recipe 3 — parse-error (worker returned, output unusable)

A worker whose output failed normalization surfaces as `worker_done` with status
`parse_error`. The job can still reach `terminal` with a `partial` or `failed`
verdict, so read both the stream and the verdict:

```bash
# Find the parse-error slots.
jq -c 'select(.event_type=="worker_done" and .status=="parse_error")
       | {worker_index, status}' "$OUT/execution-log.jsonl"

# Confirm the run wrapped up and read the downgraded verdict.
# Inline run: the verdict is the contract's status field.
[ -f "$OUT/return-contract.yaml" ] && grep -E '^status:' "$OUT/return-contract.yaml"
# Detached/resume/kill: the verdict is done.json.terminal_status.
[ -f "$OUT/done.json" ] && jq -r '.terminal_status' "$OUT/done.json"
```

If normalization is the suspect step, trace the `wave_transition` events to see
whether the job entered `normalizing` and what it produced; the human log is the
quickest read:

```bash
grep -E 'wave_transition|worker_done' "$OUT/execution-log.md"
```

### Recipe 4 — degraded terminal (partial/failed verdict)

When the verdict is `partial` or `failed`, the structured stream tells you
*which* workers dragged it down, and the result contract carries the
caller-facing detail. Read the verdict from the contract on an inline run, or
from `done.json` on a detached/resumed/killed job:

```bash
# Inline run: the contract is the verdict surface (status + per-worker detail).
[ -f "$OUT/return-contract.yaml" ] && grep -E '^status:' "$OUT/return-contract.yaml"
# Detached/resume/kill: done.json carries terminal_status + contract_path.
[ -f "$OUT/done.json" ] && \
  jq -r '.terminal_status + " contract=" + .contract_path' "$OUT/done.json"

# Per-worker outcome tally.
jq -r 'select(.event_type=="worker_done") | .status' \
   "$OUT/execution-log.jsonl" | sort | uniq -c

# The final contract (present once state == terminal).
cat "$OUT/return-contract.yaml"
```

### Recipe 5 — corrupt or missing state file

`swarm status` / `swarm logs --follow` tolerate a missing or unreadable
`.swarm-state.json` (a job may have crashed before writing it). When the state
file is corrupt, the JSONL/Markdown logs are usually still intact and are the
authoritative post-mortem surface — fall back to Layer 2/3 and read the event
stream directly rather than trusting the coarse phase.

---

## Layer → use-case map

| Question | Layer | Read |
|---|---|---|
| Did an **inline** run finish, and how? | State file + contract | `.swarm-state.json` (`state==terminal`) + `return-contract.yaml` (`status`) |
| Did a **detached/resumed/killed** job finish? | Done sentinel | `done.json` (`terminal_status`) — absent on inline runs |
| Which coarse wave is it in / did it die in? | State file | `.swarm-state.json` (`state`) |
| Which worker failed, and why? | Structured log | `execution-log.jsonl` (`event_type`, `status`) |
| Quick human eyeball of the run | Human log | `execution-log.md` |
| Final caller-facing verdict + detail | Result contract | `return-contract.yaml` |
| Preflight-resolved job spec (recovery) | Manifest | `manifest.json` |

For **waiting** on a job rather than diagnosing one — fire-and-wait on the
sentinel, live-tail the JSONL, or watch the coarse phase — use the three
patterns in [`monitoring-patterns.md`](./monitoring-patterns.md). This procedure
deliberately does not restate them.

---

## References

- `phase-9-tasklist.md:78-111` — OPS-003 / R-152 / T09.03 deliverable + ACs
  (state file / JSONL log / Markdown log / done sentinel + debugging recipes).
- `merged-requirements.compressed.md:465` — parent spec "three-layer durable
  observability" (the source of the state-file / JSONL / Markdown-log layering).
- [`monitoring-patterns.md`](./monitoring-patterns.md) — the three
  wait-on-a-job patterns (done-sentinel poll / JSONL tail / `status --watch`);
  cross-referenced, not duplicated here.
- [`env-readiness.md`](./env-readiness.md) — OPS-002 env checklist + INV-007
  env-missing contract (Recipe 1).
- `src/superclaude/cli/swarm/commands.py` — `SWARM_STATE_FILENAME`,
  `EXECUTION_LOG_JSONL_FILENAME`, `EXECUTION_LOG_MD_FILENAME`,
  `DONE_SENTINEL_FILENAME`, `RESULT_CONTRACT_FILENAME` constants; `status_cmd`,
  `logs_cmd`, `kill` implementations.
- `src/superclaude/cli/swarm/models.py` — `SwarmStateValue`, `EventType`,
  `WorkerStatus` enums.
- `src/superclaude/cli/swarm/logging_.py` — Markdown-log line shape.
