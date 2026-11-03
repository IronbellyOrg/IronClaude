# Scan A1 — core user docs

Scope: README.md, docs/getting-started/quick-start.md, docs/user-guide/{commands,flags,modes,agents,how-we-work,session-management,memory-system}.md.
Tree: HEAD d953b983 (tag v5.0.0), clean. Read-only scan.

Version ground truth: `pyproject.toml:7` `version = "5.0.0"`; `uv run superclaude --version` prints `SuperClaude, version 5.0.0`.

## README.md

**Describes:** IronClaude identity vs the `superclaude` package name; install from the fork (`pipx install git+https://github.com/IronbellyOrg/IronClaude` + `superclaude install`, README.md:57-62), which correctly states the PyPI `superclaude` is upstream; install includes the codegraph phase and the cleanup of old MCP registrations (README.md:64); dev install, CLI pipelines, pytest plugin, PM-agent patterns, repo structure, docs map, MCP integrations, eval platform support.

**Verdict:** present-but-stale (install section is current for 5.0.0; the stale parts are labels, the MCP list, missing 5.0.0 capabilities and the missing upgrade path).

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| README.md:40 | "Context freshness hooks (v4.3) — seven active shell hooks" | `docs/user-guide/freshness-hooks.md:3` (seven freshness hooks); CHANGELOG.md:9 (4.3.5 never tagged); CHANGELOG.md:93 adds a codegraph `SessionStart` hook in 5.0.0 | Drop the "(v4.3)" label (untagged version). Seven is right for freshness hooks only; 5.0.0 also installs a codegraph SessionStart index hook (`SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` turns it off). |
| README.md:38 | "integrations such as Auggie, Tavily, and Context7" | `src/superclaude/core/CLAUDE.md` MCP table lists auggie, codegraph, context7, tavily, playwright; `src/superclaude/cli/install_mcp.py:96` registry entry `codegraph` | Name codegraph, installed and registered by default in 5.0.0. |
| README.md:216-222 | MCP integrations: Auggie, Tavily, Context7, Playwright, **Mindbase** | `install_mcp.py:43-107` registry keys: context7, playwright, morphllm-fast-apply, tavily, auggie, codegraph, litellm; `install_mcp.py:346` disables `mindbase` and `airis-agent` in the gateway config | Remove Mindbase. Add codegraph (default), LiteLLM (opt-in `superclaude mcp --servers litellm`, release notes v5.0.0.md:91), Morphllm. |
| README.md:53-79 (absent) | No upgrade instructions | docs/releases/v5.0.0.md:144-153 | Add "Upgrading to 5.0.0": `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install --force`, then restart Claude sessions; plain `superclaude install` skips existing files and `superclaude update` never installs codegraph or retires old MCP registrations. Link docs/releases/v5.0.0.md. |
| README.md:224-229 | `superclaude mcp` to "Inspect MCP-related configuration" | `uv run superclaude mcp --help`: options `--servers`, `--list`, `--scope`, `--dry-run`; CHANGELOG.md:103 menu is "1. Install MCP servers (default)" / "2. Cancel" | Bare `superclaude mcp` opens an install menu; inspect with `superclaude mcp --list` or `--dry-run`. Minor. |
| README.md (absent) | No mention of session memory location, `/sc:impact`, `/sc:graph` | `src/superclaude/commands/load.md:42`; `impact.md`, `graph.md` | Optional one-line mentions (see Uncovered section). |

Verified current: README.md:57 (PyPI `superclaude` is upstream), README.md:60-61 and 71-76 (fork URL; `uv venv && make install && uv run superclaude install`), README.md:83/205 (How We Work pointer), README.md:101 `superclaude reflect run <tasklist.md> --fix` (`superclaude --help` lists `reflect`). All linked files exist (`docs/user-guide/freshness-hooks.md`, `docs/guides/reflect-cli-tools-guide.md`, `PROJECT_INDEX.md`, `KNOWLEDGE.md`, `docs/user-guide/mcp-installation.md`). No Serena, codebase-memory, or `pip install SuperClaude`.

