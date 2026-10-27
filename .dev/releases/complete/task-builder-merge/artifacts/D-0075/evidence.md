# D-0075 — T06.09 Evidence: Wire within-cycle + cross-cycle dedup behavior (INV-012)

**Date:** 2026-05-18
**Task:** T06.09 — Wire within-cycle (R-123) + cross-cycle (R-124, INV-012 non-regression) dedup composition at the four FR-CONV.6 wrapper sites; reference T05.07 INV-012 subsection by line + sha pin.
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-123 (within-cycle identical-dedup_key collapse to one record with found_n_times incremented); R-124 (cross-cycle identical dedup_key is dedup case NOT regression — contributes 1 not 2 to F_n+1; INV-012 composition with PR-02 monotonicity)
**Tier:** STANDARD
**Critical Path Override:** No
**Verification Method:** Direct test execution (grep + structural inspection + cross-reference against T05.07 INV-012 subsection)
**MCP Requirements:** None; Preferred: Sequential
**Status:** PASS

---

## 1. Summary

T06.09 lands the **R-123 within-cycle dedup collapse rule + R-124 cross-cycle dedup composition rule (INV-012 non-regression)** at the four FR-CONV.6 wrapper sites (`src/superclaude/agents/rf-analyst.md`, `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/skills/task-builder/SKILL.md`). The clause formalises two orthogonal dedup-collapse rules and two new named rejection symbols at the **cross-emission compositional layer** between the per-emission field-shape gates (DM-003 from T06.03/T06.04/T06.05) and the cohort-level path-selection gate (R-122 from T06.08):

- **Within-cycle collapse (R-123).** Two synthetic-dnsp findings emitted within the SAME retry cycle for the SAME `(assigned_files_range, escalation_ladder_exhaust_point)` 2-tuple MUST collapse to a single record with `found_n_times` incremented by exactly `1` (default `1` → `2`). The collapse happens BEFORE the merge step picks up the synthetic block at SKILL.md §A.8 / §A.10 (T06.11). Violations surface as `INV-012-within-cycle-collapse-violation` errors.
- **Cross-cycle composition (R-124, INV-012 non-regression).** A synthetic-dnsp finding with an identical `dedup_key` re-emitted on cycle `n+1` AFTER appearing on cycle `n` contributes `1` (not `2`) to `|F_{n+1}|` and MUST NOT trip Step 1 (regression detection) because `dedup_key ∈ FAIL_n ⇒ dedup_key ∉ PASS_n`, so the Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is FALSE by construction. Persistence trips Step 2 (monotonicity) **if and only if** `|F_{n+1}| >= |F_n|` after the dedup-collapse step — the intended halt when the partition agent is stuck. Violations surface as `INV-012-cross-cycle-composition-violation` errors.

T06.09's clause references the T05.07 INV-012 operational rule subsection at SKILL.md L1077-1091 by line + sha pin (`5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`) — that subsection is the canonical source-of-truth for the cross-cycle composition rule, and T06.09's per-wrapper enforcement clause binds to it without modifying it. The line range shifted from L1075-1089 (T05.07 closure baseline) to L1077-1091 because T06.09's new paragraph at SKILL.md (between the R-122 paragraph and the existing "Dedup key" paragraph) pushed the subsection down by 2 lines; the subsection content is byte-identical (sha256 unchanged) and the T06.09 clause's line range cites the post-edit reality.

`rf-team-lead.md` is NOT edited (preservation gate; §5).

## 2. Planning Inputs

