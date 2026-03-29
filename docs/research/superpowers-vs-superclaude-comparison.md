# Deep Comparative Analysis: Superpowers vs SuperClaude (Developer Support)

**Date**: 2026-03-23
**Methodology**: Web research (Tavily, GitHub, community sources) + internal codebase analysis

---

## Executive Summary

**Superpowers** (obra/superpowers, ~104K stars) and **SuperClaude** take fundamentally different approaches to augmenting AI coding agents. Superpowers is a **workflow methodology framework** -- it enforces a linear development lifecycle (brainstorm -> plan -> TDD -> review -> merge) across multiple agent platforms. SuperClaude is a **specialized command toolkit** -- it provides 40+ discrete commands, 29 named agents, 12 skills, and a Python pytest plugin for targeted developer operations. They overlap on code review, testing enforcement, and debugging, but diverge sharply on audit depth, agent specialization, MCP integration, and repository intelligence.

**Key finding**: Superpowers excels at enforcing a disciplined end-to-end development workflow on greenfield projects. SuperClaude excels at targeted analysis, evidence-gated auditing, and deep integration with Python testing infrastructure on existing codebases.

---

## 1. Feature-by-Feature Comparison

### 1.1 Developer Support Commands

| Capability | Superpowers | SuperClaude |
|---|---|---|
| **Total skills/commands** | ~14 skills | 40+ slash commands, 12 skill protocols |
| **Code analysis** | None (no dedicated analysis skill) | `/sc:analyze` -- 4-domain analysis (quality, security, performance, architecture) with severity ratings |
| **Implementation** | `executing-plans`, `subagent-driven-development` | `/sc:implement` -- persona-activated (9 personas), `/sc:build` |
| **Testing** | `test-driven-development` (RED-GREEN-REFACTOR enforcement) | `/sc:test` -- framework auto-detection, coverage analysis, Playwright e2e, watch mode |
| **Debugging** | `systematic-debugging` (4-phase root cause), `verification-before-completion` | `/sc:troubleshoot` -- 4-type diagnosis (bug, build, performance, deployment), `--fix` gating |
| **Code review** | `requesting-code-review`, `receiving-code-review` (2-stage: spec compliance + code quality) | `/sc:cleanup-audit` -- 3-pass evidence-gated audit (42-module scope) |
| **Documentation** | Design documents saved from brainstorming; no dedicated doc skill | `/sc:document` -- dedicated documentation generation |
| **Repository indexing** | None | `/sc:index-repo` -- 94% token reduction (58K -> 3K tokens), dual output (MD + JSON) |
| **Planning** | `brainstorming` (Socratic), `writing-plans` (2-5 min tasks) | `/sc:brainstorm`, `/sc:design`, `/sc:spec-panel`, `/sc:estimate` |
| **Git workflow** | `using-git-worktrees`, `finishing-a-development-branch` | `/sc:git` -- git operations command |
| **Recommendation engine** | None | `/sc:recommend` -- multi-language command recommender with estimation |
| **Adversarial testing** | None | `/sc:adversarial` -- adversarial protocol testing |
| **Research** | None | `/sc:research` -- deep research with web search integration |
| **Explanation** | None | `/sc:explain` -- code explanation engine |
| **Reflection/learning** | None (no cross-session learning) | `/sc:reflect` -- reflexion pattern with cross-session memory |
| **Release management** | None | `/sc:release-split`, `/sc:roadmap`, `/sc:tasklist`, `/sc:sprint` |

**Verdict**: SuperClaude provides roughly 3x the command surface area with significantly more specialized capabilities. Superpowers intentionally constrains its scope to the core build lifecycle.

---

### 1.2 Audit Capabilities

