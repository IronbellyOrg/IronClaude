# Position B: Turn the main session into an Orca orchestrator

## Claim
Refactor /sc:brainstorm so the main session only runs Wave 0, the Socratic dialogue (Wave 1), agent-spec composition (Wave 2B), merge gating and handoff, and dispatches enrichment (S1) and proposal generation and advocacy (S2, S3, and later S4) as separate supervised Orca workers. Keep Task dispatch as a fallback when Orca is unavailable.

## Case
1. **Real model diversity.** Today the "multi-model" brainstorm is opus, sonnet and haiku: one vendor, one training lineage, correlated blind spots. `orca orchestration worker-start --agent codex|cursor|opencode --model <id>` runs different model families. Debate value depends on variants disagreeing for real reasons.
2. **Context isolation and survival.** Sub-agent results flow back into the parent's context; a deep run (up to 7 proposals, up to 500K tokens estimated) pushes the parent toward compaction, which is exactly when the protocol's state (domain, strategy, enrichment tiers, agent-spec) is at risk. Workers write files; the orchestrator holds only paths and the return contract. This matches the repo's own rule that cross-agent transfer happens through on-disk artifacts.
3. **Observability and control.** Orca shows each worker live; the user can read, stop (`worker-stop`), retry (`--retry-of`) or steer one worker without killing the run. A Task call is a black box until it returns, and S2 to S3 failures today can only be retried whole.
4. **Resumability.** A worker is a separate process that survives parent crash, so `--resume-from` can reattach to finished proposals instead of regenerating them.
5. **Full tools per proposer.** A proposer worker can run its own codebase search and research while writing its proposal, instead of consuming a pre-digested 30K-token enrichment summary. S1 and S2 could merge into one worker per persona.
6. **Scoped delivery.** Do it in stages: first S2 (variant generation only) behind `--runtime orca`, default stays Task. No change to scoring, merge or return contract. Ship S3 and S1 only if S2 proves out.

## Mitigation of known costs
- Fallback to Task when `orca --version` fails or the session is not in an Orca worktree.
- Worker contract: prompt file in, one result file out, `worker_done` signal; the orchestrator verifies the file on disk (repo rule: never trust the delivery signal alone).
- Token accounting: read transcript size or count words as an estimate; accept coarser telemetry for the Orca path.
