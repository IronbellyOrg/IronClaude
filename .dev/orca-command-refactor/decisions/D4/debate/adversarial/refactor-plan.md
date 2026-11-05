# Refactoring Plan: Merge into Base (Variant 3)

## Overview
- Base: Variant 3, option (c) (`variant-3-original.md`, cited `V3:N`). Non-base variants: Variant 1, option (a) (`V1:N`); Variant 2, option (b) (`V2:N`).
- Incorporating strengths from: Variant 2 (shared-worktree mechanics, one provenance rule, "(b) is the default and fallback"); Variant 1 (states its own weakness where it bites, S-004; the deferred auggie-review summary path, `AUG:319`); the Round 2 refinement (c′) that all three advocates recommend (`debate-transcript.md:720-722`); the Round 2.5 invariant probe (`invariant-probe.md`); and five fixed constraints set by the team lead for this resume (listed below).
- Planned changes: 11.
- Risk level: Medium overall. Most changes rewrite base rules (Medium); none restructures the position file.
- Resumed 2026-11-02 after a dev-environment restart at about 16:28 UTC. Steps 1-3 were not redone or rescored.

### Step 3 state found on disk, and why the base stands
`base-selection.md` names Variant 3 as the base (`base-selection.md:153`), but 11 of its sections are still `<!-- TODO -->` (Clarity, Risk Coverage, Invariant & Edge Case Coverage, Qualitative Summary, Edge Case Floor Check, Position-Bias Mitigation, Combined Scoring, and the three rationale sections; `base-selection.md:132-163`). Both qualitative passes are complete (`scoring/qual-pass-1.md:72-86`, `scoring/qual-pass-2.md:72-86`). Without rescoring, the base was checked against what is on disk:
- The orchestrator's own sensitivity line records final combined scores of V1 0.7504, V2 0.7522, V3 0.7871 under the alternative SR formula, and says the base, the tiebreaker trigger and its outcome do not change (`base-selection.md:80`). Solving those numbers for the qualitative score gives V1 19/30, V2 18/30, V3 20/30, so the main-formula combined scores are V1 0.7804, V2 0.7850, V3 0.8106 (quant from `base-selection.md:23`).
- Independently of that line: the two passes disagree on only four cells outside the already-resolved Structure rows (V3 Risk 2, V1 Risk 4, V3 Risk 4, V3 Invariant 2; `qual-pass-1.md:57,59,67` against `qual-pass-2.md:57,59,67`). Under every way of resolving them, V3's qualitative total is 19-22/30, V2's is 18/30 and V1's is 18-19/30, so V3's lowest combined score (0.7939) is above V2's (0.7850) and V1's highest (0.7804).
- V3's lead over V2 is under 5% in the orchestrator's figures, so the tiebreaker applies. Level 1 is debate performance: V3 won 13 points outright and V2 won 5 (`debate-transcript.md:663`). V3 stays the base.
- `base-selection.md` itself was left unedited, as instructed. Its TODO sections remain a gap in the Step 3 record (NOT BUILT), not a reason to change the base.

### Fixed constraints applied (not debated)
| ID | Constraint | Source given by the team lead | Effect on the base |
|---|---|---|---|
| FC-1 | Every worktree is created by Orca at Orca's default path, never under `.dev/worktrees/`. | `changes/CR-01-feature-worktree-hierarchy.md:41` (user decision, 2026-11-02) | Replaces (c′)'s ".dev/worktrees/" placement (`rounds/r2-variant-3.md:92`) and the 7.2 disposable worktree path (`SPEC:235`). |
| FC-2 | SuperClaude upstream is never pushed to or interacted with; every GitHub action targets `IronbellyOrg/IronClaude` only. | `CLAUDE.md:39-48`; `CR-01:45` | Every outward step and check in the merged text names `--repo IronbellyOrg/IronClaude`; Orca issue and PR linking stays unused (`CR-01:45`). |
| FC-3 | Merged PR #343: only blocking findings fail a review; review loops cap at 2 fix cycles. | `git log -1 80f934de` ("only blocking findings fail a review ... at most 2 fix cycles (3 reviews)") | A minor finding no longer turns a run into a failure, so it cannot stop a `worker_status: succeeded` commit; the Step 4 review of this plan uses the same rule. |
| FC-4 | CR-01: a worker that may commit gets its own child worktree (trigger T1). | `CR-01:16-17,29` | Replaces V3's "its own feature branch" (`V3:3`) with an Orca child worktree created with `--worktree new-child --base-branch <feature branch>`. |
| FC-5 | git-ownership converged on hybrid option E: workers commit locally only where the brief grants it, with `git commit --only -- <paths>`; one owner does every push, PR and comment. | `decisions/git-ownership/debate/adversarial/round2-advocate-e.md:63-87`; `decisions/git-ownership/option-e.md:8-14` | Adds `--only`, the untouched-path tripwire, the pre-commit follow-up read and E's resume placement; five E rules conflict with this plan (W3, W5/W6 failure status, W6 SHA location, C2, O3), each stated under Changes NOT Being Made. |

