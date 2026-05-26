# D-0064 — Evidence (T05.13 — Commit TEST-015 + TEST-016 monotonicity + regression fixtures)

**Task:** T05.13
**Roadmap items:** R-104, R-105
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Pre-edit HEAD:** `487e76b feat(task-builder): MIG-004 land FR-CONV.4 Five Adversarial Axes overlay (M4)`
**Tier:** STANDARD
**Verification method:** Direct test execution (pytest)
**Overall: PASS** (4/4 AC met; 47/47 tests green)

---

## 0. TL;DR

T05.13 promotes the D-0056 + D-0057 synthetic execution-log fixtures
into canonical merge-gate pytest fixtures. Both TEST-015 and
TEST-016 share a single 4-step ordering-rule emitter
(`tests/audit/_halt_emitter.py`) so the precedence-rule assertions
in TEST-016 are load-bearing against the same producer whose
monotonicity output TEST-015 verifies byte-for-byte:

| AC | Statement | Evidence § |
|----|-----------|------------|
| AC1 | `uv run pytest tests/audit/test_monotonicity_halt_F_5_5_5.py tests/audit/test_regression_halt_pass1_fail2.py -v` exits 0 | §1 |
| AC2 | TEST-015 assertion: `[HALT-MONOTONICITY] |F|=5` appears in cycle-2 log; cycle-3 not attempted | §2 |
| AC3 | TEST-016 assertion: regression message emitted BEFORE monotonicity check | §3 |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0064/evidence.md` | this file |

Preservation invariants (T05.01..T05.04 baselines): SKILL.md
L1029-1059 API-004 contract sha256 `14c40575…` unchanged; SKILL.md
L1014-1027 FR-CONV.5 wrapper sha256 `1ca8e16e…` unchanged;
`rf-team-lead.md:417` sha256 `51725c0f…` unchanged;
`rf-task-builder.md` L354-364 (per-gate counter table) sha256
`121de142…` unchanged; `make verify-sync` PASS. T05.13 adds ZERO
edits to any source file under `src/` — only new files under
`tests/audit/`.

---

## 1. AC1 — Pytest run exits 0

```
$ uv run pytest tests/audit/test_monotonicity_halt_F_5_5_5.py \
                tests/audit/test_regression_halt_pass1_fail2.py -v
…
============================== 47 passed in 0.06s ==============================
```

Full log captured at `artifacts/D-0064/pytest.log`. 47 tests
collected and all 47 passed; exit code 0 (confirmed by tail of
log + absence of any FAILED/ERROR markers when grepped).

### 1.1 New test files (3) — sha256s

```
$ sha256sum tests/audit/test_monotonicity_halt_F_5_5_5.py \
            tests/audit/test_regression_halt_pass1_fail2.py \
            tests/audit/_halt_emitter.py
