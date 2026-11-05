40950c4008013a396f395a09d8206bc392d6458a e80bbb4ed8cf6aca89f26f0667fedcaaa44def88
F1.1 resolved
F1.3 resolved
F1.4 resolved
F1.5 resolved
F3.1 resolved
T6.AC1 met: T6.AC1@docs/reference/model-aliases.md:5, docs/reference/model-aliases.md:14-20, docs/reference/model-aliases.md:45-49, docs/reference/model-aliases.md:54-56, docs/reference/model-aliases.md:59-61, docs/reference/model-aliases.md:63-75, docs/reference/model-aliases.md:77-82, docs/reference/README.md:22
T6.AC2 met: T6.AC2@.dev/tasks/to-do/TASK-WF-makeTheAliasOnly-20261105-051649/artifacts/t6-test.log:1 (13 passed; grep exit 1)
F3.2 sev=blocking trigger=B2 ac=scope at=docs/reference/model-aliases.md:24 anchor=tests/skills/test_model_alias_policy.py:223-224 chk=n,y,n,n family=test-scope-misstated fix=reword line 24 so it says the test does not require plain aliases for these examples, and note that test_retry_ladder_uses_the_variable_names_the_workspace_exports requires retry.md to name T3Model01, T2Model02, T1Model02 and T1Model01 first=A3 origin=late: line 24 says "The test has no check for these examples", but the first example (the retry ladder slot variables on line 26) is checked by that test, which asserts each of the four names is in refs/retry.md.
