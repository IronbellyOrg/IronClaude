# Panel notes (shadow07)

- identity_source: requested-pinned. Reviewer model pins come from panel/resolution.json; no transcript-level model id was observed. No claim of verified independence is made.
- identity_mismatch_suspected: true. reviewer-1 self-reports "claude-gw-tier1b (the brief pins claude-sonnet-5-5)"; reviewer-2 self-reports "claude-gw-tier1b[1m]" (pin haiku); reviewer-3 self-reports "claude-gw-tier1b" (pin opus). All three self-reports disagree with their pins, mirroring shadow02 (2/3) and shadow03 (2/3). Pattern across runs: the harness appears to serve tier1b to subagent slots regardless of pin.
- judge_identity: unknown. sc-adversarial's return contract names no judge record; judge_class_collision: unknown (never false).
- No Fable model and no Tier 0 alias was picked as reviewer or calibrator.
- card-parse incident: first cluster pass marked all 3 cards invalid — briefs' findings-block template allowed roles (repo) and categories outside the findings-v2 schema. Orchestrator remapped mechanically (repo->source/test; categories to the allowed six) and re-clustered; 8/8 findings calibrated, agreement 1.0. Root cause is the orchestrator-authored brief template, to fix in the brief line for future runs.
- panel_parity: true (resolution order sonnet/haiku/opus == legacy rotation analyzer/qa/refactorer).
