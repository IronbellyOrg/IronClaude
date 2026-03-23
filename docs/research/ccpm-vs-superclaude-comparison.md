# Deep Comparative Analysis: CCPM vs SuperClaude

## Execution Pipeline, Tasklist Management, and Parallel Strategy

**Date**: 2026-03-23
**Methodology**: Repository analysis via GitHub raw content extraction, source code review of SuperClaude CLI modules, and structural comparison of architectural decisions.

---

## 1. Executive Summary

CCPM and SuperClaude represent two fundamentally different philosophies for AI-agent-driven software delivery. CCPM is a **single-skill, GitHub-native workflow** that treats GitHub Issues as the canonical source of truth and uses git worktrees for physical isolation of parallel work. SuperClaude is a **comprehensive framework** with a supervised CLI pipeline, programmatic quality gates, KPI instrumentation, and in-process parallel execution via dependency-graph analysis.

| Dimension | CCPM | SuperClaude |
|-----------|------|-------------|
| Architecture | Single skill (SKILL.md + references/) | Framework (38 commands, 29 agents, 13 skills, Python CLI) |
| Source of truth | GitHub Issues | Markdown tasklist files |
| Parallel model | Git worktrees + multi-agent processes | Wave-Checkpoint-Wave (in-process ThreadPoolExecutor) |
| Quality gates | Convention-based preflight checks | Programmatic trailing gates, wiring gates, confidence gating |
| GitHub integration | Deep (gh CLI, sub-issues, labels, comments) | Minimal (branch/PR workflow only) |
| Tracking | Bash scripts (deterministic, no LLM) | TUI + KPI reports + TurnLedger (programmatic) |
| Complexity | ~20 files, single skill | ~100+ modules, full Python package |

---

## 2. Source of Truth

### CCPM: GitHub Issues

CCPM treats GitHub Issues as the shared project state:

- **PRD** -> `.claude/prds/<name>.md` (local, pre-sync)
- **Epic** -> `.claude/epics/<name>/epic.md` (local) -> GitHub Issue with label `epic,epic:<name>,feature`
- **Tasks** -> `.claude/epics/<name>/<N>.md` (local) -> GitHub sub-issues with label `task,epic:<name>`
- **Post-sync renaming**: Local task files are renamed from sequential `001.md` to actual GitHub issue numbers `1234.md`
- **Bidirectional sync**: Progress updates are posted as GitHub issue comments; issue state drives local file state

**Strengths**:
- Universally accessible -- any human or agent can see status via GitHub UI
- Labels, milestones, and PR workflows come free
- Multi-agent and human+agent collaboration is natural
- No proprietary database or format lock-in
- Sub-issue relationships via `gh-sub-issue` extension

**Weaknesses**:
- Requires network connectivity for sync operations
- GitHub API rate limits can throttle batch operations
- File renaming after sync creates a mutable identifier problem (local `001.md` becomes `1234.md`)
- Tight coupling to GitHub ecosystem (no GitLab, Bitbucket support)
- Progress comments can become noisy on long-running issues

### SuperClaude: Markdown Tasklist Files

SuperClaude uses structured markdown files as the canonical format:

- **Tasklist index** -> `tasklist-index.md` referencing phase files
- **Phase files** -> `phase-NN.md` containing `### T<PP>.<TT> -- Title` blocks
- **Task metadata** -> Inline in markdown: dependencies, classifiers, commands
- **Results** -> `SprintResult` dataclass with `PhaseResult[]` and `TaskResult[]`

**Strengths**:
- Fully offline -- no external service dependency
- Version-controlled alongside code (atomic commits)
- Deterministic parsing (regex-based task extraction)
- Rich metadata model (dependencies, classifiers, execution modes)
- No mutable identifier problem -- task IDs are stable

**Weaknesses**:
- Not visible outside the local development environment
- No built-in collaboration mechanism for multi-human teams
- Requires custom tooling to read/write (not a standard format)
- Progress is not accessible via web UI

### Verdict

CCPM's GitHub Issues approach is superior for **team visibility and collaboration**. SuperClaude's markdown approach is superior for **deterministic execution and offline reliability**. The ideal system would use markdown as the authoritative local format with optional GitHub Issue sync -- which is essentially what CCPM does, but CCPM makes GitHub the authority rather than the mirror.

---

## 3. Parallel Execution

### CCPM: Git Worktrees + Multi-Agent Processes

CCPM's parallelism operates at two levels:

