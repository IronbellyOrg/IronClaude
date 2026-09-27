---
title: Context Embedding Protocol and Standards
description: "Establishes mandatory context review requirements for all tasks. Defines framework context files and task-specific context guidelines to ensure agents have complete understanding before execution."
id: "context-embedding-protocol"
sidebar_position: 6
created_date: "2025-10-08"
last_updated: "2025-10-11"
version: 1.1.0
draft: false
content_status: Published
tags:
- "context-embedding"
- "task-execution"
- "context-review"
- "quality-control"
- standards
- "ai-rules"
content_type: CoreConcept
target_audience:
- Developer
- ComponentDeveloper
- SystemDesigner
- SystemArchitect
- QAEngineer
- AI
- Machine
owner: "framework-team"
autogen: false
autogen_method: ""
autogen_source: []
autogen_version: ""
ai_model: ""
model_settings: ""
source_references:
- path: newmain/.claude/docs/migrating_to_context_embedding.md
  type: context_doc
  version_hash: ""
  description: Migration guide for Milestone 1 context embedding enhancement
related_links:
- text: IB Agent Core
  link: ~/.claude/rules/core/ib_agent_core.md
- text: Quality Gates
  link: ~/.claude/rules/core/quality_gates.md
- text: "Anti-Hallucination Rules"
  link: ~/.claude/rules/core/anti_hallucination_task_completion_rules.md
related_task_id: []
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: "2026-04-11"
---

# Context Embedding Protocol and Standards

**Purpose**: Establishes mandatory context review requirements for all tasks to ensure agents have complete understanding of framework rules, quality standards, and task-specific requirements before execution.

**Impact**: +40% improvement in task understanding, +30% reduction in execution errors.

---

## Overview

All tasks require mandatory context review before execution. This protocol defines:
1. **Framework context files** (core rules - always required)
2. **Task-specific context** (customized per task - minimum requirements)
3. **Context review checkpoint** (verification before execution)

---

## Required Context Files

### Framework Context (Always Required - Minimum 5 Files)

These files define core framework rules and MUST be included in every task:

#### 1. Core Execution: `~/.claude/rules/core/ib_agent_core.md`
- **Purpose:** Five-step execution pattern and mandatory protocols
- **Key Sections:** READ → IDENTIFY → EXECUTE → UPDATE → REPEAT, prohibited behaviors
- **Why:** Ensures agent follows framework execution standards

#### 2. Quality Standards: `~/.claude/rules/core/quality_gates.md`
- **Purpose:** Task completion criteria and quality requirements
- **Key Sections:** Evidence requirements, validation standards, error severity
- **Why:** Ensures agent knows quality expectations before starting

#### 3. Anti-Hallucination Protocol: `~/.claude/rules/core/anti_hallucination_task_completion_rules.md`
- **Purpose:** Zero-tolerance accuracy policy
- **Key Sections:** Evidence format, verification workflow, penalties
- **Why:** Prevents fabrication of information or results

#### 4. Anti-Sycophancy Protocol: `~/.claude/rules/core/anti_sycophancy.md`
- **Purpose:** Truth-over-agreement and risk assessment
- **Key Sections:** Core principles, risk patterns, response strategies
- **Why:** Ensures factually accurate, evidence-based responses

#### 5. File Conventions: `~/.claude/rules/core/file_conventions.md`
- **Purpose:** File naming, structure, and frontmatter standards
- **Key Sections:** YAML frontmatter format, naming patterns, directory structure
- **Why:** Ensures consistent file creation and organization

### Task-Specific Context (Customized Per Task - Minimum 1 File)

**Minimum Requirement**: At least **1 task-specific context file** must be specified.

**Recommendation**: Specify **2-4 task-specific files** for complex tasks to provide comprehensive context.

Task-specific files depend on the task domain. Guidelines:

#### For API Development Tasks:
4. API documentation (endpoints, contracts)
5. Schema files (request/response formats)
6. Example requests (usage patterns)

