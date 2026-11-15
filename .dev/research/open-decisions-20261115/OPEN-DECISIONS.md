# Open decisions and questions, all IronClaude worktrees

Written 2026-11-15 by the coordinator (ORCH-IronClaude). Scope: the 20 IronClaude worktrees found on 2026-11-15, the open issues I track, and the open items from this session. The Coder repo's own worktrees were not swept.

## How to use this file

1. Write your answer on the **Owner answer:** line of an item. Plain words are fine ("yes", "option 2", "no, because ...").
2. Add the word `GO` at the end of your answer if you want me to start the "If GO" step listed under that item. Without `GO` I only record your answer and reply. I never merge, and I never act on an item that has no "If GO" line.
3. I watch this file for 2 hours and reply on the **Coordinator reply:** line of the item you changed. Each reply is committed and pushed to this same branch, so the remote copy matches. After the watch ends I stop; the file stays.
4. If you edit on GitHub, I fetch before I reply. If two edits collide I keep yours and reply under it.
5. Status words: OPEN (waiting for you), ANSWERED (you answered, nothing else to do), IN PROGRESS (a worker is running), DONE.

Evidence notes: facts come from the worktree scans I ran on 2026-11-15 and from this session. Anything I could not check is marked UNVERIFIED. File and line references come from the scans and were not all re-read by me. Numbers from workers (for example evaluation results) are theirs, not mine.

**Watch window:** (filled in when the watch starts)

---

## Part A. Worktree cleanup and uncommitted work

Done today, on your order to delete merged worktrees after validating that nothing of consequence was unpushed:

- Deleted 11 worktrees: `install-core-stale-warning`, `issue-394-launch-level-hook`, `issue-441`, `issue-443`, `issue-488-tiers`, `issue-504`, `issue-512`, `tier3-effort`, `codegraph-wording`, `mcp-audit`, `smoke-504`.
- Check used: the worktree's last commit equals the last commit of its merged pull request (or, for `mcp-audit` and `smoke-504`, is already inside `origin/master`), and nothing under `.dev/tasks`, `src`, `tests`, `docs` or any other non-`.dev` path was untracked or modified. Untracked files under `.dev/` (claim packages, reflect, troubleshoot and brainstorm output, audit notes) were not kept, as you ordered. Orca needed `--force` for seven of them because of those untracked files.
- Two idle Claude sessions that sat in `issue-488-tiers` and `codegraph-wording` were stopped by the removal.
- The local branch `ironbelly/issue-394-launch-level-hook` was kept by Orca (it could not prove the branch merged, because the PR was squash-merged). See D-04.
- Kept because they failed the check: `issue-409-mvp` (D-01) and `issue-339-orchestrator-mode` (D-02).

### D-01 Two commits exist only on this computer (observer, branch `409-Phase2`)
**Where:** worktree `issue-409-mvp` (Orca display name `issue-409-TUIDash-P2`).
**Question:** Commits `1ae72e1a1` ("enable the live coordinator-questions read against the owner's record") and `f104ca51a` ("cite the owner-written pass record ... archive the release 2 plan") are not on GitHub. They change `src/superclaude/cli/observe/commands.py` and tests. Push them and open a pull request?
**Why it matters:** the first commit switches the live read of coordinator questions on (`QUESTION_GATE_PASSED`). The orchestrator-TUI notes (D-51, Q6 and Q30) say it should stay off until a seeded live test with a throwaway coordinator has run. A scan says that test appears not done (UNVERIFIED). Another scan reported the branch as 5 commits ahead; my own check counted 2 not on the remote.
**My recommendation:** push and open the PR so the work is not only local, and do not merge it until the seeded live test (Q30 option 1) has passed.
**If GO:** I push `409-Phase2` and run `/sc:pr-submit --monitor 3` for it (fork only, never merge).
**Owner answer:**
**Coordinator reply:**

