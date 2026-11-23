# Round 2 rebuttal: advocate 4 (Variant 4, GFxAI approach adapted, qa persona), last in the sequence

Written 2026-11-23. Read: round1-advocate-1.md to round1-advocate-4.md and round2-advocate-1.md to round2-advocate-3.md. Citation style follows the earlier rebuttals: A1-W13 is advocate 1's Round 1 weakness 13, A2-S5 is advocate 2's Round 1 strength 5, A3-C1 is advocate 3's Round 1 concession 1, A1R2-4 is point 4 of advocate 1's Round 2 section 1, N3 is advocate 2's Round 2 evidence item 3, E2 is advocate 3's Round 2 evidence item 2 (so my own Round 1 evidence log items are written R1-E1 to R1-E7). My own Round 1 strengths and concessions are R1-S and R1-C. New evidence of this round is labelled M1 to M11 and is in section 3. Everything was read-only; nothing was written to GitHub or to this repository except this file (scratch repos were under `/tmp` and removed). UNVERIFIED marks anything I could not confirm.

## 1. Response to criticisms of Variant 4
### Settled, no further defence (already conceded in R1-C1 to R1-C4 and agreed by all four)
1. **Merging `integration` into the release (A1-W13, A2-W13, A3-W10; X-003, C-018, A-017).** Wrong. R1-E3 tested it and A1, A2 and A3 all reject A-017. Nothing to add.
2. **When CI runs, X-008 (A1-W14, A2-W13, A3-W11) and the undefined base (A3-W12; C-002, X-001).** The first was resolved by dropping pull requests per story (gfxai-fit named change 1, R1-C1); the second by "cut from `master`" (R1-C3). Both are closed.
3. **Ledger and planning base (C-020, X-009), the long-lived cap (C-013), cherry-pick hotfixes (C-015).** Conceded in R1-C4, R1-C7, R1-C6; A1R2, A2R2 and A3R2 all adopt V1's version.

### Conceded now because the new evidence forces it
4. **Three-level story names (A1-W17, A2R2 Q1, A3R2 Q1; C-001, A-007, A-011).** I conceded "flat names are more robust" in R1-C5 but kept `dash1.3/story/NN-slug`. A2 and A3 now give the concrete failure and M1 supports it. The Orca help text (M1) says a worktree's branch gets "the prefixed default" unless `--branch` is passed, and CONTEXT line 12 says `worker-start` has no `--branch`. The owner's own token for the release is `dash1.3`. A worktree named `dash1.3` therefore gets the branch `ironbelly/dash1.3`, and `ironbelly/dash1.3/story/01-x` can then never be created (the git error is the one R1-E1 reproduced for a bare `dash1.3`). Flat story names (`dash1.3-s04-slug`) cannot hit that, with or without the prefix. I withdraw R1-S1 for story branches and keep only the `release/<rel>` folder for the release line, where no tool is likely to name a worktree `release/dash1.3` by accident.
5. **Squash into the release line (A1-S10, A1R2 section 5 C-005, A2R2 C-005, A3R2 C-005; C-005, X-004).** I withdraw R1-S2's differentiator and R1-S3. Reasons, each tested or read today: (a) A1R2 section 3 item 1 showed that reverting the revert first, then merging the fixed branch, is clean; so the `--no-ff` trap I verified (R1-E2) is a missing procedure, not a structural defect, and I said "structural" in R1. (b) R1-S3 claimed a cheap bisect for squash; M5 shows `git bisect --first-parent` over six `--no-ff` story merges names `merge s4` as the first bad commit, the same story-level answer, and the first-parent log has 7 entries against 26 in the full history. (c) The optional review-only story PR layer in A3R2 Q2 only works if GitHub can see the PR as merged after the coordinator's local merge; for a merge commit that is true by general GitHub behaviour (the PR head is reachable from the base), for a local squash it is not (UNVERIFIED by me: a GitHub write would be needed; the throwaway test in A3R2 settles it). (d) The cleanup tool keys on "its own pull request is merged" (M6), so PR-backed stories under `--no-ff` can be retired by the tool and local squashes cannot. What I keep: the merge-method rule for the release pull request (merge commit only), which all four now share, and a plain `git revert <sha>` is still marginally simpler than `-m 1`. C-005 is a tie that I lean to `--no-ff` for local story merges.
6. **Release-sized review is the shape with in-repo evidence against it (A3-W14, A3R2 E4, A2-W15, A2R2 point 10; C-021, C-007).** A3's #31 (2,089 files, merged 2026-05-12) after ten story pull requests with no checks or reviews is a better local example than GFxAI #147. I re-checked #31 itself (M9: 0 reviews, 0 comments, 2,089 files); the claim that its ten story pull requests had no checks or reviews is A3's sample and I did not re-check it. I also give up the weight I put on R1-S8(b) ("#640 and #664 landed and stayed"): A2 N2 shows those promotions merged in 43, 17 and 27 minutes, and a fast merge of 181 or 1,146 files proves nothing broke, not that anyone read it. What stays of R1-S8 is the narrower claim: the lesson supports a story cap, a digest and an extra outside gate, not a ban on a release line. The combined design adds the outside gates (M2, M8) that V4 and V1 lacked.
7. **"Closeout checks the merge method" (R1 strength table, R1 failure table row 4; A1R2 point 4 adopted it).** I wrote it as if it existed. M4: `branch-landed.sh` reads `mergeCommit` and `baseRefName` and is built to be squash-safe, and grep finds no assertion about the merge method in the closeout skill. It is new work, but small: a merge commit has two parents, and the script already fetches the merge commit. I retract the implication that it is in place.
8. **`/sc:worktrees` could remove an unpushed release worktree (R1-W2).** Retracted. M6: the tool removes a worktree only when "its own pull request is merged, nothing was added after that pull request" and about six other conditions hold, and "every step fails closed". An unmerged release worktree cannot be removed by it. The forward-only push stays as a backup against a disk loss or a manual `orca worktree rm`, not against that tool. A3-W1's wording "worktrees do get archived and removed" is correct only after the PR is merged.

