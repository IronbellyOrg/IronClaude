start=4e6a6df7dfa46c8c0d4c1c0d3b7cde488dfdff79 tree=e1f88b05127f60f438b828bf6ea6b489b336a8dc
F2.1 sev=blocking trigger=B1 ac=T9.AC1 at=tests/pr_submit/test_merge_guard_protocol.py:388 anchor="it names an L3 or `draft` condition" chk=y,n,n,n family=wave0-test-gate-coverage fix=in _wave0_problems run the gate scan over the whole bullet except the literal off sentence, including the bold heading (the real heading is "(every ordinal, both modes)" and holds none of the gate words), and add mutation cases for a heading of "(L3 only)" and for "at level 3" covers="The Wave 0 test fails when ... it names an L3 or `draft` condition" first=A2 origin=fix-induced: The gate scan starts after the bold heading marker, so a heading edit never reaches it; with the heading changed to "(L3 only)" or "(draft mode)", or "at level 3, " added to the loading sentence, _wave0_problems returns no problems, so the test passes a bullet that names an L3 or draft condition.
F1.1 resolved
- T9.AC1 unmet (F2.1). T9.AC1@tests/pr_submit/test_merge_guard_protocol.py:388.
- T9.AC2 met. T9.AC2@src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:245.
- T9.AC3 met. T9.AC3@./artifacts/retries/T9/extras-2.log:1-6.
- T9.AC4 met. T9.AC4@tests/pr_submit/test_merge_guard_protocol.py:466.
- T9.AC5 met. T9.AC5@./artifacts/t9-checks.log:1-10.
F2.1 resolved
