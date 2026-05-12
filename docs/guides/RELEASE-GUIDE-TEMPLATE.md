---
component: "[Component Name]"
component_version: "[e.g., 4.2.0 or skill-v2]"
covers_release: "[release tag or PR reference]"
last_updated: "[YYYY-MM-DD]"
author: "[name or agent]"
---

# [Component Name] — Release Guide

This guide covers the `[component]` [CLI tool / skill / command], including:
- what [each component / the skill] does,
- when to use it,
- how to [run it / invoke it],
- practical examples with all options,
- the [N-step/N-phase] [pipeline / architecture] ([brief description of key mechanisms]),
- [gate criteria and validation / quality gates and verification],
- [output artifacts and file structure],
- known limitations and gotchas,
- troubleshooting common issues,
- and how it fits into the **[upstream] -> [this component] -> [downstream]** workflow.

---

## 1) Release Summary (What is included)

### Core [command surface / capability]
[1-3 sentence description of what this component provides. Include the number of subcommands or primary operations.]

### [Migration notes (include if this replaces or refactors a prior version)]

[If this release changes behavior from a prior version, document:
- **What changed**: Concrete list of behavioral or structural changes
- **What broke**: Any backwards-incompatible changes
- **What to do**: Migration steps for users of the prior version
- **What was removed**: Features or behaviors that no longer exist

If this is a brand-new component with no prior version, omit this subsection.]

### Architecture overview
[Paragraph describing the high-level architecture. Include:
- The overall strategy (adversarial, multi-agent, deterministic, etc.)
- Key stages or phases
- What makes this approach distinctive]

### [Module structure / Skill file structure]
```
[Directory tree showing all relevant source files with inline comments describing each]
```

### Key design decisions
[Bullet list of 4-7 architectural decisions with brief rationale. Format: **Decision name**: Explanation.]

---

## 2) [Command Reference / Invocation Reference] — When and How to Use

[For each command or invocation method, include a subsection with:]

### `[command syntax]`

#### What it does
[2-3 sentences describing the operation.]

#### Use when
[Bullet list of 4-6 scenarios where this command is the right choice.]

#### Syntax
```bash
[full command syntax with placeholders]
```

#### [Positional arguments / Input requirements]
| [Argument / Input] | Required | Description |
|---------------------|----------|-------------|
| ... | ... | ... |

#### [Key options (for CLI tools)]
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| ... | ... | ... | ... |

#### Examples
```bash
# [Description of example]
[command example]

# [Description of example]
[command example]

# [Full production example with multiple options]
[command example with multiple flags]
```

[Repeat this subsection for each subcommand or invocation method.]

---

## 3) The [N]-Step/Phase [Pipeline / Architecture]

[Describe the overall execution flow.]

### Pipeline overview
```
[ASCII diagram showing the flow of steps/phases, including:
- Sequential dependencies
- Parallel execution points
- Gate/checkpoint locations
- Non-standard steps (deterministic, trailing, etc.)]
```

### [Step / Phase] details

| [Step / Phase] | [ID] | [Timeout / Parallel] | [Gate Tier / Agent Types] | Description |
|------|------|---------|-----------|-------------|
| ... | ... | ... | ... | ... |

[For complex pipelines, add a subsection per step/phase with detailed behavior.]

---

## 4) [Gate Criteria and Validation / Quality Gates and Validation]

[Describe the overall validation strategy.]

### [Per-gate or per-step gate details]

[For each gate, include:]
- **Gate name/location**
- **Enforcement tier** (STRICT/STANDARD/TRAILING or PASS/FAIL)
- **Checklist items** (numbered)
- **Verdict behavior** (what happens on pass/fail)
- **Retry/fix cycle limits**

---

## 5) Output Artifacts

[Describe where outputs go and what each artifact contains.]

### [Directory structure / Output file layout]
```
[Directory tree showing all output artifacts with inline descriptions]
```

### [Artifact reference table (if applicable)]

| Artifact | Source [Step / Phase] | Description |
|----------|----------------------|-------------|
| ... | ... | ... |

---

## 6) [Configuration / Content Rules / Depth Modes]

[Component-specific configuration section. Include any:]
- Mode selections (depth, tier, etc.)
- Content rules or format requirements
- Agent configuration
- Scope classification

---

## 7) Behind the Scenes: [What the Runtime Executes / How Execution Works]

[Detailed technical explanation of the execution mechanics. Include:]

### 7.1 [Call path / Execution flow]
[Step-by-step description of what happens when the command/skill is invoked.]

### 7.2 [Subprocess management / Agent spawning strategy]
[How child processes or subagents are managed.]

### 7.3 [State persistence / Resumability]
[How state is saved and how resume works.]

### 7.4 [Parallel execution details]
[Threading model, cross-cancellation, partitioning strategy.]

### 7.5 [Error handling]
[What happens on failure, halt diagnostics, retry behavior.]

---

## 8) End-to-End Workflow: [Full pipeline context]

[Show how this component fits into the larger workflow.]

### Stage [N]: [Upstream component]
```bash
[command or invocation]
```
[Brief description.]

### Stage [N+1]: [This component] <- **This [tool / skill]**
```bash
[command or invocation]
```
[Brief description of what this component produces.]

### Stage [N+2]: [Downstream component]
```bash
[command or invocation]
```
[Brief description.]

[Continue for all stages in the pipeline.]

---

## 9) Performance & Cost Expectations

[Help users plan resource usage before running the component.]

### Execution time estimates

| [Tier / Mode / Depth] | Approximate Wall Time | Agent Count | Notes |
|------------------------|----------------------|-------------|-------|
| ... | ... | ... | ... |

### Token consumption
[Rough token ranges by configuration. Include notes on which options significantly increase cost.]

### Resource requirements
[Any system requirements: disk space for artifacts, memory for large pipelines, network for web research, etc.]

---

## 10) Known Limitations & Gotchas

[Dedicated section for non-obvious behaviors, edge cases, and traps. Format each as:]

### [Short descriptive title]
**Symptom**: [What the user observes]
**Cause**: [Why it happens]
**Workaround**: [What to do about it]

[Include 4-8 items. Prioritize things that are surprising or frequently asked about.]

---

## 11) Troubleshooting

[Symptom-based lookup table for common issues.]

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| [Error message or observed behavior] | [Root cause] | [Concrete action to resolve] |
| ... | ... | ... |

[Include 6-10 entries covering the most common failure modes.]

---

## 12) Practical Use Cases

[8-10 use cases covering common and edge-case scenarios.]

### Use case [N]: [Descriptive title]
```bash
[command invocation]
```
[2-3 sentence explanation of what this does, why you'd choose these options, and what to expect.]

---

## 13) Quick [Command Cheat Sheet / Reference]

[Condensed reference for quick lookups.]

```bash
# --- [command group] ---

# [Basic usage]
[command]

# [Common variation 1]
[command with options]

# [Common variation 2]
[command with options]

# [Full production example]
[command with all common options]
```

[For skills: include key behaviors, output locations, and quality guarantees as bullet lists.]
