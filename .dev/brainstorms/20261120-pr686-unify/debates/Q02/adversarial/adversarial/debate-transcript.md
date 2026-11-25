# Adversarial Debate Transcript

## Metadata
- Depth: quick (one round; Round 2, Round 2.5 invariant probe and Round 3 skipped by design: `--depth quick`)
- Rounds completed: 1 (Round 1 parallel advocate statements; no forced taxonomy round needed)
- Convergence achieved: 92.9% (13 of 14 diff points agreed)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant 1 = OURS, Variant 2 = CLAY; both ran as independent read-only agents of the same model family, so this is not a multi-model debate)
- Taxonomy coverage: L1 (S-001, C-006), L2 (S-002, C-001, C-004, C-007), L3 (C-002, C-003, C-005, X-001, X-002, A-001, A-002, A-003). All three levels covered, so no forced round.
- Omission check: both advocates answered A-001, A-002 and A-003. No `[OMISSION]` flags.
- Statements below keep each advocate's headings and substance; the "Files read" footers are dropped.

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)

**Position summary.** A local `git branch -d` is a guarded yes. Issue 687 gets the order of operations right. Its nine rules are not enough for branch deletion, because `-d` has no default-branch or long-lived-branch protection and rule 2 can pick an older merged PR over a newer open one. Three cheap refusals (branch name, any open PR on the head, a dry-run column) are added, and the guards that cannot be defended are dropped.

**Steelman of Variant 2.** Safety already exists in layers: rule 1 excludes the main checkout, rule 2 needs the PR MERGED (squash-safe, from PR state), rule 3 needs HEAD at or behind the PR head, git's `-d` refuses what it cannot prove merged, there is no `--force`, and dry run is the default. A refusal is reported as "kept", not as an error. An acceptance test records every command and fails on `-D`, `rm`, `prune` or a remote delete. Loss is recoverable (the branch stays on GitHub; `deleteBranchOnMerge` is false, so branches pile up; confirmed `squashMergeAllowed:true`, default `master`). Extra rules are extra code with their own bugs. A coherent, tested, never-force design.

