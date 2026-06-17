# Refactor Plan — How A is grafted into the merged spec

Base = Proposal A. Apply these grafts to produce `merged-requirements.md`.

## From B (sonnet:analyzer) — determinism + reproducibility engine
- **G-B1** Add `normalized_observation_digest` to the per-run schema; require the 3 digests per test to
  be byte-identical → introduce `DISAGREE` test status + `cross_run_disagreement` suite-failure class.
- **G-B2** Add determinism hygiene to ALL probes: `LC_ALL=C` + `--sort path` on every `rg`; capture
  `stdout_sha256`/`stderr_sha256`; exclude volatile fields (run_id, timestamps, durations, artifact_dir)
  from the digest.
- **G-B3** Label each acceptance criterion `class: DETERMINISTIC | JUDGMENT`; report a per-test and
  suite-wide **judgment fraction**; keep judgment criteria ≤ 2 across the whole suite, each anchored to
  a quoted token.
- **G-B4** Adopt B's `suite_failure_class` enum: `none | missing_artifact | schema_invalid | run_failed | cross_run_disagreement`.
- **G-B5** Fold B's extra E4 coverage in: incident-report rebind to `report_path (REPORT.md)` /
  `audit_log_path (audit.log)`; report-template asymmetric-cost rendering rules (`Files that MUST NOT change`).

## From C (haiku:devops) — orchestration + audit operability
- **G-C1** Adopt the 2-file per-run evidence split: `verdict.yaml` (machine) + `findings.md` (human).
- **G-C2** Adopt the orchestration plan: 4 sequential batches × 3 parallel runs (single parallel
  message per batch); a dedicated **aggregator subagent** after all 12 land.
- **G-C3** Adopt `roll-up.yaml` (machine) + `dashboard.md` (4×3 PASS/FAIL matrix + GREEN/RED gate).
- **G-C4** Adopt idempotency: append-only evidence root; re-run → new timestamped root, never overwrite.
- **G-C5** Adopt cost guardrails: ~2K tokens/run, ~27K total; 5-min per-subagent timeout; fail-fast
  within a run (record FAIL + first-failure context).

## Retained from A (base) — unchanged
- The 4-test structure, scopes, explicit ignore-list (generic "forensic" in unrelated skills out of scope).
- Falsification criteria per test (E1 sweep-liveness, E2 no-field-leak, E3/E4 `FIX_TOTAL==FIX_PROHIBITION`,
  E4 no-backend-token-in-freeze + baseline-self-consistency).
- The deliberate E3∩E4 `--fix` overlap.
- Strict 12/12; split → INDETERMINATE + human-halt; unanimous FAIL → MIGRATION_NOT_VALIDATED.
- Re-derivation-free audit trail principle.

## Net effect
A's exhaustive, falsification-anchored spec body, executed under B's determinism/reproducibility engine,
wrapped in C's CI-style orchestration + dashboard. Zero criteria dropped; coverage is the UNION.
