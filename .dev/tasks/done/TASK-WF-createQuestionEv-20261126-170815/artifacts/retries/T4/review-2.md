20a5b4889a1482fde59eefb34342aebd4e734312 tree=d25eddcda400167ecfc58d002589dee8669564bc
T4.AC1 unmet (T4.AC1@harness-feasibility.md:103-109; F2.1, F2.2)
T4.AC2 met (T4.AC2@harness-feasibility.md:226-249)
T4.AC3 met (T4.AC3@harness-feasibility.md:61-107)
T4.AC4 met (T4.AC4@harness-feasibility.md:219-223)
F2.1 sev=blocking trigger=B1 ac=T4.AC1 at=.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness-feasibility.md:103-109 anchor="answers each bullet above with a command and its real output, not a guess" chk=y,n,n,n family=answer-supplied-unevidenced fix=re-run the answered probe with a driver that waits for the answer to be processed, keep the transcript and the after-answer screen in the scratch directory, and quote them; or write "answer supply not evidenced here" covers="whether the run can supply the answer \"keep my wording\"" first=A2 origin=unknown: The "Answer supplied: yes" claim and the quoted run F tool_result line have no retained raw record; the run F transcript was removed before run H, and the retained run F screens still show the open question screen.
F2.2 sev=blocking trigger=B2 ac=T4.AC1 at=.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/harness-feasibility.md:127,132,224,248 anchor=/tmp/createQuestionEv-scratch/gh-stub-dry.log:2 chk=n,y,n,n family=startup-gh-calls-misdescribed fix=list every gh call the stub logged (including issue list -R anthropics/claude-code ...), say which are Claude Code start-up reads, and widen the known-read rule for the fake gh accordingly covers="how each GitHub write path is blocked in a run" first=A2 origin=unknown: The file says the only gh calls in the dry runs are the stub test and Claude Code's own gh auth token, but the stub log also holds an issue list call against anthropics/claude-code at the same second as a start-up auth token.
F1.1 resolved
F1.2 resolved
F1.3 resolved
F2.1 resolved
F2.2 resolved
