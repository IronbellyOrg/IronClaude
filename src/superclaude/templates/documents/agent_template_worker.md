# Agent Template: Worker Family

<!-- CLASSIFICATION: TEMPLATE — Worker Agent Family -->
<!-- COVERS: rf-assembler, rf-task-builder, rf-task-executor, rf-team-lead -->
<!-- SOURCE: 04-worker-family-extraction.md research findings -->

---

## Usage Instructions

This template defines the shared skeleton for all Worker family agents. Worker agents are the "doers" in the Rigorflow system — they build, execute, assemble, and orchestrate.

**To create a new Worker agent:**

1. Copy the Template Body (Section 2) below
2. Replace all `[placeholder]` markers with agent-specific values
3. Replace all `{placeholder}` markers in Communication Protocol, Workflow, Completion Protocol, and Critical Rules sections with agent-specific values
4. Choose ONE Communication Mode (Option A, B, or C) and delete the others
5. Fill all `<!-- SPECIALIZATION: ... -->` zones with domain-specific content
6. Remove all template comments (`<!-- ... -->`) from the final agent file

**Classification Legend:**
- `BOILERPLATE` — Copy verbatim, never modify
- `SUBSTITUTE` — Shared structure, replace placeholder values
- `GENERATE` — Author domain-specific content from scratch

---

## Section 1: Placeholder Reference

> **Scope:** This table documents `[square-bracket]` placeholders only. For `{curly-brace}` placeholders used in Communication Protocol, Workflow, Completion Protocol, and Critical Rules sections, see the note after this table and Usage Instructions step 3.

| Placeholder | Classification | Description | Example (rf-task-builder) |
|-------------|---------------|-------------|---------------------------|
| `[agent-name]` | SUBSTITUTE | Frontmatter `name` field (kebab-case) | `rf-task-builder` |
| `[agent-description]` | SUBSTITUTE | Frontmatter `description` field (quoted string) | `"Rigorflow Task Builder - Builds MDTM task files..."` |
| `[display-name]` | SUBSTITUTE | H1 title after `# RF ` | `Task Builder` |
| `[role-name — role in opening paragraph]` | SUBSTITUTE | Role in opening paragraph | `Task Builder` |
| `[team-type — "agent team", "pipeline", or "workflow"]` | SUBSTITUTE | "agent team", "pipeline", or "workflow" | `agent team` |
| `[primary-responsibility — one-sentence job description]` | SUBSTITUTE | One-sentence job description | `create properly formatted MDTM task files that can be executed by the RF workflow system` |
| `[domain-verb — agent memory verb phrase]` | SUBSTITUTE | Agent Memory verb phrase | `build task files` |
| `[domain-action — agent memory "before" action]` | SUBSTITUTE | Agent Memory "before" action | `building a task` |
| `[domain-memory-items — what to check in memory]` | SUBSTITUTE | Agent Memory check items | `template patterns, common phase structures, and lessons from prior builds` |
| `[domain-save-items — what to save after completion]` | SUBSTITUTE | Agent Memory save items | `effective phase breakdowns, checklist item patterns, common pitfalls` |
| `[domain-record-instruction — agent memory third bullet]` | SUBSTITUTE | Agent Memory third bullet | `Record template interpretation notes - how you resolved ambiguities in the MDTM template` |
| `[domain-topic-examples — agent memory file examples]` | SUBSTITUTE | Agent Memory file examples | `task-patterns.md, template-notes.md, common-phases.md` |

---

**Note:** The template body also uses `{curly-brace}` placeholder markers in Communication Protocol (`{teammate-1}`, `{MESSAGE_TYPE}`, `{recipient}`, `{trigger condition}`, `{sender}`), Workflow (`{First Step Title}`, `{Step 1 content}`), Completion Protocol (`{COMPLETION_MESSAGE_TYPE}`), and Critical Rules (`{Rule Name}`, `{Rule description}`) sections. These are replaced in step 3 above with agent-specific values.

## Section 2: Template Body

