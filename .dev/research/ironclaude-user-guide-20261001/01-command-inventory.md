# Research: IronClaude Command, Skill, and CLI Inventory (user-guide input)
**Scope:** /Users/cmerritt/GFxAI/IronClaude (branch feature/task-builder-merge): README.md, CLAUDE.md, KNOWLEDGE.md, docs/getting-started/*, docs/user-guide/*, src/superclaude/commands/*.md, src/superclaude/skills/*/SKILL.md, src/superclaude/cli/
**Status:** Complete (master correction applied; see Sections 6-8)
**Date:** 2026-10-01
**Mode:** Read-only on source. All paths below are relative to /Users/cmerritt/GFxAI/IronClaude unless absolute.
**HEAD inspected:** 58bdef20 (feature/task-builder-merge)

> **AUTHORITY NOTE (coordinator correction, 2026-10-01):** /Users/cmerritt/GFxAI/IronClaude is an old June branch. The authoritative copy is **/Users/cmerritt/GFxAI/IronClaude-tier-tools** (checked out branch `feat/tier-tools-update`, HEAD 50a8c7f4, 2026-09-30, "Merge pull request #250 from IronbellyOrg/Workflow_v3"). Sections 1-5 below were built from the June branch and are kept as the baseline. **Section 6 is the master delta and overrides Sections 1-5 wherever they disagree.** Section 7 records what is actually installed for this user. Section 8 re-checks every gap against master.

---

## How the columns were judged

- **Cost (light / medium / heavy):** derived from each file's `complexity:` frontmatter plus whether it fans out subagents. `low`/`basic` = light; `standard`/`enhanced`/`moderate` = medium; `advanced`/`high`/`meta`, or any command that delegates to a multi-agent protocol skill, = heavy. This is a judgment from frontmatter, not a measured token cost. [CODE-VERIFIED frontmatter only; actual token cost UNVERIFIED]
- **Interactive vs autonomous:** "interactive" = the file describes Socratic dialogue, `--interactive`, a stop-and-wait step, or output the user must paste/act on. Everything else runs to completion once invoked.
- **Thin command + protocol skill:** 18 of the 42 command files (README.md excluded) are thin wrappers whose body says `> Skill <name>` (blocking activation). The real logic lives in the paired `src/superclaude/skills/<name>/SKILL.md`. CLAUDE.md:9-14 makes invoking that skill an ABSOLUTE RULE.

## 1. Slash commands (`src/superclaude/commands/*.md`, installed to `~/.claude/commands/sc/`)

| Command | What it does (one plain sentence) | When a human should reach for it | Interactive / autonomous | Cost | Source (activation line) |
|---|---|---|---|---|---|
| `/sc:help` | Prints a static table of /sc commands and framework flags; executes nothing. | First session, or when you forget a command name. | Autonomous (display only) | Light (`complexity: low`) | src/superclaude/commands/help.md |
| `/sc` | Command dispatcher/help that lists only 5 commands (research, index-repo, agent, recommend, sc). | Rarely; `/sc:help` or `/sc:recommend` is more complete. | Autonomous (display) | Light | src/superclaude/commands/sc.md |
| `/sc:recommend` | Builds a paste-ready prompt routing your goal to the best existing command/skill/agent, or says "just use native tools". | Whenever you have a goal but do not know which command fits. `--plugin` searches the external plugin ecosystem. | Interactive (you paste the output yourself; it never executes it, recommend.md:111) | Medium (`standard`; auggie + tavily; `--eval` opt-in is heavy) | src/superclaude/commands/recommend.md:54 -> skills/sc-recommend |
| `/sc:agent` | Session-controller startup checklist (git status, token reminder) that then waits for you to describe a task. | Start of a session if you want the orchestrator persona. | Interactive (waits for user) | Light | src/superclaude/commands/agent.md |
| `/sc:pm` | Project-manager orchestration with PDCA cycles that delegates to sub-agents. | Multi-step feature work where you want one coordinator to plan and delegate. | Autonomous | Heavy (`complexity: meta`, 8 MCP servers) | src/superclaude/commands/pm.md:52 -> skills/sc-pm-protocol |
| `/sc:task` | Classifies a request into STRICT / STANDARD / LIGHT / EXEMPT compliance tiers, then executes (trivial tiers inline, others via protocol skill). | General "do this change" requests where you want tiered rigor. | Autonomous | Heavy for STRICT/STANDARD, light for LIGHT/EXEMPT | src/superclaude/commands/task.md:99-102 -> skills/sc-task-protocol |
| `/sc:brainstorm` | Socratic requirements dialogue, then parallel proposals, then adversarial merge into a spec. | Vague idea, need to turn it into requirements. | Interactive (Socratic dialogue) | Heavy (`advanced`; delegates to adversarial at brainstorm.md:133) | src/superclaude/commands/brainstorm.md:141 -> skills/sc-brainstorm-protocol |
| `/sc:adversarial` | Structured debate, comparison, and merge of 2-10 artifacts (specs, roadmaps, designs). | You have competing drafts and want one best-of merged version. | Autonomous (some interactive options) | Heavy (`advanced`, 3002-line protocol) | src/superclaude/commands/adversarial.md:146 -> skills/sc-adversarial-protocol |
| `/sc:spec-panel` | Simulated panel of named specification experts reviews and improves a spec. | Before building from a spec, to stress-test it. | Autonomous (has discussion/critique/socratic modes) | Medium (`enhanced`) | src/superclaude/commands/spec-panel.md |
| `/sc:business-panel` | Simulated panel of business thought leaders analyzes a document. | Strategy or business-case review, not code. | Autonomous (socratic mode available) | Medium-heavy (`performance-profile: complex`) | src/superclaude/commands/business-panel.md |
| `/sc:roadmap` | Generates roadmap artifacts from 1-3 spec/TDD/PRD files; mirrors `superclaude roadmap run`. | You have a spec and need a phased roadmap. | Autonomous | Heavy | src/superclaude/commands/roadmap.md:85 -> skills/sc-roadmap-protocol |
| `/sc:validate-roadmap` | Validates roadmap outputs against specs with coverage matrix and gap registry; mirrors `roadmap validate`. | After a roadmap exists, before generating tasklists. | Autonomous | Heavy (`advanced`, multi-agent) | src/superclaude/commands/validate-roadmap.md:74 -> skills/sc-validate-roadmap-protocol |
| `/sc:tasklist` | Turns a roadmap into a deterministic, Sprint-CLI-compatible tasklist bundle. | After roadmap validation, before `superclaude sprint run`. | Autonomous | Heavy (`high`) | src/superclaude/commands/tasklist.md:76 -> skills/sc-tasklist-protocol |
| `/sc:release-split` | Analyzes whether one planned release should become two, with adversarial validation and fidelity check. | A release spec feels too big. | Autonomous by default; `--interactive` flag available | Heavy (`advanced`) | src/superclaude/commands/release-split.md:103 -> skills/sc-release-split-protocol |
| `/sc:reflect` | Tiered reflection: pre-execution coverage audit of a plan vs spec, or post-execution deviation audit of finished work. | Before executing a tasklist (`--mode pre`) or after finishing work (`--mode post`). | Autonomous | Heavy (`advanced`; Tier 2 fans out 2-3 reviewers) | src/superclaude/commands/reflect.md:128 -> skills/sc-reflect-protocol |
| `/sc:troubleshoot` | Tiered debugging: fast triage, auto-escalation to parallel hypotheses and fix debate, optional task-builder remediation. | Broken build, failing test, runtime error, regression. | Autonomous (`--fix` opt-in) | Medium at Tier 1, heavy at Tier 2/3 | src/superclaude/commands/troubleshoot.md:80 -> skills/sc-troubleshoot-protocol |
| `/sc:auggie-review` | Code review of a PR, diff, or file using Auggie retrieval, can post review to the PR and offer remediation. | Reviewing a PR or local diff. | Autonomous (`--post-pr` / remediation offer) | Heavy (`advanced`) | src/superclaude/commands/auggie-review.md:69 -> skills/sc-auggie-review-protocol |
| `/sc:cleanup-audit` | Multi-pass read-only repository audit producing evidence-backed cleanup recommendations. | Repo hygiene review; it changes nothing. | Autonomous | Heavy (`high`, multi-pass) | src/superclaude/commands/cleanup-audit.md:82 -> skills/sc-cleanup-audit-protocol |
| `/sc:cli-portify` | Ports an inference-based sc workflow into a programmatic CLI pipeline. | Framework contributors converting a skill into a CLI pipeline. | Autonomous | Heavy (`high`) | src/superclaude/commands/cli-portify.md:81 -> skills/sc-cli-portify-protocol |
| `/sc:review-translation` | Localization review with adversarial validation and real-world evidence search. | Reviewing translated UI or docs. | Autonomous | Heavy (`advanced`) | src/superclaude/commands/review-translation.md:48 -> skills/sc-review-translation-protocol |
| `/sc:init-lite` | Safe, non-destructive audit of project-local SuperClaude context files with an optional advisory scaffold. | Onboarding a new project to see what context surfaces exist. | Autonomous | Light (`complexity: low`) | src/superclaude/commands/init-lite.md:50 -> skills/sc-init-lite-protocol |
| `/sc:validate-tests` | Validates `/sc:task` tier classification against YAML test specs. | Framework contributors only. | Autonomous | Medium (`moderate`) | src/superclaude/commands/validate-tests.md:113 -> skills/sc-validate-tests-protocol |
| `/sc:tdd` | Creates or populates a Technical Design Document from the project template. | Designing a component or turning a PRD into a TDD. | Autonomous | Heavy (`advanced`) | src/superclaude/commands/tdd.md:151 -> skills/tdd |
| `/sc:analyze` | Code analysis across quality, security, performance, architecture. | Quick health read of a module. | Autonomous | Light (`basic`) | src/superclaude/commands/analyze.md |
| `/sc:build` | Build, compile, package with error handling. | Building the project. | Autonomous | Medium (`enhanced`) | src/superclaude/commands/build.md |
| `/sc:cleanup` | Removes dead code and tidies structure (this one does edit, unlike cleanup-audit). | After cleanup-audit, or small tidy-ups. | Autonomous | Medium (`standard`) | src/superclaude/commands/cleanup.md |
| `/sc:design` | Designs architecture, APIs, component interfaces. | Early design sketches (lighter than `/sc:tdd`). | Autonomous | Light (`basic`) | src/superclaude/commands/design.md |
| `/sc:document` | Generates focused docs for a component, function, or API. | Small doc tasks. | Autonomous | Light (`basic`) | src/superclaude/commands/document.md |
| `/sc:estimate` | Development estimates for tasks or features. | Sizing work. | Autonomous | Medium (`standard`) | src/superclaude/commands/estimate.md |
| `/sc:explain` | Explains code, concepts, or behavior. | Learning a codebase. | Autonomous | Medium (`standard`) | src/superclaude/commands/explain.md |
| `/sc:git` | Git operations with generated commit messages. | Committing or branch workflow. | Autonomous | Light (`basic`) | src/superclaude/commands/git.md |
| `/sc:implement` | Feature implementation with persona activation and MCP use. | Writing a feature directly (no task file). | Autonomous | Medium (`standard`, 4 MCP servers) | src/superclaude/commands/implement.md |
| `/sc:improve` | Systematic quality, performance, maintainability improvements. | Refactor or polish pass. | Autonomous | Medium (`standard`) | src/superclaude/commands/improve.md |
| `/sc:test` | Runs tests with coverage and reporting. | Running the test suite. | Autonomous | Medium (`enhanced`) | src/superclaude/commands/test.md |
| `/sc:index` | Generates project documentation / knowledge base. | Building project docs. | Autonomous | Medium (`standard`) | src/superclaude/commands/index.md |
| `/sc:index-repo` | Builds a compact repository index (claims 58K to 3K tokens). | Start of work on a large repo to save context. | Autonomous | Medium (one-time cost) | src/superclaude/commands/index-repo.md |
| `/sc:load` | Loads project context from Serena memory at session start. | Resuming a project in a new session. | Autonomous | Medium (needs Serena MCP) | src/superclaude/commands/load.md |
| `/sc:save` | Persists session context to Serena memory. | End of a session. | Autonomous | Medium (needs Serena MCP) | src/superclaude/commands/save.md |
| `/sc:research` | Deep web research with adaptive planning. | Questions beyond the model's knowledge or needing current sources. | Autonomous | Heavy (`advanced`; tavily, playwright) | src/superclaude/commands/research.md |
| `/sc:select-tool` | Picks between Serena and Morphllm MCP tools by complexity score. | Rarely by hand; mostly internal routing. | Autonomous | Light-medium (`high` label but advisory) | src/superclaude/commands/select-tool.md |
| `/sc:spawn` | Breaks a large multi-domain operation into delegated subtasks. | Very large cross-cutting work. | Autonomous | Heavy (`high`) | src/superclaude/commands/spawn.md |
| `/sc:workflow` | Generates an implementation workflow from a PRD or feature spec. | Turning a PRD into implementation steps (lighter alternative to roadmap pipeline). | Autonomous | Heavy (`advanced`, 6 MCP servers) | src/superclaude/commands/workflow.md |

