# Draft notes

Leave a list empty (write "None") when there is nothing to report. "None" is the empty marker, never an item, and `- None` under both headings is the same state as empty notes. Items under New material cause no question: they are kept in the issue body and printed in the final output. One or more supported items under Contradictions cause exactly one question to the user.

## New material

- The installer orchestrates later retirement steps after installing skills, with a warning if retirement raises; failures affect exit status (src/superclaude/cli/main.py:202-208,257-296).
- The batch installer tracks installed, skipped, command-served and failed skills, and the single-skill installer copies directories (src/superclaude/cli/install_skills.py:83-115; src/superclaude/cli/install_skill.py:52).
- Existing installer and skill tests are in tests/unit/test_cli_install.py:475 and :644.
- Codegraph and Auggie MCP tools unavailable; quick pass used Grep and Read (available tool inventory).
- No possible duplicates found (scout.md:28-33).
- Medium priority follows the planned feature trigger (refs/create.md:73-82).
- Repo IronbellyOrg/IronClaude, base integration, `/sc:implement` then `/sc:pr-submit --monitor 3`, structured count propagation and preserving existing exit behavior are proposed implementation plan (task instructions; src/superclaude/cli/main.py:202-208,285-296).
- Assumption: The count covers successful copies by the batch skill installer in this invocation, excluding skipped, failed and command-served skills; forced reinstalls count as copies. Report the count even if a later phase fails; `--list` remains a listing rather than an install.
- Proposed tests cover fresh, repeat, forced, mixed-failure and later-phase-failure installs and last-line/exit behavior; regression gate and reviewer checks are specified in the test plan (task instructions; src/superclaude/cli/install_skills.py:83-115; src/superclaude/cli/main.py:285-296).
- Assumption: Mock unrelated installer phases to keep tests isolated.

## Contradictions

None
