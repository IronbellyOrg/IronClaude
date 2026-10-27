# T05.21 — Evidence Manifest

**Task:** T05.21 — Author E15 eval body per OQ-2 resolution
**Deliverable:** D-0099
**Date:** 2026-05-20

## Files

| File | What it proves | AC mapped |
|---|---|---|
| `describe-E15.txt` | `superclaude eval describe --suite real --eval E15` renders the OQ-2-frozen body (title `"hook timeout fails open with telemetry"`, category `hook-lifecycle`, 3 inputs (Write seed + Read fixture.txt + /quit), 4 expects (3× `file` against `logs/hook-errors.jsonl` + 1× `exit_code`), `timeout_sec: 60`, `no_pty: skip`, `isolation.home_strategy: ephemeral`). | AC: "File `suites/real.yaml` contains entry `id: E15` matching the OQ-2 resolution"; AC: "`TASKLIST_ROOT/artifacts/D-0099/spec.md` records the eval body summary" (cross-link). |
| `list-default.txt` | `superclaude eval list` enumerates suite `real (version 1.0, 17 evals)` — the suite continues to load cleanly after the E15 body landed (schema validation passes; no parse error). | AC: implicit — schema validity is a precondition for the suite enumerating at all. |
| `list-with-E15.txt` | `superclaude eval list --json` confirms the eval count is still 17 (E1-E15 with E2 parameterized to E2.1-E2.3). The E15 body change did not break suite-wide loading; E15 enumerates with the new title "hook timeout fails open with telemetry" and `requires=[]`. | AC: implicit — the post-OQ-2 17-eval roster is intact and final. |
| `expect-roundtrip.txt` | Python round-trip of each E15 `expects[]` row through `Expect.from_mapping`. Three `file` rows + one `exit_code` row all resolve to valid `ExpectCallable`s. Suite-wide enumeration shows E15 listed with title "hook timeout fails open with telemetry" and `requires=[]`. | AC: "Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`" — the `file` primitive resolves paths against `EvalContext.home_path` per `expect.py:187-268`; `exit_code` primitive consumes `EvalContext.process_result` per `expect.py:556-569`. |

## Out-of-scope (deferred / blocked)

- `superclaude eval run --suite real --eval E15` 3-run determinism proof — blocked on `commands.py:1418` `NameError: name '_new_run_id' is not defined`. Same blocker documented in T05.03..T05.20 evidence blocks. Responsibility of the runner-completion task (Phase-5 dependency).
- **Slow fixture script `tests/fixtures/hooks/slow-post-read.sh`** does not exist on disk. Required by OQ-2 input shape (a sleep-longer-than-timeout shell script). Deferred per spec.md §8.1 to fixture-creation follow-up task. Unique to E15 — E13's `failing-post-read.sh` is a sibling, different behavior.
- **`isolation.hooks_variant:` schema field** does not exist today — `suites/suite.schema.json` has `evalEntry.additionalProperties: false`. SHARED WITH E13/T05.19; the schema bump + setup-wrapper extension closes both at once.
- **Structured `logs/hook-errors.jsonl` emission** distinguishing `type:"hook_timeout"` from `type:"hook_error"` not wired — current PTY harness reaps slow hooks structurally (subprocess timeout) but does NOT emit the OQ-2-named row to a structured ledger. SHARED WITH E13/T05.19 — same ledger file, different discriminator.
- **Expect.duration primitive** is not a `PRIMITIVE_NAMES` entry — declarative YAML cannot express the OQ-2-named `duration.less_than(hook_timeout + 2.0)` wall-clock bound. Unique to E15; deferred to a primitive-extension follow-up task.

See D-0099 spec.md §3 + §8.1 and notes.md "Scaffolding-gap inheritance
vs T05.07..T05.20" for full deferral rationale. T05.21 inherits **4
scaffolding gaps** (3 shared with E13 + 1 unique Expect.duration
primitive) — one less than T05.20's 5 because T05.21 reuses E13's
hooks.json-variant + ledger-emission tracks rather than introducing
fresh dependencies. T05.21 is the only post-OQ-2 body whose strict
form requires a **new Expect.* primitive** rather than a schema
extension (T05.20) or hook-script wiring (T05.07..T05.16). The body
itself is FR-SCH2-valid and resolves correctly through
`Expect.from_mapping`, satisfying the per-task ACs for the
body-authoring deliverable.

T05.21 is the **seventeenth and final eval body** to land under the
OQ-2 resolution; the 17-eval roster is now schema-complete.
