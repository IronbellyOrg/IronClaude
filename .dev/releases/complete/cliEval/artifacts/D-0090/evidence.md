# D-0090 — Cross-references / evidence

## Source files inspected

| File | Lines | Purpose |
|---|---|---|
| `src/superclaude/cli/eval/suites/real.yaml` | 369-462 (post-edit) | E6 manifest entry |
| `src/superclaude/cli/eval/suites/suite.schema.json` | 124-160 | Eval entry schema (inputs/expects open-shape, no_pty enum, isolation enum) |
| `src/superclaude/cli/eval/expect.py` | 56-64 (PRIMITIVE_NAMES), 79-91 (_resolve_path), 144 (_named_callable), 186-265 (Expect.file), 269-369 (Expect.jsonl — for the YAML-expressibility analysis), 484-551 (Expect.exit_code), 640-669 (Expect.from_mapping) | Primitive surface for the five assertions in this body + the deferred `event_count` analysis |
| `src/superclaude/hooks/hooks.json` | PreToolUse block (single matcher group `Edit\|Write\|mcp__serena__*`, command=freshness-pre-edit.sh, timeout=5) | Single PreToolUse matcher block fanning out across three coverage evals (E6/E7/E8) |
| `src/superclaude/hooks/scripts/freshness-pre-edit.sh` | 78-87 (no_prior_read create_allowed branch), 108-119 (JSONL emit to logs/freshness-hook.jsonl with event/tool field names) | Current revision of the PreToolUse hook script — emits to `freshness-hook.jsonl` with `event`/`tool` fields; **does not** yet write `logs/freshness.jsonl` with `type`/`matcher` fields on the normal path (see spec §8.1 + notes §"Hook telemetry gap") |
| `.dev/releases/current/cliEval/decisions.md` | OQ-2 block (lines 530-583, esp. E6 row) | OQ-2 resolution status + E6 frozen row |
| `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` | §3 (hook-surface map), §4 (E6 body shape), §6 (capability rollup), §7 (impacts row T05.10 → E6 → R-089) | Frozen body shape source of truth |
| `.dev/releases/current/cliEval/artifacts/D-0087/spec.md` | full | Sibling deliverable (E3 body, first-position SessionStart) — same telemetry-gap posture |
| `.dev/releases/current/cliEval/artifacts/D-0088/spec.md` | full | Sibling deliverable (E4 body, second-position SessionStart matcher=*) — same JSONL ledger target |
| `.dev/releases/current/cliEval/artifacts/D-0089/spec.md` | full | Sibling deliverable (E5 body, UserPromptSubmit no-matcher) — same JSONL ledger target |
| `.dev/releases/current/cliEval/artifacts/D-0089/notes.md` | full | Sibling design notes — substring-proxy / event_count-deferral / content-prompt-rationale carried forward |
| `.dev/releases/current/cliEval/phase-5-tasklist.md` | T05.10 block (lines 450-498) | Source task spec |

## Manifest delta

Pre-edit (scaffolding):

```yaml
- id: E6
  title: "PreToolUse Edit matcher fires"
  category: hook-lifecycle
  isolation:
    home_strategy: ephemeral
  no_pty: skip
```

Notable pre-edit issues addressed by T05.10:

1. **No `timeout_sec`** — relied on suite default (120s). T05.10 pins
   `timeout_sec: 60` per spec §"Why timeout_sec: 60" and sibling
   parity with E3 / E4 / E5.
2. **No `inputs` / `expects`** — scaffolding only. T05.10 lands the
   OQ-2 body shape verbatim, including the three-input shape (Write
   seed + Edit fire + /quit) that distinguishes E6 from the simpler
   E3/E4/E5 siblings.

Post-edit (`real.yaml:369-462`):

```yaml
- id: E6
  title: "PreToolUse Edit matcher fires"
  category: hook-lifecycle
  timeout_sec: 60
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # T05.10 / D-0090 — body shape per OQ-2 resolution (D-0082 §4).
  # E6 exercises the Edit branch of the PreToolUse matcher group
  # [...] [verbose comment block — see real.yaml:376-441 for full text]
  inputs:
    - prompt: "Use the Write tool to create a file named edited.txt under the current working directory with the single line 'before'."
    - prompt: "Use the Edit tool on edited.txt to replace 'before' with 'edited'."
    - prompt: "/quit"
  expects:
    - file:
        path: logs/freshness.jsonl
        exists: true
    - file:
        path: logs/freshness.jsonl
        exists: true
        contains: '"type":"pre_edit"'
    - file:
        path: logs/freshness.jsonl
        exists: true
        contains: '"matcher":"Edit"'
    - file:
        path: edited.txt
        exists: true
    - exit_code:
        equals: 0
```

