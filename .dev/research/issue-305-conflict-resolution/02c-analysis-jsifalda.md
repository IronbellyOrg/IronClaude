# 02c — Analysis: jsifalda/ai-project-rules `merge` skill (conflict resolution focus)

Source: https://github.com/jsifalda/ai-project-rules @ 338cc3fa1fa76e5429c765581fc49a9b2971a63d, path `skills/merge/SKILL.md` (279 lines). Local copy read: `/tmp/cr305-repos.Tkozsd/ai-project-rules/skills/merge/SKILL.md`. Method: `/sc:analyze` Discover, Scan, Evaluate, Report, focus narrowed to merge-conflict resolution. Nothing was run.

## 1. Summary

A single self-contained SKILL.md (no scripts or other files in `skills/merge/`) with six phases: 1 Preflight (one read-only bash block that aborts or prints resolved values), 2 Fetch and merge, 3 Resolve conflicts (agent prose, not a script), 4 Verify (project gates), 5 Push (guarded bash block), 6 Report (fixed six-line block), plus a "Hard rules" list and an "Abort conditions" table.
Approach: merge the base remote's default branch into the current PR branch, never rebase, never stash, never force; resolve conflicts by reading all three index stages and keeping both intents.
Generated files (lockfiles, snapshots, built assets) are regenerated, not hand-merged; decision-level conflicts (intentional same-behaviour changes, delete/modify, colliding migrations) STOP with the merge left in progress and resume through a `MERGE_HEAD` re-entry path.
Shell state is not carried between blocks; the agent copies Phase 1 values into later placeholders by hand.

## 2. Itemized behaviours and instructions

### Scope and triggers
- [J-01] The skill triggers on `/merge` or on phrases such as merge main into this branch, sync this branch with main, update this branch from main, pull main into here, or resolve conflicts with main and push. | source: skills/merge/SKILL.md:8-10
- [J-02] An optional argument, a base branch name, overrides the detected default branch. | source: skills/merge/SKILL.md:10-11
- [J-03] The skill must not be used to open a PR, to merge a PR into main, to rebase, to squash, to force-push, or to switch branches. | source: skills/merge/SKILL.md:11-12
- [J-04] The skill works in a linked git worktree and in a plain checkout, on GitHub and GitLab, with no provider CLI. | source: skills/merge/SKILL.md:7-8
- [J-05] The skill changes no branch other than the one currently checked out. | source: skills/merge/SKILL.md:21
- [J-06] The skill avoids `git checkout main` because in a linked worktree the default branch is usually checked out elsewhere. | source: skills/merge/SKILL.md:23-24

### Remote selection (forks)
- [J-07] The base remote, which holds the default branch, is `upstream` when that remote exists and `origin` otherwise. | source: skills/merge/SKILL.md:29-31, 70
- [J-08] The push remote is the remote of the branch's own configured upstream, and `origin` when no upstream is set. | source: skills/merge/SKILL.md:31, 58-67
- [J-09] The push branch name is read from `branch.<current>.merge` with the `refs/heads/` prefix stripped. | source: skills/merge/SKILL.md:59-60
- [J-10] When the upstream remote or branch is missing, or the remote is `.`, the push target falls back to `origin` and the current branch name, and a first push sets upstream. | source: skills/merge/SKILL.md:61-67

