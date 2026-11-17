"""The link-off questions screen is byte-identical to the one captured before R3 (T64).

With the questions on and the link switch off, the keys line stays ``QUESTIONS_KEYS_LINE`` and
``screen_lines`` at 160, 116 and 80 columns (height 40, the fake clock) equals
``golden_questions_linkoff.json``, which was generated from the code before the link change.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector
from superclaude.cli.observe.render import screen_lines
from superclaude.cli.observe.terminal import resolve_policy
from superclaude.cli.observe.view import QUESTIONS_KEYS_LINE, Session, build_view
from tests.observe.conftest import (
    QRUN,
    FakeDiscover,
    FakeRunner,
    make_envelope,
    make_question_envelope,
    make_question_rows,
    make_rows,
    routed_runner_responses,
)

GOLDEN = Path(__file__).parent / "golden_questions_linkoff.json"
HEIGHT = 40
WIDTHS = (160, 116, 80)
KEYS_LITERAL = (
    "Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  "
    "m mark rows  e export all  q quit"
)


def _view(clock, rows):
    worker = (0, json.dumps(make_envelope(make_rows(4, 1), total=4)))
    message = (0, json.dumps(make_question_envelope(rows)))
    runner = FakeRunner([], [routed_runner_responses(worker, message)])
    collector = Collector(
        LiveSource(runner, FakeDiscover([])), clock, run_id=QRUN, questions=True
    )
    return build_view(collector.run_once(), Session(), clock)


def capture(clock):
    scenarios = {
        "five": make_question_rows(5),
        "long_subject": make_question_rows(3, subject="x" * 300),
    }
    out = {}
    for name, rows in scenarios.items():
        view = _view(clock, rows)
        out[name] = {
            str(width): screen_lines(
                view, resolve_policy({}, "utf-8", {"ascii": False}, width, HEIGHT)
            )
            for width in WIDTHS
        }
    return out


def test_the_link_off_keys_line_is_the_pinned_literal(fake_clock):
    assert QUESTIONS_KEYS_LINE == KEYS_LITERAL and len(KEYS_LITERAL) == 107
    assert _view(fake_clock, make_question_rows(2)).help_line == KEYS_LITERAL


@pytest.mark.parametrize("scenario", ("five", "long_subject"))
def test_the_link_off_questions_screen_equals_the_reference(fake_clock, scenario):
    golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
    assert capture(fake_clock)[scenario] == golden[scenario]
