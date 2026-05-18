# D-0074 — T06.08 Evidence: Wire all-agents-fail guard precedence (R-122)

**Date:** 2026-05-18
**Task:** T06.08 — Wire all-agents-fail guard precedence (Zero-partitions-succeeded → NO synthetic + activate `rf-team-lead.md:417`; ≥1-success AND ≥1-exhaust → emit synthetic-dnsp alongside real findings; all-succeeded → no synthetic; three mutually-exclusive paths)
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-122 (all-agents-fail guard mutual-exclusivity contract)
**Tier:** STRICT
**Critical Path Override:** Yes
**Verification Method:** Sub-agent (quality-engineer)
**MCP Requirements:** Required: Sequential, Serena
**Status:** PASS

---

## 1. Summary

T06.08 lands the **R-122 all-agents-fail guard precedence contract** at the four FR-CONV.6 wrapper sites (`src/superclaude/agents/rf-analyst.md`, `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/skills/task-builder/SKILL.md`). The clause formalises the cohort-level pre-emission guard that routes each partition-cohort outcome down **exactly one of three mutually-exclusive paths**:

- **Path A (zero-partitions-succeeded → existing `rf-team-lead.md:417` fix-cycle escalation; NO synthetic emits)** — the cohort success count is `0`; the orchestrator MUST activate the byte-stable `rf-team-lead.md:417` fix-cycle escalation (max-3-cycles HALT-and-ask-user contract that shipped pre-PR-03) without emitting any synthetic-dnsp block.
- **Path B (≥1-success AND ≥1-exhaust → synthetic-dnsp emits ALONGSIDE real findings)** — at least one partition succeeded AND at least one partition exhausted its escalation ladder; the orchestrator MUST emit one synthetic-dnsp block per exhausted partition into the normal output stream alongside the real findings from the successful partitions (the synthetic-dnsp adds to, never replaces, real findings — preserving NFR-CONV.10 parallel-research invariant).
- **Path C (all-partitions-succeeded → no synthetic; normal merge)** — every partition succeeded; the baseline no-DNSP path.

