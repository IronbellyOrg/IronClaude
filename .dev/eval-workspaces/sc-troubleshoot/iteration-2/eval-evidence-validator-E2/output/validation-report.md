# Evidence Validation Report

**Report under validation**: /config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/iteration-2/fixtures/evidence-validator/E2-half-wrong-line-draft.md
**Timestamp**: 2026-05-21T06:01:22Z
**Total citations**: 4
**Verified**: 2
**Dropped**: 2
**Passed through (command, no reexec)**: 0
**Suggested report status**: partial

## Verified citations

| # | Type | Location | Verdict |
|---|------|----------|---------|
| 1 | file:line | `.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1476` | verified |
| 2 | file:line | `.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1406` | verified |

## Dropped citations

| # | Type | Location | Reason | Recommended action |
|---|------|----------|--------|--------------------|
| 3 | file:line | `.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:42` | line-mismatch — line 42 in `commands.py` is a blank line (between `from typing import ...` on line 41 and `import click` on line 43); cited snippet `output_dir=output_dir,` is not present in the ±5 window. The snippet does exist verbatim at line 1476 (see citation 1). | remove this citation as duplicative/wrong-line; the underlying claim is already covered by verified citation 1 |
| 4 | file:line | `.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/config.py:999` | file-bounds — `config.py` contains only 260 lines (`wc -l` = 260), so line 999 does not exist. Cited snippet `def resolve_scratch_root(` cannot be located at the cited line. | drop citation; if the report still wants to cite the `resolve_scratch_root` definition, the report-writer should re-locate the actual line in `config.py` (within the 1–260 range) and re-cite |

## Passed-through citations (command, allow_command_reexec=false)

| # | Command | Note |
|---|---------|------|
| — | (none) | no command citations present in draft |

## Notes

- Both dropped citations are file:line errors, not command errors. Pattern: the draft contains a real bug claim grounded by 2 correct citations (1, 2), plus 2 fabricated/wrong-line citations (3, 4) that appear designed to inflate evidence count. This is the failure mode this validator exists to catch.
- Citation 3 is a *line-mismatch where the snippet exists elsewhere in the same file* — the snippet `output_dir=output_dir,` is real and present at line 1476. The report-writer should not re-cite; citation 1 already covers it.
- Citation 4 is a *file-bounds violation*: the cited line is past EOF. The `resolve_scratch_root` symbol may genuinely exist somewhere in `config.py` (within lines 1–260), but the cited line 999 is fabricated. Report-writer must re-locate before re-citing; do not assume the symbol is absent.
- No draft-input pathology detected: the Evidence section was found at the expected locator, citations were parseable, and the draft itself flags citations 3 and 4 as known-bad in inline annotations (which the validator independently confirmed rather than trusted).
- Suggested status `partial` per the protocol's "≥1 dropped → partial" rule.
