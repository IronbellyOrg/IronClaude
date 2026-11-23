<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (architect: release line, story branches, local merges) -->
<!-- Merge date: 2026-11-23T14:10:06Z -->

# Unified branching proposal for dashboard releases

## 1. Summary

<!-- Source: Base (original, modified) - Variant 1 sec 1 rewritten to stand alone; "Nothing is pushed for review until the release is complete" replaced per Change #21; retitled per Change #15 -->

### 1.1 In short

Every dashboard release (1.1, 1.105, 1.2, up to 2.0) gets one long-lived branch, called the **release line**, for example `release/dash1.3`. It is cut from `master` when the release starts. Every user story gets its own branch and its own Orca worktree (a separate working folder for one branch), cut from the release line. The coordinator (the session that runs the release) merges each settled story into the release line on its own machine, one story at a time, with a merge commit. After each merge it pushes the line forward to GitHub as a backup. No pull request for the release is opened until the line is frozen.

When the last planned story is in (or the time box ends), the coordinator merges `master` into the line, runs the checks, and `/sc:pr-submit --monitor 3` opens **one** pull request that takes the whole release into `master`. CI and the two automatic reviewers (Augment and Codex) run on that pull request. The owner merges it with a merge commit. Then the release is tagged, a sync pull request brings `master` back into `integration`, and the branches and worktrees are deleted.

This is the owner's model made precise. It keeps the coordinator, the progress ledger and the per-story pipeline (spec panel, plan, plan review panel, implement, per-task QA) as they are today. Its weak point is that nothing outside the coordinator's own test run looks at the code until the end, and the end is one large batch. Section 8 (a size budget counted in files) and the time box in Q4 bound that batch. The outside CI run and the optional review-only story pull request in Q2 give earlier looks.

### 1.2 Words used in this proposal

<!-- Source: Base (original, modified) - glossary is new text for a reader who has not seen the debate; the "integration branch" sentence is per Change #1 -->

| Term | What it means here |
|------|--------------------|
| Owner | The repository owner (Ironbelly). Merges every pull request and decides the open questions in section 10. |
| Clay | The other maintainer. Opens most pull requests into the repository branch called `integration`. |
| Coordinator | The AI session that runs one release: creates the line and the story worktrees, merges settled stories, keeps the ledger, runs the checks. It is the only writer of the ledger. |
| Worker | The AI session that builds one story in its own worktree. |
| Release line | The long-lived branch of one release, `release/dash<rel>`. The owner's words "integration branch" mean this release line. The repository branch called `integration` is a different thing, which is why the line is not called `integration`. |
| Story | One user story of the release, built on its own branch `dash<rel>-s<NN>-<slug>`. |
| Settled story | A story whose worker has finished the pipeline and whose verdicts are PASS. |
| Ledger | The file `sprint-status.yaml`, kept on the release line, written only by the coordinator. One line per story merge. |
| Path claim | The list of paths a story says it will touch. Two stories running at once must claim disjoint paths. |
| Local gate | The commands that copy what CI runs, taken from `test.yml` at release start and run by the coordinator after every story merge (Q2). |
| Merge commit, `--no-ff` | A merge that always creates a merge commit with two parents. One merge commit per story means one `git revert -m 1` can later remove that whole story. |
| Squash, rebase | Two other ways to merge. Squash flattens a branch into one commit; rebase rewrites a branch. This proposal uses neither for stories (rebase is never used once others branched from the branch). |
| Forward push | `git push origin release/dash<rel>` with no `--force`. A rejected push is a stop. |
| Merge in | Merge `origin/master` into the line with a merge commit (never a rebase). |
| `/sc:pr-submit --monitor 3` | The only way a pull request is opened here. It opens the PR on the fork, waits for CI and the two bots, fixes confirmed findings and replies. It runs in its own top-level session in the worktree of the PR's head branch. |
| The two bots | Augment and Codex, the automatic reviewers on pull requests. |
| CI | The workflow `.github/workflows/test.yml`. It runs only for pull requests and pushes into `master` and `integration`, so a pull request into a release line gets no CI. |
| Dispatch run | A manual run of `test.yml` on a pushed branch (`workflow_dispatch`). It tests the branch tip alone and does not run the pull-request-only workflows. |
| `.dev/` records | Planning, report and QA files kept under `.dev/`. They are committed on the branch where they were made, and they count as files in a pull request. |
| Freeze | The point after which only fix branches enter the line (Q6). |
| Time box | The limit that closes a release at six merged stories or seven days from the cut, whichever comes first. Scope floats, time does not. |
| Carried story | A story not merged when the time box ends. It moves to the next release. |
| Records PR | A pull request into `master` that carries only `.dev/` records, used when the release would be too large (section 8). |
| Sync PR | The pull request that brings `master` back into `integration` after a release lands. Its head branch is `dash<rel>-sync<N>`. |
| Ref conflict | Git cannot hold `dash1.3` and `dash1.3/story1` as branches at once, because a branch is stored as a file and `dash1.3` would also have to be a folder. Verified by the coordinator on 2026-11-23. |

### 1.3 How much to trust each number

<!-- Source: Variant 4 (GFxAI adapted), line 5 provenance marks, merged per Change #7 (marks replaced by the five below) -->

Nothing technical enforces any branching rule in this repository: `master` and `integration` have no protection and the repository has no rulesets (VERIFIED-PROBE). Every rule here is a rule the coordinator follows, so the marks below tell a reader which rules rest on evidence and which rest on taste. Every number or behaviour claim in this document carries one of them.

| Mark | Meaning |
|------|---------|
| VERIFIED-HERE | Run or read while writing this proposal on 2026-11-23 (a scratch repository under `/tmp`, CLI help, fetched documentation, a grep). |
| VERIFIED-PROBE | Verified by the invariant probe or by a debater with read-only commands during the debate; recorded in the debate files and not re-run for this text. |
| ESTIMATE | Derived from measured data by inference; the inference is stated. |
| GUESS | Chosen for headroom or convenience; no data behind it. |
| UNVERIFIED | Not confirmed. A trial in section 9 settles it. |

Everything marked "default" is a number or rule the owner may change (section 10).

### 1.4 How this fits the owner's decisions of 2026-11-23

<!-- Source: Base (original, modified) - new table per Change #29; owner decisions as stated in CONTEXT.md -->

