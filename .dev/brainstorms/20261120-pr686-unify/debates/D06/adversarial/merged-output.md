<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (OURS) -->
<!-- Merge date: 2026-11-20 -->

# Recommended authority model (D06): authority for merging, script-started coordinators, reviewer hold

<!-- Source: Base (original, modified) - status line reworded to describe the merged output; conventions added; no repository change is implied -->
Status: merged output of the D06 adversarial pipeline (base Variant A, OURS), written as the recommended authority model. It is spec text only; nothing here is applied to any repository file, GitHub or Orca. Paths marked (master) are in the read-only export /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6). "D:nnn" is a line of `docs/designs/orchestrator.md` in the same export (the design merged by PR 681).

Conventions used below. "Narrows" is used where a gate lowers a risk and "closes" only where a named check exists; no such check exists yet. Every gate that is unbuilt or UNVERIFIED is marked "not shown to pass". "Owner DECISION" marks a choice that only the repository owner can make, in chat.

## The claim

<!-- Source: Base (original, modified) - coordinator start (depth 0, self-attested) per Change #6; validator wording per Change #4 -->
Authority over outward and irreversible actions stays with the person. A coordinator session is opened by a person, or is started at depth 0 (a terminal plus `ccsession`, never `worker-start`) by the owner's installed watcher under an authorization the owner recorded in chat; a launch-prompt authorization is self-attested, and the paper says so (see "Contract amendments" and "What it risks"). It acts outward only on the person's named instruction, never merges on its own initiative, and never runs `/sc:pr-submit` as an Orca worker. A reviewer that shows no activity is skipped inside the `/sc:pr-submit` loop. Approvals and goes are given in chat. A validator checks that a recorded answer is current and matches its question; it cannot prove who typed it (mechanism item 5). Where automation helps, it narrows the person's work (it prepares, checks and waits); it does not replace the person's go.

## The mechanism

