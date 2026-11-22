# Full report: PR #686, design PR #681, deletion PR #682 and the two lines of work

Written 2026-11-20 by the coordinator (ORCH-IronClaude) for the repository owner. Local file only; not posted to GitHub. All times UTC. "Clay" means the GitHub account `clayphi`. "ironbelly" is the login of the repository owner and also of the sessions on this host, so a GitHub action under it does not show which person acted. Every statement below comes from the eight analyst files in this folder, listed at the end, and from my own spot checks. I marked UNVERIFIED where no source was read.

## 1. The answer in ten lines

1. PR #686 is not new, original work. It rewrites the issue watcher you built in PRs #447 and #448 and implements the design merged in PR #681. It does not use the observer, the sweep or the TUI dashboard.
2. The suspicion that earlier work was not checked is only partly supported. Issue #655 (the plan behind all of it) names #331, #450, #447, #448, #485, #548, #584 and #591, says it "replaces #450", and lists what it keeps and drops. It was filed after a written question to you on #450.
3. It is supported for four things the work did not see or did not cite: your zero-setup watcher plan (local and unpushed), Coder issues #515 and #516, the owner decisions of 2026-11-14 to 2026-11-19 (Decision 6, Q35 to Q41), and the alignment decisions in PRs #587 to #589.
4. The one recorded contact between the two lines is Clay's comment on #450 at 2026-11-18 17:00:32, addressed to `@ironbelly`, ending "What do you think?". No answer exists on GitHub. Issue #655 was filed 2 hours 55 minutes later.
5. The most serious event is PR #682: Clay deleted the code of your merged PRs #584 and #591, three days after you merged them, and merged it about 66 minutes after opening it (corrected on 2026-11-20 by the inventory check; #681 took about 90), with no human review.
6. In #655, #681 and the design, "the owner" means Clay. In your decision records, "the owner" means you. Both are called the owner; nothing says who rules on what. This is the root of the "approved" status of the design.
7. On GitHub, no comment, review, reaction or assignment by `ironbelly` exists on #655, #681 to #684, #686, #687, #689 or #690. Whether you saw them elsewhere (chat, calls) is UNVERIFIED, and the shared login weakens this evidence.
8. A live collision exists now: your worktree `claim-handoff-planb` is building the zero-setup watcher on the old design in the same six files #686 rewrites.
9. No rule in this repository told a contributor to search open issues and PRs before building. The one duplicate check, in `/sc:issue --create`, lists and never stops.
10. Several of Clay's other pieces are complementary and worth folding in (section 6).

## 2. PR #686 in one paragraph

Title "feat(issue-watch): the poll wakes the repo's orchestrator (issue 655, PR A)", head `4e7f12b1a`, 59 files, +14,256 / -16,637, open, not merged. It changes the watcher from "claim an issue, launch a session, wait for an approval comment" to "route a newly assigned issue to a per-repo orchestrator and wake it". New: a registry `.orchestrator/orchestrators.json`, a `hold:plan` label for issues with no plan, wake files, per-repo tier settings, 62 audit reasons. Removed: the claim-session launch, the approval comment code, the trigger and approver settings, the project-board reads. About 88 percent of the deleted lines are old tests. The poll stays `enabled: false`, so nothing runs live. PR B (the orchestrator skill) and PR E (live test) do not exist yet, so nothing on master reads the wake files.

Reuse: the process runner, audit log, lock, call budget and rate-limit code of #447 (design table 4.10). One deliberate copy: `wake.py` ports about 100 lines of `orca_term.py`, now on master via #684. Observer and sweep: no shared code and no reader of the new files.

## 3. PR #682: what was deleted, why, what follows

**What.** PR D, by Clay, merged 2026-11-20 00:02 UTC (commit `01e7a9e23`), 36 files, 4,599 lines removed:
- The package `src/superclaude/cli/issue_pipeline/` (about 1,600 lines): plan hash, the approval-line check (`approved <record-id> plan-sha256=...`), a locked store of adoption rows and approval rows (stops a second worker start), the label and comment rules for approval, GitHub reads, the worker brief, `release-worker`, and the verbs `superclaude issue-pipeline ...`.
- Its tests (about 2,900 lines, including recorded replies from throwaway issue 452) and the `tests/cli` registration test.
- Rule WC-17 and the section "Issue pipeline duties" in `WORKER-CONTRACT.md`, and the first rule of guard G2.
- Kept: the three design notes under `docs/designs/issue-pipeline-*.md`, and the rule that `ask` and `send` carry no `--to`.

