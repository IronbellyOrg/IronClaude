# Retrospective: IronClaude 6.0.0 release

Written by the `ic6-orchestrator` session after the tag and the post-release run. Everything here is a proposal: no release procedure, skill or command was changed. Clay reviews this first. Facts come from `PROCESS-LOG.md` (entries 1 to 36), `RELEASE-READINESS.md`, `DECISIONS.md` and the agents' process notes in this folder.

## 1. What we did, in order, with times

All times UTC. Dates are 2026-11-16 to 2026-11-18.

| When | What | Time it took |
|---|---|---|
| 11-16 | Clay decided 6.2 (keep `integration`), 6.4 (merge #570), 6.5 (tag on green), 6.7 (small fixes ship in 6.0.0) | planning, before this session |
| 11-17 07:27 to 18:32 | Ryan approved wave 1 (W1); decided swarm stays (S1, 13:06) and where `/sc:review-translation` moves (S2, 18:32); Clay kept `integration` (S3), set merge-without-asking (S4) and the no-history-edits rule (S5) | planning |
| 11-17 19:48 | Orchestrator started: read the brief, issue 571 (155 KB of comments), `release-procedure.md` and the 5.0.0 records; wrote the four records files; merged `master` into `integration` | 5 min + 4 min |
| 11-17 19:50 to 20:49 | Wave 1: PRs 1 `prd-cli` (#616), 2 `cleanup-audit-runner` (#615), 5 `spawn` (#617) | 60 min |
| 11-17 20:51 to 22:16 | Wave 2: PRs 6 `save-load` (#620), 7 `build` (#622), 10 `review-translation` (#621) | 85 min |
| 11-17 22:18 to 23:52 | Wave 3: PR 8 `improve` (#627) and small-fix PRs A (#626) and B (#625) | 94 min |
| 11-17 23:54 to 11-18 00:25 | Wave 4: PR 4 `cli-portify` (#629), alone | 31 min |
| 11-18 00:27 to 02:05 | Wave 5: PR 9 `index` (#631), PR 11 roadmap, tasklist, sprint (#632); the PR 9 agent never started and was relaunched (12 min lost) | 98 min |
| 11-18 02:07 to 03:08 | Wave 6: PR 12, the retire step (#633), new code | 61 min |
| 11-18 03:10 to 03:40 | Release preparation written: version 6.0.0, `CHANGELOG.md` `[6.0.0]`, `docs/releases/v6.0.0.md`; asked Ryan about 6.1, 6.3 and 6.6 once | 30 min |
| 11-18 03:19 to 14:51 | Release preparation PR #634: three fix rounds, a fourth thread answered; waited about 10 hours for Clay's approval of the third round | 11.5 h, almost all waiting |
| 11-18 14:55 to 15:46 | `master` merged into `integration`: the API returned a 409 conflict in the routing guide, Clay was asked, an agent resolved it as #639 (opened 15:36, merge commit) | 51 min |
| 11-18 15:47 to 16:27 | Release PR #640 (`integration` to `master`) opened; reviewers finished; gate G1 to G9 run on the merged tree | 40 min |
| 11-18 16:29 to 16:30 | Clay's yes relayed (merge commit; accept the one known failing test); #640 merged as `3f3b34a26` | 1 min |
| 11-18 16:34 to 16:37 | Hold (Part B scope), then released: Part B ships as 6.1.0 | 3 min |
| 11-18 16:39 to 16:40 | Tag `v6.0.0` pushed 16:39:58; GitHub release published 16:40:17 | 11 min from "Clay's yes", 9 of them waiting for CI on the merge commit |
| 11-18 16:43 to 17:11 | Fix of the flaky install-keep test (#646) | 28 min |
| 11-18 16:43 to 18:31 | Post-release (#649): docs sync, real install and upgrade runs, two review fix rounds | 108 min |
| 11-18 17:13 | Part B issue number received (#647); GitHub release body updated | 2 min |
| 11-18 18:31 to 18:40 | Post-release merged; final #571 comment; this retrospective | |

Totals: first agent started 2026-11-17 19:50; tag 2026-11-18 16:39:58 (20 hours 50 minutes later, of which about 10 hours were waiting for one approval); post-release merged 18:31. Pull requests: 15 merged into `integration` for the release (the 13 planned plus #634 and #639), one merge commit into `master` (#640), and 2 after the release (#646, #649). Nudges to agents: 6 (1 body fix, 4 rebase instructions, 1 idle agent) and 1 relaunch. Questions to Clay: the #634 third round, the `master` conflict, the release PR merge with the failing test, and the #510 checklist (still unanswered, non-blocking).

## 2. What worked, what did not, and why

### What worked

- **One agent per removal, in waves, merged by the orchestrator after reading GitHub itself.** 13 planned pull requests merged in about 7 hours 18 minutes of clock time. A wave of one took 31 minutes; waves of three took 60 to 94 minutes. Parallel waves beat one at a time even with the rebases (entry 21).
- **The merge rule** (every check green, Augment and Codex finished on the final head, no open thread, read from GitHub's thread list and not from the reviewers' status comments). It caught a stale "unresolved" count twice (entries 11 and 19) and a wrong pass-count claim in my own records (entry 29).
- **Generated lists instead of hand lists.** The removed names, hashes and flags came from `git ls-tree` and the old tag's own help output (entries 26, 28). The retire step generates its data from the tag, so the next release regenerates it in one command.
- **A real install and upgrade run in a throwaway home** (gate G7, G8 (d), and the post-release workstream C) found things unit tests did not: the old package's installer cannot remove anything, so the notes had to say "package first, then installer" (entry 29); `doctor` fails while a customized removed command is kept; Claude Code's own updater can replace the `claude` binary during a first install.
- **Reading deletion code myself** before merging the retire step (entry 27), and reading each fix PR's changed-file list against the approved scope (entry 18).
- **Waves feeding the next prompts.** Notes from wave 1 went into wave 2's prompts and the Generator-Constraint section appeared in the PR body from the start from wave 4 on (entry 21).
- **Tag on green with a prepared body.** From "Clay's yes" to a live release took 11 minutes, 9 of them waiting for the CI run on the merge commit.

### What did not work, and why

| Problem | Evidence | Cause |
|---|---|---|
| **Part B (the task and documentation bundle) was not in the brief and was caught only at the release PR.** After the release PR had merged into `master`, a hold stopped only the tag. | Entries 32, 33; `DECISIONS.md` 6.3 | The brief listed decision 6.3 as "still open with Ryan", planned waves only for Part A and the small fixes, and nobody mapped Part B or decided whether it was in 6.0.0. GeneralIronFlow's account is that Part B was left out of the brief by GeneralIronFlow. Once the release PR is merged, `master` is the release for anyone who installs from git, so a scope decision after the merge can no longer change the code. |
| **Scope decisions 6.1, 6.3 and 6.6 were still open at the release PR.** Ryan did not answer; Clay answered 6.3 and the post-release scope later. | `DECISIONS.md` | The release procedure has no step that requires scope decisions before the release PR merges. |
| **The release preparation PR waited about 10 hours on one approval** (a third fix round) | Entry 29 | A rule that every extra fix round needs Clay's approval, combined with an overnight gap. Three of the four review threads were about my own gate wording in a record file inside the pull request; the reviewers read records that describe gate criteria as requirements. |
| **Merging #634 with `--delete-branch` deleted the records branch.** | Entry 29 | The records branch was the head of the pull request. Recovered by re-pushing within a minute; nothing lost. |
| **The gate script was written by hand during the release, and its first run was invalid.** | Entries 29, 31 | No `.claude/` mirror (`make sync-dev` not run), no `ruff` in the virtualenv, then the newest `ruff` instead of the pinned `0.15.20`. A full local `make test` takes about 24 minutes. |
| **The plan's test baseline (14610) was obsolete** and the pass count differed between agents (3 to 13 failures on the same tree). | Entries 7, 15, 31 | The suite is now about 22,650 tests, and load-sensitive tests and the shared `/tmp/eval-runs` folder fail differently depending on how many agents run the suite at once. A fixed count rule is unreliable; "no new failing id, and CI green" is the usable rule. |
| **One known flaky test (`test_same_content_...`) failed alone on every run** and stayed in the baseline of every PR for 24 hours. | Entries 7 to 25, 31, 34 | The cause was a real installer defect (a stale `filecmp` cache), found only when #646 was done after the release. It was accepted as a known failure instead of being fixed first. |
| **The last PR of a wave paid twice for shared files.** | Entries 9, 14, 15, 16 | Almost every removal PR edits `PROJECT_INDEX.*`, `technical-architecture.md`, `test_routing_refresh.py`, `test_cli_install.py`, `WORKER-CONTRACT.md`, the routing guide. Three per wave always gave one or two rebases. |
| **The plan's "edits outside" counts were too low.** | Entries 19, 24 | They are counts of known edits; shared sentences and the root `commands/` copies were missed (9 against 22; 19 too low for PR 8). |
| **`master` merged into `integration` only at the start of each wave, so the last merge conflicted** (a routing guide edited by two release lines). | Entry 30 | Merge cadence, not an error in any one PR. |
| **#480 merged after 5.0.0 with no changelog entry** and was found only by my test upgrade. | Entry 31 | No check compares merged pull requests with the changelog. |
| **A PR agent never started** (`claude: not found`, the updater replaced the binary mid-launch). 12 minutes lost. | Entry 23 | The watch looked for idleness, not for a failed start. |
| **The agents' permission prompts for `rm -rf "$(cat ...)"`** stopped two finished agents; `orca terminal send` into a permission prompt is refused. | Entry 8 | An unresolvable path in a delete command. A literal path avoids it. |
| **`#649`'s install script came back with five Augment findings in three rounds**, all about its own exit-code check. The two-round cap was reached with 2 Medium findings answered, not fixed. | Entry 36 | The script printed results but never failed, and its failure path had no test. Each round found a smaller hole in a guard written after the fact. |
| **`Closes #N` in a PR into `integration` does not close the issue.** | Entry 18 | GitHub closes only on merge to the default branch. The release PR body had to carry the `Closes` lines; it did. |
| **Wrong figures in my own reports** (6 of 12 removal PRs; "Ryan's answer never needed"; 14610; 22648 versus 22649). | Entries 17, 29 | Written from memory instead of from the records. Fixed each time Augment or I re-read; the rule that works is to copy numbers from the records file. |

## 3. Draft release template

The template has four parts. Parts B to D are stub files copied into `.dev/releases/current/vX.Y.Z/` on day one (entry 2 showed the first commit should be a copy, not a write). Part A is the release-plan issue.

### A. The release-plan issue (starting from issue 571)

Keep issue 571's sections, and add the ones it lacked. Each row names an owner.

1. **Goal and "Done when" list.** Every item the release depends on has an owner in the brief, or is marked "not in this release", before wave 1 starts. (6.0.0 lost Part B here.)
2. **Decisions so far** (a table kept in the issue body, updated by the orchestrator, so nobody reads 21 comments). Each row: number, question, recommendation, owner, answer, date. **Scope decisions (version, what is in, post-release scope) are gate items: answered before the release PR merges.**
3. **Scope table:** one row per pull request: item, branch, worktree name, exact approved scope, the issue it closes, files expected (a floor, not a count), shared files it will touch, merge order.
4. **Closes list:** every issue the release closes, copied into the release PR body.
5. **Waves:** which rows start together; at most two per wave when they share docs and tests, or the merge order given to every agent up front.
6. **Gate list (G1 to G9 plus release-specific checks)** with the exact criteria written once, precisely. Criteria in the issue, not in a record inside a pull request.
7. **Known failing tests:** each with its id, the reason, who fixes it, and whether it blocks. A known failing test that is a real defect is fixed in a small PR before the gate.
8. **Out of scope, for later.**

### B. `RELEASE-READINESS.md` (stub)

Sections: 1 Baseline (taken once on `integration` with the same command the gate uses, per mode); 2 Pull requests (number, change, branch, state, link, tests before and after, merge time and commit); 3 Ordering and dependencies; 4 `master` merged into `integration` (each time, with the commit); 5 Waves reported (link to each #571 comment); 6 Gate on the release PR's merge commit (G1 to G9 with the command run, the result, and the tree id gated); 6b Tag and release (steps with times); 7 Finished worktrees (for the owner to remove).

### C. `DECISIONS.md` (stub)

Columns: number, decision, answer, decided by, date. Rows for scope (version, branch model, what is in, post-release scope), for how pull requests are merged (who merges, on what evidence), for historical records (never edited), and for the coordinator itself (who may start it).

### D. `PROCESS-LOG.md` (stub) and the per-agent notes

One entry per step: date and time, step, commands or skills, how long it took, what went well, what got in the way, what should change. Each agent keeps `PROCESS-NOTES.md` (one line per step) and the orchestrator copies the useful lines in when its PR merges. Entry fields are as in this release's log; the file ends with "Out of scope, for later".

### E. Prompt template for an agent (one file per pull request)

The 6.0.0 prompts converged on a fixed body that should ship as a template: the task and its exact scope; the venv setup line (`uv venv --python 3.10 && uv pip install -e '.[dev]' 'pytest-xdist>=3.5,<4' 'ruff==0.15.20' && make sync-dev`); the baseline command and a list of known load-sensitive tests; the `## Generator-Constraint Considered` PR-body rule; the no-subagents rule; delete throwaway homes with a literal path; the merge order and rebase rule; "known review findings" with the standard answers (retire step belongs to the retire-step PR; root `commands/` is a static copy; the guard-list question); `/sc:pr-submit` arguments (`--body` text, not a file path); where to write `PROCESS-NOTES.md`; and "STOP, do not merge".

## 4. Draft release workflow

Branches: removal and fix pull requests go to `integration`; `master` is reached only by the release PR; the records live on their own branch (here `clayphi/release-6.0.0`), which is never the head of a pull request merged with `--delete-branch`. Owners: the **owner** (Clay) decides scope and gives the yes before the release PR merges; the **orchestrator** runs the waves, merges into `integration`, keeps the records and runs the gate; **agents** each do one pull request in their own Orca worktree and stop at a green PR.

| Step | Who | Commands or skills | Gate to leave the step |
|---|---|---|---|
| 1. Plan | owner, planning session | release-plan issue (template part A); `/sc:release-split` when a part of the plan is unmapped | Every "Done when" item has an owner or is marked "not in this release"; scope decisions answered or scheduled as gate items |
| 2. Brief the orchestrator | owner, planning session | brief file; records stubs copied in | The brief names every item of the plan |
| 3. Baseline | orchestrator | the gate script on `integration` (see section 5, item 6); `git merge-tree` against `master` | A fresh baseline per mode in `RELEASE-READINESS.md`; the failing tests that pass alone are listed |
| 4. Fix known real defects first | orchestrator, one small PR | a normal PR | A known failing test that is a real defect is fixed before the waves, so no PR carries it |
| 5. Waves (two PRs per wave when they share files) | orchestrator starts agents; agents build | `orca worktree create ... --agent claude --prompt`; the prompt template (part E); a watch per agent; `/sc:pr-submit --monitor 3` inside the agent | Every check green, Augment and Codex finished on the final head, no open thread, read from GitHub by the orchestrator |
| 6. Merge after each PR | orchestrator | `gh pr merge --squash` (not `--delete-branch` on the records branch); `master` merged into `integration` after each wave, not only at the start | Merged; the wave comment on the plan issue and the summary to the coordinating session |
| 7. Release preparation | orchestrator | version, changelog cut, release notes; a changelog completeness check against `git log --first-parent <last tag>..master` | G3 and G4 pass; every merged PR since the last tag is in the changelog or named as excluded |
| 8. Scope decisions | owner | decisions table | **All scope decisions answered before step 9** |
| 9. Release PR (`integration` to `master`) | orchestrator | `gh pr create --repo IronbellyOrg/IronClaude --base master --head integration`; the body carries the `Closes` list | Green, reviewers finished, no open thread |
| 10. Gate G1 to G9 on the merged tree | orchestrator | the gate script (`make sync-dev`, pinned `ruff`, the checks, the throwaway-home upgrade from the previous tag), run while the PR waits for reviewers | All pass, or the failure goes to the owner |
| 11. Owner's yes, merge | owner says yes; orchestrator merges | `gh pr merge --merge` | Merge commit on `master`; the gated tree id equals the merged tree id |
| 12. Tag and publish | orchestrator | annotated tag on the merge commit after G2 is re-read on that SHA; `gh release create --verify-tag --notes-file` | Tag exists, release published, not a draft |
| 13. Post-release | agent | `/sc:post-release vX.Y.Z` with the scope decided in step 8; one PR into `integration` | Docs synced, install and upgrade runs green in throwaway homes, PR green |
| 14. Close out | orchestrator | final comment on the plan issue; records pushed; `RETROSPECTIVE.md`; list of finished worktrees for the owner | Plan issue left open for the owner to close |

What an orchestrator checks in every wave (all done by hand in 6.0.0, none by script): the PR's latest check results; its reviews with their commit ids; Codex's state comment; the thread list from GraphQL; the agent's evidence folder. `verify.sh`, `waitpr.sh`, `watch.sh` and the prompt generator were written during the release and are not in the repository.

## 5. Proposed changes (proposals only)

None of these is done. Each has its reason and the evidence in this folder. The skill proposals rest on the command file (`src/superclaude/commands/post-release.md`, which has only `<version>` and `--output`) and on the post-release agent's notes; I did not run `/sc:release-split` in this release, so the proposals for it are UNVERIFIED against a real run.

### `docs/developer-guide/release-procedure.md`

| # | Proposal | Reason |
|---|---|---|
| 1 | Add a step before "Open the release PR": **answer every scope decision (version, what is in, post-release scope, anything still marked open) and record who answered.** State that after the release PR merges, `master` is the release for anyone who installs from git, so a hold can only stop the tag. | Part B was found after the merge, and a hold four minutes later could only stop the tag and the release (entry 32). |
| 2 | In "Open the release PR", add a **changelog completeness check**: compare `git log --first-parent <last tag>..master` (and the pull requests merged into the release branch) with the pull request numbers in the new section; every merged PR is in the changelog or named as excluded. | #480 merged after 5.0.0 with no entry and was found by accident (entry 31). |
| 3 | In the same step: the release PR body carries a **`Closes #N` list**, and say that `Closes` in a pull request into an integration branch does not close the issue. | Entry 18; worked in 6.0.0 only because I copied the list in. |
| 4 | Add a **branch rule**: merge the release-preparation pull request without `--delete-branch` when its head branch also holds the records, or keep the records on a different branch. | Entry 29: the records branch was deleted on GitHub and re-pushed. |
| 5 | Move the **update of `docs/getting-started/upgrading.md`** (and any other page that names the current version or the counts) from post-release into the release preparation. | Users read it the moment the tag exists; in 6.0.0 it still described 5.0.0 for the first two hours after the release (post-release found it). |
| 6 | State which **version files** the gate checks and which it leaves (`pyproject.toml`, `__init__.py`, `CLAUDE.md` labels, the observe golden file `tests/observe/golden_release1_surface.json` that records the version), and say that `package.json` and `.claude-plugin/plugin.json` are not bumped. | CI failed on the golden file after the bump (entry 29); the two other files were found by chance; root `VERSION` still says 3.7. |
| 7 | **Gate G5/G8 (b):** replace a fixed pass count with "no failing test id that passes alone is new relative to a baseline taken on the base branch with the same command, and CI `Test on Python 3.10` is green"; say that the full suite takes about 24 minutes and 9 minutes under `-n auto`; and require `make sync-dev` and the pinned `ruff` (`0.15.20`, whatever the repository pins) before `make test`. | The 14610 baseline was obsolete; the first gate run was invalid without the `.claude/` mirror and `ruff` (entries 7, 15, 29, 31). |
| 8 | **Gate G7:** describe the throwaway-home upgrade from a genuine previous-tag install (`git archive <tag> src`, its own interpreter path, `HOME` set to a new temporary folder, deleted with a literal path), and require `doctor` and the retire step's `Removed`, `Kept` and "nothing to do" lines in the record. | This is how G7 and G8 (d) were actually run and passed in 6.0.0; the text still describes `./update.sh` on the live workspace. |
| 9 | **Gate G8 (a):** require a written allowlist of intentional leftover names, collected from each PR body, before the leftover search is run. | The search for removed names is never empty (46 intentional lines in 6.0.0, entries 21, 24, 25, 31). |
| 10 | Add **"known failing tests"**: a known failing test that is a real defect is fixed in a small PR before the gate; if the owner accepts it for the gate, the record says so plainly and a fix PR is opened. | The flaky test was a real installer defect (#646) that every PR's baseline carried for a day. |
| 11 | In Step 4, say that the GitHub release body is the release notes without the front matter, and that when the notes change after the tag (post-release), the release body is edited to match. | Done by hand twice in 6.0.0 (#647, the backup-file sentence). |
| 12 | Add an **"Orchestrated release"** section, or link to the new release skill (below): the branch model, the waves, the merge rule (checks, both reviewers on the final head, thread list from GraphQL), `master` merged into the integration branch after each wave, the owner's questions (only for a failed gate, a merge conflict or a round past the cap), and the records. The current text begins "A human runs every step". | 6.0.0 ran this way for 33 hours; none of it is written down outside this folder. |

### `sc-post-release-protocol` and `/sc:post-release`

| # | Proposal | Reason |
|---|---|---|
| 1 | Add a **`--workstreams A,B,C`** option (default all five). | Decision 6.6 skipped D and E; the command only has `<version>` and `--output`, so the scope lived in a prompt line. |
| 2 | Put the **throwaway-home rules** in the skill (set `HOME` to a new folder, clean environment, a private copy of the `claude` binary, wait for three good probes, delete by a literal path, check the real home before and after). | The agent needed four runs of about 10 minutes each: three first-install steps failed with `Claude CLI is unavailable` when Claude Code's updater replaced the binary mid-run (post-release notes). |
| 3 | Add a **citation-drift check** to workstream B that compares a note's citations with the tree of the note's last commit and resolves bare file names. | The agent's checker gave false positives for notes written after the previous tag and missed citations without a `src/` prefix; about 25 minutes of manual fixes. |
| 4 | Say in the skill that **the install script must fail on an unexpected exit** and ship a negative-path test with it. | Five Augment findings in three rounds, all about the e2e script's own result check (entry 36). |
| 5 | Let the caller give the **prompt and the "not in this PR" list of a referenced pull request** (here #480) so the text matches the code. | The prompt said "every installed file"; the code and PR limit the backup to commands, rules and output styles. |

### `sc-release-split-protocol`

| # | Proposal | Reason |
|---|---|---|
| 1 | Run `/sc:release-split` at step 1 of the workflow whenever a part of the plan is unmapped or undecided (in 6.0.0: Part B and Part C). Its input is the spec file, so the plan issue's "Done when" list should be exportable to one. | Part B was in effect split into 6.1.0 after the release PR merged, by a hold, not by an analysis. UNVERIFIED: I did not run the skill. |

### A new release skill (proposal: `sc-release-orchestrate`, command `/sc:release`)

It carries the workflow of section 4 so an orchestrator session is started with one command. Contents, each from this release:

1. Records stubs (template parts B to D) copied into `.dev/releases/current/vX.Y.Z/`.
2. The **prompt generator** (`/tmp/ic6-gen/gen.py` here) and the **prompt template** (part E).
3. The **watch and verify scripts** (`watch.sh`, `verify.sh`, `waitpr.sh`): failed-start detection (`not found`, `No such file`, `exec:` in the first minutes), the 12-minute idle rule, one-call PR state (latest check per name, reviews with commit ids, Codex state, GraphQL thread list).
4. The **gate script**: `make sync-dev`, pinned `ruff`, the checks, the throwaway-home upgrade test, the leftover search with the allowlist; run on the release branch while the release PR waits for reviewers.
5. The **merge rule** and the **question rule** (ask the owner only for a failed gate, a conflict, a round past the cap, or a decision that is the owner's).
6. The **changelog completeness check** and the **closes list**.

### Smaller tool changes seen in this release

- `make sync-dev` does not delete files that `src/` no longer has, so `make verify-sync` fails after a removal until the files are deleted by literal path (agent note, entry 25).
- `make baseline`-style target that writes the test counts to a file; give each worktree its own `TMPDIR` so parallel suites do not collide on `/tmp/eval-runs` (entries 7, 15).
- `/sc:workflow` has no option to skip its reflect step when subagents are banned (entry 27); the pre-check that needs subagents cannot run in agent sessions.
- The Orca `send` into a permission prompt is refused: instruct agents to use literal paths in deletes (entry 8).
- Review bots: Augment took 13 minutes on a 123-file PR and 10 on a 1,146-file PR (entries 21, 31); the watch needs an explicit wait for it. Their status comments keep a stale "unresolved" count, so a watch must read the thread list (entries 11, 19).

### Open items for the owner, not process changes

- #510 checklist question (`docs/testing/v5.0.0/impact-validation/william.md` stays unedited by my recommendation; unanswered).
- Decision 6.1 (version 6.0.0) and 6.6 (post-release scope) were never answered by Ryan; Part C (#572, the agents evaluation) is undecided.
- Follow-ups from #649: a failure-path test for the install script, `unset NOTRACK EXPECT_RC` at its top, no technical document for `observe`, no changelog entries for the new command-line groups, the release notes' validation numbers (39, 37, 37) against the run's (38, 36, 36), root `VERSION` 3.7.
- Pull requests #641 (Clay's ccsession feature into `master`) and the Coder repository's pin-bump pull request for the 6.0.0 commit: I have not touched either.