| Dimension | Superpowers | SuperClaude |
|---|---|---|
| **Dedicated audit system** | No | Yes -- 3-pass escalating audit |
| **Pass 1** | N/A | Surface scan (Haiku agents): DELETE/REVIEW/KEEP classification |
| **Pass 2** | N/A | Structural audit (Sonnet agents): mandatory 8-field per-file profiles |
| **Pass 3** | N/A | Cross-cutting comparison: duplication matrices with overlap percentages |
| **Evidence gating** | Code review checks against plan | Every classification requires grep proof of zero references |
| **Batch processing** | N/A | Configurable batch sizes (50/25/30 per pass) |
| **Checkpoint/resume** | N/A | `progress.json` for session interruption recovery |
| **Quality validation** | N/A | 10% spot-check sampling |
| **Output** | N/A | Structured reports to `.claude-audit/` directory |
| **Safety** | N/A | READ-ONLY -- no file modifications during audit |

**Verdict**: SuperClaude's audit system is a unique capability with no equivalent in Superpowers. The 3-pass evidence-gated approach with grep-proof requirements and duplication matrices represents a significantly more rigorous approach to codebase analysis than Superpowers' plan-compliance code review.

---

### 1.3 Agent Specialization

| Dimension | Superpowers | SuperClaude |
|---|---|---|
| **Agent model** | Generic subagents (fresh per task) | 29 named specialized agents |
| **Agent identity** | Unnamed, disposable | Named roles: `security-engineer`, `performance-engineer`, `root-cause-analyst`, etc. |
| **Specialization** | Context injected via task prompt | Domain-specific behavioral definitions per agent |
| **Audit agents** | None | 5 dedicated: `audit-scanner`, `audit-analyzer`, `audit-comparator`, `audit-consolidator`, `audit-validator` |
| **Architecture agents** | None | `system-architect`, `backend-architect`, `frontend-architect`, `devops-architect` |
| **Quality agents** | Generic reviewer | `quality-engineer`, `python-expert`, `refactoring-expert` |
| **Research agents** | None | `deep-research-agent`, `deep-research` |
| **Teaching agents** | None | `socratic-mentor`, `learning-guide` |
| **PM agents** | None | `pm-agent`, `requirements-analyst` |
| **Review agents** | Spec reviewer + code quality reviewer (prompt templates) | `self-review`, `debate-orchestrator`, `business-panel-experts` |
| **Parallel dispatch** | `dispatching-parallel-agents` | Wave -> Checkpoint -> Wave pattern (3.5x speedup) |

**Verdict**: SuperClaude's 29 named agents with domain-specific behavioral definitions provide significantly deeper specialization than Superpowers' generic subagent model. Superpowers compensates with purpose-built prompt templates for its reviewers (spec-reviewer, code-quality-reviewer), but these are limited to the review phase.

---

### 1.4 MCP Server Integration

| Dimension | Superpowers | SuperClaude |
|---|---|---|
| **MCP integration** | None built-in | 10 MCP server integrations |
| **Web search** | Not integrated | Tavily MCP -- deep research capability |
| **Documentation lookup** | Not integrated | Context7 MCP -- official library docs (prevents hallucination) |
| **Reasoning** | Not integrated | Sequential Thinking MCP -- 30-50% token reduction on complex reasoning |
| **Symbol navigation** | Not integrated | Serena MCP -- project memory, symbol navigation |
| **Browser automation** | Not integrated | Playwright MCP -- e2e testing, browser automation |
| **UI generation** | Not integrated | Magic MCP -- UI component generation |
| **Codebase search** | Not integrated | Auggie MCP -- codebase retrieval (recommended before significant edits) |
| **Gateway option** | N/A | AIRIS Gateway -- 60+ tools, 98% token reduction, single SSE endpoint |
| **Per-command MCP routing** | N/A | Commands declare required MCP servers in frontmatter metadata |

**Verdict**: This is SuperClaude's most significant structural advantage. MCP integration allows commands to access live documentation, web search, browser automation, and persistent memory. Superpowers operates as a pure prompt/skill framework with no external tool integration beyond what the host agent provides natively.

---

### 1.5 Testing Integration