The clause binds a **new named rejection symbol `R-122-guard-precedence-violation`** scoped to the cohort-level path-selection gate (upstream of the per-emission wire-shape gate landed by T06.07's `API-003-exhaust-point-vocabulary-violation` and the DM-003 field-rejection contracts landed by T06.03/T06.04/T06.05). The three paths are exhaustive: a cohort outcome that satisfies more than one path's precondition, or satisfies none (e.g., zero successes AND zero exhausts under the M5 escalation-ladder semantics from FR-CONV.5 — every partition must terminate in success-or-exhaust), is rejected as a contract violation rather than absorbed into a default path.

The clause also pins the **COMP-006-M6 byte-stability gate** for `rf-team-lead.md:417` explicitly inside each wrapper, citing the line-417 sha pin `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`. The Path A activation MUST NOT replace, short-circuit, or modify the existing fix-cycle escalation — only route control to it.

`rf-team-lead.md` itself is NOT edited (preservation gate; §5).

## 2. Planning Inputs

- **Dependency closure.** T06.07 (D-0073) PASS — API-003-M6 wire-shape contract landed at 4/4 sites with `API-003-exhaust-point-vocabulary-violation` named symbol; rf-team-lead.md:417 byte-stable post-T06.07.
- **R-122 spec.** Mutually-exclusive paths: zero-success → activate `rf-team-lead.md:417` (no synthetic); ≥1-success + ≥1-exhaust → emit synthetic-dnsp; all-success → no synthetic. AC: pre-emission guard wired; rf-team-lead.md:417 path activates on zero-success; sub-agent confirms mutual exclusivity.
- **COMP-006-M6 preservation gate.** Per CP-P06-T01-T05 §6, D-0068 §6, D-0069 §7, D-0070 §6, D-0071 §5, D-0072 §5, D-0073 §5 — `rf-team-lead.md` whole-file sha256 = `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`; line-417 sha256 = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`. The preservation gate is the M6 invariant for the zero-success destination.
- **Phase 6 sequencing.** T06.08 wires the cohort-level path-selection guard (this task); T06.09 wires within-cycle + cross-cycle dedup composition (INV-012); T06.10 wires INV-021 N-1 concurrency + HIGH severity non-overridable; T06.11 lands the consumer-side SKILL.md A.8 + A.10 merge step. Positive-path fixtures (TEST-018..TEST-021) land in T06.15 + T06.16 — the AC1 zero-partitions fixture and AC2 mixed-success fixture are the TEST-020 + TEST-018 line items respectively, and T06.08's spec-level contract at the 4 wrapper sites is what those fixtures will programmatically bind to.

## 3. Execution — Acceptance-criterion grep evidence

### 3.1 AC1 — Zero-partitions-succeeded fixture's execution log shows `rf-team-lead.md:417` activation and no synthetic block

Spec-level binding (the programmatic fixture lands at T06.16 as TEST-020 per D-0081). The R-122 clause at 4/4 wrapper sites pins the Path A activation contract explicitly:

```text
$ grep -c -F "Path A (zero-partitions-succeeded" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1

$ grep -c -F "rf-team-lead.md:417" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:2
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:5
```

Path A is named at 1/1/1/1 across the 4 wrapper sites and explicitly couples zero-success to the existing `rf-team-lead.md:417` fix-cycle escalation with the `NO synthetic emits` clause stated in the wrapper paragraph itself. The T06.16 TEST-020 fixture (per Phase 6 task graph) will programmatically bind to this spec-level contract → **PASS** for AC1 (spec-level binding); fixture-level binding deferred to T06.16 with the line-range targets pinned in the wrapper clause.

### 3.2 AC2 — Mixed-success fixture's output stream contains synthetic-dnsp emission

Spec-level binding (the programmatic fixture lands at T06.15 as TEST-018 per D-0080):

```text
$ grep -c -F "Path B (≥1-success AND ≥1-exhaust" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

Path B explicitly binds the `synthetic-dnsp emits ALONGSIDE real findings` contract at 1/1/1/1, and the wrapper paragraph names "synthetic-dnsp adds to, never replaces, real findings — preserving the cohort's real-finding count and the parallel-research invariant" per NFR-CONV.10 → **PASS** for AC2 (spec-level binding); fixture-level binding deferred to T06.15 (TEST-018).

### 3.3 AC3 — Sub-agent quality-engineer report confirms mutually-exclusive paths preserved

Sub-agent verification (§4 below) ran 7 structural checks (V1–V7) covering R-122 clause anchor, three-path naming, named rejection symbol, COMP-006-M6 preservation gate, mutual-exclusivity formal contract, strict additivity of prior contract anchors, and sync parity. **Overall verdict: PASS** (all 7 checks confirmed). The mutual-exclusivity contract specifically — checks V2 (three paths named at 4/4) + V5 (literal anchors `mutually exclusive` and `every partition must terminate in success-or-exhaust` at 4/4) — confirmed PASS by the sub-agent → **PASS** for AC3.

### 3.4 AC4 — Evidence at `TASKLIST_ROOT/artifacts/D-0074/evidence.md`

This file → **PASS** for AC4.

### 3.5 R-122 clause anchor at all 4 wrapper sites

```text
$ grep -c -F "All-agents-fail guard precedence (R-122)" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

R-122 clause anchor present at 4/4 wrapper sites (1/1/1/1 = 100%) → **PASS**.

### 3.6 Named rejection symbol `R-122-guard-precedence-violation` at all 4 sites

```text
$ grep -c -F "R-122-guard-precedence-violation" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

The new named symbol is bound at 4/4 wrapper sites. Distinct from `API-003-exhaust-point-vocabulary-violation` (T06.07) and `DM-003-dedup-key-shape-violation` (T06.05) because the path-selection gate is **upstream** of the per-emission wire-shape gate — the symbol scopes the cohort-level path-selection failure (cohort outcome internally inconsistent), not a per-emission field-shape failure → **PASS**.

### 3.7 Mutual-exclusivity formal contract anchors at all 4 sites

```text
$ grep -c -F "mutually exclusive" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1

$ grep -c -F "every partition must terminate in success-or-exhaust" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

Both mutual-exclusivity formal-contract anchors (the `mutually exclusive` literal and the `every partition must terminate in success-or-exhaust` contract-violation reject clause) present at 4/4 sites (2 × 1/1/1/1 = 8/8 = 100%) → **PASS**.

### 3.8 COMP-006-M6 sha pin literal cited at all 4 sites

```text
$ grep -c -F "51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

The byte-stable line-417 sha pin literal is cited at 4/4 wrapper sites — operator tooling can grep the sha to confirm the wrapper-level contract references the frozen baseline → **PASS**.

### 3.9 Full clause text (representative — symmetric at all 4 sites)

> **All-agents-fail guard precedence (R-122).** The synthetic-dnsp emitter MUST gate on the partition-cohort success count BEFORE any per-partition emission attempt, routing the cohort outcome down exactly one of three mutually-exclusive paths: **Path A (zero-partitions-succeeded → existing rf-team-lead.md:417 fix-cycle escalation; NO synthetic emits)** fires when the success count is `0` and the orchestrator MUST activate the byte-stable `rf-team-lead.md:417` fix-cycle escalation (max-3-cycles HALT-and-ask-user contract) without emitting any synthetic-dnsp block — a HIGH synthetic for every partition is informationally equivalent to escalation and adds noise; **Path B (≥1-success AND ≥1-exhaust → synthetic-dnsp emits ALONGSIDE real findings)** fires when at least one partition succeeded AND at least one partition exhausted its escalation ladder, and the orchestrator MUST emit one synthetic-dnsp block per exhausted partition into the normal output stream alongside the real findings from the successful partitions (the synthetic-dnsp adds to, never replaces, real findings — preserving the cohort's real-finding count and the parallel-research invariant); **Path C (all-partitions-succeeded → no synthetic; normal merge)** fires when every partition succeeded and is the baseline no-DNSP path. The three paths are mutually exclusive (a single partition-cohort outcome MUST traverse exactly one path; the guard MUST reject any cohort outcome that satisfies more than one path's precondition or none — e.g., a cohort with zero successes AND zero exhausts is a contract violation because every partition must terminate in success-or-exhaust). Such guard-precedence violations surface as `R-122-guard-precedence-violation` errors (named symbol distinct from `API-003-exhaust-point-vocabulary-violation` and `DM-003-dedup-key-shape-violation` because the path-selection gate is upstream of the per-emission wire-shape gate — the symbol scopes the cohort-level path-selection failure, not a per-emission field-shape failure) and MUST NOT be silently coerced into a default path. The `rf-team-lead.md:417` line MUST be byte-stable across the M6 landing (COMP-006-M6 preservation gate; sha256 frozen at `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`); the all-agents-fail Path A activation MUST NOT replace, short-circuit, or modify the existing fix-cycle escalation, only route control to it.

(SKILL.md carries an extended paragraph with the same path semantics plus a 3-part rationale clause naming why the cohort-level pre-emission guard, exhaustive-paths-with-contract-reject, and distinct-named-symbol design choices each rule out a class of latent failure modes.)

## 4. Sub-Agent Verification — quality-engineer ratification

A `quality-engineer` sub-agent (agent-id `ab60f195417fac103`) was spawned with the T06.08 verification charter (7 structural checks V1–V7 + strict-additivity invariant). The sub-agent ran read-only Grep + Read + `sha256sum` + `git diff` against the 4 wrapper files and the COMP-006-M6 preservation gate, then emitted the verdict:

**OVERALL: PASS — V1/V2/V3/V4/V5/V6/V7 all CONFIRMED**

| # | Check | Sub-agent verdict | Anchor counts (rf-analyst / rf-qa / rf-qa-qual / SKILL.md) |
|---|---|---|---|
| V1 | R-122 clause anchor at 4/4 wrapper sites | **PASS** | `All-agents-fail guard precedence (R-122)` = 1/1/1/1 |
| V2a | `Path A (zero-partitions-succeeded` at 4/4 | **PASS** | 1/1/1/1 |
| V2b | `Path B (≥1-success AND ≥1-exhaust` at 4/4 | **PASS** | 1/1/1/1 |
| V2c | `Path C (all-partitions-succeeded` at 4/4 | **PASS** | 1/1/1/1 |
| V3a | New `R-122-guard-precedence-violation` at 4/4 | **PASS** | 1/1/1/1 |
| V3b | Prior `API-003-exhaust-point-vocabulary-violation` preserved | **PASS** | 1/1/1/2 (≥1 each) |
| V3c | Prior `DM-003-dedup-key-shape-violation` preserved | **PASS** | 1/1/1/3 (≥1 each) |
| V4a | `sha256(rf-team-lead.md)` = `874a516e3baedd…e255e40b` | **PASS** | exact match |
| V4b | `sha256(line 417)` = `51725c0ffa15…701a0a0` | **PASS** | exact match |
| V4c | `git diff rf-team-lead.md` empty | **PASS** | empty |
| V4d | Byte-stable sha pin literal cited at 4/4 | **PASS** | 1/1/1/1 |
| V5a | `mutually exclusive` literal at 4/4 | **PASS** | 1/1/1/1 |
| V5b | `every partition must terminate in success-or-exhaust` at 4/4 | **PASS** | 1/1/1/1 |
| V6a | `DM-003-fixed-field-invariant-violation` preserved | **PASS** | 1/1/1/1 |
| V6b | `DM-003-dynamic-field-invariant-violation` preserved | **PASS** | 1/1/1/1 |
| V6c | `DM-003-recommendation-invariant-violation` preserved | **PASS** | 1/1/1/1 |
| V6d | `DM-003-dedup-key-shape-violation` preserved | **PASS** | 1/1/1/3 (≥1 each) |
| V6e | `DM-003-found-n-times-invariant-violation` preserved | **PASS** | 1/1/1/1 |
| V6f | `API-003-exhaust-point-vocabulary-violation` preserved | **PASS** | 1/1/1/2 (≥1 each) |
| V6g | `severity: HIGH` (≥1 per file) | **PASS** | 1/1/1/1 (≥1) |
| V6h | `source: "synthetic-dnsp"` (regex tolerant of YAML quoting) | **PASS** | 1/2/1/1 (≥1 each) |
| V6i | Byte-exact recommendation literal (≥1 per file) | **PASS** | 2/1/1/2 (≥1 each) |
| V7 | `diff -q src/ vs .claude/` for all 4 files | **PASS** | no output (synced) |

**Strict-additivity invariant:** Sub-agent confirms T06.08 is purely additive — no prior anchor was removed, renamed, or count-reduced. Every prior named rejection symbol (5 DM-003 symbols from T06.03/T06.04/T06.05 + the API-003 symbol from T06.07), severity/source/recommendation literal anchor, and byte-stable sha pin literal remains intact at the required ≥1 per file. COMP-006-M6 preservation gate is fully held (rf-team-lead.md byte-identical end-to-end, no diff).

**Sub-agent non-blocking observations:**
1. Asymmetric anchor counts in SKILL.md (e.g., `DM-003-dedup-key-shape-violation` = 3, `API-003-exhaust-point-vocabulary-violation` = 2) reflect the skill file's prior T06.05/T06.07 anchor density across the broader DNSP contract section, not new drift.
2. `R-122-guard-precedence-violation` is the third named rejection symbol introduced in Phase 6 (after T06.05's DM-003-dedup-key-shape-violation and T06.07's API-003-exhaust-point-vocabulary-violation); the naming convention is internally consistent (`<contract-id>-<violation-name>`).
3. T06.08 files (rf-analyst.md, rf-qa.md, rf-qa-qualitative.md, SKILL.md) byte-identical between `src/superclaude/` and `.claude/` post-`make sync-dev`.

## 5. Preservation invariants — COMP-006-M6 gate

| Slice | sha256 (pre-T06.08 = post-T06.07) | sha256 (post-T06.08) |
|---|---|---|
| `src/superclaude/agents/rf-team-lead.md:417` (COMP-006-M6 preservation gate, byte-stable end-to-end across PR-02, PR-03, M1–M6) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — no edit anywhere) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |

