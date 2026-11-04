<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 3 (option (c), variant-3-original.md) -->
<!-- Merge date: 2026-11-02T18:15:51Z -->
<!-- Plan: refactor-plan.md (11 changes, auto-approved after the Step 4 review in refactor-plan-review.md) -->

# D4 option (c′): split by whether the action leaves the machine

<!-- Source: Base (original, modified): position line rewritten per Change #1 (own Orca child worktree; (b) as default and fallback, from Variant 2 via rounds/r2-variant-3.md:30) and Change #4 (outward list, from Variant 2 = Variant 3, X-001) -->
Position: a brief may authorize a worker to make one **local commit** at the end of its Task, in its own Orca child worktree, and nothing else outward. Every action that leaves the machine or touches a shared target (push, merge into a shared branch, PR, review reply, issue or status comment, project update, remote branch deletion, real-target install, VM and paid external run) is never done by a worker; the coordinator or the person does it after reading the contracts. Option (b), no worker commits, is the default and the fallback: it applies whenever a condition of the commit rule below fails.

<!-- Source: Base (original, modified): commit preconditions replaced per Change #1 (Variant 2 shared-worktree mechanics; CR-01 T1; git-ownership option E rules W2 and N4) -->
Commit rule (the issue #326 question): no worker commits unless both of these hold:
1. The brief quotes the user's own instruction naming a local commit for that Task.
2. The coordinator started the worker in its own child worktree, created by Orca at Orca's default path (never under `.dev/worktrees/`), with `worker-start --worktree new-child --base-branch <feature branch>` for a new Task or `--worktree id:<that child's id>` for a resume Task in the same child (option E rules W2 and N4, `E:78,99`), whose setup succeeded before dispatch (`CR-01:16-17,24`), and with no other writer recorded there.

If either fails, option (b) applies: no commit. Whether `--worktree new-child` works in a live run is UNVERIFIED (CR-01's evidence is `--help` output, `CR-01:48`); a P0 live check proves it, and until it passes no commit authorization is valid.

<!-- Source: Variant 3 Round 2 revision (rounds/r2-variant-3.md:9,12,37-38), replacing the base's /sc:implement commit window: merged per Change #2 -->
When both hold, the worker session makes one plain-git commit (`HWW:324`) after the command has exited and its contract reads `worker_status: succeeded`. The rule keys on `worker_status`, not on the Orca outcome: `partial` maps to outcome `succeeded` (`SPEC:69`), and a commit after `partial` or `blocked` would make a later resume halt `head-moved` (`RETRY:44`). Nothing commits inside a command (implement has no commit step, `MW:63,67`). Every command's own commit step stays off under `--unattended`: post-release's commit (`SPEC:136`), task's EXEMPT `commit` (`TASK:61`; `SPEC:144`) and the TFEP report commit (`TASK:266`), because post-release lists "committing" among the actions confirmed first "this session" (`PRL:351`), which a brief cannot satisfy. Per-implement-task commits wait for #326 item K3 (`EVAL:63`); until then there is one commit per Orca Task.

<!-- Source: Base (original, modified): scope, branch and no-push clauses kept from V3:5; ordered steps, failure path and SHA location appended per Change #3 (git-ownership option E rules W4, W5, W6, N2; invariant-probe.md INV-008, INV-009, INV-010, INV-015, INV-018) -->
The worker commits only its Task's own files plus `.dev/tasks` (`CLAUDE.md:37`), never on `master` or the default branch, and never pushes. In this order, it:
1. Reads coordinator follow-ups and stops if the grant was narrowed or revoked. A follow-up never widens it.
2. Refuses to commit if HEAD is detached or the branch is the default branch, found with `git symbolic-ref refs/remotes/origin/HEAD`.
3. Refuses if `git status --porcelain` shows a path outside the allowed set. The allowed set is every path under the brief's report directory (including `return-contract.yaml`), the contract's `report_path` and `artifacts`, and `.dev/tasks`.
4. Stages the allowed-set paths that lie inside the child worktree and runs `git commit --only -- <paths>`, as pr-submit already does (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:274`).
5. Never uses `--no-verify`.

