# Round 2 rebuttal: advocate 2 (Variant 2, analyzer persona)

Written 2026-11-23. Read: round1-advocate-1.md to round1-advocate-4.md and round2-advocate-1.md. Citation style follows advocate 1: A1-W2 is advocate 1's weakness 2 against V2 (from the "Weaknesses identified in the others" list), A3-S2 is advocate 3's strength 2, A4-C1 is advocate 4's concession 1, A1R2-n is point n in advocate 1's Round 2 section 1. My own Round 1 points are R1-S (strength) and R1-C (concession). Every new number below comes from a read-only command I ran today (section 3); nothing was written to GitHub or to this repository. Anything not confirmed is marked UNVERIFIED.

## 1. Response to criticisms of Variant 2
### Conceded because the evidence forces it
1. **`integration` is not the live trunk today (A4-W5, my R1-S10 withdrawn).** N1 and N3: no merged PR into `integration` since 2026-11-19, 26 commits on `master` it lacks, 18 of them the owner's. V2 section 3 assumes work flows through `integration`; the owner's practice is direct PRs to `master`. Any V2 slice would first need a 26-commit `master` into `integration` sync and would then sit on a branch the owner has not used in 130 PRs. This is a bigger fit problem than the ledger, and it was invisible from CONTEXT alone. I withdraw R1-S10 ("uses the documented flow"): the documented flow is CLAUDE.md, the practice is different, and the owner's constraint is a release merged to the default branch.
2. **No home for the ledger (A1-W2, A3-W8, A4-W4).** Conceded in full; C-020 and X-009 go to V1. My R1-C2 per-slice record file is not needed once a release line holds the ledger.
3. **Dark landing is unproven (A1-W3, A3-W7).** Conceded; I have no new evidence for it and the combined design below does not depend on it.
4. **Shipping is tied to Clay's promotions (A1-W4, A3-W6, A4-W6).** N2 gives the concrete case: Clay promoted `integration` twice in about 36 hours (#640 merged 2026-11-18 16:30, #664 merged 2026-11-19 01:47) at his own timing and carrying everything on the branch. A dark slice in `integration` would have shipped with the first one whether or not the dashboard release was ready. "Dark by construction" is then a hard requirement, not a style choice.
5. **Release-level rollback (A1-W5, A3-W9).** The promotion merge commit holds all unpromoted `integration` work, Clay's included, so reverting it is a bad release-level undo. C-022 at release level goes to V1. I keep slice-level undo (A1 R1-C3 concedes it).
6. **Clean-up by auto-delete (A4-S6, A1R2 section 3 item 3).** V2 section 3 step 4 relies on a setting I marked UNVERIFIED; N8 shows it is off. V2 needs an explicit delete step, so C-023 goes to V1 and V4.
7. **The owner is the lane (A1-W1, A3-W5), with the load now measured.** I keep R1-C1. N1 shows the owner's PRs merge at about 5.7 a day with a median of 90 minutes open, and Clay's slice PRs merged in a median of 24 minutes, so V2's load is inside the demonstrated rate and A1R2 correctly withdrew "throttled". I do not claim more than that: those are largely self-authored PRs, the counts include record-only PRs, and none of them is one release's slices.
8. **My R1 weakness 1 against V1 was wrong in one part (A1R2-6).** I said the Clay collision lands on `master` after the release. It lands on a sync branch and then on `integration`, the testing branch. I withdraw that wording. The part that stands: the cost falls on Clay's open PRs, and the only early warning is path claims plus a trial merge.