### D-02 Your decision records in the 339 worktree are uncommitted
**Where:** worktree `issue-339-orchestrator-mode` (the sweep PR #539 is merged). Four tracked files are modified and `open-decisions.md` is untracked, all under `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/`.
**Question:** Commit them on a new docs branch and open a PR (this is Q7 in that file), or leave them as they are?
**Why it matters:** these are your answers (`owner-answers.md`, `accepted-answers.md`, `human-decisions.md`) and the question list (`open-decisions.md`, see D-51). They exist only in this one folder.
**My recommendation:** commit them (the file's own recommendation for Q7 is option 1, 65%).
**If GO:** I start a worker that commits those files on a new branch from `origin/master` and opens a docs PR through `/sc:pr-submit --monitor 3`.
**Owner answer:**
**Coordinator reply:**

### D-03 Uncommitted work in five other worktrees
**Question:** For each worktree, commit and push, open a PR, keep as is, or discard? I have not read the modified files themselves.

| Worktree (branch) | State on 2026-11-15 | Pull request |
|---|---|---|
| `eval-tasklist-review-panel` (`ironbelly/eval-tasklist-review-panel`) | 16 ahead, 14 behind master; 68 modified, 3,570 untracked; last commit today; has a remote branch | none |
| `brainstorm-reflect-panel` (`ironbelly/shadow-runs`) | 5 ahead, 3 behind; 181 modified, 9 untracked; last commit 2026-11-14 | none |
| `claim-handoff-b` (`ironbelly/claim-handoff-b`) | level with master; 7 modified, 3 untracked; no remote branch | none |
| `issue-442-runbook` (`ironbelly/issue-442-runbook`) | 40 behind master; 49 modified, 5 untracked; no remote branch | none |
| `issue-463` (`ironbelly/issue-463`) | 30 behind; 44 modified, 7 untracked; no remote branch | none |

**My recommendation:** first let me start one read-only worker per worktree that summarizes what the modified files are and proposes commit, discard or keep. Then you decide with facts.
**If GO:** I start those read-only workers (nothing is changed).
**Owner answer:**
**Coordinator reply:**

### D-04 Leftover local branch
**Question:** Delete the local branch `ironbelly/issue-394-launch-level-hook`? Its PR #432 merged on 2026-11-08 and its worktree is gone.
**My recommendation:** yes, delete it.
**If GO:** I delete that one local branch only.
**Owner answer:**
**Coordinator reply:**

---

## Part B. Review panel program

### D-10 Evaluation of the tasklist review panel (worktree `eval-tasklist-review-panel`)
**Source:** `.dev/eval-workspaces/tasklist-review-panel/OPEN-DECISIONS-20261115.md` and `OPEN-QUESTIONS-20261115.md`, and `20261114-sweep-sheet/OPEN-ITEMS.md` in that worktree. The document's own advice is to ask you one question at a time with a recommendation.
**Open questions:**
- **a. Hold-out answers:** who writes and attests the ground truth for the hold-out documents, and which documents are the hold-out set? No list exists, and your "use sessions" order does not cover the author.
- **b. Strictness:** may the format checks forgive small slips? Does the recipe-ledger compliance gate stay at 10% if the second attempt also fails? Is a model's review of a recipe acceptable instead of a person's? Who runs the three tests only a maintainer can run?
- **c. Severity change:** apply the narrowed "contradiction is blocking" rule now, after the experiments, or never? A second, separate decision covers the "unpassable check" rule.
- **d. Mismatched models:** how to treat a run whose served model differs from its label (drop it, or only flag it)? Run the 96-run model ablation, or accept "not run"? What rule applies if a control report contains a `## Ledger` heading?
- **e. Housekeeping:** what order to commit, freeze and push in? Delete three stray scripts in `20261111-a1/tools/tmp-scripts/`? Was the old 1.83 baseline inflated (UNVERIFIED; the folder is gone; a rebuild with 6 plain-panel rows was offered)?
**My recommendation:** answer a to e in that file's own order, a first, because the hold-out set gates every later claim.
**If GO:** none; this needs your answers first.
**Owner answer:**
**Coordinator reply:**

### D-11 Adopt the evaluation's reviewer combinations as the panel defaults?
**Source:** `COMBO-REPORT.md` in the same worktree; figures are the evaluation worker's.
**Reported result:** default = Ember plus two Luna reviewers (64k tokens); high-assurance = Haiku plus two Luna reviewers (191k tokens; best real blocking-finding rate 1.2 of 8). A replication of Sonnet plus two Luna (mean 2.33 of 14) was indistinguishable from Ember plus two Luna at 2.2 times the cost, so the proposed change was rejected. Batches 9 to 11 had outage incidents that were rerun.
**Question:** make those two the packaged panel defaults, and when?
**My recommendation:** yes, but only after D-24 confirms the Muse models really answer as the model they are labelled (the results depend on it).
**If GO:** none yet; it depends on D-24 and on committing the report (D-03).
**Owner answer:**
**Coordinator reply:**

### D-12 Review panel unification research (worktree `brainstorm-reflect-panel`, branch `ironbelly/shadow-runs`)
**Source:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/RESEARCH-REPORT-review-panel-unification-run2.md` (scan lines 4702-4710, 4772, 4788-4791). Pull request #519 (Stages 0 to 2 of the reflect panel) merged 2026-11-12.
**Open questions:**
- **Q-40:** does "one core" mean a thin shared contract with a separate engine per module, or a single engine? A single engine triggers extra conditions (C-01).
- **Q-36:** about 15 rulings that block the plan: whether D-1 is a bug or a contract; the quorum rule; the convergence threshold and single-vendor stance; who owns the verdict; the severity pair; the finding-location type; the repair policy; the lens roster; the `lib/` gitignore; thresholds T-1 to T-10; the +35% time limit; who pays for the 326-run validation; who owns `verify-run`; the installed variants. The document recommends: D-1 is a bug; threshold 0.80 and degrade unless `--allow-single-vendor`; a fixed CRITICAL, MAJOR, MINOR severity pair.
- **Q-41:** what does "no change to `cli/reflect`" allow? One fix needs an edit at `cli/reflect/ensemble.py:601-630`.
- **Q-38:** archive or keep the five installed-only spec-panel variants?
**My recommendation:** answer Q-40 first (thin shared contract). It decides how many of the Q-36 rulings are needed at all.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-13 Blocker-classification program (17 owner decisions, OD1 to OD17)
**Source:** `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:1023-1044` and `09-plan-input.md:30-32` in the same worktree. The scan names it #552 (UNVERIFIED).
**Open:** OD3 asks whether private finding text may go to TypeSafe or Jev, and whether to request a key. OD5, OD6, OD7, OD8, OD10 and OD17 are undecided. The draft plan (`TASK-WF-loosenBlockerCla-20261115-133045`, line 21) uses the recommendations for OD1, 2, 4, 9 and 11 to 16 "unless the owner changes them"; that is not your confirmation.
**Document's recommendation:** decide privacy first; approve Jev for the 5-run experiment only with zero data retention or an accepted contract; OD17 defaults to no.
**My recommendation:** answer OD3 first.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-14 Centralized Review Panel, issue #520
**Source:** issue #520 body. These are still "Not known yet": the final shared interface, which additional callers are in scope, whether reflect's default engine changes, the rollout order and measurable benefit, and what is out of scope. The body still calls #519 "open"; it merged on 2026-11-12.
**Question:** claim #520 now, or wait for D-12?
**My recommendation:** wait for D-12 (Q-40 decides the shape).
**If GO (to start now anyway):** I correct #520's body (#519 is merged) and add the link to the unification research report.
**Owner answer:**
**Coordinator reply:**

### D-15 Model-policy hook (#546 and #551), 11 restrictions
**Source:** `.dev/brainstorms/20261114-jev-model-validation-hook/OPEN-QUESTIONS.md:17-35` in the eval worktree. Nothing is implemented, and nine facts there are UNVERIFIED.
**Question:** for each of the 11 restrictions (for example, models not on the list such as `gpt-6-luna` are denied), keep, narrow or drop? Open a version-2 issue?
**Document's recommendation:** per row, for example give every harness model a tier and use hash-tied grants.
**If GO:** none; answer per row in that file.
**Owner answer:**
**Coordinator reply:**

---

## Part C. Tiers and models

### D-20 Implement issue #523 (muse-ember-1.0 in Tier 4), IronClaude half
**Facts:** the Coder half (PR #502, release 20261112-1) merged on 2026-11-12 and its distribution run succeeded; eight running workspaces moved to it (reported by CoderOrchestrator, not checked by me). The IronClaude half is not started: `ccsession-models.json` tier 4 becomes `["T4Model01", "T4Model04", "T4Model02", "T4Model03"]` (Luna, Ember, Haiku, Grok), plus picker entries, docs, tests and changelog. Two workspaces are not on the new release: `bruno` (unreachable, ignored by you) and `will-two` (stopped). If `will-two` starts and downloads the new list before its Coder defaults catch up, its tier requests fail for up to about an hour.
**Position in the model order:** Coder put `muse-ember-1.0` after `muse-spark-1.3` (reported). Confirm.
**My recommendation:** go now. Merge any time after the PR review, because the Coder slot is already distributed.
**If GO:** I start a worker that implements #523, then `/sc:pr-submit --monitor 3` (fork only, never merge).
**Owner answer:**
**Coordinator reply:**

### D-21 Close issue #488 and #523 housekeeping
**Facts:** #488's IronClaude half merged as #518; the Coder issues #494 and #503 are closed (reported). Optional Coder cleanup later: remove `T3Model04` to `T3Model06` once every workspace has a model list at version 2026-11-11.1 or newer (Coder side, reported).
**Question:** close #488 by hand now?
**My recommendation:** yes, close it. The Coder cleanup stays with CoderOrchestrator.
**If GO:** none; closing issues is yours.
**Owner answer:**
**Coordinator reply:**

### D-22 Follow-up issue #489 (eval-framework panel tiers and alias map for Tier 2b)
**Status:** open; I have not read its body.
**Question:** claim it, and when?
**My recommendation:** after D-10 and D-11, since they touch the same evaluation framework.
**If GO:** I claim #489 with `/sc:issue --claim 489 --pipeline none`.
**Owner answer:**
**Coordinator reply:**

### D-23 Issue #517 (GLM thinking error stops a whole tier)
**Source:** main checkout `.dev/issues/517/issue-body.md:91`. A tier whose first model always thinks fails every request with the default effort and never moves to the next model. PR #516 only worked around this for the `issue-worker-t3` agent.
**Options:** (1) retry with effort `low`, no model parked; (2) move to the next model without the one-hour park; (3) fix at the gateway. The document recommends not a plain "switch" rule; whatever is chosen must never park the model.
**My recommendation:** option 1 as the first fix, option 3 as the real fix.
**If GO:** I claim #517 with `/sc:issue --claim 517 --pipeline none` and start a plan.
**Owner answer:**
**Coordinator reply:**

### D-24 Do the Muse models answer as the model they are labelled?
**Facts:** in one evaluation run, `muse-wonder-1.0` answered as `gpt-6.1-terra`. For `muse-ember-1.0` the gateway only lists it; nobody has made a completion call (reported). Routing is not ours to change.
**Question:** have a worker send one tiny completion to each Muse model through the gateway and report which model name comes back?
**My recommendation:** yes. It costs almost nothing and gates D-11 and D-20.
**If GO:** I start that read-only worker (no credentials printed).
**Owner answer:**
**Coordinator reply:**

---

## Part D. Issue watcher, guard and claim pipeline

### D-30 Issue watcher rollout, issue #450
**Facts:** only you can do these (no agent may): the live test, the shadow run, the lock test, the restart test and the cron install. `enabled` stays `false`. `docs/designs/issue-watcher-live-test.md` does not exist on master. The accepted "permission checks off for the first test session" may not cover the second agent that the claim now starts (document says "not confirmed"). The review-and-approval flow (plan posted on the issue, assignee asked to approve) is still "to be designed".
**Question:** who owns the watcher folder and its up to 6 sessions a day (this is Q20 in D-51), and when will you run the checklist?
**My recommendation:** name an owner (Q20 option 1), then follow the checklist in section 16 of `docs/designs/issue-watcher-setup.md` in order.
**If GO:** none; the steps are yours.
**Owner answer:**
**Coordinator reply:**

### D-31 Switch on the refusal for a missing pre-push guard (L2)
**Facts:** `IR7_REFUSE = False` on master. The refusal stays off until the #442 observations pass and you approve separately. The 12-item observation runbook (`.dev/issues/442/handoff-runbook.md`, worktree `issue-442-runbook`) needs a person at a real terminal, and no results file exists. A line in it says the L2 layer is not built, which is stale (it merged in #469). The related governed-claim checks OB-H1 item 1, OB-H2 and OB-H3 had not passed at the last record (2026-11-08); anything later is UNVERIFIED. The implement ledger for #442 stopped on 2026-11-09 (task 5 blocked at retry 3).
**Question:** will a person run the runbook, and is the stalled #442 work abandoned or to be resumed?
**My recommendation:** run the runbook before any governed claim is used on a real issue; resume #442 only after that.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-32 Claim-handoff plan (worktree `claim-handoff-b`)
**Source:** `.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909/`.
**Open:** which GitHub issue (written by you) should real recorded fixtures use (the answer goes in `tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md`)? Do you give the separate go to run Plan A with `/sc:implement`? Who runs and records the first live test (Plan B task 20, which has 11 PENDING facts)? The revised 19-task plan was reviewed only partly (the Tier 2 merge was not a real debate); re-run `/sc:reflect --mode pre --tier 2` with the advocate dispatch?
**My recommendation:** re-run the review first, then give the go.
**If GO:** I start the re-review worker only.
**Owner answer:**
**Coordinator reply:**

### D-33 Leftovers from issue #443 (not blocking)
**Facts (from the deleted worktree's notes):** a 1-in-176 xdist failure (class of #352, still open), a test-environment leak in `_real_launch`, and `ccsession:985` treating every return code 1 as a refusal. The 30 CI repeat runs were never done.
**Question:** file one issue for these?
**My recommendation:** yes, one low-priority issue.
**If GO:** I file one issue with `/sc:issue --create` (feature, quick depth).
**Owner answer:**
**Coordinator reply:**

---

## Part E. The `--unattended` flag

### D-40 Open items after PR #508
**Facts:** issue #507 is closed and PR #508 merged on 2026-11-11. Still open for you, from CoderOrchestrator's analysis (unverified by me): the five gates that turn a person's check into a caller input (review-translation `--context`, cli-portify `--resume`, cli-eval W3, reflect `--remediate`, tdd); whether `cleanup`, `improve`, `task`, `tasklist` and `cli-eval` are held out until the second-phase live check passes; new evaluation suites for the second-phase commands (a follow-up). A Low review finding was left open: the developer guide still names the removed `UNATTENDED_COMMANDS` and removed tests (lines 394, 1091, 1138).
**My recommendation:** hold those five commands out until the live check passes; fix the Low finding in a small docs PR.
**If GO:** I start a worker that fixes the stale developer-guide lines and opens a PR.
**Owner answer:**
**Coordinator reply:**

---

## Part F. Observer, orchestrator TUI and design records

### D-50 Observer release 3 and the direction record
**Source:** `.dev/issues/409/bmad/spec-orca-observer/release-gates.md:10, 20-34` and `.dev/issues/409/owner-decisions-20261108.md:17`.
**Open:** the dated "direction selected" record and what "production integration" means. Without it release 3 cannot start. Two readings are at lines 31-32; the stricter applies until you say. Also undecided from 2026-11-08: write-back from the BBS, the licence opinion, and TUIBBS as the staff platform. Issue #409 stays open. The Medium review finding left open on #514 (a capped list can recount an old evicted question) was accepted by you; recorded here only.
**My recommendation:** write the direction record now (the orchestrator-TUI notes recommend option 1, 68%).
**If GO:** none; the record must be written by you.
**Owner answer:**
**Coordinator reply:**

### D-51 Orchestrator-TUI alignment questions (Q7 to Q41)
**Source:** `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/open-decisions.md` (untracked, in worktree `issue-339-orchestrator-mode`). It gives three options each with a recommended one and a confidence. None has an answer in `owner-answers.md`.
**Open (the file's recommendation and confidence in brackets):**
- Q29: how does this workspace get the sweep command (merged in #539 but not runnable here)? Template, then remove the extra copy [option 1, 70%].
- Q20: who owns the watcher folder and its sessions [option 1, a named person, 70%].
- Q24: who runs the live Orca checks [option 1, 65%].
- Q30: which coordinator may the questions-panel test read, and do you accept that questions may be lost [option 1, 85%].
- Q14: what does "#339 complete" mean for #423 [option 1, 80%].
- Q7 and Q8: commit your decision records; write a dated design-direction record [option 1, 65% and 68%].
- Q13, Q15, Q16, Q19, Q22, Q41: the observer falling back to plain `orca`; v2 pushing into non-worker sessions; trust scope; which dashboard improvement first (55%, re-read the reviewer's comment); stale-file age; confirm that a worktree with no agent for a moment is accepted [option A].
- Owner actions that block work: start Plan A; supply an owner-written issue for test fixtures; "go" on Task 16 (remove plain `approved`); written acceptance for the first live test; separate grants for GitHub posts; fix the stale "private fork" line in CLAUDE.md.
**My recommendation:** if you agree with the file's recommended option everywhere, write "accept all recommended" and I record it here; any change, list it.
**If GO:** none; the owner actions are yours.
**Owner answer:**
**Coordinator reply:**

### D-52 Orchestrator v2 worker-liveness leftovers
**Source:** `.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/merged-requirements.md:804-834`.
**Open:** the restart window (1 per 60 minutes is unmeasured); whether a v2 monitor may live in package code (Q6); the v2 build waits on both. The reply-acknowledgement rule and the person-directed cancellation rule were answered on 2026-11-07 and shipped in #434.
**My recommendation:** measure the restart window first; it is cheap.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-53 Orca-refactor evaluation
**Source:** `.dev/brainstorms/20261111-orca-orchestrator-refactor-eval/adversarial/merged-output.md:8-12, 47, 79`.
**Open:** accept "do not make brainstorm call Orca; use a coordinator session for separate processes"? Points C-002, C-004 (two routes for non-Claude models, leaning Route 1), C-008 and C-009 were left open. The document recommends measuring worker cold-start time and cost before any decision to use workers.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-54 Dashboard research choices
**Source:** `.dev/research/orca-dashboard-20261105/REPORT.md:221-234, 256`. Framework (Bubble Tea with Lip Gloss, Textual, or Ratatui), where dashboard-only state lives, how to list every decision completely, and terminal sizes. The report says none is needed to finish its design deliverables. Likely moot because `superclaude observe` shipped in releases 1 and 2 (UNVERIFIED).
**My recommendation:** mark it moot.
**If GO:** none.
**Owner answer:**
**Coordinator reply:**

---

## Part G. Model defaults, research and leftovers

### D-60 Issue #462 (Opus 5.5 default in orchestrator-spawned sessions)
**Facts:** PR #483 was closed. Fix commit `91af19e56` (plus a format commit) exists only in worktree `issue-462`, with no remote branch. The diagnosis stopped at confidence 0.30. Either the setup commands explicitly asked for `claude-opus-5-5`, or an owner decision on later pins is missing (`REPORT.md:30,62` in that worktree).
**Question:** can you give one real example of an unqualified launch that landed on Opus, with its full command? Or give a direct instruction on the pins?
**My recommendation:** keep implementation paused. Do not hardcode Tier 1b as a universal default.
**If GO:** none.
**Owner answer:**
**Coordinator reply:**

### D-61 Issues #463 (model and effort router research) and #470 (research pipeline block)
**Facts:** #463's research task halted at its work-splitting check. Options in `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/OPEN-DECISIONS.md:19-41`: (1) one more mechanically built correction plus one final review; (2) relax the task's rules; (3) set it aside for a smaller `/tech-research`; (4) stop. The document recommends option 1, with option 3 as the alternative. Also: ratify that the executor launched all workers itself because the named coordinator terminal no longer exists (document: yes); who is "Jev" (unresolved; must not be guessed); what happens to six workers still `unverifiable`. #470 stays on hold, as you ordered.
**My recommendation:** option 3. #463 should not start before #470's plan unblocks it.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-62 `.claude-audit/` in the main checkout
**Facts:** 65 unchecked "Need Decision" boxes in 26 batch reports; batches 15, 27 and 29 to 47 are missing; `progress.json` is stale. The question is which stray repository files to delete.
**My recommendation:** discard this audit and run a fresh one when you want it; the batches are incomplete.
**If GO:** none; deleting is yours.
**Owner answer:**
**Coordinator reply:**

### D-63 Follow-ups from the deleted `mcp-audit` worktree
**Facts (its findings file went with the worktree; this is the summary I kept):** the file `agent.md` has malformed front matter (no opening `---`; master's still starts with `name: sc:agent`), and fixing it may rename the slash command, so it needs its own issue. The same tool-less web-research wording appears in five other skills. `load.md` has drifted. `task-builder` line 1208 needs a look.
**My recommendation:** file one issue for `agent.md` and one for the wording drift.
**If GO:** I file those two issues with `/sc:issue --create` (bug, quick depth).
**Owner answer:**
**Coordinator reply:**

### D-64 Follow-up left by the deleted `codegraph-wording` session
**Facts:** that session's last note recommended that the coordinator fix "two stale sentences" in a follow-up so that guide rule 7 and two files agree. The session and its report were removed with the worktree, so I do not know which two sentences. The change itself merged as PR #513.
**Question:** do you want me to dig it out of the merged PR and its review comments?
**My recommendation:** no, unless you remember the file names; the cost is higher than the value.
**If GO:** I read PR #513's files and review comments and report what the two sentences are.
**Owner answer:**
**Coordinator reply:**

---

## Part H. This file

### D-70 Where does this file go next?
**Facts:** the file lives on its own branch on the fork. No pull request is open.
**Question:** open a pull request to put it on master, or keep it as a branch?
**My recommendation:** keep it as a branch while you answer; open a PR when it is mostly answered, so master is not filled with a changing document.
**If GO (open a PR now):** I open one with `/sc:pr-submit --monitor 3`.
**Owner answer:**
**Coordinator reply:**
