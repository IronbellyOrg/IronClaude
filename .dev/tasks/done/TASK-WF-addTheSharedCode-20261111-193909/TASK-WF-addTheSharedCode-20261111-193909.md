---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-addTheSharedCode-20261111-193909
version: "1"
priority: Medium
created_date: "2026-11-11"
---

# Add the shared codegraph rule to ten general-purpose agents

Source: ./source.md
Goal: Ten agent files under src/superclaude/agents/ carry the shared codegraph rule (use codegraph only when the caller's brief passes index_state: fresh with checked_at, worktree_root and projectPath; otherwise Grep/Glob/Read), with no other change and no tools line.

## Constraints

- Rule text, identical in the nine engineering agents: "For symbols, callers, callees and impact use the codegraph tools per `~/.claude/CODEGRAPH.md`: only when the caller's brief says `index_state: fresh` together with `checked_at`, `worktree_root` and the `projectPath` to pass on every call, and Read every row before citing it. Otherwise use Grep, Glob and Read, and say so in your reply." It is the wording of the rule in src/superclaude/agents/reflect-reviewer.md, reuse-auditor.md, auggie-reviewer.md and troubleshoot-analyst.md.
- These ten files declare no tools line and inherit all tools: do not add a tools line or restrict tools. Change nothing but the added rule.
- Do not reference src/superclaude/ paths inside an agent file; point at ~/.claude/CODEGRAPH.md.
- Do not edit src/superclaude/core/CODEGRAPH.md, the four agents that already carry the rule, any command or skill, or .claude/. No commit, no push.

## Phase 1: Add the rule to each agent file

## Task 1: Add the rule to system-architect.md

In src/superclaude/agents/system-architect.md add the rule from Constraints as one bullet at the end of the `## Key Actions` list.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/system-architect.md are each at least 1; the diff adds only that bullet and no `tools:` line.

## Task 2: Add the rule to root-cause-analyst.md

In src/superclaude/agents/root-cause-analyst.md add the rule from Constraints as one bullet at the end of the `## Key Actions` list.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/root-cause-analyst.md are each at least 1; the diff adds only that bullet and no `tools:` line.

## Task 3: Add the rule to refactoring-expert.md

In src/superclaude/agents/refactoring-expert.md add the rule from Constraints as one bullet at the end of the `## Key Actions` list.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/refactoring-expert.md are each at least 1; the diff adds only that bullet and no `tools:` line.

## Task 4: Add the rule to security-engineer.md

In src/superclaude/agents/security-engineer.md add the rule from Constraints as one bullet at the end of the `## Key Actions` list.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/security-engineer.md are each at least 1; the diff adds only that bullet and no `tools:` line.

## Task 5: Add the rule to performance-engineer.md

In src/superclaude/agents/performance-engineer.md add the rule from Constraints as one bullet at the end of the `## Key Actions` list.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/performance-engineer.md are each at least 1; the diff adds only that bullet and no `tools:` line.

## Task 6: Add the rule to python-expert.md

In src/superclaude/agents/python-expert.md add the rule from Constraints as one bullet at the end of the `## Key Actions` list.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/python-expert.md are each at least 1; the diff adds only that bullet and no `tools:` line.

## Task 7: Add the rule to backend-architect.md

In src/superclaude/agents/backend-architect.md add the rule from Constraints as one bullet at the end of the `## Key Actions` list.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/backend-architect.md are each at least 1; the diff adds only that bullet and no `tools:` line.

## Task 8: Add the rule to quality-engineer.md

In src/superclaude/agents/quality-engineer.md add the rule from Constraints as one bullet at the end of the `## Key Actions` list.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/quality-engineer.md are each at least 1; the diff adds only that bullet and no `tools:` line.

## Task 9: Add the rule to self-review.md

In src/superclaude/agents/self-review.md add the rule from Constraints as one item at the end of the `## How to Operate` section, in that section's own list style.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/self-review.md are each at least 1; the diff adds only that item and no `tools:` line.

## Task 10: Add a code-fact-only rule to technical-writer.md

In src/superclaude/agents/technical-writer.md add the rule from Constraints as one bullet at the end of the `## Key Actions` list, worded to apply only when looking up a code fact to document (a symbol, its callers, its impact); prose, structure and audience work never needs codegraph.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/technical-writer.md are each at least 1; the diff adds only that bullet and no `tools:` line.

## Phase 2: Sync and check

## Task 11: Sync the dev copies and confirm they match

Depends on: Task 10

Run `make sync-dev` then `make verify-sync` from the repository root; run the tests that cover agent files (find them with grep under tests/) with `uv run pytest`.

Acceptance criteria:
- `make verify-sync` passes, `grep -rn 'src/superclaude'` over the ten agent files shows no new hit, and the agent-file tests pass; evidence saved to ./artifacts/t11-verify.log.
