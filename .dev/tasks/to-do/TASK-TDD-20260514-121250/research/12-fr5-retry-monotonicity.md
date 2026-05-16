# Research: FR-CONV.5 (PR-02) Monotonicity + Regression Guards Insertion Points

**Status:** In Progress
**Date:** 2026-05-14
**Agent type:** Code Tracer
**CASE:** D (sc:tasklist has roadmap-validation stop-conditions; task-builder has 3-cycle hard limit — related but non-conflicting)
**Conflict-register row:** PR-02
**Protected invariant:** zero-trust QA (halt MUST NOT mask remaining failures)
**Lands:** 5th of 6 FRs

---

## 1. Verified-Current Insertion Points

### Site #1 — `src/superclaude/skills/task-builder/SKILL.md` lines 867–873 (PRD cites 870)

```
3. **NEED_USER_INPUT flow** (unresolvable user-intent ambiguity): Since the builder runs as a fire-and-forget Agent subagent, it cannot pause mid-execution to ask the orchestrator questions. If the builder encounters an ambiguity that cannot be inferred from research, it documents the ambiguity in the task file's **Open Questions** section and proceeds with the most reasonable interpretation. The user reviews Open Questions when the task file is presented (A.11) and can modify the task file before execution.

These are SEPARATE retry counters — a builder that returns RESEARCH_NEEDED twice and then produces a malformed file gets 2+2=4 total invocations maximum.

### A.10: Task File Validation
```

**Context:** Tail of section A.9 (Builder mediation) closing paragraph asserting the "SEPARATE retry counters" invariant for RESEARCH_NEEDED (max 2) and MALFORMED (max 2) — the 4-counter invariant that MUST NOT be collapsed into shared monotonicity state. The Retry Monotonicity Protocol section needs to land here, immediately after this paragraph, as a new subsection that augments — not replaces — the existing separate-counter rule.

### Site #2 — `src/superclaude/skills/task-builder/SKILL.md` lines 1547–1553 (PRD cites 1550)

```
11. **Multi-track isolation.** Failure in one track MUST NOT prevent other tracks from completing. Each track is independent — failed tracks are reported alongside successful ones.

12. **Builder mediation has separate retry counters.** RESEARCH_NEEDED (max 2 rounds) and MALFORMED (max 2 rounds) are tracked independently. A builder that needs more research twice and then produces a bad file gets 4 total invocations, not 2.

13. **No team infrastructure.** This skill uses the Agent tool exclusively. NEVER use TeamCreate, TeamDelete, SendMessage, TaskCreate (with team_name), or TaskUpdate. All agents receive ESCALATION blocks overriding their team-based defaults.
```

**Context:** Inside the "Behavioral Constraints" / hard invariants list. Item 12 restates the separate-retry-counter rule. The Retry Monotonicity Protocol invariant should be inserted as item 12.5 (or as a new item between 12 and 13) so the F-set shrinkage / regression rule sits adjacent to its sibling invariant about per-counter independence.

### Site #3 — `src/superclaude/agents/rf-task-builder.md` lines 334–361 (PRD cites 336–359)

```
---

## QA Gate, Validation, and Testing Encoding (BUILD_REQUEST Fields)

When the BUILD_REQUEST includes `QA_GATE_REQUIREMENTS`, `VALIDATION_REQUIREMENTS`, or `TESTING_REQUIREMENTS`, you MUST encode corresponding checklist items in the generated task file. These fields are not informational — they are mandatory instructions.

### QA_GATE_REQUIREMENTS

| Value | What to Encode |
|-------|---------------|
| `NONE` | No QA gate checklist items needed |
| `FINAL_ONLY` | Include a single QA validation phase before the final completion phase. This phase spawns rf-qa to verify all task outputs before marking Done. |
| `PER_PHASE` | Include QA gate checklist items after each major execution phase. Each gate spawns rf-qa (and optionally rf-qa-qualitative) to verify the preceding phase's outputs before proceeding. Use the M1 Phase-Gate QA Sequence pattern (Template 02) or the Phase Gate template section (both templates) from I15. |

**QA gate items follow B2 self-contained pattern.** Each item must specify: the agent to spawn, the QA phase type, the input files to verify, the output report path, the verdict handling (proceed on PASS, fix cycle on FAIL), and the error handling clause.

**Fix cycle limits per gate type (from I16):**

| Gate Type | Max Cycles | After Max |
|-----------|-----------|-----------|
| research-gate | 3 | HALT and escalate |
| synthesis-gate | 2 | Open Questions |
| report-validation | 3 | HALT and escalate |
| task-integrity | 2 | Open Questions |
| Any qualitative gate | 3 | HALT and escalate |

### VALIDATION_REQUIREMENTS
```

