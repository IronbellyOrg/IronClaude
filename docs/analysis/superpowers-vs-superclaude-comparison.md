# Deep Comparative Analysis: Superpowers vs SuperClaude

**Date**: 2026-03-23
**Scope**: Skill system architecture, development methodology, execution models, cross-platform strategy
**Sources**: Superpowers repo (obra/superpowers, 106K stars, v5.0.5), SuperClaude repo (local, v4.2.0)

---

## 1. Executive Summary

Superpowers and SuperClaude represent two fundamentally different philosophies for augmenting AI coding agents. Superpowers is a **lightweight, cross-platform methodology layer** that enforces software engineering discipline through composable Markdown skills and auto-triggering behavior. SuperClaude is a **deep, vertically-integrated execution platform** with Python-backed CLI pipelines, programmatic confidence scoring, compliance tiering, and real-time sprint orchestration. They overlap in intent (make agents produce better code) but diverge sharply in mechanism, scope, and target audience.

| Dimension | Superpowers | SuperClaude |
|-----------|-------------|-------------|
| Core metaphor | "Discipline for agents" | "Execution platform for agents" |
| Stars / adoption | 106K GitHub stars | Internal / early-stage |
| Skill count | 14 composable skills | 13 protocol skills + 40 commands |
| Platform support | 5+ (Claude Code, Cursor, Codex, OpenCode, Gemini CLI) | Claude Code only |
| Language | Shell/Markdown (57.8% Shell, 30.1% JS) | Python + Markdown |
| Installation | Plugin marketplace / 2 commands | `pipx install` + `superclaude install` |
| Enforcement model | Behavioral (Markdown instructions) | Programmatic (Python gates + sub-agents) |
| TDD approach | Absolute mandate, delete-and-restart | Compliance-tiered, optional per tier |
| Context management | Fresh subagent per task (isolation) | Wave-Checkpoint-Wave (parallelism) |

---

## 2. Skill System Design

### 2.1 Superpowers: Auto-Trigger + Composability

**Architecture**: Each skill is a single `SKILL.md` file (plus optional supporting refs). Skills are pure Markdown with YAML frontmatter. The `using-superpowers` meta-skill bootstraps at session start and forces the agent to check skill applicability before every action.

**Auto-triggering mechanism**:
- The bootstrap skill (`using-superpowers`) runs at conversation start
- Before any action, the agent must ask: "Could any skill apply here?"
- Threshold is extremely low: even 1% relevance triggers skill loading
- Process skills (brainstorming, planning) take priority over implementation skills
- Skills announce themselves: "I'm using the X skill to..."

**Composability model**: Skills chain in a fixed pipeline:
```
brainstorming --> writing-plans --> [subagent-driven-development | executing-plans]
                                          |
                                   test-driven-development (per task)
                                          |
                                   requesting-code-review --> finishing-a-development-branch
```

**Strengths**:
- Zero-code installation; pure Markdown is universally portable
- Auto-triggering removes the burden of remembering commands
- Fixed pipeline prevents agents from skipping steps
- Each skill is self-contained and readable

**Weaknesses**:
- No programmatic enforcement; relies entirely on the LLM following instructions
- No telemetry, metrics, or machine-readable gates
- Pipeline is rigid; no compliance tiering for trivial tasks
- Cannot verify that skills were actually followed (honor system)

### 2.2 SuperClaude: Explicit Invocation + Deep Protocols

**Architecture**: Skills are directories containing `SKILL.md` plus supporting subdirectories (`refs/`, `rules/`, `templates/`, `scripts/`, `evals/`). Skills are backed by Python CLI modules that provide programmatic execution.

**Invocation model**:
- Explicit command invocation: `/sc:task`, `/sc:roadmap`, `/sc:brainstorm`
- Commands classify intent and invoke the appropriate skill protocol
- The `sc-task-unified-protocol` auto-classifies tasks into compliance tiers (STRICT/STANDARD/LIGHT/EXEMPT)
- Keywords and path patterns drive classification with confidence scoring

**Composability model**: Skills are independent protocols, not a fixed pipeline. The unified task command routes to the appropriate depth:
```
/sc:task "description"
    |
    v
[Classification: STRICT | STANDARD | LIGHT | EXEMPT]
    |
    v
[Execution depth varies by tier]
    |
    v
[Verification: sub-agent | direct test | skip]
```