| Dimension | Superpowers | SuperClaude |
|---|---|---|
| **Testing philosophy** | Mandatory RED-GREEN-REFACTOR TDD | Framework-agnostic test execution with coverage analysis |
| **TDD enforcement** | Strict: deletes code written before tests | Not enforced at framework level |
| **Pytest plugin** | None | Auto-loaded via `pyproject.toml` entry point |
| **Custom fixtures** | None | `confidence_checker`, `self_check_protocol`, `reflexion_pattern`, `token_budget`, `pm_context` |
| **Auto-markers** | None | Tests in `/unit/` -> `@pytest.mark.unit`, `/integration/` -> `@pytest.mark.integration` |
| **Custom markers** | None | `@pytest.mark.confidence_check`, `@pytest.mark.self_check`, `@pytest.mark.reflexion`, `@pytest.mark.complexity()` |
| **Token budgeting** | None | Complexity-based: simple=200, medium=1000, complex=2500 tokens |
| **Pre-execution checks** | None | ConfidenceChecker: 90% proceed, 70-89% options, <70% stop |
| **Post-execution validation** | `verification-before-completion` | SelfCheckProtocol: evidence-based validation |
| **Error learning** | None | ReflexionPattern: cross-session error prevention |
| **Anti-pattern detection** | Testing anti-patterns reference doc | Built into pytest markers and PM agent |
| **E2E testing** | Not integrated | Playwright MCP integration for browser testing |

**Verdict**: Different strengths. Superpowers enforces TDD discipline at the workflow level (an agent literally cannot skip writing tests first). SuperClaude provides deeper pytest infrastructure with fixtures, markers, confidence checking, and cross-session learning -- but does not enforce test-first as a hard constraint.

---

### 1.6 Code Quality Enforcement

| Dimension | Superpowers | SuperClaude |
|---|---|---|
| **Enforcement model** | Workflow-level: mandatory skill activation prevents skipping steps | Command-level: user invokes specific quality commands |
| **TDD** | Mandatory -- deletes code written before tests | Available via `/sc:test` but not mandatory |
| **Code review** | Mandatory between tasks; critical issues block progress | On-demand via `/sc:cleanup-audit` or `/sc:analyze` |
| **Design review** | Mandatory via brainstorming skill | Available via `/sc:design`, `/sc:brainstorm` |
| **Confidence gating** | None | Pre-execution confidence check (100-200 token investment, 25-250x ROI) |
| **Evidence requirements** | Plan compliance checking | Grep-proof evidence for every audit classification |
| **Quality personas** | None | 9 activatable personas (architect, frontend, backend, security, qa, etc.) |

**Verdict**: Superpowers enforces quality through mandatory workflow gates -- the agent cannot proceed without completing each step. SuperClaude provides deeper analytical tools but relies on user invocation. Both approaches have merit: Superpowers prevents process shortcuts; SuperClaude enables targeted deep analysis.

---

### 1.7 Repository Indexing

| Dimension | Superpowers | SuperClaude |
|---|---|---|
| **Indexing capability** | None | `/sc:index-repo` with 94% token reduction |
| **Output formats** | N/A | `PROJECT_INDEX.md` (3KB) + `PROJECT_INDEX.json` (10KB) |
| **Token savings** | N/A | 550K tokens over 10 sessions, 5.5M over 100 sessions |
| **Metadata extraction** | N/A | Entry points, modules, exports, dependencies, test coverage |
| **Update modes** | N/A | Full, update, quick (skip tests) |

**Verdict**: Entirely unique to SuperClaude. No equivalent exists in Superpowers.

---

## 2. Pros and Cons

### 2.1 Superpowers

**Pros:**
- Enforced workflow discipline -- agents cannot skip steps (brainstorm -> plan -> TDD -> review -> merge)
- Strict TDD: RED-GREEN-REFACTOR is mandatory, code written before tests is deleted
- Multi-platform support: Claude Code, Cursor, Codex, OpenCode, Gemini CLI
- Git worktree management provides true branch isolation for parallel agent work
- Subagent isolation prevents context drift on long-running tasks
- 2-stage code review (spec compliance + code quality) catches both functional and stylistic issues
- Low barrier to entry: single plugin install command
- Massive community (104K stars, 8.4K forks) ensures rapid iteration and community skills
- Composable: community can add new skills following `writing-skills` guide
- Philosophy-driven: "systematic over ad-hoc" creates consistent outputs

