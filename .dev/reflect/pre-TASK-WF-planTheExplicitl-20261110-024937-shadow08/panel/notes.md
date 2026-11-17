# Panel notes (shadow)

## Identity (step 9)
identity_source: requested-pinned (adapter knows only the model it asked for)
- reviewer-1 (t1b-1, sonnet/analyzer): self-report "claude-gw-tier1b (sonnet-class)" — matches pin.
- reviewer-2 (t4-1, haiku/qa): self-report "claude-gw-tier1b (haiku-class model)" — pin was haiku-class claude-gw-tier4 alias via launch haiku; class matches (haiku), alias string does not (tier1b vs tier4). Recorded; identity_mismatch_suspected stays false on class comparison (the aggregator recomputes from headers).
- reviewer-3 (t1a-1, opus/refactorer): self-report "claude-gw-tier1b (opus-class)" — class matches pin (opus via claude-gw-tier1a alias); alias string differs. Same treatment as reviewer-2.
No non-Anthropic self-report this run (unlike shadow04/shadow06's haiku-slot GPT-5.2 reports). Self-reports are not authoritative; recorded, not asserted.

## Judge (step 7)
judge_identity: claude-gw-tier3[1m] (inline orchestrator of the adversarial merge, a different class than all three debaters per Khan ICML 2024 weak-judge-strong-debaters preference; not a reviewer class, not the calibrator classes used per-card). judge_class_collision: false. sc-adversarial's return contract names judge_identity explicitly this run.

## Parity (step 2)
panel_parity: true — resolution (t1b/analyzer, t4/qa, t1a/refactorer) matches the legacy rotation (sonnet/analyzer, haiku/qa, opus/refactorer) exactly; card headers carry persona/model_class/model for aggregator recompute.

## Fallbacks
None: no panel_fallback_reason (D4 unused); anchor t1b resolved fixed-strategy, not replaced (anchor_replaced: false); N_eff=3 (3 resolved, 3 complete).

## Precheck
11 citations flagged missing-file/not-in-snapshot (reviewers cited repo files outside the package-only input snapshot; same shape as shadow04's 10 flags). All 11 joined the evidence-validator re-read set; all resolved (citations_dropped: 0). cluster_agreement 1.0 (telemetry only), calibration_coverage 9/9.

## Manifest mechanics learned
`--completion` accepts only complete|truncated|invalid|failed|timed_out; per-attempt rows must be recorded BEFORE the stage advance that closes them (dispatched-attempt rows recorded after the stage advanced were rejected OutOfOrder; collected-attempt rows recorded correctly before advancing).