## Verification runs

Captured under `.dev/releases/current/cliEval/evidence/T05.10/`:

| File | Command | Outcome |
|---|---|---|
| `describe-E6.txt` | `uv run superclaude eval describe --suite real --eval E6` | exit 0; renders the new inputs/expects rows verbatim; proves manifest body is loadable and round-trips through the manifest loader. |
| `list-with-E6.txt` | `uv run superclaude eval list --json` | exit 0; reports `eval_count: 17` for the `real` suite (1 + 3 + 13 = 17 entries: E1 + E2.{1,2,3} + E3..E15) — confirms E6 enumerates and passes FR-SCH2 alongside its siblings. |
| `expect-roundtrip.txt` | `uv run python /tmp/expect-roundtrip-e6.py` (per-row `Expect.from_mapping` resolution over E6) | exit 0; resolves `expects[0..3]`→`file`, `expects[4]`→`exit_code` cleanly; proves the declarative DSL accepts every row, including all three `file`-substring assertions. |
| `run-E6.txt` | `uv run superclaude eval run --suite real --eval E6` | exit 1; hits the same pre-existing `NameError: name '_new_run_id' is not defined` in `cli/eval/commands.py:1418` documented in T05.03 / T05.04 / T05.05 / T05.06-prep / T05.07 / T05.08 / T05.09 evidence blocks. **Not introduced** by D-0090; predates the deliverable; runner-completion task owns the fix. |

### Describe output (manifest shape proof)

From `describe-E6.txt`:

```
id: E6
title: PreToolUse Edit matcher fires
category: hook-lifecycle
timeout_sec: 60
isolation:
  home_strategy: ephemeral
inputs:
- prompt: Use the Write tool to create a file named edited.txt under the current
    working directory with the single line 'before'.
- prompt: Use the Edit tool on edited.txt to replace 'before' with 'edited'.
- prompt: /quit
expects:
- file:
    path: logs/freshness.jsonl
    exists: true
- file:
    path: logs/freshness.jsonl
    exists: true
    contains: '"type":"pre_edit"'
- file:
    path: logs/freshness.jsonl
    exists: true
    contains: '"matcher":"Edit"'
- file:
    path: edited.txt
    exists: true
- exit_code:
    equals: 0
no_pty: skip
```

The describe output round-trips the body verbatim — proving:

