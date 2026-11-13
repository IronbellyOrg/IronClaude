# Panel notes (shadow)

## Identity (step 9)
identity_source: requested-pinned (adapter knows only the model it asked for)
- reviewer-1 (t1b-1): self-report "claude-gw-tier1b (1M context)" — matches pin (sonnet slot alias).
- reviewer-2 (t4-1): self-report "GPT-5.2" — pin was haiku-class claude-gw-tier2. identity_mismatch_suspected: true. Self-reports are not authoritative; recorded, not asserted.
- reviewer-3 (t1a-1): pending.

## Judge
judge_identity: unknown until sc-adversarial return contract read (step 7); judge_class_collision: unknown, never false.

## Misc
panel_parity: true (resolution personas/classes match legacy rotation exactly).
anchor: template @reflect-pre anchor slot t1b resolved fixed-strategy; not replaced (anchor_replaced: false).

## Identity (final, step 9)
- reviewer-3 (t1a-1): self-report "claude-gw-tier1a (Claude Opus-class)" — matches pin (opus slot alias).
Final: reviewer-1 match, reviewer-2 MISMATCH (recorded, not asserted), reviewer-3 match. identity_mismatch_suspected: true (1 of 3, requested-pinned source). Second consecutive run with a non-Anthropic self-report on the haiku-slot pattern (shadow06 recorded the same).

## Judge (step 7, final)
Judge was the inline orchestrator of this reflect session (sonnet class). judge_identity recorded; judge_class_collision: true with reviewer-1 (sonnet slot). sc-adversarial's return contract names no separate judge record in this configuration, so collision with reviewers is recorded rather than unknown.

## Parity (step 2)
panel_parity: true — resolution (t1b/analyzer, t4/qa, t1a/refactorer) matches the legacy rotation (sonnet/analyzer, haiku/qa, opus/refactorer) exactly; card headers carry persona/model_class/model for aggregator recompute.

## Fallbacks
None: no panel_fallback_reason (D4 unused); anchor t1b resolved fixed, not replaced (anchor_replaced: false); N_eff=3.