**Level 1: Epic-level isolation**
- Each epic gets a dedicated worktree: `../epic-<name>/` on branch `epic/<name>`
- Worktree created during sync phase via `git worktree add ../epic-<name> -b epic/<name>`
- Clean separation -- different epics never share a working directory

**Level 2: Intra-issue stream decomposition**
- A single issue is analyzed for independent work streams (database, service, API, UI, tests)
- Each stream gets assigned files it may modify
- Multiple Claude Code agents are launched, each scoped to its stream
- Coordination rules:
  - Agents only touch assigned files
  - Commits are the sync mechanism (frequent, using `Issue #N: description` format)
  - Before editing a shared file, check if another agent modified it
  - Pull with rebase before beginning new file work
  - Conflicts are reported and paused, never auto-resolved
  - No `--force` flags allowed

**Analysis file** (`.claude/epics/<name>/<N>-analysis.md`) documents:
- Per-stream scope, files, start conditions, estimates
- Coordination points and shared files
- Conflict risk assessment
- Expected timeline with/without parallelization

**Strengths**:
- True process-level isolation -- agents cannot corrupt each other's state
- Git is the coordination protocol -- well-understood, robust
- Worktrees are a first-class git feature, not a hack
- Stream analysis produces an auditable plan before execution
- Conflict detection is explicit, not implicit

**Weaknesses**:
- Worktree management adds operational complexity (cleanup, branch management)
- Agent coordination is convention-based, not enforced programmatically
- "Check if another agent modified it" is a race condition in theory
- No automatic stream dependency resolution -- agents must self-report blockers
- Parallelism is limited by how cleanly work can be decomposed into non-overlapping file sets

### SuperClaude: Wave-Checkpoint-Wave (In-Process)

SuperClaude's parallel execution is a programmatic dependency-graph solver:

```
Wave 1: [Task A, Task B, Task C]  -- all independent, run concurrently
Checkpoint: Analyze results, check gates
Wave 2: [Task D, Task E]          -- depend on Wave 1 outputs
Checkpoint: Final validation
```

**Implementation** (`src/superclaude/execution/parallel.py`):
- `ParallelExecutor` with configurable `max_workers` (ThreadPoolExecutor)
- `Task.can_execute(completed_tasks)` checks dependency satisfaction
- Topological sort identifies parallel groups automatically
- Circular dependency detection with explicit error messages
- Speedup estimation (sequential vs parallel time)

**Sprint-level execution** (`src/superclaude/cli/sprint/executor.py`):
- Phases execute sequentially (Phase 1 -> Phase 2 -> ...)
- Within a phase, tasks execute with subprocess isolation (Claude Code instances)
- Trailing gates run on daemon threads in parallel with task execution
- Wiring gates analyze task outputs for structural correctness

**Strengths**:
- Fully programmatic -- no convention-based coordination
- Dependency resolution is deterministic (topological sort)
- Gate evaluation is non-blocking (trailing gates on daemon threads)
- KPI instrumentation provides quantitative feedback (latency, pass rates)
- No worktree management overhead

**Weaknesses**:
- ThreadPoolExecutor parallelism is within a single process -- no true isolation
- Tasks share the same filesystem (potential for file conflicts)
- No built-in mechanism for multi-agent coordination across processes
- Wave boundaries are static (determined at planning time, not adaptive)

### Verdict

These are complementary approaches solving different problems:

- **CCPM's worktree model** excels at **multi-agent, multi-process parallelism** where different agents work on different parts of a codebase simultaneously. This is genuinely novel and well-suited for large features with clearly separable components.

- **SuperClaude's wave model** excels at **pipeline orchestration** where tasks have formal dependencies and quality gates must be evaluated between stages. This is better for structured delivery workflows.

**Key learning**: CCPM's worktree-based parallel execution is the more ambitious and practically useful model for AI coding agents. SuperClaude's wave model is more suited to build/CI-style pipelines than to actual multi-agent coding.

---

## 4. Slash Command Design Philosophy

### CCPM: Natural Language Triggers (v2) / Slash Commands (v1)

CCPM has moved away from explicit slash commands (`/pm:prd-new`, `/pm:execute`) to **natural language intent detection**:

- "I want to build X" -> Plan phase
- "break down the epic" -> Structure phase
- "sync it to GitHub" -> Sync phase
- "start working on issue 42" -> Execute phase
- "what's our standup?" -> Track phase

