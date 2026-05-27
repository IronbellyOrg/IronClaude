# Research: Patterns & Conventions + Template & Examples

Status: Complete

## Scope

Research topic: command/skill source patterns for adding `/sc:init-lite --context-optimized` as a thin dispatcher whose protocol details live in a lazily loaded skill.

Evidence tags: `[CODE-VERIFIED]` means the claim is verified against repository files cited on the same bullet; `[TASK-DECISION]` means a design/task choice derived from the critiqued feature design rather than pre-existing code.

Inspected source files within the requested scope:

- `/config/workspace/IronClaude/src/superclaude/commands/recommend.md`
- `/config/workspace/IronClaude/src/superclaude/commands/pm.md`
- `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md`
- `/config/workspace/IronClaude/src/superclaude/commands/cleanup-audit.md`
- `/config/workspace/IronClaude/src/superclaude/commands/cli-portify.md`
- `/config/workspace/IronClaude/src/superclaude/commands/roadmap.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-recommend-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-pm-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/cli/install_skills.py`
- `/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`
- `/config/workspace/IronClaude/src/superclaude/core/CLAUDE.md`

## Findings: source-of-truth locations and sync discipline

- [CODE-VERIFIED] Source of truth for distributable commands and skills is `src/superclaude/`: commands live under `src/superclaude/commands/`, skills under `src/superclaude/skills/`, and `.claude/` contains dev convenience copies synced from `src/` (`/config/workspace/IronClaude/src/superclaude/core/CLAUDE.md:17-28`).
- [CODE-VERIFIED] Required workflow after component edits is `make sync-dev` followed by `make verify-sync`; edits should start in `src/superclaude/`, not `.claude/` (`/config/workspace/IronClaude/src/superclaude/core/CLAUDE.md:32-48`, `/config/workspace/IronClaude/src/superclaude/core/CLAUDE.md:83-87`).
- [CODE-VERIFIED] Installed commands target `~/.claude/commands/sc/`; installed skills target `~/.claude/skills/`; dev convenience copies mirror under `.claude/commands/sc/`, `.claude/skills/`, and `.claude/agents/` (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:76-93`).

## Findings: command/skill split and startup context control

- [CODE-VERIFIED] The documented architecture is exactly the pattern requested: commands are a "thin dispatch layer" that invoke skills via an Activation section; skills hold behavioral protocol plus optional refs; agents are separate specialist executors (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:40-48`).
- [CODE-VERIFIED] Command files should own flags, usage, examples, boundaries, and Activation handoff; they should contain zero protocol logic. The developer guide explicitly states that command `/sc:adversarial` defines the interface and hands off to a skill containing the detailed protocol (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:50-58`).
- [CODE-VERIFIED] The mandatory Activation handoff pattern is documented as:
  - `## Activation`
  - `**MANDATORY**: Before executing any protocol steps, invoke:`
  - `> Skill <skill-name>`
  - `Do NOT proceed with protocol execution using only this command file.`
  - `The full behavioral specification is in the protocol skill.`
  (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:60-74`).
- [CODE-VERIFIED] Startup-context optimization is supported by the documented context loading sequence: commands load only when explicitly typed, while skills load only name and description at session start and full content on invocation (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:95-105`).
- [CODE-VERIFIED] The repo-level core context repeats the same token-efficiency convention: skills in `~/.claude/skills/` load on-demand at approximately 50 tokens each at session start, and full behavioral specs live in skill files (`/config/workspace/IronClaude/src/superclaude/core/CLAUDE.md:97-102`).
- [TASK-DECISION] Therefore `/sc:init-lite --context-optimized` should be a short `src/superclaude/commands/init-lite.md` dispatcher and should not embed the init-lite algorithm, report schema, template prose, or examples beyond concise interface examples.

## Findings: command markdown conventions to mirror

- [CODE-VERIFIED] Developer guide says every command file has YAML frontmatter plus a Markdown body (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:242-247`). Required command frontmatter fields are `name`, `description`, `category`, `complexity`, `mcp-servers`, and `personas`; optional field shown is `version` (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:248-268`).
- [CODE-VERIFIED] Standard command body sections are title, Required Input or Triggers, Usage, Options or Arguments if flags exist, Behavioral Flow, MCP Integration if used, Tool Coordination, Examples, Boundaries, and Related Commands (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:270-283`).
- [CODE-VERIFIED] Existing thin dispatcher examples include frontmatter and an Activation section pointing to a protocol skill:
  - `/config/workspace/IronClaude/src/superclaude/commands/recommend.md:1-5` defines `name`, `description`, `category`; `/config/workspace/IronClaude/src/superclaude/commands/recommend.md:40-46` invokes `Skill sc:recommend-protocol` and forbids executing from the command file alone.
  - `/config/workspace/IronClaude/src/superclaude/commands/pm.md:1-8` defines command metadata including `complexity`, `mcp-servers`, and `personas`; `/config/workspace/IronClaude/src/superclaude/commands/pm.md:49-55` invokes `Skill sc:pm-protocol`.
  - `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md:1-10` includes `allowed-tools`, `mcp-servers`, `personas`, and `version`; `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md:70-84` invokes `Skill sc:tasklist-protocol`, passes explicit context, and forbids generation from the command alone.
  - `/config/workspace/IronClaude/src/superclaude/commands/cli-portify.md:76-90` shows the command passing resolved context fields into `Skill sc:cli-portify-protocol` and forbidding execution from only the command file.
- [TASK-DECISION] Recommended command frontmatter for `/sc:init-lite --context-optimized` should follow the guide and majority examples with `name: init-lite` rather than embedding the `sc:` prefix. Evidence: guide maps `name: <command-name>` to `/sc:<name>` (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:248-261`), while `pm.md`, `tasklist.md`, `cleanup-audit.md`, and `cli-portify.md` use bare command names in frontmatter (`/config/workspace/IronClaude/src/superclaude/commands/pm.md:1-8`, `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md:1-10`, `/config/workspace/IronClaude/src/superclaude/commands/cleanup-audit.md:1-9`, `/config/workspace/IronClaude/src/superclaude/commands/cli-portify.md:1-10`).
- [CODE-VERIFIED] There are inconsistent older/example commands where `recommend.md` uses `name: sc:recommend` and `roadmap.md` uses `name: sc:roadmap` (`/config/workspace/IronClaude/src/superclaude/commands/recommend.md:1-5`, `/config/workspace/IronClaude/src/superclaude/commands/roadmap.md:1-5`), so task acceptance should not depend on changing unrelated conventions, but new command work should use the documented bare-name pattern unless the cli-registration researcher finds a stricter installer requirement.

## Findings: skill markdown conventions to mirror

- [CODE-VERIFIED] Developer guide says minimum skill frontmatter is `name`, `description`, and `allowed-tools`; the complex field set additionally includes `category`, `complexity`, `mcp-servers`, `personas`, and `argument-hint` (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:500-539`).
- [CODE-VERIFIED] `allowed-tools` is the primary skill safety boundary; read-only/report skills should omit `Edit`, and safety-critical Bash can be constrained to command families (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:555-570`).
- [CODE-VERIFIED] Existing protocol skills use protocol-specific names and descriptions:
  - `sc:recommend-protocol` declares `allowed-tools: Read, Glob, Grep, Bash, TodoWrite, mcp__auggie-mcp__codebase-retrieval` (`/config/workspace/IronClaude/src/superclaude/skills/sc-recommend-protocol/SKILL.md:1-5`).
  - `sc:pm-protocol` declares `allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill` (`/config/workspace/IronClaude/src/superclaude/skills/sc-pm-protocol/SKILL.md:1-5`).
  - `sc:cleanup-audit-protocol` includes the full complex metadata set and scoped Bash families (`/config/workspace/IronClaude/src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:1-10`).
  - `sc-cli-portify-protocol` includes `category`, `complexity`, `allowed-tools`, `mcp-servers`, `personas`, and `argument-hint` (`/config/workspace/IronClaude/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:1-10`).
  - `sc:roadmap-protocol` uses frontmatter `name: sc:roadmap-protocol`, `description`, `allowed-tools`, and `argument-hint` (`/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:1-6`).
- [CODE-VERIFIED] Existing protocol skills state they are invoked only by their command and not directly by users. Examples: `sc:recommend-protocol` says it is invoked only by `sc:recommend` and never directly by users (`/config/workspace/IronClaude/src/superclaude/skills/sc-recommend-protocol/SKILL.md:9-18`); `sc:pm-protocol` says the same for `sc:pm` (`/config/workspace/IronClaude/src/superclaude/skills/sc-pm-protocol/SKILL.md:9-19`); `sc:roadmap-protocol` says the same for `sc:roadmap` (`/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:19-28`).
- [TASK-DECISION] For init-lite, the skill should therefore begin with a concise protocol-only `SKILL.md` that says it is invoked only by `/sc:init-lite`, accepts pass-through flags including `--context-optimized`, and must not be invoked directly by users.
- [TASK-DECISION] Candidate `allowed-tools` for `sc-init-lite-protocol` should be minimal and evidence-based. If the protocol only reads project state and writes a report/scaffold, use `Read, Glob, Grep, Write, Bash` plus any exact Bash family restrictions identified by the report/scaffold researcher. Do not include `Edit` unless the feature modifies existing files; developer guide says omitting `Edit` prevents file modification for report/audit-style skills (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:555-570`).

## Findings: refs/ lazy-loading pattern

- [CODE-VERIFIED] The developer guide defines `refs/` as detailed reference material loaded on demand per wave, not pre-loaded at session start, specifically for token efficiency (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:642-645`).
- [CODE-VERIFIED] Design rules: keep `SKILL.md` to behavioral intent and approximately 400-500 lines, put algorithms/formulas/prompts/templates in `refs/`, keep at most 2-3 refs loaded at once, and explicitly declare when each ref is loaded (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:646-657`).
- [CODE-VERIFIED] Token budget model in docs: skill name+description loads at session start, full `SKILL.md` loads on invocation, and each ref loads per wave/on demand (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:659-666`).
- [CODE-VERIFIED] Existing refs examples match this: `sc-cli-portify-protocol` loads `refs/analysis-protocol.md` only before Phase 1 (`/config/workspace/IronClaude/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:71-74`); the roadmap templates ref says it is for Wave 2 and Wave 3 and contains template discovery, milestone planning, effort estimation, body templates, and YAML frontmatter schemas (`/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/refs/templates.md:1-5`).
- [TASK-DECISION] For init-lite, put the large template/report schema/examples under one or more refs, for example `src/superclaude/skills/sc-init-lite-protocol/refs/report-template.md` and/or `src/superclaude/skills/sc-init-lite-protocol/refs/scaffold-rules.md`, and have `SKILL.md` explicitly say when to `Read` each ref. Do not place these in the command file.

## Findings: install behavior for `sc-*` and `sc-*-protocol` skills

- [CODE-VERIFIED] `install_skills.py` documents that skills whose directory name starts with `sc-` and have a corresponding slash command are served via `/sc:<name>` commands and are not installed as separate skills to avoid duplicate autocomplete entries (`/config/workspace/IronClaude/src/superclaude/cli/install_skills.py:1-11`).
- [CODE-VERIFIED] The actual check strips only the `sc-` prefix from the skill directory name and looks for `src/superclaude/commands/<stripped-name>.md` (`/config/workspace/IronClaude/src/superclaude/cli/install_skills.py:19-30`).
- [CODE-VERIFIED] During batch install, skills satisfying that check are skipped, a stale installed copy is removed, and the message reports `skill → /sc:<cmd_name>` (`/config/workspace/IronClaude/src/superclaude/cli/install_skills.py:58-68`, `/config/workspace/IronClaude/src/superclaude/cli/install_skills.py:94-100`).
- [CODE-VERIFIED] Consequence for the proposed name `src/superclaude/skills/sc-init-lite-protocol/`: the installer would strip `sc-` to `init-lite-protocol` and look for `/config/workspace/IronClaude/src/superclaude/commands/init-lite-protocol.md`, not `/config/workspace/IronClaude/src/superclaude/commands/init-lite.md` (`/config/workspace/IronClaude/src/superclaude/cli/install_skills.py:25-30`). With only `commands/init-lite.md`, this protocol skill would be installed as a standalone skill.
- [CODE-VERIFIED] This is not hypothetical drift: current protocol skills are named with `-protocol` directories (for example `src/superclaude/skills/sc-recommend-protocol/SKILL.md`) while their commands are named without `-protocol` (for example `src/superclaude/commands/recommend.md`), and those skill frontmatters explicitly say not to invoke them directly (`/config/workspace/IronClaude/src/superclaude/skills/sc-recommend-protocol/SKILL.md:9-18`, `/config/workspace/IronClaude/src/superclaude/commands/recommend.md:40-46`).
- [TASK-DECISION] Task design decision needed: if the acceptance criterion is "not installed as standalone," either name the backing skill directory `src/superclaude/skills/sc-init-lite/` so `_has_corresponding_command` maps it to `commands/init-lite.md`, or change `install_skills.py` to treat `sc-<command>-protocol` as corresponding to `commands/<command>.md`. If keeping the user-provided `sc-init-lite-protocol` name, the task should explicitly include the installer change and tests from the cli-registration researcher.

## Exact files likely needed for this track

- [TASK-DECISION] Add thin dispatcher command: `/config/workspace/IronClaude/src/superclaude/commands/init-lite.md`.
- [TASK-DECISION] Add protocol skill: `/config/workspace/IronClaude/src/superclaude/skills/sc-init-lite-protocol/SKILL.md` if keeping the requested `sc-init-lite-protocol` naming, or `/config/workspace/IronClaude/src/superclaude/skills/sc-init-lite/SKILL.md` if intentionally using existing standalone-skip semantics.
- [TASK-DECISION] Add lazy refs only if the protocol needs substantial templates/examples: `/config/workspace/IronClaude/src/superclaude/skills/sc-init-lite-protocol/refs/<name>.md` (or corresponding `sc-init-lite/refs/<name>.md` if using the alternate skill directory name).
- [CODE-VERIFIED] Do not add or edit `.claude/` source copies directly; after source edits, run `make sync-dev` and `make verify-sync` per source-of-truth workflow (`/config/workspace/IronClaude/src/superclaude/core/CLAUDE.md:32-48`, `/config/workspace/IronClaude/src/superclaude/core/CLAUDE.md:83-87`).

## Suggested command skeleton constraints for task file

- [TASK-DECISION] `src/superclaude/commands/init-lite.md` should include concise frontmatter with at least `name: init-lite`, a one-line `description`, `category`, `complexity`, `mcp-servers`, and `personas` per command guide (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:248-261`).
- [TASK-DECISION] The command body should include Triggers/Required Input, Usage showing `/sc:init-lite --context-optimized`, an Arguments/Flags table, Behavioral Summary only, Activation, Examples, and Boundaries per standard command sections (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:270-283`).
- [TASK-DECISION] The Activation section should invoke `Skill sc:init-lite-protocol` or the exact final skill name and should explicitly pass user-provided arguments/flags through if the implementation needs them. `roadmap.md` demonstrates pass-through arguments to the Skill invocation (`/config/workspace/IronClaude/src/superclaude/commands/roadmap.md:71-79`), and `tasklist.md`/`cli-portify.md` demonstrate passing resolved context fields (`/config/workspace/IronClaude/src/superclaude/commands/tasklist.md:70-84`, `/config/workspace/IronClaude/src/superclaude/commands/cli-portify.md:76-90`).
- [TASK-DECISION] The command must explicitly forbid executing init-lite protocol steps using only the command file, mirroring recommend/pm/tasklist (`/config/workspace/IronClaude/src/superclaude/commands/recommend.md:40-46`, `/config/workspace/IronClaude/src/superclaude/commands/pm.md:49-55`, `/config/workspace/IronClaude/src/superclaude/commands/tasklist.md:70-84`).

## Suggested skill skeleton constraints for task file

- [TASK-DECISION] `SKILL.md` should include protocol frontmatter with `name`, `description`, and `allowed-tools` minimum; include `argument-hint: "[--context-optimized] ..."` if helpful for invocation ergonomics, following the skill guide and existing roadmap/cli-portify protocol skills (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:500-539`, `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:1-6`, `/config/workspace/IronClaude/src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:1-10`).
- [TASK-DECISION] The first body section should say the protocol is invoked only by `/sc:init-lite` and is never invoked directly by users, matching recommend/pm/roadmap protocol skills (`/config/workspace/IronClaude/src/superclaude/skills/sc-recommend-protocol/SKILL.md:9-18`, `/config/workspace/IronClaude/src/superclaude/skills/sc-pm-protocol/SKILL.md:9-19`, `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:19-28`).
- [TASK-DECISION] Keep `SKILL.md` focused on behavioral flow, tool coordination, outputs, and gating. Put bulky report templates, scaffold examples, and detailed checklists into `refs/` and load them only at the exact phase where they are needed (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:642-657`).
- [TASK-DECISION] If init-lite is report/scaffold oriented and should be safe by default, omit `Edit` unless another researcher proves existing-file modification is required; docs identify `allowed-tools` as the primary safety boundary and recommend omitting `Edit` for report-only skills (`/config/workspace/IronClaude/docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:555-570`).

## Summary

- [TASK-DECISION] The source-of-truth implementation should add `src/superclaude/commands/init-lite.md` plus a backing protocol skill under `src/superclaude/skills/`, then sync dev copies with `make sync-dev` and verify with `make verify-sync`.
- [TASK-DECISION] `/sc:init-lite --context-optimized` should be a thin command dispatcher: interface, flags, concise examples, boundaries, and mandatory Activation only. Protocol, templates, examples, and detailed report/scaffold rules belong in the skill and lazy `refs/`.
- [CODE-VERIFIED] If the skill directory is named `sc-init-lite-protocol`, current `install_skills.py` will install it as a standalone skill because the skip logic maps only `sc-<name>` to `commands/<name>.md`; avoiding standalone install requires either using `sc-init-lite/` or changing installer logic to map `sc-<name>-protocol` to `commands/<name>.md`.
- [TASK-DECISION] Recommended task acceptance should require evidence-backed frontmatter and Activation patterns, minimal `allowed-tools`, no `.claude/` direct edits, and explicit lazy ref loading for any bulky templates/checklists.
