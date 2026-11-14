b0a7f9d6eaf45660bfe9511bd5cafecce21dafed cc0d6e6cc3090ad0fd723c47b1311536515bdd34
Reviewer AC marks (A2 review, fresh subagent ab50502b8d3d0003d, 106 passed in its own run): F1.1 resolved. F1.2 resolved. F1.3 resolved. F1.4 resolved. F1.7 open (same family, further unflagged claims).
T1.AC1 met (DESIGN.md:60-104). T1.AC2 met (tests/test_faults.py:51-195; tests/test_hook.py:33-167; tests/test_launcher.py:41-146). T1.AC3 met apart from the exclusions (IMPLEMENTATION.md:200-201). T1.AC4 met (spikes/out/s0-summary.json:1; spikes/out/act-rates.json:1; spikes/out/smoke-check-smoke-f7-el2-3.json:1). T1.AC5 unmet: F2.1, F2.2, F2.3.
F2.1 sev=blocking trigger=B1 ac=T1.AC5 at=IMPLEMENTATION.md:214 anchor=T1.AC5 "Every number and claim in it must match what is on disk" chk=y,y,n,n family=impl-md-accuracy fix=delete the sentence "The offline measurement was 9-81 ms." from section 7.2 first=A1 origin=late: (reviewer id F1.7.a) the figure was dropped at line 136 but survives at line 214, so the file contradicts itself and the number has no evidence row.
F2.2 sev=blocking trigger=B1 ac=T1.AC5 at=IMPLEMENTATION.md:216 anchor=T1.AC5 "Every number and claim in it must match what is on disk" chk=y,y,n,n family=impl-md-accuracy fix=say S0 recorded the process list and the pattern is unit-tested, with no one-session baseline first=A1 origin=late: (reviewer id F1.7.b) "S0 re-checked the concurrency pattern (passes)" contradicts line 142 "Only partly shown by S0".
F2.3 sev=blocking trigger=B2 ac=T1.AC5 at=IMPLEMENTATION.md:111 anchor=tests/test_pins.py:22 chk=n,y,n,n family=impl-md-accuracy fix=write "cd frozen && sha256sum -c pins.sha256" at lines 111 and 192 first=A1 origin=late: (reviewer id F1.8) run from R4 or REPO, sha256sum -c frozen/pins.sha256 prints "10 listed files could not be read".
F1.1 resolved
F1.2 resolved
F1.3 resolved
F1.4 resolved
F1.7 open
F2.1 resolved
F2.2 resolved
F2.3 resolved
F1.7 resolved
(review r2-2, fresh subagent a8e7b1d7ef3ac9dfb: no new finding; the blockers were fixed in place, see repair-2-1.md)
