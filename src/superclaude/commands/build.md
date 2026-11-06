---
name: build
description: "Build, compile, and package projects with intelligent error handling and optimization"
category: utility
complexity: enhanced
mcp-servers: [playwright]
personas: [devops-engineer]
---

# /sc:build - Project Building and Packaging

## Triggers

- Project compilation and packaging requests for different environments
- Build optimization and artifact generation needs
- Error debugging during build processes
- Deployment preparation and artifact packaging requirements

## Usage

```
/sc:build [target] [--type dev|prod|test] [--clean] [--optimize] [--verbose]
/sc:build [target] [--output <file>] [--unattended] [--report-dir <dir>]
```

`--output <file>` writes the build report to that file. A standalone run writes a file only when you pass it.

## Behavioral Flow

1. **Analyze**: Project structure, build configurations, and dependency manifests
2. **Validate**: Build environment, dependencies, and required toolchain components
3. **Execute**: Build process with real-time monitoring and error detection
4. **Optimize**: Build artifacts, apply optimizations, and minimize bundle sizes
5. **Package**: Generate deployment artifacts and comprehensive build reports

Key behaviors:

- Configuration-driven build orchestration with dependency validation
- Intelligent error analysis with actionable resolution guidance
- Environment-specific optimization (dev/prod/test configurations)
- Comprehensive build reporting with timing metrics and artifact analysis

## MCP Integration

- **Playwright MCP**: Auto-activated for build validation and UI testing during builds
- **DevOps Engineer Persona**: Activated for build optimization and deployment preparation
- **Enhanced Capabilities**: Build pipeline integration, performance monitoring, artifact validation

## Tool Coordination

- **Bash**: Build system execution and process management
- **Read**: Configuration analysis and manifest inspection
- **Grep**: Error parsing and build log analysis
- **Glob**: Artifact discovery and validation
- **Write**: Build reports and deployment documentation

## Key Patterns

- **Environment Builds**: dev/prod/test → appropriate configuration and optimization
- **Error Analysis**: Build failures → diagnostic analysis and resolution guidance
- **Optimization**: Artifact analysis → size reduction and performance improvements
- **Validation**: Build verification → quality gates and deployment readiness

## Examples

### Standard Project Build

```
/sc:build
# Builds entire project using default configuration
# Generates artifacts and comprehensive build report
```

### Production Optimization Build

```
/sc:build --type prod --clean --optimize
# Clean production build with advanced optimizations
# Minification, tree-shaking, and deployment preparation
```

### Targeted Component Build

```
/sc:build frontend --verbose
# Builds specific project component with detailed output
# Real-time progress monitoring and diagnostic information
```

### Development Build with Validation

```
/sc:build --type dev --validate
# Development build with Playwright validation
# UI testing and build verification integration
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:build` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/build-report.md` when `--output` is absent; `artifacts` lists the build output files the build tool reports, except paths outside the repository and paths git ignores (in a git repository, check each with `git check-ignore`; typically `build/`, `dist/` and `*.egg-info/`): those are left out, because WC-9 stages every listed path and git refuses them, and the build report names where they were written. A build that completes is succeeded; one that fails is failed, with its error analysis in the report.
- **Gates.** There is no gate, and no person-mode flag. Installs and deployments stay out of scope as today.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Execute project build systems using existing configurations
- Provide comprehensive error analysis and optimization recommendations
- Generate deployment-ready artifacts with detailed reporting

**Will Not:**

- Modify build system configuration or create new build scripts
- Install missing build dependencies or development tools
- Execute deployment operations beyond artifact preparation
