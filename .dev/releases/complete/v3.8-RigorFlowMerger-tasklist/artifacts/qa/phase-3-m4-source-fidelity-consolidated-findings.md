# M4 Source-Fidelity — Consolidated Findings

**Step:** 3.5 (M4 source-fidelity consolidation)
**Task:** TASK-RF-rfmerger-refresh-20260618-172224
**Date:** 2026-06-18
**Scope:** M4 source-fidelity ONLY (NO M3 structural/content findings mixed in)
**Disposition:** Report-only — NO fixes applied.

---

## CONSOLIDATED VERDICT: FAIL

**Rule:** Consolidated verdict is FAIL if ANY of the six M4 reports is FAIL.

**Per-report verdict roll-up (PER-OUTPUT granularity preserved):**

| # | M4 Report | Affected document(s) | Verdict |
|---|-----------|----------------------|---------|
| 1 | phase-3-m4-fidelity-historical-vs-spec.md | spec.md | **FAIL** |
| 2 | phase-3-m4-fidelity-historical-vs-prd.md | prd.md | **FAIL** |
| 3 | phase-3-m4-fidelity-historical-vs-tdd.md | tdd.md | **FAIL** |
| 4 | phase-3-m4-fidelity-current-source-vs-spec.md | spec.md | PASS |
| 5 | phase-3-m4-fidelity-current-source-vs-tdd.md | tdd.md | **FAIL** |
| 6 | phase-3-m4-fidelity-ledger-matrix.md | refresh-requirements-ledger.md, refresh-validation-matrix.md | PASS |

**Tally:** 4 of 6 reports FAIL → CONSOLIDATED VERDICT = **FAIL**.

PASS outputs (not collapsed into the package verdict): `spec.md` is current-source-clean (report 4), and `refresh-requirements-ledger.md` + `refresh-validation-matrix.md` are fidelity-clean against both historical and current source (report 6). The FAIL is driven by historical-fidelity drift on spec/prd/tdd and current-source drift on tdd — NOT by the ledger/matrix outputs.

---

## Adversarial axis legend

- **AX-1** drift from source
- **AX-2** contradictions
- **AX-3** omissions
- **AX-4** weakened criteria
- **AX-5** invented content

---

## Deduplicated Findings

Deduplicated by **affected document + requirement**. The P2 bounded-patch-loop cap defect recurs as the SAME requirement across THREE different documents (spec.md, prd.md, tdd.md); per the dedup key (document + requirement) these remain three distinct findings — one per document — because the fix must be applied independently in each. The P3 contract under-specification in tdd.md was flagged by TWO agents (historical-vs-tdd and current-source-vs-tdd) against the SAME document + requirement → collapsed to ONE finding (F-06) with both originators credited.

