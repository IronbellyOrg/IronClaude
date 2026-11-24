# Task 2 Compliance Review

## AC marks

start=f647b2362128593cd33049b703bba5d61c1ced67 tree=b89bb624bd040cd0bd2e6b240b3b22da2e985eea
T2.AC1 met @ tests/swarm/test_cli_registration.py:119-126: root scaffold help test rejects false option, requires JobSpec/field/custom-lens binding and inline route.
T2.AC2 met @ tests/swarm/test_cli_registration.py:129-138: option rejection exit 2, exact diagnostic and unchanged temporary directory.
T2.AC3 met @ ./artifacts/scaffold-help-red.txt:107-111 and ./artifacts/parser-before.txt:13-17: two expected help failures, parser passes. Reviewer could not verify T1 preservation from supplied diff; parent directly compared actual red-file bytes with T2's pinned Q0 blob and confirmed identical, not from git diff (which omits unindexed contents).
T2.AC4 met @ ./artifacts/public-before.txt:8-80: actual public commands, full output/status 0/0/2 and local commit/module provenance.
T2.AC5 met @ ./artifacts/diagnostic-disposition.md:13-21: exact rows addressed by new evidence, identical reference forms not controls, no-op causally inapplicable; original pending rows untouched.

## Findings and result

F1.1 chk=n,n,n,n is a command-spelling Note, not a blocker; saved in T2 notes. No confirmed blocking finding. Parent verdict compliant. Extras: Ruff passed; existing registration/parser cases 7 passed, 1 skipped, two expected-red help cases deselected for this extras run only. Required red observations remain separately recorded. No dependency install, product edit, model job, commit or push.
