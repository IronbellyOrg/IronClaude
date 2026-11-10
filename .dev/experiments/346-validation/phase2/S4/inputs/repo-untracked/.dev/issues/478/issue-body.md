## Bug Summary

BMAD and Ponytail are reported to be accessible only in projects where the user previously installed them, rather than being available globally by default.

## Environment (OS, version)

- OS: Not known yet
- Version: Not known yet

## Current Behavior

BMAD and Ponytail are reported not to be available by default across projects; they are accessible in projects where the user has previously installed them.

## Expected Behavior

BMAD and Ponytail should be available globally to the user across projects by default. When BMAD is accessed in a project where it has never been used or installed, it should create the directories needed to function if they do not already exist.

## Steps to Reproduce

1. Not known yet

## Impact Assessment (Severity, Blast Radius)

- Severity: Not known yet
- Blast Radius: Users accessing BMAD or Ponytail in projects where they have not previously installed them, as reported.

## Error Messages

```text
Not known yet
```

## Codebase Context (from `/sc:analyze`)

### Findings from the current code (verified by file:line)

Static read only; nothing was run. These are facts, not a root cause or a fix. The image does install the BMAD CLI globally, so the gap described above concerns project setup and global availability of the BMAD and Ponytail assets, not the CLI binary.

- The image installs `bmad-method` globally and creates a `/usr/local/bin/bmad` wrapper; this establishes CLI installation, not automatic project setup or runtime availability in the reported environment (`templates/VSCode-AIDev02/image/Dockerfile.coder:133-144`).
- The Default profile selects BMAD and IronClaude; the Minimal profile selects only Claude Code (`templates/VSCode-AIDev02/image/catalogue/profiles.yaml:14-21`). Startup runs the BMAD installer only when the profile permits it (`templates/VSCode-AIDev02/image/scripts/startup.sh:1163-1176`).
- The BMAD installer checks for the CLI and configures the recorded seed repo when applicable; it skips configuration if no valid seed repo is recorded or existing BMAD files are detected (`templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:17-25`, `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:40-46`). Its manifest instructs users to install BMAD manually in other repos (`templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:12-14`). Automatic first-use initialization in other projects is unverified.
- Documentation says IronClaude pins Ponytail as a Claude Code plugin in its own marketplace (`docs/operations/upstream-monitor.md:62`); Ponytail's actual installation and exposure mechanism in the reported environment is UNVERIFIED.
- Quick static pass only; codegraph and auggie tools were unavailable, so Glob, Grep and Read were used. Runtime behavior was not tested.

## Related Issues

Possibly related, not confirmed duplicates: #204, #202 and #216 concern earlier Orca bundle work involving BMAD; #264 concerns default Orca values on new install; #432 is an open owner-questions issue. Relevance to this specific behavior is unverified.

## Testing Notes

Not known yet

<!-- sc:issue:create template=issue-bug-simple -->
