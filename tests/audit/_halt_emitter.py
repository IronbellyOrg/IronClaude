"""Shared 4-step fix-cycle halt emitter for TEST-015 + TEST-016.

Phase-5 / T05.13 helper. Implements the SKILL.md §A.9 "API-004
Fix-Loop Halt Signals" 4-step ordering rule
(``regression → monotonicity → hard-cap → proceed``) in pure
Python so both ``test_monotonicity_halt_F_5_5_5.py`` (TEST-015) and
``test_regression_halt_pass1_fail2.py`` (TEST-016) exercise the
same emitter — that is what makes the precedence-rule assertions
in TEST-016 load-bearing against the actual halt-string emitter.

The byte-exact wire strings frozen by API-004-M5 (SKILL.md row 1
and row 2 of the halt-message table) are emitted via
``emit_monotonicity_halt`` / ``emit_regression_halt``. The
``run_fix_cycle`` driver implements the strict ordering rule and
the "Do NOT consult subsequent steps" invariant at SKILL.md:1054.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple

HALT_MONOTONICITY_TEMPLATE = "[HALT-MONOTONICITY] |F|=<n>"


@dataclass
class CycleState:
    """End-of-cycle state for the fix-cycle loop.

    Mirrors the SKILL.md §A.9 F-set definition: ``F_n`` is the SET
    (not multiset) of FAIL-verdict items at the end of fix cycle
    ``n``; set membership is by dedup-key identity. ``pass_set`` is
    the complementary set of PASS-verdict items needed for the
    regression check.
    """

    cycle: int
    fail_set: Set[str]
    pass_set: Set[str]


@dataclass
class HaltLog:
    """Output of the 4-step iterator over one fix-cycle run."""

    lines: List[str] = field(default_factory=list)
    transitions: List[Tuple[int, str, str]] = field(default_factory=list)
    halt_message: Optional[str] = None
    cycles_started: List[int] = field(default_factory=list)


def emit_monotonicity_halt(n: int) -> str:
    """Substitute ``<n>`` ← integer cardinality in the byte-exact wire
    template. Returns the exact string the fix-cycle wrapper MUST
    emit per API-004-M5.
    """
    return HALT_MONOTONICITY_TEMPLATE.replace("<n>", str(n))


def emit_regression_halt(item: str, prev_cycle: int) -> str:
    """Substitute ``X.Y`` ← regressed item and ``N`` ← prior-PASS
    cycle number in the byte-exact regression wire template. The
    em-dash ``—`` is U+2014 (NOT an ASCII hyphen).
    """
    return (
        f"Regression detected on Item {item} — previously PASS at cycle "
        f"{prev_cycle}, now FAIL. Halt overrides monotonicity check."
    )


def regression_step(prev: CycleState, curr: CycleState) -> Optional[str]:
    """Step 1 of the 4-step ordering rule. Returns the regressed
    item's dedup-key if any PASS@prev item is FAIL@curr, else None.

    Iteration order is sorted so the emitted halt message is
    deterministic across runs.
    """
    regressed = sorted(prev.pass_set & curr.fail_set)
    return regressed[0] if regressed else None


def monotonicity_step(prev: CycleState, curr: CycleState) -> Optional[int]:
    """Step 2 of the 4-step ordering rule. Returns the halting
    cardinality ``|F_{n+1}|`` if ``|F_n| > 0 AND |F_{n+1}| >= |F_n|``
    (strict non-shrink), else None.

    Gating on ``|F_n| > 0`` mirrors the SKILL.md §A.9 first
    invariant ("only consulted when ``|F_n| > 0``").
    """
    if len(prev.fail_set) == 0:
        return None
    if len(curr.fail_set) >= len(prev.fail_set):
        return len(curr.fail_set)
    return None


def run_fix_cycle(
    cycles: List[CycleState],
    *,
    gate: str = "research-gate",
    cap: int = 3,
) -> HaltLog:
    """Synthesise the execution log for a fix-cycle run. Implements
    the 4-step ordering rule per SKILL.md §A.9
    (``regression → monotonicity → hard-cap → proceed``). Returns
    the log + halt message (None if the loop completed without
    halting).
    """
    log = HaltLog()
    if not cycles:
        return log

    for state in cycles:
        log.cycles_started.append(state.cycle)
        log.lines.append(
            f"CYCLE {state.cycle} START   gate={gate} counter={state.cycle}/{cap}"
        )
        fails_csv = ",".join(sorted(state.fail_set))
        pass_csv = ",".join(sorted(state.pass_set))
        log.lines.append(
            f"CYCLE {state.cycle} END     gate={gate} "
            f"|F_{state.cycle}|={len(state.fail_set)} "
            f"fails=[{fails_csv}] pass=[{pass_csv}]"
        )

    # Walk transitions. The canonical fixture (D-0056 §1.3) labels
    # the transition that runs AFTER observing cycle ``curr`` as
    # ``curr -> curr+1`` — i.e., the decision "should we spawn cycle
    # curr+1?". The comparison itself is between ``prev`` and
    # ``curr``, but the LABEL is anchored to the prospective cycle.
    for prev, curr in zip(cycles, cycles[1:]):
        decision_from = curr.cycle
        decision_to = curr.cycle + 1

        # Step 1: regression.
        regressed = regression_step(prev, curr)
        if regressed is not None:
            verdict = (
                f"HALT  Item {regressed} flipped PASS@{prev.cycle} → "
                f"FAIL@{curr.cycle} (dedup-key={regressed}; previously PASS "
                f"at cycle {prev.cycle}, now FAIL)"
            )
            log.transitions.append((decision_to, "regression", verdict))
            log.lines.append(
                f"TRANSITION {decision_from}->{decision_to} step=regression  "
                f"verdict={verdict}"
            )
            log.halt_message = emit_regression_halt(regressed, prev.cycle)
            log.lines.append(f"HALT {log.halt_message}")
            return log

        log.transitions.append((decision_to, "regression", "PASS"))
        log.lines.append(
            f"TRANSITION {decision_from}->{decision_to} step=regression  verdict=PASS"
        )

        # Step 2: monotonicity.
        halt_n = monotonicity_step(prev, curr)
        if halt_n is not None:
            log.transitions.append((decision_to, "monotonicity", f"HALT |F|={halt_n}"))
            log.lines.append(
                f"TRANSITION {decision_from}->{decision_to} step=monotonicity "
                f"verdict=HALT  |F_{curr.cycle}|={halt_n} >= "
                f"|F_{prev.cycle}|={len(prev.fail_set)} (strict non-shrink)"
            )
            log.halt_message = emit_monotonicity_halt(halt_n)
            log.lines.append(f"HALT {log.halt_message}")
            return log

        log.transitions.append((decision_to, "monotonicity", "PROCEED"))
        log.lines.append(
            f"TRANSITION {decision_from}->{decision_to} step=monotonicity "
            f"verdict=PROCEED"
        )

        # Step 3: hard-cap (per-gate cap = the third-precedence backstop).
        if curr.cycle >= cap:
            log.transitions.append((decision_to, "hard-cap", "HALT"))
            log.lines.append(
                f"TRANSITION {decision_from}->{decision_to} step=hard-cap    "
                f"verdict=HALT counter={curr.cycle}/{cap}"
            )
            return log

        # Step 4: proceed.
        log.transitions.append((decision_to, "proceed", "re-spawn"))
        log.lines.append(
            f"TRANSITION {decision_from}->{decision_to} step=proceed     "
            f"re-spawn cycle {decision_to}"
        )

    return log
