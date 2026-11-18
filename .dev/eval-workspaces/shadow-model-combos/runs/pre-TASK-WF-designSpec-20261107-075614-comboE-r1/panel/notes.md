# Panel notes (shadow)
- findings_block_compliance_rate 1.0: all three cards parsed valid on the first parse (coverage.json had an entry per card); no re-ask needed.
- Valid blocks after re-ask: 3 of 3.
- calibration_coverage 23/23 (bare indented `calibration:` mapping in panel/cards works; no fenced yaml needed).
- Identity: identity_source requested-pinned. Self-reports differ from the pins on all 3 cards (reviewer-1 claude-haiku-5-5 vs pin claude-sonnet-5-5; reviewer-2 gpt-6-luna vs pin claude-haiku-5-5; reviewer-3 claude-gw-tier4 vs pin claude-opus-5-5): identity_mismatch_suspected true. No claim of verified independence.
- Judge: claude-gw-tier1b[1m] (orchestrator model), not a reviewer pin, not Fable, not Tier 0; judge_class_collision false.
- panel_parity true (resolution classes sonnet, haiku, opus equal the legacy rotation); `review panel resolve` has no reviewer-count option, so D5 is not applied there.
- Shadow runs do not alter the legacy verdict.
