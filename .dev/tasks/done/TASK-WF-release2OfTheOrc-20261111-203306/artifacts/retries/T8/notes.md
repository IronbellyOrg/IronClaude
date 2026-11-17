759924f31781b03261c9a62851e99dbafd5455f0
A1 r1-1 F1.1 note src/superclaude/cli/observe/questions.py:165 ac=T8.AC1 n,n,n,n unknown-created records sort last, so known-created records are evicted first; the spec does not settle the order
A1 r1-1 F1.2 minor src/superclaude/cli/observe/questions.py:167 ac=T8.AC1 n,n,n,n an evicted question that Orca returns again is re-added as a new record and counted in evicted again, so the open total is a lower bound that can overcount; consistent with never lowering the total