**Strengths claimed.**
1. `-d` has no default-branch protection. Reproduced in a copy of the scratch repo: a local `integration` and `master`, fully merged into origin, were both deleted from another branch. Caveat: created at the same commit as `origin/master`, so trivially merged.
2. Issue 687 has no branch-name guard. Its only "name guard" is for folder names (`orca-port-*` and similar, issue lines 221 and 276). Rule 1 protects `master` only if it is the first `git worktree list` entry; a linked worktree on `master`, `main` or `integration` is not excluded.
3. `integration` is real: `git ls-remote --heads origin integration` returns 141e97fe; `gh pr list --head integration --state all` returns three MERGED PRs (#664, #658, #640), all into `master`. A worktree on `integration` matches rule 2.
4. Today's `integration` tip fails rule 3 (141e97fe is not an ancestor of those PR heads, checked with `git merge-base --is-ancestor`), so the hole is latent; a stale `integration` checkout would pass rules 2 and 3. No linked worktree is on `master`, `main` or `integration` now.
5. `-d` means "pushed or merged", not "its PR landed": `feat-pushed` was deleted with only a warning. The proof of landing has to come from rules 2 and 3.
6. Orca's own removal is conservative ("retains ... any branch whose changes it cannot prove are already merged"); a script that deletes more is looser than the tool beside it.
7. A branch-name refusal costs a set of names plus `gh repo view`; a stale local branch is cosmetic, a deleted `integration` needs the reflog or remote.

**Weaknesses identified in Variant 2.**
1. Fact 8 rests on a misleading citation: D13's "`-d` refuses an unmerged branch" holds only for never-pushed or squash-with-deleted-remote cases (reproduced: `feat-local` and `feat-squash [gone]` refused), and is false for a pushed-but-unmerged branch, which V2's own Risk admits.
2. "Git's own refusal behind it" covers only what git models; no branch-name rule is offered.
3. Rule 2's "newest merged one when there are several" (issue line 277) leaves a gap: an older merged PR plus a newer open PR resolves to the merged one. Rule 3 catches new commits but not an open PR whose head equals the old merged head. Not shown to occur (GitHub may refuse a no-diff PR: UNVERIFIED), so defense in depth, not a demonstrated bug.
4. The dry run shows one decision per worktree; the branch outcome appears only afterwards as "kept". A person approving `--apply` cannot see which branches will go.
5. Both sides cite WORKER-CONTRACT lines 236-237; as paraphrased it also forbids removing a branch with an open PR or unmerged commits. Not re-read this round (UNVERIFIED here); not leaned on.

**Concessions.** (1) "No other worktree has it checked out" is redundant (git refuses; reproduced), drop it. (2) Strict `headRefOid` equality is stricter than rule 3 (equal or ancestor); keep rule 3's wording, add no second check. (3) "No open PR uses it as its base" is speculative, thin, can be dropped. (4) The `integration` risk is latent, not live. (5) Not measured how often an older merged PR and a newer open PR co-occur on one branch name. (6) The guard list adds code and about four tests that must themselves be correct.

**Shared assumptions.**
- A-001: QUALIFY. False when the remote branch is deleted (`[gone]`: the squash scratch case and 21 of 56 local branches). Recovery then needs `refs/pull/N/head` or the reflog; the "recoverable" claim must say so.
- A-002: ACCEPT. `-d` compares to the upstream if set, else HEAD of the checkout it runs in; the `feat-pushed` run shows it varies per branch and checkout. Another reason `-d` is not the guard.
- A-003: QUALIFY. `gh pr list --head <branch>` matches by name only, no owner filter; rule 1 requires an owned origin, which limits but does not remove a wrong match; a reused name like `integration` shows several PRs on one name, so state and `headRefOid` checks matter.

**Per diff point.** S-001 equal. S-002 HYBRID (keep issue 687's rule set in place, add only the few branch refusals). C-001 agreed yes. C-002 OURS (no branch-name guard in the issue; `-d` deleted `master` and `integration` in the copy; `integration` is real). C-003 HYBRID (keep the branch if any OPEN PR has this head; drop "open PR as its base"). C-004 CLAY (rule 3 already covers it; extra check withdrawn). C-005 CLAY (git refuses). C-006 OURS (per-row "branch: would delete / would keep (reason)"). C-007 HYBRID (`--apply` the only switch; Clay's report-only week adopted; whether a grant is also required is left to the owner). X-001 OURS (`feat-pushed` reproduced). X-002 QUALIFY (gap real in the wording of rule 2, unproven in practice; one "any OPEN PR on this head keeps the branch" line covers it).

### Variant 2 Advocate (CLAY)

**Position summary.** A local `git branch -d` after a safe worktree removal is a yes, and issue 687 already specifies it as step 4, with no `-D`, no remote delete and a dry run by default. The nine rules plus git's refusal are enough for the common cases. A small branch-name refusal (default branch, `integration`, `main`) and a dry-run branch column are cheap, separable additions that OURS has earned.

**Steelman of Variant 1.** `git branch -d` is a weak safety check: "merged to HEAD or to the upstream", not "its PR landed". In OURS' scratch test it deleted a pushed but unmerged branch, and it has no notion of a default or long-lived branch. The repo really has a long-lived `integration` branch. The owner asked for "extra rigid and strict" validation, so a script that deletes branches should carry its own refusal list and show each branch decision in the dry run. Orca itself keeps branches it cannot prove merged. All of this is cheap; the downside of over-strictness is a stale local branch. It gets two things right: rule 1 as written has no branch-name refusal, and a daily unattended script is a different risk class from a human typing `git branch -d`.

**Strengths claimed.**
1. The spec already decides the question and has a tested never-force surface: step 4 ("`git branch -d`, never `-D` ... reported as kept, which is not an error ... remain on GitHub"), the "never does" list, and an acceptance test that records every command and fails on `--force`, `-D`, `rm`, `prune` or a remote delete (saved text line 354). OURS' "exactly `git branch -d <name>`" is already satisfied.
2. The branch step adds little risk beyond the worktree removal: nine rules must pass first (merged PR, nothing after the PR head, issue closed, no unsaved files, idle 7 days, not in use). Deleting the local ref only removes a pointer to commits already merged and held on GitHub. An open-PR conflict would already be a reason to keep the worktree.
3. Squash merges and unmerged work are handled as documented: `-d` refuses a squash-merged branch, so it is kept and reported (issue lines 214 and 369); rule 2 is "never from commit ancestry"; git refuses a branch checked out elsewhere, which makes OURS' guard redundant (C-005).
4. Orca already deletes the local branch with or without `--force` (checked `orca worktree rm --help`); the script's `-d` is not a new class of action.
5. `deleteBranchOnMerge` is `false` (verified with `gh repo view`), so merged branches pile up; every extra guard is code that needs tests, and the spec is already about 35 test cases.

**Weaknesses identified in Variant 1.**
1. The `integration` risk is mostly theoretical here: no linked worktree on `master`, `main` or `integration`; deletion needs HEAD to equal the newest merged PR's `headRefOid`; a local delete of `integration` is recoverable from origin. Real edge case, low probability, does not justify a guard framework.
2. The open-PR guard partly duplicates rules 2 and 3 (a newer open PR from the same branch normally carries newer commits, which rule 3 catches). "No open PR uses it as base" is a new concept the spec never mentions; UNVERIFIED as needed.
3. OURS' own fact 2 is weaker than it looks: a pushed, unmerged branch deleted by `-d` leaves its commits on `origin/<branch>`, the normal recovery path.
4. Hand-rolled guards can be wrong in ways git's check is not (a `headRefOid` match and a default-branch lookup add `gh` calls that can fail or mismatch); the spec already says a failed lookup keeps the worktree.

**Concessions.** (1) OURS' fact 2 is real; the nine rules, not `-d`, carry that safety, and D13's phrasing "`-d` refuses an unmerged branch" (V2 fact 8) overstates git: withdrawn as a safety argument (X-001). (2) The default-branch and long-lived refusal is genuinely missing from issue 687; about three lines, separable, adopted (C-002). (3) Rule 2's "newest merged one when there are several" leaves a gap; one sentence fixes it (X-002). (4) A dry-run branch column is a real usability gain (C-006). (5) Citation caveat: the WORKER-CONTRACT text sits at different line numbers in different trees; the text itself (coordinator "removes the child with `orca worktree rm` and deletes its branch"; never a branch with an "open PR" or unmerged commits without the user's instruction) is confirmed. `orchestrator.md` line 139 (ADD5) is about `gh pr merge --delete-branch`, i.e. remote deletion, so it does not decide the local question.