## 1b. Skills without their own command file (`src/superclaude/skills/*/SKILL.md`)

These are invoked by skill name (for example `/prd`, `/task-builder`) or auto-triggered by their description, not via an `/sc:` command file.

| Skill | What it does | When to reach for it | Interactive / autonomous | Cost | Source |
|---|---|---|---|---|---|
| `prd` | Creates or populates a Product Requirements Document from the template. | Defining a product or feature. | Autonomous | Heavy (462-line skill, multi-agent research) | src/superclaude/skills/prd/SKILL.md |
| `tech-research` | Deep technical investigation producing a research report with gaps, options, recommendations. | "How does X work and what would it take to change it". | Autonomous (file mentions interactive steps) | Heavy (1389 lines) | src/superclaude/skills/tech-research/SKILL.md |
| `tech-reference` | Creates a Technical Reference document for an already-built feature. | Documenting shipped functionality. | Autonomous | Heavy (1346 lines) | src/superclaude/skills/tech-reference/SKILL.md |
| `task-builder` | Builds an MDTM task file from a request or BUILD_REQUEST via parallel research and QA gates. | Any large or multi-file job you want planned as a checklist first. | Autonomous | Heavy (2517 lines) | src/superclaude/skills/task-builder/SKILL.md |
| `task` | Executes an MDTM task file item by item with subagents and progress tracking. | After task-builder produced a task file; also to resume one. | Autonomous | Heavy (depends on task file) | src/superclaude/skills/task/SKILL.md |
| `confidence-check` | Pre-implementation readiness check (90% threshold: duplicates, architecture, docs, OSS refs, root cause). | Before starting implementation. | Autonomous | Light (150 lines) | src/superclaude/skills/confidence-check/SKILL.md |
| `sc-crash-recovery` | Reconstructs "where was I" after a crash from pipeline artifacts, session logs, git, serena. | After a reboot, lost session, or interrupted sprint/roadmap run. | Autonomous | Medium-heavy (parallel subagents) | src/superclaude/skills/sc-crash-recovery/SKILL.md |
| `ccsession-tag` | Tags the current Claude session so `ccsession <name>` can resume it from the shell. | Before stepping away from a long session. | Autonomous | Light | src/superclaude/skills/ccsession-tag/SKILL.md |
| `sc-bare-review` | Infrastructure skill: sends 2-4 unscaffolded reviews to external models via a proxy and hands them to `/sc:adversarial`. | Not called directly by humans ("Delegate-only, no slash command"). | Autonomous | Heavy (external models) | src/superclaude/skills/sc-bare-review/SKILL.md |

The 17 protocol skills (`sc-recommend` plus 16 `sc-*-protocol`: adversarial, auggie-review, brainstorm, cleanup-audit, cli-portify, init-lite, pm, recommend, reflect, release-split, review-translation, roadmap, task, tasklist, troubleshoot, validate-roadmap, validate-tests) are the bodies behind the thin commands in Section 1 and are not meant to be invoked by name.

## 2. CLI subcommands (`superclaude` and `ic` console scripts)

Entry points [CODE-VERIFIED pyproject.toml:66-68]: `superclaude = "superclaude.cli.main:main"` and `ic = "superclaude.cli.ic:main"`. The root group is a Click group at src/superclaude/cli/main.py:18-20. Line numbers below are the decorator line, then the `def` line when they differ. CLI pipelines are autonomous by nature: they spawn headless Claude subprocesses and run to completion; the only "interactive" ones are the sprint attach/tmux surface.