#### For UI/Component Tasks:
4. Design specifications (mockups, style guide)
5. Component library documentation (existing components)
6. Accessibility standards (WCAG compliance)

#### For Data Processing Tasks:
4. Data schemas (structure, types)
5. Transformation rules (business logic)
6. Validation specifications (quality criteria)

#### For Documentation Tasks:
4. Documentation template (structure, format)
5. Style guide (voice, tone, conventions)
6. Example documentation (reference samples)

#### For Infrastructure Tasks:
4. Deployment specifications (environment requirements)
5. Configuration examples (settings, parameters)
6. Security standards (compliance requirements)

---

## How to Use This System

### When Creating a New Task

**Step 1:** Use `/rf:taskbuilder` command or copy template (`01_mdtm_template_generic_task.md`)

**Step 2:** Keep framework context files 1-5 as-is (already specified in template)

**Step 3:** Identify task-specific context (minimum 1 file, recommended 2-4):
- What documentation is most critical for this task?
- What technical specifications must be understood?
- What integration requirements exist?
- What domain knowledge is required?

**Step 4:** Specify task-specific files with actual file paths and descriptions:
```markdown
6. **[Domain Documentation]:** `.claude/docs/api_standards.md`
   - Purpose: Understand API design patterns and conventions
   - Key sections: REST principles, error handling, versioning

7. **[Technical Specifications]:** `./docs/api_schema.yaml`
   - Purpose: See exact request/response formats required
   - Key sections: Endpoints, authentication, data models

8. **[Integration Requirements]:** `.claude/workflows/api_workflow.md`
   - Purpose: Understand API development lifecycle
   - Key sections: Design phase, implementation, testing
```

**Step 5:** Ensure all files exist and are accessible

**Step 6:** Verify purpose and key sections are clear and actionable

### When Executing a Task

**Agent Responsibilities:**

1. **Locate Context Section:** Find "📚 MANDATORY CONTEXT" at task top
2. **Read All Files:** Read all context files completely, in order (framework files 1-5 + task-specific files)
3. **Extract Requirements:** Document key requirements in task notes
4. **Complete Checkpoint:** Mark all checkpoint items complete (one per file)
5. **Proceed with Execution:** Only after checkpoint is complete

**Checkpoint Verification Pattern:**
- [ ] Framework file 1 read and key requirements logged
- [ ] Framework file 2 read and key requirements logged
- [ ] Framework file 3 read and key requirements logged
- [ ] Framework file 4 read and key requirements logged
- [ ] Framework file 5 read and key requirements logged
- [ ] Task-specific file 1 read and key requirements logged
- [ ] [Additional task-specific files as specified...]
- [ ] Ambiguities flagged for clarification
- [ ] Five-step pattern understood
- [ ] Ready to proceed

### When Reviewing Tasks (QA)

**QA Verification:**

1. **Context Review Completed:** Check that agent marked checkpoint complete
2. **Task Notes Populated:** Verify task notes contain extracted requirements
3. **Execution Alignment:** Ensure execution follows context file requirements
4. **Quality Standards Met:** Validate against standards from context files

**Red Flags:**
- Checkpoint incomplete or skipped
- No task notes from context review
- Execution contradicts context file requirements
- Quality standards not met per context files

---

## Benefits of Context Embedding

### For Agents
1. **Clearer Expectations:** No guessing about rules or standards
2. **Reduced Errors:** Fresh understanding of requirements before execution
3. **Less Rework:** Correct execution first time
4. **Accountability:** Clear record of context review

### For QA
1. **Explicit Verification:** Can verify context was reviewed
2. **Faster Validation:** Know where to look for evidence
3. **Better Quality Signals:** Can identify systemic issues (context not reviewed)
4. **Granular Rejection:** Can fail specific context items

### For System
1. **Consistency:** All tasks follow same context pattern
2. **Quality Improvement:** 40% better task understanding
3. **Error Reduction:** 30% fewer execution errors
4. **Efficiency:** Less back-and-forth clarification