## docs/getting-started/quick-start.md

**Describes:** three steps: install via installation.md, read How We Work, run `/sc:recommend` or `/sc:help`; link to the commands reference.

**Verdict:** present-and-current (7 lines; nothing the 5.0.0 code contradicts).

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| quick-start.md:3 | Install "installs the slash commands, agents, skills, and the How We Work guide into `~/.claude/`" | README.md:64; CHANGELOG.md:91-95 | Accurate but incomplete: install also installs and registers codegraph and the session-start indexing hook. Optional: "restart Claude Code after installing" (release notes v5.0.0.md:152). Not a contradiction. |

`/sc:recommend` and `/sc:help` exist (`src/superclaude/commands/recommend.md`, `help.md`).

## docs/user-guide/how-we-work.md

**Describes:** one paragraph pointing at `HOW-WE-WORK.md`, its six levels, the hard limit, `/sc:help`, `/sc:recommend`, and that `superclaude install` copies it to `~/.claude/HOW-WE-WORK.md`.

**Verdict:** present-but-stale (one upgrade instruction).

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| how-we-work.md:3 | "run `superclaude update` after upgrading to refresh that copy" | docs/releases/v5.0.0.md:69, 144 (`update` "never installs codegraph or retires the old MCP servers, so neither is enough for this release. Use `install --force`") | For the 5.0.0 upgrade run `superclaude install --force` (it also refreshes the guide). Same sentence is in `src/superclaude/core/HOW-WE-WORK.md:3`; fixing only this page leaves the source guide saying it too. |
| how-we-work.md:3 | Link `../../src/superclaude/core/HOW-WE-WORK.md` | file exists | Current. |

## docs/user-guide/commands.md

**Describes:** per-command reference with a "Changes files?" column, syntax, options, examples, MCP servers. "Last Updated: 2026-10-14" (commands.md:9). Header "Complete SuperClaude Framework Command Reference" (commands.md:5).