### Phase 1: Preflight
- [J-11] Preflight runs as one block that is read-only except `git remote set-head`, which writes only a local ref. | source: skills/merge/SKILL.md:35-36
- [J-12] Preflight either prints a single `ABORT:` line or prints the resolved values. | source: skills/merge/SKILL.md:36
- [J-13] Any `ABORT:` line ends the run; the agent prints the reason and stops. | source: skills/merge/SKILL.md:102
- [J-14] Abort when not inside a git work tree. | source: skills/merge/SKILL.md:41
- [J-15] Abort on a detached HEAD and tell the user to check out a branch. | source: skills/merge/SKILL.md:43-44
- [J-16] Detect an in-progress merge by testing for `MERGE_HEAD` through `git rev-parse --git-path`. | source: skills/merge/SKILL.md:46
- [J-17] Abort when a rebase (`rebase-merge` or `rebase-apply`), cherry-pick, revert, or sequencer operation is in progress, telling the user to finish or abort it. | source: skills/merge/SKILL.md:48-52
- [J-18] Abort on a dirty working tree only when no merge is in progress, telling the user to commit or discard changes. | source: skills/merge/SKILL.md:54-56, 110-112
- [J-19] `MERGE_HEAD` is tested before the dirty-tree check because an in-progress merge makes the tree dirty, so a resumed run must not hit the dirty-tree abort. | source: skills/merge/SKILL.md:105-107
- [J-20] Never stash, because every worktree shares one stash stack and a pop can take another session's work. | source: skills/merge/SKILL.md:24-26, 110-112
- [J-21] Abort when the push remote is not configured. | source: skills/merge/SKILL.md:68
- [J-22] Abort when the base remote is not configured. | source: skills/merge/SKILL.md:71
- [J-23] With no argument, the default branch is read from `refs/remotes/<base-remote>/HEAD`. | source: skills/merge/SKILL.md:73-76, 103-104
- [J-24] When that ref is unset, run `git remote set-head <base-remote> -a` and read it again. | source: skills/merge/SKILL.md:77-80
- [J-25] Abort when the default branch still cannot be detected, telling the user to run `git remote set-head <base-remote> -a`. | source: skills/merge/SKILL.md:81
- [J-26] Abort when the current branch or the push branch equals the default branch. | source: skills/merge/SKILL.md:83-85
- [J-27] When a merge is in progress, abort unless `MERGE_HEAD` is an ancestor of `<base-remote>/<default-branch>`, which proves it is a merge of the default branch and not a merge the user started by hand. | source: skills/merge/SKILL.md:87-89, 107-108
- [J-28] Preflight prints current, base_remote, default_branch, push_remote, push_branch, set_upstream, and merge_in_progress. | source: skills/merge/SKILL.md:91-97
- [J-29] `merge_in_progress: 1` means skip Phase 2 and resume at Phase 3. | source: skills/merge/SKILL.md:109
- [J-30] Each block runs as its own command, so the agent copies printed values into later `<...>` placeholders by hand and never reuses a variable from an earlier command. | source: skills/merge/SKILL.md:113-115

### Phase 2: Fetch and merge
- [J-31] Fetch only the default branch from the base remote. | source: skills/merge/SKILL.md:125
- [J-32] Merge with `git merge --no-edit <base-remote>/<default-branch>`. | source: skills/merge/SKILL.md:126
- [J-33] Keep Git's own merge message. | source: skills/merge/SKILL.md:129
- [J-34] Do not pass `--no-ff`; a fast-forward is a good result. | source: skills/merge/SKILL.md:129-130
- [J-35] `Already up to date` means nothing to integrate; go to Phase 5 and report `merge: nothing to do`. | source: skills/merge/SKILL.md:132-133
- [J-36] Exit status 0 with a fast-forward or clean merge means the merge is committed; skip Phase 3 and go to Phase 4. | source: skills/merge/SKILL.md:134-135
- [J-37] Exit status 1 with conflict lines means go to Phase 3. | source: skills/merge/SKILL.md:136
- [J-38] Merge, never rebase, because the branch is on a PR and a history rewrite breaks the review. | source: skills/merge/SKILL.md:26-27, 255

