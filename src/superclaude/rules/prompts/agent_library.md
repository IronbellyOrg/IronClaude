---
title: "Agent Library - Available Worker and QA Agents"
description: "Reference library of all available worker and QA agents in the Rigorflow framework, including their specializations, use cases, and prompt file locations. Guides task assignment and agent selection during task creation."
id: "agent-library"
sidebar_position: 1
created_date: "2025-10-15"
last_updated: "2025-10-15"
version: 1.0.0
draft: false
content_status: Published
tags:
- agents
- workflow
- "task-assignment"
- rigorflow
- reference
content_type: Reference
target_audience:
- AI
- Machine
- Developer
- SystemArchitect
owner: "framework-team"
autogen: false
autogen_method: ""
autogen_source: []
autogen_version: ""
ai_model: ""
model_settings: ""
related_links:
- text: IB Agent Core Rules
  link: ~/.claude/rules/core/ib_agent_core.md
- text: Task Builder Command
  link: .claude/commands/rf/taskbuilder.md
- text: Automated QA Workflow Script
  link: .claude/scripts/automated_qa_workflow.sh
related_task_id: []
review_info:
  last_reviewed_by: "framework-team"
  last_review_date: "2025-10-15"
  next_review_date: "2026-04-15"
---

# Agent Library

This document provides a reference library of all available worker and QA agents in the Rigorflow framework. Use this guide when:
- Creating new tasks (selecting appropriate agent)
- Understanding agent capabilities and specializations
- Assigning tasks to agents via the `assigned_to` field

---

## Quick Reference Table

| Agent Name | Specialization | Best For | Worker Prompt | QA Prompt |
|------------|----------------|----------|---------------|-----------|
| **automated_qa_workflow** | General documentation and code tasks | Default/fallback for generic tasks, mixed content work | `automated_qa_workflow_worker_prompt.md` | `automated_qa_workflow_qa_prompt.md` |
| **doc_code_analyst** | Code analysis and API documentation | Deep C++ analysis, API reference generation, technical documentation from source code | `doc_code_analyst_worker_prompt.md` | `doc_code_analyst_qa_prompt.md` |
| **documentation_expert** | Documentation structure and product docs | Creating documentation ecosystems, information architecture, product documentation, PRDs | `documentation_expert_worker_prompt.md` | `documentation_expert_qa_prompt.md` |
| **recruiting_expert** | Candidate evaluation and recruiting | Scoring candidates against rubrics, technical recruiting, talent evaluation | `recruiting_expert_worker_prompt.md` | `recruiting_expert_qa_prompt.md` |

---

## Agent Profiles

### 1. automated_qa_workflow (Generic Worker)

**Role**: Default worker agent for general-purpose documentation and code tasks.

**Specialization**:
- Mixed documentation and code work
- Generic task execution following standard patterns
- Fallback for tasks without specialized agent assignment

**Best For**:
- Simple documentation updates
- File creation and modification
- Tasks that don't require domain expertise
- Mixed workflows combining multiple task types

**Key Capabilities**:
- Batch-oriented checklist completion
- Standard file operations (create, read, edit)
- Basic quality verification
- Generic handoff creation

**When to Use**:
- Task doesn't fit specialized agent categories
- Simple, straightforward work
- No deep domain knowledge required
- Default choice when uncertain

**Prompt Files**:
- Worker: `~/.claude/rules/prompts/automated_qa_workflow_worker_prompt.md`
- QA: `~/.claude/rules/prompts/automated_qa_workflow_qa_prompt.md`

---

### 2. doc_code_analyst (Code Analysis Specialist)

**Role**: Code analysis specialist for deep technical analysis of source code and API documentation generation.

**Specialization**:
- Deep technical analysis of C++ source code
- Header and implementation file paired analysis
- API reference documentation generation
- Extracting configuration and architectural patterns

**Best For**:
- Analyzing C++ plugins and modules
- Generating API reference documentation
- Extracting UPROPERTY, attributes, and configuration
- Documenting system architecture from code
- Creating parameter ontologies

**Key Capabilities**:
- Paired C++ file analysis (.h + .cpp together)
- Source reference tracking (file:line format)
- Confidence scoring for findings
- Anti-hallucination evidence tables
- Raw and consolidated analysis reports
- Cross-cutting insight identification

**When to Use**:
- Working with C++ codebases (especially Unreal Engine)
- Need API documentation generated from source
- Require deep technical analysis of systems
- Building reference documentation from code
- Extracting configurable elements

**Prompt Files**:
- Worker: `~/.claude/rules/prompts/doc_code_analyst_worker_prompt.md`
- QA: `~/.claude/rules/prompts/doc_code_analyst_qa_prompt.md`

---

### 3. documentation_expert (Documentation & Product Specialist)

**Role**: Senior documentation and product systems architect for comprehensive documentation ecosystems.

**Specialization**:
- Information architecture and organization
- SaaS product documentation
- Product development documentation (PRDs, specs, roadmaps)
- Technical writing and style guide compliance
- Gaming and technical product documentation

**Best For**:
- Creating documentation structures and ecosystems
- Product Requirements Documents (PRDs)
- Feature specifications and design docs
- User guides and API documentation
- Documentation reorganization and IA work
- Product vision and strategy documents

