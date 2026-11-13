first_parse_valid: reviewer-1=true reviewer-2=false(citation path typo, fixed same run) reviewer-3=true => rate 2/3 = 0.667

- cluster_agreement: 0.3207 (telemetry only)
- calibration_coverage: 21/21
- precheck: 42 checked, 1 quote-not-found (rv1 F5 ellipsis-abbreviated quote; full text confirmed on plan:137 by orchestrator Read; joins EV reread set)
- snapshot path prefix + --root mapping fixed (input/ prefix vs bare filenames; root=.dev/eval-workspaces/shadow-model-combos)
debate_skipped_similar=false; judge_identity=claude-gw-tier3[1m] (distinct from all 3 debater classes); judge_class_collision=false
- identity_source: requested-pinned (no observed model ids read from transcripts; no independence claim made)
- identity_mismatch_suspected: false (no self-reports collected)
- findings_block_compliance_rate: 0.667 first-parse (2/3; rv2 card had one citation-path typo fixed same run, no re-ask needed)
- review of runs 1-3: no card-write corruption this run (readback clean)