**Strengths**:
- Programmatic enforcement via Python gates, not just LLM compliance
- Compliance tiering prevents over-engineering trivial changes
- Machine-readable telemetry (classification headers, KPI tracking)
- Test Failure Escalation Protocol (TFEP) with formal halt-and-freeze semantics
- Sprint executor with TUI, tmux integration, real-time monitoring

**Weaknesses**:
- Explicit invocation means users must remember commands
- Higher installation complexity (`pipx install` + `superclaude install`)
- Markdown+Python dual nature increases maintenance burden
- Single-platform (Claude Code only)

---

## 3. Development Methodology Enforcement

### 3.1 Superpowers: TDD as Absolute Mandate

Superpowers enforces strict RED-GREEN-REFACTOR on every task:

1. **No exceptions by default**: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"
2. **Delete-and-restart policy**: If code was written before the test, delete it entirely
3. **No peeking**: Cannot use previously-written code as reference for tests
4. **Verification at every step**: Must watch each test fail, confirm the failure reason
5. **Completion checklist**: Every function must have a test that was seen failing first

**Exceptions** require explicit human approval:
- Throwaway prototypes
- Generated code
- Configuration files

**Red flags** that trigger a full stop and restart:
- Code before test
- Tests written after implementation
- Test passes immediately
- "Just this once" reasoning
- Claiming the case is special

### 3.2 SuperClaude: Compliance-Tiered Verification

SuperClaude takes a graduated approach:

| Tier | TDD Required | Verification | Token Cost |
|------|-------------|-------------|------------|
| STRICT | Yes (sub-agent QA) | Full adversarial validation | 3-5K |
| STANDARD | Affected tests run | Direct test execution | 300-500 |
| LIGHT | No | Quick sanity check | ~0 |
| EXEMPT | No | None | 0 |

**Key differentiator**: The Test Failure Escalation Protocol (TFEP) provides formal semantics for what happens when tests fail:
- Pre-existing test failures trigger mandatory escalation
- 3+ simultaneous new test failures trigger escalation
- Ad-hoc fixes without TFEP workflow are PROHIBITED
- Test baseline snapshots track pre-existing vs new tests

**SuperClaude also provides**:
- `ConfidenceChecker`: Pre-implementation assessment (>=90% proceed, 70-89% present options, <70% stop)
- `SelfCheckProtocol`: Post-implementation evidence-based validation
- `ReflexionPattern`: Cross-session error learning and prevention

### 3.3 Comparison

| Aspect | Superpowers | SuperClaude |
|--------|-------------|-------------|
| TDD enforcement | Absolute, no exceptions | Tiered by task criticality |
| Failure handling | Delete and restart | TFEP with formal escalation |
| Pre-implementation check | Brainstorming phase | ConfidenceChecker (scored) |
| Post-implementation check | Two-stage code review | SelfCheckProtocol + adversarial QA |
| Error learning | None (per-session only) | ReflexionPattern (cross-session) |
| Trivial task overhead | Same as complex task | Near-zero (LIGHT/EXEMPT tiers) |

**Verdict**: Superpowers is more disciplined but less pragmatic. Mandating TDD for a typo fix or docstring edit is wasteful. SuperClaude's tiering is more realistic for production use, but the TDD-always approach produces stronger guarantees when followed.

---

## 4. Cross-Platform Strategy

### 4.1 Superpowers: 5+ Platforms

| Platform | Installation | Mechanism |
|----------|-------------|-----------|
| Claude Code | Plugin marketplace (2 commands) | Native plugin system |
| Cursor | Plugin marketplace | `/add-plugin superpowers` |
| Codex | Manual fetch | Agent reads install instructions from URL |
| OpenCode | Manual fetch | Same pattern as Codex |
| Gemini CLI | Extension system | `gemini extensions install` |

**Adaptation strategy**:
- Core skills are Markdown, universally portable
- Platform-specific directories (`.claude-plugin/`, `.codex/`, `.cursor-plugin/`, `.opencode/`)
- Tool substitution system maps platform-specific equivalents (e.g., `TodoWrite` vs `update_plan` for Codex)
- Simplified subagent handling for platforms without native delegation
- `GEMINI.md` and `gemini-extension.json` for Gemini-specific config

**Key insight**: Because skills are pure Markdown behavioral instructions, they work on any platform that can read files and follow instructions. The "code" is the English-language protocol, not executable logic.

### 4.2 SuperClaude: Claude Code Deep Integration

