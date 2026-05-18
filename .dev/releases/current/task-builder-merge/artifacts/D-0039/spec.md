# D-0039 — T03.16 Spec: MIG-003 PR-04 Landing Migration

**Task:** T03.16 (Phase 3)
**Roadmap items:** R-067, R-068
**Date:** 2026-05-17
**Status:** PASS (landed at commit `ad083b6`)

---

## 1. Scope

MIG-003 is the single-commit landing migration for FR-CONV.3 — the
`## Inherited Structural Verdict` PR-04 Gate Results Passthrough between
rf-qa (A.10 producer) and rf-qa-qualitative (A.10.5 consumer), plus the
`## Self-Audit` consumer-side reliance-vs-verification accounting (M3).
The migration is strictly additive: the anti-inflation Prohibited
Behaviors block in the Confidence Gate Protocol at
`rf-qa-qualitative.md:766-775` remains byte-identical pre/post (verified
by quality-engineer sub-agent — see `evidence.md` § 4), the
BUILD_REQUEST schema is untouched, M2 Execution Context Header emission
is preserved, and TB-Add-7 / TB-Add-8 / MALFORMED retry max-2 invariants
are all maintained.

## 2. FF_INHERITED_STRUCTURAL_VERDICT feature flag

| Field | Value |
|---|---|
| Flag name | `FF_INHERITED_STRUCTURAL_VERDICT` |
| Scope | A.10 → A.10.5 verdict passthrough: spawn-prompt injection of `## Inherited Structural Verdict` block at SKILL.md §A.10.5 (producer side), Critical Rule #11 reliance/verification distinction + `## Self-Audit` output schema at rf-qa-qualitative.md (consumer side), INV-002 fix-cycle freshness re-injection, INV-010 dynamic TB-Add-* enumeration, INV-019 Self-Audit obligation |
| Default value at M3 | `ON` (DEFAULT-ON at landing) |
| Activation commit | `ad083b6` on `feat/mig-002-execution-context-header` (Phase 3 piggybacks the M2 landing branch; final merge to `master` follows release-spec §19.x sequencing) |
| Governance file | This spec (`D-0039/spec.md`) |
| Cleanup window | **M7 consolidation** (post-M3..M6 stabilization) — when the K-003 audit-target window (first 5 rf-qa-qualitative runs post-FR-CONV.3; release-spec §8.3 row 4) reports 100% Self-Audit coverage and no INV-019 regressions are observed across M3..M6, the passthrough behavior is folded into the rf-qa/rf-qa-qualitative contract proper and the flag is retired. Operationalised by the OPS-001 runbook (M7). |
| Cross-references | Phase 3 task T03.16 (this artifact); M7 consolidation window (OPS-001 runbook + K-003 gate); roadmap items R-067 (single-commit landing) and R-068 (governance); release-spec §8.3 row 4 (audit-after-FR-CONV.3-lands); release-spec §19.4 (rollback path — passthrough flag disable); D-0025 (MIG-002 governance, for cross-flag M7 coordination) |

## 3. Per-line rollback path (commit body authoritative)

Documented in the MIG-003 commit body (`git log <MIG-003-SHA>`):

1. **SKILL.md** — comment out the `**Inherited Structural Verdict
   (PR-04 Gate Results Passthrough …):**` directive paragraph in §A.10.5
   (the orchestrator extraction + splice instruction). The embedded
   `## Inherited Structural Verdict (rf-qa A.10 output — DO NOT
   re-verify)` heading in the spawn-prompt template MAY remain inert;
   suppressing the directive prevents the orchestrator from extracting
   the Items Reviewed span, so the heading materialises with no body
   (the consumer's branch-3 "Missing / malformed verdict" fallback
   handles the empty case by reverting to standalone behavior).
2. **SKILL.md** — comment out the `**Fix-cycle re-entry (INV-002
   freshness — stale-verdict rejection):**` procedure block (steps
   1–7). With no producer extraction running, there is no verdict to
   re-inject; the procedure becomes a no-op naturally.
