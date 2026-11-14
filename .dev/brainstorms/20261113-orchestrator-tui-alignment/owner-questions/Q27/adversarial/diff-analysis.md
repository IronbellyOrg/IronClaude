# Diff Analysis: owner-answer proposal comparison (Q27, where SW-02's plan package lives)

## Metadata
- Generated: 2026-11-14T00:45Z
- Variants compared: 3 (V1 = proposal-A, plan in the coordinator home; V2 = proposal-B, new phase in the existing sweep task package inside #539; V3 = proposal-C, new plan package committed in #539)
- Total differences found: 16
- Categories: structural (1), content (4), contradictions (3), unique (4), shared assumptions (3: UNSTATED 2, STATED 1)

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Section set | five sections, 4 steps | five sections, 4 steps | five sections, 4 steps | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Where the plan lives | Coordinator home, outside #539 | Inside #539, appended to the Done sweep task package | Inside #539, a new `/sc:workflow` package | High |
| C-002 | Executor | `/sc:implement` run from the #539 checkout on a plan in another checkout | `/task` on a reopened task file | `/sc:implement` in the same checkout | Medium |
| C-003 | Dependency on Q26 (coordinator home) | Depends: no home, no plan | None | None | High |
| C-004 | Effect on #539's file set | None from SW-02's plan | Existing package grows | One new package (a few files) | Medium |

## Contradictions

| # | Point of Conflict | V1 | V2 | V3 | Impact |
|---|-------------------|----|----|----|--------|
| X-001 | Does rule A-004 (no new program, collector, key, sidecar or program artifact in #539, `merged-requirements.md:978`) cover a plan package? | Treats it as excluded | Keeps the letter (no new package) by editing an existing one | Says a plan is none of the four things | Medium |
| X-002 | Is there a conflict between "`.dev/tasks/` always staged" and "#539 commits named paths only"? | Avoided by placing the plan elsewhere | Avoided because the package is already tracked | Removed by committing the plan | Low |
| X-003 | Routing level (`~/.claude/CLAUDE.md` workflow table) | Level 3 | Level 4 machinery without a stated need | Level 3 | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Plan sits beside the program ledger on the program branch | Low |
| U-002 | V2 | Per-phase reviewer panels for the fix | Low |
| U-003 | V3 | Measured precedent: 921 `.dev/tasks/to-do/` files already in #539 | Medium |
| U-004 | V1 | Where `/sc:implement` archives a package that lives in another checkout is UNVERIFIED | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|-----------|------------------|--------|--------|
| A-001 | The session that plans SW-02 can write into the place the plan lives. `/sc:workflow` always writes into the checkout it runs in (`sc-workflow-protocol/SKILL.md:47`). Under V1 that means a session in the coordinator home writes the plan: either the coordinator plans another session's item, or the #539 author opens a second session in the coordinator's folder (one live session per checkout, spec 6.2) | V1 and V3 both say "the #539 author" plans and executes | High (guard, L3) | UNSTATED, promoted |
| A-002 | The package's later state changes (progress ledger lines, the archive move to `done/`) happen in the same checkout as the code being changed | all three assume one executor run updates its package | Medium (state, L3) | UNSTATED, promoted |
| A-003 | SW-02 needs a written plan under the hard limit (more than one source file or more than 5 edits) | all three | Medium | STATED (question.md fact 1), not promoted |

## Summary
- Total structural differences: 1
- Total content differences: 4
- Total contradictions: 3
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-003, A-001
- Taxonomy tags: S-001 L1; C-001, C-002, C-004, X-002, X-003 L2; C-003 L2 (dependency); X-001 L3 (guard on A-004); A-001, A-002 L3
