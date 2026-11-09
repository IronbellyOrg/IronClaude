b675805775e8472e8b3a8576b9f83a1347a648e9
A1 r1-1 F1.2 minor src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1079 ac=scope n,n,n,n nothing records pre_audit; an audit-raw record does not prove the pre-audit verdict was PASS
A1 r1-1 F1.3 minor src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1073 ac=scope n,n,n,n a --reply path that does not exist exits 5 instead of recording the audit incomplete
A2 r2-1 F2.1 minor src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:1088 ac=scope n,n,n,n apply-audit writes no pre_audit field; Task 5's sentinel must derive pre_audit
A2 r2-1 F2.2 minor src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py:684 ac=scope n,n,n,n canary evidence renders as "[verified] <text>" while claim evidence names a place and line, so a grader could tell canaries apart
