# D-0058 — Evidence (T05.05 — Define F-set + ordering precedence rule)

**Task:** T05.05
**Roadmap items:** R-094, R-095
**Date:** 2026-05-17
**Branch:** `feat/mig-002-execution-context-header`
**Pre-edit HEAD:** `487e76b feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)`
**Tier:** STRICT
**Verification method:** Sub-agent (quality-engineer) — read-only ratification
**Overall: PASS** (4/4 AC met)

---

## 0. TL;DR

T05.05 ratifies — via the quality-engineer sub-agent — the F-set
identity definition (R-094) and the 4-step ordering precedence rule
(R-095) that T05.01 + T05.02 + T05.03 + T05.04 jointly landed in
`src/superclaude/skills/task-builder/SKILL.md`. T05.05 makes **zero
source-file edits**; the sub-agent report (§3-§7 below) confirms all
four acceptance criteria PASS verbatim against the landed SKILL.md
text and the preserved `rf-team-lead.md:417` and `rf-task-builder.md:
354-364` slices.

| AC | Statement (verbatim) | Sub-agent verdict | Evidence § |
|----|----------------------|-------------------|------------|
| AC1 | Documented precedence text explicitly states the 4-step order `regression → monotonicity → hard-cap → proceed` (regex match on the ordered string in SKILL.md) and sub-agent report confirms "regression always exits BEFORE monotonicity" | PASS | §3 + §4 |
| AC2 | F-set identity (dedup-key) explicitly stated in SKILL.md | PASS | §5 |
| AC3 | Existing rf-team-lead.md:417 hard-cap referenced as fallback | PASS | §6 |
| AC4 | Sub-agent quality-engineer report confirms 4-step ordering verbatim | PASS | §7 |

Preservation invariants (T05.01 + T05.02 + T05.03 + T05.04 baselines):
SKILL.md L1014-1027 sha256 `1ca8e16e…` unchanged; SKILL.md L1029-1059
sha256 `14c40575…` unchanged; `rf-team-lead.md:417` sha256 `51725c0f…`
unchanged; `rf-task-builder.md` L354-364 sha256 `121de142…` unchanged;
`make verify-sync` PASS.

---

## 1. Sub-agent identity and scope

The quality-engineer sub-agent was spawned read-only with the explicit
instruction "No edits permitted. Produce a structured verdict report."
The sub-agent inspected:

- `src/superclaude/skills/task-builder/SKILL.md` L1014-1027 (FR-CONV.5
  wrapper), L1029-1059 (API-004 contract block), L1042-1048 (F-set
  definition), L1050-1059 (4-step ordering rule), L1025 (INV-012
  composition).
- `src/superclaude/agents/rf-team-lead.md` L417 (3-cycle hard cap).
- `src/superclaude/agents/rf-task-builder.md` L354-364 (per-gate
  counter table).

The sub-agent's overall verdict is **PASS** with byte-exact verbatim
quotes for every step of the 4-step ordering rule, the F-set
definition, the INV-012 composition rule, and the hard-cap fallback
reference. The verbatim quotes are reproduced in §3-§7 below.

## 2. Pre-condition: rf-team-lead.md:417 hard cap still present (preservation check)

```
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md
- **Fix Cycles**: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings.

$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
```

Hash matches T05.01 / D-0054 §2.5 baseline, T05.02 / D-0055 §2.5
baseline, T05.03 / D-0056 §4.2 baseline, and T05.04 / D-0057 §4.3
baseline (`51725c0f…`). The 3-cycle hard cap referenced by Step 3 of
the 4-step ordering rule is byte-identical.

## 3. AC1 — Ordered-string regex match on `regression → monotonicity → hard-cap → proceed`

### 3.1 Verbatim matches in SKILL.md

```
$ grep -nE "regression → monotonicity → hard-cap → proceed" src/superclaude/skills/task-builder/SKILL.md
1021:**Precedence rule (regression > monotonicity).** Regression detection ALWAYS runs BEFORE the monotonicity check on every cycle transition `n → n+1`. When both conditions would trigger in the same cycle, the regression halt-message is emitted and the monotonicity check is NOT consulted on the regressed item. The full ordering chain (regression → monotonicity → hard-cap → proceed) is documented in the F-set + ordering precedence section.
1052:On every cycle transition `n → n+1`, run the following steps in this exact order and EXIT on the first match — `regression → monotonicity → hard-cap → proceed`:
```

