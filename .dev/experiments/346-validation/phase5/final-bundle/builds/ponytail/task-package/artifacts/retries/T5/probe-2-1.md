9e83e1e98bec90d57fa2a925fa0bf92ecae216ee
## families owner-count-held-set (F2.1), verdict-prior-table-parse (F2.2), verdict-new-table-parse (F2.3) — written after the brief-3 run; before-output read from checkpoint tree a2 = 25cac27c897e2f53c2a17ee5e4e004b7ee95e0a3
defect forms: held ids re-listed by review 3 dropped from the owner count; resolution rows with no status word read as not open; ungraded review-3 rows dropped
command: git grep -n -e 'held_cm = ' -e 'listed_open = ' -e 'BLOCKING_RE.search(line.lower())' -e 'resolution rows without a status' 25cac27c897e2f53c2a17ee5e4e004b7ee95e0a3 -- src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py
before:
25cac27c897e2f53c2a17ee5e4e004b7ee95e0a3:src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:931:        if BLOCKING_RE.search(line.lower()):
25cac27c897e2f53c2a17ee5e4e004b7ee95e0a3:src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:978:    listed_open = [t for t, st in prior if st in ("open", "regressed")]
25cac27c897e2f53c2a17ee5e4e004b7ee95e0a3:src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:991:    held_cm = sum(ids.get(t, {}).get("label") in CM for t in held if t not in new)
coupled sites: the owner-count tests, test_unlabelled_blocking_row_in_review3_counts_as_open, r3() fixture
after:
after: 937:        if parse_grade(line, key)[1] is not False:
after: 982:            f"resolution rows without a status ({', '.join(sorted(STATUS_WORDS))}): {', '.join(blank)}"
after: 989:    listed_open = [t for t, st in prior if st in ("open", "regressed")]
after: 1003:    held_cm = sum(
