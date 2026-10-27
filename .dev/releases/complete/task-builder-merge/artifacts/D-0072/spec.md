# D-0072 — T06.05 Spec: Implement recommendation + dedup_key + found_n_times emitters

**Task:** T06.05 — Implement DM-003.recommendation + DM-003.dedup_key + DM-003.found_n_times emitters
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-117 (DM-003.recommendation fixed string), R-118 (DM-003.dedup_key 2-tuple YAML list), R-119 (DM-003.found_n_times int default 1)
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution (grep + structural inspection)

---

## 1. Goal

Bind explicit emitter-level rejection semantics to the three remaining DM-003 fields that T06.02 (D-0069) enumerated in the 7-field contract and that T06.03 (D-0070) + T06.04 (D-0071) did not cover. After T06.05, every wrapper site (`SKILL.md` + `rf-analyst.md` + `rf-qa.md` + `rf-qa-qualitative.md`) carries an additional clause/paragraph stating:

1. **`recommendation`** MUST be the literal byte-exact string `Manual review required — partition agent failed twice` (case-sensitive; no leading/trailing whitespace; no suffix). This matches R-117 (roadmap.md L368) verbatim. Any other value is rejected with the named error `DM-003-recommendation-invariant-violation`.
2. **`dedup_key`** MUST be a 2-element YAML list `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]` where the second element is drawn from the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` (per R-118 + R-121). Wrong cardinality (≠2 elements) or out-of-vocabulary exhaust_point is rejected with the named error `DM-003-dedup-key-shape-violation`.
3. **`found_n_times`** MUST be a positive integer ≥1; default `1` on first emission; increments by exactly `1` on each within-cycle dedup-key collapse (per R-119). Non-integer or value `<1` on first emission is rejected with the named error `DM-003-found-n-times-invariant-violation`.

## 2. Wrapper Drift Correction (R-117 contract realignment)

Prior to T06.05 the wrapper at all 4 sites carried the recommendation literal as:

```
recommendation: "Manual review required — partition agent failed twice on this range"
```

This contradicts R-117 (roadmap.md L368), which pins the byte-exact value as:

```
Manual review required — partition agent failed twice
```

The wrapper extension `on this range` was authored in commit `dfae6cf` prior to T06.01, predating any rejection contract. T06.05's AC1 requires byte-exact match; therefore T06.05 corrects the wrapper at 5 sites:

| # | File | Line | Current (drift) | Corrected (R-117 byte-exact) |
|---|---|---|---|---|
| 1 | `src/superclaude/skills/task-builder/SKILL.md` | 664 | `recommendation: "Manual review required — partition agent failed twice on this range"` | `recommendation: "Manual review required — partition agent failed twice"` |
| 2 | `src/superclaude/agents/rf-analyst.md` | 70 | (same drifted quoted value inside wrapper bullet) | (corrected to R-117 byte-exact) |
| 3 | `src/superclaude/agents/rf-analyst.md` | 83 | `- **Recommendation:** Manual review required — partition agent failed twice on this range. The other N-1 partitions completed; review the affected_range files manually before accepting the gate verdict.` | `- **Recommendation:** Manual review required — partition agent failed twice` (with operator-note moved to a separate sentence outside the field-value scope) |
| 4 | `src/superclaude/agents/rf-qa.md` | 78 | (drifted quoted value) | (R-117 byte-exact) |
| 5 | `src/superclaude/agents/rf-qa-qualitative.md` | 79 | (drifted quoted value) | (R-117 byte-exact) |

The wrapper's per-bullet narrative is otherwise preserved; only the quoted field VALUE is corrected. The example output format in rf-analyst.md L83 keeps the operator note as a sibling bullet so the guidance is not lost.

## 3. New Rejection Clauses

### 3.1 Agent files (rf-analyst.md L70 tail, rf-qa.md L78 tail, rf-qa-qualitative.md L79 tail)

Append immediately after the T06.04 "Dynamic-field emitter rejection (R-115 + R-116)" clause:

> **Fixed-value + tuple-shape + counter emitter rejection (R-117 + R-118 + R-119).** The `recommendation` field is a fixed-value invariant: the emitter MUST reject any synthetic emission whose `recommendation` field is not the literal byte-exact string `Manual review required — partition agent failed twice` (case-sensitive; no leading/trailing whitespace; no suffix). The `dedup_key` field MUST be emitted as a 2-element YAML list of the shape `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`; the emitter MUST reject any synthetic emission whose `dedup_key` is not a 2-element list OR whose second element falls outside the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`. The `found_n_times` field defaults to the integer `1` on first emission and increments by exactly `1` on each within-cycle dedup-key collapse; the emitter MUST reject any synthetic emission whose `found_n_times` is not a positive integer ≥1 OR whose first emission carries a value other than `1`. Such rejections surface as `DM-003-recommendation-invariant-violation`, `DM-003-dedup-key-shape-violation`, and `DM-003-found-n-times-invariant-violation` errors respectively, and MUST NOT be silently coerced.