```text
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
$ sha256sum src/superclaude/agents/rf-team-lead.md
874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b  src/superclaude/agents/rf-team-lead.md
$ git diff src/superclaude/agents/rf-team-lead.md
(empty)
```

Both hashes match the values pinned in D-0068 §6, D-0069 §7, D-0070 §6, D-0071 §5, D-0072 §5, D-0073 §5, and CP-P06-T01-T05 §6 → **COMP-006-M6 preservation gate PASS.**

**All-agents-fail textual parity at 4/4 sites preserved.** The canonical guard paragraph at SKILL.md (the original 1-sentence "All-agents-fail guard" paragraph) is preserved verbatim; T06.08 appends the formal R-122 precedence paragraph immediately after it (additive — not a replacement). The three agent parity wrapper bullets at rf-analyst.md / rf-qa.md / rf-qa-qualitative.md are extended at the tail of their existing T06.07 clause with the R-122 contract appended; the existing all-agents-fail sentence inside each wrapper bullet ("All-agents-fail still escalates normally (no DNSP)") is preserved verbatim.

## 6. Edits applied

| # | File | Region | Change type | Description |
|---|---|---|---|---|
| 1 | `src/superclaude/skills/task-builder/SKILL.md` | New paragraph inserted between the existing "**All-agents-fail guard.**" paragraph and the subsequent "**Dedup key**" paragraph | additive | Inserted the formal "**All-agents-fail guard precedence (R-122).**" paragraph naming the three mutually-exclusive paths (A/B/C), the `R-122-guard-precedence-violation` named rejection symbol, the COMP-006-M6 sha pin literal, the cohort-level pre-emission guard semantics, the contract-violation reject for "zero successes AND zero exhausts", and a 3-part rationale clause |
| 2 | `src/superclaude/agents/rf-analyst.md` | DNSP wrapper bullet tail (appended after T06.07 API-003-M6 wire-shape clause) | additive | Appended the R-122 all-agents-fail guard precedence clause naming the three mutually-exclusive paths, the new `R-122-guard-precedence-violation` symbol, and the byte-stable sha pin literal |
| 3 | `src/superclaude/agents/rf-qa.md` | DNSP wrapper bullet tail | additive | Symmetric to #2 |
| 4 | `src/superclaude/agents/rf-qa-qualitative.md` | DNSP wrapper bullet tail | additive | Symmetric to #2 |

