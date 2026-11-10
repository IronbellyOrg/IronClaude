db07fea14a627a52c2878b0e2471960a2fb11bc0
A1 r1-1 F1.5 minor src/superclaude/skills/sc-diffgate/scripts/diffgate.py:352 ac=scope n,n,n,n an empty lock file is read as pid 0 and removed as stale (window between O_EXCL create and pid write); two callers removing the same stale lock could each take it.
A2 r2-1 F2.1 minor src/superclaude/skills/sc-diffgate/scripts/diffgate.py:352 ac=T1.AC4 n,n,n,n an empty lock file is read as pid 0 and deleted as stale; a holder between its O_EXCL create and its pid write can lose the lock (same defect as F1.5).
A2 r2-1 F2.2 minor src/superclaude/skills/sc-diffgate/scripts/diffgate.py:103 ac=scope n,n,n,n str.splitlines() also splits on form feed and other separators, so a file of under 100,000 newline lines that contain form feeds can exit 2.
