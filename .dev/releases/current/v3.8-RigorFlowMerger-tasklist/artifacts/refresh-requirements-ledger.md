---
title: RFMerger Refresh — Requirements Ledger (Canonical P1-P5)
generated: 2026-06-18
status: refreshed-draft
task: TASK-RF-rfmerger-refresh-20260618-172224 (Step 2.1)
---

# RFMerger Refresh — Requirements Ledger

**Purpose.** Canonical ledger mapping the historical RigorFlow-Merger (RFMerger) P1-P5
proposals onto current `src/superclaude/...` source surfaces for the refresh. Each row carries
its historical evidence, the adversarial/current revision, the implication for current source,
the refresh disposition, the human-decision status, and the validation coverage. This is a
**refreshed-draft document only** — it produces no implementation tasklist and promotes no stale
token to current guidance.

**Canonical taxonomy.** The canonical RFMerger P1-P5 below follow the historical proposal
numbering in `design-rfmerger-proposals.md`: P1 Context-Armed Steps, P2 Bounded Patch Loop,
P3 DNSP (Detect-Nudge-Synthesize-Proceed), P4 Evidence-Anchored Validation, P5 Feedback-Driven
Tier Calibration. All historical evidence is **HISTORICAL-ONLY** unless re-checked against current
source.

**Stale-token discipline.** Tokens `/rf:*`, `.gfdoc`, `llm-workflows`, `/config/.claude`, and
`sc:task-unified` appear in this ledger **only** as historical-evidence citations. None is a
current edit target; each row names the current source surface to rebase onto.

## Canonical RFMerger P1-P5 Ledger

