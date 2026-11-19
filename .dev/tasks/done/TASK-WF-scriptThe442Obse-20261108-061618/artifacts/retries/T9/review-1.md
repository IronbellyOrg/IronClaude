start=a4bb361e1c6375fe1dedddd00ccf6192329f8a51 tree=508020ca3e6a5cdc2c5dcdf792165fef59f01056
AC T9.AC1 met .dev/issues/442/scripts/runbook-selftest.sh:24-33
AC T9.AC2 met .dev/issues/442/scripts/selftest.sh:132-133
F9.1 sev=blocking trigger=B2 ac=T9.AC1 at=.dev/issues/442/observation-runbook.md:839 anchor=.dev/issues/442/scripts/session-gov.sh:211 chk=amiss:n,false:y,harm:n,constraint:n family=runbook-overclaim fix="narrow the section 6 sentence to what the scripts do (scripts you run; helpers rely on their caller; network, Orca, Git and Claude calls bounded)" first=A1 origin=new: section 6 said every script sets pipefail and umask and bounds every external call with timeout; lib.sh and driver-helpers.sh set neither, and pgrep at session-gov.sh:211 has no timeout (Read back: session-gov.sh:211)

--- re-review r1-2 tree=4e928433b4623e72d2073cc50a928c37792407e8 ---
F9.1 resolved
F9.2 sev=blocking trigger=B2 ac=scope at=.dev/issues/442/observation-runbook.md:856 anchor=.dev/issues/442/scripts/driver-helpers.sh:35 chk=amiss:n,false:y,harm:n,constraint:n family=runbook-overclaim fix="say the dialog can also appear after the prompt was sent" first=A1 origin=new: (the text predates the fix pass, so this is a new finding and not fix-induced) the NEEDS_INPUT bullet said the driver sent nothing, but wait_turn prints NEEDS_INPUT after the send (Read back: driver-helpers.sh:35 prints NEEDS_INPUT from wait_turn, called after orca terminal send at driver.sh:61)

--- re-review r1-3 tree=9295b3b87ce56324ee611d4869e7c334b9a745dc ---
F9.2 resolved
F9.3 sev=blocking trigger=B2 ac=scope at=.dev/issues/442/observation-runbook.md:839 anchor=.dev/issues/442/scripts/setup-github.sh:19 chk=amiss:n,false:y,harm:n,constraint:n family=runbook-overclaim fix="narrow the scratch sentence" first=A1 origin=new: section 6 said every script keeps its scratch under /tmp/ob; setup-github.sh creates mktemp issue-body files in the system temp dir (Read back: setup-github.sh:19 tpl=$(mktemp))
F9.4 sev=blocking trigger=B2 ac=scope at=.dev/issues/442/observation-runbook.md:859 anchor=.dev/issues/442/scripts/session-a2.sh:34 chk=amiss:n,false:y,harm:n,constraint:n family=runbook-overclaim fix="say the script stopped without recording that step and the line gives the reason" first=A1 origin=new: the PENDING sentence listed two causes and said the line names the screen file; session-a2.sh:34 reason=h1m-log-empty and session-gov.sh lines print other reasons without a screen (Read back: session-a2.sh:34)
F9.5 sev=minor note: the O-10 sentence lacked the branch condition (fixed in the repair)
F9.6 sev=minor note: setup-github.sh prints NEEDS_INPUT itself (fixed in the repair)