| Owner decision | How this proposal fits | Departure or cost |
|----------------|------------------------|-------------------|
| Dashboard releases are integration branches merged to `master` when done | The release line `release/dash<rel>` is that branch. It lands in one pull request into `master` by a merge commit; then the next release is cut from `master`. | The line is not called `integration`, because the repository already has a branch of that name. |
| Stories are sub-branches | Each story is cut from the line and merged back. The link is kept by the Orca parent worktree, the `dash<rel>-` name prefix and the ledger. | Not a folder under the line's name: the owner's literal `dash1.3/story1` cannot coexist with `dash1.3`, and the folder form under `release/` is avoided as insurance (section 2). |
| No human plan approval; a panel verdict instead | The story pipeline gates on the panel verdict, which the coordinator writes into the ledger line. The coordinator merges a story when the verdicts are PASS, the path claims are disjoint, `git merge-tree` is clean and the local gate is green. | No human sees a story before the release pull request. That makes the size budget (section 8) and the bots the only readers, and it is why the optional review-only story PR exists (Q2). Humans still decide three things: local-merge authority, the numbers, and each release PR merge. |
| Two stories in parallel for the first release | Path claims must be disjoint; merges are serial. Re-open the design if the plan grows to about four parallel stories (A-004, 65 percent). | Shared files and pinned counts (Q2) are where two "disjoint" stories collide anyway. |
| Clay's habit of branching from `integration` | Unchanged while a release is built. `integration` is never merged into the line. After landing, the sync PR (Q8). | Clay's real landing branch is `master` (10 of the last 30 `master` commits are Clay's: VERIFIED-PROBE), so collisions that matter arrive through the merge-in of `master`. `master` is 26 commits ahead of `integration` and `integration` has had no merged PR since 2026-11-18 or 2026-11-19 (the two debate sources differ by a day; VERIFIED-PROBE). Decision 5 asks whether `integration` is still in use. |
| Pull requests only through `/sc:pr-submit --monitor 3`, in its own top-level session | Every PR in the design goes that way: release PR, records PR, sync PR, a revert PR, a two-PR landing, an optional review-only story PR. | About three to four pr-submit sessions per release (records when triggered, release, sync, plus any revert), each with an owner click. |
| CI runs only for PRs into `master` and `integration` | The release PR, the records PR and a revert PR get CI. Story merges are local, so they get none; the gap is covered by the local gate and by dispatch runs (Q2). | Whether to add `release/**` to the `pull_request` filter of `test.yml` is decision 6, recommended no for the first release. |

### 1.5 What the coordinator may and may not do

<!-- Source: Variant 4, rule 2 ("AI Agent: Merge to Main no") as a coordinator rule, merged per Change #8; upstream and fork-only sentence per refactor-plan "Concrete anchors preserved" -->

- The coordinator never merges a pull request and never merges into `master` or `integration`. Only the owner merges pull requests.
- A local merge of a settled story into the release line is a separate, smaller class of act: it is local, unpublished until the forward push, revertable, and the same class as the worker contract's child-into-feature merge. It needs the owner's confirmation in chat (the use-case notes say "to be confirmed"; decision 1). If the owner declines, every story goes through the optional review-only pull request in Q2.
- Nothing is committed directly on `master`. Every pull request goes through `/sc:pr-submit --monitor 3` with `--repo IronbellyOrg/IronClaude`. Nothing is ever pushed to, fetched from, or opened against `SuperClaude-Org` (the public upstream).
- A published branch is never rebased and never force-pushed. A merge conflict stops the coordinator; a worker resolves it (Q2).
- `.dev/` records are committed on the branch where they were made.

## 2. Branch names, examples, and the ref-conflict rule

<!-- Source: Base (original, modified) - Variant 1 sec 2 table and invariant replaced per Changes #1, #3, #10, #19, #20, #28; release line name from Variant 4 rule 1; flat names from Variant 2 sec 2 and Variant 3 sec 2; tag from Variant 4 rule 4 -->

### 2.1 The names

| Kind | Pattern | Example |
|------|---------|---------|
| Release line | `release/dash<rel>` | `release/dash1.3`, `release/dash1.105` |
| Story | `dash<rel>-s<NN>-<slug>` | `dash1.3-s04-token-usage-panel` |
| Fix inside a release | `dash<rel>-fix<NN>-<slug>` | `dash1.3-fix01-empty-state` |
| Sync PR head | `dash<rel>-sync<N>` | `dash1.3-sync1` |
| Records PR head (only when triggered, section 8) | `dash<rel>-records` | `dash1.3-records` |
| First half of a two-PR landing (only when triggered, section 8) | `release/dash<rel>-p1` | `release/dash1.3-p1` |
| One-story release (no line) | `dash<rel>-s01-<slug>` | `dash1.105-s01-add-widget-tests` |
| Fix of shipped code that belongs to no dashboard release | `fix/<issue>-<slug>` | `fix/731-ledger-path` |
| Marker after landing (a tag, not a branch) | `dash-<rel>` | `dash-1.3` |

`<rel>` is the dashboard release number, for example `1.3`. It is not the package version (the package is 6.1.0 on `master`), which is why the tag is `dash-1.3` and not `v1.3.0`.

### 2.2 The five rules that keep names from clashing

1. A branch name is never the folder part of another branch name. The only folders are `release/` and `fix/`, and no branch is named `release` or `fix`.
2. The bare token `dash<rel>` and the tag name `dash-<rel>` are never branch names. A tag and a branch with one name make `git checkout dash-1.3` ambiguous.
3. Release tokens are matched exactly or with a hyphen-terminated glob such as `*dash1.1-*`. The token `dash1.1` is a prefix of `dash1.105`: a glob `release/dash1.1*` matched both in a scratch repository (VERIFIED-HERE). A future release 1.10 is written 1.100.
4. The worktree name equals the branch leaf. The line's worktree is `dash1.3-release`.
5. After creating a worktree the coordinator reads the real branch name (`git -C <worktree> branch --show-current`) and writes it in the ledger.

To list one release: `git branch --list '*dash1.3-*'`. The leading `*` also finds a copy that carries the `ironbelly/` prefix that Orca adds by default.

Story numbers `s01` to `s99` sort in creation order. The planned release numbers (1.1, 1.105, 1.2 and on up to 2.0) group sensibly; the 1.10 hazard is rule 3.

### 2.3 Creating the branches

Check before creating a name: `git check-ref-format --branch <name>` succeeds; `git for-each-ref refs/heads/<name> 'refs/heads/<name>/*'` prints nothing; for names under `release/` or `fix/`, `git rev-parse --verify -q refs/heads/release` (or `fix`) fails.

```
orca worktree create --name dash1.3-release --branch release/dash1.3 --base-branch origin/master --agent claude
orca worktree create --name dash1.3-s04-token-usage-panel --branch dash1.3-s04-token-usage-panel --base-branch release/dash1.3 --parent-worktree <release worktree selector> --agent claude
```

The plain `worker-start` command has no `--branch` flag, so exact names need `orca worktree create`. The usage line of `orca worktree create` requires `--name`, which the first draft of this proposal had left out (VERIFIED-HERE).

### 2.4 Why story names are flat, and what that changes for the owner

<!-- Source: Variant 2 sec 2 and Variant 3 sec 2, merged per Change #10 -->

The owner wrote `dash1.3/story1`. This proposal writes `dash1.3-s04-<slug>` instead, and the reason is stated plainly: git does not force flat names (`release/dash1.3` plus `dash1.3/story-...` works). Flat names are insurance against one failure. A worktree created without `--branch` and called `dash1.3` gets the branch `ironbelly/dash1.3` (49 remote branches carry the `ironbelly/` prefix: VERIFIED-PROBE), after which `ironbelly/dash1.3/s04-...` cannot be created ("cannot lock ref"). A flat name is a leaf and cannot become the folder of another branch, with or without the prefix.

Three of four debaters chose flat names (70 percent confidence); the debater of the owner's model kept folders (60 percent). If trial T1 (section 9) shows that `--branch` always keeps the exact name and refuses a conflicting one, folders become safe again, and stories can be `dash<rel>/s<NN>-<slug>` under a line named `release/dash<rel>`. The ref-conflict rules above still hold. Flat stays the simpler default.

### 2.5 The tag, and what was checked

<!-- Source: Variant 4 rule 4 (tag `dash-1.3`), merged per Change #3 -->

The tag `dash-<rel>` goes on the merge commit on `master` after landing. In a scratch repository the tag `dash-1.3` sat next to the branches `release/dash1.3`, `release/dash1.105`, `release/dash1.1` and `dash1.3-s04-x` without error (VERIFIED-HERE).

| Status | Fact |
|--------|------|
| VERIFIED-HERE | `orca worktree create --help` prints `--branch <name>  Git branch name to use instead of the prefixed default`, so `--branch` replaces the `ironbelly/` prefix. The usage line requires `--name`. The tag coexists with the similar branch names above. |
| VERIFIED-PROBE | `git check-ref-format --branch` accepts `release/dash1.3`, `release/dash1.105`, `dash1.3-s04-slug`, `dash1.3-fix01-slug`, `dash-1.3` and `ironbelly/release/dash1.3`. No remote branch matches `release/*` or `dash*` today. |
| UNVERIFIED (trial T1) | That `--branch` keeps the exact name in a real run; that "a taken name gets a numeric suffix" (read from the CLI help by a debater, not seen again); what a name that conflicts with an existing ref does. |
| UNVERIFIED (trial T2) | That `worker-start --worktree path:<coordinator-created worktree>` adopts an exact-name worktree. |
| UNVERIFIED (trial T8, low priority) | How Orca, `/sc:pr-submit` and the closeout script treat a tag next to similar branch names. The git side is verified. |
| UNVERIFIED (trial T12, only for the third rung of Q5) | Whether stacked pull requests and a merge queue are available on this repository's plan. The design uses neither. Stacking is replaced by this, which was checked in a scratch repository (VERIFIED-HERE): line n+1 cut from line n's tip, n landed with a merge commit, `master` merged into n+1; then `git diff --name-only master...n+1` lists only n+1's own file. |
| UNVERIFIED (trials T3, T4, T6) | How `/sc:pr-submit` and the two bots behave on the release PR, on a PR above 300 files, and on a PR whose base is not `master`. Bots did review PRs into the non-default base `346Claude-integration` and CI did not run there (VERIFIED-PROBE); the rest is not seen. |

## 3. How a release moves from the first story to `master`

<!-- Source: Base (original, modified) - Variant 1 sec 3 diagram and steps 1 to 6 rewritten per Changes #1, #2, #4, #6, #10, #19, #21, #25, #26; worked timeline added for the owner's reading -->

### 3.1 The flow in one picture

```
master              A ------------------------------------------- F ----->
                     \                                           ^
                      \  (cut once, at release start)            |  owner merges ONE PR
                       \                                         |  (merge commit)
release/dash1.3         R0 --- M1 ------- M2 ---- X ---- (final) +
                          \   ^  \        ^       ^
                           s01     s02            master merged in (merge commit), then local gate
                (one worktree each; the coordinator merges with --no-ff, one at a time,
                 and pushes the line forward after each green merge)
```

`A` is the `master` commit the line is cut from, `R0` the first commit on the line, `M1` and `M2` story merge commits, `X` the merge of `master` into the line, `F` the merge commit on `master` made by the owner's click. Story branches are named `dash1.3-s01-<slug>` and so on.

### 3.2 The steps

1. **Cut the line.** Cut `release/dash<rel>` from `origin/master` (section 2.3). Replace the contents of `sprint-status.yaml` with the new release's header (release id, `master` tip at the cut); the previous ledger stays in `master` history and under its tag. Write the release brief as the first ledger entry (Q2 and Q4 say what it lists). Commit the planning `.dev/` records and the ledger on the line.
2. **Start each story.** Create the story worktree from the line tip with the flat name (section 2.3). The worker runs the story pipeline (spec panel, plan, plan review panel, implement, per-task QA) and commits its `.dev/` records on the story branch before it reports done.
3. **Merge a settled story.** In this order: path-claim check; predict the line's file count and write it to the ledger line (section 8.5); `git merge-tree` trial; `--no-ff` merge; local gate; ledger line; then `git push origin release/dash<rel>` (plain push, never `--force`; a rejected push is a stop). If the gate is red after the merge, do not push; reset the unpublished merge to the tip hash the ledger recorded before it, and send the story back to its worker. Story N+1 does not merge until story N's gate result is in the ledger. The push is a backup, not a review request: no pull request for the release is opened until the freeze (the only earlier pull requests are the optional review-only story PRs of Q2 and a records PR cut early, section 8.5). Pushing the line and the tag starts no workflow (VERIFIED-PROBE: only `test.yml` has a `push` trigger and it filters on `master` and `integration`).
4. **Bring a waiting story up to date.** The next story that was started earlier first merges the new line tip into itself (a merge, never a rebase), re-runs its checks, then is merged the same way.
5. **Freeze.** Freeze starts when the ledger shows the last planned story merged, or when the time box ends (six merged stories or seven days from the cut: Q4). From freeze until the owner merges, only `dash<rel>-fix<NN>-<slug>` branches enter the line, and no new story. While `/sc:pr-submit --monitor 3` runs, nothing enters at all (Q4).
6. **Count, then check.** Count the files of the release PR (section 8). If a records PR is needed, it goes first. Merge `origin/master` into the line, then run the gate list of Q4: local gate, a green dispatch run on the final tip, then `/sc:pr-submit --monitor 3 --base master` in its own top-level session in the line's worktree.
7. **The owner merges with a merge commit.** The release PR body starts with "Merge this pull request with a merge commit, not squash."
8. **After landing.** Tag `dash-<rel>` on the merge commit on `master`. Open the sync PR (head `dash<rel>-sync<N>`, Q8). Delete story, line and records branches and worktrees, local and remote, and run the sweep of Q7. BMAD planning (the planning method used here) of release n+1 starts from `master` after release n merges.

### 3.3 One release, start to finish (worked example)

The names, days and file counts below are an illustration of the rules, not measurements. Release 1.3 has five planned stories and one foundation story that owns the shared files (Q2).

| When | Who | What happens |
|------|-----|--------------|
| Before day 0 | Owner | Confirms in chat the coordinator's authority (decision 1) and the numbers (decision 2). |
| Day 0 | Coordinator | Runs the name check, creates the line: `orca worktree create --name dash1.3-release --branch release/dash1.3 --base-branch origin/master --agent claude`. Reads back the real branch name with `git -C <worktree> branch --show-current` and writes it in the ledger. Replaces the ledger header. Reads `git show origin/master:.github/workflows/test.yml` and writes the release brief: the exact local gate commands, the pull-request-only workflows, the shared-file list. Commits the planning records. |
| Day 0 to 1 | Worker, then coordinator | Foundation story `dash1.3-s01-shared-counts` (owns `CHANGELOG.md` and the count-pinned test) is built alone. Merge: path claim checked, predicted 12 files written to the ledger, `git merge-tree` clean, `--no-ff` merge, local gate green, ledger line, first `git push origin release/dash1.3`. Because it touches the shared list, the coordinator dispatches `gh workflow run test.yml --repo IronbellyOrg/IronClaude --ref release/dash1.3` and reads the result (about 9 minutes) before any later story that touches the same list merges. |
| Day 1 to 3 | Two workers, coordinator | `dash1.3-s02-token-usage-panel` and `dash1.3-s03-empty-state` run in parallel with disjoint path claims. s03 settles first and merges (total 50 files). s02 then merges the new line tip into itself, re-runs its checks, and merges (total 96). |
| Day 3 | Coordinator | `master` has moved (about 8 pull requests a day land there). Between two story merges the coordinator merges `origin/master` into the line and runs the gate. |
| Day 4 | Worker, coordinator | `dash1.3-s04-cost-chart` merges (predicted total 156, under the stop-adding threshold of 200). |
| Day 5 | Worker, coordinator | `dash1.3-s05-settings-page` is predicted to bring the total to 208. That is in the 201 to 250 band: it merges, and no new story starts. It is the last planned story, so the freeze begins. |
| Day 5 | Coordinator | Counts: `git diff --name-only origin/master...release/dash1.3 \| wc -l` gives 208, which is 250 or less, so no records PR. Merges `master` in, runs the gate, dispatches `test.yml` on the final tip and reads a green result. Checks whether any changed path matches `**/gates.py`, `**/structural_checkers.py` or `**/*_validator.py` (if so, the PR body gets the heading `## Generator-Constraint Considered`). |
| Day 5 to 6 | Coordinator, pr-submit session | A top-level session in the line's worktree runs `/sc:pr-submit --monitor 3 --base master`. During this window the line's worktree has one writer, pr-submit. On day 6 a bug is found in s03: the coordinator creates `dash1.3-fix01-empty-state`, the ledger says "queued", and it enters only after the monitor ends; then a new pr-submit run starts on the new head. |
| Day 6 to 7 | Owner | Reads the PR (path classes, per-story digest, bot findings) and merges with a merge commit. The ledger records the PR-opened and PR-merged times. |
| After the merge | Coordinator | Tags `dash-1.3` on the merge commit. Checks the merge commit has two parents (`gh pr view <n> --repo IronbellyOrg/IronClaude --json mergeCommit`, then `git cat-file -p <sha>` shows two `parent` lines). Cuts `dash1.3-sync1` from `origin/integration`, merges `master` in with a merge commit, pushes, and a top-level session runs `/sc:pr-submit --monitor 3 --base integration`. |
| After the sync PR merges | Owner, coordinator | Owner merges the sync PR. Coordinator deletes `release/dash1.3` and the worktrees (local and remote), then runs `git ls-remote --heads origin 'refs/heads/release/dash1.3*' 'refs/heads/dash1.3-*'`, which must print nothing. Planning of the next release starts from `master`. |

## 4. The nine questions

<!-- Source: Base (original, modified) - Variant 1 sec 4 (Q1 to Q9) with the changes named in each answer -->

### Q1. Names

<!-- Source: Base (original, modified) - Variant 1 Q1, per Changes #1, #10, #28 -->

See section 2. One rule: the release line is a leaf under the folder `release/`, and every story, fix, sync and records branch is a flat leaf with no slash. So no branch name is ever the folder of another, with or without the `ironbelly/` prefix that Orca adds by default. The names carry the release number and the story id, sort in creation order, and one pattern (`*dash1.3-*`) lists a whole release. After every creation the coordinator reads back the real branch name and writes it in the ledger. Whether `--branch` keeps the exact name is UNVERIFIED until trial T1.

### Q2. Where story work merges, how, who resolves conflicts, what stops two stories colliding

<!-- Source: Base (original, modified) - Variant 1 Q2, extended per Changes #8, #11, #13, #16, #21, #26 (INV-004, 006, 007, 019, 026, 023) -->

**Where.** Locally, by the coordinator, into `release/dash<rel>`. There is no pull request per story, so by default there is no CI and no automatic review per story. Before a merge, a story has passed its own gates (spec-compliance QA per task, plan review panel), and the coordinator has written the panel verdict into the ledger line. After the merge, the local gate runs (below).

**Authority.** Section 1.5: the coordinator never merges a pull request; a local merge into the line is a smaller class of act that the owner confirms in chat (decision 1).

**Method.** A merge commit (`--no-ff`). One merge commit per story means one `git revert -m 1` can remove the whole story later (Q9), and the story's own commits stay in history. Squash would hide that boundary. Rebase is not allowed once other branches were cut from the line. Squash or merge commit is an open owner choice (decision 4); merge commit is the written default.

**Order for every story** (INV-006). Path-claim check; `git merge-tree` trial (it finds textual clashes only: debate point A-005); merge; local gate; ledger line; push only if the gate is green. A red gate means no push and a reset to the ledger's recorded tip hash (Q9). Story N+1 does not merge until story N's gate result is in the ledger. A story that touches the same shared or risky files as a story whose dispatch run is still open waits for that run (GUESS). `master` has no protection and the repository has no rulesets (VERIFIED-PROBE), so these are rules of the coordinator, not enforcement.

**The local gate is the CI list** (INV-007). Tests after a merge are not the same gate CI applies: CI's `lint` job also runs `ruff check`, `ruff format --check`, `make verify-deps`, `make sync-dev`, `make verify-sync` and `make lint-architecture`, and its `test` job runs `make sync-dev` first because the `.claude/` mirrors are gitignored (VERIFIED-PROBE). At release start the coordinator reads `git show origin/master:.github/workflows/test.yml`, copies the exact commands of both jobs into the first ledger entry (the release brief), and runs them after every story merge. The worker contract lets the coordinator run `make sync-dev` or other Makefile targets only when the user's instruction names the step; the release brief is that instruction, and decision 1 asks the owner to confirm it. Evidence for the gap: 9 of the last 40 `test.yml` pull-request runs failed (22.5 percent), and all 6 failed runs that were opened failed in the lint job (VERIFIED-PROBE). Local run time is unmeasured (trial T9). The gate is always the full local suite, never a targeted subset.

**Conflicts.** The coordinator stops and reports; it never resolves a conflict itself (worker contract). The story's worker resolves it in the story worktree by merging the line tip into the story branch, re-runs its gates, and the coordinator retries the merge. A conflict that comes from two stories that wanted the same behaviour goes to the owner as a decision.

**Prevention.**
1. Each story names the paths it owns at creation. Two stories running at once must be disjoint; the coordinator checks the claim before starting the second one.
2. Disjoint paths are necessary, not sufficient. Shared files belong to exactly one story, or to a first foundation story that merges before the others start (one session at a time for dependency changes). The list: `CHANGELOG.md`, `CLAUDE.md`, `README.md`, `PROJECT_INDEX.json`, `PROJECT_INDEX.md`, docs index files; `pyproject.toml`, `uv.lock`, `scripts/dependency_baseline.txt` (the CI lint job runs `make verify-deps` against them: VERIFIED-PROBE); and every test that pins a count, for example the assertion `len(data["commands"]) == 47` in `tests/recommend/test_routing_refresh.py` (VERIFIED-HERE by grep on 2026-11-23; cite the assertion, not its line, because lines move). The list grows as releases find new files.
3. Identical edits to a pinned count merge cleanly and give a wrong value: in a scratch run two branches each changed `n=47` to `n=48`, the merge exited 0, the file read 48, and the true count is 49 (VERIFIED-PROBE). So a story that adds a counted item (a command, a skill, a registered entry) names the pinned count in its path claim, and two stories that touch the same pinned count are serialised or one owns the count. Detection when ownership fails is the full local suite failing.
4. Merges are serial, and the full local suite after each merge is what catches a semantic collision that merges cleanly.

**Records reach the line.** The worker commits its `.dev/` records on the story branch before it reports done. Before merging, and before `orca worktree rm`, the coordinator checks that `git status --short` in the story worktree is empty. Whether child-report directories reach the branch is UNVERIFIED (trial T2).

**Outside gate (default on, needs the owner's CI-minutes nod: decision 6).** <!-- Source: Variant 2 Q2 goal ("CI on every slice runs against the real integration"), means from Change #11 -->After the forward push of any story merge that touches the shared or risky list above, and always on the final tip, the coordinator dispatches the workflow: `gh workflow run test.yml --repo IronbellyOrg/IronClaude --ref release/dash<rel>`. It reads the result before the next story that touches the same list merges (about 9 minutes against a bad line: GUESS rule). Evidence: `test.yml` has an unconditional `workflow_dispatch` trigger (VERIFIED-PROBE); two dispatch runs on 2026-11-05 on a branch outside the filter list were both green, 4 min 7 s and 5 min 1 s; the median pull-request run is 9.2 minutes, range 7.0 to 12.6, over the last 40 runs, 31 of which succeeded (VERIFIED-PROBE). A dispatch run tests the tip alone and does not run the pull-request-only workflows (Q4).

**Optional layer: a review-only story pull request** (off by default). <!-- Source: Variant 3 Q2 and Round 2 statement of its advocate, merged per Change #16 -->When the owner turns it on for stories above a threshold of about 15 files or 1,000 added lines (ESTIMATE from two data points: pull request #484 had 8 files and +217 lines; #490 had 25 files and +4,636 lines and produced the fix pull request #491 the same day), the story branch is pushed and its worker session runs `/sc:pr-submit --monitor 3 --base release/dash<rel>` for review only. The two bots do review pull requests whose base is not `master` (#484, #490, #491 on the base `346Claude-integration`: VERIFIED-PROBE). The coordinator then merges locally with `--no-ff` after pushing the line, so GitHub should show the PR as merged (UNVERIFIED, trial T6). Costs written into the text: no CI on those pull requests; `/sc:pr-submit` reports CI as clean when no checks exist, so read "clean" as "no checks existed" and never claim CI for a story PR (INV-023); one top-level session per story; after story A merges locally, story B's open PR has a moved base, and pr-submit handles that with one merge commit of the recorded base tip, pushed fast-forward.

### Q3. Keeping the release line current with `master` and `integration`

<!-- Source: Base (original, modified) - Variant 1 Q3, extended per Change #30 (INV-010, INV-012, INV-020, INV-021) -->

- **`master`:** merge `origin/master` into the line (merge commit) at three points: at the start, between story merges whenever `master` has moved (never mid-merge), and right before the release pull request. Never rebase the line after the first story branch was cut from it, and never after it is pushed (`/sc:pr-submit` never rewrites a published branch).
- **The rebase rule, stated once.** The project's pre-pull-request check 2 says to rebase onto `origin/master` before pushing. That fits an unpublished branch. The line becomes a published branch at its first forward push, so for this pull request the check is replaced by a merge of `master`. The standing memory rule already limits rebase to unpublished commits; the owner confirms the exception once (decision 1, part e).
- **How much merge-in work.** 116 pull requests were merged since 2026-11-09, about 8 a day, so a seven-day line can be 50 or more `master` pull requests behind (VERIFIED-PROBE). The merge-in rule covers it, and a conflict stops the coordinator.
- **`integration`:** not merged into the line. Merging it in would make the release pull request carry Clay's unreleased work into `master` (a scratch test showed `git diff --stat master...release/dash1.3` listing the `integration` commit's file). Instead, at release start the coordinator lists the files in open `integration` pull requests and compares them with the stories' path claims, and runs `git merge-tree` against `origin/integration`. These are early warnings, not guards: `master` against `integration` has 0 conflict hunks today, and the collisions that matter arrive through the merge-in of `master`, because Clay's real landing branch is `master` (INV-021; decision 5 asks whether `integration` is still in use).
- **A story worktree** gets later line changes by merging the line into the story branch.
- **A hotfix lands on `master` while the release PR is open.** GitHub runs no `pull_request` checks on a conflicting PR; `/sc:pr-submit` then runs its conflict ladder (one merge commit of the recorded base tip, pushed fast-forward). A fix that clashes in meaning with dashboard code stops the coordinator at the merge-in, and a worker resolves it.

### Q4. How the release lands

<!-- Source: Base (original, modified) - Variant 1 Q4, extended per Changes #5, #6, #11, #14, #23, #25, #26 -->

**One pull request.** `release/dash<rel>` into `master`, opened by `/sc:pr-submit --monitor 3 --base master` in its own top-level session in the line's worktree. CI (`test.yml`), Augment and Codex run once, on the whole release. The owner merges.

**The merge click** (INV-009). All three merge methods are allowed on `master`, nothing technical stops a wrong click, and the last 12 merged pull requests into `master` all landed as single-parent commits, so the owner's normal click is the wrong one for a release (VERIFIED-PROBE). Precedent: pull request #658 was squashed by mistake, reverted by #662, and redone as #664. Controls: the first line of the release PR body and of the sync PR body is "Merge this pull request with a merge commit, not squash." A closeout check reads `mergeCommit` from `gh pr view <n> --repo IronbellyOrg/IronClaude --json mergeCommit`, then `git cat-file -p <sha>` must show two `parent` lines. The check is detective only, it is new work that does not exist yet (the closeout script `branch-landed.sh` asserts no merge method), and it is filed as a follow-up outside this proposal. If the wrong method was used: a revert PR through pr-submit, then redo (the #658, #662, #664 path). No repository setting change is proposed (decision 8).

**Release size.** The reviewers see everything at once. That is the pattern DORA warns about ("regrouping the batches before sending them downstream", S6) and that Faros links to slower reviews and more bugs per PR (S19, vendor data). Size evidence, with no weight as precedent:

| Pull request | Size | Outcome |
|--------------|------|---------|
| GFxAI #147 (the owner's organisation repository) | 34 commits, 1,384 files, +242,976 lines | Merged "with file-level rejections" |
| In-repo #640 | 1,146 files | Merged in 43 minutes, with one Augment review and one Codex comment |
| In-repo #664 and #658 | 181 files each | Merged in 27 and 17 minutes |
| In-repo #31 | 2,089 files | 0 reviews, 0 comments |

A fast merge shows nothing broke, not that anyone read the diff. Because no human approves plans (section 1.4), the release PR is the first place a human reads the result, so the control matters more, not less. The controls are the file budget of section 8 (counted over all paths, `.dev/` included), a per-story digest in the PR body (the ledger lines plus `git log --merges`), and the time box below.

**Time box.** A release closes at six merged stories or seven days from the cut, whichever comes first (both ESTIMATE; the owner sets them: decision 2). The seven days extrapolate DORA's one-week batch limit (S6); this is not a DORA figure for release branches. A story not merged by then is not in this release. It stays in the ledger as "carried", keeps its branch and worktree, merges the new line tip into itself when the next release starts (merge, never rebase), and keeps its old `dash<rel>-` name. The ledger records the move.

**The gate list for the final tip, in order.**
1. Freeze (section 3.2 step 5).
2. `master` merged in, right before the PR (a PR run tests the merge of the head with the current `master`, and `master` moves about 8 pull requests a day: VERIFIED-PROBE).
3. The local gate green.
4. A green dispatch run of `test.yml` on the final tip. This is necessary, not sufficient: `boundary-guard.yml` and `contract3-generator-constraint-lint.yml` have only a `pull_request` trigger, so a dispatch run cannot show them green, and it tests the tip alone (INV-026). The dispatch step needs the owner's CI-minutes nod (decision 6).
5. `/sc:pr-submit --monitor 3 --base master`, then the pull-request run and both bots settle. The PR run is the real gate: the owner merges only when `test.yml`, `boundary-guard` and the Contract #3 check are green and both bots have settled. Each pr-submit fix push starts a new PR run (pr-submit allows `max_rounds + 1` pushes, default 2, hard cap 5), so the final state is read after the last push.
6. The owner merges with a merge commit.

Not carried over from the GFxAI approach: its three test tiers, UAT sign-off and two approvers, which have no counterpart in this repository.

**Contract #3 heading** (INV-008). The brief lists the pull-request-only workflows read from `origin/master` at release start (`test.yml`, `boundary-guard.yml`, `contract3-generator-constraint-lint.yml`). Before opening the PR the coordinator runs `git diff --name-only origin/master...release/dash<rel>`; if it matches `**/gates.py`, `**/structural_checkers.py` or `**/*_validator.py`, the PR body gets the heading `## Generator-Constraint Considered` (the workflow also re-runs when the body is edited).

**The monitor window** (INV-005). From the start of `/sc:pr-submit --monitor 3` until it reports its final state, the line's worktree has one writer, pr-submit. The coordinator does no merge, commit, push or branch switch there. A `-fix` waits (ledger: "queued") and enters after the monitor ends; it then starts a new pr-submit run on the new head, because a hand push gets CI but no bot re-review (only pr-submit posts the re-trigger comments). Before starting, `git status` in the worktree is clean with no merge or revert open, or pr-submit halts with `foreign_op_in_progress`. A head that moved halts it with `pr_head_mismatch` (both VERIFIED-PROBE from the command's own text; trial T3).

