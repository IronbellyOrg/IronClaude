# Phase 4 — Consolidated QA Findings (M3 lens gate)

8 lens agents ran (3 structural + 3 content + 2 domain), all report-only. (3 of the
8 timed out on the first parallel batch — API timeouts, not findings — and were
re-spawned; all 8 reports are now on disk.)

| Lens | Report | Verdict |
|---|---|---|
| template-conformance | qa-structural-conformance-phase4.md | PASS |
| internal-consistency | qa-structural-consistency-phase4.md | PASS |
| evidence/anchor-freshness | qa-structural-evidence-phase4.md | PASS |
| actionability/test-correctness | qa-content-actionability-phase4.md | PASS (mutation-tested) |
| domain-accuracy | qa-content-domain-accuracy-phase4.md | PASS |
| crossref-chain | qa-content-crossref-phase4.md | PASS |
| INV-R3 fidelity | qa-domain-inv-fidelity-phase4.md | PASS (4 worked examples) |
| closed-enum count | qa-domain-closed-enum-phase4.md | PASS (37 + 6 end-to-end) |

## TOP-LINE VERDICT: PASS — no fixes required

All 8 lenses PASS. The actionability lens proved non-vacuity via 5 source mutations
(min→max FAILED, None-guard-drop → TypeError, member-removal → 36≠37, dedup-break →
True-is-False, fold-neuter → resume miss). INV-R3 traced [1,3]→1, [3,1]→1, []→None,
[2,2]→2. Counts: `len(EventType)==37`, `len(IDEMPOTENCY_SETS)==6` end-to-end.

## Non-blocking observations (no fix; documented)
- **O-1 (MINOR):** `decline-twice.json` carries `cycles`/`max_rounds`/`effective_max_rounds`
  keys that T-1124 does not all consume (only `auggie_review_invoked_count`). The fixture
  is partly aspirational; the test still verifies the core resume strict-once guarantee.
  Not a defect — left as-is (the fsm-level cycle replay is exercised in Phase 5 tests).
- **O-2 (INFO → Phase 5):** `EventType.DECLINE_DETECTED` has no `rebuild_state` fold — correct,
  it's a `SkillResult` runtime field (decline_detected) and an fsm-emitted event, not a
  rebuild counter. Producer-side emission (whether MAX_ROUNDS_CLAMPED carries
  effective_max_rounds) is Phase 5 fsm scope — flagged for the Phase 5 lens.
- **O-3 (INFO):** the anchor-map artifact's generic-consumer line numbers drifted (expected;
  the map self-declares it drifts). run_log.py itself is correct.
