# D-0076 — T06.10 Evidence: Wire INV-021 N-1 concurrency + R-126 HIGH severity non-overridable across merge step

**Date:** 2026-05-18
**Task:** T06.10 — Wire R-125 (INV-021 N-1 partition cohort concurrency invariant) + R-126 (HIGH severity non-overridable across merge step; synthetic emits ALONGSIDE — not IN PLACE OF — real findings)
**Phase:** Phase 6 — M6 Synthetic DNSP on Partition Exhaust
**Roadmap Item IDs:** R-125, R-126
**Tier:** STRICT
**Critical Path Override:** No
**Verification Method:** Sub-agent (quality-engineer) — STRICT-tier delegation required
**MCP Requirements:** Required: Sequential, Serena
**Status:** PASS

---

## 1. Summary

T06.10 lands the **R-125 INV-021 N-1 cohort concurrency invariant + R-126 HIGH severity non-overridable across merge step + real-findings-preservation invariant** at the four FR-CONV.6 wrapper sites (`src/superclaude/agents/rf-analyst.md`, `src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/skills/task-builder/SKILL.md`). The clause introduces three new named rejection symbols at the **execution-layer + merge-step layer** — the 5th tier of the Phase 6 rejection-symbol hierarchy, the layer that the prior per-emission gates (DM-003 ×5, API-003 ×1), cohort-level path-selection gate (R-122 ×1), and cross-emission compositional layer (INV-012 ×2) collectively cannot cover:

- **INV-021 N-1 cohort concurrency (R-125).** When one partition's escalation ladder exhausts, the orchestrator MUST allow the remaining N-1 sibling partitions to continue executing concurrently to their own success-or-exhaust terminal state **BEFORE** the exhausted partition's synthetic-dnsp emission is composed AND **BEFORE** the merge step at SKILL.md §A.8 / §A.10 runs. The exhausted partition's synthesis MUST NOT block, pause, serialize, or reduce the parallelism of the sibling cohort. Spawn-log timestamps are the evidence vehicle for the invariant. Violations surface as `INV-021-cohort-serialization-violation` errors.
- **R-126 HIGH severity non-overridable across merge step.** The per-emission `DM-003-fixed-field-invariant-violation` gate from T06.03 enforces `severity: HIGH` non-override at the emission boundary; T06.10 extends the invariant **transitively across the cohort-level merge step** at SKILL.md §A.8 / §A.10. No merge-time normalization, severity-downgrade transform, severity-coalesce rule, or operator-overridable severity flag is permitted to lower the synthetic-dnsp severity below HIGH. Violations surface as `R-126-severity-override-violation` errors (distinct from `DM-003-fixed-field-invariant-violation` — the DM-003 symbol scopes per-emission boundary failures, the R-126 symbol scopes merge-step / cohort-layer override failures across the emission lifecycle).
- **R-126 real findings preserved alongside synthetic.** The synthetic-dnsp block MUST be merged ALONGSIDE the real findings from the successful partitions (Path B from T06.08), **never IN PLACE OF** them. The cohort's real-finding count post-merge MUST equal the cohort's real-finding count pre-merge plus the synthetic count (strictly additive — not replacement, coalesce, or filter). Violations surface as `R-126-real-findings-replacement-violation` errors.

T06.10's wiring binds to the existing T06.09 INV-012 cross-emission compositional layer via citation update (`L1077-1091` → `L1079-1093` for the SKILL.md INV-012 operational rule subsection, which shifted down by 2 lines because T06.10 inserted a new paragraph at SKILL.md L684). The subsection content is byte-identical (sha256 unchanged at `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`); the line range citation update follows the D-0075 §10 convention for downstream tasks T06.10..T06.18.

`rf-team-lead.md` is NOT edited (COMP-006-M6 preservation gate; §5).

## 2. Planning Inputs