**Verdict:** present-but-stale. Two new 5.0.0 commands missing; several routing statements contradict the 5.0.0 routing guide; several MCP-server lines omit codegraph.

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| commands.md:32-115 and detail sections | No `/sc:impact` or `/sc:graph` entry | `src/superclaude/commands/impact.md:8` argument-hint `<symbol>... \| --diff [<base>] [--depth 1-3] [--limit N] [--tests] [--test-depth N] [--output-dir <dir>] [--caller <name>]`; `graph.md:8` `[status\|init] [--worktree-local] [--output-dir <dir>]`; HOW-WE-WORK.md:325-326 | Add `/sc:impact` (dependents of symbols or a diff; writes `impact.md` + `return-contract.yaml` under `.dev/impact/`; changes no code → "Report only"; MCP codegraph) and `/sc:graph` (`status` default; `init` indexes this worktree → "Only with `init`"; MCP codegraph). 45 command files in `src/superclaude/commands/` (excluding README.md); the doc covers 43. |
| commands.md:5 | "Complete SuperClaude Framework Command Reference" | README.md:1-5 | "IronClaude command reference" (cosmetic). |
| commands.md:9 | "Last Updated: 2026-10-14" | release 2026-11-02 | Update on refresh. |
| commands.md:68 | `/sc:troubleshoot` "Report only (`--fix` adds a task file you run with `/task`)" | `troubleshoot.md:54` default `--fix` route `sc:workflow` → `/sc:implement`; MDTM/`/task` only with `--depth deep`; `troubleshoot.md:192` | "`--fix` offers a `/sc:workflow` plan you run with `/sc:implement`; `--fix --depth deep` offers a `/task-builder` task file for `/task`". |
| commands.md:693 | `/sc:workflow`: "A few files … one or two sessions; always pass `--depth quick` … for many files or multi-session work use `/task-builder`" | `workflow.md:39` default depth `standard`; HOW-WE-WORK.md:17 ("Standard is the default; use quick for smaller checked plans"), :24 ("File count, multiple sessions … never select level 4") | Level 3 is the ordinary planned-implementation default including many files/sessions; default `--depth standard`; `/task-builder` only for explicit or exceptional MDTM. |
| commands.md:41 | `/sc:workflow` "Short checked plan for a few files (level 3)" | HOW-WE-WORK.md:17 | "Checked implementation plan (level 3, the ordinary default)". |
| commands.md:549 | `/sc:task`: larger work "needs a written plan (`/sc:workflow --depth quick` or `/task-builder`)" | HOW-WE-WORK.md:22 ("normally level 3, not automatic level 4") | "`/sc:workflow` (level 3); `/task-builder` only for explicit MDTM". |
| commands.md:504 | `/sc:spawn`: "For work that changes code, use `/task-builder` then `/task` instead (level 4)" | HOW-WE-WORK.md:332 | "use `/sc:workflow` then `/sc:implement` (level 3)". |
| commands.md:292 | `/sc:pm`: "multi-file work to `/task-builder` then `/task`, … new product … `/prd`, `/tdd`, `/roadmap`" | HOW-WE-WORK.md:17, 20, 296-298 | "multi-file work to `/sc:workflow` then `/sc:implement`; new product to `/prd`, `/tdd`, then `/sc:workflow`". |
| commands.md:454 | `/sc:roadmap`: "for the default planning route use `/roadmap`" | HOW-WE-WORK.md:298 ("not the ordinary post-PRD/TDD default") | "for ordinary planning use `/sc:workflow`; `/roadmap` is the MDTM composer for explicit selection". |
| commands.md:925 | `/sc:improve`: "for a large or structural refactor, write a spec and use `/task-builder`" | HOW-WE-WORK.md:174 | "write a spec, `/sc:workflow`, then `/sc:implement`". |
| commands.md:297 | `/sc:pm` "Delegates tasks to personas (backend, frontend, security...)" | release notes v5.0.0.md:111 (`PERSONAS.md` removed); `pm.md:7` `personas: [pm-agent]` | "Delegates to specialist agents (requirements-analyst, system-architect, …)". |
| commands.md:185 | `/sc:auggie-review` "MCP servers: none" | `auggie-review.md:6` `[codegraph]` | "codegraph". |
| commands.md:199 | `/sc:cleanup-audit` "MCP servers: context7" | `cleanup-audit.md:7` `[codegraph, context7]` | "codegraph, context7". |
| commands.md:653 | `/sc:validate-roadmap` "MCP servers: auggie" | `validate-roadmap.md:7` `[auggie, codegraph]` | "auggie, codegraph". |
| commands.md:767 | `/sc:brainstorm` "MCP servers: auggie-mcp, tavily" | `brainstorm.md:6` `[auggie-mcp, codegraph, tavily]` | add codegraph. |
| commands.md:1064 | `/sc:explain` "MCP servers: context7"; no callers view | `explain.md:6` `[context7, codegraph]`; `explain.md:51` one-hop callers/callees view (CHANGELOG.md:86) | add codegraph and a "one-hop callers/callees view for code targets" bullet. |
| commands.md:1325 | `/sc:reflect` "MCP servers: auggie, context7, tavily" | `reflect.md:6` `[auggie, codegraph, context7, tavily]` | add codegraph. |
| commands.md:896-919 | `/sc:troubleshoot` has no MCP line | `troubleshoot.md:6` `[auggie, codegraph, context7, tavily]` | add MCP line. |
| commands.md:276-284 | `/sc:load` omits the one-release `.serena/memories/` read-only fallback and the `/sc:graph status` pointer | `load.md:43`, `load.md:53` | Add both. |
| commands.md:1343 | `superclaude reflect run --fix` "auto-runs the corrective `/task`" | CHANGELOG.md:255 (interactive remediation default moved to `/sc:workflow`) | UNVERIFIED: the CLI auto-fix loop may legitimately still author MDTM; not checked in `src/superclaude/cli/`. Technical-docs scanner should confirm. |
| commands.md:943-946, 973 | Examples `/sc:improve auth-service --type security --validate`, `/sc:cleanup --type imports --preview` | same examples at `improve.md:89`, `cleanup.md:73`; syntax lines commands.md:937, 966 do not declare them; HOW-WE-WORK.md:172 | Pre-existing, not 5.0.0: drop or mark unsupported. |