## Planned Changes

### Change 1: Commit only in an Orca child worktree; (b) is the default and fallback (from Variant 2 and the debate; FC-1, FC-4)
- **Source**: V2's shared-worktree mechanics (`rounds/r1-variant-2.md`, cited at `rounds/r2-variant-3.md:30`); (c′) condition 2 (`rounds/r2-variant-3.md:10,92`); V2's framing "(b) is the default and fallback of (c′)" (`rounds/r2-variant-3.md:30`); CR-01 T1 (`CR-01:16-17`).
- **Target**: Base, position line and commit rule (`V3:3`, `V3:5`) (replace).
- **Rationale**: V3 conceded that "its own feature branch" is not the spec default, because workers share a worktree (`SPEC:75`) and so share HEAD and the index (`rounds/r1-variant-3.md:38`; A-004, A-009 in `diff-analysis.md:80,85`). The debate fixed it with an own-worktree condition (X-002 to V3, 96%, `debate-transcript.md:653`). FC-1 moves that worktree from `.dev/worktrees/` to an Orca-created child worktree, which also removes (c′)'s third condition: CR-01 records that an Orca-created worktree removes the UNVERIFIED question of whether Orca accepts a worktree it did not create (`CR-01:41`; `SPEC:236`), and INV-022's empty-set risk (`invariant-probe.md:51`) disappears with it.
- **Integration point**: The commit rule opens with: no worker commits unless (1) the brief quotes the user's own instruction naming a local commit for that Task, and (2) the coordinator started the worker in its own child worktree, created by Orca at Orca's default path, with `worker-start --worktree new-child --base-branch <feature branch>` for a new Task or `--worktree id:<that child's id>` for a resume Task in the same child (git-ownership E rule W2 and N4, `round2-advocate-e.md:78,99`), whose setup succeeded before dispatch (`CR-01:16-17,24`), and with no other writer recorded there. If either fails, option (b) applies: no commit. Whether `--worktree new-child` works in a live run is UNVERIFIED (CR-01's evidence is `--help` output, `CR-01:48`); a P0 live check proves it, and until it passes no commit authorization is valid.
- **Risk**: Medium. It changes the base's central precondition.

### Change 2: One end-of-Task commit after the command; command commit steps stay off (from the debate, Variant 2 evidence)
- **Source**: `rounds/r2-variant-3.md:9,12,37-38`; V2's finding that a plain-git commit after the command needs no command feature (`HWW:324`, cited at `rounds/r2-variant-3.md:9`).
- **Target**: Base, commit rule (`V3:5`) and Implementation cost (`V3:23`) (replace).
- **Rationale**: V3's commit window inside `/sc:implement` needs a commit step implement does not have (X-006 to V2, 97%, `debate-transcript.md:657`; `MW:63,67`), and that made "No command needs a new outward flag" (`V3:23`) false (conceded, `rounds/r1-variant-3.md:37`). The worker session's single plain-git commit after the command exits removes both errors. Keying on `worker_status: succeeded`, not on the Orca outcome, matters because `partial` maps to outcome `succeeded` (`SPEC:69`) and a commit after `partial` or `blocked` would make a later resume halt `head-moved` (`RETRY:44`, cited at `rounds/r2-variant-3.md:38`). post-release lists "committing" among actions confirmed first "this session" (`PRL:351`), which a brief cannot satisfy, so every command's own commit step stays off under `--unattended`: post-release's commit (`SPEC:136`), task's EXEMPT `commit` (`TASK:61`; `SPEC:144`) and the TFEP report commit (`TASK:266`). Per-implement-task commits wait for #326 item K3 (`EVAL:63`).
- **Integration point**: Replace the `/sc:implement` window sentence in `V3:5` with the end-of-Task rule; replace `V3:23`'s "No command needs a new outward flag" with the actual spec edit list (Change 9).
- **Risk**: Medium. It narrows #326's "after each task" to one commit per Orca Task (INV-014, conceded, `invariant-probe.md:43`).

### Change 3: Commit mechanics from git-ownership option E, plus the probe's guard fixes (FC-5)
- **Source**: git-ownership round 2, option E rules W4, W5, W6 and N2 (`decisions/git-ownership/debate/adversarial/round2-advocate-e.md:80-82,94`); probe items INV-008, INV-009, INV-010, INV-015, INV-018 (`invariant-probe.md:37-39,44,47`).
- **Target**: Base, commit rule (`V3:5`) (append).
- **Rationale**: Staging explicit paths is not enough when the index already holds other staged paths; `git commit --only -- <paths>` commits only the named paths, as pr-submit already does (`sc-pr-submit-protocol/SKILL.md:274`). The probe found no rule for a detached HEAD, a default-branch detector, a hook that rejects or rewrites files, an empty or ignored staging set, or a failed commit (G5-G8, `invariant-probe.md:69-72`).
- **Integration point**: After the conditions in Change 1, the worker, in this order: (1) reads coordinator follow-ups and stops if the grant was narrowed or revoked (a follow-up never widens it); (2) refuses to commit if HEAD is detached or the branch is the default branch, found with `git symbolic-ref refs/remotes/origin/HEAD`; (3) refuses if `git status --porcelain` shows a path outside the allowed set, which is every path under the brief's report directory (including `return-contract.yaml`), the contract's `report_path` and `artifacts`, and `.dev/tasks`; (4) stages the allowed-set paths that lie inside the child worktree and runs `git commit --only -- <paths>`; (5) never uses `--no-verify`. If any step refuses, the commit is empty, or a hook fails or changes files, no commit is made, the files stay in the child worktree, and the worker sends `worker_done --outcome failed` with a body whose first sentence gives `worker_status: succeeded; commit not made` and the reason. The contract is not edited after the commit; the worker gives the new SHA in the `worker_done` body, and the coordinator reads the authoritative list from the branch (`git -C <child worktree> log <feature branch>..HEAD`). This replaces "lists each SHA in `artifacts`" (`V3:5`), because `artifacts` holds files (`SPEC:68`) and editing the contract after the commit would leave the worktree dirty (INV-015).
- **Risk**: Medium. It adds one WC-5 sentence (a failed commit gives outcome `failed`) and departs from E's W5 and W6 wording on the failure status and on where the SHA is recorded (both stated under Changes NOT Being Made).

### Change 4: Everything that leaves the machine stays with one owner, on the fork only (Variant 2 = Variant 3; FC-2, FC-5)
- **Source**: X-001 (V2 = V3, 97%, `debate-transcript.md:652`); EVAL F4 and F5 (`EVAL:54-55`); `AUG:319`; option E rule O1 (`round2-advocate-e.md:64`); `CR-01:45`; probe INV-023 (`invariant-probe.md:52`).
- **Target**: Base, position line (`V3:3`) and Safety (`V3:13`) (replace and append).
- **Rationale**: No variant now defends a worker push, PR or post. V1 conceded every outward action (`rounds/r2-variant-1.md:7-15`). The coordinator is the one session that can still ask the person (`SPEC:66`; `PRL:351`).
- **Integration point**: State the outward list as: push, merge into a shared branch, PR, review reply, issue or status comment, project update, remote branch deletion, real-target install, VM and paid external run. The coordinator does them in its own chat, only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation (`PRL:351`). Every `gh` call names `--repo IronbellyOrg/IronClaude`, nothing is pushed to `upstream`, and Orca's issue and PR linking is not used until Orca's project identity resolves to the fork (`CR-01:45`). PRs open only through `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`). The auggie-review summary is posted by the coordinator from the worker's `REVIEW.md` (`AUG:319`). Add the D3 coupling: D3 option (b) (pr-submit as a worker) needs D4 option (a), so this decision rules D3 (b) out until D4 is loosened, and AC-4.3 (`SPEC:276`) does not run.
- **Risk**: Low. Additive except for the D3 coupling sentence.

