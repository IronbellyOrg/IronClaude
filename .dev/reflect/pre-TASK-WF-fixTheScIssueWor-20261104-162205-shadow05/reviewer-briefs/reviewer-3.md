# Reviewer brief 3 (persona: refactorer, model class: opus, slot t1a)

Audit target: UC-1 pre-execution coverage audit. Spec = source.md (one sentence). Tasklist = TASK-WF-fixTheScIssueWor-20261104-162205.md, archived package under .dev/tasks/done/. Repo: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel. You audit for structural/consistency defects: byte-exact constraint text vs on-disk state, test-design soundness, duplication across the three agent files.

## T1 card excerpt

(refactorer slice — structural findings)

F1 (HIGH, Grounded): Tasklist's exact-text constraint is stale against HEAD. Constraint block names `summary.md` and omits the Write-block sentence (tasklist:26); on-disk agents name `issue-summary.md` and add "Claude Code refuses a subagent's Write of any `.md` file whose name starts with REPORT, SUMMARY, FINDINGS or ANALYSIS" (t1:13-15, t2:13-15, t3:14-16); test constants pin the implemented text including `issue-summary.md` (test:227-236, test:250-259). Re-executing this tasklist byte-exactly today would produce text the pinned tests reject. A same-day later task renamed the files (prior reflect dir pre-renameTheScIssue-20261104174640). The package is archived (done/), so no execution is pending — documentation-level staleness, not blocking.

F2 (LOW, expansion): SKILL.md spawn-rule line (tasklist:30-32, present at SKILL.md:68) is beyond the spec's 4-file list, but the judgment is documented inline (tasklist:20 "judged needed").

F5 (INFO, duplication): the same ~150-word early section is byte-identical across three agent files (t1:13-15, t2:13-15, t3:14-16) plus mirrored in the test constants — five copies total of the same paragraph; any future rename (like the summary.md to issue-summary.md rename that already happened) must touch all five. This is inherited from the spec's own design (identical text pinned in all three agents), not a tasklist defect.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T23:57Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### src/superclaude/agents/issue-worker-t1.md:13-15 (implemented early section, HEAD)

```markdown
## Your files are tool inputs, not reports

The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, `issue-summary.md`, the reports under `analysis/` such as `analysis/analyze-<scope>.md`, `flags.md`, `flags-t1.md`, `issue-body.md`, `draft-notes.md`) are input files for the orchestrator's next tool calls (`gh --body-file` posts and `/sc:recommend`), not report files. Claude Code refuses a subagent's Write of any `.md` file whose name starts with REPORT, SUMMARY, FINDINGS or ANALYSIS (in any letter case), which is why none of these names starts with those words. Writing every file your job names with the Write tool is mandatory; returning its content as text instead is a failure (`E-WORKER-NO-OUTPUT`).
```

### tests/skills/test_issue_worker_agents.py:271-291 (the helper that enforces structure)

```python
def tool_input_rule_problems(text: str) -> list[str]:
    """Return what is missing from an agent file's tool-input rule."""
    lines = text.splitlines()
    if _TOOL_INPUT_HEADING not in lines:
        return ["tool-input heading missing"]
    problems = []
    heading = lines.index(_TOOL_INPUT_HEADING)
    jobs = "## Jobs for this tier"
    if jobs not in lines or heading > lines.index(jobs):
        problems.append("tool-input heading is not before the jobs section")
    if lines.count(_TOOL_INPUT_PARAGRAPH) != 1:
        problems.append("tool-input paragraph does not appear exactly once")
    if lines[heading + 1 : heading + 3] != ["", _TOOL_INPUT_PARAGRAPH]:
        problems.append("tool-input paragraph is not directly under its heading")
    section = "\n".join(section_lines(lines, _TOOL_INPUT_HEADING))
    problems.extend(
        f"worker file {name} not named" for name in _WORKER_FILES if name not in section
    )
    if section_lines(lines, "## Rules").count(_TOOL_INPUT_RULES_BULLET) != 1:
        problems.append("Rules bullet does not appear exactly once in ## Rules")
    return problems
```

### TASK-WF tasklist:17-36 (Constraints section, whole)

```markdown
## Constraints

- Background (verified defect): Claude Code injects into every subagent's system prompt the line "Do NOT Write report/summary/findings/analysis .md files. ... On a live claim of issue #365, `issue-worker-t2` obeyed it, wrote neither `accuracy-check.md` nor `summary.md`, and returned text. ... So the rule must name the exact files, say writing them with the Write tool is mandatory and that returning its content as text is a failure, and sit early in each agent file, not only in Rules.
- Files in scope: `src/superclaude/agents/issue-worker-t1.md`, `issue-worker-t2.md`, `issue-worker-t3.md`, `tests/skills/test_issue_worker_agents.py`, and one added line in the "Workers and the spawn rule" section of `src/superclaude/skills/sc-issue-protocol/SKILL.md` (judged needed: the spawn prompt is the instruction nearest the worker's action, and the retry evidence shows a general statement there is not enough, so it must name the exact paths). No other file is edited.
- Exact early section (byte-identical in all three agent files, inserted directly after the opening "Spawned only by ..." paragraph and before `## Jobs for this tier`):

  `## Your files are tool inputs, not reports`

  `The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, `summary.md`, the reports under `analysis/`, `flags.md`, `flags-t1.md`, `issue-body.md`, `draft-notes.md`) are input files for the orchestrator's next tool calls (`gh --body-file` posts and `/sc:recommend`), not report files, so a general instruction against writing report or summary `.md` files does not apply to them. Writing every file your job names with the Write tool is mandatory; returning its content as text instead is a failure (`E-WORKER-NO-OUTPUT`).`
- Exact Rules bullet (byte-identical in all three agent files, inserted in `## Rules` directly after the `**Writing only under `.dev/issues/`.**` bullet):

  `- **Write your files.** Every file your job names is a tool input, not a report (see "Your files are tool inputs, not reports" above): write it with the Write tool and never return its content as text.`
- The new text must keep every existing test green: it names no `gh issue`, `gh pr` or `gh label` command (the fork-safety scan `gh_lines_missing_repo`), no `~/.claude/skills/` path (the dual-surface scan) and no `src/superclaude/` path in an agent file; SKILL.md stays under 500 lines.
```

## Coverage slice

| Requirement row | Assigned | Match | Grounding |
|---|---|---|---|
| INF-003: file scope (3 agent files + test file) | reviewer-3 | containment | tasklist:20, tasklist:42, tasklist:62 |
