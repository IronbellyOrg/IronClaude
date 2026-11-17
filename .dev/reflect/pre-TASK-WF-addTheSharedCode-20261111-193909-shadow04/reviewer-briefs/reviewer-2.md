# Reviewer Brief 2 — persona: qa (model class: haiku, reviewer_id t4-1)

You are a Tier-2 reflection reviewer (UC-1, pre-execution coverage audit). Audit ONLY the evidence in this brief plus what you can Read/Grep from your grounding root (/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel). You are read-only: no edits, no writes, no shell execution. You own the coverage/acceptance surface.

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## T1 card excerpt

From <output>/t1-card.md — coverage and extraction summary (qa slice):

- Pass 1 (ID_REGEX): 0 labeled requirement IDs (spec carries no SPEC-/T- IDs).
- Pass 2 (inference): 3 valid INF rows: INF-001 (shared codegraph rule with three fields: checked_at, worktree_root, projectPath), INF-002 (ten general-purpose agent files listed in .dev/issues/504/issue-summary.md), INF-003 (following the wording in four named agent files).
- parsed_count=0 < inferred_count=3 → coverage_degraded: parsed-sparse (T1 stop forbidden; Tier 2 forced, consistent with --tier 2 pin).
- Union coverage 3/3 mapped; unmapped union requirements: [].
- Tasklist: 11 tasks (10 per-file rule additions + 1 sync-and-check). Every task has acceptance criteria; Tasks 1-10 ACs are grep-count based; Task 11 AC requires make verify-sync pass, no new src/superclaude references, agent-file tests pass, evidence saved to artifacts/t11-verify.log.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T23:57:23Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### spec (whole body): .dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/source.md:1

```text
Add the shared codegraph rule (use codegraph only when the caller passes index_state: fresh with checked_at, worktree_root and projectPath; otherwise Grep/Glob/Read) to the ten general-purpose agent files listed in .dev/issues/504/issue-summary.md, following the wording in troubleshoot-analyst.md, reflect-reviewer.md, reuse-auditor.md and auggie-reviewer.md
```

### plan: .dev/tasks/done/TASK-WF-addTheSharedCode-20261111-193909/TASK-WF-addTheSharedCode-20261111-193909.md:15-22 (Goal + Constraints)

```markdown
Goal: Ten agent files under src/superclaude/agents/ carry the shared codegraph rule (use codegraph only when the caller's brief passes index_state: fresh with checked_at, worktree_root and projectPath; otherwise Grep/Glob/Read), with no other change and no tools line.

## Constraints

- Rule text, identical in the nine engineering agents: "For symbols, callers, callees and impact use the codegraph tools per `~/.claude/CODEGRAPH.md`: only when the caller's brief says `index_state: fresh` together with `checked_at`, `worktree_root` and the `projectPath` to pass on every call, and Read every row before citing it. Otherwise use Grep, Glob and Read, and say so in your reply." It is the wording of the rule in src/superclaude/agents/reflect-reviewer.md, reuse-auditor.md, auggie-reviewer.md and troubleshoot-analyst.md.
- These ten files declare no tools line and inherit all tools: do not add a tools line or restrict tools. Change nothing but the added rule.
- Do not reference src/superclaude/ paths inside an agent file; point at ~/.claude/CODEGRAPH.md.
- Do not edit src/superclaude/core/CODEGRAPH.md, the four agents that already carry the rule, any command or skill, or .claude/. No commit, no push.
```

### plan: task-section template (Task 1 example): TASK-WF-addTheSharedCode-20261111-193909.md:26-31

```markdown
## Task 1: Add the rule to system-architect.md

In src/superclaude/agents/system-architect.md add the rule from Constraints as one bullet at the end of the `## Key Actions` list.

Acceptance criteria:
- `grep -c codegraph` and `grep -c index_state` on src/superclaude/agents/system-architect.md are each at least 1; the diff adds only that bullet and no `tools:` line.
```

(Tasks 2-8 repeat this shape per file; Task 9 targets self-review.md `## How to Operate` in its own list style; Task 10 words the rule for technical-writer.md to apply only when looking up a code fact; Task 11 runs `make sync-dev`, `make verify-sync`, agent-file tests with `uv run pytest`, evidence to artifacts/t11-verify.log. Read the tasklist file for the full text.)

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001 rule added, identical text, nine engineering agents | Tasks 1-9 | covered | tasklist:26-87 |
| INF-001 variant | Task 10 (technical-writer, code-fact-only wording) | covered | tasklist:89-94 |
| INF-002 ten files enumerated | Tasks 1-10 | covered | tasklist:26-94 |
| INF-003 wording follows four agents | Constraints:19 | covered-with-finding (T1 F1: four agents' text differs from mandated text) | tasklist:19 |
| sync + verify | Task 11 | covered | tasklist:98-105 |
