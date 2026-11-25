# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

- Code anchors, the cooldown note for candidate fix 2, the backup-too-large exception and the existing test names, all from `origin/master` (see the issue body, Codebase Context). The worker's first draft cited an out-of-date local checkout; the orchestrator re-checked every line against `origin/master` and replaced them.
- Environment details (Linux, Claude Code 2.1.322, branch master) came from the orchestrator's task input and the session, not from the description file.

## Contradictions

- None. Two contradictions the worker reported (a missing `kind=request` audit line and a tier-3 list order mismatch) were artifacts of the out-of-date checkout; on `origin/master` the audit line exists (`local-gateway-alias-proxy.py:941`) and `MODEL-TIERS.md:43` lists GLM-5.3 then Qwen3.8 Max.
