---
proposal_id: PR-03
case: B
source_mechanism: src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1150 (current "retry once before reporting error") extended per FINAL-REPORT §7-R1 with DNSP — synthesize HIGH-severity finding flagging affected task range, proceed with N-1 agents
target_integration_point: src/superclaude/skills/task-builder/SKILL.md:574-654 (A.8 research gate spawning rf-analyst + rf-qa in parallel) and SKILL.md:872-916 (A.10 task integrity spawning rf-qa); src/superclaude/agents/rf-analyst.md:42-69 (partition protocol) and src/superclaude/agents/rf-qa.md:50-77 (partition protocol)
final_report_citation: FINAL-REPORT §7-R1 (DNSP for Validation Agents); §6.1 Aggregate Results (P3 39/50 — the only ADOPT proposal across all 5)
direction_inversion_basis: |
  FINAL-REPORT §6.1 shows P3 (DNSP) was the SINGLE proposal across 5 RF→SC ports that did NOT require revision (39/50 Proposed = 39/50 Winner — Proposed wins).
  This is the strongest evidence that DNSP is paradigm-neutral: it addresses "system fails loudly when components break" which both deterministic and adversarial paradigms benefit from. §6.3's over-engineering risk does NOT apply because DNSP adds a stop condition (synthetic finding emission) rather than a new behavior class.
  Asymmetry: in sc:tasklist, partition agents are anonymous Task-tool agents over phase slices. In task-builder, partition agents are named rf-analyst / rf-qa instances over research-file slices (Bucket D rf-analyst.md:42-58, rf-qa.md:50-77 — "assigned_files" partitioning).
  The DNSP pattern transplants cleanly: same failure (one partition agent dies) and same right answer (synthesize a HIGH finding citing the un-covered range, surface gap visibly, proceed with remaining agents).
conflict_with_task_builder: no
invariant_protected: n/a-for-case-B-or-C
complexity_estimate: ~20 lines-of-change
expected_quality_gain: high — currently a partition-agent failure silently weakens the QA gate or aborts it; DNSP turns the failure into an explicit, citable evidence item
---

## Mechanism in /sc:tasklist

sc:tasklist's Stage 7 (Bucket A SKILL.md:1091-1106) spawns 2N parallel Task-tool agents. Failure handling at SKILL.md:1150 is "retry once before reporting error." FINAL-REPORT §7-R1 proposes: after the single retry fails, **synthesize a conservative HIGH-severity finding** with `source: "synthetic-dnsp"` metadata flagging the affected task range for manual review. The orchestrator merge step then **proceeds with 2N-1 agent findings**. Add an all-agents-fail guard (if zero agents succeeded, raise StageError as today). This was the highest-scoring of FINAL-REPORT's 5 proposals — Proposed variant won at 39/50 with no revision (Bucket E confirms).

## Proposed adaptation in task-builder

task-builder's A.8 research gate (SKILL.md:574-654) spawns `rf-analyst` and `rf-qa` in parallel; both support partitioning via `assigned_files` when there are >6 research files (Bucket D rf-analyst.md:42-58, rf-qa.md:50-77). Currently neither agent has explicit synthetic-finding behavior on partition failure — Bucket D §"Surfaces relevant" calls out rf-analyst as the natural host. Similarly, A.10 task integrity (SKILL.md:872-916) and A.10.5 qualitative (SKILL.md:923-1000) spawn rf-qa / rf-qa-qualitative.

Add to the orchestrator's behavior when collecting partition-agent results:
1. **After retry failure on any partition agent:** emit a synthetic finding with:
   - `severity: HIGH`
   - `source: "synthetic-dnsp"`
   - `affected_range`: the agent's `assigned_files` slice
   - `evidence`: path to the failed agent's spawn log (or stub if logging unavailable)
   - `recommendation: "Manual review required — partition agent failed twice"`
