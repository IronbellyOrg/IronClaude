# Reviewer 3 brief: refactorer lens (model class: opus)

Mode: UC-1 pre-execution. You audit a PROPOSED plan (tasklist) against its driving spec, read-only. Do not run commands. Return findings only; the orchestrator persists them.

Spec: /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/source.md
Tasklist under review (read it in full): /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/tasks/to-do/TASK-WF-refactorIronClau-20261102-162730/TASK-WF-refactorIronClau-20261102-162730.md

Your lens: structure and execution risk. Check that each task names the right files and anchors, that mirrors (plugins/superclaude, .claude via make sync-dev) stay consistent, that task order and dependencies are safe, and that nothing the plan tells the executor to run or write is wrong for this repository. Check every file path the plan names against the repo (Read/Grep/Glob). Classify each divergence under the 4-category taxonomy (authorized expansion, necessary deviation, drift, regression) with a one-line rationale and a file:line citation.

## T1 card excerpt

Verbatim from /home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths/.dev/reflect/pre-refactorIronClau-20261102175540/t1-card.md, section "Structural / tech-debt section (refactorer lens)":

- S1: Mirror discipline is correct. Task 6 copies src to plugins and runs `make sync-dev` before `make verify-sync` and the parity tests (plan line 116). tests/commands/test_routing_plugin_parity.py:29-47 enforces byte parity for the sc-recommend skill tree and for commands/recommend.md, so the plan's Constraint (plan line 21) is grounded and its test choice is correct.
- S2: Internal temporary checkouts are protected only by "unchanged" assertions (Task 7, plan line 135). No task runs their tests (tests/skills/test_implement_retry_revert.py, tests/cli/reflect/test_isolate_reviewers_cli.py, tests/troubleshoot/backtest/). Because those files are not edited the risk is low, but "keep working without Orca" is asserted by non-change, not by an observed run.
- S3: Line-number drift avoided: tasks anchor edits by section heading and quoted text, not line numbers (Tasks 2, 4, 5). That avoids the recurring defect "bare line citations drift once earlier tasks edit the same file" (docs/memory/reflect/deviation-patterns-IronClaude.md:12).
- S4: The Orca command surface is pinned to verified help output (plan line 23), and the unverified `orca worktree rm` selector syntax is deferred to a `--help` check inside Task 2 (plan line 58).
- S5: Tasks 2 and 3 both edit CLAUDE.md; Task 3 depends on Task 2, so there are no concurrent edits to one file.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-02T17:55Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths projectPath=/home/coder/workspaces/worktrees/IronClaude/orca-default-worktree-paths

### tests/commands/test_routing_plugin_parity.py:29-47

```python
def test_sc_recommend_plugin_tree_mirrors_src_plus_guide():
    src, plug = _rels(_SRC_SKILL), _rels(_PLUG_SKILL)
    assert "refs/HOW-WE-WORK.md" not in src
    assert plug - src == {"refs/HOW-WE-WORK.md"}
    assert src <= plug, src - plug
    _, mismatch, errors = filecmp.cmpfiles(
        _SRC_SKILL, _PLUG_SKILL, sorted(src), shallow=False
    )
    assert not mismatch and not errors, mismatch + errors
    assert filecmp.cmp(_GUIDE, _PLUG_SKILL / "refs/HOW-WE-WORK.md", shallow=False)


@pytest.mark.parametrize("name", ["help", "recommend", "workflow", "implement"])
def test_readme_listed_command_mirrors_match_src(name):
    """T70: the four commands src/superclaude/commands/README.md says are mirrored."""
    src = _REPO / "src/superclaude/commands" / f"{name}.md"
    plug = _REPO / "plugins/superclaude/commands" / f"{name}.md"
    assert f"`{name}.md`" in (src.parent / "README.md").read_text(encoding="utf-8")
    assert filecmp.cmp(src, plug, shallow=False), f"{plug} differs from {src}"
```

### src/superclaude/skills/sc-recommend/SKILL.md:128

```markdown
The checkout paths (row 7) resolve under the repository root (`git rev-parse --show-toplevel`); the project paths (row 5) are read from cwd. If the user's cwd is a worktree under `.dev/worktrees/<name>/`, that command returns the worktree's root, so both resolve against **that worktree**. The skill must remain worktree-aware.
```

### tests/skills/test_implement_retry_revert.py:611-614

```python
def test_revert_targets_ledger_worktree_only(tmp_path):
    main = make_repo(tmp_path)
    wt = main / ".dev/worktrees/wt"
    git(main, "worktree", "add", "-q", str(wt), "-b", "wtbranch")
```

## Coverage slice

| Requirement | Matched task | Status | Grounding |
|---|---|---|---|
| INF-003 every tracked file | Task 1 | containment 0.75; edits in Tasks 2-7 | source.md:1 |
| INF-009 source of truth src/superclaude | Task 5 | containment 1.0 | source.md:1 |
| INF-010 run make sync-dev | Task 6 | containment 1.0 | source.md:1 |
| INF-011 never stage .claude mirrors | none (lexical) | content-level covered | source.md:1; plan Constraints |
