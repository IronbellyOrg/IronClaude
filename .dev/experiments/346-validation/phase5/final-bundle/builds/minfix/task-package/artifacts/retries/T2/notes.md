0ca44cafe2eeaebbeeff497a38edb74a24688843
A1 r1-1 F1.1 minor tests/skills/test_sc_fixcheck.py:390 ac=T2.AC4 amiss=n,false=n,harm=n,constraint=n the partial-quote fixture is 18 characters, not 20; same rule exercised, and a 20-character probe gives exit 1 with quote not in baseline
A1 r1-1 F1.2 minor src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py:286 ac=scope amiss=n,false=n,harm=n,constraint=n NEW_ID_RE also matches UTF-8, SHA-256 and ISO-8601 when absent from the baseline (false-positive risk; the spec calls these tripwires unverified)
