# Hypothesis: Brittle evidence and provenance handoffs

**Investigation type:** Evidence-backed candidate cause
**Date:** 2026-10-23
**Status:** Complete candidate card; debate and independent validation pending
**Scope:** Evidence-only failures and incorrect change attribution in selected sessions01/15
**Template:** tech-research/SKILL.md, Codebase Research Agent Prompt, adapted as hypothesis card
**Rank:** Unassigned; actual adversarial debate pending
**Counting unit:** Incident-level evidence; repeated reviewer messages are not independent cases.

## Hypothesis
The conversion of verified work into durable proof sometimes loses meaning or provenance. A later reviewer then rejects missing, wrong or misleading evidence even when the delivered files did not regress.
This candidate explains evidence-only final failures and a false attribution of extra work; it does not explain every semantic defect in the sample.
**Key takeaway:** Proof can become the failing work product independently of the delivered implementation.

## Exact Mechanism
- Temporary test proof is replaced by an unrelated source-line citation when task QA becomes a ledger entry.
- A blank or incomplete evidence range survives the first final audit and is found by the next reviewer; repairing it changes proof, not delivery.
- Reconstructing the task baseline after editing from HEAD erases preexisting dirty work from the baseline, falsely making that work appear task-created.
- A missing checkpoint is classified by a guard as head-moved; that label does not itself prove HEAD changed.
**Key takeaway:** The common failure is an invalid connection between claim, evidence and historical state, not simply an inaccurate line number.

## Supporting Incidents
Case reports: [documentation and baseline case](../research/03-session-6f744b87.md), sections4-5; [credential final reviews](../research/06-session-0690ee9f.md), sections3-5.
Primary transcript root: `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/`.
The table's physical JSONL anchors are under that root, not line numbers in an extracted summary.

| Incident | Primary evidence | Discriminating observation |
|---|---|---|
| Initial credential package | `0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl:332,390,411,435`; nested `0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-abd76ef5e5d22848f.jsonl:36` | Genuine temporary lint proof became a README separator citation. Durable proof and pointer correction produced a pass without delivery changes. |
| Credential follow-up package | Same parent `:1425,1932,1968,2012,2015,2036`; nested `0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-af349dd52cae648a5.jsonl:16` | Task10's blank line10 existed before the first final repair. Second final found the old pointer error; first evidence repair also missed one row. |
| Dirty-baseline dispute and checkpoint | `6f744b87-6508-4d3e-9e71-c1193fd2162d.jsonl:188,204,217,234,485-486` | Explicit post-edit HEAD substitution created false extra hunks. Investigation recovered the truthful earlier Git tree; the render task separately lacked its start-HEAD file. |

**Key takeaway:** The strongest controls are unchanged delivery digests and historical-before/after evidence, not the mere sequence of verdicts.

## Counterevidence
The initial final-review evidence rejection was valid under its loaded rule; proof repair was real required work, not necessarily reviewer error. The follow-up also had a genuine literal lint-condition failure, so evidence weakness alone is incomplete.
The third final pass followed both pointer corrections and a changed rubric. Current `src/superclaude/skills/sc-implement-protocol/refs/qa.md:82` already says a moved line alone is never issues; these historical failures cannot prove that rule is still absent.
**Key takeaway:** This candidate explains historical avoidable repeats, not permission to ignore unsupported evidence or present policy as unchanged.

## Scope and Overlap
Direct support is concentrated in two selected sessions and three package/task contexts, not independent random samples. It overlaps changed review policy, incomplete first-pass checking and execution-record discipline.
The missing checkpoint contributes a halt mechanism, not proof that it caused either initial rendering failure or an actual repository movement.

## Competing Explanations
A strict evidence contract may intentionally demand durable proof even for correct delivery. Different review focus explains late detection of an old blank pointer; why the first final reviewer missed it is unknown. Changed policy partly explains the last verdict and prevents isolating the effect of pointer fixes.

## Falsification Test
For each evidence-only repeat, reconstruct the true pre-task state, retain the original proof and check every cited range under a fixed rubric. The candidate weakens if repeated failures persist despite complete valid proof, correct baseline and unchanged delivered requirements, or if the supposed proof-only interval contains a necessary delivery correction.
This comparison is proposed, not executed here; it must not waive semantic support just because a cited line exists.

## Provisional Evidence Strength and Limits
Strong within the named historical evidence failures: actual ledger writes, nested tool output, unchanged delivery digests and independently recovered Git trees support the mechanisms. Breadth is limited; digests exclude evidence artifacts and policy. No fleet-wide frequency, numerical probability or new-versus-old-version effect follows.

## Gaps and Questions
The actor changing the rubric and the exact reason the first audit missed the blank pointer remain unknown. A fresh Read of the formerly archived `TASK-WF-issue358FollowUp-20261022-193837/artifacts/t10-markdownlint.log` under the recorded Coder worktree returned file does not exist. The original nested transcript still preserves that log body; this card does not claim the archived file survives now.

## Stale Documentation Found
Historical pointers include an unrelated README separator, blank log line and a later-task line shift. The current managed FINAL rule already distinguishes moved pointers from unmet end-state criteria. Preserved old and new rule text is in [historical rule evidence](../research/historical-review-rules.json); current matching source copies do not erase that historical change.

## Summary
Brittle proof handoffs explain repeat rejections without new delivery defects in the named cases. Correct baselines, durable proof and meaningful citation checks address different mechanisms and must not be conflated. The historical rubric change limits attribution of the final pass. This remains an unranked candidate for the requested debate.
