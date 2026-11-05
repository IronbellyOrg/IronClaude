# Documentation Context Card

**Generated**: 2026-11-04T15:06Z
**Wave**: 1.5
**Scope**: src/superclaude/hooks/scripts/block-bare-python.sh:101

## Release context

- **Release**: TASK-WF-implementIronbel-20261104-130647 (issue #357 workflow plan; no PRD/TDD/spec in .dev/releases)
- **Artifacts**: .dev/tasks/done/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md, source.md, artifacts/amendments.md
- **Summary**: The plan fixes the exit-code / fail-open contract, the wrapper list (with options and the timeout duration) and the rule that text that only mentions python is never blocked. ANSI-C escape decoding, long options with a separate argument and `[[ ]]` are not specified; the plan's tests do not cover them.
- **Confidence**: 0.85

## Architectural docs consulted

- `src/superclaude/hooks/scripts/block-bare-python.sh` (header 1-50): verdict `current`. It promises $'...' tracking and wrapper skipping "with their options"; none of the three defects is a listed ceiling or false positive.
- `CHANGELOG.md` (#357 entry, 7-16): verdict `current`. Wrapped commands are "checked word by word"; Known limits do not list the three defects.
- `docs/developer-guide/technical-architecture.md`: verdict `unknown`. Does not describe this hook (documentation gap).

> CAUTION: docs/developer-guide/technical-architecture.md is unknown per the Section 2 currency check; treat its claims as advisory, not authoritative.

## Restrictions / decisions that constrain the fix

- `src/superclaude/hooks/scripts/block-bare-python.sh:10` (contract): "allow -> exit 0; block -> one message on stderr + exit 2; never exit 1."
- `src/superclaude/hooks/scripts/block-bare-python.sh:13` (scanner): "blocks only when the scanner positively reports a bare command word."
- `src/superclaude/hooks/scripts/block-bare-python.sh:14` (hook): "The hook itself runs no Python."
- plan :19 (Done-when): "does not block commands that only mention python in arguments, paths or quoted text"
- plan :37 (quotes): "Text inside single quotes, and text inside double quotes, is never a command word"
- plan :38 (wrappers): env and timeout "plus its following options", timeout "plus its options and its duration argument", `command -v`/`-V` stays allowed.
- plan :41 (performance): awk or jq tokenising, 100 KB well under 3 s; `tests/hooks/test_block_bare_python.py:204` "assert elapsed < 1".
- plan :46 and `tests/cli/test_install_hooks.py:785`: plugin mirror byte-identical and executable.

## Re-frame signals

- The three defects are deviations from the documented contract (header lines 19 and 24-28, CHANGELOG "checked word by word", plan Done-when line 19), not documented behaviour: proceed with a code fix.
- Any fix must keep the fail-open contract, stay in awk (no Python), keep the 100 KB timing test green, and update the plugin mirror byte-for-byte; the hook header ceilings and CHANGELOG limits should be updated to match.
