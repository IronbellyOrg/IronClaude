start=6fdae45fcfb2d8f73b7acb9b87a530ab57ee0517 tree=2bdf9978e6b51e0ad88a7de46086a53321e2da53
F5.1 resolved
AC T5.AC1 met .dev/issues/442/scripts/setup-github-selftest.sh:68-72
AC T5.AC2 met .dev/issues/442/scripts/setup-github-selftest.sh:91-98
AC T5.AC3 met .dev/issues/442/scripts/setup-github.sh:56-62
F5.2 sev=blocking trigger=B4 ac=scope at=.dev/issues/442/scripts/setup-github.sh:22 anchor="fills every section with the runbook's title and body text for that issue (line 177 and line 178)" chk=amiss:n,false:n,harm:n,constraint:y family=body-text-fidelity fix="Fill the template sections with the runbook's body text verbatim, including 'The only change wanted: create the file ob-442/$t.txt holding the single line ob-442 $t. Touch nothing else. Close without merging anything.'" covers="fills every section with the runbook's title and body text for that issue (line 177 and line 178)" first=A1 origin=new: the filled body paraphrases the runbook body and drops "The only change wanted... Touch nothing else. Close without merging anything."; the governed sessions later work these issues and "Touch nothing else" is the part that matters.
F5.2 resolved
