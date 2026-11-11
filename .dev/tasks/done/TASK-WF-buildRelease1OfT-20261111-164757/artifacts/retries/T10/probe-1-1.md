c20b44431773899e36942d392b4278c16667e94c
family status-literal-in-renderer: defect form: a status literal string written in render.py instead of coming from view.py
command: grep -n -F -e FROZEN -- src/superclaude/cli/observe/render.py src/superclaude/cli/observe/view.py
before:
src/superclaude/cli/observe/render.py:130:    flags = (("FROZEN",) if row.frozen else ()) + row.flags
src/superclaude/cli/observe/view.py:557:    tokens.append(CountsToken(f"POLICY FROZEN {UNAVAILABLE}", False))
coupled sites: render.py _flags_text (fix), view.py _row_view flags (add marker), tests asserting FROZEN in test_view.py and test_render.py
after:
src/superclaude/cli/observe/render.py:130:    return ", ".join(row.flags)  # the view owns every marker, FROZEN included
src/superclaude/cli/observe/view.py:55:FROZEN_MARKER = "FROZEN"  # fixture mode only; no other state overrides it (T34)
src/superclaude/cli/observe/view.py:346:        ((FROZEN_MARKER,) if frozen else ())
src/superclaude/cli/observe/view.py:561:    tokens.append(CountsToken(f"POLICY FROZEN {UNAVAILABLE}", False))
