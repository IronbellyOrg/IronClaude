# Status and branch list with /sc:git

Loaded for `status` (also a bare `/sc:git`) and `branch list`. Both are reads: any `/sc:git` line runs them, `safety.md` is not loaded, and nothing below writes a ref, the index, a file or a config value. Every git call is its own visible Bash call. Print only the report asked for.

## status

1. Run `vcs preflight`. For a read, its refusal is not a stop: print the facts as facts. Show the branch (or "detached HEAD"), whether it counts as protected and why (`protected.reason`), a merge, rebase, cherry-pick, revert or bisect in progress (`operation_in_progress`), an `index.lock` file (`index_lock`), the git version, and `submodule_recurse` and `push_recurse_submodules` when they are set. When `notice` is not null, print it as it is.
2. Run `git status --porcelain=v2 -b --ignore-submodules=none`. The `--ignore-submodules=none` makes a changed or dirty submodule show up in the list, which the default hides.
3. Run `vcs submodules`. Skip it, and say "no submodules", when `rows` is empty.
4. Print the report in this order:
   - **Branch.** The branch name, the short HEAD sha, and the upstream with its ahead and behind counts exactly as the `# branch.upstream` and `# branch.ab` lines give them. When there is an upstream line but no `# branch.ab` line, say that git gave no counts and give no reason of your own.
   - **Changes.** One count and one list for each group: staged, unstaged, untracked and unmerged (the `u` lines). Staged and unstaged come from the two status letters of each `1` and `2` line. List at most 20 paths per group, with the total and a note when the list was cut. This is a display limit only. Never print file contents.
   - **Submodules.** One line per row of `vcs submodules`: `path`, `state`, and the short `head`. Add the `warnings` text as it is. A row whose `state` is `None` or that carries a `reason` is shown with that reason, never as clean.
5. Add next-step advice from the list below. Advice is printed, never run, and authorizes nothing.

### Next-step advice

Choose only what the facts support, at most three lines:

| Fact | Advice |
|---|---|
| staged paths exist | the `commit` operation of this command commits them |
| unstaged or untracked paths exist | the `add` operation with the named paths stages them |
| detached HEAD, or a protected branch with changes | the `branch create <name>` operation starts a local branch from here |
| unmerged paths | resolve them by hand; this command does not resolve conflicts |
| `operation_in_progress` | finish or abort it with git yourself; this command writes nothing while it runs |
| `index_lock` | another git process may be running; check before anything else, and never remove the lock file |
| a submodule `state` other than `in-sync` | the `submodule status` operation explains each state |

Advice never names publishing a branch, joining branches or opening a pull request. Ahead and behind counts are shown and no advice follows from them. When the tree is clean and nothing is in progress, say "nothing to do".

## branch list

1. Run `vcs preflight` for the current branch and its notice, as for `status`.
2. Run `git for-each-ref --sort=refname --format='%(HEAD)%09%(refname:short)%09%(upstream:short)%09%(upstream:track)%09%(worktreepath)' refs/heads`. Local branches only; a remote branch is never listed.
3. Print one table row per branch: a `*` for the current one, the name, the upstream, the track text and the work-tree path. Show the cells exactly as git prints them. A branch checked out in another worktree shows its path; say nothing more about it. List at most 200 rows, with the total and a note when cut.
4. After the table, add this note once when any row shows `[gone]`: `[gone]` says the upstream branch is no longer on the remote as of the last fetch. It is not proof that the work was merged. Do not suggest that such a branch is safe to remove.
5. End with one line: to remove finished worktrees and their local branches, the `branch cleanup` operation prints the route.

The report follows the read rule of `SKILL.md`: the table asked for and nothing else.
