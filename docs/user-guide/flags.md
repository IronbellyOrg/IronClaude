# IronClaude Flags Guide 🏁

**Flags do not activate automatically.** No keyword or pattern matching runs in code, and mode files under `src/superclaude/modes/` are not installed or loaded automatically. A mode flag such as `--brainstorm` is a hint Claude may honour. Where this page says a flag "auto-activates" or lists "Auto-Triggers", it describes when Claude is guided to apply it from your request, not code that switches it on.

Most flags on this page are hints Claude may honour; the System Flags section lists real `superclaude` terminal options. A command's own options are defined in its file under `~/.claude/commands/sc/` (listed in the [Commands Reference](commands.md)); a flag that a command does not list may be ignored or rejected, so check there before passing one.

## Essential Auto-Activation Flags (90% of Use Cases)

Since 5.0.0 `FLAGS.md` and `MODES.md` are no longer shipped, and old copies left in `~/.claude/` are not loaded. The only hint flags an installed file still names are `--c7`, `--tavily` and `--play`, listed as advisory flags in the MCP table of the shipped `~/.claude/CLAUDE.md`. No installed file defines the other hint flags in this section or in Advanced Control Flags; Claude knows them only if you explain them in your request.

### Core Analysis Flags

| Flag | When Activated | What It Does |
|------|---------------|--------------|
| `--think` | 5+ files OR complex analysis | Standard structured analysis |
| `--think-hard` | Architectural analysis, system dependencies | Deep analysis with enhanced tools |
| `--ultrathink` | Critical system redesign, legacy modernization | Maximum depth analysis with all tools |

### MCP Server Flags

| Flag | Server | Purpose | Auto-Triggers |
|------|---------|---------|---------------|
| `--c7` / `--context7` | Context7 | Official docs, framework patterns | Library imports, framework questions |
| `--play` / `--playwright` | Playwright | Browser testing, E2E validation | Testing requests, visual validation |
| `--tavily` | Tavily | Web search, real-time info | Web search requests, research queries |
| `--morph` / `--morphllm` | Morphllm | Bulk transformations, pattern edits | Bulk operations, style enforcement |
| (no flag) | codegraph | Symbols, callers, impact and file outlines of the indexed worktree | Used automatically for symbol, caller and impact questions; `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` switches it off in commands, skills and agents |

`--morph` is not in the MCP table of the shipped `~/.claude/CLAUDE.md`; Morphllm is an optional server you install with `superclaude mcp --servers morphllm-fast-apply` (needs `MORPH_API_KEY`).

### Behavioral Mode Flags

| Flag | When Activated | What It Does |
|------|---------------|--------------|
| `--brainstorm` | Vague requests, exploration keywords | Collaborative discovery mindset |
| `--introspect` | Self-analysis, error recovery | Expose reasoning process with transparency |
| `--task-manage` | >3 steps, complex scope | Orchestrate through delegation |
| `--orchestrate` | Multi-tool operations, performance needs | Optimize tool selection and parallel execution |
| `--token-efficient` / `--uc` / `--ultracompressed` | Context >75%, efficiency needs | Symbol-enhanced communication (token savings not measured) |

### Execution Control Flags

| Flag | When Activated | What It Does |
|------|---------------|--------------|
| `--loop` | "improve", "polish", "refine" keywords | Iterative enhancement cycles |
| `--safe-mode` | Production, >85% resource usage | Maximum validation, conservative execution |
| `--validate` | Risk >0.7, production environment | Pre-execution risk assessment |
| `--delegate [auto\|files\|folders]` | >7 directories OR >50 files | Sub-agent parallel processing |

## Command-Specific Flags

### Analysis Command Flags (`/sc:analyze`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--focus` | Target specific domain | `security`, `performance`, `quality`, `architecture` |
| `--depth` | Analysis thoroughness | `quick`, `deep` |
| `--format` | Output format | `text`, `json`, `report` |

