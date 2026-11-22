# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Listing iterates all workspaces' topics and spawns `head`, an `ls -t` transcript fallback, two `stat` calls and `date` per session row (src/superclaude/skills/ccsession-tag/ccsession:1446-1512, 1362, 1379, 1401, 1415)
- The interactive listing runs on every Orca/Coder terminal open via `ccsession-orca` → `ask_session_name()` (ccsession:1538-1565)
- Every launch also does a model-data freshness check against IronClaude, bounded at ~2 seconds and cached (ccsession:114-116)

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None
