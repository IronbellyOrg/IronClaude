# D-0076 — T06.10 Spec: INV-021 N-1 concurrency + R-126 HIGH severity non-overridable across merge step

**Date:** 2026-05-18
**Task:** T06.10 — Wire R-125 (INV-021 N-1 partition cohort concurrency invariant) + R-126 (HIGH severity non-overridable across merge step; synthetic emits ALONGSIDE — not IN PLACE OF — real findings)
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-125, R-126
**Tier:** STRICT
**Critical Path Override:** No
**Sub-Agent Delegation:** Required (quality-engineer)
**MCP Requirements:** Required: Sequential, Serena
**Deliverable IDs:** D-0076

---

## 1. Purpose

Land the **R-125 INV-021 N-1 cohort concurrency invariant** and **R-126 HIGH severity non-overridable + real-findings preservation invariant** at the 4 FR-CONV.6 wrapper sites established by T06.01–T06.09. T06.10 extends the synthetic-dnsp emitter contract from the per-emission gates (DM-003 ×5 from T06.03/T06.04/T06.05, API-003 ×1 from T06.07) and the cohort-level path-selection gate (R-122 from T06.08) and the cross-emission compositional layer (INV-012 ×2 from T06.09) **upward to the execution-layer + merge-step layer** — the layer where cohort-wide parallelism (during emission) and post-emission severity / count preservation (during merge at SKILL.md §A.8 / §A.10) emerge as cross-cutting invariants that no per-emission or per-cohort-path gate can detect.

## 2. Scope

### 2.1 In scope

- **R-125 (INV-021).** When one partition's escalation ladder exhausts, the orchestrator MUST allow the remaining N-1 sibling partitions to continue executing concurrently to their own success-or-exhaust terminal state **BEFORE** the exhausted partition's synthetic-dnsp emission is composed AND **BEFORE** the merge step at SKILL.md §A.8 / §A.10 runs (explicit merge-step pick-up wiring lands at T06.11 / R-127 + R-128). The exhausted partition's synthesis MUST NOT block, pause, serialize, or reduce the parallelism of the sibling cohort. Spawn-log timestamps are the evidence vehicle for the invariant.
- **R-126 (HIGH severity non-overridable across merge step + real findings preserved alongside synthetic).**
  - **HIGH severity non-overridable at the merge-step layer.** The per-emission `DM-003-fixed-field-invariant-violation` gate from T06.03 enforces `severity: HIGH` non-override at the emission boundary; T06.10 extends the invariant **transitively across the cohort-level merge step** at SKILL.md §A.8 / §A.10. No merge-time normalization, severity-downgrade transform, severity-coalesce rule, or operator-overridable severity flag is permitted to lower the synthetic-dnsp severity below HIGH.
  - **Real findings preserved alongside synthetic.** The synthetic-dnsp block MUST be merged ALONGSIDE the real findings from the successful partitions (Path B from T06.08), **never IN PLACE OF** them. The cohort's real-finding count post-merge MUST equal the cohort's real-finding count pre-merge plus the synthetic count (strictly additive — not replacement, coalesce, or filter).
- **Three new named rejection symbols:**
  1. `INV-021-cohort-serialization-violation` — sibling cohort paused awaiting exhausted-partition synthesis; spawn-log timestamps show serialization of the N-1 partitions behind the exhausted partition's synthesis; the parallel-research invariant NFR-CONV.10 is degraded for the exhausted-partition case.
  2. `R-126-real-findings-replacement-violation` — a real finding is dropped during the merge step; a real finding is coalesced into a synthetic finding; the cohort's real-finding count post-merge is strictly less than the real-finding count pre-merge; merge logic replaces a real finding with a synthetic one when both share a severity bucket.
  3. `R-126-severity-override-violation` — merge-time severity-downgrade transform reduces synthetic-dnsp severity below HIGH; merge-time severity-coalesce rule overrides synthetic-dnsp severity from HIGH to another bucket; an operator override flag is honored to lower synthetic-dnsp severity.

### 2.2 Out of scope (deferred to downstream tasks)

- Programmatic spawn-log-timestamp fixture proving N-1 partitions overlap with synthesis step — lands at **T06.16 / D-0081 (TEST-021 cohort-concurrency fixture)**.
- Merge-step pick-up wiring at SKILL.md §A.8 (`:572-656`) and §A.10 (`:870-918`) — lands at **T06.11 / D-0077 (R-127 + R-128)**.
- MIG-006 single-commit landing — at **T06.17 / D-0082**.
- FF_SYNTHETIC_DNSP_EMISSION governance entry + NFR-CONV.10 governance reference for M7 — at **T06.17 / D-0082**.

