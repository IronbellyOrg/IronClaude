# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- WC-13 prohibits worker-session Orca fan-out and leaves further worker decisions to the coordinator; the evaluation should consider this restriction (`src/superclaude/core/WORKER-CONTRACT.md:62`).
- The installed orchestration skill is a discovery stub pointing to an Orca-supplied version-matched guide (`~/.claude/skills/orchestration/SKILL.md:14-18,49-61`); `ls -ld /home/coder/.claude/skills/orchestration` identifies the symlink.
- No matching command or skill was found in the four requested source and installed locations, and a text search found no explicitly named `/sc:orchestrator` specification in `docs/` or `.dev/` outside the issue draft (Glob searches and Grep for `/sc:orchestrator`; `ls -ld` installed paths). This is a bounded search, not proof that no work exists under another name.
- Possible related issues #339, #423 and #431 are unconfirmed matches (`.dev/issues/draft-20261108-044422-evaluate-the-value-implications-and-unlo/scout.md:21-30`).
- The quick pass used Glob, Grep and Read because codegraph and Auggie tools were unavailable; it did not inspect the Orca-supplied guide (session tool availability and `~/.claude/skills/orchestration/SKILL.md:49-61`).

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None. The description calls `/sc:orchestrator` new; its absence in the checked paths does not contradict that description.
