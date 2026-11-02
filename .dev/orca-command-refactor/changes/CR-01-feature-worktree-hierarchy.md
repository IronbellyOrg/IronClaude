# CR-01: Feature worktree hierarchy

Status: PROPOSED. Separate spec change, to be applied in the next consolidated revision round together with the D1-D5 and git-ownership outcomes. Not yet applied to `specs/orca-worker-contract-spec.md`.

## 1. Problem
By default Orca workers share the coordinator's worktree (`CAPS:115`). The spec allows that in normal use (WC-11, `SPEC:75`) and isolates a worker only inside the 7.2 live check (`SPEC:235`). It has no rule for when a worker needs its own checkout, and four findings show that sharing is unsafe for some work:
- `/sc:implement`'s rollback restores or deletes every path changed in the worktree since its task started, excluding only its own run files and certain `.dev/` and submodule paths (`~/.claude/skills/sc-implement-protocol/refs/retry.md:201-208,220`). It cannot see other Orca workers, so it can overwrite or delete their output. Found in the git-ownership debate (`decisions/git-ownership/debate/adversarial/round2-advocate-b.md`); derived from protocol text, not yet observed in a run.
- `/sc:pr-submit` binds to the PR head checkout, commits one fix per cycle there, and halts when a fix touches a file with pending changes (`~/.claude/skills/sc-pr-submit-protocol/SKILL.md:268,274,318`; `round2-advocate-c.md`).
- `/sc:implement`'s retry requires that HEAD has not moved since the task started (`retry.md:41`). Any commit by another worker in the same checkout breaks it, and two git writers in one checkout contend for the same index lock.
- Issue #326 asks for a worktree per parallel experiment and cleanup of worktrees and branches afterwards (`review/issue-326-evaluation.md`).

Orca's own guidance is to create a worktree "only when the user requested one or a concrete checkout or filesystem conflict makes sharing unsafe" (`CAPS:115`, quoting `[G:placement]` lines 8-11). The findings above are exactly such conflicts, so the fix is a conditional rule, not a worktree for every worker.

