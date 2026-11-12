# Behaviour definitions

| # | Primitive | Asserted behaviour | Defining artifact | Fetch query | Status |
|---|---|---|---|---|---|
| 1 | `orca worktree create` (Orca runtime) | creates the worktree and seeds a first terminal with no startup command when the create carries no agent | /home/coder/workspaces/IronOrca/src/main/runtime/runtime-local-worktree-terminal-startup.ts:202-214, :259-269 and src/shared/worktree-first-surface.ts:2-14 (function bodies) | the code that implements "seeds a first terminal with no startup command when the create carries no agent" | fetched:local-source (IronOrca checkout, read 2026-11-08T01:58Z; pasted in tier1-observation.md ## Behaviour definitions). Also observed directly this run (tier1-observation.md N8, M-SEED). Installed-binary equality with the checkout not proven; installed help (N2) states the same default. |
