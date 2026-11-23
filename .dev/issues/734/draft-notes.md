# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Assumption: the Reviser's spec edits in an unattended fix cycle are handled either as edits to a copy under the report directory or by returning the Reviser brief to the coordinator; the sources read (command file, SKILL.md, WORKER-CONTRACT.md) do not settle it, so the issue names both and leaves the choice to the plan. Source: ~/.claude/skills/sc-spec-panel-stoprule-protocol/SKILL.md S9/failure table; ~/.claude/WORKER-CONTRACT.md WC-2/WC-6.
- Assumption: under `--unattended` the worker session runs both columns of the step table (protocol already allows the no-coordinator one-session form), and the S4 grader batches and S6 audit become the worker's own Agent-tool fan-out (WC-7 keeps a command's Agent fan-out). Source: SKILL.md "Who runs which step (owner ruling)" paragraph; WORKER-CONTRACT.md WC-7.
- Assumption: `src/superclaude/commands/spec-panel-stoprule.md` and `src/superclaude/skills/sc-spec-panel-stoprule-protocol/` are the source-of-truth paths (CLAUDE.md sync rule); only the installed `~/.claude/` copies were read (dual-surface rule), the `src/` copies were UNVERIFIED (not read).
- Assumption: `tests/skills/test_worker_contract.py` needs its converted-command set and exact counts updated; its current P-set constant names and count values were only greped, not read in full (UNVERIFIED beyond the grep).
- Assumption: `--mode discussion` counts as a person-mode flag refused under `--unattended` (it writes dialogue, not a verdict-carrying critique report); only `--mode critique` is the loop mode. Source: ~/.claude/commands/sc/spec-panel-stoprule.md "Review Loop" ("critique mode only") and "Cap" section.
- Priority reason wording and Related-Issues framing (blocks #731/#733, workaround exists) taken from the description and the #733 spec (UI-24, OD-1) at .dev/brainstorms/20261123-implement-unattended/SPEC.md.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None
