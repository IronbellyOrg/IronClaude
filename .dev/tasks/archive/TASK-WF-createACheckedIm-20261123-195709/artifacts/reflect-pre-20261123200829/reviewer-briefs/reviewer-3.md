# Refactorer review brief

## T1 card excerpt

The two public producers are the `validate_lenses_cmd` docstring and the `scaffold_cmd` lens-option help in `src/superclaude/cli/swarm/commands.py`; they are registered by `swarm_group.add_command` in `src/superclaude/cli/swarm/__init__.py`. The plan changes no registration or parser option.

The current `_apply_custom_prompt_dir` in `preflight.py` gates directory reading on lens custom and a nonempty field. `_custom_prompt_dir_lens_failures` in `schema.py` explicitly allows inline custom prompts without a directory. Plan constraints and Tasks 3/4 preserve these semantics, injection guards and metadata rules.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-23T20:08:34Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-568-swarm-help

### src/superclaude/cli/swarm/schema.py:700-706

```python
    The reverse direction (``lens=='custom'`` without
    ``custom_prompt_dir``) is intentionally not enforced here because
    FR-021's wording ("When ``lens==custom`` AND ``custom_prompt_dir``
    set...") leaves room for a ``lens='custom'`` spec to derive its
    prompts from inline ``prompt.system`` / ``prompt.user_template``.
    The T02.05 directory reader handles the FR-021 path semantics
    after this rule has confirmed the binding.
```

Read candidate `../../../TASK-WF-createACheckedIm-20261123-195709.md`, source `../../../source.md`, `../coverage-matrix.md`, and the governing template `/home/coder/.claude/skills/sc-workflow-protocol/refs/00_mdtm_template_simple_task.md`. Final verification and independent final review are executor-owned by that template; it forbids verification-only tasks. Judge any missing-review-step candidate against that actual contract, not an invented requirement for a fifth task.

## Coverage slice

| Requirements | Concern |
|---|---|
| INF-002, INF-003, INF-007, INF-008, INF-010, INF-011 | Scope, unchanged behavior, review/evidence ownership and counters |

Persona: refactorer. Review the plan for unnecessary mutation, dependency errors, false statements, missing deliverables and scope leakage. Do not redesign the process or expand the fix. Distinguish a report filename preference from a missing independent-review obligation; determine consequence from the actual executor contract. Check all constraints remain visible to each task reviewer. Return PASS/FAIL and every concrete finding with HIGH/MEDIUM/LOW label, Blocking (Decision/Missing/Safety) or Medium/Note grade, evidence, consequence and narrow remedy. Zero findings is valid with scope and reasons. No commands, Git, file writes, skills or spawning; parent persists your card.
