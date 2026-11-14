9ecbe691236fd0327cf3336ce4c78b7f8bdc2601
A1 r1-1 F1.2 note src/superclaude/cli/sweep/report.py:164 ac=scope amiss:n,false:n,harm:n,constraint:n _version_line compares the text before the first "-" (the 1.0a facts rule), not the leading MAJOR.MINOR.PATCH; "1.4.245+b" prints UNVERIFIED, which errs safe.
A1 r1-1 F1.3 note src/superclaude/cli/sweep/report.py:379 ac=scope amiss:n,false:n,harm:n,constraint:n the Retained problems cap line states a row count and has no Distinct line; logged as choice (7) in Phase 8 Findings.
A1 r1-1 F1.4 note src/superclaude/cli/sweep/report.py:419 ac=scope amiss:n,false:n,harm:n,constraint:n the Sessions table has a leading ID column before the ten dimensions; logged as choice (5).
A1 r1-1 F1.5 note src/superclaude/cli/sweep/report.py:633 ac=scope amiss:n,false:n,harm:n,constraint:n sanitize also alters [, ], <, > and | in JSON path values; DESIGN 7.4 says values are sanitized, so report_path with those characters would not round-trip.
A1 r1-1 F1.6 note src/superclaude/cli/sweep/classify.py:269 ac=scope amiss:n,false:n,harm:n,constraint:n frozen-plan evidence text from classify contains "STOP code"; a strict string test over fixture output would hit it.
