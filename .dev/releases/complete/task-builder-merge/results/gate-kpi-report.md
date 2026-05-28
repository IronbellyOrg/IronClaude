## Gate & Remediation KPI Report

> **NOTE — Manual reconstruction.** The original v3.9 sprint executor did
> not persist its in-memory `gate_results` / `remediation_log` /
> `turn_ledger` to disk; the regenerated artifact below draws gate-pass
> counts from checkpoint verdicts (`checkpoints/CP-P0[2-7]-*.md`) and
> turn aggregates from per-phase stream-json `result` events. Latency
> percentiles and remediation telemetry are unrecoverable and shown as
> `N/A (data not persisted)`. Reconstructed 2026-05-19 from
> `execution-log.jsonl` + `results/phase-N-output.txt`.

### Gate Evaluation (derived from checkpoint verdicts)

  Total evaluated:   21  (18 regular tasks T07.01–T07.20 + 3 mid-checkpoints T07.06/T07.12/T07.18, per CP-P07-END.md §2)
  Passed:            21  (18/18 regular + 3/3 mid-checkpoints; T07.20 carries CONDITIONAL-GO sub-disposition on K-003)
  Failed:             0
  Pass rate:        100.0%
  Latency (p50):    N/A (data not persisted)
  Latency (p95):    N/A (data not persisted)

  Note: count above is Phase-7-only; full cross-phase task count is 85
  deliverables (D-0015..D-0099 + Phase-1 D-0001..D-0014). All 7 phases PASS
  per execution-log.md.

### Remediation

  Total:             N/A (data not persisted)
  Resolved:          N/A
  Pending:           N/A
  Frequency:         N/A

  Observable proxy: zero remediation events appear in any phase's
  stream-json output (errors=0 across all 6 sprint phases per the
  release retrospective).

### Conflict Review

  Reviews:           N/A (data not persisted)
  Conflicts found:   N/A
  Conflict rate:     N/A

### Wiring Gate

  Findings total:    N/A (data not persisted)
  Findings by type:  N/A

  Source: `wiring-verification.md` is present at release root; consult
  it for the historical wiring-gate posture across the 6 FR-CONV.X land
  commits.

### Sprint Aggregates (from execution-log.jsonl + stream-json)

  Phases:            6 (2..7; Phase 1 ran out-of-sprint as M1 ratification)
  Sprint outcome:    success
  Total duration:    24h 28m (2026-05-17T15:42:30Z → 2026-05-18T16:11:10Z)
  Total turns:       125 (sum of `num_turns` from phase-N result events)
  Total input tokens:    890,859 (incl. cache_creation_input_tokens)
  Total output tokens:    94,544
  Phases passed:     6 / 6

### Checkpoint Manifest

  Total:            21 (3 per phase across phases 1..7)
  Found on disk:    18 (all phases 2..7 mid + END checkpoints)
  Missing on disk:   3 (Phase 1: CP-P01-T01-T05, CP-P01-T07-T11, CP-P01-END
                       — Phase 1 was the out-of-sprint M1 ratification
                       phase; its checkpoints were never produced under
                       this release dir)

### K-003 Audit Window (single inscribed contingency on v3.9 tag)

  Runs captured:     3 of 5  (TRACKING-PASS at tag time)
  Self-Audit cov.:   100% across all 3 captured runs
  Semantic checks:   4 / 4 / 13 (≥1 floor, see D-0083 §2.3-§2.4)
  SLA:               OPS-001 4-business-hour window
  Window expiry:     2026-08-21 (M7 phase end)
  Trajectory:        FINAL-PASS-likely on 4/4/13 evidence
  FAIL action:       release-spec §19.4 rollback (tag-message inscribed)
