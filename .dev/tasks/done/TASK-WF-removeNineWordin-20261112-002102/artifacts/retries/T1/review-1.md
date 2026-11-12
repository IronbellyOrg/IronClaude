55cb1afbedc5de3eadad0ad35adfdd1a97914451 tree=d67bac912e2994ad6b44965deffdcfff0d25cff9
T1.AC1: met CODEGRAPH.md:13, :74
T1.AC2: met CODEGRAPH.md:22, :50, :32
T1.AC3: unmet (F1.1) tests/core/test_codegraph_guide.py:134
F1.1 sev=blocking trigger=B1 ac=T1.AC3 at=tests/core/test_codegraph_guide.py:134 anchor="`uv run pytest tests/core/test_codegraph_guide.py -q` passes" chk=y,n,n,n family=plugin-twin-sync fix=copy src/superclaude/core/CODEGRAPH.md byte for byte to plugins/superclaude/core/CODEGRAPH.md and rerun the test file covers="`uv run pytest tests/core/test_codegraph_guide.py -q` passes" first=A1 origin=new: the source guide was edited, but the plugin twin plugins/superclaude/core/CODEGRAPH.md was not updated, so the byte-identity test fails and the test file does not pass.
