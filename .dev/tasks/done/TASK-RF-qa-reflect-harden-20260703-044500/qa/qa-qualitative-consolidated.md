# QA Qualitative — Consolidated Report (A.10.5)

**Topic:** TASK-RF-qa-reflect-harden-20260703-044500 (FX1/FX2/FX3/FX5/FX7 additive hardening)
**Date:** 2026-07-03
**Phase:** task-qualitative (A.10.5 SERIALIZED FIX AGENT)
**fix_authorization:** true (fixes applied in-place to the task file)

This report consolidates the A.10.5 serialized-fix pass. It reads the two upstream
report-only lens reports (`qa-qualitative-operational-report.md` CRITICAL-1;
`qa-qualitative-sufficiency-report.md` IMPORTANT + MINOR) and applies every fix
to the task file `TASK-RF-qa-reflect-harden-20260703-044500.md`.

## A.10.5 Qualitative Fixes

Fixes are appended incrementally below as each is applied (no one-shot).

### MINOR (sufficiency AX-2) — phase token — FIXED

All 9 `rf-qa-qualitative` spawn items now pass `QA_PHASE: task-qualitative`
(was `task-integrity` in Gates A/B/C, `report-validation` in the final gate PC.4).
The 9 `rf-qa` (structural) spawns are UNCHANGED (`task-integrity` / `report-validation`
are valid rf-qa phases). Verified via grep: 0 rf-qa-qualitative spawns carry a
structural token; all 9 structural spawns retain their tokens. The gate-TYPE labels
in the section headers (`task-integrity gate`, `report-validation`) are preserved.

### MINOR-2 (operational) — FX5 drift-alarm regex — FIXED

Step 2.7a's drift-alarm now specifies the CONCRETE, LITERAL matcher
`re.compile(r"_(path|paths)_resolv|_resolve_|_findings_|_observed_|_selected_|_stale_|_shape_observed|_review_completeness")`
(from research/02 §4.1 step 4), restricted to MODULE-LEVEL `ast.FunctionDef` nodes,
with the exclusion set spelled out: the entire `_*_checks` builder family,
`ValidationReport.passed`, and the `CandidateContract.required_unobserved` dataclass
method are DELIBERATELY NOT auto-matched (hand-registered instead). The matched set
is asserted to EQUAL the ~9 module-level defs the enforced registry covers, making
Step 2.8 green-ness deterministic rather than executor-guessed.

### IMPORTANT (sufficiency AX-4) — FINAL gate agent-count scaling — FIXED

- The final-gate header no longer hard-pins 6 agents; it states the count SCALES with
  the PC.3-measured net-line delta per MDTM I19 (<500→6 / 500–1500→8 / 1500–3000→10 /
  >3000→12, as 3+3 / 4+4 / 5+5 / 6+6 splits), and flags the realistic 500–800-line
  estimate → likely the 8-agent (4+4) band.
- PC.3 now records `MEASURED_NET_LINES` and selects `FINAL_GATE_AGENT_COUNT` at the top
  of the change-set manifest, with a `HALT-RESCOPE` escape when the executor cannot
  spawn the scaled count.
- PC.4 gains a SCALING DIRECTIVE that reads `FINAL_GATE_AGENT_COUNT` and spawns the
  baseline 6 PLUS additional balanced structural/content lens agents to reach the
  selected count (or HALTs). PC.5 consolidation now globs ALL `qa-final-*.md` reports
  and asserts the count equals `FINAL_GATE_AGENT_COUNT` (not a fixed six).

### CRITICAL-1 (operational AX-2/AX-3) — FX7 must be additive + green; routing is a HALT — FIXED

**Root defect (from the operational report):** FX7 Step 3.2(c) UNCONDITIONALLY flipped
`ensemble.py:551` `verification_skip_reason` from the exempt `"tool-unavailable"` to a
non-exempt token. Because `build_reflect_contract` ALWAYS emits `verification_ran: False`
(verified: `ensemble.py:550-551`), this fired Trigger-12 for EVERY ensemble run →
DEGRADED/exit-11, breaking existing green tests (`test_ensemble_unit.py:342-363`
`test_r2f2` pins the exempt reason + its `_VERIFICATION_SKIP_EXEMPTIONS` membership;
`test_ensemble_stub_integration.py:160-171` `test_i1` pins clean PASS/exit-0),
self-contradicting Step 3.4b, and REVERSING the deliberate R2-F2 design. The blanket
Step 3.5 revert clause would then unwind FX7. Result: Phase 3 could not be green AND
additive simultaneously.

