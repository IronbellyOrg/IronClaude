# Scan B — technical docs

Scope: docs/developer-guide/*.md, docs/reference/*.md, docs/dev/*.md, docs/mcp/*.md, docs/sprint-budget-architecture.md, docs/sprint-cli-deep-dive.md, docs/eval/*.md, docs/swarm/{runbook,operator-runbook,rollback-procedure,observability-procedure,transport-limits,env-readiness,monitoring-patterns}.md, KNOWLEDGE.md, CONTRIBUTING.md, src/superclaude/rules/core/changelog_maintenance.md.
Tree: HEAD d953b983 (tag v5.0.0). Read-only scan. Ground truth: CHANGELOG.md `## [5.0.0]`, docs/releases/v5.0.0.md, .dev/releases/current/v5.0.0/DECISIONS.md.
Tags: [CODE-VERIFIED] / [CODE-CONTRADICTED] / [UNVERIFIED]. Tables list only CONTRADICTED and UNVERIFIED claims.

## Code facts used across sections

- Package version 5.0.0: `pyproject.toml:7`. CLI version string is `superclaude --version` / `superclaude version` (`src/superclaude/cli/main.py:19`, `:514`); prog_name "SuperClaude".
- No `src/superclaude/__main__.py` exists, so `python -m superclaude` has no module entry point, and `python3 -m SuperClaude` (capital S) cannot import on a case-sensitive file system.
- `superclaude install` options are only `--target`, `--force`, `--list` (`src/superclaude/cli/main.py:29-46`). No `--components`, `--list-components`, `--diagnose`, `--install-dir`, `--fresh`; no `backup` or `uninstall` subcommands (`main.py:521-561` lists every subcommand group).
- Install from the fork: `pipx install git+https://github.com/IronbellyOrg/IronClaude` (repo CLAUDE.md, docs/releases/v5.0.0.md); the PyPI `superclaude`/`SuperClaude` package is upstream. Upgrade path: `update.sh:7-8` runs `pipx install --force ./` then `superclaude install --force`; `superclaude update` (`main.py:340-360`) only re-copies files from the installed package and does not upgrade it. Python `>=3.10` (`pyproject.toml:16`).
- MCP registry (`src/superclaude/cli/install_mcp.py:43-113`): context7 = `npx -y @upstash/context7-mcp`, playwright = `npx -y @playwright/mcp@latest`, morphllm-fast-apply = `npx -y @morphllm/morphmcp`, tavily, auggie (Node 20+, `:87`), codegraph, litellm (HTTP). npm servers need Node 18+ (`install_mcp.py:515`). No Magic/21st server in the registry.
- `src/superclaude/rules/` is installed to `~/.claude/rules/` (`src/superclaude/cli/install_user_setup.py:94-97`), so `changelog_maintenance.md` is an installed primitive.
- `.gitignore:127-128` ignores `.claude/*` except `settings.json`, so `.claude/changelogs/` is git-ignored. `.claude/changelogs/` does not exist in the tree.
- `/sc:analyze` flags: `--focus`, `--depth`, `--format` only (`src/superclaude/commands/analyze.md:22`). `--no-mcp` appears only in `commands/reflect.md` and `commands/troubleshoot.md`. `--all-mcp` appears in no command or core file.
- Core files at 5.0.0 (`src/superclaude/core/`): BASH_INSPECTION_POLICY, BUSINESS_PANEL_EXAMPLES, BUSINESS_SYMBOLS, CLAUDE, CODEGRAPH, HOW-WE-WORK, ISSUE-BACKLOG, ISSUE-HANDOFF, PRINCIPLES, RESEARCH_CONFIG, RULES (.md). No ORCHESTRATOR/COMMANDS/PERSONAS/MODES/FLAGS/MCP.md.

## src/superclaude/rules/core/changelog_maintenance.md

Describes: the mandatory changelog and release-notes process (Keep a Changelog, SemVer, detailed release-notes files, tagging, GitHub release). Installed to `~/.claude/rules/core/`.
Verdict: STALE — conflicts with decision 7.3 in five places and its GitHub-release command can target the upstream parent.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 107 | Detailed release notes are saved to `.claude/changelogs/` | [CODE-CONTRADICTED] | `.gitignore:127-128` (`.claude/*`, only `!.claude/settings.json`); DECISIONS.md 7.3; `docs/releases/v5.0.0.md` exists | Save to `docs/releases/vX.Y.Z.md` (tracked). |
| 115 | CHANGELOG links `[.claude/changelogs/YYYY-MM-DD_vX.Y.Z_DESCRIPTION.md]` | [CODE-CONTRADICTED] | CHANGELOG.md 5.0.0 intro links `docs/releases/v5.0.0.md` | Link `docs/releases/vX.Y.Z.md`. |
| 134-136 | `gh release create vX.Y.Z --title ... --notes-file .claude/changelogs/...` | [CODE-CONTRADICTED] | DECISIONS.md 7.3 (`--notes-file docs/releases/v5.0.0.md`); repo CLAUDE.md "PR Target = Fork" (gh defaults to the fork's parent) | `gh release create vX.Y.Z --repo IronbellyOrg/IronClaude --title "..." --notes-file docs/releases/vX.Y.Z.md`. Missing `--repo` lets gh pick `SuperClaude-Org/SuperClaude_Framework`. |
| 35, 139, 168, 184 | A human reference `.claude/changelogs/README.md` exists (section 4 = web UI steps) | [CODE-CONTRADICTED] | `.claude/changelogs` absent from tree; git-ignored path | No such file; drop the link or point to `docs/releases/`. |
| 166 | Detailed files live at `.claude/changelogs/YYYY-MM-DD_vX.Y.Z_DESCRIPTION.md` | [CODE-CONTRADICTED] | as line 107 | `docs/releases/vX.Y.Z.md` (naming is `vX.Y.Z.md`, not dated). |
| 37, 105, 167 | Template at `.claude/templates/workflow/changelog_template.md` | [UNVERIFIED] | Source is `src/superclaude/templates/workflow/changelog_template.md`; installed copy goes to `~/.claude/templates/`; project `.claude/templates/` exists only after `make sync-dev` (absent in this tree) | Use `~/.claude/templates/workflow/changelog_template.md` (installed path). |
| 60-70, 141-149 | Every change goes into an `## [Unreleased]` section | [UNVERIFIED] | CHANGELOG.md 5.0.0 says it is "the first versioned section"; whether an Unreleased header is kept after the tag was not checked in this slice | Confirm against CHANGELOG.md head. |
| 126-127 | `git push origin vX.Y.Z` | [CODE-VERIFIED] | origin = fork per repo CLAUDE.md | — |

Verified claims: 3 (SemVer rules, tag command, CHANGELOG.md at repo root).

## docs/reference/common-issues.md

Describes: quick fixes for install, permission, MCP and missing-component problems.
Verdict: STALE — every install and verification command targets the upstream 4.1.5 package and an install CLI that no longer exists.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 18, 83 | `python3 -m SuperClaude --version` shows 4.1.5 | [CODE-CONTRADICTED] | `pyproject.toml:7` = 5.0.0; no `__main__.py`; `main.py:19` | `superclaude --version` prints 5.0.0. |
| 22, 25 | Upgrade with `pipx upgrade SuperClaude` / `pip install --upgrade SuperClaude` | [CODE-CONTRADICTED] | PyPI package is upstream (repo CLAUDE.md) | In a clone: `git pull` then `./update.sh` (`update.sh:7-8`: `pipx install --force ./` + `superclaude install --force`); or `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install --force`. `superclaude update` only re-copies files from the already-installed package (`main.py:340-360`). |
| 28 | Reinstall with `python3 -m SuperClaude install` | [CODE-CONTRADICTED] | no `__main__.py` | `superclaude install` (`--force` to overwrite). |
| 36, 39, 71, 78 | `pipx install SuperClaude`, `pip install --user SuperClaude`, `pip3 install SuperClaude` | [CODE-CONTRADICTED] | upstream package name | `pipx install git+https://github.com/IronbellyOrg/IronClaude`. |
| 48 | `/sc:analyze . --no-mcp` | [CODE-CONTRADICTED] | `commands/analyze.md:22` flags = `--focus --depth --format` | No `--no-mcp` on `/sc:analyze`; remove. |
| 49 | Node.js 16+ | [CODE-CONTRADICTED] | `install_mcp.py:515` (18+), `:87` (auggie 20+) | Node.js 18+ (20+ for Auggie). |
| 55 | `install --components core commands agents modes --force` | [CODE-CONTRADICTED] | `main.py:29-46` (no `--components`); MODES.md removed in 5.0.0 | `superclaude install --force`. |
| 64 | `--install-dir` on Windows | [CODE-CONTRADICTED] | `main.py:30-34` only `--target` (commands dir) | No such option; Windows support [UNVERIFIED]. |
| 85 | `SuperClaude install --list-components` | [CODE-CONTRADICTED] | `main.py:40-44` | `superclaude install --list`. |

Verified claims: 2 (restart Claude Code; `chown ~/.claude`).

## docs/reference/troubleshooting.md

Describes: troubleshooting from quick fixes to diagnostics, plus a freshness-hook section.
Verdict: STALE outside the freshness-hook section (lines 106-140 are current).

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 10, 25, 73 | `python3 -m SuperClaude --version` shows 4.1.5 | [CODE-CONTRADICTED] | `pyproject.toml:7`; no `__main__.py` | `superclaude --version` → 5.0.0. |
| 11, 27 | `SuperClaude install --list-components` | [CODE-CONTRADICTED] | `main.py:40-44` | `superclaude install --list`; MCP state: `superclaude mcp --list`. |
| 37-59 | Install/uninstall `SuperClaude` via pipx/pip (incl. `--break-system-packages`) | [CODE-CONTRADICTED] | upstream package | `pipx install git+https://github.com/IronbellyOrg/IronClaude`. |
| 65 | `install --components core commands agents modes --force` | [CODE-CONTRADICTED] | `main.py:29-46`; MODES.md removed | `superclaude install --force`. |
| 84-85 | `/sc:analyze . --no-mcp`, `--scope file` | [CODE-CONTRADICTED] | `commands/analyze.md:22` | Neither flag exists on `/sc:analyze`. |
| 93 | MCP config is `~/.claude/.claude.json` | [UNVERIFIED] | installer uses `claude mcp add --scope user` (Claude Code stores user scope in `~/.claude.json`, not under `~/.claude/`) | `claude mcp list`. |
| 94-95 | Node 16+; `SuperClaude install --components mcp --force` | [CODE-CONTRADICTED] | `install_mcp.py:515`; `main.py:284-304` | Node 18+; `superclaude mcp --servers <name>`. |
| 98-102 | Magic needs `TWENTYFIRST_API_KEY` | [CODE-CONTRADICTED] | no magic entry in `install_mcp.py:43-113` | Magic is not a shipped server; keep only `MORPH_API_KEY`. |
| 106 | Heading "Freshness Hook Issues (v4.3+)" | [UNVERIFIED] | 4.3.x was never tagged (CHANGELOG 5.0.0 intro) | Drop the version tag or say 5.0.0. |
| 121 | `~/.claude/hooks/freshness-*.sh` = 7 files | [CODE-VERIFIED] | `src/superclaude/hooks/scripts/` has 7 `freshness-*.sh` | — |
| 147-148 | `SuperClaude install --diagnose`; `~/.claude/logs/superclaude.log` | [CODE-CONTRADICTED] | no `--diagnose` (`main.py:29-46`); `superclaude doctor` exists (`main.py:472-477`) | `superclaude doctor --verbose`. |
| 161-163 | `SuperClaude backup --create`, `uninstall`, `install --fresh` | [CODE-CONTRADICTED] | no such subcommands (`main.py:521-561`) | `superclaude install --force` / `superclaude update`. |
| 175 | Issues go to SuperClaude-Org/SuperClaude_Framework | [CODE-CONTRADICTED] | repo CLAUDE.md (fork = IronbellyOrg/IronClaude) | `https://github.com/IronbellyOrg/IronClaude/issues`. |

Verified claims: 9 (freshness hooks section 106-140, restart guidance, `@agent-security` per `agents/security-engineer.md:9`).

## docs/reference/mcp-server-guide.md

Describes: MCP troubleshooting; a current codegraph section (13-44) followed by legacy npm-global troubleshooting.
Verdict: PARTIAL — codegraph section current; the rest uses wrong package names, Node versions and a removed install CLI.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 13-16 | Available servers: codegraph, Context7, Playwright, Morphllm | [CODE-CONTRADICTED] | `install_mcp.py:43-113` also ships tavily, auggie, litellm (+ AIRIS gateway line 21) | List all registry servers. |
| 52, 85, 152, 614 | Node.js 16+ | [CODE-CONTRADICTED] | `install_mcp.py:515` | 18+ (20+ Auggie); line 21 of the same file already says 18+. |
| 105-136, 153, 244-270, 522 | Context7 is `@context7/mcp-server`, installed with `npm install -g` | [CODE-CONTRADICTED] | `install_mcp.py:47` (`npx -y @upstash/context7-mcp`) | Package `@upstash/context7-mcp`, run via npx; no global install. |
| 345-348 | Morphllm is `@morphllm/mcp-server` | [CODE-CONTRADICTED] | `install_mcp.py:61` (`@morphllm/morphmcp`) | `@morphllm/morphmcp`. |
| 162, 580 | `python3 -m SuperClaude install --components mcp --force` | [CODE-CONTRADICTED] | no `__main__.py`; `main.py:29-46` | `superclaude mcp --servers context7` (etc.). |
| 156 | Context7 config visible via `grep context7 ~/.claude/CLAUDE.md` | [UNVERIFIED] | registration is in Claude Code MCP config | `claude mcp get context7`. |
| 199, 227, 381 | `--no-mcp` and `--all-mcp` flags | [CODE-CONTRADICTED] | `--all-mcp` in no command; `--no-mcp` only reflect/troubleshoot | Remove or scope to those two commands. |
| 169-170, 213-230, 455-458 | ports 8000-8002, `context7-server.example.com`, `~/.claude/mcp-config.json`, `MCP_CONTEXT7_TIMEOUT` | [UNVERIFIED] | none in source (stdio npx servers) | Placeholder content; remove. |
| 593 | `../user-guide/mcp-servers.md` | [CODE-VERIFIED] | file exists | — |
| 605-606 | Support at SuperClaude-Org/SuperClaude_Framework | [CODE-CONTRADICTED] | fork rule | IronbellyOrg/IronClaude. |

Verified claims: 9 (codegraph section 27-44: pin 1.6.2, `CODEGRAPH_MCP_TOOLS` list, `--list` "Ready for Serena retirement", doctor check, AUTOINIT opt-out — match CHANGELOG 5.0.0 and `install_codegraph.py`).

## docs/mcp/mcp-optional-design.md

Describes: design principle that MCP use is optional at runtime, with native fallbacks per capability (mixed Japanese/English).
Verdict: STALE for 5.0.0 — says install provisions no MCP server, and says memory needs Mindbase; both changed in 5.0.0. codegraph is absent from the fallback model.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 9 | "`superclaude install` ... does not install any MCP server" | [CODE-CONTRADICTED] | `src/superclaude/cli/main.py:239-253` (Step 8 "codegraph, a required user-level phase"); CHANGELOG 5.0.0 "codegraph installed by default" | `superclaude install` installs and registers codegraph (required phase, exit 1 on failure); every other MCP server is optional via `superclaude mcp`. |
| 312 | "Normal installation provisions no MCP server" | [CODE-CONTRADICTED] | as above | Normal install provisions codegraph only. |
| 29-33 | Code understanding: Auggie, else Grep+Read | [CODE-CONTRADICTED] (incomplete) | `src/superclaude/core/CODEGRAPH.md`; CHANGELOG 5.0.0 (codegraph above the Grep/Read floor) | Add codegraph (structure: symbols/callers/impact) with Grep/Read floor. |
| 49-51, 179-180 | Memory: Mindbase with MCP; without MCP "session context only, no cross-session memory" | [CODE-CONTRADICTED] | `src/superclaude/agents/pm-agent.md:19-35` (`<project>/.superclaude/memory/<key>.md`); CHANGELOG 5.0.0 "session memory moves to `.superclaude/memory/` files" | Cross-session memory is plain markdown under `<project>/.superclaude/memory/`, no MCP needed. |
| 65, 107, 138, 271-279, 321 | Mindbase auto-load / auto-save; "Install Mindbase (cross-session memory)" | [CODE-CONTRADICTED] | `docs/mcp/mcp-integration-policy.md:236-238` (same repo: "No automatic memory load is implemented"); CLAUDE.md (Mindbase disabled in gateway template) | Remove; memory is file-based. |
| 200-210 | A JSON config with per-MCP `"auto"/"disabled"/"enabled"` | [UNVERIFIED] | no such config key found in `src/superclaude/cli/` | Mark as illustrative or remove. |

Verified claims: about 6 (Context7/Tavily/Auggie fallbacks to WebFetch/WebSearch/Grep, "native tools always available").

## docs/mcp/mcp-integration-policy.md

Describes: MCP server definitions, selection matrix, PM-agent lifecycle and anti-patterns; partly rewritten with "superseded" notes.
Verdict: PARTIAL — memory section already updated to `.superclaude/memory/`; codegraph (the 5.0.0 default server) is missing, and the References block points at install paths that do not exist.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 5-168 | Core MCP servers = ReflexionPattern, Mindbase, Context7, Tavily | [CODE-CONTRADICTED] (omission) | `install_mcp.py:96-102` (codegraph); `main.py:239-253` | Add codegraph as the default-installed server; selection matrix 169-224 should route code structure to codegraph. |
| 235, 248-249, 280-281 | PM agent reads `docs/patterns/*.md`, `docs/mistakes/` | [CODE-CONTRADICTED] | `docs/patterns`, `docs/mistakes` do not exist; `agents/pm-agent.md:31-35` reads `.superclaude/memory/` | Session start reads `.superclaude/memory/*.md`. |
| 406 | "Remove MODE_Task_Management.md memory sections" | [UNVERIFIED] | `src/superclaude/modes/MODE_Task_Management.md` exists in source but no installer copies `modes/` (`grep MODE_ src/superclaude/cli/*.py` = none) | Historical; state modes are not installed. |
| 419-421 | `~/.claude/superclaude/agents/pm-agent.md`, `~/.claude/superclaude/modes/MODE_*.md`, `~/.claude/superclaude/framework/rules.md` | [CODE-CONTRADICTED] | agents install to `~/.claude/agents/` (repo CLAUDE.md table); RULES at `~/.claude/RULES.md` (`src/superclaude/core/RULES.md`); modes not installed | `~/.claude/agents/pm-agent.md`, `~/.claude/RULES.md`; drop the modes line. |
| 303, 317 | `--c7`, `--tavily` manual overrides | [UNVERIFIED] | user CLAUDE.md marks these flags advisory; FLAGS.md removed in 5.0.0 | Say "advisory hint, not a parsed flag". |

Verified claims: about 10 (ReflexionPattern API, storage and 0.7 overlap per `src/superclaude/pm_agent/reflexion.py`, Mindbase stub note, memory superseded notes 236-238, 334-343).

## docs/reference/diagnostic-reference.md

Describes: bash diagnostics for installed context files, MCP config, permissions, and a clean reinstall.
Verdict: PARTIAL — install/doctor commands current; the import check, command path and reinstall are wrong.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 80-90 | `grep "^@import" ~/.claude/CLAUDE.md`; ≥5 imports means "configured correctly" | [CODE-CONTRADICTED] | `src/superclaude/core/CLAUDE.md:3` is the only import line, `@BASH_INSPECTION_POLICY.md` (no `@import` keyword) | `grep '^@' ~/.claude/CLAUDE.md` → exactly one line. As written, the script always prints "Some imports may be missing". |
| 180, 209 | Command file at `~/.claude/commands/$COMMAND.md` | [CODE-CONTRADICTED] | `main.py:32` default target `~/.claude/commands/sc` | `~/.claude/commands/sc/$COMMAND.md`. |
| 5-7, 321-326 | "no processes to monitor", "no network operations (except MCP)", "No code executes" | [CODE-CONTRADICTED] | codegraph SessionStart hook runs a background `codegraph init` (`src/superclaude/hooks/hooks.json:28`; CHANGELOG 5.0.0: up to ~1 GB memory on first init); Python CLI pipelines (`main.py:521-561`) | State that hooks, codegraph and the CLI pipelines do run processes. |
| 301-305 | Clean reinstall = `rm -rf ~/.claude` then `superclaude install` | [CODE-CONTRADICTED] (unsafe) | `docs/developer-guide/technical-architecture.md:100-101` (other `~/.claude` dirs are Claude Code's own); `~/.claude/settings.json`, `projects/` hold user state | Use `superclaude install --force` (or `superclaude update`); never delete `~/.claude`. |

Verified claims: 8 (`superclaude --version`, `install --list` "available/installed", `doctor`, core-file list, `~/.claude.json` MCP config, `commands/sc` in permission loop, modes not installed note line 48-49).

## docs/reference/README.md

Describes: index of the reference folder.
Verdict: CURRENT (links resolve). It lists common-issues.md, troubleshooting.md and mcp-server-guide.md as the troubleshooting path, which routes users to the stale docs above.
Verified claims: 9 (all link targets exist). No contradicted claims.

## docs/reference/deviation-report-format.md

Describes: the 7-column deviation report schema for fidelity gates.
Verdict: PARTIAL — schema text not checked against a parser; its named dataclass does not exist.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 105 | Dataclass `FidelityDeviation` in `src/superclaude/cli/roadmap/fidelity.py` | [CODE-CONTRADICTED] | no `fidelity.py`; `grep "class FidelityDeviation" src/superclaude` = none; nearest is `src/superclaude/cli/roadmap/fidelity_checker.py` | Point to the real model in `fidelity_checker.py` or drop the row. |

Verified claims: 0 checked beyond the path (not 5.0.0-relevant).

## docs/reference/pm-agent-autonomous-reflection.md, docs/reference/nfr-conv-2-prose-determinism.md, docs/reference/claude-code-history-management.md

Describes: ReflexionPattern/PM-agent reflection (explicit API); task-builder determinism contract; Claude Code history rotation.
Verdict: CURRENT for 5.0.0 scope. pm-agent-autonomous-reflection already says MindBase is not implemented and storage is `docs/memory/` (matches `src/superclaude/pm_agent/reflexion.py:15,65-77,172,221`).

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| pm-agent-autonomous-reflection 679 | `docs/research/...` files cited as historical | [CODE-VERIFIED] (doc itself says they are gone) | — | — |
| pm-agent-autonomous-reflection (whole) | Does not mention 5.0.0 session memory under `.superclaude/memory/` | [UNVERIFIED] (omission) | `agents/pm-agent.md:19-35` | Add one line distinguishing ReflexionPattern `docs/memory/` from session memory `<project>/.superclaude/memory/`. |

Verified claims: about 8 (0.7 threshold, `REFLEXION_OUTPUT_DIR`, `_search_mindbase` stub, `solutions_learned.jsonl`).

## docs/developer-guide/technical-architecture.md

Describes: the `~/.claude/` layout, import system, agent/command/mode structure, MCP config.
Verdict: PARTIAL — import system and modes text are current; the directory tree predates 5.0.0 (no codegraph hook, no CODEGRAPH.md, wrong agent and command lists).

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 25-33 | Core files: CLAUDE, BASH_INSPECTION_POLICY, HOW-WE-WORK, RULES, PRINCIPLES, RESEARCH_CONFIG, BUSINESS_* | [CODE-CONTRADICTED] (incomplete) | `src/superclaude/core/` also has `CODEGRAPH.md`, `ISSUE-HANDOFF.md`, `ISSUE-BACKLOG.md` (new in 5.0.0) | Add the three 5.0.0 core files. |
| 34-53 | "agents/ (19 total)" incl. `spec-panel-experts`, `test-runner`, `wave-orchestrator` | [CODE-CONTRADICTED] | `src/superclaude/agents/` has 46 `.md`; those three do not exist | List from `superclaude install --list` instead of a fixed set. |
| 54-62 | hooks/ = session-init + 7 freshness scripts "(v4.3+)" | [CODE-CONTRADICTED] | `src/superclaude/hooks/hooks.json:28` registers `codegraph-session-start.sh`; also `auggie-flag-clear.sh`, `pragmatic-subagent.js`, ccsession `session-name.sh` (`hooks.json:58,69,104,124`) | Add codegraph-session-start.sh (5.0.0) and the others; drop "v4.3+" (never tagged). |
| 72-98 | "commands/sc (25 total)" incl. `estimate.md`, `select-tool.md` | [CODE-CONTRADICTED] | 46 files in `src/superclaude/commands/`; `estimate.md`, `select-tool.md` absent; `/sc:impact`, `/sc:graph` (5.0.0) missing | Regenerate list. |
| 24-102 | Tree omits `skills/`, `templates/`, `rules/` | [CODE-CONTRADICTED] | 39 skill dirs; `install_user_setup.py:94-97` installs `rules/` | Add them. |
| 314-318 | "No Execution Engine ... no processes execute"; "No Quality Gates" | [CODE-CONTRADICTED] | `superclaude sprint/roadmap/tasklist/eval/swarm` pipelines (`main.py:521-561`); codegraph hook | Describe the Python CLI and hooks as executing components. |

Verified claims: 9 (single `@BASH_INSPECTION_POLICY.md` import per `core/CLAUDE.md:3`; modes not installed; `~/.claude.json` MCP config with `@upstash/context7-mcp`; agent activation by description; `commands/sc/` path).

## docs/developer-guide/contributing-code.md

Describes: contributor setup, component templates, PR flow.
Verdict: PARTIAL — PR flow is current (`/sc:pr-submit --monitor 3`, `--repo IronbellyOrg/IronClaude`); prerequisites and validation commands stale.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 26, 54 | Node.js 16+ | [CODE-CONTRADICTED] | `install_mcp.py:515` | 18+ (20+ Auggie). |
| 355 | `grep "@import" ~/.claude/CLAUDE.md` tests the import system | [CODE-CONTRADICTED] | `core/CLAUDE.md:3` | `grep '^@' ~/.claude/CLAUDE.md`. |
| 168-177 | Branch from a fresh clone of master | [UNVERIFIED] | repo CLAUDE.md "Create branch from `integration`" | Align with the documented `integration` flow or state master. |
| 179 | `git add .` | [UNVERIFIED] (risk) | repo CLAUDE.md forbids staging `.claude/` mirrors (gitignored, so `git add .` is safe unless `-f`) | Recommend staging named paths and `make sync-dev` + `make verify-sync`. |
| 315-322 | "Adding New Modes" as a contribution path | [CODE-CONTRADICTED] | modes are not installed (`technical-architecture.md:300`, no MODE_ in `src/superclaude/cli/*.py`) | Remove or say modes are not loaded. |
| (absent) | No mention of `make sync-dev` / `make verify-sync` or the `src/superclaude` path rule check | [UNVERIFIED] (omission) | repo CLAUDE.md "Component Sync" | Add the sync step (CONTRIBUTING.md:35 has it). |

Verified claims: 8 (clone URL, `uv venv && make install`, `uv run superclaude install`, `src/superclaude/{core,agents,commands,skills,modes,mcp,cli}` exist, PR fallback with `--repo`).

## docs/developer-guide/testing-debugging.md

Describes: installation verification, MCP checks, common issues, diagnostic script.
Verdict: MOSTLY CURRENT — uses `superclaude install --list`, `doctor --verbose`, fork install URL; three stale points and one unsafe step.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 133 | Node v16.0.0 or higher | [CODE-CONTRADICTED] | `install_mcp.py:515` | 18+. |
| 113-141 | MCP verification covers `.claude.json` and Context7 only | [UNVERIFIED] (omission) | `main.py:157-166` (`install --list` prints a codegraph block and retired-MCP lines); doctor "codegraph MCP registration" check (CHANGELOG 5.0.0) | Add `superclaude install --list` codegraph block and `superclaude doctor` codegraph check. |
| 306-307 | Complete reinstall = `rm -rf ~/.claude` | [CODE-CONTRADICTED] (unsafe) | deletes Claude Code settings, transcripts, other tools' files | `superclaude install --force`. |
| 7, 319-322 | "not executable software", "No Unit Tests", "No Integration Tests" | [CODE-CONTRADICTED] | `tests/` pytest suite; `make test`; CLI pipelines | Reword. |

Verified claims: 12 (`superclaude --version` output form "SuperClaude, version x" per click `version_option` `main.py:19`, `install --force` semantics, `mcp --list/--servers`, `@BASH_INSPECTION_POLICY.md` expected import line 93, fork install URL 253-254).

## docs/developer-guide/README.md

Describes: landing page of the developer guide.
Verdict: STALE.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 38, 39, 45, 51 | Anchors `#architecture-overview`, `#quick-start-testing-tutorial`, `#integration-testing`, `#quality-framework` | [CODE-CONTRADICTED] | headings absent in `technical-architecture.md` / `testing-debugging.md` | Point to existing headings. |
| 59, 75-78 | "NOT a CLI tool or executable software"; "Not Persistent: each conversation is independent" | [CODE-CONTRADICTED] | `superclaude` CLI (`main.py`); session memory `<project>/.superclaude/memory/` (`agents/pm-agent.md:21`) | Reword: package ships a CLI; `/sc:save`/`/sc:load` persist memory in files. |
| 130 | Python 3.8+ | [CODE-CONTRADICTED] | repo CLAUDE.md / pyproject `>=3.10` | 3.10+. |
| 132 | Node.js 16+ | [CODE-CONTRADICTED] | `install_mcp.py:515` | 18+. |
| 142 | `cat ~/.claude/commands/implement.md` | [CODE-CONTRADICTED] | `main.py:32` | `~/.claude/commands/sc/implement.md`. |
| 152-156 | Add modes in `~/.claude/modes/`; Claude reads them automatically | [CODE-CONTRADICTED] | modes not installed or imported (`technical-architecture.md:300`) | Remove. |
| 174, 198 | Repo = SuperClaude-Org/SuperClaude_Framework | [CODE-CONTRADICTED] | repo CLAUDE.md fork rule | `https://github.com/IronbellyOrg/IronClaude`. |
| 88-124 | WCAG 2.1 compliance, "240+ glossary terms", "all examples tested" | [UNVERIFIED] | no evidence in repo | Remove marketing claims. |

Verified claims: 3 (three linked guides exist).

## docs/developer-guide/documentation-index.md

Describes: navigation index for the developer guide.
Verdict: PARTIAL — links mostly resolve; sizes and one file reference wrong.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 82 | `docs/eval/release-checklist.md` exists | [CODE-CONTRADICTED] | `docs/eval/` has retention, retry, runtime, scratch-roots, validation-commands only | Drop it. |
| 23, 55, 88 | Lengths ~1,000 / ~800 / ~500 lines | [CODE-CONTRADICTED] | actual 445 / 332 / 335 lines | Drop or fix. |
| 33-49 | Git Standards doc is this repo's governance reference | [CODE-CONTRADICTED] | see git-standards-protocols.md section below (GFxAI project doc) | Mark as foreign or remove. |
| 155 | "Mode Development" pathway | [CODE-CONTRADICTED] | modes not installed | Remove. |
| 255 | "Correct Python module execution paths" | [CODE-CONTRADICTED] | sibling reference docs still use `python3 -m SuperClaude` | — |

Verified claims: 20+ (anchor links into contributing-code/testing-debugging/technical-architecture resolve; eval-pipeline.md exists).

## docs/developer-guide/git-standards-protocols.md

Describes: git workflow for "the GFxAI project" (`id: GFXAI-GIT-STANDARDS-PROTOCOLS`, status "To Do").
Verdict: WRONG PROJECT — imported from another codebase; contradicts this repo's branch model and leaves release/tagging empty.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 1-56 | Applies to GFxAI; related docs `../10_development_process.md`, `../11_testing_qa.md`, `../12_deployment_ops.md`, `development-methodology.md`, `testing-strategy.md`, `cicd-pipeline.md` | [CODE-CONTRADICTED] | none of the 6 targets exist (link check, lines 52, 277-331, 876-892) | Rewrite for IronClaude or remove. |
| 122-372, 233-245 | Branches `main` / `release/*`, Local→Dev→Test→Beta→Prod environments, 2 approvals on `main` | [CODE-CONTRADICTED] | repo CLAUDE.md: `master` ← `integration` ← `feature/*`; no environments; `.github/workflows/` = boundary-guard, contract3-generator-constraint-lint, test | Document master/integration and the fork PR rule (`--repo IronbellyOrg/IronClaude`). |
| 593-595 | Section 6 "Release and Tagging Protocol": "[To Do - No prework content]" | [CODE-CONTRADICTED] (gap) | DECISIONS.md 7.3 (notes in `docs/releases/`), 7.7 ("write G1-G9 into the release procedure afterwards") | Release procedure is undocumented; see Uncovered section. |
| 457-470 | Signed commits required by branch protection | [UNVERIFIED] | not checkable from repo | — |

Verified claims: 1 (conventional commits, matches repo CLAUDE.md).

## docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md

Describes: 2,089-line author guide for commands, skills and agents (anatomy, waves, compliance tiers, MCP integration, sync workflow).
Verdict: PARTIAL — path rules (95-112), memory (459, 796) and import text (118) are 5.0.0-current; sections 6.3, 6.4, 7.2, 7.4 restate content of core files removed in 5.0.0, codegraph is absent, and several paths are wrong.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 828-848 | "Delegation Intelligence": auto-delegate at `directory_count > 7` with `--delegate --parallel-dirs` etc. | [CODE-CONTRADICTED] | came from ORCHESTRATOR.md/FLAGS.md (removed in 5.0.0); `grep parallel-dirs src/superclaude/{commands,skills,agents,core}` = no definition | Remove the section. |
| 850-860 | "Resource Management Zones" green/yellow/orange/red with `--uc` | [CODE-CONTRADICTED] | ORCHESTRATOR.md removed; no primitive defines zones (`grep "0-60%"` none) | Remove. |
| 892-910 | MCP circuit breaker thresholds (5 failures/60s ...) and `--all-mcp` / `--no-mcp` flags | [CODE-CONTRADICTED] | MCP.md removed; `--all-mcp` in no command; `--no-mcp` only reflect/troubleshoot | Replace with: commands/skills name servers; codegraph/auggie/context7 with Grep/Read floor per `~/.claude/CODEGRAPH.md`. |
| 937-945 | `--think`/`--think-hard`/`--ultrathink` token budgets and MCP auto-enable | [UNVERIFIED] | FLAGS.md removed; user CLAUDE.md: flags advisory | Mark advisory or remove. |
| 892-910, whole doc | No codegraph integration guidance (readiness check, `graph:*` tokens, `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`, Read-before-cite rule) | [CODE-CONTRADICTED] (omission) | `src/superclaude/core/CODEGRAPH.md`; CHANGELOG 5.0.0 "codegraph in commands, skills and agents" | Add a section pointing primitive authors to `~/.claude/CODEGRAPH.md`. |
| 800 | Compliance tiers implemented by `/sc:task-unified` | [CODE-CONTRADICTED] | `src/superclaude/commands/task-unified.md` absent; `commands/task.md` exists | `/sc:task`. |
| 878, 1662, 1703 | Skill path `src/superclaude/skills/sc-adversarial/...` | [CODE-CONTRADICTED] | directory is `src/superclaude/skills/sc-adversarial-protocol/` | Fix path. |
| 2063 | Core files source `src/superclaude/*.md` | [CODE-CONTRADICTED] | `src/superclaude/core/*.md` | Fix. |
| 2089 | "Source material in `docs/generated/dev-guide-research/`" | [CODE-CONTRADICTED] | directory absent | Drop. |
| 1154, 1643, 2081 | REVISE loop max 2 iterations | [UNVERIFIED] | consistent with B2 cap; specific skill not traced | — |

Verified claims: about 15 (three-tier model, Activation pattern, install locations 76-93, path rules 95-112 = repo CLAUDE.md, `make sync-dev`/`verify-sync`, `.superclaude/memory/` 459/796 = `agents/pm-agent.md:19-35`, agent spec format, debate-orchestrator/merge-executor agents exist).

## docs/developer-guide/sprint-tui-reference.md

Describes: sprint TUI internals and a proposed generic pipeline TUI.
Verdict: CURRENT for 5.0.0 scope (not touched by 5.0.0 changes).

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 752, 798 | "Proposed: `src/superclaude/cli/pipeline/tui.py` / `logging_.py`" | [UNVERIFIED] | labelled "Proposed"; per-pipeline copies exist instead (`cli/{sprint,prd,swarm,cleanup_audit}/tui.py`, `logging_.py`) | Note the proposal was not adopted. |

Verified claims: not counted in depth (out of 5.0.0 focus); all other `src/` paths cited resolve.

## docs/dev/sync-discipline.md

Describes: source-of-truth rule (`src/superclaude/` → `make sync-dev` → `make verify-sync`), never stage `.claude/` mirrors.
Verdict: CURRENT (one wording error).

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 15-16 | "`superclaude install` regenerates `.claude/` from `src/`" | [CODE-CONTRADICTED] | `main.py:32` (targets `~/.claude/...`); project `.claude/` is written by `make sync-dev` (`Makefile:109`) | `superclaude install` writes the user `~/.claude/`; `make sync-dev` writes the repo `.claude/`. |

Verified claims: 10 (mirror table = `.gitignore:127-128`; `make sync-dev`/`verify-sync` targets `Makefile:109,166`).

## docs/dev/migration-skill.md

Describes: source-first sync for the `sc-bare-review` thin-caller migration (MIG-001/MIG-003).
Verdict: STALE STATUS (historical, not 5.0.0-relevant).

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 3-6, 96-110 | Legacy shell dispatch "still in tree"; MIG-003 will delete `scripts/*.sh` | [CODE-CONTRADICTED] | `src/superclaude/skills/sc-bare-review/` = `SKILL.md` + `refs/templates/` only | Mark MIG-003 done; keep as history. |

Verified claims: 4.

## docs/dev/lens-contribution-policy.md

Describes: governance for swarm lens registry entries.
Verdict: CURRENT for 5.0.0 scope.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 3-5 | "8-entry built-in registry" | [UNVERIFIED] (count) | `src/superclaude/cli/swarm/lenses/__init__.py:108-118` has 9 entries (8 lenses + `custom` placeholder) | "8 lenses plus the `custom` escape hatch". |
| 286 | `/sc:some-future-skill` | [CODE-VERIFIED] (placeholder, intended) | — | — |

Verified claims: not fully enumerated (out of 5.0.0 focus).

## docs/sprint-cli-deep-dive.md

Describes: 1,724-line architecture reference for `superclaude sprint`, with line-number citations.
Verdict: PARTIAL — behaviour descriptions spot-check true, but line numbers have drifted and the prompt command name is wrong.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 670-676 | `ClaudeProcess.build_prompt()` (line 123) sends `/sc:task-unified Execute all tasks in @<phase_file> ...` | [CODE-CONTRADICTED] | `src/superclaude/cli/sprint/process.py:173` (`build_prompt`), `:220` (`f"/sc:task Execute all tasks in @{phase_file} "`) | `/sc:task ...`; line 173. |
| 251, 345 (and other `executor.py:N` cites) | `execute_sprint` claude check at `executor.py:1124`; `_parse_phase_tasks` at `:1095` | [CODE-CONTRADICTED] (line drift) | `executor.py:1773` (`shutil.which("claude")`), `:1726` (`_parse_phase_tasks`), `:1761` (`execute_sprint`) | Behaviour true; update line numbers or cite symbols. |
| 1642 | Heading "Auto-Resume (v4.3.5)" | [UNVERIFIED] | 4.3.5 was never tagged (CHANGELOG 5.0.0 intro) | "(5.0.0)" or drop version. |

Verified claims: 3 spot checks of behaviour (claude-binary check, per-task vs whole-phase split, resume module list under `cli/sprint/resume/`).

## docs/sprint-budget-architecture.md

Describes: sprint turn-budget ledger and remediation design.
Verdict: PARTIAL (not touched by 5.0.0).

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 479-482 | Anti-instinct FAIL path at `executor.py:882` with "Deferred to v3.2" comment | [CODE-CONTRADICTED] (line drift) | comment now at `src/superclaude/cli/sprint/executor.py:976-978` | Cite `executor.py:976`. |
| 120-140 (box diagram) | Box-drawing characters render as literal `u2502` | [CODE-CONTRADICTED] (formatting) | doc text | Restore `│` characters. |

Verified claims: 1 (inline-fail, no-retry behaviour still present).

## docs/eval/*.md (retention, retry, runtime, scratch-roots, validation-commands)

Describes: cliEval harness internals: scratch roots, runtime budget, retry, retention, validation commands.
Verdict: CURRENT (not touched by 5.0.0).

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| retention.md 47, 211; validation-commands.md 45, 63, 81, 101, 129 | Links to `.dev/tasks/to-do/TASK-RF-20260522-153212/...` and `.dev/releases/current/cliEval/...` evidence | [CODE-CONTRADICTED] (broken links) | targets absent from tree | Point at archived location or drop. |

Verified claims: 6 (`DEFAULT_RETRY_COUNT = 0` `cli/eval/runner.py:741`; `RUN_INTERRUPTED_EXIT_CODE` = `EXIT_INTERRUPTED` = 3 `cli/eval/commands.py:583`, `signal_handler.py:47`; `SUITE_RUNTIME_BUDGET_SEC=600`, `BASELINE_SPEC_COUNT=15`, `BASELINE_PARALLEL=8` `tests/cli/eval/test_suite_runtime.py:86-91`; `cli/eval/pty/` has no `__init__.py`).

## docs/swarm/{runbook,operator-runbook,rollback-procedure,observability-procedure,transport-limits,env-readiness,monitoring-patterns}.md

Describes: swarm operator procedures (UV-only invocation, run/monitor/rollback, transports, env readiness).
Verdict: CURRENT for 5.0.0 scope. Every `superclaude swarm <verb>` used exists (`src/superclaude/cli/swarm/__init__.py:175-182` + `run`), and every `--flag` used in a `swarm` command line appears in `src/superclaude/cli/swarm/` option strings.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| rollback-procedure.md 31-45 | sc-bare-review shell files are "being retired ... once the migration commits land" | [UNVERIFIED] (stale tense) | files are absent at v5.0.0 | Past tense: removed. |

Verified claims: about 30 (8 subcommands, all flags, UV-only rule = repo CLAUDE.md).

## KNOWLEDGE.md

Describes: accumulated debugging insights (freshness hooks, anti-instinct gate, obligation scanner, spec-fidelity tokenizer, sprint 429 recovery).
Verdict: CURRENT except one install instruction.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 257 | `pipx reinstall superclaude` propagates local validator-source edits; venv at `/config/.local/share/pipx/...` | [UNVERIFIED] (likely wrong) | `pipx reinstall` reinstalls from the original spec (a git URL per the fork install), not the local checkout; repo's own path is `update.sh:7` `pipx install --force ./` | From the checkout: `./update.sh` (or `pipx install --force ./`). Path is host-specific. |

Verified claims: not enumerated (debug notes; freshness F1-F5 consistent with `hooks/scripts/freshness-*.sh`).

## CONTRIBUTING.md

Describes: rot-budget rule and pre-PR checks.
Verdict: CURRENT.

| Doc line | Claim | Tag | Code evidence | Correct statement |
|---|---|---|---|---|
| 26 | Compare with `git stash && git checkout master` | [UNVERIFIED] (risk) | environment note: the stash stack is shared across worktrees and sessions | Use a separate worktree or a WIP commit instead of bare `git stash`. |
| (absent) | No PR-target rule | [UNVERIFIED] (omission) | repo CLAUDE.md "PR Target = Fork" | Add one line: `/sc:pr-submit --monitor 3` or `gh pr create --repo IronbellyOrg/IronClaude`. |

Verified claims: 3 (`ruff check`, `pytest`, `make verify-sync`).

## Uncovered 5.0.0 subsystems/decisions

Search: `grep -rli` over `docs/` for codegraph, retire step terms, `.superclaude/memory`, fix-cycle/blocking/minor terms, release gate terms; `ls docs/{architecture,design,decisions,*adr*}` (none exist). There is no ADR, design or architecture folder anywhere under `docs/`.

| 5.0.0 subsystem / decision | Where it is described today | Technical doc (ADR/design/architecture) under docs/? |
|---|---|---|
| codegraph integration architecture: pinned 1.6.2 + SHA-256 download (`src/superclaude/cli/install_codegraph.py`), required install phase (`main.py:239-253`), user-scope registration ownership/repair, `CODEGRAPH_MCP_TOOLS` narrowing, SessionStart autoinit hook (`hooks/scripts/codegraph-session-start.sh`), primitive contract (`core/CODEGRAPH.md`, `graph:*` tokens, `SUPERCLAUDE_CODEGRAPH_PRIMITIVES`), `/sc:impact`, `/sc:graph` | CHANGELOG, `docs/releases/v5.0.0.md`, user guide `docs/user-guide/mcp-installation.md`, troubleshooting `docs/reference/mcp-server-guide.md:27-44`, agent-facing `core/CODEGRAPH.md` | **NONE.** No design note explains ownership/repair rules, the pin-update procedure, the autoinit cost model, or why `codegraph_explore` is hidden. developer-guide and docs/mcp do not mention codegraph at all. |
| MCP retire step (`src/superclaude/cli/install_retired_mcp.py`): proof-of-authorship shapes, 10 s/15 s bounds, `serena-local` exemption, current-pin Serena kept until codegraph ready, doctor/update notices | CHANGELOG, `docs/releases/v5.0.0.md`, `docs/user-guide/mcp-installation.md` | **NONE.** No technical note of which registration shapes are "provable", or the receipt/marker files. |
| File-based session memory (`<project>/.superclaude/memory/`, per-worktree store, `.superclaude/.gitignore` = `*`, single-owner vs per-session keys, one-release `.serena/memories/` read fallback) | `agents/pm-agent.md:19-35`, user guides (memory-system, session-management, commands), release notes | **NONE** as design. `docs/mcp/mcp-optional-design.md:49-51,179-180` still contradicts it (says no cross-session memory without Mindbase). |
| Review severity / loop-cap rule (decisions B1-B5: blocking vs minor, 2 fix cycles = 3 reviews, HALT+escalate at cap, `/sc:implement` A2 change, cli-portify convergence 1) and its guard `tests/skills/test_review_severity_rule.py` | `output-styles/pragmatic.md` (S1-S5), CHANGELOG, release notes | **NONE.** Also cross-slice drift (outside slice B, flagged for the owner): `docs/guides/prd-skill-release-guide.md:261,455,620` and `docs/guides/tdd-skill-release-guide.md:271,477,652` still say "max 3 fix cycles" for the research gate, contradicting B2. |
| Release procedure: notes in `docs/releases/vX.Y.Z.md` (7.3), release gate G1-G9 (7.7: "write them into the release procedure afterwards"), `gh release create --repo IronbellyOrg/IronClaude` | DECISIONS.md only | **NONE.** `git-standards-protocols.md:593-595` Section 6 is an empty "To Do"; the only process rule, `rules/core/changelog_maintenance.md`, contradicts 7.3. |
| Removed core files (ORCHESTRATOR/COMMANDS/PERSONAS/MODES/FLAGS/MCP.md) | release notes | Not documented as a decision; their content survives in `SuperClaude-Developer-Guide-Commands-Skills-Agents.md:828-860, 892-945` (delegation thresholds, resource zones, circuit breaker, `--all-mcp`). |

## Self-audit

- Coverage: all files in the slice were opened or grep-checked. Read in full: changelog_maintenance.md, common-issues.md, troubleshooting.md, mcp-server-guide.md, diagnostic-reference.md, reference/README.md, technical-architecture.md, contributing-code.md, testing-debugging.md, developer-guide/README.md, documentation-index.md, CONTRIBUTING.md. Partly read with targeted greps: SuperClaude-Developer-Guide (lines 24-123, 440-499, 764-962, 2050-2089 + whole-file greps), git-standards-protocols (frontmatter, outline, section 6), mcp-integration-policy (1-130, 180-325, 395-423), mcp-optional-design (1-60 + grep), sprint docs, eval, swarm, docs/dev, KNOWLEDGE.md, pm-agent-autonomous-reflection, nfr-conv-2, claude-code-history-management, deviation-report-format.
- Mechanical checks run over the whole slice: stale-term grep (Serena, codebase-memory, removed core file names, versions, `python -m`, pip/pipx package names, SuperClaude-Org, `.claude/changelogs`, `gh release|pr create`); relative-link existence; `src/`/`tests/` path existence; `/sc:<name>` existence; swarm subcommand and flag existence.
- Confirmed the two known items with exact lines: common-issues.md:18-28 (and 36-85) and troubleshooting.md:10 (and 11-175); changelog_maintenance.md:107 (plus 35, 115, 134-139, 166-168, 184) and missing `--repo` at 134-136.
- No Serena or codebase-memory-mcp reference survives in the slice except the intended "Ready for Serena retirement" label (`mcp-server-guide.md:32`, matches `main.py:157-166`).
- Limits: line-number drift in sprint-cli-deep-dive.md was spot-checked (3 cites, all drifted), not exhaustively. "Verified claims" counts are approximate for the large files. `[UNVERIFIED]` rows need a runtime or external check (Claude Code config paths, pipx reinstall semantics, branch-protection settings). Out-of-slice drift in docs/guides is reported but not scanned in full.
- No repo file other than this output was modified; no installs or git mutations.
