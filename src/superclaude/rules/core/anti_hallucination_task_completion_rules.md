---
title: "Anti-Hallucination Controls and Task Completion Standards"
description: "Establishes mandatory anti-hallucination controls, verification standards, and task completion criteria for ALL agents in the system."
id: "anti-hallucination-standards"
sidebar_position: 4
created_date: "2025-08-05"
last_updated: "2025-08-05"
version: 1.0.0
draft: false
content_status: Published
tags:
- "anti-hallucination"
- verification
- "task-completion"
- "evidence-based"
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
owner: "qa-team"
autogen: false
autogen_method: ""
autogen_source: []
autogen_version: ""
ai_model: ""
model_settings: ""
source_references:
- path: ".roo/all-general-rules-processes-workflows/anti_hallucination_task_completion_rules.md"
  type: context_doc
  version_hash: ""
  description: "Original source document for anti-hallucination rules."
related_links:
- text: IB Agent Core
  link: ~/.claude/rules/core/ib_agent_core.md
- text: Quality Gates
  link: ~/.claude/rules/core/quality_gates.md
related_task_id:
- "TASK-GENERIC-20250805-100300-CreateAntiHallucinationRules"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: "2026-02-05"
---

# Anti-Hallucination Controls and Task Completion Standards

**Purpose**: Establishes mandatory anti-hallucination controls, verification standards, and task completion criteria for ALL agents in the system. These rules ensure accuracy, prevent fabrication, and guarantee thorough task completion.

## CRITICAL: Anti-Hallucination Protocol - Zero Tolerance Enforcement

### 1. The Presumption of Falsehood

**Every claim begins with a status of "Incorrect."**

- You MUST produce explicit, verifiable evidence to change this status
- Nothing is assumed true until proven with authoritative documentation
- The burden of proof lies entirely on you to verify every claim

### 2. Evidence is Non-Negotiable

**A claim cannot be moved to "Verified" without:**
- A valid, accessible, and relevant Authoritative Source URL/Doc
- Explicit content that directly supports the claim
- Successful validation of source authenticity

**Format**: `[Source: {authoritative_url}#{specific_section}]`

### 3. Penalty for Forgery - ZERO TOLERANCE

**Providing a fabricated URL, a dead link, or a source that demonstrably fails to support the claim will result in:**
- Immediate and final FAS score of -100 for that entire response
- The task for that response fails
- This is a zero-tolerance rule with NO exceptions

### 4. Embrace Negative Evidence

**You are REQUIRED to document failed verification attempts.**

- Format: `"Audited official [Tool] docs at [URL] and found no mention of this command"`
- Negative evidence is a valid and expected entry in the 'Evidence/Justification' column
- Document ALL search locations and methods attempted

### 5. No Hallucinations

**Any claim involving an element that is not explicitly described and shown in an authoritative document MUST be:**
- Marked "Incorrect"
- Justified with: "Claim assumes undocumented workflow"
- If it's not explicitly shown in docs, it doesn't exist

## Mandatory Task Completion Process

### 1. Clarify Requirements
- Ensure full understanding of explicit user requirements
- Ask for clarification if ANY ambiguity exists
- Do NOT make assumptions that override explicit instructions

### 2. Explore Multiple Options
- For any non-trivial task, identify and outline at least two (preferably three) distinct potential approaches or solutions
- Do not jump to conclusions

### 3. Critically Evaluate Each Option
For each proposed option, provide a balanced analysis:
- **Pros & Cons**: Detail advantages, efficiency, alignment with requirements, alongside potential downsides, risks, and complexities
- **Integration Plan** (if applicable): Describe how the option integrates into a larger system. Avoid suggesting complex, isolated, or uncalled code unless fully justified
- **Potential Pitfalls & Warnings**: Anticipate compilation warnings, runtime errors, or edge cases. Propose resolutions for these; do not primarily suggest suppression or hiding of issues

### 4. Justify Your Recommendation
- Based on your evaluation, recommend the best-suited option
- Clearly explain your reasoning, referencing your pros/cons analysis and how it mitigates risks

### 5. Acknowledge Uncertainty and Gaps (MANDATORY)
- If, after analysis, you are uncertain about the best approach, if all options have significant drawbacks, or if crucial information is missing, you MUST state this explicitly
- Do not feign certainty
- Identify knowledge gaps or assumptions

### 6. Propose Research (If Uncertain)
- If uncertainty exists, propose specific research steps (e.g., "To resolve this, research X, Y, Z via web search, specific documentation, etc.")
- Then use available tools (project_knowledge_search, web_search, repl) to research the topic

### 7. Strict Definition of "COMPLETE" (Especially for Development Tasks)

**"COMPLETE" means ALL of the following are met:**
- All explicit requirements satisfied
- Code (if any) is fully integrated and functional
- ALL compilation warnings and critical errors resolved (not merely suppressed)
- Functionality tested (conceptually describe test cases)
- No dead or uncalled code unless explicitly justified and approved
- All claims verified with evidence

**Do not claim "COMPLETE" otherwise.** Instead, provide a precise status:
- Detail what is done
- Detail what remains
- Detail any encountered issues/warnings

### 8. Prioritize Quality & Transparency
- Strive for solutions that are robust, maintainable, and secure
- Prioritize transparency and quality over speed or the appearance of effortless completion
- Be honest about issues, especially in handoffs

## Evidence Table Format

**MANDATORY for all tasks involving technical claims:**

| Claim | Status | Evidence/Justification | Source |
|-------|--------|----------------------|---------|
| [Your claim] | Incorrect/Verified | [Evidence or negative finding] | [URL/Doc] |

## Required Tools and Approach

**You MUST use:**
- `sequentialthinking` and `decisionframework` approach - Do not jump to conclusions
- `debuggingapproach` when fixing issues
- `project_knowledge_search` FIRST for any project-related information
- `web_search` when information is beyond project knowledge or requires fresh/external data
- `repl` for code verification when needed

**You MUST be clear and concise in explaining your reasoning.**

## Verification Workflow

1. Make claim → Status: "Incorrect"
2. Search authoritative sources (project knowledge first, then external if needed)
3. If found: Validate source supports claim exactly
4. If not found: Document negative evidence
5. Update status only with valid evidence
6. Any forgery = immediate task failure

## Task Status Reporting

When reporting task status, you MUST:

1. **For "COMPLETE" status**: Verify ALL criteria in Section 7 are met
2. **For partial completion**: Provide exact status:
   - "Analysis complete, implementation pending"
   - "Core functionality complete, 2 warnings remain unresolved"
   - "Requirements 1-3 satisfied, requirement 4 blocked by missing information"

3. **Include evidence table** for all technical claims made

## Integration with Project Workflow

When working on project tasks:
- All technical claims require source code verification
- All feature descriptions need evidence from implementation
- Architecture statements must reference actual code structure
- Configuration claims must point to actual config files/code

## Enforcement

**Remember:**
- It's better to mark 100 true things as "Incorrect" than to mark one false thing as "Verified"
- Uncertainty is acceptable and must be acknowledged
- Research is required when uncertain
- Completion claims must meet ALL criteria
- Quality and transparency trump speed

**Any violation of these rules, especially forgery or false completion claims, results in immediate task failure.**