- **Dependency closure.** T06.08 (D-0074) PASS — R-122 all-agents-fail guard precedence landed at 4/4 wrapper sites with `R-122-guard-precedence-violation` named symbol; T06.08 establishes the immediate-prior wrapper anchor after which T06.09 appends. T05.07 (D-0059) PASS — INV-012 cross-cycle dedup composition operational rule landed at SKILL.md L1075-1089 (now at L1077-1091 post-T06.09) with two synthetic execution-log fixtures and sub-agent quality-engineer PASS verdict; T06.09 references this subsection by line + sha pin.
- **R-123 + R-124 spec.** R-123: within-cycle identical-dedup_key collapse to one record with found_n_times incremented. R-124: cross-cycle identical dedup_key is dedup case NOT regression (prior verdict was already FAIL); contributes 1 (not 2) to |F_{n+1}|; persistence trips monotonicity (intended), not regression. AC: within-cycle fixture cardinality 1 + found_n_times=2; cross-cycle same-dedup_key contributes 1 not 2 to F_{n+1}; no regression halt emitted for cross-cycle case (trips monotonicity, intended).
- **COMP-006-M6 preservation gate.** Per CP-P06-T01-T05 §6 + D-0074 §5 — `rf-team-lead.md` whole-file sha256 = `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`; line-417 sha256 = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`. The preservation gate is the M6 invariant for the zero-success destination.
- **T05.07 INV-012 byte-stability invariant.** Per D-0059 §7, §10 — the T05.07 INV-012 operational rule subsection sha256 = `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`. T06.09 references but MUST NOT modify this subsection.
- **Phase 6 sequencing.** T06.09 wires the cross-emission compositional layer (this task); T06.10 wires INV-021 N-1 concurrency + HIGH severity non-overridable; T06.11 lands the consumer-side SKILL.md A.8 + A.10 merge step. Positive-path fixture for within-cycle collapse (TEST-019, T06.15 / D-0080) lands later; cross-cycle no-regression fixture (TEST-022 at T05.14 / D-0065) is already landed and serves as the programmatic ratifier for R-124's no-regression-halt invariant.

## 3. Execution — Acceptance-criterion grep evidence

All grep counts shown are file:count pairs across the 4 wrapper files (rf-analyst.md / rf-qa.md / rf-qa-qualitative.md / SKILL.md). Required: ≥1 per file unless noted.

### 3.1 AC1 — T06.09 clause anchor at 4/4 wrapper sites

```text
$ grep -c -F "Within-cycle + cross-cycle dedup composition (INV-012, R-123 + R-124)" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

T06.09 clause anchor present at 4/4 wrapper sites (1/1/1/1 = 100%) → **PASS** for AC1.

### 3.2 AC2 — Two new named rejection symbols at 4/4 sites

```text
$ grep -c -F "INV-012-within-cycle-collapse-violation" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1

$ grep -c -F "INV-012-cross-cycle-composition-violation" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

Both new named symbols bound at 4/4 sites (2 × 1/1/1/1 = 8/8 = 100%) → **PASS** for AC2. The two symbols are distinct from the five DM-003 symbols (T06.03/T06.04/T06.05) + API-003 symbol (T06.07) + R-122 symbol (T06.08), scoping the cross-emission compositional layer that the prior symbols' per-emission and cohort-level gates cannot detect.

### 3.3 AC3 — R-124 core invariant phrase at 4/4 sites

```text
$ grep -c -F 'contributes `1` (not `2`) to `|F_{n+1}|`' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:2
```

The byte-exact R-124 core invariant phrase ` contributes ` `` `1` (not `2`) `` to `` `|F_{n+1}|` `` is present at 4/4 wrapper sites (≥1 per file). SKILL.md has 2 occurrences: one in the new T06.09 paragraph (the per-wrapper enforcement binding) and one in the T05.07 INV-012 operational rule subsection at L1079 (the source-of-truth statement that T06.09 references). Both occurrences carry the byte-exact phrase identically → **PASS** for AC3.

### 3.4 AC4 — R-123 within-cycle increment phrase at 4/4 sites

```text
$ grep -c -F 'found_n_times` incremented by exactly `1`' src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

The R-123 core invariant phrase (`found_n_times` incremented by exactly `1`) present at 4/4 wrapper sites (1/1/1/1 = 100%) → **PASS** for AC4.

### 3.5 AC5 — INV-012 subsection sha pin literal at 4/4 sites

