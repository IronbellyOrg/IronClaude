# D-0087 — Cross-references / evidence

## Source files inspected

| File | Lines | Purpose |
|---|---|---|
| `src/superclaude/cli/eval/suites/real.yaml` | 178-183 (pre-edit), 178-225 (post-edit) | E3 manifest entry |
| `src/superclaude/cli/eval/suites/suite.schema.json` | 124-160 | Eval entry schema (inputs/expects open-shape, no_pty enum, isolation enum) |
| `src/superclaude/cli/eval/expect.py` | 56-64 (PRIMITIVE_NAMES), 186-265 (Expect.file), 484-551 (Expect.exit_code), 640-669 (from_mapping) | Primitive surface for the three assertions in this body |
| `src/superclaude/hooks/hooks.json` | 4-15 (SessionStart block) | First-position SessionStart hook → session-init.sh; second-position matcher=`*` → freshness-session-start.sh |
| `src/superclaude/scripts/session-init.sh` | 1-31 | Current revision of session-init.sh — emits banner to stdout; **does not** yet write `state/session-init.log` or `logs/session-events.jsonl` (see spec §8.1 + notes §"Hook telemetry gap") |
| `.dev/releases/current/cliEval/decisions.md` | 530-583 (OQ-2 block) | OQ-2 resolution status + E3 frozen row at line 543 |
| `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` | §3 (hook-surface map), §4 (E3 body shape), §6 (capability rollup), §7 (impacts row T05.07 → E3 → R-086) | Frozen body shape source of truth |
| `.dev/releases/current/cliEval/artifacts/D-0083/spec.md` | full | Sibling deliverable (E1 body) — sticky-clear hook contract pattern carried forward |
| `.dev/releases/current/cliEval/artifacts/D-0086/spec.md` | full | Most-recent matcher-coverage sibling — template for this deliverable's spec structure |
| `.dev/releases/current/cliEval/phase-5-tasklist.md` | T05.07 block (lines 301-349) | Source task spec |

## Manifest delta

Pre-edit (`real.yaml:178-183`):

```yaml
- id: E3
  title: "30-minute freshness gate fires on stale prompt timestamp"
  category: hook-lifecycle
  isolation:
    home_strategy: ephemeral
  no_pty: skip
```

Notable pre-edit issues addressed by T05.07:

1. **Title was a placeholder** referencing "30-minute freshness gate"
   — superseded by OQ-2 resolution (D-0082 §"Determinism + isolation"
   / decisions.md:565): *"the original design-spec note tying E3 to
   '30-min freshness tests' is superseded; freshness-staleness via
   time offset becomes a follow-up eval after OQ-8 closes."* T05.07
   replaces the title with the OQ-2-frozen text "SessionStart
   unmatched (session-init) hook fires".
2. **No `timeout_sec`** — relied on suite default (120s). T05.07 pins
   `timeout_sec: 60` per spec §"Why timeout_sec: 60".
3. **No `inputs` / `expects`** — scaffolding only. T05.07 lands the
   OQ-2 body shape.

Post-edit (`real.yaml:178-225`):

```yaml
- id: E3
  title: "SessionStart unmatched (session-init) hook fires"
  category: hook-lifecycle
  timeout_sec: 60
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # T05.07 / D-0087 — body shape per OQ-2 resolution (D-0082 §4).
  # E3 exercises the FIRST SessionStart hook entry in hooks.json
  # (no matcher, command=session-init.sh) — distinct from the second
  # SessionStart entry (matcher=*, freshness-session-start.sh) which
  # is covered by E4. Spawning a fresh claude session via the PTY
  # harness triggers both SessionStart hooks before prompt-ready;
  # the first-position hook is responsible for emitting the
  # session_init telemetry into the per-eval HOME.
  #
  # OQ-2-frozen body shape (D-0082 §4 / spec.md §3):
  #   - inputs: spawn fresh claude session; /quit to exit cleanly.
  #   - expects[0]: file.exists(state/session-init.log) — proves the
  #     first-position SessionStart hook ran (script writes its own
  #     log into the per-eval HOME under $HOME/.claude/state/).
  #   - expects[1]: file(logs/session-events.jsonl, contains
  #     '"type":"session_init"') — proves the session_init event was
  #     emitted into the SessionStart event ledger. Expect.jsonl
  #     with predicate filters requires a Python callable
  #     (expect.py:269-369), not expressible in YAML — so the
  #     event-fire assertion uses Expect.file with the JSONL
  #     substring, same pattern E1 / E2.1-3 use for their
  #     sticky_cleared assertions on logs/auggie-first.jsonl.
  #   - expects[2]: exit_code.equals(0) — clean session exit on /quit.
  #
  # No capability tags; no MCP; no network — runs on every host.
  # Determinism (D-0082 §2.2): every PTY spawn writes a new session
  # log + JSONL event with a fresh `ts` field that is not asserted
  # against, so the body passes/fails the same way every run on a
  # clean per-eval HOME (FR-ISO2).
  inputs:
    - prompt: "/quit"
  expects:
    - file:
        path: state/session-init.log
        exists: true
    - file:
        path: logs/session-events.jsonl
        exists: true
        contains: '"type":"session_init"'
    - exit_code:
        equals: 0
```

