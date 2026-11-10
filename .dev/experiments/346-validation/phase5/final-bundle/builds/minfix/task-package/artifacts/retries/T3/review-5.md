73e3cafd123859e9a454ed39aaeb467e00dbc7d2 tree=a513944addcfba91751936e75ceb8244ec890fe6
F1.1 resolved
F1.2 resolved
F2.1 resolved
F2.2 resolved
F3.1 resolved
F4.1 resolved
F5.1 resolved
F5.2 resolved
T3.AC1 unmet (F6.1), T3.AC1@src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py:1002. The other listed tests all pass: tests/skills/test_sc_fixcheck.py:521, :536, :549, :561, :570, :582, :600, and the enforce-then-check assertion at :790-791.
T3.AC2 met, T3.AC2@tests/skills/test_sc_fixcheck.py:748-749 (`random.Random(346)`, 200 cases, assertions that `--enforce` and the plain check both exit 0 at :778 and :791).
T3.AC3 met, T3.AC3@tests/skills/test_sc_fixcheck.py:618-625 (directory listing compared before and after).
T3.AC4 met, T3.AC4@tests/skills/test_sc_fixcheck.py:747: 84 passed.
F6.1 sev=blocking trigger=B1 ac=T3.AC1 at=src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py:1002 anchor="keeps in-budget fixes byte-for-byte" chk=y,y,n,n family=enforce-line-break-restore fix=in restore_line_breaks, restore a gap only when neither word next to it lies within an attributed hunk's revised text (or only after the unit diff, not the word diff, shows the gap inside an equal region), and correct the docstring at :934; add a test where an in-budget `add` appends "Backups also copy the cache." after OLD on the same line in BASE, asserting that plain check exits 0 and `--enforce` leaves the spec bytes unchanged covers="--enforce restores the over-budget and unattributed text and keeps in-budget fixes byte-for-byte" first=A5 origin=fix-induced: the new restore_line_breaks step (:929-946, run first at :988 and :1002) works on a word alignment of the whole file. When an in-budget appended sentence starts with the same word as the next paragraph, the aligner can match that word to the next paragraph's first word. The paragraph break then lands between two "unchanged" words, so the step moves the reviser's sentence into its own paragraph. Repro: the suite's BASE, with `R = BASE.replace(OLD, OLD + " Backups also copy the cache.")`. The ledger is L1 F1 op=add anchor=OLD new="Backups also copy the cache.". Plain check gives `h1 L1 F1 ... status=fixed`, exit 0. `--enforce` prints `reverted=- hunks=- ... line-breaks=1` and rewrites the spec as "...after one hour.\n\nBackups also copy the cache.\n\nBackups run at night...". That spec differs from R even though nothing was over budget. A fuzz of 300 in-budget same-line appends altered 4. The docstring at :934 ("A ledger entry is word-based, so such a change is never part of a declared fix") is false for this input. The property test cannot catch this: its kept-slice check (tests/skills/test_sc_fixcheck.py:776-787) compares only unit text, not the separators around it.
