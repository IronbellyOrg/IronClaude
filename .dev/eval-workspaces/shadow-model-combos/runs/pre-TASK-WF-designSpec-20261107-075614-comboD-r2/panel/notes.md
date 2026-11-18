# Panel notes (shadow, comboD-r2)

- Findings blocks: 3 of 3 valid on first parse (19 findings); no re-ask needed; valid blocks after re-ask: 3.
- Reviewer 1's findings block, as returned through the task notification, showed `&lt;` in one quote; written to the card as `<` (transport escape, not a reviewer edit of meaning). Reviewer 2's 8 quote-not-found flags are backtick-stripped quotes.
- Identity: requested-pinned. Reviewer 3 self-reported gpt-6-luna against the pin claude-opus-5-5 (this run's opus alias is gpt-6-luna), so a mismatch is suspected; no verified-independence claim is made.
- Judge: the orchestrator (claude-gw-tier1b[1m], sonnet class) judged inline; it collides with reviewer 1's class (judge_class_collision true). The installed sc-adversarial return contract names no judge; recorded as the orchestrator value above.
- Cluster command: findings with empty refs and equal fingerprints (reviewer-1 F1, F3-F7 and reviewer-3 F1) were placed in one cluster (C1); cluster_agreement 0.3357 is telemetry only.
- Calibration coverage 19/19 (fenced yaml per_finding blocks parsed).
- Dual-pass position-bias check in sc-adversarial was not run as two independent evaluations (fallback_mode true).
- Not measured: per-wave durations and token usage.
