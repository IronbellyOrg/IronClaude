# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | Each repo's config gets its own state_dir, so lock, store and DISABLED never collide | UNADDRESSED | HIGH | cycle.py:259-266: an absent `state_dir` falls back to one XDG path, so a generated config that omits the key makes two repos share one lock and `dispatch.json`; issue numbers are not repo-qualified |
| INV-002 | state_variables | One account-level rate wait at loop level is enough | UNADDRESSED | MEDIUM | cycle.py:748-750, 757-761: the child stores its own `next_permitted_at`; the loop must learn the child's reason; `gh api user` (REST) and Project lookups (GraphQL) are separate buckets |
| INV-003 | guard_conditions | The origin guard works once the repo is threaded from config | UNADDRESSED | HIGH | launch.py:50, 249; cycle.py:721, 1075: `check_origin` runs every cycle and before launch; each repo's Coordinator worktree origin must match its repo name |
| INV-004 | guard_conditions | The launch prompt carries enough to target the right repo | UNADDRESSED | MEDIUM | launch.py:92, 110: the prompt is `/sc:issue --claim <n> --pipeline none` with no repo; the target is the origin of `--worktree`; a wrong worktree sends the claim to the wrong repo |
| INV-005 | count_divergence | MAX_LAUNCHES_PER_CYCLE=1 becomes global per sweep | UNADDRESSED | MEDIUM | cycle.py:35, 36: a per-process constant; a global cap needs the loop to parse each child's result; a fixed repo order lets an early repo take the slot every sweep |
| INV-006 | count_divergence | A 270 s loop cap fits the 240 s per-cycle deadline | UNADDRESSED | MEDIUM | cycle.py:41 (240 s), 120 s launch cutoff, 1091-1099: a kill timer shorter than the child's deadline can kill it between `mark_pending` and launch; the child timeout must exceed 240 s and repo order must rotate |
| INV-007 | collection_boundaries | Every repo in `orca repo list` is a valid watch target | UNADDRESSED | MEDIUM | requirements.md lists six repos including a temporary test repo; `projectsV2(first:10)` can return zero, one or several Projects; a wrong `project_id` makes `predicates.project_check` (cycle.py:958) reject every issue |
| INV-008 | collection_boundaries | Zero repos exits 0 | UNADDRESSED | LOW | an Orca failure or timeout from `orca repo list` looks the same as an empty list |
| INV-009 | interaction_effects | Threading `REPO` is a config-to-module change only | ADDRESSED | LOW | github.py:37, 186-187, 208, 259 are scoped by the constant, so threading scopes them |
| INV-010 | interaction_effects | The two labels exist when a cycle runs | UNADDRESSED | HIGH | requirements R11; a missing trigger label gives an empty list and `predicates.py:224-225` treats a missing trigger event as "cannot pass": a silent clean run with no launch |
| INV-011 | interaction_effects | `enabled` stays a per-repo switch | UNADDRESSED | LOW | cycle.py:685-686: a generated config starts `enabled: false`; silent until the owner flips it, which contradicts "works with no setup" |
| INV-012 | sufficiency_challenge | The loop design alone gives a watcher that starts and works with no setup | UNADDRESSED | HIGH | falsified by gates outside it: R6 no scheduler; R10 no worktree (`worktree_invalid`, cycle.py:373-375); R9 no coordinator to act on a `--pipeline none` claim; R11 labels; INV-003 origin check |

## Summary

- **Total findings**: 12
- **ADDRESSED**: 1
- **UNADDRESSED**: 11
  - HIGH: 4 (INV-001, INV-003, INV-010, INV-012)
  - MEDIUM: 5 (INV-002, INV-004, INV-005, INV-006, INV-007)
  - LOW: 2 (INV-008, INV-011)
