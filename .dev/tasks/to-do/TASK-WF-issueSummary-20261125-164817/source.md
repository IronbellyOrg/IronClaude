# Summary: #842 [launch-level observation] OB-H3 full-submit test issue

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/842
- Type: feature
- Complexity: simple (rubric: `refs/claim.md`; one scratch-file area, up to 4 hours)
- Effort estimate: 1 hours
- spec-route: design — Simple scope with explicit acceptance criteria: one named file, exact one-line contents, a feature-branch commit and push, and one open PR that is never merged.

## What the issue asks for

Create only `.dev/ll-obs/C.txt` containing the single line `observation C`, commit it on a feature branch, push that branch, and open exactly one pull request against IronbellyOrg/IronClaude. This disposable change supports the OB-H3 FS observation; it is not a request to change enforcement code or open the ship gate. Never merge the pull request or push to the default branch, which is currently `integration`. The coordinator owns the surrounding observation and closes the PR without merging, then closes the issue as not planned; no implementation or publishing was performed by this accuracy-check worker.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `/home/coder/workspaces/worktrees/IronClaude/Coordinator/.dev/ll-obs/C.txt` | Requested scratch file; currently absent here and absent from the checked default-branch tree. Create the equivalent repo-relative path in the assigned implementation worktree, not in this review pass. |
| `/home/coder/workspaces/worktrees/IronClaude/obs-plan/.dev/launch-level-observations/plan.md` | Section 6.4 describes FS: one scratch-line change, feature-branch publication and an unmerged PR. Probe collection, disposable-base conflict setup and protected-push experiments belong to the surrounding coordinator-run observation; they do not expand the issue's one-file implementation scope. |
| `/home/coder/workspaces/worktrees/IronClaude/Coordinator/docs/designs/sc-issue-launch-level-hook.md` | Sections 4, 11 and 14 describe allowed FS actions, OB-H3 evidence and prerequisite gates. This pass confirms the references, not successful observations or permission to bypass the gates. |
| `/home/coder/workspaces/worktrees/IronClaude/Coordinator/src/superclaude/hooks/scripts/launch-level-guard.sh` | Existing FS policy allows commit, feature-branch push and PR submission while blocking merge and protected pushes. No code change is requested. |
| `/home/coder/.claude/skills/sc-issue-protocol/refs/claim.md` | Defines the claim's full-submit lifecycle, observation gates and the simple-effort rubric. |
| IronbellyOrg/IronClaude GitHub PR workflow | Exactly one PR, never merged. The implementation must follow the repository's required PR submission process; issue cleanup remains coordinator-owned. The scratch change is tiny; the 1-hour estimate includes publication and review handling, excludes the wider multi-level observation programme, and does not predict external review wait time. |

## Analysis

None: the accuracy check found the issue current, so no analysis ran. Codegraph and Auggie tools were unavailable; this minimal verification used Read, Glob, Grep and read-only Git/GitHub calls. No tests or live observation were run, and no launch-level gate was certified as passed.
