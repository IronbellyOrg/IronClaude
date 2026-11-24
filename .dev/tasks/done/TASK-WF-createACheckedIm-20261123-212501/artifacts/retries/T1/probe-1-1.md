start=fdff62848f3268733cedac6bf940bf08f30663b8

## weak-custom-lens-assertion

Defect: separate substrings lens/custom do not enforce their binding.
Command: git grep -n -F -e '"lens" in help_text' -e 'lens:custom' -- tests/swarm/test_cli_registration.py
Before: tests/swarm/test_cli_registration.py:112 has the bare pair assertion; no explicit binding assertion.
Coupled sites: only new test assertion at 112. Docs reference at docs/swarm/command-reference.md:57-58 explicitly binds the JobSpec field to custom lens. No product code edit or other tests needed for this family.
After: re-run same git grep command found only tests/swarm/test_cli_registration.py:112 asserting `lens:custom` after whitespace/backtick normalization. Strengthened pre-fix test still fails on stale help, retained separately in ./artifacts/validate-help-red-strengthened.txt; original red capture unchanged.
