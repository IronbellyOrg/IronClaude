# Open decisions and questions: orchestrator, observer, issue watcher and approval flow

**Status as of 2026-11-16 evening (Q16 and Q19 answered 2026-11-15; routed answers from another program recorded 2026-11-16, see section 3 item 11; agent triage of the open questions on 2026-11-16, see section 3 item 12; Q7, Q8, Q13, Q14, Q15, Q24 and Q41 answered the same evening, see `owner-answers.md` "2026-11-16, evening": nothing is waiting for an answer, two items wait for a go). Written for someone arriving with no context, a person or an AI agent. Read the preamble first; it is short.**

## Preamble: what this is and why it exists

### The program in plain words

The owner of this repository (`IronbellyOrg/IronClaude`, a fork of SuperClaude) is building a chain of tools so that AI coding sessions can work on many issues across many git worktrees, while a person stays on top of everything from one dashboard. The intended chain is:

1. **An issue monitor** (the "watcher", `superclaude issue-watch`) notices an approved GitHub issue and starts a session that claims it.
2. **A coordinator** (a Claude session a person opens) starts and supervises worker sessions in separate worktrees, keeps a decision ledger, and does not edit code itself.
3. **A read-only status report** (the "sweep", `superclaude sweep run`, command `/sc:sweep`) lets the coordinator see what its workers are doing.
4. **A terminal dashboard** (the "observer", `superclaude observe`) shows Orca workers to a person. Orca is the local app that runs the sessions.
5. **A knowledge layer** ("Orchestrator v2", issue #423) would later share what agents learn. Not started.

### What exists today (verified 2026-11-14 and 2026-11-15)

- Built and merged: the sweep (PR #539, merged 2026-11-14, master commit `4d3c0b126`), the observer (PRs #503 and #514), the watcher (PRs #447 and #448; never run live; its schedule is not installed), and a design amendment for the watcher (PR #548, merged).
- NOT built, and this file never claims otherwise: the handoff from the watcher to a coordinator (route B, being planned), a coordinator that manages work end to end, the knowledge layer, and any dashboard screen where a person answers questions or approves plans. The observer's coordinator-questions panel is switched off (`QUESTION_GATE_PASSED = False`).
- The sweep is on master but is not runnable on the owner's workspace yet (Q29 below).

### How decisions were prepared

Five independent reviews and a structured debate produced a plan (the "merged requirements", about 1,350 lines) and 33 owner questions. Each question got three proposals and a three-way debate with a recommendation. Questions that were safe, reversible and needed none of the owner's own knowledge were accepted for the agent. The rest went to the owner. The owner answered many on 2026-11-13 to 2026-11-15. **This file lists what is still open.**

### Where everything is

All paths are in this repository on the branch this file is committed to, under `.dev/brainstorms/20261113-orchestrator-tui-alignment/` unless marked otherwise.

| File | What it is |
|---|---|
| `owner-questions/open-decisions.md` | This file: the status board and the open cards |
| `owner-questions/owner-answers.md` | The dated record of every answer the owner gave, with limits and open points |
| `owner-questions/accepted-answers.md` | The 12 answers accepted for the agent, with limits |
| `owner-questions/01-classification.md` | Why each of the 33 questions went where it went |
| `owner-questions/human-decisions.md` | The original 21 owner cards (2026-11-14); many are now answered; kept for history |
| `owner-questions/later-notes.md` | Notes filed for later (a second GitHub account for approvers) |
| `owner-questions/Q<nn>/card.md` and `final.md` | One question's card, and its debate result with the recommendation |
| `owner-questions/Q02-approval-flow/final.md` | The approval flow design (who may tell an agent to proceed) |
| `owner-questions/Q26-coordinator-layout/final.md` | The layout and naming for `.dev/coordinators/` |
| `merged-requirements.md` | The full plan; its section 3 lists the original recommended answers |
| `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md` | The source of truth for facts, with evidence |

The route B plan (18 to 19 tasks) is NOT in this repository yet: it lives in a local worktree named `claim-handoff-b` (see "Other open items", item 1).

### How to answer

Each open card ends with a one-line reply format, for example `Q7: option 1, I will commit them myself`. Answer in any order, a few at a time. "Reply with the default" is always allowed: every card says what happens if you say nothing. What is still waiting for the owner is listed in one block at the end of section 1.

### Rules for any agent reading this file

- You may explain, compare and recommend. You may NOT answer an owner question for the owner, and an answer here is never a grant.
- A **grant** is the owner's separate approval for one outward action (a push, a merge, a post to GitHub, a live test). A reply to a question is not a grant. A grant for one action or one PR never covers another.
- Never interact with the upstream repository `SuperClaude-Org/SuperClaude_Framework`. Pull requests go only to `IronbellyOrg/IronClaude` through `/sc:pr-submit --monitor 3`.
- This repository is currently PUBLIC (checked 2026-11-14). The owner accepted that everything pushed is publicly readable for now. Do not add secrets or tokens.
- Re-read live state (PR state, issue `updatedAt`, Orca) before acting on any fact here. Facts in this file are dated.
- Owner preference (2026-11-16, all sessions): acknowledge an answer once, briefly (for example "Received"), without repeating it, then go to the next applicable question. Do not invent a question or give duplicate receipts.

### Ten terms used below

- **Orca**: the local app that runs Claude sessions in separate git worktrees and records who works on what.
- **Run, Task, Dispatch, worker**: Orca's records. A Run is one coordinated piece of work, a Task is a job in it, a Dispatch is one attempt, a worker is a session doing it.
- **The sweep / the observer / the watcher**: see "The program in plain words".
- **A grant**: see above.
- **INV-008**: the security finding that the sweep's `git status` could run programs named in git configuration. Fixed in PR #539.
- **G1 and G2**: two ways to run the plan-writing worker. G1 runs it without the launch-level guard, only for one test issue. G2 changes the guard so a worker can ask and be released; required before any other issue.
- **The launch-level guard**: a hook that blocks a governed session from committing, pushing, posting to GitHub or running `/sc:implement` until a person releases it.
- **FU-1**: the watcher's first live test.
- **Route A / route B**: how an approval reaches the plan-writing agent. Route B (chosen): the coordinator starts the agent as a supervised Orca worker, and approval travels through Orca's own `ask` and `reply`.
- **W0 to W5**: the plan's waves (steps). A question "gates" a work item when that item cannot start until it is answered.

---

## 1. Status board for all questions

**Nothing is waiting for an owner answer after the evening of 2026-11-16.** The triage cut the list from 11 to 3 (Q7, Q24, Q41); the owner then answered those three and also Q8, Q13, Q14 and Q15 (see `owner-answers.md`). The triage was an agent recommendation after a three-way debate (`ponytail-cuts-adversarial/final-cut-list.md` in this folder), not an owner answer. Say `reinstate Q<nn>` to put any deferred card back. **One item waits for the owner, not an answer:** the remaining Q8 record fields once the owner has read the draft paragraph. The Q24 captures are done (2026-11-16), see `Q24/capture-findings-20261116.md`.

State: **ANSWERED** = the owner answered; **ACCEPTED** = the debated recommendation was accepted for the agent (reversible, no grant); **OPEN** = needs the owner (card in section 2); **OPEN, SHRUNK** = still open in a smaller form; **TRIMMED (default applies)** = the card's own "if you do not answer" outcome applies, labelled as a default and never as an owner answer; **DEFERRED** = waits for a named event; **MOOT** = overtaken by events.

| Q | Topic in plain words | State | What was decided, or what is missing |
|---|---|---|---|
| Q1 | Fix or accept the git-config hole in the sweep | ANSWERED | (a) fix. PR #539 merged with the fix: fsmonitor off on every git call, submodules ignored (owner chose this), a worktree where a selected filter could run is reported `unscanned`. The route scope (a2, b) was settled by the merge; the owner has not restated it. Residual limits are listed on GitHub issue #547 |
| Q2 | Watcher claim level and permission mode | ANSWERED | Option 3 (default claim level: worktree plus a second agent), with Decisions 1 to 9 (see `owner-answers.md`). Route B partly replaces it. The written acceptance for the first live test is recorded: permission checks off for both sessions, one test issue only |
| Q3 | Coder#477 workspace listener | ANSWERED | Narrow to read-only status and identity, no prompt routing; the reply is NOT posted (needs a grant and Q22) |
| Q4 | What "TUI Panel" meant | ANSWERED | Owner's own line recorded; NOT posted. Idea: keep single-host with a read-only API a TUIBBS dashboard connects to |
| Q5 | Keep both programs, one contract note | ACCEPTED | |
| Q6 | When to switch on the observer's questions panel | ACCEPTED (half) | Not before the seeded test. The scope sentence stays the owner's and returns later |
| Q7 | Save the owner's decision records from a side checkout | ANSWERED and DONE (2026-11-16) | Owner confirmed the 2026-11-12 pass record is theirs and said go with the recommendation. Backup made at `/home/coder/backups/issue-409-mvp-20261116/` (bundle with the two unpushed commits, tarball of 119 untracked files, patch of tracked changes, `SHA256SUMS.txt`), no push, no commit. The two commits (`1ae72e1a1`, `f104ca51a`) still go into no PR or merge without their own grant |
| Q8 | The dated design-direction record for #409 | ANSWERED in part (2026-11-16); draft paragraph written, record fields still open | Owner direction: ANSI-enhanced TUI with panes, tabs and panels, "cool" and very functional, taken from the approved images in #409. Draft paragraph: `owner-questions/Q08/visual-direction-paragraph.md` (agent-written at the owner's instruction, not yet confirmed as theirs). The other record fields (defaults, post-link choice, fallback date, stack, command name, meaning of "production integration") are not answered. The #409 correction waits on them |
| Q9 | Store the sweep's JSON output | ACCEPTED | Not now |
| Q10 | May the sweep read Orca messages | ACCEPTED | The observer's alone for now |
| Q11 | What the "static report in chat" is | ACCEPTED | The sweep summary only |
| Q12 | Routing-guide row for the observer | ACCEPTED | One row, own small PR after #539 (now possible) |
| Q13 | May the observer fall back to a plain `orca` command | ANSWERED (2026-11-16) | Owner: "Yes" = option 1. The contract note records both lookup rules, the limit (proves "this is Orca", not "the same Orca the sweep reads") and the Orca build per capture. One fact to keep: the observer's probe runs the candidate program once before checking it is Orca (`src/superclaude/cli/install_user_setup.py:259`) |
| Q14 | What "#339 is complete" means for #423's start | ANSWERED (2026-11-16) | Owner: "option 1 accepted". v2 waits for the sweep merge (done) and the shared capture record; the code fix for the sweep's `working` class stays a follow-up. Never make a code change a start gate. The capture was made on 2026-11-16 (Q24): it shows the running-worker values and the `agentWait` key, but no non-null `agentWait` value (see `Q24/capture-findings-20261116.md`) |
| Q15 | May v2 push corrections into non-worker sessions | ANSWERED (2026-11-16) | Owner: "Option 1 accepted". v2 reports only, reopened only when a channel, a threat model, an approval rule and a shared grant vocabulary exist. Caveat: the "never messaged" sentence (`src/superclaude/core/WORKER-CONTRACT.md:288`) covers person-started sessions, not watcher-started ones |
| Q16 | How far the trust promise goes | ANSWERED | Option 1: shared permission/grant vocabulary and audit format; independent enforcement; no access expansion. See owner-answers.md, 2026-11-15 Q19/Q16 batch |
| Q17 | Should the observer show sweep facts | ACCEPTED | Not now |
| Q18 | Copy the observer snapshot to the TUIBBS machine | ACCEPTED | Not yet. The owner's new API idea is a candidate transport |
| Q19 | Which dashboard improvement first | ANSWERED | Option 2: plain-English summaries and named stages first in coordinator/sweep report; Q17 unchanged; Fleet Quilt/Decision Desk later. See owner-answers.md, 2026-11-15 Q19/Q16 batch |
| Q20 | Who owns the watcher's working folder and sessions | **DEFERRED** | Until the watcher schedule is installed (no schedule, config or labels exist today). A named person is still needed before the first live launch, see section 3 item 3 |
| Q21 | May the sweep label machine-started sessions | ACCEPTED | Phase 2, after the first live test |
| Q22 | How old a status file may be before it counts as stale | **DEFERRED** | Until a reader of `snapshot.json` exists (none in `src/` today). The unposted Coder#477 draft keeps its blank "[N minutes: owner decides]" |
| Q23 | Is a "reclaimable" worker live, historical or its own state | ACCEPTED | Its own state |
| Q24 | Who runs the live Orca checks | ANSWERED and DONE (2026-11-16) | Owner: "a live session on master made for this job" = option 1, then "Q24 go", "q24: second capture" and "Record Q24". The session ran in worktree `/home/coder/workspaces/worktrees/IronClaude/q24-orca-capture`. Findings (names and values only): `owner-questions/Q24/capture-findings-20261116.md`; raw captures stay outside git in `/home/coder/captures/`. Headline: for a running worker `dispatch.status` is `dispatched`, `projection.outcome` is `in_progress`, liveness is `live`, `agentWait` is present and null; the sweep's parked `working` rule expects status `in_progress`, so it could not match as written. Not seen: a non-null `agentWait`. The plan was: two read-only captures only: `orca-ide worktree ps --agent-wait --json` and `orca-ide orchestration worker-show --dispatch <one live id> --json` (both in the sweep allow list, `src/superclaude/cli/sweep/probes.py:52` and `:58-59`), pasted into one file that stays untracked unless you say otherwise. The worker-id comparison and the message-write test are deferred, not erased. Each capture still needs its own permission row |
| Q25 | Who runs `/sc:pr-submit` for program PRs | ANSWERED | Option 3: one agent per change builds and publishes it, no supervised worker. Watch-out: such agents are invisible to Orca's worker list, and the owner declined a recurring timer (Q31). A per-item deadline in the decision ledger is recommended |
| Q26 | Where the coordinator lives, and the layout | ANSWERED | A dedicated worktree through Orca counts as person-opened. Shared branch `coordinators` (CREATED 2026-11-14 15:39 at master `d2d8a2d16`, no README yet), folders `.dev/coordinators/<kind>-<slug>/<github-login>/`, standing narrowed push approval, branch protection dropped, scope folder `epic-orchestrator-tui-alignment`, the `.dev/README.md` entry later. The 11 edits it implies for the plan are listed, not applied |
| Q27 | May SW-02's plan package ship in PR #539 | ACCEPTED | Done in practice: the fix's plan package was archived inside #539 |
| Q28 | What `/sc:pr-submit` may do on PR #539 | MOOT | #539 merged on 2026-11-14 |
| Q29 | How this workspace gets the sweep command | **DEFERRED** | Until the first coordinator is about to open. Both installed copies of `superclaude` predate the sweep merge, so the sweep is not runnable here and nothing needs it yet |
| Q30 | Which coordinator the questions-panel test may read | **DEFERRED** | Until the questions panel is scheduled. The panel is off (`QUESTION_GATE_PASSED = False`, `src/superclaude/cli/observe/commands.py:67`) |
| Q31 | The 10-minute recurring check | ANSWERED | Option 2: no timer; only the checked-in coordinator rule |
| Q32 | May workers make local commits | ACCEPTED | No; the PR session commits |
| Q33 | Who fixes PR #539 | ANSWERED and DONE | A fresh session; the fix merged |
| Q34 | Guard for the plan-writing worker | ANSWERED | G1 for the one test issue; G2 before any other issue |
| Q35 | How the claim changes under route B | ANSWERED | B1b: the watcher claims with `--pipeline none`; the coordinator runs the existing worktree script then starts the worker |
| Q36 | Approval latency | ANSWERED | Approve in the coordinator session; the "check now" command is not selected |
| Q37 | Where the worker's approval rule lives | ANSWERED | In `WORKER-CONTRACT.md`, next to WC-3 |
| Q38 | How a coordinator approval releases a guarded worker | ANSWERED | Default: G2 not built yet |
| Q39 | Remove plain `approved` typed in a session | ANSWERED | Remove it now, everywhere (the owner reversed his own first reading; "remove now" is final) |
| Q40 | Where the design amendments go | ANSWERED | One follow-up documentation PR, opened only after the owner reads the plan |
| Q41 | A worktree with no agent for a moment under B1b | ANSWERED (2026-11-16) | Owner: "yes accepted" = answer A. Matches plan Task 19 (line 226), now also recorded in `owner-answers.md` |

### What is waiting after the evening of 2026-11-16

No question waits for an answer. One thing waits for the owner:

```text
Q8: say whether the draft paragraph is yours, and answer the remaining record fields (or "deferred to release 3" where allowed)
```

Recommendations are not decisions. Q20, Q22, Q29 and Q30 stay deferred by agent triage (see section 3 item 12); their full cards stay in section 2 as history. Their original recommended replies were: Q20 option 1 (with a named owner), Q22 option 1, Q29 option 1, Q30 option 1.

---

## 2. Owner cards (open, shrunk, trimmed and deferred)

**Only Q7, Q24 and Q41 need you today.** The cards for the trimmed and deferred questions are kept below unchanged as history; each carries a "Triage 2026-11-16" line saying what applies now. Those lines are agent recommendations, not owner answers.

Each card was written for a reader who has never seen the project. "Update since the card was written" lines were added on 2026-11-15 where events changed a fact.


The full original cards (with debate details) are in `human-decisions.md`; the debate record for each is in `Q<nn>/final.md`. The cards below are the same questions, shortened, with each card's update line.

### Q7. Save your own decision records before a side checkout is cleaned up

> **ANSWERED 2026-11-16 (owner: "I confirm this was me ... go with the recommendation"); backup done, see `owner-answers.md` "2026-11-16, evening".** The earlier triage (agent recommendation) read: SHRUNK. Do a plain backup only: a local copy of the files below plus a sha256 list kept outside git. No push and no commit, because commit `1ae72e1a1` sets `QUESTION_GATE_PASSED = True` on a record its own message calls "typed by the executor from the owner's words", and `f104ca51a` repoints it to a first-person record headed "Written by the owner" that git cannot attribute. A backup is not approval of that record; you confirm it separately. Those two commits go into no PR until you do. Reply: `Q7: backup only`.

- **Question:** Will you confirm your 2026-11-12 approval record is your own text, and get it and your other decision records out of the side checkout where they are the only copies?
- **Why it matters:** The side checkout `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp` holds your "pass" approval record and your 2026-11-12 decision record (two unpushed commits), plus untracked `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/` and `handoff-mvp-brainstorm.md`. If it is cleaned or the disk fails they are gone. The record says "Written by the owner" but an agent session made the commits, so git cannot prove who typed it. Project rule: agents may quote your records, never write them. The switch-on of the dashboard's questions panel must cite the approval record.
- **Update since the card:** Not re-checked on 2026-11-15 (UNVERIFIED). Re-list the files before acting.
- **Options:**
  1. Freeze today, then save everything now (recommended, 65%). A dated "do not clean" note names every file; you re-read, write one dated line saying they are yours, and commit them unchanged in a small records-only change. An agent copies them only if you say so in writing. Upside: nothing can be lost. Downside: about one sitting; one plan condition ("approval record is committed in the switch-on change") must be reworded.
  2. Do it yourself on the plan's original schedule. The approval record stays a single copy until the switch-on, which may never happen.
  3. Not now; freeze only. Single copies for an open-ended time; the note is not a lock.
- **If you do not answer:** The side checkout must not be cleaned, the switch-on change cannot open, and the records stay single copies.
- **Does not authorize:** switching the panel on, choosing which sessions the panel may read, or any agent writing your records.
- **Reply:** `Q7: option 1, I will commit them myself` (or `option 1, a named session may copy`, `option 2`, `option 3`), and say whether to save `handoff-mvp-brainstorm.md`.

### Q8. Record, in your own words, the dashboard design direction you chose

> **ANSWERED IN PART 2026-11-16: the owner gave the visual direction and asked for a paragraph; a draft is at `owner-questions/Q08/visual-direction-paragraph.md` (not yet confirmed as the owner's). The other record fields are still open.** The earlier triage (agent recommendation) read: DEFERRED until release 3 of the dashboard is scheduled. Your Q19 answer moved the next work to summaries, so a record written today would describe a direction that already changed. Until then the #409 correction says "not met as recorded".

- **Question:** Will you write one short dated paragraph recording the design direction you chose for the dashboard, or rewrite the issue's first acceptance criterion instead?
- **Why it matters:** Issue #409 says "A human selects the visual direction before production integration." The dashboard's rules say only your own dated record meets it. You chose a staged direction on 2026-11-08 (worker list, then question list, then Decision Desk), but an agent relayed it, so it does not count. Without the record the criterion cannot be marked met, the issue text cannot be corrected on this point, and the next release is blocked. The record must cover: date, option, who decided, where your statement lives, defaults before and after questions are shown, post-link choice, fallback date, stack, command name, and what "production integration" means (the command in the shipped tool, or the dashboard switched on in the product; the stricter one applies until you say).
- **Update since the card:** The #409 correction pass (a GitHub post, separate grant) waits on this.
- **Options:**
  1. Write the record now, keep the criterion (recommended, 68%, 3 of 3 advocates). Post-link choice and fallback date may say "deferred to release 3". Upside: meets the rule, settles the meaning of "production integration". Downside: a few minutes; it says it was written after releases 1 and 2 shipped.
  2. Rewrite the acceptance criterion. The dashboard's rules must change too; reads as moving the bar after shipping.
  3. Neither now. The issue says "not met as recorded"; the next release has no date.
- **If you do not answer:** The issue correction posts without a status line on this criterion, and the next release cannot start.
- **Does not authorize:** an agent writing the record, switching on any dashboard part, or starting the next release.
- **Reply:** `Q8: option 1, I will write it at <location>` (or `option 2`, `option 3`).

### Q13. May the observer fall back to a plain `orca` command

> **ANSWERED 2026-11-16 (owner: "Yes" = option 1).** The earlier triage (agent recommendation) read: TRIMMED. The card's own default applies (the contract note records both rules as facts, no verdict). Reason: the observer accepts a program only if `skills list --json` lists `orca-cli` (`src/superclaude/cli/install_user_setup.py:268`), so the screen reader cannot be chosen. One residual to keep in the note: that probe runs the candidate program once (line 259), so a wrong program would be run once.

- **Question:** May the observer dashboard fall back to a program named `orca` on the system path, when the sweep's rule is never to do that?
- **Why it matters:** The planned contract note between the two programs must say whether this difference is accepted. Accepting it is a small written acceptance of risk. On Linux a program named `orca` outside Orca's terminals is usually the GNOME screen reader, not Orca. The observer tries `orca-ide`, then `orca`, and uses one only if `skills list --json` lists `orca-cli`. The sweep uses `ORCA_CLI_COMMAND` if set, else `orca-ide`, never `orca`, and asks no question first. Today the variable is unset and both use `orca-ide`.
- **Update since the card:** PR #539 is merged (2026-11-14). The sweep rule was not re-read after the merge (UNVERIFIED).
- **Options:**
  1. Yes, and write down the limit (recommended, 72%). The note records both rules, says the check proves "this is Orca" but not "the same Orca the sweep reads", records the Orca build next to each capture, and asks you again if builds differ. No code change.
  2. No: a small observer PR makes it use the sweep's rule. Changes working code for a problem never seen.
  3. No ruling: record both rules as facts, ask only if a difference is ever seen.
- **If you do not answer:** The note records both rules without a verdict (same as option 3).
- **Does not authorize:** any code change to the observer, watcher or sweep.
- **Reply:** `Q13: option 1` (or `option 2`, `option 3`).

### Q14. What "#339 is complete" means for when Orchestrator v2 may start

> **ANSWERED 2026-11-16 (owner: "option 1 accepted").** The earlier triage (agent recommendation) read: TRIMMED. Option 1 applies as a labelled default; options 2 and 3 are dropped. Never make a code change a start gate. Issue #423 itself says nothing starts before a brainstorm and research, and it is open and untouched since 2026-11-08.

- **Question:** Issue #423 (Orchestrator v2) says it starts "after #339 is complete". What must be finished first?
- **Why it matters:** The words can be read several ways, so the start gate cannot be checked. Your answer sets the #423 rewrite's sequencing sentence and whether a small sweep code change becomes a prerequisite. The sweep's `working` class is switched off because the exact names Orca uses for "live" and "waiting" were never recorded. A one-time read-only "shared capture" of live Orca values (tracked in issue #534) would record them. Restoring the class afterwards is a separate small code PR.
- **Update since the card:** The first half is met: PR #539 merged on 2026-11-14. The capture is not recorded (it needs Q24 and a reachable Orca).
- **Options:**
  1. #539 merged plus the capture recorded (recommended, 80%). The gate says whether the values are enough to switch the `working` class on; the code fix stays a follow-up; optionally you add a fallback date.
  2. #539 merged, capture recorded and the `working` class restored in code. Slowest; puts code on a planning gate.
  3. #539 merged only. Fastest; likely rework when the capture arrives.
- **If you do not answer:** The plan uses option 1, labelled "default".
- **Does not authorize:** editing #423, running the capture, any sweep code change, or starting v2.
- **Reply:** `Q14: option 1` (optionally `with fallback date YYYY-MM-DD`), `option 2` or `option 3`.

### Q15. May v2 push corrections into sessions that are not Orca workers

> **ANSWERED 2026-11-16 (owner: "Option 1 accepted").** The earlier triage (agent recommendation) read: TRIMMED. The default applies: v2 reports only. Caveat to keep: `src/superclaude/core/WORKER-CONTRACT.md:288` says person-started sessions "are never messaged"; it does not mention sessions the issue watcher starts, which is the card's open case.

- **Question:** Must the planned v2 knowledge layer ever send a correction directly into a session that is not an Orca worker, or only report to you or the coordinator?
- **Why it matters:** #423 says v2 should "relay them to affected agents". That would push content into sessions the current rules say are never messaged (ones you start, ones the issue watcher starts, ones with no Orca run). Today the coordinator corrects a worker only by leaving a message the worker picks up itself (rule WC-12). No known channel delivers into a non-worker session, and signing messages does not stop harmful text inside them. It is a trust-boundary call and decides whether the unbuilt trust layer becomes a v2 prerequisite.
- **Update since the card:** None. The gap remains: watcher-launched unattended sessions are never corrected automatically.
- **Options:**
  1. Report only, with a condition for ever reopening (recommended, 82%). Reopen only when a channel, a threat model for harmful content, a rule on whether you approve each correction, and a shared grant vocabulary exist.
  2. Never, as a standing rule for every program. Binds future designs nobody has researched.
  3. Yes eventually, behind the trust layer. Moves unbuilt trust work onto v2's path; no channel is known.
- **If you do not answer:** Report only, without the reopening condition.
- **Does not authorize:** edits to #423 or the worker contract, a new message channel, or v2 work.
- **Reply:** `Q15: option 1` (or `option 2`, `option 3`).

### Q16. How far the trust promise goes across the three planned programs

**ANSWERED 2026-11-15: option 1.** Shared permission/grant vocabulary and audit format, independently enforced by each component; no access expansion. Terms and format still need one owner and later reconfirmation. See [dated owner record](owner-answers.md#2026-11-15-q19-and-q16-owner-decisions-recorded-through-dot). The original card below is retained as history, not an open question or a grant.

- **Question:** Promise one shared trust design for the observer, Orchestrator v2 and the Coder workspace listener, or only one shared set of permission names plus one shared audit log format, each program checking permissions its own way?
- **Why it matters:** #409 decision 6 now says "Decide one design, not two." #423 and Coder#477 (in the separate `IronbellyOrg/Coder` repository) wait on this sentence, and so do the future trust layer, the v2 design and the observer's planned answer screen. Nothing is built; this is a promise in issue text. "Trust" means who may do what and how that is checked and logged. The three programs face different risks: the observer only reads on one machine; the first v2 release reads only what the same user can read; the listener would cross between Coder workspaces.
- **Update since the card:** None.
- **Options:**
  1. One shared vocabulary and one shared audit record (recommended, 70%). #409 decision 6 becomes "Decide one grant vocabulary and one audit record."; #423 and Coder#477 promise the shared terms, not a shared design. The terms are written later with one owner, and you re-confirm then.
  2. Promise nothing yet (the default). #409 keeps "one design", the others say nothing, so the issues disagree.
  3. One trust design for all three. The spec lists this as out of scope; it either over-builds the observer or under-protects the listener.
- **If you do not answer:** The default (option 2) applies and the trust-dependent work stays on hold.
- **Does not authorize:** relay of knowledge between agents, any issue edit, or any code.
- **Reply:** `Q16: option 1` (or `option 2`, `option 3`).

### Q19. Which dashboard improvement first

**ANSWERED 2026-11-15: option 2.** Plain-English task/done/remaining/needs-me summaries, issue/PR links and named stages first in the coordinator/sweep report. Fleet Quilt and Decision Desk later; Q17 remains unchanged (no sweep facts on observer now). See [dated owner record](owner-answers.md#2026-11-15-q19-and-q16-owner-decisions-recorded-through-dot). The original card below is retained as history, not an open question or a grant.

- **Question:** Of the four improvements a reviewer asked for on the worker dashboard, which comes first, and does the dashboard itself or the coordinator's report carry it?
- **Why it matters:** The dashboard's third release (the "Decision Desk" screen) cannot start until the first improvement and its home are named. The reviewer's 2026-11-11 comment on #409 asked for four things named after design pictures: Fleet Quilt, Decision Desk, Loop Detector or Mission Pulse (named steps with green, yellow, red), and a plain-English summary with issue and PR links. Decision Desk needs a coordinator-question-to-worker link that is not established. Fleet Quilt's data needs are not written down. The summary and named steps have a known data source today (each task's brief and the progress files workers write). Nobody confirmed the reviewer's priority order.
- **Update since the card:** The sweep (where the summary would live) is now merged.
- **Options:**
  1. Fleet Quilt first on the dashboard; the summary second (recommended, only 55%). Re-read the reviewer's comment first; if it says the summary matters most, pick option 2. Pick Decision Desk instead if you prefer it (it then waits for its link).
  2. The summary and named steps first, in the coordinator's report. Buildable soonest but in a report the reviewer never sees, unless you allow sweep facts on the dashboard (Q17).
  3. Do not pick yet. Same as not answering.
- **If you do not answer:** Release 3 does not start; none of the four moves.
- **Does not authorize:** any code, any change to the sweep's allowed commands, showing sweep facts on the dashboard, or any reply on #409.
- **Reply:** `Q19: option 1, Fleet Quilt` (or `option 1, Decision Desk`, `option 2`, `option 3`).

### Q20. Who owns the watcher's working folder and sessions

> **Triage 2026-11-16 (agent recommendation, not an owner answer): DEFERRED** until the watcher schedule is installed. Today there is no schedule, no config and no `issue-watch` label on the fork, so no sessions spawn. A named person is still needed before the first live launch (section 3 item 3).

- **Question:** Who owns the agent in the issue watcher's working folder, and may that folder collect up to 6 new Claude sessions a day that no coordinator session looks after?
- **Why it matters:** The watcher's first live test, the setup step that creates its folder, and one planned edit to #450 (the watcher rollout issue) wait on this. The watcher is a background process: when an issue is approved it starts a Claude session that claims the issue. Orca's rule: whoever creates a worktree with an agent owns that agent. It starts at most 6 sessions per 24 hours (a value fixed in code, for you to confirm after a trial run). Nothing closes them; the setup guide says to close them yourself in Orca. They read issue text anyone who can comment can write, and on this host they run with permission checks off (Q2).
- **Update since the card:** Under route B the plan-writing agent is started by the coordinator as a supervised worker (so the coordinator owns it); this question now covers only the watcher's own folder and its claim sessions. The first live test (FU-1) still needs a named person.
- **Options:**
  1. A person you name owns it; sessions stay person-reviewed (recommended, 70%). The one-session live test runs now. Before the schedule is switched on you write down who closes sessions and when, how often they check, and who covers when they are away.
  2. Decide nothing yet. No folder, no live test, no schedule.
  3. The coordinator owns it and reviews the sessions. The coordinator stops when its work ends, cannot really see these sessions and would be exposed to outsider-written text.
- **If you do not answer:** Same as option 2: no setup step, no #450 edit, no live test.
- **Does not authorize:** the live test itself (that also needs your written acceptance, see section 3 item 3), switching on the schedule, or any coordinator adopting watcher sessions.
- **Reply:** `Q20: option 1, owner is <name>` (or `option 2`, `option 3`).

### Q22. How old a status file may be before readers call it stale

> **Triage 2026-11-16 (agent recommendation, not an owner answer): DEFERRED** until a reader of `snapshot.json` exists. None exists in `src/`, and the file was last written 2026-11-11. The file already carries `generatedAt`.

- **Question:** When a program reads a status file written by another program, at what age should it say "this file is stale"?
- **Why it matters:** The contract note between the observer and the sweep, and the narrowed Coder#477 text, which has a blank "[N minutes: owner decides]", wait on this. The observer checks every 15 seconds and rewrites `snapshot.json` each time, even after a failed check; after errors it waits up to 60 seconds. On its own screen it calls data stale after 45 seconds. The file has a timestamp `generatedAt` and says inside whether its data was fresh. The Coder workspace record and the copy channel to TUIBBS (the owner's other platform) are not built; nobody reads these files yet.
- **Update since the card:** None. The Coder#477 post is still waiting on a grant, and needs this number or formula.
- **Options:**
  1. A rule: stale after three intervals or the longest normal gap, whichever is larger (recommended, 70%). For the observer's file that is about 75 seconds (inferred from code, not measured). Readers print the age and keep "stale file" separate from "stale data".
  2. One fixed number now (suggested 2 minutes, or your own). A guess for a producer that does not exist.
  3. No number yet. The stopgap (about 15 seconds) would flip a normal observer file between fresh and stale.
- **If you do not answer:** The stopgap applies and the Coder issue keeps its blank.
- **Does not authorize:** posting to Coder#477, building a reader, or adding a field to the snapshot file.
- **Reply:** `Q22: option 1` (or `option 2, N minutes`, `option 3`).

### Q24. Who runs the live Orca checks

> **ANSWERED 2026-11-16 (owner: "a live session on master made for this job" = option 1); the captures were run on 2026-11-16 and the findings are in `Q24/capture-findings-20261116.md`.** The earlier triage (agent recommendation) read: SHRUNK to two read-only captures, pasted into one file that stays untracked unless you say otherwise: `orca-ide worktree ps --agent-wait --json` and `orca-ide orchestration worker-show --dispatch <one live id> --json`. The observer snapshot already holds two of the three unknown Orca names; only `agentWait` is missing. The worker-id comparison and the message-write test are deferred, not erased: they answer different questions. Each capture still needs its own permission row. Reply: `Q24: two captures only`.

- **Question:** Which session or person runs three live checks against Orca: a read-only capture of a few unknown fields, a one-time comparison of worker ids between the dashboard and the sweep report, and a test that writes throwaway messages?
- **Why it matters:** Without a named runner none runs. That blocks the Orchestrator v2 gate (#423) and the dashboard's PR that turns on its questions panel. The review suggested "the 409 session". The debate found two problems: that session's worktree is on an unmerged branch holding unpushed work and nobody checked it is alive, and the comparison must run the sweep on merged master code (now possible, but see Q29).
- **Update since the card:** #539 merged on 2026-11-14, so the comparison is possible in principle, but the sweep is not runnable on this workspace until Q29 is done.
- **Options:**
  1. A fresh session on master made for this job (recommended, about 65%). The coordinator creates a new Orca worktree with its own agent; it runs the capture, then the comparison once the sweep is runnable. You run the message-writing test yourself unless you name someone else.
  2. The 409 session. If it has ended, nothing runs; its unsaved work is at risk.
  3. You run them by hand, from agent-written procedures. Three sittings.
- **If you do not answer:** None of the three runs, the v2 gate cannot pass, the panel stays off.
- **Does not authorize:** any permission row (each check needs its own), `run-use`, a merge, or a message to a live coordinator.
- **Reply:** `Q24: option 1` (optionally `and I run the message test`, or name a runner).

### Q29. How this workspace gets the sweep command

> **Triage 2026-11-16 (agent recommendation, not an owner answer): DEFERRED** until the first coordinator is about to open. No coordinator exists to run the sweep, no sweep report was ever produced, and both installed copies of `superclaude` answer "No such command 'sweep'".

- **Question:** Should this workspace's `superclaude` command get the sweep through the Coder template, or through a one-time reinstall you approve?
- **Why it matters:** The coordinator is meant to run `/sc:sweep`, and the observer-versus-sweep comparison needs it. Your rule: updates reach workspaces only through the Coder template (`IronbellyOrg/Coder` pins an IronClaude commit; a daily workflow opens a bump PR; after you merge it the image is rebuilt and each workspace updated, which ends running sessions). This workspace has two copies of the command (checked 2026-11-14): the image copy in `/usr/local/bin` and a hand-installed copy in `/home/coder/.local/bin` (2026-11-12 22:12, installer unknown) that comes first. `/home/coder` survives updates, so a template update alone would not change which copy runs.
- **Update since the card:** #539 is merged, so the next step is available now. The sweep is still not runnable here.
- **Options:**
  1. Coder template, then remove the extra copy (recommended, 70%). Start the pin-bump workflow by hand, merge its PR, update the workspace between sessions, then approve removing the copy in `/home/coder/.local/bin`. Slower; the update ends running sessions.
  2. A one-time reinstall at the exact merge commit into `/home/coder/.local/bin`. Fast, but an exception to your update rule.
  3. Decide later. The sweep stays "not runnable" and the question returns unchanged.
- **If you do not answer:** Option 3 applies.
- **Does not authorize:** running the sweep more often than once per 5 minutes, any sweep write beyond its one report, or changes to other workspaces.
- **Reply:** `Q29: option 1, and yes, remove the extra copy after the update` (or `option 2`, `option 3`).

### Q30. Which coordinator the questions-panel test may read

> **Triage 2026-11-16 (agent recommendation, not an owner answer): DEFERRED** until the questions panel is scheduled. The panel is off, and after your Q19 answer and the Q17 answer it has no audience now. No PR switches it on while this is deferred.

- **Question:** For the one live test of the observer's questions panel, which coordinator's work may it read, and do you accept in writing that questions there might be lost?
- **Why it matters:** The panel shows questions workers send to their coordinator. It is switched off. Switching it on needs one live test in a real coordinator's terminal (only the terminal that holds a Run can read its questions). Orca's help says the panel's read "does not mark read", but nobody tested it on a live coordinator (open, estimated 61%), so the test could make a question vanish. The program's own coordinator must never be the test subject.
- **Update since the card:** None.
- **Options:**
  1. A throwaway coordinator you open just for the test (recommended, 85%). After the planted-message test passes, you open a test coordinator and start one test worker that asks one known question; the panel reads it while unanswered; loss is judged by whether that question still reaches the coordinator. Then everything is closed. Needs Orca up.
  2. A real coordinator from your other work, at a quiet moment. A real question could be lost, and a quiet moment shows little.
  3. No live test for now. The panel never ships while this holds.
- **If you do not answer:** Option 3 applies; the PR that switches the panel on is not opened.
- **Does not authorize:** `run-use` on any other Run, reading any Run other than the one you name, reading the program's own coordinator, or switching the panel on.
- **Reply:** `Q30: option 1, and yes, I accept that questions in the test Run may be consumed` (or `option 2` with the Run id, or `option 3`).

### Q41. A worktree with no agent for a short moment under the chosen handoff

> **ANSWERED 2026-11-16 (owner: "yes accepted" = A).** The earlier triage (agent recommendation) read: one line, no card. Plan Task 19 already records "answered 2026-11-14: A". Reply `Q41: confirm A` and an agent adds the row you wrote; an agent does not write it for you.

- **Question:** Under the chosen design (B1b), the coordinator runs the worktree script, and only then starts the worker. For a short moment the new worktree has no agent, which the "every worktree gets an agent" rule normally forbids. Accept that and say so in the plan?
- **Where it stands:** The route B plan records "answered A: accept it and say so", but the answer is not in `owner-answers.md`. Confirm or correct.
- **Reply:** `Q41: confirm A` (or say what you want instead).

---

## 3. Other open items (not numbered questions)

These need an owner action or a grant. None is a grant by being listed here.

1. **The route B plan is not yet in this repository.** It is a plan package in a local worktree named `claim-handoff-b` (branch `ironbelly/claim-handoff-b`, nothing pushed, no PR). On 2026-11-15 an independent review of it found 8 changes to make, and they are being applied: split it into two plan files (Plan A runs now with Task 16 first; Plan B waits on an owner-run item "first live test run and recorded"), build only three feature chain rows, record real GitHub fixtures before writing the predicates, restrict the guard's `orchestration send` to the coordinator, and fix a few acceptance checks. Next owner steps: read the revised plan, then say whether to start Plan A. One input is needed from the owner: **a GitHub issue the owner wrote**, used to record real read-only fixtures.
2. **Task 16 (remove plain `approved`)** changes a security hook (`launch-level-guard.sh` and its plugin copy) and a skill template. The owner decided "remove now". It still needs a build, an independent review and its own go. Until it is merged, typing `approved` still releases a governed worktree-level session on this host.
3. **The watcher's first live test (FU-1)** needs all of: the claim command's own hook check (recorded as not yet run), a separate live-test grant, a reachable Orca, a named owner of the watcher worktree (Q20), a running coordinator, a test issue whose text the owner wrote, and the owner's written acceptance at test time: "I accept, for test issue #<N> only, that the plan-writing worker runs with permission checks off and with no launch-level guard (nothing blocks a commit, push, merge, GitHub write or /sc:implement), reading issue text that I wrote myself." The worker can also post the approval label or an `approved` comment as the same GitHub login, and nothing tells those apart.
4. **Posts to GitHub waiting for grants**, each a separate grant, in the agreed order: edits to #450 (the watcher rollout issue), the narrowed reply on Coder#477 (needs Q22; carries the Q4 line), the correction pass on #409 (needs Q8; the trust sentence is settled by Q16 option 1, answered 2026-11-15), one comment on #339, then the rewrite of #423 (needs Q14 and Q15; Q16 is answered). The correction texts are in the adjudicated document, part 6. Re-read each issue's `updatedAt` immediately before each write.
5. **Coordinator layout follow-ups (Q26).** The shared branch `coordinators` exists and is empty of coordinator files. Not done: its `README.md` (the owner's standing push approval does not cover this project-wide file), the 11 edits to the plan listed in `owner-questions/Q26-coordinator-layout/final.md`, the first coordinator, and the `.dev/README.md` row (later, with the first coordinator-tooling PR).
6. **The workspace update for the sweep (Q29).** After the Coder template update, a second copy of `superclaude` in `/home/coder/.local/bin` (installed by hand on 2026-11-12) would still shadow the image copy. Removing it needs the owner's approval. Until then `/sc:sweep` is "not runnable" here and the observer-versus-sweep id comparison waits.
7. **The coordinator's decision ledger has no home yet** until the first coordinator runs (Q26). Until then answers live in `owner-answers.md`.
8. **A stale line in `CLAUDE.md`.** Line 43 calls the fork "the user's private fork", but the repository is public. The owner accepted public for now ("I can always set it to private later"). Decide whether to correct the sentence.
9. **Two records the plan cites are not in `owner-answers.md`:** Q41 (above) and the owner's 2026-11-14 acceptance of Decision 1 for the second session. Confirm both.
10. **A merged-plan refresh.** `merged-requirements.md` still shows the original recommended answers and defaults in its section 3. The change lists that bring it up to date are in the route B plan (its last task) and in the Q26 final. The owner has not decided when to apply them.
11. **Answers from a separate coordinator index, recorded 2026-11-16** (details in `owner-answers.md`, section "2026-11-16"). They close none of Q1 to Q41. Two were pasted: the active workflow is `/sc:workflow` plus `/sc:implement`, `sprint run` in its current form is obsolete, and `/sc:task` and the task-builder commands are to be retired (a decision, not done); only Sprint run and its CLI tool suite get an evaluation against retirement. Still open from that decision: the evaluation itself, the retirement steps and date, and the routing guide `HOW-WE-WORK.md`, whose level 4 still names `/task-builder` and `/task`, so it will need a change when retirement is done. The packet's other answers (D-12, D-13, D-15, issues #553 and #562) live in three packet files that were not supplied here and are not recorded.

12. **Agent triage of the open questions, 2026-11-16.** Three reviewers and a three-way debate (`adversarial/` and `final-cut-list.md` in `ponytail-cuts-adversarial/`, with the review summary in `ponytail-triage-20261116.md`, both in this folder) produced the status changes above. They are recommendations, not owner answers, and nothing in them is a grant. What else came out of it:
    - **Hold.** Commits `1ae72e1a1` and `f104ca51a` in `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp` go into no pull request or merge without their own grant. The provenance condition (the owner confirming the 2026-11-12 pass record) was met on 2026-11-16 (see Q7); the owner said they do not care what happens to the commits, so nothing is planned for them. A backup of them is at `/home/coder/backups/issue-409-mvp-20261116/`.
    - **Kept as decided, cut not taken.** The approval flow stays as you approved it (label with Status move; exact comment "ideally"); Task 16 (remove plain `approved`) stays as planned; the owner-written-record rule and the `QUESTION_GATE_PASSED` constant stay; `slo_numbers` stays because `docs/designs/issue-watcher-setup.md:470` still calls it; the questions-panel code, the snapshot export and the three Orca finders stay. If you want less to build, the comment-approval input is the one piece an advocate would drop; it was not raised as a question.
    - **Needs a pull request, not started.** One line in the sweep report saying the `working` class is off (the class is a stub that returns nothing, `src/superclaude/cli/sweep/classify.py:251-257`), so `working: 0` is not read as "nothing is running".
    - **Recommendation to the route B plan, not applied.** Run one throwaway delivery test (`worker-start`, `ask`, `reply`) before the GitHub-reading tasks, and keep Task 16 first and unblocked.
    - **Effect on the posts in item 4.** The #409 correction says "not met as recorded" (Q8 deferred). The Coder#477 reply keeps its blank "[N minutes: owner decides]" (Q22 deferred). The #423 rewrite uses the labelled defaults for Q14 and Q15.
    - **Open facts.** The questions-panel deletion size (about 2,500 lines) and the savings claimed for shrinking the approval flow (about 4,000 lines, 13 files) were not verified.

## 4. How to keep this file current

Whoever records an answer should (1) add a dated row to `owner-answers.md`, (2) change the state of that question in section 1 above, and (3) delete its card from section 2 or mark it answered. Do not edit a card's recommendation to match an answer. The debate record lives in `Q<nn>/final.md`.
