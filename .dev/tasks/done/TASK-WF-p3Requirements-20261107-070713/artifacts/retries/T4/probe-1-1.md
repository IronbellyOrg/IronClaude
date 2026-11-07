bc1400fa3ea604d9a68598157baf459e648ad1ff
family T4-guard-docstring
defect form: the regression-guard statement is only a comment
command: grep -n -F -e "regression guard" -- tests/pr_submit/test_ci_classify.py
before:
337:# are regression guards: they pass on today's code because ``classify_checks`` never
coupled sites: the three new test functions after the comment block
after:
337:# are regression guards: they pass on today's code because ``classify_checks`` never