The SKILL.md acts as a router: detect intent, load the appropriate reference file, execute. This is a **single-skill architecture** -- one SKILL.md entry point with 5 reference docs (plan, structure, sync, execute, track) plus a conventions doc.

**Design principles**:
- Natural language over memorized commands
- Script-first for deterministic operations (status, standup, validation)
- LLM reasoning only for creative tasks (PRD writing, stream analysis)

### SuperClaude: Explicit Slash Commands (38 total)

SuperClaude maintains an explicit command taxonomy:

- `/sc:sprint`, `/sc:roadmap`, `/sc:audit`, `/sc:pipeline` -- CLI pipeline commands
- `/sc:analyze`, `/sc:build`, `/sc:code`, `/sc:debug` -- task-oriented commands
- `/sc:research`, `/sc:review`, `/sc:test` -- investigation commands
- `/sc:help`, `/sc:doctor`, `/sc:index-repo` -- meta commands

Each command maps to a skill package with rules, templates, and reference docs.

**Design principles**:
- Explicit invocation over implicit detection
- Commands as protocol triggers (must invoke skill before generating output)
- Rich command taxonomy covering the full development lifecycle
- Each command activates a specific persona and MCP server set

### Verdict

CCPM's natural language approach is **more user-friendly** and has lower learning curve. SuperClaude's explicit commands provide **more precise control** and **reproducible behavior**. For a PM/delivery tool, CCPM's approach is arguably better -- you want to say "what's next?" not `/sc:sprint status --format=json`. For a developer framework, SuperClaude's explicit commands reduce ambiguity.

---

## 5. GitHub Integration Depth

### CCPM: Deep, First-Class Integration

| Capability | Implementation |
|-----------|---------------|
| Issue creation | `gh issue create` with structured labels |
| Sub-issues | `gh-sub-issue` extension for parent-child |
| Progress sync | `gh issue comment` with structured updates |
| Issue close | `gh issue close` on task completion |
| Label taxonomy | `epic`, `epic:<name>`, `feature`, `task`, `bug` |
| Worktree branches | `epic/<name>` branch per epic |
| Commit convention | `Issue #N: description` |
| Safety check | Blocks writes to template repo |
| Batch operations | Parallel agent creation for 5+ tasks |
| Bug follow-up | Linked bug issues with back-references |
| Epic merge | Branch merge + worktree cleanup + issue close |

CCPM treats GitHub as an integral part of the workflow, not an optional integration.

### SuperClaude: Minimal, Branch-Level Only

SuperClaude's GitHub integration is limited to:
- Feature branch creation (convention-based)
- Standard git commit/push workflow
- PR creation via `gh pr create` (manual, not automated)
- No issue tracking integration
- No label management
- No progress sync to issues

### Verdict

CCPM is dramatically ahead on GitHub integration. This is perhaps the single largest functional gap in SuperClaude for team-based delivery workflows. CCPM's approach of treating GitHub Issues as the coordination layer for multi-agent work is well-designed and practically useful.

---

## 6. Quality Gates and Verification

### CCPM: Convention-Based Preflight Checks

CCPM's quality gates are procedural checks embedded in reference docs:

**Before sync**:
- Epic file must exist
- Task files must exist (otherwise: "No tasks to sync. Decompose the epic first.")
- Remote safety check (not the template repo)

**Before execution**:
- Local task file must exist
- Analysis file must exist (or analysis must run first)
- Epic worktree must exist
- Working tree must be clean (`git status --porcelain`)
- Epic branch must exist

**During execution**:
- Agents stay within assigned file scope
- Frequent commits required
- No force flags
- Conflicts reported, not auto-resolved

**Validation script** (`validate.sh`):
- Frontmatter consistency
- Orphaned file detection
- Missing GitHub link detection
- Dependency integrity

**Characteristics**: Manual/convention-based, bash-script-driven, no programmatic enforcement within the agent runtime.

### SuperClaude: Programmatic, Multi-Layer Gate System

SuperClaude has a sophisticated, code-enforced quality gate architecture:

**Trailing Gates** (daemon-thread, non-blocking):
- `TrailingGateRunner`: submits gate evaluations on background threads
- `GateResultQueue`: thread-safe collection of results
- `DeferredRemediationLog`: persistent log of failures needing remediation
- `TrailingGatePolicy`: abstract protocol for remediation step construction
- Gate results include: `step_id`, `passed`, `evaluation_ms`, `failure_reason`