### Change 5: Review worker commits before any push (probe INV-027)
- **Source**: `invariant-probe.md:56,74`; `HWW:282` ("Commit locally, show your lead what changed, and push only when they say go").
- **Target**: Base, Safety (`V3:13-14`) (append).
- **Rationale**: Under `PRL:351`'s live-conversation exemption the coordinator could push worker commits no person has seen, and `/sc:pr-submit --monitor 3` then pushes fixes without asking (`HWW:282`). That breaks the base's claim that the worst case is one local commit (G10).
- **Integration point**: Before any push that would publish a worker commit the person has not yet seen, the coordinator shows the person every such commit (`git log --stat origin/<branch>..<branch>`, or `git log --stat <feature base>..<branch>` for a branch never pushed) and pushes only on a go the person gives after seeing them. No earlier pre-authorization waives this, and it applies to every push, not only the first (for example, after a later child branch is merged into an already-pushed feature branch). pr-submit's own fix-commit pushes after an approved push follow `HWW:282` unchanged; they contain no worker commits.
- **Risk**: Medium. It adds one person step per pushed branch.

### Change 6: Quiescence and placement rules for the git owner (probe INV-001, INV-002, INV-003)
- **Source**: `invariant-probe.md:30-32`; option E rules C1 and C3 (`round2-advocate-e.md:69,71`); CR-01 merge-back (`CR-01:23`); D2 consensus item 4 (`decisions/D2/debate/adversarial/invariant-probe.md`, "Emerging consensus" item 4).
- **Target**: Base, Reliability (`V3:16-17`) (append).
- **Rationale**: (c′) moves the shared-worktree HEAD hazard to the coordinator rather than removing it (INV-001), and a reused child worktree can move HEAD under an earlier implement Task left `blocked` (INV-002). A grant with no lifetime can leak into a follow-up Task on a reused terminal (INV-003).
- **Integration point**: (1) The git owner commits in, or merges a child branch into, a worktree only when no worker is running there. (2) In any worktree, the shared feature worktree included, that holds an `/sc:implement` Task ended `blocked` or `partial`, the git owner makes no commit or merge and the coordinator dispatches no other Task until the person has resumed or discarded that work; merge-back of other children into that worktree waits (D2 consensus item 4). (3) A commit grant covers one Task and ends at that Task's `worker_done`; a resume or follow-up Task needs its own quoted grant. (4) The coordinator records which Task writes in which worktree (E rule C3). (5) Concurrent implement runs in different worktrees use distinct plan slugs (E rule G2, `round2-advocate-e.md:86`; INV-025). (6) The brief copies the user's instruction word for word and the coordinator keeps the same copy in its run notes (INV-004). (7) A Task placed in a child worktree gets an absolute report directory inside that child worktree; the coordinator reads the contract there by absolute path before merge-back (INV-020).
- **Risk**: Medium. It adds coordinator duties to section 2.3.

