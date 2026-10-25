# Detection-contract readiness: UNAVAILABLE

- Request: detection-contract readiness for `synthetic/example` PR #1 (`--no-promote`)
- Status: **UNAVAILABLE** (stopped on a precondition). No UC-1/UC-2 audit was run.
- Reason: the `superclaude` package executable is not installed. `command -v superclaude` found nothing on PATH, and the plugin does not bundle it.
- Protocol basis: `plugin/skills/sc-reflect-protocol/SKILL.md:91-95` and `:148-157` (readiness bypass)
- Command to run once the package is installed: `superclaude reflect contract-status [--validate] --repo synthetic/example --pr 1`
- Not done: no package code was imported, nothing was installed, the CLI was not impersonated, no agents were delegated, no promotion or moves happened, and the PR state was not touched.
- Audit root recorded: `fixtures/project` (git init only, no commits). Nothing in it was read or modified for this request.
