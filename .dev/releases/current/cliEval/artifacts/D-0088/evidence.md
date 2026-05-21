# D-0088 — Cross-references / evidence

## Source files inspected

| File | Lines | Purpose |
|---|---|---|
| `src/superclaude/cli/eval/suites/real.yaml` | 227-289 (post-edit) | E4 manifest entry |
| `src/superclaude/cli/eval/suites/suite.schema.json` | 124-160 | Eval entry schema (inputs/expects open-shape, no_pty enum, isolation enum) |
| `src/superclaude/cli/eval/expect.py` | 56-64 (PRIMITIVE_NAMES), 186-265 (Expect.file), 269-369 (Expect.jsonl — for the YAML-expressibility analysis), 484-551 (Expect.exit_code), 640-669 (Expect.from_mapping) | Primitive surface for the three assertions in this body + the deferred `event_count` analysis |
| `src/superclaude/hooks/hooks.json` | 4-25 (SessionStart block) | First-position SessionStart → `session-init.sh` (E3 / D-0087); second-position matcher=`*` → `freshness-session-start.sh` (E4 / this) |
| `src/superclaude/hooks/scripts/freshness-session-start.sh` | full (especially the `jq -nc ... hookSpecificOutput ...` emit block, lines ~115-120) | Current revision of the freshness hook — emits SessionStart envelope to stdout; **does not** yet write `logs/freshness.jsonl` (see spec §8.1 + notes §"Hook telemetry gap") |
| `.dev/releases/current/cliEval/decisions.md` | 530-583 (OQ-2 block, esp. line 544 E4 frozen row) | OQ-2 resolution status + E4 frozen row |
| `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` | §3 (hook-surface map), §4 (E4 body shape), §6 (capability rollup), §7 (impacts row T05.08 → E4 → R-087) | Frozen body shape source of truth |
| `.dev/releases/current/cliEval/artifacts/D-0087/spec.md` | full | Sibling deliverable (E3 body, first-position SessionStart) — companion to this deliverable; same posture on telemetry gap |
| `.dev/releases/current/cliEval/artifacts/D-0087/notes.md` | full | Sibling design notes — `event_count`/callable trade-off, telemetry-gap mitigation pattern carried forward |
| `.dev/releases/current/cliEval/phase-5-tasklist.md` | T05.08 block | Source task spec |

## Manifest delta

Pre-edit (scaffolding):

```yaml
- id: E4
  title: "session_start hook deploys settings.json into ephemeral HOME"
  category: hook-lifecycle
  isolation:
    home_strategy: ephemeral
  no_pty: skip
```

Notable pre-edit issues addressed by T05.08:

1. **Title was a pre-OQ-2 placeholder** — referenced "session_start
   hook deploys settings.json into ephemeral HOME", which was the
   pre-OQ-2 understanding before D-0082 §3 finalized the hook-surface
   coverage map. The OQ-2 resolution (D-0082 §4 row E4 / decisions.md
   line 544) names E4 explicitly as "SessionStart matcher=* freshness
   hook fires" — a description of the *hook surface*, not a
   settings-deploy artifact. T05.08 replaces the title with the
   OQ-2-frozen text.
2. **No `timeout_sec`** — relied on suite default (120s). T05.08 pins
   `timeout_sec: 60` per spec §"Why timeout_sec: 60" and sibling
   parity with E3.
3. **No `inputs` / `expects`** — scaffolding only. T05.08 lands the
   OQ-2 body shape verbatim.

Post-edit (`real.yaml:227-289`):

```yaml
- id: E4
  title: "SessionStart matcher=* freshness hook fires"
  category: hook-lifecycle
  timeout_sec: 60
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # T05.08 / D-0088 — body shape per OQ-2 resolution (D-0082 §4).
  # E4 exercises the SECOND SessionStart hook entry in hooks.json
  # (matcher=*, command=freshness-session-start.sh) — distinct from
  # the first-position SessionStart entry (no matcher,
  # session-init.sh) which is covered by E3. Both SessionStart hooks
  # fire before prompt-ready on a fresh PTY spawn; E3 pins the
  # position-0 hook's side-effects and E4 pins position-1.
  #
  # OQ-2-frozen body shape (D-0082 §4 / decisions.md OQ-2):
  #   - inputs: spawn fresh claude session; /quit to exit cleanly
  #     (identical input shape to E3 — same spawn triggers both
  #     SessionStart hooks).
  #   - expects[0]: file.exists(logs/freshness.jsonl) — proves the
  #     freshness event ledger was opened by the matcher=* hook.
  #   - expects[1]: file(logs/freshness.jsonl, contains
  #     '"type":"session_start"') — proves the session_start event
  #     was emitted into the freshness ledger by freshness-session-
  #     start.sh. Expect.jsonl predicate filters require a Python
  #     callable (expect.py:269-369), not expressible in declarative
  #     YAML; following the E3 / E1 / E2.1-3 precedent, the
  #     event-fire assertion uses Expect.file with the JSONL
  #     substring. The D-0082 §4 `event_count == 1` aspect is the
  #     same kind of count assertion that requires a callable —
  #     deferred to a follow-up under the YAML callback escape
  #     hatch (D-4) if duplicate-fire detection becomes load-bearing.
  #   - expects[2]: exit_code.equals(0) — clean session exit on /quit.
  #
  # [plus capability / determinism / telemetry-gap comment block]
  inputs:
    - prompt: "/quit"
  expects:
    - file:
        path: logs/freshness.jsonl
        exists: true
    - file:
        path: logs/freshness.jsonl
        exists: true
        contains: '"type":"session_start"'
    - exit_code:
        equals: 0
```