Verified current: `/sc:pr-submit` syntax (commands.md:366) equals `pr-submit.md:8`, no `--yes`, default monitor 3 (`pr-submit.md:25`); `/sc:reflect` syntax (commands.md:1305) equals `reflect.md:10`, no `--onboard`/`--with-hierarchy`; `/sc:implement` syntax equals `implement.md:6`; `/sc:troubleshoot` syntax (commands.md:910) equals `troubleshoot.md:8`; `/sc:load`/`/sc:save` say `.superclaude/memory/`; `/sc:help` matches CHANGELOG.md:243; `--promote` default on (commands.md:1346) matches release notes :101. No `/sc:README`, Serena, codebase-memory or PyPI install command.

## docs/user-guide/flags.md

**Describes:** "SuperClaude Flags Guide": advisory behavior/MCP/thinking flags (hints only, flags.md:3-5), per-command flag tables, advanced hint flags, `superclaude` terminal system flags. Per CHANGELOG.md:243 this page is now the flag reference that moved out of `/sc:help`; the core file `FLAGS.md` that used to define the hint flags is removed in 5.0.0 (release notes v5.0.0.md:111).

**Verdict:** present-but-stale.

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| flags.md:17-24 | MCP flag table: `--c7`, `--play`, `--tavily`, `--morph`; no codegraph | `src/superclaude/core/CLAUDE.md` MCP table (installed `~/.claude/CLAUDE.md`): auggie (auto), **codegraph (auto)**, context7 `--c7`, tavily `--tavily`, playwright `--play`; no `--morph` row | Add a codegraph row (no flag; used automatically for symbol/caller/impact questions; `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` switches it off in commands/skills/agents, CHANGELOG.md:87). Note `--morph` is not in the shipped CLAUDE.md table (still a registry server, `install_mcp.py:57`). |
| flags.md:7-43, 179-198, 225-229 | `--think`, `--think-hard`, `--ultrathink`, `--introspect`, `--task-manage`, `--orchestrate`, `--uc`, `--loop`, `--safe-mode`, `--validate`, `--delegate`, `--all-mcp`, `--frontend-verify`, token figures (~4K/~10K/~32K, 30-50%) | These came from core `FLAGS.md`/`MODES.md`, removed in 5.0.0 (release notes v5.0.0.md:111, CHANGELOG.md:252); grep of `src/superclaude/{core,commands,agents,skills}` for `--think-hard\|--task-manage\|--ultracompressed\|--safe-mode\|--orchestrate\|--introspect` hits only `commands/business-panel.md` and `skills/sc-adversarial-protocol/SKILL.md` | Say plainly that since 5.0.0 no installed file defines these hint flags (FLAGS.md and MODES.md are no longer shipped; old copies in `~/.claude/` are not loaded), so Claude knows them only if you explain them. Remove or mark the token figures as unmeasured. |
| flags.md:111 | `/sc:troubleshoot --fix` "Apply fixes" | `troubleshoot.md:54` ("offer the Tier 3 remediation chain… Code changes never auto-apply; the user runs the executor") | "`--fix`: after a successful diagnosis, offer a remediation plan (`/sc:workflow` → `/sc:implement`; MDTM with `--depth deep`). Never applies fixes itself." |
| flags.md:45-177 | No `/sc:impact` or `/sc:graph` flag tables | `impact.md:8`, `graph.md:8` | Add tables: `/sc:impact` `<symbol>...`/`--diff [<base>]`, `--depth 1-3` (default 2), `--limit` (20), `--tests`, `--test-depth`, `--output-dir`, `--caller`; `/sc:graph` `status` (default) / `init`, `--worktree-local`, `--output-dir`. |
| flags.md:45-177 | No `/sc:pr-submit` table (its `--yes` was removed and default is now `--monitor 3`) | `pr-submit.md:8, 25`; release notes v5.0.0.md:97, 110 | Optional: add `/sc:pr-submit` flags (`--monitor {0..3}` default 3, `--pr <N>`, `--resume`), and note `--yes` was removed. |
| flags.md:200-209 | System flags omit `superclaude install --list` and the 5.0.0 meaning of `--force` | release notes v5.0.0.md:144-153 (`install --force` refreshes every shipped file, installs codegraph and retires old registrations; `install --list` shows the codegraph block) | Extend the `--force` row: "required to upgrade to 5.0.0; overwrites edited files in `~/.claude/` without backup". Add `superclaude install --list`. |
| flags.md:83, 86, 120, 252 | `/sc:improve --type … security`, `--preview`; `/sc:cleanup --preview` | `improve.md:89`, `cleanup.md:73` (examples only); HOW-WE-WORK.md:172 | Pre-existing (not 5.0.0): example-only controls, not supported flags. |
| flags.md:1 | "SuperClaude Flags Guide" | README.md:1-5 | Cosmetic rename to IronClaude. |

