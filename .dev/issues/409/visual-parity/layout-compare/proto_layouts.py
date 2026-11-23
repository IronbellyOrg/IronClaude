"""Prototype: the same real fixture data drawn stacked (A) and in two columns (B).

Not product code. It reads the observer's real view objects (questions panel, desk) and arranges
them with Rich panels in the mockup palette, so the only difference between A and B is arrangement.
Run from the repository root:
    PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 uv run python .dev/issues/409/visual-parity/layout-compare/proto_layouts.py
Writes layout-compare/html/<screen>-<width>.html (A over B; width 80 has only the stacked form,
because the spec keeps 80 columns stacked in both options).
"""

from __future__ import annotations

import io
import json
import pathlib

from rich import box
from rich.console import Console, Group
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.collector import Collector
from superclaude.cli.observe.view import Key, Session, apply_key, build_view
from tests.observe.conftest import (
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

OUT = pathlib.Path(".dev/issues/409/visual-parity/layout-compare/screens")
BASE, MUTED, SLATE = "rgb(225,233,238)", "rgb(165,182,194)", "rgb(82,108,128)"
AMBER, CYAN = "rgb(250,178,25)", "rgb(112,205,226)"
QUESTIONS = (
    ("w-001", "Approve plan: edit src/superclaude/cli/observe/render.py and tests/observe/test_render.py, hash 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"),
    ("w-002", "Confirm deployment window"),
    ("w-003", "Name the release reviewer"),
)
FONT = {
    "0": ("███", "█ █", "█ █", "█ █", "███"), "1": (" █ ", "██ ", " █ ", " █ ", "███"),
    "2": ("███", "  █", "███", "█  ", "███"), "3": ("███", "  █", "███", "  █", "███"),
    "4": ("█ █", "█ █", "███", "  █", "  █"), "5": ("███", "█  ", "███", "  █", "███"),
    "6": ("███", "█  ", "███", "█ █", "███"), "7": ("███", "  █", "  █", "  █", "  █"),
    "8": ("███", "█ █", "███", "█ █", "███"), "9": ("███", "█ █", "███", "  █", "███"),
    "+": ("   ", " █ ", "███", " █ ", "   "),
}


def questions_result(clock):
    rows = make_rows(6, 2)
    for row, number in zip(rows, range(1, 7)):
        row["dispatchId"] = f"w-{number:03d}"
        row["resource"] = {"worktreeId": f"wt-{number}"}
    messages = []
    for index, (dispatch, text) in enumerate(QUESTIONS):
        messages += make_question_rows(1, start=index, payload=question_payload(dispatch, text))
    worker = (0, json.dumps(make_envelope(rows, total=6)))
    message = (0, json.dumps(make_question_envelope(messages)))
    runner = FakeRunner([], [routed_runner_responses(worker, message)])
    collector = Collector(
        LiveSource(runner, FakeDiscover([], "/opt/fake/orca")), clock,
        run_id=QRUN, questions=True, link=True,
    )
    return collector.run_once()


def pane(body, title, width, kind):
    colour = {"attention": AMBER, "secondary": SLATE, "count": CYAN}[kind]
    shape = box.HEAVY if kind == "attention" else box.ROUNDED
    return Panel(body, title=Text(title, style=f"bold {colour}"), title_align="left",
                 border_style=colour, box=shape, width=width, padding=(0, 1))


def tile(figure, width):
    rows = [Text(" ".join(FONT[c][r] for c in figure), style=f"bold {AMBER}") for r in range(5)]
    return Group(*rows)


def list_lines(panel):
    out = []
    for q in panel.lines:
        line = Text()
        line.append("▸ " if q.selected else "  ", style=f"bold {AMBER}")
        line.append(f"{q.age_text:>4}  ", style=f"bold {AMBER}")
        line.append(q.shown or q.text, style=f"bold {BASE}")
        line.append("  reason unknown", style=MUTED)
        out.append(line)
    return out


def muted(text):
    return Text(text, style=MUTED)


def questions_parts(panel, left_w, count_w):
    rows = list_lines(panel)
    figure = str(panel.open_total)
    ctx = [muted(panel.run_line), muted(panel.caveat_line), muted(panel.retention_line)]
    head = [muted(panel.disclosure)]
    return rows, figure, ctx, head


def questions_stacked(panel, width):
    w = width - 2
    rows, figure, ctx, head = questions_parts(panel, w, 0)
    body = Group(muted(panel.run_line), muted(panel.disclosure),
                 Text(panel.counts_line, style=f"bold {CYAN}"), muted(panel.caveat_line),
                 *rows, muted(panel.retention_line))
    return Padding(pane(body, panel.title, w, "attention"), (0, 1))


def questions_two(panel, width):
    right_w, gap = 42, 2
    left_w = width - 2 - gap - right_w
    rows, figure, ctx, head = questions_parts(panel, left_w, right_w)
    left = pane(Group(*head, *rows), panel.title, left_w, "attention")
    count = pane(Group(tile(figure, right_w), Text(panel.counts_line, style=BASE)),
                 "SEEN IS NOT RESOLVED", right_w, "count")
    retain = pane(Group(*ctx), "RETAIN CONTEXT", right_w, "secondary")
    grid = Table.grid(padding=0)
    grid.add_column(width=left_w)
    grid.add_column(width=gap)
    grid.add_column(width=right_w)
    grid.add_row(left, "", Group(count, retain))
    return Padding(grid, (0, 1))


def desk_parts(panel, desk, width):
    qpane_body = Group(Text(f"{desk.qid}  age {desk.age_text}", style=f"bold {AMBER}"),
                       Text(desk.ask, style=f"bold {AMBER}"))
    fields = Table.grid(padding=(0, 1))
    fields.add_column(style=MUTED)
    fields.add_column(style=BASE)
    for label, value in desk.session_fields:
        fields.add_row(label + ":", value)
    evidence = Group(fields, *[muted(n) for n in desk.notes])
    return qpane_body, evidence, list_lines(panel)


def desk_stacked(panel, desk, width):
    w = width - 2
    q, e, rows = desk_parts(panel, desk, w)
    return Padding(Group(pane(q, "DECISION DESK", w, "attention"),
                         pane(e, "LINKED SESSION", w, "secondary"),
                         pane(Group(*rows), "COORDINATOR QUESTIONS", w, "secondary")), (0, 1))


def desk_two(panel, desk, width):
    q, e, rows = desk_parts(panel, desk, width)
    gap = 2
    grid = Table.grid(padding=0)
    if width >= 160:
        lw, rw = 76, 80
        grid.add_column(width=lw)
        grid.add_column(width=gap)
        grid.add_column(width=rw)
        grid.add_row(Group(pane(q, "DECISION DESK", lw, "attention"),
                           pane(Group(*rows), "COORDINATOR QUESTIONS", lw, "secondary")),
                     "", pane(e, "LINKED SESSION", rw, "secondary"))
        return Padding(grid, (0, 1))
    full = width - 2
    lw, rw = 66, 46
    grid.add_column(width=lw)
    grid.add_column(width=gap)
    grid.add_column(width=rw)
    grid.add_row(pane(e, "LINKED SESSION", lw, "secondary"), "",
                 pane(Group(*rows), "COORDINATOR QUESTIONS", rw, "secondary"))
    return Padding(Group(pane(q, "DECISION DESK", full, "attention"), grid), (0, 1))


TEMPLATE = (
    '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>{stylesheet}'
    'body{{margin:0;background:#0b1620}}pre{{margin:0;padding:12px 16px;'
    'font-family:"DejaVu Sans Mono",monospace;font-size:14px;line-height:1.25;'
    'color:#e1e9ee;background:#0b1620}}</style></head><body><pre><code>{code}</code></pre></body></html>'
)


def page(width, label_a, a, label_b, b):
    """Return the screen as JSON: a list of lines, each a list of [text, [r,g,b] or null, bold]."""
    console = Console(width=width, force_terminal=True, color_system="truecolor", file=io.StringIO())
    parts = [Text(f" {label_a}", style=f"bold {CYAN}"), a]
    if b is not None:
        parts += [Text(""), Text(f" {label_b}", style=f"bold {CYAN}"), b]
    lines = console.render_lines(Group(*parts), console.options.update(width=width), pad=True)
    out = []
    for line in lines:
        cells = []
        for seg in line:
            colour = seg.style.color.get_truecolor() if seg.style and seg.style.color else None
            cells.append([seg.text, list(colour) if colour else None, bool(seg.style and seg.style.bold)])
        out.append(cells)
    return json.dumps(out)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    clock = FakeClock()
    result = questions_result(clock)
    session = Session()
    plain = build_view(result, session, clock)
    session, _ = apply_key(session, Key("text", "n"), plain, clock)
    desk_view = build_view(result, session, clock)
    for width in (160, 116, 80):
        two = width >= 116
        qa, qb = questions_stacked(plain.questions, width), (questions_two(plain.questions, width) if two else None)
        da = desk_stacked(desk_view.questions, desk_view.desk, width)
        db = desk_two(desk_view.questions, desk_view.desk, width) if two else None
        suffix = "" if two else " (80 columns: both options are stacked)"
        (OUT / f"questions-{width}.json").write_text(page(
            width, f"A. STACKED, {width} columns{suffix}", qa, f"B. TWO COLUMNS, {width} columns", qb), encoding="utf-8")
        (OUT / f"desk-{width}.json").write_text(page(
            width, f"A. STACKED, {width} columns{suffix}", da, f"B. TWO COLUMNS, {width} columns", db), encoding="utf-8")
    print("wrote", len(list(OUT.glob("*.json"))), "pages")


main()
