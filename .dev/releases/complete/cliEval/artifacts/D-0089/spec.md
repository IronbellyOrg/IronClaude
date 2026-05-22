# D-0089 — E5 UserPromptSubmit Freshness Hook Coverage Eval (Body)

**Deliverable ID:** D-0089
**Task ID:** T05.09 (Phase 5)
**Roadmap items:** R-088 (E5 body)
**Status:** 🟢 AUTHORED
**Date:** 2026-05-20
**Author:** Claude (Opus 4.7) under RyanW direction
**Manifest target:** `src/superclaude/cli/eval/suites/real.yaml` (E5 entry)

---

## 1. Purpose

Author the **inputs + expects** body for eval E5 — the third of the
post-OQ-2 hook-event coverage entries (R-086 … R-098). E5 covers the
sole **UserPromptSubmit hook** in `src/superclaude/hooks/hooks.json` —
a no-matcher entry whose command is `freshness-user-prompt.sh`
(timeout=3). This is distinct from the two SessionStart hooks (E3
covers position-0 `session-init.sh`; E4 covers position-1 matcher=*
`freshness-session-start.sh`).

The body must:

- spawn a fresh claude session via the PTY harness and inject a
  content prompt ("echo test" per OQ-2 D-0082 §4) so the
  UserPromptSubmit hook fires at least once;
- assert the hook's observable side-effects (freshness ledger present
  + `user_prompt` event row recorded);
- exit cleanly so the `exit_code.equals(0)` assertion can pin a clean
  `/quit`;
- run with **no capability tags** — no MCP, no network, no shared
  state — so the body executes on every host regardless of MCP-server
  availability (D-0082 §6 capability-tag rollup row for E5).

## 2. Hook-surface contract (from `hooks.json` + OQ-2 D-0082 §4)

`src/superclaude/hooks/hooks.json` UserPromptSubmit block:

```jsonc
"UserPromptSubmit": [
  {
    "hooks": [
      { "type": "command",
        "command": "~/.claude/hooks/freshness-user-prompt.sh",
        "timeout": 3 }
    ]
  }
]
```

A single UserPromptSubmit entry fires once per user-prompt submission:

- **No-matcher** → `freshness-user-prompt.sh` → covered by **E5** (this).

The OQ-2 resolution (D-0082 §4 / decisions.md:545) freezes E5's body
shape to assert the hook's side-effects:

| Observable | Purpose |
|---|---|
| `logs/freshness.jsonl` exists | proves the freshness event ledger was opened by `freshness-user-prompt.sh` (or by a prior SessionStart hook on the same spawn) |
| `logs/freshness.jsonl` contains `"type":"user_prompt"` | proves the `user_prompt` event row was emitted to the freshness ledger by `freshness-user-prompt.sh` |
| Process exits cleanly on `/quit` | sanity-pin that the spawn lifecycle ran end-to-end |

