Task F{N}: apply review findings to the Phase {N} spec and generate its tasklist with /sc:workflow.

First read /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/codegraph-migration/orchestration/README.md (shared rules; binding). Then read `.dev/codegraph-migration/review/review.md` and the Phase {N} spec: {SPEC}.

Change:
1. Apply every review finding that targets the Phase {N} spec (and, for N=2, the Coder handoff files under `.dev/codegraph-migration/handoff/`). Verify each finding against the source before applying; if a finding is wrong, reject it with evidence. Append a `## Review resolution` section to the spec: finding id, applied/rejected, one-line reason. Cross-phase findings: apply only the hunk that belongs to Phase {N}; never edit another phase's spec.
2. Then invoke the `/sc:workflow` command on the revised spec: `/sc:workflow {SPEC} --depth standard --handoff none` (positive return: produces the checked tasklist package with acceptance criteria that `/sc:implement` executes). It creates `.dev/tasks/to-do/TASK-WF-<subject>-<timestamp>/`. Read its advisory reflect result; fix any plan defect it reports by editing the generated plan, not by rerunning blindly.
3. Make sure the generated tasklist keeps: a test command and a commit point after every task group, the issue #323 progress-comment step at each commit point, the decision rules (simple self / mid `/sc:adversarial --compare ... --depth quick` / complex `/sc:adversarial --compare ...`), and a final full verification task.
4. Write `.dev/codegraph-migration/review/F{N}-result.md`: the tasklist package path, the reflect status, and the list of autonomous decisions taken.

Constraints: no source edits; do not implement. Stage nothing and commit nothing (the coordinator stages `.dev/tasks`).

Ownership: Phase {N} spec, its handoff files when N=2, the new `.dev/tasks/to-do/TASK-WF-*` package /sc:workflow creates, `.dev/codegraph-migration/decisions/F{N}-*`, and `.dev/codegraph-migration/review/F{N}-result.md`.

Observable acceptance: spec has a Review resolution section; the task package exists with its plan `<id>.md` and `progress.md`; F{N}-result.md names the package path and reflect status.