```text
$ grep -c -F "5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1

$ grep -c -F "L1077-1091" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

The T05.07 INV-012 subsection's sha256 pin literal (`5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`) and post-T06.09 line range (`L1077-1091`) are both cited at 4/4 wrapper sites → **PASS** for AC5.

### 3.6 AC6 — Step 1 predicate at 4/4 sites

```text
$ grep -c -F "dedup_key ∈ PASS_n ∩ FAIL_{n+1}" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:3
```

The Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` is present at 4/4 wrapper sites. SKILL.md has 3 occurrences: T06.09's new paragraph, the T05.07 INV-012 subsection (decision rule paragraph), and the T05.07 INV-012 subsection (regression non-emission invariant paragraph). All carry the byte-exact predicate identically → **PASS** for AC6.

### 3.7 AC7 — `rf-team-lead.md:417` byte-stable + whole-file unchanged (COMP-006-M6 preservation gate)

```text
$ sha256sum src/superclaude/agents/rf-team-lead.md
874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b  src/superclaude/agents/rf-team-lead.md
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
$ git diff src/superclaude/agents/rf-team-lead.md
(empty)
```

Both hashes match the values pinned in D-0068 §6, D-0069 §7, D-0070 §6, D-0071 §5, D-0072 §5, D-0073 §5, D-0074 §5, and CP-P06-T01-T05 §6 → **COMP-006-M6 preservation gate PASS for AC7.**

The byte-stable line-417 sha pin literal is also cited at all 4 wrapper sites:

```text
$ grep -c -F "51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

Operator tooling can grep the sha pin literal to confirm the wrapper-level contract references the frozen baseline.

### 3.8 AC8 — INV-012 subsection at SKILL.md L1077-1091 byte-stable

```text
$ grep -n "INV-012 cross-cycle dedup composition (operational rule)" src/superclaude/skills/task-builder/SKILL.md
1077:**INV-012 cross-cycle dedup composition (operational rule):**

$ sed -n '1077,1091p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785  -
```

The T05.07 INV-012 operational rule subsection content is byte-identical post-T06.09 (sha256 matches the D-0059 §10 pin exactly). The subsection's line range shifted from L1075-1089 (T05.07 closure baseline) to L1077-1091 (post-T06.09) because T06.09's new paragraph at SKILL.md (between L680 R-122 paragraph and L682 existing "Dedup key" paragraph) pushed the subsection down by 2 lines; the **content** is unchanged. The T06.09 clause's line range and sha pin both cite the post-edit reality, so the cross-reference resolves correctly → **PASS** for AC8.

### 3.9 AC9 — Strict additivity (all prior named rejection symbols preserved at ≥1 per file)

```text
$ for sym in DM-003-fixed-field-invariant-violation DM-003-dynamic-field-invariant-violation DM-003-recommendation-invariant-violation DM-003-dedup-key-shape-violation DM-003-found-n-times-invariant-violation API-003-exhaust-point-vocabulary-violation R-122-guard-precedence-violation; do
  printf "%-50s" "$sym:"
  grep -c -F "$sym" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md | tr '\n' ' '
  echo