### Build Command Flags (`/sc:build`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--type` | Build configuration | `dev`, `prod`, `test` |
| `--clean` | Clean before build | Boolean |
| `--optimize` | Enable optimizations | Boolean |
| `--verbose` | Detailed output | Boolean |

### Design Command Flags (`/sc:design`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--type` | Design target | `architecture`, `api`, `component`, `database` |
| `--format` | Output format | `diagram`, `spec`, `code` |

### Explain Command Flags (`/sc:explain`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--level` | Complexity level | `basic`, `intermediate`, `advanced` |
| `--format` | Explanation style | `text`, `examples`, `interactive` |
| `--context` | Domain context | Any domain (e.g., `react`, `security`) |

### Improve Command Flags (`/sc:improve`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--type` | Improvement focus | `quality`, `performance`, `maintainability`, `style` |
| `--safe` | Conservative approach | Boolean |
| `--interactive` | User guidance | Boolean |

### Task Command Flags (`/sc:task`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--strategy` | Task approach | `systematic`, `agile`, `enterprise` |
| `--parallel` | Parallel execution | Boolean |
| `--delegate` | Sub-agent coordination | Boolean |

### Workflow Command Flags (`/sc:workflow`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--strategy` | Workflow approach | `systematic`, `agile`, `enterprise` |
| `--depth` | Analysis depth | `quick`, `standard`, `deep` |
| `--handoff` | Next command | `none`, `design`, `implement`, `tasklist` |

`--output` is retired (`E-LEGACY`): plans are always written to a new `.dev/tasks/to-do/TASK-WF-…/` package.

### Troubleshoot Command Flags (`/sc:troubleshoot`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--type` | Issue category | `bug`, `build`, `performance`, `deployment`, `security`, `test` |
| `--fix` | After a diagnosis, offers a remediation plan (`/sc:workflow` → you run `/sc:implement`; an MDTM task file for `/task` with `--depth deep`); never applies fixes itself | Boolean |

### Cleanup Command Flags (`/sc:cleanup`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--type` | Cleanup target | `code`, `imports`, `files`, `all` |
| `--safe` / `--aggressive` | Cleanup intensity | Boolean |
| `--interactive` | User guidance | Boolean |

### Index Command Flags (`/sc:index`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--type` | Index target | `docs`, `api`, `structure`, `readme` |
| `--format` | Output format | `md`, `json`, `yaml` |

### Reflect Command Flags (`/sc:reflect`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--mode` | Reflection mode | `pre` (UC-1 coverage/gap audit), `post` (UC-2 deviation audit); auto-detected if omitted |
| `--spec` | Driving spec/PRD/objectives doc | Path — **required for `--mode pre`** |
| `--tasklist` | Tasklist file | Path — **strongly recommended for `--mode post`** (does not STOP if omitted) |
| `--diff` | Completed work to audit | Git ref (e.g. `HEAD~1..HEAD`) or diff file — **required for `--mode post`** (unless `--task-log`) |
| `--task-log` | Completed work to audit | Path — UC-2 alternative to `--diff` (satisfies the `--mode post` input requirement when no diff is available) |
| `--depth` | Tier control | `quick` (Tier 1 only), `standard` (default), `deep` (force Tier 2) |
| `--tier` | Explicit tier pin | `1`, `2`, `auto` (default) |
| `--reviewers` | Tier 2 reviewer count | `2`–`3` (default `3`) |
| `--output` | Output directory | Path (default `.dev/reflect/<mode>-<slug>-<ts>/`); MUST NOT be under `.claude/skills,agents,commands/` |
| `--no-promote` | Suppress UC-2 Wave 7 promotion mutation | Boolean (UC-2 default-on) |
| `--remediate` | Offer the Tier 3 remediation chain after the audit | Boolean |
| `--no-verify` | Disable the UC-2 verification triangle (scoped tests/linters/type-checkers/build) | Boolean (UC-2 default-on) |

> This table lists the most-used flags. For the full surface (promotion controls, `--coverage-floor`, tier pins, MCP toggles, etc.) read `~/.claude/commands/sc/reflect.md` or see the `/sc:reflect` command reference.

