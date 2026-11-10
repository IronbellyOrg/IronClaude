1ae48c764cf7142f1c060c33d14759fad52c5da4
## family apply-row-kinds (F1.1)
defect form: SKILL.md lists the apply row kinds incompletely
command: grep -n -e 'deletion rows' -e 'restore' src/superclaude/skills/sc-fix-audit/SKILL.md
before:
31:4. Apply. Re-runs the check, then makes the one scripted edit (reverts and deletion rows) all or nothing:
coupled sites: the Files list (apply-log.md line)
## family apply-stop-output (F1.2)
defect form: SKILL.md says a bad row prints APPLY_STOP although the re-run check catches it first
command: grep -n -e 'APPLY_STOP' -e 'CHECK_FAIL' src/superclaude/skills/sc-fix-audit/SKILL.md
before:
30:   Any failure prints `CHECK_FAIL <rule> <row>` lines and records `audit: skipped(check failed)`; stop here.
37:   A row that fails an exact-once or overlap test prints `APPLY_STOP: nothing written`; a second run prints `already applied`.
56:- `check.log`: `CHECK_OK` or `CHECK_FAIL` lines, plus `DOWNGRADE` and `UPGRADE` lines
coupled sites: step 3 text (CHECK_FAIL lines)
after (apply-row-kinds):
after: 31:4. Apply. Re-runs the check, then makes the one scripted edit (revert rows plus the `delete` and `restore` edit rows) all or nothing:
after (apply-stop-output):
after: 30:   Any failure prints `CHECK_FAIL <rule> <row>` lines and records `audit: skipped(check failed)`; stop here.
after: 37:   A row that fails an exact-once or overlap test is caught by that re-run check (`CHECK_FAIL K7`, `K8` or `K9` lines, then `audit: skipped(check failed)`); `APPLY_STOP: nothing written` appears only when the apply step itself finds such a failure. Either way the specification is not written. A second run prints `already applied`.
after: 56:- `check.log`: `CHECK_OK` or `CHECK_FAIL` lines, plus `DOWNGRADE` and `UPGRADE` lines
