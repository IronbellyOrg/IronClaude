# Reviewer 2 brief: persona qa (model class haiku alias = glm-5.3)

Mode: UC-1 pre-execution review of a proposed plan. Working tree: /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357 (read-only for you).
Spec: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/source.md
Tasklist under review: .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md
Lens: coverage and acceptance. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also check every task's acceptance criteria are observable, testable, and actually prove the issue's Done-when bullets. Assume mistakes exist.

## T1 card excerpt

- Issue Done-when bullet 1 (block + message naming uv run python and jq): Task 1, Task 2.
- Bullet 2 (allow uv forms; text-only mentions not blocked): Task 1 rules, Task 2 allowed table.
- Bullet 3 (tests incl. &&, ; and |): Task 2 second acceptance criterion.
- Bullet 4 (install registers; fires for subagents): Task 3, Task 4 (install), Task 7 (subagent).
- Bullet 5 (read-parse.md:8): Task 5.
- Bullet 6 (fresh session blocked and pointed to uv run python or jq): Task 7.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T13:08:56Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357 projectPath=/home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357

### .dev/tasks/to-do/TASK-WF-implementIronbel-20261104-130647/source.md:1
```text
Implement IronbellyOrg/IronClaude issue #357: block bare python, python3, pip and pip3 in Bash tool calls with a PreToolUse hook, because the UV-only rule is text-only and agents and helper subagents keep breaking it. Read the issue in full first (gh issue view 357 --repo IronbellyOrg/IronClaude): it lists the allowed cases (uv run python, uv pip, uvx, commands that only mention python in paths, patterns or quoted text), the files (src/superclaude/hooks/hooks.json, plugins/superclaude/hooks/hooks.json, src/superclaude/hooks/scripts/, plugins/superclaude/hooks/scripts/, src/superclaude/cli/install_hooks.py, the existing PreToolUse freshness-pre-edit hook as the model), the bare call to replace in src/superclaude/skills/sc-troubleshoot-protocol/refs/probe-packs/read-parse.md:8, and the Done-when list, which is the acceptance criteria.
```

### Issue #357 Done-when (quoted verbatim in the tasklist Constraints, first bullet; source: gh issue view 357 --repo IronbellyOrg/IronClaude)
```text
- A PreToolUse `Bash` hook blocks a command that runs bare `python`, `python3`, `pip` or `pip3`, with a message naming `uv run python` and `jq`.
- It allows `uv run python`, `uv pip` and `uvx`, and does not block commands that only mention python in arguments, paths or quoted text.
- Tests cover both the blocked and the allowed cases, including commands chained with `&&`, `;` and `|`.
- `superclaude install` installs and registers the hook, and it fires for subagent Bash calls.
- `read-parse.md:8` uses `uv run python`.
- A fresh session that tries `echo '{}' | python3 -c 'import sys,json; json.load(sys.stdin)'` is blocked and pointed to `uv run python` or `jq`.
```

### tests/cli/test_install_hooks.py:699-726
Precedent: codegraph hook registration test parametrized over src and plugins hooks.json; packaged, listed and mirrored test.

### tests/hooks/test_freshness_pre_edit_create_case.py:24-35
Precedent subprocess runner for a hook script with HOME in tmp_path.

### Makefile:308-325
verify-sync installer-registration check: every src/superclaude/hooks/scripts/*.sh and *.js must be in `_FRESHNESS_SCRIPTS`.

## Coverage slice

Full matrix: .dev/reflect/pre-TASK-WF-implementIronbel-20261104-130647-20261104130837/artifacts/coverage-matrix.yaml (read it). Summary: parsed_count 0, inferred_count 12, coverage_pct_union 0.75, unmapped by rule INF-001, INF-002, INF-006 (semantic notes say INF-001 and INF-006 are substantively covered, INF-002 partially).

| Requirement | Matched task | Status |
|---|---|---|
| INF-003 uv run python allowed | Task 1 | covered |
| INF-004 uv pip allowed | Task 1 | covered |
| INF-005 uvx allowed | Task 1 | covered |
| INF-006 mentions in paths, patterns, quoted text not blocked | none (0.5) | unmapped by rule |
| INF-007 both hooks.json files | Task 1 (real: Task 3) | covered |
| INF-008 both scripts dirs | Task 1 | covered |
| INF-009 install_hooks.py | Task 3 | covered |

Return findings as a list: id, severity (blocking or minor: blocking = wrong behaviour, false claim, missing required deliverable, security or data-loss risk; minor = wording, style, nit), task number, tasklist line, evidence (file:line you Read), and the concrete fix. If nothing blocking, include a short self-audit. Do not write any file.
