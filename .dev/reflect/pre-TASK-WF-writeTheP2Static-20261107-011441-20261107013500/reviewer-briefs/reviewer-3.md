# Reviewer 3 brief (persona: refactorer; model slot: opus)

Mode: UC-1 (pre-execution plan review). You review a PROPOSED plan for structure and executability. Read-only: never edit, write or run anything; return findings only. Grounding root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2 (all relative paths below are under it).

Inputs:
- Plan under review: `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/TASK-WF-writeTheP2Static-20261107-011441.md` (read it whole).
- Driving brief: `.dev/tasks/to-do/TASK-WF-writeTheP2Static-20261107-011441/source.md`.
- The P1 static plan it models: `.dev/tasks/done/TASK-WF-writeTheP1Static-20261105-033458/TASK-WF-writeTheP1Static-20261105-033458.md`.
- Repo rules: `CLAUDE.md` (never stage `.claude/` paths; never hardcode `src/superclaude/` paths in installed primitives; plugin mirrors).

Persona focus (refactorer): the plan is executed task by task by `/sc:implement`, whose reviewer sees only one task plus the Constraints. Check that each task stands alone (names every file it edits and the source section it needs), that `Depends on:` lines are right (a task that adds a nested call to a command must depend on the task that gives that command `--unattended`, unless the callee is a P1 command), that no two tasks edit the same lines in conflicting ways (for example `tests/skills/test_worker_contract.py`, `WRITE_VERB_CLASSIFICATION` entries, `EXPECTED_NESTING`), that each Check ADDITIVE claim is achievable for the edits the task asks for (an edit that must change an existing line in a command file breaks the check), that the mirror rule is applied exactly to the pinned files and no others, and that the scope matches the brief (no unrequested edits). Read the command and skill files a task edits when you need to confirm an anchor (a heading, a table, a line the task says exists).

Output: a YAML card with `findings:` (each: id R3-Fn, severity P1 | P2 | P3 as defined: P1 = the plan would produce wrong behaviour or violate a stated rule; P2 = a task is incomplete, mis-ordered or an AC cannot catch its defect; P3 = wording/minor), claim, evidence as file:line list you actually read, deviation_class, suggested_fix), plus `self_confidence` (0-1) and a `self_audit` paragraph. Every claim must cite file:line you read; tag anything else [INFERRED].

## T1 card excerpt

```yaml
  - id: T1-F2
    severity: P3
    claim: "Task 1 tells the executor to 'drop only the case that relied on equality' in test_p1_set_check_fails_on_a_missing_extra_or_repeated_command, but under the new subset rule every existing case still fails, so the instruction has no target and invites an unneeded edit."
  - id: T1-F4
    severity: P3
    claim: "Task 16 moves tasklist Stage 10.5 reflect outputs under --unattended to <report-dir>/nested/reflect-<n>/ (D-P2-13); readers of the old folder are only checked by running tests/tasklist."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-07T01:31:09Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2 projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P2

### tests/skills/test_worker_contract.py:1061-1072

```python
def test_only_brainstorm_lists_nested_commands():
    listed = {c: e["nested"] for c, e in UNATTENDED_EXPECT.items() if e.get("nested")}
    assert listed == {"brainstorm": ["analyze", "adversarial"]}


def test_nested_check_fails_on_nested_text_without_a_nested_list():
    # workflow's reflect step runs without the flag, so workflow lists no nested name.
    section = _unattended_section("workflow")
    expect = UNATTENDED_EXPECT["workflow"]
    _check_nested_text(section, expect)
    with pytest.raises(AssertionError):
        _check_nested_text(section + "\nnested/reflect-<n>/\n", expect)
```

### src/superclaude/commands/brainstorm.md:156

```markdown
- **Research.** Under `--unattended`, research enrichment is off: the automatic route and an explicit `--research light` or `--research deep` are skipped, each recorded in `enrichment_used` with `quality_tier: skipped` ...
```

## Coverage slice

| Requirement | Plan location | Status |
|---|---|---|
| INF-004 P1 static plan as the model (source.md:3) | plan:25-43, Task 1 | covered |
| INF-019 exact files, observable ACs, tests per task (source.md:16) | Tasks 1-21 | covered (verify task independence) |
| INF-020 installed-path rule, pinned mirrors, sync-dev (source.md:16) | plan:23-24, Tasks 6, 17, 21 | covered |
| INF-028 no execution, nothing staged under .claude/ (source.md:18) | plan:22 | covered |