Verified current: `/sc:workflow` flags and retired `--output` (flags.md:96-104) match `workflow.md:38-42`; `/sc:reflect` table (flags.md:129-148) matches `reflect.md:10, 93-106` (`--task-log`, `--reviewers` default 3, `--no-verify` exist); no `--onboard`/`--with-hierarchy`; `superclaude mcp --dry-run` exists (`superclaude mcp --help`); no `superclaude mcp --uninstall`/`--yes`. Links `mcp-servers.md`, `session-management.md`, `commands.md` exist.

## docs/user-guide/modes.md

**Describes:** six behavioral "modes" (Brainstorming, Introspection, Deep Research, Task Management, Orchestration, Token Efficiency), their triggers, example outputs, troubleshooting, FAQ. Disclaimer at modes.md:5 and :638 says mode files are not installed or loaded. The `MODES.md` core file is removed in 5.0.0 (release notes v5.0.0.md:111); `src/superclaude/modes/MODE_*.md` exist but are not installed (consistent with modes.md:5).

**Verdict:** present-but-stale.

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| modes.md:22 | "Modes activate through behavioral instructions — Claude Code reads context files to determine which mode behaviors to adopt" | modes.md:5 itself; `MODES.md` removed (release notes v5.0.0.md:111); `src/superclaude/core/` listing has no MODES.md or MODE_* files | No installed context file defines modes in 5.0.0. Remove this sentence or replace with modes.md:5's wording. |
| modes.md:568 | "Report mode issues at [GitHub Issues](https://github.com/SuperClaude-Org/SuperClaude_Framework/issues)" | CLAUDE.md fork rule; release notes v5.0.0.md:249 (`gh issue create --repo IronbellyOrg/IronClaude`); agents.md:773 already uses the fork | Link `https://github.com/IronbellyOrg/IronClaude/issues`. Upstream URL presented as the place to report. |
| modes.md:265 | Orchestration example "Morphllm (pattern edits) + Magic (UI components)" | `install_mcp.py:43-107` registry has no `magic` server | Drop Magic; if naming code-intelligence tools, use codegraph. |
| modes.md:547-548 | `/sc:help modes`, `/sc:reflect --type mode-status` | `/sc:help` takes no arguments (commands.md:239; help.md usage lines 100-116 are bare `/sc:help`); `reflect.md:10` legacy grammar is only `--type task --analyze\|--validate` | Remove both; no mode diagnostics command exists. |
| modes.md:488, 498, 508, 518, 527-530 | `--no-task-manage`, `--no-uc`, `--no-introspect`, `--simple`; error codes B001/T001/U001/I001/O001/M001-M003 | no command file declares these flags; grep of `src/superclaude` for `B001\|M003` returns nothing | Remove invented flags and the error-code table (pre-existing fiction, now with no FLAGS.md/MODES.md behind it at all). |
| modes.md:629 | "SuperClaude's 5 behavioral modes" then lists 6 (and table modes.md:9-16 lists 6 incl. Deep Research) | modes.md:9-16 | Internal count error (cosmetic). |
| modes.md:614 | "Token Efficiency: 30-50% context reduction" | no measurement in repo; HOW-WE-WORK.md:271 forbids unmeasured figures | Remove or mark unmeasured. |
| modes.md:674 | Link `commands.md#token-efficiency` | commands.md has no such heading (headings read in full) | Broken anchor; link `flags.md` instead. |
| modes.md:453, 552 | Points to `../reference/common-issues.md` for mode installation problems | release notes v5.0.0.md:230 (Known Issue: common-issues.md still says `pipx upgrade SuperClaude`, the upstream package) | Link target is stale (owned by another scanner); flag the dependency. |

