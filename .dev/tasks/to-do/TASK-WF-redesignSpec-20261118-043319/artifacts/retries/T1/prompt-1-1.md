75384655d5bf9a0274bfbbb2be4d41f963cc0a9f
Review one task for spec compliance.

Task brief: ## Task 1: Rebuild the baseline capture script and add the render-compare harness

Spec Part B steps 0.1, 0.2 and 0.3. Create `.dev/issues/409/visual-parity/inputs/tools/render_current.py` (the spec's step 0.1 assumes it exists; it does not on this branch). It builds the ledger, questions, desk and desk-planask views from the observer's own fixtures (`OBS/fixtures/`) and view builders and writes plain captures, wrapped in `if __name__ == "__main__":` so it is importable. Then create `.dev/issues/409/visual-parity/tools/render_compare.py` that loads `render_current.py` by path, exposes `render_case(view, width, height, *, env, ascii, depth="16") -> CaseOutput` (fields `plain`, `stream`, `html`) built on `resolve_policy`, `make_console(policy, file=io.StringIO(), record=True)`, `render` and `console.file.getvalue()` (never `export_text(styles=True)`), and implements the full CLI contract of step 0.3: screens `ledger`, `questions`, `desk`, `desk-planask`; widths 160, 116, 80 at heights 48, 42, 42; five passes (truecolor, 256, 16-colour, NO_COLOR, ASCII); the output file names and `manifest.json` per width; `--depth`, `--heights` and `--check` flags; `--check` writes `checks.json` with the script-checked rows listed in step 0.3 (RB-01(a), RB-04, RB-05 to RB-10, RB-13, RB-14, RB-16, RB-17, RB-19 to RB-22 for the parts marked Script). Before Phase 2 lands `TerminalPolicy.color_system`, the harness produces only the 16-colour depth and marks the other two `not-available-before-P1` in `manifest.json`. The desk-planask view uses the synthetic plan-ask built in Task 3 (import it from the tests helper or duplicate the constant with a comment naming its twin).

Acceptance criteria:
- `uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out ./artifacts/gates/p0/iter-1 --check --heights 44,40,24,12,8` exits 0 and writes, for every screen and width, the `.txt`, `.nocolor.txt`, `.ascii.txt`, `.ascii.ansi`, `.16.ansi` and `.16.html` files plus `manifest.json` and `checks.json`.
- The `.nocolor.txt` file contains no ESC byte and the `.ascii.txt` file passes `str.isascii()`, as `checks.json` records.
- The observer package is unchanged: `git diff --stat -- src/` is empty.
Global constraints: - Numbering: plan Phase N is spec Phase N-1 (plan Phase 1 is the spec's Phase 0, plan Phase 8 is the spec's Phase 7). Task text names the plan phase unless it says "spec Phase".
- Shorthand used in every task: OBS is `src/superclaude/cli/observe/`; T is `tests/observe/`; VP is `.dev/issues/409/visual-parity/`; RR is `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`; "the spec" is `./source.md` (its section numbers, Part B step numbers such as 1.4 and Part C step numbers such as 2.12 are cited in each task).
- Do not edit `OBS/export.py`. `record_text` and `snapshot_json` stay byte-identical. Question text appears on screen only; both hash canaries (record and snapshot) pass from Phase 1 onward.
- NO_COLOR output has zero ESC bytes and the same text as the coloured output after SGR removal. ASCII output is pure ASCII with `+ - |` borders and `#` for the block glyph. The 16-colour theme keeps eight distinct role colours.
- Draw only facts the screen has: no owner, requester, mapped-tree, SIGNALS bars or affected-session list (accepted divergences AD-1 to AD-8 of the spec).
- Existing source guards stay true: `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED` (`OBS/commands.py` lines 67 and 70) untouched, the words `release-gates.md` and `Task 18` stay in `OBS/commands.py`, no `Console(`, `from_markup`, `sorted(`, `.sort(` or adapter, collector, parse import in `OBS/render.py`, and `len(group.renderables) == len(screen_lines(...))` holds.
- Owner rulings already applied (spec section 10 and Part C): Decision Desk in two columns at 160 and 116 and stacked at 80; questions screen stacked at every width; the 64-hex hash is never shown on screen; the other defaults of spec section 10 apply (D-2 to D-5, D-7 to D-12). OPEN-1 to OPEN-3 are treated as Medium and gating.
- Phase gate rule (spec section 8): each phase ends with the render gate, at most 3 iterations, a fresh reviewer per width each iteration. A phase closes only when every in-scope High and Medium rubric row passes in the last iteration. If a row still fails after iteration 3, or two consecutive iterations do not improve the passing count, write `./.dev/issues/409/visual-parity/scores/<phase>/stop.md` (path relative to the repository root), stop, and ask the owner. Never start the next phase before the previous gate closes.
- Gate outputs (renders, captures, scores) are written under `./artifacts/gates/<phase>/iter-<n>/` in this package; the closing record `scores.json` of the last iteration is also copied to `.dev/issues/409/visual-parity/scores/<phase>/` because the spec's definition of done reads it there.
- The spec's Phase 0 inputs (`render_current.py` and the baseline captures) exist only untracked in a local checkout that must never be edited. They are not on this branch, so Phase 1 rebuilds `render_current.py` from the observer's own view builders and fixtures. Never edit the local checkout.
- Goldens are regenerated only from the current tree, in the same change set as the change that moves them; styled bytes are never written into a golden.
- Nothing under `.claude/` is staged. This plan does not commit, push or open a PR before a human asks; the final task states the PR route for that moment (`/sc:pr-submit --monitor 3`, target `IronbellyOrg/IronClaude`, never `SuperClaude-Org`).
- Judgment call recorded here: spec step 2.13 names `_field_lines`, a function that step 5.2 only creates in the desk phase (spec Phase 5, plan Phase 6). The space-diet work (spec Phase 2, plan Phase 3) therefore applies the label, alignment and badge changes to the existing desk field loop in `OBS/render.py` (lines 347-353 today), and plan Phase 6 replaces that loop with `_field_lines` while keeping those changes.
Start sha: 75384655d5bf9a0274bfbbb2be4d41f963cc0a9f
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b: ran on the Grep floor; the task adds two new files under .dev/issues/409/visual-parity/ and changes no existing symbol, so there are no dependents outside the diff.

Touched files (both new, untracked, shown as full-file diffs): .dev/issues/409/visual-parity/inputs/tools/render_current.py and .dev/issues/409/visual-parity/tools/render_compare.py. Task-run evidence (the harness run the AC asks for, command and output) is in the package folder ./artifacts/gates/p0/iter-1/ (checks.json, manifest.json, per-width files); for this review that folder is at /home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/tasks/to-do/TASK-WF-redesignSpec-20261118-043319/artifacts/gates/p0/iter-1/ and you may Read it. git diff --stat -- src/ is empty.

diff --git a/.dev/issues/409/visual-parity/inputs/tools/render_current.py b/.dev/issues/409/visual-parity/inputs/tools/render_current.py
new file mode 100644
index 000000000..2f3a37895
--- /dev/null
+++ b/.dev/issues/409/visual-parity/inputs/tools/render_current.py
@@ -0,0 +1,125 @@
+"""Render the observer's four reference screens from its own fixtures (baseline capture script).
+
+Rebuilt for issue #606 (the original lived only in an untracked local checkout). It builds the
+four views the render gate compares with the design mockups, with the test fake clock and the
+fake runner, so no process is started and every run is repeatable:
+
+- ``ledger``        questions off, the ``base`` fixture (the Signal Bridge pairing)
+- ``questions``     questions on, link off, five questions (the Attention Ledger pairing)
+- ``desk``          questions on, link on, one question selected (the Decision Desk pairing)
+- ``desk-planask``  the same with the plan-approval question ``PLAN_ASK`` (64-hex hash and paths)
+
+A direct run writes the plain (``screen_lines``) captures to ``--out``; the harness
+``render_compare.py`` imports this module and uses ``build_views()`` instead.
+
+Run from the repository root: ``uv run python .dev/issues/409/visual-parity/inputs/tools/render_current.py --out <dir>``.
+"""
+
+from __future__ import annotations
+
+import argparse
+import json
+import sys
+from pathlib import Path
+
+ROOT = Path(__file__).resolve().parents[6]
+if str(ROOT) not in sys.path:
+    sys.path.insert(0, str(ROOT))
+
+from superclaude.cli.observe.adapter import LiveSource  # noqa: E402
+from superclaude.cli.observe.collector import Collector, FixtureSource  # noqa: E402
+from superclaude.cli.observe.render import screen_lines  # noqa: E402
+from superclaude.cli.observe.terminal import resolve_policy  # noqa: E402
+from superclaude.cli.observe.view import Session, build_view  # noqa: E402
+from tests.observe.conftest import (  # noqa: E402
+    QRUN,
+    FakeClock,
+    FakeDiscover,
+    FakeRunner,
+    make_envelope,
+    make_question_envelope,
+    make_question_rows,
+    make_rows,
+    question_payload,
+    routed_runner_responses,
+)
+
+SCREENS = ("ledger", "questions", "desk", "desk-planask")
+WIDTHS = (160, 116, 80)
+# Heights of the three design mockup frames (04 section 4); render_current's old height 50 was not like for like.
+MOCKUP_HEIGHTS = {160: 48, 116: 42, 80: 42}
+HASH = "0123456789abcdef" * 4
+# Twin of PLAN_ASK in tests/observe/test_render.py (R3 block): keep the two identical.
+PLAN_ASK = (
+    "Approve the plan in .dev/plans/observer-visual-parity/plan.md before the worker edits "
+    "src/superclaude/cli/observe/render.py and src/superclaude/cli/observe/terminal.py "
+    f"(plan hash {HASH})?"
+)
+
+
+def _question_view(clock, rows, *, link: bool, selected: int | None):
+    worker = (0, json.dumps(make_envelope(make_rows(3, 1), total=3)))
+    message = (0, json.dumps(make_question_envelope(rows)))
+    runner = FakeRunner([], [routed_runner_responses(worker, message)])
+    result = Collector(
+        LiveSource(runner, FakeDiscover([])),
+        clock,
+        run_id=QRUN,
+        questions=True,
+        link=link,
+    ).run_once()
+    session = Session(
+        selected_question=None if selected is None else (QRUN, f"msg_{selected:012x}")
+    )
+    return build_view(result, session, clock)
+
+
+def _linked_rows(specs):
+    rows = []
+    for index, (dispatch, text) in enumerate(specs):
+        rows += make_question_rows(
+            1, start=index, payload=question_payload(dispatch, text)
+        )
+    return rows
+
+
+def build_views() -> dict:
+    """The four reference views, each built with its own fake clock."""
+    clock = FakeClock()
+    collector = Collector(FixtureSource("base"), clock)
+    collector.run_once()
+    ledger = build_view(collector.run_once(), Session(), clock)
+    questions = _question_view(
+        FakeClock(), make_question_rows(5), link=False, selected=0
+    )
+    desk = _question_view(
+        FakeClock(),
+        _linked_rows([("w-001", "Which branch should the worker rebase on?"), ("w-002", "Ship the change now?")]),
+        link=True,
+        selected=1,
+    )
+    plan = _question_view(
+        FakeClock(),
+        _linked_rows([("w-001", "Which branch should the worker rebase on?"), ("w-002", PLAN_ASK)]),
+        link=True,
+        selected=1,
+    )
+    return {"ledger": ledger, "questions": questions, "desk": desk, "desk-planask": plan}
+
+
+def main() -> None:
+    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
+    parser.add_argument("--out", required=True, help="directory for the plain captures")
+    args = parser.parse_args()
+    out = Path(args.out)
+    views = build_views()
+    for width in WIDTHS:
+        (out / str(width)).mkdir(parents=True, exist_ok=True)
+        policy = resolve_policy({}, "utf-8", {"ascii": False}, width, MOCKUP_HEIGHTS[width])
+        for name in SCREENS:
+            text = "\n".join(screen_lines(views[name], policy)) + "\n"
+            (out / str(width) / f"{name}.txt").write_text(text, encoding="utf-8")
+
+
+if __name__ == "__main__":
+    main()
diff --git a/.dev/issues/409/visual-parity/tools/render_compare.py b/.dev/issues/409/visual-parity/tools/render_compare.py
new file mode 100644
index 000000000..24fcf0f47
--- /dev/null
+++ b/.dev/issues/409/visual-parity/tools/render_compare.py
@@ -0,0 +1,389 @@
+"""Render-compare harness for the observer visual-parity gate (issue #606, spec section 8 and step 0.3).
+
+Command::
+
+    uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out <dir> \
+        [--depth 16,256,truecolor] [--heights 44,40,24,12,8] [--check]
+
+For the screens ``ledger``, ``questions``, ``desk`` and ``desk-planask`` (views from
+``inputs/tools/render_current.py``) at widths 160, 116 and 80 (heights 48, 42, 42) it writes, per
+width into ``<out>/<width>/``:
+
+    <screen>.txt                 plain ``screen_lines``
+    <screen>.<depth>.ansi/.html  the coloured stream and ``export_html`` for each selected depth
+    <screen>.nocolor.txt         env NO_COLOR=1
+    <screen>.ascii.txt           ``--ascii`` plain, and <screen>.ascii.ansi (16-colour stream)
+    <screen>.h<height>.txt       with --heights: a text-only height matrix
+    manifest.json                line counts, widest cell, and which depths were really produced
+
+``--check`` also writes ``<out>/checks.json``: one entry per script-checked rubric row, each
+``{"status": "pass"|"fail"|"na", "evidence": [...]}``. A run without ``--check`` or without all
+five passes is not a valid gate run.
+
+The capture is ``console.file.getvalue()`` of a recording console; ``export_text(styles=True)``
+is never used (it ignores NO_COLOR and the colour downgrade).
+"""
+
+from __future__ import annotations
+
+import argparse
+import dataclasses
+import importlib.util
+import io
+import json
+import re
+import sys
+from dataclasses import dataclass
+from pathlib import Path
+
+HERE = Path(__file__).resolve().parent
+VP = HERE.parent
+ROOT = VP.parents[3]
+if str(ROOT) not in sys.path:
+    sys.path.insert(0, str(ROOT))
+
+
+def _load_current():
+    spec = importlib.util.spec_from_file_location(
+        "render_current", VP / "inputs" / "tools" / "render_current.py"
+    )
+    module = importlib.util.module_from_spec(spec)
+    spec.loader.exec_module(module)
+    return module
+
+
+current = _load_current()
+
+from rich.cells import cell_len  # noqa: E402
+
+from superclaude.cli.observe.render import render, screen_lines  # noqa: E402
+from superclaude.cli.observe.terminal import make_console, resolve_policy  # noqa: E402
+from superclaude.cli.observe import view as observe_view  # noqa: E402
+
+SCREENS = current.SCREENS
+WIDTHS = current.WIDTHS
+HEIGHTS = current.MOCKUP_HEIGHTS
+RICH_DEPTH = {"16": "standard", "256": "256", "truecolor": "truecolor"}
+SGR = re.compile(r"\x1b\[[0-9;]*m")
+ANSI_ANY = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
+# The eight mockup palette triples (spec RB-01, 04 section 2).
+PALETTE = {
+    (225, 233, 238): "base",
+    (165, 182, 194): "muted",
+    (82, 108, 128): "slate",
+    (250, 178, 25): "amber",
+    (112, 205, 226): "cyan",
+    (139, 215, 175): "green",
+    (240, 141, 150): "red",
+    (194, 173, 242): "violet",
+}
+HEX_RUN = re.compile(r"[0-9a-fA-F]{32,}")
+
+
+def strip_sgr(text: str) -> str:
+    return SGR.sub("", text)
+
+
+@dataclass
+class CaseOutput:
+    plain: list[str]
+    stream: str
+    html: str
+    produced_depth: str  # the depth really rendered ("n/a" when the policy cannot carry it yet)
+
+
+def _policy(width: int, height: int, *, env: dict, ascii: bool):
+    return resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)
+
+
+def render_case(view, width: int, height: int, *, env: dict, ascii: bool, depth: str = "16") -> CaseOutput:
+    """One render: the plain lines, the written stream (SGR included) and the recorded HTML."""
+    policy = _policy(width, height, env=env, ascii=ascii)
+    produced = depth
+    if hasattr(policy, "color_system"):
+        if policy.color_system is not None:
+            policy = dataclasses.replace(policy, color_system=RICH_DEPTH[depth])
+    elif depth != "16":
+        produced = "not-available-before-P1"  # make_console pins "standard" until step 1.1
+    console = make_console(policy, file=io.StringIO(), record=True)
+    console.print(render(view, policy))
+    return CaseOutput(
+        plain=screen_lines(view, policy),
+        stream=console.file.getvalue(),
+        html=console.export_html(inline_styles=True),
+        produced_depth=produced,
+    )
+
+
+def _write(path: Path, text: str) -> None:
+    path.parent.mkdir(parents=True, exist_ok=True)
+    path.write_text(text, encoding="utf-8")
+
+
+# -- checks ---------------------------------------------------------------------------------
+
+
+def _row(status: str, *evidence: str) -> dict:
+    return {"status": status, "evidence": [e for e in evidence if e]}
+
+
+def _flat(lines) -> str:
+    return " ".join(" ".join(lines).split())
+
+
+def _unframe(line: str) -> str:
+    """Strip a one-cell margin and a rounded, heavy or ASCII border pair when present."""
+    text = re.sub(r"^\s?[│┃|]\s", "", line)
+    return re.sub(r"\s[│┃|]\s?$", "", text) if text != line else line
+
+
+def _required_literals(name: str, view) -> list[str]:
+    out: list[str] = []
+    panel = view.questions
+    if panel is None:
+        out.append(view.gap_notice)
+    else:
+        out += [panel.disclosure, panel.caveat_line, panel.retention_line, panel.counts_line]
+        if name in ("desk", "desk-planask"):
+            out.append(observe_view.DESK_TITLE)
+    return [x for x in out if x]
+
+
+def check_screen(name: str, view, width: int, height: int, outs: dict, nocolor: CaseOutput, ascii_out: CaseOutput):
+    """Per-screen rows; returns {row: {status, evidence}} for one width."""
+    rows: dict[str, dict] = {}
+    plain = outs["plain"]
+    flat = _flat(plain)
+
+    # RB-05 required literals, whole and uncut (whitespace-collapsed, so wrapping is allowed).
+    missing = [lit for lit in _required_literals(name, view) if _flat([lit]) not in flat]
+    rows["RB-05"] = _row("fail", *[f"missing or cut: {m[:70]}" for m in missing]) if missing else _row("pass")
+
+    # RB-06 NO_COLOR: no ESC, same text as the coloured pass after SGR removal.
+    esc = "\x1b" in nocolor.stream
+    coloured = [ln.rstrip() for ln in strip_sgr(outs["stream"]).split("\n")]
+    plain_lines = [ln.rstrip() for ln in plain]
+    same = [ln for ln in coloured if ln] == [ln for ln in plain_lines if ln]
+    rows["RB-06"] = (
+        _row("fail", "ESC byte in NO_COLOR stream" if esc else "", "" if same else "SGR-stripped text differs from plain")
+        if esc or not same
+        else _row("pass")
+    )
+
+    # RB-07 ASCII: pure ASCII; a framed pane uses + - |, never ?
+    bad: list[str] = []
+    if not all(ln.isascii() for ln in ascii_out.plain) or not ascii_out.stream.isascii():
+        bad.append("non-ASCII in ASCII pass")
+    borders = [ln for ln in ascii_out.plain if ln.lstrip().startswith("+")]
+    bad += [f"? inside a border: {ln[:60]}" for ln in borders if "?" in ln]
+    rows["RB-07"] = _row("fail", *bad) if bad else (_row("pass") if borders else _row("pass", "no frame yet; text part only"))
+
+    # RB-08 fit: width, height, footer last, no blink, no mouse sequences.
+    problems: list[str] = []
+    for ln in plain:
+        if cell_len(ln) > width:
+            problems.append(f"line wider than {width}: {ln[:50]}")
+    if len(plain) > height:
+        problems.append(f"{len(plain)} rows > height {height}")
+    if not any("q quit" in ln for ln in plain[-4:]):
+        problems.append("footer keys are not among the last lines")
+    for label, text in (("stream", outs["stream"]), ("nocolor", nocolor.stream)):
+        if re.search(r"\x1b\[(?:[0-9;]*;)?[56](?:;[0-9;]*)?m", text):
+            problems.append(f"SGR 5 or 6 (blink) in {label}")
+        if re.search(r"\x1b\[\?100[0236]h", text):
+            problems.append(f"mouse sequence in {label}")
+    rows["RB-08"] = _row("fail", *problems) if problems else _row("pass")
+
+    # RB-13 the key list is whole: every two-space group sits whole on one line; none cut by ' >'.
+    help_line = getattr(view, "help_line", "")
+    groups = [g for g in re.split(r"\s{2,}", help_line.strip()) if g]
+    cut = [g for g in groups if not any(g in ln for ln in plain)]
+    rows["RB-13"] = _row("fail", *[f"key group not whole: {g}" for g in cut]) if cut else _row("pass")
+
+    # RB-20 a rule line precedes the footer keys; the key pair n/p question is intact when linked.
+    first_help = next((i for i, ln in enumerate(plain) if groups and groups[0] in ln), None)
+    rule_ok = first_help is not None and first_help > 0 and bool(re.fullmatch(r"[─-]{10,}", plain[first_help - 1].strip()))
+    pair_ok = "n/p question" not in help_line or any("n/p question" in ln for ln in plain)
+    rows["RB-20"] = _row("pass") if rule_ok and pair_ok else _row("fail", "" if rule_ok else "no rule line above the footer", "" if pair_ok else "n/p question split")
+
+    # RB-21 counts lines are not cut inside a token: a trailing ' >' must follow a space.
+    cut_counts = [ln for ln in plain[:6] if ln.endswith(">") and len(ln) > 1 and ln[-2] != " "]
+    rows["RB-21"] = _row("fail", *[f"cut inside a token: {ln[-30:]}" for ln in cut_counts]) if cut_counts else _row("pass")
+
+    # RB-19 Q7 (desk-planask): the hash is whole on one line and the screen fits.
+    if name == "desk-planask":
+        hash_lines = [ln for ln in plain if current.HASH in _unframe(ln)]
+        rows["RB-19"] = _row("pass") if hash_lines else _row("fail", "64-hex hash not whole on one line (cut, wrapped or hidden)")
+    # RB-27 no run of 32 hex characters on the questions screen or the desk.
+    if name != "ledger":
+        runs = [ln for ln in plain if HEX_RUN.search(ln)]
+        rows["RB-27"] = _row("fail", *[f"hex run shown: {ln.strip()[:70]}" for ln in runs[:2]]) if runs else _row("pass")
+
+    # RB-14 desk (a), (c), (d) on the plain pass.
+    if name in ("desk", "desk-planask"):
+        body = [_unframe(ln) for ln in plain]
+        try:
+            start = next(i for i, ln in enumerate(body) if observe_view.DESK_TITLE in ln)
+            first = body[start + 1]
+            fields = [(i, ln) for i, ln in enumerate(body[start + 1 :], start + 1) if re.match(r"^[\w.]+:\s", ln)]
+            a_ok = bool(re.match(r"^\S+\s+age\s", first)) and (not fields or all(i > start + 1 for i, _ in fields))
+            offsets = {re.match(r"^([\w.]+:\s*)", ln).end() for _, ln in fields if re.match(r"^[\w.]+:\s+\S", ln)}
+            c_ok = len(offsets) <= 1
+            d_ok = all(cell_len(ln) <= width for ln in plain)
+            parts = [] if a_ok else ["question text does not lead (qid age, then text, then fields)"]
+            parts += [] if c_ok else [f"field values start at {len(offsets)} different offsets"]
+            parts += [] if d_ok else ["a line exceeds the width"]
+            rows["RB-14"] = _row("fail", *parts) if parts else _row("pass")
+        except (StopIteration, IndexError):
+            rows["RB-14"] = _row("fail", "desk not found on screen")
+
+    # RB-17 census (b)/(c): run, caveat and retention lines occur exactly once each.
+    if view.questions is not None:
+        census = {lit: flat.count(_flat([lit])) for lit in (view.questions.run_line, view.questions.caveat_line, view.questions.retention_line) if lit}
+        wrong = [f"{k[:40]}: {n} times" for k, n in census.items() if n != 1]
+        rows["RB-17"] = _row("fail", *wrong) if wrong else _row("pass", "census only; pane frame checked after phase 4")
+
+    # RB-04 (c), (d): the counts line is whole on one line with the figure.
+    if view.questions is not None:
+        whole = any(_flat([view.questions.counts_line]) in _flat([ln]) for ln in plain)
+        rows["RB-04"] = _row("pass") if whole else _row("fail", "counts line not whole on one line")
+
+    # RB-01 (a): every foreground colour of the truecolor stream is one of the eight triples.
+    return rows
+
+
+def role_census_truecolor(stream: str) -> dict:
+    colours = set()
+    for m in re.finditer(r"\x1b\[([0-9;]*)m", stream):
+        parts = [int(p) for p in m.group(1).split(";") if p.isdigit()]
+        i = 0
+        while i < len(parts):
+            if parts[i] == 38 and parts[i + 1 : i + 2] == [2] and len(parts) >= i + 5:
+                colours.add(tuple(parts[i + 2 : i + 5]))
+                i += 5
+            elif parts[i] == 38 and parts[i + 1 : i + 2] == [5]:
+                colours.add(("idx", parts[i + 2]) if i + 2 < len(parts) else ("idx", -1))
+                i += 3
+            else:
+                if 30 <= parts[i] <= 37 or 90 <= parts[i] <= 97:
+                    colours.add(("ansi", parts[i]))
+                i += 1
+    return {c for c in colours}
+
+
+def theme_rows() -> dict:
+    """RB-09 and RB-10(d) read the theme module when it exists (phase 2 onward)."""
+    try:
+        from superclaude.cli.observe import theme  # type: ignore
+    except ImportError:
+        return {
+            "RB-09": _row("na", "theme.py not built yet (plan Phase 2)"),
+            "RB-10": _row("na", "theme.py not built yet (plan Phase 2)"),
+        }
+    palette_roles = ("attention", "identity", "secondary", "muted", "state_running", "state_settled", "state_failed", "state_frozen")
+    codes = {}
+    for role in palette_roles:
+        style = theme.style_for(role, "standard")
+        codes[role] = None if style is None else style.color.number if style.color is not None else None
+    distinct = len({v for v in codes.values() if v is not None}) == len([v for v in codes.values() if v is not None]) and len(set(codes.values())) == len(codes)
+    rb09 = _row("pass") if distinct else _row("fail", f"16-colour role codes collide: {codes}")
+    keys = [("workerState", "running"), ("workerState", "succeeded"), ("workerState", "failed"), ("dispatchStatus", "completed"), ("liveness", "alive")]
+    state = getattr(theme, "STATE_ROLE", {})
+    missing = [k for k in keys if k not in state]
+    frozen_ok = getattr(theme, "FROZEN_ROLE", None) == "state_frozen"
+    rb10 = _row("pass", "(d) table keys only; (a)(b) census is added with the phase 2 gate") if not missing and frozen_ok else _row("fail", f"STATE_ROLE missing {missing}", "" if frozen_ok else "FROZEN_ROLE != state_frozen")
+    return {"RB-09": rb09, "RB-10": rb10}
+
+
+# -- main -----------------------------------------------------------------------------------
+
+
+def main(argv=None) -> int:
+    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
+    ap.add_argument("--out", required=True)
+    ap.add_argument("--depth", default="16,256,truecolor")
+    ap.add_argument("--heights", default="")
+    ap.add_argument("--check", action="store_true")
+    args = ap.parse_args(argv)
+    out = Path(args.out)
+    depths = [d.strip() for d in args.depth.split(",") if d.strip()]
+    for d in depths:
+        if d not in RICH_DEPTH:
+            ap.error(f"unknown depth {d!r}; use 16, 256 or truecolor")
+    heights = [int(h) for h in args.heights.split(",") if h.strip()]
+    views = current.build_views()
+    checks: dict[str, dict] = {}
+    all_rows: dict[str, list] = {}
+
+    def merge(row_id: str, key: str, row: dict) -> None:
+        all_rows.setdefault(row_id, []).append((key, row))
+
+    for width in WIDTHS:
+        wdir = out / str(width)
+        height = HEIGHTS[width]
+        manifest: dict = {"width": width, "height": height, "screens": {}}
+        for name in SCREENS:
+            view = views[name]
+            base = render_case(view, width, height, env={}, ascii=False, depth="16")
+            nocolor = render_case(view, width, height, env={"NO_COLOR": "1"}, ascii=False)
+            ascii_out = render_case(view, width, height, env={}, ascii=True)
+            _write(wdir / f"{name}.txt", "\n".join(base.plain) + "\n")
+            _write(wdir / f"{name}.nocolor.txt", nocolor.stream)
+            _write(wdir / f"{name}.ascii.txt", "\n".join(ascii_out.plain) + "\n")
+            _write(wdir / f"{name}.ascii.ansi", ascii_out.stream)
+            entry = {"lines": len(base.plain), "widest_cell": max((cell_len(x) for x in base.plain), default=0), "depths": {}}
+            truecolor_stream = ""
+            for depth in depths:
+                case = render_case(view, width, height, env={}, ascii=False, depth=depth)
+                _write(wdir / f"{name}.{depth}.ansi", case.stream)
+                _write(wdir / f"{name}.{depth}.html", case.html)
+                entry["depths"][depth] = case.produced_depth
+                if depth == "truecolor":
+                    truecolor_stream = case.stream
+            for h in heights:
+                _write(wdir / f"{name}.h{h}.txt", "\n".join(render_case(view, width, h, env={}, ascii=False).plain) + "\n")
+            manifest["screens"][name] = entry
+            if args.check:
+                rows = check_screen(name, view, width, height, {"plain": base.plain, "stream": base.stream}, nocolor, ascii_out)
+                for rid, row in rows.items():
+                    merge(rid, f"{name}@{width}", row)
+                if truecolor_stream and entry["depths"].get("truecolor") == "truecolor":
+                    colours = role_census_truecolor(truecolor_stream)
+                    stray = [c for c in colours if c not in PALETTE]
+                    merge("RB-01", f"{name}@{width}", _row("fail", f"foreground colours outside the eight triples: {sorted(map(str, stray))[:4]}") if stray else _row("pass", "census (a) only; (b)-(f) are reviewer rows"))
+                else:
+                    merge("RB-01", f"{name}@{width}", _row("na", "no truecolor stream before plan Phase 2"))
+        _write(wdir / "manifest.json", json.dumps(manifest, indent=1, sort_keys=True))
+
+    if args.check:
+        for rid, row in theme_rows().items():
+            all_rows[rid] = [("theme", row)]
+        for rid in ("RB-16",):
+            all_rows[rid] = [("roles", _row("na", "needs role spans (plan Phase 2 and Phase 5); checked then"))]
+        baseline_md = VP / "scores" / "baseline.md"
+        n_known = baseline_md.exists() and re.search(r"RB-22 threshold N:\s*(\d+)", baseline_md.read_text(encoding="utf-8"))
+        ledger_rows = []
+        for width in (116, 80):
+            lines = (out / str(width) / "ledger.txt").read_text(encoding="utf-8").splitlines()
+            runs = [max((len(m.group(0)) for m in re.finditer(r"(?<=\S) {2,}(?=\S)", ln)), default=0) for ln in lines if re.search(r"w-\d{3}", ln)]
+            ledger_rows.append((width, max(runs, default=0)))
+        if n_known:
+            limit = int(n_known.group(1))
+            bad = [f"{w} cols: blank run {r} > N={limit}" for w, r in ledger_rows if r > limit]
+            all_rows["RB-22"] = [("ledger", _row("fail", *bad) if bad else _row("pass", f"N={limit}"))]
+        else:
+            all_rows["RB-22"] = [("ledger", _row("na", f"threshold N not recorded yet; measured {ledger_rows}"))]
+        for rid, entries in sorted(all_rows.items()):
+            statuses = {row["status"] for _, row in entries}
+            status = "fail" if "fail" in statuses else ("pass" if "pass" in statuses else "na")
+            checks[rid] = {
+                "status": status,
+                "cases": {key: row for key, row in entries if row["status"] != "pass"} or {"all": "pass"},
+            }
+        _write(out / "checks.json", json.dumps(checks, indent=1, sort_keys=True))
+    print(f"render_compare: wrote {out}" + (f" ({len(checks)} rubric rows checked)" if args.check else ""))
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

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