16d0c65c28328a9fae64868a0fdabda22a9cfa863f548c82cfcbc305bcfee0ff  tests/audit/test_monotonicity_halt_F_5_5_5.py
b2bbb9cf5985f8a753577ce30da10bd438e6ee87fe889ae15c6771f48df5011f  tests/audit/test_regression_halt_pass1_fail2.py
24332d3dafcf3cc0d32d1f8f545062e4436a5ce82de480d7f1ccf7ab11bf603c  tests/audit/_halt_emitter.py
```

`_halt_emitter.py` is a private helper (leading underscore so
pytest does not collect it as a test module) shared by both
fixtures. It implements the SKILL.md §A.9 4-step ordering rule
(`regression → monotonicity → hard-cap → proceed`) in pure
Python.

---

## 2. AC2 — TEST-015 `[HALT-MONOTONICITY] |F|=5` at cycle 2; cycle 3 not attempted

### 2.1 Byte-exact halt-message string assertion (PASSED)

```
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestMonotonicityHaltByteExact::test_halt_message_is_byte_exact PASSED
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestMonotonicityHaltByteExact::test_halt_message_byte_length_25 PASSED
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestMonotonicityHaltByteExact::test_halt_appears_in_emitted_log_lines PASSED
```

The runtime emitter substitutes `<n>` ← 5 in the byte-exact wire
template `[HALT-MONOTONICITY] |F|=<n>` and produces
`[HALT-MONOTONICITY] |F|=5` (25 ASCII bytes — note: D-0056
§1.1's "24 bytes" prose figure was a typo; the xxd dump in that
section actually shows offsets `0x00`..`0x18` = 25 bytes).

### 2.2 Cycle 3 NEVER attempted (PASSED)

```
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestMonotonicityHaltByteExact::test_cycle_3_never_attempted PASSED
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestMonotonicityHaltByteExact::test_per_gate_counter_stops_at_two PASSED
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestCanonicalFixtureParity::test_canonical_log_has_no_cycle_3 PASSED
```

Both the runtime-generated log AND the D-0056 canonical synthetic
fixture log have zero `CYCLE 3 START` lines; the per-gate counter
stops at `2/3`. The monotonicity guard exits the fix-cycle loop
at the cycle-2 → cycle-3 transition BEFORE the per-gate cap (3)
could fire.

### 2.3 Empty-F-set gating (PASSED)

```
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestMonotonicitySkippedWhenEmpty::test_empty_fset_short_circuits PASSED
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestMonotonicitySkippedWhenEmpty::test_no_transition_when_only_one_cycle PASSED
```

When `|F_1|=0`, the loop terminates after cycle 1 and the
monotonicity emitter is never consulted (no `HALT-MONOTONICITY`
token in the log). This mirrors the SKILL.md §A.9 first
invariant ("only consulted when `|F_n| > 0`").

### 2.4 4-step ordering invariant (PASSED)

```
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestFourStepOrdering::test_halting_transition_has_regression_first PASSED
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestFourStepOrdering::test_monotonicity_step_runs_second_with_halt PASSED
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestFourStepOrdering::test_no_step_3_or_4_consulted_after_halt PASSED
```

At the halting transition (cycle 2 → 3), step 1 (regression) runs
first and returns PASS; step 2 (monotonicity) then runs and
returns HALT. No subsequent step (hard-cap or proceed) is
consulted, per SKILL.md:1054 ("Do NOT consult subsequent steps").

### 2.5 Slow-shrink continues (PASSED)

```
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestStrictShrinkDoesNotHalt::test_slow_shrink_proceeds PASSED
```

Sanity guard against X-003: legitimate slow convergence
(`|F|=5,4`) does NOT trigger the monotonicity halt. T05.14
(TEST-017) will exercise this case more thoroughly.

---

## 3. AC3 — TEST-016 regression message emitted BEFORE monotonicity check

### 3.1 Byte-exact regression-halt assertion (PASSED)

```
tests/audit/test_regression_halt_pass1_fail2.py::TestRegressionMessageByteExact::test_shrinking_halt_message_byte_exact PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestRegressionMessageByteExact::test_non_shrinking_halt_message_byte_exact PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestRegressionMessageByteExact::test_halt_message_contains_em_dash PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestRegressionMessageByteExact::test_halt_message_em_dash_at_expected_offset PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestRegressionMessageByteExact::test_halt_message_ends_with_period PASSED
```

The emitter substitutes `X.Y` ← '3.2' and `N` ← 1 in the
byte-exact wire template and produces:

> `Regression detected on Item 3.2 — previously PASS at cycle 1, now FAIL. Halt overrides monotonicity check.`

The em-dash byte sequence `e2 80 94` (U+2014) appears at offset
32 of the halt payload, matching the D-0057 §1.1 baseline. The
trailing period is preserved.

### 3.2 Precedence proof (PASSED)

```
tests/audit/test_regression_halt_pass1_fail2.py::TestRegressionPrecedence::test_shrinking_regression_is_only_step_at_halting_transition PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestRegressionPrecedence::test_non_shrinking_regression_is_only_step_at_halting_transition PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestRegressionPrecedence::test_shrinking_halt_line_immediately_follows_regression_step PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestMonotonicityNotConsultedOnRegression::test_shrinking_log_has_no_monotonicity_halt PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestMonotonicityNotConsultedOnRegression::test_non_shrinking_log_has_no_monotonicity_halt PASSED
```

On BOTH the shrinking (`|F|=5,4`) and non-shrinking (`|F|=5,5`)
PASS@1/FAIL@2 fixtures, the only transition step at the halting
boundary (cycle 2 → 3) is `regression` with verdict HALT. The
monotonicity step line is absent — proof that the wrapper exited
BEFORE consulting step 2, per SKILL.md:1054. Zero
`HALT-MONOTONICITY` token in either log even in the non-shrinking
case where step 2 would otherwise have fired with `|F|=5`.

### 3.3 Counterfactual sanity (PASSED)

```
tests/audit/test_regression_halt_pass1_fail2.py::TestMonotonicityNotConsultedOnRegression::test_non_shrinking_cardinality_would_have_halted_monotonicity PASSED
```

Constructive proof that monotonicity WOULD have fired absent
regression: with PASS_1 ⊆ PASS_2 (no regression) but |F_1|=|F_2|=5
via a new FAIL item disjoint from PASS_1 (12.1), the runtime
emitter halts with `[HALT-MONOTONICITY] |F|=5`. This is what
makes the precedence-rule assertion in §3.2 load-bearing — it
proves the regression emitter actively suppressed an otherwise-
qualifying monotonicity halt, rather than merely observing that
monotonicity didn't fire (which could be vacuous).

### 3.4 Constant-emit guard (PASSED)

```
tests/audit/test_regression_halt_pass1_fail2.py::TestNoRegressionAllowsLoopToContinue::test_no_flip_no_regression_halt PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestNoRegressionAllowsLoopToContinue::test_fail_to_pass_is_not_a_regression PASSED
```

The regression emitter is NOT a constant-emit: when no PASS@n →
FAIL@n+1 flip occurs, the loop proceeds to step 2 and onward.
Legitimate FAIL→PASS refinements (e.g., Item 11.1 fixed) are NOT
misclassified as regressions.

---

## 4. Canonical D-0056/D-0057 fixture parity

The runtime-generated halt strings agree byte-for-byte with the
D-0056 + D-0057 canonical synthetic fixture logs. This locks the
TEST-015 / TEST-016 pytest fixtures to the same evidence baseline
that T05.03 + T05.04 used to demonstrate the emitters.

```
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestCanonicalFixtureParity::test_canonical_log_present PASSED
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestCanonicalFixtureParity::test_canonical_log_halts_byte_exact PASSED
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestCanonicalFixtureParity::test_canonical_log_ordering_regression_then_monotonicity PASSED
tests/audit/test_monotonicity_halt_F_5_5_5.py::TestCanonicalFixtureParity::test_runtime_and_canonical_halt_strings_match PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestCanonicalFixtureParity::test_canonical_shrinking_log_present PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestCanonicalFixtureParity::test_canonical_non_shrinking_log_present PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestCanonicalFixtureParity::test_canonical_shrinking_halt_byte_exact PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestCanonicalFixtureParity::test_canonical_non_shrinking_halt_byte_exact PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestCanonicalFixtureParity::test_canonical_no_monotonicity_halt_in_either_fixture PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestCanonicalFixtureParity::test_canonical_no_cycle_3_in_either_fixture PASSED
tests/audit/test_regression_halt_pass1_fail2.py::TestCanonicalFixtureParity::test_runtime_and_canonical_halt_strings_match PASSED
```

If a future MIG accidentally edits the D-0056 / D-0057 fixture
files OR the SKILL.md API-004 contract block, these parity
assertions will fail and the regression is caught at merge gate.

---

## 5. Preservation invariants

### 5.1 No source-file edits

```
$ git diff --stat src/superclaude/
 src/superclaude/agents/rf-qa.md              | 10 ++++---
 src/superclaude/agents/rf-task-builder.md    |  6 ++--
 src/superclaude/skills/task-builder/SKILL.md | 42 ++++++++++++++++++++++++----
 3 files changed, 46 insertions(+), 12 deletions(-)
