# Decisions only you can make (21 questions)

You do not need to have followed this project to use this file. Each card is self-contained. Read the glossary once, then answer the cards in the order given. You can answer a few at a time; nothing needs all 21 at once. For each card the reply format is one line, for example `Q2: option 1, yes`. "Reply with the default" is always allowed: the card says what happens if you say nothing.

## Glossary (the ten terms the cards use)

- **Orca**: the local app that runs Claude sessions in separate git worktrees and records who is working on what.
- **The sweep** (`superclaude sweep`, PR #539): a command that reads Orca, git and session records and writes one status report about the workers a coordinator started. PR #539 is still open.
- **The observer** (`superclaude observe`): a terminal dashboard of Orca workers. It is already built and merged. Its "coordinator questions" panel is switched off.
- **The watcher** (`superclaude issue-watch`, issue #450): a poller that starts a session to claim an approved GitHub issue. FU-1 is its first live test.
- **Coder#477**: an issue in the separate Coder repository proposing a listener inside each workspace.
- **#423, "v2"**: a proposed later "knowledge layer" that would share what agents learn.
- **The coordinator**: the Claude session you will start with the launch prompt. It runs the plan across worktrees and asks you these questions one at a time.
- **W0 to W5 and "gates"**: the plan's steps. A question "gates" a work item when that item cannot start until it is answered.
- **A grant**: your separate approval for one outward action (a push, a merge, a post, a live test). Answering a question here never counts as a grant.
- **INV-008**: the security finding that the sweep's `git status` can run programs named in git config.

## Order

Decide first (they block the first wave): Q1, Q33, Q26, Q2, Q3, Q4, Q25, Q31.
Then (needed in the second wave): Q7, Q8, Q20, Q28, Q30, Q24, Q16, Q13, Q22.
Later (their gates are further out): Q14, Q15, Q19, Q29.

Quick confirmations that take a few seconds: Q4, Q13, Q22, Q31.

---

## Q1 (Security or trust = high; Reversibility= easy; Who is affected= only this program; Needs the owner's = partly; Cost if the answer= medium; Does it grant auth= yes; Debate= converged)

> **Part (a) is already answered (2026-11-13): "fix".** This card asks only how, and how widely. New since the first draft: two facts found on this host on 2026-11-14 change the wording of any fix. (1) The system git config here sets up a git-lfs filter for every repository, so a rule of the form "refuse any worktree that has a filter configured" would refuse all of them. The rule must count a program only where it could actually run for that worktree. (2) This session's environment carries two harmless `GIT_CONFIG_*` credential settings, so the environment route is routinely non-empty. I verified both read-only.

### How to fix the git-config hole in the sweep, and which routes the fix must cover

**Already answered: you chose to fix this hole (not accept it). This card asks only how, and how widely.**

#### Question in one sentence
Should the fix stop the sweep from running config-named programs by refusing to scan affected worktrees, by disabling those programs, or by a mix, and which routes must it cover?

#### Why you are being asked
PR #539 (the `superclaude sweep` report command) cannot merge until your ruling is posted on its security thread. The project's rules require your ruling to name the fix shape and to authorise the change to the owner-signed list of allowed git commands.

#### Background you need
- The sweep runs `git status` in every worktree Orca (the local agent-orchestration app) lists. On 2026-11-13 git started a program named in configuration through six routes: the fsmonitor hook, clean filters, process filters, included config files, per-worktree config, and `GIT_CONFIG_*` and other environment settings.
- Found on 2026-11-14: this host's system git config sets up a git-lfs filter for every repository, and this session's environment carries two harmless `GIT_CONFIG_*` credential settings. A filter only runs for files a repository marks for it.
- So a rule like "refuse any worktree that has a filter configured" would refuse every worktree here.

#### Your options
1. **Refuse and report, counting only programs that could actually run.** A worktree where a route names a program that could run for it is not scanned and shows as "unscanned" with the reason; anything unclear is refused too.
   - If you pick this: you post the ruling; the PR author adds a test that fails if any program runs or if a worktree that should be refused is scanned.
   - Upside: the sweep never shows a wrong git state as if it were right; one behaviour to review.
   - Downside: worktrees that use only the fsmonitor speed-up lose their git facts for no security gain.
2. **Disable by default, refuse only where disabling could change the result.**
   - If you pick this: two behaviours are built and tested.
   - Upside: keeps more git facts.
   - Downside: its key judgement ("could this change the result") is harder and unmeasured; more to review in a very large PR.
3. **Let the PR author pick at implementation time.**
   - If you pick this: you rule only the outcome; the author chooses and explains in the PR.
   - Upside: the choice is made next to the code.
   - Downside: the project's rules require your ruling to name the shape; the author is not yet named.

#### What the debate found
- All three advocates, including those for options 2 and 3, recommended option 1 with amendments.
- The original draft claimed refusing also covers routes nobody listed; that was wrong and is removed.
- Every option must keep the git-status fix separate from the sweep's other reads that share the same list of paths.

#### Recommendation and confidence
Option 1, 60 percent, with all six routes in scope as a minimum and any route you leave out named. This partly matches the spec, which recommended "neutralise or refuse" without choosing.

#### If you do not answer
PR #539 stays open, and everything that waits on its merge stays held.

#### What this answer does not authorize
Any git allow-list change beyond this fix; a merge of PR #539; the PR tool fixing this on its own; any code design (that stays with the PR author).

#### How to answer
Type, for example: "Q1: option 1, all six routes" (or "Q1: option 2, all six routes" / "Q1: option 3").

---

## Q33 (Security or trust = low; Reversibility= easy; Who is affected= only this program; Needs the owner's = yes; Cost if the answer= medium; Does it grant auth= no; Debate= split)

### Who should apply the fixes to pull request #539 and push them? (Q33)

**Question in one sentence:** Which session should make the remaining changes to pull request #539 and push them?

**Why you are being asked:** PR #539 (the new read-only `superclaude sweep` status command) cannot merge until three things are done:
- your ruling on its security finding is applied in the code or text,
- one review thread is fixed,
- its checks are refreshed and green.

Most later work waits on that merge. The plan needs a named session to do it. No file or Orca record says which session owns the PR's working copy, so only you can name it. Until you do, those pushes are held.

**Background you need:**
- The PR's working copy is the folder `.../worktrees/IronClaude/issue-339-orchestrator-mode`. Orca (the app that runs agent sessions) shows that a Claude agent was created there, but not which session it is.
- The last four commits there (12 to 13 November) are review fixes made from that folder.
- Naming the author gives it no permission by itself. Each push and each thread resolve still needs your separate yes, recorded in the decision record.
- The plan keeps program work out of this folder, because stray files could be committed into the PR. Right now the session running this program is working in this folder (unverified whether it is the PR's own session).

**Your options:**

1. **The session that already owns that folder.** It gets a short written list of the PR's rules, you read each change before approving its push, and any program work it does there moves elsewhere first.
   - If you pick this: you name the session; it applies the fixes after your ruling and pushes only with your approval each time.
   - Upside: fastest, keeps the session that knows the PR's history, and adds no new agent.
   - Downside: you must identify it, and it must stop doing program work in that folder first.
2. **A fresh session that does only this job.**
   - If you pick this: the current session moves its other work elsewhere, and a new session is started in that folder with a written brief covering only these three tasks.
   - Upside: cleanest separation and least chance of committing stray files.
   - Downside: unverified whether Orca allows starting a second session in the same folder. It also loses the PR's history and adds a setup step.
3. **You do the commits and pushes yourself.**
   - If you pick this: an agent prepares and tests each change and stops. You review, commit the named files and push.
   - Upside: you see every line of the security-related change before it goes out.
   - Downside: every push waits on your time, and the plan's role text must change. The PR tool also stays off this PR.

**What the debate found:**
- Two of three debaters chose option 1, and one chose option 2.
- They split three ways on who should hold push permission.
- All three said option 1 is right only if program work leaves that folder first.
- Option 2 is the fallback if you cannot identify the session.

**Recommendation:** Option 1 with its conditions, about 55 percent confidence. This matches the plan's recommended answer, plus those conditions.

**If you do not answer:** No pushes to PR #539 for these fixes, so the PR cannot merge and the work behind it waits.

**What this answer does not authorize:** any push, thread resolve or merge (each needs its own approval), use of the PR tool on #539, or any tool designing the security fix.

**How to answer:** type `Q33: option 1, the session is <its name or terminal>` (or `option 2`, or `option 3`).

---

## Q26 (Security or trust = low; Reversibility= easy; Who is affected= only this program; Needs the owner's = yes; Cost if the answer= medium; Does it grant auth= yes; Debate= split)

### Where should the program's coordinator session live?

#### Question in one sentence
In which folder should the coordinator session run, and on which branch should its always-staged decision ledger sit?

#### Why you are being asked
Nothing that hands work to a worker can start until the coordinator exists, and the coordinator cannot start until you name its home. That blocks 15 planned changes (sweep follow-ups, the observer switch, watcher changes, the observer-sweep contract note, Orchestrator v2 work). Ruling on the git safety question for PR #539 does not wait for this.

#### Background you need
- The coordinator is a Claude session that keeps the decision ledger, creates worktrees with agents through Orca (the local agent-orchestration app) and starts workers. The project's rules say it must be a session "the person opened", and it must never run in the PR #539 folder.
- The ledger is a folder under `.dev/tasks/`. Project rule: that folder is always staged (added to git's index), never committed unless you ask.
- Staged files belong to a folder's index, not to a branch: if that folder later switches branch, the staged ledger goes with it.
- Your main folder `/home/coder/workspaces/IronClaude` is on the docs branch `docs/409-orca-dashboard-designs`: pushed, no open PR, no unsaved tracked changes, 21 untracked items. It is 60 commits behind master.
- Checked 2026-11-14: switching that folder to a branch made from master aborts today, because 34 untracked files there have the same paths as files on master (identical copies). Git refuses until they are moved or removed. The abort is safe.
- Orca did not answer on 2026-11-13; it must answer before any worker can start.

#### Your options

### 1. A dedicated program worktree you create through Orca (recommended)
- If you pick this: you run `orca worktree create --name <name> --base-branch origin/master --agent claude --prompt "<coordinator brief>"`; that agent is the coordinator and the ledger is staged there. You also confirm that a session you launch this way and then watch counts as "person-opened".
- Upside: the ledger never moves to another branch; your main folder is untouched; nothing else shares the coordinator's folder.
- Downside: no file confirms the "person-opened" reading, so it rests on your statement; it needs Orca to be up; one more worktree on the host.

### 2. Your main folder, switched to a new program branch
- If you pick this: you move or remove the 34 blocking untracked copies, switch the main folder to a new branch from master, and open the coordinator session there yourself.
- Upside: certainly "person-opened"; it is the spec's own recommendation and matches the project's "open the main checkout" guidance; the ledger can start before Orca is back.
- Downside: while the ledger is staged, the main folder must not switch branch, take any other commit, or host your other Claude sessions; otherwise the ledger can end up on the wrong branch.

### 3. No coordinator yet
- If you pick this: you keep the ledger in your own notes; nothing is written to any branch; you are asked again when the first worker task is next.
- Upside: no move made before Orca and the "person-opened" reading are settled.
- Downside: all 15 worker tasks wait; agents cannot read your approvals from disk, so you restate them in every session.

#### What the debate found
- Three advocates agreed on every point, but the points split between options 1 and 2, and the scores tied (option 1 won the tiebreak).
- Option 1 won on keeping the ledger in place and the coordinator alone in its folder; option 2 won on being certainly "person-opened".
- The debate found that option 2's branch switch currently aborts until the 34 identical copies are cleared.

#### Recommendation and confidence
Option 1, with your statement that it counts as person-opened; option 2 with its three rules if you will not make that statement. Confidence 60 percent.

#### If you do not answer
Option 3 applies: no coordinator starts, you keep the ledger by hand, and your ruling on the PR #539 git question goes only on its PR thread.

#### What this answer does not authorize
No merge, push, PR, issue post or commit. It does not let any session create a worktree for itself, and it does not let the coordinator switch a folder's branch on its own.

#### How to answer
"Q26: option 1, and yes, a session I launch through Orca and watch counts as person-opened" (or "Q26: option 2", or "Q26: option 3").

---

## Q2 (Security or trust = high; Reversibility= easy; Who is affected= only this program; Needs the owner's = partly; Cost if the answer= medium; Does it grant auth= yes; Debate= converged)

### How far the issue watcher's automatic claim goes, and whether its first test may run without permission checks

#### Question in one sentence
Should the issue watcher's automatic claim stop after assigning and commenting (`--pipeline none`) or also open a worktree with a second agent (the default), and do you accept in writing that its first live test session runs with permission checks off?

#### Why you are being asked
The watcher is built but has never run live. Its first live test (called FU-1), the small code change that sets the claim level, and edits to the rollout issue #450 all wait for this answer. Accepting a security risk in writing is yours alone.

#### Background you need
- The watcher polls for approved issues and starts a Claude session that runs `/sc:issue --claim <N>`. It passes nothing else, so today the claim runs at its default level.
- Default level: assign the issue, post two comments, write summary files, then create a worktree and start a second agent that stops at a plan for a person. `--pipeline none` stops after the comments.
- Your own watcher design says the claim stops at the summary file ("claim-only"). The default contradicts it; reviewers judged that an accident.
- On this host every launched Claude session runs with permission checks off. The session reads the issue's text, which anyone who can edit the issue controls.
- The claim command's own gate says no claim at any level runs on a real issue until a hook check called "OB-H1 item 5" passes; it is recorded as not yet run.

#### Your options
1. **Claim-only, and accept permission checks off for the one test issue.**
   - If you pick this: a small watcher change adds `--pipeline none`; the test waits until the hook check passes, you record a separate live-test permission, Orca is reachable and the watcher worktree has a named owner; then one test runs and is recorded.
   - Upside: matches your design; one session per approval, no extra worktrees; the test settles facts nothing else can.
   - Downside: that one session still reads untrusted text with checks off. Your acceptance covers whatever it does on that issue, not only the intended writes. One possible write (a ClickUp script) may not be reversible.
2. **Claim-only, but do not accept permission checks off yet.**
   - If you pick this: the same small change; the live test waits until a session can run with checks on, or until you accept later.
   - Upside: no session runs with checks off on your say-so.
   - Downside: nothing downstream starts; a session with checks on may stall with nobody to approve prompts.
3. **Keep the default (claim, worktree and second agent).**
   - If you pick this: no code change; your design document is amended; the test waits for all of the claim command's hook checks; your acceptance covers two sessions.
   - Upside: each approval yields a ready plan.
   - Downside: two sessions with checks off per approval, unowned worktrees and agents (up to 6 sessions a day), and it reverses your own recorded decision.

#### What the debate found
- All three advocates, including those for options 2 and 3, recommended option 1 when asked to be neutral.
- The default level was judged an accident against your own "claim-only" decision.
- Every option also needs a separate live-test permission row, a reachable Orca and an owner for the watcher worktree; none of the drafts said so.
- The hook check "OB-H1 item 5" binds even the claim-only level and is recorded as not yet run.

#### Recommendation and confidence
Option 1, 72 percent, with the acceptance worded to cover whatever the one session does on the test issue. Writing the test issue's text yourself lowers the risk. This matches the spec's recommended answer, plus the preconditions above.

#### If you do not answer
The small watcher change and the live test do not start, and the first edit to #450 is left out of the edit set and recorded as skipped.

#### What this answer does not authorize
Any later, non-test issue running with checks off; the live test itself without its separate live-test permission row; any merge; any handoff from the watcher to an orchestrator (not built).

#### How to answer
Type, for example: "Q2: option 1, accepted for the test issue only" (or "Q2: option 2" / "Q2: option 3, accepted for both sessions on the test issue").

---

## Q3 (Security or trust = low; Reversibility= easy; Who is affected= other people or repos; Needs the owner's = yes; Cost if the answer= low; Does it grant auth= no; Debate= converged)

### What to do with the Coder workspace-listener issue (Coder#477)

#### Question in one sentence
Should the Coder issue #477 ("Workspace listener, monitor registration and secure prompt routing for every Coder workspace") be kept as written, narrowed to read-only workspace status, or closed?

#### Why you are being asked
The issue sits in a different repository (IronbellyOrg/Coder), and its central idea, sending prompts into workspaces, no longer matches how the issue watcher was built. A reply is drafted and waiting. Nothing in IronClaude is blocked by it, but the reply also settles one sentence in the planned rewrite of issue #423.

#### Background you need
- The issue watcher (IronClaude #331) was built as a poller inside each workspace. Your design chose no listener, no inbound port and no address list. #477 was written to serve that watcher.
- Any route that can start a session in a workspace starts it with permission checks off on the standard image. That is the main risk of keeping prompt routing.
- `superclaude observe` (the read-only worker dashboard, IronClaude #409) sees only this host. Seeing other workspaces is a planned later release; a TUIBBS screen (your separate TUI platform) is a possible later reader.
- On 2026-11-13 you commented on #477: "Ensure this aligns with Orchestrator and TUI Panel."
- Three replies are drafted: narrow, keep, close.

#### Your options
1. **Narrow to read-only status and identity, with no prompt routing.**
   - If you pick this: the issue is rewritten so an outside reader can see which of your workspaces exist, whether each runs, and each one's status record. Nothing can be sent in. Some placeholders (for example how old a record may be before it counts as stale) are filled first.
   - Upside: answers your alignment comment; removes the risky send route; keeps the real gap on record.
   - Downside: the reply is not ready to paste yet; it designs for readers that do not exist yet; in practice it replaces the issue's problem statement.
2. **Close as superseded, with two reopen conditions.**
   - If you pick this: a ready closing comment says when to reopen (a watcher-design revisit, or a remote or TUIBBS reader that needs other workspaces). One link placeholder in it must be fixed first.
   - Upside: fewest decisions now; honest that nothing waits on it.
   - Downside: may not match your comment of yesterday; the gap is easy to forget once closed.
3. **Keep the listener and prompt routing, with strict guards.**
   - If you pick this: you reopen your watcher design choice; the issue waits for a signed-grant format that does not exist yet.
   - Upside: a path for one place to ask another workspace to act.
   - Downside: the largest attack surface; contradicts the built watcher; cannot be built yet.

#### What the debate found
- Two of three advocates recommended narrowing; the third recommended closing, but only if you confirm single-host and no TUIBBS screen soon.
- All three ranked "keep" last.
- The closing text, called ready to post, still contains a link placeholder.
- Closing changes the issue's state, so the posting permission must say so.

#### Recommendation and confidence
Option 1 (narrow), 55 percent. Close instead if you say the dashboard stays single-host for good and no TUIBBS or remote reader is planned. This matches the spec's recommended answer.

#### If you do not answer
Nothing is posted on #477; the reply is recorded as skipped and the next issue edit in the sequence goes ahead.

#### What this answer does not authorize
Posting the reply itself (that needs its own permission row naming each write, including a close); any work in the Coder repository; any route that sends prompts into a workspace.

#### How to answer
Type, for example: "Q3: option 1, narrow" (or "Q3: option 2, close; single-host for good" / "Q3: option 3, keep").

---

## Q4 (Security or trust = none; Reversibility= easy; Who is affected= other people or repos; Needs the owner's = yes; Cost if the answer= low; Does it grant auth= no; Debate= converged)

### What you meant by "TUI Panel" on the Coder workspace-listener issue

#### Question in one sentence
In your 2026-11-13 comment on Coder#477, "Ensure this aligns with Orchestrator and TUI Panel", what is the "TUI Panel"?

#### Why you are being asked
The reply to Coder#477 must say in one line what it is aligning with. Nobody can tell from the files: the phrase appears in nothing you wrote elsewhere. The answer also affects whether that issue should be narrowed or closed (Q3) and whether a copy of dashboard data should go to another host (Q18).

#### Background you need
- `superclaude observe` is the read-only terminal dashboard of Orca workers (the local agent-orchestration app), built for IronClaude issue #409 and merged. Today it reads one host only.
- Its planned later releases include one for answering coordinator questions (may or may not write; not established) and one that reads a remote fleet.
- TUIBBS is your separate TUI platform on another host. Your 2026-11-08 note said the dashboard "may become a TUIBBS module", marked "Background, not deciding".
- On 2026-11-08 you also replaced #409's Go direction with Python plus Rich.
- Reviewers rate "the #409 dashboard" as the likely meaning (about 70 to 75 percent) and a TUIBBS screen at about 15 percent.

#### Your options
1. **The #409 dashboard, with today's properties only** (the host-neutral proposal, with today's verified facts added). Reply line: "TUI Panel = `superclaude observe` (the #409 dashboard); single-host and read-only today; later readers, including a possible TUIBBS screen, not decided."
   - If you pick this: the line is shown to you, then posted; the copy-to-another-host question stays at "not yet"; the narrow-or-close question is decided on its own.
   - Upside: true today and stays true when later releases ship.
   - Downside: a reader of the Coder issue does not learn whether one host or several must be served.
2. **The #409 dashboard, single-host and read-only (the spec's original line).**
   - If you pick this: the line "TUI Panel = `superclaude observe`; single-host; read-only" is posted.
   - Upside: shortest, firmest statement.
   - Downside: reads as a lasting limit that the planned remote-fleet release would contradict; pushes the Coder issue toward closing.
3. **Both: the dashboard now, and a TUIBBS screen reading its data as the plan.**
   - If you pick this: you are stating a TUIBBS screen is planned; the copy-to-TUIBBS work can be scoped now.
   - Upside: gives the Coder issue a real future consumer.
   - Downside: commits to cross-host work with no plan or task yet, and moves worker data off the host.

#### What the debate found
- Unmodified, two of three advocates picked option 2 and one a host-neutral version; all three then agreed on option 1's line.
- "Single-host" today cannot answer whether the dashboard "stays" single-host, which is what the narrow-or-close decision needs.
- Nothing in the files shows a TUIBBS screen is planned.

#### Recommendation and confidence
Option 1, 64 percent. This partly matches the spec's recommended answer: same meaning, but "single-host" and "read-only" are scoped to "today".

#### If you do not answer
The working reading (the #409 dashboard) is used until you say otherwise; the Coder reply still waits for the narrow-or-close answer.

#### What this answer does not authorize
Posting the reply (that needs its own permission row); any copy of dashboard data to another host; any TUIBBS work.

#### How to answer
Type, for example: "Q4: option 1" (or "Q4: option 2" / "Q4: option 3, a TUIBBS screen is planned" / "Q4: I meant <something else>").

---

## Q25 (Security or trust = high; Reversibility= costly; Who is affected= other people or repos; Needs the owner's = yes; Cost if the answer= medium; Does it grant auth= yes; Debate= split)

### Which session publishes each pull request?

#### Question in one sentence
For each of the program's nine code changes, which session should open the pull request and run the review-and-fix tool `/sc:pr-submit --monitor 3` on your fork?

#### Why you are being asked
Nine work items end in a PR, and none can be published until this is answered. The rules already forbid two candidates. A supervised worker may not push or open PRs. The coordinator may not run the tool, because its waiting loop would block the coordinator's own watch duty.

#### Background you need
- A supervised worker is an agent started under the worker contract. It builds and tests one change, then reports "done" (`worker_done`) for the coordinator to accept.
- `/sc:pr-submit --monitor 3` opens the PR on `IronbellyOrg/IronClaude` and waits for two automatic reviewers. It then fixes, pushes, replies to and resolves their confirmed findings without asking.
- Orca is the app that runs agents. Nobody has checked whether Orca lets a second agent start in a worktree after its worker has finished.
- The worker contract requires that you see unseen changes before they are pushed.

#### Your options

### 1. Worker builds, then a separate PR session publishes (recommended)
- If you pick this: after a worker's result is accepted and its session has ended, the coordinator starts a PR session in the same worktree. That session shows you the diff, waits for your go, then commits and runs the tool. Before the first item, someone checks that Orca allows this. If Orca does not, option 3's route is used, with a deadline check.
- Upside: the code is built under worker supervision; no session of yours per PR.
- Downside: rests on an unchecked Orca behaviour; two agents per change; the publishing session did not write the code.

### 2. You open each PR session yourself
- If you pick this: the coordinator tells you when a change is ready; you open a Claude session in that worktree and run the tool there.
- Upside: you give the instruction to publish yourself, every time.
- Downside: nine sessions you must open and attend; PRs wait whenever you are away.

### 3. One agent per change builds it and publishes it, with no worker
- If you pick this: the coordinator creates one worktree and agent per change; that agent builds, shows you the diff, and runs the tool.
- Upside: simplest; no unchecked Orca behaviour; the author answers its own reviews.
- Downside: loses worker supervision; an agent that stalls before opening its PR is not noticed automatically.

#### What the debate found
- The advocates split three ways on the overall answer, though most single points had a clear majority.
- All agreed option 2 best guarantees you see each diff, option 3 is simplest, and option 1 alone keeps supervision without costing your time.
- All found a rule gap: the worker contract gives commits to the coordinator, but the plan gives them to the PR session. One sentence in decision D3, plus a grant row listing every write, closes it.

#### Recommendation and confidence
Option 1 with option 3 as its fallback, about 55 percent. This is a close call.

#### If you do not answer
No PR is opened. Each change stays uncommitted in its worktree, and its lane is held.

#### What this answer does not authorize
It does not authorize any merge, and no PR is opened without its own permission row. It allows nothing on any repository other than `IronbellyOrg/IronClaude`, and no `/sc:pr-submit` on PR #539, which question Q28 governs.

#### How to answer
Type: "Q25: option 1" (or "Q25: option 2", "Q25: option 3").

---

## Q31 (Security or trust = low; Reversibility= easy; Who is affected= only this program; Needs the owner's = yes; Cost if the answer= low; Does it grant auth= no; Debate= converged)

### Should this program's coordinator run your 10-minute read-only check? (Q31)

**Question in one sentence:** Does your 2026-11-05 order to run a check about every 10 minutes apply to the coordinator of this program, as a read-only check?

**Why you are being asked:** Your order exists only in a memory note, which the plan ranks as its least reliable source, so the plan will not assume it either way. Nothing is blocked. Your answer sets whether one extra recurring check runs.

**Background you need:**
- The coordinator is the Claude session that runs this program and supervises its helper sessions.
- Orca is the app that runs those sessions and carries their messages. The checked-in coordinator rule (WC-16, in the worker contract) already makes the coordinator keep waiting on Orca, and run a status sweep at most once every 5 minutes.
- Your 2026-11-05 order adds a timer, about every 10 minutes, that reads: the Orca job's messages, the list of live sessions, open pull requests on IronbellyOrg/IronClaude and IronbellyOrg/Coder, and renews "tell me when you go idle" requests on busy sessions. You gave it after sessions went unwatched. Sessions that are not Orca workers never show up in Orca's message queue.
- This program will have such sessions: the sessions that open pull requests, and the session that owns PR #539. The sweep command that could list them does not work yet. It needs PR #539 merged and installed first.
- The timer tool stops after 7 days and only fires while the coordinator is idle.

**Your options:**

1. **Yes, read-only, for this program only.**
   - If you pick this: the coordinator starts one timer at the start of the program, records its id and expiry in the decision record, and restarts it after 7 days or after a restart. It reports only when you need to decide something. It never writes and never runs the sweep more often than the 5-minute limit allows.
   - Upside: the program's non-worker sessions and pull requests are seen within about 10 minutes. It matches your order.
   - Downside: a second clock, about 144 reads a day, and the timer can quietly stop if a restart is missed.
2. **No, keep only the checked-in coordinator rule.**
   - If you pick this: no timer. Pull requests are read at phase gates and when the coordinator wakes.
   - Upside: one rule in one checked-in file, less load, nothing to restart.
   - Downside: sessions that are not Orca workers go unwatched until the sweep command works, which is the failure your order was meant to prevent.
3. **Yes, and also write it into the coordinator rules for every project.**
   - If you pick this: same as option 1 now, plus a separate small pull request that adds the check to the worker contract.
   - Upside: future coordinators get the rule without being asked.
   - Downside: changes a file every project receives, on the basis of a one-program question. Adds a pull request now. Its wording is not settled.

**What the debate found:**
- All three debaters, including those assigned to argue for options 2 and 3, chose option 1.
- Option 2 leaves non-worker sessions unseen before the sweep command works.
- Option 3's contract change is sound, but it should be asked as its own item.
- The debate added these details: the check runs only while the coordinator is idle, it sends no messages to the sessions, and it is silent unless a decision is needed.

**Recommendation:** Option 1, about 70 percent confidence. This is the same as the plan's recommended answer.

**If you do not answer:** The coordinator follows only the checked-in rule (no timer). Q31 stays listed as open at the top of the decision record.

**What this answer does not authorize:** running the sweep more often than once every 5 minutes, any write of any kind, or any grant of permission.

**How to answer:** type `Q31: option 1` (or `option 2`, or `option 3`).

---

## Q7 (Security or trust = low; Reversibility= easy; Who is affected= only this program; Needs the owner's = yes; Cost if the answer= medium; Does it grant auth= yes; Debate= converged)

### Saving your own decision records before a side workspace is deleted (Q7)

#### Question in one sentence
Will you confirm that your 2026-11-12 approval record is your own text, and get it and your other decision records out of the side workspace where they are the only copies?

#### Why you are being asked
Several of your records exist only in one side checkout on this machine (untracked files and local commits never pushed). If that checkout is cleaned up or the disk fails, they are gone. The work that switches on the dashboard's questions panel must cite your approval record, and the project rule is that agents may quote your records but never write them, so only you can vouch for them.

#### Background you need
- The side checkout is `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`.
- At risk (checked 2026-11-14): your approval ("pass") record and your 2026-11-12 decision record (in two unpushed commits), and the untracked `owner-decisions-20261108.md`, `live-test-guide.md`, `tuibbs-review/` and `handoff-mvp-brainstorm.md`.
- The approval record says "Written by the owner." at the top, but the commits holding it were made by an agent session, so git cannot prove who typed it.
- The current plan saves the approval record only inside the switch-on change, which may never happen.

#### Your options
1. Freeze today, then save everything now (recommended)
   - If you pick this: today a dated "do not clean" note names every file at risk; you re-read the files, write one dated line saying they are yours, and commit them unchanged to the main branch in a small records-only change (or name an archive). An agent session copies them for you only if you write that this is acceptable. The switch-on change later points to the saved copy.
   - Upside: nothing can be lost, whether or not the panel is ever switched on; reviewers can read the records.
   - Downside: about one sitting of your time; one written condition of the plan ("the approval record is committed in the switch-on change") must be reworded.
2. Do it yourself, on the plan's original schedule
   - If you pick this: you commit the decision records in the next batch of work; the approval record goes in with the switch-on change.
   - Upside: matches the plan exactly; no rewording.
   - Downside: the approval record stays a single copy until the switch-on happens, and the side checkout could be cleaned before then.
3. Not now; freeze the side checkout and ask later
   - If you pick this: a dated "do not clean" note only; nothing is saved; asked again when the switch-on is scheduled.
   - Upside: no effort now.
   - Downside: single copies for an open-ended time; the note is not a lock; correcting the dashboard's issue text stays blocked.

#### What the debate found
- Two of three advocates chose option 1's core; the third chose option 2 plus the freeze. All three agreed the approval record must be saved before any cleanup, not only with the switch-on.
- All three agreed you should re-read the files first, because git cannot show who typed them.
- The open split is whether an agent may make the copy; the recommendation defaults to you.

#### Recommendation and confidence
Option 1, 65 percent. It is the only option where no record can be lost whatever happens to the switch-on.

#### If you do not answer
The side checkout must not be cleaned, the switch-on change cannot open, and the records stay single copies.

#### What this answer does not authorize
It does not switch the panel on, does not choose which work sessions the panel may read, and does not let any agent edit or write your records. A copy by an agent session happens only if you say so in writing.

#### How to answer
Type: "Q7: option 1, I will commit them myself" (or "Q7: option 1, a named session may copy", "Q7: option 2", "Q7: option 3"), and say whether to save `handoff-mvp-brainstorm.md`.

---

## Q8 (Security or trust = none; Reversibility= easy; Who is affected= only this program; Needs the owner's = yes; Cost if the answer= low; Does it grant auth= no; Debate= converged)

### Recording, in your own words, which dashboard design direction you chose (Q8)

#### Question in one sentence
Will you write one short dated paragraph recording the design direction you chose for the dashboard, or would you rather rewrite the issue's first acceptance criterion instead?

#### Why you are being asked
Issue #409 (the dashboard issue) has the acceptance criterion "A human selects the visual direction before production integration." The dashboard's own rules say this is met only by a dated record written by you, never by an agent. That record does not exist, so the criterion cannot be marked met, the issue text cannot be corrected on this point, and the next release (Decision Desk) is blocked.

#### Background you need
- The dashboard is `superclaude observe`, a read-only terminal view of agent work. Releases 1 and 2 are merged.
- You chose a staged direction on 2026-11-08 (worker list first, then the question list, then Decision Desk). That decision was written down by an agent session relaying your instruction, so it does not count as your own record.
- The rules list the fields the record must cover (date, option, who decided, where your statement lives, defaults before and after questions are shown, post-link choice, fallback date, stack, command name, and what "production integration" means).
- "Production integration" has two possible meanings in the rules: the command being in the shipped tool, or the dashboard being switched on in the product. Until you say which, the stricter one applies.

#### Your options
1. Write the record now, keep the criterion (recommended)
   - If you pick this: you write one dated paragraph covering the listed fields briefly (post-link choice and fallback date may say "deferred to release 3"); agents cite it. The issue then says the direction was selected on 2026-11-08 and recorded later. If you have not written it by the time the issue is corrected, the issue says "not met as recorded" meanwhile.
   - Upside: meets the rule exactly; settles what "production integration" means; unblocks the next release.
   - Downside: a few minutes of writing; you choose where the file lives; it is written after the first two releases shipped, and says so.
2. Rewrite the acceptance criterion instead
   - If you pick this: you approve new criterion text describing the staged choice, citing your earlier decisions.
   - Upside: no new document.
   - Downside: the dashboard's rules on the main branch still demand your own record, so they must be changed too; it reads as moving the bar after the work shipped.
3. Neither now
   - If you pick this: the issue says honestly that the criterion is "not met as recorded"; the record waits until the next release is started.
   - Upside: no effort now.
   - Downside: the next release has no date, so this may never close; the strict meaning of "production integration" stays in force.

#### What the debate found
- All three advocates, including those for options 2 and 3, chose option 1 (3 of 3), mean confidence 68 percent.
- The earlier 2026-11-08 file was written by an agent, so it cannot be the record.
- Option 1 as first drafted covered only three of the eleven fields; the recommendation now covers all of them.

#### Recommendation and confidence
Option 1, 68 percent. Only a record written by you satisfies the rule and settles what "production integration" means.

#### If you do not answer
The issue correction posts without any status line for this criterion and without changing it, and the next release cannot start.

#### What this answer does not authorize
It does not let an agent write the record for you, does not switch on any part of the dashboard, and does not start the next release by itself.

#### How to answer
Type: "Q8: option 1, I will write it at <location>" (or "Q8: option 2", or "Q8: option 3").

---

## Q20 (Security or trust = high; Reversibility= easy; Who is affected= only this program; Needs the owner's = yes; Cost if the answer= medium; Does it grant auth= yes; Debate= converged)

### Who is responsible for the issue watcher's sessions? (Q20)

#### Question in one sentence
Who owns the agent in the issue watcher's working folder, and may that folder collect up to 6 new Claude sessions a day that no coordinator session looks after?

#### Why you are being asked
The watcher's first live test, the setup step that creates its folder, and one planned edit to issue #450 (the watcher rollout issue) all wait on this answer. Without it the watcher cannot be tested or switched on.

#### Background you need
- The issue watcher is a background process: when an issue is approved, it starts a Claude session that claims the issue. It is not part of the coordinator's managed work.
- Every session starts in one shared Orca working folder (a "worktree"). Orca's rule: whoever creates a worktree with an agent owns that agent.
- It starts at most 6 sessions in 24 hours (a value fixed in code, meant for you to confirm after a trial run). Nothing closes these sessions; the setup guide says to close them yourself in Orca.
- The sessions read issue text that anyone who can comment can write. On this host they run with permission checks off (a separate question, Q2).
- The coordinator session's duty ends when its own batch of work is done; it can only see these sessions as rows it "could not determine".

#### Your options

### 1. A person you name owns it; sessions stay person-reviewed (recommended)
- If you pick this: that person creates the folder and owns its agent; up to the confirmed cap (default 6) of sessions a day are allowed, never coordinator-owned. The one-session live test runs now. Before the schedule is switched on, you write down who closes sessions and when, how often the person checks, and who covers when they are away.
- Upside: matches how the watcher was designed; keeps outsider-written text away from the coordinator.
- Downside: relies on that person actually looking and closing sessions by hand.

### 2. Decide nothing yet
- If you pick this: no folder, no live test, no schedule; asked again together with a cleanup rule.
- Upside: no unattended sessions at all.
- Downside: the watcher stalls, and the cleanup rule needs the live test's results anyway.

### 3. The coordinator session owns it and reviews the sessions
- If you pick this: the coordinator creates the folder and lists watcher sessions in its regular checks; a person still closes them.
- Upside: something already running keeps an eye on them.
- Downside: the coordinator stops when its own work ends, cannot really see these sessions, and would be exposed to outsider-written text.

#### What the debate found
- All three debaters, including those arguing for options 2 and 3, judged option 1 best (60 to 70 percent).
- Option 2's caution belongs before switching the schedule on, not before a one-session test; that was added to option 1.
- The 6-a-day cap is yours to confirm or lower (a small code change).

#### Recommendation and confidence
Option 1, 70 percent.

#### If you do not answer
The same as option 2: the setup step and the #450 edit are left out, and the watcher's live test does not run.

#### What this answer does not authorize
It does not authorize the live test itself (that also needs the claim-level answer and your written acceptance of the session's permission mode, Q2), switching on the schedule, or any coordinator adopting watcher sessions.

#### How to answer
Type: "Q20: option 1, owner is <name>" (or "Q20: option 2" or "Q20: option 3").

---

## Q28 (Security or trust = high; Reversibility= costly; Who is affected= only this program; Needs the owner's = yes; Cost if the answer= medium; Does it grant auth= yes; Debate= split)

### How much may the PR review tool do on PR #539?

#### Question in one sentence
May the automated PR review tool `/sc:pr-submit` work on PR #539, and if so, when and with how much freedom?

#### Why you are being asked
PR #539 holds an open security finding that waits for your ruling. At its highest level, the tool fixes review findings by itself, then pushes, replies and resolves threads. On #539 it could design and push its own fix for that security finding and bypass your ruling. Merging #539 needs a decision on whether the tool helps or a person does everything by hand.

#### Background you need
- PR #539 adds the read-only `superclaude sweep` command. It has 1003 files and is open, not a draft, with merge state UNSTABLE (read 2026-11-14).
- The security finding: the sweep's `git status` call can run commands that a repository's git settings define. You rule on it (Q1); then the PR author applies your ruling (work item SW-02).
- Tool levels: level 1 proposes fixes only; level 2 applies fixes on the local machine and stops; level 3 also commits, pushes, replies on review threads and resolves them.
- The tool ignores a review thread only once it is marked resolved; a reply alone is not enough (checked in the tool's rules).
- With `--merge-guard off`, the tool's check that the PR is still open before pushing may not run (its own documents disagree). A push after a mid-cycle merge has happened before (PR #368).

#### Your options

### 1. Nothing until the ruling lands and Codex's next review is clean; then the full tool (recommended)
- If you pick this: the PR author pushes by hand until your ruling is applied, the security thread is marked resolved, and the automated Codex reviewer has checked the ruling's push with no new git-settings finding. After that the author runs the tool at level 3 without the draft toggle, under a list of approved actions you write. The tool never merges, stops on any git-settings finding, and checks the PR is open before every push.
- Upside: the risky moment passes under human control; after it, the tool's verification and push checks help on a very large PR.
- Downside: the stop on git-settings findings is a written instruction, not a switch in the tool; hand work until Codex reports back.

### 2. After the ruling, level 2 only: the tool fixes locally and a person pushes
- If you pick this: the tool verifies and applies fixes on the local machine; the PR author reads each one and pushes, replies and resolves by hand.
- Upside: a person sees every change before it leaves the machine.
- Downside: slower, hand pushes lose the tool's checks, and the tool may still post one report comment if the other automated reviewer, Augment, declines the PR as too large.

### 3. Never use the tool on #539
- If you pick this: the PR author handles every finding, failing check, push, reply and resolve by hand until you merge.
- Upside: no automated action on the PR that carries the security finding.
- Downside: much hand work on a 1003-file PR, no automatic check that a finding is real, and no later point to relax the rule.

#### What the debate found
- The three advocates split: each kept its own option, and none agreed on how much freedom the tool should have after the ruling.
- All agreed: no tool at all before the ruling (the spec's optional "propose only" level would still draft a fix for the security finding); the thread must be marked resolved, not just replied to; check the PR is open before every push.
- The newest risk is Codex's review of the ruling's own push, because that push changes the same git code.

#### Recommendation and confidence
Option 1. Confidence 55 percent.

#### If you do not answer
Option 3 applies: no tool on #539 at any level, and the author pushes by hand.

#### What this answer does not authorize
A merge; any issue post; your ruling reply on the security thread; any fix of the security finding designed by the tool; or the tool on any other PR.

#### How to answer
"Q28: option 1, with `--merge-guard off`" (or "option 1 with the draft toggle", "Q28: option 2", "Q28: option 3").

---

## Q30 (Security or trust = low; Reversibility= easy; Who is affected= only this program; Needs the owner's = partly; Cost if the answer= low; Does it grant auth= yes; Debate= converged)

### Which coordinator may the questions-panel test read?

#### Question in one sentence
For the one live test of the observer's questions panel, which coordinator's work may it read, and do you accept in writing that questions there might be lost?

#### Why you are being asked
The observer (`superclaude observe`, the read-only dashboard of Orca workers) has a panel that shows questions workers send to their coordinator. It is switched off. Switching it on needs one live test in a real coordinator's terminal. Nobody has proved whether the panel's read removes questions from the coordinator's mailbox, so the test could make a question vanish.

#### Background you need
- In Orca, a Run is one coordinated piece of work. A coordinator is the Claude session you open to hold a Run and direct its workers.
- Only the terminal that holds a Run can read its questions (a test on 2026-11-11 showed this), so the test must run in the coordinator's own terminal.
- Orca's help text says the panel's read "does not mark read", but nobody has tested it on a live coordinator (open, estimated 61 percent).
- An earlier step tests a throwaway Run with planted messages first. It cannot show what happens with a live coordinator that is waiting for questions and confirming answers.
- The program's own coordinator must never be the test subject: losing its workers' questions would break the program.

#### Your options

### 1. A throwaway coordinator you open just for the test (recommended)
- If you pick this: after the planted-message test passes, you open a test coordinator and start one test worker that asks one known question. While the question is unanswered, the panel reads it. Loss is judged by whether that known question still reaches the coordinator. Then everything is closed.
- Upside: real waiting and confirming behaviour, and nothing of value can be lost.
- Downside: setup work (a test coordinator, a worker and its worktree), and Orca must be up.

### 2. A real coordinator from your other work, at a quiet moment
- If you pick this: the panel reads a coordinator you are already running for something else, when no worker is waiting.
- Upside: the most realistic test; no setup.
- Downside: a real question could be lost; the spec's own rule says the Run must carry no work whose questions matter; and a quiet moment means no question is pending, so the test shows little.

### 3. No live test for now
- If you pick this: the test is held and the panel stays off.
- Upside: nothing can be lost.
- Downside: the questions panel never ships while this holds.

#### What the debate found
- All three advocates chose option 1, including the two assigned to the other options.
- They found one flaw in option 1 as first written: the question must still be unanswered when the panel reads, or the test proves nothing.
- Checking for a lost question with a plain read would itself remove messages, so loss is judged against the known test question.

#### Recommendation and confidence
Option 1, and yes, accept that questions in the throwaway Run may be lost. Confidence 85 percent.

#### If you do not answer
Option 3 applies: the live test is held and the PR that switches the panel on is not opened.

#### What this answer does not authorize
Binding the observer to any other Run (`run-use`); reading any Run other than the one you name; reading the program's own coordinator; or switching the panel on (a separate PR with its own approval).

#### How to answer
"Q30: option 1, and yes, I accept that questions in the test Run may be consumed" (or "Q30: option 2" with the Run id, or "Q30: option 3").

---

## Q24 (Security or trust = low; Reversibility= easy; Who is affected= only this program; Needs the owner's = partly; Cost if the answer= medium; Does it grant auth= no; Debate= converged)

### Who should make the live Orca checks?

#### Question in one sentence
Which session (or person) should run three live checks against Orca: a read-only capture of a few unknown fields, a one-time comparison of worker ids between the dashboard and the sweep report, and a test that writes throwaway messages?

#### Why you are being asked
Without a named runner, none of the three runs. That blocks the gate check for Orchestrator v2 (issue #423) and the dashboard's PR that turns on its questions panel. The review suggested "the 409 session, in one sitting". The debate found two problems with that.

#### Background you need
- Orca is the local app that runs agent workers. The dashboard is `superclaude observe`. The sweep is the coordinator's read-only report (PR #539, not merged yet).
- "The 409 session" is the agent that built the dashboard, in worktree `issue-409-mvp`. That worktree is on an unmerged branch and holds unpushed commits and records that must not be lost. Nobody has checked whether that session is still alive.
- The comparison must run the sweep on merged (master) code, so it can only happen after PR #539 merges. That makes it a second sitting, two waves after the first.
- The message-writing test needs its own separate permission.

#### Your options

### 1. A fresh session on master, made for this job (recommended)
- If you pick this: the coordinator creates a new Orca worktree from master with its own agent. That agent runs the capture now and the comparison after the merge. It may ask the 409 session questions but does not use it to run anything. You run the message-writing test yourself unless you name someone else.
- Upside: certain to exist; on the right code; cannot touch the 409 worktree's unsaved work.
- Downside: one more worktree to create and clean up; the new agent starts without dashboard history.

### 2. The 409 session (the review's suggestion)
- If you pick this: the coordinator checks that the session is alive and that its terminal is not bound to a Run, then it runs all three, each under its own permission.
- Upside: it knows the dashboard and has run similar checks safely before.
- Downside: if it has ended, nothing runs; its branch is not master; its unsaved work is at risk.

### 3. You run them by hand
- If you pick this: an agent writes step-by-step procedures, and you run each check at a plain terminal.
- Upside: no agent makes live Orca calls.
- Downside: three sittings of your time; hand-typed commands drift more easily.

#### What the debate found
- 2 of 3 advocates chose option 1; 8 of 10 points agreed. Who runs the message test, and whether agents should make live calls at all, stayed open.
- A past failure only blocked reading another Run's mailbox, not listing its workers. The first step of the capture should confirm this.

#### Recommendation and confidence
Option 1, about 65 percent.

#### If you do not answer
None of the three checks runs. The Orchestrator v2 gate check cannot pass, and the dashboard's questions panel stays off.

#### What this answer does not authorize
It does not grant any permission row. Each check still needs its own row in the ledger. The message-writing test needs its own write permission. No `run-use`, no merge, and no message to a live coordinator.

#### How to answer
Type: "Q24: option 1" (or "Q24: option 2", "Q24: option 3"). With option 1, you can add "and I run the message test" or name a runner for it.

---

## Q16 (Security or trust = high; Reversibility= easy; Who is affected= other people or repos; Needs the owner's = partly; Cost if the answer= medium; Does it grant auth= no; Debate= converged)

### How far should the trust promise go across the three planned programs? (Q16)

#### Question in one sentence
Should the project promise one shared trust design for all three planned programs, or only one shared set of permission names plus one shared audit log format, with each program checking permissions its own way?

#### Why you are being asked
Three issue texts wait on this sentence: the observer dashboard issue (#409, its design decision 6 now says "Decide one design, not two."), the Orchestrator v2 issue (#423) and the workspace listener issue (Coder#477, in the separate IronbellyOrg/Coder repository). Later work also waits on it: the future trust layer, the v2 design, and the observer's planned answer screen, which must log every answer in the agreed terms. Nothing is built yet; this is a promise in issue text.

#### Background you need
- "Trust" here means who may do what (for example read a status or answer a question) and how that is checked and logged.
- The three programs face different risks: the observer only reads, on one machine; the first v2 release reads only what the same user on the same machine can read; the listener would cross between separate Coder workspaces.
- A Medium-confidence (66 percent) earlier review leaned toward the narrower promise and said the point cannot be decided from documents alone.
- Signing messages does not stop harmful text being passed along; that is handled by a separate rule that relayed text stays plain typed data.
- No trust layer, permission format or signing exists today.

#### Your options

### 1. One shared vocabulary and one shared audit record (recommended)
- If you pick this: #409 decision 6 becomes "Decide one grant vocabulary and one audit record."; #423 and Coder#477 promise the shared terms, not a shared design. The terms themselves are written later, in the trust-layer work, with one owner; you re-confirm when that starts.
- Upside: each program gets checks that fit its own risk; logs from all three can be read side by side; small, reversible text change.
- Downside: three mechanisms to review; the same word could mean weaker protection in one program unless each term says what it enforces.

### 2. Promise nothing yet (the default)
- If you pick this: #409 keeps "Decide one design, not two."; #423 and Coder#477 say nothing about trust; later trust work stays on hold.
- Upside: no new promise before a design exists.
- Downside: #409 still promises one design while the others say nothing, so the issues disagree; the held work waits on a step that itself waits on this answer.

### 3. One trust design for all three
- If you pick this: the permission format and checking chosen under #339 (the Orchestrator mode issue) become the only ones; #409 keeps its sentence; #423 and Coder#477 say they use it and define no second format.
- Upside: one thing to build and test; one owner; no translation between programs later.
- Downside: the spec lists one trust design as out of scope; one design either over-builds the read-only observer or under-protects the listener; it can give a false sense of safety.

#### What the debate found
- All three debaters, including the ones arguing for options 2 and 3, judged option 1 best (65 to 70 percent).
- The spec itself says only the shared vocabulary and audit format are "in reach".
- The default (option 2) is not neutral: it leaves a one-design promise in #409.
- Option 1 was strengthened with option 3's single owner and option 2's "ask again when a real design exists".

#### Recommendation and confidence
Option 1, 70 percent.

#### If you do not answer
The default applies: #409 decision 6 is left unchanged, #423 and Coder#477 promise nothing about trust, and the trust-layer, v2 design and observer answer-screen work that needs the shared terms stays on hold.

#### What this answer does not authorize
It does not authorize passing knowledge between agents (relay), any issue edit by itself (edits still go through the single editor and their own permission), or any code.

#### How to answer
Type: "Q16: option 1" (or "Q16: option 2" or "Q16: option 3").

---

## Q13 (Security or trust = low; Reversibility= easy; Who is affected= only this program; Needs the owner's = no; Cost if the answer= low; Does it grant auth= yes; Debate= converged)

### Which Orca program the observer may run (owner question 13)

#### Question in one sentence
May the observer dashboard fall back to a program simply named `orca` on the system path, when the sweep's rule is to never do that?

#### Why you are being asked
The two programs find the Orca command line differently, and the planned contract note between them (a design file recording how they relate) must say whether that difference is accepted. Accepting it is a small written acceptance of risk, so it is yours.

#### Background you need
- Orca is the local agent-orchestration app; both programs call its command line. On this host it is reachable as `orca-ide` and as `orca`.
- On Linux, a program named `orca` outside Orca's own terminals is usually the GNOME screen reader, not Orca.
- The observer (`superclaude observe`, merged) tries `orca-ide`, then `orca`, and uses one only if it answers an Orca-only question (`skills list --json` must list `orca-cli`). The issue watcher does the same.
- The sweep (`/sc:sweep`, PR #539) uses the variable `ORCA_CLI_COMMAND` if set, else `orca-ide`, and never `orca`. It asks no question first.
- So the two differ only if `ORCA_CLI_COMMAND` is set, or `orca-ide` is missing or fails. Today the variable is unset and both use `orca-ide`.

#### Your options
1. **Yes, and write down the limit** (recommended)
   - If you pick this: the contract note records both rules, says the check proves "this is Orca" but not "the same Orca the sweep reads", records the Orca build next to each capture, and you are asked again if builds differ or `ORCA_CLI_COMMAND` is used. Two small gaps are logged for later, not fixed now.
   - Upside: no code change; keeps working where only `orca` exists; future programs get a stated rule.
   - Downside: two rules stay; a silent fallback to `orca` can happen if `orca-ide` is slow or broken.
2. **No: make the observer use the sweep's rule**
   - If you pick this: a small observer PR makes it use `ORCA_CLI_COMMAND`, else `orca-ide`, keeping the Orca check.
   - Upside: both read-only programs always read the same Orca, which helps a planned comparison of their records.
   - Downside: changes working code for a problem never seen; hosts with only `orca` stop working until the variable is set.
3. **No ruling: record both rules as facts**
   - If you pick this: the note lists both rules with no verdict; you are asked only if a difference is ever seen.
   - Upside: spends no decision on an unseen problem.
   - Downside: the next program that calls Orca has no rule to copy.

#### What the debate found
- Two of three advocates picked option 1 when unassigned; one picked option 2 narrowly.
- All three agreed the Orca check proves identity, not sameness.
- On a normal host both programs already read `orca-ide`; the fallback matters only where `orca-ide` is missing.

#### Recommendation and confidence
Option 1, 72 percent.

#### If you do not answer
The note records both rules without a verdict (the same as option 3).

#### What this answer does not authorize
No code change to the observer, the watcher or the sweep, no edit to PR #539, and no fix of the two logged gaps.

#### How to answer
Type: "Q13: option 1" (or "Q13: option 2" or "Q13: option 3").

---

## Q22 (Security or trust = none; Reversibility= easy; Who is affected= other people or repos; Needs the owner's = partly; Cost if the answer= low; Does it grant auth= no; Debate= converged)

### How old can a status file be before readers call it stale?

#### Question in one sentence
When a program reads a status file written by another program, at what age should it say "this file is stale" instead of treating it as current?

#### Why you are being asked
Two pieces of text are waiting on this: the contract note that describes what the observer and the sweep share (XC-05), and the narrowed text of the Coder issue Coder#477, which has an open blank "[N minutes: owner decides]". The review left the number to you.

#### Background you need
- The observer (`superclaude observe`) is the built dashboard of Orca agent workers. While running, it checks every 15 seconds and rewrites a file, `snapshot.json`, each time, even after a failed check. After errors it waits up to 60 seconds.
- On its own screen it calls its data stale after 45 seconds (three missed checks).
- The file has a timestamp, `generatedAt`, and no "still alive" flag. The file also already says, inside it, whether its data was fresh.
- The Coder workspace record and a copy channel to the owner's other platform (TUIBBS) are not built. Nobody reads these files yet.

#### Your options

### 1. A rule: stale after three intervals or the longest normal gap, whichever is larger (recommended)
- If you pick this: the observer's file is stale after about 75 seconds (inferred from its code); the Coder record and copy channel get numbers when they are designed. Readers always print the age and keep "stale file" separate from "stale data".
- Upside: matches how the observer actually writes; no guess for things not built yet.
- Downside: the Coder issue shows a formula, not a number; 75 seconds is inferred, not measured.

### 2. One fixed number now (suggested: 2 minutes, or your own)
- If you pick this: both kinds of record are stale after 2 minutes; future producers must write at least that often.
- Upside: one plain number; closes the Coder issue blank now.
- Downside: a guess for a producer that does not exist; little time left for copying the file to another host.

### 3. No number yet
- If you pick this: keep the review's stopgap ("older than one of the producer's cycles is stale") and ask again when a reader is built.
- Upside: decided against a real reader later.
- Downside: the stopgap (about 15 seconds) would make a normal observer file flip between fresh and stale; the Coder issue blank stays open.

#### What the debate found
- All three advocates agreed the stopgap in option 3 flickers and should not be kept.
- The code shows a live observer can leave about 75 seconds between writes, so 45 seconds is too tight for the file.
- Option 1 won 6 of 10 points; option 2's number won on the observer threshold only.

#### Recommendation and confidence
Option 1, about 70 percent.

#### If you do not answer
The stopgap applies: readers call any file older than one producer cycle stale and print its age. The Coder issue keeps "[N minutes: owner decides]".

#### What this answer does not authorize
It does not post anything to Coder#477, build any reader, or add any field to the snapshot file.

#### How to answer
Type: "Q22: option 1" (or "Q22: option 2, N minutes", or "Q22: option 3").

---

## Q14 (Security or trust = none; Reversibility= easy; Who is affected= only this program; Needs the owner's = partly; Cost if the answer= medium; Does it grant auth= no; Debate= converged)

### When Orchestrator v2 may start (owner question 14)

#### Question in one sentence
Issue #423 (Orchestrator v2) says it starts "after #339 is complete": what exactly must be finished first?

#### Why you are being asked
The words can be read several ways, so the start gate cannot be checked as written. Your answer sets the #423 rewrite's sequencing sentence and decides whether a small sweep code change becomes a prerequisite.

#### Background you need
- #339 is Orchestrator mode. Its Phase 1 is the read-only sweep (`/sc:sweep`), open as PR #539. Later phases (`/sc:close`, resume, a trust layer) are not built.
- #423 is v2: a planned advisory knowledge layer that reports to a person or the coordinator session. Nothing of it exists.
- The sweep sorts sessions into classes. Its `working` class is switched off today, because the exact names Orca uses for "live" and "waiting" were never recorded, so working sessions show as "could not determine".
- A planned one-time read-only "shared capture" of live Orca values (tracked in issue #534) would record those names. Restoring the `working` class afterwards is a separate small code PR.

#### Your options
1. **PR #539 merged plus the capture recorded** (recommended)
   - If you pick this: v2 waits for the sweep merge and the capture record; the gate entry also says whether the recorded values are enough to switch the `working` class on; the code fix stays a follow-up. Optionally you set a date after which v2 may start without the capture, marking those fields pending.
   - Upside: v2 is designed with real Orca values; the gate is two checkable records; matches the plan as written.
   - Downside: still waits on a live Orca session (unreachable on 2026-11-13); v2 may launch while the sweep still says "could not determine" for working sessions.
2. **PR #539 merged, capture recorded, and the `working` class restored in code**
   - If you pick this: a small sweep PR (with its own review and your grant) must merge before v2 starts.
   - Upside: proved by a passing test; v2 sits on a sweep that can say "working".
   - Downside: slowest; puts a code change on a planning gate; if Orca does not expose what the rule needs, v2 waits on a sweep redesign.
3. **PR #539 merged only**
   - If you pick this: v2 design starts at the merge; fields that need live values are marked pending until the capture.
   - Upside: fastest; cannot be stalled by Orca being unavailable.
   - Downside: likely rework when the capture arrives; the list of "live-value fields" does not exist yet.
- In all three, `/sc:close`, resume and the trust layer come first only if v2 decides to send messages to agents, not just report to a person.

#### What the debate found
- All three advocates, asked what they would pick if unassigned, picked option 1.
- The capture is a record; restoring the class is code. The plan already treats them separately.
- Option 2's best point (check the values are enough) and option 3's best point (a fallback if Orca stays down) were folded into option 1.

#### Recommendation and confidence
Option 1, 80 percent.

#### If you do not answer
The plan uses option 1 as its default, labelled "default" in the #423 rewrite.

#### What this answer does not authorize
It does not authorize editing issue #423, running the live capture, any sweep code change, or starting v2 work; each needs its own grant or answer.

#### How to answer
Type: "Q14: option 1" (optionally "with fallback date YYYY-MM-DD"), or "Q14: option 2" or "Q14: option 3".

---

## Q15 (Security or trust = high; Reversibility= easy; Who is affected= only this program; Needs the owner's = partly; Cost if the answer= medium; Does it grant auth= no; Debate= converged)

### May v2 push corrections into sessions that are not Orca workers (owner question 15)

#### Question in one sentence
Must the planned v2 knowledge layer ever send a course correction directly into a session that is not an Orca worker, or should it only report to you or the coordinator?

#### Why you are being asked
Issue #423 (v2) says it should "relay them to affected agents". That would mean pushing content into sessions the current rules say are never messaged. The answer sets v2's design and decides whether the unbuilt trust layer becomes a v2 prerequisite. It is a trust-boundary call.

#### Background you need
- Orca is the local agent-orchestration app. A worker is a session Orca starts for one task; a coordinator is the person-opened session that supervises workers.
- Other sessions: ones you start yourself, ones the issue watcher starts (they may run unattended), and ones with no Orca run.
- Today the coordinator corrects a worker only by leaving a message the worker picks up itself (rule WC-12). Person-started sessions "are never messaged".
- No known channel delivers a message into a non-worker session. Signing messages does not stop harmful content inside them.
- v2 is planned and advisory; nothing of it exists.

#### Your options
1. **Report only, with a condition for ever reopening** (recommended)
   - If you pick this: v2 reports to you or the coordinator; for workers, the coordinator decides whether to send a follow-up. The question is reopened only once a channel, a threat model for harmful content, a rule on whether you approve each correction, and a shared grant vocabulary exist.
   - Upside: no new way into your sessions; no trust layer needed for v2; easy to widen later.
   - Downside: narrows #423's "relay to affected agents"; unattended watcher-launched sessions are never corrected automatically.
2. **Never, as a standing rule for every program**
   - If you pick this: same v2 behaviour, but written as a permanent rule for all future programs.
   - Upside: the strongest boundary.
   - Downside: binds future designs nobody has researched; reopening means overriding a standing rule.
3. **Yes eventually, behind the trust layer**
   - If you pick this: the first release reports only, but v2 plans to deliver into non-worker sessions once the #339 trust layer exists, which moves that unbuilt work onto v2's path.
   - Upside: keeps #423's purpose; could correct unattended sessions.
   - Downside: no channel is known; opens a way into sessions that are never messaged today; longer path.

#### What the debate found
- All three advocates, asked what they would pick if unassigned, picked option 1.
- For every release actually planned, options 1 and 2 behave the same; option 1 avoids binding the future.
- The real gap is unattended watcher-launched sessions; it is recorded as an open case.

#### Recommendation and confidence
Option 1, 82 percent.

#### If you do not answer
Report only (the same v2 behaviour as option 1, without the reopening condition).

#### What this answer does not authorize
No edit to issue #423 or to the worker contract, no new message channel, and no v2 work; each needs its own grant or answer.

#### How to answer
Type: "Q15: option 1" (or "Q15: option 2" or "Q15: option 3").

---

## Q19 (Security or trust = none; Reversibility= easy; Who is affected= only this program; Needs the owner's = yes; Cost if the answer= low; Does it grant auth= no; Debate= split)

### Which dashboard improvement should be built first? (Q19)

#### Question in one sentence
Of the four improvements a reviewer asked for on the worker dashboard, which comes first, and should the dashboard itself or the coordinator's report carry it?

#### Why you are being asked
The dashboard's third release (the "Decision Desk" screen) cannot start until someone names the first improvement and where it lives. If you do not answer, that release does not start.

#### Background you need
- The observer (`superclaude observe`) is the built, read-only terminal dashboard of agent workers. The sweep is a read-only report a coordinator session writes about its workers; it is a local file that is never posted, and it is still in an open pull request (#539).
- A reviewer on 2026-11-11 asked for four things, named after design pictures: Fleet Quilt, Decision Desk, Loop Detector or Mission Pulse (named steps with green, yellow, red), and a plain-English summary with issue and PR links.
- Decision Desk depends on a link between a coordinator question and a specific worker that is not established yet. What data Fleet Quilt needs is not written down anywhere.
- The summary and named steps have a known data source today: each task's brief and the progress files workers already write.
- An earlier review read the reviewer as valuing Fleet Quilt and Decision Desk most; nobody has shown the reviewer actually ranked them.

#### Your options

### 1. Fleet Quilt first on the dashboard; the summary second (recommended)
- If you pick this: Fleet Quilt gets a dashboard release row, started after the shared field definitions and one recorded live check exist; its first step is writing down what data it reads. The summary and named steps are recorded as the second item; the report can prepare their data once #539 merges.
- Upside: the reviewer gets a screen where they look; it avoids the Decision Desk blocker.
- Downside: Fleet Quilt's data is unknown, so it is not quick.

### 2. The summary and named steps first, in the coordinator's report
- If you pick this: the report gains a plain task title and step states after #539 merges.
- Upside: buildable soonest, from data that already exists.
- Downside: it appears in a report the reviewer never sees, unless you later allow sweep facts on the dashboard (Q17).

### 3. Do not pick yet
- If you pick this: nothing starts until the Decision Desk link and the related records exist.
- Upside: no commitment while inputs are missing.
- Downside: the same as not answering; the reviewer gets no answer.

#### What the debate found
- Two of three debaters favoured a dashboard screen first; one favoured the summary because only it can be built now.
- The earlier review that found the summary's data source itself says to choose the screen direction first.
- Nobody confirmed the reviewer's priority order.

#### Recommendation and confidence
Option 1, 55 percent. Re-read the reviewer's 2026-11-11 comment on #409 first; if it says the summary matters most, choose option 2. Choose Decision Desk instead of Fleet Quilt if you prefer it; it then waits for its link to be established.

#### If you do not answer
Release 3 of the dashboard does not start and none of the four improvements moves.

#### What this answer does not authorize
It does not authorize any code, any change to the sweep's allowed commands, showing sweep facts on the dashboard, or any reply on #409.

#### How to answer
Type: "Q19: option 1, Fleet Quilt" (or "Q19: option 1, Decision Desk", "Q19: option 2" or "Q19: option 3").

---

## Q29 (Security or trust = low; Reversibility= easy; Who is affected= other people or repos; Needs the owner's = yes; Cost if the answer= low; Does it grant auth= yes; Debate= converged)

### How should this workspace get the new sweep command?

#### Question in one sentence
Once PR #539 is merged, should this workspace's `superclaude` command get the new sweep command through the Coder template or through a one-time reinstall you approve?

#### Why you are being asked
The coordinator session is meant to run `/sc:sweep` (a read-only report on its workers), and one later test (the join comparison between the observer and the sweep) needs it. The installed command does not have the sweep yet, and your rule says updates reach workspaces only through the Coder template.

#### Background you need
- The Coder template (`IronbellyOrg/Coder`) builds the workspace image and pins which IronClaude commit it installs. A daily workflow opens a PR to bump that pin when IronClaude master moves; after that PR is merged, the image is rebuilt and each workspace is updated.
- This workspace has two copies of the command (checked 2026-11-14): the image copy in `/usr/local/bin`, and a second copy in `/home/coder/.local/bin` installed by hand on 2026-11-12 at 22:12 (who installed it is unknown). The second copy comes first, so it is the one that runs.
- `/home/coder` survives template updates. So a template update alone would not change which copy runs here.
- A workspace update builds a new container, which ends running sessions.

#### Your options

### 1. Coder template, then remove the extra copy (recommended)
- If you pick this: after the merge, start the Coder pin-bump workflow by hand, merge its PR, update the workspace between sessions, then approve removing the copy in `/home/coder/.local/bin`. The coordinator then checks that the sweep runs.
- Upside: follows your update rule; every workspace runs the same reviewed version.
- Downside: takes longer (a Coder PR, an image build and a workspace update); the update ends running sessions.

### 2. A one-time reinstall on this workspace
- If you pick this: after the merge, you approve reinstalling the command in `/home/coder/.local/bin` at the exact merge commit; you remove it later, when the template catches up.
- Upside: working within minutes; no restart.
- Downside: an exception to your update rule; this workspace runs a different version from the others until the clean-up.

### 3. Decide later
- If you pick this: the sweep is recorded as "not runnable" and the join test waits; you are asked again when that test is next.
- Upside: nothing changes now.
- Downside: the template cannot fix this workspace on its own because of the extra copy, so the question comes back unchanged.

#### What the debate found
- Two of three advocates chose option 1; the third preferred option 2 for speed.
- All three agreed the extra copy in `/home/coder/.local/bin` has to go at some point, and that the check must run in the coordinator's own session.
- The spec's recommended route (the template alone) would not work on this workspace without removing that copy.

#### Recommendation and confidence
Option 1. Confidence 70 percent.

#### If you do not answer
Option 3 applies: the sweep duty is recorded as "not runnable" and the join comparison (XC-04) waits.

#### What this answer does not authorize
Running the sweep more often than once per 5 minutes; any write by the sweep beyond its one report; a merge of PR #539; or changes to other workspaces beyond the normal template update.

#### How to answer
"Q29: option 1, and yes, remove the extra copy after the update" (or "Q29: option 2", or "Q29: option 3").

---
