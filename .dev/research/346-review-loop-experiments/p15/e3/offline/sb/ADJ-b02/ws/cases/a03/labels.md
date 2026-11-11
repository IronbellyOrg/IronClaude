## Label A
blocking: no
sentence: Fails: the finding itself says which text wins is a guess; WC-11 is in the unattended-mode contract, SA-1 freezes paths only without --unattended, and line 85 already treats the fixed .claude-audit path as a one-audit-per-worktree limit under WC-11, so no stated texts force a wrong build.
evidence: line 69 WC-11; line 146 SA-1 'Without --unattended, every ... output path ... stays as it is today'; line 85 'output dir is fixed, so one audit per worktree at a time (WC-11)'
confidence: high

## Label B
blocking: no
sentence: An implementer who follows WC-11 as written would give timestamped or slugged default output paths to commands in every mode, which conflicts with SA-1 and the fixed paths in the rows; but WC-11 sits in the worker-contract requirements and has no scope statement, so which of the two texts governs needs a guess, and the finding is Medium, not blocking.
evidence: L69 WC-11: 'Default output paths carry a timestamp or the slug the coordinator passes'; L146 SA-1: 'Without --unattended, every ... output path ... stays as it is today'; L85 cleanup-audit row: 'output dir is fixed'; L86 index-repo row: 'PROJECT_INDEX.md (location implied)'; L87 init-lite row.
confidence: low