Two byte-exact matches:

- **L1021** — wrapper-level cross-reference to the 4-step section.
- **L1052** — canonical 4-step preamble inside the API-004 contract
  block.

The ordered string is the literal sequence
`regression → monotonicity → hard-cap → proceed` with U+2192 right-
arrow separators. Both lines satisfy the AC1 regex match requirement.

### 3.2 Sub-agent AC1 quote (verbatim from sub-agent report)

> **AC1 — 4-step ordered string regex match:**
>
> - SKILL.md:1021: "The full ordering chain (regression → monotonicity → hard-cap → proceed) is documented in the F-set + ordering precedence section."
> - SKILL.md:1052: "On every cycle transition `n → n+1`, run the following steps in this exact order and EXIT on the first match — `regression → monotonicity → hard-cap → proceed`:"
> - **Conclusion: PASS** — the literal ordered string `regression → monotonicity → hard-cap → proceed` appears verbatim in SKILL.md at L1021 (wrapper cross-reference) and L1052 (the canonical 4-step preamble).

## 4. AC1b — "regression always exits BEFORE monotonicity"

### 4.1 Three byte-exact occurrences in SKILL.md

The required property "regression always exits BEFORE monotonicity"
is stated three times in the M5 protocol:

- **SKILL.md L1018** (monotonicity guard bullet, gating clause): "The
  monotonicity check is only consulted when `|F_n| > 0` AND only
  after the regression check has passed for this cycle transition."
- **SKILL.md L1021** (wrapper precedence rule): "Regression detection
  ALWAYS runs BEFORE the monotonicity check on every cycle transition
  `n → n+1`. When both conditions would trigger in the same cycle,
  the regression halt-message is emitted and the monotonicity check
  is NOT consulted on the regressed item."
- **SKILL.md L1059** (strict ordering invariant inside the 4-step
  block): "Strict ordering invariant: regression ALWAYS exits BEFORE
  monotonicity; monotonicity ALWAYS exits BEFORE hard-cap; hard-cap
  ALWAYS exits BEFORE proceed. Producers MUST NOT reorder or skip
  steps; consumers (fixture asserts) MUST verify ordering by emission
  ordering in the execution log."

### 4.2 Sub-agent AC1b quote (verbatim from sub-agent report)

> **AC1b — "regression always exits BEFORE monotonicity":**
>
> - SKILL.md:1021: "Regression detection ALWAYS runs BEFORE the monotonicity check on every cycle transition `n → n+1`. When both conditions would trigger in the same cycle, the regression halt-message is emitted and the monotonicity check is NOT consulted on the regressed item."
> - SKILL.md:1059: "Strict ordering invariant: regression ALWAYS exits BEFORE monotonicity; monotonicity ALWAYS exits BEFORE hard-cap; hard-cap ALWAYS exits BEFORE proceed."
> - **Conclusion: PASS** — both the wrapper-level precedence rule (L1021) and the strict ordering invariant (L1059) explicitly state regression exits before monotonicity, with no ambiguity.

## 5. AC2 — F-set identity (dedup-key) explicitly stated

### 5.1 Verbatim SKILL.md L1042-1048 (sub-agent quote)

> - **L1042:** "**F-set definition (item identity = dedup-key, cardinality post-dedup):**"
> - **L1044:** "`F_n` is the SET (not multiset) of FAIL-verdict items at the end of fix cycle `n`. Set membership is determined by the dedup-key:"
> - **L1045:** "- For ordinary checklist items: dedup-key = item ID (e.g., `3.2`)."
> - **L1046:** "- For synthetic-dnsp findings (PR-03): dedup-key = `(assigned_files_range, escalation_ladder_exhaust_point)`."
> - **L1048:** "`|F_n|` is the cardinality of `F_n` AFTER dedup-key deduplication — two failures sharing a dedup-key collapse to one element BEFORE the monotonicity comparison is computed. The regression check uses the same dedup-key identity, so a synthetic-dnsp finding with an identical dedup-key re-emitted on cycle `n+1` is NOT a regression (the prior verdict was FAIL, not PASS); it is the INV-012 cross-cycle dedup case."

