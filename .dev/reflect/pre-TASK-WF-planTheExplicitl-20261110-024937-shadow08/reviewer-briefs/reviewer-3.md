# Reviewer Brief 3 — persona: refactorer (model class: opus, reviewer_id t1a-1)

You are a Tier-2 reflection reviewer (UC-1, pre-execution coverage audit). Audit ONLY the evidence in this brief plus what you can Read/Grep from your grounding root (/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel). You are read-only: no edits, no writes, no shell execution. You own the scope-discipline and wording-fidelity surface: does the plan stay inside the spec's boundaries (no subordinate mode, no worker-contract change, no historical-artifact edits, staging rules), and does the narrowed wording stay consistent across all touched surfaces?

## T1 card excerpt (verbatim from <output>/t1-card.md, refactorer slice)

- 4 inferred requirements (INF-001..004); union coverage 4/4 mapped; unmapped union: [].
- T1 F3 (positive): Constraints:19 forbids subordinate-mode implementation and worker-contract edits; no task touches WORKER-CONTRACT.md (WC-13 at :62 untouched); staging rules match CLAUDE.md absolute rules; the plan's target set equals the research report's O1 wording surface (report:2335-2338) with the "each item only if that wording is selected" condition (report:2272) satisfied.
- T1 F2: research Section 8 O1 also lists installed global copies (/home/coder/.claude/CLAUDE.md etc.) as distribution dependencies the plan intentionally does not touch — consistent with "only as necessary", not a defect.

Calibrator-noted gaps you must adjudicate (from blind calibration, C=0.76):
- Root vs core wording differs today: root CLAUDE.md:312 "An Orca coordinator is person-opened"; core/CLAUDE.md:58 "A supervised orchestrator's coordinator is person-opened"; root lacks core's worker-contract parenthetical (core:55-57). The test phrase "coordinator is person-opened" passes both, hiding the difference. Is the plan required to keep them different, align them, or is the difference out of scope?
- The plan adds ccsession-tag/README.md as a named canonical-guidance target where the spec says only "canonical guidance" (inference presented as fact?).
- Research report existence: source.md points at a to-do path; verify it exists (read-only) at .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md.
- The card mixes post-hoc on-disk state (package already executed) with the pre-execution audit framing.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:14:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### spec (whole body): .dev/tasks/done/TASK-WF-planTheExplicitl-20261110-024937/source.md:1

```text
Plan the explicitly requested narrow wording clarification for PR #449's phrase 'a coordinator under another orchestrator', preserving the existing worker-session fan-out ban and person-opened coordinator eligibility. Use .dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115/RESEARCH-REPORT-sub-orchestrator-mode.md sections 7.4, 7.6 and 8. Address canonical guidance, hook message, required mirrors and affected tests only as necessary. This is a wording clarification, not implementation of a subordinate mode.
```

### plan Goal + Constraints: tasklist:15-22 (verbatim)

```markdown
Goal: Remove the ambiguous subordinate-coordinator wording while preserving existing authority boundaries.

## Constraints

- Preserve the person-opened coordinator rule and the prohibition on supervised workers creating worktrees or dispatching workers. Do not implement a subordinate mode or alter the worker contract.
- Do not edit historical research artifacts or treat historical references as current guidance.
- `.dev/tasks/` is always staged; never stage generated `.claude/` mirrors. Commit or push only if separately requested.
```

### plan Task 1 + Task 2: tasklist:25-43 — Task 1 narrows owner wording in CLAUDE.md, src/superclaude/core/CLAUDE.md, src/superclaude/skills/ccsession-tag/README.md ("Keep the appended launch-guidance paragraphs identical in the two distributable files and retain their existing required role language"); Task 2 aligns the hook script + plugins/ mirror ownership sentence, the exact-message test, focused assertions "where necessary", make sync-dev, "do not stage generated mirrors".

### source: the three guidance locations today (post-narrowing on-disk state)

- CLAUDE.md:310-312 (root): "Every worktree gets an agent, and its creator owns it. ... The eligible session that creates a worktree owns its agent(s). An Orca coordinator is person-opened; ownership does not authorize a supervised worker to create worktrees or dispatch workers. A worktree a human creates needs an agent too. Supervised workers are started with `orca orchestration worker-start` ... A PreToolUse hook ... blocks ... the other parts of this rule are instructions only."
- src/superclaude/core/CLAUDE.md:54-61: "Every Orca worktree gets an agent: create it with `worktree create --agent` (supervised workers use `worker-start`, and a supervised worker follows its worker contract, which forbids it from creating worktrees), and never create a worktree for your own use. The eligible session that creates a worktree owns its agent(s). A supervised orchestrator's coordinator is person-opened; ownership does not authorize a supervised worker to create worktrees or dispatch workers. A hook blocks `orca worktree create` without `--agent`."
- src/superclaude/skills/ccsession-tag/README.md:240-243: mirrors core/CLAUDE.md's appended paragraph verbatim (verified identical).

### source: research report Section 7.6 item 1 (report:2272, abridged quote)

```text
The one decision: gap A01 (Important), the PR #449 phrase "a coordinator under another orchestrator". Choose between (a) narrowing the phrase now, as a wording change separate from any subordinate mode ... Under (a), the Section 8 O1 wording surface applies, each item only if that wording is selected. That surface is `CLAUDE.md`, `src/superclaude/core/CLAUDE.md`, the ccsession README, the worktree-hook message with its exact-message test, and their copies.
```

## Coverage slice (rows you own)

| Requirement | Status per T1 card | Your question |
|-------------|--------------------|---------------|
| INF-004 wording clarification only; no subordinate mode; worker contract unaltered | covered (tasklist:19,27) | Does any task step or AC leak scope (role redefinition, contract edits, historical-artifact edits)? |
| Cross-surface wording consistency | T1 F3: target set equals O1 surface; F2: installed global copies intentionally untouched | Is the required-phrase set coherent across root CLAUDE.md, core/CLAUDE.md, README and hook message, and is the root-vs-core wording difference (An Orca coordinator vs A supervised orchestrator's coordinator) legitimate variation or a fidelity defect the plan should have flagged? |
| Staging / mirror discipline | covered (tasklist:21,39) | Do the staging constraints match the repo's absolute rules, and can any step accidentally stage generated mirrors? |
