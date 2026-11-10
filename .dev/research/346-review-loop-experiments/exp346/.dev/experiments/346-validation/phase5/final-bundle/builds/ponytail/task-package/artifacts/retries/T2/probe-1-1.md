8446c587969d893ff1e7fa21c254546fec5814a9
## family report-id-parse (F1.1, F1.2)
defect form: a graded record is keyed on the first id of any line with a grade word, so free-text lines define ids and multi-id cells keep only their first id
command: grep -n -e 'rid = toks' -e 'toks = id_tokens' -e 'def parse_report' src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py tests/skills/test_fix_audit_script.py
before:
src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:115:def parse_report(text: str) -> dict:
src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:132:        toks = id_tokens(cs[0] if cs else line)
src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:136:        rid = toks[0]
coupled sites: parse_report callers (cmd_prepare graded/prior_only); tests test_four_grade_formats, test_prior_status_row_without_heading_is_prior_only
## family disposition-parse (F1.3)
defect form: the Where column is found only by an exact 'where' header cell
command: grep -n -e 'where' src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py
before:
208:    where = None
212:            where = None
214:        if where is None:
216:            where = low.index("where") if "where" in low else None
218:        if is_separator(cs) or where >= len(cs):
220:        ids = {t for c in cs[:where] for t in id_tokens(c)}
222:            for a, z in re.findall(r":([0-9]+)(?:-([0-9]+))?", cs[where]):
coupled sites: classify() overlap test; test_minor_hunk_on_disposition_line_of_blocking_id_is_blocking_involved
## family import-list (F1.4)
defect form: an import outside the plan's listed standard-library modules
command: grep -n -e 'collections' -e 'Counter' src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py tests/skills/test_fix_audit_script.py
before:
src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:17:from collections import Counter
src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:309:            (Counter(id_tokens(s_txt)) - Counter(id_tokens(b_txt))).keys()
tests/skills/test_fix_audit_script.py:107:        "collections",
coupled sites: test_script_imports_only_stdlib allowlist
after (report-id-parse):
after: src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:137:def parse_report(text: str) -> dict:
after: src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:165:            toks = id_tokens(cs[0])  # every id of the id cell, ranges expanded
after (disposition-parse):
after: 246:    where = None
after: 250:            where = None
after: 252:        if where is None:
after: 255:            where = next((i for i, c in enumerate(low) if c.startswith("where")), None)
after: 257:        if is_separator(cs) or where >= len(cs):
after: 259:        ids = {t for c in cs[:where] for t in id_tokens(c)}
after: 261:            for a, z in re.findall(r":([0-9]+)(?:-([0-9]+))?", cs[where]):
after (import-list):
