f497f24ba9dfa1ef073a84f5969f5fcdd81c2ea3
family=probe-param-coverage
defect form: a basename the plan names as a non-matching probe case is missing from the test_harness_regex_matches_probe parametrization
command: grep -n -F -e '("analyze-report.md", False)' -e '("notes.md", False)' tests/skills/test_issue_worker_agents.py
before:
(no hits)
coupled sites: tests/skills/test_issue_worker_agents.py:428-429 (test_written_md_names_takes_basenames extracts the same two basenames); plan Task 3 bullet 3 lists the full probe set
after:
417:        ("analyze-report.md", False),
418:        ("notes.md", False),
