# Consolidated plan — /sc:post-release v5.0.0

- Release: v5.0.0 (tag commit `d953b983`, HEAD == tag). Run mode: ground-up (no prior manifest). Install-surface class: package.
- Repo: `/home/coder/workspaces/worktrees/IronClaude/post-release-v5.0.0`
- Inputs: `scan/A1-core-user-docs.md`, `scan/A2-feature-user-docs.md`, `scan/B-technical-docs.md`, `scan/C-install-surface.md`, `scan/DE1-cli-surface.md`, `scan/DE2-claude-surface.md`; `docs/testing/v5.0.0/c-e2e-transcript.txt` (GREEN); `CHANGELOG.md` `## [5.0.0]` (line 7); `docs/releases/v5.0.0.md`; `.dev/releases/current/v5.0.0/DECISIONS.md`.
- Paths below are repo-relative. "scan/X" means `.dev/releases/current/v5.0.0/post-release/scan/X`.
- Legend for states: **P** = present-and-current, **S** = present-but-stale, **M** = missing, **n-a** = not applicable.

## Capability inventory

45 capabilities. "5.0.0" = added or changed in the 5.0.0 changelog window (everything since the package version was set to 4.3.5 on 2026-06-04; CHANGELOG.md:9). Audience: **user** = any person with the package installed; **sysop** = needs workspace-admin rights, the central workspace env file, or push rights to the fork's master (see section 5 E).

### Python CLI (`superclaude`, `ic`)

| # | id | Capability | Audience | Source | 5.0.0 |
|---|---|---|---|---|---|
| 1 | `cli-version` | `superclaude --version` / `superclaude version` print 5.0.0 | user | `src/superclaude/cli/main.py:19`, `:513-516`; `pyproject.toml:7` | yes (version) |
| 2 | `cli-install` | `superclaude install [--target] [--force]`: core, commands, agents, skills, ccsession wiring, hooks, templates, user setup (rules, output styles, settings defaults, Orca skills, default plugins), then required codegraph phase, then retire step; exit 1 if any required phase fails | user | `main.py:29-280`; `install_user_setup.py:251-311` | yes (codegraph phase, retire step, ISSUE-*/CODEGRAPH core files) |
| 3 | `cli-install-list` | `superclaude install --list`: installed-vs-available, codegraph block, one line per retired name; read-only | user | `main.py:86-172`; `install_mcp.py:1059-1060` | yes |
| 4 | `cli-upgrade` | 5.0.0 upgrade = `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install --force`, restart sessions | user | `docs/releases/v5.0.0.md:139-157`; `main.py:178-267` | yes |
| 5 | `cli-update` | `superclaude update`: force-refresh framework steps only; no codegraph, no retire; prints legacy notice | user | `main.py:334-429` (notice `:407-415`) | yes (notice; insufficient for 5.0.0) |
| 6 | `cli-update-sh` | `./update.sh` from a clone: `pipx install --force ./`, `superclaude install --force`, `make sync-dev`, `superclaude doctor` | user | `update.sh:2-10` | yes (now includes codegraph via install --force) |
| 7 | `cli-install-skill` | `superclaude install-skill <name> [--target] [--force]` | user | `main.py:432-468`; `install_skill.py:40-97` | no |
| 8 | `cli-doctor` | `superclaude doctor [--verbose]`: 7 checks incl. codegraph registration (fails only when command not executable) and retired-MCP warning | user | `main.py:471-510`; `doctor.py:17-54`, `:160-175` | yes |
| 9 | `codegraph-install` | Pinned codegraph 1.6.2: discover / download / SHA-256 / extract / receipt / link / user-scope registration with 7 tools | user | `install_codegraph.py:26-404`; `install_mcp.py:709-1020` | yes (new) |
| 10 | `mcp-retire` | Retire step: removes provably-IronClaude user-scope `serena` / `codebase-memory-mcp` registrations, keeps the rest with reason, `serena-local` exempt, 10 s / 15 s bounds | user | `install_retired_mcp.py:35-494`; `main.py:255-267` | yes (new) |
| 11 | `cli-mcp` | `superclaude mcp [--servers ...] [--list] [--scope] [--dry-run]`; menu Install/Cancel; `--uninstall`/`--yes` and `serena`/`codebase-memory-mcp` removed | user | `main.py:283-331`; `install_mcp.py:42-115`, `:1317-1458` | yes |
| 12 | `mcp-litellm` | Opt-in LiteLLM MCP gateway entry (`http://ibcore:4000/mcp/`, `${LITELLM_API_KEY}` header) | user (operator network dependency) | `install_mcp.py:107-115` | yes (new) |
| 13 | `cli-sprint-run` | `superclaude sprint run` incl. default auto-resume, `--fresh/--restart`, `-y/--yes`, `CI`/`SUPERCLAUDE_SPRINT_ASSUME_YES` | user | `cli/sprint/commands.py:323-528` | yes |
| 14 | `cli-sprint-pertask` | `--handoff/--no-handoff`, `--resume <task_id>`, `--task-parallelism K`, `handoff/phase-{N}-task-{id}.json`, `task_complete` event | user | `CHANGELOG.md:302-307`; `cli/sprint/handoff.py` | yes (new) |
| 15 | `cli-sprint-aux` | `sprint rerun-tasks` (auto-detect), `verify-checkpoints`, `attach`, `kill`, `status` (stub), `logs` (stub) | user | `sprint/commands.py:727-945`; `sprint/logging_.py:367-378`; `sprint/tmux.py:262-276` | partly (rerun-tasks auto-detect) |
| 16 | `cli-roadmap-tasklist` | `superclaude roadmap run/validate/accept-spec-change`, `superclaude tasklist validate` | user | `cli/roadmap/commands.py:299-513`; `cli/tasklist/commands.py:170-185` | no |
| 17 | `cli-reflect` | `superclaude reflect run` (`--fix`, `--max-fix-iterations`, `--base`, `--promote` default, plan route → `/sc:implement`), `reflect contract-status`, recursion breaker | user | `cli/reflect/commands.py:44-478`; `cli/reflect/runner.py:474-477`, `:597` | yes |
| 18 | `cli-prd` | `superclaude prd run/resume` (research fix cycles default 2) | user | `cli/prd/commands.py:115-234` | yes |
| 19 | `cli-eval` | `superclaude eval list/describe/doctor/run` (null executor WARNING, output root, exit codes 0-3) | user (maintainer) | `cli/eval/commands.py:844-2004` | yes |
| 20 | `cli-swarm` | `superclaude swarm` 8 subcommands; fresh run now does Wave 2/3 (merged.md, return-contract.yaml); `reflect-review` lens; `run --tui` | user | `cli/swarm/commands.py:2083-2159`; `cli/swarm/lenses/reflect_review.py:33-72` | yes (in window; not named in changelog headings) |
| 21 | `cli-portify` | `superclaude cli-portify run` (convergence 1 iteration; `--max-convergence` not wired) | user | `cli/cli_portify/commands.py:189-227` | yes |
| 22 | `cli-cleanup-audit` | `superclaude cleanup-audit run` | user | `cli/cleanup_audit/commands.py:85-93` | no (skill changed) |
| 23 | `cli-init-lite` | `superclaude init-lite --context-optimized` | user | `cli/init_lite.py:247-350` | no |
| 24 | `cli-recommend-helpers` | `superclaude recommend cache/telemetry/eval/dispatch` (plumbing for `sc-recommend`) | user (internal) | `cli/recommend/commands.py:57-403` | yes (key rename, fingerprint) |
| 25 | `cli-ic` | `ic` launcher: sources `~/.aienv`, model-slot overrides, `--no-yolo` | user | `pyproject.toml:72`; `cli/ic.py:12-15`; `src/superclaude/scripts/ic:25-110` | no |

### Claude Code surface (`~/.claude`)

