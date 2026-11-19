a0470c0d8ad3b097c83e3b74c4c3f4242eceb13e
Review one task for spec compliance.

Task brief: ## Task 8: Make the one-shot path style-capable and update the style-sensitive tests

Depends on: Task 7

Spec steps 1.5 and 1.6 parts (a), (b), (c), (f). In `OBS/commands.py` add `_screen_text(view, policy, *, styled)` returning `console.file.getvalue()` when styled and `console.export_text()` otherwise; `run_once` (line 225, the `export_text()` call at line 242) sets `styled = policy.color_system is not None and stdout_is_tty`, taking stdout from the same dependency object `_emit` uses; add `policy.color_system` to the `LiveScreen` shape tuple (line 265). Leave lines 67 and 70 untouched. In `tests/observe/release1_surface.py` make `_printed` return `strip_sgr(buffer.getvalue())` (import `strip_sgr` from `tests.observe.conftest`). In `tests/observe/test_render.py` replace the check at lines 250-259 with `strip_sgr(colour) == nocolor` plus the ESC assertions, and apply `strip_sgr` before `cell_len` or `bad_chars` at every `printed(` call (lines 76, 161, 181, 255-256, 277, 605, 977, 987). Create `tests/observe/test_styled_capture.py` per step 1.6(f).

