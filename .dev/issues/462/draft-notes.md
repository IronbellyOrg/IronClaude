# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- In tier mode, ccsession exports alias mappings for tiers the owner may use, including Sonnet to Tier1b; these exports alone do not establish the main session model (`src/superclaude/skills/ccsession-tag/ccsession:880-898`).
- In tier mode, without explicit model or tier, an allowed `ANTHROPIC_MODEL` is selected before the default tier; otherwise the launcher calls `default-tier` (`src/superclaude/skills/ccsession-tag/ccsession:1143-1170`).
- The Orca wrapper recognizes `--model` as a value-taking option (`src/superclaude/skills/ccsession-tag/ccsession-orca:103-108`).
- Previous alias probes and a same-family Sonnet edge case are documented; they do not establish the reported sessions' resolved models (`docs/reference/model-aliases.md:48-56`).
- Closed issue #384 is possibly related, not a confirmed duplicate (`scout.md:21-27`).
- Quick static pass used Glob, Grep and Read; codegraph and auggie tools were unavailable; no runtime probe or tests were run (this investigation).

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- None. The observation has not been verified or disproved by the static configuration review.
