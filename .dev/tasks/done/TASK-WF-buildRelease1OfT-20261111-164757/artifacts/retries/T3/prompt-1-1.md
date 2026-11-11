95c95f092862226ac361812c0c8c18c18eaed860
Review one task for spec compliance.

Task brief: 
## Task 3: Build the terminal policy `terminal.py`

Depends on: Task 2

Create `src/superclaude/cli/observe/terminal.py` and `tests/observe/test_terminal.py`, following `ARCHITECTURE-SPINE.md` AD-13 and CD-4, CD-5 and CD-8, and `rendering-rules.md` sections "Geometry and height" and "Truncation". It exposes `resolve_policy(env, encoding, flags, width, height) -> TerminalPolicy` (frozen dataclass), `output_encoding() -> str`, `make_console(policy, file=None, record=False) -> Console`, the single truncation helper `clip(text, width, policy) -> str`, the glyph table and a palette table. Rules: every console gets `highlight=False`, `markup=False` and an explicit `width`; `no_color` is true when `NO_COLOR` is set and non-empty (`1` and `yes` both) and is passed as `color_system=None` with `no_color=True`; `ascii` is true with the `--ascii` flag or a non-UTF-8 encoding (PROPOSED) and selects `box.ASCII`, `safe_box=True` and a glyph table mapping box drawing to `+-|` and other non-ASCII glyphs to ASCII; the palette is empty (CD-8) and never uses blink, faint, italic or underline; width classes are 160 and wider (full table), 116 to 159 (line form), 80 to 115 (short form) and below 80 (`terminal too narrow (min 80)`); a named constant `MIN_ROWS` (PROPOSED: 8, enough for two header lines, the COUNTS strip, the gap notice, one ledger row and the footer) with a `too_small` predicate. `clip` measures with `rich.cells.cell_len` (never `len()`), never splits a double-width character, and marks a cut with a single `>` that fits inside the width (or `>` mapped for ASCII). No other module may construct a `Console` or read `NO_COLOR`, `COLUMNS` or the stream encoding.

Acceptance criteria:
- [T3.AC1] `uv run pytest tests/observe/test_terminal.py -v` passes.
- [T3.AC2] T26: `NO_COLOR=1` and `NO_COLOR=yes` both produce output with no SGR colour codes, and a colour-enabled policy produces colour codes only where the palette sets them (none by default).
- [T3.AC3] T28: no output of a console made by `make_console` contains SGR 5 or 6 (blink), and the palette table contains no blink, faint, italic or underline style.
- [T3.AC4] T30 (helper part): for widths 1 to 40, `cell_len(clip(s, W)) <= W` for CJK and emoji strings, a cut never leaves half a double-width character, and a cut string ends with `>`; in ASCII mode the result of clipping an ASCII string is pure ASCII.
- [T3.AC5] A test shows `resolve_policy` returns `too_narrow` below 80 columns, the correct width class at 80, 115, 116, 159 and 160, and `too_small` below `MIN_ROWS` rows.
- [T3.AC6] A source scan test asserts no module under `src/superclaude/cli/observe/` other than `terminal.py` constructs `Console(` or reads `NO_COLOR`.

Global constraints: 
## Constraints