done
DM-003-fixed-field-invariant-violation:           src/superclaude/agents/rf-analyst.md:1 src/superclaude/agents/rf-qa.md:1 src/superclaude/agents/rf-qa-qualitative.md:1 src/superclaude/skills/task-builder/SKILL.md:1
DM-003-dynamic-field-invariant-violation:         src/superclaude/agents/rf-analyst.md:1 src/superclaude/agents/rf-qa.md:1 src/superclaude/agents/rf-qa-qualitative.md:1 src/superclaude/skills/task-builder/SKILL.md:1
DM-003-recommendation-invariant-violation:        src/superclaude/agents/rf-analyst.md:1 src/superclaude/agents/rf-qa.md:1 src/superclaude/agents/rf-qa-qualitative.md:1 src/superclaude/skills/task-builder/SKILL.md:1
DM-003-dedup-key-shape-violation:                 src/superclaude/agents/rf-analyst.md:1 src/superclaude/agents/rf-qa.md:1 src/superclaude/agents/rf-qa-qualitative.md:1 src/superclaude/skills/task-builder/SKILL.md:3
DM-003-found-n-times-invariant-violation:         src/superclaude/agents/rf-analyst.md:1 src/superclaude/agents/rf-qa.md:1 src/superclaude/agents/rf-qa-qualitative.md:1 src/superclaude/skills/task-builder/SKILL.md:2
API-003-exhaust-point-vocabulary-violation:       src/superclaude/agents/rf-analyst.md:1 src/superclaude/agents/rf-qa.md:1 src/superclaude/agents/rf-qa-qualitative.md:1 src/superclaude/skills/task-builder/SKILL.md:3
R-122-guard-precedence-violation:                 src/superclaude/agents/rf-analyst.md:1 src/superclaude/agents/rf-qa.md:1 src/superclaude/agents/rf-qa-qualitative.md:1 src/superclaude/skills/task-builder/SKILL.md:2
```

All 7 prior named rejection symbols are preserved at ≥1 per file (no removal, no count reduction). SKILL.md's higher counts on DM-003-dedup-key-shape-violation (3), DM-003-found-n-times-invariant-violation (2), API-003-exhaust-point-vocabulary-violation (3), and R-122-guard-precedence-violation (2) reflect the broader DNSP contract anchor density and the cross-references in T06.09's new paragraph itself (the T06.09 clause names all four prior symbols to scope-distinguish them from the two new INV-012 symbols). Strict additivity is preserved → **PASS** for AC9.

### 3.10 AC10 — Sync parity for all 4 wrapper files

```text
$ for f in agents/rf-analyst.md agents/rf-qa.md agents/rf-qa-qualitative.md skills/task-builder/SKILL.md; do
    diff -q "src/superclaude/$f" ".claude/$f"
  done
