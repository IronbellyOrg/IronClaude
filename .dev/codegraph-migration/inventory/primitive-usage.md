# W6: semantic usage map of codebase-memory and Serena inside primitives

Task `task_275bd0799127` (planning run for issue #323). Read-only. Repo HEAD 55d40308 on branch `ironbelly/feat-codememory-codegraph-init`, observed 2026-10-29.

How this file was built: every row below was classified by hand from the live files; the quoted line in each row, the row-to-hit coverage and all counts were produced by a throwaway script that read the files and ran the `rg` commands in section 2 (the script lives outside the repo and is not a deliverable). The script refused to write this file until every in-scope hit line was covered by a row (0 uncovered). In quotes a backtick is shown as `'` and a pipe as `\|`; long lines are cut with `...`. Paths are repo-relative; `S/` below means `src/superclaude/`, `P/` means `plugins/superclaude/`.

## 1. Summary

- **codebase-memory has zero references inside primitives.** The strict search (section 2, C4) finds 0 hit lines in `skills commands agents core hooks templates mcp modes rules output-styles` and `plugins/superclaude`, and 0 in the installed `~/.claude` primitives and docs. The only hits of a looser pattern are Auggie's `mcp__auggie-mcp__codebase-retrieval` (false positive, C5). The installed `~/.claude` has no skill, agent, hook or command added by the upstream codebase-memory installer (C10, C10b). Codebase-memory therefore only exists in the installer code and docs (W1's inventory), not in primitives. Phase 1 and Phase 3 primitive work is Serena-only.
- **Serena: 251 rows in 73 primitive files under `src/superclaude` (469 hit lines of the broader pattern: the word Serena plus bare Serena tool names) plus 19 mirror rows in `plugins/superclaude` (129 hit lines).** The plain word `serena` alone gives 361 hit lines in 83 files across those trees (C1). 86 rows are load-bearing, 165 are decorative (rules in section 3).
- **Serena is invisible to a name-only search in several places** (section 2, C3: bare tool names on lines without the word `serena`). The worst cases: `S/modes/MODE_Task_Management.md` (a whole mode built on `write_memory`/`think_about_*`, never says Serena), `S/agents/pm-agent.md` and `S/skills/sc-pm-protocol/SKILL.md` (PM memory protocol), `S/skills/sc-task-protocol/SKILL.md:88`, `S/hooks/scripts/freshness-pre-edit.sh:25` (reads Serena's `relative_path` argument). Phase 1 must search tool names, not only the word.
- **Three leaks into user-facing output:** `S/skills/sc-tasklist-protocol/SKILL.md:683` makes generated tasklists say STRICT tasks require Serena; `S/skills/sc-task-protocol/SKILL.md:287` says STRICT execution has no fallback without Serena; `S/core/CLAUDE.md:21` installs a `--serena` row into every user's global `~/.claude/CLAUDE.md` (the only place the `--serena` flag appears inside primitives; `rg -n -e '--serena' src tests docs README.md CLAUDE.md` also finds it documented in `docs/user-guide/flags.md:25`, `docs/user-guide/mcp-servers.md:97`, `docs/mcp/mcp-integration-policy.md:348` and `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:909`, which are W2's; no code in `src/` or `tests/` parses the flag).
- **`mcp-servers:` frontmatter looks decorative:** 21 of the 29 src allowlist lines are `mcp-servers: [...]` and `rg -n 'mcp-servers' src/superclaude --glob '*.py'` finds 0 Python consumers (C13). Whether Claude Code itself reads that field is UNVERIFIED. The `tools:` / `allowed-tools:` lines are different: Claude Code enforces them. Of the 8 src `tools:`/`allowed-tools:` lines, four are load-bearing (the validate-roadmap command and skill, the troubleshoot skill, the reflect skill) and one more (`agents/troubleshoot-analyst.md:5`) is pinned exactly by a test (section 6).
- **Heaviest consumer: the reflect skill** (`S/skills/sc-reflect-protocol/`, 186 hit lines across SKILL.md and 10 refs files): activation, config probe, symbol chain, verification triangle, memory I/O and a CLI-parsed output contract. It is the one place where Phase 3 needs a real design; everything else is small.
- **Memory is the largest load-bearing job** (PM agent and protocol, `/sc:save`, `/sc:load`, sc-roadmap save points and resume, validate-roadmap ledgers, reflect memory I/O, MODE_Task_Management). It is not a code-graph job.
- **Plugin mirror** `plugins/superclaude/` is tracked (120 files) and only partly in sync with `src/` (section 5.7 notes IDENTICAL vs DIFFERS per file). It must be edited in Phase 1 like `src/`; `tests/commands/test_routing_plugin_parity.py` requires the plugin's `sc-recommend/refs/HOW-WE-WORK.md` to be a byte copy of `S/core/HOW-WE-WORK.md`.

## 2. Search commands and hit counts

All commands were run from the repo root on 2026-10-29. Output is verbatim.

**C1 Serena word, files**

```bash
rg -i -c serena src/superclaude/skills src/superclaude/commands src/superclaude/agents src/superclaude/core src/superclaude/hooks src/superclaude/templates src/superclaude/mcp plugins/superclaude | wc -l
```

```text
83
```

**C1 Serena word, hit lines**

```bash
rg -i serena src/superclaude/skills src/superclaude/commands src/superclaude/agents src/superclaude/core src/superclaude/hooks src/superclaude/templates src/superclaude/mcp plugins/superclaude | wc -l
```

```text
361
```

**C1b Serena hit lines per directory**

```bash
for d in src/superclaude/skills src/superclaude/commands src/superclaude/agents src/superclaude/core src/superclaude/hooks src/superclaude/templates src/superclaude/mcp plugins/superclaude; do echo "$d $(rg -i -c serena $d | wc -l) files $(rg -i serena $d | wc -l) lines"; done
```

```text
src/superclaude/skills 31 files 199 lines
src/superclaude/commands 19 files 58 lines
src/superclaude/agents 5 files 13 lines
src/superclaude/core 3 files 7 lines
src/superclaude/hooks 1 files 1 lines
src/superclaude/templates 0 files 0 lines
src/superclaude/mcp 6 files 19 lines
plugins/superclaude 18 files 64 lines
```

**C2 Serena word in the other src/superclaude folders (modes rules output-styles scripts tools pr_submit contracts)**

```bash
rg -i -c serena src/superclaude/modes src/superclaude/rules src/superclaude/output-styles src/superclaude/scripts src/superclaude/tools src/superclaude/pr_submit src/superclaude/contracts
```

```text
src/superclaude/modes/MODE_Orchestration.md:1
```

**C3 Serena tool names on lines WITHOUT the word serena (files)**

```bash
rg -i --pcre2 -c '^(?!.*serena).*(list_memories|read_memory|write_memory|edit_memory|delete_memory|rename_memory|activate_project|think_about_|find_symbol|find_referencing_symbols|get_symbols_overview|find_declaration|find_implementations|type_hierarchy|replace_symbol_body|insert_after_symbol|insert_before_symbol|search_for_pattern|prepare_for_new_conversation|summarize_changes|get_diagnostics_for_file|execute_shell_command|get_current_config)' src/superclaude/skills src/superclaude/commands src/superclaude/agents src/superclaude/core src/superclaude/hooks src/superclaude/templates src/superclaude/mcp src/superclaude/modes src/superclaude/rules src/superclaude/output-styles plugins/superclaude | wc -l
```

```text
23
```

**C3 Serena tool names on lines WITHOUT the word serena (hit lines)**

```bash
rg -i --pcre2 '^(?!.*serena).*(list_memories|read_memory|write_memory|edit_memory|delete_memory|rename_memory|activate_project|think_about_|find_symbol|find_referencing_symbols|get_symbols_overview|find_declaration|find_implementations|type_hierarchy|replace_symbol_body|insert_after_symbol|insert_before_symbol|search_for_pattern|prepare_for_new_conversation|summarize_changes|get_diagnostics_for_file|execute_shell_command|get_current_config)' src/superclaude/skills src/superclaude/commands src/superclaude/agents src/superclaude/core src/superclaude/hooks src/superclaude/templates src/superclaude/mcp src/superclaude/modes src/superclaude/rules src/superclaude/output-styles plugins/superclaude | wc -l
```

```text
218
```

**C4 codebase-memory strict pattern in primitives (hit lines)**

```bash
rg -i 'codebase[-_ ]?memory|codebase-memory-mcp|search_graph|trace_path|get_architecture|query_graph|get_code_snippet|detect_changes|index_repository|ingest_traces|cbm' src/superclaude/skills src/superclaude/commands src/superclaude/agents src/superclaude/core src/superclaude/hooks src/superclaude/templates src/superclaude/mcp plugins/superclaude src/superclaude/modes src/superclaude/rules src/superclaude/output-styles | wc -l
```

```text
0
```

**C4b same, files**

```bash
rg -i -c 'codebase[-_ ]?memory|codebase-memory-mcp|search_graph|trace_path|get_architecture|query_graph|get_code_snippet|detect_changes|index_repository|ingest_traces|cbm' src/superclaude/skills src/superclaude/commands src/superclaude/agents src/superclaude/core src/superclaude/hooks src/superclaude/templates src/superclaude/mcp plugins/superclaude src/superclaude/modes src/superclaude/rules src/superclaude/output-styles | wc -l
```

```text
0
```

