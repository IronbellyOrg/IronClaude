# Panel notes (shadow, comboB-r1)

- Findings blocks valid after the re-ask: 3 of 3 (no re-ask was needed; first-parse rate 1.0).
- Orchestrator never edited a reviewer finding; cards were written verbatim from the returned text and read back with jq.
- Parity: legacy rotation as run (sonnet analyzer, haiku qa, opus refactorer) equals panel/resolution.json (t1b-1 sonnet, t4-1 haiku, t1a-1 opus): panel_parity true.
- Identity: requested-pinned; reviewer-2 self-reports "OpenAI GPT" against the haiku pin (identity_mismatch_suspected true); executor class unknown, so no verified independence claim.
- Judge: sc-adversarial return contract names no judge; judge_identity unknown; the orchestrating session model was claude-gw-tier1b (sonnet alias), same alias as reviewer 1.
- Cluster: agreement_clusters empty in the cluster output; cluster_agreement 1.0 as printed; calibration 12/12; clusters_kept written with all 12 card findings kept by the evidence validator (it dropped one citation of the merged report, not a card finding).
- verify-citations flagged 38 of 38 as not-in-snapshot (snapshot used bare file names); joined the re-read set.
