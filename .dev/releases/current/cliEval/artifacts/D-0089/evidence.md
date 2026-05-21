# D-0089 — Cross-references / evidence

## Source files inspected

| File | Lines | Purpose |
|---|---|---|
| `src/superclaude/cli/eval/suites/real.yaml` | 291-367 (post-edit) | E5 manifest entry |
| `src/superclaude/cli/eval/suites/suite.schema.json` | 124-160 | Eval entry schema (inputs/expects open-shape, no_pty enum, isolation enum) |
| `src/superclaude/cli/eval/expect.py` | 56-64 (PRIMITIVE_NAMES), 186-265 (Expect.file), 269-369 (Expect.jsonl — for the YAML-expressibility analysis), 484-551 (Expect.exit_code), 640-669 (Expect.from_mapping) | Primitive surface for the three assertions in this body + the deferred `event_count` analysis |
| `src/superclaude/hooks/hooks.json` | UserPromptSubmit block (single entry, no matcher, command=freshness-user-prompt.sh, timeout=3) | Single UserPromptSubmit hook entry — covered exclusively by E5 |
| `src/superclaude/hooks/scripts/freshness-user-prompt.sh` | 252-256 (truncation-only ledger write), 259-264 (stdout `hookSpecificOutput` emit) | Current revision of the UserPromptSubmit hook — emits envelope to stdout; **does not** yet write `logs/freshness.jsonl` on the normal path (see spec §8.1 + notes §"Hook telemetry gap") |
| `.dev/releases/current/cliEval/decisions.md` | 530-583 (OQ-2 block, esp. line 545 E5 frozen row) | OQ-2 resolution status + E5 frozen row |
| `.dev/releases/current/cliEval/artifacts/D-0082/spec.md` | §3 (hook-surface map), §4 (E5 body shape), §6 (capability rollup), §7 (impacts row T05.09 → E5 → R-088) | Frozen body shape source of truth |
| `.dev/releases/current/cliEval/artifacts/D-0087/spec.md` | full | Sibling deliverable (E3 body, first-position SessionStart) — same telemetry-gap posture |
| `.dev/releases/current/cliEval/artifacts/D-0088/spec.md` | full | Sibling deliverable (E4 body, second-position SessionStart matcher=*) — same JSONL ledger target |
| `.dev/releases/current/cliEval/artifacts/D-0088/notes.md` | full | Sibling design notes — substring-proxy / event_count-deferral pattern carried forward |
| `.dev/releases/current/cliEval/phase-5-tasklist.md` | T05.09 block (lines 400-448) | Source task spec |

## Manifest delta

Pre-edit (scaffolding):

```yaml
- id: E5
  title: "pre_tool_call hook denies on missing capability"
  category: hook-lifecycle
  isolation:
    home_strategy: ephemeral
  no_pty: skip
```

Notable pre-edit issues addressed by T05.09:

1. **Title was a pre-OQ-2 placeholder** — referenced "pre_tool_call
   hook denies on missing capability", which was a pre-OQ-2
   understanding (the pre_tool_call surface is actually owned by E6
   per D-0082 §3 / decisions.md). The OQ-2 resolution (D-0082 §4 row
   E5 / decisions.md line 545) names E5 explicitly as
   "UserPromptSubmit freshness hook fires" — a description of the
   UserPromptSubmit hook surface. T05.09 replaces the title with the
   OQ-2-frozen text.
2. **No `timeout_sec`** — relied on suite default (120s). T05.09 pins
   `timeout_sec: 60` per spec §"Why timeout_sec: 60" and sibling
   parity with E3 / E4.
3. **No `inputs` / `expects`** — scaffolding only. T05.09 lands the
   OQ-2 body shape verbatim, including the content-prompt injection
   `"echo test"` that distinguishes E5 from the SessionStart-only
   E3/E4 siblings.

Post-edit (`real.yaml:291-367`):