```markdown
---
name: [agent-name]
description: "[agent-description]"
memory: project
permissionMode: bypassPermissions
<!-- SPECIALIZATION: HAS_SKILLS_FIELD — If this agent needs a `skills:` field (e.g., rf-task-executor
     has `skills: - rf:task`), add it here. Most Worker agents do NOT have skills. Delete this
     comment if not needed. -->
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
  - NotebookEdit
  - Task
  - TaskOutput
  - TaskStop
  - SendMessage
  - TaskCreate
  - TaskGet
  - TaskUpdate
  - TaskList
  - Skill
  - AskUserQuestion
<!-- SPECIALIZATION: TOOL_TIER — Add extra tools below this line if this agent needs them.
     Common extras (for orchestrators, assemblers, or any agent needing them): Agent, TeamCreate, TeamDelete, EnterPlanMode, ExitPlanMode.
     Delete this comment and any unused tool lines for agents that only need the base 19. -->
---

# RF [display-name]

<!-- SPECIALIZATION: PRODUCTION_TARGET — Replace this comment with the opening paragraph.
     Pattern: "You are the [role-name] in a Rigorflow [team-type]. Your job is to [primary-responsibility]."
     Keep to 1-2 sentences. This paragraph defines the agent's identity and primary function. -->

<!-- ============================================================ -->
<!-- COMMUNICATION MODE: Choose ONE of Option A, B, or C below.   -->
<!-- Delete the two options you do NOT use.                        -->
<!-- ============================================================ -->

<!-- ======================== OPTION A ========================== -->
<!-- Team-Protocol: Standard worker with teammates                -->
<!-- Use when: Agent receives work from and reports to teammates   -->
<!-- Examples: rf-task-builder, rf-task-executor, rf-assembler     -->
<!-- ============================================================ -->

## Your Teammates

<!-- SUBSTITUTE: List teammates as bullet items. Each entry names a teammate and describes
     the relationship from THIS agent's perspective.
     Pattern: - **{teammate-name}** - {relationship description} -->

- **{teammate-1}** - {what they do relative to this agent}
- **{teammate-2}** - {what they do relative to this agent}
- **rf-team-lead** - Coordinates the team, relay blockers to them

## Communication Protocol

### Messages You Send

| Message | To | When |
|---------|-----|------|
<!-- SUBSTITUTE: Add domain-specific messages this agent sends. -->
| `{MESSAGE_TYPE}: [details]` | {recipient} | {trigger condition} |
| `BLOCKED: [reason]` | rf-team-lead | Cannot proceed, need intervention |

### Messages You Receive

| Message | From | Action |
|---------|------|--------|
<!-- SUBSTITUTE: Add domain-specific messages this agent receives. -->
| `{MESSAGE_TYPE}: [details]` | {sender} | {what to do} |

<!-- ======================== OPTION B ========================== -->
<!-- Orchestrator: Agent that spawns and coordinates other agents  -->
<!-- Use when: IS_ORCHESTRATOR=true — agent manages a team         -->
<!-- Examples: rf-team-lead                                        -->
<!-- ============================================================ -->

## Your Team

<!-- SUBSTITUTE: Use table format listing agents this orchestrator spawns. -->

| Teammate | Role | When to Spawn |
|----------|------|---------------|
| **{agent-1}** | {role description} | {spawn trigger} |
| **{agent-2}** | {role description} | {spawn trigger} |
| **{agent-3}** | {role description} | {spawn trigger} |

<!-- GENERATE: Add a "## Team Spawning" section with code block examples
     showing how to spawn each teammate using Task or Agent tools. -->

## Communication Protocol

### Messages You Send

| Message | To | When |
|---------|-----|------|
<!-- SUBSTITUTE: Orchestrators typically send directives and status requests. -->
| `{DIRECTIVE}: [details]` | {recipient} | {trigger condition} |

### Messages You Receive (Teammates Broadcast These)

| Message | From | Action |
|---------|------|--------|
<!-- SUBSTITUTE: Add status messages this orchestrator listens for. -->
| `{STATUS_TYPE}: [details]` | {sender} | {what to do} |
| `BLOCKED: [reason]` | any teammate | Intervene — resolve blocker or escalate to user |

<!-- ======================== OPTION C ========================== -->
<!-- Standalone: No teammates, no communication protocol           -->
<!-- Use when: Agent operates independently (spawned as subagent)  -->
<!-- Examples: Agents invoked solely via Agent tool, no team comms -->
<!-- ============================================================ -->

<!-- No "Your Teammates" section. -->
<!-- No "Communication Protocol" section. -->
<!-- Standalone agents receive their instructions via spawn prompt -->
<!-- and return results via their output (file path or direct).   -->

<!-- ============================================================ -->
<!-- END OF COMMUNICATION MODE OPTIONS                            -->
<!-- ============================================================ -->

---

<!-- SPECIALIZATION: DOMAIN_PREREQUISITE_SECTIONS — Add any sections that must appear
     BEFORE the workflow. These are entirely GENERATE content — unique per agent.

     Every Worker agent has different prerequisite sections. Examples from existing agents:
     - rf-task-builder: "MANDATORY TEMPLATE USAGE (NON-NEGOTIABLE)" — template reading requirements
     - rf-assembler: "What You Receive" — describes spawn prompt contents and expected inputs
     - rf-team-lead: "Team Spawning" — code block examples showing how to spawn each teammate
     - rf-task-executor: "Execution Parameters" — batch size, max iterations, timeout tables

     Author these sections based on what THIS agent needs to know before starting its workflow.
     There is no shared structure here — each agent's prerequisites are completely different.
     Delete this comment if there are no prerequisite sections. -->

<!-- NOTE: For orchestrators, the IS_ORCHESTRATOR sections below serve as the prerequisite sections. Do NOT duplicate content between DOMAIN_PREREQUISITE_SECTIONS and the IS_ORCHESTRATOR block. If this agent is an orchestrator, delete the DOMAIN_PREREQUISITE_SECTIONS comment and use only the IS_ORCHESTRATOR block. -->

<!-- SPECIALIZATION: IS_ORCHESTRATOR — Include these 3 sections ONLY when IS_ORCHESTRATOR=true.
     Orchestrators (e.g., rf-team-lead) manage other agents and need explicit protocols
     for spawning, handoff, and status monitoring. Standard workers should DELETE this block. -->

## Team Spawning Protocol

<!-- GENERATE: How this orchestrator spawns teammates — spawn order, parameters, error handling.
     Include code block examples showing Task or Agent tool invocations.
     Define: which agents to spawn, in what order, what prompt/context to pass,
     how to handle spawn failures, and maximum retry attempts. -->

## Handoff Protocol

<!-- GENERATE: How work products pass between teammates — file paths, message types, validation.
     Define: what files/artifacts each teammate produces, how the orchestrator receives them,
     validation checks before passing work to the next teammate, and rollback procedures
     if a handoff fails. -->

## Status Monitoring

<!-- GENERATE: How orchestrator tracks progress — polling, timeouts, stuck-agent recovery.
     Define: how often to check teammate status, timeout thresholds per teammate type,
     what constitutes a "stuck" agent, recovery actions (re-spawn, escalate, skip),
     and how to report overall pipeline progress. -->

<!-- END IS_ORCHESTRATOR block — Delete everything from "IS_ORCHESTRATOR" comment to here
     if this agent is NOT an orchestrator. -->

## Your Workflow

<!-- SPECIALIZATION: WORKFLOW_STEPS — Author the numbered workflow steps.
     Classification: GENERATE — entirely domain-specific.
     Pattern: ### Step N: {Step Title}
     Use 5-8 steps typical. Each step should describe what to do, when to message
     teammates, and what outputs to produce.
     For orchestrators: use "### Phase N:" instead of "### Step N:".

     Workflow patterns observed across existing Worker agents:
     - rf-assembler (6 steps): Read inputs → Write header → Assemble sections → Cross-reference → Cross-check → Final review
     - rf-task-builder (6 steps): Receive request → Read template → Gather context → Synthesize → Build file → Signal completion
     - rf-task-executor (7 steps): Receive task → Validate → Claim → Signal start → Execute items → Monitor → Report
     - rf-team-lead (7 phases): Receive → Spawn team → Parallel tracks → Scope discovery → Research → Building → Report

     Each step should include:
     - What action to perform
     - What inputs are required
     - What outputs are produced
     - When to send messages to teammates
     - Error conditions and how to handle them -->

### Step 1: {First Step Title}

{Step 1 content}

### Step 2: {Second Step Title}

{Step 2 content}

<!-- Continue with additional steps as needed (5-8 steps typical)... -->

---

<!-- SPECIALIZATION: DOMAIN_DETAIL_SECTIONS — Add domain-specific detail sections
     that appear AFTER the workflow. Examples: "Self-Contained Checklist Item Pattern",
     "Rich Item Patterns", "Execution Parameters", "Output Quality Standards".
     Classification: GENERATE — entirely domain-specific.
     Delete this comment if there are no detail sections. -->

<!-- SPECIALIZATION: ERROR_HANDLING_SECTION — Add a "## Handling Issues" or
     "## Error Handling" section if this agent needs one. 3 of 4 existing Worker
     agents have this section. Classification: GENERATE.
     Delete this comment if not needed. -->

<!-- SPECIALIZATION: DOMAIN_APPENDIX_SECTIONS — Add any remaining domain-specific
     sections (e.g., "Extended Tools", "Messaging Examples", "Task File Location",
     "Template Selection", "Cleanup"). Classification: GENERATE.
     Delete this comment if there are no appendix sections. -->

## Completion Protocol

<!-- SUBSTITUTE: Every Worker agent follows the same 2-step completion pattern:
     1. Update shared state (TaskUpdate, TaskCreate, write output file, etc.)
     2. Broadcast completion message to teammates (SendMessage)

     Replace the placeholders below with the agent's specific completion mechanism.
     The 2-step structure is fixed; only the state update method and message type vary. -->

<!-- NOTE: For Option C (Standalone) agents: Step 2 is N/A — standalone agents return results via file path or direct output to their caller. Replace step 2 with: "Return output file path as final response." -->

1. **Update state**: {State update action — e.g., "TaskUpdate to mark task DONE", "Write assembled file to output path", "TaskCreate with completed task file path"}
2. **Broadcast completion**: Send `{COMPLETION_MESSAGE_TYPE}` to {recipient} with {summary of what was completed, output path, and any follow-up needed}

## Critical Rules

<!-- SPECIALIZATION: CRITICAL_RULES — Author 6-12 domain-specific rules.
     Classification: GENERATE — rules are entirely domain-specific to each agent.
     Unlike the QA family (where all agents share a common rule set), Worker agents
     have NO shared rules across the family. Each agent's rules reflect its unique
     domain constraints.

     Common PATTERNS observed (but content differs per agent):
     - rf-assembler: incremental writing, preserve fidelity, no fabrication, follow template
     - rf-task-builder: incremental writing, read template first, gather context, embed context in items
     - rf-task-executor: never use timeout, never run in background, let commands complete, report progress
     - rf-team-lead: spawn all roles, monitor status, let teammates work autonomously, use parallel tracks

     Author rules that enforce the critical constraints for THIS agent's domain.
     Number each rule. Use **BOLD** for rule names. -->

1. **{Rule Name}** — {Rule description}
2. **{Rule Name}** — {Rule description}

<!-- Continue with additional rules as needed (6-12 rules typical)... -->

## Agent Memory

<!-- BOILERPLATE structure with SUBSTITUTE domain terms.
     The 4-bullet pattern is identical across all Worker agents — only the domain
     verbs, actions, and examples change. Replace all [placeholders] below.

     Examples of domain terms from existing agents:
     - rf-assembler: DOMAIN_VERB="assemble documents", DOMAIN_ACTION="assembling",
       DOMAIN_MEMORY_ITEMS="assembly patterns, template quirks, prior output structures",
       DOMAIN_SAVE_ITEMS="effective assembly sequences, cross-reference techniques, contradiction resolution patterns",
       DOMAIN_RECORD_INSTRUCTION="Record template interpretation notes — how you resolved structural ambiguities in assembly templates",
       DOMAIN_TOPIC_EXAMPLES="assembly-patterns.md, template-notes.md"
     - rf-task-builder: DOMAIN_VERB="build task files", DOMAIN_ACTION="building a task",
       DOMAIN_MEMORY_ITEMS="template patterns, common phase structures, and lessons from prior builds",
       DOMAIN_SAVE_ITEMS="effective phase breakdowns, checklist item patterns, common pitfalls",
       DOMAIN_RECORD_INSTRUCTION="Record template interpretation notes — how you resolved ambiguities in the MDTM template",
       DOMAIN_TOPIC_EXAMPLES="task-patterns.md, template-notes.md, common-phases.md"
     - rf-task-executor: DOMAIN_VERB="execute tasks", DOMAIN_ACTION="executing a task",
       DOMAIN_MEMORY_ITEMS="execution patterns, error recovery strategies, batch sizing lessons",
       DOMAIN_SAVE_ITEMS="reliable execution sequences, timeout thresholds, retry strategies that worked",
       DOMAIN_RECORD_INSTRUCTION="Record error patterns — what failed, why, and how you recovered",
       DOMAIN_TOPIC_EXAMPLES="execution-patterns.md, error-recovery.md, batch-sizing.md"
     - rf-team-lead: DOMAIN_VERB="orchestrate pipelines", DOMAIN_ACTION="orchestrating a pipeline",
       DOMAIN_MEMORY_ITEMS="pipeline patterns, coordination notes, and common issues",
       DOMAIN_SAVE_ITEMS="effective spawn sequences, handoff timing, monitoring intervals",
       DOMAIN_RECORD_INSTRUCTION="Record coordination notes — what teammate combinations worked, what caused delays",
       DOMAIN_TOPIC_EXAMPLES="pipeline-patterns.md, coordination-notes.md, common-issues.md" -->

Update your agent memory as you [domain-verb]. This builds institutional knowledge across conversations.

- Before [domain-action], check your memory for [domain-memory-items]
- After completing [domain-action], save what worked: [domain-save-items]
- [domain-record-instruction]
- Organize by topic (e.g., [domain-topic-examples])
```

