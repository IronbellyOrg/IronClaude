"""Render-compare harness for the observer visual-parity gate (issue #606, spec section 8 and step 0.3).

Command::

    uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out <dir> \
        [--depth 16,256,truecolor] [--heights 44,40,24,12,8] [--check]

For the screens ``ledger``, ``questions``, ``desk`` and ``desk-planask`` (views from
``inputs/tools/render_current.py``) at widths 160, 116 and 80 (heights 48, 42, 42) it writes, per
width into ``<out>/<width>/``:

    <screen>.txt                 plain ``screen_lines``
    <screen>.<depth>.ansi/.html  the coloured stream and ``export_html`` for each selected depth
    <screen>.nocolor.txt         env NO_COLOR=1
    <screen>.ascii.txt           ``--ascii`` plain, and <screen>.ascii.ansi (16-colour stream)
    <screen>.h<height>.txt       with --heights: a text-only height matrix
    manifest.json                line counts, widest cell, and which depths were really produced

``--check`` also writes ``<out>/checks.json``: one entry per script-checked rubric row, each
``{"status": "pass"|"fail"|"na", "evidence": [...]}``. A run without ``--check`` or without all
five passes is not a valid gate run.

The capture is ``console.file.getvalue()`` of a recording console; ``export_text(styles=True)``
is never used (it ignores NO_COLOR and the colour downgrade).
"""

from __future__ import annotations

import argparse
import dataclasses
import importlib.util
import io
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
VP = HERE.parent
ROOT = VP.parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _load_current():
    spec = importlib.util.spec_from_file_location(
        "render_current", VP / "inputs" / "tools" / "render_current.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


current = _load_current()

from rich.cells import cell_len  # noqa: E402

from superclaude.cli.observe import view as observe_view  # noqa: E402
from superclaude.cli.observe.render import render, screen_lines  # noqa: E402
from superclaude.cli.observe.terminal import make_console, resolve_policy  # noqa: E402

SCREENS = current.SCREENS
WIDTHS = current.WIDTHS
HEIGHTS = current.MOCKUP_HEIGHTS
RICH_DEPTH = {"16": "standard", "256": "256", "truecolor": "truecolor"}
SGR = re.compile(r"\x1b\[[0-9;]*m")
ANSI_ANY = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
# The eight mockup palette triples (spec RB-01, 04 section 2).
PALETTE = {
    (225, 233, 238): "base",
    (165, 182, 194): "muted",
    (82, 108, 128): "slate",
    (250, 178, 25): "amber",
    (112, 205, 226): "cyan",
    (139, 215, 175): "green",
    (240, 141, 150): "red",
    (194, 173, 242): "violet",
}
HEX_RUN = re.compile(r"[0-9a-fA-F]{32,}")


def strip_sgr(text: str) -> str:
    return SGR.sub("", text)


@dataclass
class CaseOutput:
    plain: list[str]
    stream: str
    html: str
    produced_depth: str  # the depth really rendered ("n/a" when the policy cannot carry it yet)


def _policy(width: int, height: int, *, env: dict, ascii: bool):
    return resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)


