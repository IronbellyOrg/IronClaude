---
proposal_id: PR-04
case: B
source_mechanism: src/superclaude/skills/sc-tasklist-protocol/SKILL.md Stage 6 → Stage 7 prompt injection per FINAL-REPORT §7-R3 — emit gate-results.txt, inject into Stage 7 agent prompt ("All PASS items are machine-verified — do not re-check")
target_integration_point: src/superclaude/skills/task-builder/SKILL.md:923-1000 (A.10.5 qualitative gate spawning rf-qa-qualitative) — propagate rf-qa's structural verdict JSON into rf-qa-qualitative's prompt context
final_report_citation: FINAL-REPORT §7-R3 (Quality Gate Evidence Passthrough); §6.2 F3 ("the quality gate already catches what the evidence extraction would catch")
direction_inversion_basis: |
  FINAL-REPORT §6.2 F3 was the Correctness debate's strongest finding for P4 — sc:tasklist's 17-point gate already catches the structural facts a parallel evidence extraction would surface, so the right move is to PIPE the gate's results to validation agents rather than build a second extraction pipeline.
  Inverting: task-builder's rf-qa-qualitative agent has an EXPLICIT existing rule "do not re-verify what rf-qa already checks (section numbering / file existence)" (Bucket D rf-qa-qualitative.md:794). That rule is currently RHETORICAL — there is no mechanism delivering the rf-qa verdict to rf-qa-qualitative's prompt. This proposal operationalises an existing rule.
  Asymmetry: this is the lowest-risk port because we are making explicit a rule that the agent description already commits to, but the orchestration currently has no way to deliver. §6.3 risk of over-engineering does not apply — we are aligning behavior with documented intent.
conflict_with_task_builder: no
invariant_protected: n/a-for-case-B-or-C
complexity_estimate: ~15 lines-of-change
expected_quality_gain: medium — token savings on rf-qa-qualitative + sharper semantic focus; eliminates the gap between rf-qa-qualitative.md:794 stated intent and orchestrator behavior
---

## Mechanism in /sc:tasklist

FINAL-REPORT §7-R3 specifies for sc:tasklist:
- **Stage 6 emits** `TASKLIST_ROOT/validation/gate-results.txt` — a plain-text summary of all 17 check results (PASS/FAIL per check).
- **Stage 7 agent prompts receive** the gate-results as injected context with an explicit instruction: "All PASS items are machine-verified — do not re-check. All FAIL items are machine-verified defects — flag as HIGH. Focus on semantic quality."
- Token savings come from agents skipping mechanical re-verification of structural facts; semantic-quality focus is sharper.

The motivating finding (§6.2 F3): "If the gate passes (which it must — write atomicity requires it), the evidence JSON's `orphan_deliverables` and `missing_roadmap_items` fields would be empty. The extraction is redundant with the gate."

## Proposed adaptation in task-builder

task-builder's pipeline runs A.10 task-integrity (rf-qa structural, 9-item checklist — Bucket C SKILL.md:898-906) BEFORE A.10.5 qualitative (rf-qa-qualitative, 15-item — SKILL.md:961). Currently the orchestrator spawns rf-qa-qualitative WITHOUT delivering rf-qa's verdict (Bucket D rf-qa-qualitative.md:101, 246, 314 — "spawned by orchestrator after rf-qa structural passes"). The agent description states the principle (rf-qa-qualitative.md:794) but there is no mechanism.

Add to A.10.5 orchestration in `src/superclaude/skills/task-builder/SKILL.md:923-1000`:
1. **Capture rf-qa verdict.** rf-qa already emits a structured Items Reviewed table with PASS/FAIL per item (Bucket D rf-qa.md:317-355). Read `qa/qa-task-validation.md` after rf-qa completes A.10.
2. **Inject into rf-qa-qualitative spawn prompt.** When spawning rf-qa-qualitative for A.10.5, include a `## Inherited Structural Verdict` section in the spawn prompt containing rf-qa's table verbatim plus the instruction: "Items marked PASS by rf-qa are machine-verified. Do not re-verify section numbering, frontmatter shape, or item structure. Focus on semantic quality (scope, audience, logical flow, contradictions, evidence sufficiency)."
3. **Surface in rf-qa-qualitative's output.** rf-qa-qualitative's Self-Audit section (Bucket D rf-qa-qualitative.md:675-714) must record which rf-qa PASS items it relied on; preserves the audit trail.