## 2. Proposed model
1. **One top-level worktree per feature.** It holds the feature branch; the coordinator runs there. Orca lineage records it as the parent; its Orca metadata links the feature's issue and, later, its PR (`orca worktree set --issue`, `--pr`, `--workspace-status`).
2. **Child worktrees only when a trigger applies.** The coordinator starts a worker with `--worktree new-child --base-branch <feature branch>` when any of these hold, and otherwise uses the shared parent worktree:
   - T1: the brief authorizes the worker to commit;
   - T2: the worker runs `/sc:implement` while any other worker writes outside `.dev/` in the same worktree;
   - T3: the worker runs `/sc:pr-submit` (its checkout must be the PR head with no other writer for the whole loop);
   - T4: the work is a parallel experiment to be compared or discarded (#326).
   T1-T3 come from the git-ownership debate (B's rule P1 and C's addition M1); T4 from #326.
3. **Branching is explicit.** Orca treats lineage and git base as separate decisions (`[G:placement]`: "Orca lineage, Git base, filesystem isolation, coordination parentage, UI grouping, and execution host are separate decisions"), so every child names `--base-branch <feature branch>`.
4. **Merge-back and cleanup belong to the git owner.** When a child's Task settles and its result is admitted (section 2.3), the git owner chosen by the git-ownership decision merges the child branch into the feature branch, then removes the child worktree with `orca worktree rm` and deletes its branch. A discarded experiment is removed without merging. Orchestration verbs never delete worktrees (`CAPS:115`), so this is an explicit step.
5. **Every child gets setup before use.** A new worktree lacks the gitignored `.claude/` copies, a Python environment and a code-graph index. The coordinator starts children with `--setup run` and does not dispatch the command until setup has succeeded (the same gap as defect D3 in `review/final-diff-review.md`).

## 3. Spec changes (wording)
Keep additions to these four places; add no other rule.
- **Section 2.3, placement item.** Replace "and the worktree placement (`CAPS:115`)" with: "and the worktree placement: the shared feature worktree, or a child worktree created with `--worktree new-child --base-branch <feature branch>` when CR-01 trigger T1, T2, T3 or T4 applies (`CAPS:115`)."
- **WC-11.** Append: "A worker that commits, runs `/sc:implement` alongside other writers, runs `/sc:pr-submit`, or runs a parallel experiment gets its own child worktree (section 2.3); sharing is for workers that only write their own report directory."
- **Section 2.3, new short paragraph "Feature worktree".** "Each feature has one top-level worktree on its feature branch, linked to its issue. Child worktrees branch from the feature branch. After a child's result is admitted, the git owner merges its branch into the feature branch, then removes the worktree and deletes the branch; a discarded experiment is removed without merging. A child is dispatched only after its setup has succeeded."
- **Section 7, one acceptance check.** "Two workers in one feature: one `/sc:implement` task whose rollback is forced, in a child worktree, and one report-only worker in the parent. Pass: the report-only worker's files are unchanged, and the child's branch merges into the feature branch or is removed as the brief says."

## 4. Interactions
- **Git ownership** (`decisions/git-ownership/`): all five options converged on the hybrid E (local commits by workers only where granted; one owner for push, PR and comments). CR-01 supplies E's placement rule; the git owner it names also merges children back and removes them.
- **D2 and D3:** a child per `/sc:pr-submit` run is what makes parallel PR monitoring under D3 (b) workable, and a child per `/sc:implement` keeps its halt and rollback from touching other work under D2.
- **D4 and worker commits:** T1 only applies if D4 lets a brief authorize commits.
- **Final-review defect D3** (`review/final-diff-review.md`): children need the same setup the 7.2 disposable worktree needs, so one fix covers both.
- **Issue #326:** satisfies the worktree-per-experiment and cleanup asks; deleting branches after a PR merges stays in #326.

## 5. Open questions
1. **Location: RESOLVED by the user (2026-11-02): defer to Orca's default paths.** Every worktree, parent or child, is created by Orca (`worker-start --worktree new-child`/`new-top-level` or `orca worktree create`) at Orca's default location, observed as `/home/coder/workspaces/worktrees/<repo>/<name>` for this spec's own Orca-created worktree (`orca-ide worktree show`: `creatorProvenance.kind = paired-device`, `createdWithAgent = claude`). No worktree is created with raw `git worktree add` under `.dev/worktrees/`. The repo rule at `CLAUDE.md:299-300` and every IronClaude file that encodes `.dev/worktrees/` must be refactored to Orca's defaults; that repo-wide change is planned separately (17 tracked files outside `.dev/`, 108 references, from `git grep -E '\.dev/worktrees|git worktree add'`, 2026-11-02). This also replaces the 7.2 disposable worktree under `.dev/worktrees/` (`SPEC:235`) with an Orca-created one, which removes the UNVERIFIED question of whether Orca accepts a worktree it did not create (`SPEC:236`).
2. **Setup content.** Whether the repository's Orca setup hook (`--setup run`) performs `make sync-dev`, creates the Python environment and initializes the code graph is UNVERIFIED. If not, the coordinator must run those steps itself before dispatch.
3. **Merge conflicts.** When two children change the same file, the merge-back needs a rule: the git owner stops and reports the conflict instead of resolving it automatically. Recommended; not yet debated.
4. **Stale children.** A long-running child can fall behind the feature branch. Recommended: the git owner rebases or merges the feature branch into the child only between Tasks, never while a worker is running in it.
5. **Upstream is never touched (user rule, 2026-11-02).** SuperClaude upstream (`SuperClaude-Org/SuperClaude_Framework`) is ignored: never pushed to, never interacted with. Orca records this repo's project as `github:superclaude-org/superclaude_framework` (`orca-ide worktree show`, `projectId`). Until Orca's project identity is confirmed to resolve to `IronbellyOrg/IronClaude`, the coordinator does not use Orca's issue or PR linking (`worktree create --issue/--pr`, `worktree set --issue/--pr`); feature status and issue links go through `gh ... --repo IronbellyOrg/IronClaude` only, and PRs only through `/sc:pr-submit` on the fork.

## 6. Evidence
- `orca-ide orchestration worker-start --help` line 3 (`--worktree <current|selector|new-child|new-top-level>`), lines 21 and 41 (`--base-branch`; creation flags rejected for existing worktrees).
- `orca-ide skills get orchestration --reference references/placement-and-remote.md`: "Stacked child worktree" example with `--worktree new-child`; lineage, git base, isolation and grouping are separate decisions.
- `orca-ide skills get orca-cli`: `worktree create --parent-worktree <selector>`, `worktree set --parent-worktree` / `--no-parent`, lineage rules, and `--no-parent` does not choose the git base.
- `orca-ide worktree show --worktree path:/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs --json`: `parentWorktreeId = None`, `childWorktreeIds = []`, `baseRef = refs/remotes/origin/master`, `projectId = github:superclaude-org/superclaude_framework` (read 2026-11-02).
- `.dev/orca-command-refactor/inventory/orca-capabilities.md:115` (`CAPS:115`).
- `~/.claude/skills/sc-implement-protocol/refs/retry.md:41,201-208,220`; `~/.claude/skills/sc-pr-submit-protocol/SKILL.md:268,274,318`.
- `CLAUDE.md:299-300` (worktree location rule).
