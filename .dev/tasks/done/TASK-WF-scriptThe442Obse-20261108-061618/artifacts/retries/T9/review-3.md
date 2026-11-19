start=a4bb361e1c6375fe1dedddd00ccf6192329f8a51 tree=91f4a99ffb6b3cf3621626f016183cdc946ef435
AC T9.AC1 met .dev/issues/442/observation-runbook.md:765,837,850,854,858
AC T9.AC2 met .dev/issues/442/scripts/runbook-selftest.sh:25-37
F9.6 sev=blocking trigger=B2 ac=scope at=.dev/issues/442/observation-runbook.md:854 anchor=.dev/issues/442/scripts/driver.sh:55 chk=amiss:n,false:y,harm:n,constraint:n family=needs-input-resend fix="split the NEEDS_INPUT row: before the send nothing was sent, so answer and send the prompt again; during the turn the prompt was sent, so answer only" first=A3 origin=new: the NEEDS_INPUT row ended with "Do not resend the prompt." but driver.sh:55 says a dialog seen before the send means the prompt is not sent (Read back: driver.sh:55 holds the Pre-send check comment)
F9.7 sev=minor trigger=none ac=scope at=.dev/issues/442/observation-runbook.md:661 anchor=none chk=amiss:n,false:n,harm:n,constraint:n family=o10-web-ui fix="note that the scripted path uses the contents API" first=A3 origin=new: line 661 still describes the web UI edit as the way to make the O-10 edit, outside the plan's lines 764-769
F9.8 sev=minor trigger=none ac=scope at=.dev/issues/442/observation-runbook.md:766 anchor=none chk=amiss:n,false:n,harm:n,constraint:n family=release-cite fix="move the refs/claim.md citation to the release line is an rm" first=A3 origin=new: the claim.md line 119 citation follows the shell sentence although it supports only that the release line is an rm

--- re-review r3-2 tree=4e88aeb45b73d873b32721ac81b80fc32efd8b6b ---
F9.6 resolved
No blocking finding; T9.AC1 and T9.AC2 met.
