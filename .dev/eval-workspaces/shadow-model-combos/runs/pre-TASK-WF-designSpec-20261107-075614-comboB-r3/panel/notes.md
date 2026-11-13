# Panel notes (shadow, comboB-r3)

- Findings blocks: 3/3 valid on first parse (findings_block_compliance_rate 1.0); no re-ask was needed.
- Pre-check: 34 citations flagged `missing-file / not-in-snapshot` (0 out-of-range, 0 quote-not-found). Cause: the brief told reviewers to cite repo-relative paths, the snapshot lists bare names (`source.md`). Not remapped (orchestrator never edits reviewer findings); all 34 join the evidence-validator re-read set.
- Calibration coverage 11/11 (bare indented `calibration:` mapping per card).
- cluster_agreement 1.0 with 0 agreement clusters (11 single-member clusters): the same defect (resume_decision row 4, T1-F1) was reported by reviewer 1 F1 and reviewer 3 F2 but was not merged by the cluster step. Telemetry only.
- Identity: identity_source requested-pinned. reviewer-2 (haiku pin) self-reported "OpenAI GPT" -> identity_mismatch_suspected: true. reviewer-1 and reviewer-3 reports (claude-gw-tier1b, claude-gw-tier1a) are aliases of their pins, no contradiction. No claim of verified independence.
- Dispatch: all three reviewers were dispatched with explicit model classes sonnet, haiku, opus (no dispatch collapse).
- Calibrator: one confidence-calibrator (sonnet class) per card; disjoint set empty -> calibrator_diversity degraded.
