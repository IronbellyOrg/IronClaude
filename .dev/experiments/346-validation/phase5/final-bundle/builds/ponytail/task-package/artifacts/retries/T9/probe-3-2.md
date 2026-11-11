7987ab62e0024258b9bd4ad4197ddcc89dbbee48
## family doc-claim-vs-code (F3.2)
written before the brief-4 run; before-output from the checkpoint tree a3=67547a4f2dcc57e6e873f36bd231fef8c731c146 (the Q0-rebuilt tree has no note)
defect form: the note states what a step prints or does on failure, or a count rule, more broadly than fix_audit.py does
command: grep -n -i -e 'APPLY_STOP' -e 'CHECK_FAIL' -e 'nothing written' -e 'byte-identical' -e 'every failure' -e 'on failure' -e 'Not covered' -e 'adds every' -- docs/designs/spec-panel-ponytail.md
before:
31:- What each step does on failure:
34:  - An exact-once or overlap failure prints `APPLY_STOP: nothing written` and the specification is not written.
35:  - If the specification write or its read-back fails, the script tries to copy `current-before-audit.md` back over the specification, then prints `APPLY_STOP: nothing written (write failed: ...)`.
36:  - Not covered: if writing `apply-log.md` or `closed-minor.txt` fails after the specification was replaced, the specification stays edited and `state.json` still says `checked`. Restore it by copying `fix-audit/current-before-audit.md` onto the s
44:Owner decision: findings that the script defers (reverted, listed in `closed-minor.txt`) or demotes (logged `DOWNGRADE`) stay open in the success measure. `final-verdict.md` prints `held open (deferred or demoted): ...`, `review-3 new critical+maj
80:In S1 a pure one-line name substitution does not work, so the briefs T05-T09 stay byte-identical and one Task T08a is inserted between T08 (cycle-2 reviser) and T09 (review 3). Its single command line is:
coupled sites: Owner count paragraph (held id counting, fix_audit.py:1057-1062); What it is paragraph (atomic write, K1); src/superclaude/skills/sc-fix-audit/SKILL.md:37 (out of T9 scope, not edited)
after (doc-claim-vs-code F3.2):
after: 32:What each step prints, on success and on failure, is listed in the `sc-fix-audit` skill (`~/.claude/skills/sc-fix-audit/SKILL.md`); this note does not repeat it.