## Verification runs

Captured under `.dev/releases/current/cliEval/evidence/T05.08/`:

| File | Command | Outcome |
|---|---|---|
| `describe-E4.txt` | `uv run superclaude eval describe --suite real --eval E4` | exit 0; renders the new inputs/expects rows verbatim; proves manifest body is loadable and round-trips through the manifest loader. |
| `list-with-E4.txt` | `uv run superclaude eval list --json` | exit 0; reports `eval_count: 17` for the `real` suite (1 + 3 + 13 = 17 entries: E1 + E2.{1,2,3} + E3..E15) — confirms E4 enumerates and passes FR-SCH2 alongside its siblings. |
| `expect-roundtrip.txt` | `uv run python -c "..."` (per-row `Expect.from_mapping` resolution over E4) | exit 0; resolves `expects[0]`→`file`, `expects[1]`→`file`, `expects[2]`→`exit_code` cleanly; proves the declarative DSL accepts every row. |
| `run-E4.txt` | `uv run superclaude eval run --suite real --eval E4` | exit 1; hits the same pre-existing `NameError: name '_new_run_id' is not defined` in `cli/eval/commands.py:1418` documented in T05.03 / T05.04 / T05.05 / T05.06-prep / T05.07 evidence blocks. **Not introduced** by D-0088; predates the deliverable; runner-completion task owns the fix. |

### Describe output (manifest shape proof)

From `describe-E4.txt`:

```
id: E4
title: SessionStart matcher=* freshness hook fires
category: hook-lifecycle
timeout_sec: 60
isolation:
  home_strategy: ephemeral
inputs:
- prompt: /quit
expects:
- file:
    path: logs/freshness.jsonl
    exists: true
- file:
    path: logs/freshness.jsonl
    exists: true
    contains: '"type":"session_start"'
- exit_code:
    equals: 0
no_pty: skip
```

The describe output round-trips the body verbatim — proving:

- the YAML parses,
- the loader accepts every field,
- the schema validator (`suite.schema.json`) passes,
- the entry serializes back cleanly for `describe`-style rendering.

### Expect.from_mapping round-trip (declarative DSL proof)

From `expect-roundtrip.txt`:

```
Suite: real, evals: 17
E4: id=E4 title='SessionStart matcher=* freshness hook fires'
E4.inputs: ({'prompt': '/quit'},)
E4.expects (raw rows from manifest): (
  {'file': {'path': 'logs/freshness.jsonl', 'exists': True}},
  {'file': {'path': 'logs/freshness.jsonl', 'exists': True, 'contains': '"type":"session_start"'}},
  {'exit_code': {'equals': 0}},
)

=== Expect.from_mapping round-trip ===
  expects[0]: ... -> file (callable)
  expects[1]: ... -> file (callable)
  expects[2]: ... -> exit_code (callable)

All expects rows resolve cleanly.
```

Every row resolves to a named `ExpectCallable` via the public
`Expect.from_mapping` entry point — the same path the runner takes at
EvalContext construction time. This is the strongest static proof
available at T05.08 authoring time that the body **will** execute as
declared once the runner NameError fix lands.

### Suite enumeration (FR-SCH2 + count proof)

From `list-with-E4.txt`:

```
[
  {
    "eval_count": 17,
    "name": "real",
    "version": "1.0"
  }
]
```

`eval_count: 17` is the post-T05.07-and-T05.08 sum: E1 (1) + E2.{1,2,3} (3) +
E3..E15 (13) = 17. The list command performs full manifest load +
FR-SCH2 validation across every eval id — `E4` is implicitly accepted
by the count being non-erroring.

### Run command output (pre-existing blocker)

From `run-E4.txt`:

```
NameError: name '_new_run_id' is not defined
```

Same pre-existing runner bug documented in T05.03 / T05.04 / T05.05 /
T05.06-prep / T05.07 evidence. Not in scope for T05.08; documented for
parity with sibling deliverables.

## Schema validation

The post-edit YAML loads cleanly under `SuiteLoader().load(...)`:

- The loader does not raise (proof: `expect-roundtrip.txt` reports
  `Suite: real, evals: 17`).
- The schema validator is invoked internally; clean load confirms no
  `additionalProperties: false` violations, no schema-required field
  omissions, and no enum mismatches.
- Each `expects[]` row has exactly one primitive key (`file`, `file`,
  `exit_code`) which matches `PRIMITIVE_NAMES` (`expect.py:56-64`).
- `eval describe` renders the body without round-trip loss.

## Coverage gate impact