**Context:** The QA Gate encoding section in rf-task-builder. The per-gate fix-cycle table currently encodes only the hard-cap dimension (max cycles + HALT/Open-Questions terminal action). FR-CONV.5 needs the monotonicity/regression rule embedded into the verdict-handling description, AND a "Halt Conditions Per Fix Cycle" subsection added that codifies the two stop-conditions BEFORE the existing max-cycles row trips.

### Site #4 — `src/superclaude/agents/rf-qa.md` lines 308–315 (PRD cites 310–313)

```
### Rules

- Maximum 3 fix cycles. After 3 cycles, if issues remain, HALT execution and ask the user for guidance. Do NOT convert unfixed findings to Open Questions.
- Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem.

---
```

**Context:** The "Fix Cycle Protocol → Rules" subsection of rf-qa.md. The second bullet already gestures at the monotonicity intuition ("Each cycle should have fewer issues than the previous one") but expresses it as a SHOULD with no halt verb and no regression case. FR-CONV.5 promotes this to a MUST with explicit `|F_{n+1}| >= |F_n|` semantics, adds the regression-precedence rule, and binds the verbatim halt message.

### Adjacent context: `src/superclaude/agents/rf-team-lead.md:417` (3-cycle cap)

```
- **Fix Cycles**: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings.
```

This is the 3-cycle hard limit referenced in §6 below — it is preserved and composes with the new monotonicity halts (which trip earlier when applicable).

---

## 2. Two Stop-Conditions (per PRD §14.1 FR-CONV.5)

**Definition.** Let `F_n` = the set of items with FAIL verdict at the end of fix cycle `n` (see §3 for identity definition). The Retry Monotonicity Protocol enforces two halts that fire BEFORE the existing 3-cycle hard cap is consulted:

### (a) Monotonicity guard

**Rule:** `F_n` MUST shrink strictly each cycle. Concretely, if `|F_{n+1}| >= |F_n|` (the set fails to shrink), the protocol halts.

**Halt emission (exact format):**

```
[HALT-MONOTONICITY] |F|=<n>
```

where `<n>` is the cardinality of `F_{n+1}` (the stagnant or growing count). After emission the fix-cycle loop exits and control returns to the caller as a halt verdict — no further cycle is attempted and no further QA gate is invoked under this fix-cycle counter.

### (b) Regression detection

**Rule:** If any item that held verdict PASS at cycle `n` flips to verdict FAIL at cycle `n+1`, the protocol halts immediately. **Regression detection has STRICT PRECEDENCE over the monotonicity guard** — regression check runs FIRST every cycle, monotonicity check runs SECOND. Even if `|F_{n+1}| < |F_n|` (set IS shrinking), a single PASS→FAIL flip on any item still halts.

**Halt emission (verbatim, must appear character-for-character):**

```
Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.
```

The substitutions are: `X.Y` → the item identifier in the task file's checklist numbering scheme; `N` → the cycle index at which that item last held PASS verdict. After emission the fix-cycle loop exits without consulting the monotonicity guard.

### Ordering invariant

For every cycle transition `n → n+1`:

