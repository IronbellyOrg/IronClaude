6d7416a6b3f7eee6ad6fdf548fe2fd710af2da58
family status-cell-clipped: the merged status cell is narrower than its longest raw values.
search: grep -n -F -e "status" src/superclaude/cli/observe/render.py
before: three column tables (full, line, short) each with a 22-cell status column
coupled sites: the three width values in _columns only
after: 36, 36 and 30 cells; a test checks every non-active triple of the base fixture is whole at 160 and 116