**C5 FALSE-POSITIVE check: loose pattern with 'mcp__codebase' (matches Auggie's mcp__auggie-mcp__codebase-retrieval)**

```bash
rg -i -n 'mcp__codebase' src/superclaude/skills src/superclaude/commands src/superclaude/agents | cut -c1-110
```

```text
src/superclaude/commands/validate-roadmap.md:6:allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, 
src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:4:allowed-tools: Read, Glob, Grep, Edit, Write, B
src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:125:| Query codebase (semantic) | `mcp__auggie-mc
src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:255:**Requires**: `mcp__auggie-mcp__codebase-retr
src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:872:**Requires**: `mcp__auggie-mcp__codebase-retr
```

**C6 codebase-memory strict pattern in installed ~/.claude primitives and docs (hit lines)**

```bash
rg -i 'codebase[-_ ]?memory|codebase-memory-mcp|search_graph|trace_path|get_architecture|query_graph|get_code_snippet|detect_changes|index_repository|ingest_traces|cbm' ~/.claude/skills ~/.claude/agents ~/.claude/hooks ~/.claude/commands ~/.claude/rules ~/.claude/templates ~/.claude/output-styles ~/.claude/CLAUDE.md ~/.claude/HOW-WE-WORK.md ~/.claude/RULES.md ~/.claude/PRINCIPLES.md ~/.claude/RESEARCH_CONFIG.md ~/.claude/settings.json 2>/dev/null | wc -l
```

```text
0
```

**C7 codebase-memory strict pattern in the rest of src/superclaude (cli etc., W1 domain), files**

```bash
rg -i -l 'codebase[-_ ]?memory|codebase-memory-mcp|search_graph|trace_path|get_architecture|query_graph|get_code_snippet|detect_changes|index_repository|ingest_traces|cbm' src/superclaude --glob '!skills/**' --glob '!commands/**' --glob '!agents/**' --glob '!core/**' --glob '!hooks/**' --glob '!templates/**' --glob '!mcp/**' --glob '!modes/**'
```

```text
src/superclaude/cli/install_codebase_memory.py
src/superclaude/cli/main.py
src/superclaude/cli/install_mcp.py
```

**C8 Serena in installed ~/.claude by area (hit lines)**

```bash
for d in skills agents commands hooks; do echo "$d $(rg -i serena ~/.claude/$d | wc -l)"; done; echo "CLAUDE.md $(rg -i serena ~/.claude/CLAUDE.md | wc -l)"; echo "settings.json $(rg -i serena ~/.claude/settings.json | wc -l)"; echo "top-level docs $(rg -i serena ~/.claude/HOW-WE-WORK.md ~/.claude/RESEARCH_CONFIG.md ~/.claude/RULES.md ~/.claude/PRINCIPLES.md | wc -l)"
```

```text
skills 199
agents 13
commands 58
hooks 0
CLAUDE.md 2
settings.json 1
top-level docs 5
```

**C9 Serena in the tests tree (files / hit lines)**

```bash
echo "$(rg -i -c serena tests | wc -l) files / $(rg -i serena tests | wc -l) lines"
```

```text
40 files / 75 lines
```

**C10 installed primitives NOT in src/superclaude (possible installer-added companions)**

```bash
for k in skills agents; do echo "== $k"; comm -13 <(ls src/superclaude/$k | sed 's/\.md$//' | sort) <(ls ~/.claude/$k | sed 's/\.md$//' | sort); done
echo "== commands/sc"; comm -13 <(ls src/superclaude/commands | sed 's/\.md$//' | sort) <(ls ~/.claude/commands/sc | sed 's/\.md$//' | sort)
echo "== hooks"; comm -13 <(ls src/superclaude/hooks/scripts | sort) <(ls ~/.claude/hooks | sort)
```

```text
== skills
computer-use
orca-cli
orchestration
== agents
== commands/sc
== hooks
session-init.sh
```

**C10b Serena or graph words in those extra installed items**

```bash
for x in computer-use orca-cli orchestration; do echo "$x serena=$(rg -i -c serena ~/.claude/skills/$x 2>/dev/null | wc -l) cbm=$(rg -i -c 'codebase.?memory|search_graph|trace_path' ~/.claude/skills/$x 2>/dev/null | wc -l)"; done
echo "extra names matching codebase|graph|memory: $(ls ~/.claude/skills ~/.claude/agents ~/.claude/hooks ~/.claude/commands/sc | rg -i 'codebase|graph|cbm|memory' | tr '\n' ' ')"
```

```text
computer-use serena=0 cbm=0
orca-cli serena=0 cbm=0
orchestration serena=0 cbm=0
extra names matching codebase|graph|memory:
```

**C11 settings.json permission/matcher entries naming these servers (~/.claude and repo .claude)**

```bash
rg -n 'mcp__serena|mcp__codebase|codebase-memory|serena' ~/.claude/settings.json .claude/settings.json | cut -c1-210
```

```text
/home/coder/.claude/settings.json:162:        "matcher": "Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol",
```

**C12 other agent homes (~/.codex, ~/.config/opencode) mention codebase-memory**

```bash
rg -i -l 'codebase-memory' ~/.codex ~/.config/opencode 2>/dev/null | wc -l
```

```text
0
```

**C13 mcp-servers frontmatter consumers in python (src/superclaude/**/*.py)**

```bash
rg -n 'mcp-servers' src/superclaude --glob '*.py' | wc -l
```

```text
0
```

**C14 Serena in rest of src/superclaude (cli etc.), files**

```bash
rg -i -c serena src/superclaude/cli src/superclaude/pm_agent src/superclaude/execution src/superclaude/examples
```

```text
src/superclaude/cli/reflect/contract.py:3
src/superclaude/cli/reflect/ensemble.py:1
src/superclaude/cli/reflect/config.py:2
src/superclaude/cli/eval/coverage.py:1
src/superclaude/cli/install_mcp.py:6
src/superclaude/cli/eval/suites/real.yaml:37
src/superclaude/cli/eval/suites/README.md:1
```

Row coverage check: 598 in-scope hit lines matched the generator's pattern (the word serena, the bare Serena tool names of C3, and Serena-specific onboarding terms; plain-English 'onboarding' in unrelated docs is excluded), and 0 of them are outside a row. The pattern is a superset of C1 and C3 limited to the scanned folders (C1 trees plus modes, rules, output-styles).

## 3. Row classification rules

- **Server** is `serena` for every row (codebase-memory has no rows, see section 1).
- **load-bearing (LB):** a numbered step, gate, protocol action, installer-read config, enforced allowlist or contract field that calls or depends on the tool or on state it stored. Removing Serena breaks the step or degrades the workflow. A fail-open step is still load-bearing: the workflow loses that capability and the fallback column says what remains.
- **decorative (DEC):** prose mention, table row that repeats a step documented elsewhere, `mcp-servers:` metadata, example, comparison text, a Serena step that is only one tier of a ladder whose next tier is a native tool named in the same place, or a file that only exists to describe the server.
- **Fallback column:** what the primitive itself names as the alternative (`none` means the text offers no alternative).
- Rows quote the first line of their range. A range row covers all hit lines in the range; counts per job use hit lines assigned to the first row that covers them.

## 4. Grouping by job

Counts are for `src/superclaude` rows. The mirror column counts `plugins/superclaude` mirror rows by the job of their src twin. Hit lines = in-scope lines matching the Serena pattern, assigned to one row.

| Job | Meaning | Rows | LB | DEC | Hit lines | Mirror rows | One-line Phase 3 hint (not a design) |
|---|---|---:|---:|---:|---:|---:|---|
| `SYM` | Symbol lookup / navigation | 41 | 10 | 31 | 63 | 2 | Candidate for a codegraph symbol/search lookup; Read/Grep stays the native floor. (Phase 3 decides; codegraph tool names UNVERIFIED here.) |
| `REF` | Reference tracing (callers, usages) | 8 | 3 | 5 | 8 | 0 | Candidate for a codegraph callers/impact query if W4 confirms one exists; otherwise rg. |
| `DIAG` | Diagnostics, scoped verification, change summary | 6 | 3 | 3 | 12 | 0 | No graph equivalent: keep scoped tests/linters in Bash, drop the Serena-only verification triangle wiring. |
| `MEM` | Memory persistence (cross-session state) | 77 | 40 | 37 | 159 | 9 | Not a code-graph job. Per consumer: native files under the output dir (sc-roadmap already has a `.session-memory.md` fallback) or drop. /sc:save and /sc:load need an explicit Phase 3 decision. |
| `ACT` | Project activation, onboarding, config probe | 18 | 12 | 6 | 43 | 0 | Likely drop (no activation concept expected in codegraph, UNVERIFIED); index freshness moves to install/sync. |
| `NUDGE` | Meta-cognition prompts (think_about_*, summarize_changes in /sc:save) | 15 | 7 | 8 | 24 | 0 | Drop: they are prompts with no code-graph analogue. |
| `EDIT` | Symbol-level edit and edit-freshness gating | 6 | 2 | 4 | 6 | 3 | Native Edit/Write; remove the four mcp__serena__ names from the freshness matcher. |
| `ALLOW` | Tool allowlist / mcp-servers frontmatter | 41 | 4 | 37 | 41 | 2 | Mechanical: strip mcp__serena__* / `serena` entries; add codegraph names only where the body calls them. |
| `CFG` | Server install config and server guide | 3 | 1 | 2 | 11 | 3 | Phase 1 delete (installer, configs, guide); Phase 2 adds codegraph config. |
| `CONTRACT` | Reflect output-contract and telemetry fields that name Serena | 4 | 4 | 0 | 17 | 0 | Coordinate with the reflect CLI owner; fields can collapse into the generic `degraded_components` list. |
| `DOC` | Mention only (routing tables, flags, comparison prose, availability notes) | 32 | 0 | 32 | 85 | 0 | Phase 1 text edit only. |
| **Total** | | **251** | **86** | **165** | **469** | **19** | |

Load-bearing rows by job and primitive (what Phase 3 must give a replacement or an explicit drop):

- `SYM`: `commands/troubleshoot.md` (1), `skills/sc-reflect-protocol/SKILL.md` (6), `skills/sc-troubleshoot-protocol/SKILL.md` (1), `skills/sc-validate-roadmap-protocol/SKILL.md` (2)
- `REF`: `agents/reuse-auditor.md` (1), `skills/sc-reflect-protocol/SKILL.md` (2)
- `DIAG`: `skills/sc-reflect-protocol/SKILL.md` (3)
- `MEM`: `agents/pm-agent.md` (10), `commands/load.md` (2), `commands/pm.md` (2), `commands/save.md` (3), `modes/MODE_Task_Management.md` (6), `skills/sc-crash-recovery/scripts/bootstrap_scan.sh` (1), `skills/sc-pm-protocol/SKILL.md` (6), `skills/sc-reflect-protocol/SKILL.md` (3), `skills/sc-roadmap-protocol/SKILL.md` (3), `skills/sc-task-protocol/SKILL.md` (1), `skills/sc-validate-roadmap-protocol/SKILL.md` (3)
- `ACT`: `commands/load.md` (2), `skills/sc-reflect-protocol/SKILL.md` (5), `skills/sc-task-protocol/SKILL.md` (2), `skills/sc-tasklist-protocol/SKILL.md` (1), `skills/sc-validate-roadmap-protocol/SKILL.md` (2)
- `NUDGE`: `agents/pm-agent.md` (3), `commands/save.md` (1), `modes/MODE_Task_Management.md` (3)
- `EDIT`: `hooks/hooks.json` (1), `hooks/scripts/freshness-pre-edit.sh` (1)
- `ALLOW`: `commands/validate-roadmap.md` (1), `skills/sc-reflect-protocol/SKILL.md` (1), `skills/sc-troubleshoot-protocol/SKILL.md` (1), `skills/sc-validate-roadmap-protocol/SKILL.md` (1)
- `CFG`: `mcp/configs/serena.json` (1)
- `CONTRACT`: `skills/sc-reflect-protocol/SKILL.md` (4)

## 5. Usage rows

Columns: ID, primitive path:line, server, tool or concept named, job (section 4 codes), class (LB load-bearing, DEC decorative), fallback named by the primitive, quoted line (first line of the range).

### 5.1 Agents (25 rows: 14 LB, 11 DEC)

| ID | Primitive:line | Server | Tool or concept | Job | Class | Fallback | Quoted line |
|---|---|---|---|---|---|---|---|
| R001 | `src/superclaude/agents/auggie-reviewer.md:5` | serena | tools: allowlist (mcp__serena__find_symbol, find_referencing_symbols) | ALLOW | DEC | Read/Grep | `tools: [Read, Grep, Glob, Bash, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols]` |
| R002 | `src/superclaude/agents/auggie-reviewer.md:36` | serena | mcp__serena__find_symbol for adjacent context | SYM | DEC | Read named in same line | `2. **For each non-trivial change, pull adjacent context** with 'Read' (or 'mcp__serena__find_symbol'): the surrounding function, the callers, the callees. Most bugs hide in the join between ...` |
| R003 | `src/superclaude/agents/auggie-reviewer.md:81` | serena | find_symbol / find_referencing_symbols cross-reference | REF | DEC | Read/Grep | `- **mcp__serena__find_symbol** / **find_referencing_symbols**: precise symbol-level cross-reference when you need to confirm who calls what` |
| R004 | `src/superclaude/agents/auggie-reviewer.md:115` | serena | 'Serena symbol tools freely' | SYM | DEC | none needed | `- Use cheap codebase queries (mcp__auggie__codebase-retrieval, Serena symbol tools) freely` |
| R005 | `src/superclaude/agents/pm-agent.md:11` | serena | Session start restores context from Serena memory (MANDATORY) | MEM | LB | none | `- **Session Start (MANDATORY)**: ALWAYS activates to restore context from Serena MCP memory` |
| R006 | `src/superclaude/agents/pm-agent.md:19-21` | serena | Session lifecycle built on Serena memory operations | MEM | LB | none | `## Session Lifecycle (Serena MCP Memory Integration)` |
| R007 | `src/superclaude/agents/pm-agent.md:31-35` | serena | list_memories / read_memory restore (body protocol) | MEM | LB | none | `1. list_memories() → Check for existing PM Agent state` |
| R008 | `src/superclaude/agents/pm-agent.md:54` | serena | write_memory plan | MEM | LB | none | `- write_memory("plan", goal_statement)` |
| R009 | `src/superclaude/agents/pm-agent.md:67` | serena | write_memory checkpoint every 30 min | MEM | LB | none | `- write_memory("checkpoint", progress) every 30min` |
| R010 | `src/superclaude/agents/pm-agent.md:78` | serena | think_about_task_adherence self-evaluation | NUDGE | LB | none | `- think_about_task_adherence() → Self-evaluation` |
| R011 | `src/superclaude/agents/pm-agent.md:93` | serena | write_memory summary | MEM | LB | none | `- write_memory("summary", outcomes)` |
| R012 | `src/superclaude/agents/pm-agent.md:105` | serena | think_about_whether_you_are_done | NUDGE | LB | none | `1. think_about_whether_you_are_done()` |
| R013 | `src/superclaude/agents/pm-agent.md:109-114` | serena | write_memory last_session / next_actions | MEM | LB | none | `2. write_memory("last_session", summary)` |
| R014 | `src/superclaude/agents/pm-agent.md:133` | serena | write_memory pm_context | MEM | LB | none | `- write_memory("pm_context", complete_state)` |
| R015 | `src/superclaude/agents/pm-agent.md:157-160` | serena | think_about_* named in self-check questions | NUDGE | DEC | none needed | `- "Did I follow the architecture patterns?" (think_about_task_adherence)` |
| R016 | `src/superclaude/agents/pm-agent.md:240-252` | serena | Memory Operations Reference: list/read/write_memory | MEM | LB | none | `PM Agent uses specific Serena MCP memory operations:` |
| R017 | `src/superclaude/agents/pm-agent.md:255-257` | serena | Memory Operations Reference: think_about_* triad | NUDGE | LB | none | `- think_about_task_adherence() → "Am I following patterns?"` |
| R018 | `src/superclaude/agents/pm-agent.md:260-262` | serena | Session End: write_memory last_session / next_actions / pm_context | MEM | LB | none | `- write_memory("last_session", summary) → What was accomplished` |
| R019 | `src/superclaude/agents/reflect-reviewer.md:5` | serena | tools: allowlist (find_symbol, find_referencing_symbols, get_symbols_overview, get_diagnostics_for_file) | ALLOW | DEC | body never names them (UNVERIFIED whether the reviewer calls them) | `tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for ...` |
| R020 | `src/superclaude/agents/reflect-reviewer.md:147` | serena | no-mutation denylist note about execute_shell_command/serena path | DOC | DEC | n/a | `4. **L3 (§6.1.1 no-mutation denylist)** — defense-in-depth on the 'execute_shell_command'/serena path (NOT the incident vector, which traveled the Bash-tool/L1 path).` |
| R021 | `src/superclaude/agents/reuse-auditor.md:5` | serena | tools: allowlist (find_symbol, get_symbols_overview, find_referencing_symbols) | ALLOW | DEC | Read/Grep | `tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols` |
| R022 | `src/superclaude/agents/reuse-auditor.md:54` | serena | F1 fingerprint uses get_symbols_overview + Read | SYM | DEC | Read | `\| F1 I/O skeleton \| read→transform→write data-flow shape \| 'get_symbols_overview' + Read body \|` |
| R023 | `src/superclaude/agents/reuse-auditor.md:57` | serena | F4 call-graph role uses find_referencing_symbols | REF | LB | rg skeleton grep (line 131), findings capped advisory | `\| F4 call-graph role \| when in the pipeline it fires \| 'find_referencing_symbols' \|` |
| R024 | `src/superclaude/agents/reuse-auditor.md:131` | serena | auggie-unavailable fallback to serena find_symbol + ripgrep | SYM | DEC | ripgrep named in same line | `- **auggie-unavailable (fail-open, NEVER STOP):** fall back to serena 'find_symbol' by capability tokens + ripgrep skeleton grep; compute C_cap/C_shape from structure only (renormalize, drop ...` |
| R025 | `src/superclaude/agents/troubleshoot-analyst.md:5` | serena | tools: allowlist (4 serena tools); exact set pinned by test | ALLOW | DEC | body never names them | `tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for ...` |

### 5.2 Core docs (8 rows: 0 LB, 8 DEC)

| ID | Primitive:line | Server | Tool or concept | Job | Class | Fallback | Quoted line |
|---|---|---|---|---|---|---|---|
| R026 | `src/superclaude/core/CLAUDE.md:21` | serena | MCP table row: serena, flag `--serena` | DOC | DEC | n/a | `\| serena \| Symbol navigation, project memory \| --serena \|` |
| R027 | `src/superclaude/core/CLAUDE.md:90` | serena | S2 trigger text names replace_content / replace_symbol_body | EDIT | DEC | n/a | `- **S2.** About to issue an Edit / Write / replace_content / replace_symbol_body` |
| R028 | `src/superclaude/core/CLAUDE.md:112` | serena | Refresh-tool table: symbolic queries -> mcp__serena__find_symbol / find_referencing_symbols | SYM | DEC | Read/rg | `\| Symbolic queries (which function, where defined, what references) \| 'mcp__serena__find_symbol' / 'find_referencing_symbols' \|` |
| R029 | `src/superclaude/core/HOW-WE-WORK.md:237` | serena | /sc:save and /sc:load store Serena project memory | MEM | DEC | n/a (routing prose) | `'/sc:save' and '/sc:load' store and load Serena project memory. They are not a way to resume work or a guarantee of complete executor state. Other command-owned continuations keep their own ...` |
| R030 | `src/superclaude/core/HOW-WE-WORK.md:327` | serena | /sc:load row: 'requires Serena' (test-pinned) | MEM | DEC | n/a (routing prose) | `\| '/sc:load' \| Load/refresh Serena project context with supported type/refresh/analyze controls; requires Serena. Not executor resume or proof of complete checkpoint restoration; exclude und ...` |
| R031 | `src/superclaude/core/HOW-WE-WORK.md:329` | serena | /sc:save row: 'Requires Serena and writes memory' (test-pinned) | MEM | DEC | n/a (routing prose) | `\| '/sc:save' \| Persist requested session/learnings/context/all memory with supported summarize/checkpoint controls. Requires Serena and writes memory; not durable task execution state or a l ...` |
| R032 | `src/superclaude/core/RESEARCH_CONFIG.md:26` | serena | research tools config: memory: serena | MEM | DEC | session only | `tools: {discovery: tavily, routing: smart, memory: serena, parallel: true}` |
| R033 | `src/superclaude/core/RESEARCH_CONFIG.md:142` | serena | table: serena \| memory management \| session only | MEM | DEC | session only | `\| serena \| memory management \| session only \|` |

### 5.2b Modes (11 rows: 9 LB, 2 DEC)

| ID | Primitive:line | Server | Tool or concept | Job | Class | Fallback | Quoted line |
|---|---|---|---|---|---|---|---|
| R034 | `src/superclaude/modes/MODE_Orchestration.md:24` | serena | routing table: Symbol operations -> Serena MCP, fallback Manual search | EDIT | DEC | Manual search named | `\| Symbol operations \| Serena MCP \| Manual search \|` |
| R035 | `src/superclaude/modes/MODE_Task_Management.md:15-18` | serena | Memory schema: write_memory plan/phase/task/todo (never says 'Serena') | MEM | LB | none | `📋 **Plan** → write_memory("plan", goal_statement)` |
| R036 | `src/superclaude/modes/MODE_Task_Management.md:25-26` | serena | Session start: list_memories / read_memory | MEM | LB | none | `1. list_memories() → Show existing task state` |
| R037 | `src/superclaude/modes/MODE_Task_Management.md:27` | serena | think_about_collected_information | NUDGE | LB | none | `3. think_about_collected_information() → Understand where we left off` |
| R038 | `src/superclaude/modes/MODE_Task_Management.md:33` | serena | write_memory task completion | MEM | LB | none | `1. write_memory("task_2.1", "completed: auth middleware")` |
| R039 | `src/superclaude/modes/MODE_Task_Management.md:34` | serena | think_about_task_adherence | NUDGE | LB | none | `2. think_about_task_adherence() → Verify on track` |
| R040 | `src/superclaude/modes/MODE_Task_Management.md:36` | serena | write_memory checkpoint every 30 min | MEM | LB | none | `4. write_memory("checkpoint", current_state) every 30min` |
| R041 | `src/superclaude/modes/MODE_Task_Management.md:42` | serena | think_about_whether_you_are_done | NUDGE | LB | none | `1. think_about_whether_you_are_done() → Assess completion` |
| R042 | `src/superclaude/modes/MODE_Task_Management.md:43-44` | serena | write_memory session_summary / delete_memory | MEM | LB | none | `2. write_memory("session_summary", outcomes)` |
| R043 | `src/superclaude/modes/MODE_Task_Management.md:49-53` | serena | Workflow: load via list/read_memory, write_memory per level | MEM | LB | none | `1. **Load**: list_memories() → read_memory() → Resume state` |
| R044 | `src/superclaude/modes/MODE_Task_Management.md:82-108` | serena | worked example with write_memory/read_memory/think_about_* | MEM | DEC | example only | `list_memories() → Empty` |

### 5.3 Hooks (3 rows: 2 LB, 1 DEC)

| ID | Primitive:line | Server | Tool or concept | Job | Class | Fallback | Quoted line |
|---|---|---|---|---|---|---|---|
| R045 | `src/superclaude/hooks/hooks.json:47` | serena | PreToolUse matcher names 4 mcp__serena__ edit tools -> freshness-pre-edit.sh (pinned by test) | EDIT | LB | none: matcher entries go dead when Serena is removed | `"matcher": "Edit\|Write\|mcp__serena__replace_content\|mcp__serena__replace_symbol_body\|mcp__serena__insert_after_symbol\|mcp__serena__insert_before_symbol",` |
| R046 | `src/superclaude/hooks/scripts/freshness-pre-edit.sh:25` | serena | reads tool_input.relative_path (Serena edit-tool argument shape; never says 'serena') | EDIT | LB | file_path path also handled | `REL_PATH=$(printf '%s' "$INPUT" \| jq -r '.tool_input.relative_path // empty' 2>/dev/null)` |
| R047 | `src/superclaude/hooks/scripts/freshness-pre-edit.sh:36` | serena | fail-open message mentions relative_path | EDIT | DEC | n/a | `echo "freshness-pre-edit: no file_path/relative_path in tool_input for $TOOL_NAME; allowing." >&2` |

### 5.4 MCP guides and configs (7 rows: 1 LB, 6 DEC)

| ID | Primitive:line | Server | Tool or concept | Job | Class | Fallback | Quoted line |
|---|---|---|---|---|---|---|---|
| R048 | `src/superclaude/mcp/MCP_Serena.md:1 (whole file; first hit shown)` | serena | entire Serena server guide (installed to ~/.claude/mcp; filename pinned by test) | CFG | DEC | n/a | `# Serena MCP Server` |
| R049 | `src/superclaude/mcp/MCP_Tavily.md:31` | serena | Serena stores Tavily research sessions | MEM | DEC | n/a | `- **Serena**: Tavily performs searches → Serena stores research sessions` |
| R050 | `src/superclaude/mcp/MCP_Tavily.md:152` | serena | flow step 5: Serena stores research session | MEM | DEC | n/a | `5. Serena: Store research session` |
| R051 | `src/superclaude/mcp/MCP_Morphllm.md:15-31` | serena | comparison prose: Morphllm vs Serena for edits | EDIT | DEC | n/a | `- **Over Serena**: For pattern-based edits, not symbol operations` |
| R052 | `src/superclaude/mcp/MCP_Auggie.md:16-37` | serena | comparison prose: Auggie vs Serena | SYM | DEC | n/a | `- **Over Serena**: When you need broad codebase recall, not symbol-level navigation` |
| R053 | `src/superclaude/mcp/configs/serena.json:2 (whole file; first hit shown)` | serena | server definition `uvx --from serena-agent==1.7.0 serena start-mcp-server` (pinned by registry test; consumer is cli/install_mcp.py, W2) | CFG | LB | none | `"serena": {` |
| R054 | `src/superclaude/mcp/configs/serena-docker.json:2 (whole file; first hit shown)` | serena | docker variant of the server definition (consumption UNVERIFIED; file list pinned by test) | CFG | DEC | n/a | `"serena": {` |

### 5.5 Commands (62 rows: 12 LB, 50 DEC)

| ID | Primitive:line | Server | Tool or concept | Job | Class | Fallback | Quoted line |
|---|---|---|---|---|---|---|---|
| R055 | `src/superclaude/commands/cli-eval.md:6` | serena | mcp-servers: [context7, serena] | ALLOW | DEC | metadata | `mcp-servers: [context7, serena]` |
| R056 | `src/superclaude/commands/validate-roadmap.md:6` | serena | allowed-tools: mcp__serena__read_memory, write_memory, find_symbol, get_symbols_overview, search_for_pattern, activate_project | ALLOW | LB | skill body calls them fail-open | `allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__auggie-mcp__codebase-retrieval, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__find_symbol ...` |
| R057 | `src/superclaude/commands/validate-roadmap.md:7` | serena | mcp-servers: [auggie, serena] | ALLOW | DEC | metadata | `mcp-servers: [auggie, serena]` |
| R058 | `src/superclaude/commands/pm.md:6` | serena | mcp-servers list includes serena | ALLOW | DEC | metadata | `mcp-servers: [context7, playwright, morphllm, serena, tavily]` |
| R059 | `src/superclaude/commands/pm.md:16` | serena | Session Start (MANDATORY) restore context via Serena MCP memory | MEM | LB | none | `- **Session Start (MANDATORY)**: ALWAYS activates to restore context via Serena MCP memory` |
| R060 | `src/superclaude/commands/pm.md:47` | serena | PM keeps continuous context across sessions via Serena MCP memory | MEM | LB | none | `PM Agent is the always-active orchestration layer that auto-delegates user requests to domain specialists (backend, frontend, security, etc.) without requiring manual agent selection. It mai ...` |
| R061 | `src/superclaude/commands/brainstorm.md:6` | serena | mcp-servers: [serena, auggie-mcp, tavily] | ALLOW | DEC | metadata | `mcp-servers: [serena, auggie-mcp, tavily]` |
| R062 | `src/superclaude/commands/release-split.md:7` | serena | mcp-servers: [context7, serena] | ALLOW | DEC | metadata | `mcp-servers: [context7, serena]` |
| R063 | `src/superclaude/commands/adversarial.md:7` | serena | mcp-servers: [context7, serena] | ALLOW | DEC | metadata | `mcp-servers: [context7, serena]` |
| R064 | `src/superclaude/commands/task.md:7` | serena | mcp-servers list includes serena | ALLOW | DEC | metadata | `mcp-servers: [context7, serena, playwright, morphllm]` |
| R065 | `src/superclaude/commands/cleanup-audit.md:7` | serena | mcp-servers: [serena, context7] | ALLOW | DEC | metadata | `mcp-servers: [serena, context7]` |
| R066 | `src/superclaude/commands/post-release.md:7` | serena | mcp-servers: [serena] | ALLOW | DEC | metadata | `mcp-servers: [serena]` |
| R067 | `src/superclaude/commands/init-lite.md:7` | serena | mcp-servers: [serena] | ALLOW | DEC | metadata | `mcp-servers: [serena]` |
| R068 | `src/superclaude/commands/cli-portify.md:7` | serena | mcp-servers: [serena, context7] | ALLOW | DEC | metadata | `mcp-servers: [serena, context7]` |
| R069 | `src/superclaude/commands/auggie-review.md:6` | serena | mcp-servers: [serena] | ALLOW | DEC | metadata | `mcp-servers: [serena]` |
| R070 | `src/superclaude/commands/auggie-review.md:78` | serena | Serena: symbol-level cross-reference when validating Auggie citations | REF | DEC | Read | `- **Serena**: Symbol-level cross-reference when validating Auggie's file:line citations against actual code` |
| R071 | `src/superclaude/commands/pr-submit.md:6` | serena | mcp-servers: [serena, auggie] | ALLOW | DEC | metadata | `mcp-servers: [serena, auggie]` |
| R072 | `src/superclaude/commands/review-translation.md:6` | serena | mcp-servers list includes serena | ALLOW | DEC | metadata | `mcp-servers: [tavily, context7, serena]` |
| R073 | `src/superclaude/commands/research.md:6` | serena | mcp-servers list includes serena | ALLOW | DEC | metadata | `mcp-servers: [tavily, playwright, serena]` |
| R074 | `src/superclaude/commands/research.md:100` | serena | Serena: research session persistence | MEM | DEC | n/a | `- **Serena**: Research session persistence` |
| R075 | `src/superclaude/commands/troubleshoot.md:3` | serena | description names auggie + serena grounding | DOC | DEC | n/a | `description: "Tiered debugging — fast Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate, and an opt-in remediation chain (s ...` |
| R076 | `src/superclaude/commands/troubleshoot.md:6` | serena | mcp-servers: [auggie, serena, context7, tavily] | ALLOW | DEC | metadata | `mcp-servers: [auggie, serena, context7, tavily]` |
| R077 | `src/superclaude/commands/troubleshoot.md:52` | serena | --scope narrows auggie/serena queries | SYM | DEC | n/a | `\| '--scope' \| (none) \| File, directory, or symbol to narrow auggie/serena queries against. \|` |
| R078 | `src/superclaude/commands/troubleshoot.md:58` | serena | --no-mcp skips auggie/serena | DOC | DEC | native-only mode exists | `\| '--no-mcp' \| 'false' \| Run in native-tools-only mode (skip auggie/serena/context7/tavily). Tier 1 quality degrades; surfaced in the report. \|` |
| R079 | `src/superclaude/commands/troubleshoot.md:75` | serena | Tier 1 grounding with auggie/serena | SYM | DEC | n/a | `\| Tier 1 \| Always (unless STOP) \| Single grounded hypothesis from 'root-cause-analyst' + 'confidence-calibrator', with auggie/serena grounding \| ~3-6k Claude tokens, 1-3 min \|` |
| R080 | `src/superclaude/commands/troubleshoot.md:89` | serena | Serena: Tier 1+2 symbol navigation, 'Critical when the issue names a specific function or class' | SYM | LB | Grep/Glob (--no-mcp) | `- **Serena**: Tier 1 + Tier 2 symbol-level navigation via 'find_symbol', 'find_referencing_symbols', 'get_symbols_overview'. Critical when the issue names a specific function or class.` |
| R081 | `src/superclaude/commands/troubleshoot.md:96` | serena | tool list: find_symbol / find_referencing_symbols / get_symbols_overview | SYM | DEC | n/a | `- **'mcp__serena__find_symbol' / 'find_referencing_symbols' / 'get_symbols_overview'**: symbol navigation` |
| R082 | `src/superclaude/commands/troubleshoot.md:112` | serena | example comment: spawns root-cause-analyst with auggie + serena | DOC | DEC | n/a | `# - Spawns root-cause-analyst with auggie + serena grounding` |
| R083 | `src/superclaude/commands/troubleshoot.md:161` | serena | example comment: --no-mcp skips auggie/serena | DOC | DEC | n/a | `# - Skip auggie/serena/context7/tavily; use Read/Grep/Glob/Bash only` |
| R084 | `src/superclaude/commands/troubleshoot.md:173` | serena | 'Use auggie + serena every tier' | SYM | DEC | n/a | `- Use auggie + serena every tier for in-repo grounding; use context7 + tavily in Tier 2 when the symptom suggests external knowledge, with the skill's conditional Tier 1 behaviour-definition ...` |
| R085 | `src/superclaude/commands/load.md:3` | serena | description: Serena MCP integration for project context loading | DOC | DEC | n/a | `description: "Session lifecycle management with Serena MCP integration for project context loading"` |
| R086 | `src/superclaude/commands/load.md:6` | serena | mcp-servers: [serena] | ALLOW | DEC | metadata | `mcp-servers: [serena]` |
| R087 | `src/superclaude/commands/load.md:27` | serena | Initialize: establish Serena MCP connection | ACT | LB | none | `1. **Initialize**: Establish Serena MCP connection and session context management` |
| R088 | `src/superclaude/commands/load.md:35` | serena | Serena MCP integration for memory management | MEM | DEC | n/a | `- Serena MCP integration for memory management and cross-session persistence` |
| R089 | `src/superclaude/commands/load.md:42` | serena | Serena MCP: Mandatory integration for project activation, memory retrieval | MEM | LB | none | `- **Serena MCP**: Mandatory integration for project activation, memory retrieval, and session management` |
| R090 | `src/superclaude/commands/load.md:48` | serena | tool list: activate_project | ACT | LB | none | `- **activate_project**: Core project activation and context establishment` |
| R091 | `src/superclaude/commands/load.md:49` | serena | tool list: list_memories / read_memory | MEM | LB | none | `- **list_memories/read_memory**: Memory retrieval and session context loading` |
| R092 | `src/superclaude/commands/load.md:66` | serena | example comment: loads context with Serena memory integration | MEM | DEC | n/a | `# Loads current directory project context with Serena memory integration` |
| R093 | `src/superclaude/commands/load.md:98` | serena | Will: load context using Serena MCP integration | MEM | DEC | n/a | `- Load project context using Serena MCP integration for memory management` |
| R094 | `src/superclaude/commands/load.md:105` | serena | Will not: load context without Serena MCP integration | MEM | DEC | n/a | `- Load context without proper Serena MCP integration and validation` |
| R095 | `src/superclaude/commands/save.md:3` | serena | description: Serena MCP integration for session persistence | DOC | DEC | n/a | `description: "Session lifecycle management with Serena MCP integration for session context persistence"` |
| R096 | `src/superclaude/commands/save.md:6` | serena | mcp-servers: [serena] | ALLOW | DEC | metadata | `mcp-servers: [serena]` |
| R097 | `src/superclaude/commands/save.md:28` | serena | Persist: save session context and learnings using Serena MCP memory | MEM | LB | none | `2. **Persist**: Save session context and learnings using Serena MCP memory management` |
| R098 | `src/superclaude/commands/save.md:35` | serena | Serena MCP integration for memory management | MEM | DEC | n/a | `- Serena MCP integration for memory management and cross-session persistence` |
| R099 | `src/superclaude/commands/save.md:42` | serena | Serena MCP: Mandatory integration for session management, memory operations | MEM | LB | none | `- **Serena MCP**: Mandatory integration for session management, memory operations, and cross-session persistence` |
| R100 | `src/superclaude/commands/save.md:48` | serena | tool list: write_memory / read_memory | MEM | LB | none | `- **write_memory/read_memory**: Core session context persistence and retrieval` |
| R101 | `src/superclaude/commands/save.md:49-50` | serena | tool list: think_about_collected_information, summarize_changes | NUDGE | LB | none | `- **think_about_collected_information**: Session analysis and discovery identification` |
| R102 | `src/superclaude/commands/save.md:66` | serena | example comment: saves session to Serena MCP | MEM | DEC | n/a | `# Saves current session discoveries and context to Serena MCP` |
| R103 | `src/superclaude/commands/save.md:98` | serena | Will: save session context using Serena MCP | MEM | DEC | n/a | `- Save session context using Serena MCP integration for cross-session persistence` |
| R104 | `src/superclaude/commands/save.md:104` | serena | Will not: operate without Serena MCP integration | MEM | DEC | n/a | `- Operate without proper Serena MCP integration and memory access` |
| R105 | `src/superclaude/commands/reflect.md:6` | serena | mcp-servers: [auggie, serena, context7, tavily] | ALLOW | DEC | metadata | `mcp-servers: [auggie, serena, context7, tavily]` |
| R106 | `src/superclaude/commands/reflect.md:106` | serena | --no-verify flag doc (execute_shell_command triangle) | DIAG | DEC | skill owns behaviour | `\| '--no-verify' \| 'false' (UC-2) \| Disable the UC-2 verification triangle ('execute_shell_command' scoped non-mutating tests/linters/type-checkers/build, §6.1 step 5.5). Default-on; when set ...` |
| R107 | `src/superclaude/commands/reflect.md:108` | serena | --onboard flag doc (Serena onboarding bootstrap) | ACT | DEC | skill owns behaviour | `\| '--onboard' \| 'false' \| Opt-in one-shot Serena 'onboarding' bootstrap at Wave 0.7b — runs ONLY when 'list_memories' is empty for the project slug; seeds the §6.3 cold-start calibration bas ...` |
| R108 | `src/superclaude/commands/reflect.md:109` | serena | --with-hierarchy flag doc (type_hierarchy) | SYM | DEC | skill owns behaviour | `\| '--with-hierarchy' \| 'false' \| Opt-in 'type_hierarchy' transitive supertype/subtype retrieval (§6.1 step 4.5, Wave 1B.3). Backend-gated ('jetbrains' only; default OFF on 'lsp', unavailable ...` |
| R109 | `src/superclaude/commands/reflect.md:144` | serena | Tier 1 table: auggie/serena grounding | SYM | DEC | n/a | `\| Tier 1 \| Always (unless STOP) \| Single grounded card from 'root-cause-analyst' + 'confidence-calibrator', with auggie/serena grounding. \| ~3-6k Claude tokens, 1-3 min \|` |
| R110 | `src/superclaude/commands/reflect.md:158` | serena | Serena: Wave 0-6 symbol navigation and verification triangle | SYM | DEC | skill owns behaviour | `- **Serena**: Wave 0-6 symbol-level navigation ('find_symbol', 'find_referencing_symbols', 'get_symbols_overview', plus 'find_declaration' / 'find_implementations' / 'type_hierarchy' for dec ...` |
| R111 | `src/superclaude/commands/reflect.md:166-168` | serena | tool list: find_symbol, find_referencing_symbols, get_symbols_overview, find_declaration, find_implementations, type_hierarchy | SYM | DEC | skill owns behaviour | `- **'mcp__serena__find_symbol' / 'find_referencing_symbols' / 'get_symbols_overview'**: symbol navigation` |
| R112 | `src/superclaude/commands/reflect.md:169` | serena | tool list: get_diagnostics_for_file / execute_shell_command / summarize_changes | DIAG | DEC | skill owns behaviour | `- **'mcp__serena__get_diagnostics_for_file' / 'execute_shell_command' / 'summarize_changes'**: UC-2 §6.1 step-5.5 verification triangle (LSP issues + scoped non-mutating tests/linters/type-c ...` |
| R113 | `src/superclaude/commands/reflect.md:170` | serena | tool list: onboarding | ACT | DEC | skill owns behaviour | `- **'mcp__serena__onboarding'**: opt-in cold-start memory bootstrap at Wave 0.7b ('--onboard', default OFF)` |
| R114 | `src/superclaude/commands/reflect.md:171` | serena | tool list: think_about_* | NUDGE | DEC | skill owns behaviour | `- **'mcp__serena__think_about_*'**: checkpoint signals (§6.4) — three-row table feeds the merge, never the sole verdict` |
| R115 | `src/superclaude/commands/reflect.md:172` | serena | tool list: read_memory / write_memory / list_memories | MEM | DEC | skill owns behaviour | `- **'mcp__serena__read_memory' / 'write_memory' / 'list_memories'**: cross-session learning capture (§6.3 — 20-entry, 90-day retention)` |
| R116 | `src/superclaude/commands/reflect.md:281` | serena | Won't: use think_about_* as sole reflection mechanism | NUDGE | DEC | n/a | `- Use the Serena 'think_about_*' triad as the sole reflection mechanism (the v1 failure mode) — they are checkpoint signals only; the protocol applies §6.4 fail-open policy` |

### 5.6 Skills (SKILL.md, refs, scripts) (135 rows: 48 LB, 87 DEC)

| ID | Primitive:line | Server | Tool or concept | Job | Class | Fallback | Quoted line |
|---|---|---|---|---|---|---|---|
| R117 | `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md:28` | serena | heuristic table: 'auggie/serena beats brute Grep' | SYM | DEC | n/a | `\| Repository-wide semantic ranking \| Many Grep/Glob calls \| YES (auggie/serena beats brute Grep) \|` |
| R118 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:3` | serena | description names auggie + serena grounding | DOC | DEC | n/a | `description: "Tiered debugging protocol — fast Tier 1 triage with auggie + serena grounding, auto-escalation to parallel hypothesis agents + adversarial fix debate in Tier 2, and an opt-in r ...` |
| R119 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:4` | serena | allowed-tools: mcp__serena__find_symbol, find_referencing_symbols, get_symbols_overview, ... | ALLOW | LB | Grep/Glob fallback (line 439) | `allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get ...` |
| R120 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:10` | serena | mcp-servers: [auggie, serena, context7, tavily] | ALLOW | DEC | metadata | `mcp-servers: [auggie, serena, context7, tavily]` |
| R121 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:31` | serena | analyst profile resolution note names serena | DOC | DEC | n/a | `- **Resolve before dispatch:** inspect '.claude/agents/troubleshoot-analyst.md' first, then '~/.claude/agents/troubleshoot-analyst.md' only if the project copy is absent. Read the selected d ...` |
| R122 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:156` | serena | --scope narrows auggie/serena queries | SYM | DEC | n/a | `3. Resolve '--scope' to a concrete path/symbol. If given, narrow auggie/serena queries to that target.` |
| R123 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:168` | serena | telemetry field mcps_available: <auggie\|serena\|...> | DOC | DEC | n/a | `mcps_available: <auggie\|serena\|context7\|tavily\|none>` |
| R124 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:193` | serena | Tier 1 step: mcp__serena__get_symbols_overview / find_symbol on the target | SYM | LB | Glob/Grep fallback (line 439) | `- 'mcp__serena__get_symbols_overview' on the target file or 'mcp__serena__find_symbol' on a specific function if the issue names one.` |
| R125 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:216` | serena | exit criteria: auggie + serena results captured, or Glob/Grep fallback noted | SYM | DEC | Glob/Grep named | `**Exit criteria**: Real-code grounding complete (auggie + serena results captured in audit log, or 'Glob'/'Grep' fallback noted); observation captured at '<output-dir>/tier1-observation.md' ...` |
| R126 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:439` | serena | failure table: MCP call fails -> Grep/Glob | DOC | DEC | n/a | `\| MCP call fails (auggie/serena) \| Fall back to 'Grep'/'Glob'; note in audit \| None — proceed without that enrichment \|` |
| R127 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:606` | serena | tier tool matrix row for the three symbol tools | SYM | DEC | n/a | `\| 'mcp__serena__find_symbol' / 'find_referencing_symbols' / 'get_symbols_overview' \| ✓ \| ✓ \| — \|` |
| R128 | `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:620` | serena | 'Use auggie/serena every tier' | SYM | DEC | n/a | `- Use auggie/serena every tier for in-repo grounding; use context7/tavily for relevant Tier 2 enrichment, with the conditional behaviour-definition fetch also permitted in Tier 1 before pair ...` |
| R129 | `src/superclaude/skills/sc-troubleshoot-protocol/refs/diagnosability-audit.md:11 (whole file; first hit shown)` | serena | audit prompt mentions serena | DOC | DEC | n/a | `Each branch issues ONE 'mcp__auggie__codebase-retrieval' call (single message, fan-out via parallel Task spawns from the Wave 1.6 orchestrator). Each branch is dispatched with 'subagent_type ...` |
| R130 | `src/superclaude/skills/sc-troubleshoot-protocol/refs/triage-checklist.md:11` | serena | checklist item: serena symbol overview | SYM | DEC | n/a | `- [ ] The serena symbol overview / surrounding function definitions` |
| R131 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:4` | serena | allowed-tools: mcp__serena__read_memory, write_memory, find_symbol, get_symbols_overview, search_for_pattern, activate_project | ALLOW | LB | all calls fail-open | `allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__auggie-mcp__codebase-retrieval, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__find_symbol ...` |
| R132 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:13` | serena | mcp-servers: [auggie, serena] | ALLOW | DEC | metadata | `mcp-servers: [auggie, serena]` |
| R133 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:22-25` | serena | description: deep protocol grounded in Auggie/Serena enrichment | DOC | DEC | n/a | `- **Use this skill** for thorough investigative validation — when a human reviewer wants a multi-phase coverage matrix, gap registry, adversarial review, and remediation plan grounded in Aug ...` |
| R134 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:47` | serena | phase table: extraction via Auggie/Serena enrichment | SYM | DEC | n/a | `\| Phase 1 — Extraction & taxonomy \| Coverage (#6, input-aware) \| Skill extracts requirements via Auggie/Serena enrichment; CLI relies on caller-supplied input files. \|` |
| R135 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:126-127` | serena | MCP table: read/write session memory | MEM | DEC | table row (steps below are the LB rows) | `\| Read session memory \| 'mcp__serena__read_memory' \| Load validation ledger, terminology, patterns (Pre-Phase 0) — fail-open \|` |
| R136 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:128` | serena | MCP table: activate_project | ACT | DEC | table row | `\| Activate project \| 'mcp__serena__activate_project' \| Initialize Serena project context (Pre-Phase 0, Step 0.5) — fail-open \|` |
| R137 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:129-130` | serena | MCP table: find_symbol / get_symbols_overview | SYM | DEC | table row | `\| Find symbol \| 'mcp__serena__find_symbol' \| Symbol lookup for context supplement (Step 0.5, deep only) — fail-open \|` |
| R138 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:138-145` | serena | Pre-Phase 0: load validation ledger / terminology / patterns from memory | MEM | LB | fail-open skip | `**Requires**: 'mcp__serena__read_memory', 'mcp__serena__activate_project' (fail-open — skip all pre-phase hooks if Serena is unavailable).` |
| R139 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:146` | serena | Pre-Phase 0: mcp__serena__activate_project | ACT | LB | fail-open skip | `1. Call 'mcp__serena__activate_project' for the current repository.` |
| R140 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:147-165` | serena | Pre-Phase 0: read_memory validation-ledger / terminology-map / adversarial-patterns | MEM | LB | fail-open skip | `2. Call 'mcp__serena__read_memory' with key 'validation-ledger-{project-slug}'.` |
| R141 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:320-328` | serena | Step 0.5 (deep only): find_symbol / get_symbols_overview enrichment | SYM | LB | skip, no artifact | `**Requires**: 'mcp__serena__find_symbol', 'mcp__serena__get_symbols_overview' (fail-open — skip entirely if Serena is unavailable or depth is not 'deep').` |
| R142 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:329` | serena | Step 0.5: activate Serena project | ACT | LB | skip, no artifact | `2. **Activate Serena project**: Call 'mcp__serena__activate_project' (if not already activated in Pre-Phase 0).` |
| R143 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:331-349` | serena | Step 0.5: per-identifier find_symbol include_body=False; failure handling | SYM | LB | skip, no artifact | `- For each code identifier, call 'mcp__serena__find_symbol' with 'include_body=False' to locate the symbol's file, type (class/function/method), and parent hierarchy.` |
| R144 | `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:980-1071` | serena | Post-Phase 6: write ledger, terminology map, pattern log, adversarial stats to memory | MEM | LB | fail-open skip | `**Requires**: 'mcp__serena__write_memory' (fail-open — skip all post-phase hooks if Serena is unavailable).` |
| R145 | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:15` | serena | mcp-servers: [serena, auggie-mcp, tavily] | ALLOW | DEC | metadata | `mcp-servers: [serena, auggie-mcp, tavily]` |
| R146 | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:57` | serena | artifact description: Auggie/Serena/Glob output | SYM | DEC | n/a | `3. 'enrichment/codebase-context.md' (if applicable) — Auggie/Serena/Glob output` |
| R147 | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:193` | serena | quality_tier fallback_1 uses Serena | SYM | DEC | WebSearch/native tier | `- 'fallback_1' — primary failed, used Serena (codebase) or WebSearch (research)` |
| R148 | `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:387` | serena | Auggie down -> fall back to Serena get_symbols_overview, then native Glob/Grep | SYM | DEC | native fallback_2 | `\| Codebase enrichment fails (Auggie down) \| WARN, fall back to Serena 'get_symbols_overview' (quality_tier=fallback_1) \| Native Glob/Grep (quality_tier=fallback_2) \|` |
| R149 | `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:24-27` | serena | Tier 2 (fallback_1): Serena get_symbols_overview / find_symbol | SYM | DEC | native Tier 3 | `**Tier 2 (fallback_1)**: Serena MCP` |
| R150 | `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:10` | serena | mcp-servers: [serena, auggie] | ALLOW | DEC | metadata | `mcp-servers: [serena, auggie]` |
| R151 | `src/superclaude/skills/sc-cli-eval-protocol/SKILL.md:11` | serena | mcp-servers: [context7, serena] | ALLOW | DEC | metadata | `mcp-servers: [context7, serena]` |
| R152 | `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:7` | serena | mcp-servers: [serena, context7, auggie-mcp] | ALLOW | DEC | metadata | `mcp-servers: [serena, context7, auggie-mcp]` |
| R153 | `src/superclaude/skills/sc-release-split-protocol/SKILL.md:13` | serena | mcp-servers: [context7, serena] | ALLOW | DEC | metadata | `mcp-servers: [context7, serena]` |
| R154 | `src/superclaude/skills/sc-init-lite-protocol/SKILL.md:13` | serena | mcp-servers: [serena] | ALLOW | DEC | metadata | `mcp-servers: [serena]` |
| R155 | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:10` | serena | mcp-servers: [serena, auggie] | ALLOW | DEC | metadata | `mcp-servers: [serena, auggie]` |
| R156 | `src/superclaude/skills/sc-post-release-protocol/SKILL.md:11` | serena | mcp-servers: [serena] | ALLOW | DEC | metadata | `mcp-servers: [serena]` |
| R157 | `src/superclaude/skills/sc-post-release-protocol/SKILL.md:244-259` | serena | mcps_available telemetry set {auggie, serena, context7, tavily} | DOC | DEC | n/a | `- 'mcps_available' — the pipe-joined subset of '{auggie, serena, context7, tavily}' whose tools are present in the runtime tool list this session; 'none' if empty. Presence in the tool list ...` |
| R158 | `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:6` | serena | mcp-servers: [serena, context7] | ALLOW | DEC | metadata | `mcp-servers: [serena, context7]` |
| R159 | `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:57` | serena | exclusion-segment list includes `.serena/` | DOC | DEC | n/a | `segment (covers '.claude/', '.dev/', '.github/', '.serena/',` |
| R160 | `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:83` | serena | Serena MCP: import chain tracing in Step 1 discovery (no explicit tool call) | SYM | DEC | Grep/Read | `- **Serena MCP**: Import chain tracing during Step 1 discovery phase; symbol-level understanding for verifying dynamic loading patterns` |
| R161 | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:12` | serena | mcp-servers: [context7, serena] | ALLOW | DEC | metadata | `mcp-servers: [context7, serena]` |
| R162 | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:491` | serena | MCP table: Serena memory persistence of outcomes at Step 5 (rg finds no write_memory call in the skill) | MEM | DEC | n/a | `\| Serena \| Memory persistence of adversarial outcomes \| Step 5 \|` |
| R163 | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:2243-2285` | serena | persona/MCP yaml config naming serena | DOC | DEC | n/a | `serena:` |
| R164 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:13` | serena | mcp-servers: [context7, serena] | ALLOW | DEC | metadata | `mcp-servers: [context7, serena]` |
| R165 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:325-326` | serena | completion step: persist session state to Serena memory, else `.session-memory.md` | MEM | LB | `<output_dir>/.session-memory.md` | `2. Persist session state to Serena memory (key: 'sc-roadmap:<spec-name>:<timestamp>')` |
| R166 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:414-419` | serena | MCP table + circuit breaker: Serena session persistence | MEM | DEC | `.session-memory.md` | `\| Serena \| Session persistence, memory, cross-session state \| 0, 4, completion \|` |
| R167 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:425` | serena | Save points after each wave persist state to Serena memory | MEM | LB | `.session-memory.md` | `**Save points**: After each wave completion, persist session state to Serena memory using key 'sc-roadmap:<spec-name>:<timestamp>'. State accumulates progressively:` |
| R168 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:436` | serena | Resume protocol keyed on a matching Serena memory session | MEM | LB | none (resume unavailable, user warned) | `**Resume protocol**: When sc:roadmap is invoked and Serena memory contains a matching session (same 'spec_source' + 'output_dir'):` |
| R169 | `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:443-455` | serena | graceful degradation + feature list mention | MEM | DEC | `.session-memory.md` | `**Graceful degradation**: If Serena unavailable, proceed without persistence and write session state to '<output_dir>/.session-memory.md' as fallback. Warn user that cross-session resume is ...` |
| R170 | `src/superclaude/skills/sc-task-protocol/SKILL.md:88` | serena | STRICT execution step 1: mcp__serena__activate_project | ACT | LB | none ('fallback not allowed') | `1. Activate project (mcp__serena__activate_project)` |
| R171 | `src/superclaude/skills/sc-task-protocol/SKILL.md:91` | serena | STRICT execution step 4: list_memories -> read_memory | MEM | LB | none | `4. Check relevant memories (list_memories -> read_memory)` |
| R172 | `src/superclaude/skills/sc-task-protocol/SKILL.md:103` | serena | downstream impact: find_referencing_symbols OR grep | REF | DEC | grep named | `2. Search downstream impacts (find_referencing_symbols OR grep)` |
| R173 | `src/superclaude/skills/sc-task-protocol/SKILL.md:287` | serena | Required servers by tier: 'STRICT: Serena (fallback not allowed)' | ACT | LB | none | `- STRICT: Serena (fallback not allowed)` |
| R174 | `src/superclaude/skills/sc-task-protocol/SKILL.md:303` | serena | Tool Coordination planning: list_memories / read_memory | MEM | DEC | coordination list | `3. list_memories / read_memory: Check project state` |
| R175 | `src/superclaude/skills/sc-task-protocol/SKILL.md:309` | serena | Tool Coordination execution: find_referencing_symbols | REF | DEC | Grep/Glob listed one line above | `3. find_referencing_symbols: Trace dependencies` |
| R176 | `src/superclaude/skills/sc-task-protocol/SKILL.md:315` | serena | Tool Coordination verification: think_about_task_adherence | NUDGE | DEC | coordination list | `3. think_about_task_adherence: Reflect on completeness` |
| R177 | `src/superclaude/skills/sc-task-protocol/SKILL.md:319-320` | serena | Tool Coordination completion: write_memory, think_about_whether_you_are_done | MEM | DEC | coordination list | `1. write_memory: Save session state` |
| R178 | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:683` | serena | generated per-task tool table: STRICT tier Required Tools = Serena (leaks into generated tasklists) | ACT | LB | none | `\| STRICT \| Serena \| Context7 \| No \|` |
| R179 | `src/superclaude/skills/sc-pm-protocol/SKILL.md:21` | serena | heading: Session Lifecycle (Serena MCP Memory Integration) | MEM | LB | none | `## Session Lifecycle (Serena MCP Memory Integration)` |
| R180 | `src/superclaude/skills/sc-pm-protocol/SKILL.md:26-30` | serena | Session start: list_memories + read_memory pm_context/current_plan/last_session/next_actions | MEM | LB | none | `- list_memories() → Check for existing PM Agent state` |
| R181 | `src/superclaude/skills/sc-pm-protocol/SKILL.md:43-44` | serena | PDCA plan/do: write_memory plan, checkpoint every 30 min | MEM | LB | none | `1. Plan: write_memory("plan", goal_statement); define what to implement and why` |
| R182 | `src/superclaude/skills/sc-pm-protocol/SKILL.md:50-52` | serena | session end: write_memory last_session, next_actions, pm_context | MEM | LB | none | `1. Final Checkpoint: write_memory("last_session", summary); write_memory("next_actions", todo_list)` |
| R183 | `src/superclaude/skills/sc-pm-protocol/SKILL.md:113` | serena | learning capture: write_memory | MEM | LB | none | `6. Learning Capture: Success → write_memory; Failure → Return to Step 2` |
| R184 | `src/superclaude/skills/sc-pm-protocol/SKILL.md:157-166` | serena | learning/patterns and learning/mistakes write_memory | MEM | LB | none | `- write_memory("learning/patterns/[name]", reusable_pattern)` |
| R185 | `src/superclaude/skills/sc-crash-recovery/SKILL.md:3` | serena | description names serena memory as a recovery source | MEM | DEC | investigator skipped when dir absent | `description: Post-crash work-state recovery. Fans parallel subagents across pipeline artifacts (.dev/releases, manifest.json, execution-log.jsonl, .roadmap-state.json), recent Claude Code se ...` |
| R186 | `src/superclaude/skills/sc-crash-recovery/SKILL.md:37` | serena | WARN check: no `.serena/` among project markers | MEM | DEC | n/a | `- **WARN** (don't stop) if the resolved project path exists but has no '.dev/', no '.git/', no '.serena/', and no recent session logs. Tell the user the project looks untouched; ask whether ...` |
| R187 | `src/superclaude/skills/sc-crash-recovery/SKILL.md:62-67` | serena | bootstrap reports `.serena/` presence; skip serena-memory investigator if empty | MEM | DEC | skip | `- whether '.dev/', 'docs/', '.serena/', '.git/' exist` |
| R188 | `src/superclaude/skills/sc-crash-recovery/SKILL.md:79` | serena | investigator table: serena-memory runs only if `.serena/memories/` exists | MEM | DEC | skip | `\| serena-memory \| no '.serena/memories/' \| general-purpose \|` |
| R189 | `src/superclaude/skills/sc-crash-recovery/SKILL.md:145` | serena | failure table: serena-memory marked unscanned | MEM | DEC | unscanned | `\| 'bootstrap_scan.sh' exits non-zero or returns malformed JSON \| Continue with the investigators that don't depend on it (git-state, claude-sessions); mark pipeline-artifacts and serena-memo ...` |
| R190 | `src/superclaude/skills/sc-crash-recovery/SKILL.md:157` | serena | note: complementary to /sc:load (Serena project-context loader) | DOC | DEC | n/a | `- It does not replace '/sc:load' (Serena project-context loader). They're complementary: '/sc:load' loads project context into the session; this skill diagnoses outstanding work.` |
| R191 | `src/superclaude/skills/sc-crash-recovery/refs/investigators.md:76-85` | serena | serena-memory investigator prompt reads `.serena/memories/` files from disk | MEM | DEC | skipped when absent (works without the server) | `## 3. serena-memory` |
| R192 | `src/superclaude/skills/sc-crash-recovery/refs/investigators.md:164` | serena | example invocation | MEM | DEC | n/a | `[Task: serena-memory for tracel3t]` |
| R193 | `src/superclaude/skills/sc-crash-recovery/refs/report-template.md:63` | serena | report section: Serena memory highlights | MEM | DEC | omit when none | `## Serena memory highlights` |
| R194 | `src/superclaude/skills/sc-crash-recovery/refs/report-template.md:124` | serena | example: memory current_focus.md vs latest session | MEM | DEC | n/a | `- Serena memory 'current_focus.md' says we're on Y; latest session log shows assistant working on Z` |
| R195 | `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:146-147` | serena | JSON fields has_serena / serena_memory_count from `.serena/memories` | MEM | LB | false/0 when dir absent; consumed by SKILL.md investigator gating | `"has_serena": $([[ -d "$ABS_PROJECT/.serena/memories" ]] && echo true \|\| echo false),` |
| R196 | `src/superclaude/skills/ccsession-tag/install.sh:41` | serena | comment + rm -f of retired Serena context-save plan file in older installs | DOC | DEC | n/a | `# Remove the retired, unbuilt Serena context-save plan from older installations.` |
| R197 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:5` | serena | allowed-tools: 20 mcp__serena__ tools (symbol, reference, diagnostics, memory CRUD, config, onboarding, shell, type_hierarchy); exact set not test-pinned | ALLOW | LB | fail-open (line 1492) | `allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get ...` |
| R198 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:19` | serena | mcp-servers: [serena, auggie, context7, tavily] | ALLOW | DEC | metadata | `mcp-servers: [serena, auggie, context7, tavily]` |
| R199 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:22-29` | serena | supersedes legacy think_about_* command; rationale | DOC | DEC | n/a | `supersedes: src/superclaude/commands/reflect.md (legacy think_about_* surface)` |
| R200 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:90` | serena | --no-verify flag doc | DIAG | DEC | n/a | `- '--no-verify' — disable the UC-2 'execute_shell_command' verification triangle (§6.1 step 5.5). Default is *default-on*: in UC-2, scoped non-mutating verification (tests/linters/type-check ...` |
| R201 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:91` | serena | --onboard flag doc | ACT | DEC | n/a | `- '--onboard' — opt-in (default OFF) one-shot Serena 'onboarding' bootstrap at Wave 0.7b, run ONLY when 'list_memories' is empty for the project slug. Seeds the cold-start calibration baseli ...` |
| R202 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:92` | serena | --with-hierarchy flag doc | SYM | DEC | n/a | `- '--with-hierarchy' — opt-in (default OFF) enable 'type_hierarchy' transitive supertype/subtype retrieval at §6.1 step 4.5 and Wave 1B.3. Backend-gated: **default OFF on 'lsp' backends** (n ...` |
| R203 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:147-154` | serena | wave outline lines naming Serena steps (0.5c get_current_config, 0.7, 0.7b, 1A) | DOC | DEC | n/a | `0.5c get_current_config probe (active context/modes/version fingerprint)` |
| R204 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:287` | serena | input snapshot is a real git worktree checkout, not an archive, 'so serena/auggie stay indexed' (design constraint set by the Serena/Auggie indexers) | ACT | DEC | archive would also work for native tools | `3. **Snapshot creation (COR-2 / A-2)** — on the committable path, pre-clean a leftover '<output>/_review-snapshot', re-resolve HEAD immediately before 'git worktree add --detach <output>/_re ...` |
| R205 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:252-262` | serena | Step 0.5c: mcp__serena__get_current_config probe, version fingerprint, snapshot yaml | ACT | LB | fail-open: degraded_components + version unknown | `**Step 0.5c (active-project config probe, FR-7).** At Wave 0, invoke 'mcp__serena__get_current_config' once to fingerprint Serena's own active state — a calibration input reflect currently l ...` |
| R206 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:266-282` | serena | Step 0.5d: availability probe (backend, execute_shell_command, onboarding, read_only from .serena/project.yml) | ACT | LB | fail-open | `backend: jetbrains \| lsp \| none # gates FR-1 type_hierarchy step 4.5` |
| R207 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:295-303` | serena | Step 0.7: activate_project + onboarding-status parse + list_memories proxy | ACT | LB | fail-open: onboarding_status unknown | `**Step 0.7 (activate project + memory hydrate + onboarding-status parse, FR-6).** At Wave 0, after 'mcp__serena__activate_project' and memory hydrate, derive whether project memory was boots ...` |
| R208 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:305-314` | serena | Step 0.7b: mcp__serena__onboarding() bootstrap (--onboard only) | ACT | LB | skipped unless --onboard | `**Step 0.7b (onboarding bootstrap, FR-RV3-MED.2).** A one-shot, opt-in cold-start calibration bootstrap. It runs **ONLY when '--onboard' is set AND 'list_memories' returns empty for the proj ...` |
| R209 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:340` | serena | UC-1 step 1a: mcp__serena__find_declaration for diff hunks | SYM | LB | Grep/Glob, degraded | `1a. (FR-2) For each task's diff hunks, resolve each hunk's canonical declaration site via 'mcp__serena__find_declaration' BEFORE deriving touched symbols — this anchors the overlap graph to ...` |
| R210 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:342-343` | serena | UC-1 step 1: mcp__serena__find_symbol per task diff hunk | SYM | LB | Grep/Glob, degraded | `1. For each task in the tasklist, derive its touched symbols via 'mcp__serena__find_symbol' against the task's diff hunks.` |
| R211 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:344` | serena | UC-1 step 3: find_referencing_symbols for overlap edges | REF | LB | Grep/Glob, degraded | `3. For each overlap edge, query 'mcp__serena__find_referencing_symbols' to determine whether the symbol is genuinely shared or just transiently named the same.` |
| R212 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:345` | serena | UC-1 step 3a: type_hierarchy (--with-hierarchy, backend-gated) | SYM | LB | gated off, no degrade | `3a. (FR-RV3-MED.1) When an overlap node is a **shared base-class symbol** flagged as a top-30 hotspot, AND the Wave-0 step 0.5d backend is hierarchy-capable AND '--with-hierarchy' is set, ru ...` |
| R213 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:355` | serena | L4 live-execution prohibition mentions execute_shell_command | DOC | DEC | n/a | `**Live-execution prohibition (L4, read-only reviewer).** A reviewer brief MUST NOT embed live-execution instructions: no "run pytest", no "run 'git diff'", no "compute the baseline test coun ...` |
| R214 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:361` | serena | Step 5.0: probe sc-adversarial existence via mcp__serena__list_memories | MEM | DEC | no-op Skill --help probe named in same line | `**Step 5.0 (sc-adversarial pre-invocation probe and F1/F2/F3 fallback).** Before calling 'Skill sc-adversarial-protocol', probe its existence via 'mcp__serena__list_memories' for the skill's ...` |
| R215 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:383-386` | serena | Wave-6 handoff persist: prepare_for_new_conversation, fallback write_memory | MEM | LB | write_memory; both fail -> task-builder cold start | `2. **Persist (tool-presence-gated, OQ-M1):** if 'prepare_for_new_conversation' is exposed in the active Serena context, write the blob via it (its signature confirmed by a live probe at adop ...` |
| R216 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:389-400` | serena | handoff ordering notes | MEM | DEC | n/a | `**Plan route ('--remediate', no deep) — phases (detail in 'refs/remediation-handoff.md' "Plan route").** Step 6.0 and the FR-8 path emission above do NOT run on this route: 'sc:workflow' has ...` |
| R217 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:500-508` | serena | section 6 heading 'Modern Serena Tool Usage' and rationale | DOC | DEC | n/a | `## 6. Modern Serena Tool Usage` |
| R218 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:509` | serena | chain step 1: mcp__serena__activate_project | ACT | LB | Grep/Glob, degraded | `1. mcp__serena__activate_project (once, idempotent at Wave 0)` |
| R219 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:510-513` | serena | chain steps 2-3b: get_symbols_overview, find_declaration, find_symbol, find_implementations | SYM | LB | Grep/Glob, degraded | `2. mcp__serena__get_symbols_overview <file> # structural map` |
| R220 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:514` | serena | chain step 4: find_referencing_symbols include_info:true | REF | LB | Grep/Glob, degraded | `4. mcp__serena__find_referencing_symbols <symbol> include_info:true # downstream impact + signatures` |
| R221 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:523` | serena | step 4a fallback: inline serena + ripgrep grep-skeleton | SYM | DEC | ripgrep | `Fallback: agent unavailable → inline serena+ripgrep grep-skeleton degrade, findings CAPPED at advisory L2,` |
| R222 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:525` | serena | chain step 4.5: type_hierarchy | SYM | LB | gated off | `4.5. mcp__serena__type_hierarchy(hierarchy_type=both\|subtypes, depth=0) # transitive family (backend+--with-hierarchy gated)` |
| R223 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:526-527` | serena | chain steps 5, 5.5: get_diagnostics_for_file, execute_shell_command (verification triangle) | DIAG | LB | verification_ran:false | `5. mcp__serena__get_diagnostics_for_file <file> # LSP-level issues` |
| R224 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:530` | serena | chain step 7: find_symbol search_deps:true | SYM | LB | skipped | `7. mcp__serena__find_symbol <symbol> search_deps:true # third-party / dependency surface` |
| R225 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:531` | serena | chain step 7': summarize_changes corroboration | DIAG | LB | serena_summary_corroboration:unavailable | `7'. mcp__serena__summarize_changes # UC-2 corroboration vs supplied diff` |
| R226 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:534-565` | serena | explanatory notes for the chain steps | SYM | DEC | n/a | `Step 2a (FR-2) resolves a diff hunk to its canonical declaration site before symbol lookup; on zero matches it emits 'find_declaration_no_match'. Step 3b (FR-1) enumerates the polymorphic su ...` |
| R227 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:567-585` | serena | 6.1.1 execute_shell_command safety envelope (timeout, output cap, denylist) | DIAG | LB | verify_blocked | `### 6.1.1 'execute_shell_command' safety envelope (FR-RV3-MED.4)` |
| R228 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:590-595` | serena | Memory I/O: read_memory last-pass / deviation-patterns, write_memory, prepare_for_new_conversation, list_memories | MEM | LB | degraded: memory_persist_failed | `mcp__serena__read_memory key=reflect/last-pass-{project-slug} # Wave 0 hydrate` |
| R229 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:600-620` | serena | retention sweep: list/delete/rename/edit_memory, slug rules, version gate | MEM | LB | skipped when read-only / version unknown | `**Handoff schema ('reflect/handoff-{slug}-{timestamp}', FR-RV3-MED.3).** A Tier-3 bridge memory written at Wave 5/6 — immediately BEFORE the Wave-6 task-builder handoff — carrying the in-fli ...` |
| R230 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:622-632` | serena | 6.4 think_about_* scripted checkpoints ('not load-bearing' by its own heading) | NUDGE | DEC | checkpoint_logged: skipped | `### 6.4 'think_about_*' as scripted checkpoints (not load-bearing)` |
| R231 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:636` | serena | 'Every Serena call is fail-open' | DOC | DEC | Grep/Glob | `Every Serena call is fail-open per 'sc-validate-roadmap-protocol' convention. Missing Serena → fall back to 'Grep'/'Glob' with 'degraded: true' in the audit. The protocol must never abort be ...` |
| R232 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:747` | serena | contract field onboarding_ran | CONTRACT | LB | n/a | `onboarding_ran: <bool> # FR-2 (Wave 0.7b one-shot --onboard bootstrap; false when gated off)` |
| R233 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:780` | serena | contract field serena_summary_corroboration (read by cli/reflect, tests pin) | CONTRACT | LB | n/a | `serena_summary_corroboration: agree \| partial \| disagree \| unavailable # FR-5` |
| R234 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:862` | serena | contract field handoff_memory_key | CONTRACT | LB | null | `handoff_memory_key: <serena-memory-name> \| null # FR-3 (reflect/handoff-{slug}-{timestamp}; null when no Tier 3)` |
| R235 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:961-992` | serena | telemetry fields: serena_version, serena_active_context, onboarding_*, handoff_persist_*, type_hierarchy_invoked | CONTRACT | LB | n/a | `serena_checkpoints_path: <path>` |
| R236 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1081-1137` | serena | deviation-classification prose citing Serena evidence | DOC | DEC | n/a | `- A 'third_party_api_verified' flag (FR-4): the divergence resolves to a verified external-API constraint — 'find_symbol(search_deps:true)' confirmed the upstream third-party behavior the wo ...` |
| R237 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1348` | serena | grader check checkpoint_logged for scripted Serena checkpoints | NUDGE | DEC | n/a | `- 'checkpoint_logged' — verify 'audit.log' includes a row for a named checkpoint (scripted Serena think-checkpoints, audit-emit per-step).` |
| R238 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1492-1520` | serena | error table: Serena unavailable / tool context-excluded / write_memory fails | DOC | DEC | documented fallbacks | `\| Serena unavailable \| Fall back to Grep/Glob; skip 'get_diagnostics_for_file'; mark 'degraded: ["serena"]' \| Continue \|` |
| R239 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1867-1896` | serena | do/don't lists: modern Serena symbolic chain, per-project Serena memory | DOC | DEC | n/a | `- Use modern Serena symbolic chain ('get_symbols_overview' → 'find_symbol' → 'find_referencing_symbols') for evidence; wire 'think_about_*' as scripted nudges captured to audit, never as the ...` |
| R240 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1950` | serena | grader table row: Serena scripted checkpoints | NUDGE | DEC | n/a | `\| §6.4 Serena scripted checkpoints \| 'checkpoint_logged' \| 'audit.log checkpoint=<name>' \|` |
| R241 | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:1986-2041` | serena | roadmap/posture notes: Serena memory 90-day expiry | MEM | DEC | n/a | `4. **Persistent deviation knowledge graph** — Serena memory stores the last-pass summary. A full deviation graph with deduplication, temporal trending, and cross-project aggregation is a sep ...` |
| R242 | `src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md:118-180` | serena | operator WARN catalog for Serena context/read_only/onboarding conditions | DOC | DEC | n/a | `## Serena-adoption operator WARN catalog (V3-Serena medium)` |
| R243 | `src/superclaude/skills/sc-reflect-protocol/refs/input-resolution.md:81-82` | serena | Wave 0 inputs: Serena activation + memory hydrate; auggie+serena availability | ACT | DEC | n/a | `- Serena project activation + memory hydrate (step 0.7).` |
| R244 | `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:124-130` | serena | rubric weights keyed to Serena probes (config exclusion, onboarding_status, implementors, hierarchy) | DOC | DEC | n/a | `**S_dev_density sub-terms (V3 Serena adoptions).** The threshold semantics above are unchanged — the following are **additive weighting inputs** (not threshold changes) layered onto the comp ...` |
| R245 | `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md:50-83` | serena | taxonomy flags citing find_symbol / get_diagnostics_for_file / execute_shell_command / serena_summary_corroboration | DOC | DEC | n/a | `- A 'third_party_api_verified' flag (FR-4): the divergence resolves to a verified external-API constraint — 'find_symbol(search_deps:true)' confirmed the upstream third-party behavior the wo ...` |
| R246 | `src/superclaude/skills/sc-reflect-protocol/refs/grader-extensions.md:217` | serena | checkpoint_logged semantics for scripted Serena checkpoints | NUDGE | DEC | n/a | `**Semantics.** Read 'audit.log' as JSONL (one event per line, schema '{ts, step, checkpoint, ...}'). Pass when ≥1 row has 'checkpoint == checkpoint_name'. Confirms scripted Serena think-chec ...` |
| R247 | `src/superclaude/skills/sc-reflect-protocol/refs/reviewer-spec.md:14-55` | serena | reviewer brief: no execute_shell_command; hunks derived from find_implementations / find_referencing_symbols / type_hierarchy | DOC | DEC | n/a | `- **No shell execution, no git.** A reviewer runs no 'Bash' / 'execute_shell_command' and no git verbs. Verification (tests/linters/build) is run by the orchestrator at §6.1 step 5.5 and sur ...` |
| R248 | `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:179-232` | serena | handoff key recoverable via read_memory (task-builder/task skills contain no read_memory call: rg) | MEM | DEC | plan route uses remediation-source.md | `# 'read_memory' this key to recover reflect's in-flight rubric` |
| R249 | `src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml:73-74` | serena | cost-profile comment: reuses step-4 find_referencing_symbols, step-5.5 execute_shell_command | DOC | DEC | n/a | `# Adds NO new tool class (reuses step-4 find_referencing_symbols, step-6 re-Read, and the` |
| R250 | `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md:21` | serena | partition find_referencing_symbols results into production vs test evidence | REF | DEC | n/a | `Use this table to partition 'find_referencing_symbols' results into production referrers vs test/comment evidence. Unknown languages or ambiguous comment/test classification yield 'DEGRADE', ...` |
| R251 | `src/superclaude/skills/sc-reflect-protocol/refs/coverage-mapping.md:173-195` | serena | coverage numerators from find_implementations / type_hierarchy | SYM | DEC | n/a | `'find_implementations'. It is added to the UC-1 unmapped numerator above so an` |

### 5.7 Plugin mirror `plugins/superclaude/` (19 rows, one per file; hit lines per file in the concept column)

Each row is a whole-file mirror row. The quoted line is the first hit in the file; the line number after the path is that line. Class is the class of the src twin's main reference. `DIFFERS` means the plugin file is not byte-identical to its src twin (checked with `cmp`); `IDENTICAL` means it is.

| ID | Primitive:line | Server | Tool or concept | Job | Class | Fallback | Quoted line |
|---|---|---|---|---|---|---|---|
| R252 | `plugins/superclaude/agents/pm-agent.md:11` | serena | mirror of src agents/pm-agent.md (32 hit lines) | MEM | LB | IDENTICAL to src | `- **Session Start (MANDATORY)**: ALWAYS activates to restore context from Serena MCP memory` |
| R253 | `plugins/superclaude/commands/brainstorm.md:6` | serena | mirror of commands/brainstorm.md (1 hit line) | ALLOW | DEC | IDENTICAL to src | `mcp-servers: [serena, auggie-mcp, tavily]` |
| R254 | `plugins/superclaude/commands/load.md:3` | serena | mirror of commands/load.md (10 hit lines) | MEM | LB | IDENTICAL to src | `description: "Session lifecycle management with Serena MCP integration for project context loading"` |
| R255 | `plugins/superclaude/commands/pm.md:6` | serena | mirror of commands/pm.md (3 hit lines) | MEM | LB | IDENTICAL to src | `mcp-servers: [context7, playwright, morphllm, serena, tavily]` |
| R256 | `plugins/superclaude/commands/reflect.md:6` | serena | mirror of commands/reflect.md (14 hit lines) | SYM | DEC | DIFFERS from src (82 diff lines) | `mcp-servers: [auggie, serena, context7, tavily]` |
| R257 | `plugins/superclaude/commands/research.md:6` | serena | mirror of commands/research.md (2 hit lines) | MEM | DEC | DIFFERS from src (4 diff lines) | `mcp-servers: [tavily, playwright, serena]` |
| R258 | `plugins/superclaude/commands/save.md:3` | serena | mirror of commands/save.md (11 hit lines) | MEM | LB | IDENTICAL to src | `description: "Session lifecycle management with Serena MCP integration for session context persistence"` |
| R259 | `plugins/superclaude/commands/task.md:7` | serena | mirror of commands/task.md (1 hit line) | ALLOW | DEC | IDENTICAL to src | `mcp-servers: [context7, serena, playwright, morphllm]` |
| R260 | `plugins/superclaude/core/RESEARCH_CONFIG.md:98` | serena | mirror of core/RESEARCH_CONFIG.md (2 hit lines) | MEM | DEC | DIFFERS from src (546 diff lines) | `memory_backend: serena` |
| R261 | `plugins/superclaude/hooks/hooks.json:37` | serena | mirror of hooks/hooks.json (freshness matcher) (1 hit line) | EDIT | LB | DIFFERS from src (29 diff lines) | `"matcher": "Edit\|Write\|mcp__serena__replace_content\|mcp__serena__replace_symbol_body\|mcp__serena__insert_after_symbol\|mcp__serena__insert_before_symbol",` |
| R262 | `plugins/superclaude/mcp/MCP_Morphllm.md:15` | serena | mirror of mcp/MCP_Morphllm.md (3 hit lines) | EDIT | DEC | DIFFERS from src | `- **Over Serena**: For pattern-based edits, not symbol operations` |
| R263 | `plugins/superclaude/mcp/MCP_Serena.md:1` | serena | mirror of mcp/MCP_Serena.md (7 hit lines) | CFG | DEC | DIFFERS from src (2 diff lines) | `# Serena MCP Server` |
| R264 | `plugins/superclaude/mcp/MCP_Tavily.md:29` | serena | mirror of mcp/MCP_Tavily.md (2 hit lines) | MEM | DEC | DIFFERS from src | `- **Serena**: Tavily performs searches → Serena stores research sessions` |
| R265 | `plugins/superclaude/mcp/configs/serena-docker.json:2` | serena | mirror of mcp/configs/serena-docker.json (2 hit lines) | CFG | DEC | IDENTICAL to src | `"serena": {` |
| R266 | `plugins/superclaude/mcp/configs/serena.json:2` | serena | mirror of mcp/configs/serena.json (3 hit lines) | CFG | LB | IDENTICAL to src | `"serena": {` |
| R267 | `plugins/superclaude/modes/MODE_Orchestration.md:25` | serena | mirror of modes/MODE_Orchestration.md (1 hit line) | EDIT | DEC | DIFFERS from src (2 diff lines) | `\| Symbol operations \| Serena MCP \| Manual search \|` |
| R268 | `plugins/superclaude/modes/MODE_Task_Management.md:15` | serena | mirror of modes/MODE_Task_Management.md (bare write_memory/think_about_* calls) (30 hit lines) | MEM | LB | src twin not diffed here | `📋 **Plan** → write_memory("plan", goal_statement)` |
| R269 | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:237` | serena | byte copy of core/HOW-WE-WORK.md required by tests/commands/test_routing_plugin_parity.py (3 hit lines) | MEM | DEC | byte copy of core guide | `'/sc:save' and '/sc:load' store and load Serena project memory. They are not a way to resume work or a guarantee of complete executor state. Other command-owned continuations keep their own ...` |
| R270 | `plugins/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md:28` | serena | mirror of sc-recommend heuristics row (1 hit line) | SYM | DEC | IDENTICAL to src | `\| Repository-wide semantic ranking \| Many Grep/Glob calls \| YES (auggie/serena beats brute Grep) \|` |

## 6. Tool allowlists and settings that name these servers

These must change in Phase 1 (removal) or Phase 3 (swap). `tools:` and `allowed-tools:` are enforced by Claude Code; `mcp-servers:` is metadata with no Python consumer (C13). Computed from frontmatter of every `.md` file in `src/superclaude` and `plugins/superclaude`.

| Primitive:line | Field | Serena entries named | Entries on the line | Body calls them? | Test-pinned |
|---|---|---|---:|---|---|
| `P/commands/brainstorm.md:6` | `mcp-servers` | `serena` (in list) | 3 | n/a (metadata) |  |
| `P/commands/load.md:6` | `mcp-servers` | `serena` (in list) | 1 | n/a (metadata) |  |
| `P/commands/pm.md:6` | `mcp-servers` | `serena` (in list) | 5 | n/a (metadata) |  |
| `P/commands/reflect.md:6` | `mcp-servers` | `serena` (in list) | 4 | n/a (metadata) |  |
| `P/commands/research.md:6` | `mcp-servers` | `serena` (in list) | 3 | n/a (metadata) |  |
| `P/commands/save.md:6` | `mcp-servers` | `serena` (in list) | 1 | n/a (metadata) |  |
| `P/commands/task.md:7` | `mcp-servers` | `serena` (in list) | 4 | n/a (metadata) |  |
| `S/agents/auggie-reviewer.md:5` | `tools` | `mcp__serena__find_symbol`, `mcp__serena__find_referencing_symbols` | 7 | optional (Read alternative) |  |
| `S/agents/reflect-reviewer.md:5` | `tools` | `mcp__serena__find_symbol`, `mcp__serena__find_referencing_symbols`, `mcp__serena__get_symbols_overview`, `mcp__serena__get_diagnostics_for_file` | 8 | no (UNVERIFIED if reviewer calls them) |  |
| `S/agents/reuse-auditor.md:5` | `tools` | `mcp__serena__find_symbol`, `mcp__serena__get_symbols_overview`, `mcp__serena__find_referencing_symbols` | 7 | fallback only |  |
| `S/agents/troubleshoot-analyst.md:5` | `tools` | `mcp__serena__find_symbol`, `mcp__serena__find_referencing_symbols`, `mcp__serena__get_symbols_overview`, `mcp__serena__get_diagnostics_for_file` | 8 | no | tests/troubleshoot/test_diagnostic_worker_contract.py (exact roster) |
| `S/commands/adversarial.md:7` | `mcp-servers` | `serena` (in list) | 2 | n/a (metadata) |  |
| `S/commands/auggie-review.md:6` | `mcp-servers` | `serena` (in list) | 1 | n/a (metadata) |  |
| `S/commands/brainstorm.md:6` | `mcp-servers` | `serena` (in list) | 3 | n/a (metadata) |  |
| `S/commands/cleanup-audit.md:7` | `mcp-servers` | `serena` (in list) | 2 | n/a (metadata) |  |
| `S/commands/cli-eval.md:6` | `mcp-servers` | `serena` (in list) | 2 | n/a (metadata) |  |
| `S/commands/cli-portify.md:7` | `mcp-servers` | `serena` (in list) | 2 | n/a (metadata) |  |
| `S/commands/init-lite.md:7` | `mcp-servers` | `serena` (in list) | 1 | n/a (metadata) |  |
| `S/commands/load.md:6` | `mcp-servers` | `serena` (in list) | 1 | n/a (metadata) |  |
| `S/commands/pm.md:6` | `mcp-servers` | `serena` (in list) | 5 | n/a (metadata) |  |
| `S/commands/post-release.md:7` | `mcp-servers` | `serena` (in list) | 1 | n/a (metadata) |  |
| `S/commands/pr-submit.md:6` | `mcp-servers` | `serena` (in list) | 2 | n/a (metadata) |  |
| `S/commands/reflect.md:6` | `mcp-servers` | `serena` (in list) | 4 | n/a (metadata) |  |
| `S/commands/release-split.md:7` | `mcp-servers` | `serena` (in list) | 2 | n/a (metadata) |  |
| `S/commands/research.md:6` | `mcp-servers` | `serena` (in list) | 3 | n/a (metadata) |  |
| `S/commands/review-translation.md:6` | `mcp-servers` | `serena` (in list) | 3 | n/a (metadata) |  |
| `S/commands/save.md:6` | `mcp-servers` | `serena` (in list) | 1 | n/a (metadata) |  |
| `S/commands/task.md:7` | `mcp-servers` | `serena` (in list) | 4 | n/a (metadata) |  |
| `S/commands/troubleshoot.md:6` | `mcp-servers` | `serena` (in list) | 4 | n/a (metadata) |  |
| `S/commands/validate-roadmap.md:6` | `allowed-tools` | `mcp__serena__read_memory`, `mcp__serena__write_memory`, `mcp__serena__find_symbol`, `mcp__serena__get_symbols_overview`, `mcp__serena__search_for_pattern`, `mcp__serena__activate_project` | 16 | yes via skill, fail-open |  |
| `S/commands/validate-roadmap.md:7` | `mcp-servers` | `serena` (in list) | 2 | n/a (metadata) |  |
| `S/skills/sc-cleanup-audit-protocol/SKILL.md:6` | `mcp-servers` | `serena` (in list) | 2 | n/a (metadata) |  |
| `S/skills/sc-cli-portify-protocol/SKILL.md:7` | `mcp-servers` | `serena` (in list) | 3 | n/a (metadata) |  |
| `S/skills/sc-reflect-protocol/SKILL.md:5` | `allowed-tools` | `mcp__serena__find_symbol`, `mcp__serena__find_referencing_symbols`, `mcp__serena__get_symbols_overview`, `mcp__serena__get_diagnostics_for_file`, `mcp__serena__read_memory`, `mcp__serena__write_memory`, `mcp__serena__list_memories`, `mcp__serena__search_for_pattern`, `mcp__serena__activate_project`, `mcp__serena__get_current_config`, `mcp__serena__find_implementations`, `mcp__serena__find_declaration`, `mcp__serena__delete_memory`, `mcp__serena__rename_memory`, `mcp__serena__edit_memory`, `mcp__serena__summarize_changes`, `mcp__serena__execute_shell_command`, `mcp__serena__onboarding`, `mcp__serena__prepare_for_new_conversation`, `mcp__serena__type_hierarchy` | 33 | yes (section 6 chain, memory I/O) |  |
| `S/skills/sc-troubleshoot-protocol/SKILL.md:4` | `allowed-tools` | `mcp__serena__find_symbol`, `mcp__serena__find_referencing_symbols`, `mcp__serena__get_symbols_overview` | 16 | yes (Tier 1 step 193) |  |
| `S/skills/sc-validate-roadmap-protocol/SKILL.md:4` | `allowed-tools` | `mcp__serena__read_memory`, `mcp__serena__write_memory`, `mcp__serena__find_symbol`, `mcp__serena__get_symbols_overview`, `mcp__serena__search_for_pattern`, `mcp__serena__activate_project` | 16 | yes, fail-open |  |

Other places that name Serena tools as permissions or matchers (C11, plus file reads):

| Location | What | Note |
|---|---|---|
| `S/hooks/hooks.json:47` | PreToolUse matcher `Edit|Write|mcp__serena__replace_content|mcp__serena__replace_symbol_body|mcp__serena__insert_after_symbol|mcp__serena__insert_before_symbol` -> `freshness-pre-edit.sh` | Installed into the user's settings by `superclaude install`; pinned by `tests/cli/test_install_hooks.py`. |
| `P/hooks/hooks.json:37` | same matcher in the plugin copy | DIFFERS from src (older). |
| `~/.claude/settings.json:162` | same matcher, written by the installer | Read-only check. Removing it needs `superclaude install`/`update` logic (W2/W5 domain), not just a source edit. |
| `.claude/settings.json` (repo) | no `mcp__serena`/`mcp__codebase` entries | C11 shows only the two `~/.claude/settings.json` lines. |
| `~/.claude/settings.json` permissions | no allow/deny entry naming `serena` or `codebase-memory` | C11: the only Serena hit is the matcher at line 162. |

## 7. Tests that pin these references

Found with `rg -i -c serena tests` (C9). Only tests that assert on a primitive, a primitive-derived contract or a primitive file list are listed; the other hits are fixtures or false positives and are marked as such. Line numbers are those of the quoted line.

| Test:line | Pins | Primitive affected | Strength | Quoted line |
|---|---|---|---|---|
| `tests/troubleshoot/test_diagnostic_worker_contract.py:22` | TOOLS roster constant (this line to get_diagnostics_for_file, 4 serena names) | agents/troubleshoot-analyst.md:5 | pin: exact | `"mcp__serena__find_symbol",` |
| `tests/troubleshoot/test_diagnostic_worker_contract.py:37` | assert_profile demands the roster equals TOOLS exactly, so removing the serena names from the agent's `tools:` line fails this test until TOOLS is edited | agents/troubleshoot-analyst.md:5 | pin: exact | `assert len(tools) == len(TOOLS) and set(tools) == TOOLS, (` |
| `tests/troubleshoot/test_diagnostic_worker_contract.py:152` | mutation list uses a Serena edit tool as a forbidden-capability example (stays valid, name goes stale) | agents/troubleshoot-analyst.md:5 | stale name only | `"mcp__serena__replace_content",` |
| `tests/cli/test_install_hooks.py:684` | freshness matcher must still contain the four mcp__serena__ edit tools (this line to +3) | hooks/hooks.json:47 | pin: exact | `assert "mcp__serena__replace_content" in matcher_tools` |
| `tests/core/test_how_we_work_routing_table.py:1074` | routing table text for /sc:load must say 'requires Serena' | core/HOW-WE-WORK.md:327 | pin: exact | `assert "requires Serena" in other` |
| `tests/core/test_how_we_work_routing_table.py:1075` | routing table text for /sc:save (the guide line also says 'Requires Serena') | core/HOW-WE-WORK.md:329 | pin: wording around Serena | `assert "writes memory; not durable task execution state" in other` |
| `tests/commands/test_routing_plugin_parity.py:38` | plugin guide copy must stay a byte copy of core/HOW-WE-WORK.md (edit both together) | core/HOW-WE-WORK.md + plugins/.../sc-recommend/refs/HOW-WE-WORK.md | pin: byte parity | `assert filecmp.cmp(_GUIDE, _PLUG_SKILL / "refs/HOW-WE-WORK.md", shallow=False)` |
| `tests/recommend/fixtures/routing_refresh_cases.json:576` | fixture field for /sc:save (whether test_routing_refresh asserts this string: UNVERIFIED) | core/HOW-WE-WORK.md:329 | fixture text | `"side_effects": "Serena memory writes only; not task execution state",` |
| `tests/recommend/fixtures/routing_refresh_cases.json:584` | fixture expectation for the plugin-only /sc:save variant (assertion use UNVERIFIED) | core/HOW-WE-WORK.md:329 | fixture text | `"unavailable_plugin": {"environment": "plugin-only", "missing": "sc:save", "expected": "not installed: sc:save; Serena prerequisite disclosed"},` |
| `tests/sc-roadmap/conftest.py:14` | skill_md_content fixture source path (falls back to installed copy, skips if absent) | skills/sc-roadmap-protocol/SKILL.md | fixture | `SKILL_MD_PATH = os.path.join(` |
| `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py:79` | HARD pin: sc-roadmap SKILL.md must contain the word Serena/serena | skills/sc-roadmap-protocol/SKILL.md:13,325,414 | pin: exact | `assert "Serena" in skill_md_content or "serena" in skill_md_content` |
| `tests/sc-roadmap/compliance/test_mcp_circuit_breakers.py:33` | weak pin: passes on the word 'fallback' or 'circuit' anywhere in the skill | skills/sc-roadmap-protocol/SKILL.md:419 | pin: weak | `def test_serena_fallback(self, skill_md_content):` |
| `tests/sc-roadmap/integration/test_wave5_completion.py:71` | weak pin: passes on 'write_memory' or the word 'memory' | skills/sc-roadmap-protocol/SKILL.md:325 | pin: weak | `def test_memory_persistence_in_skill_md(self, skill_md_content):` |
| `tests/sc-roadmap/integration/test_wave5_completion.py:77` | weak pin: passes on 'circuit' or 'fallback' | skills/sc-roadmap-protocol/SKILL.md:419 | pin: weak | `def test_circuit_breaker_for_serena(self, skill_md_content):` |
| `tests/unit/test_cli_install.py:150` | expected installed file list for the mcp component names MCP_Serena.md (plus lines +3 for configs/serena*.json) | mcp/MCP_Serena.md, mcp/configs/serena*.json | pin: file list | `MCP_Playwright.md MCP_Serena.md MCP_Tavily.md __init__.py configs/__init__.py` |
| `tests/unit/test_cli_install.py:423` | second expected file list (plugin/no-Auggie variant) names MCP_Serena.md (+2 lines for configs) | mcp/MCP_Serena.md, mcp/configs/serena*.json | pin: file list | `MCP_Context7.md MCP_Morphllm.md MCP_Playwright.md MCP_Serena.md MCP_Tavily.md` |
| `tests/cli/test_install_mcp_registry.py:13` | registry command pin for the serena server (W2 owns the installer side) | mcp/configs/serena.json | pin: exact | `"serena": (` |
| `tests/cli/test_install_mcp_registry.py:45` | template args pin for configs/serena.json | mcp/configs/serena.json | pin: exact | `"serena.json": [` |
| `tests/cli/reflect/test_verdict_mapping.py:93` | reflect contract: degraded_components containing 'serena' maps to exit 11 | skills/sc-reflect-protocol/SKILL.md:961-992 (contract) | pin: exact | `def test_degraded_serena() -> None:` |
| `tests/cli/reflect/test_verdict_mapping.py:193` | reflect contract field serena_summary_corroboration | skills/sc-reflect-protocol/SKILL.md:780 | pin: exact | `def test_serena_summary_corroboration_unavailable_not_degraded() -> None:` |
| `tests/cli/reflect/test_verdict_mapping.py:245` | reflect contract degraded component name | skills/sc-reflect-protocol/SKILL.md:301 | pin: exact | `"serena:onboarding-parse",` |
| `tests/cli/reflect/test_runner_e2e.py:71` | end-to-end reflect run uses the degraded_serena fixture | reflect contract | pin: exact | `factory = make_claude_process_stub("degraded_serena.yaml", rc=0)` |
| `tests/cli/eval/test_coverage_gate.py:127` | uses a Serena tool name as an example of a non-matching tool (stale name only) | none | stale name only | `spec = _spec("E1", "mcp__serena__find_symbol")` |
| `tests/skills/test_implement_severity_replay.py:192` | 'serena' is just a finding label in a replay fixture (false positive, no change) | none | false positive | `R_A4 = [fnd("serena", origin="fix-induced"), fnd("row2"), fnd("wording", cosmetic=True)]` |

Also pinned through fixtures: 25 YAML files under `tests/cli/reflect/fixtures/` contain the word serena (`serena_summary_corroboration` field or `degraded_components: [serena]`), consumed by the reflect CLI contract tests above. `tests/troubleshoot/fixtures/regression/sysbox-20260918/Fable-D3/REPORT.md:17` and `:56` are historical report text (no change needed).

Tests that pin codebase-memory against primitives: none. Files in `tests/` that mention codebase-memory (`rg -i -l 'codebase.?memory|search_graph|trace_path' tests`): tests/cli/test_install_mcp_registry.py tests/cli/test_install_codebase_memory.py tests/cli/test_install_mcp_tavily.py tests/cli/test_update_command.py All are installer/CLI tests, W1's domain.

## 8. Installed ~/.claude (read-only check)

- Serena in installed primitives: counts by area are in C8 (they mirror `src/`, because `superclaude install` copied them).
- Installed items that are not in `src/superclaude` (C10): see the C10 output above. The extras are three Orca skills (`computer-use`, `orca-cli`, `orchestration`) and the hook script `session-init.sh`. C10b shows the three skills mention neither Serena nor codebase-memory, C8 shows `~/.claude/hooks` has 0 Serena lines and C6 shows 0 codebase-memory lines across skills, agents, hooks and commands; no extra name contains codebase, graph, cbm or memory. Conclusion: **no primitives were added by the upstream codebase-memory installer under `~/.claude/{skills,agents,hooks,commands}`** (UNVERIFIED for `~/.codex` and `~/.config/opencode`: C12 shows no `codebase-memory` text there, but their layout was not walked).
- `~/.claude/CLAUDE.md:21` carries the MCP table row `| serena | Symbol navigation, project memory | --serena |` and `~/.claude/CLAUDE.md:112` the refresh-tool row naming `mcp__serena__find_symbol` / `find_referencing_symbols`. Both are copies of `S/core/CLAUDE.md:21` and `:112` (rows R026 and R028). `rg -n -e '--serena' src/superclaude/{skills,commands,agents,core,hooks,mcp,templates} plugins/superclaude ~/.claude/*.md` returns only the two copies of line 21.
- Installed hook script `~/.claude/hooks/freshness-pre-edit.sh` is byte-identical to `S/hooks/scripts/freshness-pre-edit.sh` (`cmp`).

## 9. Out of scope pointers (not primitives; other workers own them)

- Installer/CLI code and docs: C14 lists the Serena-bearing files in `src/superclaude/cli` (including `cli/reflect/contract.py`, `ensemble.py`, `config.py`, which parse the reflect contract fields listed in section 5 as CONTRACT rows, and `cli/eval/suites/real.yaml` with the most hits). W1 and W2 inventory those.
- Docs (`docs/`, `README.md`, `CLAUDE.md`, `SECURITY.md`) and the rest of `tests/`: W1 and W2.
- `scripts/build_superclaude_plugin.py` builds `dist/plugins/superclaude` from src (Makefile `build-plugin`); how the tracked `plugins/superclaude/` tree is refreshed from it was not traced (UNVERIFIED). Phase 1 should edit `plugins/superclaude/` directly or regenerate it, and then re-run `tests/commands/test_routing_plugin_parity.py`.

## Decisions

No mid-level or architectural decision arose, so no adversarial run was needed. Autonomous choices made while building the map (method: self):

| Decision | Options considered | Method | Rationale |
|---|---|---|---|
| Count bare Serena tool names (no word 'Serena') as references | name-only search vs name plus tool-name search | self | Several workflows (MODE_Task_Management, PM protocol, /sc:save) depend on Serena memory tools without naming Serena; a name-only map would miss them. |
| Treat a Serena step as decorative when the same place names a native fallback tier | always load-bearing vs decorative-when-native-tier-exists | self | Keeps the load-bearing set to things that actually lose capability. The fallback column preserves the information. |
| One whole-file row per `plugins/superclaude` file | one row per hit line vs one row per file | self | The plugin files are copies of src files; per-line rows would duplicate 64 hit lines without new information. Job counts use src rows only. |
| Mark `mcp-servers:` frontmatter decorative | load-bearing vs decorative | self | No Python consumer (C13). Claude Code behaviour for this field is UNVERIFIED, so Phase 1 should still strip it (it is harmless to remove). |

