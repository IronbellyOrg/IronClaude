# Round 2, Variant 3 advocate: D4 option (c), rebuttals

Citation key as in `diff-analysis.md:12` (`SPEC`, `PRL`, `HWW`, `EVAL`, `RETRY`, `MW`, `QA`), plus `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `AUG:N` = `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:N`; `TASK:N` = `src/superclaude/skills/sc-task-protocol/SKILL.md:N`; `R1-Vn:N`, `R2-Vn:N` = lines of the Round 1 and Round 2 statements in this folder; `DA:N` = `diff-analysis.md:N`. Every source line cited was re-read on branch `ironbelly/OrcaCLICommandRefactor-Specs` on 2026-11-02. "V3" below means option (c′) as refined in R1-V3:6.

## Responses to criticisms

| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | "No command needs a new outward flag" (`V3:23`) is contradicted by V3's own commit window inside `/sc:implement`, which has no commit step (X-006, A-005). | R1-V1:31, R1-V2:36, `DA:56` | Conceded in R1-V3:37. The fix is now simpler than my Round 1 wording: the worker session commits with plain git after the command has exited ("Native tools may be enough", `HWW:324`; R2-V2:36), so no command's own commit step is switched on and nothing commits inside implement ("A FINAL pass is not a commit", `MW:63`; acceptance never "authorizes commit", `MW:67`). K3 stays #326 work (`EVAL:63`). | Concede the original; hold (c′) |
| 2 | "Its own feature branch" is not the spec default. Workers share the worktree (`SPEC:75`), so they share HEAD; another worker's commit trips `RETRY:41`, and a `git reset` can drop another worker's commits (A-004, A-009). | R1-V1:32, R1-V2:35 | Correct for the original. (c′) makes a commit authorization void unless the worker has its own worktree and branch. The repo already requires this for parallel sessions: "When running multiple Claude Code sessions in parallel, use `git worktree` to avoid conflicts" (`CLAUDE.md:297`), located under `.dev/worktrees/` (`CLAUDE.md:299`); Orca allows it when "a concrete checkout or filesystem conflict makes sharing unsafe" (`CAPS:115`). | Concede the original; hold (c′) |
| 3 | The evaluation's F2 proposes a worktree per worker only for experiments, so (c′) goes beyond it. | R1-V2:35 | True of F2's wording (`EVAL:52`), but a committing worker is the same `CAPS:115` conflict (shared HEAD and index), and `CLAUDE.md:297` is not limited to experiments. F2 needs one more clause: "and any worker whose brief authorizes a commit". | Hold; spec edit needed |
| 4 | The commit window is correct for one sequential implement run only. | R1-V2:36, `DA:33` | Answered by 1 and 2: one commit after the command ends, in a worktree no one else writes. Never after `blocked` or `partial`, because a resume would then halt `head-moved` (`RETRY:44`). Note `partial` maps to outcome `succeeded` (`SPEC:69`), so the rule keys on `worker_status: succeeded`, not on the outcome. | Concede the original; hold (c′) |
| 5 | `git add .dev/tasks` is repo-wide, so the scope rule stages other workers' ledgers. | R1-V2:37, `DA:42` | In its own worktree, `.dev/tasks` holds only that worker's ledgers, so `CLAUDE.md:37` is obeyed without leaking. | Concede the original; hold (c′) |
| 6 | V3 accepts the provenance gap for commits, so its objection to (a) is blast radius, which argues for narrowing (a). | R1-V1:33 | V1 has since narrowed (a) to exactly (c′) (R2-V1:79). Blast radius is the right test: `PRL:351` puts hard-to-reverse actions behind same-session confirmation, and only the commit in an isolated worktree is easy to reverse. | Hold |
| 7 | V3 does not address D2 consistency; the commit still rests on the coordinator's quotation, which `QA:254` would not accept for a Ruling (C-007). | R1-V2:38, `DA:37` | V2 is more consistent. My mitigation: the brief is fixed at creation (`SPEC:70`) and auditable, the commit is undoable in its own worktree, and the person reviews it before any push (`HWW:282`). That limits the gap; it does not close it. | Concede C-007 to V2 |
| 8 | `PRL:351`'s "this session" holds for the coordinator only while the user's instruction is in its live conversation (A-003). | R1-V1:34 | Agreed. When the instruction is stale, the coordinator asks the person before any outward step. It can ask; a worker cannot (WC-2, `SPEC:66`). | Concede the qualifier; hold the conclusion |
| 9 | (c) carries the same re-run cost as (b) for deferred outward steps (A-006). | R1-V1:35 | Smaller than claimed, including in my own R1-V3:40. The auggie-review summary posts from the saved file with the skill's own command (`AUG:319`; failure path `AUG:384`). Only the inline Critical/High comments (`AUG:320-327`) need manual posting. The real-target install is the step itself; when the coordinator runs it, the transcript (`PRL:333`) comes from that run. | Concede the small residual |
| 10 | Under (c′) the commit is per Orca Task, not per implement task, until K3. | R2-V1:21 | True. #326's "after each task" (`EVAL:19`) is met only at Orca Task granularity. Finer commits are K3, after spec P4 (`EVAL:89`). | Concede |
| 11 | AC-4.2's "`git log -1` unchanged" (`SPEC:275`) must become conditional. | R2-V1:21, R2-V2:29 | Agreed. Wording: unchanged when no commit was authorized. When one was, every new commit is on the worker's branch in its own worktree, each SHA is in `artifacts`, and `git log origin/<branch>` is unchanged. | Concede |
| 12 | Each committing worker leaves a branch with unmerged commits; F3 forbids removing it without the user (`EVAL:53`), so there is one decision per worker. | R2-V1:21, R2-V2:28, R2-V2:39 | The cost is real. But it is the review `HWW:282` already prescribes ("show your lead what changed, and push only when they say go"), not a new kind of work. | Concede the cost; hold that it is the intended review |
| 13 | Own-worktree placement rests on an UNVERIFIED step: whether `worker-start` accepts a worktree Orca did not create (`SPEC:236`). | R2-V2:27, R2-V2:38 | Concede. A P0 check must prove it. Until it does, no commit authorization can be valid, so (b) applies in practice. | Concede |
| 14 | The worktree needs the same setup as the 7.2 check. | R2-V2:30 | Concede. One F2 sentence covers both (`EVAL:52`). | Concede |
| 15 | Attribution comes from the worktree and `git status`, not from commits; this rebuts R1-V3:34. | R2-V2:16 | Correct (`SPEC:235`, `SPEC:245`, `SPEC:68`). I withdraw R1-V3:34. A commit's value is a reviewable history and an undo point, which is #326's request. | Concede |
| 16 | V3 stated no weakness of its own. | `DA:22` (S-004) | Corrected in R1-V3:36-42 and above. | Concede |

## Updated assessment of other variants

**Variant 1 (a).** Steelman: V1 argued against its own interest and now recommends (c′) (R2-V1:79). It also produced the evidence that most reduces the cost of (b) and (c): the deferred auggie-review summary path (`AUG:319`, R2-V1:25). What remains unique to (a) is one-run delivery of post-release's real-target install (`PRL:333`) and D3 (b) parallel PR monitoring (`SPEC:342`). Critique: both are conveniences. Both stay available later as an additive loosening, which V1 itself accepts. One residual difference: R2-V1's C-006 still lets a brief switch on task's own `commit` step. New evidence 2 below argues against that.

**Variant 2 (b).** Steelman: V2's shared-worktree mechanics (R1-V2:20) were the strongest argument in this debate. They forced (c′)'s own-worktree condition. Its framing that "(b) is the default and fallback of (c′)" (R2-V2:90) is the correct way to write the rule: no commit unless both conditions hold. It also found that the end-of-Task commit needs no command feature (`HWW:324`, R2-V2:36). Critique: none of substance remains. V2 keeps C-003, C-007, C-009, C-013 and X-006. I agree on all five, because each describes a property (b) has unconditionally and (c′) has only under its preconditions.

All three advocates now recommend the same rule. The remaining differences are notation and the C-006 detail.

## New evidence

1. **The repo already requires a separate worktree for parallel sessions.** "**CRITICAL**: When running multiple Claude Code sessions in parallel, use `git worktree` to avoid conflicts" (`CLAUDE.md:297`), under `.dev/worktrees/` (`CLAUDE.md:299`). WC-11's shared default (`SPEC:75`) is safe only because workers write disjoint report directories. Once a worker commits, it shares HEAD and the index, and `CLAUDE.md:297` applies. The own-worktree condition therefore follows existing repo policy; it does not add a new rule.
2. **post-release treats "committing" as a confirm-first action "this session".** Its guardrail lists "provisioning a VM, running install scripts against a real target, committing, and opening a PR" as "outward-facing / hard-to-reverse" (`PRL:351`), and `PRL:340` groups the commit with push and PR. A brief cannot satisfy "this session" inside the skill. So I revise (c′): **a command's own commit steps stay off under `--unattended`, always.** That covers post-release's commit (`SPEC:136`), task's EXEMPT `commit` (`TASK:61`; `SPEC:144`) and the TFEP report commit (`TASK:266`). The only worker commit is the session's single end-of-Task plain-git commit (`HWW:212`, `HWW:324`). This gives one mechanism and one test, and no skill guardrail is ever satisfied through a quotation. It changes my C-006 reason and simplifies the `SPEC:136` and `SPEC:144` rows to "commit off".
3. **The commit rule keys on `worker_status`, not on the outcome.** `partial` maps to `--outcome succeeded` (WC-5, `SPEC:69`). A commit after `partial` would trip `head-moved` on a later resume (`RETRY:44`). The trigger must therefore be `worker_status: succeeded`.

## Updated shared assumption responses

| A-NNN | Round 1 | Round 2 | Reason |
|---|---|---|---|
| A-005 | ACCEPT | ACCEPT, no longer binding on (c′) | Implement has no commit step (`MW:63,67`). Under the revised (c′), no command's commit step is used at all (new evidence 2), so the assumption cannot fail for (c′). |
| A-006 | QUALIFY ("auggie-review posting does need a re-run") | QUALIFY, narrowed | No re-run is needed: the summary posts from `REVIEW.md` with the skill's own command (`AUG:319`). Only the inline comments (`AUG:320-327`) need manual posting. The real-target install is the step itself (`PRL:333`). |

## Final per-point positions

"V2 = V3" means V2 and V3 tie and both beat V1.

| ID | Superior approach | Changed since R1? | Reason |
|---|---|---|---|
| S-001 | V3 | No | Separate operative commit paragraph. |
| S-002 | equal | No | Citation-key style is cosmetic. |
| S-003 | equal | No | Only the headings differ. |
| S-004 | V1 | No | Only V1 stated its central weakness where it bites (`V1:14-15`). |
| S-005 | V3 | No | Only executable commit constraints (`V3:5`). |
| S-006 | equal | No | Cosmetic. |
| S-007 | V3 | No | Marks its one unverified claim. |
| C-001 | V3 | No | Relayed authority only for one undoable commit in the worker's own worktree. |
| C-002 | V3 | No | In its own worktree an unpushed commit is undoable; a publication is not. |
| C-003 | V2 | No | Zero HEAD risk unconditionally; (c′) matches only under its preconditions, one still UNVERIFIED (`SPEC:236`). |
| C-004 | V2 = V3 | No (notation) | Real-target install and VM are on `PRL:351`'s confirm-first list. |
| C-005 | V2 = V3 | No (notation) | The coordinator posts the summary from `REVIEW.md` (`AUG:319`). |
| C-006 | V3 | Reason changed | Commands' own commit steps stay off under `--unattended` (`PRL:351`; `TASK:61,266`); only the end-of-Task session commit is authorizable; push refused. |
| C-007 | V2 | No | One provenance rule across D2 and D4 (`QA:254`). |
| C-008 | V3 | No | Conditional AC-4.2 plus `git log origin/<branch>` unchanged and own-worktree checks. |
| C-009 | V2 | No | Cheapest: clause rewrites only. |
| C-010 | V3 | No | Commits per Orca Task (`EVAL:19`) with posting at the coordinator (`EVAL:54`); finer granularity is K3. |
| C-011 | equal | No | All three now route PRs through pr-submit at the coordinator (`CLAUDE.md:50`). |
| C-012 | V3 | No | Scope, branch, no push, own worktree. |
| C-013 | V2 | No | Allowing more later is additive; recalling a publication is impossible. |
| C-014 | V3 | No | One reviewable branch per worker before an approved push (`HWW:282`). |
| C-015 | V3 | No | Removes `README.md:31` from both `SPEC:73` and `SPEC:156`. |
| X-001 | V2 = V3 | Yes (was V3) | (b) and (c) are identical on everything that leaves the machine. |
| X-002 | V3 | No | Authorized local commits only in the worker's own worktree; (b) otherwise. |
| X-003 | V2 = V3 | Yes (was V3) | After V2 withdrew `CLAUDE.md:68`, both apply `PRL:351` at the coordinator only. |
| X-004 | V2 = V3 | Yes (was V3) | `EVAL:54` supports both. |
| X-005 | V3 | No | The repo separates a local commit from publication (`HWW:282`, `HWW:324`). |
| X-006 | V2 | No | V3's original window needed a step implement lacks; conceded. |
| X-007 | equal | No | Moot under D3 (a) (`SPEC:341-343`). |
| A-003 | V2 = V3 | Yes (was V3) | Both keep outward steps at a coordinator that can ask the person; (b)'s stale-authority damage is not larger than (c′)'s. |
| A-006 | V1 | No | Only (a) avoids deferral; the residual cost is small (`AUG:319`). |
| A-010 | equal | No | All three treat #326 as design input (`EVAL:74`). |

## Overall recommendation

Adopt option (c′), with (b) as its default and fallback. Change the spec's D4 recommendation (`SPEC:348`) from (a) to (c), and cite `PRL:351` as the reason outward steps stay at the coordinator.

**Worker commits:** none unless all three conditions hold:
1. The brief quotes the user's instruction naming a commit for that Task.
2. The coordinator has placed the worker in its own worktree and branch under `.dev/worktrees/` (`CLAUDE.md:297-299`; `CAPS:115`).
3. A P0 check has proven that `worker-start` accepts that worktree (`SPEC:236`).

When all three hold, the worker session makes one plain-git commit (`HWW:324`) after the contract reads `worker_status: succeeded`. It never commits after `partial` or `blocked`, and never inside a command. It stages the Task's files plus that worktree's `.dev/tasks` (`CLAUDE.md:37`), never commits on the default branch, never pushes, and lists each SHA in `artifacts`. Every command's own commit step stays off under `--unattended`: post-release, task's EXEMPT `commit`, and the TFEP commit (`PRL:351`; `TASK:61,266`). Per-implement-task commits wait for K3 (`EVAL:63`).

**Everything that leaves the machine** stays with the coordinator: push, merge, PR, GitHub comment or progress post, real-target install, VM and paid run. The coordinator confirms with the person at action time unless the instruction is in its own live conversation (`PRL:351`). PRs go only through `/sc:pr-submit` (`CLAUDE.md:50`), and auggie-review summaries are posted from the worker's `REVIEW.md` (`AUG:319`).

**Spec edits:**
- Apply EVAL F0, F1 (reworded to the end-of-Task commit), F2 (adding "any worker whose brief authorizes a commit"), F3 and F4 (`EVAL:50-54`).
- Remove `README.md:31` from WC-9 and the `/sc:git` row.
- AC-4.2 becomes conditional and gains "`git log origin/<branch>` unchanged".

Option (a) remains a later, additive loosening, if a concrete need appears.