- **Dependency closure.** T06.09 (D-0075) PASS — INV-012 within-cycle + cross-cycle dedup composition landed at 4/4 wrapper sites with two new `INV-012-within-cycle-collapse-violation` + `INV-012-cross-cycle-composition-violation` named symbols; T06.09 establishes the immediate-prior wrapper anchor after which T06.10 appends. T06.08 (D-0074) PASS — R-122 all-agents-fail guard precedence landed Path B (`≥1-success AND ≥1-exhaust → synthetic-dnsp emits ALONGSIDE real findings`) — T06.10's R-126 real-findings-preservation invariant binds directly to this Path B. T06.03 (D-0070) PASS — `DM-003-fixed-field-invariant-violation` per-emission `severity: HIGH` gate — T06.10's R-126 severity-non-overridable invariant extends this transitively across the merge step.
- **R-125 + R-126 spec.** R-125: INV-021 N-1 concurrency invariant — on one partition's escalation exhaust, the N-1 sibling partitions continue concurrently to completion before exhausted one synthesises finding. R-126: HIGH severity non-overridable; synthetic emits ALONGSIDE (not IN PLACE OF) real findings.
- **COMP-006-M6 preservation gate.** Per CP-P06-T01-T05 §6 + D-0074 §5 + D-0075 §5 — `rf-team-lead.md` whole-file sha256 = `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b`; line-417 sha256 = `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0`. The preservation gate is the M6 invariant for the zero-success destination.
- **T05.07 INV-012 byte-stability invariant.** Per D-0059 §7, §10 + D-0075 §5 — the T05.07 INV-012 operational rule subsection sha256 = `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`. T06.10 references but MUST NOT modify this subsection. Line-range citation update from `L1077-1091` (post-T06.09 baseline) to `L1079-1093` (post-T06.10) follows the D-0075 §10 convention.
- **Phase 6 sequencing.** T06.10 wires the execution-layer + merge-step layer (this task); T06.11 lands the SKILL.md §A.8 + §A.10 consumer-side merge-step pick-up wiring (R-127 + R-128). Positive-path fixture for N-1 concurrency (TEST-021, T06.16 / D-0081) lands later; T06.10 pins the per-wrapper enforcement clause that the future fixture will programmatically bind to.

## 3. Execution — Acceptance-criterion grep evidence

All grep counts shown are file:count pairs across the 4 wrapper files (rf-analyst.md / rf-qa.md / rf-qa-qualitative.md / SKILL.md). Required: ≥1 per file unless noted.

### 3.1 AC1 — T06.10 clause anchor at 4/4 wrapper sites

```text
$ grep -c -F "INV-021 N-1 cohort concurrency + R-126 HIGH severity non-overridable across merge step (R-125 + R-126)" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

T06.10 clause anchor present at 4/4 wrapper sites (1/1/1/1 = 100%) → **PASS** for AC1.

### 3.2 AC2 — `INV-021-cohort-serialization-violation` named symbol at 4/4 sites

```text
$ grep -c -F "INV-021-cohort-serialization-violation" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

`INV-021-cohort-serialization-violation` symbol bound at 4/4 sites → **PASS** for AC2.

### 3.3 AC3 — `R-126-real-findings-replacement-violation` named symbol at 4/4 sites

```text
$ grep -c -F "R-126-real-findings-replacement-violation" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

`R-126-real-findings-replacement-violation` symbol bound at 4/4 sites → **PASS** for AC3.

### 3.4 AC4 — `R-126-severity-override-violation` named symbol at 4/4 sites

```text
$ grep -c -F "R-126-severity-override-violation" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

`R-126-severity-override-violation` symbol bound at 4/4 sites → **PASS** for AC4.

### 3.5 AC5 — R-125 N-1 concurrency invariant phrase at 4/4 sites

```text
$ grep -c -F "remaining N-1 sibling partitions to continue executing concurrently" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

R-125 N-1 concurrency phrase present at 4/4 sites → **PASS** for AC5.

### 3.6 AC6 — R-126 ALONGSIDE + strictly-additive + HIGH-non-overridable invariant phrases at 4/4 sites

```text
$ grep -c -F "ALONGSIDE the real findings from the successful partitions" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1

$ grep -c -F "strictly additive — not replacement, coalesce, or filter" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1

$ grep -c -F "MUST be non-overridable at every downstream layer" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

All 3 R-126 invariant phrases present at 4/4 sites → **PASS** for AC6.

### 3.7 AC7 — NFR-CONV.10 parallel-research invariant binding at 4/4 sites