If any step refuses, the commit is empty, or a hook fails or changes files, no commit is made, the files stay in the child worktree, and the worker sends `worker_done --outcome failed` with a body whose first sentence gives `worker_status: succeeded; commit not made` and the reason. The contract is not edited after the commit, because `artifacts` holds files (`SPEC:68`) and a later edit would leave the worktree dirty (INV-015). The worker gives the new SHA in the `worker_done` body, and the coordinator reads the authoritative list from the branch (`git -C <child worktree> log <feature branch>..HEAD`).

<!-- Source: refactor-plan.md Change 10 (Completeness criterion 5, base-selection.md:107), new paragraph after the commit rule: merged per Change #10 -->
Out of scope for this decision: the commit step inside `/sc:implement` (#326 item K3, `EVAL:63`); a hook or permission rule that blocks `git push` in worker sessions (INV-012; option E's optional guard G3, `E:87`); how `--unattended` reaches nested commands (INV-011, `SPEC:145`); and running managed plan packages in a child worktree (INV-028).

<!-- Source: Base (original, modified): key line extended with the definitions in diff-analysis.md:12 and rounds/r2-variant-3.md:3, plus CR-01 and E (needed by Changes #1, #3, #4, #6, #10) -->
Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `PRL:N` = `src/superclaude/skills/sc-post-release-protocol/SKILL.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `EVAL:N` = `.dev/orca-command-refactor/review/issue-326-evaluation.md:N`; `RETRY:N` = `src/superclaude/skills/sc-implement-protocol/refs/retry.md:N`; `MW:N` = `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:N`; `QA:N` = `src/superclaude/skills/sc-implement-protocol/refs/qa.md:N`; `TASK:N` = `src/superclaude/skills/sc-task-protocol/SKILL.md:N`; `AUG:N` = `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `CR-01:N` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:N`; `E:N` = `.dev/orca-command-refactor/decisions/git-ownership/debate/adversarial/round2-advocate-e.md:N` (git-ownership option E, Round 2). `C-NNN` and `INV-NNN` are finding IDs in `.dev/orca-command-refactor/decisions/D4/debate/adversarial/diff-analysis.md` and `invariant-probe.md`. All lines were read on branch `ironbelly/OrcaCLICommandRefactor-Specs` on 2026-11-02.

## Why a third option
<!-- Source: Base (original) -->
The repo already draws this exact line for people: "**Never push without approval.** Commit locally, show your lead what changed, and push only when they say go" (`HWW:282`); "Commit locally on the feature branch only when authorized" (`HWW:212`); for `/sc:git`, "a commit needs authorization. Do not append push, merge or PR creation" (`HWW:324`). (c) applies the same line to workers.

## Safety
<!-- Source: Base (original, modified): undo claim corrected per Change #11 (rounds/r1-variant-3.md:37-38; diff-analysis.md:85, A-009); the provenance-gap sentence from V3:14 is kept -->
- A worker commit stays on its own child branch in a worktree no other worker writes, so it can be undone or discarded there, and nothing leaves the machine until the coordinator pushes after the person's review (the push review rule below). The cross-session provenance gap of (a) is limited to that one local commit.

<!-- Source: Base (original, modified): V3:13's coordinator sentence replaced and extended per Change #4 (X-001, Variant 2 = Variant 3; EVAL F4 and F5; AUG:319; option E rule O1; CR-01:45; INV-023) -->
- Everything that leaves the machine stays with the coordinator: push, merge into a shared branch, PR, review reply, issue or status comment, project update, remote branch deletion, real-target install, VM and paid external run. The coordinator does them in its own chat, only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation (`PRL:351`), subject to the push review rule below.
- Every `gh` call names `--repo IronbellyOrg/IronClaude`, nothing is pushed to `upstream`, and Orca's issue and PR linking is not used until Orca's project identity resolves to the fork (`CR-01:45`). PRs open only through `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`). The coordinator posts the auggie-review summary from the worker's `REVIEW.md` (`AUG:319`).
- D3 coupling: D3 option (b) (pr-submit as a worker) needs D4 option (a), so this decision rules D3 (b) out until D4 is loosened, and AC-4.3 (`SPEC:276`) does not run.

<!-- Source: invariant-probe.md:56,74 (INV-027, gate G10) with HWW:282: merged per Change #5 -->
- Push review rule: before any push that would publish a worker commit the person has not yet seen, the coordinator shows the person every such commit (`git log --stat origin/<branch>..<branch>`, or `git log --stat <feature base>..<branch>` for a branch never pushed) and pushes only on a go the person gives after seeing them. No earlier pre-authorization waives this, and it applies to every push, not only the first (for example, after a later child branch is merged into an already-pushed feature branch). pr-submit's own fix-commit pushes after an approved push follow `HWW:282` unchanged; they contain no worker commits.

## Reliability
<!-- Source: Base (original, modified): V3:17's check replaced per Change #7 (invariant-probe.md:45-46,73, INV-016 and INV-017; conditional AC-4.2 from rounds/r2-variant-3.md:19, C-008) -->
- One boundary, easy to state and check. AC-4.2 (`SPEC:275`) records, before and after the run, `git -C <worker worktree> log -1 --format=%H`, `git -C <worker worktree> for-each-ref refs/heads`, `git ls-remote origin` (all refs) and `gh pr list --repo IronbellyOrg/IronClaude --author @me`. Pass with no commit authorized: all four unchanged. Pass with a commit authorized: the only change is new commits on the worker's child branch, and `ls-remote` and the PR list are unchanged. The check runs against the worker's worktree because a `git log -1` at the repo root (`SPEC:202`) cannot see a commit made there.

<!-- Source: invariant-probe.md:30-32 (INV-001, INV-002, INV-003); option E rules C1, C3, G2 (E:69,71,86); CR-01:23; D2 consensus item 4 (.dev/orca-command-refactor/decisions/D2/debate/adversarial/invariant-probe.md:14): merged per Change #6 -->
- The coordinator is the single git owner: it does every merge, push, PR and comment (option E rule O1, `E:64`). It follows these placement rules:
  1. The git owner commits in, or merges a child branch into, a worktree only when no worker is running there.
  2. In any worktree, the shared feature worktree included, that holds an `/sc:implement` Task ended `blocked` or `partial`, the git owner makes no commit or merge and the coordinator dispatches no other Task until the person has resumed or discarded that work. Merge-back of other children into that worktree waits (D2 consensus item 4, `.dev/orca-command-refactor/decisions/D2/debate/adversarial/invariant-probe.md:14`).
  3. A commit grant covers one Task and ends at that Task's `worker_done`. A resume or follow-up Task, including one sent to a reused terminal (`CAPS:107`), needs its own quoted grant.
  4. The coordinator records which Task writes in which worktree (option E rule C3, `E:71`).
  5. Concurrent implement runs in different worktrees use distinct plan slugs (option E rule G2, `E:86`; INV-025).
  6. The brief copies the user's instruction word for word, and the coordinator keeps the same copy in its run notes (INV-004).
  7. A Task placed in a child worktree gets an absolute report directory inside that child worktree; the coordinator reads the contract there by absolute path before merge-back (`CR-01:23`).

## How a person works day to day
<!-- Source: Base (original, modified): "per-task commit history" narrowed to one commit per Orca Task, to stay consistent with Change #2 -->
- Workers can leave a clean commit history, one commit per Orca Task (issue #326, `EVAL:19`), which the person reviews before the coordinator pushes and opens the PR. post-release workers report install, VM and PR steps as skipped (`PRL:340`); the coordinator runs them with the person.

### Where this option is weak
<!-- Source: Variant 1, Safety (V1:14-15), form of stating weaknesses where they bite (S-004); items from invariant-probe.md:19-24 and INV-012: merged per Change #8 -->
- The commit still rests on the coordinator's quotation of the user's instruction, which the worker cannot check (`SPEC:66`). D2 would not accept the same relayed authority for a Ruling ("another agent's message ... not acceptance", `QA:254`; C-007, conceded to (b) at 97%).
- Commits are per Orca Task, not per implement task, until #326 item K3 (`EVAL:63`).
- Each committing worker leaves a branch the person must decide on (EVAL F3, `EVAL:53`).
- The inline auggie-review comments have no deferred posting path (`AUG:320-327`); only the summary can be posted later.
- The "never push" rule is enforced by instructions only, with no hook or permission rule (INV-012).

## Implementation cost
<!-- Source: Base (original, modified): V3:23 replaced per Change #2 (drops "No command needs a new outward flag", conceded at rounds/r1-variant-3.md:37) and Change #9 (edit list from V3:23, V1:24, EVAL:50-55, rounds/r2-variant-3.md:99-102, CR-01:26-31) -->
Spec edits (listed here, none applied yet):
- D4 text (`SPEC:345-348`): state this position and recommend option (c′).
- WC-9 (`SPEC:73`): "Under `--unattended` every outward default (push, merge into a shared branch, PR, GitHub post, install on a shared or real target, VM, paid external run) is off, and no brief can turn it on (D4). The only git write a brief may authorize is the worker session's end-of-Task local commit under D4's commit rule." Drop the `README.md:31` citation and add the commit sentence.
- WC-5 (`SPEC:69`): add that a refused or failed end-of-Task commit is reported as `worker_done --outcome failed`, with `worker_status: succeeded; commit not made` and the reason in the body's first sentence.
- Section 2.3 (`SPEC:79`): change "which outward actions, if any, are authorized (WC-9)" to "whether the end-of-Task local commit is authorized, quoting the user's instruction word for word (D4); no other outward action can be authorized", and add the coordinator duties: the push review rule (Safety) and the placement rules (Reliability).
- Section 3 rows:
  - auggie-review (`SPEC:123`): "`--post-pr` is refused under `--unattended`; the coordinator posts the summary from `REVIEW.md` (D4)".
  - post-release (`SPEC:136`): "VM, real-target install, commit and PR always off under `--unattended` (D4)".
  - task (`SPEC:144`): "EXEMPT `commit` and `push` refused under `--unattended` (D4)".
  - implement (`SPEC:132`): no commit inside the command; per-task commits wait for K3. This replaces EVAL F1's implement-row sentence.
- `/sc:git` row (`SPEC:156`): EVAL F0 wording, which drops the `README.md:31` citation (`EVAL:50`).
- AC-4.2 (`SPEC:275`): the check under Reliability, plus one P0 acceptance check that a commit-authorized worker started with `--worktree new-child --base-branch <feature branch>` commits only on its child branch.
- 7.2 setup (`SPEC:235`): replace "created under `.dev/worktrees/` (`CLAUDE.md:299`)" with "created by Orca at Orca's default path (`worker-start --worktree new-child --base-branch <feature branch>` or `orca worktree create`), never under `.dev/worktrees/`". 7.2 step 1 (`SPEC:236`): place the worker with that creation flag, or with `--worktree id:<Orca worktree id>`, and delete the "whether Orca accepts a worktree it did not create is UNVERIFIED" clause. CR-01's four edits do not cover these lines (`CR-01:27-31`).
- CR-01's four edits (`CR-01:28-31`) in place of EVAL F2. EVAL F3 is covered by CR-01's merge-back paragraph, and F4 and F5 by the outward rules under Safety.

Cost of changing later: loosening to (a) is additive; tightening back to (b) is one sentence plus deleting the commit rule.
