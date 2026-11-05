# Reviewer 1 brief: persona analyzer, model sonnet (UC-1 pre-execution plan review)

Audit target: the plan `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/TASK-WF-closeIronbellyOr-20261104-084334.md` (121 lines; Read it in full) against its spec `.dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/source.md` and the design it implements, `.dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md`. Lens: root cause and evidence. Question: will executing these six tasks, as written, deliver the design and the source checks, and is every task claim true against the repo? Classify each divergence as authorized | necessary | drift | regression (plan-vs-spec), or route it to a grounding gap.

## T1 card excerpt

From `reflection-card.yaml` (verbatim):

```yaml
  - id: F-3
    kind: coverage-by-constraint
    claim: "INF-002, INF-003 and INF-009 (ledger decision, ledger alternative, no-change list) are carried only in the plan's Constraints section; INF-001 (the design reference) only in the Goal line. The containment matcher scores tasks only, so they show as unmapped although the plan states them."
  - id: F-4
    kind: risk
    claim: "Task 5 runs the real `claude plugin` commands under a throwaway HOME; whether the `claude` CLI needs credentials or writes outside that HOME is unverified, and a network clone of DietrichGebert/ponytail (about 13 MB) may hit the 30 s budget."
  - id: F-5
    kind: ordering
    claim: "Task 2 depends on Task 1 although the code change is independent; the dependency is only the shared test file, which is a safe serialisation."
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
    if failed:
        return True, (
            f"⚠️  Plugins: not installed: {', '.join(failed)}; "
            "rerun `superclaude install` to retry"
        )
    return True, f"✅ Plugins: installed {', '.join(wanted)}"
```

### .dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-084334/TASK-WF-closeIronbellyOr-20261104-084334.md:17-25

The plan's Constraints section (Read it): scope list, data-only rule, single source, never touch `~/.claude`, non-fatal, ledger decision with the off+ledger-off alternative, `.dev/tasks` staging.

### .dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md:263-289

The design's Tests and Acceptance Criteria (T1-T6, AC-1..AC-3, AC-M1..M3). Compare each to the plan's tasks.

## Coverage slice

| Requirement | Task | Status | Grounding |
|---|---|---|---|
| INF-001 implement the design in merged-requirements.md | none (Goal line) | unmapped by containment | source.md:1 |
| INF-002 ledger Outcome 2 + mode off | none (Constraints) | unmapped by containment | source.md:1 |
| INF-003 off+ledger-off alternative step | none (Constraints) | unmapped by containment | source.md:1 |
| INF-005 failure-label fix ≤5 lines | Task 2 | covered | source.md:1 |
| INF-009 no change to main.py, update.sh, doctor.py, output styles, .claude/ | none (Constraints) | unmapped by containment | source.md:1 |

Return a reviewer card (YAML) with: reviewer, persona, model, findings (id, claim, evidence as file:line, deviation_class or grounding_gap, severity blocking|minor, recommendation), self_reported_confidence. Do not write files.
