# D-0096 — Evidence Pointer

**Deliverable ID:** D-0096
**Task ID:** T05.17 (Phase 5)
**Date:** 2026-05-20

Evidence artifacts for T05.17 live under
`TASKLIST_ROOT/evidence/T05.17/` (= `.dev/releases/current/cliEval/evidence/T05.17/`).

## Quick links

- `evidence/T05.17/describe-E12.txt` — `eval describe --suite real --eval E12` output (proves OQ-2 body rendered by CLI)
- `evidence/T05.17/list-with-E12.txt` — `eval list --json` output (proves suite enumerates 17 evals)
- `evidence/T05.17/list-default.txt` — `eval list` plain output (sibling sanity check)
- `evidence/T05.17/expect-roundtrip.txt` — Python round-trip of each `expects[]` row through `Expect.from_mapping`

## Out-of-scope (deferred to runner-completion + escape-hatch tasks)

- Full `eval run --eval E12` PTY execution + 3-run determinism proof — blocked on `commands.py:1418` `NameError` (runner-completion task downstream of T05.17).
- "Second deploy + digest unchanged" idempotency strict form — deferred per spec.md §8.1 to a follow-up task gated on either the YAML `callback:` escape hatch (D-4) being added to the schema, or a future `Expect.file.digest_unchanged_after:` primitive. The currently landed body asserts the registration-presence half of the OQ-2 contract via six `Expect.settings_json(key_path=hooks.<event>, exists=true)` rows, which is necessary but not sufficient for the PR #49 regression class.

See D-0096 spec.md §8 + §8.1 for full deferral rationale and
inheritance from T05.07..T05.16 posture.
