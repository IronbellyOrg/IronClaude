model: top rung (tier unknown) family: claude rung: top  family-fallback: no verified spawn path for a GPT T1 model  entry: escalation 1, adviser B
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T2.AC1 | Met (review-2.md:3). `main` takes an injected runner (attempt-2.diff:522-534). Top-level help names `--apply` and `--out` only in the epilog (attempt-2.diff:486). | Keep this. Also add both flags to the top-level parser, with `default=argparse.SUPPRESS` on the per-verb copies, so `--help` shows them as real options. |
| T2.AC2 | Missed. Push used a fixed deny set of whole tokens (attempt-2.diff:296-308, review-2.md:7), so `-df` and `--dele` got through. Attempt 1 missed orca `-f` the same way (review-1.md:7). The same weakness is in orca rm (attempt-2.diff:360) and branch `--list` returning early (attempt-2.diff:272). | Match every write verb against one complete argument shape and refuse everything else. Give each read verb its own list of allowed options. Do not use deny lists. |
| T2.AC3 | Met (review-2.md:5, attempt-2.diff:872-882). | Keep the scan. Also keep `subprocess` called only inside `_execute`. |
| T2.AC4 | Met (review-2.md:6), but the block is a short credit line, not the license notice (attempt-2.diff:8-12). | Use the standard Apache-2.0 header: copyright line, "Licensed under...", license URL, the "AS IS" clause, the source URL, then "Changed by IronClaude, see scripts/worktree_cleanup_PROVENANCE.md". Put it in the first 20 lines and test those lines. |

differs-by: every command is accepted only if it matches a complete argument shape, with no deny lists anywhere, which makes bundled short options and shortened long options impossible to pass.

Steps:
1. Rewrite `Runner.check_allowed` as exact shapes:
   - push: `push origin <branch>` or `push --porcelain origin <branch>`. The remote is literally `origin`, the folder is the evidence clone, and the branch matches `^[A-Za-z0-9_][A-Za-z0-9._/-]*$` with no `..`, `:`, `+` or `*`.
   - `branch -d <name>` exactly, plus `branch --show-current` and `branch --list <name>`.
   - `worktree remove <path>` and `worktree list --porcelain`, where the path does not start with `-`.
   - Orca: `worktree rm --worktree <sel>` exactly, and `terminal close --worktree <sel> --all` exactly, only when that selector is authorized.
   - Keep the xargs clean shape as it was.
   - git `-c` allowed only for the credential helper, and only before clone, fetch or push.
2. Find the landed-check script by comparing its real path with the three lookup paths recorded by Task 1, not by a path suffix (attempt-2.diff:185-188).
3. Read verbs:
   - Keep only status, rev-parse, log, ls-files, merge-base, remote get-url and config --get. Drop diff, show, cat-file and the other unused ones (attempt-2.diff:197-210); later tasks add what they need.
   - Each verb gets a list of exact allowed options. Any other dash token is refused, which covers `--output`, its shortened forms, `-o`, `--ext-diff`, `--textconv` and `--exec`.
   - A plain argument may not start with `-`.
   - Run read verbs with `GIT_OPTIONAL_LOCKS=0`, and remove `GIT_EXTERNAL_DIFF` from their environment.
4. Credential:
   - Pass `GH_TOKEN` and `GITHUB_TOKEN` only to gh, to the landed check (it runs gh, as the reviewer accepted) and to `git push`. The F2.2 fix asks for exactly this (review-2.md:8).
   - `git clone` and `git fetch` run without them, using `-c credential.helper=!gh auth git-credential`. They then rely on the person's existing gh login, which the script never reads itself.
   - If they fail, that is a failed save: keep the worktree. This is the item 5 fallback of plan line 35.
   - Put the env variable name, never its value, in the module docstring. Tell the parent that a plan amendment is needed if the switched-off automation must fetch with `GH_TOKEN` only.
   - Drop `gh repo clone` (attempt-2.diff:337-344); the plan does not list it.
5. Tests in `tests/worktree_cleanup/test_runner.py`:
   - Add refused cases with the never-run guard: push `-df`, `-fd`, `--dele`, `--del`, `--forc`, `--force-if-includes`, `--mirror`, `origin +main`, `origin main:main`, `origin :x`, `upstream main`; branch `-df`, `-d -f`, `--del`, `--list -D x`; worktree remove `--forc`; orca rm `--forc`, `-fy`, `--force=true`; `git diff --output=x`; `git log --outp=x`; `git reset`.
   - Fix the token tests so clone and fetch get no token (attempt-2.diff:949-950).
6. Run `uv run pytest tests/worktree_cleanup -q` and `ruff check`, then grep the new files for em and en dashes.

Files:
- /home/coder/workspaces/worktrees/IronClaude/issue-687/.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/TASK-WF-specWorktreeClea-20261120-173546.md
- /home/coder/workspaces/worktrees/IronClaude/issue-687/.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/retries/T2/review-2.md
- /home/coder/workspaces/worktrees/IronClaude/issue-687/.dev/tasks/to-do/TASK-WF-specWorktreeClea-20261120-173546/artifacts/retries/T2/attempt-2.diff