def render_case(view, width: int, height: int, *, env: dict, ascii: bool, depth: str = "16") -> CaseOutput:
    """One render: the plain lines, the written stream (SGR included) and the recorded HTML."""
    policy = _policy(width, height, env=env, ascii=ascii)
    produced = depth
    if hasattr(policy, "color_system"):
        if policy.color_system is not None:
            policy = dataclasses.replace(policy, color_system=RICH_DEPTH[depth])
    elif depth != "16":
        produced = "not-available-before-P1"  # make_console pins "standard" until step 1.1
    console = make_console(policy, file=io.StringIO(), record=True)
    console.print(render(view, policy))
    return CaseOutput(
        plain=screen_lines(view, policy),
        stream=console.file.getvalue(),
        html=console.export_html(inline_styles=True),
        produced_depth=produced,
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# -- checks ---------------------------------------------------------------------------------


def _row(status: str, *evidence: str) -> dict:
    return {"status": status, "evidence": [e for e in evidence if e]}


def _flat(lines) -> str:
    return " ".join(" ".join(lines).split())


def _unframe(line: str) -> str:
    """Strip a one-cell margin and a rounded, heavy or ASCII border pair when present."""
    text = re.sub(r"^\s?[│┃|]\s", "", line)
    return re.sub(r"\s[│┃|]\s?$", "", text) if text != line else line


_TOP = re.compile(r"^ ?[╭┏+][─━-] (.*?) [─━-]*[╮┓+]$")
_BOTTOM = re.compile(r"^ ?[╰┗+][─━-]+[╯┛+]$")
_BODY = re.compile(r"^ ?[│┃|] (.*) [│┃|]$")


def _unframed(lines) -> list[str]:
    """The screen as before the frames: a top border becomes its title row, a body row loses its
    borders, a bottom border is dropped, any other line stays."""
    out: list[str] = []
    for ln in lines:
        if m := _TOP.match(ln):
            out.append(m.group(1))
        elif _BOTTOM.match(ln):
            continue
        else:
            out.append(m.group(1).rstrip() if (m := _BODY.match(ln)) else ln)
    return out


_PANE_END = "╮╯│┓┛┃+|"


def _split_panes(lines, width: int) -> list[str]:
    """The screen lines with each two-column desk row split into its two panes (the twin of
    ``split_panes`` in tests/observe/conftest.py): in a run of consecutive two-column rows the
    left panes come first, then the right panes. The left pane is ``width - 4 - 80`` cells at
    160 and above and ``width - 4 - 46`` from 116 to 159; below that nothing is split."""
    if width >= 160:
        cut = 1 + width - 4 - 80
    elif width >= 116:
        cut = 1 + width - 4 - 46
    else:
        return list(lines)

    def two_columns(line: str) -> bool:
        if len(line) < cut + 2 or line[cut : cut + 2] != "  ":
            return False
        if line[:cut].strip():
            return line[cut - 1] in _PANE_END
        return len(line) > cut + 2 and line[cut + 2] in "╭╰│┏┗┃+|"

    out: list[str] = []
    run: list[tuple[str, str]] = []

    def flush() -> None:
        out.extend(a for a, _ in run if a.strip())
        out.extend(b for _, b in run if b.strip())
        run.clear()

    for ln in lines:
        if two_columns(ln):
            run.append((ln[:cut].rstrip(), (" " + ln[cut + 2 :]).rstrip()))
        else:
            flush()
            out.append(ln)
    flush()
    return out


def _screen_counts(panel, width: int) -> str:
    """The count as the screen shows it: the full line at 160 and 116 (the strip), the short
    forms at 80 (owner ruling 2026-11-18, `seen !done` and `proof-done`); the record keeps the
    full ``counts_line``."""
    if width >= 116:
        return panel.counts_line
    return getattr(panel, "screen_counts_line", "") or panel.counts_line


def _required_literals(name: str, view, width: int = 160) -> list[str]:
    out: list[str] = []
    panel = view.questions
    if panel is None:
        out.append(view.gap_notice)
    else:
        out += [
            panel.disclosure,
            panel.caveat_line,
            panel.retention_line,
            _screen_counts(panel, width),
        ]
        if name in ("desk", "desk-planask"):
            out.append(observe_view.DESK_TITLE)
    return [x for x in out if x]


def check_screen(name: str, view, width: int, height: int, outs: dict, nocolor: CaseOutput, ascii_out: CaseOutput):
    """Per-screen rows; returns {row: {status, evidence}} for one width."""
    rows: dict[str, dict] = {}
    plain = outs["plain"]
    # Text checks read the screen as before the frames (top border to its title, body rows
    # without their borders, bottom borders dropped); shape and height checks use ``plain``.
    # The two-column desk rows are read pane by pane (``_split_panes``).
    panes = _split_panes(plain, width)
    text_lines = _unframed(panes)
    flat = _flat(text_lines)

    # RB-05 required literals, whole and uncut (whitespace-collapsed, so wrapping is allowed).
    missing = [lit for lit in _required_literals(name, view, width) if _flat([lit]) not in flat]
    rows["RB-05"] = _row("fail", *[f"missing or cut: {m[:70]}" for m in missing]) if missing else _row("pass")

    # RB-06 NO_COLOR: no ESC, same text as the coloured pass after SGR removal.
    esc = "\x1b" in nocolor.stream
    coloured = [ln.rstrip() for ln in strip_sgr(outs["stream"]).split("\n")]
    plain_lines = [ln.rstrip() for ln in plain]
    same = [ln for ln in coloured if ln] == [ln for ln in plain_lines if ln]
    rows["RB-06"] = (
        _row("fail", "ESC byte in NO_COLOR stream" if esc else "", "" if same else "SGR-stripped text differs from plain")
        if esc or not same
        else _row("pass")
    )

    # RB-07 ASCII: pure ASCII; a framed pane uses + - |, never ?
    bad: list[str] = []
    if not all(ln.isascii() for ln in ascii_out.plain) or not ascii_out.stream.isascii():
        bad.append("non-ASCII in ASCII pass")
    borders = [ln for ln in ascii_out.plain if ln.lstrip().startswith("+")]
    bad += [f"? inside a border: {ln[:60]}" for ln in borders if "?" in ln]
    rows["RB-07"] = _row("fail", *bad) if bad else (_row("pass") if borders else _row("pass", "no frame yet; text part only"))

    # RB-08 fit: width, height, footer last, no blink, no mouse sequences.
    problems: list[str] = []
    for ln in plain:
        if cell_len(ln) > width:
            problems.append(f"line wider than {width}: {ln[:50]}")
    if len(plain) > height:
        problems.append(f"{len(plain)} rows > height {height}")
    if not any("q quit" in ln for ln in plain[-4:]):
        problems.append("footer keys are not among the last lines")
    for label, text in (("stream", outs["stream"]), ("nocolor", nocolor.stream)):
        if re.search(r"\x1b\[(?:[0-9;]*;)?[56](?:;[0-9;]*)?m", text):
            problems.append(f"SGR 5 or 6 (blink) in {label}")
        if re.search(r"\x1b\[\?100[0236]h", text):
            problems.append(f"mouse sequence in {label}")
    rows["RB-08"] = _row("fail", *problems) if problems else _row("pass")

    # RB-13 the key list is whole: every two-space group sits whole on one line; none cut by ' >'.
    help_line = getattr(view, "help_line", "")
    groups = [g for g in re.split(r"\s{2,}", help_line.strip()) if g]
    cut = [g for g in groups if not any(g in ln for ln in plain)]
    rows["RB-13"] = _row("fail", *[f"key group not whole: {g}" for g in cut]) if cut else _row("pass")

    # RB-20 a rule line precedes the footer keys; the key pair n/p question is intact when linked.
    first_help = next((i for i, ln in enumerate(plain) if groups and groups[0] in ln), None)
    rule_ok = first_help is not None and first_help > 0 and bool(re.fullmatch(r"[─-]{10,}", plain[first_help - 1].strip()))
    pair_ok = "n/p question" not in help_line or any("n/p question" in ln for ln in plain)
    rows["RB-20"] = _row("pass") if rule_ok and pair_ok else _row("fail", "" if rule_ok else "no rule line above the footer", "" if pair_ok else "n/p question split")

    # RB-21 counts lines are not cut inside a token: a trailing ' >' must follow a space.
    cut_counts = [ln for ln in plain[:6] if ln.endswith(">") and len(ln) > 1 and ln[-2] != " "]
    rows["RB-21"] = _row("fail", *[f"cut inside a token: {ln[-30:]}" for ln in cut_counts]) if cut_counts else _row("pass")

    # RB-19 Q7 is replaced by RB-27 (spec step 2.12): the hash is no longer shown at all.
    if name == "desk-planask":
        rows["RB-19"] = _row("na", "replaced by RB-27 (spec step 2.12): the hash is not shown")
    # RB-27 no run of 32 hex characters on the questions screen or the desk.
    if name != "ledger":
        runs = [ln for ln in plain if HEX_RUN.search(ln)]
        rows["RB-27"] = _row("fail", *[f"hex run shown: {ln.strip()[:70]}" for ln in runs[:2]]) if runs else _row("pass")

    # RB-24 string census (Part C): the question text, the Run id, the count words and the
    # freshness state of the question source each occur once on the screen (the panel's own state
    # line `question read: ...` is the one allowed second mention of the state, RR 45).
    panel = view.questions
    if panel is not None and name != "ledger":
        census: dict[str, int] = {}
        if getattr(view, "desk", None) is not None and view.desk.ask:
            census[f"question text {view.desk.ask[:30]!r}"] = flat.count(_flat([view.desk.ask]))
        else:
            for q in panel.lines:
                census[f"question text {q.shown[:30]!r}"] = flat.count(_flat([q.shown]))
        census["Run id"] = flat.count(panel.run_id)
        short = width < 116  # 80 columns: the two 10-character short forms
        census["count label"] = flat.count("seen !done" if short else "seen, not resolved")
        census["closed label"] = flat.count("proof-done" if short else "closed by evidence")
        census["freshness cell"] = flat.count(getattr(panel, "screen_cell", "") or "questions OK")
        twice = [f"{k}: {n} times" for k, n in census.items() if n != 1]
        rows["RB-24"] = _row("fail", *twice) if twice else _row("pass")

        # RB-25 reasons said once, in the title.
        has_reason = any(getattr(q, "reason", "") for q in panel.lines)
        suffix = [ln for ln in plain if "reason unknown" in ln]
        note = "reasons: none in source" in flat
        bad = [f"row suffix: {ln.strip()[:60]}" for ln in suffix[:2]] + ([] if note or has_reason else ["title note missing"])
        rows["RB-25"] = _row("fail", *bad) if bad else _row("pass")

    # RB-26 status: one ACTIVE badge only for active/active/none, else three raw values.
    if name == "ledger":
        wrong = []
        for rv in view.visible_rows:
            line = next((ln for ln in plain if rv.dispatch_id in ln), "")
            active = (rv.dispatch_status, rv.terminal_state, rv.outcome) == ("active", "active", "none")
            triple = f"{rv.dispatch_status}/{rv.terminal_state}/{rv.outcome}"
            if line and active != (" ACTIVE" in line) and "FROZEN" not in line:
                wrong.append(f"{rv.dispatch_id}: ACTIVE shown={not active}")
            if line and not active and triple not in line and width >= 116:
                wrong.append(f"{rv.dispatch_id}: raw values {triple} not shown whole")
        rows["RB-26"] = _row("fail", *wrong[:3]) if wrong else _row("pass")
    elif name in ("desk", "desk-planask") and getattr(view, "desk", None) is not None:
        fields = dict(view.desk.session_fields)
        triple = (fields.get("dispatchStatus"), fields.get("terminalState"), fields.get("outcome"))
        block = panes[next(i for i, ln in enumerate(panes) if observe_view.DESK_TITLE in ln) :]
        shown_badge = any(re.match(r"^status\s+ACTIVE\b", _unframe(ln)) for ln in block)
        raw_rows = [lbl for lbl in ("dispatchStatus", "terminalState", "outcome") if any(re.match(rf"^{lbl}\s+\S", _unframe(ln)) for ln in block)]
        ok = shown_badge if triple == ("active", "active", "none") else (not shown_badge and len(raw_rows) == 3)
        rows["RB-26"] = _row("pass") if ok else _row("fail", f"badge={shown_badge} raw rows={raw_rows} for {triple}")

    # RB-28 ledger diet (the script part): no flags column, one rule line (above the footer), no
    # '+N more' row, a legend, and any non-alive value spelled out in the NO_COLOR pass.
    if name == "ledger":
        problems = []
        if any(re.search(r"\bflags\b", ln) for ln in plain[:12]):
            problems.append("a flags column heading is shown")
        rules = [ln for ln in plain if re.fullmatch(r"[─-]{10,}", ln.strip())]
        if len(rules) != 1:
            problems.append(f"{len(rules)} rule lines (only the footer rule may stay)")
        if any(re.search(r"\+\d+ more", ln) for ln in plain):
            problems.append("a '+N more' row is shown")
        if True:  # the liveness dot is at every width (the 80 column short form too)
            for rv in view.visible_rows:
                verdict = str(rv.raw.liveness_verdict)
                line = next((ln for ln in nocolor.plain if rv.dispatch_id in ln), "")
                if line and verdict not in ("alive", "live") and verdict not in line and "unknown" not in line:
                    problems.append(f"{rv.dispatch_id}: non-alive value {verdict!r} not spelled out")
        rows["RB-28"] = _row("fail", *problems[:3]) if problems else _row("pass")

    # RB-14 desk (a), (c), (d) on the plain pass.
    if name in ("desk", "desk-planask"):
        body = [_unframe(ln) for ln in panes]
        try:
            start = next(i for i, ln in enumerate(body) if observe_view.DESK_TITLE in ln)
            first = body[start + 1]
            # spec 2.9 (d) and 2.13: the first body line is `age <age>` (no message id) and the
            # field lines are `label<padding>value` with plain labels in one aligned column
            label = r"(?:session|state|alive|next|status|worktree|dispatchStatus|terminalState|outcome)"
            fields = [(i, ln) for i, ln in enumerate(body[start + 1 :], start + 1) if re.match(rf"^{label}\s+\S", ln)]
            a_ok = bool(re.match(r"^(?:\S+\s+)?age\s", first)) and (not fields or all(i > start + 1 for i, _ in fields))
            offsets = {re.match(rf"^({label}\s+)", ln).end() for _, ln in fields}
            c_ok = len(offsets) <= 1
            d_ok = all(cell_len(ln) <= width for ln in plain)
            parts = [] if a_ok else ["question text does not lead (qid age, then text, then fields)"]
            parts += [] if c_ok else [f"field values start at {len(offsets)} different offsets"]
            parts += [] if d_ok else ["a line exceeds the width"]
            rows["RB-14"] = _row("fail", *parts) if parts else _row("pass")
        except (StopIteration, IndexError):
            rows["RB-14"] = _row("fail", "desk not found on screen")

    # RB-17 census (b)/(c): run, caveat and retention lines occur exactly once each.
    if view.questions is not None:
        census = {lit: flat.count(_flat([lit])) for lit in (view.questions.run_line, view.questions.caveat_line, view.questions.retention_line) if lit}
        wrong = [f"{k[:40]}: {n} times" for k, n in census.items() if n != 1]
        # (a)-(d): when a RETAIN CONTEXT frame is drawn it holds all three lines (a, b); at 80
        # columns no such frame exists (d); when it is dropped the lines are in the list (c).
        retain = any(_TOP.match(ln) and "RETAIN CONTEXT" in ln for ln in plain)
        if width < 116 and retain:
            wrong.append("a RETAIN CONTEXT frame at 80 columns")
        if retain:
            start = next(i for i, ln in enumerate(plain) if _TOP.match(ln) and "RETAIN CONTEXT" in ln)
            end = next((i for i in range(start + 1, len(plain)) if _BOTTOM.match(plain[i])), len(plain))
            body = _flat(_unframed(plain[start + 1 : end]))
            wrong += [f"{lit[:40]} not in the RETAIN pane" for lit in census if _flat([lit]) not in body]
        rows["RB-17"] = _row("fail", *wrong) if wrong else _row("pass", "census plus the RETAIN pane contents")

    # RB-04 (c), (d): the counts line is whole on one line with the figure.
    if view.questions is not None:
        # 160 and 116: the strip shows the full line; 80: the list line shows the two short forms
        # (owner ruling 2026-11-18: RB-04 (c) is read with them at 80 columns)
        counts = _screen_counts(view.questions, width)
        whole = any(_flat([counts]) in _flat([ln]) for ln in text_lines)
        # (d) at 80 columns no strip frame; at 160 and 116 the strip frame holds the title
        has_strip = any(_TOP.match(ln) and "SEEN, NOT RESOLVED" in ln for ln in plain)
        want_strip = width >= 116
        bad = []
        if not whole:
            bad.append("counts line not whole on one line")
        if has_strip != want_strip:
            bad.append(f"strip frame {'missing' if want_strip else 'present at 80 columns'}")
        if has_strip:  # the figure N equals the number in the count line
            figure = re.search(r"seen, not resolved: (\d+)", flat)
            if not figure or figure.group(1) != view.questions.count_figure:
                bad.append("figure does not equal the count")
        rows["RB-04"] = _row("fail", *bad) if bad else _row("pass")

    # RB-01 (a): every foreground colour of the truecolor stream is one of the eight triples.
    return rows


def role_census_truecolor(stream: str) -> dict:
    colours = set()
    for m in re.finditer(r"\x1b\[([0-9;]*)m", stream):
        parts = [int(p) for p in m.group(1).split(";") if p.isdigit()]
        i = 0
        while i < len(parts):
            if parts[i] == 38 and parts[i + 1 : i + 2] == [2] and len(parts) >= i + 5:
                colours.add(tuple(parts[i + 2 : i + 5]))
                i += 5
            elif parts[i] == 38 and parts[i + 1 : i + 2] == [5]:
                colours.add(("idx", parts[i + 2]) if i + 2 < len(parts) else ("idx", -1))
                i += 3
            else:
                if 30 <= parts[i] <= 37 or 90 <= parts[i] <= 97:
                    colours.add(("ansi", parts[i]))
                i += 1
    return {c for c in colours}


def theme_rows() -> dict:
    """RB-09 and RB-10(d) read the theme module when it exists (phase 2 onward)."""
    try:
        from superclaude.cli.observe import theme  # type: ignore
    except ImportError:
        return {
            "RB-09": _row("na", "theme.py not built yet (plan Phase 2)"),
            "RB-10": _row("na", "theme.py not built yet (plan Phase 2)"),
        }
    palette_roles = ("attention", "identity", "secondary", "muted", "state_running", "state_settled", "state_failed", "state_frozen")
    codes = {}
    for role in palette_roles:
        style = theme.style_for(role, "standard")
        codes[role] = None if style is None else style.color.number if style.color is not None else None
    distinct = len({v for v in codes.values() if v is not None}) == len([v for v in codes.values() if v is not None]) and len(set(codes.values())) == len(codes)
    rb09 = _row("pass") if distinct else _row("fail", f"16-colour role codes collide: {codes}")
    keys = [("workerState", "running"), ("workerState", "succeeded"), ("workerState", "failed"), ("dispatchStatus", "completed"), ("liveness", "alive")]
    state = getattr(theme, "STATE_ROLE", {})
    missing = [k for k in keys if k not in state]
    frozen_ok = getattr(theme, "FROZEN_ROLE", None) == "state_frozen"
    rb10 = _row("pass", "(d) table keys only; (a)(b) census is added with the phase 2 gate") if not missing and frozen_ok else _row("fail", f"STATE_ROLE missing {missing}", "" if frozen_ok else "FROZEN_ROLE != state_frozen")
    return {"RB-09": rb09, "RB-10": rb10}


def fg_by_char(stream_line: str) -> list[tuple[str, int | None]]:
    """(character, foreground SGR code) for each visible character of one 16-colour stream line."""
    out: list[tuple[str, int | None]] = []
    fg: int | None = None
    pos = 0
    for m in SGR.finditer(stream_line):
        out += [(ch, fg) for ch in stream_line[pos : m.start()]]
        for p in [int(x) if x else 0 for x in m.group(0)[2:-1].split(";")]:
            if p == 0 or p == 39:
                fg = None
            elif 30 <= p <= 37 or 90 <= p <= 97:
                fg = p
        pos = m.end()
    out += [(ch, fg) for ch in stream_line[pos:]]
    return out


def state_census(stream: str) -> dict:
    """RB-10 (a) and (b) on the 16-colour ledger stream: a state word in the table carries exactly
    its role's colour, and every other state word carries the body colour (never a state role)."""
    try:
        from superclaude.cli.observe import theme  # type: ignore
    except ImportError:
        return _row("na", "theme.py not built yet (plan Phase 2)")

    def code(role: str) -> int | None:
        style = theme.style_for(role, "standard")
        number = style.color.number if style and style.color is not None else None
        return None if number is None else (30 + number if number < 8 else 82 + number)

    in_table = {value: theme.STATE_ROLE[key] for key, value in ((k, k[1]) for k in theme.STATE_ROLE)}
    other = ("idle", "blocked", "exited", "ready", "stopped", "abandoned", "active", "dispatched", "ended", "unverifiable")
    bad: list[str] = []
    checked = 0
    for line in stream.split("\n"):
        plain = strip_sgr(line)
        if not re.search(r"\bw-\d{3}\b", plain):
            continue
        chars = fg_by_char(line)
        for m in re.finditer(r"\b[A-Za-z]+\b", plain):
            word = m.group(0)
            if word in in_table:
                want = code(in_table[word])
            elif word in other:
                want = code("body")
            else:
                continue
            checked += 1
            got = {fg for _, fg in chars[m.start() : m.end()]}
            if got != {want}:
                bad.append(f"{word!r} has colours {sorted(map(str, got))}, want {want}: {plain.strip()[:60]}")
    if not checked:
        return _row("fail", "no state word found on the ledger rows")
    return _row("fail", *bad[:4]) if bad else _row("pass", f"{checked} state words checked against the table")


# -- main -----------------------------------------------------------------------------------


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", required=True)
    ap.add_argument("--depth", default="16,256,truecolor")
    ap.add_argument("--heights", default="")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    out = Path(args.out)
    depths = [d.strip() for d in args.depth.split(",") if d.strip()]
    for d in depths:
        if d not in RICH_DEPTH:
            ap.error(f"unknown depth {d!r}; use 16, 256 or truecolor")
    heights = [int(h) for h in args.heights.split(",") if h.strip()]
    views = current.build_views()
    checks: dict[str, dict] = {}
    all_rows: dict[str, list] = {}

    def merge(row_id: str, key: str, row: dict) -> None:
        all_rows.setdefault(row_id, []).append((key, row))

    for width in WIDTHS:
        wdir = out / str(width)
        height = HEIGHTS[width]
        manifest: dict = {"width": width, "height": height, "screens": {}}
        for name in SCREENS:
            view = views[name]
            base = render_case(view, width, height, env={}, ascii=False, depth="16")
            nocolor = render_case(view, width, height, env={"NO_COLOR": "1"}, ascii=False)
            ascii_out = render_case(view, width, height, env={}, ascii=True)
            _write(wdir / f"{name}.txt", "\n".join(base.plain) + "\n")
            _write(wdir / f"{name}.nocolor.txt", nocolor.stream)
            _write(wdir / f"{name}.ascii.txt", "\n".join(ascii_out.plain) + "\n")
            _write(wdir / f"{name}.ascii.ansi", ascii_out.stream)
            entry = {"lines": len(base.plain), "widest_cell": max((cell_len(x) for x in base.plain), default=0), "depths": {}}
            truecolor_stream = ""
            for depth in depths:
                case = render_case(view, width, height, env={}, ascii=False, depth=depth)
                _write(wdir / f"{name}.{depth}.ansi", case.stream)
                _write(wdir / f"{name}.{depth}.html", case.html)
                entry["depths"][depth] = case.produced_depth
                if depth == "truecolor":
                    truecolor_stream = case.stream
            for h in heights:
                _write(wdir / f"{name}.h{h}.txt", "\n".join(render_case(view, width, h, env={}, ascii=False).plain) + "\n")
            manifest["screens"][name] = entry
            if args.check:
                rows = check_screen(name, view, width, height, {"plain": base.plain, "stream": base.stream}, nocolor, ascii_out)
                for rid, row in rows.items():
                    merge(rid, f"{name}@{width}", row)
                if name == "ledger" and width == 160:
                    merge("RB-10", "census@160", state_census(base.stream))
                if truecolor_stream and entry["depths"].get("truecolor") == "truecolor":
                    colours = role_census_truecolor(truecolor_stream)
                    stray = [c for c in colours if c not in PALETTE]
                    merge("RB-01", f"{name}@{width}", _row("fail", f"foreground colours outside the eight triples: {sorted(map(str, stray))[:4]}") if stray else _row("pass", "census (a) only; (b)-(f) are reviewer rows"))
                else:
                    merge("RB-01", f"{name}@{width}", _row("na", "no truecolor stream before plan Phase 2"))
        _write(wdir / "manifest.json", json.dumps(manifest, indent=1, sort_keys=True))

    if args.check:
        for rid, row in theme_rows().items():
            merge(rid, "theme", row)
        for rid in ("RB-16",):
            all_rows[rid] = [("roles", _row("na", "needs role spans (plan Phase 2 and Phase 5); checked then"))]
        baseline_md = VP / "scores" / "baseline.md"
        n_known = baseline_md.exists() and re.search(r"RB-22 threshold N:\s*(\d+)", baseline_md.read_text(encoding="utf-8"))
        ledger_rows = []
        for width in (116, 80):
            lines = (out / str(width) / "ledger.txt").read_text(encoding="utf-8").splitlines()
            runs = [max((len(m.group(0)) for m in re.finditer(r"(?<=\S) {2,}(?=\S)", ln)), default=0) for ln in lines if re.search(r"w-\d{3}", ln)]
            ledger_rows.append((width, max(runs, default=0)))
        if n_known:
            limit = int(n_known.group(1))
            bad = [f"{w} cols: blank run {r} > N={limit}" for w, r in ledger_rows if r > limit]
            all_rows["RB-22"] = [("ledger", _row("fail", *bad) if bad else _row("pass", f"N={limit}"))]
        else:
            all_rows["RB-22"] = [("ledger", _row("na", f"threshold N not recorded yet; measured {ledger_rows}"))]
        for rid, entries in sorted(all_rows.items()):
            statuses = {row["status"] for _, row in entries}
            status = "fail" if "fail" in statuses else ("pass" if "pass" in statuses else "na")
            checks[rid] = {
                "status": status,
                "cases": {key: row for key, row in entries if row["status"] != "pass"} or {"all": "pass"},
            }
        _write(out / "checks.json", json.dumps(checks, indent=1, sort_keys=True))
    print(f"render_compare: wrote {out}" + (f" ({len(checks)} rubric rows checked)" if args.check else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
