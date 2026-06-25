# Synthesis Quality Review — Report A (Partition 1 of N)

**Analyst:** rf-analyst | **Mode:** synthesis-review | **fix_authorization:** false (report-only)
**Stance:** ADVERSARIAL (find problems)
**Date:** 2026-06-20
**Task:** TASK-TDD-20260619-235400 (FR-RH2 Headless Ensemble Fix TDD)

**Assigned files (3):**

- `synthesis/synth-01-exec-problem-goals.md` (TDD §1–4)
- `synthesis/synth-02-requirements.md` (TDD §5)
- `synthesis/synth-03-architecture.md` (TDD §6)

**Cross-check sources:** `research/00-prd-extraction.md`, `research/reuse-audit.yaml`, `research/01-reflect-runner-seam.md` (via live code re-verification), template `src/superclaude/examples/tdd_template.md`, and shipped source under `src/superclaude/cli/{reflect,swarm}/`.

> **[PARTITION NOTE]** This report covers only the 3 assigned synthesis files (§1–6). Cross-file consistency checks (criterion 7) are applied within this subset plus against research/template. Full cross-synthesis consistency (e.g., §22 Open Questions in synth-09 actually receiving the items synth-01 defers to it) requires merging with the partition(s) covering synth-04..synth-09.

---

## Overall Verdict: **PASS** (0 blocking issues; 3 minor advisories)

All three assigned synthesis files pass the 9-criteria Synthesis Quality Review plus the reuse-audit subsection check. Findings are evidence-cited, spec-traced, and grounded against shipped code re-verified during this review. No fabrication detected. Three minor advisories are recorded below — none blocks assembly; all are cosmetic/forward-looking.

| File | Verdict |
|------|---------|
| synth-01-exec-problem-goals.md | PASS |
| synth-02-requirements.md | PASS |
| synth-03-architecture.md | PASS |

---

## Criterion-by-Criterion (across all 3 files)

### (1) Template headers match `tdd_template.md` sections — PASS

| Synth file | Claims TDD § | Template section (line) | Match |
|-----------|-------------|------------------------|-------|
| synth-01 | §1 Executive Summary | §1 (L199) | OK |
| synth-01 | §2 Problem Statement & Context | §2 (L211) | OK |
| synth-01 | §3 Goals & Non-Goals | §3 (L237) | OK |
| synth-01 | §4 Success Metrics | §4 (L270) | OK |
| synth-02 | §5 Technical Requirements (5.1/5.2) | §5 (L293), 5.1 (L295), 5.2 (L304) | OK |
| synth-03 | §6 Architecture (6.1/6.2/6.3/6.4) | §6 (L362), 6.1 (L364), 6.2 (L374), 6.3 (L386), 6.4 (L394) | OK |

Sub-section headers align with the template. synth-01 §2 is titled "Business / Engineering Context" vs template's "2.3 Business Context" (L227) — a justified rename (this is an internal eng fix with no product PRD), explicitly stated in the body. Not a defect.

**Header numbering note (advisory, not a failure):** synth-03 renders §6.6 (Reuse & Consolidation Audit) and §6.7 (Architecture Status Note) but skips §6.5. The template's §6.5 is **Multi-Tenancy Architecture *(if applicable — SaaS/platform components)*** (L404), which the template explicitly says to "Skip … for single-tenant, internal, or purely frontend components." This is a CLI reliability fix, so the skip is correct. However, §6.6/§6.7 are non-template section numbers (the template's §6 stops at 6.5). This is acceptable as a synthesis-stage local numbering, but the assembler should renumber to avoid a §6.5 gap in the final TDD. → **Advisory A1.**

### (2) Correct table column structures — PASS

