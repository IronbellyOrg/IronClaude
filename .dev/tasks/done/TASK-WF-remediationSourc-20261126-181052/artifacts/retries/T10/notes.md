57895d5aca1f7bf6bd78cfb5a2dd36d1107e3f4f
A1 r1-1 F1.1 note docs/user-guide/run-ledger.md:44 ac=scope chk=n,n,n,n doc says the 24-hour rule catches an unrecorded Run; the 24 hours applies only when no readable previous ledger exists (the Run is still caught)
A1 r1-1 F1.2 note docs/user-guide/run-ledger.md:16 ac=scope chk=n,n,n,n zero-Runs guard text omits that the previous ledger must have had Runs
A1 r1-1 F1.3 note docs/user-guide/run-ledger.md:25 ac=scope chk=n,n,n,n cron line needs the superclaude state folder to exist before the first run (flock and the redirect do not create it); Coder#545 should mkdir it