Verified current: modes.md:213 Task Management memory = `.superclaude/memory/` (matches `load.md:42`); modes.md:557-559 `superclaude doctor --verbose`, `superclaude install --list` exist (release notes :153). No Serena, codebase-memory or PyPI install.

## docs/user-guide/agents.md

**Describes:** what agents are (`src/superclaude/agents/` → `~/.claude/agents/`), manual `@agent-` invocation, delegation (no keyword matching in code, agents.md:55-58), 15 domain agents plus pm-agent, coordination, MCP integration, troubleshooting, keyword tables.

**Verdict:** present-but-stale.

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| agents.md:20, 71, 683 | "Frontend architect + Magic MCP should activate"; MCP servers include "Magic (UI)"; "Magic: UI generation for frontend-architect" | `install_mcp.py:43-107` registry: no `magic` | Remove Magic. |
| agents.md:678-685 | MCP integration list: Context7, Magic, Playwright, Morphllm; no codegraph | `grep -l codegraph src/superclaude/agents/*.md` → `auggie-reviewer.md`, `reflect-reviewer.md`, `reuse-auditor.md`, `troubleshoot-analyst.md` (the "four agents" of release notes v5.0.0.md:84) | Add codegraph: these four agents use codegraph symbol/caller/impact tools with Grep/Read as fallback. |
| agents.md:700, 803 | "use `/sc:focus [domain]`" | no `src/superclaude/commands/focus.md` (command listing above) | Nonexistent command; remove. |
| agents.md:698-751, 814-831 | Keyword trigger tables ("triggers security-engineer") | agents.md:55-58 says there is no keyword matching in code | Pre-existing internal contradiction; the 5.0.0 removal of `PERSONAS.md`/`ORCHESTRATOR.md` (release notes :111) removes the last file these tables echoed. Reword as "Claude may choose". |
| agents.md:36-40, 147-655 | Roster of 16 agents | 45 agent files in `src/superclaude/agents/` (46 `.md` incl. README.md) | Not a 5.0.0 contradiction; optional note that workflow-internal agents (rf-*, audit-*, eval-*, reflect-reviewer, troubleshoot-analyst, etc.) are spawned by skills. |
| agents.md:1 | "SuperClaude Agents Guide" | README.md:1-5 | Cosmetic. |

Verified current: agents.md:155 pm-agent runs only via `/sc:pm` or delegation (matches CHANGELOG.md:245); agents.md:374 memory in `.superclaude/memory/`; agents.md:773 issue link is the fork; agents.md:768 `superclaude doctor --verbose` / `install --list`. No Serena or codebase-memory.

## docs/user-guide/session-management.md

**Describes:** `/sc:save`/`/sc:load` project memory as markdown files under `<project>/.superclaude/memory/` (one store per worktree, auto `.gitignore`), resume via ccsession or rerunning `/task`/`/sc:implement`, the per-turn `<session-context>` envelope.