SuperClaude is exclusively built for Claude Code:
- Skills reference Claude Code-specific tools (`Task`, `Skill`, `TodoWrite`)
- CLI pipeline requires `claude` binary for sprint execution
- MCP server integration (Serena, Auggie, Tavily, Context7) assumes Claude Code environment
- TUI/tmux integration for sprint monitoring
- Plugin system targets `~/.claude/` directory structure

**Why single-platform**:
- Deep Python integration (pytest plugin, CLI tools) requires a specific runtime
- Compliance gates and sprint execution are programmatic, not behavioral
- MCP server orchestration is Claude Code-native
- Trade-off: depth over breadth

### 4.3 Comparison

| Aspect | Superpowers | SuperClaude |
|--------|-------------|-------------|
| Platforms | 5+ | 1 (Claude Code) |
| Portability mechanism | Markdown is universal | Python requires runtime |
| Depth of integration | Behavioral only | Programmatic + behavioral |
| Installation friction | 2 commands (marketplace) | `pipx install` + `superclaude install` |
| Update mechanism | `/plugin update` (auto) | Manual / pip upgrade |

**Verdict**: Superpowers' cross-platform strategy is its strongest competitive advantage. The marketplace model drives adoption (106K stars). SuperClaude's depth is its advantage, but at the cost of platform lock-in.

---

## 5. Context Management

### 5.1 Superpowers: Subagent Isolation

**Model**: Fresh subagent per task, no inherited session history.

```
Controller (holds plan)
    |
    +--> Implementer Subagent (Task 1) --> Spec Reviewer --> Quality Reviewer
    |
    +--> Implementer Subagent (Task 2) --> Spec Reviewer --> Quality Reviewer
    |
    +--> Final Reviewer (whole implementation)
```

**Isolation rules**:
- Each subagent starts with zero context except what the controller provides
- Controller passes only task text and necessary context
- Subagents do not read the plan file directly
- Git worktrees provide filesystem-level isolation per branch
- Prevents context drift that causes quality degradation in long sessions

**Parallel dispatch** (separate skill):
- One agent per independent problem domain
- No shared state between parallel agents
- Post-completion merge with conflict checking

### 5.2 SuperClaude: Wave-Checkpoint-Wave Parallelism

**Model**: Dependency-graph-based parallel execution within a single session.

```
[Wave 1: Read files in parallel]
    --> Checkpoint: Analyze dependencies
[Wave 2: Edit files in parallel]
    --> Checkpoint: Run tests
[Wave 3: Fix issues in parallel]
```

**Key components**:
- `ParallelGroup`: Tasks with no inter-dependencies execute concurrently
- `Task.can_execute()`: Checks dependency satisfaction before launch
- `ThreadPoolExecutor`: Concurrent execution within the Python runtime
- Sprint executor: Orchestrates multi-task execution with TUI monitoring

**Sprint execution model**:
- `SprintConfig` defines task list and execution parameters
- `TurnLedger` tracks per-turn metrics and gate outcomes
- `TrailingGatePolicy` enforces quality gates with deferred remediation
- Real-time monitoring via `OutputMonitor` with error detection

### 5.3 Comparison

| Aspect | Superpowers | SuperClaude |
|--------|-------------|-------------|
| Isolation unit | Per-task subagent | Per-wave parallel group |
| Context drift prevention | Fresh context per task | Dependency checkpoints |
| Memory between tasks | Controller-mediated only | TurnLedger + ReflexionPattern |
| Parallel strategy | Multi-agent (separate processes) | Multi-thread (same process) |
| Overhead | High (new agent per task) | Lower (wave batching) |
| Autonomy duration | Hours (subagent keeps focus) | Sprint-bounded (TUI-monitored) |

**Verdict**: Superpowers' subagent isolation is elegant for preventing context drift in long sessions. SuperClaude's wave model is more efficient for throughput. They solve different problems: Superpowers optimizes for focus, SuperClaude optimizes for speed.

---

## 6. Quality Assurance Approaches

### 6.1 Superpowers

| Stage | Mechanism | Enforced By |
|-------|-----------|-------------|
| Pre-design | Socratic brainstorming | brainstorming skill |
| Pre-implementation | Plan review (subagent) | writing-plans skill |
| Per-task | Strict TDD (red-green-refactor) | test-driven-development skill |
| Post-task | Two-stage review (spec + quality) | subagent-driven-development |
| Post-all | Final review subagent | subagent-driven-development |
| Debugging | Systematic root cause analysis | systematic-debugging skill |
| Completion | Verification-before-completion | verification-before-completion skill |

### 6.2 SuperClaude

