# Findings: issue 780, Orca registers this repository under the upstream project id

Checked 2026-11-24 against the live issue (open, label `bug`, no comments, created 2026-11-24T19:27:32Z) and this worktree (branch `ironbelly/Issuecleanup`, HEAD a7ae3dd30). Analyze report: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g7/780/analyze/analyze-report.md`.

## Verdict

**still-relevant.** The fault reproduces today, and the cause is not the one the issue suspects.

- Reproduced: `orca worktree current --json` in this worktree prints `"projectId": "github:superclaude-org/superclaude_framework"`. `git remote -v` shows only `origin` = `https://github.com/IronbellyOrg/IronClaude`.
- Real cause (observed): `orca repo list --json` gives the IronClaude repo record (id `de550e99-fa3c-42e2-abfe-1d092771c759`, path `/home/coder/workspaces/IronClaude`) a stored `"upstream": {"owner":"SuperClaude-Org","repo":"SuperClaude_Framework","host":"github.com"}`. `gh repo view IronbellyOrg/IronClaude --json isFork,parent` reports `isFork: true` with parent `SuperClaude-Org/SuperClaude_Framework`. The non-fork repos (Coder, PrivateRepoB, PrivateRepoC) have `"upstream": null`, and the fork IronOrca has upstream `stablyai/orca`. So Orca records the GitHub fork parent as `upstream`.
- Why that sets the id (Orca source, read live): in `/home/coder/workspaces/IronOrca/src/shared/project-host-setup-projection.ts`, `getProjectProviderIdentity` (lines 26-61) returns the stored `upstream` first when owner and repo are set; the `origin` remote is only the last fallback (`getGitRemoteProviderIdentity`, lines 63-72); the id is `github:<owner>/<repo>` (lines 123-125). UNVERIFIED: that the installed Orca 1.4.245-aidev02 matches this IronOrca checkout. UNVERIFIED: where Orca stamps `upstream` from the fork parent (not traced).
- The issue's suspect (`pyproject.toml:64-67`, `package.json:18`) does contain `SuperClaude-Org` URLs (confirmed; `package.json` also at lines 22, 25, 27), but nothing in the Orca code read feeds them into the id. Changing them will very likely not fix the id (not tested on a throwaway clone, UNVERIFIED).
- `CLAUDE.md:54` still records the wrong id and bans Orca link flags (confirmed). No fix PR exists: `gh pr list --search` found none about the Orca project id (hits 356, 584, 686 are unrelated).

## Complexity and size

Complexity medium, size M: the repair is outside this repository (Orca fork code or Orca's stored repo record, with no `orca repo` verb to change `upstream`), and the stamping path is not yet traced.

## Priority

P2: Orca links could resolve to the public upstream, but the CLAUDE.md ban on `--issue` and `--pr` (CLAUDE.md:54) is a working guard, and it blocks only the CLAUDE.md rewrite in issue 769 decision 5.

## Concrete next steps

1. Trace where IronOrca sets `repo.upstream` (the fork-parent lookup) and whether the installed Orca matches the checkout (answers both UNVERIFIED items).
2. Owner decides the route: (a) change Orca so `origin` wins, or a user override exists, for the project id (an issue and change in the IronOrca repo, not this one); (b) clear or override the stored `upstream` for this repo record if Orca allows it.
3. Do not edit `pyproject.toml` or `package.json` for this issue. Whether those URLs should change for other reasons (PyPI metadata) is a separate owner decision.
4. After the fix, run `orca worktree current --json` in any worktree: `projectId` must be `github:IronbellyOrg/IronClaude`. Then update the CLAUDE.md Orca paragraph (issue 769, decision 5); lift the link-flag ban only when the owner says so.
5. Update issue 780's "Fix approach" so the coordinator does not dispatch `/sc:implement` on package metadata (coordinator action, after the owner's go).

## Dependencies

- Needs: an owner decision on the route (step 2), and possibly a change in the IronOrca repo (no issue number known; UNVERIFIED whether one exists).
- Blocks: the CLAUDE.md Orca paragraph rewrite in #769 (decision 5, per the issue text; #769 is open, title "[FEATURE] Trim Startup token costs"), and any future use of Orca `--issue`/`--pr` link flags in this repo.

## Related issues

- #769 (open): decision 5 waits on this fault.
- No other issue found about the Orca project id (`gh issue list --search 'orca project id upstream'` returned only #780 and #769 as relevant).

## Related PRs

- None fixes this. #356 (merged, "refactor(worktrees): Orca default worktree paths, self-cleaning eval_runner, no upstream interaction") is background on the no-upstream rule only.
