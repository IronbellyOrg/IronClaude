---
proposal_id: PR-02
case: D
source_mechanism: src/superclaude/skills/sc-tasklist-protocol/SKILL.md Stages 9-10 (post-FINAL-REPORT §7-R4 design) — monotonicity guard + regression detection + full-set re-validation requirement for the patch loop
target_integration_point: src/superclaude/skills/task-builder/SKILL.md:870, 1550 (independent retry counters) and src/superclaude/agents/rf-task-builder.md:336-359 (per-gate fix-cycle limits 5/3/2/3/3); src/superclaude/agents/rf-qa.md:310-313 (3-fix-cycle then HALT)
final_report_citation: FINAL-REPORT §7-R4 (Dual-Mode Patch Recovery); §6.2 F2 (subset-only re-validation oscillation defect: "Successive cycles can oscillate"); §6.3 (adapt intent, not implementation)
direction_inversion_basis: |
  FINAL-REPORT §6.2 F2 documented oscillation in sc:tasklist's patch loop because Stage 9's `sc:task-unified` is non-deterministic and the subset-only re-validation hid regressions.
  Inverting to task-builder is asymmetric: task-builder ALREADY has multi-cycle retries (rf-qa 3, rf-task-builder per-gate 2-3, RESEARCH_NEEDED 2, MALFORMED 2 — Bucket C SKILL.md:651/859/865/870; rf-task-builder.md:336-359) and the existing 4-stage gate runs full checklists each cycle. So the IMPORT here is NOT a new loop — it is two stop conditions (monotonicity + regression detection) that prevent the same oscillation §6.2 F2 found.
  §6.3 risk of over-engineering: LOW because we add stop-conditions, not new pipeline stages or new fix loops.
conflict_with_task_builder: yes
invariant_protected: zero-trust QA
complexity_estimate: ~25 lines-of-change
expected_quality_gain: medium-high — removes oscillation risk (§6.2 F2 documented as "21 retry files across 18 batches" empirical pattern) without adding a new loop
---

## Mechanism in /sc:tasklist

FINAL-REPORT §7-R4 specifies for sc:tasklist's automated mode: **one retry cycle** with (a) **full-set re-validation** (not subset-only), (b) **monotonicity guard** — halt if |UNRESOLVED| doesn't strictly shrink between cycles, (c) **regression detection** — halt if a previously-RESOLVED item becomes UNRESOLVED. Cap at 2 total passes. FINAL-REPORT §6.2 F2 documented why subset-only re-validation has an oscillation defect: "Patching item A can regress previously-RESOLVED item B. Because only the UNRESOLVED subset is re-checked, this regression goes undetected. Successive cycles can oscillate (fix A breaks B, fix B breaks A)." The empirical pattern was 21 retry files across 18 batches in the RF llm-workflows repository.

## Proposed adaptation in task-builder

Add monotonicity-guard and regression-detection rules to the existing retry budgets in task-builder. The TARGET surfaces are:
- `src/superclaude/skills/task-builder/SKILL.md:651` (research-gate gap-fill max 3 rounds)
- `src/superclaude/skills/task-builder/SKILL.md:859, 865, 870` (RESEARCH_NEEDED max 2, MALFORMED max 2, separate counters)
- `src/superclaude/agents/rf-task-builder.md:336-359` (per-gate fix-cycle limits)
- `src/superclaude/agents/rf-qa.md:310-313` (3-fix-cycle hard cap)

For each retry loop, add two stop conditions BEFORE the existing iteration cap fires:
1. **Monotonicity guard:** record the gate-failure count `F_n` at end of cycle `n`. If `F_{n+1} >= F_n` (i.e., the count of remaining gate failures did not strictly shrink), HALT and escalate. Surface "non-convergent" in the gate report.
2. **Regression detection:** record the set of PASS items at end of each cycle. If any item that PASSed at cycle `n` FAILs at cycle `n+1`, HALT immediately. Surface "regression detected — item X passed then failed".

Full-set re-validation is ALREADY the task-builder norm — Bucket C SKILL.md:898-906 (task-integrity 9-item) and SKILL.md:1491-1507 (15-item validation) run on the entire task file each cycle. So §7-R4's "full-set" requirement is met by existing behavior; this proposal need only add the two stop conditions.

## Why this is NOT a 1:1 port

§6.3's lesson is that direct porting of correction-loop mechanisms across paradigms over-engineers. The inverse direction has a complementary risk: introducing too much stop-condition logic could prematurely halt agent-team workflows that legitimately need a few cycles. Mitigation: monotonicity guard only fires when count does NOT shrink (not when shrinking slowly); regression detection only fires on items that previously PASSED (not on legitimate refinements). These are conservative thresholds that preserve task-builder's existing tolerance for multi-cycle correction.

## Invariant analysis

- **zero-trust QA (PROTECTED, central):** strengthened. The guards prevent the QA gate from accepting a state where adversarial review oscillates. This makes the zero-trust stance stricter, not looser.
- **self-contained-item (untouched):** item schema unchanged.
- **evidence-bound-item (untouched):** evidence citations unchanged.
- **persistent .dev/tasks/ artifact (untouched):** gate logs in `qa/*.md` continue to persist; new logs capture monotonicity/regression events as additional evidence.
- **parallel research (untouched):** retry budgets are sequential by design; this proposal only adds stop conditions.

## Failure modes the proposal must handle

1. **Single-cycle case.** If the first cycle PASSes, no second cycle runs; guards are no-ops. Verified.
2. **Legitimate slow convergence.** If `F_n` strictly shrinks each cycle, monotonicity guard does NOT fire — the cycle continues to the existing cap. The guard only catches oscillation/stagnation.
3. **Race between guards.** If both monotonicity and regression conditions trigger in the same cycle, regression takes precedence (escalation message specifies which item regressed).
4. **Counter overflow in independent counters.** Each retry counter (RESEARCH_NEEDED, MALFORMED, research-gate, per-gate) keeps its own monotonicity-history. They are NOT collapsed — preserves Bucket C SKILL.md:870, 1550 "Counters tracked independently".

## Concrete change sketch

- Add a "Retry Monotonicity Protocol" subsection to `src/superclaude/skills/task-builder/SKILL.md` near SKILL.md:870 documenting the two stop conditions and their precedence.
- Edit `src/superclaude/agents/rf-task-builder.md` (~lines 336-359) to add: "Before re-spawning a fix cycle, compare |gate_failures| to the previous cycle's count. HALT if it did not strictly shrink. Before accepting a fix cycle output, compare the PASS set to the previous cycle's PASS set. HALT if any previously-PASS item is now FAIL."
- Edit `src/superclaude/agents/rf-qa.md` (~lines 310-313) to add the same protocol to its 3-fix-cycle.
- Update rule #7 (mandatory QA gates) in SKILL.md:1540 to reference the new protocol so it is treated as part of zero-trust QA.
