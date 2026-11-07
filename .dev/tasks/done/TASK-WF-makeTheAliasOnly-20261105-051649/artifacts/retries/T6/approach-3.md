40950c4008013a396f395a09d8206bc392d6458a
Implementer claims (not facts):
- Rebuilt docs/reference/model-aliases.md from brief 3: the policy section lists what each named test function checks, exceptions sit under "Outside the test's scope (found 2026-11-05)", status lines are dated, and I ran a sweeping-word grep with a justification per hit (artifacts/t6-claims.md).
- The first review of this tree found the probe sentence credited the sonnet variable; one repair fixed it.
- The repair re-review found line 24 ("The test has no check for these examples") ignores that the retry-names test checks refs/retry.md for the four slot names. I believe the other sentences are accurate.
