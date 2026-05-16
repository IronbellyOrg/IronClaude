---
proposal_id: PR-05
case: D
source_mechanism: src/superclaude/skills/sc-tasklist-protocol/SKILL.md feedback-log.md design per FINAL-REPORT §7-R5 — read prior feedback-log.md, render `## Tier Calibration Advisory` section, advisory-only (scored tiers unmodified)
target_integration_point: src/superclaude/skills/task-builder/SKILL.md:88-101 (current tier selection: Quick/Standard/Deep rule-based — Bucket C SKILL.md:90-94 file/researcher count, SKILL.md:96-101 selection rules); add a pre-A.0 read of prior `.dev/tasks/done/TASK-RF-*/TASK-RF-*.md` for tier patterns
final_report_citation: FINAL-REPORT §7-R5 (Tier Calibration Advisory); §6.2 F4 (hidden-input framing — "advisory-only resolves the determinism violation")
direction_inversion_basis: |
  FINAL-REPORT §6.2 F4 is the most subtle finding: in sc:tasklist, an unknown feedback-log.md would create a "hidden input" that breaks the determinism guarantee. The resolution was "advisory-only — all scored tiers computed from roadmap text alone."
  Inverting to task-builder: task-builder has NO determinism guarantee (Bucket C §"Determinism status" — "No explicit determinism claim"). So the hidden-input risk does NOT materialise the same way. But the OPPOSITE risk exists: task-builder is so agent-exploratory that adding any historical pattern could OVER-influence the tier rule selection, eroding the rule-based selection at SKILL.md:96-101.
  Mitigation parallel to §6.2 F4: keep the advisory STRICTLY non-binding. The tier still comes from SKILL.md:96-101 rules; the advisory only surfaces "prior similar tasks chose Standard; current rule chose Deep — verify intent."
  Asymmetry: in sc:tasklist the risk was that feedback would change scoring; in task-builder the risk is that pattern-matching against history would short-circuit the existing rule-based selection. Both mitigated by advisory-only framing.
  §6.3 over-engineering risk: HIGHEST of the 7 proposals because task-builder has no existing feedback infrastructure. Marking as Phase-2 / future work, not Phase-1 quick-win.
conflict_with_task_builder: yes
invariant_protected: evidence-bound-item
complexity_estimate: ~30 lines-of-change
expected_quality_gain: medium — improves cross-task tier consistency once `.dev/tasks/done/` accumulates volume; LOW value until 10+ completed tasks exist
---

## Mechanism in /sc:tasklist

FINAL-REPORT §7-R5 specifies: if `feedback-log.md` exists in `TASKLIST_ROOT`, parse override rows (min 2 matching entries for a pattern to surface), produce a `## Tier Calibration Advisory` section in `tasklist-index.md`. **Advisory only — all scored tiers remain roadmap-only.** STRICT downgrade warnings if feedback suggests easier-than-rule tiers. The Feedback Collection Template exists in the index (Bucket A SKILL.md:743-761; templates/index-template.md:108-114) but the generator currently never reads it.

§6.2 F4 motivates the advisory-only constraint: "Adding feedback-log.md as a second input that modifies tier scores means different feedback files produce different tiers for the same roadmap. This is a 'hidden input' problem."

## Proposed adaptation in task-builder

task-builder's tier selection is rule-based (Bucket C SKILL.md:90-101): Quick (3 researchers, <5 files), Standard (4-5 researchers, 5-15 files), Deep (6-8 researchers, multi-track or "thorough/comprehensive/deep dive"). There is no feedback log; there is no existing pattern reading.

This proposal adds an **optional pre-A.0 advisory step**:
1. **Scan** `.dev/tasks/done/TASK-RF-*/TASK-RF-*.md` frontmatter for `tier` and `task_type` fields (Bucket C SKILL.md:1410-1429 lists tags including `task_type`).
2. **Match** the current GOAL/BUILD_REQUEST's `task_type` (or inferred type when absent) against historical tasks. Threshold: min 2 historical tasks of matching type for a pattern to surface.
3. **Render** an `## Tier Selection Advisory` block in the generated task file's header (NOT in the frontmatter) listing:
   - The rule-based tier the current selection logic chose
   - Historical pattern: "Of 4 prior `type=feature` tasks, 3 used Standard, 1 used Deep"
   - Recommendation: explicit "Advisory only. Tier remains the rule-based selection above."
