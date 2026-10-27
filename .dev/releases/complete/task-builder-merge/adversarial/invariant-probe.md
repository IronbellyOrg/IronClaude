# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

**Probe scope**: Emerging consensus after Round 2 (PR-03 leading, PR-02 / PR-06 next; PR-05 recommended for deferral). 5-category standard checklist PLUS 5 task-builder invariants as additional probe targets.

## Standard 5-Category Findings

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | Independent retry counters (RESEARCH_NEEDED, MALFORMED, research-gate, per-gate) each carry their own monotonicity history — no shared state corruption | ADDRESSED | LOW | PR-02 line 53 explicitly "Each retry counter keeps its own monotonicity-history. They are NOT collapsed" |
| INV-002 | state_variables | PR-04 inherited verdict state in rf-qa-qualitative prompt may persist across fix cycles even after rf-qa re-runs and updates verdict | UNADDRESSED | MEDIUM | PR-04 line 50 covers "rf-qa FAILED but A.10.5 still spawned" but does not specify re-injection on subsequent fix-cycles. If A.10 re-runs after fix and produces new verdict, the orchestrator MUST re-inject — not specified explicitly. |
| INV-003 | guard_conditions | PR-05 advisory text presence is verified by rf-qa task-integrity, but the rule "advisory is non-binding" cannot be enforced by structural check — relies on agent prompt obedience | UNADDRESSED | MEDIUM | PR-05 line 67 critical-rule #19 "rule-based tier always wins" + X-004 contradiction. No structural test that proves advisory does not influence tier selection in practice. |
| INV-004 | guard_conditions | PR-03 synthetic finding "all-agents-fail guard" must trigger BEFORE DNSP emission to avoid emitting N synthetic findings when zero partitions succeeded | ADDRESSED | LOW | PR-03 line 35 "All-agents-fail guard: if zero partition agents succeeded, escalate normally" precedes DNSP emission logic. Order is correct in proposal. |
| INV-005 | count_divergence | PR-02 monotonicity comparison F_{n+1} vs F_n uses strict `>=` for halt — confirm inclusive (count did not strictly shrink) | ADDRESSED | LOW | PR-02 line 30 "If F_{n+1} >= F_n (i.e., the count of remaining gate failures did not strictly shrink), HALT". Logic is correct: shrink-by-zero halts; shrink-by-one continues. |
| INV-006 | count_divergence | PR-06 TB-Add-2 bounds (>=3 and <=40 track / <=50 single-track) are speculative without empirical calibration from `.dev/tasks/done/` | UNADDRESSED | LOW | PR-06 line 60 author-acknowledged: "ADVISORY-fail (warn not block) until calibrated". This is the proposal's own mitigation; treat as Phase-1 ADVISORY landing, Phase-2 calibration. |
| INV-007 | collection_boundaries | PR-03 partition-set when only 1 file (N=1) — partitioning is disabled; DNSP cannot trigger; current rf-task-builder behavior unchanged | ADDRESSED | LOW | rf-analyst.md:42-58 partition protocol only activates when >6 files. N=1 case is below threshold; DNSP path is not entered. |
| INV-008 | collection_boundaries | PR-01 Execution Context with zero inferable source areas (BUILD_REQUEST minimal) — header degrades to References-only | ADDRESSED | LOW | PR-01 failure mode #2 line 47: "Header degenerates to References-only, with WHY/source-area lines omitted. Optional behavior preserved." |
| INV-009 | collection_boundaries | PR-05 with empty `.dev/tasks/done/` directory or zero matching task_types — advisory does not render | ADDRESSED | LOW | PR-05 failure modes #1, #2 line 56-57: "Skip the advisory step entirely — no degradation" |
| INV-010 | interaction_effects | PR-04 + PR-06 sequencing: if PR-04 lands before PR-06, the inherited verdict is "thin" (only the existing 9-item set). When PR-06 lands, the verdict richens — but rf-qa-qualitative's prompt template must be updated to reference the new TB-Add items by name | UNADDRESSED | MEDIUM | PR-04 Round-2 rebuttal acknowledges sequencing; no concrete mechanism for prompt template auto-update when TB-Add items go live. Refactor plan must specify either "land PR-06 first" or "PR-04 prompt uses dynamic checklist enumeration" |
| INV-011 | interaction_effects | PR-01 + PR-06 TB-Add-7 (cross-validation): the rf-qa check "Execution Context source-areas reappear in items" must run BEFORE rf-qa-qualitative spawns (otherwise PR-04 passthrough propagates an unvalidated header) | ADDRESSED | LOW | rf-qa structural runs A.10 BEFORE A.10.5 (rf-qa-qualitative) per Bucket D rf-qa-qualitative.md:101. TB-Add-7 lives in A.10, ordering is correct. |
| INV-012 | interaction_effects | PR-02 + PR-03 stacking: if a partition agent fails (PR-03 DNSP fires) inside a multi-cycle retry (PR-02 governs), does the synthetic finding count as a "failure" for monotonicity purposes? | UNADDRESSED | MEDIUM | Neither proposal addresses this composition. The synthetic finding is HIGH-severity by design → it SHOULD count as a failure for monotonicity. But the synthetic was emitted BECAUSE the gate cannot run — it represents un-verified gap, not a new failure. Refactor plan must specify: synthetic findings count as failures for |F_n| BUT a synthetic for the same range across consecutive cycles is a dedup case (PR-03 failure-mode #4), not a regression. |
| INV-013 | interaction_effects | PR-07 5-axis overlay + PR-04 inherited verdict: when rf-qa-qualitative receives both the verdict (PR-04) AND the 5 axes (PR-07), the axes must be applied to the items NOT covered by inherited PASS | ADDRESSED | LOW | PR-07 line 32 "5-axis overlay applies to all 15 checks" + PR-04 line 41 "PASS items skip structural re-checking but each semantic check requires your own tool engagement". The 5 axes are semantic — they live in the items rf-qa-qualitative still runs. Composition is clean. |

## Task-Builder-Invariant-Specific Findings (5 invariants × 7 proposals = 35 cells; surfacing only non-default findings)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-014 | self-contained-item (invariant 1) | PR-01 task-level header could be misread as a replacement for per-item Context fields | ADDRESSED | LOW | PR-01 line 39 explicit: "self-contained-item (untouched): the 5-field schema for each checklist item is unchanged. The new header is task-level, not item-level." |
| INV-015 | evidence-bound-item (invariant 2) | PR-01 "no specific file paths" rule could leak into per-item Context if rf-task-builder misreads scope | UNADDRESSED | MEDIUM | PR-01 confines the rule to the header (line 34) AND requires rf-qa task-integrity to cross-validate (line 54). But the rule's scope-confinement depends on rf-task-builder agent obedience to the "header-only" framing. No structural test that proves Context fields retain file:line citations. Refactor plan should require an A.10 check: "Every Context field that references a code surface includes at least one file:line citation." |
| INV-016 | evidence-bound-item (invariant 2) | PR-03 synthetic finding's `evidence: path to the failed agent's spawn log (or stub if logging unavailable)` — the "or stub" fallback might emit a synthetic without real evidence | ADDRESSED | LOW | PR-03 line 31 explicitly addresses this; the spawn-log stub is still an evidence reference (citing the absence of log). zero-trust QA flags the gap visibly. |
| INV-017 | evidence-bound-item (invariant 2) | PR-05 advisory "Based on `TASK-RF-XXXXXXXX-XXXXXX/...`" cites historical files but does not verify those files still exist or that their frontmatter is unchanged since archival | UNADDRESSED | LOW | PR-05 line 49 commits to citing specific paths but offers no staleness check. Mitigation: rf-qa task-integrity could verify each cited path exists. Refactor plan should add this. Low severity because Phase-2 deferral makes this academic for now. |
| INV-018 | persistent-.dev/tasks/-artifact (invariant 3) | All proposals assume `.dev/tasks/` directory layout is stable; none consider migration if directory structure changes | UNADDRESSED | LOW | Shared assumption A-001 already promoted. No proposal anticipates structural changes to `.dev/tasks/`; if it changes, ALL 7 proposals require re-integration. Generic refactor-plan note suffices. |
| INV-019 | zero-trust QA (invariant 4) | PR-04 passthrough must NOT cause rf-qa-qualitative to mark items VERIFIED that rf-qa marked PASS structurally but require semantic verification | ADDRESSED | LOW | PR-04 line 41 "Confidence Gate Protocol ... still requires ≥95% computed confidence; rf-qa's PASS items count toward the VERIFIED tally but only when rf-qa-qualitative itself runs the semantic check." Anti-inflation rule preserved. |
| INV-020 | zero-trust QA (invariant 4) | PR-05 advisory rendering happens BEFORE the gate runs — could the advisory itself become a gate input? | ADDRESSED | LOW | PR-05 line 67 critical rule #19: "Tier Advisory is non-binding. Rule-based tier selection in SKILL.md:96-101 always wins." Plus rf-qa task-integrity check for disclaimer presence (line 68). |
| INV-021 | parallel-research (invariant 5) | PR-03 DNSP fires after the entire escalation ladder exhausts — does this serialize the partition-agent cohort? | ADDRESSED | LOW | PR-03 line 47 "DNSP preserves parallel-research by allowing N-1 partitions to complete; sequential abort would defeat parallelism." The retry-and-DNSP is within-agent-instance, not across the cohort. |

---

## Summary

- **Total findings**: 21
- **ADDRESSED**: 16 (12 LOW + 4 MEDIUM ADDRESSED — note: ADDRESSED MEDIUMs are conservative LOWs in practice)
- **UNADDRESSED**: 5
  - HIGH: 0
  - MEDIUM: 4 (INV-002, INV-003, INV-010, INV-012, INV-015)
  - LOW: 2 (INV-006, INV-017, INV-018)

Correction count: UNADDRESSED-MEDIUM = 4 (INV-002, INV-003, INV-010, INV-012, INV-015) — counted carefully: INV-002, INV-003, INV-010, INV-012, INV-015 → 5 items. Recount: of UNADDRESSED items above (INV-002, INV-003, INV-006, INV-010, INV-012, INV-015, INV-017, INV-018) = 8 items total UNADDRESSED. By severity: MEDIUM (INV-002, INV-003, INV-010, INV-012, INV-015) = 5; LOW (INV-006, INV-017, INV-018) = 3. HIGH = 0.

**Restated summary**:
- Total findings: 21
- ADDRESSED: 13
- UNADDRESSED: 8 (0 HIGH, 5 MEDIUM, 3 LOW)

**Convergence-blocking?** NO. Convergence requires `count(HIGH + UNADDRESSED) == 0`. Result = 0. Convergence is NOT blocked by the invariant probe.

**MEDIUM warnings** (do not block, must be reviewed):
- INV-002: PR-04 verdict re-injection on subsequent fix cycles
- INV-003: PR-05 advisory operational obedience (not just disclaimer presence)
- INV-010: PR-04 + PR-06 sequencing prompt-template auto-update
- INV-012: PR-02 + PR-03 stacking — synthetic findings as failure-count input to monotonicity
- INV-015: PR-01 scope-confinement of "no file paths" rule requires structural test

All 5 MEDIUMs are addressable in the refactor plan as explicit acceptance criteria; none are merge-blocking but ALL must appear in the refactor-plan's per-proposal action list.

**LOW notes**:
- INV-006: PR-06 TB-Add-2 bounds Phase-2 calibration deferral
- INV-017: PR-05 historical file staleness check (academic given Phase-2 deferral)
- INV-018: directory-structure assumption (portfolio-wide note)