**CLI wrapper:** The `superclaude reflect run` CLI wrapper layers auto-fix flags on top of this skill surface — `--fix/--no-fix`, `--max-fix-iterations`, and `--base` — and flips `--promote` on by default. See [docs/guides/reflect-cli-tools-guide.md](../guides/reflect-cli-tools-guide.md) for the full CLI surface.

**Legacy grammar (preserved for `/sc:troubleshoot` Wave 6 and other v1 callers):**

| Flag | Purpose | Maps to |
|------|---------|---------|
| `--type task --analyze` | Pre-execution analysis audit | `--mode pre` |
| `--type task --validate` | Post-execution validation audit | `--mode post` |

### Spawn Command Flags (`/sc:spawn`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--strategy` | Coordination approach | `sequential`, `parallel`, `adaptive` |
| `--depth` | Analysis depth | `normal`, `deep` |

### Git Command Flags (`/sc:git`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--smart-commit` | Generate commit message | Boolean |
| `--interactive` | Guided operations | Boolean |

### Test Command Flags (`/sc:test`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--coverage` | Include coverage | Boolean |
| `--type` | Test type | `unit`, `integration`, `e2e` |
| `--watch` | Watch mode | Boolean |

### Impact Command Flags (`/sc:impact`)

| Flag | Purpose | Values |
|------|---------|--------|
| `<symbol>...` | Symbols to report on | 1-30 bare names; either symbols or `--diff`, never both |
| `--diff [<base>]` | Report on the symbols a diff touches | Git ref; `HEAD` when given without a value |
| `--depth` | Transitive impact depth | `1`-`3` (default `2`) |
| `--limit` | Caller rows per symbol | `1`-`100` (default `20`) |
| `--tests` | Add an advisory test list | Boolean |
| `--test-depth` | Test search depth (only with `--tests`) | `1`-`5` |
| `--output-dir` | Where `impact.md` and `return-contract.yaml` go | Path (default `.dev/impact/<slug>-<timestamp>/`) |
| `--caller` | Name of the calling skill; shortens chat output | Name |

### Graph Command Flags (`/sc:graph`)

| Flag | Purpose | Values |
|------|---------|--------|
| `status` \| `init` | What to do | `status` (default) reports readiness; `init` indexes this worktree, only when you type it |
| `--worktree-local` | Build a nested worktree's own index | Boolean, only with `init` |
| `--output-dir` | Also write `return-contract.yaml` there | Path |

### PR Submit Command Flags (`/sc:pr-submit`)

| Flag | Purpose | Values |
|------|---------|--------|
| `--monitor` | Autonomy ceiling | `0` (open the PR only), `1`, `2`, `3` (default `3`) |
| `--pr` | Attach to an existing PR instead of opening one | PR number |
| `--resume` | Rebuild state from a run log | Path to `monitor-run-<N>.jsonl` |
| `--max-rounds` | Remediation cycles | Number (default `2`, hard cap `5`) |
| `--head` / `--base` / `--title` / `--body` | PR details | Branch names, text |

`--yes` was removed from `/sc:pr-submit` in 5.0.0 (it was accepted but never read).

## Advanced Control Flags

Like the flags at the top of this page, the flags under Scope and Focus and Execution Control are hints Claude may honour, not options every command accepts. No installed file defines them since 5.0.0 (`FLAGS.md` is no longer shipped and an old copy in `~/.claude/` is not loaded), so Claude knows them only if you explain them. Check a command's own entry in the [Commands Reference](commands.md) before passing one. The System Flags further down are different: System Flags are options of the `superclaude` command (run in a terminal), not slash-command flags; the table names the command or subcommand for each.

### Scope and Focus

| Flag | Purpose | Values |
|------|---------|--------|
| `--scope` | Analysis boundary | `file`, `module`, `project`, `system` |
| `--focus` | Domain targeting | `performance`, `security`, `quality`, `architecture`, `accessibility`, `testing` |

### Execution Control

