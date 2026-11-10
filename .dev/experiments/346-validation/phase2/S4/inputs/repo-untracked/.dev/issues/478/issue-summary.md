# Summary: #478 [BUG] BMAD and Ponytail not accessible globally by default

- Issue: https://github.com/IronbellyOrg/Coder/issues/478
- Type: bug
- Complexity: complex (rubric: `refs/claim.md`)
- Effort estimate: 20 hours

## What the issue asks for

BMAD and Ponytail should be available to the user in every project by default, not only in projects where they were installed before. When BMAD is used in a project where it was never installed, it should create the directories it needs if they are missing. The issue gives no environment, reproduction steps or error output. It touches two separate mechanisms: the BMad catalogue slug in this repo, and Ponytail, which this repo does not install directly (see below). That is why it is rated complex.

## Relevant files and systems (cheatsheet)

All facts below were read from code at `origin/main` f1ac0c93 (static read; nothing run). They describe the current mechanism, not a cause or a fix.

| Path or system | Why it matters |
|---|---|
| `templates/VSCode-AIDev02/image/Dockerfile.coder:133-144` | Installs the BMad CLI image-wide: `npm install -g bmad-method@6.9.0` and a `/usr/local/bin/bmad` wrapper. Only the CLI is global. |
| `templates/VSCode-AIDev02/image/catalogue/profiles.yaml:14-21` | Default (`orca`) profile includes `bmad` and `ironclaude`; Minimal has only `claude-code`. |
| `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:3,12-14` | Slug scope `hybrid`; welcome text tells users to run `bmad install ... --directory .` by hand in any repo other than the seed repo. |
| `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:18-55` | Boot installer: checks the CLI, then runs `bmad install` only in the recorded seed repo, only if it has no `_bmad/` or tracked `.claude/skills/bmad-*`. Writes `_bmad/`, `_bmad-output/`, `.claude/skills/bmad-*/` inside that repo and hides them via `info/exclude`. |
| `templates/VSCode-AIDev02/image/catalogue/bmad/module.tf` | Terraform module with no `coder_app`; no launch surface. Wired in `templates/VSCode-AIDev02/modules.tf:50-52`. |
| `templates/VSCode-AIDev02/image/scripts/startup.sh:673-681` | §8 writes `~/.aidev/status/seed-repo-path` (the only writer); BMad reads it. |
| `templates/VSCode-AIDev02/image/scripts/startup.sh:692-714,1113-1117,1163-1176` | §9 catalogue installs: profile filter, BMad deselect exception, and BMad's own subshell invocation. |
| `templates/VSCode-AIDev02/image/scripts/lib/spec2-health.sh:77,99-111` | BMad health check looks for `_bmad/_config/manifest.yaml` and the `bmad-*` skills in the seed repo only. |
| `templates/VSCode-AIDev02/image/catalogue/ironclaude/install.sh:122` and `manifest.yaml:12-13` | Runs `superclaude install` into `~/.claude` (user-global). Its welcome text says commands, agents, skills and hooks there reach every Claude Code session. |
| `templates/VSCode-AIDev02/image/Dockerfile.coder:283-352` | Bakes the IronClaude `superclaude` CLI, pinned by `ARG IRONCLAUDE_GIT_SHA` (line 288). |
| `docs/operations/upstream-monitor.md:62`, `.github/upstream-monitor/expected.txt:20` | Only references to Ponytail as a product: IronClaude pins it as a Claude Code plugin in its own marketplace (`src/superclaude/cli/user_settings_defaults.json` in the IronClaude repo). |
| Ponytail install and exposure | No file under `templates/VSCode-AIDev02/` installs or names Ponytail (template matches are `# ponytail:` code comments only). Whether `superclaude install` enables it globally is UNVERIFIED: that code is in IronbellyOrg/IronClaude, outside this check. |
| `templates/VSCode-AIDev02/image/aienv.d/`, `aienv.skel`, `workspace_defaults/CLAUDE.md`, `etc/` | Checked: no BMad, Ponytail or plugin references. |
| `.github/contract-tests/test-19-catalogue-cli-presence.sh`, `test-46-catalogue-health.sh`, `test-57-catalogue-configure.sh`, `test-startup-boot.sh` | Contract tests that mention BMad; any change to its install behaviour reaches these. |
| `templates/VSCode-AIDev02/README.md:241,297-319` | Documents the Default profile and the multi-project workflow (extra repos cloned by hand after boot, which the BMad installer never visits). |

## Analysis

None: the accuracy check found the issue current, so no analysis ran.
