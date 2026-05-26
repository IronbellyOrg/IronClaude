# D-0057 — T05.04 Spec: Regression Halt-Message Emitter

**Task:** T05.04 (Phase 5 — M5 Retry Monotonicity + Regression Halts)
**Roadmap item:** R-093 (Regression halt-message emitter)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [█████████-] 90%
**Verification method:** Direct test execution (synthetic execution-log fixtures)

---

## 1. Scope

T05.04 lands the regression halt-message **emitter** — the producer
side of the byte-exact wire string

> `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`

that the API-004-M5 wire ABI (T05.02 / D-0055) froze at SKILL.md
L1038 (contract row 2). The emitter:

1. Substitutes `X.Y` ← the regressed item identifier (by dedup-key
   identity — for ordinary checklist items this is the item ID;
   for synthetic-dnsp findings it is `(assigned_files_range,
   escalation_ladder_exhaust_point)` per SKILL.md L1045-L1046).
2. Substitutes `N` ← the prior-PASS cycle number (the cycle at the
   end of which the regressed item carried verdict PASS — i.e.,
   the `n` in the transition `n → n+1`).
3. Fires on **per-item PASS→FAIL flip** across the cycle
   transition: any item in the cycle-`n` PASS set that is in the
   cycle-`n+1` FAIL set triggers the halt.
4. Is the **first** step of the 4-step ordering rule (SKILL.md
   L1052-L1057). When it HALTs, the wrapper does NOT consult
   step 2 (monotonicity), step 3 (hard-cap), or step 4 (proceed)
   on that cycle transition. This is the precedence guarantee
   that mirrors the gate-B short-circuit demonstrated from the
   monotonicity-emitter angle in D-0056 §3.

T05.04 is **additive** with respect to the SKILL.md / agents
protocol landed by T05.01 + T05.02. No edits to the protocol are
needed; the emitter behaviour is fully captured by:

- The wrapper paragraph at `SKILL.md:1019` (gating + wire string).
- The API-004 contract row at `SKILL.md:1038` (wire string + `X.Y`
  / `N` substitution rules).
