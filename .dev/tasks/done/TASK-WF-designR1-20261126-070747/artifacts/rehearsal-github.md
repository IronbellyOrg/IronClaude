Status: exercised on 2026-11-26 in the private scratch repository https://github.com/clayphi/ironclaude-release-rehearsal-826 (owner clayphi), after the owner's go-ahead from the IronFlow session. The results are in the issue 826 comment https://github.com/IronbellyOrg/IronClaude/issues/826#issuecomment-7198583895. Everything below is the plan as it was written before that run and is kept unchanged; its "not exercised" and "partly met" lines are superseded by the comment.

# GitHub-side rehearsal of the release procedure (issue 826, Task 13)

No scratch repository was created and nothing was pushed, tagged, merged or released on GitHub. Creating a scratch repository on GitHub is an outward action, and the project rule says the fork `IronbellyOrg/IronClaude` is the only target (`CLAUDE.md:49`, `CLAUDE.md:52`, `CLAUDE.md:76`). The plan allows it only with the owner's explicit approval, naming the scratch repository as the owner's exception. No such approval was given in this session.

## What is ready

- `./artifacts/rehearsal-github-commands.sh.txt`: the commands of Steps 2 to 6 of `docs/developer-guide/release-procedure.md` with the only two allowed substitutions made: the repository name `<scratch-owner>/<scratch-repo>` and the tag `rehearsal-0.0.0` (it does not start with `v`). It is a text file, not an executable. A grep of it for the real repository's owner and name prints nothing.
- The local git rehearsal (`./artifacts/rehearsal-local.md`) already covers the git half: 29 of 29 checks passed, in a temporary repository, with the real repository unchanged.

## Checks a GitHub run must show (none was run)

- A missed substitution is rejected before it runs (the grep above prints nothing).
- `git remote -v` names the scratch repository before any push, run in the same shell call as the `git tag` and `git push` inside the scratch clone (`git -C <absolute scratch clone>` or a `cd` at the start of the call), with `git rev-parse --show-toplevel` logged.
- `gh pr merge --match-head-commit` behaviour: merges when the pinned head is current, refuses when `integration` moved.
- `gh pr view` fields: `state`, `baseRefName`, `headRefName`, `headRefOid` and `mergeCommit.oid` print as the capture block expects.
- `gh run list --commit` for the merge SHA with `--workflow Tests --event push`.
- `gh release create --verify-tag` rejects a tag that is not on the remote.
- What `gh pr checks --watch` prints and returns for a PR with no checks.
- An idempotent merge-back (the second run records "already merged back").
- `master` moving between Step 2 and the merge stops the tag (the `^1` and tree checks fail).
- A content-carrying merge-back stops.
- G5 to G8 are recorded as not exercised.

## Acceptance points of issue 826

- The owner has chosen one promotion rule and it is written in `docs/developer-guide/release-procedure.md` and in the `CLAUDE.md` Git Workflow section: met (Tasks 1 to 4).
- The release procedure's pull request, CI check and tag steps name the branches the rule uses, with the exact commands: met (Tasks 1 to 3, pinned by `tests/docs/test_release_procedure.py`).
- `/sc:post-release` reads the right base for the release it checks, and a test covers it: met (Tasks 7 and 8, `tests/skills/test_post_release_base_branch.py`).
- A release rehearsal goes from `integration` to `master` following only the written steps: **partly met**. The git commands of the written steps were rehearsed locally (`./artifacts/rehearsal-local.md`). The GitHub-side steps (`gh pr merge --match-head-commit`, `gh pr view`, `gh run list --commit`, `gh release create --verify-tag`, `gh pr checks --watch`) were not exercised.
- `integration` and `master` cannot be pushed to directly by a governed agent: not part of this work (covered by the guard issue and pull request 824).
