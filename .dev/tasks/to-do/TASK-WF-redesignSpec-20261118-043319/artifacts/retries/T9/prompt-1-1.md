5870e7076fcd81df4729e00231a8556ee3a5d5c5
Review one task for spec compliance.

Task brief: ## Task 9: Add the live pty test and close the Phase 2 gate

Depends on: Task 7, Task 8

Spec steps 1.6(g) and 1.7. Read `OBS/commands.py` lines 257-279 (`LiveScreen.__init__`, `draw`, `close`) and `tests/observe/spike_child.py:64`. Create `tests/observe/live_child.py` (builds the fixture view and drives the real `LiveScreen` under `pexpect.spawn` with a fixed pty size) and `tests/observe/test_live_screen_pty.py` asserting the stream contains `\x1b[?1049h`, SGR `38;2` when `COLORTERM=truecolor`, only 16-colour codes otherwise, no SGR under `NO_COLOR=1`, no SGR 5 or 6 and none of `\x1b[?1000h`, `?1002h`, `?1003h`, `?1006h`; if Rich emits a bare reset under NO_COLOR, adjust with the measured bytes and note it. Update the harness to produce real 256 and truecolor passes now that the policy carries `color_system`. Run the render gate (spec section 8) into `./artifacts/gates/p1/` with rubric rows RB-01, RB-05 to RB-11 and RB-23 in scope.