**Verdict:** present-but-stale (core 5.0.0 memory model is correct; the Serena migration step is missing and one routing example is stale).

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| session-management.md:3-17 (absent) | No migration note for existing Serena memories | `load.md:43` (one-release read-only fallback to `.serena/memories/<key>.md`); release notes v5.0.0.md:154, 173, 198 | Add "Upgrading from Serena memory (5.0.0)": copy files from `<project>/.serena/memories/` into `<project>/.superclaude/memory/`; for 5.0.0 only `/sc:load` still reads `.serena/memories/<key>.md` read-only when the new file is absent; the fallback ends next release. |
| session-management.md:125 | `/task-builder "Phase 2: payment and order processing"  # larger work goes through a task file (see How We Work)` | HOW-WE-WORK.md:17, 24 (larger work is level 3 `/sc:workflow` → `/sc:implement`; file count/sessions never select level 4) | `/sc:workflow "Phase 2: payment and order processing" --depth standard --handoff none`, then `/sc:implement <printed plan path>`. |
| session-management.md:11 | `/sc:load` syntax `[project_path]` | `load.md:22` `/sc:load [target] [--type project\|config\|deps\|checkpoint] [--refresh] [--analyze]` | Use the full syntax (minor). |
| session-management.md:13-17 (absent) | `/sc:load` result does not mention the code-graph pointer | `load.md:53` (ends with a line telling the user to run `/sc:graph status`) | Add: "It ends by pointing you to `/sc:graph status` to check this worktree's code-graph index." |
| session-management.md:128 | "Per-Turn Session Context Envelope (v4.3+)" | CHANGELOG.md:9 (4.3.5 never tagged; first versioned section is 5.0.0) | Drop the untagged version label. |
| session-management.md:229-232 | "Morphllm MCP: Applies stored refactoring patterns" | no memory integration in `install_mcp.py:57` entry; memory is plain files read by Glob/Read (`load.md:49-50`) | UNVERIFIED claim with no code behind it; remove. |

Verified current: session-management.md:3 `.gitignore` with `*` (`save.md:43`); :36 `/sc:save` flags; :108-113 resume paths match HOW-WE-WORK.md:229-237 (ccsession `--here`, `--here --all`, `/rename`); no Serena tool references.

## docs/user-guide/memory-system.md

**Describes:** the `ReflexionPattern` error-learning helper (`src/superclaude/pm_agent/reflexion.py`): JSONL store, lookup, pytest recorder, privacy, maintenance.

**Verdict:** present-and-current (not affected by the 5.0.0 changes; checked claims match code).

| Doc line | Claim | Code evidence | Correct statement |
|---|---|---|---|
| memory-system.md:18 | Session restore is the `.superclaude/memory/` markdown files, not this class | `load.md:42`; release notes v5.0.0.md:75 | Current. |
| memory-system.md:20 | MindBase search is a stub returning `None` | `reflexion.py:172-182` (`_search_mindbase`, "TODO: Implement mindbase integration") | Current. |
| memory-system.md:27-31 | Directory order: `memory_dir`, `REFLEXION_OUTPUT_DIR`, `docs/memory/` | `reflexion.py:65-74` | Current. |
| memory-system.md:205 | "Open an issue on GitHub" (no URL) | release notes v5.0.0.md:249 | Optional: name `IronbellyOrg/IronClaude`. |

Linked files exist: `docs/memory/reflexion.jsonl.example`, `docs/reference/pm-agent-autonomous-reflection.md`. Not re-verified: the worked-example arithmetic and pytest-hook details (memory-system.md:66-140) beyond the directory logic.

## Uncovered 5.0.0 capabilities

Grep of all nine slice files (case-insensitive) for each term; hits listed.

