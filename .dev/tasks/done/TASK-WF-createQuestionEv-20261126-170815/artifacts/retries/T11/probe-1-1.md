13d4ac5d1aca6c9692fc3c1ec643ec91dd7c2952

## family live-call-wording
defect form: a delivered text says the only live GitHub call of the work is one named read, while the harness also reads the live fork for fork activity
command: grep -n -E -e "live call|live GitHub|no live|only live|one live|live read" .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/pr-notes.md .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/evidence-matrix.md .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-170815/artifacts/gates.md
before:
artifacts/pr-notes.md:18:... The one live call of this work is a read of issue 834's state by the orchestrator ...
artifacts/evidence-matrix.md:3:Every GitHub call of every run went to a fake gh ...
coupled sites: the Decided block line about fork activity (.dev/issues/834/issue-summary.md:58) already says the snapshots exist; pr-notes.md line 18 and evidence-matrix.md line 3 now state the reads

after: live-call-wording
artifacts/pr-notes.md:18: The live calls of this work are reads only, made outside the model sessions ...
artifacts/evidence-matrix.md:3: Every GitHub call made inside a run's model session went to a fake gh (the only live GitHub calls were read-only ...)