**While the PR waits for the owner** (INV-003). One release line is open at a time. The coordinator does only: monitor and `-fix` handling, sync-branch preparation, clean-up preparation. No line for release n+1 is cut and planning of n+1 starts only after n merges. The ledger records the PR-opened and PR-merged times for the first two releases (trial T11). If the wait exceeds one working day (GUESS) in both, the owner decides whether n+1 may be cut from n's tip. That is mechanically cheap, because n lands by merge commit: in a scratch test (VERIFIED-HERE), n+1 was cut from n's tip, n was landed with a merge commit and `master` merged in, and `git diff --name-only master...n+1` listed only n+1's own file.

**Too large to land.** Section 8 says what the coordinator does when the count passes 250 or 300 files.

### Q5. Flags, trunk-based alternatives, and whether a long-lived line is justified

<!-- Source: Base (original, modified) - Variant 1 Q5; time-box justification from Variant 3 Q5 per Change #14; ladder per Changes #12 and #15 (Variant 2 steps 1 and Q5, Variant 3 Q5) -->

- **Flags are not used in the design.** The point of the line is that `master` never carries half a release.
- **Justification of the long-lived line: the scope floats, the time does not.** A release closes at the time box of Q4; stories not merged ride the next release. That removes the need for flags: unfinished work is "not in this release", not "in but hidden". Dashboard releases are a deliberate set of stories that should reach `master` together, the coordinator owns merge order, and only two stories run at once, so the line moves slowly. Driessen's own 2020 note says release branches fit software released as explicit versions (S3), and Fowler says to use a release branch when a releasable mainline cannot be kept at the team's integration frequency (S8). Mozilla and Chrome ship on a schedule and go without unready features (S22).
- **The counter-evidence is real.** Trunk-based sources say branches should live about two days (S1), continuous-delivery teams "do not do release branches" (S2), and DORA says small batches are the countermeasure to AI-driven instability (S6). This design holds only if lines stay days, not weeks; that is what the time box and the file budget are for.
- **Fallback ladder** (move down one rung at a time):
  - Rung 0: the line alone.
  - Rung 1: optional review-only story pull requests for stories above the size threshold (Q2).
  - Rung 2: a review-only pull request for every story, if the time box is missed twice.
  - Rung 3 (not the default): after a pilot on one story, a story that cannot finish inside the time box is sliced into pieces that each land alone (new files nothing imports yet, or behind a flag) as direct pull requests into `master`. Every flag gets a retirement line in the ledger at creation.
