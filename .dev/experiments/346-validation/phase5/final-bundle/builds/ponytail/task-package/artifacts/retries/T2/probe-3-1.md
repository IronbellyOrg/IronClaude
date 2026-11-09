8446c587969d893ff1e7fa21c254546fec5814a9
## family report-id-parse (F3.1, F3.2)
defect form: a table row is a graded record when its first cell merely contains an id (free text allowed) or when only a blocking word (no severity label) appears in it
command: grep -n -e 'toks = id_tokens(cs\[0\])' -e 'label == "unknown" and blocking is None' src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py tests/skills/test_fix_audit_script.py
before:
src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:172:            toks = id_tokens(cs[0])  # every id of the id cell, ranges expanded
src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:185:        if in_prior or (status and label == "unknown" and blocking is None):
src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:188:        if label == "unknown" and blocking is None and not fr:
coupled sites: parse_report prior branch (status rows), test_unknown_or_conflicting_grade_is_blocking, test_every_id_of_an_id_cell_is_graded, FLG_R2_STYLE table rows
after: src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:23:ID_CELL_RE = re.compile(rf"{LEAD}(?![\w-])")
after: src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:175:            toks = id_tokens(cell) if ID_CELL_RE.fullmatch(cell) else []
after: src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:191:        if label == "unknown" and not fr:
