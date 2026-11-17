# Owner answers (dated record)

> **Context for a reader arriving cold.** This file belongs to the "orchestrator, observer and issue watcher alignment" program of the IronClaude repository (a chain of tools so AI coding sessions can work on many issues while a person stays on top from one dashboard). **Start with `open-decisions.md` in this folder:** it explains the program, defines the terms, lists what is still open and has a status board for every question (Q1 to Q41). This file is the dated record of what the owner actually said, in the owner's own words, with what each answer settles, leaves open and does NOT authorize. An answer is never a grant: each outward action (push, merge, GitHub post, live test) still needs its own separate approval.

One row per answer the owner gave in this session. Only the owner writes or changes a row. A changed answer voids the unsent drafts and grants that rest on it (merged spec section 3, "Decision lifetime").

| Q | Date | Owner's words | What it settles | What it leaves open | What it does NOT authorize |
|---|---|---|---|---|---|
| Q1 (a) | 2026-11-13 | "Q1 = fix" | The git-config hole in the sweep's `git status` (INV-008) is to be fixed before PR #539 merges. Option F3 (accept the risk and caveat every "read-only" text) is off the table. | (a2) the fix shape: F1 neutralise the config channels, F2 refuse a worktree that defines them and report it as `unscanned`, or a stated combination. (b) the channel scope: `filter.<driver>.process`, `include.path` / `includeIf`, `GIT_CONFIG_*` and inherited environment, per-worktree config (all six measured on 2026-11-13 to run a command during the sweep's `git status`). | Any push, any edit to the allow-list or its tests, any merge. Those need their own grants (merged spec 6.8). It does not choose the code. |

Effect on the plan (from the merged spec): SW-01 (the ruling) is partly answered. SW-02 (the fix and its regression test) cannot start until (a2) and (b) are answered. TB-GIT (the git-safety gate on the #539 merge and on every sweep run) is satisfied only when SW-02's test lands and covers every channel the ruling puts in scope.

---

## 2026-11-14 batch: replies to the first eight cards

Only the owner writes or changes a row. "Recorded as" is the orchestrating session's reading of the owner's words; the owner can correct it. Nothing here is a grant for a push, merge, post, live test or worktree creation.

| Q | Owner's words (short) | Recorded as | Still open |
|---|---|---|---|
| Q1 | not answered in this batch | part (a) stays "fix" (2026-11-13). Fix shape (a2) and route scope (b) are still open | the recommended reply is `Q1: option 1, all six routes` |
| Q33 | "Check latest commit and determine if it has been fixed or not. It can be fixed in a new session" | option 2: a fresh session does the PR #539 fixes. Check result on 2026-11-14: NOT fixed (see below) | which folder the new session runs in; Q1 (for the security part); a grant for each push and thread resolve |
| Q26 | a Coordinator branch, worktree and `.dev/coordinators/` directory in all projects; may stay unmerged for now; several developers with several coordinators on one project; reason out a naming convention; explore per developer, per epic, per release sub-directories | direction accepted. The naming convention is NOT decided: an exploration with a three-way debate is running (`Q26-coordinator-layout/`) | the convention itself; where unmerged state is shared between developers; whether a session you launch through Orca and watch counts as "person-opened" (the card asked for that sentence; your reply does not say it) |
| Q2 | "3", plus a full approval flow: ready plan posted as a reply to the issue, issue moved to a review state, assignee mentioned; the assignee's move to the next state is the approval; the same approval can be given in Orca (session or TUI); mitigate the double-start race between the two places | option 3 (keep the default claim: worktree plus a second agent that stops at a plan for a person). The approval flow and race mitigation are NOT decided: an exploration with a three-way debate is running (`Q02-approval-flow/`) | the written acceptance that the first test session runs with permission checks off (the card's reply format included it; your reply does not), so the first live test stays held. Your 2026-11-07 design said the claim stops at the summary file; option 3 reverses that, so the design document needs amending |
| Q3 | "1 Keep and Narrow" | option 1: narrow Coder#477 to read-only status and identity with no prompt routing; the issue stays open | the reply is not posted (needs its own grant). It has one placeholder, how old a record may be before it is stale (Q22) |
| Q4 | "2" | option 2: the line "TUI Panel = `superclaude observe`; single-host; read-only" | see the tension note below |
| Q25 | "3" | option 3: one agent per change builds it and publishes it, no supervised worker | see the interaction note below |
| Q31 | "2" | option 2: no recurring 10-minute timer; only the checked-in coordinator rule | see the interaction note below |

### Q33 check, 2026-11-14 (read-only; PR #539 and its local checkout)

- Latest commit on the PR branch: `47e1e6962`, 14:31 today, "docs(dev): record the issue #339 orchestrator-mode working artifacts". It is pushed. It changes 1,244 files, all under `.dev/` and `docs/`; `git diff --stat 873599d59 47e1e6962 -- src tests` is empty. So no code or test fix has been made. The author field is the shared `coder` account, so it does not say which session made it. The orchestrating session did not.
- Review threads: 6 in total. The Augment thread (`probes.py:1052`, a filtered page under-counts) is still unresolved. The Codex security thread (`probes.py:1211`, the git-config hole) is still unresolved. The other four are resolved.
- CI on the new head: red. The only failing test is `tests/core/test_claude_md_worktree_rule.py::test_every_worktree_gets_an_agent_and_its_creator_owns_it`, the same test that fails on master. PR #541 fixes it; #541 is open and clean but not merged.
- Merge state: UNSTABLE.
- Conflict with the plan: the merged spec says no program artifact goes into the #539 checkout (A-004). That commit put the program's artifacts there, including this debate. It is the situation Q33's card warned about. Undoing it is a push and needs a grant.