### 5.2 Sub-agent AC2 conclusion (verbatim)

> **Conclusion: PASS** — F-set identity is explicitly defined as
> dedup-key for BOTH ordinary checklist items (item ID) AND
> synthetic-dnsp findings (assigned_files_range,
> escalation_ladder_exhaust_point), with cardinality computed
> post-dedup.

## 6. AC3 — rf-team-lead.md:417 hard-cap fallback reference

### 6.1 SKILL.md references the rf-team-lead.md:417 hard cap twice

The sub-agent located two byte-exact SKILL.md references to the
fallback hard cap:

- **SKILL.md L1016** (wrapper preamble): "the existing 3-cycle hard
  cap at `rf-team-lead.md:417` is preserved as the fourth-precedence
  backstop"
- **SKILL.md L1056** (Step 3 of the 4-step rule, the fallback step
  itself): "**Hard-cap check.** If the per-gate cycle counter has
  reached the gate-specific cap (research-gate=3, synthesis-gate=2,
  report-validation=3, task-integrity=2, qualitative=3 — see the
  rf-task-builder.md per-gate cap table, with the global 3-cycle
  backstop at `rf-team-lead.md:417`), HALT per the gate's existing
  escalation path (HALT-and-escalate or Open Questions)."

### 6.2 rf-team-lead.md:417 itself

```
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md
- **Fix Cycles**: If a phase pipeline returns issues, invoke another pipeline with a FIX request (max 3 cycles per phase). If max cycles exhausted, HALT and ask user — do NOT proceed with unresolved findings.
```

### 6.3 Sub-agent AC3 conclusion (verbatim)

> **Conclusion: PASS** — Step 3 (L1056) explicitly references
> `rf-team-lead.md:417` as the global 3-cycle backstop, and
> rf-team-lead.md:417 still contains the 3-cycle hard cap intact.

## 7. AC4 — Sub-agent confirms 4-step ordering verbatim (step-by-step quotes)

The sub-agent quoted all four steps and the strict ordering invariant
byte-for-byte from SKILL.md:

### 7.1 Step 1 — Regression check (SKILL.md L1054)

> "**Regression check.** If any item with verdict PASS at end-of-cycle-`n` has verdict FAIL at end-of-cycle-`n+1` (by dedup-key identity), HALT and emit the byte-exact regression halt-message. Do NOT consult subsequent steps."

### 7.2 Step 2 — Monotonicity check (SKILL.md L1055)

> "**Monotonicity check.** If `|F_n| > 0` AND `|F_{n+1}| >= |F_n|` (cardinality after dedup), HALT and emit the byte-exact monotonicity halt-message `[HALT-MONOTONICITY] |F|=<n>` (with `<n>` = `|F_{n+1}|`). Do NOT consult subsequent steps."

### 7.3 Step 3 — Hard-cap check (SKILL.md L1056)

> "**Hard-cap check.** If the per-gate cycle counter has reached the gate-specific cap (research-gate=3, synthesis-gate=2, report-validation=3, task-integrity=2, qualitative=3 — see the rf-task-builder.md per-gate cap table, with the global 3-cycle backstop at `rf-team-lead.md:417`), HALT per the gate's existing escalation path (HALT-and-escalate or Open Questions)."

### 7.4 Step 4 — Proceed (SKILL.md L1057)

> "**Proceed.** Re-spawn the fix cycle for cycle `n+1`."

### 7.5 Strict ordering invariant (SKILL.md L1059)

> "Strict ordering invariant: regression ALWAYS exits BEFORE monotonicity; monotonicity ALWAYS exits BEFORE hard-cap; hard-cap ALWAYS exits BEFORE proceed. Producers MUST NOT reorder or skip steps; consumers (fixture asserts) MUST verify ordering by emission ordering in the execution log."

### 7.6 Sub-agent AC4 conclusion (verbatim)

