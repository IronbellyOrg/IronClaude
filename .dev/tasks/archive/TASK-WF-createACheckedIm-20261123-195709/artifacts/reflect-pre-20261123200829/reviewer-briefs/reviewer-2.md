# QA review brief

## T1 card excerpt

Coverage-matrix.md records 0 parsed requirements, 12 quote-pinned inferred requirements and 4 tasks. Literal containment maps 6/12 (coverage_pct_union=0.5, S_dev_density=0.5); parsed-only coverage is null. Semantically the scope constraints are in the plan's Constraints section, which the single-task matcher excludes. No lexical mismatch is silently relabelled covered. The source's sparse labeling mandates Tier 2 regardless of confidence. Tasks 1/2 require expected red help failures and an unchanged parser guard, Task 3 corrects validate-lenses, and Task 4 corrects scaffold with final repaired-surface captures and executor-owned independent review. The historic repair blockers remain open until those future checks actually occur.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-23T20:08:34Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help

### .dev/tasks/to-do/TASK-WF-createACheckedIm-20261123-195709/source.md:1 (entire source body)

```text
Create a checked implementation plan only for issue 568, swarm help advertises unsupported --custom-prompt-dir. Source is this inline request, informed by .dev/troubleshoot/bug-swarm-custom-prompt-help-20261123191427/REPORT.md and linked transferred evidence. Preserve blocked/partial historical diagnosis and all pending verification requirements. Plan the supported two-help-description correction in src/superclaude/cli/swarm/commands.py using JobSpec custom_prompt_dir with lens custom, reproducing regression tests failing before the edit and passing afterward, corrected public help captures, rejection of unsupported run option and independent review. No new CLI flag, prompt-loading changes, inline-custom-spec changes, injection-guard or metadata changes. Work only in this isolated checkout. Do not replay counter-update.py or change diagnostic counters, implement product code/tests, run models, commit, push, interact with GitHub or create worktrees. User explicitly requests plan only, no implementation.
```

Read candidate `../../../TASK-WF-createACheckedIm-20261123-195709.md`, source `../../../source.md` and `../coverage-matrix.md`. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. This source asks for a plan whose eventual implementation will need tests; it does not authorize performing those tests now. No verification results are claimed by this pre-review.

## Coverage slice

| Requirements | Concern |
|---|---|
| INF-001, INF-004, INF-005, INF-007, INF-009, INF-010, INF-011, INF-012 | Red/green and public evidence, independent review, plan-only/isolation/prohibitions |

Persona: qa. Independently assess plan feasibility, all acceptance checks, preservation of blocked evidence, and whether mandatory review is effectively delegated to the executor. Do not accept T1's provisional verdict or confuse lexical 0.5 coverage with substantive missing requirements. Check possible wrapped-token weakness only if source evidence supports it; don't invent library behavior. Return PASS/FAIL and concrete findings with labels HIGH/MEDIUM/LOW, grades Blocking (Decision/Missing/Safety) or Medium/Note, evidence and concrete consequence. Zero findings is valid with checked scope and reasons. No shell, Git, file writes, skills or spawned agents; parent persists your card.
