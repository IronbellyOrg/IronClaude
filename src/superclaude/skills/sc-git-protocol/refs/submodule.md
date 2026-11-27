# Submodules with /sc:git

Loaded for `submodule status`, `submodule update <path>...` and `submodule commit-pointer <path>`. `status` is a read and loads only this ref. `update` and `commit-pointer` are writes and load `safety.md` with this ref. Every git call below is its own visible Bash call, and every write runs with `GIT_TERMINAL_PROMPT=0` as `safety.md` says.

Only top-level registered submodules are handled. A row whose `nested` flag is true carries the reason `nested-not-inspected`: nothing inside it is read, updated or committed. The helper, `vcs submodules`, runs only for a line the person typed. It returns, for each row, the facts, one `state`, and two eligibility objects, `update` and `commit_pointer`, each with `ok` and `reason`. A value the helper could not read is `null`. Never show a null as clean, and never decide an eligibility yourself when the object says no. When the helper cannot be run, or its output is not JSON with `vcs_contract` equal to `"1"`, refuse `helper-missing`.

## What the helper says, in words

| `state` | Meaning |
|---|---|
| `conflict` | the module has a merge conflict entry |
| `dirty-tracked`, `dirty-untracked` | the module has changed tracked files, or untracked files |
| `detached-new-commits` | the module HEAD is detached, differs from the recorded commit, and is on no branch |
| `uninitialized` | the module was never cloned here |
| `target-not-local` | the recorded commit is not in the module's object store |
| `submodule-ahead` | the recorded commit is an ancestor of the module HEAD (the module moved on) |
| `submodule-diverged` | neither commit is an ancestor of the other |
| `pointer-moved` | the module HEAD is an ancestor of the recorded commit (the superproject moved on) |
| `in-sync` | the module HEAD is the recorded commit |
| `null` | a fact it needs is unknown; the row's `reason` says which |

An ancestry lookup that git could not answer is never shown as `submodule-diverged`.

## status

1. Run `vcs submodules`. When it refuses `not-a-repo`, say so and stop. When `rows` is empty, print "no submodules" with the superproject lines below.
2. Print the superproject branch and the short HEAD sha (`superproject`).
3. Print `config.submodule_recurse` and `config.push_recurse_submodules` as configured. A value of `null` is printed as "unset", and "unset" and "false" are never merged. Print `warnings` as they are; when `submodule.recurse` is true the text says a later plain push may push submodules too.
4. Print one row per submodule, sorted by path, with: `path`, `state`, the short `gitlink` (recorded in HEAD), `index_gitlink` (recorded in the index) and `head` (checked out), `branch` or "detached", the three dirty flags (`commit_changed`, `tracked_dirty`, `untracked_dirty`), `initialized`, `target_local`, `contained`, `remote_mismatch`, `url_configured`, `fetch_mismatch`, `gitmodules_url` (already without credentials), the `update` result and the `commit_pointer` result. Add `reason` whenever it is set. A `null` is shown as "unknown", with the reason.
5. Advice, printed and never run, at most one line per row that is not `in-sync`: `pointer-moved`, `target-not-local` and `uninitialized` point to the `submodule update` operation; `submodule-ahead` points to `submodule commit-pointer`; `dirty-tracked`, `dirty-untracked` and `conflict` say to deal with the module first, from inside it; `detached-new-commits` says `git -C <path> switch -c <name>` keeps the commits (for the person to run); `submodule-diverged` says to decide by hand.

## update

Line: `submodule update <path>... [--url <path>=<url>]...`. One line authorizes the named paths only. `update` runs `git --literal-pathspecs submodule update --init --checkout -- '<path>'`, once per path. `--literal-pathspecs` makes git read the path literally, so a glob character in it (`lib[1]`) cannot select another module. It never recurses and never carries `--recursive`, `--remote`, `--force`, `--merge` or `--rebase`. It does carry `--checkout`, so that a module's own `submodule.<name>.update` setting (`none`, `merge` or `rebase`) cannot skip the update or merge or rebase instead of checking out the recorded commit. Its one outward effect is that git may clone a missing module or fetch a missing commit from the URL recorded in `.gitmodules`. Git's default recursive fetch may also contact the remotes of nested modules that are checked out, or that the fetched commit brings in, and the helper cannot see those. That is the single network exception of `/sc:git`, and it is made only on this typed line.

### Preflight, for every path before any write

1. Authorize as `SKILL.md` says. Run `vcs preflight` and refuse `operation-in-progress`, `index-locked` and `git-too-old` as `safety.md` defines them. As with branch changes, the call changes a module work tree and not the superproject history.
2. Run `vcs submodules` once. For each named path find its row. A path that is not a top-level registered submodule is refused in words, and no command line is printed.
3. For each row read `update`. When `ok` is false, refuse that path with the token in `reason`:

