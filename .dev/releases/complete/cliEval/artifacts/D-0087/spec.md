# D-0087 — E3 SessionStart Unmatched (session-init) Hook Coverage Eval (Body)

**Deliverable ID:** D-0087
**Task ID:** T05.07 (Phase 5)
**Roadmap items:** R-086 (E3 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E3 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E3 — the first of the
post-OQ-2 hook-event coverage entries (R-086 … R-098). E3 covers the
**first-position SessionStart hook** in `src/superclaude/hooks/hooks.json`
— a matcher-less entry whose command is `session-init.sh`. This is
distinct from the second SessionStart entry (matcher=`*`, command=
`freshness-session-start.sh`) which is covered by E4 / D-0088.

The body must:

- spawn a fresh claude session via the PTY harness so that both
  SessionStart hooks fire automatically before prompt-ready;
- assert the *first-position* hook's observable side-effects
  (state log present + session_init JSONL event recorded);
- exit cleanly so the `exit_code.equals(0)` assertion can pin a clean
  `/quit`;
- run with **no capability tags** — no MCP, no network, no shared state
  — so the body executes on every host regardless of MCP-server
  availability (D-0082 §6 capability-tag rollup row for E3).

## 2. Hook-surface contract (from `hooks.json` + OQ-2 D-0082 §4)

`src/superclaude/hooks/hooks.json` lines 4-15 (SessionStart block):

```jsonc
"SessionStart": [
  {
    "hooks": [
      { "type": "command",
        "command": "~/.claude/hooks/session-init.sh",
        "timeout": 10 }
    ]
  },
  {
    "matcher": "*",
    "hooks": [
      { "type": "command",
        "command": "~/.claude/hooks/freshness-session-start.sh",
        "timeout": 5 }
    ]
  }
]
```

Two SessionStart entries fire at session start:

1. **First-position** (no matcher) → `session-init.sh` → covered by **E3** (this).
2. **Second-position** (matcher=`*`) → `freshness-session-start.sh` → covered by **E4**.

The OQ-2 resolution (D-0082 §4 / decisions.md:543) freezes E3's body
shape to assert the first-position hook's side-effects:

| Observable | Purpose |
|---|---|
| `state/session-init.log` exists | proves `session-init.sh` ran (script writes its own log) |
| `logs/session-events.jsonl` contains `"type":"session_init"` | proves the session_init event was emitted to the SessionStart event ledger |
| Process exits cleanly on `/quit` | sanity-pin that the spawn lifecycle ran end-to-end |

These three observables are independently sufficient: (a) the file
existence pins that the hook **ran**; (b) the JSONL substring pins
that the hook **emitted its event**; (c) the exit code pins that the
session reached a clean shutdown. Each rules out a different failure
mode (hook didn't fire / hook fired but didn't emit / session crashed).

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E3 entry that previously
carried only scaffolding metadata (title, category, isolation, no_pty
tag). New body additions:

| Field | Value |
|---|---|
| **timeout_sec** | `60` (raised from defaults' 120s default — SessionStart hook flush is <2s on every observed host; 60s is generous) |
| **inputs[0].prompt** | `"/quit"` — minimal input that lets the PTY driver exit cleanly after the SessionStart hooks have fired |
| **expects[0]** | `file: { path: state/session-init.log, exists: true }` |
| **expects[1]** | `file: { path: logs/session-events.jsonl, exists: true, contains: '"type":"session_init"' }` |
| **expects[2]** | `exit_code: { equals: 0 }` |

Capability tags: `[]` (no `requires:` clause). The eval runs on every
host regardless of `--no-mcp` posture; it is **not** soft-skipped by
the FR-CAP1 gate.

PTY-exclusion tag: `no_pty: skip` (carried forward from the scaffolding
entry — every eval in the `real` suite is PTY-driven per DOC-OQ3 /
R-077).

## 4. Eval id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. The literal id `E3` is
trivially accepted — `eval describe --suite real --eval E3` returns
the full body and `eval list --json` enumerates it alongside E1 / E2.1
/ E2.2 / E2.3.

## 5. Determinism (3-run AC)

The body is deterministic on a clean per-eval HOME (D-0082 §2
constraint 2 / per-task AC):

- The PTY spawn writes a new session log on every invocation
  (FR-ISO2 fresh HOME per eval — no carry-over).
- The `session_init` JSONL event is emitted on every fresh
  SessionStart by the first-position hook contract.
- The `/quit` input causes an immediate clean exit (exit code 0).
- No time-of-day, network, or shared-state dependencies — D-0082 §2
  constraint 3 (no `CLAUDE_FAKE_TIME_OFFSET`) is honored.

Three consecutive `eval run --suite real --eval E3` invocations on a
clean HOME must therefore yield identical EvalOutcome statuses, which
is the per-task acceptance criterion.

## 6. Schema validation

The body uses only manifest-supported constructs:

- `inputs[].prompt: string` (additionalProperties: true under
  `evalEntry.inputs.items` per `suite.schema.json` line 139-142).
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved at
  load-time by `Expect.from_mapping` (`expect.py:640-669`). All three
  primitives used (`file`, `file`, `exit_code`) are in
  `PRIMITIVE_NAMES` (`expect.py:56-64`).
- `file` primitive kwargs `path`, `exists`, `contains` are supported by
  `Expect.file._build` (`expect.py:186-265`).
- `exit_code` primitive kwarg `equals` is supported by
  `Expect.exit_code._build` (`expect.py:484-551`).
- `timeout_sec: 60` is `integer ≥ 1` per schema line 137.
- `isolation.home_strategy: ephemeral` is in the enum at schema line 96.
- `no_pty: skip` matches the enum at schema line 154-156.

No schema-version bump required.

## 7. `--no-mcp` and `--no-pty` behavior matrix

| Invocation | E3 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E3` (no flags) | RUNS | no capability tags; PTY harness present on host |
| `eval run --suite real --eval E3 --no-mcp` | RUNS | no `requires:` → FR-CAP1 gate is a no-op for E3 |
| `eval run --suite real --eval E3 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077) |
| `eval run --suite real --eval E3 --no-mcp --no-pty` | SKIPPED (`--no-pty`) | `--no-pty` short-circuits first per `commands.py` |

## 8. Verification

Per phase-5-tasklist.md T05.07, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E3
```

**Today's runner state:** the same pre-existing `NameError: name
'_new_run_id' is not defined` in `cli/eval/commands.py:1418`
documented in T05.03 / T05.04 / T05.05 evidence blocks any direct
`eval run` invocation. That blocker is the responsibility of the
runner-completion task (Phase-5 dependency of the CP-P05-T01-T05
checkpoint at T05.06). T05.07 authors the manifest body; observable
verification is therefore via:

- (a) `eval describe --suite real --eval E3` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.07/describe-E3.txt`);
- (b) `eval list --json` enumerating E3 alongside E1 / E2.1-3 (proves
  schema acceptance; see `evidence/T05.07/list-with-E3.txt`);