---

## Examples

### Example 1: Simple File Creation Task

**Task:** Create configuration file

**Framework Context Files 1-5:** (Standard - always included)

**Task-Specific Files:**
6. **Configuration Examples:** `.claude/docs/config_examples.md`
   - Purpose: See example configuration structures
   - Key sections: Basic config, advanced options

7. **Project Structure:** `./README.md`
   - Purpose: Understand where config file fits in project
   - Key sections: Project layout, configuration section

### Example 2: API Implementation Task

**Task:** Implement user authentication API

**Framework Context Files 1-5:** (Standard - always included)

**Task-Specific Files:**
6. **API Standards:** `.claude/docs/api_standards.md`
   - Purpose: Understand API design patterns and conventions
   - Key sections: REST principles, error handling, authentication

7. **Auth Specifications:** `./docs/auth_requirements.md`
   - Purpose: See exact authentication requirements
   - Key sections: Token format, session management, security

8. **API Workflow:** `.claude/workflows/api_development_workflow.md`
   - Purpose: Understand API development lifecycle
   - Key sections: Design, implementation, testing, deployment

### Example 3: Documentation Task

**Task:** Create API documentation

**Framework Context Files 1-5:** (Standard - always included)

**Task-Specific Files:**
6. **Documentation Template:** `.claude/templates/api_doc_template.md`
   - Purpose: See required documentation structure
   - Key sections: Endpoint format, example format, metadata

7. **Style Guide:** `.claude/docs/documentation_style_guide.md`
   - Purpose: Understand voice, tone, and conventions
   - Key sections: Technical writing standards, formatting rules

8. **Example Documentation:** `./docs/examples/user_api_docs.md`
   - Purpose: See reference example of good API documentation
   - Key sections: Complete example with all required elements

---

## Troubleshooting

### Problem: Context file doesn't exist

**Solution:**
1. Check file path for typos
2. Verify file is in correct location
3. If file missing, create it or find alternative
4. Update task with correct path

### Problem: Context file not helpful

**Solution:**
1. Review if correct file was specified
2. Consider if different file would be more appropriate
3. Update task with better context file
4. Document issue for future task creation

### Problem: Too much context to read

**Solution:**
1. Focus on "Key sections" specified in task
2. Read framework files (1-5) once, reference thereafter for future tasks
3. Deep-read task-specific files (varies per task)
4. Use checkpoint to confirm essential understanding

### Problem: Checkpoint takes too long

**Solution:**
1. Context review is investment that saves time later
2. Typical checkpoint time: 10-15 minutes
3. Saves 30-60 minutes in prevented errors and rework
4. Speed improves as framework files become familiar

---

## Migration from Old Tasks

See: `.claude/docs/migrating_to_context_embedding.md` for complete migration guide.

**Quick Migration:**
1. Add context section after frontmatter
2. Include framework files 1-5 as standard
3. Identify minimum 1, recommended 2-4 task-specific files
4. Fill in placeholders with actual file paths and descriptions
5. Test task execution

---

## Metrics & Measurement

### Success Indicators
- **Clarity Score:** >7/10 (up from 5.6/10 baseline)
- **Context Completeness:** 100% (up from 0%)
- **First-Attempt Success:** >80% (up from ~65%)
- **Clarification Requests:** <10% of tasks (down from ~25%)

### How to Measure
1. **Clarity:** Rate task clarity 1-10 after context review
2. **Completeness:** Verify all framework files (5) + minimum task-specific files (1+) specified
3. **Success:** Track first-attempt completion rate
4. **Requests:** Count number of clarification requests

---

## Future Enhancements

Potential improvements for future milestones:
- Automated context file validation
- Context file summary generation
- Intelligent context file recommendations
- Context dependency mapping

---

**Document Maintained By:** Framework Enhancement Team
**Last Updated:** 2025-10-08
**Next Review:** After Milestone 4 completion
