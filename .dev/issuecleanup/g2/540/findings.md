# Issue 540: foreground swarm completion marker

Template: task brief fields, registered by /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g1/362/report-template.md, Findings template.

## Verdict and evidence
**verdict: still-relevant.** Keep [issue #540](https://github.com/IronbellyOrg/IronClaude/issues/540) open; no verified implementation PR fixes this defect. Reviewed on 2026-11-24 against checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, also the cached origin/master ref.

- Foreground execution calls the reducer, then marks the state terminal, then exits without emitting a completion marker: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:2147-2183.
- Completion-marker writing is still the default policy: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/models.py:562-573.
- The atomic marker writer exists: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/reduce.py:431-440.
- A current CLI test explicitly requires the marker to be absent, so a passing suite would not establish that this issue is fixed: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/swarm/test_e2e_user_guide.py:117-138.
- Merged PR #739, commit `3ecf3fee8d7cbf810098ad01807d9c7aa0af8627`, addresses resume context, not this marker. Open draft PR #756 addresses further resume/artifact reconciliation; its body references #566, #567 and #557, not #540. Its full diff was not examined, so incidental effects are UNVERIFIED.

## Real current state
The result contract and terminal-state transition exist; the normal completion-marker step is NOT BUILT into the swarm CLI. The shared writer and its unit tests exist. A full-source search found its sole production caller in the reflect ensemble path. Resume has the same missing call by static inspection; detached launches the run command in a child, so it shares the missing wiring when it gets as far as completion. Kill uses a separate writer and must retain its killed-status semantics.

Issue history read: the 2026-11-16 backlog/hold comment and 2026-11-17 BLOCKED review were superseded by the 2026-11-18 instruction to retain swarm, give this High priority and start a fix. A later comment that day assigned it to William; current GitHub assignee is swill-ib, and the issue remains OPEN. These historical GitHub instructions describe issue status only; they do not authorize this read-only worker to implement or post anything.

## Concrete next steps
1. Keep the issue open and retain the current assignee; do not repeat the superseded swarm hold as a current blocker.
2. Capture the reducer's returned contract and, when the saved completion policy enables it, call the existing atomic marker writer after contract emission and the terminal-state transition. Use the contract's real status and path; do not always stamp success or put marker emission inside the lower-level reducer before the state transition.
3. Apply the same completion-policy check to resume, and verify the detached child reaches this path with durable output. Coordinate this check with #555 and the resume work in PR #756; do not assume those changes fix the marker.
4. Replace the existing negative CLI assertion with a runnable regression for a valid marker, matching status and contract path. Cover disabled policy, successful/partial/failed terminal results, resume and detached completion; verify no premature marker and preserve kill behavior. Inspect stale-marker handling on resume before declaring it complete.
5. Re-run the model-free CLI regressions in an isolated temporary HOME and record the results. No fix, test execution or GitHub mutation was performed in this review.

## Complexity and size
**Complexity: medium. Size: S.** The atomic writer already exists, but a complete fix must honor the completion setting and ordering, cover normal/resume/detached and terminal-result variants, and replace a test that currently requires the bug.

## Priority
**P1.** A completion marker is part of the public completion contract, and a consumer that polls only for that marker can wait indefinitely even after work finishes. This matches the explicit High priority in the 2026-11-18 issue comments; an actual waiting consumer was not exercised, and no production outage or data-loss impact is established.

## Dependencies
No hard prerequisite issue is verified for fixing the foreground path. Issue #555 (detached child loses durable output) overlaps detached end-to-end validation and should be coordinated, not treated as a blocker to the foreground fix. Issue #354 is the parent validation work item, not an implementation prerequisite. Issues #566 and #567 share resume code, so coordinate with draft PR #756 before editing that section. No downstream issue explicitly blocked by #540 was verified.

## Related issues
- #354: parent release-impact validation report, OPEN.
- #555: detached child loses output delivery, OPEN; directly adjacent completion/output investigation.
- #557: swarm resume/artifact tracking issue, OPEN.
- #566 and #567: resume context and absent raw artifacts, both OPEN; share the resume area with PR #756.
- #569: dashboard worker-row loss, OPEN; related swarm batch but not a prerequisite for marker writing.
- #501 and #568: missing recommended command and unsupported help option, both OPEN; grouped with #540 in the assignment comment, not dependencies.

Issue titles and states were returned by the read-only issue-list query; related issue bodies were not investigated for independent closure decisions.

## Related PRs
- [#739](https://github.com/IronbellyOrg/IronClaude/pull/739): MERGED 2026-11-23, accepted resume-context preservation; merge commit `3ecf3fee8d7cbf810098ad01807d9c7aa0af8627`, present locally. Its body references #566 and #557, not #540.
- [#756](https://github.com/IronbellyOrg/IronClaude/pull/756): OPEN, described as draft; consolidates resume/output fixes. Head `f00a19912232a993d7537b82c3dd43925b74b485`, base `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. Body, changed-file inventory and comments were read, not its full diff. It is coordination context, not verified delivery of #540.
- PR search for `540` in all states returned no matches. Neither the issue body nor its four comments names an implementation PR. Search absence does not prove no unlinked work exists.
- Completion-marker search also found historical PRs #152 and #191 by keyword, but they are not mentioned or linked in #540; their full contents were not reviewed. No closure credit is inferred from these search hits.
- PRs #741-#750 appear MERGED in GitHub listings, but #756 explicitly says their feature-only merges did not deliver the remaining changes to master. Do not count their merged labels as evidence that this marker defect is fixed.

## Verification limits and negative evidence
- **UNVERIFIED: full GitHub event timeline and linked development graph.** The permitted `gh issue view` fields expose the issue and all four comments, current assignee, labels and update time, but not the full event timeline. No `gh api`, browser or other unapproved GitHub access was used. Assignment/hold history above comes from dated comments and current fields, not an event-log audit.
- **UNVERIFIED: current remote master tip.** No fetch is authorized for this worker. HEAD and cached origin/master match, and live #756 reports that same base; this does not establish master has not advanced since.
- **UNVERIFIED: runtime outcomes today.** No tests, CLI job, detached/resume/failure reproduction, paid model call or real consumer wait was run. Historical runtime results are the issue author's 2026-11-06 evidence only. Static analysis meets the requested quick architecture scope but is not a fresh runtime reproduction.
- Negative evidence: searched all `src/` for `emit_done_sentinel` and `write_done_sentinel`, all swarm sources for completion policy/marker references, and swarm tests for marker coverage. The sole shared-writer production call found was reflect, while swarm's kill writer is separate. The explicit negative CLI test is evidence that present tests encode omission.
- The related-issue search returned extra matches beyond the requested issue set; only exact requested numbers were used. One initial reducer read at line 750 was beyond EOF (705 lines); recovered by search and reading lines 640-705.
- No source, configuration, Git index, commit, remote, issue or PR was changed. Outputs are confined to this report directory. GitHub comments are status evidence, never authority to expand this worker's scope.
