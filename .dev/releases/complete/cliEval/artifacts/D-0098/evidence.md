# D-0098 — Evidence Pointer

**Deliverable ID:** D-0098
**Task ID:** T05.20 (Phase 5)
**Date:** 2026-05-20

Evidence artifacts for T05.20 live under
`TASKLIST_ROOT/evidence/T05.20/` (= `.dev/releases/current/cliEval/evidence/T05.20/`).

## Quick links

- `evidence/T05.20/describe-E14.txt` — `eval describe --suite real --eval E14` output (proves OQ-2 body rendered by CLI: title `"Concurrent SessionStart bursts"`, category `hook-lifecycle`, 1 input (`/quit`), 3 expects (2× `file` + 1× `exit_code`), `timeout_sec: 60`, `no_pty: skip`, `isolation.home_strategy: ephemeral`)
- `evidence/T05.20/list-with-E14.txt` — `eval list --json` output (proves suite enumerates 17 evals — schema acceptance after E14 body landed)
- `evidence/T05.20/list-default.txt` — `eval list` plain output (sibling sanity check — suite `real (version 1.0, 17 evals)` loads cleanly)
- `evidence/T05.20/expect-roundtrip.txt` — Python round-trip of each `expects[]` row through `Expect.from_mapping` (2× `file`, 1× `exit_code` all resolve to valid `ExpectCallable`s); suite-wide enumeration confirms E14 listed with new title "Concurrent SessionStart bursts" and `requires=[]`

## Out-of-scope (deferred to schema-bump + callback-wiring + runner-completion tasks)

- Full `eval run --eval E14` PTY execution + 3-run determinism proof — blocked on `commands.py:1418` `NameError` (runner-completion task downstream of T05.20). Same blocker documented in T05.03..T05.19 evidence blocks.
- **YAML `callback:` schema field** does not exist today — `suites/suite.schema.json` has `evalEntry.additionalProperties: false`, which would reject the field. Deferred per spec.md §8.1 to schema-bump follow-up task (per D-4 escape hatch).
- **`SuiteLoader` callback-string resolution** is not wired — no import-path → callable resolution in `loader.py`. Deferred per spec.md §3 / §8.1 to loader-extension follow-up task.
- **`EvalRunner` callback-invocation path** does not exist — `runner.py` drives one PTY session per eval via `claude_process.py`; no alternative invocation path that hands control to a Python callable. Deferred per spec.md §3 / §8.1 to runner-extension follow-up task.
- **`superclaude.cli.eval.suites.real_callbacks` module** does not exist — the named callable `E14_concurrent_session_start` has no implementation; the module directory itself does not exist. Deferred per spec.md §3 / §8.1 to callable-implementation follow-up task.
- **Multi-HOME isolation orchestration** does not exist — the per-eval setup wrapper (NFR-ISO2 / T02.13) creates ONE HOME per eval; the callback would need N=3 distinct HOMEs per invocation with per-session observables collected for assertion. Deferred per spec.md §3 / §8.1 to setup-wrapper extension follow-up task.
- **Inherited gap — `session-init.sh` doesn't emit `{"type":"session_init",...}` rows** to `logs/session-events.jsonl` today (the script writes `state/session-init.log` only). Shared with E3 / T05.07; deferred to the same hook-script-emission follow-up task. Until this closes, `Expect.file(logs/session-events.jsonl, contains '"type":"session_init"')` will ERROR (file doesn't exist), not FAIL.
- **Per-`<sid>` sticky file glob assertion** (`state/auggie-first-pending/<sid>.txt`) — the proxy at `expects[0]` checks the parent directory `state/auggie-first-pending`, not per-session file paths. The per-`<sid>` form requires either a callback (multi-HOME) or a new `file_glob:` primitive in `expect.py`. Deferred per spec.md §8.1.

See D-0098 spec.md §3 + §8.1 and notes.md "Scaffolding-gap
inheritance" for full deferral rationale and the deepest-stack
position vs. T05.17 (0 gaps) and T05.19 (3 gaps): T05.20 inherits
**5 scaffolding gaps + 1 inherited hook-script-emission gap**, the
deepest of any post-OQ-2 body landed so far. Critically, T05.20 is
the only post-OQ-2 body whose strict form requires a **schema
extension** rather than only hook-script wiring or hooks.json
variants. The body itself is FR-SCH2-valid and resolves correctly
through `Expect.from_mapping`, satisfying the per-task acceptance
criteria for the body-authoring deliverable.
