---
title: Automated Quality Gates for Task Outputs
description: Defines the automated checks and error severity levels for task outputs to ensure high quality and consistency.
id: "quality-gates"
sidebar_position: 2
created_date: "2025-08-05"
last_updated: "2025-10-14"
version: 1.1.0
draft: false
content_status: Published
tags:
- "quality-gates"
- validation
- verification
- "error-severity"
- standards
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
- path: ".roo/all-general-rules-processes-workflows/quality_gates.md"
  type: context_doc
  version_hash: ""
  description: Base document adapted for generic quality gates.
related_links:
- text: IB Agent Core
  link: ~/.claude/rules/core/ib_agent_core.md
- text: File Conventions
  link: ~/.claude/rules/core/file_conventions.md
- text: "Anti-Sycophancy Protocol"
  link: ~/.claude/rules/core/anti_sycophancy.md
related_task_id:
- "TASK-GENERIC-20250805-100100-CreateGenericQualityGates"
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: "2026-02-05"
---

# Automated Quality Gates for Task Outputs

All task outputs must pass appropriate quality gates before being considered complete. The specific checks vary by output type, but follow consistent principles of verification, validation, and quality assurance.

## Universal Quality Gate Principles

1. **Verifiability**: All outputs must be traceable to source requirements
2. **Completeness**: All specified requirements must be satisfied
3. **Correctness**: Technical accuracy verified against sources
4. **Consistency**: Uniform formatting and conventions followed
5. **Clarity**: Clear, understandable, and well-structured
6. **Anti-Sycophancy**: Responses must be factually accurate over agreeable (v5.2)

## Quality Gate Categories by Output Type

### Documentation Outputs

| Check Category      | Specific Check                                                                 | Pass Criteria                                                      |
| :------------------ | :----------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| **Metadata**        | Valid frontmatter/metadata structure?                                          | Must follow project conventions                                    |
|                     | All required fields present per project standards?                             | All required fields populated                                      |
|                     | Source references documented?                                                   | Sources tracked for all claims                                     |
| **Structure**       | Proper heading hierarchy?                                                       | Valid hierarchy, no skipped levels                                 |
|                     | Consistent formatting conventions?                                              | Follows project style guide                                        |
| **Code Blocks**     | All code examples properly formatted?                                           | Language identifiers, proper syntax                                |
|                     | Code examples verified against actual implementation?                           | Must match source files                                            |
| **Links**           | All internal links valid?                                                       | Links resolve correctly                                            |
|                     | External links accessible?                                                      | No dead links                                                      |
| **Content**         | Technical accuracy verified?                                                    | All claims verified against sources                                |
|                     | No hallucinated or fabricated content?                                          | Zero tolerance for fabrication                                     |

### Code/Script Outputs

| Check Category      | Specific Check                                                                 | Pass Criteria                                                      |
| :------------------ | :----------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| **Syntax**          | Passes language linter/formatter?                                               | No syntax errors                                                   |
|                     | Follows project coding standards?                                               | Adheres to style guide                                             |
| **Functionality**   | Core requirements implemented?                                                  | All specified features work                                        |
|                     | Error handling present?                                                         | Graceful error handling                                            |
| **Testing**         | Unit tests pass?                                                                | All tests green                                                    |
|                     | Integration verified?                                                           | Works with existing code                                           |
| **Documentation**   | Inline documentation present?                                                   | Functions/classes documented                                       |
|                     | Usage examples provided?                                                        | Clear how to use                                                   |

### Data/Configuration Outputs

| Check Category      | Specific Check                                                                 | Pass Criteria                                                      |
| :------------------ | :----------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| **Format**          | Valid structure (JSON/YAML/etc)?                                                | Parseable without errors                                           |
|                     | Schema compliance?                                                              | Matches defined schema                                             |
| **Completeness**    | All required fields present?                                                    | No missing required data                                           |
|                     | Default values appropriate?                                                     | Sensible defaults provided                                         |
| **Validation**      | Data types correct?                                                             | Types match specification                                          |
|                     | Value ranges valid?                                                             | Within acceptable bounds                                           |

### Analysis/Report Outputs

