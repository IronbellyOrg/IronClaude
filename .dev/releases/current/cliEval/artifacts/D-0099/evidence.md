# D-0099 — Evidence Pointer

**Deliverable ID:** D-0099
**Task ID:** T05.21 (Phase 5)
**Date:** 2026-05-20

Evidence artifacts for T05.21 live under
`TASKLIST_ROOT/evidence/T05.21/` (= `.dev/releases/current/cliEval/evidence/T05.21/`).

## Quick links

- `evidence/T05.21/describe-E15.txt` — `eval describe --suite real --eval E15` output (proves OQ-2 body rendered by CLI: title `"hook timeout fails open with telemetry"`, category `hook-lifecycle`, 3 inputs (Write seed + Read fixture.txt + /quit), 4 expects (3× `file` against `logs/hook-errors.jsonl` + 1× `exit_code`), `timeout_sec: 60`, `no_pty: skip`, `isolation.home_strategy: ephemeral`)
- `evidence/T05.21/list-with-E15.txt` — `eval list --json` output (proves suite enumerates 17 evals — schema acceptance after E15 body landed)
- `evidence/T05.21/list-default.txt` — `eval list` plain output (sibling sanity check — suite `real (version 1.0, 17 evals)` loads cleanly)
- `evidence/T05.21/expect-roundtrip.txt` — Python round-trip of each `expects[]` row through `Expect.from_mapping` (3× `file`, 1× `exit_code` all resolve to valid `ExpectCallable`s); suite-wide enumeration confirms E15 listed with title "hook timeout fails open with telemetry" and `requires=[]`

## Out-of-scope (deferred to shared follow-ups with E13 + Expect.duration extension)

- Full `eval run --eval E15` PTY execution + 3-run determinism proof — blocked on `commands.py:1418` `NameError: name '_new_run_id' is not defined` (runner-completion task downstream of T05.21). Same blocker documented in T05.03..T05.20 evidence blocks.
- **Fixture script `tests/fixtures/hooks/slow-post-read.sh` does not exist** — required by OQ-2 input shape but not on disk. Deferred per spec.md §8.1 to fixture-script-creation follow-up task. Unique to E15 (sibling E13 needs `failing-post-read.sh`, different fixture).
- **`isolation.hooks_variant:` schema field does not exist on `evalEntry`** — per-eval setup wrapper (`hook_adapter.deploy_hooks_to(home_path)`, NFR-ISO2 / T02.13) deploys the production `src/superclaude/hooks/hooks.json` verbatim; no path for swapping in a test-only hooks.json with the slow fixture registered AND the per-hook `timeout:` field tuned below the sleep. **SHARED WITH E13 (T05.19/D-0097)** — both rely on the same hooks.json-variant deployment path; the schema-bump + setup-wrapper extension closes both at once.
- **Structured `logs/hook-errors.jsonl` emission distinguishing `type:"hook_timeout"` from `type:"hook_error"` not wired** — current PTY harness's per-hook timeout enforcement is structural (subprocess timeout / SIGTERM) but does NOT emit the OQ-2-named `{type:"hook_timeout", disposition:"fail_open"}` row. **SHARED WITH E13 (T05.19/D-0097)** — same ledger file, different discriminator; the harness-emission extension closes both at once. Until this closes, `Expect.file(logs/hook-errors.jsonl, contains '"type":"hook_timeout"')` will ERROR (file doesn't exist), not FAIL.
- **Expect.duration is not a PRIMITIVE_NAMES entry** — `Expect.PRIMITIVE_NAMES` enumerates `{file, exit_code, jsonl, settings_json, stderr}` per `expect.py`; no `duration:` row in declarative YAML. The OQ-2-named `duration.less_than(hook_timeout + 2.0)` wall-clock upper-bound assertion is deferred to a primitive-extension follow-up task. **Unique to E15** — no sibling eval requires Expect.duration; this is the only post-OQ-2 body whose strict form introduces a brand-new declarative primitive (vs T05.20/E14 which required a YAML callback-field schema extension).

See D-0099 spec.md §3 + §8.1 and notes.md "Scaffolding-gap inheritance
vs T05.07..T05.20" for full deferral rationale. T05.21 inherits **4
scaffolding gaps** (3 shared with E13 + 1 unique Expect.duration
primitive), one less than T05.20's 5 because T05.21 reuses E13's
hooks.json-variant + ledger-emission tracks rather than introducing
fresh dependencies. T05.21 is the only post-OQ-2 body whose strict
form requires a **new Expect.* primitive** rather than a schema
extension (T05.20) or hook-script wiring (T05.07..T05.16). The body
itself is FR-SCH2-valid and resolves correctly through
`Expect.from_mapping`, satisfying the per-task acceptance criteria
for the body-authoring deliverable.

T05.21 is the **seventeenth and final eval body** to land under the
OQ-2 resolution; the 17-eval roster (E1, E2.1-2.3, E3-E15) is now
schema-complete.