### Phase 3: Resolve conflicts
- [J-39] Conflict resolution is the agent's own work, not a script. | source: skills/merge/SKILL.md:140
- [J-40] Take conflicted files one at a time. | source: skills/merge/SKILL.md:140
- [J-41] List conflicted files with `git diff --name-only --diff-filter=U`. | source: skills/merge/SKILL.md:142
- [J-42] Read all three index stages before changing a file: `:1:` merge base, `:2:` this branch, `:3:` default branch, via `git show`. | source: skills/merge/SKILL.md:143-145
- [J-43] Keep the intent of both sides. | source: skills/merge/SKILL.md:145
- [J-44] Never take `--ours` or `--theirs` wholesale on a source file. | source: skills/merge/SKILL.md:145, 260
- [J-45] Lockfile conflicts are generated output and are regenerated, not merged; the listed lockfiles are package-lock.json, pnpm-lock.yaml, yarn.lock, bun.lock, bun.lockb, Cargo.lock, poetry.lock, uv.lock, Gemfile.lock, go.sum, and composer.lock. | source: skills/merge/SKILL.md:146-149
- [J-46] For a lockfile, run `git checkout --theirs -- <file>` and then regenerate it with the manager's lockfile-only command (examples: `pnpm install --lockfile-only`, `npm install --package-lock-only`, `cargo generate-lockfile`, `uv lock`, `go mod tidy`). | source: skills/merge/SKILL.md:149-152
- [J-47] For any other package manager, look up its lockfile-only flag; the command updates the lockfile and adds no package. | source: skills/merge/SKILL.md:152-153
- [J-48] Use only the package manager the repository's lockfile names, never a different one. | source: skills/merge/SKILL.md:153-154
- [J-49] A generated file whose source of truth is in the repository, such as test snapshots or deliberately committed built assets, takes the default-branch side and is then regenerated from its source. | source: skills/merge/SKILL.md:155-157
- [J-50] A conflict needing a product or design decision is a STOP; one such case is both sides changing the same behaviour on purpose. | source: skills/merge/SKILL.md:158-159, 261
- [J-51] The default branch deleting a file that this branch edits (delete/modify) is a STOP. | source: skills/merge/SKILL.md:159-160
- [J-52] Two colliding migrations are a STOP. | source: skills/merge/SKILL.md:160
- [J-53] On a STOP, leave the merge in progress. | source: skills/merge/SKILL.md:160, 276
- [J-54] On a STOP, report the file, the intent of each side, and one recommendation, and do not guess. | source: skills/merge/SKILL.md:160-161, 276
- [J-55] After the user answers a STOP, `/merge` resumes through the Phase 1 `MERGE_HEAD` path. | source: skills/merge/SKILL.md:161-162
- [J-56] Stage each file with `git add -- <file>` as soon as it is finished. | source: skills/merge/SKILL.md:163
- [J-57] Before committing, `git diff --cached --check` must print nothing. | source: skills/merge/SKILL.md:165-169
- [J-58] Before committing, a grep of `git diff --cached` for added conflict-marker lines (`<<<<<<< `, `=======`, `>>>>>>> `) must print nothing. | source: skills/merge/SKILL.md:165-166, 170
- [J-59] Close the merge with `git commit --no-edit`. | source: skills/merge/SKILL.md:173
- [J-60] Never commit with `--no-verify`. | source: skills/merge/SKILL.md:173
- [J-61] Report a pre-commit hook failure verbatim and fix its cause. | source: skills/merge/SKILL.md:173-174
- [J-62] After fixing a hook failure, stage the fix with `git add` and run `git commit --no-edit` again. | source: skills/merge/SKILL.md:174-175
- [J-63] Never `--amend` after a hook failure, because the merge commit does not exist yet. | source: skills/merge/SKILL.md:175

### Phase 4: Verify (gates and failure classification)
- [J-64] Run the gates the project defines for itself, reading `CLAUDE.md` or `AGENTS.md` first for a verification protocol. | source: skills/merge/SKILL.md:179-180
- [J-65] Then use package scripts (build, test, lint, typecheck) or the language equivalent such as `cargo test`, `go test ./...`, or `pytest`. | source: skills/merge/SKILL.md:180-182
- [J-66] A conflict resolution is authored code and gets whatever review path the project's protocol defines for authored changes. | source: skills/merge/SKILL.md:184-185
- [J-67] A clean merge that authored no line is integration only, and the project's protocol decides whether review runs on it. | source: skills/merge/SKILL.md:185-186
- [J-68] A gate that fails because of the merge gets a follow-up commit, never `--amend`, and the gates are run again. | source: skills/merge/SKILL.md:187-188
- [J-69] A failure counts as pre-existing only when the failing test or file was not touched by this branch and either the default branch's own CI is red or the failure is in code only the default branch changed. | source: skills/merge/SKILL.md:189-191
- [J-70] A pre-existing failure is reported as `FAIL (pre-existing)` and the run continues to the push. | source: skills/merge/SKILL.md:191-192
- [J-71] Do not stash anything to prove a failure is pre-existing. | source: skills/merge/SKILL.md:192-193
- [J-72] With no gates in the project, report `gates: none found` and do not invent one. | source: skills/merge/SKILL.md:194

