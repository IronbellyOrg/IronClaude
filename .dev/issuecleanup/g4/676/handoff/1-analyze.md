# Analyze handoff

Command: /sc:analyze src/superclaude/cli --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/676/analyze
Task ID: task_4967a5b7bfc8
Dispatch ID: ctx_d2cf6a4077ae
worker_status: succeeded
Deliverables: .dev/issuecleanup/g4/676/analyze/analyze-report.md and .dev/issuecleanup/g4/676/analyze/return-contract.yaml
Decision: source confirms no backups for core files, agents and templates; existing guide warnings cover core and agents but omit templates, and the helper docstring still overpromises.
Scope: static inspection only; no UV, tests, installs, commits or GitHub writes.
Guard: installed analyze command has Unattended mode; project command copy does not exist; standalone flag and exactly one report directory supplied.
Applied coordinator message IDs: none (mailbox empty at both checkpoints).
Next Command: none. Remaining brief steps: finalize findings and run the independent fresh-context review.
