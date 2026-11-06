---
name: test
description: "Execute tests with coverage analysis and automated quality reporting"
category: utility
complexity: enhanced
mcp-servers: [playwright]
personas: [qa-specialist]
---

# /sc:test - Testing and Quality Assurance

## Triggers

- Test execution requests for unit, integration, or e2e tests
- Coverage analysis and quality gate validation needs
- Continuous testing and watch mode scenarios
- Test failure analysis and debugging requirements

## Usage

```
/sc:test [target] [--type unit|integration|e2e|all] [--coverage] [--watch] [--fix]
/sc:test [target] [--output <file>] [--unattended] [--report-dir <dir>]
```

`--output <file>` writes the test and coverage summary to that file. A standalone run writes a file only when you pass it.

## Behavioral Flow

1. **Discover**: Categorize available tests using runner patterns and conventions
2. **Configure**: Set up appropriate test environment and execution parameters
3. **Execute**: Run tests with monitoring and real-time progress tracking
4. **Analyze**: Generate coverage reports and failure diagnostics
5. **Report**: Provide actionable recommendations and quality metrics

Key behaviors:

- Auto-detect test framework and configuration
- Generate comprehensive coverage reports with metrics
- Activate Playwright MCP for e2e browser testing
- Provide intelligent test failure analysis
- Support continuous watch mode for development

## MCP Integration

- **Playwright MCP**: Auto-activated for `--type e2e` browser testing
- **QA Specialist Persona**: Activated for test analysis and quality assessment
- **Enhanced Capabilities**: Cross-browser testing, visual validation, performance metrics

## Tool Coordination

- **Bash**: Test runner execution and environment management
- **Glob**: Test discovery and file pattern matching
- **Grep**: Result parsing and failure analysis
- **Write**: Coverage reports and test summaries

## Key Patterns

- **Test Discovery**: Pattern-based categorization → appropriate runner selection
- **Coverage Analysis**: Execution metrics → comprehensive coverage reporting
- **E2E Testing**: Browser automation → cross-platform validation
- **Watch Mode**: File monitoring → continuous test execution

## Examples

### Basic Test Execution

```
/sc:test
# Discovers and runs all tests with standard configuration
# Generates pass/fail summary and basic coverage
```

### Targeted Coverage Analysis

```
/sc:test src/components --type unit --coverage
# Unit tests for specific directory with detailed coverage metrics
```

### Browser Testing

```
/sc:test --type e2e
# Activates Playwright MCP for comprehensive browser testing
# Cross-browser compatibility and visual validation
```

### Development Watch Mode

```
/sc:test --watch --fix
# Continuous testing with automatic simple failure fixes
# Real-time feedback during development
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:test` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/test-report.md`, holding the coverage and test summary. `artifacts` lists every other file the run wrote; paths git ignores are left out (WC-4; typically coverage output such as `htmlcov/`, `.coverage`, `coverage.xml` and `.pytest_cache/`), and the test report names where they were written; it is `[]` when nothing else listable was written. A failing suite is a verdict in that report and the run still ends succeeded; it ends failed only when no test runner could run.
- **Person-mode flags.** `--watch` is refused before any work, because it never ends (contract `worker_status: failed`, the flag in `reason`).
- **Gates.** There is no other gate. `--fix` is the caller's consent for non-destructive fixes only; a destructive change to a test file (the rule "without explicit permission") is never made under `--unattended`.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Execute existing test suites using project's configured test runner
- Generate coverage reports and quality metrics
- Provide intelligent test failure analysis with actionable recommendations

**Will Not:**

- Generate test cases or modify test framework configuration
- Execute tests requiring external services without proper setup
- Make destructive changes to test files without explicit permission