### 2a. Top-level commands (src/superclaude/cli/main.py)

| Command | What it does | When to reach for it | Interactive / autonomous | Cost | Evidence |
|---|---|---|---|---|---|
| `superclaude install` | Installs core files, slash commands (default `~/.claude/commands/sc`), agents, skills into Claude Code. `--force`, `--list`. | First-time setup and after upgrading the package. | Autonomous | Light (file copy, no LLM) | main.py:29 / def install main.py:46 |
| `superclaude update` | Re-installs framework files to match the package version; equivalent to `install --force`. | After `pipx upgrade superclaude`. | Autonomous | Light | main.py:260 / def update main.py:266 |
| `superclaude install-skill <name>` | Installs one skill into `~/.claude/skills`. | Adding a single skill. | Autonomous | Light | main.py:313 / def install_skill main.py:325 |
| `superclaude mcp` | Installs and manages MCP servers (`--servers`, `--list`, `--scope local/project/user`, `--dry-run`). | Setting up Tavily, Context7, Serena, etc. | Interactive when run with no flags (CLAUDE.md:126 "Interactive install") | Light | main.py:215 / def mcp main.py:229 |
| `superclaude doctor` | Checks install health (pytest plugin, skills). `--verbose`. | Something seems not installed. | Autonomous | Light | main.py:352 / def doctor main.py:358 |
| `superclaude version` (also `--version`) | Prints version. | Bug reports. | Autonomous | Light | main.py:394 / def version main.py:395; `version_option` main.py:19 |
| `superclaude init-lite` | CLI twin of `/sc:init-lite`: safe audit of project-local context surfaces (`--dry-run`, `--scaffold`). | Onboarding a project. | Autonomous | Light | init_lite.py:283 / def init_lite_command init_lite.py:322; registered main.py:434 |

### 2b. Pipeline groups

| Command | What it does | When to reach for it | Interactive / autonomous | Cost | Evidence |
|---|---|---|---|---|---|
| `superclaude sprint run <index_path>` | Executes a multi-phase sprint from a tasklist index, phase by phase, in tmux by default (`--start/--end`, `--resume`, `--dry-run`, `--no-tmux`, `--task-parallelism`, stall timeouts). | After `/sc:tasklist` produced a bundle and you want unattended execution. | Autonomous (long-running, background tmux) | Heavy (one Claude subprocess per task/phase) | sprint/commands.py:72 / def run :234; group :16-17; registered main.py:402 |
| `superclaude sprint attach` | Attaches to the running sprint tmux session. | Watching a live sprint. | Interactive | Light | sprint/commands.py:580 / :581 |
| `superclaude sprint status` | Shows sprint status without attaching. | Quick check. | Autonomous | Light | sprint/commands.py:592 / :593 |
| `superclaude sprint logs` | Tails the sprint execution log (`--lines`, `--follow`). | Debugging a run. | Autonomous | Light | sprint/commands.py:604 / :618 |
| `superclaude sprint kill` | Stops a running sprint (`--force`). | Abort. | Autonomous | Light | sprint/commands.py:629 / :635 |
| `superclaude sprint verify-checkpoints <output_dir>` | Verifies and optionally recovers checkpoint reports (`--recover`, `--json`). | After a sprint, before trusting results. | Autonomous | Light-medium | sprint/commands.py:647 / :663 |
| `superclaude sprint rerun-tasks` | Re-executes only named failed tasks within one phase. | Fixing a few failed tasks without rerunning a phase. | Autonomous | Medium | sprint/commands.py:705 / :793 |
| `superclaude roadmap run <input_files...>` | Runs the roadmap generation pipeline (extract, generate with `--agents`, diff, debate, score, merge, spec-fidelity, test-strategy, certify, remediate) on 1-3 spec/TDD/PRD files. | Producing a validated roadmap headlessly; `/sc:roadmap` mirrors it in-session. | Autonomous | Heavy (multi-agent, many steps; `--depth`) | roadmap/commands.py:32 / def run :256; registered main.py:406 |
| `superclaude roadmap validate <output_dir>` | Validates roadmap pipeline outputs (single-agent reflection, or adversarial merge with `--agents`). | After `roadmap run`. | Autonomous | Medium-heavy | roadmap/commands.py:430 / :463 |
| `superclaude roadmap accept-spec-change <output_dir>` | Updates the stored spec hash after accepted deviations so `--resume` does not force regeneration. | You intentionally edited the spec mid-pipeline. | Autonomous | Light | roadmap/commands.py:404 / :406 |
| `superclaude tasklist validate <output_dir>` | Validates tasklist fidelity against a roadmap (`--roadmap-file`, `--tasklist-dir`). | After tasklist generation, before sprint. | Autonomous | Medium | tasklist/commands.py:31 / :73; group docstring "Tasklist validation commands." :16 |
| `superclaude cleanup-audit run <target>` | Runs the multi-pass read-only cleanup audit (`--pass`, `--batch-size`, `--focus`). | Headless repo audit; CLI twin of `/sc:cleanup-audit`. | Autonomous | Heavy | cleanup_audit/commands.py:24 / :61; registered main.py:410 |
| `superclaude cli-portify run <workflow>` | Ports a skill workflow into a programmatic CLI pipeline (`--dry-run`, `--resume`, `--gate-mode`). | Framework contributors. | Autonomous | Heavy | cli_portify/commands.py:30 / :115; registered main.py:418 |
| `superclaude prd run <request>` | Multi-step PRD generation pipeline (`--product`, `--where`, `--tier`, `--dry-run`). | Headless PRD creation. | Autonomous | Heavy | prd/commands.py:32 / :79; registered main.py:422 |
| `superclaude prd resume` | Resumes an interrupted PRD pipeline from a step. | After a crash or stop. | Autonomous | Heavy | prd/commands.py:135 / :171 |
| `superclaude eval doctor` | Verifies host preconditions for `eval run`; refuses non-Linux hosts (README.md:252-254). | Before first eval run. | Autonomous | Light | eval/commands.py:767 / :821; registered main.py:426 |
| `superclaude eval list` | Lists suite manifests under `cli/eval/suites/`. | Discovering eval suites. | Autonomous | Light | eval/commands.py:924 / :941 |
| `superclaude eval describe` | Prints a validated, expanded suite manifest. | Checking a suite before running it. | Autonomous | Light | eval/commands.py:1205 / :1241 |
| `superclaude eval run --suite <stem>` | Runs a cliEval suite end to end in isolated HOMEs driving real Claude Code (`--parallel`, `--no-mcp`, `--no-pty`, `--junit`, `--json`). | Regression-testing commands/skills against real Claude behavior. Linux only. | Autonomous | Heavy (real Claude sessions per eval) | eval/commands.py:1553 / :1655 |
| `superclaude recommend cache get/put`, `telemetry append`, `eval run`, `eval plugin`, `dispatch` | Deterministic helper plumbing called by the `sc-recommend` skill (lookup cache, telemetry JSONL, opt-in `--eval` panel, plugin adoption gate, hot-path dispatch). | Not for humans; the skill calls these. | Autonomous | Light (except `eval run`) | recommend/commands.py:34 group docstring "sc-recommend lookup-cache deterministic helpers." :35; cache :51-90; telemetry :145-172; eval :196-346; dispatch :403/:434 |

### 2c. `ic` launcher

| Command | What it does | When to reach for it | Interactive / autonomous | Cost | Evidence |
|---|---|---|---|---|---|
| `ic [alias] [-p preset] [-H/-S/-O model] [--no-yolo] [-- claude-args]` | Bash wrapper that launches `claude` with `--dangerously-skip-permissions` by default and remaps the haiku/sonnet/opus model slots from aliases/presets in `~/.aienv`. | Starting a Claude session with non-default model routing. | Interactive (starts a Claude session) | Depends on models chosen | src/superclaude/cli/ic.py:12-15 execs src/superclaude/scripts/ic (usage header lines 2-21) |

**Safety note for the guide:** `ic` skips Claude Code permission prompts unless `--no-yolo` is passed [CODE-VERIFIED scripts/ic header]. A user guide should say this plainly.

### 2d. Code present but NOT registered as a CLI command

