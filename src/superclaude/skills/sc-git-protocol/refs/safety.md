# Safety rules for /sc:git writes

Load this ref, with the operation's group ref, for every write (`add`, `commit`, `branch create`, `branch switch`, `submodule update`, `submodule commit-pointer`). A read never loads it. The lists below are copied from `scripts/vcs_rules.py`, which is the single source. When one changes, the constant and this text change together; a test fails if only one does.

## The lists

- `PROTECTED_BRANCHES`: `master`, `main`, `integration`
- `FORBIDDEN_FLAGS`: `--no-verify`, `-n`, `--amend`, `--force`, `-f`, `-D`, `--delete`, `-A`, `--all`, `.`, `-a`, `--allow-empty`, `--no-edit`, `--remote`, `--recurse-submodules=on-demand`, `--discard-changes`
- `DEV_MIRROR_ALLOW`: `settings.json`
- `MIN_GIT`: `2.25`

How they apply:

- **Protected branches.** The preflight adds the target of `refs/remotes/origin/HEAD` when it resolves, and any further name the repository's own instructions call protected (the report names that source). A resolved default only adds a name and never removes a fixed one. Inside a submodule the default is read from the submodule's own refs.
- **Forbidden flags.** No command this skill plans or runs carries one of these tokens, and a person's line that carries one is stopped by the command file. `-n` is the commit short option for no-verify, and `.` is a pathspec. The one place `-A` appears is the private-index snapshot below, which never touches the person's index.
- **Project agent-host folder.** Only the files named in `DEV_MIRROR_ALLOW` may be staged under `.claude/`.
- **Git version.** `MIN_GIT` is the higher of 2.23 (the switch verb) and the version that supports `--pathspec-from-file` for add and commit. 2.25 is UNVERIFIED: no test of the installed git has turned it into a stated fact. Below the floor, refuse `git-too-old`.

## Never prompt and never wait

Every write runs with `GIT_TERMINAL_PROMPT=0` set on that Bash call, and the commit call uses the Bash timeout of 600000 ms. Hooks and signing are never disabled to meet it. When git or the host would ask for a signing credential or for authentication, stop and report it. Never wait for an answer and never retry. That variable does not cover a signing prompt from a key agent, so a call that reaches the timeout, or ends with an exit status above 128, follows the interruption rule below.

## Preflight refusals

Run `vcs preflight` before any write. A refusal prints the token, no command line, and says that HEAD, the index and the work tree did not change.

| Token | Raised when |
|---|---|
| `detached-head` | HEAD is not on a branch. Inside a submodule's work tree the same refusal applies to the repository that receives the commit. Only `submodule commit-pointer` reads the submodule's own detached HEAD, under the rules of `submodule.md`. |
| `protected-branch` | the current branch is in `PROTECTED_BRANCHES` (with the run-time additions above). For `branch create`, a protected or existing name is refused too. |
| `operation-in-progress` | a merge, rebase, cherry-pick, revert or bisect is under way |
| `index-locked` | an `index.lock` file exists. Never remove it, and never assume it is stale. |
| `git-too-old` | the installed git is below `MIN_GIT` |

When `default_branch_known` is false, print this notice and go on, with no network lookup and no block:

`default branch unknown: refs/remotes/origin/HEAD is not set; protected names: master, main, integration`

and the local fix `git remote set-head origin <branch>`, as advice the person may run.

## Path rules

These apply to `add <path>...` and `commit <path>...`. `vcs stage-plan` applies them and lists what it dropped in `skipped`.

- **Literal paths only.** `.`, a glob and a directory are never expanded. A path that names a directory is refused `directory-entry`.
- **Agent-host copies.** A `.claude/` path other than those in `DEV_MIRROR_ALLOW` is refused `dev-copy-path`, also when git already tracks it. The refusal names the file and stops, and suggests no staging command. Tracking a file is not authority to stage it.
- **Submodules.** A path equal to or under a submodule's recorded commit (mode 160000, in HEAD or the index) is refused `gitlink`, with a pointer to `/sc:git submodule commit-pointer`.
- **Outside the repository.** An absolute path, a `..` traversal, and a path that resolves through a symlink to a place outside the repository are refused `outside-repo`.
- **Names a record cannot carry.** A path with a comma, a newline or a control character is refused `path-unrepresentable`.
- **Quietly skipped, listed with the reason.** A gitignored path, a path under `.dev/implement/`, and a path missing from the work tree, the index and HEAD. A path missing from the work tree but still in the index or HEAD is a deletion and is staged.
- **Transport.** Paths pass through a NUL-delimited temporary file outside the work tree, never on the command line. Print the complete path list before the call. The host guard still sees the call as a commit, and a host denial is final: report `blocked-by-host` and never look for another way.

## Message format

`vcs check-message --file <message_path>` checks the text, without `--implement`. It refuses with the rule it broke (`header_len` and `rule` in its JSON), and a refusal is the `message` token.

- The first line is `<type>[(<scope>)][!]: <summary>`, at most 72 Unicode code points of the decoded header, counted without normalization. When drafting, cut at the last space at or before code point 72.
- `<type>` is one of `feat`, `fix`, `refactor`, `docs`, `test`, `build`, `ci`, `chore`, `perf` or `style`.
- The second line is blank.
- Trailers that the session's own standing instructions require come last. The helper adds none.

The message goes to a temporary file outside the work tree and is passed with `-F`, never inline.

## Hook outcomes