1. **First**: compute regression set `R = { item ∈ items | verdict(item, n) = PASS ∧ verdict(item, n+1) = FAIL }`. If `R ≠ ∅`, emit regression halt for an arbitrary `item ∈ R` and exit.
2. **Second**: compute `|F_{n+1}|`. If `|F_{n+1}| >= |F_n|`, emit `[HALT-MONOTONICITY] |F|=|F_{n+1}|` and exit.
3. **Third**: if neither halt fired and `n+1` has reached the 3-cycle hard cap, fall through to the existing cap halt (HALT and escalate / Open Questions per gate type).
4. **Fourth**: otherwise, proceed to fix cycle `n+2`.

---

## 3. F-set Definition

**Definition.** `F_n` is the set of FAIL-verdict items at the end of fix cycle `n`, where the **identity of an item is its dedup-key**, NOT the item's checklist position or surface text.

Why dedup-key as identity:

- Two findings with different surface text but identical dedup-key represent the **same underlying defect** for monotonicity purposes — they count as one element of `F_n`.
- This is exactly what enables INV-012 composition with FR-CONV.6's synthetic-dnsp emissions: a synthetic finding emitted in cycle `n` and re-emitted in cycle `n+1` with the same dedup-key is the SAME element of `F`, not two.
- It also defends against trivial perturbations (renumbering, paragraph reflow, agent re-phrasing) that would otherwise spoof the monotonicity check.

`|F_n|` is the cardinality after dedup-key deduplication.

---

## 4. INV-012 Composition Rule

**Statement (verbatim semantics):**

Synthetic-dnsp findings emitted by FR-CONV.6 (DNSP — Do-Not-Silently-Pass) **count as failures** for `|F_n|` monotonicity. They are first-class members of `F` and contribute to both the regression check and the monotonicity-cardinality check.

**Exception (dedup case, NOT regression):** A synthetic finding with identical dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)` across consecutive cycles is a **dedup case** — the same `F` element persisting — and therefore:

- It is the **same element** of `F_n` and `F_{n+1}` (so it contributes `1`, not `2`, to either cardinality).
- It is **NOT a regression** even though it appeared in cycle `n+1` after cycle `n`, because its prior cycle verdict was already FAIL (synthetic emission = FAIL), not PASS.
- If it persists with no other change, the monotonicity guard WILL trip on cycle `n+1` (since `|F_{n+1}| >= |F_n|` — the persistent element prevents shrinkage). This is the **intended behavior**: a synthetic-dnsp finding that the team cannot dislodge in one cycle is exactly the runaway condition the monotonicity halt protects against.

**Composite dedup-key.** The dedup-key for synthetic-dnsp findings is the 2-tuple `(assigned_files_range, escalation_ladder_exhaust_point)`. For non-synthetic (organic QA) findings, the dedup-key is whatever the QA agent normally emits (typically a normalized rule-id + file-anchor pair). The monotonicity engine does not need to know which kind of dedup-key it is holding; it only needs equality.

---

## 5. Acceptance Criteria (from PRD §14.1 FR-CONV.5)

### Observable

- `|F_{n+1}| >= |F_n|` halts the fix-cycle loop with exact emission `[HALT-MONOTONICITY] |F|=<n>` where `<n>` is the stagnant/growing cardinality.
- A PASS@N → FAIL@N+1 flip on any item halts with the verbatim regression message **BEFORE** the monotonicity guard is consulted (precedence test).
- A synthetic-dnsp finding with identical dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)` across consecutive cycles does NOT count as a regression (its prior verdict was FAIL, not PASS). It WILL still trip monotonicity on the next cycle if nothing else changes — which is correct behavior.

### Verification

