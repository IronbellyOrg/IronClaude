# Open decisions and questions, all IronClaude worktrees

Written 2026-11-15 by the coordinator (ORCH-IronClaude). Scope: the 20 IronClaude worktrees found on 2026-11-15, the open issues I track, and the open items from this session. The private workspace-image repository's own worktrees were not swept.

**Updated 2026-11-26** (walk-through with the coordinator, one entry at a time, each change approved before it was written). Every entry now starts with a Status line checked on 2026-11-26 against `origin/integration` and GitHub; the older text of an entry is mostly kept below its status line and is historical; where the old question or table was replaced or shortened (D-03, D-10, D-11, D-13, D-20, D-21, D-32 and a few reworded lines), the 2026-11-15 and 2026-11-16 wording is in the git history of this file on integration (PR 859). Counted from the Status lines, the file has 35 entries: 21 closed or done (D-01, D-02, D-03 (superseded; the question on issue 463's branch stays with the owner), D-04, D-10, D-15, D-20, D-21, D-23, D-24, D-30, D-32, D-33, D-54, D-60, D-61, D-62, D-63, D-64, D-67, D-68); 10 decided but not finished (D-12, D-13, D-14, D-22 (owner said not to claim 489 now), D-40, D-50, D-52, D-53, D-65, D-66); 4 open or pending (D-11, D-31, D-51 (mostly answered; Q22 deferred and two other points pending), D-70). D-31 (a refusal switch still off) is worth reading first. Nothing here is a decision by the coordinator; PENDING OWNER means the owner has not answered on the record. The 2-hour watch described under "Watch window" below is over (that paragraph says so).

## How to use this file

From 2026-11-26 the owner answers in chat; the coordinator records the answer here. The Owner answer and Coordinator reply lines below are historical (the 2026-11-15 to 2026-11-16 method); the file watch described in steps 1 to 4 of the original text ended on 2026-11-16.

Original method (historical):

1. Write your answer on the **Owner answer:** line of an item. Plain words are fine ("yes", "option 2", "no, because ...").
2. Add the word `GO` at the end of your answer if you want me to start the "If GO" step listed under that item. Without `GO` I only record your answer and reply. I never merge, and I never act on an item that has no "If GO" line.
3. I watch this file for 2 hours and reply on the **Coordinator reply:** line of the item you changed. Each reply is committed and pushed to this same branch, so the remote copy matches. After the watch ends I stop; the file stays.
4. If you edit on GitHub, I fetch before I reply. If two edits collide I keep yours and reply under it.
5. Status words: OPEN (waiting for you), ANSWERED (you answered, nothing else to do), IN PROGRESS (a worker is running), DONE. In the 2026-11-26 update, Status lines use plain words such as done, closed, superseded, decided, partly open, still open and conflict; PENDING OWNER means the owner has not answered on the record.

Evidence notes: facts come from the worktree scans I ran on 2026-11-15 and from this session. Anything I could not check is marked UNVERIFIED. File and line references come from the scans and were not all re-read by me. Numbers from workers (for example evaluation results) are theirs, not mine.

**Watch window:** 2026-11-16 16:55 UTC to 18:55 UTC. The file was pushed on 2026-11-15 but I only saw the worker's report on 2026-11-16, so the watch starts then. The monitor ran from about 17:00 to about 17:55 UTC (two 30-minute runs). I did not re-arm it for the last hour because the session was idle. A one-shot check at 19:27 UTC found no edits by you in this file or on the remote branch, so nothing was missed. The watch is now over: answers you write in this file after 18:55 UTC are read only when you tell me. Answers you gave in chat are recorded in D-13, D-61, D-65, D-66, D-67 and D-68.

---

## Part A. Worktree cleanup and uncommitted work

Done today, on your order to delete merged worktrees after validating that nothing of consequence was unpushed:

- Deleted 11 worktrees: `install-core-stale-warning`, `issue-394-launch-level-hook`, `issue-441`, `issue-443`, `issue-488-tiers`, `issue-504`, `issue-512`, `tier3-effort`, `codegraph-wording`, `mcp-audit`, `smoke-504`.
- Check used: the worktree's last commit equals the last commit of its merged pull request (or, for `mcp-audit` and `smoke-504`, is already inside `origin/master`), and nothing under `.dev/tasks`, `src`, `tests`, `docs` or any other non-`.dev` path was untracked or modified. Untracked files under `.dev/` (claim packages, reflect, troubleshoot and brainstorm output, audit notes) were not kept, as you ordered. Orca needed `--force` for seven of them because of those untracked files.
- Two idle Claude sessions that sat in `issue-488-tiers` and `codegraph-wording` were stopped by the removal.
- The local branch `ironbelly/issue-394-launch-level-hook` was kept by Orca (it could not prove the branch merged, because the PR was squash-merged). See D-04.
- Kept because they failed the check: `issue-409-mvp` (D-01) and `issue-339-orchestrator-mode` (D-02). (2026-11-26: both worktrees no longer exist; see D-01 and D-02.)

### D-01 Two commits exist only on this computer (observer, branch `409-Phase2`)
**Status: DONE (updated 2026-11-26).** Merged via PRs 577 (enable the live questions read) and 586 (live questions test and load test recorded), both merged 2026-11-17; `QUESTION_GATE_PASSED = True` on integration; issue 409 is still open. The local commits `1ae72e1a1` and `f104ca51a` on `409-Phase2` are superseded, and the worktree `issue-409-mvp` no longer exists. The text below is the 2026-11-15 entry (historical).
**Where:** worktree `issue-409-mvp` (Orca display name `issue-409-TUIDash-P2`).
**Question:** Commits `1ae72e1a1` ("enable the live coordinator-questions read against the owner's record") and `f104ca51a` ("cite the owner-written pass record ... archive the release 2 plan") are not on GitHub. They change `src/superclaude/cli/observe/commands.py` and tests. Push them and open a pull request?
**Why it matters:** the first commit switches the live read of coordinator questions on (`QUESTION_GATE_PASSED`). The orchestrator-TUI notes (D-51, Q6 and Q30) say it should stay off until a seeded live test with a throwaway coordinator has run. A scan says that test appears not done (UNVERIFIED). Another scan reported the branch as 5 commits ahead; my own check counted 2 not on the remote.
**My recommendation:** push and open the PR so the work is not only local, and do not merge it until the seeded live test (Q30 option 1) has passed.
**If GO:** I push `409-Phase2` and run `/sc:pr-submit --monitor 3` for it (fork only, never merge).
**Owner answer:**
**Coordinator reply:**

### D-02 Your decision records in the 339 worktree are uncommitted
**Status: DONE (updated 2026-11-26).** Committed via PRs 587, 588 and 589 (merged 2026-11-17); all four record files are on integration under `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/`. Issue 339 is still open; the worktree `issue-339-orchestrator-mode` no longer exists. The text below is the 2026-11-15 entry (historical).
**Where:** worktree `issue-339-orchestrator-mode` (the sweep PR #539 is merged). Four tracked files are modified and `open-decisions.md` is untracked, all under `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/`.
**Question:** Commit them on a new docs branch and open a PR (this is Q7 in that file), or leave them as they are?
**Why it matters:** these are your answers (`owner-answers.md`, `accepted-answers.md`, `human-decisions.md`) and the question list (`open-decisions.md`, see D-51). They exist only in this one folder.
**My recommendation:** commit them (the file's own recommendation for Q7 is option 1, 65%).
**If GO:** I start a worker that commits those files on a new branch from `origin/master` and opens a docs PR through `/sc:pr-submit --monitor 3`.
**Owner answer:**
**Coordinator reply:**

### D-03 Uncommitted work in five other worktrees
**Status: SUPERSEDED (updated 2026-11-26).** The five worktrees (`eval-tasklist-review-panel`, `brainstorm-reflect-panel`, `claim-handoff-b`, `issue-442-runbook`, `issue-463`) no longer exist. Their branches remain on origin with commits that are not ancestors of integration:

| Branch | Commits not on integration (hash-based) | Pull request / issue |
|---|---|---|
| `ironbelly/eval-tasklist-review-panel` | 30 | no PR |
| `ironbelly/shadow-runs` | 13 | PR 581 merged |
| `ironbelly/claim-handoff-b` | 5 | PR 584 (Plan A) merged |
| `ironbelly/issue-442-runbook` | 5 | PRs 677 and 685 merged; issue 442 open |
| `ironbelly/issue-463` | 1 | no PR; issue 463 closed |

The counts are hash-based and the repo squash-merges PRs, so the commits of `shadow-runs`, `claim-handoff-b` and `issue-442-runbook` are probably already on integration through their merged PRs. `eval-tasklist-review-panel` (30, no PR) and `issue-463` (1, no PR, issue closed) may hold work that is NOT on integration. Whether any uncommitted files existed in those worktrees is UNVERIFIED and cannot be checked now.
**Update 2026-11-26:** the owner ordered a pull request for `ironbelly/eval-tasklist-review-panel`; PR 873 is open (base integration, 12,861 files, all under `.dev/`). Before it, the coordinator pushed the 4 commits that existed only locally (2026-11-16: Recipe Ledger freeze, hold-out ground truth, debate of cuts, frozen hold-out comparison) and one commit that removes a link to a private repository. See D-10 for the hold-out result.
**Open follow-up: PENDING OWNER** for `issue-463` only: open a PR for the branch, or delete it.

### D-04 Leftover local branch
**Status: DONE (updated 2026-11-26).** The owner said yes; the coordinator deleted the local branch `ironbelly/issue-394-launch-level-hook` (tip `e6febfa2f`) on 2026-11-26 after the file check below. The text below is historical. Before the deletion the branch still existed, with no remote copy and no worktree. PR #432 merged 2026-11-08 by squash (commit `3b344dd4e`), so the branch's 4 commits show as not on integration by hash only. A file comparison of the branch tip against the squash commit on all 201 files the branch touched found 0 that differ, so the branch holds nothing that is not on integration.
**Question:** Delete the local branch?
**My recommendation:** yes, delete it.
**If GO:** I delete that one local branch only.
**Owner answer:**
**Coordinator reply:**

---

## Part B. Review panel program

### D-10 Evaluation of the tasklist review panel (worktree `eval-tasklist-review-panel`)
**Status: CLOSED (checked 2026-11-26).** The owner dropped the 96-run ablation; Recipe Ledger was not adopted by the hold-out comparison (PR 873 carries the evidence); no open point remains. The text below is historical (it was written before this closure, and its UNVERIFIED notes no longer apply).
**Earlier status (2026-11-26, before the closure): PARTLY OVERTAKEN; the open points were UNVERIFIED until the coordinator restated them.** The source files exist on branch `ironbelly/eval-tasklist-review-panel` (PR 873 is open; not yet on integration; worktree gone). On 2026-11-16 that branch recorded: Sweep Sheet stopped by the owner after its recall gate failed twice; Recipe Ledger run as a 9-replicate exploratory experiment (3 arms, 3 study packages); the owner's model-usage answer; and next steps "not yet ordered by the owner". Related issues 549, 550 and 531 are open and none of them contains these answers (550 says to treat the Recipe Ledger result as not proven until a pre-registered re-test; 531 notes the served-model risk but records no drop-or-flag rule).
**Source:** `.dev/eval-workspaces/tasklist-review-panel/OPEN-DECISIONS-20261115.md` and `OPEN-QUESTIONS-20261115.md`, and `20261114-sweep-sheet/OPEN-ITEMS.md` in that worktree. The document's own advice is to ask you one question at a time with a recommendation.
**Questions, as checked:**
- **a. Hold-out answers:** MOOT for Sweep Sheet (stopped 2026-11-16; its hold-out rows are void). For Recipe Ledger, ANSWERED by the hold-out result (see the update below): the hold-out ground truth was written and the comparison ran.
- **b. Strictness:** PARTLY ANSWERED by the hold-out result (a strict format reading would fail 46 percent of Recipe Ledger reports). The rest, on the 10% compliance gate, on a model's review of a recipe instead of a person's, and on who runs the three maintainer-only tests, is UNVERIFIED until the coordinator restates it.
- **c. Severity change:** PARTLY ANSWERED by the hold-out result (Recipe Ledger failed non-regression); whether the severity change itself is still wanted is UNVERIFIED until the coordinator restates it.
- **d. Mismatched models:** PARTLY ANSWERED. The owner's 2026-11-16 answer is that model-usage infractions do not halt work: log and report warnings after the fact; strict verification of the served model is not a first-release gate. So "only flag it" is answered in principle. The 96-run ablation and the `## Ledger` heading rule are STILL OPEN.
- **e. Housekeeping:** STILL OPEN. No recorded answer on the commit and push order or on deleting the three stray scripts; whether the old 1.83 baseline was inflated is UNVERIFIED.
**Update 2026-11-26:** the owner ordered a pull request for `ironbelly/eval-tasklist-review-panel`; PR 873 is open (base integration, 12,861 files, all under `.dev/`; see D-03). The 4 commits that existed only locally are now pushed (2026-11-16: Recipe Ledger freeze, hold-out ground truth, debate of cuts, frozen hold-out comparison). The Recipe Ledger hold-out result in those commits: NOT adopted. It failed time, effect, consistency and non-regression; it passed precision and one more check; a strict format reading would fail 46 percent of its reports (60 panel runs). So question a is no longer a recommended next step, and parts of b and c are answered by that result. The owner said this entry "makes no sense"; the remaining open points are UNVERIFIED until the coordinator restates them.
**My recommendation (2026-11-15, historical):** answer a to e in that file's own order, a first (for Recipe Ledger), because the hold-out set gates every later claim.
**If GO:** none; this needs your answers first.
**Owner answer:**
**Coordinator reply:**

### D-11 Adopt the evaluation's reviewer combinations as the panel defaults?
**Status: SUPERSEDED, PENDING OWNER (checked 2026-11-26).** Integration packages a different, provisional default review panel: `wonsol` (`muse-wonder-1.0` with fallback `claude-sonnet-5-5`, `gpt-6.1-sol`, `muse-ember-1.0`), set by PR 623 on 2026-11-18 on the owner's order although its confirming test missed its pre-registered bar (`docs/reference/review-panel-live7.md`). The evaluation combinations (Ember plus two Luna; Haiku plus two Luna) were not adopted as written; the source report exists only on branch `ironbelly/eval-tasklist-review-panel`. Open: whether the evaluation combinations should still be considered. D-24 (do the Muse models answer as labelled) is closed (2026-11-26). 2026-11-26: the owner asked for the top 5 combinations compared with today's default, using the latest table; the report is at `~/workspaces/worktrees/IronClaude/Coordinator/.dev/reviews/d11-top5-combinations-20261126.md`. Key facts from it: the latest table is the FINAL table of 2026-11-13; the proposed default (Ember plus two Luna) is row 26 of 32, not in the top 5; in the one fair test (stronger panel, same plans) `wonsol` ranked first (0.432) and Ember plus two Luna last of seven (0.188); the confirming test did not meet its bar (+0.099 and +0.109, lower bounds -0.004 and -0.006). The `wonsol` test commits `3f698dc63`, `567cf8540` and `90b5fec22` exist only on a local branch (`ironbelly/eval-severity-rule-test`, not pushed). The coordinator's recommendation to the owner is to keep `wonsol` and close D-11; the owner has not answered yet, so this entry stays PENDING OWNER.
**Source:** `COMBO-REPORT.md` in the same worktree; figures are the evaluation worker's.
**Reported result:** default = Ember plus two Luna reviewers (64k tokens); high-assurance = Haiku plus two Luna reviewers (191k tokens; best real blocking-finding rate 1.2 of 8). A replication of Sonnet plus two Luna (mean 2.33 of 14) was indistinguishable from Ember plus two Luna at 2.2 times the cost, so the proposed change was rejected. Batches 9 to 11 had outage incidents that were rerun.
**Owner answer:**
**Coordinator reply:**

### D-12 Review panel unification research (worktree `brainstorm-reflect-panel`, branch `ironbelly/shadow-runs`)
**Status: DECIDED, NOT IMPLEMENTED (updated 2026-11-26).** On 2026-11-26 the owner chose ONE ENGINE for Q-40 (not the debate's per-module engines); the report's C-01 conditions T-a, T-b, T-c and the anchor-span precondition now apply. The Q-36 rulings and Q-41 were approved as recommended on 2026-11-26; Q-41's weak reading ("additive files only") may not hold under one engine (UNVERIFIED; the plan step must restate it). Q-38: the owner said copy the five variants to an archive folder and open an issue to re-review and iterate on them; DONE: copies (sha256 equal) at `~/workspaces/worktree-archives/IronClaude/spec-panel-variants-20261126/`, issue 877 opened. The text below is the earlier state of this entry (historical). The owner said this is "not a question, push to PR". Finding: `ironbelly/shadow-runs` has 13 files that differ from integration, all changed later on integration (newer versions there), and the blocker-classification stage 3 package is on integration (139 files), so there is nothing unmerged to push. The routed answers packets (`ironbelly__shadow-runs__answers.md` and the two others) were searched in all 308 refs, all session logs and the file system and were not found. The owner said "no idea, find them"; the coordinator then also searched every file under `~/.claude` (session logs, subagent logs, paste cache), the Orca config and the worktree archives. Result: the three answer packets were never pasted into any session; the owner's 2026-11-16 paste contained only the routing table plus sections 1 and 7, and says the packets were "split locally from the verified consolidated answer artifact", so they live outside this machine. NOT recoverable here. What is recorded: issue 549 (open) has the owner's approvals of 2026-11-14: one shared Review Panel core in `src/superclaude/cli/review/` with thin modules for reflect, tasklist and workflow, spec review and later PR review; both current worktrees finish, push to a PR and merge; then a brand-new worktree is created for the unification and the two old worktrees are deleted; branch names `feat_review-panel/<name>`; close condition: the new unification worktree exists and both older worktrees are finished and deleted. Status of that plan on 2026-11-26: the tasklist worktree work is PR 873 (open); the shadow-runs work is merged (PR 581; the run-1-versus-run-2 comparison package is on integration); both old worktrees are deleted; the new unification worktree is NOT created. So "push to PR" is done for both branches. Q-40 was open at that time (decided 2026-11-26, see above): the 2026-11-14 approval settles the name "one shared Review Panel core ... with thin modules", not the engine question. The run 2 research report (line 4790, row Q-40) quotes that approval and still asks the owner whether to accept the debate's reading: a thin shared contract with a separate engine per module (spec review on the v1 engine, reflect and PR review on the v2 kernel), or one engine (which triggers the C-01 conditions T-a, T-b, T-c). Q-36, Q-41 and Q-38 were then pending (answered 2026-11-26, see above). The report's own advice: for Q-41 (what "no change to `cli/reflect`" allows), the owner states the reading; if it is weak (additive files only), list the H1 edit at `cli/reflect/ensemble.py:601-630` as a named exception or deliver H1 through a brief file, and settle where the write-side helpers live before they are built. For Q-38 (the five installed-only spec-panel variants under `~/.claude`), it is machine-state cleanup only, with no effect on the core design, and no research can add evidence; leave the status quo or archive with the `.dev` archives kept; do not change `~/.claude` without the owner. The worktree `brainstorm-reflect-panel` is gone; branch `ironbelly/shadow-runs` remains (PR 581 merged). The research report is on integration. Issue 549 (open) recommends "one shared Review Panel core in `src/superclaude/cli/review/`, with thin modules for reflect, tasklist and workflow, spec review, and later PR review". No owner answer to Q-40, Q-36, Q-41 or Q-38 is recorded on integration; the owner's 2026-11-16 answers to D-12 were routed to a packet not on integration (`owner-answers.md`, line 224 onward, under `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/`).
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
**Status: DECIDED, NOT IMPLEMENTED (updated 2026-11-26).** On 2026-11-26 the owner approved all recommendations as written: OD3 no for private repositories; OD5 no; OD6 defer; OD7 align Medium to non-blocking; OD8 neither; OD10 per the document; OD17 no brake in version 1 with the entry condition. Earlier state (checked 2026-11-26, before the answers): Issue 552 is open; stages 0, 1 and 3 merged (PRs 581, 582, 605, 688, 694). The classifier has no authority in version 1, and a real Jev run still needs the owner decision on sending finding text to TypeSafe and an API key (issue 552 status review of 2026-11-17). Stage four waits on the owner's chat go and on accepting the recorded classifier cuts (backlog review of 2026-11-24). The program files are on integration under `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/`. No answer to OD3 or OD5 to OD17 is recorded on integration; the owner's 2026-11-16 answers to D-13 were routed to a packet not on integration (`owner-answers.md`, line 224 onward, under `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/`).
**Source:** `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:1023-1044` and `09-plan-input.md:30-32` in the same worktree. The scan names it #552 (UNVERIFIED).
**Open:** OD3 asks whether private finding text may go to TypeSafe or Jev, and whether to request a key. OD5, OD6, OD7, OD8, OD10 and OD17 are undecided. The draft plan (`TASK-WF-loosenBlockerCla-20261115-133045`, line 21) uses the recommendations for OD1, 2, 4, 9 and 11 to 16 "unless the owner changes them"; that is not your confirmation.
**Document's recommendation:** decide privacy first; approve Jev for the 5-run experiment only with zero data retention or an accepted contract; OD17 defaults to no.
**My recommendation:** answer OD3 first.
**Update 2026-11-16:** the owner's answer packet (issue-based split, pasted in chat) says to use a pinned Jev version (issue #553, see D-65). It does not answer OD3 (data-sharing approval) or evaluation access; both stayed open on 2026-11-16 (OD3 was answered on 2026-11-26, see the Status line above).
**Update 2026-11-16 (second):** for two other tools (issues #574 and #575, see D-67 and D-68) the owner said that sending conversation data, commands, output and code to Jev is a blocker at the moment, that live runs use public fixtures only, and that an alternative judge (a decision model from Anthropic, or a local model on a 3090 or 4090 GPU) and, for jev-pruner, a risk and legal assessment come first. That was stated for those two tools.
**Superseded (2026-11-26):** the hold above was reversed by the owner in chat on 2026-11-16 (about 21:19 UTC; recorded by the coordinator, no verbatim wording kept): use Jev directly because the IronClaude repo is public. This does not cover private repositories or OD3. Issues 574, 575 and 576 are closed. The reversal did not answer OD3 for the blocker classifier at that time; on 2026-11-26 the owner answered OD3: no for private repositories (see the Status line above), so OD3 is no longer pending.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-14 Centralized Review Panel, issue #520
**Status: DECIDED: WAIT FOR D-12 (updated 2026-11-26).** The owner approved on 2026-11-26: wait for D-12. Issue 520 is open. Its body called PR 519 open; the owner said "Correct", and the coordinator corrected the body on 2026-11-26 (PR 519 marked merged 2026-11-12 in four places; read back and checked). The body is corrected. The unification is being carried on tracking issue 549 (520's status review of 2026-11-17). The shared interface, the caller list and the reflect default-engine decision are still "Not known yet", and they depend on D-12 (open).
**Source:** issue #520 body. These are still "Not known yet": the final shared interface, which additional callers are in scope, whether reflect's default engine changes, the rollout order and measurable benefit, and what is out of scope. The body still calls #519 "open"; it merged on 2026-11-12.
**Question:** claim #520 now, or wait for D-12?
**My recommendation:** wait for D-12 (Q-40 decides the shape).
**If GO (to start now anyway):** I correct #520's body (#519 is merged) and add the link to the unification research report.
**Owner answer:**
**Coordinator reply:**

### D-15 Model-policy hook (#546 and #551), 11 restrictions
**Status: CLOSED, NOT PLANNED (checked 2026-11-26).** Issue 551 was closed as not planned on the owner's instruction on 2026-11-17 (the model-policy hook effort is dropped for now; reopen 551 to resume); issue 546 was closed as not planned on 2026-11-24. No hook is on integration. The design and its 11 restrictions (`.dev/brainstorms/20261114-jev-model-validation-hook/`, including `OPEN-QUESTIONS.md` and `merged-requirements.md`) exist on the remote fork branch `origin/ironbelly/eval-severity-rule-test` (commit `e83a6faa9`, 33 files), not on integration (0 files on `origin/integration`); not at risk of loss. The question and lines below are historical. Per-row answers to the 11 restrictions are not recorded on integration; the owner's 2026-11-16 answers to D-15 (final v1 rule: warning-only, limited to model-usage compliance; real blockers keep review and refactoring) were routed to a packet not on integration (`owner-answers.md`, line 224 onward, under `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/`).
**Source (historical):** `.dev/brainstorms/20261114-jev-model-validation-hook/OPEN-QUESTIONS.md:17-35` in the eval worktree. Nothing is implemented, and nine facts there are UNVERIFIED.
**Question:** for each of the 11 restrictions (for example, models not on the list such as `gpt-6-luna` are denied), keep, narrow or drop? Open a version-2 issue?
**Document's recommendation:** per row, for example give every harness model a tier and use hash-tied grants.
**If GO:** none; answer per row in that file.
**Owner answer (historical):**
**Coordinator reply (historical):**

---

## Part C. Tiers and models

### D-20 Implement issue #523 (muse-ember-1.0 in Tier 4), IronClaude half
**Status: CLOSED BY OWNER DECISION (updated 2026-11-26).** The owner said issue 523 STAYS CLOSED. Ember fact: the workspace env defaults set `T4Model04=muse-ember-1.0`, but ccsession orders a tier by the slot names in its model list and `ccsession-models.json` on integration names only `T4Model01` to `T4Model03`, so ccsession does not use Ember in Tier 4 today. Earlier state (checked 2026-11-26): issue 523 was closed as completed on 2026-11-24 (closed by the owner's login at about 15:55 UTC, no closing comment, no linked pull request), although the cleanup review of the same day said still-relevant, keep open. The change is not on integration or master: `src/superclaude/skills/ccsession-tag/ccsession-models.json` still lists Tier 4 as `T4Model01` to `T4Model03` (no `T4Model04`, no Ember), and no pull request for 523 was found. The work the review lists: tier 4 order `[T4Model01, T4Model04, T4Model02, T4Model03]`, Ember in `picker.show`, `picker.one_million_context` and `picker.display_overrides`, the `review-tiers.default.json` tier 4 list, test fixtures and docs. The owner said "Investigate". Findings (2026-11-26): the closure sits inside a run of four COMPLETED closures within 82 seconds (issues 501, 421, 387 and 523, between about 15:54:05 and 15:55:26 UTC), about 4.5 hours after the backlog review that called 523 still-relevant (P2, Simple/S). The change is not made: `muse-ember-1.0` is a review-panel seat (`tier5c` in `review-tiers.default.json`, PR 623, the `wonsol` panel), but `ccsession-models.json` tier 4 still lists `T4Model01` to `T4Model03`. Likely closed by a bulk pass in error; UNVERIFIED, because no statement of intent exists. Decided 2026-11-26: 523 stays closed.
**Facts (2026-11-15, not rechecked):** the half in the private workspace-image repository (issue 503 there, release 20261112-1) merged on 2026-11-12 and its distribution run succeeded (reported, not checked by me). The IronClaude half was not started: `ccsession-models.json` tier 4 becomes `["T4Model01", "T4Model04", "T4Model02", "T4Model03"]` (Luna, Ember, Haiku, Grok), plus picker entries, docs, tests and changelog. Two workspaces were not on the new release (one unreachable and ignored by you, one stopped); if the stopped one starts and downloads the new list before its defaults catch up, its tier requests fail for up to about an hour.
**Position in the model order:** the workspace-image repository put `muse-ember-1.0` after `muse-spark-1.3` (reported). Confirm.
**My recommendation:** go now. Merge any time after the PR review, because the workspace slot is already distributed.
**If GO:** I start a worker that implements #523, then `/sc:pr-submit --monitor 3` (fork only, never merge).
**Owner answer:**
**Coordinator reply:**

### D-21 Close issue #488 and #523 housekeeping
**Status: DONE (checked 2026-11-26).** Issue 488 is closed as completed (2026-11-17); its IronClaude half merged as PR 518 on 2026-11-12. The 523 housekeeping part is covered by D-20 (523 is closed but the change is not on integration). The optional cleanup of old Tier 3 slots belongs to the private workspace-image repository and is not tracked here. The text below is historical.
**Facts (2026-11-15):** #488's IronClaude half merged as #518; the issues #494 and #503 in the private workspace-image repository are closed (reported). Optional cleanup later: remove `T3Model04` to `T3Model06` once every workspace has a model list at version 2026-11-11.1 or newer (workspace-image side, reported).
**Question:** close #488 by hand now?
**My recommendation:** yes, close it. The cleanup stays with the workspace-image team's orchestrator.
**If GO:** none; closing issues is yours.
**Owner answer (historical):**
**Coordinator reply (historical):**

### D-22 Follow-up issue #489 (eval-framework panel tiers and alias map for Tier 2b)
**Status: DECIDED NOT TO CLAIM NOW (updated 2026-11-26).** The owner answered No: do not claim issue 489 now. Issue 489 is open and unassigned. Its precondition (issue 488) is closed and deployed (PRs 493 and 518 merged); the owner decisions of 2026-11-10 are recorded on the issue. Issue 487, the framework it feeds, is open. Whether the harness files were already updated to the new panel is UNVERIFIED.
**Question:** claim it, and when?
**My recommendation:** after D-10 (D-11 is superseded), since it touches the same evaluation framework.
**If GO:** I claim #489 with `/sc:issue --claim 489 --pipeline none`.
**Owner answer:**
**Coordinator reply:**

### D-23 Issue #517 (GLM thinking error stops a whole tier)
**Status: DONE (updated 2026-11-26).** Issue 517 was closed on 2026-11-26 by the coordinator on the owner's approval. Earlier state: Option 2 (skip a model that rejects the effort, for that request only, no cooldown) shipped in PR 865, merged 2026-11-26 and on integration. Live check of the fix path done 2026-11-26 (spare-port proxy from the PR branch, real gateway: medium effort skipped to the second model, high effort answered by the first, not parked; PR 865 comment). Issue 517 was open and assigned to the owner until then. Whether option 3 (gateway fix) is still wanted was not answered on the record. The text below is historical.
**Source (historical):** main checkout `.dev/issues/517/issue-body.md:91`. A tier whose first model always thinks fails every request with the default effort and never moves to the next model. PR #516 only worked around this for the `issue-worker-t3` agent.
**Options:** (1) retry with effort `low`, no model parked; (2) move to the next model without the one-hour park; (3) fix at the gateway. The document recommends not a plain "switch" rule; whatever is chosen must never park the model.
**My recommendation:** option 1 as the first fix, option 3 as the real fix.
**If GO:** I claim #517 with `/sc:issue --claim 517 --pipeline none` and start a plan.
**Owner answer:**
**Coordinator reply:**

### D-24 Do the Muse models answer as the model they are labelled?
**Status: CLOSED (updated 2026-11-26).** The owner said to use the models' own answers as confirmation; the gateway operator check is dropped. The owner said yes on 2026-11-26 to the check; the coordinator ran the check read-only through the gateway (one tiny message per model, a few cents). Result: the gateway echoes the asked model name in every reply, so that field proves nothing. The models' own answers: `muse-wonder-1.0` "I am Muse Wonder, made by Meta"; `muse-spark-1.3` "Muse Spark, built by Meta"; `muse-wonder-full-1.0` "Muse Wonder, created by Muse"; `muse-ember-1.0` "Muse Ember, made by Anthropic" (it only answered after a 3,000-token limit because it thinks first). So no model answered as a different named model (the earlier evaluation run where wonder answered as `gpt-6.1-terra` did NOT reproduce on one probe), but self-reports are not proof of the real model and the vendor claims differ. The gateway's model-info address returned 404, so the real routing could not be read; proof would need the gateway operator's routing list. Before this check: no result of a completion check on the Muse models was recorded on integration. The provisional default review panel `wonsol` (PR 623) uses `muse-wonder-1.0` and `muse-ember-1.0` seats, so the question now bears on that default. It also still gates D-20; D-11 is superseded. Recommendation unchanged: have a read-only worker send one tiny completion to each Muse model and report the answering model name (no credentials printed). Cost is a few cents (one tiny completion per Muse model); the coordinator can run it on the owner's go.
**Facts:** in one evaluation run, `muse-wonder-1.0` answered as `gpt-6.1-terra`. For `muse-ember-1.0` the gateway only lists it; nobody has made a completion call (reported). Routing is not ours to change.
**Question:** have a worker send one tiny completion to each Muse model through the gateway and report which model name comes back?
**My recommendation:** yes. It costs almost nothing and gates D-11 and D-20.
**If GO:** I start that read-only worker (no credentials printed).
**Owner answer:**
**Coordinator reply:**

---

## Part D. Issue watcher, guard and claim pipeline

### D-30 Issue watcher rollout, issue #450
**Status: SUPERSEDED, rollout done; Q20 answered (updated 2026-11-26).** Issue 450 was closed on 2026-11-24 at the owner's request: the watcher is live and enabled on the owner's host, the cron entry is installed, and the automatic first-run check replaced the manual shadow, lock and restart tests. As of 2026-11-26 the ship gate is open (PR 851, on master through PR 856); when 450 closed on 2026-11-24 it was still closed. Leftovers named in the closing comment: a stale status line in `docs/designs/issue-watcher.md`, a self-contradiction in `docs/designs/issue-watcher-setup.md` (section 14.1 against section 17), and the never-written live-test record with 20 assumed fixtures (said to be tracked in issue 717, not rechecked). Q20 (who owns the watcher folder and its sessions per day, see D-51) was answered on 2026-11-26: the owner answered "Me"; the owner (login ironbelly) owns the watcher folder and its sessions. The text below is historical.
**Facts (2026-11-15):** only you can do these (no agent may): the live test, the shadow run, the lock test, the restart test and the cron install. `enabled` stays `false`. `docs/designs/issue-watcher-live-test.md` does not exist on master. The accepted "permission checks off for the first test session" may not cover the second agent that the claim now starts (document says "not confirmed"). The review-and-approval flow (plan posted on the issue, assignee asked to approve) is still "to be designed".
**Question:** who owns the watcher folder and its up to 6 sessions a day (this is Q20 in D-51), and when will you run the checklist?
**My recommendation:** name an owner (Q20 option 1), then follow the checklist in section 16 of `docs/designs/issue-watcher-setup.md` in order.
**If GO:** none; the steps are yours.
**Owner answer:**
**Coordinator reply:**

### D-31 Switch on the refusal for a missing pre-push guard (L2)
**Status: STILL OPEN, PENDING OWNER (updated 2026-11-26).** The owner approved the entry as written on 2026-11-26; a supervised worker is running the second-layer refusal test in a scratch repository (worktree `l2-refusal-test`); `IR7_REFUSE` stays off until the owner approves in chat after the result. `IR7_REFUSE` is still `False` (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:859`). Issue 442 is open. The L2 layer merged in PR 469 (2026-11-10); the runbook and an older results file are on integration (PRs 677 and 685). The observations that gate the watcher were run on 2026-11-25 and their evidence is on integration (28 files under `.dev/launch-level-observations/evidence/`, committed by PR 851): OB-H1 items 1 and 5, OB-H2 (a real claim of issue 827), OB-H3 runs W, F and FS (issues 829, 841, 842) and OB-CTX runs A, B and C. So the "OB-H2 FAIL on record" in the older results file is superseded, and PR 851's opening of the ship gate matches the gate rule (its four required items: OB-H1 items 1 and 5, OB-H2, OB-H3). Still NOT observed (listed in PR 851): OB-H1 items 2, 3, 4 and 6 to 9, `/clear`, auto mode, persistent cwd, PID reuse, the Task, Workflow, RemoteTrigger and MCP push-class tools, the L2 pre-push hook's own refusal, and a real merge conflict through pr-submit; the L2 refusal was never seen live because L1 always refused first. Open, PENDING OWNER: who finishes the remaining observations, and when `IR7_REFUSE` is switched on. The facts below are from 2026-11-15 and partly stale.
**Facts (2026-11-15):** `IR7_REFUSE = False` on master. The refusal stays off until the #442 observations pass and you approve separately. The 12-item observation runbook (`.dev/issues/442/handoff-runbook.md`, worktree `issue-442-runbook`) needs a person at a real terminal, and no results file exists. A line in it says the L2 layer is not built, which is stale (it merged in #469). The related governed-claim checks OB-H1 item 1, OB-H2 and OB-H3 had not passed at the last record (2026-11-08); anything later is UNVERIFIED. The implement ledger for #442 stopped on 2026-11-09 (task 5 blocked at retry 3).
**Question:** will a person run the runbook, and is the stalled #442 work abandoned or to be resumed?
**My recommendation:** run the runbook before any governed claim is used on a real issue; resume #442 only after that.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-32 Claim-handoff plan (worktree `claim-handoff-b`)
**Status: DONE (checked 2026-11-26).** See the update line below. The text between is historical.
**Source (historical):** `.dev/tasks/to-do/TASK-WF-planDecision6BFo-20261114-174909/`.
**Open:** which GitHub issue (written by you) should real recorded fixtures use (the answer goes in `tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md`)? Do you give the separate go to run Plan A with `/sc:implement`? Who runs and records the first live test (Plan B task 20, which has 11 PENDING facts)? The revised 19-task plan was reviewed only partly (the Tier 2 merge was not a real debate); re-run `/sc:reflect --mode pre --tier 2` with the advocate dispatch?
**My recommendation:** re-run the review first, then give the go.
**If GO:** I start the re-review worker only.
**Owner answer (historical):**
**Coordinator reply (historical):**
**Update 2026-11-26:** Plan A merged as PR 584 and Plan B as PR 591 (both 2026-11-17); the zero-setup watcher followed in PR 707 (2026-11-20). Owner input O-1 was given: issue 452 (`tests/issue_pipeline/fixtures/recorded/OWNER-INPUT.md`). The first live test runbook (`docs/designs/issue-pipeline-fu1.md`) has 11 recorded facts (a to k) plus the closing line "RUN BY OWNER: ironbelly", and no PENDING line; the recorded values are UNVERIFIED. PR 700 rolled back PRs 681, 682 and 684 (the issue 655 orchestrator build, including the retirement of the old plan-approval gate); Plan A's approval core is still present (`tests/issue_pipeline` has 18 files on integration). The re-review question is moot. The worktree `claim-handoff-b` no longer exists.

### D-33 Leftovers from issue #443 (not blocking)
**Status: DONE (updated 2026-11-26).** Issue 879 was filed for the leftovers; two are confirmed in code (the test helper copies the whole real environment, and the launcher treats every return code 1 as a refusal); the flaky-test item was linked on issue 352. Earlier state (checked 2026-11-26, before the filing): issue 443 is closed (PR 453). The xdist flake is already tracked in open issue 352. `_real_launch` is still in `tests/unit/test_ccsession_tiers.py` (line 1915); whether it still leaks test environment, and whether `ccsession` still treats every return code 1 as a refusal, are UNVERIFIED (the old line reference no longer matches). No issue exists for these leftovers. Owner question (answered by the filing): file one low-priority issue for the three leftovers, or fold the xdist item into 352 and drop the rest?
**Facts (from the deleted worktree's notes, 2026-11-15):** a 1-in-176 xdist failure (class of #352, still open), a test-environment leak in `_real_launch`, and `ccsession:985` treating every return code 1 as a refusal. The 30 CI repeat runs were never done.
**Question:** file one issue for these?
**My recommendation:** yes, one low-priority issue.
**If GO:** I file one issue with `/sc:issue --create` (feature, quick depth).
**Owner answer:**
**Coordinator reply:**

---

## Part E. The `--unattended` flag

### D-40 Open items after PR #508
**Status: DECIDED, FIX IN PROGRESS (updated 2026-11-26).** The owner approved on 2026-11-26: no new live check; the developer guide fix is being made in a PR by a worker (worktree `dev-guide-fix`). Earlier state (checked 2026-11-26): issue 507 is closed and PR 508 merged (2026-11-11). Command files with an Unattended mode section on integration: 23, and they match the 23 keys of `UNATTENDED_EXPECT` exactly. The commands the entry named as not yet converted (review-translation, cli-portify, tdd, improve, tasklist) have no command file on integration: they were removed on purpose by PRs 621, 627, 629, 632 and 650, so the five-gate items for them are closed, not pending; cli-eval, reflect, cleanup and task are converted. Formerly pending: (1) the second-phase live check (no recorded answer), and (2) the docs fix to the developer guide (`docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`): lines 385, 1091 and 1138 say to add a command name to `UNATTENDED_COMMANDS`, but `tests/skills/test_worker_contract.py:746` derives that set from `UNATTENDED_EXPECT`, so the maintainer must add an entry to `UNATTENDED_EXPECT`; line 1138 cites `test_no_command_has_unattended_mode_section_after_p0`, which does not exist (the check is `test_unattended_sections_match_the_listed_commands`); line 976 says 28 converted commands but there are 23 (28 minus the five removed commands). Related open issues: 733 (implement) and 734 (spec-panel-stoprule).
**Facts (2026-11-15, partly stale):** issue #507 is closed and PR #508 merged on 2026-11-11. Still open for you, from the workspace-image team's orchestrator's analysis (unverified by me): the five gates that turn a person's check into a caller input (review-translation `--context`, cli-portify `--resume`, cli-eval W3, reflect `--remediate`, tdd); whether `cleanup`, `improve`, `task`, `tasklist` and `cli-eval` are held out until the second-phase live check passes; new evaluation suites for the second-phase commands (a follow-up). A Low review finding was left open: the developer guide still names the removed `UNATTENDED_COMMANDS` and removed tests (lines 394, 1091, 1138).
**My recommendation:** hold those five commands out until the live check passes; fix the Low finding in a small docs PR.
**If GO:** I start a worker that fixes the stale developer-guide lines and opens a PR.
**Owner answer:**
**Coordinator reply:**

---

## Part F. Observer, orchestrator TUI and design records

### D-50 Observer release 3 and the direction record
**Status: DECIDED, PARKED (updated 2026-11-26).** The owner approved on 2026-11-26: park release 3; the three items (write-back, the licence opinion and TUIBBS as the staff platform) are deferred with triggers (the triggers were not given to me; UNVERIFIED). Earlier state (checked 2026-11-26): a dated owner direction record exists on integration (`.dev/issues/409/owner-direction-record-20261116.md`, 2026-11-16): fallback date not needed; order worker list first, then questions, third screen later; tool authorized to run and read the real system; Python and name decisions confirmed. It was recorded through PR 577 (merged 2026-11-17); PR 598 (2026-11-17) kept question text on screen only. Issue 409 is now the dashboard issue (open); remaining work is tracked in issue 706. The owner corrected the dashboard goal on 2026-11-25: the dashboard replaces direct talk to the coordinator; long conversations stay in the coordinator; a later brainstorm covers a narrow orchestrator plus separate conversation agents. So the undecided items belong to that rework, not to the old release plan: write-back from the BBS (a future release, blocked on a data source Orca does not provide), the licence opinion and TUIBBS as the staff platform (design item CD-12, "No Go or TUIBBS reader is built"). No owner decision on them is recorded (searched integration files and issues for TUIBBS, "BBS licence" and write-back). The Medium finding on PR 514 (recount of an old evicted question) was fixed in the branch commit `2083db2ae`, squash-merged with PR 514 (2026-11-12), except for a documented residual: an older evicted question that returns can be counted again (`src/superclaude/cli/observe/questions.py`, shortcut comment at lines 44 to 47). The owner accepted it; it is not tracked in issue 706 (searched its body only; UNVERIFIED beyond that). The text below is the 2026-11-15 entry.
**Source (2026-11-15):** `.dev/issues/409/bmad/spec-orca-observer/release-gates.md:10, 20-34` and `.dev/issues/409/owner-decisions-20261108.md:17`.
**Open:** the dated "direction selected" record and what "production integration" means. Without it release 3 cannot start. Two readings are at lines 31-32; the stricter applies until you say. Also undecided from 2026-11-08: write-back from the BBS, the licence opinion, and TUIBBS as the staff platform. Issue #409 stays open. The Medium review finding left open on #514 (a capped list can recount an old evicted question) was accepted by you; recorded here only.
**My recommendation:** write the direction record now (the orchestrator-TUI notes recommend option 1, 68%).
**If GO:** none; the record must be written by you.
**Owner answer:**
**Coordinator reply:**

### D-51 Orchestrator-TUI alignment questions (Q7 to Q41)
**Status: MOSTLY ANSWERED (checked 2026-11-26).** The question list is on integration (`.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/`, PR 587) and was updated through 2026-11-17: Q7, Q8, Q13, Q14, Q15, Q16, Q19, Q24, Q29 and Q41 answered; Q30 overtaken (PRs 577 and 586); Q20 and Q22 deferred. Owner actions done: Plan A (PR 584), the fixtures issue (452), Task 16 (PR 583), the first live test run by the owner. Q20 was answered on 2026-11-26: the owner (login ironbelly) owns the watcher folder and its sessions (same as D-30). Still open, PENDING OWNER: Q22 stays deferred by the owner's decision of 2026-11-26 (stale-file age; whether a `snapshot.json` reader exists is UNVERIFIED); separate grants for GitHub posts (UNVERIFIED); and the wording "private fork" in `CLAUDE.md` lines 43 and 47, which says private fork while the repository is public today; whether it is right depends on the owner's decision to make the repository private, so fix it only after that decision. The text below is the 2026-11-15 entry (historical).
**Source (2026-11-15):** `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/open-decisions.md` (untracked, in worktree `issue-339-orchestrator-mode`). It gives three options each with a recommended one and a confidence. None has an answer in `owner-answers.md`.
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
**Status: DECIDED, DEFERRED (updated 2026-11-26).** The owner said defer on 2026-11-26. Earlier state (checked 2026-11-26): the source folder is on integration; PR 434 (2026-11-08) shipped the v1 liveness rules. Issue 423 (Orchestrator v2) is open. No measurement of the restart window and no decision on whether a v2 monitor may live in package code (Q6) is recorded on integration (searched docs, `.dev/issues` and the TUI alignment folder). The v2 build still waits on both. The 2026-11-25 dashboard goal correction may change the v2 plan; that link is not verified.
**Source (2026-11-15):** `.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/merged-requirements.md:804-834`.
**Open:** the restart window (1 per 60 minutes is unmeasured); whether a v2 monitor may live in package code (Q6); the v2 build waits on both. The reply-acknowledgement rule and the person-directed cancellation rule were answered on 2026-11-07 and shipped in #434.
**My recommendation:** measure the restart window first; it is cheap.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-53 Orca-refactor evaluation
**Status: DECIDED (updated 2026-11-26).** The owner accepted the debate result as it stands on 2026-11-26 (keep brainstorm's own sub-agent fan-out; separate processes come from a coordinator session). Earlier state (checked 2026-11-26): the evaluation is on integration (`.dev/brainstorms/20261111-orca-orchestrator-refactor-eval/`, 12 files). Its verdict is to keep brainstorm's own sub-agent fan-out and get separate processes from a coordinator session running `/sc:brainstorm --unattended`; no owner decision on it is recorded (searched docs, issues and the TUI alignment folder). `/sc:brainstorm` now has an Unattended mode section; whether it is used that way is UNVERIFIED. C-002, C-004, C-008 and C-009 and the cold-start measurement remain open.
**Source (2026-11-15):** `.dev/brainstorms/20261111-orca-orchestrator-refactor-eval/adversarial/merged-output.md:8-12, 47, 79`.
**Open:** accept "do not make brainstorm call Orca; use a coordinator session for separate processes"? Points C-002, C-004 (two routes for non-Claude models, leaning Route 1), C-008 and C-009 were left open. The document recommends measuring worker cold-start time and cost before any decision to use workers.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-54 Dashboard research choices
**Status: SETTLED (updated 2026-11-26).** The owner answered on 2026-11-26: Python with Rich. The three other points stay tracked with issues 409 and 706. Earlier state (checked 2026-11-26): The framework point is settled in practice for the shipped observer (Python with Rich: `src/superclaude/cli/observe/commands.py:20` and `render.py:18-20` import `rich`; `pyproject.toml` lists `rich>=13.0.0`; no Textual, Bubble Tea or Ratatui in `src`), and the owner confirmed the Python decisions on 2026-11-16 (`.dev/issues/409/owner-direction-record-20261116.md`); the dashboard rework of 2026-11-25 has no recorded framework decision of its own (UNVERIFIED). The report is on integration and says "No user decision is needed to finish these design deliverables. Implementation and adopting a particular fork remain separate decisions." Still open, tracked with issues 409 and 706: where dashboard-only seen, claimed and snoozed state lives, how to list every decision completely, and the required terminal sizes (UNVERIFIED whether the existing rendering size cases settle the last one).
**Source (2026-11-15):** `.dev/research/orca-dashboard-20261105/REPORT.md:221-234, 256`. Framework (Bubble Tea with Lip Gloss, Textual, or Ratatui), where dashboard-only state lives, how to list every decision completely, and terminal sizes. The report says none is needed to finish its design deliverables. Likely moot because `superclaude observe` shipped in releases 1 and 2 (UNVERIFIED).
**My recommendation:** mark it moot.
**If GO:** none.
**Owner answer:**
**Coordinator reply:**

---

## Part G. Model defaults, research and leftovers

### D-60 Issue #462 (Opus 5.5 default in orchestrator-spawned sessions)
**Status: CLOSED, NOT PLANNED (checked 2026-11-26).** Issue 462 was closed by the owner on 2026-11-17 (not needed now). The fix attempt is kept on the remote branch `ironbelly/issue-462` (commit `00db7c7b5`; the earlier commit `91af19e56` is on that branch); PR 483 was closed on 2026-11-10 and not merged; the worktree no longer exists. Reopen the issue if the work is wanted later. The question and lines below are historical.
**Facts (2026-11-15):** PR #483 was closed. Fix commit `91af19e56` (plus a format commit) exists only in worktree `issue-462`, with no remote branch. The diagnosis stopped at confidence 0.30. Either the setup commands explicitly asked for `claude-opus-5-5`, or an owner decision on later pins is missing (`REPORT.md:30,62` in that worktree).
**Question:** can you give one real example of an unqualified launch that landed on Opus, with its full command? Or give a direct instruction on the pins?
**My recommendation:** keep implementation paused. Do not hardcode Tier 1b as a universal default.
**If GO:** none.
**Owner answer:**
**Coordinator reply:**

### D-61 Issues #463 (model and effort router research) and #470 (research pipeline block)
**Status: CLOSED, NOT PLANNED (checked 2026-11-26).** Issue 463 was closed by the owner on 2026-11-17 (not needed now; no research was completed); the halted research task and its card exist only on the remote branch `ironbelly/issue-463` (commit `846e03f21`), not on integration (0 files). Issue 470 was closed as not planned on 2026-11-24: the research-only workflow it covered was removed by PRs 650 and 656 and release PR 658 (all merged 2026-11-18); it was closed as superseded by removal, not fixed; the old bug is not claimed to be corrected (closing comment). Reopen 463 if the work is wanted later. The options and questions below are historical.
**Facts:** #463's research task halted at its work-splitting check. Options in `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/OPEN-DECISIONS.md:19-41`: (1) one more mechanically built correction plus one final review; (2) relax the task's rules; (3) set it aside for a smaller `/tech-research`; (4) stop. The document recommends option 1, with option 3 as the alternative. Also: ratify that the executor launched all workers itself because the named coordinator terminal no longer exists (document: yes); who is "Jev" (issue #553's body calls it the TypeSafe System One decision model and the blocker spec calls it the TypeSafe model `jev-1.14.0` that judges supplied text only; both are written descriptions, not your answer, and what it can do for #463 stays unresolved); what happens to six workers still `unverifiable`. #470 stays on hold, as you ordered.
**My recommendation:** option 3. #463 should not start before #470's plan unblocks it.
**If GO:** none yet.
**Owner answer:**
**Coordinator reply:**

### D-62 `.claude-audit/` in the main checkout
**Status: DONE (updated 2026-11-26).** The folder was copied to `~/workspaces/worktree-archives/IronClaude/claude-audit-20261126` (77 files, tree hash equal) and the original was deleted. Earlier state (checked 2026-11-26): the untracked folder `.claude-audit/` still existed in the main checkout (all 77 files dated 2026-11-05; 0 tracked on integration). Counts re-checked 2026-11-26 and unchanged: 65 unchecked boxes, 0 checked, in 26 reports in `pass1/`; reports 15, 27 and 29 to 47 are missing; `progress.json` not examined. My recommendation is unchanged: discard it and run a fresh audit if one is wanted; deleting is the owner's call.
**Facts (2026-11-15):** 65 unchecked "Need Decision" boxes in 26 batch reports; batches 15, 27 and 29 to 47 are missing; `progress.json` is stale. The question is which stray repository files to delete.
**My recommendation:** discard this audit and run a fresh one when you want it; the batches are incomplete.
**If GO:** none; deleting is yours.
**Owner answer:**
**Coordinator reply:**

### D-63 Follow-ups from the deleted `mcp-audit` worktree
**Status: DONE (updated 2026-11-26).** Issue 878 was filed for `agent.md`. Earlier state (checked 2026-11-26): still true: `src/superclaude/commands/agent.md` has no opening `---` (line 1 is `name: sc:agent`; it has the closing one) on integration and master; no issue exists for it; fixing it may rename the slash command. Moot: `load.md` and the `task-builder` skill no longer exist on integration (0 files). The tool-less web-research wording in five skills could not be found and stays UNVERIFIED (searched the skills and commands for "tool-less", "no web tools", "without web", "no tools" and "without tools": only an unrelated line in `ccsession-tag/MODEL-TIERS.md`). Recommendation (done by issue 878): file one issue for `agent.md`.
**Facts (2026-11-15; its findings file went with the worktree; this is the summary I kept):** the file `agent.md` has malformed front matter (no opening `---`; master's still starts with `name: sc:agent`), and fixing it may rename the slash command, so it needs its own issue. The same tool-less web-research wording appears in five other skills. `load.md` has drifted. `task-builder` line 1208 needs a look.
**My recommendation:** file one issue for `agent.md` and one for the wording drift.
**If GO:** I file those two issues with `/sc:issue --create` (bug, quick depth).
**Owner answer:**
**Coordinator reply:**

### D-64 Follow-up left by the deleted `codegraph-wording` session
**Status: CLOSED (checked 2026-11-26).** PR 513 merged 2026-11-12 (31 files). The session's note about two stale sentences is probably the two files PR 513 itself corrected (`sc-graph-protocol/SKILL.md` and the developer guide, which "no longer say the MCP status needs no guard"; `sc-graph-protocol/SKILL.md` on integration has no "no guard" wording left); the match to the entry is UNVERIFIED because the session's note is gone. No open follow-up was found. The question and lines below are historical.
**Facts (2026-11-15):** that session's last note recommended that the coordinator fix "two stale sentences" in a follow-up so that guide rule 7 and two files agree. The session and its report were removed with the worktree, so I do not know which two sentences. The change itself merged as PR #513.
**Question:** do you want me to dig it out of the merged PR and its review comments?
**My recommendation:** no, unless you remember the file names; the cost is higher than the value.
**If GO:** I read PR #513's files and review comments and report what the two sentences are.
**Owner answer:**
**Coordinator reply:**

### D-65 Jev plugin pin and upstream monitor, issue #553
**Status: DECIDED, PR IN PROGRESS (updated 2026-11-26).** The owner decided on 2026-11-26 to add Jev to the EXISTING central upstream monitor workflow, with no separate workflow. Fact: the central monitor (a workflow in the private workspace-image repository, daily at 04:23 UTC, Renovate) already follows plugin pins in `src/superclaude/cli/user_settings_defaults.json` through a regex on entries shaped like the Ponytail entry (description "<name> vX.Y.Z, pinned by IronClaude", source github, repo, ref tag, sha); a Jev entry of that shape is monitored with no new workflow, the weekly-check cadence is replaced by the monitor's daily run, and that repository is readable. Read-only research of 2026-11-26 (report `~/workspaces/worktrees/IronClaude/Coordinator/.dev/reviews/jev-pin-research-20261126.md`): upstream `typesafe-ai/skills`, newest tag `v0.6.2` = commit `302eea662c54bca6730873fe245bec1d69ebc23d`, MIT, no GitHub Releases (tags only). The plugin is Markdown and two JSON manifests only: no hooks, no code, no base URL, no network call of its own; the only data path is a live test request gated by the user's permission (SKILL.md lines 213 to 218). So answering OD3 is NOT needed before installing the skill text; it is needed before any IronClaude feature calls the Jev API with private text. The plugin id is `typesafe@ironclaude`, not `typesafe@typesafe-ai`. Any earlier line saying the issue 553 plugin sends data was about the separate jev-pruner and fast-jev tools (issues 574 and 575). A worker (worktree `typesafe-pin`) is making the PR that adds the pinned entry in `src/superclaude/cli/user_settings_defaults.json`. Earlier state (checked 2026-11-26): the owner decided to pin a release tag (chat 2026-11-16; repeated on issue 553 on 2026-11-17: install the TypeSafe plugin pinned to a tag; pick the reviewed release tag, pin it in the default install, and have the upstream monitor watch for new tags). Issue 553 is open and unassigned; no tag is pinned and no pull request exists. The coordinator's 2026-11-16 lookup of the upstream repository found tags `v0.6.2` and `v0.5.7` and no GitHub Releases: the 2026-11-16 reading, not rechecked in this walk. The 2026-11-24 backlog review lists the next step: resolve the tag and its 40-character commit and review the skill text at that commit before pinning. Settled by the 2026-11-26 findings above: the monitor cadence (daily) and the data-sharing question for the skill text (OD3 is needed only before a feature sends private text). Whether the monitor follows a tag that has no GitHub Release is UNVERIFIED (tags only). The local package `.dev/issues/553/` is not on integration (0 files) and its worktree is gone.
**Source (2026-11-16):** the owner's answer packet of 2026-11-16, issue-based split (pasted in chat; its branch mapping is not verified). Issue #553 ("Install the TypeSafe Jev agent skill plugin by default and have the upstream monitor watch it") is open. Its local package is in worktree `brainstorm-reflect-panel`, folder `.dev/issues/553/` (untracked, on no branch).
**Decided:** use a pinned Jev version, and update the upstream monitor to track Jev upstream.
**Still unspecified:** the exact pin (a reviewed release tag and commit; whether the Jev repository has release tags is "Not known yet" in #553's body), the monitor configuration and cadence, data-sharing approval (D-13, OD3) and evaluation access. #553's pinned route is an `ironclaudeMarketplace` entry that the private workspace-image repository's Renovate configuration watches, and its body expects no change there. Whether "update the upstream monitor" also means a change there is not stated.
**Authorization:** documentation only. Nothing is implemented, installed, configured, stored, sent or posted to GitHub.
**Recorded in:** `.dev/issues/553/issue-body.md` and `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/00b-jev-default-install-description.md`, both in `brainstorm-reflect-panel`. The second file is staged there, not committed.
**Question for you:** which Jev release tag and commit should be pinned, and who reviews it? ANSWERED 2026-11-16 (see below).
**Owner answer:** (from chat, 2026-11-16) pin the latest release tag and commit. Later updates are reviewed through the central upstream monitor. If release tags are not posted, start unpinned and watched.
**Coordinator reply:** Recorded on 2026-11-16 in the two files above and in D-13 and D-61, and the second answer in the same two files. A read-only lookup of `typesafe-ai/skills` (about 17:13 UTC, not independently reviewed) found git tags `v0.6.2` (commit `302eea662c54`, the same version as the local plugin cache) and `v0.5.7` (commit `65a39f393687`), and no GitHub Releases (the releases API answers 404). I read "release tag" as a git tag, so the pinned route applies and the latest tag is `v0.6.2`. You confirmed on 2026-11-16 (chat) that release tags or plain tags suffice, so that reading stands and the unpinned fallback does not apply. Nothing is pinned or implemented. Also not decided: whether the central monitor can follow a tag that has no GitHub Release (UNVERIFIED, workspace-image side).

### D-66 Eval coverage gate, issue #562 (decision recorded, not implemented)
**Status: DECIDED, PARKED, NOT IMPLEMENTED (updated 2026-11-26; the owner said no action).** The decision recorded on 2026-11-16 stands: allow explicitly isolated component evaluation suites to avoid unrelated installed-hook coverage, with a separate installed-hook integration check. Issue 562 is open, unassigned and low priority (P3); it was parked by Clay on 2026-11-16 (low priority, backlog; comments of 2026-11-17 and 2026-11-18) and kept parked by the 2026-11-24 backlog review, until the eval harness is used again. No pull request touches the coverage gate; `.dev/issues/562/` has 0 files on integration. Implementation remains unauthorized. The unresolved ledger-replacement and per-seat items are unchanged; whether the five documents listed below changed is not rechecked in this walk.
**Source (2026-11-16):** the same answer packet. Issue #562 ("Should installed hook coverage reject unrelated packaged eval suites?") is open as a question. I found no document for it in any IronClaude worktree, so no worktree owns it.
**Decided (decision only):** allow explicitly isolated component evaluation suites to avoid unrelated installed-hook coverage, while maintaining and verifying a separate installed-hook integration check that catches mismatches.
**Owner's facts:** the recorded failure was the coverage preflight, not a demonstrated broken hook. Suites lacked an expected tool call matching an installed MCP PostToolUse pattern, and the guide identifies an Auggie pattern. It is not established that ordinary workflow or implement execution was blocked.
**Authorization correction:** Ryan's "proceed with that" meant record the decision, not implement it. The earlier implementation reading was withdrawn, and that attempt was stopped before any code or tests changed. Implementation is not authorized.
**Documents that describe today's gate and change only if implementation is authorized:** `src/superclaude/skills/sc-cli-eval-protocol/refs/eval-contracts.md:54-62`, `docs/guides/suites-guide.md:623`, `docs/user-guide/eval-pipeline.md:254`, `docs/testing/v5.0.0/user/D15-eval-harness.md:448,543`, and the docstring in `src/superclaude/cli/eval/coverage.py:3-11`. None was edited.
**Unresolved, from the packet:** the conditional ledger replacement (pending developer evidence) and the per-seat future design and exit-code numbers. The packet does not say which document each belongs to, so none is mapped.
**Owner answer:**
**Coordinator reply:** Recorded on 2026-11-16 in this item only.

### D-67 Evaluate fast-jev-compaction, issue #574 (testing on hold)
**Status: DONE, REJECTED (checked 2026-11-26).** The hold recorded on 2026-11-16 was lifted the same day (owner: use Jev directly on the public repository; recorded by the coordinator, no verbatim wording kept). Issue 574 was run and closed on 2026-11-16 (22:44 UTC) with the verdict REJECT: K4 and K11 failed. Live Jev kept 0 of 57 planted tool-result facts against a bar of 0.95 (0 of 42 development, 0 of 15 held-out fixtures), and failure handling (K11) was clean in 14 of 17 injected cases. Only the library route was measured; the plugin and host layer were not tested. The package `.dev/issues/574/` is on integration (9 files). Issue 576 (local inference node) was closed as not planned on 2026-11-17. The issue titles of 574 and 575 still read "(HOLD: no live testing yet)" although both issues are closed with a REJECT verdict. The text below is the 2026-11-16 entry and the open list no longer applies (historical).
**Source (2026-11-16):** your answers of 2026-11-16 to my question about the two drafts (in chat). Issue: https://github.com/IronbellyOrg/IronClaude/issues/574 (open, created 2026-11-16, type Feature, label `enhancement`, Complexity Simple). Its package is `.dev/issues/574/` in the main checkout (untracked).
**Decided:** sending all conversation data over the wire is not acceptable for now, so there is no install or live test until a potential alternative judge is found and assessed (for example a decision model from Anthropic, or a local model on premises on a 3090 or 4090 GPU). Live runs, once allowed, use public fixtures only. Budget $50.
**Posted:** the issue carries a HOLD banner and a runbook section 0 that holds stages S2 to S7 and allows reading the repository, document-only steps and an alternatives study (stage A0). Nothing was installed or run, and no key was used. No "blocked" label exists in the repository and I did not create one.
**Open:** which alternative to study first and who runs A0; whether the risk and legal assessment you required for #575 also applies here; whether the $50 covers Jev credits and downstream model calls together (I read it that way).
**My recommendation:** run A0 first. It is documents only.
**If GO:** I start one worker to write the A0 alternatives study for #574 and #575 together (read-only; no tool code run; no TypeSafe call).
**Owner answer:**
**Coordinator reply:** Recorded on 2026-11-16.

### D-68 Evaluate jev-pruner, issue #575 (testing on hold)
**Status: DONE, REJECTED (checked 2026-11-26).** The hold recorded on 2026-11-16 was lifted the same day (same reversal as D-67). Issue 575 was run and closed on 2026-11-16 (22:44 UTC) with the verdict REJECT: on text the model actually sees, needed-line retention was 0.00 against a 0.98 bar and false removal 1.00 against 0.02, identical to running with no plugin, because Claude Code 2.1.325 and 2.1.326 show the model only a 2 KB head of any Bash result over about 30,000 characters; repeatability also failed (0.912 over 5 fixtures and 0.853 over the 3 where Jev pruned anything, bar 0.90). Not done by the owner's decision: stages S5 to S8, the Codex integration and private data. Spend was about 2.43 dollars of the 50 dollar cap (figures as reported, prices unverified). It would be reopened by a host version without the 2 KB preview or a judge that scores noise below 0.1. The package `.dev/issues/575/` is on integration (9 files). The evidence files named in the verdict (`.dev/eval-workspaces/jev-pruner/results/`, report `S4-benchmark.md`) were in an evaluation worktree and are not committed there; they are not on integration (0 files under `.dev/eval-workspaces/jev-pruner/`). The issue title still reads "HOLD: no live testing yet" although the issue is closed. The text below is the 2026-11-16 entry (historical).
**Source (2026-11-16):** the same answers. Issue: https://github.com/IronbellyOrg/IronClaude/issues/575 (open, created 2026-11-16, type Feature, label `enhancement`, Complexity Simple). Package: `.dev/issues/575/` in the main checkout (untracked).
**Decided:** everything command related that the tool sends to Jev, including code, is a blocker at the moment, so testing is on hold. A proper risk and legal assessment is needed, with local models tested. Live runs, once allowed, use public fixtures only. Budget $50. Claude Code only: no Codex integration.
**Posted:** the issue carries a HOLD banner and a runbook section 0 that holds stages S2 to S8, with the hold lifted only when an alternative has been assessed and the risk and legal assessment is done, and then only by your written word on the issue. The Codex integration is out of scope.
**Open:** who does the risk and legal assessment and what it covers (the runbook suggests: what is sent, where it goes, retention and contract terms, and what a local judge can do instead); which alternative to study first; whether the $50 covers Jev credits and Claude usage together.
**My recommendation:** same as D-67: A0 first, then the assessment.
**If GO:** same worker as D-67.
**Owner answer:**
**Coordinator reply:** Recorded on 2026-11-16.

---

## Part H. This file

### D-70 Where does this file go next?
**Status: PARTLY DONE (checked 2026-11-26).** PR 859 (merged 2026-11-26) put this file on integration; it reaches master only with the next promotion from integration to master. This update of the file (the 2026-11-26 status lines) is a separate change; on 2026-11-26 the owner approved committing it and opening one docs pull request to integration. The text below is historical.
**Facts (2026-11-15):** the file lives on its own branch on the fork. No pull request is open.
**Question:** open a pull request to put it on master, or keep it as a branch?
**My recommendation:** keep it as a branch while you answer; open a PR when it is mostly answered, so master is not filled with a changing document.
**If GO (open a PR now):** I open one with `/sc:pr-submit --monitor 3`.
**Owner answer:**
**Coordinator reply:**