### Contested, with counter-evidence
9. **"V4 adds mostly weak-fit pieces to V1" (A1-W15).** Right about the original text, wrong about the surviving parts. What V4 still contributes that V1 lacked and that all three others have adopted: the `release/<rel>` folder (A1R2 Q1, A2R2 Q1, A3R2 Q1), the freeze (A1R2-2, A2R2 C-016, A3R2 C-016), the explicit clean-up rule with the delete step because `delete_branch_on_merge` is off (all three), and the provenance marks (A1R2 U-014, A3R2 U-014). I do not claim more than that.
10. **"Provenance marks are documentation, not substance" (A1-W15).** For this decision they are substance: M7 shows nothing technical enforces any of the branching rules (no rulesets, `master` and `integration` unprotected), so what makes a rule real here is that a reader can see which ones rest on evidence and which on invention.
11. **The thin source (A2-W14, A2-W15, A3-W13).** Conceded in R1-C9 and R1-C10; unchanged. I do not ask for weight on the GFxAI pedigree.

## 2. Updated assessment of the other variants
### V1 (now the base of every combined design)
- **Changed my mind:** four of A1R2's adoptions are right and I adopt them as written: forward-only push of the release line (A1R2-1), the freeze (A1R2-2), the merge-method sentence in the release PR body (A1R2-4, with the retraction in section 1 point 7: the check is new work), and the rule "never re-merge a reverted story branch directly" (A1R2 section 3 item 1; my R1-E2 and M5 are consistent with it). A1R2-6 is also right that the Clay collision lands on a sync branch and then on `integration`, not on `master`; the `git merge-tree` run against `origin/integration` (A1R2 Q3) is the best cheap early warning on the table.
- **Changed my mind against V1:** A1R2 point 7 reads the 17 to 43 minute promotions as "reviewers here already take roll-ups of this size". A2R2 point 10 and A3R2 point 11 read the same numbers as a rubber stamp, and I now side with them: the merge time of a 1,146 file diff cannot show that it was read (section 1 point 6). V1's real review control is therefore the story cap, the digest and whatever outside gate is added before the roll-up, not the roll-up itself.
- **Did not change:** V1 still has no outside look at a single story unless the owner approves a dispatch run or a review-only PR. That is the gap V4-with-local-merges inherits, and M2 and M8 now say how to fill it cheaply.

### V2
- **Changed my mind:** `integration` is not a live trunk. I checked A2's N1 from the git side (M11: the newest commit on `origin/integration` is #667, 2026-11-18 21:35 -0600) and `master` is 26 ahead and 2 behind. V2 as a base is out, and A2R2 section 2 says so itself. Two V2 pieces are worth taking: the spec-time classification of each story's shared files and independent shippability (U-006, as a planning rule only), and the idea that every change should be judged by something other than the coordinator (here by dispatch CI and optional bot review).
- **Did not change:** C-007 and C-011 stay V2's on detection latency. Where I disagree with A2R2 is the hand-opened draft release PR (A2R2 Q2) as a way to get CI on every push: `/sc:pr-submit` cannot open a PR as a draft (its argument hint has `--merge-guard {draft,off}` but no open-as-draft flag) and its guard flips drafts to ready on its own schedule (M10), the owner's rule is that pull requests are opened only through `/sc:pr-submit`, and draft behaviour of Augment, Codex and CI is "unverified" by the command's own text. I would not build on it.
- **A2R2 Q5 two lanes (small direct pull requests for 1.1 bug-fix and 1.105 test-only releases):** reasonable, but it departs from the owner's model (CONTEXT line 7: every release is a branch). V1 already allows a one-story release to skip the line. I would put the test-only case to the owner as a question, not as a rule.