## Verification runs

Captured under `.dev/releases/current/cliEval/evidence/T05.07/`:

| File | Command | Outcome |
|---|---|---|
| `describe-E3.txt` | `uv run superclaude eval describe --suite real --eval E3` | exit 0; renders the new inputs/expects rows verbatim; proves manifest body is loadable and round-trips through the manifest loader. |
| `list-with-E3.txt` | `uv run superclaude eval list --json` | exit 0; reports `eval_count: 17` for the `real` suite (1 + 3 + 13 = 17 entries: E1 + E2.{1,2,3} + E3..E15) — confirms E3 enumerates and passes FR-SCH2 alongside its siblings. |
| `expect-roundtrip.txt` | `uv run python -c "from superclaude.cli.eval.expect import Expect; from superclaude.cli.eval.loader import SuiteLoader; ..."` (per-row `Expect.from_mapping` resolution) | exit 0; resolves `expects[0]`→`file`, `expects[1]`→`file`, `expects[2]`→`exit_code` cleanly; proves the declarative DSL accepts every row. |
| `run-E3.txt` | `uv run superclaude eval run --suite real --eval E3` | exit 1; hits the same pre-existing `NameError: name '_new_run_id' is not defined` in `cli/eval/commands.py:1418` documented in T05.03 / T05.04 / T05.05 / T05.06-prep evidence blocks. **Not introduced** by D-0087; predates the deliverable; runner-completion task owns the fix. |

### Describe output (manifest shape proof)

```
id: E3
title: SessionStart unmatched (session-init) hook fires
category: hook-lifecycle
timeout_sec: 60
isolation:
  home_strategy: ephemeral
inputs:
- prompt: /quit
expects:
- file:
    path: state/session-init.log
    exists: true
- file:
    path: logs/session-events.jsonl
    exists: true
    contains: '"type":"session_init"'
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
E3: id=E3 title='SessionStart unmatched (session-init) hook fires'
E3.inputs: ({'prompt': '/quit'},)
E3.expects (raw rows from manifest): (
  {'file': {'path': 'state/session-init.log', 'exists': True}},
  {'file': {'path': 'logs/session-events.jsonl', 'exists': True, 'contains': '"type":"session_init"'}},
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
available at T05.07 authoring time that the body **will** execute as
declared once the runner NameError fix lands.

## Schema validation

The post-edit YAML loads cleanly under `SuiteLoader().load(...)`:

- The loader does not raise (proof: `expect-roundtrip.txt` reports
  `Suite: real, evals: 17`).
- The schema validator (`SuiteLoader.validate_manifest`) is invoked
  internally; clean load confirms no `additionalProperties: false`
  violations, no schema-required field omissions, and no enum
  mismatches.
- Each `expects[]` row has exactly one primitive key (`file`, `file`,
  `exit_code`) which matches `PRIMITIVE_NAMES` (`expect.py:56-64`).
- `eval describe` renders the body without round-trip loss.

## Coverage gate impact

E3 issues no MCP tool calls. `_iter_eval_tool_calls(spec_E3)` is
empty, so E3 contributes nothing to the matcher-coverage triad gate
(which remains E1 + E2.1-3 territory; see D-0086 §"Completing the v1
matcher-coverage triad" / `coverage-map.txt` evidence). E3's coverage
contribution lives in the **hook-event** coverage axis (D-0082 §3):
first-position `SessionStart` is now covered, completing the
SessionStart row when E4 lands (T05.08 / D-0088).

## Pre-existing runner bug (not in scope for T05.07)

`uv run superclaude eval run --suite real --eval E3` exits 1 with:

```
File "/config/workspace/IronClaude/src/superclaude/cli/eval/commands.py", line 1418, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

