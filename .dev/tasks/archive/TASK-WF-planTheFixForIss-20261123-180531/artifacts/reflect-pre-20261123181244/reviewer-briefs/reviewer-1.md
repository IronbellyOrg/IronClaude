# Reviewer 1, analyzer, pre-execution

## T1 card excerpt
Risks for independent review: distinguishing a caller template equal to the bundled template from a defaulted template; avoiding empty-command suppression for caller-owned values; count and comma/space-path parsing without modifying siblings. All are constrained by plan Task3. No new helper/framework/dependency or global validation promised. A future executor must implement within this boundary or surface infeasibility, never silently expand scope.

## Grounding hunks
codegraph run state: index_state=fresh checked_at=2026-11-23T18:12:44Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s projectPath=/home/coder/workspaces/worktrees/IronClaude/bug-swarm-refactor-find-recommends-unavailable-s

### src/superclaude/cli/swarm/commands.py:2129-2144
```python
        succeeded_final_paths = [
            w.final_path
            for w in normalized_workers
            if w.status == "success" and w.final_path
        ]
        next_cmd_subs = dict(inline_job.recommended_next_command_substitutions or {})
        next_cmd_subs.setdefault(
            "suspect_files",
            ",".join(succeeded_final_paths)
            if succeeded_final_paths
            else "<no-bare-files>",
        )
        next_cmd_subs.setdefault(
            "compare_files",
            ",".join(["<existing-review>", *succeeded_final_paths]),
        )
```
### src/superclaude/cli/swarm/lenses/refactor_find.py:49-53
```python
    default_workers=3,
    default_target_line_cap=4000,
    suspect=False,
    tier="T2-code",
    recommended_next_command_template=("/sc:code-review --apply {compare_files}"),
```
### src/superclaude/commands/adversarial.md:39
```text
- `--compare`: Comma-separated file paths (2-10 existing files)
```
Review root is the live current isolated user worktree, not a reviewer snapshot (reviewer_isolation=disabled). Review only the proposed plan, no implementation expected. Full candidate at .dev/tasks/to-do/TASK-WF-planTheFixForIss-20261123-180531/TASK-WF-planTheFixForIss-20261123-180531.md; source at sibling source.md. Read them directly. Explicit no implementation/commit/push. Inspect concrete correctness/scope defects and executable acceptance requirements, not stylistic preferences. Return full structured card to parent for persistence, binary PASS/FAIL, one row per finding with Blocking Decision/Missing/Safety or minor Medium/Note plus label HIGH/MEDIUM/LOW. Do not edit, execute commands, spawn or invoke skills. No findings quota. Identify scope and why no defect when zero. Include any limits. Do not mistake lexical matching misses for absent semantic requirements.

## Coverage slice
Own replacement and refactor-only caller/sibling preservation: INF001, INF002, INF003. Raw exact clauses in ../requirements.json (all source.md:1); machine matches respectively Task2 ratio0.6471, Task3 ratio0.8571, none ratio0.5714. Manual coverage lead for INF003: Task3 lines60,69. Task3 also requires count/path guards and intact result statuses. These are obligations, not witnessed repaired behavior. Independently check feasibility of the existing shared-block edit. Do not inherit T1 PASS as a conclusion.
