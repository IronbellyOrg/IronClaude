# Round 2 rebuttal: advocate 1 (Variant 1, architect persona)

Written 2026-11-23. Read: round1-advocate-1.md to round1-advocate-4.md. Numbered points are cited as A2-W1 (advocate 2, weakness 1), A3-S2 (advocate 3, strength 2), A4-C1 (advocate 4, concession 1) and so on. Read-only checks I ran today are listed in section 3 with their output.

## 1. Response to criticisms of Variant 1

### Conceded in full (the evidence forces it)
1. **Nothing is pushed, so the release line is a single local copy (A3-W1, A4-W2).** Correct. V1 section 1 says "Nothing is pushed for review until the release is complete" and I let "not pushed for review" stand in for "not pushed". A lost or cleaned worktree loses the release, and A4 notes the new worktree-removal tool (#711) as a way that could happen. Fix, adopted: the coordinator pushes `release/<rel>` forward-only after each story merge, as a backup and not as a review request. This breaks no rule: V1 already never rewrites, `/sc:pr-submit` only forbids rewriting a published branch, and CI does not run on a push to a non-listed branch (`test.yml` lines 4 to 7), so the push costs nothing and notifies no bot. It also answers A2-W5 (no way for the owner to look early): GitHub's branch compare page shows the release against `master` at any time, with no pull request.
2. **No freeze rule (A4-W3, A4-S4).** Adopted: once the planned stories are merged, only `fix-` branches enter the release line until the pull request is merged. It costs the coordinator one refusal rule.
3. **Revert-then-redo needs a stated procedure (A4-W1, A4-S2).** I ran this in a scratch repo today (section 3, item 1). A4's finding is right: re-merging a story branch after `git revert -m 1` of its merge stops with a conflict (`DU s.txt`). But reverting the revert first and then merging the fixed branch is clean and yields both the story and the fix. So V1's risk 5 was a missing procedure, not a structural defect. Adopted rule: never re-merge a reverted story branch directly; either revert the revert and merge, or fix forward on a `fix-` branch. I do not move on `--no-ff` versus squash (C-005) because of this; see section 5.
4. **A wrong merge click on the release pull request is a real risk (A4 E4, release #658 squash-merged by mistake, reverted by #662, redone as #664).** V1 Q4 said "merge commit" but built no guard. Adopted: the pull request body says "merge commit only", and the closeout check reads the merge method. All three methods are allowed on this repository today (section 3, item 3), so nothing else stops the click. If a squash happens anyway the release is still one revertable commit on `master`; only the per-story merge commits inside it are lost.
5. **Review size and no outside gate (A2-W2, A2-W3, A3-W2, concessions 1 and 2 of my Round 1).** I stand on the concession. I narrow it with two facts below (section 3, items 2 and 6): the repository's own `integration` to `master` promotions are already release-sized (181 files for #664, 1,146 for #640 per A4 E4), so V2 and V3 also produce a large pull request at the end; and `test.yml` already has an unconditional `workflow_dispatch:` trigger, which can run the same suite on the pushed release line in GitHub's environment at any point without editing a trigger. That makes the coordinator's local run no longer "the only thing" (V1 Q2 prevention c). It is UNVERIFIED by a real run (a run is a GitHub write I was told not to make), and each run spends CI minutes, so it needs the owner's nod.

### Contested, with counter-evidence
6. **"Isolation is deferred, not removed; the collision lands on production first" (A2-W1, A3-W3).** It does not land on production. The release pull request is tested against `master`, and `master` only ever holds the dashboard-only state. A conflict at the later `master` into `integration` sync happens on a sync branch, not on `master`. The combination of dashboard plus Clay's unreleased work first exists on `integration`, which CLAUDE.md names as the testing branch, and first reaches `master` through the normal promotion with its own CI. So V1 does not skip the testing step; it moves it after landing, onto the branch built for it. The real cost is on Clay: his open pull requests may need rework after the sync. New mitigation (section 3, item 5): at each `master` merge-in and before the pull request, run `git merge-tree` of the release tip against `origin/integration`. It is read-only, imports none of Clay's work, and finds textual collisions at the earliest possible moment. This extends U-001 and U-003 and brings Clay-collision detection time close to V2's for textual clashes.
7. **"One large pull request" (A2-W3, A4-W10).** Both advocates point to #147 in GFxAI. The better local evidence is this repository: #640 and #664 landed as single large pull requests and stayed, and the failure was the merge click (A4 E4). Reviewers here already take roll-ups of this size. What V2 and V3 get is per-unit review before the roll-up, which I conceded; what they do not escape is the roll-up itself, since the `integration` to `master` promotion is one anyway, and it also carries Clay's work. V1's single pull request replaces that promotion for the dashboard, it does not add to it.
8. **"Self-conditional justification" (A2-W4).** Every variant states a fallback trigger: V2 ("first thing to test" the pilot), V3 ("if trains routinely run past the time box, move toward Proposal 2"), V1 (Q5). A stated exit is design hygiene, not a concession. I do take V3's stronger form of it (floating scope, section 4 Q5).
9. **"Merge-in housekeeping and a rebase-forbidden line" (A2-W6).** V1's housekeeping is one rule (merge `master` between story merges). V2 moves the same work onto every slice branch: each worker merges `integration` repeatedly while Clay and the owner keep moving it. The total is higher in V2, spread across more sessions.
10. **"Documented flow is `master <- integration <- feature`" (A2-S10, A3-S3).** V1 departs from CLAUDE.md here and I said so (my Round 1 concession 5). But the owner's stated model (CONTEXT line 7) is that the release merges to the default branch, and the repository's own flow is not strictly followed: `master` is 26 commits ahead of `integration` right now (section 3, item 5), maintainers sync by hand, and a wrong-method promotion has already happened (#658). A flow that already drifts is weak ground for ruling out a direct landing.
11. **"No per-story record on GitHub; the bots never see a story" (A2-W5).** True and accepted as cost. Findings the bots raise at the release pull request are fixed by `/sc:pr-submit --monitor 3` as commits on the release line. Attribution to a story is looser than in V3. I do not claim this is free.
12. **"Reverts of dependent stories are manual with no CI backing" (A3-W4).** Dependent reverts are manual in every variant that merges dependent stories. The only difference is CI on the revert result, and the dispatch trigger (point 5) supplies that on request.
13. **"The coordinator is a single point of failure" (A3's A-002 row, my own Round 1 concession 6).** With the push in point 1 and the ledger lines written before and after each merge (A4's table), a successor coordinator resumes by comparing the remote release tip with the ledger. This closes most of the gap A3 correctly said V3 has over V1.
14. **"V1 relaxes the merge-owner rule with no external check at all" (A3-A14 reason).** True. The difference I rely on is authority class, not checking: V1's merge is local into an unpublished or backup-only branch, reversible, and of the same kind as the worker contract's child-into-feature merge (CONTEXT line 9). V3 asks for authority to merge GitHub pull requests. V3's gate is stronger; V1's ask is smaller. A3 concedes V3 is no better than V2 without Decision A (A3-C1), and V1 has no such dependency.


## 2. Updated assessment of the other variants

### V2
- **Did not change my mind:** the owner is still the single merge lane (A2-C1 concedes it), the ledger still has no home (A2-C2), dark landing is still unproven (A2-C4), and shipping is still tied to Clay's state (A2-C3). A2 conceded these four, which are the four structural points I made against V2.
- **Changed my mind, partly:** A4 measured the owner's landing rate (about 6 commits a day on `master`, A4 E5), so A2-C1's "owner clicks every slice" is plausible at the current rate and I withdraw "throttled" as a flat claim. It remains the heaviest owner load of the four, and the load is one the owner would have to choose.
- **A2-S2 is right and I had missed it:** V2's CI trigger keys on the base branch (`integration`), so the Orca prefix cannot silently disable it. V1 shares that immunity (its only pull request targets `master`); V3 and V4-with-story-PRs do not.
- **A2-S3 and A2-S7 (earliest detection, no serial lane) are partly met by V1 now:** pre-merge `git merge-tree` against the release tip and against `origin/integration`, plus on-demand CI through `workflow_dispatch` on the pushed release line. They are still weaker than CI on every slice against the real `integration`. I do not call this a draw.
- **A2-W (against V1) points 2 and 5 have force:** I took the push and dispatch fix and the early-look compare page; point 3 I answered with the promotion-is-large-anyway fact.

### V3
- **What A3 settled against its own variant:** Decision A is a hard dependency (A3-C1), `master` fixes need a back-port (A3-C5), planning base moves (A3-C6), a top-level `/sc:pr-submit` session per story (A3-C10), and CI minutes grow with waiting stories (A3-C4). A3 also could not confirm where GitHub reads the workflow file (A3-C12), so V3's central claim (CI on every story pull request) still rests on an unverified step plus a throwaway test.
- **Strongest argument, which I take seriously:** A3-S2, the bulkhead: V3 relaxes the owner rule only for `train/*`, behind green CI and two settled reviewers. That is a stricter gate than V1's local merge. It does not change my view, because the stricter gate costs three owner decisions and a workflow edit before story one runs, and V1's dispatch route buys part of the same gate at one owner nod.
- **What I take from V3:** floating scope with a time box (U-010), the throwaway check before trusting any prefix or CI filter (U-013), and a short list of decisions put to the owner (U-012). All three are compatible with local merges.
- **A3's claim that V3 is "the reversible middle rung":** fair. It is also why V1's fallback to V3 stays in the design (section 4, Q5).

### V4
- **A4 dropped almost everything V4's original text claimed:** pull request per story (A4-C1), merging `integration` in (A4-C2), no base stated (A4-C3), ledger and planning base (A4-C4), the long-lived cap (A4-C7), cherry-pick hotfix copying (A4-C6). What remains is V1 plus four differences: the folder layout, squash, a freeze, and an acceptance gate. A4 says so itself.
- **Of those four I take two and a half:** the freeze (adopted); the release-line folder `release/<rel>` (adopted, section 4 Q1, because it gives one pattern for rulesets, clean-up and listing, and costs nothing: no `release/*` branch exists on the remote today); the acceptance gate only as "full local suite plus the single pull request's CI and bots", not the GFxAI tiers and two approvers, which A4-C9 itself says do not transfer.
- **Squash versus `--no-ff` I did not give up:** the trap A4 verified (A4 E2) is real and I reproduced it, but the revert-the-revert procedure removes the conflict (section 3, item 1). That leaves squash with one real advantage (simpler revert, no `-m 1`) against the loss of per-task commits that the ledger refers to (A4-C8 concedes the loss). It is a close call and the owner's.
- **A4's real-practice evidence has more weight than I gave it:** the #658 wrong-method incident is the one concrete branching failure in this repository's recent history, and it argues for a merge-method guard on the release pull request, which I adopt, more than for any naming or method choice.


## 3. New evidence not presented in Round 1

All read-only. Items 1 and 3 to 5 are my own runs today (2026-11-23); item 2 is a read of the workflow file.

1. **Re-merge after reverting a story merge (scratch repo under `/tmp`, removed after).** Setup: story branch adds `s.txt`; merged into the release line with `--no-ff`; merge reverted with `git revert -m 1`; story branch then gets a fix commit. Result A, direct re-merge: exit code 1, status `DU s.txt` (conflict). Result B, `git revert` of the revert commit first, then merge the story branch: exit code 0, `s.txt` holds both the original line and the fix. This confirms A4 E2 and shows the standard remedy works. Under the worker contract a conflict stops the coordinator, so the rule "revert the revert, then merge, or fix forward" must be written into the proposal.
2. **`.github/workflows/test.yml` lines 3 to 8:** triggers are `push` and `pull_request` for `[master, integration]` and an unconditional `workflow_dispatch:`. No job is gated on the event name (read the whole file, lines 1 to 200). So the same suite can be started by hand against any pushed branch that contains the file, with no trigger edit. UNVERIFIED by a real run (it would be a GitHub write). This is a candidate mitigation for the V1 and V4 "no CI before the end" gap, as A4 E7 also noted; it is not CI on a pull request, so no bot review comes with it.
3. **Repository merge settings, `gh api repos/IronbellyOrg/IronClaude`:** `allow_merge_commit true`, `allow_squash_merge true`, `allow_rebase_merge true`, `delete_branch_on_merge false`. Confirms A4 E6. A-006 is therefore settled: both methods are allowed per pull request, nothing stops a wrong click, and any variant relying on auto-delete (V2 section 3 step 4, V3 Q7) is relying on a setting that is off.
4. **Remote heads named `release/*` or `dash*`:** `git ls-remote --heads origin` with those patterns printed nothing. `release/dash1.3` and `dash1.3/*` are unused on the remote today. Local-only branches not checked.
5. **`git rev-list --left-right --count origin/master...origin/integration` printed `26 2`.** `master` has 26 commits `integration` lacks; `integration` has 2 `master` lacks (A4 saw `24 2` earlier, so the gap moves by hours). A release line cut from `integration` starts behind `master` by that gap; one cut from `master` starts at the branch it lands on. This supports C-002 and X-001 for V1 and V4.
6. **From A4 E4, used as an argument rather than re-measured:** this repository's own promotions (#640: 1,146 files; #664: 181 files) are release-sized pull requests that landed. Whatever V2 and V3 do per story, the owner still reviews a promotion of that size at the end, and in V2 and V3 it also contains Clay's work.

## 4. Combined design, question by question

Base is V1 (owner's model: release line, story sub-branches, coordinator merges locally, one pull request into `master`). Source of each piece is in brackets. Constraints honoured: no ref conflict, coordinator merges locally, pull requests only through `/sc:pr-submit`, CI only for pull requests and pushes into `master` or `integration`.

**Q1. Names.**
- Release line `release/dash1.3` [V4 folder, V1 idea]. Stories `dash1.3/s04-slug`, fixes inside the release `dash1.3/fix-01-slug` [V1], fixes on shipped code `fix/<issue>-<slug>` from `master` [V1, V2, V3; the repository already uses `fix/`, A4-C5]. Tag `dash-1.3` on the merge commit [V4; hyphen avoids any `dash/` folder reading].
- Invariant, written once: no branch is ever named `dash1.3` or `release` alone. Release and story folders are different (`release/` against `dash1.3/`), so they coexist (A4 E1, tested; my Round 1 claim for the layout stands). With an `ironbelly/` prefix both stay siblings if the prefix is uniform.
- Release tokens: write `1.10` as `1.100` if it ever arises, or sort by the ledger; "1.1" is a prefix of "1.105" and sorts first, as planned.
- Before first use: one throwaway `orca worktree create --branch ...` to see whether the name is kept or prefixed [V3 U-013]. This is the A-007 and A-011 check, once, for all variants.

**Q2. Where story work merges.**
- Locally, by the coordinator, into `release/dash1.3`, `--no-ff`, one story at a time [V1]. Before each merge: path claims checked (disjoint) and a read-only `git merge-tree` trial [V1 U-001]. After each merge: tests (full suite if it is fast, else affected tests; A-010 to be timed once), ledger line written before and after, release line pushed forward-only [new, section 1 point 1].
- Conflicts: the coordinator stops and reports; the story worker merges the release tip into its own branch and re-runs its gates; a clash of intent goes to the owner [V1, worker contract].
- Optional extra gate: the coordinator may start `test.yml` by `workflow_dispatch` on the pushed release line (owner to approve the CI minutes) [new, UNVERIFIED by run].
- No pull request per story. Where the owner wants an early look: the GitHub compare page of the pushed release line. If the owner wants per-story bot review anyway, that is the signal to move to V3 for that release, not to patch V1.

**Q3. Staying current.**
- Merge `origin/master` into the release line between story merges, at the start and before the pull request; merge only, never rebase [V1].
- Do not merge `integration` in (A-017 rejected by A2, A3, A4 and my own check). Instead run a read-only `git merge-tree` of the release tip against `origin/integration` at each `master` merge-in and before the pull request, and compare path claims with open `integration` pull requests at release start [V1 U-003, extended].

**Q4. How the release lands.**
- One pull request `release/dash1.3` into `master` by `/sc:pr-submit --monitor 3 --base master`, from a top-level session in the release worktree. Body: "Merge this pull request with a merge commit, not squash" [#658 incident], the per-story digest [V1 U-002], the path classes so reviewers can skip `.dev/` records [A-009]. Closeout checks the merge method actually used.
- Freeze from the last planned story merge: only `fix-` branches enter until the owner merges [V4].
- Size: story-count cap set when the release is planned; the owner decides the number. Size is a stated risk, not a solved one.

**Q5. Flags, trunk, justification.**
- No flags. The line is justified by explicit versioned releases (S3, S8) and a hard cap: days, not weeks, one week at most [V1].
- At the cap, scope floats: unmerged stories ride the next release rather than extend this one [V3 U-010]. If caps are routinely missed, move that release to V3 (per-story gate), and if that overruns too, to V2 slicing [V1 Q5, V3 Q5].

**Q6. Hotfixes and bug fixes.**
- Shipped bug: `fix/<issue>-<slug>` from `master`, pull request into `master`; the open release gets it at the next `master` merge-in. No cherry-pick, no copying [V1; A4-C6 agrees].
- Bug inside the release: `dash1.3/fix-NN-slug`, merged locally like a story.
- 1.1 bug-fix and 1.105 test-only releases: ordinary release lines. A one-story release: plain `fix/` or `feat/` branch and one pull request [V1].

**Q7. Clean-up and records.**
- Story branch and worktree: removed after the merge is in the ledger and the release line is pushed (the push is what makes removal safe, A4-W2). The story tip stays reachable as second parent.
- Release line: after the owner merges and the sync pull request is open, the coordinator deletes the local and remote branch and the worktree. Explicit deletion is mandatory because `delete_branch_on_merge` is false (section 3, item 3) [V4 C-023 rule, V1 step 6]. Tag the merge commit.
- Records: `.dev/` records and `sprint-status.yaml` on the release line, landing on `master` with it [V1].

**Q8. Fit with `integration` and Clay.**
- Clay unchanged during the release. After landing, the coordinator opens the `master` into `integration` sync the way maintainers already do it by hand (A4 E4: five "merge master into integration" commits in three days; exact mechanism UNVERIFIED). Release-line clean-up waits for that sync to be open [V1, V4]. Collision cost lands on Clay's open pull requests after the sync; the early warnings in Q3 reduce it.

**Q9. Failure and rollback.**
- Bad story inside the release: `git revert -m 1 <story merge>`, or fix forward. If the reverted story must return, revert the revert first, then merge the fixed branch; never merge the reverted branch directly (section 3, item 1). Dependent stories revert in reverse order.
- Release fails on `master`: revert pull request of the release merge commit through `/sc:pr-submit`; prefer a bug-fix release line over re-landing. If the release was squashed by mistake, the same revert still removes it as one commit.
- Mistaken merge method: handled by the Q4 body text and closeout check, not by repository settings.


## 5. Per diff point positions (contested points)

Confidence is my probability that the winner is the right call for this repository, after Round 1 and section 3. Winners are V1, V2, V3, V4 or "combined" (the section 4 design takes pieces from several).

| Point | Winner | Conf. | Reason |
|-------|--------|-------|--------|
| C-001 names | Combined: V4 release folder, V1 story names | 60 | All four are valid; flat names (V2, V3) are the most robust and I concede that. The `release/` folder gives one pattern for rulesets and clean-up (free today, section 3 item 4); two-level story names keep the owner's `dash1.3/...` shape. A4 E1 verified coexistence. |
| C-002, X-001 base branch | V1 (and V4 once it says so) | 85 | `master` is 26 ahead of `integration` today (section 3 item 5); the line lands on `master`; ledger and planning base stay (X-009). A4 conceded. A2 and A3 still contest. |
| C-003, X-002 landing path | V1 and V4 | 75 | The owner's model; no Clay work in the release; the promotion that V2 and V3 end with is a release-sized pull request anyway (section 3 item 6). Contested by A2-S10 and A3-S3 on the documented flow: real cost, answered in section 1 point 6 and 10. |
| C-004 where story work merges | V1 | 60 | Existing worker-contract mechanism, smallest ask. V3's per-story pull requests give a real gate but need the workflow edit, Decision A, and unverified bot behaviour (A3-C12). |
| C-005, X-004 merge method | V1, narrowly | 55 | Trap verified and its remedy verified (section 3 item 1). Squash is simpler, `--no-ff` keeps the per-task trail. The owner's call; I say so rather than claim more. |
| C-006, X-005 merge guard | V1 | 60 | Local merge into a backup-only branch is a smaller authority than merging GitHub pull requests (section 1 point 14). Owner confirmation still required (CONTEXT line 11, "to be confirmed"). |
| C-007 CI and reviewers per story | V2 | 70 | V2 has real CI and both bots per slice with no edit. V1 with dispatch has CI on demand but no bot review. V3 and V4 need the edit. |
| C-008 staying current | V1 | 80 | Merge `master` only; V4 conceded; V3 pays a weekly merge-in; V2 has no line but per-slice merge-ins. |
| C-009, X-007 rebase | V1 | 70 | One invariant, no carve-out. Low stakes. |
| C-010 conflict procedure | Split V1 and V3 | 50 | V1 routes through coordinator then worker; V3 adds the sync branch (U-011), a good mechanism I do not need while there is no `integration` merge-in. |
| C-011 collision control | Split: V2 and V3 on latency, V1 on pre-merge guards | 65 | Added: `git merge-tree` against the release tip and `origin/integration`; dispatch CI on request. |
| C-012 incomplete-work isolation | V1 with V3's rule | 65 | No flags; floating scope at the cap. V2's dark landing is unproven (A2-C4). |
| C-013, X-006 justification | Combined: V1 line, V3 time box | 65 | V3's "scope floats, time does not" is the better rule; the line stays because the owner's model and the ledger need it (A4 agrees). |
| C-015 hotfix back-port | V1 | 85 | No cherry-pick, no back-port step; A4-C6 conceded. |
| C-016 bug fix inside a release, freeze | V4 | 75 | Freeze adopted. |
| C-018 coupling to Clay | V1 | 85 | Conceded by A2-C3, A3-C3, A4-C2. |
| C-019 sync obligation | V1 and V4 | 55 | V3 has the smaller obligation (A3), but the owner's model lands on `master`; sync is the price. Who runs it is still UNVERIFIED. |
| C-020, X-009 ledger and planning base | V1 | 90 | Conceded by A2-C2 and A3-C6, and A4-C4. |
| C-021 release size at final review | V2 and V3 | 60 | Per-unit review is smaller; but the promotion pull request is large in V2 and V3 too (section 3 item 6). I keep the cap, digest and freeze. |
| C-022 rollback | V1 at release level, V2 at slice level | 65 | One release merge commit with no Clay work inside it; story revert with the tested redo procedure; V2's flag-off is finer where it is possible. |
| C-023 clean-up | V1 and V4 | 85 | Both delete explicitly; V2 and V3 rely on `delete_branch_on_merge`, which is false (section 3 item 3). |
| C-024 tag | V4 (`dash-1.3`) | 55 | Same value as V1 with no `dash/` folder; trivial. |
| X-003, A-017 | V1 | 95 | Tested by A4 E3; A2, A3, A4 all reject A-017. |
| X-008 (V4 internal) | Not contested | n/a | A4 resolved it by dropping story pull requests (A4-C1). |
| X-010, C-025 stacks | Not contested | n/a | V1 has no pull requests to stack. |
| U-001 to U-003 | V1 unique, keep | 80 | Extended with merge-tree against `origin/integration`. |
| U-010, U-012, U-013 | V3, adopt | 75 | Time-boxed floating scope, owner decision list, throwaway check. |
| U-014, U-015, U-017 | V4, adopt | 65 | Provenance marks in the merged text; PR #147 plus #640 and #664 as size evidence; the "no agent merge to the default branch" wording for what is relaxed. |
| U-018 | V4 in part | 50 | Release pull request gate = full local suite, pull request CI and bots, owner; not the GFxAI tiers or two approvers (A4-C9). |
| U-006 to U-009 | V2, not adopted in the base | 60 | Slicing and dark landing stay as the third-rung fallback (Q5). |
| A-006 | ACCEPT (changed from QUALIFY) | 95 | Verified: all three merge methods allowed, section 3 item 3. |
| A-008, A-012, A-013 | ACCEPT, unchanged | 80 | Only V3 and V4-with-story-pull-requests carry them. |
| A-005, A-010 | QUALIFY, unchanged | 70 | Still unmeasured by anyone; time the suite once and measure dashboard coverage before the first release. |
| A-003 | QUALIFY, updated | 65 | A4 E5 shows the owner lands about 6 commits a day, so click volume is not impossible; large-diff review is the V1 and V4 cost. |

Not contested by me: S-001 to S-006 (document form), C-014, C-017, C-025, X-008, X-010.

