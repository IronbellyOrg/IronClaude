# 02b — Analysis: Spardutti `git-merge-conflicts` skill

Source: https://github.com/Spardutti/claude-skills, commit `f4c1f2a3539db1fd9b8aeb2ca78e8e5bac7975b1`, path `skills/git-merge-conflicts/SKILL.md` (254 lines). Focus: git merge-conflict resolution only. Analysis method: `/sc:analyze` (Discover, Scan, Evaluate, Report), read-only; nothing was run.

## 1. Summary

A single self-contained Markdown skill (no scripts, refs or other files in its folder) with YAML frontmatter that triggers on any merge, rebase, cherry-pick, stash pop or revert that stops with conflicts.
Its core rule is "resolve by intent, never by side": read both sides against the merge base, keep both behaviours when compatible, never invent code, and never abort.
It is laid out as seven ordered steps (orient, show the base with zdiff3, recover intent, resolve the hunk, sweep for unmarked semantic and tree conflicts, regenerate lockfiles and fix migration chains, prove with tests then continue), each with BAD/GOOD command or code examples.
It closes with a 14-line "Rules" list that restates the steps as always/never rules; the skill gives instructions only and has no executable automation.

## 2. Itemized behaviours and instructions

Where an item is also restated in the closing "Rules" list (lines 240-253), that rule line is cited after a comma.