- the YAML parses,
- the loader accepts every field (including the three-element
  `inputs[]` array and five-element `expects[]` array that
  distinguishes E6 from E3/E4/E5's smaller bodies),
- the schema validator (`suite.schema.json`) passes,
- the entry serializes back cleanly for `describe`-style rendering.

### Expect.from_mapping round-trip (declarative DSL proof)

From `expect-roundtrip.txt`:

```
Suite: real, evals: 17
E6: id=E6 title='PreToolUse Edit matcher fires'
E6.inputs: ({'prompt': "Use the Write tool to create a file named edited.txt under the current working directory with the single line 'before'."}, {'prompt': "Use the Edit tool on edited.txt to replace 'before' with 'edited'."}, {'prompt': '/quit'})
E6.expects (raw rows from manifest): (
  {'file': {'path': 'logs/freshness.jsonl', 'exists': True}},
  {'file': {'path': 'logs/freshness.jsonl', 'exists': True, 'contains': '"type":"pre_edit"'}},
  {'file': {'path': 'logs/freshness.jsonl', 'exists': True, 'contains': '"matcher":"Edit"'}},
  {'file': {'path': 'edited.txt', 'exists': True}},
  {'exit_code': {'equals': 0}},
)

=== Expect.from_mapping round-trip ===
  expects[0]: ... -> file (callable)
  expects[1]: ... -> file (callable)
  expects[2]: ... -> file (callable)
  expects[3]: ... -> file (callable)
  expects[4]: ... -> exit_code (callable)

All expects rows resolve cleanly.
```

Every row resolves to a named `ExpectCallable` via the public
`Expect.from_mapping` entry point — the same path the runner takes at
EvalContext construction time. This is the strongest static proof
available at T05.10 authoring time that the body **will** execute as
declared once the runner NameError fix lands. The `inputs` tuple also
confirms the three-prompt shape (Write seed → Edit fire → /quit)
loads correctly.

### Suite enumeration (FR-SCH2 + count proof)

From `list-with-E6.txt`:

```
[
  {
    "eval_count": 17,
    "name": "real",
    "version": "1.0"
  }
]
```

`eval_count: 17` is unchanged from the post-T05.07/T05.08/T05.09 sum:
E1 (1) + E2.{1,2,3} (3) + E3..E15 (13) = 17. The list command
performs full manifest load + FR-SCH2 validation across every eval
id — `E6` is implicitly accepted by the count being non-erroring and
identical to the pre-edit total (the entry already existed as a
scaffolding stub; T05.10 only populated its body).

### Run command output (pre-existing blocker)

From `run-E6.txt`:

```
File "/config/workspace/IronClaude/src/superclaude/cli/eval/commands.py", line 1418, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

Same pre-existing runner bug documented in T05.03 / T05.04 / T05.05 /
T05.06-prep / T05.07 / T05.08 / T05.09 evidence. Not in scope for
T05.10; documented for parity with sibling deliverables.

## Schema validation

The post-edit YAML loads cleanly under `validate_manifest(...)`:

- The loader does not raise (proof: `expect-roundtrip.txt` reports
  `Suite: real, evals: 17`).
- The schema validator is invoked internally; clean load confirms no
  `additionalProperties: false` violations, no schema-required field
  omissions, and no enum mismatches.
- Each `expects[]` row has exactly one primitive key (4×`file`,
  1×`exit_code`) which matches `PRIMITIVE_NAMES` (`expect.py:56-64`).
- `inputs[]` carries three `{prompt: str}` mappings — the open-shape
  schema accepts the multi-prompt form without modification.
- `eval describe` renders the body without round-trip loss.

## Coverage gate impact

E6 issues no MCP tool calls in its assertion surface and carries no
`expect_tool_call` field (Write and Edit are built-in Claude Code
tools, not MCP-prefixed). `_iter_eval_tool_calls(spec_E6)` is empty
for the MCP-matcher-prefix dimension, so E6 contributes nothing to
the matcher-coverage triad gate (which remains E1 + E2.1-3 territory;
see D-0086 §"Completing the v1 matcher-coverage triad" /
`coverage-map.txt` evidence). E6's coverage contribution lives in the
**hook-event** coverage axis (D-0082 §3): **PreToolUse (matcher=Edit)**
is now covered. E7 / E8 will complete the PreToolUse matcher-group
coverage when they land.

## Pre-existing runner bug (not in scope for T05.10)

`uv run superclaude eval run --suite real --eval E6` exits 1 with:

```
File "/config/workspace/IronClaude/src/superclaude/cli/eval/commands.py", line 1418, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

Same failure documented across the T05.03..T05.09 evidence trail.
**Not introduced** by D-0090; predates this deliverable; fixing it is
the responsibility of the runner-completion task that is a Phase-5
dependency of the CP-P05-T07-T11 checkpoint (T05.12). T05.10's
acceptance criteria (manifest body landed matching OQ-2 resolution,
FR-SCH2-valid id, body roundtrips through `Expect.from_mapping`,
spec/notes/evidence recorded under D-0090/) are met by the
describe / list / roundtrip evidence above.

## Pre-existing hook-script gap (not in scope for T05.10)

`freshness-pre-edit.sh` does not yet write to `logs/freshness.jsonl`
on the normal PreToolUse path; it writes to
**`logs/freshness-hook.jsonl`** (note the `-hook` suffix) and uses
**`event`/`tool`** field names rather than the OQ-2-contract
**`type`/`matcher`** names.

Two divergences vs. OQ-2 D-0082 §4 contract:

1. **Path**: `logs/freshness-hook.jsonl` vs. asserted
   `logs/freshness.jsonl`.
2. **Field names**: `event=PreToolUse` / `tool=Edit` vs. asserted
   `type=pre_edit` / `matcher=Edit`.

The OQ-2 resolution (D-0082 §4) freezes the eval body to assert this
observable on the basis of the **hook contract**, not the current
hook implementation. T05.10's job is to author the manifest body
matching the frozen shape; updating `freshness-pre-edit.sh` to emit
the asserted observable is a downstream task that, when paired with
the runner NameError fix, unblocks the per-task AC ("`eval run --eval
E6` exits 0 deterministically across 3 runs"). See spec §8.1 + notes
§"Hook telemetry gap" for the full discovery + mitigation discussion.

The gap mirrors the parallel `session-init.sh` gap from D-0087 §8.1,
`freshness-session-start.sh` gap from D-0088 §8.1, and
`freshness-user-prompt.sh` gap from D-0089 §8.1 — a single follow-up
task can pair all four script updates.

## Cross-deliverable verification

| Deliverable | Verification status at T05.10 close |
|---|---|
| D-0082 (OQ-2 resolution) | E6 body in real.yaml matches §4 row E6 verbatim (with `event_count == 1` predicate deferred per spec §3 footnote) ✅ |
| D-0083 (E1 body) | Independent — different hook surface |
| D-0086 (E2.3 body) | Independent — different hook surface; substring-proxy verification pattern reused |
| D-0087 (E3 body) | Sibling — position-0 SessionStart hook; same PTY spawn, different hook surface ✅ |
| D-0088 (E4 body) | Sibling — position-1 SessionStart matcher=* hook; same ledger target, different hook surface ✅ |
| D-0089 (E5 body) | Sibling — UserPromptSubmit no-matcher hook; same ledger target ✅ |
| T05.10 spec.md | All sections rendered; sign-off block populated ✅ |
| T05.10 notes.md | Design rationale + telemetry-gap + event_count-deferral + matcher-discrimination rationale + three-input rationale documented ✅ |
| T05.10 evidence/ | 4 evidence files captured: describe, list, expect-roundtrip, run (with documented pre-existing blocker) ✅ |

## Acceptance criteria check (T05.10)

Per phase-5-tasklist.md T05.10 acceptance criteria:

- ✅ **AC1:** File `suites/real.yaml` contains entry `id: E6` whose body matches the OQ-2 resolution recorded in T05.01. (Evidence: `describe-E6.txt` shows the full body; matches D-0082 §4 row E6 verbatim modulo the deferred `event_count == 1` predicate documented in spec §3 footnote and notes §"Why `event_count == 1` is deferred".)
- ⚠️ **AC2 (transitive):** `uv run superclaude eval run --suite real --eval E6` exits 0 on a clean HOME. **Blocked by pre-existing runner NameError + pre-existing hook-script gap**, both out of T05.10 scope per sibling deliverables D-0083 / D-0086 / D-0087 / D-0088 / D-0089. Manifest body is authored such that AC2 becomes satisfiable as soon as both upstream fixes land. (Evidence: `run-E6.txt` documents the NameError; spec §8.1 + notes §"Hook telemetry gap" document the script gap.)
- ⚠️ **AC3 (transitive):** E6 is deterministic: 3 consecutive runs produce identical EvalOutcome statuses. Same transitive blocker as AC2. The body **is** deterministic by construction (notes §"Determinism analysis"): no time / network / shared-state dependencies, no asserted-against `ts` / `session_id` / `tool_call_idx` / `recent_read_age_sec` / `decision` / `reason` fields, no asserted-against agent reasoning text. Once AC2 unblocks, AC3 will hold without further body changes.
- ✅ **AC4:** Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`. (Evidence: `isolation.home_strategy: ephemeral`; all asserted paths are relative — `logs/freshness.jsonl`, `edited.txt` — and resolve against `ctx.home_path` per `expect.py:79-91`.)
- ✅ **AC5:** `TASKLIST_ROOT/artifacts/D-0090/spec.md` records the eval body summary. (Evidence: present at `.dev/releases/current/cliEval/artifacts/D-0090/spec.md`.)

Net: 3 of 5 ACs are PASS at T05.10 close; 2 are transitively blocked
on the same pre-existing infrastructure issues that block E1 / E2.1-3
/ E3 / E4 / E5 from full execution today. T05.10 lands every
acceptance criterion that is within scope.
