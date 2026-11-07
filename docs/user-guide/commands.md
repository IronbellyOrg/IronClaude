# SC Commands Reference

<!-- markdownlint-disable MD040 MD051 -->

**IronClaude command reference**

> This file serves two purposes: quick navigation for Claude Code and learning resource for humans.

**Last Updated**: 2026-11-03

---

## 📑 Table of Contents

- [📋 How to Use This Document](#-how-to-use-this-document)
- [🗂️ Command Categories](#️-command-categories)
- [📖 Detailed Description of Each Command](#-detailed-description-of-each-command)

---

## 📋 How to Use This Document

This page is the per-command reference: exact syntax, options, and what each command produces. It does not say which command to use for a job; for that, see [How We Work](how-we-work.md), or run `/sc:recommend "<what you want to do>"`.

| Section | Purpose |
|---------|---------|
| [`🗂️ Command Categories`](#️-command-categories) | Every command by category, and whether it changes files |
| [`📖 Detailed Descriptions`](#-detailed-description-of-each-command) | Syntax, options, and examples for each command |

---

## 🗂️ Command Categories

### 1. ORCHESTRATION (Meta-level)

| Command | Purpose | File | Changes files? |
|---------|---------|------|----------------|
| [`/sc:pm`](#scpm---project-manager-agent) | Project Manager agent | `pm.md` | Yes |
| [`/sc:spawn`](#scspawn---meta-system-task-orchestration) | Decomposition Epic → Task | `spawn.md` | Report only (stops after the task breakdown; see its Critical Boundaries) |
| [`/sc:task`](#sctask---enhanced-task-management) | One small, direct change (level 2) | `task.md` | Yes |
| [`/sc:workflow`](#scworkflow---implementation-plan-generator) | Checked implementation plan (level 3, the default for planned work) | `workflow.md` | Only with `--handoff implement` |
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
| [`/sc:troubleshoot`](#sctroubleshoot---issue-diagnosis) | Root cause analysis | `troubleshoot.md` | Report only (`--fix` offers a `/sc:workflow` plan you run with `/sc:implement`; `--fix --depth deep` offers a `/task-builder` task file you run with `/task`) |
| [`/sc:impact`](#scimpact---change-impact-report) | What depends on a symbol or a diff, from the code graph | `impact.md` | Report only |
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
| `/sc:load` | Load project memory from `.superclaude/memory/` (not a resume method) | `load.md` | No |
| `/sc:save` | Save project memory to `.superclaude/memory/` (not a resume method) | `save.md` | Report only |
| `/sc:help` | List installed commands, skills, process levels | `help.md` | No |
| [`/sc:graph`](#scgraph---code-graph-index-status) | Code-graph index status; builds the index only on `init` | `graph.md` | Only with `init` |
| [`/sc:issue`](#scissue---github-issue-claim-and-create) | Claim a GitHub issue (assign, accuracy check, summary, next-step prompt, then an Orca worktree and a launched agent) or create a templated issue | `issue.md` | Yes (posts to GitHub; writes `.dev/issues/`) |
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

**MCP servers:** context7

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

**MCP servers:** codegraph

---

### `/sc:cleanup-audit` - Multi-Pass Repository Audit

**When to use:** Run a read-only, multi-pass audit of a repository or path that classifies each file with evidence and recommends cleanup. It never modifies, deletes, moves or renames files; acting on the recommendations is a separate, human-reviewed step.

**Syntax:**

```
/sc:cleanup-audit [target-path] [--pass surface|structural|cross-cutting|all] [--batch-size N] [--focus infrastructure|frontend|backend|all]
```

**MCP servers:** codegraph, context7

---

### `/sc:cli-eval` - cliEval Suite Lifecycle

**When to use:** Author a new cliEval suite (`create`) or interactively pick and supervise a run of an existing suite (`run`). It adds no flags to the `superclaude eval` CLI and never reports a non-green run as green.

**Syntax:**

```
/sc:cli-eval create [--name <stem>] [--from @<design-or-spec>.md] [--agents opus,sonnet,haiku]
/sc:cli-eval run    [--suite <name>] [--eval <id>]
```

**MCP servers:** context7

---

### `/sc:cli-portify` - Workflow to CLI Pipeline Port

**When to use:** Port an inference-based SuperClaude workflow (command, skills and agents) into a programmatic CLI pipeline with supervised execution. It does not modify the source skill files or run the generated pipeline.

**Syntax:**

```
/sc:cli-portify --workflow <skill-name-or-path> [--name <cli-name>] [--output <dir>] [--dry-run]
```

**Review loop:** its spec review runs 1 convergence iteration (a focus pass and a critique pass). MINOR findings go to the spec's Open Items and never start another pass; if CRITICAL findings are still unaddressed after that iteration it stops with `status: partial` and escalates them to you.

**MCP servers:** context7

---

### `/sc:graph` - Code-Graph Index Status

**When to use:** Check whether this worktree's code-graph index is ready (codegraph version, pin match, index state, worktree relation, counts, pending files, telemetry and one next action). The session-start hook already starts indexing in every new checkout; type `/sc:graph init` only when it did not cover this worktree: a nested worktree that answers from its parent's index, the hook switched off with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`, or an init that failed or was interrupted.

**Syntax:**

```
/sc:graph [status|init] [--worktree-local] [--output-dir <dir>]
```

**Options:**

| Flag | Default | What it does |
|------|---------|--------------|
| `status` \| `init` | `status` | `status` prints the readiness report. `init` builds the index for this worktree and runs only when you type it; no skill, agent or automatic flow runs it |
| `--worktree-local` | off | Only with `init`: give a nested worktree its own index instead of its parent's |
| `--output-dir <dir>` | screen only | Also write `return-contract.yaml` there |

**Examples:**

```bash
/sc:graph                        # readiness report
/sc:graph init                   # index this worktree
/sc:graph init --worktree-local  # nested worktree: build its own index
```

It never rebuilds an existing index, never runs `init` while another init or index is running, and never changes MCP registration or installs codegraph. See the [codegraph guide](codegraph.md).

**MCP servers:** codegraph

---

### `/sc:help` - Installed Commands and Process Levels

**When to use:** List the SuperClaude commands and skills installed here, show the six process levels, and point to the routing guide. It is read-only and does not recommend a workflow; for that, see [How We Work](how-we-work.md).

**Syntax:**

```
/sc:help
```

**MCP servers:** none

---

### `/sc:impact` - Change Impact Report

**When to use:** Before you change a symbol, see what depends on it: for named symbols, or for the symbols a diff touches, it lists their definitions and their production and test dependents (direct callers plus transitive impact), and with `--tests` adds an advisory list of test files. It never edits code, runs tests or builds an index (use `/sc:graph` for index status).

**Syntax:**

```
/sc:impact <symbol>... | --diff [<base>] [--depth 1-3] [--limit N] [--tests] [--test-depth N] [--output-dir <dir>] [--caller <name>]
```

**Options:**

| Flag | Default | What it does |
|------|---------|--------------|
| `<symbol>...` | none | 1-30 bare names (no `Class.method` or path); use either symbols or `--diff`, never both |
| `--diff [<base>]` | `HEAD` when given without a value | Map the changed hunks of the diff to the symbols they touch |
| `--depth 1-3` | `2` | Transitive depth for impact |
| `--limit N` | `20` | Caller rows per symbol (1-100) |
| `--tests` | off | Add an advisory test list; it can add tests to a selection, never remove any |
| `--test-depth N` | codegraph's own | 1-5, only with `--tests` |
| `--output-dir <dir>` | `<worktree>/.dev/impact/<slug>-<timestamp>/` | Where `impact.md` and `return-contract.yaml` are written |
| `--caller <name>` | unset | Name of the calling skill; shortens the chat output to three lines |

**Examples:**

```bash
/sc:impact parse_config                      # dependents of one symbol
/sc:impact --diff origin/master --tests      # symbols a branch changed, plus advisory tests
```

When codegraph, the index or its lookup tools are not usable, it falls back to Grep, keeps going and reports `status: partial`. See the [codegraph guide](codegraph.md).

**MCP servers:** codegraph

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

**MCP servers:** none

---

### `/sc:issue` - GitHub Issue Claim and Create

**When to use:** Take an existing GitHub issue on the repository `origin` points at, or file a new one. `--claim` assigns the issue to you, checks whether its text is still accurate against today's code and the pull requests merged since it was opened, writes a summary (with an effort estimate in hours) and a next-step prompt under `.dev/issues/<N>/`, posts an accuracy-check comment and a claim comment, then creates (or reuses) an Orca worktree named `issue-<N>` and launches one Claude Code agent in it. How far that agent goes is the `--pipeline` level (below); nothing ever merges. Orca must be running: without it the claim stops with `E-ORCA-REQUIRED` before it assigns or posts anything. `--create` turns a description into an issue built from one of four templates (feature or bug, simple or complex) with labels from a fixed set.

**Syntax:**

```
/sc:issue --claim <number|url> [--pipeline worktree|full|none] [--submit]
/sc:issue --create "<description>" [--depth quick|standard|deep] [--mode feature|bug] [--type <type>]
```

**Options:**

| Flag | Mode | Default | What it does |
|------|------|---------|--------------|
| `--claim <number\|url>` | claim | - | The issue to claim: a number (`302`, `#302`) or an issue URL on the origin repo |
| `--create "<description>"` | create | - | The feature or bug description, as text or `@path` to a file |
| `--depth quick\|standard\|deep` | create | `quick` | How hard the command checks your flags and fills the body; `deep` uses the complex template |
| `--mode feature\|bug` | create | chosen by a worker | Picks the feature or bug template and the `enhancement` or `bug` label |
| `--type <type>` | create | chosen by a worker | Area of the change: `cicd`, `command`, `skill`, `agent`, `hook`, `cli`, `core`, `docs`, `tests`, `install` or `other`; maps to a `type: <value>` label |
| `--pipeline worktree\|full\|none` | claim | `worktree` | How far the launched agent goes (see the levels below); every value creates the worktree, `none` launches no agent |
| `--submit` | claim | off | Only with `--pipeline full`: the agent also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`. Takes no value |

`--depth`, `--mode` and `--type` work with `--create` only; `--pipeline` and `--submit` work with `--claim` only (`E-CLAIM-ONLY-FLAG`), and `--submit` without `--pipeline full` stops with `E-SUBMIT-NEEDS-FULL`. There is no repository option: the repository is always `origin`.

**Claim levels (`--pipeline`):**

| Level | What the launched agent does | Commit, push, PR |
|-------|------------------------------|------------------|
| `worktree` (default) | Runs the steps of `next-steps.md` up to the plan boundary, prints the plan path and `Waiting for approval`, then waits until you reply `approved` (or run the printed implement command) | No |
| `full` | Runs every step, implementation included, and leaves the changes in the working tree, nothing staged | No |
| `full` with `--submit` | Does the same, then commits, pushes a feature branch to `origin` and opens a PR through `/sc:pr-submit --monitor 3` | Yes; never merges |
| `none` | Creates the worktree and copies the files; launches no agent. You run `next-steps.md` there yourself | No |

No level merges anything: people review and merge. The agent starts behind the ccsession shim (the claim warns with `W-LAUNCH-NOT-CCSESSION` if it cannot confirm that). The levels are instructions in the agent's prompt until the launch-level enforcement hook (issue 394) is installed; until then the claim warns with `W-ENFORCEMENT-ABSENT` and you should not use `full` or `--submit` on a real issue.

**Examples:**

```bash
/sc:issue --claim 302
/sc:issue --claim 302 --pipeline none
/sc:issue --claim 302 --pipeline full
/sc:issue --claim 302 --pipeline full --submit
/sc:issue --create "The sync check misses deleted skill files" --mode bug --type cli --depth standard
/sc:issue --create @notes/new-command.md --depth deep
```

It posts directly to GitHub, without showing the comment or the issue body for approval first. It never creates labels: a label from the fixed set that the repository does not have is skipped and listed. On claim it also assigns the matching ClickUp task, only when `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` are set; `--create` never touches ClickUp. The claim itself never runs a step of `.dev/issues/<N>/next-steps.md`: the launched agent does, at the level you chose (with `--pipeline none` you run them yourself in the worktree). A re-claim reuses the existing worktree and does not launch a second agent, also when you re-claim from inside the worktree; the claim output names the two files that hold the launch (`.dev/issues/<N>/worktree.json` and a file in the worktree's git directory), and removing the `launch` entry from both launches again. Worktree or launch problems are warnings: the issue stays assigned and the comments stay posted.

**ClickUp settings (claim only, environment variables):**

| Variable | Required | What it does |
|----------|----------|--------------|
| `CLICKUP_API_TOKEN` | yes | Your own ClickUp personal token (`pk_...`); never printed or written to disk |
| `CLICKUP_WORKSPACE_ID` | yes | The ClickUp workspace (team) to search |
| `CLICKUP_LIST_IDS` | no | Comma-separated list IDs that narrow the search |
| `CLICKUP_MAX_PAGES` | no | Pages of 100 tasks to search, default `20` |

The task is found by the issue URL in its description or a custom field, or else by `#<N>` in its title, and is assigned only when exactly one task matches. The ClickUp result appears in the claim comment and never stops the claim: `not found`, `ambiguous (<count> candidates)`, `already assigned` and `error (<reason>)` all leave the GitHub assignment in place. `error (page_cap)` means the search reached `CLICKUP_MAX_PAGES` before it saw every task, so nothing was assigned; raise `CLICKUP_MAX_PAGES` or set `CLICKUP_LIST_IDS` and claim again.

**MCP servers:** auggie, codegraph

---

### `/sc:load` - Project Context Loading

**When to use:** Load project memory from the `.superclaude/memory/` files (project context, memories and checkpoints) at the start of a session. It is not a way to resume work: to continue a task, rerun `/task <task file>` or `/sc:implement <plan path>`, or reopen a tagged session with `ccsession <name>` (see [How We Work](how-we-work.md), section 3.12). It does not modify project structure or configuration, or override existing session context without a checkpoint.

- For 5.0.0 only, when `<project>/.superclaude/memory/<key>.md` is absent it reads the old `<project>/.serena/memories/<key>.md` instead, read-only: it never writes there and tells you that folder is read-only history.
- It ends its summary by pointing you to `/sc:graph status` to see whether this worktree's code-graph index is ready; it never runs `/sc:graph` itself.

**Syntax:**

```
/sc:load [target] [--type project|config|deps|checkpoint] [--refresh] [--analyze]
```

**MCP servers:** none

---

### `/sc:pm` - Project Manager Agent

**Status:** A command. It runs only when you invoke it; nothing activates it automatically.

**When to use:** Agent-coordinated work when you want the PM agent's PDCA cycle. For choosing a workflow, prefer the levels in [How We Work](how-we-work.md): a vague idea goes to `/sc:brainstorm`, multi-file work to `/sc:workflow` then `/sc:implement`, and a new product or major feature to `/prd`, `/tdd`, then `/sc:workflow`.

**What it does:**

- Loads project memory from `.superclaude/memory/` (not a way to resume work)
- Delegates to specialist agents (backend, frontend, security...)
- Runs PDCA cycle: Plan → Do → Check → Act
- Saves notes to project memory in `.superclaude/memory/` (not a way to resume work)

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

**MCP servers:** context7, playwright, morphllm, tavily

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

**MCP servers:** none

---

### `/sc:pr-submit` - PR Review Auto-Remediation Monitor

**When to use:** Open a PR on the fork and, at `--monitor 1` or higher, arm an in-session monitor that polls for the Augment and Codex reviews (a reviewer that never shows activity on the PR is skipped), verifies findings, and sends verified ones to `/sc:troubleshoot`; higher levels also fix, push, reply and resolve. With no `--monitor` it runs level 3. `--monitor 0` only opens the PR; it never pushes to an upstream parent or to a protected branch.

**Syntax:**

```
/sc:pr-submit [--monitor {0,1,2,3}] [--max-rounds N≤5] [--poll-interval ≥30] [--timeout 600] [--silence-timeout 300] [--base <branch>] [--head <branch>] [--title ...] [--body ...] [--pr <N>] [--conflict-max-tier {0,1,2}] [--output-dir <dir>] [--resume <run-log.jsonl>]
```

**Merge conflicts:** `--monitor` defaults to `3`, but `--conflict-max-tier` defaults to `0` (detect and report only). These are independent ceilings: raising the conflict cap does not grant more monitor authority. Monitor 0 skips conflict handling; monitor 1 and above detect conflicts before the first review and report a per-file plan before editing. A branch that is merely behind the base is reported, not automatically rebased.

| Conflict cap | What it permits |
|---|---|
| `0` (default) | Detect and report only. Unresolved conflicts can still halt the run or skip CI; this is not a promise of a clean result. |
| `1` (opt-in) | Also regenerate a conflicted root `uv.lock` before CI. For eligible Tier 1 cases after a clean or report-only review, monitor 1 proposes and monitor 2 leaves a validated, uncommitted merge in progress; monitor 3 may push one validated merge of the recorded base tip. |
| `2` (opt-in) | Also resolve text/tree conflicts by stated intent, only before the first review at monitor 3. Requires at least two remaining review rounds, at most eight text-conflict files, a resolution record, a read-only grounding check and full tests. Re-triggers configured reviewers; an attributed re-review spends a round. |

Tier 3 conflicts need human resolution: for example protected/migration paths, binary files, symlinks, mode changes, unsupported lock/generated files or unclear intent. They are reported at monitor 1 or 2 and halt at monitor 3. There is at most one conflict cycle per run; late text conflicts halt rather than triggering continuous repair. A conflict that first appears while the CI wait is running gets one more Tier 1 sync only when no conflict cycle started earlier in the run; it needs `--conflict-max-tier` of at least 1 at every monitor level (with the default cap of 0 it ends with `tier_above_cap`), and with a cap of at least 1 monitor 1 only proposes and monitor 2 only leaves a validated uncommitted merge, both only after a `clean` or `report_only` review, and only monitor 3 pushes; a late text (Tier 2) conflict halts. A Tier 1 sync push uses no review round and sends no reviewer re-trigger, reply or thread resolution; it does not clear a non-clean review outcome. After a merge push, CI follows the new head: expected-but-missing checks keep polling and may time out as `ci_not_started`; unresolved conflicts skip CI as `pr_conflicting`.

**Examples (run in Claude Code, not a shell):**

```text
/sc:pr-submit --pr 42 --monitor 3                         # conflicts detected and reported only
/sc:pr-submit --pr 42 --monitor 3 --conflict-max-tier 1   # opt in to root uv.lock regeneration
/sc:pr-submit --pr 42 --monitor 3 --conflict-max-tier 2 --max-rounds 2
```

**Safety and recovery:** use conflict resolution only on PRs from collaborators you trust with your credentials. Regeneration, tests and commit hooks execute project code. The lock trust gate is a narrow check, not a sandbox: Git/URL dependency sources are not covered, and Python 3.10 has no built-in TOML parser so that gate fails closed. The tracked tree must be clean and no foreign operation may be in progress. The skill does not stash changes, rebase a published head or force-push. At monitor 2, review and finish the uncommitted merge yourself, or abort it. Other halt messages say whether the owned merge was aborted or left for inspection; resume checks its recorded ownership and push state, never aborting a foreign merge or blindly publishing an uncovered local commit. Undo a published merge with a new revert commit, not rewritten history.

The run reports the highest conflict tier, the conflict outcome and a separate Tier 1 sync-push count (`sync_tier`, `sync_outcome`, `sync_push_count`). See [PR Submit Command Flags](flags.md#pr-submit-command-flags-scpr-submit) and the shipped protocol's `refs/conflict-mechanical.md` (cycle/recovery) and `refs/conflict-intent.md` (Tier 2) for details. This is an attended skill workflow, not a background conflict-resolution service.

`--yes` was removed in 5.0.0 (it was accepted but never read); drop it from your scripts.

**MCP servers:** auggie

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

**MCP servers:** context7

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

**MCP servers:** tavily, context7

---

### `/sc:roadmap` - Roadmap Generator

**When to use:** Generate roadmap pipeline artifacts from one to three markdown inputs (spec, TDD and/or PRD), mirroring the `superclaude roadmap run` CLI. It does not generate tasklists, execute implementation, or modify the source files. It belongs to the separate release pipeline (`/sc:tasklist`, then `superclaude sprint run`). For ordinary planning use `/sc:workflow`; `/roadmap` is the MDTM composer for when you explicitly select it (see [How We Work](how-we-work.md), section 5).

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

**When to use:** Save session context, learnings and checkpoints to project memory in `.superclaude/memory/` so a later session can read them with `/sc:load`. It is not a way to resume work (see [How We Work](how-we-work.md), section 3.12). It does not override existing session context without checkpoint preservation.

**Syntax:**

```
/sc:save [--type session|learnings|context|all] [--summarize] [--checkpoint]
```

**MCP servers:** none

---

### `/sc:spawn` - Meta-System Task Orchestration

**When to use:** Break a large job into parts with dependencies; it stops after the task breakdown. For work that changes code, use `/sc:workflow` then `/sc:implement` instead (level 3 in [How We Work](how-we-work.md)).

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

**When to use:** A small, direct change: one source file plus its test, five edits or fewer, and you know exactly what it should be (level 2 in [How We Work](how-we-work.md)). Work that touches more than one source file or needs more than five edits needs a written plan (`/sc:workflow`, level 3; `/task-builder` only when you explicitly select MDTM).

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

**MCP servers:** context7, playwright, morphllm

---

### `/sc:tasklist` - Tasklist Generator

**When to use:** Turn a roadmap into a deterministic, Sprint CLI-compatible tasklist bundle and validate it against the source roadmap. It does not modify the roadmap or run `superclaude sprint run`.

**Syntax:**

```
/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]
```

**Review loop:** only High and Medium validation findings are blocking and get patched; Low findings are listed as notes and are never patched or re-checked. The patch loop runs at most one re-patch pass, then stops and escalates any open blocking findings to you instead of shipping them.

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

**MCP servers:** auggie, codegraph

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

**When to use:** Any change that needs a written plan, including work across many files or several sessions, with or without a spec, PRD or TDD (level 3 in [How We Work](how-we-work.md), the ordinary default for planned work). The default is `--depth standard`; use `--depth quick` for a smaller checked plan. It writes a phased plan (`<id>.md`, named like its package directory). Use `/task-builder` only when you explicitly select MDTM or have an exceptional need for its machinery (level 4).

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
/sc:workflow "Add a retry limit to the job runner: stop after 3 failures. Files: src/jobs/runner.py, src/jobs/config.py" --depth standard --handoff none
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
- Composes a `--agents` spec spanning 3 model aliases × domain-detected personas (in a ccsession tier workspace the launcher sets each `ANTHROPIC_DEFAULT_*_MODEL` for a tier the owner may use, so the matching aliases `opus`, `sonnet` and `haiku` map to `claude-gw-tier1a`, `claude-gw-tier1b` and `claude-gw-tier2`; see [model-aliases](../reference/model-aliases.md))
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

**MCP servers:** auggie-mcp, codegraph, tavily  
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

**MCP servers:** tavily, playwright

---

### `/sc:implement` - Feature Implementation

**When to use:** Execute a written plan, spec or task list (or an inline prompt) one step at a time, with a reviewer check of each step against its acceptance criteria. For work that spans more than one session or many files, see [How We Work](how-we-work.md).

**What it does:**

- Splits the source into tasks and, after each task, checks that task against its acceptance criteria (the source text itself when the source is informal); lint and tests are recorded as extras, never the pass/fail
- Keeps one progress ledger: for a `/sc:workflow` plan it is `progress.md` beside the plan; otherwise `.dev/implement/<slug>/progress.md` (override with `--ledger`)
- `--resume` continues from the first task that is not complete
- On a `/sc:workflow` plan, once every task passes it runs a final independent review and archives the plan folder to `.dev/tasks/done/`; on macOS (any system other than Linux) the archive is refused on purpose and the folder stays in `.dev/tasks/to-do/`. `--skip-final-review` skips the final review and, on such a plan, also blocks the archive
- Never commits, opens PRs, or releases
- Review loops: it keeps its own severity model instead of the general 2-fix-cycle rule. Minor and note findings never change a task's verdict; only blocking findings fail it, and each attempt gets at most one in-place repair before the next attempt or a halt that asks you to decide

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
- `--fix` offers a `/sc:workflow` plan you run with `/sc:implement`; `--fix --depth deep` offers a `/task-builder` task file you run with `/task`. Code changes never apply automatically

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

**MCP servers:** auggie, codegraph, context7, tavily

---

### `/sc:improve` - Code Improvement

**When to use:** Code works, but you want to make it better in a small, contained area. Commit first and review `git diff` afterwards; for a large or structural refactor, write a spec, run `/sc:workflow`, then `/sc:implement` (see [How We Work](how-we-work.md), section 3.7).

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
- For code targets, a one-hop view of the symbol's direct callers and callees from codegraph (Read and Grep alone when codegraph is not usable)
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

**MCP servers:** context7, codegraph

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

**MCP servers:** auggie, codegraph, context7, tavily

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
| `--fix` / `--no-fix` | `--no-fix` | Run the bounded audit → apply → re-verify auto-fix loop. By default the wrapper reads the skill's `remediation_plan_path` and applies `/sc:implement <remediation_plan_path>`; only with `--depth deep` it reads `remediation_task_path` and runs `/task <remediation_task_path>`. |
| `--max-fix-iterations N` | `2` | Max apply → verify cycles before a terminal HALT. |
| `--base <ref>` | (none) | Explicit audit base ref (single ref vs. working tree). Highest precedence — overrides frontmatter `start_commit` + merge-base. |
| `--promote` / `--no-promote` | `--promote` | Allow reflect's gated Wave-7 promotion. The default is now **on**; pass `--no-promote` to suppress it. |

**Headless auto-authoring:** Because the wrapper launches the skill under `claude --print` (no TTY), the skill's `--remediate` handoff **auto-accepts and authors** the corrective artifact without the interactive yes/no prompt (a `/sc:workflow` plan, emitted as `remediation_plan_path`; with `--depth deep`, an MDTM task file, emitted as `remediation_task_path`) — but only for AUTO-FIXABLE registers (Drift / Necessary). HUMAN-REQUIRED registers (any Regression, or `needs_human_decision: true`) author nothing auto-runnable, and the wrapper terminal-HALTs rather than auto-applying a human-decision change. The skill never runs `/sc:implement` or `/task` itself; the wrapper's auto-fix loop is the sole consumer that runs the authored path. The loop reads only these contract fields (`remediation_plan_path` was added in contract 1.8.0) — it never guesses a "newest `TASK-RF-*`" directory.

**Examples:**

```bash
superclaude reflect run path/to/TASK.md                                  # audit-only gate, fail-closed exit code
superclaude reflect run path/to/TASK.md --fix --max-fix-iterations 3     # bounded auto-fix loop
superclaude reflect run path/to/TASK.md --base origin/master --no-promote
superclaude reflect run path/to/TASK.md --tmux --depth deep              # watch live in a detached window
```

> Full reference (verdict matrix, sentinel/`--tmux` mechanics, recursion breaker, sidecar, and the complete auto-fix state machine): see `docs/guides/reflect-cli-tools-guide.md`.

---

*This document is updated as the project evolves.*
