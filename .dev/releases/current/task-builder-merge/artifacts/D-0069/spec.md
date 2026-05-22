# D-0069 — T06.02 Spec: Implement DM-003-M6 7-field schema

**Task:** T06.02 (Phase 6 — M6 Synthetic DNSP on Partition Exhaust)
**Roadmap items:** R-112 (DM-003-M6 — Synthetic DNSP Finding schema M6 implementation per M1 contract-freeze)
**Date:** 2026-05-18
**Status:** PASS
**Tier:** STRICT
**Critical Path Override:** Yes (DM-003 wire shape governs INV-012 composition with FR-CONV.5)
**Confidence:** [█████████-] 90%
**Verification method:** Sub-agent (quality-engineer)
**Sub-Agent Delegation:** Required (executed; report at §6 below)
**Branch:** `feat/hook-sync-and-matcher-fix`
**Pre-edit HEAD:** `edd3ddd docs(task-builder): D-0067 T05.16 MIG-005 evidence + FF governance entry`

---

## 1. Scope

T06.02 implements the **DM-003-M6 7-field synthetic-DNSP-finding emission contract** across the four wrapper sites landed by T06.01 (FR-CONV.6). The M1 contract-freeze enumerates seven fields (roadmap.md L109); prior to T06.02 the wrapper enumerated five fields explicitly (`severity`, `source`, `affected_range`, `evidence`, `recommendation`) and described `dedup_key` + `found_n_times` only as narrative paragraphs. T06.02 elevates `dedup_key` and `found_n_times` to **explicit emission-contract fields** at all four sites so the emission shape is field-for-field congruent with the M1 freeze. The three fixed-value fields (`severity: HIGH`, `source: "synthetic-dnsp"`, `recommendation: "Manual review required — partition agent failed twice on this range"`) are byte-identical against the contract-freeze. `escalation_ladder_exhaust_point` is constrained at the wrapper to the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` per DM-003.dedup_key (R-118) and the M7 vocabulary registry (R-121). The all-agents-fail guard preserved by T06.01 (rf-team-lead.md:417) is unchanged byte-for-byte.

## 2. Inputs

| Input | Path | Role |
|---|---|---|
| M1 DM-003 contract-freeze | `roadmap.md` L109 | Authoritative 7-field schema (`severity:HIGH-fixed; source:synthetic-dnsp-fixed; affected_range:string; evidence:spawn-log-path-or-stub; recommendation:Manual-review-required-fixed; dedup_key:2-tuple-range-exhaust_point; found_n_times:int-default-1`). T01.13 contract-freeze artifact (D-0011) was not separately materialised; per the Phase 1 schema-registry pattern the roadmap row IS the contract-freeze. |
| R-112 task spec | `roadmap.md` L363 | DM-003-M6 implementation row — "all-7-fields-populated" acceptance criterion |
| FR-CONV.6 wrapper (T06.01 baseline) | `SKILL.md` L656-676 + `rf-analyst.md` L70 + `rf-qa.md` L78 + `rf-qa-qualitative.md` L79 | Five-field emission contract + N-1 concurrency wiring + all-agents-fail guard landed by `dfae6cf feat(task-builder): PR-03 DNSP synthetic finding (paradigm-neutral, BASE)`. T06.02 extends to the full 7-field shape. |
| INV-012 composition rule | `SKILL.md` L1061-1075 (D-0059) | Cross-cycle dedup composition. T06.02 makes `dedup_key` + `found_n_times` explicit at the EMISSION site so INV-012's CONSUMPTION rule binds cleanly. |
| R-118 (DM-003.dedup_key) | `roadmap.md` L369 | "canonical wire format YAML list `["<range>", "<exhaust_point>"]`"; exhaust_point closed vocabulary |
| R-119 (DM-003.found_n_times) | `roadmap.md` L370 | "Default 1; increments by 1 on each within-cycle dedup collapse" |
| R-121 (vocabulary) | `roadmap.md` L372 | `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` closed vocabulary; free-form descriptions forbidden |
| D-0068 (T06.01 evidence) | `artifacts/D-0068/evidence.md` | Confirms FR-CONV.6 wrapper preconditions are PASS; T06.02 is the field-shape implementation layer on top |

## 3. Edits (strictly additive — extend existing 5-field bullet list to 7-field bullet list)

### Edit 1 — `src/superclaude/skills/task-builder/SKILL.md` L660-666 (emission contract)

The five existing bullets (`severity`, `source`, `affected_range`, `evidence`, `recommendation`) are preserved BYTE-IDENTICAL. Two new bullets are appended:

- `dedup_key: 2-tuple (assigned_files_range, escalation_ladder_exhaust_point)` — emitted as YAML list `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`; `escalation_ladder_exhaust_point` MUST be drawn from the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` (free-form descriptions rejected by emitter)
- `found_n_times: int, default 1` — increments by 1 on each within-cycle dedup-key collapse (cross-references the existing **Dedup key** paragraph for the cross-cycle composition rule with PR-02 / INV-012)

