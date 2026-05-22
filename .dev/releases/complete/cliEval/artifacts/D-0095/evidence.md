# D-0095 — Evidence Pointer

**Deliverable ID:** D-0095
**Task ID:** T05.16 (Phase 5)
**Date:** 2026-05-21

Evidence artifacts for T05.16 live under
`TASKLIST_ROOT/evidence/T05.16/` (= `.dev/releases/current/cliEval/evidence/T05.16/`).

See `evidence/T05.16/README.md` for the manifest + AC mapping.

## Quick links

- `evidence/T05.16/describe-E11.txt` — `eval describe --suite real --eval E11` output (proves OQ-2 body rendered by CLI)
- `evidence/T05.16/list-with-E11.txt` — `eval list --json` output (proves suite enumerates 17 evals)
- `evidence/T05.16/list-default.txt` — `eval list` plain output (sibling sanity check)
- `evidence/T05.16/expect-roundtrip.txt` — Python round-trip of each `expects[]` row through `Expect.from_mapping`

## Out-of-scope (deferred to runner-completion task)

- Full `eval run --eval E11` PTY execution + 3-run determinism proof
- `freshness-subagent-stop.sh` telemetry update so the script emits
  to `logs/freshness.jsonl` with the OQ-2 field name
  (`type:"subagent_stop"`)
- Strict declarative form of the start/stop symmetry predicate
  (`event_count(subagent_start) == event_count(subagent_stop)`)

See D-0095 spec.md §8 + §8.1 and §3 footnote for full deferral
rationale and inheritance from T05.07..T05.15 posture.