| Stage | Mechanism | Enforced By |
|-------|-----------|-------------|
| Pre-implementation | ConfidenceChecker (scored) | pm_agent/confidence.py |
| Classification | Compliance tier detection | sc-task-unified-protocol |
| Per-task | Tier-appropriate testing | Sprint executor |
| Failure handling | TFEP (halt-freeze-escalate) | sc-task-unified-protocol |
| Post-implementation | SelfCheckProtocol | pm_agent/self_check.py |
| Adversarial validation | sc-adversarial-protocol | Dedicated skill |
| Cross-session | ReflexionPattern | pm_agent/reflexion.py |
| Sprint-level | TrailingGatePolicy | pipeline/trailing_gate.py |
| Forensic | sc-forensic-qa-protocol | Dedicated skill |

### 6.3 Assessment

Superpowers has a **linear, always-on** QA model: every task gets the same treatment regardless of complexity. SuperClaude has a **graduated, context-sensitive** QA model: trivial changes get minimal overhead while critical changes get maximum scrutiny.

Superpowers' advantage: simplicity and consistency. No task can slip through without review.
SuperClaude's advantage: pragmatism and efficiency. Token spend scales with risk.

---

## 7. Skill Complexity Comparison

### 7.1 Superpowers Skill Anatomy

```
skills/
  brainstorming/
    SKILL.md              # ~200 lines, pure behavioral instructions
  test-driven-development/
    SKILL.md              # ~400 lines, detailed workflow + anti-patterns
    refs/
      testing-anti-patterns.md
```

- Average skill: 1-2 files
- Purely declarative (Markdown)
- No executable code
- Enforced by LLM compliance
- Tokens per skill: ~30-50 at load, full content on invocation

### 7.2 SuperClaude Skill Anatomy

```
skills/
  sc-task-unified-protocol/
    SKILL.md              # ~200 lines, protocol definition
    __init__.py           # Python module integration
  sc-cleanup-audit-protocol/
    SKILL.md
    __init__.py
    rules/                # Enforcement rules
    scripts/              # Executable scripts
    templates/            # Output templates
  sc-release-split-protocol/
    SKILL.md
    __init__.py
    refs/                 # Reference material
    evals/                # Evaluation tests
```

- Average skill: 2-6 files across multiple subdirectories
- Mixed declarative (Markdown) + imperative (Python)
- Backed by CLI modules (`cli/sprint/`, `cli/roadmap/`, etc.)
- Enforced by both LLM compliance AND programmatic gates
- Additional backing: pytest fixtures, MCP server integration

### 7.3 Assessment

| Metric | Superpowers | SuperClaude |
|--------|-------------|-------------|
| Files per skill | 1-2 | 2-6 |
| Lines per skill | 200-400 | 200+ (SKILL.md) + Python modules |
| Executable code | None | Python CLI, pytest, gates |
| Maintenance burden | Low | High |
| Customization ease | Fork and edit Markdown | Edit Python + Markdown + sync |
| Community contribution | Very easy (just write .md) | Harder (must understand Python architecture) |

---

## 8. Community Adoption Model

### 8.1 Superpowers

- **Distribution**: Plugin marketplace (Claude Code, Cursor) + manual install (Codex, OpenCode, Gemini)
- **Update model**: `/plugin update superpowers` (automatic)
- **Contributing**: Fork repo, create branch, write SKILL.md, submit PR
- **Barrier to entry**: Near-zero (just write Markdown)
- **Growth vector**: 106K stars, 8.5K forks, 27 contributors, 70 open issues, 95 open PRs
- **Ecosystem**: Claude Plugin Marketplace presence drives discovery
- **Sponsorship**: Open source with optional GitHub Sponsors

### 8.2 SuperClaude

- **Distribution**: PyPI (`pipx install superclaude`) + `superclaude install`
- **Update model**: Manual (`pip upgrade`)
- **Contributing**: Must understand Python package structure, pytest, CLI framework
- **Barrier to entry**: Moderate (Python + architecture knowledge required)
- **Growth vector**: Internal/early-stage
- **Ecosystem**: No marketplace presence yet

### 8.3 Key Learnings for SuperClaude

1. **Marketplace presence is a growth multiplier**: Superpowers' 106K stars are largely driven by marketplace discoverability. A `/plugin install` command is dramatically lower friction than `pipx install`.

2. **Markdown-only skills invite contributions**: Superpowers' "writing-skills" meta-skill teaches users how to create new skills. The barrier is zero because skills are just Markdown files with a pattern.