Acceptance criteria:
- `uv run pytest tests/observe/ -v` is green including the pty test.
- Gate record `.dev/issues/409/visual-parity/scores/p1/scores.json` shows every in-scope High and Medium row PASS in the last iteration within 3 iterations, or `stop.md` exists and the run has stopped for the owner.
- The 16-colour pass maps the eight roles to eight distinct ANSI colours (RB-09) and the state roles pass the RB-10 census.
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
Start sha: 5870e7076fcd81df4729e00231a8556ee3a5d5c5
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b (Grep floor): the render fixes made during the gate (muted trailing absent values in counts tokens and the questions counts line; the selected question's reason muted) change only role spans in src/superclaude/cli/observe/render.py (_absent_tail, _token_line, _question_line, _panel_lines); no signature or plain text changes.
Evidence: uv run pytest tests/observe/ -q printed '847 passed in 22.94s' (842 before the task) including the 5 pty tests; ruff check All checks passed; git diff --stat -- tests/observe/*.json is empty. Gate output: /home/coder/workspaces/worktrees/IronClaude/issue-606/.dev/tasks/to-do/TASK-WF-redesignSpec-20261118-043319/artifacts/gates/p1/iter-1..3 (renders, checks.json, reviewer-outputs/width-<W>.scores.md). The gate stopped after iteration 3 with RB-08 at width 80 failing (a key-list cut that is a text defect scheduled for a later phase); stop record: .dev/issues/409/visual-parity/scores/p1/stop.md. Touched: src/superclaude/cli/observe/render.py, tests/observe/test_render.py (modified, tracked); tests/observe/live_child.py, tests/observe/test_live_screen_pty.py, .dev/issues/409/visual-parity/scores/p1/stop.md (new); .dev/issues/409/visual-parity/tools/render_compare.py (untracked; the diff below is old copy to current).

diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index 8c67ec947..efd1b4b4c 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -184,13 +184,18 @@ def _absent_role(text: str, role: str = "body") -> str:
 # -- the COUNTS strip ------------------------------------------------------------------------------
 
 
+def _absent_tail(text: str, role: str) -> Line:
+    """``text`` in ``role``, except a trailing absent value (the source had none), which is muted.
+    ``text_of`` quotes a real value "unknown", so a bare trailing word means absent."""
+    for absent in (UNAVAILABLE, "unavailable", "unknown"):
+        cut = len(text) - len(absent)
+        if text.endswith(absent) and (cut == 0 or text[cut - 1] == " "):
+            return join(seg(text[:cut], role), seg(text[cut:], "muted"))
+    return seg(text, role)
+
+
 def _token_line(text: str, token: CountsToken) -> Line:
-    if token.protected:
-        return seg(text, "identity")
-    if text.endswith(UNAVAILABLE):  # the suffix is the absent part: muted
-        cut = len(text) - len(UNAVAILABLE)
-        return join(seg(text[:cut], "body"), seg(text[cut:], "muted"))
-    return seg(text, "body")
+    return _absent_tail(text, "identity" if token.protected else "body")
 
 
 def counts_line_objects(
@@ -510,8 +515,12 @@ def _question_line(q: QuestionLine, policy: TerminalPolicy) -> Line:
     ):  # a cut question text ends in a visible "..."
         text = text[: _prefix_length(text, room - 3)] + "..."
     shown = clip(text, room, policy)
-    if q.selected:
-        return seg(clip(head + shown + tail, width, policy), "selected")
+    if (
+        q.selected
+    ):  # marker, age and question text in one role; the absent reason stays muted
+        return join(seg(head + shown, "selected"), seg(tail, "muted")).clipped(
+            width, policy
+        )
     lead = ascii_safe(q.lead) if policy.ascii else q.lead
     marker = head[: len(head) - len(lead) - 2]
     line = join(
@@ -569,7 +578,10 @@ def _panel_lines(
     for state_line in panel.state_lines:  # the state of the read comes first
         lines += _wrapped(state_line, width, policy, "muted")
     lines += _wrapped(panel.disclosure, width, policy, "muted")
-    lines += _wrapped(panel.counts_line, width, policy, "identity")
+    lines += [
+        _absent_tail(text, "identity")
+        for text in wrap(panel.counts_line, width, policy)
+    ]
     lines += _wrapped(panel.caveat_line, width, policy, "muted")
     shown, cut = panel.window(capacity)
     lines += [_question_line(q, policy) for q in shown]
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 41dcd9efc..2a37fe1d8 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -1221,7 +1221,9 @@ def test_a_selected_question_is_one_bold_amber_line_and_the_others_have_parts(
     _, view = r3_screen(fake_clock, rows, 1, 160, height=60)
     lines = _compose(view, policy_for(160, height=60))
     selected = next(ln for ln in lines if ln.plain.startswith("▸ "))
-    assert {s.role for s in selected.spans} == {"selected"}
+    assert roles_at(selected, "second?") == {"selected"}
+    assert roles_at(selected, "▸") == {"selected"}
+    assert roles_at(selected, "reason unknown") == {"muted"}  # absent stays muted
     other = first_line(lines, "first?")
     assert roles_at(other, "first?") == {"body_bold"}
     assert roles_at(other, "reason unknown") == {"muted"}
@@ -1231,6 +1233,13 @@ def test_a_selected_question_is_one_bold_amber_line_and_the_others_have_parts(
 def test_absent_values_are_muted_and_state_words_follow_the_table(fake_clock):
     view = fixture_view("missing-fields", fake_clock)
     lines = _compose(view, policy_for(160, height=60))
+    counts = first_line(
+        lines, "source counts:"
+    )  # a counts token ending in an absent value
+    assert roles_at(counts, "source counts:") == {"body"}
+    assert roles_at(counts, "unknown  runs") == {"muted"}  # the absent value itself
+    cost = first_line(lines, "cost unavailable")
+    assert roles_at(cost, "unavailable") == {"muted"}
     absent = first_line(lines, "unknown (unknown)")
     assert roles_at(absent, "unknown (unknown)") == {"muted"}  # the bare verdict
     assert any(
diff --git a/tests/observe/live_child.py b/tests/observe/live_child.py
new file mode 100644
index 000000000..7f040265e
--- /dev/null
+++ b/tests/observe/live_child.py
@@ -0,0 +1,41 @@
+"""Live-screen child: draws one questions screen through the real ``LiveScreen`` on a pty.
+
+Run only by ``test_live_screen_pty.py``. It reads the terminal size and the environment the way
+the command does (``detect_size``, ``resolve_policy``), draws once, prints ``LIVE_READY`` and
+waits for one line on stdin, then closes the screen so the alternate screen is left cleanly.
+"""
+
+from __future__ import annotations
+
+import os
+import sys
+from pathlib import Path
+
+sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
+
+from superclaude.cli.observe.commands import LiveScreen  # noqa: E402
+from superclaude.cli.observe.terminal import (  # noqa: E402
+    detect_size,
+    output_encoding,
+    resolve_policy,
+)
+from tests.observe.conftest import FakeClock  # noqa: E402
+from tests.observe.test_render import r3_rows, r3_screen  # noqa: E402
+
+
+def main() -> int:
+    width, height = detect_size()
+    policy = resolve_policy(os.environ, output_encoding(), {}, width, height)
+    rows = r3_rows([("w-001", "first?"), ("w-002", "second?"), ("w-003", "third?")])
+    _, view = r3_screen(FakeClock(), rows, 1, width, height)
+    screen = LiveScreen()
+    screen.draw(view, policy, None)
+    sys.stdout.write("LIVE_READY\n")
+    sys.stdout.flush()
+    sys.stdin.readline()
+    screen.close()
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
diff --git a/tests/observe/test_live_screen_pty.py b/tests/observe/test_live_screen_pty.py
new file mode 100644
index 000000000..009a9137f
--- /dev/null
+++ b/tests/observe/test_live_screen_pty.py
@@ -0,0 +1,93 @@
+"""The real ``LiveScreen`` on a pty: alternate screen, colour depth, no blink, no mouse (Q5 live gate).
+
+``Console(file=StringIO)`` writes nothing under ``Live(screen=True)``, so the live path is only
+checked on a real pseudo-terminal. The child is ``live_child.py``.
+"""
+
+from __future__ import annotations
+
+import os
+import re
+import sys
+from pathlib import Path
+
+import pytest
+
+pexpect = pytest.importorskip("pexpect")
+pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX pty test")
+
+CHILD = Path(__file__).with_name("live_child.py")
+ROOT = Path(__file__).resolve().parents[2]
+SGR = re.compile(rb"\x1b\[([0-9;]*)m")
+MOUSE = (b"\x1b[?1000h", b"\x1b[?1002h", b"\x1b[?1003h", b"\x1b[?1006h")
+
+
+def run_child(env_extra: dict, rows: int = 40, cols: int = 160) -> bytes:
+    """Everything the live screen wrote to the terminal, from start to a clean exit."""
+    env = {
+        k: v
+        for k, v in os.environ.items()
+        if k not in ("COLUMNS", "LINES", "NO_COLOR", "COLORTERM", "TERM")
+    }
+    env["TERM"] = "xterm"
+    env.update(env_extra)
+    child = pexpect.spawn(
+        sys.executable,
+        [str(CHILD)],
+        env=env,
+        dimensions=(rows, cols),
+        encoding=None,
+        cwd=str(ROOT),
+        timeout=60,
+    )
+    child.expect(b"LIVE_READY")
+    before = child.before + b"LIVE_READY"
+    child.sendline(b"")
+    child.expect(pexpect.EOF)
+    return before + child.before
+
+
+def sgr_codes(data: bytes) -> list[int]:
+    """Every SGR code in ``data``; the arguments of extended colours (38 and 48) are skipped."""
+    codes: list[int] = []
+    for match in SGR.finditer(data):
+        params = [int(p) if p else 0 for p in match.group(1).split(b";")]
+        i = 0
+        while i < len(params):
+            if params[i] in (38, 48) and i + 1 < len(params):
+                i += 3 if params[i + 1] == 5 else 5
+                continue
+            codes.append(params[i])
+            i += 1
+    return codes
+
+
+def test_the_live_screen_uses_the_alternate_screen_and_no_mouse_or_blink():
+    out = run_child({})
+    assert b"\x1b[?1049h" in out and b"\x1b[?1049l" in out  # entered and left cleanly
+    assert not any(seq in out for seq in MOUSE)
+    assert not {5, 6} & set(sgr_codes(out))  # no blink
+
+
+def test_a_truecolor_terminal_gets_the_mockup_palette():
+    out = run_child({"COLORTERM": "truecolor"})
+    assert b"38;2;" in out
+
+
+def test_a_256_colour_terminal_gets_indexed_colours_only():
+    out = run_child({"TERM": "xterm-256color"})
+    assert b"38;5;" in out and b"38;2;" not in out
+
+
+def test_a_16_colour_terminal_gets_only_16_colour_codes():
+    out = run_child({})
+    codes = sgr_codes(out)
+    assert codes and b"38;2;" not in out and b"38;5;" not in out
+    assert all(c in (0, 1, 22) or 30 <= c <= 37 or 90 <= c <= 97 for c in codes)
+
+
+def test_no_color_writes_no_colour_or_weight_codes():
+    out = run_child({"NO_COLOR": "1", "COLORTERM": "truecolor"})
+    assert b"\x1b[?1049h" in out
+    # Measured: with NO_COLOR the console sets no style at all, so no SGR sequence is written.
+    assert sgr_codes(out) == []
diff --git a/.dev/issues/409/visual-parity/scores/p1/stop.md b/.dev/issues/409/visual-parity/scores/p1/stop.md
new file mode 100644
index 000000000..aa0e5b566
--- /dev/null
+++ b/.dev/issues/409/visual-parity/scores/p1/stop.md
@@ -0,0 +1,30 @@
+# Gate stop: colour and theme phase (plan Phase 2, spec P1)
+
+Status: STOPPED after iteration 3. The next phase is not started. Owner decision needed.
+
+## Failing rows after iteration 3
+
+- RB-08 at width 80 (High). Evidence: the ledger screen's key list is cut at 80 columns (`... m mark  e exp>`, the `e export all  q quit` part is lost) and the last line of the screen is `shown 31/54 | collected 80 / reported 80`, so "the footer keys are the last lines" does not hold. The script check (`checks.json`, RB-08, case `ledger@80`) fails the same way in all three iterations. All other in-scope rows (RB-01, RB-05, RB-06, RB-07, RB-09, RB-10, RB-11, RB-23) pass at all three widths in iteration 3.
+
+## Iteration scores (failing High and Medium rows, per width)
+
+| Iteration | 160 | 116 | 80 | What changed before it |
+|---|---|---|---|---|
+| 1 | RB-11 | RB-11 | RB-08, RB-11 | first render |
+| 2 | RB-11 | none | RB-08, RB-11 | absent values at the end of a counts token muted; the selected question keeps its reason muted |
+| 3 | none | none | RB-08 | the counts line `... unavailable (no source)` muted |
+
+Reviewer answers (one per width per iteration): `artifacts/gates/p1/iter-<n>/reviewer-outputs/width-<W>.scores.md` in the plan package.
+
+## Why this cannot be fixed inside this phase
+
+The cut key list at 80 columns is finding M-11. The spec closes it in the text-defects phase (spec P2, step 2.3, `wrap_groups`, rubric RB-13) and that phase regenerates both presentation goldens. The colour phase must leave every `screen_lines` string and both goldens byte-identical (spec P1, "Byte-identical in this phase"). Fixing it here would break that rule. The same defect already failed on the baseline (`scores/baseline.json`, RB-08 at 80 is FAIL), although the spec's baseline expectation listed RB-08 as passing.
+
+## Decision needed from the owner
+
+Choose one:
+
+- Option A (recommended): for this phase's gate only, treat the footer-key clause of RB-08 at width 80 as deferred to the text-defects phase, where RB-13 and the footer fix land, and close this phase as passed. Nothing else changes.
+- Option B: pull the key-list fix (M-11) forward into this phase and re-baseline the release-1 presentation golden here; the colour phase then loses its "no text change" guarantee.
+
+Until the owner answers, no later task of the plan is started.
diff --git a/tmp/rc-old.py b/.dev/issues/409/visual-parity/tools/render_compare.py
index 24fcf0f47..a36fbc043 100644
--- a/tmp/rc-old.py
+++ b/.dev/issues/409/visual-parity/tools/render_compare.py
@@ -56,9 +56,9 @@ current = _load_current()
 
 from rich.cells import cell_len  # noqa: E402
 
+from superclaude.cli.observe import view as observe_view  # noqa: E402
 from superclaude.cli.observe.render import render, screen_lines  # noqa: E402
 from superclaude.cli.observe.terminal import make_console, resolve_policy  # noqa: E402
-from superclaude.cli.observe import view as observe_view  # noqa: E402
 
 SCREENS = current.SCREENS
 WIDTHS = current.WIDTHS
@@ -295,6 +295,62 @@ def theme_rows() -> dict:
     return {"RB-09": rb09, "RB-10": rb10}
 
 
+def fg_by_char(stream_line: str) -> list[tuple[str, int | None]]:
+    """(character, foreground SGR code) for each visible character of one 16-colour stream line."""
+    out: list[tuple[str, int | None]] = []
+    fg: int | None = None
+    pos = 0
+    for m in SGR.finditer(stream_line):
+        out += [(ch, fg) for ch in stream_line[pos : m.start()]]
+        for p in [int(x) if x else 0 for x in m.group(0)[2:-1].split(";")]:
+            if p == 0 or p == 39:
+                fg = None
+            elif 30 <= p <= 37 or 90 <= p <= 97:
+                fg = p
+        pos = m.end()
+    out += [(ch, fg) for ch in stream_line[pos:]]
+    return out
+
+
+def state_census(stream: str) -> dict:
+    """RB-10 (a) and (b) on the 16-colour ledger stream: a state word in the table carries exactly
+    its role's colour, and every other state word carries the body colour (never a state role)."""
+    try:
+        from superclaude.cli.observe import theme  # type: ignore
+    except ImportError:
+        return _row("na", "theme.py not built yet (plan Phase 2)")
+
+    def code(role: str) -> int | None:
+        style = theme.style_for(role, "standard")
+        number = style.color.number if style and style.color is not None else None
+        return None if number is None else (30 + number if number < 8 else 82 + number)
+
+    in_table = {value: theme.STATE_ROLE[key] for key, value in ((k, k[1]) for k in theme.STATE_ROLE)}
+    other = ("idle", "blocked", "exited", "ready", "stopped", "abandoned", "active", "dispatched", "ended", "unverifiable")
+    bad: list[str] = []
+    checked = 0
+    for line in stream.split("\n"):
+        plain = strip_sgr(line)
+        if not re.search(r"\bw-\d{3}\b", plain):
+            continue
+        chars = fg_by_char(line)
+        for m in re.finditer(r"\b[A-Za-z]+\b", plain):
+            word = m.group(0)
+            if word in in_table:
+                want = code(in_table[word])
+            elif word in other:
+                want = code("body")
+            else:
+                continue
+            checked += 1
+            got = {fg for _, fg in chars[m.start() : m.end()]}
+            if got != {want}:
+                bad.append(f"{word!r} has colours {sorted(map(str, got))}, want {want}: {plain.strip()[:60]}")
+    if not checked:
+        return _row("fail", "no state word found on the ledger rows")
+    return _row("fail", *bad[:4]) if bad else _row("pass", f"{checked} state words checked against the table")
+
+
 # -- main -----------------------------------------------------------------------------------
 
 
@@ -347,6 +403,8 @@ def main(argv=None) -> int:
                 rows = check_screen(name, view, width, height, {"plain": base.plain, "stream": base.stream}, nocolor, ascii_out)
                 for rid, row in rows.items():
                     merge(rid, f"{name}@{width}", row)
+                if name == "ledger" and width == 160:
+                    merge("RB-10", "census@160", state_census(base.stream))
                 if truecolor_stream and entry["depths"].get("truecolor") == "truecolor":
                     colours = role_census_truecolor(truecolor_stream)
                     stray = [c for c in colours if c not in PALETTE]
@@ -357,7 +415,7 @@ def main(argv=None) -> int:
 
     if args.check:
         for rid, row in theme_rows().items():
-            all_rows[rid] = [("theme", row)]
+            merge(rid, "theme", row)
         for rid in ("RB-16",):
             all_rows[rid] = [("roles", _row("na", "needs role spans (plan Phase 2 and Phase 5); checked then"))]
         baseline_md = VP / "scores" / "baseline.md"
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