| ID | Originating agent(s) | Severity | Axis | Affected document | Description | Required fix | Source-evidence path | Blocks tasklist gen? |
|----|----------------------|----------|------|-------------------|-------------|--------------|----------------------|----------------------|
| F-01 | historical-vs-spec | CRITICAL | AX-1, AX-4, AX-5 | spec.md | P2 retained-option contract invents a 3-total-pass cap (original + 2 re-patch passes); historical post-adversarial recommendation was one retry / 2 total passes. | Change every P2 cap reference to original + 1 retry = 2 total passes, OR explicitly mark the 3-pass version as a new current-source revision rejecting historical guidance, with rationale + citation. | `spec.md:209-214`, `:230`, `:237-239`, `:575-580` vs `artifacts/adversarial-validation.md:135-142`, `FINAL-REPORT.md:230-237` | YES |
| F-02 | historical-vs-prd | IMPORTANT | AX-1, AX-4 | prd.md | PR-2 retained-if-chosen cap says 3 total / 2 extra passes; historical revised cap is 2 total passes (one retry). Reintroduces the pre-adversarial design cap. | Change PRD P2 acceptance criteria + risk mitigation to "2-total-pass cap (original + one retry)" unless a new explicit, cited product decision justifies expansion. | `prd.md:505`, `:656` vs `artifacts/adversarial-validation.md:137-141`, `FINAL-REPORT.md:236` | YES |
| F-03 | historical-vs-tdd; current-source-vs-tdd (corroborating) | IMPORTANT | AX-2, AX-5 | tdd.md | P2 retained-option cap uses 2 extra / 3 total passes, matching the pre-adversarial original proposal rather than the post-adversarial final (one retry / 2 total). | Change all P2 retained-option references in `tdd.md` to original + one retry = 2 total passes, unless a new revision away from historical recommendation is declared and justified with citations. | `tdd.md:289`, `:628-640`, `:690-694`, `:799-801`, `:930-931` vs `artifacts/adversarial-validation.md:137-142`, `FINAL-REPORT.md:234-236` | YES |
| F-04 | historical-vs-spec | IMPORTANT | AX-2, AX-4 | spec.md | P5 overclaims hidden-feedback determinism as "same roadmap → same output" while the advisory depends on `feedback-log.md`; sample mislabels a STANDARD→STRICT upgrade as "STRICT-downgrade", contradicting the stated downgrade rule. | Rephrase determinism to "same roadmap → same scored tiers" and "same roadmap + same feedback-log.md → same advisory"; fix the sample row/warning label so STRICT downgrade means STRICT → lower tier only. | `spec.md:106-109`, `:332-340`, `:341-344` | YES |
| F-05 | historical-vs-prd | IMPORTANT | AX-1, AX-3 | prd.md | P5 changed to PENDING human decision; historical post-adversarial recommendation was REVISE/advisory-only. PRD does not state this is a deliberate departure nor reject advisory-only as a non-goal. | Either (a) align PRD to retained-advisory-only, or (b) add cited rationale that the refresh intentionally supersedes the historical advisory-only recommendation with a PENDING decision, preserving advisory-only as the only allowed retain shape. | `prd.md:543-558`, `:655`, `:691` vs `artifacts/adversarial-validation.md:227-249`, `FINAL-REPORT.md:240-246` | YES |
| F-06 | historical-vs-tdd; current-source-vs-tdd | CRITICAL | AX-2, AX-3, AX-4 | tdd.md | P3 synthesized-finding data model claims reuse of the existing task-builder `synthetic-dnsp` contract but under-specifies it: lists only `severity`, `task_range`, `source`; omits `dedup_key` (2-element), `found_n_times`, `affected_range`, nonblank `evidence`, fixed `recommendation`, all-agents-fail/merge semantics. | Expand the P3 data model to enumerate the full task-builder DNSP contract fields with their fixed/dynamic invariants, OR explicitly state `sc:tasklist` stores only a narrower projection and justify why this does not violate the reuse claim. | `tdd.md:438-456`, `:289-291` vs `task-builder/SKILL.md:873-911` | YES |
| F-07 | current-source-vs-tdd | CRITICAL | AX-5 | tdd.md | TDD presents a `StageError` zero-success raise and a "canonical finding type lives in current Stage-7/orchestrator merge code" as current ("exactly as today") for `sc:tasklist`; grep over current tasklist protocol + CLI finds no `StageError` — Stage 7 is markdown instructions, not typed orchestrator code. | Reword all `StageError`/current finding-type claims as release intent, or cite/use an actual current error/return contract; if a new `StageError` is desired, define it as a future requirement + add a discovery item. | `tdd.md:422-450`, `:523-525`, `:623-624`, `:666-667`, `:692-693`, `:1104-1107` vs grep of `src/superclaude/skills/sc-tasklist-protocol`, `src/superclaude/cli/tasklist` | YES |
| F-08 | current-source-vs-tdd | IMPORTANT | AX-3 | tdd.md | API table under-represents `/sc:tasklist --spec`: current source uses it for Stage-10.5 PRE reflect AND supplementary TDD extraction (§4.1a), source-document enrichment (§4.4a), and Stage-7 supplementary TDD validation. | Expand the `--spec` row to include generation enrichment + Stage-7 supplementary validation; keep the exact-input-contract inconsistency as a separate upstream risk. | `tdd.md:492-500`, `:507-513` vs `commands/tasklist.md:20-85`, `sc-tasklist-protocol/SKILL.md:130-214,246-292,1297-1308,1466-1475`, `cli/tasklist/prompts.py:151-234` | NO |
| F-09 | current-source-vs-tdd | IMPORTANT | AX-2, AX-3 | tdd.md | TDD treats `phase-template.md` as a source-side reference reflecting current shape; current `phase-template.md` still has non-numbered `### Checkpoint:` headings while authoritative `SKILL.md` requires numbered `### T<PP>.<NN> -- Checkpoint:`. The template reference is stale in a way the TDD does not disclose. | Add the `phase-template.md` checkpoint-heading lag to the mirror-lag/open-risk discussion; state authoritative checkpoint shape comes from inline `SKILL.md` until the reference template is updated. | `tdd.md:558-559`, `:870-875`, `:1170-1172` vs `sc-tasklist-protocol/templates/phase-template.md:107-135` | NO |
| F-10 | current-source-vs-tdd | IMPORTANT | AX-5 | tdd.md | P4 describes `gate-results.txt` (one check/line, PASS/FAIL tokens, trailing `GATE: PASS\|FAIL`) as "the existing quality-gate output"; current source has a 20-check pre-write gate but no emitted artifact / line-format contract. The file body is future design, not current behavior. | Reframe the `gate-results.txt` line format as a future artifact contract; do not call it the existing quality-gate output unless a current emitter exists and is cited. | `tdd.md:429-436`, `:599-612`, `:677-678`, `:741`, `:847-850` vs `sc-tasklist-protocol/SKILL.md:1132-1194` | NO |
| F-11 | current-source-vs-tdd | IMPORTANT | AX-1 | tdd.md | OQ-1 still says stale `tests/reflect/` references must be fixed "before pinning the matrix command downstream," but the refreshed validation matrix already pins `uv run pytest tests/cli/reflect/ -v`. Drifts from the M3 fix direction (OQ-1 is upstream-source cleanup, not a matrix-command pin blocker). | Rephrase OQ-1 as upstream-source cleanup only: matrix command is already pinned correctly; the downstream `/task-builder` handoff waits on the stale source references being fixed or formally waived. | `tdd.md:1019-1025` vs `artifacts/refresh-validation-matrix.md` (pinned `tests/cli/reflect/`) | NO |