Acceptance criteria:
- `tests/observe/test_commands.py:121` (no ESC in piped one-shot output) still passes; the gate-constant tests at `tests/observe/test_commands.py:747-772` pass.
- `tests/observe/golden_release1_surface.json` and `golden_questions_linkoff.json` are byte-identical to before (`git diff --stat` shows neither).
- `_screen_text(styled=True)` at 160, 116 and 80 contains SGR and `strip_sgr` of it equals the `export_text()` text; NO_COLOR gives zero ESC; ASCII stays ASCII.
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
Start sha: a0470c0d8ad3b097c83e3b74c4c3f4242eceb13e
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b (Grep floor, confirmed by Read): run_once is called by execute in src/superclaude/cli/observe/commands.py and the tests; its signature is unchanged. LiveScreen.draw shape tuple gains a fifth member (read only inside draw). Two new private helpers (_stdout_is_tty, _screen_text) have no other callers except the new test file.
Evidence: uv run pytest tests/observe/ -q printed '842 passed in 20.39s' (830 before this task); ruff check: All checks passed; git diff --stat -- tests/observe/*.json is empty. The release1_surface _printed strip, the test_render.py strip_sgr comparison at the colour/no-colour test and the strip in the width test were made in the previous task (visible in the previous diff, not this one); this task strips two more printed() uses. Touched: src/superclaude/cli/observe/commands.py, tests/observe/test_render.py (modified); tests/observe/test_styled_capture.py (new).

diff --git a/src/superclaude/cli/observe/commands.py b/src/superclaude/cli/observe/commands.py
index 96d62615f..e1d85c2ef 100644
--- a/src/superclaude/cli/observe/commands.py
+++ b/src/superclaude/cli/observe/commands.py
@@ -222,6 +222,25 @@ def _write_snapshot(view: Any, target: Path) -> str | None:
 # -- --once ----------------------------------------------------------------------------------------------
 
 
+def _stdout_is_tty(deps: Deps) -> bool:
+    """True when the stream ``_emit`` writes to is a terminal (a piped one-shot stays plain)."""
+    stream = deps.stdout if deps.stdout is not None else sys.stdout
+    try:
+        return bool(stream.isatty())
+    except (AttributeError, ValueError, OSError):
+        return False
+
+
+def _screen_text(view: Any, policy: Any, *, styled: bool) -> str:
+    """The screen as text through a recorded console: with its colour and weight escapes when
+    ``styled`` (the bytes a terminal would receive), else the plain text.
+
+    ``export_text(styles=True)`` is never used: it ignores the colour switch and the colour depth."""
+    console = make_console(policy, file=io.StringIO(), record=True)
+    console.print(render(view, policy))
+    return console.file.getvalue() if styled else console.export_text()
+
+
 def run_once(options: Options, deps: Deps) -> int:
     clock = deps.clock or SystemClock()
     source = _build_source(options, deps)
@@ -237,9 +256,8 @@ def run_once(options: Options, deps: Deps) -> int:
     view = build_view(result, session, clock)
     if options.width is not None:  # the width-bound screen, through a recorded console
         policy = _policy_maker(options, deps)()
-        console = make_console(policy, file=io.StringIO(), record=True)
-        console.print(render(view, policy))
-        text = console.export_text()
+        styled = policy.color_system is not None and _stdout_is_tty(deps)
+        text = _screen_text(view, policy, styled=styled)
     else:
         text = record_text(view)
     _emit(text, deps)
@@ -262,7 +280,13 @@ class LiveScreen:
         self._shape: tuple | None = None
 
     def draw(self, view: Any, policy: Any, message: str | None) -> None:
-        shape = (policy.width, policy.height, policy.ascii, policy.no_color)
+        shape = (
+            policy.width,
+            policy.height,
+            policy.ascii,
+            policy.no_color,
+            policy.color_system,
+        )
         group = render(view, policy, message)
         if self._live is None or shape != self._shape:
             self.close()
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 443021841..41dcd9efc 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -139,7 +139,7 @@ def test_the_inspector_shows_the_full_identifier_wrapped_by_cells(fake_clock):
 
 def test_worker_text_with_markup_renders_literally(fake_clock):
     view = fixture_view("injection", fake_clock, Session(show_historical=True))
-    out = printed(view, policy_for(160))
+    out = strip_sgr(printed(view, policy_for(160)))
     assert "[bold]x[/bold]" in out
 
 
@@ -160,17 +160,19 @@ def test_injection_renders_no_escape_c1_or_format_characters(fake_clock, width,
         out = printed(view, policy)
         assert bad_chars(out) == [], out
         assert bad_chars("\n".join(screen_lines(view, policy))) == []
-    assert "red detail" in printed(
-        fixture_view(
-            "injection",
-            fake_clock,
-            Session(
-                focus="inspector",
-                selected=base.visible_rows[0].identity,
-                show_historical=True,
+    assert "red detail" in strip_sgr(
+        printed(
+            fixture_view(
+                "injection",
+                fake_clock,
+                Session(
+                    focus="inspector",
+                    selected=base.visible_rows[0].identity,
+                    show_historical=True,
+                ),
             ),
-        ),
-        policy_for(160),
+            policy_for(160),
+        )
     )
 
 
diff --git a/tests/observe/test_styled_capture.py b/tests/observe/test_styled_capture.py
new file mode 100644
index 000000000..51ca96474
--- /dev/null
+++ b/tests/observe/test_styled_capture.py
@@ -0,0 +1,83 @@
+"""The one-shot path can carry the screen's colour and weight; the capture is never export_text(styles=True)."""
+
+from __future__ import annotations
+
+import io
+
+import pytest
+
+from superclaude.cli.observe.commands import (
+    Options,
+    _screen_text,
+    _stdout_is_tty,
+    execute,
+)
+from superclaude.cli.observe.terminal import resolve_policy
+from tests.observe.conftest import strip_sgr
+from tests.observe.test_commands import deps_for
+from tests.observe.test_render import WIDTHS, fixture_view
+
+
+class _Tty(io.StringIO):
+    def isatty(self) -> bool:
+        return True
+
+
+def _policy(width, env=None, ascii=False):
+    return resolve_policy(env or {}, "utf-8", {"ascii": ascii}, width, 40)
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_a_styled_screen_has_escapes_and_the_same_text_as_the_plain_one(
+    fake_clock, width
+):
+    view = fixture_view("base", fake_clock)
+    policy = _policy(width)
+    styled = _screen_text(view, policy, styled=True)
+    plain = _screen_text(view, policy, styled=False)
+    assert "\x1b[" in styled
+    assert strip_sgr(styled) == plain and "\x1b" not in plain
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_no_color_gives_zero_escape_bytes_even_when_styled_is_asked_for(
+    fake_clock, width
+):
+    view = fixture_view("base", fake_clock)
+    out = _screen_text(view, _policy(width, {"NO_COLOR": "1"}), styled=True)
+    assert "\x1b" not in out
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_ascii_stays_ascii_with_colour_on(fake_clock, width):
+    view = fixture_view("long-identifiers", fake_clock)
+    out = _screen_text(view, _policy(width, ascii=True), styled=True)
+    assert "\x1b[" in out and out.isascii()
+
+
+def test_the_styled_capture_follows_the_colour_depth(fake_clock):
+    view = fixture_view("base", fake_clock)
+    truecolor = _screen_text(
+        view, _policy(160, {"COLORTERM": "truecolor"}), styled=True
+    )
+    standard = _screen_text(view, _policy(160), styled=True)
+    assert "38;2;" in truecolor and "38;2;" not in standard
+
+
+def test_a_piped_one_shot_stays_plain_and_a_terminal_one_is_styled(fake_clock):
+    options = Options(once=True, fixture="base", width=160)
+    piped = deps_for(fake_clock)  # a StringIO: not a terminal
+    assert execute(options, piped) == 0 and "\x1b" not in piped.stdout.getvalue()
+    tty = deps_for(fake_clock, stdout=_Tty())
+    assert execute(options, tty) == 0 and "\x1b[" in tty.stdout.getvalue()
+    quiet = deps_for(fake_clock, stdout=_Tty(), env={"NO_COLOR": "1"})
+    assert execute(options, quiet) == 0 and "\x1b" not in quiet.stdout.getvalue()
+    assert strip_sgr(tty.stdout.getvalue()) == piped.stdout.getvalue()
+
+
+def test_a_stream_without_isatty_counts_as_not_a_terminal(fake_clock):
+    class _Bare:
+        def write(self, text):
+            return len(text)
+
+    assert _stdout_is_tty(deps_for(fake_clock, stdout=_Bare())) is False
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