- **Stagnation fixture:** 3-cycle sequence with `|F| = 5, 5, 5` halts at cycle 2 with `[HALT-MONOTONICITY] |F|=5`. Cycle 3 is not attempted.
- **Regression fixture:** Item `2.3` PASS at cycle 1, FAIL at cycle 2 → halts with `Regression detected on Item 2.3 — previously PASS at cycle 1, now FAIL. Halt overrides monotonicity check.` regardless of whether `|F_2| < |F_1|`.
- **Dedup fixture:** Synthetic-dnsp finding with dedup-key `(A.1-A.5, ladder-step-3)` emitted in cycles 1 and 2; `|F|` drops `7 → 4 → 2` due to OTHER findings being resolved. Loop proceeds to cycle 3 (no regression, monotonicity holds because synthetic counts once per dedup-key and other findings shrink the set).
- **Source-code presence:** `grep -n "Retry Monotonicity Protocol" src/superclaude/skills/task-builder/SKILL.md` returns ≥2 lines (sites #1 and #2 above).

### Negative

- **Slow-cycle shrink MUST NOT be halted.** A sequence `|F| = 10, 9, 8` is valid — it shrinks by 1 each cycle, monotonicity holds, no halt. There is **no "shrinks too slowly" threshold** (X-003 REJECTED in PRD).
- **The 4 separate retry counters MUST NOT be collapsed.** RESEARCH_NEEDED (max 2), MALFORMED (max 2), research-gate cycles (max 3), synthesis-gate cycles (max 2), report-validation cycles (max 3), task-integrity cycles (max 2), qualitative-gate cycles (max 3) all remain independent. Monotonicity tracks `F_n` PER fix-cycle counter, not as a shared global. (Site #1 / Site #2 invariants protect this.)
- **No halt-on-slow-convergence threshold.** There is no rule of the form "if shrinkage rate < K per cycle, halt." Only strict non-shrinkage and regression trip the new halts.

---

## 6. Coexistence with 3-cycle hard limit

The existing 3-cycle-per-phase hard limit in `rf-team-lead.md:417` ("max 3 cycles per phase ... HALT and ask user") is **preserved unchanged**. The per-gate fix-cycle table in `rf-task-builder.md:354–360` (research-gate: 3, synthesis-gate: 2, etc.) is also preserved unchanged.

**Composition order (per fix cycle transition):**

1. Regression check (new — FR-CONV.5).
2. Monotonicity check (new — FR-CONV.5).
3. Hard-cap check (existing — `rf-team-lead.md:417` and `rf-task-builder.md:354–360`).
4. Proceed to next cycle.

The two mechanisms compose cleanly:

- A **fast pathological loop** (5 items stuck at 5, or a PASS→FAIL flip) trips the new monotonicity/regression halt **first**, possibly in cycle 2, before the 3-cycle cap is ever consulted.
- A **slow-but-honest grind** (10 → 9 → 8 over three cycles) passes the new checks every cycle and stops at the existing hard cap — `[HALT-MONOTONICITY]` is NOT emitted; the existing "HALT and escalate" path is used.
- A **clean resolution** (5 → 2 → 0) passes both new checks AND the hard cap (because `F_3 = ∅` resolves the gate).

No existing rule is removed or weakened. The new halts only ADD earlier exit paths for the pathological cases.

---

## 7. Dependencies on other FRs

- **FR-CONV.1 (Synth-vs-build gate)** — produces the per-cycle `F_n` count and per-item PASS/FAIL verdicts that the monotonicity engine consumes. Without FR-CONV.1's gate verdicts, there is no `F_n` to monitor. Strong upstream dependency.
- **FR-CONV.6 (DNSP — synthetic-dnsp findings)** — emits synthetic findings that the monotonicity engine consumes per the INV-012 composition rule in §4. Synthetic findings use the composite dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)`. FR-CONV.5 must be aware of this dedup-key shape so it can deduplicate correctly when computing `|F_n|`.
- **FR-CONV.2 (Execution context plumbing)** — landed earlier (3rd of 6) and provides the cycle-counter / verdict-history plumbing needed to compare cycle `n` to cycle `n+1`. The monotonicity engine reads from this execution context to detect regressions.
- **FR-CONV.3, FR-CONV.4** — no direct interaction with monotonicity logic; they affect other parts of the task-builder/QA pipeline.

---

## 8. Gaps and Questions

- **Per-counter scope confirmation needed.** The PRD says "MUST NOT collapse 4 retry counters into shared monotonicity state" but does not explicitly enumerate which counter family each `F_n` belongs to. Interpretation in this research: monotonicity is tracked per fix-cycle counter (per gate type — research-gate, synthesis-gate, report-validation, task-integrity, qualitative-gate) **and** the builder-mediation counters (RESEARCH_NEEDED, MALFORMED) are excluded from monotonicity (they are not gate-fix-cycles and have no `F_n` to monitor). TDD should make this explicit.
- **Item identity across re-numbering.** If the task file is re-generated between cycles (e.g., MALFORMED retry), item `2.3` in cycle 1 may not be item `2.3` in cycle 2. Dedup-key as identity (§3) protects monotonicity-cardinality, but the regression halt message format `Item X.Y` assumes stable numbering. TDD should specify whether the message uses the item's CURRENT cycle numbering or its dedup-key for human readability.
- **Empty-set transition.** If `|F_n| = 0`, the fix-cycle loop should terminate normally (gate PASS), not emit `[HALT-MONOTONICITY] |F|=0`. Strict `|F_{n+1}| >= |F_n|` with `|F_n| = 0` would falsely trigger. TDD must clarify that monotonicity check is only consulted when `|F_n| > 0` (or equivalently, that gate-PASS termination precedes the monotonicity check in cycle ordering).
- **Synthetic-dnsp dedup-key emission point.** FR-CONV.6 emits the composite dedup-key, but where exactly in the verdict envelope does it land? Site #3 (QA gate encoding) does not currently specify a dedup-key field. TDD-FR-CONV.6 should pin this; TDD-FR-CONV.5 should reference it.

---

## 9. Stale Documentation Found

- **`rf-qa.md:312`** currently says *"Each cycle should have fewer issues than the previous one. If issue count increases, flag this as a systemic problem."* This is a SHOULD with no halt verb and no regression case. Once FR-CONV.5 lands, this bullet becomes stale and MUST be replaced (not just amended) with the strict MUST-halt protocol. Risk: leaving the old bullet in place creates a contradictory soft-rule alongside the new hard-rule.
- **`rf-task-builder.md:354–360`** fix-cycle limits table describes only the hard-cap dimension and the terminal action (HALT/Open-Questions). It is not stale per se, but it is **incomplete** post-FR-CONV.5 — the table or its surrounding prose must reference the monotonicity/regression halts so encoded task files include the verdict-handling that triggers them.
- **No existing references to "Retry Monotonicity Protocol", "HALT-MONOTONICITY", or "monotonicity" in any of the three target files** — confirmed via `grep -n "Retry Monotonicity\|monotonicity\|HALT-MONOTONICITY"`. This is a clean greenfield insertion; no rename/migration needed.

---

## 10. Summary

FR-CONV.5 (PR-02) lands a two-part Retry Monotonicity Protocol — strict `|F_{n+1}| >= |F_n|` halting with `[HALT-MONOTONICITY] |F|=<n>`, and regression detection with the verbatim halt message having precedence over monotonicity — across four verified insertion sites (task-builder SKILL.md:870 invariant tail, task-builder SKILL.md:1550 hard-invariants list, rf-task-builder.md:336–359 QA-gate encoding table, rf-qa.md:310–313 fix-cycle rules). `F_n` is defined by dedup-key identity, which is what makes INV-012 composition with FR-CONV.6 synthetic-dnsp findings work: synthetic findings count toward `|F|` but persistent same-dedup-key emissions are NOT regressions (their prior verdict was FAIL). The new halts compose cleanly with the existing 3-cycle hard cap in rf-team-lead.md:417 — they trip earlier on pathological loops without disturbing slow-but-honest grinds or clean resolutions. Two protected invariants from the conflict register survive intact: (i) the 4 separate retry counters remain independent (no shared monotonicity state), and (ii) zero-trust QA holds — halts emit specific verdict-bearing messages that do NOT mask remaining failures. The slow-convergence threshold proposed in X-003 was REJECTED in PRD; only strict non-shrinkage and regression trip the new halts.

---

**Status:** Complete
