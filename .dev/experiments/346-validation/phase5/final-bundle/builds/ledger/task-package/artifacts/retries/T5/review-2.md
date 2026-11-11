414f305d927f0b1fd771c31bada924a05e984b77 tree=f90e5b45c0eee15f4ce5810b9248fe0311d9d148
F1.1 resolved
F2.1 resolved
F3.1 resolved
F3.2 resolved
F4.1 resolved
T5.AC1: met (src/superclaude/skills/sc-review-ledger/SKILL.md:2)
T5.AC2: met (tests/skills/test_review_ledger_script.py:1554)
T5.AC3: met (src/superclaude/skills/sc-review-ledger/SKILL.md:1)
F5.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/skills/sc-review-ledger/SKILL.md:24 anchor="those sessions never run the writing script: a review session reads only files the script wrote" chk=n,n,n,y family=who-runs-what fix=say review and reviser sessions run no script first=A1 origin=late: SKILL.md lets review and reviser sessions run status, verdict and --dry-run calls; the plan constraint says they never run the writing script (owner ruling 2026-11-08 Option A / Proposal A allows the read-only calls; see artifacts/owner-rulings.md).
F6.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/skills/sc-review-ledger/SKILL.md:102 anchor="every subcommand with flags, refusal codes and exit codes" chk=n,n,n,y family=refusal-code-mapping fix=add E-USAGE (neither --ledger nor --doc) to the status and verdict rows first=A1 origin=late: status and verdict refuse E-USAGE but their rows omit it.
F7.1 sev=note trigger=none ac=scope at=src/superclaude/skills/sc-review-ledger/SKILL.md:88 anchor=src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py:730 chk=n,n,n,n family=refusal-code-mapping fix=say every mutation but init can be refused those codes first=A2 origin=fix-induced: the general refusal sentence includes init, which cannot raise E-NO-LEDGER, E-TAMPERED, E-STALE-SEQ or E-OP-CONFLICT (the false-claim anchor :730 is the def line and does not hold contradicting text, so the yes failed its Read-back).
F1.1 resolved
F2.1 resolved
F3.1 resolved
F3.2 resolved
F4.1 resolved
F5.1 open
F6.1 resolved
