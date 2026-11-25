# D16 Round 2 rebuttal, Variant 2 (CLAY) advocate

Written 2026-11-20, after the OURS Round 2. "They" means Clay (`clayphi`). Every figure marked "re-read" or "my count" was read or computed today with read-only commands (`gh ... --repo IronbellyOrg/IronClaude`, `git log`, `jq`, doc pages). Anything I did not read is marked UNVERIFIED. All costs are estimates, none measured. I wrote nothing to GitHub or Orca and did not touch SuperClaude-Org.

## Position in four sentences

OURS' new measurements mostly hold, and they moved me: I now accept a narrow code-owner ruleset now, a decisions file, and root `CLAUDE.md` as the carrier. I still refuse three pieces of the OURS package: a required pasted deletion check (it fires on 11 of 100 PRs and mostly flags a person's own work), a ruleset with no bypass (it would have blocked the owner's own 3-minute revert on 2026-11-19), and any named fallback who has never acted. I add one thing OURS did not: the open series PR 690 is on no path list in either package, so a one-PR lock is not enough and the open 655 PRs need a direct hold. The two packages now differ by about three items, and I say which.

## Part 1. Testing the OURS measurements

I re-ran the figures that carry weight. Data set: the same 100 merged PRs (merged 2026-11-09 02:00 to 2026-11-20 02:26 UTC; my fetch returned exactly 100 across four date slices, because one 100-PR file query returned HTTP 502).

| # | OURS claim | What I found | Verdict |
|---|---|---|---|
| 1 | 14 of 100 PR bodies carry the template (`## Checklist`); 681, 682, 686 do not | 14 of 100 (`ironbelly` 13, `clayphi` 1). The same 14 also hold "Testing Methods" and "Related Issues", so the count is stable. 681 and 682 do not carry it. 686 is open, so it is not in the merged set and I did not check its body: UNVERIFIED | HOLDS |
| 2 | 89 of 100 merged by their own author; Clay's self-merges stay open median 0.76 h, p90 2.5 h | 89 of 100 (`ironbelly` 57 of 58, `clayphi` 32 of 42). Clay self-merge wait: n=32, median 0.756 h, p90 2.49 h. One `ironbelly` PR was merged by `clayphi` | HOLDS |
| 3 | Owner-merged Clay PRs: 10 PRs, median about 4.4 h, none waited days | Waits (h): 0.2, 0.2, 2.5, 3.3, 3.7, 5.1, 6.2, 6.2, 8.4, 16.9; median 4.4. Limit: this is merged PRs only. I also read the open list: 4 open PRs (685, 686, 690, 693), all created within the last day, none stale | HOLDS, with the survivorship limit |
| 4 | 31 gated PRs in 11 days (15 Clay, 16 owner); 12 on 11-17, 7 on 11-18 | 31 (`clayphi` 15, `ironbelly` 16). 12 on 11-17, 7 on 11-18, 3 on 11-19, 3 on 11-20. `WORKER-CONTRACT.md` 18, `docs/designs/` 16 (`ironbelly` 12, `clayphi` 4). `issue_watch/` 1. Only 3 of the 31 were merged by someone other than the author | HOLDS |
| 5 | PR 686: 59 files, +14,306 / -16,637; 27 added, 26 modified, 6 deleted; 0 of 59 on the two paths | Exact match. 11 files are in `issue_watch/`. Its 24 deleted or heavily rewritten files (6 deleted plus 18 with 50 or more deleted lines) are all last touched inside 30 days and hold 16,486 deleted lines. Where I could map the earlier PR, 8 of those files came from `ironbelly`; 16 I could not map (UNVERIFIED) | HOLDS |
| 6 | Code owners need write access | GitHub docs: "The people you choose as code owners must have write permissions for the repository." One listed owner's approval is enough ("an approval from any of the owners"). The three people with write are `ironbelly` (admin), `clayphi` and `IB-JonathanB` (maintain) | HOLDS |
| 7 | PR 682 matches the two-path list on 1 of 36 files | 1 file: `WORKER-CONTRACT.md`, +1 -12. A test that pins the contract (`tests/skills/test_worker_contract.py`, +8 -54) is in the same PR, which supports OURS' reason that removing the feature forced the contract edit | HOLDS |
| 8 | Edit frequency of the candidate files; `/sc:pr-submit` never mentions the template | Same 100 PRs: `HOW-WE-WORK.md` 22, root `CLAUDE.md` 7, `CONTRIBUTING.md` 0, PR template 0. No hit for the template name in the pr-submit skill folder or command file | HOLDS |
| 9 | `IB-JonathanB` has never acted | `maintain` role. `gh search` for PRs (author, reviewed-by, commenter) and for issues (author, commenter) all returned `[]` | HOLDS |
| 10 | Computed deletion check catches 682 and 686 | 682: 28 of 28 deleted or heavy rows are under 30 days old (4,523 recent deleted lines). 686: 24 of 24 (above). Both caught | HOLDS |
| 11 | Rulesets and the dry-run mode: OURS marked both UNVERIFIED | New, from me: the organisation plan is `free` (`gh api orgs/IronbellyOrg`). GitHub docs say rulesets are "available in public repositories with GitHub Free". "Evaluate" mode exists, but I could not confirm it is offered on Free: still UNVERIFIED | Resolves one UNVERIFIED for both sides |

Two things OURS did not test, which I did, and which change the debate:

1. **How often the computed check fires.** OURS wrote "I did not measure how often it fires on ordinary PRs." I ran the same two commands (a deleted file's first-add date; a heavily rewritten file's last touch before the PR) over all 100 PRs. It flags **11 of 100 PRs** (at least one recent file), 9 of them with 200 or more recent deleted lines. That is about one a day. Nine of the 11 are `clayphi`'s PRs (9 of their 42) and 2 are `ironbelly`'s (2 of 58). The flagged PRs are 620, 629, 632, 640, 650, 653, 656, 658, 662, 664, 682. Method limit: "recent" means any edit in the last 30 days, so a one-line edit makes an old file count; and I mapped "whose work" through the PR number in the commit subject, which fails for older PRs (labelled unknown below).
2. **Whose work the flagged files were.** For PRs 650, 656 and 658 the earlier work on the flagged files was the author's own (24, 16 and 18 files mapped to `clayphi`). Only 3 flagged PRs delete mostly someone else's recent work: 682 (27 of 28 files from `ironbelly`'s PRs), and 662 and 664 (19 and 22 files from `clayphi`'s PRs). PRs 662 and 664 are the owner's revert of release PR 658 at 01:17 on 11-19 (merged 3 minutes later) and the re-landing at 01:20 (merged by `clayphi` 27 minutes later). Why the owner did that: UNVERIFIED.

What this does to OURS' claims:
- "I expect it to fire often": it fires on 11 percent, so it is not noise-level, but the first-order result is that most firings are an author editing their own recent work.
- The two-path list caught every large deletion in the window. The six PRs with more than 4,000 recent deleted lines (650, 656, 658, 662, 664, 682) all touch `WORKER-CONTRACT.md`. The three flagged PRs that are off the two paths (632, 640, 653) have 391, 295 and 315 recent deleted lines. So in these 11 days the path list had full recall on the large cases. I said in Round 1 that 682 was caught only by luck; the contract edit is not luck, it is how features are removed here. I withdraw that.
- 17 of the 18 contract PRs change the contract by 15 lines or fewer (median 5, largest 45, line counts from the PR file lists). So the contract path gates mostly small edits; 18 of the 31 gated PRs come from it.

## Part 2. The remaining disputes

### R-1. Narrow code-owner ruleset now versus hold behind a tripwire

**Final position: I accept it now, in OURS' narrow form, with three changes (below).** I moved from "hold in reserve". Reasons, from the tests:
- The owner is responsive on PRs: median 4.4 h on Clay's PRs they merged, none over 17 h, and no stale open PR. This was my main fear (a block that stalls) and the data does not support it for PR review. It does not cover questions in issue comments: the 450 question has had no answer for two days.
- The two paths caught all six large deletions in the window.
- Rulesets are free here (plan `free`, public repository). Turning it off is one admin action.
- OURS is right that a tripwire needs someone watching merges, and nobody is. The coordinator report on 681 and 682 came the day after.

What I do not accept, and why:

1. **"No bypass list" is wrong.** PR 662 (the owner's revert of the 6.1.0 release) touches `WORKER-CONTRACT.md`. Under a no-bypass symmetric gate it waits for Clay's approval, and the 3-minute revert becomes a wait. Any gate needs an emergency path and the only mechanical one is a bypass. I ask for the repository admin role as a bypass actor in "for pull requests only" mode (the docs list this option; individual users cannot be bypass actors, but `ironbelly` is the only admin, so it is the same thing). This also answers the cost to the owner: 16 of the 31 gated PRs are the owner's, and with the bypass they do not wait on Clay at all. The honest price: the gate then binds `clayphi` and not the owner, and sessions on the shared `ironbelly` login can use the bypass. That already describes how the owner's PRs merge today (57 of 58 self-merged), so it is no loss, but the owner should say in chat that they accept a one-directional gate. If the owner prefers symmetry, I accept it and the revert case is simply a wait. Whether owner sessions must pass `gh pr merge --admin` to use the bypass: UNVERIFIED.
2. **Test the zero-approval setting before the ruleset exists.** OURS marked "0 approvals plus code-owner review" as UNVERIFIED. The GitHub docs I fetched say nothing against it; one community report says it works with approvals set to 0. If it cannot be made to block on owned paths with 0 approvals, a required approval of 1 would apply to every PR (89 of 100 were self-merged), which is a different and much larger cost. In that case I drop the ruleset and fall back to my Round 1 hold. The throwaway-PR test is a condition, not a courtesy.
3. **The temporary `issue_watch` line: acceptable, with its limit stated.** It is cheap (1 of 100 PRs besides 686 touches that path) and it is the only lock on 686. But it does not cover PR 690 ("issue 655, PR P", open, +2,811 -39, 13 files, none on `docs/designs/`, `WORKER-CONTRACT.md` or `issue_watch/`) or later PRs of the series. So the open 655 PRs also get a direct hold (item 2 of the table): the owner says in chat that 686 and 690 wait for the owner's ruling, and Clay sets them to Draft. A draft PR cannot be merged ("No one can merge the pull request", GitHub docs). Whether a maintainer other than the author can convert it: UNVERIFIED; the author can. This is a speed bump, not a lock, because the author can mark it ready again. I rely on the line only for 686.

Cost to the owner, stated plainly: without the bypass, 16 PRs in 11 days (about 1.5 a day) wait for Clay, and 12 of the 31 landed on one day (11-17). With the bypass the owner's wait is 0 and the owner's added work is the throwaway test (5 minutes) and the 14-day review (20 minutes). Cost to Clay: 15 PRs in 11 days wait for the owner, at the response times above.

**What would change my mind back to "hold":** (a) the zero-approval test fails (point 2); (b) the owner says in chat that they cannot answer a gated review within one working day and will not name a deputy; (c) the 14-day review shows a median wait over one working day or any wait over 3 working days. In case (c) the first cut is the contract path, but see item 8 of the table: it is also the path that catches deletions, so it should be replaced by the CI check rather than simply dropped.

### R-2. Both triggers, with a computed deletion check pasted into the PR body

**Final position: the computed check is a modest improvement in precision, not a clear improvement in safety, and as a required paste it is over-engineered. I keep the "30 days" sentence, add the commands as an optional helper, and do not make the paste mandatory.**

Evidence:
- **It does not fix the failure it was meant to fix.** The author of 682 skipped the check; an author can skip the paste the same way. OURS' own answer is that "one skipped paste is the trigger for building the check". That is a tripwire, the same device OURS rejects for the ruleset in R-1. I accept the tripwire here and say it applies there only because the two-path ruleset already covers the large cases.
- **It adds little over the path list in the measured window.** On top of the two paths it flags 632, 640 and 653 (295 to 391 recent deleted lines each) and, if it were run today, 686. Nothing at the scale of the incident.
- **It flags mostly a person's own work.** In 8 of the 11 firings the earlier work on the flagged files is the author's (or unknown). The rule "name the person whose work it touches and quote their written yes" has no one to name in those cases.
- **It has no exception for reverts.** A revert PR deletes someone else's recent merged work by definition. PRs 662 and 664 are the proof. A rule that demanded Clay's written yes for the owner's revert would be dropped or ignored on its first use.
- **It adds machinery.** Two commands in the rule text that every session must run, a threshold that "a person has to set" (OURS' words), and a recency test that counts a one-line edit as recent.

What I keep from it: the commands are good. A session that wants to know whether a PR removes someone's recent work gets a precise answer in a minute. I would put them in the rule text as "to check, run" and keep the written sentence, with the revert exception written in: "Deletes or rewrites code merged in the last 30 days: yes or no, whose, and where their written yes is. A revert of a PR merged in the last 7 days is exempt and is reported to its author the same day." A written sentence plus an optional helper plus the second-person gate on the two paths covers the cases the data shows.

**What would change my mind:** one PR after the ruleset is live that deletes or rewrites 200 or more lines of someone else's recent code, merges with no second person, and is off the two paths. Then the CI check (item 8) is built and made required. Also: if the owner or Clay says in chat that the paste is cheap in practice and wants it, I accept it as a written rule, not a check.

### R-3. One file `docs/decisions.md` seeded with about 10 rulings versus a one-time publish through issue comments

**Final position: I accept the file. I concede this one.**

What moved me:
- The standing rule changes who records. The owner gives rulings in chat and the agent records them (memory rule, 2026-11-17). So the file does not depend on the owner writing anything, which was my rot worry in Round 1.
- The coordination sessions search pushed code with Augment, which sees a file and does not see issue comments. A ruling in a comment on #655 is invisible to the next session that does not know #655 exists. This is a real advantage of the file, and I had not weighed it.
- Cost parity: both are about 1 to 2 hours of session time to draft, and OURS dropped the folder and the full back-fill.

Conditions I attach:
1. The seed has only the rulings that open work depends on (OURS' list of about 10 groups from FULL-REPORT section 5). Nothing else goes in until a ruling is given.
2. The owner approves the wording in chat before it merges, and the same session posts one line on #655 and one on #450 pointing at it, so Clay does not have to find a new file to learn that rulings exist.
3. Each entry says how the owner gave it ("chat, date") and quotes the owner's sentence. Clay cannot see the owner's chat, so for Clay the quote is a claim made by an agent. That limit exists with any recording method.
4. The file is not on CODEOWNERS (item 9 of the table).
5. The seed source, `owner-answers.md` and `RULINGS.md` in the owner's sessions, has not been read by me or by OURS: UNVERIFIED. If it is already published somewhere durable, there is nothing to seed.

**What would change my mind:** if fewer than three entries are added in 30 days after the seed while the owner gave rulings in that time, the file is rotting and I would move the rulings to issue comments. Or if the owner says in chat that issue comments are the record.

### R-4. Silence fallback: ask-again timer of 3 working days; the owner names a deputy or "nobody" in chat

**Final position: ACCEPT, with two additions.**

I accept that the 3 working days is a timer to ask again and never a timer that grants permission. I accept that the owner decides once, in chat, who rules when they are away, and that the default is "nobody". I accept that it applies only to work that reverses or deletes someone else's merged work, so other work proceeds (the cost of waiting falls on the person who wants to reverse). I accept that any one non-author code owner satisfies a gated review.

Additions:
1. **Do not write `IB-JonathanB` in anywhere until they have said yes in an issue comment.** The data confirms they have never acted here (Part 1, row 9), and nobody has recorded asking them. A named person who was not asked is a paper fallback. I would also leave them off CODEOWNERS for now: they add nothing while two active people cover each other, and they would be auto-requested on every gated PR (about 31 in 11 days) with no sign they would answer.
2. **The owner names the channel they read.** The 450 question sat unanswered for two days, while PR reviews were answered in hours. The rule text must say where a question to the owner goes so that "ask again" has an address. Which channel: UNVERIFIED; the owner says in chat.

**What would change my mind:** if `IB-JonathanB` authors, reviews or comments on anything and agrees in writing, I would name them default deputy. If the owner rules in chat that after 3 working days an author may proceed on a reversal, that is the owner's call and the rule says so.

### R-5. Rule text in root `CLAUDE.md` (carrier), pointers elsewhere, PR template as reminder only

**Final position: ACCEPT.**

The template reaches 14 of 100 PRs and none of the two incident PRs; `/sc:pr-submit`, the mandated way to open a PR, never mentions it; neither the template nor `CONTRIBUTING.md` was edited once in 100 PRs. Root `CLAUDE.md` is read by every session in the checkout, is edited (7 of 100 PRs), and already carries the one other rule about how a PR is opened (the PR-target rule). I withdraw my Round 1 placement of the text in `CONTRIBUTING.md`. I also accept the correction on `CONTRIBUTING.md:77-79`: line 75 is the heading "Disclaimer: social convention, not a CI-enforced gate" and the passage is about one CI rule (the rot budget), not team governance. I cited it wrongly.

One cost OURS understates. A pointer in `HOW-WE-WORK.md` is not two lines of work: the project `CLAUDE.md` says an edit there must be copied byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and the level table re-copied into `src/superclaude/core/CLAUDE.md`, with tests checking both. About 15 more minutes, and the file is edited often (22 of 100 PRs), so conflicts are likely. I would still do it, because the owner's 2026-10-29 answer on #290 says rules go there, and the owner can rule otherwise in chat. Whether sessions obey a root `CLAUDE.md` rule: UNVERIFIED.

## Part 3. Final ranked, costed, ordered package

"Admin only" means `ironbelly`, the only admin; `clayphi` and `IB-JonathanB` have `maintain`.

| Rank | Item | Cost estimate | Who can do it | Do now / after / drop |
|---|---|---|---|---|
| 1 | Roles said in chat by the owner: who rules on designs, deputy or "nobody", the channel the owner reads, "a question to a named person gets a written answer"; Clay accepts in writing in the PR that carries the text | 10 min owner chat, 10 min Clay | Owner decides in chat; a session records; `clayphi` accepts | Now |
| 2 | Direct hold: the open 655 series PRs (686 and 690) wait as Draft for the owner's ruling | 5 min | Owner says it in chat; `clayphi` converts (a maintainer doing it: UNVERIFIED) | Now |
| 3 | Rule text: root `CLAUDE.md` section (roles; silence never a yes; 3 working days to ask again; reversal or deletion of someone else's merged work needs their written yes and a different merger, with the revert exemption; publish a plan as a draft PR or issue comment within a day; the two helper commands, optional); pointers in `HOW-WE-WORK.md` and `CONTRIBUTING.md`; two reminder lines in the PR template. Finishes #290 | 60 to 90 min, one PR | Any maintainer or session; `clayphi` as #290 assignee | Now |
| 4 | `docs/decisions.md` seeded with about 10 ruling groups, plus one line each on #655 and #450 | 1 to 2 h session time, a few min owner chat | Any maintainer or session drafts; owner approves the wording in chat | Now (the 686 reconciliation needs it) |
| 5 | `.github/CODEOWNERS`: `docs/designs/`, `src/superclaude/core/WORKER-CONTRACT.md`, and a temporary `src/superclaude/cli/issue_watch/` line; owners `ironbelly` and `clayphi` (no `IB-JonathanB` yet) | 15 min | Any maintainer, by PR (inert until rank 6) | Now |
| 6 | Ruleset on `master`: PR required, 0 approvals, code-owner review, no force push, no deletion, admin role as bypass for pull requests only; run a throwaway PR first and use "Evaluate" first if the option is offered | 15 to 30 min | **Repository admin only** | Now, after rank 5 merges and the throwaway test passes |
| 7 | 14-day review: count gated PRs, median wait, any wait over 3 working days; remove the temporary `issue_watch` line when the owner says in chat the 655 series is reconciled | 20 min | Owner and `clayphi`; the CODEOWNERS edit is any maintainer | After (14 days after rank 6) |
| 8 | CI check for deletions of recent code (modelled on `boundary-guard.yml`, advisory today); made required only on a tripwire | 2 to 4 h | Any maintainer writes it; **admin only** to make it required | After, only if a large deletion of someone else's recent code merges off the two paths, or the review in rank 7 removes the contract path |
| 9 | CODEOWNERS on root `CLAUDE.md` and `docs/decisions.md` | 5 min plus about 7 extra gated reviews per 11 days | Any maintainer edits; the ruleset enforces | Drop, unless the rule text is edited by the author of a gated PR without the other person's written accept |
| 10 | Draft PR or issue comment within a day for work others could collide with | 0 | Everyone (inside rank 3) | Now |
| Drop | `/sc:overlap`; stop-on-overlap in `/sc:issue`; 24 hour cooling timer; tracked in-flight register; `docs/decisions/` folder with index and full back-fill; required pasted deletion check; a ruleset with no bypass; naming `IB-JonathanB` as fallback before they agree; the five-path OURS list; changing `/sc:pr-submit` to inject the template | | | Drop |

Total "do now": about 3 to 4.5 hours of session or maintainer time, 15 to 30 minutes of admin time, about 25 minutes of owner and Clay chat. Rank 6 is the only item nobody but the owner can do; ranks 1, 2 and 4 need the owner's word in chat.

Where this differs from the OURS final package: ranks 1, 3, 4, 5, 6, 7, 10 are the same in kind. The differences are the direct hold (rank 2), the admin bypass and the zero-approval condition (rank 6), the optional helper instead of a required paste (rank 3 against OURS rank 2), the CI check kept as a tripwire (rank 8, same as OURS), and no named fallback (rank 5).

### The lightest version that would have prevented the incident

Ranks 1, 3, 5 and 6 limited to the two paths, with the 14-day review: it is about 2.5 hours plus 15 to 30 minutes for the admin, and it gives a second person on `docs/designs/` and `WORKER-CONTRACT.md`, which would have stopped both 681 and 682, because both PRs touch those paths. Words alone (ranks 1 and 3) cost about 1.5 hours and prevent the incident only if sessions obey a `CLAUDE.md` line, which I cannot show and which PR 681's own body ("the owner reviews and merges") argues against.

### The version I would still refuse

A ruleset with no bypass that gates the owner's own PRs, grows to the five-path list (45 percent of recent merges, per OURS' own Round 1 count), and sits next to a required paste on 11 percent of PRs would make both people queue on named paths and teach sessions to work around the gate, and it would have blocked the owner's own revert on 2026-11-19. I would also refuse any item that adds commands or CI the owner said on #290 not to build yet, and any fallback that depends on a person who has never acted here.

## Part 4. Shared assumptions

- **A-001 (the owner or an alternate answers within a bounded time): QUALIFY.** The package bounds what it can (any one non-author code owner, 3 working days to ask again, deputy or "nobody" named by the owner), and PR reviews were answered in a median of 4.4 h, but the unanswered 450 question shows the channel matters.
- **A-002 (the rule reaches the sessions that do the work): ACCEPT.** The template reaches 14 of 100 PRs and `/sc:pr-submit` ignores it; root `CLAUDE.md` is the carrier (whether sessions obey it: UNVERIFIED).
- **A-003 (Clay accepts `ironbelly` as owner for design rulings): QUALIFY.** The owner says it in chat and Clay accepts it in writing in the PR that carries the text, before the ruleset is announced; the merged design's "approved by the owner (Clay)" has to be settled in the same PR.
- **A-004 (the next collision will look like this one): QUALIFY.** In the 11-day window the two paths caught all six large deletions, but they miss PR 686 and PR 690 type work (rewrites and additions on other paths), and only the publish rule, the decisions file and the CI-check tripwire reach that.

## Part 5. What I now concede

1. The ruleset on a narrow path list should be switched on now. My "hold behind a tripwire" is withdrawn.
2. The contract path catching 682 is not luck: all six large deletions in the window touch `WORKER-CONTRACT.md`. My Round 1 "brittle path list" argument is withdrawn.
3. The file `docs/decisions.md` is better than issue comments, because Augment search sees files and not comments, and because agents record the rulings.
4. Root `CLAUDE.md` is the carrier, not `CONTRIBUTING.md`; and I cited `CONTRIBUTING.md:77-79` wrongly.
5. A tripwire fires after the harm and nobody watches merges; for 686 specifically I accept the temporary `issue_watch` line as a lock.
6. The 3 working days as an ask-again timer, and "nobody" as the default when the owner names no deputy.
7. The owner is responsive on PR review (median 4.4 h on the 10 merged Clay PRs, no stale open PRs), which was the basis of my stall fear.

## UNVERIFIED and not done

Whether "0 approvals plus code-owner review" blocks on owned paths; whether "Evaluate" mode is offered on the Free plan; whether a maintainer other than the author can convert a PR to Draft; whether owner sessions need `gh pr merge --admin` under a bypass; whether 686's body carries the template; whether sessions obey a root `CLAUDE.md` rule; why the owner reverted and re-landed release 6.1.0; the contents of `owner-answers.md` and `RULINGS.md`; the channel the owner reads; how often the owner is away; whether `IB-JonathanB` wants any role. My recency test counts any edit in 30 days and maps "whose work" through the PR number in commit subjects, so the 11-of-100 and the own-versus-other split are approximate (16 of 686's files and some others are unmapped).