- [S-01] Use the skill whenever a git merge, rebase, cherry-pick, stash pop or revert stops with conflicts, including "CONFLICT (content)", "Automatic merge failed", "could not apply", unmerged paths, or leftover `<<<<<<<` markers in a file. | source: skills/git-merge-conflicts/SKILL.md:4
- [S-02] Treat a conflict as two intents rather than two texts, and do not decide what the merged code should do until you can say what each side was trying to do. | source: skills/git-merge-conflicts/SKILL.md:9-10,240
- [S-03] Never pick a side just to make the markers disappear, because that silently deletes someone's work and tests usually still pass since the deleted behaviour had no test on this branch. | source: skills/git-merge-conflicts/SKILL.md:11-13,243
- [S-04] Never run `--abort` to escape a conflict; resolve it instead, because aborting throws away the analysis and hands the conflict to the next person. | source: skills/git-merge-conflicts/SKILL.md:15-16,253
- [S-05] Before editing anything, establish which operation (merge, rebase, cherry-pick and so on) is in progress, because the finishing commands and the meaning of "ours" differ. | source: skills/git-merge-conflicts/SKILL.md:18-21
- [S-06] Run `git status` to name the operation in progress and the unmerged paths. | source: skills/git-merge-conflicts/SKILL.md:24
- [S-07] Run `git diff --name-only --diff-filter=U` to list just the conflicted files. | source: skills/git-merge-conflicts/SKILL.md:25
- [S-08] Run `git log --oneline --graph -15 --all` to see what is being combined. | source: skills/git-merge-conflicts/SKILL.md:26
- [S-09] During `git merge feature`, treat `--ours`/`HEAD` as the branch you are on and `--theirs` as the incoming `feature` branch. | source: skills/git-merge-conflicts/SKILL.md:33-35
- [S-10] During `git rebase main`, treat `--ours`/`HEAD` as `main` (the branch being replayed onto) and `--theirs` as your own commit being replayed. | source: skills/git-merge-conflicts/SKILL.md:33-38,242
- [S-11] Never run `git checkout --ours <file>` during a rebase to "keep my changes", because it discards the commit being replayed. | source: skills/git-merge-conflicts/SKILL.md:38-44
- [S-12] Name the sides explicitly instead of trusting the labels by reading index stages: `git show :2:<path>` for ours. | source: skills/git-merge-conflicts/SKILL.md:46-48
- [S-13] Read `git show :3:<path>` for theirs. | source: skills/git-merge-conflicts/SKILL.md:49
- [S-14] Read `git show :1:<path>` for the merge base. | source: skills/git-merge-conflicts/SKILL.md:50
- [S-15] Set `git config --global merge.conflictStyle zdiff3` so the merge base appears inside every future conflict. | source: skills/git-merge-conflicts/SKILL.md:55-60,241
- [S-16] Re-render a file that is already in conflict with the base shown, without redoing the merge, using `git checkout --conflict=zdiff3 -- <path>`. | source: skills/git-merge-conflicts/SKILL.md:62-63
- [S-17] Read a zdiff3 conflict as three sides and compare each side against the base to tell which side changed a line and which merely has it. | source: skills/git-merge-conflicts/SKILL.md:55-57,66-78
- [S-18] When one side changed one part of a line and the other side changed another part, combine both changes into the merged line (example: `timeout: 30_000, retries: 3`). | source: skills/git-merge-conflicts/SKILL.md:78-81
- [S-19] Answer "why was this written" for each side before writing any resolution. | source: skills/git-merge-conflicts/SKILL.md:85
- [S-20] Run `git log --merge -p -- <path>` to see only the commits either side made to the conflicted file. | source: skills/git-merge-conflicts/SKILL.md:88
- [S-21] Run `git log --oneline HEAD..MERGE_HEAD` to see what the incoming branch did overall. | source: skills/git-merge-conflicts/SKILL.md:89
- [S-22] Run `gh pr list --search "<terms>"` to find the discussion behind the change. | source: skills/git-merge-conflicts/SKILL.md:90
- [S-23] Treat commit messages, PR descriptions and linked issues as the primary sources for why a change was made, since a diff only shows what changed. | source: skills/git-merge-conflicts/SKILL.md:93-94
- [S-24] Do not resolve a hunk by keeping HEAD's version when that drops a check the other side added (BAD example: rate-limit check lost). | source: skills/git-merge-conflicts/SKILL.md:98-104
- [S-25] Resolve a hunk so both intents survive in the merged code (GOOD example: HEAD's lookup change plus the other side's rate limiting). | source: skills/git-merge-conflicts/SKILL.md:106-113
- [S-26] Do not "merge" by inventing a third behaviour that neither side wrote or reviewed (BAD example: added `createGuestUser` fallback). | source: skills/git-merge-conflicts/SKILL.md:115-121
- [S-27] When the two intents are compatible, keep both, because most conflicts are two edits near each other rather than against each other. | source: skills/git-merge-conflicts/SKILL.md:125-126,244
- [S-28] When the intents are genuinely incompatible, pick the one that matches the merge's stated goal. | source: skills/git-merge-conflicts/SKILL.md:127
- [S-29] When you drop one side's behaviour, say out loud which behaviour you dropped and why. | source: skills/git-merge-conflicts/SKILL.md:127-128,246
- [S-30] Never introduce in a resolution any line that neither side wrote. | source: skills/git-merge-conflicts/SKILL.md:129-130,245
- [S-31] If the correct merge needs new code, put it in a follow-up commit rather than in the conflict resolution. | source: skills/git-merge-conflicts/SKILL.md:130-131
- [S-32] Never leave a conflict marker; delete every `<<<<<<<`, `|||||||`, `=======` and `>>>>>>>` line. | source: skills/git-merge-conflicts/SKILL.md:132
- [S-33] Expect that both sides can apply cleanly and still produce broken code (for example one side renames a function in one file while the other adds a call to the old name in another file), because git compares text and does not know the call graph. | source: skills/git-merge-conflicts/SKILL.md:136-147
- [S-34] After every resolution, run `git grep -n "<old name>\b"` to check whether a renamed symbol's old name is still called anywhere. | source: skills/git-merge-conflicts/SKILL.md:149-152
- [S-35] After every resolution, run `git diff --check` to find leftover conflict markers. | source: skills/git-merge-conflicts/SKILL.md:153
- [S-36] After every resolution, run `git grep -n "^<<<<<<< \|^>>>>>>> "` to find markers in files git no longer tracks as unmerged. | source: skills/git-merge-conflicts/SKILL.md:154
- [S-37] Sweep for semantic breakage covering renamed symbols, moved files and changed signatures. | source: skills/git-merge-conflicts/SKILL.md:247
- [S-38] Read the two-letter codes in `git status --short` to find tree-level conflicts, which have no markers. | source: skills/git-merge-conflicts/SKILL.md:157-158,248
- [S-39] For `DU`/`UD` (one side deleted the file, the other edited it), let the deletion win only if you can show the edit is obsolete; otherwise restore the file and re-apply the edit. | source: skills/git-merge-conflicts/SKILL.md:160-161
- [S-40] For `AA` (both sides added a file at the same path), merge the contents rather than keeping one file and dropping the other. | source: skills/git-merge-conflicts/SKILL.md:162-163
- [S-41] Recognise `AU`/`UA` as a file added by one side while the other side moved or renamed it. | source: skills/git-merge-conflicts/SKILL.md:164
- [S-42] Decide each `DU`/`UD` explicitly instead of letting `git add .` pick: `git checkout --theirs -- <path>` to keep the edited version, or `git rm <path>` to confirm the deletion. | source: skills/git-merge-conflicts/SKILL.md:166-170
- [S-43] Never hand-merge a generated file such as a lockfile, because the result matches neither side and no tool will ever reproduce it (BAD: resolving `package-lock.json` hunk by hunk). | source: skills/git-merge-conflicts/SKILL.md:174-179,249
- [S-44] For a lockfile conflict, take either side whole (example: `git checkout --theirs -- package-lock.json`). | source: skills/git-merge-conflicts/SKILL.md:181-183
- [S-45] Then let the tool rewrite the lockfile by running the package manager (`npm install`, `pnpm install`, `yarn`, `uv lock` or `poetry lock`). | source: skills/git-merge-conflicts/SKILL.md:184
- [S-46] Then stage the regenerated lockfile with `git add <lockfile>`. | source: skills/git-merge-conflicts/SKILL.md:185
- [S-47] Treat build output, coverage reports and committed snapshots the same way: regenerate and re-record them rather than editing. | source: skills/git-merge-conflicts/SKILL.md:188-189
- [S-48] Treat migration conflicts as ordering conflicts (two branches each added a migration with the same parent revision) and fix the chain rather than merging the text, which would leave two heads. | source: skills/git-merge-conflicts/SKILL.md:191-193,250
- [S-49] Alembic: repoint the later migration's `down_revision` at the other migration, or run `alembic merge heads`. | source: skills/git-merge-conflicts/SKILL.md:195-196
- [S-50] Alembic: verify with `alembic heads` that there is one head, not two. | source: skills/git-merge-conflicts/SKILL.md:196
- [S-51] Django: run `python manage.py makemigrations --merge`. | source: skills/git-merge-conflicts/SKILL.md:197
- [S-52] Drizzle/Prisma: keep both SQL files, then regenerate the journal or the migration lock so ordering is single-valued. | source: skills/git-merge-conflicts/SKILL.md:198-199
- [S-53] Never renumber a migration that has already run in any shared environment. | source: skills/git-merge-conflicts/SKILL.md:201
- [S-54] Consider a resolution done only when the project's own checks pass, not when the markers are gone. | source: skills/git-merge-conflicts/SKILL.md:205-206
- [S-55] Discover what checks this repo actually runs, then run its typecheck and tests (example: `npm run typecheck && npm test`, or `pytest`, `cargo test`, `go test ./...`) before continuing. | source: skills/git-merge-conflicts/SKILL.md:208-210,251
- [S-56] Fix whatever the merge broke before continuing, treating a merge commit that fails CI as an incorrectly resolved conflict. | source: skills/git-merge-conflicts/SKILL.md:213-214
- [S-57] Stage the resolution with `git add -A`. | source: skills/git-merge-conflicts/SKILL.md:217
- [S-58] Finish a merge with `git merge --continue`. | source: skills/git-merge-conflicts/SKILL.md:218
- [S-59] Finish a rebase with `git rebase --continue`, repeating the resolve-and-continue cycle until every commit is replayed. | source: skills/git-merge-conflicts/SKILL.md:219
- [S-60] Finish a cherry-pick with `git cherry-pick --continue`. | source: skills/git-merge-conflicts/SKILL.md:220
- [S-61] Use `git rebase --skip` (which drops your commit entirely) only when the change is already present upstream and you confirmed that by reading the diff. | source: skills/git-merge-conflicts/SKILL.md:223-224,252
- [S-62] Enable `git config --global rerere.enabled true` so git records each resolution and replays it when the identical conflict reappears during a long rebase. | source: skills/git-merge-conflicts/SKILL.md:228-235
- [S-63] Still read what rerere filled in, because a recorded resolution is a past decision, not a verified one. | source: skills/git-merge-conflicts/SKILL.md:235-236

