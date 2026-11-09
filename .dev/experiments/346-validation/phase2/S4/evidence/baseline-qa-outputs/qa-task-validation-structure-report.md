# QA Report: task file structure and phase ordering (lens: phase-structure)

**Task file:** TASK-RESEARCH-bmad-first-use-20261107-075901.md
**Reviewer:** rf-qa agent aad68c81ea295c338 (spawned as a5eed7e7082257261 notification id); report transcribed by the orchestrator because the agent's harness forbids writing .md files. Content below is the agent's inline return, not re-derived.
**Date:** 2026-11-07
**Caveats stated by the reviewer:** frontmatter checked by eye (no yaml module); bodies of Steps 5.9-5.17 and 6.2-6.7b only skimmed.

## Findings

| # | Severity | Finding | Disposition |
|---|----------|---------|-------------|
| 1 | IMPORTANT | Step 7.2 stages `.dev/tasks` before Steps 7.3-7.5 write user-summary.md, the Task Summary and the Done status; staging must come after Step 7.5 | fix |
| 2 | IMPORTANT | Step 2.1 "OBSERVED RUN" (agent 01 runs `bmad install` in a /tmp scratch dir with a scratch HOME) contradicts the binding "read and research only" guard and the CLAUDE.md ban on one-off probes; not tied to an Open Question (TB-Add-3) | fix: strike it; use this worktree's already-installed `_bmad/` as the observed output of a real install |
| 3 | IMPORTANT | TB-Add-7: Execution Context (line 105) carries `Dockerfile.coder:133-144`; Source areas omits docs/, README.md, CHANGELOG.md, SECURITY.md, .github/workflows/ used by Steps 2.4-2.5 | fix |
| 4 | IMPORTANT | Fifteen cycle-2 items (3.10-3.12, 5.14-5.16, three each in Gates 3, 4, 5) say "EXACTLY the prompt above", breaking the B2 self-contained rule | fix: restate or reference by exact step number with the prompt text inlined |
| 5 | IMPORTANT | Gates 4 and 5 fixed at 2 agents; SKILL.md requires 3-4 when input exceeds 1000 lines (test-startup-boot.sh alone is 3061 lines); no conditional | fix: add a third agent per gate or a stated conditional |
| 6 | MINOR | `git status` guards assume the task folder is untracked | note |
| 7 | MINOR | Gate 3 prompts carry a literal "N errors"; N computed in prose at line 365 | note |
| 8 | MINOR | Verify wording mixed; Steps 1.1, 7.5, 7.6 have no verify clause | note |
| 9 | MINOR | Steps 2.1/2.2 are about 9-10 KB each; Steps 7.1 and 6.8 are composite without split justification | note |
| 10 | MINOR | Step 6.8 edits the report after all gates without re-verification; line 472 mis-cites I22 | note |
| 11 | MINOR | Task-Specific Context Files subsection and Post-Completion Actions heading missing | note |
| 12 | MINOR | Step 3.1 "three UNVERIFIED items" differs from line 129 | note |
| 13 | MINOR | Step 5.4 reads synth-01/02 "if they exist" | note |
| 14 | MINOR | Step 7.5 sets Done unconditionally | note |

## Passes (reviewer-stated)
Gate counts 3/3/7/2/2 with a single fix agent per gate and 2 cycles; item dependencies form a DAG; no TBD/TODO strays; no POST reflect gate; no Ponytail items; /tech-reference non-blocking and last; Task Log present; 89 items.

## Summary
- Blocking: 5 (IMPORTANT). Minor: 9.
- VERDICT: FAIL
