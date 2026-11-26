## Verdict
still-relevant. Issue [699](https://github.com/IronbellyOrg/IronClaude/issues/699), the claim worktree's delayed agent launch, is OPEN with zero comments at review time (2026-11-24). Assessed checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`.

The report is partly stale, but its core policy mismatch remains:
- The actual create argument list still omits `--agent`: `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:695-710`. Copying follows in `finish` at lines 558-576, reached after creation at lines 737-748. The docstring at lines 23-40 explains the intentional copy-before-launch sequence. The direct claim route separately launches later, rather than making the create start an agent.
- `CLAUDE.md:305-314` still requires an agent on creation without naming the claim exception. The distributed global instruction at `src/superclaude/core/CLAUDE.md:55-61` likewise requires create-with-agent. In contrast, `src/superclaude/core/WORKER-CONTRACT.md:299` explicitly documents creating/copying first and then starting the single worker. PR 701, merged as `0a46644576a31f0f62b9629b0f095b213027cdf6`, supplied this contract clarification and explicitly left issues 698 and 699 open; PR 697 itself was CLOSED, not merged, after PR 700 restored the package.
- The issue's uncertainty about hook coverage is now answered at the source level: `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh:60-61` explicitly names the script's subprocess as outside the hook. The implementation examines only `tool_input.command` at lines 345-349; the claim helper directly invokes `subprocess.run` at `orca_worktree.py:145-154`. This is not a runtime observation or a security guarantee.
- The no-agent behavior already has test definitions: `tests/skills/test_issue_orca_worktree.py:283-298` forbids `--agent`; lines 864-886 pin the exact create and plain-tab close calls; lines 899-907 and 921-935 check that tab handling follows the copy. `tests/skills/test_worker_contract.py:431-432` pins the contract exception wording. Therefore do not describe all required tests as absent or the issue as wholly untouched.

The issue records the owner's default as keeping a documented exception. That is the smallest remaining completion path, not authority granted here to change policy. No verified current implementation PR was found by `gh pr list --state all --search '699'`: its one returned PR was merged 701, which disclaims fixing this issue. Static analysis is saved in `analyze/analyze-report.md`. Tests and live one-agent counts are UNVERIFIED in this run; no UV, install, worktree creation, source changes or GitHub writes were performed.

## Complexity and size
Complexity: simple. Size: S. The recorded default needs bounded policy alignment and targeted verification of existing copy-first/one-launch behavior, not a new worktree lifecycle; choosing the alternative redesign would require re-estimation.

## Priority
P2. Conflicting mandatory instructions can misdirect future claim work into starting an agent before the copy and launching again afterward; source shows an intentional functioning design shape, not an observed outage, data loss, or release blocker. No verified numbered issue is hard-blocked by this policy cleanup.

## Concrete next steps
1. Have the owner confirm completion on the recorded documented-exception path, rather than treating the issue's historical note as new authorization. Name the claim helper's copy-before-launch exception in both the repository worktree policy and the installed global policy source, preserving the existing worker-contract sequence.
2. Keep the existing no-agent and copy-order tests, and verify or add focused sequence coverage for create, copy and exactly one later launch on the relevant coordinator/direct-claim routes. Include failure handling: a failed copy or launch must not be presented as a successful agent-backed worktree. Existing tests have been inspected, not run here.
3. Retain the hook's explicit subprocess coverage limitation. Do not add `--agent` to the create argument list by itself; a redesign must remove or replace the later launch and address access to the issue files before starting the one agent.
4. Before closure, record the chosen policy and observed focused test results. If the owner chooses the alternative create-with-agent design instead, also perform the issue's requested throwaway-issue live count in an independently authorized run. Live counts and hook behavior on an actual claim remain UNVERIFIED here.
5. Coordinate terminology and claim-worktree separation with the topology debate cited by the issue. `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/VERDICT.md:22,67` recommends separating claim agents from the standing Coordinator worktree or limiting concurrency. This is design context, not evidence that issue 699's fix is implemented or approved.

## Dependencies
No verified hard dependency on another numbered issue, and no verified numbered issue blocked by 699. It needs the owner's policy choice and verification evidence, not completion of the separate security work in issue 698. Issue 289 is broader worktree-policy coordination; issue 655 is the historical orchestration umbrella, not a proven prerequisite.

## Related issues
- [698](https://github.com/IronbellyOrg/IronClaude/issues/698), OPEN: sibling follow-up from PR 697 covering release-worker protection and the assignee shortcut, not this worktree policy mismatch. Read live body.
- [289](https://github.com/IronbellyOrg/IronClaude/issues/289), OPEN: broader decision about parallel-session branches and worktrees. Read live body; its old placement examples are not treated as current instructions.
- [655](https://github.com/IronbellyOrg/IronClaude/issues/655): historical orchestrator umbrella referenced by PRs 682, 686 and 700. Its full present scope and state were not inspected, so UNVERIFIED beyond that documented relationship.

## Related PRs
Read live metadata/body and available comments for the issue's named PRs and subsequent disposition:
- [584](https://github.com/IronbellyOrg/IronClaude/pull/584), MERGED, `b6d038a30c15ebeab5797c7b039500ee5dc6bb63`: original approval core.
- [591](https://github.com/IronbellyOrg/IronClaude/pull/591), MERGED, `6af80d6c04f74d7c1db196f467e09c1d937d5503`: original coordinator handoff.
- [682](https://github.com/IronbellyOrg/IronClaude/pull/682), MERGED, `01e7a9e23519fd54bc438bb1a1a0e03dcdae5baf`: removed approval machinery, not the claim helper.
- [697](https://github.com/IronbellyOrg/IronClaude/pull/697), CLOSED without merge: proposed revert and clarification `fd23c01a9ca1f5aee44522f8107a07104f780c4f`; comments explicitly track remaining work in 699. Do not attribute that commit as a merged fix.
- [700](https://github.com/IronbellyOrg/IronClaude/pull/700), MERGED, `471f10511c8e2e8176c0e2088720ece03beca317`: restored approval flow and superseded 697.
- [701](https://github.com/IronbellyOrg/IronClaude/pull/701), MERGED, `0a46644576a31f0f62b9629b0f095b213027cdf6`: brought the contract clarification to master; body explicitly says it does not fix issues 698/699.
- [686](https://github.com/IronbellyOrg/IronClaude/pull/686), CLOSED without merge: related watcher rewrite and topology context; not a current fix for 699. Body/state were read; its full review discussion and downstream implementation are UNVERIFIED.

PR review-thread resolution state was not fetched through an API because the brief allows only issue/pr view and list. Historical reviewer comments are context, not substitutes for the current source and test definitions.
