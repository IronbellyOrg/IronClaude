# Evidence Validation Report

**Report under validation**: /config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/iteration-2/fixtures/evidence-validator/E1-all-verified-draft.md
**Timestamp**: 2026-05-21T06:01:19Z
**Total citations**: 3
**Verified**: 2
**Dropped**: 1
**Passed through (command, no reexec)**: 0
**Suggested report status**: partial

## Verified citations

| # | Type | Location | Verdict |
|---|------|----------|---------|
| 1 | file:line | `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1476` | verified |
| 2 | file:line | `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/commands.py:1406` | verified |

## Dropped citations

| # | Type | Location | Reason | Recommended action |
|---|------|----------|--------|--------------------|
| 1 | file:line | `/config/workspace/IronClaude/.dev/eval-workspaces/sc-troubleshoot/evals/fixtures/real-bug-scratch-root/config.py:1` | snippet-mismatch — cited snippet `"""Scratch-root resolution and allowlist policy."""` does not match actual line-1 content `"""EvalConfig — frozen configuration dataclass for the cliEval harness.`. Semantic difference in docstring text. | Remove citation or update to quote the actual top-of-file docstring text. The draft's parenthetical hedge ("check whatever real content is at line 1") acknowledges uncertainty; the literal quoted snippet is the citation under test and it does not match. |

## Passed-through citations (command, allow_command_reexec=false)

(none)

## Notes

- The first two citations (commands.py:1476 and commands.py:1406) match the actual file content exactly and corroborate the diagnosis that `eval_run` passes `output_dir=output_dir` to `resolve_scratch_root`.
- The third citation has a clearly mismatched quoted snippet. The hedge in parentheses indicates the report author was not confident in the exact line-1 content; per protocol, the cited snippet is what is validated, and it does not match. The underlying claim (config.py begins with a docstring) is true, but the quoted text is wrong.
- This citation appears low-value to the diagnosis — config.py:1 is not the locus of the bug; the bug is in `resolve_scratch_root`'s handling of the `output_dir` kwarg (in config.py somewhere, presumably) and the call site at commands.py:1476. Recommend the report-writer either (a) drop citation 3 entirely as orthogonal, or (b) replace with a real `resolve_scratch_root` snippet showing the allowlist self-extension.
- No draft input pathology — Evidence section present and parseable.
