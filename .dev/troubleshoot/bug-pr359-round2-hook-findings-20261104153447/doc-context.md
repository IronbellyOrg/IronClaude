# Documentation Context Card

**Generated**: 2026-11-04T15:36:43Z
**Wave**: 1.5
**Scope**: src/superclaude/hooks/scripts/block-bare-python.sh:120

## Release context
- **Release**: TASK-WF-implementIronbel-20261104-130647 (issue #357 plan; nothing in .dev/releases)
- **Artifacts**: .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md, .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/artifacts/amendments.md
- **Summary**: The plan requires one awk scanner tracking quotes, backticks and $( as nested contexts and honours backslash escapes; it does not mention [[ ]], process substitution or backticks inside $(( )).
- **Confidence**: 0.85

## Architectural docs consulted
- `src/superclaude/hooks/scripts/block-bare-python.sh` (header) — verdict: `current` — promises process substitution, $(( )) and [[ ]] handling; none of the three defects is a listed ceiling.
- `CHANGELOG.md` (#357 entry) — verdict: `current` — process substitution checked word by word; [[ ]] words are not commands.
- `CLAUDE.md`, `KNOWLEDGE.md`, `docs/` — verdict: `unknown` — nothing on this hook.
> CAUTION: CLAUDE.md, KNOWLEDGE.md and docs/ are unknown per the Section 2 currency check; treat their claims as advisory, not authoritative.

## Restrictions / decisions that constrain the fix
- `src/superclaude/hooks/scripts/block-bare-python.sh:10` (contract) — "allow -> exit 0; block -> one message on stderr + exit 2; never exit 1."
- `.dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md:37` (quotes) — "Backslash escapes outside single quotes are honoured when tracking quotes." (a quoted or escaped [[ is literal)
- `.dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md:41` (performance) — awk or jq only, 100 KB well under 3 s; `tests/hooks/test_block_bare_python.py` 100 KB case under 1 s.
- `.dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md:32` and `tests/cli/test_install_hooks.py:785` — byte-identical, executable mirror.

## Re-frame signals
- All three defects contradict the hook header (lines 21-25) and the CHANGELOG: proceed with a code fix inside the awk scanner, mirrored byte-for-byte.
