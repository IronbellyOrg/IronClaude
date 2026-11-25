# D16 Round 1: advocate for Variant 1 (OURS, the heavier package of FULL-REPORT section 11)

Written 2026-11-20. Facts re-read today with read-only commands (`gh ... --repo IronbellyOrg/IronClaude`, grep, Read) against `/home/coder/.cache/ic-snap-20261120/master` and the FULL-REPORT. Anything I could not read is marked UNVERIFIED. "They" means Clay (`clayphi`).

## 1. Position summary

Take Variant 2's words (they are the cheapest and some are better than ours), add one server-side control that only the admin can switch on, and drop the four items of section 11 that cost days or rot. A sentence in a file did not stop PR 682, because PR 681's own body already said "the owner reviews and merges" and its author merged it about 90 minutes after opening it (FULL-REPORT.md section 4). So I defend Variant 1 in a narrowed form: the full nine-item package is not worth its cost for three maintainers, but "words plus a mechanical second reviewer on a short path list" is.

### Ranked, costed set (my estimates; none measured)

| Rank | Item | Cost | Who can do it | Verdict |
|---|---|---|---|---|
| 1 | Roles by login (owner, maintainers) and a silence rule ("a question to a named person is answered in writing; silence is never a yes"), with a named alternate and an expected reply time. Put it in `HOW-WE-WORK.md` and `CLAUDE.md`, not only CONTRIBUTING.md | 30 to 60 min | any maintainer | Do first. Variant 2's sentence is good. |
| 2 | PR template: `Reverses:` line and one `Related work:` line that must include unpushed plans and other repositories | 15 min | any maintainer | Do first. |
| 3 | Draft PR or issue comment within a day for work others could collide with | 0 once agreed | everyone | Do first. This replaces the tracked in-flight table. |
| 4 | Finish #290 with the same text | about 1 hour | `clayphi` (assignee) | Do, as the vehicle for ranks 1 to 3. |
| 5 | Ruleset on `master`: pull request required, no force push, code-owner review required on a short path list, no bypass for the shared login if the admin can stand it | 15 min plus review time | repository admin (`ironbelly`) only | Do second, within the week. The only item that turns silence into a block. |
| 6 | `CODEOWNERS` file on that short path list | 15 min | any maintainer can commit it; it only bites after rank 5 | Do with rank 5. |
| 7 | Decision log `docs/decisions/`, back-filled only for the rulings FULL-REPORT section 5 lists as contradicted (Decision 6, Q26, Q35 to Q41, R6, R16, R19, R22, R23, R25, R35, R36), about 10 rulings | 2 to 3 hours once, 5 min per later ruling | any maintainer | Do third. The only item that publishes what lives in memory files. |
| Drop | Tracked in-flight register table; 24 hour cooling timer; `/sc:overlap`; `/sc:issue` stop-on-overlap | days, or cannot be enforced, or rots | | Drop for now. Reasons below. |

Only the admin can: create the ruleset or branch protection, require code-owner review, block force pushes, set or remove the bypass list, and make `boundary-guard.yml` a required check (its lines 19-20 say that "is a repository-settings decision"). Org-level rulesets could not be read here (needs `admin:org`): UNVERIFIED. Whether an "evaluate only" ruleset mode exists on this plan: UNVERIFIED. The repository is public (`gh api repos/IronbellyOrg/IronClaude` returns `private: false`), so I expect rulesets need no paid plan, but I did not confirm that: UNVERIFIED.

## 2. Steelman of Variant 2

