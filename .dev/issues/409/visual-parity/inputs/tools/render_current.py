"""Render the observer's four reference screens from its own fixtures (baseline capture script).

Rebuilt for issue #606 (the original lived only in an untracked local checkout). It builds the
four views the render gate compares with the design mockups, with the test fake clock and the
fake runner, so no process is started and every run is repeatable:

- ``ledger``        questions off, the ``base`` fixture (the Signal Bridge pairing)
- ``questions``     questions on, link off, five questions (the Attention Ledger pairing)
- ``desk``          questions on, link on, one question selected (the Decision Desk pairing)
- ``desk-planask``  the same with the plan-approval question ``PLAN_ASK`` (64-hex hash and paths)

A direct run writes the plain (``screen_lines``) captures to ``--out``; the harness
``render_compare.py`` imports this module and uses ``build_views()`` instead. The screens now
carry colour roles: the coloured streams (truecolor, 256-colour and 16-colour ANSI, with their HTML
exports) and the NO_COLOR and ASCII passes are written by ``render_compare.py``, not here, so a
plain capture from this script holds no escape sequence by design, not because the product has
none. The baseline in ``scores/baseline.*`` is the pre-fix reference and is never overwritten;
write post-fix output only under the gate output directory
(``.dev/tasks/<package>/artifacts/gates/``).

Run from the repository root: ``uv run python .dev/issues/409/visual-parity/inputs/tools/render_current.py --out <dir>``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from superclaude.cli.observe.adapter import LiveSource  # noqa: E402
from superclaude.cli.observe.collector import Collector, FixtureSource  # noqa: E402
from superclaude.cli.observe.render import screen_lines  # noqa: E402
from superclaude.cli.observe.terminal import resolve_policy  # noqa: E402
from superclaude.cli.observe.view import Session, build_view  # noqa: E402
from tests.observe.conftest import (  # noqa: E402
    QRUN,
    FakeClock,
    FakeDiscover,
    FakeRunner,
    make_envelope,
    make_question_envelope,
    make_question_rows,
    make_rows,
    question_payload,
    routed_runner_responses,
)

SCREENS = ("ledger", "questions", "desk", "desk-planask")
WIDTHS = (160, 116, 80)
# Heights of the three design mockup frames (04 section 4); render_current's old height 50 was not like for like.
MOCKUP_HEIGHTS = {160: 48, 116: 42, 80: 42}
HASH = "0123456789abcdef" * 4
# Twin of PLAN_ASK in tests/observe/test_render.py (R3 block): keep the two identical.
PLAN_ASK = (
    "Approve the plan in .dev/plans/observer-visual-parity/plan.md before the worker edits "
    "src/superclaude/cli/observe/render.py and src/superclaude/cli/observe/terminal.py "
    f"(plan hash {HASH})?"
)


def _question_view(clock, rows, *, link: bool, selected: int | None):
    worker = (0, json.dumps(make_envelope(make_rows(3, 1), total=3)))
    message = (0, json.dumps(make_question_envelope(rows)))
    runner = FakeRunner([], [routed_runner_responses(worker, message)])
    result = Collector(
        LiveSource(runner, FakeDiscover([])),
        clock,
        run_id=QRUN,
        questions=True,
        link=link,
    ).run_once()
    session = Session(
        selected_question=None if selected is None else (QRUN, f"msg_{selected:012x}")
    )
    return build_view(result, session, clock)


def _linked_rows(specs):
    rows = []
    for index, (dispatch, text) in enumerate(specs):
        rows += make_question_rows(
            1, start=index, payload=question_payload(dispatch, text)
        )
    return rows


def build_views() -> dict:
    """The four reference views, each built with its own fake clock."""
    clock = FakeClock()
    collector = Collector(FixtureSource("base"), clock)
    collector.run_once()
    ledger = build_view(collector.run_once(), Session(), clock)
    questions = _question_view(
        FakeClock(), make_question_rows(5), link=False, selected=0
    )
    desk = _question_view(
        FakeClock(),
        _linked_rows([("w-001", "Which branch should the worker rebase on?"), ("w-002", "Ship the change now?")]),
        link=True,
        selected=1,
    )
    plan = _question_view(
        FakeClock(),
        _linked_rows([("w-001", "Which branch should the worker rebase on?"), ("w-002", PLAN_ASK)]),
        link=True,
        selected=1,
    )
    return {"ledger": ledger, "questions": questions, "desk": desk, "desk-planask": plan}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", required=True, help="directory for the plain captures")
    args = parser.parse_args()
    out = Path(args.out)
    views = build_views()
    for width in WIDTHS:
        (out / str(width)).mkdir(parents=True, exist_ok=True)
        policy = resolve_policy({}, "utf-8", {"ascii": False}, width, MOCKUP_HEIGHTS[width])
        for name in SCREENS:
            text = "\n".join(screen_lines(views[name], policy)) + "\n"
            (out / str(width) / f"{name}.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