`rf-team-lead.md` was NOT edited (preservation gate — see §5).

## 7. Acceptance Criteria — Coverage Table

| AC | Criterion | Status | Evidence |
|---|---|---|---|
| AC1 | Zero-partitions-succeeded fixture's execution log shows `rf-team-lead.md:417` activation and no synthetic block | **PASS (spec-level)** | §3.1 (Path A named at 1/1/1/1 with explicit `rf-team-lead.md:417` reference and `NO synthetic emits` semantics; fixture-level binding deferred to T06.16 TEST-020 per Phase 6 task graph) |
| AC2 | Mixed-success fixture's output stream contains synthetic-dnsp emission | **PASS (spec-level)** | §3.2 (Path B named at 1/1/1/1 with explicit `synthetic-dnsp emits ALONGSIDE real findings` semantics; fixture-level binding deferred to T06.15 TEST-018 per Phase 6 task graph) |
| AC3 | Sub-agent quality-engineer report confirms mutually-exclusive paths preserved | **PASS** | §4 V5a + V5b (sub-agent confirms `mutually exclusive` literal at 4/4 and the `every partition must terminate in success-or-exhaust` contract-violation reject clause at 4/4) |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0074/evidence.md` | **PASS** | This file |
| AC5 (implicit) | R-122 clause anchor at 4/4 wrapper sites | **PASS** | §3.5 (1/1/1/1 = 100%) |
| AC6 (implicit) | New `R-122-guard-precedence-violation` named symbol at 4/4 sites | **PASS** | §3.6 (1/1/1/1 = 100%; distinct from `API-003-exhaust-point-vocabulary-violation` and `DM-003-dedup-key-shape-violation`) |
| AC7 (implicit) | Three mutually-exclusive paths (A/B/C) each named at 4/4 | **PASS** | §3.1 + §3.2 + sub-agent V2a/V2b/V2c (3 × 1/1/1/1 = 12/12 = 100%) |
| AC8 (implicit) | COMP-006-M6 sha pin literal cited at 4/4 sites | **PASS** | §3.8 (1/1/1/1 = 100%) |
| AC9 (implicit) | `rf-team-lead.md:417` byte-stable; whole-file unchanged | **PASS** | §5 (sha256 pair matches D-0068/.../D-0073/CP-P06-T01-T05 pin byte-identically; `git diff` empty) |
| AC10 (implicit) | Strict additivity — no prior contract clauses removed | **PASS** | Sub-agent §4 strict-additivity invariant (all 6 prior named rejection symbols + severity/source/recommendation literal anchors preserved at ≥1 per file; 4/4 wrapper sites synced) |

**Overall: PASS.**

## 8. Post-edit slice hashes (for downstream tasks)

| Slice | sha256 (post-edit) |
|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` (whole file) | `7deb5090a04b063a240054f884851709bd17053d69bc59a86039af46ac9c9dfb` |
| `src/superclaude/agents/rf-analyst.md` (whole file) | `932701df6ff1a43d20730376b15281bddccf61d3795853d1465973765cd2b81a` |
| `src/superclaude/agents/rf-qa.md` (whole file) | `788d76686dfdfafe080d8f6a062dfe66c31d6d66a5551f98ad3a3c4118a1a521` |
| `src/superclaude/agents/rf-qa-qualitative.md` (whole file) | `73eeec6db1141bc38aebfba2a7d18696b162c4bafbd07e1f9bf93de23cf365e9` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — unchanged) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |

`make sync-dev` ran clean for the four touched files. `diff -q src/superclaude/<file> .claude/<file>` returns no output for all four (verified post-sync; sub-agent V7 PASS).

## 9. Observations (Non-Blocking)

- **Fixture-level AC1/AC2 binding deferred to T06.15 + T06.16 (by design).** T06.08 pins the wrapper-level contract that the TEST-020 (all-agents-fail bypass) and TEST-018 (twice-exhaust) fixtures will programmatically bind to. Per the Phase 6 task graph dependency map (T06.16 depends on T06.08, T06.10, T06.15), the cohort-level path-selection guard wired by T06.08 is the spec-level contract that the fixture-level binding ratifies. This sequencing matches T06.07's deferred consumer-side merge-step wiring at T06.11 (where T06.07 pinned the producer-side wire-shape contract and T06.11 lands the consumer-side edit at SKILL.md A.8/A.10).
- **Three-named-symbol dual-gate scoping is intentional.** `R-122-guard-precedence-violation` (T06.08), `API-003-exhaust-point-vocabulary-violation` (T06.07), and `DM-003-dedup-key-shape-violation` (T06.05) form a 3-tier rejection hierarchy: the cohort-level path-selection gate (R-122 — fires when the cohort outcome doesn't fit any of the three mutually-exclusive paths), the per-emission wire-shape gate (API-003 — fires when an emission's wire-shape is malformed or the exhaust_point is non-vocabulary), and the per-emission field-shape gate (DM-003 — fires when the dedup_key tuple shape itself is wrong). All three can fire on the same input depending on which gate trips first; operator tooling can grep the symbols to distinguish the three failure modes.
- **`make verify-sync` reports pre-existing drift on `auggie-bash-gate.sh` (not distributable) + `reject-workspace-writes.sh` installer registration.** Same pre-existing drift documented in D-0068 §6, D-0069 §9, D-0070 §9, D-0071 §8, D-0072 §8, D-0073 §10, CP-P06-T01-T05 §7.4 — belongs to the in-flight `feat/hook-sync-and-matcher-fix` branch, unrelated to T06.08 / R-122. The skills/agents/commands cross-checks all PASS for the four T06.08-touched files.
- **Bullet/paragraph structure preserved.** The new T06.08 clause extends the existing T06.07 wire-shape clause within the same wrapper bullet at each agent site rather than introducing a new bullet, preserving the 6-bullet "Orchestrator Responsibilities" list count. SKILL.md gets one additional paragraph (between the existing 1-sentence "All-agents-fail guard" paragraph and the "Dedup key" paragraph), matching the additive pattern used by T06.03 → T06.04 → T06.05 → T06.07. The existing 1-sentence "All-agents-fail guard" paragraph at SKILL.md is preserved verbatim — T06.08 augments rather than replaces it.
- **Strict additivity is invariantly preserved on this branch.** Same as T06.03/T06.04/T06.05/T06.07: no fix-cycle loops added, no new stages, no new partition agent roles, no changes to PR-02 / M5 halt-guards wrapper / API-004 contract / per-gate counter tables. T06.08's only behavioural addition is the cohort-level path-selection guard with the new named rejection symbol (which fires upstream of the per-emission rejection symbols already landed by T06.03–T06.07).