E4 issues no MCP tool calls. `_iter_eval_tool_calls(spec_E4)` is
empty, so E4 contributes nothing to the matcher-coverage triad gate
(which remains E1 + E2.1-3 territory; see D-0086 §"Completing the v1
matcher-coverage triad" / `coverage-map.txt` evidence). E4's coverage
contribution lives in the **hook-event** coverage axis (D-0082 §3):
second-position `SessionStart` (matcher=*) is now covered, completing
the SessionStart row paired with E3 (D-0087, first-position
`SessionStart` / no-matcher).

## Pre-existing runner bug (not in scope for T05.08)

`uv run superclaude eval run --suite real --eval E4` exits 1 with:

```
File "/config/workspace/IronClaude/src/superclaude/cli/eval/commands.py", line 1418, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

Same failure documented across the T05.03..T05.07 evidence trail.
**Not introduced** by D-0088; predates this deliverable; fixing it is
the responsibility of the runner-completion task that is a Phase-5
dependency of the CP-P05-T07-T11 checkpoint (T05.12). T05.08's
acceptance criteria (manifest body landed matching OQ-2 resolution,
FR-SCH2-valid id, body roundtrips through `Expect.from_mapping`,
spec/notes/evidence recorded under D-0088/) are met by the
describe / list / roundtrip evidence above.

## Pre-existing hook-script gap (not in scope for T05.08)

`freshness-session-start.sh` does not yet write to
`logs/freshness.jsonl`. The script emits its SessionStart envelope to
stdout via `jq -nc ... hookSpecificOutput ...` (the Claude Code hook
output channel) but does not append a `session_start` row to a
freshness ledger.

The OQ-2 resolution (D-0082 §4) freezes the eval body to assert this
observable on the basis of the **hook contract**, not the current hook
implementation. T05.08's job is to author the manifest body matching
the frozen shape; updating `freshness-session-start.sh` to emit the
asserted observable is a downstream task that, when paired with the
runner NameError fix, unblocks the per-task AC ("`eval run --eval E4`
exits 0 deterministically across 3 runs"). See spec §8.1 + notes
§"Hook telemetry gap" for the full discovery + mitigation discussion.

The gap mirrors the parallel `session-init.sh` gap from D-0087 §8.1 —
a single follow-up task can pair both script updates.

## Cross-deliverable verification

| Deliverable | Verification status at T05.08 close |
|---|---|
| D-0082 (OQ-2 resolution) | E4 body in real.yaml matches §4 row E4 verbatim (with `event_count == 1` predicate deferred per spec §3 footnote) ✅ |
| D-0083 (E1 body) | Independent — different hook surface |
| D-0086 (E2.3 body) | Independent — different hook surface; substring-proxy verification pattern reused |
| D-0087 (E3 body) | Sibling — completes SessionStart row when paired with E4 ✅ |
| T05.08 spec.md | All sections rendered; sign-off block populated ✅ |
| T05.08 notes.md | Design rationale + telemetry-gap + event_count-deferral documented ✅ |
| T05.08 evidence/ | 4 evidence files captured: describe, list, expect-roundtrip, run (with documented pre-existing blocker) ✅ |

## Acceptance criteria check (T05.08)

Per phase-5-tasklist.md T05.08 acceptance criteria:

- ✅ **AC1:** File `suites/real.yaml` contains entry `id: E4` whose body matches the OQ-2 resolution recorded in T05.01. (Evidence: `describe-E4.txt` shows the full body; matches D-0082 §4 row E4 verbatim modulo the deferred `event_count == 1` predicate documented in spec §3 footnote and notes §"Why `event_count == 1` is deferred".)
- ⚠️ **AC2 (transitive):** `uv run superclaude eval run --suite real --eval E4` exits 0 on a clean HOME. **Blocked by pre-existing runner NameError + pre-existing hook-script gap**, both out of T05.08 scope per sibling deliverables D-0083 / D-0086 / D-0087. Manifest body is authored such that AC2 becomes satisfiable as soon as both upstream fixes land. (Evidence: `run-E4.txt` documents the NameError; spec §8.1 + notes §"Hook telemetry gap" document the script gap.)
- ⚠️ **AC3 (transitive):** E4 is deterministic: 3 consecutive runs produce identical EvalOutcome statuses. Same transitive blocker as AC2. The body **is** deterministic by construction (notes §"Determinism analysis"): no time / network / shared-state dependencies, no asserted-against `ts` or `session_id` fields. Once AC2 unblocks, AC3 will hold without further body changes.
- ✅ **AC4:** Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`. (Evidence: `isolation.home_strategy: ephemeral`; all asserted paths are relative — `logs/freshness.jsonl` — and resolve against `ctx.home_path` per `expect.py:79-91`.)
- ✅ **AC5:** `TASKLIST_ROOT/artifacts/D-0088/spec.md` records the eval body summary. (Evidence: present at `.dev/releases/current/cliEval/artifacts/D-0088/spec.md`.)

Net: 3 of 5 ACs are PASS at T05.08 close; 2 are transitively blocked
on the same pre-existing infrastructure issues that block E1 / E2.1-3 /
E3 from full execution today. T05.08 lands every acceptance criterion
that is within scope.