- `src/superclaude/cli/audit/` (40+ modules: wiring_gate, dead_code, credential_scanner, ...) has no `click.group`/`command` registration and is not added in main.py:396-434. It is library code used by other pipelines. [CODE-VERIFIED by grep of decorators]
- `src/superclaude/cli/pipeline/` same: library, no registration.
- `install_agents.py`, `install_commands.py`, `install_core.py`, `install_hooks.py`, `install_mcp.py`, `install_skills.py`, `install_templates.py` are helpers behind `install`/`mcp`, not separate subcommands.
- No `swarm` command exists anywhere in src/superclaude/cli on this branch (grep for "swarm" returned nothing). See Section 5.

## 3. Documented recommended workflows and command sequences

Each block quotes the source path and line. Whether each sequence still matches the current command files is tagged.

### 3.1 Spec-to-execution pipeline (the IronClaude-native path)
Source: docs/analysis-sc-tasklist.md:627-640 ("Pipeline chaining (typical workflow)")
1. `superclaude roadmap run tdd.md --prd-file prd.md --output ./output`
2. `/sc:tasklist @./output/roadmap.md --output ./output/tasklist/`
3. `superclaude tasklist validate ./output/tasklist/`
4. `superclaude sprint run ./output/tasklist/tasklist-index.md`
Tag: [CODE-VERIFIED] every step maps to a registered command (roadmap/commands.py:32, commands/tasklist.md:76, tasklist/commands.py:31, sprint/commands.py:72). Optional extras implied by command files: `superclaude roadmap validate <output_dir>` or `/sc:validate-roadmap` after step 1 (validate-roadmap.md description), `/sc:reflect --mode pre` before step 4 (reflect.md argument-hint line 10).
Note: this sequence lives in an analysis doc, not in docs/user-guide/. The user guide (commands.md) never mentions roadmap, sprint, validate-roadmap, release-split, cleanup-audit, auggie-review, init-lite, cli-portify, review-translation, or tdd (grep count 0 in docs/user-guide/commands.md).

### 3.2 Brainstorm pipeline
Source: docs/user-guide/brainstorm.md:206-226 ("Pipeline Position")
`topic -> /sc:brainstorm -> optional enrichment (/sc:analyze | /sc:research | tech-research) -> seed-brief.md -> /sc:adversarial --source seed-brief.md --generate spec -> merged-requirements.md -> --handoff none | design | tasklist | task`
Handoff table: docs/user-guide/brainstorm.md:165-174 (`--handoff task` invokes the task-builder skill; `--handoff tasklist` invokes sc-tasklist-protocol). Convergence gating: brainstorm.md:157-163 (score >= 0.65 PASS, >= 0.50 PARTIAL, < 0.50 FAIL).
Tag: [CODE-VERIFIED] against commands/brainstorm.md:71, :133-134, :175.

### 3.3 "Visual Map: When to Use What"
Source: docs/user-guide/commands.md:1033-1082
brainstorm -> research -> workflow -> spawn -> design -> implement -> test -> build -> troubleshoot -> improve/cleanup -> document -> analyze/spec-panel.
Tag: commands exist [CODE-VERIFIED], but the map predates the roadmap/tasklist/sprint pipeline and the task-builder/task skills, so it omits the heavier spec-driven route in 3.1.

### 3.4 commands.md "Typical Workflows"
Source: docs/user-guide/commands.md:1505-1660
| Workflow | Sequence | Lines |
|---|---|---|
| New project setup | Serena `activate_project` + `onboarding`, and/or `/sc:index-repo` | 1507-1526 |
| New feature | `/sc:brainstorm` -> `/sc:design --type api` -> `/sc:workflow` -> `/sc:implement` -> `/sc:test --coverage` | 1528-1538 |
| Bug fix | `/sc:troubleshoot "error" --trace` -> `/sc:implement fix` -> `/sc:test` | 1540-1548 |
| Refactoring | `/sc:analyze --type quality` -> `/sc:improve --focus X` -> `/sc:cleanup --scope module` -> `/sc:test` | 1550-1559 |
| Code review | `/sc:analyze PR --type quality`, then `--type security`, then `/sc:test --type integration` | 1561-1569 |
| Business idea to spec | brainstorm -> research -> business-panel (discussion, debate) -> design -> spec-panel critique | 1571-1584 |
| Improving a spec/PRD | `/sc:spec-panel --mode socratic` -> answer -> `--mode critique` -> `--iterations 2` | 1586-1597 |
| Architecture validation | design -> spec-panel with named experts -> fix -> workflow -> implement | 1599-1612 |
| Pitch/strategy | business-panel discussion -> debate -> `--synthesis-only` | 1614-1625 |
| Enterprise feature | brainstorm -> business-panel -> design -> spec-panel -> workflow `--depth deep` -> spawn -> task -> analyze security -> test | 1627-1641 |
Tags: Bug fix [CODE-CONTRADICTED in part]: current troubleshoot.md argument-hint (line 10) has no `--trace` flag and offers `--fix` itself, so the separate `/sc:implement fix` step is optional. Code review [OUTDATED]: `/sc:auggie-review` (commands/auggie-review.md) is the purpose-built PR reviewer and is not mentioned. Remaining rows: commands exist; flag-level accuracy UNVERIFIED (flags are prompt conventions, not parsed code).

### 3.5 Quick-start "First Project Session"
Source: docs/getting-started/quick-start.md:213-256
`/sc:brainstorm` -> `/sc:load src/` -> `/sc:analyze --focus architecture` -> `/sc:workflow` -> `/sc:implement` -> `/sc:test --coverage` -> `/sc:save`.
Tag: commands exist. `/sc:load` and `/sc:save` require Serena MCP (load.md, save.md `mcp-servers: [serena]`).

### 3.6 Session lifecycle
Source: docs/user-guide/session-management.md:110-157 and 236-250
Start: `/sc:load` -> `/sc:reflect` -> work. End: `/sc:reflect` -> `/sc:save`.
Tag: [CODE-CONTRADICTED] for the `/sc:reflect` part; see Gap G7.

### 3.7 cliEval loop (Linux only)
Source: docs/user-guide/eval-pipeline.md:41-61 and 286-333
`uv run superclaude eval doctor` -> `eval list` -> `eval describe --suite real` -> `eval run --suite real` (subset with `--eval E1 --eval E2 --verbose`; CI with `--output-dir ... --json --junit`).
Tag: [CODE-VERIFIED] subcommands and flags at eval/commands.py:767-1654; Linux-only gate per README.md:245-258.

### 3.8 Task-file route (skills, not commands)
No user-guide doc describes it. From skill descriptions: `task-builder` builds an MDTM task file (src/superclaude/skills/task-builder/SKILL.md frontmatter), then `task` executes it (src/superclaude/skills/task/SKILL.md frontmatter). `/sc:troubleshoot` Tier 3 and `/sc:brainstorm --handoff task` both route into task-builder (troubleshoot.md description; brainstorm.md:175). Tag: [CODE-VERIFIED] at frontmatter level; no human-facing walkthrough exists (Gap G10).

## 4. Onboarding: what a new user must know