**Wiring Gates** (structural correctness):
- Post-task analysis of code structure
- Modes: `off`, `shadow` (log only), `soft` (warn on critical), `full` (block on critical+major)
- Budget-controlled: `wiring_analysis_turns`, `remediation_cost`
- Grace period support for gradual rollout

**Anti-Instinct Gates**:
- Rollout modes: `off`, `shadow`, `soft`, `full`
- Evaluates behavioral compliance patterns

**Confidence Gating** (pre-execution):
- >= 90%: proceed
- 70-89%: present alternatives
- < 70%: ask questions before implementing
- ROI: 25-250x token savings

**Gate Display States** (TUI):
- Full lifecycle visualization: NONE -> CHECKING -> PASS/FAIL_DEFERRED -> REMEDIATING -> REMEDIATED/HALT
- Valid state transitions enforced programmatically

**KPI Reporting**:
- Gate pass/fail rates
- Latency percentiles (p50, p95)
- Remediation frequency
- Wiring findings by type
- Net turn cost accounting

**Characteristics**: Code-enforced, instrumented, multi-modal (trailing, wiring, confidence, anti-instinct), with quantitative feedback loops.

### Verdict

SuperClaude's quality gate system is significantly more sophisticated. CCPM's gates are adequate for preventing obvious errors (missing files, dirty worktrees) but lack runtime enforcement, quantitative measurement, and automated remediation. SuperClaude's trailing gate architecture with deferred remediation and KPI reporting is a genuine engineering achievement.

---

## 7. Sprint Management Approach

### CCPM: Epic-Driven Delivery

CCPM's delivery unit is the **epic**:

1. **Plan**: PRD with guided brainstorming (problem, users, success metrics, constraints)
2. **Structure**: Epic decomposed into max 10 tasks with dependencies, effort estimates, and parallelism flags
3. **Sync**: Push to GitHub Issues, create worktree, establish mapping
4. **Execute**: Analyze streams, launch parallel agents, coordinate via Git
5. **Track**: Bash scripts for status, standup, blockers, next priority

Progress is calculated as `closed_tasks / total_tasks`. The cycle is: plan one feature, deliver it, merge it, archive it.

### SuperClaude: Phase-Based Sprint Pipeline

SuperClaude's delivery unit is the **sprint** (a collection of phases):

1. **Parse**: Extract tasks from markdown phase files via regex
2. **Plan**: Dependency analysis, execution mode selection (claude/python/skip)
3. **Execute**: Phase-by-phase execution with subprocess isolation
4. **Gate**: Trailing gates evaluate quality in parallel; wiring gates check structure
5. **Remediate**: Deferred remediation for gate failures
6. **Report**: KPI report with pass rates, latency, turn accounting

The sprint executor manages:
- Phase ordering and dependencies
- Turn budget allocation and reimbursement
- Output monitoring (error detection, prompt-too-long detection)
- Signal handling (graceful interruption)
- tmux integration for live tail output
- TUI with Rich for phase/task status visualization
- Diagnostic collection and failure classification

### Verdict

CCPM is more **product-management oriented** (PRD -> epic -> tasks -> issues). SuperClaude is more **engineering-execution oriented** (tasklist -> phases -> tasks -> gates -> KPIs). CCPM answers "what should we build?". SuperClaude answers "how do we ensure it's built correctly?". These are complementary concerns.

---

## 8. Simplicity vs Comprehensiveness

### CCPM: Elegant Simplicity

- **~20 files** total (SKILL.md, 6 reference docs, ~14 bash scripts)
- **Zero Python dependencies** -- pure shell + markdown + `gh` CLI
- **Single skill** -- one entry point, five phases
- **Harness-agnostic** -- works with Claude Code, Codex, Cursor, Factory, Amp
- **Install**: Copy a directory, point your harness at it
- **Learning curve**: Minutes (natural language triggers)

### SuperClaude: Engineered Comprehensiveness

- **100+ modules** across Python CLI, skills, commands, agents
- **Python package** with pip/pipx installation, entry points, pytest plugin
- **38 commands, 29 agents, 13 skills** -- extensive taxonomy
- **MCP server integration** (7 servers, persona-based routing)
- **Rich TUI**, tmux integration, diagnostic collection
- **Install**: `pipx install superclaude && superclaude install`
- **Learning curve**: Hours to days (command taxonomy, gate modes, personas)

### Verdict

CCPM wins on approachability. SuperClaude wins on capability density. CCPM could be adopted by any team in 10 minutes. SuperClaude requires investment but delivers more control over execution quality.

