65dbd5726fe7a4028e5760c211ccc55f65f7a49c
family handoff-claim-vs-source
defect form: a handoff sentence states a behaviour as universal or a test as proof where the live code has an exception or the test does not reach it
search: grep -n -i -E 'every|never|always|any |all |unique|starts untagged|waits for ever|proves' .dev/tasks/to-do/TASK-WF-fixGitHubIssue31-20261105-031410/artifacts/coder-handoff.md
after: the handoff was rewritten against ccsession and ccsession-orca with each guarantee's exceptions and with the tests that reach each claim; new tests added for input ended, an unwritable name list through ccsession-orca, a zero limit written 00 and a leading-zero limit; ccsession now reads 00 as no limit and 002 as 2
second pass (r2-1): sweep of the handoff for universal words; new tests test_orca_valid_ccsession_name_is_passed_even_where_a_launch_stays_untagged and test_ask_limit_starts_again_after_a_star; resume dropped from every CCSESSION_NAME claim (handoff, README, CHANGELOG, D08); CC_CLAUDE_FLAGS wording corrected.