| Step | What to do | Evidence | Status |
|---|---|---|---|
| 1. Prerequisites | Python >= 3.10, UV for development, Claude Code installed. | README.md:237-241 | [CODE-VERIFIED] pyproject.toml declares the package; Python floor per CLAUDE.md:385 |
| 2a. Install from source (IronClaude fork) | `git clone https://github.com/IronbellyOrg/IronClaude`, `cd IronClaude`, `make install` (editable `uv pip install -e ".[dev]"`), `make verify`. | Makefile:5-10, :28; README.md:70-74 says `make dev` | `make dev` does NOT exist (Gap G1). Use `make install`. |
| 2b. Install package (as documented) | `pipx install superclaude` | README.md:59-61 | UNVERIFIED that the PyPI `superclaude` package is this fork rather than upstream SuperClaude (Gap G2). |
| 3. Install assets into Claude Code | `superclaude install` copies core files, slash commands (`~/.claude/commands/sc`), agents, skills, hooks, templates. `--force` to overwrite, `--list` to inspect. | main.py:29-46, hooks at :191, templates at :201 | [CODE-VERIFIED] |
| 4. Health check | `superclaude doctor` (`--verbose`). | main.py:352-358 | [CODE-VERIFIED] |
| 5. Optional MCP servers | `superclaude mcp` (interactive), `superclaude mcp --list`, `superclaude mcp --servers tavily context7`. Many heavy commands assume auggie, serena, tavily, context7, sequential. | main.py:215-229; CLAUDE.md:125-129, 315-335 | [CODE-VERIFIED] command; server availability per-user |
| 6. First commands in Claude Code | `/sc:help` for the list; `/sc:recommend "<goal>"` to get a paste-ready prompt routed to the right command or skill; `/sc:init-lite` to audit a project's context surfaces safely. | commands/help.md; commands/recommend.md:21-27; commands/init-lite.md | Getting-started docs never mention `/sc:help`, `/sc:recommend`, or `/sc:init-lite` (Gap G9). |
| 7. Know the hard rule | When a message starts with `/sc:<command>`, the paired skill must be invoked first; under context pressure, start a new chat rather than improvise. | CLAUDE.md:9-14 | [CODE-VERIFIED] rule text; enforcement for recommend via hooks/scripts/sc-recommend-phase0.sh |
| 8. Know the freshness hook | Edits are blocked on files not Read in the last 30 minutes; the assistant must Read then retry. | README.md:40; docs/user-guide/freshness-hooks.md:17, 40-45; hooks/scripts/freshness-pre-edit.sh | [CODE-VERIFIED] script exists |
| 9. Know the `ic` launcher | `ic` starts Claude with `--dangerously-skip-permissions` unless `--no-yolo`; model slots come from `~/.aienv`. | scripts/ic header lines 2-21; pyproject.toml:68 | [CODE-VERIFIED]; not documented in any user guide (Gap G11) |
| 10. After a crash | Use the `sc-crash-recovery` skill ("where was I"). | skills/sc-crash-recovery/SKILL.md | [CODE-VERIFIED] skill exists; no user-guide mention |
| 11. Eval harness | Linux only; run `superclaude eval doctor` first. | README.md:245-258; eval-pipeline.md:44-45 | [CODE-VERIFIED] |

## 5. Gaps and contradictions between docs and code

| ID | Doc claim (path:line) | What the code shows | Tag | Guide impact |
|---|---|---|---|---|
| G1 | `make dev` installs the editable package (README.md:73, :172; CLAUDE.md:106, :367) | No `dev:` target in Makefile. Editable install is `make install` (Makefile:5-10); `make help` calls it "RECOMMENDED" (Makefile:531). | CODE-CONTRADICTED | Guide must say `make install`, not `make dev`. |
| G2 | `pipx install superclaude` installs IronClaude (README.md:59-61) | Package name is `superclaude` (pyproject.toml:6). Whether the PyPI `superclaude` is this fork or upstream SuperClaude was not checked. | UNVERIFIED | Recommend source install for IronClaude until confirmed. |
| G3 | `superclaude tasklist run <roadmap-dir>` (README.md:94) | `tasklist` group has only `validate` (tasklist/commands.py:31; group docstring "Tasklist validation commands." :16). Tasklist generation is the `/sc:tasklist` slash command. | CODE-CONTRADICTED | Remove `tasklist run`; document `/sc:tasklist` + `superclaude tasklist validate`. |
| G4 | Install options `--components`, `--list-components`, `--dry-run`, `--yes`, plus `SuperClaude backup` / `uninstall` (docs/getting-started/installation.md:254-262, :279-285, :326-350) | `install` accepts only `--target`, `--force`, `--list` (main.py:29-45). No `backup` or `uninstall` command is registered (main.py:29-434). | CODE-CONTRADICTED | Installation doc is upstream-era; rewrite. |
| G5 | Version: 4.1.5 (installation.md:281), 4.2.0 (CLAUDE.md:74, :384) | `pyproject.toml:7` and `src/superclaude/__init__.py:8` say 4.3.5; a second `src/superclaude/__version__.py:3` says 0.4.0. CLI prints `__init__` value (main.py:15, :19). | CODE-CONTRADICTED | Guide should not hardcode a version; `superclaude --version` is authoritative. Stray `__version__.py` is a code smell. |
| G6 | Command and agent counts: help.md lists 24 commands (help.md:30-55) and warns it "may become outdated" (:153); sc.md lists 5; CLAUDE.md:210 says "/pm, /research, /index-repo, and 27 others"; installation.md:5 "21 Commands, 14 Agents & 6 MCP Servers"; agents.md:3 "16 domain specialist agents" | 42 command files in src/superclaude/commands (excluding README); 38 agent files in src/superclaude/agents (excluding README). | CODE-CONTRADICTED | `/sc:help` is stale. Missing from it: adversarial, auggie-review, cleanup-audit, cli-portify, init-lite, pm, recommend, release-split, research, index-repo, review-translation, roadmap, tasklist, tdd, validate-roadmap, validate-tests, agent, sc. |
| G7 | `/sc:reflect [--scope project\|session]` is a Serena memory progress check (docs/user-guide/session-management.md:59-82; help.md:47) | reflect.md is the tiered UC-1 pre / UC-2 post audit; `--scope <path>`; legacy grammar is `--type task --analyze\|--validate` (reflect.md:10, :20, :97-106). | CODE-CONTRADICTED | Session lifecycle docs give a flag form that no longer exists. |
| G8 | commands/README.md:15-21 says commands are copies of `plugins/superclaude/commands/` and to edit there first | CLAUDE.md:141 and README.md:143 say `src/superclaude/` is the source of truth. `plugins/superclaude/commands/` holds only 30 files vs 42 in src. | CODE-CONTRADICTED | Contributor confusion; not user-facing but should be fixed. |
| G9 | Getting-started (quick-start.md, installation.md) | Neither file mentions `/sc:help`, `/sc:recommend`, or `/sc:init-lite` (grep of docs/getting-started). | Doc gap | Onboarding should lead with `/sc:recommend`. |
| G10 | User guide coverage | docs/user-guide/commands.md has zero mentions of roadmap, sprint, validate-roadmap, release-split, cleanup-audit, auggie-review, init-lite, cli-portify, review-translation, tdd; no user doc for the task-builder/task skills or `sc-crash-recovery`. Sprint is only covered in docs/sprint-cli-deep-dive.md (developer depth). | Doc gap | The IronClaude-specific pipelines are the least documented for end users. |
| G11 | `ic` launcher | Shipped as a console script (pyproject.toml:68; cli/ic.py; scripts/ic) but not in README, CLAUDE.md, or any user-guide file. Defaults to `--dangerously-skip-permissions`. | Doc gap | Must be documented with a safety warning. |
| G12 | Swarm / pr-submit / cli-eval surfaces | No `swarm` CLI group, and no `swarm-wizard`, `pr-submit`, or `cli-eval` command or skill exists in src/superclaude on this branch (grep returned nothing; not among the 27 skill dirs). These names do appear in the IC-Harness session's installed skill list, so they likely live on another IronClaude branch or an installed copy. | UNVERIFIED (location) | Do not document them from this branch. Confirm the source branch first. |
| G13 | Thin commands activate skills by name | cli-portify.md:81 says `> Skill sc:cli-portify-protocol` but the skill's frontmatter name is `sc-cli-portify-protocol`; validate-roadmap.md:74 and recommend.md:54 use hyphen names that match. Others use colon names matching frontmatter (e.g. sc-adversarial-protocol has `name: sc:adversarial-protocol`). | UNVERIFIED (whether Claude Code resolves the colon form for cli-portify) | Possible activation failure for `/sc:cli-portify`; needs a live test. |
| G14 | Agent manual-invoke names `@agent-security`, `@agent-frontend`, `@agent-backend`, `@agent-qa`, `@agent-devops` (quick-start.md:105, :262-268; installation.md:294) | Actual agent files are `security-engineer`, `frontend-architect`, `backend-architect`, `quality-engineer`, `devops-architect`. agents.md also points to `superclaude/Agents/` (agents.md core concepts) while the real path is src/superclaude/agents/. | CODE-CONTRADICTED | Examples should use real agent names. |
| G15 | Upstream-era install references: `git clone .../SuperClaude-Org/SuperClaude_Framework` + `./install.sh` (CLAUDE.md:351-353), npm `@bifrost_inc/superclaude` (quick-start.md:88-89), `pip install SuperClaude` (installation.md:145) | No `install.sh` at repo root (ls). README.md:71 uses the IronbellyOrg fork URL. | CODE-CONTRADICTED (install.sh); UNVERIFIED (npm package) | Guide should use only the fork URL path. |
| G16 | commands.md "Bug Fix" uses `/sc:troubleshoot "error" --trace` (commands.md:1540-1548) | troubleshoot.md argument-hint (line 10) lists `--type`, `--depth`, `--scope`, `--no-escalate`, `--fix`, `--models`, `--output-dir`, `--no-doc-discovery`, `--no-mcp`; no `--trace`. | CODE-CONTRADICTED | Update example. |
| G17 | Behavioral flags (`--think`, `--uc`, `--delegate`, etc. in help.md:57-133 and docs/user-guide/flags.md) | These are prompt conventions read by the model, not parsed by any code. Whether a given command honors them is model-dependent. | UNVERIFIED (behavior) | Present as "hints", not guaranteed switches. |
| G18 | README.md:256-258 "no `--ci` flag", CI deferred | docs/user-guide/eval-pipeline.md:305-317 shows a "CI invocation" using `--json --junit`. Not a contradiction (no `--ci` flag exists), but the two docs frame CI differently. | Soft inconsistency | Say "manual CI wiring possible; no official CI support". |
| G19 | confidence-check skill | Frontmatter `name: Confidence Check` (with a space) while the directory is `confidence-check`. | UNVERIFIED (invocation name users must type) | Confirm the slash name before documenting. |