<!-- Source: Base (original, modified) - items 1 to 4 unchanged; item 5 reworded as a stale-answer validator per Change #4 -->
1. The coordinator rules bind "an Orca coordinator session the person opened" (`src/superclaude/core/WORKER-CONTRACT.md:70` (master)). Every git and GitHub outward action happens "only when the user's instruction names that action, and confirms with the person at the moment of action" (:241). A `merge_ready` message "merges only on the person's instruction" (:108).
2. Publishing is separate from approving: "Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this" (:245).
3. PRs go "only through `/sc:pr-submit --monitor 3`, run in an ordinary top-level session as decision D3 states, never as a worker" (:244); `/sc:pr-submit` is on the never-as-worker list (:23).
4. In the PR loop a silent reviewer is recorded absent and ignored: "a reviewer that never shows activity is recorded absent ... and ignored for the rest of the run" (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:29-32` (master); table at :363-364; project CLAUDE.md:58).
5. Approvals live in chat, not files or relayed text (owner order 2026-11-17, memory `approvals-through-chat-never-files`; WORKER-CONTRACT D2: only the person gives a Ruling). <!-- Source: Variant B (CLAY), The mechanism item 4 and Cited fact 5 - merged per Change #4 --> A validator, Variant B's `superclaude orchestrator answer-check`, checks that a recorded answer has an entry, names the question key, names the head sha and is newer than the notice (D:694). It is a stale-answer validator only. It does not prove who typed the answer: the design's wake path types lines into the same terminal with `orca terminal send` (D:112), and a script knows the sha. Spoofed typing is therefore a residual risk (see "What it risks"). Whether the harness marks sent text differently from typed text is UNVERIFIED. `answer-check` is not built and is not shown to pass.

## Merge procedure

<!-- Source: Variant B (CLAY), The mechanism items 1 to 3, Cited fact 1 and Cited fact 9 - merged per Change #1 -->
This section is a requirement for a later build, not a present control. The gate it uses is Variant B's `superclaude orchestrator merge-gate`, which decides with the existing `superclaude.pr_submit` core and has a closed set of thirteen reasons (wave 6, D:578-583). No `merge-gate` exists in master, PR 686 or the branch `issue-655-pr-p` (Variant B's own admission). Until it is built, the person's go is the only control, and the gate is not shown to pass.

The gate is a read-only check that the person consults. A passing gate never triggers a merge. The person's go is required for every merge, in this section and in every other section of this paper.

### Steps

<!-- Source: Variant B (CLAY), The mechanism items 1 to 3 - merged per Change #1 -->
1. The orchestrator runs the gate, read-only.
2. It shows the full gate output to the person in chat: every reason, the open threads, the review state and the file-list result. The gate output belongs in front of the go because `gh pr diff --name-only` does not print `previous_filename`, so a rename out of `.github/workflows/` is invisible to a person reading that diff while the gate sees it (D:597).
3. The person types a go (see "The go: contents, expiry and reach").
4. The gate runs again immediately before the merge (D:588). The merge is refused if any gate reason, open thread, review state, base branch or draft state differs from what the person was shown.
5. `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>`, and never `--auto`, `--admin` or `--delete-branch` (D:118, D:586-590). `--match-head-commit` covers only the head sha. A new `changes_requested`, a thread opened after the gate, a flipped check, a moved base or a retargeted PR leave the sha unchanged and the pinned merge would still land; step 4 exists for that reason.
6. The orchestrator reads the PR state back. After a restart it reads the PR state first, so a go cannot cause a second merge (D:591).
7. <!-- Source: Variant B (CLAY), Round 2 hybrid gap on AU4a and AU7 (D:812, D:601) - merged per Change #9 --> The audit after the merge (AU4a, AU7; D:812, D:601) is kept even when a person gave the go, because it can find a merge the gate did not make.

### The go: contents, expiry and reach

<!-- Source: Variant B (CLAY), Round 2 rebuttal "Hybrid gaps" and Variant A Round 2 "Updated assessment", with probe INV-002, INV-004, INV-006 - merged per Change #2 -->
A go for a merge names all of the following:

- the repo, the PR number and the full 40-character head sha;
- the merge method, which the gate checks against the repo's `merge_method` or `release_merge_method` (the squash merge of release 6.1.0 (#658) was reverted by #662, D:118);
- the word "merge";
- the gate output it refers to.

It is typed in live chat after the gate output and is newer than that output. A live-chat go needs no second confirmation (WORKER-CONTRACT.md:241 ends "unless that instruction is in its live conversation"). It is recorded as an entry (repo, PR, sha, time). The go is a one-shot entry for one merge, not a standing grant.

The go has an expiry. The number of minutes is an Owner DECISION; no source gives it. After the expiry the go is void and the gate output is shown again. The go is also void on any head change and on any new gate reason. If the person does not answer, the question waits with no default (D:692).

The go is not shown to pass as a control. The expiry is not agreed, the recorded entry and the second gate run are not built, and nothing verifies that a person typed the go (see "What it risks").

### Gate reasons and what a go may override

<!-- Source: Variant B (CLAY), The mechanism item 1 and item 3, with probe INV-004 - merged per Change #2 -->
<!-- Source: Base (original, modified) - orchestrator correction after the merge: the thirteen reason names are added from D:582 (master); the merge-executor had only nine in its inputs -->
The gate is a closed set of thirteen reasons, named at D:582: `checks_failing`, `checks_pending`, `review_pending`, `review_stalled`, `review_none_present`, `threads_open`, `worker_not_done`, `head_moved`, `draft`, `not_mergeable`, `snapshot_incomplete`, `changes_requested`, `merge_safety`. The column says whether a go may override the reason.

| Reason | Go may override? |
|--------|------------------|
| `head_moved` | No. The go is void. |
| `draft` | No. |
| `not_mergeable` | No. |
| `snapshot_incomplete` | No. A missing or short file list fails closed (D:597). |
| `changes_requested` | Recommended rule: no, a hard refusal. Owner DECISION: whether it is a hard refusal or a go may merge over it. Until the owner decides, treat it as a hard refusal. The gate output must print which rule applies. |
| `merge_safety` | Only by a go that carries this reason's own question key (for example `merge_safety:<PR>:<head sha>`, D:694). The design (D:593) holds a merge-safety change until an explicit OK tied to that PR and head sha; this paper keeps that rule, and a recorded OK for a failing check never clears it (D:593). |
| `checks_failing` | Only by a go that carries this reason's own question key. |
| `review_stalled` | No. The owner sets `reviewers: none` for a repo with no review agent. |
| `review_none_present` | No. The owner sets `reviewers: none` for a repo with no review agent. |
| `checks_pending` | No. Wait until the checks finish. |
| `review_pending` | No. Wait until the listed reviewers finish. |
| `threads_open` | No. Open review threads are answered first. |
| `worker_not_done` | No. The worker's `worker_done` is required. |

### Windows

<!-- Source: Variant B (CLAY), Round 2 hybrid gap "Go window" and probe INV-006, INV-008 - merged per Change #2 -->
Three clocks are kept apart (INV-006):

- The 2-minute window runs from the second gate run to the merge call (D:587-588). It does not run from the gate output to the person's go, so the time taken to type a 40-character sha is not inside it.
- The 60-minute hold runs from the moment the final head's checks finish (D:580). The 60 minutes is a default, UNVERIFIED as the right number, and an Owner DECISION.
- The go expiry is a third number and an Owner DECISION (see "The go: contents, expiry and reach").

The loop's silence timeout is a different clock again: the loop declares a reviewer absent at `min(silence_timeout, timeout)` (`reviewers.py:390-391`). The merge-time hold does not reuse it. The 60-minute hold and the go expiry are not agreed and are not shown to pass.

## Silent reviewer

<!-- Source: Variant B (CLAY), Cited facts 2 to 4, with Round 1 shared assumption A-001, Round 2 Variant A item 2 and probe INV-005, INV-007, INV-008, INV-009 - merged per Change #3 -->
The skip rule stays in the loop. `/sc:pr-submit` is unchanged: it still records a reviewer that shows no activity as absent and ignores it for the rest of the run (SKILL.md:29-32, table at :363-364). The hold lives at merge time, in the gate's `review_stalled` and `review_none_present` reasons.

Why a merge-time hold is needed. The loop's absent state is sticky and clock-based: `codex_wait_outcome` returns absent when the peer has settled or elapsed time reaches `min(silence_timeout, timeout)` (`reviewers.py:390-391`), and SKILL.md:31-32 rebuilds it on `--resume`. `merge_wait` then uses only the reviewer that is done, so one done plus one absent reads clean or findings (`reviewers.py:414-419`). Absent is a clock or settled-peer outcome, not a finding that the reviewer is not installed (`reviewers.py:379-382`). The owner's memory records a Codex security review that posted minutes after its code review reported clean (memory `pr-submit-check-pr-open-before-push`, 15 days old, not re-verified).

The hold, as explicit steps:

1. Read the per-repo `reviewers` list, which the owner sets (`none` is allowed). It is a setting, not detected (A-005).
2. If the list is not `none`, request a review of the final head from each listed reviewer, then wait. This re-trigger is a required step because the loop never re-triggers or pokes an absent reviewer (SKILL.md:364, "no wait, no re-trigger, no poke"); without it the hold would wait for a reviewer nobody asked to review that head (INV-009). Whether Codex reviews on push or only on request is UNVERIFIED, which is why the step is explicit.
3. Re-poll the final head. Do not read the loop's sticky absent state.
4. Wait up to 60 minutes (default, UNVERIFIED, Owner DECISION), measured from the moment the final head's checks finish. If the repo has zero checks, that anchor does not exist (zero checks gives `clean` or `polling` forever depending on `expect_checks`, `ci.py:33-55`), so the clock falls back to the push time of the final head (INV-008).
5. If no listed reviewer shows activity, the gate raises `review_none_present`; if a listed reviewer does not finish within the bound, it raises `review_stalled`. Neither is overridable by a go. After the bound the question escalates to the person (D:138, D:1155), and nothing is decided by default.

Rules for the `reviewers` list:

- It is edited only on the owner's recorded word (INV-005). The design write-protects `merge_safety_files` and `grants` by `--answer-ref` (D:595) but not `reviewers`; this paper adds `reviewers`, including `none`, because one edit to `none` removes the hold.
- A list that names a reviewer the repo does not run stalls every PR for the full bound and then escalates (INV-007). The design records Augment alone on IronFlow PRs 1 and 3, Codex alone on IronOrca PR 11 and none on IronOrca PR 8 (D:138). The gate output must name the reviewer that did not answer so the owner can correct the list.
- `none` is a valid value. Requirement: under `none` the gate prints `reviewers: none` and raises neither `review_none_present` nor `review_stalled`. The design leaves this output undefined; it must be fixed before the gate is built.

What the hold narrows and does not close (INV-012). A reviewer never triggered on the final head, a review that lands after the gate and before the merge on the same head, a reviewer outside `augment` and `codex` (invisible to the gate), and a done review with an unreadable marker (read as `incomplete`, `reviewers.py:353-358`) all remain residual. The merge-gate, the re-trigger, the 60-minute hold and the reviewer lists are not shown to pass.

## Standing lists

<!-- Source: Variant B (CLAY), Round 2 "Remaining dispute" item 4 and Cited fact 5 (grants keys), with probe INV-011 - merged per Change #5 -->
A verb refuses any GitHub write that is not on a list the owner recorded in chat (`E-NO-GRANT`, D:696). The list holds only duties the owner recorded in chat. It never holds `pr.merge` or `issue.close`. A repo-level standing grant for either is not adopted: it is broader than a per-issue go and conflicts with WORKER-CONTRACT.md:245. The merge go is a one-shot entry (see "The go: contents, expiry and reach"), not a `grants` row.

| Action | How it is authorized |
|--------|----------------------|
| Issue-pipeline duties of a script-started coordinator | Standing list: only the duties the owner wrote down, recorded in chat and cited in the launch prompt (R17) |
| Push of a feature branch and the PR for an issue the owner set to Full Submit | Per-issue go: the owner's Full Submit setting and approval (R25); a feature-branch push and PR only, never a merge, a force push or a branch deletion |
| Merge of a PR | Per-PR go: the one-shot entry of the Merge procedure; never on a standing list |
| Close of an issue | Never on a standing list; the person's instruction must name the action (WORKER-CONTRACT.md:241) |
| Any other GitHub write | Refused by the verb unless it is on the standing list |

Requirement (INV-011). `E-NO-GRANT` sees only writes made through the orchestrator's own verbs (D:696); a raw `gh pr merge` is never seen by it, and a per-issue go is not a grants row. So the merge must go through one verb that demands the go entry described in "The go: contents, expiry and reach" and refuses a raw `gh pr merge` outside it. That verb does not exist; it is not shown to pass. Until it is built, the audit after the merge (Steps, step 7) is the check that can find a raw merge. Changes to `grants`, `merge_safety_files` and `reach_daily_max` stay behind an `--answer-ref` that `answer-check` accepts (D:688), with the validator's limits stated above.

## Contract amendments

<!-- Source: Variant B (CLAY), Cited fact 7, with Variant A Round 2 (c), (d) and probe INV-010 - merged per Change #6 -->
Contract text changes are a documentation action for the owner. This paper applies none. Each amendment below needs the owner's approval in chat before it counts (Owner DECISION), and none is in force.

1. WORKER-CONTRACT.md:70. Proposed sentence: the coordinator rules bind an Orca coordinator session the person opened, or one started at depth 0 (a terminal plus `ccsession`, not `worker-start`) by the owner's installed watcher under a standing authorization the owner recorded in chat, whose launch prompt cites that record and lists only the duties it names.
2. WORKER-CONTRACT.md:245. Proposed sentence (Variant A, Round 2): "A push of a feature branch for an issue the owner set to Full Submit and approved with the approval label counts as the person's go for that issue's push and pull request only, and never covers a merge, a force push, a branch deletion or any other push."
3. WORKER-CONTRACT.md:23 and :244 stay unchanged, with a note: they stay true because the Full Submit launch is an ordinary top-level session, so `/sc:pr-submit` is still never run as a worker. The worker route that Variant B's ADD1 would add (a `worker-start` worker with `Flow: orchestrated-issue` running `/sc:pr-submit`) is not adopted: D3's AC-4.3 live check was never run, ADD1 states no brief-guard route, and `/sc:pr-submit` has no unattended mode (D:135).

A launch-prompt authorization stays self-attested even after these amendments (INV-010); the amendments declare it and require the cited owner record, and they do not verify it.

## Reasons to reach the person

<!-- Source: Variant B (CLAY), Cited fact 6 and Round 2 "Remaining dispute" item 5 - merged per Change #7 -->
- The design's nine-row table (D:664-696) lists when the orchestrator may reach the person, under the rule "an unanswered question waits, no default" (D:692).
- It is adopted here only as an inventory of reasons for non-outward decisions. Every outward action (push, PR, comment, merge, close) still waits for the person's go.
- Owner DECISION: whether to adopt the nine-row list. Its benefit is not shown in use (UNVERIFIED). If the owner does not adopt it in chat, remove this section.

## Cited facts

<!-- Source: Base (original, modified) - facts 1 to 6 and 9 unchanged; facts 7 and 8 extended per Change #6 -->
1. These rules are decisions of the repository owner, not drift. `/home/coder/workspaces/IronClaude/.dev/orca-command-refactor/decisions/APPROVED.md:10-13` records D3 (pr-submit never an Orca worker; one ordinary session per PR, started only when the person names the PR), D4 (no worker acts outward; the coordinator does every push, PR, comment, install and paid run), D5 (coordinator is a person-opened session) and the GIT row (coordinator owns push, PR, replies, comments, merges), approved by the owner on 2026-11-02 ("Nothing here is reopened for debate", :3).
2. D5's stated reason is partly technical, not only about authority: a coordinator that was itself started with `worker-start` is depth 1, and at the Orca maximum of 1 its own worker starts "would be refused (presumed)" (`.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md:9`). So "person opened" is a precondition that protects fan-out.
3. D3's debate found that a pr-submit run by the coordinator "has no start authority" (HOW-WE-WORK.md lines cited there as :215 and :221, invariant INV-006; line numbers as of 2026-11-02) and put one ordinary session per PR in the PR's own child worktree (`.dev/orca-command-refactor/decisions/D3/RECOMMENDATION.md` section 1). A worker per PR "is deferred, not rejected" (same section) and needs D4 (a), AC-4.3 and a check that a chat-surface worker can run the loop (APPROVED.md:10).
4. That check was never run. The worker-contract plan holds pr-submit-as-worker "only if D3 (b) is chosen" and AC-4.3 is a live check on a scratch PR (`.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/source.md:224, :328`); the master contract's never-as-worker list still names pr-submit (:23). The design's own ADD1 admits `/sc:pr-submit` "has no unattended mode" (`docs/designs/orchestrator.md:135` (master)).
5. The master branch of IronClaude is not protected, no ruleset exists, and the acting user holds `maintain` (design DQ8, `docs/designs/orchestrator.md:118` (master); risk K12 at :1234 says only the worker's written prompt holds a worker back from pushing to `master`). With no GitHub-side stop, the person's go is the only brake on a merge into the default branch.
6. The owner's own memory records a real miss by an autonomous step: on 2026-11-04 the owner squash-merged PR 368 mid-cycle, and the skill's round-2 push re-created the deleted branch; also "a Codex *security* review can post a finding minutes after its code review reported clean" (memory `pr-submit-check-pr-open-before-push`, 15 days old, not re-verified). Automation around merge and review needed a human at the merge moment.
7. The zero-setup plan already automates what is safe and keeps the go where it matters. Requirement R25 lets the watcher launch Full Submit (commit, push a feature branch, run `/sc:pr-submit --monitor 3`, "and never merges") and states the rule change: for an approved Full Submit issue "that setting is the person's go for that issue's push and pull request, and nothing else is pushed" (`/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`, row R25; branch `ironbelly/issue-watcher-zero-setup-plan`, HEAD d0a0a433b, local and unpushed). The launched session is an ordinary top-level session, which is the route D3 allows. <!-- Source: Base (original, modified) - R25 status added per Change #6 --> R25 is in a local, unpushed plan, so it is not a rule in force. It amends :245 rather than complying with it ("Rule change to state in the contract"), so it counts only after the owner approves it in chat and the amendment in "Contract amendments" is made (conceded by both advocates in Round 2; X-005).
8. The same plan starts the coordinator by script: R9 and R17 ("the coordinator takes the issue-pipeline duties from its launch prompt (a standing owner authorization recorded here on 2026-11-18)", with the caveat "the launch prompt text must state the standing authorization"; Coder issue 516, session `COORD-<RepoName>`). So OURS already allows a script-started coordinator when the owner has recorded the authorization; what is in dispute is who may grant authority, not who types the start command. <!-- Source: Variant B (CLAY), Cited fact 7 - merged per Change #6 --> On depth, Variant B's reading is adopted (both advocates agreed in Round 2; X-001): a terminal plus `ccsession` start (`ccsession orchestrator-<short>-<n> --tier <orchestrator_tier>`, D:112; the pattern `waker.py` already uses, design U3, D:1261 citing `waker.py:144-169`) is a depth-0 session, and D5's depth reason (D5 RECOMMENDATION.md:9) is about a coordinator started by `worker-start`. This narrows fact 2: its depth reason covers a `worker-start` start only. "Person opened" (WORKER-CONTRACT.md:70) is a separate authority rule and still needs the amendment in "Contract amendments". A launch-prompt authorization is self-attested (INV-010): the script writes the prompt, so the coordinator cannot verify its source, and the same script can type into the same terminal (D:112) and supply a go. The prompt must therefore cite the owner's recorded authorization (a record the owner gave in chat and an agent wrote down) and list only the duties that record names. This is a requirement, not a verified control, and it is not shown to pass.
9. The design itself concedes the conflict: ADD1 says the autonomous merge, close and comments of ruling R10 "contradict all of this" (`docs/designs/orchestrator.md:135`), and the Clay-approved flow reverses owner decisions D3, D4 and D5 and WORKER-CONTRACT lines 23 and 244-245. The design's "owner" is Clay (FULL-REPORT.md section 4); no `ironbelly` approval of PR 681 (the merged design) exists on GitHub.

## What it costs

<!-- Source: Base (original) -->
- A person must give the go for each merge, so a merge waits until a person answers. Throughput is bounded by a person's attention.
- The `merge_ready` and typed-go rules are prose in the contract; nothing mechanical binds the coordinator to them (the technical reference says no IronClaude hook enforces D4 for a person-opened coordinator, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:318` (master)).

