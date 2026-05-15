---
proposal_id: PR-06
case: D
source_mechanism: src/superclaude/skills/sc-tasklist-protocol/SKILL.md:979-1034 (17-point pre-write gate, specifically the structural checks 11/13/14/15/16/17 unique to sc:tasklist)
target_integration_point: src/superclaude/skills/task-builder/SKILL.md:898-906 (A.10 task-integrity 9-item checklist) and src/superclaude/agents/rf-qa.md:264-287 (task-integrity 20-item agent-side checklist) — per-check classification per CB-3, not bulk import
final_report_citation: FINAL-REPORT §3.1 (17-point quality gate runs before any file is written); §6.3 (adapt intent, not implementation — port checks individually)
direction_inversion_basis: |
  FINAL-REPORT §6.3 found 4/5 RF→SC ports over-engineered because they ported COMPLEX correction-cycle MECHANISMS into SC's simple single-pass architecture. The inverse risk for THIS proposal is the opposite: porting SC's 17 SIMPLE structural checks into task-builder's complex multi-stage gates risks gate redundancy, not over-engineering.
  Asymmetry resolution: per CB-3 advisory, "must classify per-check, not in bulk." This proposal does NOT import all 17. It identifies the SPECIFIC structural checks present in sc:tasklist's 17-point gate that are NOT in task-builder's 9-item task-integrity (Bucket C SKILL.md:898-906) or 15-item validation checklist (SKILL.md:1491-1507), and adds only those.
  Checks already covered by task-builder are EXCLUDED. Net additions: placeholder/TBD scan, circular-dependency detection, XL splitting enforcement, per-phase item count bounds, clarification-task adjacency. ~4-6 new items, not 17.
conflict_with_task_builder: yes
invariant_protected: zero-trust QA
complexity_estimate: ~20 lines-of-change
expected_quality_gain: medium — closes specific structural gaps; additive to existing gates without redundancy
---

## Mechanism in /sc:tasklist

sc:tasklist's pre-write gate (Bucket A SKILL.md:979-1034) enumerates 17 checks. Of these, the ones NOT present (per Bucket C analysis CB-3) in task-builder's 9-item task-integrity (SKILL.md:898-906) and 15-item validation checklist (SKILL.md:1491-1507):

1. **Check 11** (Bucket A SKILL.md:1000) — No placeholder/empty task descriptions (no "TBD"/"TODO"/title-only).
2. **Check 13** (Bucket A SKILL.md:1025) — Phase task count >=1 and <=25.
3. **Check 14** (Bucket A SKILL.md:1026) — Clarification Task adjacency before blocked task.
4. **Check 15** (Bucket A SKILL.md:1027) — Circular dependency detection (no A→B→C→A).
5. **Check 16** (Bucket A SKILL.md:1028) — XL splitting enforcement (items flagged XL must have subtasks).
6. **Check 17** (Bucket A SKILL.md:1029) — Confidence bar format consistency.

(Other 11 checks are either already present in task-builder, irrelevant to single-task output, or sc:tasklist-specific bundle properties like "Every phase file starts `# Phase N -- <Name>`".)

## Proposed adaptation in task-builder

Add 4-6 specific checks to `src/superclaude/agents/rf-qa.md:264-287` (task-integrity 20-item checklist) and mirror in `src/superclaude/skills/task-builder/SKILL.md:898-906` (A.10 9-item):

- **TB-Add-1: Placeholder scan.** "No checklist item contains 'TBD', 'TODO', 'FIXME', or is title-only without context/action/output/verification/completion-gate body."
- **TB-Add-2: Item count bounds.** "Track has >=3 and <=40 checklist items (split larger via Template 02 multi-phase if needed); single-track has >=3 and <=50."
- **TB-Add-3: Clarification adjacency.** "If task has Open Questions, related blocked checklist items reference the open question by index in their Context field."
- **TB-Add-4: Circular dependency.** "Item-to-item dependencies form a DAG; no item depends on a later item that depends back on it."
- **TB-Add-5: Granularity check.** "If an item is flagged as 'complex' or 'multi-file', either it is split into subtasks (Template 02 nesting) OR a critical-rule-aware comment justifies single-item handling." (Mirrors check 16 XL splitting, adapted to task-builder's lack of XL effort labels.)
- **TB-Add-6: Confidence/Verification format consistency.** "All Verification fields use the same `Verify: ...` prefix; all Acceptance Criteria entries use the `- ✅` or `- [x]` form per Template 01/02 conventions."

Per CB-3, each addition references its source check ID for traceability ("Imported from sc:tasklist check 11 / 13 / 14 / 15 / 16 / 17").

## Why this is NOT a 1:1 port

The full 17 checks include sc:tasklist-specific bundle invariants (e.g., "Every phase file in index exists in bundle," "Index contains literal phase filenames"). Task-builder emits a SINGLE MDTM file per track, not a multi-file bundle indexed by Sprint CLI; those checks have no analog and are correctly omitted. Per FINAL-REPORT §6.3, porting all 17 wholesale would import bundle-specific machinery that doesn't apply to task-builder's output format. This proposal is the CB-3 per-check classification in action.

## Invariant analysis

- **zero-trust QA (STRENGTHENED):** additive checks make the existing gate adversarial-stronger. No existing check is removed or weakened.
- **self-contained-item (REINFORCED):** TB-Add-1 (placeholder scan) directly enforces the 5-field schema by rejecting title-only items.
- **evidence-bound-item (untouched):** the new checks are structural; evidence binding remains a separate rule (#2 SKILL.md:1530).
- **persistent .dev/tasks/ artifact (untouched):** check additions live in gate logs that already persist in `qa/*.md`.
- **parallel research (untouched):** checks run at task-integrity gate which is post-research.

## Failure modes the proposal must handle

1. **Check false positives.** Each new check should produce an unambiguous error message naming the offending item ID (e.g., "Item 1.4 contains 'TODO' on line N — replace with concrete description"). False positives wasted-cycle risk is contained by Bucket D rf-qa.md:407 ("never claim VERIFIED without tool output") — checks use Read/Grep evidence, not pattern speculation.
2. **Existing tasks (pre-import) fail the new checks.** Migration path: tasks created before this proposal lands are grandfathered. New tasks fail the gate per existing fix-cycle rules.
3. **Check overlap with rf-qa-qualitative.** Risk: TB-Add-1 (placeholder) and TB-Add-6 (format consistency) could re-fire in qualitative. Mitigation per PR-04 — Inherited Structural Verdict prevents re-checking.
4. **Bound thresholds (TB-Add-2) misfire for legitimate large tasks.** Threshold rationale should cite empirical data from `.dev/tasks/done/`; if absent, mark as ADVISORY-fail (warn not block) until calibrated.

## Concrete change sketch

- Edit `src/superclaude/agents/rf-qa.md` near lines 264-287 (task-integrity 20-item checklist) to add the 6 new items, each citing source check from sc:tasklist for traceability.
- Edit `src/superclaude/skills/task-builder/SKILL.md` near SKILL.md:898-906 (A.10 9-item) to mirror the additions in the skill-side checklist (9-item → 13-item).
- Edit `src/superclaude/skills/task-builder/SKILL.md` near SKILL.md:1491-1507 (15-item validation checklist) to add the same 6 checks (15-item → 19-item).
- Update the "Comparison to sc:tasklist's 17" note in Bucket C digest with the per-check mapping table once integration is complete.
