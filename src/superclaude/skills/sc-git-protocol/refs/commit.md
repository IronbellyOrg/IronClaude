# Staging and committing with /sc:git

Loaded for `add` and `commit`, together with `safety.md`. The checks, the lists and the work-tree protection steps live in `safety.md` and are not repeated here. Every git call below is its own visible Bash call. Run the argv exactly as `vcs stage-plan` printed it, with `git` in front, and never edit it.

## Argv shapes

`stage-plan` returns each argv without the `git` program name. Prepend `git`. The temporary files live outside the work tree.

| Operation | Shape |
|---|---|
| `add <path>...` | `git --literal-pathspecs add --pathspec-from-file=<pathspec file> --pathspec-file-nul` |
| `commit <path>...` | `git --literal-pathspecs commit --only -F <message file> --pathspec-from-file=<pathspec file> --pathspec-file-nul` |
| `commit` with no path | `git commit -F <message file>` |
| staging `.dev/tasks` | `git add -- .dev/tasks` |

A commit with no path has no `--only` and no pathspec file, so that exactly the index the person staged is committed and no unstaged edit of a partly staged file is pulled in. No argv carries a token of the forbidden list in `safety.md`.

The pathspec file holds the paths of `pathspec_file.content`, each ended by a NUL. Write it to `pathspec_file.path` with a Bash call such as `printf '%s\0' '<path1>' '<path2>' > <pathspec_file.path>`, quoting every path literally, then check that `sha256sum` of the file equals `pathspec_file.sha256`. A different hash means the file is wrong: stop and make no git call. Print the complete path list before the call. The message file is `message_path`.

## add

1. Authorize, run `vcs preflight`, and apply the refusals of `safety.md`.
2. Run `vcs stage-plan --path <p>...`. Refuse what it refuses. List every path in `skipped` with its reason. When `status` is `nothing`, say so and stop; no git call runs.
3. Write the pathspec file, print the path list, and run the `add` shape with `GIT_TERMINAL_PROMPT=0`.
4. Read back with `git status --porcelain=v2 --ignore-submodules=none` and report which of the named paths are now staged. The report follows `SKILL.md`: argv as run, result, HEAD (unchanged), the index change, undo advice for the person: `git restore --staged -- <paths>`.

`add` stages the named paths and nothing else. It does not stage `.dev/tasks`, and it never stages a path the person did not name.

## commit

### Plan

1. Authorize, run `vcs preflight`, and apply the refusals of `safety.md`. Remember HEAD as the parent, and keep `git status --porcelain=v2 --ignore-submodules=none` as the "before" state of the report.
2. Run `vcs stage-plan --path <p>...` for a commit of paths, or `vcs stage-plan` with no `--path` for a commit of the index as staged. In both modes `commit_paths` is S, the commit set. For a commit with no path, S is frozen here: it is the index change set before any call, and nothing staged later widens it. When `status` is `nothing`, say so and stop.
3. Refuse `dev-copy-path` when the plan says so, or when `git diff --cached --name-only -z` lists a `.claude/` path that is not in `DEV_MIRROR_ALLOW`. Refuse the other path tokens of the plan as `safety.md` lists them. For a commit with no path, also refuse `legacy-run-folder` and `gitlink`: that commit takes the whole index, so a path the plan leaves out of S would still be committed. Name the path and say to unstage it with `git restore --staged -- <path>` or to name the paths to commit.
4. If S holds a file named `commits.md`, warn in the report: that file belongs to a `/sc:implement` run and may hold a commit boundary that is not settled; committing it by hand settles nothing. Name its path. Do not edit it and do not try to settle it here. The warning does not block the commit.

### Message

5. `--message "<text>"`: write the person's text unchanged to `message_path` with the Write tool.
6. `--smart-commit`: read the staged diff and draft a Conventional Commits message from it, then show the draft before the commit. For a commit with no path, read `git diff --cached`. For a commit of paths, nothing is staged yet, so read `git diff HEAD -- <paths>` (what `--only` will commit) and, for a named path git does not track yet, use its name and say it is new. Write the draft to `message_path`. The subject says what changed and why in at most 72 code points; the body is short and quotes no file contents.
7. Run `vcs check-message --file <message_path>`. On a refusal print the rule it names and stop with `message`. A `--message` text is never rewritten. A `--smart-commit` draft may be redrafted before any write.

### Stage

8. Commit of paths: write the pathspec file, print the path list, run the `add` shape, then run `git add -- .dev/tasks` when that folder exists. The order is fixed: the named paths and `.dev/tasks` are staged first, and then only the named paths are committed. The person's other staged changes stay staged, because `--only` leaves them out.
9. Commit with no path: nothing is staged before the commit.

### Protect, then write

10. Take the before snapshot and pin it, as steps 1 to 3 of "Protecting work outside the commit set" in `safety.md` say.
11. Run the commit shape with `GIT_TERMINAL_PROMPT=0` and the Bash timeout of 600000 ms. Note the exit status. Do not retry.

### Read back

12. Run `git rev-parse HEAD`. When it differs from the parent, run `git rev-list --parents -n 1 HEAD` (exactly one parent, and it is the remembered parent) and `git diff-tree --no-commit-id --name-only -r -z HEAD` (the changed paths).
13. Classify with the table in `safety.md`. The commit is `committed` when the exit status is 0, HEAD has the remembered parent as its only parent, and every changed path is in S. HEAD changed but a changed path is outside S: `hook-rewrite-committed`. Exit 0 with HEAD unchanged is not a success: report it as unexplained and stop.
14. Take the second snapshot and make the comparison of steps 5 to 7 of "Protecting work outside the commit set" in `safety.md`. A damage report or an unverified comparison stops the run even when the commit succeeded, and the pin is then kept.
15. Commit with no path: run `git add -- .dev/tasks` now, also after a refusal, so that package files are not left unstaged. It never widens the commit that was just made.

`vcs verify` is built for the boundaries of `/sc:implement`: it needs a boundary key and the `Implement-Boundary` trailer, which a `/sc:git` commit does not carry. For a `/sc:git` commit it answers `uncertain` with `trailer-missing`; do not read that as a failed commit, and take the class from steps 12 and 13.

## Report

Print the report of `SKILL.md` with these facts: the preconditions (preflight, plan, message check), each argv as run, the result (the new commit sha, or the class or token and the first 40 lines of git's output), HEAD before and after, whether the index and the work tree changed, the pin and whether it was deleted or kept, and any `skipped` path with its reason. After a commit print, as advice that is never run:

- `git reset --soft <parent>` keeps the changes staged; use it only for a commit that has not been pushed;
- `git revert <sha>` records a new commit that undoes it.

Printed advice authorizes nothing.

A refusal prints the rule that was broken and no command line, and says that HEAD, the index and the work tree did not change.