| Table | Expected columns (template) | synth columns | Match |
|-------|----------------------------|---------------|-------|
| §3.1 Goals (synth-01) | ID / Goal / Success Criteria (L243) | ID / Goal / Success Criteria | OK |
| §3.2 Non-Goals (synth-01) | ID / Non-Goal / Rationale (L253) | ID / Non-Goal / Rationale | OK |
| §3.3 Future (synth-01) | Item / Target Phase / Notes (L263) | Item / Target Phase / Notes | OK |
| §4.1 Tech Metrics (synth-01) | Metric / Current State / Target / Measurement Method (L276) | Metric / Current State / Target / Measurement Method | OK |
| §5.1 FRs (synth-02) | ID / Requirement / Priority / Acceptance Criteria (L297) | ID / Requirement / Priority / Acceptance Criteria / **Source** | OK + extra `Source` col |
| §6.4 Key Decisions (synth-03) | Decision / Choice / Rationale / Alternatives Considered (L398) | Decision / Choice / Rationale / Alternatives Considered | OK |
| §6.3 Boundaries (synth-03) | Boundary / Description / Protocol (L388) | Boundary / Description / Protocol / Contract | OK (Protocol/Contract merged-label) |

The §5.1 FR table adds a `Source` column (maps each FR-001..009 to its FR-RH2.N origin). This is an additive traceability column, not a structural violation — it strengthens auditability. The §5.2 NFRs use the template's "Attribute / Detail" per-NFR block form rather than a single multi-row table; both are valid template renderings of NFRs and each carries the required **Measurement method** row. PASS.

### (3) No fabrication beyond research files — PASS (sampled + traced)

Sampled claims traced to a research file or shipped source:

| Sampled claim | Synth | Traced to | Verdict |
|---------------|-------|-----------|---------|
| `_audit_once` at runner.py:392-428; `expected_tier` computed in that block | synth-01 §1, synth-03 §6.1 | **Live code:** `runner.py` `expected_tier = 2 if config.depth in {"standard","deep"} else 1` present in `_audit_once`; parse+derive tail (`parse_contract`→`derive_verdict`) present | VERIFIED |
| reflect pkg is 6 files, `ensemble.py` absent | synth-01 §2.1, synth-03 §6.7 | **Live:** `ls src/superclaude/cli/reflect/` = commands/config/contract/__init__/models/runner.py (6); no ensemble.py | VERIFIED |
| `mechanical_merge` 8 LOC, header `## From {model_label} ({elapsed_ms}ms)` | synth-03 §6.2 | **Live:** `merge.py:50` def; `:55` header `f"## From {wr.model_label} ({wr.elapsed_ms}ms)"` | VERIFIED |
| success predicate `status == "success"` (M over N) | synth-01 §4, synth-02 §5.2.5, synth-03 §6.1 | **Live:** `dispatch.py:496` `success_count = sum(1 for r in results if r.status == "success")` | VERIFIED |
| `dispatch_wave1` sync `def`, `transport_for_slot` factory param | synth-03 §6.2/§6.4 | **Live:** `dispatch.py:334` plain `def dispatch_wave1(... transport_for_slot: Optional[Callable[[int], Transport]] ...)` | VERIFIED |
| `ModelPoolTooSmallError` (L589) raised when pool < N; factory L612 private | synth-03 §6.1/§6.4 D1 | **Live:** `commands.py:589` class; `:612` `def _resolve_run_transport_factory`; `:688` raise | VERIFIED |
| reuse-audit: 4 candidates, 8 neighbours, max overlap 0.81, all maybe-related, no centralize | synth-03 §6.6 | `reuse-audit.yaml` L2-6 (`candidates_scanned:4`, `neighbours_found:8`, `max_overlap:0.81`, `degraded:[]`, `sampled:false`); 4 findings all `tier: maybe-related`, `recommend_centralize:false` | VERIFIED |
| FR-RH2.4 diversity over distinct `model_id`s of M survivors | synth-01 §4, synth-02 FR-004 | `00-prd-extraction.md` L83 (verbatim) | VERIFIED |
| (M,N) guard table M==0→blocked/2/ensemble-empty … M≥2∧≥2cls→pass/0 | synth-01 §4, synth-02 §5.4 | `00-prd-extraction.md` L198-203 | VERIFIED |

No invented file paths, line numbers, or contract fields found in the sample. Every distinctive numeric/structural claim re-grounds against either a research file or live source. PASS.

### (4) Evidence cites actual file paths — PASS