### 3.2 SKILL.md L670+ (new paragraph after the T06.04 "Dynamic-field emitter rejection" paragraph)

> **Fixed-value + tuple-shape + counter emitter rejection (R-117 + R-118 + R-119).** The `recommendation`, `dedup_key`, and `found_n_times` fields complete the DM-003 emitter rejection contract. The `recommendation` field is a fixed-value invariant pinned to the literal byte-exact string `Manual review required — partition agent failed twice` (case-sensitive; no leading/trailing whitespace; no suffix); the emitter MUST reject any synthetic-dnsp emission carrying any other value, including same-prefix-with-trailing-suffix variants (the wrapper's earlier ` on this range` extension was a pre-T06.01 drift and is removed by T06.05). The `dedup_key` field MUST be emitted as a 2-element YAML list of the shape `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`; the emitter MUST reject any synthetic emission whose `dedup_key` is not a 2-element list OR whose second element falls outside the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` (the closed vocabulary is API-003-M6's exhaust-point alphabet, ratified by T06.07 / R-121). The `found_n_times` field defaults to the integer `1` on first emission and increments by exactly `1` on each within-cycle dedup-key collapse (the cross-cycle collapse rule composing with PR-02 monotonicity / INV-012 is the "Dedup key" paragraph below); the emitter MUST reject any synthetic emission whose `found_n_times` is not a positive integer ≥1 OR whose first emission carries a value other than `1`. Such rejections surface as `DM-003-recommendation-invariant-violation`, `DM-003-dedup-key-shape-violation`, and `DM-003-found-n-times-invariant-violation` errors respectively and MUST NOT be silently coerced. Rationale: a byte-exact `recommendation` literal makes synthetic findings grep-discoverable by operators without false positives from elaborated suffixes (an unbounded suffix would let two synthetics with the same dedup_key but slightly different recommendations skip dedup collapse, breaking R-118's two-identical-dedup_keys → cardinality 1 + found_n_times=2 invariant); a 2-element list with closed-vocabulary second element makes the dedup_key cardinality-comparable across cycles without YAML-dialect ambiguity (a 3-element list or a free-form exhaust_point would let cross-cycle composition mis-collide, breaking INV-012); a strictly positive `found_n_times` integer with default `1` and exact `+1` increment-on-collapse makes the within-cycle collapse counter monotonic and the cross-cycle cohort-count semantics auditable (a counter that resets or skips would let dedup collapses double-count, breaking T05.07's INV-012 cross-cycle composition with PR-02 monotonicity).

## 4. Edits (Strictly Additive + Targeted Drift Correction)

