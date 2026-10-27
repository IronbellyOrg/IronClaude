# D-0072 — T06.05 Evidence: Implement recommendation + dedup_key + found_n_times emitters

**Date:** 2026-05-18
**Task:** T06.05 — Implement DM-003.recommendation + DM-003.dedup_key + DM-003.found_n_times emitters
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-117 (recommendation byte-exact fixed string), R-118 (dedup_key 2-tuple YAML list), R-119 (found_n_times int default 1 + increment on collapse)
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution (grep + structural inspection)
**Status:** PASS

---

## 1. Summary

T06.05 closes the DM-003 emitter rejection contract by binding **explicit emitter-level rejection semantics** to the three remaining fields that T06.02 (D-0069) enumerated in the 7-field contract and that T06.03 (D-0070, severity + source) and T06.04 (D-0071, affected_range + evidence) did not cover. After T06.05, each of the four wrapper sites (`SKILL.md`, `rf-analyst.md`, `rf-qa.md`, `rf-qa-qualitative.md`) carries an additional clause/paragraph naming three new rejection error symbols:

- **`DM-003-recommendation-invariant-violation`** — fires when the `recommendation` field is not the byte-exact literal `Manual review required — partition agent failed twice` (R-117).
- **`DM-003-dedup-key-shape-violation`** — fires when `dedup_key` is not a 2-element YAML list `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]` OR when the second element falls outside the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` (R-118 + R-121).
- **`DM-003-found-n-times-invariant-violation`** — fires when `found_n_times` is not a positive integer ≥1 OR the first emission carries a value other than `1` (R-119).

T06.05 also corrects a **pre-T06.01 wrapper drift**: the recommendation field was carried at 5 sites with the suffix ` on this range` (`recommendation: "Manual review required — partition agent failed twice on this range"`), contradicting R-117's roadmap.md L368 byte-exact pin. Correction is targeted (5 sites) and preserves the operator-guidance prose by relocating it to a sibling bullet in the example output (rf-analyst.md L83-84). The `rf-team-lead.md:417` all-agents-fail backstop is byte-stable end-to-end (§5).

## 2. Planning Inputs

- **Dependency closure.** T06.04 (D-0071) PASS — dynamic-field rejection contract (`affected_range` + `evidence`) bound at all 4 wrapper sites with error symbol `DM-003-dynamic-field-invariant-violation` (D-0071 §3 grep evidence; D-0071 §7 ACs all PASS).
- **R-117 spec (roadmap.md L368).** `DM-003.recommendation` — recommendation field — fixed string `Manual review required — partition agent failed twice`. AC: `emission:carries-fixed-recommendation-string-byte-exact`.
- **R-118 spec (roadmap.md L369).** `DM-003.dedup_key` — 2-tuple `(assigned_files_range, escalation_ladder_exhaust_point)` emitted as YAML list `["<range>", "<exhaust_point>"]`.
- **R-119 spec (roadmap.md L370).** `DM-003.found_n_times` — int, default `1`; increments by `1` on each within-cycle dedup-key collapse.
- **R-121 cross-reference (roadmap.md L373).** API-003 closed vocabulary for `escalation_ladder_exhaust_point` is `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`. T06.07 ratifies API-003 emission; T06.05 binds the vocabulary to the dedup_key rejection rule so the wrapper-level contract is internally consistent.
- **M1 contract-freeze reference (roadmap.md L109).** `recommendation:Manual-review-required-fixed; dedup_key:2-tuple-range-exhaust_point; found_n_times:int-default-1`. Per the Phase 1 schema-registry pattern (consistent with D-0069 §2, D-0070 §2, D-0071 §2), the roadmap row IS the contract-freeze; T06.05 does not re-pin the values, it binds the rejection semantics + the canonical wire shapes (literal recommendation, 2-tuple list shape, integer counter discipline) to them.
- **Wrapper-drift discovery.** Pre-T06.05 baseline (sha256 = `1d26642...`/`...`/`...`/`c759aba...`, matching D-0071 §8 post-edit table) carried `recommendation: "Manual review required — partition agent failed twice on this range"` at 5 sites (`SKILL.md` L664, `rf-analyst.md` L70 wrapper + L83 example, `rf-qa.md` L78, `rf-qa-qualitative.md` L79). This contradicts R-117's byte-exact literal — the drift was authored in commit `dfae6cf` prior to T06.01 and was carried through T06.01–T06.04 untouched. T06.05's AC1 (`recommendation field is the literal string \`Manual review required — partition agent failed twice\` byte-exact`) requires correction; D-0072 §2 (this evidence file's drift-correction subsection) documents the realignment.

## 3. Execution — Acceptance-criterion grep evidence

### 3.1 AC1 — byte-exact recommendation literal at all 4 wrapper sites; ` on this range` suffix absent

```text
$ grep -c -F 'Manual review required — partition agent failed twice' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:2
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:2
```

All 4 wrapper sites carry the byte-exact R-117 literal (rf-analyst.md hits 2 because both the wrapper bullet and the example output `**Recommendation:**` row carry it; SKILL.md hits 2 because both the contract bullet at L664 and the T06.05 rejection paragraph at L672 carry it) → **PASS** for AC1 (positive side).

```text
$ grep -rn "on this range" src/superclaude/
src/superclaude/skills/task-builder/SKILL.md:672:**Fixed-value + tuple-shape + counter emitter rejection (R-117 + R-118 + R-119).** ... (the wrapper's earlier ` on this range` extension was a pre-T06.01 drift and is removed by T06.05). ...
```

The only remaining ` on this range` occurrence in `src/superclaude/` is the intentional meta-narrative inside the T06.05 rejection paragraph itself, naming the corrected drift. The drift no longer exists in any wrapper bullet, contract-value position, or example-output rendering → **PASS** for AC1 (negative side, drift removed).

### 3.2 AC2 — `dedup_key` YAML 2-tuple shape `["<range>", "<exhaust_point>"]` at all 4 wrapper sites

```text
$ grep -c -F '["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:2
```

All 4 wrapper sites carry the YAML 2-tuple shape (SKILL.md hits 2 because both the contract bullet and the T06.05 rejection paragraph carry it) → **PASS** for AC2.

### 3.3 AC3 — closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` at all 4 wrapper sites

```text
$ grep -c -F '{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:2
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:2
```

All 4 wrapper sites carry the closed vocabulary at least once (rf-analyst.md hits 2 because both the wrapper bullet and the example-output Dedup key row carry it; SKILL.md hits 2 because both the contract bullet and the T06.05 rejection paragraph carry it) → **PASS** for AC3.

### 3.4 AC4 — `found_n_times` discipline (default 1 + increment on within-cycle collapse) at all 4 wrapper sites

```text
$ grep -c -F 'found_n_times' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:2
```

Every wrapper site names the `found_n_times` field; the rejection clause adds the discipline ("defaults to the integer `1` on first emission and increments by exactly `1` on each within-cycle dedup-key collapse") at every site → **PASS** for AC4.

### 3.5 AC5 — three new rejection error symbols present at all 4 wrapper sites

```text
$ for sym in DM-003-recommendation-invariant-violation DM-003-dedup-key-shape-violation DM-003-found-n-times-invariant-violation; do
    echo "--- $sym ---"
    grep -c -F "$sym" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
done
--- DM-003-recommendation-invariant-violation ---
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
--- DM-003-dedup-key-shape-violation ---
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
--- DM-003-found-n-times-invariant-violation ---
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

All three named rejection error symbols are present at every wrapper site → **PASS** for AC5.

### 3.6 Full clause text (rf-analyst.md L70 tail; symmetric at rf-qa.md L78 and rf-qa-qualitative.md L79)

> **Fixed-value + tuple-shape + counter emitter rejection (R-117 + R-118 + R-119).** The `recommendation` field is a fixed-value invariant: the emitter MUST reject any synthetic emission whose `recommendation` field is not the literal byte-exact string `Manual review required — partition agent failed twice` (case-sensitive; no leading/trailing whitespace; no suffix). The `dedup_key` field MUST be emitted as a 2-element YAML list of the shape `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`; the emitter MUST reject any synthetic emission whose `dedup_key` is not a 2-element list OR whose second element falls outside the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}`. The `found_n_times` field defaults to the integer `1` on first emission and increments by exactly `1` on each within-cycle dedup-key collapse; the emitter MUST reject any synthetic emission whose `found_n_times` is not a positive integer ≥1 OR whose first emission carries a value other than `1`. Such rejections surface as `DM-003-recommendation-invariant-violation`, `DM-003-dedup-key-shape-violation`, and `DM-003-found-n-times-invariant-violation` errors respectively, and MUST NOT be silently coerced.

### 3.7 Full paragraph text (SKILL.md L672)

> **Fixed-value + tuple-shape + counter emitter rejection (R-117 + R-118 + R-119).** The `recommendation`, `dedup_key`, and `found_n_times` fields complete the DM-003 emitter rejection contract. The `recommendation` field is a fixed-value invariant pinned to the literal byte-exact string `Manual review required — partition agent failed twice` (case-sensitive; no leading/trailing whitespace; no suffix); the emitter MUST reject any synthetic-dnsp emission carrying any other value, including same-prefix-with-trailing-suffix variants (the wrapper's earlier ` on this range` extension was a pre-T06.01 drift and is removed by T06.05). The `dedup_key` field MUST be emitted as a 2-element YAML list of the shape `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]`; the emitter MUST reject any synthetic emission whose `dedup_key` is not a 2-element list OR whose second element falls outside the closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` (the closed vocabulary is API-003-M6's exhaust-point alphabet, ratified by T06.07 / R-121). The `found_n_times` field defaults to the integer `1` on first emission and increments by exactly `1` on each within-cycle dedup-key collapse (the cross-cycle collapse rule composing with PR-02 monotonicity / INV-012 is the "Dedup key" paragraph below); the emitter MUST reject any synthetic emission whose `found_n_times` is not a positive integer ≥1 OR whose first emission carries a value other than `1`. Such rejections surface as `DM-003-recommendation-invariant-violation`, `DM-003-dedup-key-shape-violation`, and `DM-003-found-n-times-invariant-violation` errors respectively and MUST NOT be silently coerced. Rationale: a byte-exact `recommendation` literal makes synthetic findings grep-discoverable by operators without false positives from elaborated suffixes (an unbounded suffix would let two synthetics with the same dedup_key but slightly different recommendations skip dedup collapse, breaking R-118's two-identical-dedup_keys → cardinality 1 + found_n_times=2 invariant); a 2-element list with closed-vocabulary second element makes the dedup_key cardinality-comparable across cycles without YAML-dialect ambiguity (a 3-element list or a free-form exhaust_point would let cross-cycle composition mis-collide, breaking INV-012); a strictly positive `found_n_times` integer with default `1` and exact `+1` increment-on-collapse makes the within-cycle collapse counter monotonic and the cross-cycle cohort-count semantics auditable (a counter that resets or skips would let dedup collapses double-count, breaking T05.07's INV-012 cross-cycle composition with PR-02 monotonicity).

## 4. Edits applied

| # | File | Region | Change type | Description |
|---|---|---|---|---|
| 1 | `src/superclaude/skills/task-builder/SKILL.md` | L664 (contract bullet value) | drift-fix | Removed ` on this range` suffix from the quoted `recommendation:` field value to match R-117 byte-exact |
| 2 | `src/superclaude/skills/task-builder/SKILL.md` | New paragraph at L672 (between the T06.04 "Dynamic-field emitter rejection" paragraph at L670 and the "Then the orchestrator merges" paragraph) | additive | Inserted "Fixed-value + tuple-shape + counter emitter rejection (R-117 + R-118 + R-119)" paragraph with rationale; names three new rejection error symbols |
| 3 | `src/superclaude/agents/rf-analyst.md` | DNSP wrapper bullet L70 tail (after T06.04 dynamic-field rejection clause) | drift-fix + additive | (a) Removed ` on this range` from the quoted `recommendation:` field value inside the bullet; (b) appended R-117/R-118/R-119 rejection clause naming the three new error symbols |
| 4 | `src/superclaude/agents/rf-analyst.md` | Example output L83-84 (was L83 single bullet) | drift-fix | Trimmed `**Recommendation:**` bullet to byte-exact `Manual review required — partition agent failed twice`; relocated operator-guidance sentence as a new sibling bullet `**Operator note:**` so the field-value rendering matches the canonical literal byte-exact |
| 5 | `src/superclaude/agents/rf-qa.md` | DNSP wrapper bullet L78 tail | drift-fix + additive | Symmetric to #3 (no example-output rendering present in this file) |
| 6 | `src/superclaude/agents/rf-qa-qualitative.md` | DNSP wrapper bullet L79 tail | drift-fix + additive | Symmetric to #3 (no example-output rendering present in this file) |

`rf-team-lead.md` was NOT edited (preservation gate — see §5).

## 5. Preservation invariants

| Slice | sha256 (pre-T06.05 = post-T06.04) | sha256 (post-T06.05) |
|---|---|---|
| `src/superclaude/agents/rf-team-lead.md:417` (3-cycle hard cap + all-agents-fail escalation backstop — COMP-006-M6 preservation gate, byte-stable end-to-end across PR-02, PR-03, M1–M6) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — no edit anywhere) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |

```text
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
$ sha256sum src/superclaude/agents/rf-team-lead.md
874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b  src/superclaude/agents/rf-team-lead.md
```

Both hashes match the values pinned in D-0068 §6, D-0069 §7, D-0070 §6, and D-0071 §5 → **COMP-006-M6 preservation gate PASS.**

## 6. Acceptance Criteria — Coverage Table

| AC | Description | Status | Evidence |
|---|---|---|---|
| AC1 | `recommendation` field byte-exact literal `Manual review required — partition agent failed twice` at all 4 wrapper sites (no ` on this range` suffix) | **PASS** | §3.1 (byte-exact literal hits ≥1 per file; ` on this range` only present as meta-narrative inside the T06.05 rejection paragraph naming the corrected drift; no wrapper bullet, contract-value, or example-output rendering carries the drift) |
| AC2 | `dedup_key` field clause carries the YAML 2-tuple shape `["<range>", "<exhaust_point>"]` at all 4 wrapper sites | **PASS** | §3.2 (literal `["<assigned_files_range>", "<escalation_ladder_exhaust_point>"]` hits ≥1 per file) |
| AC3 | Closed vocabulary `{retry-1, retry-2, gap-fill-round-1, gap-fill-round-2, gap-fill-round-3}` named at all 4 wrapper sites | **PASS** | §3.3 (literal closed vocabulary hits ≥1 per file) |
| AC4 | `found_n_times` documented as integer default `1` with +1 increment on within-cycle collapse at all 4 wrapper sites | **PASS** | §3.4 (`found_n_times` field named at every site, T06.05 rejection clause adds the discipline at every site) |
| AC5 | Three named rejection error symbols (`DM-003-recommendation-invariant-violation`, `DM-003-dedup-key-shape-violation`, `DM-003-found-n-times-invariant-violation`) present at all 4 wrapper sites | **PASS** | §3.5 (all three symbols hit ≥1 per file across all 4 sites; 12/12 = 100%) |
| AC6 | `rf-team-lead.md:417` byte-stable; whole-file unchanged | **PASS** | §5 (sha256 pair matches D-0068/D-0069/D-0070/D-0071 pin byte-identically) |
| AC7 | Two-identical-dedup_key fixture (TEST-019, T06.15) collapses to cardinality 1 with `found_n_times=2` | **PASS (spec-level)** | §3.6 + §3.7 (clause/paragraph pin the `found_n_times` +1 increment on within-cycle dedup-key collapse with named `DM-003-found-n-times-invariant-violation` rejection on first-emission ≠ `1`; positive-path TEST-019 fixture lands in T06.15 / D-0080, identical staging to T06.03's TEST-018 staging and T06.04's TEST-018/TEST-019 staging — see D-0070 §9 and D-0071 §8) |
| AC8 | Evidence at `TASKLIST_ROOT/artifacts/D-0072/evidence.md` | **PASS** | This file |