| `reason` | What to tell the person |
|---|---|
| `remote-mismatch` | `submodule.<name>.url` in the repository config differs from `.gitmodules`, also for a module that is not yet cloned (`submodule init` keeps a url already configured, and the clone uses it), or, when git would fetch a missing commit, the module's own `origin` (or the remote its branch tracks, or its only remote) has a url other than `.gitmodules` (`fetch_mismatch`). Print `git submodule sync -- <path>` as advice for the person to run. Remotes are never substituted. |
| `pointer-staged` | the index records a different commit for the module than HEAD does (`index_gitlink` differs from `gitlink`), and `submodule update` checks out the index commit. Print `git restore --staged -- <path>` as advice for the person to run, or to commit the pointer first. |
| `submodule-dirty` | the module has uncommitted changes; deal with them from inside it |
| `conflict` | the module has a conflict |
| `detached-new-commits` | HEAD is detached and on no branch, so an update would orphan commits. Stop and ask. Print `git -C <path> switch -c <name>` as the way to keep them. |
| `submodule-ahead` | the module is ahead of the record; the `submodule commit-pointer` operation records it |
| `submodule-diverged` | the two commits have diverged; decide by hand |
| `in-sync` | nothing to do |
| `path-unrepresentable` | the path holds a single quote or a control character, which could end the quoting of the command line (the same token applies to `commit-pointer`). Refuse it; the person renames the module or runs git by hand |

   Other reasons (`state-unknown`, `remote-unverifiable`, `containment-unknown`, `gitmodules-url-unknown`, `nested-not-inspected` for an update that may fetch into a module that has its own `.gitmodules`; `remote-unverifiable` also covers a branch that names a repository directly instead of a configured remote) mean the helper could not prove the path safe: say which fact is unknown and refuse. A relative `.gitmodules` URL is not compared with the configured one, so an initialized module with such a URL, and an uninitialized one whose config already holds a url (`url_configured`), end here as unverifiable.
4. For a row with `update.needs_url` true (an uninitialized module), print the `gitmodules_url` shown in the row and say that this update clones from it, over the network. The update runs only when the person's line repeats that displayed text, byte for byte, as the `--url` option for that path, in the form `<path>=<url>`. A missing, different or altered value is refused in words with the displayed URL printed; the call is not made. The comparison is always against the displayed text, which has any credentials removed. Never print a URL that carries credentials.
5. For `target-not-local` (the helper has already shown the module is clean and its HEAD is on a branch), say before the write that git may fetch the missing commit from the `.gitmodules` URL, and that git's recursive fetch may also contact nested modules' remotes. For `pointer-moved` the target is already local.
6. When any named path is refused, no path is written. Report every path as refused (with its token) or untouched, and stop. The person may type a new line.

### Write, one path at a time

For each path, in the order typed:

1. Run `vcs submodules` again and check that the row still has `update.ok` true and, for an uninitialized module, that its `gitmodules_url` still equals the text the person repeated. A change is a refusal for this path and every later path.
2. Run `GIT_TERMINAL_PROMPT=0 git --literal-pathspecs submodule update --init --checkout -- '<path>'` with the Bash timeout of 600000 ms. Do not retry. When git or the host would ask for a credential, stop and report it, as `safety.md` says. A timeout or an exit status above 128 leaves the path open: classify nothing, say a git process may still be running, kill nothing and remove no lock.
3. Read back with `git -C '<path>' rev-parse HEAD` and compare it with the row's `gitlink`. Equal: the path is `updated`. Different: the result is `uncertain`, reported with both shas, and the update is not repeated.
4. A path whose call fails, or is `uncertain`, ends the run. The paths after it stay untouched. Earlier paths are not rolled back.

### Report

Follow `SKILL.md` and add a list with every path as one of three groups: completed (old head, new head), untouched, failed (with the token or the git message, at most 40 lines). Say that the index and the superproject HEAD did not change, and that the recorded commit in the superproject is unchanged: only the module work tree moved. Running the same line again reports satisfied paths as `in-sync`. Undo advice, printed and never run: for a checkout, `git -C <path> checkout <old head>` returns the module to where it was; a fresh clone is not undone by this command.

## commit-pointer

Line: `submodule commit-pointer <path> (--message "<text>" | --smart-commit)`, with exactly one of the two message flags. It records the module's current commit as the new recorded commit of the superproject: a commit with the single changed path `<path>`. One path only. It is a local-history write and applies the full preflight.

### Conditions

1. Run `vcs preflight` and refuse all five of its refusals (`detached-head`, `protected-branch`, `operation-in-progress`, `index-locked`, `git-too-old`) for the superproject. The module's own HEAD may be detached; that is checked below. When `snapshot_lossless` is false, refuse `snapshot-unsupported`, as `safety.md` says.
2. Run `vcs submodules` and take the row of `<path>`. A path that is not a top-level registered submodule is refused in words.
3. Read `commit_pointer`. When `ok` is false, refuse with its `reason`:

