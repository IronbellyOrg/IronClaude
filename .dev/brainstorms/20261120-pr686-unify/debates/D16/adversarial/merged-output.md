# D16 unified prevention package

<!-- Provenance: produced by /sc:adversarial; Base: Variant 1 (OURS); Merge date: 2026-11-20 -->

Written 2026-11-20 for debate D16 (prevention package after the PR 681, 682 and 686 collision in `IronbellyOrg/IronClaude`). "They" means Clay (`clayphi`); "the owner" means `ironbelly`, the repository owner and the only repository admin. Every figure comes from the debate files in this folder; anything those files mark UNVERIFIED is marked UNVERIFIED here. All costs are estimates, none measured.

## Claim

<!-- Source: Base (original, modified) - reframed per Change #1: text alone does not bind; the prevention claim is conditional on the throwaway test -->

The incident (PR 681, Clay's design, and PR 682, Clay's deletion of the code of the owner's merged PRs 584 and 591, both merged by their own author on 2026-11-20 with no human review) happened because nothing in the repository made a second person say yes.

Text alone does not bind. PR 681's body already said "the owner reviews and merges", and its author merged it about 90 minutes after opening it. PR 683 was self-merged by the same author about 75 minutes after 681 and 682 merged (INV-019). A written agreement alone also repeats the 2026-10-22 pattern: a rule told in a meeting and never written (issue 290).

The unified package therefore has four parts:

1. Words in the file every session reads (root `CLAUDE.md`).
2. One admin ruleset on `master` and `integration`, with `.github/CODEOWNERS` on a short path list and a sole code owner, `@ironbelly`.
3. One decisions file, `docs/decisions.md`.
4. A direct hold on the open 655 series (PRs 686 and 690).

Only part 2 is a mechanical block. Whether it blocks the incident input has not been shown, because GitHub's documentation is silent on an author who is himself a listed code owner at 0 required approvals (INV-007). So "this package would have prevented 681 and 682" is stated here as "probably, UNVERIFIED" until the throwaway test in `## Test protocol and fallbacks` passes (INV-007, INV-026, INV-027). The text parts add no prevention of their own (INV-026).

The package is a narrowed form of the nine items of FULL-REPORT section 11. What was cut, and why, is in `## Dropped items and why`.

## Mechanism

<!-- Source: Base (original, modified) - three layers kept; layer 1 carrier and layer 3 contents replaced per Changes #2 to #6, layer 2 per Changes #8 and #9 -->

Three layers, each catching what the one below misses, plus a direct hold on the open series. Layer 3 is the only layer a session cannot skip, and it is the only one that has not yet been tested on this repository.

### Layer 1: words in the files sessions read

<!-- Source: Base (original, modified) - carrier moved from CONTRIBUTING.md to root CLAUDE.md per Change #2 (Variant 2 (CLAY) Round 1 A-002, accepted in both Round 2 papers) -->

Where the words go:

| File | What goes there | Why |
|---|---|---|
| Root `CLAUDE.md` | The source text: a new section "who rules, and what needs a second person" (about 12 lines) | Read at session start by every session; edited in 7 of the last 100 merged PRs; the PR-target rule already lives there for the same reason. Whether sessions obey a root `CLAUDE.md` rule: UNVERIFIED |
| `HOW-WE-WORK.md` | A two-line pointer to that section | The owner's 2026-10-29 answer on issue 290 puts rules there; the owner can rule otherwise in chat. A pointer avoids two copies drifting. It is not two lines of work: the file needs a byte copy to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and a level-table copy into `src/superclaude/core/CLAUDE.md`, with tests checking both (about 15 more minutes; the file is edited in 22 of 100 PRs, so conflicts are likely) |
| `CONTRIBUTING.md` | One line pointing to the section | Cold file (0 edits in 100 PRs); humans read it, sessions do not |
| `.github/PULL_REQUEST_TEMPLATE.md` | Two reminder lines, not counted as a control | Reached 14 of 100 PRs and 0 of the last 79; `/sc:pr-submit` never mentions it; a PR opened with `--body` replaces it |

The two template lines:

- `Related work (include unpushed plans and other repositories):`
- `Deletes or rewrites code merged in the last 30 days: yes or no, whose, and where their written yes is.`

<!-- Source: Variant 2 (CLAY), Round 2 Part 2 R-2 and R-4 and Round 1 rule text; Base (original), Mechanism layer 1 - merged per Change #3 -->

Rule text content (the section in root `CLAUDE.md`):

1. Roles by login: the owner of the repository and of design rulings is `ironbelly`, pending the owner's chat decision 1 in `## Decisions the owner gives in chat`. `IB-JonathanB` is not named anywhere until they agree in an issue comment.
2. A question to a named person gets a written answer. Silence is never a yes.
3. Three working days is a timer to ask again, never permission. After three working days the author asks again in the same thread, by name, and on the channel the owner reads (which channel: UNVERIFIED; the owner names it in chat). Meanwhile the author may continue only work that does not reverse or delete someone else's merged work: additive work, work behind a flag or on another path, or work in the author's own area. A second maintainer's opinion may be recorded as advice; it is not a ruling.
4. The owner names in chat a deputy for design rulings or "nobody". If the owner says nothing, the default is nobody. A deputy may not rule on their own PR or on reversing their own earlier work.
5. Reversing or deleting someone else's merged work needs their written yes and a merger other than the author.
6. A revert is exempt from the written yes, but not from the gate, and is reported to the author the same day. "Revert" means: made with GitHub's Revert button or `git revert`, undoing one named PR in full, merged within 7 days (this narrow definition answers INV-010; PR 682 could otherwise have been labelled an unwinding).
7. Publish a plan as a draft PR or an issue comment within a day, so work others could collide with is findable.
8. Optional helper, not a required paste: two commands that list a PR's deleted files and when each was added or last changed, so a session can check rule 5 in a minute. The PR file list from `gh pr view --json files` is cut at 100 files and 22 of the last 100 merged PRs exceed that, so for a large PR read the file list with `gh api repos/IronbellyOrg/IronClaude/pulls/<N>/files --paginate` (INV-020).

```bash
# deleted files of a PR (small PRs; use the paginated API above for 100 or more files)
gh pr view <N> --repo IronbellyOrg/IronClaude --json files --jq '.files[] | select(.changeType=="DELETED") | .path'
# when a deleted file was added
git log --all --diff-filter=A --format=%cs -1 -- <path>
# when a modified file was last changed
git log origin/master --format=%cs -1 -- <path>
```

Finishing issue 290 (open, assigned to `clayphi`) with this same text gives the rule an owner who wrote it. The same PR settles the merged design's "approved by the owner (Clay)" wording (INV-003).

### Layer 2: visibility

<!-- Source: Base (original, modified) - decision folder replaced by one file per Change #8; in-flight register replaced by draft PRs; direct hold added per Change #9 (Variant 2 (CLAY) Round 2 Part 1 table and R-1) -->

1. **One decisions file, `docs/decisions.md`** (not a folder). It is seeded once with the rulings that open work depends on, about 10 groups from FULL-REPORT section 5: R19, R22, R35, R36 (the approval stays the gate); R6 and R16 (cron is the scheduler); R23 and R25 (the Pipeline field picks the launch level); the per-issue grant row; Q26 (the `.dev/coordinators/` layout); R10 (coordinator, not orchestrator); the ruling named "Decision 6" and Q35 to Q41. The source files `owner-answers.md` and `RULINGS.md` have not been read by anyone in this debate and were not found under `.dev` (INV-004), so the seed is built from FULL-REPORT section 5 and the owner's chat. One line each on issues 655 and 450 points at the file.
2. **How a ruling is recorded.** The owner gives rulings in chat and never writes a file. The session that hears a ruling adds one entry (date, ruled by login, where given as "chat", what it settles, issue number, recorded by) to the next PR it opens for that area, with the owner's chat sentence quoted in the PR body. The owner approves the wording in chat before the entry merges. If open work depends on the ruling at once, the session also posts one line on the issue the same day. The quoted chat sentence is the only evidence of the owner's word; the shared `ironbelly` login hides which session posted, and that limit cannot be removed.
3. **Work in flight** is shown by draft PRs and issue comments within a day (rule 7). There is no tracked register table.
4. **Direct hold on the open 655 series.** The owner states in chat that PRs 686 and 690 wait for the owner's ruling. `clayphi` sets both to Draft; neither is Draft today (both `isDraft=false`, `mergeStateStatus=CLEAN`; INV-002). Draft is a speed bump: the author can mark ready again, and whether a maintainer other than the author may convert a PR is UNVERIFIED. `/sc:pr-submit` does not undo a draft (`SKIP_ALREADY_DRAFT`), and code owners are not auto-requested while a PR is a draft (INV-009). The lasting hold is the ruleset with the two temporary CODEOWNERS lines below.

### Layer 3: enforcement by GitHub

<!-- Source: Base (original, modified) - five-path list replaced and owner list restructured per Changes #4 and #5; ruleset detailed per Change #6 (Variant 2 (CLAY) Round 2 R-1 for the bypass; invariant-probe.md INV-001 and INV-021 for `integration` and stale approvals) -->

**CODEOWNERS** (`.github/CODEOWNERS`, read from the PR base branch):

| Lines | Owner | Status |
|---|---|---|
| `docs/designs/` | `@ironbelly` | Core |
| `src/superclaude/core/WORKER-CONTRACT.md` | `@ironbelly` | Core |
| `/.github/CODEOWNERS` | `@ironbelly` | Core: without it a self-merge by an unowned author removes the gate (INV-006) |
| `src/superclaude/cli/issue_watch/` | `@ironbelly` | Temporary: PR 686 has 11 source files here. Removed when the owner says in chat that the 655 series is reconciled |
| `src/superclaude/skills/sc-issue-protocol/` | `@ironbelly` | Temporary: PR 690 has 4 files here (orchestrator check). Removed on the same chat statement |
| `src/superclaude/hooks/scripts/launch-level-*.sh` and the plugin mirror | `@ironbelly` | Optional after the 14 day review, the owner decides (9 of 100 PRs touched them, 5 by Clay) |

Why the owner is `@ironbelly` only, not `clayphi` as well: at 0 required approvals a listed owner who authors the PR may be able to merge it unreviewed (INV-007: one community report, unverified), and both incident PRs were Clay's. A sole non-author owner also puts the queue where the evidence says it is small: 17 of the 23 gated PRs on `master` are the owner's and would otherwise wait on Clay (INV-013). Code owners must have write access; `ironbelly` has admin (INV-005). Neither advocate proposed this; it follows from the fault-finder and from both advocates' own cost figures.

**Ruleset** (repository admin only), on `master` and `integration`:

1. Pull request required.
2. 0 required approvals.
3. Require review from code owners.
4. Dismiss stale approvals when new commits are pushed (because `/sc:pr-submit --monitor 3` pushes verified fixes after review; INV-021).
5. Block force push.
6. Block deletion.
7. Bypass for the repository admin role, for pull requests only.

`integration` is included because 23 of the last 100 merged PRs went there, all self-merged by `clayphi`, and the branch is `protected=false` (INV-001). The bypass is a hybrid taken from the Clay side: PR 662, the owner's 3 minute revert of release 6.1.0, touches `WORKER-CONTRACT.md`, so a gate with no bypass would have held it. The price is stated plainly: the gate then binds `clayphi` and not the owner, and any session on the shared `ironbelly` login can use the bypass by hand (the orchestrator never passes `--admin`; INV-022, INV-023). The owner confirms in chat that they accept a one-directional gate (decision 3). `clayphi` is `maintain`, not admin, so the author of the two incident PRs cannot use the bypass.

## Cited facts

<!-- Source: Base (original, modified) - base facts 1 to 10 kept; facts 11 to 18 added from Variant 2 (CLAY) Round 2 and invariant-probe.md per Changes #1, #3, #5, #6 and #9 -->

Figures in these facts that were later recounted are corrected in `## Corrected figures`; where they differ, that section governs.

<!-- Source: Base (original) - facts 1 to 10 kept as written in Variant 1 -->

1. Master has no protection and no ruleset. `gh api repos/IronbellyOrg/IronClaude/branches/master/protection` returns 404 "Branch not protected"; `gh api repos/IronbellyOrg/IronClaude/rulesets` returns `[]` (read 2026-11-20). Organisation-level rulesets could not be read (needs the `admin:org` scope): UNVERIFIED.
2. No CODEOWNERS file exists (snapshot `/home/coder/.cache/ic-snap-20261120/master`: `.github/` holds only FUNDING.yml, ISSUE_TEMPLATE, PULL_REQUEST_TEMPLATE.md, workflows; no `docs/decisions/`).
3. Self-merge is the norm, so the author's word was the only gate. Of the last 60 merged PRs, 29 were authored and merged by `clayphi`, 22 by `ironbelly`, 8 Clay-authored PRs were merged by `ironbelly`, 1 the other way; none has a review decision of APPROVED (`gh pr list --state merged --limit 60`).
4. PR 681 (design) opened 2026-11-19 22:32:39Z, merged 2026-11-20 00:02:33Z by its author, about 90 minutes. PR 682 (deletion of the code of owner PRs 584 and 591) opened 22:56:28Z, merged 00:02:36Z by its author, 66 minutes, reviewed only by the bot `augmentcode` (`gh pr view`).
5. The one written question went unanswered: issue 450 (the owner's issue to roll out the watcher, assigned to `ironbelly`) shows Clay's comment at 2026-11-18T17:00:32Z and nothing from `ironbelly` after it. FULL-REPORT.md section 1 item 4: issue 655 followed 2 hours 55 minutes later.
6. "Owner" is undefined: the design says "approved by the owner (Clay)" (FULL-REPORT.md section 4); the owner's decision records use "owner" for `ironbelly`. Roles on GitHub: `ironbelly` admin, `clayphi` and `IB-JonathanB` maintain, seven others read (`gh api .../collaborators`). Neither CONTRIBUTING.md (79 lines) nor CLAUDE.md says who rules on design.
7. The only duplicate check lists and never stops: `src/superclaude/skills/sc-issue-protocol/refs/create.md:20` says "Possible duplicates do not stop the run"; the PR template's only link field is `Closes #` (`.github/PULL_REQUEST_TEMPLATE.md`).
8. A spoken rule already failed once. Issue 290 (open, assigned to `clayphi`) records what the team was told on 2026-10-22 (file an issue first, run `/sc:recommend --plugin`, do not create new skills yet) and says "None of this is in HOW-WE-WORK.md".
9. A repo advisory check that cannot block already exists as precedent: `.github/workflows/boundary-guard.yml` says it "cannot block a merge. Making it a real merge control is a repository-settings decision".
10. The owner's decisions were not visible: they sit in an unpushed local plan, memory files and Coder issues 515 and 516 (FULL-REPORT.md section 1 item 3, section 10 item 6).

<!-- Source: Variant 2 (CLAY), Round 2 Part 1 and invariant-probe.md INV-003 and INV-019 - merged per Changes #1 and #3 -->

11. The merged design contradicts the owner's identity. PR 681's body says "The design was approved by Clay on 2026-11-19" and "the owner reviews and merges"; `docs/designs/orchestrator.md:593` says "Clay's ruling 35 ... waits for Clay's explicit OK"; every ruling in the sources read was posted under `clayphi` (FULL-REPORT.md:50). All quoted from INV-003.
12. PR 683 (`clayphi`, base master, touches `WORKER-CONTRACT.md` and `docs/designs/`) opened 2026-11-19T23:07Z and was merged 2026-11-20T01:16:58Z by `clayphi`, about 75 minutes after 681 and 682 merged (INV-019).

<!-- Source: Variant 2 (CLAY), Round 2 Part 1 rows 5 and 11 and invariant-probe.md INV-001, INV-002, INV-005, INV-018 - merged per Changes #5, #6 and #9 -->

13. Base branches of the 100 merged PRs (numbers 469 to 688): `master` 71, `integration` 23 (all `clayphi`, all self-merged), `346Claude-integration` 5 and `346GPT-integration` 1 (all `ironbelly`, self-merged). `integration` returns `protected=false`. Work reaches master through release PRs with head `integration` (640, 658, 664), each a bundle of 100 or more files (INV-001).
14. PRs 686 and 690 are not Draft. 686 (`clayphi`, title "issue 655, PR A") has 59 files, +14,306 and -16,637, 11 source files in `issue_watch/`, none on `WORKER-CONTRACT.md` or `docs/designs/`. 690 ("issue 655, PR P") has 13 files, +2,811 and -39, 4 of them in `sc-issue-protocol/` (orchestrator check), none on `WORKER-CONTRACT.md`, `docs/designs/` or `issue_watch/` (INV-002, INV-018).
15. PR 662, the owner's revert of release 6.1.0 (opened 2026-11-19T01:17:35Z, merged 01:20:30Z), touches `WORKER-CONTRACT.md`.
16. Rulesets are available here: the organisation plan is `free` (`gh api orgs/IronbellyOrg`), the repository is public, and GitHub's documentation says rulesets are "available in public repositories with GitHub Free". Whether "Evaluate" (dry run) mode is offered on the Free plan: UNVERIFIED. Code owners must have write permission; `ironbelly` (admin), `clayphi` and `IB-JonathanB` (both maintain) have it. No CODEOWNERS file exists at `.github/`, the root or `docs/` (all three 404).
17. PR 682 reaches the gated path list through 1 of its 36 files (`WORKER-CONTRACT.md`, +1 -12); 27 of its files are deleted files, all first added on 2026-11-16 or 2026-11-17. A test that pins the contract to the pipeline (`tests/skills/test_worker_contract.py`) is in the same PR, which is why removing the feature forced a contract edit; code the contract never mentions has no such tie.
18. `/sc:pr-submit --monitor 3` pushes verified fixes to the PR head branch without asking and releases the PR to ready after the push (INV-021). Draft PRs are never mutated by it.

## Cost

<!-- Source: Base (original, modified) - estimates re-derived from the Round 2 final tables as adjusted by refactor-plan.md (Change #10); per-item costs are in the ranked table -->

Estimates (the advocates'; none measured). Per-item costs are in `## Ranked, costed, ordered package`. The "do now" items add up as follows (my arithmetic over those estimates):

| Who | Items | Estimate |
|---|---|---|
| Session or maintainer time | Ranks 2, 3, 4, 6 and 8 (5 min, 60 to 90 min, 15 min, about 5 min, 1 to 2 h) | 145 to 235 minutes, about 2.4 to 3.9 hours |
| Repository admin | Rank 5 (ruleset) | 15 to 30 minutes, `ironbelly` only |
| Owner and Clay chat | Rank 1 (10 min owner, 10 min Clay), plus a few minutes to approve wording for ranks 3 and 8 | about 20 minutes plus the wording approvals |

For comparison, the Round 2 papers each stated a total of 2.5 to 4 hours (OURS) and 3 to 4.5 hours (CLAY) of session or maintainer time, 15 to 30 minutes of admin time and 20 to 25 minutes of owner and Clay chat. The unified package adds the sole-owner CODEOWNERS file, the throwaway test and the `integration` target; the papers cost the file at 15 minutes and the test at about 5 minutes for one PR, and do not cost the `integration` target separately.

Who pays the queue (recount, `## Corrected figures`): Clay's gated PRs on `master` and `integration` together are about 17 in about 10 days (6 on `master`, 11 on `integration`) and wait on the owner. The owner's own gated PRs do not wait on Clay if the bypass is kept. The owner's added work is the throwaway test (about 5 minutes) and the 14 day review (about 20 minutes).

Items not costed in the papers: the owner's chat decisions beyond the roles, the announcement, and the optional guard-file lines.

## Risk

<!-- Source: Base (original, modified) - base risks kept where still true; stop-on-overlap risk removed with its item; risks from refactor-plan.md Risk Summary and invariant-probe.md added -->

- A path-limited required review makes the approver a queue. With `@ironbelly` as the sole code owner, Clay's gated PRs wait on the owner, about 17 in about 10 days on `master` and `integration` together. The only measured owner response is the 4.4 hour median on Clay's PRs the owner merged (n=10); no code owner approved anything in the window, so there is no observed approval time (INV-025). Mitigation: drop a path at the 14 day review, `WORKER-CONTRACT.md` first.
- A sole code owner is a single point. If `ironbelly` is away, gated PRs wait: the deputy the owner names in chat is not wired into CODEOWNERS (INV-017). How often the owner is away: UNVERIFIED.
- A required reviewer behind the shared login `ironbelly` proves little. The gate yields "a login other than the author's said yes", not "the owner read it" (INV-008). PR 681 is a 1,412-line single file.
- The gate may never block, or may block the owner (INV-007). Impact: High if silent, Medium if loud. Rollback: one admin click turns the ruleset off; the test protocol finds out before the ruleset is announced.
- The bypass can be used by any session on the shared login. Rollback: remove the bypass; the owner's PRs then need a second approver.
- Path coverage is fragile. PR 682 reaches the list through 1 of 36 files; a pure deletion of `src/superclaude/cli/issue_pipeline/` without the contract edit would not match. The 655 design's next PRs create `src/superclaude/cli/orchestrator/`, which is on no list, and the temporary lines are removed once the series is reconciled (INV-018).
- Authors skip the reversal sentence, as 682's author did (it named neither #584 nor #591). The gate on paths is the backstop; the CI check is built only on a tripwire.
- The root `CLAUDE.md` rule text and `docs/decisions.md` are not on CODEOWNERS (only `/.github/CODEOWNERS` is), so an unowned self-merge can edit them (INV-006). Rank 11 is the tripwire answer.
- The decisions file rots, or is seeded from second-hand summaries. Rulings 1 to 39 were all posted under `clayphi`, so a "ruled by" column would record `clayphi` for rulings the package calls the owner's (INV-004). Rollback: move rulings to issue comments if fewer than 3 entries are added in 30 days.
- Draft is reversible by the author (speed bump only). The lasting hold is the ruleset with the two temporary lines.
- A tracked in-flight table would rot; it is dropped in favour of draft PRs.

Risk summary (from the refactoring plan):

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 5 and 6 (sole owner, ruleset) | The gate never blocks, or blocks the owner (INV-007) | High if silent; Medium if loud | One admin click turns the ruleset off; the test protocol finds it loud or silent before it is announced |
| 6 (bypass) | Sessions on the shared login can use it | Medium | Remove the bypass; the owner's PRs then need a second approver |
| 4 (paths) | Queue on the owner for Clay's gated PRs, about 17 in 10 days on `master` and `integration` together (recount; one third on `master`) | Medium | Drop a path at the 14 day review, `WORKER-CONTRACT.md` first |
| 3 (self-classified text) | Authors skip the "reversal" sentence, as 682's author did | Medium | The gate on paths is the backstop; CI check on tripwire |
| 8 (decisions file) | Rots, or seeded from second-hand summaries | Low | Move rulings to issue comments if fewer than 3 entries are added in 30 days |
| 9 (hold) | Draft is reversible by the author | Low | The ruleset with the two temporary lines |

## What it gets right

<!-- Source: Base (original, modified) - four base points kept, first two qualified; points added from Variant 2 (CLAY) What it gets right per Changes #3 and #10 -->

- Silence becomes a block instead of a yes, on the gated paths. That is the property that would have stopped PR 682 merging 66 minutes after it opened, probably, UNVERIFIED until the throwaway test passes.
- It writes down who "owner" means by login, which is gap 3 and the root of the "approved" status of the design. It does so in chat and in a PR that Clay accepts, not by decree (A-003).
- It makes decisions findable (the decisions file) and work in flight findable (draft PRs and issue comments), the items that reach the owner's unpushed plan.
- It takes the fix out of memory and meetings, where the 2026-10-22 rule died (issue 290).

<!-- Source: Variant 2 (CLAY), What it gets right bullets 1 and 3, and Round 1 Claim - merged per Change #3 -->

- It fixes the two causes the evidence supports as inputs: no definition of "owner" and no rule that silence is not consent ("a question to a named person gets a written answer; silence is never a yes").

<!-- Source: Variant 2 (CLAY), What it gets right bullets 3 and 4, with Round 1 U-005 - merged per Change #10 -->

- Publishing beats searching. The missed items (the zero-setup plan, Coder issues 515 and 516, the owner's decisions in memory files) were unpushed or in another repository, so no search or template section reaches them; only publishing does.
- It adds no new command or skill that issue 290 says not to build yet (the 2026-10-22 onboarding rule "not to create new skills or commands yet", and the owner's 2026-10-29 answer "only file issues until we have an eval framework").

## Ranked, costed, ordered package

<!-- Source: Variant 2 (CLAY), Round 2 Part 3 final table, with Base (original) Round 2 OURS final table - merged per Change #10 and adjusted by Changes #3 to #9 (sole owner, `integration`, stale approvals, throwaway test, direct hold) -->

"REPOSITORY ADMIN ONLY" means `ironbelly`, the only admin (`clayphi` and `IB-JonathanB` have `maintain`). All costs are estimates, none measured. Ranks follow the order of the next subsection.

| Rank | Item | Cost estimate | Who can do it | When (now / after X / drop) |
|---|---|---|---|---|
| 1 | Owner decisions in chat: decisions 1 to 6 in `## Decisions the owner gives in chat` (roles and sole code owner `@ironbelly`; deputy or "nobody" and the channel; one-directional gate and bypass; `integration` in or out; hold on PRs 686 and 690; seed of the decisions file). A session records each. | 10 min owner chat, 10 min for Clay to accept the roles in the PR of rank 3 (both Round 2 papers); the added decisions are not costed separately | Owner decides in chat; a session records; `clayphi` accepts the roles in writing | Now. First: ranks 2 to 8 depend on it |
| 2 | Direct hold: the owner states in chat that PRs 686 and 690 wait for the owner's ruling; `clayphi` sets both to Draft | 5 min | Owner says it in chat; `clayphi` converts (a maintainer converting: UNVERIFIED) | Now, right after rank 1 |
| 3 | Rule text PR: root `CLAUDE.md` section, two-line pointer in `HOW-WE-WORK.md`, one line in `CONTRIBUTING.md`, two PR template lines, the silence, reversal and revert rules, publish within a day (this is the draft PR habit, cost 0), the optional helper commands. Finishes issue 290 and settles the design's "approved by the owner (Clay)" wording | 60 to 90 min in one PR (includes about 15 min for the `HOW-WE-WORK.md` copies); a few minutes for the owner to approve the wording in chat | Any maintainer or session writes it; `clayphi` as issue 290 assignee; `clayphi` accepts the roles in the PR | Now, after rank 1. Must be accepted by Clay before rank 7 |
| 4 | `.github/CODEOWNERS` PR: core lines `docs/designs/`, `src/superclaude/core/WORKER-CONTRACT.md`, `/.github/CODEOWNERS`; temporary lines `src/superclaude/cli/issue_watch/` and `src/superclaude/skills/sc-issue-protocol/`; sole owner `@ironbelly` | 15 min | Any maintainer, by PR (inert until rank 5) | Now, in parallel with rank 3. Merge before rank 5 |
| 5 | Ruleset on `master` and `integration`: PR required, 0 required approvals, code-owner review, dismiss stale approvals, no force push, no deletion, bypass for the admin role for pull requests only. Use "Evaluate" first if the option is offered | 15 to 30 min | **REPOSITORY ADMIN ONLY** | Now, after rank 4 is merged |
| 6 | Throwaway test (INV-027), in `## Test protocol and fallbacks` | About 5 min for one throwaway PR (both Round 2 papers); the full protocol has three PRs and is not costed separately | `clayphi` opens the first two throwaway PRs and never the owner's login; an owner-authored PR for the third; the admin reads the result | After rank 5 is active, before rank 7. If it does not block: the fallbacks |
| 7 | Announcement: the owner states in chat that the gate is live and confirms that it binds non-owners (the bypass) | Not costed in the papers | Owner, in chat | After rank 6 passes and rank 3 is merged with Clay's acceptance |
| 8 | `docs/decisions.md` seeded with about 10 ruling groups, plus one line each on issues 655 and 450 | 1 to 2 h session time; a few minutes of owner chat to approve the wording | Any maintainer or session drafts; the owner approves the wording in chat | Now, in parallel with ranks 3 to 7 (needs rank 1; the PR 686 reconciliation needs it) |
| 9 | 14 day review: count gated PRs, median wait, any wait over 3 working days, and silent passes (gated PRs that merged with no non-author approval), against a minimum sample; decide the optional guard-file lines; remove the two temporary CODEOWNERS lines when the owner says in chat that the 655 series is reconciled | 20 min | Owner and `clayphi`; the CODEOWNERS edit is any maintainer | After: 14 days after the ruleset is switched on. The temporary lines come out on the owner's chat statement, not on day 14 |
| 10 | CI check that fails when a PR deletes or rewrites recent code with no non-author approval, modelled on `boundary-guard.yml` (98 lines, advisory today); reads files with `gh api .../pulls/N/files --paginate` | 2 to 4 h | Any maintainer writes it; **REPOSITORY ADMIN ONLY** to make it required | After, only on the tripwire: a PR that deletes or rewrites 200 or more lines of someone else's recent code merges with no second person off the gated paths, or the 14 day review removes the contract path |
| 11 | CODEOWNERS lines on root `CLAUDE.md` and `docs/decisions.md` | 5 min plus about 7 extra gated reviews per 11 days (the papers' figure, not re-checked) | Any maintainer edits; the ruleset enforces | After, only if the rule text or the decisions file is edited by the author of a gated PR without the other person's written accept. Otherwise drop |
| 12 | Optional CODEOWNERS lines `src/superclaude/hooks/scripts/launch-level-*.sh` and the plugin mirror (decision 7) | Not costed in the papers | Any maintainer edits; the owner decides in chat | After rank 9, if the owner says yes |
| Drop | Items in `## Dropped items and why` | | | Drop |

Ranks 1, 2, 3, 7 and 8 need the owner's word in chat; rank 5 is the only "do now" item that nobody but the owner can do.

### Order and dependencies

<!-- Source: Base (original, modified) - base listed nine items with no order; order added per Change #10 from the Round 2 tables and Changes #7 and #9 -->

1. **Owner chat decisions** (rank 1). No dependency. Gates everything below. A session records each decision.
2. **Direct hold** (rank 2). Needs decision 5. Closes the exposure of the open series until the ruleset is on.
3. **Rule text PR accepted by Clay** (rank 3). Needs decisions 1 and 2. Clay's written acceptance of "owner = `ironbelly`" in this PR is a prerequisite of the announcement (A-003), because a ruleset applied before it turns the dispute into a blocked merge button.
4. **CODEOWNERS PR** (rank 4). Needs decision 1 (sole owner) and decision 4 for the target branches. Merge it before the ruleset so the switch is one admin action.
5. **Ruleset** (rank 5). Needs rank 4 merged. Admin only.
6. **Throwaway test** (rank 6). Needs ranks 4 and 5. Run by `clayphi`, not from the owner's login.
7. **Announcement** (rank 7). Needs rank 6 passed and rank 3 accepted. If rank 6 fails, apply the fallbacks first.
8. **Decisions file** (rank 8). Needs decision 6 and the owner's chat approval of the wording. It has no admin step, so it runs in parallel with ranks 3 to 7.
9. **14 day review** (rank 9). Needs rank 5 active. Counts silent passes as well as waits, because a gate that never blocks produces an empty, happy review (INV-027). The minimum sample is not fixed in the debate files; see `## Open invariants`.
10. **Tripwire items** (ranks 10, 11, 12). Each fires only on the condition named in its row.

## What only the repository admin can enable

<!-- Source: Base (original, modified) - admin-only list from Variant 1 Round 1 and Round 2 OURS, extended with items added by Changes #5, #6 and #7 -->

Only `ironbelly`, the sole admin, can do these (`clayphi` and `IB-JonathanB` have `maintain`):

1. Create the ruleset (or branch protection) on `master`.
2. Add `integration` as a target of the ruleset (it is `protected=false` today).
3. Require review from code owners.
4. Set the required approvals count (0 in this package; 1 is fallback 1 in `## Test protocol and fallbacks`).
5. Turn on "dismiss stale approvals when new commits are pushed".
6. Block force push and block deletion.
7. Set the bypass list (the admin role, for pull requests only).
8. Make any CI check required, including `boundary-guard.yml` (its own text says making it a real merge control "is a repository-settings decision") and the deletion check of rank 10.
9. Use the ruleset rule "required reviewers" by path (fallback 2). Whether this free-plan organisation can use it, and whether it needs a team: UNVERIFIED.
10. Use "Evaluate" (dry run) mode, if it is offered. Whether it exists on the Free plan: UNVERIFIED.
11. Read or change organisation-level rulesets. They could not be read because the token lacks the `admin:org` scope: UNVERIFIED.

Any maintainer can do these by PR, with no admin step:

1. The `.github/CODEOWNERS` file (inert until the ruleset exists, and an edit to it is gated by the ruleset once its own line is there).
2. The rule text in root `CLAUDE.md`, the pointer in `HOW-WE-WORK.md` and the line in `CONTRIBUTING.md`.
3. `docs/decisions.md`.
4. The two PR template lines.
5. Finishing issue 290 (`clayphi` is the assignee).
6. Writing the CI deletion check (making it required is admin only).
7. Draft PRs and issue comments.

Converting a PR to Draft: the author can; whether a maintainer other than the author can is UNVERIFIED.

## Lightest version that would have prevented the incident

<!-- Source: Variant 2 (CLAY), Round 2 Part 3 "The lightest version that would have prevented the incident", adjusted by Changes #5 and #6 and by invariant-probe.md INV-026 - merged per Change #10 -->

The lightest version is ranks 1, 3, 4, 5, 6, 7 and 9, limited to the two core paths (`docs/designs/` and `src/superclaude/core/WORKER-CONTRACT.md`) plus the `/.github/CODEOWNERS` line, with `@ironbelly` as the sole code owner and the ruleset on `master` and `integration`. It leaves out the two temporary lines, the decisions file (rank 8), the direct hold (rank 2) and every tripwire item.

Why it would have caught the incident input: PR 681 changed `docs/designs/orchestrator.md`, and PR 682 changed `WORKER-CONTRACT.md` (+1 -12, 1 of its 36 files). Both authors were `clayphi`, who is not a code owner under this list and is not admin, so cannot use the bypass.

Cost: the Round 2 CLAY paper estimated about 2.5 hours plus 15 to 30 minutes for the admin. Adding the rows of the ranked table for ranks 1, 3, 4, 6 and 9 (20, 60 to 90, 15, about 5 and 20 minutes) gives about 120 to 150 minutes of session, maintainer and chat time, plus the same 15 to 30 minutes for the admin (the owner's decisions beyond the roles and the announcement are not costed). Either way it is under 3 hours.

Words alone (ranks 1 and 3) cost about 1.5 hours and do not prevent the incident. The text alone would not have prevented it: PR 681's body said "the owner reviews and merges" and it was self-merged, and PR 683 was self-merged about 75 minutes after 681 and 682 merged. Whether a session obeys a `CLAUDE.md` line cannot be shown.

The prevention claim for this lightest version is conditional on the throwaway test (INV-007). Until rank 6 passes, the claim is "probably, UNVERIFIED". Gate by gate, the weakest points are G3 (682 matches only through 1 of 36 files) and G4 (an author at 0 required approvals); see `## Open invariants`.

## Version still refused

<!-- Source: Variant 2 (CLAY), Round 2 Part 3 "The version I would still refuse", reconciled with the refactor-plan.md adjudication table and "Changes NOT Being Made" - merged per Change #10 -->

The unified package still refuses:

1. **Words alone offered as prevention.** The incident shows a sentence in a file did not bind. The Clay Round 1 idea of holding the ruleset in reserve behind a tripwire was withdrawn by Clay in Round 2: a tripwire fires after the harm and nobody watches merges.
2. **The five-path CODEOWNERS list** of FULL-REPORT section 11 item 3. It matches 27 of the last 60 merged PRs and makes a queue on active work (OURS Round 1 concession).
3. **A required pasted deletion check.** It fires on 11 of 100 PRs (not re-run by the fault-finder), 9 of them Clay's and mostly their own earlier work, and has no revert exemption (PRs 662 and 664). Its place is an optional helper, with a CI check only on the tripwire.
4. **Any item that adds commands or skills that issue 290 says not to build yet** (`/sc:overlap`, stop-on-overlap in `/sc:issue`).
5. **Any fallback that depends on a person who has never acted here.** `IB-JonathanB` is not named as deputy, owner or code owner until they agree in an issue comment.

The one point left to the owner is symmetry. A ruleset with no bypass would gate the owner's own PRs too, and would have held PR 662, the owner's 3 minute revert of release 6.1.0. The plan adopts the bypass (admin role, pull requests only) and asks the owner to confirm in chat (decision 3). If the owner prefers symmetry, Clay accepts it and the revert case is simply a wait; the owner's own gated PRs then need an approval from a code owner other than the author, which a sole-owner list cannot give (OURS Round 1 concession 2), so the CODEOWNERS list would have to change.

## Test protocol and fallbacks

<!-- Source: Variant 2 (CLAY), Round 2 R-1 point 2 (the throwaway test is a condition, not a courtesy), with condition INV-027 copied from refactor-plan.md "Invariant conditions" - merged per Change #7 -->

Condition INV-027, as stated in the refactoring plan:

> Test protocol: after the CODEOWNERS file is merged and the ruleset is active, `clayphi` opens a throwaway PR that edits one line under `docs/designs/` with base `master`, with no approval; expected result `mergeStateStatus` BLOCKED and review decision REVIEW_REQUIRED, and the merge button refuses without `--admin`; repeat with base `integration`; then an owner-authored throwaway PR on the same path to learn whether the bypass is needed; close all throwaway PRs unmerged. Do not run it from the owner's login. If the first test does not block: fallback 1, require 1 approval for pull requests (cost: every PR, 89 of 100 recent merges were self-merged); fallback 2, the ruleset rule "required reviewers" by path (generally available since 2026-02-17 per GitHub's changelog; whether this free-plan organisation can use it, and whether it needs a team, is UNVERIFIED); fallback 3, drop the gate and keep words, the hold and the tripwire

Why the conditions matter (INV-027): a pass is only meaningful if the author is `clayphi` (a non-admin; under the sole-owner list also not a code owner), the PR touches an owned path, the base is `master`, there is no approval, and the merge is tried without `--admin`. Run from the owner's login it passes or fails for the wrong reason (admin and shared login). The owner-authored third PR also shows how the author-owner case of INV-007 behaves for the owner's own PRs.

The test belongs after the ruleset is active and before the announcement (ranks 6 and 7 in `## Ranked, costed, ordered package`). Both Round 2 papers asked for a throwaway PR; the Clay paper makes it a condition. Clay's Round 2 view is that a required approval of 1 (fallback 1) is a much larger cost than the narrow gate, so if the zero-approval setting cannot be made to block they would drop the ruleset and fall back to the hold and the tripwire (fallback 3). The plan lists the three fallbacks in the order above.

### 14 day review

<!-- Source: Variant 2 (CLAY), Round 2 rank 7, with Base (original) Round 2 OURS rank 6, as extended by invariant-probe.md INV-016 and INV-027 - merged per Change #7 -->

After the ruleset is switched on, the owner and Clay (about 20 minutes) count:

1. Gated PRs, and their median wait, and any that waited more than 3 working days.
2. Silent passes: gated PRs that merged with no non-author approval. A gate that never blocks produces an empty, happy review if only waits are counted (INV-027).
3. Whether the sample is large enough to judge. A quiet fortnight could show a handful of gated PRs, a burst fortnight 30 or more (INV-016). The debate files give no minimum figure: UNVERIFIED, open.

If the median wait is over one working day, drop `WORKER-CONTRACT.md` from CODEOWNERS first (18 of the 31 gated PRs counted in Round 2, 21 of 35 on recount, and the least tied to the incident). The Clay paper adds that the contract path also catches deletions, so it should then be replaced by the CI check of rank 10 rather than simply dropped.

## Dropped items and why

<!-- Source: Base (original, modified) - items of Variant 1 and section 11 rejected per refactor-plan.md "Changes NOT Being Made"; merged per Change #10 -->

| Item | Proposed by | Why dropped (evidence) |
|---|---|---|
| `/sc:overlap` command or CI overlap scan | OURS, section 11 item 8 | Days of work; contradicts the owner's 2026-10-29 answer on issue 290 ("only file issues until we have an eval framework"); misses the unpublished work that was the real miss (U-005) |
| Stop-on-overlap in `/sc:issue --create` and `--claim` | Section 11 item 1 | `--claim` already stops on an issue assigned to someone else (`refs/claim.md:42`); `--create` lists up to 10 possible duplicates and continues (`refs/create.md:20`); issue 655 cited 13 items, so a stop would have passed (X-002) |
| 24 hour cooling period | Section 11 item 7 | GitHub cannot enforce a delay; the required reviewer does the work (C-009) |
| Tracked in-flight register | Section 11 item 6 | Rots; draft PRs and issue comments do the job at zero cost (C-008). Revisit when the coordinator layout `.dev/coordinators/` of Q26 exists (topic D07) |
| `docs/decisions/` folder with index and full back-fill | Section 11 item 5 | One file is enough until it has about 50 entries (OURS Round 2) |
| Mandatory pasted deletion check | OURS, Round 2 | Fires on 11 of 100 PRs, 9 of them Clay's and mostly their own earlier work; no revert exemption (PRs 662, 664); one more thing the author can skip. Replaced by a written sentence, an optional helper and a CI check only on a tripwire |
| Five-path CODEOWNERS list | Section 11 item 3 | Matches 27 of the last 60 merged PRs; a queue on active work (OURS Round 1 concession) |
| Naming `IB-JonathanB` as the deputy | Both, Round 1 | Not shown active: no authored PR, no reviewed PR |
| Changing `/sc:pr-submit` to inject the PR template | OURS, Round 2 | The template reached 0 of the last 79 PRs, so the template is not a carrier; the text goes in root `CLAUDE.md` instead. Dropped for now |

## Decisions the owner gives in chat

<!-- Source: Base (original, modified) - the base had no decision points (base-selection.md, Clarity 5); decisions derived from the refactor-plan.md adjudication table, Invariant conditions and Changes #3 to #9 -->

Standing rule: every approval and ruling is given by the owner in chat and recorded by the agent. The owner is never asked to write a file. Decisions 1 to 6 are asked now (rank 1); decision 7 is asked after the 14 day review (rank 9).

1. **Roles and sole code owner.** Yes ("owner = `ironbelly` for design rulings; the only code owner is `@ironbelly`; Clay accepts in the PR of rank 3") lets rank 3 be written, puts one owner in the CODEOWNERS file, and makes `clayphi`, who authored both incident PRs, a non-owner. Another answer (for example that Clay is the owner for design, or that a second code owner is listed) changes the roles text, the CODEOWNERS owner and the design file's wording, and the throwaway test must be re-run for that list (INV-003, INV-007). The ruleset is not announced until the owner and Clay agree (A-003).
2. **Deputy or "nobody", and the channel the owner reads.** A named deputy for design rulings (one chat line per absence with dates) goes into the roles text, and may not rule on their own PR or on reversing their own earlier work. "Nobody; designs wait" is the default if the owner says nothing. The channel gives the "ask again after 3 working days" rule an address. `IB-JonathanB` is not named until they agree in an issue comment.
3. **One-directional gate and bypass.** Yes (bypass for the admin role, pull requests only) keeps the owner's own gated PRs, and a revert like PR 662, from waiting, and means the gate binds `clayphi` and not the owner. Sessions on the shared `ironbelly` login can use the bypass; the orchestrator never passes `--admin`. No (symmetry) means the owner's gated PRs need a code owner other than the author, so the CODEOWNERS list would need a second owner (see `## Version still refused`).
4. **`integration` in or out.** In puts the ruleset on `master` and `integration`: 23 of the last 100 merged PRs went there, all self-merged. Out must be one of two things: the owner retires `integration`, or allows it to reach `master` only through a reviewed PR (INV-001). Otherwise a design or deletion opened against `integration` passes every other item.
5. **Hold on PRs 686 and 690.** Yes ("686 and 690 wait for my ruling") lets `clayphi` set both to Draft, and the two temporary CODEOWNERS lines stay until the owner says in chat the 655 series is reconciled. No leaves only the temporary lines: 686 is caught through `issue_watch/` and 690 through `sc-issue-protocol/`, but later PRs of the series that create `src/superclaude/cli/orchestrator/` are on no list (INV-018).
6. **Seed of the decisions file.** The owner approves the wording of about 10 ruling groups (FULL-REPORT section 5) in chat before the file merges. The seed sources `owner-answers.md` and `RULINGS.md` have not been read by anyone, so if the owner's chat is the only source the file may be small on day one (INV-004). If the owner rules that issue comments are the system of record, the file is dropped; if fewer than 3 entries are added in 30 days while the owner gave rulings, rulings move to issue comments.
7. **Launch-level guard files on CODEOWNERS, after the review.** Yes adds `src/superclaude/hooks/scripts/launch-level-*.sh` and the plugin mirror (9 of 100 PRs touched them, 5 by Clay), which adds gated PRs for the owner to review. No leaves them off.

## Corrected figures

<!-- Source: Base (original, modified) - figures recounted by the fault-finder in invariant-probe.md (INV-001, INV-012 to INV-015) replace the advocates' figures per refactor-plan.md Overview; CONTRIBUTING.md:77-79 struck per Round 2 of both advocates -->

Where the fault-finder's recount differs from an advocate's figure, the recount is used. Window: the 100 most recent merged PRs (numbers 469 to 688, merged 2026-11-09T19:18Z to 2026-11-20T02:26Z, about 10.3 days, not 11).

| Figure | Advocate figure | Corrected figure | Source |
|---|---|---|---|
| PRs touching a gated path (`WORKER-CONTRACT.md` or `docs/designs/`) | 31 (18 and 16) | **35** (WC 21, DD 18, overlap 4). A floor: 22 of the 100 PRs have 100 or more files, the cap of `gh pr list --json files`, so every path count is a minimum | INV-012 |
| Of the gated PRs, those on `master` | not split | **23** (WC 11, DD 16): **17 owner-authored, 6 Clay-authored**. The other 12 of the 35 target another base: 11 Clay PRs into `integration` (617, 620, 621, 622, 627, 629, 631, 632, 639, 650, 656) plus 474 | INV-001, INV-013 |
| Who waits on whom | 15 on Clay's side, 16 on the owner's, "about even" | On `master`, with an owner-and-Clay list, 17 PRs would wait on Clay and 6 on the owner (about 3 to 1 on Clay). With the sole owner `@ironbelly`, Clay's gated PRs on `master` and `integration` together are about 17 in about 10 days (6 on `master`, 11 on `integration`). Open time of the 17 owner PRs on `master` (minutes): median 48 | INV-013, plan Risk Summary |
| Worst gated day on `master` | 12 on 2026-11-17 | **7** on 2026-11-17; the 12 included 5 `integration` PRs | INV-013 |
| PR template reach | 14 of 100 | 14 of 100, **but 0 of the last 79**: all 14 are PRs 477 to 500 (merged 2026-11-10 and 11-11); 681, 682 and 683 do not carry it. The template adds no safety | INV-014 |
| Self-merge | 89 of 100 | 89 of 100 held (`ironbelly` 57 of 58, `clayphi` 32 of 42); 0 APPROVED reviews; of the 35 gated PRs only 3 were merged by a non-author; 20 of the 23 gated `master` PRs were self-merged | INV-015 |
| `CONTRIBUTING.md:77-79` | cited by Variant 2 as team governance (and in the Round 2 OURS fact list) | **Struck from the evidence.** Line 75 is the heading "Disclaimer: social convention, not a CI-enforced gate"; lines 77 to 79 are about one CI rule, the rot budget for test failures. Both advocates agreed | Round 2 OURS R-5, Round 2 CLAY R-5 |
| `IB-JonathanB` | named as deputy or third owner in Round 1 | Role `maintain`; **no authored PR and no reviewed PR**; `gh search` for issue comments printed nothing (run by both advocates and the orchestrator, not re-run by the fault-finder) | Round 2 OURS section 0, Round 2 CLAY Part 1 row 9 |

Figures that stand but were not re-run by the fault-finder: the 11-of-100 firing rate of the computed deletion check, and the median open times of owner-merged PRs (Clay's PRs the owner merged: 10 PRs, median about 4.4 hours, none waited days). Clay's self-merges stay open a median of 0.76 hours, 90th percentile 2.5 hours (n=32; re-run by the Clay advocate and held).

## Open invariants

<!-- Source: Base (original, modified) - the four HIGH UNADDRESSED findings of invariant-probe.md become binding conditions per refactor-plan.md "Invariant conditions" (Change #7); the Round 2.5 depth standard allows no Round 3, so they are resolved here by stated condition, not by a further round -->

Four findings stay open. Each has the condition that resolves it.

| ID | Finding | Condition that resolves it |
|---|---|---|
| INV-001 | The ruleset on `master` does not cover the places where design and deletion work lands: 29 of the 100 recent PRs, and 12 of the 35 gated PRs, targeted a non-master base; `integration` is `protected=false` | The ruleset targets `master` and `integration`; or the owner retires `integration` or allows it to reach `master` only through a reviewed PR. Until then a design or deletion opened against `integration` passes every other item |
| INV-007 | "Require review from code owners" at 0 required approvals may pass an author who is himself a listed code owner. GitHub's documentation is silent; one community report (discussion 14866, comment of 2024-08-26) says the PR is then mergeable; an opposite report (2026-03-24) says an owner-authored PR with approvals required stays blocked | "Would have prevented 681 and 682" is stated as "probably, UNVERIFIED" until the throwaway test in `## Test protocol and fallbacks` passes. Mitigation in the design: the only code owner is `@ironbelly`, so the incident author (`clayphi`) is not an owner |
| INV-026 | The Round 2 consensus claim that its ranks 1 to 7 alone would have prevented 681 and 682 is falsified if any gate fails for the incident input | The gate-by-gate table below. The text items alone add no prevention |
| INV-027 | The throwaway test and the 14 day review may not detect a gate that does not block | The test protocol copied in `## Test protocol and fallbacks`, run with the stated conditions, plus a 14 day review that counts silent passes and has a minimum sample |

Gate by gate for the incident input (INV-026), with PR 681 (author `clayphi`, base `master`, 1 file `docs/designs/orchestrator.md`) and PR 682 (author `clayphi`, base `master`, 36 files):

| Gate | Question | State |
|---|---|---|
| G1 | A ruleset exists | No today (`protection` 404, `rulesets` `[]`); yes after rank 5 |
| G2 | A pull request is required | Yes |
| G3 | The path matches | 681 yes via `docs/designs/`; 682 yes via 1 of 36 files, `WORKER-CONTRACT.md`; fragile (INV-018) |
| G4 | A non-owner author is blocked at 0 required approvals | To be tested (INV-007, INV-027) |
| G5 | The author cannot use the bypass | Yes: `clayphi` is not admin |
| G6 | The approver is independent | Only a second login, not proof that the owner read it (INV-008) |
| G7 | The approval is current at merge | Needs "dismiss stale approvals", which is in the ruleset (INV-021) |
| G8 | The base is `master` or `integration` | Covered when `integration` is a target |

### Medium findings also carried

<!-- Source: Variant 2 (CLAY) and Base (original), with refactor-plan.md "Invariant conditions" MEDIUM list - merged per Changes #3, #6, #7 and #9 -->

The plan states that the verdict must also carry these:

- **INV-021, stale approvals.** `/sc:pr-submit --monitor 3` pushes fixes after review, so the ruleset sets "dismiss stale approvals". The default of that option in the ruleset UI: UNVERIFIED.
- **INV-022, two authorities and two gates.** The orchestrator design makes Clay the authority for CODEOWNERS edits (lines 288 and 593); this package makes the owner the approver. The orchestrator never uses `--admin`, and the owner's chat go is not a GitHub approval, so on gated paths a merge needs both.
- **INV-002, who converts 686 and 690 to Draft.** Neither is Draft today; the owner states the hold in chat and `clayphi` converts. Whether another maintainer may: UNVERIFIED.
- **INV-010, "revert".** Defined narrowly in rule 6 of the rule text. The text exemption and the mechanical gate can still disagree: PR 662 is exempt by the text but gated by the ruleset, which is why the bypass exists.
- **INV-016 and INV-027, the 14 day review** needs a minimum sample and a count of silent passes. The debate files give no minimum figure.
- **INV-012, INV-013, INV-014, corrected figures.** See `## Corrected figures`.
- **INV-006, the gate persists.** Only the `/.github/CODEOWNERS` line is core; root `CLAUDE.md` and `docs/decisions.md` stay unowned until rank 11 fires.
- **INV-004, decisions file seed.** The seed sources have not been read by anyone.
- **INV-017, single approver.** Under a sole code owner there is no second eligible approver; see `## Risk`.

What stays UNVERIFIED across the package: who besides the author may convert a PR to Draft; whether Evaluate mode is offered on the Free plan; the default of the stale-approval options; who reads the shared-login review requests (INV-025); the 11-of-100 deletion firing rate; whether sessions obey a root `CLAUDE.md` rule; organisation-level rulesets (token lacks `admin:org`); whether the "required reviewers" ruleset rule is available to this organisation; how often the owner is away; the channel the owner reads.