## 3. Caveats

Changes global git config: S-15 (`merge.conflictStyle zdiff3`, line 60) and S-62 (`rerere.enabled`, line 231) use `--global`, which affects every repository for the user, not just the one in conflict.
"Never abort" policy (lines 15-16, 253) gives no escalation path: an agent stuck on a genuinely ambiguous conflict has no instruction to stop and hand back to a human.
Triggers on stash pop and revert (line 4), but Step 7 gives finish commands only for merge, rebase and cherry-pick (lines 218-220); no `git revert --continue`, and no guidance that a conflicted stash pop keeps the stash entry.
`git add -A` (line 217) stages every change in the working tree, including unrelated untracked files.
The DU/UD example `git checkout --theirs` "to keep the edited version" (line 168) assumes theirs is the editing side; during a rebase the sides are inverted (S-10), so the example can pick the wrong file.
`git log --oneline HEAD..MERGE_HEAD` (line 89) only works during a merge; `MERGE_HEAD` does not exist during a rebase or cherry-pick, and the skill offers no alternative there.
`gh pr list --search` (line 90) names no `--repo`; in a fork clone gh can resolve to the parent repository.
"Pick the one matching the merge's stated goal" (line 127) does not say where the stated goal comes from.
The marker grep on line 154 matches only `<<<<<<<` and `>>>>>>>` lines, not `=======` or `|||||||`.
Lockfile regeneration (line 184) and the typecheck/test run (line 210) execute package installs and project code, which can be slow, need network access, or run install scripts; no guidance is given when a repo has no tests.
The "Rules" list (lines 240-253) adds no new behaviour except naming "moved files, changed signatures" in the semantic sweep (line 247, S-37); everything else restates Steps 1-7.