### Contested, with evidence
9. **Cherry-pick duplicate noise (A4-W7).** N7: real only when `integration` later edits the same lines (case 2 conflicted, case 1 merged clean), and it resolves as an ordinary conflict in the sync. Low cost, and not needed at all in the combined design because the line merges back into `master`.
10. **Duplicated second review (A1-W6).** N2: promotions merge in 17 to 43 minutes, so the second pass is cheap in practice. The stronger reading is that the roll-up is not where review happens; N4 shows the 23 slice PRs each got Augment, Codex and CI in their own right (sample of 4). This also answers A1R2-7 ("reviewers here already take roll-ups of this size ... landed and stayed"): the data show they were merged quickly, which is not evidence that a 181 or 1,146 file diff was read. V1's single PR gets exactly that treatment and has no earlier review behind it.
11. **"Merge-in work is higher in V2 because it is per slice" (A1R2-9).** UNVERIFIED either way; nobody measured conflict rates. Per-slice drift is hours, the line's drift is days, and conflict probability grows with drift, but I cannot show the totals.
12. **Squash makes dashboard history inseparable from Clay's (A3-W9).** True for revert as one object; findable by story id in the commit message and by `git log --grep`. This is a cost, not a defect, and only matters if V2 is the base, which I no longer argue.

### Not contested
V2 is a counter-proposal to the owner's model (A4-W4). For this round the model and the five constraints you listed are fixed, so I judge V2 by which of its pieces survive them (section 4).

## 2. Updated assessment of the other variants
### V1 (after A1's rebuttal)
**Changed my mind.** (a) Landing and base: N1 and N3 say `master` is the real trunk and `integration` is stale, so C-002, X-001, C-003 and X-002 now go to V1 for the owner's dashboard releases. (b) The adopted fixes are real improvements: forward-only push of the release line after each merge (A1R2-1), the freeze (A1R2-2), the revert-the-revert rule (A1R2-3, which also confirms A4's trap and closes my R1 shared point 18), and a merge-method guard in the PR body for the #658 failure (A1R2-4). (c) The `git merge-tree` trial merge against `origin/integration` (A1R2-6) is a good extension of U-001 and U-003.
**Did not change my mind.** (i) V1 still has no bot review of any story. Its `workflow_dispatch` idea is partly right: the trigger exists (N6), so CI can be started on a pushed release line without a workflow edit. But a dispatched run is a GitHub write that someone must request each time, it gives no Augment or Codex review, and A1 admits it is untested. It narrows C-007 and C-011; it does not close them. (ii) A1R2-7 reads the promotion record as reassurance; N2 reads it as evidence that a roll-up is a rubber stamp. That makes the story-count cap the only real review-size control in V1, and the cap number is still not set. (iii) V1's weakest remaining claim is "one owner nod buys part of the same gate"; until that is run once, it is a hypothesis.

### V3 (after A3's Round 1)
A3 conceded Decision A as a hard dependency (A3-C1), CI growth with waiting stories (A3-C4), per-story top-level `/sc:pr-submit` sessions (A3-C10) and that it could not confirm where GitHub reads the workflow file (A3-C12). Under the owner's constraint that CI runs only for PRs into `master` or `integration`, V3's main benefit (CI on every story PR) needs that constraint lifted, so V3 does not fit the constraint set as given. What survives and I take: U-010 (time box, floating scope), U-012 (owner decisions as a short list) and U-013 (throwaway PR before relying on any filter or prefix). A3-S2 (the bulkhead) is the best argument for V3; it does not change my position because it still needs the `test.yml` edit and a new merge authority.

### V4 (after A4's Round 1)
A4 dropped the PR-per-story, the `integration` merge, the undefined base, the missing ledger, the missing cap and the cherry-pick copying (A4-C1 to C7). What is left is V1 plus a `release/` folder, squash, a freeze and an acceptance gate. I accept that reading. A4's evidence log is the most useful new material in Round 1 (the #658 incident, delete-on-merge off, `workflow_dispatch`), and N8 reproduces the settings. A4-C5's worry about three-level names under the Orca prefix has a concrete mechanism, see N5 and section 4 Q1.

### V2 (my own variant)
As a standalone proposal V2 does not fit: it needs a live `integration` trunk (N1, N3), a ledger home it lacks, and a dark-landing practice nobody has tested. As a source of parts it still holds the strongest evidence-based pieces: per-change outside review and CI with no config edit, slice-level undo, flat names that cannot collide, and the idea that a release should be cut late and kept short. Section 4 takes those.

## 3. New evidence not presented in Round 1
All read-only. Dates are UTC. "Merged" counts come from `gh pr list --state merged`, so they say a PR reached the merged state, not who clicked.