- The 4-step ordering rule step 1 at `SKILL.md:1054` ("HALT and
  emit the byte-exact regression halt-message. Do NOT consult
  subsequent steps.").
- The wrapper paragraphs at `rf-task-builder.md:368` and
  `rf-qa.md:341` (per-gate wrapper restatement of the same
  byte-exact string).

T05.04 demonstrates the emitter via three synthetic execution-log
fixtures (the wire ABI's downstream consumers — fixture asserts,
execution-log scanners — match these as byte-for-byte producers).

T05.13 will later commit the canonical pytest fixture
(`tests/audit/test_regression_halt_pass1_fail2.py`) that re-
asserts the same byte-exact behaviour at merge-gate. The three
fixtures in this deliverable are the **specification by example**
that T05.13 will codify, mirroring the D-0056 / T05.03 pattern.

## 2. Emitter wiring (no new code; protocol-level emission)

The fix-cycle loops in scope (SKILL.md §A.10, §A.10.5; rf-task-
builder per-gate cycles at `rf-task-builder.md:354-360`; rf-qa
3-fix-cycle at `rf-qa.md:308-345`) all share the SAME emitter
contract because the FR-CONV.5 halt-guards wrapper layered ON TOP
of each of them (T05.01) forwards to the same wire string. The
"emitter" is therefore the single literal regression halt-message
that every wrapper emission site copies verbatim into the
execution log.

| Emission site | File | Anchor |
|---|---|---|
| Wrapper paragraph (protocol-level) | `src/superclaude/skills/task-builder/SKILL.md` | L1019 |
| API-004 contract table row | `src/superclaude/skills/task-builder/SKILL.md` | L1038 |
| 4-step ordering rule step 1 | `src/superclaude/skills/task-builder/SKILL.md` | L1054 |
| rf-task-builder per-gate wrapper | `src/superclaude/agents/rf-task-builder.md` | L368 |
| rf-qa fix-cycle regression bullet | `src/superclaude/agents/rf-qa.md` | L341 |

All five sites carry the byte-identical 113-byte template
`Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`
The em-dash `—` between `X.Y` and `previously` is U+2014 (bytes
`e2 80 94`) — verified at T05.02 / D-0055 §3 row 2 by `od -c`;
re-verified in this deliverable's §3.1 fixture xxd.

## 3. Detection semantics (per-item PASS→FAIL flip)

The detector is **per-item** and **per-transition**:

- At end-of-cycle-`n`, record `PASS_n` = the set of items with
  verdict PASS (dedup-key identity).
- At end-of-cycle-`n+1`, compute `FAIL_{n+1}` = the set of items
  with verdict FAIL (dedup-key identity).
- `Regressed_{n→n+1}` = `PASS_n ∩ FAIL_{n+1}`. If this set is
  non-empty, HALT and emit the byte-exact regression message
  with `X.Y` ← any element of `Regressed_{n→n+1}` (the wire-ABI
  requires emitting at least one regressed item; deterministic
  tie-breaking by lexicographic dedup-key order is the
  recommended convention but is NOT a wire-string requirement —
  the M5 contract pins the template, not the tie-break).

The detector explicitly does NOT fire on:

- Legitimate refinement of still-FAILing items (PASS_n ∩ FAIL_n
  intersection is empty by construction; items that were FAIL and
  remain FAIL contribute to `|F_{n+1}|` for monotonicity but not
  to the regression set).
- Legitimate FAIL→PASS transitions (items that became PASS contribute
  to `PASS_{n+1}` and are exactly the convergence signal the loop
  is trying to surface).
- INV-012 cross-cycle dedup of synthetic-dnsp findings (the prior-
  cycle verdict was FAIL, not PASS — the same dedup-key cannot
  flip PASS→FAIL because it was never in `PASS_n`). T05.07 wires
  this in execution.

## 4. Precedence semantics (step 1 of the 4-step ordering rule)

The 4-step ordering rule at SKILL.md L1052-L1057 mandates strict
ordering: regression → monotonicity → hard-cap → proceed. The
"EXIT on the first match" clause at L1052 plus the "Do NOT consult
subsequent steps" clause at L1054 make the regression emitter the
**absolute first** halt-condition consulted on every cycle
transition. Therefore:

- When the regression emitter fires, the wrapper's execution log
  for that transition shows **no `step=monotonicity` line after
  the HALT** (the wrapper short-circuits before re-entering the
  step iterator).
- When the regression emitter does NOT fire (regression-set is
  empty), the wrapper proceeds to step 2 (monotonicity) and the
  4-step ordering rule continues evaluating downstream
  conditions.

This precedence is **independent** of the cardinality trajectory.
The fixtures in §5 below demonstrate this with two contrasting
shapes:

- §5.1 (`fixture-pass1-fail2-shrinking.log`): regression fires
  even when `|F_2|=4 < |F_1|=5` (i.e., the monotonicity step would
  PROCEED). Proves regression is not dependent on `|F|` non-shrink.
- §5.2 (`fixture-pass1-fail2-non-shrinking.log`): regression fires
  AHEAD of monotonicity when `|F_2|=5 >= |F_1|=5` (i.e., the
  monotonicity step would HALT if consulted). Proves precedence.

## 5. Demonstration fixtures

Three synthetic execution-log fixtures live in this deliverable
directory:

1. `fixture-pass1-fail2-shrinking.log` — TEST-016 canonical PASS@1/
   FAIL@2 flip with `|F_2|=4 < |F_1|=5` (strict shrink — monotonicity
   would PROCEED). The regression emitter fires at the cycle-1 →
   cycle-2 transition with byte-exact payload; cycle 3 is NEVER
   attempted. Demonstrates AC1 (byte-exact message) + AC2 (ordering)
   independent of cardinality trajectory.
2. `fixture-pass1-fail2-non-shrinking.log` — same PASS@1/FAIL@2 flip
   on Item 3.2 but with `|F_2|=5 >= |F_1|=5` (cardinality non-shrink
   — monotonicity would HALT if consulted). The regression emitter
   fires; the `step=monotonicity` log line is ABSENT for the cycle-
   2 → cycle-3 transition. Demonstrates AC3 (monotonicity NOT
   consulted on regressed item).
3. `fixture-no-regression-loop-continues.log` — no item flips PASS→
   FAIL across the cycle transition (legitimate refinement only).
   The regression emitter does NOT fire; the wrapper proceeds to
   step 2 (monotonicity), which also PROCEEDs because `|F_2|=4 <
   |F_1|=5`; the loop continues into cycle 3. Demonstrates the
   negative case — proves the emitter is NOT a constant-emit and
   does not fire on legitimate refinement.

The fixture format mirrors the execution-log shape used in D-0056
(monotonicity-emitter fixtures) and the shape that the producer
wrappers will emit at runtime: one `CYCLE` line per cycle boundary
and one `TRANSITION` line per 4-step ordering step, plus a final
`HALT` line carrying the byte-exact halt-message wire string when
a halt fires.

## 6. Acceptance criteria coverage

| AC | Statement | Where verified |
|----|-----------|----------------|
| AC1 | `Regression detected on Item 3.2` literal appears in halt log on PASS@1/FAIL@2 fixture | `fixture-pass1-fail2-shrinking.log` line 22 + `fixture-pass1-fail2-non-shrinking.log` line 25 (both byte-exact) |
| AC2 | Ordering assertion confirms regression check runs first | Both halt fixtures show `TRANSITION 2->3 step=regression verdict=HALT` as the FIRST step line at the cycle-2 → cycle-3 boundary; no preceding `step=monotonicity` line |
| AC3 | Monotonicity check NOT consulted on the regressed item | `fixture-pass1-fail2-non-shrinking.log` — `step=monotonicity` is absent at the cycle-2 → cycle-3 transition; `grep -c HALT-MONOTONICITY` returns 0 |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0057/evidence.md` | `evidence.md` (sibling file) |

## 7. Preservation invariants (carried from T05.01 + T05.02 + T05.03)

T05.04 makes ZERO edits to any source file. The following hashes
recorded in D-0054 / D-0055 / D-0056 remain unchanged:

| Slice | sha256 |
|---|---|
| `SKILL.md` L1029-1059 (API-004 contract block — T05.02 baseline) | `14c40575…` |
| `SKILL.md` L1014-1027 (FR-CONV.5 wrapper — T05.01 baseline) | `1ca8e16e…` |
| `rf-team-lead.md:417` (3-cycle hard cap — preserved end-to-end) | `51725c0f…` |
| `rf-task-builder.md` L354-364 (per-gate counter table — preserved) | `121de142…` |

The four independent retry counters (RESEARCH_NEEDED, MALFORMED,
research-gate gap-fill, per-gate fix cycles) and the global
3-cycle hard cap at `rf-team-lead.md:417` are PRESERVED end-to-
end.

## 8. Dependencies and cross-references

- **Dependencies:** T05.02 (D-0055) — API-004 wire string contract,
  contract row 2 (regression halt) with `X.Y` and `N` placeholders
  + U+2014 em-dash freeze.
- **Sibling task:** T05.03 (D-0056) — monotonicity emitter; D-0056
  §3 already demonstrated this transition from the monotonicity-
  emitter angle (showing monotonicity NOT consulted); this
  deliverable demonstrates it from the regression-emitter angle
  (showing regression fires byte-exact). The two deliverables form
  a complementary pair on the precedence rule.
- **Unblocks:** T05.05 (D-0058, F-set + ordering ratification);
  T05.13 (D-0064, official pytest fixture commit TEST-016 using
  the same execution-log shape).
- **Mirrors:** D-0056 / T05.03 pattern (synthetic execution-log
  fixtures shipped with the protocol-edit deliverable; pytest
  commit deferred to T05.13).

## 9. Rollback

Per roadmap R-093 rollback note: disable the regression guard
individually by removing the bullet at `SKILL.md:1019` and the
corresponding L1054 step 1 of the 4-step ordering rule. The
monotonicity guard (T05.03 / D-0056) is independently disable-
able and is unaffected by a regression-guard rollback. Per-gate
caps continue to govern fix-cycle escalation via the preserved
`rf-team-lead.md:417` hard cap and the per-gate counter table at
`rf-task-builder.md:354-360`.
