# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- Colour support is already available through the console's `standard` colour system; ASCII and colour are currently independent policy decisions. Adding styles therefore needs explicit verification of the requested escape-free ASCII fallback, not just ASCII-safe borders. Evidence: `src/superclaude/cli/observe/terminal.py:82-91`, `src/superclaude/cli/observe/terminal.py:110-124`.
- The one-shot width-bound output calls `console.export_text()` without requesting styles, while the interactive `LiveScreen` draws the renderable directly. The render gate must inspect styled screen output rather than use plain one-shot output as proof that colour works. Evidence: `src/superclaude/cli/observe/commands.py:238-244`, `src/superclaude/cli/observe/commands.py:264-274`.
- Existing tests compare colour-enabled and NO_COLOR printed bytes for equality, not only their text content. A styling change needs a deliberate update to that expectation while preserving text equivalence and deterministic output. Evidence: `tests/observe/test_render.py:249-259`.
- The release-1 surface captures both screen lines/printed output and record/snapshot output; the link-off reference compares screen lines exactly. Golden updates must distinguish intentional presentation changes from unintended record/snapshot changes. Evidence: `tests/observe/release1_surface.py:34-60`, `tests/observe/test_linkoff_screen_reference.py:50-75`.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None
