# Round 2, Variant 1 advocate: D4 option (a), rebuttals

Citation key as in `diff-analysis.md:12` (`SPEC`, `PRL`, `HWW`, `EVAL`, `RETRY`, `MW`, `QA`), plus `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `AUG:N` = `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:N`; `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`; `R1-V2:N`, `R1-V3:N` = Round 1 statement lines. Every source line cited was re-read on branch `ironbelly/OrcaCLICommandRefactor-Specs` on 2026-11-02.

## Responses to criticisms

1. **(a) grants authority the worker cannot verify, through the channel `QA:254` rejects.** Source: R1-V2:28, R1-V3:25. Response: a brief is fixed at `task-create` (`SPEC:70`), not a mid-run message, and `QA:254` governs accepting an unmet criterion, so the cases differ in form. But a worker can never ask the person (WC-2, `SPEC:66`), so an unrecallable action gets no check before its effect. **Concede** for everything that leaves the machine; **hold** only the difference in form.
2. **`PRL:351` "this session" cuts against (a).** Source: R1-V2:29, R1-V3:25. Response: conceded in Round 1. My fallback, `PRL:340`'s "standing authorization", is in the same file as `PRL:351`, the narrower guardrail that names exactly these actions (VM, real-target install, commit, PR); the specific rule governs. **Concede.**
3. **No commit scope, branch or timing; with push allowed, mixed shared-worktree commits can reach `origin`.** Source: R1-V2:30, R1-V3:26. Response: correct. I adopt V3's (c′) condition: no commit authorization without the worker's own worktree and branch (R1-V3:6, R1-V3:19). **Concede.**
4. **No commit step exists in `/sc:implement`.** Source: R1-V2:30. Response: `MW:63`, `MW:67`; the step is #326 K3 (`EVAL:63`). Adopt V3's one commit after a `succeeded` contract (R1-V3:37). **Concede.**
5. **Highest test and maintenance cost.** Source: R1-V2:31, R1-V3:28. Response: one live check per authorized action (`V1:18`) is real. **Hold** only that (b) is not zero: `SPEC:123`, `SPEC:136`, `SPEC:144` say "unless the brief authorizes" and need rewriting under (b). **Concede** the ranking.
6. **#326 does not support worker posting.** Source: R1-V2:32, R1-V3:27. Response: withdrawn in Round 1 (`EVAL:54`, `EVAL:74`). **Concede.**
7. **Faithful quoting cannot be the safety basis; a misquote causes a publication.** Source: R1-V2:58, R1-V3:53. Response: the fixed brief makes a misquote auditable, but only after a publication or real-target install has happened. **Concede** for outward actions; **hold** for an isolated local commit, where V3 accepts the same basis.
8. **The coordinator can confirm at action time; a worker cannot.** Source: R1-V2:22, R1-V2:54. Response: my claim that (b)/(c) only "move the gap" was too strong: a stale coordinator can still ask the person (`PRL:351`); a worker cannot (`SPEC:66`). **Concede.**
9. **Published actions cannot be recalled; tightening later is harder.** Source: R1-V2:23. Response: `V1:15` admitted it; (a) stays available as an additive loosening. **Concede.**

## Updated assessment of other variants

**Variant 2 (b).** Steelman: V2 moved its commit ban from the run-local `README.md:31` to mechanics. Under WC-11's shared worktree (`SPEC:75`), one worker's commit moves HEAD inside another's implement window (`RETRY:41`), and `git add .dev/tasks` sweeps up other workers' ledgers (`CLAUDE.md:37`) (R1-V2:20). This is correct and is the best argument against unconditional worker commits. Critique: V2 itself would accept (c) once each committing worker has its own worktree and K3 exists (R1-V2:43). Its ban therefore fits the default placement only, and it still fails #326's commit request (`EVAL:19`).

**Variant 3 (c′).** Steelman: (c′) closes all three holes in its original. A commit requires the worker's own worktree (A-004, A-009). Nothing commits inside implement until K3 (X-006). A commit happens only after a `succeeded` contract (R1-V3:6, R1-V3:37; `RETRY:41`). It matches EVAL F0, F1, F2 and F4 (R1-V3:18). Small remaining gaps: the commit is per Orca Task, not per implement task, until K3; AC-4.2's "`git log -1` unchanged" (`SPEC:275`) must become conditional; and the coordinator owes worktree removal (F3, `EVAL:53`; `CAPS:115`).

## New evidence

1. **auggie-review posting can be deferred without a re-run (weakens my A-006).** The summary is posted with `gh pr review <PR> --comment --body-file <output-dir>/REVIEW.md` (`AUG:319`), and the skill's own failure path saves `REVIEW.md` and surfaces it to the user (`AUG:384`). The coordinator can run the same command on a worker's report; only the inline Critical/High comments (`AUG:320-325`) need manual re-posting. My Round 1 "Deferral means re-running the work" (r1-variant-1.md:56) was overstated.
2. **Orca's placement rule supports the own-worktree condition:** create a worktree when "a concrete checkout or filesystem conflict makes sharing unsafe" (`CAPS:115`); a committing worker sharing HEAD and the index is one.
3. **The routing guide forbids silently raising authority:** "Disclose conflicts with stronger project policy rather than silently increasing authority" (`HWW:307`). A worker publishing on a brief cannot disclose anything to a person at the moment it acts.
4. **Side finding:** WC-7 cites pr-submit's top-level rule as `SKILL.md:37-39` (`SPEC:71`); on this branch it is `PRS:47-49`. That citation is WRONG, like `qa.md:232,238` (`diff-analysis.md:107`).

## Updated shared assumption responses

| A-NNN | Round 1 | Round 2 | Reason |
|---|---|---|---|
| A-003 | QUALIFY ("(b) and (c) move the gap") | QUALIFY, gap not merely moved | The coordinator is "this session" only while the user's instruction is in its live conversation; when stale, it can still ask the person before acting (`PRL:351`), which a worker never can (`SPEC:66`). |
| A-006 | REJECT | QUALIFY | False for post-release's real-target install, which only the worker run or a later coordinator run produces (`PRL:333`). Mostly true for auggie-review: the summary posts from `REVIEW.md` with the skill's own command (`AUG:319`, `AUG:384`); only inline comments need re-posting. |
| A-007 | QUALIFY | QUALIFY, narrowed | A fixed brief (`SPEC:70`) makes quoting auditable afterwards; that is an adequate basis only for an undoable local commit on an isolated branch, never for an action that leaves the machine. |

## Final per-point positions

"V2 = V3" means V2 and V3 tie and both beat V1.

| ID | Superior approach | Changed since R1? | Reason |
|---|---|---|---|
| S-001 | V3 | No | Separate operative commit paragraph is clearer. |
| S-002 | equal | No | Citation-key style is cosmetic. |
| S-003 | equal | No | Heading names are cosmetic. |
| S-004 | V1 | No | Only V1 stated its central weakness where it bites (`V1:14-15`). |
| S-005 | V3 | No | Only V3 gives executable commit constraints (`V3:5`). |
| S-006 | equal | Yes | Cosmetic; aligning with R1-V3. |
| S-007 | V3 | No | Only V3 marks an unverified claim. |
| C-001 | V3 | Yes (was V1) | Accepts the provenance gap only for an undoable commit on an isolated branch; concession 1. |
| C-002 | V3 | No | Reversibility is the right line once the worktree is the worker's own. |
| C-003 | V2 | Yes (was V3) | Zero HEAD risk unconditionally; (c′) matches only under its own-worktree and end-of-Task conditions. |
| C-004 | V2 = V3 | Yes (was V1) | Real-target install and VM are on `PRL:351`'s confirm-first list; the one-run delivery is convenience only. |
| C-005 | V2 = V3 | Yes (was V1) | The coordinator can post the summary from `REVIEW.md` (`AUG:319`); worker posting is not needed. |
| C-006 | V3 | Yes (was V1) | task's commit authorizable, push refused, TFEP commit off (`SPEC:144`). |
| C-007 | V2 | Yes (was V1) | One provenance rule across D2 and D4 (`QA:254`); my form distinction does not outweigh it. |
| C-008 | V3 | No | AC-4.2 plus `git log origin/<branch>` unchanged and own-branch checks. |
| C-009 | V2 | No | Cheapest; only clause rewrites. |
| C-010 | V3 | No | Per-task commits with coordinator posting (`EVAL:19`, `EVAL:54`). |
| C-011 | V2 = V3 | No | PRs only through pr-submit at the coordinator (`CLAUDE.md:50`). |
| C-012 | V3 | No | Scope, branch, no-push, plus own worktree. |
| C-013 | V2 | No | Loosening later is additive; published actions cannot be recalled. |
| C-014 | V3 | Yes (was V1) | One reviewable branch per worker before an approved push (`HWW:282`). |
| C-015 | V3 | Yes (was equal) | V3 alone now removes `README.md:31` from both WC-9 (`SPEC:73`) and the `/sc:git` row (`SPEC:156`). |
| X-001 | V2 = V3 | Yes (was V1) | Nothing that leaves the machine runs on relayed authority; concessions 1, 2, 7, 8. |
| X-002 | V3 | No | Authorized local commits, valid only in an isolated worktree. |
| X-003 | V3 | No | Applies "this session" only to the coordinator, where it can hold. |
| X-004 | V3 | No | `EVAL:54` puts progress posts at the coordinator. |
| X-005 | V3 | No | The repo separates local commits from publication (`HWW:282`, `HWW:324`). |
| X-006 | V2 | Yes (was V1) | No new mechanism; V3 conceded its implement window needs K3. |
| X-007 | equal | Yes (was V1) | V2 withdrew its `PRS` overreach; with D3 (a) recommended (`SPEC:341-343`) the point is moot for all three. |
| A-003 | V3 | Yes (was V1) | Smallest damage if authority is stale; the coordinator can still ask. |
| A-006 | V1 | No | Only (a) avoids deferral, but the cost is smaller than claimed (new evidence 1). |
| A-010 | equal | Yes (was V3) | After V1's withdrawal all three treat #326 as design input (`EVAL:74`). |

## Overall recommendation

I now recommend Variant 3 as refined in Round 1, option (c′), not my own option (a), and the spec's D4 recommendation (`SPEC:348`) should change from (a) to (c), with its `PRL:351` citation corrected. **Worker commits:** allowed only when the brief quotes the user's instruction naming a commit for that Task, and only when the coordinator has put that worker in its own worktree and branch under `.dev/worktrees/` (`CLAUDE.md:299`; `CAPS:115`). The worker commits once, after the command has written a `succeeded` contract: the Task's own files plus that worktree's `.dev/tasks` (`CLAUDE.md:37`). It never commits on the default branch, never pushes, and lists each SHA in `artifacts`. There are no commits inside `/sc:implement` until #326 K3 adds the step (`MW:63,67`; `EVAL:63`). **Everything that leaves the machine** (push, PR, GitHub comment or progress post, real-target install, VM, paid run) is done by the coordinator. It asks the person at the moment of action unless the instruction is in its own live conversation (`PRL:351`). PRs go only through `/sc:pr-submit` (`CLAUDE.md:50`), and auggie-review summaries are posted from the worker's `REVIEW.md` (`AUG:319`). Spec edits: EVAL F0, F1, F3 and F4 (`EVAL:50-54`); remove `README.md:31` from WC-9 and the `/sc:git` row; AC-4.2 gains "`git log origin/<branch>` unchanged" and makes "`git log -1` unchanged" depend on whether a commit was authorized. Option (a) remains a later, additive loosening. Adopt it only if the user names a concrete need, for example D3 (b) parallel PR monitoring or unattended real-target installs.
