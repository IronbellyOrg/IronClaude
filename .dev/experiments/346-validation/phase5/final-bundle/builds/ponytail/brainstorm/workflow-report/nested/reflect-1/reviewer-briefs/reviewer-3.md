# Reviewer 3 brief (persona: refactorer), UC-1 pre-execution reflect of a workflow plan

Persona lens: refactorer. Read-only: audit the plan against the spec; return findings only; never edit files, run no shell or git.
Spec: /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md. Plan (tasklist): /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md. Declared plan scope: spec sections 3 and 4 only, plus owner decisions listed in the plan's Constraints (they override the spec).

## T1 card excerpt

## Refactorer section (structure / risk)

- S1. Plan Task 12 reads two source paths under /tmp/impl/exp/s1/ that may not survive until /sc:implement runs; the plan says stop and report blocked. Risk: Task 12 blocks.
- S2. Plan Task 8 stages new delivery files with `git add` so tracked-file scans see them; staging inside an /sc:implement run may interact with its private-index snapshots. [INFERRED] no direct evidence of conflict.
- S3. The `verdict` owner count depends on parsing review-3 new-finding labels whose real format is unknown until S1 runs; tests use synthetic fixtures only. Risk carried by fail-closed exit 2.
- S4. Plan has 12 tasks in 5 phases, contiguous numbering, every task has Acceptance criteria (Wave 3 gate of the workflow passed).


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


## Coverage slice

Full matrix: /home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/brainstorms/346-ponytail/workflow-report/nested/reflect-1/artifacts/coverage-matrix.yaml (109 inferred rows, coverage_pct_union 0.789, S_dev_density 0.211, coverage_degraded parsed-sparse). Unmatched by containment: INF-001, INF-003, INF-021, INF-023, INF-024, INF-036, INF-040, INF-041, INF-042, INF-051, INF-057, INF-069, INF-070, INF-072, INF-087, INF-099..INF-106. Mapper advisory notes: INF-051 (verdict exit 2 on inconsistency not in Task 5), INF-077 (MAJOR (FR-8 GAP) graded-minor test absent from Task 2).

Return format: a YAML list of findings, each {id, severity: blocking|minor (blocking = the plan as written would deliver wrong behaviour, miss a required in-scope deliverable, or contradict an owner decision; else minor), plan_task, spec_ref (source.md:<line>), evidence (quoted plan or spec text with file:line), claim_tag: grounded|INFERRED, recommendation (file + change + verifier)}, then confidence 0.00-1.00 and one line naming what you actively checked.
