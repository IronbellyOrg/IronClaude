# Analyzer review brief

## T1 card excerpt

The proposed change is narrowly limited to human-facing help, plus public-root regression tests. Current source still contains the unsupported option in the validate-lenses docstring and scaffold option help; the command reference instead identifies the JobSpec field. The plan is not an applied fix. Independent source-to-task mapping is recorded separately in coverage-matrix.md; review findings remain subject to blind calibration, Tier 2 comparison and evidence validation.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-23T20:08:34Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help

### src/superclaude/cli/swarm/commands.py:435-439

```python
    Runs the COMP-023 five-assertion lens validator over every entry in
    :data:`superclaude.cli.swarm.lenses.LENSES`. The ``custom`` escape
    hatch (COMP-026) is intentionally skipped — its prompt body flows in
    from ``--custom-prompt-dir`` at preflight and is validated on that
    path (T02.05 / T02.07).
```

Read the complete candidate `../../../TASK-WF-createACheckedIm-20261123-195709.md`, source `../../../source.md`, and sibling `../coverage-matrix.md`. Paths here are relative to this brief directory. Read current source snippets yourself before citing. Do not inherit a PASS from T1. Find concrete contradictions, missing obligations or safety failures; zero findings is valid when scope and reasons are stated.

## Coverage slice

| Requirements | Concern |
|---|---|
| INF-002, INF-003, INF-006, INF-008 | Supported correction, blocked historical status, parser and unchanged interface |

Persona: analyzer. Judge the actual plan against the source, historical REPORT.md's Proposed Fix/Next Steps and real code. Check task dependency order and whether intentionally red checkpoints have valid acceptance conditions. Candidate warnings from coverage review are hypotheses, not findings to confirm: possible wrapped token, exact applied-review filename, excluded directory placeholder. Validate or reject with evidence. Return a binary PASS/FAIL and each concrete finding with label HIGH/MEDIUM/LOW, grade Blocking (Decision/Missing/Safety) or Medium/Note, cited location, consequence and remedy. Never invent a finding for a quota; do not request product work. No shell, Git, tools that write, skills or new agents. Parent persists the returned card.
