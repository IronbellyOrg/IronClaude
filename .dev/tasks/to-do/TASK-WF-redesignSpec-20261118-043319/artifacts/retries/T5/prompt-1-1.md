4b5fba831ba572764096e72d6b7899cabb4d7bba
Review one task for spec compliance.

Task brief: ## Task 5: Resolve the colour system in the policy and add the theme module

Depends on: Task 4

Spec steps 1.1 and 1.2. In `OBS/terminal.py` add `color_system: str | None = "standard"` as the last field of the frozen `TerminalPolicy`; in `resolve_policy` return `None` when NO_COLOR is set or `TERM` is `dumb` or `unknown`, `"truecolor"` for `COLORTERM` `truecolor` or `24bit`, `"256"` when `TERM` ends `256color`, else `"standard"`; in `make_console` (line 121) use `color_system=policy.color_system`, keeping `no_color=policy.no_color`. The `NO_COLOR` literal stays only in `terminal.py`. Create `OBS/theme.py` with `ROLES` (title, attention, attention_title, identity, secondary, body, body_bold, muted, selected, border_attention, border_secondary, border_count, state_running, state_settled, state_failed, state_frozen), `style_for(role, depth)` (None for no depth), one table per depth using the palettes of step 1.2 (truecolor RGB, 256 indexes, 16-colour named ANSI colours), Style objects cached per `(role, depth)`, `STATE_ROLE` and `FROZEN_ROLE = "state_frozen"` as in step 1.4, and none of the literals `Console(`, `NO_COLOR`, `COLUMNS`, `stdout.encoding`, `getpreferredencoding` (comments included). Add depth cases to `tests/observe/test_terminal.py` and create `tests/observe/test_theme.py` per step 1.6(d) and (e).

Acceptance criteria:
- `tests/observe/test_terminal.py` covers NO_COLOR, `TERM=dumb`, COLORTERM truecolor, TERM `xterm-256color` and none, each checking `make_console(...).color_system`; the callers that build policies with an empty env (`tests/observe/test_render.py`, `test_commands.py`, `release1_surface.py`, `conftest.py`, `test_export.py`, `test_question_cap.py`, `test_linkoff_screen_reference.py`, `test_golden_contract.py`) still pass unchanged.
- `tests/observe/test_theme.py` asserts every role exists at every depth, eight distinct palette roles at `"standard"`, four distinct state-role SGR codes at `"standard"`, the five required `STATE_ROLE` keys, `FROZEN_ROLE == "state_frozen"`, and no blink.
- The source scan of `tests/observe/test_terminal.py` (lines 181-198) passes, so no forbidden literal sits in `theme.py`.
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
Start sha: 4b5fba831ba572764096e72d6b7899cabb4d7bba
Diff against the start snapshot: Codegraph context: index_state: fresh; checked_at: 2026-11-18T04:42:32Z; worktree_root: /home/coder/workspaces/worktrees/IronClaude/issue-606; projectPath: /home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b (Grep floor, confirmed by Read): TerminalPolicy is constructed only in src/superclaude/cli/observe/terminal.py (resolve_policy); its new last field has a default, so every existing construction stays valid. resolve_policy callers: src/superclaude/cli/observe/commands.py and the tests test_question_cap.py, test_render.py, test_terminal.py, release1_surface.py, conftest.py, test_export.py, test_commands.py, test_linkoff_screen_reference.py, test_golden_contract.py (none edited by this task; all pass with an empty or default environment, which resolves to standard). make_console callers: src/superclaude/cli/observe/commands.py (LiveScreen.draw, run_once) and tests; make_console now passes policy.color_system, which equals the old value for an empty environment (standard) and for NO_COLOR (None).
Evidence: uv run pytest tests/observe/ -q printed '819 passed in 19.17s' (794 before this task); uv run ruff check on src/superclaude/cli/observe and tests/observe: All checks passed. Touched: src/superclaude/cli/observe/terminal.py, tests/observe/test_terminal.py (modified); src/superclaude/cli/observe/theme.py, tests/observe/test_theme.py (new, full-file diffs).

