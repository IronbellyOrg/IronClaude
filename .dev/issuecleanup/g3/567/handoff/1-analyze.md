# Analyze handoff

- Command: `/sc:analyze src/superclaude/cli/swarm --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/567/analyze`
- Task ID: task_b658c08b8155
- Dispatch ID: ctx_b1b35c6006df
- worker_status: succeeded
- Deliverable: `.dev/issuecleanup/g3/567/analyze/analyze-report.md`
- Contract: `.dev/issuecleanup/g3/567/analyze/return-contract.yaml`
- Decision: issue #567 is in-progress; the current checkout still advertises unwritten raw files, while draft PR #756 carries reconciliation into master.
- Evidence revision: a7ae3dd30fcf88aaab655c37e94e58e121c2d863.
- Limits: static review only; no test/environment run, live-provider call, GitHub mutation, staging or commit.
- Applied coordinator message IDs: none (inbox empty at checkpoints).
- Next Command line: none.
- Remaining brief deliverables: finish findings.md, obtain independent qa.md and send worker_done exactly once.