**Who built it.** You: PR #584 (Plan A) and PR #591 (Plan B), both merged 2026-11-17, implementing Decision 6 = B, Decisions 2, 3, 5, 7, 8, and Q35 to Q41 in your decision record `owner-answers.md`.

**Why it was deleted.** The stated reasons are Clay's: the PR says "Nothing runs this code: the issue watcher has `enabled: false` and never ran live", and issue #655 lists "the plan-approval gate after the claim" under "Dropped on purpose: the plan is reviewed at creation". Neither the PR, #655 nor the design names Decision 6, route B or Q35 to Q41. #655 does name #584 and #591 as related.

**What follows.**
- Human approval of a plan before a worker implements is gone and not replaced. PR #686 only checks that three plan headings are filled in. Nobody can say "build it" or "no" between plan and implementation.
- The coordinator duties you accepted on 2026-11-18 no longer exist on master. I recorded this in my memory.
- Protections the old tests pinned (one winner when two callers race, a killed start blocks a second start, refusal of bot and edited approvals) have no equal on master. PR B plans some, but nothing is built.
- `/sc:issue` text and the watcher runbook still describe a coordinator handoff that is gone. Installed copies on this host still list the old verbs until the next install.
- Your worktree `claim-handoff-planb` has 53 uncommitted files, including edits to the deleted package. It will conflict on rebase (UNVERIFIED; not tried).

**The case for the deletion.** It never ran live. It relied on a login anyone could use (your own accepted risk L-1). It needed two sessions and a grant row per approval, and you accepted that latency only "for now" (Q36). The author documented the reasons, kept the guard rule that still matters, and had the guard change independently reviewed.
**The case against.** It reverses merged work and recorded decisions of the repository owner without naming them or recording agreement from the person who made them, and it merged without human review.

## 4. Who approved the design in PR #681

- The design says "approved by the owner (Clay) on 2026-11-19 ... (ruling 37)". It never names a GitHub login for the owner.
- The author, the approver of record and the merger of #681 are all `clayphi`. #681 and #655 have no human review, approval, reaction or assignment from anyone else. The PR body says "the owner reviews and merges", and the author merged it.
- Rulings 1 to 39 are kept in a file `RULINGS.md` of the orchestrator session (unread: UNVERIFIED). Every ruling in the sources read was posted under `clayphi`.
- Roles on GitHub: `clayphi` has `maintain`, `ironbelly` has `admin`. No CODEOWNERS file and no role text in CONTRIBUTING.md define who rules on design.
- So the design is "approved" by its author, calling themselves the owner. Whether you agreed outside GitHub is UNVERIFIED.

## 5. What the design (PR #681) does to the existing work

Full table in `H-design681-map.md`. Summary by class.

**Conflicts with your recorded decisions or rules (reconcile or drop):**

