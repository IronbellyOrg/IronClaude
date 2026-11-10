7987ab62e0024258b9bd4ad4197ddcc89dbbee48
## family doc-claim-vs-code (F2.1)
written late: after the brief-3 run, not before it (process slip, recorded here); before-output taken from the checkpoint tree a2=f45b735179daa0fc17e0bcad216762cadc9333b3, since the Q0-rebuilt tree has no note
defect form: a blanket failure-path guarantee in the note that the live apply/check code does not keep
command: grep -n -i -e 'every failure' -e 'byte-identical' -e 'all or nothing' -e 'nothing written' -- docs/designs/spec-panel-ponytail.md
before:
7:One fix audit per review loop, at the end of fix cycle 2: after the reviser applies the cycle-2 fixes and before review 3. It runs as its own step, `/sc:spec-panel-ponytail @<spec> --fix-audit --re-review <review-2 report> --baseline <copy review 2 saw>`, in a fresh session that is neither the rev
31:- Every failure path leaves the specification byte-identical to `current-before-audit.md`.
75:In S1 a pure one-line name substitution does not work, so the briefs T05-T09 stay byte-identical and one Task T08a is inserted between T08 (cycle-2 reviser) and T09 (review 3). Its single command line is:
coupled sites: docs/designs/spec-panel-ponytail.md What it is paragraph (all-or-nothing wording); Safe apply first bullet (auditor writes only audit.md); fix_audit.py:727-737, :785-794, :876-882, :898-903 (not edited by T9)
after (doc-claim-vs-code):
after: 34:  - An exact-once or overlap failure prints `APPLY_STOP: nothing written` and the specification is not written.
after: 35:  - If the specification write or its read-back fails, the script tries to copy `current-before-audit.md` back over the specification, then prints `APPLY_STOP: nothing written (write failed: ...)`.
after: 80:In S1 a pure one-line name substitution does not work, so the briefs T05-T09 stay byte-identical and one Task T08a is inserted between T08 (cycle-2 reviser) and T09 (review 3). Its single command line is:
