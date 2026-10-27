# Phase 3 M4 Source-Fidelity Fix Report — Pass 2 (spec.md + prd.md propagation)

**Date:** 2026-06-18
**Role:** rf-qa, M4 source-fidelity fix (authorized, fix_authorization: true)
**Scope:** Propagate two already-applied tdd.md corrections into spec.md and prd.md. tdd.md NOT edited (already correct). No source code, no .claude mirrors, no phase-outputs/reviews. P2/P5 PENDING preserved (untouched).
**Grounding sources read first:** tdd.md:420-528 (DM-003 + StageError caveat + data flow), src/superclaude/skills/task-builder/SKILL.md:870-893 (canonical DNSP/DM-003 contract).

## Overall Verdict: PASS (both fixes propagated; files now consistent with tdd.md)

---

## FIX 1 — StageError stale "as today" claim (M4 qualitative finding #1)

Reworded every "raise StageError as today" / "exactly as today" claim and brought the parallel risk/test/rollback surfaces into consistency with tdd.md:427-437 (zero-success = all-agents-fail escalation path; typed `StageError` = release intent / implementation-time decision, NOT current behavior). Removed all "as today" / "exactly as today" tokens (verified zero remain via grep). The one surviving `task_range` mention in spec.md:479 is the clearly-labeled historical correction note (mirrors tdd.md:459), permitted by the fix instruction.

### spec.md edits (FIX 1)
1. **~L101** — "zero-success raises `StageError` as today" → "zero-success follows the all-agents-fail escalation path — a typed `StageError` is release intent / an implementation-time decision, NOT current behavior".
2. **~L257** (FR-RFMERGE.3 description) — "raise `StageError` exactly as today" → all-agents-fail escalation path (rf-team-lead-style fix-cycle, task-builder Path A, SKILL.md:873-911); typed StageError = release intent, not verified current behavior.
3. **~L277** (acceptance criterion) — "zero-success raises `StageError`" → all-agents-fail escalation path; typed StageError = implementation-time decision.
4. **~L579** (P3 YAML `on_zero_success`) — "raise StageError (as today)" → "all-agents-fail escalation path (task-builder Path A); typed StageError = release intent, NOT current behavior".
5. **~L625** (Risk table) — consistency: "zero-success raises `StageError`" → all-agents-fail escalation path (release intent: StageError; no typed StageError in current source — §4.5 caveat).
6. **~L642** (Test plan row) — consistency: renamed test fn `test_dnsp_all_agents_fail_raises_stageerror` → `test_dnsp_all_agents_fail_escalates`; reframed "confirm the StageError raise site" → NEW requirement (no typed StageError exists); assertion now "no synthetic emitted + escalation path fires" (mirrors tdd.md:843).
7. **~L685** (Rollback plan) — "restore prior `StageError`-on-failure" → "fall back to the all-agents-fail escalation path; release intent: StageError, §4.5 caveat" (mirrors tdd.md:947).

### prd.md edits (FIX 1)
1. **~L236** — "raising `StageError` on total failure" → on total failure follows the all-agents-fail escalation path; typed StageError = release intent / implementation-time decision, not current behavior.
2. **~L522** (acceptance criterion) — "zero-success raises `StageError` exactly as today" → all-agents-fail escalation path; typed StageError = release intent / implementation-time decision, NOT current behavior.
3. **~L669** (Risk table) — "zero-success raises `StageError`" + "Restore prior `StageError`-on-failure" → all-agents-fail escalation path (release intent: StageError; no typed StageError in current source) / fall back to escalation path.

## FIX 2 — P3 synthesized-finding data model (M4 qualitative finding #2)

### spec.md §4.5 (~L464-482) — full replacement
Replaced the OLD under-specified 3-field model (`severity` / `task_range` / `source`) and the false "canonical type lives in current Stage-7/orchestrator merge code" claim with the tdd.md:450-489 / SKILL.md:873-889 framing:
- Canonical owner = `task-builder` (DM-003), `task-builder/SKILL.md:873-911`; P3 REUSES verbatim (narrower Stage-7 case), does NOT redefine.
- Canonical field is `affected_range` (note: earlier `task_range` non-canonical).
- Required fields now include `evidence`, fixed byte-exact `recommendation`, 2-element `dedup_key`, `found_n_times`; illustrative dict carries R-113..R-119 field constraints.
- Guard 1 reframed to Path A/B/C precedence (R-122); zero-success = all-agents-fail escalation path (typed StageError = release intent), not "raise StageError".

### prd.md
- **~L750** (data-model summary row "P3 synthesized finding") — "Existing validation-finding shape gains a `source` field … else `StageError`" → REUSES task-builder-owned `synthetic-dnsp`/DM-003 contract (fixed HIGH+source, `affected_range`, `evidence`, fixed `recommendation`, 2-element `dedup_key`, `found_n_times`); canonical contract owned by task-builder, not current Stage-7 code; else the all-agents-fail escalation path (release intent: StageError).
- prd.md has no dedicated §4.5-equivalent illustrative-dict block, so no further structural block replacement was needed; the summary-row reframe is the prd surface of FIX 2.

## Edit counts
- **spec.md: 8 edits** (5 FIX-1 reword/consistency + 1 FIX-1 risk-table + 1 FIX-1 rollback already counted; precisely: L101, L257, L277, L579, L625, L642, L685 = 7 FIX-1, plus §4.5 full replacement = 1 FIX-2). **Total spec.md = 8.**
- **prd.md: 4 edits** (L236, L522, L669 = FIX-1; L750 = FIX-2). **Total prd.md = 4.**

## Adversarial axis results
| Axis | Fired? | Note |
|------|--------|------|
| AX-1 drift | none after fix | source-of-truth = tdd.md + SKILL.md:873-911; all reworded text matches |
| AX-2 contradictions | resolved | bare "raises StageError" risk/test/rollback rows contradicted reworded core claims + tdd.md; brought into consistency |
| AX-3 omissions | none | FIX-2 added the previously-omitted `evidence`/`recommendation`/`dedup_key`/`found_n_times` fields |
| AX-4 weakened criteria | none | criteria not weakened; total-failure visibility preserved (escalation path, no masking) |
| AX-5 invented content | none | every field/line traces to tdd.md:450-489 / SKILL.md:873-889 |

## Unresolved issues
None. tdd.md left untouched (already correct). P2/P5 PENDING preserved. The historical `task_range` mention retained in spec.md:479 is the intentional correction-note form (matches tdd.md:459), not a stale operative token.
