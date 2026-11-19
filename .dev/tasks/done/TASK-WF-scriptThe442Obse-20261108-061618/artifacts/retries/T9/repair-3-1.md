a4bb361e1c6375fe1dedddd00ccf6192329f8a51
reviewed=91f4a99ffb6b3cf3621626f016183cdc946ef435 ref=r3-1
F9.6 sev=blocking trigger=B2 ac=scope at=.dev/issues/442/observation-runbook.md:854 anchor=.dev/issues/442/scripts/driver.sh:55 chk=amiss:n,false:y,harm:n,constraint:n family=needs-input-resend fix="split the NEEDS_INPUT row: before the send nothing was sent, so answer and send the prompt again; during the turn the prompt was sent, so answer only" first=A3 origin=new: the NEEDS_INPUT row ended with "Do not resend the prompt." but driver.sh:55 says a dialog seen before the send means the prompt is not sent (Read back: driver.sh:55 holds the Pre-send check comment)
applied tree=4e88aeb45b73d873b32721ac81b80fc32efd8b6b