## Summary

- **Surface size:** 42 slash command files (18 thin wrappers that delegate to a protocol skill), 27 skill directories (17 protocol bodies plus 10 standalone skills such as prd, tdd, tech-research, tech-reference, task-builder, task, confidence-check, sc-crash-recovery, ccsession-tag, sc-bare-review), 38 agent files, and a `superclaude` CLI with 6 top-level commands, `init-lite`, and 8 groups (sprint, roadmap, cleanup-audit, tasklist, cli-portify, prd, eval, recommend), plus the separate `ic` launcher.
- **Most important user path that docs underserve:** spec -> `superclaude roadmap run` -> `/sc:tasklist` -> `superclaude tasklist validate` -> `superclaude sprint run` (Section 3.1), and the task-builder -> task skill route (Section 3.8).
- **Top onboarding fixes:** `make install` not `make dev` (G1); drop `tasklist run` (G3); rewrite installation.md from the fork's real CLI (G4, G15); regenerate `/sc:help` (G6); lead onboarding with `/sc:recommend` (G9); document `ic` with its permission-skip warning (G11).
- **Unresolved:** PyPI package identity (G2), location of swarm/pr-submit/cli-eval (G12), cli-portify skill activation name (G13), confidence-check invocation name (G19).

## 6. MASTER delta (authoritative): /Users/cmerritt/GFxAI/IronClaude-tier-tools @ 50a8c7f4

All paths in this section are relative to /Users/cmerritt/GFxAI/IronClaude-tier-tools. Method: `diff` of directory listings and `cmp` of each file between the June branch and master, then frontmatter read of every new or changed file.

### 6.1 Slash commands: removed on master (drop from the guide)

| Command | June source | Master status |
|---|---|---|
| `/sc:estimate` | IronClaude/src/superclaude/commands/estimate.md | REMOVED (file absent; also removed from master help.md and docs/user-guide/commands.md) |
| `/sc:select-tool` | IronClaude/src/superclaude/commands/select-tool.md | REMOVED (file absent; removed from master help.md) |
| `/sc` (dispatcher) | IronClaude/src/superclaude/commands/sc.md | REMOVED (file absent; removed from commands.md file map) |

### 6.2 Slash commands: added on master

| Command | What it does (one plain sentence) | When a human should reach for it | Interactive / autonomous | Cost | Source (activation line) |
|---|---|---|---|---|---|
| `/sc:pr-submit` | Opens a PR on the fork and arms an in-session monitor that waits for the Augment review, re-grades and verifies each finding, sends verified ones to `/sc:troubleshoot`, and at higher `--monitor` levels fixes, validates, pushes, replies, and resolves. | When you are ready to open a PR and want review findings handled for you. `--monitor 0` just opens and watches; 3 is full auto-remediation. | Attended in-session loop (you keep the session open); autonomy scales with `--monitor {0,1,2,3}` | Heavy (`advanced`, repeated rounds, capped by `--max-rounds N<=5`) | src/superclaude/commands/pr-submit.md:71 -> skills/sc-pr-submit-protocol |
| `/sc:swarm-wizard` | Plain-language interview that turns "what do you want reviewed and why" into the right `superclaude swarm` lens/transport/flags, proves it with a stub dry run, then offers to launch, monitors, and explains results. | Any time you want several AI models to review code, docs, or a spec and do not want to learn swarm settings. | Interactive (interview; `--yes` skips confirmations) | Light to set up; heavy when `--real` launches the swarm | src/superclaude/commands/swarm-wizard.md:68 -> skills/sc-swarm-wizard-protocol; user doc docs/swarm/wizard-guide.md |
| `/sc:cli-eval` | Authors a new cliEval suite (propose, critique, debate, author, validate, document) or interactively picks and supervises a run of an existing suite. | Writing or running real-Claude regression evals for commands and skills. Linux host for runs. | Interactive (suite selection; create path debates) | Heavy (`advanced`) | src/superclaude/commands/cli-eval.md:70 -> skills/sc-cli-eval-protocol |
| `/sc:post-release` | After a release ships, synchronizes and creates the version's external surface: user docs, technical docs, install/deploy scripts validated by real end-to-end runs, and human-run e2e test guides. | Right after a release is cut. | Autonomous | Heavy (`high`, Wave 0-5 protocol) | src/superclaude/commands/post-release.md:63 -> skills/sc-post-release-protocol |

### 6.3 Slash commands: behavior changed on master (replace the June rows)

| Command | June behavior | Master behavior | Source |
|---|---|---|---|
| `/sc:implement` | Prompt-only "feature implementation with persona activation and MCP integration" (`complexity: standard`, 4 MCP servers). | "Middleweight spec executor": walks a spec/PRD/tasklist (or informal notes or an inline prompt) task by task with per-task spec-compliance QA and a one-line-per-task ledger. Args `<path-or-prompt> [--resume] [--ledger <path>] [--skip-final-review]`. Now a thin wrapper. Cost: medium to heavy depending on spec size. | src/superclaude/commands/implement.md:75 -> skills/sc-implement-protocol (160 lines) |
| `/sc:workflow` | Prompt-only "structured implementation workflows from PRDs" (`advanced`, 6 MCP servers). | "Generate a phased implementation plan from a PRD, spec, or feature prompt": writes `.dev/workflow/<slug>/plan.md` + `return-contract.yaml`, does not write code or sprint tasklists. Args `<path-or-prompt> [--strategy systematic\|agile\|enterprise] [--depth quick\|standard\|deep] [--output DIR] [--handoff none\|design\|implement\|tasklist]`; `--depth shallow\|normal` and `--parallel` are legacy. Now `complexity: standard`. | src/superclaude/commands/workflow.md:53 -> skills/sc-workflow-protocol (64 lines); docs/user-guide/commands.md (master diff) |
| `/sc:reflect` | UC-1/UC-2 tiered audit. | Same, plus `--no-reachability` in the argument-hint. | src/superclaude/commands/reflect.md:10, :142 |
| `/sc:recommend` | `--plugin`, `--eval`. | Adds `--minstar <N>` to the argument-hint. | src/superclaude/commands/recommend.md:8, :56 |
| `/sc:pm`, `/sc:help`, others | | Master trimmed Sequential and Magic MCP references (help.md example now uses `--c7` instead of `--magic`; CLAUDE.md optional MCP list now only Playwright). Remaining 25 changed files differ only cosmetically or in MCP lists (not separately audited line by line). | git-free `diff` of each file |

Unchanged in purpose on master (June rows in Section 1 stand): adversarial, agent, analyze, auggie-review, brainstorm, build, business-panel, cleanup, cleanup-audit, cli-portify, design, document, explain, git, help, improve, index, index-repo, init-lite, load, pm, recommend, release-split, research, review-translation, roadmap, save, spawn, spec-panel, task, tasklist, tdd, test, troubleshoot, validate-roadmap, validate-tests.

**Master command count:** 43 command files excluding README (42 June - 3 removed + 4 added).

