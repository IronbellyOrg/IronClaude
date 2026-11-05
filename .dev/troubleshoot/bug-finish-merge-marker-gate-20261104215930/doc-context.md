# Documentation Context Card

## Release context
No release artifact under .dev/releases scopes this script; the controlling artifact is the design package .dev/tasks/done/TASK-WF-design-20261104-164423/source.md (sections 4.6, 7.2). Branch A confidence 0.7.

## Architectural docs consulted
- .dev/tasks/done/TASK-WF-design-20261104-164423/source.md (currency: unknown; CAUTION: no header markers) - 7.2 step 4 pins the 7-wide regex (:817); step 5 compares blob ids only (:818).
- src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md (currency: unknown; CAUTION) - step 9 finish gate and token table (:103-120); merge command without marker-size override (:76).
- src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md (currency: unknown; CAUTION) - :60 "Remove every conflict marker".

## Restrictions / decisions that constrain the fix
- Reuse tokens `markers` (A1) and `staged_unexpected` (C2); no new token (source.md:824; finish-merge.sh:24-26).
- One stdout line, details on stderr, exit 0/2, set -u -o pipefail, no stdin/prompt, temp files under the git dir (source.md:756).
- Read-only additions only; the script changes the repository only through its one commit (source.md:797).
- `--no-renames` on every diff feeding the gate (INV-016, source.md:1176).
- Step 4 stays a relative count (stage-1 markers are not "introduced"; F3 test).
- Static text rules: no stash/force words anywhere, exactly one `git commit` match, no git add/checkout/reset/config, no gh (test_conflict_scripts.py:1068-1088).

## Re-frame signals
- Both findings are design gaps that the script follows faithfully; the fix extends the gate toward its stated purpose ("changes nothing beyond the auto-merge result plus the resolved paths", source.md:818).
- The widened marker match must keep F2/F3 semantics; the mode check must keep F4/F5 (path on stderr).
