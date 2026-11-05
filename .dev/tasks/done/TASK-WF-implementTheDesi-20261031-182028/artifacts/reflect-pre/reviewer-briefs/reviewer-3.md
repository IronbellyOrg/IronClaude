# Reviewer 3 brief (persona: refactorer)

Read-only audit (UC-1, pre-execution). Audit the implementation PLAN against its spec (source.md -> the linked design). Do not edit, write, or run anything; Read/Grep/Glob only, from repo root /home/coder/workspaces/IronClaude/.dev/worktrees/pr-submit-codex. Return a reviewer card as YAML: reviewer, persona, findings (list of {id, claim, citation file:line, class: aligned|refinement|drift|gap, severity: high|medium|low, recommendation naming a task}), self_confidence 0-1. Tag any claim without a file:line with [INFERRED].

## T1 card excerpt

## Structural / risk section

- Regression candidate R1: Task 4 changes `_thread_findings` (src/superclaude/pr_submit/classifier.py:259) used by `_selection` (classifier.py:380-383) for every Augment Cosmos classification; the default-argument path must keep Augment behaviour identical. Task 4's acceptance criteria name the Cosmos and silence test files as the guard.
- Regression candidate R2: Task 3 changes `rereview_request_count` folding (src/superclaude/pr_submit/run_log.py:189-191), which INV-R1 tests and crash recovery (src/superclaude/pr_submit/recovery.py:136-141) read; old logs without `cycle_id` must rebuild to the same count (Task 3 AC covers it).
- Risk R3: SKILL.md / refs are markdown with no executable test of the new two-reviewer loop; correctness of the orchestration text rests on test_skill_parse.py / test_static_grep.py plus review. The core functions it calls are unit-tested (Task 10).
- Risk R4: the Task 7 dry check needs network access to GitHub and the PR 336 threads; it is read-only.
- Risk R5: an operator's existing local override (Augment-only) would silently disable Codex (Task 2 choice).


## Grounding hunks

### .dev/tasks/to-do/TASK-WF-implementTheDesi-20261031-182028/TASK-WF-implementTheDesi-20261031-182028.md:1-187
The plan under audit (Read the whole file).

### .dev/pr-submit-codex/design/pr-submit-codex-design.md:220-297 (dedup, reply, re-trigger, loop guard, events)
### src/superclaude/pr_submit/run_log.py:160-242 (rebuild_state)
### src/superclaude/pr_submit/recovery.py:115-145 (resume S5a rule)
### src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:41-130 (attended poll loop + snapshot gate)
### src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh:1-149

## Coverage slice

| Requirement area | Tasks | Status |
|---|---|---|
| design s9 dedup, s10 reply, s11 re-trigger, s12 loop guard, s13 events | 3,9,11,12,14 | partly mapped (see semantic_gaps) |