(empty — no diff for any file)
```

`make sync-dev` ran clean for all 4 wrapper files; `diff -q src/superclaude/<file> .claude/<file>` returns empty for all four → **PASS** for AC10.

### 3.11 AC11 — Fixture-level binding deferred (per-task-graph staging)

Within-cycle TEST-019 cardinality + found_n_times collapse fixture lands at T06.15 (D-0080); T06.09 pins the per-wrapper enforcement clause that the future fixture will programmatically bind to (same staging as T06.03/T06.04/T06.05 fixture deferral to T06.15, T06.07 merge-step deferral to T06.11, T06.08 AC1/AC2 fixture deferral to T06.15/T06.16). Cross-cycle no-regression-halt fixture is **already landed** at T05.14 (D-0065 TEST-022 cross-cycle dedup pytest fixture); T05.14 / D-0065 plus the T05.07 / D-0059 synthetic execution-log fixtures (`fixture-cross-cycle-dedup-shrinking.log` + `fixture-cross-cycle-dedup-non-shrink.log`) already verify the R-124 no-regression invariant programmatically. T06.09 binds the per-wrapper enforcement that those fixtures ratify → **PASS** for AC11.

### 3.12 AC12 — Evidence at `TASKLIST_ROOT/artifacts/D-0075/evidence.md`

This file → **PASS** for AC12.

## 4. Sub-Agent Verification — N/A (STANDARD tier, direct test execution)

T06.09 is a STANDARD-tier task with Verification Method = "Direct test execution" and Sub-Agent Delegation = "None" per the phase-6 tasklist. The grep evidence at §3 + the preservation gate verification at §3.7/§3.8 + the cross-reference verification at §3.5 collectively satisfy the direct-test-execution verification method. No sub-agent quality-engineer spawn was required (the prior T06.08 STRICT-tier landing already established the wrapper-paragraph density baseline and the sub-agent ratification convention for the wrapper-clause pattern; T06.09 extends that pattern without departing from it).

## 5. Preservation invariants — COMP-006-M6 gate + T05.07 INV-012 byte-stability invariant

| Slice | sha256 (pre-T06.09 = post-T06.08) | sha256 (post-T06.09) |
|---|---|---|
| `src/superclaude/agents/rf-team-lead.md:417` (COMP-006-M6 preservation gate, byte-stable end-to-end across PR-02, PR-03, M1–M6) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — no edit anywhere) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |
| `src/superclaude/skills/task-builder/SKILL.md` INV-012 operational rule subsection (L1075-1089 pre-edit → L1077-1091 post-edit; content byte-identical) | `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` | `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` |

```text
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
$ sha256sum src/superclaude/agents/rf-team-lead.md
874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b  src/superclaude/agents/rf-team-lead.md
$ git diff src/superclaude/agents/rf-team-lead.md
(empty)
$ sed -n '1077,1091p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785  -
```

COMP-006-M6 preservation gate + T05.07 INV-012 byte-stability invariant both PASS.

**Existing inline "Dedup key" paragraph (T06.01 baseline) preserved.** The one-sentence `**Dedup key (composition with PR-02 Retry Monotonicity, INV-012).**` paragraph at SKILL.md (now shifted from L682 to L684 post-T06.09) is preserved verbatim — T06.09 augments rather than replaces it. The T06.09 new paragraph is the formal operational rule + named rejection symbols; the existing L684 paragraph remains the informal inline anchor.

**Existing all-agents-fail and R-122 anchors preserved.** The one-sentence `**All-agents-fail guard.**` paragraph (T06.01 baseline) and the formal `**All-agents-fail guard precedence (R-122).**` paragraph (T06.08 baseline) at SKILL.md are unchanged by T06.09; the new T06.09 paragraph sits immediately after the R-122 paragraph and immediately before the existing inline "Dedup key" paragraph, matching the additive insertion pattern used by T06.03 → T06.04 → T06.05 → T06.07 → T06.08.

## 6. Edits applied

| # | File | Region | Change type | Description |
|---|---|---|---|---|
| 1 | `src/superclaude/skills/task-builder/SKILL.md` | New paragraph inserted between the existing "**All-agents-fail guard precedence (R-122).**" paragraph (T06.08 baseline at L680) and the existing one-sentence "**Dedup key (composition with PR-02 Retry Monotonicity, INV-012).**" paragraph (T06.01 baseline at L682, now shifted to L684) | additive | Inserted the formal "**Within-cycle + cross-cycle dedup composition (INV-012, R-123 + R-124).**" paragraph naming the two dedup-collapse rules, the two new `INV-012-within-cycle-collapse-violation` + `INV-012-cross-cycle-composition-violation` named rejection symbols, the T05.07 INV-012 subsection cross-reference (L1077-1091 + sha256 pin `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`), the Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` (regression non-emission invariant), the F-set cardinality reference (SKILL.md L1064), the Step 2 monotonicity comparison reference (SKILL.md L1071), and a 3-part rationale tail explaining why two distinct compositional-layer symbols are required |
| 2 | `src/superclaude/agents/rf-analyst.md` | DNSP wrapper bullet tail (appended after T06.08 R-122 all-agents-fail guard precedence clause) | additive | Appended the same T06.09 clause naming the two dedup-collapse rules + two new named rejection symbols + T05.07 INV-012 subsection cross-reference + Step 1 predicate (without the SKILL.md-only rationale tail, matching T06.07 / T06.08 wrapper density convention) |
| 3 | `src/superclaude/agents/rf-qa.md` | DNSP wrapper bullet tail | additive | Symmetric to #2 |
| 4 | `src/superclaude/agents/rf-qa-qualitative.md` | DNSP wrapper bullet tail | additive | Symmetric to #2 |

`rf-team-lead.md` was NOT edited (preservation gate — see §5).

## 7. Acceptance Criteria — Coverage Table