2. **Merge with remaining N-1 partition agents' findings** rather than aborting the gate.
3. **All-agents-fail guard:** if zero partition agents succeeded, escalate normally (existing behavior — Bucket C SKILL.md:651, 859, 865 retry-then-Open-Questions flow).

## Why this is NOT a 1:1 port

The mechanism is closely identical to FINAL-REPORT §7-R1 — DNSP is paradigm-neutral. The only adaptations are:
- Failure type: sc:tasklist's Task-tool agents fail via API/timeout; task-builder's rf-analyst/rf-qa fail via the agent's escalation ladder (Bucket D rf-task-researcher.md:378-384 WebSearch → /rf:opinion → team-lead). DNSP fires after the entire escalation ladder exhausts within partition scope.
- Range coordinate system: sc:tasklist uses phase-task ranges (T<PP>.<TT>); task-builder uses research-file paths (`research/[NN]-[topic].md` slices).
- Reporting venue: sc:tasklist surfaces via ValidationReport.md; task-builder surfaces via `qa/qa-research-gate.md` or `qa/qa-task-validation.md` (Bucket C SKILL.md:120-129).

## Invariant analysis

- **zero-trust QA (REINFORCED):** the synthetic finding is the strongest possible form of zero-trust — when verification cannot be performed, surface a HIGH-severity gap rather than silently passing or aborting. Bucket D rf-qa.md:140-142 already mandates "any gap regardless of severity = FAIL" — DNSP makes the gap visible.
- **evidence-bound-item (UPHELD):** the synthetic finding cites the failed partition's `assigned_files` range AND the spawn log — both are evidence references, not invented.
- **parallel research (UPHELD):** DNSP preserves parallel-research by allowing N-1 partitions to complete; sequential abort would defeat parallelism.
- **persistent .dev/tasks/ artifact (UPHELD):** synthetic findings are written into the persistent `qa/*.md` evidence trail like any other gate result.
- **self-contained-item (untouched):** no checklist-item schema impact.

## Failure modes the proposal must handle

1. **Cascading partition failures (all N fail).** All-agents-fail guard escalates to team-lead per Bucket D rf-team-lead.md:417 (3 fix cycles per phase). DNSP does NOT trigger.
2. **Spurious agent failure (rate-limit, transient).** The single retry per Bucket A SKILL.md:1150 catches transient failures. Only persistent failures result in DNSP.
3. **Synthetic finding masks a real issue.** Risk acknowledged in FINAL-REPORT K3. Mitigation: HIGH severity ensures the flag is never dismissed silently; rf-qa's existing "any gap = FAIL" rule (Bucket D rf-qa.md:140-142) means a synthetic finding can fail the gate.
4. **Synthetic finding from re-spawned gap-fill.** If task-builder's `RESEARCH_NEEDED` re-spawn (Bucket C SKILL.md:859, max 2) hits DNSP, the resulting synthetic finding should be deduplicated against any prior synthetic for the same range.

## Concrete change sketch

- Edit `src/superclaude/skills/task-builder/SKILL.md` near SKILL.md:651 (A.8 research-gate gap-fill section) to add a "DNSP Synthetic Finding Protocol" paragraph specifying the 3-bullet emission contract above.
- Edit `src/superclaude/agents/rf-analyst.md` (~lines 60-69, partition protocol) to instruct: "If a partition agent fails after retry, emit a `source: synthetic-dnsp` finding citing `assigned_files` and the failed spawn log. Continue with N-1 partitions." Add example finding to the agent's Output Format section.
- Edit `src/superclaude/agents/rf-qa.md` (~lines 70-77, partition protocol) symmetrically.
- Edit `src/superclaude/agents/rf-qa-qualitative.md` similarly if partitioning is enabled there (Bucket D rf-qa-qualitative.md:72-78).
- Add an item to rf-qa's Items Reviewed table format documenting `synthetic-dnsp` as a valid `source` value.