## What it risks

<!-- Source: Base (original, modified) - bullets kept; risk register table added per Change #8; second bullet updated because Change #3 adds a merge-time check -->
- A hard "person only" rule leaves the person as a bottleneck when nobody is present; the plan to run the watcher unattended (R16, R18) makes that gap more visible.
- Skipping a silent reviewer in the pr-submit loop can let a PR finish its loop "clean" when a reviewer was only late (memory note above). The base had no separate merge-time check for this; the "Silent reviewer" section adds one, which is designed and not built.

<!-- Source: Variant B (CLAY), risk habit (K12, AU4a, AU7) with shared assumption A-004 and probe INV-003, INV-012, INV-013 - merged per Change #8 -->
Risk register. Status values: "built" (exists and was shown to work), "designed" (specified in this paper, not built), "UNVERIFIED", "accepted" (no mitigation, stated cost). No row is "built". Every mitigation below narrows a risk and none closes it.

| Risk or cost | Mitigation | Status |
|--------------|-----------|--------|
| The person is a bottleneck and throughput is bounded by the person's attention | An unanswered question waits with no default (D:692); the go expires and the gate output is shown again | accepted; go expiry number is an Owner DECISION |
| The `merge_ready` and typed-go rules are prose; no hook binds the coordinator (`SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:318`) | The merge goes through one verb that demands the go entry (see "Standing lists"); the audit after the merge (Steps, step 7) | designed; verb not built; not shown to pass |
| A state change that leaves the head sha alone (new `changes_requested`, open thread, retarget, re-run check, draft flip) | The gate runs again immediately before the merge and refuses on any difference (Steps, step 4) | designed; gate not built; not shown to pass |
| A late or silent reviewer | Merge-time hold with a final-head re-trigger (see "Silent reviewer") | designed; whether Codex reviews on push is UNVERIFIED; 60 minutes is an Owner DECISION; not shown to pass |
| A dead 60-minute wait when a reviewer is never triggered or not installed | The owner sets `reviewers: none` for that repo, or shortens the wait | designed; Owner DECISION |
| Spoofed typing: a script types the go with `orca terminal send` into the same terminal (D:112) | `answer-check` as a validator of entry, question key, head sha and freshness; it cannot prove who typed | residual risk; whether the harness marks sent text differently is UNVERIFIED |
| A self-attested launch prompt (the script writes the prompt) | The prompt cites the owner's recorded authorization and lists only the duties it names | designed; residual; not shown to pass |
| A go replayed after a restart | Go expiry, a recorded entry (repo, PR, sha, time), and the PR state read first (D:591) | designed; not built; expiry number is an Owner DECISION |
| A raw `gh pr merge` that `E-NO-GRANT` never sees | The merge verb refuses a raw merge outside the go entry; the audit after the merge | designed; verb not built |
| `master` is unprotected and the acting user holds `maintain` (D:118; K12 at D:1234) | Only the person's go stands in the way. Branch protection, a ruleset, required review or a merge queue is a repo-admin action | Owner DECISION; feasibility UNVERIFIED; not a consensus item (A-004) |

