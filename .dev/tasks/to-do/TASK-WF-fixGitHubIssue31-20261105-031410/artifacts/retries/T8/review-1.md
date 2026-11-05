fef4d9bcad703581e2786a70c61735758066cd22
AC marks (reviewer, summary): T8.AC1 met tests/unit/test_ccsession_tiers.py:481-521 and ./artifacts/t8-tiers-tests.log (131 passed)
No findings. Reviewer note: the "Session name not in output" check in the new test cannot fail with stdin on /dev/null; the label regex and argument checks cover the behaviour.
