# D16 Round 2 (rebuttal): advocate for Variant 1 (OURS)

Written 2026-11-20. "They" means Clay (`clayphi`). All figures below were read today with read-only commands (`gh ... --repo IronbellyOrg/IronClaude`, `git log`, `jq`, grep on `/home/coder/.cache/ic-snap-20261120/master`). Anything I did not read is marked UNVERIFIED. All costs are my estimates, none measured.

## 0. What I measured for this round (new since Round 1)

| Fact | Value | How read |
|---|---|---|
| Window | 100 merged PRs, 2026-11-09 to 2026-11-20 (about 11 days) | `gh pr list --state merged --limit 100` (a limit of 200 returned HTTP 502) |
| Merged by their own author | 89 of 100 (`ironbelly` 57 of 58; `clayphi` 32 of 42) | same list, `mergedBy` |
| How long Clay's self-merged PRs stay open | median 0.76 h, 90th percentile 2.5 h (n=32) | same |
| How long Clay's PRs stay open when the owner merges them | 10 PRs: 0.2, 0.2, 2.5, 3.3, 3.7, 5.1, 6.2, 6.2, 8.4, 16.9 h; median about 4.4 h, none waited days | same |
| PRs touching `WORKER-CONTRACT.md` / `docs/designs/` / `src/superclaude/cli/issue_watch/` | 18 / 16 / 1; union of the first two 31 (`clayphi` 15, `ironbelly` 16); `docs/designs/` alone: `ironbelly` 12, `clayphi` 4 | same |
| Gated PRs per day | 2.8 on average; 12 on 2026-11-17 (a day with 26 merges), 7 on 2026-11-18 | same |
| PR bodies that carry the template (`## Checklist`) | 14 of 100 (`ironbelly` 13, `clayphi` 1); PRs 681, 682 and 686 do not | `gh pr list --json body` |
| Does `/sc:pr-submit` mention the template | No hit for `PULL_REQUEST_TEMPLATE` in its skill folder or command file | grep of the snapshot |
| How often the candidate "words" files change (same 100 PRs) | `HOW-WE-WORK.md` 22, root `CLAUDE.md` 7, `CONTRIBUTING.md` 0, PR template 0 | `--json files` |
| PR 682 | 36 files; 27 are DELETED files, and all 27 were first added on 2026-11-16 or 17; it matches the two-path list on 1 file (`WORKER-CONTRACT.md`, +1 -12), the full OURS list on 4 files (orchestrator's count) | `gh pr view 682 --json files`, `git log --diff-filter=A` |
| PR 686 (open, by `clayphi`, no approval, title "issue 655, PR A") | 59 files, +14,306 / -16,637; 27 ADDED, 26 MODIFIED, 6 DELETED; 0 of 59 files on `WORKER-CONTRACT.md` or `docs/designs/`; 11 source files and many test files on `issue_watch`; 18 files with 50 or more deleted lines, all last touched within 30 days, holding 16,322 of the 16,637 deleted lines | `gh pr view 686 --json files`, `git log -1` |
| `IB-JonathanB` | role `maintain`; no authored PR, no reviewed PR, and `gh search issues --commenter IB-JonathanB` printed nothing | `gh api .../collaborators`, `gh search` |
| Master | `branches/master/protection` still 404; `rulesets` still `[]` | `gh api` |

Two of these change my Round 1 position, so I say so now. My Round 1 told you to drop `issue_watch/` from the list because neither 681 nor 682 touched it. I never tested the open PR. PR 686 matches the two-path list on nothing and the old list only through `issue_watch`. And Round 1 said I did not know whether a better sentence behaves differently; the template figure (14 of 100, none of the three PRs) shows a sentence placed in the template would not even have been seen.

## R-1. Ruleset on master with code-owner review: now, or hold behind a tripwire

**Final position: switch it on now, in the narrow form, with a written 14-day review and an off switch. Merge the CODEOWNERS file first so the switch is one admin action.**

The form (this is smaller than my section 11 list and close to what they said they would accept):
- CODEOWNERS paths: `docs/designs/`, `src/superclaude/core/WORKER-CONTRACT.md`, and `src/superclaude/cli/issue_watch/` marked temporary (remove it when the owner says in chat that the five-PR series from #655 has been reconciled).
- Code owners: `ironbelly`, `clayphi`, `IB-JonathanB`. Any one code owner who is not the author satisfies the review, so an inactive third name blocks nobody. All three have write access (`admin`, `maintain`, `maintain`), which GitHub requires of code owners (fetched docs page: owners "must have write permissions").
- Ruleset on `master` (admin only): pull request required, required approvals 0, require review from code owners, block force push, block deletion, no bypass list. Whether "0 approvals plus code-owner review" behaves as I describe is UNVERIFIED; the admin should try it on one throwaway PR before announcing it (about 5 minutes).

Why now and not behind their tripwire ("one self-merged design or deletion after the agreement lands"):
1. **The exposure is still open.** The report calls #686 the first of five PRs, and the median Clay self-merge stays open 45 minutes. Master is unprotected today (404, `[]`). A tripwire that needs one more event means the next event is the plan.
2. **A tripwire fires after the harm and depends on someone seeing it.** 681 and 682 were found by a coordinator analysis written the day after, not by an alert. I have no evidence of any detector. The harm from 682 was 4,599 deleted lines of work the owner had merged three days earlier (FULL-REPORT section 4); I cannot cost it in hours (UNVERIFIED).
3. **The cost of switching on is bounded and reversible.** At the measured rate the gated list is 31 reviews in 11 days, split 15 on the owner and 16 on Clay, about 1.4 a day each. The owner already merged 10 of Clay's PRs at a median of 4.4 hours open. Turning it off is one admin click (delete the ruleset or set it to disabled).
4. **The one thing that would justify waiting is not available.** A dry run ("evaluate" mode) would let you see the queue without blocking. A web search summary of GitHub's docs says that mode is Enterprise-only and that rulesets work on public repositories on Free; the two doc pages I fetched did not say either, so treat both as unconfirmed. This organisation's plan is UNVERIFIED.

The queue is real and I will not wave it away. On 2026-11-17, 12 PRs would have needed a second human on a day with 26 merges. Two things bound it: the 14-day review below, and the fact that the owner's 16 gated PRs now wait on Clay (or the third name), which is a cost to the owner that my Round 1 did not state.

14-day review (owner and Clay, about 20 minutes): count gated PRs, their median wait, and any that waited more than 3 working days. If the median wait is over one working day, drop `WORKER-CONTRACT.md` from CODEOWNERS first (it is 18 of the 31 and the least tied to the incident), keep `docs/designs/` and `issue_watch`.

**What would change my mind.** (a) The owner says in chat that they cannot answer a gated review within one working day and will not name a deputy: then a hard block turns into a stall and I would hold behind their tripwire, with CODEOWNERS already merged. (b) The owner rules in chat on the whole #686 conflict list (FULL-REPORT section 5) and orders the five PRs in sequence under their own named approval: then the in-flight exposure is covered by a person, and I would accept the hold. (c) The throwaway PR shows that code-owner review cannot be made to block with 0 required approvals and no workable alternative exists.

## R-2. Trigger: short path list, or "design PR or deletion of code merged in the last 30 days", or both

**Final position: both, and make the second one computed rather than judged.** The two incident PRs and the open one show that each trigger alone misses one of them.

| PR | Two-path list (`docs/designs/`, `WORKER-CONTRACT.md`) | `issue_watch` line | Computed deletion check |
|---|---|---|---|
| 681 (design, +1,412 -0) | caught (`docs/designs/orchestrator.md`) | no | not caught (nothing deleted) |
| 682 (-4,599) | caught, by 1 file of 36 (`WORKER-CONTRACT.md`, +1 -12); the full OURS list matches 4 of 36 | no | caught (27 of 27 deleted files added within 30 days) |
| 686 (-16,637, open) | not caught (0 of 59) | caught | caught (16,322 of 16,637 deleted lines sit in files last touched within 30 days) |

They are right on the point that matters: 682 is caught by the path list because a 13-line edit to the contract came with it. The ten source files of `src/superclaude/cli/issue_pipeline/` and the test files that carry most of the deletion are not on any list I proposed. A pure deletion would have gone through. The reason it is not pure luck is that the contract has a test pinning it to the pipeline (`tests/skills/test_worker_contract.py` is in the 682 file list), so removing the feature forced a contract edit; code the contract never mentions has no such tie. I cannot promise that tie holds for the next PR.

Their trigger has a different weakness: the author applies it, and the author of 682 did not name #584 or #591 (FULL-REPORT section 8). I tested a way to remove the judgment. The rule text carries two commands the author pastes the output of into the PR body:

1. List deleted files: `gh pr view <N> --repo IronbellyOrg/IronClaude --json files --jq '.files[] | select(.changeType=="DELETED") | .path'`.
2. For each path, and for any modified file with 50 or more deleted lines, print when it was added or last changed: `git log --all --diff-filter=A --format=%cs -1 -- <path>` for deleted files, `git log origin/master --format=%cs -1 -- <path>` for modified ones.

Result when I ran it: PR 682, 27 of 27 deleted files dated 2026-11-16 or 2026-11-17; PR 686, 18 of 18 heavy-deletion files last touched inside 30 days. Limits, stated plainly: I ran it on these two PRs only; I did not measure how often it fires on ordinary PRs (the repository is young, so I expect it to fire often and the threshold has to be set by a person; UNVERIFIED); a rewrite inside an old file would not show. The threshold is my guess; both incident PRs are far above any figure I would pick (a few hundred deleted lines).

Rule when the output shows deleted lines in recently merged code: the PR body names the person whose work it touches and quotes their written yes, and a person other than the author merges. A server cannot enforce this part. A required CI check could, and that is the item I hand to their tripwire (see the table, rank 8): the pasted output is the first signal, and one skipped paste is the trigger for building the check.

**What would change my mind.** If the owner or Clay shows that the computed check wrongly flags a large share of ordinary PRs (say, more than a third), I would drop the computed check to "advisory in the PR body" and keep only the path list and the written 30-day sentence.

## R-3. Decision log: `docs/decisions/` folder with back-fill, or one-time publish

**Final position: one file, not a folder: `docs/decisions.md`. Seed it once with only the rulings that open work depends on. Add one line on #655 and one on #450 pointing at it.** This takes their "or one file" option and keeps a durable place that sessions can grep.

Why not a folder and a full back-fill: I concede it. A folder with an index and cross-references costs more than one file, and nothing I can show needs more until the file has far more entries than the ten I can name (my guess: about 50).

Why a file and not only issue comments: the issue is not that comments are hard to search. The rulings that were missed were never on GitHub (the zero-setup plan, Coder #515 and #516, `owner-answers.md`, Decision 6, Q35 to Q41: FULL-REPORT section 1 item 3). Publishing them is the fix, and both of us agree on that. A comment on #655 serves the reconciliation of #686 today. A file serves the next session that does not know #655 exists. They cost the same to draft, so I take the file and add the comment links.

Seed set (about 10 groups, from FULL-REPORT section 5): R19, R22, R35, R36 (the approval stays the gate); R6 and R16 (cron is the scheduler); R23 and R25 (the Pipeline field picks the launch level); the per-issue grant row; Q26 (the `.dev/coordinators/` layout); R10 (coordinator, not orchestrator); Decision 6 and Q35 to Q41. The source is `owner-answers.md` in the owner's sessions, which I have not read (UNVERIFIED). Cost: 1 to 2 hours of session time to draft, and a few minutes of the owner's chat time to approve the text.

**How rulings get recorded from now on, given the owner gives them in chat and never writes a file** (standing rule in memory: every approval and ruling is given by the owner in chat and recorded by the agent):
1. The session that hears the ruling adds one entry to `docs/decisions.md`: date, ruled by (login), where given ("chat"), what it settles, the issue number, recorded by (session name if it has one).
2. It goes in the next PR that session opens for that area, with the owner's chat sentence quoted in the PR body. No stand-alone PR, no ceremony.
3. If open work depends on the ruling right away, one line on the issue the same day, and the entry follows with the next PR.
4. The owner approves the wording in chat before the entry is merged, so no one writes a ruling for them. The shared login hides which session posted; the quoted chat sentence is the only evidence of the owner's word, and that is a limit I cannot remove.

**What would change my mind.** If `owner-answers.md` or `RULINGS.md` turns out to be already published somewhere durable, there is nothing to seed. If the owner rules in chat that issue comments are the system of record, I would drop the file.

## R-4. Silence fallback: 3 working days, then a named alternate

**Final position: the 3 working days is a timer for asking again, never a timer that grants permission. The named alternate is not a plan, because nothing shows `IB-JonathanB` has ever acted here.**

Evidence: `maintain` role; no authored PR, no reviewed PR, no issue comment found. Writing his name in as the fallback gives a paper fallback. I would still list him as a third code owner, because any one code owner is enough and an inactive name blocks nobody. I would not rely on him.

There are two different silences, and they need different answers:

1. **A question that needs a ruling, and the work reverses or deletes someone else's merged work.** Silence is never a yes, at any length. After 3 working days the author asks again in the same thread by name and on the channel the owner reads (which channel that is, I do not know: UNVERIFIED; the owner names it in the roles paragraph). Meanwhile the author may continue only work that does not reverse or delete: additive work, work behind a flag or on another path, or work in the author's own area. A second maintainer's opinion may be asked for and recorded as advice; it is not a ruling. The cost of this wait falls on the person who wants to reverse, which is where it belongs.
2. **A review request on a gated path.** Any one code owner who is not the author is enough. The two active people cover each other. The owner does not have to be the one. If both are away, nothing on those paths merges, and I accept that.

**Who rules when the owner is away.** The owner decides this once, in chat, and the agent records it in the roles paragraph: either "deputy for design rulings from <date> to <date>: <login>", one chat line per absence, or "nobody; designs wait". If the owner says nothing, the default is nobody. A deputy may not rule on their own PR or on reversing their own earlier work. How often the owner is away: UNVERIFIED.

**What would change my mind.** If `IB-JonathanB` (or anyone else) reviews or authors a PR here, I would name that person as default deputy. If the owner rules in chat that after 3 working days an author may proceed on a reversal, that is their call and I would write it in.

## R-5. Where the words go, and the CONTRIBUTING.md correction

What I measured about each file (section 0): the PR template reaches 14 of 100 PRs and none of 681, 682, 686, because a PR opened with `--body` replaces it and `/sc:pr-submit` never mentions it. `CONTRIBUTING.md` and the template were not edited once in 100 PRs. `HOW-WE-WORK.md` is edited often (22 of 100) but is not loaded at session start (per the owner's own global instructions) and reaches `~/.claude` only after `superclaude install`; editing it also requires a byte copy to `plugins/superclaude/skills/sc-recommend/refs/` and a level-table copy, with tests checking both (root `CLAUDE.md` line 346). Root `CLAUDE.md` is read by every session in the checkout, and it already holds the one rule that governs how a PR is opened (the PR-target rule, lines 39 to 79), for the same reason: a setting does not carry it.

| File | What goes there | Why |
|---|---|---|
| Root `CLAUDE.md` | Source text: new section "ABSOLUTE RULE: who rules, and what needs a second person" (about 12 lines): roles by login; silence is never a yes, 3 working days to ask again; reversal or deletion of someone else's merged work needs their written yes and a different merger; the two computed commands; publish a plan as a draft PR or issue comment within a day | Read at session start by every session; precedent in the PR-target rule. 7 edits in 100 PRs, so it is warm |
| `HOW-WE-WORK.md` | Two-line pointer to that section | The owner's 2026-10-29 answer on #290 puts rules there; the owner can rule otherwise in chat. A pointer avoids two copies drifting |
| `CONTRIBUTING.md` | One line for humans and new members pointing to the section | Cold file; humans read it, sessions do not |
| PR template | Two lines: `Related work (include unpushed plans and other repositories):` and `Deletes or rewrites code merged in the last 30 days (paste command output or "none"):` | A reminder for the 14 percent of PRs that use it; not the carrier |

Correction, once and for both sides: `CONTRIBUTING.md:77-79` is not team governance. Line 75 is the heading "Disclaimer: social convention, not a CI-enforced gate" and lines 77 to 79 are about one CI rule, the rot budget for test failures. It says "Enforcement relies on PR reviewers checking the rule during code review." Strike it from both fact lists. The only use it has is the sentence it ends on: a convention needs a reviewer, and 89 of 100 recent merges were merged by their own author. I am not claiming that shows a written rule fails here; they were right to say no written rule existed before today (their Round 1 concession 3).

## Final ranked, costed, ordered package

All costs are estimates. "Admin only" means `ironbelly`, the only admin (`clayphi` and `IB-JonathanB` have `maintain`).

| Rank | Item | Cost | Who can do it | Do now / after / drop |
|---|---|---|---|---|
| 1 | Roles in chat: the owner says who is owner for what, who rules on design, who is deputy when away (or "nobody"), and which channel they read; Clay accepts it in writing in the PR that carries the text (prerequisite for A-003) | 10 min owner chat, 10 min Clay | Owner decides in chat; `clayphi` accepts | Now |
| 2 | Rule text: root `CLAUDE.md` section, pointers in `HOW-WE-WORK.md` and `CONTRIBUTING.md`, two PR-template lines, silence rule, reversal rule, the two computed commands, publish within a day. Finishes #290 (assignee `clayphi`) | 45 to 75 min, one PR | Any maintainer or session; `clayphi` as #290 assignee | Now |
| 3 | `.github/CODEOWNERS` on the three paths, owners `ironbelly`, `clayphi`, `IB-JonathanB` (inert until rank 4) | 15 min | Any maintainer, by PR | Now |
| 4 | Ruleset on `master`: PR required, 0 approvals, code-owner review, no force push, no deletion, no bypass list; try it on one throwaway PR first | 15 to 30 min | **Repository admin only** | Now, after rank 3 merges; review at 14 days; off switch is one click |
| 5 | `docs/decisions.md` seeded with about 10 ruling groups; one line each on #655 and #450 | 1 to 2 h session time, a few min owner chat | Any maintainer or session drafts; owner approves in chat | Now (the #686 reconciliation needs it) |
| 6 | 14-day review of the gate: count gated PRs, median wait; drop `WORKER-CONTRACT.md` from CODEOWNERS first if the median wait is over one working day; remove the `issue_watch` line when the #655 series is reconciled | 20 min | Owner and `clayphi`; the CODEOWNERS edit is any maintainer | After (14 days after rank 4) |
| 7 | Draft PR or issue comment within a day for work others could collide with | 0 | Everyone | Now (inside rank 2) |
| 8 | CI check that fails when deleted lines in recently touched files exceed a threshold and no non-author approval exists, modelled on `boundary-guard.yml` (98 lines, advisory today); making it required is admin only | 2 to 4 h | Any maintainer writes it; **admin only** to require it | After, only if one PR skips the pasted output (their tripwire, applied to this item) |
| 9 | Put root `CLAUDE.md` and `docs/decisions.md` on CODEOWNERS so the rule text cannot be quietly edited | 5 min plus about 7 extra reviews per 11 days | Any maintainer edits CODEOWNERS; the ruleset from rank 4 enforces it | After, only if the rule text is edited by the author of a gated PR |
| Drop | Tracked in-flight register; 24 hour cooling timer; `/sc:overlap`; stop-on-overlap in `/sc:issue`; `docs/decisions/` folder with an index and full back-fill; changing `/sc:pr-submit` to inject the template; naming `IB-JonathanB` as the fallback | | | Drop |

Total "do now": about 2.5 to 4 hours of maintainer or session time, 15 to 30 minutes of admin time, about 20 minutes of owner and Clay chat. Rank 4 is the only item that nobody but the owner can do; ranks 1, 2 and 5 also need the owner's approval in chat.

## Answers to A-001 to A-004

- **A-001 (the owner or an alternate answers within a bounded time): QUALIFY.** True and unstated in both. My package bounds what it can: any one code owner suffices for a gated review, the 3 working days only triggers asking again, and the owner names a deputy or "nobody" in chat. It does not rely on `IB-JonathanB`, who is not shown active.
- **A-002 (the rule reaches the sessions that do the work): ACCEPT.** It was a flaw in both texts. The template reaches 14 of 100 PRs and none of the three here; root `CLAUDE.md` is the file every session reads.
- **A-003 (Clay accepts `ironbelly` as owner for design rulings): QUALIFY.** The ruleset needs only "a person who is not the author"; the owner's yes needs agreement. Settle it once, in chat, accepted by Clay in the PR (rank 1), before the ruleset is announced.
- **A-004 (the next collision will look like this one): QUALIFY.** The union of the path list, the `issue_watch` line and the computed check catches all three PRs here; any one alone misses one. A large feature PR on unlisted paths that deletes nothing is still not caught; only draft PRs and the decision file reach it.

## What I now concede

1. The path list alone is fragile: 682 is caught through 1 of 36 files, and 686 is not caught by the two paths at all. I was wrong in Round 1 to drop `issue_watch` without testing 686.
2. Their 30-day deletion idea is needed; I add a computed form so the author does not judge it. I concede the deletion check as a required CI check belongs behind their tripwire.
3. The `docs/decisions/` folder and full back-fill: dropped for one file.
4. 3 working days is accepted, as an ask-again timer. The named alternate is dropped as the fallback.
5. The PR template is not a carrier (14 of 100); `HOW-WE-WORK.md` is not auto-loaded. Root `CLAUDE.md` is the carrier.
6. The gate moves a real cost onto the owner: 16 of the 31 gated PRs are the owner's and would now wait on Clay (or a third name). The queue is 12 PRs on the worst day measured.
7. A ruleset cannot prove it was the owner's own yes under the shared login; it proves a login other than the author's said yes.

## UNVERIFIED and not done

Whether "0 approvals plus code-owner review" blocks as described; whether GitHub blocks an author approving their own PR (the doc page I fetched did not say; it is known GitHub behaviour but I did not read it here); whether rulesets are free for this organisation and whether "evaluate" mode exists (web search summary only); the computed check's false-positive rate; whether the owner reads a second channel; contents of `owner-answers.md` and `RULINGS.md`; whether sessions obey a root `CLAUDE.md` rule; who the owner is for design rulings (A-003). I wrote nothing to GitHub or Orca and did not touch SuperClaude-Org.
