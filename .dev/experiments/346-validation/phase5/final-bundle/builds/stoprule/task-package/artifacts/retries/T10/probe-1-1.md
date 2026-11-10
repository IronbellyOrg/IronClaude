cccc8c5f4469bdb87755dabc4963612e0d50ce0c
family drift-filter-too-broad
form: a line-prefix exemption in the drift check hides edits to inherited lines
command: grep -n -e 'startswith' -e 'def is_replaced' -e 'def drift' -e 'x.strip()' -- tests/skills/test_spec_panel_stoprule.py
before:
40:def is_replaced(line):
43:        line.startswith(("name: ", "description: ", "# /sc:spec-panel"))
44:        or line.startswith("/sc:spec-panel")  # Usage and Examples command lines
48:        or line.startswith(
60:def drift(variant_text, base_text):
69:            x for x in base_text.splitlines()[i1:i2] if x.strip() and not is_replaced(x)
74:            if x.strip() and not is_replaced(x)
145:        line = next(ln for ln in body.splitlines() if ln.startswith(rule))
coupled sites: is_replaced, drift, the negative-case tests
after:
55:def drift(variant_text, base_text):
67:        if line.startswith(INSERTED_PREFIXES):
71:        if line.startswith(BULLET8):
88:            and new.startswith(m.group(0))
89:            and (not old.startswith("description: ") or n <= 8)
160:        line = next(ln for ln in body.splitlines() if ln.startswith(rule))