### 6.4 Skills added on master (no own command file unless noted)

| Skill | What it does | When to reach for it | Interactive / autonomous | Cost | Source |
|---|---|---|---|---|---|
| `roadmap` | Phased implementation roadmap from any input (PRD, TDD, prompt) producing a roadmap doc, BUILD_REQUEST files, and MDTM task files by composing task-builder and task. Distinct from `/sc:roadmap` (the spec-to-roadmap pipeline). | Planning a build as executable task files. | Autonomous | Heavy (2678 lines) | src/superclaude/skills/roadmap/SKILL.md |
| `readme` | Creates or populates a README from the project template. | Writing a README. | Autonomous | Heavy (2161 lines) | src/superclaude/skills/readme/SKILL.md |
| `operational-guide` | Creates or populates an operational guide for a deployment/setup procedure. | Documenting an ops procedure. | Autonomous | Heavy (1656 lines) | src/superclaude/skills/operational-guide/SKILL.md |
| `sc-implement-protocol`, `sc-workflow-protocol`, `sc-pr-submit-protocol`, `sc-swarm-wizard-protocol`, `sc-cli-eval-protocol`, `sc-post-release-protocol` | Protocol bodies behind the new or changed commands in 6.2 / 6.3. | Not invoked by name. | n/a | n/a | src/superclaude/skills/<name>/SKILL.md |

**Master skill count:** 36 directories (27 June + 9 added). Agents added on master: eval-docs-loader, eval-run-reporter, eval-suite-author, reflect-reviewer, reuse-auditor (44 agent .md files incl. README vs 39 June).

### 6.5 CLI on master (src/superclaude/cli/main.py)

Top-level commands unchanged in name: `install` (main.py:29/46), `mcp` (:233/247), `update` (:278/284), `install-skill` (:366/378), `doctor` (:405/411), `version` (:447/448). `install` options still only `--target`, `--force`, `--list`. Master `install` and `update` additionally call `wire_ccsession` (main.py:64, :296) and `install_user_setup` (main.py:83, :217, :302, :348); installation.md on master says `superclaude install` deploys core instructions, a Bash inspection batching policy, skills, agents, and hooks under `~/.claude/` and is "active in every project that loads normal user configuration" (master installation.md diff, "Global policy activation").

Groups registered (main.py:455-495): sprint :455, roadmap :459, cleanup-audit :463, tasklist :467, cli-portify :471, prd :475, eval :479, **swarm :483 (NEW)**, recommend :487, init-lite :491, **reflect :495 (NEW)**.

Line numbers for existing groups shifted on master: sprint run :72/252, attach :617/618, status :629/630, logs :641/655, kill :666/672, verify-checkpoints :684/708, rerun-tasks :757/845; prd run :32/90, resume :148/184. Roadmap, tasklist, cleanup-audit, cli-portify, eval, recommend, init-lite line numbers match Section 2.

**New CLI commands on master:**

| Command | What it does | When to reach for it | Interactive / autonomous | Cost | Evidence |
|---|---|---|---|---|---|
| `superclaude swarm run <spec_path>` | Runs a multi-model swarm review job: Wave 0 preflight then Wave 1 dispatch (`--lens`, `--target`, `--transport`, `--reviewers`, `--detached`, `--tui`, `--resume`, `--stdin`). | Multi-model review of code/docs/spec; humans should usually start with `/sc:swarm-wizard`. | Autonomous (can detach to tmux) | Heavy (several external models) | swarm/commands.py:1368/1558; registered swarm/__init__.py:175; group swarm/__init__.py:100/101 "Orchestrate multi-model swarm execution." |
| `superclaude swarm scaffold` | Emits a starter JobSpec for a named lens. | Hand-building a job. | Autonomous | Light | swarm/commands.py:3773/3802; __init__.py:176 |
| `superclaude swarm validate` | Schema-checks a JobSpec JSON file. | Before `swarm run`. | Autonomous | Light | swarm/commands.py:242/261; __init__.py:178 |
| `superclaude swarm validate-lenses` | Validates the bundled lens registry. | Contributors. | Autonomous | Light | swarm/commands.py:420/432; __init__.py:179 |
| `superclaude swarm status` / `logs` / `attach` / `kill` | Report phase and status, dump or tail the log, re-attach to the detached tmux session, terminate it. | Monitoring a detached swarm. | attach is interactive; others autonomous | Light | status :2757/2811, logs :3193/3282, attach :3405/3407, kill :3597/3613; __init__.py:172-177 |
| `superclaude reflect run <tasklist>` | Runs the post-execution reflect gate as a top-level subprocess (validate, optional auto-fix with `--fix`, verify, promote). Options include `--depth`, `--transport`, `--reviewers`, `--fix/--no-fix`, `--max-fix-iterations`, `--dry-run`, `--resume`, `--tmux`, `--print-command`. | After executing a tasklist, to audit and optionally auto-fix deviations headlessly; CLI twin of `/sc:reflect --mode post`. | Autonomous | Heavy (multi-reviewer) | reflect/commands.py:216/330; group :47/48; README.md (master) adds `superclaude reflect run <tasklist.md> --fix`; guide docs/guides/reflect-cli-tools-guide.md |
| `superclaude reflect contract-status` | Reports detection-contract readiness without launching the audit. | Pre-check before `reflect run`. | Autonomous | Light | reflect/commands.py:76/95 |

### 6.6 Master documentation changes relevant to the guide

- README.md (master) adds the `superclaude reflect run <tasklist.md> --fix` line and a pointer to docs/guides/reflect-cli-tools-guide.md.
- docs/guides/ (master) holds user-adjacent release guides: reflect-cli-tools-guide.md, roadmap-cli-tools-release-guide.md, sprint-cli-tools-release-guide.md, cli-portify-and-pipeline-runner-guide.md, prd-skill-release-guide.md, tdd-skill-release-guide.md, SuperClaude-Developer-Guide-Commands-Skills-Agents.md.
- docs/swarm/ (master) is a full swarm doc set: wizard-guide.md (plain-language, for non-experts), command-reference.md, lens-catalog.md, runbook.md, monitoring-patterns.md, env-readiness.md, rollback-procedure.md, release-notes-v1.md.
- docs/user-guide/commands.md (master) drops estimate/select-tool/sc and rewrites the `/sc:workflow` section; it still does not cover roadmap, sprint, pr-submit, swarm-wizard, cli-eval, post-release, or the new spec-executor behavior of `/sc:implement`: master docs/user-guide/commands.md:78, :171, :236 still describe implement as "Feature Implementation / Write code" [CODE-CONTRADICTED by master implement.md:75 and its description].
- CLAUDE.md (master) adds an ABSOLUTE RULE: worktrees live under `<repo>/.dev/worktrees/<name>/`, never `.claude/worktrees/`, and the `EnterWorktree` tool must not be used.
- Unchanged on master: quick-start.md, agents.md, eval-pipeline.md, modes.md, session-management.md, memory-system.md.

### 6.7 Recommended workflows added or changed by master

- **Spec to code without the sprint CLI:** `/sc:workflow <spec> --handoff implement` -> `/sc:implement <plan or spec>` (workflow.md argument-hint; implement.md:75). This is a new middle path between ad-hoc `/sc:implement` and the full roadmap/tasklist/sprint pipeline.
- **Post-execution audit headlessly:** `superclaude sprint run ...` then `superclaude reflect run <tasklist.md> --fix` (README.md master; reflect/commands.py:216).
- **Multi-model review:** `/sc:swarm-wizard` (docs/swarm/wizard-guide.md section "The 30-second version") -> it drives `superclaude swarm run`.
- **PR flow:** `/sc:pr-submit --monitor N` -> verified findings routed to `/sc:troubleshoot` (pr-submit.md description).
- **Release close-out:** `/sc:release-split` (planning) ... ship ... `/sc:post-release` (post-release.md description: "Runs AFTER the release").

## 7. What is actually installed for this user (2026-10-01)

