# Draft notes

Leave a list empty (write "None") when there is nothing to report. The orchestrator asks the user one question only when either list has an item.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). -->

- The image globally installs the BMAD CLI and creates a wrapper (`templates/VSCode-AIDev02/image/Dockerfile.coder:133-144`).
- Default and Minimal profiles select different catalogue slugs; startup filters the BMAD installer by profile (`templates/VSCode-AIDev02/image/catalogue/profiles.yaml:14-21`, `templates/VSCode-AIDev02/image/scripts/startup.sh:1163-1176`).
- The installer checks the CLI and conditionally configures only the recorded seed repo; the manifest directs users to install in other repos manually (`templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:17-25`, `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:40-46`, `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:12-14`).
- Documentation identifies Ponytail as a plugin pinned in IronClaude's marketplace, but its installation and exposure remain unverified (`docs/operations/upstream-monitor.md:62`).
- Possible related issues and their titles/states come from the scout lookup (`.dev/issues/draft-20261107-072128-bmad-and-ponytail-not-accessible-globall/scout.md:28-37`); relevance is not confirmed.
- Static quick pass used Glob, Grep and Read because codegraph and auggie tools were unavailable; runtime was not tested.

## Contradictions

<!-- Each place where the description disagrees with the code, one per line, with path:line evidence. -->

- The description broadly says BMAD is not installed globally; the image does globally install its CLI and provides a wrapper (`templates/VSCode-AIDev02/image/Dockerfile.coder:133-144`). This does not establish global project configuration or disprove the reported experience.
