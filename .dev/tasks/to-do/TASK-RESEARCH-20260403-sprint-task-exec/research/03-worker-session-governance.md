# 03 — Worker Session Governance

**Status**: Complete
**Date**: 2026-04-03
**Investigator**: Architecture Analyst
**Research Question**: What behavioral governance does a `claude --print -p` subprocess inherit automatically?

---

## 1. The CLI Command Built by ClaudeProcess

**File**: `src/superclaude/cli/pipeline/process.py`, lines 71-91

The base `ClaudeProcess.build_command()` constructs:

```
claude --print --verbose --dangerously-skip-permissions --no-session-persistence \
       --tools default --max-turns <N> --output-format <format> -p <prompt>
```

Key flags and their governance implications:

| Flag | Effect on Governance |
|------|---------------------|
| `--print` | Non-interactive mode. **Does NOT skip CLAUDE.md loading.** The `--print` help says "The workspace trust dialog is skipped" but nothing about skipping config loading. |
| `--no-session-persistence` | Sessions are not saved to disk and cannot be resumed. **No effect on skill loading or CLAUDE.md.** This is purely about persistence, not about what gets loaded into the session. |
| `--tools default` | Enables ALL built-in tools (Bash, Edit, Read, Write, Glob, Grep, etc.). This is the full toolset, not a restricted subset. |
| `--verbose` | Override verbose mode setting from config. |
| `--dangerously-skip-permissions` | Bypass all permission checks. No tool approval prompts. |

**Critical absence**: The `--bare` flag is NOT used. The `--bare` flag would "skip hooks, LSP, plugin sync, attribution, auto-memory, background prefetches, keychain reads, and CLAUDE.md auto-discovery." Without `--bare`, ALL of these features are active.

**Critical absence**: The `--disable-slash-commands` flag is NOT used. Without it, all installed skills resolve normally.

## 2. What the Worker Process Automatically Loads

### 2.1 CLAUDE.md Files (Auto-Discovered)

Since `--bare` is not passed, Claude Code performs its standard CLAUDE.md auto-discovery:

1. **User-level CLAUDE.md** at `~/.claude/CLAUDE.md` -- Contains the full SuperClaude framework context including Python environment rules, project structure, dev commands, MCP server table, persona table, and 10 core rules (UV only, parallel by default, confidence check, etc.).

2. **Project-level CLAUDE.md** at `<working-dir>/CLAUDE.md` -- Contains the full IronClaude project instructions including architecture (v4.2.0), testing patterns, PM Agent patterns, slash command installation, component sync workflow, and git workflow rules.

**However**: The `CLAUDE_WORK_DIR` env var is set to an isolation directory (e.g., `results/.isolation/phase-1/`), which contains only a copy of the phase file. If Claude Code resolves CLAUDE.md relative to this working directory, it would NOT find the project-level CLAUDE.md. But if it traverses upward or uses the git root, it likely would.

### 2.2 Skills from ~/.claude/skills/

Since `--disable-slash-commands` is not passed, skills are available. The sprint prompt starts with:

```
/sc:task-unified Execute all tasks in @<phase-file> --compliance strict --strategy systematic
```

This is a skill invocation (`sc:task-unified`). For this to work, the worker must resolve `sc:task-unified` to the `sc-task-unified-protocol` skill in `~/.claude/skills/`. The `--bare` help text confirms: "Skills still resolve via /skill-name" even in bare mode. In normal (non-bare) mode, they definitely load.

The user-level `~/.claude/skills/` contains 15 skill packages including `sc-task-unified-protocol`, which is a substantial behavioral protocol defining compliance tiers, verification workflows, and execution strategies.

### 2.3 Commands from ~/.claude/commands/sc/

The `~/.claude/commands/sc/` directory contains 30+ slash command definitions. These are available to the worker since `--disable-slash-commands` is not passed. However, commands typically need to be explicitly invoked; they are not injected into the system prompt.

### 2.4 Agents from ~/.claude/agents/

The `~/.claude/agents/` directory contains agent definitions (audit-analyzer, backend-architect, debate-orchestrator, etc.). These would be available if the skill protocol requests agent delegation.

### 2.5 User Settings from ~/.claude/settings.json

The user-level settings include:

```json
{
  "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" },
  "model": "opus[1m]",
  "alwaysThinkingEnabled": true,
  "effortLevel": "medium",
  "skipDangerousModePermissionPrompt": true,
  "teammateMode": "auto"
}
```

These are loaded unless `CLAUDE_SETTINGS_DIR` is overridden to point elsewhere. **Finding**: The sprint executor does NOT pass `CLAUDE_SETTINGS_DIR` in the env_vars.

### 2.6 Project Settings from .claude/settings.json

The project-level `.claude/settings.json` is empty (`{}`). No hooks, no allowlists, no MCP server configs at this level.

## 3. The 4-Layer Isolation Gap

**File**: `src/superclaude/cli/sprint/executor.py`, lines 108-184

An `IsolationLayers` dataclass and `setup_isolation()` function are defined but **never called** in the main sprint runner loop. The isolation layers would set:

1. `CLAUDE_WORK_DIR` -- Restrict working directory (this IS applied, line 1252)
2. `GIT_CEILING_DIRECTORIES` -- Prevent git traversal above release dir (NOT applied)
3. `CLAUDE_PLUGIN_DIR` -- Point to empty tempdir (NOT applied)
4. `CLAUDE_SETTINGS_DIR` -- Isolated settings dir (NOT applied)

**Actual isolation at runtime** (line 1250-1253): Only `CLAUDE_WORK_DIR` is set. The other 3 layers are dead code.

## 4. Environment Variable Manipulation