What the gates narrow and do not close. For the stale-go gap (INV-013) the falsifiers are: a state change that leaves the sha alone, a go that cites a gate output the person did not read, a go replayed after a restart, a go typed by a script, and a method that disagrees with `merge_method`. The gate verb, the second gate run, `answer-check`, the :245 amendment and the go expiry are not built or not agreed, and `master` has no branch protection (D:118). For the late-reviewer gap (INV-012) the falsifiers are listed under "Silent reviewer". None of these gates is shown to pass.

## What it gets right

<!-- Source: Base (original, modified) - third bullet qualified for consistency with Change #6; first two bullets unchanged -->
- It places the irreversible act (merge into an unprotected default branch) behind a human, matching three owner decisions (D3, D4, GIT) and the 2026-11-17 chat-approval order.
- It keeps outward actions out of workers, so a worker that ignores its prompt cannot push or merge. The design's own K12 records the opposite risk for workers that run with no guard.
- <!-- Source: Base (original, modified) - "owner-approved" qualified for R25 so it does not contradict Cited fact 7 as modified per Change #6 --> It already contains a way to automate the push and PR (R25, Full Submit as a per-issue go; in a local, unpushed plan, so it counts only after the owner approves it in chat and :245 is amended) and the script-started coordinator (R9, R17, with the owner's authorization recorded 2026-11-18), so OURS is not "never automate"; it is "the owner grants the authority, in chat, and it is recorded."
