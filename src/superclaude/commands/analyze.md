---
name: analyze
description: "Comprehensive code analysis across quality, security, performance, and architecture domains"
category: utility
complexity: basic
mcp-servers: [codegraph]
personas: []
---

# /sc:analyze - Code Analysis and Quality Assessment

## Triggers

- Code quality assessment requests for projects or specific components
- Security vulnerability scanning and compliance validation needs
- Performance bottleneck identification and optimization planning
- Architecture review and technical debt assessment requirements

## Usage

```
/sc:analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep] [--format text|json|report]
/sc:analyze [target] [--output <file>] [--unattended] [--report-dir <dir>]
```

`--output <file>` writes the report to that file. A standalone run writes a file only when you pass it.

## Behavioral Flow

Before step 1, run the codegraph readiness check exactly once per run, as section 2 of `~/.claude/CODEGRAPH.md` describes. Keep `index_state`, `access`, `checked_at` and `worktree_root` for the whole run and do not repeat the check. Below, "`index_state: fresh`" means `index_state: fresh` with `access: mcp` (the lookup tools are listed); with `access: cli` or `access: none` every step stays on Glob, Grep and Read, and no codegraph tool, including `codegraph_files`, is called.

1. **Discover**: Categorize source files using language detection and project analysis. When `index_state: fresh`, first call `codegraph_files {format:"grouped", maxDepth:2}` for the layout and `codegraph_search` to locate the target's symbols
2. **Scan**: Apply domain-specific analysis techniques and pattern matching. When `index_state: fresh`, first call `codegraph_node` (symbol body with `includeCode:true`, file outline with `symbolsOnly:true`), `codegraph_callers` and `codegraph_callees` for call paths (security: entry points to sinks; performance: hot-path callers)
3. **Evaluate**: Generate prioritized findings with severity ratings and impact assessment. When `index_state: fresh`, use `codegraph_impact` and `codegraph_callers` as dependency and blast-radius evidence for architecture and quality findings (dead-code candidates are leads only)
4. **Recommend**: Create actionable recommendations with implementation guidance
5. **Report**: Present comprehensive analysis with metrics and improvement roadmap, with one line `Codegraph: index_state=<state>, checked_at=<UTC>; degraded: <graph:* tokens or none>` (a missing or stale graph leaves the run succeeded once the report is written)

Key behaviors:

- Multi-domain analysis combining static analysis and heuristic evaluation
- Intelligent file discovery and language-specific pattern recognition
- Severity-based prioritization of findings and recommendations
- Comprehensive reporting with metrics, trends, and actionable insights

## Tool Coordination

- **Glob**: File discovery and project structure analysis
- **Grep**: Pattern analysis and code search operations
- **Read**: Source code inspection and configuration analysis
- **Bash**: External analysis tool execution and validation
- **Write**: Report generation and metrics documentation
- **codegraph** (`mcp__codegraph__codegraph_status` once; then `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`): used only when `index_state: fresh`, always before the matching Glob/Grep/Read step, which stays the floor

## Key Patterns

- **Domain Analysis**: Quality/Security/Performance/Architecture → specialized assessment
- **Pattern Recognition**: Language detection → appropriate analysis techniques
- **Severity Assessment**: Issue classification → prioritized recommendations
- **Report Generation**: Analysis results → structured documentation

## Codegraph (optional)

Full rules: `~/.claude/CODEGRAPH.md` (read it when you use codegraph). This section is the short form for `/sc:analyze`.

- **Readiness**: the single check named before step 1 of the Behavioral Flow; never repeat it. `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` means `graph:disabled`.
- **Use only when `index_state: fresh` and `access: mcp`.** Otherwise continue on Glob, Grep and Read, add the matching `graph:*` token to the report's Codegraph line, and go on: never halt, never ask. A missing, stale or failing graph never fails the run (it is succeeded once the report is written).
- **Leads, not citations**: re-Read a `file:line` before citing it; an empty result is not a "no callers" finding; caller rows give the definition line, so confirm the call site (guide section 5) before citing; a caller list shorter than its total is `graph:truncated`.
- **Read-only**: never run `codegraph init`, `index`, `sync`, `explore` or `context`.
- **Names**: exact tool names `mcp__codegraph__codegraph_<tool>`, with `projectPath` set to `worktree_root` on every call.
- **Subagents** (if the run fans out): the brief carries `index_state`, `checked_at` and `worktree_root`; they call codegraph only when `index_state: fresh`.

## Examples

### Comprehensive Project Analysis

```
/sc:analyze
# Multi-domain analysis of entire project
# Generates comprehensive report with key findings and roadmap
```

### Focused Security Assessment

```
/sc:analyze src/auth --focus security --depth deep
# Deep security analysis of authentication components
# Vulnerability assessment with detailed remediation guidance
```

### Performance Optimization Analysis

```
/sc:analyze --focus performance --format report
# Performance bottleneck identification
# Generates HTML report with optimization recommendations
```

### Quick Quality Check

```
/sc:analyze src/components --focus quality --depth quick
# Rapid quality assessment of component directory
# Identifies code smells and maintainability issues
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:analyze` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/analyze-report.md` when `--output` is absent. The run is succeeded when the report is written, and failed otherwise.
- **Gates.** There is no gate, and no person-mode flag. Under `--unattended` consent is never given: the rule "without explicit user consent" is not answered by assuming consent, so the command still modifies no source.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Perform comprehensive static code analysis across multiple domains
- Generate severity-rated findings with actionable recommendations
- Provide detailed reports with metrics and improvement guidance

**Will Not:**

- Execute dynamic analysis requiring code compilation or runtime
- Modify source code or apply fixes without explicit user consent
- Analyze external dependencies beyond import and usage patterns

**Output**: Analysis report containing:

- Severity-rated findings
- Code quality metrics
- Security vulnerabilities
- Performance issues
- Recommendations

**Next Step**: After review, use `/sc:improve` to apply recommended fixes or `/sc:cleanup` for dead code removal.