**Overall: PASS.**

## 7. Post-edit slice hashes (for downstream tasks)

| Slice | sha256 (post-edit) |
|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` (whole file) | `f48babc538cd1cf0f565d9f7169181a6aa31b905d322922460112bca8be13a1d` |
| `src/superclaude/agents/rf-analyst.md` (whole file) | `1ae58957a790b1694fc955e50a65c25cea500f823d37ce34bb8e627604d67fcc` |
| `src/superclaude/agents/rf-qa.md` (whole file) | `aa2d2c4539abf942786a1fe9410c0eff93d48465f58073047d696a4b7920c6f0` |
| `src/superclaude/agents/rf-qa-qualitative.md` (whole file) | `588adeeb4ea47df87a5bc28ad40292ebb1352a56a25194409ecaea64cc1e9bc5` |

`make sync-dev` ran clean for the four touched files. Skills/agents/commands cross-check confirms `src/` and `.claude/` agree for the FR-CONV.6 wrapper edit set byte-identically (`diff -q src/superclaude/<file> .claude/<file>` returns no output for all four).

## 8. Observations (Non-Blocking)

- **Wrapper drift fixed in-scope.** The pre-T06.01 wrapper drift on the recommendation field is corrected by this task per T06.05's explicit AC1 byte-exact requirement. The correction is localised (5 sites: SKILL.md L664, rf-analyst.md L70 + L83, rf-qa.md L78, rf-qa-qualitative.md L79) and preserves the operator-guidance prose at rf-analyst.md L83-84 by relocating it to a sibling `**Operator note:**` bullet (which is informational and not subject to byte-exact emitter rules). Future tasks (T06.07 emission code, T06.15 TEST-019 fixture) now bind to the canonical R-117 literal without ambiguity.
- **`make verify-sync` reports pre-existing drift on `auggie-bash-gate.sh` (not distributable) + `reject-workspace-writes.sh` installer registration.** Same pre-existing drift documented in D-0068 §6, D-0069 §9, D-0070 §9, D-0071 §8 — belongs to the in-flight `feat/hook-sync-and-matcher-fix` branch, unrelated to T06.05 / FR-CONV.6 / R-117 / R-118 / R-119. The skills/agents/commands cross-checks all PASS for the four T06.05-touched files.
- **Negative-path programmatic verification staging.** AC5 binds three named rejection symbols at all 4 wrapper sites as spec-level contracts so the programmatic emission code landing in T06.07 (D-0073, API-003-M6 emission) can bind to them. The end-to-end positive path (an exhausted-partition emitter producing the byte-exact `recommendation`, the well-shaped `dedup_key`, and the monotonic `found_n_times`) becomes fixture-verifiable when T06.15's TEST-019 lands (D-0080); the end-to-end negative path (an emitter producing a suffix-extended `recommendation`, a 3-element `dedup_key`, or `found_n_times: 0` being rejected) becomes programmatically exercisable when T06.07's emission code lands. This sequencing is by-design per the Phase 6 task graph (T06.05 spec → T06.07 emission code → T06.15 positive fixture → T06.06 + T06.18 cross-cutting ratification), identical to T06.03's staging (D-0070 §9) and T06.04's staging (D-0071 §8).
- **Bullet structure preserved.** The new T06.05 clause extends the existing T06.04 dynamic-field clause within the same wrapper bullet at each agent site rather than introducing a new bullet, preserving the 6-bullet "Orchestrator Responsibilities" list count downstream sub-agent verification keys on. SKILL.md gets one additional paragraph (between the T06.04 paragraph and the "Then the orchestrator merges" paragraph), matching the pattern used by T06.03 → T06.04.
- **`found_n_times` cross-cycle composition is named, not duplicated.** The T06.05 rejection clause names the within-cycle `+1` increment rule and points the cross-cycle composition rule at the existing "Dedup key" paragraph (SKILL.md L676) which already references PR-02 monotonicity / INV-012 (T05.07 wiring). T06.09 (R-123 + R-124) will land the full cross-cycle dedup composition; T06.05 binds only the within-cycle counter discipline + the rejection contract on the first-emission default value.

## 9. Provenance

- Pre-edit HEAD: `edd3ddd docs(task-builder): D-0067 T05.16 MIG-005 evidence + FF governance entry` (same baseline as T06.01–T06.04 — no commits yet for the M6 wrapper landing series).
- M1 contract-freeze reference: `roadmap.md` L109 + L368–370 (DM-003 row + R-117/R-118/R-119 rows).
- T06.01 closure (FR-CONV.6 wrapper landed): D-0068 (Overall PASS, 2026-05-18).
- T06.02 closure (DM-003-M6 7-field schema): D-0069 (Overall PASS, 2026-05-18; sub-agent verification 6/6 PASS).
- T06.03 closure (severity + source fixed-field rejection): D-0070 (Overall PASS, 2026-05-18).
- T06.04 closure (affected_range + evidence dynamic-field rejection): D-0071 (Overall PASS, 2026-05-18).
- R-117 (DM-003.recommendation byte-exact fixed string): wrapper-level rejection contract landed by T06.05; programmatic emission code lands in T06.07; positive-path fixture lands in T06.15 (TEST-019).
- R-118 (DM-003.dedup_key 2-tuple YAML list with closed-vocabulary second element): wrapper-level rejection contract landed by T06.05; programmatic emission code lands in T06.07; closed-vocabulary cross-binding to API-003-M6 lands in T06.07 (R-121); positive-path fixture lands in T06.15 (TEST-019).
- R-119 (DM-003.found_n_times int default 1 with +1 increment on within-cycle collapse): wrapper-level within-cycle rejection contract landed by T06.05; cross-cycle composition with PR-02 monotonicity (INV-012, T05.07) wired by T06.09; positive-path collapse fixture lands in T06.15 (TEST-019).
- T06.06 mid-phase checkpoint (D-CP06-MID-T01-T05) gates T06.01–T06.05 collectively immediately after this task.
