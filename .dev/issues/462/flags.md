# Flags decision

- Decided by: issue-worker-t2
- Depth: quick

| Field | Value | Reason |
|---|---|---|
| Mode | bug | The user reports unwanted Opus defaults in spawned sessions and asks to investigate and correct them toward Tier1b; the observation is not a verified root cause. |
| Type | core | Default model selection across orchestrator-spawned sessions is cross-cutting framework behavior; the description and scout do not establish a single command, skill, agent, or CLI as the owner. |
| Complexity | simple | follows depth (quick = simple, standard = medium, deep = complex); this is the command-depth classification, not an estimate of engineering scope. |