| Check Category      | Specific Check                                                                 | Pass Criteria                                                      |
| :------------------ | :----------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| **Evidence**        | All findings supported by evidence?                                             | Citations for all claims                                           |
|                     | Evidence table/log present?                                                     | Structured evidence tracking                                       |
| **Completeness**    | All specified areas analyzed?                                                   | Full scope coverage                                                |
|                     | Negative results documented?                                                    | "Not found" explicitly stated                                      |
| **Structure**       | Clear summary provided?                                                         | Executive summary present                                          |
|                     | Actionable recommendations?                                                     | Clear next steps identified                                        |

### Anti-Sycophancy Opinion Analysis Outputs (/rf:opinion command)

| Check Category           | Specific Check                                                                 | Pass Criteria                                                      |
| :----------------------- | :----------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| **Risk Assessment**      | Risk score and level documented?                                               | Score (0.0-1.0) and level (Low/Medium/High/Critical) present      |
| **Layer Activation**     | Which analysis layers were applied?                                            | Activated layers explicitly listed ([1][2][3])                     |
| **Layer 1 Analysis**     | Constitutional AI directives applied?                                          | Core principles documented (if Layer 1 activated)                  |
| **Layer 2 Analysis**     | Fact-checking verification results present?                                    | CoVe verification results documented (if Layer 2 activated)        |
| **Layer 3 Analysis**     | Multi-perspective analysis provided?                                           | Alternative viewpoints presented (if Layer 3 activated)            |
| **Evidence**             | Citations and sources provided?                                                | Verifiable sources cited for factual claims                        |
| **Confidence Level**     | Uncertainty explicitly stated?                                                 | High/Medium/Low confidence documented                              |
| **Synthesis**            | Objective conclusion with balanced perspective?                                | Final synthesis acknowledges valid points from multiple sides      |

**Note**: This category applies only to outputs from the `/rf:opinion` command (Tier 2 anti-sycophancy analysis). Standard responses follow Tier 1 behavioral requirements checked under Evidence Verification and Analysis/Report categories.

## Evidence Verification Requirements

For any task output making technical claims:

| Requirement         | Description                                                                    | Implementation                                                     |
| :------------------ | :----------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| **Evidence Table**  | Structured tracking of all claims                                               | Required for technical outputs                                     |
| **Status Tracking** | Each claim marked as "Verified" or "Unverified"                                | Explicit status required                                           |
| **Source Links**    | Valid references to source material                                             | Must be accessible                                                 |
| **Negative Evidence** | Document what was checked but not found                                       | "Audited [source] and found no mention of [claim]"                |
| **Zero Fabrication** | No made-up URLs, sources, or claims                                          | Automatic task failure if detected                                 |

## Task Completion Standards

A task is only considered "COMPLETE" when:

1. ✓ All checklist items marked as done
2. ✓ All outputs pass relevant quality gates
3. ✓ Evidence verification complete (where applicable)
4. ✓ No placeholder or temporary content remains
5. ✓ All follow-up items documented in task log
6. ✓ Task status updated to "🟢 Done"

## Error Severity Levels

The following severity levels apply to all quality gate failures:

| Severity Level | Description                                                                                                | Action Required |
| :------------- | :--------------------------------------------------------------------------------------------------------- | :-------------- |
| **Sev 1**      | Critical error; blocks functionality, creates security risk, or fundamentally misleads                     | Immediate fix   |
| **Sev 2**      | Important issue; impacts usability or understanding but doesn't block core functionality                   | Fix in cycle    |
| **Sev 3**      | Minor issue; cosmetic or style problems not impacting functionality                                        | Fix when able   |

## Quality Gate Automation

Where possible, quality gates should be automated through:

- Linting tools for code and documentation
- Schema validators for structured data
- Link checkers for references
- Test suites for functionality
- Custom validation scripts for project-specific requirements

## Customization Guidelines

Projects should extend these quality gates by:

1. Adding project-specific validation rules
2. Defining required metadata fields
3. Specifying coding/documentation standards
4. Creating custom validation scripts
5. Setting project-appropriate thresholds

*Failure to meet quality gates requires revision before task completion.*