**Cons:**
- No dedicated code analysis or security scanning capability
- No audit system -- code review is limited to plan-compliance checking
- Generic subagents with no persistent specialization
- No MCP server integration -- cannot access live docs, web search, or external tools
- No repository indexing -- every session re-reads the full codebase
- No pytest or test framework integration beyond TDD enforcement
- No cross-session learning or reflexion patterns
- No command recommendation engine
- No documentation generation skill
- No token budgeting or efficiency optimization
- No confidence-gated execution (no pre-execution assessment)
- Workflow is linear and opinionated -- less suited to targeted analysis of existing codebases
- No release management, sprint planning, or roadmap capabilities

### 2.2 SuperClaude

**Pros:**
- 40+ specialized commands covering the full developer support spectrum
- 3-pass evidence-gated audit system with grep-proof requirements (unique in the market)
- 29 named specialized agents with domain-specific behavioral definitions
- 10 MCP server integrations (Tavily, Context7, Sequential, Serena, Playwright, etc.)
- Native pytest plugin with auto-loaded fixtures and custom markers
- PM Agent with ConfidenceChecker (25-250x token ROI), SelfCheckProtocol, and ReflexionPattern
- Repository indexing with 94% token reduction
- Command recommendation engine with multi-language support
- Token budgeting and efficiency tracking
- Release management pipeline (roadmap, sprint, tasklist)
- 9 activatable personas for domain-specific behavior
- Wave -> Checkpoint -> Wave parallel execution (3.5x speedup)
- Cross-session learning via ReflexionPattern

**Cons:**
- Claude Code only -- no multi-platform support (no Cursor, Codex, Gemini CLI)
- No mandatory TDD enforcement -- testing is available but not forced
- Higher complexity: 40+ commands create a steeper learning curve
- Workflow is user-driven, not auto-triggered -- requires knowing which command to invoke
- No auto-triggering skills based on detected activity (user must explicitly call `/sc:*`)
- No git worktree management skill for parallel branch isolation
- No built-in subagent isolation pattern for long-running tasks
- Smaller community footprint compared to Superpowers' 104K stars
- Heavier installation footprint (Python package + MCP servers vs single plugin)

---

## 3. Unique Advantages

### 3.1 SuperClaude's Unique Advantages Over Superpowers

1. **Evidence-Gated Audit System**: The 3-pass cleanup audit with grep-proof requirements, duplication matrices, and 10% spot-check validation has no equivalent anywhere. This is SuperClaude's most defensible differentiator.

2. **MCP Server Ecosystem**: 10 integrated MCP servers providing live documentation, web search, browser automation, symbol navigation, and codebase retrieval. Superpowers has zero MCP integration.

3. **Repository Indexing**: 94% token reduction with structured index generation. Over 100 sessions, this saves 5.5M tokens. Superpowers has no equivalent.

4. **PM Agent / Confidence Gating**: Pre-execution confidence assessment that prevents wrong-direction work before tokens are spent. The 25-250x ROI on a 100-200 token investment is a structural efficiency advantage.

5. **29 Named Specialized Agents**: Domain-specific agents (5 audit agents, 4 architecture agents, security engineer, performance engineer, etc.) vs Superpowers' generic disposable subagents.

6. **Cross-Session Learning**: ReflexionPattern records errors and prevents recurrence across sessions. Superpowers has no memory or learning mechanism.

7. **Pytest Plugin Integration**: Auto-loaded fixtures, custom markers, complexity-based token budgets. Native Python testing infrastructure that Superpowers completely lacks.

8. **Release Management Pipeline**: Sprint execution, roadmap generation, tasklist management -- an entire project management layer that Superpowers does not address.

