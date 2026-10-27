# D-0097 — Evidence Pointer

**Deliverable ID:** D-0097
**Task ID:** T05.19 (Phase 5)
**Date:** 2026-05-20

Evidence artifacts for T05.19 live under
`TASKLIST_ROOT/evidence/T05.19/` (= `.dev/releases/current/cliEval/evidence/T05.19/`).

## Quick links

- `evidence/T05.19/describe-E13.txt` — `eval describe --suite real --eval E13` output (proves OQ-2 body rendered by CLI: title `"Hook stderr error fails open"`, category `hook-lifecycle`, 3 inputs, 5 expects, `timeout_sec: 60`, `no_pty: skip`)
- `evidence/T05.19/list-with-E13.txt` — `eval list --json` output (proves suite enumerates 17 evals)
- `evidence/T05.19/list-default.txt` — `eval list` plain output (sibling sanity check — suite `real (version 1.0, 17 evals)` loads cleanly)
- `evidence/T05.19/expect-roundtrip.txt` — Python round-trip of each `expects[]` row through `Expect.from_mapping` (3×`file`, 1×`stderr`, 1×`exit_code` all resolve to valid `ExpectCallable`s)

## Out-of-scope (deferred to runner-completion + scaffolding tasks)

- Full `eval run --eval E13` PTY execution + 3-run determinism proof — blocked on `commands.py:1418` `NameError` (runner-completion task downstream of T05.19). Same blocker documented in T05.03..T05.17 evidence blocks.
- **Failing-fixture script** (`tests/fixtures/hooks/failing-post-read.sh`) does not exist on disk today — a follow-up task is responsible for landing it as a deterministic-exit shell script. Per spec.md §3 / notes.md "Scaffolding-gap inheritance".
- **hooks.json-variant deployment path** does not exist — the per-eval setup wrapper deploys the production `src/superclaude/hooks/hooks.json` verbatim; no `isolation.hooks_variant:` schema field and no `inputs[].setup:` callback. Deferred per spec.md §8.1 to either (a) YAML `callback:` escape hatch (D-4) or (b) new `isolation.hooks_variant:` schema field.
- **Harness structured hook-error ledger emission** is not wired — the harness propagates hook stderr opaquely but does not emit the structured `{type:"hook_error", disposition:"fail_open"}` row to `logs/hook-errors.jsonl`. Deferred per spec.md §8.1 to a future harness-completion task.
- **Same-row conjunction** for the `{type, disposition}` substring proxies — deferred per spec.md §8.1 to a follow-up task gated on the YAML `callback:` escape hatch or a future declarative `jsonl.contains_event:` primitive. The currently landed body uses two parallel `Expect.file(contains=…)` substring assertions, which converge with the strict semantic in practice (the harness emits all fields on a single row by design per design-spec §11).

See D-0097 spec.md §8 + §8.1 + notes.md "Scaffolding-gap inheritance"
for the full deferral rationale and inheritance from T05.07..T05.17
posture. T05.19 inherits the deepest scaffolding-gap stack of any
post-OQ-2 body landed so far (three preconditions, vs. T05.17's
zero) — but the body itself is FR-SCH2-valid and resolves correctly
through `Expect.from_mapping`, satisfying the per-task acceptance
criteria for the body-authoring task.
