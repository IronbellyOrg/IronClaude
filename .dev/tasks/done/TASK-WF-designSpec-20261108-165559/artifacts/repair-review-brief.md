# Authorized repair review

## Inputs and authorization

Checkout: /home/coder/workspaces/worktrees/IronClaude/issue-441.
Package: .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559.
Original failed FINAL: artifacts/final-review.md within that package. Repair scope, direct user authorization and checks: artifacts/final-repairs.md and artifacts/final-repair-probes.md. No defect is waived. User separately approved insertion before E and the seven-entry history-only acceptance in artifacts/spec-deviations.md:31. Do not trust the implementer's report.

## Review criteria

Read real current files and compare against backup ref refs/superclaude/repairs/issue-441/pre-final-fixes. Verify both original FINAL findings are fixed, with exact live evidence and one yes/no answer for each of the four qa.md checklist questions for any new finding. In particular:
- Shared data validation must reject a real FIFO without blocking, preserve symlink refusal/type/uid/mode checks, return conflict through install_l2 and owned-hook l2_status, preserve the FIFO and leave no private files. Inspect new bounded subprocess tests and saved before/after logs. Do not run tests or builds.
- Compare progress.md with artifacts/progress-before-final-repairs.md. Exactly eight note relocations must correct pathname parsing without changing existing verdicts, citations or Rulings. Later explicitly authorized records may be appended. Every real delivery path must be covered; inspect the real helper manifest and disposable-copy sensitivity check, not only its prose.
- Check actual seven-commit order, dedicated repair before E, E still last/separate, E product diff limited to original off-refusal additions, IR7_REFUSE False. Both protected tests and pinned plan/source unchanged. Scope acceptance waives only literal history count.
- Review the repair against original T6 and T7 ACs (plan lines 90-109) and T12 ACs (159-168). Cite every mark. Do not confuse the historical original failed FINAL with the current end state.

## Output template

Create and populate artifacts/repair-review.json as a JSON object with keys:
- findings: array of objects {id, checklist: {missing, false, harmful, constraint}, anchor, detail, fix}
- original_findings: object mapping F-FINAL1 and F-FINAL2 to resolved/open with citations
- acceptance_criteria: object mapping T6.AC1,T6.AC2,T7.AC1,T7.AC2,T7.AC3,T12.AC1,T12.AC2,T12.AC3 to met/unmet plus citations; keep history criterion literally unmet with scoped acceptance
- verdict: pass or issues; accepted history count alone cannot fail
- self_audit: checked items and verification limits, particularly zero-finding audit.

Write only that output. If your higher-priority instructions prohibit any report writes, return that exact JSON directly, at most 6000 characters so it is not truncated. No edits to source, ledger, config or git state. No tests, builds, pushes or PRs. No delegation. Every tool output <=40 lines, Read in <=35-line chunks; never cat retry/adversarial/reflect files. Return the output path plus two result lines if written.
