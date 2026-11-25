# Position OURS (D16): adopt the heavier prevention package of FULL-REPORT section 11

Written 2026-11-20 for debate D16. Advocate for the owner's line.

## Claim
The incident (PR 681, Clay's design, and PR 682, Clay's deletion of the owner's merged issue-pipeline code, both merged by their own author on 2026-11-20 with no human review) happened because nothing in the repository made a second person say yes. A written agreement alone repeats the 2026-10-22 pattern: a rule told in a meeting, never written (issue 290), never enforced. The package of FULL-REPORT section 11 (nine items) closes the eight gaps of section 10. The cheap-and-enforced items must be taken together: a role definition, a reversal rule, owner-only paths with a real required reviewer, a decision log, and an in-flight register. The repository settings that enforce it are one admin action each.

## Mechanism
Three layers, each catching what the one below misses:
1. Words in the files people and agents read first: a roles paragraph in CONTRIBUTING.md (who "the owner" is, by login), a "Related work" and a "Reverses" section in the PR template, a search-first rule.
2. Visibility: a decision log on master (`docs/decisions/`) and an in-flight register (or draft PRs), so work that today lives in memory files and an unpushed worktree is findable.
3. Enforcement by GitHub, not by goodwill: CODEOWNERS plus "require review from code owners" on a short path list, so a design or a deletion on those paths cannot merge on the author's word alone. Silence then blocks a merge instead of allowing it.

## Cited facts
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

## Cost
Estimates (mine; none measured): roles paragraph and PR template lines, under 1 hour; CODEOWNERS file, 15 minutes; admin settings (ruleset with required code-owner review on the named paths), 15 minutes by `ironbelly` only; decision log with a back-fill of the 8 to 10 rulings other people build on, 2 to 3 hours of agent time once, 5 minutes per later ruling; draft-PR habit, 0 once agreed; `/sc:issue` stop-on-overlap, a protocol change plus tests, about a day; `/sc:overlap`, several days.

## Risk
- A path-limited required review makes the approver a queue: Clay's PRs on `docs/designs/` wait for `ironbelly` (and `ironbelly`'s wait for another code owner unless a bypass is set).
- A required reviewer behind the shared login `ironbelly` proves little (FULL-REPORT.md section 1 item 7).
- A tracked in-flight table rots unless someone edits it every time.
- A stop-on-overlap check on keyword search will stop on noise and be bypassed.

## What it gets right
- Silence becomes a block instead of a yes. That is the property that would have stopped PR 682 merging 66 minutes after it opened.
- It writes down who "owner" means, which is gap 3 and the root of the "approved" status of the design.
- It makes decisions findable (gap 6) and work in flight findable (gap 7), the only items that reach the owner's unpushed plan.
- It takes the fix out of memory and meetings, where the 2026-10-22 rule died (issue 290).
