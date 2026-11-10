9e83e1e98bec90d57fa2a925fa0bf92ecae216ee
## family owner-count-held-set (F1.1)
defect form: DOWNGRADE ids enter the held set only when the audit applied
command: grep -n -e 'held = ' -e 'if applied and' src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py
before:
927:    if applied and (d / "closed-minor.txt").exists():
942:    held = closed + [t for t in downgrades if applied and t not in closed]
coupled sites: test_owner_count_equal_when_audit_skipped; the owner-decision comment above held
## family verdict-new-table-parse (F1.2)
defect form: a review-3 row graded blocking without a severity label is dropped from new_blocking
command: grep -n -e 'new_blocking = ' -e 'no resolution table rows' src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py
before:
950:        unparseable.append("no resolution table rows in the review-3 report")
958:    new_blocking = [t for t, g in new.items() if g["blocking"]]
coupled sites: parse_report label rule (T2, not changed here); verdict tests
after (owner-count-held-set):
after: 949:    if applied and (d / "closed-minor.txt").exists():
after: 964:    held = closed + [t for t in dict.fromkeys(downgrades) if t not in closed]
after (verdict-new-table-parse):
after: 972:        unparseable.append("no resolution table rows in the review-3 report")
after: 980:    new_blocking = list(
after: 982:            [t for t, g in new.items() if g["blocking"]] + unlabelled_blocking(r3)
