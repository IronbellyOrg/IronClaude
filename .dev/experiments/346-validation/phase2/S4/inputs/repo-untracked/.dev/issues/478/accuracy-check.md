## Accuracy check for #478

**Verdict:** current

Checked against `origin/main` at f1ac0c93ad5a64b03f0ed49866d3adfe140c28b1, and the pull requests merged since the issue was opened (0, list truncated: no).

Static read only; nothing was run. codegraph and auggie were not used; Grep, Glob and Read were used instead. All claims below are still true; none changed or is gone.

| # | Claim in the issue (quoted) | Status today (still true / changed / gone) | Evidence (path:line, PR #number or commit) |
|---|---|---|---|
| 1 | "The image installs `bmad-method` globally and creates a `/usr/local/bin/bmad` wrapper" (`Dockerfile.coder:133-144`) | still true | `templates/VSCode-AIDev02/image/Dockerfile.coder:133-144`: `npm install -g bmad-method@6.9.0` (line 139), wrapper written to `/usr/local/bin/bmad` (lines 142-143) |
| 2 | "The Default profile selects BMAD and IronClaude; the Minimal profile selects only Claude Code" (`profiles.yaml:14-21`) | still true | `templates/VSCode-AIDev02/image/catalogue/profiles.yaml:14-21`: `orca` ("Default") slugs `[claude-code, orca, ironclaude, bmad, mcp-bundle-core]`; `minimal` slugs `[claude-code]` |
| 3 | "Startup runs the BMAD installer only when the profile permits it" (`startup.sh:1163-1176`) | still true | `templates/VSCode-AIDev02/image/scripts/startup.sh:1163-1169` skip on unresolved or out-of-profile; `:1174-1176` runs `( source "${HOME}/.aienv" && bash .../install.sh )` for `bmad`. Also present: `:1113-1117`, a deselected BMad slug's marker is never removed (owner exception). |
| 4 | "The BMAD installer checks for the CLI and configures the recorded seed repo when applicable; it skips configuration if no valid seed repo is recorded or existing BMAD files are detected" (`install.sh:17-25`, `40-46`) | still true | `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:18` CLI check; `:21-25` seed-repo and existing-BMad guards; `:42` `bmad install --yes --directory "${D}" --modules bmm --tools claude-code --output-folder _bmad-output`; `:46` manifest check. Seed path is written only by `startup.sh:673-681`. |
| 5 | "Its manifest instructs users to install BMAD manually in other repos" (`manifest.yaml:12-14`) | still true | `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:12-14` |
| 6 | "Automatic first-use initialization in other projects is unverified." | still true | No code under `templates/VSCode-AIDev02/` runs `bmad install` outside the seed repo (only call site `catalogue/bmad/install.sh:42`). Runtime behaviour UNVERIFIED. |
| 7 | "Documentation says IronClaude pins Ponytail as a Claude Code plugin in its own marketplace" (`docs/operations/upstream-monitor.md:62`) | still true | `docs/operations/upstream-monitor.md:62`; also `.github/upstream-monitor/expected.txt:20` (`IronbellyOrg/IronClaude  DietrichGebert/ponytail  src/superclaude/cli/user_settings_defaults.json`) |
| 8 | "Ponytail's actual installation and exposure mechanism in the reported environment is UNVERIFIED." | still true | No file under `templates/VSCode-AIDev02/` installs or names Ponytail as a plugin (all template matches are `# ponytail:` code comments). The only install path that could carry it is `superclaude install` into `~/.claude` (`catalogue/ironclaude/install.sh:122`); what that writes lives in the IronClaude repo, outside this check. UNVERIFIED. |
| 9 | Environment, steps to reproduce, severity, error messages | Not known yet | The issue gives none. |

### Merged pull requests that touch this issue

| PR | Title | Relevant files | Effect on the issue |
|---|---|---|---|
| none | none merged since 2026-11-07T07:23:55Z | none | none |

<!-- sc:issue:accuracy-check -->