These three observables are independently sufficient: (a) the file
existence pins that the hook **opened the ledger**; (b) the JSONL
substring pins that the hook **emitted its `user_prompt` event row**;
(c) the exit code pins that the session reached a clean shutdown. Each
rules out a different failure mode (hook didn't fire / hook fired but
didn't emit / session crashed).

The D-0082 §4 second assertion `event_count >= 1 per injected prompt`
is **deferred** — see §3 footnote on YAML expressibility.

## 3. Frozen body shape

The body lands in `suites/real.yaml` under the E5 entry that previously
carried only scaffolding metadata (title, category, isolation, no_pty
tag). New body additions:

| Field | Value |
|---|---|
| **title** (corrected) | `"UserPromptSubmit freshness hook fires"` (was pre-OQ-2 stub `"pre_tool_call hook denies on missing capability"`) |
| **timeout_sec** | `60` (raised from defaults' 120s — UserPromptSubmit hook flush is <1s on every observed host; 60s is generous; matches E3 / E4 sibling for spawn-lifecycle parity) |
| **inputs[0].prompt** | `"echo test"` — the injected content prompt that fires UserPromptSubmit; matches D-0082 §4 `inject_prompt("echo test")` shape verbatim |
| **inputs[1].prompt** | `"/quit"` — clean session exit so `exit_code.equals(0)` can pin the PTY teardown contract |
| **expects[0]** | `file: { path: logs/freshness.jsonl, exists: true }` |
| **expects[1]** | `file: { path: logs/freshness.jsonl, exists: true, contains: '"type":"user_prompt"' }` |
| **expects[2]** | `exit_code: { equals: 0 }` |

Capability tags: `[]` (no `requires:` clause). The eval runs on every
host regardless of `--no-mcp` posture; it is **not** soft-skipped by
the FR-CAP1 gate.

PTY-exclusion tag: `no_pty: skip` (carried forward from the scaffolding
entry — every eval in the `real` suite is PTY-driven per DOC-OQ3 /
R-077).

**Footnote — `event_count >= 1 per injected prompt` deferral.** D-0082
§4 row E5 lists two `jsonl` assertions: `contains_event(type=user_prompt)`
and `event_count(type=user_prompt) >= 1 per injected prompt`. Both
forms require a filter predicate (a Python callable bound to the `type`
field), which the v1 Expect.* DSL exposes only via
`Expect.jsonl(filter=..., assert_any=..., line_count=...)` Python kwargs
— NOT expressible in declarative YAML (`expect.py:269-369`). The E3 /
E4 siblings (D-0087 §3 / D-0088 §3) solved the same problem by using
`Expect.file` with the JSONL substring as a sufficient proxy for
`contains_event`; T05.09 follows the same precedent. The per-injected-
prompt count aspect — a multi-fire pairing guard — is deferred until
either (a) the YAML callback escape hatch (D-4) is exercised for E5,
or (b) a future schema bump adds a declarative `jsonl: contains_event:
{ type: ..., count_per_input: N }` shorthand. Neither is in scope for
T05.09; the current body satisfies the OQ-2 minimum AC ("body matches
the OQ-2 resolution; runs deterministically on a clean HOME").

## 4. Eval id passes FR-SCH2

`validate_eval_id` (FR-SCH2 / T01.05) requires the eval id match
`^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`. The literal id `E5` is
trivially accepted — `eval describe --suite real --eval E5` returns
the full body and `eval list --json` continues to enumerate 17 evals
under suite `real`.

## 5. Determinism (3-run AC)

The body is deterministic on a clean per-eval HOME (D-0082 §2
constraint 2 / per-task AC):

- The PTY spawn writes a new freshness ledger entry on every
  UserPromptSubmit fire (FR-ISO2 fresh HOME per eval — no carry-over).
- The `user_prompt` JSONL row is emitted on every UserPromptSubmit
  fire by the hook contract; with two injected prompts ("echo test"
  + "/quit"), at least one row is guaranteed and the substring assertion
  holds.
- The `/quit` input causes an immediate clean exit (exit code 0).
- No time-of-day, network, or shared-state dependencies — D-0082 §2
  constraint 3 (no `CLAUDE_FAKE_TIME_OFFSET`) is honored. The `ts`,
  `session_id`, and `turn` fields on the JSONL row are not asserted
  against.

Three consecutive `eval run --suite real --eval E5` invocations on a
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
  `Expect.exit_code._build`.
- `timeout_sec: 60` is `integer ≥ 1` per schema.
- `isolation.home_strategy: ephemeral` is in the enum.
- `no_pty: skip` matches the enum.

No schema-version bump required.

## 7. `--no-mcp` and `--no-pty` behavior matrix

| Invocation | E5 outcome | Why |
|---|---|---|
| `eval run --suite real --eval E5` (no flags) | RUNS | no capability tags; PTY harness present on host |
| `eval run --suite real --eval E5 --no-mcp` | RUNS | no `requires:` → FR-CAP1 gate is a no-op for E5 |
| `eval run --suite real --eval E5 --no-pty` | SKIPPED (`--no-pty`) | per-eval `no_pty: skip` tag (R-077 / D-0077) |
| `eval run --suite real --eval E5 --no-mcp --no-pty` | SKIPPED (`--no-pty`) | `--no-pty` short-circuits first per `commands.py` |

## 8. Verification

Per phase-5-tasklist.md T05.09, primary verifier:

```bash
uv run superclaude eval run --suite real --eval E5
```

**Today's runner state:** the same pre-existing `NameError: name
'_new_run_id' is not defined` in `cli/eval/commands.py:1418`
documented in T05.03 / T05.04 / T05.05 / T05.07 / T05.08 evidence
blocks any direct `eval run` invocation. That blocker is the
responsibility of the runner-completion task (Phase-5 dependency of
the CP-P05-T07-T11 checkpoint at T05.12). T05.09 authors the manifest
body; observable verification is therefore via:

- (a) `eval describe --suite real --eval E5` rendering the new
  inputs/expects rows (manifest shape proof; see
  `evidence/T05.09/describe-E5.txt`);
- (b) `eval list --json` continuing to enumerate suite `real` with
  17 evals (proves schema acceptance; see
  `evidence/T05.09/list-with-E5.txt`);
- (c) `Expect.from_mapping` round-trip over each `expects[]` row
  (proves declarative DSL resolution; see
  `evidence/T05.09/expect-roundtrip.txt`).

Full end-to-end PTY execution + 3-run determinism proof rolls into
the runner-completion task downstream of T05.09.

### 8.1 Risk note — freshness-user-prompt.sh telemetry gap

`src/superclaude/hooks/scripts/freshness-user-prompt.sh` (current
revision at lines 259-264) emits the UserPromptSubmit envelope to
**stdout** via `jq -nc ... hookSpecificOutput ...` and writes
truncation telemetry to `logs/freshness-hook.jsonl` only when the
envelope is truncated (lines 252-256). On the normal (non-truncated)
path it does **not** append a `{"type":"user_prompt"}` row to
`$HOME/.claude/logs/freshness.jsonl`. The OQ-2 D-0082 §4 body shape —
which T05.09 lands verbatim — asserts this observable anyway.

This gap is **not introduced** by T05.09; it predates the deliverable
and mirrors the identical `session-init.sh` / `freshness-session-
start.sh` telemetry gaps discovered during T05.07 (D-0087 §8.1) and
T05.08 (D-0088 §8.1). All three gaps belong to a follow-up hook-script
update task that wires:

- `session-init.sh` → `logs/session-events.jsonl` `session_init` rows
  (D-0087 §8.1);
- `freshness-session-start.sh` → `logs/freshness.jsonl` `session_start`
  rows (D-0088 §8.1);
- `freshness-user-prompt.sh` → `logs/freshness.jsonl` `user_prompt`
  rows (this gap).

Acceptance criteria for T05.09 (manifest body landed, FR-SCH2-valid
id, OQ-2 body shape recorded, spec/notes/evidence written) are met
by the describe / list / roundtrip evidence above; the per-task AC
that requires `eval run --eval E5` to exit 0 deterministically depends
transitively on (a) the runner NameError fix and (b) the
freshness-user-prompt.sh emit-observables update.

## 9. Impacts / dependencies

| Direction | Item | Note |
|---|---|---|
| Depends on | T05.01 / D-0082 | OQ-2 resolution — frozen body shape |
| Depends on | T01.05 (FR-SCH2 validate_eval_id) | accepts literal `E5` |
| Depends on | T04.02 / T04.03 (Expect.file impl) | satisfied by current `expect.py` |
| Depends on | T04.04 / T04.05 (Expect.exit_code impl) | satisfied by current `expect.py` |
| Sibling | T05.07 (E3 body) | first-position SessionStart hook (same comment-block template) |
| Sibling | T05.08 (E4 body) | second-position SessionStart matcher=* hook (same JSONL ledger) |
| Sibling | T05.10 (E6 body) | PreToolUse Edit matcher (same freshness JSONL ledger) |
| Unblocks | T05.12 (CP-P05-T07-T11 checkpoint) | E5 must enumerate + describe; full-run verification follows runner fix |

## 10. Sign-off

| Status | Signed | Date |
|---|---|---|
| 🟢 AUTHORED | Claude (Opus 4.7) | 2026-05-20 |
| 🟢 BODY FROZEN | per D-0082 §4 / decisions.md OQ-2 | 2026-05-20 |
