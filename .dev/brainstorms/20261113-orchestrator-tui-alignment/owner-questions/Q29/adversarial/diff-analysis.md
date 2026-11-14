# Diff Analysis: owner-answer proposal comparison (Q29, how the sweep command reaches this host's CLI)

## Metadata
- Generated: 2026-11-14T02:05Z
- Variants compared: 3 (V1 = proposal-A, owner-approved user-level reinstall at the merge commit; V2 = proposal-B, Coder template update; V3 = proposal-C, decide later, duty not runnable)
- Total differences found: 15
- Categories: structural (1), content (4), contradictions (3), unique (3), shared assumptions (4: UNSTATED 2, STATED 2)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Section set | five sections, 4 steps | five sections, 4 steps | five sections, 4 steps | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Delivery route | user-level `uv tool install --force` at the merge commit | Coder pin bump, image rebuild, template push, workspace update | none chosen; re-ask before XC-04 | High |
| C-002 | Time from merge to SWEEP-RUNNABLE | minutes | up to a day plus a Coder PR, build and workspace update | unbounded | Medium |
| C-003 | Effect on other workspaces | none (this host only; drift) | all workspaces get the same pin | none | Medium |
| C-004 | Effect on running sessions | none | a workspace update may end running sessions (UNVERIFIED) | none | Medium |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Owner rule "updates reach workspaces only through the Coder template" (owner memory 2026-11-12) | needs an explicit exception | follows it | follows it by not acting | High |
| X-002 | Does the template route alone make the coordinator's CLI change on this host? | no: V1 relies on the shadowing user-level install | V2's own risk section says no, unless the user-level install is removed | V3 says the gate may never pass on its own | High |
| X-003 | Provenance of what the coordinator runs | a user-chosen commit on one host | the reviewed, pinned, image-built commit | unchanged | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Pin the reinstall to the merge commit, never a branch | Medium |
| U-002 | V2 | `workflow_dispatch` on the Coder monitor removes the up-to-a-day wait | Medium |
| U-003 | V3 | If the template delivers on its own, the gate passes without a decision | Low |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | The coordinator's environment resolves `superclaude` through the same `PATH` as this worker's shell (`~/.local/bin` first, observed 2026-11-14). A session started by Orca or ccsession could have a different `PATH` | all three reason from the observed `PATH` | High (state, L3) | UNSTATED, promoted |
| A-002 | Removing or replacing the user-level install is safe: nothing else on this host depends on `~/.local/bin/superclaude` or `ic` at `d2d8a2d16` (the receipt lists entry points `ic` and `superclaude`) | V1 replaces it; V2 needs it removed | Medium (state, L3) | UNSTATED, promoted |
| A-003 | Neither `superclaude install` nor `make sync-dev` upgrades the CLI (`merged-requirements.md:1154`) | all | Medium | STATED, not promoted |
| A-004 | The `/sc:sweep` fallback to `uv run` does not trigger on "No such command" (`sc-sweep-protocol/SKILL.md` step 2) | all | Medium | STATED, not promoted |

## Summary
- Total structural differences: 1
- Total content differences: 4
- Total contradictions: 3
- Total unique contributions: 3
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, X-001, X-002, A-001
- Taxonomy tags: S-001 L1; C-001, C-002, C-003, C-004, X-001, X-003 L2; X-002, A-001, A-002 L3
- Diff points debated: S-001, C-001 to C-004, X-001 to X-003, A-001, A-002 (10)