### V3
- **The best new idea of Round 2 is A3R2 Q2, the optional review-only story pull request.** It keeps "the coordinator merges locally" and removes Decision A. M8 verifies its key premise from this repository's own history: Augment and Codex both reviewed pull requests whose base was a non-default batch branch (#484, #490, #491), and #491 is the follow-up fix for #490's findings. It also gives an honest price: no CI on those pull requests (0 checks on all three), a top-level `/sc:pr-submit` session per story (A3-C10), and two bot passes on top of the final roll-up. As an optional layer for large or risky stories it is worth taking.
- **Two cautions A3R2 did not cover.** (a) It needs the local merge to be a merge commit (section 1 point 5c). (b) After the coordinator merges story A locally, story B's open pull request has a moved base; `/sc:pr-submit` resolves that only "as one merge commit of the recorded base tip, pushed fast-forward" (SKILL.md line 337), so the coordinator has to push the release line before B's monitor reads it. Order of operations must be written down.
- **Route (a) of A3R2 Q2 (the workflow edit as the line's first commit)** rests on two secondary sources about which workflow file a `pull_request` run reads (A3R2 E7, UNVERIFIED). Route (b), `workflow_dispatch`, has an in-repo precedent (M2). I would make (b) the default.

### V4 (my own variant, honest summary after two rounds)
What is left of V4 in the combined design: the `release/<rel>` folder for the release line, the beta freeze, the explicit clean-up and delete-the-remote-branch rule, the merge-method rule for the release pull request, a fix-forward rule for hotfixes (merge `master` in, no cherry-pick), and the FROM SOURCE / FROM PRACTICE / MY ADAPTATION marks. What is not left: pull request per story, the `integration` merge, squash, three-level names, the source's tiers and approvers, and any claim that the GFxAI pedigree counts as precedent.

## 3. New evidence not presented earlier
All read-only, run 2026-11-23. Commands are named in words, not copied, to keep the file short.

- **M1. What `orca worktree create --branch` does (the CLI's own help, Orca 1.4.245).** Option text: "`--branch <name>` Git branch name to use instead of the prefixed default". Notes: "Pass --branch to name the Git branch without the configured prefix (a taken name gets a numeric suffix)". So with `--branch` the name is exact and unprefixed (A-011 answered by the documented behaviour, not by a run), and without it the branch is the prefixed default (A2 N5: `ironbelly/<worktree name>`). Two edges: `worker-start` has no `--branch` (CONTEXT line 12), and a "taken" name silently gets a numeric suffix, so the coordinator must read back the real branch name after every create. Whether a ref-conflicting name (a branch under an existing leaf) counts as "taken" is UNVERIFIED.
- **M2. `workflow_dispatch` has already run on a non-listed branch in this repository.** `gh run list --workflow test.yml --event workflow_dispatch` returns two runs on 2026-11-05, both on branch `ci/parallel-python310-tests` (not `master` or `integration`), both `success`, 4 min 7 s and 5 min 1 s. This turns A1R2's "UNVERIFIED by a real run" into a verified precedent for dispatch on an arbitrary pushed branch (a new run is still a GitHub write that needs the owner's nod).
- **M3. CI wall time.** Of the last 40 `pull_request` runs of `test.yml`, 31 succeeded: minimum 7.0, median 9.2, maximum 12.6 minutes. That is the CI cost of one dispatch run per story merge (about 9 minutes each). It answers part of A-010 for CI; the local suite time is still unmeasured by anyone.
- **M4. What closeout checks about merging.** `~/.claude/skills/sc-closeout-protocol/scripts/branch-landed.sh` is written to be "Squash-safe" and reads `mergeCommit`, `mergedBy` and `baseRefName` through `gh pr view`, and `settle.sh` and the result template only record the first 7 characters of the merge commit. I read every match of squash, merge method and mergeCommit in the closeout skill; none asserts the method. A merge-commit check is new work (two parents on the merge commit).
- **M5. First-parent bisect over `--no-ff` story merges (scratch repo, git 2.47.3).** Six story branches of three commits each merged with `--no-ff`, story 4 breaks a file. `git bisect start --first-parent` plus `bisect run` reports "merge s4" as the first bad commit. `git log --first-parent` shows 7 entries against 26 in the full history. Merge-commit history therefore gives story-level bisect, which removes my R1-S3 advantage.
- **M6. What the new cleanup tool removes.** `scripts/worktree_cleanup.py` on `origin/master` (read with `git show`): "A worktree is removed only when all eight rules hold: ... its own pull request is merged, nothing was added after that pull request, every issue it relates to is closed, nothing unsaved is in it ... Every step fails closed". Consequences: (a) it cannot remove an unmerged release worktree, so my R1-W2 worry is withdrawn; (b) a story worktree with no pull request has no merged PR and is kept, so a local-merge design needs an explicit manual removal step; (c) for a review-only story PR the tool can retire the worktree only if GitHub shows the PR MERGED.
- **M7. No technical enforcement of any branching rule.** `gh api repos/IronbellyOrg/IronClaude/rulesets` returns no rulesets; `branches/master/protection` returns "Branch not protected" (404); `branches/integration` reports `protected: false`. So nothing blocks a direct push to `master`, nothing requires a review or a green check, and nothing limits the merge method. "No commit directly on master", "merge commit only" and the freeze are conventions that a person or a skill has to check. My R1 claim of "one `release/**` pattern for a ruleset" is a possibility, not a current fact.
- **M8. A3's bot claim, re-checked by me.** `gh pr view` on #484, #490 and #491 (base `346Claude-integration`, a non-default batch branch): reviewers `augmentcode` and `chatgpt-codex-connector` on #484 and #490, `augmentcode` on #491; `statusCheckRollup` length 0 (no CI) on all three; #491 is "fix(review): address #490 review findings (refs #346)". Bots do review non-default bases here; CI does not run there. A-012 can be answered ACCEPT for this repository.
- **M9. #31 re-checked.** `gh pr view 31`: base `master`, 2,089 files, merged 2026-05-12, 0 reviews, 0 comments. A search of `master` commits from 2026-05-12 to 2026-06-15 for "tdd-spec-merge" or "#31)" found only the merge commit and one unrelated merge; I found no revert. That is weak evidence of no harm (one grep, one window) and no evidence of harm, so #31 shows an ungated big landing, not a failure.
- **M10. `/sc:pr-submit` and drafts.** `~/.claude/commands/sc/pr-submit.md`: argument hint `--merge-guard {draft,off}` with no flag to open a PR as a draft; line 83 and following: at `--monitor 3` the guard turns the PR into a draft during a fix cycle and marks it ready afterwards; line 94: behaviour of Augment, Codex and CI on drafts "is unverified until the owner's run on a disposable PR; do not rely on it". This bears on the release PR (the one PR that always exists) and on A2R2's draft-PR idea.
- **M11. `integration` recency.** `git log origin/integration -1`: `141e97fec` by clayphi, 2026-11-18 21:35 -0600, "docs: post-release sync and install runs for 6.1.0 (#667)". `master` has 26 commits `integration` lacks and `integration` has 2 `master` lacks (A1R2, A3 E1 and my R1-E4 saw 26, 26 and 24 as `master` moved).

## 4. Combined design, question by question
Base: the owner's model as V1 states it (release line, story sub-branches cut from it, the coordinator merges locally, one pull request into the default branch by `/sc:pr-submit`). Constraint check against your list: the release is a branch and stories are sub-branches by ancestry (Q1, Q2); no ref conflict is possible with the names in Q1; the coordinator merges locally (Q2); pull requests are opened only by `/sc:pr-submit` (Q2, Q4); CI stays configured for pull requests and pushes into `master` and `integration` only, and the extra CI in Q2 is a manual dispatch, not a trigger change. Sources in brackets; "(new)" marks a piece none of the four variants had.

**Q1. Names.**
- Release line `release/dash1.3` [V4 folder; V1, V2 and V3 advocates agree]. Story branches flat: `dash1.3-s04-<slug>`; in-release fix `dash1.3-fix01-<slug>`; docs-only `dash1.3-docs01-<slug>` [V2, V3 flat names; V4 kinds in flat form]. Shipped-code fix `fix/<issue>-<slug>` from `master` [all; the repository already uses `fix/`, R1-C5]. Tag `dash-1.3` on the merge commit [V4].
- Why flat for stories: M1 plus CONTEXT line 12. A worktree made without `--branch` gets `ironbelly/<worktree name>`; the owner's own token is `dash1.3`; a folder-style story name then collides with it. A flat name coexists with `ironbelly/dash1.3`, with `release/dash1.3` and with the prefix.
- One invariant, written once: no branch is ever named exactly `release`. Two-digit story numbers sort; release tokens 1.1 and 1.105 sort in the planned order, a future 1.10 would not, so write it 1.100 [V1].
- Create every release and story branch with `orca worktree create --name <n> --branch <exact name> --base-branch <ref> --parent-worktree <selector> --agent claude`, then read back the real branch name, because a "taken name gets a numeric suffix" (M1) [new]. First use is preceded by one throwaway create [V3 U-013].

**Q2. Where story work merges, how, who resolves, what stops collisions.**
- Locally, by the coordinator, into `release/dash1.3`, one story at a time, with `--no-ff` [V1; I lean this way, see section 5 C-005]. Before the merge: disjoint path claims, the shared-file list below, and a read-only `git merge-tree` trial [V1 U-001, U-003]. After the merge: targeted tests, one ledger line written before and one after, then a forward-only push of the line [A1R2-1; new for V4].
- Shared-file list (R1 A-001 answer, from the stat of #662): `CHANGELOG.md`, `CLAUDE.md`, `README.md`, `PROJECT_INDEX.json`, `PROJECT_INDEX.md` and the docs index files belong to the coordinator and are edited once near the end, or to a first foundation story [V1 foundation story, new list].
- Outside gate 1, default, no workflow edit: the coordinator starts `test.yml` by `workflow_dispatch` on the pushed line after a story merge when the story touched shared or risky paths, and always on the final tip. Precedent M2, cost about 9 minutes per run (M3), needs the owner's nod for the CI minutes [A1R2, A2R2; M2 is new].
- Outside gate 2, optional per story, chosen in the story spec: a review-only story pull request, `/sc:pr-submit --monitor 3 --base release/dash1.3`, so Augment and Codex review a small diff (M8); the monitor fixes confirmed findings; when the bots have settled the coordinator merges locally (merge commit) and pushes, and GitHub then shows the PR as merged (UNVERIFIED, one throwaway test) [A3R2 Q2]. Use it for stories above a size the owner sets; A3R2's suggestion (about 15 files or 1,000 added lines) is consistent with #490 (25 files, +4,636, needed #491) against #484 (8 files, +217), and is not a measured threshold.
- Conflicts: the coordinator stops and reports; the story worker merges the release tip into its own branch and re-runs its gates; a clash of intent goes to the owner [V1, worker contract, CONTEXT line 9]. Parallelism two stories for the first release (A-004); above about four, re-open the design [A3R2 A-004].

**Q3. Staying current.**
- Merge `origin/master` into the line at the start, between story merges (never mid-merge) and before the release pull request; merge only, never rebase after the first push [V1, V4].
- Never merge `integration` (A-017). Run `git merge-tree` of the line against `origin/integration` at each `master` merge-in and compare path claims with open `integration` pull requests at release start [V1 U-003, A1R2-6].

**Q4. How the release lands.**
- One pull request `release/dash1.3` into `master`, opened by `/sc:pr-submit --monitor 3 --base master` from a top-level session in the release worktree. CI and both bots run once on it [V1, V4].
- Body: the sentence "Merge this pull request with a merge commit, not squash" (the #658 incident, R1-E4), the per-story digest [V1 U-002] and the path classes so reviewers can skip `.dev/` records [A-009]. Closeout gets a small check that the merge commit has two parents (M4) [new; needs building].
- Pre-landing acceptance gate, reduced from V4's tiers: freeze after the last planned story (Q6), a green dispatch run on the final tip, the full local suite, and the owner. No two-approver rule: the owner is the only merger [V4 U-018, reduced; R1-C9].
- Size: a story-count cap and the days-not-weeks rule set at planning (Q5). Merge speed is not evidence of review depth (section 1 point 6), so the cap and the optional story pull requests are the controls, not the roll-up.
- `--merge-guard draft` is the default at `--monitor 3` and the effect of drafts on bots and CI is "unverified" (M10): include the release PR in the throwaway test list.

**Q5. Flags, trunk-based, justification.**
- No flags. The line is justified by explicit versioned releases and the owner's model, only while short [V1, V3 U-010]. Time box with floating scope: stories not merged at the end ride the next release. Starting numbers for the owner to accept or change: about six stories or seven days, whichever comes first (A2R2 and A3R2 estimates, not measurements).
- Escalation ladder, as all neighbours state: if a box is missed twice, review-only story pull requests for every story; if that is missed too, land dark-by-construction slices as direct pull requests, only after a pilot [V3, V2 U-009].
- A one-story release skips the line [V1]. Whether a test-only release (1.105) may do the same is a question for the owner (departs from CONTEXT line 7) [A2R2].

**Q6. Hotfixes and bug fixes during a release.**
- Shipped bug: `fix/<issue>-<slug>` from `master`, pull request into `master`; the open line picks it up at its next `master` merge-in. No cherry-pick and no copying step [V1; R1-C6].
- Bug inside the line: `dash1.3-fix01-<slug>`, merged locally like a story. Freeze: once the last planned story is merged, only `-fix` branches enter the line until the owner merges [V4, adopted by all].
- 1.1 bug-fix releases are ordinary lines of fix stories [V1, V4].

**Q7. Clean-up and records.**
- Story branch and worktree: after the merge is in the ledger and the line is pushed. The cleanup tool will not retire a story worktree that has no merged pull request of its own (M6), so the coordinator removes it (`orca worktree rm`) and deletes any pushed story branch on the remote [new; the repository's `delete_branch_on_merge` is false, R1-E6]. With `--no-ff` the story tip stays reachable as a second parent.
- Release line: after the owner merges and the sync pull request (Q8) is open, delete the remote and local branch and remove the worktree (the tool can retire this one by itself once its PR is merged and nothing was added) and tag `dash-1.3` [V1, V4].
- Records: `.dev/` records, the ledger and `sprint-status.yaml` stay on the line and land with it [V1]; the per-story digest lives in the release PR body.

**Q8. Fit with `integration` and Clay.**
- Nothing changes for Clay during a release. After the landing the coordinator opens the `master` into `integration` sync, which maintainers already do by hand (five such commits by clayphi on 2026-11-17 to 11-19, R1-E4) [V1, V4]. Clean-up of the line waits for that sync to be open.
- A question the data raises for the owner: is `integration` still the branch Clay works from? Its newest commit is 2026-11-18 (M11) and it is 26 commits behind `master`, so the first sync carries 26 commits that are not the release's doing [A2R2 Q8, A3R2 Q8].

**Q9. Failure and rollback.**
- Bad story inside the line: `git revert -m 1 <story merge>`, or fix forward on a `-fix` branch. Never merge a reverted story branch directly: revert the revert first, then merge the fixed branch (A1R2 section 3 item 1, tested by A1 and by me in R1-E2). Dependent stories revert in reverse order [V1 U-005]. To find which story broke the line, `git bisect --first-parent` names the story merge in a few steps (M5) [new].
- Release fails on `master`: a revert pull request of the release merge commit through `/sc:pr-submit`; prefer a bug-fix release line over re-landing. The repository has already used this path once: #662 reverted the squash of #658 and #664 landed the same work as a merge commit (R1-E4).
- A wrong merge method on the release pull request: the Q4 sentence and the two-parent check; nothing in the repository settings can stop the click (M7).

**What the owner has to decide (one list).** (1) Confirm that the coordinator may merge settled stories into the release line locally (CONTEXT line 11, "to be confirmed"). (2) Story cap and time box. (3) Approve CI minutes for dispatch runs, and say whether review-only story pull requests are wanted and above what size. (4) Is `integration` still in use. (5) Story merge method: `--no-ff` (my lean) or squash.

**Throwaway tests before the first release.** (a) `orca worktree create --branch` keeps the exact name, and what happens with a name that conflicts with an existing ref (M1). (b) A review-only story pull request against `release/...`: do both bots review it, and does GitHub show it merged after a local `--no-ff` merge and push. (c) The release pull request at `--monitor 3` with the draft guard: do the bots and CI behave (M10). (d) One dispatch run on the pushed line. (e) The two-parent check in closeout.

## 5. Per diff point positions (points I contest)
"Winner" is the variant, or combination, whose answer I would put in the merged proposal for this repository under the owner's constraints. Confidence is my probability that the call is right. Changes from my Round 1 are marked.

| Point | Winner | Conf. | Reason |
|---|---|---|---|
| C-001 names | Combined: V4 `release/<rel>` folder, V2/V3 flat story names (changed from R1 "partial") | 70 | M1 and CONTEXT line 12 give the concrete prefix hazard for folder-style stories; flat names cannot hit it. The folder for the release line is safe because `--branch` gives the exact name (M1) and nothing else is named `release`. |
| C-002, X-001 base | V1 (`master`), V4 once it says so | 90 | M11 and A1R2, A2R2 N3, A3R2 E1: `integration` is 26 behind and quiet since 2026-11-18. All four now agree. |
| C-003, X-002 landing | V1 (V4 agrees) | 85 | Owner's model; the promotion path carries everything in `integration`; all four agree. |
| C-004 where stories merge | V1 default, V3 optional review-only PR layer | 60 | Local merge fits the constraints; M8 verifies bots on a non-default base and shows a follow-up fix (#491) from a small-PR review. |
| C-005, X-004 merge method (changed from R1 "win") | No winner; I lean `--no-ff` for local story merges | 55 | Trap has a tested remedy (A1R2 3.1), first-parent bisect gives story-level granularity (M5), the optional PR layer and the cleanup tool both favour a merge commit (M6); squash keeps a marginally simpler revert. The release PR is a merge commit for everyone. |
| C-006, X-005 merge guard | V1 | 65 | Local merge into a line only the coordinator and workers use is the smaller authority; owner confirmation still needed (A-014). |
| C-007 per-story CI and reviewers | V2 for CI latency; combined: dispatch default plus V3 review-only layer for bots | 60 | M2 and M3 make dispatch a proven, 9 minute route; M8 proves the bots on non-default bases; V2 keeps the lead on "every change, no edit, no ask". |
| C-008 staying current | V1 | 85 | `master` only. |
| C-009, X-007 rebase | V1 (merge only) | 75 | One rule. Low stakes. |
| C-010 conflict procedure | V1 | 60 | No `integration` merge-in, so V3's sync branch is a reserve only. |
| C-011 collision latency | V2 on latency; V1 guards before the merge; V3 layer adds bots | 60 | Same suite behind all of them (A-005). |
| C-012 incomplete-work isolation | V1 with V3 time box | 75 | No flags; dark landing unproven (A2R2 concedes). |
| C-013, X-006 justification | Combined: V1 line, V3 time box and ladder | 75 | Conceded in R1-C7; all four converge. |
| C-014 story granularity | V1 (one story, one branch, one worktree) | 70 | Owner's model; V4's source unit (a whole feature) does not transfer. |
| C-015 hotfix back-port | V1 | 85 | R1-C6. |
| C-016 freeze | V4 | 80 | Adopted by all; the one rule that makes "being verified" mean something at AI speed. |
| C-018 Clay coupling | V1 | 90 | All four. |
| C-019 sync obligation | V1 and V4 | 60 | The sync is the price of landing on `master`; clayphi does it by hand today (R1-E4); who does it after a dashboard release is still unassigned (A-015). |
| C-020, X-009 ledger and planning base | V1 | 90 | All four. |
| C-021 release size | Combined: V1 cap and digest, V3 optional story PRs; V2/V3 win on per-unit review | 60 | Merge speed is not review depth (section 1 point 6); the controls are the cap, the digest and the outside gates. |
| C-022 rollback | V1 at release and story level (with the redo procedure), V2 at slice level | 65 | Changed from R1: V4's squash edge is gone. The #662 to #664 sequence is the in-repo precedent for revert then re-land. |
| C-023 clean-up | V4 and V1 | 85 | `delete_branch_on_merge` false (R1-E6) and the cleanup tool needs a merged PR (M6): explicit local and remote deletion is required for PR-less story branches. |
| C-024 tag | V4 `dash-1.3` | 55 | Trivial; four of four use or accept it. |
| C-025, X-010 stacks | No winner | n/a | Nothing to stack under local merges. |
| X-008 (V4 internal) | Resolved | n/a | By dropping story PRs. |
| U-001 to U-003 (V1) | V1, adopt | 80 | With `git merge-tree` against `origin/integration`. |
| U-006 (V2 slice classification) | V2 as a planning rule only | 55 | Each story spec lists shared files and whether it can ship alone; also feeds the shared-file list. |
| U-010 to U-013 (V3) | V3, adopt | 85 | U-013 now has five jobs (throwaway tests a to e). |
| U-014, U-015 (V4) | V4, adopt | 65 | Provenance marks; size evidence from GFxAI #147 and in-repo #31, with #31's limits (M9). |
| U-016 kind in the branch path | Flat form only | 50 | `dash1.3-fix01-...`; the folder form is dropped. |
| U-017 "no agent merge to the default branch" | V4 as wording | 55 | States what the owner rule forbids; local merges into the line are a separate class. |
| U-018 release gate | V4 reduced | 55 | Green dispatch run on the final tip, full local suite, owner; not the GFxAI tiers or two approvers. |
| S-002 provenance | V4 | 55 | M7: nothing enforces the rules, so showing which rest on evidence is substance. |
| S-003, S-005 (diagram, costs and risks sections) | V1, V2, V3 | 80 | I concede. |

Assumptions, one verdict each (changes from R1 marked):

| A-NNN | Verdict | Conf. | Reason |
|---|---|---|---|
| A-001 | QUALIFY | 70 | Path claims necessary not sufficient; shared-file list added in Q2. |
| A-002 | QUALIFY | 70 | Ledger line before and after each merge, push after each merge. |
| A-003 | QUALIFY | 65 | A2 N1: about 5.7 owner merges a day; one large read is a different load from many clicks. |
| A-004 | QUALIFY | 65 | Two stories fine; re-open above about four. |
| A-005 | REJECT | 70 | Not a premise anyone can rely on; the others say "necessary, not sufficient" and I agree with that wording. |
| A-006 | ACCEPT | 95 | Verified by three advocates; nothing stops a wrong click (M7). |
| A-007 | QUALIFY | 65 | Flat names lower the risk; throwaway test (a). |
| A-008 | QUALIFY | 60 | Moot for the default route (dispatch, M2); the PR-merge-ref route (A3R2 E7) is UNVERIFIED. |
| A-009 | QUALIFY | 65 | Path classes and digest; check whether bots can skip `.dev/**` (UNVERIFIED). |
| A-010 | QUALIFY | 70 | CI is about 9 minutes (M3); local suite still unmeasured. |
| A-011 | QUALIFY | 75 | Exact name with `--branch`, prefixed default without it, numeric suffix when taken (M1); read back the name. |
| A-012 | ACCEPT (changed from R1 QUALIFY) | 90 | M8 verified for a non-default base in this repository. |
| A-013 | QUALIFY | 70 | Not needed by the default route; needed only for CI on story PRs. |
| A-014 | QUALIFY | 65 | Needed for local merges; owner confirms in chat. |
| A-015 | ACCEPT | 80 | clayphi does it by hand; assign it for dashboard releases. |
| A-016 | QUALIFY | 65 | Review is the bottleneck, but merge method (#658) and merge speed (A2 N2) also matter. |
| A-017 | REJECT | 95 | R1-E3, and all four agree. |

## 6. Points where all four advocates now agree
Read from the three Round 2 statements plus mine; "all four" means advocates 1, 2, 3 and 4 give the same call in their combined designs or position tables.

1. **Base of the release line is `master`; the release lands by one pull request into `master` through `/sc:pr-submit --monitor 3 --base master` (C-002, X-001, C-003, X-002).** A2R2 and A3R2 withdrew their `integration` positions; A1 and I never held it.
2. **`integration` is never merged into the release line (X-003, C-018, A-017 rejected).** Four of four; A4 tested it (R1-E3).
3. **Keep the current-with-`master` rule: merge `master` only, never rebase after the first push, and run `git merge-tree` against `origin/integration` (C-008, C-009, X-007, U-001, U-003).**
4. **Ledger and `.dev/` records stay on the release line; planning of the next release starts from `master` (C-020, X-009).**
5. **Hotfixes and shipped-code bugs: `fix/<issue>-<slug>` from `master`, picked up by the next `master` merge-in, no cherry-pick (C-015).**
6. **Freeze after the last planned story merge; only `-fix` branches until the owner merges (C-016).**
7. **Explicit clean-up, including deleting the remote branch, because `delete_branch_on_merge` is false (C-023, A-006 ACCEPT).** All three methods are enabled; the release pull request is stated to be a merge commit in its body.
8. **Forward-only push of the release line after each story merge, as a backup and not a review request.**
9. **Release line named `release/<rel>`; tag `dash-1.3`; shipped-code fix on `fix/` (C-001 for the release line, C-024).**
10. **Revert-then-redo needs a stated procedure: revert the revert first, then merge the fixed branch (C-005 trap, C-022).**
11. **No flags in the base design; a time box with floating scope; the ladder to per-story pull requests and then to V2 slicing as the fallback (C-012, C-013, X-006, U-010).**
12. **Adopt U-001 to U-003, U-010, U-012, U-013, U-014, U-015.** U-006 to U-009 are third-rung fallbacks only.
13. **X-008 (V4 internal) is resolved; C-025 and X-010 (stacks) are dropped because nothing is stacked under local merges.**
14. **A-017 REJECT; A-006 ACCEPT; A-012 ACCEPT (M8, E2); A-005, A-010 QUALIFY with the CI time measured (M3).**
15. **Local coordinator merges into the line need the owner's explicit confirmation in chat (A-014; CONTEXT line 11 "to be confirmed").**

## 7. Points still contested
1. **Story branch shape (C-001).** A1R2 keeps `dash1.3/s04-slug` (folder, "release/" for the line); A2R2, A3R2 and I use flat `dash1.3-s04-slug`. Three of four. The remaining disagreement is whether a hand-made branch named `dash1.3` is a risk worth designing out (M1 and A2 N5 say yes); a throwaway create (test a) settles how the prefix behaves.
2. **Story merge method (C-005, X-004).** A1R2 leans `--no-ff` (55), A2R2 and A3R2 say no winner (50), I lean `--no-ff` (55). Nobody now argues for squash with evidence; it is the owner's call (decision 5 in section 4).
3. **How much outside gate a story gets (C-004, C-007, C-011, C-021).** A1R2: dispatch on request, no story pull requests. A2R2: dispatch after each story, plus a hand-opened draft PR to be tested. A3R2: dispatch plus an optional review-only story pull request, and a first-commit workflow edit as a second route. Mine: dispatch default and the optional review-only layer; I reject the hand-opened draft PR (M10, owner's rule). What decides it is three tests: the merged state after a local merge, the bots on `release/` bases, and the draft behaviour at `--monitor 3`.
4. **Numbers for the cap and the time box (C-013, C-021).** A2R2 and A3R2: about six stories or seven days; A1R2: owner decides; mine: owner decides, starting numbers are estimates only.
5. **Whether bug-fix (1.1) and test-only (1.105) releases need a line (C-017).** A2R2 and A3R2: no line for small or test-only releases; A1R2 and I: ordinary lines, with a one-story skip, test-only as an owner question.
6. **Who runs the `master` into `integration` sync (C-019, A-015) and whether `integration` is still in use.** All four flag it; nobody can answer it from the repository (M11).
7. **Release PR acceptance gate content (U-018).** A1R2 and I: full local suite, pull request CI and bots, owner; plus, in my design, a green dispatch run on the final tip. A2R2 and A3R2: the same, without a stated gate.
8. **Where the workflow file is read for a `pull_request` run (A-008).** A3R2 cites secondary sources for the merge ref; A2R2 and A1R2 mark it UNVERIFIED; the default route avoids the question, so it only matters if story pull requests need CI.
9. **Who may merge a review-only story PR (A-014).** The coordinator locally, never by a click (A3R2, mine) against the owner by click (the standing rule). Owner's decision, no evidence settles it.
10. **Value of the GFxAI pedigree (U-015, U-014).** I give it no weight as precedent; A1R2 gives U-014 and U-015 65; A3R2 the same. Low stakes, no effect on the design.
