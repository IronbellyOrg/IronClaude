a47a7bb1e3d1e65ebbaed540aefa159ab0bd7615
family footer-literal: defect form: footer text puts the count before the word (x/y shown) where the spec footer literal is 'shown x/y | collected n / reported T'
command: grep -n -F -e shown -- src/superclaude/cli/observe/view.py tests/observe/test_view.py
before:
src/superclaude/cli/observe/view.py:145:    shown: int
src/superclaude/cli/observe/view.py:147:    more: int  # rows not shown, never counting the selected row
src/superclaude/cli/observe/view.py:148:    text: str  # "x/y shown"
src/superclaude/cli/observe/view.py:191:            shown = rows
src/superclaude/cli/observe/view.py:196:            shown = rows[start : start + capacity]
src/superclaude/cli/observe/view.py:197:        shown_ids = {r.identity for r in shown}
src/superclaude/cli/observe/view.py:200:            1 for r in rows if r.identity not in shown_ids and r.identity != selected_id
src/superclaude/cli/observe/view.py:203:            rows=shown,
src/superclaude/cli/observe/view.py:204:            shown=len(shown),
src/superclaude/cli/observe/view.py:207:            text=f"{len(shown)}/{total} shown",
tests/observe/test_view.py:504:    shown = build(result, fake_clock, Session(show_historical=True))
tests/observe/test_view.py:505:    assert shown.historical_note is None and len(shown.visible_rows) == 9
tests/observe/test_view.py:506:    assert {rv.terminal_state for rv in shown.visible_rows} >= {
tests/observe/test_view.py:520:    assert counts(hidden) == counts(shown)  # the toggle never changes source counts
tests/observe/test_view.py:583:    assert window.shown == 10 and window.total == 80 and window.text == "10/80 shown"
tests/observe/test_view.py:586:    assert view.footer(window).endswith("10/80 shown | collected 80 / reported 80")
tests/observe/test_view.py:603:    assert (everything.shown, everything.more, everything.more_text) == (80, 0, "")
tests/observe/test_view.py:604:    assert view.window(500).text == "80/80 shown"
coupled sites: view.py Window.text (x/y shown, overflow text, keep), View.footer (fix), tests/observe/test_view.py footer assertion (update)
after:
src/superclaude/cli/observe/view.py:145:    shown: int
src/superclaude/cli/observe/view.py:147:    more: int  # rows not shown, never counting the selected row
src/superclaude/cli/observe/view.py:148:    text: str  # "x/y shown"
src/superclaude/cli/observe/view.py:191:            shown = rows
src/superclaude/cli/observe/view.py:196:            shown = rows[start : start + capacity]
src/superclaude/cli/observe/view.py:197:        shown_ids = {r.identity for r in shown}
src/superclaude/cli/observe/view.py:200:            1 for r in rows if r.identity not in shown_ids and r.identity != selected_id
src/superclaude/cli/observe/view.py:203:            rows=shown,
src/superclaude/cli/observe/view.py:204:            shown=len(shown),
src/superclaude/cli/observe/view.py:207:            text=f"{len(shown)}/{total} shown",
src/superclaude/cli/observe/view.py:212:        shown = f"shown {window.shown}/{window.total}"  # the footer literal; "x/y shown" is the overflow text
src/superclaude/cli/observe/view.py:213:        return f"{self.help_line}  {shown} | {self.collected_text}"
tests/observe/test_view.py:504:    shown = build(result, fake_clock, Session(show_historical=True))
tests/observe/test_view.py:505:    assert shown.historical_note is None and len(shown.visible_rows) == 9
tests/observe/test_view.py:506:    assert {rv.terminal_state for rv in shown.visible_rows} >= {
tests/observe/test_view.py:520:    assert counts(hidden) == counts(shown)  # the toggle never changes source counts
tests/observe/test_view.py:583:    assert window.shown == 10 and window.total == 80 and window.text == "10/80 shown"
tests/observe/test_view.py:586:    assert view.footer(window).endswith("shown 10/80 | collected 80 / reported 80")
tests/observe/test_view.py:587:    assert "shown 80/80 | collected 80 / reported 80" in view.footer(view.window(None))
tests/observe/test_view.py:604:    assert (everything.shown, everything.more, everything.more_text) == (80, 0, "")
tests/observe/test_view.py:605:    assert view.window(500).text == "80/80 shown"
