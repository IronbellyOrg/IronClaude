# Reviewer brief 1 (persona: analyzer, model class: sonnet, slot t1b)

Audit target: UC-1 pre-execution coverage audit. Spec = source.md (one sentence). Tasklist = TASK-WF-fixTheScIssueWor-20261104-162205.md. The work-unit package is archived under .dev/tasks/done/. You audit the spec/tasklist pair for coverage gaps and defects; the repo is at /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel.

## T1 card excerpt

(analyzer slice — deviation/root-cause findings)

F1 (HIGH, Grounded): Tasklist's exact-text constraint is stale against HEAD. Constraint block names `summary.md` and omits the Write-block sentence (tasklist:26); on-disk agents name `issue-summary.md` and add "Claude Code refuses a subagent's Write of any `.md` file whose name starts with REPORT, SUMMARY, FINDINGS or ANALYSIS" (t1:15, t2:15, t3:16); test constants pin the implemented text including `issue-summary.md` (test:227-236, test:250-259). Re-executing this tasklist byte-exactly today would produce text the pinned tests reject. A same-day later task renamed the files (prior reflect dir pre-renameTheScIssue-20261104174640). The package is archived (done/), so no execution is pending — flag as documentation-level staleness, not a blocking defect.

F2 (LOW, Grounded): Tasklist expands spec scope: SKILL.md spawn-rule line (tasklist:30-32, present at SKILL.md:68) is beyond the spec's 4-file list, but the judgment is documented inline (tasklist:20 "judged needed").

Union coverage: 3/3 inferred rows matched (INF-001 rule → Task 2, INF-002 regression test → Task 1, INF-003 file scope → Tasks 1-2). coverage_pct_union = 1.0.

End your card with a ## Findings block fenced findings-v2 block (lens: reflect-pre, citations with roles plan and spec) and a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-12T23:57Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### TASK-WF tasklist:19-26 (constraints: the harness line and exact early section)

```markdown
- Background (verified defect): Claude Code injects into every subagent's system prompt the line "Do NOT Write report/summary/findings/analysis .md files. Return findings directly as your final assistant message ... (Files written as input to another tool are fine; this note is about report files.)". On a live claim of issue #365, `issue-worker-t2` obeyed it, wrote neither `accuracy-check.md` nor `summary.md`, and returned text. Coordinator follow-up (message "Retry still skipped summary.md: name the files explicitly"): the protocol's one retry, with a spawn prompt stating the exemption in general terms, wrote `accuracy-check.md` but still skipped `summary.md`, because the harness line names "summary" files directly. So the rule must name the exact files, say writing them with the Write tool is mandatory and that returning their content as text is a failure, and sit early in each agent file, not only in Rules.
```

```markdown
  `## Your files are tool inputs, not reports`

  `The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, `summary.md`, the reports under `analysis/`, `flags.md`, `flags-t1.md`, `issue-body.md`, `draft-notes.md`) are input files for the orchestrator's next tool calls (`gh --body-file` posts and `/sc:recommend`), not report files, so a general instruction against writing report or summary `.md` files does not apply to them. Writing every file your job names with the Write tool is mandatory; returning its content as text instead is a failure (`E-WORKER-NO-OUTPUT`).`
```

### src/superclaude/agents/issue-worker-t1.md:13-15 (implemented early section, HEAD)

```markdown
## Your files are tool inputs, not reports

The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, `issue-summary.md`, the reports under `analysis/` such as `analysis/analyze-<scope>.md`, `flags.md`, `flags-t1.md`, `issue-body.md`, `draft-notes.md`) are input files for the orchestrator's next tool calls (`gh --body-file` posts and `/sc:recommend`), not report files. Claude Code refuses a subagent's Write of any `.md` file whose name starts with REPORT, SUMMARY, FINDINGS or ANALYSIS (in any letter case), which is why none of these names starts with those words. Writing every file your job names with the Write tool is mandatory; returning its content as text instead is a failure (`E-WORKER-NO-OUTPUT`).
```

### tests/skills/test_issue_worker_agents.py:227-236 (pinned paragraph constant)

```python
_TOOL_INPUT_PARAGRAPH = (
    "The files you write under `.dev/issues/` (`scout.md`, `accuracy-check.md`, "
    "`issue-summary.md`, the reports under `analysis/` such as "
    "`analysis/analyze-<scope>.md`, `flags.md`, `flags-t1.md`, `issue-body.md`, "
    "`draft-notes.md`) are input files for the orchestrator's next tool calls "
    ...
)
```

### tests/skills/test_issue_worker_agents.py:250-259 (pinned file list)

```python
_WORKER_FILES = (
    "scout.md",
    "accuracy-check.md",
    "issue-summary.md",
    "analysis/analyze-<scope>.md",
    "flags.md",
    "flags-t1.md",
    "issue-body.md",
    "draft-notes.md",
)
```

### source.md:1 (the entire spec)

```markdown
Fix the /sc:issue worker agents so they always write their files: add to each issue-worker-t*.md Rules section a rule that the files they write under .dev/issues/ are input files for the orchestrator's next tool calls (gh --body-file posts, /sc:recommend), not report files, so the general harness note against writing report .md files does not apply to them, and returning the content as text instead is a failure (E-WORKER-NO-OUTPUT). Add a regression test in tests/skills/test_issue_worker_agents.py that every issue-worker agent file carries that rule. Files: src/superclaude/agents/issue-worker-t1.md, issue-worker-t2.md, issue-worker-t3.md, tests/skills/test_issue_worker_agents.py
```

## Coverage slice

| Requirement row | Match | Task(s) | Grounding |
|---|---|---|---|
| INF-001: Rules-section rule in each issue-worker-t*.md | containment | Task 2 + Goal | tasklist:15, tasklist:58-62 |
| INF-002: regression test in tests/skills/test_issue_worker_agents.py | containment | Task 1 | tasklist:38-50 |
| INF-003: file scope (3 agent files + test file) | containment | Tasks 1-2 | tasklist:42, tasklist:62 |
