# SC Commands Reference

<!-- markdownlint-disable MD040 MD051 -->

**Complete SuperClaude Framework Command Reference**

> This file serves two purposes: quick navigation for Claude Code and learning resource for humans.

**Last Updated**: 2026-10-14

---

## 📑 Table of Contents

- [📋 How to Use This Document](#-how-to-use-this-document)
- [🗂️ Command Categories](#️-command-categories)
- [📖 Detailed Description of Each Command](#-detailed-description-of-each-command)
- [📂 index-repo vs Serena](#-index-repo-vs-serena--indexing-tools-comparison)

---

## 📋 How to Use This Document

This page is the per-command reference: exact syntax, options, and what each command produces. It does not say which command to use for a job; for that, see [How We Work](how-we-work.md), or run `/sc:recommend "<what you want to do>"`.

| Section | Purpose |
|---------|---------|
| [`🗂️ Command Categories`](#️-command-categories) | Every command by category, and whether it changes files |
| [`📖 Detailed Descriptions`](#-detailed-description-of-each-command) | Syntax, options, and examples for each command |
| [`📂 index-repo vs Serena`](#-index-repo-vs-serena--indexing-tools-comparison) | Which indexing tool to use for project memory |

---

## 🗂️ Command Categories

### 1. ORCHESTRATION (Meta-level)

| Command | Purpose | File | Changes files? |
|---------|---------|------|----------------|
| [`/sc:pm`](#scpm---project-manager-agent) | Project Manager agent | `pm.md` | Yes |
| [`/sc:spawn`](#scspawn---meta-system-task-orchestration) | Decomposition Epic → Task | `spawn.md` | Report only (stops after the task breakdown; see its Critical Boundaries) |
| [`/sc:task`](#sctask---enhanced-task-management) | One small, direct change (level 2) | `task.md` | Yes |
| [`/sc:workflow`](#scworkflow---implementation-plan-generator) | Short checked plan for a few files (level 3) | `workflow.md` | Only with `--handoff implement` |
| `/sc:agent` | Session controller for investigate, build, review | `agent.md` | Yes |
| `/sc:roadmap` | Roadmap artifacts from spec, TDD, PRD | `roadmap.md` | Report only |
| `/sc:tasklist` | Sprint-ready tasklist bundles from roadmaps | `tasklist.md` | Report only |
| `/sc:release-split` | Two-phase release split analysis | `release-split.md` | Report only |

### 2. DISCOVERY

| Command | Purpose | File | Changes files? |
|---------|---------|------|----------------|
| [`/sc:brainstorm`](#scbrainstorm---orchestrated-multi-agent-brainstorm) | Clarify requirements (Socratic) | `brainstorm.md` | Report only |
| [`/sc:research`](#scresearch---deep-web-research) | Web research via Tavily | `research.md` | Report only |

### 3. IMPLEMENTATION

| Command | Purpose | File | Changes files? |
|---------|---------|------|----------------|
| [`/sc:implement`](#scimplement---feature-implementation) | Write code | `implement.md` | Yes |
| [`/sc:design`](#scdesign---system-and-component-design) | Architecture, API, schemas | `design.md` | Report only |
| `/sc:tdd` | Create or populate a Technical Design Document | `tdd.md` | Yes (writes the TDD into your repo, `docs/<domain>/TDD_<COMPONENT>.md` by default, or the `--output` path) |
| `/sc:cli-portify` | Port workflows into programmatic CLI pipelines | `cli-portify.md` | Yes |

### 4. QUALITY

| Command | Purpose | File | Changes files? |
|---------|---------|------|----------------|
| [`/sc:analyze`](#scanalyze---code-analysis) | Code analysis (quality/security/perf) | `analyze.md` | Report only |
| [`/sc:troubleshoot`](#sctroubleshoot---issue-diagnosis) | Root cause analysis | `troubleshoot.md` | Report only (`--fix` adds a task file you run with `/task`) |
| [`/sc:test`](#sctest---testing) | Tests + coverage | `test.md` | Only with `--fix` |
| [`/sc:build`](#scbuild---project-building) | Build project | `build.md` | Yes |
| `/sc:adversarial` | Adversarial debate, compare, merge of artifacts | `adversarial.md` | Report only |
| `/sc:auggie-review` | Auggie code review of PRs and diffs | `auggie-review.md` | Report only |
| `/sc:cleanup-audit` | Read-only multi-pass repository cleanup audit | `cleanup-audit.md` | Report only |
| `/sc:swarm-wizard` | Plain-language guide to the swarm CLI | `swarm-wizard.md` | Report only |
| `/sc:validate-roadmap` | Validate roadmap pipeline outputs | `validate-roadmap.md` | Report only |
| `/sc:validate-tests` | Validate tier classification against YAML specs | `validate-tests.md` | Report only |
| `/sc:cli-eval` | Author or run cliEval eval suites | `cli-eval.md` | Yes |

### 5. IMPROVEMENT

| Command | Purpose | File | Changes files? |
|---------|---------|------|----------------|
| [`/sc:improve`](#scimprove---code-improvement) | Refactoring, optimization | `improve.md` | Yes |
| [`/sc:cleanup`](#sccleanup---code-cleanup) | Dead code, unused imports | `cleanup.md` | Yes |

### 6. DOCUMENTATION

| Command | Purpose | File | Changes files? |
|---------|---------|------|----------------|
| [`/sc:explain`](#scexplain---code-explanation) | Code explanation | `explain.md` | No |
| [`/sc:document`](#scdocument---documentation-generation) | Generate documentation | `document.md` | Yes |
| [`/sc:index-repo`](#scindex-repo---repository-indexing) | Repository indexing | `index-repo.md` | Yes (writes `PROJECT_INDEX.md` and `PROJECT_INDEX.json` into your repo) |
| `/sc:index` | Project documentation and knowledge base | `index.md` | Yes (generates project documentation in your repo) |
| `/sc:post-release` | Sync docs and install surface after release | `post-release.md` | Yes |
| `/sc:review-translation` | Localization review with quality scoring | `review-translation.md` | Yes |

### 7. EXPERT PANELS

| Command | Purpose | File | Changes files? |
|---------|---------|------|----------------|
| [`/sc:spec-panel`](#scspec-panel---expert-specification-review) | Specification review (Wiegers, Fowler...) | `spec-panel.md` | Report only |
| [`/sc:business-panel`](#scbusiness-panel---business-analysis-panel) | Business analysis (Porter, Drucker...) | `business-panel.md` | Report only |

### 8. UTILITIES

| Command | Purpose | File | Changes files? |
|---------|---------|------|----------------|
| [`/sc:git`](#scgit---git-operations) | Git + smart commits | `git.md` | Yes |
| [`/sc:reflect`](#screflect---tiered-reflection) | Pre/post-execution audit | `reflect.md` | Only with `--mode post` (moves the work folder on a pass unless you add `--no-promote`) |
| `/sc:load` | Load Serena project memory (not a resume method) | `load.md` | No |
| `/sc:save` | Save Serena project memory (not a resume method) | `save.md` | Report only |
| `/sc:help` | List installed commands, skills, process levels | `help.md` | No |
| `/sc:recommend` | Paste-ready prompt for the right command | `recommend.md` | Report only (inside an IronClaude checkout it writes its cache and telemetry under `.claude/cache/`) |
| `/sc:init-lite` | Safe audit of project-local context surfaces | `init-lite.md` | Report only |
| `/sc:pr-submit` | Open fork PR and monitor review fixes | `pr-submit.md` | Yes |

"Report only" means the command only answers, or saves its report under `.dev/`, `claudedocs/` or its own output folder, and never edits your code or docs. "Yes" follows the routing guide's rule: writing docs into your repository, a commit, or moving a task folder to `done/` all count as changes, so `/sc:document` is "Yes". `/sc:workflow --handoff implement` hands the plan to `/sc:implement`, which edits code. `/sc:reflect --mode post` also moves the work folder on a pass unless you add `--no-promote`; `/sc:auggie-review` posts to the PR unless you add `--no-post-pr`; `/sc:pr-submit --monitor 0` only opens the PR.

---

## 📖 Detailed Description of Each Command

---

### `/sc:adversarial` - Adversarial Debate and Merge

**When to use:** Compare 2-10 artifacts (or generate variants from one source) through a structured adversarial debate and get a documented, scored merge. It plans and merges only; it does not check domain correctness or run the merged output (see [How We Work](how-we-work.md)).

**Syntax:**

```
/sc:adversarial --compare file1.md,file2.md[,...,fileN.md] [options]
```

Other input forms (use exactly one): `--source <file> --generate <type> --agents <model[:persona]>,...` generates variants from one file and compares them; `--pipeline "<shorthand>"` or `--pipeline @pipeline.yaml` runs a multi-phase pipeline.

**Options:**

| Flag | Default | What it does |
|------|---------|--------------|
| `--depth quick\|standard\|deep` | `standard` | Debate depth |
| `--convergence <0.50-0.99>` | `0.80` | Agreement threshold that ends the debate |
| `--interactive` | off | Pause for your input at decision points |
| `--output <dir>` | auto | Where the six output files go |
| `--focus <areas>` | all | Comma-separated debate focus areas |
| `--blind` | off | Strip model names before comparing |

Full option list: `~/.claude/commands/sc/adversarial.md`.

**Examples:**

```bash
/sc:adversarial --compare draft-a.md,draft-b.md --depth standard
/sc:adversarial --source auth-spec.md --generate roadmap --agents opus:architect,sonnet:security --depth deep
```

**MCP servers:** context7, serena

---

### `/sc:agent` - Session Controller

**When to use:** Start a session controller that clarifies scope, plans the investigation, and drives implementation and review for the task you describe. It waits silently after its startup checklist until you describe the task. For choosing how much process a job needs, prefer the levels in [How We Work](how-we-work.md).

**Syntax:**

```
/sc:agent
```

**MCP servers:** none

---

### `/sc:auggie-review` - Auggie-Powered Code Review

**When to use:** Review a PR, a local diff, or a file snapshot for narrow bugs, architectural risks and anti-patterns, using Auggie's indexed codebase context. It is advisory only (it never edits the code under review) and posts the report to the PR unless you pass `--no-post-pr`.

**Syntax:**

```
/sc:auggie-review [<PR-num|PR-URL>|--diff <base>...HEAD|--snapshot <path>] [--focus security,architecture,quality,performance,all] [--depth quick|standard|deep] [--post-pr|--no-post-pr] [--remediation-offer|--no-remediation-offer]
```

**MCP servers:** serena

---

### `/sc:cleanup-audit` - Multi-Pass Repository Audit

**When to use:** Run a read-only, multi-pass audit of a repository or path that classifies each file with evidence and recommends cleanup. It never modifies, deletes, moves or renames files; acting on the recommendations is a separate, human-reviewed step.

**Syntax:**

```
/sc:cleanup-audit [target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]
```

**MCP servers:** serena, context7

---

### `/sc:cli-eval` - cliEval Suite Lifecycle

**When to use:** Author a new cliEval suite (`create`) or interactively pick and supervise a run of an existing suite (`run`). It adds no flags to the `superclaude eval` CLI and never reports a non-green run as green.

**Syntax:**

```
/sc:cli-eval create [--name <stem>] [--from @<design-or-spec>.md] [--agents opus,sonnet,haiku]
/sc:cli-eval run    [--suite <name>] [--eval <id>]
```

**MCP servers:** context7, serena

---

### `/sc:cli-portify` - Workflow to CLI Pipeline Port

**When to use:** Port an inference-based SuperClaude workflow (command, skills and agents) into a programmatic CLI pipeline with supervised execution. It does not modify the source skill files or run the generated pipeline.

**Syntax:**

```
/sc:cli-portify --workflow <skill-name-or-path> [--name <cli-name>] [--output <dir>] [--dry-run]
```

**MCP servers:** serena, context7

---

### `/sc:help` - Installed Commands and Process Levels

**When to use:** List the SuperClaude commands and skills installed here, show the six process levels, and point to the routing guide. It is read-only and does not recommend a workflow; for that, see [How We Work](how-we-work.md).

**Syntax:**

```
/sc:help
```

**MCP servers:** none

---

### `/sc:index` - Project Documentation

**When to use:** Generate project documentation and a knowledge base with intelligent organization and cross-referencing. It does not override existing manual documentation without explicit permission.

**Syntax:**

```
/sc:index [target] [--type docs|api|structure|readme] [--format md|json|yaml]
```

**MCP servers:** context7

---

### `/sc:init-lite` - Safe Context Audit

**When to use:** Audit the project-local SuperClaude context surfaces (`CLAUDE.md`, `.mcp.json`, `.claude/` settings, commands, skills, agents), estimate their context weight, and write a non-destructive report under `.dev/superclaude/`. It never modifies those context inputs and writes nothing with `--dry-run`.

**Syntax:**

```
/sc:init-lite --context-optimized [--project-root <dir>] [--output <path>] [--dry-run] [--scaffold] [--force]
```

**MCP servers:** serena

---

### `/sc:load` - Project Context Loading

**When to use:** Load Serena project memory (project context, memories and checkpoints) at the start of a session. It is not a way to resume work: to continue a task, rerun `/task <task file>` or `/sc:implement <plan path>`, or reopen a tagged session with `ccsession <name>` (see [How We Work](how-we-work.md), section 3.12). It does not modify project structure or configuration, or override existing session context without a checkpoint.

**Syntax:**

```
/sc:load [target] [--type project|config|deps|checkpoint] [--refresh] [--analyze]
```

**MCP servers:** serena

---

### `/sc:pm` - Project Manager Agent

**Status:** A command. It runs only when you invoke it; nothing activates it automatically.

**When to use:** Agent-coordinated work when you want the PM agent's PDCA cycle. For choosing a workflow, prefer the levels in [How We Work](how-we-work.md): a vague idea goes to `/sc:brainstorm`, multi-file work to `/task-builder` then `/task`, and a new product or major feature to `/prd`, `/tdd`, `/roadmap`.

**What it does:**

- Loads Serena project memory (not a way to resume work)
- Delegates tasks to personas (backend, frontend, security...)
- Runs PDCA cycle: Plan → Do → Check → Act
- Saves notes to Serena project memory (not a way to resume work)

**Workflow:**

```
User: "I want to add authentication"
PM Agent:
  1. Activates Brainstorming Mode (if request is vague)
  2. Delegates to requirements-analyst
  3. Delegates to system-architect
  4. Delegates to security-engineer
  5. Delegates to backend-architect
  6. Delegates to quality-engineer
  7. Documents in CLAUDE.md
```

**Syntax:**

```
/sc:pm [request] [--strategy brainstorm|direct|wave] [--verbose]
```

**MCP servers:** context7, playwright, morphllm, serena, tavily

**Key patterns:**

- Session Start Protocol (context restoration)
- Self-Correcting Execution (root cause first!)
- PDCA Document Structure (`docs/pdca/[feature]/`)

---

### `/sc:post-release` - Post-Release Follow-Through

**When to use:** After the release gate tags a version, bring that release's external surface current: user docs, technical docs, install and deploy scripts (checked by real end-to-end runs), and human-run e2e test guides. It needs an existing release tag.

**Syntax:**

```
/sc:post-release <version> [options]
```

**Options:**

| Flag | Default | What it does |
|------|---------|--------------|
| `<version>` | required | An existing release tag, for example `v1.4.1` |
| `--output <dir>` | `docs/testing/<version>/` | Where the report, manifest and test guides go |

**Examples:**

```bash
/sc:post-release v1.4.1
/sc:post-release v1.4.1 --output docs/testing/v1.4.1/
```

**MCP servers:** serena

---

### `/sc:pr-submit` - PR Review Auto-Remediation Monitor

**When to use:** Open a PR on the fork and, at `--monitor 1` or higher, arm an in-session monitor that polls for the Augment review, verifies findings, and sends verified ones to `/sc:troubleshoot`; higher levels also fix, push, reply and resolve. With no `--monitor` it runs level 3. `--monitor 0` only opens the PR; it never pushes to an upstream parent or to a protected branch.

**Syntax:**

```
/sc:pr-submit [--monitor {0,1,2,3}] [--max-rounds N≤5] [--poll-interval ≥30] [--timeout 600] [--silence-timeout 300] [--base <branch>] [--head <branch>] [--title ...] [--body ...] [--pr <N>] [--output-dir <dir>] [--resume <run-log.jsonl>]
```

**MCP servers:** serena, auggie

---

### `/sc:recommend` - Refined-Prompt Builder

**When to use:** Describe a goal and get a paste-ready prompt that hands it to the right local skill, command, agent or native-tool sequence, checked against the source files; with `--plugin` it searches the Claude plugin and community skill ecosystem instead. It reads [How We Work](how-we-work.md) first and only recommends commands and flags that exist.

**Syntax:**

```
/sc:recommend <goal description> [--plugin] [--eval <mode>] [--minstar <N>]
```

**MCP servers:** auggie, tavily

---

### `/sc:release-split` - Release Split Analysis

**When to use:** Analyze a release artifact (spec, roadmap, tasklist or refactor plan) for natural split points and get a neutral split or no-split recommendation with fidelity verification. It does not execute the resulting release plans or produce tasklists or roadmaps directly.

**Syntax:**

```
/sc:release-split <spec-file-path> [options]
```

**Options:**

| Flag | Default | What it does |
|------|---------|--------------|
| `--output <dir>` | `<spec-dir>/release-split/` | Where all artifacts go (paths under `.claude/skills/`, `.claude/agents/` or `.claude/commands/` are refused) |
| `--depth quick\|standard\|deep` | `standard` | Analysis depth |
| `--interactive` | off | Pause for your confirmation between parts |
| `--resume-from <proposal>` | - | Start from an already validated split proposal |
| `--no-split` | off | Skip split analysis; check the release as one piece |
| `--agents <specs>` | `opus:architect,sonnet:analyzer` | Agents that write competing split proposals (at least 2) |

Full option list: `~/.claude/commands/sc/release-split.md`.

**Examples:**

```bash
/sc:release-split path/to/release-spec.md
/sc:release-split path/to/release-spec.md --depth deep --interactive
```

**MCP servers:** context7, serena

---

### `/sc:review-translation` - Localization Quality Review

**When to use:** Review translation files for linguistic and cultural quality, with adversarial validation, real-world usage evidence and a scored, prioritized report. It implements fixes only on your explicit request and does not replace a professional human translator for high-stakes content.

**Syntax:**

```
/sc:review-translation [source-file] [translation-files...] [flags]
```

**Options:**

| Flag | Default | What it does |
|------|---------|--------------|
| `--strict` | off | Strict validation mode |
| `--depth quick\|standard\|deep` | `standard` | Review depth |
| `--tone-matrix` | off | Score tone on a measured scale |
| `--platform steam\|playstation\|mobile\|web\|enterprise` | auto | Apply that platform's conventions |
| `--export` | off | Also write a team handoff file |

**Examples:**

```bash
/sc:review-translation english.json de_DE.json fr_FR.json es_ES.json
/sc:review-translation source.json translations/*.json --depth deep --tone-matrix
```

**MCP servers:** tavily, context7, serena

---

### `/sc:roadmap` - Roadmap Generator

**When to use:** Generate roadmap pipeline artifacts from one to three markdown inputs (spec, TDD and/or PRD), mirroring the `superclaude roadmap run` CLI. It does not generate tasklists, execute implementation, or modify the source files. It belongs to the separate release pipeline (`/sc:tasklist`, then `superclaude sprint run`); for the default planning route use `/roadmap`, which writes a task file for every phase (see [How We Work](how-we-work.md), section 5).

**Syntax:**

```
/sc:roadmap [OPTIONS] INPUT_FILES...
```

`INPUT_FILES` is 1-3 markdown files (at most one spec, one TDD and one PRD), in any order.

**Options:**

| Flag | Default | What it does |
|------|---------|--------------|
| `--output <dir>` | folder of the first input | Where all artifacts go |
| `--agents <specs>` | `opus:architect,sonnet:architect` | Agents for the generate and debate steps (`model[:persona]`) |
| `--depth quick\|standard\|deep` | `standard` | Debate rounds (1, 2 or 3) |
| `--resume` | off | Skip steps whose outputs already pass their gates |
| `--dry-run` | off | Print the step plan and gate criteria, then exit |
| `--no-validate` | off | Skip the validation step at the end |

Full option list: `~/.claude/commands/sc/roadmap.md`.

**Examples:**

```bash
/sc:roadmap spec.md tdd.md prd.md --output .dev/releases/current/example-release/
/sc:roadmap spec.md --dry-run
```

**MCP servers:** none

---

### `/sc:save` - Session Context Persistence

**When to use:** Save session context, learnings and checkpoints to Serena project memory so a later session can read them with `/sc:load`. It is not a way to resume work (see [How We Work](how-we-work.md), section 3.12). It does not override existing session context without checkpoint preservation.

**Syntax:**

```
/sc:save [--type session|learnings|context|all] [--summarize] [--checkpoint]
```

**MCP servers:** serena

---

### `/sc:spawn` - Meta-System Task Orchestration

**When to use:** Break a large job into parts with dependencies; it stops after the task breakdown. For work that changes code, use `/task-builder` then `/task` instead (level 4 in [How We Work](how-we-work.md)).

**What it does:**

- Breaks down Epic → Story → Task → Subtask
- Selects strategy: sequential/parallel/adaptive
- Coordinates dependencies between tasks

**Syntax:**

```
/sc:spawn [complex-task] [--strategy sequential|parallel|adaptive] [--depth normal|deep]
```

**Examples:**

```bash
# Decompose a large job into a task hierarchy (no code is changed)
/sc:spawn "plan the move of the reporting jobs to the new scheduler" --strategy adaptive --depth deep
# Breakdown: Epic → Story → Task → Subtask, with dependencies
```

**Difference from `/sc:task`:**

- spawn = decomposition (breaking down)
- task = execution (doing work)

---

### `/sc:swarm-wizard` - Guided Swarm Launcher

**When to use:** Run the `superclaude swarm` multi-model review without being a swarm expert: it interviews you about what to review and why, picks the lens and flags, proves the pipeline with a stub dry-run, then asks before launching a real run and summarizes the outcome. It never launches a real-model run without your go-ahead and a passing dry-run.

**Syntax:**

```
/sc:swarm-wizard [--goal <text>] [--target <path>] [--output <dir>] [--real] [--detached] [--advanced] [--yes]
```

**MCP servers:** none

---

### `/sc:task` - Enhanced Task Management

**When to use:** A small, direct change: one source file plus its test, five edits or fewer, and you know exactly what it should be (level 2 in [How We Work](how-we-work.md)). Work that touches more than one source file or needs more than five edits needs a written plan (`/sc:workflow --depth quick` or `/task-builder`).

**What it does:**

- Prints a `Tier:` line at the start (`STRICT`, `STANDARD`, `LIGHT` or `EXEMPT`)
- `STANDARD` and `STRICT` run the full protocol, including the affected tests
- `LIGHT` (typos, comments, formatting) and `EXEMPT` (no code change) skip its checks, so run the test yourself afterwards

**Syntax:**

```
/sc:task [operation] [target] [--strategy systematic|agile|enterprise] [--compliance strict|standard|light|exempt] [--verify] [--skip-compliance] [--force-strict] [--parallel] [--delegate] [--no-escalation]
```

**Examples:**

```bash
# One small, direct change (level 2)
/sc:task "Rename recieved_at to received_at in src/jobs/runner.py and update its tests"
# Prints its Tier: line, makes the change, and (STANDARD/STRICT) runs the affected tests
```

**MCP servers:** context7, serena, playwright, morphllm

---

### `/sc:tasklist` - Tasklist Generator

**When to use:** Turn a roadmap into a deterministic, Sprint CLI-compatible tasklist bundle and validate it against the source roadmap. It does not modify the roadmap or run `superclaude sprint run`.

**Syntax:**

```
/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]
```

**MCP servers:** context7

---

### `/sc:tdd` - Technical Design Document Creator

**When to use:** Create or populate a Technical Design Document for a component, service or system, researched from the actual codebase and optionally translated from a PRD. It designs only; it does not implement the system.

**Syntax:**

```
/sc:tdd <component> [options]
```

**Options:**

| Flag | Default | What it does |
|------|---------|--------------|
| `--from-prd <path>` (alias `--prd`) | - | PRD to translate into engineering specifications |
| `--tier lightweight\|standard\|heavyweight` | `standard` | Design depth |
| `--focus <dirs or files>` | all | Comma-separated places to investigate |
| `--output <path>` | auto | Path for the finished TDD |
| `--resume <task file>` | - | Continue an interrupted TDD session |

**Examples:**

```bash
/sc:tdd "canvas roadmap" --from-prd docs/product/PRD_ROADMAP_CANVAS.md --tier standard --focus frontend/app/roadmap/
/sc:tdd --resume .dev/tasks/to-do/TASK-TDD-20260401-143022/TASK-TDD-20260401-143022.md
```

**MCP servers:** context7, auggie-mcp

---

### `/sc:validate-roadmap` - Roadmap Pipeline Output Validator

**When to use:** Validate the `roadmap.md`, `test-strategy.md` and `extraction.md` produced by a prior `superclaude roadmap run`, with single-agent reflection or, for two or more agents, an adversarial merge. It writes only to `<OUTPUT_DIR>/validate/`, never modifies the inputs, and always exits 0 with findings printed to the console.

**Syntax:**

```
/sc:validate-roadmap <roadmap-path> --specs <spec1.md,spec2.md,...> [options]
```

The command hands its arguments to the `sc-validate-roadmap-protocol` skill, which needs the roadmap file and the spec files it was built from. It is a read-only audit and writes its findings to `<roadmap-dir>/validation/` unless you pass `--output`.

**Options:**

| Flag | Default | What it does |
|------|---------|--------------|
| `--specs <files>` | required | Comma-separated spec files the roadmap must satisfy (1-10) |
| `--output <dir>` | `<roadmap-dir>/validation/` | Where the validation artifacts go |
| `--depth quick\|standard\|deep` | `standard` | How thorough the analysis is |
| `--exclude <domains>` | none | Comma-separated domains to leave out |
| `--max-agents <n>` | `20` | Maximum parallel agents (4-20) |
| `--skip-adversarial` | off | Skip the adversarial pass |
| `--skip-remediation` | off | Skip the remediation plan |
| `--report <path>` | none | Also write a summary to this path |
| `--prior-taxonomy <file>` | none | Seed domain clustering from a prior `00-domain-taxonomy.md` |

**Examples:**

```bash
/sc:validate-roadmap .dev/releases/current/v2/roadmap.md --specs docs/specs/billing-tdd.md
/sc:validate-roadmap ./roadmap.md --specs spec-a.md,spec-b.md --depth deep
```

**MCP servers:** auggie, serena

---

### `/sc:validate-tests` - Behavioral Test Validation

**When to use:** Validate tier classification behavior against YAML test specifications and report pass and fail counts. It does not modify the test specifications or the classification algorithm.

**Syntax:**

```
/sc:validate-tests [target] [flags]
```

`target` is a test file or folder (default `tests/sc-task/`).

**Options:**

| Flag | What it does |
|------|--------------|
| `--all` | Run every test file |
| `--category <name>` | One category: classification, routing, compound, boosters, comparison, edge, integration |
| `--verbose` | Detailed trace for each test |
| `--summary` | Pass/fail counts only (the default) |
| `--stop-on-fail` | Stop at the first failure |
| `--report <path>` | Save the report to a file |

**Examples:**

```bash
/sc:validate-tests --all
/sc:validate-tests --category classification --verbose
```

**MCP servers:** none

---

### `/sc:workflow` - Implementation Plan Generator

**When to use:** A few files with clear scope that fit in one or two sessions (level 3 in [How We Work](how-we-work.md)); always pass `--depth quick`. It writes a phased plan (`<id>.md`, named like its package directory). For a PRD or TDD use `/roadmap`; for many files or multi-session work use `/task-builder`.

**What it does:**

- Parses a PRD, spec, or inline prompt
- Creates a new package `.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/` (`<subject>` = lower camelCase, max 16 chars, e.g. `authLogin`) with `<id>.md` (schema `workflow-plan/1.2`), a `source.md` snapshot and `return-contract.yaml`; never overwrites an existing package
- Checks the plan against your request when it is written (`/sc:reflect --mode pre`, advisory) and prints the result with the plan path
- Run it with `/sc:implement .dev/tasks/to-do/<id>/<id>.md` (not MDTM `/task`); on completion `/sc:implement` archives the package to `.dev/tasks/done/` on Linux; on any other system (including macOS) the archive is refused on purpose, the folder stays in `.dev/tasks/to-do/` and the run reports archive-blocked. That is expected; never move the folder by hand
- **Does NOT implement code** and does **not** emit sprint tasklists

**Syntax:**

```
/sc:workflow <path-or-prompt> [--strategy systematic|agile|enterprise] [--depth quick|standard|deep] [--handoff none|design|implement|tasklist]
```

`--depth shallow|normal`, `--parallel` and the retired `--output` are `E-LEGACY` (use `quick|standard`, omit `--parallel`; every plan goes to a new `.dev/tasks/to-do/<id>/` package, there is no destination override).

**Examples:**

```bash
/sc:workflow "Add a retry limit to the job runner: stop after 3 failures. Files: src/jobs/runner.py, src/jobs/config.py" --depth quick
```

**Difference from `/sc:implement` / `/sc:task`:**

- workflow = planning (`.dev/tasks/to-do/TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>/<id>.md`: one plan folder, and the plan file is named like its folder)
- implement / task = execution

---

### `/sc:brainstorm` - Orchestrated Multi-Agent Brainstorm

**When to use:** Topic is ambiguous and needs perspectives surfaced via parallel proposals and adversarial merge — not just Socratic dialogue.

**What it does:**

- Runs a depth-tiered Socratic dialogue → `seed-brief.md`
- Auto-routes codebase + research enrichment (`/sc:analyze`, `/sc:research`, `tech-research`)
- Composes a `--agents` spec spanning 3 model aliases × domain-detected personas
- Delegates to `/sc:adversarial` for N parallel proposals + debate + merge → `merged-requirements.md`
- Optionally hands off to `/sc:design`, `/sc:tasklist`, or `/task-builder`

**Syntax:**

```
/sc:brainstorm "<topic>" [--proposals N] [--depth quick|standard|deep] \
  [--strategy systematic|agile|enterprise|auto] \
  [--codebase|--no-codebase] [--research light|deep|none|--no-research] \
  [--personas p1,p2,...] [--models opus,sonnet,haiku] \
  [--blind] [--convergence FLOAT] [--interactive] \
  [--handoff none|design|tasklist|task] [--output DIR] \
  [--dry-run] [--resume-from PATH] [--force-stale]
```

**Examples:**

```bash
# Codebase feature discovery (auto: Auggie enrichment + 3 proposals)
/sc:brainstorm "add rate limiting to public API endpoints" --depth standard

# Deep incident post-mortem
/sc:brainstorm "deployment broke staging at 3am" --depth deep --strategy systematic

# Product idea with research + full handoff to sprint planning
/sc:brainstorm "AI-powered changelog summarizer" --strategy agile --handoff tasklist

# Blind multi-model comparison (strips model identity before scoring)
/sc:brainstorm "consolidate three duplicate auth modules" --depth deep --blind --proposals 4

# Dry-run: preview composed agent-spec without spending tokens on adversarial
/sc:brainstorm "improve onboarding workflow" --dry-run --strategy enterprise
```

**MCP servers:** serena, auggie-mcp, tavily  
**Personas:** architect, analyzer, scribe (auto-selected per detected domain)

→ Full guide: [brainstorm.md](brainstorm.md)

---

### `/sc:research` - Deep Web Research

**When to use:** Need up-to-date information from the internet.

**What it does:**

- Parallel web searches via Tavily
- Multi-hop exploration (following link chains)
- Evidence-based synthesis
- Saves report to `claudedocs/research_*.md`

**Syntax:**

```
/sc:research "[query]" [--depth quick|standard|deep|exhaustive] [--strategy planning|intent|unified]
```

**Examples:**

```bash
/sc:research "latest developments in quantum computing 2024" --depth deep
/sc:research "competitive analysis of AI coding assistants" --depth exhaustive
```

**MCP servers:** tavily, playwright, serena

---

### `/sc:implement` - Feature Implementation

**When to use:** Execute a written plan, spec or task list (or an inline prompt) one step at a time, with a reviewer check of each step against its acceptance criteria. For work that spans more than one session or many files, see [How We Work](how-we-work.md).

**What it does:**

- Splits the source into tasks and, after each task, checks that task against its acceptance criteria (the source text itself when the source is informal); lint and tests are recorded as extras, never the pass/fail
- Keeps one progress ledger: for a `/sc:workflow` plan it is `progress.md` beside the plan; otherwise `.dev/implement/<slug>/progress.md` (override with `--ledger`)
- `--resume` continues from the first task that is not complete
- On a `/sc:workflow` plan, once every task passes it runs a final independent review and archives the plan folder to `.dev/tasks/done/`; on macOS (any system other than Linux) the archive is refused on purpose and the folder stays in `.dev/tasks/to-do/`. `--skip-final-review` skips the final review and, on such a plan, also blocks the archive
- Never commits, opens PRs, or releases

**Syntax:**

```
/sc:implement <path-or-prompt> [--resume] [--ledger <path>] [--skip-final-review]
```

**Examples:**

```bash
# Run a /sc:workflow plan
/sc:implement .dev/tasks/to-do/<id>/<id>.md

# Inline prompt
/sc:implement Add logout to the header and wire it to /logout

# Continue an interrupted task list
/sc:implement .dev/plans/auth-tasklist.md --resume
```

**MCP servers:** none

---

### `/sc:design` - System and Component Design

**When to use:** Need to draft one design (an API, a component, a schema) in a single pass, without implementing it. When other people will build against the design, use `/tdd` instead (see [How We Work](how-we-work.md), section 5).

**What it does:**

- Architecture diagrams
- API specifications
- Database schemas
- Component interfaces

**Syntax:**

```
/sc:design [target] [--type architecture|api|component|database] [--format diagram|spec|code]
```

**Examples:**

```bash
/sc:design user-management-system --type architecture --format diagram
/sc:design payment-api --type api --format spec
/sc:design e-commerce-db --type database --format diagram
```

**Difference from `/sc:implement`:**

- design = blueprint (documentation)
- implement = code (implementation)

---

### `/sc:analyze` - Code Analysis

**When to use:** Need a code audit.

**What it does:**

- Quality: code smells, maintainability
- Security: vulnerabilities, OWASP
- Performance: bottlenecks
- Architecture: technical debt

**Syntax:**

```
/sc:analyze [target] [--focus quality|security|performance|architecture] [--depth quick|deep] [--format text|json|report]
```

**Examples:**

```bash
/sc:analyze src/auth --focus security --depth deep
/sc:analyze --focus performance --format report
/sc:analyze src/components --focus quality --depth quick
```

---

### `/sc:troubleshoot` - Issue Diagnosis

**When to use:** Something is broken, need to find the cause.

**What it does:**

- Root cause analysis
- Stack trace examination
- Log analysis
- Suggests fixes

**Syntax:**

```
/sc:troubleshoot [<issue description>] [--type bug|build|performance|deployment|security|test] [--depth quick|standard|deep] [--scope <path|symbol>] [--no-escalate] [--fix] [--models <tier:model,...>] [--output-dir <path>] [--no-doc-discovery] [--no-mcp] [--context <path>] [--caller <name>]
```

**Examples:**

```bash
/sc:troubleshoot "Null pointer exception in user service" --type bug --depth deep --fix
/sc:troubleshoot "TypeScript compilation errors" --type build --fix
/sc:troubleshoot "API response times degraded" --type performance
```

---

### `/sc:improve` - Code Improvement

**When to use:** Code works, but you want to make it better in a small, contained area. Commit first and review `git diff` afterwards; for a large or structural refactor, write a spec and use `/task-builder` (see [How We Work](how-we-work.md), section 3.7).

**What it does:**

- Quality refactoring
- Performance optimization
- Maintainability improvements
- Technical debt reduction

**Syntax:**

```
/sc:improve [target] [--type quality|performance|maintainability|style] [--safe] [--interactive]
```

**Examples:**

```bash
/sc:improve src/ --type quality --safe
/sc:improve api-endpoints --type performance --interactive
/sc:improve auth-service --type security --validate
```

**MCP servers:** context7

---

### `/sc:cleanup` - Code Cleanup

**When to use:** Need to remove dead code and unused imports. Run `/sc:cleanup-audit` first, commit, then clean up and review `git diff` afterwards (see [How We Work](how-we-work.md), section 3.7).

**What it does:**

- Dead code detection
- Import optimization
- Structure cleanup
- Safety validation

**Syntax:**

```
/sc:cleanup [target] [--type code|imports|files|all] [--safe|--aggressive] [--interactive]
```

**Examples:**

```bash
/sc:cleanup src/ --type code --safe
/sc:cleanup --type imports --preview
/sc:cleanup --type all --interactive
```

**MCP servers:** context7

---

### `/sc:test` - Testing

**When to use:** Need to run tests.

**What it does:**

- Detects test runner
- Coverage reports
- Playwright for E2E
- Failure analysis

**Syntax:**

```
/sc:test [target] [--type unit|integration|e2e|all] [--coverage] [--watch] [--fix]
```

**Examples:**

```bash
/sc:test
/sc:test src/components --type unit --coverage
/sc:test --type e2e  # Activates Playwright MCP
/sc:test --watch --fix
```

**MCP servers:** playwright

---

### `/sc:build` - Project Building

**When to use:** Need to build the project.

**What it does:**

- Compilation
- Bundling
- Optimization
- Error analysis

**Syntax:**

```
/sc:build [target] [--type dev|prod|test] [--clean] [--optimize] [--verbose]
```

**Examples:**

```bash
/sc:build
/sc:build --type prod --clean --optimize
/sc:build frontend --verbose
```

**MCP servers:** playwright

---

### `/sc:explain` - Code Explanation

**When to use:** Need to understand how code works.

**What it does:**

- Explains code at different levels (basic/advanced)
- Framework-specific explanations via Context7
- Interactive examples

**Syntax:**

```
/sc:explain [target] [--level basic|intermediate|advanced] [--format text|examples|interactive] [--context domain]
```

**Examples:**

```bash
/sc:explain authentication.js --level basic
/sc:explain react-hooks --level intermediate --context react
/sc:explain microservices-system --level advanced --format interactive
```

**MCP servers:** context7

---

### `/sc:document` - Documentation Generation

**When to use:** Need to create documentation.

**What it does:**

- Inline comments (JSDoc)
- API documentation
- User guides
- External docs

**Syntax:**

```
/sc:document [target] [--type inline|external|api|guide] [--style brief|detailed]
```

**Examples:**

```bash
/sc:document src/auth/login.js --type inline
/sc:document src/api --type api --style detailed
/sc:document payment-module --type guide --style brief
```

---

### `/sc:index-repo` - Repository Indexing

**When to use:** Starting work with a large repository.

**What it does:**

- Creates `PROJECT_INDEX.md` (3KB instead of 58KB)
- 94% token savings
- Entry points, modules, tests, dependencies

**Syntax:**

```
/sc:index-repo [mode=update|quick]
```

**Examples:**

```bash
/sc:index-repo                # Full indexing
/sc:index-repo mode=update    # Update existing
/sc:index-repo mode=quick     # Quick (without tests)
```

---

### `/sc:spec-panel` - Expert Specification Review

**When to use:** Need specification, API, or requirements review from "experts".

**What it does:**
Simulates a panel discussion of renowned software engineering experts.

**Expert Panel (10 personas):**

| Expert | Specialization | Typical Question/Critique |
|--------|---------------|---------------------------|
| **Karl Wiegers** | Requirements Engineering | "Requirement lacks measurable criteria" |
| **Gojko Adzic** | Specification by Example | "Can you provide Given/When/Then?" |
| **Alistair Cockburn** | Use Cases | "Who is the primary stakeholder?" |
| **Martin Fowler** | Architecture & Design | "This violates single responsibility" |
| **Michael Nygard** | Production Systems | "What happens when this fails?" |
| **Sam Newman** | Microservices | "How handle backward compatibility?" |
| **Gregor Hohpe** | Enterprise Integration | "What's the message exchange pattern?" |
| **Lisa Crispin** | Agile Testing | "How would QA validate this?" |
| **Janet Gregory** | Collaborative Testing | "Did whole team participate?" |
| **Kelsey Hightower** | Cloud Native | "How handle cloud deployment?" |

**Three Operating Modes:**

| Mode | What Happens |
|------|--------------|
| `--mode discussion` | Experts build on each other's ideas (collaborative) |
| `--mode critique` | Systematic review with severity and priorities |
| `--mode socratic` | Questions for deep understanding (learning) |

**Focus Areas:**

| Focus | Lead Expert | Analyzes |
|-------|-------------|----------|
| `--focus requirements` | Wiegers | Clarity, testability, acceptance criteria |
| `--focus architecture` | Fowler | Interfaces, boundaries, patterns |
| `--focus testing` | Crispin | Test strategy, edge cases, coverage |
| `--focus compliance` | Wiegers + Nygard | Security, audit, regulatory |

**Syntax:**

```
/sc:spec-panel [specification_content|@file] [--mode discussion|critique|socratic] [--experts "name1,name2"] [--focus area1,area2,...] [--iterations N] [--format standard|structured|detailed]
```

**Examples:**

```bash
# API specification review
/sc:spec-panel @auth_api.spec.yml --mode critique --focus requirements,architecture

# Requirements workshop
/sc:spec-panel "user story content" --mode discussion --experts "wiegers,adzic,cockburn"

# Learning through questions
/sc:spec-panel @my_first_spec.yml --mode socratic --iterations 2

# Iterative improvement (3 rounds)
/sc:spec-panel @complex_system.spec.yml --iterations 3 --format detailed
```

**Example output (critique mode):**

```
KARL WIEGERS - Requirements Quality:
❌ CRITICAL: Requirement R-001 lacks acceptance criteria
📝 RECOMMENDATION: Replace "handle gracefully" with "open circuit after 5 failures"
🎯 PRIORITY: High
📊 QUALITY IMPACT: +40% testability

MARTIN FOWLER - Interface Design:
⚠️ MINOR: CircuitBreaker couples state with execution
📝 RECOMMENDATION: Separate CircuitBreakerState from Executor
```

**MCP servers:** context7

---

### `/sc:business-panel` - Business Analysis Panel

**When to use:** Need business analysis of strategy, plan, or idea.

**What it does:**
Simulates a panel discussion of legendary business thinkers.

**Expert Panel (9 personas):**

| Expert | Framework | Typical Question |
|--------|-----------|------------------|
| **Clayton Christensen** | Disruption, Jobs-to-be-Done | "What job is customer hiring this for?" |
| **Michael Porter** | Five Forces, Competitive Strategy | "What's your sustainable advantage?" |
| **Peter Drucker** | Management by Objectives | "What results are you measuring?" |
| **Seth Godin** | Tribe Building, Permission Marketing | "Who is your tribe? What story?" |
| **Kim & Mauborgne** | Blue Ocean Strategy | "Competing or creating new market?" |
| **Jim Collins** | Good to Great, Flywheel | "What's your hedgehog concept?" |
| **Nassim Taleb** | Antifragility, Black Swan | "Does this benefit from volatility?" |
| **Donella Meadows** | Systems Thinking | "Where are the leverage points?" |
| **Jean-luc Doumont** | Structured Communication | "Is the message clear and actionable?" |

**Three Operating Modes:**

| Mode | What Happens |
|------|--------------|
| `--mode discussion` | Collaborative — experts build on each other's ideas |
| `--mode debate` | Adversarial — experts argue, stress-test ideas |
| `--mode socratic` | Question-driven — deep questions for understanding |

**Syntax:**

```
/sc:business-panel [content|@file] [--experts "porter,christensen"] [--mode discussion|debate|socratic] [--focus domain] [--synthesis-only]
```

**Examples:**

```bash
# Business plan analysis
/sc:business-panel @business_plan.md

# Competitive analysis
/sc:business-panel @market_analysis.md --experts "porter,christensen" --focus "competitive-analysis"

# Strategy debate (stress-test)
/sc:business-panel @strategy.md --mode debate

# Synthesis only (without detailed analysis)
/sc:business-panel @pitch_deck.md --synthesis-only
```

**Example output (discussion mode):**

```
PORTER: "The competitive position relies on cost leadership..."
CHRISTENSEN: "But cost leadership is vulnerable to disruption from below..."
KIM/MAUBORGNE: "Consider creating new market space instead..."
TALEB: "The real question: does this benefit from uncertainty?"
```

**MCP servers:** context7

---

### When to Use Which Panel

| Document | Panel |
|----------|-------|
| API specification | [`/sc:spec-panel`](#scspec-panel---expert-specification-review) |
| User stories / Requirements | [`/sc:spec-panel`](#scspec-panel---expert-specification-review) |
| Architecture Decision Record | [`/sc:spec-panel`](#scspec-panel---expert-specification-review) |
| Business plan | [`/sc:business-panel`](#scbusiness-panel---business-analysis-panel) |
| Go-to-market strategy | [`/sc:business-panel`](#scbusiness-panel---business-analysis-panel) |
| Pitch deck | [`/sc:business-panel`](#scbusiness-panel---business-analysis-panel) |
| PRD (Product Requirements) | **Both** — spec for technical, business for strategy |

---

### `/sc:git` - Git Operations

**When to use:** Git operations with smart commit messages.

**Syntax:**

```
/sc:git [operation] [args] [--smart-commit] [--interactive]
```

**Examples:**

```bash
/sc:git status
/sc:git commit --smart-commit  # Generates conventional commit message
/sc:git merge feature-branch --interactive
```

---

### `/sc:reflect` - Tiered Reflection

**When to use:** Audit a proposed plan against its spec before execution (UC-1), or audit completed work for adherence and deviations after execution (UC-2). Reviewer-side, structurally-independent — not single-agent self-review.

**Syntax:**

```
/sc:reflect [--mode pre|post] [--spec <path>] [--tasklist <path>] [--diff <ref-or-path>] [--scope <path>] [--depth quick|standard|deep] [--tier 1|2|auto] [--reviewers N] [--output <dir>] [--no-reachability] [--no-promote] [--promote-dry-run] [--remediate]
```

**Examples:**

```bash
/sc:reflect --mode pre --spec docs/spec.md --tasklist .dev/tasklists/feat.md   # UC-1 coverage/gap audit
/sc:reflect --mode post --diff HEAD~1..HEAD --tasklist .dev/tasklists/feat.md  # UC-2 deviation audit
/sc:reflect --mode post --diff HEAD~1..HEAD --depth deep --remediate           # force Tier 2 + offer remediation
```

**Legacy grammar** (preserved for `/sc:troubleshoot` Wave 6 and other v1 callers):

```bash
/sc:reflect --type task --analyze    # maps to --mode pre
/sc:reflect --type task --validate   # maps to --mode post
```

> The post-mapped legacy form (`--type task --validate`) still requires `--diff` or `--task-log`; `/sc:troubleshoot` Wave 6 supplies these, so standalone callers must add `--diff <ref>`.

**MCP servers:** auggie, serena, context7, tavily

#### `superclaude reflect run` (CLI auto-fix wrapper)

**When to use:** Run the post-execution reflect gate non-interactively (CI, sprint hooks, headless pipelines) when you want a fail-closed exit code and, optionally, a bounded auto-fix loop. This is the CLI **engine**, distinct from the `/sc:reflect` **skill** above.

**Engine vs. skill:** The wrapper does not re-implement reflection. It launches `/sc:reflect --mode post` as a **top-level `claude --print` subprocess** (so Tier-2 heterogeneous fan-out is preserved — a nested call would collapse it), parses the resulting `return-contract.yaml`, derives a fail-closed 4-state verdict, and writes a `reflect_post:` block back into the task file's frontmatter. The process exit code is the verdict code: **pass `0`, halted `10`, degraded `11`, blocked `2`**. Only a clean, full, non-degraded Tier-2 pass exits `0`.

**Syntax:**

```
superclaude reflect run <tasklist> [--fix/--no-fix] [--max-fix-iterations N] [--base <ref>] [--promote/--no-promote] [--depth standard|deep] [--tmux] [--resume] [--dry-run] [--print-command] [--output <dir>] [--timeout <sec>] [--allow-single-vendor]
```

**Wrapper-specific flags:**

| Flag | Default | Purpose |
|------|---------|---------|
| `--fix` / `--no-fix` | `--no-fix` | Run the bounded audit → apply → re-verify auto-fix loop. When enabled, the wrapper consumes the skill's `remediation_task_path` and auto-runs the corrective `/task`. |
| `--max-fix-iterations N` | `2` | Max apply → verify cycles before a terminal HALT. |
| `--base <ref>` | (none) | Explicit audit base ref (single ref vs. working tree). Highest precedence — overrides frontmatter `start_commit` + merge-base. |
| `--promote` / `--no-promote` | `--promote` | Allow reflect's gated Wave-7 promotion. The default is now **on**; pass `--no-promote` to suppress it. |

**Headless auto-authoring:** Because the wrapper launches the skill under `claude --print` (no TTY), the skill's `--remediate` handoff **auto-accepts and authors** the corrective MDTM without the interactive yes/no prompt — but only for AUTO-FIXABLE registers (Drift / Necessary). HUMAN-REQUIRED registers (any Regression, or `needs_human_decision: true`) author nothing auto-runnable, emit `remediation_task_path: null`, and the wrapper terminal-HALTs rather than auto-applying a human-decision change. The skill never executes `/task` itself; the wrapper's auto-fix loop is the sole consumer that runs the authored path. This handoff rides on return-contract `contract_version` **≥1.4.0** (1.4.0 added the `remediation_task_path` field the loop reads; the 1.5.0 D13 bump is additive and leaves this field unchanged) — it never guesses a "newest `TASK-RF-*`" directory.

**Examples:**

```bash
superclaude reflect run path/to/TASK.md                                  # audit-only gate, fail-closed exit code
superclaude reflect run path/to/TASK.md --fix --max-fix-iterations 3     # bounded auto-fix loop
superclaude reflect run path/to/TASK.md --base origin/master --no-promote
superclaude reflect run path/to/TASK.md --tmux --depth deep              # watch live in a detached window
```

> Full reference (verdict matrix, sentinel/`--tmux` mechanics, recursion breaker, sidecar, and the complete auto-fix state machine): see `docs/guides/reflect-cli-tools-guide.md`.

---

## 📂 index-repo vs Serena — Indexing Tools Comparison

### What Each Tool Creates

| Tool | Creates files | Where stored |
|------|---------------|--------------|
| [`/sc:index-repo`](#scindex-repo---repository-indexing) | `PROJECT_INDEX.md` (3KB) | Project root |
| **Serena MCP** | `.serena/project.yml` + `.serena/memories/*.md` | `.serena/` folder in project |

### Serena File Structure

```
.serena/
├── project.yml              # Configuration (languages, encoding, LSP settings)
├── .gitignore               # Git ignore
└── memories/
    ├── project_overview.md      # About the project, tech stack
    ├── suggested_commands.md    # Development commands
    ├── style_conventions.md     # Code styles and conventions
    └── task_completion.md       # Task completion checklist
```

---

### Key Differences

| Aspect | [`/sc:index-repo`](#scindex-repo---repository-indexing) | **Serena MCP** |
|--------|------------------|----------------|
| **Type** | Static file | Live LSP server + memories |
| **Main goal** | Quick start (token savings) | Semantic code understanding |
| **What it understands** | File structure | Symbols (functions, classes, types) |
| **Updates** | Manual (`mode=update`) | Memories — manual, LSP — automatic |
| **Persistence** | File in project | Files in `.serena/memories/` |
| **LSP operations** | ❌ No | ✅ rename, find references, go to definition |
| **Cross-session** | ✅ Read file | ✅ Memories are persistent |
| **Tokens at start** | ~3K (reading INDEX) | On demand (reading needed memories) |

---

### When to Use What

**[`/sc:index-repo`](#scindex-repo---repository-indexing)** — for quick session start:

- Project structure overview
- Entry points and key modules
- Dependencies and configuration
- Quick start commands
- **Savings**: 58K → 3K tokens at start

**Serena MCP** — for deep code work:

- `find_symbol` — find class/function by name
- `find_referencing_symbols` — where symbol is used
- `rename_symbol` — rename everywhere safely via LSP
- `get_symbols_overview` — file structure (class methods etc.)
- **Memories** — persistent notes about project across sessions

---

### Recommendation

**Either one is sufficient** to start working:

| If you chose | What you get | Each session |
|--------------|--------------|--------------|
| **Serena** (recommended) | Memories + LSP + symbols | No need to read anything |
| [**index-repo**](#scindex-repo---repository-indexing) | PROJECT_INDEX.md | Can read for context |
| **Both** | Maximum information | Optional |

```bash
# Initial setup (once)
serena activate_project .         # Activate project
serena onboarding                 # Create memories
# and/or
/sc:index-repo                    # Create PROJECT_INDEX.md

# On structural changes
/sc:index-repo mode=update        # Update INDEX (if using)
serena edit_memory ...            # Update memories (if needed)
```

**Important**: SuperClaude commands automatically use Serena for code work.
Explicitly reading PROJECT_INDEX.md or calling `serena read_memory` each session is **not required**.

---

### Auto-update?

| What | Auto-updates? | How to update |
|------|---------------|---------------|
| `PROJECT_INDEX.md` | ❌ No | [`/sc:index-repo`](#scindex-repo---repository-indexing) `mode=update` |
| Serena memories | ❌ No | `write_memory` / `edit_memory` |
| Serena LSP understanding | ✅ Yes | Automatically sees file changes |

---

### When to Update?

| Event | [index-repo](#scindex-repo---repository-indexing) | Serena memories |
|-------|------------|-----------------|
| Added new module/folder | ✅ Update | ⚡ Optional |
| Renamed module | ✅ Update | ⚡ Optional |
| Fixed bug in file | ❌ Not needed | ❌ Not needed |
| Added dependency | ✅ Update | ❌ Not needed |
| Changed code conventions | ❌ Not needed | ✅ Update |
| Before PR/release | ⚡ Good practice | ❌ Not needed |

---

*This document is updated as the project evolves.*
