# Position OURS (D06): authority for merging, script-started coordinators, reviewer hold

Status: complete. Paths marked (master) are in the read-only export /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6).

## The claim

Authority over outward and irreversible actions stays with the person. A coordinator session is opened by a person (or started by the owner's installed watcher under an authorization the owner recorded in chat), acts outward only on the person's named instruction, never merges on its own initiative, and never runs `/sc:pr-submit` as an Orca worker. A reviewer that shows no activity is skipped inside the `/sc:pr-submit` loop. Approvals and goes are given in chat and are checked as such. Where automation helps, it narrows the person's work (it prepares, checks and waits); it does not replace the person's go.

## The mechanism

1. The coordinator rules bind "an Orca coordinator session the person opened" (`src/superclaude/core/WORKER-CONTRACT.md:70` (master)). Every git and GitHub outward action happens "only when the user's instruction names that action, and confirms with the person at the moment of action" (:241). A `merge_ready` message "merges only on the person's instruction" (:108).
2. Publishing is separate from approving: "Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this" (:245).
3. PRs go "only through `/sc:pr-submit --monitor 3`, run in an ordinary top-level session as decision D3 states, never as a worker" (:244); `/sc:pr-submit` is on the never-as-worker list (:23).
4. In the PR loop a silent reviewer is recorded absent and ignored: "a reviewer that never shows activity is recorded absent ... and ignored for the rest of the run" (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:29-32` (master); table at :363-364; project CLAUDE.md:58).
5. Approvals live in chat, not files or relayed text (owner order 2026-11-17, memory `approvals-through-chat-never-files`; WORKER-CONTRACT D2: only the person gives a Ruling).

## Cited facts

1. These rules are decisions of the repository owner, not drift. `/home/coder/workspaces/IronClaude/.dev/orca-command-refactor/decisions/APPROVED.md:10-13` records D3 (pr-submit never an Orca worker; one ordinary session per PR, started only when the person names the PR), D4 (no worker acts outward; the coordinator does every push, PR, comment, install and paid run), D5 (coordinator is a person-opened session) and the GIT row (coordinator owns push, PR, replies, comments, merges), approved by the owner on 2026-11-02 ("Nothing here is reopened for debate", :3).
2. D5's stated reason is partly technical, not only about authority: a coordinator that was itself started with `worker-start` is depth 1, and at the Orca maximum of 1 its own worker starts "would be refused (presumed)" (`.dev/orca-command-refactor/decisions/D5/RECOMMENDATION.md:9`). So "person opened" is a precondition that protects fan-out.
3. D3's debate found that a pr-submit run by the coordinator "has no start authority" (HOW-WE-WORK.md lines cited there as :215 and :221, invariant INV-006; line numbers as of 2026-11-02) and put one ordinary session per PR in the PR's own child worktree (`.dev/orca-command-refactor/decisions/D3/RECOMMENDATION.md` section 1). A worker per PR "is deferred, not rejected" (same section) and needs D4 (a), AC-4.3 and a check that a chat-surface worker can run the loop (APPROVED.md:10).
4. That check was never run. The worker-contract plan holds pr-submit-as-worker "only if D3 (b) is chosen" and AC-4.3 is a live check on a scratch PR (`.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/source.md:224, :328`); the master contract's never-as-worker list still names pr-submit (:23). The design's own ADD1 admits `/sc:pr-submit` "has no unattended mode" (`docs/designs/orchestrator.md:135` (master)).
5. The master branch of IronClaude is not protected, no ruleset exists, and the acting user holds `maintain` (design DQ8, `docs/designs/orchestrator.md:118` (master); risk K12 at :1234 says only the worker's written prompt holds a worker back from pushing to `master`). With no GitHub-side stop, the person's go is the only brake on a merge into the default branch.
6. The owner's own memory records a real miss by an autonomous step: on 2026-11-04 the owner squash-merged PR 368 mid-cycle, and the skill's round-2 push re-created the deleted branch; also "a Codex *security* review can post a finding minutes after its code review reported clean" (memory `pr-submit-check-pr-open-before-push`, 15 days old, not re-verified). Automation around merge and review needed a human at the merge moment.
7. The zero-setup plan already automates what is safe and keeps the go where it matters. Requirement R25 lets the watcher launch Full Submit (commit, push a feature branch, run `/sc:pr-submit --monitor 3`, "and never merges") and states the rule change: for an approved Full Submit issue "that setting is the person's go for that issue's push and pull request, and nothing else is pushed" (`/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`, row R25; branch `ironbelly/issue-watcher-zero-setup-plan`, HEAD d0a0a433b, local and unpushed). The launched session is an ordinary top-level session, which is the route D3 allows.
8. The same plan starts the coordinator by script: R9 and R17 ("the coordinator takes the issue-pipeline duties from its launch prompt (a standing owner authorization recorded here on 2026-11-18)", with the caveat "the launch prompt text must state the standing authorization"; Coder issue 516, session `COORD-<RepoName>`). So OURS already allows a script-started coordinator when the owner has recorded the authorization; what is in dispute is who may grant authority, not who types the start command.
9. The design itself concedes the conflict: ADD1 says the autonomous merge, close and comments of ruling R10 "contradict all of this" (`docs/designs/orchestrator.md:135`), and the Clay-approved flow reverses owner decisions D3, D4 and D5 and WORKER-CONTRACT lines 23 and 244-245. The design's "owner" is Clay (FULL-REPORT.md section 4); no `ironbelly` approval of PR 681 (the merged design) exists on GitHub.

## What it costs

- A person must give the go for each merge, so a merge waits until a person answers. Throughput is bounded by a person's attention.
- The `merge_ready` and typed-go rules are prose in the contract; nothing mechanical binds the coordinator to them (the technical reference says no IronClaude hook enforces D4 for a person-opened coordinator, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:318` (master)).

## What it risks

- A hard "person only" rule leaves the person as a bottleneck when nobody is present; the plan to run the watcher unattended (R16, R18) makes that gap more visible.
- Skipping a silent reviewer in the pr-submit loop can let a PR finish its loop "clean" when a reviewer was only late (memory note above); OURS has no separate merge-time check for this.

## What it gets right

- It places the irreversible act (merge into an unprotected default branch) behind a human, matching three owner decisions (D3, D4, GIT) and the 2026-11-17 chat-approval order.
- It keeps outward actions out of workers, so a worker that ignores its prompt cannot push or merge. The design's own K12 records the opposite risk for workers that run with no guard.
- It already contains an owner-approved way to automate the push and PR (R25, Full Submit as a per-issue go) and the script-started coordinator (R9, R17), so OURS is not "never automate"; it is "the owner grants the authority, in chat, and it is recorded."