diff --git a/src/superclaude/cli/observe/terminal.py b/src/superclaude/cli/observe/terminal.py
index 5c1b36819..452a86900 100644
--- a/src/superclaude/cli/observe/terminal.py
+++ b/src/superclaude/cli/observe/terminal.py
@@ -41,6 +41,8 @@ class TerminalPolicy:
     no_color: bool
     ascii: bool
     width_class: str  # "full" | "line" | "short" | "narrow"
+    # Colour depth for the console: None (no colour), "standard" (16), "256" or "truecolor".
+    color_system: str | None = "standard"
 
     @property
     def too_narrow(self) -> bool:
@@ -70,6 +72,18 @@ def width_class(width: int) -> str:
     return "narrow"
 
 
+def _color_system(env: Mapping[str, str], no_color: bool) -> str | None:
+    """Colour depth from the environment: none, truecolor, 256-colour or the 16-colour floor."""
+    term = env.get("TERM", "")
+    if no_color or term in ("dumb", "unknown"):
+        return None
+    if env.get("COLORTERM", "").lower() in ("truecolor", "24bit"):
+        return "truecolor"
+    if term.endswith("256color"):
+        return "256"
+    return "standard"
+
+
 def resolve_policy(
     env: Mapping[str, str],
     encoding: str | None,
@@ -89,6 +103,7 @@ def resolve_policy(
         no_color=no_color,
         ascii=use_ascii,
         width_class=width_class(width),
+        color_system=_color_system(env, no_color),
     )
 
 
@@ -118,7 +133,7 @@ def make_console(
         highlight=False,
         markup=False,
         emoji=False,
-        color_system=None if policy.no_color else "standard",
+        color_system=policy.color_system,
         no_color=policy.no_color,
         safe_box=policy.ascii,
         record=record,
diff --git a/tests/observe/test_terminal.py b/tests/observe/test_terminal.py
index 3f63a2841..3ac341538 100644
--- a/tests/observe/test_terminal.py
+++ b/tests/observe/test_terminal.py
@@ -51,6 +51,50 @@ def test_no_color_unset_or_empty_keeps_colour_available(env):
     assert "31" in [p for m in SGR.findall(render(pol, "red")) for p in m.split(";")]
 
 
+# -- colour depth (D2): none, truecolor, 256-colour, 16-colour floor ---------------
+
+
+@pytest.mark.parametrize(
+    ("env", "expected"),
+    [
+        ({"NO_COLOR": "1"}, None),
+        ({"NO_COLOR": "1", "COLORTERM": "truecolor"}, None),
+        ({"TERM": "dumb"}, None),
+        ({"TERM": "unknown"}, None),
+        ({"COLORTERM": "truecolor", "TERM": "xterm"}, "truecolor"),
+        ({"COLORTERM": "24bit"}, "truecolor"),
+        ({"COLORTERM": "TrueColor"}, "truecolor"),
+        ({"TERM": "xterm-256color"}, "256"),
+        ({"TERM": "xterm"}, "standard"),
+        ({}, "standard"),
+        ({"NO_COLOR": ""}, "standard"),
+    ],
+)
+def test_colour_depth_is_resolved_from_the_environment(env, expected):
+    pol = policy(env)
+    assert pol.color_system == expected
+    assert make_console(pol, file=io.StringIO()).color_system == expected
+
+
+def test_truecolor_beats_256_colour_when_both_are_set():
+    pol = policy({"COLORTERM": "truecolor", "TERM": "xterm-256color"})
+    assert pol.color_system == "truecolor"
+
+
+@pytest.mark.parametrize(
+    ("env", "style", "needle"),
+    [
+        # A different colour per case: Rich caches the ANSI codes on a parsed style, so
+        # reusing one colour string at two depths would show the first depth's codes.
+        ({"COLORTERM": "truecolor"}, "rgb(10,200,30)", "38;2;10;200;30"),
+        ({"TERM": "xterm-256color"}, "rgb(11,201,31)", "38;5;"),
+    ],
+)
+def test_the_chosen_depth_reaches_the_bytes_the_console_writes(env, style, needle):
+    out = render(policy(env), style)
+    assert needle in out
+
+
 # -- width classes, height, ASCII -----------------------------------------------
 
 
diff --git a/src/superclaude/cli/observe/theme.py b/src/superclaude/cli/observe/theme.py
new file mode 100644
index 000000000..a8346b182
--- /dev/null
+++ b/src/superclaude/cli/observe/theme.py
@@ -0,0 +1,126 @@
+"""Colour roles for the observer screens, one explicit table per colour depth.
+
+The screen builders tag text with a semantic role (``attention``, ``muted``, ``state_running``
+and so on); this module maps a role and a depth to a Rich ``Style``. The depth is the
+``color_system`` of the terminal policy: ``"truecolor"`` uses the design-mockup palette exactly,
+``"256"`` the nearest indexed colours, and ``"standard"`` (16 colours) named ANSI colours only,
+because Rich's automatic downgrade of the mockup RGB values collapses several roles onto one
+index. No role sets blink, dim or reverse. No module here builds a console or reads the
+environment: the terminal policy module owns both.
+"""
+
+from __future__ import annotations
+
+from rich.style import Style
+
+ROLES: tuple[str, ...] = (
+    "title",
+    "attention",
+    "attention_title",
+    "identity",
+    "secondary",
+    "body",
+    "body_bold",
+    "muted",
+    "selected",
+    "border_attention",
+    "border_secondary",
+    "border_count",
+    "state_running",
+    "state_settled",
+    "state_failed",
+    "state_frozen",
+)
+
+# Each role names one of the eight palette colours and says whether it is bold.
+_PALETTE_OF: dict[str, str] = {
+    "title": "cyan",
+    "attention": "amber",
+    "attention_title": "amber",
+    "identity": "base",
+    "secondary": "slate",
+    "body": "base",
+    "body_bold": "base",
+    "muted": "muted",
+    "selected": "amber",
+    "border_attention": "amber",
+    "border_secondary": "slate",
+    "border_count": "cyan",
+    "state_running": "green",
+    "state_settled": "cyan",
+    "state_failed": "red",
+    "state_frozen": "violet",
+}
+_BOLD: frozenset[str] = frozenset(
+    {"title", "attention", "attention_title", "secondary", "body_bold", "selected"}
+)
+
+# The eight palette colours per depth (mockup RGB; 256-colour indexes; named 16-colour ANSI colours).
+_COLOURS: dict[str, dict[str, str]] = {
+    "truecolor": {
+        "base": "rgb(225,233,238)",
+        "muted": "rgb(165,182,194)",
+        "slate": "rgb(82,108,128)",
+        "amber": "rgb(250,178,25)",
+        "cyan": "rgb(112,205,226)",
+        "green": "rgb(139,215,175)",
+        "red": "rgb(240,141,150)",
+        "violet": "rgb(194,173,242)",
+    },
+    "256": {
+        "base": "color(189)",
+        "muted": "color(145)",
+        "slate": "color(60)",
+        "amber": "color(214)",
+        "cyan": "color(80)",
+        "green": "color(115)",
+        "red": "color(210)",
+        "violet": "color(147)",
+    },
+    "standard": {
+        "base": "bright_white",
+        "muted": "white",
+        "slate": "bright_black",
+        "amber": "bright_yellow",
+        "cyan": "bright_cyan",
+        "green": "green",
+        "red": "red",
+        "violet": "magenta",
+    },
+}
+
+# Display mapping from a real state word to a state role, keyed by (field, exact raw value).
+# This is a display choice, not a count mapping and not a health verdict: the word is always
+# printed, and every value not listed here keeps the body role.
+STATE_ROLE: dict[tuple[str, str], str] = {
+    ("workerState", "running"): "state_running",
+    ("liveness", "alive"): "state_running",
+    ("liveness", "live"): "state_running",
+    ("workerState", "succeeded"): "state_settled",
+    ("dispatchStatus", "completed"): "state_settled",
+    ("workerState", "failed"): "state_failed",
+    ("dispatchStatus", "failed"): "state_failed",
+}
+FROZEN_ROLE = (
+    "state_frozen"  # a flags cell holding the frozen marker (fixture mode only)
+)
+
+_CACHE: dict[tuple[str, str], Style] = {}
+
+
+def style_for(role: str, depth: str | None) -> Style | None:
+    """The Rich style of ``role`` at ``depth``; ``None`` when there is no colour depth.
+
+    Styles are cached per ``(role, depth)`` so a style made for one depth in a process is never
+    reused for another (Rich caches the ANSI codes it renders on a ``Style``).
+    """
+    if role not in _PALETTE_OF:
+        raise KeyError(f"unknown role: {role!r}")
+    if depth is None:
+        return None
+    key = (role, depth)
+    style = _CACHE.get(key)
+    if style is None:
+        style = Style(color=_COLOURS[depth][_PALETTE_OF[role]], bold=role in _BOLD)
+        _CACHE[key] = style
+    return style
diff --git a/tests/observe/test_theme.py b/tests/observe/test_theme.py
new file mode 100644
index 000000000..8add9681d
--- /dev/null
+++ b/tests/observe/test_theme.py
@@ -0,0 +1,95 @@
+"""Colour roles: every role exists at every depth, the 16-colour floor keeps its roles apart."""
+
+from __future__ import annotations
+
+import pytest
+
+from superclaude.cli.observe import theme
+from superclaude.cli.observe.theme import (
+    FROZEN_ROLE,
+    ROLES,
+    STATE_ROLE,
+    style_for,
+)
+
+DEPTHS = ("standard", "256", "truecolor")
+# One role per palette colour, so eight distinct colours means eight distinct roles (RB-09).
+PALETTE_ROLES = (
+    "attention",  # amber
+    "identity",  # base
+    "secondary",  # slate
+    "muted",
+    "state_running",  # green
+    "state_settled",  # cyan
+    "state_failed",  # red
+    "state_frozen",  # violet
+)
+
+
+@pytest.mark.parametrize("depth", DEPTHS)
+def test_every_role_has_a_style_at_every_depth(depth):
+    for role in ROLES:
+        assert style_for(role, depth) is not None
+
+
+def test_no_depth_means_no_style():
+    assert all(style_for(role, None) is None for role in ROLES)
+
+
+def test_an_unknown_role_is_an_error_not_a_silent_default():
+    with pytest.raises(KeyError):
+        style_for("nonsense", "standard")
+
+
+def test_the_eight_palette_roles_keep_eight_distinct_colours_at_16_colours():
+    numbers = [style_for(role, "standard").color.number for role in PALETTE_ROLES]
+    assert len(set(numbers)) == 8
+
+
+def test_the_four_state_roles_have_four_different_codes_at_16_colours():
+    roles = ("state_running", "state_settled", "state_failed", "state_frozen")
+    codes = {style_for(role, "standard").color.number for role in roles}
+    assert len(codes) == 4
+
+
+def test_the_state_table_is_not_empty_and_names_the_minimum_keys():
+    required = [
+        ("workerState", "running"),
+        ("workerState", "succeeded"),
+        ("workerState", "failed"),
+        ("dispatchStatus", "completed"),
+        ("liveness", "alive"),
+    ]
+    assert all(key in STATE_ROLE for key in required)
+    assert FROZEN_ROLE == "state_frozen"
+    assert all(role in ROLES for role in (*STATE_ROLE.values(), FROZEN_ROLE))
+    # A word the table does not name keeps the body role: it is never classified.
+    assert ("workerState", "blocked") not in STATE_ROLE
+    assert ("terminalState", "released") not in STATE_ROLE
+
+
+def test_no_style_blinks_dims_or_reverses():
+    for depth in DEPTHS:
+        for role in ROLES:
+            style = style_for(role, depth)
+            assert not (style.blink or style.blink2 or style.dim or style.reverse)
+
+
+def test_styles_are_distinct_objects_per_depth_and_cached_per_depth():
+    standard = style_for("attention", "standard")
+    truecolor = style_for("attention", "truecolor")
+    assert standard is not truecolor and standard != truecolor
+    assert style_for("attention", "standard") is standard
+    assert truecolor.color.get_truecolor().hex == "#fab219"
+
+
+def test_the_theme_module_holds_no_terminal_facts():
+    text = open(theme.__file__, encoding="utf-8").read()
+    for literal in (
+        "Console(",
+        "NO_COLOR",
+        "COLUMNS",
+        "stdout.encoding",
+        "getpreferredencoding",
+    ):
+        assert literal not in text
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
