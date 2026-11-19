ce29bcda4f5cb5efdd9b720f7e78c81cd1f36e63
A4 r4-3 F1.1 minor .dev/issues/442/scripts/session-a.sh:109 ac=scope n,n,n,n resume of item 4: a rerun after a stop at p03 fires /sc:implement x again (item 4 is not a numbered step)
A4 r4-3 F1.2 minor .dev/issues/442/scripts/session-a-selftest.sh:95 ac=T4.AC2 n,n,n,n the NEEDS_INPUT case comment says the dialog is at the LL-NOBIND step but it stops at step 1; no assert that nothing was sent after the stop
A4 r4-3 F1.3 minor artifacts/t4-selftest.txt:86 ac=scope n,n,n,n evidence file dates from 2026-11-09 and has no rows for later self-test cases (count-esc, resume)
A4 r4-3 F1.4 minor .dev/issues/442/scripts/session-a2.sh:30 ac=scope n,n,n,n A2 gives the h1m probe log only a 3 s wait and has no ready poll
A4 r4-3 F1.5 note .dev/issues/442/scripts/session-a.sh:136 ac=scope n,n,n,n MAIN is read at step 17, not first as the runbook says; evidence.sh derives it itself
A4 r4-3 F1.6 note .dev/issues/442/scripts/session-a.sh:145 ac=scope n,n,n,n the line-444 prompt is sent in session A (p16), as runbook line 442 says; the task text lists it under A2