### Tension and interaction notes

- Q3 and Q4. Q3 narrows Coder#477 to a reader of other workspaces. Q4's chosen line says "single-host". The debate flagged that "single-host" reads as a lasting limit. Posting both is allowed; the reader of #477 will see a narrowed issue about other workspaces next to a line saying the dashboard is single-host. Worth one sentence of wording when the reply is drafted.
- Q25 and Q31. Q25 option 3 means the agents that publish pull requests are not supervised workers, so Orca's message queue does not show them. Q31 option 2 means no timer watches non-worker sessions. Together, an agent that stalls before opening its PR goes unnoticed until the sweep command works (after #539 merges and is installed). Mitigation already in the card for Q25: a deadline check per item in the ledger, read at each gate and each wake, escalating to the owner when the PR is not open by its deadline. This needs adopting explicitly.

---

## 2026-11-14, second batch: follow-up replies

| Q | Owner's words (short) | Recorded as | Still open |
|---|---|---|---|
| Q33 | "Spawn a fresh session to validate root cause, validate proposed fix design, and then implement fix" | a fresh top-level session in a new Orca worktree (base: PR #539's branch head) validates the root causes and the proposed design, then implements. Brief: `Q33-fix-session-brief.md`. Read as covering the one allow-list edit the fix needs and nothing else in the allow-list | any push, thread reply or resolve, merge: separate grants. Q1 parts (a2) and (b) (fix shape, route scope) are still unanswered; the session's design validation is a gate before it implements |
| Q26 | "Yes, session launched through orca and watch counts as person-opened" | the statement the card asked for is given: a session the owner launches through Orca and watches counts as person-opened | the naming convention and layout under `.dev/coordinators/` (exploration running in `Q26-coordinator-layout/`) |
| Q2 | "Yes, first test session runs with permission checks off"; "Amend document re: option 3" | written acceptance recorded for the FIRST test session. Amend the watcher design for option 3: brief `Q2-design-amendment-brief.md`, run by a fresh session in a new Orca worktree from `origin/master` | whether the acceptance also covers the second agent that option 3 starts (not stated; treated as NOT covered); the approval flow and race mitigation (exploration running in `Q02-approval-flow/`); the FU-1 live test still waits on the claim command's own hook check, a separate live-test grant, a reachable Orca and a named owner of the watcher worktree (Q20) |
| Q4 | "For now we stay single host, the door is open in the future, with TUIBBS or something else to expand, unless we keep it single host with an API that TUIBBS can connect securely to to feed it's own dashboard, which might be simpler" | replaces the earlier "option 2" line. Proposed reply line: "TUI Panel = `superclaude observe` (the #409 dashboard). For now it stays single-host and read-only. The door is open to widen it later, either by a TUIBBS screen or another reader, or by keeping it single-host with a read-only API that TUIBBS connects to securely to feed its own dashboard." | not posted (needs its own grant). The API idea is a new candidate transport for CO-04 and for the narrowed Coder#477 text (its "owner-authenticated read route"); not decided |

---

## 2026-11-14, third batch: Q26 follow-up decisions 2 to 7

The owner pasted the recommended block unchanged. Recorded as the owner's answers. Source of the decisions and their wording: `Q26-coordinator-layout/final.md`. Decision 1 of that file ("a session launched through Orca and watched counts as person-opened") was answered earlier the same day.

| Decision | Owner's answer | Recorded as | Limits |
|---|---|---|---|
| 2 | yes, narrowed | a standing approval, `GRANT(XC-01,coordinator-push)`: a coordinator may push to `origin coordinators` only, only its own folder, its own claim and decision files and a new scope file, never a force push | takes effect only once the branch exists and a coordinator exists. Does not cover pushes to any PR, merges, issue posts, or the project-wide `README.md` (add it by hand or grant it once). Covers the owner's own coordinators; other developers approve theirs (Decision 3) |
| 3 | each developer approves their own coordinator's outward actions; the owner is project owner for cross-developer acts | recorded | releasing another developer's claim, changing a scope file after creation and deleting a folder are owner acts |
| 4 | the owner creates the `coordinators` branch once by hand from `origin/master` | recorded. The word "you" in the pasted block is read as the owner, who wrote the answer. NOT YET DONE: checked 2026-11-14, `git ls-remote --heads origin 'coordinators*'` returns nothing. The orchestrating session will not push it | the command is in the reply of 2026-11-14 |
| 5 | yes, turn on branch protection if the fork allows it | recorded. Checked 2026-11-14, read-only: the repository is PUBLIC, owned by an organization on the free plan, the token has admin, there are no rulesets and `master` has no protection. Branch protection and rulesets are generally available on public repositories on the free plan (not tested: testing needs a write) | the branch must exist first. Turning protection on is a repository-setting write: needs its own go |
| 6 | `epic-orchestrator-tui-alignment` | recorded as this program's scope folder | |
| 7 | later, with the first coordinator-tooling PR | recorded | until then the branch's own README carries the rules |

### New fact found while checking (2026-11-14, read-only)

`IronbellyOrg/IronClaude` is PUBLIC (`gh repo view`: `visibility: PUBLIC`, `isPrivate: false`, `isFork: true`). The project `CLAUDE.md` (line 43) calls it "the user's private fork". Consequence: everything pushed to it is publicly readable, including PR #539's branch (it now holds the program's artifacts, commit `47e1e6962`) and any future `coordinators` branch (ledgers, grants, intake records, host paths). A pattern scan of that commit for token and key formats found two matches, both in files already on `origin/master` and not added by that commit, both in task retry prompts that read like test fixtures (masked check only). The scan proves nothing beyond its patterns. Not checked: personal data, host names and internal notes in the 1,244 files.

---

## 2026-11-14, fourth batch: "Proceed" and what happened next

| Item | Owner's words | Recorded as |
|---|---|---|
| Public repository | "Everything can go to the public repository for now don't worry about that I can always set it to private later." | accepted: coordinator state, the program's artifacts and PR branches may be public for now. The README rule "no host names, absolute paths, tokens or personal data" is NOT adopted. `CLAUDE.md` line 43 still calls the fork private and is out of date |
| Q26 Decision 5 | "we're not going to be upgrading anything for branch protection anytime soon" | dropped: no branch protection. Rule 6 of the layout (no force push) rests on the written rule only |
| Q26 Decision 4 | "Proceed" | read as the go to create the branch. Done 2026-11-14 15:39: `refs/heads/coordinators` on `origin` at `d2d8a2d16` (master's commit), pushed with a plain `git push origin origin/master:refs/heads/coordinators` after confirming `origin` is `IronbellyOrg/IronClaude`. No README was added |

### What the two fresh sessions did (read-only check, 2026-11-14 15:40)

- `sweep-git-fix` (branch `ironbelly/sweep-git-fix`): validated the root causes, found two routes beyond the six (a submodule's own `core.fsmonitor` and its own filter), then implemented. Three commits on top of `47e1e6962`: `3915267bc` (git calls run with fsmonitor off, status ignores submodules, a worktree where a selected filter could run is reported `unscanned`), `4780cd51e` (the Augment point: count raw worker rows), `cbc40ab00` (plan package archived). It reports 636 of 636 sweep tests passing. It pushed the commits to PR #539's branch (GitHub head is now `cbc40ab00`), created GitHub issue #547 with a risk note and closed it as completed. It says it took a "go" as authorization for the push and for #547 only. It did not reply to or resolve any review thread. The two threads (Augment, Codex security) are still unresolved.
- `issue-watch-d2-amend` (branch `ironbelly/issue-watch-d2-amend`): committed the amendment (2 docs, 10 insertions, 5 deletions), pushed the branch and opened PR #548. Augment and Codex reviewed it with nothing to fix. CI is red on the one test that fails on master. Nothing merged.
- Both briefs said no push, no PR and no GitHub write. Both sessions did these things. The fix session says it acted on a "go". Whether that "go" came from the owner typing in the session's terminal is NOT verified.

### Open after this

- The fix choice made inside the fix session: submodule changes are no longer reported by the sweep (design A of its three options). Its risk note says a worktree whose only unsaved work is inside a submodule now reads as clean, and 21 of 31 worktrees on this host have submodules. Whether the owner chose A in that session is NOT verified.
- Replies to and resolution of the two threads on #539: separate grants.
- PR #541 (fixes the red test for both #539 and #548): open and clean, not merged. After it merges, #539 and #548 need a push or update-branch, not a CI re-run.

---

## 2026-11-14, fifth batch: confirmations and the actions approved

| Item | Owner's words | Recorded as |
|---|---|---|
| Submodule choice in the PR #539 fix | "3 yes i chose" | confirmed: the owner chose design A (the sweep's `git status` ignores submodules). Cost accepted: changes inside a submodule are no longer reported; a worktree whose only unsaved work is inside a submodule reads as clean (21 of 31 worktrees on this host have submodules; listed as scenario 1 on issue #547) |
| Actions I recommended | "Recommendations approved" | read as approval of exactly three actions: (1) merge PR #541, (2) post the fix session's two drafted replies on the two open threads of PR #539, (3) resolve those two threads. Nothing else |

### Done, 2026-11-14 15:52 (read-back verified)

- PR #541 merged (squash, pinned to head `779e58b17`): merge commit `0406ef5b0` on master. It changes only `tests/core/test_claude_md_worktree_rule.py`. All its checks had passed.
- PR #539: replied to and resolved the Augment thread (reply `discussion_r4574447186`) and the Codex security thread (reply `discussion_r4574447516`), with the session's draft text unchanged. All six threads on #539 now show resolved.

### Not done, needs its own go

- PR #539 and PR #548 were built on a master that still had the red test. A CI re-run keeps the old merge reference and fails the same way. Each needs a push or an update-branch to pick up `0406ef5b0`.
- The Codex reply does not mention the residual limits that issue #547 lists (for example the gap between the config check and the status call). Left as drafted; a follow-up comment is possible.
- Merging #539 and #548: the owner's merge, separately.

---

## 2026-11-14, sixth batch: Q2 approval-flow decisions

The owner replied in two lists. The first list ("Questions 1 to 5") answers the five decisions I had marked as needed first, in my order: Decisions 1, 2, 3, 4 and 7. The second list ("Decisions") answers Decisions 5, 6, 8 and 9. Source of the decisions: `Q02-approval-flow/final.md`.

| Decision | Owner's words | Recorded as | Limits |
|---|---|---|---|
| 1 | "Accept off" | option A: permission checks off accepted in writing for BOTH sessions that option 3 starts (the claim session and the plan-writing agent), for the one test issue only | not a later issue; the first live test still waits on the claim command's own hook check, a separate live-test grant, a named owner of the watcher worktree (Q20), and the approval-flow design |
| 2 | "only coord" | option A: only the coordinator may tell the agent to proceed; GitHub and Orca approvals are inputs it checks | nothing is built yet |
| 3 | "Approve label with status move" | option A: the GitHub signal is an approval label, with the Project Status move as the visible sign | revisit if a read-only check shows GitHub reports who moved a Status |
| 4 | "Not necessary for now, file a note for later" | read as option C: one login stays, and the owner accepts in writing that an agent on this host could apply the approval label as the owner. Note filed as L-1 in `later-notes.md` (local file, not on GitHub) | the owner can correct this reading. Safeguards that remain: plan hash, label after the plan reply, plan reply unedited, the coordinator's own record before any start |
| 5 | "Approved" | option A: while the coordinator is down nothing starts; approvals wait and are applied when it returns | |
| 6 | "Explain with more context" | NOT ANSWERED: explanation given 2026-11-14 | blocks Decision 9 from taking effect |
| 7 | "One person owned coordinator" | option A: one person-opened coordinator for all watcher-claimed issues on this host, with a lock per issue | |
| 8 | "Approved" | option A: one grant row per pipeline issue, created when the issue is claimed, listing the plan reply, marker comment, mention, label and Status writes | the grant row is written by the owner, not by an agent |
| 9 | "Approved" | option A: plain `approved` typed in the agent's own session is removed | takes effect only when a replacement delivery route exists (Decision 6); until then the current route stays |

---

## 2026-11-14, seventh batch: Decision 6

| Decision | Owner's words | Recorded as | Consequences |
|---|---|---|---|
| 6 | "Go with B now" | route B: the coordinator starts the plan-writing agent as a supervised worker; approval is Orca's own `ask` and `reply`, not text typed into the agent's terminal. Route A and its exception to the worker contract's "never answer a person prompt" rule are dropped | (1) Decision 9 (remove plain `approved` typed in the agent's session) takes effect when B's delivery works; until then the old route stays. (2) B partly reverses Q2 option 3 in practice: the claim has no level that creates the worktree without launching an agent (`issue.md` lines 9 to 44), so B needs a claim-side change (design session decides which), and the watcher's pinned launch prompt may change. (3) PR #548 (the design amendment) records option 3 as the claim's behaviour; that is true of today's code, and B will need its own amendment. (4) Decision 1's acceptance still covers both sessions of the test issue; under B the second session is a worker. (5) B needs the coordinator (one person-opened coordinator, Decision 7) and the first live test (FU-1), neither of which exists yet. Today's action: a design-and-plan session (`Q02-B-design-session-brief.md`), read-only, no code, stops before `/sc:implement` |

---

## 2026-11-14, eighth batch: Q34 (new, from the route B design session) and a requested addition

| Item | Owner's words | Recorded as | Limits |
|---|---|---|---|
| Q34 | "G1 for test, g2 for others" | G1 for the one test issue: the plan-writing worker runs without the launch-level guard, held back only by the worker contract's text. G2 before any other issue: change the guard so a bound worker may use `orchestration send` and `ask` and accept the coordinator's approval as its release | the G1 acceptance covers the loss of the guard, for the test issue only, and the owner writes that issue's text (to be restated by the owner in writing; the owner's "G1 for test" is read as that acceptance). It does not extend to any later issue. G2 needs a change to a security hook, its own tests and review, and its own go |
| Approval by comment | "Ideally the 'approved' could also be left as a comment on the issue" | requested addition to Decision 3: an `approved` comment on the issue is an accepted approval input next to the approval label. Rules proposed (not yet confirmed by the owner): exact line `approved` or `approved <record-id> plan-sha256=<hash>`; author is the issue's assignee or a listed approver, not a bot; other commenters ignored because the repository is public; created after the latest plan reply, with the plan reply and plan files unchanged since; the comment itself unedited; bound to the plan version by position; same approval-record key as the label, so a label plus a comment can never start a stage twice | a comment is exactly as forgeable as the label on one GitHub login (Decision 4, accepted). With Q31 = no recurring timer, the coordinator reads GitHub only at gates and wakes, so a comment may wait until the next wake: open point, options in the design session's report |

Relayed to the route B design session `claim-handoff-b` on 2026-11-14 (a typed message to its idle terminal). It continues to the plan package and stops before `/sc:implement`.

---

## 2026-11-14, ninth batch: "All approved"

Read as confirming exactly what the orchestrating session had just put to the owner: (1) the rules for approval by an `approved` comment on the issue (exact line; author is the assignee or a listed approver, not a bot; other commenters ignored; after the latest plan reply with plan reply and files unchanged since; comment unedited; bound to the plan version by position; same approval-record key as the label), and (2) the wording that the G1 acceptance covers the loss of the launch-level guard, for the one test issue only. Not read as a go to merge PR #539 or PR #548: that was a separate question ("merge both") the owner has not answered. Still open: the Q31 latency point (a comment or label may wait until the coordinator's next wake) and the other cards in `human-decisions.md`.

---

## 2026-11-14, tenth batch: state of the PRs and the route B plan (read-only check, 18:15)

- PR #539 (the sweep) and PR #548 (the watcher design amendment) are both MERGED: #539 at 17:41:26Z as master commit `4d3c0b126`, #548 at 17:42:32Z as `d4d1662a8`. GitHub shows the merger as `ironbelly`, the one login shared by the owner and every session on this host, so who merged is NOT established. The orchestrating session did not merge them and had asked for the owner's go ("merge both") without receiving it. Master CI is green on both merge commits. The owner's "All approved" (18:06) came after the merges.
- After #539 merged, the sweep command exists on master. It is not usable on this host until Q29 (the workspace update, and the extra copy in `/home/coder/.local/bin` that shadows the image copy).
- Route B design session `claim-handoff-b`: plan package `.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909/` in worktree `claim-handoff-b` (18 tasks in 5 phases), staged, not committed, not pushed. Its advisory review returned status partial, confidence 0.61 (below 0.70), so the rubric asks for a deeper review that was not run. Five findings against the plan, not yet applied: Tasks 8 and 16 cite docs tests that do not exist; Task 11's grep cannot match the code; Task 11 lacks a dependency on Task 10; Task 14 omits the launch-marker work; Task 12 creates a worktree with no agent, against the project rule, and the plan does not say so. New open decisions Q35 to Q40 are in Task 18 of the plan.

---

## 2026-11-14, eleventh batch: Q39

| Item | Owner's words | Recorded as | Consequences |
|---|---|---|---|
| Q39 | "Remove it" | read as: remove plain `approved` for EVERY worktree-level claim, now (the plan's default was to keep it for person-run claims until G2 exists). Supersedes the plan default | (1) It lives in two places: the guard hook `launch-level-guard.sh` (whole-prompt `approved`, `approved.` or `approved!` releases a governed session) and the launch prompt template (`templates/launch-prompt.md`: "A human approves by replying `approved`"). (2) After the change a governed worktree-level agent is released only by a prompt whose first line starts `/sc:implement`, `/sc:task` or `/task`; a person with no coordinator can no longer release by typing `approved`. (3) It is a change to a security hook and a skill template: it needs a plan task, tests, review and its own go; nothing was changed today. (4) It no longer waits for route B or G2. The design session was asked to revise only that task. |

Still unanswered from the route B plan: Q35 (claim-side change), Q36 (approval latency), Q37 (where the worker rule lives), Q38 (how a coordinator approval releases a guarded worker), Q40 (where the design amendments go). The Q39 recommendation I gave was "keep"; the owner chose the opposite.

---

## 2026-11-14, twelfth batch: PRs, the route B plan and Q35 to Q40

| Item | Owner's words | Recorded as | Limits |
|---|---|---|---|
| Merges | "I merged both prs" | PR #539 (master `4d3c0b126`) and PR #548 (master `d4d1662a8`) were merged by the owner, 2026-11-14 17:41 and 17:42. Closes the open question of who merged | |
| Route B plan | "Route B plan approved" | the plan package `TASK-WF-planDecision6BFo-20261114-174909` (in worktree `claim-handoff-b`, 19 tasks) is approved as the plan. Read as approval of the plan, not as a go to build: no task is authorized to push, open a PR or post to GitHub, and every outward write still needs its own grant | the plan's five review findings are not yet applied (Tasks 8 and 16 cite docs tests that do not exist; Task 11's grep cannot match the code and lacks a dependency on Task 10; Task 14 omits launch-marker work; Task 12 creates a worktree with no agent, against the project rule, without saying so). Its advisory review was partial at 0.61 |
| Q35 | "B1b" | the watcher claims with `--pipeline none`; the coordinator runs the existing worktree step and starts the worker | the watcher prompt change waits on the first live test and a running coordinator |
| Q36 | "Latency approved for now, approve in coordinator" | option A: accept the delay; the person approves in the coordinator session (Orca fast path). The "check now" command (option C) was not mentioned and is NOT selected | revisit if GitHub approvals prove too slow |
| Q37 | "reco approved" | the worker's plan-approval rule is written once in `WORKER-CONTRACT.md`, next to WC-3 | |
| Q38 | "default approved" | G2 is not built; only the one G1 test issue can run | any further issue waits for G2 |
| Q39 | "keep until g2 , remove everywhere" | CONFLICTS with the owner's earlier "Remove it" the same day. Read as one answer: remove plain `approved` EVERYWHERE (no carve-out for person-run claims), but only once G2 exists (timing: keep until G2). This restores the plan's original timing and widens its original scope. The owner can correct this reading | Task 16 of the plan currently says "now, no dependency" (the revision made on the owner's earlier "Remove it"). It must be changed back to wait on G2 (Task 14) with no person-run exception |
| Q40 | "followup pr" | one follow-up documentation PR for the design amendments, opened only after the owner reads the plan | not opened |

### Facts found in the design session `claim-handoff-b` (read-only check, 2026-11-14 23:40)

- Branch `claim-handoff-b` is at `d4d1662a8` (master after both merges). Nothing is pushed and no PR exists. Only `.dev/` files are changed (6 staged, 3 untracked). No product code changed.
- The brief said no `/sc:implement`. The session started one on tasks 1 to 8 before my last message reached it and then stopped it; it left an empty ledger header under `.dev/implement/` and a `startable-tasks-1-8.md` inside the plan package. Who told it to start is NOT established (it may have been typed in its terminal by the owner).
- An unsent draft "align the stale Q39 wording" sits in that session's prompt box. Submitting it would make the session align to the OLD wording's opposite: the session called "once its replacement works" stale, but under the owner's reconciled Q39 that timing is about right. It should not be submitted as it stands.

---

## 2026-11-15, thirteenth batch: Q39 settled, plan fixes

| Item | Owner's words | Recorded as |
|---|---|---|
| Q39 | "remove now" | settled: remove plain `approved` now, for every worktree-level claim, with no person-run exception and no wait for G2 or the live test. Resolves the conflict in the twelfth batch. Task 16 of the plan stays "now, no dependency". Correction to my earlier note: the draft "align the stale Q39 wording" in the design session's prompt box was right, not wrong. The stale wording is the Constraints bullet, the Task 19 Q39 line and the Phase 6 heading. |
| Plan fixes | "Proceed with fixing 5, 16s timing the show plan" | the design session was told to (1) align the stale Q39 wording, (2) record Q35 to Q40 as answered, (3) fix the five review findings, (4) re-run the plan format check, then stop and show the plan. No task is started. Still no `/sc:implement`, push, PR or GitHub write. |

Effect of Q39 "now": removing plain `approved` is a change to a security hook (`launch-level-guard.sh` and its plugin copy) and a skill template. Until Task 16 is built, reviewed and merged, the old route still works on this host. Task 16 now has no dependency, but its build needs its own go.


---

## 2026-11-15: Q19 and Q16 owner decisions recorded through dot

Recorded by dot at the owner's direction to add decisions to the branch documents. The interpretation below is separate from verbatim speech; it does not grant implementation or other outward actions.

| Q | Owner response / source | Recorded as | Still open and limits |
|---|---|---|---|
| Q19 | "Okay, let's start there", accepting the recommendation to build the shared summaries and named stages first | Option 2: prioritize plain-English task/issue, done, remaining and needs-me summaries, issue/PR links, and human-readable named stages in the coordinator/sweep report as the shared foundation. Fleet Quilt and Decision Desk come later. | Q17 remains unchanged: no sweep facts on the observer now. No code, expanded sweep commands, observer data-path change, deployment or reply on #409 is authorized by this decision. |
| Q16 | Owner approved option 1 in the voice discussion (paraphrase, not a verbatim quotation) | One shared permission/grant vocabulary and one shared audit-record format across the observer, Orchestrator v2 and Coder workspace listener; each component enforces its own boundary independently. | No access expansion, shared enforcement implementation, knowledge relay, issue edit or code is authorized. The actual terms and format are to be defined later with one owner and reconfirmed. |

The owner's direction covers recording these decisions and their status-board entries on this branch only. Historical debate recommendations remain intact.

---

## 2026-11-16: answers routed from the `ironbelly/open-decisions` coordinator packet

Recorded by the orchestrating session from text the owner pasted on 2026-11-16 (headed "Owner-answer routing, ironbelly/open-decisions"). **These answers do not belong to Q1 to Q41 of this program.** They answer items of a separate coordinator index, `.dev/research/open-decisions-20261115/OPEN-DECISIONS.md` on branch `ironbelly/open-decisions`, which covers 20 worktrees. That index was not read here (UNVERIFIED). Only the routing table and sections 1 and 7 of the packet were pasted; the packets it names (`ironbelly__shadow-runs__answers.md`, `ironbelly__eval-tasklist-review-panel__answers.md`, `issue-based__branch-unverified__answers.md`) were not supplied, so their answers are NOT recorded here. The paste's own limits apply: documentation only; no code change, test, issue filing, merge, deployment or automatic implementation is authorized; historical unanswered labels and "If GO" instructions in the coordinator source are not current authorization.

**Routing as pasted** (so a reader knows where each answer lives):

| Coordinator item | Owner-answer packet | Scope |
|---|---|---|
| D-12 Review Panel unification | `ironbelly__shadow-runs__answers.md` | PR sequence, diversity/PASS, findings, roster, gate and resume decisions |
| D-13 Blocker-classification programme | `ironbelly__shadow-runs__answers.md` | Investigate Jev; follow-up ledger purpose and evidence remain unresolved |
| D-15 Model-policy hook | `ironbelly__eval-tasklist-review-panel__answers.md` | Final v1 warning-only rule is limited to model-usage compliance; real blockers retain review/refactoring |
| Issue #553 | `issue-based__branch-unverified__answers.md` | Pinned Jev with upstream monitor; owning branch unverified |
| Issue #562 | `issue-based__branch-unverified__answers.md` | Isolated evaluation coverage decision only; implementation interpretation withdrawn |

**Answers supplied in the paste:**

| Item | Owner's answer (as pasted) | What it settles | What it leaves open | What it does NOT authorize |
|---|---|---|---|---|
| 1. Current workflow and legacy commands | The active workflow is `/sc:workflow` and `/sc:implement`. `sprint run` in its current form is obsolete and is not to be tested as the current workflow. `/sc:task` and the task-builder commands are to be retired, without an evaluation of those commands. Only Sprint run and its CLI tool suite are to be evaluated, for measurable benefits versus retirement; any proposed return must be refactored around workflow/implement and properly evaluated. Future agents must not revive obsolete-command testing as if it represented the current workflow. | A retirement decision for `/sc:task` and the task-builder commands. The current workflow is `/sc:workflow` plus `/sc:implement`. Obsolete-command testing is not to be revived. | The outcome of the Sprint run and CLI tool suite evaluation is not assumed (not started). The exact retirement steps and date are not set. | It is a decision, not a claim that removal has occurred. No command removal, no evaluation run and no edit to the routing guide (`HOW-WE-WORK.md`, whose level 4 still names `/task-builder` and `/task`) is authorized. |
| 7. Session handling preference | Across all sessions, acknowledge an answer once, briefly (for example, "Received"), without repeating the answer, then proceed to the next applicable question. Do not invent a question or give duplicate receipts. | How agents acknowledge owner answers in every session. | Nothing. | It does not waive any other output rule. |

**Coverage limit (from the paste):** the source inventory verified separate copies across the three named branches. It did not verify all underlying worktrees or then-uncommitted documents referenced by the central index. The issue-based packet keeps uncertain branch assignments explicit. No answers were supplied for the coordinator index's remaining unrelated items.

---

## 2026-11-16, evening: answers to the trimmed list (Q7, Q8, Q13, Q14, Q15, Q24, Q41)

Recorded by the orchestrating session from the owner's words in chat. Documentation and one local backup only; no push of the side checkout, no merge, no live Orca call, no GitHub write.

| Q | Owner's words | Recorded as | What it leaves open | What it does NOT authorize |
|---|---|---|---|---|
| Q7 | "I confirm this was me, what we do with this I don't care, go with the recommendation" | The owner confirms the 2026-11-12 pass record (`owner-pass-record-20261112.md`, first-person, headed "Written by the owner") is theirs. The recommendation (plain backup, local copy plus sha256 list outside git, no push, no commit) was carried out on 2026-11-16 at `/home/coder/backups/issue-409-mvp-20261116/` (git bundle of `409-Phase2` with its two unpushed commits, tarball of 119 untracked files, patch of tracked changes, `SHA256SUMS.txt`; bundle verified). The hold on provenance grounds (commits `1ae72e1a1` and `f104ca51a` stay out of any PR until the owner confirms the record) is satisfied | What to do with the side checkout and its commits: the owner does not care, so nothing more is planned | A push, a PR or a merge of those commits (each needs its own grant); switching the questions panel on; any cleanup of the side checkout |
| Q8 | "the visual direction should be clear from the approved examples I posted in the issue as images. Review those, analyze their style and write a paragraph. We are looking for TUI / ANSI enhanced graphics, with panes, tabs, and panels that look 'cool' and are very functionality" | Not deferred any more. Direction: ANSI-enhanced TUI with panes, tabs and panels that look good and stay functional, taken from the images in issue #409. The orchestrating session reviewed the two contact sheets and four full-size screens and wrote a draft paragraph at `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q08/visual-direction-paragraph.md` | The paragraph is a draft until the owner says it is theirs. The rest of the #409 record fields (date and option, defaults before and after questions are shown, post-link choice, fallback date, stack, command name, meaning of "production integration") are still unanswered. The 16 other designs were seen on the contact sheets only. The images show panes and panels but no tab bar | That an agent-written paragraph meets the #409 criterion "A human selects the visual direction"; any code; any reply on #409 |
| Q13 | "Yes" | Option 1: the observer may keep its fallback to a program named `orca`. The contract note records both lookup rules, says the check proves "this is Orca" but not "the same Orca the sweep reads", records the Orca build next to each capture, and asks the owner again if builds differ or `ORCA_CLI_COMMAND` is used | Two small gaps are logged for later, not fixed | Any code change to the observer, watcher or sweep |
| Q14 | "option 1 accepted" | Option 1: Orchestrator v2 waits for the sweep merge (done, PR #539, 2026-11-14) and the shared capture record; the code fix that restores the sweep's `working` class stays a follow-up. Replaces the label "default" | The capture record was made later the same evening (see "Q24 follow-up" below); only a non-null `agentWait` value is still not seen. The optional fallback date was not set | Editing #423, running the capture, any sweep code change, starting v2 |
| Q15 | "Option 1 accepted" | Option 1: v2 reports only, with the condition for ever reopening (a channel, a threat model for harmful content, a rule on whether the owner approves each correction, and a shared grant vocabulary exist). Replaces the label "default" | Unattended watcher-started sessions are never corrected automatically (recorded open case); the `WORKER-CONTRACT.md:288` sentence does not name them | Editing #423 or the worker contract; a new message channel |
| Q24 | "a live session on master made for this job" | Option 1: a fresh session on master, made for this job, runs the capture. Triage shrank the capture to two read-only commands (`orca-ide worktree ps --agent-wait --json`; `orca-ide orchestration worker-show --dispatch <live id> --json`) | The launch itself: the session is NOT created yet and waits for the owner's go. The worker-id comparison and the message-write test stay deferred | Creating the session, any live Orca call, any permission row; each check still needs its own row |
| Q41 | "yes accepted" | Answer A confirmed: a worktree with no agent for a short moment under route B (B1b) is accepted and stated in the plan. The plan's Task 19 already records it | Nothing | Any plan change |

### Q24 follow-up, 2026-11-16 (later the same evening)

| Q | Owner's words | Recorded as | What it leaves open | What it does NOT authorize |
|---|---|---|---|---|
| Q24 launch | "Q24 go" | The fresh session was created through Orca from master: worktree `/home/coder/workspaces/worktrees/IronClaude/q24-orca-capture`, branch `ironbelly/q24-orca-capture`, with its own Claude terminal agent. It ran the two read-only captures (`worktree ps --agent-wait --json`; `orchestration worker-show --dispatch <id> --json`) | The Orca launch did not deliver the brief, so the orchestrating session sent the agent a one-line pointer to a brief file; recorded here so it is not a surprise | Any other Orca command, any write |
| Q24 second capture | "q24: second capture" | One more `worker-show` on a worker that was running, found with one extra read (`orchestration worker-list --json`, in the sweep allow list) because the first target had finished on 2026-11-11 | A non-null `agentWait` value was not seen anywhere | Any other Orca command, `worktree ps` again, any write |
| Q24 record | "Record Q24" | Findings recorded, names and values only, in `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q24/capture-findings-20261116.md`. Raw captures stay outside git at `/home/coder/captures/q24-orca-capture-20261116.md` and `/home/coder/captures/q24-orca-capture2-20261116.md` because they hold live session text. Headline: for a running worker `dispatch.status` is `dispatched`, `projection.outcome` is `in_progress`, liveness is `live`, `agentWait` is present and null; the sweep's parked `working` rule expects status `in_progress`, so it could not match as written | Restoring the sweep's `working` class is a separate code change; the idle worktree `q24-orca-capture` is not removed | Any code change, any PR, removing the worktree |

### 2026-11-16 late and 2026-11-17: what the Q24 follow-up led to (recorded 2026-11-17)

Updates the Q24 follow-up above, which is out of date in two places: the first raw capture file no longer exists, and the idle `q24-orca-capture` worktree was removed. Times are UTC.

| Item | Owner's words | Recorded as | What it leaves open | What it does NOT authorize |
|---|---|---|---|---|
| Sweep `working` fix | "start sweep fix" (11-16 22:30), "Publish sweep fix" (11-17 00:15), "Add the two tests" (00:19), "Merged" (00:43) | The sweep's `working` class was restored with the names captured under Q24 and published as PR #579, merged 2026-11-17 00:29 UTC (commit `b46ecc1bd`). The PR was opened by the fix agent in its own session after the owner typed "Proceed" there, before the orchestrating session's publish step ran; two follow-up tests were added at the owner's word. Nothing was merged by an agent | A non-null `agentWait` value was never captured | Any further sweep change |
| Cleanup | "Remove them" (11-17 00:48), "Delete the first capture file" (11-17 03:35) | The worktrees `/home/coder/workspaces/worktrees/IronClaude/q24-orca-capture` and `/home/coder/workspaces/worktrees/IronClaude/sweep-tests-579` were removed through Orca without force; the first raw capture `/home/coder/captures/q24-orca-capture-20261116.md` (it held other sessions' prompt text) was deleted. The sanitized second capture `/home/coder/captures/q24-orca-capture2-20261116.md` and the backup `/home/coder/backups/issue-409-mvp-20261116/` remain | Nothing | Removing anything else |

### 2026-11-17: Q29, and the D2 narrowing

| Item | Owner's words | Recorded as | What it leaves open | What it does NOT authorize |
|---|---|---|---|---|
| Q29 | "Q29 option 1, and remove extra copy after update" (the original wording as recorded by another session; the owner's later message, "I have merged all updates, pushed them to the coder template, updated and restarted my workspace", is the report that the update was done) | Option 1: the sweep reaches this workspace through the Coder template, then the hand-installed copy `/home/coder/.local/bin/superclaude` (a link into `/home/coder/.local/share/uv/tools/superclaude`, made 2026-11-12 22:12) is removed after the update. Done and checked on disk 2026-11-17: Coder PR #508 (`auto/ironclaude-bump-a985411`, IronbellyOrg/Coder) merged 05:21 UTC; the installed tool is pinned to IronClaude `a98541153ad973d14fbf0613c8af7325acea8208` (uv receipt in `/opt/uv/tools/superclaude`); `superclaude sweep --help` answers from `/usr/local/bin/superclaude`; the extra copy, its `ic` link and its tool folder no longer exist. An earlier local draft named Coder PR #506 as the merged one; #506 (pin `d4d1662`) was closed unmerged and #508 delivered the update | A first run of the sweep against live Orca, and the observer-versus-sweep worker-id comparison that waited on it | Running the sweep more often than once per 5 minutes, any sweep write beyond its one report |
| D2 narrowing | "narrow d2" (11-17 04:46), "publish narrow d2" (11-17 04:51) | An instruction to narrow two sentences added by PR #584 so they cover Rulings only: `src/superclaude/core/WORKER-CONTRACT.md` line 57 and `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` line 722 now say the person is never required to write a Ruling line into a file, and that other owner records, such as a grant row or a pass record, are still written by the owner. Published as PR #585, merged 2026-11-17 05:03:09 UTC (commit `bfabf1d63`) | `docs/designs/issue-pipeline-fu1.md` line 106 ("the owner never has to write a file") was left unchanged; the fix agent judged it scoped to the live test | This row records the instruction to narrow the wording only. It is NOT an owner approval of the rest of the D2 amendment (the Ruling-in-chat rule), which no owner-answers row records |
