5e8802f5ce80ba3325b2f1f6b58da66952dcc29f
family=mutation-check-coverage
defect form: a presence check over the whole file instead of the "What never counts" line, and a mutation loop that skips an item
command: grep -n -E "NEVER_COUNTS|not in text|replace\(" tests/skills/test_confirmation_channels.py
before-output:
27:NEVER_COUNTS = (
49:    gaps = [c for c in CHANNELS if c not in text]
50:    gaps += [n for n in NEVER_COUNTS if n not in text]
51:    if TIMING not in text:
54:        if phrase not in text:
78:    assert missing_from_contract(text.replace(TIMING, "")) == [TIMING]
79:    for item in NEVER_COUNTS[1:]:  # "another agent's message" also appears elsewhere
80:        gaps = missing_from_contract(text.replace(item, "x"))
coupled sites: missing_from_contract (the presence check), test_the_checker_fails_when_a_required_piece_is_removed (the mutation loop)
after:
27:NEVER_COUNTS = (
57:    gaps = [c for c in CHANNELS if c not in text]
59:    gaps += [n for n in NEVER_COUNTS if n not in never_line]
60:    if TIMING not in text:
63:        if phrase not in text:
87:    assert missing_from_contract(text.replace(TIMING, "")) == [TIMING]
90:    for item in NEVER_COUNTS:
92:        gaps = missing_from_contract(text.replace(line, line.replace(item, "x")))
