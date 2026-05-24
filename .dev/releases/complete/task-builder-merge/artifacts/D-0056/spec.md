# D-0056 — T05.03 Spec: Monotonicity Halt-Message Emitter

**Task:** T05.03 (Phase 5 — M5 Retry Monotonicity + Regression Halts)
**Roadmap item:** R-092 (Monotonicity halt-message emitter)
**Date:** 2026-05-17
**Status:** PASS
**Tier:** STANDARD
**Confidence:** [█████████-] 90%
**Verification method:** Direct test execution (synthetic execution-log fixtures)

---

## 1. Scope

T05.03 lands the monotonicity halt-message **emitter** — the producer
side of the byte-exact wire string `[HALT-MONOTONICITY] |F|=<n>` that
the API-004-M5 wire ABI (T05.02 / D-0055) froze. The emitter:

1. Substitutes the integer cardinality `|F_{n+1}|` (post dedup-key
   deduplication) into the `<n>` placeholder.
2. Fires only on **strict non-shrink** (`|F_{n+1}| >= |F_n|`).
3. Is **gated** on two preconditions:
   - **Gate A — non-empty F_n:** the check is consulted only when
     `|F_n| > 0`. A first cycle that finishes with zero failures
     skips the monotonicity check entirely (no F_{n+1} exists to
     compare against, and even if it did the wrapper exits via the
     "Proceed" step before any halt could be emitted).
   - **Gate B — regression check passed:** per the 4-step ordering
     rule at `SKILL.md:1052-1057`, the regression check runs FIRST.
     When a regression flip is detected on the same cycle transition,
     the regression halt is emitted and the monotonicity check is
     NOT consulted on that transition (precedence preserved end-to-
     end; no monotonicity emission in the same cycle as a regression
     emission).

T05.03 is **additive** with respect to the SKILL.md / agents protocol
landed by T05.01 + T05.02. No edits to the protocol are needed; the
emitter behaviour is fully captured by:

- The wrapper paragraph at `SKILL.md:1018` (gating + wire string).
- The API-004 contract row at `SKILL.md:1037` (wire string + `<n>` ←
  `|F_{n+1}|` substitution rule).
- The 4-step ordering rule step 2 at `SKILL.md:1055` (gate A: `|F_n|
  > 0`; gate B: implicit because step 1 already exited on regression).

T05.03 demonstrates the emitter via three synthetic execution-log
fixtures (the wire ABI's downstream consumers — fixture asserts,
execution-log scanners — match these as byte-for-byte producers).

T05.13 will later commit the canonical pytest fixture
(`tests/audit/test_monotonicity_halt_F_5_5_5.py`) that re-asserts
the same byte-exact behaviour at merge-gate. The three fixtures in
this deliverable are the **specification by example** that T05.13
will codify.

## 2. Emitter wiring (no new code; protocol-level emission)

The fix-cycle loops in scope (SKILL.md §A.10, §A.10.5; rf-task-builder
per-gate cycles at `rf-task-builder.md:354-360`; rf-qa 3-fix-cycle at
`rf-qa.md:308-345`) all share the SAME emitter contract because the
FR-CONV.5 halt-guards wrapper layered ON TOP of each of them (T05.01)
forwards to the same wire string. The "emitter" is therefore the
single literal `[HALT-MONOTONICITY] |F|=<n>` that every wrapper
emission site copies verbatim into the execution log.

| Emission site | File | Anchor |
|---|---|---|
| Wrapper paragraph (protocol-level) | `src/superclaude/skills/task-builder/SKILL.md` | L1018 |
| API-004 contract table row | `src/superclaude/skills/task-builder/SKILL.md` | L1037 |
| 4-step ordering rule step 2 | `src/superclaude/skills/task-builder/SKILL.md` | L1055 |
| rf-task-builder per-gate wrapper | `src/superclaude/agents/rf-task-builder.md` | L368 |
| rf-qa fix-cycle monotonicity bullet | `src/superclaude/agents/rf-qa.md` | L342 |

All five sites carry the byte-identical 28-byte template `[HALT-
MONOTONICITY] |F|=<n>` (single `0x20` space between `]` and `|F|`,
ASCII pipes, no smart-quotes — verified at T05.02 / D-0055 §3 row
1 by `od -c`).

## 3. Gating semantics (the two halt-suppression conditions)

### Gate A — `|F_n|=0` skip

If `|F_n|=0` (the cycle-`n` failure set is empty after dedup), the
4-step ordering rule's step 2 short-circuits via the `|F_n| > 0`
precondition. Step 1 (regression) cannot fire either — no item
flipped from PASS to FAIL because no item was FAILing at cycle `n`
to begin with — so the wrapper falls through to step 3 (hard-cap)
and step 4 (proceed). In practice, `|F_n|=0` means the cycle
already PASSed; the fix-cycle loop terminates with verdict PASS
and never spawns cycle `n+1`. The emitter is therefore **never
consulted** on a passing first cycle.

This is the SKILL.md L1027 "Single-cycle case" invariant:

> If the first cycle PASSes, no second cycle runs; both guards are
> no-ops by construction.

