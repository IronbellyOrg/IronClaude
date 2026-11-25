# Round 2 rebuttal: advocate 3 (Variant 3, release train, backend persona)

Written 2026-11-23. Read: round1-advocate-1.md to round1-advocate-4.md, round2-advocate-1.md, round2-advocate-2.md. Citation style: A1-W2 is advocate 1's weakness 2 (Round 1 list), A2-S3 is advocate 2's strength 3, A4-C1 is advocate 4's concession 1, A1R2-6 is point 6 of advocate 1's Round 2 section 1, N3 is advocate 2's Round 2 evidence item 3. My own Round 1 points are R1-S (strength), R1-W (weakness), R1-C (concession). Every number labelled "E" below comes from a read-only command I ran today (section 3). Nothing was written to GitHub or git. Anything not confirmed is marked UNVERIFIED.

## 1. Response to criticisms of Variant 3
### Conceded because the evidence forces it
1. **Cut from `integration` and landing through it are wrong for this repository (A1-W12, A4-W5, A4-W6, A2R2 point 1; C-002, C-003, X-001, X-002).** `integration` is 26 commits behind `master` and 2 ahead (E1), has had 24 PRs in its life against 460 into `master` (E1), and advocate 2's N1 says none merged since 2026-11-19. My R1-S3 (collisions with Clay found before `master`) and half of R1-S2 rested on `integration` being the live trunk. It is not. I withdraw both as differentiators and give C-002, C-003, X-001, X-002 to V1. This also removes my own cost of moving the BMAD planning base (X-009, R1-C6): cut from `master` and planning does not move.
2. **"V1 fails on production, V3 fails in a cheap place" (R1-S3, R1-W3) was overstated (A1R2-6).** The sync happens on a sync branch and then on `integration`, not on `master`. Withdrawn.
3. **Durability of V1 (R1-W1).** A1R2-1 adopts a forward-only push of the release line after each story merge. That removes the single-copy risk; it is no longer a V3 advantage.
4. **The package of three owner decisions is too much (A1-W7, A2-W7, A2R2 point on constraints).** Decision A (merge authority over GitHub PRs) is avoidable, see the mechanism below. Decision C (edit `test.yml`) is only needed if the owner wants CI, not only bots, on story PRs. Only Decision B (time box) stays. As a full package V3 asked for more than it needed to.
5. **Clean-up (R1-C, A4-S6, A2R2 point 6; C-023).** My Q7 relied on "Automatically delete head branches", which is off (A1R2 section 3 item 3 and A2 N8). Explicit deletion is mandatory. Conceded to V1 and V4.
6. **Merge commits "avoid the reverted-merge trap" (R1-S6).** I only flagged it UNVERIFIED. A4 E2 and A1R2 section 3 item 1 show the trap is real and the remedy (revert the revert, then merge) works. V3 holds no advantage over V1 here, and squash (V2, V4) is simpler. C-005 has no winner from me.
7. **Stacks (A1-W9, C-025, X-010).** Weak under current CI; with local merges there is nothing to stack. Dropped.
8. **Review load of two bot passes per story plus roll-up (A4-W9, A2-W10).** True, and it is the largest real V3 cost. I answer it by making per-story PRs selective (Q2 below), not universal.
9. **The time box is unset (A2-W12).** True. I give a measured starting point in Q5; the owner sets it.