```yaml
- id: E5
  title: "UserPromptSubmit freshness hook fires"
  category: hook-lifecycle
  timeout_sec: 60
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  # T05.09 / D-0089 — body shape per OQ-2 resolution (D-0082 §4).
  # E5 exercises the sole UserPromptSubmit hook entry in hooks.json
  # (no matcher, command=freshness-user-prompt.sh, timeout=3) —
  # distinct from the two SessionStart hooks (E3 covers position-0
  # session-init.sh; E4 covers position-1 matcher=*
  # freshness-session-start.sh). UserPromptSubmit fires once per
  # user prompt submission; the eval injects a content prompt
  # ("echo test" per D-0082 §4) so the hook fires at least once
  # before the session exits on /quit.
  #
  # OQ-2-frozen body shape (D-0082 §4 row E5):
  #   - inputs[0]: prompt "echo test" — the injected content prompt
  #     that fires UserPromptSubmit; matches the D-0082 §4
  #     inject_prompt("echo test") shape verbatim.
  #   - inputs[1]: prompt "/quit" — clean session exit so
  #     exit_code.equals(0) can pin the PTY teardown contract
  #     (sibling pattern to E3 / E4).
  #   - expects[0]: file.exists(logs/freshness.jsonl) — proves the
  #     freshness event ledger was opened by the UserPromptSubmit
  #     hook (or a prior SessionStart hook on the same spawn).
  #   - expects[1]: file(logs/freshness.jsonl, contains
  #     '"type":"user_prompt"') — proves the user_prompt event row
  #     was emitted into the freshness ledger by
  #     freshness-user-prompt.sh. Expect.jsonl predicate filters
  #     require a Python callable (expect.py:269-369), not
  #     expressible in declarative YAML; following the E3 / E4 /
  #     E1 / E2.1-3 precedent, the event-fire assertion uses
  #     Expect.file with the JSONL substring. The D-0082 §4
  #     `event_count >= 1 per injected prompt` aspect is the same
  #     kind of count assertion that requires a callable — deferred
  #     to a follow-up under the YAML callback escape hatch (D-4)
  #     if per-prompt event-count discrimination becomes
  #     load-bearing.
  #   - expects[2]: exit_code.equals(0) — clean session exit on /quit.
  #
  # [plus capability / determinism / telemetry-gap comment block]
  inputs:
    - prompt: "echo test"
    - prompt: "/quit"
  expects:
    - file:
        path: logs/freshness.jsonl
        exists: true
    - file:
        path: logs/freshness.jsonl
        exists: true
        contains: '"type":"user_prompt"'
    - exit_code:
        equals: 0
```

## Verification runs

Captured under `.dev/releases/current/cliEval/evidence/T05.09/`:

| File | Command | Outcome |
|---|---|---|
| `describe-E5.txt` | `uv run superclaude eval describe --suite real --eval E5` | exit 0; renders the new inputs/expects rows verbatim; proves manifest body is loadable and round-trips through the manifest loader. |
| `list-with-E5.txt` | `uv run superclaude eval list --json` | exit 0; reports `eval_count: 17` for the `real` suite (1 + 3 + 13 = 17 entries: E1 + E2.{1,2,3} + E3..E15) — confirms E5 enumerates and passes FR-SCH2 alongside its siblings. |
| `expect-roundtrip.txt` | `uv run python -c "..."` (per-row `Expect.from_mapping` resolution over E5) | exit 0; resolves `expects[0]`→`file`, `expects[1]`→`file`, `expects[2]`→`exit_code` cleanly; proves the declarative DSL accepts every row. |
| `run-E5.txt` | `uv run superclaude eval run --suite real --eval E5` | exit 1; hits the same pre-existing `NameError: name '_new_run_id' is not defined` in `cli/eval/commands.py:1418` documented in T05.03 / T05.04 / T05.05 / T05.06-prep / T05.07 / T05.08 evidence blocks. **Not introduced** by D-0089; predates the deliverable; runner-completion task owns the fix. |

### Describe output (manifest shape proof)

From `describe-E5.txt`:

```
id: E5
title: UserPromptSubmit freshness hook fires
category: hook-lifecycle
timeout_sec: 60
isolation:
  home_strategy: ephemeral
inputs:
- prompt: echo test
- prompt: /quit
expects:
- file:
    path: logs/freshness.jsonl
    exists: true
- file:
    path: logs/freshness.jsonl
    exists: true
    contains: '"type":"user_prompt"'
- exit_code:
    equals: 0
no_pty: skip
```

The describe output round-trips the body verbatim — proving:

- the YAML parses,
- the loader accepts every field (including the two-element
  `inputs[]` array that distinguishes E5 from E3/E4's single-prompt
  inputs),
