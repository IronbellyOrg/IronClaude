8446c587969d893ff1e7fa21c254546fec5814a9
## family report-id-parse (F2.1) — written after the brief-3 run (late; the before-output is read from checkpoint tree a2 = 2f4cf6a6e75d19673980d63927551cc11c97358c, the tree the A2 review failed on)
defect form: bullet lines (-, *, +) under a finding are read as graded records after their marker is stripped
command: git grep -n -e MARKER_RE -e BULLET_RE -e RECORD_RE -e 'def lead_ids' 2f4cf6a6e75d19673980d63927551cc11c97358c -- src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py tests/skills/test_fix_audit_script.py
before:
2f4cf6a6e75d19673980d63927551cc11c97358c:src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:23:MARKER_RE = re.compile(r"^\s*(?:#+\s*)?(?:[-*+]\s+|[0-9]+[.)]\s+)?[*_`\s]*")
2f4cf6a6e75d19673980d63927551cc11c97358c:src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:77:def lead_ids(line: str) -> list[str]:
2f4cf6a6e75d19673980d63927551cc11c97358c:src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:79:    m = LEAD_RE.match(MARKER_RE.sub("", line, count=1))
coupled sites: parse_report prose branch (lead_ids caller); test_four_grade_formats prose lines; FLG_R2_STYLE fixture
after:
after: src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:23:BULLET_RE = re.compile(r"^\s*[-*+]\s")
after: src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:24:RECORD_RE = re.compile(
after: src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:80:def lead_ids(line: str) -> list[str]:
after: src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:84:    if BULLET_RE.match(line):
after: src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:86:    m = RECORD_RE.match(line)
