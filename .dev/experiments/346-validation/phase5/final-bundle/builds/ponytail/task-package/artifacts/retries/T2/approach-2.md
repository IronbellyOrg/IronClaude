Implementer claims (A1 + A2, not verified):
- Built fix_audit.py prepare: trigger check, sha256s, byte copy, difflib hunks over non-blank lines, id tokens with range expansion, multiset citation diff, tolerant grade parse, protected flag, four classes, skip guard, fix-list.md/state.json/brief.md.
- A2 fix pass: graded records keyed on the lead ids of a prose line (after stripping list, heading and bold markers) or on every id of a table row's first cell; blocking yes/no column read from the table header; Where column found by prefix; Counter replaced by a dict multiset.
- Believed T2.AC1-AC3 met by tests/skills/test_fix_audit_script.py (46 passed).
- Known gap the A2 review found: list-bullet lines under a finding (e.g. "- WC-3: ... Not blocking") are still read as graded records, and "Not blocking" parses as blocking.