**Finding count: 11 deduplicated findings.**

---

## Severity Tally (deduplicated)

| Severity | Count | Finding IDs |
|----------|-------|-------------|
| CRITICAL | 3 | F-01, F-06, F-07 |
| IMPORTANT | 8 | F-02, F-03, F-04, F-05, F-08, F-09, F-10, F-11 |
| MINOR | 0 | — |
| **Total** | **11** | |

**Downstream-blocking:** 7 of 11 findings (F-01 … F-07) block downstream implementation-tasklist generation. The 4 tdd-only current-source representational findings (F-08 … F-11) are IMPORTANT clarity/framing defects that do not by themselves block generation, but should be remediated in the same fix cycle since they affect the same document (tdd.md).

---

## PENDING P2/P5 disposition (per spawn requirement)

Per instruction, PENDING P2/P5 are NOT fidelity failures unless a document auto-defaulted them.

- **P2:** The ledger/matrix correctly record P2 as PENDING with no auto-default (report 6, checks 15-16). The flagged P2 findings (F-01/F-02/F-03) are NOT about the PENDING status — they are about the **retained-IF-chosen cap value** (3-total-pass) printed in spec/prd/tdd contradicting the historical post-adversarial cap (2-total-pass). That is a documented-criteria fidelity drift inside the retain-option contract, independent of the human-decision gate. Flagging is therefore correct.
- **P5:** Same pattern. P5 remains PENDING with no auto-default in ledger/matrix. F-04 (spec determinism overclaim + sample mislabel) and F-05 (prd PENDING-without-historical-rejection-rationale) concern the documented retain shape / determinism claims, not the existence of the PENDING gate. No document auto-defaulted P5; no finding is raised merely for P5 being PENDING.

Conclusion: No finding in this consolidation penalizes a PENDING status per se. All P2/P5 findings target document content (cap value, determinism wording, missing departure-rationale).

---

## Per-Output Summary (granularity preserved — not collapsed)

| Output document | Verdict | Findings | Notes |
|-----------------|---------|----------|-------|
| spec.md | **FAIL** (historical) / PASS (current-source) | F-01 (CRITICAL), F-04 (IMPORTANT) | Current-source-clean (report 4, 21/21). Historical fidelity drift on P2 cap + P5 determinism. |
| prd.md | **FAIL** | F-02 (IMPORTANT), F-05 (IMPORTANT) | P2 cap drift + P5 PENDING lacks historical-departure rationale. |
| tdd.md | **FAIL** (historical + current-source) | F-03, F-06, F-07, F-08, F-09, F-10, F-11 | Heaviest defect concentration: P2 cap drift, P3 contract under-spec, invented `StageError`, `--spec` under-rep, stale phase-template, gate-results framing, OQ-1 drift. |
| refresh-requirements-ledger.md | PASS | — | Fidelity-clean vs historical + current source (report 6, 28/28). P2/P5 correctly PENDING, no auto-default. |
| refresh-validation-matrix.md | PASS | — | Fidelity-clean; per-output rows for all 5 outputs; matrix command correctly pinned to `tests/cli/reflect/`. |

---

## Downstream Gate Decision

**BLOCKED.** Implementation-tasklist generation must NOT proceed. 7 downstream-blocking findings (3 CRITICAL, 4 IMPORTANT) remain open across spec.md, prd.md, and tdd.md. tdd.md carries the most defects (7 of 11) and both CRITICALs involving tdd (F-06, F-07). The P2-cap fidelity drift (F-01/F-02/F-03) is a coherent cross-document defect — the historical post-adversarial cap of 2 total passes was systematically replaced with the rejected pre-adversarial 3-total-pass cap in all three product documents — and must be resolved consistently. After remediation, re-run the M4 source-fidelity gate (all six reports) before generation.

---

## QA Complete

**Consolidated verdict:** FAIL
**Deduplicated findings:** 11 (3 CRITICAL, 8 IMPORTANT, 0 MINOR)
**Fixes applied:** 0 (report-only)
