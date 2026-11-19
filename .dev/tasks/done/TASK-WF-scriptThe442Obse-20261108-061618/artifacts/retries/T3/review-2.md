start=e42b6fad93894e7144df9bd08a9a35a06d6c5e93 tree=8d614005a7488e22c4e3d198624ed2828d3aada1
F3.1 resolved
F3.2 open (new boundary; see below)
AC T3.AC1 met .dev/issues/442/scripts/driver-selftest.sh:24
AC T3.AC2 met .dev/issues/442/scripts/driver.sh:52
AC T3.AC3 met .dev/issues/442/scripts/driver-selftest.sh:38
AC T3.AC4 unmet .dev/issues/442/scripts/driver-helpers.sh:55 (finding F3.2)
AC T3.AC5 met .dev/issues/442/scripts/driver.sh:77
AC T3.AC6 met .dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/artifacts/t3-orca-help.txt:1
F3.2 sev=blocking trigger=B2 ac=T3.AC4 at=.dev/issues/442/scripts/driver-helpers.sh:55 anchor="keeps `send` waiting until the notice and its answer (a further Stop) appear" chk=amiss:y,false:y,harm:n,constraint:y family=notice-vacuous fix="Fail at EOF when no Stop beyond a was seen; reset the notice latch at s == a; add a self-test case whose log ends at the turn's Stop" covers="keeps `send` waiting until the notice and its answer (a further Stop) appear" first=A2 origin=fix-induced: with wait-notice, when the log ends at the turn's new Stop (the normal pending state), the awk never evaluates s > a, falls off EOF with default exit 0, and notice_answered succeeds, so wait_turn prints TURN_END stop at once (live probe 0.07s, no notice); a <task-notification> from before the baseline also latches seen_notice.
