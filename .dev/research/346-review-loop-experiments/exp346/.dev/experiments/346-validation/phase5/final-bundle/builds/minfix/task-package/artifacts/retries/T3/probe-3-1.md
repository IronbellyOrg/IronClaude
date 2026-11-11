73e3cafd123859e9a454ed39aaeb467e00dbc7d2
## family enforce-equal-region-structure
defect form: the unit diff compares normalised text only, so a unit whose kind changes (fence, code, cell, heading, text) between the files sits in an equal region that --enforce never rewrites
command: grep -n -e "u.norm for u in" src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py
before:
545:    opcodes = difflib.SequenceMatcher(None, [u.norm for u in bu], [u.norm for u in ru], autojunk=False).get_opcodes()
coupled sites: diff_hunks opcodes and the moved-unit pool (both key on norm only); region_edits rewrites only non-equal regions