| # | File | Region | Change Type | Description |
|---|---|---|---|---|
| 1 | `src/superclaude/skills/task-builder/SKILL.md` | L664 | drift-fix | Remove ` on this range` suffix from `recommendation:` field value to match R-117 byte-exact |
| 2 | `src/superclaude/skills/task-builder/SKILL.md` | new paragraph after L670 | additive | Insert "Fixed-value + tuple-shape + counter emitter rejection (R-117 + R-118 + R-119)" paragraph with rationale |
| 3 | `src/superclaude/agents/rf-analyst.md` | L70 tail | drift-fix + additive | (a) Remove ` on this range` from quoted `recommendation:` field value inside the bullet; (b) append R-117/R-118/R-119 rejection clause |
| 4 | `src/superclaude/agents/rf-analyst.md` | L83 | drift-fix | Trim `**Recommendation:**` example to byte-exact `Manual review required — partition agent failed twice`; relocate the operator-guidance sentence as a separate sibling bullet so example renders the canonical field value |
| 5 | `src/superclaude/agents/rf-qa.md` | L78 tail | drift-fix + additive | Symmetric to #3 (no example output to fix) |
| 6 | `src/superclaude/agents/rf-qa-qualitative.md` | L79 tail | drift-fix + additive | Symmetric to #3 (no example output to fix) |

`rf-team-lead.md` is NOT edited (COMP-006-M6 preservation gate — see Acceptance Criteria below).

## 5. Acceptance Criteria

| AC | Description |
|---|---|
| AC1 | `recommendation` field at all 4 wrapper sites is the literal `Manual review required — partition agent failed twice` byte-exact (no ` on this range` suffix anywhere in the wrapper or example output) |
| AC2 | `dedup_key` field clause carries the YAML 2-tuple shape `["<range>", "<exhaust_point>"]` at all 4 wrapper sites |
| AC3 | Closed-vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` is named at all 4 wrapper sites for the exhaust_point alphabet |
| AC4 | `found_n_times` is documented as integer default `1` with +1 increment on within-cycle collapse at all 4 wrapper sites |
| AC5 | Three named rejection error symbols (`DM-003-recommendation-invariant-violation`, `DM-003-dedup-key-shape-violation`, `DM-003-found-n-times-invariant-violation`) present at all 4 wrapper sites |
| AC6 | `rf-team-lead.md:417` byte-stable (sha256 = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`); whole-file rf-team-lead.md sha256 unchanged |
| AC7 | Two-identical-dedup_key fixture (TEST-019, lands in T06.15) collapses to cardinality 1 with `found_n_times=2` — spec-level contract pinned here, programmatic positive-path verification deferred to T06.15 (same staging as T06.03/T06.04) |
| AC8 | Evidence at `TASKLIST_ROOT/artifacts/D-0072/evidence.md` |

## 6. Validation Plan

- **Manual review:** reviewer confirms YAML 2-tuple list format named in the clause; reviewer confirms the byte-exact recommendation literal matches R-117 (roadmap.md L368).
- **Grep evidence:** byte-exact `Manual review required — partition agent failed twice` present at all 4 wrapper sites; ` on this range` ABSENT from `src/superclaude/`; three new rejection error symbols present at all 4 sites; closed vocabulary entries present at all 4 sites.
- **Preservation gate:** rf-team-lead.md:417 sha256 unchanged (COMP-006-M6).
- **Fixture binding:** TEST-019 fixture (T06.15, D-0080) will be the positive-path verifier for the cardinality-1 + found_n_times=2 invariant; T06.07 emission code (D-0073) will be the programmatic negative-path verifier for the three rejection symbols.

## 7. Dependencies and Provenance

- **Upstream dependencies:** T06.04 (D-0071) PASS — dynamic-field rejection contract landed at all 4 wrapper sites with explicit error symbol `DM-003-dynamic-field-invariant-violation`.
- **Roadmap references:** R-117 (recommendation fixed-string, roadmap.md L368), R-118 (dedup_key 2-tuple, roadmap.md L369), R-119 (found_n_times int default 1, roadmap.md L370), R-121 (closed exhaust-point vocabulary, roadmap.md L373).
- **Downstream consumers:** T06.06 mid-phase checkpoint (D-CP06-MID-T01-T05), T06.07 emission code (D-0073, programmatic rejection ratification), T06.09 dedup composition (D-0075, INV-012 cross-cycle), T06.15 fixture (D-0080, positive-path TEST-019 cardinality + found_n_times collapse).