| Surface | What is there | Evidence | Meaning |
|---|---|---|---|
| `~/.claude/commands/` | Empty directory. `~/.claude/commands/sc` does not exist. | `ls -la /Users/cmerritt/.claude/commands/` (2 entries: . and ..) | No user-level `/sc:*` commands are installed. |
| `~/.claude/skills/` | Only `ccsession-tag` (byte-identical to master) plus 4 non-IronClaude entries: computer-use, orca-cli, orchestration (symlinks to ~/.agents/skills), skill-creator (symlink to ~/.vendor/anthropic-skills). | `ls -la /Users/cmerritt/.claude/skills`; `cmp` vs master SKILL.md | No IronClaude protocol skills installed at user level. |
| `~/.claude/agents/` | Empty (0 files). | `ls /Users/cmerritt/.claude/agents` | No user-level IronClaude agents. |
| `~/.claude/hooks/` | Only `pragmatic-subagent.js` (byte-identical to master src/superclaude/hooks/scripts/pragmatic-subagent.js). No freshness hooks, no sc-recommend-phase0.sh. | `ls -la ~/.claude/hooks`; `cmp` | Freshness gate and recommend Phase-0 gate are NOT active at user level. |
| `~/.claude/*.md` core files | None. `~/.claude/settings.json` has 0 matches for "superclaude" or "freshness". | `ls ~/.claude/*.md` (no matches); grep count 0 | Core framework instructions are not installed at user level. |
| `superclaude` CLI on PATH | `/Users/cmerritt/.local/bin/superclaude` -> pipx venv, **version 4.2.0**, installed from `file:///Users/cmerritt/GFxAI/IronClaude` (the June-line checkout, non-editable, symlink dated 2026-03-24) with `--force-reinstall`. Commands: cleanup-audit, cli-portify, doctor, install, install-skill, mcp, roadmap, sprint, tasklist, update, version. | `superclaude --version`; `superclaude --help`; pipx_metadata.json; direct_url.json | Installed CLI is stale: it lacks master's `prd`, `eval`, `swarm`, `recommend`, `init-lite`, and `reflect` groups. |
| `ic` launcher | Not on PATH (`which ic` -> not found). | `which ic` | The `ic` console script from master pyproject is not installed. |
| Project-level copy in IC-Harness (where `/sc:*` actually resolves in this workspace) | `/Users/cmerritt/GFxAI/IC-Harness/.claude/commands/sc/` (dir dated 2026-06-23): 45 command files plus README. vs master: has `estimate`, `sc`, `select-tool` (removed on master); lacks `post-release` (added on master); 15 files byte-identical to master, 27 differ (including implement.md and workflow.md, which are the OLD prompt-only versions). `/Users/cmerritt/GFxAI/IC-Harness/.claude/skills/` lacks `sc-implement-protocol`, `sc-post-release-protocol`, `sc-workflow-protocol`; also contains IC-Harness-own skills (agent-creator, agent-transformer, persona-agent, repo-cleanup, skill-eval, skill-transformer, understand-skills, skill-creator). | `ls`, `diff`, `cmp` against master src/superclaude | In this workspace `/sc:implement` and `/sc:workflow` behave like June, `/sc:post-release` is unavailable, and `/sc:estimate` / `/sc:select-tool` / `/sc` still appear even though master removed them. |

**Install-state conclusion:** a user guide written from master will not match what this user can run today. To match master the user would need, from /Users/cmerritt/GFxAI/IronClaude-tier-tools: `make install` (editable) or `pipx install --force /Users/cmerritt/GFxAI/IronClaude-tier-tools`, then `superclaude install --force` (or `superclaude update`), then a new Claude Code session (master installation.md "Global policy activation" says a running session does not reload). This was NOT executed (read-only task). Note that per master installation.md the install makes the policy active in every project, not only IronClaude.

## 8. Gap re-check against master (supersedes Section 5 status)

| ID | Status on master | Master evidence |
|---|---|---|
| G1 `make dev` | STILL OPEN | Makefile has `install:` at line 5 and no `dev:`; README.md:73, :175 and CLAUDE.md:106, :371 still say `make dev`. |
| G2 PyPI identity | STILL UNVERIFIED; also moot for this user | This user's pipx install comes from a local path (Section 7), not PyPI. |
| G3 `tasklist run` | STILL OPEN | README.md:94 still says `superclaude tasklist run <roadmap-dir>`; tasklist/commands.py still only has `validate` (:31/73). |
| G4 installation.md options/backup/uninstall | STILL OPEN | `install` options still `--target --force --list` (main.py:29-45). Master installation.md only added the "Global policy activation" block. |
| G5 version drift | STILL OPEN, plus a new layer | master pyproject.toml:7 and __init__.py:8 = 4.3.5; __version__.py:3 = 0.4.0; installed CLI = 4.2.0 (Section 7). |
| G6 stale counts / help | STILL OPEN | master help.md lists 22 commands vs 43 files; missing everything listed in G6 plus pr-submit, swarm-wizard, cli-eval, post-release, implement-as-spec-executor. agents.md (unchanged) still says 16 agents vs 43 agent files. |
| G7 reflect `--scope project\|session` | STILL OPEN | session-management.md unchanged on master; reflect.md:10 `--scope <path>`. |
| G8 commands/README.md says plugins/ is source | STILL OPEN (1-line change only on master) | master src/superclaude/commands/README.md diff = 1 line. |
| G9 onboarding omits help/recommend | STILL OPEN | quick-start.md unchanged on master. |
| G10 user-guide coverage | PARTLY CLOSED | Swarm now has docs/swarm/wizard-guide.md; reflect CLI has docs/guides/reflect-cli-tools-guide.md; roadmap/sprint have release guides in docs/guides/. Still no user-guide entry for pr-submit, cli-eval, post-release, task-builder/task, crash recovery. |
| G11 `ic` undocumented | STILL OPEN; and not installed for this user | pyproject still exposes `ic`; `which ic` not found. |
| G12 swarm/pr-submit/cli-eval missing | CLOSED on master | All three commands and protocol skills exist on master (Section 6.2); `swarm` CLI registered main.py:483. |
| G13 cli-portify activation name | STILL OPEN | master cli-portify.md:81 `> Skill sc:cli-portify-protocol`; master skill frontmatter `name: sc-cli-portify-protocol`. |
| G14 `@agent-security` etc. | STILL OPEN | quick-start.md and agents.md unchanged on master. |
| G15 upstream install refs | STILL OPEN | quick-start.md unchanged; CLAUDE.md install section unchanged apart from worktree/MCP edits. |
| G16 `--trace` | STILL OPEN | troubleshoot.md master argument-hint has no `--trace`. |
| G17 behavioral flags are hints | STILL APPLIES | help.md flags section only had Sequential/Magic rows removed. |
| G18 CI framing | STILL APPLIES | eval-pipeline.md unchanged. |
| G19 confidence-check name | STILL OPEN | master frontmatter `name: Confidence Check`. |
| G20 (NEW) `/sc:implement` docs describe old behavior | OPEN | master docs/user-guide/commands.md:78, :171, :236 vs master implement.md (spec executor). |
| G21 (NEW) installed surfaces lag master | OPEN | Section 7: stale 4.2.0 CLI, empty user-level commands/agents, June-era project copy in IC-Harness. |
| G22 (NEW) two different "roadmap" things | OPEN (naming clarity) | `/sc:roadmap` + `superclaude roadmap run` (spec -> roadmap pipeline, sc-roadmap-protocol) vs the `roadmap` skill (any input -> roadmap doc + BUILD_REQUESTs + MDTM task files). A guide must disambiguate. |

## Final summary (master-authoritative)

- **Master surface:** 43 slash commands (removed estimate, select-tool, sc; added pr-submit, swarm-wizard, cli-eval, post-release; implement and workflow rebuilt as thin wrappers over new protocol skills), 36 skill directories, 44 agent files incl. README, and a `superclaude` CLI with 6 top-level commands plus `init-lite` and 10 groups (sprint, roadmap, cleanup-audit, tasklist, cli-portify, prd, eval, swarm, recommend, reflect), plus the `ic` launcher.
- **What the user can run today is not master:** user-level `~/.claude` has no IronClaude commands, agents, or core files; the CLI on PATH is 4.2.0 from the June checkout; `/sc:*` in IC-Harness resolves from a June-23 project copy.
- **Highest-value guide content:** onboarding via `/sc:recommend`; the three execution routes (light: `/sc:implement`; middle: `/sc:workflow` -> `/sc:implement`; heavy: roadmap -> tasklist -> sprint -> `superclaude reflect run`); `/sc:swarm-wizard` for multi-model review; `/sc:pr-submit` for PRs; plus the install-state fix in Section 7.