### Edit 2a — `src/superclaude/agents/rf-analyst.md` L70 (orchestrator-responsibilities bullet)

Single in-place rewrite of the DNSP bullet that prior to the edit enumerated only 5 fields and described dedup_key + found_n_times narratively at the bullet's tail. Post-edit: bullet explicitly enumerates **all 7 fields** in the order of the M1 freeze, naming `dedup_key` (with YAML wire shape + closed vocabulary) and `found_n_times` (with default 1 + within-cycle increment rule) as emission-contract fields rather than as narrative annotation. The "remaining N-1 partitions rather than aborting" + "All-agents-fail still escalates normally (no DNSP)" preservation clauses are kept verbatim.

### Edit 2b — `src/superclaude/agents/rf-analyst.md` L77-86 (Output Format example block)

Two new bullets appended to the example DNSP finding block:

- `**Dedup key:** ["${TASK_DIR}research/[NN]-foo.md, [NN]-bar.md", "retry-2"]` (2-tuple + closed vocabulary parenthetical)
- `**Found N times:** 1` (default + increment-on-collapse parenthetical)

This gives downstream reviewers and emitters a concrete example shape for the 6th and 7th fields, matching the example shape of the existing 5 fields.

### Edit 3 — `src/superclaude/agents/rf-qa.md` L78 (orchestrator-responsibilities bullet)

Symmetric to Edit 2a. The post-edit bullet enumerates the same 7 fields in the same order with identical wire-shape language. The "remaining N-1 partitions rather than aborting" + "All-agents-fail still escalates normally (no DNSP)" preservation clauses are kept verbatim. The L80 sentence about treating the synthetic-dnsp row as a real finding in the Items Reviewed table is preserved byte-identical.

### Edit 4 — `src/superclaude/agents/rf-qa-qualitative.md` L79 (orchestrator-responsibilities bullet)

Symmetric to Edits 2a + 3. The bullet enumerates the same 7 fields in the same order with identical wire-shape language. Additionally, the missing `All-agents-fail still escalates normally (no DNSP)` clause (flagged by D-0068 §6 as a textual-parity follow-up candidate) is added here for parity with rf-analyst.md and rf-qa.md. The `affected_range` description retains the qualitative-path-specific phrasing `<assigned_files / assigned_phases slice verbatim>` because the qualitative partition stream can carry phase-shaped scopes as well as file-shaped scopes.

## 4. Preservation invariants

| Slice | sha256 (pre + post-edit identical) |
|---|---|
| `src/superclaude/agents/rf-team-lead.md:417` (3-cycle hard cap + all-agents-fail escalation backstop — COMP-006-M6 preservation gate, byte-stable end-to-end across PR-02, PR-03, M1–M6) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — no edit anywhere) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |

The four other files (`SKILL.md`, `rf-analyst.md`, `rf-qa.md`, `rf-qa-qualitative.md`) carry strictly-additive edits within the FR-CONV.6 wrapper regions. The five-field portion of the existing emission contract (the three fixed-value fields plus `affected_range` and `evidence`) is preserved byte-identical (re-confirmed in §5 below).

## 5. Fixed-value byte-identity verification

The M1 contract-freeze pins three fields to fixed values. Every post-edit emission site asserts these as literal strings:

| Field | Required literal | Post-edit grep evidence |
|---|---|---|
| `severity` | `HIGH` | `grep -F "severity: HIGH"` returns ≥1 hit in each of: SKILL.md, rf-analyst.md, rf-qa.md, rf-qa-qualitative.md |
| `source` | `"synthetic-dnsp"` | `grep -F 'source: "synthetic-dnsp"'` returns ≥1 hit in each of the same four files |
| `recommendation` | `"Manual review required — partition agent failed twice on this range"` | `grep -F "Manual review required — partition agent failed twice on this range"` returns ≥1 hit in each of the same four files (em-dash `—` is U+2014, byte-identical with the contract-freeze wording) |

Per-file grep counts of all 7 field names are recorded in `evidence.md` §3.

## 6. Sub-agent quality-engineer ratification

