# Coverage matrix (UC-1, Pass 2 inferred rows)

Parsed rows: 0. Inferred rows: 82. coverage_pct_union: 0.9024. S_dev_density: 0.0976.

| id | cite | matched | method | ratio | quote |
|---|---|---|---|---|---|
| INF-001 | source.md:16 | Task 11 | containment | 0.769 | It never uses `--force` on a worktree removal, never `git branch -D`, never `rm`, never pushes to a source repo and never deletes a remote branch. |
| INF-002 | source.md:16 | Task 1 | containment | 0.75 | Its only push goes to the evidence repo. |
| INF-003 | source.md:16 | Task 8 | containment | 0.8 | Tracked edits and commits made after the pull request always keep the worktree. |
| INF-004 | source.md:78 | Task 2 | containment | 0.8 | Dry run is the default for every verb that could remove something; `--apply` is the only way to remove. |
| INF-005 | source.md:82 | Task 6 | containment | 0.833 | Prints a table of every git worktree of every repo of ours, one decision (keep or removable) and one reason per row. |
| INF-006 | source.md:83 | Task 9 | containment | 0.909 | Runs only the evidence step of section 7 on one worktree: copy, push, check against GitHub. |
| INF-007 | source.md:84 | Task 15 | containment | 0.615 | Removes one worktree whose work is safe, run from outside it, usually right after its pull request merges. |
| INF-008 | source.md:85 | Task 12 | containment | 1.0 | Runs the same decision on all worktrees and removes the removable ones. |
| INF-009 | source.md:87 | Task 6 | containment | 0.87 | One row per worktree: repo, folder, branch, in Orca (yes or no), pull request and state, issue(s) and state, idle days, size, saved copy (none needed, saved and checked, or failed), decision and reason. |
| INF-010 | source.md:89 | Task 11 | containment | 0.727 | Each step fails closed: if any step cannot be completed or read back, the worktree is kept and the reason is shown. |
| INF-011 | source.md:91 | Task 13 | containment | 0.625 | Without a `VERIFIED` result the worktree is kept and nothing below happens. |
| INF-012 | source.md:92 | Task 11 | containment | 1.0 | An `unverifiable` or failed close keeps the worktree. |
| INF-013 | source.md:93 | Task 11 | containment | 1.0 | Any change since the save and any process still inside the worktree keeps it. |
| INF-014 | source.md:94 | Task 11 | containment | 0.778 | Never a path that is not in the manifest, never `-d` on a folder as a whole, never a tracked file (decision 2). |
| INF-015 | source.md:95 | Task 11 | containment | 1.0 | For a worktree Orca lists: `orca worktree rm --worktree id:<id>` without `--force`. |
| INF-016 | source.md:95 | Task 13 | containment | 0.833 | For a worktree Orca does not list (the 13 removable ones today): `git worktree remove <path>` without `--force`. |
| INF-017 | source.md:96 | Task 2 | containment | 1.0 | **Remove the local branch with `git branch -d`, never `-D`.** |
| INF-018 | source.md:97 | Task 11 | containment | 0.778 | Confirm the folder is gone, `git worktree list` no longer shows it and `orca worktree list` no longer shows it. |
| INF-019 | source.md:99 | Task 11 | containment | 1.0 | In a dry run (no `--apply`) steps 1 to 7 are not run |
| INF-020 | source.md:102 | Task 4 | containment | 0.824 | a repo whose `origin` belongs to IronbellyOrg or IronbellyGroup, found from `orca repo list` plus `git worktree list` in each repo (so worktrees Orca does not list are covered), wherever they sit |
| INF-021 | source.md:105 | Task 2 | containment | 0.778 | As a second guard the script skips any worktree whose folder name starts with `orca-port-`, `orca-recipe-` or `orca-pristine-`, or is `orca-old-patched`, even if git lists it. |
| INF-022 | source.md:112 | Task 18 | containment | 0.733 | One Orca automation per Coder workspace, once a day at 2:00 AM Central (08:00 UTC), switched on by that workspace's owner. |
| INF-023 | source.md:112 | Task 18 | containment | 1.0 | The name must not start with `coordinator-`. |
| INF-024 | source.md:116 | Task 18 | containment | 0.6 | The cron string is `0 8 * * *` (UTC). |
| INF-025 | source.md:124 | Task 2 | containment | 0.667 | Python standard library only, no model call anywhere. |
| INF-026 | source.md:125 | none | none | 0.375 | It is a command, not a skill: a skill installs for everyone and would break the opt-in schedule. |
| INF-027 | source.md:126 | Task 18 | containment | 1.0 | The automation definition, written and switched off, modelled on `scripts/merged_pr_log_orca_automation.md`. |
| INF-028 | source.md:131 | none | none | 0.417 | a precheck command that exits non-zero makes Orca skip the run and start no agent session. |
| INF-029 | source.md:137 | Task 18 | containment | 0.944 | Name: `worktree-cleanup-daily`. Trigger: `0 8 * * *` (UTC; 2:00 AM Central in winter, decision 11). Status: written, not switched on. |
| INF-030 | source.md:144 | Task 13 | containment | 1.0 | `GH_TOKEN` (never read from a file by the script; it is passed to `gh` and to `git push` through the environment). |
| INF-031 | source.md:146 | Task 12 | containment | 0.944 | One lock file per repo in the output folder, so two runs cannot remove the same worktree twice; a second run after a removal finds nothing more to do. |
| INF-032 | source.md:148 | Task 12 | containment | 1.0 | Each run writes `<out dir>/prune-<UTC timestamp>.md` (the table) and a `.json` of the same rows |
| INF-033 | source.md:148 | Task 12 | containment | 0.821 | Exit codes follow Jay's: 0 means the run completed (some worktrees may be kept; read the table), 64 means a usage error or a `retire` of a worktree that is not removable, 69 means a lookup or a removal failed (the table still shows what happened). |
| INF-034 | source.md:148 | Task 12 | containment | 1.0 | No output names an agent or a model. |
| INF-035 | source.md:150 | none | none | 0.556 | Clay switches it on in his workspace and for the first week it only writes the table (no `--apply`) |
| INF-036 | source.md:154 | Task 6 | containment | 0.667 | A worktree is removed only when ALL eight rules hold. |
| INF-037 | source.md:154 | Task 1 | containment | 0.889 | Every rule fails closed: if the script cannot tell, it keeps the worktree. |
| INF-038 | source.md:158 | Task 12 | containment | 0.667 | It is a linked worktree of one of our repos that this run may touch. |
| INF-039 | source.md:159 | Task 5 | containment | 1.0 | Its own pull request is MERGED. |
| INF-040 | source.md:160 | Task 9 | containment | 0.8 | Nothing was added after the pull request. |
| INF-041 | source.md:161 | Task 6 | containment | 1.0 | The issue it was for is CLOSED. |
| INF-042 | source.md:162 | none | none | 0.5 | Nothing unsaved is in it. |
| INF-043 | source.md:163 | Task 13 | containment | 0.6 | Nothing but its own Orca terminals is using it. |
| INF-044 | source.md:164 | Task 8 | containment | 1.0 | It has been idle for at least 7 days and was not created in the last 7 days. |
| INF-045 | source.md:165 | none | none | 0.5 | It is not pinned and nobody asked to keep it. |
| INF-046 | source.md:170 | Task 11 | containment | 0.867 | Decision 1 allows `git clean -f -x` for the exact paths saved and verified in the evidence repo and for nothing else |
| INF-047 | source.md:171 | Task 11 | containment | 0.909 | Close an Orca terminal of a worktree that has not passed every other rule and whose save is not verified. |
| INF-048 | source.md:173 | none | none | 0.562 | Run `git worktree prune`, because a missing folder can mean a disk is not mounted (Jay's guard); it reports such a worktree and leaves it. |
| INF-049 | source.md:175 | Task 11 | containment | 0.75 | Create, move or change a file inside a worktree it keeps (the archive step reads and copies; it never edits). |
| INF-050 | source.md:176 | Task 12 | containment | 0.75 | Read a credential from a file, print a credential, or name an agent or a model in any output. |
| INF-051 | source.md:186 | Task 9 | containment | 0.833 | Needs the merged pull request of rule 2. Without one it refuses (nothing is saved for unmerged work). |
| INF-052 | source.md:188 | Task 9 | containment | 0.929 | Pack the ignored files under `.dev/` (not `__pycache__`) into `ignored.tar.gz`, split into parts of 85 MB when larger |
| INF-053 | source.md:188 | Task 9 | containment | 0.857 | Write `saved-paths.txt`, one exact path per line |
| INF-054 | source.md:188 | Task 9 | containment | 0.96 | Write `MANIFEST.md`: source repo, branch, pull request link and title, merge date, worktree head and pull request head, worktree folder, time saved, count of files, and a SHA-256 of each archive file and of `saved-paths.txt`. |
| INF-055 | source.md:189 | Task 9 | containment | 0.889 | Commit in the evidence repo with the message `archive(<repo>): <date> pr<N> <subject>`. |
| INF-056 | source.md:190 | Task 9 | containment | 1.0 | If the push is refused, repeat from the fetch up to 3 times |
| INF-057 | source.md:191 | Task 6 | containment | 0.8 | Print `VERIFIED <folder> files=<n>`. |
| INF-058 | source.md:192 | none | none | 0.5 | It never overwrites a folder. |
| INF-059 | source.md:194 | Task 9 | containment | 1.0 | `<source-repo>/<pr-author>/<YYYY-MM-DD>_pr<number>_<subject>/`. |
| INF-060 | source.md:212 | Task 6 | containment | 0.667 | after the save is pushed and verified against GitHub, do whatever is needed to make the worktree removable, for the saved untracked and ignored files only. |
| INF-061 | source.md:235 | Task 9 | containment | 0.667 | YES: a names-only secret check before pushing. |
| INF-062 | source.md:244 | Task 8 | containment | 0.625 | They never touch a real worktree. Each case must fail if its rule is removed. |
| INF-063 | source.md:249 | Task 13 | containment | 1.0 | Decision 3: a worktree that passes every rule and has Orca terminals open and a process inside is removed in `--apply` only after `orca terminal close --worktree id:<id> --all` is confirmed |
| INF-064 | source.md:251 | Task 5 | containment | 0.909 | A squash-merged pull request whose commits are not on the base is judged landed from pull request state, not ancestry. |
| INF-065 | source.md:252 | Task 8 | containment | 1.0 | A pull request that is merged but whose branch was later reused for new commits keeps the worktree. |
| INF-066 | source.md:255 | Task 2 | containment | 1.0 | A test records every command the script runs, in every verb and every branch |
| INF-067 | source.md:257 | Task 12 | containment | 0.933 | A second run after a removal finds nothing more to do; two runs at once do not both remove the same worktree (one lock per repo). |
| INF-068 | source.md:259 | Task 13 | containment | 1.0 | No output names an agent or a model (a test greps the table, the summary and the log). |
| INF-069 | source.md:264 | Task 9 | containment | 1.0 | An ignored archive larger than 85 MB is split into parts that join back to the same bytes. |
| INF-070 | source.md:266 | Task 10 | containment | 1.0 | Two clones pushing different folders at the same time both end up on `origin/main` after the rebase and retry. |
| INF-071 | source.md:268 | Task 13 | containment | 0.917 | Decision 1: exactly the paths in `saved-paths.txt` are cleared (including a name with a space) and nothing else |
| INF-072 | source.md:269 | Task 11 | containment | 0.941 | Decision 2: a merged worktree with a tracked edit or a commit after the pull request is kept, nothing is cleared, no terminal is closed and nothing is archived by `prune`. |
| INF-073 | source.md:271 | Task 7 | containment | 1.0 | `git worktree remove` without force refuses a worktree with an untracked file and one with a modified tracked file, and removes one that holds only ignored files |
| INF-074 | source.md:274 | Task 20 | containment | 0.846 | A dry run in Clay's workspace prints a table whose counts match `git worktree list` |
| INF-075 | source.md:275 | Task 19 | containment | 0.769 | Jay's files that are adapted keep his Apache-2.0 notice and say what was changed |
| INF-076 | source.md:276 | Task 20 | containment | 0.643 | The regression gate passes: the full test suite, `make lint` and the sync checks that `/sc:pr-submit` runs. |
| INF-077 | source.md:276 | Task 17 | containment | 0.8 | No em or en dashes in new files. |
| INF-078 | source.md:373 | Task 1 | containment | 0.7 | on throwaway worktrees only, and write the findings to `.dev/research/worktree-cleanup-proofs.md`. |
| INF-079 | source.md:375 | none | none | 0.556 | registered where the repo lists commands. Reuse the landed check of #668. |
| INF-080 | source.md:376 | Task 2 | containment | 1.0 | A provenance block with Jay's Apache-2.0 notice at the top of the script. |
| INF-081 | source.md:377 | Task 19 | containment | 0.667 | **Retire the manual tool** in the evidence repo (its `tools/archive-workspace.sh` becomes a pointer to the script) |
| INF-082 | source.md:379 | Task 1 | containment | 0.714 | **Pull request** with `/sc:pr-submit --monitor 3`. |
