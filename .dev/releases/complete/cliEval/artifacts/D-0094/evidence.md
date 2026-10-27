# D-0094 — Evidence Pointer

**Deliverable ID:** D-0094
**Task ID:** T05.15 (Phase 5)
**Date:** 2026-05-20

Evidence artifacts for T05.15 live under
`TASKLIST_ROOT/evidence/T05.15/` (= `.dev/releases/current/cliEval/evidence/T05.15/`).

See `evidence/T05.15/README.md` for the manifest + AC mapping.

## Quick links

- `evidence/T05.15/describe-E10.txt` — `eval describe --suite real --eval E10` output (proves OQ-2 body rendered by CLI)
- `evidence/T05.15/list-with-E10.txt` — `eval list --json` output (proves suite enumerates 17 evals)
- `evidence/T05.15/list-default.txt` — `eval list` plain output (sibling sanity check)
- `evidence/T05.15/expect-roundtrip.txt` — Python round-trip of each `expects[]` row through `Expect.from_mapping`

## Out-of-scope (deferred to runner-completion task)

- Full `eval run --eval E10` PTY execution + 3-run determinism proof
- `freshness-subagent-start.sh` telemetry update so the script emits
  to `logs/freshness.jsonl` with the OQ-2 field name
  (`type:"subagent_start"`)

See D-0094 spec.md §8 + §8.1 for full deferral rationale and
inheritance from T05.07..T05.14 posture.
