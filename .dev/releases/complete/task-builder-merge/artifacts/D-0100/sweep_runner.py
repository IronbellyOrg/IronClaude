"""T05.17 -- Slow-cycle correction false-halt-rate sweep driver.

Phase-5 / T05.17 deliverable (D-0100). Replays the 4-step ordering
iterator from ``tests/audit/_halt_emitter.py`` across three slow-shrink
trajectories — |F|=5,4 / |F|=5,3 / |F|=5,2 — to confirm none emit a
false halt under the X-003 rejection invariant.

Acceptance reference (phase-5-tasklist.md L811-819):

  Steps:
  2. Re-run |F|=5,4, |F|=5,3, |F|=5,2 fixtures.
  3. Confirm no false halts; document false-halt-rate metric baseline.

Output:
  * Prints a one-line PASS/FAIL summary per trajectory.
  * Prints the false-halt-rate metric (false_halts / trajectories).
  * Exit code 0 if all trajectories complete without halts.

Run: ``uv run python .dev/releases/current/task-builder-merge/artifacts/D-0100/sweep_runner.py``
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[6]
TESTS_AUDIT = REPO_ROOT / "tests" / "audit"
sys.path.insert(0, str(TESTS_AUDIT))

from _halt_emitter import CycleState, run_fix_cycle  # noqa: E402


def _trajectory(fail_n2: int) -> list[CycleState]:
    """Build a |F_1|=5 / |F_2|=fail_n2 / |F_3|=0 trajectory.

    Cycle-1 FAILs: item-3.1 .. item-3.5 (5 items, dedup-keys unique).
    Cycle-2 FAILs: first (5 - delta) items remain, where delta = 5 - fail_n2.
                   No new items introduced -> no PASS->FAIL flip
                   (the cycle-1 PASS set never overlaps the cycle-2 FAIL set).
    Cycle-3 FAILs: empty (converged).
    """
    base_fail = [f"item-3.{i}" for i in range(1, 6)]
    pass_set_c1 = {"item-1.1", "item-4.2", "item-6.1", "item-8.2", "item-10.1"}

    delta = 5 - fail_n2
    if delta <= 0 or fail_n2 < 0:
        raise ValueError(f"trajectory requires strict shrink; got |F_2|={fail_n2}")
    fixed = set(base_fail[:delta])
    fail_c2 = set(base_fail[delta:])
    pass_c2 = pass_set_c1 | fixed

    return [
        CycleState(cycle=1, fail_set=set(base_fail), pass_set=pass_set_c1),
        CycleState(cycle=2, fail_set=fail_c2, pass_set=pass_c2),
        CycleState(
            cycle=3,
            fail_set=set(),
            pass_set=pass_c2 | fail_c2,
        ),
    ]


def main() -> int:
    trajectories = [("|F|=5,4", 4), ("|F|=5,3", 3), ("|F|=5,2", 2)]
    false_halts = 0
    print(
        "T05.17 slow-cycle correction false-halt-rate sweep "
        "(X-003 rejection enforcement)"
    )
    print("=" * 78)
    print(f"{'trajectory':<14}  {'halt_message':<40}  {'cycle_3_started':<16}  verdict")
    print("-" * 78)

    for label, fail_n2 in trajectories:
        log = run_fix_cycle(_trajectory(fail_n2))
        halt_msg = log.halt_message if log.halt_message else "<none>"
        cycle_3 = 3 in log.cycles_started
        halted = log.halt_message is not None
        if halted:
            false_halts += 1
            verdict = "FAIL (false halt)"
        elif not cycle_3:
            false_halts += 1
            verdict = "FAIL (cycle 3 missing)"
        else:
            verdict = "PASS"
        print(f"{label:<14}  {halt_msg:<40}  {str(cycle_3):<16}  {verdict}")

    total = len(trajectories)
    rate = false_halts / total
    print("-" * 78)
    print(f"false_halts={false_halts}/{total}  false_halt_rate={rate:.3f}")
    print(
        "baseline: false_halt_rate=0.000 expected on legitimate slow-shrink "
        "cases (X-003 REJECTED — binary non-shrink predicate, no rate threshold)"
    )

    return 0 if false_halts == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