- (c) `Expect.from_mapping` round-trip over each `expects[]` row
  (proves declarative DSL resolution; see
  `evidence/T05.07/expect-roundtrip.txt`).

Full end-to-end PTY execution + 3-run determinism proof rolls into
the runner-completion task downstream of T05.07.

### 8.1 Risk note — session-init.sh telemetry gap

`src/superclaude/scripts/session-init.sh` (current revision) prints
the SessionStart banner to **stdout** but does **not** write to
`$HOME/.claude/state/session-init.log` or
`$HOME/.claude/logs/session-events.jsonl`. The OQ-2 D-0082 §4 body
shape — which T05.07 lands verbatim — asserts both side-effects.

This gap is **not introduced** by T05.07; it predates the deliverable
and is the responsibility of a follow-up hook-script update task
that wires `session-init.sh` to emit the asserted observables.
Acceptance criteria for T05.07 (manifest body landed, FR-SCH2-valid
id, OQ-2 body shape recorded, spec/notes/evidence written) are met
by the describe / list / roundtrip evidence above; the per-task AC
that requires `eval run --eval E3` to exit 0 deterministically depends
transitively on (a) the runner NameError fix and (b) the
session-init.sh emit-observables update. See `notes.md` §"Hook
telemetry gap" for the full discovery + mitigation discussion.

## 9. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T05.01 / D-0082 | OQ-2 resolution — frozen body shape |
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts literal `E3` |
| Depends on | T04.02 / T04.03 (Expect.file impl) | satisfied by current `expect.py` |
| Depends on | T04.04 / T04.05 (Expect.exit_code impl) | satisfied by current `expect.py` |
| Sibling | T05.08 (E4 body) | covers second-position SessionStart hook |
| Unblocks | T05.12 (CP-P05-T07-T11 checkpoint) | E3 must enumerate + describe; full-run verification follows runner fix |

## 10. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟢 AUTHORED | Claude (Opus 4.7) | 2026-05-20 |
| 🟢 BODY FROZEN | per D-0082 §4 / decisions.md OQ-2 | 2026-05-20 |