## 3. Wire-shape additions

T06.10 adds **one new clause** to the FR-CONV.6 wrapper at 4 sites. The clause anchor is:

```
**INV-021 N-1 cohort concurrency + R-126 HIGH severity non-overridable across merge step (R-125 + R-126).**
```

At the 3 agent files (`rf-analyst.md`, `rf-qa.md`, `rf-qa-qualitative.md`), the clause is **appended within the existing DNSP wrapper bullet** at the end of the T06.09 clause (no new bullet introduced — preserves the bullet-count of the "Orchestrator Responsibilities" list).

At `SKILL.md`, the clause is **inserted as a new paragraph** between the T06.09 paragraph (currently L682) and the existing inline "Dedup key (composition with PR-02 Retry Monotonicity, INV-012)" paragraph (previously L684, shifted to L686 by T06.10's insertion). The SKILL.md version carries a 3-part rationale tail; the agent-file versions do not (matching the T06.07 / T06.08 / T06.09 wrapper-density convention).

## 4. Symbol hierarchy after T06.10

The Phase 6 rejection-symbol hierarchy now spans **five tiers** (Phase 6 adds the 5th tier; the symbol tally goes from 9 to 12):

| Tier | Layer | Symbols | Source Task |
|---|---|---|---|
| 1 | Per-emission field-shape (fixed) | `DM-003-fixed-field-invariant-violation` | T06.03 |
| 1 | Per-emission field-shape (dynamic) | `DM-003-dynamic-field-invariant-violation` | T06.04 |
| 1 | Per-emission field-shape (recommendation) | `DM-003-recommendation-invariant-violation` | T06.05 |
| 1 | Per-emission field-shape (dedup_key tuple) | `DM-003-dedup-key-shape-violation` | T06.05 |
| 1 | Per-emission field-shape (counter) | `DM-003-found-n-times-invariant-violation` | T06.05 |
| 2 | Per-emission wire-shape | `API-003-exhaust-point-vocabulary-violation` | T06.07 |
| 3 | Cohort-level path-selection | `R-122-guard-precedence-violation` | T06.08 |
| 4 | Cross-emission compositional layer | `INV-012-within-cycle-collapse-violation` | T06.09 |
| 4 | Cross-emission compositional layer | `INV-012-cross-cycle-composition-violation` | T06.09 |
| **5** | **Execution-layer + merge-step layer** | **`INV-021-cohort-serialization-violation`** | **T06.10 (NEW)** |
| **5** | **Execution-layer + merge-step layer** | **`R-126-real-findings-replacement-violation`** | **T06.10 (NEW)** |
| **5** | **Execution-layer + merge-step layer** | **`R-126-severity-override-violation`** | **T06.10 (NEW)** |

Operator tooling can grep any of the 12 symbols to scope a failure to its emergence boundary without false positives across the layers.

## 5. Acceptance criteria

| AC | Criterion |
|---|---|
| AC1 | T06.10 clause anchor (`INV-021 N-1 cohort concurrency + R-126 HIGH severity non-overridable across merge step (R-125 + R-126)`) present at ≥1 per file at the 4 wrapper sites. |
| AC2 | `INV-021-cohort-serialization-violation` named symbol present at ≥1 per file at the 4 wrapper sites. |
| AC3 | `R-126-real-findings-replacement-violation` named symbol present at ≥1 per file at the 4 wrapper sites. |
| AC4 | `R-126-severity-override-violation` named symbol present at ≥1 per file at the 4 wrapper sites. |
| AC5 | R-125 invariant unambiguous (N-1 sibling partitions continue concurrently; synthesis does NOT block/pause/serialize; spawn-log timestamps are evidence vehicle). |
| AC6 | R-126 invariant unambiguous (synthetic merges ALONGSIDE real findings, never IN PLACE OF; cohort real-finding count post-merge = pre-merge + synthetic count; HIGH severity non-overridable across merge step in addition to per-emission DM-003 gate). |
| AC7 | NFR-CONV.10 parallel-research invariant binding present at the 4 wrapper sites. |
| AC8 | COMP-006-M6 preservation gate — `rf-team-lead.md` whole-file sha256 = `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`; line-417 sha256 = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`; `git diff` empty. |
| AC9 | T05.07 INV-012 subsection content byte-identical (sha = `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`); line-range citation updated from `L1077-1091` to `L1079-1093` at all 4 wrapper sites (the sha pin remains the byte-stability invariant per D-0075 §10 convention). |
| AC10 | Strict additivity — all 9 prior named rejection symbols preserved at ≥1 per file (no removal, no count reduction). |
| AC11 | Sync parity — `make sync-dev` clean; `diff -q src/superclaude/<file> .claude/<file>` returns empty for all 4 wrapper files. |
| AC12 | Sub-agent quality-engineer report: PASS on all 12 verification checks. |
| AC13 | Evidence at `TASKLIST_ROOT/artifacts/D-0076/evidence.md`. |

## 6. Roadmap traceability

| Roadmap Item | Description | T06.10 binding |
|---|---|---|
| R-125 | INV-021: on one partition's escalation exhaust, N-1 sibling partitions continue concurrently to completion before exhausted one synthesises finding | `INV-021-cohort-serialization-violation` named symbol; per-cohort N-1 concurrency invariant clause |
| R-126 | HIGH severity: synthetic findings emit ALONGSIDE (not in place of) real findings from successful partitions | `R-126-real-findings-replacement-violation` + `R-126-severity-override-violation` named symbols; strictly-additive merge invariant + merge-step non-overridable HIGH invariant |

## 7. Dependencies (closed)

- T06.09 / D-0075 PASS (INV-012 within-cycle + cross-cycle dedup composition).
- T06.08 / D-0074 PASS (R-122 all-agents-fail guard precedence — the upstream Path B gate that T06.10's real-findings-preservation invariant binds to).
- T06.07 / D-0073 PASS (API-003-M6 + closed exhaust-point vocabulary).
- T06.03 / D-0070 PASS (DM-003 severity + source fixed-field — the per-emission `severity: HIGH` gate that T06.10 transitively extends across the merge step).

## 8. Rollback

Per roadmap rollback contract: remove the T06.10 clause from the 4 wrapper sites; the all-agents-fail escalation (Path A from T06.08, rf-team-lead.md:417) remains intact regardless. Rollback is byte-additive (the T06.10 clause is an append at the end of the DNSP wrapper bullet at agent files and a new paragraph at SKILL.md; removing it returns the wrapper to its post-T06.09 state).

## 9. Provenance

- Pre-edit HEAD: `5439ea1 feat(hooks): widen auggie-flag-clear matcher to mcp__auggie-mcp__; add verify-sync hook coverage and cross-consistency checks` (same baseline as T06.01–T06.09 — MIG-006 single-commit landing scheduled for T06.17).
- M1 contract-freeze references: roadmap.md R-125 row + R-126 row.
- T05.07 / D-0059 — INV-012 cross-cycle dedup composition operational rule (referenced via sha pin `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` at new line range L1079-1093).
- T06.08 / D-0074 — R-122 all-agents-fail guard Path B (upstream guard precedence).
- D-0075 §10 (Observations) — established the line-range-update + sha-pin-stability convention for T06.10..T06.18.

## 10. Pin hashes (frozen at T06.10 close)

| Slice | sha256 |
|---|---|
| `src/superclaude/agents/rf-team-lead.md` (whole file — UNCHANGED) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |
| `src/superclaude/agents/rf-team-lead.md:417` (UNCHANGED) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `src/superclaude/skills/task-builder/SKILL.md` INV-012 operational rule subsection L1079-1093 (content UNCHANGED; line range shifted +2 from T06.09 baseline) | `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` |
| `src/superclaude/agents/rf-analyst.md` (whole file — post-T06.10) | `8d41ae8038769bb32eb56db78569235614c82aa3dc2170886237797ed9f8ff43` |
| `src/superclaude/agents/rf-qa.md` (whole file — post-T06.10) | `fd2487860810d163f7c19263f830f08bcf4b9efede1bf89ed8c2ea9184ddc6e9` |
| `src/superclaude/agents/rf-qa-qualitative.md` (whole file — post-T06.10) | `ed35b7884db1a2d6dfe1aa8a8bddb9b3308d4b268ba4892ad39956d6149883a1` |
| `src/superclaude/skills/task-builder/SKILL.md` (whole file — post-T06.10) | `4b2ead830f6708cdfd5efcf111285d7f48263f512eac3a0a8c672810c0db4c0b` |
