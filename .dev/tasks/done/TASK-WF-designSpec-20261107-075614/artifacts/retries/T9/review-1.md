start=4e6a6df7dfa46c8c0d4c1c0d3b7cde488dfdff79 tree=1cc04af1c83b7078102b29277a27a341d26f324a
F1.1 sev=blocking trigger=B1 ac=T9.AC1 at=tests/pr_submit/test_merge_guard_protocol.py:382 anchor="it names an L3 or `draft` condition" chk=y,n,n,n family=wave0-test-gate-coverage fix=in _wave0_problems assert that the loading text (before "At L3 with") contains no L3, ordinal, --monitor or bare draft outside the two event names; add mutation cases for "at L3, on --resume" and "when the PR is a draft" covers="The Wave 0 test fails when ... it names an L3 or `draft` condition" first=start origin=new: The gate list holds only four literal phrases, so an edited bullet saying "on --resume at L3", "at ordinal 3", "when the PR is a draft" or "with --monitor 3" passes the test; AC1 asks that the test fail when the bullet names an L3 or draft condition.
- T9.AC1 unmet (F1.1). T9.AC1@tests/pr_submit/test_merge_guard_protocol.py:382.
- T9.AC2 met. T9.AC2@src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:245.
- T9.AC3 met. T9.AC3@tests/pr_submit/test_merge_guard_protocol.py:1-8.
- T9.AC4 met. T9.AC4@src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:263.
- T9.AC5 met. T9.AC5@./artifacts/t9-checks.log:1-10.