### Contested, with evidence
10. **"Per-story CI and review rest on unverified third parties" (A1-W8, A1R2 point 5).** The bot half is now verified in this repository: both bots reviewed 5 of 5 story PRs into a batch branch (E2). The CI half is verified absent (E2: 0 checks), exactly my R1 risk 5. So V3's feedback loop is bots today and bots plus CI after one edit or one dispatch run (E6, E7). A1's "no better than V1 until the throwaway passes" is false for bots.
11. **"A roll-up of 181 or 1,146 files merges in 17 to 43 minutes, so reviewers take roll-ups" (A1R2 point 7 against A2R2 point 10).** I side with advocate 2's reading: a fast merge of a huge diff shows it was not read. E3 and E4 are in-repository evidence: per-story review produced a follow-up fix before any roll-up (#490 then #491), while the ten unreviewed story PRs of `feat/tdd-spec-merge` ended in one 2,089-file landing (#31).
12. **"V3 asks for authority to merge GitHub PRs; V1's ask is smaller" (A1R2 point 14, A1R2 section 5 C-006).** Right about the authority class, wrong that it forces Decision A. Mechanism: the story's worker runs `/sc:pr-submit --monitor 3 --base release/dash1.3` for review only; when the bots have settled, the coordinator merges locally with `--no-ff` as V1 does and pushes the release line. GitHub marks a PR merged when its head commits become reachable from the base by a push (general GitHub behaviour; UNVERIFIED here, one throwaway test settles it). The coordinator never clicks merge on GitHub, the owner's standing rule holds, and "the coordinator merges locally" holds.
13. **"V3 couples the release to promotion cadence" (A1-W10).** True of V3 as I wrote it, moot once the line is cut from and lands on `master`. The weekly merge-in cost does not vanish: it becomes `master` merge-ins, which advocate 1 also pays.
14. **"Isolation is a bulkhead only if Clay promotes at his own timing" (A2R2 point 4).** Agree with N2's facts: two promotions in about 36 hours at Clay's timing. That is an argument against V2, and it supports a private release line, which V3 and V1 share.

## 2. Updated assessment of the other variants
### V1
**Changed my mind:** base and landing (`master`, one PR, merge commit), the forward-only push (A1R2-1), the freeze (A1R2-2), the merge-method guard in the PR body after #658 (A1R2-4), the `git merge-tree` trial against `origin/integration` (A1R2-6) and the rule that a reverted story is never re-merged directly (A1R2 section 3 item 1). V1 plus these is the right base, and I say so as the V3 advocate.
**Did not change my mind:** (a) V1 still has no outside review of any single story, and `workflow_dispatch` (E6) gives CI on request but no bot review; E2 shows the bots do review story PRs into a batch branch, so V1 gives up something that works today. (b) A1R2 point 7 asks us to treat past large roll-ups as reassurance; E4 reads the other way. (c) A1's answer to "who gates a story" is "the coordinator's run plus the final PR", which for a 25-file, 4,636-line story (#490) is thin.

### V2
**Changed my mind:** V2 is not a candidate base: `integration` is not a live trunk (E1, N1, N3), the ledger has no home, and dark landing is unproven. A2 conceded all of that and I agree.
**Did not change my mind:** V2 is still the only variant with per-change CI and bots with no configuration at all. Its principle (a change is judged by something other than the coordinator) is what V3's optional PR layer borrows, for bots only unless the owner approves a CI edit or dispatch runs.

### V4
**Changed my mind:** A4 reduced V4 to V1 plus four items, and A1R2 section 2 adopted two and a half. I take the same: the freeze (C-016), the explicit clean-up rule with the forward-only push (C-023) and the `release/<rel>` folder as one pattern for listing and rulesets. U-017's wording ("no AI merge to the default branch") is the clean statement of what the owner rule means: the coordinator never merges into `master`, and the local merge into the release line is a separate class.
**Did not change my mind:** squash is not clearly better for local coordinator merges (A4-S2): the trap has a tested remedy, and `--no-ff` keeps per-task commits that the ledger refers to (A1-S10). It is the owner's call and I do not claim it.

### What the three Round 1 and two Round 2 statements jointly settled
A-017 is rejected by all four of us (X-003: V1 right). `integration` must not be merged into the release line. Ledger and planning base stay with V1 (C-020, X-009). Hotfixes need no back-port step (C-015). All three merge methods are enabled and auto-delete is off (A-006, C-023). The only open items are bot and CI treatment of story PRs, merge method for stories, and the story cap.

