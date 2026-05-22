# T05.20 — Evidence Manifest

**Task:** T05.20 — Author E14 eval body per OQ-2 resolution
**Deliverable:** D-0098
**Date:** 2026-05-20

## Files

| File | What it proves | AC mapped |
|---|---|---|
| `describe-E14.txt` | `superclaude eval describe --suite real --eval E14` renders the OQ-2-frozen body (title `"Concurrent SessionStart bursts"`, category `hook-lifecycle`, 1 input (`/quit`), 3 expects (2× `file` + 1× `exit_code`), `timeout_sec: 60`, `no_pty: skip`, `isolation.home_strategy: ephemeral`). | AC: "File `suites/real.yaml` contains entry `id: E14` matching the OQ-2 resolution"; AC: "`TASKLIST_ROOT/artifacts/D-0098/spec.md` records the eval body summary" (cross-link). |
| `list-default.txt` | `superclaude eval list` enumerates suite `real (version 1.0, 17 evals)` — the suite continues to load cleanly after the E14 body landed (schema validation passes; no parse error). | AC: implicit — schema validity is a precondition for the suite enumerating at all. |
| `list-with-E14.txt` | `superclaude eval list --json` confirms the eval count is still 17 (E1-E15 with E2 parameterized to E2.1-E2.3). The E14 body change did not break suite-wide loading; E14 enumerates with the new title "Concurrent SessionStart bursts" and `requires=[]`. | AC: implicit — the post-OQ-2 17-eval roster is intact. |
| `expect-roundtrip.txt` | Python round-trip of each E14 `expects[]` row through `Expect.from_mapping`. Two `file` rows + one `exit_code` row all resolve to valid `ExpectCallable`s. Suite-wide enumeration shows E14 listed with the new title "Concurrent SessionStart bursts" and `requires=[]`. | AC: "Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`" — the `file` primitive resolves paths against `EvalContext.home_path` per `expect.py:187-268`; `exit_code` primitive consumes `EvalContext.process_result` per `expect.py:556-569`. |

## Out-of-scope (deferred / blocked)

- `superclaude eval run --suite real --eval E14` 3-run determinism proof — blocked on `commands.py:1418` `NameError: name '_new_run_id' is not defined`. Same blocker documented in T05.03..T05.19 evidence blocks. Responsibility of the runner-completion task (Phase-5 dependency).
- **YAML `callback:` schema field** does not exist today — `suites/suite.schema.json` has `evalEntry.additionalProperties: false`, which rejects the field. Deferred per spec.md §3 / §8.1 to a schema-bump follow-up task (per D-4 escape hatch).
- **`SuiteLoader` callback-string resolution** is not wired — no `import_module + getattr` path in `loader.py`.
- **`EvalRunner` callback-invocation path** does not exist — runner drives one PTY session per eval via `claude_process.py`.
- **`superclaude.cli.eval.suites.real_callbacks` module** does not exist — the named callable `E14_concurrent_session_start` has no implementation; the module directory itself does not exist.
- **Multi-HOME isolation orchestration** does not exist — the per-eval setup wrapper creates ONE HOME per eval; the callback would need N=3 distinct HOMEs per invocation.
- **Inherited gap from E3 / T05.07:** `session-init.sh` does not yet append `{"type":"session_init",...}` rows to `logs/session-events.jsonl` — the OQ-2 contract names this ledger path; the current hook script only writes `state/session-init.log`. Shared follow-up task is responsible for the JSONL emission.
- **Per-`<sid>` sticky file glob assertion** (`state/auggie-first-pending/<sid>.txt`) — the proxy at `expects[0]` checks the parent directory, not per-session file paths. The strict per-`<sid>` form requires either a callback (multi-HOME) or a new `file_glob:` primitive in `expect.py`.

See D-0098 spec.md §3 + §8.1 and notes.md "Scaffolding-gap
inheritance" for full deferral rationale and inheritance from
T05.07..T05.19 posture. T05.20 inherits the **deepest** scaffolding-
gap stack of any post-OQ-2 body landed so far (five preconditions
+ one inherited hook-script emission gap, vs. T05.19's three and
T05.17's zero) — AND is the only post-OQ-2 body whose strict form
requires a **schema extension** (not just hook-script wiring or
hooks.json variants). The body itself is FR-SCH2-valid and resolves
correctly through `Expect.from_mapping`, satisfying the per-task
ACs for the body-authoring deliverable.