**Re-authored FX7 to the coherent additive design (grounded in live source + research/03
§2c/§3.4, which themselves emphasize "builder + NEW visibility fields, NOT repurposing"
and warn the skip-reason flip "would degrade globally"):**

- **Step 3.2** — REMOVED the unconditional skip-reason flip (old subitem (c)). FX7 now
  KEEPS only the truly-additive pieces: (a) the defaulted `reviewers_requested` kwarg +
  threading; (b) `degraded_components` population guarded on a GENUINE reviewer shortfall
  (`reviewers_requested is not None and reviewer_count < reviewers_requested`) so clean
  runs leave `degraded_components == []`; (c) the NEW `*_verified` visibility fields with
  the `reviewers_verified` None-guard (LOW-2). The clean-run `verification_skip_reason`
  MUST remain the exempt `"tool-unavailable"` (BYTE-UNCHANGED). The aggressive
  "force DEGRADED whenever `verification_ran` is False (incl. clean full-reviewer runs)"
  routing — which reverses R2-F2 and is non-additive — is written as a PENDING
  `needs_human_decision` marker `phase-outputs/plans/fx7-degrade-on-unverified-DECISION.md`
  (R2-F2 tension documented, cites `test_ensemble_unit.py:342-363` + driving-plan §3.4),
  NOT auto-applied. Step 3.2 lands the additive pieces and defers ONLY the routing flip
  (mirrors the human-decision-must-halt fail-safe: the disputed SHIP-A-CHANGE mutation is
  never auto-applied; the agreed additive pieces proceed).
- **Step 3.4b** — rewrote the unit tests to assert the ADDITIVE visibility fields +
  reviewer-shortfall degrade + the clean-run skip reason staying `"tool-unavailable"`
  (additive-safety witness); explicitly FORBIDS any test asserting a non-exempt clean-run
  skip reason. `test_r2f2` / `test_i1` need NO edit and MUST stay green.
- **Step 3.4c** — the verdict-mapping degraded-route test is now driven SOLELY by the
  reviewer-shortfall `degraded_components` trigger, NOT a skip-reason change.
- **Step 3.5** — scoped the revert clause: (1) fix new tests; (2) a `test_r2f2`/`test_i1`
  failure is the signature of the HALTED flip wrongly applied → REMOVE the flip / restore
  the exempt reason (NOT revert the additive fields); (3) revert an additive field ONLY if
  it itself breaks a consumer. NEVER blanket-revert every FX7 change.
- **Framing propagated** — Task Overview FX7 bullet, Key Objective 3, Key Constraints FX7
  block, Phase 3 preamble, Gate B lenses (additive-safety, degrade-mechanism-correctness,
  no-vacuous-pass-and-visibility, domain-accuracy, rf-analyst completeness), the Open
  Questions FX7 resolution note, the M4 fidelity DETAIL-PRESERVATION clause (PC.8), and the
  final-gate backstop lens (PC.4) were all rewritten to the additive design so no gate
  verifies against the removed mechanism.

**Re-verification:** the additive FX7 is green against ALL existing `tests/cli/reflect/`
tests (no clean-run routing change); the reviewer-shortfall case honestly degrades; the
aggressive degrade-on-unverified routing is HALTED as a PENDING human decision; PC.4
scales with PC.3's measurement; phase tokens correct; item count 78 (unchanged);
PC.11 reflect wrapper penultimate, PC.12 Done last; staleness overrides
(FX2 keep-15/AX-2/no-AX-6; FX1 advisory/no-5th-class; FX7 no-exemption-edit/no-status:degraded;
F1-F4 regression framing) all intact.

## Overall Verdict: PASS (all applied)

All four findings from the two upstream report-only lenses are remediated in-place in the
task file:
- CRITICAL-1 (FX7 additive + green, routing HALTED) — FIXED
- IMPORTANT (final-gate agent count scales with PC.3 per I19) — FIXED
- MINOR (rf-qa-qualitative QA_PHASE → task-qualitative on all 9 spawns) — FIXED
- MINOR-2 (FX5 drift-alarm concrete regex + exclusions) — FIXED

## QA Complete