```text
$ grep -c -F "NFR-CONV.10 parallel-research invariant" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

NFR-CONV.10 binding present at 4/4 sites → **PASS** for AC7.

### 3.8 AC8 — `rf-team-lead.md:417` byte-stable + whole-file unchanged (COMP-006-M6 preservation gate)

```text
$ sha256sum src/superclaude/agents/rf-team-lead.md
874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b  src/superclaude/agents/rf-team-lead.md
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
$ git diff src/superclaude/agents/rf-team-lead.md
(empty)
```

Both hashes match the values pinned in D-0068..D-0075 → **COMP-006-M6 preservation gate PASS for AC8.**

The byte-stable line-417 sha pin literal is also cited at all 4 wrapper sites (inherited from the T06.08 wrapper clause; no removal at T06.10):

```text
$ grep -c -F "51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

### 3.9 AC9 — INV-012 subsection sha-stable + line-range citation updated to L1079-1093

```text
$ grep -n "INV-012 cross-cycle dedup composition (operational rule)" src/superclaude/skills/task-builder/SKILL.md
1079:**INV-012 cross-cycle dedup composition (operational rule):**

$ sed -n '1079,1093p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785  -

$ grep -c "L1077-1091" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:0
src/superclaude/agents/rf-qa.md:0
src/superclaude/agents/rf-qa-qualitative.md:0
src/superclaude/skills/task-builder/SKILL.md:0

$ grep -c "L1079-1093" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md
src/superclaude/agents/rf-analyst.md:1
src/superclaude/agents/rf-qa.md:1
src/superclaude/agents/rf-qa-qualitative.md:1
src/superclaude/skills/task-builder/SKILL.md:1
```

The T05.07 INV-012 subsection content is byte-identical post-T06.10 (sha256 matches the D-0059 §10 pin exactly). The subsection's line range shifted from L1077-1091 (post-T06.09 baseline) to L1079-1093 (post-T06.10) because T06.10's new paragraph at SKILL.md (between L682 T06.09 paragraph and L684 existing "Dedup key" paragraph) pushed the subsection down by 2 lines; the **content** is unchanged. Per the D-0075 §10 convention, the line-range citation was updated at all 4 wrapper sites; the sha pin remains the byte-stability invariant. The old `L1077-1091` citation is no longer present at any wrapper site (0/0/0/0); the new `L1079-1093` citation is present at all 4 wrapper sites (1/1/1/1) → **PASS** for AC9.

### 3.10 AC10 — Strict additivity (all 9 prior named rejection symbols preserved at ≥1 per file)

```text
$ for sym in DM-003-fixed-field-invariant-violation DM-003-dynamic-field-invariant-violation DM-003-recommendation-invariant-violation DM-003-dedup-key-shape-violation DM-003-found-n-times-invariant-violation API-003-exhaust-point-vocabulary-violation R-122-guard-precedence-violation INV-012-within-cycle-collapse-violation INV-012-cross-cycle-composition-violation; do
  printf "%-50s" "$sym:"
  grep -c -F "$sym" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md src/superclaude/agents/rf-qa-qualitative.md src/superclaude/skills/task-builder/SKILL.md | tr '\n' ' '
  echo
done
DM-003-fixed-field-invariant-violation:           rf-analyst.md:1 rf-qa.md:1 rf-qa-qualitative.md:1 SKILL.md:2
DM-003-dynamic-field-invariant-violation:         rf-analyst.md:1 rf-qa.md:1 rf-qa-qualitative.md:1 SKILL.md:1
DM-003-recommendation-invariant-violation:        rf-analyst.md:1 rf-qa.md:1 rf-qa-qualitative.md:1 SKILL.md:1
DM-003-dedup-key-shape-violation:                 rf-analyst.md:1 rf-qa.md:1 rf-qa-qualitative.md:1 SKILL.md:3
DM-003-found-n-times-invariant-violation:         rf-analyst.md:1 rf-qa.md:1 rf-qa-qualitative.md:1 SKILL.md:3
API-003-exhaust-point-vocabulary-violation:       rf-analyst.md:1 rf-qa.md:1 rf-qa-qualitative.md:1 SKILL.md:4
R-122-guard-precedence-violation:                 rf-analyst.md:1 rf-qa.md:1 rf-qa-qualitative.md:1 SKILL.md:3
INV-012-within-cycle-collapse-violation:          rf-analyst.md:1 rf-qa.md:1 rf-qa-qualitative.md:1 SKILL.md:2
INV-012-cross-cycle-composition-violation:        rf-analyst.md:1 rf-qa.md:1 rf-qa-qualitative.md:1 SKILL.md:2
```