| `reason` | Text |
|---|---|
| `submodule-dirty` | the module is not initialized, has a conflict, or is not clean: "commit inside the submodule first; run `/sc:git commit` from inside it" |
| `in-sync` | the module HEAD already is the recorded commit; nothing to do |
| `submodule-unpublished reason=no-gitmodules-remote` | the module has no remote whose URL equals the `.gitmodules` URL |
| `detached-new-commits` | the target is on no branch at all; print `git -C <path> switch -c <name>` as the way to keep it |
| `submodule-unpublished` | the target is not on a remote-tracking branch of that remote; use the refusal text below |
| `state-unknown`, `containment-unknown` | a needed fact is unknown; say which, and refuse |

   There is no override flag. A detached module HEAD at a target that is contained is eligible.
4. Record the full target: the row's `head`. It is the only commit this operation may record.

### Last fetch and the refusal text for an unpublished target

The helper does not supply a time. Read it with two read-only calls: `git -C '<path>' rev-parse --absolute-git-dir`, then `stat -c '%y' '<that folder>/FETCH_HEAD'` (on BSD, `stat -f '%Sm'`). A missing file prints as "never". This is the time of the last fetch that wrote that file in this module, as a local observation.

For `submodule-unpublished`, print this text with the values filled in and no command line: "`<short-sha>` is not on a remote-tracking branch of `<path>`'s `.gitmodules` remote (local refs; last fetch: `<time or never>`). Push it first, or run `git -C <path> fetch` yourself if it is already pushed. `/sc:git` never pushes and never fetches on its own; only `submodule update` may clone or fetch, from the `.gitmodules` URL, and only on the person's typed line." Stale local refs can refuse a target that is in fact published; a later rewrite on the remote can make a contained target unavailable. Say so once.

### Message, protect, write

1. Message. Make a temporary file outside the work tree with `mktemp` and write to it with the Write tool. With `--message`, write the person's text unchanged. With `--smart-commit`, draft it and show it: header `chore(submodule): bump <path> to <short-sha>` (the first seven characters of the target), body a short text from `git diff --submodule=log -- '<path>'`, quoting no file contents. Run `vcs check-message --file <that file>` and refuse `message` when it refuses.
2. Write the pathspec file for the one path: `printf '%s\0' '<path>' > <temporary file>`, outside the work tree. Print the path before the call. The commit set S is `{<path>}`. No other path is staged, and `.gitmodules` and the config are not touched.
3. Re-check the target just before the commit: run `vcs submodules` again. The row must still be eligible with the same full `head`; otherwise refuse in words, "the target changed", and make no commit.
4. Take the before snapshot and pin it, as steps 2 and 3 of "Protecting work outside the commit set" in `safety.md` say. Remember HEAD as the parent.
5. Run `GIT_TERMINAL_PROMPT=0 git --literal-pathspecs commit --only -F '<message file>' --pathspec-from-file='<pathspec file>' --pathspec-file-nul` with the Bash timeout of 600000 ms, as `safety.md` says. Do not retry.

### Read back and report

1. Run `git rev-parse HEAD`. When it changed, run `git rev-list --parents -n 1 HEAD` (one parent, the remembered one) and `git diff-tree --no-commit-id --name-only -r -z HEAD` (exactly `<path>`).
2. Run `git ls-tree HEAD -- '<path>'`. It must name the recorded target. When it does not, the result is `uncertain`: report both shas and stop.
3. Classify the outcome with the hook table of `safety.md`. `vcs verify` needs a boundary key and trailer that this commit does not carry, so take the class from the steps above, as the commit ref does. Take the second snapshot and compare it, as steps 5 to 7 of "Protecting work outside the commit set" say. A damage report stops the run, and the pin is kept.
4. Report as `SKILL.md` says. On success add: "on `<remote-ref>` as of last fetch `<time>`", labelled a local observation and not proof that others can fetch it. The remote refs come from `git -C '<path>' for-each-ref --contains <target> refs/remotes`; the helper has confirmed that one of them belongs to the `.gitmodules` remote. Undo advice, printed and never run: `git reset --soft <parent>` for a commit not pushed, or `git revert <sha>`.

## A commit inside a submodule

A commit inside a submodule is an ordinary `/sc:git commit` run from inside the submodule's own work tree, with its own preflight, branch and hooks. A detached HEAD there is refused until a branch exists, which is the safe order: the module commit comes first, then `commit-pointer` records it. This command does not run a commit for you across the boundary.

## Launched sessions

A session started by a launcher may deny every `git submodule` command at every level, because the launch guard does not know the verb. When a call is denied that way, report `blocked-by-host` with the denied argv, make no other attempt, try no other form of the command, and do not touch the guard. Reads through `vcs submodules` are unaffected.
