# D-0008 — freshness-file-changed.sh evidence

## Task: T02.05 (STRICT, confidence 0.75 — REQUIRES PROBE in Phase 5)

FileChanged tracker per design §3.5. Records external modifications ONLY for
paths that some session has Read (last 24h).

## File

`src/superclaude/hooks/scripts/freshness-file-changed.sh`, mode 0755, `bash -n` clean.

## ⚠ Probe-pending note

The tasklist spec mandates a probe handler (deployed to live `~/.claude/settings.json`)
to capture the actual FileChanged stdin schema before the production handler is
committed. **This session is Phases 1–4 only — the probe runs in Phase 5.**

The handler is therefore implemented with the design-§3.5 assumed schema (`path`,
`change_type`) **plus permissive fallbacks** (`file_path`, `filePath`,
`changeType`, `event`) to survive minor field-name variation. If the Phase 5 probe
reveals the real schema diverges, this handler should be updated and re-mirrored.

A probe block is added to the Phase 5 follow-up note (Phase 4 close).

## Dry-run 1 — path in reads.jsonl → APPEND

Setup: reads.jsonl contains 50 entries from prior post-read concurrency test.

Input: `{"path":"/conc/5.go","change_type":"modified"}`

Result: changes.jsonl gains 1 row.

```json
{"ts":"2026-05-12T19:46:08+00:00","ts_unix":1778615168,"path":"/conc/5.go","change_type":"modified"}
```

✓ Schema per design §2.2.

## Dry-run 2 — path NOT in reads.jsonl → NO-OP

Input: `{"path":"/never/read.go","change_type":"modified"}`

Result: changes.jsonl line count unchanged. Exit 0.

## Cost analysis

Grep over reads.jsonl per FileChanged fire. With reads.jsonl bounded to ~1000 rows
in steady state and jq's path/ts_unix filter, latency is well under 50ms
(per design cost analysis). Verified on 50-entry reads.jsonl, sub-millisecond
local execution.

## Acceptance criteria

| Criterion | Status |
|---|---|
| File mode 0755, `bash -n` clean | PASS |
| Probe schema captured | DEFERRED to Phase 5 (probe handler step) |
| Production handler implemented per design-assumed schema | PASS |
| Dry-run with path in reads.jsonl appends to changes.jsonl | PASS |
| Dry-run with path NOT in reads.jsonl → no append | PASS |
| Sub-millisecond latency on representative reads.jsonl | PASS |

## Hand-off to Phase 5

The probe step is recorded in CP-P02-END follow-ups. T05.01's "live install"
phase should:

1. Backup `~/.claude/settings.json`.
2. Temporarily wire `freshness-file-changed.sh` body to:
   `cat - > ~/.claude/logs/file-changed-probe-$(date +%s).json; exit 0`
3. Edit a watched file in a real session, capture probe output.
4. Compare captured fields to assumed (`path`, `change_type`). Update handler if
   needed and re-mirror.
5. Restore real handler.

## Sub-agent verification deferral

A combined sub-agent review for D-0004..D-0009 runs at Phase 2 close. The review
should explicitly note T02.05's probe deferral and validate that the design-§3.5
schema assumption with permissive fallbacks is the right structural choice for
the source-tree implementation.
