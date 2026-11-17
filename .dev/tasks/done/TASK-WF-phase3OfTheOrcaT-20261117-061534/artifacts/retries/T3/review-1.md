c62f30dd5f4cf84e9a7766e02d245b98e818a5c8 tree=1d4e438375be85893c9274ce3df831f3e82b6c03
T3.AC1 met tests/observe/test_commands.py:762
T3.AC2 unmet tests/observe/test_commands.py:796 F1.1
T3.AC3 met tests/observe/test_collector.py:137
T3.AC4 met src/superclaude/cli/observe/collector.py:153
F1.1 sev=blocking trigger=B1 ac=T3.AC2 at=tests/observe/test_commands.py:796 anchor="the question line of the record, <qid> | ... | dispatchId=<id> | link=linked, is present and the record does not contain the question text; with --width 116 the screen contains the question text" chk=y,n,n,n family=ac2-record-screen-asserts fix=add the record and screen assertions once Tasks 4 to 6 exist first=A1 origin=new: the --once test asserts only collector state, the argv log and the link kwarg; the record suffix is built in Task 6 and the screen text in Tasks 4 and 5, which run after Task 3 (plan ordering defect).