All 9 prior named rejection symbols are preserved at ≥1 per file (no removal, no count reduction). SKILL.md's higher counts on DM-003-fixed-field (2), DM-003-dedup-key-shape (3), DM-003-found-n-times (3), API-003-exhaust-point-vocabulary (4), R-122 (3), INV-012 ×2 (2 each) reflect the broader DNSP contract anchor density and the cross-references in T06.10's new paragraph itself (the T06.10 clause names all prior symbols to scope-distinguish them from the three new INV-021 + R-126 symbols). Strict additivity is preserved → **PASS** for AC10.

### 3.11 AC11 — Sync parity for all 4 wrapper files

```text
$ for f in agents/rf-analyst.md agents/rf-qa.md agents/rf-qa-qualitative.md skills/task-builder/SKILL.md; do
    diff -q "src/superclaude/$f" ".claude/$f"
  done
(empty — no diff for any file)
```

`make sync-dev` ran clean for all 4 wrapper files; `diff -q src/superclaude/<file> .claude/<file>` returns empty for all four → **PASS** for AC11.

### 3.12 AC12 — Sub-agent quality-engineer verification: PASS on all 12 checks

A quality-engineer sub-agent (agentId `ae81cacee4bbfe9f0`) was spawned to independently verify the 12 STRICT-tier criteria. The sub-agent report (full verdict: **PASS** on all 12 checks):

| # | Check | Verdict |
|---|---|---|
| 1 | Anchor presence at 4/4 sites | PASS |
| 2 | Three new named symbols (INV-021 + R-126 ×2) at 4/4 sites | PASS |
| 3 | R-125 invariant wording unambiguous (N-1 concurrent; non-blocking synthesis; spawn-log evidence) | PASS — exact phrases quoted |
| 4 | R-126 invariant wording unambiguous (ALONGSIDE; strictly-additive count; merge-step non-override) | PASS — exact phrases quoted |
| 5 | NFR-CONV.10 binding present | PASS |
| 6 | Symbol scope distinction correct (execution-layer + merge-step layer; DM-003 vs R-126 split) | PASS |
| 7 | COMP-006-M6 preservation (rf-team-lead.md whole-file + L417 sha; git diff empty) | PASS |
| 8 | T05.07 INV-012 subsection byte-stable; line-range citation updated to L1079-1093 | PASS |
| 9 | Sync parity (4/4 files) | PASS |
| 10 | Bullet/paragraph structure preserved | PASS |
| 11 | Mutual exclusivity / clause ordering at agent files (DM-003 → API-003 → R-122 → INV-012 → INV-021+R-126) | PASS |
| 12 | Rationale tail only in SKILL.md (3-part); not in agent files | PASS |

Sub-agent overall verdict: **PASS** on all 12 checks → **PASS** for AC12.

### 3.13 AC13 — Evidence at `TASKLIST_ROOT/artifacts/D-0076/evidence.md`

This file → **PASS** for AC13.

## 4. Sub-Agent Verification — quality-engineer (STRICT tier)

T06.10 is a STRICT-tier task requiring Sub-Agent Delegation per the phase-6 tasklist. A quality-engineer sub-agent (agentId `ae81cacee4bbfe9f0`) was spawned with explicit instructions to verify:
1. Anchor presence at 4/4 wrapper sites
2. Three new named symbols at each file
3. R-125 invariant wording (3 sub-points)
4. R-126 invariant wording (3 sub-points)
5. NFR-CONV.10 binding
6. Symbol scope distinction against 9 prior symbols
7. COMP-006-M6 preservation gate
8. T05.07 INV-012 subsection byte-stability + line-range citation update
9. Sync parity
10. Bullet/paragraph structure preservation
11. Mutual exclusivity / clause ordering
12. Rationale tail only in SKILL.md

The sub-agent independently performed all 12 checks via Read, Grep, and Bash. All 12 checks returned **PASS** with cited evidence (line numbers, sha256 hashes, exact quoted phrases). Overall sub-agent verdict: **PASS**.

## 5. Preservation invariants — COMP-006-M6 gate + T05.07 INV-012 byte-stability invariant

