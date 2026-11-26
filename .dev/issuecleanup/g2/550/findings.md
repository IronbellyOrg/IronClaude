# Issue 550 review
## Verdict and evidence
**Verdict: in-progress.** Issue [#550](https://github.com/IronbellyOrg/IronClaude/issues/550), preserving and integrating proven tasklist experiments, is partly addressed by retained research and a value inventory, but its complete experiment classification, incorporation and same-ground-truth retests are not established. Keep it open; this is not a request to restore the retired tasklist command.

Evidence:
- A real value inventory already exists: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/synthesis/synth-08-value-inventory.md:14-23` names study, brainstorm and collaboration-design source ledgers; `:43` defines destination-based row fields, not the issue's experiment/result-class acceptance matrix. Its totals were read, not recomputed.
- The comparison explicitly calls this research an input to a later plan, not an execution plan: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/tasks/to-do/COMPARE-review-panel-run1-vs-run2-20261114/MERGED-review-panel-unification.md:7382-7388`. Its tasklist baseline remains `6c0984326`: `:983-993`. That does not establish coverage of later experiment results.
- Cached experiment-branch commit `bfd2b357c` retains a 2026-11-16 Recipe Ledger result, discussed below. `c44c98a77a0bc8fcc122a60bc87a2cf9005479e0`, the post-baseline preservation commit required by the issue, is locally readable but is not an ancestor of this checkout (`git merge-base --is-ancestor c44c98a77 HEAD` exited 1). Equivalent selective copying is UNVERIFIED; ancestry alone cannot rule it out.
- [PR #623](https://github.com/IronbellyOrg/IronClaude/pull/623), merged as `7f93c0d9f7b72938976127d59a2bf523c06d5e03`, ships a provisional default model mix and its supporting selection machinery, not the experiment process designs. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/data/review-panel.wonsol.json:5` explicitly excludes the evaluation seat lenses and calls the choice provisional because its confirming test missed its pre-registered bar. This is partial adjacent adoption, not proof of all #550 acceptance criteria.
- Live issue read: OPEN, one status-review comment dated 2026-11-17, no closing-PR references and no retest result posted in its comments. Read-only PR searches for `550` and the exact tasklist experiment head returned no results. These searches do not prove that no indirectly related PR exists.
## Real current state
### Preserved or implemented
- Shared review helpers and packaged model panels exist in this checkout. The current default pointer is wonsol, and its description explicitly limits shipment to the model mix; it does not claim to ship collaboration designs or Recipe Ledger instructions.
- The older research has a durable value-capture inventory and a merged comparison. Therefore the issue's 2026-11-17 comment saying an inventory is unverified is no longer the full local picture. The existing inventory is useful starting material, not evidence that every experiment has been classified as proven, not proven or untested.
- Cached `origin/ironbelly/eval-tasklist-review-panel` points to `bfd2b357c`, whose Recipe Ledger report is retained at git object `bfd2b357c:.dev/eval-workspaces/tasklist-review-panel/20261114-recipe-ledger/results/derivation-3x/SUMMARY-9reps.md`. The report states 81 panel runs across three arms, three packages and nine repeats. It labels the evidence exploratory, reports a higher counted-find total for Recipe Ledger but no difference in real blocking finds, and says the +35% time cap failed on two packages. Those are the report's claims; raw scoring and statistics were not independently recomputed here. Its own caveats rule out treating it as a confirmed production winner.
- Cached `c44c98a77` progress note retains all five collaboration designs, their early counted rows, invalid rows and time-cap exceptions. The note explicitly says its one-row-per-cell numbers are not comparable results. Both artifacts are later than the comparison's pinned tasklist baseline.

### Not established
- A complete, current experiment-by-experiment acceptance matrix covering the post-baseline commits, durable provenance and result class is UNVERIFIED.
- Incorporation of every qualifying design into the unified panel and same-ground-truth retests there are UNVERIFIED. No such results are posted on #550.
- The parent #549 and feature #520 remain OPEN. This does not prove all unification work is absent, only that the programme is not recorded as complete.
- [PR #632](https://github.com/IronbellyOrg/IronClaude/pull/632), merged as `af5fb69eb9b016287e3560cda50bce2a16123349`, retired the roadmap/tasklist/sprint command family. A local Glob of those source packages returned no files. Preserve applicable experiment value in the surviving shared review/workflow/reflect paths rather than interpreting this issue as restoration of those commands.
## Concrete next steps
1. Inventory every tasklist experiment after baseline `6c0984326`, beginning with `c44c98a77`, and include the 2026-11-16 Recipe Ledger result. For each record the evidence path and one result class: proven, not proven or untested. Treat the exploratory Recipe Ledger result as not proven until a pre-registered, same-ground-truth decision says otherwise.
2. Preserve that inventory and its evidence in the durable location named by the #549 unification plan, without restoring the retired tasklist command family.
3. Incorporate only designs the plan classifies as proven, using the surviving shared review, workflow and reflect paths.
4. Retest each incorporated design against the same 16-defect ground truth and post the result on #550.
## Complexity and size
**Complexity: complex. Size: L.** The remaining work crosses historical experiment evidence, a unification decision, selective incorporation into surviving review paths and multiple retests; the shared panel code itself is already present and does not make this a large new-code feature.
## Priority
**Priority: P2.** It preserves measured review value before the tasklist experiment branch or worktree disappears, but no current production defect or other issue is verified to be blocked by it.
## Dependencies
- Needs #549, the parent Review Panel unification programme, to name the durable destination and incorporation route. #549 is OPEN.
- #520, the reusable Review Panel feature, remains OPEN and defines the shared feature this issue feeds.
- No issue is verified as blocked by #550.
## Related issues
- #549: parent unification programme, OPEN.
- #520: reusable Review Panel feature, OPEN.
- #487: reusable spec/task evaluation framework, OPEN.
- #531: Shadow Run Module, OPEN.
- #546: model-policy hook arising from the experiment incident, OPEN; related context, not an acceptance dependency.
- IronbellyOrg/PrivateRepoF#505: private workspace-fault issue named by the experiment progress note. Its current state is UNVERIFIED because this task permits only IronClaude repository reads.
## Related PRs
- No directly matching PR was returned by the all-state `550` search or the exact experiment branch-head search. Search results do not prove that no direct or indirect PR exists.
- #623, merged as `7f93c0d9f7b72938976127d59a2bf523c06d5e03`: provisional wonsol model-mix default; explicitly not the evaluation seat lenses.
- #519, merged as `d2d8a2d166c945f556d921b31530a3673f00df89`: shared reflect panel stages, dormant or shadow-only and not the tasklist designs.
- #581, merged as `fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d`, and #582, merged as `64e8eacf2b3ff40be07ae9c9959071684c3765a0`: later shared review safety and consequence-rule changes that any incorporation must account for.
- #632, merged as `af5fb69eb9b016287e3560cda50bce2a16123349`: retired roadmap, tasklist and sprint commands. This changes the preservation route but does not erase experiment evidence.
## Verification limits and negative evidence
- Full event-level GitHub timeline is UNVERIFIED: the permitted `gh issue view` reads exposed issue dates, current state, comments, relationships and closing-PR references, not every timeline event. No disallowed API call was used to fill that gap.
- The complete experiment inventory, qualification of every design and all same-ground-truth retests are UNVERIFIED.
- Whether every post-baseline commit was selectively copied despite not being an ancestor is UNVERIFIED. The local 5,950-row inventory totals were read but not recomputed.
- Recipe Ledger raw scores, permutations and judge outputs were not independently recomputed. Worktree deletion state and uncommitted branch files were not verified.
- Direct searches for `550` and the exact branch head found no PR. They cannot prove no indirectly related PR exists.
- IronbellyOrg/PrivateRepoF#505 state is UNVERIFIED because this task allows GitHub reads only in IronbellyOrg/IronClaude. No source was modified and no tests were run.
