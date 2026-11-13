# Panel notes (shadow, combo B round 2)
- findings_block_compliance_rate: 1.0 (3 of 3 cards valid on the first parse; no re-ask); valid blocks after re-ask: 3.
- calibration_coverage: 25/25 findings calibrated (cluster pass 1); 23/23 in the kept pass (two cards' unkept findings left out of --kept on purpose).
- panel_parity: true (analyzer/qa/refactorer on sonnet/haiku/opus classes, equal to panel/resolution.json).
- identity: identity_source requested-pinned; reviewer 2 (pinned claude-haiku-5-5) self-reports an OpenAI assistant => identity_mismatch_suspected true. Reviewers 1 and 3 self-report the gateway aliases claude-gw-tier1b and claude-gw-tier1a. No claim of verified independence; executor class unknown (UC-1 pre mode).
- judge_identity: unknown (the sc-adversarial return contract names no judge; the advocates, scorer and merge-executor were separate agents of classes sonnet/haiku/opus and opus). judge_class_collision: unknown.
- debate_skipped_similar: false.
- verify-citations precheck: 4 of 72 flagged on the reviewer cards (reviewer 1: 3 repo files tagged role plan are outside the snapshot, 1 quote not found at a brief-relative line). The validator re-read set was the merged-finding citations instead.
- Process incident: a script error truncated docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md to 0 bytes during the Wave 5 memory write; it was rebuilt (96 lines, 13 entries) from the frozen baseline plus the combo C, D and E entries recovered from their run logs, then this run's entry was added atomically (14 entries, 107 lines).