- **A line with zero merged stories at the time box** (INV-015): no PR is opened; the line and its worktree are deleted (Q7); the release number is reused at the next cut; the ledger notes "closed empty". The pre-PR failure "No commits between master and branch" is the signal.

### Q6. Hotfixes and bug fixes during a release

<!-- Source: Base (original, modified) - Variant 1 Q6; freeze from Variant 4 rule 6 per Change #2; one-story release per Change #20; special releases per Change #27 -->

1. **A bug in code already shipped on `master`:** branch `fix/<issue>-<slug>` from `master`, pull request into `master` through pr-submit. The open line picks it up at the next merge-in of `master`. No cherry-pick and no back-port step is needed, because the line merges back into `master` (the cherry-pick-only-from-trunk rule is for maintenance branches that never merge back; debate point C-015, unanimous, 93 percent).
2. **A bug in a story already merged into the line:** `dash<rel>-fix<NN>-<slug>` from the line tip, merged locally like a story.
3. **Freeze.** Freeze starts when the ledger shows the last planned story merged, or when the time box ends. From freeze until the owner merges, only `dash<rel>-fix<NN>-<slug>` branches enter the line; no new story. While `/sc:pr-submit --monitor 3` runs, nothing enters at all (Q4).
4. **Every dashboard release number is an ordinary release,** including 1.1 (bug-fix) and 1.105 (test-only): line `release/dash1.1` or `release/dash1.105`, story branches `dash1.1-s01-<slug>`, ledger on the line, one pull request into `master`, merge commit, tag `dash-1.1`. One rule set keeps the ledger convention, which needs a branch to hold the ledger.
5. **A release with exactly one story has no line.** The one story is `dash<rel>-s01-<slug>`, cut from `master`, with the ledger and `.dev/` records on it, one PR into `master` by `/sc:pr-submit --monitor 3 --base master`, merge commit, tag `dash-<rel>`. The plain `fix/<issue>-<slug>` branch stays for shipped-code fixes that belong to no dashboard release.
6. **Name hazard:** `dash1.1` is a prefix of `dash1.105` (section 2.2, rule 3).
7. **Left to the owner (decision 7):** whether a test-only release of several stories (1.105) may skip the line. Recommended: no.