**Shared assumptions.**
- A-001: QUALIFY. Holds only while the remote branch exists; with `deleteBranchOnMerge` false it usually does; otherwise recovery is `refs/pull/N/head`, so the script should log the PR head SHA.
- A-002: ACCEPT. `-d` judges against upstream or HEAD, which varies; keep rules 2 and 3 as the real gate and print the `headRefOid` match in the dry run.
- A-003: QUALIFY. The script should require the PR's `headRepositoryOwner` to be ours and the matched head SHA to equal HEAD; one check inside rule 2, no separate branch guard.

**Per diff point.** S-001 equal. S-002 CLAY (an addendum to rules 1-3 suffices; no separate guard list). C-001 agreed. C-002 OURS, adopt as HYBRID (name refusal for `master`, `main`, `integration` and the default branch; `origin/integration` exists, three merged PRs use it as head). C-003 HYBRID (explicit "keep when any PR with this head is OPEN" in rule 2; skip the "base" refinement). C-004 HYBRID leaning OURS (use exact `headRefOid` equality for the branch decision; the ancestor clause is fine for the worktree but exact match is stricter for deleting a ref). C-005 CLAY. C-006 OURS. C-007 HYBRID (`--apply` the only switch; the script ships report-only first; Clay's one-week report-only period fits). X-001 OURS. X-002 OURS on the gap, CLAY on the fix (one added sentence in rule 2).

## Scoring Matrix
| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | Tie (agreed equal) | 90% | Same section layout; both advocates say equal |
| S-002 | HYBRID, structure from Variant 2 | 75% | Keep issue 687's rules in place; add an addendum, not a parallel list (both advocates) |
| C-001 | Agreed yes | 95% | Both advocates and issue 687 step 4 |
| C-002 | Variant 1 | 92% | Variant 2 conceded; `-d` deleted `master` and `integration` in the scratch repo; three merged PRs use `integration` as head |
| C-003 | HYBRID, Variant 1 idea in one line | 80% | Both: keep the branch if any OPEN PR has this head; drop the "open PR as base" part |
| C-004 | Split; resolved to Variant 2 (rule 3 as written) | 55% | V1 withdrew the extra check; V2 leaned to exact equality; a ref at an ancestor of the PR head loses no commit, so the stricter check protects nothing more |
| C-005 | Variant 2 | 92% | Git refuses a branch checked out elsewhere (both measured); V1 conceded |
| C-006 | Variant 1 | 90% | Both agree a per-row branch outcome in the dry run is a real gain |
| C-007 | HYBRID | 70% | `--apply` the only switch (both); report-only first week adopted; grant requirement left to the coordinator rules |
| X-001 | Variant 1 | 95% | Reproduced `feat-pushed` deletion; V2 withdrew fact 8 as a safety argument |
| X-002 | Variant 1 on the gap, Variant 2 on the fix | 78% | Wording gap real, unproven in practice; one added sentence closes it |
| A-001 | QUALIFY (both) | 85% | Recovery also needs `refs/pull/N/head`; log the PR head SHA |
| A-002 | ACCEPT (both) | 90% | `-d` judges against upstream or HEAD; rules 2-3 are the gate |
| A-003 | QUALIFY (both) | 82% | Require our `headRepositoryOwner` and matching head SHA inside rule 2 |

## Convergence Assessment
- Points resolved: 13 of 14 (unresolved: C-004)
- Alignment: 92.9%
- Threshold: 80%
- Status: CONVERGED (taxonomy levels all covered; Round 2.5 not run at depth quick, so the invariant gate is not applied)
- Unresolved points: C-004 (resolved afterwards by the orchestrator in base-selection.md with the reason above)