**N1. Where merged PRs actually go (gh, since 2026-11-01).**
- Into `integration`: 23 PRs, all by clayphi; median 23.6 minutes from open to merge; median 51 files, 90th percentile 101 files. The all-time list for base `integration` returned only 24 merged PRs, newest merged 2026-11-19 03:35 (#667). So `integration` has had no merged PR for about four days.
- Into `master`: 155 PRs, 130 by ironbelly and 25 by clayphi; median 89.9 minutes; median 37 files, 90th percentile 334 files (record-heavy PRs such as #728, 453 files, and #730, 292 files, are in the tail).
- Consequence: 0 of the owner's 130 PRs went through `integration`. The owner's real trunk is `master`; `integration` was used for one wave by Clay (the v6 release, PRs #615 to #667), which is itself the V2 shape: many small PRs into `integration`, each with bots and CI, then a promotion.

**N2. How the promotions were reviewed (gh, created to merged).** #640 (`integration` to `master`, 1,146 files): 43 minutes. #658 (181 files, the mistaken squash): 17 minutes. #664 (181 files): 27 minutes. A roll-up of this size is merged in well under an hour, so it works as a final check, not as the place where review depth comes from.

**N3. `integration` against `master` (git, now).** `git rev-list --count`: 26 commits on `master` that `integration` lacks, 2 on `integration` that `master` lacks (both release bookkeeping from 2026-11-18 and 2026-11-19). Of the 26, 18 are by Ironbelly and 8 by clayphi (for example #711 and #700 by clayphi), so both maintainers have been landing directly on `master` since the v6 wave.

**N4. Bots and CI on non-draft PRs (gh api).** Augment (`augmentcode[bot]`) and Codex (`chatgpt-codex-connector[bot]`) both appear, with six check runs, on the four `integration` PRs I sampled (#639, #650, #656, #667) and on the three `master` PRs I sampled (#664, #673, #728). This confirms the baseline V2 relies on for bases `integration` and `master` only. It says nothing about any other base (A3's A-012 risk for `train/*` and `release/**` stays UNVERIFIED). PRs #686 and #690 are closed and currently drafts, and both carry Augment, Codex and six check runs, but I cannot tell whether those arrived before or after they became drafts, so this is inconclusive for draft behaviour.

**N5. Branch names the owner's sessions really produce (git).** 49 remote branches start with `ironbelly/`; PR #636's head is `ironbelly/RefactorIssueClaimPipeline` and the same name exists locally, so the pattern is `ironbelly/<name>`. Exact names without the prefix also occur in the owner's PRs (#730 `docs/409-606-working-records`, #688 `feature/blocker-classification-stage3c`, #660 `fix/review-seat-labels`). Remote shapes by first segment: `ironbelly/` 49, `clayphi/` 37, flat 33, `fix/` 19, `docs/` 16, `feature/` 13, others fewer. A worktree's current branch can differ from its worktree name (the `claim-handoff-planb` worktree is on `ironbelly/fix-comparison-pr-686-690-status`). What I did not run: `orca worktree create --branch`, so whether `--branch` keeps the exact name is still UNVERIFIED.

**N6. The workflow and pr-submit on drafts.** `.github/workflows/test.yml` has `pull_request` (line 6) and an unconditional `workflow_dispatch:` (line 8); the only `if:` lines are 140, 195 and 199 and none test the event name or the draft flag, so config does not skip drafts. `~/.claude/commands/sc/pr-submit.md` line 94 says that whether Augment, Codex and CI behave as expected on a draft is "unverified until the owner's run on a disposable PR; do not rely on it", and its argument hint has `--merge-guard {draft,off}` but no flag to open a PR as a draft.

**N7. Cherry-pick duplicate test (scratch repo under /tmp, removed after).** `integration` has slices A, B and a fix F; `release/dash1.3` is cut at A and F is cherry-picked onto it; the release is merged into `master` with a merge commit; then `master` is merged into `integration`. Case 1, no later edit of the fixed lines: clean merge. Case 2, `integration` edited the same line again after F: `CONFLICT` in the file. (My first two runs were invalid because an identical-hash cherry-pick made the commits the same object; the third run used distinct parents and is the one reported.) So A4-W7 is real but narrow.

**N8. Repository settings (gh api).** `delete_branch_on_merge` false; squash, merge commit and rebase merges all allowed. Matches A1R2 section 3 and A4 E6.

## 4. Combined design, question by question
Base: the owner's model as advocate 1 laid it out (release line, story sub-branches, coordinator merges locally, one PR into the default branch through `/sc:pr-submit`). I agree with advocate 1's skeleton for feature releases and propose these changes to it. Constraint check: no ref conflict (Q1), coordinator merges locally (Q2), PRs only via `/sc:pr-submit` (Q4, Q6), CI only for PRs into `master` or `integration` (Q2 and Q4 respect it; nothing here needs a `test.yml` edit).

**Q1. Names.** Release line `release/dash1.3` [V1, V4, agreed by A1R2]. Story branches flat: `dash1.3-s04-<slug>`; in-release fix `dash1.3-fix01-<slug>` [V2, V3]. Shipped-code fix `fix/<issue>-<slug>` [all]. Tag `dash-1.3` [V4]. Why flat and not `dash1.3/s04-<slug>`: the owner's own token is `dash1.3`, and N5 shows Orca names a branch `ironbelly/<worktree name>`. A worktree called `dash1.3` for the release would be `ironbelly/dash1.3`, and then `ironbelly/dash1.3/s04-...` fails with git's "cannot lock ref" error, exactly the error CONTEXT line 8 recorded. Flat names coexist with that accident, with `release/dash1.3` and with `ironbelly/` (R1-S5). They are still sub-branches by ancestry (cut from the release tip), which is what the owner's model needs. Listing: `git branch --list '*dash1.3-*'`. One throwaway `orca worktree create --branch ...` before first use settles the prefix question for all names [V3 U-013]. Source of the combined idea: V2 and V3 names, V4 release folder.

**Q2. Where story work merges.** Locally by the coordinator into `release/dash1.3`, one at a time, `--no-ff`, as in V1; before each merge the path claims and a read-only `git merge-tree` trial [V1 U-001, U-003]; after each merge the tests, a ledger line, and a forward-only push of the release line as a backup [A1R2-1]. The outside gate comes from V2's principle (a change is judged by something other than the coordinator's own run): start `test.yml` by `workflow_dispatch` on the pushed release line after each story merge, with the owner's standing approval for the CI minutes [A1R2-5, N6]. Two things to test once on a disposable PR before relying on them (N6, pr-submit line 94): whether a long-lived draft release PR against `master` (opened by hand, since `/sc:pr-submit` has no open-as-draft flag) gives CI on each push and bot review of the growing diff, and whether Augment and Codex react to a draft at all. If that works it is the closest thing to V2's per-slice feedback that fits the constraints. UNVERIFIED. Source: V1 base, V2 principle.

**Q3. Staying current.** V1 unchanged: merge `origin/master` into the release line at the start, between story merges and before the PR; never merge `integration` (A-017 rejected by everyone); never rebase after publication. Add the `git merge-tree` of the release tip against `origin/integration` at each master merge-in [A1R2-6]. Because `integration` is 26 commits behind `master` today (N3), do not use it as a base for anything dashboard related. Source: V1.

**Q4. How the release lands.** One PR `release/dash1.3` to `master` by `/sc:pr-submit --monitor 3 --base master`, merge commit only, stated in the PR body and checked by closeout [A1R2-4, V4]. Add the per-story digest [V1 U-002]. Freeze after the last planned story merge: only `dash1.3-fix<NN>` enters [V4]. Size: because a roll-up is merged in 17 to 43 minutes whatever its size (N2), the cap on the line is the real control. My estimate for the owner to set: about six stories, roughly 300 files at today's median of 37 to 51 files per PR, counted without `.dev/` records (inference from N1, not a measured limit). If the planned list is longer, plan two lines. Source: V1 with V4 freeze; the cap number is mine.

**Q5. Flags, trunk, justification.** Two lanes, decided at planning, not one rule for all releases:
- Feature release (1.2, 1.3 and so on): the release line, with a hard time box and floating scope, so an unready story rides the next line [V3 U-010]. No flags. Slice any story that cannot finish inside the box into stories that can [V2 U-006 adapted: the story spec states for each story its shared files and whether it is independently shippable].
- Bug-fix (1.1) and test-only (1.105) releases: no release line. Small PRs straight into the default branch with `/sc:pr-submit`, as the owner already does for 130 of the last 155 `master` PRs (N1). A test-only PR needs no isolation because it adds no behaviour. [V1 Q6 one-story shortcut, extended; V2 for test-only slices.]
- Third rung, only if the box is missed twice in a row: land dark-by-construction slices (new files that nothing imports) as direct PRs, as V2 describes. Needs the V2 pilot first (U-009).

**Q6. Hotfixes and bug fixes.** V1 unchanged: `fix/<issue>-<slug>` from `master`, PR to `master`, the open line picks it up at the next merge-in; no cherry-pick (N7 shows the cherry-pick path can conflict later and is only needed when a line does not merge back). Fix inside a line: `dash1.3-fix<NN>-<slug>`, merged like a story. Source: V1; V2's cherry-pick rule dropped.

**Q7. Clean-up and records.** Explicit deletion, because `delete_branch_on_merge` is false (N8): story branch and worktree after the merge is in the ledger and the line has been pushed; the line, its worktree and the remote branch after the owner merges and the sync PR is open; tag the merge commit [V1, V4]. `.dev/` records and `sprint-status.yaml` stay on the line [V1]. Source: V1, V4.

**Q8. Fit with `integration` and Clay.** V1: nothing changes for Clay during a release; after landing the coordinator opens the `master` into `integration` sync [V1, A1R2]. One new fact to hand the owner: `integration` has had no merged PR for four days and is 26 commits behind (N1, N3), so the first sync carries those 26 commits, which are not the release's doing. Whether `integration` is still the branch Clay works from is a question for the owner, not for this proposal. Source: V1.

**Q9. Failure and rollback.** Bad story inside the line: `git revert -m 1` of its merge commit, or a `-fix` branch; to bring a reverted story back, revert the revert first, then merge the fixed branch (A1R2-3, tested by A1 and A4) [V1]. Failed release on `master`: revert PR of the release merge commit, then a fix line [V1]; if it was squashed by mistake the revert still removes it as one commit. Slice-level undo and flag-off exist only in the third rung of Q5 [V2]. Source: V1.

**What the owner must decide (one list, A3 U-012 style).** (1) Confirm local coordinator merges into the release line (CONTEXT line 11, "to be confirmed"). (2) Set the story-count cap. (3) Approve CI minutes for a dispatch run after each story merge. (4) Say whether `integration` is still in use.

## 5. Per diff point positions (contested points)
"Winner" is the variant (or combination) whose answer I would put in the merged proposal for this repository under the owner's constraints. Confidence is my probability that the winner is right.

| Point | Winner | Conf. | Reason |
|---|---|---|---|
| C-001 names | V2/V3 flat story names with V4/V1 `release/` folder | 70 | N5: Orca's `ironbelly/<worktree name>` plus the owner's own token `dash1.3` reproduces the CONTEXT line 8 conflict for folder-style story names; flat names cannot. A4 E1 shows folders work if nobody creates the bare token, which is the hand-made mistake in question. |
| C-002, X-001 base branch | V1 (master) | 85 | N3: `integration` is 26 behind and unused for four days (N1). I concede this point from my R1. |
| C-003, X-002 landing path | V1 | 70 | The owner's model and the owner's practice (N1: 0 of 130 via `integration`). V2 and V3 shape is real for Clay's v6 wave, but not for the dashboard. |
| C-004 where stories merge | V1 | 65 | Fits the constraints. V2 is the better design in the abstract and cannot be adopted whole (section 2). |
| C-005, X-004 merge method | No winner (V1 `--no-ff` locally) | 50 | A1 and A4 each verified a trap and the remedy; for local story merges into a line that lands by merge commit, `--no-ff` with the revert-the-revert rule is adequate. |
| C-006, X-005 merge guard | V1 | 60 | Local merge into a backup-only branch is the smaller authority; the owner confirms it in chat. |
| C-007 per-change CI and reviewers | V2 | 70 | Only V2 gets CI and both bots on each change with no edit (N4). V1 with dispatch narrows it but gives no bot review (section 2). |
| C-008 staying current | V1 | 75 | Merge `master` only; V2 has no line, but under the constraints a line exists. |
| C-009, X-007 rebase | V1 | 70 | One rule, no carve-out. Low stakes. |
| C-010 conflict procedure | V1 with V3's sync branch unused | 55 | Without an `integration` merge-in there is no train-versus-`integration` conflict to route. |
| C-011 collision detection latency | V2 | 65 | Still earliest; V1's trial merge, path claims and dispatch runs reduce but do not remove the gap. |
| C-012 incomplete-work isolation | V1 and V3 (no flags) | 70 | N2 and A3-W6: a dark slice on a branch Clay promotes can ship at his timing. I concede from my R1. |
| C-013, X-006 justification of a long line | Combined: V1 line, V3 time box, hard cap | 65 | V2's "no long line" does not fit the owner's model; the cap is what limits the risk. |
| C-015 hotfix and back-port | V1 | 85 | N7 shows the cherry-pick path conflicts later and is needed only when a line does not merge back. |
| C-016 freeze | V4 | 70 | Adopted. |
| C-018, X-003, A-017 Clay coupling | V1 | 90 | N2 and A4 E3; I concede. |
| C-019 sync obligation | V1 and V4 | 55 | Sync is the price of landing on `master`; who runs it is still UNVERIFIED (A-015). |
| C-020, X-009 ledger and planning base | V1 | 90 | Conceded. |
| C-021 release size at final review | V2/V3 on review quality; the cap is the control in V1 | 60 | N2: a roll-up is merged in 17 to 43 minutes whatever its size. |
| C-022 rollback | V1 at release level, V2 at slice level | 65 | Section 1 point 5. |
| C-023 clean-up | V1 and V4 | 85 | N8: auto-delete is off. Conceded. |
| U-006 slice classification | V2, adapted as a planning rule | 60 | Each story spec states shared files and independent shippability; also the basis for the two-lane rule in Q5. |
| U-007 just-in-time cut | V2 in spirit only | 40 | Under the owner's model the line is cut at release start; the useful part is "keep it short", which the cap and time box carry. |
| U-008, U-009 (flags, pilot) | Third rung only | 55 | Needed only if the time box is missed twice. |
| U-010, U-012, U-013 | V3, adopt | 80 | Floating scope, owner decision list, throwaway check before trusting a prefix or a trigger. |
| U-001 to U-003 | V1, adopt | 80 | With the trial merge extended to `origin/integration`. |
| A-003 owner capacity | QUALIFY, updated | 65 | N1: about 5.7 merged PRs a day and a median of 90 minutes open for the owner; the load is inside the demonstrated rate, but it is self-authored PRs, not one release's slices. |
| A-005 tests catch collisions | QUALIFY, unchanged | 70 | Still unmeasured for dashboard code. |
| A-006 both merge methods enabled | ACCEPT (changed from QUALIFY) | 95 | N8 (also A1R2 and A4 E6). The #658 click shows nothing stops a wrong choice. |
| A-008, A-012 | ACCEPT for V3 and V4 only | 80 | N4 confirms bots and CI on bases `master` and `integration`; nothing on other bases. |
| A-015 who syncs | QUALIFY | 60 | Clay did it by hand (merge commit f7dcf031d, PR #639); the owner's direct-to-master PRs make the gap grow (N3), so assign it explicitly. |

Points I do not contest: S-001 to S-006, C-014, C-017, C-024, C-025, X-008, X-010.

**Net.** I still hold C-007 and C-011 for V2 and the slice-level half of C-022. I concede C-002, C-003, C-004, C-012, C-015, C-018, C-020, C-023 and X-001 to X-003 to V1, and C-001 and C-012's flag question are where V2 and V3 contribute to the combined design.