A commit runs the repository's hooks as they are. Classify the outcome from the exit status and the read-back of the commit step in `commit.md`:

| Class | Meaning for `/sc:git` |
|---|---|
| `blocked-by-host` | a host hook refused the Bash call before git ran; HEAD and the index are unchanged |
| `hook-failed` | exit 1, HEAD unchanged, the commit set unchanged. Also a file over the size limit, which the report names. |
| `hook-rewrite` | exit 1, HEAD unchanged, and a hook changed paths inside the commit set |
| `hook-rewrite-committed` | HEAD moved, but the commit changed paths other than the commit set |
| `commit-error` | exit 128 |
| `hook-rewrite-evidence`, `hook-rewrite-pinned` | `/sc:implement` boundaries only; a `/sc:git` commit has no package evidence and no plan pin |

Exit statuses above 128 and a timeout are not classified: stop with the interruption rule below.

Every non-success class stops the run. Print the report with the first 40 lines of git's output and no more, plus the exit status and the class. For `hook-rewrite` and `hook-rewrite-committed` pin the rewritten tree (the second snapshot below) as `refs/superclaude/git/rewritten/<timestamp>` and print `git diff --stat` of it against the before snapshot. Never retry in the same run. Never use `--no-verify`, `-n`, `SKIP=`, `commit-tree` or `--amend`, and never edit a hook or `core.hooksPath`. A later attempt needs a new typed line from the person.

## Protecting work outside the commit set

Under `--only`, every change outside the commit set S counts as unstaged, and a hook framework that stashes unstaged changes can lose them if it is killed. Edits to a file marked assume-unchanged can be overwritten even without a kill. S is the named paths, or, for a commit with no path, the index change set frozen before the call. Staging `.dev/tasks` never widens S. Two proofs stay separate: the commit's content (checked by `commit.md`) and a snapshot of the work tree (here). One never stands in for the other. The steps also apply to `submodule commit-pointer`.

1. **Lossless first.** When `vcs preflight` reports `snapshot_lossless` false (a content filter or `core.autocrlf=true`), refuse `snapshot-unsupported` before the commit.
2. **Capture before the commit**, after the add calls and immediately before the commit call, with the Q0 private-index method. It starts from HEAD and never copies the person's index:
   - `idx=$(mktemp -u)` (a name outside the work tree and outside `.git/`);
   - with `GIT_INDEX_FILE="$idx"` set, run the git verbs `read-tree HEAD`, then `add -A` (every tracked and non-ignored file, into the private index only), then `write-tree`, which prints the tree; then `rm -f "$idx"`.
3. **Pin it** with a visible call: `git update-ref refs/superclaude/git/boundary-wt/<timestamp> <tree> ""`. The timestamp is UTC, as `YYYYMMDDTHHMMSSZ`. The empty last word makes the pin create-once: a ref that already exists is refused `pin-conflict`, and an earlier pin is never overwritten. A failed or incomplete snapshot or pin is `snapshot-failed`, and no commit is made.
4. **Commit.** The commit call of `commit.md`, with the prompt and timeout rules above.
5. **Compare after every attempt** that finished normally (exit status 0, 1 or 128). Take a second snapshot the same way, before any report or log is written, and compare every path outside S with the before tree: `git diff --name-status -z <before-tree> <after-tree>` lists additions, deletions, type changes and modes. A snapshot or comparison that fails stops `outside-unverified`, keeps the before pin, and is never read as "no changes". The whole set is compared. Showing at most 20 entries, with the total count and a truncation notice, is only a display limit.
6. **Damage.** Any path outside S that differs is `outside-changed`, even when the commit itself verified. Stop with that token, make no second commit, and keep the before pin. Name the count in the report and print this advice, never run it: `git restore --source=refs/superclaude/git/boundary-wt/<timestamp> -- <literal paths>`, with the words "compare first: this overwrites any newer edit". Do this for paths that existed in the before snapshot only. A path that did not exist then needs separate handling, never a blanket restore or delete. Also name the real index content and the hook framework's saved patch files, if it keeps any, as further evidence. Never restore, reset, stash or delete a lock or a saved patch yourself. The pin stays until the person says to release it.
7. **Clean comparison.** Only after the comparison finds nothing outside S, delete the pin with a visible call, `git update-ref -d refs/superclaude/git/boundary-wt/<timestamp>`, and say so in the report. A pin is kept only while an outside-change report about it is outstanding. The next `/sc:git` write reports a kept pin first.

Coverage is stated, not implied: tracked work-tree content and non-ignored additions, including assume-unchanged and skip-worktree entries. It does not cover ignored files, empty directories, file metadata or the inside of a submodule. Another process writing in the same work tree, and arbitrary trusted hook or filter behavior, stay outside the guarantee.

## Interruption and quiescence

A reported timeout, or an exit status above 128, leaves the attempt open. Write no result, classify nothing, and stop `commit-interrupted`, saying: check that no git or hook process is still running in this worktree before restoring anything or re-running. Read-only observations may be shown as provisional. The absence of a lock file is not proof that processes stopped. Never kill an orphan process and never remove a lock. Keep the before pin.

## What every write report adds

The report of `SKILL.md` always names: the checks run, each argv exactly as run, HEAD before and after, whether the index and the work tree changed, the pin ref and whether it was kept or deleted, and the undo advice (`git reset --soft <parent>` only for an unpushed commit, or `git revert <sha>`). Printed advice authorizes nothing. Never print file contents, credentials or a remote URL that carries credentials.