The strongest version: the evidence shows two missing facts, not a missing machine. First, nobody wrote down who "the owner" is, so "approved by the owner (Clay)" was a sincere reading, not a trick (FULL-REPORT.md sections 1 item 6 and 4). Second, a question to a named person went unanswered (Clay's comment on #450, 2026-11-18 17:00:32, and nothing from `ironbelly` after the 2026-11-17 comment; I re-read the comment list today) and the author took silence for a yes. Both are fixed by four sentences and one template line, in an hour, with no admin setting.

Variant 2 also gets these right, and I accept them:
- The unpublished work is the real miss. The zero-setup plan, Coder #515 and #516 and the owner's rulings were not on GitHub. No search, template section or scan reaches them. Only publishing does (FULL-REPORT.md section 1 item 3, section 9).
- Gates cost the team that is building fastest. In the last 60 merged PRs, 51 were merged by their own author, none has an APPROVED review decision (I re-ran `gh pr list --state merged --limit 60`: 37 authored by `clayphi`, 23 by `ironbelly`, 51 self-merged, 0 approved).
- The shared login weakens any "approval by `ironbelly`" (FULL-REPORT.md section 1 item 7).
- A new `/sc:overlap` command would sit badly with the owner's 2026-10-29 answer on #290 ("only file issues until we have an eval framework"), and the section 11 path list as written would make the owner a queue. I measured that (section 5 below).

## 3. Strengths claimed (Variant 1)

1. **A sentence in a file did not hold in this very incident.** FULL-REPORT.md section 4: the PR body said "the owner reviews and merges", and the author merged #681 anyway. #682 was merged 66 minutes after opening (`gh pr view 682`: created 2026-11-19T22:56:28Z, merged 2026-11-20T00:02:36Z; reviews: `augmentcode COMMENTED` only). Variant 2's item 3 ("merged by someone other than its author") is the same kind of sentence that was already broken, and nothing in Variant 2 would make it bind.
2. **A path trigger is mechanical; a self-classified trigger is not.** Variant 2 triggers on "a design PR" and "a PR that deletes code merged in the last 30 days", both judged by the author. #682 never named #584 or #591 (FULL-REPORT.md section 8, last line). By path, both PRs of the incident would have been caught: #681 changed `docs/designs/orchestrator.md`; #682 changed `src/superclaude/core/WORKER-CONTRACT.md` and `src/superclaude/hooks/scripts/launch-level-guard.sh` (`gh pr view 681|682 --json files`, read today).
3. **The state of the repository permits the miss and nothing else is looking.** `gh api .../branches/master/protection` returns 404 "Branch not protected"; `gh api .../rulesets` returns `[]` (read today). Both caught PRs merged with no human review.
4. **The recorded owner decision already asks for a reviewer.** Issue #290, owner comment of 2026-10-29: "pr approved first by reviewer" for primitive changes, rules to live in `HOW-WE-WORK.md`. A required reviewer is not new policy; it enforces a decision already taken.
5. **The written-agreement vehicle has already been tried once and has not landed.** #290 was handed to `clayphi` on 2026-10-29; the owner's status review of 2026-11-17 says "nothing has been written down since". I grepped master's `HOW-WE-WORK.md` today for "propose", "new skill", "recommend --plugin": no rule (only an unrelated brainstorm line at 54). Whether a local branch has it: UNVERIFIED. I do not blame Clay for this; I say a written rule needs an enforcement path as well, or it waits on whoever is busy.
6. **Part of what was missed was searchable.** Variant 2 says no search would have helped. FULL-REPORT.md section 8 lists items not cited by #655 or #681 to #690: #431, #539, #587 to #589, #613, #636 and #290 are numbered items of this repository (613 and 636 are merged `ironbelly` PRs that touch `WORKER-CONTRACT.md` or `docs/designs/`, from my path scan; I did not open the others, so that they are findable by search is UNVERIFIED). Four others (zero-setup plan, Coder #515 and #516, owner-answers record) were not on this repository. So a one-line "Related work" prompt can help for about two thirds of the listed misses, if each was findable. It does not need a new command.
7. **Decisions become findable.** A decision log is the publishing vehicle that Variant 2 itself says is needed (its fact 4: "only the owner publishing them does"). Variant 2 asks for publishing but gives no place to publish rulings; its only trail is issue comments, which is how Decision 6 and Q35 to Q41 stayed invisible.

## 4. Weaknesses identified in Variant 2

1. **Misread of the evidence for "this repo governs by convention".** Variant 2 fact 2 cites CONTRIBUTING.md:77-79. Line 75 is the heading "Disclaimer: social convention, not a CI-enforced gate" and line 77 begins "This rot-budget rule is a social convention". It is a disclaimer for one CI rule about test failures, not a statement of team governance. It also ends "Enforcement relies on PR reviewers checking the rule during code review", and 0 of the last 60 merged PRs has an approved review. So the cited passage shows a convention that depends on reviewers who were absent.
2. **The package depends on exactly the behaviour that failed.** Silence is covered "only by a sentence" (Variant 2's own risk list). X-003: it asks for a second person on design and deletion PRs but gives no way to get one. PR 682 had only a bot comment.
3. **The roles paragraph goes where sessions do not read it.** CONTRIBUTING.md is not referenced from the root `CLAUDE.md` (grep of the snapshot, no match), and the repository is worked largely by Claude sessions that load CLAUDE.md and skills. See A-002.
4. **Self-classification again.** The trigger "deletes code merged in the last 30 days" asks the author to run the check that the author skipped in #682.
5. **No audit trail.** Rulings stay in issue comments (Variant 2's own risk list). the design says "approved by the owner (Clay) ... (ruling 37)" with no login, and rulings 1 to 39 sit in a file `RULINGS.md` of the orchestrator session that no one has read (FULL-REPORT.md section 4: UNVERIFIED).
6. **A one-sided fix is a fix someone has to accept.** Variant 2 writes "owner = `ironbelly`" into a file `clayphi` edits (via #290). The merged design says the owner is Clay. If they do not agree, the paragraph is a statement, not a settlement. A server setting does not need their agreement to hold (but does need the admin; see A-003).

## 5. Concessions (genuine weaknesses of Variant 1)

1. **The path list of section 11 item 3 is too wide.** I counted it on the last 60 merged PRs (`gh pr list --state merged --limit 60 --json files`): `WORKER-CONTRACT.md` 17, `hooks/` 11, `docs/designs/` 10, `sc-issue-protocol/` 6, `issue_watch/` 1. The union of just `WORKER-CONTRACT.md` and `docs/designs/` is 24 of 60 (40 percent); the full list is 27 of 60 (45 percent). These 60 PRs span about four days of unusually fast agent-driven work (#583 to #683), so the rate is a burst, not a steady state, but a one-admin approver on that list is a queue. Variant 2's fact 8 is right on this point. `issue_watch/` and the sc-issue skill did not appear in either #681 or #682 and add nothing to catching them; I would drop them from the list.
2. **The shared login limits what the gate proves.** A required code-owner review by `ironbelly` can be satisfied by a session on the owner's host. And GitHub does not let an author approve their own PR, so the owner's own PRs on a one-owner list either need a bypass (which sessions can also use) or a second code owner. My fix is two or three code owners on the short list (the admin plus the other maintainers). That gives "a second human who is not the author", which is the property that would have stopped #682. It does not give "the owner's yes". The owner's yes stays a written-rule matter (rank 1).
3. **The 24 hour cooling period cannot be enforced by GitHub.** A required review replaces it. Only a custom status check could enforce a timer, and that is more code for little gain. Drop it.
4. **The in-flight table rots** unless someone edits it every time (Variant 1's own risk list). Draft PRs do the same job for free. Drop the table.
5. **`/sc:overlap` and `/sc:issue` stop-on-overlap cost days and fire on noise** (Variant 1's own risk list). The claim path already stops on an issue assigned to someone else (`src/superclaude/skills/sc-issue-protocol/refs/claim.md:42`), and the create path lists possible duplicates and does not stop (`refs/create.md:20`). The real gap is that Clay did not go through `--claim`; a template line reaches them where a command change does not. Drop for now.
6. **Variant 2 is right that unpublished work is the central miss**, and a decision log only helps if the owner pushes rulings to it. A rule on the owner is easy to skip. I have no mechanical answer to that; I only say the ruleset does not depend on it.
7. **A required review stalls when the reviewer is away**, and neither package says who rules then. I propose a named alternate and an expected reply time in the roles paragraph (A-001).
8. **All my cost figures are estimates, none measured.**

## 6. Shared assumptions

- **A-001 (the owner or an alternate answers within a bounded time): QUALIFY.** True for both and unstated in both. Under Variant 2 a missed answer becomes a merge, which is the incident. Under Variant 1 it becomes a stall, which is annoying but not harmful. So the assumption matters for safety in Variant 2 and for speed in Variant 1. The fix for both: a second named person in the roles paragraph and an expected reply time written down. GitHub cannot enforce a deadline.
- **A-002 (the rule reaches the sessions that do the work): ACCEPT, and it is a flaw in both texts as written.** Root `CLAUDE.md` has no reference to CONTRIBUTING.md (grep of the snapshot). The 2026-10-29 owner decision on #290 puts rules in `HOW-WE-WORK.md`, which sessions are told to read. So the words go to `HOW-WE-WORK.md` and the project `CLAUDE.md`. A server-side ruleset is the only layer a session cannot skip, which is Variant 1's one real structural advantage here.
- **A-003 (Clay accepts `ironbelly` as owner for design rulings): QUALIFY.** Words need their agreement; a ruleset does not, but needs the admin. GitHub already records the roles: `ironbelly` admin, `clayphi` and `IB-JonathanB` maintain, seven others read (`gh api .../collaborators`, read today). If they disagree with "owner = `ironbelly`" that has to be settled by a person, once, in writing, before either package works. I treat that as a prerequisite, not a cost of one variant.
- **A-004 (the next collision looks like this one): QUALIFY.** The path gate catches any PR on those paths whatever its shape; it does not catch a large feature PR elsewhere that duplicates open work. The shape-independent items are the decision log and draft PRs. I do not claim to cover a different shape with the gate.

## 7. Per-point table

| Point | My position | One-line evidence |
|---|---|---|
| S-001 | Neutral | Layout only; three layers are a presentation of the same items. |
| S-002 | Neutral | Variant 2's facts are mostly counter-evidence; some are accurate (fact 8, fact 5), one misread (fact 2). |
| C-001 | Both causes real; mine is the one a rule can fix | Unanswered question (450 comments) and undefined owner (section 10 item 3) are inputs; a 66 and 90 minute self-merge on an unprotected `master` is the failure. |
| C-002 | Favour V1, narrowed | `protection` returns 404, `rulesets` returns `[]`; #681 and #682 merged with no human review. |
| C-003 | Favour V1 | #681 touched `docs/designs/`, #682 touched `WORKER-CONTRACT.md`; #682 named neither #584 nor #591. |
| C-004 | Converge, with one change | Same paragraph; put it in `HOW-WE-WORK.md` and `CLAUDE.md` too (#290 owner comment, 2026-10-29). |
| C-005 | Take V2's sentence and add the block | One-sentence rule costs nothing; a required reviewer makes silence block. |
| C-006 | Concede the command, keep one template line | Eight of the twelve uncited items in section 8 are numbered items of this repository; four are not. Stop-on-overlap is a day of work for a partial benefit. |
| C-007 | Favour V1, back-fill only about 10 rulings | Section 5 table of FULL-REPORT lists the contradicted decisions; Variant 2 has no publishing place. |
| C-008 | Concede to V2 | Draft PR within a day replaces the register table at zero cost. |
| C-009 | Concede to V2 | GitHub cannot enforce a 24 hour timer; the required review does the work. |
| C-010 | Concede to V2 | Days of work; the miss was partly unpublished work no scan reaches (section 1 item 3). |
| C-011 | Both true; finish #290 | Spoken rule of 2026-10-22 unwritten, and the 2026-11-17 status review says nothing written since 2026-10-29; the same issue is the right vehicle. |
| C-012 | Variant 2 is cheaper; Variant 1 narrowed is affordable | My scan: 24 of 60 recent merges touch the two core paths; so the list must be narrow and shared among maintainers. |
| C-013 | Partly concede | Shared login limits proof, not the second-human property; use several code owners and no bypass if possible. |
| X-001 | Same data, different reading | 51 of 60 self-merged, 0 approved: trust works until it is a deletion of someone else's merged work (#682). |
| X-002 | Partly V2 | Four of twelve uncited items were unpublished; eight were numbered items here (findability UNVERIFIED). Publishing plus one template line, not a scan. |
| X-003 | Favour V1 | PR 681 body already said "the owner reviews and merges"; the author merged it. A convention without a reviewer did not hold. |

## 8. Prose on the points that matter most

**C-002 and X-003 (enforcement).** The incident is the proof that a written line is not enough: #681 said the owner reviews and merges, and it merged 90 minutes later by its author. Variant 2 answers with a better sentence. I cannot show that a better sentence behaves differently, and Variant 2 admits the risk ("nothing stops a self-merge, master stays unprotected"). A ruleset with code-owner review on a short list is one admin action (about 15 minutes). That is the only line in either package that changes the result when someone is busy or sure of themselves.

**C-003 and C-012 (trigger and cost).** A path list is the one trigger no author has to remember, and it would have fired on both incident PRs. But it also fires on 40 to 45 percent of the recent merges, so I narrow it: only `WORKER-CONTRACT.md` and `docs/designs/` (drop `issue_watch/` and the sc-issue skill, which neither incident PR touched), set several maintainers as code owners, and review after two weeks how many PRs waited and how long (a count I have not made). If the waits are bad, drop the ruleset and keep ranks 1 to 4, which is Variant 2 plus a template line.

**X-002 and C-006 (search versus publish).** Variant 2 is right that nothing finds an unpushed plan, and that is the miss that mattered most. It overstates by saying the miss was not searchable: eight of the twelve uncited items in FULL-REPORT.md section 8 (#431, #539, #587 to #589, #613, #636, #290) are numbered items of this repository, though I did not test that a search would have found each. A one-line template field, "Related work, including unpushed plans and other repositories", is enough. I do not defend a new command.

**C-007 (decision log).** Variant 2 and I agree the owner's rulings must be published. They give no place to put them. A short file is the place, and its first use is the ten contradicted rulings of FULL-REPORT.md section 5, which are exactly what #686's author needs to reconcile. Without it, "publish them" is a request to the person who did not answer the last request.

**C-013 and A-003 (the shared login and who is owner).** Both limits are real and both are prerequisites, not arguments against the ruleset. Two code owners on the short list make the gate "a human who is not the author" even under the shared login. Who is the owner is a conversation to have once, in writing, whichever package is taken.