- the schema validator (`suite.schema.json`) passes,
- the entry serializes back cleanly for `describe`-style rendering.

### Expect.from_mapping round-trip (declarative DSL proof)

From `expect-roundtrip.txt`:

```
Suite: real, evals: 17
E5: id=E5 title='UserPromptSubmit freshness hook fires'
E5.inputs: ({'prompt': 'echo test'}, {'prompt': '/quit'})
E5.expects (raw rows from manifest): (
  {'file': {'path': 'logs/freshness.jsonl', 'exists': True}},
  {'file': {'path': 'logs/freshness.jsonl', 'exists': True, 'contains': '"type":"user_prompt"'}},
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
available at T05.09 authoring time that the body **will** execute as
declared once the runner NameError fix lands. The `inputs` tuple also
confirms the two-prompt shape (`"echo test"` + `"/quit"`) loads
correctly.

### Suite enumeration (FR-SCH2 + count proof)

From `list-with-E5.txt`:

```
[
  {
    "eval_count": 17,
    "name": "real",
    "version": "1.0"
  }
]
```

`eval_count: 17` is unchanged from the post-T05.07-and-T05.08 sum:
E1 (1) + E2.{1,2,3} (3) + E3..E15 (13) = 17. The list command
performs full manifest load + FR-SCH2 validation across every eval
id — `E5` is implicitly accepted by the count being non-erroring and
identical to the pre-edit total (the entry already existed as a
scaffolding stub; T05.09 only populated its body).

### Run command output (pre-existing blocker)

From `run-E5.txt`:

```
File "/config/workspace/IronClaude/src/superclaude/cli/eval/commands.py", line 1418, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

Same pre-existing runner bug documented in T05.03 / T05.04 / T05.05 /
T05.06-prep / T05.07 / T05.08 evidence. Not in scope for T05.09;
documented for parity with sibling deliverables.

## Schema validation

The post-edit YAML loads cleanly under `SuiteLoader().load(...)`:

- The loader does not raise (proof: `expect-roundtrip.txt` reports
  `Suite: real, evals: 17`).
- The schema validator is invoked internally; clean load confirms no
  `additionalProperties: false` violations, no schema-required field
  omissions, and no enum mismatches.
- Each `expects[]` row has exactly one primitive key (`file`, `file`,
  `exit_code`) which matches `PRIMITIVE_NAMES` (`expect.py:56-64`).
- `inputs[]` carries two `{prompt: str}` mappings — the open-shape
  schema accepts the multi-prompt form without modification.
- `eval describe` renders the body without round-trip loss.

## Coverage gate impact

