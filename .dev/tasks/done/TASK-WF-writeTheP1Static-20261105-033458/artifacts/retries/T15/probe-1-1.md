# T15 family probe for family=lint-warn-claim (before the fix)

Family: a "new WARN" / "new size warning" claim, or a new-vs-existing comparison keyed on the full warning line (which includes the line count), so a grown existing warning reads as new.

Probe command: `grep -n -i 'new WARN\|new size warning\|WARN' p1-static-report.md lint-format-compare.md` plus a read of the generator logic that builds the compare file.

Hits:
- p1-static-report.md:15 "one new WARN recorded below"
- p1-static-report.md:21 "shows a new size warning for brainstorm.md (217 lines ...) ... The total warning count stays 5."
- lint-format-compare.md:5 "New WARN lines (recorded, do not fail): 1" and :6 the brainstorm.md line
- Generator (`/tmp/p1_impl/t15_compare.py`, lint part): `new_warn = c_warn - b_warn` compares whole lines, so the changed line count made the same warning look new. This is the cause; the fix keys warnings by file name and reports a changed count as "grew".

Other warnings (reflect.md, spawn.md, spec-panel.md, troubleshoot.md): identical lines in baseline and current, no claim made about them.

No other file in the package says "new WARN". `p1-static-report.md` is the only report; `ac-c3-compare.md` and `wider-compare.md` make no WARN claim.
