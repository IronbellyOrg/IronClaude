---
command: "/sc:business-panel"
category: "Analysis & Strategic Planning"  
purpose: "Multi-expert business analysis with adaptive interaction modes"
wave-enabled: true
performance-profile: "complex"
---

# /sc:business-panel - Business Panel Analysis System

## Overview

AI facilitated panel discussion between renowned business thought leaders analyzing documents through their distinct frameworks and methodologies.

## Expert Panel

### Available Experts

- **Clayton Christensen**: Disruption Theory, Jobs-to-be-Done
- **Michael Porter**: Competitive Strategy, Five Forces
- **Peter Drucker**: Management Philosophy, MBO
- **Seth Godin**: Marketing Innovation, Tribe Building
- **W. Chan Kim & Renée Mauborgne**: Blue Ocean Strategy
- **Jim Collins**: Organizational Excellence, Good to Great
- **Nassim Nicholas Taleb**: Risk Management, Antifragility
- **Donella Meadows**: Systems Thinking, Leverage Points
- **Jean-luc Doumont**: Communication Systems, Structured Clarity

## Analysis Modes

### Phase 1: DISCUSSION (Default)

Collaborative analysis where experts build upon each other's insights through their frameworks.

### Phase 2: DEBATE

Adversarial analysis activated when experts disagree or for controversial topics.

### Phase 3: SOCRATIC INQUIRY

Question-driven exploration for deep learning and strategic thinking development.

## Usage

### Basic Usage

```bash
/sc:business-panel [document_path_or_content]
```

### Advanced Options

```bash
/sc:business-panel [content] --experts "porter,christensen,meadows"
/sc:business-panel [content] --mode debate
/sc:business-panel [content] --focus "competitive-analysis"
/sc:business-panel [content] --synthesis-only
```

### Mode Commands

- `--mode discussion` - Collaborative analysis (default)
- `--mode debate` - Challenge and stress-test ideas
- `--mode socratic` - Question-driven exploration
- `--mode adaptive` - System selects based on content

### Expert Selection

- `--experts "name1,name2,name3"` - Select specific experts
- `--focus domain` - Auto-select experts for domain
- `--all-experts` - Include all 9 experts

### Output Options

- `--synthesis-only` - Skip detailed analysis, show synthesis
- `--structured` - Use symbol system for efficiency
- `--verbose` - Full detailed analysis
- `--questions` - Focus on strategic questions
- `--output <file>` - Write the analysis to that file (a standalone run writes a file only when you pass it)

## Auto-Persona Activation

- **Auto-Activates**: Analyzer, Architect, Mentor personas
- **MCP Integration**: Context7 (business patterns)
- **Tool Orchestration**: Read, Grep, Write, MultiEdit, TodoWrite

## Integration Notes

- Compatible with all thinking flags (--think, --think-hard, --ultrathink)
- Supports wave orchestration for comprehensive business analysis
- Integrates with scribe persona for professional business communication

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:business-panel` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/business-panel-report.md` when `--output` is absent. The run is succeeded when the analysis document is written, and failed otherwise.
- **Person-mode flags.** `--mode socratic` and `--mode=socratic` are refused before any work (contract `worker_status: failed`, the flag in `reason`). `--mode adaptive` never selects the Socratic mode under `--unattended`; it chooses between discussion and debate only.
- **Gates.** There is no other gate. Nested invocations: none.
- **Outward actions.** It pushes, commits and stages nothing.

## CRITICAL BOUNDARIES

**SYNTHESIS OUTPUT ONLY - NOT IMPLEMENTATION**

This command produces EXPERT ANALYSIS and RECOMMENDATIONS only.

**Default behavior**:

- Assemble expert panel
- Conduct analysis/discussion
- **STOP with synthesis document** - do not implement recommendations

**Completion Criteria**:

- All relevant experts have contributed
- Consensus or disagreements documented
- Actionable recommendations provided

**Explicitly Will NOT**:

- Implement any business recommendations
- Make code or architectural changes
- Execute decisions without user approval

**Output**: Business analysis document containing:

- Expert perspectives (9 simulated experts)
- Consensus points
- Disagreements with reasoning
- Priority-ranked recommendations

**Next Step**: User reviews recommendations, then:

- Use `/sc:design` for architectural changes
- Use `/sc:implement` for feature development
- Use `/sc:workflow` for planning
