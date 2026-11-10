0047c2b27973251d0eb09a98eae2c34de5c7b671 tree=ba9683444b514b6f394f9413c4ddcb9c1afae3c2
T3.AC1: unmet F1.1 (tests/skills/test_review_ledger_script.py:948)
T3.AC2: met (tests/skills/test_review_ledger_script.py:1159)
F1.1 sev=blocking trigger=B1 ac=T3.AC1 at=tests/skills/test_review_ledger_script.py:948 anchor="each status transition in the source.md section 2 table and its refusal code" chk=y,n,n,n family=missing-transition-test fix=add tests for an untouched verified row answered regressed/open (E-NOT-CHANGED), a once-verified fixed row answered open (reopened), resolved on an unmappable anchor (E-ANCHOR), a verify new row with a missing or repeated anchor (E-ANCHOR, E-ANCHOR-AMBIGUOUS) first=A1 origin=new: four table rows have no test.
F1.2 sev=minor trigger=none ac=scope at=src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py:659 anchor=tests/skills/test_review_ledger_script.py:1092 chk=n,n,n,n family=brief-literal fix=test close on the same report with only its body edited and the tail intact first=A1 origin=new: the intact-tail E-PHASE test uses a different report.
F1.1 resolved
