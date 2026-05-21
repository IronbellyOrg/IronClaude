# T05.17 — Evidence Manifest

**Task:** T05.17 — Author E12 eval body per OQ-2 resolution
**Deliverable:** D-0096
**Date:** 2026-05-20

## Files

| File | What it proves | AC mapped |
|---|---|---|
| `describe-E12.txt` | `superclaude eval describe --suite real --eval E12` renders the OQ-2-frozen body (title `"Hook deploy idempotency"`, category `hook-lifecycle`, 1 input, 7 expects, `timeout_sec: 60`, `no_pty: skip`). | AC: "File `suites/real.yaml` contains entry `id: E12` matching the OQ-2 resolution"; AC: "`TASKLIST_ROOT/artifacts/D-0096/spec.md` records the eval body summary" (cross-link). |
| `list-default.txt` | `superclaude eval list` enumerates suite `real (version 1.0, 17 evals)` — the suite continues to load cleanly after the E12 body landed (schema validation passes; no parse error). | AC: implicit — schema validity is a precondition for the suite enumerating at all. |
| `list-with-E12.txt` | `superclaude eval list --json` confirms the eval count is still 17 (E1-E15 with E2 parameterized to E2.1-E2.3). The E12 body change did not break suite-wide loading. | AC: implicit — the post-OQ-2 17-eval roster is intact. |
| `expect-roundtrip.txt` | Python round-trip of each E12 `expects[]` row through `Expect.from_mapping`. Six `settings_json` rows + one `exit_code` row all resolve to valid `ExpectCallable`s. Suite-wide enumeration shows E12 listed with the new title "Hook deploy idempotency" and `requires=[]`. | AC: "Eval body runs against a freshly-isolated per-eval HOME (per FR-ISO2) and does not read/write outside `EvalContext.scratch_root`" — the `settings_json` primitive resolves `path: settings.json` against `EvalContext.home_path` per `expect.py:383-387`. |

## Out-of-scope (deferred / blocked)

- `superclaude eval run --suite real --eval E12` 3-run determinism proof — blocked on `commands.py:1418` `NameError: name '_new_run_id' is not defined`. Same blocker documented in T05.03..T05.16 evidence blocks. Responsibility of the runner-completion task (Phase-5 dependency of CP-P05-T13-T17 at T05.18).
- "Twice in a row + digest unchanged" strict idempotency form (the dominant PR #49 regression class) — deferred per D-0096 spec.md §8.1 to a follow-up task gated on the YAML `callback:` escape hatch (D-4) landing in the schema, or a future `Expect.file.digest_unchanged_after:` primitive.

See D-0096 spec.md §8 + §8.1 for full deferral rationale and inheritance from T05.07..T05.16 posture.