---

## 9. Identified Learnings for SuperClaude

### High-Priority Adoptions

1. **GitHub Issues as optional sync target**: SuperClaude's markdown tasklists should optionally sync to GitHub Issues for team visibility. CCPM's label taxonomy (`epic:<name>`, `task`, `feature`) and file-to-issue renaming pattern are well-designed. This does not mean replacing markdown as source of truth -- it means adding a sync layer.

2. **Git worktree-based parallel execution**: For multi-agent scenarios, SuperClaude should support worktree-based isolation. The current Wave model is good for pipeline orchestration but does not enable true multi-agent parallel coding. CCPM's pattern of `git worktree add ../epic-<name> -b epic/<name>` with scoped file assignments is the right model.

3. **Stream analysis before execution**: CCPM's analysis file pattern (documenting per-stream scope, files, dependencies, conflict risks, and expected timeline savings) is excellent for auditability and should be adopted. SuperClaude's dependency graph analysis is programmatic but not auditable in the same way.

4. **Script-first for deterministic operations**: CCPM's rule of "run bash scripts for status/standup/validation, use LLM only for creative work" is a strong design principle. SuperClaude's KPI reporting is programmatic, but operational queries (status, next, blocked) could benefit from fast bash scripts.

### Medium-Priority Adoptions

5. **Natural language triggers as alternative UX**: SuperClaude's explicit slash commands are precise but high-friction. Adding natural language intent detection as an alternative entry point (while keeping slash commands for power users) would improve accessibility.

6. **Commit convention enforcement**: CCPM's `Issue #N: description` commit format links code changes to work items. SuperClaude should adopt a similar convention when GitHub Issue sync is present.

7. **Epic-level progress tracking**: CCPM's `closed_tasks / total_tasks` progress model with automatic recalculation is simple and effective. SuperClaude's KPI system is more detailed but lacks a simple "how done are we?" metric.

### Lower-Priority Observations

8. **Harness agnosticism**: CCPM's design as a portable skill (works with Claude Code, Codex, Cursor, etc.) is forward-thinking. SuperClaude is deeply coupled to Claude Code. This may matter as the agent ecosystem diversifies.

9. **PRD-first workflow**: CCPM's structured PRD creation with guided brainstorming (problem, users, success metrics, constraints, out-of-scope) is a useful upstream addition that SuperClaude's roadmap pipeline could incorporate.

---

## 10. Comparative Risk Assessment

| Risk | CCPM | SuperClaude |
|------|------|-------------|
| Agent misbehavior | Convention-based only -- agent must self-enforce file scope | Programmatic gates with automated remediation |
| GitHub outage | Blocks sync/execute phases entirely | No impact (offline-first) |
| Scale (large projects) | Linear issue creation; potential API rate limits | Bounded by turn budget and phase structure |
| Debugging failures | Bash script output + GitHub issue comments | Diagnostic collector, failure classifier, debug logger |
| Context window pressure | Minimal (single skill, ~50 tokens) | Higher (framework context, multiple skills) |
| Maintenance burden | Low (~20 files, no dependencies) | High (Python package, test suite, CI) |

---

## 11. Conclusion

CCPM and SuperClaude are not competitors -- they solve adjacent problems with different design centers:

- **CCPM** is a **project management skill** that excels at turning ideas into tracked, parallelized work items using GitHub as the coordination layer. Its greatest strengths are GitHub-native integration, worktree-based isolation, and operational simplicity.

- **SuperClaude** is an **execution framework** that excels at ensuring work is done correctly through programmatic quality gates, KPI instrumentation, and structured pipelines. Its greatest strengths are trailing gate architecture, confidence-based gating, and quantitative feedback loops.

The most impactful integration opportunity is adopting CCPM's GitHub Issues sync and worktree-based parallel execution as optional capabilities within SuperClaude's sprint pipeline, creating a system that both coordinates multi-agent work effectively (CCPM's strength) and verifies execution quality programmatically (SuperClaude's strength).

---

## Sources

- CCPM Repository: https://github.com/automazeio/ccpm
- CCPM SKILL.md, execute.md, sync.md, conventions.md, track.md (raw GitHub content)
- SuperClaude source: `src/superclaude/cli/sprint/executor.py`, `models.py`, `kpi.py`
- SuperClaude source: `src/superclaude/cli/pipeline/trailing_gate.py`
- SuperClaude source: `src/superclaude/execution/parallel.py`