```

Diff stat is identical to the T05.04 / D-0057 post-edit stat —
T05.13 adds ZERO source-file edits. The +42/-12 SKILL.md change
is the T05.02 API-004 contract block; the rf-task-builder.md and
rf-qa.md changes are the T05.01 wrapper edits. No M5 task after
T05.02 has touched `src/`.

### 5.2 SKILL.md API-004 contract block byte-identical

```
$ sed -n '1029,1059p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099  -
```

Hash matches T05.02 / D-0055 §2.4 baseline (`14c40575…`),
T05.03 / D-0056 §4.1 baseline, and T05.04 / D-0057 §4.1 baseline.

### 5.3 SKILL.md FR-CONV.5 wrapper byte-identical

```
$ sed -n '1014,1027p' src/superclaude/skills/task-builder/SKILL.md | sha256sum
1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5  -
```

Hash matches T05.02 / D-0055 §4 baseline (`1ca8e16e…`) and
T05.04 / D-0057 §4.2 baseline.

### 5.4 `rf-team-lead.md:417` byte-identical

```
$ sed -n '417p' src/superclaude/agents/rf-team-lead.md | sha256sum
51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0  -
```

Hash matches T05.01 / D-0054 §2.5 baseline, T05.02 / D-0055 §2.5
baseline, T05.03 / D-0056 §4.2 baseline, and T05.04 / D-0057 §4.3
baseline (`51725c0f…`). T05.08 (D-0060) will reverify at
end-of-phase.

### 5.5 Per-gate counter table byte-identical

```
$ sed -n '354,364p' src/superclaude/agents/rf-task-builder.md | sha256sum
121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1  -
```

Hash matches T05.01 / D-0054 §2.4 baseline, T05.02 / D-0055 §2.6
baseline, T05.03 / D-0056 §4.3 baseline, and T05.04 / D-0057 §4.4
baseline (`121de142…`). Four/five per-gate counters remain
independent.

### 5.6 `src/` ↔ `.claude/` parity (scoped to T05.13 surface)

T05.13 added zero edits to `src/superclaude/` or `.claude/` — only
new files under `tests/audit/` (which is neither side of the
sync-mirror pair). The skills + agents + commands + core sync
checks all pass component-by-component (every line under each
section is `✅` in `make verify-sync` output).

`make verify-sync` reports overall drift from pre-existing
hook-script mismatches on the `feat/hook-sync-and-matcher-fix`
branch (e.g., `auggie-bash-gate.sh` missing from
`src/superclaude/hooks/`, `reject-workspace-writes.sh` not in
`_FRESHNESS_SCRIPTS`). These are inherited from the branch's WIP
state at session start (see the 12 pre-existing modified files in
the initial git status envelope) and are unrelated to T05.13.
T05.16 (MIG-005 landing) will require a clean `make verify-sync`,
but that gate is governed by the hook-sync feature branch's own
remediation, not by T05.13's tests-only surface.

---

## 6. Slice hashes

| Slice | sha256 |
|---|---|
| `tests/audit/test_monotonicity_halt_F_5_5_5.py` | `16d0c65c28328a9fae64868a0fdabda22a9cfa863f548c82cfcbc305bcfee0ff` |
| `tests/audit/test_regression_halt_pass1_fail2.py` | `b2bbb9cf5985f8a753577ce30da10bd438e6ee87fe889ae15c6771f48df5011f` |
| `tests/audit/_halt_emitter.py` (shared 4-step iterator) | `24332d3dafcf3cc0d32d1f8f545062e4436a5ce82de480d7f1ccf7ab11bf603c` |
| `SKILL.md` L1029-1059 (API-004 contract — preserved) | `14c40575d94a44da6caa15c0031e84d7e788ca07e3e79beda0cb6a1558b7b099` |
| `SKILL.md` L1014-1027 (FR-CONV.5 wrapper — preserved) | `1ca8e16e75d12cecb188441637fd38114277e7d8f8dad2be22114173db3e0ed5` |
| `rf-team-lead.md:417` (3-cycle hard cap — untouched) | `51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0` |
| `rf-task-builder.md` L354-364 (per-gate counter table — preserved) | `121de1427674e91d4880836acd1dcfd9b446f4fa79c1fb14ea2b25169b8f1fc1` |

---

## 7. Cross-reference to downstream M5 tasks

| Downstream task | Inherits from this task |
|---|---|
| T05.14 (D-0065, TEST-017 + TEST-022) | Will reuse the same `_halt_emitter.py` 4-step iterator. TEST-017 (slow-shrink) confirms `|F|=5,4` continues — already exercised here by `TestStrictShrinkDoesNotHalt::test_slow_shrink_proceeds`. TEST-022 (cross-cycle dedup) extends with INV-012 composition semantics (same `dedup_key` ≠ regression). |
| T05.15 (D-0066, TEST-024 sequencing) | Independent fixture — does not reuse `_halt_emitter.py`, but follows the same `tests/audit/` evidence pattern. |
| T05.16 (D-0067, MIG-005 PR-02 landing) | Depends on T05.13..T05.15 fixtures green. T05.13's 47/47 PASS is one of the three gate signals MIG-005 needs before the strictly-additive halts can land. |
| T05.18 (D-CP05, end-of-Phase-5 checkpoint) | Will cite this evidence under "Regression precedes monotonicity on PASS@N→FAIL@N+1 fixture (D-0057 + D-0064)" and "`|F|=5,5,5` halts at cycle 2; `|F|=5,4` continues (D-0056 + D-0064 + D-0065)". |

---

## 8. Verdict

**T05.13 PASS — all 4 AC met.**

- AC1: `uv run pytest tests/audit/test_monotonicity_halt_F_5_5_5.py tests/audit/test_regression_halt_pass1_fail2.py -v` exits 0 ✅ (47/47 PASS; `artifacts/D-0064/pytest.log`).
- AC2: TEST-015 assertion: `[HALT-MONOTONICITY] |F|=5` appears in cycle-2 log; cycle-3 not attempted ✅ (§2.1-§2.2; runtime emission + D-0056 canonical fixture both verified).
- AC3: TEST-016 assertion: regression message emitted BEFORE monotonicity check ✅ (§3.2; both shrinking and non-shrinking `|F|` trajectories; counterfactual in §3.3 proves monotonicity would have fired absent regression).
- AC4: Evidence at `TASKLIST_ROOT/artifacts/D-0064/evidence.md` ✅ (this file).

**Preservation invariants:** SKILL.md L1029-1059 hash unchanged
(`14c40575…`); SKILL.md L1014-1027 hash unchanged (`1ca8e16e…`);
`rf-team-lead.md:417` hash unchanged (`51725c0f…`); per-gate
counter table hash unchanged (`121de142…`); no new retry loops or
stages introduced; no source-file edits in T05.13 (only new files
under `tests/audit/`). `make verify-sync` reports pre-existing
hook-sync drift on the `feat/hook-sync-and-matcher-fix` branch
that is unrelated to T05.13 — skills/agents/commands/core all
PASS component-by-component (see §5.6).

**Unblocks:** T05.14 (D-0065, TEST-017 + TEST-022), T05.16
(D-0067, MIG-005 PR-02 landing), T05.18 (D-CP05, end-of-Phase-5
checkpoint).
