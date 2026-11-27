# Local branches with /sc:git

Loaded for `branch create <name>`, `branch switch <name>` and `branch cleanup`. `create` and `switch` are writes and load `safety.md` with this ref; `cleanup` is a read that only prints a route, loads only this ref and runs nothing. Every git call below is its own visible Bash call, run with `GIT_TERMINAL_PROMPT=0` as `safety.md` says. This command never deletes a branch, local or remote, and never uses `--force`, `-f` or `--discard-changes`.

## create and switch: shared checks

1. **Authorize.** The person's current message starts with `/sc:git branch`, as `SKILL.md` says. The line authorizes only the one branch name it carries.
2. **Preflight.** Run `vcs preflight` and refuse `operation-in-progress`, `index-locked` and `git-too-old` as `safety.md` defines them. Branch operations are working-tree writes, not local-history writes, so being on a protected branch or on a detached HEAD does not refuse them: moving away from either is a normal reason to run them. The protected-name rule below applies to the target name, not to where you stand. Print `notice` when it is set.
3. **Name.** The name must pass `git check-ref-format --branch '<name>'` (exit 0) and may use only letters, digits, `.`, `_`, `-` and `/`. Anything else is refused in words and no command line is printed; a name outside that set cannot be passed safely on a command line. Always quote the name in single quotes in the call.

No snapshot pin is taken: `create` leaves the work tree as it is, and `switch` only runs on a clean tree.

## create

1. Refuse `protected-branch` when the name equals a name in `PROTECTED_BRANCHES` (the list in `safety.md`), or the default branch that `git symbolic-ref --short refs/remotes/origin/HEAD` names once its leading `origin/` is removed. When that ref is not set, the fixed names still apply.
2. Refuse in words, "the branch name already exists", when `git show-ref --verify --quiet 'refs/heads/<name>'` exits 0. The existing branch is not touched.
3. Run `git switch -c '<name>'`. The new branch starts at the current HEAD; say which sha that is.
4. Read back with `git branch --show-current` (it must print the name) and `git rev-parse HEAD` (it must equal the sha before the call).
5. Report as `SKILL.md` says: the checks, the argv as run, the result, HEAD before and after (the same sha), the index and work tree unchanged. Undo advice, printed and never run: `git switch '<previous branch>'` returns to where you were; the new branch stays.

## switch

1. Run `git status --porcelain=v2 --ignore-submodules=none`. When it prints anything, refuse in words, "the work tree is not clean", with at most 20 entries, the total and a truncation note, and print no command line. This count includes untracked files and changed submodules. Advice: make the tree clean first, for example by committing; this command does not set changes aside, discard them or force a switch.
2. Run `git switch '<name>'`. Add no other flag. When no local branch has that name, git may create one from a single matching remote-tracking branch; that is git's own behavior, it fetches nothing, and its output says so.
3. When git refuses because the branch is checked out in another worktree, or for any other reason, show git's message as it is (first 40 lines). Do not look for another way, and do not retry.
4. Read back with `git branch --show-current` (it must print the name) and `git status --porcelain=v2 --ignore-submodules=none` (it must still be empty).
5. When `submodule_recurse` from the preflight is true, say so in the report: git then also moved the submodule work trees. Otherwise a changed submodule pointer leaves the submodule work trees where they were, and the `submodule status` operation shows the difference.
6. Report as `SKILL.md` says. Undo advice, printed and never run: `git switch -` returns to the previous branch.

## cleanup

`branch cleanup` is read-only routing. It changes nothing and runs no `/sc:worktrees` verb. The cleanup of finished worktrees and their local branches already exists in `/sc:worktrees` (the script `scripts/worktree_cleanup.py`), which keeps its own eight removal rules and its `--apply` switch. This command reuses it and does not repeat or replace it.

1. Find the top of the checkout with `git rev-parse --show-toplevel`, then look for `scripts/worktree_cleanup.py` under it.
2. When the file is absent, print this notice and stop: `/sc:worktrees` runs only inside an IronClaude checkout that has `scripts/worktree_cleanup.py`.
3. Otherwise print this route and stop. The person chooses and types the line; this command types none of them, and never adds `--apply`:

| Line | What it does |
|---|---|
| `/sc:worktrees list` | read-only: one row per worktree with the reason it is kept or removable |
| `/sc:worktrees archive <worktree>` | writes the finished worktree's `.dev` files to the evidence repository, even without `--apply`; removes nothing, so it is not an inspection |
| `/sc:worktrees retire <worktree> --apply` | removes one worktree whose work is safe, and only with `--apply` |
| `/sc:worktrees prune --apply` | the same decision for every worktree, and only with `--apply` |

Without `--apply`, `retire` and `prune` are dry runs.

Local branches that have no worktree are not cleaned by any command. That gap is recorded as accepted residual scope; it is revisited only if the owner names it. Nothing here deletes a remote branch.