| Design element | Your decision it contradicts |
|---|---|
| R1 assignment is the only trigger; no approval label, no approver list, no plan gate | Zero-setup R19, R22, R35, R36: the approval stays the gate (the `Approved` field) |
| R4 Orca automation, no cron | R6 and R16: cron is the scheduler (2026-11-18); Coder #515 |
| R9 claim only at level none | R23 and R25: the Pipeline field picks the launch level |
| DQ6 standing grant list | Per-issue grant row |
| DQ7 workers run with no launch guard | The guard work (#394, #442, #685) |
| DQ8 and ADD1 orchestrator merges and is started by a script | `WORKER-CONTRACT.md`: a coordinator a person opened; acts only on the person's go; `/sc:pr-submit` never as a worker |
| ADD4 a silent reviewer holds the PR | `/sc:pr-submit`: a reviewer with no activity is skipped |
| 5.7 state in another repo, `.orchestrator/` | Q26 in-project `.dev/coordinators/` layout |
| Name `/sc:orchestrator` | "coordinator, not orchestrator" (R10, Coder #516); #444 proposed the same name for another purpose |
| NG-2: the poll writes labels | `issue-watcher.md`: the poll writes nothing to GitHub |

**The cron example in detail.** Your recorded reason (requirements line 18, Coder #515): an Orca automation "starts an agent session with a prompt on each run". The design's answer is a "precheck" step that exits non-zero, so Orca records `skipped_precheck` and starts no agent (its spec 4.8, citing `waker.py`, on master via #684). That would meet your objection if it works as claimed; I have not tested it. The order of the two decisions cannot be fixed: Clay's #450 comment is timed 17:00:32; your cron decision has no hour, and its first dated trace is 17:09:03. No record debates automation against cron; the debate folder covers one dispatcher against one entry per project. The design cites #450's cron item as dropped, and does not cite Coder #515 or the zero-setup plan.

**Silent on, and should say how it relates to:** `/sc:sweep` and WC-16, `superclaude observe` and #409 item 9, #423, #431, and where #444 fits. **Builds on:** the built poller, `/sc:issue --claim`, the `/sc:pr-submit` poll scripts, `/sc:closeout`, ccsession tiers, Orca verbs. **Complements:** the plan hold, the nine-row escalation table, audit AU1 to AU8, the "no GitHub text in a typed line" rule.

## 6. All of Clay's work, sorted

| Group | Items | Evidence |
|---|---|---|
| **Fold in (complementary, no conflict found)** | `/sc:closeout` (#683, issue #668): the claim to #339's `sc:close` is session close, a different job; `agent-work-report` skill (#684); `/sc:issue --plan` and plan sections (#651, #661 merged, #690); worktree cleanup (#687, which matches a duty #339 lists); daily PR log (#670); the 6.0.0 and 6.1.0 removals you approved in #571 (you reversed the swarm removal) | F table rows A and D |
| **Overlap to resolve** | `/sc:orchestrator` name and scope against #339, #444, #423; the work report against `/sc:sweep` and the observer; #689 (moves brainstorm and design into create, changes your claim chain); the dashboard #409 against the living report | F, H |
| **Replaces your work (needs your explicit ruling)** | #682 (deletes #584/#591 and WC-17); #686 (removes the #447 approval and trigger code); #655 "replaces #450" while #450 stays open and assigned to you | E, F |
| **Unrelated** | #499, #570, #608, #619, #628, #630, #666, older ccsession and pr-submit PRs; closed #652, #663 | F |

## 7. How the two lines met, in order

- 10-23: #289 and #290 filed by Clay (rules for worktrees; rules for proposing new primitives). 10-29: you answered "only file issues until we have an eval framework" and gave #290 to Clay. #290 is still open.
- 10-27: Clay's coordinator spec (IronFlow repo, UNVERIFIED, unread).
- 10-30 to 11-08: you filed #331, #339, #409, #423, #431, #444; merged #447, #448; filed #450 (with cron as its item FU-2); closed #331.
- 11-11: Clay's one comment on #409. 11-14: #539 sweep and #548 option 3 merged. 11-17: #584 and #591 merged; alignment records #587 to #589; status reviews including #450 BLOCKED.
- **11-18 17:00:32:** Clay's eight-point proposal on #450, to `@ironbelly`. No GitHub answer.
- 11-18 (hour unrecorded): your zero-setup requirements: cron, the approval gate, "coordinator not orchestrator". 18:25: #651 filed ("No duplicate found", #450 "out of scope"). 18:26 and 18:40: Coder #515 and #516 filed. **19:55: #655 filed**, "replaces #450", cross-referenced on #450 and #331.
- 11-18 20:00 to 11-19 22:19: Clay posts rulings and "body updated" comments on #655; you continue the zero-setup plan (`/sc:implement` started 11-19 15:29).
- **11-19 22:32 to 11-20 02:01:** #681 to #684 opened; **#681 and #682 merged at 00:02 by Clay**; #686, #687, #689, #690 opened; #683 and #684 merged.
- 11-20 01:50: your R36 withdraws the Status gate; your branch is still building in `issue_watch/`.

Points where one line could have seen the other: the #450 mention; the cross-references on #450 and #331; ClickUp direct messages (content unreadable); the plan folders and Coder issues, which postdate or ran concurrent with #655. Your zero-setup plan was never pushed, so no one on GitHub could see it.

## 8. Issues and PRs that should have been referenced first

Precedence is your call; these are the items the sources show as relevant. Cited by #655: #331, #450, #447, #448, #485, #548, #584, #591, #339, #423, #444, #442, Coder #477. **Not cited by #655 or by PRs #681 to #690:** #431, #539, #587 to #589, #613, #636, Coder #515 and #516, the zero-setup plan, your owner-answers record (Decision 6, Q35 to Q41, Q26), and #290 (rule for proposing new primitives, assigned to Clay). #409 is also not cited in them, but Clay commented on #409 on 11-11 at your request, so they knew it. The design document names #331, #450, #339 and #444 inside its text (it says "replacing #450"), although its own "inputs read in full" list omits them. PR #682 cites #655 and #665 but not #584 or #591.

## 9. Where the evidence points the other way

- #655 states its replacements in writing, with reasons and a carry-over list, and posts the proposal on your own issue with an `@` mention before building. It reuses your code and safety features, not a copy.
- You did not answer the #450 comment, and your own decisions of 11-18 and 11-19 sit in an unpushed local plan, memory files and Coder issues that never mention #655. No process required Clay to find them.
- The alignment records you wrote (#587 to #589) mark the watcher-to-orchestrator handoff as DEFERRED, not rejected, and your chain is watcher, then orchestrator, then dashboard. #655 points the same way.

## 10. The gaps that let this happen

1. **No search-first rule.** `CLAUDE.md`, `CONTRIBUTING.md`, the issue templates and the PR template have no "check existing issues and PRs" step. `HOW-WE-WORK.md` says "ask your lead before starting anything large" with no way to know who the lead is.
2. **The duplicate check lists and never stops.** `/sc:issue --create` writes up to ten "possible duplicates" and continues. Claim mode has no duplicate check.
3. **No definition of "owner".** Two documents use the word for two people. No file says who may rule on design, on the worker contract, or on deletions.
4. **Design PRs can be approved and merged by their author.** The repository permits it. The PR body said the owner reviews and merges.
5. **No review requirement for deleting someone else's merged code.** #682 merged with only two bot reviews.
6. **Decisions were not visible.** Your decisions live in memory files, an unpushed plan, local worktrees and Coder issues, not in a tracked decision log on master.
7. **No registry of work in progress.** Nothing on GitHub told Clay a watcher rebuild was running on a local branch, or told you a replacement was being written.
8. **#290 is unfinished.** The onboarding rule for proposing new primitives is open and assigned to Clay.

## 11. Recommended workflow to prevent it

1. **Related-work check, required and visible.** Add a "Related work" section to the issue and PR templates: open issues and PRs found by a stated search, worktrees and branches in flight, and the decisions this reverses (with links). `/sc:issue --create` and `--claim` stop, not list, when an open issue in the same area is assigned to another person, until the author states the relation.
2. **Reversal rule.** A PR that deletes or replaces code from a PR merged in the last 30 days, or a decision recorded in a decision log, must name it and carry a written acknowledgement from that work's author. The PR template gets a "Reverses" line.
3. **Owner-only paths.** Add `CODEOWNERS` with you as required reviewer for `src/superclaude/core/WORKER-CONTRACT.md`, `hooks/`, `issue_watch/`, `docs/designs/` and the sc-issue-protocol skill. Turn on "require approval from someone other than the author" for those paths.
4. **Define roles.** One paragraph in CONTRIBUTING.md: who is the owner for what, who rules on design, who merges what. Replace "the owner" in design documents with a login.
5. **Decision log on master.** A tracked `docs/decisions/` file for every ruling that other people build on, with date, who ruled, and the issue it settles. Push plans as a draft PR within a day of starting, so work in progress is visible.
6. **Claim and in-flight register.** A tracked table (or the `.dev/coordinators/` layout of Q26): area, owner, branch, worktree, status. A new design starts by reading it.
7. **Cooling period for designs.** A design-only PR that changes behaviour others rely on waits for review by the named owner; no self-merge, and no merge within 24 hours of opening.
8. **Automatic overlap scan.** A CI step or a coordinator command (the four-lens scan I just ran, as `/sc:overlap`) that lists open PRs, open issues and local worktrees touching the same paths and posts the list on the PR.
9. **Finish #290.** Close the onboarding rule for new primitives.

## 12. What I recommend now (owner decides each)

1. Do not merge #686 until the conflict list in section 5 has a ruling from you. It is the first of five PRs; later ones build on it.
2. Decide the trigger and gate question (approve label or field, against assignment only) and the scheduler question (cron against an Orca automation, including a test of the precheck claim). Everything else follows from those two.
3. Pause the `claim-handoff-planb` implementation or tell it which design wins. It is editing the same files now.
4. Ask Clay on #655, in writing, for an answer to the section 5 list and for the identity of "the owner" in the design.
5. Do not revert #682 yet. Nothing ran the removed code. Decide whether the plan-approval step is wanted at all; if yes, restore it on top of master as a new PR.
6. Fold in the complementary items (section 6) one at a time, each with its own look at overlap with the sweep and observer.
7. Adopt items 1 to 5 of section 11 first; they cost little and stop a repeat.

## Source files

`/home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/`: `A-past-prs.md`, `B-open-issues.md`, `C-worktrees.md`, `D-master-code.md`, `E-pr682.md`, `F-clay-inventory.md`, `G-history.md`, `H-design681-map.md`. Not read by anyone: the IronFlow coordinator spec, `RULINGS.md`, the orchestrator repo, chat and direct-message content, ClickUp.