### Change 7: Checks that see the worker's worktree and every remote ref (probe INV-016, INV-017)
- **Source**: `invariant-probe.md:45-46,73`; (c′)'s conditional AC-4.2 (`rounds/r2-variant-3.md:19`; C-008 to V3, 90%, `debate-transcript.md:644`).
- **Target**: Base, Reliability (`V3:17`) (replace).
- **Rationale**: AC-4.2's `git log -1` runs at the repo root (`SPEC:202`), so it cannot see a commit made in the worker's worktree; `git log origin/<branch>` errors for a never-pushed branch and misses pushes to other refs.
- **Integration point**: AC-4.2 records, before and after the run, `git -C <worker worktree> log -1 --format=%H`, `git -C <worker worktree> for-each-ref refs/heads`, `git ls-remote origin` (all refs) and `gh pr list --repo IronbellyOrg/IronClaude --author @me`. Pass with no commit authorized: all four unchanged. Pass with a commit authorized: the only change is new commits on the worker's child branch, and `ls-remote` and the PR list are unchanged.
- **Risk**: Low. Test-only change.

### Change 8: State the option's own weaknesses where they bite (from Variant 1)
- **Source**: S-004 (V1, 95%, `debate-transcript.md:633`); V1's form at `V1:14-15`; conceded residuals (`invariant-probe.md:19-24`); A-006 (V1, 92%, `debate-transcript.md:660`); INV-012 (`invariant-probe.md:41`).
- **Target**: Base, new subsection after "How a person works day to day" (insert).
- **Rationale**: V3 stated no weakness of its own (conceded, `rounds/r2-variant-3.md:24`); every variant scored NOT MET on stating scope (Completeness 5, `base-selection.md:107`).
- **Integration point**: List: the commit still rests on the coordinator's quotation, which D2 would not accept for a Ruling (C-007 to V2, 97%); commits are per Orca Task, not per implement task, until K3; each committing worker leaves a branch the person must decide on (F3); inline auggie-review comments have no deferred posting path (`AUG:320-327`); the "never push" rule is enforced by instructions only, with no hook or permission rule (INV-012).
- **Risk**: Low. Additive.

