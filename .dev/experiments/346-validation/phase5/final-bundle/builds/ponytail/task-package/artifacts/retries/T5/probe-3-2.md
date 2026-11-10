9e83e1e98bec90d57fa2a925fa0bf92ecae216ee
## family verdict-closed-disagree (F4.1) — written after the brief-4 run; before-output read from checkpoint tree a3 = a9b1fcf2ac1ec19f50b7dc06ddbbacee30133d8c
defect form: a status-word row of review-2 ids is skipped before its blocking grade is read
command: git grep -n -e 'set(toks) <= r2_ids' -e 'parse_grade(line, key)' a9b1fcf2ac1ec19f50b7dc06ddbbacee30133d8c -- src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py
before:
a9b1fcf2ac1ec19f50b7dc06ddbbacee30133d8c:src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:187:        label, blocking, fr = parse_grade(line, key)
a9b1fcf2ac1ec19f50b7dc06ddbbacee30133d8c:src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:937:        if any(c.lower() in STATUS_WORDS for c in cs[1:]) and set(toks) <= r2_ids:
a9b1fcf2ac1ec19f50b7dc06ddbbacee30133d8c:src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py:939:        if parse_grade(line, key)[1] is not False:
coupled sites: the disagree list in cmd_verdict; closed-id verdict tests
after:
after: 187:        label, blocking, fr = parse_grade(line, key)
after: 942:        blocking = parse_grade(line, key)[1]
after: 951:            blocking is not True
after: 953:            and set(toks) <= r2_ids
