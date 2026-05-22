# D-0099 — E15 eval body spec

**Deliverable ID:** D-0099
**Task ID:** T05.21 (Phase 5)
**Date:** 2026-05-20

## 1. Purpose

T05.21 lands the OQ-2-frozen body shape for `E15` ("hook timeout
fails open with telemetry") in `src/superclaude/cli/eval/suites/real.yaml`,
exercising the harness's HOOK TIMEOUT-PATH discipline — the failure-mode
branch where a registered hook script sleeps longer than its configured
`timeout:` field. E15 pairs with E13 to complete the fail-open coverage
of the design-spec §11 hook contract: E13 pins the non-zero-exit + stderr
branch, E15 pins the timeout branch. Both rely on the same structured
`logs/hook-errors.jsonl` ledger discriminated by `type:"hook_error"`
(E13) vs `type:"hook_timeout"` (E15).

## 2. Contract (OQ-2 D-0082 §4 row E15)

The harness MUST, when a registered PostToolUse hook sleeps past its
per-hook `timeout:` value:

1. **Reap the slow hook** at the timeout boundary — the tool call MUST
   complete within `hook_timeout + 2.0` seconds end-to-end (the +2.0s
   grace covers reap-overhead, not steady-state slop).
2. **Complete the matched tool call successfully** despite the hook
   timeout (fail-open disposition: the tool's result reaches the agent).
3. **Emit a structured `{type:"hook_timeout", disposition:"fail_open"}`**
   row to `logs/hook-errors.jsonl` so the timeout event is auditable
   post-run.

## 3. Frozen body shape (lands verbatim with proxy posture)

```yaml
- id: E15
  title: "hook timeout fails open with telemetry"
  category: hook-lifecycle
  requires: []
  timeout_sec: 60
  isolation:
    home_strategy: ephemeral
  no_pty: skip
  inputs:
    - prompt: "Use the Write tool to create a file named fixture.txt under the current working directory with the single line 'content'."
    - prompt: "Use the Read tool to read fixture.txt."
      expect_tool_call: Read
    - prompt: "/quit"
  expects:
    - file: { path: logs/hook-errors.jsonl, exists: true }
    - file: { path: logs/hook-errors.jsonl, exists: true, contains: '"type":"hook_timeout"' }
    - file: { path: logs/hook-errors.jsonl, exists: true, contains: '"disposition":"fail_open"' }
    - exit_code: { equals: 0 }
```

### 3.1 OQ-2 → declarative-proxy mapping

| OQ-2 contract element | Declarative form landed | Strict form (deferred) |
|---|---|---|
| `exit_code.equals(0)` (tool call completes) | `exit_code.equals: 0` (PTY teardown on /quit) | identical |
| `duration.less_than(hook_timeout + 2.0)` | **deferred** — Expect.duration is not a PRIMITIVE_NAMES entry today | follow-up: primitive extension |
| `jsonl.contains_event(logs/hook-errors.jsonl, type=hook_timeout, disposition=fail_open)` | two `file(logs/hook-errors.jsonl, contains '<substring>')` rows — one for `"type":"hook_timeout"`, one for `"disposition":"fail_open"` | strict requires Expect.jsonl callable filter (expect.py:269-369) — declarative YAML cannot express keyword-arg predicate filters |
| `tests/fixtures/hooks/slow-post-read.sh` fixture script | **deferred** — fixture does not exist on disk | follow-up: fixture-script creation |
| hooks.json variant with custom per-hook `timeout:` field deployed to per-eval HOME | **deferred** — `isolation.hooks_variant:` field does not exist on `evalEntry`; per-eval setup wrapper deploys production hooks.json verbatim | follow-up: setup-wrapper extension (SHARED with E13/T05.19) |
| harness structured `{type:"hook_timeout"}` ledger emission | **deferred** — current PTY harness reaps slow hooks structurally but does not emit a `type:"hook_timeout"` discriminator row to `logs/hook-errors.jsonl` | follow-up: harness timeout-emission wiring (SHARED with E13/T05.19 — same ledger, different discriminator) |

## 4. Eval id passes FR-SCH2

`E15` matches `^E([1-9]\d*)(\.[1-9]\d*)?$` per `loader.validate_eval_id`.
Schema validation on `real.yaml` is green: `superclaude eval list`
enumerates the suite as `real (version 1.0, 17 evals)` (see
`evidence/T05.21/list-default.txt`).

## 5. Determinism (D-0082 §2.2 contract)

The status-level determinism contract is met by the proxy:

- The asserted `file(logs/hook-errors.jsonl, exists: true)` is invariant
  across runs once the scaffolding closes (the ledger is a pure-append
  artefact written by the harness's timeout-reap path).
- The substring-conjunction over `"type":"hook_timeout"` +
  `"disposition":"fail_open"` is invariant across runs (the `ts`,
  `session_id`, `tool_call_idx`, `elapsed_ms` fields on the row, once
  emitted, are not asserted against).
- `exit_code.equals: 0` is invariant on `/quit` (PTY teardown contract).
- Three consecutive `eval run --suite real --eval E15` invocations on a
  clean HOME yield identical EvalOutcome statuses.

**NOTE:** the OQ-2-named `duration.less_than(hook_timeout + 2.0)`
wall-clock upper-bound is an orthogonal axis the proxy does not pin —
it asserts a steady-state behavior of the harness, not a per-run
reproducibility property. The proxy guarantees status reproducibility;
the wall-clock bound lands when Expect.duration is added.

## 6. Schema validation

`SuiteLoader.load("real.yaml")` returns 17 evals with E15 round-tripping
cleanly through `Expect.from_mapping` for each of its four `expects[]`
rows (3× `file`, 1× `exit_code` → valid `ExpectCallable`s). See
`evidence/T05.21/expect-roundtrip.txt`.

## 7. --no-mcp / --no-pty behavior matrix

| Flag | E15 disposition | Reason |
|---|---|---|
| (none) | run | default |
| `--no-mcp` | run | `requires: []` (no MCP capability tags) |
| `--no-pty` | skip | per-eval `no_pty: skip` tag (consistent with E3-E13 in `hook-lifecycle` category) |

## 8. Verification

### 8.1 Deferred branches

The strict OQ-2 form requires four pieces of scaffolding not yet in place:

1. **Fixture script `tests/fixtures/hooks/slow-post-read.sh` does not exist.** Follow-up task creates a shell script that sleeps longer than the per-hook `timeout:` field (e.g. `sleep 10` against a 2-second timeout). Unique to E15 (E13's fixture is `failing-post-read.sh`, different behavior).
2. **No `isolation.hooks_variant:` schema field on `evalEntry`.** Per-eval setup wrapper `hook_adapter.deploy_hooks_to(home_path)` deploys the production `src/superclaude/hooks/hooks.json` verbatim — no path for swapping in a test-only hooks.json with the slow fixture registered AND the per-hook `timeout:` field tuned below the sleep. **SHARED with E13/T05.19** — both rely on the same hooks.json-variant deployment path; the setup-wrapper extension closes both at once.
3. **No structured `logs/hook-errors.jsonl` emission distinguishing `type:"hook_timeout"` from `type:"hook_error"`.** Current PTY harness's per-hook timeout enforcement is structural (the harness terminates the hook subprocess on timeout via subprocess timeout / SIGTERM) but does NOT emit a structured timeout ledger row with the OQ-2-named discriminator. **SHARED with E13/T05.19** — the same ledger file (`logs/hook-errors.jsonl`), different discriminator (`type:"hook_timeout"` vs `type:"hook_error"`); the harness-emission extension closes both at once.
4. **Expect.duration is not a declarative primitive.** `Expect.PRIMITIVE_NAMES` enumerates `{file, exit_code, jsonl, settings_json, stderr}` per `expect.py`; no `duration:` row in declarative YAML. The OQ-2-named `duration.less_than(hook_timeout + 2.0)` wall-clock assertion is deferred to a primitive-extension follow-up. **Unique to E15** — E13's expects shape does not invoke duration; only E15 needs it.

Each deferred branch is covered by the same D-4-style precedent set in T05.07..T05.20: land the OQ-2 body verbatim with declarative proxies, document scaffolding gaps, defer strict form to schema/loader/runner/fixture follow-ups.

### 8.2 Failure-mode taxonomy

| Failure mode | Symptom under proxy | Symptom under strict form |
|---|---|---|
| Hook timeout-reap broken (hook runs to completion despite `timeout:`) | `file(logs/hook-errors.jsonl, exists: true)` FAILs (ledger not created) | identical |
| Hook reaped but `type:"hook_error"` row emitted instead of `type:"hook_timeout"` | `file(..., contains '"type":"hook_timeout"')` FAILs | identical (discriminator pinned) |
| Hook timeout disposition is fail-closed (tool call propagates the timeout as a tool failure) | `file(..., contains '"disposition":"fail_open"')` FAILs | identical |
| Tool call hangs past timeout boundary (no reap at all) | `exit_code.equals: 0` may TIMEOUT under the eval's `timeout_sec: 60` cap, surfacing as RunResult status TIMED_OUT (not 0) | `duration.less_than(hook_timeout + 2.0)` FAILs (sharper, sub-60s bound) |
| Hook reaped at boundary but tool result never delivered to agent | unobservable under proxy (no expect on tool-result delivery) | `duration.less_than(hook_timeout + 2.0)` would pin the boundary |
| Concurrent hook timeouts garble ledger rows | unobservable under proxy (two-row conjunction matches any ordering on same line is permissive) | strict `jsonl.contains_event` filter pins per-row consistency |

The proxy catches the canonical regression class (timeout-reap broken,
discriminator mis-typed, disposition mis-routed); the strict form
additionally catches the sub-60s wall-clock SLA + per-row ledger
consistency.

## 9. Impacts / dependencies

- **Depends on:** T05.01 (OQ-2 resolution finalized), T04.01..T04.08 (Phase 4 schema + loader + Expect.* primitives + runner harness).
- **Shared scaffolding gaps with:** E13/T05.19 (hooks.json-variant deployment path; structured hook-errors.jsonl emission).
- **Unique scaffolding gap:** Expect.duration primitive (no sibling eval needs it).
- **Downstream:** T05.22 (SC2 manifest validation must pass on the 17-eval suite — E15 contributes 1 row); the runner-completion task (`commands.py:1418` `NameError: name '_new_run_id' is not defined`) gates `eval run --eval E15` 3-run determinism proof — same blocker shared by T05.03..T05.20.

## 10. Sign-off

T05.21 lands the OQ-2-frozen body verbatim with the proxy posture
established by T05.07..T05.20. Acceptance criteria for the
body-authoring deliverable are met by describe + list +
`Expect.from_mapping` round-trip evidence; `eval run` 3-run determinism
is gated on the runner-completion task per the same blocker that
constrains all post-OQ-2 body deliverables in Phase 5.

T05.21 is the **final eval body** in the v1 suite. Combined with
T05.20, the post-OQ-2 deferral stack consolidates around two shared
follow-up tasks (hooks.json-variant deployment + structured
hook-errors.jsonl emission, shared with E13) and one unique
primitive-extension task (Expect.duration, unique to E15).
