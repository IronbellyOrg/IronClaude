# Runtime Entrypoint Card

## Boundary and replay

producer: swarm CLI run_cmd and _run_resume_branch
transformers: preflight/spec decoding -> stub worker dispatch -> normalize -> reduce contract -> terminal-state persistence
consumer_or_evaluator: external filesystem marker-presence oracle, followed by JSON status/path validation when a marker exists
boundary_crossed: real CLI process -> persisted output artifacts
replay_command: exact uv/stub foreground and separate resume commands in tier1-observation.md:10-37
production_boundary_reach_proof: artifacts/import-paths.txt binds imported modules to this worktree; raw stdout, real contracts, state files and direct filesystem captures are retained. Stub substitutes paid worker responses, not completion persistence.
external_outcome_asserted: after exit0 and terminal success contract, default-on completion must leave done.json next to contract. Observed false on both real paths.

## Witnesses

forbidden_interpretation: successful worker/helper tests or a terminal-state file alone establish completion-marker publication.
negative_witness_command: run actual foreground CLI with stub transport and fresh output, then the read-only Path.is_file assertion recorded in artifacts/negative-witness.txt.
negative_witness_result: FAIL, assertion exit1: completion marker missing after real foreground CLI success.
accepted_substitute_rationale: captured pre-fix replay is a listed accepted negative-witness class. No literal revert is needed because the source is still unmodified and the defect remains present. Original output roots preserved.
positive_witness_command: NOT RUN; requires a separately authorized implementation and the same real CLI plus marker JSON/status/path/order assertions.
positive_witness_result: NOT PROVEN. Existing25 passing tests exercise old expectations and helper writes, not repaired CLI marker publication.

## Verdict

HC1: FAIL under this run's conservative interpretation of the positive-witness schema/pairing requirement. The negative production-boundary witness exists, but no fix-applied positive witness or repaired ordering proof exists. This is a repair-closure blocker, not doubt about observed marker absence. The ref defines no pending diagnostic state before a fix; treating pre-fix positive evidence as rationalized N/A/advisory is an acknowledged alternative, not an interpretation this run silently adopts. Ordinary hardening FAIL is not explicitly mapped to diagnostic reportstatus blocked by the contract; that report disposition is this run's conservative choice. No missing probe is silently waived; waiver_status remains none. No product fix was applied.