| Slice | sha256 (pre-T06.10 = post-T06.09) | sha256 (post-T06.10) |
|---|---|---|
| `src/superclaude/agents/rf-team-lead.md:417` (COMP-006-M6 preservation gate, byte-stable end-to-end across PR-02, PR-03, M1–M6) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — no edit anywhere) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |
| `src/superclaude/skills/task-builder/SKILL.md` INV-012 operational rule subsection (L1077-1091 pre-T06.10 → L1079-1093 post-T06.10; content byte-identical) | `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` | `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` |

```text
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
$ sha256sum src/superclaude/agents/rf-team-lead.md
874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b  src/superclaude/agents/rf-team-lead.md
$ git diff src/superclaude/agents/rf-team-lead.md
(empty)
$ sed -n '1079,1093p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785  -
```

COMP-006-M6 preservation gate + T05.07 INV-012 byte-stability invariant both PASS.

**Existing inline "Dedup key" paragraph (T06.01 baseline) preserved.** The one-sentence `**Dedup key (composition with PR-02 Retry Monotonicity, INV-012).**` paragraph at SKILL.md (now shifted from L684 to L686 post-T06.10) is preserved verbatim — T06.10 inserts before it.

**Existing all-agents-fail, R-122, INV-012 (R-123+R-124) wrapper paragraphs preserved.** The T06.01 baseline `**All-agents-fail guard.**` paragraph, the T06.08 baseline `**All-agents-fail guard precedence (R-122).**` paragraph, and the T06.09 baseline `**Within-cycle + cross-cycle dedup composition (INV-012, R-123 + R-124).**` paragraph at SKILL.md are unchanged by T06.10; the new T06.10 paragraph sits immediately after the T06.09 paragraph and immediately before the existing inline "Dedup key" paragraph, matching the additive insertion pattern used by T06.03 → T06.04 → T06.05 → T06.07 → T06.08 → T06.09.

## 6. Edits applied

| # | File | Region | Change type | Description |
|---|---|---|---|---|
| 1 | `src/superclaude/skills/task-builder/SKILL.md` | New paragraph inserted between the existing "**Within-cycle + cross-cycle dedup composition (INV-012, R-123 + R-124).**" paragraph (T06.09 baseline at L682) and the existing one-sentence "**Dedup key (composition with PR-02 Retry Monotonicity, INV-012).**" paragraph (T06.01 baseline at L684, now shifted to L686 post-T06.10) | additive | Inserted the formal "**INV-021 N-1 cohort concurrency + R-126 HIGH severity non-overridable across merge step (R-125 + R-126).**" paragraph naming the two invariants, the three new `INV-021-cohort-serialization-violation` + `R-126-real-findings-replacement-violation` + `R-126-severity-override-violation` named rejection symbols, the NFR-CONV.10 parallel-research invariant binding (with M6 governance entry reference at MIG-006 / T06.17), the cross-references to all 9 prior named symbols for scope distinction, and a 3-part rationale tail (per-cohort N-1 concurrency invariant; real-findings-preservation invariant; merge-step-layer HIGH non-overridable invariant). |
| 2 | `src/superclaude/skills/task-builder/SKILL.md` | T06.09 clause line-range citation | citation update | Updated `L1077-1091` → `L1079-1093` to reflect post-T06.10 line range of the T05.07 INV-012 operational rule subsection (sha pin unchanged at `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`) per D-0075 §10 convention. |
| 3 | `src/superclaude/agents/rf-analyst.md` | DNSP wrapper bullet tail (appended after T06.09 INV-012 dedup composition clause) | additive | Appended the same T06.10 clause naming the two invariants + three new named rejection symbols + NFR-CONV.10 binding + scope-distinction references (without the SKILL.md-only rationale tail, matching T06.07 / T06.08 / T06.09 wrapper density convention) |
| 4 | `src/superclaude/agents/rf-analyst.md` | T06.09 clause line-range citation | citation update | Updated `L1077-1091` → `L1079-1093` symmetric to #2 |
| 5 | `src/superclaude/agents/rf-qa.md` | DNSP wrapper bullet tail | additive | Symmetric to #3 |
| 6 | `src/superclaude/agents/rf-qa.md` | T06.09 clause line-range citation | citation update | Symmetric to #4 |
| 7 | `src/superclaude/agents/rf-qa-qualitative.md` | DNSP wrapper bullet tail | additive | Symmetric to #3 |
| 8 | `src/superclaude/agents/rf-qa-qualitative.md` | T06.09 clause line-range citation | citation update | Symmetric to #4 |