Every architectural assertion in synth-03 carries a `file:line` citation and a `[CODE-VERIFIED]` tag. synth-01 §2.2 includes a dedicated Evidence Table (6 rows, each with `Source (file:line)`). synth-02 cites FR-RH2.N / NFR-RH2.N for all 9 FRs + 8 NFRs and adds line anchors for CLI wiring (`commands.py:101-106`). Citations sampled above resolve to real lines. PASS.

### (5) Architecture includes a diagram — PASS

synth-03 contains **two** diagrams:

- §6.1 High-Level Architecture: ASCII data-flow diagram (the seam → ensemble.py → swarm → /sc:adversarial → reflect contract → verdict).
- §6.2 Component Diagram: a `mermaid graph TD` module-dependency graph with edge-nature narrative table.

Both exceed the template's minimum (template §6.1 asks for one diagram, §6.2 provides a mermaid stub). PASS.

### (6) FR-001/NFR-001 ID numbering + priority + acceptance criteria — PASS

- synth-02 §5.1: FR-001..FR-009, each with **Priority** (`Must Have`) and **Acceptance Criteria** in Given/When/Then form. Matches template L297-302 (`FR-001`, `Must Have`, Given/When/Then). The FR-001..009 ↔ FR-RH2.1..9 mapping is explicit (FR-005↔FR-RH2.9, FR-008↔FR-RH2.7, FR-009↔FR-RH2.8) with the spec-ordering rationale stated.
- synth-02 §5.2: NFR blocks 5.2.1..5.2.8, each 1:1 to NFR-RH2.1..8 with explicit Measurement method.

Spec-trace coverage claim ("no `[NO SPEC TRACE]` gaps") independently confirmed against `00-prd-extraction.md §2/§3`: all 9 FRs and 8 NFRs have a real spec source. PASS.

### (7) Cross-references consistent (within assigned subset) — PASS

- synth-01 §3 G3 ("score via sc-adversarial Mode A, not swarm merge") ↔ synth-02 FR-003 ↔ synth-03 §6.4 D3 — consistent.
- synth-01 §4 (M,N) table ↔ synth-02 §5.4 guard table ↔ synth-03 §6.1 "diversity over M, not N" — identical verdict/exit-code/slug rows; no drift.
- synth-01 §3 NG3 (swarm merge stays mechanical) ↔ synth-02 FR-003 AC ↔ synth-03 §6.2 boundary invariant — consistent.
- synth-02 §5.3 path-confinement (two `return-contract.yaml`) ↔ synth-03 §6.1 path-confinement B — consistent.
- **Forward cross-ref (deferred, see partition note):** synth-01 §5/§3.3 and synth-03 §6.4 D1 note defer the public-transport-factory coupling and diversity-pool reconciliation **to §22 Open Questions** (a synth-04..09 file). synth-01 L103-105 and synth-03 L188 explicitly route these to §22. This report cannot confirm §22 actually receives them — flagged for the merge step. → **Advisory A2.**

### (8) No doc-only / `[UNVERIFIED]` claims asserted as fact in §6 — PASS

synth-03's evidence rule (L9) states net-new components are marked **NET-NEW** and only `[CODE-VERIFIED]` findings are asserted as current architecture. Verified by inspection:

- `ensemble.py`, `reflect_review.py`, output template, stub test are all labelled **NET-NEW**.
- §6.4 D5 / §6.7 mark the wiring "does not yet exist in code".
- The one `[CODE-CONTRADICTED]` item (no public swarm transport-factory API) is surfaced as a coupling **smell** in §6.4 D1 supporting note — NOT asserted as a benign fact — and routed to §22. This is the correct handling.

No `[UNVERIFIED]` claim is stated as fact in §6. PASS.

### (9) Stale-doc discrepancies surfaced, not buried — PASS

The single `[CODE-CONTRADICTED]` finding ("public swarm transport-factory equivalent exists" → contradicted; both `_resolve_run_transport` L510 and `_resolve_run_transport_factory` L612 are private) is surfaced in **three** places: synth-01 §3.3 (Future Considerations, deferred to §22), synth-03 §6.4 D1 supporting note, and the §6.2 edge table ("private symbol — coupling smell — see §6.4"). It is explicitly tagged `[CODE-CONTRADICTED]` and re-confirmed during this review (live: `grep` shows `_resolve_run_transport_factory` is `_`-prefixed/private). Surfaced prominently, not buried. PASS.