### Q7. Clean-up and what is kept

<!-- Source: Base (original, modified) - Variant 1 Q7; explicit remote deletion and sweep from Variant 4 rule 7 per Change #4; records rule per Change #25; tag per Change #3; INV-001, INV-004, INV-014 per Change #30 -->

- **Story branch and worktree:** deleted as soon as the coordinator records the merge in the ledger and the story's `git status --short` was empty. The story tip stays reachable as the second parent of its merge commit, and that merge commit reaches `master` in the release merge, so no tag is needed and a premature delete loses nothing.
- **Release line, records branch, sync branch and their worktrees:** after the owner merges the release PR and the sync PR is open, delete `release/dash<rel>`, `dash<rel>-records` and the worktrees, local and remote (`git push origin --delete <name>`). The sync branch goes after its own PR merges. Branch deletion is part of the authority the owner confirms in chat (decision 1).
- **Why explicit deletion is mandatory:** `delete_branch_on_merge` is false and 170 remote branches exist today (VERIFIED-PROBE). GFxAI shows the cost of having no rule: 6 `backup/...` branches and a stale `release/v0.1` (0 commits ahead, 62 behind `master`).
- **Closeout sweep** (one command, after the sync PR is merged and its branch deleted): `git ls-remote --heads origin 'refs/heads/release/dash<rel>*' 'refs/heads/dash<rel>-*'` must print nothing (hyphen-terminated globs, section 2.2). The script `scripts/worktree_cleanup.py` removes a worktree only when its own pull request is merged and about six other conditions hold, and fails closed, so an unmerged release worktree is safe and a worktree with no PR is not touched; story worktrees are removed by hand with `orca worktree rm` (read through a debater, not re-read here).
- **Kept:** the tag `dash-<rel>`; the ledger lines; the story merge commits; and the `.dev/` records, by this rule. The ledger (`sprint-status.yaml`) and the planning set stay on the line and land with it, never moved out. Every other `.dev/` record (story report folders, panel outputs, QA files) is committed on the story branch, reaches the line at the story merge, and may leave the release PR through a records PR (section 8).
- **The ledger path** is one fixed file. At every line cut the coordinator replaces its contents with the new release's header; the previous ledger stays in `master` history and under its tag. The first landing creates the file on `master` (it is absent there today: VERIFIED-PROBE).

### Q8. Fit with `integration` and Clay's habit

<!-- Source: Base (original, modified) - Variant 1 Q8; sync branch from Variant 3 sec 2 per Change #19; price sentence from Variant 4 rule 4 per Change #9 -->

Clay keeps branching from `integration` and opening pull requests into it. Nothing changes for Clay while a release is built. Clay's unreleased work never enters the line.

After the release lands on `master`, the coordinator brings `master` back into `integration` by a sync pull request:

1. Cut `dash<rel>-sync<N>` from `origin/integration`, merge `master` in with a merge commit, push.
2. In its own top-level session, run `/sc:pr-submit --monitor 3 --base integration`.
3. The PR body says "Merge this pull request with a merge commit, not squash." A squash would break the shared history.
4. A conflict stops the coordinator; a worker resolves it on this branch.

The head is a separate branch because the owner rule is no commit on `master`, and because a conflict between `master` and Clay's `integration` work needs somewhere to be resolved and committed. Whether pr-submit would accept `master` itself as a head is UNVERIFIED and no longer needed.

`integration` does not contain the release until the sync pull request lands. That is the price of landing on `master` instead of through `integration`. Who runs this sync today is UNVERIFIED (a debater counted five manual sync commits by Clay between 2026-11-17 and 2026-11-19; not re-run). Decision 5 asks the owner to assign it and to say whether `integration` is still in use. The cost: if Clay's open work touches dashboard files, the collision shows up in the sync PR, late.

### Q9. Failure and rollback

<!-- Source: Base (original, modified) - Variant 1 Q9; "revert the revert first" per Change #22; first-parent bisect per Change #24; red-gate reset per Change #21 -->

- **A story fails the gate right after its merge, before the push:** do not push; reset the unpublished merge to the tip hash the ledger recorded before it (local and unpublished, so allowed), and send the story back to its worker. A slower alternative with no data loss is `git revert -m 1` on the unpublished merge.
- **A story goes bad after it merged into the line:** `git revert -m 1 <story merge commit>` on the line (a new commit; published history is never rewritten), or fix forward with a `-fix` branch. If later stories depend on it, revert them in reverse order or fix forward.
- **A release fails on `master`:** revert the release merge commit through a revert pull request opened by `/sc:pr-submit`; this removes all stories at once. Single stories can still be backed out of a landed release, because their merge commits are preserved. Prefer a bug-fix release (fix stories on a new line cut from `master`) over a re-merge.
- **Bringing back a story or a release that was reverted:** first revert the revert commit, then merge the fixed branch. Never merge the old branch directly. A scratch run in the debate showed why: a direct re-merge after `git revert -m 1` stops with a conflict (`DU s.txt`), while reverting the revert first and then merging the fixed branch is clean (VERIFIED-PROBE).
- **Finding the story that broke something:** `git bisect start --first-parent` on the line or on `master` names the story merge that introduced a regression. In a scratch repository it named the bad one ("merge s4") over six story merges, and the first-parent log had 7 entries against 26 (VERIFIED-PROBE); git 2.47.3 here accepts the option (VERIFIED-HERE).
- **A wrong merge click:** see Q4 (revert pull request, then redo).

## 5. What it costs

<!-- Source: Base (original, modified) - Variant 1 sec 5, updated per Changes #11, #16, #21, #23, #25 -->