4. **No tier modification.** The actual `tier` field in frontmatter and the rf-team-lead spawn decision both use SKILL.md:96-101 rules unchanged.

## Why this is NOT a 1:1 port

sc:tasklist's R5 reads a curated feedback-log.md authored explicitly for calibration purposes. task-builder's analog reads completed task files themselves — there is no curated source. This brings TWO adaptations:
1. **Match threshold is type-based, not exact-match-based.** sc:tasklist's R5 looked for prior runs with the same TIER OVERRIDE on the same roadmap-item-text; we look for prior runs of the same task_type.
2. **The "STRICT downgrade warning" form** has no analog because task-builder's tiers control research depth (not artifact compliance). The warning shape is "current tier=Quick but 3/3 similar tasks needed Standard — verify scope."

FINAL-REPORT §6.3 lesson aggressively applied: do NOT replicate the feedback-log.md file schema; instead, READ existing persisted artifacts. Avoid the over-engineering of building a new feedback-log infrastructure when `.dev/tasks/done/` already has the data structure.

## Invariant analysis

- **evidence-bound-item (PROTECTED, central):** the advisory MUST cite the specific historical task files it references (e.g., "Based on `TASK-RF-20250304-091000/TASK-RF-20250304-091000.md` and `TASK-RF-20250408-143000/TASK-RF-20250408-143000.md`"). This makes the advisory itself evidence-bound. Failing to cite is a rule violation.
- **persistent .dev/tasks/ artifact (UPHELD AND EXTENDED):** the proposal READS but never modifies historical task files. The persistence invariant is reinforced because completed tasks gain a second consumer (advisory generation).
- **zero-trust QA (untouched):** advisory does not affect any gate. rf-qa task-integrity (Bucket C SKILL.md:898-906) should add a check confirming the advisory cites valid file paths if present.
- **self-contained-item (untouched):** item schema unchanged.
- **parallel research (untouched):** advisory is pre-A.0; no parallelism impact.

## Failure modes the proposal must handle

1. **No `.dev/tasks/done/` directory or empty.** Skip the advisory step entirely — no degradation.
2. **Fewer than 2 matching historical tasks.** Skip pattern surfacing; per the min-2 threshold from §7-R5.
3. **Advisory drifts from rule-based selection.** rf-task-builder MUST still apply SKILL.md:96-101 rules. The advisory is documentation, never input to the tier decision.
4. **Hidden-input regression.** Mitigation: the rendered advisory section explicitly states "Advisory only. Tier remains the rule-based selection above." rf-qa task-integrity should verify this disclaimer is present when the advisory section exists.
5. **Privacy / leak risk.** Historical tasks may reference internal modules. Mitigate by reading only the frontmatter (`tier`, `task_type`, `tags`) — NOT task body content.
6. **Over-engineering risk (HIGHEST among PR-01–07).** Until `.dev/tasks/done/` has ≥10 completed tasks of varied types, the advisory will rarely fire. Document this explicitly — this proposal has LOW immediate value and high latent value.

## Concrete change sketch

- Add a new "Tier Selection Advisory (optional)" subsection to `src/superclaude/skills/task-builder/SKILL.md` just before A.0 (current tier selection at SKILL.md:88-101).
- The instruction body specifies: read `.dev/tasks/done/TASK-RF-*/TASK-RF-*.md` (frontmatter only); group by `task_type`; require ≥2 historical entries; render the advisory block in the task file header AFTER frontmatter and (if present) AFTER PR-01's Execution Context block.
- Add a new Critical Rule (#19 if extending the list) — "Tier Advisory is non-binding. Rule-based tier selection in SKILL.md:96-101 always wins."
- Add a rf-qa task-integrity check (Bucket C SKILL.md:898-906): "(N+1) If Tier Selection Advisory section exists: cites valid historical file paths AND contains the 'Advisory only' disclaimer."
- No new template files — instruction lives in SKILL.md only.