| Flag | Purpose | Values |
|------|---------|--------|
| `--concurrency [n]` | Control parallel ops | 1-15 |
| `--iterations [n]` | Improvement cycles | 1-10 |
| `--all-mcp` | Enable all MCP servers | Boolean |
| `--no-mcp` | Native tools only | Boolean |
| `--frontend-verify` | UI testing, frontend debugging, layout validation | Enable Playwright + Chrome DevTools |

### System Flags (`superclaude` terminal command)

| Flag | Command | Purpose |
|------|---------|---------|
| `--version` | `superclaude --version` | Show the installed version |
| `--help` | `superclaude --help`, or `superclaude <subcommand> --help` | Show the options of the command or subcommand |
| `--verbose` | `superclaude doctor --verbose` | Show detailed diagnostic information |
| `--dry-run` | `superclaude mcp --dry-run`, `superclaude sprint run ... --dry-run` | Show what would happen without doing it |
| `--force` | `superclaude install --force`, `superclaude install-skill <name> --force` | Reinstall even if the files already exist. `install --force` is required for the 5.0.0 upgrade, because a plain `install` skips existing files; it overwrites edited core files, commands and agents in `~/.claude/` without a backup and re-copies skill folders |
| `--list` | `superclaude install --list` | List the framework components without installing |
| `--resume <task_id>` | `superclaude sprint run ... --resume <task_id>` | Resume from a task id, skipping tasks that already passed |
| `--task-parallelism K` | `superclaude sprint run ... --task-parallelism K` | Run K tasks of a phase at once (default `1`, sequential) |
| `--handoff` / `--no-handoff` | `superclaude sprint run ...` | Turn per-task handoff records on (default) or off |
| `--yes` / `-y` | `superclaude sprint run ... --yes`, `superclaude sprint rerun-tasks ... --yes` | Answer yes to the sprint confirmation prompts; on `sprint run` it allows non-interactive auto-resume (also `CI=1` or `SUPERCLAUDE_SPRINT_ASSUME_YES=1`) |

## Flag Interactions

### Compatible Combinations

- `--think` + `--c7`: Analysis with documentation
- `--safe-mode` + `--validate`: Maximum safety
- `--loop` + `--validate`: Iterative improvement with validation

### Conflicting Flags

- `--all-mcp` vs individual MCP flags (use one or the other)
- `--no-mcp` vs any MCP flags (--no-mcp wins)
- `--safe` vs `--aggressive` (cleanup intensity)

### Hint Relationships (not automatic)

- `--safe-mode`: Claude is asked to also apply `--uc` and `--validate`
- `--ultrathink`: Claude is asked to also use all MCP servers
- `--think-hard`: Claude is asked to also apply `--c7`

## Troubleshooting Flags

### Common Issues

- **Too many tools**: Use `--no-mcp` to test with native tools only
- **Operation too slow**: Add `--uc` to compress output
- **Validation blocking**: Use `--validate` instead of `--safe-mode` in development
- **Context pressure**: Ask for `--token-efficient` output (nothing switches it on automatically)

### Debug Flags

```bash
/sc:analyze . --depth deep                   # Deeper analysis pass (an option /sc:analyze defines)
/sc:reflect --mode pre --spec docs/spec.md --tasklist <plan> --tier 1   # Quick Tier-1 coverage second opinion
```

### Quick Fixes

```bash
# Options for one command: read ~/.claude/commands/sc/<name>.md (slash commands have no --help flag)
/sc:analyze . --no-mcp                       # Native execution only
```

## Flag Priority Rules

1. **Safety First**: `--safe-mode` > `--validate` > optimization flags
2. **Explicit Override**: User flags > auto-detection
3. **Depth Hierarchy**: `--ultrathink` > `--think-hard` > `--think`  
4. **MCP Control**: `--no-mcp` overrides all individual MCP flags
5. **Scope Precedence**: system > project > module > file

## Related Resources

- [Commands Guide](commands.md) - Commands that use these flags
- [MCP Servers Guide](mcp-servers.md) - Understanding MCP flag activation
- [Session Management](session-management.md) - Using flags with persistent sessions
