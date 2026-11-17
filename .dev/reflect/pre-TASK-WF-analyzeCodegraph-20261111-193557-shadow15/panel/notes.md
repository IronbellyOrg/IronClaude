# Panel notes — shadow15

## Identity (step 9)
- identity_source: requested-pinned (adapter knows only the requested model; no transcript read).
- R1 (t1b-1, pinned sonnet claude-gw-tier1b[1m]): self-report "claude-gw-tier1b" — matches pin.
- R2 (t4-1, pinned haiku claude-gw-tier2[1m]): self-report "claude-gw-tier1b[1m]" — MISMATCH.
- R3 (t1a-1, pinned opus claude-gw-tier1a[1m]): self-report "claude-gw-tier1b[1m]" — MISMATCH.
- identity_mismatch_suspected: true (2 of 3). While identity stays requested-pinned and mismatches exist, the panel makes NO claim of verified reviewer independence; the class-diversity guarantee is unverified this run.
- Hypothesis (unverified): the gateway may route several alias slots to one serving class, or reviewer self-report is unreliable. Either way effective diversity is suspect.

## Coverage.json assignment (step 6)
- Run assigned coverage rows only via brief coverage slices; R1 assigned 5 slice rows, R2 assigned 4, R3 assigned 4. Cards did not report coverage_rows fields in findings (schema allows but reviewers did not set them), so observed sets are empty; recorded honestly in panel/coverage.json.

## Judge (post-debate)
- To be recorded after Wave 4.

## Normalize + cluster (steps 4-6)
- findings_block_compliance_rate: 1.0 (3/3 valid on first parse; no re-ask needed; 10 finding lines).
- Fence-fix note: cards were first written with fence info string `json`; findings-v2 requires the fence info string `findings-v2`. Orchestrator corrected its OWN card-file writing (not reviewer content) and re-ran; first cluster pass recorded 0/0 invalid. Process lesson for briefs: the shadow brief line says "fenced findings-v2 block" — persist cards with that exact fence string.
- cluster_agreement: 1.0; calibration_coverage: 10/10 (all clustered findings matched a calibration value).
- verify-citations pre-check: checked 19, flagged 19 — all are repo-file citations (analyze.md, core/CODEGRAPH.md) outside the package-only snapshot; expected shape (shadow04: 10, shadow08: 11, here 19 because cards cite both files). All join the EV re-read set.
