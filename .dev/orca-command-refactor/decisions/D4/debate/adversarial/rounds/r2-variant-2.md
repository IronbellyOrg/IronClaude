# Round 2, Variant 2 advocate: D4 option (b), rebuttals

Citation key as in `diff-analysis.md:12` (`SPEC`, `PRL`, `HWW`, `EVAL`, `RETRY`, `MW`, `QA`), plus `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`; `AUG:N` = `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `R1-V1:N`, `R1-V3:N`, `R2-V1:N` = lines of the Round 1 and Round 2 statements in this folder. Every source line cited was re-read on branch `ironbelly/OrcaCLICommandRefactor-Specs` on 2026-11-02.

## Responses to criticisms

| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | V2 generalized `CLAUDE.md:68` into "the repo's outward rules are session-scoped". | R1-V1:25, R1-V3:33 | Withdrawn in Round 1 (r1-variant-2.md:5). The session rule that governs these actions is `PRL:351`, which V1 now treats as the specific guardrail (R2-V1:8). | Concede the citation; hold the conclusion on `PRL:351` |
| 2 | V2 read `PRS:47-49` as "only the coordinator or person ever runs" pr-submit. | R1-V1:26, R1-V3:33 | `PRS:47-49` bars an Agent-tool subagent, not a top-level worker (`SPEC:71`). Withdrawn in Round 1 (r1-variant-2.md:42). D3 (a) is recommended (`SPEC:341-343`), so the point is moot. | Concede |
| 3 | "Zero beyond today's spec" is false, because six spec rows say "unless the brief authorizes". | R1-V1:16, R1-V1:27, R2-V1:11 | Correct. Under (b), WC-9 (`SPEC:73`), the 2.3 brief item (`SPEC:79`), auggie-review (`SPEC:123`), post-release (`SPEC:136`), task (`SPEC:144`) and D3 (b) (`SPEC:342`) all need "never" wording. These are clause rewrites, not new mechanisms, so (b) is still the cheapest option, but its cost is not zero. | Concede the claim; hold the ranking |
| 4 | Deferring work to the coordinator forces re-runs (auggie-review, post-release). | R1-V1:18, R1-V1:27 | Mostly answered. The summary posts from `REVIEW.md` with the skill's own command (`AUG:319`; V1's own finding, R2-V1:25). Only the inline Critical/High comments (`AUG:320-327`) need manual posting. The real-target install is the step itself, so skipping it in the worker wastes no work (R1-V3:52); its transcript (`PRL:333`) comes from the coordinator's run. | Hold; small residual cost conceded |
| 5 | The commit ban rests on the run-local `README.md:31`. | R1-V1:28, R1-V3:31 | Round 1 moved the ban's basis to mechanics (r1-variant-2.md:20). With a shared worktree (`SPEC:75`), one worker's commit moves HEAD inside another worker's implement window (`RETRY:41`; `q0-head`, `sc-implement-protocol/SKILL.md:114`), and `git add .dev/tasks` stages other workers' ledgers (`CLAUDE.md:37`). Those mechanics disappear when the worker has its own worktree, which (c′) now requires (R1-V3:6). | Concede when the worker has its own worktree; hold when it shares one |
| 6 | V2 groups a local commit with publishing. | R1-V1:28, R1-V3:32 | The repo keeps them separate: "Commit locally ... push only when they say go" (`HWW:282`); "a commit needs authorization. Do not append push, merge or PR creation" (`HWW:324`). V2:13 is wrong as a classification. It was only a safety grouping for the shared-worktree case. | Concede |
| 7 | (b) fails #326's per-task commit request. | R1-V3:31, R2-V1:19 | True (`EVAL:19`). The owner's comment is design input, not authorization (`EVAL:74`), so it does not decide D4 by itself. Still, a rule that can meet the request safely should. | Concede |
| 8 | Several workers' uncommitted edits mix in one working tree, which makes attribution hard. | R1-V3:34 | The worktree gives attribution, not the commit. The 7.2 check attributes changes with `git status --porcelain` in a disposable worktree and makes no commit (`SPEC:235`, `SPEC:245`), and every contract lists `artifacts`, "every other file written" (`SPEC:68`). A commit adds history, not attribution. | Hold |
| 9 | (b) rules out D3 (b) parallel PR monitoring. | R1-V1:21 | D3 recommends (a) (`SPEC:341-343`), and V1 now treats the point as moot (R2-V1:72). Allowing it later only adds permission and is cheap. | Hold |
| 10 | `PRL:340`'s "standing authorization" has no session limit, so a brief qualifies. | R1-V1:17 | `PRL:351` sits in the same file's Guardrails, names exactly these actions and says "this session". V1 conceded (R2-V1:8). | Hold |
| 11 | (b) only moves the provenance gap to a stale coordinator. | R1-V1:53 | A stale coordinator can still ask the person before acting (`PRL:351`); a worker cannot (WC-2, `SPEC:66`). V1 conceded (R2-V1:14). | Hold |
| 12 | V2 would itself accept (c) with an own worktree and K3, so its ban fits only the default placement. | R2-V1:19 | Correct. K3 is not even needed for (c′)'s single end-of-Task commit. The worker session commits with plain git after the command has finished ("Native tools may be enough", `HWW:324`), so no command commit step has to be switched on, and A-005 does not arise. | Concede; I move to (c′) |

## Updated assessment of other variants

**Variant 1 (a).** Steelman: V1 argued honestly and has itself moved to (c′) (R2-V1:79). What remains distinct to (a) is one-run delivery of post-release's real-target install (`PRL:333`) and D3 (b) parallel PR monitoring (`SPEC:342`). Critique: both are conveniences, and both stay available later as a purely additive change, as V1 itself says (R2-V1:79). Nothing that leaves the machine should run on authority a worker cannot verify and no person can confirm at the moment of action (`PRL:351`; `SPEC:66`; `HWW:307`, "Disclose conflicts ... rather than silently increasing authority"). (a) is no longer contested.

**Variant 3 (c′).** Steelman: (c′) applies the repo's own human rule to workers (`HWW:212`, `HWW:282`, `HWW:324`). It requires the worker's own worktree and branch, which removes every shared-worktree hazard I raised (A-004, A-009). It commits once, after a `succeeded` contract, and never inside implement until K3 (R1-V3:6, R1-V3:37). Nothing leaves the machine. It meets #326 F0, F1 and F4 (`EVAL:50-54`). The provenance gap is limited to one local commit that can be undone. Remaining conditions, none of them a reason to reject it:
- (i) Own-worktree placement rests on an UNVERIFIED step: whether `worker-start` accepts a worktree that Orca did not create (`SPEC:236`).
- (ii) Each committing worker leaves a branch with unmerged commits, which F3 forbids the coordinator to remove without the user's instruction (`EVAL:53`). The person must decide, branch by branch, whether to merge or discard.
- (iii) AC-4.2's "`git log -1` unchanged" (`SPEC:275`) must depend on whether the brief authorized a commit.
- (iv) The worktree needs the same setup the 7.2 check needs (`EVAL:52`).

When either condition is missing (no quoted authorization, or no worktree of its own), (b)'s rule applies unchanged: no commit.

## New evidence

1. **The end-of-Task commit needs no command feature.** `/sc:git`'s routing row says "a commit needs authorization ... Native tools may be enough" (`HWW:324`). The worker session can run `git commit` itself after the command exits, so neither implement's missing commit step (`MW:63`, `MW:67`) nor K3 (`EVAL:63`) blocks (c′). This weakens my Round 1 X-006 point for (c′), though not for V3's original window inside implement.
2. **Attribution does not need commits.** 7.2 attributes changes by `git status --porcelain` in a disposable worktree (`SPEC:235`, `SPEC:245`), and the contract lists every file written (`SPEC:68`).
3. **The (c′) precondition is unverified.** "whether Orca accepts a worktree it did not create is UNVERIFIED" (`SPEC:236`). Orca's guide creates a worktree only when "a concrete checkout or filesystem conflict makes sharing unsafe" (`CAPS:115`); a committing worker is one. No orchestration verb removes a worktree; removal is `orca worktree rm` (`CAPS:115`).
4. **Cleanup cost.** F3 keeps branches with unmerged commits until the user decides (`EVAL:53`), so (c′) adds one decision per committing worker. (b) adds none.
5. **Residual posting cost.** `AUG:319` lets the coordinator post the summary from `REVIEW.md`; the inline comments (`AUG:320-327`) have no deferred path.

## Updated shared assumption responses

| A-NNN | Round 1 | Round 2 | Reason |
|---|---|---|---|
| A-006 | QUALIFY | QUALIFY, narrowed | Deferral costs less than I conceded: the auggie-review summary posts from `REVIEW.md` (`AUG:319`), and the real-target install is the step itself. Only the inline comments (`AUG:320-327`) lack a deferred path. |
| A-007 | REJECT | QUALIFY | Faithful quoting cannot be checked by the worker (`QA:254` logic), but the brief is fixed at creation (`SPEC:70`) and can be audited afterwards. That is enough only for one undoable local commit in the worker's own worktree, never for an action that leaves the machine. |

## Final per-point positions

"V2 = V3" means V2 and V3 tie and both beat V1. V3 means (c′) as refined in R1-V3:6.

| ID | Superior approach | Changed since R1? | Reason |
|---|---|---|---|
| S-001 | V3 | No | A separate, operative commit paragraph is clearer. |
| S-002 | equal | Yes (was V3) | Citation-key style is cosmetic; aligns with R1-V3 and R2-V1. |
| S-003 | equal | No | Only the headings differ. |
| S-004 | V1 | No | Only V1 stated its central weakness where it bites (`V1:14-15`). |
| S-005 | V3 | No | Only executable commit constraints (`V3:5`). |
| S-006 | equal | Yes (was V2 = V3) | Cosmetic. |
| S-007 | V3 | No | Marks its one unverified claim. |
| C-001 | V3 | Yes (was V2) | Accepts relayed authority only for one undoable commit in the worker's own worktree; (b)'s rule stays the default. |
| C-002 | V3 | Yes (was V2) | With its own worktree, a reset touches no other worker (A-009 resolved); a publication cannot be undone. |
| C-003 | V2 | No | Zero HEAD risk unconditionally; (c′) matches only under its own conditions. |
| C-004 | V2 = V3 | No | Real-target install and VM are on `PRL:351`'s confirm-first list. |
| C-005 | V2 = V3 | No | The coordinator posts the summary from `REVIEW.md` (`AUG:319`). |
| C-006 | V3 | Yes (was V2) | task's commit can be authorized in the worker's own worktree, push is refused, and the TFEP commit stays off (`SPEC:144`; `sc-task-protocol/SKILL.md:61,266`). |
| C-007 | V2 | No | Most consistent with D2 (`QA:254`); V1 and V3 concede this. |
| C-008 | V3 | Yes (was V2) | `git log origin/<branch>` unchanged plus an own-branch check is the better test under any option. |
| C-009 | V2 | No | Cheapest: clause rewrites only, though not zero (response 3). |
| C-010 | V3 | No | Per-task commits with coordinator posting (`EVAL:19`, `EVAL:54`). |
| C-011 | V2 = V3 | No | PRs only via pr-submit at the coordinator (`CLAUDE.md:50`). |
| C-012 | V3 | No | Scope, branch, no-push, own worktree. |
| C-013 | V2 | No | Allowing more later is additive; tightening after a publication is not. |
| C-014 | V3 | No | One reviewable branch per worker before an approved push (`HWW:282`). |
| C-015 | V3 | Yes (was equal) | V3 alone removes `README.md:31` from both `SPEC:73` and `SPEC:156`. |
| X-001 | V2 = V3 | No | Nothing that leaves the machine runs on relayed authority. |
| X-002 | V3 | Yes (was V2) | Authorized local commits are safe once the worker has its own worktree; (b) applies when it does not. |
| X-003 | V2 = V3 | No | Both apply "this session" only where it can hold. |
| X-004 | V2 = V3 | No | `EVAL:54`. |
| X-005 | V3 | Yes (was V2) | The repo separates local commit from publication (`HWW:282`, `HWW:324`). |
| X-006 | V2 | No | No new mechanism; V3's original window inside implement needed K3 (conceded in R1-V3:37). |
| X-007 | equal | Yes (was V3) | Moot under D3 (a) (`SPEC:341-343`). |
| A-003 | V2 = V3 | Yes (was V2) | Both keep outward steps at the coordinator, which can ask the person (`PRL:351`). |
| A-006 | V1 | No | Only (a) avoids deferral, but the residual cost is small (new evidence 5). |
| A-010 | equal | Yes (was V2 = V3) | After V1 withdrew that use, all three treat #326 as design input (`EVAL:74`). |

## Overall recommendation

I now recommend Variant 3 as refined, option (c′), with my option (b) as its default and fallback. The spec's D4 recommendation (`SPEC:348`) should change from (a) to (c), and its `PRL:351` citation should be read as support for keeping outward steps at the coordinator.

**Worker commits.** None unless both conditions hold:
1. The brief quotes the user's instruction naming a commit for that Task.
2. The coordinator has placed the worker in its own worktree and branch under `.dev/worktrees/` (`CLAUDE.md:299`; `CAPS:115`).

When both hold, the worker session makes one commit with plain git (`HWW:324`), after the command has written a `succeeded` contract. It never commits after `partial` or `blocked`, and never inside `/sc:implement` until K3 (`MW:63,67`; `EVAL:63`). It stages the Task's files plus that worktree's `.dev/tasks` (`CLAUDE.md:37`), never commits on the default branch, never pushes, and lists each SHA in `artifacts`. If either condition is missing, the worker makes no commit.

**Everything that leaves the machine** stays with the coordinator: push, PR, GitHub comment or progress post, real-target install, VM and paid run. It confirms with the person at the moment of action unless the instruction is in its own live conversation (`PRL:351`). PRs go only through `/sc:pr-submit` (`CLAUDE.md:50`), and auggie-review summaries are posted from the worker's `REVIEW.md` (`AUG:319`).

**Spec edits:**
- Apply EVAL F0, F1 (reworded to one commit at the end of the Task until K3), F3 and F4 (`EVAL:50-54`).
- Remove `README.md:31` from WC-9 and the `/sc:git` row.
- AC-4.2 adds "`git log origin/<branch>` unchanged" and makes "`git log -1` unchanged" depend on whether a commit was authorized.
- Add a check that proves own-worktree placement (`SPEC:236`, UNVERIFIED) before any commit authorization is used.
