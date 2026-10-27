# D-0088 — E4 SessionStart matcher=* Freshness Hook Coverage Eval (Body)

**Deliverable ID:** D-0088
**Task ID:** T05.08 (Phase 5)
**Roadmap items:** R-087 (E4 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E4 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E4 — the second of the
post-OQ-2 hook-event coverage entries (R-086 … R-098). E4 covers the
**second-position SessionStart hook** in `src/superclaude/hooks/hooks.json`
— a `matcher: "*"` entry whose command is `freshness-session-start.sh`.
This is distinct from the first-position SessionStart entry (no
matcher, `session-init.sh`) which is covered by E3 / D-0087.

The body must:

- spawn a fresh claude session via the PTY harness so that both
  SessionStart hooks fire automatically before prompt-ready (the same
  spawn that triggers E3's position-0 hook also triggers E4's
  position-1 hook);
- assert the *second-position* hook's observable side-effects
  (freshness ledger present + `session_start` event row recorded);
- exit cleanly so the `exit_code.equals(0)` assertion can pin a clean
  `/quit`;
- run with **no capability tags** — no MCP, no network, no shared
  state — so the body executes on every host regardless of MCP-server
  availability (D-0082 §6 capability-tag rollup row for E4).

## 2. Hook-surface contract (from `hooks.json` + OQ-2 D-0082 §4)

`src/superclaude/hooks/hooks.json` SessionStart block (paraphrased
from D-0087 §2 for symmetry):

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

1. **First-position** (no matcher) → `session-init.sh` → covered by **E3** (D-0087).
2. **Second-position** (matcher=`*`) → `freshness-session-start.sh` → covered by **E4** (this).

The OQ-2 resolution (D-0082 §4 / decisions.md:544) freezes E4's body
shape to assert the second-position hook's side-effects:

| Observable | Purpose |
|---|---|
| `logs/freshness.jsonl` exists | proves the freshness event ledger was opened by the matcher=* hook |
| `logs/freshness.jsonl` contains `"type":"session_start"` | proves the `session_start` event row was emitted to the freshness ledger by `freshness-session-start.sh` |
| Process exits cleanly on `/quit` | sanity-pin that the spawn lifecycle ran end-to-end |

These three observables are independently sufficient: (a) the file
existence pins that the hook **opened the ledger**; (b) the JSONL
substring pins that the hook **emitted its `session_start` event row**;
(c) the exit code pins that the session reached a clean shutdown. Each
rules out a different failure mode (hook didn't fire / hook fired but
didn't emit / session crashed).

The D-0082 §4 second assertion `jsonl.event_count(...) == 1` is
**deferred** — see §3 footnote on YAML expressibility.

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E4 entry that previously
carried only scaffolding metadata (title, category, isolation, no_pty
tag). New body additions:

| Field | Value |
|---|---|
| **title** (corrected) | `"SessionStart matcher=* freshness hook fires"` (was pre-OQ-2 stub `"session_start hook deploys settings.json into ephemeral HOME"`) |
| **timeout_sec** | `60` (raised from defaults' 120s default — SessionStart hook flush is <2s on every observed host; 60s is generous; matches E3 sibling for spawn-lifecycle parity) |
| **inputs[0].prompt** | `"/quit"` — minimal input that lets the PTY driver exit cleanly after the SessionStart hooks have fired |
| **expects[0]** | `file: { path: logs/freshness.jsonl, exists: true }` |
| **expects[1]** | `file: { path: logs/freshness.jsonl, exists: true, contains: '"type":"session_start"' }` |
| **expects[2]** | `exit_code: { equals: 0 }` |

Capability tags: `[]` (no `requires:` clause). The eval runs on every
host regardless of `--no-mcp` posture; it is **not** soft-skipped by
the FR-CAP1 gate.

PTY-exclusion tag: `no_pty: skip` (carried forward from the scaffolding
entry — every eval in the `real` suite is PTY-driven per DOC-OQ3 /
R-077).

**Footnote — `event_count == 1` deferral.** D-0082 §4 lists two
`jsonl` assertions for E4: `contains_event(type=session_start)` and
`event_count(type=session_start) == 1`. Both forms require a filter
predicate (a Python callable bound to the `type` field), which the
v1 Expect.* DSL exposes only via `Expect.jsonl(filter=...,
assert_any=..., line_count=...)` Python kwargs — NOT expressible in
declarative YAML (`expect.py:269-369`). The E3 sibling (D-0087 §3)
solved the same problem by using `Expect.file` with the JSONL
substring as a sufficient proxy for `contains_event`; T05.08 follows
the same precedent. The `event_count == 1` aspect — a duplicate-fire
guard — is deferred until either (a) the YAML callback escape hatch
(D-4) is exercised for E4, or (b) a future schema bump adds a
declarative `jsonl: contains_event: { type: ... }` shorthand. Neither
is in scope for T05.08; the current body satisfies the OQ-2 minimum AC
("body matches the OQ-2 resolution; runs deterministically on a clean
HOME").

## 4. Eval id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. The literal id `E4` is
trivially accepted — `eval describe --suite real --eval E4` returns
the full body and `eval list --json` continues to enumerate 17 evals
under suite `real`.

## 5. Determinism (3-run AC)

The body is deterministic on a clean per-eval HOME (D-0082 §2
constraint 2 / per-task AC):

- The PTY spawn writes a new freshness ledger entry on every
  invocation (FR-ISO2 fresh HOME per eval — no carry-over).
- The `session_start` JSONL row is emitted on every fresh
  SessionStart by the second-position (matcher=*) hook contract.
- The `/quit` input causes an immediate clean exit (exit code 0).
- No time-of-day, network, or shared-state dependencies — D-0082 §2
  constraint 3 (no `CLAUDE_FAKE_TIME_OFFSET`) is honored. The `ts`
  field in the JSONL row is not asserted against.

Three consecutive `eval run --suite real --eval E4` invocations on a
clean HOME must therefore yield identical EvalOutcome statuses, which
is the per-task acceptance criterion.

## 6. Schema validation

The body uses only manifest-supported constructs:

- `inputs[].prompt: string` (additionalProperties: true under
  `evalEntry.inputs.items` per `suite.schema.json`).
- `expects[]` rows matching `{primitive: kwargs}` shape — resolved at
  load-time by `Expect.from_mapping` (`expect.py:640-669`). All three
  primitives used (`file`, `file`, `exit_code`) are in
  `PRIMITIVE_NAMES` (`expect.py:56-64`).
- `file` primitive kwargs `path`, `exists`, `contains` are supported by
  `Expect.file._build` (`expect.py:186-265`).
- `exit_code` primitive kwarg `equals` is supported by
  `Expect.exit_code._build` (`expect.py`).
- `timeout_sec: 60` is `integer ≥ 1` per schema.
- `isolation.home_strategy: ephemeral` is in the enum.
- `no_pty: skip` matches the enum.

No schema-version bump required.

## 7. `--no-mcp` and `--no-pty` behavior matrix

| Invocation | E4 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E4` (no flags) | RUNS | no capability tags; PTY harness present on host |
| `eval run --suite real --eval E4 --no-mcp` | RUNS | no `requires:` → FR-CAP1 gate is a no-op for E4 |
| `eval run --suite real --eval E4 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077) |
| `eval run --suite real --eval E4 --no-mcp --no-pty` | SKIPPED (`--no-pty`) | `--no-pty` short-circuits first per `commands.py` |

## 8. Verification

Per phase-5-tasklist.md T05.08, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E4
```

**Today's runner state:** the same pre-existing `NameError: name
'_new_run_id' is not defined` in `cli/eval/commands.py:1418`
documented in T05.07 evidence (and T05.03 / T05.04 / T05.05) blocks
any direct `eval run` invocation. That blocker is the responsibility
of the runner-completion task (Phase-5 dependency of the
CP-P05-T07-T11 checkpoint at T05.12). T05.08 authors the manifest
body; observable verification is therefore via:

- (a) `eval describe --suite real --eval E4` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.08/describe-E4.txt`);
- (b) `eval list --json` continuing to enumerate suite `real` with
  17 evals (proves schema acceptance; see
  `evidence/T05.08/list-with-E4.txt`);
- (c) `Expect.from_mapping` round-trip over each `expects[]` row
  (proves declarative DSL resolution; see
  `evidence/T05.08/expect-roundtrip.txt`).

Full end-to-end PTY execution + 3-run determinism proof rolls into
the runner-completion task downstream of T05.08.

### 8.1 Risk note — freshness-session-start.sh telemetry gap

`src/superclaude/hooks/scripts/freshness-session-start.sh` (current
revision) emits the SessionStart envelope to **stdout** via
`jq -nc ... hookSpecificOutput ...` (line 115-120) and creates state
files under `$HOME/.claude/state/`, but does **not** currently append
a `{"type":"session_start"}` row to `$HOME/.claude/logs/freshness.jsonl`.
The OQ-2 D-0082 §4 body shape — which T05.08 lands verbatim — asserts
both side-effects (file present + JSONL substring).

This gap is **not introduced** by T05.08; it predates the deliverable
and mirrors the identical `session-init.sh` telemetry gap discovered
during T05.07 (D-0087 §8.1). Both gaps belong to a follow-up
hook-script update task that wires `session-init.sh` to emit the
`session-init.log` + `session-events.jsonl` observables AND wires
`freshness-session-start.sh` to emit `logs/freshness.jsonl`
`session_start` rows. Acceptance criteria for T05.08 (manifest body
landed, FR-SCH2-valid id, OQ-2 body shape recorded, spec/notes/
evidence written) are met by the describe / list / roundtrip
evidence above; the per-task AC that requires `eval run --eval E4`
to exit 0 deterministically depends transitively on (a) the runner
NameError fix and (b) the freshness-session-start.sh emit-observables
update.

## 9. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T05.01 / D-0082 | OQ-2 resolution — frozen body shape |
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts literal `E4` |
| Depends on | T04.02 / T04.03 (Expect.file impl) | satisfied by current `expect.py` |
| Depends on | T04.04 / T04.05 (Expect.exit_code impl) | satisfied by current `expect.py` |
| Sibling | T05.07 (E3 body) | covers first-position SessionStart hook |
| Sibling | T05.09 (E5 body) | covers UserPromptSubmit freshness hook (same matcher ledger) |
| Unblocks | T05.12 (CP-P05-T07-T11 checkpoint) | E4 must enumerate + describe; full-run verification follows runner fix |

## 10. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟢 AUTHORED | Claude (Opus 4.7) | 2026-05-20 |
| 🟢 BODY FROZEN | per D-0082 §4 / decisions.md OQ-2 | 2026-05-20 |