## 3. New evidence not presented in Round 1
All read-only (`gh pr list`, `gh pr view`, `gh api` timeline, `git rev-list`, `git log`, `git show`, one web search). Date 2026-11-23.

**E1. Where this repository's 506 PRs point (gh, all states, limit 1000).** Base `master` 460, `integration` 24, and 22 others: `feat/tdd-spec-merge` 10, `346Claude-integration` 5, and one each for `346GPT-integration`, `Ironbelly/IBv1.4`, `clayphi/v61-pr1-doc-skills`, `fix/v2.20-WorkflowEvolution`, `scratch/361-base`, `scratch/361-live-20261109-0239-base`. So the V3 shape (many PRs into a batch branch) is not new here: it has been done twice, once in March to May 2026 and once on 2026-11-10 and 11. `git rev-list --left-right --count origin/master...origin/integration` prints `26 2`, same as advocate 1 and 2.

**E2. What happened on PRs into a batch branch (gh pr view, PRs #484, #490, #491, #492, #493 into `346Claude-integration`).** Check runs: 0 on every one of the five. Augment (`augmentcode`) left a review on all five. Codex (`chatgpt-codex-connector`) left a review or a comment on all five (reviews on #484, #490, #493; comments on #491, #492). Sizes 5 to 25 files, +83 to +4,636 lines. This settles A-012 for this repository and for non-default bases: both bots do review a PR whose base is a batch branch. It also confirms my own risk 5 and A-008: with the current `test.yml` such a PR gets no CI.

**E3. A per-story review loop produced a fix before the roll-up.** #490 ("live 7-reviewer panel", 25 files, +4,636) merged 2026-11-11 03:12; #491 is titled "fix(review): address #490 review findings" and merged 05:46 the same day, both into the batch branch. I did not read the findings, so how serious they were is UNVERIFIED; the sequence shows review feedback landing on a small PR instead of inside one large final diff.

**E4. The roll-up and the big-bang in the same repository.** #497 (`346Claude-integration` into `master`, 58 files, +6,162) is CLOSED, not merged; why is UNVERIFIED. #31 (`feat/tdd-spec-merge` into `master`) is 2,089 files, +318,059 and merged 2026-05-12 after ten story PRs into that batch branch; the four of those I sampled (#20, #21, #27, #30, 6 to 147 files) have zero check runs, zero reviews and zero comments. That is this repository's own evidence for the V1 and V4 failure shape (a batch with no gate, then one landing), and it complements advocate 4's GFxAI #147.

**E5. #474 is not CI on a batch base.** #474 shows 6 passing checks but its base was changed (`base_ref_changed`, 2026-11-09 19:16:45Z) to `346GPT-integration` after opening, and the filter is `[master, integration]`; the checks most likely ran while the base was `master` (inference). I do not count it as evidence that CI runs on a batch base.

**E6. The workflow today.** At `80f361804` (the last edit to `test.yml`, 2026-11-05, #402): `push` and `pull_request` both `branches: [master, integration]`, plus an unconditional `workflow_dispatch:`.

**E7. Where GitHub reads the workflow file for a `pull_request` run (A-008).** Web search today: Mergify's migration page says "A `pull_request` run uses the workflow file from the pull request's merge commit", and a GitHub community thread says the version that runs "is always github.sha", the merge ref. These are secondary sources; GitHub's own events page, which I fetched in Round 1, did not state it. Consequence if true: the one-line `branches` edit can be the first commit on the release line itself, so a story PR into that line (whose merge ref contains that tip) uses it. Nothing needs to change on `master` or `integration` before the release starts. Settle with one throwaway PR.

## 4. Combined design, question by question
Base: V1 (owner's model: release line, story sub-branches, coordinator merges locally, one PR into `master` by `/sc:pr-submit`). V3 contributes one optional layer and three rules. Constraints honoured: no ref conflict (Q1), coordinator merges locally (Q2), PRs only through `/sc:pr-submit`, CI only for PRs and pushes into `master` or `integration` is left as it is (Q2 shows the two ways to get CI without relying on that changing).

**Q1. Names.** Release line `release/dash1.3` [V4, V1, V2 agree]. Stories flat: `dash1.3-s04-<slug>`; in-release fixes `dash1.3-fix<NN>-<slug>` [V2, V3]. Shipped-code fix `fix/<issue>-<slug>` from `master` [all]. Tag `dash-1.3` [V4]. Why flat for stories: advocate 2's point (A2R2 Q1) that Orca names a branch `ironbelly/<worktree name>` is correct as far as it goes (49 remote branches have that shape, N5): a worktree called `dash1.3` would make `ironbelly/dash1.3`, and `ironbelly/dash1.3/s04-...` would then hit the exact "cannot lock ref" error in CONTEXT line 8. Flat story names cannot, with or without the prefix. I drop my own `train/` word; `release/` is the same idea with an existing name. Check once with a throwaway `orca worktree create --branch` [U-013]. If the prefix is added, any filter on `release/**` must also match `*/release/*`.

**Q2. Where story work merges.**
- Default, as V1: the coordinator merges each settled story locally into `release/dash1.3` with `--no-ff`, one at a time, after path claims and a read-only `git merge-tree` trial [V1 U-001, U-003]; ledger line before and after; forward-only push of the line after each merge [A1R2-1].
- V3's optional layer, per story, chosen at planning: **review-only story PR**. The story's worker runs `/sc:pr-submit --monitor 3 --base release/dash1.3`; Augment and Codex review it and the monitor fixes confirmed findings, as in #484 to #493 (E2, E3). When the bots have settled, the coordinator merges locally (not by a click on GitHub) and pushes; the PR then shows merged (UNVERIFIED, one throwaway test). This keeps "coordinator merges locally" and removes my Decision A. Use it for a story flagged risky in its spec or larger than a threshold the owner sets; my suggestion, not a measurement: about 15 files or 1,000 added lines (#490 was 25 files, +4,636 and produced a follow-up fix, E3; #484 was 8 files, +217).
- CI for those story PRs, two routes, owner picks: (a) one-line `branches` edit as the first commit on the release line, so each story PR's merge ref carries it (E7, UNVERIFIED; revert that commit before the release PR if the owner does not want `release/**` kept); (b) no edit: the coordinator starts `test.yml` by `workflow_dispatch` on the pushed line (E6; advocate 1's idea). Route (a) gives CI on the PR itself, (b) gives CI on the line only.
- Conflicts: coordinator stops and reports, the story worker merges the release tip into its branch and re-gates [V1, worker contract]. No `dash1.3-sync<N>` branch needed, since `integration` is not merged in (U-011 kept in reserve).

**Q3. Staying current.** Merge `origin/master` into the line at the start, between story merges and before the release PR; merge only, never rebase [V1]. Never merge `integration` (A-017). At each `master` merge-in run `git merge-tree` of the line against `origin/integration` and compare path claims with open `integration` PRs [V1 U-003, A1R2-6]. Merge-in cost is real because `master` moves at the owner's pace (about 5.7 merged PRs a day, A2 N1).

**Q4. How the release lands.** One PR `release/dash1.3` into `master` by `/sc:pr-submit --monitor 3 --base master`, merge commit only, written in the PR body, method checked at closeout [#658; A1R2-4]. Body: per-story digest [V1 U-002] and path classes. Freeze after the last planned story: only `-fix` branches enter [V4]. Where stories had review-only PRs, the release PR's bot pass is the second look at a diff already reviewed in parts, which is where the two-bot duplication in A4-W9 is paid; that is why the PR layer is selective.

**Q5. Flags, trunk-based, justification.** No flags. Long line justified only while short: time box with floating scope [V3 U-010]: when the box ends, stories not yet merged ride the next release. Starting numbers for the owner to accept or change, from advocate 2's estimate and V1's cap: about six stories or seven days, whichever comes first. Escalation ladder, as both neighbours state: if the box is missed twice, per-story PRs for every story (the V3 layer for all); if still missed, slicing and direct PRs (V2, third rung, only after its pilot, U-009). Bug-fix (1.1) and test-only (1.105) releases: A2R2's rule fits: small direct PRs into `master`, no line, when there is no behaviour to isolate.

**Q6. Hotfixes and bug fixes.** V1 unchanged: `fix/<issue>-<slug>` from `master`, PR to `master`, the open line picks it up at the next `master` merge-in; no cherry-pick, no back-port step [V1, C-015]. In-release bug: `dash1.3-fix<NN>-<slug>` merged like a story.

**Q7. Clean-up and records.** Explicit deletion, because auto-delete is off (A1R2 section 3 item 3; A2 N8). Story branch and worktree after the merge is in the ledger and the line is pushed; line, worktree and remote branch after the owner merges and the `master` into `integration` sync PR is open; tag. `.dev/` records and `sprint-status.yaml` stay on the line [V1; C-020]. The story tip stays reachable as second parent.

**Q8. Fit with `integration` and Clay.** V1 unchanged: Clay unaffected during a release; after landing the coordinator opens the sync PR; early warning by Q3's `git merge-tree` and path claims. Ask the owner one question the data raises (A2R2 Q8): is `integration` still the branch Clay works from, given 24 PRs in its life and none merged since 2026-11-19 (E1, N1)? The answer decides whether the sync PR carries 26 unrelated commits.

**Q9. Failure and rollback.** Story bad in the line: `git revert -m 1 <story merge>`; to bring it back, revert the revert first, then merge the fixed branch, never re-merge the reverted branch directly [A1R2, A4 E2]. A story that was reviewed by PR keeps its PR record on GitHub. Release fails on `master`: revert PR of the release merge commit; prefer a fix line over re-landing. Layers: story revert inside the line, release revert on `master`.

**What the owner must decide (one list).** (1) Confirm local coordinator merges into the release line (CONTEXT line 11, "to be confirmed"). (2) Story cap and time box. (3) Whether to use review-only story PRs, with which size or risk rule, and whether CI on them is by a first-commit edit or by dispatch. (4) Is `integration` still in use.

## 5. Per diff point positions (contested points)
"Winner" is the variant, or the combination, whose answer I would put in the merged proposal for this repository under the owner's constraints. Confidence is my probability that the winner is right.

| Point | Winner | Conf. | Reason |
|---|---|---|---|
| C-001 names | Combined: V4/V1 `release/<rel>` folder, V2/V3 flat stories | 70 | Orca prefix plus the owner's own token `dash1.3` reproduces CONTEXT line 8 for folder-style stories (N5); flat names cannot (A2R2 Q1). Folder for the release gives one pattern. |
| C-002, X-001 base branch | V1 (`master`) | 90 | E1: `master` 26 ahead of `integration`; four advocates now agree. I concede my R1 position. |
| C-003, X-002 landing path | V1 | 85 | Owner's model; `integration` is not the live trunk (E1, N1). Conceded. |
| C-004 where stories merge | V1 default, V3 review-only PR as optional layer | 60 | Local merge fits the constraints; E2 and E3 show bot review of story PRs into a batch branch works here today and found follow-up work. |
| C-005, X-004 merge method | No winner (owner's call) | 50 | Trap and remedy both verified (A4 E2, A1R2 3.1). Squash simpler; `--no-ff` keeps the per-task trail. I withdraw my R1 claim. |
| C-006, X-005 merge guard | V1 | 65 | Local merge into a pushed line is the smaller authority; the review-only PR layer does not need Decision A. Owner confirmation still needed. |
| C-007 per-story CI and reviewers | V2 for CI; V3-layer for bots, tie otherwise | 60 | Bots on a non-default base verified (E2). CI on a batch base absent today (E2), needs the first-commit edit (E7, UNVERIFIED) or dispatch (E6). V2 has both with no edit. |
| C-008 staying current | V1 | 85 | `master` only. V4 and V2 concede; my `integration` merge-in is withdrawn. |
| C-009, X-007 rebase | V1/V3 (merge only) | 75 | One rule, no carve-out. Low stakes. |
| C-010 conflict procedure | V1 | 60 | No `integration` merge-in, so no train-versus-`integration` conflict; U-011 only in reserve. I concede the point I claimed as a win in R1. |
| C-011 collision detection latency | V2 for CI latency; V1 pre-merge guards; V3 layer adds bots | 60 | Same suite behind all of them (A-005); `git merge-tree` is the best pre-merge guard (U-001). |
| C-012 incomplete-work isolation | V1 with V3's time box | 75 | No flags; floating scope at the cap [U-010]. V2 dark landing unproven. |
| C-013, X-006 justification | Combined: V1 line, V3 time box and ladder | 75 | Both neighbours point to the same ladder (A1R2 Q5, A2R2 Q5). |
| C-015 hotfix and back-port | V1 | 85 | No back-port step. Conceded. |
| C-016 freeze | V4 | 70 | Adopted. |
| C-018, X-003 Clay coupling | V1 | 90 | Conceded. |
| C-019 sync obligation | V1 and V4 | 55 | Sync is the price of landing on `master`; who runs it is UNVERIFIED (A-015). |
| C-020, X-009 ledger and planning base | V1 | 90 | Conceded; cutting from `master` removes my X-009 cost. |
| C-021 release size at final review | V3 layer on selected stories, plus V1's cap and digest | 60 | E3, E4: in-repository evidence for per-unit review before a roll-up; roll-up merge times (17 to 43 min, N2) show a roll-up is not where depth comes from. |
| C-022 rollback | V1 at release level; V2 at slice level | 65 | Same as advocates 1 and 2. I claim no V3 edge. |
| C-023 clean-up | V1 and V4 | 90 | Auto-delete is off; explicit deletion. Conceded. |
| C-024 tag | V4 (`dash-1.3`) | 55 | Trivial. |
| C-025, X-010 stacks | No winner | n/a | Nothing to stack with local merges. Dropped. |
| X-008 (V4 internal) | Not contested | n/a | A4 resolved it. |
| U-001 to U-003 | V1, adopt | 80 | With `git merge-tree` against `origin/integration`. |
| U-010 time-boxed floating scope | V3, adopt | 85 | Both advocates 1 and 2 adopt it. |
| U-011 sync branch | V3, reserve only | 60 | Needed only if `integration` is merged in, which it is not. |
| U-012 owner decision list | V3, adopt | 80 | Section 4 ends with one. |
| U-013 throwaway test PR | V3, adopt | 90 | It now has three jobs: Orca prefix (A-011), merged-by-push status (section 4 Q2), workflow file read for a PR into the line (E7). |
| U-014, U-015, U-017 | V4, adopt | 65 | Provenance marks; sizes from E4 and GFxAI #147; U-017 as the wording of what the owner rule forbids. |
| U-006 to U-009 | V2, third rung only | 55 | After a pilot. |
| A-008 | QUALIFY, improved | 60 | E7 (secondary sources): the filter edit can be the line's own first commit. Settle with the throwaway PR. |
| A-012 | ACCEPT (changed from QUALIFY) | 90 | E2: both bots reviewed 5 of 5 PRs into a non-default base. |
| A-013 | QUALIFY | 75 | Only needed if per-story CI is wanted; dispatch (E6) is the no-edit route. |
| A-014 | QUALIFY, narrowed | 65 | The review-only PR layer needs no relaxed rule; only the local line merge does (CONTEXT line 11, "to be confirmed"). |
| A-006 | ACCEPT (changed from QUALIFY) | 95 | All three methods are enabled; nothing stops a wrong click (#658). |
| A-004 | QUALIFY, unchanged | 65 | With local merges the serial-lane cost of per-merge CI re-runs mostly disappears; bot reviews on PRs are parallel. Still revisit above about four parallel stories. |

Points I no longer contest: S-001 to S-006, C-014, C-016, C-017.
