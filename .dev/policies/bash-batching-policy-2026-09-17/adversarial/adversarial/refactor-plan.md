# Refactoring Plan

## Base

`POLICY.md`

## Applied Changes

1. Qualify `N=4` transcript evidence as mechanical-streak data and provisional.
2. Exempt same-turn parallel Bash fan-out.
3. Add an in-flight singleton exception for legitimately late discovery.
4. Define every interpret-before-next-action checkpoint as a sequence reset.
5. Expand write-capable exclusions and ban dynamic shell constructs.
6. State lack of snapshot isolation.
7. Require `umask 077`, `mktemp -d`, per-chunk scripts, and cleanup-failure reporting.
8. Enforce aggregate/per-command time and output caps with truncation markers.
9. Specify marker accounting and explicit `exit 0`/`exit 1`.
10. Treat transcript visibility as audit only under `bypassPermissions`; restrict unattended batches to simple commands.
11. Preserve tracked-Read requirements and apply threshold across delegated subagents.
12. Rename adoption surface to normative guidance and describe source-of-truth wiring as future work.
13. Make any future hook completion-aware and label it a mechanical proxy.
14. Define rollout denominators and separate semantic from mechanical metrics.

## Changes Not Made

- No hard-blocking fifth-call hook: it enforces a number, not safety or independence.
- No shell validator or structured runner: outside the requested artifact-only scope.
- No `/tmp` sweeper: destructive cleanup requires a separately reviewed implementation.
- No lower threshold: the sampled elbow and adaptivity cost support starting at four.

## Residual Risk

Free-form shell under unattended `bypassPermissions` remains unacceptable without validation/sandboxing. The merged policy limits the command grammar and labels the remaining gap rather than claiming closure.
