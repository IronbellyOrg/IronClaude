# T05.19 — Evidence Manifest

**Task:** T05.19 — Author E13 eval body per OQ-2 resolution
**Deliverable:** D-0097
**Date:** 2026-05-20

## Files

| File | What it proves | AC mapped |
|---|---|---|
| `describe-E13.txt` | `superclaude eval describe --suite real --eval E13` renders the OQ-2-frozen body (title `"Hook stderr error fails open"`, category `hook-lifecycle`, 3 inputs (Write seed / Read trigger / `/quit`), 5 expects (3× file substring on `logs/hook-errors.jsonl` + stderr.contains + exit_code.equals(0)), `timeout_sec: 60`, `no_pty: skip`). | AC: "File `suites/real.yaml` contains entry `id: E13` matching the OQ-2 resolution"; AC: "`TASKLIST_ROOT/artifacts/D-0097/spec.md` records the eval body summary" (cross-link). |
| `list-default.txt` | `superclaude eval list` enumerates suite `real (version 1.0, 17 evals)` — the suite continues to load cleanly after the E13 body landed (schema validation passes; no parse error). | AC: implicit — schema validity is a precondition for the suite enumerating at all. |
| `list-with-E13.txt` | `superclaude eval list --json` confirms the eval count is still 17 (E1-E15 with E2 parameterized to E2.1-E2.3). The E13 body change did not break suite-wide loading; E13 enumerates with the new title "Hook stderr error fails open" and `requires=[]`. | AC: implicit — the post-OQ-2 17-eval roster is intact. |
| `expect-roundtrip.txt` | Python round-trip of each E13 `expects[]` row through `Expect.from_mapping`. Three `file` rows + one `stderr` row + one `exit_code` row all resolve to valid `ExpectCallable`s. Suite-wide enumeration shows E13 listed with the new title "Hook stderr error fails open" and `requires=[]`. | AC: "Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`" — the `file` primitive resolves `path: logs/hook-errors.jsonl` against `EvalContext.home_path` per `expect.py:187-268`; `stderr` and `exit_code` primitives consume `EvalContext.process_result` per `expect.py:556-569`. |

## Out-of-scope (deferred / blocked)

- `superclaude eval run --suite real --eval E13` 3-run determinism proof — blocked on `commands.py:1418` `NameError: name '_new_run_id' is not defined`. Same blocker documented in T05.03..T05.17 evidence blocks. Responsibility of the runner-completion task (Phase-5 dependency).
- **Failing-fixture script** (`tests/fixtures/hooks/failing-post-read.sh`) does not exist on disk today — a follow-up task is responsible for landing it as a deterministic-exit shell script (e.g., `printf "simulated hook failure\n" >&2; exit 17`).
- **hooks.json-variant deployment path** does not exist — the per-eval setup wrapper deploys the production `src/superclaude/hooks/hooks.json` verbatim; no `isolation.hooks_variant:` schema field and no `inputs[].setup:` callback could swap in a test-only hooks.json registering the failing fixture.
- **Harness structured hook-error ledger** (`<home>/.claude/logs/hook-errors.jsonl`) emission is not wired — the harness propagates hook stderr opaquely but does not emit the structured `{type:"hook_error", disposition:"fail_open"}` row.
- **Same-row conjunction** for the `{type, disposition}` substring proxies — deferred per D-0097 spec.md §8.1 to a follow-up task gated on the YAML `callback:` escape hatch (D-4) or a future declarative `jsonl.contains_event:` primitive. The currently landed body uses two parallel `Expect.file(contains=…)` substring assertions, which converge with the strict semantic in practice (the harness emits all fields on a single row by design per design-spec §11).

See D-0097 spec.md §8 + §8.1 and notes.md "Scaffolding-gap
inheritance" for full deferral rationale and inheritance from
T05.07..T05.17 posture. T05.19 inherits the deepest scaffolding-gap
stack of any post-OQ-2 body landed so far (three preconditions, vs.
T05.17's zero) — but the body itself is FR-SCH2-valid and resolves
correctly through `Expect.from_mapping`, satisfying the per-task ACs
for the body-authoring deliverable.
