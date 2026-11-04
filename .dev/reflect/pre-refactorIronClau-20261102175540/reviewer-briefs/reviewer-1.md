# Reviewer 1 brief: analyzer lens (model class: sonnet)

Mode: UC-1 pre-execution. You audit a PROPOSED plan (tasklist) against its driving spec, read-only. Do not run commands. Return findings only; the orchestrator persists them.

Spec: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/source.md
Tasklist under review (read it in full): /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md

Your lens: does each task faithfully carry out what the spec asks, and where does the plan go beyond or fall short of it? Classify each divergence under the 4-category taxonomy (authorized expansion, necessary deviation, drift, regression) with a one-line rationale and a file:line citation. Try to refute the T1 card's findings, not just confirm them.

## T1 card excerpt

Verbatim from /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/reflect/pre-refactorIronClau-20261102175540/t1-card.md, section "Root-cause / deviation section (analyzer lens)":

- F1 (deviation, needs user decision): the plan adds a third class, "Historical record, keep unchanged", for POST-REFLECT-TASK.md (plan line 37). The source names only two classes: project worktree (move to Orca) and internal temporary checkout (keep working without Orca) (source.md:1). POST-REFLECT-TASK.md holds 79 of the 108 hits, so 73% of the hit lines stay as they are. Class: refinement beyond the source; the rationale is recorded in Task 1 but the user did not authorize it.
- F2 (deviation, minor): Task 1 classifies per FILE (one row per file with a hit count, plan lines 33-45), while the source says "Classify each hit" (source.md:1). For a mixed file (CLAUDE.md after Task 2 holds both a retired-location prohibition and an internal-exception line) a per-file class is coarser than per-hit.
- F3 (interpretation, low): Task 3 reads "never pushed to or interacted with" as also forbidding fetch or pull from the upstream remote (plan lines 73 and 82). This is a literal reading of "interacted with", not stated explicitly in the source.
- F4 (residual by design, aligned): Task 4 keeps the `.dev/worktrees/` ignore entry (plan line 89), so a hit remains in .gitignore; Task 7's residual rule (plan line 134) allows it. Aligned with "replace the rule" because the comment is rewritten to say retired.
- F5 (gap, low): CLAUDE.md keeps a markdown link to an upstream SuperClaude-Org issue (#419) in its Slash Commands note. Task 3's new wording "no tool call or link (gh, git or Orca) that resolves to it" (plan line 73) may read as contradicting that existing link. [INFERRED] Whether a static doc link counts as "interaction" is a reading question the plan does not address.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-02T17:55Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths projectPath=/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths

### .dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/source.md:1

```text
Refactor IronClaude to Orca's default worktree paths: replace the .dev/worktrees rule in CLAUDE.md and every tracked file that encodes .dev/worktrees or git worktree add (git grep -E '\.dev/worktrees|git worktree add' -- ':!.dev'). Classify each hit as project worktree (move to Orca-created worktrees at Orca's default location) or internal temporary checkout used by a CLI or test (keep working without Orca). Also tighten the CLAUDE.md rule: SuperClaude upstream is never pushed to or interacted with. Source of truth is src/superclaude; run make sync-dev; never stage .claude mirrors.
```

### CLAUDE.md:43-48

```markdown
**NEVER**, under any circumstance:

- Run a bare `gh pr create` without `--repo IronbellyOrg/IronClaude`. The GitHub CLI defaults `gh pr create` to the **parent repo of a fork**, which means PRs silently land on the public upstream — exposing private fork work and misrouting reviews.
- Open PRs against `SuperClaude-Org/SuperClaude_Framework` without explicit user authorization in the same session. Treat that target as forbidden.
- Push to `upstream` (the `upstream` remote name above). The `origin` remote is the correct push target.
- Assume the upstream is the right target because gh's interactive flow suggests it. The interactive flow is the trap.
```

### CLAUDE.md:68

```markdown
**Exceptions:** Contributing back to upstream is explicit, separate, deliberate user authorization in the same session — never a default behavior. Without that explicit instruction, every PR goes on the fork.
```

### POST-REFLECT-TASK.md:1-9

```yaml
---
id: "TASK-RF-reflect-reviewer-guard-20260622-200400"
title: "Harden /sc:reflect Wave-3 reviewer spawning against repository mutation (six defense layers + falsifier suite)"
description: "Add six defense-in-depth layers (L1 restricted reviewer agent, L1b ClaudeProcess restricted profile, L2 reviewer-isolation snapshot gate, L3 verb-denylist defense-in-depth, L4 advisory READ-ONLY brief, L5 static+dynamic graders) plus a 6-test falsifier suite to prevent a reflect reviewer (spawned today with all-tools personas) from mutating the repo it is auditing. Reliability / data-loss-prevention hardening — NOT a security framing."
version: ""
status: "🔴 Blocked"
type: "🔧 Refactor"
priority: "🔼 High"
created_date: "2026-06-22"
```

## Coverage slice

| Requirement | Matched task | Status | Grounding |
|---|---|---|---|
| INF-005 classify each hit into two classes | Task 1 | covered lexically (0.842); plan uses three classes | source.md:1; tasklist Task 1 |
| INF-006 project worktree moves to Orca default location | Task 2 | covered (0.889) | source.md:1; tasklist Tasks 2, 4, 5 |
| INF-007 internal checkout keeps working without Orca | Task 1 | covered (0.889) by "unchanged" assertions | source.md:1; tasklist Tasks 1, 7 |
| INF-008 tighten upstream rule | Task 3 | covered (0.9) | source.md:1; CLAUDE.md:43-48, 68 |