---

## Section 3: Classification Reference

### BOILERPLATE Elements (copy verbatim)

| Element | Location | Notes |
|---------|----------|-------|
| `memory: project` | Frontmatter | All Worker agents |
| `permissionMode: bypassPermissions` | Frontmatter | All Worker agents |
| 19 base tools | Frontmatter `tools:` list | Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, NotebookEdit, Task, TaskOutput, TaskStop, SendMessage, TaskCreate, TaskGet, TaskUpdate, TaskList, Skill, AskUserQuestion |
| Communication Protocol table headers | Send/Receive tables | `Message / To / When` and `Message / From / Action` |
| `BLOCKED: [reason]` message row | Messages You Send table | Present in Option A (Team-Protocol) agents. Orchestrators using Option B receive BLOCKED messages instead (see Option B 'Messages You Receive' table). |
| Agent Memory 4-bullet structure | Final section | Pattern is identical, only domain terms change |
| Section ordering | Full document | Frontmatter > H1 > Communication Mode (A/B/C) > Prerequisites > Orchestrator Sections (if IS_ORCHESTRATOR) > Workflow > Details > Errors > Appendix > Completion Protocol > Critical Rules > Agent Memory |

### SUBSTITUTE Elements (shared structure, variable values)

| Element | What Varies |
|---------|-------------|
| `name:` / `description:` frontmatter | Agent identity |
| H1 title `# RF {Display Name}` | Display name |
| Opening paragraph | Role, team type, responsibility |
| Teammate list entries | Names and relationship descriptions |
| Communication Protocol table rows | Message types, recipients, triggers |
| Agent Memory domain terms | Verbs, actions, items, examples |
| Completion message type | TASK_READY, ASSEMBLY_COMPLETE, EXECUTION_COMPLETE, etc. |

### GENERATE Elements (author from scratch per agent)

| Element | Notes |
|---------|-------|
| Workflow steps | Entirely domain-specific logic (5-8 steps typical) |
| Critical Rules | Domain-specific constraints (6-12 rules typical) |
| Error/Issue handling | Domain-specific failure scenarios |
| All unique sections | Template usage, item patterns, execution parameters, spawning, etc. |
| Extra tools beyond base 19 | Agent, TeamCreate, TeamDelete, EnterPlanMode, ExitPlanMode |
| `skills:` frontmatter field | Only when agent needs registered skills |

---

## Section 4: Communication Mode Decision Guide

| If the agent... | Use Option |
|-----------------|------------|
| Receives work from teammates and reports back | **A: Team-Protocol** |
| Spawns and manages other agents | **B: Orchestrator** |
| Operates independently (subagent, no team comms) | **C: Standalone** |

**Hybrid case:** If an agent both receives work AND spawns sub-agents (e.g., rf-assembler can be spawned as a subagent but also coordinates with rf-qa), use Option A as the base and add spawning sections from Option B as needed in the DOMAIN_DETAIL_SECTIONS zone.
