# Reviewer Brief 3 — persona: refactorer (model class: opus, reviewer_id t1a-1)

You are a Tier-2 reflection reviewer (UC-1, pre-execution coverage audit). Audit ONLY the evidence in this brief plus what you can Read/Grep from your grounding root (/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel). You are read-only: no edits, no writes, no shell execution. You own the structural/consistency surface: does the plan fit each target file's existing structure and the repo's sync discipline?

## T1 card excerpt

From <output>/t1-card.md — structural findings (refactorer slice):

- **F2 (low, AC strength): Tasks 1-10 acceptance criteria are grep-count based** (`grep -c codegraph` and `grep -c index_state` each >= 1). They do not verify the pasted text matches the Constraints rule verbatim; an executor could satisfy the AC with materially different text.
- **F4 (positive): constraints match repo discipline.** All ten target files verified to have `tools:` count 0 and heading structure `## Triggers; ## Behavioral Mindset; ## Focus Areas; ## Key Actions; ## Outputs; ## Boundaries` (nine files) and self-review.md `## Primary Responsibilities; ## How to Operate`. Task 11 runs `make sync-dev` + `make verify-sync` + agent-file tests per CLAUDE.md component-sync workflow.
- **F5 (note): sanctioned wording variant for technical-writer (Task 10)** and self-review's different section/list style (Task 9) are both correctly specified.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T23:57:23Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### plan: TASK-WF-addTheSharedCode-20261111-193909.md:17-22 (Constraints, structural rules)

```markdown
## Constraints

- Rule text, identical in the nine engineering agents: "For symbols, callers, callees and impact use the codegraph tools per `~/.claude/CODEGRAPH.md`: only when the caller's brief says `index_state: fresh` together with `checked_at`, `worktree_root` and the `projectPath` to pass on every call, and Read every row before citing it. Otherwise use Grep, Glob and Read, and say so in your reply." It is the wording of the rule in src/superclaude/agents/reflect-reviewer.md, reuse-auditor.md, auggie-reviewer.md and troubleshoot-analyst.md.
- These ten files declare no tools line and inherit all tools: do not add a tools line or restrict tools. Change nothing but the added rule.
- Do not reference src/superclaude/ paths inside an agent file; point at ~/.claude/CODEGRAPH.md.
- Do not edit src/superclaude/core/CODEGRAPH.md, the four agents that already carry the rule, any command or skill, or .claude/. No commit, no push.
```

### plan: TASK-WF-addTheSharedCode-20261111-193909.md:84-87 (Task 9, self-review variant)

```markdown
## Task 9: Add the rule to self-review.md

In src/superclaude/agents/self-review.md add the rule from Constraints as one item at the end of the `## How to Operate` section, in that section's own list style.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/self-review.md are each at least 1; the diff adds only that item and no `tools:` line.
```

### plan: TASK-WF-addTheSharedCode-20261111-193909.md:89-105 (Task 10 + Phase 2)

```markdown
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
```

### target file shape: src/superclaude/agents/system-architect.md — headings (verified by orchestrator survey)

```text
## Triggers; ## Behavioral Mindset; ## Focus Areas; ## Key Actions; ## Outputs; ## Boundaries
```

Identical heading shape in root-cause-analyst, refactoring-expert, security-engineer, performance-engineer, python-expert, backend-architect, quality-engineer, technical-writer. self-review.md has `## Primary Responsibilities; ## How to Operate` only. None of the ten declares a `tools:` line. Read the files to confirm bullet list style at the end of `## Key Actions` before judging whether "one bullet at the end" is executable as written.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001 placement rule executable per file structure | Tasks 1-10 | covered | tasklist:26-94 + target headings |
| INF-002 sync discipline (Task 11) | Task 11 | covered | tasklist:98-105 |
| INF-003 no-structural-damage guardrails | Constraints | covered | tasklist:17-22 |