| # | id | Capability | Audience | Source | 5.0.0 |
|---|---|---|---|---|---|
| 26 | `sc-graph` | `/sc:graph [status\|init] [--worktree-local] [--output-dir]` | user | `src/superclaude/commands/graph.md:8-53`; `skills/sc-graph-protocol/SKILL.md:25-151` | yes (new) |
| 27 | `sc-impact` | `/sc:impact <symbol>... \| --diff [<base>]` with `--depth/--limit/--tests/--test-depth/--output-dir/--caller`; Grep fallback | user | `commands/impact.md:8-63`; `skills/sc-impact-protocol/SKILL.md:15,29` | yes (new) |
| 28 | `codegraph-autoinit-hook` | SessionStart (startup) hook runs one background `codegraph init --yes`; `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` | user | `hooks/hooks.json:23-31`; `hooks/scripts/codegraph-session-start.sh:6-31` | yes (new) |
| 29 | `codegraph-primitives` | Commands/skills/agents use codegraph above Grep/Read per `~/.claude/CODEGRAPH.md`; `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`; `/sc:explain` one-hop view | user | `core/CODEGRAPH.md:11-34`; `core/CLAUDE.md:28-30`; `commands/explain.md:51` | yes (new) |
| 30 | `memory-files` | `/sc:save`, `/sc:load`, `/sc:pm`, PM agent use `<project>/.superclaude/memory/`; one-release `.serena/memories/` read-only fallback; `/sc:load` points to `/sc:graph status` | user | `commands/save.md:22,42-45`; `commands/load.md:22,42-53`; `commands/pm.md:16,47`; `agents/pm-agent.md:19-35` | yes (breaking) |
| 31 | `routing-guide` | `~/.claude/HOW-WE-WORK.md`; `/sc:help` prints level table; `/sc:recommend` reads guide first | user | `core/HOW-WE-WORK.md:3,11-28`; `commands/help.md:21-132`; `commands/recommend.md:32-60` | yes (new) |
| 32 | `core-files` | Shorter `~/.claude/CLAUDE.md` (routing block, Core Rule 10); removed ORCHESTRATOR/COMMANDS/PERSONAS/MODES/FLAGS/MCP.md and `/sc:README` | user | `core/CLAUDE.md`; `CHANGELOG.md:242,248,252` | yes |
| 33 | `issue-templates` | `~/.claude/ISSUE-HANDOFF.md`, `ISSUE-BACKLOG.md` + Core Rule 10 (`gh issue create --body-file`) | user | `cli/install_core.py:21-22`; `core/ISSUE-HANDOFF.md:1-10`; `core/CLAUDE.md:43` | yes (new) |
| 34 | `sc-pr-submit` | `/sc:pr-submit` default `--monitor 3`, `--pr <N>`, origin-first, head check, Codex support, `--yes` removed | user | `commands/pr-submit.md:8,25-66`; `pr_submit/fsm.py:31,33,77` | yes |
| 35 | `review-severity-cap` | Blocking vs minor; max 2 fix cycles (3 reviews) then escalate; injected via SubagentStart; CI guard | user | `output-styles/pragmatic.md:225-229`; `hooks/hooks.json:120-127`; `tests/skills/test_review_severity_rule.py` | yes |
| 36 | `remediation-routing` | `/sc:troubleshoot --fix`, `/sc:reflect --remediate`, auggie-review offer → `/sc:workflow` plan for `/sc:implement`; MDTM only with `--depth deep` | user | `commands/troubleshoot.md:54`; `CHANGELOG.md:259` | yes |
| 37 | `sc-workflow-implement` | Level-3 planning chain `/sc:workflow` (default `--depth standard`) → `/sc:implement` (one A2 repair; calls `/sc:impact`) | user | `commands/workflow.md:38-42`; `commands/implement.md:6`; `core/HOW-WE-WORK.md:17,24` | yes |
| 38 | `sc-reflect` | `/sc:reflect` (`--onboard`/`--with-hierarchy` removed; contract 1.8.0; codegraph) | user | `commands/reflect.md:6,10,93-106` | yes |
| 39 | `sc-other-commands` | The remaining `/sc:` commands (45 command files total; unchanged ones such as analyze, build, design, document, git, improve, cleanup, index, research, spawn, spec-panel, test, release-split, review-translation, roadmap, swarm-wizard, validate-tests, post-release) | user | `src/superclaude/commands/*.md` | mostly no (post-release added 2026-07-06, inside the window, not in changelog) |
| 40 | `ccsession-naming` | `ccsession <name>` = Claude Code `--name`; `/rename` sync; names per repo; `--key`; `--migrate-names`; `/ccsession-tag` retired | user | `skills/ccsession-tag/ccsession:11-12,127,1606-1608`; `hooks/hooks.json:54-73` | yes |
| 41 | `ccsession-lists` | `--list`, `--here`, `--here --all`, `--rm`, `--ask` (exit 1 / 130) | user | `ccsession:27-53,1324,1441-1467` | yes (#347) |
| 42 | `ccsession-orca` | `ccsession-orca` launcher; Orca tab title `<label> · Claude Code` | user | `skills/ccsession-tag/ccsession-orca:19-81`; `ccsession:1512-1528` | yes (new) |
| 43 | `ccsession-tiers` | User side: `--tier`, `--model`, `--models-status`, `--refresh-models`; shim survives terminal (#341). Admin side: `CCSESSION_TIER_RULES` / `CCSESSION_ACCESS` / `T<N>` slots in `/etc/aidev02/aienv.d/defaults.sh` | user + sysop | `skills/ccsession-tag/models.py:63-104,320-328,454-620`; `ccsession:57-66,798`; `local-gateway-alias-proxy.py:172-203` | yes |
| 44 | `ccsession-model-data` | Published `ccsession-models.json` fetched from the fork's master on every launch; `CCSESSION_MODELS_URL`, `CCSESSION_MODELS_REFRESH=0` | sysop (publish) / user (override) | `models.py:53-58,296-314`; `ccsession:73-76` | yes (2026-10-28.1 layout) |
| 45 | `freshness-hooks` | Freshness hooks (session-context envelope, pre-edit gate, read tracker, subagent start/stop), auggie flag hook | user | `hooks/hooks.json:13-141`; `hooks/scripts/freshness-pre-edit.sh:15,84-133` | partly (Serena matcher removed) |

Removed surface that guides must show as ABSENT (not counted as capabilities): `superclaude mcp --uninstall/--yes`, `--servers serena|codebase-memory-mcp`, `/sc:reflect --onboard/--with-hierarchy`, `/sc:pr-submit --yes`, `/ccsession-tag`, `/sc:README` on new installs, the six core files (`CHANGELOG.md:70,103,106,217,248,252`).

## Coverage matrix

Columns: **A** user doc, **B** technical doc, **C** install doc, **D** user test guide, **E** sysop test guide. No D or E guide exists yet (`docs/testing/v5.0.0/` holds only the C e2e run), so every applicable D/E cell is **M**. E applies only to the two sysop-only capabilities (rows 43 admin side, 44); every other E cell is n-a. Planned D/E file in brackets.

| # | id | A (user doc) | B (tech doc) | C (install doc) | D | E |
|---|---|---|---|---|---|---|
| 1 | `cli-version` | P `README.md` | S `docs/reference/common-issues.md:18,83`, `troubleshooting.md:10,25,73` (4.1.5, `python3 -m SuperClaude`) | P `docs/getting-started/installation.md` | M [D01] | n-a |
| 2 | `cli-install` | P `README.md:57-64`; P `docs/getting-started/quick-start.md` (incomplete) | S `docs/developer-guide/technical-architecture.md:24-102` | S `installation.md` (no codegraph, prerequisites, what's installed) | M [D01] | n-a |
| 3 | `cli-install-list` | S `docs/user-guide/flags.md:200-209` (absent) | S `docs/developer-guide/testing-debugging.md:113-141` (omission) | S `installation.md:280-286` (not used for verification); P `docs/releases/v5.0.0.md:153` | M [D01] | n-a |
| 4 | `cli-upgrade` | M `README.md` (no upgrade section); S `docs/user-guide/how-we-work.md:3` | S `common-issues.md:22-28` | S `installation.md:53-57,326-333,363-365`; M standalone upgrade guide | M [D01] | n-a |
| 5 | `cli-update` | S `how-we-work.md:3`; S `src/superclaude/core/HOW-WE-WORK.md:3` | S `troubleshooting.md:161-163` | S `installation.md:56,329,333,363`; P `docs/user-guide/mcp-installation.md:70` | M [D01] | n-a |
| 6 | `cli-update-sh` | M | S `KNOWLEDGE.md:257` | M `installation.md`; S `docs/releases/v5.0.0.md:151,228` (minor) | M [D01] | n-a |
| 7 | `cli-install-skill` | P `flags.md:208` (one row) | n-a | M `installation.md` (help text only) | M [D01] | n-a |
| 8 | `cli-doctor` | P `modes.md:557-559`, `agents.md:768` | S `troubleshooting.md:147-148` (`--diagnose`); S `testing-debugging.md` (no codegraph check) | S `installation.md:280-286` (plain doctor) | M [D01] | n-a |
| 9 | `codegraph-install` | P `README.md:64`; S `docs/user-guide/mcp-servers.md:14-34` (codegraph absent) | P `docs/reference/mcp-server-guide.md:13-44`; M design note | P `mcp-installation.md:5-60`; M `installation.md` | M [D01, D03] | n-a |
| 10 | `mcp-retire` | M (README upgrade note) | M design note | P `mcp-installation.md:52-56,62-71` (line 71 stale) | M [D01] | n-a |
| 11 | `cli-mcp` | S `README.md:216-229`; S `mcp-servers.md` | S `mcp-server-guide.md:105-606` | P `mcp-installation.md:73-310` | M [D02] | n-a |
| 12 | `mcp-litellm` | P `mcp-servers.md:117-128`; M `README.md` | n-a | M `mcp-installation.md` (no litellm row) | M [D02] | n-a |
| 13 | `cli-sprint-run` | S `docs/guides/sprint-cli-tools-release-guide.md` | S `docs/sprint-cli-deep-dive.md:670-676,1642` | n-a | M [D10] | n-a |
| 14 | `cli-sprint-pertask` | M (only release notes) | M | n-a | M [D10] | n-a |
| 15 | `cli-sprint-aux` | S sprint guide `:17-23` (5 vs 7 subcommands) | P deep-dive (behaviour) | n-a | M [D10] | n-a |
| 16 | `cli-roadmap-tasklist` | S `docs/guides/roadmap-cli-tools-release-guide.md:104-141,899,1420`; S `cli-portify-and-pipeline-runner-guide.md:400-425` | n-a | n-a | M [D11] | n-a |
| 17 | `cli-reflect` | S `docs/guides/reflect-cli-tools-guide.md:28-60,262-273`; S `commands.md:1343` | n-a | n-a | M [D12] | n-a |
| 18 | `cli-prd` | M (only `docs/designs/prd-spec-flag.md`) | P design doc | n-a | M [D13] | n-a |
| 19 | `cli-eval` | P `docs/user-guide/eval-pipeline.md` (dead links); S `docs/guides/suites-guide.md` | P `docs/eval/*.md` | n-a | M [D15] | n-a |
| 20 | `cli-swarm` | S `docs/swarm/README.md`, `user-guide.md`, `command-reference.md`, `lens-catalog.md`; S(minor) `wizard-guide.md` | S `docs/swarm/operator-runbook.md:118`, `monitoring-patterns.md:7-9`; S `docs/dev/lens-contribution-policy.md:3-5,38,187` | n-a | M [D14] | n-a |
| 21 | `cli-portify` | S `cli-portify-and-pipeline-runner-guide.md:80,199-202,495-506` | n-a | n-a | M [D13] | n-a |
| 22 | `cli-cleanup-audit` | P `commands.md` (MCP line S `:199`) | n-a | n-a | M [D13] | n-a |
| 23 | `cli-init-lite` | P `commands.md:114,260-267` | n-a | n-a | M [D16] | n-a |
| 24 | `cli-recommend-helpers` | n-a (internal plumbing) | n-a | n-a | M [D16 appendix] | n-a |
| 25 | `cli-ic` | M (no doc mentions `ic`) | n-a | M `installation.md` (console script not listed) | M [D16] | n-a |
| 26 | `sc-graph` | M `commands.md`, `flags.md`; P `mcp-installation.md:60` (one paragraph) | M design note | P `mcp-installation.md:42-60` | M [D03] | n-a |
| 27 | `sc-impact` | M `commands.md`, `flags.md`; P `mcp-installation.md:60` | M design note | P `mcp-installation.md:60` | M [D03] | n-a |
| 28 | `codegraph-autoinit-hook` | S `README.md:40`; S `docs/user-guide/freshness-hooks.md:13-23` (omits) | S `technical-architecture.md:54-62`; S `diagnostic-reference.md:5-7,321-326` | P `mcp-installation.md:42-50` | M [D03] | n-a |
| 29 | `codegraph-primitives` | S `flags.md:17-24`; S `agents.md:678-685`; S `commands.md` MCP lines; S `brainstorm.md:14,17,107` | S `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:892-910` (omission); S `docs/mcp/mcp-optional-design.md:29-33`; M design note | P `mcp-installation.md:58-60` | M [D03] | n-a |
| 30 | `memory-files` | S `docs/user-guide/session-management.md`; P `commands.md`; P `memory-system.md` | S `mcp-optional-design.md:49-51,65,107,138,179-180,271-279,321`; S `docs/mcp/mcp-integration-policy.md:235,248-249,280-281`; M design note | n-a | M [D04] | n-a |
| 31 | `routing-guide` | S `how-we-work.md:3`; S `commands.md` routing lines | n-a | n-a | M [D05] | n-a |
| 32 | `core-files` | S `flags.md:7-43,179-198`; S `modes.md:22,488-548` | S `technical-architecture.md:25-33`; S Developer Guide `:828-860,937-945` | n-a | M [D05] | n-a |
| 33 | `issue-templates` | M | S `technical-architecture.md:25-33` (not listed) | n-a | M [D05] | n-a |
| 34 | `sc-pr-submit` | P `commands.md:361-366`; M `flags.md` table | P `docs/developer-guide/contributing-code.md`; S `CONTRIBUTING.md` (no PR-target line) | n-a | M [D07] | n-a |
| 35 | `review-severity-cap` | S `docs/guides/prd-skill-release-guide.md:261,332,455,620`; S `tdd-skill-release-guide.md:265,271,345,477,652`; S cli-portify guide `:80`; M `commands.md` | M design note | n-a | M [D06] | n-a |
| 36 | `remediation-routing` | S `commands.md:68`; S `flags.md:111`; S reflect guide | n-a | n-a | M [D06] | n-a |
| 37 | `sc-workflow-implement` | S `commands.md:41,292,454,504,549,693,925`; S `session-management.md:125` | n-a | n-a | M [D06] | n-a |
| 38 | `sc-reflect` | P `commands.md:1305`, `flags.md:129-148` (MCP line S `commands.md:1325`) | n-a | n-a | M [D12] | n-a |
| 39 | `sc-other-commands` | P `commands.md` (cosmetic header/date; S MCP lines; S `improve`/`cleanup` example flags) | n-a | n-a | M [D05 sample] | n-a |
| 40 | `ccsession-naming` | P `session-management.md:108-113`; skill `README.md` not scanned | n-a | n-a | M [D08] | n-a |
| 41 | `ccsession-lists` | P `session-management.md:110`, `commands.md:276` | n-a | n-a | M [D08] | n-a |
| 42 | `ccsession-orca` | M in `docs/` (skill `README.md` not scanned) | n-a | n-a | M [D08] | n-a |
| 43 | `ccsession-tiers` | skill `README.md:270-379`, `MODEL-TIERS.md` (cited as source by DE2; not scanned for staleness) | n-a | n-a | M [D08 user side] | M [E01 admin side] |
| 44 | `ccsession-model-data` | skill `README.md` (not scanned) | n-a | n-a | n-a | M [E02] |
| 45 | `freshness-hooks` | S `freshness-hooks.md:117,123-124` | P `troubleshooting.md:106-140`; P `KNOWLEDGE.md` | n-a | M [D09] | n-a |

## Gap list

Disposition rules applied: **fix-this-run** for anything that contradicts 5.0.0 behaviour (rule a) and for small, same-file fixes a writer touches anyway; **defer** only for pre-existing staleness unrelated to 5.0.0 that needs a large rewrite or an owner decision (rule b); suspected code bugs go to section 6. "Item" names the writer-worklist entry in section 4.

### Workstream C — install and upgrade

| # | Gap | Evidence | Remedy (item) | Disposition |
|---|---|---|---|---|
| 1 | Existing installs told to upgrade with `superclaude update` | `installation.md:53-57`; `main.py:334-429` (no codegraph, no retire); `v5.0.0.md:144` | Replace with `pipx install --force ...` + `superclaude install --force` (C-W1) | fix-this-run: upgrade command contradicts 5.0.0 |
| 2 | Upgrade blocks use `superclaude update` (pipx and pip) | `installation.md:326-333` | Same (C-W1) | fix-this-run: rule a |
| 3 | "Plain install never replaces files; run `superclaude update`" | `installation.md:363`; `install_skills.py:89-98`; `main.py:239-267` | Point to `install --force` (C-W1) | fix-this-run: rule a |
| 4 | "`install --force` does the same" as update | `installation.md:365`; `main.py:239-280` | State that `--force` also runs codegraph + retire and can exit 1 after files are overwritten (C-W1) | fix-this-run: rule a (install --force described as framework-only) |
| 5 | "`superclaude install --force` reinstalls framework files only" | `mcp-installation.md:71`; `main.py:52,239-267` | Reword: `--force` changes only framework steps; codegraph + retire run on every install (C-W2) | fix-this-run: rule a |
| 6 | Prerequisites wrong: git "optional", no `claude` CLI or network | `installation.md:80-94`; `install_mcp.py:937-947`; `install_codegraph.py:308-327` | Required list (C-W1) | fix-this-run: install exits 1 without them |
| 7 | pip method "All" platforms / "Best for Windows" | `installation.md:34,164-198`; `install_codegraph.py:46-52,280-289` | State Linux/macOS x64/arm64 for codegraph; elsewhere install exits 1 unless codegraph 1.6.2 on PATH (C-W1) | fix-this-run: contradicts exit code |
| 8 | `python3 -m pip install --user pipx` / `pip install` fail on PEP 668 systems | `installation.md:134,172` | Recommend `uv tool install pipx` or distro pipx (C-W1) | fix-this-run: small, same file |
| 9 | Verification uses plain `superclaude doctor` (passes without codegraph) | `installation.md:280-286`; `doctor.py:160-175` | `doctor --verbose` + `install --list` checks from `v5.0.0.md:153` (C-W1) | fix-this-run: rule a |
| 10 | "What's installed" lists 5 locations | `installation.md:297-309`; `main.py:174-253`; `install_user_setup.py:251-311` | Full list incl. codegraph, ccsession links, plugins, `~/.claude.json` entry (C-W1) | fix-this-run: same file |
| 11 | Uninstall omits codegraph and ccsession-orca | `installation.md:353-361`; `mcp-installation.md:34-40` | Add + link (C-W1) | fix-this-run: same file |
| 12 | `installation.md` never mentions codegraph | grep: 0 hits | Codegraph note + link (C-W1) | fix-this-run: 5.0.0 required phase undocumented |
| 13 | `CLAUDE_CONFIG_DIR` read for `.claude.json` but files always go to `$HOME/.claude` | `install_mcp.py:721-726`; `install_core.py:47` | One-paragraph note (C-W1); code finding O15 | fix-this-run (doc part) |
| 14 | Default-plugin install step (network, 6 plugins, 30 s budget) undocumented | `install_user_setup.py:251-311`; `user_settings_defaults.json:28-49` | Mention in what's-installed (C-W1) | fix-this-run: same file |
| 15 | No standalone upgrade guide (only release notes are correct) | scan/C Gaps 1, 6, 7; transcript lines 449-787 | Create `docs/getting-started/upgrading.md` (C-W3) | fix-this-run: required new user coverage |
| 16 | Upgrade leaves codebase-memory-mcp companions (skill `codebase-memory`, 3 agents) | transcript lines 729-736, 771-773 (doctor counts 48 agents, 39 skills vs 45/38 shipped) | Explain in upgrading.md with removal command (C-W3) | fix-this-run: user-visible upgrade outcome |
| 17 | `update.sh` installs the checked-out tree and needs `make`; release notes say "first line" | `update.sh:7,9`; `v5.0.0.md:151,228` | Correct statement in upgrading.md (C-W3); release-notes wording deferred (#80) | fix-this-run (guide) |
| 18 | `mcp-installation.md` server table has no litellm row | grep `litellm` in file: 0 hits; `install_mcp.py:107-115` | Add opt-in row (C-W2) | fix-this-run: 5.0.0 entry missing |

### Workstream A — user docs

| # | Gap | Evidence | Remedy (item) | Disposition |
|---|---|---|---|---|
| 19 | README "(v4.3)" label; codegraph SessionStart hook not named | `README.md:40`; `CHANGELOG.md:9,93` | A-W1 | fix-this-run: untagged version number |
| 20 | README MCP list names Mindbase, omits codegraph/litellm/Morphllm | `README.md:38,216-222`; `install_mcp.py:43-116,346` | A-W1 | fix-this-run: removed/disabled feature |
| 21 | README has no upgrade path, no `/sc:impact`/`/sc:graph`, misdescribes bare `superclaude mcp` | `README.md:53-79,224-229` | A-W1 | fix-this-run: rule a |
| 22 | quick-start omits prerequisites, restart, upgrade link | `quick-start.md:3`; scan/C Gap 2 | A-W2 | fix-this-run: new-user path |
| 23 | `superclaude update` as the post-upgrade step | `how-we-work.md:3`; `src/superclaude/core/HOW-WE-WORK.md:3`; `v5.0.0.md:144` | A-W3 (plus byte-for-byte plugin mirror) | fix-this-run: rule a |
| 24 | commands.md lacks `/sc:impact`, `/sc:graph` | `commands.md:32-115`; `impact.md:8`; `graph.md:8` | A-W4 | fix-this-run: rule a |
| 25 | commands.md routing sends planned work to `/task-builder`/`/roadmap`, `--depth quick`, troubleshoot `--fix` → `/task` | `commands.md:41,68,292,454,504,549,693,925`; `HOW-WE-WORK.md:17,22,24,298`; `troubleshoot.md:54` | A-W4 | fix-this-run: rule a (routing) |
| 26 | commands.md MCP lines omit codegraph; no `/sc:explain` one-hop view; `/sc:pm` "personas" | `commands.md:185,199,297,653,767,1064,1325,896-919`; command frontmatter `mcp-servers:` lines | A-W4 | fix-this-run: 5.0.0 behaviour / removed PERSONAS.md |
| 27 | commands.md `/sc:load` omits `.serena` fallback and graph pointer | `commands.md:276-284`; `load.md:43,53` | A-W4 | fix-this-run: 5.0.0 behaviour |
| 28 | commands.md says `reflect run --fix` auto-runs `/task` | `commands.md:1343`; `runner.py:474-477,597` | A-W4 (resolved conflict, section 7) | fix-this-run: routing |
| 29 | commands.md has no review-cap note; examples use undeclared `--type security`, `--preview` | `commands.md:943-946,973`; `pragmatic.md:225-229` | A-W4 | fix-this-run: 2-fix-cycle rule; nonexistent flags |
| 30 | flags.md: no codegraph row; FLAGS.md hint flags presented as defined; troubleshoot `--fix` "Apply fixes"; no `/sc:impact`/`/sc:graph`/`/sc:pr-submit` tables; system flags miss `install --force` upgrade meaning, `install --list`, sprint 5.0.0 flags; `--preview`/`--type security` | `flags.md:7-43,83,86,111,120,179-209,225-229,252` | A-W5 | fix-this-run: removed core files, routing, missing commands, nonexistent flags |
| 31 | modes.md: modes "read from context files"; upstream issue URL; Magic; `/sc:help modes`, `--type mode-status`; invented flags/error codes; count/figure/anchor errors | `modes.md:22,265,488-530,547-548,568,614,629,674` | A-W6 | fix-this-run: removed MODES.md, upstream URL, nonexistent flags |
| 32 | agents.md: Magic MCP; codegraph agents missing; `/sc:focus`; keyword-trigger tables contradict "no keyword matching" | `agents.md:20,55-58,71,678-685,698-751,700,803,814-831` | A-W7 | fix-this-run: nonexistent server/command; removed ORCHESTRATOR content |
| 33 | session-management: no Serena migration note; `/task-builder` routing example; short `/sc:load` syntax; no graph pointer; "(v4.3+)"; Morphllm memory claim | `session-management.md:3-17,11,125,128,229-232` | A-W8 | fix-this-run: rule a |
| 34 | memory-system issue link has no repo | `memory-system.md:205` | A-W9 | fix-this-run: one line |
| 35 | mcp-servers.md: no codegraph; Auggie Node 18+; `implement` tool; research-depth block under litellm; AIRIS setup; sample config; `/sc:validate`; `--no-mcp`/`--all-mcp`/`--concurrency`; modes links | `mcp-servers.md:14-34,65,106-107,139-171,189-213,225-259,313-335`; `install_mcp.py:79-87,96-116,346` | A-W10 | fix-this-run: nonexistent flags/command, 5.0.0 server |
| 36 | freshness-hooks: `superclaude install -f`; codegraph hook not mentioned; jq "build dependency" | `freshness-hooks.md:13-23,117,123-124`; `install -f` → "No such option" | A-W11 | fix-this-run: nonexistent flag |
| 37 | brainstorm: MCP list lacks codegraph; fallback tier; `--brainstorm` mode flag | `brainstorm.md:14,17,107,233`; `commands/brainstorm.md:6` | A-W12 | fix-this-run: 5.0.0 behaviour |
| 38 | eval-pipeline: dead links; `--check-coverage` wording; no `/sc:cli-eval` pointer | `eval-pipeline.md:7,77,86,388,391`; `commands/cli-eval.md` | A-W13 | fix-this-run: small, same file |
| 39 | swarm docs say Wave 2/3 pending (M5), 7 lenses / "8 entries, 7 validated", no `reflect-review`, no `--tui`, exit 130, `--custom-prompt-dir` flag (rejected), broken custom example | `docs/swarm/README.md:8-15,27,43,66-123,157`; `command-reference.md:22-66,147-177,241-263`; `user-guide.md:9-11,63-100,191-199,248-253,387-391,434-481`; `wizard-guide.md:73-74`; `lens-catalog.md:18,80,148`; `swarm/commands.py:2083-2169`; `validate-lenses` → `9 entries inspected, 8 validated` | A-W14 | fix-this-run: contradicts behaviour in the 5.0.0 window; nonexistent flag |
| 40 | sprint guide: 5 subcommands; no `--resume/--task-parallelism/--handoff`; CI example lacks `--yes`; `/sc:task-unified`; child argv shape; tmux forward list; misplaced sub-bullet | `sprint-cli-tools-release-guide.md:17-23,56,64-79,96-97,295-305,320,368-371,461-467`; `sprint/process.py:220`; `pipeline/process.py:134-165` | A-W15 | fix-this-run: 5.0.0 flags; nonexistent command |
| 41 | reflect guide: only `/task` route; no `remediation_plan_path`; no `contract-status` | `reflect-cli-tools-guide.md:28-31,41,59-60,262-273`; `runner.py:474-477,597,769-775` | A-W16 | fix-this-run: routing |
| 42 | cli-portify guide: "converge until ≥7.0"; options missing; argv shape; roadmap "9-step" | `cli-portify-and-pipeline-runner-guide.md:80,199-202,400-425,495-506`; `sc-cli-portify-protocol/SKILL.md:367-380` | A-W17 | fix-this-run: 2-fix-cycle rule (Breaking Change 4) |
| 43 | roadmap guide: single `SPEC_FILE`; options table incomplete; convergence default False | `roadmap-cli-tools-release-guide.md:104,117-141,899,1420`; `roadmap/models.py:111-113`; `roadmap run --help` | A-W18 | fix-this-run: small targeted edits in a file whose CLI flags are wrong |
| 44 | prd guide: "max 3 fix cycles"; MINOR must be fixed; no `superclaude prd` pointer | `prd-skill-release-guide.md:261,332,455,620`; `skills/prd/refs/build-request-template.md:130`; `skills/prd/refs/agent-prompts.md:273,283` | A-W19 | fix-this-run: 2-fix-cycle rule |
| 45 | tdd guide: same | `tdd-skill-release-guide.md:265,271,345,477,652`; `skills/tdd/refs/build-request-template.md:125`; `skills/tdd/refs/agent-prompts.md:282,291` | A-W20 | fix-this-run: 2-fix-cycle rule |
| 46 | suites-guide: `git stash apply stash@{0}` (unsafe, shared stash), suites "not on disk", 88/18 counts | `suites-guide.md:44-77,214-409,59-61`; `eval list` → 17 suites, `real` 17 evals, 87 total | A-W21 | fix-this-run: unsafe advice |
| 47 | No codegraph usage guide for users | scan/A1 Uncovered; scan/A2 Uncovered | Create `docs/user-guide/codegraph.md` (A-W22) | fix-this-run: required new coverage |

### Workstream B — technical docs

| # | Gap | Evidence | Remedy (item) | Disposition |
|---|---|---|---|---|
| 48 | Changelog rule saves notes to git-ignored `.claude/changelogs/`, release command lacks `--repo`, template path project-only | `changelog_maintenance.md:35,37,105,107,115,134-139,166-168,184`; `.gitignore:127-128`; DECISIONS 7.3 | B-W1 | fix-this-run: rule a (named) |
| 49 | common-issues: `python3 -m SuperClaude`, 4.1.5, `pipx upgrade SuperClaude`, PyPI names, `--components`, `--install-dir`, `--list-components`, `/sc:analyze --no-mcp`, Node 16 | `common-issues.md:18-85`; `main.py:29-46`; `pyproject.toml:7`; Known Issue `v5.0.0.md:230` | B-W2 | fix-this-run: rule a |
| 50 | troubleshooting: same family plus `--diagnose`, `backup`, `uninstall`, `install --fresh`, Magic key, upstream issues URL, "(v4.3+)" | `troubleshooting.md:10-175`; `main.py:521-561` | B-W3 | fix-this-run: rule a |
| 51 | mcp-server-guide (non-codegraph part): server list, Node 16, `@context7/mcp-server`, `@morphllm/mcp-server`, `python3 -m SuperClaude install --components mcp`, `--no-mcp`/`--all-mcp`, placeholder ports/hosts, upstream URLs | `mcp-server-guide.md:13-16,52-614`; `install_mcp.py:47,61,515` | B-W4 | fix-this-run: rule a |
| 52 | mcp-optional-design: "install provisions no MCP server"; Mindbase memory; no codegraph | `mcp-optional-design.md:9,29-33,49-51,65,107,138,179-180,200-210,271-279,312,321`; `main.py:239-253` | B-W5 | fix-this-run: removed feature / 5.0.0 behaviour |
| 53 | mcp-integration-policy: no codegraph; `docs/patterns`, `docs/mistakes`; `~/.claude/superclaude/...` paths; flags as parsed | `mcp-integration-policy.md:5-168,235,248-249,280-281,303,317,406,419-421` | B-W6 | fix-this-run: 5.0.0 default server missing |
| 54 | diagnostic-reference: `rm -rf ~/.claude` reinstall; `@import` check always fails; command path lacks `sc/`; "no processes" | `diagnostic-reference.md:5-7,80-90,180,209,301-305,321-326` | B-W7 | fix-this-run: unsafe advice |
| 55 | deviation-report-format cites nonexistent `fidelity.py`/`FidelityDeviation`; pm-agent-autonomous-reflection lacks session-memory distinction | `deviation-report-format.md:105`; `pm-agent-autonomous-reflection.md` | B-W8 | fix-this-run: small |
| 56 | technical-architecture tree: misses CODEGRAPH/ISSUE-* core files, codegraph hook, `/sc:impact`/`/sc:graph`, skills/templates/rules; wrong agent and command lists; "(v4.3+)"; "no execution engine" | `technical-architecture.md:24-102,314-318`; `hooks.json:28,58,69,104,124` | B-W9 | fix-this-run: 5.0.0 files missing |
| 57 | contributing-code: Node 16; `@import` grep; "Adding New Modes"; no sync step; `git add .` | `contributing-code.md:26,54,179,315-322,355` | B-W10 | fix-this-run: removed modes; small |
| 58 | testing-debugging: Node 16; no codegraph verification; `rm -rf ~/.claude`; "no tests" | `testing-debugging.md:7,113-141,133,306-307,319-322` | B-W11 | fix-this-run: unsafe advice |
| 59 | developer-guide/README: dead anchors; "not a CLI"; Python 3.8; Node 16; command path; modes; upstream repo URL; unverified marketing claims | `developer-guide/README.md:38-198` | B-W12 | fix-this-run: upstream URL presented as the place to go |
| 60 | documentation-index: `docs/eval/release-checklist.md`; wrong sizes; git-standards presented as governance; mode development | `documentation-index.md:23,33-49,55,82,88,155,255` | B-W13 | fix-this-run: small; also links the 4 new tech notes |
| 61 | Developer guide restates removed core-file content (delegation thresholds, resource zones, circuit breaker, `--all-mcp`); no codegraph section; `/sc:task-unified`; wrong skill/core paths; dead source link | `SuperClaude-Developer-Guide-Commands-Skills-Agents.md:800,828-860,878,892-945,1662,1703,2063,2089` | B-W14 | fix-this-run: removed features (targeted section edits, not a rewrite) |
| 62 | sync-discipline says `superclaude install` regenerates repo `.claude/` | `sync-discipline.md:15-16`; `Makefile:109` | B-W15 | fix-this-run: one line |
| 63 | lens-contribution-policy: "8-entry registry"; `--custom-prompt-dir` as a flag | `lens-contribution-policy.md:3-5,38,187`; `swarm/lenses/__init__.py:108-118`; `swarm/commands.py:125` (flag is future) | B-W15 | fix-this-run: nonexistent flag |
| 64 | sprint-cli-deep-dive: `/sc:task-unified`; heading "Auto-Resume (v4.3.5)" | `sprint-cli-deep-dive.md:670-676,1642`; `sprint/process.py:220` | B-W16 | fix-this-run: nonexistent command; untagged version |
| 65 | swarm runbooks: "requires the M5 contract"; "Until M5 lands"; retired shell files in present tense | `operator-runbook.md:118`; `monitoring-patterns.md:7-9`; `rollback-procedure.md:31-45` | B-W17 | fix-this-run: contradicts 5.0.0-window behaviour (CONFLICT resolved, section 7) |
| 66 | KNOWLEDGE `pipx reinstall superclaude` to pick up local edits; CONTRIBUTING bare `git stash`; no PR-target rule | `KNOWLEDGE.md:257`; `CONTRIBUTING.md:26`; `update.sh:7` | B-W18 | fix-this-run: unsafe advice; install advice |
| 67 | No technical note for codegraph integration + MCP retire step | scan/B Uncovered rows 1-2 | Create `docs/developer-guide/codegraph-integration.md` (B-W19) | fix-this-run: required |
| 68 | No technical note for file-based session memory | scan/B Uncovered row 3 | Create `docs/developer-guide/session-memory.md` (B-W20) | fix-this-run: required |
| 69 | No technical note for review severity / 2-fix-cycle rule | scan/B Uncovered row 4; DECISIONS B1-B5 | Create `docs/developer-guide/review-severity-rule.md` (B-W21) | fix-this-run: required |
| 70 | No release procedure (G1-G9, `docs/releases/`, `--repo`); git-standards section 6 empty | DECISIONS 7.3, 7.7; `RELEASE-READINESS.md:192-200`; `git-standards-protocols.md:593-595` | Create `docs/developer-guide/release-procedure.md` (B-W22) | fix-this-run: required (decision 7.7) |

### Deferred

| # | Gap | Evidence | Remedy for a follow-up | Disposition |
|---|---|---|---|---|
| 71 | git-standards-protocols.md is another project's doc (GFxAI; wrong branches, environments, 6 dead links) | `git-standards-protocols.md:1-56,122-372,593-595` | Rewrite for IronClaude (master ← integration ← feature, fork PR rule) or delete; B-W13 marks it foreign and B-W22 covers release | defer: copied from another project, needs a full rewrite and an owner call on keep vs delete |
| 72 | sprint-cli-deep-dive.md line-number drift across 1,724 lines | `sprint-cli-deep-dive.md:251,345` vs `executor.py:1726,1761,1773` | Replace `file:line` cites with symbol names in one pass | defer: long deep-dive drift (rule b example); behaviour text spot-checks true |
| 73 | sprint-budget-architecture.md line drift and literal `u2502` box characters | `sprint-budget-architecture.md:120-140,479-482` | Restore box characters; cite `executor.py:976` | defer: not 5.0.0; cosmetic |
| 74 | docs/eval broken links to `.dev/tasks/to-do/TASK-RF-20260522-153212/` evidence | `retention.md:47,211`; `validation-commands.md:45,63,81,101,129` | Repoint to archived evidence or drop | defer: historical evidence links, not 5.0.0 |
| 75 | docs/dev/migration-skill.md still says legacy shell dispatch is in tree | `migration-skill.md:3-6,96-110` | Mark MIG-003 done | defer: historical record |
| 76 | sprint-tui-reference "Proposed" pipeline TUI never adopted | `sprint-tui-reference.md:752,798` | Add a "not adopted" note | defer: not 5.0.0 |
| 77 | Swarm historical records (`release-notes-v1.md`, `oq-resolutions.md`, `post-release-metrics.md`) mention `--custom-prompt-dir` / M5 | grep hits listed in section 7 | Leave as dated records, or add a one-line "superseded" banner | defer: point-in-time records of swarm v1 |
| 78 | suites-guide has no sections for suites #12-#14, `real`, `post_release_command_contract` | `suites-guide.md:81-418` | Add five sections | defer: additive content, not a contradiction; stash/count fixes are in A-W21 |
| 79 | Release-guide templates do not state the 2-fix-cycle default | `RELEASE-GUIDE-INSTRUCTIONS.md:124`; `RELEASE-GUIDE-TEMPLATE.md:148` | Add "max 2 fix cycles; minor findings are notes" | defer: placeholders, no behaviour claim |
| 80 | Release notes: `update.sh` "first line" (is line 7); no "check out v5.0.0 first" | `v5.0.0.md:151,228`; `update.sh:7` | Correct in the next release's notes | defer: published notes for the tag; C-W3 carries the correct statement |
| 81 | Generated `cli-api-inventory.md` understates `update` steps | `docs/generated/contributor-knowledge-base/cli-api-inventory.md:54` | Regenerate | defer: generated pipeline artifact |
| 82 | No user doc for the `ic` launcher | grep of `docs/`, `README.md`: 0 hits | Short README or user-guide section | defer: pre-existing, not 5.0.0; D16 hand-tests it |
| 83 | ccsession skill docs (`skills/ccsession-tag/README.md`, `MODEL-TIERS.md`) were not scanned for staleness | no scanner covered them (section 7) | Scan in the next post-release run | defer: outside every scanner's slice; DE2 used them as code-adjacent source |
| 84 | contributing-code says branch from master; repo CLAUDE.md says branch from `integration` | `contributing-code.md:168-177`; repo `CLAUDE.md` Git Workflow | Owner decides the documented base branch | defer: process decision, not a doc fact |

Totals: 70 fix-this-run (1-70), 14 defer (71-84). Code findings are separate (section 6).

## Writer worklist

Rules for every writer:

- Line numbers come from the scans at `d953b983`. Read the target file first and match on the quoted text, not the number.
- Ground facts used below (verified in code during consolidation): version `5.0.0` (`pyproject.toml:7`); install from the fork `pipx install git+https://github.com/IronbellyOrg/IronClaude`; upgrade `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install --force`; `superclaude install` options are only `--target`, `--force`, `--list` (`main.py:29-46`); no `__main__.py`, so never `python -m superclaude`/`SuperClaude`; npm MCP servers need Node.js 18+, Auggie 20+ (`install_mcp.py:87,515`); issues go to `https://github.com/IronbellyOrg/IronClaude/issues`; 45 commands, 45 agents, 38 skill folders, 11 core files (counted from `src/superclaude/`, matches the e2e new-user install, transcript lines 383-389).
- Files under `src/superclaude/` are installed primitives: after editing run `make sync-dev` and `make verify-sync`; never stage `.claude/`. Do not add `src/superclaude/...` paths to installed primitives (repo `CLAUDE.md`).
- Do not touch `docs/releases/v5.0.0.md` or `CHANGELOG.md` (published record).

### Workstream A — user docs

**A-W1 `README.md` (update)** — gaps 19-21
1. `:40` "Context freshness hooks (v4.3) — seven active shell hooks" → drop "(v4.3)"; add: "5.0.0 also installs a codegraph SessionStart hook that indexes each checkout on its first session (`SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` turns it off)". Evidence `hooks/hooks.json:23-31`, `CHANGELOG.md:9,93`.
2. `:38` "integrations such as Auggie, Tavily, and Context7" → name codegraph first ("installed and registered by default").
3. `:216-222` MCP list → remove Mindbase (disabled, `install_mcp.py:346`); list codegraph (default, `install_mcp.py:96-103`), Context7, Playwright, Tavily, Auggie, Morphllm (`morphllm-fast-apply`), LiteLLM (opt-in, `superclaude mcp --servers litellm`, operator network only, `install_mcp.py:107-115`).
4. `:224-229` "`superclaude mcp` ... Inspect MCP-related configuration" → "bare `superclaude mcp` opens an install menu (1. Install, 2. Cancel); inspect with `superclaude mcp --list` or `--dry-run`" (`install_mcp.py:1377-1389`).
5. After the install section (`:53-79`) add "Upgrading to 5.0.0": back up edited `~/.claude` files; `pipx install --force git+https://github.com/IronbellyOrg/IronClaude`; `superclaude install --force`; restart Claude sessions; plain `install` skips existing files and `superclaude update` never installs codegraph or retires old MCP registrations; link `docs/getting-started/upgrading.md` and `docs/releases/v5.0.0.md`.
6. Add one line each for `/sc:impact`, `/sc:graph` (link `docs/user-guide/codegraph.md`) and for session memory in `<project>/.superclaude/memory/` (link `docs/user-guide/session-management.md`).

**A-W2 `docs/getting-started/quick-start.md` (update)** — gap 22
1. `:3` → keep the sentence; add: prerequisites (Python 3.10+, git, the Claude Code CLI `claude` on PATH, network to GitHub — the codegraph phase exits 1 without them; `install_mcp.py:937-947`); "restart Claude Code after installing"; "already installed? see `upgrading.md`".

**A-W3 `docs/user-guide/how-we-work.md` + `src/superclaude/core/HOW-WE-WORK.md` + `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (update)** — gap 23
1. `how-we-work.md:3` and `HOW-WE-WORK.md:3` "run `superclaude update` after upgrading IronClaude to refresh that copy" → "after upgrading IronClaude run `superclaude install --force` to refresh that copy (it also installs codegraph and retires old MCP registrations; `superclaude update` refreshes files only)". Keep the existing overwrite/backup warning and apply it to `install --force` too (`main.py:178-267`; `v5.0.0.md:144`).
2. Copy `src/superclaude/core/HOW-WE-WORK.md` byte-for-byte to the plugin path (currently identical, `cmp` confirmed); line 3 is outside the level-table markers (`:11-28`), so `src/superclaude/core/CLAUDE.md` needs no change. Run `make sync-dev`, `make verify-sync`, `uv run pytest tests/ -k "how_we_work or routing" -q`.

**A-W4 `docs/user-guide/commands.md` (update)** — gaps 24-29
1. Table `:32-115` and detail sections: add `/sc:impact` — syntax `/sc:impact <symbol>... | --diff [<base>] [--depth 1-3] [--limit N] [--tests] [--test-depth N] [--output-dir <dir>] [--caller <name>]` (`impact.md:8`); writes `impact.md` + `return-contract.yaml` under `.dev/impact/<slug>-<ts>/`; Changes files? "Report only"; MCP codegraph; falls back to Grep with `status: partial`. Add `/sc:graph` — `[status|init] [--worktree-local] [--output-dir <dir>]` (`graph.md:8`); `status` default; `init` only when you type it; Changes files? "Only with `init`"; MCP codegraph.
2. `:5` → "IronClaude command reference"; `:9` → "Last Updated: 2026-11-02".
3. `:68` troubleshoot → "`--fix` offers a `/sc:workflow` plan you run with `/sc:implement`; `--fix --depth deep` offers a `/task-builder` task file for `/task`" (`troubleshoot.md:54`).
4. `:41` and `:693` workflow → "Checked implementation plan (level 3, the ordinary default for planned work, including many files and several sessions); default `--depth standard`; `/task-builder` only for explicit or exceptional MDTM" (`workflow.md:39`; `HOW-WE-WORK.md:17,24`).
5. `:549` task → "needs a written plan (`/sc:workflow`, level 3; `/task-builder` only for explicit MDTM)"; `:504` spawn → "use `/sc:workflow` then `/sc:implement` (level 3)"; `:292` pm → "multi-file work to `/sc:workflow` then `/sc:implement`; new product to `/prd`, `/tdd`, then `/sc:workflow`"; `:454` roadmap → "for ordinary planning use `/sc:workflow`; `/roadmap` is the MDTM composer for explicit selection"; `:925` improve → "write a spec, `/sc:workflow`, then `/sc:implement`" (`HOW-WE-WORK.md:22,174,296-298,332`).
6. `:297` pm "Delegates tasks to personas" → "Delegates to specialist agents" (`PERSONAS.md` removed, `v5.0.0.md:111`).
7. MCP lines → `:185` auggie-review "codegraph"; `:199` cleanup-audit "codegraph, context7"; `:653` validate-roadmap "auggie, codegraph"; `:767` brainstorm "auggie-mcp, codegraph, tavily"; `:1064` explain "context7, codegraph" + bullet "one-hop callers/callees view for code targets" (`explain.md:51`); `:1325` reflect "auggie, codegraph, context7, tavily"; troubleshoot section `:896-919` add "MCP servers: auggie, codegraph, context7, tavily" (each from the command's `mcp-servers:` frontmatter line).
8. `:276-284` load → add "For 5.0.0 only, reads `<project>/.serena/memories/<key>.md` read-only when the new file is absent" and "ends by pointing you to `/sc:graph status`" (`load.md:43,53`).
9. `:1343` `superclaude reflect run --fix` → "applies `/sc:implement <remediation_plan_path>` by default; `/task <remediation_task_path>` only with `--depth deep`" (`runner.py:474-477,597`).
10. Under `/sc:task`, `/sc:implement`, `/sc:tasklist`, `/sc:cli-portify` add: "Review loops: minor findings are notes and never fail a review; at most 2 fix cycles (3 reviews), then it stops and escalates open blocking findings to you. `/sc:cli-portify` runs 1 convergence iteration" (`pragmatic.md:225-229`; `v5.0.0.md:96,212-216`).
11. `:943-946`, `:973` examples `--type security --validate`, `--preview` → drop them (not declared in `improve.md`/`cleanup.md` syntax; code finding O13).
12. `/sc:pr-submit` entry → add "`--yes` was removed in 5.0.0" (`CHANGELOG.md:217`).

**A-W5 `docs/user-guide/flags.md` (update)** — gap 30
1. `:17-24` MCP table → add row "codegraph — no flag; used automatically for symbol, caller and impact questions; `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` switches it off" (`core/CODEGRAPH.md:11,26`); keep `--morph` but note it is not in the shipped `CLAUDE.md` table.
2. Top of `:7-43` and `:179-198` → state: "Since 5.0.0 no installed file defines these hint flags (`FLAGS.md`, `MODES.md` are no longer shipped; old copies in `~/.claude/` are not loaded). Claude knows them only if you explain them." Remove the token figures (~4K/~10K/~32K, 30-50%) or mark them unmeasured.
3. `:111` troubleshoot `--fix` "Apply fixes" → "after a diagnosis, offers a remediation plan (`/sc:workflow` → `/sc:implement`; MDTM with `--depth deep`); never applies fixes itself" (`troubleshoot.md:54`).
4. Add tables: `/sc:impact` (`<symbol>...` or `--diff [<base>]`, `--depth` 1-3 default 2, `--limit` 1-100 default 20, `--tests`, `--test-depth` 1-5, `--output-dir`, `--caller`; `impact.md:29-38`); `/sc:graph` (`status` default / `init`, `--worktree-local` init only, `--output-dir`; `graph.md:20-25`); `/sc:pr-submit` (`--monitor {0..3}` default 3, `--pr <N>`, `--resume <jsonl>`, `--max-rounds` default 2 cap 5; `--yes` removed; `pr-submit.md:25-56`).
5. `:200-209` system flags → `--force` row: "required for the 5.0.0 upgrade; overwrites edited files in `~/.claude/` without backup and re-copies skill folders"; add `superclaude install --list`; add `superclaude sprint run --resume <task_id>`, `--task-parallelism K` (default 1), `--handoff/--no-handoff`, and "`--yes` or `CI=1` for non-interactive auto-resume" (`sprint run --help`; `CHANGELOG.md:302-323`).
6. `:83,86,120,252` `--type ... security`, `--preview` → remove (example-only, not declared).
7. `:1` title → "IronClaude Flags Guide".

**A-W6 `docs/user-guide/modes.md` (update)** — gap 31
1. `:22` → replace with the `:5` wording: no installed context file defines modes in 5.0.0.
2. `:568` → `https://github.com/IronbellyOrg/IronClaude/issues`.
3. `:265` → drop "Magic (UI components)" (no `magic` in `install_mcp.py:43-116`).
4. `:547-548` → remove `/sc:help modes` (`/sc:help` takes no arguments) and `/sc:reflect --type mode-status` (`reflect.md:10`).
5. `:488-530` → remove `--no-task-manage`, `--no-uc`, `--no-introspect`, `--simple` and the B001/T001/U001/I001/O001/M001-M003 table (no source defines them).
6. `:629` "5 behavioral modes" → "6"; `:614` remove "30-50% context reduction"; `:674` link `flags.md` instead of `commands.md#token-efficiency`.

**A-W7 `docs/user-guide/agents.md` (update)** — gap 32
1. `:20`, `:71`, `:683` → remove Magic.
2. `:678-685` → add codegraph: `auggie-reviewer`, `reflect-reviewer`, `reuse-auditor`, `troubleshoot-analyst` use codegraph symbol/caller/impact tools with Grep/Read as fallback (`grep -l codegraph src/superclaude/agents/*.md`).
3. `:700`, `:803` → remove `/sc:focus` (no such command).
4. Before the keyword tables `:698-751`, `:814-831` → add: "These keywords are hints for you; no installed file matches keywords (see 'How delegation works' above), and the `ORCHESTRATOR.md`/`PERSONAS.md` files they came from are no longer shipped."
5. Optional note near `:36-40`: 45 agents ship; workflow agents (rf-*, audit-*, eval-*, reflect-reviewer, troubleshoot-analyst) are spawned by skills.

**A-W8 `docs/user-guide/session-management.md` (update)** — gap 33
1. After `:3-17` add "Upgrading from Serena memory (5.0.0)": copy `<project>/.serena/memories/*` into `<project>/.superclaude/memory/`; for 5.0.0 only `/sc:load` reads `.serena/memories/<key>.md` read-only when the new file is absent; the fallback ends next release (`load.md:43`; `v5.0.0.md:154,198`).
2. `:11` → `/sc:load [target] [--type project|config|deps|checkpoint] [--refresh] [--analyze]` (`load.md:22`).
3. `:13-17` → add "It ends by pointing you to `/sc:graph status`" (`load.md:53`).
4. `:125` → `/sc:workflow "Phase 2: payment and order processing" --depth standard --handoff none`, then `/sc:implement <printed plan path>` (`HOW-WE-WORK.md:17,24`).
5. `:128` → drop "(v4.3+)".
6. `:229-232` → remove the Morphllm "stored refactoring patterns" claim (memory is plain files; `load.md:49-50`).

**A-W9 `docs/user-guide/memory-system.md` (update)** — gap 34
1. `:205` "Open an issue on GitHub" → "open an issue on `IronbellyOrg/IronClaude` (`gh issue create --repo IronbellyOrg/IronClaude`)".

**A-W10 `docs/user-guide/mcp-servers.md` (update)** — gap 35
1. `:14-20` → add a codegraph section first: installed by `superclaude install`, pinned 1.6.2, seven tools (node, search, callers, callees, impact, files, status), link `mcp-installation.md#default-setup-codegraph` and `codegraph.md` (`install_mcp.py:96-103,855-872`).
2. `:26-34` → add row "Symbol, caller, impact questions → codegraph (Grep/Read fallback)".
3. `:106`, `:244`, `:256` → Auggie needs Node.js 20+; installer pins `@augmentcode/auggie@0.36.0` (`install_mcp.py:79-87`).
4. `:107` → "the shipped description names `codebase-retrieval` and `ask_question`" (drop `implement`; `install_mcp.py:78`).
5. `:139-144` → move "Capabilities" and "Research Depth Control" back under Tavily / `/sc:research` (`research.md:25`).
6. `:148-171` → installer path `superclaude mcp --servers airis-mcp-gateway`; tool count advertised as 60+ (unverified); a fresh template download disables `airis-agent` and `mindbase` (`install_mcp.py:28,346`).
7. `:189-213` sample → `npx -y @upstash/context7-mcp`, `npx -y @playwright/mcp@latest`; recommend `superclaude mcp --servers <name>` over hand edits.
8. `:65` `/sc:validate ... --play` → `/sc:test --type e2e` (`commands/test.md:22`).
9. `:225`, `:228`, `:259` → `--all-mcp` does not exist; `--no-mcp` exists only on `/sc:troubleshoot` and `/sc:reflect` (`troubleshoot.md:58`; `reflect.md:103`). `:323` → remove `--concurrency`.
10. `:313-318`, `:335` → reword modes as advisory hints (no mode files installed).

**A-W11 `docs/user-guide/freshness-hooks.md` (update)** — gap 36
1. `:117` `superclaude install -f` → `superclaude install --force`.
2. After the table `:13-23` → note that `hooks.json` also registers `codegraph-session-start.sh` (SessionStart, 5.0.0; opt out with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`), `auggie-flag-clear.sh` and `pragmatic-subagent.js`, so removing freshness entries must not delete them.
3. `:123-124` → "requires `jq` on PATH".

**A-W12 `docs/user-guide/brainstorm.md` (update)** — gap 37
1. `:17` → `auggie-mcp, codegraph, tavily` (`commands/brainstorm.md:6`).
2. `:14`, `:107` → codebase context order Auggie → codegraph → Glob/Grep (`sc-brainstorm-protocol/SKILL.md:57,193,386`).
3. `:233` → "`--brainstorm` is an advisory hint; no mode file is installed".

**A-W13 `docs/user-guide/eval-pipeline.md` (update)** — gap 38
1. `:7`, `:391` → remove link to `.dev/releases/current/cliEval/design-spec.md` (absent); `:388` remove `docs/eval/release-checklist.md` (absent).
2. `:77`, `:86` → quote help: `--check-coverage` "wires the FR-G5 coverage gate marker into the payload".
3. Add a short "Authoring or running suites from Claude Code" pointer to `/sc:cli-eval` (`commands/cli-eval.md`).

**A-W14 swarm user docs (update)** — gap 39. Evidence for all: `swarm/commands.py:2083-2169`; live stub run (scan/A2 README section); `swarm validate-lenses` → `registry OK (9 entries inspected, 8 validated)`; `lenses/reflect_review.py:33-72`; `swarm run --help` (`--tui`, `--lens custom` rejected, no `--custom-prompt-dir`).
- `docs/swarm/README.md`: `:8-15` remove the M5-pending banner; a fresh run with a recipe runs Wave 2 normalize + Wave 3 reduce and writes `merged.md`, `return-contract.yaml`, per-worker `*.final.md` + `*.meta.json`; `done.json` only on `swarm kill --output`. `:27`, `:77-79`, `:132`, `:157` → 8 lenses + `custom` = 9 entries, 8 validated. `:66-75` add row `reflect-review · 3 · passthrough · stable · yes · /sc:adversarial`. `:43` run = preflight → dispatch → normalize → reduce/contract. `:75` custom prompts come from the JobSpec field `custom_prompt_dir`, not a flag. `:95-123` rewrite the artifact table.
- `docs/swarm/command-reference.md`: `:22-24` include Wave 2/3; `:35-51` add `--tui` (fresh run only, needs a TTY, exclusive with `--detached`); `:44` spec-file/stdin runs default to `openai_compat`; `:60-66` add exit 130 (Ctrl-C during `--tui`); `:147-148` 9/8; `:170-173` exit 1 is reachable; `:175-177` add `terminal_status=`; `:241-263` rewrite artifacts; `:51`, `:58` say "the `custom_prompt_dir` `system.txt`".
- `docs/swarm/user-guide.md`: `:9-11`, `:63-73` `ls -A` also shows `merged.md`, `return-contract.yaml`, `bare-review-0{0,1,2}-...{final.md,meta.json}`; `:85`, `:95-100` 8 lenses / 9 entries; `:191-199` add `reflect-review` (used by `superclaude reflect` Tier 2); `:248-253` contract writer has landed; `:387-391` keep only the `done.json` caveat; `:434-439`, `:477` replace with a spec file (`"lens": "custom"`, `custom_prompt_dir`) run as `superclaude swarm run job.json --output ... --auto-inject-guard`; `:481` only `done.json` is absent; add `--tui` to §7.
- `docs/swarm/wizard-guide.md`: `:73-74` → two stable lenses (`bare-review`, `reflect-review`; the wizard does not offer `reflect-review`).
- `docs/swarm/lens-catalog.md`: `:18` → "The 8 bundled lenses" (add `reflect-review`); `:148` → `9 entries inspected, 8 validated`; `:80` → prompt body from the JobSpec `custom_prompt_dir` field.

**A-W15 `docs/guides/sprint-cli-tools-release-guide.md` (update)** — gap 40
1. `:17-23` → 7 subcommands: run, attach, status, logs, kill, rerun-tasks, verify-checkpoints; note `status` and `logs` print "not yet connected" stubs (`sprint/logging_.py:367-378`).
2. `:64-79` → add `--handoff/--no-handoff` (default on; writes `<results_dir>/handoff/phase-{N}-task-{id}.json` and a `task_complete` event), `--resume <task_id>` (skips validated-successful tasks; composes with `--start/--end`), `--task-parallelism K` (default 1) (`CHANGELOG.md:302-307`). Move the `--permission-flag` sub-bullet from `:77-78` under `:76`.
3. `:96-97`, `:461-467` CI → add `--yes` (or `CI=1`; any non-empty value counts, `sprint/commands.py:323-327`).
4. `:56`, `:303`, `:320` `/sc:task-unified` → `/sc:task Execute all tasks in @<phase-file> --compliance strict --strategy systematic` (`sprint/process.py:220`).
5. `:295-305` → argv `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format stream-json`, prompt on stdin (`pipeline/process.py:134-165`; `sprint/process.py:166`).
6. `:368-371` → tmux also forwards `--state-dir`, `--debug`, `--stall-*`, `--ignore-run-lock`; state that `--resume`, `--task-parallelism`, `--handoff/--no-handoff`, `--yes` are not forwarded in tmux mode (`sprint/tmux.py:178-217`; code finding O9) and recommend `--no-tmux` when using them.

**A-W16 `docs/guides/reflect-cli-tools-guide.md` (update)** — gap 41
1. `:28-31`, `:59-60`, `:262-273` → with `--depth standard` (default) the corrective artifact is a `/sc:workflow` plan run via `/sc:implement <remediation_plan_path>`; `/task <remediation_task_path>` only with `--depth deep`; the MDTM pointer wins if both are set; HALT only when neither is present (`runner.py:474-477,597,769-775`; `CHANGELOG.md:262`).
2. `:41` → wrapper consumes `remediation_task_path` and `remediation_plan_path` (contract 1.8.0).
3. Add a section for `superclaude reflect contract-status [--validate] [--repo OWNER/NAME] [--pr N]` (prints `state:`, `checked_paths:`, `blocker_count:`, `next_command:`; suggests `/sc:pr-submit --monitor 3 --pr <N>` when ready; `reflect/commands.py:145-200`).
4. Warn: if `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` is exported in your shell, every `reflect` subcommand exits 0 at once (`reflect/commands.py:62-73`).

**A-W17 `docs/guides/cli-portify-and-pipeline-runner-guide.md` (update)** — gap 42
1. `:80` → one convergence iteration (2 review passes); converges when no CRITICAL is unaddressed, else escalates to the user; score ≥ 7.0 only sets `downstream_ready` (`sc-cli-portify-protocol/SKILL.md:367-380`).
2. `:495-506` → add `--cli-name` (alias of `--name`), `--commands-dir`, `--skills-dir`, `--agents-dir`, `--include-agent`, `--save-manifest`, `--start` (alias of `--resume`), `--max-convergence` (default 1; currently has no effect, `v5.0.0.md:229`), `--gate-mode [shadow|soft|full]` (`cli-portify run --help`).
3. `:199-202` → prompt on stdin; output format per caller (default stream-json); reviewer profile drops the permission flag and `--tools default` (`pipeline/process.py:95,137,144-153`).
4. `:400-425` → roadmap runner takes `INPUT_FILES...` (1-3: spec, TDD, PRD) and link the roadmap guide for the step list.

**A-W18 `docs/guides/roadmap-cli-tools-release-guide.md` (update)** — gap 43
1. `:104`, `:117-125` → `superclaude roadmap run [OPTIONS] INPUT_FILES...` (1-3 markdown files, auto-detected).
2. `:127-141` → add `--no-convergence`, `--input-type [auto|tdd|spec]`, `--tdd-file`, `--prd-file`, `--no-compress`, `--allow-cosmetic-remediation/--no-allow-cosmetic-remediation`, `--strict-no-remediation`, and one line pointing to `roadmap run --help` for the 11 `--tool-write-*` flags.
3. `:899`, `:1420` → `convergence_enabled` default `True`; disable with `--no-convergence` (`roadmap/models.py:111-113`; `roadmap/commands.py:362`).

**A-W19 `docs/guides/prd-skill-release-guide.md` (update)** — gap 44
1. `:261`, `:455`, `:620` → "max 2 fix cycles (3 reviews), then HALT and escalate the open blocking findings to you" (`skills/prd/refs/build-request-template.md:130`).
2. `:332` → "Only blocking findings (CRITICAL, IMPORTANT) must be resolved; MINOR findings are notes, never fail a gate and are not rechecked" (`skills/prd/refs/agent-prompts.md:273,283`).
3. Add a pointer: `superclaude prd run "<request>" [--tier ...] [--dry-run]` and `superclaude prd resume <STEP_ID>` run the same pipeline headlessly; research fix cycles default to 2 (`prd/commands.py:115-234`).
4. Frontmatter `last_updated` → 2026-11-02.

**A-W20 `docs/guides/tdd-skill-release-guide.md` (update)** — gap 45
1. `:271`, `:477`, `:652` → "max 2 fix cycles; after 2 fix cycles (3 reviews) execution halts and escalates" (`skills/tdd/refs/build-request-template.md:125`).
2. `:265` "Minor still must be fixed" → "Minor gaps are notes and do not fail the gate" (`skills/tdd/refs/agent-prompts.md:282`).
3. `:345` → only blocking findings must be resolved (`agent-prompts.md:291,340-341`).
4. Frontmatter `last_updated` → 2026-11-02.

**A-W21 `docs/guides/suites-guide.md` (update)** — gap 46
1. `:44-51`, `:64-77` → delete the "stash@{0}" column/section; all 17 suites are on disk (`ls src/superclaude/cli/eval/suites/`; `superclaude eval list`).
2. `:214`, `:243`, `:271`, `:293`, `:323`, `:354`, `:385`, `:409` → delete each `git stash apply stash@{0} -- ...` line (unsafe: the stash stack is shared across worktrees and sessions).
3. `:59-61` → "87 expanded evals across 17 suites, including `real` (17)".

**A-W22 `docs/user-guide/codegraph.md` (create)** — gap 47. A user guide (not install). Sections and sources:
1. What codegraph does for you (symbol, caller, impact answers; commands fall back to Grep/Read) — `core/CODEGRAPH.md:11-34`; `CHANGELOG.md:84-87`.
2. Install and removal: one paragraph + link `mcp-installation.md#default-setup-codegraph` and `#removing-codegraph`.
3. Indexing: one index per checkout; SessionStart (startup only) runs one background `codegraph init --yes` when `<top>/.codegraph/codegraph.db` is absent; skipped for `$HOME` and `/`; log `${XDG_STATE_HOME:-~/.local/state}/superclaude/codegraph-init.log`; about 70 KB per file and up to about 1 GB memory on first init; `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` (recommended for CI) — `codegraph-session-start.sh:6-31`; `CHANGELOG.md:93`.
4. `/sc:graph`: the 8-line status report fields; `next:` values (disabled → enable; absent → install; not initialized → type `/sc:graph init`; foreign index → `--worktree-local`; pin mismatch → `superclaude install --force` or `./update.sh`; stale → wait for sync); `init` refusals `already_initialized`, `init_running`, `nested_worktree`; init runs only when your own message starts with `/sc:graph init`; 600 s timeout — `sc-graph-protocol/SKILL.md:25-26,50-82,142-151`; `commands/graph.md:20-53`.
5. `/sc:impact`: usage examples (`impact.md:20-25`), flags (`:29-38`), outputs and labels `def-line` / `call-site-verified` / `unresolved` with shown/total (`:47-57`), never claims "no dependents" from an empty graph (`:63`), Grep fallback → `status: partial`.
6. Which commands use codegraph: troubleshoot, reflect, validate-roadmap, brainstorm, cleanup-audit, auggie-review, task, tasklist, explain (one-hop view), four agents; `/sc:implement`, `/sc:pr-submit`, `/sc:troubleshoot --fix`, `/sc:auggie-review`, `/sc:task` (STRICT), `/sc:reflect` call `/sc:impact` for context only (`CHANGELOG.md:84-86`).
7. Switches: `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` (commands/skills/agents only) vs `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` (hook only); neither touches the registration.
8. Troubleshooting: `codegraph` must be on PATH for `/sc:graph init` (allowlist `Bash(codegraph init --yes *)`, `graph.md:9`; installer links `~/.local/bin/codegraph` and warns when it is not on PATH, `install_codegraph.py:155-163`); restart Claude after install; `superclaude doctor --verbose` and `superclaude install --list` codegraph block.
9. Link from `docs/user-guide/commands.md`, `mcp-servers.md`, `README.md`.

### Workstream B — technical docs

**B-W1 `src/superclaude/rules/core/changelog_maintenance.md` (update)** — gap 48. Installed to `~/.claude/rules/core/` (`install_user_setup.py:94-97`), so it runs in other projects: keep paths project-relative and generic.
1. `:107` "Save to: `.claude/changelogs/`" → "Save to `docs/releases/vX.Y.Z.md` (tracked; `.claude/` is git-ignored)" (`.gitignore:127-128`; DECISIONS 7.3).
2. `:115` → `**Detailed Release Notes**: [docs/releases/vX.Y.Z.md](docs/releases/vX.Y.Z.md)`.
3. `:134-136` → `gh release create vX.Y.Z --repo <owner>/<repo> --title "..." --notes-file docs/releases/vX.Y.Z.md`, plus: "Always pass `--repo`: in a fork gh defaults to the parent repository. For IronClaude: `--repo IronbellyOrg/IronClaude`."
4. `:35` (frontmatter link), `:139`, `:168`, `:184` → drop the `.claude/changelogs/README.md` references (file does not exist); `:139` web-UI option → "attach `docs/releases/vX.Y.Z.md` as the release body".
5. `:166` → "Detailed files: `docs/releases/vX.Y.Z.md`".
6. `:37`, `:105`, `:167` template path → `~/.claude/templates/workflow/changelog_template.md` (installed copy; in an IronClaude dev checkout also `.claude/templates/...` after `make sync-dev`).
7. Keep `## [Unreleased]` guidance (`:60-70`): verified, `CHANGELOG.md:5` keeps an empty Unreleased header above 5.0.0.
8. Run `make sync-dev`, `make verify-sync`; grep the file for `.claude/changelogs` (expect 0).

**B-W2 `docs/reference/common-issues.md` (update)** — gap 49
1. `:18`, `:83` → `superclaude --version` prints `SuperClaude, version 5.0.0`.
2. `:22`, `:25`, `:28` → upgrade: `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install --force`; from a clone `./update.sh`; link `../getting-started/upgrading.md`. Note `superclaude update` refreshes files only.
3. `:36`, `:39`, `:71`, `:78` → `pipx install git+https://github.com/IronbellyOrg/IronClaude` (the PyPI `superclaude` package is upstream).
4. `:48` → remove `/sc:analyze . --no-mcp` (`analyze.md:22` flags are `--focus --depth --format`).
5. `:49` → Node.js 18+ (20+ for Auggie).
6. `:55` → `superclaude install --force`; `:64` → remove `--install-dir` (only `--target`, commands dir; Windows support unverified and codegraph is Linux/macOS only); `:85` → `superclaude install --list`.

**B-W3 `docs/reference/troubleshooting.md` (update)** — gap 50
1. `:10`, `:25`, `:73` → `superclaude --version` → 5.0.0. `:11`, `:27` → `superclaude install --list`; MCP state `superclaude mcp --list`.
2. `:37-59` → fork install with pipx (drop PyPI `SuperClaude`, `--break-system-packages`).
3. `:65` → `superclaude install --force`. `:84-85` → remove `--no-mcp`/`--scope file` on `/sc:analyze`.
4. `:93` → check MCP registrations with `claude mcp list` (user scope lives in `~/.claude.json`). `:94-95` → Node 18+; `superclaude mcp --servers <name>`.
5. `:98-102` → drop Magic / `TWENTYFIRST_API_KEY`; keep `MORPH_API_KEY`.
6. `:106` → drop "(v4.3+)". `:147-148` → `superclaude doctor --verbose`. `:161-163` → `superclaude install --force` (no `backup`, `uninstall`, `install --fresh`).
7. `:175` → `https://github.com/IronbellyOrg/IronClaude/issues`.

**B-W4 `docs/reference/mcp-server-guide.md` (update, keep `:13-44` codegraph section)** — gap 51
1. `:13-16` → list every registry server: codegraph (default), context7, playwright, morphllm-fast-apply, tavily, auggie, litellm (opt-in), plus the AIRIS gateway (`install_mcp.py:43-116`).
2. `:52`, `:85`, `:152`, `:614` → Node 18+ (20+ Auggie).
3. `:105-136`, `:153`, `:244-270`, `:522` → Context7 is `@upstash/context7-mcp` run via `npx -y`; no global npm install (`install_mcp.py:47`). `:345-348` → Morphllm `@morphllm/morphmcp` (`:61`).
4. `:162`, `:580` → `superclaude mcp --servers <name>`.
5. `:156` → `claude mcp get context7`.
6. `:199`, `:227`, `:381` → remove `--all-mcp`; `--no-mcp` only on `/sc:troubleshoot`, `/sc:reflect`.
7. `:169-170`, `:213-230`, `:455-458` → remove placeholder ports 8000-8002, `context7-server.example.com`, `~/.claude/mcp-config.json`, `MCP_CONTEXT7_TIMEOUT` (no source).
8. `:605-606` → IronbellyOrg/IronClaude issues (drop Discussions link unless it exists on the fork).

**B-W5 `docs/mcp/mcp-optional-design.md` (update)** — gap 52
1. `:9`, `:312` → "`superclaude install` installs and registers codegraph (required phase, exit 1 on failure); every other MCP server is optional via `superclaude mcp`" (`main.py:239-253`).
2. `:29-33` → code understanding: codegraph for structure (symbols, callers, impact), Auggie for semantic search, Grep/Read floor always (`core/CODEGRAPH.md`).
3. `:49-51`, `:179-180` → cross-session memory is plain markdown under `<project>/.superclaude/memory/`, no MCP needed (`agents/pm-agent.md:19-35`).
4. `:65`, `:107`, `:138`, `:271-279`, `:321` → remove Mindbase auto-load/auto-save and "Install Mindbase".
5. `:200-210` → mark the per-MCP JSON config as illustrative (no such key in `src/superclaude/cli/`).

**B-W6 `docs/mcp/mcp-integration-policy.md` (update)** — gap 53
1. `:5-168` → add codegraph as the default-installed server; `:169-224` selection matrix routes code structure to codegraph.
2. `:235`, `:248-249`, `:280-281` → session start reads `<project>/.superclaude/memory/*.md` (no `docs/patterns`, `docs/mistakes`).
3. `:303`, `:317` → `--c7`, `--tavily` are advisory hints, not parsed flags.
4. `:406` → state modes are not installed. `:419-421` → `~/.claude/agents/pm-agent.md`, `~/.claude/RULES.md`; drop the modes line.

**B-W7 `docs/reference/diagnostic-reference.md` (update)** — gap 54
1. `:301-305` → replace `rm -rf ~/.claude` with `superclaude install --force` and a warning never to delete `~/.claude` (it holds Claude Code settings, transcripts, other tools' files).
2. `:80-90` → `grep '^@' ~/.claude/CLAUDE.md` should print exactly one line, `@BASH_INSPECTION_POLICY.md` (`core/CLAUDE.md:3`).
3. `:180`, `:209` → `~/.claude/commands/sc/$COMMAND.md` (`main.py:32`).
4. `:5-7`, `:321-326` → hooks, the codegraph SessionStart init and the CLI pipelines do run processes and network (`hooks.json:28`).

**B-W8 `docs/reference/deviation-report-format.md` + `docs/reference/pm-agent-autonomous-reflection.md` (update)** — gap 55
1. `deviation-report-format.md:105` → point to the model actually defined in `src/superclaude/cli/roadmap/fidelity_checker.py` (writer: read that file and name the class) or drop the row; `fidelity.py`/`FidelityDeviation` do not exist.
2. `pm-agent-autonomous-reflection.md` → add one line: ReflexionPattern stores in `docs/memory/` (`reflexion.py:65-77`); session memory from `/sc:save` lives in `<project>/.superclaude/memory/` (`agents/pm-agent.md:19-35`).

**B-W9 `docs/developer-guide/technical-architecture.md` (update)** — gap 56
1. `:25-33` → add `CODEGRAPH.md`, `ISSUE-HANDOFF.md`, `ISSUE-BACKLOG.md` (11 core files; `src/superclaude/core/`).
2. `:34-53`, `:72-98` → replace fixed lists with counts (45 agents, 45 commands) and "run `superclaude install --list`"; remove nonexistent `spec-panel-experts`, `test-runner`, `wave-orchestrator`, `estimate.md`, `select-tool.md`; name `/sc:impact`, `/sc:graph`.
3. `:54-62` → add `codegraph-session-start.sh` (5.0.0), `auggie-flag-clear.sh`, `pragmatic-subagent.js`, ccsession `session-name.sh`; drop "(v4.3+)" (`hooks.json:28,58,69,104,124`).
4. `:24-102` → add `skills/`, `templates/`, `rules/`, `output-styles/` and the non-`~/.claude` paths (`~/.codegraph/`, `~/.local/bin/codegraph`, `~/.local/bin/ccsession{,-orca}`).
5. `:314-318` → describe the Python CLI pipelines and hooks as executing components; note the removed core files (ORCHESTRATOR/COMMANDS/PERSONAS/MODES/FLAGS/MCP.md) and that `HOW-WE-WORK.md` replaces their routing content.

**B-W10 `docs/developer-guide/contributing-code.md` (update)** — gap 57
1. `:26`, `:54` → Node 18+ (20+ Auggie). `:355` → `grep '^@' ~/.claude/CLAUDE.md`.
2. `:315-322` → remove "Adding New Modes" (modes are not installed).
3. `:179` → stage named paths; never `git add -f` under `.claude/`.
4. Add the sync step: edit `src/superclaude/`, `make sync-dev`, `make verify-sync` (repo `CLAUDE.md` Component Sync).

**B-W11 `docs/developer-guide/testing-debugging.md` (update)** — gap 58
1. `:133` → Node 18+.
2. `:113-141` → add `superclaude install --list` codegraph block (`User registration: matches`, `Ready for Serena retirement: yes`) and `superclaude doctor --verbose` codegraph check (transcript lines 330-341, 765-783).
3. `:306-307` → replace `rm -rf ~/.claude` with `superclaude install --force`.
4. `:7`, `:319-322` → the repo has a pytest suite (`make test`) and executable CLI pipelines.

**B-W12 `docs/developer-guide/README.md` (update)** — gap 59
1. `:38`, `:39`, `:45`, `:51` → point anchors at existing headings in `technical-architecture.md` / `testing-debugging.md`.
2. `:59`, `:75-78` → the package ships the `superclaude` CLI; `/sc:save`/`/sc:load` persist memory in files.
3. `:130` → Python 3.10+; `:132` → Node 18+; `:142` → `~/.claude/commands/sc/implement.md`; `:152-156` → remove modes.
4. `:174`, `:198` → `https://github.com/IronbellyOrg/IronClaude`.
5. `:88-124` → remove WCAG / "240+ glossary terms" / "all examples tested" claims.
6. Link the four new notes (B-W19..B-W22).

**B-W13 `docs/developer-guide/documentation-index.md` (update)** — gap 60
1. `:82` → drop `docs/eval/release-checklist.md`. `:23`, `:55`, `:88` → drop line-count claims.
2. `:33-49` → mark `git-standards-protocols.md` as imported from another project and not IronClaude's process (gap 71); point release questions to `release-procedure.md`.
3. `:155` → remove "Mode Development". `:255` → drop the "correct Python module execution paths" claim.
4. Add entries for `codegraph-integration.md`, `session-memory.md`, `review-severity-rule.md`, `release-procedure.md`.

**B-W14 `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` (update, targeted sections only)** — gap 61
1. `:828-848` "Delegation Intelligence" and `:850-860` "Resource Management Zones" → remove (came from removed ORCHESTRATOR.md/FLAGS.md; no primitive defines them).
2. `:892-910` → replace circuit-breaker / `--all-mcp` text with: commands and skills name their MCP servers in frontmatter; codegraph, Auggie and Context7 sit above a Grep/Read floor; primitive authors follow `~/.claude/CODEGRAPH.md` (readiness check, closed `graph:*` tokens, Read before citing, `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`).
3. `:937-945` → mark `--think*` budgets as advisory hints with no installed definition.
4. `:800` `/sc:task-unified` → `/sc:task`. `:878`, `:1662`, `:1703` → `src/superclaude/skills/sc-adversarial-protocol/`. `:2063` → `src/superclaude/core/*.md`. `:2089` → drop the `docs/generated/dev-guide-research/` source line.

**B-W15 `docs/dev/sync-discipline.md` + `docs/dev/lens-contribution-policy.md` (update)** — gaps 62-63
1. `sync-discipline.md:15-16` → "`superclaude install` writes the user `~/.claude/`; `make sync-dev` writes the repo `.claude/`" (`main.py:32`; `Makefile:109`).
2. `lens-contribution-policy.md:3-5` → "8 bundled lenses plus the `custom` escape hatch (9 registry entries)" (`swarm/lenses/__init__.py:108-118`).
3. `lens-contribution-policy.md:38`, `:187` (and `:234`, `:468` mentions) → "the JobSpec `custom_prompt_dir` field (a `--custom-prompt-dir` flag is planned, not shipped)" (`swarm/commands.py:125`; `swarm run --help`).

**B-W16 `docs/sprint-cli-deep-dive.md` (update, two spots)** — gap 64
1. `:670-676` → `build_prompt()` at `sprint/process.py:173` sends `/sc:task Execute all tasks in @<phase_file> ...` (`:220`).
2. `:1642` heading "Auto-Resume (v4.3.5)" → "Auto-Resume" (4.3.5 was never tagged). Line drift elsewhere is gap 72 (deferred).

**B-W17 swarm operator docs (update)** — gap 65
1. `docs/swarm/operator-runbook.md:118` → drop "(requires the M5 contract)"; exit 1 = terminal with partial/failed contract.
2. `docs/swarm/monitoring-patterns.md:7-9` → "Wave 3 reduce now runs on a fresh run, but `done.json` is still written only by `swarm kill --output`; watch `.swarm-state.json` / `swarm status` instead".
3. `docs/swarm/rollback-procedure.md:31-45` → past tense: the sc-bare-review shell files were removed (absent at v5.0.0).

**B-W18 `KNOWLEDGE.md` + `CONTRIBUTING.md` (update)** — gap 66
1. `KNOWLEDGE.md:257` → to pick up local source edits run `./update.sh` (or `pipx install --force ./` from the checkout); `pipx reinstall` reinstalls from the original spec; drop the host-specific venv path (`update.sh:7`).
2. `CONTRIBUTING.md:26` → compare against master in a separate worktree (`git worktree add .dev/worktrees/master-check master`) instead of `git stash` (shared stash stack).
3. `CONTRIBUTING.md` → add: open PRs with `/sc:pr-submit --monitor 3`; fallback `gh pr create --repo IronbellyOrg/IronClaude ...` (repo `CLAUDE.md`).

**B-W19 `docs/developer-guide/codegraph-integration.md` (create)** — gap 67. Design note; cite code for every claim.
1. Install pipeline: discover (PATH, then `~/.local/bin`, exact `1.6.2`), platform table (linux/darwin × x64/arm64), pre-existing dir rule, download URL + 60 s timeout, SHA-256 pin, strict tar extraction limits, receipt written first, links never replace foreign links, pointer `~/.codegraph/.superclaude-bin`, prune one run later — `install_codegraph.py:26-72,97-163,193-264,273-404`.
2. Registration: user scope only; `claude --version` prerequisite; reads `mcpServers.codegraph` from `$CLAUDE_CONFIG_DIR/.claude.json` or `~/.claude.json`; writes only via `claude mcp add-json ... --scope user`; exact entry (stdio, `serve --mcp`, `alwaysLoad`, telemetry/update-check off, `CODEGRAPH_MCP_TOOLS=node,search,callers,callees,impact,files,status`); owned entry repaired, user-managed working entry kept — `install_mcp.py:709-1020`. Why `codegraph_explore` is hidden: about 1,861 extra tokens per session in four headless runs (`CHANGELOG.md:92`).
3. Sequencing: step 8 of `superclaude install`, required, `--force` not forwarded, exit 1 after framework steps already ran; `update` skips it — `main.py:52,239-253,269-280,334-429`.
4. SessionStart hook: matcher `startup`, timeout 5, skip rules, detached `nohup`, log path, cost model — `hooks.json:23-31`; `codegraph-session-start.sh:6-31`; `CHANGELOG.md:93`.
5. Primitive contract: `core/CODEGRAPH.md` readiness check, closed `graph:*` tokens, Read-before-cite, Grep/Read floor, `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`; `core/CLAUDE.md` block between `SUPERCLAUDE_CODEGRAPH_BEGIN/END` (`core/CLAUDE.md:28-30`); `/sc:graph` (readiness, only manual init) and `/sc:impact` (never stops its caller) roles.
6. Observability: `install --list` block (no download, no `claude mcp` call; `install_mcp.py:1059-1060`), `doctor` check fails only for a non-executable command (`doctor.py:160-175`).
7. Retire step: proof-of-authorship shapes (`install_retired_mcp.py:56-89`), user scope only, 10 s per call / 15 s total, never changes the exit code, `serena-local` exempt, current-pin Serena kept until codegraph is ready, receipt/marker files `~/.local/bin/.superclaude-codebase-memory.json` and `.pending`, `install --list` verdict lines, `doctor` warning, `update` notice — `install_retired_mcp.py:35,214-494`; `main.py:255-267,407-415`; `CHANGELOG.md:108-115`.
8. Pin update: describe only what the code shows (the version constant and SHA table at `install_codegraph.py:26-33`, the pin text in `core/CODEGRAPH.md:34`, and the tests that pin them — writer: grep `tests/` for `1.6.2`); mark anything else UNVERIFIED.

**B-W20 `docs/developer-guide/session-memory.md` (create)** — gap 68
1. Store: `<project>/.superclaude/memory/<key>.md`, `<project>` = `git rev-parse --show-toplevel` or cwd; one store per worktree; first write creates `.superclaude/.gitignore` containing `*` — `save.md:42-43`; `load.md:42`.
2. Keys: single-owner `pm_context`, `last_session`, `next_actions` overwritten; parallel keys (`checkpoint`, `decision`, handoffs) written as `<key>-<session-or-timestamp>.md` — `save.md:44-45`.
3. Consumers: `/sc:save`, `/sc:load`, `/sc:pm`, PM agent — `pm.md:16,47`; `agents/pm-agent.md:19-35`. Behaviour is prompt-driven (no script), so wording varies.
4. Migration: one-release read-only `.serena/memories/<key>.md` fallback, never written — `load.md:43`; `v5.0.0.md:154,173,198`.
5. Why: Serena removed (Breaking Change 1); no MCP needed; contrast with ReflexionPattern `docs/memory/` (`reflexion.py:65-77`).

**B-W21 `docs/developer-guide/review-severity-rule.md` (create)** — gap 69
1. Decisions B1-B5 (`DECISIONS.md:12-19`): minor findings are notes; 2 fix cycles = 3 reviews; HALT and escalate at the cap; `/sc:implement` drops the second A2 repair; cli-portify 1 iteration.
2. Rule text S1-S5: `output-styles/pragmatic.md:225-229`; injected into every subagent by `pragmatic-subagent.js` on SubagentStart (`hooks.json:120-127`; script exits 1 if `~/.claude/output-styles/pragmatic.md` is missing).
3. Scope list: `CHANGELOG.md:29-33` (rf-qa agents, QA and MDTM templates, prd/tdd/task/task-builder skills, prd CLI default 2, `/sc:tasklist` patch loop, cli-portify).
4. Guard: `tests/skills/test_review_severity_rule.py` (fails CI on old wording, caps above 2, Open-Questions-at-cap, minor-to-fix-pass).
5. Known exceptions/open items: `--max-convergence` not wired (DECISIONS B4 amended; Known Issue `v5.0.0.md:229`); roadmap convergence `max_runs=3` (O10); `sc-cli-eval-protocol` "max 3 fix loops" (O18) — state as open questions, not as rule violations.

**B-W22 `docs/developer-guide/release-procedure.md` (create)** — gap 70
1. Version: `pyproject.toml` `version`, `src/superclaude/__init__.py` `__version__`, `superclaude --version` agree (G3).
2. Changelog: keep `## [Unreleased]` empty above `## [X.Y.Z] - YYYY-MM-DD` (G4); detailed notes at `docs/releases/vX.Y.Z.md` from `~/.claude/templates/workflow/changelog_template.md` (DECISIONS 7.3).
3. Gate G1-G9 (generalize `RELEASE-READINESS.md:192-200`): fork target (`git remote -v`, `gh repo view --json nameWithOwner`), CI on the exact merge commit, version consistency, changelog cut, `make test`/`lint`/`verify-sync`/`verify-deps`/`lint-architecture`, `uv build`, upgrade path on an existing workspace (`./update.sh`, new session, `doctor`, `install --list`, `/sc:graph status`), release-specific checks, no open PR meant for the release. Any failure stops and goes back to the owner (DECISIONS T1, 7.7).
4. Tag and publish: `git tag vX.Y.Z`, `git push origin vX.Y.Z`, `gh release create vX.Y.Z --repo IronbellyOrg/IronClaude --title "..." --notes-file docs/releases/vX.Y.Z.md`.
5. After the tag: `/sc:post-release vX.Y.Z` (DECISIONS T1).
6. Link from `docs/developer-guide/README.md`, `documentation-index.md`, and the empty section 6 of `git-standards-protocols.md` (one-line pointer only).

### Workstream C — install and upgrade

**C-W1 `docs/getting-started/installation.md` (update)** — gaps 1-4, 6-14
1. `:53-57` → "Existing installations upgrade with `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude install --force`; see `upgrading.md`" (`main.py:239-267`; `v5.0.0.md:144`).
2. `:326-333` → replace `superclaude update` with `superclaude install --force` in the pipx and pip blocks.
3. `:363` → "A plain `superclaude install` keeps existing framework files; run `superclaude install --force` to refresh them (it also installs codegraph and retires old MCP registrations)."
4. `:365` warning → keep the backup advice; say `install --force` overwrites the same files as `update` and also runs codegraph + retire, and exits 1 if codegraph fails after the files are already refreshed (`main.py:178-280`; `v5.0.0.md:233`).
5. `:80-94` prerequisites → Required: Python ≥3.10 (`pyproject.toml:16`), git, pipx (recommended) or pip, the Claude Code CLI `claude` on PATH, network to GitHub (codegraph download). Install exits 1 without `claude` (`install_mcp.py:937-947`).
6. `:34`, `:164-198` → codegraph auto-install supports Linux and macOS on x64/arm64 only; elsewhere `superclaude install` exits 1 unless a `codegraph` printing `1.6.2` is on PATH; hooks are bash (`install_codegraph.py:46-52,280-289`).
7. `:134`, `:172` → on PEP 668 systems use `uv tool install pipx` or the distro pipx package instead of `python3 -m pip install --user pipx`.
8. `:280-286` → verify with `superclaude --version` (5.0.0), `superclaude install --list` (codegraph `User registration: matches`, `Ready for Serena retirement: yes`), `superclaude doctor --verbose` (no "no codegraph registration" line); plain `doctor` passes even without codegraph (`doctor.py:160-175`; transcript lines 326-378).
9. `:297-309` → add: `~/.claude/templates/`, `rules/`, `output-styles/`, merges into `~/.claude/settings.json` (backup `settings.json.bak.<ISO>`), `~/.local/bin/ccsession` and `ccsession-orca`, `~/.claude/ccsession.env`, `~/.codegraph/`, `~/.local/bin/codegraph`, the user `codegraph` entry in `~/.claude.json`, default plugins installed with `claude plugin install --scope user` (network, 30 s budget, never fails the step) (`main.py:174-253`; `install_user_setup.py:251-311`; `user_settings_defaults.json:28-49`).
10. `:353-361` uninstall → add codegraph removal (`claude mcp remove codegraph --scope user`, delete the paths `install --list` prints as owned; link `../user-guide/mcp-installation.md#removing-codegraph`) and `~/.local/bin/ccsession-orca`.
11. Add a short "codegraph" section: required phase, what it downloads, restart Claude afterwards, link `mcp-installation.md`.
12. Add a note: the installer always writes files under `$HOME/.claude/`; if you set `CLAUDE_CONFIG_DIR`, it is used only to read `.claude.json`, and an empty value makes codegraph registration fail (`install_mcp.py:721-726`; `install_core.py:47`).

**C-W2 `docs/user-guide/mcp-installation.md` (update)** — gaps 5, 18
1. `:71` → "`--force` only changes the framework-file steps (overwrite instead of skip). The codegraph phase and the cleanup step run on every `superclaude install`, with or without `--force`. `--target` changes only the slash-command destination. There is no framework-wide dry-run option." (`main.py:52,183-188,239-267`).
2. Server table (`:97-105`) → add "**litellm** — LiteLLM MCP gateway (`http://ibcore:4000/mcp/`, header `x-litellm-api-key: Bearer ${LITELLM_API_KEY}`); opt-in, skipped by option `0`; works only on the operator's network with an issued key" (`install_mcp.py:107-115,1406-1410`).
3. `:85-86` "Install all individual servers" example → note it omits litellm on purpose.

**C-W3 `docs/getting-started/upgrading.md` (create)** — gaps 15-17
1. Who: anyone on 4.x (including the untagged 4.3.5) moving to 5.0.0.
2. Back up edited `~/.claude` files (`cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.mine`); `install --force` overwrites every shipped file and deletes/re-copies each shipped skill folder (`v5.0.0.md:143`; `install_skill.py:46-48`).
3. Upgrade: `pipx install --force git+https://github.com/IronbellyOrg/IronClaude`, then `superclaude install --force` (`v5.0.0.md:146-149`). Why not plain `install` (skips existing files) or `update` (no codegraph, no retire; `main.py:334-429`). If you already ran `update`, run `install --force` now.
4. From a clone: `git fetch origin && git checkout v5.0.0` (or update master), then `./update.sh`; it installs the checked-out working tree (`update.sh:7`), runs `superclaude install --force` (`:8`), `make sync-dev` (`:9`, needs `make`) and `superclaude doctor` (`:10`); needs `pipx` on PATH (`uv tool install pipx`).
5. What happens: framework files refreshed; codegraph 1.6.2 downloaded, SHA-256 verified and registered; old `codebase-memory-mcp`/`serena` user registrations that IronClaude wrote are removed; anything else is kept with the reason and a removal command printed. If codegraph fails (no network, no `claude`, unsupported platform) the command exits 1 after the files are refreshed; fix and re-run (`v5.0.0.md:151,233`).
6. Expected output (from the e2e, transcript lines 724-736): "installed codegraph 1.6.2 (SHA-256 verified)", "Removed the codebase-memory-mcp user registration (codegraph is ready: kind-B registration (binary and companions stay))", the printed manual-cleanup commands.
7. Restart every running Claude session (a running session can write a removed registration back) and the ccsession shim (`pkill -f local-gateway-alias-proxy.py` when no session needs it) (`v5.0.0.md:152,157`).
8. Verify: `superclaude --version` → 5.0.0; `superclaude install --list` codegraph block not `absent`, `Ready for Serena retirement: yes`, retired names `absent`; `superclaude doctor --verbose` passes; `/sc:graph status` in a new session reports an index state (`v5.0.0.md:153`).
9. Leftovers that stay on purpose: the codebase-memory-mcp binary and its client companions — after the e2e upgrade `doctor` listed 48 agents and 39 skills (including skill `codebase-memory`) versus 45 agents and 38 skills shipped (transcript lines 770-773). Remove them with `"$HOME/.local/bin/codebase-memory-mcp" uninstall -y --dir="$HOME/.local/bin"`; indexes in `~/.cache/codebase-memory-mcp` only if no longer needed (`CHANGELOG.md:125-149`). Old core files (`ORCHESTRATOR.md` etc.) and `~/.claude/commands/sc/README.md` stay until you delete them (`CHANGELOG.md:248,252`).
10. Memories: copy `<project>/.serena/memories/` into `<project>/.superclaude/memory/`; keep Serena only as `serena-local` (exact command `CHANGELOG.md:122`).
11. Scripts: drop `--yes` from `/sc:pr-submit`, `--uninstall`/`--yes` from `superclaude mcp`; add `--yes` or `CI=1` to `superclaude sprint run` in CI, or `--start 1` for the old behaviour; `superclaude reflect run` now promotes by default (`--no-promote` to keep the old) (`v5.0.0.md:156,218-222`).
12. Link from `installation.md`, `README.md`, `quick-start.md`, `common-issues.md`.

Item counts: A 22 (A-W1..A-W22: 21 update, 1 create), B 22 (B-W1..B-W22: 18 update, 4 create), C 3 (2 update, 1 create).

## Test guide plan (D and E)

### D — user test guides (`docs/testing/v5.0.0/user/`)

DE1's 10 CLI groups and DE2's 9 Claude-surface groups merge into 16 non-overlapping guides. Overlaps resolved: DE1 G1 + DE2 §5 (install/codegraph CLI) → D01; DE2 G1 (codegraph in Claude) → D03; DE2 G3 + G8 (routing, issue templates) → D05; DE2 G9 (ccsession tier admin) → E01; DE1 G9 + G10 → D16. Every guide uses three tiers so a tester can stop early: **Tier A** free smoke (read-only, seconds), **Tier B** local writes (throwaway `HOME`, `/tmp` output, copied fixture), **Tier C** Claude API, proxy credentials, real PRs or long runs. Each step must be marked with its cost tag: `[FREE]`, `[LOCAL-WRITE]`, `[CLAUDE-SESSION]` (needs an interactive Claude Code session, uses API tokens), `[API-LONG]` (headless `claude` subprocesses, minutes to hours), `[PROXY]` (needs `T2ProxyUrl`/`T2ProxyKey`/`T2Model0N`), `[EXTERNAL]` (creates a PR, issue or other outside state).

| Guide | Capabilities (ids) | Code-derived expected results | Hand-test cost notes |
|---|---|---|---|
| `D01-install-upgrade-doctor.md` | cli-version, cli-install, cli-install-list, cli-upgrade, cli-update, cli-update-sh, cli-install-skill, cli-doctor, codegraph-install, mcp-retire | scan/DE1 "Install, upgrade, health" + G1; scan/C "Real install path", "codegraph phase detail", "Real upgrade path", "Isolation plan" (exact `env -i HOME=... PATH=...` recipe, stubs for `codegraph`/`orca`/`orca-ide`, 4.3.5 baseline `539e2414`, Serena seed shape); transcript `docs/testing/v5.0.0/c-e2e-transcript.txt` lines 18-415 (new user) and 416-787 (upgrade) as the expected output; `docs/testing/v5.0.0/c-e2e-run.sh` | Tier A `[FREE]`: `--version`, `doctor --verbose`, `install --list`. Tier B `[LOCAL-WRITE]` + network (codegraph tarball, pipx clone, default plugins): fresh install, second install idempotent, `install --force`, `update` (shows legacy notice, no codegraph), `install-skill confidence-check --target /tmp/x`, upgrade from `539e2414`. Never against the real `HOME`. Expected upgrade leftovers: skill `codebase-memory` + 3 agents (transcript 771-773). Negative: `install-skill pm-agent` fails (help example, O3). |
| `D02-mcp-servers.md` | cli-mcp, mcp-litellm | scan/DE1 "MCP server management"; scan/A2 mcp-servers rows | Tier A `[FREE]`: `mcp --dry-run`; `mcp --dry-run --servers serena` → exit 1 "Unknown MCP server selection: serena"; `mcp --uninstall` → exit 2; `mcp </dev/null` → exit 1; `mcp --dry-run --servers litellm`. `mcp --list` is slow (one `claude mcp list` per server, budget 1-2 min). Tier B `[LOCAL-WRITE]`: `mcp --servers context7 --scope project` in a temp project (npm network). litellm real use needs the operator network and `LITELLM_API_KEY` (mark `[EXTERNAL]`). |
| `D03-codegraph-graph-impact.md` | codegraph-autoinit-hook, codegraph-primitives, sc-graph, sc-impact | scan/DE2 §1-§5 (status report order, `next_action` table, init refusals, impact flags/outputs, hook skip rules, kill switches) | `[CLAUDE-SESSION]`, cheap (15-25 min). Preconditions: install done, `~/.local/bin` on PATH, scratch git repo with Python. Steps: fresh clone with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` → `/sc:graph` shows not initialized; `/sc:graph init` → fresh; second init → `already_initialized`; `/sc:graph bogus` → blocked; hook run without the switch creates `.codegraph/codegraph.db` and the log; `/sc:impact <sym>`; `--diff`; `--tests`; symbol + `--diff` → blocked; `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` → `disabled` / `partial`, never stops. First init can use ~1 GB memory. |
| `D04-session-memory.md` | memory-files | scan/DE2 §6 | `[CLAUDE-SESSION]`, cheap. Check files, not wording (prompt-driven): `.superclaude/memory/*.md`, `.superclaude/.gitignore` = `*`, `git status` clean; new session `/sc:load` cites saved content and ends with the `/sc:graph status` line; seeded `.serena/memories/last_session.md` read and reported read-only, `.serena/` unchanged; second worktree has its own empty store; `/sc:pm` uses the same store. |
| `D05-routing-core-files-issue-templates.md` | routing-guide, core-files, issue-templates, sc-other-commands (sample) | scan/DE2 §7, §11, removed-surface notes; `help.md:21-132`; `recommend.md:32-60` | `[CLAUDE-SESSION]`, cheap. `/sc:help` prints the level table verbatim (compare with `~/.claude/HOW-WE-WORK.md:11-28`), lists `-protocol` skills last, `business-panel` shows "(no description line)" (O12); moved guide → exact "Routing guide not found" line; `/sc:recommend` level-2 and level-3 prompts; `--minstar 10` warning. Absent: `/sc:README` (new install), `/ccsession-tag`, the six core files on a fresh `HOME`. `~/.claude/ISSUE-*.md` exist with four headings; asking Claude to file a backlog issue copies the template (checksum unchanged) — filing is `[EXTERNAL]`, use a throwaway repo. |
| `D06-plan-implement-review-cap.md` | sc-workflow-implement, remediation-routing, review-severity-cap | scan/DE2 §9 and G4; `HOW-WE-WORK.md:17,24`; `troubleshoot.md:54`; `pragmatic.md:225-229` | `[CLAUDE-SESSION]` + `[API-LONG]`. Cheap checks: a subagent's injected context starts with `PRAGMATIC MODE ACTIVE`; `/sc:troubleshoot ... --fix` offers a `/sc:workflow` plan, `--fix --depth deep` offers `/task-builder`. Long: `/sc:workflow "<small feature>" --depth standard --handoff none` → `.dev/tasks/to-do/<id>/<id>.md` + check; `/sc:implement <path>` → `progress.md`, `/sc:impact` call, archive to `.dev/tasks/done/` (Linux only). Escalation after review 3 needs a seeded persistent blocking defect (long; optional). |
| `D07-pr-submit.md` | sc-pr-submit | scan/DE2 §8 | `[EXTERNAL]` + `[API-LONG]`: real PR on a sandbox branch of `IronbellyOrg/IronClaude` (or a throwaway fork), Augment and/or Codex apps, CI. Steps: `--monitor 0` opens PR only (verify URL owner `IronbellyOrg`); `--monitor 1 --pr <N>` proposes; `--monitor 2` edits locally and halts before push; bare `/sc:pr-submit --pr <N>` pushes; wrong branch → `pr_head_mismatch`; `--max-rounds 6` rejected; `--yes` behaviour (removed; rejection wording UNVERIFIED). Known issue: clean Augment "0 suggestions" may be recorded incomplete. |
| `D08-ccsession.md` | ccsession-naming, ccsession-lists, ccsession-orca, ccsession-tiers (user side) | scan/DE2 §10; `CHANGELOG.md:11-22,56-76,170-204` | Medium; Coder workspace with tier env; Orca for the Orca steps. `[CLAUDE-SESSION]` for `/rename` sync. Steps: names with spaces; `/rename` appears in the list at the next message; `--here`, `--here --all`, `--list`, `--rm`; `--ask` exit 1 on timeout/EOF, 130 on Ctrl+C; `ccsession-orca` as Orca's Claude command (asks only on a TTY, not on resume, `CCSESSION_AUTOSTART=0`); tab title `<label> · Claude Code`; `--tier 1a`, `--model`, `--models-status`, `--refresh-models`; shim survives closing its terminal (#341). Warn: `pkill -f local-gateway-alias-proxy.py` cuts every session of this user; default launch uses `--dangerously-skip-permissions`. Known flaky tests: #352. |
| `D09-hooks-freshness-pragmatic.md` | freshness-hooks (+ pragmatic injection, auggie flag) | scan/DE2 §12; `freshness-pre-edit.sh:15,84-133` | `[CLAUDE-SESSION]`, cheap. Edit an unread file → `no_prior_read` block; Read then Edit → allowed; Write a new path → `create_allowed`; external modification after Read → mtime block; `<session-context>` envelope present each turn; telemetry in `~/.claude/logs/freshness-hook.jsonl`; `AUGGIE_FIRST_DISABLE=1`. Needs `jq`, `node`. |
| `D10-sprint.md` | cli-sprint-run, cli-sprint-pertask, cli-sprint-aux | scan/DE1 "Sprint" + G3; `CHANGELOG.md:298-344` | Tier A `[FREE]`: `sprint attach`/`kill` with no session → exit 1; `status`/`logs` print stub lines (O4). Tier B `[LOCAL-WRITE]`: `sprint run <fixture> --dry-run --start 1` (fixture `.dev/e2e-reflect/tl-1/bundle/tasklist-index.md`); `verify-checkpoints` on a COPY (writes `manifest.json`, O16). Tier C `[API-LONG]`: `sprint run --no-tmux` on a 1-phase fixture; then `--resume <task_id>`, `--task-parallelism 2`, `--no-handoff` (use `--no-tmux`; tmux drops these, O9); non-interactive auto-resume without `--yes` → exit 2; `CI=0` still counts as yes (O7). |
| `D11-roadmap-tasklist.md` | cli-roadmap-tasklist | scan/DE1 "Roadmap and tasklist" + G4 | Tier B `[LOCAL-WRITE]`: `roadmap run <spec> --dry-run --output /tmp/rm-dry` (creates the dir, O17); >3 inputs → exit 2. Tier C `[API-LONG]`: `roadmap run --depth quick`, `roadmap validate` (exits 0 even with blocking issues, by design NFR-006), `tasklist validate` (exit 1 on HIGH deviations). |
| `D12-reflect.md` | cli-reflect, sc-reflect | scan/DE1 "Reflect" + G5; scan/A2 reflect guide rows; `runner.py:474-477,597` | Tier A `[FREE]`: `reflect contract-status`; `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1 superclaude reflect contract-status` → breaker line, exit 0. Tier B: `reflect run <abs task> --print-command` / `--dry-run`. Tier C: `--transport stub` (no proxy) and `openai_compat` `[PROXY]`; `--fix` uses the plan route (`/sc:implement`) unless `--depth deep`; exit codes 0/10/11/2; `--promote` default. `/sc:reflect --onboard` absent. |
| `D13-prd-portify-cleanup-audit.md` | cli-prd, cli-portify, cli-cleanup-audit | scan/DE1 "PRD", "cli-portify", "Cleanup audit" + G6 | Tier A/B: `prd run "MVP spec" --dry-run`; `cli-portify run sc:roadmap --dry-run` (help says it runs early steps; code returns first, O5); `cleanup-audit run --dry-run`. Tier C `[API-LONG]`: one lightweight run each; `--max-convergence 3` has no effect (Known Issue); Ctrl-C on cli-portify exits 0 with `EXIT_RECOMMENDATION: INTERRUPTED`. |
| `D14-swarm.md` | cli-swarm (+ `/sc:swarm-wizard`) | scan/DE1 "Swarm" + G7; scan/A2 swarm sections (live stub-run artifact list) | Tier A `[FREE]`: `validate-lenses` → `9 entries inspected, 8 validated`; `scaffold --lens bare-review | validate /dev/stdin`. Tier B `[LOCAL-WRITE]`: `swarm run --lens bare-review --transport stub --target README.md --output /tmp/sw1` → `merged.md`, `return-contract.yaml`, per-worker files, no `done.json`; `status`/`logs --output /tmp/sw1`; `--detached` + `attach`/`kill --output`; `--tui` on a TTY. Tier C `[PROXY]`: `openai_compat`; `/sc:swarm-wizard` `[CLAUDE-SESSION]`. Negative: `--lens custom` and `--custom-prompt-dir` rejected. |
| `D15-eval-harness.md` | cli-eval (+ `/sc:cli-eval`) | scan/DE1 "Eval harness" + G8; scan/A2 eval-pipeline rows | Maintainer audience; Linux only. Tier A `[FREE]`: `eval list` (17 suites), `eval describe --suite eval_smoke`, `eval doctor --json --no-mcp`. Tier B `[LOCAL-WRITE]`: `eval run --suite real --no-pty --no-mcp --output-dir /tmp/eval-runs/t1 --junit` (bare `/tmp/eval-runs` rejected); results NOT authoritative (null executor WARNING). `/sc:cli-eval` `[CLAUDE-SESSION]`. |
| `D16-init-lite-recommend-ic.md` | cli-init-lite, cli-recommend-helpers, cli-ic | scan/DE1 "Recommend helpers and init-lite", "`ic` launcher", G9, G10 | Tier A `[FREE]`: `init-lite --context-optimized --dry-run`; `recommend cache get spec-generation` → exit 1 on empty cache; `ic --help`. Tier B `[LOCAL-WRITE]`: `init-lite --context-optimized --project-root /tmp/proj --scaffold`; `--output CLAUDE.md` refused; `ic --no-yolo -- --version` with `AIENV=/tmp/aienv`. `recommend` subcommands as an appendix (plumbing). Warn: `ic` launches `claude --dangerously-skip-permissions` unless `--no-yolo`. |

Optional: `docs/testing/v5.0.0/README.md` index listing D01-D16 and E01-E02 with their cost tags.

### E — sysop-only guides (`docs/testing/v5.0.0/sysop/`)

No role, root or admin check exists in the CLI (scan/DE1 "Sysop-only candidates": only file-ownership `st_uid` checks in `install_retired_mcp.py:214,231,351`). A capability is classed sysop-only when its effect depends on a file or service only an administrator controls and it reaches other users.

| Candidate | Gate evidence | Classification | Guide |
|---|---|---|---|
| ccsession tier policy: `CCSESSION_TIER_RULES`, `CCSESSION_ACCESS`, `CCSESSION_DEFAULT_TIER`, `CCSESSION_MODEL_ORDER`, `T<N>ModelNN`, `T<N>_WINDOW` | Read from the workspace env file `/etc/aidev02/aienv.d/defaults.sh` (`models.py:104`), pushed from the Coder template; central file changed only through review; a broken line stops ccsession for every Coder user (`skills/ccsession-tag/README.md:332-336,354`); parser `models.py:63-104,454-620` | **sysop-only**; testable from repo code by pointing `AIDEV_AI_DEFAULTS_PATH` (`models.py:320-328`) at a test env file and setting `CODER_WORKSPACE_OWNER_NAME` / `CODER_WORKSPACE_OWNER_ROLES` | E01 |
| Coder role assignment feeding `role:` entries | `CODER_WORKSPACE_OWNER_ROLES` set by the Coder template (`models.py:509-518`) | sysop-only (Coder admin), outside repo code; its effect is simulated inside E01 via the env var | folded into E01 |
| Real enforcement of tier limits (gateway key scoping) | ccsession limit is advisory; "only a gateway key limited to those models enforces it" (`README.md:348-352`; `models.py:320-328,476`) | sysop-only, outside the repo (LiteLLM key config) — not testable from repo code; E01 documents the bypass as expected behaviour | none |
| Publishing `ccsession-models.json` | Every launch fetches from the fork's master (`models.py:54-57,296-314`); a push to master changes every install's picker | **sysop-only** to publish (push rights to master); testable from repo code with `CCSESSION_MODELS_URL` pointing at a candidate file and a throwaway cache dir | E02 |
| LiteLLM MCP gateway (`superclaude mcp --servers litellm`) | `opt_in_only` only excludes it from "all"; any user can register it (`install_mcp.py:107-115,1406-1410`) | ordinary command with an external operator dependency (gateway host, key issuance). CONFLICT resolved: scan/DE1 said sysop-only, scan/DE2 said ordinary — code has no gate, so ordinary | D02 |
| Proxy transport credentials (`T2ProxyUrl`, `T2ProxyKey`, `T2Model0N`; `--tier2-fallback` `T1Model0N`) | env only (`swarm/config.py:36-39`) | ordinary commands, operator-issued credentials | D12, D14 (`[PROXY]`) |
| `ic` launcher | needs `~/.aienv` (user-owned); no gate (`scripts/ic:25-30`) | ordinary (power user) | D16 |
| Coder image reinstalling Serena / codebase-memory registrations | retire step keeps shapes Coder's bundle writes (`CHANGELOG.md:111,131`) | sysop-only (Coder template), outside repo; the keep-with-reason output is user-visible | D01 |
| `CCSESSION_SHOW_ALL_MODELS=1` ("Admin options") | plain env var, own shim (`README.md:296-299`; `models.py:744`) | ordinary (labelled admin, not gated) | D08 note |
| Sprint operator knobs (`--ignore-run-lock`, `--force-fidelity[-fail]`, `--max-session-resets` with the `~/.aienv` account pool, `SUPERCLAUDE_PROMPT_MAX_BYTES`, `SUPERCLAUDE_SPRINT_RENDER_DIAG`) | flags/env, no gate (`sprint/commands.py:159-250`; `pipeline/process.py:53-58`; `sprint/tui.py:112-118`) | ordinary (operator-flavoured) | D10 notes |
| Shim lifecycle, codegraph kill switches, `AUGGIE_FIRST_DISABLE`, hook opt-out, `/sc:pr-submit --monitor 3` push | user env / user `~/.claude/settings.json` / repo write rights | ordinary | D03, D08, D09, D07 |
| `eval` group | Linux-only, scratch-root allowlist (`eval/commands.py:844-859`) | maintainer audience, not sysop | D15 |

| Guide | Capabilities | Expected results (code) | Cost / safety notes |
|---|---|---|---|
| `E01-ccsession-tier-policy.md` | ccsession-tiers (admin side) | Rules grammar `<who>=<start>[:<tiers>][+models]`; precedence username > first matching `role:` > `*` (`models.py:72-79,522-620`); `CCSESSION_ACCESS` read only when no rules line (`models.py:81-85`); a broken or duplicate entry for the owner stops the launch with the reason (`models.py:557-581`); a limited user's `--help`, `/model` list and `--tier`/`--model` cover only allowed tiers; `ccsession --models-status` shows the owner's access; letter tiers `T1a_WINDOW`, `claude-gw-tier1a` (`CHANGELOG.md:155-168,186`) | Never edit the real `/etc/aidev02/aienv.d/defaults.sh`: use `AIDEV_AI_DEFAULTS_PATH=/tmp/defaults.sh` plus `CODER_WORKSPACE_OWNER_NAME`/`_ROLES` in a throwaway shell. Mostly `[FREE]` (`--models-status`, `--help`); launching Claude is `[CLAUDE-SESSION]`. Record the advisory-limit bypass (owner can unset env, `CCSESSION_TIERS=0`) as expected. Rollout on the real file needs Coder admin review. |
| `E02-ccsession-model-data-publishing.md` | ccsession-model-data | Schema 2 required (`models.py:53`); 256 KiB cap (`:59`); id/name/label/tier regexes (`:60-65`); older ccsession rejects letter-tier data and keeps its copy (`CHANGELOG.md:160`); `refresh()` reports status and prints a change line when the version changes (`models.py:296-314`); `CCSESSION_MODELS_REFRESH=0` skips the fetch | Validate a candidate file before pushing to master: `CCSESSION_MODELS_URL=<candidate URL> ccsession --refresh-models` then `--models-status`, with `HOME`/`XDG_CACHE_HOME` pointing at a temp dir (cache writes `models.checked`, `models.py:305-308`). Whether a `file://` URL passes `_fetch` is UNVERIFIED — writer reads `models.py` `_fetch` (around `:270-293`) and, if needed, serves the file over a local HTTP URL. Publishing itself is `[EXTERNAL]` (push to master of the fork affects every install). |

## Out-of-scope code findings (follow-up issues)

Never fixed in this run. File each with `~/.claude/ISSUE-BACKLOG.md` and `gh issue create --repo IronbellyOrg/IronClaude --body-file <copy>`.

| # | Finding | Evidence | Status |
|---|---|---|---|
| O1 | Flaky ccsession shim tests under load | issue #352 (OPEN): "Flaky ccsession shim tests in tests/unit/test_ccsession_tiers.py under load" | existing reference |
| O2 | `superclaude update --help` lists only core/commands/agents/skills/hooks; it also does ccsession, templates, user setup, and never codegraph | `main.py:344-345` vs `:365-404` | new |
| O3 | `install-skill` help example `pm-agent` has no matching skill folder, so the example exits 1 | `main.py:448-452`; `install_skill.py:58-97` | new |
| O4 | `sprint status` and `sprint logs` are stubs ("not yet connected"); help says they read the log | `sprint/logging_.py:367-378` | new |
| O5 | `cli-portify run --dry-run` help says it runs the early steps; the command returns before `run_portify` | `cli_portify/commands.py:196-204` | new |
| O6 | `--max-convergence` not wired to the convergence engine | DECISIONS B4 (amended); Known Issue `v5.0.0.md:229`; follow-up noted in #343 | existing follow-up |
| O7 | `CI` / `SUPERCLAUDE_SPRINT_ASSUME_YES` truthiness: any non-empty value, including `CI=0`/`false`, auto-assents | `sprint/commands.py:323-327,891-895` | new |
| O8 | An exported `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` makes every `reflect` subcommand exit 0 silently (looks like a pass) | `reflect/commands.py:44,62-73` | new (design risk) |
| O9 | tmux mode rebuilds the inner worker from argv and does not forward `--resume`, `--task-parallelism`, `--handoff/--no-handoff`, `--yes` | `sprint/tmux.py:178-217` (comment `:210-214`) | new; UNVERIFIED at runtime |
| O10 | Roadmap convergence allows `max_runs=3`, above the 5.0.0 2-fix-cycle cap (changelog scope does not name roadmap) | `roadmap/convergence.py:440,446` | new; intent UNVERIFIED |
| O11 | Swarm `refactor-find` lens hands off to `/sc:code-review`, which is not a shipped SuperClaude command | `swarm/lenses/refactor_find.py:53` | new |
| O12 | `business-panel.md` has no `description:` line, so `/sc:help` prints "(no description line)" | `src/superclaude/commands/business-panel.md` (grep `^description:` = 0) | new |
| O13 | `improve.md` and `cleanup.md` examples use flags their syntax does not declare (`--type security --validate`, `--preview`) | `commands/improve.md:89`; `commands/cleanup.md:73` | new |
| O14 | Plain `superclaude doctor` passes with no codegraph registration (only a detail line) | `doctor.py:160-175`; Known Issue `v5.0.0.md:232` | existing known issue |
| O15 | Installer reads `$CLAUDE_CONFIG_DIR/.claude.json` but always writes files to `$HOME/.claude/`; an empty value fails registration | `install_mcp.py:721-726`; `install_core.py:47`; `install_hooks.py:136` | new |
| O16 | `sprint verify-checkpoints` writes `OUTPUT_DIR/manifest.json` even without `--recover` | `sprint/commands.py:747-748` | new |
| O17 | `roadmap run --dry-run` creates the output directory before the dry-run branch | `roadmap/executor.py:3670,3735-3737` | new (minor) |
| O18 | `sc-cli-eval-protocol` allows "max 3 fix loops" for manifest loader errors; check whether the 2-fix-cycle rule and `test_review_severity_rule.py` are meant to cover non-review loops | `skills/sc-cli-eval-protocol/SKILL.md:204`; `refs/create-pipeline.md:50` | new; may be intended |
| O19 | A fresh swarm run never writes `done.json` (only `swarm kill --output`); resume path unclear | live stub run (scan/A2); `swarm/reduce.py:139` | new; UNVERIFIED for resume |
| O20 | `/sc:graph init` allowlist is `Bash(codegraph init --yes *)`; when `~/.local/bin` is not on PATH the bare command may not resolve | `commands/graph.md:9`; `install_codegraph.py:155-163` | new; UNVERIFIED |
| O21 | Upgrade leaves codebase-memory-mcp companions (skill `codebase-memory`, 3 agents); retire step says "binary and companions stay" but does not list the companion paths | transcript lines 729-736, 771-773 | by design; consider printing the paths |
| O22 | e2e harness reported `REAL_HOME_CHANGED` (`/home/coder/.claude.json` mtime) although the registration went to the throwaway `HOME` and the real file has no `ic-e2e` path (checked: `grep -c ic-e2e` = 0); most likely concurrent live sessions writing that file | transcript lines 785-798; `c-e2e-run.sh:31,68-69` | re-run the e2e with no other Claude session active to confirm `claude` under a fake `HOME` never touches the real file |

## Self-audit

What was checked:

- Read all six scans, `DECISIONS.md`, `docs/releases/v5.0.0.md` in full, `CHANGELOG.md` lines 1-435 (the whole 5.0.0 section), and the e2e transcript (summary, counts, upgrade retire output, doctor output; lines 1-21, 380-470, 724-800 plus a grep of the rest).
- Re-verified in code during consolidation: file counts (`src/superclaude/agents` 46 `.md` incl. README → 45 agents; `commands` 46 incl. README → 45; 38 skill folders; 11 core files; 12 files in `hooks/scripts` + `scripts/session-init.sh` = 13 installed hooks); `--no-mcp` declarations (`troubleshoot.md:8,58`, `reflect.md:103`); `runner.py:474-477,597` (plan route); `models.py:53-109,290-328` (`DEFAULTS_FILE`, `AIDEV_AI_DEFAULTS_PATH`, `CCSESSION_MODELS_URL`); `mcp-installation.md:60-99` (line 71 wording, no litellm row); `changelog_maintenance.md` `.claude/changelogs` lines and the `## [Unreleased]` guidance (`CHANGELOG.md:5` has the header); `src/superclaude/core/HOW-WE-WORK.md:3` and its byte-identical plugin mirror; no test pins line 3; `superclaude update` mentions across docs and primitives; `SuperClaude-Org` hits (exactly six in `docs/`); `git stash` and `rm -rf ~/.claude` hits; `install -f`, `--custom-prompt-dir`, `python3 -m SuperClaude` hits; swarm "7 lenses"/M5 hits in docs outside A2's slice; issue #352 exists and is open; `post-release.md` was added 2026-07-06 and `impact.md`/`graph.md` on 2026-10-31.
- Every gap row cites the doc line from a scan plus code evidence; worklist items carry the same evidence so a writer need not re-scan.

Conflicts resolved:

1. `--no-mcp`: scan/A2 (mcp-servers rows) said no command defines it; scan/B said `reflect.md` and `troubleshoot.md` do. Code: `troubleshoot.md:8,58,161`, `reflect.md:103,134` → **scan/B is right**. A-W10 and B-W4 say `--no-mcp` exists only on those two; `--all-mcp` exists nowhere.
2. `superclaude reflect run --fix` route: scan/A1 left `commands.md:1343` UNVERIFIED; scan/A2 cited the plan route. Code `runner.py:474-477,597` → plan route `/sc:implement` by default, `/task` only with `--depth deep` (**A2 right**).
3. Counts: scan/DE2 said 46 agents, 37 skill folders, 12 core files; scan/B said 39 skill dirs; scan/A1 said 45 agents. Code and the e2e install → **45 agents, 38 skill folders, 11 core files** (transcript 383-389). Worklist uses these.
4. Swarm operator docs: scan/B called `operator-runbook.md` and `monitoring-patterns.md` current for 5.0.0; grep shows `operator-runbook.md:118` "(requires the M5 contract)" and `monitoring-patterns.md:7-9` "pending M5", which contradict the 5.0.0-window reduce path (`swarm/commands.py:2083-2169`, scan/A2 live run). Resolved as stale (gap 65); `done.json` still absent on a fresh run, so the "prefer state file" advice stays.
5. LiteLLM classification: scan/DE1 sysop-only vs scan/DE2 ordinary with sysop dependency. No gate in `install_mcp.py:107-115,1406-1410` → **ordinary** (D02); the gateway host and key issuance are outside the repo.
6. `ic`: scan/DE1 "sysop / power-user" → ordinary (no gate; `~/.aienv` is a user file) (D16).
7. `/sc:post-release` new in 5.0.0 (scan/DE2 UNVERIFIED): added 2026-07-06, inside the 5.0.0 window (after 2026-06-04), absent from the changelog → recorded as "in window, not in changelog".
8. Help/recommend "run `superclaude update`" when the routing guide is missing (`help.md:77,81`; `sc-recommend/SKILL.md:48`): checked and **not a gap** — `update` does copy `HOW-WE-WORK.md`; the instruction restores a file, it is not an upgrade path. Same for `skills/ccsession-tag/README.md:57` and `mcp-installation.md:70` (accurate).

No unresolved `CONFLICT:` remains.

Limits and UNVERIFIED items carried forward:

- Not scanned by any scanner: `src/superclaude/skills/ccsession-tag/README.md`, `MODEL-TIERS.md` (gap 83), `docs/designs/`, `docs/agents/`, `docs/analysis-sc-tasklist.md`, `docs/Templates/`. `docs/memory/pm_context.md:77` mentions Serena as historical context only (left alone).
- UNVERIFIED and marked where used: `file://` support in ccsession `_fetch` (E02); `/sc:pr-submit --yes` rejection wording (D07); tmux flag dropping at runtime (O9); roadmap `max_runs=3` intent (O10); AIRIS "60+ tools"; auggie `implement` tool; `claude` CLI never writing the real `~/.claude.json` under a fake `HOME` (O22).
- Line numbers are from the scans and greps at `d953b983`; writers must match on text.
- Only this file was written; no other repo file was modified.