E5 issues no MCP tool calls in its assertion surface and carries no
`expect_tool_call` field. `_iter_eval_tool_calls(spec_E5)` is empty,
so E5 contributes nothing to the matcher-coverage triad gate (which
remains E1 + E2.1-3 territory; see D-0086 §"Completing the v1
matcher-coverage triad" / `coverage-map.txt` evidence). E5's coverage
contribution lives in the **hook-event** coverage axis (D-0082 §3):
**UserPromptSubmit (no matcher)** is now covered, advancing the
freshness-hook-chain coverage to full when paired with E3 + E4. With
T05.07 + T05.08 + T05.09 landed, every freshness-related hook
registration in `hooks.json` has a corresponding eval body asserting
its observable.

## Pre-existing runner bug (not in scope for T05.09)

`uv run superclaude eval run --suite real --eval E5` exits 1 with:

```
File "/config/workspace/IronClaude/src/superclaude/cli/eval/commands.py", line 1418, in eval_run
    run_id = _new_run_id()
             ^^^^^^^^^^^
NameError: name '_new_run_id' is not defined
```

Same failure documented across the T05.03..T05.08 evidence trail.
**Not introduced** by D-0089; predates this deliverable; fixing it is
the responsibility of the runner-completion task that is a Phase-5
dependency of the CP-P05-T07-T11 checkpoint (T05.12). T05.09's
acceptance criteria (manifest body landed matching OQ-2 resolution,
FR-SCH2-valid id, body roundtrips through `Expect.from_mapping`,
spec/notes/evidence recorded under D-0089/) are met by the
describe / list / roundtrip evidence above.

## Pre-existing hook-script gap (not in scope for T05.09)

`freshness-user-prompt.sh` does not yet write to
`logs/freshness.jsonl` on the normal UserPromptSubmit path. The
script emits its envelope to stdout via
`jq -nc ... hookSpecificOutput ...` (lines 259-264, the Claude Code
hook output channel) and writes truncation telemetry to
`logs/freshness-hook.jsonl` only when the envelope must be truncated
(lines 252-256), but does not append a `user_prompt` row to the
freshness ledger on the normal path.

The OQ-2 resolution (D-0082 §4) freezes the eval body to assert this
observable on the basis of the **hook contract**, not the current
hook implementation. T05.09's job is to author the manifest body
matching the frozen shape; updating `freshness-user-prompt.sh` to
emit the asserted observable is a downstream task that, when paired
with the runner NameError fix, unblocks the per-task AC ("`eval run
--eval E5` exits 0 deterministically across 3 runs"). See spec §8.1
+ notes §"Hook telemetry gap" for the full discovery + mitigation
discussion.

The gap mirrors the parallel `session-init.sh` gap from D-0087 §8.1
and `freshness-session-start.sh` gap from D-0088 §8.1 — a single
follow-up task can pair all three script updates.

## Cross-deliverable verification

| Deliverable | Verification status at T05.09 close |
|---|---|
| D-0082 (OQ-2 resolution) | E5 body in real.yaml matches §4 row E5 verbatim (with `event_count >= 1 per injected prompt` predicate deferred per spec §3 footnote) ✅ |
| D-0083 (E1 body) | Independent — different hook surface |
| D-0086 (E2.3 body) | Independent — different hook surface; substring-proxy verification pattern reused |
| D-0087 (E3 body) | Sibling — position-0 SessionStart hook; same PTY spawn, different hook surface ✅ |
| D-0088 (E4 body) | Sibling — position-1 SessionStart matcher=* hook; same ledger target, different hook surface ✅ |
| T05.09 spec.md | All sections rendered; sign-off block populated ✅ |
| T05.09 notes.md | Design rationale + telemetry-gap + event_count-deferral + content-prompt input rationale documented ✅ |
| T05.09 evidence/ | 4 evidence files captured: describe, list, expect-roundtrip, run (with documented pre-existing blocker) ✅ |

## Acceptance criteria check (T05.09)

Per phase-5-tasklist.md T05.09 acceptance criteria:

- ✅ **AC1:** File `suites/real.yaml` contains entry `id: E5` whose body matches the OQ-2 resolution recorded in T05.01. (Evidence: `describe-E5.txt` shows the full body; matches D-0082 §4 row E5 verbatim modulo the deferred `event_count >= 1 per injected prompt` predicate documented in spec §3 footnote and notes §"Why `event_count >= 1 per injected prompt` is deferred".)
- ⚠️ **AC2 (transitive):** `uv run superclaude eval run --suite real --eval E5` exits 0 on a clean HOME. **Blocked by pre-existing runner NameError + pre-existing hook-script gap**, both out of T05.09 scope per sibling deliverables D-0083 / D-0086 / D-0087 / D-0088. Manifest body is authored such that AC2 becomes satisfiable as soon as both upstream fixes land. (Evidence: `run-E5.txt` documents the NameError; spec §8.1 + notes §"Hook telemetry gap" document the script gap.)
- ⚠️ **AC3 (transitive):** E5 is deterministic: 3 consecutive runs produce identical EvalOutcome statuses. Same transitive blocker as AC2. The body **is** deterministic by construction (notes §"Determinism analysis"): no time / network / shared-state dependencies, no asserted-against `ts` / `session_id` / `turn` fields, no asserted-against agent reply text. Once AC2 unblocks, AC3 will hold without further body changes.
- ✅ **AC4:** Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`. (Evidence: `isolation.home_strategy: ephemeral`; all asserted paths are relative — `logs/freshness.jsonl` — and resolve against `ctx.home_path` per `expect.py:79-91`.)
- ✅ **AC5:** `TASKLIST_ROOT/artifacts/D-0089/spec.md` records the eval body summary. (Evidence: present at `.dev/releases/current/cliEval/artifacts/D-0089/spec.md`.)

Net: 3 of 5 ACs are PASS at T05.09 close; 2 are transitively blocked
on the same pre-existing infrastructure issues that block E1 / E2.1-3
/ E3 / E4 from full execution today. T05.09 lands every acceptance
criterion that is within scope.