**File**: `src/superclaude/cli/pipeline/process.py`, lines 93-108

The `build_env()` method:
- Copies `os.environ` (inheriting all parent env vars)
- Removes `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` (prevents nested session detection)
- Merges any caller-provided `env_vars`

This means the worker inherits:
- `HOME` (can find `~/.claude/`)
- `PATH` (can find `claude` binary and other tools)
- All MCP server environment variables
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` (from user settings)
- Any other env vars from the parent process

## 5. Governance the Worker Actually Receives

### Explicitly via Prompt
- The `/sc:task-unified` invocation with `--compliance strict --strategy systematic`
- Sprint context (phase number, artifact paths, prior phase dirs)
- Execution rules (task ordering, tier-specific behavior, scope boundary)
- Result file instructions

### Implicitly via Claude Code Auto-Loading
- **User CLAUDE.md** (`~/.claude/CLAUDE.md`): Full SuperClaude framework rules including UV-only, parallel-first, confidence checks, output path rules
- **Project CLAUDE.md** (if discoverable from working dir): Full IronClaude project rules
- **User settings.json**: Model preferences, effort level, thinking mode, agent teams flag
- **All installed skills**: 15 skill packages available for invocation
- **All installed commands**: 30+ slash commands available
- **All installed agents**: Available for delegation
- **MCP servers**: Any configured MCP servers (from user settings or project config)

### Governance NOT Received (due to missing isolation)
- No `CLAUDE_SETTINGS_DIR` override means user settings bleed through
- No `CLAUDE_PLUGIN_DIR` override means plugins (if any) load
- No `GIT_CEILING_DIRECTORIES` means git operations can traverse above the isolation dir
- No `--bare` flag means full auto-discovery is active

## 6. The Prompt's `/sc:task-unified` Invocation

The prompt begins with `/sc:task-unified`, which is a skill trigger. When Claude Code processes this:

1. It matches against installed skills in `~/.claude/skills/`
2. It loads `sc-task-unified-protocol/SKILL.md` (a substantial document defining tier classification, compliance verification, and execution strategy)
3. The skill itself references additional rules from `src/superclaude/core/RULES.md` and `PRINCIPLES.md`
4. The skill may delegate to agents defined in `~/.claude/agents/`

This means the "minimal prompt" sent by the sprint executor actually triggers loading of an extensive behavioral protocol that governs how the worker executes tasks.

## 7. Contrast: What `--bare` Mode Would Do

If the sprint executor added `--bare` to the command:
- CLAUDE.md auto-discovery would be skipped
- Hooks would be skipped
- Plugin sync would be skipped
- Auto-memory would be skipped
- **Skills would still resolve** (per `--bare` documentation)

So even `--bare` would not fully strip governance if the prompt contains `/sc:task-unified`.

---

## Gaps and Questions

1. **Dead isolation code**: `setup_isolation()` and `IsolationLayers` exist (lines 108-184) but are never called. Was this intentional or an incomplete implementation? Only 1 of 4 isolation layers is actually applied.

2. **CLAUDE.md discovery with CLAUDE_WORK_DIR**: When `CLAUDE_WORK_DIR` points to an isolation directory (e.g., `results/.isolation/phase-1/`), does Claude Code search for CLAUDE.md only in that directory, or does it traverse upward? If it traverses, the project CLAUDE.md may still be found. If it doesn't, only the user-level CLAUDE.md applies.

3. **MCP server loading**: Are MCP servers configured in `~/.claude/settings.json` or project-level configs loaded in `--print` mode? The base `settings.json` is empty, but the user-level settings have env vars suggesting MCP features. If MCP servers load, the worker has access to web search, sequential thinking, codebase retrieval, etc.

4. **Skill loading token cost**: Each skill in `~/.claude/skills/` is described as "~50 tokens each at session start" (per CLAUDE.md). With 15+ skills, that's 750+ tokens of overhead per worker subprocess. However, the full `sc-task-unified-protocol` SKILL.md is substantially larger when actually invoked.

5. **Model override**: The user settings specify `"model": "opus[1m]"` but the sprint executor passes `--model` explicitly via config. The CLI flag should take precedence, but this is a potential conflict point.

6. **Agent teams**: The env var `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set in user settings. This may enable multi-agent delegation features within worker subprocesses, adding another layer of implicit governance.

---

## Summary

**The worker subprocess inherits extensive governance** even without the sprint executor explicitly providing it. The governance comes from three layers:

1. **Claude Code auto-loading** (since `--bare` is not used): Both user-level and project-level CLAUDE.md files are auto-discovered and injected into the system prompt. User settings (model, effort, thinking mode) apply. All installed skills, commands, and agents are available.

2. **The prompt's skill invocation**: The `/sc:task-unified` prefix triggers loading of a comprehensive behavioral protocol that defines compliance tiers, verification workflows, and execution strategies. This is not a "minimal prompt" -- it is a gateway to a full execution framework.

3. **Environment inheritance**: The subprocess inherits the full parent environment (minus `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT`), including all MCP-related env vars.

**The architect's reference to an "extensive system" is correct.** A headless `claude --print -p` subprocess in this codebase is not a bare LLM call. It operates under the full SuperClaude governance framework: CLAUDE.md rules, skill protocols, available agents, user settings, and the complete built-in toolset. The only thing "headless" about it is the lack of interactive TUI -- the behavioral governance layer is fully intact.

**The 4-layer isolation system is partially implemented**: Only `CLAUDE_WORK_DIR` is applied; `CLAUDE_SETTINGS_DIR`, `CLAUDE_PLUGIN_DIR`, and `GIT_CEILING_DIRECTORIES` are defined but never wired into the execution path. This means worker subprocesses have less isolation than the code architecture intended.