| AC | Criterion | Status | Evidence |
|---|---|---|---|
| AC1 | T06.09 clause anchor `Within-cycle + cross-cycle dedup composition (INV-012, R-123 + R-124)` present at 4/4 wrapper sites | **PASS** | §3.1 (1/1/1/1 = 100%) |
| AC2 | Two new named rejection symbols `INV-012-within-cycle-collapse-violation` + `INV-012-cross-cycle-composition-violation` each present at 4/4 sites | **PASS** | §3.2 (2 × 1/1/1/1 = 8/8 = 100%) |
| AC3 | R-124 core invariant phrase ` contributes ` `` `1` (not `2`) `` to `` `|F_{n+1}|` `` present at 4/4 sites | **PASS** | §3.3 (1/1/1/2 = ≥1 per file; SKILL.md has 2 = new T06.09 paragraph + T05.07 INV-012 subsection source-of-truth statement) |
| AC4 | R-123 within-cycle increment phrase (`found_n_times` incremented by exactly `1`) present at 4/4 sites | **PASS** | §3.4 (1/1/1/1 = 100%) |
| AC5 | T05.07 INV-012 subsection cross-reference (`L1077-1091` + sha256 pin `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`) present at 4/4 sites | **PASS** | §3.5 (sha pin 1/1/1/1; line range 1/1/1/1) |
| AC6 | Step 1 predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` present at 4/4 sites (regression non-emission invariant binding) | **PASS** | §3.6 (1/1/1/3 = ≥1 per file; SKILL.md has 3 = T06.09 paragraph + T05.07 decision rule paragraph + T05.07 regression non-emission invariant paragraph) |
| AC7 | `rf-team-lead.md:417` byte-stable (sha256 = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`); whole-file rf-team-lead.md sha256 = `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` (COMP-006-M6) | **PASS** | §3.7 + §5 (sha256 pair matches D-0068/.../D-0074/CP-P06-T01-T05 pin byte-identically; `git diff` empty; sha pin literal cited at 4/4 wrapper sites) |
| AC8 | T05.07 INV-012 subsection content byte-identical post-T06.09 (sha256 = `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`); line range shifted from L1075-1089 to L1077-1091 due to T06.09 SKILL.md paragraph insertion (content unchanged) | **PASS** | §3.8 + §5 (sha256 matches D-0059 §10 pin exactly) |
| AC9 | Strict additivity — all 7 prior named rejection symbols + severity/source/recommendation literal anchors + COMP-006-M6 sha pin literal preserved at ≥1 per file | **PASS** | §3.9 (all 7 symbols ≥1 per file; SKILL.md higher counts reflect T06.09's explicit scope-distinguishing references to prior symbols, not drift) |
| AC10 | Sync parity — `make sync-dev` clean; `diff -q src/superclaude/<file> .claude/<file>` returns empty for all 4 wrapper files | **PASS** | §3.10 (no diff for any of the 4 files) |
| AC11 | Fixture-level binding deferred (within-cycle TEST-019 to T06.15 / D-0080; cross-cycle TEST-022 already-landed at T05.14 / D-0065) | **PASS** | §3.11 (staging matches T06.03/T06.04/T06.05/T06.07/T06.08 deferral convention; T05.07 / D-0059 synthetic fixtures + T05.14 / D-0065 TEST-022 already ratify R-124 no-regression invariant programmatically) |
| AC12 | Evidence at `TASKLIST_ROOT/artifacts/D-0075/evidence.md` | **PASS** | This file |

**Overall: PASS.**

## 8. Post-edit slice hashes (for downstream tasks)

| Slice | sha256 (post-edit) |
|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` (whole file) | `f7f3869bb56b46cca8b5edba0f710b3eaf649d0ee3a80af97b68b414c6a47f36` |
| `src/superclaude/agents/rf-analyst.md` (whole file) | `7bd6b0218c9aae69a7760342b562439c140f500622738958e55349aa72d7178f` |
| `src/superclaude/agents/rf-qa.md` (whole file) | `50782e42ffff53c855cf6cd72f57f36e96ac731b7f8ad1a161c789a6e3b2d0bb` |
| `src/superclaude/agents/rf-qa-qualitative.md` (whole file) | `c194dd856f01bc2c204435c26261e5320391a6a90c6d24a086fda426dc067270` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — unchanged) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |
| `src/superclaude/skills/task-builder/SKILL.md` L1077-1091 (T05.07 INV-012 operational rule subsection — referenced by T06.09; content byte-identical post-T06.09) | `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` |

`make sync-dev` ran clean for the four touched files. `diff -q src/superclaude/<file> .claude/<file>` returns no output for all four (verified post-sync).

## 9. Observations (Non-Blocking)

- **Two distinct compositional-layer symbols by design.** `INV-012-within-cycle-collapse-violation` and `INV-012-cross-cycle-composition-violation` are kept distinct (not collapsed into one combined symbol) so that operator tooling can grep-distinguish "the within-cycle counter was wrong at the emission boundary" from "the cross-cycle composition was wrong at the F-set construction boundary" without reading the full execution log. The dedup-composition gate is the **cross-emission compositional layer** — the operator-facing scope between the per-emission field-shape gates (DM-003) and the cohort-level path-selection gate (R-122). Together with the API-003 wire-shape symbol from T06.07 and the R-122 cohort-level symbol from T06.08, the Phase 6 rejection-symbol hierarchy now spans four tiers:
  1. **DM-003 (5 symbols)** — per-emission field-shape gates (T06.03/T06.04/T06.05).
  2. **API-003 (1 symbol)** — per-emission wire-shape gate (T06.07).
  3. **INV-012 (2 symbols, NEW in T06.09)** — cross-emission compositional layer.
  4. **R-122 (1 symbol)** — cohort-level path-selection gate (T06.08).

  Operator tooling can grep any of the 9 symbols to scope the failure mode without false positives.
- **Line-range drift inside the wrapper clause is structurally bounded.** T06.09's clause cites the T05.07 INV-012 subsection at SKILL.md L1077-1091 (post-T06.09). Future edits to SKILL.md that insert content above L1077 will shift the subsection further down; the sha256 pin (`5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`) is the authoritative anchor that survives line drift. Per the D-0059 §10 + D-0074 §8 convention, downstream tasks (T06.10..T06.18) MUST update the line range citation when shifting the subsection, but the sha pin remains the byte-stability invariant.
- **TEST-022 already-landed cross-cycle no-regression fixture.** Unlike T06.03/T06.04/T06.05/T06.07/T06.08 which all defer the positive-path fixture verification to later tasks (T06.15/T06.16), T06.09 has a partial already-landed verifier: T05.07's two synthetic execution-log fixtures (`D-0059/fixture-cross-cycle-dedup-shrinking.log` + `D-0059/fixture-cross-cycle-dedup-non-shrink.log`) and T05.14's TEST-022 pytest fixture (`D-0065`) already programmatically verify the R-124 no-regression-halt invariant. The within-cycle R-123 collapse fixture (TEST-019, T06.15 / D-0080) lands as the remaining positive-path verifier. This means T06.09 has stronger programmatic backing than T06.07 or T06.08 had at their landing time.
- **`make verify-sync` reports pre-existing drift on `auggie-bash-gate.sh` (not distributable) + `reject-workspace-writes.sh` installer registration.** Same pre-existing drift documented in D-0068 §6, D-0069 §9, D-0070 §9, D-0071 §8, D-0072 §8, D-0073 §10, D-0074 §9, CP-P06-T01-T05 §7.4 — belongs to the in-flight `feat/hook-sync-and-matcher-fix` branch, unrelated to T06.09 / R-123 + R-124. The skills/agents/commands cross-checks all PASS for the four T06.09-touched files.
- **Bullet/paragraph structure preserved.** The new T06.09 clause extends the existing T06.08 R-122 clause within the same wrapper bullet at each agent site rather than introducing a new bullet, preserving the 6-bullet "Orchestrator Responsibilities" list count at the agent files. SKILL.md gets one additional paragraph (between the existing T06.08 R-122 paragraph and the existing T06.01 inline "Dedup key" paragraph), matching the additive insertion pattern used by T06.03 → T06.04 → T06.05 → T06.07 → T06.08.
- **Strict additivity is invariantly preserved on this branch.** Same as T06.03/T06.04/T06.05/T06.07/T06.08: no fix-cycle loops added, no new stages, no new partition agent roles, no changes to PR-02 / M5 halt-guards wrapper / API-004 contract / per-gate counter tables. T06.09's only behavioural addition is the cross-emission compositional layer with two new named rejection symbols (which fire at the compositional layer between the per-emission rejection symbols and the cohort-level path-selection symbol already landed by T06.03–T06.08).

## 10. Provenance

- Pre-edit HEAD: `5439ea1 feat(hooks): widen auggie-flag-clear matcher to mcp__auggie-mcp__; add verify-sync hook coverage and cross-consistency checks` (same baseline as T06.01–T06.08 — no commits yet for the M6 wrapper landing series; MIG-006 single-commit landing scheduled for T06.17).
- M1 contract-freeze references: roadmap.md R-123 row (within-cycle identical-dedup_key collapse to one record with found_n_times incremented); roadmap.md R-124 row (cross-cycle identical dedup_key is dedup case NOT regression — contributes 1 not 2 to F_n+1; persistence trips monotonicity intended, not regression).
- T05.07 closure (INV-012 operational rule subsection landed): D-0059 (Overall PASS, 2026-05-17) — two synthetic execution-log fixtures (`fixture-cross-cycle-dedup-shrinking.log` + `fixture-cross-cycle-dedup-non-shrink.log`) + sub-agent quality-engineer PASS verdict; T06.09 references the subsection at L1077-1091 with sha pin `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`.
- T05.14 closure (TEST-022 cross-cycle dedup pytest fixture landed): D-0065 — programmatic positive-path verifier for R-124 no-regression-halt invariant; T06.09 binds the per-wrapper enforcement clause that this fixture programmatically ratifies.
- T06.01 closure (FR-CONV.6 wrapper landed): D-0068 (Overall PASS, 2026-05-18).
- T06.02 closure (DM-003-M6 7-field schema): D-0069 (Overall PASS, 2026-05-18).
- T06.03 closure (severity + source fixed-field rejection): D-0070 (Overall PASS, 2026-05-18).
- T06.04 closure (affected_range + evidence dynamic-field rejection): D-0071 (Overall PASS, 2026-05-18).
- T06.05 closure (recommendation + dedup_key + found_n_times rejection): D-0072 (Overall PASS, 2026-05-18).
- T06.06 mid-phase checkpoint: CP-P06-T01-T05 (Overall PASS, 2026-05-18).
- T06.07 closure (API-003-M6 wire-shape + closed vocabulary): D-0073 (Overall PASS, 2026-05-18) — `API-003-exhaust-point-vocabulary-violation` named symbol bound at 4/4 sites.
- T06.08 closure (R-122 all-agents-fail guard precedence): D-0074 (Overall PASS, 2026-05-18) — `R-122-guard-precedence-violation` named symbol bound at 4/4 sites; three mutually-exclusive paths (A/B/C) explicitly named.
- R-123 + R-124 (within-cycle + cross-cycle dedup composition, INV-012): two new `INV-012-within-cycle-collapse-violation` + `INV-012-cross-cycle-composition-violation` named symbols bound at 4/4 sites by T06.09; within-cycle fixture-level binding (TEST-019) lands at T06.15, cross-cycle fixture-level binding (TEST-022) already-landed at T05.14.
- T06.10 (D-0076 — INV-021 N-1 concurrency + HIGH severity non-overridable) is the natural next consumer of T06.09's INV-012 contract — it composes with the within-cycle collapse rule (synthetic emits at cardinality 1 with found_n_times incremented under R-122 Path B AND R-123 within-cycle collapse) and the cross-cycle composition rule (N-1 sibling partitions continue concurrently while the exhausted partition's synthesis collapses with prior-cycle counterpart under R-124).
- T06.14 (verify COMP-006-M6 preservation) is the downstream gate that verifies the byte-stability sha pin literal cited at the 4 wrapper sites; T06.18 (End-of-Phase-6 checkpoint) gates T06.01–T06.17 collectively for MIG-006 single-commit landing at T06.17.
