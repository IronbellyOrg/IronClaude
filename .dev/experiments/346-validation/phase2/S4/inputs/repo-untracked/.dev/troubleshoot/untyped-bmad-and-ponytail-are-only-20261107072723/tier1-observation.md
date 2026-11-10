# Tier 1 observation (static; nothing was executed)

Symptom (issue #478): BMAD and Ponytail are reachable only in projects where the user installed them earlier; they are not installed by default in all projects or global to the user; BMAD used in a never-installed project should create the directories it needs.

No repro available: run-site unobservable (fresh workspace boot cannot be driven from here). Observations below are static reads of the repo and of the already-booted workspace (`/home/coder`). Provenance for each: run=none, arm=static-read, command=Read/Grep/Glob.

## Facts observed in the repo (file:line)

- `templates/VSCode-AIDev02/image/Dockerfile.coder:133-144` installs the BMAD CLI image-wide: `npm install -g bmad-method@6.9.0` and writes the `/usr/local/bin/bmad` wrapper. Only the CLI is image-wide.
- `templates/VSCode-AIDev02/image/catalogue/profiles.yaml:14-21`: the "Default" profile (`orca`) selects `[claude-code, orca, ironclaude, bmad, mcp-bundle-core]`; "Minimal" selects `[claude-code]`.
- `templates/VSCode-AIDev02/image/scripts/startup.sh:1158-1176`: slugs with scope `workspace` or `hybrid` are installed at boot only when in the resolved profile; BMAD is invoked as `( source ~/.aienv && bash <dir>/install.sh )`.
- `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:3`: scope is `hybrid`.
- `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:21-26`: the installer reads `~/.aidev/status/seed-repo-path`; when no seed repo is recorded it only logs "no seed repo recorded; nothing to configure" and still writes its success marker (`:57-60`).
- `templates/VSCode-AIDev02/image/catalogue/bmad/install.sh:42`: the only `bmad install` call is `bmad install --yes --directory "${D}" --modules bmm --tools claude-code --output-folder _bmad-output ...` with `D` = the seed repo; `:32-34` hides `/_bmad/`, `/_bmad-output/`, `/.claude/skills/bmad-*/` through the seed repo's `info/exclude`.
- `templates/VSCode-AIDev02/image/scripts/startup.sh:673-681`: section 8 is the only writer of `seed-repo-path` (set only when the seed clone outcome is `cloned` or `preserved-valid`, removed otherwise).
- `templates/VSCode-AIDev02/image/catalogue/bmad/manifest.yaml:12-14`: the welcome text tells users to run `bmad install --yes --directory . --modules bmm --tools claude-code --output-folder _bmad-output` by hand "for any other repo".
- BMAD installer options (installed package, outside the repo): `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/commands/install.js:14-37` lists `--directory <path>`, `--modules`, `--tools`, `--user-name`, `--yes` and no global/user-scope option. Package version `6.9.0` (`.../bmad-method/package.json`).
- BMAD skills read per-project state: `/home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.claude/skills/bmad-help/SKILL.md:25-26` reads `{project-root}/_bmad/_config/bmad-help.csv` and runs `{project-root}/_bmad/scripts/resolve_config.py`.
- `templates/VSCode-AIDev02/image/Dockerfile.coder:283-353` bakes the IronClaude `superclaude` CLI (pinned by `ARG IRONCLAUDE_GIT_SHA`, line 288).
- `templates/VSCode-AIDev02/image/catalogue/ironclaude/install.sh:121-122`: runs `superclaude install` into `~/.claude` (user-global) when the `ironclaude` slug is selected; manifest says commands, agents, skills and hooks there reach every Claude Code session (`catalogue/ironclaude/manifest.yaml:12-13`).
- No file under `templates/VSCode-AIDev02/` installs or names Ponytail as a product; all 9 case-insensitive hits are `# ponytail:` code comments (grep run on 2026-11-07). Only repo references to Ponytail as a product: `docs/operations/upstream-monitor.md:62` and `.github/upstream-monitor/expected.txt:20`.

## Facts observed outside the repo (this booted workspace; provenance: static read)

- `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/cli/user_settings_defaults.json:29-37` lists `"ponytail@ironclaude": true` in `enabledPlugins`; `:52-70` defines the `ironclaudeMarketplace` catalog that pins plugin `ponytail` to `DietrichGebert/ponytail` ref `v5.3.3`.
- `/opt/uv/tools/superclaude/lib/python3.13/site-packages/superclaude/cli/install_user_setup.py:1-21,44,47` documents that settings defaults fill only unset keys in `~/.claude/settings.json`, the catalog is written to `~/.claude/ironclaude-marketplace/`, and `_RENAMED_PLUGINS` maps `ponytail@ironclaude` to `ponytail@ponytail`.
- `/home/coder/.claude/settings.json:327` has `"ponytail@ironclaude": true` and `:342-347` an `ironclaude` marketplace of source `directory` at `/home/coder/.claude/ironclaude-marketplace`.
- `/home/coder/.claude/plugins/installed_plugins.json:64-70` records `ponytail@ironclaude` v5.3.3 with `"scope": "user"`.
- No `bmad-*` directory exists directly under `/home/coder/.claude/skills/` (Glob of `skills/bmad-*` in `/home/coder/.claude` returned nothing).
- This worktree has `_bmad/_config/manifest.yaml` and `.claude/skills/bmad-help/SKILL.md`: BMAD is project-scoped here.

## Documented owner decisions (parent-read in Wave 1.5; quoted verbatim)

- `_bmad-output/specs/spec-orca-bundle-gap-closure/owner-decisions.md:5`: "OD-1 BMad placement | **Cancelled.** BMad is installed per project only, never globally. | CAP-1 is retired. BMad keeps #207's seed install unchanged, and FR-6 is not pursued."
- `_bmad-output/specs/spec-orca-bundle-gap-closure/.memlog.md:32`: "Owner 2026-09-25: BMad integration work is CANCELLED, because BMad must be installed per project and never globally or at user level. OD-1=A is void."
- `_bmad-output/specs/spec-orca-bundle-gap-closure/.memlog.md:27` (earlier, now void): "OD-1 resolved by owner: A, user-level BMad as the #205 PRD states; the seed repo gets no _bmad/. Gate: a spike must prove BMad resolves from user scope; if it fails, stop and re-raise with the owner."
- `_bmad-output/specs/spec-orca-bundle-gap-closure/SPEC.md:77`: "Any BMad change (FR-6 and the BMad installer's marker and timeout). BMad stays a per-project seed install, exactly as #207 built it." (non-goal)
- `_bmad-output/specs/spec-orca-catalogue-bundle/SPEC.md:141`: "BMad in repos cloned after boot and in Orca-created worktrees. The excluded `_bmad/` is untracked, and worktrees carry only tracked files. Users run the one-command path instead." and `:174`: "Should BMad later reach Orca worktrees, through a tracked install or a worktree-create hook? That is a scope expansion; today it is a non-goal."
- `_bmad-output/planning-artifacts/prds/prd-Coder-orca-bundled-catalogues-2026-09-24/prd.md:154-161` (#205 PRD FR-6) asked for the opposite (user-level BMAD, no Project writes); it was cancelled by the 2026-09-25 owner decision above.
- Ponytail: no document in this repo governs it as a product beyond `docs/operations/upstream-monitor.md:62`.

## Unobserved / UNVERIFIED

- Whether the `ponytail` plugin actually loads in a fresh Default-profile workspace boot (depends on `superclaude install` finishing inside the 60 s limit and its network step; `install_user_setup.py:36-40`). UNVERIFIED.
- Whether a Minimal-profile workspace gets Ponytail: the Minimal profile does not select `ironclaude` (`profiles.yaml:19-21`), so by code no `superclaude install` runs; runtime outcome UNVERIFIED.
- Whether `bmad install --directory "$HOME"` would produce user-level skills Claude Code discovers: UNVERIFIED (not run; BMAD installer behaviour for a home directory not read).
- Which environment the issue author used. UNVERIFIED.
