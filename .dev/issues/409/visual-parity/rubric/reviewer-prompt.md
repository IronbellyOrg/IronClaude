# Reviewer prompt for the render gate (one fresh reviewer per width, no resume)

You score one rendered width of the `superclaude observe` screens against the fixed rubric. You do not edit any file. You do not see the author's reasoning.

## Inputs (and only these)

- The rubric: `.dev/issues/409/visual-parity/rubric/rubric.md` (rows RB-01 to RB-29; score only the rows the caller lists as in scope for the phase, and mark every later row `N/A (scheduled P<n>)`).
- For your width W: the mockup references from `.dev/issues/409/attachments/` (`signal-bridge.png`, `attention-ledger.png`, `decision-desk.png`) and the mockup text and ANSI exports inside `.dev/issues/409/orca-observer-design-package.zip` (`orca-observer-20261106/exports/<W>/` and `agent-focus/exports/<W>/`).
- The rendered output for width W from the gate output folder you are given: `<screen>.txt`, `<screen>.<depth>.ansi`, `<screen>.nocolor.txt`, `<screen>.ascii.txt`, the `.png` rasterisations when present, and the folder's `checks.json` (script-checked rows).

## Screen pairing

- `ledger` is scored against `signal-bridge`.
- `questions` is scored against `attention-ledger`.
- `desk` and `desk-planask` are scored against `decision-desk`.

Pairing is for colour, weight, titled borders and pane order only. The mockup title `OPEN HUMAN QUESTIONS` is retired by the spec and is not scored, and facts the screen does not have (owner, requester, mapped trees, SIGNALS bars, affected-session lists) must not be drawn (accepted divergences AD-1 to AD-8 in the spec).

## What to do

- Rows marked "Script" in the rubric are decided by `checks.json`; copy its status and verify one evidence line yourself by Reading the rendered file.
- Rows marked "Reviewer" are yours: read the rendered files and the mockup files and decide.
- A row passes only when every part of its wording holds. One quoted counter-example with its line number fails the row.

## Output

Return only this JSON (a `scores.json` for width W):

```json
{
  "width": 160,
  "iteration": 1,
  "rows": {
    "RB-01": {"result": "PASS|FAIL|N/A", "evidence": "one line: file:line or quoted text"}
  },
  "failing_high_medium": ["RB-.."]
}
```

One evidence line per in-scope row. Do not suggest fixes. Do not edit files.