3. **Cross-platform unlocks network effects**: Each new platform Superpowers supports brings that platform's entire user base as potential adopters. Platform lock-in caps growth.

4. **Auto-update via marketplace builds retention**: Users never need to think about version management. SuperClaude requires manual updates.

---

## 9. Identified Learnings and Recommendations

### 9.1 What SuperClaude Should Learn from Superpowers

| Learning | Detail | Difficulty |
|----------|--------|------------|
| **Auto-triggering** | Implement a bootstrap skill that checks applicability before every action, rather than requiring explicit `/sc:` invocation | Medium |
| **Cross-platform skill layer** | Extract a Markdown-only skill subset that works on Cursor, Codex, Gemini CLI without Python dependencies | High |
| **Marketplace distribution** | Package core skills for Claude Plugin Marketplace for discoverability | Medium |
| **Contribution simplicity** | Create a "writing-skills" meta-skill and lower the barrier for community skill authoring | Low |
| **Subagent isolation pattern** | Adopt fresh-context-per-task for long sprints to prevent context drift | Medium |
| **Delete-and-restart TDD culture** | Consider adopting the "delete code written before tests" rule for STRICT tier | Low |

### 9.2 What Superpowers Could Learn from SuperClaude

| Learning | Detail |
|----------|--------|
| **Compliance tiering** | Not every task needs full TDD + brainstorming + review. A LIGHT/EXEMPT tier prevents ceremony fatigue |
| **Programmatic gates** | Markdown-only enforcement is honor-system. Python gates provide verifiable compliance |
| **Confidence scoring** | Pre-implementation confidence check with scored thresholds prevents wrong-direction work |
| **Test failure escalation** | TFEP provides formal semantics for test failures instead of just "delete and restart" |
| **Cross-session learning** | ReflexionPattern enables error prevention across sessions; Superpowers has no memory system |
| **Sprint orchestration** | TUI + tmux + KPI tracking enables monitored multi-hour autonomous execution |
| **Telemetry** | Machine-readable classification headers enable A/B testing and pipeline analytics |

### 9.3 Synthesis: Hybrid Opportunities

The most powerful system would combine:

1. **Superpowers' auto-triggering** with **SuperClaude's compliance tiering** -- skills activate automatically but scale their ceremony to task complexity
2. **Superpowers' Markdown portability** with **SuperClaude's Python enforcement** -- a two-layer architecture where Markdown skills work everywhere and Python gates add depth on Claude Code
3. **Superpowers' subagent isolation** with **SuperClaude's wave parallelism** -- isolation for focus on complex tasks, waves for throughput on independent tasks
4. **Superpowers' marketplace model** with **SuperClaude's programmatic quality** -- marketplace distribution for growth, programmatic gates for reliability

---

## 10. Risk Assessment

### 10.1 Superpowers Risks
- **LLM compliance fragility**: Skills only work if the LLM follows instructions. Model updates or different models may degrade compliance
- **Rigidity for experienced users**: No way to opt out of TDD for known-good patterns without human override
- **No telemetry**: Cannot measure whether skills are actually followed or how often they prevent errors
- **Platform dependency**: Relies on platform plugin systems that can change without notice

### 10.2 SuperClaude Risks
- **Platform lock-in**: Claude Code only limits total addressable market
- **Complexity barrier**: Python + Markdown + CLI + MCP integration is harder to maintain and contribute to
- **Over-engineering potential**: 4 compliance tiers + TFEP + adversarial protocol + forensic QA may be more ceremony than most tasks need
- **Adoption ceiling**: Without marketplace presence, growth depends on manual discovery

---

## 11. Conclusion

Superpowers and SuperClaude represent two valid but different bets:

**Superpowers bets on breadth**: Lightweight, portable, universally applicable. Its 106K stars prove that a simple, cross-platform methodology layer meets massive demand. Its weakness is that enforcement is behavioral only -- the LLM may or may not follow instructions.

**SuperClaude bets on depth**: Programmatic gates, compliance tiering, sprint orchestration, cross-session learning. Its strength is verifiable quality enforcement. Its weakness is platform lock-in and adoption friction.

The market signal from Superpowers is clear: **developers want structured methodology for AI agents, and they want it to work everywhere with zero friction**. The engineering signal from SuperClaude is also clear: **behavioral enforcement alone is insufficient for production reliability**.

The strategic opportunity is a two-layer architecture: a Markdown-portable skill layer for cross-platform reach (learn from Superpowers), backed by a Python enforcement layer for depth where available (SuperClaude's existing strength).
