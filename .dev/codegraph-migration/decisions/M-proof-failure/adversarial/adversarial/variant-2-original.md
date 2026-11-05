# Option B: issue only

- No branch, no PR. Open (or comment on, idempotently by title) one issue "codegraph vX.Y.Z bump failed: <stage>" with the run URL, the stage, the proof log tail and the commands to reproduce locally.
- Rationale: nothing mergeable is ever created from failed or unverified bytes; issues notify the owner.
- Cost: the reviewer has no diff to inspect or push fixes onto (for example a needed `MCP_TOOLS` change); they must re-run the script by hand.
