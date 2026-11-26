# Findings: issue 826 (release path from integration to master)

Checked 2026-11-25 against the worktree (branch ironbelly/Issuecleanup, HEAD a7ae3dd30) and the local remote refs origin/integration (4e35750e7, the PR 824 merge) and origin/master (f2894fc44). No fetch was run, so those refs are as of the last fetch (UNVERIFIED that they are current).

## Verdict

**still-relevant** (open, not started, and unblocked: the owner picked the rule on 2026-11-25).

Evidence:
- Issue 826 is OPEN, label `enhancement`, no linked closing PR, no blockers, no sub-issues. Its one comment (2026-11-25T00:53:59Z, ironbelly) records the owner decision: a release PR from `integration` to `master`, opened by a person, merged as a merge commit, tagged on that merge commit. Options 2 and 3 dropped. Step 1 done; steps 2 to 5 can start.
- `docs/developer-guide/release-procedure.md` still assumes master, identically on origin/integration: line 59 `gh pr create ... --base master`; line 71 (G2) `gh run list ... --branch master`; line 88 "never a later `master` commit"; line 22 "Every merge to `master`"; line 3 mentions master and integration CI triggers.
- PR 824 (MERGED 2026-11-24T23:25:39Z, base integration) fixed other base-branch references but not this document or the post-release protocol.
- `src/superclaude/skills/sc-post-release-protocol/SKILL.md:91` checks `git merge-base --is-ancestor <tag> <default-branch>` with the default branch auto-detected. The default is now `integration`. With the chosen rule the tag sits on a merge commit on `master`, which is not an ancestor of `integration` until master is merged back (no post-tag merge-back is recorded: PR 639 merged master into integration before release PR 640 to resolve a conflict, and PR 663 was closed unmerged; 6.1.0 was a squash into master, unlike the merge-commit rule now chosen). So the check can raise a false release-integrity finding. This is a gap the issue does not name. (Reasoned from git semantics and the PR history, not run.)
- `src/superclaude/commands/post-release.md` has no master or base-branch text (grep found none).
- No test covers post-release base-branch logic. The only post-release mentions in tests are `tests/skills/test_worker_contract.py:2371-2384` and a name in `tests/core/test_how_we_work_routing_table.py:86`.
- `CLAUDE.md` on origin/integration already says `master` (production) <- `integration` (testing) at line 290 and "Merge to `integration` -> validate -> merge to `master`" at line 297, but gives no release-PR commands.
- `src/superclaude/commands/impact.md:23` and `src/superclaude/commands/auggie-review.md:37,113` still use `origin/master` in examples.
- Not verified: that a rehearsal works (none done); whether the branch-protection issues will block the release merge.

## Complexity and size

Complexity medium; size M. Docs rewrite plus one protocol change plus a new test plus a rehearsal release; the tag-ancestry problem needs a design decision.

## Priority

P2. Releases still work by hand and the owner is the only releaser, but the written procedure now points at the wrong branch for the next release; nothing else is blocked on it.

## Concrete next steps

1. (Done) Owner chose the rule; recorded in the issue comment.
2. Rewrite `docs/developer-guide/release-procedure.md`: line 59 `--base master --head integration`; line 71 G2 CI check on the release PR's merge SHA on `master`; line 88 tag rule; lines 3 and 22 wording; add the exact commands. Decide and write whether master is merged back into `integration` after the tag (needed for the ancestry check below).
3. Change `src/superclaude/skills/sc-post-release-protocol/SKILL.md:91` so the ancestry check uses `master` (or the release PR base) rather than the auto-detected default branch; add a test that pins the base it checks (a new file under `tests/skills/`).
4. Update `CLAUDE.md` Git Workflow (lines 290 to 297 area) with the release-PR rule, and the `origin/master` examples in `impact.md` and `auggie-review.md` only if their meaning of "diff against base" should now be integration (they are feature-branch diffs, so likely `origin/integration`). Run `make sync-dev`, `make verify-sync`, `make lint`, `uv run pytest`.
5. Rehearse a release on a scratch fork or throwaway tag using only the written steps; attach the result to the issue.
6. Ship through `/sc:pr-submit --monitor 3` with base `integration`.

## Dependencies

Needs: none open (owner decision is made). Soft: #702 and #723 (branch protection) could affect how the release merge is done but are out of scope. Blocks: no issue found.

## Related issues

#702 (protect the default branch, OPEN), #723 (protect master and integration with GitHub rules, OPEN, parked), #571 (Release 6.0.0 plan, UNVERIFIED state), #769 follow-up 1 (where this came up, UNVERIFIED).

## Related PRs

#824 (MERGED, integration as base everywhere); #658 (merged, release 6.1.0 into master); #640 (merged, release 6.0.0 into master); #639 (merged, master into integration to resolve a conflict before release PR 640); #663 (closed unmerged, merge master 6.1.0 squash into integration); #634 (merged, 6.0.0 version bump into integration).