| ID | Historical proposal | Historical evidence | Adversarial/current revision | Current-source implication | Refresh disposition | Human decision status | Validation coverage |
|---|---|---|---|---|---|---|---|
| **P1** | **Context-Armed Steps** — borrow RF self-contained-item pattern (R1): add per-step `Context:`/`Ensuring:` sub-fields to each EXECUTION step. | `design-rfmerger-proposals.md` Proposal 1 (lines 69-106); `FINAL-REPORT.md` §5 line 140, §6.2 F1 lines 175-178, R2 lines 214-220. [HISTORICAL-ONLY] | REVISE (Proposed 22/50 → Conservative 34/50, convergence 0.75). Generator works on roadmap *text*, not a live codebase → per-step file paths would be hallucinated/stale. Adopt an optional task-level `## Execution Context` block: roadmap refs always included, "source areas" not file paths, **no** `Ensuring:` clause. (`adversarial-validation.md:58-104`.) | Align with current tasklist phase template `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md`; Acceptance Criteria remain the single source of truth (no duplicate `Ensuring:`); no invented/per-step paths. | **Retain (conservative, adversarially-revised form only).** Adopt the task-level `## Execution Context` block; reject the original per-step form. No heavyweight new mechanism. | **N/A** (retained, conservative — no human gate). | Add `## Execution Context` template assertion + phase-template tests if retained; covered by refreshed spec + TDD test plan. |
| **P2** | **Bounded Patch Loop** — borrow RF correction loops (R4): after Stage 10, loop back to Stage 9 re-patching ONLY the UNRESOLVED subset, capped at 2 extra cycles (3 total passes). Historical Stage-9 delegate cited as `sc:task-unified`. | `design-rfmerger-proposals.md` Proposal 2 (lines 110-144); `FINAL-REPORT.md` §5 line 141, §6.2 F2 lines 180-184, R4 lines 230-238. Historical delegate `sc:task-unified` (`FINAL-REPORT.md:83,181`). [HISTORICAL-ONLY] | REVISE (Proposed 20/50 → Conservative 39/50, convergence 0.85). Subset-only re-validation is a structural correctness defect (oscillation/regression risk). If retained at all: full-set re-validation + monotonicity guard + regression detection + **1-extra-pass cap (2 total passes: original + at most 1 re-patch pass)** — the adversarially-adopted cap (`adversarial-validation.md:141`; corroborated `FINAL-REPORT.md:236,334`); interactive human checkpoint preferred. (NOTE: the Canonical [HISTORICAL-ONLY] column's "3 total passes" is the **pre-adversarial / rejected** Variant-B value, retained there only as historical evidence; the adversarial revision adopted 2 total passes.) (`adversarial-validation.md:107-143`.) | Must reconcile current Stage 9/10 + Stage 10.5 reflect responsibilities first; any extra loop must NOT overlap Stage 10.5 reflect remediation. Historical `sc:task-unified` delegate remaps to current `sc:task` (do not edit the stale name). | **`decision: retain-with-full-set-revalidation-and-guards`** (recorded 2026-06-19 by human operator; explicit choice, not a default). Retained in its full guarded form: full-set re-validation + monotonicity guard + regression detection + 1-extra-pass cap (2 total passes) + no overlap with Stage 10.5. Downstream implementation-tasklist generation is now UNBLOCKED. | **`decision: retain-with-full-set-revalidation-and-guards`** — chosen from {`defer`, `retain-with-full-set-revalidation-and-guards`} (recorded 2026-06-19). (Underpinned by historical open risk K4, patch-loop regression.) | RETAINED (recorded 2026-06-19) — active implementation requirements: tests for full-set re-validation, monotonicity guard, regression detection, **1-extra-pass cap (2 total passes: original + at most 1 re-patch pass; `adversarial-validation.md:141`)**, and non-overlap with Stage 10.5. |
| **P3** | **DNSP** — canonical **Detect-Nudge-Synthesize-Proceed** (task-label gloss: "Dynamic / synthetic no-source provenance"; same entry). On Stage-7 validation-agent retry failure, synthesize a conservative HIGH finding for the affected task range and proceed (never block Stage 8 on one agent). | `design-rfmerger-proposals.md` Proposal 3 (lines 148-189); `FINAL-REPORT.md` §5 line 139, §6.1 line 166, R1 lines 206-213. RF source mechanism R3 (`automated_qa_workflow.sh:4698-4723`, an `.gfdoc` historical path). [HISTORICAL-ONLY] | ADOPT (Proposed 39/50 — the adversarial winner; convergence 0.80; only proposal adopted as-proposed). Two refinements: (1) **all-agents-fail guard** — DNSP activates only when ≥1 agent succeeded; if zero succeeded, zero-success follows the all-agents-fail escalation path (whether to surface a typed `StageError` is a new implementation-time decision / release intent, not current behavior — no typed `StageError` exists in current source); (2) synthesized findings carry **`source: "synthetic-dnsp"`** provenance metadata. (`adversarial-validation.md:23-55`.) | Belongs in current validation-agent failure handling / orchestrator merge step (~25 lines). The `.gfdoc` script path is historical evidence only, not an edit target. **Ownership note: a `synthetic-dnsp` contract ALREADY EXISTS, owned by `task-builder` (`src/superclaude/skills/task-builder/SKILL.md:873-911`) — richer (fixed `HIGH`+`source`, 2-element dedup key, found-count, all-agents-fail Path A/B/C, additive merge, N-1 concurrency). The `sc:tasklist` P3 REUSES that contract (the narrower Stage-7 case), it does NOT define a new divergent one.** | **Retain (adopted + refined form, reusing the existing task-builder `synthetic-dnsp` contract).** Carry the adopted DNSP with **both** the all-agents-fail guard (activate only when ≥1 agent succeeded; else zero-success follows the all-agents-fail escalation path — typed `StageError` is release intent / an implementation-time decision, not current behavior) **and** the `source: "synthetic-dnsp"` provenance marker on every synthesized finding, conformant to the existing contract (`HIGH` non-overridable; 2-element dedup key). | **retained-with-guard (no human gate needed)** — guard stated explicitly: all-agents-fail guard + `source: "synthetic-dnsp"` provenance marker are mandatory; without them P3 is not retained. | Add tests for synthetic-finding provenance (`source: "synthetic-dnsp"`), the all-agents-fail guard (zero-success → all-agents-fail escalation path; typed `StageError` is release intent / implementation-time decision, not current behavior), AND compatibility/regression vs the existing `task-builder` contract (`tests/skills/test_task_builder_merge.py`, `tests/audit/test_dnsp_*` where present) if implemented; covered by refreshed spec + TDD. |
| **P4** | **Evidence-Anchored Validation** — borrow RF PABLOV evidence (R2): add a new Stage 6.5 emitting `generation-evidence.json` under `TASKLIST_ROOT/validation/evidence/`, with regex-extracted task/deliverable/roadmap IDs feeding Stage 7 agents. | `design-rfmerger-proposals.md` Proposal 4 (lines 193-258); `FINAL-REPORT.md` §5 line 142, §6.2 F3 lines 186-189, R3 lines 222-228. [HISTORICAL-ONLY] | REVISE (Proposed 27/50 → Conservative 39/50, convergence 0.82). The existing pre-write quality gate (the historical adversarial reasoning called it "17-point"; the **current source gate is 20-check**, checks 1-20 per `sc-tasklist-protocol/SKILL.md:1132-1194`) already catches orphan deliverables / missing roadmap items; a new JSON-extraction stage is redundant and adds a high-authority regex failure surface. Adopt the lighter **Quality-Gate Evidence Passthrough**: Stage 6 emits `TASKLIST_ROOT/validation/gate-results.txt`, injected into Stage 7 prompts (~15 lines). (`adversarial-validation.md:146-196`.) | Reuse existing quality-gate output; inject gate evidence into validation prompts. **Explicitly a quality-gate PASSTHROUGH — NOT a new "Stage 6.5 JSON/PABLOV pipeline"** and NOT a new `generation-evidence.json` artifact system. | **Retain as a quality-gate PASSTHROUGH.** Emit `gate-results.txt` from the existing gate and pass it into Stage 7 prompts. Reject the original Stage 6.5 + `generation-evidence.json` JSON pipeline. | **N/A** (retained, lighter form — no human gate). | Add task items for prompt passthrough + tests that the gate-results passthrough reaches Stage 7; no new-artifact regex tests. Covered by refreshed spec + TDD. |
| **P5** | **Feedback-Driven Tier Calibration** — borrow RF agent-memory + correction patterns: Stage 0 reads `feedback-log.md`, builds `tier-calibration.json`, and **mutates** scored tiers during Stage 4. | `design-rfmerger-proposals.md` Proposal 5 (lines 261-302); `FINAL-REPORT.md` §5 line 143, §6.2 F4 lines 191-194, R5 lines 240-246. [HISTORICAL-ONLY] | REVISE (Proposed 23/50 → Conservative 40/50, convergence 0.85). Auto-mutating tiers from hidden feedback violates the "same roadmap → same output" determinism guarantee (the "hidden input" problem). Adopt **advisory-only**: render a `## Tier Calibration Advisory` section (min 2 matching overrides) with STRICT-downgrade warnings; scored tiers stay roadmap-only. (`adversarial-validation.md:200-249`.) | If retained, advisory rendering must NOT mutate scored tiers; scored tiers remain a pure function of the roadmap (determinism preserved). | **`decision: retain-advisory-only`** (recorded 2026-06-19 by human operator; explicit choice, not a default). Retained advisory-only: scored tiers stay deterministic and roadmap-only; the advisory may read `feedback-log.md` but never feeds back into or mutates the scored tiers. Downstream implementation-tasklist generation is now UNBLOCKED. | **`decision: retain-advisory-only`** — chosen from {`defer`, `retain-advisory-only`} (recorded 2026-06-19). (Underpinned by historical open risk K2, feedback-log population.) | RETAINED advisory-only (recorded 2026-06-19) — active implementation requirement: tests proving the advisory section never alters scored tiers (determinism). |

## Naming-collision quarantine — reflect UC-2 "P1-P5" is NOT the canonical RFMerger P1-P5

> **QUARANTINE — NAMING COLLISION.** The `sc:reflect` UC-2 protocol uses the labels **P1-P5**
> for an entirely different taxonomy: P1/P2 per-task verdicts (`per_task_verdicts[]`), P3
> cross-task interaction scanning (Wave 1B.3 symbol-overlap graph), P4 per-task verdict report
> rendering (`refs/report-template.md`), and P5 budget routing (`--budget-remaining`,
> `budget_forced_tier_downgrade`). (Source: `research/04-task-builder-boundaries.md:61-73`, §7,
> citing `sc-reflect-protocol/SKILL.md:769,776,308,319` and `refs/report-template.md:105-107`.)
>
> **These reflect UC-2 "P1-P5" are NOT the canonical historical RFMerger P1-P5 in the ledger
> above.** They share only the `P<n>` label — there is no semantic correspondence (reflect P1 ≠
> RFMerger P1 Context-Armed Steps, etc.). The two taxonomies MUST be kept strictly separate.
> Downstream synthesis (spec / PRD / TDD) MUST NOT substitute the reflect UC-2 taxonomy for the
> canonical RFMerger P1-P5, and MUST NOT re-use the reflect `P<n>` labels when referring to
> RFMerger proposals. Per `research/04` §7, the RFMerger P1-P5 are largely *existing* reflect
> contract/spec surface — the complementary path is consumer wiring / fixture coverage / boundary
> enforcement, not greenfield re-implementation of reflect's own UC-2 fields.

## Notes

- **Canonical source-of-truth.** All current edit targets resolve under `src/superclaude/...`
  (canonical) with `.claude/` as a generated mirror via `make sync-dev` + `make verify-sync`. No
  row above names a `.claude/` mirror as an edit target.
- **Stale-token audit (this ledger).** `/rf:*`, `.gfdoc`, `llm-workflows`, `/config/.claude`, and
  `sc:task-unified` appear above **only** as historical-evidence citations (P2 cites
  `sc:task-unified`; P3 cites the `.gfdoc` `automated_qa_workflow.sh` path) — each is paired with
  its current-source rebase target. None is presented as a current edit target. The old
  "10-stage-only" tasklist framing is also historical-only; the current model is 11-stage with a
  Stage 10.5 reflect gate.
- **Human-decision blocking semantics.** P2 and P5 are now decided (recorded 2026-06-19): P2 =
  `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only`. Both are explicit human
  choices, not defaults. Document QA/review proceeded; with both decisions now recorded in the refreshed
  documents (and the review checkpoint passing), **implementation-tasklist generation is UNBLOCKED**. This ledger
  records the decisions; it selected no default for either. The canonical decision records
  are `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/phase-outputs/reviews/p2-human-decision-record.md`
  and `.../p5-human-decision-record.md`; when a decision is recorded it must be propagated to **all four**
  document carriers (`spec.md`, `prd.md`, `tdd.md`, and this ledger) so no P2/P5 field is left stale.
- **Non-goals carried forward.** RF mechanisms R5 (session management) and R6 (batch-immutability /
  UID tracking) are execution-time concepts judged N/A to SC generation and are explicit non-goals
  (HIST Section B); they are intentionally absent from the canonical P1-P5 ledger.