### Gate B — regression precedence skip

If the regression check (step 1) fires on cycle transition `n →
n+1`, it HALTs and emits the byte-exact regression halt-message
`Regression detected on Item X.Y — previously PASS at cycle N,
now FAIL. Halt overrides monotonicity check.` The "Do NOT consult
subsequent steps" sentence at `SKILL.md:1054` is the precedence
guarantee — the monotonicity check is NOT consulted on the
regressed cycle transition, even if the cardinality condition
`|F_{n+1}| >= |F_n|` would otherwise have fired.

This is the SKILL.md L1021 "Precedence rule" invariant:

> When both conditions would trigger in the same cycle, the
> regression halt-message is emitted and the monotonicity check
> is NOT consulted on the regressed item.

## 4. Demonstration fixtures

Three synthetic execution-log fixtures live in this deliverable
directory:

1. `fixture-F-5-5-5-halt-cycle-2.log` — TEST-015 canonical
   `|F|=5,5,5` flow. Cycle 1 ends with 5 failures, cycle 2 ends
   with 5 failures (no shrink); the monotonicity emitter fires
   at the cycle-1 → cycle-2 transition with `[HALT-MONOTONICITY]
   |F|=5`; cycle 3 is NEVER attempted. Demonstrates AC1 + AC2.
2. `fixture-F-0-skip.log` — cycle 1 PASSes with `|F_1|=0`; the
   monotonicity check is skipped per gate A; no halt-message is
   emitted; the loop terminates with verdict PASS. Demonstrates
   AC3.
3. `fixture-regression-precedes-monotonicity.log` — cycle 1 ends
   with 5 failures including Item 3.2 PASSing; cycle 2 ends with
   5 failures including Item 3.2 FAILing (regression flip). The
   regression emitter fires; the monotonicity emitter does NOT
   fire even though `|F_2|=5 >= |F_1|=5` would otherwise satisfy
   the cardinality condition. Demonstrates AC4.

The fixture format mirrors the execution-log shape that the
producer wrappers will emit at runtime: one `EXEC` line per cycle
transition documenting the per-cycle F-set cardinality plus a
final `HALT` line carrying the byte-exact halt-message wire string
(or a terminating `PROCEED`/`PASS` line when no halt fires).

## 5. Acceptance criteria coverage

| AC | Statement | Where verified |
|----|-----------|----------------|
| AC1 | `[HALT-MONOTONICITY] |F|=5` literal appears in halt log on `|F|=5,5,5` fixture | `fixture-F-5-5-5-halt-cycle-2.log` line 8 |
| AC2 | Cycle 3 NOT attempted | Same fixture — last line is the HALT, no `CYCLE 3` line |
| AC3 | Monotonicity check skipped when `|F_n|=0` | `fixture-F-0-skip.log` — no `HALT-MONOTONICITY` token anywhere |
| AC4 | Monotonicity emission gated on prior regression-check passing (regression flip → monotonicity NOT emitted on same cycle) | `fixture-regression-precedes-monotonicity.log` — `Regression detected on Item 3.2` emitted; `HALT-MONOTONICITY` absent |
| AC5 | Evidence at `TASKLIST_ROOT/artifacts/D-0056/evidence.md` | `evidence.md` (sibling file) |

## 6. Preservation invariants (carried from T05.01 + T05.02)

T05.03 makes ZERO edits to any source file. The following hashes
recorded in D-0054 / D-0055 remain unchanged:

| Slice | sha256 |
|---|---|
| `SKILL.md` L1029-1059 (API-004 contract block, T05.02) | `14c40575…` |
| `SKILL.md` L1014-1027 (FR-CONV.5 wrapper, T05.01) | (carried) |
| `rf-team-lead.md:417` (3-cycle hard cap) | `51725c0f…` |
| `rf-task-builder.md` L354-364 (per-gate counter table) | `121de142…` |

The four independent retry counters (RESEARCH_NEEDED, MALFORMED,
research-gate gap-fill, per-gate fix cycles) and the global 3-cycle
hard cap at `rf-team-lead.md:417` are PRESERVED end-to-end.

## 7. Dependencies and cross-references

- **Dependencies:** T05.02 (D-0055) — API-004 wire string contract.
- **Unblocks:** T05.04 (D-0057, regression emitter, mirrors this
  pattern); T05.05 (D-0058, F-set + ordering ratification); T05.13
  (D-0064, official pytest fixture commit using the same execution-
  log shape).
- **Mirrors:** D-0045 / T04.05 pattern (synthetic markdown fixture
  shipped with the protocol-edit deliverable; pytest commit deferred
  to a later task in the phase).

## 8. Rollback

Per roadmap R-092 rollback note: disable the monotonicity guard
individually by removing the bullet at `SKILL.md:1018` and the
corresponding L1055 step 2 of the 4-step ordering rule; per-gate
caps continue to govern fix-cycle escalation via the preserved
`rf-team-lead.md:417` hard cap and the per-gate counter table at
`rf-task-builder.md:354-360`. The regression guard (T05.04 / D-0057)
is independently disable-able and is unaffected by a monotonicity-
guard rollback.