3. **SKILL.md** — comment out the `**TB-Add catalogue enumeration
   (INV-010 dynamic catalogue lookup):**` procedure block (steps 1–8).
   With no verdict block to assemble, the dynamic enumeration has no
   downstream consumer.
4. **SKILL.md** — restore the original passthrough sentence wording in
   the orchestrator narrative (i.e. revert the per-cycle re-read
   guidance to the M1 baseline that did not yet exercise the PR-04
   passthrough). The fall-back-to-standalone clause in Critical Rule
   #11 of rf-qa-qualitative.md (see step 5 below) ensures the consumer
   side does not break when the producer side is disabled.
5. **rf-qa-qualitative.md** — the additive trailing sections
   ("Self-Audit Schema Requirement (INV-019, K-003 Audit-Target)" and
   "Handling the Inherited Structural Verdict") MAY remain in the file
   as documentation; they describe behavior under
   `FF_INHERITED_STRUCTURAL_VERDICT=ON` and the branch-3 fallback
   ("Missing / malformed verdict — fall back to standalone behavior")
   is explicit in their text. Critical Rule #11's reliance-vs-
   verification clause is also fallback-aware ("When the Inherited
   Structural Verdict is missing or malformed, fall back to your
   standalone behavior"). Per-line rollback therefore only requires
   the producer-side suppression above; no consumer-side edits are
   needed.

**Invariant during rollback:** the Prohibited Behaviors block at
`rf-qa-qualitative.md:766-775` is untouched at every step (it was
byte-identical pre/post MIG-003 and remains so under rollback). MIG-002
Execution Context Header emission, BUILD_REQUEST schema, MALFORMED
retry max-2 failure-mode, per-item Context evidence-binding (TB-Add-8),
and TB-Add-7 degraded-form tolerance continue to function unchanged.

**Fallback behavior post-rollback:** rf-qa-qualitative reverts to
independent structural re-checking (the M1 baseline) — Critical Rule
#11's fallback clause ("fall back to your standalone behavior")
covers the missing-verdict case. The producer (rf-qa) continues to
emit its `qa-task-validation-report.md` with the Items Reviewed table;
the table simply ceases to be threaded into the consumer's spawn
prompt.

## 4. Acceptance Criteria mapping

| AC (phase-3-tasklist.md L780–784) | Evidence location |
|---|---|
| `make verify-sync` exits 0 immediately after MIG-003 commit | `evidence.md` § 3 (logged exit code) |
| Commit body documents passthrough-flag disable as rollback path | `git show <MIG-003-SHA>` commit body, "Rollback path (per-line revert)" section + this spec § 3 |
| Sub-agent report confirms strictly-additive change with rf-qa-qualitative.md:766-775 byte-identical | `evidence.md` § 4 (quality-engineer report transcript + byte-diff hash) |
| FF_INHERITED_STRUCTURAL_VERDICT entry recorded at `TASKLIST_ROOT/artifacts/D-0039/spec.md` | This spec § 2 |

## 5. Dependencies

- T03.15 PASS (`D-0038/evidence.md` — TEST-010 dynamic enumeration INV-010 fixture green; 19 assertions PASS in `tests/audit/test_dynamic_enumeration_inv_010.py`)
- T03.14 PASS (`D-0037/evidence.md` — TEST-009 Self-Audit INV-019 fixture green; positive + negative + missing-heading cases all confirmed)
- T03.13 PASS (`D-0036/evidence.md` — TEST-008 INV-002 freshness 2-cycle fixture green; cycle-1 vs cycle-2 byte-diff at verdict-table region demonstrates re-injection)
- T03.12 mid-checkpoint PASS (`CP-P03-T07-T11.md`)
- T03.11 PASS (`D-0035/evidence.md` — TEST-007 inherited-verdict-present fixture green)
- T03.10 PASS (`D-0034/evidence.md` — rf-qa-qualitative.md EOF append: "Handling the Inherited Structural Verdict" + `## Self-Audit` schema; :766-775 byte-identical post-edit)
- T03.09 PASS (`D-0033/evidence.md` — SKILL.md A.10.5 spawn-prompt injection; "Inherited Structural Verdict" present in the spawn-prompt block; post-additive growth shifted the line index but the splice position is preserved relative to TARGET FILES / INSTRUCTIONS markers)
- T03.08 PASS (`D-0032/evidence.md` — anti-inflation Prohibited Behaviors block byte-stability + failure-mode halt at §A.10 before §A.10.5 when verdict missing)
- T03.06 mid-checkpoint PASS (`CP-P03-T01-T05.md`)
- T03.05 PASS (`D-0030/evidence.md` — INV-002 freshness rule wired at SKILL.md §A.10.5)
- T03.04 PASS (`D-0029/evidence.md` — Self-Audit output schema + INV-019 obligation)
- T03.03 PASS (`D-0028/evidence.md` — API-002-M3 spawn-prompt injection)
- T03.02 PASS (`D-0027/evidence.md` — DM-002-M3 3-field schema)
- T03.01 PASS (`D-0026/evidence.md` — FR-CONV.3 wrapper landed)

## 6. Risk + mitigation

| Risk | Mitigation |
|---|---|
| Producer-side passthrough regression injects stale cycle-N−1 verdict on fix-cycle re-spawn | INV-002 freshness procedure at SKILL.md §A.10.5 (re-read producer artifact + re-extract Items Reviewed span + re-enumerate TB-Add-* every cycle + sha256 stale-verdict ledger check); TEST-008 fixture asserts cycle-2 spawn contains cycle-2 content (D-0036 evidence) |
| Hand-maintained TB-Add catalogue drifts from rf-qa.md ground truth (K-007 sequencing inversion) | INV-010 dynamic enumeration: every spawn re-pulls TB-Add-* IDs from `rf-qa.md`'s `#### Structural Gate Additions` region at runtime; TEST-010 fixture (D-0038 evidence) asserts a synthetic TB-Add-N+1 stub auto-richens the catalogue with zero SKILL.md edits |
| Consumer relies on inherited PASS items without independent semantic verification (tool-engagement inflation) | INV-019 Self-Audit obligation: every rf-qa-qualitative report MUST emit `## Self-Audit` with category-(a) reliance list AND category-(b) ≥1 independent semantic check; TEST-009 negative case (zero category-(b)) MUST fail; K-003 audit window (release-spec §8.3 row 4) inspects first 5 rf-qa-qualitative runs post-FR-CONV.3 (D-0037 evidence) |
| Producer emits no verdict, consumer spawns and fabricates verification state | DM-005 `failure_mode: halt-A.10-before-A.10.5` lever wired at SKILL.md §A.10 branch 4 ("No verdict emitted") — orchestrator halts before §A.10.5; rf-qa-qualitative is NEVER spawned for a task on a cycle where the producer has no `VERDICT:` line; D-0032 + D-0034 evidence confirm |
| Anti-inflation block weakened, removed, or paraphrased during PR-04 wiring | T03.08 byte-stability gate captured sha256 of :766-775 pre-edit; this commit's pre-commit hash matches `0570c6b…` post-edit (see § 4 of `evidence.md`); quality-engineer sub-agent independently re-verifies; mirror parity (`.claude/agents/rf-qa-qualitative.md:766-775`) also byte-identical |
| K-003 audit window fails on first 5 runs (≥1 INV-019 violation) | Operational rollback path: disable `FF_INHERITED_STRUCTURAL_VERDICT`, follow per-line revert procedure § 3 above; consumer falls back to standalone structural re-checking per Critical Rule #11; producer-side `qa-task-validation-report.md` emission unaffected. Release-spec §19.4 codifies this fallback as the canonical rollback path |
