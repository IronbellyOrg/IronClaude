# D4 Round 1: Variant 3 advocate (option (c))

Citation keys as in `diff-analysis.md:12` (`SPEC`, `PRL`, `HWW`, `EVAL`, `RETRY`, `MW`, `QA`, `V1`-`V3`); `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `TASK:N` = `src/superclaude/skills/sc-task-protocol/SKILL.md:N`. All re-read on this branch on 2026-11-02.

## Position summary
Nothing that leaves the machine is ever done by a worker; a brief may authorize local commits only. The diff analysis shows the original wording is unsafe in a shared worktree (A-004, A-009) and assumes an implement commit step that does not exist (X-006, A-005), so I refine it to **(c′)**: a commit authorization is valid only when the coordinator has also placed the worker in its own worktree on its own feature branch, and the worker commits once, at the end of a `succeeded` Task, never inside `/sc:implement` until #326's K3 adds that step.

## Steelman
### Variant 1 (option (a))
V1's best case: the repo already recognises pre-authorization ("unless the user pre-authorized them this session", `PRL:351`; "or standing authorization", `PRL:340`, which has no session qualifier). Only V1 lets a worker deliver post-release's whole value, the new-user install run "to green on the classified target" (`PRL:333`; U-001). It keeps every action behind an explicit per-command flag (`SPEC:123`), so nothing turns on by default, and it is honest about its own gap (`V1:14-15`).

### Variant 2 (option (b))
V2's best case: one rule, no exceptions, already in the spec (`SPEC:73`, `SPEC:156`), tested by AC-4.2 as written (`SPEC:275`). It applies the same provenance rule as D2: "another agent's message ... not acceptance" (`QA:254`). A worker never moves HEAD, so implement's retry ladder (`RETRY:41`) and other workers in a shared worktree (`SPEC:75`) are never at risk. And its cost argument is sound: loosening later is additive, tightening after an incident is not (`V2:23`).

## Strengths claimed
1. **It is the repo's existing rule for people, applied to workers.** "Commit locally on the feature branch only when authorized" (`HWW:212`); "Never push without approval. Commit locally ... push only when they say go" (`HWW:282`); `/sc:git`: "a commit needs authorization. Do not append push, merge or PR creation" (`HWW:324`). No new concept is invented.
2. **Every published action stays where a person can confirm it.** Push, PR, comment, install and VM happen at the coordinator, run "with the person" (`V3:20`). PRs go only through `/sc:pr-submit` (`CLAUDE.md:50`), which D3 (a) keeps at the coordinator (`SPEC:341`). Hard-to-reverse actions are exactly the class `PRL:351` says must be confirmed.
3. **It meets issue #326's commit request where V2 cannot.** The owner asks for commits "after each task" (`EVAL:19`); the evaluation's F0/F1 call for authorized local commits that "never push" (`EVAL:50-51`), and its F4 keeps GitHub progress posts at the coordinator only (`EVAL:54`). (c) matches F0, F1 and F4 together; V1 conflicts with F4 and V2 with F0/F1.
4. **The refined rule makes a commit as safe as the original claimed.** A dedicated worktree is already the spec's practice when attribution matters: 7.2 uses "one worker in a fresh disposable worktree ... so step 6 can attribute every change to the worker under test" (`SPEC:235`). Orca's guide allows a new worktree when "a concrete checkout or filesystem conflict makes sharing unsafe" (`CAPS:115`), and a commit is one: HEAD and the index are shared, and `git add .dev/tasks` covers the whole tree (`CLAUDE.md:37`). The evaluation's F2 already proposes `.dev/worktrees/<run>-<n>/` on its own branch (`EVAL:52`; `CLAUDE.md:299`). In its own worktree and branch, `git reset` on an unpushed commit touches no one else's work.
5. **Checkable boundaries.** The worker lists each commit SHA in the contract's `artifacts` (`V3:5`). AC-4.2 gains a check that `git log origin/<branch>` is unchanged (`V3:17`), plus "worker's commits only on its own branch and only in its own worktree".
6. **Day to day, the person gets one reviewable branch per worker**, then approves the push as `HWW:282` already describes. Loosening to (a) later is still additive (`V3:23`).

## Weaknesses identified
**Variant 1**
1. It admits that authority reaches the worker only as the coordinator's quotation, which the worker "cannot check" (`V1:14`), and that published actions are "visible at once" (`V1:15`). Then it lets those actions run anyway. `PRL:351` says "this session", and a worker is a different session; the spot-check rates `PRL:351` as OVERSTATED support for (a) (`diff-analysis.md:105`).
2. No commit scope, branch or timing rule (`V1:3`; S-005, C-012). Under the shared-worktree default (`SPEC:75`) V1 has every A-004 hazard, and because pushes are allowed, those mixed commits can reach `origin`.
3. It cites #326's GitHub status updates as a reason (`V1:10`), but the evaluation it cites gives those posts to the coordinator only (`EVAL:54`; X-004).
4. Highest cost: every outward flag must be honoured under `--unattended`, each with its own live check on a scratch fork PR (`V1:18`, `V1:24`).

**Variant 2**
1. It fails #326's per-task commit request and admits the ban rests on this planning run's own rule ("No git commits, pushes, PRs or GitHub comments", `.dev/orca-command-refactor/README.md:31`), not repo policy (`V2:20`; `EVAL:50`).
2. It treats a local commit like a publication ("no worker can publish, push, commit", `V2:13`), but the repo separates the two (`HWW:282`).
3. It overreads its sources. `CLAUDE.md:68` covers upstream contributions only (spot-check OVERSTATED, `diff-analysis.md:102`), and `PRS:43-49` does not stop a top-level worker from running pr-submit (X-007; `SPEC:71`).
4. Several workers' source edits end up uncommitted in one working tree, and the person must separate them by hand. The spec values per-worker attribution enough to build 7.2 around it (`SPEC:235`).

## Concessions
- **X-006 / A-005: my original was wrong.** `V3:23` says "no command needs a new outward flag", but a per-task commit inside `/sc:implement` needs a step that does not exist: acceptance "never ... authorizes commit, PR, merge or release" (`MW:67`); "A FINAL pass is not a commit" (`MW:63`); the step is #326's K3 (`EVAL:63`). Until K3 lands, a worker makes no commit inside implement. Its single permitted commit happens after the command has written a `succeeded` contract, before `check` and `worker_done`. Committing after a `blocked` or `partial` result is never allowed: a later resume would fail the ladder's "HEAD has not moved" check (`RETRY:41`, `RETRY:44`).
- **A-004 / A-009: "undoable" was false as written** under WC-11's shared worktree. That is why (c′) voids a commit authorization unless the worker is in its own worktree.
- **C-007:** V2 is more consistent with D2 (`QA:254`). My answer is narrower: a commit is not acceptance of work, and under (c′) it can be undone and is reviewed before push. But the provenance gap still exists for commits.
- **U-001 / A-006:** V1 alone delivers post-release's install run in the worker. Under (c) the coordinator re-runs it. auggie-review has no deferred posting path (`SPEC:123`), so posting means the coordinator re-runs the command with `--post-pr`.
- **Cost:** V2 is cheapest (`V2:23`). (c′) adds creating worktrees and removing them afterwards (`EVAL:52-53`, F2/F3), and changes AC-4.2's `git log -1` check (`SPEC:275`) so that it depends on whether commits were authorized.
- `/sc:task` commits its TFEP report (`TASK:266`). Under (c′) that commit stays off unless the brief authorizes it, as `SPEC:144` already says, and `push` is refused even though task treats it as EXEMPT (`TASK:61`).

## Shared assumption responses
| A-NNN | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | WC-9 (`SPEC:73`) is the baseline all three start from. |
| A-002 | ACCEPT | "commit only when asked" (`CLAUDE.md:37`); `HWW:212`. |
| A-003 | QUALIFY | The coordinator is "this session" only while it is the same live conversation in which the user spoke. A restarted coordinator must re-confirm before acting (`PRL:351`). (c) limits the damage either way: a misplaced authority can at most produce a local commit on an isolated branch. |
| A-004 | ACCEPT | The hazard is real under `SPEC:75`. Fixed in (c′) by requiring the worker's own worktree and branch (`CAPS:115`; `EVAL:52`). |
| A-005 | ACCEPT | No commit step exists in implement (`MW:63,67`; `EVAL:63`). (c′) commits only at the end of a Task, after the command finishes. task (`TASK:61`) and post-release (`PRL:340`) do have commit steps. |
| A-006 | QUALIFY | Pushing deferred commits costs nothing, because they stay on the branch. A real-target install is the step itself, so skipping it in the worker wastes no work. auggie-review posting does need a re-run (`SPEC:123`); this is a real cost. |
| A-007 | QUALIFY | Under (c′) a misquoted authorization can at most cause one local commit on an isolated branch, reviewed before any push; under (a) it can cause a publication. |
| A-008 | ACCEPT | `CLAUDE.md:50`. |
| A-009 | ACCEPT | Partly contradicted, as stated. (c′) restores the claim: in its own worktree and branch, a reset touches no other worker's commits and no other implement run's HEAD. |
| A-010 | ACCEPT | The owner's comment is design input, not authorization (`EVAL:74`). |

## Per-point positions
| ID | Superior | Reason |
|---|---|---|
| S-001 | V3 | Keeps the action split separate from the commit rule's operative constraints. |
| S-002 | equal | Citation keys are only formatting. |
| S-003 | equal | Only the headings differ. |
| S-004 | V1 | States its main weakness openly; V3 did not. |
| S-005 | V3 | The only variant with executable constraints (`V3:5`). |
| S-006 | equal | V2 and V3 both use every key they declare; this is minor. |
| S-007 | V3 | Marks the one unverified claim. |
| C-001 | V3 | Accepts the provenance gap only for an isolated local commit. |
| C-002 | V3 | Once refined to the worker's own worktree, a commit is genuinely undoable; a publication is not. |
| C-003 | V2 | As of today, no HEAD risk at all; (c′) is equal only by staying out of implement until K3. |
| C-004 | equal | V2 and V3 both keep the real-target install with the coordinator, as `PRL:351` requires; V1's extra value is conceded above. |
| C-005 | equal | V2 and V3 both forbid worker posting; both have the re-run cost in A-006. |
| C-006 | V3 | Task's commit can be authorized, push is refused, and the TFEP commit stays off (`SPEC:144`). |
| C-007 | V2 | Most consistent with D2's `QA:254`. |
| C-008 | V3 | Adds checks for `origin` unchanged and own-branch commits. |
| C-009 | V2 | Zero cost. |
| C-010 | V3 | Matches EVAL F0, F1 and F4 together. |
| C-011 | equal | PRs go through pr-submit at the coordinator in all three. |
| C-012 | V3 | Scope and branch rules, plus the own-worktree fix for the `.dev/tasks` hazard. |
| C-013 | V2 | Its asymmetric-cost point is the strongest. |
| C-014 | V3 | One reviewable branch per worker before the push. |
| C-015 | V3 | Adopted here: also remove the `README.md:31` citation from WC-9 (`SPEC:73`). |
| X-001 | V3 | Same as V2 on outward actions, without V1's provenance gap. |
| X-002 | V3 | Authorized commits in an isolated worktree meet #326 safely. |
| X-003 | V3 | Applies "this session" only where it holds. |
| X-004 | V3 | Same as V2; matches `EVAL:54`. |
| X-005 | V3 | The repo separates local commits from publication (`HWW:282`). |
| X-006 | V2 | My original claim was wrong; conceded and refined. |
| X-007 | equal | D3 (a) (`SPEC:341`) settles it for V2 and V3 alike. |
| A-003 | V3 | Smallest damage if the coordinator's authority is stale. |
| A-006 | V1 | Nothing needs deferring. |
| A-010 | equal | All three are compatible with `EVAL:74`. |