---

## Reuse & Consolidation Audit subsection (synth-03 §6.6) — PASS

The "Reuse & Consolidation Audit" subsection **is present** in synth-03 (§6.6) and is faithfully rendered from `research/reuse-audit.yaml`:

| Check | reuse-audit.yaml | synth-03 §6.6 | Match |
|-------|------------------|---------------|-------|
| stage | `pre` | "stage: pre" | OK |
| candidates_scanned | 4 | "4 candidates scanned" | OK |
| neighbours_found | 8 | "8 neighbours found" | OK |
| max_overlap | 0.81 | "max overlap 0.81" | OK |
| degraded / sampled | `[]` / `false` | "degraded: [], sampled: false" | OK |
| ensemble.py verdict | `reuse-by-import` conf 0.88 | reuse-by-import (conf 0.88) | OK |
| reflect_review.py | `mirror-shape` conf 0.84 | mirror-shape (conf 0.84) | OK |
| output template | `mirror-shape` conf 0.79 | mirror-shape (conf 0.79) | OK |
| stub test | `mirror-shape` conf 0.81 | mirror-shape (conf 0.81) | OK |
| no L3 confident-duplicate banner | all maybe-related | "no confident-duplicate banner fires" | OK |
| recommend_centralize | false (all 4) | "recommend_centralize is false for every row" | OK |

One row per proposed component (4 rows), tier/verdict/disposition columns all present, detection-only framing preserved. The DIRECTIVE D4 recipe-binding note (reuse `bare-review-v1`, validator assertions 2 & 6 satisfied with zero recipe edits) was independently spot-checked: `bare_review.py` confirms `recipe_name="bare-review-v1"`, `normalizer_strategy="bare-review-v1"`. PASS.

---

## Advisories (non-blocking)

| ID | Severity | File | Issue | Recommended fix (for assembler/author — NOT applied; report-only) |
|----|----------|------|-------|------------------------------------------------------------------|
| A1 | Minor (cosmetic) | synth-03 | §6.6/§6.7 are non-template section numbers; the template §6 stops at §6.5 (Multi-Tenancy, correctly skipped). Final TDD would show a §6.5 gap. | At assembly, renumber the Reuse & Consolidation Audit and Architecture Status Note (e.g., fold into §6.5/§6.6 sequentially, or place Reuse Audit as a labelled subsection under §6.4) so the final TDD has no numbering gap. |
| A2 | Minor (cross-file, unverifiable in this partition) | synth-01, synth-03 | Three items are deferred to "§22 Open Questions" (public-transport-factory coupling, diversity-pool reconciliation, OI-3 stub auto-select). §22 lives in another synth file. | Merge step must confirm the §22-owning synth file actually contains these three deferred items; otherwise they fall through the cracks (criterion 7 cross-ref break). |
| A3 | Minor (precision) | synth-03 §6.6 | The reuse-audit `bare_review.py:66` neighbour snippet is truncated to `/sc:adversarial --compare {compare_files}` (the YAML stores only the first line). The synth narrative correctly states the template contains `{suspect_files}`; live code confirms the full template is `--compare {compare_files} --suspect-source {suspect_files}`. No correction needed in the synth — recorded so the assembler does not "fix" the synth to match the truncated YAML snippet. | None required. The synth is more accurate than the YAML snippet. Do not regress it. |

---

## Summary

- **Files reviewed:** 3 / 3 assigned
- **Files passed:** 3
- **Files failed:** 0
- **Blocking issues:** 0
- **Minor advisories:** 3 (A1 cosmetic renumber, A2 cross-file §22 verification, A3 precision note)
- **Fabrication:** none detected (9 distinctive claims sampled, all traced to research or live source)
- **Reuse & Consolidation Audit subsection:** PRESENT and faithful to reuse-audit.yaml

**Gate recommendation:** PASS this partition. The three assigned files are assembly-ready. Advisory A2 (§22 deferral verification) should be discharged by the partition-merge step that has visibility into synth-04..synth-09; advisory A1 (§6.5 numbering gap) should be handled by the assembler during final TDD assembly.