- **No CI and no automatic review per story, by default.** CI comes from dispatch runs (about 9 minutes each, ESTIMATE from the 40-run median, and they need the owner's nod: decision 6) and from the release PR at the end. The two bots see the release PR only, unless the optional review-only layer is on. Semantic breakage between stories can sit for the length of the release; the local gate that copies CI, the full suite after every merge and the time box limit how long.
- **One large review at the end** (Augment, Codex and the owner). The size is bounded by the file budget of section 8, not removed. Whether a pull request under 250 files is read well is unproven (trial T10).
- **Extra owner clicks.** One for the release PR, plus a sync PR, a records PR when the count passes 250, a revert PR when something is reverted, and a second click when a release is landed in two PRs. About three to four pr-submit sessions per release. The peak so far was 26 and 23 merged pull requests a day (2026-11-17 and 2026-11-18), so the base case of one release PR plus one sync PR per release sits inside it (VERIFIED-PROBE).
- **The coordinator is a single lane:** serial merges, serial conflict handling.
- **A long-lived line drifts from `master`** and needs merge-in housekeeping (about 8 `master` pull requests a day).
- **Local-only merges are invisible on GitHub.** The forward push shows the commits but not a pull request, so the ledger is the only record of who merged what and when.
- **The late sync:** `integration` lacks the release until the sync PR lands (Q8).
- **A control that does not exist yet:** the two-parent closeout check (Q4) is new work, filed outside this proposal.
- **The optional review-only layer** costs a top-level session per story, gives bots without CI, and reads "clean" when no checks existed (Q2).

## 6. Who does what, and who it favours

<!-- Source: Base (original, modified) - Variant 1 sec 6 "Who it favours"; role table added for the owner's reading from the rules of sections 1.5, 3 and 4 (no new rule) -->

### 6.1 Who does what

| Role | Does | Decides or confirms | Never does |
|------|------|---------------------|------------|
| Coordinator (one AI session per release) | Cuts the line and creates every worktree; reads back and records real branch names; writes the release brief; checks path claims; runs `git merge-tree`; merges settled stories with `--no-ff`; runs the local gate; writes the ledger; pushes the line forward; dispatches `test.yml` runs; merges `master` into the line; counts files; cuts the records branch and the sync branch; has a top-level session run `/sc:pr-submit --monitor 3` for each PR; tags; deletes branches and worktrees; runs the sweep. | The merge of each story, by the panel verdicts, disjoint claims, clean `merge-tree` and green gate. Predicts and writes the file count before each merge. | Merge a pull request. Merge into `master` or `integration`. Force-push or rebase a published branch. Resolve a conflict itself. Write in the line's worktree while the monitor runs. Open a pull request any way except `/sc:pr-submit --monitor 3`. Touch `SuperClaude-Org`. |
| Workers (one AI session per story) | Build the story through the pipeline in the story worktree; commit the story's `.dev/` records on the story branch; resolve conflicts by merging the line tip into the story branch; resolve a sync conflict on the sync branch; build a `-fix` branch; run a review-only pr-submit for their own story when that layer is on. | Nothing outside their story. | Merge into the line. Write the ledger. |
| Owner | Reads and merges the release PR (merge commit), the records PR, the sync PR and any revert PR. | The eight decisions of section 10; the numbers; local-merge authority; whether a carried story is the release's reason for being; whether release n+1 may be cut from n's tip after a slow wait; whether to accept the tooling fallback above 300 files. | Review a story before the release PR (no human plan approval; the bots and the size budget stand in). |
| Clay | Keeps branching from `integration` and opening pull requests into it. His merged work reaches the line only through the merge-in of `master`. | Nothing in this proposal. Whether he still works from `integration` is the owner's answer to decision 5. | Is asked nothing while a release is built. |

### 6.2 Who it favours

The owner and the coordinator: full control over order and content, one merge decision per release, the existing ledger and worker contract unchanged, and no change to CI or repository settings for the design itself (the dispatch runs and the optional layer need the owner's nod). It is neutral to Clay and slightly bad for him at sync time.

## 7. Risks

<!-- Source: Base (original, modified) - Variant 1 sec 7; risk 1 now bounded by a number per Change #25; base risk 5 (revert then re-merge) removed and its procedure moved to Q9 per Change #22; new rows from Changes #16, #23, #25, #26, #28 -->

1. **Big-batch review.** The strongest evidence in the research (S6, S19) points against batches. The file budget (section 8) bounds the release PR by a number, but a budget is a ceiling set by what the tools can read, not a promise of review quality (INV-025; trial T10).
2. **Hidden semantic collisions.** The local gate, which copies CI, is the main guard of the line. Local run time is unmeasured (trial T9), and identical edits to a pinned count merge cleanly into a wrong value (Q2).
3. **The line lives too long.** AI stories are fast and human review of the final PR is not. The time box and the owner-wait rule (Q4) are the answer; owner latency is unmeasured (trial T11).
4. **Orca behaviour is checked at help-text level only.** `--branch` keeping the exact name and `worker-start` adopting a coordinator-made worktree are UNVERIFIED (trials T1, T2). Names stay valid either way, because they are flat.
5. **No early look at a story** unless the optional review-only layer is on; that layer has two UNVERIFIED behaviours (trial T6).
6. **Records PR and two-PR landing** are new designs with no precedent in any proposal. The git side was checked in a scratch repository; the GitHub side and the bots' behaviour were not (trials T4, T7). Each costs an extra owner click.
7. **The merge-method control is a sentence plus a check that does not exist yet** (Q4). A wrong click is still possible; the recovery is a revert PR and a redo.
8. **Review tools stop above 300 files.** `gh pr diff` fails and `gh pr view --json files` shows only 100 (section 8). Whether pr-submit survives a release PR above 300 files is UNVERIFIED (trial T4).
9. **Nothing enforces the rules.** `master` and `integration` are unprotected; every rule is the coordinator's discipline (section 1.3).

## 8. Size budget and records rule

<!-- Source: New section, no variant (merge-plan Change #25); answers invariant INV-017 (HIGH) and INV-011, INV-025. Numbers carry the Variant 2 and Variant 3 estimates (about six stories, about seven days) as modified or preserved by the plan's Threshold preservation table -->

### 8.1 Why this section exists

A release pull request that is too large cannot be read by the tools in the loop. On the 2,089-file pull request #31, `gh pr diff` fails with "HTTP 406: the diff exceeded the maximum number of files (300)", `gh pr view --json files` returns only 100 files, and `gh api repos/.../pulls/31/files` pages work (page 21 returned 89 files) (VERIFIED-PROBE). The `/sc:auggie-review` skill, whose rubric `/sc:pr-submit` reuses, calls `gh pr view --json files` and `gh pr diff`. Record-only pull requests already sit at the limit: #728 changes 453 files and #730 changes 292 files (VERIFIED-PROBE). So `.dev/` records alone can pass 300 files, while a cap that counts stories would not notice.

Because no human approves plans (section 1.4) and the panels and per-task QA are AI reviewers, the release PR is the first place a human reads the result. This control therefore carries more weight, not less.

### 8.2 The numbers

Every number is a default the owner may change (decision 2), except the three tool limits, which belong to GitHub.

| Number | Default | Basis | Mark |
|--------|---------|-------|------|
| `gh pr diff` file limit | 300 files | #31: HTTP 406 above 300 | VERIFIED-PROBE; fixed by the tool |
| `gh pr view --json files` | first 100 files only | #31 returned 100 | VERIFIED-PROBE; fixed by the tool |
| `gh api .../pulls/<n>/files` | 100 per page, at most 3,000 files per PR | GitHub REST documentation fetched 2026-11-23 ("Responses include a maximum of 3000 files"; "max 100" per page); paging worked on #31 | VERIFIED-HERE (documentation), VERIFIED-PROBE (paging) |
| Release-PR file budget | 250 files, counted over all paths including `.dev/` | 50 files of headroom under the 300 limit | GUESS (the 300 it sits under is verified) |
| Stop-adding threshold | 200 files (80 percent of the budget) | headroom for the story in flight | GUESS |
| Story cap | 6 stories | median `master` PR is 37 files, p90 is 334 (155 PRs into `master`, 130 of them the owner's, none through `integration`); 6 x 37 = 222 fits 250, but one p90 story alone does not | ESTIMATE; the file budget, not the story cap, is the binding control |
| Time box | 7 days from the cut | DORA one-week batch limit (S6) extrapolated; not a DORA figure for release branches | ESTIMATE |
| Review-only story PR threshold | about 15 files or 1,000 added lines | #484 (8 files, +217) against #490 (25 files, +4,636, needed fix PR #491) | ESTIMATE from two points |
| Hard stop | 300 files | the `gh pr diff` limit | VERIFIED-PROBE |

<!-- Source: Variant 2 (Round 2 statement), "roughly 300 files, without .dev/ records" - Disposition: modified, Decision basis: the PR diff counts .dev/ (INV-011) and 300 is the gh pr diff limit; replaced by the 250 budget, 300 kept as the hard stop, per Change #25 -->

What the budget does not prove: that a PR under 250 files is read well. The in-repo evidence for "reviewable" is merge speed (#640: 1,146 files, 43 minutes, one Augment review and one Codex comment), which is not review depth (trial T10). The budget is set by what the tools can read.

### 8.3 Where `.dev/` records go

1. The ledger (`sprint-status.yaml`) and the planning set stay on the release line and land with it. They are never moved out.
2. Every other `.dev/` record (story report folders, panel outputs, QA files) is committed on the story branch, reaches the line at the story merge, and may leave the release PR through a records PR (below).
3. At freeze the coordinator counts: `git diff --name-only origin/master...release/dash<rel> | wc -l`, and the part under `.dev/`. If the total is 250 or less, there is no records PR: the release PR carries everything. If it is more than 250, the records PR goes first.
4. **Records PR mechanics.** The coordinator creates `dash<rel>-records` from `origin/master` (`orca worktree create --name dash<rel>-records --branch dash<rel>-records --base-branch origin/master --agent claude`), runs `git checkout release/dash<rel> -- <record paths>` for every `.dev/` path except the ledger and the planning set, commits, and a top-level session runs `/sc:pr-submit --monitor 3 --base master`. The owner merges it (any merge method; it is record-only: precedent #728 and #730). Then the coordinator merges `master` into the line and recounts.
5. **The mechanism was checked** in a scratch repository (VERIFIED-HERE): a line with 400 record files, one code file and a ledger file; after a records branch carrying the 400 files was merged into `master` and `master` was merged into the line, `git diff --name-only master...line` listed 2 files (the code file and the ledger), 0 of them under the records path. The merge was clean, because the files were identical on both sides.
6. **An edge found in the same scratch work** (VERIFIED-HERE): if a record file already carried by the records PR is edited again on the line afterwards, the merge of `master` into the line conflicts in that file. Rule: from the moment the records branch is cut until `master` has been merged back in, the coordinator does not edit those record paths on the line; a late record goes into a new file (or into the ledger). Late new files ride the release PR.
7. **Expected frequency:** most feature releases will trigger it (one record set was 453 files, #728; ESTIMATE). If the rule triggers three releases in a row, the owner may make the records PR the default for feature releases.
8. **Cost:** one more PR through pr-submit, one more owner click, one more CI run (CI runs for PRs into `master`), and an ordering dependency (records merge before the release PR). The records PR can itself exceed 300 files (#728 had 453): the tooling fallback below applies, and the owner reviews it by path class.

### 8.4 Review-tooling fallback

This is a rule for the release brief. The `/sc:auggie-review` skill and pr-submit's own reads of a PR are not changed by this proposal. Whether pr-submit survives a release PR above 300 files is UNVERIFIED (trial T4). A follow-up issue, outside this proposal, is to make the `/sc:auggie-review` rubric page the file list.

| Need | Do not use above the limit | Use |
|------|---------------------------|-----|
| Count the files | `gh pr view --json files` (first 100 only) | `git diff --name-only origin/master...<head> \| wc -l` locally, or `gh pr view <n> --repo IronbellyOrg/IronClaude --json changedFiles` |
| List the files | `gh pr view --json files` | `gh api repos/IronbellyOrg/IronClaude/pulls/<n>/files --paginate` (100 per page, 3,000 files at most) |
| Read the diff | `gh pr diff <n>` (fails above 300 files) | local `git diff origin/master...<head>`, or the `patch` field of the paged API |
| Tell a human what is in it | a file list | path classes and the per-story digest in the PR body (ledger lines plus `git log --merges`) |

### 8.5 What the coordinator does when a release would exceed the budget

Before every story merge the coordinator predicts the count with `git diff --name-only release/dash<rel>...<story> | wc -l` added to the line's current count, and writes both to the ledger line. Then:

| State | Action |
|-------|--------|
| Predicted total 200 or less | Merge as usual. |
| 201 to 250 | Merge; no new story starts; stories in flight finish (scope floats, Q4). |
| Above 250, records not yet split out | Apply 8.3 first (a records PR may be cut early, before freeze), recount. |
| Still above 250 and this story is not yet merged | The story does not merge. Default: it is carried to the next release (Q4). If it is the release's reason for being, the coordinator asks the owner in chat; the other choice is a planning change that splits the story into two. |
| Still above 250 and everything is merged (one story or late records pushed it over) | Land the release in two PRs. Pick a story-merge commit M_k from the ledger (every merge commit passed the local gate, so each is a green state). `git branch release/dash<rel>-p1 <M_k>`, push it, open PR 1 `release/dash<rel>-p1` into `master` through pr-submit, the owner merges it (merge commit). Merge `master` into the line. Open PR 2 `release/dash<rel>` into `master`; it carries only the stories after M_k. Tag `dash-<rel>` after PR 2 only. |
| Above 300 and no split is possible | Open no PR. The coordinator stops and asks the owner in chat; the owner may accept the tooling fallback in chat. |

The two-PR landing costs a second owner click, CI and both bots twice, and leaves half a release on `master` between PR 1 and PR 2. The coordinator picks M_k at a story group that is usable alone, and the owner may refuse the split. The split rests on git behaviour (any merge commit of the line is a valid head) and on each M_k having passed the gate; the GitHub side is UNVERIFIED (trial T7).

## 9. Trials before first reliance

<!-- Source: Variant 3, risk 5 ("check by opening one test pull request first") and unique contribution U-013, merged per Change #18; table and commands per the plan's "Trials before first reliance" -->

Every behaviour in this proposal that is marked UNVERIFIED points to one row below. Each trial is throwaway and runs on a disposable target: a worktree, branch or pull request named `dash0-trial-...` or `release/dash0-trial`, cut from `master`, never `master` itself, and removed afterwards. Trial pull requests go through `/sc:pr-submit --monitor 3 --base <throwaway base branch cut from master>` and are closed unmerged, except the pull requests of T7, which the owner merges into the throwaway base only. Writing this proposal made no project, git or GitHub write. The trials are for the coordinator, after the owner's go; anything that pushes a throwaway branch or opens a trial pull request is a GitHub write and waits for that go.

The effort figures in the first column are GUESS, except CI minutes, which are ESTIMATE from the 40-run median of 9.2 minutes. The rows are ordered by the effort to run them, cheapest first. T10 and T11 cost nothing extra but can only run inside real releases, so they close the table. T1, T2, T3, T5 and T9 must pass before release 1. T4 and T7 run before the first release whose file count may pass 250. T6 runs before the optional layer is first used. T8 rides on T1. T12 runs only if the third rung of Q5 is considered.

| ID, effort, when | What it settles | Exact command or check | Disposable target | Passes when | Fails: what it means |
|------------------|-----------------|------------------------|-------------------|-------------|----------------------|
| **T1** about 5 minutes, local only. Before release 1. | Whether `--branch` keeps an exact, unprefixed name; whether flat names stay the default; debate points A-007, A-011; INV-022. | `orca worktree create --name dash0-trial-s01-x --branch dash0-trial-s01-x --base-branch origin/master --agent claude`, then `git -C <worktree path from orca worktree list> branch --show-current`. Repeat with a name equal to an existing ref (the same command again). Repeat with a name that would make a ref conflict (create `--branch dash0-trial`, then `--branch dash0-trial/s01`). | Worktrees named `dash0-trial-*`, removed with `orca worktree rm --worktree name:<name>`; then `git branch --list '*dash0-trial*'` must print nothing (remove leftovers with `git branch -D <name>`; nothing is pushed). | The branch name is exact and unprefixed. A taken or conflicting name fails loudly, or gets a suffix that is visible. | The name is changed silently or prefixed. Then the read-back rule (section 2.2, rule 5) is what protects the design, the `*dash1.3-*` listing and any CI branch pattern must be written against the real name, and folder names stay unsafe. Flat names remain the default. |
| **T8** about 5 minutes, local only (low priority). With T1. | How Orca, pr-submit and the closeout listing treat a tag next to similar branch names. The git side is VERIFIED-HERE. | In the T1 targets also create `orca worktree create --name dash0-trial-release --branch release/dash0-trial --base-branch origin/master --agent claude`. Then `git tag dash-0-trial` (local, never pushed), `git tag --list 'dash-*'`, `git branch --list '*dash0-trial*'`, `orca worktree list`, and the read-only listing step of `/sc:closeout`. | The T1 worktrees plus the local tag; remove with `git tag -d dash-0-trial`. | No tool errors. | A tool errors or confuses tag and branch. The tag name is changed (still never a branch name) and the rule in section 2.2 stays. |
| **T2** about 10 minutes, local only. Before release 1. | Whether `worker-start` adopts a coordinator-made exact-name worktree (INV-022); whether a worker's `.dev/` records reach the story branch (INV-004). | The coordinator creates the worktree as in T1, then `worker-start --worktree path:<that worktree>`. The worker commits one `.dev/trial/T2-record.md`. Check `git -C <worktree> status --short` is empty and `git -C <worktree> log -1 --stat` shows the record. | The T1 story worktree. | The adopted worktree keeps the exact branch, and the record is committed before the coordinator merges and removes the worktree. | Adoption makes a new or prefixed branch, or the record stays uncommitted. This proposal has no second way to start a worker on an exact name, so the release does not start until the owner decides the story-start procedure. |
| **T12** about 5 minutes, read-only. Only if the third rung of Q5 is considered. | Whether stacked pull requests and a merge queue are available on this repository's plan. The design uses neither. | No command. Read the repository's settings page for rules and merge queue, and the GitHub documentation on stacked pull requests and merge queue plan requirements. Record the answer in the ledger. | None (read-only). | An answer is recorded. | An unclear answer means rung 3 stays out of reach until it is clear. Nothing else depends on it. |
| **T9** about 10 to 20 minutes locally (the CI median is 9.2 minutes; local time is unmeasured). Before release 1. | Whether the local gate equals the CI list and how long it takes (INV-007; debate point A-010). | In a disposable worktree cut from `origin/master`, copy the exact commands of the `lint` and `test` jobs from `git show origin/master:.github/workflows/test.yml` (the probe lists `ruff check`, `ruff format --check`, `make verify-deps`, `make sync-dev`, `make verify-sync`, `make lint-architecture` for lint; `make sync-dev` first for test). Run each with `time`, through `uv run` where a Python command is involved. Compare with the CI median of 9.2 minutes. | A worktree `dash0-trial-gate` from `origin/master`, removed afterwards. | Duration known, and no step in the file is missing from the brief's list. | A command fails on a clean `master`: the list or the worktree setup is wrong, so the release brief is fixed before release 1. A run far above the CI median: the coordinator reports the minutes to the owner; no rule here sets a limit. |
| **T5** about 5 to 10 minutes of CI. Before release 1. Needs the owner's nod on CI minutes (decision 6). | The default outside gate (Q2); INV-026. | Push `origin/master` as `release/dash0-trial` (`git push origin origin/master:refs/heads/release/dash0-trial`), then `gh workflow run test.yml --repo IronbellyOrg/IronClaude --ref release/dash0-trial`, `gh run list --repo IronbellyOrg/IronClaude --workflow test.yml --branch release/dash0-trial --limit 1`, and `gh run watch <id> --repo IronbellyOrg/IronClaude`. Record the duration. Confirm that no run of `boundary-guard` or `contract3-generator-constraint-lint` started for that ref. | The pushed branch `release/dash0-trial`, deleted with `git push origin --delete release/dash0-trial`. | The run starts and finishes, the duration is recorded, and the pull-request-only workflows are absent. | The dispatch is refused or behaves differently from the runs of 2026-11-05. The outside gate is dropped; only the local gate and the PR run remain, and the INV-026 text stays. |
| **T3** about 15 minutes plus one CI run. Before release 1. | How pr-submit and the bots behave on a release-shaped PR: head fixed during the run, `foreign_op_in_progress`, `pr_head_mismatch`, draft guard (INV-005; debate item M10). | Push a throwaway base (`git push origin origin/master:refs/heads/dash0-trial-base`) and cut a throwaway head with one small commit. (1) Start with a merge left open (`git merge --no-commit --no-ff <other throwaway branch>`): expect a halt `foreign_op_in_progress`; then `git merge --abort`. (2) Start clean, and during the run push one hand commit: expect `pr_head_mismatch`. (3) A clean run: watch CI and both bots, and whether the PR is treated as a draft. Command: `/sc:pr-submit --monitor 3 --base dash0-trial-base --head <throwaway head> --title "TRIAL T3, close unmerged" --body "Throwaway trial. Do not merge."` | The throwaway base and head; close with `gh pr close <n> --repo IronbellyOrg/IronClaude --delete-branch`, then `git push origin --delete dash0-trial-base`. | The two halts appear as the command's text says; the clean run completes with CI and both bots; a `-fix` pushed after the monitor ends needs a new run to get a bot re-review. | A halt does not appear: the monitor-window rule (Q4) is the only protection and is a discipline, not a guard. Bots or CI behave differently: record it and change the gate list of Q4. |
| **T6** about 30 minutes plus bot time. Before the optional layer is first used. | The optional review-only story PR (Q2; debate point A-012 on this base; INV-023). | On the throwaway line `release/dash0-trial`, cut a story branch with a small change and run `/sc:pr-submit --monitor 3 --base release/dash0-trial` in its worktree. Then in the line's worktree: `git merge --no-ff <story branch>`, `git push origin release/dash0-trial`, and `gh pr view <n> --repo IronbellyOrg/IronClaude --json state,mergedAt`. Read the pr-submit report's CI line. | The throwaway line and story branch; close with `gh pr close` if still open, delete both branches. | Both bots review. The PR shows MERGED after the push. The CI line reads "clean" with no checks existing (the INV-023 caveat, now observed). | The PR stays open after the push, or a bot does not review: the optional layer comes out of Q2 and stories rely on the local gate. |
| **T7** about 1 hour, two pull requests plus CI. Before the first release whose count may pass 250. | The GitHub side of section 8: the records PR, the file counts, the two-PR landing (INV-017). | Throwaway line `release/dash0-trial` with 301 generated record files (`mkdir -p .dev/trial-records && for i in $(seq 1 301); do echo $i > .dev/trial-records/r$i.txt; done`), one code file and a ledger file. Open the records PR `dash0-trial-records` into `dash0-trial-base` through pr-submit; the owner merges it into the base; merge the base into the line; read `gh pr view <n> --repo IronbellyOrg/IronClaude --json changedFiles` of the release PR. Then the two-PR landing: `git branch release/dash0-trial-p1 <M_k>`, push, PR 1 into the base, merge, merge the base into the line, PR 2. | The throwaway base, line, records branch and `-p1` branch, all deleted afterwards. | The counts fall as the scratch test showed (the code file and the ledger only), and both PRs of the split open and merge. | GitHub counts the records still, or PR 2 shows conflicts with PR 1. The records PR and the two-PR landing come out of section 8, and a release that passes 300 files goes to the owner in chat (the last row of 8.5). |
| **T4** about 1 hour plus bot time. Before the first release whose count may pass 250. | The review tooling above 300 files: what `gh` shows and what pr-submit and the bots do (INV-017). | On a throwaway head under the throwaway base, create 320 files (`mkdir -p .dev/trial-300 && for i in $(seq 1 320); do echo $i > .dev/trial-300/f$i.txt; done`), commit, push, and open the PR through pr-submit. Then `gh pr diff <n> --repo IronbellyOrg/IronClaude` (expect HTTP 406), `gh pr view <n> --repo IronbellyOrg/IronClaude --json files --jq '.files \| length'` (expect 100), `gh pr view <n> --repo IronbellyOrg/IronClaude --json changedFiles`, and `gh api repos/IronbellyOrg/IronClaude/pulls/<n>/files --paginate --jq '.[].filename' \| wc -l` (expect 320). Watch what pr-submit's own reads and the bots do. | The throwaway head and base; close the PR unmerged, delete both branches. | pr-submit completes, or fails in a way the release brief can describe. | pr-submit hangs or reports a clean result without reading the files. Then 300 files is an absolute hard stop, and the tooling-fallback row of 8.5 is not available. |
| **T10** no extra cost; inside release 1. | Whether bot review depth tracks PR size (INV-025). | For each PR, write in the ledger: files, bot findings, bot review count, owner minutes. | None. | Observation only. | Not applicable. The numbers are used to reset decision 2. |
| **T11** no extra cost; inside releases 1 and 2. | Owner latency while the release PR waits (INV-003). | Write the PR-opened and PR-merged times in the ledger. | None. | Observation only. | Not applicable. If both waits exceed one working day (GUESS), the owner decides whether release n+1 may be cut from n's tip (Q4). |

After all trials a last check: `git ls-remote --heads origin 'refs/heads/*dash0-trial*'` must print nothing.

Follow-up work outside this proposal, each its own issue: the two-parent closeout check (Q4); paging the file list in the `/sc:auggie-review` rubric (section 8.4).

## 10. Decisions for the owner

<!-- Source: Variant 3 sec 8 ("Open decisions") and unique contribution U-012, merged per Change #17; the eight decisions are those of refactor-plan "Decisions for the owner", same order -->

This document carries a default for all eight decisions, so the work can start before the owner answers; each answer changes the text only as stated. They are ordered most important first. Each lists the recommended answer and what every answer does.

**Decision 1. May the coordinator do five things without asking each time?**
(a) Merge a settled story into the release line locally with a merge commit. (b) Push the line forward-only after each merge, and reset a merge that failed the gate and was not yet pushed. (c) Run the CI-equivalent commands, including `make sync-dev`, that the release brief names. (d) Delete story, line and records branches and worktrees after the owner's merge. (e) Merge `master` into the line instead of rebasing (an exception to pre-PR check 2 in CLAUDE.md, because the line is published).
Recommended: yes to all five (debate point C-006, 75 percent; the use-case notes say "to be confirmed").
- **Yes:** the design runs as written; the owner clicks once per release PR (plus a records PR or a sync PR when they apply).
- **No to (a):** every story goes through a review-only PR (Q2): more owner clicks, bots on every story, and no CI without a workflow edit.
- **No to (b), (c), (d) or (e):** the coordinator asks for each such step; the backup push, the gate, the sweep or the merge-in waits for the owner.

**Decision 2. Size numbers.**
Story cap 6, time box 7 days, release-PR file budget 250 over all paths, stop adding at 200, hard stop 300 (the last is GitHub's tool limit). Recommended: accept for release 1, then reset from the ledger's measured counts.
- **Accept:** as written; unfinished stories ride the next release.
- **Looser (for example 400 files):** the PR passes the `gh pr diff` limit; reviews use the paged API and the local diff; the tooling problem of section 8 is back for that release.
- **Tighter (for example 150 files):** more, smaller releases and more owner clicks.

**Decision 3. A records PR when a release is over budget.**
Recommended: yes, decided at freeze (section 8.3); promote it to the default if it triggers three releases in a row.
- **Yes:** records land in their own PR first; the release PR stays readable; one extra owner click and CI run.
- **Always:** the same, with no freeze count; one extra PR for every release, including small ones.
- **Never:** records ride the release PR; above 300 files the review tools fail on it and the owner reviews through the local diff.

**Decision 4. Merge method of a story into the line** (debate points C-005 and X-004, unresolved at 50 percent).
Recommended: `--no-ff` (merge commit).
- **`--no-ff`:** story boundaries stay visible (`git revert -m 1`, `git bisect --first-parent`); a reverted story needs "revert the revert" before it returns; the optional review-only PR needs it to show as merged.
- **Squash:** a plain `git revert` removes a story and nothing needs the revert-the-revert step; the story's own commits are lost from the line.

**Decision 5. Is `integration` still in use, and does the coordinator run the sync?**
Facts: `master` is 26 commits ahead of `integration`, and there has been no merged PR into `integration` since 2026-11-18 or 2026-11-19. Recommended: the coordinator runs the `master` into `integration` sync PR (head `dash<rel>-sync<N>`, merge commit) after each landing, and the owner says whether Clay still works from `integration`.
- **Still in use, coordinator syncs:** as written; one more PR per release.
- **Still in use, someone else syncs:** the text names that person; the coordinator opens no sync PR.
- **Not in use:** the sync PR and the early-warning checks against `integration` come out of the text. Whether to retire the branch is a separate question this proposal does not raise.

**Decision 6. How much outside look at a story, and the one-line workflow change.**
Three parts. (a) Dispatch runs of `test.yml` on the pushed line, about 9 minutes each, after shared or risky stories and on the final tip. (b) Review-only story PRs for stories above about 15 files or 1,000 added lines. (c) Adding `release/**` to the `pull_request` branch filter of `test.yml` (one line). Recommended: (a) yes; (b) off until trial T6 passes; (c) no for release 1.
- **(a) yes:** a CI-clean check on the tip before the PR. **No:** only the local gate and the PR run.
- **(b) on:** bots see big stories early, with no CI on those PRs. **Off:** the first review is the release PR.
- **(c) yes:** story PRs get CI. **No:** story PRs get bots only.

The cost of saying yes to (c): (1) a change to `.github/workflows/test.yml`, which must also be the version GitHub reads for a `pull_request` run. Where GitHub reads it is UNVERIFIED (two secondary sources say the merge commit), so the edit may have to be the first commit on the line before any story PR is opened, and it works only for PRs opened afterwards. (2) CI minutes: median 9.2 minutes per run. With one to three runs per review-only story PR (GUESS: one on open, one per pr-submit fix push) and six stories, that is about 55 to 165 minutes per release (ESTIMATE; arithmetic on a guess). (3) A wrong pattern leaves story PRs with no CI while everyone assumes they have it: if Orca prefixes a branch, `release/**` does not match `ironbelly/release/dash1.3`, so the pattern must be checked against the real branch name (trial T1). (4) The edit rides in the release PR and changes `test.yml` on `master` permanently.

**Decision 7. A test-only release of several stories (1.105): a line or direct PRs?**
Recommended: a line, like every other release (Q6).
- **Line:** one rule set, the ledger on the line, one PR, one click.
- **Direct PRs:** each story is a PR into `master` with its own CI, bots and click; the ledger has no home for that release; the coordinator runs a second rule set.

**Decision 8. How to guard the merge click on the release PR.**
Recommended: the PR-body sentence plus the new two-parent closeout check (detective), and the revert-and-redo recovery.
- **Sentence plus check:** a wrong click is found after it happens; recovery costs a revert PR and a redo (#658, #662, #664).
- **Sentence only:** cheaper; a wrong click may go unnoticed until a story revert fails.
- **Restrict merge methods on `master` in repository settings:** blocks the wrong click, but also the owner's normal squash for every other PR; not recommended.

## 11. Sources

<!-- Source: Base (original, modified) - Variant 1 sec 8, extended with sources cited by Variants 2, 3 and 4 and by the plan; evidence ids S1 to S22 point to `research-notes.md` in this folder -->

Evidence ids (S1 and so on) point to `research-notes.md` in this folder. The debate, scoring and merge records are in the `adversarial/` folder next to this file.

**Supports the design**
- S3 Driessen note (2020): release branches fit explicitly versioned software.
- S8 Fowler: release branch and release train; use a release branch when integration frequency is low.
- S9 Microsoft Release Flow: a release branch per release; fixes start on trunk.
- S21 practitioner guides: serial merges, ownership boundaries, trial merges with `git merge-tree`.
- S22 Mozilla and Chrome: schedule-driven releases that go without unready features (the time box).
- S6 DORA small batches: the one-week batch limit extrapolated into the time box.

**Evidence against, or limits on it**
- S1 trunk-based development, short-lived branches (about two days); S2 trunk-based development, branch for release ("do not do release branches" for continuous delivery teams); S6 DORA; S19 Faros review-burden numbers (vendor data, cited as a risk).
- S4 merge queues: wildcard rules are unsupported and private repositories need an enterprise plan, so the design does not use one. S10 stacked pull requests: availability on this plan is UNVERIFIED, so the design does not use them.
- S11 GitHub Actions events (CI by base-branch filter), S12 automatic branch deletion (the setting is off here), S20 flags and branch by abstraction (the third rung of Q5).

**Repository evidence** (read-only checks, 2026-11-23, recorded in `adversarial/invariant-probe.md` and `adversarial/debate-transcript.md`): pull requests #31, #484, #490, #491, #640, #658, #662, #664, #728 and #730; the GFxAI pull request #147 and its `git-standards-protocols.md` approach document (`gfxai-approach.md`, `gfxai-fit.md` in this folder); the workflows `test.yml`, `boundary-guard.yml` and `contract3-generator-constraint-lint.yml`.

## 12. How this was produced

<!-- Source: New section (merge executor), Step 5 summary of the debate for a reader who has not seen it; facts from debate-transcript.md Convergence Assessment, base-selection.md and invariant-probe.md -->

1. **Four proposals.** The owner's model (one release line, story branches, local merges, one pull request); a trunk model (short pull requests into `integration`, unfinished work landing dark); a release train (a batch branch with a pull request per story); and the approach written down in the owner's organisation repository GFxAI, rewritten for this repository.
2. **Two debate rounds, four advocates** (the maximum at standard depth). They agreed on 51 of 58 points, 87.9 percent against an 80 percent threshold. The count includes 10 points nobody contested; without them it is 41 of 48, 85.4 percent.
3. **The owner's model was chosen as the base.** Combined score 0.9351 against 0.9203 for the release train, a margin of 0.0149, which is under the 0.05 threshold. The tiebreaker (points won in the debate) gave it 27 of 41 against 9, because the other advocates conceded the questions that decide a base: where the line is cut from, how it lands, and keeping Clay's unreleased work out of the release PR.
4. **Seven points stayed unresolved**, and each appears in this document as a default plus a decision: the merge method of a story (decision 4), whether a test-only release needs a line (decision 7), whether the CI trigger file must be edited (decision 6), how Orca treats exact branch names (trial T1), and who runs the `master` into `integration` sync (decision 5).
5. **Invariant check.** A fault-finding pass listed 26 assumptions: 8 addressed, 18 not (1 HIGH, 10 MEDIUM, 7 LOW). The HIGH one, that a very large release PR cannot be read by the tools in the loop (INV-017), is handled by the size budget of section 8. The ten MEDIUM and seven LOW findings each have a rule, a decision or a trial. The gate has not been re-run on this text, so the status stays blocked until it is: INV-017 is handled and still to verify.
6. **Nothing here is tested on the real repository.** Items marked VERIFIED-HERE were checked in scratch repositories or by reading the CLI help and documentation while writing; none of the twelve trials of section 9 has been run; the eight decisions of section 10 are unanswered, and the defaults in the text are not approvals.
