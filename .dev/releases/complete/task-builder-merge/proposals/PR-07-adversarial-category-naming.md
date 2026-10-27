---
proposal_id: PR-07
case: D
source_mechanism: src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1112-1117 (5-category adversarial agent prompt — drift / contradictions / omissions / weakened-criteria / invented-content)
target_integration_point: src/superclaude/skills/task-builder/SKILL.md:961 (A.10.5 qualitative 15-item) and src/superclaude/agents/rf-qa-qualitative.md:527-583 (task-qualitative 15-item checklist) — augment existing adversarial-stance categories with sc:tasklist's 5 named axes
final_report_citation: FINAL-REPORT §3.1 (5-category validation prompt structure); §6.3 (adapt intent — naming exercise within existing checklist, not new mechanism)
direction_inversion_basis: |
  FINAL-REPORT §6.3 lesson explicitly distinguishes intent-porting from implementation-porting. This proposal is the PUREST intent port: sc:tasklist names 5 adversarial axes; task-builder's rf-qa-qualitative has the same adversarial stance (Bucket D rf-qa-qualitative.md:82-95 — "find problems, do not confirm work") but generic. The asymmetry from §6.3 inverts here: in RF→SC, intent-porting succeeded by *removing* implementation; in SC→RF, intent-porting succeeds by *adding labels* without changing implementation.
  Risk of over-engineering: LOWEST among PR-01-07 because no new code path or stage. Just sharper named checks added to an existing checklist.
conflict_with_task_builder: yes
invariant_protected: zero-trust QA
complexity_estimate: ~15 lines-of-change
expected_quality_gain: medium — sharpens existing adversarial review; provides explicit categories for QA reports
---

## Mechanism in /sc:tasklist

sc:tasklist's Stage 7 validation agents receive a verbatim instructions block (Bucket A SKILL.md:1108-1127) with five named check categories enumerated at SKILL.md:1112-1117:
1. **Drift** — task content deviates from roadmap requirements over time/iterations.
2. **Contradictions** — internal inconsistency between task fields or between tasks.
3. **Omissions** — required roadmap deliverables missing from any task.
4. **Weakened criteria** — acceptance criteria looser than what the roadmap demands.
5. **Invented content** — task references files/concepts not present in the roadmap.

Each finding is reported with Severity / Task ID / Problem / Roadmap evidence / Tasklist evidence / Exact fix.

## Proposed adaptation in task-builder

rf-qa-qualitative's task-qualitative phase (Bucket D rf-qa-qualitative.md:527-583, 15-item checklist) implements adversarial stance generically ("Assume the work contains errors. Your job is to find what was missed" — repeated 8× per Bucket C). What it LACKS is the 5-axis named taxonomy. Per CB-3, this is a per-check classification — we add 5 named axes as a header section in the agent's checklist, not as 5 new checklist items.

Edit `src/superclaude/agents/rf-qa-qualitative.md` task-qualitative phase to add:

> **Five Adversarial Axes (applied to all 15 checks below — find ANY of these and FAIL the relevant check):**
> - **Drift:** Has the task content drifted from BUILD_REQUEST.GOAL through paraphrasing? Find paraphrases that substitute weaker verbs ("review" instead of "validate") or scope reductions.
> - **Contradictions:** Do two items in the task contradict (one says "use A", another implies "must not use A")? Do frontmatter fields contradict body content?
> - **Omissions:** Are any BUILD_REQUEST QA_GATE_REQUIREMENTS / VALIDATION_REQUIREMENTS / TESTING_REQUIREMENTS (rules #16/17/18 SKILL.md:1558-1562) missing from the task as checklist items?
> - **Weakened criteria:** Are acceptance criteria phrased more permissively than BUILD_REQUEST or research findings warrant? Look for "or" splits, "may" verbs, optional clauses.
> - **Invented content:** Does the task reference files, modules, or interfaces NOT present in `research/*.md` evidence files? Cross-check every named artifact.

Each finding in rf-qa-qualitative's Items Reviewed table (Bucket D rf-qa-qualitative.md:675-714) should annotate which axis fired (e.g., "Issue #3 [axis: contradiction]").

## Why this is NOT a 1:1 port

In sc:tasklist, the 5 axes ARE the entire validation taxonomy (Stage 7 agents check only these 5). In task-builder, the 5 axes are an OVERLAY on the existing 15-item qualitative checklist — they sharpen but do not replace. The semantic difference: sc:tasklist agents stop after the 5 checks; rf-qa-qualitative does its full 15-item review with the 5 axes acting as adversarial lenses for each. FINAL-REPORT §6.3 risk inverted: this proposal does LESS porting than the RF→SC P4 proposal (which tried to replicate the entire evidence-extraction taxonomy and was found redundant); naming-only is the lightest possible touch.

## Invariant analysis

- **zero-trust QA (REINFORCED):** the 5 named axes make the adversarial stance more SPECIFIC; rf-qa-qualitative still adheres to "Zero tolerance — if you can't verify it, it fails" (Bucket C SKILL.md:1340).
- **self-contained-item (untouched):** item schema unchanged.
- **evidence-bound-item (untouched):** the axes themselves require evidence — "invented content" axis explicitly requires cross-checking against `research/*.md`.
- **persistent .dev/tasks/ artifact (untouched):** axes appear in `qa/qa-qualitative-review.md` reports which already persist.
- **parallel research (untouched):** this is a checklist annotation; no execution flow impact.

## Failure modes the proposal must handle

1. **Axis ambiguity (a finding could match 2+ axes).** Agent picks the most-specific axis; record both if explicit. Bucket D rf-qa-qualitative.md:789 already mandates "contradictions always IMPORTANT or CRITICAL" — preserves severity floor.
2. **Axis overlap with existing checklist items.** The 5-axis overlay is an annotation, not a replacement. Items 1-15 still run; the axes provide finding-source classification.
3. **Drift detection requires baseline.** "Drift" axis only fires if BUILD_REQUEST GOAL is captured verbatim earlier in the qualitative review. Bucket D rf-qa-qualitative.md task-qualitative checklist item likely already includes a "scope check" (Bucket C SKILL.md:961 references 15-item agent-side checklist). Verify alignment when implementing.
4. **Over-flagging on "weakened criteria".** Mitigation: an item is "weakened" only if BUILD_REQUEST or research evidence demands stronger phrasing — speculation about absent stronger phrasing does not count. Aligns with Bucket D rf-qa-qualitative.md:766-775 anti-inflation rules.

## Concrete change sketch

- Edit `src/superclaude/agents/rf-qa-qualitative.md` near lines 527-583 (task-qualitative phase) to insert a "Five Adversarial Axes" header subsection BEFORE the existing 15-item checklist.
- Edit the output template near rf-qa-qualitative.md:675-714 to require the `axis` annotation on each finding in the Items Reviewed table.
- Edit `src/superclaude/skills/task-builder/SKILL.md:961` to reference the new 5-axis lens when spawning A.10.5: "rf-qa-qualitative applies the 5 Adversarial Axes (drift / contradictions / omissions / weakened-criteria / invented-content) across its 15-item checklist."
- No new agent file; no new gate stage.