A read-only quality-engineer sub-agent was spawned (no Edit / Write / replace_content / replace_symbol_body / insert_*_symbol calls against any source-of-truth file). The sub-agent verified field-for-field that the post-edit emission contract at all four wrapper sites matches the M1 DM-003 contract-freeze schema (roadmap.md L109), confirmed that the three fixed-value fields are byte-identical with the freeze wording, confirmed that `escalation_ladder_exhaust_point` is constrained at the wrapper to the closed vocabulary, and confirmed that the `rf-team-lead.md:417` slice and the FR-CONV.6 preservation clauses (`remaining N-1 partitions rather than aborting`, `All-agents-fail still escalates normally (no DNSP)`) are unchanged. The full report appears in `evidence.md` §5.

## 7. Acceptance criteria coverage

| AC | Statement (verbatim from T06.02 task) | Where verified |
|----|----------------------------------------|----------------|
| AC1 | DM-003 emission has all 7 fields: severity (HIGH), source (synthetic-dnsp), affected_range, evidence, recommendation, dedup_key, found_n_times | `evidence.md` §3 (per-file grep counts for all 7 field names ≥1 across the 4 wrapper sites); §4 (Output Format example block at rf-analyst.md L77-86 now lists 7 bullets) |
| AC2 | Sub-agent quality-engineer report confirms field-for-field match against M1 contract-freeze | `evidence.md` §5 (sub-agent report; overall verdict PASS) |
| AC3 | Diff vs DM-003 spec is byte-identical on fixed-value fields | `evidence.md` §6 (literal-grep evidence for `severity: HIGH`, `source: "synthetic-dnsp"`, and the fixed recommendation string at every wrapper site) |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0069/evidence.md` | This artifact pair |

All four ACs PASS.

## 8. Dependencies and cross-references

- **Dependencies:** T06.01 (D-0068 — FR-CONV.6 wrapper landed at the four edit sites); T01.13 (M1 contract-freeze of DM-003 schema, anchored in roadmap.md L109).
- **Unblocks:**
  - T06.03 (D-0070, severity HIGH + source sentinel emitters — now have explicit field-shape contracts to bind to)
  - T06.04 (D-0071, affected_range + evidence emitters)
  - T06.05 (D-0072, recommendation + dedup_key + found_n_times emitters)
- **Composition with INV-012 (T05.07 / D-0059):** the cross-cycle dedup composition subsection at SKILL.md L1061-1075 references DM-003's `dedup_key` 2-tuple as its bookkeeping identity. T06.02 makes this consumption rule sound by elevating `dedup_key` to an explicit emission field.
- **M6 forward-flow:** T06.07 (API-003-M6 emission), T06.08 (all-agents-fail guard precedence), T06.09 (within/cross-cycle dedup), T06.10 (N-1 concurrency + HIGH non-overridable), T06.11 (SKILL.md A.8 + A.10 merge step), T06.13–T06.14 (per-agent edit-site finalisation), T06.15–T06.16 (test fixtures), T06.17 (MIG-006 landing commit).

## 9. Rollback

Per roadmap R-112 rollback note (M6 standard rollback pattern): T06.02 is strictly additive. Rollback removes the two new bullets (`dedup_key`, `found_n_times`) from SKILL.md L665-666 and reverts the four bullet rewrites (SKILL.md, rf-analyst.md L70, rf-qa.md L78, rf-qa-qualitative.md L79) plus the two new bullets in the rf-analyst.md L85-86 Output Format example block, restoring the 5-field contract landed by T06.01. The all-agents-fail escalation backstop at rf-team-lead.md:417 is unaffected (byte-stable across the edit window).

## 10. Slice hashes (for downstream task verification)

| Slice | sha256 (post-edit) |
|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` (whole file) | `6b500cc5378b2fbc652c4546e344bf6b6105c881bd8447c76fe328b3981270bf` |
| `src/superclaude/agents/rf-analyst.md` (whole file) | `5b7071deeb8428e17aeab9e7d7bb9eea228e5378cce5dbe05d7a240c7b2b621e` |
| `src/superclaude/agents/rf-qa.md` (whole file) | `bb07e1491501db2af3e8bd89edf15335baef37aa68e597a2ab81d9b6e7996563` |
| `src/superclaude/agents/rf-qa-qualitative.md` (whole file) | `866426da72ca8c76ed56fb6c8a32c08b38884bb57b66091e6048251266f5a6a1` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — UNTOUCHED) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |
| `src/superclaude/agents/rf-team-lead.md:417` (3-cycle hard cap — UNTOUCHED) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
