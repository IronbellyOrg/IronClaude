cf0807971cd4e75cae1f7a055ccac076149c16eb
Review one task for spec compliance.

Task brief: ## Task 13: Reasons once and no hash on screen (view side)

Depends on: Task 12

Spec Part C steps 2.11 and 2.12. In `OBS/view.py` add `strip_hex(text) -> str` (remove every run of 32 or more `[0-9a-fA-F]` characters and collapse the double space left behind) applied only where the display strings `shown` and `DeskView.ask` are built, never to `ask`, `text` or anything `record_text` or `snapshot_json` read. Add the title note `reasons: none in source` and print the row suffix `reason unknown` only when the source gave a reason (decision D-13); the unknown-versus-none rule holds because the note is about the source. Rewrite the Q7 tests from Task 3 to assert the hash is absent from every screen line at 160, 116 and 80, the rest of the ask is intact, the screen fits, both canaries still pass, and the trailing-hash fixture keeps its four-line cut with `...`. Rewrite the `^\s*\d+[smh]  ` row checks and the `reason unknown` counting checks (`tests/observe/test_render.py` lines 453 and 930-948) to the new form.

Acceptance criteria:
- No run of 32 or more hex characters appears on the questions screen or the Decision Desk at any width; both hash canaries pass; the inspector keeps the full question text (default of Part C).
- A question row shows no `reason unknown` suffix when no reason is given, the title carries `reasons: none in source`, and a row with a reason shows it.
- `git diff --stat -- src/superclaude/cli/observe/export.py` is empty.
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
Start sha: cf0807971cd4e75cae1f7a055ccac076149c16eb
Diff against the start snapshot: diff --git a/src/superclaude/cli/observe/render.py b/src/superclaude/cli/observe/render.py
index 3d7dae082..f2d05294a 100644
--- a/src/superclaude/cli/observe/render.py
+++ b/src/superclaude/cli/observe/render.py
@@ -40,6 +40,7 @@ from superclaude.cli.observe.view import (
     INSPECTOR_TITLE,
     NO_MATCH_TEXT,
     QUESTIONS_REASON,
+    QUESTIONS_REASONS_NOTE,
     READ_ONLY_BADGE,
     UNAVAILABLE,
     CountsToken,
@@ -534,10 +535,13 @@ def _question_line(q: QuestionLine, policy: TerminalPolicy) -> Line:
     The age is ``attention``, the subject ``body_bold`` and the reason tail ``muted``; the
     selected question is one ``selected`` line."""
     width = policy.width
+    # The row shows a reason only when the source gave one (it has no such field today): the
+    # per-row "reason unknown" is replaced by one note in the title (see _panel_lines).
+    reason = "  " + q.reason if q.reason else ""
     if not q.link:
-        text = clip(q.text, width, policy)
+        text = clip((q.row_text or q.text) + reason, width, policy)
         split = text.find("  ")
-        tail = text.rfind("  " + QUESTIONS_REASON)
+        tail = text.rfind("  " + (q.reason or QUESTIONS_REASON))
         if split <= 0:
             return seg(text, "body_bold")
         if tail > split:
@@ -549,7 +553,7 @@ def _question_line(q: QuestionLine, policy: TerminalPolicy) -> Line:
         return join(seg(text[:split], "attention"), seg(text[split:], "body_bold"))
     mark = glyph("selected", policy) + " " if q.selected else "  "
     head = ascii_safe(mark + q.lead + "  ") if policy.ascii else mark + q.lead + "  "
-    tail = "  " + QUESTIONS_REASON
+    tail = ascii_safe(reason) if policy.ascii else reason
     room = max(width - cell_len(head) - cell_len(tail), 1)
     text = ascii_safe(q.shown) if policy.ascii else q.shown
     if (
@@ -606,6 +610,24 @@ def _desk_lines(desk: DeskView, policy: TerminalPolicy) -> list[Line]:
     return lines
 
 
+def _panel_title(
+    panel: QuestionsPanel, width: int, policy: TerminalPolicy
+) -> list[Line]:
+    """The panel title; when no question row carries a reason, the one note that replaces the
+    per-row "reason unknown" follows it, muted."""
+    if any(q.reason for q in panel.lines):
+        return _wrapped(panel.title, width, policy, "attention_title")
+    wrapped = wrap(f"{panel.title}  {QUESTIONS_REASONS_NOTE}", width, policy)
+    first, rest = wrapped[0], wrapped[1:]
+    title = ascii_safe(panel.title) if policy.ascii else panel.title
+    head = (
+        join(seg(title, "attention_title"), seg(first[len(title) :], "muted"))
+        if first.startswith(title)
+        else seg(first, "attention_title")
+    )
+    return [head, *_roled(rest, "muted")]
+
+
 def _panel_lines(
     panel: QuestionsPanel,
     policy: TerminalPolicy,
@@ -615,7 +637,7 @@ def _panel_lines(
     """The coordinator-questions block: header lines, up to ``capacity`` questions, then the
     desk block (when given), notes."""
     width = policy.width
-    lines = _wrapped(panel.title, width, policy, "attention_title")
+    lines = _panel_title(panel, width, policy)
     lines += _wrapped(panel.run_line, width, policy, "muted")
     for state_line in panel.state_lines:  # the state of the read comes first
         lines += _wrapped(state_line, width, policy, "muted")
diff --git a/src/superclaude/cli/observe/theme.py b/src/superclaude/cli/observe/theme.py
deleted file mode 100644
index a8346b182..000000000
--- a/src/superclaude/cli/observe/theme.py
+++ /dev/null
@@ -1,126 +0,0 @@
-"""Colour roles for the observer screens, one explicit table per colour depth.
-
-The screen builders tag text with a semantic role (``attention``, ``muted``, ``state_running``
-and so on); this module maps a role and a depth to a Rich ``Style``. The depth is the
-``color_system`` of the terminal policy: ``"truecolor"`` uses the design-mockup palette exactly,
-``"256"`` the nearest indexed colours, and ``"standard"`` (16 colours) named ANSI colours only,
-because Rich's automatic downgrade of the mockup RGB values collapses several roles onto one
-index. No role sets blink, dim or reverse. No module here builds a console or reads the
-environment: the terminal policy module owns both.
-"""
-
-from __future__ import annotations
-
-from rich.style import Style
-
-ROLES: tuple[str, ...] = (
-    "title",
-    "attention",
-    "attention_title",
-    "identity",
-    "secondary",
-    "body",
-    "body_bold",
-    "muted",
-    "selected",
-    "border_attention",
-    "border_secondary",
-    "border_count",
-    "state_running",
-    "state_settled",
-    "state_failed",
-    "state_frozen",
-)
-
-# Each role names one of the eight palette colours and says whether it is bold.
-_PALETTE_OF: dict[str, str] = {
-    "title": "cyan",
-    "attention": "amber",
-    "attention_title": "amber",
-    "identity": "base",
-    "secondary": "slate",
-    "body": "base",
-    "body_bold": "base",
-    "muted": "muted",
-    "selected": "amber",
-    "border_attention": "amber",
-    "border_secondary": "slate",
-    "border_count": "cyan",
-    "state_running": "green",
-    "state_settled": "cyan",
-    "state_failed": "red",
-    "state_frozen": "violet",
-}
-_BOLD: frozenset[str] = frozenset(
-    {"title", "attention", "attention_title", "secondary", "body_bold", "selected"}
-)
-
-# The eight palette colours per depth (mockup RGB; 256-colour indexes; named 16-colour ANSI colours).
-_COLOURS: dict[str, dict[str, str]] = {
-    "truecolor": {
-        "base": "rgb(225,233,238)",
-        "muted": "rgb(165,182,194)",
-        "slate": "rgb(82,108,128)",
-        "amber": "rgb(250,178,25)",
-        "cyan": "rgb(112,205,226)",
-        "green": "rgb(139,215,175)",
-        "red": "rgb(240,141,150)",
-        "violet": "rgb(194,173,242)",
-    },
-    "256": {
-        "base": "color(189)",
-        "muted": "color(145)",
-        "slate": "color(60)",
-        "amber": "color(214)",
-        "cyan": "color(80)",
-        "green": "color(115)",
-        "red": "color(210)",
-        "violet": "color(147)",
-    },
-    "standard": {
-        "base": "bright_white",
-        "muted": "white",
-        "slate": "bright_black",
-        "amber": "bright_yellow",
-        "cyan": "bright_cyan",
-        "green": "green",
-        "red": "red",
-        "violet": "magenta",
-    },
-}
-
-# Display mapping from a real state word to a state role, keyed by (field, exact raw value).
-# This is a display choice, not a count mapping and not a health verdict: the word is always
-# printed, and every value not listed here keeps the body role.
-STATE_ROLE: dict[tuple[str, str], str] = {
-    ("workerState", "running"): "state_running",
-    ("liveness", "alive"): "state_running",
-    ("liveness", "live"): "state_running",
-    ("workerState", "succeeded"): "state_settled",
-    ("dispatchStatus", "completed"): "state_settled",
-    ("workerState", "failed"): "state_failed",
-    ("dispatchStatus", "failed"): "state_failed",
-}
-FROZEN_ROLE = (
-    "state_frozen"  # a flags cell holding the frozen marker (fixture mode only)
-)
-
-_CACHE: dict[tuple[str, str], Style] = {}
-
-
-def style_for(role: str, depth: str | None) -> Style | None:
-    """The Rich style of ``role`` at ``depth``; ``None`` when there is no colour depth.
-
-    Styles are cached per ``(role, depth)`` so a style made for one depth in a process is never
-    reused for another (Rich caches the ANSI codes it renders on a ``Style``).
-    """
-    if role not in _PALETTE_OF:
-        raise KeyError(f"unknown role: {role!r}")
-    if depth is None:
-        return None
-    key = (role, depth)
-    style = _CACHE.get(key)
-    if style is None:
-        style = Style(color=_COLOURS[depth][_PALETTE_OF[role]], bold=role in _BOLD)
-        _CACHE[key] = style
-    return style
diff --git a/src/superclaude/cli/observe/view.py b/src/superclaude/cli/observe/view.py
index 46bc82151..d55632820 100644
--- a/src/superclaude/cli/observe/view.py
+++ b/src/superclaude/cli/observe/view.py
@@ -8,6 +8,7 @@ turns the ``UNKNOWN`` sentinel into screen words.
 
 from __future__ import annotations
 
+import re
 from collections.abc import Mapping
 from dataclasses import dataclass, replace
 from enum import Enum
@@ -62,6 +63,9 @@ QUESTIONS_NOT_HELD = (
 )
 QUESTIONS_EMPTY = "no observed questions in this source window; not proof none exist"
 QUESTIONS_REASON = "reason unknown"  # no verified reason field exists (PROPOSED)
+# On screen the per-row "reason unknown" is replaced by this one title note: the source has no
+# reason field, so "none in source" is a statement about the source, not about the world.
+QUESTIONS_REASONS_NOTE = "reasons: none in source"
 QUESTIONS_CLOSED = "closed by evidence: unavailable (no source)"
 QUESTIONS_RETENTION = (
     "retention reset at {hhmm}; questions observed before this start are not retained"
@@ -226,6 +230,10 @@ class QuestionLine:
     age_text: str = ""  # "5s", "unknown" ...
     lead: str = ""  # age and, when the question left the window, the bracketed state
     shown: str = ""  # the question text shown on screen: ``ask``, else the subject
+    # Screen only: the row without the per-row "reason unknown" (the record keeps ``text``), and
+    # the reason when the source gave one (it has no such field today, so this stays "").
+    row_text: str = ""
+    reason: str = ""
 
 
 @dataclass(frozen=True)
@@ -388,6 +396,16 @@ def text_of(value: Any) -> str:
     return str(value)
 
 
+_HEX_RUN = re.compile(r"( ?)[0-9a-fA-F]{32,}( ?)")
+
+
+def strip_hex(text: str) -> str:
+    """``text`` without any run of 32 or more hexadecimal characters (a plan hash): nothing is
+    left in its place, and the space on each side collapses to one. Display text only: the
+    record and the snapshot never read the result."""
+    return _HEX_RUN.sub(lambda m: " " if m[1] and m[2] else m[1] or m[2], text)
+
+
 def aggregate(count: int, unknown: int) -> str:
     """An aggregate with unknown members is never a clean number: ``n+? (k unknown)``."""
     return str(count) if unknown == 0 else f"{count}+? ({unknown} unknown)"
@@ -740,11 +758,12 @@ def _questions_panel(
                 lead.append(f"[{record.status_text}]")
             # R3: the payload question replaces the subject on screen only (text stays subject).
             ask = q.ask if isinstance(q.ask, str) and q.ask.strip() else ""
-            shown = ask or text_of(q.subject)
+            shown = strip_hex(ask or text_of(q.subject))
             built.append(
                 QuestionLine(
                     qid=text_of(q.qid),
                     text="  ".join(lead + [text_of(q.subject), QUESTIONS_REASON]),
+                    row_text="  ".join(lead + [text_of(q.subject)]),
                     created_at=q.created_at,
                     age_seconds=seconds,
                     in_window=record.in_window,
@@ -870,7 +889,7 @@ def _desk(
     return DeskView(
         qid=line.qid,
         age_text=line.age_text,
-        ask=line.ask or DESK_NO_TEXT,
+        ask=strip_hex(line.ask).strip() or DESK_NO_TEXT,
         link=line.link,
         session_fields=fields,
         notes=tuple(notes),
diff --git a/tests/observe/conftest.py b/tests/observe/conftest.py
index f411a67e4..8d9c62908 100644
--- a/tests/observe/conftest.py
+++ b/tests/observe/conftest.py
@@ -354,6 +354,19 @@ def routed_runner_responses(worker, message):
     return respond
 
 
+# A question row of the list on screen: an optional marker (selected glyph, its ASCII form or two
+# spaces), then the age and two spaces. With the per-row "reason unknown" gone from the screen
+# (one title note says it once), this is how a test counts question rows.
+QUESTION_ROW = re.compile(
+    r"^(?:[▸@] |  )?(?:\d+[smhd]|unknown|age unknown \(clock skew\))  \S"
+)
+
+
+def question_rows(lines) -> list[str]:
+    """The question-row lines of a screen, in order."""
+    return [ln for ln in lines if QUESTION_ROW.match(ln)]
+
+
 # -- styled-output helpers (the screen carries SGR from the colour phase on) ------------------------------
 
 _SGR = re.compile(r"\x1b\[([0-9;]*)m")
diff --git a/tests/observe/golden_release1_records.json b/tests/observe/golden_release1_records.json
deleted file mode 100644
index 5d3b520fd..000000000
--- a/tests/observe/golden_release1_records.json
+++ /dev/null
@@ -1,37 +0,0 @@
-{
- "base": {
-  "gap_notice": "Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"",
-  "header1": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE base, not Orca data  scope=all  as of 12:00:00",
-  "header2": "worker-list OK 0s  messages UNVERIFIED (not read)",
-  "record_text": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE base, not Orca data  scope=all  as of 12:00:00\nworker-list OK 0s  messages UNVERIFIED (not read)\ncollected 80 / reported 80  scope=all  source counts: active 54 / reclaimable 0 / retained 13 / released 13  runs seen: 8  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable\nscreen filter: none  historical rows on screen: hidden  (this record lists every collected row)\nHuman questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"\nworker-reported, not questions\ndispatchId=w-001 | run=run-b | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=10s\ndispatchId=w-002 | run=run-c | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=13s\ndispatchId=w-003 | run=run-d | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=16s | flags=FROZEN\ndispatchId=w-004 | run=run-e | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=19s\ndispatchId=w-005 | run=run-f | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=approve | liveness=alive (terminal) | evidenceAge=22s\ndispatchId=w-006 | run=run-g | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=25s\ndispatchId=w-007 | run=run-h | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=28s\ndispatchId=w-008 | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=31s\ndispatchId=w-009 | run=run-b | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=34s\ndispatchId=w-010 | run=run-c | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=37s\ndispatchId=w-011 | run=run-d | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=40s\ndispatchId=w-012 | run=run-e | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=43s\ndispatchId=w-013 | run=run-f | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=46s\ndispatchId=w-014 | run=run-g | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=49s\ndispatchId=w-015 | run=run-h | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=52s\ndispatchId=w-016 | run=run-a | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=55s\ndispatchId=w-017 | run=run-b | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=58s\ndispatchId=w-018 | run=run-c | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-019 | run=run-d | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-020 | run=run-e | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-021 | run=run-f | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-022 | run=run-g | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-023 | run=run-h | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-024 | run=run-a | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-025 | run=run-b | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-026 | run=run-c | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-027 | run=run-d | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-028 | run=run-e | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-029 | run=run-f | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-030 | run=run-g | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-031 | run=run-h | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-032 | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-033 | run=run-b | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-034 | run=run-c | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=1m\ndispatchId=w-035 | run=run-d | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-036 | run=run-e | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-037 | run=run-f | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=1m\ndispatchId=w-038 | run=run-g | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-039 | run=run-h | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-040 | run=run-a | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-041 | run=run-b | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-042 | run=run-c | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-043 | run=run-d | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-044 | run=run-e | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-045 | run=run-f | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-046 | run=run-g | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-047 | run=run-h | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-048 | run=run-a | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-049 | run=run-b | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-050 | run=run-c | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-051 | run=run-d | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-052 | run=run-e | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-053 | run=run-f | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-054 | run=run-g | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-055 | run=run-h | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-056 | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=2m\ndispatchId=w-057 | run=run-b | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=2m\ndispatchId=w-058 | run=run-c | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-059 | run=run-d | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-060 | run=run-e | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-061 | run=run-f | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-062 | run=run-g | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-063 | run=run-h | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-064 | run=run-a | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-065 | run=run-b | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-066 | run=run-c | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-067 | run=run-d | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-068 | run=run-e | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-069 | run=run-f | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-070 | run=run-g | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-071 | run=run-h | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-072 | run=run-a | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-073 | run=run-b | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-074 | run=run-c | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-075 | run=run-d | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-076 | run=run-e | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=3m\ndispatchId=w-077 | run=run-f | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=3m\ndispatchId=w-078 | run=run-g | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=wait | liveness=alive (terminal) | evidenceAge=4m\ndispatchId=w-079 | run=run-h | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=4m\ndispatchId=w-080 | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=4m\n",
-  "snapshot_json": "{\n  \"collection\": {\n    \"changedDuringRead\": false,\n    \"collected\": 80,\n    \"duplicatesIgnored\": 0,\n    \"state\": \"COMPLETE\"\n  },\n  \"counts\": {\n    \"active\": 54,\n    \"reclaimable\": 0,\n    \"released\": 13,\n    \"retained\": 13\n  },\n  \"cycle\": 2,\n  \"generatedAt\": \"2026-11-08T12:00:00Z\",\n  \"page\": {\n    \"hasMore\": false,\n    \"limit\": 100,\n    \"total\": 80\n  },\n  \"producer\": {\n    \"name\": \"superclaude-observe\",\n    \"version\": \"5.0.0\"\n  },\n  \"rows\": [\n    {\n      \"dispatchId\": \"w-001\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-001\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-002\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-002\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-003\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:44Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-003\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-004\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:41Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-004\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-005\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:38Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"approve\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-005\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-006\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:35Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:42Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-006\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-007\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:32Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:39Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-007\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-008\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:29Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:36Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-008\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-009\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:26Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:33Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-009\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-010\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:23Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:30Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-010\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-011\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:20Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:27Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-011\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-012\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:17Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:24Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-012\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-013\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:14Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:21Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-013\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-014\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:11Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:18Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-014\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-015\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:08Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:15Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-015\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-016\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:05Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:12Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-016\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-017\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:02Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:09Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-017\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-018\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:59Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:06Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-018\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-019\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:56Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:03Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-019\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-020\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:53Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:00Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-020\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-021\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:50Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-021\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-022\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:47Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-022\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-023\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:44Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-023\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-024\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:41Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-024\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-025\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:38Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-025\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-026\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:35Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:42Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-026\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-027\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:32Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:39Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-027\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-028\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:29Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:36Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-028\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-029\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:26Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:33Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-029\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-030\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:23Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:30Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-030\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-031\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:20Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:27Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-031\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-032\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:17Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:24Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-032\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-033\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:14Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:21Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-033\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-034\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:58:11Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:18Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-034\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-035\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:08Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:15Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-035\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-036\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:05Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:12Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-036\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-037\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:58:02Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:09Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-037\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-038\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:59Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:06Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-038\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-039\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:56Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:03Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-039\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-040\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:53Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:58:00Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-040\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-041\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-041\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-042\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-042\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-043\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:44Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-043\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-044\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:41Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-044\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-045\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:38Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-045\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-046\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:35Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:42Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-046\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-047\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:32Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:39Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-047\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-048\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:29Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:36Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-048\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-049\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:26Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:33Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-049\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-050\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:23Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:30Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-050\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-051\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:20Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:27Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-051\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-052\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:17Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:24Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-052\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-053\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:14Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:21Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-053\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-054\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:11Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:18Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-054\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-055\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:08Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:15Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-055\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-056\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:57:05Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:12Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-056\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-057\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:57:02Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:09Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-057\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-058\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:59Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:06Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-058\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-059\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:56Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:03Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-059\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-060\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:53Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:57:00Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-060\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-061\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-061\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-062\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-062\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-063\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:44Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-063\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-064\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:41Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-064\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-065\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:38Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-065\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-066\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:35Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:42Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-066\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-067\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:32Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:39Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-067\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-068\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:29Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:36Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-068\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-069\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:26Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:33Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-069\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-070\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:23Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:30Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-070\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-071\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:20Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:27Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-071\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-072\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:17Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:24Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-072\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-073\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:14Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:21Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-b\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-073\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-074\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:11Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:18Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-074\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-075\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:08Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:15Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-d\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-075\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-076\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:56:05Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:12Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-e\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-076\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-077\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:56:02Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:09Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-f\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-077\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-078\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:55:59Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:06Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"wait\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-g\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-078\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    },\n    {\n      \"dispatchId\": \"w-079\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:55:56Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:03Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-h\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-079\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-080\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:55:53Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:56:00Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-080\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    }\n  ],\n  \"schemaVersion\": 1,\n  \"scope\": {\n    \"source\": \"all\"\n  },\n  \"source\": {\n    \"namespace\": \"fixture:base\",\n    \"observedAt\": \"2026-11-08T12:00:00Z\",\n    \"status\": \"OK\"\n  }\n}"
- },
- "empty": {
-  "gap_notice": "Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"",
-  "header1": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE empty, not Orca data  scope=bound  one Run only  as of 12:00:00",
-  "header2": "worker-list OK 0s  messages UNVERIFIED (not read)",
-  "record_text": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE empty, not Orca data  scope=bound  one Run only  as of 12:00:00\nworker-list OK 0s  messages UNVERIFIED (not read)\ncollected 0 / reported 0  scope=bound  source counts: active 0 / reclaimable 0 / retained 0 / released 0  runs seen: 0  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable\nscreen filter: none  historical rows on screen: hidden  (this record lists every collected row)\nHuman questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"\nworker-reported, not questions\nno observed items in this source window; not proof none exist\nworker-list returned 0 workers in scope=bound\n",
-  "snapshot_json": "{\n  \"collection\": {\n    \"changedDuringRead\": false,\n    \"collected\": 0,\n    \"duplicatesIgnored\": 0,\n    \"state\": \"COMPLETE\"\n  },\n  \"counts\": {\n    \"active\": 0,\n    \"reclaimable\": 0,\n    \"released\": 0,\n    \"retained\": 0\n  },\n  \"cycle\": 2,\n  \"generatedAt\": \"2026-11-08T12:00:00Z\",\n  \"page\": {\n    \"hasMore\": false,\n    \"limit\": 100,\n    \"total\": 0\n  },\n  \"producer\": {\n    \"name\": \"superclaude-observe\",\n    \"version\": \"5.0.0\"\n  },\n  \"rows\": [],\n  \"schemaVersion\": 1,\n  \"scope\": {\n    \"source\": \"bound\"\n  },\n  \"source\": {\n    \"namespace\": \"fixture:empty\",\n    \"observedAt\": \"2026-11-08T12:00:00Z\",\n    \"status\": \"OK\"\n  }\n}"
- },
- "injection": {
-  "gap_notice": "Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"",
-  "header1": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE injection, not Orca data  scope=all  as of 12:00:00",
-  "header2": "worker-list OK 0s  messages UNVERIFIED (not read)",
-  "record_text": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE injection, not Orca data  scope=all  as of 12:00:00\nworker-list OK 0s  messages UNVERIFIED (not read)\ncollected 3 / reported 3  scope=all  source counts: active 2 / reclaimable 0 / retained 0 / released 1  runs seen: 3  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable\nscreen filter: none  historical rows on screen: hidden  (this record lists every collected row)\nHuman questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"\nworker-reported, not questions\ndispatchId=w-inj-1 | run=run-a | workerState=link text | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=10s\ndispatchId=w-inj-2 | run=run-c1 | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=bellkind | liveness=alive (terminal) | evidenceAge=13s\ndispatchId=w-inj-3 | run=run-c | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=[bold]x[/bold] | liveness=ended (terminal) | evidenceAge=16s\n",
-  "snapshot_json": "{\n  \"collection\": {\n    \"changedDuringRead\": false,\n    \"collected\": 3,\n    \"duplicatesIgnored\": 0,\n    \"state\": \"COMPLETE\"\n  },\n  \"counts\": {\n    \"active\": 2,\n    \"reclaimable\": 0,\n    \"released\": 1,\n    \"retained\": 0\n  },\n  \"cycle\": 2,\n  \"generatedAt\": \"2026-11-08T12:00:00Z\",\n  \"page\": {\n    \"hasMore\": false,\n    \"limit\": 100,\n    \"total\": 3\n  },\n  \"producer\": {\n    \"name\": \"superclaude-observe\",\n    \"version\": \"5.0.0\"\n  },\n  \"rows\": [\n    {\n      \"dispatchId\": \"w-inj-1\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-001\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"link text\"\n    },\n    {\n      \"dispatchId\": \"w-inj-2\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"bellkind\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"rtl-role\",\n      \"runId\": \"run-c1\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-002\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-inj-3\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:44Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"[bold]x[/bold]\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-c\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"unterminated\"\n      },\n      \"taskId\": \"task with newline\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    }\n  ],\n  \"schemaVersion\": 1,\n  \"scope\": {\n    \"source\": \"all\"\n  },\n  \"source\": {\n    \"namespace\": \"fixture:injection\",\n    \"observedAt\": \"2026-11-08T12:00:00Z\",\n    \"status\": \"OK\"\n  }\n}"
- },
- "missing-fields": {
-  "gap_notice": "Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"",
-  "header1": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE missing-fields, not Orca data  scope unknown  as of 12:00:00",
-  "header2": "worker-list OK 0s  messages UNVERIFIED (not read)",
-  "record_text": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE missing-fields, not Orca data  scope unknown  as of 12:00:00\nworker-list OK 0s  messages UNVERIFIED (not read)\ncollected 5 / reported unknown  scope unknown  source counts: unknown  runs seen: 1+? (1 unknown)  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable\nscreen filter: none  historical rows on screen: hidden  (this record lists every collected row)\nHuman questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"\nworker-reported, not questions\ndispatchId=unknown | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=13s | flags=identity unknown\ndispatchId=w-003 | run=unknown | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=16s\ndispatchId=w-001 | run=run-a | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=unknown | liveness=unknown (unknown) | evidenceAge=10s\ndispatchId=w-004 | run=run-a | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=unknown\ndispatchId=w-005 | run=run-a | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=22s\n",
-  "snapshot_json": "{\n  \"collection\": {\n    \"changedDuringRead\": false,\n    \"collected\": 5,\n    \"duplicatesIgnored\": 0,\n    \"state\": \"COMPLETE\"\n  },\n  \"counts\": \"UNKNOWN\",\n  \"cycle\": 2,\n  \"generatedAt\": \"2026-11-08T12:00:00Z\",\n  \"page\": {\n    \"hasMore\": false,\n    \"limit\": 100,\n    \"total\": \"UNKNOWN\"\n  },\n  \"producer\": {\n    \"name\": \"superclaude-observe\",\n    \"version\": \"5.0.0\"\n  },\n  \"rows\": [\n    {\n      \"absentFields\": [\n        \"dispatchId\"\n      ],\n      \"dispatchId\": \"UNKNOWN\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-002\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"absentFields\": [\n        \"runId\",\n        \"taskId\"\n      ],\n      \"dispatchId\": \"w-003\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:44Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"UNKNOWN\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"UNKNOWN\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"absentFields\": [\n        \"liveness.observedAt\",\n        \"liveness.source\",\n        \"liveness.verdict\",\n        \"nextAction\"\n      ],\n      \"dispatchId\": \"w-001\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"UNKNOWN\",\n        \"source\": \"UNKNOWN\",\n        \"verdict\": \"UNKNOWN\"\n      },\n      \"nextAction\": \"UNKNOWN\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-001\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"absentFields\": [\n        \"evidence.durable\",\n        \"evidence.lastObservedAt\",\n        \"evidence.liveStatus\"\n      ],\n      \"dispatchId\": \"w-004\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": \"UNKNOWN\",\n        \"lastObservedAt\": \"UNKNOWN\",\n        \"liveStatus\": \"UNKNOWN\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-004\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-005\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:38Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-005\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    }\n  ],\n  \"schemaVersion\": 1,\n  \"scope\": \"UNKNOWN\",\n  \"source\": {\n    \"namespace\": \"fixture:missing-fields\",\n    \"observedAt\": \"2026-11-08T12:00:00Z\",\n    \"status\": \"OK\"\n  }\n}"
- },
- "source-loss": {
-  "gap_notice": "Human questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"",
-  "header1": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE source-loss, not Orca data  scope=all  as of 12:00:00",
-  "header2": "worker-list OK 0s  messages UNVERIFIED (not read)",
-  "record_text": "ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE source-loss, not Orca data  scope=all  as of 12:00:00\nworker-list OK 0s  messages UNVERIFIED (not read)\ncollected 5 / reported 5  scope=all  source counts: active 3 / reclaimable 0 / retained 1 / released 1  runs seen: 1  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost unavailable\nscreen filter: none  historical rows on screen: hidden  (this record lists every collected row)\nHuman questions: source UNVERIFIED, 0 rows interpreted, not \"no questions\"\nworker-reported, not questions\ndispatchId=w-001 | run=run-a | workerState=idle | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=10s\ndispatchId=w-002 | run=run-a | workerState=blocked | dispatchStatus=blocked | terminalState=active | outcome=none | nextAction=review | liveness=alive (terminal) | evidenceAge=13s\ndispatchId=w-003 | run=run-a | workerState=exited | dispatchStatus=completed | terminalState=released | outcome=succeeded | nextAction=none | liveness=ended (terminal) | evidenceAge=16s\ndispatchId=w-004 | run=run-a | workerState=exited | dispatchStatus=failed | terminalState=retained | outcome=failed | nextAction=retry | liveness=ended (terminal) | evidenceAge=19s\ndispatchId=w-005 | run=run-a | workerState=running | dispatchStatus=active | terminalState=active | outcome=none | nextAction=none | liveness=alive (terminal) | evidenceAge=22s\n",
-  "snapshot_json": "{\n  \"collection\": {\n    \"changedDuringRead\": false,\n    \"collected\": 5,\n    \"duplicatesIgnored\": 0,\n    \"state\": \"COMPLETE\"\n  },\n  \"counts\": {\n    \"active\": 3,\n    \"reclaimable\": 0,\n    \"released\": 1,\n    \"retained\": 1\n  },\n  \"cycle\": 2,\n  \"generatedAt\": \"2026-11-08T12:00:00Z\",\n  \"page\": {\n    \"hasMore\": false,\n    \"limit\": 100,\n    \"total\": 5\n  },\n  \"producer\": {\n    \"name\": \"superclaude-observe\",\n    \"version\": \"5.0.0\"\n  },\n  \"rows\": [\n    {\n      \"dispatchId\": \"w-001\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:50Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:57Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-001\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"idle\"\n    },\n    {\n      \"dispatchId\": \"w-002\",\n      \"dispatchStatus\": \"blocked\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:47Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:54Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"review\",\n      \"outcome\": \"none\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"blocked\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-002\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"blocked\"\n    },\n    {\n      \"dispatchId\": \"w-003\",\n      \"dispatchStatus\": \"completed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:44Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:51Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"succeeded\",\n      \"provider\": \"claude\",\n      \"role\": \"reviewer\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"completed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-003\",\n      \"terminalState\": \"released\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-004\",\n      \"dispatchStatus\": \"failed\",\n      \"evidence\": {\n        \"durable\": true,\n        \"lastObservedAt\": \"2026-11-08T11:59:41Z\",\n        \"liveStatus\": \"ended\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:48Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"ended\"\n      },\n      \"nextAction\": \"retry\",\n      \"outcome\": \"failed\",\n      \"provider\": \"codex\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"failed\",\n        \"worker\": \"waiting\"\n      },\n      \"taskId\": \"t-004\",\n      \"terminalState\": \"retained\",\n      \"workerState\": \"exited\"\n    },\n    {\n      \"dispatchId\": \"w-005\",\n      \"dispatchStatus\": \"active\",\n      \"evidence\": {\n        \"durable\": false,\n        \"lastObservedAt\": \"2026-11-08T11:59:38Z\",\n        \"liveStatus\": \"live\"\n      },\n      \"hostId\": \"host-local\",\n      \"hostKind\": \"local\",\n      \"liveness\": {\n        \"observedAt\": \"2026-11-08T11:59:45Z\",\n        \"source\": \"terminal\",\n        \"verdict\": \"alive\"\n      },\n      \"nextAction\": \"none\",\n      \"outcome\": \"none\",\n      \"provider\": \"claude\",\n      \"role\": \"worker\",\n      \"runId\": \"run-a\",\n      \"stage\": {\n        \"dispatch\": \"active\",\n        \"worker\": \"coding\"\n      },\n      \"taskId\": \"t-005\",\n      \"terminalState\": \"active\",\n      \"workerState\": \"running\"\n    }\n  ],\n  \"schemaVersion\": 1,\n  \"scope\": {\n    \"source\": \"all\"\n  },\n  \"source\": {\n    \"namespace\": \"fixture:source-loss\",\n    \"observedAt\": \"2026-11-08T12:00:00Z\",\n    \"status\": \"OK\"\n  }\n}"
- }
-}
\ No newline at end of file
diff --git a/tests/observe/live_child.py b/tests/observe/live_child.py
deleted file mode 100644
index 7f040265e..000000000
--- a/tests/observe/live_child.py
+++ /dev/null
@@ -1,41 +0,0 @@
-"""Live-screen child: draws one questions screen through the real ``LiveScreen`` on a pty.
-
-Run only by ``test_live_screen_pty.py``. It reads the terminal size and the environment the way
-the command does (``detect_size``, ``resolve_policy``), draws once, prints ``LIVE_READY`` and
-waits for one line on stdin, then closes the screen so the alternate screen is left cleanly.
-"""
-
-from __future__ import annotations
-
-import os
-import sys
-from pathlib import Path
-
-sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
-
-from superclaude.cli.observe.commands import LiveScreen  # noqa: E402
-from superclaude.cli.observe.terminal import (  # noqa: E402
-    detect_size,
-    output_encoding,
-    resolve_policy,
-)
-from tests.observe.conftest import FakeClock  # noqa: E402
-from tests.observe.test_render import r3_rows, r3_screen  # noqa: E402
-
-
-def main() -> int:
-    width, height = detect_size()
-    policy = resolve_policy(os.environ, output_encoding(), {}, width, height)
-    rows = r3_rows([("w-001", "first?"), ("w-002", "second?"), ("w-003", "third?")])
-    _, view = r3_screen(FakeClock(), rows, 1, width, height)
-    screen = LiveScreen()
-    screen.draw(view, policy, None)
-    sys.stdout.write("LIVE_READY\n")
-    sys.stdout.flush()
-    sys.stdin.readline()
-    screen.close()
-    return 0
-
-
-if __name__ == "__main__":
-    raise SystemExit(main())
diff --git a/tests/observe/test_commands.py b/tests/observe/test_commands.py
index 887729b61..58dfdb59e 100644
--- a/tests/observe/test_commands.py
+++ b/tests/observe/test_commands.py
@@ -668,8 +668,10 @@ def test_with_the_guard_open_one_template_message_call_follows_the_worker_list_c
     worker = [a for a in argv_log if a[1:3] == ["orchestration", "worker-list"]]
     assert len(worker) == 1 and "--peek" not in message[0]
     lines = out.splitlines()
-    assert "COORDINATOR QUESTIONS" in lines and f"one Run only: {QRUN}" in lines
-    assert sum("reason unknown" in l for l in lines) == 4
+    assert any(l.startswith("COORDINATOR QUESTIONS") for l in lines)
+    assert f"one Run only: {QRUN}" in lines
+    # The piped text form is the record form: one msg_ row per question, reason kept per row.
+    assert len([ln for ln in lines if ln.startswith("msg_")]) == 4
     assert (
         "seen, not resolved: 4 | closed by evidence: unavailable (no source)" in lines
     )
@@ -688,7 +690,8 @@ def test_with_the_guard_open_and_a_width_the_screen_shows_the_panel(
     code, out = once(Options(once=True, run_id=QRUN, questions=True, width=116), deps)
     lines = out.splitlines()
     assert code == 0 and all(cell_len(l) <= 116 for l in lines)
-    assert "COORDINATOR QUESTIONS" in lines and GAP_NOTICE not in lines
+    assert any(l.startswith("COORDINATOR QUESTIONS") for l in lines)
+    assert GAP_NOTICE not in lines
 
 
 def test_questions_without_a_run_or_with_a_fixture_or_a_bad_run_is_refused_with_no_call(
diff --git a/tests/observe/test_golden_contract.py b/tests/observe/test_golden_contract.py
index 71fd02479..cccc13b55 100644
--- a/tests/observe/test_golden_contract.py
+++ b/tests/observe/test_golden_contract.py
@@ -370,6 +370,7 @@ from tests.observe import record_golden_questions  # noqa: E402
 from tests.observe.conftest import (  # noqa: E402
     make_envelope,
     make_rows,
+    question_rows,
     routed_runner_responses,
 )
 
@@ -428,8 +429,8 @@ def test_t55_the_success_sample_parses_to_its_two_questions_at_every_width(fake_
     for width in (160, 116, 80):
         lines = screen_lines(view, policy(width))
         assert all(cell_len(line) <= width for line in lines)
-        assert "COORDINATOR QUESTIONS" in lines
-        assert sum("reason unknown" in line for line in lines) == 2
+        assert any(line.startswith("COORDINATOR QUESTIONS") for line in lines)
+        assert len(question_rows(lines)) == 2
 
 
 def test_t55_the_missing_sample_fails_by_shape_then_by_no_active_terminal_and_keeps_questions(
diff --git a/tests/observe/test_height_budget.py b/tests/observe/test_height_budget.py
deleted file mode 100644
index 444a40047..000000000
--- a/tests/observe/test_height_budget.py
+++ /dev/null
@@ -1,26 +0,0 @@
-"""The questions-on screen never has more rows than the terminal (pins today's height budget).
-
-On ``Live(screen=True)`` rows past ``policy.height`` are dropped from the bottom, which are the
-footer keys and the ``shown x/y`` line, with no warning. Every phase that adds rows (frames, a
-count strip, a RETAIN CONTEXT pane) keeps this test green.
-"""
-
-from __future__ import annotations
-
-import pytest
-
-from tests.observe.test_render import WIDTHS, policy_for, r3_rows, r3_screen
-
-HEIGHTS = (24, 40, 44)
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-@pytest.mark.parametrize("height", HEIGHTS)
-@pytest.mark.parametrize("count", (3, 20))
-def test_questions_on_screen_fits_the_height(fake_clock, width, height, count):
-    rows = r3_rows([("w-001", f"question {i}?") for i in range(count)])
-    lines, _ = r3_screen(fake_clock, rows, 0, width, height=height)
-    policy = policy_for(width, height=height)
-    assert len(lines) <= policy.height or policy.too_small, (
-        f"{len(lines)} rows at height {height}, width {width}"
-    )
diff --git a/tests/observe/test_live_screen_pty.py b/tests/observe/test_live_screen_pty.py
deleted file mode 100644
index 009a9137f..000000000
--- a/tests/observe/test_live_screen_pty.py
+++ /dev/null
@@ -1,93 +0,0 @@
-"""The real ``LiveScreen`` on a pty: alternate screen, colour depth, no blink, no mouse (Q5 live gate).
-
-``Console(file=StringIO)`` writes nothing under ``Live(screen=True)``, so the live path is only
-checked on a real pseudo-terminal. The child is ``live_child.py``.
-"""
-
-from __future__ import annotations
-
-import os
-import re
-import sys
-from pathlib import Path
-
-import pytest
-
-pexpect = pytest.importorskip("pexpect")
-pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX pty test")
-
-CHILD = Path(__file__).with_name("live_child.py")
-ROOT = Path(__file__).resolve().parents[2]
-SGR = re.compile(rb"\x1b\[([0-9;]*)m")
-MOUSE = (b"\x1b[?1000h", b"\x1b[?1002h", b"\x1b[?1003h", b"\x1b[?1006h")
-
-
-def run_child(env_extra: dict, rows: int = 40, cols: int = 160) -> bytes:
-    """Everything the live screen wrote to the terminal, from start to a clean exit."""
-    env = {
-        k: v
-        for k, v in os.environ.items()
-        if k not in ("COLUMNS", "LINES", "NO_COLOR", "COLORTERM", "TERM")
-    }
-    env["TERM"] = "xterm"
-    env.update(env_extra)
-    child = pexpect.spawn(
-        sys.executable,
-        [str(CHILD)],
-        env=env,
-        dimensions=(rows, cols),
-        encoding=None,
-        cwd=str(ROOT),
-        timeout=60,
-    )
-    child.expect(b"LIVE_READY")
-    before = child.before + b"LIVE_READY"
-    child.sendline(b"")
-    child.expect(pexpect.EOF)
-    return before + child.before
-
-
-def sgr_codes(data: bytes) -> list[int]:
-    """Every SGR code in ``data``; the arguments of extended colours (38 and 48) are skipped."""
-    codes: list[int] = []
-    for match in SGR.finditer(data):
-        params = [int(p) if p else 0 for p in match.group(1).split(b";")]
-        i = 0
-        while i < len(params):
-            if params[i] in (38, 48) and i + 1 < len(params):
-                i += 3 if params[i + 1] == 5 else 5
-                continue
-            codes.append(params[i])
-            i += 1
-    return codes
-
-
-def test_the_live_screen_uses_the_alternate_screen_and_no_mouse_or_blink():
-    out = run_child({})
-    assert b"\x1b[?1049h" in out and b"\x1b[?1049l" in out  # entered and left cleanly
-    assert not any(seq in out for seq in MOUSE)
-    assert not {5, 6} & set(sgr_codes(out))  # no blink
-
-
-def test_a_truecolor_terminal_gets_the_mockup_palette():
-    out = run_child({"COLORTERM": "truecolor"})
-    assert b"38;2;" in out
-
-
-def test_a_256_colour_terminal_gets_indexed_colours_only():
-    out = run_child({"TERM": "xterm-256color"})
-    assert b"38;5;" in out and b"38;2;" not in out
-
-
-def test_a_16_colour_terminal_gets_only_16_colour_codes():
-    out = run_child({})
-    codes = sgr_codes(out)
-    assert codes and b"38;2;" not in out and b"38;5;" not in out
-    assert all(c in (0, 1, 22) or 30 <= c <= 37 or 90 <= c <= 97 for c in codes)
-
-
-def test_no_color_writes_no_colour_or_weight_codes():
-    out = run_child({"NO_COLOR": "1", "COLORTERM": "truecolor"})
-    assert b"\x1b[?1049h" in out
-    # Measured: with NO_COLOR the console sets no style at all, so no SGR sequence is written.
-    assert sgr_codes(out) == []
diff --git a/tests/observe/test_render.py b/tests/observe/test_render.py
index 6fa4992d8..2ea236098 100644
--- a/tests/observe/test_render.py
+++ b/tests/observe/test_render.py
@@ -454,7 +454,7 @@ def test_t19_the_screen_carries_the_title_disclosure_and_one_line_per_question(
         "retention reset at 12:00; questions observed before this start are not retained"
         in flat
     )
-    assert sum("reason unknown" in l for l in lines) == 5
+    assert len(question_rows(lines)) == 5
     assert "synthetic body" not in flat and GAP_NOTICE not in lines
     assert all(cell_len(l) <= width for l in lines)
 
@@ -482,7 +482,7 @@ def test_a_long_question_list_is_windowed_with_x_of_y_shown(fake_clock):
     lines = screen_lines(build_view(result, Session(), fake_clock), policy)
     shown = [l for l in lines if l.startswith("questions shown ") and "of 60" in l]
     assert len(shown) == 1 and len(lines) <= 30
-    assert sum("reason unknown" in l for l in lines) < 60
+    assert len(question_rows(lines)) < 60
     assert any(
         l.startswith("collected") or "collected 4" in l for l in lines
     )  # counts stay
@@ -519,7 +519,7 @@ def test_the_fenced_state_names_the_sentence_and_keeps_the_retained_lines(fake_c
     lines = screen_lines(build_view(second, Session(), fake_clock), policy_for(160))
     flat = " ".join(lines)
     assert "FAILED (consumer-fenced)" in flat and QUESTIONS_NOT_HELD in flat
-    assert sum("reason unknown" in l for l in lines) == 2
+    assert len(question_rows(lines)) == 2
     assert "seen, not resolved: 2 |" in flat and first.question_state == "OK"
 
 
@@ -532,7 +532,7 @@ def test_t12_a_question_that_left_the_window_stays_listed_on_screen(fake_clock):
         build_view(collector.run_once(), Session(), fake_clock), policy_for(160)
     )
     assert sum("no longer in source window" in l for l in lines) == 1
-    assert sum("reason unknown" in l for l in lines) == 3
+    assert len(question_rows(lines)) == 3
 
 
 def test_an_empty_good_read_screen_says_not_proof_and_never_no_questions(fake_clock):
@@ -589,7 +589,7 @@ def test_the_inspector_keeps_room_by_showing_only_the_one_line_summary(fake_cloc
     lines = screen_lines(view, policy_for(120, height=30))
     flat = "".join("".join(lines).split())
     assert view.focus == "inspector" and "".join(view.gap_notice.split()) in flat
-    assert not any("reason unknown" in l for l in lines)
+    assert not question_rows(lines)  # the inspector shows no question rows
 
 
 def test_ascii_mode_renders_only_ascii_for_a_non_ascii_subject(fake_clock):
@@ -674,7 +674,7 @@ def test_decision_1_when_cut_the_oldest_questions_stay_and_the_screen_says_so(
     cut = [ln for ln in lines if ln.startswith("questions shown ")]
     assert len(cut) == 1 and "oldest first" in cut[0] and "newer not shown" in cut[0]
     assert "e exports all" in cut[0]
-    shown = [ln for ln in lines if "reason unknown" in ln]
+    shown = question_rows(lines)
     oldest = sorted(r["created_at"] for r in rows)[0]
     assert shown and view.questions.lines[0].created_at == oldest
     assert (
@@ -693,9 +693,7 @@ def test_decision_2_the_questions_win_on_a_short_terminal_the_ledger_is_squeezed
     )
     view = build_view(result, Session(), fake_clock)
     lines = screen_lines(view, policy_for(120, height=26))
-    assert (
-        sum("reason unknown" in ln for ln in lines) == 8
-    )  # every question is shown ...
+    assert len(question_rows(lines)) == 8  # every question is shown ...
     ledger_rows = [ln for ln in lines if " w-0" in ln]
     assert (
         1 <= len(ledger_rows) <= 3
@@ -862,7 +860,8 @@ def test_the_latest_empty_read_is_said_when_older_rows_are_listed(fake_clock):
         )
     )
     assert "latest read returned 0 questions; the rows below are older" in flat
-    assert flat.count("reason unknown") == 2 and "no questions" not in flat.lower()
+    assert "reasons: none in source" in flat and "no questions" not in flat.lower()
+    assert "reason unknown" not in flat  # said once in the title, not per row
     assert dataclasses.is_dataclass(result)
 
 
@@ -955,15 +954,16 @@ def test_r3_each_unlinked_text_shows_in_the_desk(fake_clock, payload, sender, re
 
 
 @pytest.mark.parametrize("width", (116, 80))
-def test_r3_every_linked_question_line_keeps_age_state_and_reason_unknown(
+def test_r3_every_linked_question_line_keeps_age_and_state_and_has_no_per_row_reason(
     fake_clock, width
 ):
     rows = r3_rows([("w-001", "x" * 300), ("w-002", "short?")])
     lines, _ = r3_screen(fake_clock, rows, None, width, height=60)
-    question_lines = [ln for ln in lines if "reason unknown" in ln]
+    question_lines = question_rows(lines)
     assert len(question_lines) == 2
-    for ln in question_lines:
-        assert ln.endswith("reason unknown") and cell_len(ln) <= width
+    assert all(cell_len(ln) <= width for ln in question_lines)
+    assert not any("reason unknown" in ln for ln in lines)
+    assert "reasons: none in source" in flat_of(lines)  # one title note instead
     assert "..." in question_lines[0] or "x" * 20 in question_lines[0]
     assert re.match(r"^\s*\d+[smh]  ", question_lines[0])  # the age stays
 
@@ -973,7 +973,7 @@ def test_r3_a_long_question_shows_a_visible_mark_in_the_desk_and_on_the_list(
 ):
     rows = r3_rows([("w-001", "word " * 200)])
     lines, view = r3_screen(fake_clock, rows, 0, 160, height=60)
-    listed = [ln for ln in lines if ln.endswith("reason unknown")]
+    listed = question_rows(lines)
     assert listed and "..." in listed[0]
     desk = lines[lines.index(DESK_TITLE) :]
     text_lines = desk[
@@ -1021,7 +1021,7 @@ def test_r3_the_desk_gives_way_to_its_notice_and_the_list_is_kept(fake_clock):
     for height in range(8, 61):
         lines, _ = r3_screen(fake_clock, rows, 0, 116, height=height)
         flat = flat_of(lines)
-        listed = sum("reason unknown" in ln for ln in lines)
+        listed = len(question_rows(lines))
         if DESK_TITLE in lines:
             seen["desk"] += 1
             assert listed >= 1 and DESK_HIDDEN not in flat  # the list keeps a line
@@ -1053,7 +1053,7 @@ def test_r3_the_link_on_keys_line_is_shown_only_with_the_link_on(fake_clock):
 # -- Q7: a plan-approval ask with a 64-hex hash and paths in the Decision Desk (pins today's behaviour) ------------------
 
 from superclaude.cli.observe.export import record_text, snapshot_json  # noqa: E402
-from tests.observe.conftest import sgr_params, strip_sgr  # noqa: E402
+from tests.observe.conftest import question_rows, sgr_params, strip_sgr  # noqa: E402
 
 HASH = "0123456789abcdef" * 4
 # Twin of PLAN_ASK in .dev/issues/409/visual-parity/inputs/tools/render_current.py: keep the two identical.
@@ -1086,32 +1086,75 @@ def test_r3_a_plan_ask_with_a_64_hex_hash_and_paths_wraps_cleanly_in_the_desk(
     assert all(cell_len(ln) <= width for ln in lines)
     text = desk_text_lines(lines)
     assert 1 <= len(text) <= 4 and not text[-1].endswith("...")
-    assert sum(HASH in ln for ln in text) == 1  # the hash stays whole on one desk line
-    assert "".join(text).replace(" ", "") == PLAN_ASK.replace(" ", "")  # nothing lost
+    assert not any(HASH in ln for ln in lines)  # no hash anywhere on the screen
+    assert "".join(text).replace(" ", "") == PLAN_ASK.replace(f"{HASH}", "").replace(
+        " ", ""
+    )  # the rest of the ask is intact
     assert HASH not in record_text(view) and HASH not in snapshot_json(view)  # canary
 
 
 @pytest.mark.parametrize("width", WIDTHS)
-def test_r3_a_hash_after_a_long_path_list_is_cut_with_a_mark_at_80_and_116_columns(
-    fake_clock, width
-):
+def test_r3_a_hash_after_a_long_path_list_never_reaches_the_screen(fake_clock, width):
     assert len(PATHS_THEN_HASH) <= 400  # the parse cap (ASK_CAP) does not cut it
     rows = r3_rows([("w-001", PATHS_THEN_HASH)])
     lines, view = r3_screen(fake_clock, rows, 0, width, height=70)
     assert all(cell_len(ln) <= width for ln in lines)
+    assert not any(HASH in ln for ln in lines)
     text = desk_text_lines(lines)
-    if width in (
-        80,
-        116,
-    ):  # D-6 exception: four lines cut the ask, so the hash is not shown
+    shown = PATHS_THEN_HASH.replace(f" {HASH}", "")  # 327 characters
+    if width == 80:  # four lines of 80 columns cut the ask with a mark
         assert len(text) == 4 and text[-1].endswith("...")
-        assert not any(HASH in ln for ln in lines if not ln.startswith("▸ "))
     else:  # wide enough for the whole ask inside four lines
-        assert sum(HASH in ln for ln in text) == 1
-        assert "".join(text).replace(" ", "") == PATHS_THEN_HASH.replace(" ", "")
+        assert not text[-1].endswith("...")
+        assert "".join(text).replace(" ", "") == shown.replace(" ", "")
     assert HASH not in record_text(view) and HASH not in snapshot_json(view)  # canary
 
 
+def test_strip_hex_removes_only_runs_of_32_or_more_hex_digits_and_collapses_spaces():
+    from superclaude.cli.observe.view import strip_hex
+
+    assert strip_hex(f"plan hash {HASH} ok") == "plan hash ok"
+    assert strip_hex(f"(plan hash {HASH})?") == "(plan hash )?"
+    assert strip_hex(HASH) == ""
+    assert strip_hex("a" * 31) == "a" * 31  # 31 is not a hash
+    assert strip_hex("deadbeef cafe 1234") == "deadbeef cafe 1234"  # short words stay
+    assert strip_hex("x" + "a" * 32) == "x"  # a long run is removed even inside a word
+
+
+@pytest.mark.parametrize("width", WIDTHS)
+def test_reasons_are_said_once_in_the_title_and_not_on_every_row(fake_clock, width):
+    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
+    lines, view = r3_screen(fake_clock, rows, 0, width, height=70)
+    plain = [strip_sgr(ln) for ln in lines]
+    assert not any("reason unknown" in ln for ln in plain)
+    assert sum("reasons: none in source" in ln for ln in plain) == 1
+    title = next(
+        i for i, ln in enumerate(plain) if ln.startswith("COORDINATOR QUESTIONS")
+    )
+    assert "reasons: none in source" in "".join(plain[title : title + 2])
+    assert len(question_rows(plain)) == 2
+    assert "reason unknown" in record_text(view)  # the record keeps its wording
+
+
+def test_a_row_with_a_reason_shows_it_and_the_title_note_goes(fake_clock):
+    rows = r3_rows([("w-001", "first?"), ("w-002", "second?")])
+    lines, view = r3_screen(fake_clock, rows, 0, 160, height=70)
+    panel = view.questions
+    with_reason = dataclasses.replace(
+        panel,
+        lines=[
+            dataclasses.replace(panel.lines[0], reason="needs a sign-off"),
+            *panel.lines[1:],
+        ],
+    )
+    shown = screen_lines(
+        dataclasses.replace(view, questions=with_reason), policy_for(160, height=70)
+    )
+    plain = [strip_sgr(ln) for ln in shown]
+    assert sum("needs a sign-off" in ln for ln in plain) == 1
+    assert not any("reasons: none in source" in ln for ln in plain)
+
+
 @pytest.mark.parametrize("width", WIDTHS)
 def test_r3_a_120_character_worktree_id_continues_on_two_cell_indented_lines(
     fake_clock, width
@@ -1247,11 +1290,13 @@ def test_a_selected_question_is_one_bold_amber_line_and_the_others_have_parts(
     selected = next(ln for ln in lines if ln.plain.startswith("▸ "))
     assert roles_at(selected, "second?") == {"selected"}
     assert roles_at(selected, "▸") == {"selected"}
-    assert roles_at(selected, "reason unknown") == {"muted"}  # absent stays muted
+    assert "reason unknown" not in selected.plain  # said once in the title note
     other = first_line(lines, "first?")
     assert roles_at(other, "first?") == {"body_bold"}
-    assert roles_at(other, "reason unknown") == {"muted"}
     assert roles_at(other, other.plain.strip().split()[0]) == {"attention"}  # the age
+    title = first_line(lines, "COORDINATOR QUESTIONS")
+    assert roles_at(title, "COORDINATOR") == {"attention_title"}
+    assert roles_at(title, "reasons: none in source") == {"muted"}
 
 
 def test_absent_values_are_muted_and_state_words_follow_the_table(fake_clock):
@@ -1397,7 +1442,9 @@ def test_the_read_only_badge_is_right_aligned_once_and_every_line_fits(
     assert index <= 1  # the title wraps to at most two lines
     assert cell_len(badged[0]) == width and badged[0].endswith(READ_ONLY_BADGE)
     title = " ".join(lines[: index + 1]).replace(READ_ONLY_BADGE, "")
-    assert " ".join(title.split()) == " ".join(view.header1.split())  # title text unedited
+    assert " ".join(title.split()) == " ".join(
+        view.header1.split()
+    )  # title text unedited
     assert all(cell_len(ln) <= width for ln in lines)
 
 
diff --git a/tests/observe/test_styled_capture.py b/tests/observe/test_styled_capture.py
deleted file mode 100644
index 51ca96474..000000000
--- a/tests/observe/test_styled_capture.py
+++ /dev/null
@@ -1,83 +0,0 @@
-"""The one-shot path can carry the screen's colour and weight; the capture is never export_text(styles=True)."""
-
-from __future__ import annotations
-
-import io
-
-import pytest
-
-from superclaude.cli.observe.commands import (
-    Options,
-    _screen_text,
-    _stdout_is_tty,
-    execute,
-)
-from superclaude.cli.observe.terminal import resolve_policy
-from tests.observe.conftest import strip_sgr
-from tests.observe.test_commands import deps_for
-from tests.observe.test_render import WIDTHS, fixture_view
-
-
-class _Tty(io.StringIO):
-    def isatty(self) -> bool:
-        return True
-
-
-def _policy(width, env=None, ascii=False):
-    return resolve_policy(env or {}, "utf-8", {"ascii": ascii}, width, 40)
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-def test_a_styled_screen_has_escapes_and_the_same_text_as_the_plain_one(
-    fake_clock, width
-):
-    view = fixture_view("base", fake_clock)
-    policy = _policy(width)
-    styled = _screen_text(view, policy, styled=True)
-    plain = _screen_text(view, policy, styled=False)
-    assert "\x1b[" in styled
-    assert strip_sgr(styled) == plain and "\x1b" not in plain
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-def test_no_color_gives_zero_escape_bytes_even_when_styled_is_asked_for(
-    fake_clock, width
-):
-    view = fixture_view("base", fake_clock)
-    out = _screen_text(view, _policy(width, {"NO_COLOR": "1"}), styled=True)
-    assert "\x1b" not in out
-
-
-@pytest.mark.parametrize("width", WIDTHS)
-def test_ascii_stays_ascii_with_colour_on(fake_clock, width):
-    view = fixture_view("long-identifiers", fake_clock)
-    out = _screen_text(view, _policy(width, ascii=True), styled=True)
-    assert "\x1b[" in out and out.isascii()
-
-
-def test_the_styled_capture_follows_the_colour_depth(fake_clock):
-    view = fixture_view("base", fake_clock)
-    truecolor = _screen_text(
-        view, _policy(160, {"COLORTERM": "truecolor"}), styled=True
-    )
-    standard = _screen_text(view, _policy(160), styled=True)
-    assert "38;2;" in truecolor and "38;2;" not in standard
-
-
-def test_a_piped_one_shot_stays_plain_and_a_terminal_one_is_styled(fake_clock):
-    options = Options(once=True, fixture="base", width=160)
-    piped = deps_for(fake_clock)  # a StringIO: not a terminal
-    assert execute(options, piped) == 0 and "\x1b" not in piped.stdout.getvalue()
-    tty = deps_for(fake_clock, stdout=_Tty())
-    assert execute(options, tty) == 0 and "\x1b[" in tty.stdout.getvalue()
-    quiet = deps_for(fake_clock, stdout=_Tty(), env={"NO_COLOR": "1"})
-    assert execute(options, quiet) == 0 and "\x1b" not in quiet.stdout.getvalue()
-    assert strip_sgr(tty.stdout.getvalue()) == piped.stdout.getvalue()
-
-
-def test_a_stream_without_isatty_counts_as_not_a_terminal(fake_clock):
-    class _Bare:
-        def write(self, text):
-            return len(text)
-
-    assert _stdout_is_tty(deps_for(fake_clock, stdout=_Bare())) is False
diff --git a/tests/observe/test_theme.py b/tests/observe/test_theme.py
deleted file mode 100644
index 8add9681d..000000000
--- a/tests/observe/test_theme.py
+++ /dev/null
@@ -1,95 +0,0 @@
-"""Colour roles: every role exists at every depth, the 16-colour floor keeps its roles apart."""
-
-from __future__ import annotations
-
-import pytest
-
-from superclaude.cli.observe import theme
-from superclaude.cli.observe.theme import (
-    FROZEN_ROLE,
-    ROLES,
-    STATE_ROLE,
-    style_for,
-)
-
-DEPTHS = ("standard", "256", "truecolor")
-# One role per palette colour, so eight distinct colours means eight distinct roles (RB-09).
-PALETTE_ROLES = (
-    "attention",  # amber
-    "identity",  # base
-    "secondary",  # slate
-    "muted",
-    "state_running",  # green
-    "state_settled",  # cyan
-    "state_failed",  # red
-    "state_frozen",  # violet
-)
-
-
-@pytest.mark.parametrize("depth", DEPTHS)
-def test_every_role_has_a_style_at_every_depth(depth):
-    for role in ROLES:
-        assert style_for(role, depth) is not None
-
-
-def test_no_depth_means_no_style():
-    assert all(style_for(role, None) is None for role in ROLES)
-
-
-def test_an_unknown_role_is_an_error_not_a_silent_default():
-    with pytest.raises(KeyError):
-        style_for("nonsense", "standard")
-
-
-def test_the_eight_palette_roles_keep_eight_distinct_colours_at_16_colours():
-    numbers = [style_for(role, "standard").color.number for role in PALETTE_ROLES]
-    assert len(set(numbers)) == 8
-
-
-def test_the_four_state_roles_have_four_different_codes_at_16_colours():
-    roles = ("state_running", "state_settled", "state_failed", "state_frozen")
-    codes = {style_for(role, "standard").color.number for role in roles}
-    assert len(codes) == 4
-
-
-def test_the_state_table_is_not_empty_and_names_the_minimum_keys():
-    required = [
-        ("workerState", "running"),
-        ("workerState", "succeeded"),
-        ("workerState", "failed"),
-        ("dispatchStatus", "completed"),
-        ("liveness", "alive"),
-    ]
-    assert all(key in STATE_ROLE for key in required)
-    assert FROZEN_ROLE == "state_frozen"
-    assert all(role in ROLES for role in (*STATE_ROLE.values(), FROZEN_ROLE))
-    # A word the table does not name keeps the body role: it is never classified.
-    assert ("workerState", "blocked") not in STATE_ROLE
-    assert ("terminalState", "released") not in STATE_ROLE
-
-
-def test_no_style_blinks_dims_or_reverses():
-    for depth in DEPTHS:
-        for role in ROLES:
-            style = style_for(role, depth)
-            assert not (style.blink or style.blink2 or style.dim or style.reverse)
-
-
-def test_styles_are_distinct_objects_per_depth_and_cached_per_depth():
-    standard = style_for("attention", "standard")
-    truecolor = style_for("attention", "truecolor")
-    assert standard is not truecolor and standard != truecolor
-    assert style_for("attention", "standard") is standard
-    assert truecolor.color.get_truecolor().hex == "#fab219"
-
-
-def test_the_theme_module_holds_no_terminal_facts():
-    text = open(theme.__file__, encoding="utf-8").read()
-    for literal in (
-        "Console(",
-        "NO_COLOR",
-        "COLUMNS",
-        "stdout.encoding",
-        "getpreferredencoding",
-    ):
-        assert literal not in text


Codegraph context: index_state=fresh checked_at=2026-11-18T04:42:32Z worktree_root=issue-606 worktree projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-606
call codegraph only when index_state: fresh, never to widen scope
Q2b ran on the Grep/Read floor: dependents of QuestionLine and DeskView are render.py and export.py (export.py is untouched and reads only qid, text, link, dispatch_id).
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
