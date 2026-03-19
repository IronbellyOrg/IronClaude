Roadmap written to `.dev/releases/current/v3.0_unified-audit-gating/eval-runs/global-B/roadmap.md`.

**Summary**: 5-phase plan for adding pipeline progress reporting to `superclaude roadmap run`:

1. **Phase 1** — Data models + atomic writer in new `progress.py`
2. **Phase 2** — `--progress-file` CLI option + gate `summary()` method (parallelizable)
3. **Phase 3** — Wire reporter into `execute_pipeline()` callback
4. **Phase 4** — Dry-run gate summary table
5. **Phase 5** — Advanced metadata for deviation/remediation/wiring steps

Key risks are the two unresolved spec gaps (deviation sub-entry schema, remediation trigger threshold) which block Phase 5. Total effort ~5.5 units with critical path of ~4.5 units via parallelism.
