# Flags decision

- Decided by: issue-worker-t2
- Depth: quick

| Field | Value | Reason |
|---|---|---|
| Mode | feature | The request evaluates a new sub-orchestrator or coordinator capability, rather than reporting a failure of existing behavior. It asks for an assessment before any implementation decision. |
| Type | command | The proposed user-facing capability is a mode of `/sc:orchestrator`, potentially selected with `--sub`. Reviewing the orchestration skill and related specifications supports that command-focused evaluation. |
| Complexity | simple | Follows the requested quick depth (quick = simple). This classifies the evaluation issue, not the effort of implementing the proposed orchestration capability, which is not known yet. |
