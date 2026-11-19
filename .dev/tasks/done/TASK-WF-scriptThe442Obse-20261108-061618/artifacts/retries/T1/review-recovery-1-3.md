Earlier blocking findings: none given.

T1.AC1 met. Citation: T1.AC1@/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/selftest.sh:137-142. `bash -n` passed on lib.sh and selftest.sh. A full run of `bash .dev/issues/442/scripts/selftest.sh` printed `SELFTEST_OK` and exited 0.

T1.AC2 met. Citation: T1.AC2@/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/lib-selftest.sh:21-23 (case gh-fork-repo: the stub log holds `--repo IronbellyOrg/IronClaude`) and lib-selftest.sh:39-44 (case gh-fork-refuse: `gh_fork api repos/SuperClaude-Org/x` exits non-zero and the stub log is absent). Both cases printed OK in the full run. The implementation is at lib.sh:42-85.

T1.AC3 met. Citation: T1.AC3@/home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/lib-selftest.sh:57-64 (cases state-get-num, state-get-spaces with the value "$T/wt one", state-get-url and state-get-absent, all OK). The implementation is state_set and state_get at lib.sh:29-40. It uses awk, and the only `eval` hit in lib.sh is the comment at line 37.

No blocking findings.

Notes, not blocking:
- main_checkout at lib.sh:87-91 prints the first `worktree` line whose path does not end in `/.git`, not strictly the first line. The result is the same for a normal checkout.
- The saved artifacts/t1-selftest.txt is stale, dated 2026-11-09 and without the repo-view cases. I judged the live run, not that file.
- A standalone run of lib-selftest.sh without the stubs on PATH fails the gh-fork-repo cases because it calls the real gh. selftest.sh does put the stubs on PATH, so this is not a defect in the task.
