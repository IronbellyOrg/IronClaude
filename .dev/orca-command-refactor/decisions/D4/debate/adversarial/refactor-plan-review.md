# Step 4 Analytical Review: D4 Refactoring Plan

Reviewed file: `refactor-plan.md` (172 lines, read 2026-11-02). Reviewer did not write the plan. Severity rule (FC-3, merged PR #343): only BLOCKING findings fail; MINOR findings are notes and are not rechecked.

## Verdict

**FAIL**: 6 blocking findings. The plan covers every scoring-matrix strength and every MEDIUM invariant, and the base choice holds. But it does not fully resolve two of the four HIGH invariants (INV-001, INV-027). Its spec edit list leaves a `.dev/worktrees/` placement in the spec (FC-1) and leaves worker outward actions open to brief authorization, which contradicts its own Change 4. Three conflicts with git-ownership option E are not stated (FC-5). Two changes contradict each other on where the report directory lives and what the commit may stage.

## Blocking findings

### B1. The spec edit list leaves the `.dev/worktrees/` placement at SPEC:235 (fixed constraint 1)
- **Location in plan:** FC-1 row (plan line 20) and Change 9 (plan lines 84-89).
- **Problem:** FC-1 says it "Replaces ... the 7.2 disposable worktree path (`SPEC:235`)", but no planned change makes that edit. Change 9 lists "CR-01's four edits in place of EVAL F2". CR-01's four edits (section 2.3 placement, WC-11, the "Feature worktree" paragraph, one section 7 check) do not touch SPEC:235, and CR-01 says "Keep additions to these four places; add no other rule". CR-01's repo-wide `.dev/worktrees/` refactor covers "17 tracked files outside `.dev/`", and the spec is inside `.dev/`. So no edit list anywhere changes SPEC:235, and after the merge the spec still creates the 7.2 worktree "under `.dev/worktrees/` (`CLAUDE.md:299`)". SPEC:236 also still passes `--worktree path:<disposable worktree>` with the "whether Orca accepts a worktree it did not create is UNVERIFIED" note that FC-1 says is gone.
- **Evidence:** `SPEC:235` ("created under `.dev/worktrees/` (`CLAUDE.md:299`)"); `SPEC:236`; `CR-01:27` ("Keep additions to these four places"); `CR-01:28-31` (the four edits); `CR-01:41` ("17 tracked files outside `.dev/`"; "This also replaces the 7.2 disposable worktree").
- **Exact fix:** Add to Change 9's edit list: "7.2 setup (`SPEC:235`): replace 'created under `.dev/worktrees/` (`CLAUDE.md:299`)' with 'created by Orca at Orca's default path (`worker-start --worktree new-child --base-branch <feature branch>` or `orca worktree create`), never under `.dev/worktrees/` (CR-01 open question 1)'. 7.2 step 1 (`SPEC:236`): place the worker with that creation flag, or with `--worktree id:<Orca worktree id>` for a worktree Orca created, and delete the 'whether Orca accepts a worktree it did not create is UNVERIFIED' clause."

### B2. The edit list keeps brief-authorized worker push, PR, post and install, which contradicts Change 4 and option E rule O1
- **Location in plan:** Change 9 (plan line 88), with Change 2 (line 38) and Change 4 (line 53).
- **Problem:** Change 4 says that everything that leaves the machine stays with the coordinator, which matches option E rule O1. Change 9 edits WC-9 only to "drop `README.md:31`, add the commit sentence". It edits the post-release and task rows only to "commit off under `--unattended`". The spec text that lets a brief switch outward actions on in a worker stays in place:
  - WC-9: "It turns on only through the command's own explicit flag written in the brief" (`SPEC:73`).
  - Section 2.3: "which outward actions, if any, are authorized (WC-9)" (`SPEC:79`).
  - auggie-review row: "posting returns only with an explicit `--post-pr` in the brief (WC-9)" (`SPEC:123`). This row is not in the edit list at all.
  - post-release row: "VM, real-target install, commit and PR off unless the brief authorizes them" (`SPEC:136`).
  - task row: EXEMPT `push` "refused unless authorized (WC-9)" (`SPEC:144`).

  If the merge executor applies Change 9 as written, the D4 text says workers never act outward while WC-9 and four rows say a brief can authorize it. The debate already found these rows: V2 conceded that `SPEC:73`, `:79`, `:123`, `:136`, `:144` and `:342` need "never" wording. Option E's G1 also lists the `SPEC:144` push refusal as a required spec change.
- **Evidence:** `SPEC:73`, `SPEC:79`, `SPEC:123`, `SPEC:136`, `SPEC:144`; `rounds/r2-variant-2.md:11`; `rounds/r2-variant-1.md:11` (point 5); `round2-advocate-e.md:85` (G1).
- **Exact fix:** Replace Change 9's WC-9, 2.3 and section 3 items with:
  - WC-9: "Under `--unattended` every outward default (push, merge into a shared branch, PR, GitHub post, install on a shared or real target, VM, paid external run) is off, and no brief can turn it on (D4). The only git write a brief may authorize is the worker session's end-of-Task local commit under D4's commit rule." Keep the `README.md:31` removal and the commit sentence.
  - 2.3 (`SPEC:79`): change "which outward actions, if any, are authorized (WC-9)" to "whether the end-of-Task local commit is authorized, quoting the user's instruction (D4); no other outward action can be authorized".
  - auggie-review row (`SPEC:123`): "`--post-pr` is refused under `--unattended`; the coordinator posts the summary from `REVIEW.md` (D4)".
  - post-release row (`SPEC:136`): "VM, real-target install, commit and PR always off under `--unattended` (D4)".
  - task row (`SPEC:144`): "EXEMPT `commit` and `push` refused under `--unattended` (D4)".

### B3. Change 5 reviews only the first push, so INV-027 stays open for every later push
- **Location in plan:** Change 5 integration point (plan line 60); HIGH table row INV-027 (line 113).
- **Problem:** The rule applies "Before the first push of any branch that contains worker commits". Suppose a feature branch is pushed once after child A's commits were shown to the person. Child B's worker commits are then merged into the feature branch (`CR-01:23`). The coordinator's next plain `git push` publishes B's commits, which no person has seen, under `PRL:351`'s live-conversation exemption. That is exactly the INV-027 falsifier. pr-submit's own push-range guard does not cover the coordinator's plain push. `<base>` in `git log --stat <base>..<branch>` is also undefined.
- **Evidence:** `invariant-probe.md:56` (INV-027: the coordinator can push worker commits no person reviewed); `invariant-probe.md:74` (G10); `CR-01:23` (children are merged into the feature branch after admission); `HWW:282`.
- **Exact fix:** Replace Change 5's first sentence with: "Before any push that would publish a worker commit the person has not yet seen, the coordinator shows the person every such commit (`git log --stat origin/<branch>..<branch>`, or `git log --stat <feature base>..<branch>` for a branch never pushed) and pushes only on a go the person gives after seeing them. No earlier pre-authorization waives this, and it applies to every push, not only the first." Update the INV-027 row to match.

### B4. The quiescence rules leave INV-001's blocked-implement case open in the shared feature worktree
- **Location in plan:** Change 6 items (1) and (2) (plan line 67); HIGH table rows INV-001 and INV-002 (lines 110-111).
- **Problem:** INV-001 covers a git-owner commit or merge made "while an `/sc:implement` worker is inside a task window". Item (1) forbids a git-owner commit or merge only "when [a] worker is running there". Item (2) protects a `blocked` or `partial` implement Task only in a child worktree. A non-committing implement worker shares the feature worktree whenever T1-T4 do not apply (WC-11; `CR-01:16-20`). Say it halts `blocked` there, and the git owner then merges an admitted child branch into that same worktree (`CR-01:23`). No worker is running, so item (1) allows the merge, and item (2) does not apply because it is not a child worktree. The person's later resume then halts `head-moved`. The D2 consensus this plan cites in its Change 6 sources says the coordinator "dispatches no other writer into that worktree until the resume Task settles". The INV-001 row says this case is resolved, and it is not.
- **Evidence:** `invariant-probe.md:30` (INV-001: "while an `/sc:implement` worker is inside a task window"); `RETRY:41`, `RETRY:44` (a resume through row O halts `head-moved`); `CR-01:16-20`, `CR-01:23`; `decisions/D2/debate/adversarial/invariant-probe.md:14` (consensus item 4).
- **Exact fix:** Replace item (2) with: "(2) In any worktree, the shared feature worktree included, that holds an `/sc:implement` Task ended `blocked` or `partial`, the git owner makes no commit or merge and the coordinator dispatches no other Task until the person has resumed or discarded that work. The merge-back of other children into that worktree waits." Cite this item in both the INV-001 and INV-002 rows.

### B5. Three conflicts with git-ownership option E are not stated (fixed constraint 5)
- **Location in plan:** FC-5 row (plan line 24, which says "two E rules conflict"), Change 1 (line 32), Change 3 (lines 46-47), Change 4 (line 53), and "Changes NOT Being Made" (lines 145-147).
- **Problem:** FC-5 requires the plan to be consistent with E or to state each conflict. The plan states W3, W6 (where the SHA is recorded) and C2. It leaves out three more:
  1. **E rule O3 against Change 4.** O3 is the opt-in that runs one pr-submit worker Task per PR when the user asks for parallel PR monitoring. G1 lists O3 as the one exception to "a worker never ... touches a remote". All five git-ownership advocates converged on it (93%). Change 4 rules D3 (b) out while this D4 answer holds, which removes O3.
  2. **E rule W2 and new evidence N4 against Change 1.** W2 lets a sole writer be placed "new, or by exact selector for a resume", and N4 says a rule requiring `new-*` "would wrongly bar those Tasks from the commit lane". Change 1 condition (2) requires that the worker was started with `worker-start --worktree new-child`. Change 6 (3) requires a resume Task to carry its own grant, but that resume Task can never meet condition (2) in the existing child worktree. The merge executor would have to decide which rule wins.
  3. **E rules W5 and W6 against Change 3's failure path.** In E, a tripwire hit "reports `blocked`", and a hook failure gives `partial` or `blocked`. Change 3 instead leaves the contract's `worker_status: succeeded` and sends `worker_done --outcome failed`. Change 3's Risk line names only the change to where the SHA is recorded.
- **Evidence:** `round2-advocate-e.md:66` (O3), `:78` (W2), `:81` (W5), `:82` (W6), `:85` (G1), `:99` (N4); `debate-transcript.md:1297` in `decisions/git-ownership/debate/adversarial/` (C-003, all five, 93%); `git-ownership/.../invariant-probe.md:38` (INV-030: O3 is a second G1 exception).
- **Exact fix:** Add three rows to "Changes NOT Being Made", each marked **Conflict, stated explicitly**:
  - O3: D4 keeps every push and PR at the coordinator, so O3 is unavailable until D4 is loosened to (a). The git-ownership text should mark O3 as gated on D3 (b) and D4 (a).
  - W2 and N4: either amend Change 1 condition (2) to "started in its own Orca-created child worktree, with `--worktree new-child --base-branch <feature branch>` for a new Task or `--worktree id:<that child's id>` for a resume Task in the same child, with no other writer recorded there", or state that resume Tasks never commit and that E's W2 resume placement is narrowed.
  - W5 and W6 failure status: D4 reports a refused or failed commit as `worker_done --outcome failed` with `worker_status: succeeded; commit not made` in the first sentence, because the command-written contract (WC-4) is not edited. The git-ownership text should adopt this wording.

  Change FC-5's "two E rules" to the actual count.

### B6. Change 3's commit set and Change 6 (7)'s absolute report directory contradict each other
- **Location in plan:** Change 3 steps (3) and (4) (plan line 46); Change 6 item (7) (line 67); INV-020 disposition (line 132).
- **Problem:** Step (3) refuses the commit if `git status --porcelain` shows any path outside "the contract's `report_path` and `artifacts`, plus `.dev/tasks`". Step (4) stages those paths. Item (7) gives a Task in a child worktree "an absolute report directory" but does not say where it is. INV-020's problem is the coordinator reading the contract from its own checkout, which points toward a directory outside the child, and `git add` cannot stage a path outside the child worktree. If the directory is inside the child, the command writes `<report-dir>/return-contract.yaml` (WC-4). WC-4 defines `artifacts` as "every other file written" besides `report_path`, so whether the contract file is in the allowed set is unclear. In both cases the commit can be refused on every run, and the merge executor has to make the placement decision itself.
- **Evidence:** `SPEC:68` (WC-4: contract at `<report-dir>/return-contract.yaml`; `artifacts` = "every other file written"); `invariant-probe.md:49` (INV-020); `invariant-probe.md:47` (INV-018).
- **Exact fix:**
  - In Change 6 (7), write: "A Task placed in a child worktree gets an absolute report directory inside that child worktree; the coordinator reads the contract there by absolute path before merge-back."
  - In Change 3 step (3), define the allowed set as: "every path under the brief's report directory (including `return-contract.yaml`), `report_path`, `artifacts`, and `.dev/tasks`". Paths in that set that lie outside the child worktree are left out of staging and do not cause a refusal.

## Minor findings

- **M1 (Change 7).** AC-4.2's command is post-release "with no authorization flags" (`SPEC:275`), so the "Pass with a commit authorized" case needs its own named check. "Before the run" is undefined when Orca creates the child worktree at `worker-start`: take the snapshot after the worktree is created and before dispatch. `git ls-remote origin` over all refs can fail falsely if anyone else pushes during the check, so scope the comparison or note it.
- **M2 (Change 1 and Change 9).** Change 1's P0 live check that `--worktree new-child` works ("until it passes no commit authorization is valid") is not in Change 9's edit list. CR-01's section 7 check exercises a child worktree only indirectly. Add an explicit P0 acceptance check.
- **M3 (citation keys).** The plan uses `TASK`, `MW`, `AUG`, `QA`, `CR-01` and `RETRY` but defines only `V1-V3` (plan line 4). Add a key line that points to `diff-analysis.md:12` and `rounds/r2-variant-3.md:3`.
- **M4 (Change 3 step 2).** The plan does not say what happens when `git symbolic-ref refs/remotes/origin/HEAD` fails (it should refuse). A shared `integration` branch, INV-008's third case, is still not covered.
- **M5 (INV-010).** The `consumer_fenced`-after-commit half of INV-010 (`SPEC:76`) is not named. The branch-log rule mitigates it, but the disposition should say so.
- **M6 (Change 9).** The plan gives no disposition for EVAL F1's implement-row sentence (`SPEC:132`), which V3's own list included (`V3:23`). F3, F4 and F5 are covered only implicitly, through CR-01 and Change 4.
- **M7 (Risk row 3, Change 6 (1)).** "The coordinator commits it there at quiescence (E rule C1)" does not carry C1's mechanics: compare `git status --porcelain` with the settled contracts, use `--only`, and never `--no-verify` (`round2-advocate-e.md:69`).
- **M8 (Change 3 step 3).** Untracked, non-ignored files created by child setup (`--setup run`; `CR-01:42` UNVERIFIED) would trip the tripwire. Note it as a residual.
- **M9.** `SPEC:66` (WC-2) supports only the worker half of "the coordinator is the one session that can still ask the person"; `PRL:351` carries the coordinator half.

## Citations checked

| # | Citation (as used in the plan) | Claim it supports | Result |
|---|---|---|---|
| 1 | `base-selection.md:153` | V3 named as base | CONFIRMED |
| 2 | `base-selection.md:80` | Alt-SR combined scores 0.7504 / 0.7522 / 0.7871, base unchanged | CONFIRMED (arithmetic re-derived: qual 19 / 18 / 20 of 30; main-formula 0.7804 / 0.7850 / 0.8106) |
| 3 | `base-selection.md:23` | quant 0.9275 / 0.9700 / 0.9544 | CONFIRMED |
| 4 | `base-selection.md:132-163` | 11 TODO sections | CONFIRMED |
| 5 | `qual-pass-1.md:57,59,67` vs `qual-pass-2.md:57,59,67` | four disagreeing cells (V3 Risk 2, V1 Risk 4, V3 Risk 4, V3 Inv 2) | CONFIRMED (V3 range 19-22 re-derived) |
| 6 | `debate-transcript.md:663` | V3 sole 13, V2 sole 5 | CONFIRMED |
| 7 | `debate-transcript.md:653`, `:657`, `:652`, `:633`, `:660`, `:644`, `:637`, `:639,643,645,649` | X-002, X-006, X-001, S-004, A-006, C-008, C-001, C-003/7/9/13 winners and confidences | CONFIRMED |
| 8 | `debate-transcript.md:693-712`, `:714`, `:720-722` | BLOCKED_BY_INVARIANTS; handling note; advocates' recommendations | CONFIRMED |
| 9 | `invariant-probe.md:30-57` (rows cited by line) | INV-001 to INV-028 statements and severities | CONFIRMED (every row in the HIGH and MEDIUM tables matches its line) |
| 10 | `invariant-probe.md:13`, `:19-24`, `:69-74` | consensus on command commit steps; residuals; gates G5-G10 | CONFIRMED |
| 11 | `CR-01:16-17`, `:22-24`, `:29`, `:41`, `:42`, `:45`, `:48` | T1, branching, setup, WC-11 edit, location decision, setup UNVERIFIED, upstream rule, `--help` evidence | CONFIRMED |
| 12 | `CR-01:26-31` cited as covering FC-1's SPEC:235 replacement (via Change 9) | the four edits replace F2 and the 7.2 path | WRONG for SPEC:235: the four edits do not touch it (B1). Load-bearing for FC-1. |
| 13 | `round2-advocate-e.md:63-87`, `:64`, `:69-71`, `:79-82`, `:86-87`, `:94` | E rules O1, C1-C3, W3-W6, G2, G3, N2 | CONFIRMED (the cited lines hold the rules; O3 at `:66`, W2 at `:78` and N4 at `:99` are in the same range but their conflicts are not stated, B5) |
| 14 | `decisions/git-ownership/option-e.md:8-14` | E ownership table | CONFIRMED |
| 15 | `git log -1 80f934de` | only blocking findings fail; at most 2 fix cycles | CONFIRMED |
| 16 | `CLAUDE.md:39-48`, `:50`, `:37` | fork-only rule; PRs via `/sc:pr-submit --monitor 3`; `.dev/tasks` staged, commit only when asked | CONFIRMED |
| 17 | `SPEC:68`, `:69`, `:73`, `:75`, `:79`, `:136`, `:144`, `:145`, `:156`, `:202`, `:235`, `:236`, `:275`, `:276`, `:345-348` | as used | CONFIRMED (each line says what the plan attributes to it) |
| 18 | `SPEC:66` | coordinator is the session that can ask | CONFIRMED, partial (worker half only; M9) |
| 19 | `PRL:351` | "committing" confirm-first "this session" | CONFIRMED |
| 20 | `HWW:282`, `HWW:324` | commit locally, push on go, monitor 3 pushes fixes; `/sc:git` commit needs authorization | CONFIRMED |
| 21 | `RETRY:44` | resume halts `head-moved` | CONFIRMED |
| 22 | `sc-pr-submit-protocol/SKILL.md:274` | `git commit --only -- <paths>` | CONFIRMED |
| 23 | `TASK:61`, `TASK:266` | EXEMPT commit/push; TFEP report committed | CONFIRMED |
| 24 | `MW:63,67` | FINAL is not a commit; acceptance never authorizes commit | CONFIRMED |
| 25 | `AUG:319`, `AUG:320-327` | summary from `REVIEW.md`; inline comments | CONFIRMED |
| 26 | `EVAL:19`, `:50-55`, `:52`, `:63` | #326 per-task commits; F0-F5; F2 under `.dev/worktrees/`; K3 | CONFIRMED |
| 27 | `rounds/r2-variant-3.md:9,10,12,19,24,30,37-38,92,99-102` | (c′) conditions, end-of-Task commit, conditional AC-4.2, V2 framing, spec edits | CONFIRMED |
| 28 | `rounds/r1-variant-3.md:37-38` | V3 concessions (X-006, "undoable") | CONFIRMED |
| 29 | `rounds/r2-variant-1.md:7-15`; `rounds/r2-variant-2.md:11`, `:90` | V1 concessions; "Zero" conceded; V2 recommends (c′) | CONFIRMED |
| 30 | `diff-analysis.md:80,85` | A-004, A-009 contradicted | CONFIRMED |
| 31 | `V1:14-15`; `V3:3,5,13-14,17,23` | V1 weakness statement; base text targets | CONFIRMED |
| 32 | D2 `invariant-probe.md` "Emerging consensus" item 4 | no other writer into a halted worktree | CONFIRMED (line 14); this source is what B4 relies on |

Result: 31 citations CONFIRMED (one only partially), 1 WRONG (row 12, load-bearing, raised as B1).

## Self-Audit

- **Starting position:** I assumed the plan had mistakes. I checked each change against the debate record, the invariant probe and the five fixed constraints, not against the plan's own claims.
- **Check 1 (scoring-matrix strengths):** I listed every point a non-base variant won from `debate-transcript.md:628-661`: S-004, A-006, C-003, C-007, C-009, C-013, X-006, plus the shared V2 = V3 points C-004, C-005, C-011, X-001, X-003, X-004 and A-003. Each has a planned change (Changes 1, 2, 4, 8) or a "Changes NOT Being Made" row with a reason. **Passed.**
- **Check 2 (HIGH invariants):**
  - INV-016 is resolved by Change 7. The snapshot timing is a minor gap (M1).
  - INV-002 is resolved for child worktrees.
  - INV-001 is not fully resolved. The plan's "running" test misses a halted implement Task in the shared feature worktree (B4). I confirmed the halt-on-resume behaviour at `RETRY:41,44`, and the D2 consensus already requires the stricter rule.
  - INV-027 is not fully resolved, because only the first push is gated (B3).
  - All 16 MEDIUM items have a disposition; I compared them line by line with `debate-transcript.md:701`.
- **Check 3 (fixed constraints):**
  - FC-2: I searched the plan for upstream or bare `gh` use and found none; every `gh` call names `--repo IronbellyOrg/IronClaude`. **Honoured.**
  - FC-3: honoured.
  - FC-4: honoured. Change 1 uses CR-01 T1.
  - FC-1: a leftover `.dev/worktrees/` placement survives at `SPEC:235` because no edit list covers it (B1). I grepped the spec: `SPEC:235` is its only `.dev/worktrees` occurrence. I read CR-01 section 3 and open question 1 to confirm the gap.
  - FC-5: B2 covers the O1 contradiction left in the spec edit list, and B5 covers the three unstated E conflicts. I found them by reading E's final rule set (`round2-advocate-e.md:61-87`) and checking the git-ownership transcript and probe for O3.
- **Check 4 (citations):** I read 32 citation groups at their cited lines, using direct Reads and one bounded read-only batch script. Only one failed to support its claim (row 12). It is load-bearing, so it is graded blocking and raised as B1. I re-derived the Step 3 base-selection arithmetic and the four-cell disagreement range myself; the base choice (V3) is correct.
- **Check 5 (contradictions and strategic decisions):**
  - B6 needs the executor to choose where the report directory lives.
  - B5 (2) needs a choice on resume Tasks.
  - B2 leaves the D4 text and WC-9 saying opposite things.
- **Grading:** I graded a finding blocking only when the merged rule would be wrong or unsafe (B2, B3, B4), a fixed constraint is broken (B1, B5), or the executor would have to make a strategic choice (B6). Wording gaps, test-detail gaps and non-load-bearing citation issues are minor (M1-M9).
- **What I did not check:** I did not re-run the debate or rescore. I did not verify Orca CLI behaviour live. I did not check the in-progress git-ownership `merged-output.md` (its sections are empty stubs as of 18:06), so B5 is judged against `round2-advocate-e.md`, the source the plan itself cites for E.

## Re-review (fix cycle 1)

Scope: B1-B6 only, plus any new blocking problem the fix-cycle edits introduced (FC-3: minor findings are not rechecked). I re-read the whole of `refactor-plan.md`, now 183 lines; the plan line numbers below are from that version.

**Verdict: PASS.** All six blocking findings are resolved and the edits introduced no new blocking problem.

| Finding | Status | Evidence in the revised plan |
|---|---|---|
| B1 (`.dev/worktrees/` left at SPEC:235) | RESOLVED | Change 9, plan line 96: SPEC:235 now reads "created by Orca at Orca's default path ... never under `.dev/worktrees/`". SPEC:236 places the worker with the creation flag or `--worktree id:<Orca worktree id>` and drops the UNVERIFIED clause. The edit also notes that CR-01's four edits do not cover these lines (`CR-01:27-31`, re-read). No `.dev/worktrees/` placement remains except as overridden text (lines 20, 87, 158). |
| B2 (brief-authorized worker outward actions left in the spec) | RESOLVED | Change 9 now rewrites WC-9 so "no brief can turn it on" (line 90) and changes the 2.3 authorization item (line 92). It also rewrites the auggie-review (`SPEC:123`), post-release (`SPEC:136`), task (`SPEC:144`) and implement (`SPEC:132`) rows (line 93). These match Change 4 and option E rule O1. |
| B3 (only the first push reviewed) | RESOLVED | Change 5, line 60: the review applies "before any push that would publish a worker commit the person has not yet seen ... it applies to every push, not only the first". It names the range commands for pushed and never-pushed branches. The INV-027 row (line 122) matches. The carve-out for pr-submit fix pushes holds, because pr-submit's own push-range guard allows only the cycle's fix commit (`sc-pr-submit-protocol/SKILL.md:274`, read in the first review). |
| B4 (blocked implement Task in the shared feature worktree) | RESOLVED | Change 6 (2), line 67, covers "any worktree, the shared feature worktree included". It blocks commits, merges and other Tasks until the person acts, and makes merge-back wait (D2 consensus item 4). The INV-001 and INV-002 rows (lines 119-120) both cite it. |
| B5 (three unstated E conflicts) | RESOLVED | Resume placement: Change 1 condition (2), line 32, now allows `--worktree id:<that child's id>` for a resume Task in the same child, citing E W2/N4 (`round2-advocate-e.md:78,99`, re-read). New "Changes NOT Being Made" rows state the W5/W6 failure-status conflict (line 156) and the O3 conflict (line 157), each with a recommendation for the git-ownership text. The FC-5 row (line 24) now counts five conflicts, and each has a row (lines 154-158). |
| B6 (report directory and commit set) | RESOLVED | Change 6 (7), line 67, puts the absolute report directory inside the child worktree. Change 3 step (3), line 46, defines the allowed set as every path under that directory (including `return-contract.yaml`), plus `report_path`, `artifacts` and `.dev/tasks`. Step (4) stages only the allowed-set paths inside the child. The two changes now agree. |

New problems introduced by the edits (none blocking):
- **N1 (minor).** Risk Summary row 5 (line 170) still says "one person review per pushed branch". After B3 the review is per push that carries unseen worker commits, as the INV-027 row says (line 122). Wording only.
- **N2 (minor).** Change 6 (2) says the coordinator "dispatches no other Task" into such a worktree. In the shared feature worktree that also holds back report-only workers, which cannot move HEAD. It is stricter than D2 consensus item 4 ("no other writer"), but it fails safe. It also does not say outright that the person's own resume Task is exempt, though "until the person has resumed" implies it.
- **N3 (minor).** Change 3 step (4) stages every path under the report directory. If a brief points the report directory at an ignored path, `git add` fails. Change 3's failure path still reports `outcome failed`, so this is not unsafe; it is the residual already recorded under INV-018.

Fixed constraints re-checked against the revised text:
- FC-1: no `.dev/worktrees/` placement is left.
- FC-2: every `gh` call still names `--repo IronbellyOrg/IronClaude`, and there is no upstream interaction.
- FC-4: committing workers still get their own child worktree.
- FC-5: every conflict with option E is now stated.