### Change 9: Actionable spec edit list (from Variant 1 and Variant 3 decision points; corrected)
- **Source**: `V3:23`, `V1:24`; EVAL F0-F5 (`EVAL:50-55`); `rounds/r2-variant-3.md:99-102`; CR-01 section 3 (`CR-01:26-31`).
- **Target**: Base, Implementation cost (`V3:23`) (replace).
- **Rationale**: V2's "Zero beyond today's spec" was conceded false (`rounds/r2-variant-2.md:11`), and V3's list omitted the section 3 rows and the checks. F2 as written places worktrees under `.dev/worktrees/` (`EVAL:52`), which FC-1 forbids, so CR-01's wording replaces it.
- **Integration point**: Edits:
  - D4 text (`SPEC:345-348`).
  - WC-9 (`SPEC:73`): "Under `--unattended` every outward default (push, merge into a shared branch, PR, GitHub post, install on a shared or real target, VM, paid external run) is off, and no brief can turn it on (D4). The only git write a brief may authorize is the worker session's end-of-Task local commit under D4's commit rule." Drop the `README.md:31` citation and add the commit sentence.
  - WC-5 (`SPEC:69`): the failed-commit sentence from Change 3.
  - Section 2.3 (`SPEC:79`): change "which outward actions, if any, are authorized (WC-9)" to "whether the end-of-Task local commit is authorized, quoting the user's instruction word for word (D4); no other outward action can be authorized", and add the duties in Changes 5 and 6.
  - Section 3 rows: auggie-review (`SPEC:123`) "`--post-pr` is refused under `--unattended`; the coordinator posts the summary from `REVIEW.md` (D4)"; post-release (`SPEC:136`) "VM, real-target install, commit and PR always off under `--unattended` (D4)"; task (`SPEC:144`) "EXEMPT `commit` and `push` refused under `--unattended` (D4)"; implement (`SPEC:132`): no commit inside the command; per-task commits wait for K3 (replaces EVAL F1's implement-row sentence).
  - `/sc:git` row (`SPEC:156`): EVAL F0 wording.
  - AC-4.2 (`SPEC:275`): Change 7; plus one P0 acceptance check that a commit-authorized worker started with `--worktree new-child --base-branch <feature branch>` commits only on its child branch.
  - 7.2 setup (`SPEC:235`): replace "created under `.dev/worktrees/` (`CLAUDE.md:299`)" with "created by Orca at Orca's default path (`worker-start --worktree new-child --base-branch <feature branch>` or `orca worktree create`), never under `.dev/worktrees/`". 7.2 step 1 (`SPEC:236`): place the worker with that creation flag, or `--worktree id:<Orca worktree id>`, and delete the "whether Orca accepts a worktree it did not create is UNVERIFIED" clause. CR-01's four edits do not cover these lines (`CR-01:27-31`).
  - CR-01's four edits (`CR-01:28-31`) in place of EVAL F2; EVAL F3 is covered by CR-01's merge-back paragraph; F4 and F5 by Change 4. Cost of changing later: loosening to (a) is additive; tightening back to (b) is one sentence plus deleting the commit rule.
- **Risk**: Low. Lists edits; applies none.

### Change 10: Explicit out-of-scope list
- **Source**: Completeness criterion 5 NOT MET for all variants (`base-selection.md:107`).
- **Target**: Base, new short paragraph after the commit rule (insert).
- **Rationale**: The decision touches K3, D3, nested-command propagation and mechanical enforcement without deciding them.
- **Integration point**: Out of scope: the commit step inside `/sc:implement` (K3, `EVAL:63`); a hook or permission rule that blocks `git push` in worker sessions (INV-012; option E's optional guard G3, `round2-advocate-e.md:87`); how `--unattended` reaches nested commands (INV-011, `SPEC:145`); and running managed plan packages in a child worktree (INV-028).
- **Risk**: Low. Additive.

### Change 11: Correct the base's overstated claims
- **Source**: `rounds/r1-variant-3.md:37-38`; `diff-analysis.md:85` (A-009).
- **Target**: Base, Safety (`V3:13-14`) (replace).
- **Rationale**: "local and undoable (`git reset` on its own branch)" was false in a shared worktree (conceded). In a child worktree only this worker writes, the undo claim holds for that branch.
- **Integration point**: Replace with: a worker commit stays on its own child branch in a worktree no other worker writes, so it can be undone or discarded there, and nothing leaves the machine until the coordinator pushes after Change 5's review.
- **Risk**: Low.

## HIGH UNADDRESSED Invariant Coverage
The debate ended `BLOCKED_BY_INVARIANTS` with four HIGH items (`debate-transcript.md:693-712`). Each gets a planned change; none is left as accepted risk.

| ID | Problem (`invariant-probe.md` line) | Planned change | Residual after the change |
|---|---|---|---|
| INV-001 | Coordinator commits or merges in a worktree that running workers share move HEAD under them (`:30`) | Change 6 (1): the git owner commits or merges only into a worktree with no running worker; Change 6 (2): and never into any worktree, the shared feature worktree included, that holds a `blocked` or `partial` implement Task | Relies on the coordinator's placement record (Change 6 (4)); not mechanically enforced |
| INV-002 | A later commit in a reused worktree moves HEAD under an earlier `blocked` implement Task (`:31`) | Change 6 (2): no other Task in any worktree holding an implement Task ended `blocked` or `partial` until the person acts; Change 1 gives each committing Task its own child | None beyond coordinator correctness |
| INV-016 | AC-4.2's `git log -1` runs at the repo root and cannot see a worker-worktree commit (`:45`) | Change 7: the check runs `git -C <worker worktree>` and compares all local and remote refs | None for the check itself; it is still after-the-fact |
| INV-027 | Under the live-conversation exemption the coordinator can push unreviewed worker commits (`:56`) | Change 5: before any push that would publish a worker commit the person has not seen, the person sees those commits and says go, whatever was pre-authorized | One extra person step per push that carries new worker commits |

With these four changes planned, the invariant gate's blocking items each have a resolution, so the merged position can be treated as converged under `debate-transcript.md:714`. The changes are design rules: none has run live (UNVERIFIED).

## MEDIUM UNADDRESSED Invariants: Disposition
| ID | Short statement (`invariant-probe.md` line) | Disposition |
|---|---|---|
| INV-003 | Commit grant has no lifetime on a reused terminal (`:32`) | Fixed by Change 6 (3) |
| INV-004 | "Live conversation" undefined after compaction; no record of the instruction (`:33`) | Partly fixed: Change 6 (6) adds a section 2.3 duty to copy the user's instruction verbatim into the brief and the coordinator's run notes. After compaction the coordinator asks again before any outward step (Change 4). Residual accepted. |
| INV-005 | A fresh worktree lacks predecessors' outputs and untracked inputs (`:34`) | Mostly fixed by CR-01: children branch from the feature branch and run setup before dispatch (`CR-01:22,24`). Untracked inputs stay a residual; CR-01 open question 2 (`CR-01:42`) owns it. |
| INV-007 | "Own worktree" exclusivity is asserted by the coordinator only (`:36`) | Accepted risk, reduced: CR-01 creates one child per committing Task, and the commit tripwire (Change 3 step 3) refuses when an unknown path appears. |
| INV-008 | No default-branch detector; detached HEAD escapes the guard (`:37`) | Fixed by Change 3 step 2 |
| INV-009 | No rule for commit hooks that fail or rewrite files (`:38`) | Fixed by Change 3 steps 4-5 and the failure path |
| INV-010 | A failed commit still reports outcome `succeeded` (`:39`) | Fixed by Change 3's failure path and the WC-5 sentence in Change 9 |
| INV-011 | `--unattended` propagation to nested commands is unspecified (`:40`) | Out of scope (Change 10); belongs to D1 and the section 3 rows |
| INV-012 | "Never push" is enforced by prose only (`:41`) | Accepted risk, stated in Change 8 and Change 10; option E's optional guard G3 is the later fix |
| INV-015 | `artifacts` cannot hold a SHA; editing the contract after commit dirties the worktree (`:44`) | Fixed by Change 3 (SHA in the `worker_done` body; branch log is authoritative) |
| INV-017 | `git log origin/<branch>` misses other refs and errors for new branches (`:46`) | Fixed by Change 7 (`git ls-remote origin`, all refs) |
| INV-018 | Staging set undefined, may be empty or ignored (`:47`) | Fixed by Change 3 steps 3-4 and the empty-commit failure path |
| INV-020 | Relative report paths resolve inside each child worktree (`:49`) | Partly fixed: Change 6 (7) makes the brief pass an absolute report directory when the Task runs in a child worktree. Fan-in across unmerged branches stays a CR-01 merge-back matter. |
| INV-023 | D3 (b) cannot coexist with this D4 answer (`:52`) | Fixed by Change 4's coupling sentence |
| INV-025 | Implement refs are shared across worktrees; same slug collides (`:54`) | Reduced by Change 6 (5) (option E rule G2: distinct slugs across concurrent worktrees); residual accepted for two runs of the same plan |
| INV-028 | Managed plan packages fail closed in a child worktree (`:57`) | Out of scope (Change 10); fails closed, so not a safety breach |

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| X-001, C-001 | V1 (a): a brief may authorize a named worker push, PR, post, install or paid run | V1 conceded every action that leaves the machine (`rounds/r2-variant-1.md:7-15`); X-001 to V2 = V3 at 97%, C-001 to V3 at 96% (`debate-transcript.md:637,652`). (a) stays a later, additive loosening. |
| X-002, C-014 | V2 (b): no worker commits at all | X-002 to V3 at 96% (`debate-transcript.md:653`); V2's own advocate moved to (c′) (`rounds/r2-variant-2.md:90`, quoted at `debate-transcript.md:721`). (b) is kept as the default and fallback (Change 1), not as the rule. |
| C-006 | V1 and V2 Round 2: a brief may switch on `/sc:task`'s own EXEMPT `commit` step | V3's revision keeps every command's own commit step off (`rounds/r2-variant-3.md:37`; recorded as the consensus at `invariant-probe.md:13`), because `PRL:351` requires same-session confirmation for committing and a task EXEMPT commit has none of Change 3's guards. |
| X-006 | V3 original: commit inside `/sc:implement` between tasks | Not a non-base approach but the base's own conceded error; dropped by Change 2. |
| git-ownership E rule W3 (not a D4 diff point) | Commits at a command's own authorized commit step (`/sc:task`), and between implement tasks once K3 exists (`round2-advocate-e.md:79`) | **Conflict, stated explicitly.** D4 keeps command commit steps off under `--unattended`; E allows `/sc:task`'s. The D4 rule is kept for the reason in the C-006 row. E's between-implement-tasks timing is compatible but has no mechanism until K3, so today both rules produce the same single end-of-Task commit. The git-ownership text should adopt D4's narrower wording for `/sc:task`. |
| git-ownership E rule W6 SHA location (not a D4 diff point) | Each SHA listed in the contract's `artifacts` (`round2-advocate-e.md:82`) | **Conflict, stated explicitly.** INV-015 shows `artifacts` holds files and a post-commit edit dirties the worktree; Change 3 puts the SHA in the `worker_done` body and treats the branch log as authoritative. |
| git-ownership E rules W5 and W6 failure status (not a D4 diff point) | A tripwire hit reports `blocked`; a hook failure gives `partial` or `blocked` (`round2-advocate-e.md:81-82`) | **Conflict, stated explicitly.** The command writes the contract before the commit (WC-4, `SPEC:68`) and D4 does not edit it afterwards, so a refused or failed commit is reported as `worker_done --outcome failed` with "`worker_status: succeeded`; commit not made" and the reason in the body's first sentence (Change 3). The git-ownership text should adopt this wording. |
| git-ownership E rule O3 (not a D4 diff point) | Opt-in: one pr-submit worker Task per PR when the user asks for parallel PR monitoring (`round2-advocate-e.md:66`; the one exception E's G1 allows, `:85`) | **Conflict, stated explicitly.** D4 keeps every push and PR at the coordinator, so O3 is unavailable while this D4 answer holds. It needs D3 (b) and D4 (a). The git-ownership text should mark O3 as gated on both. |
| git-ownership E rule C2 and (c′) placement (not D4 diff points) | Worktrees created under `.dev/worktrees/` (`round2-advocate-e.md:70`; `rounds/r2-variant-3.md:92`) | Overridden by fixed constraint FC-1 (`CR-01:41`). |
| A-006 | V1: only (a) avoids deferring post-release's real-target install and the inline auggie-review comments | V1 wins the point (92%, `debate-transcript.md:660`), but all three narrowed its cost to a convenience (`AUG:319`); listed as a weakness in Change 8, not adopted. |
| C-003, C-007, C-009, C-013 | V2: properties (b) has unconditionally (zero HEAD risk, one provenance rule, lowest cost, safest to change later) | V2 wins each point (`debate-transcript.md:639,643,645,649`). They are recorded as the costs of (c′) in Change 8 and as the fallback in Change 1, not merged as rules, because adopting them would remove the authorized commit #326 asks for (`EVAL:19`). |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | If `--worktree new-child` does not work live, no commit can ever be authorized | Option (b) applies automatically (built into the rule) |
| 2 | Medium | #326 gets one commit per Orca Task, not per implement task | None needed; K3 refines it later |
| 3 | Medium | A misdefined tripwire refuses valid commits | Work stays uncommitted in the child worktree; the coordinator commits it there at quiescence (E rule C1) |
| 4 | Low | D3 (b) becomes unavailable while this D4 answer holds | Choose D4 (a) later if parallel PR monitoring is needed |
| 5 | Medium | Adds one person review per pushed branch | Remove the sentence; `HWW:282` still requires showing the lead |
| 6 | Medium | Coordinator duties may be skipped (no mechanical check) | Revert to the base Reliability text |
| 7 | Low | Check commands need adjustment once run live | Revert AC-4.2 to its current text |
| 8 | Low | None (documentation) | Remove the subsection |
| 9 | Low | Edit list incomplete | Add missing edits at spec revision |
| 10 | Low | None (documentation) | Remove the paragraph |
| 11 | Low | None | Restore the base sentence |

## Review Status
- [x] Auto-approved (default; `--interactive` was not set)
- [ ] User-approved (--interactive)
- Approved by: auto, after the Step 4 analytical review below
- Approval timestamp: 2026-11-02 (resumed run; exact time recorded in `merge-log.md`)
- Analytical review: `refactor-plan-review.md` (fresh general-purpose reviewer, adversarial start; severity per PR #343). First review FAIL with 6 blocking findings (B1-B6) and 9 minor notes. Fix cycle 1 of 2 applied B1-B6. Re-review PASS: all six resolved, no new blocking problem; three new minor notes (N1-N3). Minor notes were not fixed or rechecked, per PR #343.
