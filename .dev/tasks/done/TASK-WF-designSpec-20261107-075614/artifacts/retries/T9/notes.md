4e6a6df7dfa46c8c0d4c1c0d3b7cde488dfdff79
A3 r3-1 F3.1 note tests/pr_submit/test_merge_guard_protocol.py:469 ac=T9.AC1 n,n,n,n The check any("gate" in p ...) is satisfied by the pin's own message, so it does not tell a gate edit from any other edit; the pin catches both, so the behavior holds.
A3 r3-1 F3.2 note src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:220 ac=scope n,n,n,n The flag row says "No effect below L3" while refs/merge-guard.md Resume row 2 still reports held below L3; the row matches source.md and nothing is wrong at run time.
