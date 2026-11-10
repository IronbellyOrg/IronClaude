Implementer claims (A1 + A2, not verified):
- A1 wrote docs/designs/spec-panel-ponytail.md as source.md cut to its decisions: 2.1 paragraph, the 2.2 loop table, a Safe apply list condensed from 2.6, a verdict paragraph from 2.7, the owner count from Task 5, the 2.8 recommendation, the four owner decisions, the 472-line base and Unattended-mode deviation, the 3.1 file list plus fixture and routing test, install pointer, T08a line.
- The Safe apply bullets were paraphrased from source.md 2.6 and 2.3, not checked line by line against fix_audit.py apply's failure paths.
- A2 fix pass narrowed only the DOWNGRADE sentence (line 30) to ids review 2 graded blocking.
- Believed T9.AC1 and T9.AC2 met (literals log, tests/docs 11 passed). Not checked: the "every failure path" sentence (line 31) against cmd_apply's post-write file writes.