### Phase 5: Push
- [J-73] Push only when the push remote is reachable and the local branch is ahead of it. | source: skills/merge/SKILL.md:198-199
- [J-74] Probe the remote branch with `git ls-remote --exit-code --heads <push-remote> <push-branch>`. | source: skills/merge/SKILL.md:209-210
- [J-75] Exit code 0 means fetch the push branch and count commits ahead with `git rev-list --count <push-remote>/<push-branch>..HEAD`, aborting if that fetch fails. | source: skills/merge/SKILL.md:213-214
- [J-76] Exit code 2 means the branch does not exist on the remote yet (first push), so it is treated as ahead. | source: skills/merge/SKILL.md:215, 228-229
- [J-77] Any other non-zero exit code is a network or auth failure and aborts with `cannot reach remote <push-remote>` instead of guessing. | source: skills/merge/SKILL.md:216, 229-230
- [J-78] Zero commits ahead reports `push: nothing to push`. | source: skills/merge/SKILL.md:219-220
- [J-79] When upstream must be set, push with `git push -u <push-remote> <current>`. | source: skills/merge/SKILL.md:221-222
- [J-80] Otherwise push with `git push <push-remote> HEAD:refs/heads/<push-branch>`. | source: skills/merge/SKILL.md:223-224
- [J-81] Never push with `--force`, `--force-with-lease`, or `--no-verify`. | source: skills/merge/SKILL.md:232, 257
- [J-82] Never push to a remote other than the push remote. | source: skills/merge/SKILL.md:232-233
- [J-83] Report a pre-push hook failure verbatim. | source: skills/merge/SKILL.md:233
- [J-84] A non-fast-forward rejection means someone pushed to the PR branch meanwhile; do not force, report `push: BLOCKED non-fast-forward`, and stop. | source: skills/merge/SKILL.md:235-236, 278
- [J-85] After a non-fast-forward block the user integrates the remote branch (for example `git pull --ff-only <push-remote> <push-branch>`) and runs `/merge` again; the skill never runs that command itself. | source: skills/merge/SKILL.md:236-238

### Phase 6: Report
- [J-86] Print a fixed report block and nothing after it. | source: skills/merge/SKILL.md:242
- [J-87] The report lists base (`<base-remote>/<default-branch> @ <short-sha>`), branch, merge (sha and subject, or nothing to do), conflicts (count and files, none, or `STOPPED on <file>`), gates (each pass, none found, or `FAIL (pre-existing)`), and push (target and sha, nothing to push, or `BLOCKED <reason>`). | source: skills/merge/SKILL.md:244-251

### Hard rules
- [J-88] Never push the default branch and never push a branch other than the current one. | source: skills/merge/SKILL.md:256
- [J-89] Never run `--amend`, `git stash`, `git checkout <other-branch>`, or `git pull`. | source: skills/merge/SKILL.md:257-258
- [J-90] A command the skill hands to the user to run is not the skill running it. | source: skills/merge/SKILL.md:258-259
- [J-91] Operate in the current worktree only and never touch another worktree or the main checkout. | source: skills/merge/SKILL.md:262
- [J-92] The abort-conditions table maps each abort to its fixed message, including `STOPPED on <file>` and `BLOCKED non-fast-forward`. | source: skills/merge/SKILL.md:264-278

## 3. Caveats

The skill directory contains only SKILL.md; no helper scripts or referenced files exist, so every item above comes from that one file.
Nothing was executed; the bash blocks were read, not tested.
Phase 3 is prose only, so the quality of conflict resolution depends entirely on the agent following it; there is no mechanical check that both intents were kept.
The lockfile rule takes the default-branch side (`--theirs`) and regenerates; the skill does not say to resolve the manifest (package.json, Cargo.toml, pyproject.toml) first, so this ordering is left to the agent (my observation, not stated in the source).
The marker grep checks only the `<<<<<<< `, `=======` and `>>>>>>> ` forms; a diff3 `|||||||` base marker is not in that pattern and is left to `git diff --cached --check` (my observation).
The pre-existing-failure rule depends on knowing the default branch's CI state, but the skill gives no command for reading it.
No rule covers binary, rename/rename, or submodule conflicts beyond the general STOP-on-decision rule.
GitLab and MR support is claimed in the description, but no step is provider-specific.
Line numbers were verified against the local copy at the stated commit.
