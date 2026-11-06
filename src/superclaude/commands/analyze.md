---
name: analyze
description: "Comprehensive code analysis across quality, security, performance, and architecture domains"
category: utility
complexity: basic
mcp-servers: []
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

1. **Discover**: Categorize source files using language detection and project analysis
2. **Scan**: Apply domain-specific analysis techniques and pattern matching
3. **Evaluate**: Generate prioritized findings with severity ratings and impact assessment
4. **Recommend**: Create actionable recommendations with implementation guidance
5. **Report**: Present comprehensive analysis with metrics and improvement roadmap

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

## Key Patterns

- **Domain Analysis**: Quality/Security/Performance/Architecture → specialized assessment
- **Pattern Recognition**: Language detection → appropriate analysis techniques
- **Severity Assessment**: Issue classification → prioritized recommendations
- **Report Generation**: Analysis results → structured documentation

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