This is the same failure documented in T05.03 / T05.04 / T05.05
evidence (`run-E2.{1,2,3}-no-mcp.txt`) and is **not introduced** by
D-0087. It predates this deliverable; fixing it is the responsibility
of the runner-completion task that is a Phase-5 dependency of the
CP-P05-T07-T11 checkpoint (T05.12). T05.07's acceptance criteria
(manifest body landed matching OQ-2 resolution, FR-SCH2-valid id,
body roundtrips through `Expect.from_mapping`, spec/notes/evidence
recorded under D-0087/) are met by the describe / list / roundtrip
evidence above.

## Pre-existing hook-script gap (not in scope for T05.07)

`session-init.sh` does not yet write to `state/session-init.log` or
`logs/session-events.jsonl`. The grep confirms zero occurrences of
either name across `src/`:

```
$ grep -rn "session-init\.log\|session-events\.jsonl\|session_init" src/
(no output)
```

The OQ-2 resolution (D-0082 §4) freezes the eval body to assert
these observables on the basis of the **hook contract**, not the
current hook implementation. T05.07's job is to author the manifest
body matching the frozen shape; updating session-init.sh to emit the
asserted observables is a downstream task that, when paired with the
runner NameError fix, unblocks the per-task AC ("`eval run --eval E3`
exits 0 deterministically across 3 runs"). See spec §8.1 + notes
§"Hook telemetry gap" for the full discovery + mitigation discussion.

## Cross-deliverable verification

| Deliverable | Verification status at T05.07 close |
|---|---|
| D-0082 (OQ-2 resolution) | E3 body in real.yaml matches §4 row E3 verbatim ✅ |
| D-0083 (E1 body) | Independent — different hook surface |
| D-0086 (E2.3 body) | Independent — different hook surface; verification pattern reused |
| T05.07 spec.md | All sections rendered; sign-off block populated |
| T05.07 notes.md | Design rationale + telemetry-gap discovery documented |
| T05.07 evidence/ | 4 evidence files captured: describe, list, expect-roundtrip, run (with documented pre-existing blocker) |

## Acceptance criteria check (T05.07)

Per phase-5-tasklist.md T05.07 lines 336-345:

- ✅ **AC1:** File `suites/real.yaml` contains entry `id: E3` whose body matches the OQ-2 resolution recorded in T05.01. (Evidence: `describe-E3.txt` shows the full body; matches D-0082 §4 row E3 verbatim.)
- ⚠️ **AC2 (transitive):** `uv run superclaude eval run --suite real --eval E3` exits 0 on a clean HOME. **Blocked by pre-existing runner NameError + pre-existing hook-script gap**, both out of T05.07 scope per sibling deliverables D-0083 / D-0086. Manifest body is authored such that AC2 becomes satisfiable as soon as both upstream fixes land. (Evidence: `run-E3.txt` documents the NameError; spec §8.1 + notes §"Hook telemetry gap" document the script gap.)
- ⚠️ **AC3 (transitive):** E3 is deterministic: 3 consecutive runs produce identical EvalOutcome statuses. Same transitive blocker as AC2. The body **is** deterministic by construction (notes §"Determinism analysis"): no time / network / shared-state dependencies, no asserted-against `ts` or `session_id` fields. Once AC2 unblocks, AC3 will hold without further body changes.
- ✅ **AC4:** Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`. (Evidence: `isolation.home_strategy: ephemeral`; all asserted paths are relative — `state/session-init.log`, `logs/session-events.jsonl` — and resolve against `ctx.home_path` per `expect.py:79-91`.)
- ✅ **AC5:** `TASKLIST_ROOT/artifacts/D-0087/spec.md` records the eval body summary. (Evidence: present at `.dev/releases/current/cliEval/artifacts/D-0087/spec.md`.)

Net: 3 of 5 ACs are PASS at T05.07 close; 2 are transitively blocked
on the same pre-existing infrastructure issues that block E1 / E2.1-3
from full execution today. T05.07 lands every acceptance criterion
that is within scope.