> **Conclusion: PASS** — Steps 1 & 2 each contain the required "Do
> NOT consult subsequent steps." sentinel; Step 3 references
> rf-team-lead.md:417 and the rf-task-builder.md per-gate cap table;
> Step 4 is the proceed branch; the L1059 invariant matches the
> required form byte-for-byte.

## 8. INV-012 composition (cross-reference for downstream T05.07)

### 8.1 SKILL.md L1025 (sub-agent quote, verbatim)

> "**Composition with PR-03 DNSP synthetic findings (INV-012 acceptance criterion).** Synthetic findings emitted by the DNSP protocol (PR-03) COUNT as failures for the `|F_n|` monotonicity comparison — they are real, citable evidence items. BUT a synthetic finding with the same `(assigned_files_range, escalation_ladder_exhaust_point)` dedup key appearing across consecutive cycles is a DEDUP case, NOT a regression — the same partition failed the same way twice; the regression-detection logic must compare by dedup key, not by raw finding count, when synthetic-dnsp items are involved. Two synthetic findings with identical dedup keys collapse into one with a 'found N times' note (cf. PR-03 dedup behavior)."

### 8.2 Sub-agent INV-012 conclusion (verbatim)

> **Conclusion: PASS** — L1025 explicitly states synthetic-dnsp
> findings COUNT for `|F_n|` AND that identical dedup keys across
> consecutive cycles are DEDUP (not regression), satisfying the
> INV-012 composition requirement.

INV-012 composition is therefore wired textually as required by the
T05.05 deliverable description. T05.07 (D-0059) will wire the runtime
composition (cross-cycle dedup-key tracking) and run the canonical
cross-cycle dedup fixture (TEST-022 / D-0065).

## 9. Preservation invariants (T05.01 + T05.02 + T05.03 + T05.04 baselines)

T05.05 makes ZERO edits to any source file. The five baselines from
predecessor M5 tasks remain unchanged.

### 9.1 SKILL.md FR-CONV.5 wrapper (L1014-1027) byte-identical

```
$ sed -n '1014,1027p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5  -
```

Hash matches T05.02 / D-0055 §4 baseline, T05.03 / D-0056 §4 baseline,
and T05.04 / D-0057 §4.2 baseline (`1ca8e16e…`).

### 9.2 SKILL.md API-004 contract block (L1029-1059) byte-identical

```
$ sed -n '1029,1059p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099  -
```

Hash matches T05.02 / D-0055 §2.4 baseline, T05.03 / D-0056 §4.1
baseline, and T05.04 / D-0057 §4.1 baseline (`14c40575…`). The M5
contract freeze (which encompasses the F-set definition and the 4-step
ordering rule that T05.05 ratifies) holds end-to-end.

### 9.3 rf-team-lead.md:417 byte-identical (3-cycle hard cap)

```
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
```

Hash matches the T05.01 / D-0054 §2.5 baseline, T05.02 / D-0055 §2.5
baseline, T05.03 / D-0056 §4.2 baseline, and T05.04 / D-0057 §4.3
baseline (`51725c0f…`). T05.08 (D-0060) will reverify at end-of-phase.

### 9.4 Per-gate counter table (rf-task-builder.md:354-364) byte-identical

```
$ sed -n '354,364p' src/superclaude/agents/rf-task-builder.md | sha256sum
121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1  -
```

Hash matches the T05.01 / D-0054 §2.4 baseline, T05.02 / D-0055 §2.6
baseline, T05.03 / D-0056 §4.3 baseline, and T05.04 / D-0057 §4.4
baseline (`121de142…`). Four/five per-gate counters remain independent
and the table referenced by Step 3 of the 4-step ordering rule is
byte-identical.

### 9.5 `src/` ↔ `.claude/` parity

```
$ make verify-sync 2>&1 | tail -1
✅ All components in sync.
```

## 10. Slice hashes (for downstream task verification)