**Key Capabilities**:
- Information architecture excellence
- YAML frontmatter and metadata management
- Placeholder note creation with clear guidance
- Structure-first approach (scaffolding before content)
- Multi-document ecosystem creation
- Style guide compliance

**When to Use**:
- Building comprehensive documentation systems
- Product documentation projects
- Need strong IA and organization
- Creating document structures with placeholders
- Working backwards from product vision
- Strategic product documentation

**Prompt Files**:
- Worker: `~/.claude/rules/prompts/documentation_expert_worker_prompt.md`
- QA: `~/.claude/rules/prompts/documentation_expert_qa_prompt.md`

---

### 4. recruiting_expert (Recruiting & Talent Evaluation Specialist)

**Role**: Expert recruiting strategist and talent evaluator for systematic candidate evaluation.

**Specialization**:
- Candidate evaluation against scoring rubrics
- Technical recruiting for engineering roles
- Multi-category weighted scoring systems
- Candidate file processing and organization

**Best For**:
- Evaluating technical candidates
- Scoring against weighted rubrics
- Generating candidate summaries
- Organizing candidate pipelines
- Identifying top talent

**Key Capabilities**:
- Rubric-based evaluation (8-category scoring)
- Weighted score calculation and star ratings
- Evidence-based scoring from candidate files
- Candidate file processing and movement
- Incremental saving after each candidate
- Anti-hallucination controls for accurate scoring

**When to Use**:
- Technical recruiting projects
- Candidate evaluation workflows
- Scoring candidates against criteria
- Building candidate databases
- Talent pipeline management

**Prompt Files**:
- Worker: `~/.claude/rules/prompts/recruiting_expert_worker_prompt.md`
- QA: `~/.claude/rules/prompts/recruiting_expert_qa_prompt.md`

---

## Agent Selection Guidelines

### Decision Matrix

Use this matrix to select the appropriate agent for your task:

| If Your Task Involves... | Choose This Agent |
|-------------------------|-------------------|
| Deep C++ code analysis, API documentation from source | **doc_code_analyst** |
| Creating documentation structures, PRDs, product docs | **documentation_expert** |
| Evaluating candidates, scoring against rubrics | **recruiting_expert** |
| Simple file operations, mixed work, unclear fit | **automated_qa_workflow** |

### Selection Process

When creating a task:

1. **Identify primary task domain**:
   - Code analysis? → `doc_code_analyst`
   - Documentation creation? → `documentation_expert`
   - Candidate evaluation? → `recruiting_expert`
   - General/mixed work? → `automated_qa_workflow`

2. **Consider task complexity**:
   - Simple tasks: Can use default `automated_qa_workflow`
   - Complex/specialized tasks: Choose specialist agent

3. **Check agent capabilities**:
   - Review "Best For" section above
   - Ensure agent has required expertise

4. **Set in task frontmatter**:
   ```yaml
   assigned_to: "doc_code_analyst"  # or other agent name
   ```

---

## QA Agent Pairing

**Important**: Each worker agent has a corresponding QA agent that specializes in validating the same type of work.

**Automatic Pairing**: The workflow script (`automated_qa_workflow.sh`) automatically uses the matching QA agent:
- Worker: `doc_code_analyst_worker_prompt.md` → QA: `doc_code_analyst_qa_prompt.md`
- Worker: `documentation_expert_worker_prompt.md` → QA: `documentation_expert_qa_prompt.md`
- Worker: `recruiting_expert_worker_prompt.md` → QA: `recruiting_expert_qa_prompt.md`
- Worker: `automated_qa_workflow_worker_prompt.md` → QA: `automated_qa_workflow_qa_prompt.md`

**No Manual Assignment Required**: You only need to specify the worker agent in the task's `assigned_to` field. The QA agent is automatically selected based on naming convention.

---

## Creating Custom Agents

To create a new specialized agent:

1. **Create worker prompt**: `~/.claude/rules/prompts/{agent_name}_worker_prompt.md`
2. **Create QA prompt**: `~/.claude/rules/prompts/{agent_name}_qa_prompt.md`
3. **Follow naming convention**: `{agent_name}_worker_prompt.md` and `{agent_name}_qa_prompt.md`
4. **Add to this library**: Update the Quick Reference Table and Agent Profiles
5. **Test thoroughly**: Create test task and validate workflow

**Template Locations**:
- Worker prompts follow structure of `automated_qa_workflow_worker_prompt.md`
- QA prompts follow structure of `automated_qa_workflow_qa_prompt.md`
- Both must support batch processing and template variables

---

## Related Documentation

- **Delegation Matrix**: See `~/.claude/rules/core/ib_agent_core.md` for delegation decision framework
- **Task Creation**: See `.claude/commands/rf/taskbuilder.md` for interactive task creation with agent selection
- **Workflow Script**: See `.claude/scripts/automated_qa_workflow.sh` for agent prompt loading logic
- **Prompt Templates**: See `.claude/templates/` for worker and QA prompt templates

---

**Last Updated**: 2025-10-15
**Maintained By**: Framework Team
**Version**: 1.0.0
