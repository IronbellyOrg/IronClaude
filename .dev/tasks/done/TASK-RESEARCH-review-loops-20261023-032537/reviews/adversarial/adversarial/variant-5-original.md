# Hypothesis: Late feasibility and repair-authority checks

**Investigation type:** Evidence-backed candidate cause
**Date:** 2026-10-23
**Status:** Complete candidate card; debate and independent validation pending
**Scope:** Known retained fixture and environmental blockers in selected sessions27/01
**Template:** tech-research/SKILL.md, Codebase Research Agent Prompt, adapted as hypothesis card
**Rank:** Unassigned; actual adversarial debate pending
**Counting unit:** Incident-level evidence; repeated reviewer messages are not independent cases.

## Hypothesis
A task reaches review before the executor establishes that its required evidence can be produced and its blocking inputs can be corrected within the allowed scope. A resubmission then preserves a known unmet condition, so review correctly fails again.
This candidate explains retained blockers, not a universal inability to implement the original requirement.
**Key takeaway:** Rechecking an unchanged blocker cannot demonstrate its resolution.

## Exact Mechanism
- A deficient security fixture is frozen before its required semantic property is checked. Repair authority explicitly excludes changing it; three other repairs succeed, but the fourth original finding remains.
- A generated acceptance condition requires a real manual-page render when man is available. The available command prints a notice instead; static formatting evidence cannot establish rendering.
- Resubmission changes neither the frozen property nor the missing rendering capability. A scoped human decision is eventually required.
**Key takeaway:** The repeated verdict reflects an unchanged acceptance state; it is not evidence that the permitted fixes broke something new.

## Supporting Incidents
Case reports: [oracle fixture case](../research/02-session-a9b88895.md), sections4.4-6; [documentation render case](../research/03-session-6f744b87.md), sections2-4.
Primary transcript paths are absolute below; anchors are physical JSONL records.
Oracle review artifact was directly reread for this card: `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-2.md:20-28`.

| Incident | Primary evidence | Discriminating observation |
|---|---|---|
| Frozen security fixture | `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1.jsonl:291,383,398,450,521,573,668` | First repair explicitly excludes the known default_path=false fixture. Second review confirms three repairs and repeats only that original defect; authorization enables a one-field correction and later PASS. |
| Non-rendering manual-page command | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/6f744b87-6508-4d3e-9e71-c1193fd2162d.jsonl:413-414,430,433-434,443,450,506,527` | Initial nominal rc0 did not prove rendering. Static-only retry explicitly changes no text; second cannot-verify names the same unmet render clause. Scoped acceptance retains cannot-verify, not a successful render. |

**Key takeaway:** Both repeated failures are predictable from a documented blocker that the resubmission leaves unchanged.

## Counterevidence
The frozen fixture's original requirement was feasible: correct default-path data could have been authored before freezing. Its first three repairs worked. A functioning renderer could satisfy the manual-page clause elsewhere; no malformed manual page was demonstrated.
Re-review could legitimately verify repaired portions while recording a retained blocker, so the second oracle review was not intrinsically pointless or invalid.
**Key takeaway:** The claim is late blocker handling under the observed constraints, not an impossible specification or a rule against all resubmission.

## Scope and Overlap
Direct support covers two retained-blocker incidents, narrower than the whole six-session sample. It overlaps weak semantic assertions that admitted the fixture and weak availability checks that accepted a notice executable as rendering capability.
This candidate concerns unchanged blockers; later monitor completion by acceptance is also not repaired compliance, but its many earlier failures require other explanations.

## Competing Explanations
The freeze is a deliberate anti-overfitting control, and the reviewer may be correctly enforcing it. Ordinary incomplete work explains the original fixture omission; this hypothesis explains why allowed repair and resubmission could not remove that remaining finding. Renderer capability is an environmental limitation, not necessarily a defect in document editing.

## Falsification Test
Before resubmission, identify the unmet property, actual evidence-producing capability and permitted correction. Check whether the next attempt changes that blocker or obtains the required scoped decision. The candidate weakens if a valid permitted change demonstrably resolves the condition yet the reviewer repeats the same objection without support.
That is a proposed comparison; no installs, freeze bypass, altered acceptance criteria or new task execution occurred here.

## Provisional Evidence Strength and Limits
Strong for the two specific unchanged blockers: original criteria, excluded repair action, repeated finding and later scoped resolution are explicit. Moderate as a general explanation because other cases contain newly introduced or previously missed defects. No probability or claim of universal mathematical impossibility is warranted.

## Gaps and Questions
No actual manual-page rendering is established. A fresh Read of the formerly archived `TASK-WF-issue358FollowUp-20261022-210638/artifacts/t6-fix-evidence.log` under the recorded Coder worktree returned file does not exist; original transcript record450 preserves its findings. This card relies on captured historical evidence, not claimed present-day file availability or a newly tested renderer.

## Stale Documentation Found
No stale-documentation cause is needed for these incidents. The deliberately re-frozen fixture is an authorized changed input, not untouched evidence. The rendering clause was part of the executed plan even though its availability guard was inadequate.

## Summary
Late feasibility and authority checks explain why these resubmissions retained an already identified blocker. Correct reviewers repeated valid original findings while other fixes succeeded. One case ended with an authorized fixture correction and PASS; the other ended with accepted unverified rendering. Neither justifies weakening requirements or assuming every later failure is caused by repair.