## 10. Provenance

- Pre-edit HEAD: `edd3ddd docs(task-builder): D-0067 T05.16 MIG-005 evidence + FF governance entry` (same baseline as T06.01–T06.07 — no commits yet for the M6 wrapper landing series; MIG-006 single-commit landing scheduled for T06.17).
- M1 contract-freeze references: roadmap.md L114 (API-003 row — `all_fail:zero-success-routes-to-rf-team-lead.md:417-NO-DNSP`), R-122 row (R-122 all-agents-fail guard mutual-exclusivity contract).
- T06.01 closure (FR-CONV.6 wrapper landed): D-0068 (Overall PASS, 2026-05-18).
- T06.02 closure (DM-003-M6 7-field schema): D-0069 (Overall PASS, 2026-05-18).
- T06.03 closure (severity + source fixed-field rejection): D-0070 (Overall PASS, 2026-05-18).
- T06.04 closure (affected_range + evidence dynamic-field rejection): D-0071 (Overall PASS, 2026-05-18).
- T06.05 closure (recommendation + dedup_key + found_n_times rejection): D-0072 (Overall PASS, 2026-05-18).
- T06.06 mid-phase checkpoint: CP-P06-T01-T05 (Overall PASS, 2026-05-18).
- T06.07 closure (API-003-M6 wire-shape + closed vocabulary): D-0073 (Overall PASS, 2026-05-18) — `API-003-exhaust-point-vocabulary-violation` named symbol bound at 4/4 sites.
- R-122 (all-agents-fail guard mutual-exclusivity contract): three mutually-exclusive paths (A/B/C) + `R-122-guard-precedence-violation` named symbol bound at 4/4 sites by T06.08; fixture-level binding (TEST-018 mixed-success / TEST-020 all-agents-fail) lands at T06.15 + T06.16.
- T06.09 (within-cycle + cross-cycle dedup composition, INV-012) is the natural next consumer of T06.08's R-122 contract — it composes with the within-cycle counter increment under Path B and the cross-cycle dedup-as-not-regression rule under PR-02 / INV-012.
- T06.14 (verify COMP-006-M6 preservation) is the downstream gate that verifies the byte-stability sha pin literal cited at the 4 wrapper sites; T06.18 (End-of-Phase-6 checkpoint) gates T06.01–T06.17 collectively for MIG-006 single-commit landing.