## Why this is NOT a 1:1 port

In sc:tasklist, the gate result is structural-only and the receiving agents are anonymous; the prompt instruction is the entire delivery mechanism. In task-builder, the receiving agent (rf-qa-qualitative) ALREADY has a stronger stance — `rf-qa-qualitative.md:794` explicitly says it MUST NOT re-verify what rf-qa checks. The adaptation makes that stance operational. FINAL-REPORT §6.3 risk of over-engineering is reversed here: we are doing LESS work than a 1:1 port because the receiving agent's policy is pre-aligned.

## Invariant analysis

- **zero-trust QA (REINFORCED):** the passthrough is read-only — rf-qa-qualitative still runs the full 15-item adversarial review on semantic content. PASS items from rf-qa are NOT skipped; only the duplicated structural re-checking is avoided. The Confidence Gate Protocol (Bucket D rf-qa-qualitative.md:734-779) still requires ≥95% computed confidence; rf-qa's PASS items count toward the VERIFIED tally but only when rf-qa-qualitative itself runs the semantic check.
- **evidence-bound-item (UPHELD):** the rf-qa verdict is itself evidence (lives in `qa/qa-task-validation.md`); the passthrough is evidence citation.
- **persistent .dev/tasks/ artifact (UPHELD):** rf-qa verdict file persists per Bucket C SKILL.md:1536; nothing is deleted.
- **parallel research (untouched):** A.10 and A.10.5 are sequential by design (Bucket D rf-qa-qualitative.md:101 — qualitative spawned AFTER structural). No parallelism is disturbed.
- **self-contained-item (untouched):** item schema unchanged.

## Failure modes the proposal must handle

1. **rf-qa verdict file missing or malformed.** Fall back to current behavior (rf-qa-qualitative does its own structural checks too). The passthrough is an optimization, not a dependency.
2. **rf-qa-qualitative inflates confidence by relying on rf-qa.** Mitigation: Bucket D rf-qa-qualitative.md:766-775 already bans "reliance ≠ verification" and "never mark VERIFIED from another report." Strengthen the passthrough prompt with this rule explicitly: "rf-qa PASS items skip structural re-checking but each semantic check requires your own tool engagement."
3. **rf-qa FAILED but A.10.5 still spawned.** Current orchestration spawns A.10.5 only after A.10 passes (Bucket D rf-qa-qualitative.md:101). If a fix cycle moved to A.10.5 prematurely, the passthrough would propagate a FAIL — handled correctly because rf-qa-qualitative's instruction includes "All FAIL items are machine-verified defects — flag as HIGH."
4. **Confidence Gate inflation.** Tool Engagement Minimum (Bucket D rf-qa.md:414-416) requires Read+Grep+Glob count ≥ checklist items. This is unchanged — rf-qa-qualitative must still hit its minimum on its own 15-item checklist.

## Concrete change sketch

- Edit `src/superclaude/skills/task-builder/SKILL.md` near SKILL.md:923-1000 (A.10.5 spawn description) to add the 3-step passthrough protocol above.
- Add a Critical Rule (or extend rule #7 at SKILL.md:1540) requiring rf-qa-qualitative's spawn prompt to include the Inherited Structural Verdict section when rf-qa output is available.
- Edit `src/superclaude/agents/rf-qa-qualitative.md` near the existing rule at line 794 to reference the new passthrough mechanism: change "do not re-verify what rf-qa already checks" to "do not re-verify what rf-qa already checks (verdict provided via Inherited Structural Verdict in spawn prompt)."
- Add an Items Reviewed format note in rf-qa-qualitative's output template requiring it to list which Inherited PASS items it relied on (audit trail).
