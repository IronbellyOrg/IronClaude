# SuperClaude Competitive Landscape: Final Consolidated Report

**Date**: 2026-03-23
**Methodology**: 3 deep research agents (exhaustive GitHub search) + 15 comparative analysis agents (14 completed, 1 killed)
**Total repos cataloged**: 96 across all three buckets
**Deep comparisons completed**: 14 of 15

---

## Table of Contents

1. [Three-Bucket Classification](#1-three-bucket-classification)
2. [Top Competitors by Bucket](#2-top-competitors-by-bucket)
3. [Cross-Cutting Strategic Findings](#3-cross-cutting-strategic-findings)
4. [Projects to Follow and Learn From](#4-projects-to-follow-and-learn-from)
5. [Projects to Consider Forking/Integrating](#5-projects-to-consider-forkingintegrating)
6. [SuperClaude's Unique Moats](#6-superclaudes-unique-moats)
7. [Top 10 Actionable Learnings](#7-top-10-actionable-learnings)

---

## 1. Three-Bucket Classification

### Bucket A: Feature/Project Planning & Roadmapping

| Component | Type | Description |
|-----------|------|-------------|
| `cli/roadmap/` | CLI Pipeline (24 modules) | Spec → roadmap with convergence, remediation |
| `cli/pipeline/` | Shared Infra (24 modules) | Gates, FMEA, dataflow, invariants |
| `/sc:roadmap` | Command | Multi-roadmap adversarial generation |
| `/sc:release-split` | Command | Release split analysis |
| `/sc:design` | Command | System architecture design |
| `/sc:spec-panel` | Command | Multi-expert spec review |
| `/sc:brainstorm` | Command | Requirements discovery |
| `/sc:adversarial` | Command | Structured debate pipeline |
| `/sc:workflow` | Command | Implementation workflows from PRDs |
| `/sc:estimate` | Command | Development estimation |
| `sc-roadmap-protocol` | Skill | Full roadmap generation protocol |
| `sc-release-split-protocol` | Skill | Release split with verification |
| `sc-adversarial-protocol` | Skill | Debate, scoring, merge protocol |
| system-architect | Agent | Systems design |
| requirements-analyst | Agent | Requirements analysis |
| debate-orchestrator | Agent | Adversarial debate coordination |
| business-panel-experts | Agent | Multi-expert business analysis |

### Bucket B: Tasklist Generation & Execution

| Component | Type | Description |
|-----------|------|-------------|
| `cli/sprint/` | CLI Pipeline (16 modules) | Supervised execution with KPI, TUI, tmux |
| `cli/tasklist/` | CLI Pipeline (6 modules) | Roadmap → tasklist bundles |
| `cli/cli_portify/` | CLI Pipeline (22+8 modules) | Workflow → deterministic pipeline |
| `pm_agent/` | Core (4 modules) | Confidence, self-check, reflexion, budget |
| `execution/` | Core (3 modules) | Wave parallel, reflection, self-correction |
| `/sc:task-unified` | Command | Compliance-tiered task execution |
| `/sc:task` | Command | Complex task with delegation |
| `/sc:pm` | Command | PM agent orchestration |
| `/sc:spawn` | Command | Epic → Story → Task breakdown |
| `/sc:tasklist` | Command | Roadmap-to-tasklist generation |
| `/sc:cli-portify` | Command | Workflow portification |
| `sc-tasklist-protocol` | Skill | Tasklist generation algorithm |
| `sc-task-unified-protocol` | Skill | Unified execution with TFEP |
| `sc-pm-protocol` | Skill | PDCA orchestration |
| `sc-cli-portify-protocol` | Skill | Portification protocol |
| `sc-validate-tests-protocol` | Skill | Tier classification validation |
| pm-agent | Agent | Project manager |

### Bucket C: Developer Support

| Component | Type | Description |
|-----------|------|-------------|
| `cli/audit/` | CLI Pipeline (42 modules) | Multi-pass evidence-gated audit |
| `cli/cleanup_audit/` | CLI Pipeline (13 modules) | Audit runner with TUI |
| `/sc:analyze` | Command | Multi-domain code analysis |
| `/sc:implement` | Command | Feature implementation with personas |
| `/sc:test` | Command | Testing with coverage |
| `/sc:build` | Command | Build/compile/package |
| `/sc:cleanup-audit` | Command | 3-pass repo audit |
| `/sc:cleanup` | Command | Execute cleanup recommendations |
| `/sc:improve` | Command | Systematic improvements |
| `/sc:troubleshoot` | Command | Issue diagnosis |
| `/sc:explain` | Command | Code explanation |
| `/sc:document` | Command | Documentation generation |
| `/sc:index` / `/sc:index-repo` | Command | Project indexing (94% token reduction) |
| `/sc:research` | Command | Deep web research |
| `/sc:recommend` | Command | Command recommendation |
| `/sc:git` | Command | Git with smart commits |
| `/sc:review-translation` | Command | Localization review |
| `/sc:reflect` | Command | Task validation |
| `sc-cleanup-audit-protocol` | Skill | Multi-pass audit protocol |
| `sc-recommend-protocol` | Skill | Recommendation engine |
| `confidence-check` | Skill | Pre-implementation assessment |
| 5 audit agents | Agents | Scanner, analyzer, comparator, consolidator, validator |
| 4 architecture agents | Agents | System, backend, frontend, devops |
| 3 quality agents | Agents | Quality, performance, security |
| 3 dev agents | Agents | Python-expert, refactoring, merge |
| 3 communication agents | Agents | Technical-writer, learning-guide, socratic-mentor |
| `pytest_plugin.py` | Plugin | Auto-loaded fixtures and markers |

---

## 2. Top Competitors by Bucket

### Bucket A: Planning & Roadmapping — Top 5 (Most → Least Similar)

| Rank | Project | Stars | Core Match | Key Differentiator vs SuperClaude |
|------|---------|-------|------------|-----------------------------------|
| 1 | **MetaGPT** | 65.6K | Multi-agent SOP-driven planning with PM/architect roles | Breadth (end-to-end code gen) but **zero quality gates** |
| 2 | **GitHub Spec Kit** | 78.7K | Spec → Plan → Tasks pipeline with cross-platform support | Simpler (4 phases) but **no adversarial validation** |
| 3 | **BMAD Method** | 39.4K | 21+ agents covering full SDLC, agile methodology | Broader lifecycle but **shallower planning depth** |
| 4 | **OpenSpec** | 32.9K | Spec-driven development across 20+ AI tools | Cross-platform reach but **no validation rigor** |
| 5 | **ChatDev** | 31.7K | Virtual software company with role-play seminars | End-to-end generation but **cooperative, not adversarial** |

### Bucket B: Tasklist & Execution — Top 5

| Rank | Project | Stars | Core Match | Key Differentiator vs SuperClaude |
|------|---------|-------|------------|-----------------------------------|
| 1 | **Claude Task Master** | 26K | PRD → structured tasks with MCP, 5+ editors | Broader reach but **zero quality gates, stateless** |
| 2 | **GSD** | 35K | Spec-driven phased execution, parallel agents | Context rot solution but **no compliance tiers, token expensive** |
| 3 | **Superpowers** | 28K | Auto-triggering skills, TDD enforcement, 5+ platforms | Methodology enforcement but **no sprint CLI, no KPI tracking** |
| 4 | **CCPM** | 6K | PRD → GitHub Issues, worktree parallel execution | GitHub-native but **convention-only quality gates** |
| 5 | **Forge AI** | <100 | Adversarial planning + deterministic DAG execution | Closest architectural match but **very early, small community** |

### Bucket C: Developer Support — Top 5

| Rank | Project | Stars | Core Match | Key Differentiator vs SuperClaude |
|------|---------|-------|------------|-----------------------------------|
| 1 | **Superpowers** | 104K | Skills framework, SDLC enforcement, 5+ platforms | Workflow methodology but **no audit pipeline** |
| 2 | **OpenClaw** | 328K | 5,400 skills, personas, multi-platform | Scale but **security issues, no evidence gating** |
| 3 | **claude-code-best-practice** | 17.4K | Claude Code configuration reference | Knowledge base but **not a framework** |
| 4 | **TheAuditor** | 200+ | Database-first audit, taint analysis, 4-vector convergence | Deeper SAST but **no evidence gating, no multi-agent** |
| 5 | **Skylos** | 500+ | Dead code (98% recall), MCP server, CI/CD, auto-fix | MCP-exposed audit but **single-pass, no evidence gates** |

---

## 3. Cross-Cutting Strategic Findings

### 3.1 SuperClaude's Unique Moats (No Competitor Replicates)

1. **Evidence-gated classification**: Every DELETE requires grep proof of zero references; every KEEP requires reference evidence. No other tool does this.
2. **Compliance tier system**: STRICT/STANDARD/LIGHT/EXEMPT classification prevents ceremony fatigue. Unique in the landscape.
3. **Portification**: Converting AI workflows into deterministic CLI pipelines (`cli_portify`). Entirely unique.
4. **Adversarial multi-roadmap generation** with structured debate, scoring, and merge. No competitor has this for roadmapping.
5. **Convergence detection** with TurnLedger budget accounting and monotonic progress enforcement.
6. **ReflexionPattern**: Cross-session error learning with >90% reuse rate.
7. **ConfidenceChecker**: Pre-execution assessment with 25-250x token ROI.

### 3.2 SuperClaude's Biggest Gaps (Competitors Do Better)

1. **Cross-platform support**: SuperClaude is Claude Code-only. Superpowers works on 5+ platforms; OpenSpec on 20+; Task Master on 5+ editors.
2. **Community scale**: 305 stars vs OpenClaw (328K), Superpowers (104K), Spec Kit (78.7K), MetaGPT (65.6K).
3. **Onboarding friction**: Multi-step pipeline understanding required. GSD/Spec Kit/Task Master have 5-minute onboarding.
4. **CI/CD integration**: No GitHub Action, no SARIF output, no PR annotations. Skylos and CodeRabbit have this.
5. **MCP server exposure**: SuperClaude consumes MCP but doesn't expose its capabilities as MCP tools. Skylos, TheAuditor, and Task Master all expose via MCP.
6. **Taint analysis**: TheAuditor has full IFDS taint tracking. SuperClaude has none.
7. **Context rot mitigation**: GSD's fresh-context-per-task model genuinely solves this. SuperClaude's Wave model doesn't isolate context.

### 3.3 Market Trends (March 2026)

- **Spec-driven development** is the dominant pattern (Spec Kit, OpenSpec, GSD, BMAD all enforce it)
- **Fresh-context-per-task** is gaining traction as the answer to context rot (GSD, Forge AI)
- **Skill/plugin marketplaces** for coding agents are exploding (OpenClaw 328K, Superpowers 104K)
- **MCP server exposure** is becoming table stakes for developer tools
- **Cross-platform compatibility** is a competitive requirement — single-platform tools are at risk

---

## 4. Projects to Follow and Learn From

### Must-Watch (Follow Closely)

| Project | Why | What to Learn |
|---------|-----|---------------|
| **GitHub Spec Kit** (78.7K) | GitHub-backed, massive adoption, could add adversarial validation | Constitution concept, cross-platform prompts, adoption model |
| **GSD** (35K) | Explosive growth, solves context rot | Fresh-context-per-task, orchestrator context budget |
| **Claude Task Master** (26K) | De facto task MCP server | MCP tool design, cross-editor reach, onboarding simplicity |
| **Superpowers** (104K) | Closest methodology match, marketplace leader | Auto-triggering skills, marketplace model, cross-platform skills |
| **BMAD Method** (39.4K) | Full SDLC coverage, enterprise adoption | Quick Flow path, agent persona design, lifecycle coverage |

### Worth Tracking

| Project | Why | What to Learn |
|---------|-----|---------------|
| **MetaGPT** (65.6K) | Multi-agent SOP pioneer | Visual artifacts (Mermaid), lower-friction entry mode |
| **OpenSpec** (32.9K) | 20+ platform reach | Cross-platform command generation architecture |
| **CCPM** (6K) | GitHub-native PM for Claude Code | Issue sync, worktree parallel execution |
| **TheAuditor** (200+) | Database-first audit | SQLite persistence, taint analysis, convergence scoring |
| **Skylos** (500+) | MCP-exposed audit with 98% recall | MCP server design, CI/CD integration, SARIF output |
| **Forge AI** (<100) | Closest architectural match | Adversarial DAG execution, fresh-agent-per-step |

---

## 5. Projects to Consider Forking/Integrating

### Integration Opportunities (Use Together)

| Project | Integration Idea | Value |
|---------|-----------------|-------|
| **Skylos** | Use as MCP evidence source — Skylos finds candidates (98% recall), SuperClaude verifies with evidence gates | Best-of-both: high recall + high precision |
| **Task Master** | Expose SuperClaude gates as MCP tools that Task Master can call | Cross-platform quality gates without rebuilding editor integration |
| **Spec Kit** | SuperClaude validates what Spec Kit generates. Position as complementary layers | Spec Kit generates, SuperClaude verifies |
| **TheAuditor** | Import SQLite results as evidence inputs for SuperClaude's audit pipeline | Database-backed determinism + evidence-gated safety |

### Fork/Study Opportunities

| Project | What to Study | Applicable To |
|---------|--------------|---------------|
| **OpenSpec** | Cross-platform command generation architecture | Building SuperClaude skills that work on Cursor/Copilot/Gemini |
| **GSD** | Fresh-context-per-task execution model | Improving sprint executor's context isolation |
| **Superpowers** | Auto-triggering skill bootstrap mechanism | Making skills activate without explicit `/sc:` invocation |
| **CCPM** | GitHub Issues bidirectional sync | Adding optional issue tracker integration |

---

## 6. SuperClaude's Unique Position

```
                    PLANNING DEPTH
                         ↑
                         │
           MetaGPT ·     │     · SuperClaude
                         │       (adversarial + evidence-gated)
         ChatDev ·       │
                         │
    BMAD ·               │     · Forge AI
                         │
         Spec Kit ·      │     · CCPM
                         │
    OpenSpec ·           │     · Superpowers
                         │
         ─────────────────┼──────────────────→  EXECUTION RIGOR
                         │
    GSD ·                │     · Task Master
                         │
```

SuperClaude occupies the **high planning depth + high execution rigor** quadrant. No competitor occupies this same space. The nearest are:
- **MetaGPT**: High planning depth, low execution rigor (no quality gates)
- **GSD**: Moderate planning, moderate execution (context management, not quality gates)
- **Forge AI**: Architecturally closest but too early (<100 stars)

---

## 7. Top 10 Actionable Learnings

Synthesized from all 14 completed analyses, ordered by estimated impact:

### 1. Expose SuperClaude as MCP Tools
**Source**: Skylos, Task Master, TheAuditor analyses
**Action**: Wrap audit pipeline, confidence checker, and quality gates as MCP tools
**Impact**: Cross-platform reach without rebuilding editor integrations. Any AI agent in any editor can call SuperClaude's quality infrastructure.

### 2. Add Fresh-Context-Per-Task to Sprint Executor
**Source**: GSD analysis
**Action**: Switch sprint executor from per-phase to per-task subprocess spawning
**Impact**: Eliminates context rot in long sprints. Combines GSD's isolation with SuperClaude's quality gates and KPI tracking.

### 3. Build Cross-Platform Skill Layer
**Source**: OpenSpec, Superpowers analyses
**Action**: Generate simplified Markdown-only versions of key skills for Cursor, Copilot, Gemini CLI
**Impact**: 10-100x reach expansion. Two-layer architecture: portable Markdown for reach + Python CLI for depth.

### 4. Add Auto-Triggering Bootstrap
**Source**: Superpowers analysis
**Action**: Create a bootstrap mechanism that checks skill applicability before actions, rather than requiring explicit `/sc:` invocation
**Impact**: Reduces friction, prevents process shortcuts, matches market expectation.

### 5. Simplify Entry Point with Tiered Commands
**Source**: OpenSpec, claude-code-best-practice, Spec Kit analyses
**Action**: Create 3 tiers: Core (5 commands), Standard (12), Full (38). New users see Core only.
**Impact**: Dramatically reduces onboarding friction. Addresses community anti-pattern concern about long command lists.

### 6. Add CI/CD Integration
**Source**: Skylos analysis
**Action**: GitHub Action wrapper, SARIF output, PR annotations, diff-aware mode
**Impact**: Enables audit pipeline in CI without interactive Claude Code session.

### 7. Adopt Constitution Concept
**Source**: Spec Kit analysis
**Action**: Unify CLAUDE.md/RULES.md/PRINCIPLES.md into a single consulted document
**Impact**: Cleaner project governance, mirrors successful pattern from 78.7K-star project.

### 8. Add SQLite Persistence for Audit Results
**Source**: TheAuditor analysis
**Action**: Store audit results in SQLite for post-hoc queries and incremental re-auditing
**Impact**: Enables trend tracking, regression detection, and arbitrary queries after audit completes.

### 9. Add Basic Taint Analysis
**Source**: TheAuditor analysis
**Action**: Even a simplified source/sink pattern matcher closes the largest SAST capability gap
**Impact**: Moves audit pipeline from structural analysis into security analysis territory.

### 10. Create Guided Onboarding Command
**Source**: OpenSpec, BMAD analyses
**Action**: Build `/sc:onboard` — a 15-minute interactive walkthrough of core capabilities
**Impact**: Converts browsing users to active users. OpenSpec and BMAD both validate this pattern.

---

## Appendix: All Generated Reports

### Phase 1: Research Reports (3)
| Report | Location |
|--------|----------|
| Planning & Roadmapping Landscape | `docs/research/competitive-landscape-planning-tools.md` |
| Tasklist & Execution Landscape | `docs/research/competitive-landscape-tasklist-execution-2026.md` |
| Developer Support Landscape | `docs/research/competitive-landscape-developer-tools-2026.md` |

### Phase 2: Comparative Analyses (14 of 15)

**Planning & Roadmapping (5/5)**:
| Comparison | Location |
|------------|----------|
| MetaGPT vs SuperClaude | `docs/analysis/metagpt-vs-superclaude-planning-comparison.md` |
| OpenSpec vs SuperClaude | `docs/analysis/openspec-vs-superclaude-comparison.md` |
| Spec Kit vs SuperClaude | `docs/analysis/spec-kit-vs-superclaude-comparison.md` |
| BMAD vs SuperClaude | `docs/analysis/bmad-vs-superclaude-comparison.md` |
| ChatDev vs SuperClaude | `docs/generated/chatdev-vs-superclaude-analysis.md` |

**Tasklist & Execution (4/5)**:
| Comparison | Location |
|------------|----------|
| Claude Task Master vs SuperClaude | `docs/analysis/claude-task-master-vs-superclaude-comparison.md` |
| GSD vs SuperClaude | `docs/analysis/gsd-vs-superclaude-comparison.md` |
| Superpowers vs SuperClaude (execution) | `docs/analysis/superpowers-vs-superclaude-comparison.md` |
| CCPM vs SuperClaude | `docs/research/ccpm-vs-superclaude-comparison.md` |
| ~~Forge AI vs SuperClaude~~ | ~~Agent killed before completion~~ |

**Developer Support (5/5)**:
| Comparison | Location |
|------------|----------|
| Superpowers vs SuperClaude (dev support) | `docs/generated/superpowers-vs-superclaude-comparison.md` |
| OpenClaw vs SuperClaude | `docs/analysis/openclaw-vs-superclaude-comparison.md` |
| claude-code-best-practice vs SuperClaude | `docs/analysis/claude-code-best-practice-vs-superclaude.md` |
| TheAuditor vs SuperClaude | `docs/analysis/theauditor-vs-superclaude-comparison.md` |
| Skylos vs SuperClaude | `docs/generated/skylos-vs-superclaude-comparison.md` |

---

*Generated by 18 parallel research and analysis agents on 2026-03-23.*
