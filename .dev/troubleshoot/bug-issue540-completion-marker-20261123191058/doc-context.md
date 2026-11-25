# Documentation Context Card

**Generated**: 2026-11-23T19:16:54Z
**Wave**: 1.5
**Scope**: src/superclaude/cli/swarm

## Release context

- **Release**: MultiModelSwarm
- **Artifacts**: .dev/_rescued_worktrees/pr110/.dev/releases/Current/MultiModelSwarm/{roadmap.md,merged-requirements.compressed.md}
- **Summary**: Rescued roadmap.md:310 requires atomic marker emission last, with verdict in the contract even for partial/failed completion; requirements :128-130 orders contract then marker. No relevant top-level release artifact was found. These rescued copies are historical/advisory; current governing status is unverified.
- **Confidence**: 0.92 (branch discovery score, not diagnosis confidence).

## Architectural docs consulted

- `docs/swarm/README.md` (:96-126): current by mtime; correctly documents the existing missing-marker limitation and full foreground reduction.
- `docs/swarm/command-reference.md` (:22-26,250-273): current by mtime; describes terminal after contract, marker only from kill.
- `docs/swarm/user-guide.md` (:407-442): current by mtime; warns against normal-run marker polling.
- `docs/swarm/monitoring-patterns.md` (:6-11 versus :35-71): current by mtime; limitation banner matches observed implementation, later polling promise does not.
- `docs/swarm/observability-procedure.md` (:23-31,97-137): current by mtime; inline limitation matches implementation, detached/resume marker promises are unsupported by the traced code.
- `docs/swarm/operator-runbook.md` (:195-240): current by mtime; resume marker promise is unsupported, kill marker is separate.
- `.dev/troubleshoot/bug-readme-emits-resume-20260609/REPORT.md`: current by filesystem age only; historical dispatch-only/resume-marker account is superseded by live source and not used as authority.

Parent captured all doc mtimes near 1795451558.3 and newest component mtime 1795451558.370333. No dated stale/deprecated header markers were found. Mtime currency is not semantic correctness; source and captured runtime observations decide conflicting claims.

## Restrictions / decisions that constrain the fix

- `src/superclaude/cli/swarm/models.py:563-573` (OnCompletion): "write_done_sentinel=True" means atomic marker on terminal status; default true. Contract printing is a separate policy and not part of this issue.
- `src/superclaude/cli/swarm/commands.py:2161-2169` (foreground): terminal state follows reduction and persisted contract/bodies.
- `src/superclaude/cli/swarm/reduce.py:389-425` (existing marker writer): three fields, after terminal transition, co-located with contract, atomic helper, status copied from final contract; killed uses its own writer.
- `src/superclaude/cli/swarm/commands.py:2188-2192` (resume): do not rerun preflight or replace manifest truth with the live registry.
- `src/superclaude/cli/swarm/commands.py:1700-1705` (detached): child owns the pipeline; launching parent must not signal completion.
- `src/superclaude/cli/swarm/commands.py:2089-2090` (contract ownership): do not duplicate reduce's contract emission.
- Full extracted rows, including manifest identity and failure contract compatibility, are retained in `wave1_5-branch-C.md`.

## Re-frame signals

- This is an unimplemented completion policy, not a broken atomic writer. Current operator docs describe the limitation accurately; the issue explicitly requests implementing the source model's policy, so those descriptions do not prohibit the change.
- Updating the narrowly affected completion guidance belongs with a repaired behavior; do not change stdout policy or adjacent metadata bugs.
- Resume has a separate completion continuation, while detached launches the normal continuation in a child. Runtime reproduction here covers only successful foreground stub execution; sibling results remain source inspection, not reproduced claims.