9. **Command Recommendation Engine**: `/sc:recommend` analyzes user intent and suggests optimal command sequences. Superpowers relies on auto-triggering (which works differently but doesn't help with discoverability).

10. **Multi-Domain Analysis**: `/sc:analyze` covers quality, security, performance, and architecture in a single command with severity ratings. Superpowers has no analysis capability.

### 3.2 What SuperClaude Can Learn From Superpowers

1. **Mandatory Workflow Enforcement**: Superpowers' auto-triggering skills mean the agent cannot skip brainstorming, cannot write code before tests, cannot merge without review. SuperClaude could benefit from an optional "strict mode" that chains commands automatically: `/sc:brainstorm` -> `/sc:design` -> `/sc:implement` -> `/sc:test` -> `/sc:cleanup-audit` -> `/sc:git`.

2. **TDD-First Hard Constraint**: Superpowers deletes code written before tests. SuperClaude could add a `--tdd-strict` flag to `/sc:implement` that refuses to write implementation code until tests exist.

3. **Multi-Platform Support**: Superpowers works with Claude Code, Cursor, Codex, OpenCode, and Gemini CLI. SuperClaude is Claude Code only. Expanding to at least Cursor would significantly increase addressable market.

4. **Auto-Triggering Skills**: Superpowers detects what the developer is doing and activates the appropriate skill automatically. SuperClaude requires explicit `/sc:*` invocation. Adding activity detection ("you appear to be debugging -- would you like to activate `/sc:troubleshoot`?") would reduce friction.

5. **Git Worktree Integration**: Superpowers automates worktree creation, setup verification, and cleanup. SuperClaude documents worktree usage but does not automate it via a dedicated command.

6. **Subagent Isolation Pattern**: Superpowers spawns fresh subagents per task to prevent context drift. While SuperClaude uses parallel agents, it could benefit from explicit context-isolation guarantees for long-running operations.

7. **Community Skill Ecosystem**: Superpowers' `writing-skills` guide and marketplace enable community contribution. SuperClaude could open a similar skill marketplace for community-authored commands.

8. **Simplicity of Onboarding**: Superpowers installs with one command and auto-triggers. SuperClaude's 40+ commands require learning which to use when. The `/sc:recommend` engine partially addresses this, but a "guided mode" for new users would help.

---

## 4. Architecture Comparison Summary

```
Superpowers                          SuperClaude
-----------                          -----------
Philosophy: Workflow enforcement     Philosophy: Targeted tool specialization
Model:      Linear pipeline          Model:      Command toolkit + agent pool
Skills:     ~14 (lifecycle-focused)  Commands:   40+ (domain-specialized)
Agents:     Generic, disposable      Agents:     29 named, persistent definitions
MCP:        None                     MCP:        10 servers integrated
Testing:    Mandatory TDD            Testing:    Pytest plugin + fixtures
Audit:      Plan-compliance review   Audit:      3-pass evidence-gated (unique)
Indexing:   None                     Indexing:   94% token reduction
Learning:   None                     Learning:   ReflexionPattern cross-session
Platforms:  5 (Claude, Cursor, etc.) Platforms:  1 (Claude Code only)
Stars:      104K                     Stars:      Internal/emerging
Install:    1 command (plugin)       Install:    pipx + superclaude install
```

---

## 5. Conclusion

Superpowers and SuperClaude are **complementary rather than competitive**. Superpowers provides the development discipline layer -- it ensures agents follow a rigorous process. SuperClaude provides the analytical depth layer -- it gives agents specialized tools for deep inspection, evidence-gated auditing, and cross-session learning.

The ideal developer support stack would combine Superpowers' mandatory workflow enforcement with SuperClaude's specialized analysis, audit, and MCP-powered intelligence. For teams using existing codebases that need targeted analysis and audit capabilities, SuperClaude is the stronger choice. For greenfield projects where enforcing disciplined development process is the priority, Superpowers provides guardrails that SuperClaude does not enforce.

SuperClaude's most defensible differentiators -- the 3-pass evidence-gated audit, 10-server MCP integration, pytest plugin infrastructure, and 29 specialized agents -- represent capabilities that Superpowers' architecture does not support and would require fundamental redesign to replicate.

---

*Report generated via /sc:analyze comparative analysis protocol*
*Sources: GitHub (obra/superpowers), Tavily search, internal codebase analysis*
