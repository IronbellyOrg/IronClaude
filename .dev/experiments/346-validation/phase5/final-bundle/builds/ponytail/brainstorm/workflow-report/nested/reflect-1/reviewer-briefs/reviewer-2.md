# Reviewer 2 brief (persona: qa), UC-1 pre-execution reflect of a workflow plan

Persona lens: qa. Read-only: audit the plan against the spec; return findings only; never edit files, run no shell or git.
Spec: /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md. Plan (tasklist): /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md. Declared plan scope: spec sections 3 and 4 only, plus owner decisions listed in the plan's Constraints (they override the spec).

## T1 card excerpt

## QA section (coverage / acceptance)

- Q1. ./source.md section 3.5 grade-parse bullet requires a test that "`MAJOR (FR-8 GAP)` graded minor counts as protected"; plan Task 2 acceptance criteria list the four formats, non-blocking and unknown/conflicting, but not the FR-8-protected case. Candidate gap.
- Q2. ./source.md section 3.5 hunks bullet names "incidental id mentions"; plan Task 2 AC covers partial words and bare numbers but does not name incidental mentions explicitly. Candidate gap (minor).
- Q3. ./source.md section 2.5 "one smoke dispatch settles it before S1" (plugin skill in a dispatched worker) is carried only as an open precondition line in INSTALL.md (Task 11), not as a task. Out of declared scope (experiment run), candidate advisory.
- Q4. ./source.md section 3.5 static bullet "the canonical cap text and at-cap clause ... are present" is in Task 8. ./source.md section 3.5 "Keep green" list is in Task 8 AC. Covered.
- Q5. Sections 5 and 6 (measurement, replicates, paired fork, blind re-grade, falsifiers F1-F5) are excluded by the plan Constraints per the coordinator scope (sections 3 and 4). Expected unmapped rows.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-08T18:24Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail projectPath=/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail

### src/superclaude/commands/spec-panel.md:451-462
```markdown
## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:spec-panel` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument (quoted specification content is a quoted argument); otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/spec-panel-report.md`. `artifacts` lists `<report-dir>/improved-spec.md` when the Improve step ran; paths git ignores are left out (WC-4), and it is `[]` otherwise. The run is succeeded when the report is written, blocked at the gate below, and failed otherwise.
- **Person-mode flags.** None is refused. `--mode socratic` only writes its questions into the report and does not wait for answers.
- **Gates.** Under `--unattended` a TDD input without `--target-release` resolves as blocked, with the `target_release` question in `blocked_question`; PRD inputs are unchanged, because they need no `target_release`. The Improve step (step 6) runs only when `--improve` is passed, and then writes `<report-dir>/improved-spec.md`; the input specification is never modified. There is no other gate.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

```
### tests/skills/test_worker_contract.py:830-839
```python

def _check_no_unattended_sections() -> None:
    have = sorted(
        p.stem
        for p in Path(_THIS.COMMANDS_DIR).glob("*.md")
        if re.search(r"^## Unattended mode\s*$", p.read_text(encoding="utf-8"), re.M)
    )
    assert set(have) == set(UNATTENDED_COMMANDS), (
        f"unexpected `## Unattended mode` sections: {have}"
    )
```
### tests/recommend/test_routing_refresh.py:33
```python
_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}
```
### tests/recommend/test_routing_refresh.py:647-648
```python
    shipped = {p.stem for p in _COMMANDS.glob("*.md") if p.name != "README.md"}
    assert shipped - _POST_REFRESH_ADDITIONS == active
```

### .dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md:1-333 (spec body, D13 qa hunk)
Read the whole file at the path above (333 lines). Audit the coverage matrix AGAINST the spec body; surface any requirement-bearing span in sections 3 and 4 absent from the matrix (parsed or inferred) or not delivered by a plan task as a finding.

## Coverage slice

Full matrix: /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/brainstorms/346-ponytail/workflow-report/nested/reflect-1/artifacts/coverage-matrix.yaml (109 inferred rows, coverage_pct_union 0.789, S_dev_density 0.211, coverage_degraded parsed-sparse). Unmatched by containment: INF-001, INF-003, INF-021, INF-023, INF-024, INF-036, INF-040, INF-041, INF-042, INF-051, INF-057, INF-069, INF-070, INF-072, INF-087, INF-099..INF-106. Mapper advisory notes: INF-051 (verdict exit 2 on inconsistency not in Task 5), INF-077 (MAJOR (FR-8 GAP) graded-minor test absent from Task 2).

Return format: a YAML list of findings, each {id, severity: blocking|minor (blocking = the plan as written would deliver wrong behaviour, miss a required in-scope deliverable, or contradict an owner decision; else minor), plan_task, spec_ref (source.md:<line>), evidence (quoted plan or spec text with file:line), claim_tag: grounded|INFERRED, recommendation (file + change + verifier)}, then confidence 0.00-1.00 and one line naming what you actively checked.
