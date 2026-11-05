# Reviewer 3 brief: persona refactorer, model opus (UC-1 pre-execution plan review)

Audit target: the plan `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/TASK-WF-closeIronbellyOr-20261104-084334.md` (121 lines; Read it in full) against its spec `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/source.md` and the design `.dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md`. Lens: structure, task boundaries, minimal-risk change, executability by `/sc:implement` (each task is reviewed alone with only the Constraints). Check: is each task independently implementable and reviewable, are dependencies right, does any task invite scope creep or a change outside the allowed file list, and is the 5-line cap on `install_user_setup.py` achievable with the described shape. Classify each divergence as authorized | necessary | drift | regression (plan-vs-spec), or route it to a grounding gap.

## T1 card excerpt

From `reflection-card.yaml` (verbatim):

```yaml
  - id: F-5
    kind: ordering
    claim: "Task 2 depends on Task 1 although the code change is independent; the dependency is only the shared test file, which is a safe serialisation."
  - id: F-4
    kind: risk
    claim: "Task 5 runs the real `claude plugin` commands under a throwaway HOME; whether the `claude` CLI needs credentials or writes outside that HOME is unverified, and a network clone of DietrichGebert/ponytail (about 13 MB) may hit the 30 s budget."
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-04T08:47:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin

### src/superclaude/cli/install_user_setup.py:288-311

```python
    failed = []
    for args in commands:
        remaining = deadline - time.monotonic()
        if remaining < 2:
            failed.append(" ".join(args[1:3]) + f" {args[3]} (time limit)")
            continue
        try:
            result = subprocess.run(
                [claude, *args],
                capture_output=True,
                text=True,
                timeout=remaining,
                stdin=subprocess.DEVNULL,
            )
            if result.returncode != 0:
                failed.append(args[3])
        except (OSError, subprocess.SubprocessError):
            failed.append(args[3])
```

### .dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md:89-111

The design's proposed label-fix shape (`name = args[3] if args[1] == "marketplace" else args[2]`) and its "one added line, three changed lines" estimate.

### .dev/releases/current/v5.0.0/post-release/scan/C-install-surface.md:125-147

The throwaway-HOME recipe Task 5 points at (env -i, curated PATH, Orca stubs). Check that Task 5's narrower use (calling `apply_settings_defaults` and `install_plugins` via `uv run python` from the checkout) is consistent with it.

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-005 failure-label fix ≤5 lines | Task 2 | covered | source.md:1 |
| INF-009 no change outside the five delivery files | Constraints only | unmapped by containment | source.md:1 |
| INF-011 manual AC-M1 never touching ~/.claude | Task 5 | covered | source.md:1 |

Return a reviewer card (YAML) with: reviewer, persona, model, findings (id, claim, evidence as file:line, deviation_class or grounding_gap, severity blocking|minor, recommendation), self_reported_confidence. Do not write files.