- Shorthand used in the tasks below. SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`; it holds the canonical contract: `SPEC.md` and its companions `ARCHITECTURE-SPINE.md` (decisions AD-1 to AD-20 and conditional decisions CD-1 to CD-16), `adapter-contract.md`, `rendering-rules.md`, `acceptance-tests.md` (tests T1 to T51), `release-gates.md`, `snapshot-export-schema.md` and `unverified-register.md`. SNAPSRC is `.dev/issues/409/tuibbs-review/architecture-options.md` (last section, the frozen snapshot fields). The package is `src/superclaude/cli/observe/` and its tests are `tests/observe/`. Where SPECDIR and the older `.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md` differ, SPECDIR wins.
- Scope is release 1 (R1: live `worker-list`, COUNTS and freshness strips, worker ledger with the verbatim `projection.nextAction.kind` column, capped paging, STALE after 45 s, changes since last look, the one-line question-source notice, the JSON snapshot) plus the offline R0 pieces R1 needs (key-reader spike, sanitizer, cell-width truncation, NO_COLOR and ASCII, fixture variants, text export, fixture mode). The owner chose the staged direction and confirmed Python + Rich with snapshot export in `.dev/issues/409/owner-decisions-20261108.md` (items 1 and 5), so the side-by-side R0 renders of the Attention Ledger and Decision Desk that were only input to that choice are not built.
- Out of scope, not built even as stubs: question rows and any `check`, `inbox` or message read (R2), the SEEN IS NOT RESOLVED and RETAIN CONTEXT panels, the Decision Desk (R3), `--include-remote` (R4), every write path into Orca (approve, retry, terminate, spawn, merge, reply, instruct), persisting the last-look baseline, the `read k of N Runs since start` header token and its collector counters (CD-10 default places it in the Attention Ledger header only), any Go or TUIBBS code, and moving `_find_orca()`.
- Acceptance tests not built because they serve only the excluded views: T7, T10, T17, T19, T45, T46, T50 and T51, and the question half of T12 and T47. Every other test in `acceptance-tests.md` that applies to the ledger view is mapped to a task below, plus the snapshot schema test (no ID assigned in the spec).
- Authorization evidence. The owner's message of 2026-11-11, "Proceed with building the first release", is taken as the go for R0 and R1, including registering `superclaude observe` (reading 1 of "production integration" in `release-gates.md`) and live read-only `worker-list` calls. Caveat: `release-gates.md` says the owner's own dated selection record (check AC-S) states the confirmed reading and the direction. No task here writes that record, and it stays a reviewer-checked item. The final report must say it was not seen.
- Live Orca calls. Only two kinds are ever made, both read-only, both through `adapter.py`: `worker-list --json --limit 100` polling (optional `--run <runId>`, optional `--cursor <value>`, no shell) and the one startup discovery through `_find_orca()` in `src/superclaude/cli/install_user_setup.py` (runs `skills list --json`, at most two candidates, 10 s each, once per process, outside the 15 s cycle budget and the 5-call cap). No key maps to an Orca call. The forbidden set (plain `check`, `--ack`, `--wait`, `--retry-request`, `dispatch`, `inbox`, any other verb) is checked before every call and is never shortened.
- Defaults taken for open owner questions (SPECDIR `ARCHITECTURE-SPINE.md` CD table), changeable by the owner: CD-2 change flags use `stage.worker`, `stage.dispatch`, `nextAction.kind`, `liveness.verdict` and `stage.detail` and `stage.activity` stay inspector-only; CD-3 snapshot rows use timestamp order; CD-4 only the spec-fixed height rules; CD-5 truncation glyph `>`; CD-6 `--once` prints the record text to stdout, `--snapshot PATH` sets the snapshot file, the default directory is `~/.local/state/superclaude/observe/`, files are 0600 and replaced atomically; CD-8 empty palette (plain text, meaning in words); CD-16 a ledger row does not name a shared `worktreeId`.
- Plan-author rules that close gaps in the spec (PROPOSED, the owner may change them). The state directory honours `XDG_STATE_HOME` when set so tests stay out of the real home folder. `--once` with a live source writes a snapshot only when `--snapshot` is given. Fixture mode (`--fixture <variant>`) never calls Orca and never writes a snapshot unless `--snapshot` is given. A failed key-reader spike blocks the interactive tasks and is reported to the owner; the Textual switch in AD-14 is applied only on the owner's say-so, and both toolkits are never built.
- Data handling. Raw Orca output is never logged, committed, or kept in fixtures; committed fixtures hold only redacted identifiers (no absolute path, terminal handle, token or credential). Worker free text (`stage.detail`, `stage.activity`) and failed-poll stderr are shown after control-character sanitizing, labelled `worker-reported`; they are not redacted and no credential or terminal-handle field is exported.
- No code is copied from TUIBBS-scp (AGPL-3.0); the design prototype `canvas.py` is never imported. Python 3.10 compatible, no new dependency (`rich`, `click`, `jsonschema` and `pexpect` are already dependencies in `pyproject.toml`), UV only (`uv run pytest tests/observe -v`, `uv run ruff check src/superclaude/cli/observe tests/observe`), and nothing is written under `.claude/`. Every task leaves ruff clean for the files it touches.
- A fact the source does not give is the single `UNKNOWN` sentinel (never `None`, `0`, `False`, `""`) and renders as the word `unknown`. Facts with no verified source render `unavailable (no source)`. Worker text always renders as literal text, never parsed as Rich markup.

Start sha: 95c95f092862226ac361812c0c8c18c18eaed860
Diff against the start snapshot: 
diff --git a/src/superclaude/cli/observe/terminal.py b/src/superclaude/cli/observe/terminal.py
new file mode 100644
index 000000000..505564e41
--- /dev/null
+++ b/src/superclaude/cli/observe/terminal.py
@@ -0,0 +1,196 @@
+"""Terminal policy: the one module that owns colour, ASCII mode, width classes, truncation
+and every ``Console`` the observer builds (AD-13, CD-4, CD-5, CD-8).
+
+No other module in this package constructs a ``Console`` or reads the colour switch,
+the column count or the stream encoding.
+"""
+
+from __future__ import annotations
+
+import codecs
+import locale
+import shutil
+import sys
+from collections.abc import Mapping
+from dataclasses import dataclass
+from typing import IO
+
+from rich import box
+from rich.cells import cell_len
+from rich.console import Console
+from rich.style import Style
+
+MIN_WIDTH = 80  # below this every view shows "terminal too narrow (min 80)"
+MIN_ROWS = 8  # PROPOSED (CD-4): two header lines, COUNTS strip, gap notice, one ledger row, footer
+FULL_WIDTH = 160  # 160 and wider: full table
+LINE_WIDTH = 116  # 116 to 159: line form; 80 to 115: short form
+
+TOO_NARROW_TEXT = "terminal too narrow (min 80)"
+
+# Glyph table: name -> (unicode form, ASCII form). Everything else non-ASCII maps to "?".
+GLYPHS: dict[str, tuple[str, str]] = {
+    "sep": ("·", "."),
+    "selected": ("▸", "@"),
+    "truncate": (">", ">"),
+    "hrule": ("─", "-"),
+    "vrule": ("│", "|"),
+    "cross": ("┼", "+"),
+}
+
+# Palette table (CD-8): empty, so every style is plain text and meaning lives in words.
+PALETTE: dict[str, str] = {}
+
+# Style attributes the observer never uses; the background is never painted either.
+_FORBIDDEN_ATTRS = (
+    "blink",
+    "blink2",
+    "dim",
+    "italic",
+    "underline",
+    "underline2",
+    "conceal",
+)
+
+
+@dataclass(frozen=True)
+class TerminalPolicy:
+    width: int
+    height: int
+    no_color: bool
+    ascii: bool
+    width_class: str  # "full" | "line" | "short" | "narrow"
+
+    @property
+    def too_narrow(self) -> bool:
+        return self.width_class == "narrow"
+
+    @property
+    def too_small(self) -> bool:
+        return self.height < MIN_ROWS
+
+    @property
+    def box_style(self) -> box.Box:
+        return box.ASCII if self.ascii else box.SQUARE
+
+
+def _is_utf8(encoding: str | None) -> bool:
+    if not encoding:
+        return False
+    try:
+        return codecs.lookup(encoding).name == "utf-8"
+    except LookupError:
+        return False
+
+
+def width_class(width: int) -> str:
+    if width >= FULL_WIDTH:
+        return "full"
+    if width >= LINE_WIDTH:
+        return "line"
+    if width >= MIN_WIDTH:
+        return "short"
+    return "narrow"
+
+
+def resolve_policy(
+    env: Mapping[str, str],
+    encoding: str | None,
+    flags: Mapping[str, bool] | None,
+    width: int,
+    height: int,
+) -> TerminalPolicy:
+    """Decide colour, ASCII mode and width class once, from explicit inputs."""
+    flags = flags or {}
+    # NO_COLOR counts when set and non-empty ("1" and "yes" alike).
+    no_color = bool(env.get("NO_COLOR"))
+    # ASCII with --ascii; turning it on for a non-UTF-8 output encoding is PROPOSED.
+    use_ascii = bool(flags.get("ascii")) or not _is_utf8(encoding)
+    return TerminalPolicy(
+        width=width,
+        height=height,
+        no_color=no_color,
+        ascii=use_ascii,
+        width_class=width_class(width),
+    )
+
+
+def output_encoding() -> str:
+    """The encoding of standard output, falling back to the locale's."""
+    return (
+        getattr(sys.stdout, "encoding", None)
+        or locale.getpreferredencoding(False)
+        or "utf-8"
+    )
+
+
+def detect_size() -> tuple[int, int]:
+    """Current terminal size as (columns, rows); (80, 24) when it cannot be read."""
+    size = shutil.get_terminal_size(fallback=(80, 24))
+    return size.columns, size.lines
+
+
+def make_console(
+    policy: TerminalPolicy, file: IO[str] | None = None, record: bool = False
+) -> Console:
+    """The only place a ``Console`` is built: explicit width, no highlighting, no markup."""
+    return Console(
+        file=file,
+        width=policy.width,
+        height=policy.height,
+        highlight=False,
+        markup=False,
+        emoji=False,
+        color_system=None if policy.no_color else "standard",
+        no_color=policy.no_color,
+        safe_box=policy.ascii,
+        record=record,
+    )
+
+
+def glyph(name: str, policy: TerminalPolicy) -> str:
+    unicode_form, ascii_form = GLYPHS[name]
+    return ascii_form if policy.ascii else unicode_form
+
+
+def ascii_safe(text: str) -> str:
+    """Map every non-ASCII character to ``?`` (PROPOSED rule for ASCII mode)."""
+    return text.encode("ascii", errors="replace").decode("ascii")
+
+
+def palette_style(name: str) -> Style:
+    """A palette entry as a ``Style``; refuses blink, faint, italic, underline and backgrounds."""
+    spec = PALETTE.get(name, "")
+    style = Style.parse(spec) if spec else Style.null()
+    for attr in _FORBIDDEN_ATTRS:
+        if getattr(style, attr):
+            raise ValueError(
+                f"palette style {name!r} uses forbidden attribute {attr!r}"
+            )
+    if style.bgcolor is not None:
+        raise ValueError(f"palette style {name!r} paints a background")
+    return style
+
+
+def clip(text: str, width: int, policy: TerminalPolicy) -> str:
+    """The single truncation helper: fits ``text`` in ``width`` terminal cells.
+
+    Measures with ``cell_len`` (never ``len``), never splits a double-width character, and
+    marks a cut with one ``>`` that fits inside the width.
+    """
+    if policy.ascii:
+        text = ascii_safe(text)
+    if width <= 0:
+        return ""
+    if cell_len(text) <= width:
+        return text
+    marker = glyph("truncate", policy)
+    room = width - cell_len(marker)
+    kept: list[str] = []
+    used = 0
+    for ch in text:
+        step = cell_len(ch)
+        if used + step > room:
+            break
+        kept.append(ch)
+        used += step
+    return "".join(kept) + marker
diff --git a/tests/observe/test_terminal.py b/tests/observe/test_terminal.py
new file mode 100644
index 000000000..dcfd56f08
--- /dev/null
+++ b/tests/observe/test_terminal.py
@@ -0,0 +1,231 @@
+"""Terminal policy tests (AD-13; T26, T28, T30 helper part in acceptance-tests.md)."""
+
+from __future__ import annotations
+
+import io
+import re
+from pathlib import Path
+
+import pytest
+from rich import box
+from rich.cells import cell_len
+from rich.text import Text
+
+import superclaude.cli.observe as observe_pkg
+from superclaude.cli.observe import terminal
+from superclaude.cli.observe.terminal import (
+    MIN_ROWS,
+    clip,
+    make_console,
+    palette_style,
+    resolve_policy,
+)
+
+SGR = re.compile(r"\x1b\[([0-9;]*)m")
+
+
+def policy(env=None, encoding="utf-8", flags=None, width=160, height=40):
+    return resolve_policy(env or {}, encoding, flags, width, height)
+
+
+def render(pol, style, text="hello"):
+    """What the console writes to its stream (not export_text, which always styles)."""
+    buffer = io.StringIO()
+    console = make_console(pol, file=buffer, record=True)
+    console.print(Text(text, style=style))
+    return buffer.getvalue()
+
+
+# -- T26: NO_COLOR -----------------------------------------------------------
+
+
+@pytest.mark.parametrize("value", ["1", "yes"])
+def test_no_color_set_and_non_empty_gives_no_sgr_codes(value):
+    pol = policy({"NO_COLOR": value})
+    assert pol.no_color is True
+    assert "\x1b" not in render(pol, "red")
+
+
+@pytest.mark.parametrize("env", [{}, {"NO_COLOR": ""}])
+def test_no_color_unset_or_empty_keeps_colour_available(env):
+    pol = policy(env)
+    assert pol.no_color is False
+    assert "31" in [p for m in SGR.findall(render(pol, "red")) for p in m.split(";")]
+
+
+def test_colour_only_where_the_palette_sets_it():
+    assert terminal.PALETTE == {}  # CD-8: empty palette, plain text
+    assert not palette_style("anything")  # a null style
+    assert "\x1b" not in render(policy(), palette_style("anything"))
+
+
+# -- T28: no blink, faint, italic, underline ------------------------------------
+
+
+@pytest.mark.parametrize("env", [{}, {"NO_COLOR": "1"}])
+def test_no_blink_code_in_any_console_output(env):
+    for style in ("bold", "red", "green on black", "reverse"):
+        out = render(policy(env), style)
+        params = [p for m in SGR.findall(out) for p in m.split(";")]
+        assert "5" not in params and "6" not in params
+
+
+@pytest.mark.parametrize("spec", ["blink", "dim", "italic", "underline", "on red"])
+def test_palette_refuses_forbidden_styles(monkeypatch, spec):
+    monkeypatch.setitem(terminal.PALETTE, "bad", spec)
+    with pytest.raises(ValueError):
+        palette_style("bad")
+
+
+def test_palette_accepts_plain_colour_and_bold(monkeypatch):
+    monkeypatch.setitem(terminal.PALETTE, "ok", "bold red")
+    assert palette_style("ok").bold
+
+
+# -- width classes, height, ASCII -----------------------------------------------
+
+
+@pytest.mark.parametrize(
+    ("width", "expected"),
+    [
+        (79, "narrow"),
+        (80, "short"),
+        (115, "short"),
+        (116, "line"),
+        (159, "line"),
+        (160, "full"),
+        (200, "full"),
+    ],
+)
+def test_width_classes(width, expected):
+    pol = policy(width=width)
+    assert pol.width_class == expected
+    assert pol.too_narrow is (expected == "narrow")
+
+
+def test_too_small_below_min_rows():
+    assert policy(height=MIN_ROWS - 1).too_small is True
+    assert policy(height=MIN_ROWS).too_small is False
+
+
+@pytest.mark.parametrize(
+    ("encoding", "flags", "expected"),
+    [
+        ("utf-8", None, False),
+        ("UTF-8", {}, False),
+        ("utf8", {}, False),
+        ("ascii", {}, True),
+        ("latin-1", {}, True),
+        (None, {}, True),
+        ("utf-8", {"ascii": True}, True),
+    ],
+)
+def test_ascii_mode_from_flag_or_non_utf8_encoding(encoding, flags, expected):
+    pol = policy(encoding=encoding, flags=flags)
+    assert pol.ascii is expected
+    assert pol.box_style is (box.ASCII if expected else box.SQUARE)
+
+
+def test_glyph_table_maps_to_ascii():
+    ascii_pol = policy(flags={"ascii": True})
+    utf_pol = policy()
+    assert terminal.glyph("sep", utf_pol) == "·"
+    assert terminal.glyph("sep", ascii_pol) == "."
+    assert terminal.glyph("selected", ascii_pol) == "@"
+    assert all(terminal.glyph(name, ascii_pol).isascii() for name in terminal.GLYPHS)
+
+
+def test_console_is_built_with_explicit_width_and_literal_text():
+    pol = policy(width=120, height=30)
+    console = make_console(pol, file=io.StringIO(), record=True)
+    assert console.width == 120
+    assert console.safe_box is False
+    console.print("[bold]x[/bold] 123 http://a.example :smile:")
+    out = console.export_text(styles=True)
+    assert "[bold]x[/bold] 123 http://a.example :smile:" in out
+    assert "\x1b" not in out  # no highlighting of numbers or links, no emoji or markup
+    assert (
+        make_console(policy(flags={"ascii": True}), file=io.StringIO()).safe_box is True
+    )
+
+
+def test_output_encoding_and_size_helpers_return_usable_values():
+    assert isinstance(terminal.output_encoding(), str) and terminal.output_encoding()
+    columns, rows = terminal.detect_size()
+    assert columns > 0 and rows > 0
+
+
+# -- T30: clip -------------------------------------------------------------------
+
+SAMPLES = [
+    "日本語のテキストです" * 3,
+    "🚀🚀🚀🚀" * 5,
+    "abc日本def",
+    "x" * 100,
+    "mixed 中文 and 🚀 text",
+]
+
+
+@pytest.mark.parametrize("text", SAMPLES)
+def test_clip_never_overflows_never_splits_and_marks_a_cut(text):
+    pol = policy()
+    for width in range(1, 41):
+        out = clip(text, width, pol)
+        assert cell_len(out) <= width
+        if cell_len(text) <= width:
+            assert out == text
+        else:
+            assert out.endswith(">")
+            kept = out[:-1]
+            assert text.startswith(
+                kept
+            )  # whole characters only, a prefix of the original
+            assert cell_len(kept) <= width - 1
+
+
+def test_clip_does_not_leave_half_a_double_width_character():
+    pol = policy()
+    assert clip("日本語", 4, pol) == "日>"
+    assert clip("日本語", 3, pol) == "日>"
+    assert clip("日本語", 2, pol) == ">"
+    assert clip("日本語", 1, pol) == ">"
+    assert clip("日本語", 6, pol) == "日本語"
+
+
+def test_clip_edge_widths():
+    pol = policy()
+    assert clip("abc", 0, pol) == ""
+    assert clip("abc", -3, pol) == ""
+    assert clip("", 5, pol) == ""
+
+
+def test_clip_in_ascii_mode_gives_pure_ascii():
+    pol = policy(flags={"ascii": True})
+    for width in range(1, 41):
+        assert clip("x" * 100, width, pol).isascii()
+        assert clip("日本語 and 🚀", width, pol).isascii()
+        assert cell_len(clip("日本語 and 🚀", width, pol)) <= width
+    assert clip("x" * 100, 10, pol) == "x" * 9 + ">"
+
+
+# -- no other module owns terminal facts ------------------------------------------
+
+
+def test_only_terminal_py_builds_consoles_or_reads_terminal_facts():
+    package_dir = Path(observe_pkg.__file__).parent
+    patterns = [
+        r"\bConsole\(",
+        r"NO_COLOR",
+        r"COLUMNS",
+        r"stdout\.encoding",
+        r"getpreferredencoding",
+    ]
+    offenders = []
+    for path in sorted(package_dir.glob("*.py")):
+        if path.name == "terminal.py":
+            continue
+        text = path.read_text(encoding="utf-8")
+        for pattern in patterns:
+            if re.search(pattern, text):
+                offenders.append(f"{path.name}: {pattern}")
+    assert offenders == []

Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
