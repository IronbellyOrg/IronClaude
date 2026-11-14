# Q27 final: may SW-02's own plan package be committed inside PR #539?

Terms used here: SW-02 is the work item "implement the owner's INV-008 ruling inside PR #539", where INV-008 is the finding that the sweep's `git status` call can run commands defined in a repository's git configuration, and PR #539 is the open pull request that adds the read-only `superclaude sweep` command. The plan package is the folder `.dev/tasks/to-do/<id>/` that `/sc:workflow` writes; the project requires such a written plan for any change touching more than one source file. Rule A-004 (spec section 6.4 rule 5) keeps new programs, data keys, extra files and alignment-program records out of PR #539.

## Debate result

Winner: proposal C (yes, commit SW-02's own plan package in PR #539). Confidence 88 percent. All three advocates picked C (3 of 3), including the advocate assigned to proposal A, who found the evidence that sank it.

Deciding evidence: `/sc:implement`, the executor for these plans, refuses a plan stored in a different checkout from the one it runs in: "A copied plan or a plan from another checkout fails here" (`~/.claude/skills/sc-implement-protocol/refs/managed-workspace.md:11`, with STOP code `E-MANAGED-INVALID` at `:7`). `/sc:workflow` always writes its plan into the checkout it runs in (`~/.claude/skills/sc-workflow-protocol/SKILL.md:47`). So the only working arrangement is plan and code in the same checkout. The spec's default for Q27 (plan in the coordinator home, referenced by absolute path) cannot run as written.

Proposal A (no; plan in the coordinator home): its strength is the smallest possible PR, with nothing from the plan added to #539's 1003 files, and it won that one point unanimously. Its weaknesses are decisive: the executor refuses the cross-checkout plan; it cannot start at all if the coordinator home question (Q26) is left at its default; and writing the plan in the coordinator home needs either the coordinator planning another session's item or a second session in the coordinator's folder.

Proposal B (no new package; add a phase to the existing sweep task file in #539): its strength is that no new package enters #539 and the whole Phase 1 history stays in one place. Its weaknesses: it uses the heavier task-file machinery (level 4) for an ordinary fix without the stated need the project's routing table requires, it does not answer the question asked, and it reopens a task file marked Done whose recorded review sign-offs covered a different scope (`.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md:7`).

Proposal C (yes): plan, progress record and fix stay in one checkout and PR, it needs no answer to Q26, it stays on the ordinary planned route (level 3), and the spec already reserves exactly one `.dev/tasks/` package slot in #539 for it (`merged-requirements.md:988`). PR #539 already carries 921 files under `.dev/tasks/to-do/` (measured 2026-11-14). Its weakness, raised by its own advocate and verified: the plan's final review step writes reports outside the package (`.dev/reflect/...` and `docs/memory/reflect/deviation-patterns-<slug>.md`, `~/.claude/skills/sc-reflect-protocol/SKILL.md:88`, `:593`), which must stay uncommitted.

## Final recommendation

Yes. SW-02's own plan package is written in the #539 checkout and committed in PR #539 with the fix, by named paths, including its progress record, its artifacts and its move from `to-do/` to `done/`. Before writing it, the #539 author records that the existing Done sweep task does not cover SW-02. The plan's review reports written outside the package stay uncommitted, and nothing else from the alignment program enters #539. Confidence 88 percent.

Strongest reason: the plan executor only runs a plan that sits in the same checkout as the code it changes, so every other placement either fails or needs heavier machinery.

Equals the spec's recommended answer: yes, with three commit-scope details added. The debate also found that the spec's default for this question cannot run.

## What would change the answer

If the owner wants zero new `.dev/tasks/` content in #539 under any reading of rule A-004, proposal B becomes the only working alternative, at the cost of level-4 machinery and a reopened Done task.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION
- Reason for the suggested handling in two sentences. The answer is decided by a verified tool rule, all three advocates agreed, and a wrong choice is undone by dropping a few plan files before the merge. The owner's taste on how strictly to read rule A-004 is the only human element, and the spec already reserves this one exception for the plan.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q27/adversarial/` (merged answer: `../merged-output.md`)
- fallback_mode: false (three advocate agents spawned in parallel; diff analysis, scoring, plan and merge done by this worker in-context, recorded in `return-contract.yaml`)
