# Read-only Orca command discovery

## Command provenance
Commands executed from the review worktree on 2026-11-06. No installation or launch was executed.

- `orca skills get orca-cli --json`: exit 0. Selected `orca` from the installed discovery stub because this is an Orca-managed terminal and no executable override or dev-root override was set.
- `orca-ide skills install --help`: exit 0. This exact discovery command is named by the plan; it reads bundled help only.

## Agent-launch guide excerpt
The returned version-matched guide states:

> `worktree create --agent` (new checkout) and `agent launch` (existing worktree) are how to start an agent.

> `--surface chat|terminal` picks one for that launch instead of the setting; pass it only when the user asked for a chat or a terminal.

> `terminal create` makes a terminal for shells and commands.

## Installer help excerpt
The returned help states:

> Only copies Orca wrote and nobody changed are updated. A copy you changed, or a different skill with the same name, is skipped and is reported; --force replaces it after moving it to a backup under ~/.agents/.orca-skill-backups.

> Use --dry-run to print what would change and the plan digest without writing; a real run plans again and writes only if the plan still matches.

> Exits 1 when a location failed or changed while it ran; skipped folders are warnings.

The displayed generic option description for `--force` says worktree removal, while the installer-specific note describes replacement of edited skills. The specific note suffices to establish that forwarding `--force` is unsafe for the source's preserve-edits requirement. The review did not invoke it.

## Limits
No UI success, guide refresh, dry run, historical shell behavior, or incident cause is established by these help reads. Gateway model aliases do not establish actual vendor diversity.