| 5.0.0 capability | Mentioned in slice? | Where it should go |
|---|---|---|
| `/sc:impact` (impact.md) | No file | commands.md (table + detail), flags.md, README quick start |
| `/sc:graph` status/init (graph.md) | No file | commands.md, flags.md, session-management.md (after `/sc:load`) |
| codegraph default install/registration, SessionStart index hook, `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`, `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`, `~/.claude/CODEGRAPH.md` | Only README.md:64/75 (install phase); no env vars, no CODEGRAPH.md | README (MCP integrations, highlights), flags.md MCP table, agents.md MCP section |
| Serena/codebase-memory retirement and Serena memory migration (`.serena/memories/` → `.superclaude/memory/`, one-release fallback) | No file mentions Serena | session-management.md, README upgrade note |
| Upgrade path `pipx install --force …` + `superclaude install --force` + restart | Only flags.md:208 mentions `install --force`, not as the upgrade step | README, how-we-work.md, quick-start.md (link to release notes) |
| Review loops capped at 2 fix cycles; minor findings never fail a review (release notes :96, :212-216) | No file | commands.md (`/sc:task`, `/sc:implement`, `/sc:tasklist`, `/sc:cli-portify` entries) or a "what changed" note |
| `/sc:pr-submit` Codex review support | commands.md:361 mentions Codex (current) | covered |
| `/sc:pr-submit --pr <N>`, origin-first target, `--yes` removed | commands.md:366 has `--pr`; removal of `--yes` not stated | commands.md note |
| Removed: `superclaude mcp --uninstall/--yes`, `/sc:reflect --onboard/--with-hierarchy`, `/ccsession-tag`, `/sc:README`, core files ORCHESTRATOR/COMMANDS/PERSONAS/MODES/FLAGS/MCP.md | None of the slice files states these removals (none of them still advertises the removed flags/commands either) | flags.md and modes.md should state FLAGS.md/MODES.md are gone; README upgrade note |
| LiteLLM MCP gateway entry (`superclaude mcp --servers litellm`) | No file | README MCP integrations |
| `superclaude sprint run` auto-resume, `--resume <task_id>`, `--task-parallelism`; CI needs `--yes`/`CI=1` | No file (flags.md:209 lists `--yes` only as "confirmation prompts") | flags.md system flags; README pipelines |
| `superclaude reflect run` promotes by default | commands.md:1346 (current) | covered |
| Remediation routing (`--fix`/`--remediate` → `/sc:workflow` plan; MDTM only with `--depth deep`) | Contradicted in commands.md:68, flags.md:111 | see tables above |
| ISSUE-HANDOFF.md / ISSUE-BACKLOG.md + CLAUDE.md issue rule | No file | README or a docs note (low priority) |
| ccsession tier rules, session names shared across worktrees, `ccsession --here [--all]`, shim fix | session-management.md:110 and commands.md:276 cover `ccsession <name>`/`--here`/`--here --all`; tiers/shim not covered | Probably owned by a ccsession doc outside this slice |
| `/sc:explain` one-hop callers/callees view | No (commands.md:1040-1064) | commands.md |

## Self-audit

- Read in full: CHANGELOG.md 5.0.0 headings plus lines 82-150 and 232-254; docs/releases/v5.0.0.md (all 276 lines); README.md; quick-start.md; how-we-work.md; commands.md (all 1363 lines); flags.md; memory-system.md; session-management.md. modes.md read lines 1-90 and 420-674 plus grep of the rest for memory/MCP/version/URL terms; agents.md read lines 34-73, 150-229, 656-855 plus grep of the rest.
- Code checked: `src/superclaude/commands/` listing (45 command files + README.md) and every command's `mcp-servers:` line; argument-hints/flags in troubleshoot, workflow, reflect, pr-submit, explain, load, save, impact, graph, implement, improve, cleanup; `src/superclaude/core/` listing (no FLAGS/MODES/PERSONAS/ORCHESTRATOR/COMMANDS/MCP.md; CODEGRAPH.md, HOW-WE-WORK.md, ISSUE-*.md present); HOW-WE-WORK.md lines 1-30 and 160-341; core CLAUDE.md MCP table; `install_mcp.py` registry keys and the mindbase disable line; `src/superclaude/agents/` listing and codegraph grep; `reflexion.py` lookup/mindbase lines; `pyproject.toml:7`; `uv run superclaude --version`, `--help`, `mcp --help`.
- Line numbers in the tables were taken from Reads/greps in this session at HEAD d953b983 (clean tree).
- UNVERIFIED: whether `superclaude reflect run --fix` still authors an MDTM `/task` (commands.md:1343); session-management.md:232 Morphllm claim; memory-system.md worked-example arithmetic; modes.md lines 91-419 were grepped, not read line by line, so prose-level claims there (beyond MCP/memory/flag terms) were not checked.
- Not in scope and not scanned: docs/getting-started/installation.md, mcp-installation.md, mcp-servers.md, brainstorm.md, freshness-hooks.md, docs/reference/*. Repo files other than this output were not modified.