`rf-team-lead.md` was NOT edited (preservation gate — see §5).

## 7. Acceptance Criteria — Coverage Table

| AC | Criterion | Status | Evidence |
|---|---|---|---|
| AC1 | T06.10 clause anchor `INV-021 N-1 cohort concurrency + R-126 HIGH severity non-overridable across merge step (R-125 + R-126)` present at 4/4 wrapper sites | **PASS** | §3.1 (1/1/1/1 = 100%) |
| AC2 | `INV-021-cohort-serialization-violation` named symbol at 4/4 sites | **PASS** | §3.2 (1/1/1/1) |
| AC3 | `R-126-real-findings-replacement-violation` named symbol at 4/4 sites | **PASS** | §3.3 (1/1/1/1) |
| AC4 | `R-126-severity-override-violation` named symbol at 4/4 sites | **PASS** | §3.4 (1/1/1/1) |
| AC5 | R-125 N-1 concurrency invariant phrase (`remaining N-1 sibling partitions to continue executing concurrently`) at 4/4 sites | **PASS** | §3.5 (1/1/1/1) |
| AC6 | R-126 three invariant phrases (ALONGSIDE; strictly-additive count; HIGH non-overridable across merge step) at 4/4 sites | **PASS** | §3.6 (all three at 1/1/1/1) |
| AC7 | NFR-CONV.10 parallel-research invariant binding at 4/4 sites | **PASS** | §3.7 (1/1/1/1) |
| AC8 | `rf-team-lead.md:417` byte-stable (sha256 = `51725c0fff...`); whole-file rf-team-lead.md sha256 = `874a516e3b...` (COMP-006-M6) | **PASS** | §3.8 + §5 (sha256 pair matches D-0068/.../D-0075 pin byte-identically; `git diff` empty; sha pin literal cited at 4/4 wrapper sites) |
| AC9 | T05.07 INV-012 subsection content byte-identical post-T06.10 (sha256 = `5ff2a180...`); line range shifted from L1077-1091 to L1079-1093; citation updated at all 4 sites | **PASS** | §3.9 (sha256 matches D-0059 §10 pin; old citation = 0 at all sites; new citation = 1 at all sites) |
| AC10 | Strict additivity — all 9 prior named rejection symbols preserved at ≥1 per file | **PASS** | §3.10 (all 9 symbols ≥1 per file; SKILL.md higher counts reflect T06.10's explicit scope-distinguishing references to prior symbols, not drift) |
| AC11 | Sync parity — `make sync-dev` clean; `diff -q src/superclaude/<file> .claude/<file>` returns empty for all 4 wrapper files | **PASS** | §3.11 (no diff for any of the 4 files) |
| AC12 | Sub-agent quality-engineer verification: PASS on all 12 STRICT-tier verification checks | **PASS** | §3.12 + §4 (sub-agent agentId `ae81cacee4bbfe9f0`, overall PASS) |
| AC13 | Evidence at `TASKLIST_ROOT/artifacts/D-0076/evidence.md` | **PASS** | This file |

**Overall: PASS.**

## 8. Post-edit slice hashes (for downstream tasks)

| Slice | sha256 (post-T06.10) |
|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` (whole file) | `4b2ead830f6708cdfd5efcf111285d7f48263f512eac3a0a8c672810c0db4c0b` |
| `src/superclaude/agents/rf-analyst.md` (whole file) | `8d41ae8038769bb32eb56db78569235614c82aa3dc2170886237797ed9f8ff43` |
| `src/superclaude/agents/rf-qa.md` (whole file) | `fd2487860810d163f7c19263f830f08bcf4b9efede1bf89ed8c2ea9184ddc6e9` |
| `src/superclaude/agents/rf-qa-qualitative.md` (whole file) | `ed35b7884db1a2d6dfe1aa8a8bddb9b3308d4b268ba4892ad39956d6149883a1` |
| `src/superclaude/agents/rf-team-lead.md` (whole file — unchanged) | `874a516e3baedd8fed5b433592ab3d41a78bd8ec8601098d8610f47ce255e40b` |
| `src/superclaude/skills/task-builder/SKILL.md` L1079-1093 (T05.07 INV-012 operational rule subsection — referenced by T06.09 + T06.10; content byte-identical post-T06.10) | `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` |

`make sync-dev` ran clean for the four touched files. `diff -q src/superclaude/<file> .claude/<file>` returns no output for all four (verified post-sync).

## 9. Observations (Non-Blocking)

- **Five tiers in the rejection-symbol hierarchy.** T06.10 adds the 5th tier (execution-layer + merge-step layer) to the existing 4 tiers (DM-003 per-emission field-shape ×5; API-003 per-emission wire-shape ×1; R-122 cohort-level path-selection ×1; INV-012 cross-emission compositional layer ×2). The hierarchy is now: per-emission boundary (Tier 1) → per-emission wire-shape (Tier 2) → cohort-level path-selection (Tier 3) → cross-emission compositional layer (Tier 4) → execution-layer + merge-step layer (Tier 5). Operator tooling can grep any of the 12 symbols to scope a failure to its emergence boundary; the symbols are designed so that no two tiers can claim the same failure mode (each symbol is bound to a layer where its failure mode is uniquely diagnosable).
- **Line-range drift inside the wrapper clause is structurally bounded — convention enforced.** T06.10 enforces the D-0075 §10 convention by updating the T06.09 line-range citation from `L1077-1091` to `L1079-1093` at all 4 wrapper sites; the sha256 pin (`5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785`) remains the authoritative anchor that survives line drift. Downstream tasks (T06.11..T06.18) MUST continue the same convention: update the line range citation when shifting the subsection, but the sha pin remains the byte-stability invariant.
- **R-126 split into two named symbols by design.** `R-126-real-findings-replacement-violation` and `R-126-severity-override-violation` are kept distinct (not collapsed into one combined symbol) so that operator tooling can grep-distinguish "the merged report's information content was reduced (real findings were dropped/coalesced)" from "the merged report's synthetic-dnsp severity was downgraded below HIGH" without reading the full execution log. Both symbols emerge at the merge-step boundary but scope different failure modes (count pathology vs. severity-transform pathology).
- **R-126 severity-override-violation distinct from DM-003-fixed-field-invariant-violation by design.** The per-emission DM-003 gate from T06.03 catches `severity != HIGH` at the emitter (the wire format is malformed at emission time); the R-126 merge-step gate catches downstream override attempts that bypass the emitter (the wire format is well-formed at emission but the merge step applies a transform). Both layers are needed because the wire format is preserved post-emission but merge logic could still apply transforms — neither symbol is redundant with the other.
- **TEST-021 cohort-concurrency fixture deferred to T06.16 / D-0081.** T06.10 pins the per-wrapper enforcement clause that the future spawn-log-timestamp fixture will programmatically bind to (same staging as T06.03/T06.04/T06.05 fixture deferral to T06.15, T06.07 merge-step deferral to T06.11, T06.08 AC1/AC2 fixture deferral to T06.15/T06.16, T06.09 within-cycle TEST-019 deferral to T06.15). The TEST-022 cross-cycle no-regression fixture (already-landed at T05.14 / D-0065) does not bind R-125 directly but composes with the R-126 ALONGSIDE invariant (T06.10's strictly-additive merge invariant is the compositional invariant that lets the cross-cycle dedup-collapse step run without losing real findings).
- **`make verify-sync` reports pre-existing drift on `auggie-bash-gate.sh` (not distributable) + `reject-workspace-writes.sh` installer registration.** Same pre-existing drift documented in D-0068..D-0075 — belongs to the in-flight `feat/hook-sync-and-matcher-fix` branch, unrelated to T06.10 / R-125 + R-126. The skills/agents/commands cross-checks all PASS for the four T06.10-touched files.
- **Bullet/paragraph structure preserved.** The new T06.10 clause extends the existing T06.09 INV-012 clause within the same wrapper bullet at each agent site rather than introducing a new bullet, preserving the agent-file bullet count. SKILL.md gets one additional paragraph (between the existing T06.09 paragraph and the existing T06.01 inline "Dedup key" paragraph), matching the additive insertion pattern used by T06.03 → T06.04 → T06.05 → T06.07 → T06.08 → T06.09.
- **Strict additivity is invariantly preserved on this branch.** Same as T06.03/T06.04/T06.05/T06.07/T06.08/T06.09: no fix-cycle loops added, no new stages, no new partition agent roles, no changes to PR-02 / M5 halt-guards wrapper / API-004 contract / per-gate counter tables. T06.10's only behavioural addition is the execution-layer + merge-step layer with three new named rejection symbols (which fire at the execution-layer boundary for the N-1 concurrency invariant and at the merge-step boundary for the real-findings-preservation + HIGH-severity-non-override invariants).

## 10. Provenance

- Pre-edit HEAD: `5439ea1 feat(hooks): widen auggie-flag-clear matcher to mcp__auggie-mcp__; add verify-sync hook coverage and cross-consistency checks` (same baseline as T06.01–T06.09 — no commits yet for the M6 wrapper landing series; MIG-006 single-commit landing scheduled for T06.17).
- M1 contract-freeze references: roadmap.md R-125 row (INV-021: on one partition's escalation exhaust, N-1 sibling partitions continue concurrently to completion before exhausted one synthesises finding); roadmap.md R-126 row (HIGH severity: synthetic findings emit ALONGSIDE (not in place of) real findings from successful partitions).
- T05.07 closure (INV-012 operational rule subsection landed): D-0059 (Overall PASS, 2026-05-17) — two synthetic execution-log fixtures + sub-agent quality-engineer PASS verdict; T06.10 references the subsection at L1079-1093 with sha pin `5ff2a1803bbe088d2083628bf9c8cffeafba54fcc7b769efd98dd14824f09785` (line range shifted +2 from T06.09's L1077-1091 baseline; content byte-identical).
- T06.01 closure (FR-CONV.6 wrapper landed): D-0068 (Overall PASS, 2026-05-18).
- T06.02 closure (DM-003-M6 7-field schema): D-0069 (Overall PASS, 2026-05-18).
- T06.03 closure (severity + source fixed-field rejection): D-0070 (Overall PASS, 2026-05-18) — the per-emission `severity: HIGH` gate that T06.10 transitively extends across the merge step.
- T06.04 closure (affected_range + evidence dynamic-field rejection): D-0071 (Overall PASS, 2026-05-18).
- T06.05 closure (recommendation + dedup_key + found_n_times rejection): D-0072 (Overall PASS, 2026-05-18).
- T06.06 mid-phase checkpoint: CP-P06-T01-T05 (Overall PASS, 2026-05-18).
- T06.07 closure (API-003-M6 wire-shape + closed vocabulary): D-0073 (Overall PASS, 2026-05-18) — `API-003-exhaust-point-vocabulary-violation` named symbol.
- T06.08 closure (R-122 all-agents-fail guard precedence): D-0074 (Overall PASS, 2026-05-18) — `R-122-guard-precedence-violation` named symbol; three mutually-exclusive paths (A/B/C) explicitly named. T06.10's R-126 real-findings-preservation invariant binds directly to Path B.
- T06.09 closure (INV-012 within-cycle + cross-cycle dedup composition): D-0075 (Overall PASS, 2026-05-18) — two new `INV-012-within-cycle-collapse-violation` + `INV-012-cross-cycle-composition-violation` named symbols; established the line-range-update + sha-pin-stability convention that T06.10 enforces.
- R-125 + R-126 (INV-021 N-1 concurrency + HIGH non-overridable across merge + real-findings-preservation): three new `INV-021-cohort-serialization-violation` + `R-126-real-findings-replacement-violation` + `R-126-severity-override-violation` named symbols bound at 4/4 sites by T06.10; cohort-concurrency fixture-level binding (TEST-021) lands at T06.16 / D-0081.
- T06.11 (D-0077 — SKILL.md A.8 + A.10 merge-step pick-up wiring at R-127 + R-128) is the natural next consumer of T06.10's contract — the merge step at SKILL.md §A.8 (`:572-656`) and §A.10 (`:870-918`) MUST honor the T06.10 R-126 strictly-additive + HIGH-non-overridable invariants when picking up the synthetic block alongside real findings.
- T06.14 (verify COMP-006-M6 preservation) is the downstream gate that verifies the byte-stability sha pin literal cited at the 4 wrapper sites; T06.18 (End-of-Phase-6 checkpoint) gates T06.01–T06.17 collectively for MIG-006 single-commit landing at T06.17.