| Slice | sha256 |
|---|---|
| `SKILL.md` L1014-1027 (FR-CONV.5 wrapper — T05.01 baseline preserved) | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` |
| `SKILL.md` L1029-1059 (API-004 contract block + F-set + 4-step rule — T05.02 baseline preserved) | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` |
| `rf-team-lead.md:417` (3-cycle hard cap — untouched) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `rf-task-builder.md` L354-364 (per-gate counter table — preserved) | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` |

---

## 11. Cross-reference to downstream M5 tasks

| Downstream task | Inherits from this task |
|---|---|
| T05.06 (CP-P05-T01-T05 mid-phase checkpoint) | Ratification PASS from T05.05 is one of the three Verification bullets ("4-step ordering rule documented (D-0058 evidence)" and "F-set identity = dedup-key (D-0058 evidence)"). |
| T05.07 (D-0059, INV-012 cross-cycle dedup composition) | Operationalises the dedup-key identity ratified here (§5) and the INV-012 composition rule ratified in §8 for synthetic-dnsp finding bookkeeping; the cross-cycle dedup fixture (TEST-022) asserts the L1025 rule end-to-end. |
| T05.13 (D-0064, TEST-015 + TEST-016 pytest fixtures) | TEST-015 (`|F|=5,5,5`) asserts Step 2 of the 4-step rule emits `[HALT-MONOTONICITY] |F|=5` and Step 4 is never reached; TEST-016 (PASS@1/FAIL@2) asserts Step 1 fires before Step 2 — both rest on the ratified ordering invariant at L1059. |
| T05.14 (D-0065, TEST-017 slow-shrink + TEST-022 cross-cycle dedup) | TEST-017 (`|F|=5,4`) demonstrates Step 2 PROCEED on legitimate shrink (X-003 REJECTED); TEST-022 demonstrates same-dedup-key cross-cycle persistence is NOT regression per the F-set identity rule (§5) and INV-012 composition (§8). |

---

## 12. Verdict

**T05.05 PASS — all 4 AC met.**

- **AC1:** 4-step ordered string regex match in SKILL.md (L1021 + L1052) ✅
  AND sub-agent confirms "regression always exits BEFORE monotonicity"
  (L1018, L1021, L1059) ✅ (§3 + §4).
- **AC2:** F-set identity (dedup-key) explicitly stated in SKILL.md
  L1042-1048 for both ordinary checklist items (item ID) and synthetic-
  dnsp findings ((assigned_files_range, escalation_ladder_exhaust_point))
  ✅ (§5).
- **AC3:** rf-team-lead.md:417 hard-cap referenced as fallback in
  SKILL.md L1016 + L1056; rf-team-lead.md:417 itself byte-identical
  (sha256 `51725c0f…`) ✅ (§6).
- **AC4:** Sub-agent quality-engineer report confirms 4-step ordering
  verbatim — all four steps quoted byte-for-byte from SKILL.md L1054,
  L1055, L1056, L1057 plus the L1059 strict ordering invariant ✅ (§7).

**Sub-agent overall verdict (verbatim from report):** "**Overall:
PASS** — All four ACs are satisfied with byte-exact verbatim matches.
The F-set definition (L1042-1048), 4-step ordering rule (L1050-1059),
INV-012 composition (L1025), and hard-cap fallback reference (L1016,
L1056 → rf-team-lead.md:417 and rf-task-builder.md:354-364) together
form a complete, internally consistent ratification of R-094 + R-095.
Regression-before-monotonicity is stated three times (L1018 wrapper,
L1021 precedence rule, L1059 strict-ordering invariant); both halt-
message wire strings (API-004) are referenced verbatim in Steps 1 and
2; the per-gate caps in Step 3 match rf-task-builder.md:356-364
exactly; and the global 3-cycle backstop at rf-team-lead.md:417 is
preserved."

**Preservation invariants:** SKILL.md L1014-1027 hash unchanged
(`1ca8e16e…`); SKILL.md L1029-1059 hash unchanged (`14c40575…`);
`rf-team-lead.md:417` hash unchanged (`51725c0f…`); per-gate counter
table hash unchanged (`121de142…`); no new retry loops or stages
introduced; `make verify-sync` PASS.

**Unblocks:** T05.06 (mid-phase checkpoint), T05.07 (D-0059, INV-012
cross-cycle dedup composition).
