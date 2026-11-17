# Panel notes (shadow, combo D)

- findings_block_compliance_rate: 3/3 reviewer cards valid on first parse (no re-ask needed).
- calibration_coverage: 15/15 (cluster command output). Calibrator ran as claude-gw-tier1b (Sonnet class, self-report) for all three cards and the T1 card; reviewers: sonnet (tier1b), haiku (claude-haiku-5-5), opus slot (gpt-6-luna, self-report). Calibrator class equals reviewer 1 class: calibrator_diversity degraded.
- cluster_agreement: 0.1429 (telemetry only). Pre-check: 40 citations checked, 40 flagged unresolved because input-snapshot.yaml stores bare file names (source.md, TASK-...md) while the cards cite repo-relative paths; this is a snapshot-path mismatch of the orchestrator's snapshot, not evidence that citations are wrong. The evidence-validator re-read decides.
- debate_skipped_similar: false. judge_identity: unknown (orchestrator claude-gw-tier1b scored inline; the adversarial return contract names no judge); judge_class_collision: unknown.
- identity_source: requested-pinned for panel/resolution.json (resolution says claude-opus-5-5 for the opus slot; reviewer 3 self-reports gpt-6-luna). identity_mismatch_suspected: true (card header model is the pin; the reviewer self-report differs for reviewer 3). No claim of verified independence.
- panel_parity: true on (persona, class) pairs: legacy rotation analyzer/sonnet, qa/haiku, refactorer/opus equals resolution.json order.
- executor class: unknown (no flag, env or log hint); anchor not replaced.
- adversarial advocate model: general-purpose agents on the orchestrator model (UNVERIFIED which model served them).
